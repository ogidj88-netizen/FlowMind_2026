# CONTROL LAYER AUDIT V1

## Status
Phase 2 active.
Audit zone: control layer.

## Goal
Identify the one real control contour and separate it from legacy or parallel control logic.

---

## Working Verdict

### KEEP
- engine/canonical_dispatcher.py
- engine/state_validator.py
- engine/state_store.py
- FLOWMIND_WORKING_TARGET.md

Reason:
These files form the strongest currently validated basis for one stable control contour built around PROJECT_STATE.json and strict dispatcher/state rules.

---

### FREEZE
- manifest_engine/engine.py
- FLOWMIND_CANONICAL_MAP.md

Reason:
These may remain useful as utility/history/reference, but they do not qualify as the active control center for the current working contour.

---

### REMOVE
- dispatcher/engine.py
- dispatcher/engine_v16.py

Reason:
These files represent legacy or parallel dispatcher logic and violate the one-control-brain rule.

---

### REPLACE LATER
- main.py

Reason:
A single entrypoint is required, but the current implementation points into the wrong control contour and must be redirected or replaced later.

---

## Main Audit Conclusion
The repository currently contains competing control layers.

The strongest valid control core is:

- engine/canonical_dispatcher.py
- engine/state_validator.py
- engine/state_store.py

The main current control-layer problem is not lack of architecture.
It is coexistence of multiple control brains.

---

## Rule For Next Step
Do not expand architecture.

Do not clean random files first.

Next practical cleanup must continue from control-layer alignment, not from docs cleanup, production cleanup, or project artifacts cleanup.
