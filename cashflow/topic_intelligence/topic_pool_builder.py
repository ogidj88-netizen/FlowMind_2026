from __future__ import annotations

from typing import Any

from cashflow.topic_intelligence.models import ValidatedTopic


class TopicPoolBuilder:
    """
    Topic Pool (Пул тем) builder.

    Converts analyzed topics into a small ranked pool for downstream production.
    This is a lightweight contract layer, not a queue system.
    """

    def build(self, topics: list[ValidatedTopic], max_topics: int = 5) -> dict[str, Any]:
        backlog_topics = [topic for topic in topics if str(topic.verdict) in {"BACKLOG", "Verdict.BACKLOG"}]
        ranked_topics = sorted(backlog_topics, key=self._score_topic, reverse=True)
        selected_topics = ranked_topics[:max_topics]

        return {
            "pool_size": len(selected_topics),
            "topics": [self._to_topic_entry(topic, rank=index + 1) for index, topic in enumerate(selected_topics)],
        }

    def _score_topic(self, topic: ValidatedTopic) -> int:
        score = 0

        seed = topic.seed.lower().strip()
        anchor = topic.anchor_demand.lower().strip()
        utility = topic.utility.lower().strip()
        source_label = str(topic.source_label).lower().strip()

        if any(word in seed for word in ("cancel", "renew", "charged", "fee", "collections", "late fee", "apr")):
            score += 3

        if any(word in anchor for word in ("cancel", "renew", "charge", "fee", "collections", "apr")):
            score += 2

        if len(seed) >= 18:
            score += 1

        if "lose money" in utility or "debt" in utility or "recurring charges" in utility:
            score += 2

        if source_label in {"youshouldknow", "cordcutters", "frugal", "povertyfinance", "creditcards"}:
            score += 1

        return score

    def _to_topic_entry(self, topic: ValidatedTopic, rank: int) -> dict[str, Any]:
        return {
            "rank": rank,
            "topic_id": self._build_topic_id(topic),
            "entity": topic.entity,
            "seed": topic.seed,
            "anchor_demand": topic.anchor_demand,
            "utility": topic.utility,
            "pain_evidence": topic.pain_evidence,
            "source_link": str(topic.source_link) if topic.source_link else None,
            "source_type": topic.source_type,
            "source_label": topic.source_label,
            "verdict": str(topic.verdict),
            "production_status": "READY",
        }

    def _build_topic_id(self, topic: ValidatedTopic) -> str:
        base = f"{topic.entity}_{topic.anchor_demand}"
        normalized = base.lower().replace(" ", "_").replace("/", "_")
        while "__" in normalized:
            normalized = normalized.replace("__", "_")
        return normalized.strip("_")
