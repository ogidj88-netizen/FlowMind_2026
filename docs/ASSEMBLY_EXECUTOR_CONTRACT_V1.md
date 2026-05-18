# ASSEMBLY EXECUTOR CONTRACT V1

Status: TRUSTED CONTRACT
Scope: Production executor contract for FlowMind ASSEMBLY phase.

## Purpose

ASSEMBLY executor converts validated SCENES and ASSETS artifacts into a production-ready assembly plan.

ASSEMBLY v1 does not create a final video file.

ASSEMBLY v1 does not call FFmpeg.

ASSEMBLY v1 does not download assets.

ASSEMBLY v1 does not call Cloudinary.

ASSEMBLY v1 does not generate audio.

ASSEMBLY v1 does not publish content.

ASSEMBLY v1 does not control phase transitions by itself.

ASSEMBLY v1 does not modify protected manifest identity.

## Why v1 is planning-only

ASSETS v1 is planning-only.

Assets created by ASSETS v1 have:

- provider_status = planned
- local_path = null
- source_url = null
- license_status = pending

Because there are no resolved media files, ASSEMBLY v1 must not pretend to create a final render.

The honest v1 output is:

- assembly_plan.json

Not:

- final_video.mp4

## Authority

ASSEMBLY executor operates under:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_PRODUCTION_RECOVERY_PLAN_V1.md
- SCRIPT_EXECUTOR_CONTRACT_V1.md
- SCRIPT_QA_CONTRACT_V1.md
- SCENES_EXECUTOR_CONTRACT_V1.md
- ASSETS_EXECUTOR_CONTRACT_V1.md
- PROJECT_STATE.json
- canonical dispatcher control flow

## Required input

ASSEMBLY executor reads:

- projects/<PROJECT_ID>/PROJECT_STATE.json
- artifacts.script_path
- artifacts.script_meta_path
- artifacts.script_qa_path
- artifacts.scenes_path
- artifacts.assets_path

Required state fields:

- project_id
- phase
- artifacts
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
- render_profile
- stock_policy

Required artifact files:

- script.txt
- script_meta.json
- script_qa.json
- scenes.json
- assets.json

## Required starting phase

ASSEMBLY executor may run only when:

- phase = ASSEMBLY

If phase is not ASSEMBLY, executor must fail closed.

## Upstream requirements

ASSEMBLY executor may run only if:

- script_qa.json exists
- script_qa.verdict = PASS
- scenes.json exists
- assets.json exists
- scenes.scene_count >= 6
- assets.asset_count >= scenes.scene_count
- every scene_id in scenes.json has a matching asset in assets.json
- every asset has provider_status = planned
- every asset has license_status = pending
- every asset has local_path = null in v1
- every asset has source_url = null in v1

If upstream artifacts are missing or invalid, ASSEMBLY executor must fail closed.

## Output artifact

ASSEMBLY executor must create:

- projects/<PROJECT_ID>/assembly/assembly_plan.json

assembly_plan.json must contain:

- project_id
- executor
- executor_version
- source_phase
- source_scenes_path
- source_assets_path
- topic
- working_title
- niche
- audience
- content_language
- primary_platform
- render_profile
- target_duration_sec
- assembly_status
- render_ready
- scene_count
- estimated_total_duration_sec
- timeline
- missing_requirements
- created_at

Allowed assembly_status values:

- planned
- blocked

For ASSEMBLY v1:

- assembly_status = planned
- render_ready = false

Because media assets are not resolved yet.

## Timeline item structure

Each timeline item must contain:

- timeline_id
- scene_id
- order
- voiceover_text
- estimated_duration_sec
- asset_id
- asset_type
- asset_query
- usage_role
- provider_status
- local_path
- source_url
- visual_intent
- on_screen_text
- production_notes

## State update rule

ASSEMBLY executor must not directly rewrite protected manifest identity.

Allowed state output is limited to artifact registration.

Required artifact key:

- artifacts.assembly_plan_path

ASSEMBLY executor must not transition phase by itself.

Dispatcher remains responsible for any later phase transition.

## Render readiness rule

ASSEMBLY v1 must set:

- render_ready = false

unless all required assets have:

- provider_status = resolved
- local_path is non-empty
- license_status = cleared

Since ASSETS v1 is planning-only, ASSEMBLY v1 must not mark output as render-ready.

## Missing requirements rule

ASSEMBLY v1 must list missing render requirements.

Minimum missing_requirements:

- resolved media asset files
- cleared asset licenses
- audio artifact
- final render executor

This prevents fake progress.

## Production requirements

The assembly plan must:

- preserve scene order
- map every scene to an asset
- preserve voiceover_text
- preserve estimated_duration_sec
- preserve visual_intent
- preserve on_screen_text
- avoid adding unsupported factual claims
- be usable by a future render executor
- be honest about missing real media files

## Duration rule

assembly_plan.estimated_total_duration_sec must match scenes.estimated_total_duration_sec.

Allowed total duration range:

- target duration minus 20 percent
- target duration plus 20 percent

If estimated duration is outside this range, executor must fail closed.

## Forbidden

ASSEMBLY executor must not:

- run from ASSETS phase
- run before assets_path exists
- rewrite script.txt
- rewrite script_meta.json
- rewrite script_qa.json
- rewrite scenes.json
- rewrite assets.json
- transition ASSEMBLY to QA
- write ExecutionManifest.json
- use FM_* station artifacts as source of truth
- call legacy assembly modules as active authority
- modify manifest.niche
- modify manifest.audience
- modify manifest.topic
- modify manifest.working_title
- modify manifest.hook
- call FFmpeg in v1
- create final_video.mp4 in v1
- create audio
- download stock assets
- call Cloudinary
- call AI image generation
- call AI video generation
- publish to YouTube

## Fail-closed rules

ASSEMBLY executor must fail if:

- PROJECT_STATE.json is missing
- PROJECT_STATE.json is invalid
- phase is not ASSEMBLY
- artifacts.scenes_path is missing
- artifacts.assets_path is missing
- scenes.json is missing or invalid
- assets.json is missing or invalid
- scene_count does not match scenes length
- asset_count is below scene_count
- any scene lacks matching asset
- any timeline item is missing required fields
- estimated duration is outside allowed range
- assembly_plan.json cannot be written
- state artifact registration cannot be validated

## Forbidden markers

ASSEMBLY executor must fail if scenes, assets, or assembly plan contain:

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

External services are not allowed in ASSEMBLY v1.

Forbidden in v1:

- FFmpeg
- Cloudinary
- Pexels
- Pixabay
- Storyblocks
- Runway
- Pika
- Midjourney
- DALL-E
- Sora
- ElevenLabs
- YouTube API

These may be considered later only after deterministic ASSEMBLY v1 passes.

## Initial implementation rule

The first implementation must be deterministic.

Priority:

1. valid assembly_plan.json
2. honest render_ready=false
3. full scene-to-asset mapping
4. clear missing requirements
5. fail-closed behavior
6. safe artifact registration
7. real render later

## Exit condition

ASSEMBLY executor v1 is complete only when:

- project is in ASSEMBLY phase
- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase ASSEMBLY
- it reads scenes.json
- it reads assets.json
- it creates assembly_plan.json
- assembly_plan maps every scene to an asset
- assembly_plan sets render_ready=false
- assembly_plan lists missing render requirements
- it registers artifacts.assembly_plan_path safely
- PROJECT_STATE.json remains valid
- no external provider is called
- no fake final video is created
- no legacy station runtime is used
- git status is clean after milestone commit
