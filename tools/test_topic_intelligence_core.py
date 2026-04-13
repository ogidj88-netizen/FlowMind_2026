from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cashflow.topic_intelligence.collector import TopicSeedCollector
from cashflow.topic_intelligence.analyzer import TopicAnalyzer
from cashflow.topic_intelligence.validator import TopicValidator, ValidationInput


def main() -> None:
    texts = [
        "Chase charged me a fee for transferring money between my own accounts.",
        "Bank of America blocked my transaction and put my account on hold.",
        "My credit card interest rate suddenly increased to 29% APR.",
        "My rent increased again and I can't keep up with payments.",
        "My subscription auto-renewed and I didn't even get a warning.",
        "Gas prices are rising again and it's killing my monthly budget.",
    ]

    collector = TopicSeedCollector()
    analyzer = TopicAnalyzer()
    validator = TopicValidator()

    candidates = collector.collect_from_texts(texts=texts)

    print("SEED CANDIDATES")
    print("=" * 60)
    for candidate in candidates:
        print(candidate.model_dump())
    print()

    print("VALIDATED TOPICS")
    print("=" * 60)
    for candidate in candidates:
        topic = analyzer.analyze_candidate(candidate)

        result = validator.validate(
            ValidationInput(
                topic=topic,
                exact_query_volume=0,
                anchor_query_volume=500,  # більш реалістично для US
                top_results_count=5,
                instructional_results_count=0,
            )
        )

        print(result.model_dump())
        print("-" * 60)


if __name__ == "__main__":
    main()
