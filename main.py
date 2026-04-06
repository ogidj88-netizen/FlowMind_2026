#!/usr/bin/env python3
"""
FlowMind 2026
main.py

PHASE 2 TOMBSTONE:
The previous entrypoint is retired from the active control contour.

This file is intentionally fail-fast during cleanup, so the repository
cannot silently route execution into blocked legacy dispatcher paths.
"""

import sys


def main() -> None:
    print("[BLOCKED] main.py legacy entrypoint is retired from the active control contour.")
    print("[ACTION] A new canonical entrypoint must be introduced after control-layer alignment.")
    sys.exit(1)


if __name__ == "__main__":
    main()
