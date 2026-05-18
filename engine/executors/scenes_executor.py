from __future__ import annotations

import argparse
import json
import re
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

EXECUTOR_NAME = "scenes_executor"
EXECUTOR_VERSION = "1.0.0"
WORDS_PER_MINUTE = 145.0
ALLOWED_DURATION_DRIFT = 0.20
MIN_SCENE_COUNT = 6
MAX_SCENE_COUNT = 18

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


class ScenesExecutorError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ScenesExecutorError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ScenesExecutorError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise ScenesExecutorError(f"{field_name} must be an integer")

    if value <= 0:
        raise ScenesExecutorError(f"{field_name} must be > 0")

    return value


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ScenesExecutorError(f"Text file not found: {path}") from exc


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ScenesExecutorError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ScenesExecutorError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise ScenesExecutorError(f"JSON file must contain an object: {path}")

    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(path)


def fail_if_forbidden_markers(text: str, source_name: str) -> None:
    upper_text = text.upper()
    hits = [marker for marker in FORBIDDEN_MARKERS if marker in upper_text]
    if hits:
        raise ScenesExecutorError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def expected_duration_range(target_duration_sec: int) -> tuple[int, int]:
    min_duration = int(round(target_duration_sec * (1.0 - ALLOWED_DURATION_DRIFT)))
    max_duration = int(round(target_duration_sec * (1.0 + ALLOWED_DURATION_DRIFT)))
    return min_duration, max_duration


def estimate_duration_sec(text: str) -> int:
    words = count_words(text)
    if words <= 0:
        return 0

    return max(1, int(round((words / WORDS_PER_MINUTE) * 60.0)))


def split_script_into_segments(script_text: str) -> list[str]:
    paragraphs = [
        paragraph.strip()
        for paragraph in script_text.split("\n\n")
        if paragraph.strip()
    ]

    if len(paragraphs) < MIN_SCENE_COUNT:
        raise ScenesExecutorError(
            f"script has too few useful paragraphs for scenes: {len(paragraphs)}"
        )

    if len(paragraphs) <= MAX_SCENE_COUNT:
        return paragraphs

    merged: list[str] = []
    buffer: list[str] = []

    for paragraph in paragraphs:
        buffer.append(paragraph)

        if len(merged) + 1 >= MAX_SCENE_COUNT:
            continue

        if count_words(" ".join(buffer)) >= 70:
            merged.append("\n\n".join(buffer))
            buffer = []

    if buffer:
        if merged:
            merged[-1] = merged[-1] + "\n\n" + "\n\n".join(buffer)
        else:
            merged.append("\n\n".join(buffer))

    if len(merged) > MAX_SCENE_COUNT:
        raise ScenesExecutorError(f"scene segmentation exceeded max scene count: {len(merged)}")

    return merged


def choose_asset_type(index: int, segment: str) -> str:
    normalized = segment.lower()

    if index == 1:
        return "simple_motion_text"

    if any(term in normalized for term in ("refrigerator", "water heater", "computer", "dehumidifier", "dryer", "freezer", "pool pump")):
        return "stock_video"

    if any(term in normalized for term in ("check", "compare", "write down", "look at", "seven-day reset", "call the provider")):
        return "screen_style_visual"

    if any(term in normalized for term in ("bill", "charges", "rate", "kilowatt", "pricing", "fixed charges")):
        return "chart_or_bill_visual"

    return "stock_image"


def build_visual_intent(segment: str, asset_type: str) -> str:
    normalized = segment.lower()

    if asset_type == "chart_or_bill_visual":
        return "Show a clean utility bill or simple cost breakdown visual with usage, rate, and fixed charges separated."

    if asset_type == "screen_style_visual":
        return "Show a simple checklist or comparison screen that makes the diagnostic step easy to follow."

    if asset_type == "simple_motion_text":
        return "Use minimal motion text to emphasize the main idea without distracting from the voiceover."

    if asset_type == "stock_video":
        return "Show everyday household devices or home energy use that can quietly increase costs over time."

    if "device" in normalized or "fridge" in normalized or "water heater" in normalized:
        return "Show everyday household devices that can quietly increase energy costs over time."

    return "Use simple stock visuals that support the narration and keep attention on the hidden-cost explanation."


def build_on_screen_text(segment: str, order: int) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", segment.strip())
    first_sentence = sentences[0].strip() if sentences else ""

    if not first_sentence:
        return f"Scene {order}"

    words = first_sentence.split()
    if len(words) <= 9:
        return first_sentence

    return " ".join(words[:9]).rstrip(".,;:") + "..."


def build_production_notes(asset_type: str, duration_sec: int) -> str:
    return (
        f"Use {asset_type}. Keep pacing clear. Target roughly {duration_sec} seconds. "
        "Do not add new factual claims beyond the script."
    )


def build_scenes(script_text: str) -> tuple[list[dict[str, Any]], int]:
    segments = split_script_into_segments(script_text)

    scenes: list[dict[str, Any]] = []
    total_duration = 0

    for index, segment in enumerate(segments, start=1):
        duration_sec = estimate_duration_sec(segment)
        total_duration += duration_sec
        asset_type = choose_asset_type(index, segment)

        scenes.append(
            {
                "scene_id": f"SCENE_{index:03d}",
                "order": index,
                "voiceover_text": segment,
                "visual_intent": build_visual_intent(segment, asset_type),
                "on_screen_text": build_on_screen_text(segment, index),
                "asset_type": asset_type,
                "estimated_duration_sec": duration_sec,
                "production_notes": build_production_notes(asset_type, duration_sec),
            }
        )

    return scenes, total_duration


def validate_scenes(
    *,
    scenes: list[dict[str, Any]],
    estimated_total_duration_sec: int,
    target_duration_sec: int,
) -> None:
    if len(scenes) < MIN_SCENE_COUNT:
        raise ScenesExecutorError(f"scene_count below minimum: {len(scenes)}")

    if len(scenes) > MAX_SCENE_COUNT:
        raise ScenesExecutorError(f"scene_count above maximum: {len(scenes)}")

    required_scene_fields = {
        "scene_id",
        "order",
        "voiceover_text",
        "visual_intent",
        "on_screen_text",
        "asset_type",
        "estimated_duration_sec",
        "production_notes",
    }

    allowed_asset_types = {
        "stock_video",
        "stock_image",
        "simple_motion_text",
        "chart_or_bill_visual",
        "screen_style_visual",
    }

    for scene in scenes:
        missing = sorted(required_scene_fields - set(scene.keys()))
        if missing:
            raise ScenesExecutorError(
                f"{scene.get('scene_id', 'UNKNOWN_SCENE')} missing fields: {', '.join(missing)}"
            )

        for field_name in required_scene_fields:
            value = scene[field_name]
            if field_name in {"order", "estimated_duration_sec"}:
                if not isinstance(value, int) or value <= 0:
                    raise ScenesExecutorError(
                        f"{scene['scene_id']}.{field_name} must be a positive integer"
                    )
            elif not isinstance(value, str) or not value.strip():
                raise ScenesExecutorError(
                    f"{scene['scene_id']}.{field_name} must be a non-empty string"
                )

        if scene["asset_type"] not in allowed_asset_types:
            raise ScenesExecutorError(
                f"{scene['scene_id']}.asset_type is not allowed: {scene['asset_type']}"
            )

        fail_if_forbidden_markers(scene["voiceover_text"], f"{scene['scene_id']}.voiceover_text")
        fail_if_forbidden_markers(scene["visual_intent"], f"{scene['scene_id']}.visual_intent")
        fail_if_forbidden_markers(scene["on_screen_text"], f"{scene['scene_id']}.on_screen_text")

    min_duration, max_duration = expected_duration_range(target_duration_sec)
    if not (min_duration <= estimated_total_duration_sec <= max_duration):
        raise ScenesExecutorError(
            "estimated_total_duration_sec outside allowed range: "
            f"{estimated_total_duration_sec}, allowed={min_duration}-{max_duration}"
        )


def run_scenes_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "SCENES":
        raise ScenesExecutorError("SCENES executor may run only when phase is SCENES")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]
    artifacts = state.get("artifacts", {})

    if not isinstance(artifacts, dict):
        raise ScenesExecutorError("artifacts must be an object")

    niche = require_non_empty_string(manifest.get("niche"), "manifest.niche")
    audience = require_non_empty_string(manifest.get("audience"), "manifest.audience")
    content_language = require_non_empty_string(
        manifest.get("content_language"),
        "manifest.content_language",
    )
    primary_platform = require_non_empty_string(
        manifest.get("primary_platform"),
        "manifest.primary_platform",
    )
    topic = require_non_empty_string(manifest.get("topic"), "manifest.topic")
    working_title = require_non_empty_string(
        manifest.get("working_title"),
        "manifest.working_title",
    )
    hook = require_non_empty_string(manifest.get("hook"), "manifest.hook")
    target_duration_sec = require_positive_int(
        manifest.get("target_duration_sec"),
        "manifest.target_duration_sec",
    )

    if content_language.lower() != "en":
        raise ScenesExecutorError(
            "deterministic SCENES executor v1 currently supports only content_language='en'"
        )

    script_path = Path(
        require_non_empty_string(artifacts.get("script_path"), "artifacts.script_path")
    )
    script_meta_path = Path(
        require_non_empty_string(artifacts.get("script_meta_path"), "artifacts.script_meta_path")
    )
    script_qa_path = Path(
        require_non_empty_string(artifacts.get("script_qa_path"), "artifacts.script_qa_path")
    )

    script_text = read_text_file(script_path)
    script_meta = read_json_file(script_meta_path)
    script_qa = read_json_file(script_qa_path)

    if script_qa.get("verdict") != "PASS":
        raise ScenesExecutorError("SCENES executor requires script_qa.verdict=PASS")

    if script_meta.get("qa_status") != "PASS":
        raise ScenesExecutorError("SCENES executor requires script_meta.qa_status=PASS")

    if not script_text.strip():
        raise ScenesExecutorError("script text is empty")

    fail_if_forbidden_markers(script_text, "script.txt")

    scenes, estimated_total_duration_sec = build_scenes(script_text)

    validate_scenes(
        scenes=scenes,
        estimated_total_duration_sec=estimated_total_duration_sec,
        target_duration_sec=target_duration_sec,
    )

    now = utc_now_iso()
    scenes_path = state_path.parent / "scenes" / "scenes.json"

    scenes_payload = {
        "project_id": project_id,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "source_phase": state["phase"],
        "source_script_path": str(script_path),
        "source_script_qa_path": str(script_qa_path),
        "topic": topic,
        "working_title": working_title,
        "hook": hook,
        "niche": niche,
        "audience": audience,
        "content_language": content_language,
        "primary_platform": primary_platform,
        "target_duration_sec": target_duration_sec,
        "scene_count": len(scenes),
        "estimated_total_duration_sec": estimated_total_duration_sec,
        "scenes": scenes,
        "created_at": now,
    }

    write_json_atomic(scenes_path, scenes_payload)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["scenes_path"] = str(scenes_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "SCENES_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "scenes_path": str(scenes_path),
        "scene_count": len(scenes),
        "estimated_total_duration_sec": estimated_total_duration_sec,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind canonical SCENES executor v1")
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
        result = run_scenes_executor(Path(args.state))
    except (ScenesExecutorError, StateValidationError, OSError) as exc:
        print(f"[SCENES_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
