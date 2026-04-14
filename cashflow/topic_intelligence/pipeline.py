import os

from cashflow.topic_intelligence.analyzer import TopicAnalyzer
from cashflow.topic_intelligence.collector import SeedCandidate
from cashflow.topic_intelligence.models import ValidatedTopic, Verdict
from cashflow.topic_intelligence.validator import YouTubeValidator, load_env_file


class TopicPipeline:
    def __init__(self):
        load_env_file()

        api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()
        daily_limit = int(os.environ.get("YOUTUBE_DAILY_LIMIT", "1000"))

        self.validator = YouTubeValidator(
            api_key=api_key,
            daily_limit_units=daily_limit,
        )
        self.analyzer = TopicAnalyzer()

    def process(self, candidate: SeedCandidate) -> ValidatedTopic | None:
        validation = self.validator.validate(candidate.seed)

        if not validation.is_valid:
            return None

        analyzed = self.analyzer.analyze_candidate(candidate)

        enriched_pain_evidence = (
            f"{analyzed.pain_evidence}\n\n"
            f"YouTube validation matched {validation.score} titles: "
            + " | ".join(validation.matched_titles[:3])
        )

        final_verdict = analyzed.verdict
        if analyzed.verdict == Verdict.KILL:
            final_verdict = Verdict.BACKLOG

        return analyzed.model_copy(
            update={
                "pain_evidence": enriched_pain_evidence,
                "verdict": final_verdict,
            }
        )


if __name__ == "__main__":
    from cashflow.topic_intelligence.collector import SeedSource

    test_candidate = SeedCandidate(
        entity="Credit Card Debt",
        seed_source=SeedSource.SOCIAL_SIGNAL,
        seed="credit score dropped suddenly",
        matched_alias="credit score",
        trigger_words=["dropped", "suddenly"],
        raw_text="My credit score suddenly dropped and I don't know why",
    )

    pipeline = TopicPipeline()
    result = pipeline.process(test_candidate)

    if result:
        print(result.model_dump())
    else:
        print("REJECTED BY VALIDATOR")
