#!/usr/bin/env python3
from __future__ import annotations

import sys


MESSAGE = """\
FLOWMIND_LEGACY_RUNNER_DISABLED

engine/module_runner.py is frozen legacy and must not be used as an active phase runner.

Reason:
- it can route phases to engine/modules/*
- engine/modules/s2_script.py has a direct PROJECT_STATE.json write path
- active FlowMind state must be updated only through canonical guarded paths

Use instead:
- tools/flowmind_run_phase.py for active phase executor dry-run/run
- tools/dispatcher.sh for canonical phase transitions

This file intentionally fails closed.
"""


def main() -> None:
    print(MESSAGE, file=sys.stderr)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
