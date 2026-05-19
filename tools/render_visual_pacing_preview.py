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
REPO_ROOT = CURRENT_FILE.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

EXECUTOR_NAME = "render_visual_pacing_preview"
EXECUTOR_VERSION = "1.0.2"

DEFAULT_PLAN_PATH = Path("projects/P2026_TEST_001/visual_pacing/visual_pacing_plan.json")

WIDTH = 1920
HEIGHT = 1080
FPS = 30
AUDIO_SAMPLE_RATE = 48000
AUDIO_CHANNELS = 2

MAX_BEAT_DURATION_DRIFT_SEC = 1.00
MAX_FINAL_DURATION_DRIFT_SEC = 2.50

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv"}

PREVIEW_VIDEO_FILENAME = "final_video_visual_pacing_preview.mp4"
PREVIEW_REPORT_FILENAME = "visual_pacing_preview_report.json"
PREVIEW_SEGMENTS_DIRNAME = "visual_pacing_preview_segments"
PREVIEW_TMP_DIRNAME = "visual_pacing_preview_tmp"

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


class VisualPacingPreviewError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_path(value: str | Path) -> Path:
    path = Path(value)

    if path.is_absolute():
        try:
            return path.resolve().relative_to(REPO_ROOT)
        except ValueError as exc:
            raise VisualPacingPreviewError(f"path is outside repo root: {path}") from exc

    return path


def absolute_repo_path(value: str | Path) -> Path:
    return REPO_ROOT / repo_path(value)


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise VisualPacingPreviewError(f"required runtime tool missing: {name}")


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise VisualPacingPreviewError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise VisualPacingPreviewError(f"{field_name} must be non-empty")

    return normalized


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise VisualPacingPreviewError(f"{field_name} must be boolean")

    return value


def require_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise VisualPacingPreviewError(f"{field_name} must be integer")

    return value


def require_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise VisualPacingPreviewError(f"{field_name} must be number")

    if not isinstance(value, (int, float)):
        raise VisualPacingPreviewError(f"{field_name} must be number")

    normalized = float(value)
    if normalized <= 0:
        raise VisualPacingPreviewError(f"{field_name} must be > 0")

    return normalized


def require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise VisualPacingPreviewError(f"{field_name} must be list")

    return value


def read_json_file(path: Path) -> dict[str, Any]:
    absolute_path = absolute_repo_path(path)

    try:
        payload = json.loads(absolute_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualPacingPreviewError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualPacingPreviewError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise VisualPacingPreviewError(f"JSON file must contain an object: {path}")

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
        raise VisualPacingPreviewError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def ensure_existing_file(path_value: Any, field_name: str) -> Path:
    path_string = require_non_empty_string(path_value, field_name)
    path = repo_path(path_string)
    absolute_path = absolute_repo_path(path)

    if not absolute_path.exists():
        raise VisualPacingPreviewError(f"{field_name} does not exist: {path}")

    if not absolute_path.is_file():
        raise VisualPacingPreviewError(f"{field_name} must be a file: {path}")

    if absolute_path.stat().st_size <= 0:
        raise VisualPacingPreviewError(f"{field_name} is empty: {path}")

    return path


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
        raise VisualPacingPreviewError(
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
        raise VisualPacingPreviewError(
            f"ffprobe failed for {path}: {completed.stderr.strip()}"
        )

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise VisualPacingPreviewError(f"ffprobe JSON parse failed for {path}") from exc

    if not isinstance(payload, dict):
        raise VisualPacingPreviewError(f"ffprobe payload must be object for {path}")

    return payload


def probe_duration_sec(path: Path) -> float:
    payload = ffprobe_json(path)

    try:
        duration = float(payload["format"]["duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise VisualPacingPreviewError(f"duration missing from ffprobe for {path}") from exc

    if duration <= 0:
        raise VisualPacingPreviewError(f"duration must be positive for {path}")

    return round(duration, 3)


def probe_stream_types(path: Path) -> set[str]:
    payload = ffprobe_json(path)
    streams = payload.get("streams")

    if not isinstance(streams, list):
        raise VisualPacingPreviewError(f"ffprobe streams must be list for {path}")

    stream_types: set[str] = set()
    for stream in streams:
        if isinstance(stream, dict) and isinstance(stream.get("codec_type"), str):
            stream_types.add(stream["codec_type"])

    return stream_types


def validate_video_file(path: Path) -> tuple[float, int]:
    ensure_existing_file(str(path), "preview_video_path")

    stream_types = probe_stream_types(path)
    if "video" not in stream_types:
        raise VisualPacingPreviewError("preview video has no video stream")

    if "audio" not in stream_types:
        raise VisualPacingPreviewError("preview video has no audio stream")

    duration_sec = probe_duration_sec(path)
    size_bytes = absolute_repo_path(path).stat().st_size

    return duration_sec, size_bytes


def clean_preview_dirs(segments_dir: Path, tmp_dir: Path) -> None:
    for path in (segments_dir, tmp_dir):
        absolute_path = absolute_repo_path(path)
        if absolute_path.exists():
            shutil.rmtree(absolute_path)
        absolute_path.mkdir(parents=True, exist_ok=True)


def validate_plan(plan: dict[str, Any]) -> list[dict[str, Any]]:
    status = require_non_empty_string(plan.get("status"), "plan.status")
    if status != "VISUAL_PACING_PLAN_OK":
        raise VisualPacingPreviewError(f"plan.status must be VISUAL_PACING_PLAN_OK, got {status}")

    audio_master_clock = require_bool(plan.get("audio_master_clock"), "plan.audio_master_clock")
    if audio_master_clock is not True:
        raise VisualPacingPreviewError("plan.audio_master_clock must be true")

    scene_count = require_int(plan.get("scene_count"), "plan.scene_count")
    beat_count = require_int(plan.get("beat_count"), "plan.beat_count")

    if scene_count <= 0:
        raise VisualPacingPreviewError("plan.scene_count must be > 0")

    if beat_count <= scene_count:
        raise VisualPacingPreviewError("plan.beat_count must be greater than scene_count")

    duration_delta_sec = float(plan.get("duration_delta_sec", 999))
    if abs(duration_delta_sec) > 0.05:
        raise VisualPacingPreviewError(f"plan.duration_delta_sec too high: {duration_delta_sec}")

    beats = require_list(plan.get("beats"), "plan.beats")
    if len(beats) != beat_count:
        raise VisualPacingPreviewError(
            f"plan.beats length mismatch: beat_count={beat_count}, beats={len(beats)}"
        )

    normalized_beats: list[dict[str, Any]] = []
    previous_end = 0.0

    for index, beat in enumerate(beats, start=1):
        if not isinstance(beat, dict):
            raise VisualPacingPreviewError(f"beat[{index}] must be object")

        beat_id = require_non_empty_string(beat.get("beat_id"), f"beat[{index}].beat_id")
        scene_id = require_non_empty_string(beat.get("scene_id"), f"{beat_id}.scene_id")
        asset_id = require_non_empty_string(beat.get("asset_id"), f"{beat_id}.asset_id")
        audio_segment_id = require_non_empty_string(
            beat.get("audio_segment_id"),
            f"{beat_id}.audio_segment_id",
        )
        order = require_int(beat.get("order"), f"{beat_id}.order")
        beat_order = require_int(beat.get("beat_order"), f"{beat_id}.beat_order")
        scene_start_sec = float(beat.get("scene_start_sec"))
        scene_end_sec = float(beat.get("scene_end_sec"))
        global_start_sec = float(beat.get("global_start_sec"))
        global_end_sec = float(beat.get("global_end_sec"))
        beat_duration_sec = require_number(beat.get("beat_duration_sec"), f"{beat_id}.beat_duration_sec")

        if order <= 0:
            raise VisualPacingPreviewError(f"{beat_id}.order must be > 0")

        if beat_order <= 0:
            raise VisualPacingPreviewError(f"{beat_id}.beat_order must be > 0")

        if scene_end_sec <= scene_start_sec:
            raise VisualPacingPreviewError(f"{beat_id} scene timing is invalid")

        if global_end_sec <= global_start_sec:
            raise VisualPacingPreviewError(f"{beat_id} global timing is invalid")

        if abs(global_start_sec - previous_end) > 0.05:
            raise VisualPacingPreviewError(
                f"global timing gap/overlap at {beat_id}: start={global_start_sec}, previous_end={previous_end}"
            )

        source_visual_path = ensure_existing_file(beat.get("source_visual_path"), f"{beat_id}.source_visual_path")
        source_audio_path = ensure_existing_file(beat.get("source_audio_path"), f"{beat_id}.source_audio_path")

        extension = source_visual_path.suffix.lower()
        if extension not in IMAGE_EXTENSIONS and extension not in VIDEO_EXTENSIONS:
            raise VisualPacingPreviewError(f"{beat_id} unsupported visual extension: {extension}")

        display_text = beat.get("display_text", "")
        if not isinstance(display_text, str):
            raise VisualPacingPreviewError(f"{beat_id}.display_text must be string")

        text_mode = require_non_empty_string(beat.get("text_mode"), f"{beat_id}.text_mode")
        visual_action = require_non_empty_string(beat.get("visual_action"), f"{beat_id}.visual_action")
        motion_profile = require_non_empty_string(beat.get("motion_profile"), f"{beat_id}.motion_profile")

        normalized = {
            "asset_id": asset_id,
            "audio_segment_id": audio_segment_id,
            "beat_duration_sec": round(beat_duration_sec, 3),
            "beat_id": beat_id,
            "beat_order": beat_order,
            "display_text": display_text.strip(),
            "extension": extension,
            "global_end_sec": round(global_end_sec, 3),
            "global_start_sec": round(global_start_sec, 3),
            "motion_profile": motion_profile,
            "order": order,
            "scene_end_sec": round(scene_end_sec, 3),
            "scene_id": scene_id,
            "scene_start_sec": round(scene_start_sec, 3),
            "source_audio_path": str(source_audio_path),
            "source_visual_path": str(source_visual_path),
            "text_mode": text_mode,
            "visual_action": visual_action,
        }

        fail_if_forbidden_markers(json.dumps(normalized, ensure_ascii=False), beat_id)
        normalized_beats.append(normalized)
        previous_end = global_end_sec

    return normalized_beats


def base_video_filter(beat: dict[str, Any]) -> str:
    motion_profile = beat.get("motion_profile", "static_safe")
    visual_action = beat.get("visual_action", "hold_safe")

    base = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,fps={FPS},format=yuv420p"
    )

    if motion_profile == "ken_burns_subtle" and visual_action == "slow_zoom_in":
        return (
            f"scale={WIDTH * 2}:{HEIGHT * 2}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan=z='min(zoom+0.0008,1.08)':d=1:s={WIDTH}x{HEIGHT}:fps={FPS},"
            "setsar=1,format=yuv420p"
        )

    if motion_profile == "ken_burns_subtle" and visual_action == "slow_zoom_out":
        return (
            f"scale={WIDTH * 2}:{HEIGHT * 2}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan=z='max(1.08-on*0.0008,1.0)':d=1:s={WIDTH}x{HEIGHT}:fps={FPS},"
            "setsar=1,format=yuv420p"
        )

    if motion_profile == "micro_pan" and visual_action == "pan_left":
        return (
            f"scale={WIDTH + 120}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT}:x='min(120,n*0.35)':y=0,"
            f"fps={FPS},setsar=1,format=yuv420p"
        )

    if motion_profile == "micro_pan" and visual_action == "pan_right":
        return (
            f"scale={WIDTH + 120}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT}:x='max(120-n*0.35,0)':y=0,"
            f"fps={FPS},setsar=1,format=yuv420p"
        )

    if motion_profile == "micro_zoom":
        return (
            f"scale={WIDTH * 2}:{HEIGHT * 2}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan=z='min(zoom+0.0004,1.04)':d=1:s={WIDTH}x{HEIGHT}:fps={FPS},"
            "setsar=1,format=yuv420p"
        )

    return base


def audio_filter_for_beat(beat: dict[str, Any]) -> str:
    start = float(beat["scene_start_sec"])
    duration = float(beat["beat_duration_sec"])
    end = start + duration

    return (
        f"atrim=start={start:.3f}:end={end:.3f},"
        "asetpts=PTS-STARTPTS,"
        f"apad=whole_dur={duration:.3f}"
    )


def beat_output_path(segments_dir: Path, beat: dict[str, Any]) -> Path:
    safe_beat_id = beat["beat_id"].replace("/", "_").replace(" ", "_")
    return segments_dir / f"{beat['order']:03d}_{beat['beat_order']:03d}_{safe_beat_id}.mp4"


def render_beat(beat: dict[str, Any], output_path: Path) -> None:
    visual_path = repo_path(beat["source_visual_path"])
    audio_path = repo_path(beat["source_audio_path"])
    duration = f"{float(beat['beat_duration_sec']):.3f}"
    extension = beat["extension"]
    video_filter = base_video_filter(beat)
    audio_filter = audio_filter_for_beat(beat)
    filter_complex = f"[0:v]{video_filter}[v];[1:a]{audio_filter}[a]"

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
            "-i",
            str(absolute_repo_path(audio_path)),
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-t",
            duration,
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
            "-c:a",
            "aac",
            "-ar",
            str(AUDIO_SAMPLE_RATE),
            "-ac",
            str(AUDIO_CHANNELS),
            "-movflags",
            "+faststart",
            str(output_absolute),
        ]
    elif extension in VIDEO_EXTENSIONS:
        command = [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-t",
            duration,
            "-i",
            str(absolute_repo_path(visual_path)),
            "-i",
            str(absolute_repo_path(audio_path)),
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-t",
            duration,
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
            "-c:a",
            "aac",
            "-ar",
            str(AUDIO_SAMPLE_RATE),
            "-ac",
            str(AUDIO_CHANNELS),
            "-movflags",
            "+faststart",
            str(output_absolute),
        ]
    else:
        raise VisualPacingPreviewError(f"unsupported visual extension: {extension}")

    run_command(command, f"render beat {beat['beat_id']}")


def validate_beat_segment(output_path: Path, expected_duration_sec: float, beat_id: str) -> tuple[float, float]:
    ensure_existing_file(str(output_path), f"{beat_id}.output_path")

    stream_types = probe_stream_types(output_path)
    if "video" not in stream_types:
        raise VisualPacingPreviewError(f"{beat_id} output has no video stream")

    if "audio" not in stream_types:
        raise VisualPacingPreviewError(f"{beat_id} output has no audio stream")

    actual_duration_sec = probe_duration_sec(output_path)
    duration_delta_sec = round(actual_duration_sec - expected_duration_sec, 3)

    if abs(duration_delta_sec) > MAX_BEAT_DURATION_DRIFT_SEC:
        raise VisualPacingPreviewError(
            f"{beat_id} duration drift too high: delta={duration_delta_sec}, "
            f"expected={expected_duration_sec}, actual={actual_duration_sec}"
        )

    return actual_duration_sec, duration_delta_sec


def quote_concat_path(path: Path) -> str:
    value = str(path.resolve())
    escaped = value.replace("'", "'\\''")
    return f"file '{escaped}'"


def write_concat_list(tmp_dir: Path, segment_paths: list[Path]) -> Path:
    concat_path = tmp_dir / "concat_list.txt"
    concat_absolute = absolute_repo_path(concat_path)
    concat_absolute.parent.mkdir(parents=True, exist_ok=True)

    lines = [quote_concat_path(absolute_repo_path(path)) for path in segment_paths]
    concat_absolute.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return concat_path


def concat_segments(segment_paths: list[Path], preview_video_path: Path, tmp_dir: Path) -> None:
    concat_path = write_concat_list(tmp_dir, segment_paths)

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
        str(absolute_repo_path(preview_video_path)),
    ]

    run_command(command, "concat visual pacing preview")


def build_report(
    plan: dict[str, Any],
    plan_path: Path,
    preview_video_path: Path,
    final_duration_sec: float,
    final_video_size_bytes: int,
    segment_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    expected_duration_sec = float(plan["total_duration_sec"])
    duration_delta_sec = round(final_duration_sec - expected_duration_sec, 3)

    if abs(duration_delta_sec) > MAX_FINAL_DURATION_DRIFT_SEC:
        raise VisualPacingPreviewError(
            f"preview duration drift too high: delta={duration_delta_sec}, "
            f"expected={expected_duration_sec}, actual={final_duration_sec}"
        )

    return {
        "created_at": utc_now_iso(),
        "duration_delta_sec": duration_delta_sec,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "expected_duration_sec": round(expected_duration_sec, 3),
        "failed_beat_count": 0,
        "final_video_size_bytes": final_video_size_bytes,
        "max_beat_duration_drift_sec": MAX_BEAT_DURATION_DRIFT_SEC,
        "max_final_duration_drift_sec": MAX_FINAL_DURATION_DRIFT_SEC,
        "preview_video_exists": True,
        "preview_video_path": str(preview_video_path),
        "project_id": plan["project_id"],
        "render_mode": "visual_pacing_preview_no_drawtext",
        "rendered_beat_count": len(segment_reports),
        "scene_count": plan["scene_count"],
        "source_visual_pacing_plan_path": str(plan_path),
        "status": "VISUAL_PACING_PREVIEW_OK",
        "text_overlay_enabled": False,
        "total_duration_sec": final_duration_sec,
        "video_profile": {
            "audio_channels": AUDIO_CHANNELS,
            "audio_codec": "aac",
            "audio_sample_rate": AUDIO_SAMPLE_RATE,
            "container": "mp4",
            "fps": FPS,
            "pixel_format": "yuv420p",
            "resolution": f"{WIDTH}x{HEIGHT}",
            "video_codec": "h264/libx264",
        },
        "segments": segment_reports,
        "warnings": [
            "preview artifact only",
            "text overlay disabled because local ffmpeg has no drawtext filter",
            "does not update PROJECT_STATE",
            "does not replace production final_video.mp4",
            "does not approve upload",
        ],
    }


def run_preview(plan_path: Path) -> dict[str, Any]:
    require_tool("ffmpeg")
    require_tool("ffprobe")

    plan_path = repo_path(plan_path)
    plan = read_json_file(plan_path)
    beats = validate_plan(plan)

    project_dir = plan_path.parent.parent
    final_render_dir = project_dir / "final_render"
    segments_dir = final_render_dir / PREVIEW_SEGMENTS_DIRNAME
    tmp_dir = final_render_dir / PREVIEW_TMP_DIRNAME
    preview_video_path = final_render_dir / PREVIEW_VIDEO_FILENAME
    preview_report_path = final_render_dir / PREVIEW_REPORT_FILENAME

    clean_preview_dirs(segments_dir, tmp_dir)

    segment_reports: list[dict[str, Any]] = []
    segment_paths: list[Path] = []

    for beat in beats:
        output_path = beat_output_path(segments_dir, beat)

        render_beat(beat, output_path)

        actual_duration_sec, duration_delta_sec = validate_beat_segment(
            output_path=output_path,
            expected_duration_sec=float(beat["beat_duration_sec"]),
            beat_id=beat["beat_id"],
        )

        segment_paths.append(output_path)
        segment_reports.append(
            {
                "actual_duration_sec": actual_duration_sec,
                "asset_id": beat["asset_id"],
                "audio_segment_id": beat["audio_segment_id"],
                "beat_duration_sec": beat["beat_duration_sec"],
                "beat_id": beat["beat_id"],
                "beat_order": beat["beat_order"],
                "display_text": beat["display_text"],
                "duration_delta_sec": duration_delta_sec,
                "motion_profile": beat["motion_profile"],
                "order": beat["order"],
                "output_path": str(output_path),
                "render_status": "rendered",
                "scene_id": beat["scene_id"],
                "text_mode": beat["text_mode"],
                "visual_action": beat["visual_action"],
            }
        )

    concat_segments(
        segment_paths=segment_paths,
        preview_video_path=preview_video_path,
        tmp_dir=tmp_dir,
    )

    final_duration_sec, final_video_size_bytes = validate_video_file(preview_video_path)

    report = build_report(
        plan=plan,
        plan_path=plan_path,
        preview_video_path=preview_video_path,
        final_duration_sec=final_duration_sec,
        final_video_size_bytes=final_video_size_bytes,
        segment_reports=segment_reports,
    )

    write_json_atomic(preview_report_path, report)

    return {
        "beat_count": len(beats),
        "duration_delta_sec": report["duration_delta_sec"],
        "expected_duration_sec": report["expected_duration_sec"],
        "preview_report_path": str(preview_report_path),
        "preview_video_path": str(preview_video_path),
        "preview_video_size_bytes": final_video_size_bytes,
        "project_id": report["project_id"],
        "scene_count": report["scene_count"],
        "status": "VISUAL_PACING_PREVIEW_RENDER_OK",
        "text_overlay_enabled": False,
        "total_duration_sec": final_duration_sec,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render FlowMind visual pacing preview video")
    parser.add_argument(
        "--plan",
        default=str(DEFAULT_PLAN_PATH),
        help="Path to visual_pacing_plan.json relative to repo root",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = run_preview(repo_path(args.plan))
    except (VisualPacingPreviewError, OSError) as exc:
        print(f"[VISUAL_PACING_PREVIEW][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
