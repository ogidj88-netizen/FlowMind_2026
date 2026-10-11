from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.final_handoff import FinalHandoffError, validate_final_handoff
from engine.state_validator import load_state
from engine.state_store import state_lock, write_bytes_atomic, recover_artifact_publication

TOOL_NAME = "apply_final_render_readiness"
TOOL_VERSION = "1.1.0"


class ApplyFinalRenderReadinessError(RuntimeError):
    pass


def apply_final_render_readiness(
    state_path: Path,
    assembly_plan_path: Path,
    final_render_report_path: Path,
) -> dict[str, Any]:
    def absolute(path: Path) -> Path:
        return (path if path.is_absolute() else REPO_ROOT / path).resolve()

    state_path = absolute(state_path)
    try:
        with state_lock(state_path):
            recover_artifact_publication(state_path)
            state = load_state(state_path)
            if state["phase"] != "ASSEMBLY":
                raise ApplyFinalRenderReadinessError("readiness requires ASSEMBLY phase")
            packet = validate_final_handoff(state_path, state, require_ready=False)
            if absolute(assembly_plan_path) != packet["assembly_plan_path"]:
                raise ApplyFinalRenderReadinessError("assembly plan argument mismatch")
            if absolute(final_render_report_path) != packet["render_report_path"]:
                raise ApplyFinalRenderReadinessError("final render report argument mismatch")
            plan = packet["assembly_plan"]
            changed = plan["render_ready"] is not True
            if changed:
                now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
                plan.update(
                    render_ready=True, missing_requirements=[], readiness_status="render_ready",
                    source_final_render_report_path=state["artifacts"]["final_render_report_path"],
                    source_final_video_path=state["artifacts"]["final_video_path"],
                    updated_at=now, final_render_readiness_applied_by=TOOL_NAME,
                    final_render_readiness_applied_tool_version=TOOL_VERSION,
                )
                path = packet["assembly_plan_path"]
                original = path.read_bytes()
                write_bytes_atomic(path, (json.dumps(plan, indent=2, ensure_ascii=False,
                                                    sort_keys=True) + "\n").encode())
            # The tool owns assembly readiness only. Canonical state is left byte-identical.
            try:
                validate_final_handoff(state_path, state)
                if load_state(state_path) != state:
                    raise ApplyFinalRenderReadinessError("state changed during readiness")
            except Exception:
                if changed:
                    write_bytes_atomic(path, original)
                raise
            return {
                "status": "APPLY_FINAL_RENDER_READINESS_OK", "project_id": state["project_id"],
                "assembly_plan_path": state["artifacts"]["assembly_plan_path"],
                "final_render_report_path": state["artifacts"]["final_render_report_path"],
                "final_video_path": state["artifacts"]["final_video_path"],
                "render_ready": True, "readiness_status": "render_ready",
                "missing_requirements": [], "changed": changed,
            }
    except (FinalHandoffError, OSError, ValueError) as exc:
        raise ApplyFinalRenderReadinessError(str(exc)) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply FlowMind final render readiness")
    parser.add_argument("--state", required=True)
    parser.add_argument("--assembly-plan", required=True)
    parser.add_argument("--final-render-report", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        result = apply_final_render_readiness(
            Path(args.state), Path(args.assembly_plan), Path(args.final_render_report),
        )
    except ApplyFinalRenderReadinessError as exc:
        print(f"[APPLY_FINAL_RENDER_READINESS][FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
