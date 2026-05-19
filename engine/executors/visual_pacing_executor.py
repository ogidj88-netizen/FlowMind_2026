from __future__ import annotations

import argparse
import json
import math
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

EXECUTOR_NAME = "visual_pacing_executor"
EXECUTOR_VERSION = "1.0.0"

TARGET_BEAT_DURATION_SEC = 5.0
MIN_BEAT_DURATION_SEC = 3.0
MAX_BEAT_DURATION_SEC = 6.5
DURATION_TOLERANCE_SEC = 0.05

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

VISUAL_ACTIONS = (
    "slow_zoom_in",
    "slow_zoom_out",
    "pan_left",
    "pan_right",
    "crop_focus_left",
    "crop_focus_right",
    "crop_focus_center",
    "text_focus",
    "chart_focus",
    "checklist_focus",
    "hold_safe",
)

MOTION_PROFILES = (
    "ken_burns_subtle",
    "micro_pan",
    "micro_zoom",
    "static_safe",
)

TEXT_MODES = (
    "none",
    "single_focus_line",
    "short_label",
    "number_emphasis",
    "checklist_item_focus",
)


class VisualPacingExecutorError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualPacingExecutorError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualPacingExecutorError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise VisualPacingExecutorError(f"JSON file must contain an object: {path}")

    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(path)


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise VisualPacingExecutorError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise VisualPacingExecutorError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise VisualPacingExecutorError(f"{field_name} must be an integer")

    if value <= 0:
        raise VisualPacingExecutorError(f"{field_name} must be > 0")

    return value


def require_positive_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise VisualPacingExecutorError(f"{field_name} must be a number")

    if not isinstance(value, (int, float)):
        raise VisualPacingExecutorError(f"{field_name} must be a number")

    normalized = float(value)
    if normalized <= 0:
        raise VisualPacingExecutorError(f"{field_name} must be > 0")

    return normalized


def require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise VisualPacingExecutorError(f"{field_name} must be boolean")

    return value


def require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise VisualPacingExecutorError(f"{field_name} must be a list")

    return value


def fail_if_forbidden_markers(value: str, source_name: str) -> None:
    upper_value = value.upper()
    hits = [marker for marker in FORBIDDEN_MARKERS if marker in upper_value]
    if hits:
        raise VisualPacingExecutorError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def ensure_existing_file(path_value: Any, field_name: str) -> str:
    path_string = require_non_empty_string(path_value, field_name)
    path = Path(path_string)

    if not path.exists():
        raise VisualPacingExecutorError(f"{field_name} does not exist: {path_string}")

    if not path.is_file():
        raise VisualPacingExecutorError(f"{field_name} must be a file: {path_string}")

    if path.stat().st_size <= 0:
        raise VisualPacingExecutorError(f"{field_name} must be non-empty: {path_string}")

    return path_string


def validate_project_ids(project_id: str, payloads: list[tuple[str, dict[str, Any]]]) -> None:
    for name, payload in payloads:
        payload_project_id = require_non_empty_string(payload.get("project_id"), f"{name}.project_id")
        if payload_project_id != project_id:
            raise VisualPacingExecutorError(
                f"project_id mismatch: state={project_id}, {name}={payload_project_id}"
            )


def validate_preconditions(
    state: dict[str, Any],
    assembly_plan: dict[str, Any],
    audio_render: dict[str, Any],
    final_render_report: dict[str, Any],
    artifacts: dict[str, Any],
) -> None:
    phase = require_non_empty_string(state.get("phase"), "PROJECT_STATE.phase")
    if phase != "QA":
        raise VisualPacingExecutorError(f"PROJECT_STATE.phase must be QA, got {phase}")

    if require_bool(assembly_plan.get("assets_ready"), "assembly_plan.assets_ready") is not True:
        raise VisualPacingExecutorError("assembly_plan.assets_ready must be true")

    if require_bool(assembly_plan.get("audio_ready"), "assembly_plan.audio_ready") is not True:
        raise VisualPacingExecutorError("assembly_plan.audio_ready must be true")

    if require_bool(assembly_plan.get("render_ready"), "assembly_plan.render_ready") is not True:
        raise VisualPacingExecutorError("assembly_plan.render_ready must be true")

    audio_status = require_non_empty_string(audio_render.get("audio_status"), "audio_render.audio_status")
    if audio_status != "ready":
        raise VisualPacingExecutorError(f"audio_render.audio_status must be ready, got {audio_status}")

    if require_bool(audio_render.get("audio_ready"), "audio_render.audio_ready") is not True:
        raise VisualPacingExecutorError("audio_render.audio_ready must be true")

    if require_bool(audio_render.get("duration_validated"), "audio_render.duration_validated") is not True:
        raise VisualPacingExecutorError("audio_render.duration_validated must be true")

    if require_bool(audio_render.get("loudness_validated"), "audio_render.loudness_validated") is not True:
        raise VisualPacingExecutorError("audio_render.loudness_validated must be true")

    verdict = require_non_empty_string(
        final_render_report.get("verdict"),
        "final_render_report.verdict",
    )
    if verdict != "PASS":
        raise VisualPacingExecutorError(f"final_render_report.verdict must be PASS, got {verdict}")

    ensure_existing_file(artifacts.get("final_video_path"), "PROJECT_STATE.artifacts.final_video_path")


def build_by_key(items: list[Any], key_name: str, source_name: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise VisualPacingExecutorError(f"{source_name}[{index}] must be an object")

        key = require_non_empty_string(item.get(key_name), f"{source_name}[{index}].{key_name}")
        if key in result:
            raise VisualPacingExecutorError(f"duplicate {source_name}.{key_name}: {key}")

        result[key] = item

    return result


def choose_visual_action(beat_order: int, asset_type: str, text_mode: str) -> str:
    if text_mode in {"number_emphasis", "checklist_item_focus"}:
        return "text_focus"

    if "chart" in asset_type.lower():
        return "chart_focus"

    if "checklist" in asset_type.lower():
        return "checklist_focus"

    sequence = (
        "slow_zoom_in",
        "crop_focus_center",
        "pan_left",
        "slow_zoom_out",
        "pan_right",
        "crop_focus_right",
        "crop_focus_left",
    )
    return sequence[(beat_order - 1) % len(sequence)]


def choose_motion_profile(visual_action: str) -> str:
    if visual_action in {"slow_zoom_in", "slow_zoom_out"}:
        return "ken_burns_subtle"

    if visual_action in {"pan_left", "pan_right"}:
        return "micro_pan"

    if visual_action.startswith("crop_focus"):
        return "micro_zoom"

    return "static_safe"


def first_sentence(value: str) -> str:
    normalized = " ".join(value.strip().split())
    if not normalized:
        return ""

    for separator in (". ", "? ", "! "):
        if separator in normalized:
            return normalized.split(separator, 1)[0].strip() + separator.strip()

    return normalized


def shorten_to_words(value: str, max_words: int) -> str:
    words = value.strip().split()
    if len(words) <= max_words:
        return " ".join(words)

    return " ".join(words[:max_words])


def select_display_text(scene: dict[str, Any], beat_order: int) -> tuple[str, str]:
    on_screen_text = scene.get("on_screen_text")
    voiceover_text = require_non_empty_string(scene.get("voiceover_text"), "scene.voiceover_text")

    if beat_order == 1 and isinstance(on_screen_text, str) and on_screen_text.strip():
        text = shorten_to_words(on_screen_text, 12)
        if text:
            return text, "single_focus_line"

    sentence = first_sentence(voiceover_text)
    text = shorten_to_words(sentence, 12)

    if beat_order == 1 and text:
        return text, "single_focus_line"

    if beat_order % 3 == 0:
        return "", "none"

    if text:
        return text, "short_label"

    return "", "none"


def split_duration(duration_sec: float) -> list[float]:
    if duration_sec <= 7.0:
        return [round(duration_sec, 3)]

    beat_count = max(1, int(math.ceil(duration_sec / TARGET_BEAT_DURATION_SEC)))
    beat_duration = duration_sec / beat_count

    while beat_duration < MIN_BEAT_DURATION_SEC and beat_count > 1:
        beat_count -= 1
        beat_duration = duration_sec / beat_count

    while beat_duration > MAX_BEAT_DURATION_SEC:
        beat_count += 1
        beat_duration = duration_sec / beat_count

    durations = [round(beat_duration, 3) for _ in range(beat_count)]
    drift = round(duration_sec - sum(durations), 3)
    durations[-1] = round(durations[-1] + drift, 3)

    if len(durations) > 1 and durations[-1] < MIN_BEAT_DURATION_SEC:
        tail = durations.pop()
        durations[-1] = round(durations[-1] + tail, 3)

    return durations


def build_beats(
    timeline: list[Any],
    scenes_by_id: dict[str, dict[str, Any]],
    assets_by_scene_id: dict[str, dict[str, Any]],
    audio_by_scene_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    beats: list[dict[str, Any]] = []
    global_cursor = 0.0

    for timeline_index, timeline_item in enumerate(timeline, start=1):
        if not isinstance(timeline_item, dict):
            raise VisualPacingExecutorError(f"timeline[{timeline_index}] must be an object")

        scene_id = require_non_empty_string(
            timeline_item.get("scene_id"),
            f"timeline[{timeline_index}].scene_id",
        )
        timeline_id = require_non_empty_string(
            timeline_item.get("timeline_id"),
            f"timeline[{timeline_index}].timeline_id",
        )
        asset_id = require_non_empty_string(
            timeline_item.get("asset_id"),
            f"timeline[{timeline_index}].asset_id",
        )
        order = require_positive_int(timeline_item.get("order"), f"timeline[{timeline_index}].order")

        if scene_id not in scenes_by_id:
            raise VisualPacingExecutorError(f"missing scene for timeline scene_id={scene_id}")

        if scene_id not in assets_by_scene_id:
            raise VisualPacingExecutorError(f"missing resolved asset for scene_id={scene_id}")

        if scene_id not in audio_by_scene_id:
            raise VisualPacingExecutorError(f"missing audio render segment for scene_id={scene_id}")

        scene = scenes_by_id[scene_id]
        asset = assets_by_scene_id[scene_id]
        audio = audio_by_scene_id[scene_id]

        resolved_asset_id = require_non_empty_string(asset.get("asset_id"), f"asset[{scene_id}].asset_id")
        if resolved_asset_id != asset_id:
            raise VisualPacingExecutorError(
                f"asset mismatch for {scene_id}: timeline={asset_id}, resolved={resolved_asset_id}"
            )

        audio_segment_id = require_non_empty_string(audio.get("segment_id"), f"audio[{scene_id}].segment_id")
        source_visual_path = ensure_existing_file(asset.get("local_path"), f"asset[{scene_id}].local_path")
        source_audio_path = ensure_existing_file(audio.get("audio_path"), f"audio[{scene_id}].audio_path")
        duration_sec = require_positive_number(audio.get("duration_sec"), f"audio[{scene_id}].duration_sec")
        asset_type = require_non_empty_string(asset.get("asset_type"), f"asset[{scene_id}].asset_type")

        scene_cursor = 0.0
        beat_durations = split_duration(duration_sec)

        for beat_index, beat_duration in enumerate(beat_durations, start=1):
            scene_start = round(scene_cursor, 3)
            scene_end = round(scene_cursor + beat_duration, 3)
            global_start = round(global_cursor, 3)
            global_end = round(global_cursor + beat_duration, 3)

            if beat_index == len(beat_durations):
                scene_end = round(duration_sec, 3)

            display_text, text_mode = select_display_text(scene, beat_index)
            visual_action = choose_visual_action(beat_index, asset_type, text_mode)
            motion_profile = choose_motion_profile(visual_action)

            beat = {
                "asset_id": asset_id,
                "audio_segment_id": audio_segment_id,
                "beat_duration_sec": round(scene_end - scene_start, 3),
                "beat_id": f"{scene_id}_BEAT_{beat_index:03d}",
                "beat_order": beat_index,
                "display_text": display_text,
                "global_end_sec": global_end,
                "global_start_sec": global_start,
                "motion_profile": motion_profile,
                "order": order,
                "render_instruction": {
                    "ffmpeg_safe": True,
                    "requires_ai_generation": False,
                    "requires_external_provider": False,
                    "requires_new_asset": False,
                    "safe_margin_percent": 10,
                },
                "scene_end_sec": scene_end,
                "scene_id": scene_id,
                "scene_start_sec": scene_start,
                "source_audio_path": source_audio_path,
                "source_visual_path": source_visual_path,
                "text_mode": text_mode,
                "timeline_id": timeline_id,
                "visual_action": visual_action,
            }

            fail_if_forbidden_markers(json.dumps(beat, ensure_ascii=False), beat["beat_id"])
            beats.append(beat)

            scene_cursor = scene_end
            global_cursor = global_end

        scene_duration_delta = abs(round(scene_cursor - duration_sec, 3))
        if scene_duration_delta > DURATION_TOLERANCE_SEC:
            raise VisualPacingExecutorError(
                f"scene duration mismatch for {scene_id}: beats={scene_cursor}, audio={duration_sec}"
            )

    return beats


def validate_beats(beats: list[dict[str, Any]], expected_scene_count: int) -> None:
    if len(beats) <= expected_scene_count:
        raise VisualPacingExecutorError(
            f"beat_count must be greater than scene_count: beats={len(beats)}, scenes={expected_scene_count}"
        )

    previous_end = 0.0
    for index, beat in enumerate(beats, start=1):
        global_start = require_positive_number(
            beat.get("global_start_sec") if beat.get("global_start_sec") != 0 else 0.001,
            f"beats[{index}].global_start_sec",
        )
        global_start = 0.0 if beat.get("global_start_sec") == 0 else global_start

        global_end = require_positive_number(beat.get("global_end_sec"), f"beats[{index}].global_end_sec")

        if abs(global_start - previous_end) > DURATION_TOLERANCE_SEC:
            raise VisualPacingExecutorError(
                f"global timing gap or overlap at beat {index}: start={global_start}, previous_end={previous_end}"
            )

        if global_end <= global_start:
            raise VisualPacingExecutorError(f"beat {index} global_end_sec must be > global_start_sec")

        previous_end = global_end


def run_visual_pacing_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    project_id = require_non_empty_string(state.get("project_id"), "PROJECT_STATE.project_id")
    artifacts = state.get("artifacts", {})
    if not isinstance(artifacts, dict):
        raise VisualPacingExecutorError("PROJECT_STATE.artifacts must be an object")

    assembly_plan_path = Path(
        require_non_empty_string(artifacts.get("assembly_plan_path"), "artifacts.assembly_plan_path")
    )
    resolved_assets_path = Path(
        require_non_empty_string(artifacts.get("resolved_assets_path"), "artifacts.resolved_assets_path")
    )
    audio_render_path = Path(
        require_non_empty_string(artifacts.get("audio_render_path"), "artifacts.audio_render_path")
    )
    scenes_path = Path(
        require_non_empty_string(artifacts.get("scenes_path"), "artifacts.scenes_path")
    )
    final_render_report_path = Path(
        require_non_empty_string(
            artifacts.get("final_render_report_path"),
            "artifacts.final_render_report_path",
        )
    )

    assembly_plan = read_json_file(assembly_plan_path)
    resolved_assets = read_json_file(resolved_assets_path)
    audio_render = read_json_file(audio_render_path)
    scenes_payload = read_json_file(scenes_path)
    final_render_report = read_json_file(final_render_report_path)

    validate_project_ids(
        project_id,
        [
            ("assembly_plan", assembly_plan),
            ("resolved_assets", resolved_assets),
            ("audio_render", audio_render),
            ("scenes", scenes_payload),
            ("final_render_report", final_render_report),
        ],
    )

    validate_preconditions(
        state=state,
        assembly_plan=assembly_plan,
        audio_render=audio_render,
        final_render_report=final_render_report,
        artifacts=artifacts,
    )

    timeline = require_list(assembly_plan.get("timeline"), "assembly_plan.timeline")
    scenes = require_list(scenes_payload.get("scenes"), "scenes.scenes")
    assets = require_list(resolved_assets.get("assets"), "resolved_assets.assets")
    audio_segments = require_list(audio_render.get("segments"), "audio_render.segments")

    scene_count = require_positive_int(assembly_plan.get("scene_count"), "assembly_plan.scene_count")
    if scene_count != len(timeline):
        raise VisualPacingExecutorError("assembly_plan.scene_count must match timeline length")

    scenes_by_id = build_by_key(scenes, "scene_id", "scenes")
    assets_by_scene_id = build_by_key(assets, "scene_id", "resolved_assets")
    audio_by_scene_id = build_by_key(audio_segments, "source_scene_id", "audio_render.segments")

    beats = build_beats(
        timeline=timeline,
        scenes_by_id=scenes_by_id,
        assets_by_scene_id=assets_by_scene_id,
        audio_by_scene_id=audio_by_scene_id,
    )
    validate_beats(beats, scene_count)

    total_duration_sec = round(sum(beat["beat_duration_sec"] for beat in beats), 3)
    source_audio_duration_sec = require_positive_number(
        audio_render.get("total_duration_sec"),
        "audio_render.total_duration_sec",
    )
    duration_delta_sec = round(total_duration_sec - source_audio_duration_sec, 3)

    if abs(duration_delta_sec) > DURATION_TOLERANCE_SEC:
        raise VisualPacingExecutorError(
            f"total duration mismatch: beats={total_duration_sec}, audio={source_audio_duration_sec}"
        )

    now = utc_now_iso()
    visual_pacing_dir = state_path.parent / "visual_pacing"
    visual_pacing_plan_path = visual_pacing_dir / "visual_pacing_plan.json"

    visual_pacing_plan = {
        "audio_master_clock": True,
        "beat_count": len(beats),
        "beats": beats,
        "blockers": [],
        "created_at": now,
        "duration_delta_sec": duration_delta_sec,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "layer": "visual_pacing",
        "layer_version": EXECUTOR_VERSION,
        "max_beat_duration_sec": MAX_BEAT_DURATION_SEC,
        "min_beat_duration_sec": MIN_BEAT_DURATION_SEC,
        "project_id": project_id,
        "scene_count": scene_count,
        "source_assembly_plan_path": str(assembly_plan_path),
        "source_audio_render_path": str(audio_render_path),
        "source_audio_duration_sec": source_audio_duration_sec,
        "source_final_render_report_path": str(final_render_report_path),
        "source_phase": state["phase"],
        "source_resolved_assets_path": str(resolved_assets_path),
        "source_scenes_path": str(scenes_path),
        "status": "VISUAL_PACING_PLAN_OK",
        "target_beat_duration_sec": TARGET_BEAT_DURATION_SEC,
        "total_duration_sec": total_duration_sec,
        "warnings": [],
    }

    serialized = json.dumps(visual_pacing_plan, ensure_ascii=False)
    fail_if_forbidden_markers(serialized, "visual_pacing_plan")

    write_json_atomic(visual_pacing_plan_path, visual_pacing_plan)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["visual_pacing_plan_path"] = str(visual_pacing_plan_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "beat_count": len(beats),
        "duration_delta_sec": duration_delta_sec,
        "phase": saved_state["phase"],
        "project_id": project_id,
        "scene_count": scene_count,
        "status": "VISUAL_PACING_EXECUTOR_OK",
        "total_duration_sec": total_duration_sec,
        "visual_pacing_plan_path": str(visual_pacing_plan_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind visual pacing executor v1")
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
        result = run_visual_pacing_executor(Path(args.state))
    except (VisualPacingExecutorError, StateValidationError, OSError) as exc:
        print(f"[VISUAL_PACING_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
