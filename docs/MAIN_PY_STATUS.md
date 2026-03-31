# MAIN.PY STATUS

Status: LOCKED  
Branch: `cashflow-mode`

## Current verified role

`main.py` is a **legacy launcher**, not a canonical dispatcher.

Verified behavior:

- requires `--project`
- accepts:
  - `--advance`
  - `--halt`
  - `--resume`
- checks existence of:
  - `projects/<PROJECT_ID>/ExecutionManifest.json`
- delegates runtime actions to:
  - `dispatcher/engine.py`

## Meaning

`main.py` belongs to the **legacy runtime layer**.

It is tightly coupled to:

- `ExecutionManifest.json`
- `dispatcher/engine.py`
- legacy phase flow

It is **not** coupled to:

- `PROJECT_STATE.json`
- `engine/canonical_dispatcher.py`
- `tools/dispatcher_cli.py`
- `tools/dispatcher.sh`

## Rule

Until a dedicated migration plan exists, it is forbidden to:

- treat `main.py` as canonical dispatcher entrypoint
- wire `main.py` directly to the new canonical dispatcher
- mix `ExecutionManifest.json` flow with `PROJECT_STATE.json` flow inside `main.py`
- extend `main.py` with partial bridge logic “for convenience”

## Final decision

For `cashflow-mode` right now:

- `main.py` = legacy launcher
- `dispatcher/engine.py` = legacy runtime dispatcher
- `engine/canonical_dispatcher.py` = new standalone canonical dispatcher layer

## Next migration prerequisite

Before any future migration of `main.py`, all of the following must exist:

1. explicit migration plan
2. phase mapping between legacy and canonical flow
3. state model reconciliation
4. single source of truth decision
