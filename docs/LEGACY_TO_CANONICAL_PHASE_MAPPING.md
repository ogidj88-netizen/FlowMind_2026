# LEGACY TO CANONICAL PHASE MAPPING

Status: DRAFT-LOCK
Branch: cashflow-mode

## Purpose

This file defines the current working mapping between the legacy runtime flow and the new canonical dispatcher flow.

Important:
- this is a migration planning document
- this is not a claim that migration is already implemented
- this is not permission to mix legacy and canonical runtime logic

## Systems being mapped

Legacy runtime flow:
- CREATED
- S1_DONE
- S2_DONE
- S5_DONE
- S6_DONE
- S7_DONE
- S8_DONE
- S9_DONE
- S10_DONE

Canonical dispatcher flow:
- TOPIC
- SCRIPT
- SCENES
- ASSETS
- ASSEMBLY
- QA
- READY_FOR_UPLOAD
- UPLOADED
- ARCHIVED
- HALT

## Mapping table

| Legacy phase | Canonical phase | Confidence | Migration note |
| --- | --- | --- | --- |
| CREATED | TOPIC | HIGH | Both represent initial project state before downstream execution. |
| S1_DONE | TOPIC | MEDIUM | Legacy S1 is strategy-oriented and is closer to topic/strategy definition than to full script generation. |
| S2_DONE | SCRIPT | HIGH | Legacy S2 produces script outline data and is the closest verified equivalent to canonical SCRIPT. |
| S5_DONE | ASSETS | HIGH | Legacy S5 assets output aligns most closely with canonical assets stage. |
| S6_DONE | ASSEMBLY | MEDIUM | Legacy S6 visual work appears upstream of canonical assembly, but old/new granularity may differ. |
| S7_DONE | ASSEMBLY | LOW | Legacy S7 audio may be folded into canonical assembly flow, but this is not a clean 1:1 mapping yet. |
| S8_DONE | QA | LOW | Legacy S8 looks assembly-related by naming, but there is not enough verified code evidence to claim a clean QA mapping. |
| S9_DONE | READY_FOR_UPLOAD | MEDIUM | Legacy S9 is not yet verified from a live module, so pre-upload alignment remains plausible but unproven. |
| S10_DONE | UPLOADED | MEDIUM | Legacy S10 appears final, but archival semantics remain unresolved. |

## Non-1:1 areas

1. S1_DONE -> TOPIC
Reason:
Legacy S1 is strategy-heavy and does not yet look like full canonical SCRIPT output.

2. S2_DONE -> SCRIPT
Reason:
Legacy S2 produces script outline structure, which is closer to canonical SCRIPT than to SCENES.

3. SCENES has no clean legacy equivalent yet
Reason:
Canonical dispatcher separates scene planning more explicitly than the legacy layer.

4. S6_DONE / S7_DONE -> ASSEMBLY
Reason:
Legacy visual/audio phases may collapse into one canonical assembly zone.

5. S8_DONE -> QA
Reason:
The current repo audit did not confirm a live legacy S8 module in engine/modules, so this mapping remains weak.

6. S9_DONE -> READY_FOR_UPLOAD
Reason:
The current repo audit did not confirm a live legacy S9 module in engine/modules, so this mapping remains provisional.

7. S10_DONE -> UPLOADED or ARCHIVED
Reason:
Canonical flow distinguishes UPLOADED and ARCHIVED, while legacy finality may not.

## Current migration interpretation

Working assumption for planning only:

- CREATED starts the canonical path at TOPIC
- legacy S1 remains closest to strategy/topic definition
- legacy S2 is closest to canonical SCRIPT
- canonical SCENES currently has no clean legacy 1:1 equivalent
- legacy asset/visual/audio production compresses into ASSETS -> ASSEMBLY
- legacy late-stage flow after assembly is still partially unresolved
- ARCHIVED remains canonical-only for now
- HALT remains canonical-only for now

## What is not mapped yet

These canonical states do not yet have clean legacy equivalents:

- SCENES
- HALT
- ARCHIVED

These should currently be treated as canonical-only states or states without a verified clean legacy match.

## Migration rule

Until this mapping is upgraded from DRAFT-LOCK to LOCKED:

- do not implement automated phase translation
- do not rewrite legacy runtime against this table
- do not claim 1:1 compatibility
- do not use this document as a direct execution contract

## Next validation targets

Before this mapping can become LOCKED, we still need:

1. verify whether S6 + S7 should merge into canonical ASSEMBLY
2. verify what legacy S8 actually produces in runtime practice
3. verify what legacy S9 actually produces in runtime practice
4. verify whether S10_DONE means UPLOADED only, or UPLOADED + ARCHIVED semantics
5. decide whether canonical SCENES should stay canonical-only in migration v1

## Current decision

This document is the official working draft for migration planning.

It is allowed for:
- architectural reasoning
- migration planning
- risk analysis

It is not allowed for:
- direct runtime switching
- direct code rewiring
- automatic bridging without further validation
