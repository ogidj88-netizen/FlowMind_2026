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


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_template() -> dict:
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"Template not found: {TEMPLATE_PATH}")

    try:
        return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Template is not valid JSON: {exc}") from exc


def build_state(
    *,
    project_id: str,
    topic: str,
    working_title: str,
    hook: str,
    target_duration_sec: int,
    output_path: Path,
) -> dict:
    if not project_id.strip():
        raise SystemExit("project_id must be non-empty")
    if not topic.strip():
        raise SystemExit("topic must be non-empty")
    if not working_title.strip():
        raise SystemExit("working_title must be non-empty")
    if not hook.strip():
        raise SystemExit("hook must be non-empty")
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
    manifest["mode"] = "cashflow-mode"
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
        topic=args.topic,
        working_title=args.working_title,
        hook=args.hook,
        target_duration_sec=args.target_duration_sec,
        output_path=output_path,
    )

    print("BOOTSTRAP_OK")
    print(f"output={output_path}")
    print(f"project_id={state['project_id']}")
    print(f"phase={state['phase']}")
    print(f"manifest_id={state['manifest']['manifest_id']}")
    print(f"manifest_hash={state['manifest']['manifest_hash']}")


if __name__ == "__main__":
    main()
