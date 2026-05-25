from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


TOOL_NAME = "apply_audio_loudness_report"
TOOL_VERSION = "1.0.0"

LOUDNESS_MISSING_REQUIREMENT = "loudness validation"
LOUDNESS_BLOCKER = "loudness validation was not performed"


class ApplyAudioLoudnessReportError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_path(value: str | Path) -> Path:
    path = Path(value)

    if path.is_absolute():
        try:
            return path.resolve().relative_to(REPO_ROOT)
        except ValueError as exc:
            raise ApplyAudioLoudnessReportError(f"path is outside repo root: {path}") from exc

    return path


def read_json_file(path: Path) -> dict[str, Any]:
    absolute_path = REPO_ROOT / path

    try:
        payload = json.loads(absolute_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ApplyAudioLoudnessReportError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ApplyAudioLoudnessReportError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise ApplyAudioLoudnessReportError(f"JSON file must contain an object: {path}")

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
        raise ApplyAudioLoudnessReportError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ApplyAudioLoudnessReportError(f"{field_name} must be non-empty")

    return normalized


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ApplyAudioLoudnessReportError(f"{field_name} must be boolean")

    return value


def require_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise ApplyAudioLoudnessReportError(f"{field_name} must be integer")

    return value


def remove_item(values: Any, item_to_remove: str, field_name: str) -> list[str]:
    if not isinstance(values, list):
        raise ApplyAudioLoudnessReportError(f"{field_name} must be a list")

    result: list[str] = []

    for item in values:
        if not isinstance(item, str):
            raise ApplyAudioLoudnessReportError(f"{field_name} items must be strings")

        if item.strip().lower() == item_to_remove.lower():
            continue

        result.append(item)

    return result


def validate_loudness_report(
    audio_render: dict[str, Any],
    loudness_report: dict[str, Any],
    loudness_report_path: Path,
) -> None:
    audio_project_id = require_non_empty_string(
        audio_render.get("project_id"),
        "audio_render.project_id",
    )
    report_project_id = require_non_empty_string(
        loudness_report.get("project_id"),
        "audio_loudness_report.project_id",
    )

    if audio_project_id != report_project_id:
        raise ApplyAudioLoudnessReportError(
            f"project_id mismatch: audio_render={audio_project_id}, report={report_project_id}"
        )

    verdict = require_non_empty_string(
        loudness_report.get("verdict"),
        "audio_loudness_report.verdict",
    )
    if verdict != "PASS":
        raise ApplyAudioLoudnessReportError(
            f"audio_loudness_report.verdict must be PASS, got {verdict}"
        )

    loudness_validated = require_bool(
        loudness_report.get("loudness_validated"),
        "audio_loudness_report.loudness_validated",
    )
    if loudness_validated is not True:
        raise ApplyAudioLoudnessReportError(
            "audio_loudness_report.loudness_validated must be true"
        )

    fail_count = require_int(
        loudness_report.get("fail_count"),
        "audio_loudness_report.fail_count",
    )
    if fail_count != 0:
        raise ApplyAudioLoudnessReportError(
            f"audio_loudness_report.fail_count must be 0, got {fail_count}"
        )

    report_segment_count = require_int(
        loudness_report.get("segment_count"),
        "audio_loudness_report.segment_count",
    )
    audio_segment_count = require_int(
        audio_render.get("segment_count"),
        "audio_render.segment_count",
    )

    if report_segment_count != audio_segment_count:
        raise ApplyAudioLoudnessReportError(
            f"segment_count mismatch: audio_render={audio_segment_count}, report={report_segment_count}"
        )

    source_audio_render_path = require_non_empty_string(
        loudness_report.get("source_audio_render_path"),
        "audio_loudness_report.source_audio_render_path",
    )

    expected_source = str(audio_render_path)
    if source_audio_render_path != expected_source:
        raise ApplyAudioLoudnessReportError(
            f"audio_loudness_report.source_audio_render_path mismatch: {source_audio_render_path}"
        )

    if not (REPO_ROOT / loudness_report_path).exists():
        raise ApplyAudioLoudnessReportError(
            f"audio_loudness_report file missing: {loudness_report_path}"
        )


def apply_loudness_report(
    state_path: Path,
    audio_render_path: Path,
    loudness_report_path: Path,
) -> dict[str, Any]:
    state = read_json_file(state_path)
    audio_render = read_json_file(audio_render_path)
    loudness_report = read_json_file(loudness_report_path)

    validate_loudness_report(audio_render, loudness_report, loudness_report_path)

    rendered_segment_count = require_int(
        audio_render.get("rendered_segment_count"),
        "audio_render.rendered_segment_count",
    )
    segment_count = require_int(
        audio_render.get("segment_count"),
        "audio_render.segment_count",
    )
    failed_segment_count = require_int(
        audio_render.get("failed_segment_count"),
        "audio_render.failed_segment_count",
    )
    duration_validated = require_bool(
        audio_render.get("duration_validated"),
        "audio_render.duration_validated",
    )

    all_segments_rendered = (
        rendered_segment_count == segment_count
        and failed_segment_count == 0
    )

    if not all_segments_rendered:
        raise ApplyAudioLoudnessReportError(
            "audio_render must have all segments rendered before applying loudness report"
        )

    if duration_validated is not True:
        raise ApplyAudioLoudnessReportError(
            "audio_render.duration_validated must be true before applying loudness report"
        )

    now = utc_now_iso()

    audio_render["loudness_validated"] = True
    audio_render["audio_loudness_report_path"] = str(loudness_report_path)
    audio_render["missing_requirements"] = remove_item(
        audio_render.get("missing_requirements"),
        LOUDNESS_MISSING_REQUIREMENT,
        "audio_render.missing_requirements",
    )
    audio_render["blockers"] = remove_item(
        audio_render.get("blockers"),
        LOUDNESS_BLOCKER,
        "audio_render.blockers",
    )

    no_missing_requirements = len(audio_render["missing_requirements"]) == 0
    no_blockers = len(audio_render["blockers"]) == 0

    audio_ready = (
        all_segments_rendered
        and duration_validated is True
        and audio_render["loudness_validated"] is True
        and no_missing_requirements
        and no_blockers
    )

    audio_render["audio_ready"] = audio_ready
    audio_render["audio_status"] = "ready" if audio_ready else "partial"
    audio_render["updated_at"] = now
    audio_render["loudness_applied_by"] = TOOL_NAME
    audio_render["loudness_applied_tool_version"] = TOOL_VERSION

    artifacts = state.get("artifacts", {})
    if not isinstance(artifacts, dict):
        raise ApplyAudioLoudnessReportError("PROJECT_STATE.artifacts must be an object")

    artifacts["audio_render_path"] = str(audio_render_path)
    artifacts["audio_loudness_report_path"] = str(loudness_report_path)

    state["artifacts"] = artifacts
    state["updated_at"] = now

    write_json_atomic(audio_render_path, audio_render)
    write_json_atomic(state_path, state)

    return {
        "status": "APPLY_AUDIO_LOUDNESS_REPORT_OK",
        "project_id": audio_render["project_id"],
        "audio_render_path": str(audio_render_path),
        "audio_loudness_report_path": str(loudness_report_path),
        "audio_status": audio_render["audio_status"],
        "audio_ready": audio_render["audio_ready"],
        "loudness_validated": audio_render["loudness_validated"],
        "missing_requirements": audio_render["missing_requirements"],
        "blockers": audio_render["blockers"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply FlowMind audio loudness report")
    parser.add_argument(
        "--state",
        required=True,
        help="Path to PROJECT_STATE.json relative to repo root",
    )
    parser.add_argument(
        "--audio-render",
        required=True,
        help="Path to audio_render.json relative to repo root",
    )
    parser.add_argument(
        "--loudness-report",
        required=True,
        help="Path to audio_loudness_report.json relative to repo root",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = apply_loudness_report(
            state_path=repo_path(args.state),
            audio_render_path=repo_path(args.audio_render),
            loudness_report_path=repo_path(args.loudness_report),
        )
    except (ApplyAudioLoudnessReportError, OSError) as exc:
        print(f"[APPLY_AUDIO_LOUDNESS_REPORT][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
