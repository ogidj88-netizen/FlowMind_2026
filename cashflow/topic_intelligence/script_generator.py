from __future__ import annotations

from typing import Any


class ScriptGenerator:
    """
    Script Generator v1 (Генератор сценарію v1).

    Deterministic first-pass script package builder.
    Takes a validated script input payload and converts it into
    a production-ready script draft contract for downstream modules.
    """

    def build(self, script_input: dict[str, Any]) -> dict[str, Any]:
        core = script_input["core"]
        entity = str(core["entity"]).strip()
        seed = str(core["seed"]).strip()
        anchor_demand = str(core["anchor_demand"]).strip()

        angle = str(script_input["angle"]).strip()
        hook = str(script_input["hook"]).strip()
        constraints = dict(script_input["constraints"])
        metadata = dict(script_input["metadata"])
        topic_id = str(script_input["topic_id"]).strip()

        title = self._build_title(entity=entity, seed=seed, anchor_demand=anchor_demand)
        promise = self._build_promise(entity=entity, angle=angle)
        intro = self._build_intro(hook=hook, promise=promise)
        body_blocks = self._build_body_blocks(entity=entity, seed=seed, angle=angle, anchor_demand=anchor_demand)
        outro = self._build_outro(entity=entity)

        return {
            "script_id": topic_id,
            "topic_id": topic_id,
            "title": title,
            "hook": hook,
            "promise": promise,
            "angle": angle,
            "format": {
                "language": "en",
                "style": constraints.get("target_style", "conversational_american"),
                "max_duration_sec": constraints.get("max_duration_sec", 540),
            },
            "structure": {
                "intro": intro,
                "body": body_blocks,
                "outro": outro,
            },
            "source_context": {
                "entity": entity,
                "seed": seed,
                "anchor_demand": anchor_demand,
                "source_link": metadata.get("source_link"),
                "source_type": metadata.get("source_type"),
                "source_label": metadata.get("source_label"),
            },
            "generation_status": "DRAFT_READY",
        }

    def _build_title(self, entity: str, seed: str, anchor_demand: str) -> str:
        seed_lower = seed.lower()

        if "cancel" in seed_lower:
            return f"Why {entity} Keep Charging You Even When You Want Out"

        if "renew" in seed_lower:
            return f"How {entity} Quietly Turn Into Automatic Money Leaks"

        if "fee" in seed_lower or "charge" in seed_lower:
            return f"The Hidden Cost Behind {entity} Most People Miss"

        if "apr" in seed_lower or "interest" in seed_lower:
            return f"How {entity} Trap You With Small Changes That Snowball"

        return f"The Real Cost Behind {anchor_demand.title()}"

    def _build_promise(self, entity: str, angle: str) -> str:
        return (
            f"This video explains how {entity.lower()} create a hidden money-loss mechanism, "
            f"why people miss it, and what makes the trap work."
        )

    def _build_intro(self, hook: str, promise: str) -> list[str]:
        return [
            hook,
            promise,
            "By the end, the viewer should clearly understand the mechanism, the emotional trap, and the hidden cost.",
        ]

    def _build_body_blocks(
        self,
        entity: str,
        seed: str,
        angle: str,
        anchor_demand: str,
    ) -> list[dict[str, Any]]:
        return [
            {
                "section_id": "problem_setup",
                "goal": "Define the hidden money problem in simple terms.",
                "talking_points": [
                    f"Explain what the viewer thinks is happening with {entity.lower()}.",
                    f"Contrast that with the real mechanism behind '{seed}'.",
                    f"Frame the issue around demand language: '{anchor_demand}'.",
                ],
            },
            {
                "section_id": "mechanism_breakdown",
                "goal": "Show how the trap actually works.",
                "talking_points": [
                    angle,
                    f"Describe the step-by-step flow that turns {entity.lower()} into an ongoing money drain.",
                    "Show why the average user notices the cost too late.",
                ],
            },
            {
                "section_id": "consequence_layer",
                "goal": "Make the cost feel real and concrete.",
                "talking_points": [
                    "Describe how small repeated losses become meaningful over time.",
                    "Show the psychological reason people delay action.",
                    "Connect the hidden cost to real monthly pressure, stress, or loss of control.",
                ],
            },
            {
                "section_id": "viewer_takeaway",
                "goal": "End with clarity, not generic advice.",
                "talking_points": [
                    f"Restate the real risk behind {entity.lower()}.",
                    "Give the viewer a simple way to recognize the trap earlier next time.",
                    "Close with a sharp summary that reinforces the lesson.",
                ],
            },
        ]

    def _build_outro(self, entity: str) -> list[str]:
        return [
            f"The danger is not just {entity.lower()} itself — it is how easy it is to normalize the loss.",
            "Once you see the pattern clearly, the hidden cost stops feeling invisible.",
            "End on a short, memorable line that reinforces control, awareness, and consequence.",
        ]
