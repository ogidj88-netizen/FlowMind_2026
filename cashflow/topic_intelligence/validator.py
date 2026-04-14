import json
import os
import re
import urllib.parse
import urllib.request
from typing import Dict, List


DEFAULT_YOUTUBE_DAILY_LIMIT = 100
DEFAULT_SEARCH_COST_UNITS = 100
DEFAULT_MAX_RESULTS = 5


class ValidationResult:
    def __init__(
        self,
        topic: str,
        is_valid: bool,
        score: int,
        matched_titles: List[str],
        fetched_titles: List[str],
        quota_used: int,
        quota_limit: int,
    ):
        self.topic = topic
        self.is_valid = is_valid
        self.score = score
        self.matched_titles = matched_titles
        self.fetched_titles = fetched_titles
        self.quota_used = quota_used
        self.quota_limit = quota_limit

    def to_dict(self) -> Dict:
        return {
            "topic": self.topic,
            "is_valid": self.is_valid,
            "score": self.score,
            "matched_titles": self.matched_titles,
            "fetched_titles": self.fetched_titles,
            "quota_used": self.quota_used,
            "quota_limit": self.quota_limit,
        }


def load_env_file(env_path: str = ".env") -> None:
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key and key not in os.environ:
                os.environ[key] = value


class YouTubeValidator:
    def __init__(
        self,
        api_key: str,
        max_results: int = DEFAULT_MAX_RESULTS,
        daily_limit_units: int = DEFAULT_YOUTUBE_DAILY_LIMIT,
        search_cost_units: int = DEFAULT_SEARCH_COST_UNITS,
    ):
        if not api_key:
            raise ValueError("YOUTUBE_API_KEY is missing")

        if max_results < 1:
            raise ValueError("max_results must be >= 1")

        self.api_key = api_key
        self.max_results = max_results
        self.daily_limit_units = daily_limit_units
        self.search_cost_units = search_cost_units

    def fetch_titles(self, topic: str) -> List[str]:
        if self.search_cost_units > self.daily_limit_units:
            raise ValueError("YouTube daily quota limit is lower than one search request cost")

        query_params = {
            "part": "snippet",
            "q": topic,
            "type": "video",
            "order": "relevance",
            "maxResults": str(self.max_results),
            "key": self.api_key,
        }

        url = (
            "https://www.googleapis.com/youtube/v3/search?"
            + urllib.parse.urlencode(query_params)
        )

        request = urllib.request.Request(
            url,
            headers={"Accept": "application/json"},
            method="GET",
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))

        items = payload.get("items", [])
        titles: List[str] = []

        for item in items:
            snippet = item.get("snippet", {})
            title = snippet.get("title", "").strip()

            if title:
                titles.append(title)

        return titles

    def validate(self, topic: str) -> ValidationResult:
        youtube_titles = self.fetch_titles(topic)
        topic_tokens = self._normalize_tokens(topic)
        matched: List[str] = []

        for title in youtube_titles:
            title_tokens = self._normalize_tokens(title)

            if self._is_match(topic_tokens, title_tokens):
                matched.append(title)

        score = len(matched)
        is_valid = score >= 2

        return ValidationResult(
            topic=topic,
            is_valid=is_valid,
            score=score,
            matched_titles=matched,
            fetched_titles=youtube_titles,
            quota_used=self.search_cost_units,
            quota_limit=self.daily_limit_units,
        )

    def _normalize_tokens(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^a-z0-9\s]+", " ", text.lower())
        raw_tokens = cleaned.split()

        stop_words = {
            "a", "an", "the", "and", "or", "to", "of", "in", "on", "for",
            "my", "your", "why", "how", "what", "after", "with", "fast",
            "fix", "get", "no", "reason",
        }

        tokens: List[str] = []

        for token in raw_tokens:
            if len(token) < 3:
                continue
            if token in stop_words:
                continue
            tokens.append(token)

        return tokens

    def _is_match(self, topic_tokens: List[str], title_tokens: List[str]) -> bool:
        if not topic_tokens or not title_tokens:
            return False

        title_set = set(title_tokens)
        overlap = [token for token in topic_tokens if token in title_set]

        overlap_count = len(overlap)
        required_overlap = max(2, (len(topic_tokens) + 1) // 2)

        if overlap_count < required_overlap:
            return False

        strong_pain_terms = {
            "dropped",
            "suddenly",
            "overnight",
            "tank",
            "tanked",
            "declined",
            "dropped",
            "fall",
            "fell",
            "crash",
            "dropped",
        }

        topic_pain = [token for token in topic_tokens if token in strong_pain_terms]

        if topic_pain:
            title_pain_overlap = [token for token in topic_pain if token in title_set]
            if not title_pain_overlap:
                return False

        return True


if __name__ == "__main__":
    load_env_file()

    topic = "credit score dropped suddenly"
    api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()

    daily_limit_raw = os.environ.get("YOUTUBE_DAILY_LIMIT", str(DEFAULT_YOUTUBE_DAILY_LIMIT)).strip()
    daily_limit_units = int(daily_limit_raw) if daily_limit_raw else DEFAULT_YOUTUBE_DAILY_LIMIT

    validator = YouTubeValidator(
        api_key=api_key,
        max_results=DEFAULT_MAX_RESULTS,
        daily_limit_units=daily_limit_units,
        search_cost_units=DEFAULT_SEARCH_COST_UNITS,
    )

    result = validator.validate(topic)
    print(result.to_dict())
