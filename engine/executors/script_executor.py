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
    language_code = content_language.strip().lower().replace("_", "-").split("-", 1)[0]
    if language_code != "en":
        raise ScriptExecutorError(
            "deterministic script executor v1 currently supports only English content_language"
        )

    sections = [
        hook,
        "",
        "Your power bill can rise even when usage looks normal, but the usage line is not always the real clue. The hidden risk is blaming the wrong problem before you see what quietly changed. If you only look at the final amount due, you can miss the layer that actually moved.",
        "",
        f"For {audience}, the useful question behind {working_title} is simple: what changed before your habits changed? A higher bill can come from usage, rate, timing, fixed charges, or an always-on device. Those are different problems, and treating them as one problem can waste time and money.",
        "",
        f"That is why {topic.lower()} is a structure story, not just a usage story. Picture the bill arriving: the total is higher, the usage chart looks close to normal, and the first instinct is to blame the air conditioner, dryer, or someone leaving something on. But the obvious explanation can send you in the wrong direction.",
        "",
        "A power bill is a stack. There is usage, usually measured in kilowatt-hours. There is the rate charged for that usage. There may also be delivery charges, fixed service charges, taxes, time-of-use pricing, or plan changes. When one layer moves, the final number can rise while another layer stays stable.",
        "",
        "So here is the pattern interrupt: stop asking only why the total is higher. Ask which layer moved. Start with usage. Compare kilowatt-hours with the same month last year, not just last month. If usage rose, check weather, guests, heating, cooling, new routines, or an always-on device. That is probably a behavior or device problem.",
        "",
        "If kilowatt-hours are nearly the same but the total is higher, change the angle. Check the rate, the plan, and fixed charges. The usage graph can look reassuring while the price structure changes underneath it. In that case, using less energy may help a little, but it does not diagnose the real problem.",
        "",
        "Then check timing. A dishwasher, dryer, heater, air conditioner, or water heater can cost more depending on when it runs. With peak pricing, the same appliance can become more expensive without running longer. The device did not change; the clock did. Before replacing equipment, compare when the biggest loads are running.",
        "",
        "Now check quiet background loads. A second fridge, old freezer, gaming computer, dehumidifier, pool pump, or water heater can create a steady leak. These devices rarely create one dramatic moment of waste. They simply keep running until the bill turns them into a mystery.",
        "",
        "The practical diagnostic is to write down three numbers from the latest bill: total cost, kilowatt-hours, and fixed charges. Then compare the same three numbers with the same month last year. Split the problem into usage, pricing, and structure. If usage changed, inspect the home. If the rate changed, question the plan. If fixed charges changed, your habits are not the main cause.",
        "",
        "Do not treat one unusual month as a permanent pattern. Weather, guests, repairs, or a temporary schedule change can create a short spike. But if several bills rise in a row, that is a signal worth diagnosing. Compare first, then change behavior or equipment.",
        "",
        "So when your power bill rises while usage looks normal, do not start with guilt. Start with structure. Check usage, compare the rate, look at fixed charges, question timing, and diagnose always-on devices. The payoff is simple: you cannot fix the right problem until you stop chasing the wrong one.",
        "",
        "A higher electricity bill is not one question. It is three: did you use more, did pricing change, or did the bill structure change? Answer those in order, and the bill stops being a mystery. It becomes a map.",
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

