from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_STATE_PATH = Path("projects/P2026_TEST_001/PROJECT_STATE.json")
DEFAULT_ASSEMBLY_PLAN_PATH = Path("projects/P2026_TEST_001/assembly/assembly_plan.json")
DEFAULT_RESOLVED_ASSETS_PATH = Path("projects/P2026_TEST_001/assets/resolved_assets.json")
DEFAULT_AUDIO_RENDER_PATH = Path("projects/P2026_TEST_001/audio/audio_render.json")

TOOL_NAME = "apply_assembly_readiness"
TOOL_VERSION = "1.0.0"

RESOLVED_MEDIA_REQUIREMENT = "resolved media asset files"
CLEARED_LICENSE_REQUIREMENT = "cleared asset licenses"
AUDIO_ARTIFACT_REQUIREMENT = "audio artifact"
FINAL_RENDER_EXECUTOR_REQUIREMENT = "final render executor"


class ApplyAssemblyReadinessError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_path(value: str | Path) -> Path:
    path = Path(value)

    if path.is_absolute():
        try:
            return path.resolve().relative_to(REPO_ROOT)
        except ValueError as exc:
            raise ApplyAssemblyReadinessError(f"path is outside repo root: {path}") from exc

    return path


def read_json_file(path: Path) -> dict[str, Any]:
    absolute_path = REPO_ROOT / path

    try:
        payload = json.loads(absolute_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ApplyAssemblyReadinessError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ApplyAssemblyReadinessError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise ApplyAssemblyReadinessError(f"JSON file must contain an object: {path}")

    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    absolute_path = REPO_ROOT / path
    absolute_path.parent.mkdir(parents=True, exist_ok=True)

    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    temp_path = absolute_path.with_suffix(absolute_path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(absolute_path)


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ApplyAssemblyReadinessError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ApplyAssemblyReadinessError(f"{field_name} must be non-empty")

    return normalized


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ApplyAssemblyReadinessError(f"{field_name} must be boolean")

    return value


def require_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise ApplyAssemblyReadinessError(f"{field_name} must be integer")

    return value


def require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ApplyAssemblyReadinessError(f"{field_name} must be a list")

    return value


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        normalized = str(value).strip()
        if not normalized:
            continue

        key = normalized.lower()
        if key in seen:
            continue

        seen.add(key)
        result.append(normalized)

    return result


def remove_requirements(values: Any, requirements_to_remove: set[str]) -> list[str]:
    items = require_list(values, "assembly_plan.missing_requirements")
    result: list[str] = []

    normalized_remove = {item.lower() for item in requirements_to_remove}

    for item in items:
        if not isinstance(item, str):
            raise ApplyAssemblyReadinessError("assembly_plan.missing_requirements items must be strings")

        if item.strip().lower() in normalized_remove:
            continue

        result.append(item)

    return unique_strings(result)


def validate_project_ids(
    state: dict[str, Any],
    assembly_plan: dict[str, Any],
    resolved_assets: dict[str, Any],
    audio_render: dict[str, Any],
) -> str:
    state_project_id = require_non_empty_string(state.get("project_id"), "PROJECT_STATE.project_id")
    assembly_project_id = require_non_empty_string(assembly_plan.get("project_id"), "assembly_plan.project_id")
    assets_project_id = require_non_empty_string(resolved_assets.get("project_id"), "resolved_assets.project_id")
    audio_project_id = require_non_empty_string(audio_render.get("project_id"), "audio_render.project_id")

    ids = {
        state_project_id,
        assembly_project_id,
        assets_project_id,
        audio_project_id,
    }

    if len(ids) != 1:
        raise ApplyAssemblyReadinessError(
            "project_id mismatch: "
            f"state={state_project_id}, assembly={assembly_project_id}, "
            f"assets={assets_project_id}, audio={audio_project_id}"
        )

    return state_project_id


def validate_assets_ready(resolved_assets: dict[str, Any]) -> None:
    asset_count = require_int(resolved_assets.get("asset_count"), "resolved_assets.asset_count")
    resolved_count = require_int(resolved_assets.get("resolved_count"), "resolved_assets.resolved_count")
    blocked_count = require_int(resolved_assets.get("blocked_count"), "resolved_assets.blocked_count")
    license_cleared_count = require_int(
        resolved_assets.get("license_cleared_count"),
        "resolved_assets.license_cleared_count",
    )

    blockers = require_list(resolved_assets.get("blockers"), "resolved_assets.blockers")
    warnings = require_list(resolved_assets.get("warnings"), "resolved_assets.warnings")
    assets = require_list(resolved_assets.get("assets"), "resolved_assets.assets")

    if asset_count <= 0:
        raise ApplyAssemblyReadinessError("resolved_assets.asset_count must be > 0")

    if len(assets) != asset_count:
        raise ApplyAssemblyReadinessError(
            f"resolved_assets asset count mismatch: asset_count={asset_count}, actual={len(assets)}"
        )

    if resolved_count != asset_count:
        raise ApplyAssemblyReadinessError(
            f"not all assets resolved: resolved_count={resolved_count}, asset_count={asset_count}"
        )

    if license_cleared_count != asset_count:
        raise ApplyAssemblyReadinessError(
            f"not all asset licenses cleared: license_cleared_count={license_cleared_count}, asset_count={asset_count}"
        )

    if blocked_count != 0:
        raise ApplyAssemblyReadinessError(f"resolved_assets.blocked_count must be 0, got {blocked_count}")

    if blockers:
        raise ApplyAssemblyReadinessError(f"resolved_assets.blockers must be empty, got {blockers}")

    if warnings:
        raise ApplyAssemblyReadinessError(f"resolved_assets.warnings must be empty, got {warnings}")

    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            raise ApplyAssemblyReadinessError(f"resolved_assets.assets[{index}] must be an object")

        asset_id = require_non_empty_string(asset.get("asset_id"), f"asset[{index}].asset_id")
        provider_status = require_non_empty_string(
            asset.get("provider_status"),
            f"asset[{index}].provider_status",
        )
        license_status = require_non_empty_string(
            asset.get("license_status"),
            f"asset[{index}].license_status",
        )
        resolution_status = require_non_empty_string(
            asset.get("resolution_status"),
            f"asset[{index}].resolution_status",
        )
        local_path = require_non_empty_string(asset.get("local_path"), f"asset[{index}].local_path")

        if provider_status != "resolved":
            raise ApplyAssemblyReadinessError(f"{asset_id} provider_status must be resolved")

        if license_status != "cleared":
            raise ApplyAssemblyReadinessError(f"{asset_id} license_status must be cleared")

        if resolution_status != "ready":
            raise ApplyAssemblyReadinessError(f"{asset_id} resolution_status must be ready")

        if not (REPO_ROOT / repo_path(local_path)).exists():
            raise ApplyAssemblyReadinessError(f"{asset_id} local_path does not exist: {local_path}")


def validate_audio_ready(audio_render: dict[str, Any]) -> None:
    audio_ready = require_bool(audio_render.get("audio_ready"), "audio_render.audio_ready")
    audio_status = require_non_empty_string(audio_render.get("audio_status"), "audio_render.audio_status")
    loudness_validated = require_bool(
        audio_render.get("loudness_validated"),
        "audio_render.loudness_validated",
    )
    duration_validated = require_bool(
        audio_render.get("duration_validated"),
        "audio_render.duration_validated",
    )
    rendered_segment_count = require_int(
        audio_render.get("rendered_segment_count"),
        "audio_render.rendered_segment_count",
    )
    segment_count = require_int(audio_render.get("segment_count"), "audio_render.segment_count")
    failed_segment_count = require_int(
        audio_render.get("failed_segment_count"),
        "audio_render.failed_segment_count",
    )

    missing_requirements = require_list(
        audio_render.get("missing_requirements"),
        "audio_render.missing_requirements",
    )
    blockers = require_list(audio_render.get("blockers"), "audio_render.blockers")
    audio_loudness_report_path = require_non_empty_string(
        audio_render.get("audio_loudness_report_path"),
        "audio_render.audio_loudness_report_path",
    )

    if audio_status != "ready":
        raise ApplyAssemblyReadinessError(f"audio_render.audio_status must be ready, got {audio_status}")

    if audio_ready is not True:
        raise ApplyAssemblyReadinessError("audio_render.audio_ready must be true")

    if duration_validated is not True:
        raise ApplyAssemblyReadinessError("audio_render.duration_validated must be true")

    if loudness_validated is not True:
        raise ApplyAssemblyReadinessError("audio_render.loudness_validated must be true")

    if rendered_segment_count != segment_count:
        raise ApplyAssemblyReadinessError(
            f"audio segment render mismatch: rendered={rendered_segment_count}, segment_count={segment_count}"
        )

    if failed_segment_count != 0:
        raise ApplyAssemblyReadinessError(
            f"audio_render.failed_segment_count must be 0, got {failed_segment_count}"
        )

    if missing_requirements:
        raise ApplyAssemblyReadinessError(
            f"audio_render.missing_requirements must be empty, got {missing_requirements}"
        )

    if blockers:
        raise ApplyAssemblyReadinessError(f"audio_render.blockers must be empty, got {blockers}")

    if not (REPO_ROOT / repo_path(audio_loudness_report_path)).exists():
        raise ApplyAssemblyReadinessError(
            f"audio_loudness_report_path does not exist: {audio_loudness_report_path}"
        )


def validate_assembly_shape(assembly_plan: dict[str, Any]) -> None:
    timeline = require_list(assembly_plan.get("timeline"), "assembly_plan.timeline")
    scene_count = require_int(assembly_plan.get("scene_count"), "assembly_plan.scene_count")

    if scene_count <= 0:
        raise ApplyAssemblyReadinessError("assembly_plan.scene_count must be > 0")

    if len(timeline) != scene_count:
        raise ApplyAssemblyReadinessError(
            f"assembly timeline mismatch: scene_count={scene_count}, actual={len(timeline)}"
        )


def apply_assembly_readiness(
    state_path: Path,
    assembly_plan_path: Path,
    resolved_assets_path: Path,
    audio_render_path: Path,
) -> dict[str, Any]:
    state = read_json_file(state_path)
    assembly_plan = read_json_file(assembly_plan_path)
    resolved_assets = read_json_file(resolved_assets_path)
    audio_render = read_json_file(audio_render_path)

    project_id = validate_project_ids(
        state=state,
        assembly_plan=assembly_plan,
        resolved_assets=resolved_assets,
        audio_render=audio_render,
    )

    validate_assembly_shape(assembly_plan)
    validate_assets_ready(resolved_assets)
    validate_audio_ready(audio_render)

    now = utc_now_iso()

    remaining_missing_requirements = remove_requirements(
        assembly_plan.get("missing_requirements"),
        {
            RESOLVED_MEDIA_REQUIREMENT,
            CLEARED_LICENSE_REQUIREMENT,
            AUDIO_ARTIFACT_REQUIREMENT,
        },
    )

    if FINAL_RENDER_EXECUTOR_REQUIREMENT not in remaining_missing_requirements:
        remaining_missing_requirements.append(FINAL_RENDER_EXECUTOR_REQUIREMENT)

    remaining_missing_requirements = unique_strings(remaining_missing_requirements)

    assembly_plan["missing_requirements"] = remaining_missing_requirements
    assembly_plan["assets_ready"] = True
    assembly_plan["audio_ready"] = True
    assembly_plan["render_ready"] = False
    assembly_plan["readiness_status"] = "blocked_by_final_render_executor"
    assembly_plan["source_resolved_assets_path"] = str(resolved_assets_path)
    assembly_plan["source_audio_render_path"] = str(audio_render_path)
    assembly_plan["updated_at"] = now
    assembly_plan["readiness_applied_by"] = TOOL_NAME
    assembly_plan["readiness_applied_tool_version"] = TOOL_VERSION

    artifacts = state.get("artifacts", {})
    if not isinstance(artifacts, dict):
        raise ApplyAssemblyReadinessError("PROJECT_STATE.artifacts must be an object")

    artifacts["assembly_plan_path"] = str(assembly_plan_path)
    artifacts["resolved_assets_path"] = str(resolved_assets_path)
    artifacts["audio_render_path"] = str(audio_render_path)

    state["artifacts"] = artifacts
    state["updated_at"] = now

    write_json_atomic(assembly_plan_path, assembly_plan)
    write_json_atomic(state_path, state)

    return {
        "status": "APPLY_ASSEMBLY_READINESS_OK",
        "project_id": project_id,
        "assembly_plan_path": str(assembly_plan_path),
        "assets_ready": assembly_plan["assets_ready"],
        "audio_ready": assembly_plan["audio_ready"],
        "render_ready": assembly_plan["render_ready"],
        "readiness_status": assembly_plan["readiness_status"],
        "missing_requirements": assembly_plan["missing_requirements"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply FlowMind assembly readiness")
    parser.add_argument(
        "--state",
        default=str(DEFAULT_STATE_PATH),
        help="Path to PROJECT_STATE.json relative to repo root",
    )
    parser.add_argument(
        "--assembly-plan",
        default=str(DEFAULT_ASSEMBLY_PLAN_PATH),
        help="Path to assembly_plan.json relative to repo root",
    )
    parser.add_argument(
        "--resolved-assets",
        default=str(DEFAULT_RESOLVED_ASSETS_PATH),
        help="Path to resolved_assets.json relative to repo root",
    )
    parser.add_argument(
        "--audio-render",
        default=str(DEFAULT_AUDIO_RENDER_PATH),
        help="Path to audio_render.json relative to repo root",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = apply_assembly_readiness(
            state_path=repo_path(args.state),
            assembly_plan_path=repo_path(args.assembly_plan),
            resolved_assets_path=repo_path(args.resolved_assets),
            audio_render_path=repo_path(args.audio_render),
        )
    except (ApplyAssemblyReadinessError, OSError) as exc:
        print(f"[APPLY_ASSEMBLY_READINESS][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
