import json
from datetime import UTC, datetime
from pathlib import Path


class AssetEngineError(Exception):
    pass


class AssetEngine:
    """
    FlowMind Asset Engine v1

    Canonical behavior:
    - reads PROJECT_STATE.json
    - reads Director output from state["scene_plan_path"]
    - resolves project-scoped local assets only
    - writes all outputs into PROJECT_STATE["artifacts"]

    Required local inputs:
    - projects/<PROJECT_ID>/audio/voice.wav
    - projects/<PROJECT_ID>/audio/music.wav
    - projects/<PROJECT_ID>/assets/resolved/<shot_id>.mp4

    Fail-closed:
    - missing state
    - missing scene plan
    - missing audio
    - missing resolved asset
    - duplicate asset reuse when no_repeat=true
    """

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.state_path = self.project_dir / "PROJECT_STATE.json"
        self.state = self._load_state()
        self.scene_plan_path = self._resolve_required_path("scene_plan_path")

    def run(self) -> Path:
        scene_payload = self._load_scene_payload()
        shot_plan = scene_payload.get("shot_plan")

        if not isinstance(shot_plan, list) or not shot_plan:
            raise AssetEngineError("scene_plan.json missing valid shot_plan")

        voice_path = self.project_dir / "audio" / "voice.wav"
        music_path = self.project_dir / "audio" / "music.wav"

        self._require_file(voice_path, "Missing voice audio")
        self._require_file(music_path, "Missing music audio")

        assets_map = self._build_assets_map(shot_plan)
        timeline = self._build_timeline(shot_plan)

        artifacts = self.state.get("artifacts")
        if artifacts is None:
            artifacts = {}
        if not isinstance(artifacts, dict):
            raise AssetEngineError('PROJECT_STATE["artifacts"] must be an object')

        artifacts["voice_path"] = str(voice_path)
        artifacts["music_path"] = str(music_path)
        artifacts["assets_map"] = assets_map
        artifacts["timeline"] = timeline

        self.state["artifacts"] = artifacts
        self.state["updated_at"] = self._now_iso()

        self._save_state()
        return self.state_path

    def _load_state(self) -> dict:
        if not self.state_path.exists():
            raise AssetEngineError("PROJECT_STATE.json missing")

        try:
            with self.state_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise AssetEngineError(f"Invalid PROJECT_STATE.json: {exc}") from exc
        except OSError as exc:
            raise AssetEngineError(f"Failed to read PROJECT_STATE.json: {exc}") from exc

        if not isinstance(data, dict):
            raise AssetEngineError("PROJECT_STATE.json must contain an object")

        return data

    def _save_state(self) -> None:
        try:
            with self.state_path.open("w", encoding="utf-8") as handle:
                json.dump(self.state, handle, indent=2, ensure_ascii=False)
        except OSError as exc:
            raise AssetEngineError(f"Failed to write PROJECT_STATE.json: {exc}") from exc

    def _resolve_required_path(self, key: str) -> Path:
        raw_value = self.state.get(key)
        if not raw_value or not isinstance(raw_value, str):
            raise AssetEngineError(f"Missing required state field: {key}")

        raw_path = Path(raw_value)

        if raw_path.is_absolute():
            return raw_path

        project_prefixed = Path("projects") / self.project_dir.name
        if raw_path.parts[: len(project_prefixed.parts)] == project_prefixed.parts:
            return Path.cwd() / raw_path

        return self.project_dir / raw_path

    def _load_scene_payload(self) -> dict:
        if not self.scene_plan_path.exists():
            raise AssetEngineError(f"scene_plan.json missing: {self.scene_plan_path}")

        try:
            with self.scene_plan_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise AssetEngineError(f"Invalid scene_plan.json: {exc}") from exc
        except OSError as exc:
            raise AssetEngineError(f"Failed to read scene_plan.json: {exc}") from exc

        if not isinstance(data, dict):
            raise AssetEngineError("scene_plan.json must contain an object")

        return data

    def _build_assets_map(self, shot_plan: list[dict]) -> list[dict]:
        resolved_dir = self.project_dir / "assets" / "resolved"
        used_paths: set[str] = set()
        assets_map: list[dict] = []

        for shot in shot_plan:
            shot_id = shot.get("shot_id")
            visual = shot.get("visual")
            constraints = shot.get("constraints")

            if not isinstance(shot_id, str) or not shot_id.strip():
                raise AssetEngineError("Shot missing valid shot_id")

            if not isinstance(visual, dict):
                raise AssetEngineError(f"Shot {shot_id} missing visual block")

            if not isinstance(constraints, dict):
                raise AssetEngineError(f"Shot {shot_id} missing constraints block")

            asset_type = visual.get("asset_type")
            if asset_type != "video":
                raise AssetEngineError(
                    f"Unsupported asset_type for {shot_id}: {asset_type}. Asset Engine v1 supports video only."
                )

            asset_path = resolved_dir / f"{shot_id}.mp4"
            self._require_file(asset_path, f"Missing resolved asset for {shot_id}")

            normalized_asset_path = str(asset_path)

            if constraints.get("no_repeat") is True and normalized_asset_path in used_paths:
                raise AssetEngineError(f"Repeated asset detected for {shot_id}: {normalized_asset_path}")

            used_paths.add(normalized_asset_path)

            assets_map.append(
                {
                    "shot_id": shot_id,
                    "asset_type": asset_type,
                    "asset_path": normalized_asset_path,
                }
            )

        if not assets_map:
            raise AssetEngineError("No assets resolved")

        return assets_map

    def _build_timeline(self, shot_plan: list[dict]) -> list[dict]:
        timeline: list[dict] = []

        previous_end: float | None = None

        for shot in shot_plan:
            shot_id = shot.get("shot_id")
            timing = shot.get("timing")

            if not isinstance(shot_id, str) or not shot_id.strip():
                raise AssetEngineError("Shot missing valid shot_id for timeline")

            if not isinstance(timing, dict):
                raise AssetEngineError(f"Shot {shot_id} missing timing block")

            start = timing.get("start")
            end = timing.get("end")

            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                raise AssetEngineError(f"Shot {shot_id} has invalid timing values")

            start_float = float(start)
            end_float = float(end)

            if end_float <= start_float:
                raise AssetEngineError(f"Shot {shot_id} has non-positive duration")

            if previous_end is not None and start_float != previous_end:
                raise AssetEngineError(
                    f"Timeline gap or overlap detected before {shot_id}: start={start_float}, previous_end={previous_end}"
                )

            timeline.append(
                {
                    "shot_id": shot_id,
                    "start": start_float,
                    "end": end_float,
                }
            )

            previous_end = end_float

        if not timeline:
            raise AssetEngineError("Timeline is empty")

        return timeline

    def _require_file(self, path: Path, message: str) -> None:
        if not path.exists():
            raise AssetEngineError(f"{message}: {path}")
        if not path.is_file():
            raise AssetEngineError(f"Expected file but found non-file path: {path}")

    def _now_iso(self) -> str:
        return datetime.now(UTC).isoformat()
