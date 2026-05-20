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
EXECUTOR_VERSION = "1.0.0"


FINAL_RENDER_DIRNAME = "final_render"
SEGMENTS_DIRNAME = "segments"
TMP_DIRNAME = "tmp"
FINAL_VIDEO_FILENAME = "final_video.mp4"
FINAL_RENDER_REPORT_FILENAME = "final_render_report.json"

WIDTH = 1920
HEIGHT = 1080
FPS = 30
AUDIO_SAMPLE_RATE = 48000
AUDIO_CHANNELS = 2

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


def repo_relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError as exc:
        raise FinalRenderExecutorError(f"path is outside repo root: {path}") from exc


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
    if isinstance(value, bool):
        raise FinalRenderExecutorError(f"{field_name} must be number")

    if not isinstance(value, int | float):
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

    stream_types: set[str] = set()
    for stream in streams:
        if isinstance(stream, dict) and isinstance(stream.get("codec_type"), str):
            stream_types.add(stream["codec_type"])

    return stream_types


def validate_final_video(path: Path) -> tuple[float, int]:
    ensure_existing_file(path, "final_video")
    duration = probe_duration_sec(path)
    stream_types = probe_stream_types(path)

    if "video" not in stream_types:
        raise FinalRenderExecutorError("final video has no video stream")

    if "audio" not in stream_types:
        raise FinalRenderExecutorError("final video has no audio stream")

    size_bytes = absolute_repo_path(path).stat().st_size

    return duration, size_bytes


def validate_state(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    phase = require_non_empty_string(state.get("phase"), "PROJECT_STATE.phase")
    if phase != "QA":
        raise FinalRenderExecutorError(f"PROJECT_STATE.phase must be QA, got {phase}")

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

    if scene_count <= 0:
        raise FinalRenderExecutorError("assembly_plan.scene_count must be > 0")

    if len(timeline) != scene_count:
        raise FinalRenderExecutorError(
            f"assembly scene count mismatch: scene_count={scene_count}, timeline={len(timeline)}"
        )

    orders: set[int] = set()
    normalized_timeline: list[dict[str, Any]] = []

    for index, item in enumerate(timeline, start=1):
        if not isinstance(item, dict):
            raise FinalRenderExecutorError(f"timeline[{index}] must be an object")

        order = require_int(item.get("order"), f"timeline[{index}].order")
        scene_id = require_non_empty_string(item.get("scene_id"), f"timeline[{index}].scene_id")
        asset_id = require_non_empty_string(item.get("asset_id"), f"timeline[{index}].asset_id")
        timeline_id = require_non_empty_string(item.get("timeline_id"), f"timeline[{index}].timeline_id")

        if order in orders:
            raise FinalRenderExecutorError(f"duplicate timeline order: {order}")

        orders.add(order)

        normalized_timeline.append(
            {
                "timeline_id": timeline_id,
                "scene_id": scene_id,
                "asset_id": asset_id,
                "order": order,
            }
        )

    return sorted(normalized_timeline, key=lambda value: value["order"])


def validate_resolved_assets(resolved_assets: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
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

    assets = require_list(resolved_assets.get("assets"), "resolved_assets.assets")
    if len(assets) != asset_count:
        raise FinalRenderExecutorError(
            f"resolved_assets.assets length mismatch: asset_count={asset_count}, assets={len(assets)}"
        )

    asset_map: dict[tuple[str, str], dict[str, Any]] = {}

    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            raise FinalRenderExecutorError(f"resolved_assets.assets[{index}] must be an object")

        asset_id = require_non_empty_string(asset.get("asset_id"), f"asset[{index}].asset_id")
        scene_id = require_non_empty_string(asset.get("scene_id"), f"asset[{index}].scene_id")
        asset_type = require_non_empty_string(asset.get("asset_type"), f"asset[{index}].asset_type")
        local_path = repo_path(require_non_empty_string(asset.get("local_path"), f"asset[{index}].local_path"))
        order = require_int(asset.get("order"), f"asset[{index}].order")

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

        if provider_status != "resolved":
            raise FinalRenderExecutorError(f"{asset_id} provider_status must be resolved")

        if license_status != "cleared":
            raise FinalRenderExecutorError(f"{asset_id} license_status must be cleared")

        if resolution_status != "ready":
            raise FinalRenderExecutorError(f"{asset_id} resolution_status must be ready")

        extension = local_path.suffix.lower()
        if extension not in ALLOWED_VISUAL_EXTENSIONS:
            raise FinalRenderExecutorError(f"{asset_id} unsupported visual extension: {extension}")

        ensure_existing_file(local_path, f"{asset_id}.local_path")

        key = (scene_id, asset_id)
        if key in asset_map:
            raise FinalRenderExecutorError(f"duplicate resolved asset match: scene={scene_id}, asset={asset_id}")

        asset_map[key] = {
            "asset_id": asset_id,
            "scene_id": scene_id,
            "order": order,
            "asset_type": asset_type,
            "local_path": str(local_path),
            "extension": extension,
        }

    return asset_map


def validate_audio_render(audio_render: dict[str, Any]) -> dict[str, dict[str, Any]]:
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

    rendered_segment_count = require_int(
        audio_render.get("rendered_segment_count"),
        "audio_render.rendered_segment_count",
    )
    segment_count = require_int(audio_render.get("segment_count"), "audio_render.segment_count")
    failed_segment_count = require_int(
        audio_render.get("failed_segment_count"),
        "audio_render.failed_segment_count",
    )

    if rendered_segment_count != segment_count:
        raise FinalRenderExecutorError("audio_render.rendered_segment_count must equal segment_count")

    if failed_segment_count != 0:
        raise FinalRenderExecutorError("audio_render.failed_segment_count must be 0")

    missing_requirements = require_list(
        audio_render.get("missing_requirements"),
        "audio_render.missing_requirements",
    )
    blockers = require_list(audio_render.get("blockers"), "audio_render.blockers")

    if missing_requirements:
        raise FinalRenderExecutorError(
            f"audio_render.missing_requirements must be empty, got {missing_requirements}"
        )

    if blockers:
        raise FinalRenderExecutorError(f"audio_render.blockers must be empty, got {blockers}")

    segments = require_list(audio_render.get("segments"), "audio_render.segments")
    if len(segments) != segment_count:
        raise FinalRenderExecutorError(
            f"audio_render.segments length mismatch: segment_count={segment_count}, segments={len(segments)}"
        )

    audio_map: dict[str, dict[str, Any]] = {}

    for index, segment in enumerate(segments, start=1):
        if not isinstance(segment, dict):
            raise FinalRenderExecutorError(f"audio_render.segments[{index}] must be an object")

        segment_id = require_non_empty_string(segment.get("segment_id"), f"audio_segment[{index}].segment_id")
        source_scene_id = require_non_empty_string(
            segment.get("source_scene_id"),
            f"audio_segment[{index}].source_scene_id",
        )
        audio_path = repo_path(require_non_empty_string(segment.get("audio_path"), f"audio_segment[{index}].audio_path"))
        duration_sec = require_number(segment.get("duration_sec"), f"audio_segment[{index}].duration_sec")
        order = require_int(segment.get("order"), f"audio_segment[{index}].order")

        tts_status = require_non_empty_string(segment.get("tts_status"), f"audio_segment[{index}].tts_status")
        provider_status = require_non_empty_string(
            segment.get("provider_status"),
            f"audio_segment[{index}].provider_status",
        )
        segment_duration_validated = require_bool(
            segment.get("duration_validated"),
            f"audio_segment[{index}].duration_validated",
        )

        if duration_sec <= 0:
            raise FinalRenderExecutorError(f"{segment_id} duration_sec must be > 0")

        if tts_status != "rendered":
            raise FinalRenderExecutorError(f"{segment_id} tts_status must be rendered")

        if provider_status != "rendered":
            raise FinalRenderExecutorError(f"{segment_id} provider_status must be rendered")

        if segment_duration_validated is not True:
            raise FinalRenderExecutorError(f"{segment_id} duration_validated must be true")

        ensure_existing_file(audio_path, f"{segment_id}.audio_path")

        if source_scene_id in audio_map:
            raise FinalRenderExecutorError(f"duplicate audio segment for scene: {source_scene_id}")

        audio_map[source_scene_id] = {
            "segment_id": segment_id,
            "source_scene_id": source_scene_id,
            "audio_path": str(audio_path),
            "duration_sec": round(duration_sec, 3),
            "order": order,
        }

    return audio_map


def validate_loudness_report(loudness_report: dict[str, Any], project_id: str, audio_segment_count: int) -> None:
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

    if segment_count != audio_segment_count:
        raise FinalRenderExecutorError(
            f"audio_loudness_report.segment_count mismatch: report={segment_count}, audio={audio_segment_count}"
        )


def build_scene_jobs(
    timeline: list[dict[str, Any]],
    asset_map: dict[tuple[str, str], dict[str, Any]],
    audio_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []

    for item in timeline:
        scene_id = item["scene_id"]
        asset_id = item["asset_id"]
        order = item["order"]

        asset = asset_map.get((scene_id, asset_id))
        if asset is None:
            raise FinalRenderExecutorError(f"missing resolved asset for scene={scene_id}, asset={asset_id}")

        audio = audio_map.get(scene_id)
        if audio is None:
            raise FinalRenderExecutorError(f"missing audio segment for scene={scene_id}")

        if asset["order"] != order:
            raise FinalRenderExecutorError(
                f"asset order mismatch for {scene_id}: timeline={order}, asset={asset['order']}"
            )

        if audio["order"] != order:
            raise FinalRenderExecutorError(
                f"audio order mismatch for {scene_id}: timeline={order}, audio={audio['order']}"
            )

        jobs.append(
            {
                "timeline_id": item["timeline_id"],
                "scene_id": scene_id,
                "order": order,
                "asset_id": asset_id,
                "visual_asset_path": asset["local_path"],
                "visual_asset_type": asset["asset_type"],
                "visual_extension": asset["extension"],
                "audio_segment_id": audio["segment_id"],
                "audio_path": audio["audio_path"],
                "audio_duration_sec": audio["duration_sec"],
            }
        )

    return sorted(jobs, key=lambda value: value["order"])


def scene_output_path(segments_dir: Path, order: int, scene_id: str) -> Path:
    return segments_dir / f"{order:03d}_{scene_id}.mp4"


def render_scene(job: dict[str, Any], scene_video_path: Path) -> None:
    visual_path = repo_path(job["visual_asset_path"])
    audio_path = repo_path(job["audio_path"])
    duration = f"{float(job['audio_duration_sec']):.3f}"
    extension = str(job["visual_extension"]).lower()

    video_filter = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,fps={FPS},format=yuv420p"
    )

    scene_video_absolute = absolute_repo_path(scene_video_path)
    scene_video_absolute.parent.mkdir(parents=True, exist_ok=True)

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
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
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
            "-c:a",
            "aac",
            "-ar",
            str(AUDIO_SAMPLE_RATE),
            "-ac",
            str(AUDIO_CHANNELS),
            "-shortest",
            "-movflags",
            "+faststart",
            str(scene_video_absolute),
        ]
    elif extension in VIDEO_EXTENSIONS:
        command = [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            str(absolute_repo_path(visual_path)),
            "-i",
            str(absolute_repo_path(audio_path)),
            "-t",
            duration,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
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
            "-c:a",
            "aac",
            "-ar",
            str(AUDIO_SAMPLE_RATE),
            "-ac",
            str(AUDIO_CHANNELS),
            "-shortest",
            "-movflags",
            "+faststart",
            str(scene_video_absolute),
        ]
    else:
        raise FinalRenderExecutorError(f"unsupported visual extension: {extension}")

    run_command(command, f"render scene {job['scene_id']}")


def validate_scene_segment(scene_video_path: Path, expected_duration_sec: float, scene_id: str) -> tuple[float, float]:
    ensure_existing_file(scene_video_path, f"{scene_id}.scene_video_path")

    stream_types = probe_stream_types(scene_video_path)
    if "video" not in stream_types:
        raise FinalRenderExecutorError(f"{scene_id} scene segment has no video stream")

    if "audio" not in stream_types:
        raise FinalRenderExecutorError(f"{scene_id} scene segment has no audio stream")

    scene_duration_sec = probe_duration_sec(scene_video_path)
    duration_delta_sec = round(scene_duration_sec - expected_duration_sec, 3)

    if abs(duration_delta_sec) > MAX_SCENE_DURATION_DRIFT_SEC:
        raise FinalRenderExecutorError(
            f"{scene_id} duration drift too high: delta={duration_delta_sec}, "
            f"expected={expected_duration_sec}, actual={scene_duration_sec}"
        )

    return scene_duration_sec, duration_delta_sec


def quote_concat_path(path: Path) -> str:
    value = str(path.resolve())
    escaped = value.replace("'", "'\\''")
    return f"file '{escaped}'"


def write_concat_list(tmp_dir: Path, scene_paths: list[Path]) -> Path:
    concat_path = tmp_dir / "concat_list.txt"
    concat_absolute = absolute_repo_path(concat_path)
    concat_absolute.parent.mkdir(parents=True, exist_ok=True)

    lines = [quote_concat_path(absolute_repo_path(path)) for path in scene_paths]
    concat_absolute.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return concat_path


def concat_scene_segments(scene_paths: list[Path], final_video_path: Path, tmp_dir: Path) -> None:
    concat_path = write_concat_list(tmp_dir, scene_paths)

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
        str(absolute_repo_path(final_video_path)),
    ]

    run_command(command, "concat final video")


def build_success_report(
    project_id: str,
    state_path: Path,
    assembly_plan_path: Path,
    resolved_assets_path: Path,
    audio_render_path: Path,
    final_video_path: Path,
    final_duration_sec: float,
    final_video_size_bytes: int,
    expected_duration_sec: float,
    segment_reports: list[dict[str, Any]],
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
        "scene_count": len(segment_reports),
        "rendered_scene_count": len(segment_reports),
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
        "segments": segment_reports,
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
    asset_map = validate_resolved_assets(resolved_assets)
    audio_map = validate_audio_render(audio_render)
    validate_loudness_report(loudness_report, project_id, len(audio_map))

    scene_jobs = build_scene_jobs(
        timeline=timeline,
        asset_map=asset_map,
        audio_map=audio_map,
    )

    project_dir = state_path.parent
    final_render_dir = project_dir / FINAL_RENDER_DIRNAME
    segments_dir = final_render_dir / SEGMENTS_DIRNAME
    tmp_dir = final_render_dir / TMP_DIRNAME
    final_video_path = final_render_dir / FINAL_VIDEO_FILENAME
    final_render_report_path = final_render_dir / FINAL_RENDER_REPORT_FILENAME

    absolute_repo_path(segments_dir).mkdir(parents=True, exist_ok=True)
    absolute_repo_path(tmp_dir).mkdir(parents=True, exist_ok=True)

    segment_reports: list[dict[str, Any]] = []
    scene_paths: list[Path] = []

    for job in scene_jobs:
        output_path = scene_output_path(
            segments_dir=segments_dir,
            order=job["order"],
            scene_id=job["scene_id"],
        )

        render_scene(job, output_path)
        scene_duration_sec, duration_delta_sec = validate_scene_segment(
            scene_video_path=output_path,
            expected_duration_sec=float(job["audio_duration_sec"]),
            scene_id=job["scene_id"],
        )

        scene_paths.append(output_path)

        segment_reports.append(
            {
                "timeline_id": job["timeline_id"],
                "scene_id": job["scene_id"],
                "order": job["order"],
                "asset_id": job["asset_id"],
                "visual_asset_path": job["visual_asset_path"],
                "visual_asset_type": job["visual_asset_type"],
                "audio_segment_id": job["audio_segment_id"],
                "audio_path": job["audio_path"],
                "scene_video_path": str(output_path),
                "scene_duration_sec": scene_duration_sec,
                "audio_duration_sec": job["audio_duration_sec"],
                "duration_delta_sec": duration_delta_sec,
                "render_status": "rendered",
                "error_message": None,
            }
        )

    concat_scene_segments(
        scene_paths=scene_paths,
        final_video_path=final_video_path,
        tmp_dir=tmp_dir,
    )

    final_duration_sec, final_video_size_bytes = validate_final_video(final_video_path)
    expected_duration_sec = sum(float(job["audio_duration_sec"]) for job in scene_jobs)

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
        segment_reports=segment_reports,
    )

    write_json_atomic(final_render_report_path, report)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["final_video_path"] = str(final_video_path)
    candidate_artifacts["final_render_report_path"] = str(final_render_report_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = utc_now_iso()

    saved_state = save_state_with_disk_guard(absolute_repo_path(state_path), candidate_state)

    return {
        "status": "FINAL_RENDER_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "final_video_path": str(final_video_path),
        "final_render_report_path": str(final_render_report_path),
        "final_video_size_bytes": final_video_size_bytes,
        "final_duration_sec": final_duration_sec,
        "expected_duration_sec": round(expected_duration_sec, 3),
        "scene_count": len(segment_reports),
        "verdict": report["verdict"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind final render executor v1")
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
