# DISPATCHER CHEAT SHEET

Status: WORKING
Branch: cashflow-mode

## Canonical local entrypoints

Main local dispatcher command:
./tools/dispatcher.sh

Main validation command:
./tools/check_dispatcher.sh

## Basic commands

Show state:
./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json show

Transition to next phase:
./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json transition --to SCRIPT

Halt:
./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json halt --reason TEST_HALT --resume-hint resume_to_assets

Resume from HALT:
./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json resume --to ASSETS

Mark QA passed:
./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json mark-qa-passed

Approve upload:
./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json approve-upload

Run dispatcher checks:
./tools/check_dispatcher.sh

## Important rules

- Use tools/dispatcher.sh as the main local dispatcher entrypoint.
- Do not use main.py for the new dispatcher contour.
- Do not use dispatcher/engine.py for the new dispatcher contour.
- Do not mix ExecutionManifest.json flow with PROJECT_STATE.json flow.
- Use tools/check_dispatcher.sh before touching dispatcher logic.

## Current architecture truth

Legacy runtime:
- main.py
- dispatcher/engine.py
- ExecutionManifest.json

New canonical dispatcher:
- engine/canonical_dispatcher.py
- tools/dispatcher_cli.py
- tools/dispatcher.sh
- PROJECT_STATE.json

## Purpose of this file

This file is only a short operational reference.
It does not replace:
- docs/CANONICAL_DISPATCHER_ENTRYPOINTS.md
- docs/DISPATCHER_ENTRYPOINT.md
- docs/MAIN_PY_STATUS.md
- docs/DISPATCHER_ENGINE_STATUS.md
