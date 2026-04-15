from __future__ import annotations

import json
from pathlib import Path

from cashflow.topic_intelligence.collector import TopicSeedCollector
from cashflow.topic_intelligence.profile_runtime_adapter import build_collector_runtime_config


def main() -> None:
    profile_path = Path("cashflow/topic_intelligence/profiles/finance_legacy_v1.json")
    runtime_config = build_collector_runtime_config(profile_path)

    collector = TopicSeedCollector(
        entity_registry=runtime_config["entity_registry"],
        trigger_words=runtime_config["trigger_words"],
        default_subreddits=runtime_config["reddit_subreddits"],
    )

    candidates = collector.collect_from_reddit(limit_per_subreddit=3)

    print("PROFILE SEED SMOKE OK")
    print(
        json.dumps(
            {
                "profile_id": runtime_config["profile_id"],
                "profile_mode": runtime_config["profile_mode"],
                "reddit_subreddits": runtime_config["reddit_subreddits"],
                "candidate_count": len(candidates),
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    preview = []
    for candidate in candidates[:5]:
        preview.append(
            {
                "entity": candidate.entity,
                "seed": candidate.seed,
                "matched_alias": candidate.matched_alias,
                "trigger_words": candidate.trigger_words,
                "source_link": str(candidate.source_link) if candidate.source_link else None,
                "source_type": candidate.source_type,
                "source_label": candidate.source_label,
            }
        )

    print("CANDIDATE PREVIEW")
    print(json.dumps(preview, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
