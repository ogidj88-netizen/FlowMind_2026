# QA EXECUTOR CONTRACT V1

Status: TRUSTED CONTRACT
Scope: Production executor contract for FlowMind QA phase.

## Purpose

QA executor validates the current canonical project state and determines whether the project is ready to proceed.

QA v1 is a readiness/blocker QA.

QA v1 does not approve upload.

QA v1 does not create final video.

QA v1 does not create audio.

QA v1 does not render media.

QA v1 does not download assets.

QA v1 does not call external APIs.

QA v1 does not publish content.

QA v1 does not modify protected manifest identity.

QA v1 does not control phase transitions by itself.

## Why v1 is blocker QA

The current pipeline has deterministic planning artifacts:

- script.txt
- script_meta.json
- script_qa.json
- scenes.json
- assets.json
- assembly_plan.json
- audio_plan.json

But it does not yet have:

- resolved media asset files
- cleared asset licenses
- rendered audio files
- validated audio loudness
- final video render
- upload-ready metadata package

Therefore QA v1 must not mark the project as ready for upload.

The honest v1 output is:

- qa_report.json
- verdict = BLOCKED
- qa_passed = false

Not:

- verdict = PASS
- qa_passed = true
- approved_for_upload = true

## Authority

QA executor operates under:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_PRODUCTION_RECOVERY_PLAN_V1.md
- SCRIPT_EXECUTOR_CONTRACT_V1.md
- SCRIPT_QA_CONTRACT_V1.md
- SCENES_EXECUTOR_CONTRACT_V1.md
- ASSETS_EXECUTOR_CONTRACT_V1.md
- ASSEMBLY_EXECUTOR_CONTRACT_V1.md
- AUDIO_EXECUTOR_CONTRACT_V1.md
- PROJECT_STATE.json
- canonical dispatcher control flow

## Required input

QA executor reads:

- projects/<PROJECT_ID>/PROJECT_STATE.json
- artifacts.script_path
- artifacts.script_meta_path
- artifacts.script_qa_path
- artifacts.scenes_path
- artifacts.assets_path
- artifacts.assembly_plan_path
- artifacts.audio_plan_path

Required state fields:

- project_id
- phase
- artifacts
- manifest
- qa_passed
- approved_for_upload
- approval_status

Required manifest fields:

- niche
- audience
- content_language
- primary_platform
- topic
- working_title
- hook
- target_duration_sec
- render_profile
- stock_policy

Required artifact files:

- script.txt
- script_meta.json
- script_qa.json
- scenes.json
- assets.json
- assembly_plan.json
- audio_plan.json

## Required starting phase

QA executor may run only when:

- phase = QA

If phase is not QA, executor must fail closed.

## Upstream requirements

QA executor may run only if:

- script_qa.json exists
- script_qa.verdict = PASS
- scenes.json exists
- assets.json exists
- assembly_plan.json exists
- audio_plan.json exists
- scenes.scene_count >= 6
- assets.asset_count >= scenes.scene_count
- assembly_plan.scene_count = scenes.scene_count
- audio_plan.audio_segments length = assembly_plan.timeline length

If upstream artifacts are missing or invalid, QA executor must fail closed.

## Output artifact

QA executor must create:

- projects/<PROJECT_ID>/qa/qa_report.json

qa_report.json must contain:

- project_id
- executor
- executor_version
- source_phase
- topic
- working_title
- niche
- audience
- content_language
- primary_platform
- target_duration_sec
- verdict
- qa_passed
- approved_for_upload
- readiness_score
- checks
- blockers
- warnings
- missing_requirements
- created_at

Allowed verdict values:

- PASS
- BLOCKED
- FAIL

For QA v1, expected verdict is:

- BLOCKED

because real media/audio/final render are not available yet.

## QA passed rule

QA v1 must set:

- qa_passed = false

unless all upload-critical requirements are satisfied.

Upload-critical requirements:

- script QA passed
- scenes artifact valid
- assets resolved
- asset licenses cleared
- assembly render_ready = true
- audio audio_ready = true
- final video file exists
- final video path registered
- final video duration validated
- final audio loudness validated
- no forbidden markers found
- no missing requirements remain

Since current ASSETS, ASSEMBLY, and AUDIO v1 are planning-only, QA v1 must not set qa_passed=true.

## State update rule

QA executor must not directly rewrite protected manifest identity.

Allowed state output is limited to:

- artifacts.qa_report_path
- qa_passed = false

QA executor must not set:

- qa_passed = true in v1
- approved_for_upload = true
- approval_status = APPROVED

Dispatcher remains responsible for any later phase transition.

## Checks structure

Each check must contain:

- check_id
- name
- status
- severity
- detail

Allowed check status values:

- PASS
- WARN
- BLOCKED
- FAIL

Allowed severity values:

- LOW
- MEDIUM
- HIGH
- CRITICAL

Minimum checks:

- script_qa_passed
- scenes_valid
- assets_valid
- assets_resolved
- asset_licenses_cleared
- assembly_plan_valid
- assembly_render_ready
- audio_plan_valid
- audio_ready
- final_video_exists
- upload_readiness

## Required blocker checks

QA v1 must mark these as BLOCKED when current v1 planning artifacts are used:

- assets_resolved
- asset_licenses_cleared
- assembly_render_ready
- audio_ready
- final_video_exists
- upload_readiness

This prevents fake production readiness.

## Missing requirements rule

QA v1 must list missing requirements from upstream artifacts.

Minimum missing_requirements should include:

- resolved media asset files
- cleared asset licenses
- rendered audio files
- audio duration validation
- loudness validation
- final render executor
- final video file
- upload readiness approval

If assembly_plan.missing_requirements exists, QA must include it.

If audio_plan.missing_requirements exists, QA must include it.

Duplicates should be removed.

## Readiness score rule

readiness_score is an integer from 0 to 100.

For QA v1:

- script/scenes/assets/assembly/audio planning progress may increase score
- missing real media/audio/render must prevent high score
- readiness_score must remain below 80 if final video is missing
- readiness_score must remain below 60 if audio_ready=false
- readiness_score must remain below 60 if render_ready=false

For the current pipeline, expected score should be partial, not upload-ready.

## Production requirements

QA report must:

- preserve project_id
- preserve topic
- preserve working_title
- preserve manifest identity
- check all upstream artifacts
- not rewrite upstream artifacts
- clearly separate PASS, WARN, BLOCKED, FAIL
- not claim production readiness without real evidence
- be useful for deciding next engineering block

## Forbidden

QA executor must not:

- run from AUDIO phase
- run before audio_plan_path exists
- rewrite script.txt
- rewrite script_meta.json
- rewrite script_qa.json
- rewrite scenes.json
- rewrite assets.json
- rewrite assembly_plan.json
- rewrite audio_plan.json
- transition QA to READY_FOR_UPLOAD
- write ExecutionManifest.json
- use FM_* station artifacts as source of truth
- call legacy QA modules as active authority
- modify manifest.niche
- modify manifest.audience
- modify manifest.topic
- modify manifest.working_title
- modify manifest.hook
- create final_video.mp4
- create voiceover.mp3
- create voiceover.wav
- call ElevenLabs
- call OpenAI TTS
- call Cloudinary
- call FFmpeg
- publish to YouTube
- set approved_for_upload=true
- set approval_status=APPROVED
- set qa_passed=true in v1

## Fail-closed rules

QA executor must fail if:

- PROJECT_STATE.json is missing
- PROJECT_STATE.json is invalid
- phase is not QA
- artifacts.script_qa_path is missing
- artifacts.scenes_path is missing
- artifacts.assets_path is missing
- artifacts.assembly_plan_path is missing
- artifacts.audio_plan_path is missing
- any required artifact is invalid JSON
- script_qa.verdict is not PASS
- scenes.scene_count does not match scenes length
- assets.asset_count does not match assets length
- assembly_plan.timeline is empty
- audio_plan.audio_segments is empty
- qa_report.json cannot be written
- state artifact registration cannot be validated

## Forbidden markers

QA executor must fail if checked artifacts contain:

- PLACEHOLDER
- STUB
- STUBBED
- DO_NOT_PUBLISH
- TODO
- FAKE_OUTPUT
- LOREM IPSUM
- TEST ONLY
- DUMMY
- MOCK

## External service rule

External services are not allowed in QA v1.

Forbidden in v1:

- ElevenLabs
- OpenAI TTS
- Google TTS
- Azure TTS
- Amazon Polly
- Cloudinary
- FFmpeg
- Pexels
- Pixabay
- Storyblocks
- YouTube API

These may be considered later only after deterministic QA v1 passes.

## Initial implementation rule

The first implementation must be deterministic.

Priority:

1. valid qa_report.json
2. honest verdict=BLOCKED
3. qa_passed=false
4. full upstream artifact validation
5. explicit blockers
6. explicit missing requirements
7. safe artifact registration
8. no external calls
9. no fake upload readiness

## Exit condition

QA executor v1 is complete only when:

- project is in QA phase
- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase QA
- it reads script_qa.json
- it reads scenes.json
- it reads assets.json
- it reads assembly_plan.json
- it reads audio_plan.json
- it creates qa_report.json
- qa_report.verdict = BLOCKED
- qa_report.qa_passed = false
- qa_report lists blockers
- qa_report lists missing requirements
- it registers artifacts.qa_report_path safely
- PROJECT_STATE.json remains valid
- no external provider is called
- no fake final video is created
- no fake audio file is created
- no legacy station runtime is used
- git status is clean after milestone commit
