#!/usr/bin/env python3
"""
FlowMind 2026
Manifest Engine v3
Immutable + Lifecycle Model
"""

import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime, UTC

PROJECTS_DIR = Path("projects")

def compute_hash(data: dict) -> str:
    temp = dict(data)
    temp.pop("manifest_hash", None)
    encoded = json.dumps(temp, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()

def create_manifest(project_id):
    project_path = PROJECTS_DIR / project_id
    project_path.mkdir(parents=True, exist_ok=True)

    manifest = {
        "project_id": project_id,
        "manifest_version": 3,
        "status": "CREATED",
        "lifecycle": "SAFE",
        "topic": "UNDEFINED",
        "mode": "normal",
        "created_at": datetime.now(UTC).isoformat(),
        "override_history": []
    }

    manifest["manifest_hash"] = compute_hash(manifest)

    manifest_path = project_path / "ExecutionManifest.json"

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("[OK] Immutable Manifest v3 created.")
    print("[PATH]", manifest_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: engine.py <PROJECT_ID>")
        sys.exit(1)

    create_manifest(sys.argv[1])

if __name__ == "__main__":
    main()
