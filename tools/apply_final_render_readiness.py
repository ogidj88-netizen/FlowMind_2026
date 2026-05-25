from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


TOOL_NAME = "apply_final_render_readiness"
TOOL_VERSION = "1.0.0"

FINAL_RENDER_REQUIREMENT = "final render executor"


class ApplyFinalRenderReadinessError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_path(value: str | Path) -> Path:
    path = Path(value)

    if path.is_absolute():
        try:
            return path.resolve().relative_to(REPO_ROOT)
        except ValueError as exc:
            raise ApplyFinalRenderReadinessError(f"path is outside repo root: {path}") from exc

    return path


def absolute_repo_path(path: Path) -> Path:
    return REPO_ROOT / repo_path(path)


def read_json_file(path: Path) -> dict[str, Any]:
    absolute_path = absolute_repo_path(path)

    try:
        payload = json.loads(absolute_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ApplyFinalRenderReadinessError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ApplyFinalRenderReadinessError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise ApplyFinalRenderReadinessError(f"JSON file must contain an object: {path}")

    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    absolute_path = absolute_repo_path(path)
    absolute_path.parent.mkdir(parents=True, exist_ok=True)

    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    temp_path = absolute_path.with_suffix(absolute_path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(absolute_path)


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ApplyFinalRenderReadinessError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ApplyFinalRenderReadinessError(f"{field_name} must be non-empty")

    return normalized


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ApplyFinalRenderReadinessError(f"{field_name} must be boolean")

    return value


def require_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise ApplyFinalRenderReadinessError(f"{field_name} must be integer")

    return value


def require_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise ApplyFinalRenderReadinessError(f"{field_name} must be number")

    if not isinstance(value, int | float):
        raise ApplyFinalRenderReadinessError(f"{field_name} must be number")

    return float(value)


def require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ApplyFinalRenderReadinessError(f"{field_name} must be a list")

    return value


def ensure_existing_non_empty_file(path: Path, field_name: str) -> None:
    absolute_path = absolute_repo_path(path)

    if not absolute_path.exists():
        raise ApplyFinalRenderReadinessError(f"{field_name} does not exist: {path}")

    if not absolute_path.is_file():
        raise ApplyFinalRenderReadinessError(f"{field_name} must be a file: {path}")

    if absolute_path.stat().st_size <= 0:
        raise ApplyFinalRenderReadinessError(f"{field_name} is empty: {path}")


def remove_final_render_requirement(values: Any) -> list[str]:
    items = require_list(values, "assembly_plan.missing_requirements")
    result: list[str] = []

    for item in items:
        if not isinstance(item, str):
            raise ApplyFinalRenderReadinessError("assembly_plan.missing_requirements items must be strings")

        if item.strip().lower() == FINAL_RENDER_REQUIREMENT:
            continue

        result.append(item)

    return result


def validate_project_ids(
    state: dict[str, Any],
    assembly_plan: dict[str, Any],
    final_render_report: dict[str, Any],
) -> str:
    state_project_id = require_non_empty_string(state.get("project_id"), "PROJECT_STATE.project_id")
    assembly_project_id = require_non_empty_string(assembly_plan.get("project_id"), "assembly_plan.project_id")
    report_project_id = require_non_empty_string(
        final_render_report.get("project_id"),
        "final_render_report.project_id",
    )

    if state_project_id != assembly_project_id or state_project_id != report_project_id:
        raise ApplyFinalRenderReadinessError(
            "project_id mismatch: "
            f"state={state_project_id}, assembly={assembly_project_id}, final_render_report={report_project_id}"
        )

    return state_project_id


def validate_state_has_final_artifacts(
    state: dict[str, Any],
    final_render_report_path: Path,
) -> tuple[Path, Path]:
    phase = require_non_empty_string(state.get("phase"), "PROJECT_STATE.phase")
    if phase != "QA":
        raise ApplyFinalRenderReadinessError(f"PROJECT_STATE.phase must be QA, got {phase}")

    artifacts = state.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ApplyFinalRenderReadinessError("PROJECT_STATE.artifacts must be an object")

    final_video_path = repo_path(
        require_non_empty_string(
            artifacts.get("final_video_path"),
            "PROJECT_STATE.artifacts.final_video_path",
        )
    )

    state_report_path = repo_path(
        require_non_empty_string(
            artifacts.get("final_render_report_path"),
            "PROJECT_STATE.artifacts.final_render_report_path",
        )
    )

    if state_report_path != final_render_report_path:
        raise ApplyFinalRenderReadinessError(
            f"PROJECT_STATE final_render_report_path mismatch: state={state_report_path}, expected={final_render_report_path}"
        )

    ensure_existing_non_empty_file(final_video_path, "PROJECT_STATE.artifacts.final_video_path")
    ensure_existing_non_empty_file(state_report_path, "PROJECT_STATE.artifacts.final_render_report_path")

    return final_video_path, state_report_path


def validate_final_render_report(
    final_render_report: dict[str, Any],
    final_video_path: Path,
) -> None:
    status = require_non_empty_string(final_render_report.get("status"), "final_render_report.status")
    verdict = require_non_empty_string(final_render_report.get("verdict"), "final_render_report.verdict")
    report_video_path = repo_path(
        require_non_empty_string(
            final_render_report.get("final_video_path"),
            "final_render_report.final_video_path",
        )
    )

    final_video_exists = require_bool(
        final_render_report.get("final_video_exists"),
        "final_render_report.final_video_exists",
    )
    final_video_size_bytes = require_int(
        final_render_report.get("final_video_size_bytes"),
        "final_render_report.final_video_size_bytes",
    )
    final_duration_sec = require_number(
        final_render_report.get("final_duration_sec"),
        "final_render_report.final_duration_sec",
    )
    failed_scene_count = require_int(
        final_render_report.get("failed_scene_count"),
        "final_render_report.failed_scene_count",
    )
    blockers = require_list(final_render_report.get("blockers"), "final_render_report.blockers")

    if status != "FINAL_RENDER_OK":
        raise ApplyFinalRenderReadinessError(f"final_render_report.status must be FINAL_RENDER_OK, got {status}")

    if verdict != "PASS":
        raise ApplyFinalRenderReadinessError(f"final_render_report.verdict must be PASS, got {verdict}")

    if report_video_path != final_video_path:
        raise ApplyFinalRenderReadinessError(
            f"final_video_path mismatch: state={final_video_path}, report={report_video_path}"
        )

    if final_video_exists is not True:
        raise ApplyFinalRenderReadinessError("final_render_report.final_video_exists must be true")

    if final_video_size_bytes <= 0:
        raise ApplyFinalRenderReadinessError("final_render_report.final_video_size_bytes must be > 0")

    if final_duration_sec <= 0:
        raise ApplyFinalRenderReadinessError("final_render_report.final_duration_sec must be > 0")

    if failed_scene_count != 0:
        raise ApplyFinalRenderReadinessError(
            f"final_render_report.failed_scene_count must be 0, got {failed_scene_count}"
        )

    if blockers:
        raise ApplyFinalRenderReadinessError(f"final_render_report.blockers must be empty, got {blockers}")

    ensure_existing_non_empty_file(final_video_path, "final_video_path")


def validate_assembly_before_sync(assembly_plan: dict[str, Any]) -> None:
    assets_ready = require_bool(assembly_plan.get("assets_ready"), "assembly_plan.assets_ready")
    audio_ready = require_bool(assembly_plan.get("audio_ready"), "assembly_plan.audio_ready")
    render_ready = require_bool(assembly_plan.get("render_ready"), "assembly_plan.render_ready")
    missing_requirements = require_list(
        assembly_plan.get("missing_requirements"),
        "assembly_plan.missing_requirements",
    )

    if assets_ready is not True:
        raise ApplyFinalRenderReadinessError("assembly_plan.assets_ready must be true")

    if audio_ready is not True:
        raise ApplyFinalRenderReadinessError("assembly_plan.audio_ready must be true")

    if render_ready is not False:
        raise ApplyFinalRenderReadinessError("assembly_plan.render_ready must be false before sync")

    if missing_requirements != [FINAL_RENDER_REQUIREMENT]:
        raise ApplyFinalRenderReadinessError(
            f"assembly_plan.missing_requirements must be ['{FINAL_RENDER_REQUIREMENT}'], got {missing_requirements}"
        )


def apply_final_render_readiness(
    state_path: Path,
    assembly_plan_path: Path,
    final_render_report_path: Path,
) -> dict[str, Any]:
    state_path = repo_path(state_path)
    assembly_plan_path = repo_path(assembly_plan_path)
    final_render_report_path = repo_path(final_render_report_path)

    state = read_json_file(state_path)
    assembly_plan = read_json_file(assembly_plan_path)
    final_render_report = read_json_file(final_render_report_path)

    project_id = validate_project_ids(
        state=state,
        assembly_plan=assembly_plan,
        final_render_report=final_render_report,
    )

    final_video_path, _ = validate_state_has_final_artifacts(
        state=state,
        final_render_report_path=final_render_report_path,
    )

    validate_final_render_report(
        final_render_report=final_render_report,
        final_video_path=final_video_path,
    )
    validate_assembly_before_sync(assembly_plan)

    now = utc_now_iso()

    remaining_missing_requirements = remove_final_render_requirement(
        assembly_plan.get("missing_requirements")
    )

    assembly_plan["render_ready"] = True
    assembly_plan["missing_requirements"] = remaining_missing_requirements
    assembly_plan["readiness_status"] = "render_ready"
    assembly_plan["source_final_render_report_path"] = str(final_render_report_path)
    assembly_plan["source_final_video_path"] = str(final_video_path)
    assembly_plan["updated_at"] = now
    assembly_plan["final_render_readiness_applied_by"] = TOOL_NAME
    assembly_plan["final_render_readiness_applied_tool_version"] = TOOL_VERSION

    state["updated_at"] = now

    write_json_atomic(assembly_plan_path, assembly_plan)
    write_json_atomic(state_path, state)

    return {
        "status": "APPLY_FINAL_RENDER_READINESS_OK",
        "project_id": project_id,
        "assembly_plan_path": str(assembly_plan_path),
        "final_render_report_path": str(final_render_report_path),
        "final_video_path": str(final_video_path),
        "render_ready": assembly_plan["render_ready"],
        "readiness_status": assembly_plan["readiness_status"],
        "missing_requirements": assembly_plan["missing_requirements"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply FlowMind final render readiness")
    parser.add_argument(
        "--state",
        required=True,
        help="Path to PROJECT_STATE.json relative to repo root",
    )
    parser.add_argument(
        "--assembly-plan",
        required=True,
        help="Path to assembly_plan.json relative to repo root",
    )
    parser.add_argument(
        "--final-render-report",
        required=True,
        help="Path to final_render_report.json relative to repo root",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = apply_final_render_readiness(
            state_path=repo_path(args.state),
            assembly_plan_path=repo_path(args.assembly_plan),
            final_render_report_path=repo_path(args.final_render_report),
        )
    except (ApplyFinalRenderReadinessError, OSError) as exc:
        print(f"[APPLY_FINAL_RENDER_READINESS][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
