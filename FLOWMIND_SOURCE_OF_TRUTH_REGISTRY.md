# FLOWMIND SOURCE OF TRUTH REGISTRY

Status: ACTIVE INDEX
Authority: Subordinate to FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md

## Purpose

This file is an operational index of document authority.

It does not replace FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md.

The trusted boundary file remains the higher authority for deciding what is trusted, frozen, or unverified.

## Authority Rule

Primary authority:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md

This registry must not contradict the trusted boundary list.

If this registry and the trusted boundary list disagree, the trusted boundary list wins.

## Status Model

This registry uses the same trust model as the trusted boundary list:

- TRUSTED
- FROZEN LEGACY
- UNVERIFIED

No separate authority model is allowed here.

## Active Truth

FlowMind is a niche-driven media intelligence and production system.

FlowMind receives input parameters such as niche, language, format, audience, style, allowed sources, and business goal.

FlowMind analyzes validated sources, competitors, YouTube, Reddit, and other signals to identify under-covered or poorly covered content opportunities.

Production comes after topic validation.

FlowMind is not a horror-content system.

Imagine What If is not equal to FlowMind Core.

A channel, niche, or style config must not be treated as FlowMind Core.

## Current Document Index

| Document | Status | Rule |
|---|---:|---|
| FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md | TRUSTED | Primary authority for trust boundaries. |
| FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md | TRUSTED | Operational index only; subordinate to trusted boundary list. |
| FLOWMIND_SYSTEM_MAP_V1.md | TRUSTED | Active recovery guidance. |
| FLOWMIND_ACTION_SEQUENCE_V1.md | TRUSTED | Active recovery sequence guidance. |
| FLOWMIND_REPO_TRUST_BOUNDARY_V1.md | TRUSTED | Repo trust boundary guidance. |
| docs/FLOWMIND_HARD_RULESET_V1.md | TRUSTED | Work discipline and decision behavior. |
| docs/FLOWMIND_WORK_PROTOCOL_V1.md | TRUSTED | Work protocol for Evgen and ChatGPT. |
| CANONICAL_DISPATCHER_SPEC.md | TRUSTED | Trusted as control-policy and architectural-alignment document. Not automatic proof that every referenced implementation is valid. |
| FLOWMIND_WORKING_TARGET.md | TRUSTED | Trusted only as target-shape and system-intent guidance. Not trusted as proof of implemented runtime. |
| main.py | TRUSTED | Trusted only as blocking tombstone for retired legacy entrypoint. Not an active runtime launcher. |
| cashflow/topic_intelligence/niche_profile_schema.json | TRUSTED | Niche profile structure. |
| cashflow/topic_intelligence/profiles/debt_trap_us_v1.json | TRUSTED | Reviewed niche profile example. |
| cashflow/topic_intelligence/profiles/hidden_fees_us_v1.json | TRUSTED | Reviewed niche profile example. |
| cashflow/topic_intelligence/profiles/finance_legacy_v1.json | UNVERIFIED | Must be reviewed before use. |
| FLOWMIND_CANONICAL_MAP.md | FROZEN LEGACY | Historical dual-system snapshot only. Must not guide current architecture. |
| MASTER_PROMPTS_v2_FULL.txt | FROZEN LEGACY | External/old prompt artifact. Not valid as repo truth. |
| IronCore v3.5 references | FROZEN LEGACY | Historical context only unless explicitly re-approved. |
| Imagine What If horror rules | UNVERIFIED | May become niche/style config only after review. Not FlowMind Core. |

## Docs Index — TRUSTED

| Document | Status | Rule |
|---|---:|---|
| docs/BOOTSTRAP_AUDIT_V1.md | TRUSTED | Bootstrap/init audit checkpoint. Trusted as review evidence, not redesign plan. |
| docs/CANONICAL_DISPATCHER_ENTRYPOINTS.md | TRUSTED | Locked canonical dispatcher entrypoint decision. |
| docs/CANONICAL_ENTRYPOINT_DECISION_V1.md | TRUSTED | Active control-layer entrypoint decision. |
| docs/CANONICAL_MANIFEST_SPEC.md | TRUSTED | Canonical manifest/state contract. |
| docs/CONTROL_LAYER_AUDIT_V1.md | TRUSTED | Control-layer audit verdict for one active contour. |
| docs/DISPATCHER_CHEAT_SHEET.md | TRUSTED | Operational cheat sheet for canonical dispatcher commands. |
| docs/DISPATCHER_ENGINE_STATUS.md | TRUSTED | Audit truth for retired dispatcher/engine.py legacy tombstone. |
| docs/DISPATCHER_ENTRYPOINT.md | TRUSTED | Active dispatcher command-surface truth. |
| docs/FLOWMIND_HARD_RULESET_V1.md | TRUSTED | Work discipline and decision behavior. |
| docs/FLOWMIND_WORK_PROTOCOL_V1.md | TRUSTED | Cooperation protocol for FlowMind work. |
| docs/INTEGRATION_AUDIT_V1.md | TRUSTED | Integration audit checkpoint for legacy/canonical separation. |
| docs/MAIN_PY_STATUS.md | TRUSTED | Audit truth for main.py retired legacy tombstone. |
| docs/PHASE2_AUDIT_STANDARD.md | TRUSTED | Audit standard for cleanup and one-contour recovery. |
| docs/RUNTIME_AUDIT_V1.md | TRUSTED | Runtime audit checkpoint for canonical state-control layer. |

## Docs Index — FROZEN LEGACY

| Document | Status | Rule |
|---|---:|---|
| docs/COMPAT_ADAPTER_SMOKE_CHECK_V1.md | FROZEN LEGACY | Historical compatibility adapter smoke note. Not active execution path. |
| docs/MIGRATION_ROADMAP_V1.md | FROZEN LEGACY | Historical migration roadmap. Not current cleanup strategy. |
| docs/READ_ONLY_ADAPTER_USAGE_V1.md | FROZEN LEGACY | Historical read-only adapter usage note. Not active adapter work. |
| docs/READ_ONLY_COMPATIBILITY_BRIDGE.md | FROZEN LEGACY | Historical compatibility bridge plan. Not active implementation plan. |

## Docs Index — UNVERIFIED

| Document | Status | Rule |
|---|---:|---|
| docs/FLOWMIND_6_CORE_ENGINES_CONTRACTS_V1.md | UNVERIFIED | Production architecture claim. Must not guide implementation until reviewed against current FlowMind Core. |
| docs/FLOWMIND_CANONICAL_ARCHITECTURE_V1.md | UNVERIFIED | Contains possible outdated scope. Must not guide decisions until reviewed. |
| docs/FLOWMIND_DIRECTOR_ENGINE_V1.md | UNVERIFIED | Creative/production engine specification. Must not guide current architecture until reviewed. |
| docs/FLOWMIND_SHOT_SCHEMA_V1.md | UNVERIFIED | Shot/visual production schema. Must not guide current architecture until reviewed. |
| docs/LEGACY_TO_CANONICAL_PHASE_MAPPING.md | UNVERIFIED | Migration mapping document. Must not guide current architecture until reviewed. |
| docs/M3_BOUNDARY_AUDIT.md | UNVERIFIED | Migration boundary audit. Must not guide active cleanup until reviewed. |
| docs/M4_READ_ONLY_ADAPTER_CONTRACT.md | UNVERIFIED | Migration adapter contract. Must not guide active cleanup until reviewed. |
| docs/M5_ADAPTER_NON_AUTHORITY_RULE.md | UNVERIFIED | Migration adapter rule. Must not guide active cleanup until reviewed. |
| docs/M6_LEGACY_READ_SCOPE_RULE.md | UNVERIFIED | Migration adapter read-scope rule. Must not guide active cleanup until reviewed. |
| docs/M7_ADAPTER_VERSIONING_RULE.md | UNVERIFIED | Migration adapter versioning rule. Must not guide active cleanup until reviewed. |
| docs/M8_ADAPTER_FAIL_CLOSED_RULE.md | UNVERIFIED | Migration adapter fail-closed rule. Must not guide active cleanup until reviewed. |
| docs/M9_ADAPTER_REQUIRED_FIELDS_RULE.md | UNVERIFIED | Migration adapter required-fields rule. Must not guide active cleanup until reviewed. |
| docs/MIGRATION_ADAPTER_PACK_SUMMARY.md | UNVERIFIED | Migration adapter summary. Must not guide active cleanup until reviewed. |
| docs/MIGRATION_STATUS_V1.md | UNVERIFIED | Migration status document. Must not guide active cleanup until reviewed. |

## Prohibitions

Do not treat unlisted files as trusted.

Do not treat unverified files as architecture.

Do not treat frozen legacy as active guidance.

Do not treat a channel, niche, or style config as equal to FlowMind Core.

Do not delete files before runtime reference check.
