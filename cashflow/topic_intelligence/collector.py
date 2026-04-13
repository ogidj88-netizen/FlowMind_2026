from __future__ import annotations

from typing import Iterable

from pydantic import BaseModel, Field

from cashflow.topic_intelligence.models import SeedSource


class EntityRule(BaseModel):
    entity: str = Field(..., min_length=1, max_length=120)
    aliases: list[str] = Field(default_factory=list, min_length=1)


class SeedCandidate(BaseModel):
    entity: str = Field(..., min_length=1, max_length=120)
    seed_source: SeedSource
    seed: str = Field(..., min_length=1, max_length=300)
    matched_alias: str = Field(..., min_length=1, max_length=120)
    trigger_words: list[str] = Field(default_factory=list)
    raw_text: str = Field(..., min_length=1, max_length=2000)


ENTITY_REGISTRY: list[EntityRule] = [
    EntityRule(
        entity="Bank of America",
        aliases=["bank of america", "boa", "bofa"],
    ),
    EntityRule(
        entity="Chase",
        aliases=["chase", "chase bank", "jp morgan chase", "jpmorgan chase"],
    ),
    EntityRule(
        entity="Wells Fargo",
        aliases=["wells fargo", "wells"],
    ),
    EntityRule(
        entity="Credit Card Debt",
        aliases=["credit card", "credit cards", "card debt", "credit card debt", "apr"],
    ),
    EntityRule(
        entity="Student Loans",
        aliases=["student loan", "student loans", "loan payment", "federal loans"],
    ),
    EntityRule(
        entity="Taxes USA",
        aliases=["irs", "tax refund", "taxes", "tax bill", "tax return"],
    ),
    EntityRule(
        entity="Rent",
        aliases=["rent", "rent increase", "landlord", "lease"],
    ),
    EntityRule(
        entity="Healthcare Costs",
        aliases=["healthcare", "medical bill", "hospital bill", "insurance denial"],
    ),
    EntityRule(
        entity="Insurance",
        aliases=["insurance", "premium", "claim denied", "coverage"],
    ),
    EntityRule(
        entity="Subscriptions",
        aliases=["subscription", "subscriptions", "auto renew", "auto-renew", "renewal"],
    ),
    EntityRule(
        entity="Gas Prices",
        aliases=["gas prices", "gas", "fuel", "gas station"],
    ),
    EntityRule(
        entity="Groceries",
        aliases=["groceries", "grocery bill", "food prices", "supermarket"],
    ),
    EntityRule(
        entity="Inflation",
        aliases=["inflation", "price increase", "prices rising", "cost of living"],
    ),
]

TRIGGER_WORDS: tuple[str, ...] = (
    "fee",
    "fees",
    "charged",
    "charge",
    "overdraft",
    "late fee",
    "interest",
    "apr",
    "denied",
    "blocked",
    "hold",
    "frozen",
    "limit",
    "reduced",
    "cut",
    "raised",
    "increase",
    "increased",
    "higher",
    "spike",
    "missed",
    "delay",
    "delayed",
    "penalty",
    "renewal",
    "auto renew",
    "auto-renew",
    "cancel",
    "canceled",
    "claim denied",
    "out of pocket",
    "medical debt",
    "rent hike",
)


class TopicSeedCollector:
    def __init__(
        self,
        entity_registry: list[EntityRule] | None = None,
        trigger_words: Iterable[str] | None = None,
    ) -> None:
        self.entity_registry = entity_registry or ENTITY_REGISTRY
        self.trigger_words = tuple(trigger_words or TRIGGER_WORDS)

    def collect_from_texts(
        self,
        texts: list[str],
        seed_source: SeedSource = SeedSource.SOCIAL_SIGNAL,
    ) -> list[SeedCandidate]:
        candidates: list[SeedCandidate] = []

        for text in texts:
            normalized_text = self._normalize_text(text)
            if not normalized_text:
                continue

            entity_match = self._match_entity(normalized_text)
            if entity_match is None:
                continue

            matched_triggers = self._match_triggers(normalized_text)
            if not matched_triggers:
                continue

            candidate = SeedCandidate(
                entity=entity_match.entity,
                seed_source=seed_source,
                seed=self._build_seed(entity_match.entity, matched_triggers),
                matched_alias=entity_match.matched_alias,
                trigger_words=matched_triggers,
                raw_text=text.strip(),
            )
            candidates.append(candidate)

        return self._deduplicate(candidates)

    def _match_entity(self, text: str) -> "EntityMatch | None":
        for rule in self.entity_registry:
            for alias in rule.aliases:
                if alias.lower() in text:
                    return EntityMatch(entity=rule.entity, matched_alias=alias)
        return None

    def _match_triggers(self, text: str) -> list[str]:
        hits: list[str] = []

        for word in self.trigger_words:
            if word.lower() in text:
                hits.append(word)

        return sorted(set(hits))

    def _build_seed(self, entity: str, trigger_words: list[str]) -> str:
        primary_trigger = trigger_words[0]
        return f"Signal around {entity}: {primary_trigger}"

    def _deduplicate(self, candidates: list[SeedCandidate]) -> list[SeedCandidate]:
        seen: set[tuple[str, str, str]] = set()
        unique_candidates: list[SeedCandidate] = []

        for candidate in candidates:
            key = (
                candidate.entity.strip().lower(),
                candidate.seed.strip().lower(),
                self._normalize_text(candidate.raw_text),
            )
            if key in seen:
                continue

            seen.add(key)
            unique_candidates.append(candidate)

        return unique_candidates

    def _normalize_text(self, value: str) -> str:
        return " ".join(value.lower().split())


class EntityMatch(BaseModel):
    entity: str
    matched_alias: str
