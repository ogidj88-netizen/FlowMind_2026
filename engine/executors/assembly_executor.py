from __future__ import annotations

import argparse
import json
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

EXECUTOR_NAME = "assembly_executor"
EXECUTOR_VERSION = "2.0.0"

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

ALLOWED_VISUAL_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov", ".mkv"}


class AssemblyExecutorError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise AssemblyExecutorError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise AssemblyExecutorError(f"{field_name} must be non-empty")
    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise AssemblyExecutorError(f"{field_name} must be an integer")
    if value <= 0:
        raise AssemblyExecutorError(f"{field_name} must be > 0")
    return value


def require_non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise AssemblyExecutorError(f"{field_name} must be an integer")
    if value < 0:
        raise AssemblyExecutorError(f"{field_name} must be >= 0")
    return value


def require_positive_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AssemblyExecutorError(f"{field_name} must be numeric")
    normalized = float(value)
    if normalized <= 0:
        raise AssemblyExecutorError(f"{field_name} must be > 0")
    return normalized


def require_non_negative_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AssemblyExecutorError(f"{field_name} must be numeric")
    normalized = float(value)
    if normalized < 0:
        raise AssemblyExecutorError(f"{field_name} must be >= 0")
    return normalized


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise AssemblyExecutorError(f"{field_name} must be boolean")
    return value


def require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise AssemblyExecutorError(f"{field_name} must be a list")
    return value


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssemblyExecutorError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssemblyExecutorError(f"Invalid JSON file: {path}") from exc
    if not isinstance(payload, dict):
        raise AssemblyExecutorError(f"JSON file must contain an object: {path}")
    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    fail_if_forbidden_markers(serialized, str(path))
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(path)


def fail_if_forbidden_markers(value: str, source_name: str) -> None:
    upper_value = value.upper()
    hits = [marker for marker in FORBIDDEN_MARKERS if marker in upper_value]
    if hits:
        raise AssemblyExecutorError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def resolve_existing_file(path_value: Any, field_name: str) -> tuple[str, Path]:
    path_string = require_non_empty_string(path_value, field_name)
    supplied = Path(path_string)
    resolved = supplied if supplied.is_absolute() else REPO_ROOT / supplied
    if not resolved.exists():
        raise AssemblyExecutorError(f"{field_name} does not exist: {path_string}")
    if not resolved.is_file():
        raise AssemblyExecutorError(f"{field_name} must be a file: {path_string}")
    if resolved.stat().st_size <= 0:
        raise AssemblyExecutorError(f"{field_name} must be non-empty: {path_string}")
    return path_string, resolved


def validate_project_id(project_id: str, payload: dict[str, Any], source_name: str) -> None:
    payload_project_id = require_non_empty_string(
        payload.get("project_id"),
        f"{source_name}.project_id",
    )
    if payload_project_id != project_id:
        raise AssemblyExecutorError(
            f"project_id mismatch: state={project_id}, {source_name}={payload_project_id}"
        )


def validate_visual_pacing(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], int, float]:
    if payload.get("status") != "VISUAL_PACING_PLAN_OK":
        raise AssemblyExecutorError("visual_pacing.status must be VISUAL_PACING_PLAN_OK")
    if payload.get("timing_source") != "actual_canonical_audio":
        raise AssemblyExecutorError("visual_pacing.timing_source must be actual_canonical_audio")
    if require_bool(payload.get("audio_master_clock"), "visual_pacing.audio_master_clock") is not True:
        raise AssemblyExecutorError("visual_pacing.audio_master_clock must be true")
    if require_bool(payload.get("timed_execution_ready"), "visual_pacing.timed_execution_ready") is not True:
        raise AssemblyExecutorError("visual_pacing.timed_execution_ready must be true")

    scene_count = require_positive_int(payload.get("scene_count"), "visual_pacing.scene_count")
    beat_count = require_positive_int(payload.get("beat_count"), "visual_pacing.beat_count")
    total_duration_sec = require_positive_number(
        payload.get("total_duration_sec"),
        "visual_pacing.total_duration_sec",
    )

    duration_delta_sec = payload.get("duration_delta_sec")
    if not isinstance(duration_delta_sec, (int, float)):
        raise AssemblyExecutorError("visual_pacing.duration_delta_sec must be numeric")
    if abs(float(duration_delta_sec)) > 0.05:
        raise AssemblyExecutorError(
            f"visual_pacing.duration_delta_sec too high: {duration_delta_sec}"
        )

    beats = require_list(payload.get("beats"), "visual_pacing.beats")
    if len(beats) != beat_count:
        raise AssemblyExecutorError(
            f"visual_pacing beat_count mismatch: declared={beat_count}, actual={len(beats)}"
        )

    previous_global_end = 0.0
    for index, beat in enumerate(beats, start=1):
        if not isinstance(beat, dict):
            raise AssemblyExecutorError(f"visual_pacing.beats[{index}] must be an object")

        require_non_empty_string(beat.get("beat_id"), f"beat[{index}].beat_id")
        require_non_empty_string(beat.get("scene_id"), f"beat[{index}].scene_id")
        require_positive_int(beat.get("scene_order"), f"beat[{index}].scene_order")
        require_positive_int(beat.get("beat_order"), f"beat[{index}].beat_order")
        require_non_empty_string(
            beat.get("requested_asset_type"),
            f"beat[{index}].requested_asset_type",
        )
        require_non_empty_string(
            beat.get("visual_intent"),
            f"beat[{index}].visual_intent",
        )
        require_non_empty_string(
            beat.get("source_visual_unit_id"),
            f"beat[{index}].source_visual_unit_id",
        )

        start = require_non_negative_number(
            beat.get("global_start_sec"),
            f"beat[{index}].global_start_sec",
        )
        end = require_positive_number(
            beat.get("global_end_sec"),
            f"beat[{index}].global_end_sec",
        )
        duration = require_positive_number(
            beat.get("beat_duration_sec"),
            f"beat[{index}].beat_duration_sec",
        )

        if end <= start:
            raise AssemblyExecutorError(f"beat[{index}] global_end_sec must be > global_start_sec")
        if abs(start - previous_global_end) > 0.05:
            raise AssemblyExecutorError(
                f"global beat gap/overlap at {index}: start={start}, previous_end={previous_global_end}"
            )
        if abs((end - start) - duration) > 0.05:
            raise AssemblyExecutorError(
                f"beat[{index}] duration mismatch: range={end-start}, duration={duration}"
            )
        previous_global_end = end

    if abs(previous_global_end - total_duration_sec) > 0.05:
        raise AssemblyExecutorError(
            f"visual pacing total duration mismatch: beats={previous_global_end}, total={total_duration_sec}"
        )

    return beats, scene_count, round(total_duration_sec, 3)


def validate_assets(
    assets_payload: dict[str, Any],
    beats: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if assets_payload.get("timing_source") != "actual_canonical_audio":
        raise AssemblyExecutorError("assets.timing_source must be actual_canonical_audio")
    if assets_payload.get("media_requirements_source") != "timed_visual_pacing_beats":
        raise AssemblyExecutorError(
            "assets.media_requirements_source must be timed_visual_pacing_beats"
        )

    asset_count = require_positive_int(assets_payload.get("asset_count"), "assets.asset_count")
    assets = require_list(assets_payload.get("assets"), "assets.assets")

    if asset_count != len(assets):
        raise AssemblyExecutorError(
            f"assets asset_count mismatch: declared={asset_count}, actual={len(assets)}"
        )
    if asset_count != len(beats):
        raise AssemblyExecutorError(
            f"assets/beat count mismatch: assets={asset_count}, beats={len(beats)}"
        )

    seen_ids: set[str] = set()
    for index, (asset, beat) in enumerate(zip(assets, beats), start=1):
        if not isinstance(asset, dict):
            raise AssemblyExecutorError(f"assets.assets[{index}] must be an object")

        asset_id = require_non_empty_string(asset.get("asset_id"), f"asset[{index}].asset_id")
        if asset_id in seen_ids:
            raise AssemblyExecutorError(f"duplicate asset_id: {asset_id}")
        seen_ids.add(asset_id)

        scene_id = require_non_empty_string(asset.get("scene_id"), f"asset[{index}].scene_id")
        asset_type = require_non_empty_string(
            asset.get("asset_type"),
            f"asset[{index}].asset_type",
        )
        visual_intent = require_non_empty_string(
            asset.get("visual_intent"),
            f"asset[{index}].visual_intent",
        )

        if scene_id != beat.get("scene_id"):
            raise AssemblyExecutorError(
                f"asset/beat scene mismatch at index {index}: asset={scene_id}, beat={beat.get('scene_id')}"
            )
        if asset_type != beat.get("requested_asset_type"):
            raise AssemblyExecutorError(
                f"asset/beat type mismatch at index {index}: asset={asset_type}, beat={beat.get('requested_asset_type')}"
            )
        if visual_intent != beat.get("visual_intent"):
            raise AssemblyExecutorError(
                f"asset/beat visual intent mismatch at index {index}"
            )

    return assets


def validate_resolved_assets(
    resolved_payload: dict[str, Any],
    assets: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    asset_count = require_positive_int(
        resolved_payload.get("asset_count"),
        "resolved_assets.asset_count",
    )
    resolved_count = require_non_negative_int(
        resolved_payload.get("resolved_count"),
        "resolved_assets.resolved_count",
    )
    license_cleared_count = require_non_negative_int(
        resolved_payload.get("license_cleared_count"),
        "resolved_assets.license_cleared_count",
    )
    blocked_count = require_non_negative_int(
        resolved_payload.get("blocked_count"),
        "resolved_assets.blocked_count",
    )

    if asset_count != len(assets):
        raise AssemblyExecutorError(
            f"resolved asset_count mismatch: resolved={asset_count}, assets={len(assets)}"
        )
    if resolved_count != asset_count:
        raise AssemblyExecutorError("resolved_assets.resolved_count must equal asset_count")
    if license_cleared_count != asset_count:
        raise AssemblyExecutorError(
            "resolved_assets.license_cleared_count must equal asset_count"
        )
    if blocked_count != 0:
        raise AssemblyExecutorError("resolved_assets.blocked_count must be 0")

    blockers = require_list(resolved_payload.get("blockers"), "resolved_assets.blockers")
    if blockers:
        raise AssemblyExecutorError(f"resolved_assets.blockers must be empty: {blockers}")

    resolved_assets = require_list(
        resolved_payload.get("assets"),
        "resolved_assets.assets",
    )
    if len(resolved_assets) != asset_count:
        raise AssemblyExecutorError(
            f"resolved_assets.assets length mismatch: expected={asset_count}, actual={len(resolved_assets)}"
        )

    result: dict[str, dict[str, Any]] = {}
    for index, resolved in enumerate(resolved_assets, start=1):
        if not isinstance(resolved, dict):
            raise AssemblyExecutorError(
                f"resolved_assets.assets[{index}] must be an object"
            )

        asset_id = require_non_empty_string(
            resolved.get("asset_id"),
            f"resolved_asset[{index}].asset_id",
        )
        if asset_id in result:
            raise AssemblyExecutorError(f"duplicate resolved asset_id: {asset_id}")

        provider_status = require_non_empty_string(
            resolved.get("provider_status"),
            f"{asset_id}.provider_status",
        )
        license_status = require_non_empty_string(
            resolved.get("license_status"),
            f"{asset_id}.license_status",
        )
        resolution_status = require_non_empty_string(
            resolved.get("resolution_status"),
            f"{asset_id}.resolution_status",
        )

        if provider_status != "resolved":
            raise AssemblyExecutorError(f"{asset_id}.provider_status must be resolved")
        if license_status != "cleared":
            raise AssemblyExecutorError(f"{asset_id}.license_status must be cleared")
        if resolution_status != "ready":
            raise AssemblyExecutorError(f"{asset_id}.resolution_status must be ready")

        local_path_string, local_path = resolve_existing_file(
            resolved.get("local_path"),
            f"{asset_id}.local_path",
        )
        extension = local_path.suffix.lower()
        if extension not in ALLOWED_VISUAL_EXTENSIONS:
            raise AssemblyExecutorError(
                f"{asset_id} unsupported visual extension: {extension}"
            )

        normalized = dict(resolved)
        normalized["local_path"] = local_path_string
        result[asset_id] = normalized

    asset_ids = [
        require_non_empty_string(asset.get("asset_id"), "asset.asset_id")
        for asset in assets
    ]
    if set(asset_ids) != set(result):
        missing = sorted(set(asset_ids) - set(result))
        extra = sorted(set(result) - set(asset_ids))
        raise AssemblyExecutorError(
            f"resolved asset identity mismatch: missing={missing}, extra={extra}"
        )

    return result


def validate_audio_render(
    payload: dict[str, Any],
    expected_scene_ids: list[str],
) -> dict[str, dict[str, Any]]:
    if payload.get("audio_status") != "ready":
        raise AssemblyExecutorError("audio_render.audio_status must be ready")
    if require_bool(payload.get("audio_ready"), "audio_render.audio_ready") is not True:
        raise AssemblyExecutorError("audio_render.audio_ready must be true")
    if require_bool(
        payload.get("duration_validated"),
        "audio_render.duration_validated",
    ) is not True:
        raise AssemblyExecutorError("audio_render.duration_validated must be true")

    segment_count = require_positive_int(
        payload.get("segment_count"),
        "audio_render.segment_count",
    )
    rendered_segment_count = require_non_negative_int(
        payload.get("rendered_segment_count"),
        "audio_render.rendered_segment_count",
    )
    failed_segment_count = require_non_negative_int(
        payload.get("failed_segment_count"),
        "audio_render.failed_segment_count",
    )
    if rendered_segment_count != segment_count:
        raise AssemblyExecutorError(
            "audio_render.rendered_segment_count must equal segment_count"
        )
    if failed_segment_count != 0:
        raise AssemblyExecutorError("audio_render.failed_segment_count must be 0")

    segments = require_list(payload.get("segments"), "audio_render.segments")
    if len(segments) != segment_count:
        raise AssemblyExecutorError(
            f"audio_render segment count mismatch: declared={segment_count}, actual={len(segments)}"
        )

    by_scene: dict[str, dict[str, Any]] = {}
    ordered_scene_ids: list[str] = []

    for index, segment in enumerate(segments, start=1):
        if not isinstance(segment, dict):
            raise AssemblyExecutorError(f"audio_render.segments[{index}] must be an object")

        source_scene_id = require_non_empty_string(
            segment.get("source_scene_id"),
            f"audio[{index}].source_scene_id",
        )
        segment_id = require_non_empty_string(
            segment.get("segment_id"),
            f"audio[{index}].segment_id",
        )
        duration_sec = require_positive_number(
            segment.get("duration_sec"),
            f"audio[{index}].duration_sec",
        )
        if require_bool(
            segment.get("duration_validated"),
            f"audio[{index}].duration_validated",
        ) is not True:
            raise AssemblyExecutorError(f"{segment_id}.duration_validated must be true")

        audio_path_string, _ = resolve_existing_file(
            segment.get("audio_path"),
            f"{segment_id}.audio_path",
        )

        if source_scene_id in by_scene:
            raise AssemblyExecutorError(
                f"duplicate audio segment for scene_id={source_scene_id}"
            )

        normalized = dict(segment)
        normalized["audio_path"] = audio_path_string
        normalized["duration_sec"] = round(duration_sec, 3)
        by_scene[source_scene_id] = normalized
        ordered_scene_ids.append(source_scene_id)

    if ordered_scene_ids != expected_scene_ids:
        raise AssemblyExecutorError(
            "audio_render scene mapping must exactly preserve visual pacing scene order"
        )

    return by_scene


def build_scene_timeline(
    *,
    beats: list[dict[str, Any]],
    assets: list[dict[str, Any]],
    resolved_by_asset_id: dict[str, dict[str, Any]],
    audio_by_scene_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    scene_groups: dict[str, dict[str, Any]] = {}
    scene_order: list[str] = []

    for global_index, (beat, asset) in enumerate(zip(beats, assets), start=1):
        scene_id = require_non_empty_string(
            beat.get("scene_id"),
            f"beat[{global_index}].scene_id",
        )
        scene_number = require_positive_int(
            beat.get("scene_order"),
            f"beat[{global_index}].scene_order",
        )
        asset_id = require_non_empty_string(
            asset.get("asset_id"),
            f"asset[{global_index}].asset_id",
        )
        resolved = resolved_by_asset_id[asset_id]

        if scene_id not in scene_groups:
            audio = audio_by_scene_id.get(scene_id)
            if audio is None:
                raise AssemblyExecutorError(f"missing audio segment for scene_id={scene_id}")

            scene_groups[scene_id] = {
                "timeline_id": f"TIMELINE_{scene_id}",
                "scene_id": scene_id,
                "order": scene_number,
                "audio_segment_id": require_non_empty_string(
                    audio.get("segment_id"),
                    f"{scene_id}.audio_segment_id",
                ),
                "audio_path": require_non_empty_string(
                    audio.get("audio_path"),
                    f"{scene_id}.audio_path",
                ),
                "audio_duration_sec": require_positive_number(
                    audio.get("duration_sec"),
                    f"{scene_id}.audio_duration_sec",
                ),
                "visual_segments": [],
            }
            scene_order.append(scene_id)

        item = scene_groups[scene_id]
        if item["order"] != scene_number:
            raise AssemblyExecutorError(
                f"scene order changed within timed beats for {scene_id}"
            )

        visual_segment = {
            "segment_id": f"VISUAL_SEGMENT_{global_index:06d}",
            "beat_id": require_non_empty_string(
                beat.get("beat_id"),
                f"beat[{global_index}].beat_id",
            ),
            "beat_order": require_positive_int(
                beat.get("beat_order"),
                f"beat[{global_index}].beat_order",
            ),
            "source_visual_unit_id": require_non_empty_string(
                beat.get("source_visual_unit_id"),
                f"beat[{global_index}].source_visual_unit_id",
            ),
            "asset_id": asset_id,
            "asset_type": require_non_empty_string(
                resolved.get("asset_type"),
                f"{asset_id}.asset_type",
            ),
            "visual_asset_path": require_non_empty_string(
                resolved.get("local_path"),
                f"{asset_id}.local_path",
            ),
            "visual_intent": require_non_empty_string(
                beat.get("visual_intent"),
                f"beat[{global_index}].visual_intent",
            ),
            "scene_start_sec": require_non_negative_number(
                beat.get("scene_start_sec"),
                f"beat[{global_index}].scene_start_sec",
            ),
            "scene_end_sec": require_positive_number(
                beat.get("scene_end_sec"),
                f"beat[{global_index}].scene_end_sec",
            ),
            "global_start_sec": require_non_negative_number(
                beat.get("global_start_sec"),
                f"beat[{global_index}].global_start_sec",
            ),
            "global_end_sec": require_positive_number(
                beat.get("global_end_sec"),
                f"beat[{global_index}].global_end_sec",
            ),
            "duration_sec": require_positive_number(
                beat.get("beat_duration_sec"),
                f"beat[{global_index}].beat_duration_sec",
            ),
        }

        item["visual_segments"].append(visual_segment)

    timeline: list[dict[str, Any]] = []
    for scene_id in scene_order:
        item = scene_groups[scene_id]
        visual_segments = item["visual_segments"]
        if not visual_segments:
            raise AssemblyExecutorError(f"{scene_id} has no visual segments")

        previous_scene_end = 0.0
        for index, segment in enumerate(visual_segments, start=1):
            start = float(segment["scene_start_sec"])
            end = float(segment["scene_end_sec"])
            duration = float(segment["duration_sec"])
            if abs(start - previous_scene_end) > 0.05:
                raise AssemblyExecutorError(
                    f"{scene_id} visual segment gap/overlap at {index}: "
                    f"start={start}, previous_end={previous_scene_end}"
                )
            if abs((end - start) - duration) > 0.05:
                raise AssemblyExecutorError(
                    f"{scene_id} visual segment duration mismatch at {index}"
                )
            previous_scene_end = end

        if abs(previous_scene_end - float(item["audio_duration_sec"])) > 0.05:
            raise AssemblyExecutorError(
                f"{scene_id} visual/audio duration mismatch: "
                f"visual={previous_scene_end}, audio={item['audio_duration_sec']}"
            )

        item["visual_segment_count"] = len(visual_segments)
        timeline.append(item)

    return sorted(timeline, key=lambda value: value["order"])


def run_assembly_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "ASSEMBLY":
        raise AssemblyExecutorError("ASSEMBLY executor may run only when phase is ASSEMBLY")

    project_id = require_non_empty_string(state.get("project_id"), "project_id")
    artifacts = state.get("artifacts")
    if not isinstance(artifacts, dict):
        raise AssemblyExecutorError("artifacts must be an object")

    required_artifact_keys = (
        "visual_pacing_plan_path",
        "assets_path",
        "resolved_assets_path",
        "audio_render_path",
    )
    artifact_paths: dict[str, Path] = {}
    artifact_strings: dict[str, str] = {}
    for key in required_artifact_keys:
        value, resolved = resolve_existing_file(
            artifacts.get(key),
            f"artifacts.{key}",
        )
        artifact_strings[key] = value
        artifact_paths[key] = resolved

    visual_pacing = read_json_file(artifact_paths["visual_pacing_plan_path"])
    assets_payload = read_json_file(artifact_paths["assets_path"])
    resolved_assets = read_json_file(artifact_paths["resolved_assets_path"])
    audio_render = read_json_file(artifact_paths["audio_render_path"])

    for source_name, payload in (
        ("visual_pacing", visual_pacing),
        ("assets", assets_payload),
        ("resolved_assets", resolved_assets),
        ("audio_render", audio_render),
    ):
        validate_project_id(project_id, payload, source_name)

    beats, scene_count, total_duration_sec = validate_visual_pacing(visual_pacing)
    assets = validate_assets(assets_payload, beats)
    resolved_by_asset_id = validate_resolved_assets(resolved_assets, assets)

    expected_scene_ids: list[str] = []
    for beat in beats:
        scene_id = str(beat["scene_id"])
        if not expected_scene_ids or expected_scene_ids[-1] != scene_id:
            expected_scene_ids.append(scene_id)

    if len(expected_scene_ids) != scene_count:
        raise AssemblyExecutorError(
            f"visual pacing scene identity mismatch: declared={scene_count}, actual={len(expected_scene_ids)}"
        )

    audio_by_scene_id = validate_audio_render(audio_render, expected_scene_ids)

    timeline = build_scene_timeline(
        beats=beats,
        assets=assets,
        resolved_by_asset_id=resolved_by_asset_id,
        audio_by_scene_id=audio_by_scene_id,
    )

    if len(timeline) != scene_count:
        raise AssemblyExecutorError(
            f"assembly timeline scene count mismatch: expected={scene_count}, actual={len(timeline)}"
        )

    visual_segment_count = sum(int(item["visual_segment_count"]) for item in timeline)
    if visual_segment_count != len(beats):
        raise AssemblyExecutorError(
            f"assembly visual segment count mismatch: expected={len(beats)}, actual={visual_segment_count}"
        )

    audio_total_duration = round(
        sum(float(item["audio_duration_sec"]) for item in timeline),
        3,
    )
    if abs(audio_total_duration - total_duration_sec) > 0.05:
        raise AssemblyExecutorError(
            f"assembly total duration mismatch: audio={audio_total_duration}, pacing={total_duration_sec}"
        )

    now = utc_now_iso()
    assembly_plan_path = state_path.parent / "assembly" / "assembly_plan.json"

    assembly_plan = {
        "project_id": project_id,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "source_phase": state["phase"],
        "source_visual_pacing_plan_path": artifact_strings["visual_pacing_plan_path"],
        "source_assets_path": artifact_strings["assets_path"],
        "source_resolved_assets_path": artifact_strings["resolved_assets_path"],
        "source_audio_render_path": artifact_strings["audio_render_path"],
        "timing_source": "actual_canonical_audio",
        "media_source": "resolved_timed_media",
        "assets_ready": True,
        "audio_ready": True,
        "render_ready": False,
        "scene_count": scene_count,
        "beat_count": len(beats),
        "visual_segment_count": visual_segment_count,
        "total_duration_sec": total_duration_sec,
        "timeline": timeline,
        "missing_requirements": ["final render executor"],
        "created_at": now,
        "warnings": [],
        "blockers": [],
    }

    write_json_atomic(assembly_plan_path, assembly_plan)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["assembly_plan_path"] = str(assembly_plan_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "ASSEMBLY_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "assembly_plan_path": str(assembly_plan_path),
        "assets_ready": True,
        "audio_ready": True,
        "render_ready": False,
        "scene_count": scene_count,
        "beat_count": len(beats),
        "visual_segment_count": visual_segment_count,
        "total_duration_sec": total_duration_sec,
        "missing_requirements": ["final render executor"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FlowMind timed-media ASSEMBLY executor"
    )
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
        result = run_assembly_executor(Path(args.state))
    except (AssemblyExecutorError, StateValidationError, OSError) as exc:
        print(f"[ASSEMBLY_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
