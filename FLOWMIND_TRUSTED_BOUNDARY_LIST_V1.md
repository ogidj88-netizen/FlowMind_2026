# FLOWMIND TRUSTED BOUNDARY LIST V1

## Purpose
This document defines the first concrete trusted boundary list for FlowMind_2026.

It translates trust policy into operational use.

This file answers:

- what is inside the active recovery contour
- what is outside as frozen legacy
- what remains unverified until reviewed

---

## Core rule

Only explicitly listed elements may be treated as trusted during current recovery.

If an element is not listed as trusted here, it is not trusted by default.

Historical importance does not override this rule.

---

## Trusted now — active recovery contour

### Root-level canonical guidance documents
These are trusted as active recovery guidance:

- FLOWMIND_SYSTEM_MAP_V1.md
- FLOWMIND_ACTION_SEQUENCE_V1.md
- FLOWMIND_REPO_TRUST_BOUNDARY_V1.md
- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md

Reason:
- they define the current canonical direction
- they reduce ambiguity
- they support one working contour
- they do not create runtime authority conflicts

---

## Trusted now — policy intent only

The following categories are trusted only at the policy level, not automatically as runnable implementation:

- canonical state ownership rules
- dispatcher authority rules
- read-only legacy boundary rules
- anti-dual-control rules
- one-entry-point rules

Important:
Trust at policy level does not mean every related implementation file is already trusted.
Implementation trust must still be earned explicitly.

---

## Frozen outside the active contour

The following are frozen outside the active contour until explicitly reintroduced by review:

- legacy runtime authority paths
- migration-era active rebuild directions
- duplicated orchestration logic
- any module or script that implies a second control center
- any runtime path that can mutate state outside the canonical authority model
- any historical structure preserved only for audit or reference

Operational meaning:
- may be read
- may be analyzed
- must not guide current rebuild by default
- must not silently regain execution authority

---

## Unverified by default

The following remain unverified until reviewed one by one:

- code folders not yet audited in current recovery phase
- scripts not yet classified by authority
- adapters not yet classified by authority
- runners not yet classified by authority
- utilities with unclear scope
- docs that may contain historical value but unclear current authority

Operational meaning:
- do not trust by assumption
- do not execute by habit
- do not use as authority
- review first, then classify

---

## What is trusted right now in practice

Trusted in practice right now:

1. current canonical recovery documents
2. the one-contour rebuild direction
3. the rule that legacy has no automatic authority
4. the rule that unreviewed repo elements stay unverified

This is intentionally narrow.

Narrow trust is safer than false clarity.

---

## What is not trusted right now in practice

Not trusted right now in practice:

- broad legacy runtime as active authority
- any undocumented control path
- any hidden entrypoint
- any script with unclear architectural role
- any folder assumed to be important only because it exists
- any implementation path not yet reviewed in the current recovery process

---

## Classification rule for the next steps

Each repo element reviewed later must be assigned to exactly one class:

- TRUSTED
- FROZEN LEGACY
- UNVERIFIED

No element may remain “implicitly trusted”.

---

## Exit condition

This document is considered operational only if it changes how the repo is handled.

That means:

- current work uses only explicitly trusted guidance
- frozen elements stay outside active authority
- unverified elements are reviewed before use
- no code or script is treated as canonical by accident

---

## Current next focus

Next after this file:

- inspect actual top-level repo structure
- classify first real folders/files into:
  - trusted
  - frozen legacy
  - unverified
