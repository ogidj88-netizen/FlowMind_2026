# SCRIPT EXECUTOR CONTRACT V1

Status: TRUSTED CONTRACT
Scope: First production executor contract for FlowMind canonical production recovery.

## Purpose

SCRIPT executor is the first trusted production executor in the FlowMind production recovery path.

Its purpose is to create a usable script artifact from canonical project state.

It does not control phase transitions.

It does not replace the dispatcher.

It does not mutate protected manifest identity.

It does not publish content.

## Authority

SCRIPT executor operates under:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_PRODUCTION_RECOVERY_PLAN_V1.md
- PROJECT_STATE.json
- canonical dispatcher control flow

## Required input

SCRIPT executor reads:

- projects/<PROJECT_ID>/PROJECT_STATE.json

Required state fields:

- project_id
- phase
- manifest

Required manifest fields:

- niche
- audience
- content_language
- primary_platform
- topic
- working_title
- hook
- target_duration_sec

## Required starting phase

SCRIPT executor may run only when:

- phase = SCRIPT

If phase is not SCRIPT, executor must fail closed.

## Output artifact

SCRIPT executor must create:

- projects/<PROJECT_ID>/script/script.txt
- projects/<PROJECT_ID>/script/script_meta.json

script.txt must contain the final voiceover script.

script_meta.json must contain:

- project_id
- executor
- executor_version
- source_phase
- topic
- working_title
- niche
- audience
- content_language
- target_duration_sec
- word_count
- estimated_duration_minutes
- created_at
- qa_status

## State update rule

SCRIPT executor must not directly rewrite protected manifest identity.

Allowed state output is limited to artifact registration.

The preferred state update path is:

- dispatcher-safe artifact patch
- state_store validation
- no direct unsafe PROJECT_STATE.json mutation

Required artifact keys:

- artifacts.script_path
- artifacts.script_meta_path

## Production quality requirements

Script must:

- match manifest.topic
- match manifest.niche
- match manifest.audience
- use manifest.content_language
- open with a strong hook
- avoid generic AI intro
- avoid fake facts
- avoid unsupported claims
- avoid filler
- include practical payoff
- fit target_duration_sec
- be usable as voiceover

## Minimum script shape

Script should include:

1. opening hook
2. problem framing
3. concrete explanation
4. escalating stakes
5. practical insight or payoff
6. clean ending

## Word count rule

Estimated duration uses:

- 145 words per minute

Allowed range for target_duration_sec:

- minimum: target duration minus 20 percent
- maximum: target duration plus 20 percent

If script is outside range, executor must fail closed or mark QA as failed.

## Fail-closed rules

Executor must fail if:

- PROJECT_STATE.json is missing
- PROJECT_STATE.json is invalid
- phase is not SCRIPT
- required manifest fields are missing
- script output is empty
- script is below minimum useful length
- script contains placeholder text
- script contains stub text
- script contains DO_NOT_PUBLISH
- script contains obvious fake output markers
- script_meta.json cannot be written
- state artifact patch cannot be validated

## Forbidden

SCRIPT executor must not:

- run from TOPIC phase
- transition phases by itself
- write ExecutionManifest.json
- use FM_* station artifacts as source of truth
- call legacy engine/modules/s2_script.py
- modify manifest.niche
- modify manifest.audience
- modify manifest.topic
- modify manifest.working_title
- modify manifest.hook
- publish to YouTube
- create upload metadata
- create scenes
- create assets
- create audio
- create final video

## External model usage

External AI model usage is allowed only if:

- API key is read from environment
- no API key is written to code
- request failure is handled
- empty response fails closed
- output is validated before artifact registration

## Initial implementation rule

The first implementation may be simple.

Priority:

1. valid artifact
2. deterministic checks
3. fail-closed behavior
4. clean state registration
5. quality improvement later

## Exit condition

SCRIPT executor v1 is complete only when:

- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase SCRIPT
- it creates script.txt
- it creates script_meta.json
- it registers artifact paths safely
- PROJECT_STATE.json remains valid
- git status is clean after commit
- no legacy station runtime is used
