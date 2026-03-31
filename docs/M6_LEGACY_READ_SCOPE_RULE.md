# M6 Legacy Read Scope Rule

## Purpose

This document defines the allowed read scope for legacy runtime during Migration v1.

The goal is to prevent legacy runtime from depending directly on canonical internal state structures.

---

## Core rule

Legacy runtime must consume compatibility data through the read-only adapter boundary.

Legacy runtime must not treat canonical internal structures as its direct read surface.

---

## Allowed read model

For Migration v1, legacy runtime may read only:

- documented adapter output
- explicitly approved compatibility projections
- read-only derived artifacts produced for migration compatibility

This read model must be interpreted narrowly.

---

## Forbidden read model

Legacy runtime must not directly depend on:

- canonical internal transition metadata
- dispatcher-owned internal guards
- canonical retry internals
- canonical override internals
- undocumented PROJECT_STATE.json internals
- any canonical field not explicitly exposed through approved compatibility documentation

---

## Why this rule exists

If legacy runtime reads canonical internals directly, then migration creates hidden coupling.

Hidden coupling causes:

- unstable migration boundaries
- accidental dependency on dispatcher internals
- future breakage when canonical state evolves
- false assumptions about legacy compatibility guarantees

---

## Boundary interpretation

The adapter boundary is not only a write barrier.

It is also a read-scope barrier.

This means:

- canonical may expose selected derived compatibility data
- legacy may not freely inspect canonical internals just because they exist

---

## Migration v1 statement

For Migration v1:

- canonical dispatcher owns state
- adapter defines compatibility visibility
- legacy runtime reads through approved compatibility scope only
- undocumented direct reads are invalid migration behavior

---

## Acceptance condition for M6

M6 may be considered prepared on docs level only if:

1. direct legacy reads of canonical internals are explicitly forbidden
2. approved read scope is explicitly limited to adapter/projection outputs
3. hidden coupling risk is explicitly documented
4. read boundary is defined as part of migration safety

---

## Final statement

Migration safety requires both:

- no write-back from legacy into canonical state
- no uncontrolled direct read dependency from legacy into canonical internals

Both boundaries are required.
