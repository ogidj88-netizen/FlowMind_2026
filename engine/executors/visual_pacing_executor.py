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
EXECUTOR_VERSION = "2.1.0"

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


def require_non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise VisualPacingExecutorError(f"{field_name} must be an integer")

    if value < 0:
        raise VisualPacingExecutorError(f"{field_name} must be >= 0")

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


def resolve_existing_file(path_value: Any, field_name: str) -> tuple[str, Path]:
    path_string = require_non_empty_string(path_value, field_name)
    supplied_path = Path(path_string)
    resolved_path = supplied_path if supplied_path.is_absolute() else REPO_ROOT / supplied_path

    if not resolved_path.exists():
        raise VisualPacingExecutorError(f"{field_name} does not exist: {path_string}")

    if not resolved_path.is_file():
        raise VisualPacingExecutorError(f"{field_name} must be a file: {path_string}")

    if resolved_path.stat().st_size <= 0:
        raise VisualPacingExecutorError(f"{field_name} must be non-empty: {path_string}")

    return path_string, resolved_path


def validate_project_ids(project_id: str, payloads: list[tuple[str, dict[str, Any]]]) -> None:
    for name, payload in payloads:
        payload_project_id = require_non_empty_string(payload.get("project_id"), f"{name}.project_id")
        if payload_project_id != project_id:
            raise VisualPacingExecutorError(
                f"project_id mismatch: state={project_id}, {name}={payload_project_id}"
            )


def validate_scene(scene: dict[str, Any], index: int) -> None:
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

    missing = sorted(required_fields - set(scene.keys()))
    if missing:
        raise VisualPacingExecutorError(
            f"scene index {index} missing fields: {', '.join(missing)}"
        )

    require_non_empty_string(scene["scene_id"], f"scene[{index}].scene_id")
    require_positive_int(scene["order"], f"scene[{index}].order")
    require_non_empty_string(scene["voiceover_text"], f"scene[{index}].voiceover_text")
    require_non_empty_string(scene["visual_intent"], f"scene[{index}].visual_intent")
    require_non_empty_string(scene["on_screen_text"], f"scene[{index}].on_screen_text")
    require_non_empty_string(scene["asset_type"], f"scene[{index}].asset_type")
    require_positive_int(scene["estimated_duration_sec"], f"scene[{index}].estimated_duration_sec")
    require_non_empty_string(scene["production_notes"], f"scene[{index}].production_notes")

    fail_if_forbidden_markers(json.dumps(scene, ensure_ascii=False), f"scene[{index}]")



def validate_visual_units(scene: dict[str, Any], scene_index: int) -> list[dict[str, Any]]:
    scene_id = require_non_empty_string(
        scene.get("scene_id"),
        f"scene[{scene_index}].scene_id",
    )
    raw_units = require_list(
        scene.get("visual_units"),
        f"scene[{scene_index}].visual_units",
    )
    if not raw_units:
        raise VisualPacingExecutorError(
            f"scene[{scene_index}].visual_units must not be empty"
        )

    validated: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for unit_index, unit in enumerate(raw_units, start=1):
        if not isinstance(unit, dict):
            raise VisualPacingExecutorError(
                f"scene[{scene_index}].visual_units[{unit_index}] must be an object"
            )

        unit_id = require_non_empty_string(
            unit.get("unit_id"),
            f"scene[{scene_index}].visual_units[{unit_index}].unit_id",
        )
        if unit_id in seen_ids:
            raise VisualPacingExecutorError(
                f"duplicate visual unit id in {scene_id}: {unit_id}"
            )
        seen_ids.add(unit_id)

        source_scene_id = require_non_empty_string(
            unit.get("source_scene_id"),
            f"{unit_id}.source_scene_id",
        )
        if source_scene_id != scene_id:
            raise VisualPacingExecutorError(
                f"{unit_id}.source_scene_id mismatch: expected={scene_id}, got={source_scene_id}"
            )

        require_non_empty_string(unit.get("purpose"), f"{unit_id}.purpose")
        require_non_empty_string(unit.get("visual_intent"), f"{unit_id}.visual_intent")
        require_non_empty_string(unit.get("asset_type"), f"{unit_id}.asset_type")
        require_non_empty_string(
            unit.get("representation_mode"),
            f"{unit_id}.representation_mode",
        )
        require_non_empty_string(
            unit.get("production_priority"),
            f"{unit_id}.production_priority",
        )
        require_non_empty_string(
            unit.get("overlay_intent"),
            f"{unit_id}.overlay_intent",
        )

        must_show = require_list(unit.get("must_show"), f"{unit_id}.must_show")
        must_not_show = require_list(unit.get("must_not_show"), f"{unit_id}.must_not_show")
        for item_index, item in enumerate(must_show, start=1):
            require_non_empty_string(item, f"{unit_id}.must_show[{item_index}]")
        for item_index, item in enumerate(must_not_show, start=1):
            require_non_empty_string(item, f"{unit_id}.must_not_show[{item_index}]")

        fail_if_forbidden_markers(
            json.dumps(unit, ensure_ascii=False),
            unit_id,
        )
        validated.append(unit)

    return validated


def allocate_visual_units_to_beats(
    visual_units: list[dict[str, Any]],
    beat_count: int,
) -> list[dict[str, Any]]:
    if beat_count <= 0:
        raise VisualPacingExecutorError("beat_count must be > 0")
    if not visual_units:
        raise VisualPacingExecutorError("visual_units must not be empty")

    unit_count = len(visual_units)

    if unit_count == 1:
        return [visual_units[0] for _ in range(beat_count)]

    if beat_count == 1:
        return [visual_units[0]]

    assignments: list[dict[str, Any]] = []
    for beat_index in range(beat_count):
        unit_index = min(
            unit_count - 1,
            int((beat_index * unit_count) / beat_count),
        )
        assignments.append(visual_units[unit_index])

    return assignments

def validate_audio_segment(segment: dict[str, Any], index: int) -> None:
    required_fields = {
        "segment_id",
        "source_scene_id",
        "order",
        "tts_status",
        "audio_path",
        "duration_sec",
        "duration_validated",
        "provider_status",
    }

    missing = sorted(required_fields - set(segment.keys()))
    if missing:
        raise VisualPacingExecutorError(
            f"audio segment index {index} missing fields: {', '.join(missing)}"
        )

    require_non_empty_string(segment["segment_id"], f"audio[{index}].segment_id")
    require_non_empty_string(segment["source_scene_id"], f"audio[{index}].source_scene_id")
    require_positive_int(segment["order"], f"audio[{index}].order")

    tts_status = require_non_empty_string(segment["tts_status"], f"audio[{index}].tts_status")
    if tts_status != "rendered":
        raise VisualPacingExecutorError(
            f"audio[{index}].tts_status must be rendered, got {tts_status}"
        )

    provider_status = require_non_empty_string(
        segment["provider_status"],
        f"audio[{index}].provider_status",
    )
    if provider_status != "rendered":
        raise VisualPacingExecutorError(
            f"audio[{index}].provider_status must be rendered, got {provider_status}"
        )

    if require_bool(segment["duration_validated"], f"audio[{index}].duration_validated") is not True:
        raise VisualPacingExecutorError(
            f"audio[{index}].duration_validated must be true"
        )

    require_positive_number(segment["duration_sec"], f"audio[{index}].duration_sec")
    resolve_existing_file(segment["audio_path"], f"audio[{index}].audio_path")
    fail_if_forbidden_markers(json.dumps(segment, ensure_ascii=False), f"audio[{index}]")


def build_by_key(
    items: list[Any],
    key_name: str,
    source_name: str,
) -> dict[str, dict[str, Any]]:
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

    if "checklist" in asset_type.lower() or "screen" in asset_type.lower():
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


def split_sentences(value: str) -> list[str]:
    normalized = " ".join(value.strip().split())
    if not normalized:
        return []

    sentences: list[str] = []
    current = ""

    for char in normalized:
        current += char
        if char in ".?!":
            candidate = current.strip()
            if candidate:
                sentences.append(candidate)
            current = ""

    tail = current.strip()
    if tail:
        sentences.append(tail)

    return sentences


def shorten_to_words(value: str, max_words: int) -> str:
    words = value.strip().split()
    if len(words) <= max_words:
        return " ".join(words)

    return " ".join(words[:max_words])


def select_display_text(scene: dict[str, Any], beat_order: int) -> tuple[str, str]:
    on_screen_text = scene.get("on_screen_text")
    voiceover_text = require_non_empty_string(scene.get("voiceover_text"), "scene.voiceover_text")
    sentences = split_sentences(voiceover_text)

    if beat_order == 1 and isinstance(on_screen_text, str) and on_screen_text.strip():
        text = shorten_to_words(on_screen_text, 10)
        if text:
            return text, "single_focus_line"

    if beat_order % 2 == 0:
        return "", "none"

    if sentences:
        sentence_index = max(0, min(len(sentences) - 1, beat_order // 2))
        text = shorten_to_words(sentences[sentence_index], 10)
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
    scenes: list[dict[str, Any]],
    audio_by_scene_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    beats: list[dict[str, Any]] = []
    global_cursor = 0.0

    for scene_index, scene in enumerate(scenes, start=1):
        validate_scene(scene, scene_index)

        scene_id = require_non_empty_string(scene["scene_id"], f"scene[{scene_index}].scene_id")
        scene_order = require_positive_int(scene["order"], f"scene[{scene_index}].order")

        if scene_id not in audio_by_scene_id:
            raise VisualPacingExecutorError(f"missing audio render segment for scene_id={scene_id}")

        audio = audio_by_scene_id[scene_id]
        audio_segment_id = require_non_empty_string(
            audio.get("segment_id"),
            f"audio[{scene_id}].segment_id",
        )
        source_audio_path, _ = resolve_existing_file(
            audio.get("audio_path"),
            f"audio[{scene_id}].audio_path",
        )
        duration_sec = require_positive_number(
            audio.get("duration_sec"),
            f"audio[{scene_id}].duration_sec",
        )

        production_notes = require_non_empty_string(
            scene.get("production_notes"),
            f"scene[{scene_index}].production_notes",
        )
        visual_units = validate_visual_units(scene, scene_index)

        scene_cursor = 0.0
        beat_durations = split_duration(duration_sec)
        unit_assignments = allocate_visual_units_to_beats(
            visual_units,
            len(beat_durations),
        )

        for beat_index, (beat_duration, visual_unit) in enumerate(
            zip(beat_durations, unit_assignments),
            start=1,
        ):
            scene_start = round(scene_cursor, 3)
            scene_end = round(scene_cursor + beat_duration, 3)
            global_start = round(global_cursor, 3)
            global_end = round(global_cursor + beat_duration, 3)

            if beat_index == len(beat_durations):
                scene_end = round(duration_sec, 3)
                global_end = round(global_start + (scene_end - scene_start), 3)

            visual_unit_id = require_non_empty_string(
                visual_unit.get("unit_id"),
                f"{scene_id}.beat[{beat_index}].visual_unit_id",
            )
            asset_type = require_non_empty_string(
                visual_unit.get("asset_type"),
                f"{visual_unit_id}.asset_type",
            )
            visual_intent = require_non_empty_string(
                visual_unit.get("visual_intent"),
                f"{visual_unit_id}.visual_intent",
            )
            representation_mode = require_non_empty_string(
                visual_unit.get("representation_mode"),
                f"{visual_unit_id}.representation_mode",
            )
            production_priority = require_non_empty_string(
                visual_unit.get("production_priority"),
                f"{visual_unit_id}.production_priority",
            )
            purpose = require_non_empty_string(
                visual_unit.get("purpose"),
                f"{visual_unit_id}.purpose",
            )
            overlay_intent = require_non_empty_string(
                visual_unit.get("overlay_intent"),
                f"{visual_unit_id}.overlay_intent",
            )

            display_text, text_mode = select_display_text(scene, beat_index)
            visual_action = choose_visual_action(beat_index, asset_type, text_mode)
            motion_profile = choose_motion_profile(visual_action)

            beat = {
                "audio_segment_id": audio_segment_id,
                "beat_duration_sec": round(scene_end - scene_start, 3),
                "beat_id": f"{scene_id}_BEAT_{beat_index:03d}",
                "beat_order": beat_index,
                "display_text": display_text,
                "global_end_sec": global_end,
                "global_start_sec": global_start,
                "motion_profile": motion_profile,
                "requested_asset_type": asset_type,
                "scene_end_sec": scene_end,
                "scene_id": scene_id,
                "scene_order": scene_order,
                "scene_start_sec": scene_start,
                "source_audio_path": source_audio_path,
                "source_visual_unit_id": visual_unit_id,
                "text_mode": text_mode,
                "visual_action": visual_action,
                "visual_intent": visual_intent,
                "visual_purpose": purpose,
                "representation_mode": representation_mode,
                "production_priority": production_priority,
                "must_show": list(visual_unit["must_show"]),
                "must_not_show": list(visual_unit["must_not_show"]),
                "overlay_intent": overlay_intent,
                "production_notes": production_notes,
                "render_instruction": {
                    "ffmpeg_safe": True,
                    "requires_ai_generation": False,
                    "requires_external_provider": False,
                    "requires_new_asset": True,
                    "safe_margin_percent": 10,
                },
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



def validate_beats(
    beats: list[dict[str, Any]],
    scenes: list[dict[str, Any]],
) -> None:
    if not beats:
        raise VisualPacingExecutorError("beats must not be empty")

    scene_ids = [
        require_non_empty_string(scene.get("scene_id"), f"scenes[{index}].scene_id")
        for index, scene in enumerate(scenes, start=1)
    ]
    beat_scene_ids = {
        require_non_empty_string(beat.get("scene_id"), f"beats[{index}].scene_id")
        for index, beat in enumerate(beats, start=1)
    }

    missing_scene_ids = [scene_id for scene_id in scene_ids if scene_id not in beat_scene_ids]
    if missing_scene_ids:
        raise VisualPacingExecutorError(
            f"scenes without timed beats: {', '.join(missing_scene_ids)}"
        )

    previous_end = 0.0

    for index, beat in enumerate(beats, start=1):
        raw_global_start = beat.get("global_start_sec")
        if raw_global_start == 0:
            global_start = 0.0
        else:
            global_start = require_positive_number(
                raw_global_start,
                f"beats[{index}].global_start_sec",
            )

        global_end = require_positive_number(
            beat.get("global_end_sec"),
            f"beats[{index}].global_end_sec",
        )

        if abs(global_start - previous_end) > DURATION_TOLERANCE_SEC:
            raise VisualPacingExecutorError(
                f"global timing gap or overlap at beat {index}: "
                f"start={global_start}, previous_end={previous_end}"
            )

        if global_end <= global_start:
            raise VisualPacingExecutorError(
                f"beat {index} global_end_sec must be > global_start_sec"
            )

        previous_end = global_end


def validate_audio_render(
    audio_render: dict[str, Any],
    scenes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    segment_count = require_positive_int(
        audio_render.get("segment_count"),
        "audio_render.segment_count",
    )
    rendered_segment_count = require_non_negative_int(
        audio_render.get("rendered_segment_count"),
        "audio_render.rendered_segment_count",
    )
    failed_segment_count = require_non_negative_int(
        audio_render.get("failed_segment_count"),
        "audio_render.failed_segment_count",
    )

    if rendered_segment_count != segment_count:
        raise VisualPacingExecutorError(
            "audio_render must contain all rendered segments before exact timed execution"
        )

    if failed_segment_count != 0:
        raise VisualPacingExecutorError(
            f"audio_render.failed_segment_count must be 0, got {failed_segment_count}"
        )

    if require_bool(
        audio_render.get("duration_validated"),
        "audio_render.duration_validated",
    ) is not True:
        raise VisualPacingExecutorError("audio_render.duration_validated must be true")

    audio_segments = require_list(audio_render.get("segments"), "audio_render.segments")
    if len(audio_segments) != segment_count:
        raise VisualPacingExecutorError(
            f"audio segment count mismatch: declared={segment_count}, actual={len(audio_segments)}"
        )

    for index, segment in enumerate(audio_segments, start=1):
        if not isinstance(segment, dict):
            raise VisualPacingExecutorError(f"audio_render.segments[{index}] must be an object")
        validate_audio_segment(segment, index)

    scene_ids = [
        require_non_empty_string(scene.get("scene_id"), f"scenes[{index}].scene_id")
        for index, scene in enumerate(scenes, start=1)
    ]
    audio_scene_ids = [
        require_non_empty_string(
            segment.get("source_scene_id"),
            f"audio_render.segments[{index}].source_scene_id",
        )
        for index, segment in enumerate(audio_segments, start=1)
    ]

    if scene_ids != audio_scene_ids:
        raise VisualPacingExecutorError(
            "audio_render segment mapping must exactly preserve scene order"
        )

    return audio_segments


def run_visual_pacing_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    phase = require_non_empty_string(state.get("phase"), "PROJECT_STATE.phase")
    if phase != "SCENES":
        raise VisualPacingExecutorError(
            f"visual_pacing_executor may run only when phase is SCENES, got {phase}"
        )

    project_id = require_non_empty_string(
        state.get("project_id"),
        "PROJECT_STATE.project_id",
    )
    artifacts = state.get("artifacts", {})
    if not isinstance(artifacts, dict):
        raise VisualPacingExecutorError("PROJECT_STATE.artifacts must be an object")

    scenes_path = Path(
        require_non_empty_string(
            artifacts.get("scenes_path"),
            "artifacts.scenes_path",
        )
    )
    audio_render_path = Path(
        require_non_empty_string(
            artifacts.get("audio_render_path"),
            "artifacts.audio_render_path",
        )
    )

    scenes_payload = read_json_file(scenes_path)
    audio_render = read_json_file(audio_render_path)

    validate_project_ids(
        project_id,
        [
            ("scenes", scenes_payload),
            ("audio_render", audio_render),
        ],
    )

    scene_count = require_positive_int(
        scenes_payload.get("scene_count"),
        "scenes.scene_count",
    )
    scenes = require_list(scenes_payload.get("scenes"), "scenes.scenes")

    if scene_count != len(scenes):
        raise VisualPacingExecutorError(
            f"scene_count mismatch: declared={scene_count}, actual={len(scenes)}"
        )

    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            raise VisualPacingExecutorError(f"scenes[{index}] must be an object")
        validate_scene(scene, index)

    audio_segments = validate_audio_render(audio_render, scenes)
    audio_by_scene_id = build_by_key(
        audio_segments,
        "source_scene_id",
        "audio_render.segments",
    )

    beats = build_beats(
        scenes=scenes,
        audio_by_scene_id=audio_by_scene_id,
    )
    validate_beats(beats, scenes)

    total_duration_sec = round(
        sum(beat["beat_duration_sec"] for beat in beats),
        3,
    )
    source_audio_duration_sec = require_positive_number(
        audio_render.get("total_duration_sec"),
        "audio_render.total_duration_sec",
    )
    duration_delta_sec = round(
        total_duration_sec - source_audio_duration_sec,
        3,
    )

    if abs(duration_delta_sec) > DURATION_TOLERANCE_SEC:
        raise VisualPacingExecutorError(
            f"total duration mismatch: beats={total_duration_sec}, "
            f"audio={source_audio_duration_sec}"
        )

    now = utc_now_iso()
    visual_pacing_dir = state_path.parent / "visual_pacing"
    visual_pacing_plan_path = visual_pacing_dir / "visual_pacing_plan.json"

    visual_pacing_plan = {
        "project_id": project_id,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "layer": "timed_visual_execution",
        "layer_version": EXECUTOR_VERSION,
        "status": "VISUAL_PACING_PLAN_OK",
        "source_phase": state["phase"],
        "source_scenes_path": str(scenes_path),
        "source_audio_render_path": str(audio_render_path),
        "timing_source": "actual_canonical_audio",
        "audio_master_clock": True,
        "visual_unit_mapping": True,
        "visual_unit_mapping_strategy": "ordered_proportional",
        "timed_execution_ready": True,
        "scene_count": scene_count,
        "beat_count": len(beats),
        "target_beat_duration_sec": TARGET_BEAT_DURATION_SEC,
        "min_beat_duration_sec": MIN_BEAT_DURATION_SEC,
        "max_beat_duration_sec": MAX_BEAT_DURATION_SEC,
        "source_audio_duration_sec": source_audio_duration_sec,
        "total_duration_sec": total_duration_sec,
        "duration_delta_sec": duration_delta_sec,
        "beats": beats,
        "created_at": now,
        "warnings": [],
        "blockers": [],
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
        "status": "VISUAL_PACING_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "scene_count": scene_count,
        "beat_count": len(beats),
        "total_duration_sec": total_duration_sec,
        "duration_delta_sec": duration_delta_sec,
        "visual_pacing_plan_path": str(visual_pacing_plan_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FlowMind SCENES timed visual execution executor"
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
        result = run_visual_pacing_executor(Path(args.state))
    except (VisualPacingExecutorError, StateValidationError, OSError) as exc:
        print(f"[VISUAL_PACING_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
