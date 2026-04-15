from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class SeedSource(str, Enum):
    SOCIAL_SIGNAL = "social_signal"
    SEARCH_SIGNAL = "search_signal"
    MANUAL = "manual"


@dataclass(frozen=True)
class EntityRule:
    entity: str
    aliases: list[str]


@dataclass(frozen=True)
class EntityMatch:
    entity: str
    matched_alias: str


@dataclass(frozen=True)
class RedditPost:
    subreddit: str
    title: str
    selftext: str
    permalink: str

    @property
    def combined_text(self) -> str:
        parts = [self.title.strip(), self.selftext.strip()]
        return " ".join(part for part in parts if part).strip()


@dataclass(frozen=True)
class SeedCandidate:
    entity: str
    seed_source: str
    seed: str
    matched_alias: str
    trigger_words: list[str]
    raw_text: str
    source_link: str | None = None
    source_type: str = "unknown"
    source_label: str = "unknown"


LEGACY_ENTITY_REGISTRY: list[EntityRule] = [
    EntityRule(entity="Bank of America", aliases=["bank of america", "boa", "bofa"]),
    EntityRule(entity="Chase", aliases=["chase", "chase bank", "jp morgan chase", "jpmorgan chase"]),
    EntityRule(entity="Wells Fargo", aliases=["wells fargo", "wells"]),
    EntityRule(entity="Credit Card Debt", aliases=["credit card", "credit cards", "card debt", "credit card debt", "apr"]),
    EntityRule(entity="Student Loans", aliases=["student loan", "student loans", "loan payment", "federal loans"]),
    EntityRule(entity="Taxes USA", aliases=["irs", "tax refund", "taxes", "tax bill", "tax return"]),
    EntityRule(entity="Rent", aliases=["rent", "rent increase", "landlord", "lease", "rental property", "rental"]),
    EntityRule(entity="Healthcare Costs", aliases=["healthcare", "medical bill", "hospital bill", "insurance denial"]),
    EntityRule(entity="Insurance", aliases=["insurance", "premium", "claim denied", "coverage", "home warranty"]),
    EntityRule(entity="Subscriptions", aliases=["subscription", "subscriptions", "auto renew", "auto-renew", "renewal"]),
    EntityRule(entity="Gas Prices", aliases=["gas prices", "gas", "fuel", "gas station"]),
    EntityRule(entity="Groceries", aliases=["groceries", "grocery bill", "food prices", "supermarket"]),
    EntityRule(entity="Inflation", aliases=["inflation", "price increase", "prices rising", "cost of living"]),
]

LEGACY_TRIGGER_WORDS: tuple[str, ...] = (
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
    "collections",
    "debt",
    "default",
)

LEGACY_FINANCIAL_KEYWORDS: tuple[str, ...] = (
    "money",
    "debt",
    "bill",
    "bills",
    "payment",
    "payments",
    "income",
    "expense",
    "expenses",
    "budget",
    "cost",
    "costs",
    "price",
    "prices",
    "fee",
    "fees",
    "charge",
    "charged",
    "overdraft",
    "interest",
    "apr",
    "loan",
    "loans",
    "mortgage",
    "rent",
    "refund",
    "tax",
    "taxes",
    "irs",
    "insurance",
    "premium",
    "claim",
    "medical bill",
    "medical debt",
    "salary",
    "paycheck",
    "paycheck to paycheck",
    "collections",
    "credit score",
    "credit limit",
    "subscription",
    "subscriptions",
    "gas",
    "grocery",
    "groceries",
    "inflation",
    "cost of living",
    "bank account",
    "transaction",
    "cash back",
)

LEGACY_DEFAULT_SUBREDDITS: tuple[str, ...] = (
    "personalfinance",
    "povertyfinance",
    "Frugal",
    "CreditCards",
    "StudentLoans",
    "Insurance",
)

WEAK_CONTEXT_PATTERNS: tuple[str, ...] = (
    "what's your favorite",
    "what is your favorite",
    "what do you guys think",
    "best cheap",
    "go-to meal",
    "eat out",
    "coffee bean",
    "food hacks",
)

HARD_PAIN_PATTERNS: tuple[str, ...] = (
    "i was charged",
    "they charged me",
    "i got charged",
    "my account was blocked",
    "my account got blocked",
    "account blocked",
    "account frozen",
    "my card was blocked",
    "my transaction was blocked",
    "transaction declined",
    "transaction blocked",
    "my account is on hold",
    "put my account on hold",
    "lost money",
    "took money",
    "took funds",
    "overdraft fee",
    "late fee",
    "debt collectors",
    "in collections",
    "sent to collections",
    "cannot pay",
    "can't pay",
    "struggling to pay",
    "missed payment",
    "payment failed",
    "rent increased",
    "my rent increased",
    "interest rate increased",
    "apr increased",
    "auto-renewed",
    "auto renewed",
    "claim denied",
    "denied my claim",
    "default",
    "my score tanked",
)

SOFT_PAIN_PATTERNS: tuple[str, ...] = (
    "in debt",
    "living paycheck to paycheck",
    "struggling financially",
    "can't afford",
    "cannot afford",
    "too expensive",
    "rent is too high",
    "interest is killing me",
    "barely making it",
    "financially behind",
    "my budget is tight",
    "my budget is stretched",
    "my payment is too high",
    "my bills are too high",
    "i'm behind on",
    "i am behind on",
)

GENERIC_TRIGGER_WORDS: frozenset[str] = frozenset(
    {
        "hold",
        "debt",
        "limit",
        "delay",
        "delayed",
        "missed",
        "penalty",
        "default",
    }
)

STRONG_ENTITY_ALIASES: frozenset[str] = frozenset(
    {
        "bank of america",
        "boa",
        "bofa",
        "chase",
        "chase bank",
        "jp morgan chase",
        "jpmorgan chase",
        "wells fargo",
        "irs",
        "subscription",
        "subscriptions",
        "insurance",
        "student loan",
        "student loans",
        "credit card",
        "credit cards",
    }
)

ENTITY_MECHANISM_MAP: dict[str, tuple[str, ...]] = {
    "insurance": ("premium", "claim", "coverage", "deductible", "copay", "policy", "denial"),
    "subscriptions": ("renewal", "cancel", "canceled", "auto renew", "auto-renew", "trial", "billing", "charge"),
    "rent": ("lease", "landlord", "deposit", "eviction", "tenant", "rental"),
    "student loans": ("loan", "payment", "forbearance", "servicer", "federal", "repayment"),
    "credit card debt": ("apr", "interest", "minimum payment", "credit limit", "late fee", "balance"),
    "taxes usa": ("irs", "refund", "tax bill", "return", "penalty", "withholding"),
    "healthcare costs": ("medical bill", "hospital", "claim", "coverage", "copay", "deductible"),
}

STRONG_SIGNAL_RE = re.compile(
    r"(\$[\d,]+|\b\d+%|\b\d+\s?(usd|dollars|bucks|apr)\b|\bdebt\b|\bpayment\b|\bcharged\b|\bfee\b|\bcollections\b|\bcredit score\b|\bcredit limit\b)",
    re.IGNORECASE,
)


class TopicSeedCollector:
    def __init__(
        self,
        entity_registry: list[EntityRule] | None = None,
        trigger_words: Iterable[str] | None = None,
        financial_keywords: Iterable[str] | None = None,
        default_subreddits: Iterable[str] | None = None,
        user_agent: str = "FlowMindTopicCollector/1.0",
    ) -> None:
        self.entity_registry = entity_registry or LEGACY_ENTITY_REGISTRY
        self.trigger_words = tuple(trigger_words or LEGACY_TRIGGER_WORDS)
        self.financial_keywords = tuple(financial_keywords or LEGACY_FINANCIAL_KEYWORDS)
        self.default_subreddits = tuple(default_subreddits or LEGACY_DEFAULT_SUBREDDITS)
        self.user_agent = user_agent

    def collect_from_texts(
        self,
        texts: list[str],
        seed_source: SeedSource = SeedSource.SOCIAL_SIGNAL,
        source_link: str | None = None,
        source_type: str = "unknown",
        source_label: str = "unknown",
    ) -> list[SeedCandidate]:
        candidates: list[SeedCandidate] = []

        normalized_source_link = source_link.strip() if source_link else None
        normalized_source_type = source_type.strip() or "unknown"
        normalized_source_label = source_label.strip() or "unknown"
        seed_source_value = seed_source.name if isinstance(seed_source, SeedSource) else str(seed_source)

        for text in texts:
            normalized_text = self._normalize_text(text)
            if not normalized_text:
                continue

            if not self._passes_context_gate(normalized_text):
                continue

            entity_match = self._match_entity(normalized_text)
            if entity_match is None:
                continue

            matched_triggers = self._match_triggers(normalized_text)
            if not matched_triggers:
                continue

            if not self._passes_trigger_quality_gate(
                text=normalized_text,
                entity_match=entity_match,
                matched_triggers=matched_triggers,
            ):
                continue

            relevance_score = self._calculate_relevance_score(
                text=normalized_text,
                entity_match=entity_match,
                matched_triggers=matched_triggers,
            )
            if relevance_score < 5:
                continue

            seed_value = self._build_seed(entity_match.entity, matched_triggers)
            if not seed_value:
                continue

            candidates.append(
                SeedCandidate(
                    entity=entity_match.entity,
                    seed_source=seed_source_value,
                    seed=seed_value,
                    matched_alias=entity_match.matched_alias,
                    trigger_words=matched_triggers,
                    raw_text=normalized_text,
                    source_link=normalized_source_link,
                    source_type=normalized_source_type,
                    source_label=normalized_source_label,
                )
            )

        return self._deduplicate(candidates)

    def collect_from_reddit(
        self,
        subreddits: list[str] | None = None,
        limit_per_subreddit: int = 10,
        seed_source: SeedSource = SeedSource.SOCIAL_SIGNAL,
    ) -> list[SeedCandidate]:
        target_subreddits = subreddits or list(self.default_subreddits)
        reddit_posts = self.fetch_reddit_posts(
            subreddits=target_subreddits,
            limit_per_subreddit=limit_per_subreddit,
        )

        all_candidates: list[SeedCandidate] = []

        for post in reddit_posts:
            if not post.combined_text:
                continue

            post_candidates = self.collect_from_texts(
                texts=[post.combined_text],
                seed_source=seed_source,
                source_link=post.permalink,
                source_type="reddit",
                source_label=post.subreddit,
            )
            all_candidates.extend(post_candidates)

        return self._deduplicate(all_candidates)

    def fetch_reddit_posts(
        self,
        subreddits: list[str],
        limit_per_subreddit: int = 10,
    ) -> list[RedditPost]:
        posts: list[RedditPost] = []

        for subreddit in subreddits:
            posts.extend(
                self._fetch_subreddit_posts(
                    subreddit=subreddit,
                    limit=limit_per_subreddit,
                )
            )

        return posts

    def _fetch_subreddit_posts(self, subreddit: str, limit: int) -> list[RedditPost]:
        params = urlencode({"limit": limit})
        url = f"https://www.reddit.com/r/{subreddit}/new.json?{params}"

        request = Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json",
            },
            method="GET",
        )

        try:
            with urlopen(request, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            return []

        children = payload.get("data", {}).get("children", [])
        posts: list[RedditPost] = []

        for child in children:
            data = child.get("data", {})
            title = str(data.get("title", "")).strip()
            selftext = str(data.get("selftext", "")).strip()
            permalink = str(data.get("permalink", "")).strip()

            if not title or not permalink:
                continue

            posts.append(
                RedditPost(
                    subreddit=subreddit,
                    title=title,
                    selftext=selftext,
                    permalink=f"https://www.reddit.com{permalink}",
                )
            )

        return posts

    def _passes_context_gate(self, text: str) -> bool:
        lowered = text.lower()

        for weak_pattern in WEAK_CONTEXT_PATTERNS:
            if weak_pattern in lowered:
                return False

        keyword_hits = 0
        for keyword in self.financial_keywords:
            if self._contains_phrase(lowered, keyword.lower()):
                keyword_hits += 1

        has_signal_pattern = bool(STRONG_SIGNAL_RE.search(text))
        return keyword_hits >= 2 or (keyword_hits >= 1 and has_signal_pattern)

    def _passes_trigger_quality_gate(
        self,
        text: str,
        entity_match: EntityMatch,
        matched_triggers: list[str],
    ) -> bool:
        lowered = text.lower()
        alias_lower = entity_match.matched_alias.lower()
        entity_lower = entity_match.entity.lower()

        if entity_lower == "subscriptions":
            if any(
                trigger.lower() in {"cancel", "renewal", "auto renew", "auto-renew"}
                for trigger in matched_triggers
            ):
                return True

        if not self._has_entity_trigger_coupling(lowered, alias_lower, matched_triggers):
            if not any(pattern in lowered for pattern in HARD_PAIN_PATTERNS):
                return False

        if self._requires_mechanism_gate(entity_lower, matched_triggers):
            if not self._has_entity_mechanism_support(lowered, alias_lower, entity_lower):
                return False

        if len(matched_triggers) >= 2:
            return True

        primary_trigger = matched_triggers[0].lower()

        if primary_trigger not in GENERIC_TRIGGER_WORDS:
            return True

        if any(pattern in lowered for pattern in HARD_PAIN_PATTERNS):
            return True

        if STRONG_SIGNAL_RE.search(text) and alias_lower in STRONG_ENTITY_ALIASES:
            return True

        return False

    def _calculate_relevance_score(
        self,
        text: str,
        entity_match: EntityMatch,
        matched_triggers: list[str],
    ) -> int:
        lowered = text.lower()
        score = 0
        alias_lower = entity_match.matched_alias.lower()
        entity_lower = entity_match.entity.lower()

        if entity_lower == "subscriptions":
            score += 2

        if self._contains_phrase(lowered, alias_lower):
            score += 1

        if len(alias_lower) >= 6:
            score += 1

        if len(matched_triggers) >= 2:
            score += 2
        elif matched_triggers and matched_triggers[0].lower() not in GENERIC_TRIGGER_WORDS:
            score += 1

        if self._has_entity_trigger_coupling(lowered, alias_lower, matched_triggers):
            score += 2

        if self._has_entity_mechanism_support(lowered, alias_lower, entity_lower):
            score += 2

        if any(pattern in lowered for pattern in HARD_PAIN_PATTERNS):
            score += 2
        elif any(pattern in lowered for pattern in SOFT_PAIN_PATTERNS):
            score += 1

        if STRONG_SIGNAL_RE.search(text):
            score += 1

        if entity_match.entity in {"Credit Card Debt", "Student Loans", "Subscriptions", "Insurance"}:
            score += 1

        if matched_triggers and matched_triggers[0].lower() in GENERIC_TRIGGER_WORDS and not any(
            pattern in lowered for pattern in HARD_PAIN_PATTERNS
        ):
            score -= 1

        return score

    def _match_entity(self, text: str) -> EntityMatch | None:
        lowered = text.lower()
        best_match: EntityMatch | None = None
        best_alias_length = -1

        for rule in self.entity_registry:
            for alias in rule.aliases:
                alias_lower = alias.lower()
                if not self._contains_phrase(lowered, alias_lower):
                    continue

                alias_length = len(alias_lower)
                if alias_length > best_alias_length:
                    best_alias_length = alias_length
                    best_match = EntityMatch(entity=rule.entity, matched_alias=alias)

        return best_match

    def _match_triggers(self, text: str) -> list[str]:
        lowered = text.lower()
        hits: list[str] = []

        for word in self.trigger_words:
            if self._contains_phrase(lowered, word.lower()):
                hits.append(word)

        return sorted(set(hits), key=lambda value: (-len(value), value.lower()))

    def _build_seed(self, entity: str, trigger_words: list[str]) -> str:
        entity_lower = entity.strip().lower()
        primary_trigger = trigger_words[0].strip().lower()

        if entity_lower == "subscriptions":
            subscription_seed_map = {
                "cancel": "subscription hard to cancel",
                "canceled": "subscription canceled unexpectedly",
                "renewal": "subscription auto-renewed",
                "auto renew": "subscription auto-renewed",
                "auto-renew": "subscription auto-renewed",
                "charged": "subscription charged unexpectedly",
                "charge": "subscription charged unexpectedly",
                "fee": "subscription fee added",
                "fees": "subscription fees added",
                "kept charging": "subscription keeps charging",
                "keeps charging": "subscription keeps charging",
                "charged after trial": "subscription charged after free trial",
                "free trial turned into": "free trial turned into paid subscription",
                "trick you into paying more": "subscription tricked users into paying more",
                "dark pattern": "subscription dark pattern",
                "fine print": "subscription hidden in fine print",
                "cancelation trick": "subscription cancelation trick",
                "cancellation trick": "subscription cancellation trick",
            }
            return subscription_seed_map.get(primary_trigger, "subscription billing issue")

        trigger_phrase_map = {
            "apr": "apr increased",
            "fee": "unexpected fee charged",
            "fees": "unexpected fees charged",
            "charged": "unexpected charge",
            "charge": "unexpected charge",
            "overdraft": "overdraft fee hit",
            "late fee": "late fee charged",
            "renewal": "subscription auto-renewed",
            "auto renew": "subscription auto-renewed",
            "auto-renew": "subscription auto-renewed",
            "cancel": "subscription hard to cancel",
            "canceled": "subscription canceled unexpectedly",
            "medical debt": "medical debt hit",
            "debt": "debt pressure",
            "hold": "payment hold",
            "penalty": "penalty hit",
            "spike": "spike",
        }

        entity_phrase_map = {
            "credit card debt": "credit card debt",
            "bank of america": "bank of america account",
            "chase": "chase account",
            "taxes usa": "irs issue",
            "rent": "rent payment",
        }

        entity_phrase = entity_phrase_map.get(entity_lower, entity_lower)
        trigger_phrase = trigger_phrase_map.get(primary_trigger, primary_trigger)

        if trigger_phrase in entity_phrase:
            return entity_phrase.strip()

        if entity_phrase.endswith(trigger_phrase):
            return entity_phrase.strip()

        seed = f"{entity_phrase} {trigger_phrase}".strip()
        seed = re.sub(r"\s+", " ", seed).strip()

        duplicate_token_patterns = (
            "apr apr",
            "debt debt",
            "rent rent",
            "fee fee",
            "hold hold",
        )
        lowered_seed = seed.lower()
        for pattern in duplicate_token_patterns:
            if pattern in lowered_seed:
                return ""

        return seed

    def _deduplicate(self, candidates: list[SeedCandidate]) -> list[SeedCandidate]:
        seen: set[tuple[str, str, str, str | None]] = set()
        unique_candidates: list[SeedCandidate] = []

        for candidate in candidates:
            key = (
                candidate.entity.strip().lower(),
                candidate.seed.strip().lower(),
                self._normalize_text(candidate.raw_text),
                str(candidate.source_link).strip().lower() if candidate.source_link else None,
            )
            if key in seen:
                continue

            seen.add(key)
            unique_candidates.append(candidate)

        return unique_candidates

    def _normalize_text(self, value: str) -> str:
        return " ".join(value.lower().split())

    def _contains_phrase(self, text: str, phrase: str) -> bool:
        pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
        return bool(re.search(pattern, text))

    def _has_entity_trigger_coupling(
        self,
        text: str,
        alias: str,
        triggers: list[str],
        window_tokens: int = 12,
    ) -> bool:
        tokens = self._tokenize_text(text)

        alias_token_count = len(alias.split())
        alias_positions: list[int] = []

        for idx in range(len(tokens) - alias_token_count + 1):
            chunk = " ".join(tokens[idx : idx + alias_token_count])
            if chunk == alias:
                alias_positions.append(idx)

        if not alias_positions:
            return False

        trigger_positions: list[int] = []
        for trigger in triggers:
            trigger_lower = trigger.lower()
            trigger_token_count = len(trigger_lower.split())

            for idx in range(len(tokens) - trigger_token_count + 1):
                chunk = " ".join(tokens[idx : idx + trigger_token_count])
                if chunk == trigger_lower:
                    trigger_positions.append(idx)

        if not trigger_positions:
            return False

        for alias_pos in alias_positions:
            for trigger_pos in trigger_positions:
                if abs(trigger_pos - alias_pos) <= window_tokens:
                    return True

        return False

    def _requires_mechanism_gate(self, entity: str, triggers: list[str]) -> bool:
        if entity not in ENTITY_MECHANISM_MAP:
            return False

        return any(trigger.lower() in GENERIC_TRIGGER_WORDS for trigger in triggers)

    def _has_entity_mechanism_support(
        self,
        text: str,
        alias: str,
        entity: str,
        window_tokens: int = 16,
    ) -> bool:
        mechanism_terms = ENTITY_MECHANISM_MAP.get(entity, ())
        if not mechanism_terms:
            return True

        tokens = self._tokenize_text(text)
        alias_token_count = len(alias.split())
        alias_positions: list[int] = []

        for idx in range(len(tokens) - alias_token_count + 1):
            chunk = " ".join(tokens[idx : idx + alias_token_count])
            if chunk == alias:
                alias_positions.append(idx)

        if not alias_positions:
            return False

        mechanism_positions: list[int] = []
        for term in mechanism_terms:
            term_lower = term.lower()
            term_token_count = len(term_lower.split())

            for idx in range(len(tokens) - term_token_count + 1):
                chunk = " ".join(tokens[idx : idx + term_token_count])
                if chunk == term_lower:
                    mechanism_positions.append(idx)

        if not mechanism_positions:
            return False

        for alias_pos in alias_positions:
            for mechanism_pos in mechanism_positions:
                if abs(mechanism_pos - alias_pos) <= window_tokens:
                    return True

        return False

    def _tokenize_text(self, text: str) -> list[str]:
        return re.findall(r"[a-z0-9%$]+", text.lower())
