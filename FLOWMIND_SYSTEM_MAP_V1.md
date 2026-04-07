# FLOWMIND SYSTEM MAP V1

Status: ACTIVE SYSTEM MAP  
Branch: `cashflow-mode`

## Purpose

This file is the current high-level map of the repository after Phase 2 cleanup.

It distinguishes:
- active core
- active support/data
- frozen legacy
- historical context

It is intended to reduce ambiguity and prevent parallel-system thinking.

---

## 1. ACTIVE CORE

These paths belong to the active canonical control contour:

- `engine/`
- `tools/dispatcher.sh`
- `tools/dispatcher_cli.py`
- `tools/check_dispatcher.sh`
- `tools/run_dispatcher_checks.py`
- `templates/PROJECT_STATE.template.json`
- `CANONICAL_DISPATCHER_SPEC.md`
- `FLOWMIND_WORKING_TARGET.md`

### Meaning
This is the active control brain, active command surface, active validation path, and active state-template direction.

---

## 2. ACTIVE SUPPORT / DATA

These paths are active but not control-brain paths:

- `tools/` except:
  - `tools/dispatcher.sh`
  - `tools/dispatcher_cli.py`
  - `tools/check_dispatcher.sh`
  - `tools/run_dispatcher_checks.py`
- `production/`
- `projects/`
- `.githooks/`
- `.gitignore`
- `Makefile`

### Meaning
These paths support execution, validation, project state, and repository discipline.

They are not alternative control contours.

---

## 3. FROZEN LEGACY

These paths/files are preserved but not part of the active canonical control contour:

- `main.py`
- `dispatcher/`
- `core_frozen/`
- `cashflow/`
- `adapters/read_only_compat_adapter.py`
- `manifest_engine/engine.py`

### Meaning
These are frozen legacy, utility, or compatibility remnants kept for history, narrow utility, or explicit reference only.

They must not be used to define active architecture.

---

## 4. HISTORICAL CONTEXT

These documents exist as historical or audit context and must not override active system truth:

- `FLOWMIND_CANONICAL_MAP.md`
- `docs/MIGRATION_ROADMAP_V1.md`
- `docs/READ_ONLY_COMPATIBILITY_BRIDGE.md`
- `docs/READ_ONLY_ADAPTER_USAGE_V1.md`
- `docs/COMPAT_ADAPTER_SMOKE_CHECK_V1.md`
- Phase 2 audit docs and legacy migration docs under `docs/`

### Meaning
These files explain prior decisions, cleanup logic, and historical architecture.

They are not active architecture authority.

---

## 5. CURRENT RULE

When architectural ambiguity appears, the repository must be interpreted in this order:

1. `FLOWMIND_SYSTEM_MAP_V1.md`
2. `CANONICAL_DISPATCHER_SPEC.md`
3. `FLOWMIND_WORKING_TARGET.md`

Historical or frozen files must not override this order.

---

## 6. FINAL STATEMENT

FlowMind is now interpreted as:

- one active control contour
- one active state model
- one active command surface
- frozen legacy outside the contour
- historical context outside architectural authority
