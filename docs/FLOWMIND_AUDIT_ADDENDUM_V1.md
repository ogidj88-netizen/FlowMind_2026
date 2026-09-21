# FLOWMIND AUDIT ADDENDUM V1

Status: ACTIVE SUPPLEMENTAL AUDIT RECORD

Project: FlowMind / Imagine What If

Mode: SYSTEM AUDIT MODE

Authority: NONE

Parent audit record:

docs/FLOWMIND_AUDIT_FINDINGS_V1.md

Purpose:

Capture newly confirmed audit findings without repeatedly replacing the large parent audit record during an active inspection block.

This file exists to reduce:

- copy/paste risk
- accidental loss of previously verified findings
- unnecessary full-file rewrites
- audit-loop overhead

This file is not:

- operational authority
- target architecture
- a replacement for FLOWMIND_AUDIT_FINDINGS_V1.md
- implementation authorization
- an independent modernization authority

Merge rule:

Confirmed findings in this addendum must be merged into:

docs/FLOWMIND_AUDIT_FINDINGS_V1.md

at the next meaningful audit checkpoint or before SYSTEM AUDIT MODE is exited.

Until that merge:

- the parent file remains the accumulated audit record
- this addendum contains only incremental confirmed evidence
- do not duplicate or renumber earlier findings
- do not maintain a second competing audit model

---

# 1. Incremental findings

## AUDIT-020 — No verified canonical autonomous Core Lite orchestration path exists in the inspected tracked runtime contour

Components:

- tools/flowmind_run_phase.py
- current tracked orchestration contour

Related component:

engine/module_runner.py

Classification:

tools/flowmind_run_phase.py = ADAPT

engine/module_runner.py = KEEP as FROZEN LEGACY fail-closed guard

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

tools/flowmind_run_phase.py was inspected completely.

Its phase mapping is:

SCRIPT
-> engine/executors/script_executor.py

SCENES
-> engine/executors/scenes_executor.py

ASSETS
-> engine/executors/assets_executor.py

ASSEMBLY
-> engine/executors/assembly_executor.py

AUDIO
-> engine/executors/audio_executor.py

QA
-> engine/executors/qa_executor.py

run_phase() performs the following sequence:

- validate PROJECT_STATE
- read current state.phase
- reject HALT
- reject READY_FOR_UPLOAD / UPLOADED / ARCHIVED
- resolve one executor for the current phase
- build one subprocess command
- execute that one command
- return that subprocess exit code

The runner does not itself provide an ordered multi-step execution plan for required production operations inside a phase.

Previously inspected required production components are not mapped by this runner, including:

- engine/executors/script_qa.py
- engine/executors/asset_resolver.py
- engine/executors/audio_renderer.py
- tools/audio_loudness_report.py
- tools/apply_audio_loudness_report.py
- engine/executors/final_render_executor.py
- engine/executors/visual_pacing_executor.py

Repository reference discovery found:

engine/module_runner.py

as the only tracked external reference to:

tools/flowmind_run_phase.py

engine/module_runner.py was then inspected completely.

It does not call flowmind_run_phase.py.

It is an intentionally disabled legacy runner.

Its runtime behavior is:

- print FLOWMIND_LEGACY_RUNNER_DISABLED
- explain that engine/module_runner.py is frozen legacy
- direct operators toward tools/flowmind_run_phase.py and tools/dispatcher.sh
- exit with status 2

Therefore engine/module_runner.py is not an active orchestration caller.

Additional source discovery was performed for scheduler and application integration.

Searches for tracked Python implementation containing:

- APScheduler
- AsyncIOScheduler
- BackgroundScheduler
- add_job

did not identify a scheduler runtime entrypoint.

Searches for FastAPI application patterns including:

- FastAPI(
- uvicorn
- lifespan
- startup hooks
- APIRouter
- include_router

returned no tracked Python matches.

Direct tracked Python import searches for:

- fastapi
- apscheduler

also returned no matches.

A further search across tracked automation/configuration surfaces for:

- cron
- crontab
- scheduler configuration
- workflow_dispatch
- docker compose
- launchd
- LaunchAgent
- systemd
- apscheduler
- uvicorn
- fastapi
- flowmind_run_phase

returned no additional external automation path in the searched file classes.

Evidence boundary:

This finding does not prove that no manual command, untracked external machine configuration, external service, or unknown runtime mechanism could ever invoke FlowMind components.

It proves the narrower operational point:

Within the inspected tracked repository contour, no canonical autonomous Core Lite runtime has been found that deterministically executes the complete verified production sequence.

The currently verified implementation is primarily:

canonical state
+
dispatcher
+
single-phase CLI runner
+
independent executors/tools

rather than one verified autonomous end-to-end runtime contour.

Positive evidence:

tools/flowmind_run_phase.py contains useful control behavior that should be preserved:

- canonical load_state() validation
- HALT refusal
- explicit refusal of release/upload/archive phases
- legacy executor-path protection
- explicit executor existence check
- .venv Python preference
- sys.executable fallback
- subprocess invocation without shell execution
- propagated executor exit code

engine/module_runner.py also correctly fails closed rather than silently running its historical legacy path.

Risk:

A complete video-production run cannot currently be demonstrated from repository evidence as one autonomous canonical execution path.

This creates risk of:

- manual substep ordering
- missed required substeps
- inconsistent recovery behavior
- ambiguous restart/resume points
- scheduler bypass of canonical guards
- artifact readiness being assumed rather than orchestrated
- different CLI paths producing different execution contours
- inability to prove unattended end-to-end operation

This finding is related to, but distinct from:

AUDIT-015

AUDIT-015 concerns inconsistent lifecycle and phase semantics.

AUDIT-020 concerns the absence of a verified canonical runtime that executes all required production work autonomously.

Required outcome:

Create one canonical execution contour.

The target relationship should be conceptually:

PROJECT_STATE
-> canonical phase execution plan
-> required ordered substeps
-> artifact validation after each required substep
-> phase completion
-> canonical dispatcher transition
-> next phase

A phase may contain multiple required capabilities.

Do not force:

phase
=
one executor process

when actual production requires multiple validated operations.

The canonical execution path must be:

- deterministic
- fail-closed
- idempotent where operations are repeatable
- restartable from verified state
- observable
- artifact-aware
- compatible with HALT/resume rules
- consistent with canonical phase transitions

Manual CLI execution and future scheduled execution should reuse the same canonical execution path.

Do not create a second orchestrator.

If FastAPI + APScheduler remain the selected Core Lite stack, they should act as thin control/trigger layers over the same canonical execution contour rather than implementing separate production logic.

Resolution:

OPEN

---

## AUDIT-021 — No verified YouTube publishing implementation exists in the inspected tracked executable contour

Component:

YouTube publishing / release capability

Classification:

MISSING CAPABILITY — modernization required

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

Repository discovery was performed for publishing-specific implementation signals including:

- googleapiclient
- MediaFileUpload
- youtube.videos
- videos().insert
- videos.insert
- privacyStatus
- publishAt
- YouTube upload naming patterns

The initial search found lifecycle/release-state components including:

- engine/canonical_dispatcher.py
- engine/executors/qa_executor.py
- engine/state_validator.py
- tools/dispatcher_cli.py
- tools/flowmind_run_phase.py
- validation/bootstrap helpers

These components express release semantics such as:

READY_FOR_UPLOAD

and:

approved_for_upload

but do not establish provider execution.

A provider-specific search across tracked:

- Python
- JavaScript
- TypeScript
- shell

returned only:

cashflow/topic_intelligence/validator.py

That file was inspected completely for the purpose of determining whether it implements YouTube publishing.

It does not.

Its YouTube behavior is:

topic
-> HTTP GET to YouTube Data API search endpoint
-> fetch video titles
-> compare normalized title tokens with topic tokens
-> return topic-validation result

It does not implement:

- video upload
- media transfer
- videos.insert publishing
- privacy-status configuration
- scheduled publication
- upload result persistence
- remote YouTube video identity persistence
- READY_FOR_UPLOAD -> UPLOADED provider execution

Evidence boundary:

This finding does not prove that no manual uploader or external untracked service exists.

It proves:

No canonical YouTube publishing implementation was found in the inspected tracked executable repository contour.

Risk:

The lifecycle contains release/upload semantics, but repository evidence does not show a capability that can execute the final publication operation.

Therefore:

READY_FOR_UPLOAD

does not currently have a verified canonical path to:

YouTube publication
-> verified remote result
-> UPLOADED

Required outcome:

Create one canonical YouTube publishing capability behind an explicit provider contract.

Publishing must happen only after:

- QA PASS
- explicit release approval
- READY_FOR_UPLOAD

The capability must:

- receive a canonical final media artifact
- receive canonical publication metadata
- perform the provider operation
- persist remote video identity/status
- normalize provider errors
- fail closed
- support safe retry behavior
- avoid accidental duplicate uploads
- respect provider quota/rate constraints
- transition to UPLOADED only after verified provider success

Release approval and publishing execution must remain separate concerns.

Resolution:

OPEN

---

## AUDIT-022 — No verified external visual/media provider integration exists in the inspected tracked runtime contour

Component:

External visual/media provider capability

Classification:

MISSING CAPABILITY — modernization required

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

Repository discovery was performed for direct provider names and SDK/API indicators covering:

- Cloudinary
- Luma
- Dream Machine
- Runway
- Pika
- Kling
- Veo
- Replicate
- fal.ai

No matching tracked executable/configuration integration was found.

A second independent search was performed for provider-specific environment variables, domains and API signatures including:

- CLOUDINARY_
- cloudinary.com
- LUMA_
- lumalabs
- RUNWAY_
- runwayml
- REPLICATE_
- replicate.com
- FAL_KEY
- fal.ai
- PIKA_
- KLING_
- VEO_

That search also returned no matches in the inspected tracked code/configuration surfaces.

This source-discovery result is consistent with previously confirmed:

AUDIT-008

where:

engine/executors/asset_resolver.py

operates in:

local_existing_only

mode.

The currently verified visual/media contour is therefore effectively:

asset requirements
-> local/manual asset resolution
-> assembly/render

rather than:

creative intent
-> provider capability request
-> external provider
-> normalized artifact
-> validation
-> renderer

Evidence boundary:

This finding does not prove that external provider accounts, credentials or manual workflows never existed.

It proves:

No runtime integration for the searched external visual/media providers was found in the inspected tracked repository contour.

Risk:

FlowMind cannot currently demonstrate autonomous acquisition or generation of required visual media through the target provider layer.

This limits:

- unattended production
- topic-specific asset generation
- visual diversity
- provider replacement
- cost-aware routing
- provenance tracking
- scaling beyond locally available media

Required outcome:

Introduce a provider-neutral visual/media execution contract.

Minimal target flow:

asset requirement
-> capability request
-> selected provider adapter
-> normalized provider result
-> artifact validation
-> persisted provenance and cost
-> canonical production artifact

Do not integrate many providers initially.

One production-capable provider adapter is sufficient for the first canonical path.

Additional providers should be added only where:

- reliability
- quality
- cost
- availability
- capability

justify the complexity.

Resolution:

OPEN

---

## AUDIT-023 — No verified active Brain/LLM provider integration exists; the only discovered OpenAI implementation is frozen legacy

Components:

- active Brain / Editorial provider capability
- engine/modules/s2_script.py

Operational status of engine/modules/s2_script.py:

FROZEN LEGACY

Audit disposition:

REMOVE

Severity:

ORANGE

Status:

CONFIRMED — OPEN

Evidence:

Repository discovery was performed for LLM/provider indicators including:

- OpenAI
- Anthropic
- Claude
- Gemini
- Google GenAI
- xAI
- Grok
- OPENAI_
- ANTHROPIC_
- GEMINI_
- GOOGLE_API_KEY
- XAI_

The only matching tracked executable source was:

engine/modules/s2_script.py

That file was inspected completely.

It contains a real OpenAI integration.

It:

- loads OPENAI_API_KEY from environment
- constructs OpenAI(api_key=...)
- calls client.chat.completions.create(...)
- uses model="gpt-4o"
- requests generated script text
- retries generation up to MAX_ATTEMPTS
- validates generated word count
- estimates narration duration

Positive donor behavior includes:

- environment-based secret loading
- bounded generation attempts
- explicit output-length validation
- controlled empty-response failure
- useful duration estimation

However this implementation is not part of the verified active contour.

Previously verified:

tools/flowmind_run_phase.py

explicitly forbids executor paths containing:

engine/modules/

Previously verified:

engine/module_runner.py

is a frozen legacy fail-closed guard.

It explicitly states that:

engine/module_runner.py is frozen legacy

and exits with status 2 rather than routing production through engine/modules.

Therefore the discovered OpenAI implementation is not verified as active Brain execution.

Additional source evidence inside engine/modules/s2_script.py confirms why it must not be reactivated directly.

It implements its own PROJECT_STATE access:

- calculates projects/<project_id>/PROJECT_STATE.json
- reads JSON directly
- validates state locally
- writes PROJECT_STATE.json directly

It does not use the canonical active state layer:

- engine.state_validator.load_state
- engine.state_store.save_state_with_disk_guard

Its save_state() performs a direct JSON overwrite.

It also uses legacy state assumptions including top-level:

- topic
- title
- hook

rather than the verified current canonical manifest contract.

Its generated script behavior is hard-coded to:

cashflow-style video

and its system prompt explicitly targets:

high-retention financial explainer content

Therefore it also embeds historical niche intelligence.

Repeated direct execution can regenerate script content and overwrite state/artifact references without canonical execution identity or active orchestration control.

Evidence boundary:

This finding does not claim that FlowMind has never generated content using OpenAI.

It proves the narrower current implementation fact:

The only LLM provider integration discovered in the inspected tracked executable repository is inside a frozen legacy module that is explicitly excluded from the verified active execution path.

The active current SCRIPT implementation previously inspected:

engine/executors/script_executor.py

does not use an external LLM provider.

It generates predominantly hard-coded historical niche content.

Risk:

The current active contour does not have a verified provider-backed Brain / Editorial generation capability.

Reactivating engine/modules/s2_script.py directly would reintroduce:

- non-canonical state writes
- legacy state schema assumptions
- niche coupling
- direct provider coupling
- unsafe overwrite behavior
- a second script-production path

Required outcome:

Do not reactivate engine/modules/s2_script.py.

Extract only useful donor ideas.

Create the active Brain / Editorial generation capability through the canonical architecture.

Minimal target flow:

canonical creative request
-> Brain / Editorial decision contract
-> provider adapter
-> normalized generated result
-> deterministic validation
-> canonical artifact persistence
-> Script QA

Initial implementation may use one LLM provider.

Do not build dynamic multi-provider routing prematurely.

The provider/model should be replaceable through a stable adapter/configuration boundary.

Persist sufficient generation provenance where useful, including:

- provider
- model
- generation configuration
- source request identity
- artifact identity
- cost/usage where available

Secrets must remain environment-based.

engine/modules/s2_script.py should remain unreachable until its useful donor concepts are migrated, after which the legacy implementation should be removed.

Resolution:

OPEN

---

# 2. Incremental modernization backlog

## M-020 — Canonical autonomous Core Lite execution contour

Source:

AUDIT-020

Related findings:

- AUDIT-001
- AUDIT-007
- AUDIT-015
- AUDIT-016

Required outcome:

Define and implement one canonical production execution path that knows all required operations for the current lifecycle stage.

Replace the effective:

phase
-> one executor

assumption with an explicit ordered phase execution plan where needed.

Example concept:

SCRIPT
-> script production
-> Script QA
-> validate required artifacts
-> canonical transition

ASSETS
-> asset requirements
-> asset resolution
-> validate resolved assets
-> canonical transition

AUDIO
-> narration plan
-> audio rendering
-> loudness measurement
-> loudness validation/application
-> validate final audio artifacts
-> canonical transition

Later production work must likewise have one deterministic place in the lifecycle before final QA.

Preserve useful safety behavior from:

tools/flowmind_run_phase.py

Do not duplicate dispatcher responsibilities.

The dispatcher remains responsible for canonical lifecycle transitions.

The execution layer is responsible for completing and validating the work required before requesting that transition.

If APScheduler is retained:

APScheduler
-> trigger canonical execution path

not:

APScheduler
-> bypass canonical execution rules

If FastAPI is retained:

FastAPI
-> control/status/trigger surface

not:

FastAPI
-> second orchestration implementation

---

## M-021 — Canonical YouTube publishing capability

Source:

AUDIT-021

Related findings:

- AUDIT-007
- AUDIT-015
- AUDIT-016
- AUDIT-020

Required outcome:

Implement one canonical YouTube publishing adapter/capability.

Target relationship:

QA PASS
-> explicit release approval
-> READY_FOR_UPLOAD
-> YouTube publishing capability
-> normalized provider result
-> verified remote identity
-> UPLOADED

The capability must be safe under retries and must not silently create duplicate uploads.

Do not couple canonical lifecycle state directly to provider-specific response structures.

---

## M-022 — Provider-neutral visual/media execution capability

Source:

AUDIT-022

Related findings:

- AUDIT-005
- AUDIT-006
- AUDIT-008
- AUDIT-020

Required outcome:

Provide one stable visual/media capability contract between production intent and external providers.

Target relationship:

asset requirement
-> capability request
-> provider adapter
-> normalized artifact
-> validation
-> provenance/cost
-> production timeline

Start with one provider that satisfies the first production requirement.

Do not add multiple provider integrations until real quality, reliability or cost evidence requires them.

---

## M-023 — Canonical Brain / Editorial LLM capability

Source:

AUDIT-023

Related findings:

- AUDIT-004
- AUDIT-017
- AUDIT-019
- AUDIT-020

Required outcome:

Create one canonical provider-backed Brain / Editorial generation path.

Do not reactivate:

engine/modules/s2_script.py

directly.

Preserve only useful donor concepts such as:

- environment-based secret loading
- bounded retries
- output validation
- duration estimation

Replace legacy behavior with:

canonical request
-> Brain / Editorial contract
-> provider adapter
-> normalized generation result
-> deterministic validation
-> canonical artifact persistence
-> Script QA

Provider/model selection must be replaceable without editing production orchestration.

Initial implementation should use the simplest provider setup that delivers the required quality.

Dynamic routing is deferred until justified by production evidence.

---

# 3. Incremental classifications

tools/flowmind_run_phase.py

= ADAPT

engine/module_runner.py

= KEEP — FROZEN LEGACY FAIL-CLOSED GUARD

engine/modules/s2_script.py

= REMOVE — FROZEN LEGACY; DONOR-ONLY UNTIL REMOVAL

---

# 4. Expected merged audit summary

This section is informational only.

It does not replace the counters in the parent audit file until the addendum is merged.

Expected parent summary after merge:

Files materially audited:

25

Supporting runtime artifacts materially inspected:

10

Material findings:

23

Confirmed findings:

23

Confirmed RED blockers:

0

Confirmed ORANGE findings:

22

Confirmed YELLOW findings:

1

KEEP:

7

ADAPT:

17

REPLACE:

0

REMOVE:

1

UNKNOWN:

0

---

# 5. Current provider / autonomy picture

Verified current active implementation contains:

- canonical state validation/storage
- canonical dispatcher
- single-phase CLI runner
- deterministic production executors
- ElevenLabs audio provider integration
- local-only asset resolution
- final rendering
- QA/readiness logic

No verified active canonical implementation has been found for:

- autonomous Core Lite scheduling/orchestration
- YouTube publishing
- external visual/media generation/resolution
- active Brain / Editorial LLM generation

A real OpenAI integration exists only in:

engine/modules/s2_script.py

which is frozen legacy and excluded from the verified active contour.

This separation between:

target capabilities

and:

verified current implementation

must remain explicit during modernization planning.

---

# 6. Current direction

Continue SYSTEM AUDIT MODE only until the remaining audit exit-condition evidence is sufficient.

Do not implement:

- AUDIT-020 / M-020
- AUDIT-021 / M-021
- AUDIT-022 / M-022
- AUDIT-023 / M-023

yet.

Do not create another orchestrator.

Do not reactivate engine/modules/s2_script.py.

Do not add multiple providers prematurely.

No production implementation is authorized by this file.

End.