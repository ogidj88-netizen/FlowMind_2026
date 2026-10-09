from __future__ import annotations

import argparse
import json
import shutil
import subprocess
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

EXECUTOR_NAME = "final_render_executor"
EXECUTOR_VERSION = "2.0.2"

FINAL_RENDER_DIRNAME = "final_render"
SEGMENTS_DIRNAME = "segments"
VISUAL_SEGMENTS_DIRNAME = "visual_segments"
TMP_DIRNAME = "tmp"
FINAL_VIDEO_FILENAME = "final_video.mp4"
FINAL_RENDER_REPORT_FILENAME = "final_render_report.json"

WIDTH = 1920
HEIGHT = 1080
FPS = 30
AUDIO_SAMPLE_RATE = 48000
AUDIO_CHANNELS = 2

MAX_VISUAL_SEGMENT_DURATION_DRIFT_SEC = 0.50
MAX_SCENE_DURATION_DRIFT_SEC = 0.50
MAX_FINAL_DURATION_DRIFT_SEC = 1.50

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv"}
ALLOWED_VISUAL_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

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


class FinalRenderExecutorError(RuntimeError):
    pass


def print_progress(*, stage: str, completed: int, total: int, detail: str = "") -> None:
    if total <= 0:
        raise FinalRenderExecutorError("progress total must be > 0")
    bounded_completed = max(0, min(completed, total))
    width = 28
    filled = int(width * bounded_completed / total)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(round(100 * bounded_completed / total))
    suffix = f" | {detail}" if detail else ""
    print(
        f"\r[FINAL RENDER] {stage:<9} [{bar}] {percent:3d}% "
        f"({bounded_completed}/{total}){suffix}",
        end="\n" if bounded_completed == total else "",
        flush=True,
    )


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(REPO_ROOT)
        except ValueError as exc:
            raise FinalRenderExecutorError(f"path is outside repo root: {path}") from exc
    return path


def absolute_repo_path(value: str | Path) -> Path:
    return REPO_ROOT / repo_path(value)


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise FinalRenderExecutorError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise FinalRenderExecutorError(f"{field_name} must be non-empty")
    return normalized


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise FinalRenderExecutorError(f"{field_name} must be boolean")
    return value


def require_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise FinalRenderExecutorError(f"{field_name} must be integer")
    return value


def require_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FinalRenderExecutorError(f"{field_name} must be number")
    return float(value)


def require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise FinalRenderExecutorError(f"{field_name} must be a list")
    return value


def read_json_file(path: Path) -> dict[str, Any]:
    absolute_path = absolute_repo_path(path)
    try:
        payload = json.loads(absolute_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FinalRenderExecutorError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FinalRenderExecutorError(f"Invalid JSON file: {path}") from exc
    if not isinstance(payload, dict):
        raise FinalRenderExecutorError(f"JSON file must contain an object: {path}")
    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    absolute_path = absolute_repo_path(path)
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    fail_if_forbidden_markers(serialized, str(path))
    temp_path = absolute_path.with_suffix(absolute_path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(absolute_path)


def fail_if_forbidden_markers(value: str, source_name: str) -> None:
    upper_value = value.upper()
    hits = [marker for marker in FORBIDDEN_MARKERS if marker in upper_value]
    if hits:
        raise FinalRenderExecutorError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise FinalRenderExecutorError(f"required runtime tool missing: {name}")


def ensure_existing_file(path: Path, field_name: str) -> None:
    absolute_path = absolute_repo_path(path)
    if not absolute_path.exists():
        raise FinalRenderExecutorError(f"{field_name} does not exist: {path}")
    if not absolute_path.is_file():
        raise FinalRenderExecutorError(f"{field_name} must be a file: {path}")
    if absolute_path.stat().st_size <= 0:
        raise FinalRenderExecutorError(f"{field_name} is empty: {path}")


def run_command(command: list[str], context: str) -> None:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        stderr_tail = completed.stderr[-3000:] if completed.stderr else ""
        stdout_tail = completed.stdout[-1000:] if completed.stdout else ""
        raise FinalRenderExecutorError(
            f"{context} failed with exit={completed.returncode}\n"
            f"STDERR:\n{stderr_tail}\n"
            f"STDOUT:\n{stdout_tail}"
        )


def ffprobe_json(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of",
        "json",
        str(absolute_repo_path(path)),
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise FinalRenderExecutorError(
            f"ffprobe failed for {path}: {completed.stderr.strip()}"
        )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise FinalRenderExecutorError(f"ffprobe JSON parse failed for {path}") from exc
    if not isinstance(payload, dict):
        raise FinalRenderExecutorError(f"ffprobe payload must be object for {path}")
    return payload


def probe_duration_sec(path: Path) -> float:
    payload = ffprobe_json(path)
    try:
        duration = float(payload["format"]["duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise FinalRenderExecutorError(f"duration missing from ffprobe for {path}") from exc
    if duration <= 0:
        raise FinalRenderExecutorError(f"duration must be positive for {path}")
    return round(duration, 3)


def probe_stream_types(path: Path) -> set[str]:
    payload = ffprobe_json(path)
    streams = payload.get("streams")
    if not isinstance(streams, list):
        raise FinalRenderExecutorError(f"ffprobe streams must be list for {path}")
    result: set[str] = set()
    for stream in streams:
        if isinstance(stream, dict) and isinstance(stream.get("codec_type"), str):
            result.add(stream["codec_type"])
    return result


def validate_final_video(path: Path) -> tuple[float, int]:
    ensure_existing_file(path, "final_video")
    duration = probe_duration_sec(path)
    stream_types = probe_stream_types(path)
    if "video" not in stream_types:
        raise FinalRenderExecutorError("final video has no video stream")
    if "audio" not in stream_types:
        raise FinalRenderExecutorError("final video has no audio stream")
    return duration, absolute_repo_path(path).stat().st_size


def validate_state(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    phase = require_non_empty_string(state.get("phase"), "PROJECT_STATE.phase")
    if phase != "ASSEMBLY":
        raise FinalRenderExecutorError(
            f"PROJECT_STATE.phase must be ASSEMBLY before final render, got {phase}"
        )

    project_id = require_non_empty_string(state.get("project_id"), "PROJECT_STATE.project_id")
    artifacts = state.get("artifacts")
    if not isinstance(artifacts, dict):
        raise FinalRenderExecutorError("PROJECT_STATE.artifacts must be an object")

    required_keys = (
        "assembly_plan_path",
        "resolved_assets_path",
        "audio_render_path",
        "audio_loudness_report_path",
    )
    for key in required_keys:
        value = require_non_empty_string(artifacts.get(key), f"PROJECT_STATE.artifacts.{key}")
        ensure_existing_file(repo_path(value), f"PROJECT_STATE.artifacts.{key}")

    return project_id, artifacts


def validate_project_ids(
    project_id: str,
    assembly_plan: dict[str, Any],
    resolved_assets: dict[str, Any],
    audio_render: dict[str, Any],
    loudness_report: dict[str, Any],
) -> None:
    values = {
        "assembly_plan": require_non_empty_string(assembly_plan.get("project_id"), "assembly_plan.project_id"),
        "resolved_assets": require_non_empty_string(resolved_assets.get("project_id"), "resolved_assets.project_id"),
        "audio_render": require_non_empty_string(audio_render.get("project_id"), "audio_render.project_id"),
        "loudness_report": require_non_empty_string(loudness_report.get("project_id"), "audio_loudness_report.project_id"),
    }
    for source_name, value in values.items():
        if value != project_id:
            raise FinalRenderExecutorError(
                f"project_id mismatch: PROJECT_STATE={project_id}, {source_name}={value}"
            )


def validate_assembly_plan(assembly_plan: dict[str, Any]) -> list[dict[str, Any]]:
    if assembly_plan.get("executor_version") != "2.0.0":
        raise FinalRenderExecutorError("assembly_plan.executor_version must be 2.0.0")
    if assembly_plan.get("timing_source") != "actual_canonical_audio":
        raise FinalRenderExecutorError("assembly_plan.timing_source must be actual_canonical_audio")
    if assembly_plan.get("media_source") != "resolved_timed_media":
        raise FinalRenderExecutorError("assembly_plan.media_source must be resolved_timed_media")

    assets_ready = require_bool(assembly_plan.get("assets_ready"), "assembly_plan.assets_ready")
    audio_ready = require_bool(assembly_plan.get("audio_ready"), "assembly_plan.audio_ready")
    render_ready = require_bool(assembly_plan.get("render_ready"), "assembly_plan.render_ready")
    if assets_ready is not True:
        raise FinalRenderExecutorError("assembly_plan.assets_ready must be true")
    if audio_ready is not True:
        raise FinalRenderExecutorError("assembly_plan.audio_ready must be true")
    if render_ready is not False:
        raise FinalRenderExecutorError("assembly_plan.render_ready must be false before final render")

    missing_requirements = require_list(
        assembly_plan.get("missing_requirements"),
        "assembly_plan.missing_requirements",
    )
    if missing_requirements != ["final render executor"]:
        raise FinalRenderExecutorError(
            f"assembly_plan.missing_requirements must be ['final render executor'], got {missing_requirements}"
        )

    timeline = require_list(assembly_plan.get("timeline"), "assembly_plan.timeline")
    scene_count = require_int(assembly_plan.get("scene_count"), "assembly_plan.scene_count")
    beat_count = require_int(assembly_plan.get("beat_count"), "assembly_plan.beat_count")
    visual_segment_count = require_int(
        assembly_plan.get("visual_segment_count"),
        "assembly_plan.visual_segment_count",
    )

    if scene_count <= 0 or beat_count <= 0 or visual_segment_count <= 0:
        raise FinalRenderExecutorError("assembly counts must be > 0")
    if len(timeline) != scene_count:
        raise FinalRenderExecutorError(
            f"assembly scene count mismatch: scene_count={scene_count}, timeline={len(timeline)}"
        )
    if visual_segment_count != beat_count:
        raise FinalRenderExecutorError(
            f"assembly visual_segment_count must equal beat_count: {visual_segment_count}!={beat_count}"
        )

    normalized: list[dict[str, Any]] = []
    seen_orders: set[int] = set()
    total_visual_segments = 0

    for index, item in enumerate(timeline, start=1):
        if not isinstance(item, dict):
            raise FinalRenderExecutorError(f"timeline[{index}] must be an object")

        timeline_id = require_non_empty_string(item.get("timeline_id"), f"timeline[{index}].timeline_id")
        scene_id = require_non_empty_string(item.get("scene_id"), f"timeline[{index}].scene_id")
        order = require_int(item.get("order"), f"timeline[{index}].order")
        audio_segment_id = require_non_empty_string(
            item.get("audio_segment_id"),
            f"timeline[{index}].audio_segment_id",
        )
        audio_path = repo_path(
            require_non_empty_string(item.get("audio_path"), f"timeline[{index}].audio_path")
        )
        audio_duration_sec = require_number(
            item.get("audio_duration_sec"),
            f"timeline[{index}].audio_duration_sec",
        )
        visual_segments = require_list(
            item.get("visual_segments"),
            f"timeline[{index}].visual_segments",
        )

        if order <= 0:
            raise FinalRenderExecutorError(f"timeline[{index}].order must be > 0")
        if order in seen_orders:
            raise FinalRenderExecutorError(f"duplicate timeline order: {order}")
        seen_orders.add(order)
        if audio_duration_sec <= 0:
            raise FinalRenderExecutorError(f"timeline[{index}].audio_duration_sec must be > 0")
        ensure_existing_file(audio_path, f"timeline[{index}].audio_path")
        if not visual_segments:
            raise FinalRenderExecutorError(f"timeline[{index}].visual_segments must not be empty")

        normalized_segments: list[dict[str, Any]] = []
        previous_scene_end = 0.0

        for segment_index, segment in enumerate(visual_segments, start=1):
            if not isinstance(segment, dict):
                raise FinalRenderExecutorError(
                    f"timeline[{index}].visual_segments[{segment_index}] must be an object"
                )

            segment_id = require_non_empty_string(
                segment.get("segment_id"),
                f"timeline[{index}].visual_segments[{segment_index}].segment_id",
            )
            asset_id = require_non_empty_string(
                segment.get("asset_id"),
                f"{segment_id}.asset_id",
            )
            visual_asset_path = repo_path(
                require_non_empty_string(
                    segment.get("visual_asset_path"),
                    f"{segment_id}.visual_asset_path",
                )
            )
            asset_type = require_non_empty_string(segment.get("asset_type"), f"{segment_id}.asset_type")
            duration_sec = require_number(segment.get("duration_sec"), f"{segment_id}.duration_sec")
            scene_start_sec = require_number(segment.get("scene_start_sec"), f"{segment_id}.scene_start_sec")
            scene_end_sec = require_number(segment.get("scene_end_sec"), f"{segment_id}.scene_end_sec")

            if duration_sec <= 0:
                raise FinalRenderExecutorError(f"{segment_id}.duration_sec must be > 0")
            if scene_start_sec < 0 or scene_end_sec <= scene_start_sec:
                raise FinalRenderExecutorError(f"{segment_id} invalid scene timing")
            if abs(scene_start_sec - previous_scene_end) > 0.05:
                raise FinalRenderExecutorError(
                    f"{segment_id} scene timing gap/overlap: start={scene_start_sec}, previous_end={previous_scene_end}"
                )
            if abs((scene_end_sec - scene_start_sec) - duration_sec) > 0.05:
                raise FinalRenderExecutorError(
                    f"{segment_id} duration mismatch: range={scene_end_sec-scene_start_sec}, duration={duration_sec}"
                )

            ensure_existing_file(visual_asset_path, f"{segment_id}.visual_asset_path")
            extension = visual_asset_path.suffix.lower()
            if extension not in ALLOWED_VISUAL_EXTENSIONS:
                raise FinalRenderExecutorError(
                    f"{segment_id} unsupported visual extension: {extension}"
                )

            normalized_segments.append(
                {
                    "segment_id": segment_id,
                    "asset_id": asset_id,
                    "asset_type": asset_type,
                    "visual_asset_path": str(visual_asset_path),
                    "visual_extension": extension,
                    "duration_sec": round(duration_sec, 3),
                    "scene_start_sec": round(scene_start_sec, 3),
                    "scene_end_sec": round(scene_end_sec, 3),
                }
            )
            previous_scene_end = scene_end_sec

        if abs(previous_scene_end - audio_duration_sec) > 0.05:
            raise FinalRenderExecutorError(
                f"{scene_id} visual/audio duration mismatch: visual={previous_scene_end}, audio={audio_duration_sec}"
            )

        total_visual_segments += len(normalized_segments)
        normalized.append(
            {
                "timeline_id": timeline_id,
                "scene_id": scene_id,
                "order": order,
                "audio_segment_id": audio_segment_id,
                "audio_path": str(audio_path),
                "audio_duration_sec": round(audio_duration_sec, 3),
                "visual_segments": normalized_segments,
            }
        )

    if total_visual_segments != visual_segment_count:
        raise FinalRenderExecutorError(
            f"assembly visual segment total mismatch: declared={visual_segment_count}, actual={total_visual_segments}"
        )

    return sorted(normalized, key=lambda value: value["order"])


def validate_resolved_assets(resolved_assets: dict[str, Any]) -> None:
    asset_count = require_int(resolved_assets.get("asset_count"), "resolved_assets.asset_count")
    resolved_count = require_int(resolved_assets.get("resolved_count"), "resolved_assets.resolved_count")
    license_cleared_count = require_int(
        resolved_assets.get("license_cleared_count"),
        "resolved_assets.license_cleared_count",
    )
    blocked_count = require_int(resolved_assets.get("blocked_count"), "resolved_assets.blocked_count")

    if asset_count <= 0:
        raise FinalRenderExecutorError("resolved_assets.asset_count must be > 0")
    if resolved_count != asset_count:
        raise FinalRenderExecutorError("resolved_assets.resolved_count must equal asset_count")
    if license_cleared_count != asset_count:
        raise FinalRenderExecutorError("resolved_assets.license_cleared_count must equal asset_count")
    if blocked_count != 0:
        raise FinalRenderExecutorError("resolved_assets.blocked_count must be 0")

    blockers = require_list(resolved_assets.get("blockers"), "resolved_assets.blockers")
    if blockers:
        raise FinalRenderExecutorError(f"resolved_assets.blockers must be empty, got {blockers}")


def validate_audio_render(audio_render: dict[str, Any]) -> None:
    audio_status = require_non_empty_string(audio_render.get("audio_status"), "audio_render.audio_status")
    audio_ready = require_bool(audio_render.get("audio_ready"), "audio_render.audio_ready")
    duration_validated = require_bool(audio_render.get("duration_validated"), "audio_render.duration_validated")
    loudness_validated = require_bool(audio_render.get("loudness_validated"), "audio_render.loudness_validated")

    if audio_status != "ready":
        raise FinalRenderExecutorError(f"audio_render.audio_status must be ready, got {audio_status}")
    if audio_ready is not True:
        raise FinalRenderExecutorError("audio_render.audio_ready must be true")
    if duration_validated is not True:
        raise FinalRenderExecutorError("audio_render.duration_validated must be true")
    if loudness_validated is not True:
        raise FinalRenderExecutorError("audio_render.loudness_validated must be true")


def validate_loudness_report(
    loudness_report: dict[str, Any],
    project_id: str,
    expected_scene_count: int,
) -> None:
    report_project_id = require_non_empty_string(
        loudness_report.get("project_id"),
        "audio_loudness_report.project_id",
    )
    if report_project_id != project_id:
        raise FinalRenderExecutorError(
            f"audio_loudness_report project_id mismatch: {report_project_id}"
        )

    verdict = require_non_empty_string(loudness_report.get("verdict"), "audio_loudness_report.verdict")
    loudness_validated = require_bool(
        loudness_report.get("loudness_validated"),
        "audio_loudness_report.loudness_validated",
    )
    fail_count = require_int(loudness_report.get("fail_count"), "audio_loudness_report.fail_count")
    segment_count = require_int(loudness_report.get("segment_count"), "audio_loudness_report.segment_count")

    if verdict != "PASS":
        raise FinalRenderExecutorError(f"audio_loudness_report.verdict must be PASS, got {verdict}")
    if loudness_validated is not True:
        raise FinalRenderExecutorError("audio_loudness_report.loudness_validated must be true")
    if fail_count != 0:
        raise FinalRenderExecutorError(f"audio_loudness_report.fail_count must be 0, got {fail_count}")
    if segment_count != expected_scene_count:
        raise FinalRenderExecutorError(
            f"audio_loudness_report.segment_count mismatch: report={segment_count}, assembly={expected_scene_count}"
        )


def render_visual_segment(segment: dict[str, Any], output_path: Path) -> None:
    visual_path = repo_path(segment["visual_asset_path"])
    duration = f"{float(segment['duration_sec']):.3f}"
    extension = str(segment["visual_extension"]).lower()

    video_filter = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,fps={FPS},format=yuv420p"
    )

    output_absolute = absolute_repo_path(output_path)
    output_absolute.parent.mkdir(parents=True, exist_ok=True)

    if extension in IMAGE_EXTENSIONS:
        command = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-t",
            duration,
            "-i",
            str(absolute_repo_path(visual_path)),
            "-an",
            "-vf",
            video_filter,
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(FPS),
            str(output_absolute),
        ]
    elif extension in VIDEO_EXTENSIONS:
        command = [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            str(absolute_repo_path(visual_path)),
            "-t",
            duration,
            "-an",
            "-vf",
            video_filter,
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(FPS),
            str(output_absolute),
        ]
    else:
        raise FinalRenderExecutorError(f"unsupported visual extension: {extension}")

    run_command(command, f"render visual segment {segment['segment_id']}")


def validate_visual_segment(
    path: Path,
    expected_duration_sec: float,
    segment_id: str,
) -> tuple[float, float]:
    ensure_existing_file(path, f"{segment_id}.rendered_path")
    stream_types = probe_stream_types(path)
    if "video" not in stream_types:
        raise FinalRenderExecutorError(f"{segment_id} rendered segment has no video stream")
    if "audio" in stream_types:
        raise FinalRenderExecutorError(f"{segment_id} rendered segment must not contain audio")
    actual = probe_duration_sec(path)
    delta = round(actual - expected_duration_sec, 3)
    if abs(delta) > MAX_VISUAL_SEGMENT_DURATION_DRIFT_SEC:
        raise FinalRenderExecutorError(
            f"{segment_id} duration drift too high: delta={delta}, expected={expected_duration_sec}, actual={actual}"
        )
    return actual, delta


def quote_concat_path(path: Path) -> str:
    value = str(path.resolve())
    escaped = value.replace("'", "'\\''")
    return f"file '{escaped}'"


def write_concat_list(tmp_dir: Path, paths: list[Path], filename: str) -> Path:
    concat_path = tmp_dir / filename
    concat_absolute = absolute_repo_path(concat_path)
    concat_absolute.parent.mkdir(parents=True, exist_ok=True)
    lines = [quote_concat_path(absolute_repo_path(path)) for path in paths]
    concat_absolute.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return concat_path


def concat_video_segments(paths: list[Path], output_path: Path, tmp_dir: Path, filename: str) -> None:
    concat_path = write_concat_list(tmp_dir, paths, filename)
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(absolute_repo_path(concat_path)),
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(absolute_repo_path(output_path)),
    ]
    run_command(command, f"concat {output_path.name}")


def mux_scene_audio(
    visual_track_path: Path,
    audio_path: Path,
    duration_sec: float,
    output_path: Path,
) -> None:
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(absolute_repo_path(visual_track_path)),
        "-i",
        str(absolute_repo_path(audio_path)),
        "-t",
        f"{duration_sec:.3f}",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-ar",
        str(AUDIO_SAMPLE_RATE),
        "-ac",
        str(AUDIO_CHANNELS),
        "-shortest",
        "-movflags",
        "+faststart",
        str(absolute_repo_path(output_path)),
    ]
    run_command(command, f"mux scene audio {output_path.name}")


def validate_scene_video(
    scene_video_path: Path,
    expected_duration_sec: float,
    scene_id: str,
) -> tuple[float, float]:
    ensure_existing_file(scene_video_path, f"{scene_id}.scene_video_path")
    stream_types = probe_stream_types(scene_video_path)
    if "video" not in stream_types:
        raise FinalRenderExecutorError(f"{scene_id} scene segment has no video stream")
    if "audio" not in stream_types:
        raise FinalRenderExecutorError(f"{scene_id} scene segment has no audio stream")

    actual = probe_duration_sec(scene_video_path)
    delta = round(actual - expected_duration_sec, 3)
    if abs(delta) > MAX_SCENE_DURATION_DRIFT_SEC:
        raise FinalRenderExecutorError(
            f"{scene_id} duration drift too high: delta={delta}, expected={expected_duration_sec}, actual={actual}"
        )
    return actual, delta


def build_success_report(
    *,
    project_id: str,
    state_path: Path,
    assembly_plan_path: Path,
    resolved_assets_path: Path,
    audio_render_path: Path,
    final_video_path: Path,
    final_duration_sec: float,
    final_video_size_bytes: int,
    expected_duration_sec: float,
    scene_reports: list[dict[str, Any]],
    visual_segment_count: int,
) -> dict[str, Any]:
    duration_delta_sec = round(final_duration_sec - expected_duration_sec, 3)
    if abs(duration_delta_sec) > MAX_FINAL_DURATION_DRIFT_SEC:
        raise FinalRenderExecutorError(
            f"final video duration drift too high: delta={duration_delta_sec}, "
            f"expected={expected_duration_sec}, actual={final_duration_sec}"
        )

    return {
        "project_id": project_id,
        "renderer": EXECUTOR_NAME,
        "renderer_version": EXECUTOR_VERSION,
        "status": "FINAL_RENDER_OK",
        "verdict": "PASS",
        "final_video_path": str(final_video_path),
        "final_video_exists": True,
        "final_video_size_bytes": final_video_size_bytes,
        "final_duration_sec": final_duration_sec,
        "expected_duration_sec": round(expected_duration_sec, 3),
        "duration_delta_sec": duration_delta_sec,
        "scene_count": len(scene_reports),
        "rendered_scene_count": len(scene_reports),
        "visual_segment_count": visual_segment_count,
        "failed_scene_count": 0,
        "video_profile": {
            "container": "mp4",
            "video_codec": "h264/libx264",
            "audio_codec": "aac",
            "resolution": f"{WIDTH}x{HEIGHT}",
            "fps": FPS,
            "pixel_format": "yuv420p",
            "audio_sample_rate": AUDIO_SAMPLE_RATE,
            "audio_channels": AUDIO_CHANNELS,
        },
        "source_project_state_path": str(state_path),
        "source_assembly_plan_path": str(assembly_plan_path),
        "source_resolved_assets_path": str(resolved_assets_path),
        "source_audio_render_path": str(audio_render_path),
        "scenes": scene_reports,
        "warnings": [],
        "blockers": [],
        "created_at": utc_now_iso(),
    }


def run_final_render_executor(state_path: Path) -> dict[str, Any]:
    require_tool("ffmpeg")
    require_tool("ffprobe")

    state_path = repo_path(state_path)
    state = load_state(absolute_repo_path(state_path))

    project_id, artifacts = validate_state(state)

    assembly_plan_path = repo_path(artifacts["assembly_plan_path"])
    resolved_assets_path = repo_path(artifacts["resolved_assets_path"])
    audio_render_path = repo_path(artifacts["audio_render_path"])
    audio_loudness_report_path = repo_path(artifacts["audio_loudness_report_path"])

    assembly_plan = read_json_file(assembly_plan_path)
    resolved_assets = read_json_file(resolved_assets_path)
    audio_render = read_json_file(audio_render_path)
    loudness_report = read_json_file(audio_loudness_report_path)

    validate_project_ids(
        project_id=project_id,
        assembly_plan=assembly_plan,
        resolved_assets=resolved_assets,
        audio_render=audio_render,
        loudness_report=loudness_report,
    )

    timeline = validate_assembly_plan(assembly_plan)
    validate_resolved_assets(resolved_assets)
    validate_audio_render(audio_render)
    validate_loudness_report(loudness_report, project_id, len(timeline))

    project_dir = state_path.parent
    final_render_dir = project_dir / FINAL_RENDER_DIRNAME
    scenes_dir = final_render_dir / SEGMENTS_DIRNAME
    visual_segments_dir = final_render_dir / VISUAL_SEGMENTS_DIRNAME
    tmp_dir = final_render_dir / TMP_DIRNAME
    final_video_path = final_render_dir / FINAL_VIDEO_FILENAME
    final_render_report_path = final_render_dir / FINAL_RENDER_REPORT_FILENAME

    absolute_repo_path(scenes_dir).mkdir(parents=True, exist_ok=True)
    absolute_repo_path(visual_segments_dir).mkdir(parents=True, exist_ok=True)
    absolute_repo_path(tmp_dir).mkdir(parents=True, exist_ok=True)

    scene_reports: list[dict[str, Any]] = []
    scene_paths: list[Path] = []
    total_visual_segments = 0
    expected_visual_segments = sum(len(scene["visual_segments"]) for scene in timeline)
    total_progress_units = expected_visual_segments + len(timeline) + 2
    completed_progress_units = 0
    print_progress(
        stage="START",
        completed=0,
        total=total_progress_units,
        detail=f"{expected_visual_segments} visual segments, {len(timeline)} scenes",
    )

    for scene in timeline:
        scene_id = scene["scene_id"]
        scene_order = scene["order"]
        scene_visual_paths: list[Path] = []
        visual_segment_reports: list[dict[str, Any]] = []

        for segment_index, segment in enumerate(scene["visual_segments"], start=1):
            segment_output = (
                visual_segments_dir
                / f"{scene_order:03d}_{scene_id}_{segment_index:03d}.mp4"
            )
            render_visual_segment(segment, segment_output)
            actual_duration, duration_delta = validate_visual_segment(
                segment_output,
                float(segment["duration_sec"]),
                segment["segment_id"],
            )
            scene_visual_paths.append(segment_output)
            completed_progress_units += 1
            print_progress(
                stage="VISUALS",
                completed=completed_progress_units,
                total=total_progress_units,
                detail=(
                    f"scene {scene_order}/{len(timeline)} | "
                    f"visual {total_visual_segments + len(scene_visual_paths)}/{expected_visual_segments}"
                ),
            )
            visual_segment_reports.append(
                {
                    "segment_id": segment["segment_id"],
                    "asset_id": segment["asset_id"],
                    "visual_asset_path": segment["visual_asset_path"],
                    "rendered_visual_path": str(segment_output),
                    "expected_duration_sec": segment["duration_sec"],
                    "actual_duration_sec": actual_duration,
                    "duration_delta_sec": duration_delta,
                    "render_status": "rendered",
                }
            )

        total_visual_segments += len(scene_visual_paths)

        scene_tmp_dir = tmp_dir / f"{scene_order:03d}_{scene_id}"
        visual_track_path = scene_tmp_dir / "visual_track.mp4"
        scene_video_path = scenes_dir / f"{scene_order:03d}_{scene_id}.mp4"

        concat_video_segments(
            scene_visual_paths,
            visual_track_path,
            scene_tmp_dir,
            "visual_concat.txt",
        )

        mux_scene_audio(
            visual_track_path=visual_track_path,
            audio_path=repo_path(scene["audio_path"]),
            duration_sec=float(scene["audio_duration_sec"]),
            output_path=scene_video_path,
        )

        scene_duration_sec, scene_duration_delta_sec = validate_scene_video(
            scene_video_path,
            float(scene["audio_duration_sec"]),
            scene_id,
        )

        scene_paths.append(scene_video_path)
        completed_progress_units += 1
        print_progress(
            stage="SCENES",
            completed=completed_progress_units,
            total=total_progress_units,
            detail=f"scene {scene_order}/{len(timeline)} ready",
        )
        scene_reports.append(
            {
                "timeline_id": scene["timeline_id"],
                "scene_id": scene_id,
                "order": scene_order,
                "audio_segment_id": scene["audio_segment_id"],
                "audio_path": scene["audio_path"],
                "audio_duration_sec": scene["audio_duration_sec"],
                "scene_video_path": str(scene_video_path),
                "scene_duration_sec": scene_duration_sec,
                "duration_delta_sec": scene_duration_delta_sec,
                "visual_segment_count": len(scene_visual_paths),
                "visual_segments": visual_segment_reports,
                "render_status": "rendered",
                "error_message": None,
            }
        )

    concat_video_segments(
        scene_paths,
        final_video_path,
        tmp_dir,
        "scene_concat.txt",
    )
    completed_progress_units += 1
    print_progress(
        stage="CONCAT",
        completed=completed_progress_units,
        total=total_progress_units,
        detail="final video assembled",
    )

    final_duration_sec, final_video_size_bytes = validate_final_video(final_video_path)
    expected_duration_sec = sum(float(scene["audio_duration_sec"]) for scene in timeline)

    report = build_success_report(
        project_id=project_id,
        state_path=state_path,
        assembly_plan_path=assembly_plan_path,
        resolved_assets_path=resolved_assets_path,
        audio_render_path=audio_render_path,
        final_video_path=final_video_path,
        final_duration_sec=final_duration_sec,
        final_video_size_bytes=final_video_size_bytes,
        expected_duration_sec=expected_duration_sec,
        scene_reports=scene_reports,
        visual_segment_count=total_visual_segments,
    )

    write_json_atomic(final_render_report_path, report)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["final_video_path"] = str(final_video_path)
    candidate_artifacts["final_render_report_path"] = str(final_render_report_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = utc_now_iso()

    saved_state = save_state_with_disk_guard(absolute_repo_path(state_path), candidate_state)

    completed_progress_units += 1
    print_progress(
        stage="DONE",
        completed=completed_progress_units,
        total=total_progress_units,
        detail="validated and saved",
    )

    return {
        "status": "FINAL_RENDER_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "final_video_path": str(final_video_path),
        "final_render_report_path": str(final_render_report_path),
        "final_video_size_bytes": final_video_size_bytes,
        "final_duration_sec": final_duration_sec,
        "expected_duration_sec": round(expected_duration_sec, 3),
        "scene_count": len(scene_reports),
        "visual_segment_count": total_visual_segments,
        "verdict": report["verdict"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FlowMind timed-visual final render executor"
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Path to canonical PROJECT_STATE.json relative to repo root",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = run_final_render_executor(repo_path(args.state))
    except (FinalRenderExecutorError, StateValidationError, OSError) as exc:
        print(f"[FINAL_RENDER_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
