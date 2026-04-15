from __future__ import annotations

from pathlib import Path
from typing import Any

from cashflow.topic_intelligence.collector import EntityRule
from cashflow.topic_intelligence.profile_loader import load_frozen_profile


class ProfileRuntimeAdapterError(ValueError):
    """Raised when a frozen profile cannot be adapted for runtime use."""


def build_collector_runtime_config(profile_path: str | Path) -> dict[str, Any]:
    profile = load_frozen_profile(profile_path)

    candidate_anchors = profile["candidate_anchors"]
    entities_raw = candidate_anchors["entities"]
    seed_keywords_raw = candidate_anchors.get("seed_keywords", [])
    trigger_lexicon = profile["trigger_lexicon"]
    source_map = profile["source_map"]

    entity_registry: list[EntityRule] = []
    for item in entities_raw:
        name = item["name"].strip()
        aliases = [alias.strip() for alias in item["aliases"] if alias.strip()]

        if not name:
            raise ProfileRuntimeAdapterError("Entity name cannot be empty")

        if not aliases:
            raise ProfileRuntimeAdapterError(f"Entity '{name}' must have at least one alias")

        entity_registry.append(EntityRule(entity=name, aliases=aliases))

    trigger_words: list[str] = []
    for group_name in ("pain", "urgency", "complaint", "change", "friction", "risk"):
        group_values = trigger_lexicon.get(group_name, [])
        for value in group_values:
            cleaned = value.strip()
            if cleaned:
                trigger_words.append(cleaned)

    trigger_words = sorted(set(trigger_words), key=str.lower)

    financial_keywords: list[str] = []
    for value in seed_keywords_raw:
        cleaned = str(value).strip()
        if cleaned:
            financial_keywords.append(cleaned)

    financial_keywords = sorted(set(financial_keywords), key=str.lower)

    reddit_subreddits: list[str] = []
    for source in source_map:
        if not source.get("enabled", False):
            continue
        if source.get("source_type") != "reddit":
            continue

        identifier = str(source.get("source_identifier", "")).strip()
        if identifier:
            reddit_subreddits.append(identifier)

    reddit_subreddits = sorted(set(reddit_subreddits), key=str.lower)

    return {
        "profile_id": profile["profile_id"],
        "profile_mode": profile["profile_mode"],
        "entity_registry": entity_registry,
        "trigger_words": trigger_words,
        "financial_keywords": financial_keywords,
        "reddit_subreddits": reddit_subreddits,
        "source_map": source_map,
        "validation_rules": profile["validation_rules"],
        "scoring_weights": profile["scoring_weights"],
        "production_profile": profile["production_profile"],
    }


if __name__ == "__main__":
    example_path = Path("cashflow/topic_intelligence/profiles/finance_legacy_v1.json")

    try:
        runtime_config = build_collector_runtime_config(example_path)
    except (ProfileRuntimeAdapterError, ValueError) as exc:
        print(f"RUNTIME ADAPTER ERROR: {exc}")
        raise SystemExit(1) from exc

    print("RUNTIME ADAPTER OK")
    print(
        {
            "profile_id": runtime_config["profile_id"],
            "profile_mode": runtime_config["profile_mode"],
            "entity_count": len(runtime_config["entity_registry"]),
            "trigger_count": len(runtime_config["trigger_words"]),
            "financial_keyword_count": len(runtime_config["financial_keywords"]),
            "reddit_subreddit_count": len(runtime_config["reddit_subreddits"]),
        }
    )
