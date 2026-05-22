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

QA_GATE_NAME = "script_qa"
QA_VERSION = "1.1.0"
WORDS_PER_MINUTE = 145.0
ALLOWED_DURATION_DRIFT = 0.20
MIN_PASS_SCORE = 85

FORBIDDEN_MARKERS = (
    "PLACEHOLDER",
    "STUB",
    "STUBBED",
    "DO_NOT_PUBLISH",
    "TODO",
    "FAKE_OUTPUT",
    "LOREM IPSUM",
    "TEST ONLY",
    "DUMMY",
    "MOCK",
)


class ScriptQAError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ScriptQAError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ScriptQAError(f"{field_name} must be non-empty")

    return normalized


def require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise ScriptQAError(f"{field_name} must be an integer")

    if value <= 0:
        raise ScriptQAError(f"{field_name} must be > 0")

    return value


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ScriptQAError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ScriptQAError(f"Invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise ScriptQAError(f"JSON file must contain an object: {path}")

    return payload


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ScriptQAError(f"Text file not found: {path}") from exc


def expected_word_range(target_duration_sec: int) -> tuple[int, int]:
    target_minutes = target_duration_sec / 60.0
    target_words = int(round(target_minutes * WORDS_PER_MINUTE))
    min_words = int(round(target_words * (1.0 - ALLOWED_DURATION_DRIFT)))
    max_words = int(round(target_words * (1.0 + ALLOWED_DURATION_DRIFT)))
    return min_words, max_words


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(path)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def get_paragraphs(script_text: str) -> list[str]:
    return [paragraph.strip() for paragraph in script_text.split("\n\n") if paragraph.strip()]


def first_words(script_text: str, word_limit: int) -> str:
    words = re.findall(r"\b[\w'-]+\b", script_text)
    return " ".join(words[:word_limit])


def has_forbidden_marker(script_text: str) -> list[str]:
    upper_text = script_text.upper()
    return [marker for marker in FORBIDDEN_MARKERS if marker in upper_text]


def check_duration(script_text: str, target_duration_sec: int) -> tuple[bool, int, int, int, float]:
    word_count = count_words(script_text)
    min_words, max_words = expected_word_range(target_duration_sec)
    estimated_duration_minutes = round(word_count / WORDS_PER_MINUTE, 2)
    return min_words <= word_count <= max_words, word_count, min_words, max_words, estimated_duration_minutes


def check_hook_alignment(script_text: str, hook: str) -> bool:
    normalized_script = normalize_text(script_text)
    normalized_hook = normalize_text(hook)

    if not normalized_script or not normalized_hook:
        return False

    first_400_chars = normalized_script[:400]
    hook_words = [word for word in re.findall(r"\b[a-z0-9']+\b", normalized_hook) if len(word) >= 4]

    if normalized_hook in first_400_chars:
        return True

    if not hook_words:
        return False

    hits = sum(1 for word in hook_words if word in first_400_chars)
    return hits >= max(2, len(hook_words) // 2)


def check_topic_match(script_text: str, topic: str) -> bool:
    normalized_script = normalize_text(script_text)
    topic_words = [
        word
        for word in re.findall(r"\b[a-z0-9']+\b", normalize_text(topic))
        if len(word) >= 5
    ]

    if not topic_words:
        return False

    hits = sum(1 for word in topic_words if word in normalized_script)
    return hits >= max(2, len(topic_words) // 3)


def check_niche_match(script_text: str, niche: str) -> bool:
    normalized_script = normalize_text(script_text)
    normalized_niche = normalize_text(niche)

    if "money mistakes" in normalized_niche or "invisible costs" in normalized_niche:
        required_concepts = (
            "cost",
            "bill",
            "usage",
            "rate",
            "charge",
        )
        hits = sum(1 for concept in required_concepts if concept in normalized_script)
        return hits >= 3

    niche_words = [
        word
        for word in re.findall(r"\b[a-z0-9']+\b", normalized_niche)
        if len(word) >= 5
    ]
    if not niche_words:
        return False

    hits = sum(1 for word in niche_words if word in normalized_script)
    return hits >= max(1, len(niche_words) // 3)


def check_structure(script_text: str) -> bool:
    paragraphs = get_paragraphs(script_text)
    if len(paragraphs) < 8:
        return False

    normalized_script = normalize_text(script_text)
    structure_terms = (
        "first",
        "second",
        "third",
        "practical",
        "point",
        "so if",
    )
    hits = sum(1 for term in structure_terms if term in normalized_script)
    return hits >= 4


def check_practical_payoff(script_text: str) -> bool:
    normalized_script = normalize_text(script_text)
    payoff_terms = (
        "check",
        "compare",
        "write down",
        "split",
        "look at",
        "reduce",
        "question",
        "adjust",
    )
    hits = sum(1 for term in payoff_terms if term in normalized_script)
    return hits >= 4


def check_voiceover_usability(script_text: str) -> bool:
    lines = [line.strip() for line in script_text.splitlines() if line.strip()]
    if not lines:
        return False

    bullet_like_lines = sum(1 for line in lines if line.startswith(("-", "*", "1.", "2.", "3.")))
    if bullet_like_lines > 2:
        return False

    if "{" in script_text or "}" in script_text:
        return False

    if "```" in script_text:
        return False

    repeated_paragraphs = set()
    for paragraph in get_paragraphs(script_text):
        key = normalize_text(paragraph)
        if key in repeated_paragraphs:
            return False
        repeated_paragraphs.add(key)

    average_sentence_length = count_words(script_text) / max(1, len(re.findall(r"[.!?]", script_text)))
    return 8 <= average_sentence_length <= 35


def check_fake_fact_risk(script_text: str) -> bool:
    risky_patterns = (
        r"\b\d+(\.\d+)?%\b",
        r"\bstudy shows\b",
        r"\bresearch proves\b",
        r"\bexperts say\b",
        r"\baccording to\b",
        r"\blegal requirement\b",
        r"\bfederal law\b",
        r"\bguaranteed\b",
    )

    normalized_script = normalize_text(script_text)
    for pattern in risky_patterns:
        if re.search(pattern, normalized_script):
            return False

    return True


def check_first_30_seconds_hook_pressure(script_text: str) -> bool:
    opening = normalize_text(first_words(script_text, 90))

    if not opening:
        return False

    weak_openings = (
        "this video is about",
        "today we will discuss",
        "today we're going to discuss",
        "it is important to understand",
        "the working title is",
        "here is an overview",
        "in this video",
    )
    if any(phrase in opening for phrase in weak_openings):
        return False

    pressure_terms = (
        "hidden",
        "risk",
        "wrong",
        "mistake",
        "quietly",
        "leak",
        "before",
        "but",
        "not",
        "rise",
        "rises",
        "cost",
        "bill",
        "missing",
        "problem",
        "changed",
        "changes",
        "normal",
        "already",
    )
    hits = sum(1 for term in pressure_terms if term in opening)

    has_contradiction = bool(re.search(r"\b(but|not|before|even when|instead|looks normal)\b", opening))
    has_personal_cost = bool(re.search(r"\b(your|you|household|bill|cost|money)\b", opening))

    return hits >= 3 and (has_contradiction or has_personal_cost)


def check_retention_loop(script_text: str) -> bool:
    normalized_script = normalize_text(script_text)
    words = re.findall(r"\b[\w'-]+\b", normalized_script)

    if len(words) < 120:
        return False

    early = " ".join(words[: max(80, len(words) // 3)])
    later = " ".join(words[len(words) // 3 :])

    loop_terms = (
        "but",
        "not always",
        "the real",
        "before",
        "wrong",
        "mystery",
        "hidden",
        "question",
        "clue",
        "missing",
        "instead",
        "looks normal",
    )
    resolution_terms = (
        "the point",
        "once you",
        "so if",
        "this means",
        "the answer",
        "separate",
        "check",
        "diagnose",
        "turns",
        "becomes",
    )

    early_hits = sum(1 for term in loop_terms if term in early)
    later_hits = sum(1 for term in resolution_terms if term in later)

    return early_hits >= 2 and later_hits >= 2


def check_curiosity_gap(script_text: str) -> bool:
    normalized_script = normalize_text(script_text)
    words = re.findall(r"\b[\w'-]+\b", normalized_script)

    if len(words) < 120:
        return False

    early = " ".join(words[: max(90, len(words) // 3)])
    later = " ".join(words[len(words) // 3 :])

    banned_fake_mystery = (
        "you will not believe",
        "this secret will change everything",
        "experts do not want you to know",
        "one weird trick",
    )
    if any(phrase in normalized_script for phrase in banned_fake_mystery):
        return False

    curiosity_terms = (
        "not the real clue",
        "not always",
        "wrong part",
        "before changing",
        "the real clue",
        "the obvious explanation",
        "but",
        "before",
        "mystery",
        "hidden",
        "missing",
        "why",
    )
    payoff_terms = (
        "separate",
        "split",
        "check",
        "compare",
        "diagnose",
        "payoff",
        "the point",
        "so if",
    )

    early_hits = sum(1 for term in curiosity_terms if term in early)
    later_hits = sum(1 for term in payoff_terms if term in later)

    return early_hits >= 2 and later_hits >= 2


def classify_paragraph(paragraph: str) -> str:
    normalized = normalize_text(paragraph)

    if any(term in normalized for term in ("your bill", "hidden", "quietly", "before", "mistake")):
        return "hook"

    if any(term in normalized for term in ("problem", "blame", "mystery", "confusion", "rises")):
        return "problem"

    if any(term in normalized for term in ("rate", "structure", "pricing", "fixed charges", "time-of-use", "usage")):
        return "mechanism"

    if any(term in normalized for term in ("refrigerator", "water heater", "dishwasher", "dryer", "computer", "dehumidifier", "appliance")):
        return "example"

    if any(term in normalized for term in ("check", "compare", "write down", "list", "diagnose", "seven-day")):
        return "diagnostic"

    if any(term in normalized for term in ("the point", "once you", "so if", "you can", "start with")):
        return "payoff"

    return "explanation"


def check_scene_beat_readiness(script_text: str) -> bool:
    paragraphs = get_paragraphs(script_text)
    if len(paragraphs) < 7:
        return False

    beat_types = {classify_paragraph(paragraph) for paragraph in paragraphs}

    required_any = (
        "hook",
        "problem",
        "mechanism",
        "diagnostic",
        "payoff",
    )
    required_hits = sum(1 for beat in required_any if beat in beat_types)

    return required_hits >= 4 and len(beat_types) >= 5


def check_pattern_interrupt(script_text: str) -> bool:
    paragraphs = get_paragraphs(script_text)
    if len(paragraphs) < 7:
        return False

    beat_sequence = [classify_paragraph(paragraph) for paragraph in paragraphs]
    unique_beats = set(beat_sequence)
    transitions = sum(
        1
        for index in range(1, len(beat_sequence))
        if beat_sequence[index] != beat_sequence[index - 1]
    )

    return len(unique_beats) >= 5 and transitions >= 4


def check_no_article_mode(script_text: str) -> bool:
    normalized_script = normalize_text(script_text)
    paragraphs = get_paragraphs(script_text)

    ordinal_terms = ("first", "second", "third", "fourth")
    ordinal_hits = sum(1 for term in ordinal_terms if re.search(rf"\b{term}\b", normalized_script))

    hard_article_markers = (
        "the working title is",
        "this article",
        "in this essay",
        "in conclusion",
    )
    if any(marker in normalized_script for marker in hard_article_markers):
        return False

    if ordinal_hits >= 3:
        has_reversal = bool(re.search(r"\b(but|instead|not always|the real clue|wrong|before)\b", normalized_script))
        has_scene_variety = check_scene_beat_readiness(script_text)
        if not has_reversal or not has_scene_variety:
            return False

    if len(paragraphs) >= 10:
        paragraph_types = [classify_paragraph(paragraph) for paragraph in paragraphs]
        explanation_ratio = paragraph_types.count("explanation") / len(paragraph_types)
        if explanation_ratio > 0.55:
            return False

    has_direct_consequence = bool(re.search(r"\b(your bill|your cost|you pay|you miss|your money|your usage)\b", normalized_script))
    has_delayed_payoff = check_retention_loop(script_text) and check_payoff_strength(script_text)

    return has_direct_consequence and has_delayed_payoff


def check_payoff_strength(script_text: str) -> bool:
    normalized_script = normalize_text(script_text)
    words = re.findall(r"\b[\w'-]+\b", normalized_script)

    if len(words) < 100:
        return False

    ending = " ".join(words[int(len(words) * 0.70) :])

    general_payoff_terms = (
        "separate",
        "check",
        "compare",
        "diagnose",
        "start with",
        "what changed",
        "what should",
        "false assumption",
        "understanding",
    )
    money_cost_terms = (
        "behavior",
        "pricing",
        "rate",
        "structure",
        "usage",
        "fixed charges",
        "bill-structure",
        "bill structure",
    )

    general_hits = sum(1 for term in general_payoff_terms if term in ending)
    money_hits = sum(1 for term in money_cost_terms if term in ending)

    return general_hits >= 2 and money_hits >= 2


def build_check(
    *,
    name: str,
    passed: bool,
    points: int,
    detail: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "passed": passed,
        "points": points if passed else 0,
        "max_points": points,
        "detail": detail,
    }


def evaluate_script(
    *,
    script_text: str,
    script_meta: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    topic = require_non_empty_string(manifest.get("topic"), "manifest.topic")
    working_title = require_non_empty_string(manifest.get("working_title"), "manifest.working_title")
    hook = require_non_empty_string(manifest.get("hook"), "manifest.hook")
    niche = require_non_empty_string(manifest.get("niche"), "manifest.niche")
    audience = require_non_empty_string(manifest.get("audience"), "manifest.audience")
    content_language = require_non_empty_string(
        manifest.get("content_language"),
        "manifest.content_language",
    )
    target_duration_sec = require_positive_int(
        manifest.get("target_duration_sec"),
        "manifest.target_duration_sec",
    )

    if content_language.lower() != "en":
        raise ScriptQAError("deterministic SCRIPT QA v1 currently supports only content_language='en'")

    forbidden_hits = has_forbidden_marker(script_text)
    duration_ok, word_count, min_words, max_words, estimated_duration_minutes = check_duration(
        script_text,
        target_duration_sec,
    )

    hook_ok = check_hook_alignment(script_text, hook)
    topic_ok = check_topic_match(script_text, topic)
    niche_ok = check_niche_match(script_text, niche)
    payoff_ok = check_practical_payoff(script_text)
    voiceover_ok = check_voiceover_usability(script_text)
    fake_fact_ok = check_fake_fact_risk(script_text)
    hook_pressure_ok = check_first_30_seconds_hook_pressure(script_text)
    retention_loop_ok = check_retention_loop(script_text)
    article_mode_ok = check_no_article_mode(script_text)
    scene_beat_ok = check_scene_beat_readiness(script_text)
    curiosity_gap_ok = check_curiosity_gap(script_text)
    pattern_interrupt_ok = check_pattern_interrupt(script_text)
    payoff_strength_ok = check_payoff_strength(script_text)

    meta_word_count = script_meta.get("word_count")
    meta_qa_status = script_meta.get("qa_status")
    meta_ok = meta_word_count == word_count and meta_qa_status == "PASS"

    checks = [
        build_check(
            name="duration_fit",
            passed=duration_ok,
            points=10,
            detail=f"word_count={word_count}, allowed_range={min_words}-{max_words}, estimated_minutes={estimated_duration_minutes}",
        ),
        build_check(
            name="hook_alignment",
            passed=hook_ok,
            points=10,
            detail=f"working_title={working_title}",
        ),
        build_check(
            name="topic_match",
            passed=topic_ok,
            points=10,
            detail=f"topic={topic}",
        ),
        build_check(
            name="niche_match",
            passed=niche_ok,
            points=10,
            detail=f"niche={niche}",
        ),
        build_check(
            name="practical_payoff",
            passed=payoff_ok,
            points=10,
            detail=f"audience={audience}",
        ),
        build_check(
            name="voiceover_usability",
            passed=voiceover_ok,
            points=10,
            detail="requires spoken-narration-friendly script text",
        ),
        build_check(
            name="safety_no_fake_facts",
            passed=fake_fact_ok,
            points=10,
            detail="blocks unsupported precise claims and fake citation patterns",
        ),
        build_check(
            name="first_30_seconds_hook_pressure",
            passed=hook_pressure_ok,
            points=10,
            detail="opening must create urgency, contradiction, risk, curiosity, or personal consequence",
        ),
        build_check(
            name="retention_loop",
            passed=retention_loop_ok,
            points=10,
            detail="requires an early unresolved tension and later resolution",
        ),
        build_check(
            name="scene_beat_readiness",
            passed=scene_beat_ok,
            points=5,
            detail="requires distinct narration beats that can become scenes",
        ),
        build_check(
            name="pattern_interrupt",
            passed=pattern_interrupt_ok,
            points=5,
            detail="requires shifts in paragraph function to avoid flat pacing",
        ),
        build_check(
            name="no_article_mode",
            passed=article_mode_ok,
            points=0,
            detail="fails flat essay/blog-post pacing",
        ),
        build_check(
            name="curiosity_gap",
            passed=curiosity_gap_ok,
            points=0,
            detail="requires relevant unresolved curiosity before practical payoff",
        ),
        build_check(
            name="payoff_strength",
            passed=payoff_strength_ok,
            points=0,
            detail="ending must deliver clear cognitive or practical payoff",
        ),
    ]

    score = sum(int(check["points"]) for check in checks)
    failure_reasons: list[str] = []
    warnings: list[str] = []

    if not script_text.strip():
        failure_reasons.append("script is empty")

    if forbidden_hits:
        failure_reasons.append(f"forbidden markers found: {', '.join(forbidden_hits)}")

    if not meta_ok:
        warnings.append(
            f"script_meta mismatch or non-PASS qa_status: meta_word_count={meta_word_count}, actual_word_count={word_count}, meta_qa_status={meta_qa_status}"
        )

    for check in checks:
        if not check["passed"]:
            failure_reasons.append(str(check["name"]))

    verdict = "PASS"
    if failure_reasons or score < MIN_PASS_SCORE:
        verdict = "FAIL"

    return {
        "verdict": verdict,
        "score": score,
        "checks": checks,
        "failure_reasons": failure_reasons,
        "warnings": warnings,
        "word_count": word_count,
        "estimated_duration_minutes": estimated_duration_minutes,
    }


def run_script_qa(state_path: Path) -> dict[str, Any]:
    state = load_state(state_path)

    if state["phase"] != "SCRIPT":
        raise ScriptQAError("SCRIPT QA may run only when phase is SCRIPT")

    project_id = require_non_empty_string(state["project_id"], "project_id")
    manifest = state["manifest"]
    artifacts = state.get("artifacts", {})

    if not isinstance(artifacts, dict):
        raise ScriptQAError("artifacts must be an object")

    script_path_value = require_non_empty_string(
        artifacts.get("script_path"),
        "artifacts.script_path",
    )
    script_meta_path_value = require_non_empty_string(
        artifacts.get("script_meta_path"),
        "artifacts.script_meta_path",
    )

    script_path = Path(script_path_value)
    script_meta_path = Path(script_meta_path_value)

    script_text = read_text_file(script_path)
    script_meta = read_json_file(script_meta_path)

    qa_result = evaluate_script(
        script_text=script_text,
        script_meta=script_meta,
        manifest=manifest,
    )

    now = utc_now_iso()
    script_qa_path = state_path.parent / "script" / "script_qa.json"

    script_qa = {
        "project_id": project_id,
        "qa_gate": QA_GATE_NAME,
        "qa_version": QA_VERSION,
        "source_phase": state["phase"],
        "script_path": str(script_path),
        "script_meta_path": str(script_meta_path),
        "verdict": qa_result["verdict"],
        "score": qa_result["score"],
        "checks": qa_result["checks"],
        "failure_reasons": qa_result["failure_reasons"],
        "warnings": qa_result["warnings"],
        "word_count": qa_result["word_count"],
        "estimated_duration_minutes": qa_result["estimated_duration_minutes"],
        "created_at": now,
    }

    write_json_atomic(script_qa_path, script_qa)

    candidate_state = dict(state)
    candidate_artifacts = dict(candidate_state.get("artifacts", {}))
    candidate_artifacts["script_qa_path"] = str(script_qa_path)
    candidate_state["artifacts"] = candidate_artifacts
    candidate_state["updated_at"] = now

    saved_state = save_state_with_disk_guard(state_path, candidate_state)

    return {
        "status": "SCRIPT_QA_OK",
        "project_id": project_id,
        "phase": saved_state["phase"],
        "script_qa_path": str(script_qa_path),
        "verdict": script_qa["verdict"],
        "score": script_qa["score"],
        "failure_reasons": script_qa["failure_reasons"],
        "warnings": script_qa["warnings"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowMind canonical SCRIPT QA gate v1")
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
        result = run_script_qa(Path(args.state))
    except (ScriptQAError, StateValidationError, OSError) as exc:
        print(f"[SCRIPT_QA][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))

    if result["verdict"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
