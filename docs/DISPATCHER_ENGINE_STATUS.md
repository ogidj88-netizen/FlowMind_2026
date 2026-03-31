# DISPATCHER/ENGINE.PY STATUS

Status: LOCKED  
Branch: `cashflow-mode`

## Current verified status

`dispatcher/engine.py` is a **legacy frozen artifact**, not a valid canonical dispatcher.

Verified from direct audit:

- file contains:
  - locked JSON writer
  - `load_manifest(project_id)`
  - `save_manifest(manifest, path)`
  - legacy constants like `PHASE_ORDER` and `PHASE_TO_FILE`
- file does **not** provide verified live dispatcher behavior in the audited state
- audited visible code does **not** prove existence of:
  - `update_phase`
  - `halt`
  - `resume`
  - `advance`
  - canonical transition engine
  - complete runtime executor logic

## Architectural meaning

`dispatcher/engine.py` must not be treated as:

- canonical dispatcher
- safe integration target
- migration bridge to the new dispatcher layer
- trustworthy runtime control surface

## Rule

Until a dedicated migration/replacement plan exists, it is forbidden to:

- refactor `dispatcher/engine.py` incrementally
- wire the new canonical dispatcher into `dispatcher/engine.py`
- treat `dispatcher/engine.py` as the source of truth for runtime control
- base new architecture decisions on assumptions that this file is complete

## Final decision

For `cashflow-mode`:

- `dispatcher/engine.py` = legacy frozen artifact
- `main.py` = legacy launcher
- `engine/canonical_dispatcher.py` = new standalone canonical dispatcher layer

## Operational implication

Do not build new control logic on top of `dispatcher/engine.py`.
Do not migrate runtime through this file.
Keep it frozen until a full replacement/migration block is approved.
