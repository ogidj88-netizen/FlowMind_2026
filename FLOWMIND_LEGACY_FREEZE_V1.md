# FLOWMIND LEGACY FREEZE

Status: ACTIVE SYSTEM DECISION

## Decision

The station-based pipeline (S1–S10) is officially classified as:

- FROZEN LEGACY
- NON-CANONICAL
- NOT PART OF ACTIVE CONTROL CONTOUR

## Affected Areas

### Production Layer
- production/*

### Engine Legacy Modules
- engine/modules/*

### Legacy Core Guards
- engine/global_hard_gate_v1.py

## Rules

These components:

- MUST NOT be used in active runtime
- MUST NOT influence control-layer decisions
- MUST NOT be integrated into canonical dispatcher
- MAY be used only for historical reference

## Active System

The only valid system is:

- canonical dispatcher
- PROJECT_STATE.json
- validated state transitions
- single control contour

## Purpose

This freeze eliminates:

- dual runtime models
- station-based ambiguity
- migration-driven architecture

and enforces:

- one control brain
- one state model
- one execution path
