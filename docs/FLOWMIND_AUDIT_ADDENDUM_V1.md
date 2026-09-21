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
- this addendum contains only the incremental confirmed evidence
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

It proves the narrower and operationally relevant point:

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

# 3. Incremental classifications

tools/flowmind_run_phase.py

= ADAPT

engine/module_runner.py

= KEEP — FROZEN LEGACY FAIL-CLOSED GUARD

---

# 4. Expected merged audit summary

This section is informational only.

It does not replace the counters in the parent audit file until the addendum is merged.

Expected parent summary after merge:

Files materially audited:

24

Supporting runtime artifacts materially inspected:

10

Material findings:

20

Confirmed findings:

20

Confirmed RED blockers:

0

Confirmed ORANGE findings:

19

Confirmed YELLOW findings:

1

KEEP:

7

ADAPT:

17

REPLACE:

0

REMOVE:

0

UNKNOWN:

0

---

# 5. Current direction

Continue SYSTEM AUDIT MODE.

Do not implement AUDIT-020 / M-020 yet.

Do not create another orchestrator.

Continue evidence collection until audit exit conditions are satisfied.

No production implementation is authorized by this file.

End.