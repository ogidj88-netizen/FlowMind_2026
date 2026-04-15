from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cashflow.topic_intelligence.collector import TopicSeedCollector
from cashflow.topic_intelligence.pipeline import TopicPipeline


def main() -> None:
    texts = [
        "Chase charged me a fee for transferring money between my own accounts.",
        "Bank of America blocked my transaction and put my account on hold.",
        "My credit card interest rate suddenly increased to 29% APR.",
        "My rent increased again and I can't keep up with payments.",
        "My subscription auto-renewed and I didn't even get a warning.",
        "Gas prices are rising again and it's killing my monthly budget.",
        "My credit score suddenly dropped and I don't know why.",
        "My insurance premium went up again for no reason.",
        "My grocery bill keeps getting higher every month.",
        "I got hit with another overdraft fee this week.",
    ]

    collector = TopicSeedCollector()
    pipeline = TopicPipeline()

    candidates = collector.collect_from_texts(texts=texts)

    print("RECOMMENDED TOPICS")
    print("=" * 80)

    recommended_count = 0

    for candidate in candidates:
        result = pipeline.process(candidate)

        if result is None:
            continue

        if result.verdict.value not in {"PRIORITY", "BACKLOG"}:
            continue

        recommended_count += 1
        print(result.model_dump())
        print("-" * 80)

    if recommended_count == 0:
        print("NO RECOMMENDED TOPICS")


if __name__ == "__main__":
    main()
