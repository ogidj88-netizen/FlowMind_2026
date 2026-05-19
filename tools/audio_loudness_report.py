from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_AUDIO_RENDER_PATH = Path("projects/P2026_TEST_001/audio/audio_render.json")
DEFAULT_REPORT_PATH = Path("projects/P2026_TEST_001/audio/audio_loudness_report.json")

TARGET_I = -16.0
TARGET_TP = -1.5
TARGET_LRA = 11.0

MAX_INTEGRATED_DEVIATION = 1.0
MAX_TRUE_PEAK = -0.5
MAX_LRA = 8.0

REPORT_NAME = "audio_loudness_report"
REPORT_VERSION = "1.0.0"


class LoudnessReportError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LoudnessReportError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise LoudnessReportError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise LoudnessReportError(f"JSON file must contain an object: {path}")

    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(path)


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise LoudnessReportError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise LoudnessReportError(f"{field_name} must be non-empty")

    return normalized


def require_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise LoudnessReportError(f"{field_name} must be a number")

    if not isinstance(value, int | float):
        raise LoudnessReportError(f"{field_name} must be a number")

    return float(value)


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(REPO_ROOT)
        except ValueError as exc:
            raise LoudnessReportError(f"path is outside repo root: {value}") from exc

    return path


def run_loudnorm_measurement(audio_path: Path) -> dict[str, float]:
    absolute_path = REPO_ROOT / audio_path

    if not absolute_path.exists():
        raise LoudnessReportError(f"audio file not found: {audio_path}")

    if absolute_path.stat().st_size <= 0:
        raise LoudnessReportError(f"audio file is empty: {audio_path}")

    command = [
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        "-i",
        str(absolute_path),
        "-af",
        f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json",
        "-f",
        "null",
        "-",
    ]

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )

    combined_output = f"{completed.stdout}\n{completed.stderr}"

    if completed.returncode != 0:
        raise LoudnessReportError(
            f"ffmpeg loudnorm failed for {audio_path}: {combined_output[-1000:]}"
        )

    match = re.search(r"\{\s*\"input_i\".*?\}", combined_output, re.DOTALL)
    if not match:
        raise LoudnessReportError(f"loudnorm JSON block not found for {audio_path}")

    try:
        payload = json.loads(match.group(0))
        input_i = float(payload["input_i"])
        input_tp = float(payload["input_tp"])
        input_lra = float(payload["input_lra"])
        input_thresh = float(payload["input_thresh"])
        target_offset = float(payload["target_offset"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise LoudnessReportError(f"loudnorm JSON parse failed for {audio_path}") from exc

    return {
        "input_i": input_i,
        "input_tp": input_tp,
        "input_lra": input_lra,
        "input_thresh": input_thresh,
        "target_offset": target_offset,
    }


def classify_segment(measurement: dict[str, float]) -> tuple[str, list[str]]:
    warnings: list[str] = []

    integrated_deviation = abs(measurement["input_i"] - TARGET_I)

    if integrated_deviation > MAX_INTEGRATED_DEVIATION:
        warnings.append(
            f"integrated loudness deviation too high: {integrated_deviation:.2f} LU"
        )

    if measurement["input_tp"] > MAX_TRUE_PEAK:
        warnings.append(
            f"true peak too high: {measurement['input_tp']:.2f} dBTP"
        )

    if measurement["input_lra"] > MAX_LRA:
        warnings.append(
            f"loudness range too high: {measurement['input_lra']:.2f} LU"
        )

    if warnings:
        return "WARN", warnings

    return "PASS", []


def build_report(audio_render_path: Path) -> dict[str, Any]:
    audio_render = read_json_file(REPO_ROOT / audio_render_path)

    project_id = require_non_empty_string(audio_render.get("project_id"), "audio_render.project_id")
    renderer_version = require_non_empty_string(
        audio_render.get("renderer_version"),
        "audio_render.renderer_version",
    )

    segments = audio_render.get("segments")
    if not isinstance(segments, list):
        raise LoudnessReportError("audio_render.segments must be a list")

    if not segments:
        raise LoudnessReportError("audio_render.segments must not be empty")

    segment_reports: list[dict[str, Any]] = []
    pass_count = 0
    warn_count = 0
    fail_count = 0

    for index, segment in enumerate(segments, start=1):
        if not isinstance(segment, dict):
            raise LoudnessReportError(f"segment index {index} must be an object")

        segment_id = require_non_empty_string(segment.get("segment_id"), f"segment[{index}].segment_id")
        audio_path_value = require_non_empty_string(segment.get("audio_path"), f"segment[{index}].audio_path")
        tts_status = require_non_empty_string(segment.get("tts_status"), f"segment[{index}].tts_status")

        if tts_status != "rendered":
            raise LoudnessReportError(f"{segment_id} tts_status must be rendered")

        duration_sec = require_number(segment.get("duration_sec"), f"segment[{index}].duration_sec")
        audio_path = repo_path(audio_path_value)

        try:
            measurement = run_loudnorm_measurement(audio_path)
            status, warnings = classify_segment(measurement)
        except LoudnessReportError as exc:
            measurement = {}
            status = "FAIL"
            warnings = [str(exc)]

        if status == "PASS":
            pass_count += 1
        elif status == "WARN":
            warn_count += 1
        else:
            fail_count += 1

        segment_reports.append(
            {
                "segment_id": segment_id,
                "audio_path": str(audio_path),
                "duration_sec": duration_sec,
                "status": status,
                "warnings": warnings,
                "measurement": measurement,
            }
        )

    verdict = "PASS" if fail_count == 0 else "FAIL"
    loudness_validated = fail_count == 0

    return {
        "project_id": project_id,
        "report": REPORT_NAME,
        "report_version": REPORT_VERSION,
        "source_audio_render_path": str(audio_render_path),
        "source_audio_renderer_version": renderer_version,
        "created_at": utc_now_iso(),
        "target": {
            "integrated_lufs": TARGET_I,
            "true_peak_dbtp": TARGET_TP,
            "lra_lu": TARGET_LRA,
        },
        "thresholds": {
            "max_integrated_deviation_lu": MAX_INTEGRATED_DEVIATION,
            "max_true_peak_dbtp": MAX_TRUE_PEAK,
            "max_lra_lu": MAX_LRA,
        },
        "segment_count": len(segment_reports),
        "pass_count": pass_count,
        "warn_count": warn_count,
        "fail_count": fail_count,
        "verdict": verdict,
        "loudness_validated": loudness_validated,
        "segments": segment_reports,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind audio loudness report")
    parser.add_argument(
        "--audio-render",
        default=str(DEFAULT_AUDIO_RENDER_PATH),
        help="Path to audio_render.json relative to repo root",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_REPORT_PATH),
        help="Path to write loudness report JSON relative to repo root",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        audio_render_path = repo_path(args.audio_render)
        output_path = repo_path(args.out)
        report = build_report(audio_render_path)
        write_json_atomic(REPO_ROOT / output_path, report)
    except (LoudnessReportError, OSError) as exc:
        print(f"[AUDIO_LOUDNESS_REPORT][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(
        {
            "status": "AUDIO_LOUDNESS_REPORT_OK",
            "project_id": report["project_id"],
            "report_path": str(output_path),
            "verdict": report["verdict"],
            "loudness_validated": report["loudness_validated"],
            "segment_count": report["segment_count"],
            "pass_count": report["pass_count"],
            "warn_count": report["warn_count"],
            "fail_count": report["fail_count"],
        },
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
