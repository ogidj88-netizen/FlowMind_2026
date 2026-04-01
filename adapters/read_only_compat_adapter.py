#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.state_validator import load_state  # noqa: E402

ADAPTER_VERSION = "v1"

REQUIRED_PAYLOAD_FIELDS = (
    "adapter_version",
    "project_id",
    "phase",
    "halted",
    "approval_status",
    "approved_for_upload",
    "mode",
    "updated_at",
)


class AdapterError(Exception):
    pass


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fd: int | None = None
    temp_path: Path | None = None

    try:
        fd, temp_name = tempfile.mkstemp(
            prefix=f"{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            text=True,
        )
        temp_path = Path(temp_name)

        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            fd = None
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temp_path, path)

    except Exception:
        if fd is not None:
            os.close(fd)
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise


def _validate_payload(payload: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_PAYLOAD_FIELDS if field not in payload]
    if missing:
        raise AdapterError(
            f"compat payload missing required fields: {', '.join(missing)}"
        )

    if payload["adapter_version"] != ADAPTER_VERSION:
        raise AdapterError(
            f"unsupported adapter_version '{payload['adapter_version']}'"
        )

    string_fields = ("project_id", "phase", "approval_status", "mode", "updated_at")
    for field in string_fields:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise AdapterError(f"{field} must be a non-empty string")

    bool_fields = ("halted", "approved_for_upload")
    for field in bool_fields:
        value = payload.get(field)
        if not isinstance(value, bool):
            raise AdapterError(f"{field} must be boolean")

    if "halt_reason" in payload and not isinstance(payload["halt_reason"], str):
        raise AdapterError("halt_reason must be string when present")


def build_compat_payload(state: dict[str, Any]) -> dict[str, Any]:
    manifest = state["manifest"]

    payload: dict[str, Any] = {
        "adapter_version": ADAPTER_VERSION,
        "project_id": state["project_id"],
        "phase": state["phase"],
        "halted": state["halted"],
        "approval_status": state["approval_status"],
        "approved_for_upload": state["approved_for_upload"],
        "mode": manifest["mode"],
        "updated_at": state["updated_at"],
    }

    halt_reason = state.get("halt_reason")
    if halt_reason is not None:
        payload["halt_reason"] = halt_reason

    _validate_payload(payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a minimal read-only compatibility payload from PROJECT_STATE.json"
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Path to canonical PROJECT_STATE.json",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write compat payload JSON",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    state_path = Path(args.state)
    state = load_state(state_path)
    payload = build_compat_payload(state)

    json_output = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2 if args.pretty else None,
        sort_keys=True,
    )
    if args.pretty:
        json_output += "\n"

    if args.output:
        output_path = Path(args.output)
        _atomic_write_text(output_path, json_output)
        print(f"ADAPTER_OK output={output_path}")
        return

    print(json_output)


if __name__ == "__main__":
    main()
