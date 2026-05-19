# ASSET RESOLVER CONTRACT V1

Status: TRUSTED CONTRACT
Scope: Production resolver contract for FlowMind asset resolution phase.

## Purpose

Asset Resolver converts planning-only asset entries into resolved local media asset records.

Asset Resolver v1 does not render video.

Asset Resolver v1 does not create audio.

Asset Resolver v1 does not publish content.

Asset Resolver v1 does not modify protected manifest identity.

Asset Resolver v1 does not control phase transitions by itself.

## Why this exists

ASSETS executor v1 creates planning-only asset records.

Current asset records have:

- provider_status = planned
- local_path = null
- source_url = null
- license_status = pending

QA correctly blocks the project because:

- assets are not resolved
- licenses are not cleared
- assembly cannot be render-ready without real media files

Asset Resolver v1 exists to move assets from planning-only to resolved-or-blocked state.

## Authority

Asset Resolver operates under:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_PRODUCTION_RECOVERY_PLAN_V1.md
- ASSETS_EXECUTOR_CONTRACT_V1.md
- ASSEMBLY_EXECUTOR_CONTRACT_V1.md
- QA_EXECUTOR_CONTRACT_V1.md
- PROJECT_STATE.json
- canonical dispatcher control flow

## Required input

Asset Resolver reads:

- projects/<PROJECT_ID>/PROJECT_STATE.json
- artifacts.assets_path
- artifacts.scenes_path

Required state fields:

- project_id
- phase
- artifacts
- manifest

Required manifest fields:

- stock_policy
- primary_platform
- content_language
- topic
- working_title

Required artifact files:

- assets.json
- scenes.json

## Required starting phase

Asset Resolver v1 may run only when:

- phase = QA

Reason:

- QA has identified unresolved assets as blockers
- Asset Resolver v1 is a blocker-resolution tool
- it must not pretend to be a normal forward phase yet

If phase is not QA, resolver must fail closed.

## Output artifact

Asset Resolver v1 must create:

- projects/<PROJECT_ID>/assets/resolved_assets.json

resolved_assets.json must contain:

- project_id
- resolver
- resolver_version
- source_assets_path
- source_scenes_path
- asset_count
- resolved_count
- blocked_count
- license_cleared_count
- provider_mode
- assets
- blockers
- warnings
- created_at

## Resolved asset structure

Each resolved asset must contain:

- asset_id
- scene_id
- order
- asset_type
- asset_query
- visual_intent
- usage_role
- required
- provider_status
- source_provider
- source_url
- local_path
- license_status
- license_note
- resolution_status
- blocker_reason
- production_notes

Allowed provider_status values:

- resolved
- blocked

Allowed license_status values:

- cleared
- blocked

Allowed resolution_status values:

- ready
- blocked

## Provider mode

Asset Resolver v1 starts in deterministic local placeholder-free mode.

Important:

- it must not create fake media files
- it must not claim a file exists unless it exists on disk
- it must not use placeholder/stub files
- it must not mark license cleared unless the source policy is explicitly safe

Allowed provider_mode values:

- local_existing_only
- external_provider_later

For first implementation:

- provider_mode = local_existing_only

## Local existing only rule

In local_existing_only mode, Asset Resolver v1 may only resolve an asset if a real local media file already exists in an approved asset source directory.

Approved directories:

- assets_library/
- projects/<PROJECT_ID>/manual_assets/

If no matching file exists, the asset must be marked:

- provider_status = blocked
- license_status = blocked
- resolution_status = blocked

It must not generate or fake a media file.

## License rule

License status may be cleared only if:

- source_provider is explicitly known
- license policy is explicitly documented
- file source is approved
- source_url or local provenance is present

If license cannot be proven, license_status must be blocked.

## No-repeat rule

Asset Resolver must respect manifest.stock_policy.

For stock_first_no_repeat:

- do not assign the same local_path to multiple different assets
- do not reuse the same source_url across multiple different assets
- if unique media cannot be found, block the asset instead of reusing silently

## State update rule

Asset Resolver must not directly rewrite protected manifest identity.

Allowed state output is limited to artifact registration:

- artifacts.resolved_assets_path

Asset Resolver must not transition phase by itself.

Dispatcher remains responsible for any later phase transition.

## Relationship to assets.json

Asset Resolver v1 must not rewrite assets.json.

It creates a new artifact:

- resolved_assets.json

This keeps original planning assets immutable and auditable.

Later systems may decide whether to merge resolved assets into render inputs.

## Required blocker behavior

If no assets can be resolved, this is still a valid resolver run if:

- resolved_assets.json is created
- every asset is marked blocked
- blocker reasons are explicit
- PROJECT_STATE remains valid

This prevents fake progress.

## Forbidden

Asset Resolver v1 must not:

- run before assets_path exists
- rewrite assets.json
- rewrite scenes.json
- rewrite assembly_plan.json
- rewrite qa_report.json
- create fake media files
- create placeholder files
- create stub images
- set provider_status=resolved without a real file
- set license_status=cleared without evidence
- reuse the same asset path silently
- call FFmpeg
- call Cloudinary
- call YouTube API
- call AI image/video APIs
- publish content
- modify manifest fields
- transition project phase

## Fail-closed rules

Asset Resolver must fail if:

- PROJECT_STATE.json is missing
- PROJECT_STATE.json is invalid
- phase is not QA
- artifacts.assets_path is missing
- artifacts.scenes_path is missing
- assets.json is missing or invalid
- scenes.json is missing or invalid
- asset_count does not match assets length
- scene_count does not match scenes length
- any asset lacks required fields
- any resolved asset lacks required fields
- resolved_assets.json cannot be written
- state artifact registration cannot be validated

## Forbidden markers

Asset Resolver must fail if checked planning artifacts contain:

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

External services are not allowed in Asset Resolver v1 first implementation.

Forbidden in first implementation:

- Pexels API
- Pixabay API
- Storyblocks API
- Cloudinary
- FFmpeg
- Runway
- Pika
- Midjourney
- OpenAI image/video generation
- YouTube API

External providers may be added only after local_existing_only mode is stable.

## Initial implementation rule

The first implementation must be deterministic.

Priority:

1. validate assets.json
2. validate scenes.json
3. search approved local directories only
4. resolve only real existing files
5. block unresolved assets honestly
6. register resolved_assets_path
7. no fake files
8. no external calls

## Exit condition

Asset Resolver v1 is complete only when:

- project is in QA phase
- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase QA
- it reads assets.json
- it reads scenes.json
- it creates resolved_assets.json
- every asset is either resolved or blocked
- no fake media file is created
- no external provider is called
- artifacts.resolved_assets_path is registered
- PROJECT_STATE.json remains valid
- preflight passes
- git status is clean after milestone commit
