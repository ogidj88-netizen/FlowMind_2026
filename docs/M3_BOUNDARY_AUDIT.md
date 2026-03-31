# M3 Boundary Audit — Canonical vs Legacy

## Purpose

This document defines the audit boundary required for Migration v1 M3 preparation.

Its role is not to introduce new runtime behavior.

Its role is to explicitly verify that the migration model preserves canonical control authority and prevents reverse state corruption from legacy runtime paths.

---

## Canonical rule

The canonical dispatcher remains the only valid control authority for canonical project state.

Canonical state includes, at minimum:

- PROJECT_STATE.json
- canonical phase authority
- canonical halt authority
- canonical approval authority
- canonical transition authority
- canonical control metadata derived from dispatcher logic

No legacy component may directly mutate canonical state.

---

## Read-only compatibility principle

Read-only compatibility is allowed in principle.

This means legacy runtime may receive derived information from canonical state, but only through a read-only boundary.

Allowed forms include:

- compatibility snapshot
- derived payload
- adapter output
- explicitly documented projection of canonical state

This boundary exists only to support migration compatibility.

It does not grant control authority.

---

## Forbidden reverse paths

The following are explicitly forbidden:

1. Legacy runtime writing directly into PROJECT_STATE.json
2. Legacy runtime modifying canonical phase values
3. Legacy runtime clearing or changing canonical halt state
4. Legacy runtime writing approval outcomes into canonical state
5. Legacy runtime mutating canonical dispatcher-owned metadata
6. Any indirect write-back path where legacy output is treated as canonical truth without dispatcher ownership
7. Any bridge that can overwrite canonical state from legacy-side execution results

In short:

- canonical may inform legacy
- legacy may not control canonical

---

## Source-of-truth rule

For migration v1, source of truth is explicit:

- canonical dispatcher owns canonical state
- compatibility outputs are derived artifacts only
- legacy runtime is downstream of canonical state, never upstream of it

If any implementation allows the reverse direction, that implementation contradicts migration policy.

---

## Write-path test

A path must be considered invalid if all three conditions are true:

1. it originates from legacy runtime execution
2. it can alter canonical state or canonical control decisions
3. it bypasses canonical dispatcher ownership

If all three are true, the path is forbidden.

---

## Allowed migration shape

Minimal safe migration shape for v1:

- input: canonical PROJECT_STATE.json
- processing: read + derive compatibility representation
- output: read-only legacy-facing payload

No reverse path is allowed.

No canonical write authority is delegated.

---

## M3 prepared criteria

M3 may be considered prepared only if all of the following are true:

1. The read-only boundary is explicitly documented
2. Forbidden write-back paths are explicitly documented
3. The source-of-truth rule is explicit
4. No migration document contradicts dispatcher authority
5. No documented bridge grants legacy write authority into canonical state

If any of these conditions fail, M3 is not prepared.

---

## Audit conclusion

For Migration v1:

- read-only compatibility is allowed in principle
- write-back from legacy runtime is forbidden
- canonical dispatcher remains the only valid control authority for canonical state

This is the required boundary condition for M3 preparation.
