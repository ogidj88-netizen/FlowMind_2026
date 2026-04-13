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
    EntityRule(entity="Monobank", aliases=["monobank", "mono", "монобанк", "моно"]),
    EntityRule(entity="PrivatBank", aliases=["privatbank", "privat", "приватбанк", "приват"]),
    EntityRule(entity="Taxes", aliases=["tax", "taxes", "податок", "податки", "фоп"]),
    EntityRule(entity="Utilities", aliases=["комуналка", "тариф", "тарифи", "світло", "газ"]),
    EntityRule(entity="Credits", aliases=["credit", "credits", "кредит", "кредити", "розстрочка"]),
    EntityRule(entity="OVDP", aliases=["овдп", "obligation", "bond", "bonds"]),
]

TRIGGER_WORDS: tuple[str, ...] = (
    "зняли",
    "комісія",
    "комиссия",
    "підняли",
    "подняли",
    "заблокували",
    "блок",
    "ліміт",
    "лимит",
    "не прийшло",
    "списали",
    "списание",
    "штраф",
    "відсоток",
    "процент",
    "подорожчало",
    "дороже",
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
