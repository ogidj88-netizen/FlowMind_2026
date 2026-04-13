from __future__ import annotations

from pydantic import BaseModel, Field

from cashflow.topic_intelligence.models import GapStatus, ValidatedTopic, Verdict


class ValidationInput(BaseModel):
    topic: ValidatedTopic
    exact_query_volume: int = Field(default=0, ge=0)
    anchor_query_volume: int = Field(default=0, ge=0)
    top_results_count: int = Field(default=0, ge=0)
    instructional_results_count: int = Field(default=0, ge=0)


class ValidationResult(BaseModel):
    topic: ValidatedTopic
    demand_passed: bool
    gap_passed: bool
    final_verdict: Verdict


class TopicValidator:
    def validate(self, data: ValidationInput) -> ValidationResult:
        demand_passed = self._check_demand(data)
        gap_status, gap_passed = self._check_gap(data)

        final_verdict = self._build_final_verdict(
            topic=data.topic,
            demand_passed=demand_passed,
            gap_passed=gap_passed,
        )

        updated_topic = data.topic.model_copy(
            update={
                "gap_status": gap_status,
                "verdict": final_verdict,
            }
        )

        return ValidationResult(
            topic=updated_topic,
            demand_passed=demand_passed,
            gap_passed=gap_passed,
            final_verdict=final_verdict,
        )

    def _check_demand(self, data: ValidationInput) -> bool:
        if data.exact_query_volume > 0:
            return True

        if data.anchor_query_volume >= 100:
            return True

        return False

    def _check_gap(self, data: ValidationInput) -> tuple[GapStatus, bool]:
        if data.top_results_count == 0:
            return GapStatus.GAP_DETECTED, True

        if data.instructional_results_count == 0:
            return GapStatus.GAP_DETECTED, True

        return GapStatus.INSTRUCTIONAL_COVERAGE_EXISTS, False

    def _build_final_verdict(
        self,
        topic: ValidatedTopic,
        demand_passed: bool,
        gap_passed: bool,
    ) -> Verdict:
        if not demand_passed:
            return Verdict.KILL

        if not gap_passed:
            return Verdict.BACKLOG

        if topic.verdict == Verdict.KILL:
            return Verdict.BACKLOG

        return Verdict.PRIORITY
