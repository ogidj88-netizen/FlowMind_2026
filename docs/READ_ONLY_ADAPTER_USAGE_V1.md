# Read-Only Adapter Usage V1

## Purpose

This document defines how the minimal read-only compatibility adapter is intended to be used in Migration v1.

It is an operational usage note, not a new compatibility rule set.

---

## Implemented module

The implemented adapter module is:

- `adapters/read_only_compat_adapter.py`

Its role is to build a derived compatibility payload from canonical `PROJECT_STATE.json`.

---

## What the adapter does

The adapter:

- reads canonical `PROJECT_STATE.json`
- validates state through canonical validation flow
- builds a minimal derived compatibility payload
- optionally writes the derived payload to a separate output file
- never writes back into canonical state

---

## Allowed usage

Allowed usage in Migration v1 includes:

- printing compatibility payload to stdout
- writing compatibility payload to a separate JSON file
- using compatibility payload as read-only downstream input
- using compatibility payload for explicit compatibility inspection

---

## Forbidden usage

Forbidden usage includes:

- writing adapter payload back into canonical `PROJECT_STATE.json`
- treating adapter payload as canonical runtime truth
- using adapter payload as a dispatcher substitute
- mutating canonical state based on undocumented adapter-side inference
- expanding adapter payload without explicit compatibility review

---

## Current payload scope

The implemented payload currently exposes:

- `adapter_version`
- `project_id`
- `phase`
- `halted`
- `approval_status`
- `approved_for_upload`
- `mode`
- `updated_at`

Optional:
- `halt_reason` when present

---

## Operational examples

Stdout mode:

`python3 adapters/read_only_compat_adapter.py --state projects/P2026_CANONICAL_001/PROJECT_STATE.json --pretty`

File output mode:

`python3 adapters/read_only_compat_adapter.py --state projects/P2026_CANONICAL_001/PROJECT_STATE.json --output tmp/compat_P2026_CANONICAL_001.json --pretty`

---

## Migration v1 interpretation

This adapter is the first implementation step of the documented read-only compatibility boundary.

It should be treated as:

- minimal
- read-only
- non-authoritative
- versioned
- deliberately narrow

---

## Final statement

The adapter is intended to support compatibility visibility, not mixed control.

If broader compatibility behavior is needed later, it must be reviewed explicitly before expansion.
