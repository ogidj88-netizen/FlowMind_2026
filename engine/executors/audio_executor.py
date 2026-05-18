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

EXECUTOR_NAME = "audio_executor"
EXECUTOR_VERSION = "1.0.0"
WORDS_PER_MINUTE = 145.0
ALLOWED_DURATION_DRIFT = 0.20

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

REQUIRED_MISSING_REQUIREMENTS = (
    "selected TTS provider",
    "selected voice profile",
    "TTS API key",
    "rendered audio files",
    "audio duration validation",
    "loudness validation",
)


class AudioExecutorError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise AudioExecutorError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise AudioExecutorError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise AudioExecutorError(f"{field_name} must be an integer")

    if value <= 0:
        raise AudioExecutorError(f"{field_name} must be > 0")

    return value


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AudioExecutorError(f"Text file not found: {path}") from exc


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AudioExecutorError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AudioExecutorError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise AudioExecutorError(f"JSON file must contain an object: {path}")

    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(path)


def fail_if_forbidden_markers(value: str, source_name: str) -> None:
    upper_value = value.upper()
    hits = [marker for marker in FORBIDDEN_MARKERS if marker in upper_value]
    if hits:
        raise AudioExecutorError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def expected_duration_range(target_duration_sec: int) -> tuple[int, int]:
    min_duration = int(round(target_duration_sec * (1.0 - ALLOWED_DURATION_DRIFT)))
    max_duration = int(round(target_duration_sec * (1.0 + ALLOWED_DURATION_DRIFT)))
    return min_duration, max_duration


def estimate_duration_sec_from_words(word_count: int) -> int:
    if word_count <= 0:
        return 0

    return max(1, int(round((word_count / WORDS_PER_MINUTE) * 60.0)))


def validate_duration(estimated_duration_sec: int, target_duration_sec: int) -> None:
    min_duration, max_duration = expected_duration_range(target_duration_sec)
    if not (min_duration <= estimated_duration_sec <= max_duration):
        raise AudioExecutorError(
            "estimated_duration_sec outside allowed range: "
            f"{estimated_duration_sec}, allowed={min_duration}-{max_duration}"
        )


def validate_script_qa(script_qa: dict[str, Any]) -> None:
    if script_qa.get("verdict") != "PASS":
        raise AudioExecutorError("AUDIO executor requires script_qa.verdict=PASS")


def validate_assembly_plan(assembly_plan: dict[str, Any]) -> list[dict[str, Any]]:
    timeline = assembly_plan.get("timeline")
    if not isinstance(timeline, list):
        raise AudioExecutorError("assembly_plan.timeline must be a list")

    if not timeline:
        raise AudioExecutorError("assembly_plan.timeline must not be empty")

    scene_count = require_positive_int(
        assembly_plan.get("scene_count"),
        "assembly_plan.scene_count",
    )

    if scene_count != len(timeline):
        raise AudioExecutorError(
            f"assembly scene_count mismatch: scene_count={scene_count}, timeline={len(timeline)}"
        )

    required_fields = {
        "timeline_id",
        "scene_id",
        "order",
        "voiceover_text",
        "estimated_duration_sec",
        "asset_id",
        "asset_type",
        "asset_query",
        "usage_role",
        "provider_status",
        "local_path",
        "source_url",
        "visual_intent",
        "on_screen_text",
        "production_notes",
    }

    for index, item in enumerate(timeline, start=1):
        if not isinstance(item, dict):
            raise AudioExecutorError(f"timeline index {index} must be an object")

        missing = sorted(required_fields - set(item.keys()))
        if missing:
            raise AudioExecutorError(
                f"timeline index {index} missing fields: {', '.join(missing)}"
            )

        require_non_empty_string(item["timeline_id"], f"timeline[{index}].timeline_id")
        require_non_empty_string(item["scene_id"], f"timeline[{index}].scene_id")
        require_positive_int(item["order"], f"timeline[{index}].order")
        require_non_empty_string(item["voiceover_text"], f"timeline[{index}].voiceover_text")
        require_positive_int(
            item["estimated_duration_sec"],
            f"timeline[{index}].estimated_duration_sec",
        )

        fail_if_forbidden_markers(
            json.dumps(item, ensure_ascii=False),
            f"timeline[{index}]",
        )

    return timeline


def validate_script_text(script_text: str) -> None:
    if not script_text.strip():
        raise AudioExecutorError("script.txt is empty")

    fail_if_forbidden_markers(script_text, "script.txt")


def build_audio_segment(timeline_item: dict[str, Any]) -> dict[str, Any]:
    order = require_positive_int(timeline_item["order"], "timeline.order")
    scene_id = require_non_empty_string(timeline_item["scene_id"], "timeline.scene_id")
    voiceover_text = require_non_empty_string(
        timeline_item["voiceover_text"],
        "timeline.voiceover_text",
    )

    word_count = count_words(voiceover_text)
    if word_count <= 0:
        raise AudioExecutorError(f"{scene_id} voiceover_text has no words")

    estimated_duration_sec = estimate_duration_sec_from_words(word_count)

    return {
        "segment_id": f"AUDIO_SEGMENT_{order:03d}",
        "source_scene_id": scene_id,
        "order": order,
        "voiceover_text": voiceover_text,
        "estimated_word_count": word_count,
        "estimated_duration_sec": estimated_duration_sec,
        "tts_status": "planned",
        "audio_path": None,
        "provider_job_id": None,
        "production_notes": (
            "Planning-only audio segment. No TTS provider called. "
            "Render voiceover in a later TTS integration phase."
        ),
    }


def validate_audio_segment(segment: dict[str, Any], index: int) -> None:
    required_fields = {
        "segment_id",
        "source_scene_id",
        "order",
        "voiceover_text",
        "estimated_word_count",
        "estimated_duration_sec",
        "tts_status",
        "audio_path",
        "provider_job_id",
        "production_notes",
    }

    missing = sorted(required_fields - set(segment.keys()))
    if missing:
        raise AudioExecutorError(
            f"audio segment index {index} missing fields: {', '.join(missing)}"
        )

    require_non_empty_string(segment["segment_id"], f"segment[{index}].segment_id")
    require_non_empty_string(segment["source_scene_id"], f"segment[{index}].source_scene_id")
    require_positive_int(segment["order"], f"segment[{index}].order")
    require_non_empty_string(segment["voiceover_text"], f"segment[{index}].voiceover_text")
    require_positive_int(
        segment["estimated_word_count"],
        f"segment[{index}].estimated_word_count",
    )
    require_positive_int(
        segment["estimated_duration_sec"],
        f"segment[{index}].estimated_duration_sec",
    )
    require_non_empty_string(segment["tts_status"], f"segment[{index}].tts_status")
    require_non_empty_string(segment["production_notes"], f"segment[{index}].production_notes")

    if segment["tts_status"] != "planned":
        raise AudioExecutorError(f"segment[{index}].tts_status must be planned in AUDIO v1")

    if segment["audio_path"] is not None:
        raise AudioExecutorError(f"segment[{index}].audio_path must be null in AUDIO v1")

    if segment["provider_job_id"] is not None:
        raise AudioExecutorError(f"segment[{index}].provider_job_id must be null in AUDIO v1")

    fail_if_forbidden_markers(
        json.dumps(segment, ensure_ascii=False),
        f"audio_segment[{index}]",
    )


def build_audio_segments(timeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
    segments = [build_audio_segment(item) for item in timeline]

    for index, segment in enumerate(segments, start=1):
        validate_audio_segment(segment, index)

    return segments


def run_audio_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "AUDIO":
        raise AudioExecutorError("AUDIO executor may run only when phase is AUDIO")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]
    artifacts = state.get("artifacts", {})

    if not isinstance(artifacts, dict):
        raise AudioExecutorError("artifacts must be an object")

    niche = require_non_empty_string(manifest.get("niche"), "manifest.niche")
    audience = require_non_empty_string(manifest.get("audience"), "manifest.audience")
    content_language = require_non_empty_string(
        manifest.get("content_language"),
        "manifest.content_language",
    )
    topic = require_non_empty_string(manifest.get("topic"), "manifest.topic")
    working_title = require_non_empty_string(
        manifest.get("working_title"),
        "manifest.working_title",
    )
    target_duration_sec = require_positive_int(
        manifest.get("target_duration_sec"),
        "manifest.target_duration_sec",
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
    assembly_plan_path = Path(
        require_non_empty_string(
            artifacts.get("assembly_plan_path"),
            "artifacts.assembly_plan_path",
        )
    )

    script_text = read_text_file(script_path)
    script_meta = read_json_file(script_meta_path)
    script_qa = read_json_file(script_qa_path)
    assembly_plan = read_json_file(assembly_plan_path)

    validate_script_text(script_text)
    validate_script_qa(script_qa)
    timeline = validate_assembly_plan(assembly_plan)

    audio_segments = build_audio_segments(timeline)

    estimated_word_count = sum(
        int(segment["estimated_word_count"])
        for segment in audio_segments
    )
    estimated_duration_sec = sum(
        int(segment["estimated_duration_sec"])
        for segment in audio_segments
    )
    estimated_duration_minutes = round(estimated_duration_sec / 60.0, 2)

    validate_duration(estimated_duration_sec, target_duration_sec)

    meta_word_count = script_meta.get("word_count")
    if isinstance(meta_word_count, int) and meta_word_count != estimated_word_count:
        raise AudioExecutorError(
            f"audio word count mismatch: script_meta={meta_word_count}, audio_segments={estimated_word_count}"
        )

    now = utc_now_iso()
    audio_plan_path = state_path.parent / "audio" / "audio_plan.json"

    audio_plan = {
        "project_id": project_id,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "source_phase": state["phase"],
        "source_script_path": str(script_path),
        "source_script_qa_path": str(script_qa_path),
        "source_assembly_plan_path": str(assembly_plan_path),
        "topic": topic,
        "working_title": working_title,
        "niche": niche,
        "audience": audience,
        "content_language": content_language,
        "target_duration_sec": target_duration_sec,
        "audio_status": "planned",
        "audio_ready": False,
        "tts_provider": None,
        "voice_profile": None,
        "estimated_word_count": estimated_word_count,
        "estimated_duration_minutes": estimated_duration_minutes,
        "estimated_duration_sec": estimated_duration_sec,
        "audio_segments": audio_segments,
        "missing_requirements": list(REQUIRED_MISSING_REQUIREMENTS),
        "created_at": now,
    }

    serialized = json.dumps(audio_plan, ensure_ascii=False)
    fail_if_forbidden_markers(serialized, "audio_plan")

    write_json_atomic(audio_plan_path, audio_plan)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["audio_plan_path"] = str(audio_plan_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "AUDIO_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "audio_plan_path": str(audio_plan_path),
        "audio_status": "planned",
        "audio_ready": False,
        "segment_count": len(audio_segments),
        "estimated_word_count": estimated_word_count,
        "estimated_duration_sec": estimated_duration_sec,
        "missing_requirements": list(REQUIRED_MISSING_REQUIREMENTS),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind canonical AUDIO executor v1")
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
        result = run_audio_executor(Path(args.state))
    except (AudioExecutorError, StateValidationError, OSError) as exc:
        print(f"[AUDIO_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
