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

EXECUTOR_NAME = "assets_executor"
EXECUTOR_VERSION = "1.0.0"

ALLOWED_ASSET_TYPES = {
    "stock_video",
    "stock_image",
    "simple_motion_text",
    "chart_or_bill_visual",
    "screen_style_visual",
}

ALLOWED_USAGE_ROLES = {
    "primary_visual",
    "supporting_visual",
    "text_overlay",
    "diagnostic_visual",
    "transition_visual",
}

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


class AssetsExecutorError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise AssetsExecutorError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise AssetsExecutorError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise AssetsExecutorError(f"{field_name} must be an integer")

    if value <= 0:
        raise AssetsExecutorError(f"{field_name} must be > 0")

    return value


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssetsExecutorError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssetsExecutorError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise AssetsExecutorError(f"JSON file must contain an object: {path}")

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
        raise AssetsExecutorError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def normalize_query(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s/-]", " ", value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip().lower()
    if not cleaned:
        raise AssetsExecutorError("asset query became empty after normalization")
    return cleaned


def build_asset_query(asset_type: str, visual_intent: str, topic: str) -> str:
    base_topic = normalize_query(topic)
    visual = normalize_query(visual_intent)

    if asset_type == "simple_motion_text":
        return normalize_query(f"minimal animated text {base_topic}")

    if asset_type == "chart_or_bill_visual":
        return normalize_query("utility bill cost breakdown usage rate fixed charges")

    if asset_type == "screen_style_visual":
        return normalize_query("checklist compare electricity bill usage rate fixed charges")

    if asset_type == "stock_video":
        return normalize_query("home appliances electricity usage refrigerator water heater")

    if asset_type == "stock_image":
        return normalize_query(f"household energy costs simple home finance {base_topic}")

    return visual


def choose_usage_role(asset_type: str) -> str:
    if asset_type == "simple_motion_text":
        return "text_overlay"

    if asset_type in {"chart_or_bill_visual", "screen_style_visual"}:
        return "diagnostic_visual"

    if asset_type == "stock_video":
        return "primary_visual"

    if asset_type == "stock_image":
        return "supporting_visual"

    raise AssetsExecutorError(f"unsupported asset_type: {asset_type}")


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
        raise AssetsExecutorError(
            f"scene index {index} missing fields: {', '.join(missing)}"
        )

    require_non_empty_string(scene["scene_id"], f"scene[{index}].scene_id")
    require_non_empty_string(scene["voiceover_text"], f"scene[{index}].voiceover_text")
    require_non_empty_string(scene["visual_intent"], f"scene[{index}].visual_intent")
    require_non_empty_string(scene["on_screen_text"], f"scene[{index}].on_screen_text")
    require_non_empty_string(scene["asset_type"], f"scene[{index}].asset_type")
    require_non_empty_string(scene["production_notes"], f"scene[{index}].production_notes")
    require_positive_int(scene["order"], f"scene[{index}].order")
    require_positive_int(scene["estimated_duration_sec"], f"scene[{index}].estimated_duration_sec")

    if scene["asset_type"] not in ALLOWED_ASSET_TYPES:
        raise AssetsExecutorError(
            f"scene[{index}].asset_type is unsupported: {scene['asset_type']}"
        )

    for field_name in ("voiceover_text", "visual_intent", "on_screen_text", "production_notes"):
        fail_if_forbidden_markers(str(scene[field_name]), f"scene[{index}].{field_name}")


def build_asset_entry(scene: dict[str, Any], topic: str) -> dict[str, Any]:
    scene_id = require_non_empty_string(scene["scene_id"], "scene.scene_id")
    order = require_positive_int(scene["order"], f"{scene_id}.order")
    asset_type = require_non_empty_string(scene["asset_type"], f"{scene_id}.asset_type")
    visual_intent = require_non_empty_string(scene["visual_intent"], f"{scene_id}.visual_intent")
    estimated_duration_sec = require_positive_int(
        scene["estimated_duration_sec"],
        f"{scene_id}.estimated_duration_sec",
    )

    if asset_type not in ALLOWED_ASSET_TYPES:
        raise AssetsExecutorError(f"{scene_id}.asset_type is unsupported: {asset_type}")

    usage_role = choose_usage_role(asset_type)
    asset_query = build_asset_query(asset_type, visual_intent, topic)

    return {
        "asset_id": f"ASSET_{order:03d}",
        "scene_id": scene_id,
        "order": order,
        "asset_type": asset_type,
        "asset_query": asset_query,
        "visual_intent": visual_intent,
        "usage_role": usage_role,
        "estimated_duration_sec": estimated_duration_sec,
        "required": True,
        "provider_status": "planned",
        "local_path": None,
        "source_url": None,
        "license_status": "pending",
        "production_notes": (
            "Planning-only asset entry. No external provider called. "
            "Resolve media source in a later provider integration phase."
        ),
    }


def validate_asset_entry(asset: dict[str, Any], index: int) -> None:
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

    missing = sorted(required_fields - set(asset.keys()))
    if missing:
        raise AssetsExecutorError(
            f"asset index {index} missing fields: {', '.join(missing)}"
        )

    require_non_empty_string(asset["asset_id"], f"asset[{index}].asset_id")
    require_non_empty_string(asset["scene_id"], f"asset[{index}].scene_id")
    require_positive_int(asset["order"], f"asset[{index}].order")
    require_non_empty_string(asset["asset_type"], f"asset[{index}].asset_type")
    require_non_empty_string(asset["asset_query"], f"asset[{index}].asset_query")
    require_non_empty_string(asset["visual_intent"], f"asset[{index}].visual_intent")
    require_non_empty_string(asset["usage_role"], f"asset[{index}].usage_role")
    require_positive_int(asset["estimated_duration_sec"], f"asset[{index}].estimated_duration_sec")
    require_non_empty_string(asset["provider_status"], f"asset[{index}].provider_status")
    require_non_empty_string(asset["license_status"], f"asset[{index}].license_status")
    require_non_empty_string(asset["production_notes"], f"asset[{index}].production_notes")

    if asset["asset_type"] not in ALLOWED_ASSET_TYPES:
        raise AssetsExecutorError(
            f"asset[{index}].asset_type unsupported: {asset['asset_type']}"
        )

    if asset["usage_role"] not in ALLOWED_USAGE_ROLES:
        raise AssetsExecutorError(
            f"asset[{index}].usage_role unsupported: {asset['usage_role']}"
        )

    if asset["provider_status"] != "planned":
        raise AssetsExecutorError(
            f"asset[{index}].provider_status must be planned in v1"
        )

    if asset["local_path"] is not None:
        raise AssetsExecutorError(f"asset[{index}].local_path must be null in v1")

    if asset["source_url"] is not None:
        raise AssetsExecutorError(f"asset[{index}].source_url must be null in v1")

    if asset["license_status"] != "pending":
        raise AssetsExecutorError(
            f"asset[{index}].license_status must be pending in v1"
        )

    if asset["required"] is not True:
        raise AssetsExecutorError(f"asset[{index}].required must be true")

    for field_name in ("asset_query", "visual_intent", "production_notes"):
        fail_if_forbidden_markers(str(asset[field_name]), f"asset[{index}].{field_name}")


def validate_scenes_payload(scenes_payload: dict[str, Any]) -> list[dict[str, Any]]:
    scene_count = require_positive_int(
        scenes_payload.get("scene_count"),
        "scenes.scene_count",
    )

    scenes = scenes_payload.get("scenes")
    if not isinstance(scenes, list):
        raise AssetsExecutorError("scenes.scenes must be a list")

    if not scenes:
        raise AssetsExecutorError("scenes.scenes must not be empty")

    if scene_count != len(scenes):
        raise AssetsExecutorError(
            f"scene_count mismatch: scene_count={scene_count}, actual={len(scenes)}"
        )

    if scene_count < 6:
        raise AssetsExecutorError(f"scene_count below minimum: {scene_count}")

    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            raise AssetsExecutorError(f"scene index {index} must be an object")
        validate_scene(scene, index)

    return scenes


def run_assets_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "ASSETS":
        raise AssetsExecutorError("ASSETS executor may run only when phase is ASSETS")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]
    artifacts = state.get("artifacts", {})

    if not isinstance(artifacts, dict):
        raise AssetsExecutorError("artifacts must be an object")

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
    stock_policy = require_non_empty_string(
        manifest.get("stock_policy"),
        "manifest.stock_policy",
    )

    scenes_path = Path(
        require_non_empty_string(artifacts.get("scenes_path"), "artifacts.scenes_path")
    )
    script_qa_path = Path(
        require_non_empty_string(artifacts.get("script_qa_path"), "artifacts.script_qa_path")
    )

    script_qa = read_json_file(script_qa_path)
    if script_qa.get("verdict") != "PASS":
        raise AssetsExecutorError("ASSETS executor requires script_qa.verdict=PASS")

    scenes_payload = read_json_file(scenes_path)
    scenes = validate_scenes_payload(scenes_payload)

    assets = [build_asset_entry(scene, topic) for scene in scenes]

    if len(assets) < len(scenes):
        raise AssetsExecutorError("asset_count below scene_count")

    for index, asset in enumerate(assets, start=1):
        validate_asset_entry(asset, index)

    scene_ids = [scene["scene_id"] for scene in scenes]
    asset_scene_ids = [asset["scene_id"] for asset in assets]
    if scene_ids != asset_scene_ids:
        raise AssetsExecutorError("asset scene_id mapping does not preserve scene order")

    now = utc_now_iso()
    assets_path = state_path.parent / "assets" / "assets.json"

    assets_payload = {
        "project_id": project_id,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "source_phase": state["phase"],
        "source_scenes_path": str(scenes_path),
        "topic": topic,
        "working_title": working_title,
        "hook": hook,
        "niche": niche,
        "audience": audience,
        "content_language": content_language,
        "primary_platform": primary_platform,
        "target_duration_sec": target_duration_sec,
        "stock_policy": stock_policy,
        "asset_count": len(assets),
        "assets": assets,
        "created_at": now,
    }

    serialized = json.dumps(assets_payload, ensure_ascii=False)
    fail_if_forbidden_markers(serialized, "assets_payload")

    write_json_atomic(assets_path, assets_payload)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["assets_path"] = str(assets_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "ASSETS_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "assets_path": str(assets_path),
        "asset_count": len(assets),
        "provider_status": "planned",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind canonical ASSETS executor v1")
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
        result = run_assets_executor(Path(args.state))
    except (AssetsExecutorError, StateValidationError, OSError) as exc:
        print(f"[ASSETS_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
