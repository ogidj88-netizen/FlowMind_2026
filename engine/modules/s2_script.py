#!/usr/bin/env python3
"""
FlowMind 2026 — Canonical S2 Script Module

Purpose:
- Read canonical project state
- Require topic/title/hook
- Generate script.txt via OpenAI
- Fail closed on invalid inputs or weak output
- Update PROJECT_STATE.json deterministically
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

STATE_FILE = "PROJECT_STATE.json"
MIN_WORDS = 700
MAX_WORDS = 1100
WORDS_PER_MINUTE = 145.0
MAX_ATTEMPTS = 3


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def project_dir(project_id: str) -> Path:
    return Path("projects") / project_id


def state_path(project_id: str) -> Path:
    return project_dir(project_id) / STATE_FILE


def load_state(project_id: str) -> tuple[dict, Path]:
    path = state_path(project_id)
    if not path.exists():
        print(f"[S2][FAIL] PROJECT_STATE.json not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        with path.open("r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception as e:
        print(f"[S2][FAIL] Cannot read PROJECT_STATE.json: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(state, dict):
        print("[S2][FAIL] PROJECT_STATE.json must be an object", file=sys.stderr)
        sys.exit(1)

    return state, path


def save_state(state: dict, path: Path) -> None:
    state["updated_at"] = utc_now_iso()
    with path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def require_non_empty_string(state: dict, key: str) -> str:
    value = state.get(key)

    if value is None:
        print(f"[S2][FAIL] Missing required state field: {key}", file=sys.stderr)
        sys.exit(1)

    value_str = str(value).strip()
    if not value_str:
        print(f"[S2][FAIL] Empty required state field: {key}", file=sys.stderr)
        sys.exit(1)

    return value_str


def count_words(text: str) -> int:
    return len([w for w in text.split() if w.strip()])


def estimate_duration_minutes(word_count: int) -> float:
    if word_count <= 0:
        return 0.0
    return round(word_count / WORDS_PER_MINUTE, 2)


def build_base_prompt(topic: str, title: str, hook: str) -> str:
    return f"""
You are writing a YouTube voice-over script for a cashflow-style video.

Project topic:
{topic}

Working title:
{title}

Required opening hook:
{hook}

Requirements:
- Write in clear conversational American English.
- The final script must naturally land around 5 to 7 minutes when spoken.
- Aim for roughly 750 to 1000 words.
- Short sentences.
- Strong retention.
- No corporate tone.
- No AI self-reference.
- No stage directions.
- No markdown.
- No bullet points.
- No section labels.
- Make the first lines hit hard.
- Keep the script specific to the topic/title/hook above.
- Use concrete consequences, costs, and practical details.
- Make the script feel vivid, practical, and watchable.
- The hook must connect clearly to the body, not feel generic.
- End with a practical takeaway.

Output:
- Return only the final script text.
""".strip()


def build_retry_prompt(topic: str, title: str, hook: str, previous_word_count: int) -> str:
    return f"""
Your previous answer was too short at about {previous_word_count} words.

Rewrite the script completely and make it substantially fuller.

Project topic:
{topic}

Working title:
{title}

Required opening hook:
{hook}

Hard requirements:
- Minimum length: at least {MIN_WORDS} words.
- Target range: 750 to 1000 words.
- Keep it natural and watchable, not bloated.
- Add more concrete examples, consequences, details, and connective tissue.
- Keep the same topic and hook.
- Clear conversational American English.
- Short sentences.
- Strong retention.
- No markdown.
- No bullet points.
- No section labels.
- No AI self-reference.
- Return only the final script text.
""".strip()


def call_openai(messages: list[dict]) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("[S2][FAIL] OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )
    except Exception as e:
        print(f"[S2][FAIL] OpenAI request failed: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        content = response.choices[0].message.content
    except Exception as e:
        print(f"[S2][FAIL] Invalid OpenAI response shape: {e}", file=sys.stderr)
        sys.exit(1)

    if content is None:
        print("[S2][FAIL] OpenAI returned empty content", file=sys.stderr)
        sys.exit(1)

    return str(content).strip()


def generate_script_text(topic: str, title: str, hook: str) -> str:
    system_prompt = (
        "You are a professional YouTube scriptwriter focused on "
        "high-retention financial explainer content."
    )

    last_word_count = 0

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt == 1:
            user_prompt = build_base_prompt(topic=topic, title=title, hook=hook)
        else:
            user_prompt = build_retry_prompt(
                topic=topic,
                title=title,
                hook=hook,
                previous_word_count=last_word_count,
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        script_text = call_openai(messages)
        word_count = count_words(script_text)
        last_word_count = word_count

        print(f"[S2][INFO] attempt={attempt} word_count={word_count}")

        if word_count < MIN_WORDS:
            if attempt < MAX_ATTEMPTS:
                print(
                    f"[S2][WARN] Script too short ({word_count} < {MIN_WORDS}), retrying...",
                    file=sys.stderr,
                )
                continue

            print(
                f"[S2][FAIL] Generated script too short after {MAX_ATTEMPTS} attempts "
                f"({word_count} words < {MIN_WORDS})",
                file=sys.stderr,
            )
            sys.exit(1)

        if word_count > MAX_WORDS:
            if attempt < MAX_ATTEMPTS:
                print(
                    f"[S2][WARN] Script too long ({word_count} > {MAX_WORDS}), retrying...",
                    file=sys.stderr,
                )
                continue

            print(
                f"[S2][FAIL] Generated script too long after {MAX_ATTEMPTS} attempts "
                f"({word_count} words > {MAX_WORDS})",
                file=sys.stderr,
            )
            sys.exit(1)

        return script_text

    print("[S2][FAIL] Unreachable generation state", file=sys.stderr)
    sys.exit(1)


def main(project_id: str) -> None:
    state, path = load_state(project_id)

    topic = require_non_empty_string(state, "topic")
    title = require_non_empty_string(state, "title")
    hook = require_non_empty_string(state, "hook")

    pdir = project_dir(project_id)
    pdir.mkdir(parents=True, exist_ok=True)

    script_text = generate_script_text(topic=topic, title=title, hook=hook)

    script_path = pdir / "script.txt"

    try:
        with script_path.open("w", encoding="utf-8") as f:
            f.write(script_text)
    except Exception as e:
        print(f"[S2][FAIL] Cannot write script.txt: {e}", file=sys.stderr)
        sys.exit(1)

    word_count = count_words(script_text)
    estimated_minutes = estimate_duration_minutes(word_count)

    state["script_generated"] = True
    state["script_path"] = str(script_path)

    state.setdefault("metrics", {})
    if not isinstance(state["metrics"], dict):
        print("[S2][FAIL] metrics must be an object", file=sys.stderr)
        sys.exit(1)

    state["metrics"]["word_count"] = word_count
    state["metrics"]["estimated_duration_minutes"] = estimated_minutes

    if "scene_count" in state["metrics"]:
        state["metrics"]["scene_count"] = None

    save_state(state, path)

    print(f"[S2][OK] Script saved → {script_path}")
    print(f"[S2][INFO] word_count={word_count}")
    print(f"[S2][INFO] estimated_duration_minutes={estimated_minutes}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python engine/modules/s2_script.py <PROJECT_ID>", file=sys.stderr)
        sys.exit(1)

    main(sys.argv[1])
