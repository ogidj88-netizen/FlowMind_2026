# FLOWMIND TOPLEVEL CLASSIFICATION V1

## Purpose
This document defines the first top-level classification of the FlowMind_2026 repository.

It is based only on currently visible top-level structure.

This is a containment step, not a final deep audit.

---

## Top-level elements observed

Files:
- CANONICAL_DISPATCHER_SPEC.md
- FLOWMIND_ACTION_SEQUENCE_V1.md
- FLOWMIND_CANONICAL_MAP.md
- FLOWMIND_REPO_TRUST_BOUNDARY_V1.md
- FLOWMIND_SYSTEM_MAP_V1.md
- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_WORKING_TARGET.md
- main.py
- Makefile

Folders:
- adapters/
- cashflow/
- core_frozen/
- dispatcher/
- docs/
- engine/
- manifest_engine/
- production/
- projects/
- templates/
- tools/

---

## TRUSTED

### Trusted top-level guidance documents
The following are trusted as active recovery guidance:

- FLOWMIND_SYSTEM_MAP_V1.md
- FLOWMIND_ACTION_SEQUENCE_V1.md
- FLOWMIND_REPO_TRUST_BOUNDARY_V1.md
- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md

Reason:
- explicitly created in current recovery phase
- aligned with one working contour
- aligned with anti-chaos rules
- safe as current decision-support layer

---

## FROZEN LEGACY

### Explicitly frozen top-level folder
- core_frozen/

Reason:
- explicitly signals frozen historical zone
- must remain outside active authority unless deliberately reclassified later

Operational rule:
- readable for audit
- not allowed to guide active rebuild by default

---

## UNVERIFIED

### Unverified top-level files
- CANONICAL_DISPATCHER_SPEC.md
- FLOWMIND_CANONICAL_MAP.md
- FLOWMIND_WORKING_TARGET.md
- main.py
- Makefile

Reason:
- may contain useful information
- may contain historical or still-relevant structure
- current authority status is not yet confirmed in this recovery phase

Operational rule:
- do not treat as canonical authority yet
- review individually before use

### Unverified top-level folders
- adapters/
- cashflow/
- dispatcher/
- docs/
- engine/
- manifest_engine/
- production/
- projects/
- templates/
- tools/

Reason:
- names suggest importance, but names are not authority
- current role in one working contour is not yet formally confirmed
- each requires explicit review before trust is granted

Operational rule:
- no folder becomes trusted because it “looks central”
- no execution assumptions allowed before review

---

## Temporary interpretation

At this moment:

- trusted = current recovery documents only
- frozen legacy = core_frozen/
- unverified = all remaining top-level runtime/code/support structures

This is intentionally narrow and conservative.

It protects the active contour from accidental authority leakage.

---

## What this classification means operationally

Until further review:

1. active decisions may rely on trusted recovery documents
2. frozen legacy stays outside current authority
3. unverified code and folders are not to be assumed canonical
4. next trust expansion must happen by explicit classification, not intuition

---

## Known limitation

This classification is top-level only.

It does not yet determine:
- which specific files inside folders are trusted
- which runtime path is the active canonical path
- which implementation elements should enter the working contour first

That must be decided in the next review steps.

---

## Current next focus

Next after this file:

- review unverified top-level files first
- decide whether any of them should move to TRUSTED or FROZEN LEGACY
- only after that, begin folder-by-folder review
