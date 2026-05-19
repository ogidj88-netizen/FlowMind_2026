from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"
OUTPUT_PATH = REPO_ROOT / "projects/P2026_TEST_001/audio/probe/elevenlabs_probe_short.mp3"

TEXT = "This is a short FlowMind voice test."

API_KEY_ENV = "ELEVENLABS_API_KEY"
VOICE_ID_ENV = "ELEVENLABS_VOICE_ID"
VOICE_PROFILE_ENV = "FLOWMIND_TTS_VOICE_PROFILE"

MODEL_ID = "eleven_multilingual_v2"


class ProbeError(RuntimeError):
    pass


def load_env_file(path: Path) -> None:
    if not path.exists():
        raise ProbeError(f".env file not found: {path}")

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ProbeError(f"{name} is missing")

    return value.strip()


def main() -> None:
    load_env_file(ENV_PATH)

    api_key = require_env(API_KEY_ENV)
    voice_id = require_env(VOICE_ID_ENV)
    voice_profile = require_env(VOICE_PROFILE_ENV)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": TEXT,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "xi-api-key": api_key,
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60, context=ssl.create_default_context()) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "")

            if response.status != 200:
                raise ProbeError(f"unexpected http status: {response.status}")

            if not body:
                raise ProbeError("empty response body")

            OUTPUT_PATH.write_bytes(body)

    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")[:500]
        raise ProbeError(f"ElevenLabs HTTP error {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise ProbeError(f"ElevenLabs URL error: {exc}") from exc

    size = OUTPUT_PATH.stat().st_size
    if size <= 0:
        raise ProbeError("output mp3 is empty")

    print("ELEVENLABS_SHORT_PROBE_OK")
    print("voice_profile_set=", bool(voice_profile))
    print("output_path=", str(OUTPUT_PATH.relative_to(REPO_ROOT)))
    print("output_size_bytes=", size)


if __name__ == "__main__":
    try:
        main()
    except ProbeError as exc:
        print(f"ELEVENLABS_SHORT_PROBE_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
