import json
from datetime import UTC, datetime
from pathlib import Path


class AudioEngineError(Exception):
    pass


class AudioEngine:
    """
    FlowMind Audio Engine v1

    Canonical behavior:
    - reads PROJECT_STATE.json
    - validates script presence
    - resolves project-scoped local audio files only
    - writes outputs into PROJECT_STATE["artifacts"]

    Required local inputs:
    - projects/<PROJECT_ID>/script.txt
    - projects/<PROJECT_ID>/audio/voice_track.wav
    - projects/<PROJECT_ID>/audio/background_music.wav

    Fail-closed:
    - missing state
    - missing script
    - missing voice
    - missing music
    """

    LOUDNESS_TARGET_LUFS = -14
    DUCKING_ENABLED = True
    AUDIO_VERSION = 1

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.state_path = self.project_dir / "PROJECT_STATE.json"
        self.state = self._load_state()
        self.script_path = self._resolve_required_path("script_path")

    def run(self) -> Path:
        self._require_file(self.script_path, "Missing script")

        voice_path = self.project_dir / "audio" / "voice_track.wav"
        music_path = self.project_dir / "audio" / "background_music.wav"

        self._require_file(voice_path, "Missing voice audio")
        self._require_file(music_path, "Missing background music")

        artifacts = self.state.get("artifacts")
        if artifacts is None:
            artifacts = {}
        if not isinstance(artifacts, dict):
            raise AudioEngineError('PROJECT_STATE["artifacts"] must be an object')

        artifacts["voice_path"] = str(voice_path)
        artifacts["music_path"] = str(music_path)
        artifacts["audio"] = {
            "audio_version": self.AUDIO_VERSION,
            "loudness_target_lufs": self.LOUDNESS_TARGET_LUFS,
            "ducking_enabled": self.DUCKING_ENABLED,
            "voice_track_verified": True,
        }

        self.state["artifacts"] = artifacts
        self.state["audio_generated"] = True
        self.state["updated_at"] = self._now_iso()

        self._save_state()
        return self.state_path

    def _load_state(self) -> dict:
        if not self.state_path.exists():
            raise AudioEngineError("PROJECT_STATE.json missing")

        try:
            with self.state_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise AudioEngineError(f"Invalid PROJECT_STATE.json: {exc}") from exc
        except OSError as exc:
            raise AudioEngineError(f"Failed to read PROJECT_STATE.json: {exc}") from exc

        if not isinstance(data, dict):
            raise AudioEngineError("PROJECT_STATE.json must contain an object")

        return data

    def _save_state(self) -> None:
        try:
            with self.state_path.open("w", encoding="utf-8") as handle:
                json.dump(self.state, handle, indent=2, ensure_ascii=False)
        except OSError as exc:
            raise AudioEngineError(f"Failed to write PROJECT_STATE.json: {exc}") from exc

    def _resolve_required_path(self, key: str) -> Path:
        raw_value = self.state.get(key)
        if not raw_value or not isinstance(raw_value, str):
            raise AudioEngineError(f"Missing required state field: {key}")

        raw_path = Path(raw_value)

        if raw_path.is_absolute():
            return raw_path

        project_prefixed = Path("projects") / self.project_dir.name
        if raw_path.parts[: len(project_prefixed.parts)] == project_prefixed.parts:
            return Path.cwd() / raw_path

        return self.project_dir / raw_path

    def _require_file(self, path: Path, message: str) -> None:
        if not path.exists():
            raise AudioEngineError(f"{message}: {path}")
        if not path.is_file():
            raise AudioEngineError(f"Expected file but found non-file path: {path}")

    def _now_iso(self) -> str:
        return datetime.now(UTC).isoformat()
