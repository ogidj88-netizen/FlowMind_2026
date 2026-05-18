from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.state_store import save_state_atomic
from engine.state_validator import compute_manifest_hash

TEMPLATE_PATH = REPO_ROOT / "templates" / "PROJECT_STATE.template.json"
CANONICAL_COMPAT_MODE = "cashflow-mode"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_template() -> dict:
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"Template not found: {TEMPLATE_PATH}")

    try:
        raw = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Template is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise SystemExit("Template root must be a JSON object")

    if not isinstance(raw.get("manifest"), dict):
        raise SystemExit("Template must contain manifest object")

    return raw


def require_non_empty(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise SystemExit(f"{field_name} must be non-empty")
    return normalized


def build_state(
    *,
    project_id: str,
    niche: str,
    audience: str,
    content_language: str,
    primary_platform: str,
    topic: str,
    working_title: str,
    hook: str,
    target_duration_sec: int,
    output_path: Path,
) -> dict:
    project_id = require_non_empty(project_id, "project_id")
    niche = require_non_empty(niche, "niche")
    audience = require_non_empty(audience, "audience")
    content_language = require_non_empty(content_language, "content_language")
    primary_platform = require_non_empty(primary_platform, "primary_platform")
    topic = require_non_empty(topic, "topic")
    working_title = require_non_empty(working_title, "working_title")
    hook = require_non_empty(hook, "hook")

    if target_duration_sec <= 0:
        raise SystemExit("target_duration_sec must be > 0")

    template = copy.deepcopy(load_template())
    now = utc_now_iso()

    template["project_id"] = project_id
    template["updated_at"] = now
    template["phase"] = "TOPIC"
    template["phase_history"] = []
    template["halted"] = False
    template["halt_reason"] = None
    template["resume_hint"] = None
    template["approval_status"] = "PENDING"
    template["approved_for_upload"] = False
    template["qa_passed"] = False
    template["artifacts"] = {}

    manifest = template["manifest"]
    manifest["manifest_id"] = f"{project_id}:v1"
    manifest["manifest_version"] = 1

    # Compatibility label required by the current state_validator.
    # This is not FlowMind Core business identity.
    manifest["mode"] = CANONICAL_COMPAT_MODE

    manifest["niche"] = niche
    manifest["audience"] = audience
    manifest["content_language"] = content_language
    manifest["primary_platform"] = primary_platform
    manifest["topic"] = topic
    manifest["working_title"] = working_title
    manifest["hook"] = hook
    manifest["target_duration_sec"] = target_duration_sec
    manifest["created_at"] = now
    manifest["locked"] = True

    manifest["manifest_hash"] = compute_manifest_hash(manifest)

    save_state_atomic(output_path, template)
    return template


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bootstrap canonical PROJECT_STATE.json")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--niche", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--content-language", required=True)
    parser.add_argument("--primary-platform", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--working-title", required=True)
    parser.add_argument("--hook", required=True)
    parser.add_argument("--target-duration-sec", type=int, default=480)
    parser.add_argument("--output", required=True, help="Path to PROJECT_STATE.json")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    output_path = Path(args.output)
    state = build_state(
        project_id=args.project_id,
        niche=args.niche,
        audience=args.audience,
        content_language=args.content_language,
        primary_platform=args.primary_platform,
        topic=args.topic,
        working_title=args.working_title,
        hook=args.hook,
        target_duration_sec=args.target_duration_sec,
        output_path=output_path,
    )

    manifest = state["manifest"]

    print("BOOTSTRAP_OK")
    print(f"output={output_path}")
    print(f"project_id={state['project_id']}")
    print(f"phase={state['phase']}")
    print(f"manifest_id={manifest['manifest_id']}")
    print(f"manifest_hash={manifest['manifest_hash']}")
    print(f"niche={manifest['niche']}")
    print(f"audience={manifest['audience']}")
    print(f"content_language={manifest['content_language']}")
    print(f"primary_platform={manifest['primary_platform']}")


if __name__ == "__main__":
    main()
