#!/usr/bin/env python3
"""
S1 Strategy Module (Stub v1)
Generates S1_strategy.json
"""

import sys
import json
from pathlib import Path
from datetime import datetime, UTC


def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    project_id = sys.argv[1]

    project_dir = Path("projects") / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "project_id": project_id,
        "phase": "S1",
        "niche": "Invisible Costs",
        "strategy_version": "v1",
        "created_at": datetime.now(UTC).isoformat()
    }

    with open(project_dir / "S1_strategy.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("[S1 MODULE] S1_strategy.json generated.")


if __name__ == "__main__":
    main()
