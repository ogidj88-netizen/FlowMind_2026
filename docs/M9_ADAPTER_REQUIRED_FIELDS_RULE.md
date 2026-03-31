# M9 Adapter Required Fields Rule

## Purpose

This document defines the required-field rule for the read-only compatibility adapter in Migration v1.

The goal is to prevent ambiguity about which compatibility fields are mandatory for a valid adapter payload.

---

## Core rule

A compatibility payload is valid only if all required fields are present and interpretable.

Missing required fields make the payload invalid.

Invalid payload must not be treated as usable compatibility data.

---

## Required fields

For Migration v1, the following fields are required for adapter validity:

- `adapter_version`
- `project_id`
- `phase`
- `halted`
- `approval_status`
- `approved_for_upload`
- `mode`
- `updated_at`

These fields are mandatory for compatibility validation.

---

## Optional field rule

`halt_reason` may be present when relevant, but it must not be treated as universally required.

Optional fields must not be reinterpreted as silently required.

Required fields must not be downgraded into optional convenience fields.

---

## Interpretation rule

Presence alone is not enough.

A required field must also be interpretable within documented compatibility meaning.

Examples:

- `adapter_version` must identify a supported compatibility version
- `project_id` must identify the compatibility target
- `phase` must be readable as a documented compatibility phase value
- `halted` must be readable as halt visibility
- `approval_status` must be readable as approval visibility
- `approved_for_upload` must be readable as gate visibility
- `mode` must be readable as compatibility-visible execution mode
- `updated_at` must be readable as freshness metadata

---

## Invalidity rule

Payload must be considered invalid if any required field is:

- missing
- structurally malformed
- semantically uninterpretable
- present under undocumented naming
- replaced by guessed substitute meaning

---

## Migration v1 statement

For Migration v1:

- required compatibility fields must be explicit
- optional fields must remain optional
- validity requires both presence and interpretability

---

## Acceptance condition for M9

M9 may be considered prepared on docs level only if:

1. required fields are explicitly listed
2. optional fields are explicitly separated
3. interpretability is required, not just presence
4. invalidity conditions are explicitly listed

---

## Final statement

Compatibility safety requires explicit required fields.

If required fields are not defined, compatibility validity becomes guesswork.
