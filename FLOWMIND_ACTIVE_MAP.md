# FLOWMIND ACTIVE MAP

Status: ACTIVE OPERATIONAL MAP
Project: FlowMind / Imagine What If
Mode: SYSTEM MAP MODE

## 1. Purpose

This file defines the current operational work map for FlowMind.

It does not define permanent product architecture.

It is subordinate to:

- 000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md
- verified product authority
- verified runtime evidence

Its purpose is to define:

- where we are now
- what current work is allowed
- what is forbidden
- what must be verified before implementation resumes
- when to stop

This file must not override newer verified repo or runtime evidence.

---

## 2. Product direction

High-level product intent:

- FLOWMIND_WORKING_TARGET.md

Detailed target architecture:

- FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

Interpretation:

FLOWMIND_WORKING_TARGET.md defines the product principles and optimization boundaries.

FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md defines the detailed destination architecture.

Neither document is runtime proof.

---

## 3. Current mode

Current mode:

SYSTEM MAP MODE

Current objective:

Audit and clean:

- Project Sources
- authority documents
- trust boundaries
- operational maps
- duplicated or stale "current next action" instructions

before production implementation resumes.

This authority/source audit temporarily takes priority over older implementation-next-action instructions.

---

## 4. Current step

Current step:

Authority and Project Sources reconciliation.

Goal:

Create one internally consistent authority chain so that a new ChatGPT conversation cannot accidentally resume stale work.

For every authority or Project Source file:

READ
→ VERIFY CONTENT
→ CHECK FRESHNESS
→ CHECK CONFLICTS
→ CLASSIFY
→ KEEP / REMOVE / UPDATE

Classification must be exactly one of:

- TRUSTED
- FROZEN LEGACY
- UNVERIFIED

---

## 5. Current verified findings

000_ACTIVE_FLOWMIND_PROJECT_INSTRUCTIONS.md

- TRUSTED
- controls ChatGPT operating discipline and anti-drift rules

FLOWMIND_WORKING_TARGET.md

- TRUSTED for high-level product intent and principles
- not the detailed current architecture specification
- not runtime proof

FLOWMIND_TARGET_ARCHITECTURE_V2_12_MODULES.md

- verified detailed target architecture
- 12-module target structure
- not runtime proof
- does not define current working state

CHAT_START_BLOCK_FLOWMIND_CURRENT.md

- stale as current operational authority
- useful as historical operational evidence until updated or retired
- old current-next-action instructions must not control current work

FLOWMIND_CURRENT_WORK_ANCHOR.md

- stale as current operational authority
- Director Brain preparation content remains historical evidence
- old current-next-action instructions must not control current work

Previous FLOWMIND_ACTIVE_MAP.md state

- stale repo/module-inventory current step
- stale pipeline wording
- old exit condition must not control current work

---

## 6. Allowed actions now

Allowed:

- read Project Sources
- read repo authority documents
- inspect file contents
- inspect git history
- inspect current runtime evidence
- classify documents
- update stale authority documents by full replacement
- remove legacy documents from active Project Sources
- synchronize verified authority files between GitHub and Project Sources
- run validation and preflight checks
- commit only after a meaningful audit block is complete

---

## 7. Forbidden actions now

Until the authority/source audit is complete:

- do not implement Director Brain
- do not tune final video quality
- do not change renderer behavior
- do not add YouTube upload
- do not add Telegram integration
- do not add TikTok crossposting
- do not add Pexels/Pixabay integration
- do not add new provider integrations
- do not rewrite dispatcher
- do not rewrite runner
- do not activate engine/module_runner.py
- do not execute engine/modules/*
- do not create a second runtime contour
- do not open upload gate
- do not approve upload
- do not trust stale "CURRENT", "ACTIVE", "FINAL", or "TRUSTED" labels without content verification
- do not resume an old next action merely because it exists in a historical document

---

## 8. Runtime truth rule

Architecture documents describe intent.

Runtime evidence proves implementation.

A runtime component is considered real only when supported by relevant evidence such as:

- implementation
- validation
- generated artifact
- downstream consumption
- runtime log
- reproducible behavior

Historical status documents are not runtime proof.

---

## 9. Operational document consolidation rule

FlowMind must not maintain multiple competing documents that all claim to define:

- where we are now
- what the current next action is
- what current work is allowed

During this audit:

- CHAT_START_BLOCK_FLOWMIND_CURRENT.md
- FLOWMIND_CURRENT_WORK_ANCHOR.md
- FLOWMIND_ACTIVE_MAP.md

must be reconciled.

Final objective:

one current operational authority for "where we are now".

Historical checkpoints may remain in the repository but must not compete with the active operational authority.

---

## 10. Stop rule

STOP if:

- authority documents materially conflict
- current source freshness is unknown
- a file cannot be read completely enough to verify
- an action would create a second runtime contour
- an action would reactivate legacy code
- production implementation is proposed before authority reconciliation is complete
- a file is treated as trusted only because of its filename or declared status
- the next action cannot be traced to the verified authority chain

Do not guess.

Obtain evidence first.

---

## 11. Exit condition

The authority/source audit is complete only when:

1. every active Project Source has been classified;
2. stale or legacy Sources have been removed or explicitly frozen;
3. product intent and detailed target architecture have distinct roles;
4. one operational document defines current work;
5. trust-boundary documents no longer conflict with verified authority;
6. Project Sources and GitHub authority files are synchronized;
7. no stale current-next-action instruction can override the verified current objective;
8. repo validation passes.

Only then may FlowMind resume production implementation.

---

## 12. One-step rule

Work proceeds:

one file
→ audit
→ verdict
→ KEEP / REMOVE / UPDATE
→ verify
→ next file

Commit only after a meaningful authority-audit block is complete.

No automatic jumping ahead.

End.
