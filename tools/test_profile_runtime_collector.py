from __future__ import annotations

from cashflow.topic_intelligence.collector import TopicSeedCollector
from cashflow.topic_intelligence.profile_runtime_adapter import build_collector_runtime_config


def main() -> None:
    runtime_config = build_collector_runtime_config(
        "cashflow/topic_intelligence/profiles/finance_legacy_v1.json"
    )

    collector = TopicSeedCollector(
        entity_registry=runtime_config["entity_registry"],
        trigger_words=runtime_config["trigger_words"],
        default_subreddits=runtime_config["reddit_subreddits"],
    )

    print("PROFILE RUNTIME COLLECTOR OK")
    print(
        {
            "profile_id": runtime_config["profile_id"],
            "profile_mode": runtime_config["profile_mode"],
            "entity_count": len(collector.entity_registry),
            "trigger_count": len(collector.trigger_words),
            "default_subreddit_count": len(collector.default_subreddits),
        }
    )


if __name__ == "__main__":
    main()
