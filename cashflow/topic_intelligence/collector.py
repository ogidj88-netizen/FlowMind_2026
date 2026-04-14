from __future__ import annotations

import json
import re
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

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
    raw_text: str = Field(..., min_length=1, max_length=12000)


class RedditPost(BaseModel):
    subreddit: str = Field(..., min_length=1, max_length=120)
    title: str = Field(..., min_length=1, max_length=500)
    selftext: str = Field(default="", max_length=10000)
    permalink: str = Field(..., min_length=1, max_length=1000)

    @property
    def combined_text(self) -> str:
        parts = [self.title.strip()]
        if self.selftext.strip():
            parts.append(self.selftext.strip())
        return " ".join(parts).strip()


class EntityMatch(BaseModel):
    entity: str
    matched_alias: str


ENTITY_REGISTRY: list[EntityRule] = [
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
    "collections",
    "debt",
    "default",
)

FINANCIAL_KEYWORDS: tuple[str, ...] = (
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

DEFAULT_SUBREDDITS: tuple[str, ...] = (
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

STRONG_FINANCIAL_SIGNAL_RE = re.compile(
    r"(\$[\d,]+|\b\d+%|\b\d+\s?(usd|dollars|bucks|apr)\b|\bdebt\b|\bpayment\b|\bcharged\b|\bfee\b|\bcollections\b|\bcredit score\b|\bcredit limit\b)",
    re.IGNORECASE,
)


class TopicSeedCollector:
    def __init__(
        self,
        entity_registry: list[EntityRule] | None = None,
        trigger_words: Iterable[str] | None = None,
        financial_keywords: Iterable[str] | None = None,
        user_agent: str = "FlowMindTopicCollector/1.0",
    ) -> None:
        self.entity_registry = entity_registry or ENTITY_REGISTRY
        self.trigger_words = tuple(trigger_words or TRIGGER_WORDS)
        self.financial_keywords = tuple(financial_keywords or FINANCIAL_KEYWORDS)
        self.user_agent = user_agent

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

            if not self._is_financially_relevant(normalized_text):
                continue

            if self._looks_like_weak_context(normalized_text):
                continue

            relevance_score = self._calculate_relevance_score(
                text=normalized_text,
                entity_match=entity_match,
                matched_triggers=matched_triggers,
            )
            if relevance_score < 4:
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

    def collect_from_reddit(
        self,
        subreddits: list[str] | None = None,
        limit_per_subreddit: int = 10,
        seed_source: SeedSource = SeedSource.SOCIAL_SIGNAL,
    ) -> list[SeedCandidate]:
        target_subreddits = subreddits or list(DEFAULT_SUBREDDITS)
        reddit_posts = self.fetch_reddit_posts(
            subreddits=target_subreddits,
            limit_per_subreddit=limit_per_subreddit,
        )
        texts = [post.combined_text for post in reddit_posts if post.combined_text]
        return self.collect_from_texts(texts=texts, seed_source=seed_source)

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
        params = urlencode({"limit": max(1, min(limit, 100))})
        url = f"https://www.reddit.com/r/{subreddit}/new.json?{params}"

        request = Request(
            url=url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json",
            },
        )

        try:
            with urlopen(request, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            return []

        children = payload.get("data", {}).get("children", [])
        posts: list[RedditPost] = []

        for child in children:
            data = child.get("data", {})
            title = str(data.get("title", "")).strip()
            if not title:
                continue

            permalink = str(data.get("permalink", "")).strip()
            if not permalink:
                continue

            posts.append(
                RedditPost(
                    subreddit=subreddit,
                    title=title,
                    selftext=str(data.get("selftext", "")).strip(),
                    permalink=f"https://www.reddit.com{permalink}",
                )
            )

        return posts

    def _calculate_relevance_score(
        self,
        text: str,
        entity_match: EntityMatch,
        matched_triggers: list[str],
    ) -> int:
        score = 0

        if self._is_financially_relevant(text):
            score += 1

        if self._has_strong_financial_signal(text):
            score += 1

        if self._has_hard_pain(text):
            score += 2
        elif self._has_soft_pain(text):
            score += 1

        if len(matched_triggers) >= 2:
            score += 1

        if entity_match.entity in {"Credit Card Debt", "Student Loans", "Rent", "Taxes USA"}:
            score += 1

        return score

    def _is_financially_relevant(self, text: str) -> bool:
        keyword_hits = 0

        for keyword in self.financial_keywords:
            if keyword.lower() in text:
                keyword_hits += 1

        has_money_pattern = bool(
            re.search(r"(\$[\d,]+|\b\d+%|\b\d+\s?(usd|dollars|bucks|apr)\b)", text)
        )

        return keyword_hits >= 2 or (keyword_hits >= 1 and has_money_pattern)

    def _has_strong_financial_signal(self, text: str) -> bool:
        return bool(STRONG_FINANCIAL_SIGNAL_RE.search(text))

    def _looks_like_weak_context(self, text: str) -> bool:
        for pattern in WEAK_CONTEXT_PATTERNS:
            if pattern in text:
                return True
        return False

    def _has_hard_pain(self, text: str) -> bool:
        return any(pattern in text for pattern in HARD_PAIN_PATTERNS)

    def _has_soft_pain(self, text: str) -> bool:
        return any(pattern in text for pattern in SOFT_PAIN_PATTERNS)

    def _match_entity(self, text: str) -> EntityMatch | None:
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
