from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProfileLoaderError(ValueError):
    """Raised when a niche profile cannot be loaded or is invalid."""


REQUIRED_TOP_LEVEL_KEYS: tuple[str, ...] = (
    "profile_id",
    "profile_version",
    "derived_from_niche_id",
    "profile_mode",
    "source_map",
    "candidate_anchors",
    "trigger_lexicon",
    "exclusion_rules",
    "validation_rules",
    "scoring_weights",
    "formatting_rules",
    "cooldown_rules",
    "health_rules",
    "production_profile",
    "metadata",
)


def load_frozen_profile(profile_path: str | Path) -> dict[str, Any]:
    path = Path(profile_path)

    if not path.exists():
        raise ProfileLoaderError(f"Frozen profile file does not exist: {path}")

    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProfileLoaderError(f"Frozen profile is not valid JSON: {path}") from exc

    if not isinstance(raw_data, dict):
        raise ProfileLoaderError("Frozen profile root must be a JSON object")

    missing_keys = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in raw_data]
    if missing_keys:
        joined = ", ".join(missing_keys)
        raise ProfileLoaderError(f"Frozen profile is missing required keys: {joined}")

    profile_mode = raw_data.get("profile_mode")
    if profile_mode not in {"entity_driven", "pattern_driven", "mixed"}:
        raise ProfileLoaderError(
            "Frozen profile has invalid profile_mode. "
            "Expected one of: entity_driven, pattern_driven, mixed."
        )

    source_map = raw_data.get("source_map")
    if not isinstance(source_map, list) or not source_map:
        raise ProfileLoaderError("Frozen profile source_map must be a non-empty list")

    candidate_anchors = raw_data.get("candidate_anchors")
    if not isinstance(candidate_anchors, dict):
        raise ProfileLoaderError("Frozen profile candidate_anchors must be an object")

    trigger_lexicon = raw_data.get("trigger_lexicon")
    if not isinstance(trigger_lexicon, dict):
        raise ProfileLoaderError("Frozen profile trigger_lexicon must be an object")

    return raw_data


if __name__ == "__main__":
    example_path = Path("cashflow/topic_intelligence/profiles/finance_legacy_v1.json")

    try:
        profile = load_frozen_profile(example_path)
    except ProfileLoaderError as exc:
        print(f"PROFILE LOAD ERROR: {exc}")
        raise SystemExit(1) from exc

    print("PROFILE LOAD OK")
    print(
        json.dumps(
            {
                "profile_id": profile["profile_id"],
                "profile_version": profile["profile_version"],
                "profile_mode": profile["profile_mode"],
                "source_count": len(profile["source_map"]),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
