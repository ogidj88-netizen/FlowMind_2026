# MAIN.PY STATUS

Status: ACTIVE AUDIT TRUTH  
Branch: `cashflow-mode`

## Current verified role

`main.py` is a **retired legacy tombstone**, not a canonical dispatcher entrypoint and not an active launcher.

## Current verified behavior

`main.py` now:
- does not operate as a runtime launcher
- does not delegate to active dispatcher control flow
- intentionally fails fast
- exists only to prevent silent reuse of legacy entry logic during Phase 2 cleanup

## Meaning

`main.py` no longer belongs to the active control contour.

It must not be treated as:
- active launcher
- dispatcher entrypoint
- integration bridge
- temporary convenience wrapper

## Active control truth

The active canonical command surface is:

- `tools/dispatcher.sh`
- `tools/dispatcher_cli.py`
- `tools/check_dispatcher.sh`

The active canonical control core is:

- `engine/canonical_dispatcher.py`
- `engine/state_validator.py`
- `engine/state_store.py`

## Rule

During Phase 2, it is forbidden to:

- restore legacy runtime behavior inside `main.py`
- rewire `main.py` back to `dispatcher/engine.py`
- use `main.py` as a shortcut to reintroduce a second control path
- extend `main.py` before control-layer cleanup is complete

## Final decision

For `cashflow-mode` right now:

- `main.py` = retired legacy tombstone
- `dispatcher/engine.py` = retired legacy tombstone
- `dispatcher/engine_v16.py` = retired legacy tombstone
- `tools/dispatcher.sh` = active shell entrypoint
- `tools/dispatcher_cli.py` = active CLI entrypoint
- `engine/canonical_dispatcher.py` = active canonical control core
