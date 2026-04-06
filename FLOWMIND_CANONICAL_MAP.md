# FLOWMIND CANONICAL MAP

Status: FROZEN HISTORICAL DOCUMENT  
Branch: `cashflow-mode`

## Meaning

This document is preserved as a historical snapshot of the repository during the dual-system phase.

It is **not** the active canonical map of the system.

## Current truth

The repository is no longer operating under a dual-system model.

The active system is:

- one canonical dispatcher
- one control contour
- one state model (`PROJECT_STATE.json`)
- one command surface (`tools/dispatcher.sh`)

## Why this file is frozen

This map reflects an earlier state where:

- legacy runtime and canonical dispatcher coexisted
- main.py and dispatcher/engine.py were part of active control flow
- ExecutionManifest.json was still considered part of runtime logic
- migration thinking defined the architecture direction

That is no longer the current system model.

## What this file may still be used for

This file may be referenced only as:

- historical architecture context
- explanation of how the system evolved
- evidence of previous control-layer structure

## What this file must NOT be used for

Do not use this file as:

- current system map
- architectural source of truth
- decision reference for control-layer design
- justification for reintroducing legacy runtime logic

## Active Phase 2 rule

The repository is being cleaned toward:

- one control brain
- no parallel dispatcher logic
- no legacy control ambiguity
- no dual runtime model

## Final note

This file is frozen.

It does not describe the active system.
