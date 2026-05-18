# ASSETS EXECUTOR CONTRACT V1

Status: TRUSTED CONTRACT
Scope: Production executor contract for FlowMind ASSETS phase.

## Purpose

ASSETS executor converts a validated SCENES artifact into a production-ready asset plan.

ASSETS executor does not generate the script.

ASSETS executor does not rewrite the scene plan.

ASSETS executor does not download stock assets in v1.

ASSETS executor does not call Cloudinary in v1.

ASSETS executor does not call AI image or AI video generation in v1.

ASSETS executor does not create audio.

ASSETS executor does not assemble video.

ASSETS executor does not publish content.

ASSETS executor does not control phase transitions by itself.

ASSETS executor does not modify protected manifest identity.

## Authority

ASSETS executor operates under:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_PRODUCTION_RECOVERY_PLAN_V1.md
- SCRIPT_EXECUTOR_CONTRACT_V1.md
- SCRIPT_QA_CONTRACT_V1.md
- SCENES_EXECUTOR_CONTRACT_V1.md
- PROJECT_STATE.json
- canonical dispatcher control flow

## Required input

ASSETS executor reads:

- projects/<PROJECT_ID>/PROJECT_STATE.json
- artifacts.script_path
- artifacts.script_meta_path
- artifacts.script_qa_path
- artifacts.scenes_path

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
- stock_policy

Required artifact files:

- script.txt
- script_meta.json
- script_qa.json
- scenes.json

## Required starting phase

ASSETS executor may run only when:

- phase = ASSETS

If phase is not ASSETS, executor must fail closed.

## Upstream requirement

ASSETS executor may run only if:

- script_qa.json exists
- script_qa.verdict = PASS
- scenes.json exists
- scenes.json is valid JSON
- scenes.scene_count >= 6
- scenes.scenes is a non-empty list
- every scene has asset_type
- every scene has visual_intent
- every scene has estimated_duration_sec

If upstream artifacts are missing or invalid, ASSETS executor must fail closed.

## Output artifact

ASSETS executor must create:

- projects/<PROJECT_ID>/assets/assets.json

assets.json must contain:

- project_id
- executor
- executor_version
- source_phase
- source_scenes_path
- topic
- working_title
- niche
- audience
- content_language
- primary_platform
- stock_policy
- asset_count
- assets
- created_at

Each asset entry must contain:

- asset_id
- scene_id
- order
- asset_type
- asset_query
- visual_intent
- usage_role
- estimated_duration_sec
- required
- provider_status
- local_path
- source_url
- license_status
- production_notes

## State update rule

ASSETS executor must not directly rewrite protected manifest identity.

Allowed state output is limited to artifact registration.

Required artifact key:

- artifacts.assets_path

ASSETS executor must not transition phase by itself.

Dispatcher remains responsible for any later phase transition.

## V1 asset strategy

ASSETS v1 is planning-only.

It creates an asset plan but does not fetch or generate media.

Allowed provider_status values:

- planned
- unavailable
- skipped

For v1, every asset should use:

- provider_status = planned
- local_path = null
- source_url = null
- license_status = pending

This keeps ASSETS v1 deterministic and avoids hidden external costs.

## Allowed asset_type values

ASSETS executor accepts scene asset_type values:

- stock_video
- stock_image
- simple_motion_text
- chart_or_bill_visual
- screen_style_visual

ASSETS executor must fail if scenes.json contains unsupported asset_type.

## Asset query rule

Each asset must include a clear asset_query.

Examples:

- simple_motion_text:
  - "minimal animated text about rising electricity bills"
- chart_or_bill_visual:
  - "utility bill cost breakdown usage rate fixed charges"
- screen_style_visual:
  - "checklist comparing electricity bill usage rate fixed charges"
- stock_video:
  - "home appliances electricity usage refrigerator water heater"
- stock_image:
  - "household energy costs simple home finance"

Asset query must not be empty.

## Usage role rule

Allowed usage_role values:

- primary_visual
- supporting_visual
- text_overlay
- diagnostic_visual
- transition_visual

Each asset must have one usage_role.

## Production requirements

The asset plan must:

- map every scene to at least one asset
- preserve scene order
- preserve scene_id
- avoid unsupported factual additions
- avoid creating production claims not present in scenes
- be usable by future ASSEMBLY executor
- be simple enough for manual or automated asset fetching later

## Minimum asset count

asset_count must be:

- at least equal to scenes.scene_count
- not less than 6

For v1, one planned asset per scene is enough.

## Forbidden

ASSETS executor must not:

- run from SCENES phase
- run before scenes_path exists
- rewrite script.txt
- rewrite script_meta.json
- rewrite script_qa.json
- rewrite scenes.json
- transition ASSETS to ASSEMBLY
- write ExecutionManifest.json
- use FM_* station artifacts as source of truth
- call legacy asset modules as active authority
- modify manifest.niche
- modify manifest.audience
- modify manifest.topic
- modify manifest.working_title
- modify manifest.hook
- download stock assets in v1
- call Cloudinary in v1
- call AI image generation in v1
- call AI video generation in v1
- create audio
- create final video
- publish to YouTube

## Fail-closed rules

ASSETS executor must fail if:

- PROJECT_STATE.json is missing
- PROJECT_STATE.json is invalid
- phase is not ASSETS
- artifacts.scenes_path is missing
- scenes.json is missing or invalid
- scenes.scenes is empty
- scene_count does not match scenes length
- any scene is missing scene_id
- any scene is missing asset_type
- any scene has unsupported asset_type
- any scene is missing visual_intent
- any generated asset is missing required fields
- asset_count is below scene_count
- assets.json cannot be written
- state artifact registration cannot be validated

## Forbidden markers

ASSETS executor must fail if scenes or asset plan contain:

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

External services are not allowed in ASSETS v1.

Deferred services:

- Pexels
- Pixabay
- Storyblocks
- Cloudinary
- Runway
- Pika
- Midjourney
- DALL-E
- Sora
- ElevenLabs
- YouTube API

These may be considered later only after deterministic ASSETS v1 passes.

## Initial implementation rule

The first implementation must be deterministic.

Priority:

1. valid assets artifact
2. one planned asset per scene
3. no external calls
4. fail-closed behavior
5. safe artifact registration
6. provider integration later

## Exit condition

ASSETS executor v1 is complete only when:

- project is in ASSETS phase
- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase ASSETS
- it reads scenes.json
- it creates assets.json
- assets.json maps every scene_id
- it registers artifacts.assets_path safely
- PROJECT_STATE.json remains valid
- no external provider is called
- no legacy station runtime is used
- git status is clean after milestone commit
