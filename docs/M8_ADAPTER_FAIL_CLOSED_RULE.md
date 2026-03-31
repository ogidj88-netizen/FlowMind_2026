# M8 Adapter Fail-Closed Rule

## Purpose

This document defines the fail-closed rule for the read-only compatibility adapter in Migration v1.

The goal is to prevent unsafe fallback behavior when compatibility payload is missing, malformed, incomplete, or unsupported.

---

## Core rule

If adapter compatibility data is invalid, unsupported, missing, or ambiguous, legacy runtime must fail closed.

It must not invent compatibility.

It must not assume missing fields.

It must not silently continue as if compatibility were valid.

---

## Fail-closed triggers

Legacy runtime must fail closed if any of the following is true:

1. adapter payload is missing
2. adapter version is missing
3. adapter version is unsupported
4. required compatibility fields are missing
5. payload structure is malformed
6. field meanings are ambiguous
7. compatibility data contradicts canonical expectations

---

## Forbidden fallback behavior

The following behaviors are forbidden:

- guessing missing field values
- defaulting silently into assumed compatibility mode
- treating partial payload as valid enough
- inferring undocumented meanings from nearby fields
- continuing operation on unknown adapter versions
- reconstructing compatibility state from canonical internals outside approved scope

---

## Safe behavior rule

Allowed safe behavior includes:

- halting compatibility-dependent legacy behavior
- marking compatibility as invalid
- surfacing explicit error state
- requiring documented compatibility correction
- refusing unsupported adapter versions

---

## Migration v1 statement

For Migration v1:

- compatibility must be explicit
- compatibility must be valid
- unsupported compatibility must fail closed
- silent fallback is forbidden

---

## Acceptance condition for M8

M8 may be considered prepared on docs level only if:

1. fail-closed behavior is explicit
2. silent fallback is explicitly forbidden
3. invalid and unsupported payload conditions are explicitly listed
4. safe halt/error behavior is explicitly allowed

---

## Final statement

A migration adapter is safe only if invalid compatibility leads to controlled refusal, not silent continuation.

Fail closed is required.
