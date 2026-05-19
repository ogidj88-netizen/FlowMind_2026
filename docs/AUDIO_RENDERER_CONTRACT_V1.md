# AUDIO_RENDERER_CONTRACT_V1

Status: TRUSTED CONTRACT
Version: 1.0.0
Owner: FlowMind
Mode: cashflow-mode
Scope: Audio production rendering layer
Runtime target: future engine/executors/audio_renderer.py

## Purpose

AUDIO_RENDERER_CONTRACT_V1 defines the production contract for rendering voiceover audio from an existing audio plan.

This contract does not replace audio_executor.py.

audio_executor.py is responsible for planning audio segments.

audio_renderer.py is responsible for rendering real audio files from the approved audio plan.

## Core decision

Audio rendering must be separated from audio planning.

The active split is:

- audio_executor.py creates projects/<PROJECT_ID>/audio/audio_plan.json
- audio_renderer.py reads audio_plan.json
- audio_renderer.py renders real voiceover files
- audio_renderer.py writes audio_render.json
- QA reads audio evidence from audio_render.json and/or updated audio artifacts

## Why separation is required

audio_executor.py v1 is planning-only.

It intentionally outputs:

- audio_status: planned
- audio_ready: false
- tts_provider: null
- voice_profile: null
- audio_path: null
- provider_job_id: null
- tts_status: planned

This is correct for planning.

It is not correct for production rendering.

Production rendering needs:

- selected provider
- selected voice
- API access through environment variables
- real audio files
- duration validation
- loudness validation
- failure handling
- provider cost control
- no fake output

## Required starting phase

audio_renderer.py may run only when project phase is QA.

Reason:

The current canonical project P2026_TEST_001 is already in QA phase.

Rolling back from QA to AUDIO or ASSEMBLY is not allowed.

audio_renderer.py must therefore be a QA-compatible production evidence generator.

It must not mutate the canonical phase backwards.

## Required inputs

audio_renderer.py must require:

- PROJECT_STATE.json
- audio_plan.json
- script/scenes source already locked indirectly through existing artifacts
- environment variable for provider API key
- explicit provider selection
- explicit voice profile selection

Required state artifact:

- artifacts.audio_plan_path

Optional future state artifacts:

- artifacts.audio_render_path
- artifacts.voiceover_path

## Required environment variables

No API keys may be stored in source code.

No API keys may be written into JSON artifacts.

The renderer must read credentials from environment variables.

Allowed v1 environment variable names:

- ELEVENLABS_API_KEY
- OPENAI_API_KEY

The first production implementation may choose only one provider.

Do not support multiple providers in runtime until one provider path is proven stable.

## Provider decision v1

Recommended provider for v1:

ElevenLabs

Reason:

- stronger natural narration quality
- suitable for YouTube voiceover
- voice selection matters for retention
- better fit for English storytelling videos

OpenAI TTS may be evaluated later as a cheaper fallback.

Do not implement provider abstraction before first working render.

## Voice profile rule

A voice profile must be explicit.

audio_renderer.py must not silently choose a random/default voice.

Required config fields for v1 output:

- tts_provider
- voice_profile
- voice_id or provider_voice_id
- model_id if provider requires it

If the voice is not configured, renderer must fail with a clear error.

## Required output files

audio_renderer.py must write:

projects/<PROJECT_ID>/audio/audio_render.json

It may also write:

projects/<PROJECT_ID>/audio/segments/<segment_id>.mp3
projects/<PROJECT_ID>/audio/voiceover.mp3

The merged voiceover file is required before audio_ready can become true.

## audio_render.json required top-level fields

audio_render.json must include:

- project_id
- renderer
- renderer_version
- source_audio_plan_path
- tts_provider
- voice_profile
- audio_status
- audio_ready
- rendered_at
- segment_count
- rendered_segment_count
- failed_segment_count
- total_duration_sec
- target_duration_sec
- duration_validated
- loudness_validated
- voiceover_path
- segments
- warnings
- blockers
- missing_requirements

## audio_render.json segment fields

Each rendered segment must include:

- segment_id
- source_scene_id
- order
- tts_status
- voiceover_text
- audio_path
- provider_job_id
- duration_sec
- estimated_duration_sec
- duration_delta_sec
- provider_status
- error_message

## Allowed statuses

audio_status:

- rendered
- blocked
- failed

audio_ready:

- true only when all required validations pass
- false otherwise

segment tts_status:

- rendered
- blocked
- failed

provider_status:

- success
- blocked
- failed

## audio_ready rule

audio_ready may be true only if all conditions are true:

- every required segment has a real audio_path
- every audio_path exists on disk
- no segment has failed status
- rendered_segment_count equals segment_count
- voiceover_path exists
- total_duration_sec is greater than zero
- duration_validated is true
- loudness_validated is true
- blockers is empty
- missing_requirements is empty

If any condition fails, audio_ready must be false.

## Duration validation rule

audio_renderer.py must validate duration.

Minimum v1 requirement:

- each segment duration_sec must be > 0
- total_duration_sec must be > 0
- total_duration_sec must be compared against target_duration_sec
- allowed drift must be explicit

Recommended allowed drift:

- 20 percent for first production implementation

If outside allowed drift:

- audio_ready must be false
- duration_validated must be false
- blocker must explain the duration mismatch

## Loudness validation rule

audio_renderer.py must validate loudness before audio_ready can be true.

Minimum v1 rule:

- loudness_validated must not be true unless audio file was analyzed
- ffmpeg or ffprobe may be used if available
- if loudness analysis is unavailable, fail closed

Fail closed means:

- audio_ready false
- loudness_validated false
- missing_requirements includes loudness validation

Do not fake loudness validation.

## Merge rule

audio_renderer.py must create a single voiceover file.

Required output:

projects/<PROJECT_ID>/audio/voiceover.mp3

The final voiceover file must be built from segment files in order.

Segment order must follow audio_plan.audio_segments order.

If merge fails:

- audio_ready false
- voiceover_path null or missing
- blocker includes merge failure

## Idempotency rule

audio_renderer.py must be idempotent.

Repeated runs must not corrupt prior valid output.

Allowed behavior:

- overwrite generated audio_render.json
- reuse existing valid segment files if provider_job_id and audio_path are valid
- regenerate missing or failed segments
- overwrite voiceover.mp3 after successful segment validation

Disallowed behavior:

- duplicate segment files endlessly
- create random filenames without deterministic mapping
- mark audio_ready true when files are stale or missing
- silently skip failed segments

## File naming rule

Segment files must be deterministic.

Recommended pattern:

projects/<PROJECT_ID>/audio/segments/AUDIO_SEGMENT_001.mp3
projects/<PROJECT_ID>/audio/segments/AUDIO_SEGMENT_002.mp3

Merged file:

projects/<PROJECT_ID>/audio/voiceover.mp3

## API key safety rule

API keys must never be:

- hardcoded in Python
- written to audio_plan.json
- written to audio_render.json
- printed in logs
- committed to git

If an API key is missing, renderer must fail clearly.

Example blocker:

TTS API key is missing from environment.

## Cost control rule

audio_renderer.py must not render blindly without cost awareness.

Minimum v1 cost controls:

- print segment_count
- print estimated_word_count
- print provider name
- fail before provider calls if required config is missing
- do not retry infinitely
- use bounded retries

Recommended retry rule:

- max 2 retries per segment
- log provider failure without exposing secrets

## Error handling rule

No empty except blocks.

No pass-only failure handling.

Every failure must result in:

- clear error message
- blocked/failed status
- audio_ready false
- blocker or missing requirement

## Forbidden behavior

audio_renderer.py must not:

- create fake audio files
- create silent placeholder audio
- mark audio_ready true without rendered voiceover
- use placeholder provider names
- write API keys to artifacts
- call multiple providers in v1
- mutate phase backwards
- bypass QA
- delete source audio_plan.json
- modify script/scenes/assets content

## State update rule

audio_renderer.py may update PROJECT_STATE.json only by adding or updating artifact references.

Allowed:

- artifacts.audio_render_path
- artifacts.voiceover_path

Not allowed:

- setting qa_passed true
- setting approved_for_upload true
- changing phase
- removing existing artifacts
- overwriting manifest

## QA integration rule

After audio_renderer.py succeeds, qa_executor.py must be able to read audio evidence.

Minimum accepted integration path:

- qa_executor.py reads audio_plan.json for planned structure
- qa_executor.py reads audio_render.json for production audio readiness
- audio_ready check passes only if audio_render.audio_ready is true

If qa_executor.py only reads audio_plan.json, then QA will remain blocked.

Therefore QA must be updated after renderer exists.

## First implementation scope

audio_renderer.py v1 should implement only:

- one provider
- one voice profile
- mp3 output
- deterministic segment files
- merged voiceover.mp3
- duration validation
- loudness validation
- audio_render.json
- PROJECT_STATE artifact update

Do not implement:

- provider marketplace
- voice auto-selection
- multi-language voice routing
- background queue
- async batch rendering
- cloud upload
- advanced mastering
- music mixing
- sound effects

## First production target

The first target project is:

projects/P2026_TEST_001

Current known state:

- phase: QA
- audio_plan exists
- audio_status: planned
- audio_ready: false
- segment_count: 9
- estimated_duration_sec: 413
- missing provider, voice, API key, rendered files, duration validation, loudness validation

The goal is not to pass full QA yet.

The goal is to make audio_ready true with real rendered evidence.

## Exit condition

AUDIO_RENDERER_CONTRACT_V1 is complete when:

- this document exists
- audio planning and rendering are clearly separated
- provider credential rules are defined
- output schema is defined
- audio_ready rule is defined
- duration validation rule is defined
- loudness validation rule is defined
- idempotency rule is defined
- QA integration requirement is defined
- forbidden behavior is defined
- first implementation scope is limited
