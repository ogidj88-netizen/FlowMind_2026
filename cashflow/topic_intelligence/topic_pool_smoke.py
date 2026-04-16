from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cashflow.topic_intelligence.analyzer import TopicAnalyzer
from cashflow.topic_intelligence.collector import TopicSeedCollector
from cashflow.topic_intelligence.profile_runtime_adapter import build_collector_runtime_config
from cashflow.topic_intelligence.topic_pool_builder import TopicPoolBuilder


def _to_json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _to_json_safe(item) for key, item in value.items()}

    if isinstance(value, list):
        return [_to_json_safe(item) for item in value]

    if isinstance(value, tuple):
        return [_to_json_safe(item) for item in value]

    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    return str(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=str, required=True, help="Path to niche profile JSON")
    parser.add_argument("--limit", type=int, default=20, help="Posts per subreddit")
    parser.add_argument("--max-topics", type=int, default=5, help="Maximum topics in topic pool")
    args = parser.parse_args()

    profile_path = Path(args.profile)
    runtime_config = build_collector_runtime_config(profile_path)

    collector = TopicSeedCollector(
        entity_registry=runtime_config["entity_registry"],
        trigger_words=runtime_config["trigger_words"],
        financial_keywords=runtime_config["financial_keywords"],
        default_subreddits=runtime_config["reddit_subreddits"],
    )

    analyzer = TopicAnalyzer()
    pool_builder = TopicPoolBuilder()

    candidates = collector.collect_from_reddit(limit_per_subreddit=args.limit)
    analyzed_topics = [analyzer.analyze_candidate(candidate) for candidate in candidates]
    pool = pool_builder.build(analyzed_topics, max_topics=args.max_topics)

    print("TOPIC POOL SMOKE OK")
    print(
        json.dumps(
            {
                "profile_id": runtime_config["profile_id"],
                "candidate_count": len(candidates),
                "analyzed_count": len(analyzed_topics),
                "pool_size": pool["pool_size"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    print("TOPIC POOL PREVIEW")
    print(json.dumps(_to_json_safe(pool), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
