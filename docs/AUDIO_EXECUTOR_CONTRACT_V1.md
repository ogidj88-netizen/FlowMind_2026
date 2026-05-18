# AUDIO EXECUTOR CONTRACT V1

Status: TRUSTED CONTRACT
Scope: Production executor contract for FlowMind AUDIO phase.

## Purpose

AUDIO executor converts validated SCRIPT and ASSEMBLY artifacts into a production-ready audio plan.

AUDIO v1 does not call ElevenLabs.

AUDIO v1 does not call OpenAI TTS.

AUDIO v1 does not create an audio file.

AUDIO v1 does not create final video.

AUDIO v1 does not publish content.

AUDIO v1 does not control phase transitions by itself.

AUDIO v1 does not modify protected manifest identity.

## Why v1 is planning-only

The current pipeline has:

- script.txt
- script_meta.json
- script_qa.json
- scenes.json
- assets.json
- assembly_plan.json

But it does not yet have:

- selected TTS provider
- selected voice
- API key policy
- cost guard
- retry policy
- audio file output contract
- loudness validation
- duration validation against final assembly

Therefore AUDIO v1 must not pretend to produce a real voiceover file.

The honest v1 output is:

- audio_plan.json

Not:

- voiceover.mp3
- voiceover.wav
- final_audio.wav

## Authority

AUDIO executor operates under:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_PRODUCTION_RECOVERY_PLAN_V1.md
- SCRIPT_EXECUTOR_CONTRACT_V1.md
- SCRIPT_QA_CONTRACT_V1.md
- SCENES_EXECUTOR_CONTRACT_V1.md
- ASSETS_EXECUTOR_CONTRACT_V1.md
- ASSEMBLY_EXECUTOR_CONTRACT_V1.md
- PROJECT_STATE.json
- canonical dispatcher control flow

## Required input

AUDIO executor reads:

- projects/<PROJECT_ID>/PROJECT_STATE.json
- artifacts.script_path
- artifacts.script_meta_path
- artifacts.script_qa_path
- artifacts.assembly_plan_path

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
- assembly_plan.json

## Required starting phase

AUDIO executor may run only when:

- phase = AUDIO

If phase is not AUDIO, executor must fail closed.

## Upstream requirements

AUDIO executor may run only if:

- script.txt exists
- script_meta.json exists
- script_qa.json exists
- script_qa.verdict = PASS
- assembly_plan.json exists
- assembly_plan.json is valid JSON
- assembly_plan.render_ready = false is allowed
- assembly_plan.timeline is a non-empty list
- assembly_plan.scene_count matches timeline length

If upstream artifacts are missing or invalid, AUDIO executor must fail closed.

## Output artifact

AUDIO executor must create:

- projects/<PROJECT_ID>/audio/audio_plan.json

audio_plan.json must contain:

- project_id
- executor
- executor_version
- source_phase
- source_script_path
- source_script_qa_path
- source_assembly_plan_path
- topic
- working_title
- niche
- audience
- content_language
- target_duration_sec
- audio_status
- audio_ready
- tts_provider
- voice_profile
- estimated_word_count
- estimated_duration_minutes
- estimated_duration_sec
- audio_segments
- missing_requirements
- created_at

Allowed audio_status values:

- planned
- blocked

For AUDIO v1:

- audio_status = planned
- audio_ready = false
- tts_provider = null
- voice_profile = null

Because no real TTS provider is called.

## Audio segment structure

Each audio segment must contain:

- segment_id
- source_scene_id
- order
- voiceover_text
- estimated_word_count
- estimated_duration_sec
- tts_status
- audio_path
- provider_job_id
- production_notes

For AUDIO v1:

- tts_status = planned
- audio_path = null
- provider_job_id = null

## State update rule

AUDIO executor must not directly rewrite protected manifest identity.

Allowed state output is limited to artifact registration.

Required artifact key:

- artifacts.audio_plan_path

AUDIO executor must not transition phase by itself.

Dispatcher remains responsible for any later phase transition.

## Audio readiness rule

AUDIO v1 must set:

- audio_ready = false

unless all required audio segments have:

- tts_status = rendered
- audio_path is non-empty
- audio file exists on disk
- duration is validated
- loudness is validated

Since AUDIO v1 is planning-only, AUDIO v1 must not mark output as audio-ready.

## Missing requirements rule

AUDIO v1 must list missing audio requirements.

Minimum missing_requirements:

- selected TTS provider
- selected voice profile
- TTS API key
- rendered audio files
- audio duration validation
- loudness validation

This prevents fake progress.

## Production requirements

The audio plan must:

- preserve script meaning
- preserve assembly timeline order
- map every timeline scene to an audio segment
- preserve voiceover_text
- estimate duration from word count
- avoid adding unsupported factual claims
- avoid rewriting the script
- be usable by a future TTS executor
- be honest about missing real audio files

## Duration rule

Estimated duration uses:

- 145 words per minute

audio_plan.estimated_duration_sec must be reasonably close to manifest.target_duration_sec.

Allowed range:

- target duration minus 20 percent
- target duration plus 20 percent

If estimated duration is outside this range, executor must fail closed.

## TTS provider rule

AUDIO v1 must not call external TTS providers.

Forbidden in v1:

- ElevenLabs
- OpenAI TTS
- Google TTS
- Azure TTS
- Amazon Polly
- any browser-based TTS automation

TTS provider integration may be added later only after AUDIO v1 passes.

## API key rule

AUDIO executor must never hardcode API keys.

When real TTS is added later:

- API key must be read from environment
- missing key must fail closed
- empty provider response must fail closed
- request timeout must fail closed
- cost and retry behavior must be explicit

## Forbidden

AUDIO executor must not:

- run from ASSEMBLY phase
- run before assembly_plan_path exists
- rewrite script.txt
- rewrite script_meta.json
- rewrite script_qa.json
- rewrite scenes.json
- rewrite assets.json
- rewrite assembly_plan.json
- transition AUDIO to QA
- write ExecutionManifest.json
- use FM_* station artifacts as source of truth
- call legacy audio modules as active authority
- modify manifest.niche
- modify manifest.audience
- modify manifest.topic
- modify manifest.working_title
- modify manifest.hook
- call ElevenLabs in v1
- call OpenAI TTS in v1
- create voiceover.mp3 in v1
- create voiceover.wav in v1
- create final video
- publish to YouTube

## Fail-closed rules

AUDIO executor must fail if:

- PROJECT_STATE.json is missing
- PROJECT_STATE.json is invalid
- phase is not AUDIO
- artifacts.script_path is missing
- artifacts.script_qa_path is missing
- artifacts.assembly_plan_path is missing
- script.txt is missing
- script_qa.json is missing or invalid
- script_qa.verdict is not PASS
- assembly_plan.json is missing or invalid
- assembly_plan.timeline is empty
- any timeline item is missing voiceover_text
- any generated audio segment is missing required fields
- estimated duration is outside allowed range
- audio_plan.json cannot be written
- state artifact registration cannot be validated

## Forbidden markers

AUDIO executor must fail if script, timeline, or audio plan contains:

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

External services are not allowed in AUDIO v1.

Forbidden in v1:

- ElevenLabs
- OpenAI TTS
- Google TTS
- Azure TTS
- Amazon Polly
- Cloudinary
- FFmpeg
- YouTube API

These may be considered later only after deterministic AUDIO v1 passes.

## Initial implementation rule

The first implementation must be deterministic.

Priority:

1. valid audio_plan.json
2. honest audio_ready=false
3. full timeline-to-audio-segment mapping
4. clear missing requirements
5. fail-closed behavior
6. safe artifact registration
7. real TTS later

## Exit condition

AUDIO executor v1 is complete only when:

- project is in AUDIO phase
- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase AUDIO
- it reads script.txt
- it reads script_qa.json
- it reads assembly_plan.json
- it creates audio_plan.json
- audio_plan maps every timeline item to an audio segment
- audio_plan sets audio_ready=false
- audio_plan lists missing audio requirements
- it registers artifacts.audio_plan_path safely
- PROJECT_STATE.json remains valid
- no external TTS provider is called
- no fake audio file is created
- no legacy station runtime is used
- git status is clean after milestone commit
