# DISPATCHER/ENGINE.PY STATUS

Status: ACTIVE AUDIT TRUTH  
Branch: `cashflow-mode`

## Current verified role

`dispatcher/engine.py` is a **retired legacy tombstone**, not a canonical dispatcher and not an active runtime dispatcher.

## Current verified behavior

`dispatcher/engine.py` now:
- does not operate as an active dispatcher
- does not provide valid runtime control flow
- intentionally fails fast
- exists only to prevent silent reuse of legacy dispatcher logic during Phase 2 cleanup

## Meaning

`dispatcher/engine.py` no longer belongs to the active control contour.

It must not be treated as:
- canonical dispatcher
- runtime control surface
- integration target
- migration bridge
- temporary fallback dispatcher

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

- restore dispatcher behavior inside `dispatcher/engine.py`
- route `main.py` back into `dispatcher/engine.py`
- use this file as a bridge into canonical control flow
- build new runtime logic on top of this file

## Final decision

For `cashflow-mode` right now:

- `dispatcher/engine.py` = retired legacy tombstone
- `dispatcher/engine_v16.py` = retired legacy tombstone
- `main.py` = retired legacy tombstone
- `tools/dispatcher.sh` = active shell entrypoint
- `tools/dispatcher_cli.py` = active CLI entrypoint
- `engine/canonical_dispatcher.py` = active canonical control core
