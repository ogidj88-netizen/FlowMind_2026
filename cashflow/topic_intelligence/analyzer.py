from __future__ import annotations

from cashflow.topic_intelligence.collector import SeedCandidate
from cashflow.topic_intelligence.models import GapStatus, ValidatedTopic, Verdict


class TopicAnalyzer:
    def analyze_candidate(self, candidate: SeedCandidate) -> ValidatedTopic:
        utility = self._build_utility(candidate)
        pain_evidence = self._build_pain_evidence(candidate)
        anchor_demand = self._build_anchor_demand(candidate)
        gap_status = GapStatus.UNKNOWN
        verdict = self._build_initial_verdict(candidate, utility)

        return ValidatedTopic(
            entity=candidate.entity,
            seed_source=candidate.seed_source,
            seed=candidate.seed,
            anchor_demand=anchor_demand,
            utility=utility,
            gap_status=gap_status,
            pain_evidence=pain_evidence,
            source_link=candidate.source_link,
            source_type=candidate.source_type,
            source_label=candidate.source_label,
            verdict=verdict,
        )

    def _build_utility(self, candidate: SeedCandidate) -> str:
        trigger_words = {word.lower() for word in candidate.trigger_words}
        entity = candidate.entity.lower()

        if {"fee", "fees", "charged", "charge", "overdraft", "late fee", "penalty"} & trigger_words:
            return "User may lose money through unexpected fees, penalties, or avoidable charges."

        if {"blocked", "hold", "frozen", "denied"} & trigger_words:
            return "User may temporarily lose access to money, payments, or transfers."

        if {"apr", "interest", "raised", "increase", "increased", "higher"} & trigger_words and "credit card" in entity:
            return "User may fall deeper into debt because interest charges will grow faster every month."

        if {"rent hike", "raised", "increase", "increased", "higher"} & trigger_words and entity == "rent":
            return "User may face immediate monthly budget pressure because housing costs are rising."

        if {"renewal", "auto renew", "auto-renew", "cancel", "canceled"} & trigger_words:
            return "User may keep losing money on recurring charges they did not actively approve or notice."

        if {"claim denied", "out of pocket", "medical debt"} & trigger_words:
            return "User may be forced to pay large out-of-pocket costs or medical bills unexpectedly."

        if {"spike", "raised", "increase", "increased", "higher"} & trigger_words and entity == "gas prices":
            return "User may face higher commuting and daily living costs as fuel prices rise."

        if {"spike", "raised", "increase", "increased", "higher"} & trigger_words and entity == "groceries":
            return "User may lose buying power because basic food costs are rising faster than expected."

        if {"raised", "increase", "increased", "higher"} & trigger_words and entity == "insurance":
            return "User may pay more every month for the same protection or face weaker coverage."

        if {"raised", "increase", "increased", "higher"} & trigger_words and entity == "student loans":
            return "User may face higher repayment pressure and less room in their monthly budget."

        if {"raised", "increase", "increased", "higher"} & trigger_words and entity == "taxes usa":
            return "User may lose more income to taxes, penalties, or compliance mistakes."

        return "User may lose money, access, or control because a financial rule or cost changed without clear warning."

    def _build_pain_evidence(self, candidate: SeedCandidate) -> str:
        return candidate.raw_text.strip()

    def _build_anchor_demand(self, candidate: SeedCandidate) -> str:
        alias = candidate.matched_alias.strip().lower()
        primary_trigger = candidate.trigger_words[0].strip().lower()
        return f"{alias} {primary_trigger}"

    def _build_initial_verdict(self, candidate: SeedCandidate, utility: str) -> Verdict:
        trigger_count = len(candidate.trigger_words)
        raw_text_length = len(candidate.raw_text.strip())
        trigger_words = {word.lower() for word in candidate.trigger_words}
        entity = candidate.entity.lower()

        if trigger_count >= 2 and raw_text_length >= 60 and self._is_specific_utility(utility):
            return Verdict.BACKLOG

        if (
            entity == "subscriptions"
            and {"cancel", "renewal", "auto renew", "auto-renew", "canceled"} & trigger_words
            and raw_text_length >= 60
            and self._is_specific_utility(utility)
        ):
            return Verdict.BACKLOG

        return Verdict.KILL

    def _is_specific_utility(self, utility: str) -> bool:
        generic_markers = {
            "financial rule",
            "cost changed",
            "without clear warning",
        }

        lowered = utility.lower()
        return not all(marker in lowered for marker in generic_markers)
