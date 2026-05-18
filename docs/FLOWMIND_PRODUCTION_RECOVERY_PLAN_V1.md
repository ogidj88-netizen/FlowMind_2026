# FLOWMIND PRODUCTION RECOVERY PLAN V1

Status: TRUSTED PLAN
Scope: Next-step production recovery plan after governance cleanup, dispatcher verification, and bootstrap identity fix.

## Purpose

This document defines the ordered recovery path from a verified control layer to the first working production contour.

It is not an implementation file.

It does not replace:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- PROJECT_STATE.json
- canonical dispatcher runtime

## Current confirmed base

The following are confirmed:

- governance registry is active
- trusted boundary model is active
- frozen legacy is separated from active runtime
- canonical dispatcher runtime checks pass
- canonical bootstrap creates valid PROJECT_STATE.json
- bootstrap now requires explicit project identity inputs:
  - niche
  - audience
  - content_language
  - primary_platform
  - topic
  - working_title
  - hook
  - target_duration_sec

## Core recovery principle

Do not expand the system before one working production path exists.

Priority order:

1. speed
2. stability
3. production quality
4. scale
5. optimization

## Current structural verdict

FlowMind structure is valid.

The control layer is stronger than the production layer.

The main gap is not architecture.

The main gap is missing trusted production executors.

## Target production path

The target path is:

1. bootstrap project
2. dispatcher show
3. TOPIC
4. SCRIPT
5. SCENES
6. ASSETS
7. ASSEMBLY
8. QA
9. READY_FOR_UPLOAD
10. Delivery Pack
11. manual review
12. upload later

## Phase 1 — Canonical test project

Goal:

Create the first real canonical test project using explicit project identity inputs.

This project is not a production upload.

Required checks:

- PROJECT_STATE.json exists
- state validates
- dispatcher show works
- transition TOPIC to SCRIPT works
- no legacy station flow is used
- git remains clean unless the test project is intentionally committed

Exit condition:

A real canonical project state can be created and moved through dispatcher control without legacy runtime.

## Phase 2 — SCRIPT executor

Goal:

Create the first trusted production executor.

SCRIPT executor must:

- read PROJECT_STATE.json
- use manifest.topic
- use manifest.niche
- use manifest.audience
- use manifest.content_language
- use manifest.working_title
- use manifest.hook
- produce script artifact
- fail closed on invalid input
- avoid direct unsafe state mutation
- not modify protected manifest fields
- not use placeholder or stub output in production path

Output:

- artifacts.script_path
- script metadata
- validation result

Exit condition:

SCRIPT output exists, is valid, and is attached to project state through an approved path.

## Phase 3 — SCRIPT QA gate

Goal:

Prevent weak AI text from entering video production.

Minimum checks:

- strong hook
- no generic intro
- clear structure
- matches niche and audience
- no fake factual claims
- useful payoff
- target duration fit
- no placeholder or stub text
- no DO_NOT_PUBLISH marker

Exit condition:

Weak script is blocked.
Valid script can proceed.

## Phase 4 — SCENES executor

Goal:

Convert script into a production-ready scene plan.

Scene plan must include:

- scene_id
- voiceover segment
- visual intent
- on-screen text
- asset type
- estimated duration

Exit condition:

SCENES artifact exists and can guide asset selection and assembly.

## Phase 5 — ASSETS executor

Goal:

Use a simple stock-first asset strategy.

Rules:

- no complex AI video generation in v1
- no expensive visual generation before stable pipeline
- no cinematic overbuild
- assets must match scenes
- missing assets must fail clearly

Exit condition:

ASSETS artifact exists and maps to scene plan.

## Phase 6 — ASSEMBLY executor

Goal:

Create a minimal final video artifact.

Rules:

- simple assembly first
- stable output over visual complexity
- final video path must be recorded
- assembly must fail clearly if inputs are missing

Exit condition:

final_video_path exists and is readable.

## Phase 7 — FINAL QA gate

Goal:

Block unsafe or low-quality final output.

Minimum checks:

- final_video_path exists
- file is readable
- duration is valid
- audio/video are present if required
- script matches topic
- no placeholder or stub markers
- metadata exists
- human review required at start

Exit condition:

Only reviewed and valid output can move to READY_FOR_UPLOAD.

## Phase 8 — Delivery Pack

Goal:

Prepare upload-ready materials without automatic upload.

Delivery Pack includes:

- final video path
- title
- description
- tags
- thumbnail path or thumbnail prompt
- QA verdict
- human review checklist

Exit condition:

A human can review and manually publish the package.

## Deferred until later

The following must not be added before one working production path exists:

- Redis
- Celery
- Postgres
- multi-agent mesh
- analytics feedback loop
- automatic YouTube upload
- TikTok crossposting
- complex trend system
- expensive AI video generation
- full autonomous publishing

## Upload rule

YouTube API upload is not part of the immediate recovery phase.

Upload may be considered only after:

- at least two successful delivery packs
- manual review passed
- metadata contract is stable
- final QA is reliable

## Analytics rule

Analytics are valuable but deferred.

Analytics may be added only after real uploads exist.

Minimum future metrics:

- CTR
- views after 24h
- views after 72h
- average view duration
- retention
- topic score
- thumbnail score

## First test niche rule

Money Mistakes / Invisible Costs may be used as the first test production niche.

It must be passed explicitly through bootstrap inputs.

It must not be treated as FlowMind Core identity.

## Non-negotiable rules

Do not treat frozen legacy as active runtime.

Do not use ExecutionManifest.json as canonical runtime state.

Do not use FM_* station artifacts as active production contracts.

Do not allow modules to rewrite protected manifest identity.

Do not use placeholder, stub, or fake outputs in production path.

Do not build automation before the active production contour is verified.

## Current next action

Create the first canonical test project.

Target:

P2026_TEST_001

Goal:

Verify:

bootstrap
→ dispatcher show
→ TOPIC to SCRIPT transition

No production generation yet.
