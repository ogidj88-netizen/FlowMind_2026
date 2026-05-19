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

RESOLVER_NAME = "asset_resolver"
RESOLVER_VERSION = "1.0.0"
PROVIDER_MODE = "local_existing_only"

APPROVED_ASSET_DIRS = (
    "assets_library",
    "manual_assets",
)

MEDIA_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".mp4",
    ".mov",
    ".mkv",
)

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


class AssetResolverError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise AssetResolverError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise AssetResolverError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise AssetResolverError(f"{field_name} must be an integer")

    if value <= 0:
        raise AssetResolverError(f"{field_name} must be > 0")

    return value


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssetResolverError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssetResolverError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise AssetResolverError(f"JSON file must contain an object: {path}")

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
        raise AssetResolverError(
            f"{source_name} contains forbidden markers: {', '.join(hits)}"
        )


def slug_tokens(value: str) -> set[str]:
    normalized = re.sub(r"[^a-zA-Z0-9]+", " ", value.lower())
    return {token for token in normalized.split() if len(token) >= 3}


def normalize_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def approved_search_dirs(project_id: str) -> list[Path]:
    return [
        REPO_ROOT / "assets_library",
        REPO_ROOT / "projects" / project_id / "manual_assets",
    ]


def list_candidate_media_files(search_dirs: list[Path]) -> list[Path]:
    files: list[Path] = []

    for directory in search_dirs:
        if not directory.exists():
            continue

        if not directory.is_dir():
            continue

        for path in directory.rglob("*"):
            if not path.is_file():
                continue

            if path.suffix.lower() not in MEDIA_EXTENSIONS:
                continue

            files.append(path)

    return sorted(files)


def read_license_sidecar(media_path: Path) -> dict[str, Any] | None:
    sidecar_path = media_path.with_suffix(media_path.suffix + ".license.json")
    if not sidecar_path.exists():
        return None

    return read_json_file(sidecar_path)


def license_is_cleared(media_path: Path) -> tuple[bool, str, str | None]:
    license_payload = read_license_sidecar(media_path)

    if license_payload is None:
        return False, "license sidecar is missing", None

    status = license_payload.get("license_status")
    source_provider = license_payload.get("source_provider")
    license_note = license_payload.get("license_note")

    if status != "cleared":
        return False, "license sidecar does not mark license_status=cleared", None

    if not isinstance(source_provider, str) or not source_provider.strip():
        return False, "license sidecar missing source_provider", None

    if not isinstance(license_note, str) or not license_note.strip():
        return False, "license sidecar missing license_note", None

    return True, license_note.strip(), source_provider.strip()


def score_candidate(asset: dict[str, Any], candidate_path: Path) -> int:
    asset_id = require_non_empty_string(asset.get("asset_id"), "asset.asset_id").lower()
    scene_id = require_non_empty_string(asset.get("scene_id"), "asset.scene_id").lower()
    asset_query = require_non_empty_string(asset.get("asset_query"), "asset.asset_query")
    asset_type = require_non_empty_string(asset.get("asset_type"), "asset.asset_type")

    candidate_name = candidate_path.stem.lower()
    candidate_suffix = candidate_path.suffix.lower()

    score = 0

    if asset_id in candidate_name:
        score += 100

    if scene_id in candidate_name:
        score += 80

    if asset_type.lower() in candidate_name:
        score += 25

    query_tokens = slug_tokens(asset_query)
    name_tokens = slug_tokens(candidate_name)
    score += len(query_tokens & name_tokens) * 10

    if asset_type in {"stock_video"} and candidate_suffix in {".mp4", ".mov", ".mkv"}:
        score += 20

    if asset_type in {"stock_image", "chart_or_bill_visual", "screen_style_visual", "simple_motion_text"} and candidate_suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        score += 20

    return score


def choose_candidate(
    asset: dict[str, Any],
    candidate_files: list[Path],
    used_paths: set[str],
) -> Path | None:
    scored: list[tuple[int, Path]] = []

    for candidate_path in candidate_files:
        normalized_path = normalize_path(candidate_path)
        if normalized_path in used_paths:
            continue

        score = score_candidate(asset, candidate_path)
        if score <= 0:
            continue

        scored.append((score, candidate_path))

    if not scored:
        return None

    scored.sort(key=lambda item: (-item[0], normalize_path(item[1])))
    return scored[0][1]


def validate_scenes_payload(scenes_payload: dict[str, Any]) -> list[dict[str, Any]]:
    scene_count = require_positive_int(
        scenes_payload.get("scene_count"),
        "scenes.scene_count",
    )

    scenes = scenes_payload.get("scenes")
    if not isinstance(scenes, list):
        raise AssetResolverError("scenes.scenes must be a list")

    if scene_count != len(scenes):
        raise AssetResolverError(
            f"scene_count mismatch: scene_count={scene_count}, actual={len(scenes)}"
        )

    if scene_count < 1:
        raise AssetResolverError("scenes must not be empty")

    scene_ids: set[str] = set()

    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            raise AssetResolverError(f"scene index {index} must be an object")

        scene_id = require_non_empty_string(scene.get("scene_id"), f"scene[{index}].scene_id")
        require_positive_int(scene.get("order"), f"scene[{index}].order")

        scene_ids.add(scene_id)

        fail_if_forbidden_markers(
            json.dumps(scene, ensure_ascii=False),
            f"scene[{index}]",
        )

    return scenes


def validate_assets_payload(
    assets_payload: dict[str, Any],
    scenes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    asset_count = require_positive_int(
        assets_payload.get("asset_count"),
        "assets.asset_count",
    )

    assets = assets_payload.get("assets")
    if not isinstance(assets, list):
        raise AssetResolverError("assets.assets must be a list")

    if asset_count != len(assets):
        raise AssetResolverError(
            f"asset_count mismatch: asset_count={asset_count}, actual={len(assets)}"
        )

    if asset_count < 1:
        raise AssetResolverError("assets must not be empty")

    scene_ids = {
        require_non_empty_string(scene.get("scene_id"), "scene.scene_id")
        for scene in scenes
    }

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
            raise AssetResolverError(f"asset index {index} must be an object")

        missing = sorted(required_fields - set(asset.keys()))
        if missing:
            raise AssetResolverError(
                f"asset index {index} missing fields: {', '.join(missing)}"
            )

        asset_id = require_non_empty_string(asset.get("asset_id"), f"asset[{index}].asset_id")
        scene_id = require_non_empty_string(asset.get("scene_id"), f"asset[{index}].scene_id")
        require_positive_int(asset.get("order"), f"asset[{index}].order")
        require_non_empty_string(asset.get("asset_type"), f"asset[{index}].asset_type")
        require_non_empty_string(asset.get("asset_query"), f"asset[{index}].asset_query")
        require_non_empty_string(asset.get("visual_intent"), f"asset[{index}].visual_intent")
        require_non_empty_string(asset.get("usage_role"), f"asset[{index}].usage_role")
        require_positive_int(
            asset.get("estimated_duration_sec"),
            f"asset[{index}].estimated_duration_sec",
        )

        if not isinstance(asset.get("required"), bool):
            raise AssetResolverError(f"asset[{index}].required must be boolean")

        if scene_id not in scene_ids:
            raise AssetResolverError(
                f"asset {asset_id} references unknown scene_id={scene_id}"
            )

        fail_if_forbidden_markers(
            json.dumps(asset, ensure_ascii=False),
            f"asset[{index}]",
        )

    return assets


def build_blocked_asset(asset: dict[str, Any], blocker_reason: str, local_path: str | None = None) -> dict[str, Any]:
    return {
        "asset_id": require_non_empty_string(asset.get("asset_id"), "asset.asset_id"),
        "scene_id": require_non_empty_string(asset.get("scene_id"), "asset.scene_id"),
        "order": require_positive_int(asset.get("order"), "asset.order"),
        "asset_type": require_non_empty_string(asset.get("asset_type"), "asset.asset_type"),
        "asset_query": require_non_empty_string(asset.get("asset_query"), "asset.asset_query"),
        "visual_intent": require_non_empty_string(asset.get("visual_intent"), "asset.visual_intent"),
        "usage_role": require_non_empty_string(asset.get("usage_role"), "asset.usage_role"),
        "required": bool(asset.get("required")),
        "provider_status": "blocked",
        "source_provider": None,
        "source_url": None,
        "local_path": local_path,
        "license_status": "blocked",
        "license_note": "license not cleared",
        "resolution_status": "blocked",
        "blocker_reason": blocker_reason,
        "production_notes": "Asset blocked honestly. No media file was created by resolver.",
    }


def build_resolved_asset(
    asset: dict[str, Any],
    media_path: Path,
    source_provider: str,
    license_note: str,
) -> dict[str, Any]:
    local_path = normalize_path(media_path)

    return {
        "asset_id": require_non_empty_string(asset.get("asset_id"), "asset.asset_id"),
        "scene_id": require_non_empty_string(asset.get("scene_id"), "asset.scene_id"),
        "order": require_positive_int(asset.get("order"), "asset.order"),
        "asset_type": require_non_empty_string(asset.get("asset_type"), "asset.asset_type"),
        "asset_query": require_non_empty_string(asset.get("asset_query"), "asset.asset_query"),
        "visual_intent": require_non_empty_string(asset.get("visual_intent"), "asset.visual_intent"),
        "usage_role": require_non_empty_string(asset.get("usage_role"), "asset.usage_role"),
        "required": bool(asset.get("required")),
        "provider_status": "resolved",
        "source_provider": source_provider,
        "source_url": None,
        "local_path": local_path,
        "license_status": "cleared",
        "license_note": license_note,
        "resolution_status": "ready",
        "blocker_reason": None,
        "production_notes": "Asset resolved from approved local source with license evidence.",
    }


def validate_resolved_asset(resolved_asset: dict[str, Any], index: int) -> None:
    required_fields = {
        "asset_id",
        "scene_id",
        "order",
        "asset_type",
        "asset_query",
        "visual_intent",
        "usage_role",
        "required",
        "provider_status",
        "source_provider",
        "source_url",
        "local_path",
        "license_status",
        "license_note",
        "resolution_status",
        "blocker_reason",
        "production_notes",
    }

    missing = sorted(required_fields - set(resolved_asset.keys()))
    if missing:
        raise AssetResolverError(
            f"resolved asset index {index} missing fields: {', '.join(missing)}"
        )

    provider_status = resolved_asset["provider_status"]
    license_status = resolved_asset["license_status"]
    resolution_status = resolved_asset["resolution_status"]

    if provider_status not in {"resolved", "blocked"}:
        raise AssetResolverError(f"resolved asset index {index} has invalid provider_status")

    if license_status not in {"cleared", "blocked"}:
        raise AssetResolverError(f"resolved asset index {index} has invalid license_status")

    if resolution_status not in {"ready", "blocked"}:
        raise AssetResolverError(f"resolved asset index {index} has invalid resolution_status")

    if provider_status == "resolved":
        local_path = require_non_empty_string(
            resolved_asset.get("local_path"),
            f"resolved_asset[{index}].local_path",
        )
        if not (REPO_ROOT / local_path).exists():
            raise AssetResolverError(
                f"resolved asset index {index} local_path does not exist: {local_path}"
            )

        require_non_empty_string(
            resolved_asset.get("source_provider"),
            f"resolved_asset[{index}].source_provider",
        )

        if license_status != "cleared":
            raise AssetResolverError(f"resolved asset index {index} must have license_status=cleared")

        if resolution_status != "ready":
            raise AssetResolverError(f"resolved asset index {index} must have resolution_status=ready")

    if provider_status == "blocked":
        if license_status != "blocked":
            raise AssetResolverError(f"blocked asset index {index} must have license_status=blocked")

        if resolution_status != "blocked":
            raise AssetResolverError(f"blocked asset index {index} must have resolution_status=blocked")

        require_non_empty_string(
            resolved_asset.get("blocker_reason"),
            f"resolved_asset[{index}].blocker_reason",
        )

    fail_if_forbidden_markers(
        json.dumps(resolved_asset, ensure_ascii=False),
        f"resolved_asset[{index}]",
    )


def resolve_assets(
    assets: list[dict[str, Any]],
    candidate_files: list[Path],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    resolved_assets: list[dict[str, Any]] = []
    blockers: list[str] = []
    warnings: list[str] = []
    used_paths: set[str] = set()

    if not candidate_files:
        warnings.append("no approved local media files found")

    for asset in assets:
        candidate_path = choose_candidate(asset, candidate_files, used_paths)

        if candidate_path is None:
            blocker_reason = "no matching approved local media file found"
            resolved_asset = build_blocked_asset(asset, blocker_reason)
            blockers.append(f"{resolved_asset['asset_id']}: {blocker_reason}")
            resolved_assets.append(resolved_asset)
            continue

        local_path = normalize_path(candidate_path)
        license_cleared, license_note, source_provider = license_is_cleared(candidate_path)

        if not license_cleared or source_provider is None:
            blocker_reason = license_note
            resolved_asset = build_blocked_asset(asset, blocker_reason, local_path=local_path)
            blockers.append(f"{resolved_asset['asset_id']}: {blocker_reason}")
            resolved_assets.append(resolved_asset)
            continue

        resolved_asset = build_resolved_asset(
            asset,
            candidate_path,
            source_provider,
            license_note,
        )
        used_paths.add(local_path)
        resolved_assets.append(resolved_asset)

    for index, resolved_asset in enumerate(resolved_assets, start=1):
        validate_resolved_asset(resolved_asset, index)

    return resolved_assets, blockers, warnings


def run_asset_resolver(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "QA":
        raise AssetResolverError("Asset Resolver may run only when phase is QA")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]
    artifacts = state.get("artifacts", {})

    if not isinstance(artifacts, dict):
        raise AssetResolverError("artifacts must be an object")

    stock_policy = require_non_empty_string(manifest.get("stock_policy"), "manifest.stock_policy")
    primary_platform = require_non_empty_string(manifest.get("primary_platform"), "manifest.primary_platform")
    content_language = require_non_empty_string(manifest.get("content_language"), "manifest.content_language")
    topic = require_non_empty_string(manifest.get("topic"), "manifest.topic")
    working_title = require_non_empty_string(manifest.get("working_title"), "manifest.working_title")

    if stock_policy != "stock_first_no_repeat":
        raise AssetResolverError("Asset Resolver v1 supports only stock_first_no_repeat policy")

    assets_path = Path(
        require_non_empty_string(artifacts.get("assets_path"), "artifacts.assets_path")
    )
    scenes_path = Path(
        require_non_empty_string(artifacts.get("scenes_path"), "artifacts.scenes_path")
    )

    assets_payload = read_json_file(assets_path)
    scenes_payload = read_json_file(scenes_path)

    fail_if_forbidden_markers(json.dumps(assets_payload, ensure_ascii=False), "assets")
    fail_if_forbidden_markers(json.dumps(scenes_payload, ensure_ascii=False), "scenes")

    scenes = validate_scenes_payload(scenes_payload)
    assets = validate_assets_payload(assets_payload, scenes)

    search_dirs = approved_search_dirs(project_id)
    candidate_files = list_candidate_media_files(search_dirs)

    resolved_assets, blockers, warnings = resolve_assets(assets, candidate_files)

    resolved_count = sum(1 for asset in resolved_assets if asset["provider_status"] == "resolved")
    blocked_count = sum(1 for asset in resolved_assets if asset["provider_status"] == "blocked")
    license_cleared_count = sum(1 for asset in resolved_assets if asset["license_status"] == "cleared")

    if resolved_count + blocked_count != len(resolved_assets):
        raise AssetResolverError("resolved/blocked count mismatch")

    now = utc_now_iso()
    resolved_assets_path = state_path.parent / "assets" / "resolved_assets.json"

    payload = {
        "project_id": project_id,
        "resolver": RESOLVER_NAME,
        "resolver_version": RESOLVER_VERSION,
        "source_assets_path": str(assets_path),
        "source_scenes_path": str(scenes_path),
        "topic": topic,
        "working_title": working_title,
        "primary_platform": primary_platform,
        "content_language": content_language,
        "stock_policy": stock_policy,
        "asset_count": len(resolved_assets),
        "resolved_count": resolved_count,
        "blocked_count": blocked_count,
        "license_cleared_count": license_cleared_count,
        "provider_mode": PROVIDER_MODE,
        "approved_search_dirs": [normalize_path(path) for path in search_dirs],
        "assets": resolved_assets,
        "blockers": blockers,
        "warnings": warnings,
        "created_at": now,
    }

    fail_if_forbidden_markers(json.dumps(payload, ensure_ascii=False), "resolved_assets")

    write_json_atomic(resolved_assets_path, payload)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["resolved_assets_path"] = str(resolved_assets_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "ASSET_RESOLVER_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "resolved_assets_path": str(resolved_assets_path),
        "provider_mode": PROVIDER_MODE,
        "asset_count": len(resolved_assets),
        "resolved_count": resolved_count,
        "blocked_count": blocked_count,
        "license_cleared_count": license_cleared_count,
        "blockers": blockers,
        "warnings": warnings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind Asset Resolver v1")
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
        result = run_asset_resolver(Path(args.state))
    except (AssetResolverError, StateValidationError, OSError) as exc:
        print(f"[ASSET_RESOLVER][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
