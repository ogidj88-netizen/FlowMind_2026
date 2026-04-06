#!/usr/bin/env python3
"""
FlowMind 2026
dispatcher/engine.py

PHASE 2 TOMBSTONE:
This legacy dispatcher is removed from the active control contour.

It is intentionally kept only as a fail-fast tombstone during cleanup,
so accidental execution through old entrypoints cannot silently restore
legacy control flow.
"""

import sys


def main() -> None:
    print("[BLOCKED] dispatcher/engine.py is retired from the active control contour.")
    print("[ACTION] Redirect the entrypoint to the canonical control layer.")
    sys.exit(1)


if __name__ == "__main__":
    main()
