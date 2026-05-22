# SCRIPT QA CONTRACT V1

Status: TRUSTED CONTRACT
Scope: Quality gate contract for FlowMind SCRIPT phase output.
Quality layer: production-retention requirements added.

## Purpose

SCRIPT QA is the first content-quality gate after SCRIPT executor.

Its purpose is to decide whether a generated script artifact is safe, useful, and strong enough to move toward SCENES.

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
- word_count
- estimated_duration_minutes
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
16. script has first-30-seconds hook pressure
17. script contains at least one retention loop
18. script avoids article mode
19. script contains scene-beat readiness
20. script contains curiosity gap or unresolved tension before the payoff
21. script contains at least one pattern interrupt
22. script has a strong end payoff

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

## Production retention rule

The script must not merely explain a topic.

The script must create a reason to keep watching.

A production-ready script should contain:

1. first-30-seconds hook pressure
2. open loop
3. tension or friction
4. escalating explanation
5. concrete example
6. pattern interrupt
7. practical reveal
8. final payoff

If the script reads like a plain article, encyclopedia entry, generic educational essay, or flat narration, verdict must be FAIL.

## First-30-seconds hook pressure rule

The opening section must create urgency, contradiction, risk, curiosity, or personal consequence within the first 30 seconds.

A weak opening fails if it only says:

- this video is about...
- today we will discuss...
- it is important to understand...
- the working title is...
- here is an overview...

A strong opening may include:

- a hidden risk
- a surprising reversal
- a direct consequence
- a contradiction between what the viewer sees and what is actually happening
- a specific problem the viewer may already have

For Money Mistakes / Invisible Costs, the opening should make the viewer feel:

- “this may already be happening to me”
- “I may be missing a cost”
- “the obvious explanation may be wrong”

## Retention loop rule

The script must introduce at least one unresolved question or tension early and resolve it later.

Examples of valid retention loops:

- “The bill is rising, but usage is not the real clue.”
- “The number people check first is often the least useful number.”
- “The appliance is not always the problem. The timing can be.”
- “The bill can change before behavior changes.”

A script fails this rule if every paragraph fully explains itself without leaving a reason to continue.

## Curiosity gap rule

The script must contain at least one curiosity gap before the practical payoff.

A curiosity gap is valid only if:

- it is relevant to the topic
- it is resolved later
- it does not use fake mystery
- it does not exaggerate unsupported claims

Bad curiosity gaps:

- “You will not believe what happens next.”
- “This secret will change everything.”
- “Experts do not want you to know this.”

Good curiosity gaps:

- “The mistake is not always using more electricity. Sometimes it is reading the wrong part of the bill.”
- “Before changing habits, separate usage from pricing.”
- “The real clue is whether kilowatt-hours changed.”

## Scene-beat readiness rule

The script must be easy to split into visual scenes.

A production-ready script should contain distinct beats such as:

- hook beat
- problem beat
- mechanism beat
- example beat
- checklist or diagnostic beat
- payoff beat
- closing beat

A script fails this rule if it is one continuous explanation with no clear scene boundaries.

The script does not need to include scene labels, but the narration must naturally support scene extraction.

## Pattern interrupt rule

The script must include at least one shift that prevents flat pacing.

Valid pattern interrupts include:

- change from explanation to example
- change from problem to diagnostic
- change from assumption to reversal
- change from general claim to concrete action
- change from cost symptom to root cause

A script fails this rule if every paragraph has the same rhythm and function.

## No article mode rule

SCRIPT QA must fail scripts that sound like an article instead of a video.

Article mode indicators:

- repeated “First / Second / Third / Fourth” without narrative tension
- overly neutral explanatory tone
- no emotional stakes
- no visualizable beats
- no direct viewer consequence
- no delayed payoff
- conclusion only summarizes the topic

Allowed:

- clear explanation
- practical advice
- simple language
- educational value

Not allowed:

- flat essay structure
- generic blog-post pacing
- narration that could be pasted into a written article without losing anything

## Payoff strength rule

The ending must leave the viewer with a clear practical or cognitive payoff.

A valid payoff should answer:

- what changed in the viewer's understanding?
- what should they check or do next?
- what false assumption did the script correct?
- why was watching until the end worth it?

A weak ending fails if it only restates the topic.

For Money Mistakes / Invisible Costs, a strong ending should separate:

- behavior problem
- pricing problem
- bill-structure problem

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

- 85

Suggested scoring:

- duration fit: 10
- hook alignment: 10
- topic match: 10
- niche match: 10
- practical payoff: 10
- voiceover usability: 10
- safety / no fake facts: 10
- first-30-seconds hook pressure: 10
- retention loop: 10
- scene-beat readiness: 5
- pattern interrupt: 5

Mandatory fail conditions override numeric score.

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
- script is in article mode
- script has no retention loop
- script has no first-30-seconds hook pressure
- script has no clear practical payoff
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
4. enforce production retention checks
5. register script_qa.json safely
6. improve semantic scoring later

## Current known gap

The current deterministic implementation may pass article-like scripts because production-retention checks are not fully implemented yet.

This contract defines the next target for implementation.

Do not claim SCRIPT QA is production-quality until the implementation enforces:

- first-30-seconds hook pressure
- retention loop
- no article mode
- scene-beat readiness
- curiosity gap
- pattern interrupt
- payoff strength

## Exit condition

SCRIPT QA v1 is complete only when:

- it runs on P2026_TEST_001
- it reads PROJECT_STATE.json
- it confirms phase SCRIPT
- it reads script.txt
- it reads script_meta.json
- it creates script_qa.json
- it registers artifacts.script_qa_path safely
- verdict is PASS only for scripts that satisfy basic quality and production-retention checks
- PROJECT_STATE.json remains valid
- no legacy station runtime is used
- git status is clean after commit

End.
