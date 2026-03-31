# CANONICAL DISPATCHER ENTRYPOINTS

Status: LOCKED
Branch: cashflow-mode

## Final decision

For the new dispatcher contour in cashflow-mode, the official entrypoints are:

1. User-facing local entrypoint
- tools/dispatcher.sh

This is the only official shell entrypoint for manual local dispatcher operations.

2. CLI implementation layer
- tools/dispatcher_cli.py

This is the canonical CLI implementation used by tools/dispatcher.sh.

3. Core dispatcher logic
- engine/canonical_dispatcher.py

This is the canonical dispatcher core and must not be treated as the primary user-facing launcher.

4. Validation entrypoint
- tools/check_dispatcher.sh

This is the canonical local validation command for dispatcher checks.

## Rule

It is forbidden to treat any of the following as the primary local dispatcher entrypoint:

- engine/canonical_dispatcher.py
- tools/run_dispatcher_checks.py
- tools/smoke_test_dispatcher.py
- main.py
- dispatcher/engine.py
- dispatcher/engine_v16.py

## Operational truth

For manual local work, the correct command surface is:

./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json show

For validation:

./tools/check_dispatcher.sh

## Why this decision exists

This decision prevents:

- launcher duplication
- ambiguous operator behavior
- accidental use of legacy runtime entrypoints
- direct coupling between user-facing operations and dispatcher core internals

## Legacy separation rule

The following remain outside the new canonical dispatcher contour:

- main.py
- dispatcher/engine.py
- dispatcher/engine_v16.py

They belong to the legacy runtime layer and must not be mixed with the new dispatcher entrypoint model.

## Final locked statement

For cashflow-mode:

- tools/dispatcher.sh = official local dispatcher entrypoint
- tools/dispatcher_cli.py = official CLI layer
- engine/canonical_dispatcher.py = official dispatcher core
- tools/check_dispatcher.sh = official dispatcher validation entrypoint
