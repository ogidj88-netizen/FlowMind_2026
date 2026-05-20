# FLOWMIND_ACTIVE_MAP

Status: ACTIVE MAP
Scope: FlowMind / Imagine What If
Mode: SYSTEM MAP MODE

## 1. Purpose

This is the single active programming map for FlowMind.

The assistant must use this file before technical work to understand:

- where we are now
- what the next allowed step is
- what is forbidden now
- what the full pipeline is
- when to stop

If this file conflicts with older docs, this file controls the current workflow unless the user explicitly changes the active map.

## 2. Current mode

Current mode:

SYSTEM MAP MODE

Meaning:

- inspect the current repository
- identify active modules
- identify module inputs and outputs
- identify gates and handoffs
- classify files as TRUSTED, FROZEN LEGACY, or UNVERIFIED
- confirm one active runtime contour
- do not tune final video quality yet

## 3. Current step

Current step:

Repo / module inventory and active-contour confirmation.

Goal of this step:

- understand what exists
- understand what is active
- separate active runtime from archive / legacy / tests
- map how artifacts move between modules
- identify which gates already work
- identify which gates are missing or weak

## 4. Allowed next action

Allowed next action:

Inspect repository structure and classify modules/files.

Allowed actions now:

- read files
- inspect docs
- inspect executors
- inspect project artifacts
- inspect JSON validity
- inspect git status
- create documentation that prevents drift
- run preflight before documentation commits

Allowed commands:

- git status
- git log
- find
- grep
- cat
- sed
- python3 -m json.tool
- bash tools/preflight.sh

## 5. Forbidden current actions

Forbidden now:

- tune final video quality
- change renderer behavior
- add Telegram integration
- add Pexels/Pixabay integration
- add YouTube upload automation
- add new production modules
- open upload gate
- rewrite module logic before inventory is complete
- mix active runtime with donor / archive / legacy files

## 6. Active pipeline

FlowMind pipeline:

0. System Foundation  
   active map, trust boundary, one active contour, canonical state, map guard.

1. Topic / Niche / Strategy  
   chooses topic, demand angle, audience, working title, and whether the video is worth producing.

2. Script Engine  
   creates script, hook, structure, pacing, and script QA.

3. Director / Scenes  
   splits script into scenes and defines what appears on screen, timing intent, asset needs, and visual rules.

4. Assets / Stock / Licenses  
   finds/selects assets, resolves local media files, checks license status, and writes resolved assets.

5. Audio  
   creates audio plan, renders TTS, validates durations, and validates loudness.

6. Assembly  
   connects scenes, assets, and audio by Audio Master Clock and writes timeline/readiness flags.

7. Final Render  
   renders final video with FFmpeg and writes final render report.

8. QA / Readiness  
   checks blockers, readiness score, qa_passed, and approved_for_upload.

9. Human Review / Telegram / Upload  
   sends preview to user, waits for approve/reject, uploads only after approval.

10. Module Quality Hardening  
   returns to each module, improves output quality, and moves forward only after proof.

## 7. Current known state

Known current state:

- basic skeleton exists
- final video can be rendered
- audio layer works better than visual layer
- QA blocks upload
- visual pacing prototype works technically
- blind motion made informational cards worse
- video quality is not yet production-ready
- module boundaries still need review

Current interpretation:

The system can create a rough draft video, but the skeleton and nervous system must be reviewed before quality tuning.

## 8. Required MAP CHECK

Every technical response must start with:

MAP CHECK  
Active map:  
Current step:  
Allowed action:  
Forbidden action:  
Evidence:  
Verdict:

If the assistant cannot fill this block clearly, it must stop.

## 9. Stop rule

Stop if:

- current step is unknown
- user asks "по карті що далі?" and source is unclear
- git is dirty and dirty work was not approved
- task pulls into local bug-fixing while mode is SYSTEM MAP MODE
- action creates a second active contour
- action mixes active, donor, archive, or legacy
- action uses production placeholders, stubs, or fake outputs
- assistant cannot explain why the next file belongs to the current step

## 10. Exit condition for current step

This step is complete only when we have a module inventory table with:

- module name
- file path
- input artifact
- output artifact
- downstream consumer
- runtime proof
- status: TRUSTED / FROZEN LEGACY / UNVERIFIED
- readiness percentage
- next action

## 11. One-step rule

Work proceeds:

one step -> user says "виконано" or pastes output -> next step

No automatic jumping ahead.

End.
