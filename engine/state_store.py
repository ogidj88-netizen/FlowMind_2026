from __future__ import annotations

import json
import hashlib
import uuid
import shutil
from copy import deepcopy
import fcntl
import threading
from contextlib import contextmanager
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


# Stable sidecar inode: never unlink a lock while another process may wait on it.
_locks: dict[str, threading.RLock] = {}
_lock_registry = threading.Lock()
_local = threading.local()


def _reset_locks_after_fork() -> None:
    global _locks, _lock_registry, _local
    # Child must not mistake an inherited parent's lock for its own reentrant lock.
    # Close child copies without LOCK_UN (the parent's open description is shared).
    for handle in getattr(_local, "held", {}).values():
        handle.close()
    _locks = {}
    _lock_registry = threading.Lock()
    _local = threading.local()


os.register_at_fork(after_in_child=_reset_locks_after_fork)


@contextmanager
def file_lock(path: str | Path):
    key = str(Path(path).resolve())
    with _lock_registry:
        mutex = _locks.setdefault(key, threading.RLock())
    with mutex:
        held = getattr(_local, "held", {})
        if key in held:
            yield
            return
        lock_path = Path(key)
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a+b") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            held[key] = handle
            _local.held = held
            try:
                yield
            finally:
                del held[key]
                fcntl.flock(handle, fcntl.LOCK_UN)


def state_lock(path: str | Path):
    return file_lock(str(Path(path).resolve()) + ".lock")


def write_bytes_atomic(path: Path, data: bytes) -> None:
    """Unique temporary file, durable replace; caller owns the relevant lock."""
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        _fsync_directory(path.parent)
    finally:
        Path(name).unlink(missing_ok=True)


def _fsync_directory(directory: Path) -> None:
    dir_fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def _save_state_atomic(
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


def save_state_atomic(
    path: str | Path, state: Mapping[str, Any], *,
    previous_state: Mapping[str, Any] | None = None,
    enforce_runtime_mutation_only: bool = False,
) -> dict[str, Any]:
    with state_lock(path):
        if previous_state is not None and load_state(path) != validate_state(previous_state):
            raise StateValidationError("stale canonical state; reload before retry")
        return _save_state_atomic(path, state, previous_state=previous_state,
                                  enforce_runtime_mutation_only=enforce_runtime_mutation_only)


def save_state_with_disk_guard(
    path: str | Path, candidate_state: Mapping[str, Any], *,
    expected_state: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    with state_lock(path):
        state_path = Path(path)
        if state_path.exists():
            previous_state = load_state(state_path)
            if expected_state is not None and previous_state != validate_state(expected_state):
                raise StateValidationError("stale canonical state; reload before retry")
            return _save_state_atomic(state_path, candidate_state, previous_state=previous_state,
                                      enforce_runtime_mutation_only=True)
        if expected_state is not None:
            raise StateValidationError("canonical state disappeared before write")
        return _save_state_atomic(state_path, candidate_state)


__all__ = ["save_state_atomic", "save_state_with_disk_guard", "state_lock",
           "file_lock", "write_bytes_atomic"]


# Transaction journal is recovery data, never an alternative project state.
PUBLICATION_JOURNAL = ".artifact-publication.pending.json"
_PLAN_READINESS_FIELDS = {"render_ready", "missing_requirements", "readiness_status",
    "source_final_render_report_path", "source_final_video_path", "updated_at",
    "final_render_readiness_applied_by", "final_render_readiness_applied_tool_version"}


def artifact_digest(path: Path) -> str:
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if path.name == "assembly_plan.json":
            payload = {key: value for key, value in payload.items() if key not in _PLAN_READINESS_FIELDS}
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"),
                                         ensure_ascii=False, allow_nan=False).encode()).hexdigest()
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def assert_published_artifacts(state_path: Path, state: Mapping[str, Any]) -> None:
    if (state_path.parent / PUBLICATION_JOURNAL).exists():
        raise StateValidationError("incomplete artifact publication; recovery required")
    if "artifact_publication" not in state["artifacts"]:
        return  # Existing archived evidence retains its existing contract.
    receipt = state["artifacts"]["artifact_publication"]
    if not isinstance(receipt, dict) or not isinstance(receipt.get("files"), dict):
        raise StateValidationError("invalid artifact publication receipt")
    for name, expected in receipt["files"].items():
        path = Path(name).resolve()
        if not path.is_relative_to(state_path.parent.resolve()) or not path.is_file():
            raise StateValidationError("published artifact missing/outside project")
        if artifact_digest(path) != expected:
            raise StateValidationError("published artifact identity mismatch")


def recover_artifact_publication(state_path: Path) -> None:
    state_path = state_path.resolve()
    with state_lock(state_path):
        journal_path = state_path.parent / PUBLICATION_JOURNAL
        if not journal_path.exists():
            return
        journal = json.loads(journal_path.read_text())
        state = load_state(state_path)
        committed = state["artifacts"].get("artifact_publication", {}).get("id") == journal["id"]
        entries = journal["entries"]
        for entry in entries:
            for field in ("target", "backup"):
                if not Path(entry[field]).resolve().is_relative_to(state_path.parent):
                    raise StateValidationError("publication recovery path outside project")
        if committed:
            for entry in entries:
                if artifact_digest(Path(entry["target"])) != entry["digest"]:
                    raise StateValidationError("committed publication is incomplete/corrupt")
        else:
            for entry in entries:
                target, backup = Path(entry["target"]), Path(entry["backup"])
                if entry["existed"]:
                    # Keep backup until the whole rollback is durable and repeatable.
                    if not backup.is_file():
                        raise StateValidationError("publication rollback backup missing")
                    fd, name = tempfile.mkstemp(dir=target.parent, prefix=target.name + ".rollback.")
                    os.close(fd)
                    Path(name).unlink()
                    os.link(backup, name)
                    os.replace(name, target)
                else:
                    target.unlink(missing_ok=True)
                _fsync_directory(target.parent)
        journal_path.unlink()
        _fsync_directory(state_path.parent)
        for entry in entries:
            Path(entry["backup"]).unlink(missing_ok=True)


def publish_artifacts(state_path: Path, candidate_state: Mapping[str, Any], *,
                      expected_state: Mapping[str, Any], staged: Mapping[Path, Path]) -> dict[str, Any]:
    """Digest/fsync staging outside lock; publish only after CAS preflight.

    A durable journal blocks guards until a complete commit or rollback. The only
    commit authority is the publication id stored in canonical PROJECT_STATE.
    """
    state_path = state_path.resolve()
    if expected_state["phase"] != "ASSEMBLY":
        raise StateValidationError("artifact publication requires ASSEMBLY state")
    for key in ("phase", "phase_history", "qa_passed", "approval_status", "approved_for_upload",
                "halted", "halt_reason", "resume_hint"):
        if candidate_state[key] != expected_state[key]:
            raise StateValidationError("artifact publisher cannot change phase, QA or approval gates")
    identifier = uuid.uuid4().hex
    entries = []
    for target, source in staged.items():
        target, source = target.resolve(), source.resolve()
        if (not target.is_relative_to(state_path.parent) or not source.is_relative_to(state_path.parent)
                or target == source or not source.is_file()):
            raise StateValidationError("invalid staged artifact path")
        digest = artifact_digest(source)
        with source.open("rb") as stream:
            os.fsync(stream.fileno())
        entries.append({"target": str(target), "source": str(source), "digest": digest,
                        "backup": str(source.parent / (identifier + ".backup." + target.name))})
    candidate = deepcopy(candidate_state)
    receipt = deepcopy(expected_state["artifacts"].get("artifact_publication", {"files": {}}))
    receipt["id"] = identifier
    receipt["files"].update({entry["target"]: entry["digest"] for entry in entries})
    candidate["artifacts"]["artifact_publication"] = receipt
    candidate = validate_state(candidate)
    assert_runtime_mutation_only(expected_state, candidate)
    with state_lock(state_path):
        recover_artifact_publication(state_path)
        if load_state(state_path) != validate_state(expected_state):
            raise StateValidationError("stale canonical state; reload before retry")
        journal_path = state_path.parent / PUBLICATION_JOURNAL
        for entry in entries:
            target = Path(entry["target"])
            target.parent.mkdir(parents=True, exist_ok=True)
            entry["existed"] = target.exists()
            if entry["existed"]:
                os.link(target, entry["backup"])
                _fsync_directory(Path(entry["backup"]).parent)
        journal = {"id": identifier, "entries": entries}
        write_bytes_atomic(journal_path, (json.dumps(journal) + "\n").encode())
        try:
            for entry in entries:
                os.replace(entry["source"], entry["target"])
                _fsync_directory(Path(entry["target"]).parent)
            saved = save_state_with_disk_guard(state_path, candidate, expected_state=expected_state)
        except BaseException:
            recover_artifact_publication(state_path)
            raise
        # Normal commit already validated staged content outside lock; no media rehash here.
        journal_path.unlink()
        _fsync_directory(state_path.parent)
        for entry in entries:
            Path(entry["backup"]).unlink(missing_ok=True)
        return saved


@contextmanager
def artifact_staging_directory(state_path: Path, prefix: str):
    root = state_path.resolve().parent / ".staging"
    root.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(dir=root, prefix=prefix))
    try:
        yield directory
    finally:
        # Preserve rollback backups if recovery itself was interrupted/failed.
        journal_path = state_path.resolve().parent / PUBLICATION_JOURNAL
        if not journal_path.exists():
            shutil.rmtree(directory, ignore_errors=True)
