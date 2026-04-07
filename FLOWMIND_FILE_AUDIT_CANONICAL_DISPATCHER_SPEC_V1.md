# FLOWMIND FILE AUDIT — CANONICAL DISPATCHER SPEC V1

## File
CANONICAL_DISPATCHER_SPEC.md

## Audit result
Classification: TRUSTED

## Trust scope
This file is trusted as a control-policy and architectural-alignment document.

It is not trusted as automatic proof that every referenced implementation file is currently valid, canonical, or production-ready.

---

## Why this file is trusted

The document strongly aligns with the current recovery direction:

- one active control brain
- one active state authority
- one canonical phase model
- explicit rejection of legacy control ambiguity
- explicit rejection of parallel control logic
- explicit separation from legacy dispatcher paths

This reduces ambiguity and supports one working contour.

---

## Why trust is scope-limited

This document names specific implementation files as active control core and active entrypoints:

- engine/canonical_dispatcher.py
- engine/state_validator.py
- engine/state_store.py
- tools/dispatcher.sh
- tools/dispatcher_cli.py
- tools/check_dispatcher.sh

Those implementation paths are not granted trust automatically by this document alone.

They still require direct audit.

---

## Operational interpretation

Allowed:
- use this file as policy guidance
- use this file as control-layer intent reference
- use this file to reject legacy dispatcher ambiguity
- use this file as evidence for one-control-brain rule

Not allowed:
- assume all referenced code is canonical without review
- treat named implementation files as trusted automatically
- treat document claims as runtime proof
- expand trusted runtime contour without direct audit

---

## Practical classification

Final classification for current recovery phase:

- file status: TRUSTED
- trust scope: POLICY / ARCHITECTURE
- implementation authority: NOT YET VERIFIED

---

## Effect on repo handling

After this audit:

- CANONICAL_DISPATCHER_SPEC.md moves from UNVERIFIED to TRUSTED
- referenced runtime files remain UNVERIFIED until individually reviewed
- legacy dispatcher paths remain outside active authority unless explicitly reclassified

---

## Next review target

Next file to review after this audit:

FLOWMIND_CANONICAL_MAP.md
