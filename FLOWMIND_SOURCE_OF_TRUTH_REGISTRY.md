# FLOWMIND_SOURCE_OF_TRUTH_REGISTRY

Status: ACTIVE
Purpose: Defines which documents are allowed to guide FlowMind decisions.

## Core Rule

Any document not listed here has no architectural authority.

A file may exist in the repository without being allowed to guide current FlowMind decisions.

## Status Definitions

### ACTIVE
Current source of truth. Can guide architecture, implementation, and decisions.

### REVIEW
Potentially useful, but must not guide decisions until re-approved.

### DONOR
Can provide ideas or historical reasoning, but cannot define active architecture.

### ARCHIVE
Historical context only. Cannot guide current decisions.

### DELETE_CANDIDATE
Candidate for removal after runtime reference check.

## Active Truth

FlowMind is a niche-driven media intelligence and production system.

FlowMind receives input parameters such as niche, language, format, audience, style, allowed sources, and business goal.

FlowMind analyzes validated sources, competitors, YouTube, Reddit, and other signals to identify under-covered or poorly covered content opportunities.

Production comes after topic validation.

FlowMind is not a horror-content system.

Imagine What If is not equal to FlowMind Core.

## Current Registry

| Document | Status | Rule |
|---|---:|---|
| FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md | ACTIVE | Governs document authority. |
| docs/FLOWMIND_HARD_RULESET_V1.md | ACTIVE | Governs work discipline and decision behavior. |
| cashflow/topic_intelligence/niche_profile_schema.json | ACTIVE | Defines niche profile structure. |
| cashflow/topic_intelligence/profiles/debt_trap_us_v1.json | ACTIVE | Active niche profile example. |
| cashflow/topic_intelligence/profiles/hidden_fees_us_v1.json | ACTIVE | Active niche profile example. |
| cashflow/topic_intelligence/profiles/finance_legacy_v1.json | REVIEW | Must be reviewed before use. |
| docs/FLOWMIND_CANONICAL_ARCHITECTURE_V1.md | REVIEW | Contains possible outdated scope. Must not guide decisions until re-approved. |
| FLOWMIND_WORKING_TARGET.md | REVIEW | Contains possible outdated crossposting scope. Must not guide decisions until re-approved. |
| MASTER_PROMPTS_v2_FULL.txt | ARCHIVE | External/old prompt artifact. Not valid as repo truth. |
| IronCore v3.5 references | ARCHIVE | Historical context only unless explicitly re-approved. |
| Imagine What If horror rules | DONOR | Allowed only as niche/style config, not FlowMind Core. |

## Active Prohibitions

Do not treat unlisted files as architectural authority.

Do not use archive or review files to define FlowMind Core.

Do not treat a channel, niche, or style config as equal to FlowMind Core.

Do not build automation before the active system boundary is clear.

Do not delete files before runtime reference check.
