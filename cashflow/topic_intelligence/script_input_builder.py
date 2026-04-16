from __future__ import annotations

from typing import Dict

from cashflow.topic_intelligence.models import ValidatedTopic


class ScriptInputBuilder:
    """
    Transforms a validated topic into a production-ready script input payload.
    This is a STRICT contract between Topic Intelligence and Script Generator.
    """

    def build(self, topic: ValidatedTopic) -> Dict:
        if topic.verdict != "BACKLOG":
            raise ValueError("Only BACKLOG topics can be used for script generation")

        return {
            "topic_id": self._build_topic_id(topic),
            "core": {
                "entity": topic.entity,
                "seed": topic.seed,
                "anchor_demand": topic.anchor_demand,
            },
            "angle": self._build_angle(topic),
            "hook": self._build_hook(topic),
            "constraints": {
                "max_duration_sec": 540,  # 9 minutes
                "target_style": "conversational_american",
                "avoid": [
                    "generic motivation",
                    "vague advice",
                    "no numbers",
                ],
            },
            "metadata": {
                "source_link": topic.source_link,
                "source_type": topic.source_type,
                "source_label": topic.source_label,
            },
        }

    def _build_topic_id(self, topic: ValidatedTopic) -> str:
        base = f"{topic.entity}_{topic.anchor_demand}"
        return base.lower().replace(" ", "_")

    def _build_angle(self, topic: ValidatedTopic) -> str:
        """
        Converts seed into a human-understandable video angle.
        """
        seed = topic.seed.lower()

        if "cancel" in seed:
            return "companies make cancellation intentionally difficult to keep charging you"

        if "apr" in seed or "interest" in seed:
            return "small interest changes quietly trap users into long-term debt"

        if "fee" in seed or "charge" in seed:
            return "users are charged in ways they do not fully notice or understand"

        if "renew" in seed:
            return "auto-renew systems exploit user inattention"

        return "a hidden financial mechanism causes users to lose money without noticing"

    def _build_hook(self, topic: ValidatedTopic) -> str:
        """
        Generates a strong opening hook for the video.
        """
        entity = topic.entity.lower()
        demand = topic.anchor_demand.lower()

        return (
            f"Most people don't realize this, but {entity} can quietly cost you more money than you think — "
            f"especially when it comes to {demand}."
        )
