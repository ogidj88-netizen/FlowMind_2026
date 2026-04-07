# FLOWMIND REPO TRUST BOUNDARY V1

## Purpose
This document defines the repository trust boundary for FlowMind_2026.

It answers only one question:

Which parts of the repository are currently allowed to be treated as operationally trustworthy during baseline recovery?

This document is a trust map, not an implementation spec.

---

## Core rule

Historical presence does not equal architectural authority.

A file or folder is not trusted because:
- it exists
- it once worked
- it looks important
- it was part of an older plan
- it was used during migration discussions

A file or folder is trusted only if it is:
- aligned with the current canonical direction
- not contradicted by locked system rules
- usable without reintroducing ambiguity
- suitable for one working contour recovery

---

## Trust classes

### 1. TRUSTED
Definition:
- may be used as active reference during rebuild
- may influence current recovery decisions
- is compatible with canonical direction

### 2. FROZEN LEGACY
Definition:
- may be read for historical context
- must not define current architecture
- must not silently regain authority

### 3. UNVERIFIED
Definition:
- exists in repo, but trust is not yet granted
- cannot be used as authority
- requires explicit review before use

---

## Repository trust policy

### Trusted zone
Currently trusted at policy level:

- canonical map documents
- action sequence documents
- canonical rules already locked in current recovery direction
- documents that reinforce one working contour and one authority model

Examples of trusted document intent:
- system map
- action order
- canonical boundary rules
- authority rules
- state ownership rules

Trusted does not automatically mean runtime-ready.
It means safe to use as decision support.

---

### Frozen legacy zone
Frozen legacy includes:

- older runtime paths that were part of previous architectures
- migration-era materials that no longer define active work
- duplicated structures from earlier design stages
- documents or modules tied to abandoned or paused directions
- anything that implies parallel authority or parallel control contours

Frozen legacy may be used only for:
- audit
- comparison
- extracting lessons
- identifying what must stay outside the active contour

Frozen legacy must not:
- define current execution order
- redefine state ownership
- become hidden dependency for current rebuild
- regain write authority

---

### Unverified zone
Unverified includes:

- files/folders not yet reviewed in the current recovery process
- ambiguous utilities
- unclear adapters
- unclear runners
- unclear scripts with uncertain authority implications
- anything that may look useful but has not passed trust review

Unverified must be treated as unsafe by default.

---

## Decision rules

A repo element may enter TRUSTED only if:

1. its role is explicit
2. its authority level is explicit
3. it does not create dual control
4. it does not conflict with one working contour
5. it reduces ambiguity rather than adding “maybe useful” complexity

If any of the above is missing, the element stays UNVERIFIED or FROZEN LEGACY.

---

## Immediate operational interpretation

For the current recovery phase:

- trusted = current canonical guidance documents
- frozen legacy = historical architecture and legacy runtime authority paths
- unverified = everything not explicitly trusted yet

This is intentionally strict.

Strictness is preferred over accidental contamination of the active contour.

---

## What this document does not do

This document does not:
- approve all current code
- approve all current scripts
- declare runtime readiness
- replace technical audits
- replace dispatcher validation
- replace state authority validation

It only defines the trust boundary.

---

## Exit condition

This document is useful only if it changes behavior.

That means after locking this file:

- trusted materials are used intentionally
- frozen legacy is kept outside active authority
- unverified parts are reviewed before use
- no repo element gains authority by accident

If behavior does not change, this document is incomplete in practice.

---

## Current next focus

After locking Repo Trust Boundary V1, the next action is:

- define the first concrete trusted boundary list
- identify which files/folders are inside active recovery
- identify which files/folders are frozen outside the contour
