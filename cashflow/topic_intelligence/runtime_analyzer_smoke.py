from __future__ import annotations

import json
from pathlib import Path

from cashflow.topic_intelligence.analyzer import TopicAnalyzer
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
    analyzer = TopicAnalyzer()

    candidates = collector.collect_from_reddit(limit_per_subreddit=3)
    analyzed_topics = [analyzer.analyze_candidate(candidate) for candidate in candidates[:5]]

    print("RUNTIME ANALYZER SMOKE OK")
    print(
        json.dumps(
            {
                "profile_id": runtime_config["profile_id"],
                "candidate_count": len(candidates),
                "analyzed_count": len(analyzed_topics),
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    preview = []
    for topic in analyzed_topics:
        preview.append(
            {
                "entity": topic.entity,
                "seed": topic.seed,
                "anchor_demand": topic.anchor_demand,
                "source_link": str(topic.source_link) if topic.source_link else None,
                "source_type": topic.source_type,
                "source_label": topic.source_label,
                "verdict": topic.verdict.value,
            }
        )

    print("ANALYZED TOPIC PREVIEW")
    print(json.dumps(preview, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
