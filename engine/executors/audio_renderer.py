from __future__ import annotations

import argparse
import json
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
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
RENDERER_VERSION = "1.1.1"
SUPPORTED_PROVIDER = "elevenlabs"

API_KEY_ENV = "ELEVENLABS_API_KEY"
VOICE_ID_ENV = "ELEVENLABS_VOICE_ID"
VOICE_PROFILE_ENV = "FLOWMIND_TTS_VOICE_PROFILE"
RENDER_LIMIT_ENV = "FLOWMIND_AUDIO_RENDER_LIMIT"
MODEL_ID_ENV = "ELEVENLABS_MODEL_ID"

DEFAULT_MODEL_ID = "eleven_multilingual_v2"
OUTPUT_AUDIO_DIRNAME = "rendered_segments"

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


def load_env_file_if_present(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        normalized_key = key.strip()
        normalized_value = value.strip().strip('"').strip("'")

        if normalized_key and normalized_key not in os.environ:
            os.environ[normalized_key] = normalized_value


def optional_env_value(name: str) -> str | None:
    value = os.environ.get(name)
    if not isinstance(value, str):
        return None

    normalized = value.strip()
    if not normalized:
        return None

    return normalized


def parse_render_limit(segment_count: int) -> int:
    raw_value = optional_env_value(RENDER_LIMIT_ENV)
    if raw_value is None:
        return 0

    try:
        parsed = int(raw_value)
    except ValueError as exc:
        raise AudioRendererError(f"{RENDER_LIMIT_ENV} must be an integer") from exc

    if parsed < 0:
        raise AudioRendererError(f"{RENDER_LIMIT_ENV} must be >= 0")

    return min(parsed, segment_count)


def repo_relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError as exc:
        raise AudioRendererError(f"path is outside repo root: {path}") from exc


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


def render_segment_with_elevenlabs(
    segment: dict[str, Any],
    api_key: str,
    voice_id: str,
    model_id: str,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": segment["voiceover_text"],
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120, context=ssl.create_default_context()) as response:
            body = response.read()

            if response.status != 200:
                raise AudioRendererError(f"ElevenLabs unexpected HTTP status: {response.status}")

            if not body:
                raise AudioRendererError(f"ElevenLabs returned empty body for {segment['segment_id']}")

            output_path.write_bytes(body)

    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:500]
        raise AudioRendererError(f"ElevenLabs HTTP error {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise AudioRendererError(f"ElevenLabs URL error: {exc}") from exc


def probe_duration_sec(audio_path: Path) -> float:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(audio_path),
    ]

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )

    if completed.returncode != 0:
        raise AudioRendererError(
            f"ffprobe failed for {audio_path}: {completed.stderr.strip()}"
        )

    try:
        payload = json.loads(completed.stdout)
        duration_raw = payload["format"]["duration"]
        duration = float(duration_raw)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise AudioRendererError(f"ffprobe duration parse failed for {audio_path}") from exc

    if duration <= 0:
        raise AudioRendererError(f"ffprobe duration must be positive for {audio_path}")

    return round(duration, 3)


def build_blockers(
    api_key_present: bool,
    voice_profile: str | None,
    voice_id: str | None,
    render_limit: int,
    rendered_segment_count: int,
    segment_count: int,
    duration_validated: bool,
    loudness_validated: bool,
) -> list[str]:
    blockers: list[str] = []

    if not api_key_present:
        blockers.append("TTS API key is missing from environment")

    if voice_profile is None:
        blockers.append("voice profile is missing from environment")

    if voice_id is None:
        blockers.append("provider voice id is missing from environment")

    if render_limit <= 0:
        blockers.append("audio render limit is not enabled")

    if rendered_segment_count < segment_count:
        blockers.append("audio files were not fully rendered")

    if not duration_validated:
        blockers.append("project duration validation was not completed")

    if not loudness_validated:
        blockers.append("loudness validation was not performed")

    return blockers


def build_missing_requirements(
    api_key_present: bool,
    provider_selected: bool,
    voice_profile: str | None,
    voice_id: str | None,
    all_segments_rendered: bool,
    duration_validated: bool,
    loudness_validated: bool,
) -> list[str]:
    missing = list(REQUIRED_MISSING_REQUIREMENTS)

    if provider_selected and "selected TTS provider" in missing:
        missing.remove("selected TTS provider")

    if api_key_present and "TTS API key" in missing:
        missing.remove("TTS API key")

    if voice_profile is not None and voice_id is not None:
        if "selected voice profile" in missing:
            missing.remove("selected voice profile")

    if all_segments_rendered and "rendered audio files" in missing:
        missing.remove("rendered audio files")

    if duration_validated and "audio duration validation" in missing:
        missing.remove("audio duration validation")

    if loudness_validated and "loudness validation" in missing:
        missing.remove("loudness validation")

    return missing


def output_path_for_segment(audio_dir: Path, segment: dict[str, Any]) -> Path:
    segment_id = require_non_empty_string(segment["segment_id"], "segment.segment_id")
    return audio_dir / OUTPUT_AUDIO_DIRNAME / f"{segment_id}.mp3"


def build_rendered_segment(
    segment: dict[str, Any],
    audio_output_path: Path,
    duration_sec: float,
    reused_existing_file: bool,
) -> dict[str, Any]:
    duration_delta_sec = round(duration_sec - float(segment["estimated_duration_sec"]), 3)

    return {
        "segment_id": segment["segment_id"],
        "source_scene_id": segment["source_scene_id"],
        "order": segment["order"],
        "tts_status": "rendered",
        "voiceover_text": segment["voiceover_text"],
        "audio_path": repo_relative_path(audio_output_path),
        "provider_job_id": None,
        "duration_sec": duration_sec,
        "estimated_duration_sec": segment["estimated_duration_sec"],
        "duration_delta_sec": duration_delta_sec,
        "duration_validated": True,
        "provider_status": "rendered",
        "reused_existing_file": reused_existing_file,
        "error_message": None,
    }


def build_failed_segment(segment: dict[str, Any], error_message: str) -> dict[str, Any]:
    return {
        "segment_id": segment["segment_id"],
        "source_scene_id": segment["source_scene_id"],
        "order": segment["order"],
        "tts_status": "failed",
        "voiceover_text": segment["voiceover_text"],
        "audio_path": None,
        "provider_job_id": None,
        "duration_sec": 0,
        "estimated_duration_sec": segment["estimated_duration_sec"],
        "duration_delta_sec": None,
        "duration_validated": False,
        "provider_status": "failed",
        "reused_existing_file": False,
        "error_message": error_message,
    }


def build_pending_segment(segment: dict[str, Any]) -> dict[str, Any]:
    return {
        "segment_id": segment["segment_id"],
        "source_scene_id": segment["source_scene_id"],
        "order": segment["order"],
        "tts_status": "pending",
        "voiceover_text": segment["voiceover_text"],
        "audio_path": None,
        "provider_job_id": None,
        "duration_sec": 0,
        "estimated_duration_sec": segment["estimated_duration_sec"],
        "duration_delta_sec": None,
        "duration_validated": False,
        "provider_status": "not_rendered",
        "reused_existing_file": False,
        "error_message": "segment was not selected by render limit",
    }


def build_segments(
    audio_segments: list[dict[str, Any]],
    render_limit: int,
    api_key: str | None,
    voice_id: str | None,
    model_id: str,
    audio_dir: Path,
) -> tuple[list[dict[str, Any]], int, int, float]:
    rendered_segments: list[dict[str, Any]] = []
    rendered_segment_count = 0
    failed_segment_count = 0
    total_duration_sec = 0.0

    can_render = api_key is not None and voice_id is not None and render_limit > 0

    for index, segment in enumerate(audio_segments, start=1):
        should_render = can_render and index <= render_limit
        audio_output_path = output_path_for_segment(audio_dir, segment)

        if should_render:
            try:
                reused_existing_file = False

                if audio_output_path.exists() and audio_output_path.stat().st_size > 0:
                    duration_sec = probe_duration_sec(audio_output_path)
                    reused_existing_file = True
                else:
                    render_segment_with_elevenlabs(
                        segment=segment,
                        api_key=api_key,
                        voice_id=voice_id,
                        model_id=model_id,
                        output_path=audio_output_path,
                    )
                    duration_sec = probe_duration_sec(audio_output_path)

                rendered_segment_count += 1
                total_duration_sec = round(total_duration_sec + duration_sec, 3)

                rendered_segments.append(
                    build_rendered_segment(
                        segment=segment,
                        audio_output_path=audio_output_path,
                        duration_sec=duration_sec,
                        reused_existing_file=reused_existing_file,
                    )
                )
            except (AudioRendererError, OSError) as exc:
                failed_segment_count += 1
                rendered_segments.append(build_failed_segment(segment, str(exc)))
        else:
            rendered_segments.append(build_pending_segment(segment))

    return rendered_segments, rendered_segment_count, failed_segment_count, total_duration_sec


def run_audio_renderer(state_path: Path) -> dict[str, Any]:
    load_env_file_if_present(REPO_ROOT / ".env")

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

    api_key = optional_env_value(API_KEY_ENV)
    voice_profile = optional_env_value(VOICE_PROFILE_ENV)
    voice_id = optional_env_value(VOICE_ID_ENV)
    model_id = optional_env_value(MODEL_ID_ENV) or DEFAULT_MODEL_ID

    api_key_present = api_key is not None
    provider_selected = api_key_present
    render_limit = parse_render_limit(segment_count)

    now = utc_now_iso()
    audio_dir = state_path.parent / "audio"
    audio_render_path = audio_dir / "audio_render.json"

    rendered_segments, rendered_segment_count, failed_segment_count, total_duration_sec = build_segments(
        audio_segments=audio_segments,
        render_limit=render_limit,
        api_key=api_key,
        voice_id=voice_id,
        model_id=model_id,
        audio_dir=audio_dir,
    )

    all_segments_rendered = rendered_segment_count == segment_count and failed_segment_count == 0
    duration_validated = all_segments_rendered
    loudness_validated = False
    audio_ready = all_segments_rendered and duration_validated and loudness_validated

    blockers = build_blockers(
        api_key_present=api_key_present,
        voice_profile=voice_profile,
        voice_id=voice_id,
        render_limit=render_limit,
        rendered_segment_count=rendered_segment_count,
        segment_count=segment_count,
        duration_validated=duration_validated,
        loudness_validated=loudness_validated,
    )

    missing_requirements = build_missing_requirements(
        api_key_present=api_key_present,
        provider_selected=provider_selected,
        voice_profile=voice_profile,
        voice_id=voice_id,
        all_segments_rendered=all_segments_rendered,
        duration_validated=duration_validated,
        loudness_validated=loudness_validated,
    )

    audio_render = {
        "project_id": project_id,
        "renderer": RENDERER_NAME,
        "renderer_version": RENDERER_VERSION,
        "source_audio_plan_path": str(audio_plan_path),
        "tts_provider": SUPPORTED_PROVIDER if provider_selected else None,
        "voice_profile": voice_profile,
        "provider_voice_id": voice_id,
        "model_id": model_id,
        "audio_status": "ready" if audio_ready else "partial" if rendered_segment_count > 0 else "blocked",
        "audio_ready": audio_ready,
        "rendered_at": now,
        "segment_count": segment_count,
        "render_limit": render_limit,
        "rendered_segment_count": rendered_segment_count,
        "failed_segment_count": failed_segment_count,
        "total_duration_sec": total_duration_sec,
        "target_duration_sec": target_duration_sec,
        "duration_validated": duration_validated,
        "loudness_validated": loudness_validated,
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
        "render_limit": audio_render["render_limit"],
        "rendered_segment_count": audio_render["rendered_segment_count"],
        "failed_segment_count": audio_render["failed_segment_count"],
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
