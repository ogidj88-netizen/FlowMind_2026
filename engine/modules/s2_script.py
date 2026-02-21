#!/usr/bin/env python3
"""
S2 Script Module v2
Cross-Phase aware
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

    s1_path = project_dir / "S1_strategy.json"

    if not s1_path.exists():
        print("[ERROR] S1_strategy.json missing.")
        sys.exit(2)

    with open(s1_path, "r", encoding="utf-8") as f:
        s1 = json.load(f)

    data = {
        "project_id": project_id,
        "phase": "S2",
        "based_on_strategy": True,
        "based_on_niche": s1["niche"],
        "strategy_version": s1["strategy_version"],
        "script_outline": [
            "Hook",
            "Problem",
            "Escalation",
            "Reveal",
            "Call to Action"
        ],
        "created_at": datetime.now(UTC).isoformat()
    }

    with open(project_dir / "S2_script.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("[S2 MODULE] S2_script.json generated.")


if __name__ == "__main__":
    main()
