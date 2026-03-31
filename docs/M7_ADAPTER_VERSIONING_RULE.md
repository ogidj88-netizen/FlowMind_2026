# M7 Adapter Versioning Rule

## Purpose

This document defines the versioning rule for the read-only compatibility adapter in Migration v1.

The goal is to prevent silent compatibility breakage when adapter payload structure changes.

---

## Core rule

The compatibility adapter must be versioned explicitly.

Compatibility payload structure must not change silently.

If compatibility shape changes, the version identifier must change with it.

---

## Why versioning is required

Without explicit versioning, legacy runtime may:

- assume an older payload shape still exists
- misread fields after compatibility changes
- silently depend on removed or renamed fields
- produce invalid downstream behavior without obvious failure

This creates migration instability.

---

## Minimum requirement

For Migration v1, compatibility output must have an explicit adapter version identifier.

Examples of acceptable forms include:

- `adapter_version`
- `compat_version`
- documented version header in the derived artifact

The specific implementation form may be chosen later.

The rule itself is mandatory now.

---

## Change rule

A version change is required if any of the following happens:

1. allowed fields are added
2. allowed fields are removed
3. field meaning changes
4. field naming changes
5. output interpretation changes
6. compatibility contract behavior changes

No structural change may be treated as invisible.

---

## Legacy expectation rule

Legacy runtime must not assume unversioned compatibility stability.

Legacy runtime may rely only on:

- documented compatibility scope
- documented field meanings
- explicit adapter version semantics

---

## Non-goals

This document does not define:

- semantic versioning format
- implementation code
- automatic migration tooling
- bidirectional negotiation

Those decisions may come later.

---

## Migration v1 statement

For Migration v1:

- adapter compatibility must be explicit
- versioning must be explicit
- silent contract drift is forbidden

---

## Acceptance condition for M7

M7 may be considered prepared on docs level only if:

1. explicit versioning is required
2. silent payload drift is explicitly forbidden
3. change triggers are explicitly listed
4. legacy reliance on unversioned stability is explicitly denied

---

## Final statement

A compatibility adapter without explicit versioning is not a stable migration boundary.

Versioning is required to keep compatibility narrow, predictable, and auditable.
