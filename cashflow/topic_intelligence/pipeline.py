from __future__ import annotations

import argparse
import json
from pathlib import Path

from cashflow.topic_intelligence.analyzer import TopicAnalyzer
from cashflow.topic_intelligence.collector import TopicSeedCollector
from cashflow.topic_intelligence.profile_runtime_adapter import build_collector_runtime_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=str, required=True, help="Path to niche profile JSON")
    parser.add_argument("--limit", type=int, default=3, help="Posts per subreddit")
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

    reddit_posts = collector.fetch_reddit_posts(
        subreddits=runtime_config["reddit_subreddits"],
        limit_per_subreddit=args.limit,
    )

    debug = {
        "posts_total": 0,
        "passed_context_gate": 0,
        "matched_entity": 0,
        "matched_triggers": 0,
        "passed_trigger_quality_gate": 0,
        "passed_relevance_score": 0,
        "final_candidates": 0,
    }

    first_trigger_gate_block = None
    candidates = []

    for post in reddit_posts:
        if not post.combined_text:
            continue

        debug["posts_total"] += 1
        normalized_text = collector._normalize_text(post.combined_text)

        if not collector._passes_context_gate(normalized_text):
            continue
        debug["passed_context_gate"] += 1

        entity_match = collector._match_entity(normalized_text)
        if entity_match is None:
            continue
        debug["matched_entity"] += 1

        matched_triggers = collector._match_triggers(normalized_text)
        if not matched_triggers:
            continue
        debug["matched_triggers"] += 1

        passed_trigger_gate = collector._passes_trigger_quality_gate(
            text=normalized_text,
            entity_match=entity_match,
            matched_triggers=matched_triggers,
        )
        if not passed_trigger_gate:
            if first_trigger_gate_block is None:
                first_trigger_gate_block = {
                    "subreddit": post.subreddit,
                    "source_link": post.permalink,
                    "entity": entity_match.entity,
                    "matched_alias": entity_match.matched_alias,
                    "matched_triggers": matched_triggers,
                    "text_preview": normalized_text[:500],
                }
            continue

        debug["passed_trigger_quality_gate"] += 1

        relevance_score = collector._calculate_relevance_score(
            text=normalized_text,
            entity_match=entity_match,
            matched_triggers=matched_triggers,
        )
        if relevance_score < 5:
            continue
        debug["passed_relevance_score"] += 1

        seed_value = collector._build_seed(entity_match.entity, matched_triggers)
        if not seed_value:
            continue

        candidate_batch = collector.collect_from_texts(
            texts=[post.combined_text],
            source_link=post.permalink,
            source_type="reddit",
            source_label=post.subreddit,
        )
        candidates.extend(candidate_batch)

    candidates = collector._deduplicate(candidates)
    debug["final_candidates"] = len(candidates)

    analyzed_topics = [analyzer.analyze_candidate(candidate) for candidate in candidates[:10]]

    print("RUNTIME ANALYZER SMOKE OK")
    print(
        json.dumps(
            {
                "profile_id": runtime_config["profile_id"],
                "candidate_count": len(candidates),
                "analyzed_count": len(analyzed_topics),
                "debug": debug,
                "first_trigger_gate_block": first_trigger_gate_block,
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
