# M4 Read-Only Adapter Contract

## Purpose

This document defines the minimal read-only adapter contract allowed for Migration v1.

It does not define a writable bridge.

It defines the smallest safe compatibility payload that legacy runtime may read from canonical state without gaining control authority.

---

## Design goal

The adapter contract must be:

- read-only
- minimal
- explicit
- stable enough for migration use
- non-authoritative

The adapter is a compatibility layer only.

It is not a second state system.

It is not a second dispatcher.

It is not a control surface.

---

## Canonical ownership rule

Canonical state remains owned by the canonical dispatcher.

The adapter may expose derived values from canonical state, but those values do not become a new source of truth.

If adapter output conflicts with canonical state, canonical state wins.

---

## Minimal allowed read fields

For Migration v1, the adapter may expose only the following fields:

- `project_id`
- `phase`
- `halted`
- `halt_reason`
- `approval_status`
- `approved_for_upload`
- `mode`
- `updated_at`

These fields are allowed only as read-only compatibility output.

They must not be treated as writable inputs from legacy runtime.

---

## Field intent

### `project_id`
Identity only.

### `phase`
Compatibility-facing phase visibility only.  
Phase remains canonically owned by dispatcher logic.

### `halted`
Compatibility-facing halt visibility only.

### `halt_reason`
Compatibility-facing explanation only.

### `approval_status`
Compatibility-facing approval visibility only.

### `approved_for_upload`
Compatibility-facing gate visibility only.

### `mode`
Compatibility-facing execution mode visibility only.

### `updated_at`
Freshness indicator only.

---

## Forbidden fields

The adapter must not expose internal canonical control structures unless separately approved.

Examples of forbidden exposure for Migration v1 include:

- dispatcher-only transition metadata
- internal transition guards
- retry control internals
- write authority flags
- mutable override channels
- any structure that invites legacy-side control decisions
- any field not explicitly listed in this contract

Default rule:

If a field is not explicitly allowed, it is forbidden.

---

## Example output shape

Example compatibility payload:

    {
      "project_id": "P123",
      "phase": "FINAL_READY",
      "halted": false,
      "halt_reason": null,
      "approval_status": "APPROVED",
      "approved_for_upload": true,
      "mode": "cashflow",
      "updated_at": "2026-03-31T12:00:00Z"
    }

This example is illustrative only.

The example does not grant schema expansion rights.

---

## Interpretation rule

Legacy runtime may read this payload only for compatibility behavior such as:

- display
- compatibility checks
- downstream branching that does not mutate canonical state

Legacy runtime may not:

- push edits back
- reinterpret adapter output as owned state
- persist adapter output as replacement canonical truth
- derive write authority from presence of these fields

---

## Non-goals

This contract does not define:

- reverse sync
- bidirectional state exchange
- canonical write delegation
- legacy authority restoration
- legacy-driven phase control

Those are explicitly out of scope.

---

## Migration v1 rule

For Migration v1:

- canonical dispatcher owns state
- adapter exposes minimal read-only compatibility data
- legacy runtime remains downstream
- no write-back path is allowed

---

## Acceptance condition for M4

M4 may be considered prepared on docs level only if:

1. allowed read fields are explicitly listed
2. forbidden non-listed fields are explicitly excluded
3. adapter output is defined as non-authoritative
4. no reverse-sync language appears in the contract
5. canonical dispatcher ownership remains explicit

---

## Final statement

This contract exists to reduce migration ambiguity.

It is a read-only compatibility adapter contract only.

It must be interpreted narrowly, not expansively.
