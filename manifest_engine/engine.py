#!/usr/bin/env python3
"""
FlowMind Manifest Engine (v3.x) — Single-Writer enforced

Rule:
- ExecutionManifest.json is written ONLY via tools/json_write_locked.sh
"""

import json
import subprocess
import hashlib
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
JSON_WRITE_LOCKED = TOOLS_DIR / "json_write_locked.sh"


def compute_hash(manifest: dict) -> str:
    tmp = dict(manifest)
    tmp.pop("manifest_hash", None)
    raw = json.dumps(tmp, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _write_json_locked(path: Path, obj: dict) -> None:
    if not JSON_WRITE_LOCKED.exists():
        raise RuntimeError(f"locked writer missing: {JSON_WRITE_LOCKED}")

    data = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    proc = subprocess.run(
        [str(JSON_WRITE_LOCKED), str(path)],
        input=data.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace").strip())


def create_immutable_manifest(project_path: str | Path, base: dict) -> Path:
    """
    Creates/overwrites ExecutionManifest.json in project_path using locked writer.
    """
    project_path = Path(project_path)
    project_path.mkdir(parents=True, exist_ok=True)

    manifest = dict(base)
    manifest["manifest_hash"] = compute_hash(manifest)

    manifest_path = project_path / "ExecutionManifest.json"
    _write_json_locked(manifest_path, manifest)

    print("[OK] Immutable Manifest created (locked-writer).")
    print("[PATH]", manifest_path)
    return manifest_path
