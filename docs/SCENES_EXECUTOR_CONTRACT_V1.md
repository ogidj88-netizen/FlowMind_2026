# SCENES EXECUTOR CONTRACT V1

Status: TRUSTED CONTRACT
Scope: Production executor contract for FlowMind SCENES phase.

## Purpose

SCENES executor converts a validated SCRIPT artifact into a production-ready scene plan.

SCENES executor does not generate the script.

SCENES executor does not select final assets.

SCENES executor does not create audio.

SCENES executor does not assemble video.

SCENES executor does not publish content.

SCENES executor does not control phase transitions by itself.

SCENES executor does not modify protected manifest identity.

## Authority

SCENES executor operates under:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_PRODUCTION_RECOVERY_PLAN_V1.md
- SCRIPT_EXECUTOR_CONTRACT_V1.md
- SCRIPT_QA_CONTRACT_V1.md
- PROJECT_STATE.json
- canonical dispatcher control flow

## Required input

SCENES executor reads:

- projects/<PROJECT_ID>/PROJECT_STATE.json
- artifacts.script_path
- artifacts.script_meta_path
- artifacts.script_qa_path

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

Required artifact files:

- script.txt
- script_meta.json
- script_qa.json

## Required starting phase

SCENES executor may run only when:

- phase = SCENES

If phase is not SCENES, executor must fail closed.

## Script QA requirement

SCENES executor may run only if:

- script_qa.json exists
- script_qa.json is valid JSON
- script_qa.verdict = PASS

If SCRIPT QA did not pass, SCENES executor must fail closed.

## Output artifact

SCENES executor must create:

- projects/<PROJECT_ID>/scenes/scenes.json

scenes.json must contain:

- project_id
- executor
- executor_version
- source_phase
- source_script_path
- source_script_qa_path
- topic
- working_title
- niche
- audience
- content_language
- target_duration_sec
- scene_count
- estimated_total_duration_sec
- scenes
- created_at

Each scene must contain:

- scene_id
- order
- voiceover_text
- visual_intent
- on_screen_text
- asset_type
- estimated_duration_sec
- production_notes

## State update rule

SCENES executor must not directly rewrite protected manifest identity.

Allowed state output is limited to artifact registration.

Required artifact key:

- artifacts.scenes_path

SCENES executor must not transition phase by itself.

Dispatcher remains responsible for any later phase transition.

## Scene plan requirements

The scene plan must:

- preserve the meaning of script.txt
- follow the script order
- split the script into coherent production segments
- avoid changing factual meaning
- avoid adding unsupported claims
- be usable by future ASSETS executor
- be usable by future ASSEMBLY executor
- include estimated duration per scene
- keep total duration reasonably close to target_duration_sec

## Minimum scene structure

Each scene must answer:

1. what narration is spoken
2. what the viewer should see
3. what text appears on screen
4. what type of asset is needed
5. how long the scene should last
6. what production note matters

## Asset type rule

Allowed asset_type values for v1:

- stock_video
- stock_image
- simple_motion_text
- chart_or_bill_visual
- screen_style_visual

SCENES executor must not download or generate assets.

It only declares asset intent.

## Duration rule

Estimated scene duration should be based on voiceover word count.

Use:

- 145 words per minute

Allowed total duration drift:

- target duration minus 20 percent
- target duration plus 20 percent

If estimated_total_duration_sec is outside this range, executor must fail closed or mark output invalid.

## Scene count rule

For v1, scene_count should normally be:

- minimum: 6
- maximum: 18

If the script is too short to create at least 6 useful scenes, executor must fail closed.

If the script creates more than 18 scenes, executor should merge weak or tiny scenes.

## Forbidden

SCENES executor must not:

- run from SCRIPT phase
- run before SCRIPT QA PASS
- rewrite script.txt
- rewrite script_meta.json
- rewrite script_qa.json
- transition SCENES to ASSETS
- write ExecutionManifest.json
- use FM_* station artifacts as source of truth
- call legacy scene modules as active authority
- modify manifest.niche
- modify manifest.audience
- modify manifest.topic
- modify manifest.working_title
- modify manifest.hook
- create assets
- create audio
- create final video
- publish to YouTube

## Fail-closed rules

SCENES executor must fail if:

- PROJECT_STATE.json is missing
- PROJECT_STATE.json is invalid
- phase is not SCENES
- artifacts.script_path is missing
- artifacts.script_meta_path is missing
- artifacts.script_qa_path is missing
- script.txt is missing
- script_meta.json is missing or invalid
- script_qa.json is missing or invalid
- script_qa.verdict is not PASS
- script text is empty
- script contains forbidden markers
- scenes output is empty
- scene_count is below minimum
- any scene is missing required fields
- estimated_total_duration_sec is outside allowed range
- scenes.json cannot be written
- state artifact registration cannot be validated

## Forbidden markers

SCENES executor must fail if script or scenes contain:

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

## Initial implementation rule

The first implementation may be deterministic.

Priority:

1. valid scenes artifact
2. clear scene segmentation
3. deterministic duration estimates
4. fail-closed behavior
5. safe artifact registration
6. semantic improvement later

## Exit condition

SCENES executor v1 is complete only when:

- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase SCENES
- it reads script.txt
- it reads script_meta.json
- it reads script_qa.json
- it confirms script_qa.verdict = PASS
- it creates scenes.json
- it registers artifacts.scenes_path safely
- PROJECT_STATE.json remains valid
- no legacy station runtime is used
- git status is clean after milestone commit

