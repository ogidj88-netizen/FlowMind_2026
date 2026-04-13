from typing import Dict, List


class TopicIntelligenceLite:
    """
    Minimal deterministic topic generator for Cashflow Mode.

    v1.1 goals:
    - generate 30+ unique topics
    - keep logic simple and deterministic
    - no ML
    - no external APIs
    - no hidden orchestration
    """

    def __init__(self) -> None:
        self.numbers = [3, 5, 7, 9]
        self.money_amounts = ["$50", "$100", "$200", "$500", "$1,000", "$5,000", "$10,000"]

        self.categories = [
            {
                "name": "money_mistakes",
                "subjects": [
                    "money mistakes",
                    "daily money mistakes",
                    "small financial mistakes",
                    "bad money habits",
                ],
                "outcomes": [
                    "that cost you {amount}",
                    "keeping you broke",
                    "that drain your income",
                    "that quietly destroy your budget",
                ],
                "hooks": [
                    "Most people do this and never count the real cost",
                    "These mistakes look harmless until the money is gone",
                    "You may be losing money without noticing it",
                    "The damage feels small until you total it up",
                ],
            },
            {
                "name": "hidden_costs",
                "subjects": [
                    "hidden costs",
                    "everyday expenses",
                    "financial leaks",
                    "quiet money drains",
                ],
                "outcomes": [
                    "that steal {amount} from you",
                    "ruining your finances",
                    "that add up faster than rent",
                    "silently eating your paycheck",
                ],
                "hooks": [
                    "Nobody warns you about these because they look normal",
                    "This is where money disappears in real life",
                    "You probably pay for these without even thinking",
                    "These costs stay invisible until it is too late",
                ],
            },
            {
                "name": "behavior",
                "subjects": [
                    "financial habits",
                    "money behaviors",
                    "normal spending patterns",
                    "monthly decisions",
                ],
                "outcomes": [
                    "that cost you {amount} every month",
                    "making you poorer every year",
                    "that feel normal but hurt your future",
                    "wrecking your finances slowly",
                ],
                "hooks": [
                    "The worst financial habits rarely look dangerous",
                    "What feels normal can still be financially destructive",
                    "This is how people lose money without a crisis",
                    "Bad systems beat good intentions every time",
                ],
            },
        ]

        self.banned_words = [
            "motivation",
            "success tips",
            "how to be rich",
            "inspiration",
            "manifest",
            "mindset only",
        ]

    def generate_topic_pool(self, n: int = 30) -> List[Dict]:
        candidates = self._generate_candidates()
        filtered = self._apply_kill_filters(candidates)
        ranked = self._simple_rank(filtered)
        unique_topics = self._deduplicate(ranked)
        return unique_topics[:n]

    def _generate_candidates(self) -> List[Dict]:
        topics: List[Dict] = []

        for category in self.categories:
            for number in self.numbers:
                for subject in category["subjects"]:
                    for outcome_template in category["outcomes"]:
                        for hook in category["hooks"]:
                            for amount in self.money_amounts:
                                outcome = outcome_template.format(amount=amount)
                                title = f"{number} {subject} {outcome}"
                                topics.append(
                                    {
                                        "title": self._normalize_text(title),
                                        "hook": hook,
                                        "category": category["name"],
                                    }
                                )

        return topics

    def _apply_kill_filters(self, topics: List[Dict]) -> List[Dict]:
        valid_topics: List[Dict] = []

        for topic in topics:
            if self._is_valid_topic(topic):
                valid_topics.append(topic)

        return valid_topics

    def _is_valid_topic(self, topic: Dict) -> bool:
        title = topic["title"].lower()

        for word in self.banned_words:
            if word in title:
                return False

        has_number = any(char.isdigit() for char in title)
        has_money = "$" in title or "cost" in title or "paycheck" in title

        if not has_number:
            return False

        if not has_money:
            return False

        if len(title) < 20:
            return False

        if len(title) > 90:
            return False

        return True

    def _simple_rank(self, topics: List[Dict]) -> List[Dict]:
        def score(topic: Dict) -> int:
            value = 0
            title = topic["title"].lower()
            hook = topic["hook"].lower()

            if "$" in topic["title"]:
                value += 3

            if any(char.isdigit() for char in topic["title"]):
                value += 2

            if "mistake" in title or "mistakes" in title:
                value += 2

            if "cost" in title or "drain" in title or "ruining" in title:
                value += 2

            if "month" in title or "year" in title:
                value += 1

            if "lose" in hook or "destroy" in hook or "disappears" in hook:
                value += 1

            return value

        return sorted(topics, key=score, reverse=True)

    def _deduplicate(self, topics: List[Dict]) -> List[Dict]:
        seen = set()
        unique_topics: List[Dict] = []

        for topic in topics:
            key = (
                topic["title"].strip().lower(),
                topic["hook"].strip().lower(),
                topic["category"].strip().lower(),
            )

            if key in seen:
                continue

            seen.add(key)
            unique_topics.append(topic)

        return unique_topics

    def _normalize_text(self, value: str) -> str:
        cleaned = " ".join(value.split())
        cleaned = cleaned.replace(" ,", ",")
        return cleaned
