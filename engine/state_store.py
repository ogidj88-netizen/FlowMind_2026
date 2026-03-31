from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

from engine.state_validator import (
    StateValidationError,
    assert_runtime_mutation_only,
    load_state,
    validate_state,
)


def _fsync_directory(directory: Path) -> None:
    dir_fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def save_state_atomic(
    path: str | Path,
    state: Mapping[str, Any],
    *,
    previous_state: Mapping[str, Any] | None = None,
    enforce_runtime_mutation_only: bool = False,
) -> dict[str, Any]:
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    validated_candidate = validate_state(state)

    if enforce_runtime_mutation_only:
        if previous_state is None:
            raise StateValidationError(
                "previous_state is required when enforce_runtime_mutation_only=True"
            )
        assert_runtime_mutation_only(previous_state, validated_candidate)

    serialized = json.dumps(
        validated_candidate,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    ) + "\n"

    fd: int | None = None
    temp_path: Path | None = None

    try:
        fd, temp_name = tempfile.mkstemp(
            prefix=f"{state_path.name}.",
            suffix=".tmp",
            dir=state_path.parent,
            text=True,
        )
        temp_path = Path(temp_name)

        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            fd = None
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temp_path, state_path)
        _fsync_directory(state_path.parent)
        return validated_candidate

    except Exception:
        if fd is not None:
            os.close(fd)
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise


def save_state_with_disk_guard(
    path: str | Path,
    candidate_state: Mapping[str, Any],
) -> dict[str, Any]:
    state_path = Path(path)

    if state_path.exists():
        previous_state = load_state(state_path)
        return save_state_atomic(
            state_path,
            candidate_state,
            previous_state=previous_state,
            enforce_runtime_mutation_only=True,
        )

    return save_state_atomic(state_path, candidate_state)


__all__ = [
    "save_state_atomic",
    "save_state_with_disk_guard",
]
