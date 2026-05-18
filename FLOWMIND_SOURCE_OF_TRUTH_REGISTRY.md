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
| CANONICAL_DISPATCHER_SPEC.md | TRUSTED | Trusted as control-policy and architectural-alignment document. Not automatic proof that every referenced implementation is valid. |
| FLOWMIND_WORKING_TARGET.md | TRUSTED | Trusted only as target-shape and system-intent guidance. Not trusted as proof of implemented runtime. |
| main.py | TRUSTED | Trusted only as blocking tombstone for retired legacy entrypoint. Not an active runtime launcher. |
| cashflow/topic_intelligence/niche_profile_schema.json | TRUSTED | Niche profile structure. |
| cashflow/topic_intelligence/profiles/debt_trap_us_v1.json | TRUSTED | Reviewed niche profile example. |
| cashflow/topic_intelligence/profiles/hidden_fees_us_v1.json | TRUSTED | Reviewed niche profile example. |
| cashflow/topic_intelligence/profiles/finance_legacy_v1.json | UNVERIFIED | Must be reviewed before use. |
| docs/FLOWMIND_CANONICAL_ARCHITECTURE_V1.md | UNVERIFIED | Contains possible outdated scope. Must not guide decisions until reviewed. |
| FLOWMIND_CANONICAL_MAP.md | FROZEN LEGACY | Historical dual-system snapshot only. Must not guide current architecture. |
| MASTER_PROMPTS_v2_FULL.txt | FROZEN LEGACY | External/old prompt artifact. Not valid as repo truth. |
| IronCore v3.5 references | FROZEN LEGACY | Historical context only unless explicitly re-approved. |
| Imagine What If horror rules | UNVERIFIED | May become niche/style config only after review. Not FlowMind Core. |

## Prohibitions

Do not treat unlisted files as trusted.

Do not treat unverified files as architecture.

Do not treat frozen legacy as active guidance.

Do not treat a channel, niche, or style config as equal to FlowMind Core.

Do not delete files before runtime reference check.
