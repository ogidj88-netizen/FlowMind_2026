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
QA_VERSION = "1.0.0"
WORDS_PER_MINUTE = 145.0
ALLOWED_DURATION_DRIFT = 0.20
MIN_PASS_SCORE = 80

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
    paragraphs = [paragraph.strip() for paragraph in script_text.split("\n\n") if paragraph.strip()]
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
    for paragraph in [p.strip() for p in script_text.split("\n\n") if p.strip()]:
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
    structure_ok = check_structure(script_text)
    payoff_ok = check_practical_payoff(script_text)
    voiceover_ok = check_voiceover_usability(script_text)
    fake_fact_ok = check_fake_fact_risk(script_text)

    meta_word_count = script_meta.get("word_count")
    meta_qa_status = script_meta.get("qa_status")
    meta_ok = meta_word_count == word_count and meta_qa_status == "PASS"

    checks = [
        build_check(
            name="duration_fit",
            passed=duration_ok,
            points=15,
            detail=f"word_count={word_count}, allowed_range={min_words}-{max_words}, estimated_minutes={estimated_duration_minutes}",
        ),
        build_check(
            name="hook_alignment",
            passed=hook_ok,
            points=15,
            detail=f"working_title={working_title}",
        ),
        build_check(
            name="topic_match",
            passed=topic_ok,
            points=15,
            detail=f"topic={topic}",
        ),
        build_check(
            name="structure",
            passed=structure_ok,
            points=15,
            detail="requires coherent multi-part narration",
        ),
        build_check(
            name="practical_payoff",
            passed=payoff_ok,
            points=15,
            detail=f"audience={audience}",
        ),
        build_check(
            name="voiceover_usability",
            passed=voiceover_ok,
            points=15,
            detail="requires spoken-narration-friendly script text",
        ),
        build_check(
            name="safety_no_fake_facts",
            passed=fake_fact_ok,
            points=10,
            detail="blocks unsupported precise claims and fake citation patterns",
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
