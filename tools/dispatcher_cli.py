from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.canonical_dispatcher import CanonicalDispatcher, DispatcherTransitionError
from engine.state_validator import StateValidationError


def parse_artifacts_patch(raw: str | None) -> dict | None:
    if not raw:
        return None

    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON for --artifacts-patch: {exc}") from exc

    if not isinstance(value, dict):
        raise SystemExit("--artifacts-patch must decode to JSON object")

    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Canonical dispatcher CLI for FlowMind cashflow-mode"
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Path to PROJECT_STATE.json",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show", help="Load and print current state")

    transition_parser = subparsers.add_parser("transition", help="Run phase transition")
    transition_parser.add_argument("--to", required=True, help="Target phase")
    transition_parser.add_argument("--halt-reason", default=None)
    transition_parser.add_argument("--resume-hint", default=None)
    transition_parser.add_argument(
        "--artifacts-patch",
        default=None,
        help='JSON object, example: {"final_video_path":"/tmp/final.mp4"}',
    )

    halt_parser = subparsers.add_parser("halt", help="Move state into HALT")
    halt_parser.add_argument("--reason", required=True)
    halt_parser.add_argument("--resume-hint", default=None)

    resume_parser = subparsers.add_parser("resume", help="Resume from HALT")
    resume_parser.add_argument("--to", required=True)

    subparsers.add_parser("mark-qa-passed", help="Mark qa_passed=true")
    subparsers.add_parser("approve-upload", help="Mark approved_for_upload=true")

    return parser


def print_state(state: dict) -> None:
    print(json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dispatcher = CanonicalDispatcher(args.state)

    try:
        if args.command == "show":
            result = dispatcher.load()

        elif args.command == "transition":
            result = dispatcher.transition(
                args.to,
                halt_reason=args.halt_reason,
                resume_hint=args.resume_hint,
                artifacts_patch=parse_artifacts_patch(args.artifacts_patch),
            )

        elif args.command == "halt":
            result = dispatcher.halt(
                args.reason,
                resume_hint=args.resume_hint,
            )

        elif args.command == "resume":
            result = dispatcher.resume_from_halt(args.to)

        elif args.command == "mark-qa-passed":
            result = dispatcher.mark_qa_passed()

        elif args.command == "approve-upload":
            result = dispatcher.approve_for_upload()

        else:
            raise SystemExit(f"Unsupported command: {args.command}")

    except (DispatcherTransitionError, StateValidationError) as exc:
        print(f"DISPATCHER_CLI_ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    print_state(result)


if __name__ == "__main__":
    main()
