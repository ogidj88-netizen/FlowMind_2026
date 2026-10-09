from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from openai import OpenAI

from engine.state_store import save_state_with_disk_guard
from engine.state_validator import StateValidationError, load_state

EXECUTOR_NAME = "scenes_executor"
EXECUTOR_VERSION = "1.1.0"
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


ALLOWED_ASSET_TYPES = {
    "stock_video",
    "stock_image",
    "simple_motion_text",
    "chart_or_bill_visual",
    "screen_style_visual",
}

ALLOWED_REPRESENTATION_MODES = {
    "DIRECT_EVIDENCE",
    "ILLUSTRATIVE",
    "DECORATIVE",
}

ALLOWED_PRODUCTION_PRIORITIES = {
    "ESSENTIAL",
    "IMPORTANT",
    "OPTIONAL",
}


def parse_json_object(raw_text: str, source_name: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ScenesExecutorError(f"{source_name} returned invalid JSON") from exc

    if not isinstance(payload, dict):
        raise ScenesExecutorError(f"{source_name} must return a JSON object")

    return payload


def normalize_string_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ScenesExecutorError(f"{field_name} must be an array")

    normalized: list[str] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, str):
            raise ScenesExecutorError(f"{field_name}[{index}] must be a string")

        text = item.strip()
        if text:
            fail_if_forbidden_markers(text, f"{field_name}[{index}]")
            normalized.append(text)

    return normalized


def build_pass1_prompt(
    *,
    segment: str,
    scene_id: str,
    topic: str,
    working_title: str,
    hook: str,
    audience: str,
    primary_platform: str,
) -> str:
    return f"""
You are the Visual Staging / Director Pass 1 component for a production pipeline.

Create semantic visual coverage for exactly one narration scene.

PROJECT CONTEXT
Topic: {topic}
Working title: {working_title}
Hook: {hook}
Audience: {audience}
Primary platform: {primary_platform}
Scene ID: {scene_id}

NARRATION
{segment}

BOUNDARY
Pass 1 answers WHAT should be seen and WHY.
Do not invent timestamps, frame timing, shot duration, or final-cut choreography.
Do not rewrite the narration.
Do not add factual claims that are absent from the narration.
Do not optimize for one niche or topic.
Use the minimum number of visual units needed to cover materially distinct ideas in the narration.
Do not split merely to reach a target count.
Do not merge materially different visual ideas merely to reduce count.

For each visual unit return:
- purpose: why this visual exists in relation to the narration
- visual_intent: concrete, searchable/renderable description of what should be seen
- representation_mode: DIRECT_EVIDENCE, ILLUSTRATIVE, or DECORATIVE
- asset_type: stock_video, stock_image, simple_motion_text, chart_or_bill_visual, or screen_style_visual
- production_priority: ESSENTIAL, IMPORTANT, or OPTIONAL
- must_show: array of concrete elements required for the visual to communicate correctly
- must_not_show: array of misleading or contradictory elements to avoid
- overlay_intent: short overlay intent, or "none"

Rules:
- visual_intent must be specific to this narration, not generic filler.
- Different visual units must represent materially different visual ideas.
- Prefer DIRECT_EVIDENCE when the narration depends on a real interface, document, number, comparison, or observable mechanism.
- Use ILLUSTRATIVE when a faithful conceptual depiction is enough.
- Use DECORATIVE only when no stronger evidentiary visual is needed.
- Choose asset_type by the visual need, not by keyword matching.
- Return JSON only.

Required JSON shape:
{{
  "visual_units": [
    {{
      "purpose": "...",
      "visual_intent": "...",
      "representation_mode": "ILLUSTRATIVE",
      "asset_type": "stock_video",
      "production_priority": "IMPORTANT",
      "must_show": ["..."],
      "must_not_show": ["..."],
      "overlay_intent": "none"
    }}
  ]
}}
""".strip()


def generate_visual_units(
    *,
    segment: str,
    scene_id: str,
    topic: str,
    working_title: str,
    hook: str,
    audience: str,
    primary_platform: str,
) -> list[dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ScenesExecutorError("OPENAI_API_KEY not set")

    client = OpenAI(api_key=api_key)
    prompt = build_pass1_prompt(
        segment=segment,
        scene_id=scene_id,
        topic=topic,
        working_title=working_title,
        hook=hook,
        audience=audience,
        primary_platform=primary_platform,
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return only valid JSON. Follow the requested schema exactly. "
                        "Do not add markdown or commentary."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
    except Exception as exc:
        raise ScenesExecutorError(f"Pass 1 OpenAI request failed for {scene_id}: {exc}") from exc

    try:
        content = response.choices[0].message.content
    except Exception as exc:
        raise ScenesExecutorError(f"Invalid Pass 1 OpenAI response shape for {scene_id}: {exc}") from exc

    if content is None or not str(content).strip():
        raise ScenesExecutorError(f"Pass 1 OpenAI returned empty content for {scene_id}")

    payload = parse_json_object(str(content).strip(), f"{scene_id} Pass 1")
    raw_units = payload.get("visual_units")

    if not isinstance(raw_units, list) or not raw_units:
        raise ScenesExecutorError(f"{scene_id}.visual_units must be a non-empty array")

    visual_units: list[dict[str, Any]] = []
    seen_intents: set[str] = set()

    for unit_index, raw_unit in enumerate(raw_units, start=1):
        if not isinstance(raw_unit, dict):
            raise ScenesExecutorError(
                f"{scene_id}.visual_units[{unit_index}] must be an object"
            )

        purpose = require_non_empty_string(
            raw_unit.get("purpose"),
            f"{scene_id}.visual_units[{unit_index}].purpose",
        )
        visual_intent = require_non_empty_string(
            raw_unit.get("visual_intent"),
            f"{scene_id}.visual_units[{unit_index}].visual_intent",
        )
        representation_mode = require_non_empty_string(
            raw_unit.get("representation_mode"),
            f"{scene_id}.visual_units[{unit_index}].representation_mode",
        ).upper()
        asset_type = require_non_empty_string(
            raw_unit.get("asset_type"),
            f"{scene_id}.visual_units[{unit_index}].asset_type",
        )
        production_priority = require_non_empty_string(
            raw_unit.get("production_priority"),
            f"{scene_id}.visual_units[{unit_index}].production_priority",
        ).upper()
        overlay_intent = require_non_empty_string(
            raw_unit.get("overlay_intent"),
            f"{scene_id}.visual_units[{unit_index}].overlay_intent",
        )
        must_show = normalize_string_list(
            raw_unit.get("must_show"),
            f"{scene_id}.visual_units[{unit_index}].must_show",
        )
        must_not_show = normalize_string_list(
            raw_unit.get("must_not_show"),
            f"{scene_id}.visual_units[{unit_index}].must_not_show",
        )

        if representation_mode not in ALLOWED_REPRESENTATION_MODES:
            raise ScenesExecutorError(
                f"{scene_id}.visual_units[{unit_index}].representation_mode "
                f"is not allowed: {representation_mode}"
            )

        if asset_type not in ALLOWED_ASSET_TYPES:
            raise ScenesExecutorError(
                f"{scene_id}.visual_units[{unit_index}].asset_type "
                f"is not allowed: {asset_type}"
            )

        if production_priority not in ALLOWED_PRODUCTION_PRIORITIES:
            raise ScenesExecutorError(
                f"{scene_id}.visual_units[{unit_index}].production_priority "
                f"is not allowed: {production_priority}"
            )

        fail_if_forbidden_markers(
            purpose,
            f"{scene_id}.visual_units[{unit_index}].purpose",
        )
        fail_if_forbidden_markers(
            visual_intent,
            f"{scene_id}.visual_units[{unit_index}].visual_intent",
        )
        fail_if_forbidden_markers(
            overlay_intent,
            f"{scene_id}.visual_units[{unit_index}].overlay_intent",
        )

        intent_key = visual_intent.casefold()
        if intent_key in seen_intents:
            raise ScenesExecutorError(
                f"{scene_id}.visual_units contains duplicate visual_intent"
            )
        seen_intents.add(intent_key)

        visual_units.append(
            {
                "unit_id": f"{scene_id}_VU_{unit_index:03d}",
                "source_scene_id": scene_id,
                "purpose": purpose,
                "visual_intent": visual_intent,
                "representation_mode": representation_mode,
                "asset_type": asset_type,
                "production_priority": production_priority,
                "must_show": must_show,
                "must_not_show": must_not_show,
                "overlay_intent": overlay_intent,
            }
        )

    return visual_units


def build_scene_visual_summary(visual_units: list[dict[str, Any]]) -> str:
    intents = [
        require_non_empty_string(unit.get("visual_intent"), "visual_unit.visual_intent")
        for unit in visual_units
    ]
    return " | ".join(intents)



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


def build_scenes(
    *,
    script_text: str,
    topic: str,
    working_title: str,
    hook: str,
    audience: str,
    primary_platform: str,
) -> tuple[list[dict[str, Any]], int]:
    segments = split_script_into_segments(script_text)

    scenes: list[dict[str, Any]] = []
    total_duration = 0

    for index, segment in enumerate(segments, start=1):
        scene_id = f"SCENE_{index:03d}"
        duration_sec = estimate_duration_sec(segment)
        total_duration += duration_sec

        visual_units = generate_visual_units(
            segment=segment,
            scene_id=scene_id,
            topic=topic,
            working_title=working_title,
            hook=hook,
            audience=audience,
            primary_platform=primary_platform,
        )

        primary_unit = visual_units[0]
        asset_type = require_non_empty_string(
            primary_unit.get("asset_type"),
            f"{scene_id}.visual_units[1].asset_type",
        )

        scenes.append(
            {
                "scene_id": scene_id,
                "order": index,
                "voiceover_text": segment,
                "visual_intent": build_scene_visual_summary(visual_units),
                "on_screen_text": build_on_screen_text(segment, index),
                "asset_type": asset_type,
                "estimated_duration_sec": duration_sec,
                "production_notes": build_production_notes(asset_type, duration_sec),
                "visual_units": visual_units,
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

    allowed_asset_types = ALLOWED_ASSET_TYPES

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

        visual_units = scene.get("visual_units")
        if not isinstance(visual_units, list) or not visual_units:
            raise ScenesExecutorError(
                f"{scene['scene_id']}.visual_units must be a non-empty array"
            )

        unit_ids: set[str] = set()
        for unit in visual_units:
            if not isinstance(unit, dict):
                raise ScenesExecutorError(
                    f"{scene['scene_id']}.visual_units entries must be objects"
                )

            unit_id = require_non_empty_string(
                unit.get("unit_id"),
                f"{scene['scene_id']}.visual_units.unit_id",
            )
            if unit_id in unit_ids:
                raise ScenesExecutorError(
                    f"{scene['scene_id']}.visual_units contains duplicate unit_id: {unit_id}"
                )
            unit_ids.add(unit_id)

            if unit.get("source_scene_id") != scene["scene_id"]:
                raise ScenesExecutorError(
                    f"{unit_id}.source_scene_id must equal {scene['scene_id']}"
                )

            representation_mode = require_non_empty_string(
                unit.get("representation_mode"),
                f"{unit_id}.representation_mode",
            )
            if representation_mode not in ALLOWED_REPRESENTATION_MODES:
                raise ScenesExecutorError(
                    f"{unit_id}.representation_mode is not allowed: {representation_mode}"
                )

            unit_asset_type = require_non_empty_string(
                unit.get("asset_type"),
                f"{unit_id}.asset_type",
            )
            if unit_asset_type not in ALLOWED_ASSET_TYPES:
                raise ScenesExecutorError(
                    f"{unit_id}.asset_type is not allowed: {unit_asset_type}"
                )

            production_priority = require_non_empty_string(
                unit.get("production_priority"),
                f"{unit_id}.production_priority",
            )
            if production_priority not in ALLOWED_PRODUCTION_PRIORITIES:
                raise ScenesExecutorError(
                    f"{unit_id}.production_priority is not allowed: {production_priority}"
                )

            require_non_empty_string(unit.get("purpose"), f"{unit_id}.purpose")
            require_non_empty_string(unit.get("visual_intent"), f"{unit_id}.visual_intent")
            require_non_empty_string(unit.get("overlay_intent"), f"{unit_id}.overlay_intent")
            normalize_string_list(unit.get("must_show"), f"{unit_id}.must_show")
            normalize_string_list(unit.get("must_not_show"), f"{unit_id}.must_not_show")

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

    language_code = content_language.strip().lower().replace("_", "-").split("-", 1)[0]
    if language_code != "en":
        raise ScenesExecutorError(
            "deterministic SCENES executor v1 currently supports only English content_language"
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

    scenes, estimated_total_duration_sec = build_scenes(
        script_text=script_text,
        topic=topic,
        working_title=working_title,
        hook=hook,
        audience=audience,
        primary_platform=primary_platform,
    )

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
        "pass1_visual_staging": True,
        "pass1_timing_owner": False,
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
