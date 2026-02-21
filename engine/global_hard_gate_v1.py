#!/usr/bin/env python3
"""
FlowMind 2026
GLOBAL HARD GATE v1
Immutable guard between S2 and S3
"""

import json
import os
import sys

REQUIRED_SCORES = {
    "hook_score": 8,
    "ending_score": 8,
    "king_detail_score": 8,
    "tropecraft_score": 7
}


def load_json(path):
    if not os.path.exists(path):
        print(f"[HARD GATE] Missing file: {path}")
        sys.exit(1)

    with open(path, "r") as f:
        return json.load(f)


def validate_scores(data):
    scores = data.get("quality_scores", {})

    for key, min_value in REQUIRED_SCORES.items():
        value = scores.get(key)

        if value is None:
            print(f"[HARD GATE] Missing score: {key}")
            sys.exit(1)

        if value < min_value:
            print(f"[HARD GATE] FAIL: {key} = {value} < {min_value}")
            sys.exit(1)

    print("[HARD GATE] Score validation PASS")


def validate_semantic(data):
    if not data.get("semantic_pass", False):
        print("[HARD GATE] FAIL: Semantic validation not passed")
        sys.exit(1)

    print("[HARD GATE] Semantic PASS")


def main(project_id):
    base_path = f"projects/{project_id}"
    s2_path = os.path.join(base_path, "S2_script.json")

    print(f"[HARD GATE] Checking project: {project_id}")

    s2_data = load_json(s2_path)

    validate_scores(s2_data)
    validate_semantic(s2_data)

    print("[HARD GATE] GLOBAL PASS — safe to proceed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 engine/global_hard_gate_v1.py <PROJECT_ID>")
        sys.exit(1)

    main(sys.argv[1])