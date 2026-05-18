from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


class StateValidationError(ValueError):
    """Raised when PROJECT_STATE.json violates the canonical spec."""


CANONICAL_PHASES = frozenset(
    {
        "TOPIC",
        "SCRIPT",
        "SCENES",
        "ASSETS",
        "ASSEMBLY",
        "AUDIO",
        "QA",
        "READY_FOR_UPLOAD",
        "UPLOADED",
        "ARCHIVED",
        "HALT",
    }
)

REQUIRED_TOP_LEVEL_FIELDS = (
    "project_id",
    "phase",
    "phase_history",
    "updated_at",
    "halted",
    "halt_reason",
    "resume_hint",
    "approval_status",
    "approved_for_upload",
    "qa_passed",
    "artifacts",
    "manifest",
)

REQUIRED_MANIFEST_FIELDS = (
    "manifest_id",
    "manifest_version",
    "manifest_hash",
    "mode",
    "niche",
    "audience",
    "content_language",
    "primary_platform",
    "topic",
    "working_title",
    "hook",
    "target_duration_sec",
    "render_profile",
    "stock_policy",
    "created_at",
    "locked",
)

MUTABLE_TOP_LEVEL_FIELDS = frozenset(
    {
        "phase",
        "phase_history",
        "updated_at",
        "halted",
        "halt_reason",
        "resume_hint",
        "approval_status",
        "approved_for_upload",
        "qa_passed",
        "artifacts",
    }
)


def _ensure_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise StateValidationError(f"{name} must be an object/dict")
    return value


def _require_fields(payload: Mapping[str, Any], required_fields: tuple[str, ...], name: str) -> None:
    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise StateValidationError(f"{name} is missing required fields: {', '.join(missing)}")


def _ensure_non_empty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StateValidationError(f"{name} must be a non-empty string")
    return value


def _ensure_boolean(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise StateValidationError(f"{name} must be boolean")
    return value


def _ensure_positive_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise StateValidationError(f"{name} must be a positive integer")
    return value


def _ensure_iso8601(value: Any, name: str) -> str:
    text = _ensure_non_empty_string(value, name)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise StateValidationError(f"{name} must be ISO-8601 compatible") from exc
    return text


def _ensure_phase(value: Any, name: str) -> str:
    phase = _ensure_non_empty_string(value, name).strip().upper()
    if phase not in CANONICAL_PHASES:
        raise StateValidationError(
            f"{name} must be one of: {', '.join(sorted(CANONICAL_PHASES))}"
        )
    return phase


def _validate_phase_history_entry(value: Any, index: int) -> dict[str, Any]:
    entry_name = f"phase_history[{index}]"
    entry = dict(_ensure_mapping(value, entry_name))
    _require_fields(entry, ("from", "to", "at"), entry_name)

    entry["from"] = _ensure_phase(entry["from"], f"{entry_name}.from")
    entry["to"] = _ensure_phase(entry["to"], f"{entry_name}.to")
    entry["at"] = _ensure_iso8601(entry["at"], f"{entry_name}.at")
    return entry


def build_manifest_payload_for_hash(manifest: Mapping[str, Any]) -> dict[str, Any]:
    manifest_dict = copy.deepcopy(dict(_ensure_mapping(manifest, "manifest")))
    manifest_dict.pop("manifest_hash", None)
    return manifest_dict


def compute_manifest_hash(manifest: Mapping[str, Any]) -> str:
    payload = build_manifest_payload_for_hash(manifest)
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def validate_manifest(manifest: Mapping[str, Any], *, project_id: str | None = None) -> dict[str, Any]:
    manifest_dict = dict(_ensure_mapping(manifest, "manifest"))
    _require_fields(manifest_dict, REQUIRED_MANIFEST_FIELDS, "manifest")

    _ensure_non_empty_string(manifest_dict["manifest_id"], "manifest.manifest_id")
    manifest_version = _ensure_positive_int(
        manifest_dict["manifest_version"],
        "manifest.manifest_version",
    )
    _ensure_non_empty_string(manifest_dict["manifest_hash"], "manifest.manifest_hash")
    mode = _ensure_non_empty_string(manifest_dict["mode"], "manifest.mode")
    _ensure_non_empty_string(manifest_dict["niche"], "manifest.niche")
    _ensure_non_empty_string(manifest_dict["audience"], "manifest.audience")
    _ensure_non_empty_string(manifest_dict["content_language"], "manifest.content_language")
    _ensure_non_empty_string(manifest_dict["primary_platform"], "manifest.primary_platform")
    _ensure_non_empty_string(manifest_dict["topic"], "manifest.topic")
    _ensure_non_empty_string(manifest_dict["working_title"], "manifest.working_title")
    _ensure_non_empty_string(manifest_dict["hook"], "manifest.hook")
    _ensure_positive_int(manifest_dict["target_duration_sec"], "manifest.target_duration_sec")
    _ensure_non_empty_string(manifest_dict["render_profile"], "manifest.render_profile")
    _ensure_non_empty_string(manifest_dict["stock_policy"], "manifest.stock_policy")
    _ensure_iso8601(manifest_dict["created_at"], "manifest.created_at")
    locked = _ensure_boolean(manifest_dict["locked"], "manifest.locked")

    if mode != "cashflow-mode":
        raise StateValidationError("manifest.mode must be 'cashflow-mode'")

    if locked is not True:
        raise StateValidationError("manifest.locked must be true")

    if project_id is not None:
        expected_manifest_id = f"{project_id}:v{manifest_version}"
        if manifest_dict["manifest_id"] != expected_manifest_id:
            raise StateValidationError(
                f"manifest.manifest_id must be '{expected_manifest_id}'"
            )

    expected_hash = compute_manifest_hash(manifest_dict)
    if manifest_dict["manifest_hash"] != expected_hash:
        raise StateValidationError(
            "manifest.manifest_hash does not match the canonical manifest payload"
        )

    return copy.deepcopy(manifest_dict)


def validate_state(state: Mapping[str, Any]) -> dict[str, Any]:
    state_dict = dict(_ensure_mapping(state, "PROJECT_STATE"))
    _require_fields(state_dict, REQUIRED_TOP_LEVEL_FIELDS, "PROJECT_STATE")

    project_id = _ensure_non_empty_string(state_dict["project_id"], "project_id")
    phase = _ensure_phase(state_dict["phase"], "phase")

    phase_history = state_dict["phase_history"]
    if not isinstance(phase_history, list):
        raise StateValidationError("phase_history must be a list")
    state_dict["phase_history"] = [
        _validate_phase_history_entry(entry, index)
        for index, entry in enumerate(phase_history)
    ]

    _ensure_iso8601(state_dict["updated_at"], "updated_at")
    halted = _ensure_boolean(state_dict["halted"], "halted")
    approved_for_upload = _ensure_boolean(state_dict["approved_for_upload"], "approved_for_upload")
    _ensure_boolean(state_dict["qa_passed"], "qa_passed")
    approval_status = _ensure_non_empty_string(state_dict["approval_status"], "approval_status")

    if state_dict["halt_reason"] is not None and not isinstance(state_dict["halt_reason"], str):
        raise StateValidationError("halt_reason must be null or string")

    if state_dict["resume_hint"] is not None and not isinstance(state_dict["resume_hint"], str):
        raise StateValidationError("resume_hint must be null or string")

    if phase == "HALT" and halted is not True:
        raise StateValidationError("halted must be true when phase is 'HALT'")

    if phase != "HALT" and halted is not False:
        raise StateValidationError("halted must be false when phase is not 'HALT'")

    if approved_for_upload and approval_status != "APPROVED":
        raise StateValidationError(
            "approval_status must be 'APPROVED' when approved_for_upload is true"
        )

    artifacts = state_dict["artifacts"]
    if not isinstance(artifacts, dict):
        raise StateValidationError("artifacts must be an object/dict")

    final_video_path = artifacts.get("final_video_path")
    if final_video_path is not None:
        _ensure_non_empty_string(final_video_path, "artifacts.final_video_path")

    state_dict["phase"] = phase
    state_dict["manifest"] = validate_manifest(state_dict["manifest"], project_id=project_id)
    return copy.deepcopy(state_dict)


def load_state(path: str | Path) -> dict[str, Any]:
    state_path = Path(path)
    try:
        raw = json.loads(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StateValidationError(f"State file not found: {state_path}") from exc
    except json.JSONDecodeError as exc:
        raise StateValidationError(f"State file is not valid JSON: {state_path}") from exc

    return validate_state(raw)


def assert_runtime_mutation_only(
    previous_state: Mapping[str, Any],
    candidate_state: Mapping[str, Any],
) -> None:
    previous = validate_state(previous_state)
    candidate = validate_state(candidate_state)

    if previous["project_id"] != candidate["project_id"]:
        raise StateValidationError("project_id cannot change")

    previous_manifest = previous["manifest"]
    candidate_manifest = candidate["manifest"]

    previous_version = previous_manifest["manifest_version"]
    candidate_version = candidate_manifest["manifest_version"]

    if candidate_version < previous_version:
        raise StateValidationError("manifest_version cannot decrease")

    if candidate_version == previous_version:
        previous_hash = compute_manifest_hash(previous_manifest)
        candidate_hash = compute_manifest_hash(candidate_manifest)
        if previous_hash != candidate_hash:
            raise StateValidationError(
                "manifest changed without manifest_version bump"
            )

    protected_top_level_keys = set(previous.keys()) | set(candidate.keys())
    protected_top_level_keys.discard("manifest")

    for key in protected_top_level_keys:
        if key in MUTABLE_TOP_LEVEL_FIELDS:
            continue
        if previous.get(key) != candidate.get(key):
            raise StateValidationError(
                f"top-level field '{key}' is immutable outside dispatcher control"
            )


__all__ = [
    "CANONICAL_PHASES",
    "MUTABLE_TOP_LEVEL_FIELDS",
    "REQUIRED_MANIFEST_FIELDS",
    "REQUIRED_TOP_LEVEL_FIELDS",
    "StateValidationError",
    "assert_runtime_mutation_only",
    "build_manifest_payload_for_hash",
    "compute_manifest_hash",
    "load_state",
    "validate_manifest",
    "validate_state",
]

