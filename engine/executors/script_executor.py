from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.state_store import save_state_with_disk_guard
from engine.state_validator import StateValidationError, load_state

EXECUTOR_NAME = "script_executor"
EXECUTOR_VERSION = "1.0.0"
WORDS_PER_MINUTE = 145.0
ALLOWED_DURATION_DRIFT = 0.20
FORBIDDEN_MARKERS = (
    "PLACEHOLDER",
    "STUB",
    "STUBBED",
    "DO_NOT_PUBLISH",
    "TODO",
    "FAKE_OUTPUT",
)


class ScriptExecutorError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ScriptExecutorError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ScriptExecutorError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise ScriptExecutorError(f"{field_name} must be an integer")

    if value <= 0:
        raise ScriptExecutorError(f"{field_name} must be > 0")

    return value


def expected_word_range(target_duration_sec: int) -> tuple[int, int]:
    target_minutes = target_duration_sec / 60.0
    target_words = int(round(target_minutes * WORDS_PER_MINUTE))
    min_words = int(round(target_words * (1.0 - ALLOWED_DURATION_DRIFT)))
    max_words = int(round(target_words * (1.0 + ALLOWED_DURATION_DRIFT)))
    return min_words, max_words


def validate_script_text(script: str, target_duration_sec: int) -> tuple[int, float, str]:
    text = script.strip()
    if not text:
        raise ScriptExecutorError("script output is empty")

    upper_text = text.upper()
    for marker in FORBIDDEN_MARKERS:
        if marker in upper_text:
            raise ScriptExecutorError(f"script contains forbidden marker: {marker}")

    word_count = count_words(text)
    min_words, max_words = expected_word_range(target_duration_sec)

    qa_status = "PASS"
    if word_count < min_words or word_count > max_words:
        qa_status = "WARN_DURATION_RANGE"

    estimated_duration_minutes = round(word_count / WORDS_PER_MINUTE, 2)
    return word_count, estimated_duration_minutes, qa_status


def build_script(
    *,
    topic: str,
    working_title: str,
    hook: str,
    niche: str,
    audience: str,
    content_language: str,
    target_duration_sec: int,
) -> str:
    if content_language.lower() != "en":
        raise ScriptExecutorError(
            "deterministic script executor v1 currently supports only content_language='en'"
        )

    sections = [
        hook,
        "",
        f"This is a story about {topic.lower()}. It sounds simple, but it is the kind of money leak that hides inside normal life. For {audience}, the problem is not always that they use too much. The problem is that the bill can change before the behavior looks different.",
        "",
        f"The working title is simple: {working_title}. The reason it matters is that people usually look for one obvious explanation. They blame one appliance, one hot week, one mistake, or one bad habit. But in the {niche} space, the real cost often comes from a stack of small changes that are easy to miss.",
        "",
        "First, there is the rate structure. A household can use the same amount of electricity and still pay more if the price per unit changes, if peak-hour pricing applies, or if fixed charges increase. That means the number at the bottom of the bill can rise even when the usage chart looks harmless.",
        "",
        "Second, there is timing. Many people compare this month to last month and assume that is enough. It is not. A better comparison is this month against the same month last year, because weather, daylight, heating, cooling, and family routines can shift in predictable seasonal patterns. Without that comparison, a normal seasonal change can look like a mystery.",
        "",
        "Third, there are silent load changes. A refrigerator that works harder, an old water heater, a computer that stays on, a dehumidifier, a space heater, or small devices left running all day can create a slow rise. None of these feel dramatic in the moment. That is why they are easy to ignore.",
        "",
        "Fourth, there are billing details most people skip. Delivery charges, service fees, taxes, minimum charges, and plan changes can move the total even when the usage line looks stable. If someone only checks the total amount due, they miss the difference between using more power and being charged differently for the same power.",
        "",
        "The practical move is to split the bill into three parts: usage, rate, and fixed charges. If usage went up, the question is what changed inside the home. If the rate went up, the question is whether the plan, time-of-use window, or provider pricing changed. If fixed charges went up, the issue is not behavior at all. It is the structure of the bill.",
        "",
        "A simple check can save a lot of confusion. Look at kilowatt-hours, not just dollars. Compare the same month last year. Check whether peak pricing applies. Look for new fees. Then list anything in the home that runs for long periods without attention. This turns a vague money problem into a clear investigation.",
        "",
        "Here is a simple way to diagnose it. Take the latest bill and write down three numbers: total cost, kilowatt-hours, and fixed charges. Then take the same month from last year and write down the same three numbers. Do not start with the total cost. Start with kilowatt-hours. If kilowatt-hours are nearly the same but the total is higher, the problem is probably not your behavior. It is pricing, fees, or the structure of the plan.",
        "",
        "Then check the rate. Some bills show the cost per kilowatt-hour clearly. Others hide it across multiple lines. If the rate changed, your usage can look normal while the final bill moves up. This is why many people feel confused. They are looking at the usage chart, but the cost moved somewhere else.",
        "",
        "After that, look at time-of-use pricing. If your plan charges more during peak hours, the same appliance can cost more depending on when it runs. A dishwasher, dryer, air conditioner, or heater can become more expensive without being used more often. The question becomes not only what you use, but when you use it.",
        "",
        "Next, check for always-on devices. The expensive problem is not always a dramatic one. It can be a device that runs quietly every day. A second fridge in the garage, an old freezer, a gaming computer, a pool pump, a dehumidifier, or a water heater can create a background cost that nobody notices until the bill arrives.",
        "",
        "You also want to separate one-time events from repeat patterns. If the bill jumped once, it may be weather, guests, repairs, or a temporary change. If it rises for three months in a row, that is a pattern. A pattern deserves investigation. This is where many households lose money: they treat a pattern like a random bad month.",
        "",
        "The fastest useful experiment is a seven-day reset. Pick one week and reduce the biggest invisible loads. Run laundry outside peak hours if your plan uses peak pricing. Turn off devices that stay on all day. Check thermostat schedules. Then compare daily usage if your provider gives that data. You are not trying to solve everything. You are trying to identify which category moves.",
        "",
        "If nothing changes, the issue may be outside your behavior. That is when it makes sense to call the provider, ask whether the rate plan changed, ask about fixed charges, and compare available plans. Many people skip this because they assume the bill is purely a usage problem. Sometimes it is a contract problem.",
        "",
        "The point is not to panic over every bill. The point is to stop treating the final number as the whole story. A higher electricity bill is not one question. It is three questions: did you use more, did the price change, or did the bill structure change?",
        "",
        "Once you separate those three, the problem becomes easier to act on. You can reduce usage, change timing, question the provider, adjust the plan, or replace the device that is quietly wasting power. But you cannot fix what you have not separated.",
        "",
        "So if your power bill rises even when usage looks normal, do not start with guilt. Start with the structure. The bill may be telling you that the rules changed before your habits did.",
    ]

    return "\n".join(sections).strip() + "\n"


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(path)


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    write_text_atomic(path, serialized)


def run_script_executor(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "SCRIPT":
        raise ScriptExecutorError("SCRIPT executor may run only when phase is SCRIPT")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]

    niche = require_non_empty_string(manifest.get("niche"), "manifest.niche")
    audience = require_non_empty_string(manifest.get("audience"), "manifest.audience")
    content_language = require_non_empty_string(
        manifest.get("content_language"),
        "manifest.content_language",
    )
    primary_platform = require_non_empty_string(
        manifest.get("primary_platform"),
        "manifest.primary_platform",
    )
    topic = require_non_empty_string(manifest.get("topic"), "manifest.topic")
    working_title = require_non_empty_string(
        manifest.get("working_title"),
        "manifest.working_title",
    )
    hook = require_non_empty_string(manifest.get("hook"), "manifest.hook")
    target_duration_sec = require_positive_int(
        manifest.get("target_duration_sec"),
        "manifest.target_duration_sec",
    )

    project_dir = state_path.parent
    script_dir = project_dir / "script"
    script_path = script_dir / "script.txt"
    script_meta_path = script_dir / "script_meta.json"

    script_text = build_script(
        topic=topic,
        working_title=working_title,
        hook=hook,
        niche=niche,
        audience=audience,
        content_language=content_language,
        target_duration_sec=target_duration_sec,
    )

    word_count, estimated_duration_minutes, qa_status = validate_script_text(
        script_text,
        target_duration_sec,
    )

    now = utc_now_iso()
    script_meta = {
        "project_id": project_id,
        "executor": EXECUTOR_NAME,
        "executor_version": EXECUTOR_VERSION,
        "source_phase": state["phase"],
        "topic": topic,
        "working_title": working_title,
        "niche": niche,
        "audience": audience,
        "content_language": content_language,
        "primary_platform": primary_platform,
        "target_duration_sec": target_duration_sec,
        "word_count": word_count,
        "estimated_duration_minutes": estimated_duration_minutes,
        "created_at": now,
        "status": "SCRIPT_EXECUTOR_OK",
        "script_path": str(script_path),
        "script_meta_path": str(script_meta_path),
        "qa_status": qa_status,
    }

    write_text_atomic(script_path, script_text)
    write_json_atomic(script_meta_path, script_meta)

    candidate_state = dict(state)
    artifacts = dict(candidate_state.get("artifacts", {}))
    artifacts["script_path"] = str(script_path)
    artifacts["script_meta_path"] = str(script_meta_path)
    candidate_state["artifacts"] = artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "SCRIPT_EXECUTOR_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "script_path": str(script_path),
        "script_meta_path": str(script_meta_path),
        "word_count": word_count,
        "estimated_duration_minutes": estimated_duration_minutes,
        "qa_status": qa_status,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind canonical SCRIPT executor v1")
    parser.add_argument(
        "--state",
        required=True,
        help="Path to canonical PROJECT_STATE.json",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = run_script_executor(Path(args.state))
    except (ScriptExecutorError, StateValidationError, OSError) as exc:
        print(f"[SCRIPT_EXECUTOR][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
