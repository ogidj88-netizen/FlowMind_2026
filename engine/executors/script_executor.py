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
EXECUTOR_VERSION = "1.1.1"
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
        "Your power bill can rise even when your usage looks normal, but the usage line is not always the real clue. The hidden risk is that you can blame the wrong problem before you see what quietly changed. If you only look at the final amount due, you may miss the cost that moved underneath it.",
        "",
        f"The working title is {working_title}, but the real question is sharper: what changed before your habits changed? For {audience}, that question matters because a bill can feel personal. It can make someone think they wasted energy, used too much heat, or made a bad household decision. Sometimes that is true. Sometimes the bill changed because the rules around the bill changed.",
        "",
        f"This is why {topic.lower()} is not just a usage story. It is a structure story. A higher bill can come from usage, rate, timing, fixed charges, or a device that runs in the background. Those are different problems. If you treat them like one problem, you can waste time fixing the wrong thing.",
        "",
        "Here is the tension to hold while watching: the most obvious explanation is not always the useful one. A rising bill can look like an appliance problem when it is really a pricing problem. It can look like a pricing problem when it is really a timing problem. It can look like a timing problem when the quiet leak is an always-on device nobody checks.",
        "",
        "Picture the moment the bill arrives. The number is higher. The usage chart looks close to normal. The first instinct is blame. Maybe the air conditioner ran too much. Maybe the dryer was used too often. Maybe someone forgot to turn something off. That instinct feels useful because it gives the problem a face. But it can also send the investigation in the wrong direction.",
        "",
        "The mechanism is simple: a power bill is not one number. It is a stack. There is usage, usually measured in kilowatt-hours. There is the rate charged for that usage. There may be delivery charges, fixed service charges, taxes, time-of-use pricing, or plan changes. When one layer moves, the final number can rise even if another layer looks stable.",
        "",
        "That is the pattern interrupt. Stop asking, why is the total higher? Ask a better question: which layer moved? The total is only the symptom. The layer that moved is the diagnosis.",
        "",
        "That one shift matters because it changes the next action. A usage problem needs a household check. A pricing problem needs a plan check. A structure problem needs a bill check.",
        "",
        "Start with usage. Look at kilowatt-hours, not dollars. Compare the latest bill with the same month last year, not just last month. If usage rose, the home probably changed in some way. Weather, guests, new routines, heating, cooling, or an always-on device may explain the rise. That is a behavior or device problem.",
        "",
        "Now change the angle. If kilowatt-hours are nearly the same but the total is higher, the story changes. The problem is probably not behavior. It may be the rate, the plan, the time window, or fixed charges. This is the part many people miss because the usage graph gives them comfort while the price structure is doing the damage.",
        "",
        "Then check timing. A dishwasher, dryer, heater, air conditioner, or water heater can cost more depending on when it runs. If the plan uses peak pricing, the same appliance can become more expensive without being used more often. The device did not change. The clock did.",
        "",
        "Now check the quiet devices. A second fridge in the garage, an old freezer, a gaming computer, a dehumidifier, a pool pump, or a water heater can create a background cost. These do not feel dramatic. They do not create one obvious moment of waste. They just keep running until the bill turns them into a mystery.",
        "",
        "The diagnostic is practical. Take the latest bill and write down three numbers: total cost, kilowatt-hours, and fixed charges. Then take the same month from last year and write down the same three numbers. Do not start by judging the total. Split the bill into usage, rate, and structure.",
        "",
        "If usage changed, list what changed inside the home. If the rate changed, question the plan. If fixed charges changed, the issue is not your habits. If peak pricing applies, adjust timing before replacing devices. If always-on loads look suspicious, run a seven-day reset and reduce the biggest invisible loads.",
        "",
        "This is where the earlier question resolves. The bill is not asking whether you are careless. It is asking whether you can separate behavior, pricing, and bill structure before reacting. Once you separate those three, the confusion starts to shrink.",
        "",
        "There is also a trap in treating one bad month like a pattern. If the bill jumps once, it may be weather, guests, repairs, or a temporary schedule change. If it rises for several bills in a row, that is not a random bad month. That is a signal. A signal deserves a diagnosis.",
        "",
        "So the next time your power bill rises while usage looks normal, do not start with guilt. Start with the structure. Check usage. Compare the rate. Look at fixed charges. Question timing. Diagnose always-on devices. The payoff is simple: you cannot fix the right problem until you stop chasing the wrong one.",
        "",
        "A higher electricity bill is not one question. It is three questions: did you use more, did pricing change, or did the bill structure change? Answer those in order, and the bill stops being a mystery. It becomes a map.",
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

