# SCRIPT QA CONTRACT V1

Status: TRUSTED CONTRACT
Scope: Quality gate contract for FlowMind SCRIPT phase output.

## Purpose

SCRIPT QA is the first content-quality gate after SCRIPT executor.

Its purpose is to decide whether a generated script artifact is safe and useful enough to move toward SCENES.

SCRIPT QA does not generate scripts.

SCRIPT QA does not control phase transitions by itself.

SCRIPT QA does not publish content.

SCRIPT QA does not modify protected manifest identity.

## Authority

SCRIPT QA operates under:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md
- FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- FLOWMIND_PRODUCTION_RECOVERY_PLAN_V1.md
- SCRIPT_EXECUTOR_CONTRACT_V1.md
- PROJECT_STATE.json
- canonical dispatcher control flow

## Required input

SCRIPT QA reads:

- projects/<PROJECT_ID>/PROJECT_STATE.json
- artifacts.script_path
- artifacts.script_meta_path

Required state fields:

- project_id
- phase
- artifacts
- manifest

Required manifest fields:

- niche
- audience
- content_language
- topic
- working_title
- hook
- target_duration_sec

Required artifact files:

- script.txt
- script_meta.json

## Required starting phase

SCRIPT QA may run only when:

- phase = SCRIPT

If phase is not SCRIPT, QA must fail closed.

## Output artifact

SCRIPT QA must create:

- projects/<PROJECT_ID>/script/script_qa.json

script_qa.json must contain:

- project_id
- qa_gate
- qa_version
- source_phase
- script_path
- script_meta_path
- verdict
- score
- checks
- failure_reasons
- warnings
- created_at

Allowed verdicts:

- PASS
- FAIL

## State update rule

SCRIPT QA must not directly rewrite protected manifest identity.

Allowed state output is limited to artifact registration.

Required artifact key:

- artifacts.script_qa_path

SCRIPT QA must not transition phase by itself.

Dispatcher remains responsible for any later phase transition.

## PASS requirements

SCRIPT QA may return PASS only if all mandatory checks pass.

Mandatory checks:

1. script file exists
2. script meta file exists
3. PROJECT_STATE.json is valid
4. phase is SCRIPT
5. script is non-empty
6. script has no forbidden markers
7. script word count fits target duration range
8. script starts with or strongly reflects manifest.hook
9. script clearly matches manifest.topic
10. script clearly matches manifest.niche
11. script is written in manifest.content_language
12. script has a clear structure
13. script has a practical payoff
14. script does not contain obvious fake factual claims
15. script is usable as voiceover

## Forbidden markers

SCRIPT QA must fail if the script contains:

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

## Duration rule

Estimated duration uses:

- 145 words per minute

Allowed range:

- minimum: target duration minus 20 percent
- maximum: target duration plus 20 percent

If script is outside this range, verdict must be FAIL.

## Minimum structure rule

Script should contain:

1. hook
2. problem framing
3. explanation
4. stakes
5. practical insight
6. ending

If the script is only a list, outline, note, or unfinished draft, verdict must be FAIL.

## Topic match rule

The script must stay centered on manifest.topic.

It may explain supporting context, but it must not drift into a different topic.

If topic drift is detected, verdict must be FAIL.

## Niche match rule

The script must match manifest.niche.

For Money Mistakes / Invisible Costs, the script must explain hidden or overlooked cost mechanisms.

If the script is generic life advice or unrelated finance text, verdict must be FAIL.

## Audience rule

The script must be understandable for manifest.audience.

It must avoid unnecessary technical detail unless needed.

If the script does not fit the target audience, verdict must be FAIL or include a warning depending on severity.

## Fake facts rule

SCRIPT QA must fail if the script includes:

- unsupported statistics
- invented study names
- invented expert quotes
- invented company policy claims
- invented legal or regulatory claims
- precise factual claims without source support

General explanatory claims are allowed if they are clearly framed and not pretending to cite exact facts.

## Voiceover usability rule

The script must be readable as spoken narration.

Fail if:

- too many bullet fragments
- code-like output
- metadata mixed into script
- broken sentences
- repeated paragraphs
- incomplete sections
- unnatural placeholder phrasing

## Score model

SCRIPT QA score is 0 to 100.

Minimum PASS score:

- 80

Suggested scoring:

- duration fit: 15
- hook alignment: 15
- topic match: 15
- structure: 15
- practical payoff: 15
- voiceover usability: 15
- safety / no fake facts: 10

If any mandatory fail condition appears, verdict must be FAIL regardless of numeric score.

## Fail-closed rules

SCRIPT QA must fail if:

- PROJECT_STATE.json is missing
- PROJECT_STATE.json is invalid
- phase is not SCRIPT
- artifact paths are missing
- script.txt is missing
- script_meta.json is missing
- script_meta.json is invalid
- script is empty
- script has forbidden markers
- script duration is outside allowed range
- script is not usable as voiceover
- QA output cannot be written
- state artifact registration cannot be validated

## Forbidden

SCRIPT QA must not:

- generate or rewrite script.txt
- transition SCRIPT to SCENES
- write ExecutionManifest.json
- use FM_* station artifacts as source of truth
- call legacy validators as active authority
- modify manifest.niche
- modify manifest.audience
- modify manifest.topic
- modify manifest.working_title
- modify manifest.hook
- create scenes
- create assets
- create audio
- create final video
- publish to YouTube

## Initial implementation rule

The first implementation may be deterministic.

Priority:

1. fail closed
2. detect obvious bad output
3. enforce duration and marker rules
4. register script_qa.json safely
5. improve semantic scoring later

## Exit condition

SCRIPT QA v1 is complete only when:

- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase SCRIPT
- it reads script.txt
- it reads script_meta.json
- it creates script_qa.json
- it registers artifacts.script_qa_path safely
- verdict is PASS for the current deterministic script
- PROJECT_STATE.json remains valid
- no legacy station runtime is used
- git status is clean after commit
