# FLOWMIND_MAP_GUARD_V1

Status: TRUSTED OPERATIONAL GUARD
Mode after creation: SYSTEM MAP MODE

## Purpose

Prevent FlowMind work from drifting away from the active programming map.

No code, file change, renderer change, module change, provider integration, or video-quality tuning is allowed before a visible map check.

## Required MAP CHECK

Before every technical answer, the assistant must show:

MAP CHECK
Active map:
Current step:
Allowed action:
Forbidden action:
Evidence:
Verdict:

If the assistant cannot fill this block clearly, the assistant must stop.

## Active map sources

Use these files as map authority when present:

- FLOWMIND_ACTION_SEQUENCE_V1.md
- FLOWMIND_SYSTEM_MAP_V1.md
- FLOWMIND_CANONICAL_STRUCTURE.md
- FLOWMIND_REPO_TRUST_BOUNDARY_V1.md
- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- docs/MIGRATION_ROADMAP_V1.md
- docs/READ_ONLY_COMPATIBILITY_BRIDGE.md

If authority is unclear, do not guess.

Say:

STOP: map alignment required.
Reason:
Next safe action:

## Current default

Current mode: SYSTEM MAP MODE

Current objective:
Re-align with the active programming map before more production coding.

Current forbidden action:
Do not continue video-quality tuning until skeleton, module sequence, gates, and active runtime contour are reviewed.

## Work modes

SYSTEM MAP MODE:
Allowed: inspect repo, inspect docs, inspect contracts, classify files, document guardrails.
Forbidden: tune video quality, change renderer, add providers, add new production modules.

MODULE QUALITY MODE:
Allowed: improve one selected module after its input, output, consumer, and runtime proof are known.
Forbidden: jump to other modules or change unrelated files.

VIDEO QUALITY MODE:
Allowed only after skeleton and gates are confirmed.
Forbidden before system map review is complete.

## Stop triggers

Stop if:

1. Current map step is unknown.
2. Requested action does not match the map step.
3. Git is dirty and user did not approve dirty work.
4. Action creates a second active contour.
5. Action mixes active runtime, donor, archive, or legacy.
6. Action uses production placeholders, stubs, or fake outputs.
7. User asks "по карті що далі?" and assistant cannot name the source.

## File rules

All file changes:

- full file replacement only
- nano only
- no heredoc
- no partial patches
- no hidden edits
- no production placeholders
- no fake progress

## Git rules

Before commit:

1. run relevant runtime check if needed
2. run bash tools/preflight.sh
3. inspect git status
4. stage only intended files
5. commit precisely
6. push to origin cashflow-mode
7. verify clean status

## Visual pacing lesson

Visual pacing works technically, but blind motion can make video worse.

Rule:
motion must depend on asset type and content role.

Stock video: motion allowed.
Lifestyle footage: motion allowed.
Static info card: motion limited.
Chart: hold or controlled reveal.
Checklist: hold or item-by-item reveal.
Dense text card: avoid zoom and pan.

## Exit condition

Accepted when:

1. this file exists
2. it is committed to cashflow-mode
3. future technical answers include MAP CHECK
4. next action is repo/map inspection, not video-quality tuning

End.
