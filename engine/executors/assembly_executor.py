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

EXECUTOR_NAME = "assembly_executor"
EXECUTOR_VERSION = "1.0.0"
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
    "resolved media asset files",
    "cleared asset licenses",
    "audio artifact",
    "final render executor",
)


class AssemblyExecutorError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise AssemblyExecutorError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise AssemblyExecutorError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise AssemblyExecutorError(f"{field_name} must be an integer")

    if value <= 0:
        raise AssemblyExecutorError(f"{field_name} must be > 0")

    return value


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssemblyExecutorError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssemblyExecutorError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise AssemblyExecutorError(f"JSON file must contain an object: {path}")

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
        raise AssemblyExecutorError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def expected_duration_range(target_duration_sec: int) -> tuple[int, int]:
    min_duration = int(round(target_duration_sec * (1.0 - ALLOWED_DURATION_DRIFT)))
    max_duration = int(round(target_duration_sec * (1.0 + ALLOWED_DURATION_DRIFT)))
    return min_duration, max_duration


def validate_duration(estimated_total_duration_sec: int, target_duration_sec: int) -> None:
    min_duration, max_duration = expected_duration_range(target_duration_sec)
    if not (min_duration <= estimated_total_duration_sec <= max_duration):
        raise AssemblyExecutorError(
            "estimated_total_duration_sec outside allowed range: "
            f"{estimated_total_duration_sec}, allowed={min_duration}-{max_duration}"
        )


def validate_script_qa(script_qa: dict[str, Any]) -> None:
    if script_qa.get("verdict") != "PASS":
        raise AssemblyExecutorError("ASSEMBLY executor requires script_qa.verdict=PASS")


def validate_scenes_payload(scenes_payload: dict[str, Any]) -> list[dict[str, Any]]:
    scene_count = require_positive_int(
        scenes_payload.get("scene_count"),
        "scenes.scene_count",
    )

    scenes = scenes_payload.get("scenes")
    if not isinstance(scenes, list):
        raise AssemblyExecutorError("scenes.scenes must be a list")

    if scene_count != len(scenes):
        raise AssemblyExecutorError(
            f"scene_count mismatch: scene_count={scene_count}, actual={len(scenes)}"
        )

    if scene_count < 6:
        raise AssemblyExecutorError(f"scene_count below minimum: {scene_count}")

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

    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            raise AssemblyExecutorError(f"scene index {index} must be an object")

        missing = sorted(required_fields - set(scene.keys()))
        if missing:
            raise AssemblyExecutorError(
                f"scene index {index} missing fields: {', '.join(missing)}"
            )

        require_non_empty_string(scene["scene_id"], f"scene[{index}].scene_id")
        require_positive_int(scene["order"], f"scene[{index}].order")
        require_non_empty_string(scene["voiceover_text"], f"scene[{index}].voiceover_text")
        require_non_empty_string(scene["visual_intent"], f"scene[{index}].visual_intent")
        require_non_empty_string(scene["on_screen_text"], f"scene[{index}].on_screen_text")
        require_non_empty_string(scene["asset_type"], f"scene[{index}].asset_type")
        require_positive_int(
            scene["estimated_duration_sec"],
            f"scene[{index}].estimated_duration_sec",
        )
        require_non_empty_string(
            scene["production_notes"],
            f"scene[{index}].production_notes",
        )

        serialized = json.dumps(scene, ensure_ascii=False)
        fail_if_forbidden_markers(serialized, f"scene[{index}]")

    return scenes


def validate_assets_payload(assets_payload: dict[str, Any], scene_count: int) -> list[dict[str, Any]]:
    asset_count = require_positive_int(
        assets_payload.get("asset_count"),
        "assets.asset_count",
    )

    assets = assets_payload.get("assets")
    if not isinstance(assets, list):
        raise AssemblyExecutorError("assets.assets must be a list")

    if asset_count != len(assets):
        raise AssemblyExecutorError(
            f"asset_count mismatch: asset_count={asset_count}, actual={len(assets)}"
        )

    if asset_count < scene_count:
        raise AssemblyExecutorError(
            f"asset_count below scene_count: asset_count={asset_count}, scene_count={scene_count}"
        )

    required_fields = {
        "asset_id",
        "scene_id",
        "order",
        "asset_type",
        "asset_query",
        "visual_intent",
        "usage_role",
        "estimated_duration_sec",
        "required",
        "provider_status",
        "local_path",
        "source_url",
        "license_status",
        "production_notes",
    }

    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            raise AssemblyExecutorError(f"asset index {index} must be an object")

        missing = sorted(required_fields - set(asset.keys()))
        if missing:
            raise AssemblyExecutorError(
                f"asset index {index} missing fields: {', '.join(missing)}"
            )

        require_non_empty_string(asset["asset_id"], f"asset[{index}].asset_id")
        require_non_empty_string(asset["scene_id"], f"asset[{index}].scene_id")
        require_positive_int(asset["order"], f"asset[{index}].order")
        require_non_empty_string(asset["asset_type"], f"asset[{index}].asset_type")
        require_non_empty_string(asset["asset_query"], f"asset[{index}].asset_query")
        require_non_empty_string(asset["visual_intent"], f"asset[{index}].visual_intent")
        require_non_empty_string(asset["usage_role"], f"asset[{index}].usage_role")
        require_positive_int(
            asset["estimated_duration_sec"],
            f"asset[{index}].estimated_duration_sec",
        )
        require_non_empty_string(asset["provider_status"], f"asset[{index}].provider_status")
        require_non_empty_string(asset["license_status"], f"asset[{index}].license_status")
        require_non_empty_string(asset["production_notes"], f"asset[{index}].production_notes")

        if asset["provider_status"] != "planned":
            raise AssemblyExecutorError(
                f"asset[{index}].provider_status must be planned in ASSEMBLY v1"
            )

        if asset["license_status"] != "pending":
            raise AssemblyExecutorError(
                f"asset[{index}].license_status must be pending in ASSEMBLY v1"
            )

        if asset["local_path"] is not None:
            raise AssemblyExecutorError(f"asset[{index}].local_path must be null in ASSEMBLY v1")

        if asset["source_url"] is not None:
            raise AssemblyExecutorError(f"asset[{index}].source_url must be null in ASSEMBLY v1")

        if asset["required"] is not True:
            raise AssemblyExecutorError(f"asset[{index}].required must be true")

        serialized = json.dumps(asset, ensure_ascii=False)
        fail_if_forbidden_markers(serialized, f"asset[{index}]")

    return assets


def build_asset_index(assets: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    asset_index: dict[str, dict[str, Any]] = {}

    for asset in assets:
        scene_id = str(asset["scene_id"])
        if scene_id in asset_index:
            raise AssemblyExecutorError(f"duplicate asset for scene_id: {scene_id}")
        asset_index[scene_id] = asset

    return asset_index


def build_timeline_item(scene: dict[str, Any], asset: dict[str, Any]) -> dict[str, Any]:
    scene_id = require_non_empty_string(scene["scene_id"], "scene.scene_id")

    if asset["scene_id"] != scene_id:
        raise AssemblyExecutorError(
            f"asset scene_id mismatch: scene_id={scene_id}, asset_scene_id={asset['scene_id']}"
        )

    return {
        "timeline_id": f"TIMELINE_{int(scene['order']):03d}",
        "scene_id": scene_id,
        "order": int(scene["order"]),
        "voiceover_text": str(scene["voiceover_text"]),
        "estimated_duration_sec": int(scene["estimated_duration_sec"]),
        "asset_id": str(asset["asset_id"]),
        "asset_type": str(asset["asset_type"]),
        "asset_query": str(asset["asset_query"]),
        "usage_role": str(asset["usage_role"]),
        "provider_status": str(asset["provider_status"]),
        "local_path": asset["local_path"],
        "source_url": asset["source_url"],
        "visual_intent": str(scene["visual_intent"]),
        "on_screen_text": str(scene["on_screen_text"]),
        "production_notes": (
            "Assembly planning only. Render is blocked until media files, licenses, audio, "
            "and final render executor are available."
        ),
    }


def validate_timeline(timeline: list[dict[str, Any]], scene_count: int) -> None:
    if len(timeline) != scene_count:
        raise AssemblyExecutorError(
            f"timeline length mismatch: timeline={len(timeline)}, scene_count={scene_count}"
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
        missing = sorted(required_fields - set(item.keys()))
        if missing:
            raise AssemblyExecutorError(
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
        require_non_empty_string(item["asset_id"], f"timeline[{index}].asset_id")
        require_non_empty_string(item["asset_type"], f"timeline[{index}].asset_type")
        require_non_empty_string(item["asset_query"], f"timeline[{index}].asset_query")
        require_non_empty_string(item["usage_role"], f"timeline[{index}].usage_role")
        require_non_empty_string(
            item["provider_status"],
            f"timeline[{index}].provider_status",
        )
        require_non_empty_string(item["visual_intent"], f"timeline[{index}].visual_intent")
        require_non_empty_string(item["on_screen_text"], f"timeline[{index}].on_screen_text")
        require_non_empty_string(
            item["production_notes"],
            f"timeline[{index}].production_notes",
        )

        if item["provider_status"] != "planned":
            raise AssemblyExecutorError(
                f"timeline[{index}].provider_status must be planned in ASSEMBLY v1"
            )

        if item["local_path"] is not None:
            raise AssemblyExecutorError(f"timeline[{index}].local_path must be null in ASSEMBLY v1")

        if item["source_url"] is not None:
            raise AssemblyExecutorError(f"timeline[{index}].source_url must be null in ASSEMBLY v1")

        serialized = json.dumps(item, ensure_ascii=False)
        fail_if_forbidden_markers(serialized, f"timeline[{index}]")


def run_assembly_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "ASSEMBLY":
        raise AssemblyExecutorError("ASSEMBLY executor may run only when phase is ASSEMBLY")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]
    artifacts = state.get("artifacts", {})

    if not isinstance(artifacts, dict):
        raise AssemblyExecutorError("artifacts must be an object")

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
    target_duration_sec = require_positive_int(
        manifest.get("target_duration_sec"),
        "manifest.target_duration_sec",
    )
    render_profile = require_non_empty_string(
        manifest.get("render_profile"),
        "manifest.render_profile",
    )

    script_qa_path = Path(
        require_non_empty_string(artifacts.get("script_qa_path"), "artifacts.script_qa_path")
    )
    scenes_path = Path(
        require_non_empty_string(artifacts.get("scenes_path"), "artifacts.scenes_path")
    )
    assets_path = Path(
        require_non_empty_string(artifacts.get("assets_path"), "artifacts.assets_path")
    )

    script_qa = read_json_file(script_qa_path)
    validate_script_qa(script_qa)

    scenes_payload = read_json_file(scenes_path)
    assets_payload = read_json_file(assets_path)

    scenes = validate_scenes_payload(scenes_payload)
    assets = validate_assets_payload(assets_payload, len(scenes))

    estimated_total_duration_sec = require_positive_int(
        scenes_payload.get("estimated_total_duration_sec"),
        "scenes.estimated_total_duration_sec",
    )
    validate_duration(estimated_total_duration_sec, target_duration_sec)

    asset_index = build_asset_index(assets)

    timeline: list[dict[str, Any]] = []
    for scene in scenes:
        scene_id = str(scene["scene_id"])
        asset = asset_index.get(scene_id)
        if asset is None:
            raise AssemblyExecutorError(f"missing asset for scene_id: {scene_id}")

        timeline.append(build_timeline_item(scene, asset))

    validate_timeline(timeline, len(scenes))

    missing_requirements = list(REQUIRED_MISSING_REQUIREMENTS)
    now = utc_now_iso()
    assembly_plan_path = state_path.parent / "assembly" / "assembly_plan.json"

    assembly_plan = {
        "project_id": project_id,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "source_phase": state["phase"],
        "source_scenes_path": str(scenes_path),
        "source_assets_path": str(assets_path),
        "topic": topic,
        "working_title": working_title,
        "niche": niche,
        "audience": audience,
        "content_language": content_language,
        "primary_platform": primary_platform,
        "render_profile": render_profile,
        "target_duration_sec": target_duration_sec,
        "assembly_status": "planned",
        "render_ready": False,
        "scene_count": len(scenes),
        "estimated_total_duration_sec": estimated_total_duration_sec,
        "timeline": timeline,
        "missing_requirements": missing_requirements,
        "created_at": now,
    }

    serialized = json.dumps(assembly_plan, ensure_ascii=False)
    fail_if_forbidden_markers(serialized, "assembly_plan")

    write_json_atomic(assembly_plan_path, assembly_plan)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["assembly_plan_path"] = str(assembly_plan_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "ASSEMBLY_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "assembly_plan_path": str(assembly_plan_path),
        "assembly_status": "planned",
        "render_ready": False,
        "scene_count": len(scenes),
        "estimated_total_duration_sec": estimated_total_duration_sec,
        "missing_requirements": missing_requirements,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind canonical ASSEMBLY executor v1")
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
        result = run_assembly_executor(Path(args.state))
    except (AssemblyExecutorError, StateValidationError, OSError) as exc:
        print(f"[ASSEMBLY_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
