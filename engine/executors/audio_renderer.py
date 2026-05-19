from __future__ import annotations

import argparse
import json
import os
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

RENDERER_NAME = "audio_renderer"
RENDERER_VERSION = "1.0.2"
SUPPORTED_PROVIDER = "elevenlabs"
DEFAULT_VOICE_PROFILE_ENV = "FLOWMIND_TTS_VOICE_PROFILE"
DEFAULT_VOICE_ID_ENV = "ELEVENLABS_VOICE_ID"
API_KEY_ENV = "ELEVENLABS_API_KEY"

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


class AudioRendererError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise AudioRendererError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise AudioRendererError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise AudioRendererError(f"{field_name} must be an integer")

    if value <= 0:
        raise AudioRendererError(f"{field_name} must be > 0")

    return value


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AudioRendererError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AudioRendererError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise AudioRendererError(f"JSON file must contain an object: {path}")

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
        raise AudioRendererError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def optional_env_value(name: str) -> str | None:
    value = os.environ.get(name)
    if not isinstance(value, str):
        return None

    normalized = value.strip()
    if not normalized:
        return None

    return normalized


def validate_audio_plan(audio_plan: dict[str, Any]) -> list[dict[str, Any]]:
    audio_segments = audio_plan.get("audio_segments")
    if not isinstance(audio_segments, list):
        raise AudioRendererError("audio_plan.audio_segments must be a list")

    if not audio_segments:
        raise AudioRendererError("audio_plan.audio_segments must not be empty")

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

    for index, segment in enumerate(audio_segments, start=1):
        if not isinstance(segment, dict):
            raise AudioRendererError(f"audio segment index {index} must be an object")

        missing = sorted(required_fields - set(segment.keys()))
        if missing:
            raise AudioRendererError(
                f"audio segment index {index} missing fields: {', '.join(missing)}"
            )

        require_non_empty_string(segment["segment_id"], f"audio_segment[{index}].segment_id")
        require_non_empty_string(segment["source_scene_id"], f"audio_segment[{index}].source_scene_id")
        require_positive_int(segment["order"], f"audio_segment[{index}].order")
        require_non_empty_string(segment["voiceover_text"], f"audio_segment[{index}].voiceover_text")
        require_positive_int(
            segment["estimated_word_count"],
            f"audio_segment[{index}].estimated_word_count",
        )
        require_positive_int(
            segment["estimated_duration_sec"],
            f"audio_segment[{index}].estimated_duration_sec",
        )
        require_non_empty_string(segment["tts_status"], f"audio_segment[{index}].tts_status")
        require_non_empty_string(segment["production_notes"], f"audio_segment[{index}].production_notes")

        fail_if_forbidden_markers(
            json.dumps(segment, ensure_ascii=False),
            f"audio_segment[{index}]",
        )

    return audio_segments


def build_blockers(
    api_key_present: bool,
    voice_profile: str | None,
    voice_id: str | None,
) -> list[str]:
    blockers: list[str] = []

    if not api_key_present:
        blockers.append("TTS API key is missing from environment")

    if voice_profile is None:
        blockers.append("voice profile is missing from environment")

    if voice_id is None:
        blockers.append("provider voice id is missing from environment")

    blockers.append("TTS provider call is not implemented in audio_renderer v1.0.2")
    blockers.append("audio files were not rendered")
    blockers.append("duration validation was not performed")
    blockers.append("loudness validation was not performed")

    return blockers


def build_missing_requirements(
    api_key_present: bool,
    provider_selected: bool,
    voice_profile: str | None,
    voice_id: str | None,
) -> list[str]:
    missing = list(REQUIRED_MISSING_REQUIREMENTS)

    if provider_selected and "selected TTS provider" in missing:
        missing.remove("selected TTS provider")

    if api_key_present and "TTS API key" in missing:
        missing.remove("TTS API key")

    if voice_profile is not None and voice_id is not None:
        if "selected voice profile" in missing:
            missing.remove("selected voice profile")

    return missing


def build_segments(audio_segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rendered_segments: list[dict[str, Any]] = []

    for segment in audio_segments:
        rendered_segments.append(
            {
                "segment_id": segment["segment_id"],
                "source_scene_id": segment["source_scene_id"],
                "order": segment["order"],
                "tts_status": "blocked",
                "voiceover_text": segment["voiceover_text"],
                "audio_path": None,
                "provider_job_id": None,
                "duration_sec": 0,
                "estimated_duration_sec": segment["estimated_duration_sec"],
                "duration_delta_sec": None,
                "provider_status": "blocked",
                "error_message": "TTS provider call is not implemented in audio_renderer v1.0.2.",
            }
        )

    return rendered_segments


def run_audio_renderer(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "QA":
        raise AudioRendererError("audio_renderer may run only when phase is QA")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]
    artifacts = state.get("artifacts", {})

    if not isinstance(artifacts, dict):
        raise AudioRendererError("artifacts must be an object")

    audio_plan_path = Path(
        require_non_empty_string(artifacts.get("audio_plan_path"), "artifacts.audio_plan_path")
    )

    audio_plan = read_json_file(audio_plan_path)
    fail_if_forbidden_markers(json.dumps(audio_plan, ensure_ascii=False), "audio_plan")

    audio_segments = validate_audio_plan(audio_plan)
    segment_count = len(audio_segments)

    target_duration_sec = require_positive_int(
        manifest.get("target_duration_sec"),
        "manifest.target_duration_sec",
    )

    api_key_present = optional_env_value(API_KEY_ENV) is not None
    voice_profile = optional_env_value(DEFAULT_VOICE_PROFILE_ENV)
    voice_id = optional_env_value(DEFAULT_VOICE_ID_ENV)
    provider_selected = api_key_present

    blockers = build_blockers(api_key_present, voice_profile, voice_id)
    missing_requirements = build_missing_requirements(
        api_key_present,
        provider_selected,
        voice_profile,
        voice_id,
    )

    now = utc_now_iso()
    audio_dir = state_path.parent / "audio"
    audio_render_path = audio_dir / "audio_render.json"

    rendered_segments = build_segments(audio_segments)

    audio_render = {
        "project_id": project_id,
        "renderer": RENDERER_NAME,
        "renderer_version": RENDERER_VERSION,
        "source_audio_plan_path": str(audio_plan_path),
        "tts_provider": SUPPORTED_PROVIDER if provider_selected else None,
        "voice_profile": voice_profile,
        "provider_voice_id": voice_id,
        "audio_status": "blocked",
        "audio_ready": False,
        "rendered_at": now,
        "segment_count": segment_count,
        "rendered_segment_count": 0,
        "failed_segment_count": 0,
        "total_duration_sec": 0,
        "target_duration_sec": target_duration_sec,
        "duration_validated": False,
        "loudness_validated": False,
        "voiceover_path": None,
        "segments": rendered_segments,
        "warnings": [],
        "blockers": blockers,
        "missing_requirements": missing_requirements,
    }

    serialized = json.dumps(audio_render, ensure_ascii=False)
    fail_if_forbidden_markers(serialized, "audio_render")

    write_json_atomic(audio_render_path, audio_render)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["audio_render_path"] = str(audio_render_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "AUDIO_RENDERER_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "audio_render_path": str(audio_render_path),
        "audio_status": audio_render["audio_status"],
        "audio_ready": audio_render["audio_ready"],
        "segment_count": audio_render["segment_count"],
        "rendered_segment_count": audio_render["rendered_segment_count"],
        "missing_requirements": audio_render["missing_requirements"],
        "blockers": audio_render["blockers"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind audio renderer v1")
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
        result = run_audio_renderer(Path(args.state))
    except (AudioRendererError, StateValidationError, OSError) as exc:
        print(f"[AUDIO_RENDERER][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
