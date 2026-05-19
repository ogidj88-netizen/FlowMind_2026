from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.state_store import save_state_with_disk_guard
from engine.state_validator import StateValidationError, load_state

EXECUTOR_NAME = "qa_executor"
EXECUTOR_VERSION = "1.0.4"

FORBIDDEN_MARKERS = (
    "PLACEHOLDER",
    "STUB",
    "STUBBED",
    "DO_NOT_PUBLISH",
    "TODO",
    "FAKE_OUTPUT",
    "LOREM IPSUM",
    "TEST ONLY",
    "DUMMY",
    "MOCK",
)

BLOCKER_MISSING_REQUIREMENTS = {
    "assets_resolved": "resolved media asset files",
    "asset_licenses_cleared": "cleared asset licenses",
    "assembly_render_ready": "final render executor",
    "audio_ready": "rendered audio files",
    "final_video_exists": "final video file",
    "upload_readiness": "upload readiness approval",
}


class QaExecutorError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise QaExecutorError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise QaExecutorError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise QaExecutorError(f"{field_name} must be an integer")

    if value <= 0:
        raise QaExecutorError(f"{field_name} must be > 0")

    return value


def require_non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise QaExecutorError(f"{field_name} must be an integer")

    if value < 0:
        raise QaExecutorError(f"{field_name} must be >= 0")

    return value


def require_positive_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise QaExecutorError(f"{field_name} must be a number")

    if not isinstance(value, int | float):
        raise QaExecutorError(f"{field_name} must be a number")

    normalized = float(value)
    if normalized <= 0:
        raise QaExecutorError(f"{field_name} must be > 0")

    return normalized


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise QaExecutorError(f"{field_name} must be boolean")

    return value


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise QaExecutorError(f"Text file not found: {path}") from exc


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise QaExecutorError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise QaExecutorError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise QaExecutorError(f"JSON file must contain an object: {path}")

    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(path)


def fail_if_forbidden_markers(value: str, source_name: str) -> None:
    upper_value = value.upper()
    hits = [marker for marker in FORBIDDEN_MARKERS if marker in upper_value]
    if hits:
        raise QaExecutorError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def validate_artifact_text(path: Path, source_name: str) -> None:
    content = read_text_file(path)
    if not content.strip():
        raise QaExecutorError(f"{source_name} is empty")
    fail_if_forbidden_markers(content, source_name)


def make_check(
    check_id: str,
    name: str,
    status: str,
    severity: str,
    detail: str,
) -> dict[str, str]:
    allowed_statuses = {"PASS", "WARN", "BLOCKED", "FAIL"}
    allowed_severities = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    if status not in allowed_statuses:
        raise QaExecutorError(f"unsupported check status: {status}")

    if severity not in allowed_severities:
        raise QaExecutorError(f"unsupported check severity: {severity}")

    return {
        "check_id": check_id,
        "name": name,
        "status": status,
        "severity": severity,
        "detail": detail,
    }


def validate_script_qa(script_qa: dict[str, Any]) -> dict[str, str]:
    verdict = script_qa.get("verdict")
    if verdict != "PASS":
        raise QaExecutorError("QA executor requires script_qa.verdict=PASS")

    return make_check(
        "script_qa_passed",
        "Script QA passed",
        "PASS",
        "HIGH",
        "script_qa.verdict=PASS",
    )


def validate_scenes(scenes_payload: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    scene_count = require_positive_int(
        scenes_payload.get("scene_count"),
        "scenes.scene_count",
    )

    scenes = scenes_payload.get("scenes")
    if not isinstance(scenes, list):
        raise QaExecutorError("scenes.scenes must be a list")

    if scene_count != len(scenes):
        raise QaExecutorError(
            f"scene_count mismatch: scene_count={scene_count}, actual={len(scenes)}"
        )

    if scene_count < 6:
        raise QaExecutorError(f"scene_count below minimum: {scene_count}")

    required_fields = {
        "scene_id",
        "order",
        "voiceover_text",
        "visual_intent",
        "on_screen_text",
        "asset_type",
        "estimated_duration_sec",
        "production_notes",
    }

    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            raise QaExecutorError(f"scene index {index} must be an object")

        missing = sorted(required_fields - set(scene.keys()))
        if missing:
            raise QaExecutorError(
                f"scene index {index} missing fields: {', '.join(missing)}"
            )

        require_non_empty_string(scene["scene_id"], f"scene[{index}].scene_id")
        require_positive_int(scene["order"], f"scene[{index}].order")
        require_non_empty_string(scene["voiceover_text"], f"scene[{index}].voiceover_text")
        require_non_empty_string(scene["visual_intent"], f"scene[{index}].visual_intent")
        require_non_empty_string(scene["on_screen_text"], f"scene[{index}].on_screen_text")
        require_non_empty_string(scene["asset_type"], f"scene[{index}].asset_type")
        require_positive_int(
            scene["estimated_duration_sec"],
            f"scene[{index}].estimated_duration_sec",
        )
        require_non_empty_string(scene["production_notes"], f"scene[{index}].production_notes")

        fail_if_forbidden_markers(
            json.dumps(scene, ensure_ascii=False),
            f"scene[{index}]",
        )

    return scenes, make_check(
        "scenes_valid",
        "Scenes artifact valid",
        "PASS",
        "HIGH",
        f"scene_count={scene_count}",
    )


def validate_assets(
    assets_payload: dict[str, Any],
    expected_scene_count: int,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    asset_count = require_positive_int(
        assets_payload.get("asset_count"),
        "resolved_assets.asset_count",
    )

    assets = assets_payload.get("assets")
    if not isinstance(assets, list):
        raise QaExecutorError("resolved_assets.assets must be a list")

    if asset_count != len(assets):
        raise QaExecutorError(
            f"asset_count mismatch: asset_count={asset_count}, actual={len(assets)}"
        )

    if asset_count < expected_scene_count:
        raise QaExecutorError(
            f"asset_count below scene_count: asset_count={asset_count}, scene_count={expected_scene_count}"
        )

    required_fields = {
        "asset_id",
        "scene_id",
        "order",
        "asset_type",
        "asset_query",
        "visual_intent",
        "usage_role",
        "required",
        "provider_status",
        "resolution_status",
        "local_path",
        "source_provider",
        "source_url",
        "license_status",
        "license_note",
        "production_notes",
    }

    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            raise QaExecutorError(f"asset index {index} must be an object")

        missing = sorted(required_fields - set(asset.keys()))
        if missing:
            raise QaExecutorError(
                f"asset index {index} missing fields: {', '.join(missing)}"
            )

        require_non_empty_string(asset["asset_id"], f"asset[{index}].asset_id")
        require_non_empty_string(asset["scene_id"], f"asset[{index}].scene_id")
        require_positive_int(asset["order"], f"asset[{index}].order")
        require_non_empty_string(asset["asset_type"], f"asset[{index}].asset_type")
        require_non_empty_string(asset["asset_query"], f"asset[{index}].asset_query")
        require_non_empty_string(asset["visual_intent"], f"asset[{index}].visual_intent")
        require_non_empty_string(asset["usage_role"], f"asset[{index}].usage_role")
        require_non_empty_string(asset["provider_status"], f"asset[{index}].provider_status")
        require_non_empty_string(asset["resolution_status"], f"asset[{index}].resolution_status")
        require_non_empty_string(asset["license_status"], f"asset[{index}].license_status")
        require_non_empty_string(asset["production_notes"], f"asset[{index}].production_notes")

        fail_if_forbidden_markers(
            json.dumps(asset, ensure_ascii=False),
            f"asset[{index}]",
        )

    assets_resolved = all(
        asset.get("provider_status") == "resolved"
        and asset.get("resolution_status") == "ready"
        and isinstance(asset.get("local_path"), str)
        and bool(asset.get("local_path", "").strip())
        and Path(str(asset.get("local_path"))).exists()
        for asset in assets
    )

    licenses_cleared = all(asset.get("license_status") == "cleared" for asset in assets)

    checks = [
        make_check(
            "assets_valid",
            "Resolved assets artifact valid",
            "PASS",
            "HIGH",
            f"asset_count={asset_count}",
        ),
        make_check(
            "assets_resolved",
            "Assets resolved",
            "PASS" if assets_resolved else "BLOCKED",
            "CRITICAL",
            "all required assets have local media files" if assets_resolved else "resolved local media files are missing",
        ),
        make_check(
            "asset_licenses_cleared",
            "Asset licenses cleared",
            "PASS" if licenses_cleared else "BLOCKED",
            "CRITICAL",
            "all asset licenses cleared" if licenses_cleared else "asset licenses are not cleared",
        ),
    ]

    return assets, checks


def validate_assembly_plan(
    assembly_plan: dict[str, Any],
    expected_scene_count: int,
) -> tuple[list[dict[str, Any]], list[dict[str, str]], list[str]]:
    timeline = assembly_plan.get("timeline")
    if not isinstance(timeline, list):
        raise QaExecutorError("assembly_plan.timeline must be a list")

    if not timeline:
        raise QaExecutorError("assembly_plan.timeline must not be empty")

    scene_count = require_positive_int(
        assembly_plan.get("scene_count"),
        "assembly_plan.scene_count",
    )

    if scene_count != expected_scene_count:
        raise QaExecutorError(
            f"assembly scene_count mismatch: assembly={scene_count}, scenes={expected_scene_count}"
        )

    if scene_count != len(timeline):
        raise QaExecutorError(
            f"assembly timeline mismatch: scene_count={scene_count}, timeline={len(timeline)}"
        )

    render_ready = assembly_plan.get("render_ready")
    if not isinstance(render_ready, bool):
        raise QaExecutorError("assembly_plan.render_ready must be boolean")

    missing_requirements = assembly_plan.get("missing_requirements", [])
    if not isinstance(missing_requirements, list):
        raise QaExecutorError("assembly_plan.missing_requirements must be a list")

    checks = [
        make_check(
            "assembly_plan_valid",
            "Assembly plan valid",
            "PASS",
            "HIGH",
            f"timeline_items={len(timeline)}",
        ),
        make_check(
            "assembly_render_ready",
            "Assembly render ready",
            "PASS" if render_ready else "BLOCKED",
            "CRITICAL",
            "assembly render_ready=true" if render_ready else "assembly render_ready=false",
        ),
    ]

    fail_if_forbidden_markers(
        json.dumps(assembly_plan, ensure_ascii=False),
        "assembly_plan",
    )

    return timeline, checks, [str(item) for item in missing_requirements]


def validate_audio_plan(
    audio_plan: dict[str, Any],
    expected_segment_count: int,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    audio_segments = audio_plan.get("audio_segments")
    if not isinstance(audio_segments, list):
        raise QaExecutorError("audio_plan.audio_segments must be a list")

    if not audio_segments:
        raise QaExecutorError("audio_plan.audio_segments must not be empty")

    if len(audio_segments) != expected_segment_count:
        raise QaExecutorError(
            f"audio plan segment count mismatch: audio_plan={len(audio_segments)}, expected={expected_segment_count}"
        )

    for index, segment in enumerate(audio_segments, start=1):
        if not isinstance(segment, dict):
            raise QaExecutorError(f"audio plan segment index {index} must be an object")

        require_non_empty_string(segment.get("segment_id"), f"audio_plan_segment[{index}].segment_id")
        require_non_empty_string(segment.get("source_scene_id"), f"audio_plan_segment[{index}].source_scene_id")
        require_positive_int(segment.get("order"), f"audio_plan_segment[{index}].order")
        require_non_empty_string(segment.get("voiceover_text"), f"audio_plan_segment[{index}].voiceover_text")
        require_positive_int(
            segment.get("estimated_word_count"),
            f"audio_plan_segment[{index}].estimated_word_count",
        )
        require_positive_int(
            segment.get("estimated_duration_sec"),
            f"audio_plan_segment[{index}].estimated_duration_sec",
        )
        require_non_empty_string(segment.get("tts_status"), f"audio_plan_segment[{index}].tts_status")

        fail_if_forbidden_markers(
            json.dumps(segment, ensure_ascii=False),
            f"audio_plan_segment[{index}]",
        )

    checks = [
        make_check(
            "audio_plan_valid",
            "Audio plan valid",
            "PASS",
            "HIGH",
            f"audio_segments={len(audio_segments)}",
        ),
    ]

    fail_if_forbidden_markers(
        json.dumps(audio_plan, ensure_ascii=False),
        "audio_plan",
    )

    return audio_segments, checks


def validate_audio_render(
    audio_render: dict[str, Any],
    expected_segment_count: int,
) -> tuple[list[dict[str, Any]], list[dict[str, str]], list[str]]:
    audio_status = require_non_empty_string(
        audio_render.get("audio_status"),
        "audio_render.audio_status",
    )
    audio_ready = require_bool(audio_render.get("audio_ready"), "audio_render.audio_ready")
    duration_validated = require_bool(
        audio_render.get("duration_validated"),
        "audio_render.duration_validated",
    )
    loudness_validated = require_bool(
        audio_render.get("loudness_validated"),
        "audio_render.loudness_validated",
    )

    rendered_segment_count = require_non_negative_int(
        audio_render.get("rendered_segment_count"),
        "audio_render.rendered_segment_count",
    )
    segment_count = require_positive_int(
        audio_render.get("segment_count"),
        "audio_render.segment_count",
    )
    failed_segment_count = require_non_negative_int(
        audio_render.get("failed_segment_count"),
        "audio_render.failed_segment_count",
    )

    missing_requirements = audio_render.get("missing_requirements", [])
    if not isinstance(missing_requirements, list):
        raise QaExecutorError("audio_render.missing_requirements must be a list")

    blockers = audio_render.get("blockers", [])
    if not isinstance(blockers, list):
        raise QaExecutorError("audio_render.blockers must be a list")

    segments = audio_render.get("segments")
    if not isinstance(segments, list):
        raise QaExecutorError("audio_render.segments must be a list")

    if segment_count != expected_segment_count:
        raise QaExecutorError(
            f"audio_render.segment_count mismatch: audio_render={segment_count}, expected={expected_segment_count}"
        )

    if len(segments) != segment_count:
        raise QaExecutorError(
            f"audio_render.segments length mismatch: segment_count={segment_count}, actual={len(segments)}"
        )

    audio_files_ready = True

    for index, segment in enumerate(segments, start=1):
        if not isinstance(segment, dict):
            raise QaExecutorError(f"audio render segment index {index} must be an object")

        segment_id = require_non_empty_string(
            segment.get("segment_id"),
            f"audio_render_segment[{index}].segment_id",
        )
        require_non_empty_string(
            segment.get("source_scene_id"),
            f"audio_render_segment[{index}].source_scene_id",
        )
        require_positive_int(segment.get("order"), f"audio_render_segment[{index}].order")
        audio_path = require_non_empty_string(
            segment.get("audio_path"),
            f"audio_render_segment[{index}].audio_path",
        )
        require_positive_number(
            segment.get("duration_sec"),
            f"audio_render_segment[{index}].duration_sec",
        )
        tts_status = require_non_empty_string(
            segment.get("tts_status"),
            f"audio_render_segment[{index}].tts_status",
        )
        provider_status = require_non_empty_string(
            segment.get("provider_status"),
            f"audio_render_segment[{index}].provider_status",
        )
        segment_duration_validated = require_bool(
            segment.get("duration_validated"),
            f"audio_render_segment[{index}].duration_validated",
        )

        if tts_status != "rendered":
            audio_files_ready = False

        if provider_status != "rendered":
            audio_files_ready = False

        if segment_duration_validated is not True:
            audio_files_ready = False

        if not Path(audio_path).exists():
            audio_files_ready = False

        fail_if_forbidden_markers(
            json.dumps(segment, ensure_ascii=False),
            f"audio_render_segment[{index}]",
        )

        if not segment_id.startswith("AUDIO_SEGMENT_"):
            raise QaExecutorError(f"unexpected audio segment id format: {segment_id}")

    audio_ready_pass = (
        audio_status == "ready"
        and audio_ready is True
        and duration_validated is True
        and loudness_validated is True
        and rendered_segment_count == segment_count
        and failed_segment_count == 0
        and not missing_requirements
        and not blockers
        and audio_files_ready
    )

    checks = [
        make_check(
            "audio_render_valid",
            "Audio render artifact valid",
            "PASS",
            "HIGH",
            f"rendered_segments={rendered_segment_count}/{segment_count}",
        ),
        make_check(
            "audio_ready",
            "Audio ready",
            "PASS" if audio_ready_pass else "BLOCKED",
            "CRITICAL",
            "audio_render ready with rendered files"
            if audio_ready_pass
            else "audio_render is not ready",
        ),
    ]

    fail_if_forbidden_markers(
        json.dumps(audio_render, ensure_ascii=False),
        "audio_render",
    )

    return segments, checks, [str(item) for item in missing_requirements]


def compute_readiness_score(checks: list[dict[str, str]], final_video_exists: bool) -> int:
    base_score = 0

    for check in checks:
        if check["status"] == "PASS":
            base_score += 8
        elif check["status"] == "WARN":
            base_score += 3

    score = min(base_score, 100)

    blocked_ids = {
        check["check_id"]
        for check in checks
        if check["status"] in {"BLOCKED", "FAIL"}
    }

    if "final_video_exists" in blocked_ids:
        score = min(score, 79)

    if "audio_ready" in blocked_ids:
        score = min(score, 59)

    if "assembly_render_ready" in blocked_ids:
        score = min(score, 59)

    if not final_video_exists:
        score = min(score, 59)

    return max(0, score)


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []

    for value in values:
        normalized = str(value).strip()
        if not normalized:
            continue

        key = normalized.lower()
        if key in seen:
            continue

        seen.add(key)
        unique.append(normalized)

    return unique


def build_missing_requirements(
    checks: list[dict[str, str]],
    blockers: list[str],
    assembly_missing: list[str],
    audio_missing: list[str],
) -> list[str]:
    passed_check_ids = {
        check["check_id"]
        for check in checks
        if check["status"] == "PASS"
    }

    closed_requirements = {
        BLOCKER_MISSING_REQUIREMENTS[check_id]
        for check_id in passed_check_ids
        if check_id in BLOCKER_MISSING_REQUIREMENTS
    }

    raw_missing_requirements = (
        [
            BLOCKER_MISSING_REQUIREMENTS[blocker]
            for blocker in blockers
            if blocker in BLOCKER_MISSING_REQUIREMENTS
        ]
        + assembly_missing
        + audio_missing
    )

    return unique_strings(
        [
            requirement
            for requirement in raw_missing_requirements
            if requirement not in closed_requirements
        ]
    )


def run_qa_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "QA":
        raise QaExecutorError("QA executor may run only when phase is QA")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]
    artifacts = state.get("artifacts", {})

    if not isinstance(artifacts, dict):
        raise QaExecutorError("artifacts must be an object")

    niche = require_non_empty_string(manifest.get("niche"), "manifest.niche")
    audience = require_non_empty_string(manifest.get("audience"), "manifest.audience")
    content_language = require_non_empty_string(
        manifest.get("content_language"),
        "manifest.content_language",
    )
    primary_platform = require_non_empty_string(
        manifest.get("primary_platform"),
        "manifest.primary_platform",
    )
    topic = require_non_empty_string(manifest.get("topic"), "manifest.topic")
    working_title = require_non_empty_string(
        manifest.get("working_title"),
        "manifest.working_title",
    )
    target_duration_sec = require_positive_int(
        manifest.get("target_duration_sec"),
        "manifest.target_duration_sec",
    )

    script_path = Path(
        require_non_empty_string(artifacts.get("script_path"), "artifacts.script_path")
    )
    script_meta_path = Path(
        require_non_empty_string(artifacts.get("script_meta_path"), "artifacts.script_meta_path")
    )
    script_qa_path = Path(
        require_non_empty_string(artifacts.get("script_qa_path"), "artifacts.script_qa_path")
    )
    scenes_path = Path(
        require_non_empty_string(artifacts.get("scenes_path"), "artifacts.scenes_path")
    )
    planning_assets_path = Path(
        require_non_empty_string(artifacts.get("assets_path"), "artifacts.assets_path")
    )
    resolved_assets_path = Path(
        require_non_empty_string(
            artifacts.get("resolved_assets_path"),
            "artifacts.resolved_assets_path",
        )
    )
    assembly_plan_path = Path(
        require_non_empty_string(
            artifacts.get("assembly_plan_path"),
            "artifacts.assembly_plan_path",
        )
    )
    audio_plan_path = Path(
        require_non_empty_string(artifacts.get("audio_plan_path"), "artifacts.audio_plan_path")
    )
    audio_render_path = Path(
        require_non_empty_string(artifacts.get("audio_render_path"), "artifacts.audio_render_path")
    )

    validate_artifact_text(script_path, "script.txt")
    script_meta = read_json_file(script_meta_path)
    script_qa = read_json_file(script_qa_path)
    scenes_payload = read_json_file(scenes_path)
    assets_payload = read_json_file(resolved_assets_path)
    assembly_plan = read_json_file(assembly_plan_path)
    audio_plan = read_json_file(audio_plan_path)
    audio_render = read_json_file(audio_render_path)

    fail_if_forbidden_markers(json.dumps(script_meta, ensure_ascii=False), "script_meta")
    fail_if_forbidden_markers(json.dumps(script_qa, ensure_ascii=False), "script_qa")
    fail_if_forbidden_markers(json.dumps(scenes_payload, ensure_ascii=False), "scenes")
    fail_if_forbidden_markers(json.dumps(assets_payload, ensure_ascii=False), "resolved_assets")

    checks: list[dict[str, str]] = []

    checks.append(validate_script_qa(script_qa))

    scenes, scenes_check = validate_scenes(scenes_payload)
    checks.append(scenes_check)

    assets, asset_checks = validate_assets(assets_payload, len(scenes))
    checks.extend(asset_checks)

    timeline, assembly_checks, assembly_missing = validate_assembly_plan(
        assembly_plan,
        len(scenes),
    )
    checks.extend(assembly_checks)

    audio_segments, audio_plan_checks = validate_audio_plan(
        audio_plan,
        len(timeline),
    )
    checks.extend(audio_plan_checks)

    audio_render_segments, audio_render_checks, audio_missing = validate_audio_render(
        audio_render,
        len(timeline),
    )
    checks.extend(audio_render_checks)

    final_video_path = artifacts.get("final_video_path")
    final_video_exists = (
        isinstance(final_video_path, str)
        and bool(final_video_path.strip())
        and os.path.exists(final_video_path)
    )

    checks.append(
        make_check(
            "final_video_exists",
            "Final video exists",
            "PASS" if final_video_exists else "BLOCKED",
            "CRITICAL",
            "final video file exists" if final_video_exists else "final video file is missing",
        )
    )

    upload_ready = (
        all(check["status"] == "PASS" for check in checks)
        and state.get("qa_passed") is True
        and state.get("approved_for_upload") is True
    )

    checks.append(
        make_check(
            "upload_readiness",
            "Upload readiness",
            "PASS" if upload_ready else "BLOCKED",
            "CRITICAL",
            "project is upload-ready" if upload_ready else "project is not upload-ready",
        )
    )

    blockers = [
        check["check_id"]
        for check in checks
        if check["status"] in {"BLOCKED", "FAIL"}
    ]

    missing_requirements = build_missing_requirements(
        checks,
        blockers,
        assembly_missing,
        audio_missing,
    )

    readiness_score = compute_readiness_score(checks, final_video_exists)

    verdict = "BLOCKED"
    qa_passed = False
    approved_for_upload = False

    now = utc_now_iso()
    qa_report_path = state_path.parent / "qa" / "qa_report.json"

    qa_report = {
        "project_id": project_id,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "source_phase": state["phase"],
        "topic": topic,
        "working_title": working_title,
        "niche": niche,
        "audience": audience,
        "content_language": content_language,
        "primary_platform": primary_platform,
        "target_duration_sec": target_duration_sec,
        "verdict": verdict,
        "qa_passed": qa_passed,
        "approved_for_upload": approved_for_upload,
        "readiness_score": readiness_score,
        "checks": checks,
        "blockers": blockers,
        "warnings": [],
        "missing_requirements": missing_requirements,
        "artifact_summary": {
            "script_path": str(script_path),
            "script_meta_path": str(script_meta_path),
            "script_qa_path": str(script_qa_path),
            "scenes_path": str(scenes_path),
            "planning_assets_path": str(planning_assets_path),
            "resolved_assets_path": str(resolved_assets_path),
            "assembly_plan_path": str(assembly_plan_path),
            "audio_plan_path": str(audio_plan_path),
            "audio_render_path": str(audio_render_path),
            "scene_count": len(scenes),
            "asset_count": len(assets),
            "timeline_count": len(timeline),
            "audio_plan_segment_count": len(audio_segments),
            "audio_render_segment_count": len(audio_render_segments),
        },
        "created_at": now,
    }

    serialized = json.dumps(qa_report, ensure_ascii=False)
    fail_if_forbidden_markers(serialized, "qa_report")

    write_json_atomic(qa_report_path, qa_report)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["qa_report_path"] = str(qa_report_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["qa_passed"] = False
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "QA_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "qa_report_path": str(qa_report_path),
        "verdict": verdict,
        "qa_passed": False,
        "readiness_score": readiness_score,
        "blockers": blockers,
        "missing_requirements": missing_requirements,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind canonical QA executor v1")
    parser.add_argument(
        "--state",
        required=True,
        help="Path to canonical PROJECT_STATE.json",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = run_qa_executor(Path(args.state))
    except (QaExecutorError, StateValidationError, OSError) as exc:
        print(f"[QA_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
