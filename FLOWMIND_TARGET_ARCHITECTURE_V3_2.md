# FLOWMIND TARGET ARCHITECTURE V3.2

Status: TRUSTED DETAILED TARGET ARCHITECTURE
Project: FlowMind / Imagine What If
Version: 3.2
Mode: REFERENCE TARGET SYSTEM MAP
Date: 2026-09-25
Scope: detailed target architecture only; not current operational authority; not runtime proof

---

# 1. PURPOSE

This document defines the FlowMind V3.2 trusted detailed target architecture.

V3.2 consolidates:

- the trusted V3.1 target architecture
- finalized Opportunity Intelligence V1 decisions
- finalized Control Plane V1 decisions
- finalized Editorial Brain V1 decisions
- finalized Production Brain / Director V1 decisions
- finalized Quality + Compliance V1 decisions
- finalized Learning Loop V1 decisions
- existing Capability Evolution principles
- provider abstraction
- cost and latency governance
- rights and compliance
- persistent evidence and decision memory
- bounded autonomy
- cloud-first operation
- verified architecture/runtime separation rules

V3.2 does not discard valid V3.1 principles merely because the version number changed.

Its purpose is to:

- clarify ownership
- remove duplicated responsibility
- remove hidden competing authorities
- formalize critical contracts
- preserve auditability
- strengthen artifact identity and invalidation
- separate deterministic control from creative intelligence
- separate content learning from capability evolution
- prevent silent degradation
- prevent premature autonomous optimization
- preserve Minimalism / ROI discipline

V3.2 is intentionally conservative.

The system should remain only as complex as required to improve:

- content quality
- viewer value
- runtime stability
- production completion
- release speed
- automation
- adaptability
- cost control
- monetization potential

This document does not prove implementation.

A capability is operationally real only after relevant evidence demonstrates:

- valid implementation
- valid input
- successful execution
- expected output
- downstream consumption where applicable
- validation
- observable failure behaviour where applicable

Authority identity is resolved by:

FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

This document remains detailed target architecture only.

It does not define current operational state and does not prove runtime implementation.

---

# 2. CORE ARCHITECTURAL PRINCIPLE

FlowMind is not a primitive generation chain:

topic
-> script
-> images
-> voice
-> video

FlowMind is a bounded decision system:

signals
-> opportunity decision
-> editorial promise
-> packaging
-> narrative
-> production direction
-> canonical audio
-> timed audiovisual execution
-> media resolution
-> deterministic render
-> quality and compliance
-> authorized delivery
-> observation
-> evidence
-> learning
-> versioned policy
-> better future decisions

In parallel:

provider/model ecosystem
-> capability candidates
-> benchmark
-> canary
-> capability promotion
-> better execution tools

The system must:

BUILD decision logic

and:

BUY / reuse commodity capabilities

where practical.

FlowMind-owned IP should concentrate on:

1. Opportunity Intelligence decision logic
2. Editorial decision logic
3. Production / Director decision logic
4. Media-routing and fallback policy
5. Quality and Compliance contracts
6. Content Learning decision logic
7. Capability Evolution policy
8. evidence, policy and audit contracts

Commodity capabilities should remain replaceable:

- general-purpose LLMs
- research/search providers
- image generation
- video generation
- TTS
- stock providers
- music/SFX providers
- multimodal analysis
- generic render infrastructure
- analytics collection APIs

Provider identity must not unnecessarily leak into domain business logic.

---

# 3. V3.2 SYSTEM STRUCTURE

FlowMind V3.2 contains seven logical system blocks:

0. Control Plane
1. Opportunity Intelligence
2. Editorial Brain
3. Production Brain
4. Render, Quality & Compliance
5. Delivery & Content Learning
6. Capability Evolution

Cross-cutting foundations:

- Persistent State
- Evidence and Decision Memory
- Policy Store
- Capability Registry
- Provider Abstraction
- Human Decision Gateway
- Cost and Latency Governance
- Rights Evidence
- Observability and Auditability
- Secrets and Access Discipline
- Cloud-First Runtime
- Artifact Identity and Dependency Tracking

These are logical ownership boundaries.

They do not require:

- seven Python files
- seven services
- seven agents
- seven databases
- seven processes

Internal implementation should use the smallest structure that preserves:

- single authority
- clear ownership
- inspectability
- deterministic transitions
- idempotency
- testability
- version identity
- recoverability
- runtime reliability

No logical block may silently become a second Control Plane.

---

# 4. BLOCK 0 - CONTROL PLANE

## 4.1 Purpose

The Control Plane owns execution authority.

It must remain:

- narrow
- deterministic
- non-creative
- fail-closed
- observable
- idempotent
- recoverable

It does not decide:

- topic quality
- viewer promise
- title quality
- thumbnail quality
- hook quality
- script creativity
- visual style
- creative fallback
- QA verdict content
- learning hypotheses

Those responsibilities belong to domain blocks.

---

## 4.2 Single Execution Authority

FlowMind must have one canonical execution/state authority.

Do not introduce a second:

- dispatcher
- runner authority
- scheduler authority
- canonical state machine
- project-state owner
- phase controller
- policy-activation authority
- hidden runtime contour

Compatibility code may exist.

It must remain subordinate to canonical control.

---

## 4.3 Canonical Project Phase

The canonical macro lifecycle phase remains the project-level phase authority.

Domain modules may have internal sub-steps.

Internal sub-steps must not become competing project lifecycle authorities.

Project phase and internal module progress are different concepts.

---

## 4.4 Orthogonal Runtime State

V3.2 distinguishes macro project phase from runtime execution state.

Project runtime state may include:

- ACTIVE
- WAITING_HUMAN
- HALTED
- COMPLETED

Operation state may include:

- PENDING
- CLAIMED
- RUNNING
- SUCCEEDED
- FAILED
- OUTCOME_UNKNOWN
- CANCELLED

Provider-health state may include:

- HEALTHY
- DEGRADED
- RATE_LIMITED
- DOWN
- DISABLED

Approval state is separate from operation state.

These dimensions must not be collapsed into one overloaded phase field.

---

## 4.5 Logical Operation vs Attempt

A logical operation is the durable identity of intended work.

An attempt is one execution try.

These identities must not be conflated.

Example:

logical operation:
generate canonical narration for script hash X

attempt 1:
provider timeout

attempt 2:
provider returns ambiguous response

attempt 3:
successful reconciled result

Retries must preserve logical-operation identity.

Provider identity should not automatically become part of logical-operation identity unless the business contract materially requires it.

---

## 4.6 Claim and Lease Semantics

A worker may claim executable work.

Where concurrent execution risk exists, ownership may be bounded by a lease.

Lease expiry does not prove provider failure.

Timeout does not prove external side-effect failure.

Heartbeat should be introduced only where runtime evidence justifies it.

Do not build complex worker leasing machinery before concurrent execution creates a real need.

---

## 4.7 OUTCOME_UNKNOWN

External operations may have ambiguous side effects.

Examples:

- paid generation request timed out after submission
- upload call returned no final confirmation
- provider accepted request but local response was lost

In such cases:

timeout
!=
known failure

The operation becomes:

OUTCOME_UNKNOWN

The system must:

- stop unsafe blind retry
- reconcile provider/external state
- determine whether the side effect occurred
- recover the known result where possible
- retry only when safe
- HALT when ambiguity cannot be resolved safely

This is especially important for:

- paid provider calls
- publication
- irreversible external actions

---

## 4.8 Reconciliation

Startup and recovery reconciliation should be mechanical.

It may inspect:

- canonical operation state
- artifacts
- external provider job IDs
- final hashes
- expected outputs
- publication state

Reconciliation must not invent creative decisions.

Its purpose is to restore known execution truth.

---

## 4.9 Artifact Validation Before Success

An operation must not become SUCCEEDED solely because:

- a subprocess exited zero
- an API returned 200
- a file path exists

Success requires applicable artifact validation.

Examples:

- file exists
- file is readable
- schema is valid
- hash is recorded
- required fields are present
- expected downstream contract is satisfied

Domain-specific semantic validation remains owned by the relevant domain module.

---

## 4.10 HALT Contract

A HALT must be explicit and structured.

A HALT record should contain where applicable:

- halt_reason
- severity
- required_actor
- required_action
- resume_from
- resume_conditions
- relevant artifact refs
- relevant operation refs
- policy version
- failure evidence

HALT must never silently convert into success.

Resume must go through canonical control rules.

---

## 4.11 Cost Lifecycle

For paid operations, Control Plane / Cost Governance should support:

ESTIMATE
-> RESERVE
-> CALL
-> SETTLE

The system should distinguish:

- estimated cost
- reserved cost
- actual cost
- released reservation
- unknown/unsettled cost where applicable

Paid ambiguous calls must not be blindly retried.

---

## 4.12 Policy Pinning

Execution must know which policy version applies.

Policy versions are immutable objects.

The Control Plane owns the active-policy binding used for a specific project/operation.

A Policy Store must not independently become a second active-policy authority.

Running work should retain the pinned policy identity necessary for reproducibility.

Emergency safety overrides may stop execution.

They must be auditable.

---

## 4.13 Human Approval

Human approval is separate from domain verdicts.

Approval must bind to the exact relevant artifact/version/hash.

If the approved artifact materially changes:

approval becomes STALE

Approval must not silently migrate to a changed artifact.

---

## 4.14 Channel Identity

channel_id should be available from Day One where channel scope matters.

Channel identity may affect:

- strategy
- policy scope
- learning
- publication
- compliance
- format behaviour

Do not infer channel scope from provider configuration.

---

# 5. BLOCK 1 - OPPORTUNITY INTELLIGENCE

## 5.1 Purpose

Opportunity Intelligence determines:

- what deserves attention
- why now
- whether an opportunity belongs to current strategy
- whether to MAKE, PREPARE, WATCH or REJECT

It does not own:

- title
- thumbnail
- hook
- narrative
- script
- visual direction

Those belong downstream.

---

## 5.2 Signal Source Classes

V3.2 may consume five principal classes of signals.

### YouTube Public Market Signals

Examples:

- uploads
- public views
- engagement
- upload frequency
- topic recurrence
- market velocity
- unusual performance relative to local baseline

### Our YouTube Analytics

Examples where available:

- CTR
- retention
- watch time
- average percentage viewed
- subscriber conversion
- revenue
- topic performance
- packaging performance
- production outcomes

### Competitor / Market Watchlists

Watchlists should consider:

- niche relevance
- audience similarity
- format similarity
- growth state
- repeatability
- transferability
- available evidence

A single viral video is not a reusable pattern.

### Search / Trend Signals

Supporting evidence only.

### News / Event Signals

Examples:

- product launches
- platform updates
- pricing changes
- policy changes
- feature releases
- security incidents
- market events

News is a signal.

It is not automatically a video idea.

---

## 5.3 Signal Processing

Target flow:

COLLECT
-> NORMALIZE
-> DEDUPLICATE
-> SOURCE COLLAPSE
-> CANDIDATE FORMATION
-> FEATURE ASSESSMENT
-> HARD GATES
-> WHY NOW
-> DECISION POLICY
-> MAKE / PREPARE / WATCH / REJECT

Multiple articles about one event must not become independent evidence merely because URLs differ.

Source count != source independence.

---

## 5.4 Opportunity Candidate Contract

The Opportunity Candidate owns:

- topic
- market_angle
- viewer_intent
- target_audience / target_context
- format_hint
- market_evidence

Where relevant it should also retain:

- candidate_id
- parent_topic_id
- source_refs
- created_at
- freshness state
- strategic alignment
- exploration tag

Opportunity Candidate does not own final:

- viewer promise
- title
- thumbnail
- hook
- script

---

## 5.5 Coverage Gap

Coverage Gap describes a market/content coverage condition.

It is not a fake competitor-quality judgment.

Allowed states:

- HIGH
- MEDIUM
- LOW
- UNKNOWN

UNKNOWN must not silently become LOW.

Absence of a signal is not equivalent to confirmed absence.

---

## 5.6 Opportunity Assessment Axes

V3.2 does not require one aggregate opportunity score.

Useful categorical axes may include:

- DEMAND
- SUPPLY
- COVERAGE_GAP
- OUR_EDGE
- AUDIENCE_FIT
- WHY_NOW
- BUSINESS_VALUE
- EXECUTION_FEASIBILITY
- RISK
- REPEATABILITY

Axis states should remain categorical where calibration is weak.

Example:

- LOW
- MEDIUM
- HIGH
- UNKNOWN

Do not convert UNKNOWN to LOW.

Do not create fake precision.

---

## 5.7 Hard Gates

Hard gates should represent real blockers.

Examples may include:

- strategy prohibition
- unacceptable rights/compliance risk
- impossible execution constraint
- unavailable required evidence for a high-risk opportunity
- explicit channel-policy exclusion

Hard gates should not be used as disguised aesthetic scoring.

---

## 5.8 WHY NOW

WHY NOW should be explicit.

Useful categories:

- EVERGREEN
- EMERGING
- ACCELERATING
- PEAKING
- DECLINING
- NEWS_SPIKE
- ARTIFICIAL_NOISE
- UNKNOWN

WHY NOW is evidence context, not a guarantee of performance.

---

## 5.9 Decision Policy

Primary states:

- MAKE
- PREPARE
- WATCH
- REJECT

A strong opportunity outside current strategy should not silently mutate strategy.

Preferred state:

WATCH
+
strategic_review_required

where appropriate.

REJECT is not deletion.

Rejected opportunities may receive:

- revisit_at
- expiry
- event-triggered reconsideration

---

## 5.10 Prediction / Decision Ledger

Opportunity decisions are append-only evidence events.

Relevant event types may include:

- DECISION
- OUTCOME
- REVISIT
- POLICY_CHANGE

The ledger should retain:

- candidate_ref
- evidence_refs
- decision
- reason codes
- known assumptions
- timestamp
- policy version
- revisit state
- later outcome where observable

Historical decisions must not be silently rewritten.

---

## 5.11 Outcome Attribution

Opportunity outcome analysis must not force one explanation.

Attribution domains may include:

- TOPIC
- PACKAGING
- HOOK
- SCRIPT
- PRODUCTION
- DISTRIBUTION
- EXTERNAL_CONTEXT
- CHANNEL_STATE
- MIXED
- UNCLEAR

This attribution model is shared conceptually with Content Learning.

Opportunity Intelligence must not assume a failed published video proves the topic itself was bad.

---

## 5.12 Cold-Start Evidence

Early evidence should remain honest.

Useful evidence maturity states:

- INSUFFICIENT
- DEVELOPING
- SUPPORTED
- CONFLICTING
- UNCLEAR

Do not invent arbitrary universal sample thresholds.

External priors may inform early policy.

They must be labelled as external/human priors rather than internal learned truth.

---

## 5.13 External Pattern Library

External observations may generate hypotheses.

Required conceptual flow:

external observation
-> candidate pattern
-> hypothesis
-> internal validation/trial
-> evidence
-> promote or reject

FlowMind learns mechanisms.

It does not copy competitors.

---

# 6. BLOCK 2 - EDITORIAL BRAIN

## 6.1 Purpose

The Editorial Brain owns:

- what the viewer is promised
- what the narrative must deliver
- what the script claims

Required conceptual flow:

OPPORTUNITY BRIEF
-> EDITORIAL DESIGN
-> PACKAGE CANDIDATES
-> PACKAGE SELECTION
-> NARRATIVE PLAN
-> OUTLINE
-> STRUCTURAL CHECK
-> SCRIPT GENERATION
-> DETERMINISTIC CHECKS
-> EDITORIAL GATE
-> FACTUAL GATE
-> TARGETED REVISION
-> EDITORIAL PACKAGE

Packaging precedes full script generation.

---

## 6.2 Viewer Promise

Viewer Promise is the central editorial contract.

Minimum logical fields should include:

- promise_id
- audience / viewer_intent ref
- core_payoff
- required_deliverables[]
- explicit_non_goals[]
- evidence_requirements[]
- prohibited_inflation[]

Do not create pseudo-precise numeric claim-strength scores without calibrated meaning.

Useful categorical claim alignment may include:

- ALIGNED
- INFLATED
- UNKNOWN

The Viewer Promise does not override factual evidence.

---

## 6.3 Packaging

Packaging is a pair:

TITLE
+
THUMBNAIL CONCEPT

They must be evaluated together.

Retain where practical:

- package candidates
- selected package
- selection rationale
- promise_ref
- audience context

The thumbnail at this stage is a concept.

Actual visual production belongs to Production Brain.

LLMs may generate or critique candidates.

They are not trusted CTR predictors.

---

## 6.4 Hook

Hook must align with:

- Viewer Promise
- selected package
- actual script

A matching promise_id alone does not prove semantic alignment.

Hook decisions should remain inspectable.

Do not hard-code universal hook durations.

---

## 6.5 Narrative Plan

V1 Narrative Plan should remain lightweight.

It may include:

- opening intent
- key narrative beats / questions
- information order
- payoff anchors
- optional open loops
- required transitions of meaning

Avoid:

- giant narrative graphs
- mandatory fixed re-hook cadence
- universal timing formulas

Production later converts narrative meaning into visual execution.

---

## 6.6 Outline

Outline occurs before full script generation.

It should verify:

- promise coverage
- structure
- required points
- payoff order
- evidence needs

before paying the cost of full-script generation and revision.

---

## 6.7 Script Contract

The script contract should include where applicable:

- promise_ref
- package_ref
- narrative_plan_ref
- audience
- format_id
- required_points[]
- prohibited_claims[]
- evidence_requirements[]
- target duration/range
- style_policy_ref

Word count is a proxy.

It is not timing truth.

---

## 6.8 Claim Provenance

Material factual claims require structured provenance where verification is required.

Useful fields:

- claim_id
- claim_text
- claim_type
- source_refs[]
- freshness
- evidence_state

Evidence state may include:

- SUPPORTED
- UNSUPPORTED
- CONFLICTING
- UNVERIFIED

Claims requiring elevated attention may include:

- numbers
- dates
- quotes
- pricing
- current product capabilities
- current events
- legal/policy claims
- health/safety claims
- financial claims

LLM memory is not a source.

---

## 6.9 Deterministic Editorial Checks

Cheap deterministic checks should run before expensive critique where useful.

Examples:

- required fields
- missing sections
- prohibited literal phrases where appropriate
- obvious unsupported placeholders
- duration proxy bounds where configured
- duplicate blocks
- invalid references

Deterministic checks should:

flag / block

not silently rewrite creative text.

---

## 6.10 Editorial Gate

Editorial Gate evaluates editorial quality.

Useful axes:

- PROMISE_FULFILLED
- PACKAGE_HOOK_ALIGNED
- SCRIPT_PROMISE_ALIGNED
- PAYOFFS_DELIVERED
- STRUCTURE_COHERENT
- REDUNDANCY_ACCEPTABLE
- STYLE_COMPLIANT
- DURATION_FIT

Axis states may include:

- PASS
- WARNING
- FAIL
- UNKNOWN

Overall outcome may include:

- PASS
- HUMAN_REVIEW
- HARD_FAIL

Do not create one aggregate Editorial Score.

---

## 6.11 Factual Gate

Factual Gate is separate from Editorial Gate.

Useful checks:

- RISKY_CLAIMS_SUPPORTED
- SOURCE_FRESHNESS_OK
- CONTRADICTIONS_RESOLVED
- UNSUPPORTED_MATERIAL_CLAIMS

Editorial quality must not compensate for unsupported material claims.

---

## 6.12 Revision Loop

Revision should be:

diagnose failed axis
-> targeted bounded revision
-> recheck affected/dependent gates
-> PASS / RETRY / HUMAN

Do not regenerate the entire script automatically for every local defect.

Retry limits are policy.

They are not universal architecture constants.

---

## 6.13 Provider Boundary

External capabilities may include:

- editorial_design
- script_generation
- editorial_critique
- factual_research
- factual_check

The same provider may implement multiple capabilities.

Provider identity must not become editorial business logic.

Provider-specific syntax such as proprietary SSML does not belong in Editorial Brain.

Editorial owns words and meaning.

Production owns delivery intent.

Adapters own provider-specific syntax.

---

## 6.14 Editorial Evidence

Log from Day One where practical:

- candidate packages
- selected package
- Viewer Promise
- Narrative Plan
- hook
- outline
- script
- material claim provenance
- gate results
- revision events
- provider/model versions
- policy versions
- cost
- latency
- human changes

Pattern-fatigue metadata may be logged now.

A sophisticated automatic fatigue detector is deferred until evidence justifies it.

---

# 7. BLOCK 3 - PRODUCTION BRAIN

## 7.1 Purpose

The Production Brain converts Editorial Package into executable audiovisual direction.

Logical responsibilities include:

- Director
- Visual Staging
- Visual Unit planning
- Audio Strategy
- Shot Planning
- Media Requirements
- Media Routing envelope
- Visual DNA
- overlay intent
- production priority
- fallback boundaries
- pre-render plan validation

These may be separate internal implementation functions.

There is one production-decision owner.

---

## 7.2 Production Hierarchy

V3.2 distinguishes:

Editorial Beat
-> Production Visual Unit
-> Shot

Editorial Beat expresses narrative meaning.

Production Visual Unit expresses visual coverage/execution intent.

Shot is the timed execution primitive after canonical audio exists.

A separate Scene runtime layer is not required unless implementation evidence shows material value.

---

## 7.3 Two-Pass Director

V3.2 keeps the Two-Pass Director with stricter boundaries.

### Pass 1 - Visual Staging

Pass 1 answers:

WHAT should be seen
+
WHY

Pass 1 does not own exact timing.

A minimal logical Director Intent may contain:

- director_intent_id
- script_ref
- visual_dna_ref
- visual_units[]

Each Visual Unit may contain:

- unit_id
- source_beat_refs[]
- purpose
- visual_intent
- representation_mode
- ordered capability preferences
- production priority
- must_show[]
- must_not_show[]
- overlay_intent

Pass 1 must not invent:

- frame timing
- shot timestamps
- false duration estimates
- final cut choreography

Avoid duplicating Editorial Brain concepts such as:

- emotional arc essays
- open-loop architecture
- narrative promise logic

Production consumes editorial meaning.

It does not recreate it.

---

## 7.4 Representation Mode

Useful representation modes:

- DIRECT_EVIDENCE
- ILLUSTRATIVE
- DECORATIVE

DIRECT_EVIDENCE requires stronger correspondence and verifiability.

Example:

a real product/UI claim

requires higher visual evidence discipline than:

a decorative conceptual background.

Representation mode informs:

- media requirement
- semantic validation
- QA risk

---

## 7.5 Production Priority

Visual Units may use categorical criticality such as:

- ESSENTIAL
- IMPORTANT
- OPTIONAL

This is not a quality score.

It helps answer:

what may be downgraded first without breaking the video?

---

## 7.6 Audio Strategy Boundary

Editorial owns narration words.

Production may own delivery intent such as:

- voice_profile_ref
- delivery_style
- pace_intent
- emphasis_refs[]
- pronunciation_requirements[]

Provider adapter owns provider-specific representation.

Examples:

- proprietary SSML
- provider-specific parameter names

If script words must change:

return to Editorial.

If delivery changes without changing meaning:

Production Audio Strategy may handle it.

---

## 7.7 Canonical Audio

Canonical Audio is the timing truth for downstream execution.

The actual audio artifact must exist before frame-accurate Pass 2 planning.

Logical metadata may include:

- audio_id
- audio_version
- audio_hash
- script_hash
- provider
- model/version
- voice_profile_ref
- generation_parameters_fingerprint
- duration
- timing_granularity
- timing_data[]
- created_at

Timing granularity may include:

- WORD
- SENTENCE
- SEGMENT
- DURATION_ONLY

Fine-grained provider timestamps are useful but not mandatory for the entire pipeline.

If only total duration is available:

- canonical audio may remain valid
- precision-dependent features degrade
- caption/sync capabilities may be limited

An invalid/unreadable canonical audio artifact is a failure.

New TTS generation creates a new immutable audio version.

It must not silently overwrite the identity of an existing canonical audio generation.

---

## 7.8 Pass 2 - Execution Plan

Pass 2 answers:

WHEN
+
EXACTLY HOW TO EXECUTE

Inputs:

- Director Intent
- Canonical Audio
- Visual DNA
- output/format context

Pass 2 creates timed shots.

Logical shot fields may include:

- shot_id
- visual_unit_ref
- start
- end
- visual_intent_ref
- media_requirement
- overlay instruction
- caption instruction
- deterministic motion instruction
- transition instruction
- priority

Shot timing must derive from actual canonical audio timing.

---

## 7.9 Media Requirement

A Media Requirement should be capability-oriented.

Useful fields:

- visual_intent_ref
- ordered_capability_preferences[]
- duration requirement
- aspect ratio
- representation_mode
- must_show[]
- must_not_show[]
- rights requirement
- priority
- fallback_policy

Capability examples:

- stock_video
- stock_image
- generated_video
- generated_image
- screen_visual
- diagram
- motion_text

Do not encode one favourite provider as the business requirement.

---

## 7.10 Media Router

Media Router chooses execution options inside an approved creative envelope.

Director determines:

- preferred capability
- acceptable alternatives
- degraded-but-allowed alternatives
- forbidden alternatives

Router may filter using:

- capability fit
- rights
- cost
- deadline
- availability
- provider health
- format constraints
- Visual DNA hard constraints

Router must not silently invent a new creative strategy.

Router is not a second Director.

---

## 7.11 Fallback Semantics

Fallback is requirement-specific.

Useful semantic states:

- PREFERRED
- ACCEPTABLE
- DEGRADED_BUT_ALLOWED
- NOT_ALLOWED

Do not assume globally that:

generated_video
-> stock_video

is equivalent.

If only an option outside the approved fallback envelope remains:

CREATIVE_DEGRADATION_REQUIRED

The system must:

- request targeted Production re-plan
- request Human Review where required
- or HALT

No silent creative degradation.

---

## 7.12 Visual DNA

Visual DNA is a production style contract.

V3.2 separates:

### HARD CONSTRAINTS

Examples:

- format-safe zones
- typography constraints
- prohibited visual styles/elements
- critical caption/readability rules

### SOFT PREFERENCES

Examples:

- motion character
- transition family
- visual density tendency
- realism/stylization preference
- caption behaviour
- media tendencies

### VIDEO-SPECIFIC OVERRIDES

An override must retain:

- reason
- scope
- policy/version context

Visual DNA must not become a God Config.

Do not place into Visual DNA:

- provider health
- retry rules
- rights policy
- budget authority
- operation state

---

## 7.13 Cost-Aware Production

Production receives a cost/budget envelope from runtime governance.

Production may prioritize expensive visual decisions using:

- ESSENTIAL
- IMPORTANT
- OPTIONAL

Where useful, Production may produce:

- preferred execution envelope
- approved fallback envelope

When the preferred plan exceeds the allowed budget:

1. try one approved lower-cost plan
2. use approved degraded fallback where permitted
3. HALT if acceptable output cannot be produced

Do not create endless downgrade loops.

Exact budget values are policy/configuration.

---

## 7.14 Asset Validation

Asset validation has at least two conceptual layers.

### Structural

Examples:

- exists
- readable
- duration
- dimensions
- codec/format
- hash

### Semantic Suitability

Does the asset satisfy its Media Requirement?

All assets should receive appropriate semantic sanity checking.

Stronger verification is justified for:

- DIRECT_EVIDENCE
- generated visuals
- real UI
- real products
- charts/data visuals
- real people/brands
- high factual-risk visuals

Final whole-video QA is not a substitute for per-asset suitability validation.

---

## 7.15 Pre-Render Plan Validator

Before expensive final render, validate deterministically where possible:

- dependency versions/hashes consistent
- canonical audio referenced correctly
- timeline coverage valid
- illegal gaps absent
- illegal overlaps absent
- asset refs resolved
- structural asset validation passed
- required semantic suitability state present
- requested operations supported by renderer
- format consistent
- Visual DNA hard constraints satisfied
- required overlays/captions have sources/instructions

Failure should result in:

- targeted plan correction
- or HALT

Renderer must not repair a failed creative plan.

---

## 7.16 Dependency and Invalidation Model

Critical production artifacts must identify parents.

Conceptual dependency chain:

SCRIPT
├── DIRECTOR INTENT
└── CANONICAL AUDIO

DIRECTOR INTENT + CANONICAL AUDIO
-> EXECUTION PLAN

EXECUTION PLAN
-> MEDIA REQUIREMENTS
-> RESOLVED MEDIA

EXECUTION PLAN + RESOLVED MEDIA
-> RENDER MANIFEST

Each artifact should retain where applicable:

- artifact_id
- schema_version
- artifact_hash
- parent_refs / parent_hashes
- producer
- created_at

If required parent identity no longer matches:

artifact state becomes STALE.

Do not guess compatibility.

---

## 7.17 Asset Reuse After Invalidation

Invalidating an Execution Plan does not automatically destroy expensive generated media.

An existing media artifact may remain a reusable candidate.

After replanning:

asset
-> revalidate against new requirement
-> reuse if still valid

This reduces unnecessary regeneration cost.

---

## 7.18 Production Artifact Set

V3.2 target logical production artifacts:

1. director_intent
2. canonical_audio + actual audio file
3. execution_plan
4. resolved_media
5. render_manifest

Media Requirements may live inside execution_plan.

Do not create a separate media_plan artifact unless runtime evidence shows a clear lifecycle need.

---

## 7.19 Production Evidence

Log where practical:

- script hash/version
- Director Intent
- Canonical Audio provenance
- Execution Plan
- Visual DNA version
- production policy version
- media requirements
- selected assets
- provider/model
- costs
- rights metadata refs
- fallbacks
- fallback reasons
- human corrections
- asset-use history
- channel_id
- format_id
- render dependency identity

Do not store hidden model chain-of-thought.

---

# 8. BLOCK 4 - RENDER, QUALITY & COMPLIANCE

## 8.1 Purpose

Rendering executes a validated plan.

Quality determines whether the final artifact is technically and semantically acceptable.

Compliance determines whether publication requirements are satisfied.

These are distinct responsibilities.

Creative repair decisions remain upstream.

---

## 8.2 Renderer

Renderer input may include:

- Render Manifest
- Canonical Audio
- resolved media
- timed shots
- overlays
- captions
- deterministic motion
- transitions
- output specification

Renderer responsibilities:

- place media
- deterministic trim/crop under authorized fit policy
- scale
- composite
- animate according to instruction
- place captions
- place overlays
- mix audio
- encode
- produce Render Report

Renderer must not:

- choose assets
- invent shots
- rewrite text
- invent fallback
- change media capability
- redesign pacing
- make creative replacement decisions

Same validated inputs/config should be reproducible as far as the render stack permits.

---

## 8.3 Output Specification

Quality requires an explicit expected output contract.

Useful fields:

- format_id
- aspect_ratio
- resolution
- frame_rate
- container
- codec requirements
- audio requirements
- caption requirement
- expected duration relationship
- applicable versioned technical thresholds

Renderer executes against this spec.

Hard QA checks final output against it.

---

## 8.4 Render Report

Renderer should emit deterministic evidence where available.

Useful fields:

- render_id
- output_hash
- actual_duration
- frame_count
- video_stream_summary
- audio_stream_summary
- render_manifest_ref/hash
- asset_refs_used
- encode/config fingerprint
- warnings[]
- errors[]
- created_at

Render Report is evidence.

It is not a QA PASS.

---

## 8.5 Preview

Preview is optional.

Use it only where expected re-render savings justify extra latency/cost.

Preview must record how it differs from final output.

Example difference dimensions:

- resolution
- codec
- assets
- effects
- render quality
- audio
- caption representation

Do not replace concrete differences with an uncalibrated generic fidelity score.

PREVIEW PASS
!=
FINAL PASS

Final Hard QA always applies to the actual final artifact.

---

## 8.6 Hard QA

Hard QA owns objective technical/artifact validation of the final artifact.

Hard blocking verdicts should rely on deterministic or strongly objective evidence.

V1 checks may include:

- final artifact identity
- file integrity
- video decode
- audio decode
- output-spec match
- duration consistency
- required streams present
- required audio present
- timeline/stream consistency
- required captions present where applicable
- required dependency evidence present

Additional checks may include:

- black/blank frames
- freeze frames
- loudness
- clipping
- A/V offset
- caption timing

only when they have:

- a defined measurement
- a versioned threshold
- an appropriate expected-intent exception
- regression evidence

Do not invent universal magic thresholds.

Hard QA does not own final rights/compliance verdicts.

---

## 8.7 Hard QA Threshold Sources

A technical threshold should have an explicit basis such as:

- recognized technical standard
- Output Specification
- format policy
- empirically calibrated FlowMind policy

Thresholds should be versioned.

Avoid hard-coded unexplained constants.

---

## 8.8 Soft QA

Soft QA is a narrow semantic / visible-defect review.

Useful V1 axes may include:

- VISUAL_INTENT_ALIGNMENT
- NARRATION_VISUAL_ALIGNMENT
- TEXT_READABILITY
- OBVIOUS_VISUAL_DEFECT
- UNEXPECTED_REPETITION
- SPECIFIC_VISUAL_DNA_CONFLICT

Experimental/review-only axes may include:

- PACING_RISK

Avoid generic pseudo-objective scores such as:

- cinematic score
- engagement score
- beauty score
- overall watchability score

Multimodal-provider judgment is evidence.

It is not system truth.

---

## 8.9 Defect Contract

QA identifies:

WHAT is wrong

not:

HOW to creatively fix it

A structured defect may contain:

- defect_id
- code
- category
- severity
- owner
- affected_scope
- artifact_ref
- evidence_refs[]
- recommended_action_type
- created_at

Useful categories:

- TECHNICAL
- SEMANTIC
- EDITORIAL
- RIGHTS
- POLICY
- DEPENDENCY

Visual/audio are usually scope dimensions rather than mandatory top-level categories.

UNKNOWN is a check state.

It is not a defect category.

Severity may include:

- BLOCKING
- REVIEW_REQUIRED
- NON_BLOCKING

---

## 8.10 Defect Ownership

Conceptual rule:

QA
-> detects defect

Control Plane
-> routes defect

Owning module
-> decides repair

Example action types:

- RENDER_AGAIN
- RE_RESOLVE
- DIRECTOR_REPLAN
- EDITORIAL_REVIEW
- COMPLIANCE_REVIEW
- HUMAN_REVIEW
- HALT

The action type is routing semantics.

It is not a creative instruction.

---

## 8.11 UNKNOWN Policy

UNKNOWN handling is risk-sensitive.

Examples:

critical technical UNKNOWN
-> retry evidence/check
-> REVIEW / HALT according to policy if unresolved

rights UNKNOWN
-> evidence retrieval
-> HUMAN REVIEW
-> never automatic PASS

platform-policy UNKNOWN
-> HUMAN REVIEW
-> never automatic PASS

soft semantic UNKNOWN
-> WARNING or REVIEW depending risk

UNKNOWN is not automatically FAIL.

Critical UNKNOWN is never automatically PASS.

---

## 8.12 Compliance

Compliance owns:

- Rights Evidence Evaluation
- platform-policy evaluation
- publication obligations

Compliance does not own:

- creative direction
- factual claim generation
- general legal opinion
- runtime orchestration

Compliance evaluates evidence against FlowMind-owned policy contracts.

---

## 8.13 Rights Evidence

A practical Rights Evidence record may include:

- asset_id
- asset_hash
- provider
- source_ref
- rights_state
- license_type if available
- attribution_requirement if available
- retrieved_at
- evidence_ref / evidence_hash

rights_state may include:

- ALLOWED
- PROHIBITED
- UNKNOWN
- CONFLICTING

If a provider does not expose a field:

store:

UNKNOWN

or:

NOT_PROVIDED

Do not invent metadata.

---

## 8.14 Pre-Use Rights Check

Before asset use / expensive acquisition:

check enough evidence to decide whether the asset/provider is eligible to enter production.

Possible considerations:

- commercial-use evidence
- editorial-only restriction
- known prohibited state
- attribution requirement
- required evidence availability

The pre-use check prevents obviously invalid assets entering production.

---

## 8.15 Final Rights / Compliance Check

Before publication, evaluate the assets actually used.

Verify where applicable:

- required Rights Evidence exists
- final Render Manifest references expected assets
- commercial-use policy requirements are satisfied
- attribution obligations are represented in the publication package
- known provider/platform restrictions are satisfied
- unresolved critical rights UNKNOWN does not silently pass

Pre-use and final checks serve different purposes.

They are not redundant.

---

## 8.16 Rights Evidence Snapshot

Where practical, retain evidence available at acquisition/generation time.

The system should know:

- what evidence was available
- when
- from where
- for which asset
- under which policy the decision was made

If terms/policy later change, use a versioned revalidation policy.

Do not assume FlowMind can make a universal legal conclusion about retroactive rights validity.

Persistent ambiguity requires Human Review.

---

## 8.17 Generated Media Evidence

For generated assets, retain where available/relevant:

- provider
- model/version
- generation timestamp
- terms evidence ref
- output hash
- prompt hash where useful for audit

Account/tier should be retained only when terms materially depend on it and the information is available.

---

## 8.18 Platform Policy

Platform policy must be based on versioned external evidence.

Useful states:

- KNOWN_RULE
- POLICY_UNKNOWN
- INTERPRETATION_REQUIRED

Retain where practical:

- platform_id
- policy_evidence_ref
- policy_evidence_hash
- retrieved_at
- internal_compliance_policy_version

Do not reduce platform policy to:

- keyword blacklist
- model memory
- folklore
- arbitrary "fair use seconds"

---

## 8.19 Channel-Level Repetitiveness Risk

Per-video compliance cannot detect every channel-level pattern.

V1 should primarily:

LOG NOW
ANALYZE SIMPLY
AUTOMATE LATER

Useful history may include:

- asset reuse
- script/opening patterns
- visual structure
- voice usage
- template/version
- media mix

Compliance may emit:

CHANNEL_RISK_SIGNAL_PRESENT

Compliance must not decide:

- new hook strategy
- new Visual DNA
- new Editorial policy

Those belong to Learning / Editorial / Production.

Sophisticated automatic mass-produced-content detection is deferred.

---

## 8.20 Bounded Rework

Rework must be policy-bounded.

Useful independent caps:

- same_defect_attempt_cap
- total_rework_cap
- expensive_media_replacement_cap
- multimodal_review_call_cap

Exact values are configuration/policy.

Quality does not orchestrate the loop.

Control Plane enforces it.

Exhausted bounded rework becomes:

- HUMAN_REVIEW
- or HALT

---

## 8.21 Final Artifact Identity

Quality decisions apply to an exact artifact.

Retain:

- final_artifact_id
- final_artifact_hash
- render_manifest_ref/hash
- render_report_ref/hash
- source dependency refs/hashes

Human approval binds to exact relevant artifact identity.

Changed final artifact:

approval -> STALE

---

## 8.22 Human Review vs Override

These are different concepts.

Policy classes may include:

- NON_OVERRIDEABLE
- OVERRIDEABLE_WITH_REASON
- REQUIRES_HUMAN_INTERPRETATION

Examples:

corrupt artifact
-> NON_OVERRIDEABLE

soft visual warning
-> OVERRIDEABLE_WITH_REASON

rights ambiguity
-> REQUIRES_HUMAN_INTERPRETATION

Human Review must not become a universal "publish anyway" button.

---

## 8.23 Publication Eligibility

Machine-readable publication state:

- ELIGIBLE
- ELIGIBLE_WITH_WARNINGS
- HUMAN_REVIEW_REQUIRED
- NOT_ELIGIBLE

Delivery consumes this state.

Delivery does not invent its own eligibility verdict.

Initial public upload still requires explicit human approval until separately authorized autonomy policy exists.

---

## 8.24 Quality / Compliance Artifact

V1 should prefer one persisted logical report:

quality_compliance_report

Possible sections:

- artifact_identity
- hard_qa
- soft_qa
- rights
- platform_compliance
- defects
- human_decisions
- publication_eligibility
- policy_versions

Do not create multiple physical artifacts without a lifecycle need.

---

## 8.25 Regression Fixtures

Hard QA should have minimal deterministic regression fixtures from Day One.

Examples:

- known-good output
- corrupt output
- missing audio
- wrong Output Specification
- dependency mismatch

Add new fixtures from real incidents.

Compliance may maintain a small curated fixture set such as:

- known eligible evidence
- known prohibited evidence
- rights unknown
- attribution required
- policy unknown

Do not build a giant legal benchmark system.

---

# 9. BLOCK 5 - DELIVERY & CONTENT LEARNING

## 9.1 Purpose

Delivery executes an authorized publication package.

Content Learning converts real outcomes into better future policy proposals.

Delivery and Learning share evidence.

They do not share authority.

---

## 9.2 Human / Auto Delivery

V1 public upload requires explicit human approval.

Move toward autonomous publication only after runtime evidence supports it.

Relevant evidence may include:

- stable successful runs
- reliable Hard QA
- no critical compliance failures
- predictable rendering
- predictable cost
- no silent errors
- stable approval binding
- acceptable automated/human QA disagreement

Do not hard-code universal exit counts.

Delivery owns execution.

It does not own:

- eligibility
- creative changes
- policy promotion

---

## 9.3 Content Learning Purpose

Content Learning asks:

WHAT decisions appear to produce better content/business outcomes for our audience?

It does not ask:

WHICH provider/model is technically best?

That belongs to Capability Evolution.

Content Learning is a conservative evidence and policy-proposal system.

It is not a black-box auto-optimizer.

---

## 9.4 Learning V1 Flow

Target flow:

PUBLISHED / TESTED VIDEO
-> DECISION CONTEXT
-> OUTCOME SNAPSHOTS
-> PUBLICATION INTERVENTIONS
-> HUMAN INTERVENTIONS
-> INCIDENTS
-> OBSERVATION
-> EVIDENCE ASSEMBLY
-> HYPOTHESIS
-> TRIAL / CANARY where possible
   OR OBSERVATIONAL VALIDATION
-> EVALUATION
-> PROMOTE / REJECT / CONTINUE_TEST / INCONCLUSIVE
-> POLICY PROPOSAL
-> HUMAN APPROVAL
-> CONTROL PLANE ACTIVATION
-> POST-PROMOTION MONITORING
-> ROLLBACK / HALT / CONTINUE

---

## 9.5 Decision Context

Performance without decision context is insufficient.

Decision Context should capture information that may be impossible to reconstruct later.

Useful fields/context may include:

- project/video id
- channel_id
- format_id
- audience/policy scope
- exploration flag
- Opportunity Candidate ref
- topic
- market angle
- viewer intent
- Viewer Promise
- package-at-publish
- hook/script metadata
- production raw/context data
- QA/compliance result
- cost
- active policy bundle refs/hashes
- provider/model versions
- publication timestamp
- channel-state snapshot where available

Decision Context should be immutable.

---

## 9.6 Outcome Snapshots

Analytics metrics evolve over time.

Do not overwrite old metric truth.

Metric snapshots are append-only.

A minimal Metric Snapshot may include:

- metric_snapshot_id
- metric_definition_version
- metric_name
- value
- state
- source
- scope
- window definition
- retrieved_at
- data_quality
- missing_reason

Possible states:

- AVAILABLE
- UNKNOWN
- NOT_AVAILABLE
- NOT_APPLICABLE
- DELAYED

Possible data_quality:

- COMPLETE
- PARTIAL
- DELAYED
- REVISED
- UNKNOWN

Missing data != zero.

Incomplete data != poor performance.

---

## 9.7 Outcome Maturity

V3.2 does not define universal:

- 2h
- 24h
- 7d
- 30d

as architectural truth.

Evaluation policies may define metric-specific maturity stages/windows.

A policy decision must retain the exact snapshot references used.

Later metric updates do not rewrite historical evaluation decisions.

---

## 9.8 Publication Intervention Ledger

Any material post-publication change should be logged.

Examples:

- title change
- thumbnail change
- description change
- metadata change
- captions change
- visibility change
- promotion/distribution change

Useful fields:

- intervention_id
- video_ref
- intervention_type
- before_ref/value
- after_ref/value
- actor
- changed_at
- reason
- affected_learning_scope

Learning attribution must account for intervention windows.

A package change contaminates package attribution.

It does not automatically invalidate every other learning dimension.

---

## 9.9 Human Intervention Ledger

Human corrections inside FlowMind must be logged.

Examples:

- title edit
- thumbnail edit
- hook edit
- script rewrite
- asset replacement
- QA override
- publication delay
- strategy change

Useful fields:

- intervention_id
- video_ref / decision_ref
- correction_type
- owner / actor
- before_ref
- after_ref
- reason
- accepted/rejected where relevant
- occurred_at
- affected_scope

Learning should not attribute a human-created result to autonomous system policy.

Intervention contamination should be scope-specific.

Do not use one global HUMAN_TAINTED flag as the only model.

---

## 9.10 Incident Records

High-severity incidents require a separate evidence path.

Examples:

- copyright claim
- platform warning
- serious factual correction
- broken final render found after upload
- critical rights failure

Good performance metrics must not compensate for a protected-domain incident.

Incident evidence may generate:

- investigation
- policy proposal
- rollback
- HALT
- regression fixture

---

## 9.11 Raw vs Derived

Raw observations are durable evidence.

Examples:

- actual duration
- word count
- actual shot durations
- shot count
- media types
- actual cost
- provider/model ids
- publication timestamp

Derived features are rebuildable versioned views.

Examples:

- pacing category
- density category
- hook type
- media-mix category

Do not build a separate Feature Store in V1.

Do not destroy raw information through premature bucketing.

A derived feature result should retain:

feature_definition_version

Old observations must not be silently reinterpreted under a new feature definition.

---

## 9.12 Evidence Assembly

V1 may physically combine pattern detection and hypothesis preparation into one lightweight Evidence Assembly stage.

However:

evidence
!=
hypothesis

Evidence describes what was observed.

Hypothesis proposes what might explain it.

Do not let an LLM silently transform observation into causal truth.

---

## 9.13 Evidence State

Useful states:

- INSUFFICIENT
- DEVELOPING
- SUPPORTED
- CONFLICTING
- UNCLEAR

Evidence state should consider:

- comparable context
- amount of evidence
- direction consistency
- effect magnitude
- freshness
- data quality
- known confounders
- risk of proposed change

Do not use universal rules such as:

3 videos = pattern

Do not create fake probability confidence.

---

## 9.14 Attribution

Contribution domains may include:

- TOPIC
- PACKAGING
- HOOK
- SCRIPT
- PRODUCTION
- DISTRIBUTION
- EXTERNAL_CONTEXT
- CHANNEL_STATE
- MIXED
- UNCLEAR

The system is not required to choose one cause.

Separately record the strength/type of attribution evidence.

Useful evidence-type labels:

- CONTROLLED_TRIAL_EVIDENCE
- QUASI_EXPERIMENTAL_EVIDENCE
- OBSERVATIONAL_ASSOCIATION
- CONFOUNDED
- UNCLEAR

WHAT may have contributed
!=
HOW strong the attribution basis is

---

## 9.15 Survivorship and Selection Bias

Published videos are a selected dataset.

MAKE outcomes exist.

WATCH / PREPARE / REJECT often have no publication outcome.

Do not infer:

MAKE was better

merely because rejected opportunities lack outcome metrics.

Opportunity Decision Ledger and revisit events should preserve missed/opposed choices for future analysis.

V1 should acknowledge this limitation rather than pretending to solve the counterfactual.

---

## 9.16 Hypothesis Contract

A hypothesis must be testable.

Useful fields:

- hypothesis_id
- claim
- scope
- eligible_context
- target_metric
- guardrail_metrics[]
- expected_direction
- candidate_policy_change_ref
- change_risk
- evidence_refs[]
- falsification_condition
- status

Avoid unnecessary:

- Bayesian priors
- fake confidence intervals
- giant multi-metric scores

Scope should be no narrower than necessary for the hypothesis.

If the cohort becomes insufficient:

evidence remains INSUFFICIENT.

Do not silently broaden scope to manufacture sample size.

---

## 9.17 Validation / Experiment Types

V1 should distinguish:

- CONTROLLED
- CANARY / POLICY TRIAL
- QUASI_EXPERIMENT
- OBSERVATIONAL_VALIDATION
- MANUAL_TEST

Do not call an observational comparison a controlled A/B experiment.

Available experiment mechanics depend on the platform capabilities available at the time.

Do not hard-code current platform limitations as permanent architecture truth.

---

## 9.18 Experiment Registry

The Experiment / Trial Registry should be thin and auditable.

Useful fields:

- experiment_id
- type
- hypothesis_ref
- control_policy_version
- candidate_policy_version
- scope
- eligible cohort definition
- unit
- membership rules
- concurrency scope
- start time
- planned evaluation/maturity policy
- change risk
- status

Control/candidate policy versions are frozen for the registered trial.

If material execution context changes:

the experiment may become CONTAMINATED.

---

## 9.19 Concurrency / Contamination

V1 default:

No overlapping material experiments on the same attribution scope unless explicitly registered as a joint experiment.

Do not casually change:

- packaging policy
- hook policy
- production pacing policy

inside the same attribution scope and then claim one variable caused the result.

Factorial experimentation is deferred.

---

## 9.20 Canary Semantics

Content canary is not automatically traffic percentage.

It may be:

- limited future eligible videos
- one format scope
- one topic scope
- one channel scope
- manually approved set

Canary allocation is policy.

It is not a universal architecture constant.

---

## 9.21 Metric Taxonomy

Useful roles:

- PRIMARY
- GUARDRAIL
- DIAGNOSTIC
- BUSINESS
- OPERATIONAL

Any metric may be primary when the hypothesis is genuinely about that metric.

No metric should be optimized without appropriate guardrails.

Do not create one aggregate:

Content Performance Score

---

## 9.22 Goodhart Protection

Optimization must assume metrics can be gamed.

Examples:

CTR
-> misleading clickbait

Retention
-> overstimulation / padding / withholding

Revenue
-> short-term monetization damage

Cost
-> unacceptable quality degradation

Guardrails prevent one metric from becoming the only objective.

Protected-domain breaches override business success.

---

## 9.23 Evaluation

Evaluation is categorical.

Allowed results:

- PROMOTE
- REJECT
- CONTINUE_TEST
- INCONCLUSIVE

A promotion proposal requires:

- target result in expected direction
- evidence sufficient for the applicable risk
- guardrails acceptable
- data quality sufficient
- major confounders considered
- attribution evidence represented honestly

Do not use weighted-sum scoring unless future calibration justifies it.

INCONCLUSIVE is a valid result.

---

## 9.24 Rollback

ROLLBACK is a lifecycle action.

It is not an experiment verdict.

Post-promotion monitoring may trigger rollback.

Automatic rollback may be allowed for:

- predefined critical protected-domain guardrail breach
- deterministic safety/compliance condition

only when:

- rollback is authorized
- rollback target is known
- rollback target remains valid

If rollback target is stale or unsafe:

HALT
+
HUMAN REVIEW

Ambiguous business-performance drift should normally go to Human Review.

---

## 9.25 Policy Proposal

Learning proposes policy changes.

It does not directly activate them.

A Policy Proposal may include:

- proposal_id
- source_hypothesis_ref
- source_evaluation_ref
- current_version
- candidate_version
- scope
- changed_fields[]
- evidence_refs[]
- expected_effect
- guardrails_checked[]
- change_risk
- rollback_target

changed_fields must be an explicit schema-bounded diff.

Do not replace a giant policy blob invisibly.

---

## 9.26 Policy Store

Policy objects must be:

- versioned
- immutable after creation
- schema-bounded
- typed
- scoped
- traceable
- reversible

Policy Store may retain:

- policy_id
- domain
- version
- schema_ref
- values
- supersedes_version
- created_at
- created_by

Policy object should not independently own authoritative:

active = true

The Control Plane owns active-policy binding.

---

## 9.27 Policy Risk and Domain Classification

Change risk:

- LOW
- MEDIUM
- HIGH

Separately, policy domain classification may include:

- OPTIMIZABLE
- HUMAN_ONLY
- PROTECTED

Do not overload one enum with both concepts.

---

## 9.28 Protected Policy Domains

Protected domains include:

- RIGHTS
- SAFETY
- HARD COMPLIANCE
- FACTUAL CORE
- HARD TECHNICAL QA

Content-performance metrics must not automatically weaken these domains.

Learning may generate calibration proposals.

Activation remains human-owned and evidence-bound.

A high-performing violating video is not evidence to weaken protection.

---

## 9.29 Prompt Policy Boundary

Learning may propose changes only to predefined schema-controlled prompt parameters.

Examples:

- enum preference
- bounded parameter
- predefined style option

Learning may not:

- rewrite arbitrary system prompts
- generate free-form instruction blobs for direct activation
- modify application source code

Structural prompt changes are a Human-owned change process.

---

## 9.30 V1 Promotion Policy

All Content Learning policy promotions in V1 require Human Approval.

This applies even to LOW-risk changes.

Reason:

early experimentation volume is low

while:

wrong attribution / Goodhart cost is high.

Future bounded low-risk auto-promotion may be introduced only after runtime evidence justifies it.

Do not define an arbitrary video-count threshold now.

---

## 9.31 Cold Start

Cold-start state should be honest.

When evidence is weak:

- use human policy
- use explicit external priors
- use exploration where appropriate
- retain INSUFFICIENT / DEVELOPING state

Do not pretend FlowMind has learned from insufficient data.

---

## 9.32 Exploration

Opportunity may label work as:

exploration = true

The tag should propagate into:

- Decision Context
- Observation
- Hypothesis
- Evaluation

Learning V1 does not automatically manage exploration allocation.

Exploration hypotheses may use a separate versioned Evaluation Policy.

Do not kill novelty immediately against a mature exploit baseline.

Exact exploration windows and thresholds are policy.

---

## 9.33 Cross-Format and Cross-Channel Scope

Day One fields should include where relevant:

- format_id
- channel_id
- audience_scope
- policy_scope

Default:

do not transfer learned policy across formats/channels silently.

Cross-channel transfer requires explicit evidence and Human decision.

No transfer-learning engine in V1.

---

## 9.34 Reproducible Evaluation

A promotion decision should be reproducible enough to answer later:

why was Policy X promoted?

Retain:

- exact cohort definition
- included observations
- excluded observations + reason
- exact Metric Snapshot refs
- control/candidate policy versions
- relevant feature-definition versions
- evaluation_policy_version
- data-quality filters
- evidence refs
- human decision
- reason codes

Do not rely on live analytics re-queries to reconstruct past decisions.

---

## 9.35 Learning Ledger

Useful immutable events include:

- decision_context_created
- outcome_snapshot_recorded
- publication_intervention
- human_intervention
- incident
- observation_created
- evidence_state_changed
- hypothesis_registered
- experiment_registered
- experiment_membership
- evaluation_snapshot
- policy_proposal
- promotion_decision
- policy_activation
- rollback_decision

Do not store hidden LLM chain-of-thought.

Store:

- reason codes
- evidence refs
- versions
- human actor
- timestamps

---

## 9.36 Learning Versioning

Minimal relevant version dimensions may include:

- policy_version
- feature_definition_version
- metric_definition_version
- evaluation_policy_version
- schema_version

Provider/model versions are execution context/confounder metadata.

Avoid version spaghetti.

Use only versions that materially affect interpretation or reproducibility.

---

## 9.37 LLM Role in Content Learning

LLMs may assist with:

- qualitative synthesis
- pattern explanation
- hypothesis drafting
- experiment proposal drafting
- comment summarization with caveats

LLMs do not independently decide:

- causal truth
- evidence sufficiency
- statistical significance
- policy promotion
- safety weakening
- protected-policy changes

LLM output is a proposal/evidence aid.

It is not authority.

---

# 10. BLOCK 6 - CAPABILITY EVOLUTION

## 10.1 Purpose

Content Learning asks:

"What decisions produce better content/business outcomes for our audience?"

Capability Evolution asks:

"What tools/providers/models perform FlowMind capabilities best?"

These are separate loops.

Content Learning must not silently become provider benchmarking.

Capability Evolution must not silently become content strategy.

---

## 10.2 Capability Evolution Flow

WATCH
-> DISCOVER
-> REGISTER CANDIDATE
-> CONTRACT FIT
-> SECURITY / RIGHTS / COST CHECK
-> BENCHMARK
-> COMPARE
-> CANARY
-> ADOPT / REJECT
-> CONTROLLED ACTIVATION
-> MONITOR
-> ROLLBACK / REPLACE

Discovery may include:

- provider APIs
- hosted services
- open-source packages
- reusable command-line tools
- MCP-style capability servers
- agent-skill ecosystems
- local tools
- reusable automation workflows

Discovery does not grant runtime or decision authority.

---

## 10.3 Provider Watcher

Monitor approved provider sources for:

- new models
- new versions
- capability changes
- deprecations
- pricing changes
- material terms changes
- availability changes

Prefer trusted sources such as:

- official model catalog
- official API documentation
- official release notes
- official pricing
- official lifecycle/status notices

Do not blindly ingest the whole Internet into provider decisions.

---

## 10.4 Candidate Registry

Capability implementations may have states such as:

- ACTIVE
- CANDIDATE
- FALLBACK
- REJECTED
- DEPRECATED
- DISABLED

Discovery does not imply production activation.

---

## 10.5 Capability-Based Contracts

Business logic requests capabilities.

Examples:

- script_generation
- editorial_critique
- factual_research
- image_generation
- video_generation
- text_to_speech
- multimodal_quality_review
- stock_search

Provider-specific adapters implement the contract.

Provider identity should not unnecessarily leak into domain logic.

---

## 10.6 Standard Provider Result

Where applicable, provider results should expose structured metadata such as:

- provider
- model/version
- capability
- status
- estimated_cost
- actual_cost
- latency
- error_class
- quality metadata
- rights/commercial-use metadata

Media results may additionally expose:

- hash
- dimensions
- duration
- source
- attribution
- license/commercial-use evidence refs

Do not invent unavailable provider metadata.

---

## 10.7 Benchmark Harness

Each capability requires an appropriate benchmark.

Do not use one generic benchmark for all AI systems.

Script benchmark considerations may include:

- instruction compliance
- promise alignment
- structure
- factual reliability
- cost
- latency
- failure rate

Image/video benchmark considerations may include:

- requirement adherence
- temporal/visual quality
- consistency
- artifact rate
- cost
- latency

TTS benchmark considerations may include:

- naturalness
- pronunciation
- pacing
- stability
- cost
- latency

Research benchmark considerations may include:

- factual accuracy
- source quality
- citation quality
- completeness
- latency
- cost

---

## 10.8 Historical Benchmark Set

Benchmarks should use a controlled set of:

- real historical FlowMind tasks
- successful cases
- difficult cases
- known failure cases

Candidate and active versions should receive comparable inputs where possible.

---

## 10.9 Canary Before Promotion

Offline benchmark success does not prove production performance.

Where appropriate:

candidate
-> limited production canary
-> downstream evidence
-> promotion decision

Allocation is policy.

It is not an architectural constant.

---

## 10.10 Capability Promotion

Capability promotion may update:

- primary provider/model
- fallback provider/model
- candidate state

Previous stable capability should normally remain available during controlled migration where practical.

Promotion authority must remain explicit.

Capability Evolution must not mutate active content policy.

---

## 10.11 Capability Rollback

Rollback may be triggered by:

- quality degradation
- cost degradation
- latency degradation
- elevated error rate
- provider outage
- terms/rights issue
- unexpected production behaviour

Provider/model changes must be logged because they may become confounders for Content Learning.

---

## 10.12 Capability Evolution Triggers

Primary trigger classes:

1. DISCOVERY
2. DEGRADATION
3. ECONOMIC / OPERATIONAL CHANGE

Examples:

- new model
- model retirement
- material price change
- provider quality regression
- latency degradation
- terms change
- provider instability

---

## 10.13 External Capability / OSS Donor Adoption

FlowMind may reuse an external capability without adopting the external system as an authority.

Possible donor forms include:

- provider API
- hosted service
- open-source library/package
- command-line tool
- MCP-style capability server
- agent skill
- reusable workflow
- local executable/tool

A donor may contribute one narrow capability or several capabilities.

FlowMind should prefer the smallest useful adoption surface.

Do not import an entire external framework merely because one capability is valuable.

Required conceptual adoption path:

DISCOVER
-> REGISTER CANDIDATE
-> CONTRACT FIT
-> SECURITY / RIGHTS / COST CHECK
-> BENCHMARK
-> CANARY
-> ADOPT / REJECT
-> MONITOR
-> ROLLBACK / REPLACE

### Contract Fit

Before adoption, verify that the donor can fit a stable FlowMind capability contract.

Contract fit should consider where applicable:

- required inputs
- required outputs
- error/failure semantics
- side-effect semantics
- idempotency or reconciliation needs
- artifact/evidence identity
- provider/model/tool provenance
- cost and latency reporting
- rights/commercial-use evidence
- observability
- version pinning
- rollback/replacement feasibility

If contract fit requires FlowMind to surrender canonical control or hide critical state:

REJECT

or:

WRAP / ADAPT

until the authority boundary is restored.

### Security / Rights / Cost Check

Before production adoption, evaluate where applicable:

- license and commercial-use compatibility
- dependency and supply-chain risk
- secret/credential exposure
- network/data exposure
- filesystem/process permissions
- external code-execution behaviour
- provider terms
- data retention/privacy behaviour
- operational cost
- maintenance burden
- abandonment/deprecation risk

UNKNOWN material risk must not silently become acceptable.

### Authority Boundary

External capability never automatically receives authority over:

- canonical project state
- project phase
- operation state
- active-policy binding
- budget authority
- QA verdict
- rights/compliance verdict
- publication eligibility
- human approval
- Content Learning promotion
- architecture authority

External capability output is:

EVIDENCE
+
CANDIDATE RESULT
+
PROPOSAL

as appropriate.

It is not FlowMind truth merely because the external tool labels it:

- score
- recommendation
- PASS
- viral
- safe
- compliant
- high confidence
- ready

External heuristic scores must not become FlowMind gates without:

- semantic mapping
- benchmark evidence
- calibration where applicable
- explicit FlowMind-owned policy

### Integration Boundary

Preferred integration:

FlowMind capability contract
-> adapter / wrapper
-> external donor
-> normalized result
-> FlowMind validation / policy

The adapter may use:

- API call
- library invocation
- subprocess
- MCP-style call
- agent-skill invocation
- local tool execution

Provider/tool-specific syntax should remain inside the adapter where practical.

External tools must not directly mutate canonical project state unless the canonical Control Plane explicitly authorizes a bounded state operation.

### Partial Adoption

FlowMind may adopt only the useful capability slice.

Examples:

- outlier / viral-evidence extraction
- packaging critique
- hook/script critique
- retention interpretation
- Shorts extraction
- research
- media generation
- multimodal review

A donor's internal orchestration, scoring model, prompts, storage, scheduler or publishing logic may be rejected even when one capability is adopted.

### Provenance

For an adopted donor, retain where practical:

- donor/source identity
- capability
- version / release / commit identity
- adapter version
- license/terms evidence
- security review state
- benchmark result
- canary result
- cost/latency evidence
- known limitations
- rollback/replacement target

### Replacement Principle

External capabilities are replaceable execution tools.

FlowMind-owned decision contracts, state, evidence and policy must survive replacement of the donor.

A donor outage, deprecation or quality regression must not force architectural redesign unless the underlying capability contract itself was wrong.

---

# 11. HUMAN DECISION GATEWAY

## 11.1 Purpose

Human control must exist without becoming constant manual work.

Human attention should focus on:

- high-risk decisions
- ambiguous rights/policy states
- early autonomy calibration
- architecture changes
- protected-policy changes
- structural prompt changes
- major strategy changes
- publication where current policy requires it

---

## 11.2 Human Decision Semantics

A Human Decision record should communicate:

- WHAT changed
- WHY
- EVIDENCE
- EXPECTED BENEFIT
- COST
- RISK
- affected scope
- target artifact/policy identity

Possible decisions:

- APPROVE
- REJECT
- DEFER

A Human decision must be logged.

---

## 11.3 V1 Human-Gated Areas

V1 explicitly retains Human Approval for:

- public upload
- Content Learning policy promotion
- architecture promotion
- protected-policy changes
- major prompt structure changes
- major strategy changes
- ambiguous rights/compliance cases as defined by policy

Other runtime operations may be automatic when policy safely authorizes them.

---

# 12. PERSISTENT STATE AND EVIDENCE MEMORY

## 12.1 Principle

FlowMind knowledge must not live only inside:

- an LLM chat
- provider account
- process memory
- temporary local files

System knowledge belongs to FlowMind.

---

## 12.2 Structured Persistent Store

May contain:

- canonical project state
- operation state
- provider-health state
- approval state
- policy bindings
- policy versions
- opportunity decisions
- Prediction / Decision Ledger
- Decision Context
- Outcome Snapshots
- Publication Interventions
- Human Interventions
- incidents
- evidence states
- hypotheses
- experiment/trial registry
- evaluation snapshots
- costs
- Rights Evidence
- capability registry
- benchmark results
- Learning Ledger
- human decisions

V1 does not require a dedicated Feature Store.

Derived features may be rebuilt from durable raw/context evidence.

---

## 12.3 Object Storage

May contain:

- audio
- video
- images
- previews
- final renders
- provider outputs
- large evidence snapshots
- archived raw responses where retention is useful
- rights/policy document snapshots

Large artifact retention should remain cost-aware.

---

## 12.4 Git

Contains:

- application source code
- schemas
- contracts
- migrations
- stable configuration definitions
- authority documents
- deterministic fixtures where appropriate

Git must not contain secrets.

---

# 13. CLOUD-FIRST RUNTIME

Target FlowMind is cloud-first.

Always-on execution authority should not require the user's personal computer to remain powered on.

Conceptual model:

Cloud Core
-> Control Plane
-> Persistent State
-> Scheduler
-> Lightweight jobs
-> External providers

Optional workers may include:

- local GPU worker
- cloud GPU worker
- render worker

Loss of an optional worker must not destroy:

- canonical state
- operation identity
- decision history
- policy state
- evidence memory

Cloud migration still follows ROI and runtime evidence.

Do not build infrastructure before demonstrated need.

---

# 14. COST AND LATENCY GOVERNANCE

Cost is a first-class runtime constraint.

Track where possible:

- estimated provider-call cost
- reserved cost
- actual provider-call cost
- per-stage cost
- per-video cost
- period cost
- rework cost
- human-review cost where measurable

Paid operations should use reservation semantics where useful.

Latency is also a resource.

Track:

- provider response time
- queue delay
- stage duration
- end-to-end duration

A cheaper provider is not automatically better if it destroys quality or throughput.

A faster provider is not automatically better if cost, rights or quality becomes unacceptable.

Budget authority belongs to runtime governance.

QA does not independently recalculate budget policy.

---

# 15. PROVIDER HEALTH AND FALLBACK

Provider abstraction includes operational health.

Relevant mechanisms may include:

- provider-health state
- retry policy
- backoff
- circuit breaker
- fallback chain
- temporary disable
- recovery probe

Provider-health state is not project state.

Fallback must remain policy-controlled.

Do not silently switch providers where:

- rights differ
- cost materially differs
- output characteristics differ
- quality requirements differ
- Director-approved creative envelope would be violated

Media creative fallback belongs to Production constraints.

Operational provider fallback belongs to capability/runtime policy.

These must not be conflated.

---

# 16. ARTIFACT IDENTITY AND DEPENDENCY TRACKING

Critical artifacts should retain identity sufficient for audit and invalidation.

Where applicable:

- artifact_id
- schema_version
- artifact_hash
- parent_refs
- parent_hashes
- producer
- producer version
- policy refs
- created_at

A downstream artifact built against stale parent identity must not silently remain valid.

Conceptual state:

VALID
STALE
INVALID
UNKNOWN

Exact state names may be implementation policy.

The architectural requirement is:

dependency mismatch must be detectable.

Human approval also binds to relevant artifact identity.

---

# 17. OBSERVABILITY AND AUDITABILITY

Every critical decision should be explainable after the fact.

Logs/evidence should enable answers to:

- what happened
- when
- why
- which operation
- which attempt
- which provider/model
- which policy version
- which artifact
- which parent hashes
- how much it cost
- how long it took
- why retry happened
- why HALT happened
- why a defect was raised
- why publication was blocked
- why a policy proposal was made
- why policy was promoted
- why rollback happened
- why provider/model changed
- which Human approved or overrode
- which exact output was approved

No silent failure.

No empty exception handling.

Do not store hidden LLM chain-of-thought.

Store structured evidence and reason codes.

---

# 18. SECURITY

Secrets must:

- never be hard-coded
- never be committed
- never be logged
- come from environment or approved secret storage

The architecture should allow future secret-store migration without rewriting domain business logic.

Provider credentials should be isolated from domain decision logic.

Authorization-sensitive external actions should be traceable.

Publication credentials must not become accessible to unrelated creative components.

---

# 19. CROSS-MODULE OWNERSHIP INVARIANTS

## Control Plane

Owns:

- orchestration
- canonical state
- transition enforcement
- runtime operations
- retry/reconciliation
- active policy binding
- HALT
- approval enforcement

Does not own:

- creative decisions
- QA verdict creation
- learning hypotheses
- provider capability evaluation

---

## Opportunity Intelligence

Owns:

WHAT opportunity should be considered and WHY NOW.

Does not own:

- final package
- hook
- script
- visual execution

---

## Editorial Brain

Owns:

WHAT the audience is promised and WHAT the narrative says.

Does not own:

- provider execution
- frame timing
- asset selection
- runtime orchestration

---

## Production Brain

Owns:

HOW editorial intent becomes audiovisual execution.

Does not own:

- editorial factual truth
- runtime state
- publication eligibility
- learning promotion

---

## Quality + Compliance

Owns:

WHAT is technically wrong, semantically suspicious or unsafe to publish.

Does not own:

- creative repair strategy
- runtime orchestration
- active policy binding

---

## Delivery

Owns:

execution of an already authorized publication package.

Does not invent publication eligibility.

Does not redesign content.

---

## Content Learning

Owns:

- evidence assembly
- hypotheses
- evaluations
- policy proposals

Does not:

- activate active policy directly
- modify source code
- select providers as a capability benchmark
- weaken protected domains because metrics improved

---

## Capability Evolution

Owns:

provider/model/tool evolution.

Does not silently modify content strategy.

---

# 20. LOGICAL ARTIFACT MODEL

V3.2 remains inspectable.

Critical decisions and handoffs should produce machine-readable evidence.

Logical artifacts may include:

Opportunity:

- opportunity_candidate
- opportunity_decision
- prediction_ledger_event

Editorial:

- viewer_promise
- package_candidates
- selected_package
- narrative_plan
- outline
- script
- claim_provenance
- editorial_gate_result
- factual_gate_result
- editorial_package

Production:

- director_intent
- canonical_audio
- execution_plan
- resolved_media
- render_manifest

Render / QA / Compliance:

- render_report
- final_artifact
- quality_compliance_report

Delivery:

- publication_package
- approval_record
- publication_record

Learning:

- decision_context
- metric_snapshot
- publication_intervention
- human_intervention
- incident_record
- hypothesis
- experiment_record
- evaluation_snapshot
- policy_proposal
- policy_version
- learning_ledger_event

Capability Evolution:

- capability_candidate
- benchmark_result
- capability_decision

These names describe logical contracts.

They do not require one physical JSON file per logical concept.

Avoid artifact sprawl.

Combine records where:

- ownership stays clear
- lifecycle stays clear
- invalidation stays clear
- evidence remains auditable

---

# 21. POLICY ARCHITECTURE

Policy must not become hidden application code.

Policy objects should be:

- schema-controlled
- typed
- bounded where applicable
- versioned
- immutable after creation
- scoped
- auditable

Examples of policy-controlled behaviour may include:

- Opportunity decision rules
- strategic priorities
- Editorial style preferences
- package preferences
- allowed prompt parameters
- Production Visual DNA
- capability preferences
- fallback envelopes
- cost limits
- QA thresholds
- compliance interpretation rules
- experiment definitions
- evaluation rules
- exploration policy

Policy must not contain arbitrary executable code.

Learning may propose changes only to allowed policy fields.

Structural changes require Human-owned code/schema change.

Control Plane owns active-policy binding.

Policy Store owns immutable policy versions.

---

# 22. AUTONOMY POLICY

FlowMind should become highly autonomous but bounded.

V1 explicitly does NOT allow autonomous:

- public upload
- Content Learning policy promotion
- architecture changes
- protected-policy weakening
- arbitrary structural prompt rewriting
- source-code modification

Automatic runtime behaviour may be allowed where policy authorizes:

- deterministic state transitions
- safe retry
- provider fallback within allowed envelope
- bounded rework
- approved media fallback
- routine low-risk execution
- evidence collection
- analytics ingestion
- regression checks

Automatic rollback may be authorized for predefined deterministic critical conditions.

Autonomy must be:

- reversible
- auditable
- policy-bounded
- artifact-bound where applicable

Autonomy must never imply self-modifying application code.

---

# 23. PROTECTED DOMAINS

The following are protected from business-metric optimization:

- RIGHTS
- SAFETY
- HARD COMPLIANCE
- FACTUAL CORE
- HARD TECHNICAL QA

A policy may not be weakened merely because violating content achieved:

- higher CTR
- higher retention
- higher watch time
- higher revenue

Protected-domain incidents are evaluated independently from performance success.

Learning may propose calibration of detection behaviour.

Protected-domain policy activation remains Human-controlled.

---

# 24. ARCHITECTURE VS RUNTIME TRUTH

Architecture describes target intent.

Runtime truth comes only from verified repository/runtime evidence.

A capability is not operational merely because:

- this document describes it
- a file exists
- a class exists
- a function exists
- an artifact name exists
- a test fixture exists
- a historical document says it worked
- a provider adapter exists

Operational capability requires relevant runtime proof.

Architecture publication does not create implementation truth.

---

# 25. MIGRATION PRINCIPLE

Do not rewrite the entire current system merely to match V3.2 terminology.

For every existing component classify:

- KEEP
- MODIFY
- REPLACE
- REMOVE
- MISSING

Prefer:

KEEP

when current implementation already satisfies the V3.2 contract.

Prefer:

MODIFY

when controlled adaptation closes the gap.

Use:

REPLACE

only when current implementation is structurally incompatible.

Use:

REMOVE

when a component is:

- redundant
- dangerous
- legacy
- a second authority
- permanently incompatible with the canonical contour

Use:

MISSING

when V3.2 requires a capability with no verified implementation.

Implementation sequence remains evidence-driven.

---

# 26. IMPLEMENTATION PRINCIPLE

V3.2 is a destination.

It does not define implementation order.

Required implementation sequence:

CURRENT REPO / RUNTIME EVIDENCE
-> COMPARE WITH TRUSTED TARGET
-> IDENTIFY ONE REAL GAP
-> VERIFY ROI / IMPACT
-> AUTHORIZE ONE TARGET
-> IMPLEMENT
-> VALIDATE
-> COMMIT
-> OBSERVE

Do not select work only because:

- the architecture section looks important
- a module is intellectually interesting
- historical notes say it was next
- a provider feature exists

Evidence and ROI determine implementation order.

Default working mode remains:

ONE STEP
-> VALIDATE
-> NEXT STEP

---

# 27. DEFERRED / CONTROLLED SCOPE

Do not build without evidence:

- custom foundation LLM
- custom TTS foundation model
- custom image foundation model
- custom video foundation model
- custom search engine
- giant social-listening stack
- second production contour
- second dispatcher
- second policy activation authority
- dozens of microservices
- Kafka
- Kubernetes
- Temporal
- Celery
- complex distributed orchestration
- premature Feature Store
- causal ML platform
- contextual bandits
- predictive content-performance models
- automated policy exploration
- automated Content Learning promotion
- automatic structural prompt rewriting
- autonomous legal judgment
- sophisticated copyright-similarity engine
- automatic channel repetition AI
- automated people/property release inference
- cross-channel transfer learning engine
- multi-platform publication architecture before a second platform exists
- giant reviewer ensemble
- adaptive QA thresholds without calibration evidence
- giant experimentation platform
- giant dashboard stack
- arbitrary numeric scoring systems
- universal shot-duration constants
- universal hook-duration constants
- universal re-hook cadence
- universal media ratios
- fake provider quality scores

Deferred does not mean prohibited forever.

It means:

prove need first.

---

# 28. CURRENT V1 HUMAN-GATED LIMITS

Until later runtime evidence authorizes more autonomy:

Human Approval is required for:

- public upload
- Content Learning policy promotion
- architecture promotion
- protected-policy changes
- major prompt-structure changes
- major strategy changes
- ambiguous rights/compliance cases as defined by policy

This is a V1 governance choice.

It is not a permanent claim that automation can never expand.

Expansion requires:

- evidence
- bounded policy
- rollback
- observability
- explicit authority change

---

# 29. COST / QUALITY / RIGHTS PRIORITY

FlowMind must not maximize one operational dimension in isolation.

Cheapest is not automatically best.

Fastest is not automatically best.

Highest-quality provider is not automatically best if:

- cost is unsustainable
- latency destroys throughput
- rights are unacceptable
- availability is unstable

Decision contracts should consider the relevant combination of:

- requirement fit
- quality
- rights
- cost
- latency
- reliability
- policy scope

No universal weighted score is required.

---

# 30. FAILURE PHILOSOPHY

FlowMind should fail:

- visibly
- structurally
- recoverably
- with evidence

It should not fail through:

- silent fallback
- silent state mutation
- swallowed exceptions
- stale artifact reuse
- blind retries
- unknown rights silently passing
- changed approved artifacts silently publishing
- provider drift hidden from Learning
- overlapping experiments claiming false causality

A failure may become:

- targeted retry
- reconciliation
- targeted rework
- Human Review
- HALT

depending on owner and policy.

---

# 31. CROSS-MODULE INVALIDATION PRINCIPLE

When an upstream artifact changes materially:

dependent downstream artifacts may become STALE.

Examples:

script changes
-> Canonical Audio may become stale
-> Director Intent may need review
-> Execution Plan becomes stale
-> Render Manifest becomes stale
-> final artifact approval becomes stale

Canonical Audio changes
-> exact shot timing becomes stale
-> captions/timeline may become stale
-> Render Manifest becomes stale

Media Requirement changes
-> resolved asset may need revalidation

Final video changes
-> QA result may become stale
-> publication approval becomes stale

Invalidation should be driven by:

- dependency identity
- hashes
- version refs

not brittle manually maintained assumptions.

---

# 32. RIGHTS / COMPLIANCE OWNERSHIP SUMMARY

Production / Resolver:

- prevents obviously ineligible assets entering production
- stores available Rights Evidence
- does not issue final publication eligibility

Compliance:

- evaluates actual final assets and publication obligations
- evaluates platform-policy evidence
- handles UNKNOWN according to policy
- emits structured compliance result

Human:

- interprets ambiguous cases where required
- does not convert objective corruption into subjective override

Delivery:

- executes only authorized publication package
- does not invent compliance eligibility

---

# 33. LEARNING / CAPABILITY EVOLUTION BOUNDARY

Content Learning may observe provider/model identity as context.

It must not automatically conclude:

Provider A is better than Provider B

from audience outcomes alone.

Possible confounders include:

- topic
- package
- script
- timing
- channel state
- model drift
- production differences

Provider capability comparison belongs to Capability Evolution.

Capability Evolution may use:

- controlled benchmark
- cost
- latency
- error rate
- requirement adherence
- rights
- production canary

Content Learning uses:

- audience/content outcomes
- contextual decision evidence
- policy experiments
- publication interventions

The loops may exchange evidence.

They must not share authority.

---

# 34. LEARNING SAFETY INVARIANTS

Content Learning must never:

- treat missing metrics as zero
- force attribution when UNCLEAR
- call observational association causal proof
- let one outlier rewrite policy
- silently ignore Human interventions
- silently ignore title/thumbnail changes
- optimize a protected-domain violation
- change application code
- activate policy itself
- rewrite arbitrary prompts
- transfer policy across formats/channels silently
- run overlapping material experiments without contamination handling
- reinterpret old observations under changed feature definitions
- overwrite historical metric snapshots
- treat current live analytics as the historic evaluation dataset

---

# 35. QA / COMPLIANCE SAFETY INVARIANTS

Quality + Compliance must never:

- let multimodal opinion become objective technical truth by itself
- let Soft QA become a second Director
- let Compliance become autonomous legal authority
- let UNKNOWN critical rights silently PASS
- let preview PASS substitute final PASS
- let QA orchestrate its own retries
- let QA duplicate Cost Governor authority
- let Delivery invent eligibility
- let an approval float across changed final artifacts
- let Human override corrupt technical output as if corruption were subjective

---

# 36. PRODUCTION SAFETY INVARIANTS

Production must never:

- create fake frame timing before Canonical Audio
- let Router become a second Director
- silently cross the allowed fallback envelope
- let Renderer invent creative decisions
- treat one Scene as mandatory universal execution primitive
- discard expensive reusable media only because an upstream plan changed
- embed provider-specific syntax in Editorial contracts
- create Visual DNA as a God Config
- use universal stock/generated ratios
- use universal cut cadence
- use fake provider scores without calibrated meaning

---

# 37. EDITORIAL SAFETY INVARIANTS

Editorial must never:

- let package be an afterthought after the script
- treat LLM output as predicted CTR truth
- let style quality compensate for unsupported factual claims
- create one aggregate Editorial Score
- silently rewrite text through deterministic checks
- use provider-specific TTS syntax as editorial content
- hard-code universal hook duration
- hard-code universal re-hook cadence
- treat promise identity as proof of semantic alignment

---

# 38. OPPORTUNITY SAFETY INVARIANTS

Opportunity Intelligence must never:

- treat number of URLs as source independence
- treat UNKNOWN as LOW
- use one aggregate score as pseudo-truth
- automatically mutate strategy because one outside-strategy opportunity looks strong
- delete REJECT decisions from history
- call one viral competitor video a reusable pattern
- force topic blame for downstream failure
- let trend/news signal automatically authorize production

---

# 39. CONTROL PLANE SAFETY INVARIANTS

Control Plane must never:

- make creative decisions
- invent QA verdicts
- invent learning hypotheses
- blindly retry ambiguous paid side effects
- silently convert OUTCOME_UNKNOWN to failure
- allow two state authorities
- allow Policy Store to become active-policy authority
- mark operation successful without applicable artifact validation
- silently resume from HALT
- treat timeout as proof of provider failure

---

# 40. V3.2 FINAL TARGET FLOW

Primary content flow:

MARKET / CHANNEL / SEARCH / NEWS SIGNALS
-> NORMALIZATION
-> SOURCE COLLAPSE
-> OPPORTUNITY CANDIDATE
-> OPPORTUNITY DECISION
-> EDITORIAL DESIGN
-> VIEWER PROMISE
-> PACKAGE SELECTION
-> NARRATIVE PLAN
-> OUTLINE
-> SCRIPT
-> EDITORIAL GATE
-> FACTUAL GATE
-> DIRECTOR PASS 1 / VISUAL STAGING
-> CANONICAL AUDIO
-> DIRECTOR PASS 2 / EXECUTION PLAN
-> MEDIA ROUTER
-> RIGHTS / COST PRE-CHECK
-> MEDIA RESOLUTION
-> ASSET VALIDATION
-> PRE-RENDER PLAN VALIDATION
-> DETERMINISTIC RENDER
-> HARD QA
-> COMPLIANCE
-> SOFT QA
-> PUBLICATION ELIGIBILITY
-> HUMAN APPROVAL
-> DELIVERY
-> YOUTUBE
-> ANALYTICS
-> DECISION CONTEXT + OUTCOME SNAPSHOTS
-> EVIDENCE ASSEMBLY
-> HYPOTHESIS
-> TRIAL / VALIDATION
-> EVALUATION
-> POLICY PROPOSAL
-> HUMAN APPROVAL
-> CONTROL PLANE POLICY ACTIVATION
-> MONITOR
-> ROLLBACK / CONTINUE
-> BETTER FUTURE DECISIONS

Parallel capability flow:

PROVIDER / MODEL / EXTERNAL CAPABILITY ECOSYSTEM
-> DISCOVER
-> CANDIDATE REGISTRY
-> CONTRACT FIT
-> SECURITY / RIGHTS / COST CHECK
-> BENCHMARK
-> COMPARE
-> CANARY
-> ADOPT / REJECT
-> CONTROLLED ACTIVATION
-> CAPABILITY REGISTRY
-> MONITOR
-> ROLLBACK / REPLACE
-> BETTER EXECUTION TOOLS

---

# 41. V3.2 SUCCESS CRITERIA

V3.2 is not validated by document completion.

Runtime evidence should eventually demonstrate:

- consistent end-to-end runs
- correct state transitions
- reliable HALT/recovery
- operation idempotency
- safe handling of OUTCOME_UNKNOWN
- artifact identity and invalidation
- script-to-audio identity integrity
- real Canonical Audio timing
- shot-aware execution
- requirement-aware media resolution
- semantic asset suitability
- deterministic final rendering
- real final-output Hard QA
- rights/compliance protection
- publication approval bound to exact artifact
- predictable cost
- bounded rework
- learning evidence persistence
- publication/human intervention logging
- reproducible policy evaluation
- policy promotion and rollback
- capability benchmarking
- provider/model rollback
- reduced manual intervention
- measurable business/content learning

No arbitrary count is considered universal truth before real data exists.

---

# 42. CROSS-MODULE CONTRADICTION CHECKLIST

V3.2 authority-promotion checklist:

1. exactly one Control Plane exists
2. exactly one active-policy binding authority exists
3. QA does not own approval
4. Delivery does not own eligibility
5. Router does not own creative fallback invention
6. Renderer does not own creative decisions
7. Learning does not activate policy
8. Capability Evolution does not mutate content strategy
9. Editorial does not own provider execution
10. Production does not own factual truth
11. Compliance does not become legal opinion authority
12. Cost ownership is not duplicated
13. Rights pre-use and final checks have distinct purposes
14. artifact invalidation does not conflict with reusable asset retention
15. Human Review is distinct from Human Override
16. Policy Store does not contain independent active-state authority
17. Content Learning promotion remains Human-gated in V1
18. public upload remains Human-gated in V1
19. architecture claims remain separate from runtime proof
20. no deferred capability is accidentally described as mandatory V1 implementation
21. external capability / OSS donor adoption does not transfer FlowMind authority to the donor

---

# 43. V3.2 DEFERRED IMPLEMENTATION LIST

Explicitly deferred until runtime evidence justifies it:

- automatic Content Learning promotion
- fully autonomous public upload
- advanced causal inference
- Bayesian experiment engine
- contextual bandits
- automatic experiment allocation
- automatic exploration allocation
- predictive content-performance model
- complex Feature Store
- automatic channel repetition detector
- adaptive QA thresholds
- large multimodal reviewer ensemble
- sophisticated copyright similarity detection
- automated legal-risk judgment
- automated people/property release judgment
- cross-channel transfer learning
- multi-platform publication engine
- complex distributed orchestration
- infrastructure autoscaling beyond proven need

---

# 44. ARCHITECTURE MINIMALISM RULE

V3.2 is not permission to make FlowMind larger.

The objective is:

correct ownership
+
correct contracts
+
correct evidence
+
correct failure behaviour

Prefer:

- MERGE
- SIMPLIFY
- CLARIFY
- VERSION
- BOUND
- REUSE

over:

- NEW MODULE
- NEW SERVICE
- NEW DATABASE
- NEW PROVIDER
- NEW AGENT
- NEW INFRASTRUCTURE

unless evidence materially requires it.

---

# 45. BUILD VS BUY PRINCIPLE

Build internally where the logic is FlowMind-specific:

- opportunity decision policy
- editorial contracts
- production contracts
- fallback envelope semantics
- QA/compliance contracts
- evidence schemas
- learning policy governance
- provider benchmark policy
- state/control semantics

Buy/reuse where the capability is commodity:

- LLM generation
- TTS
- image generation
- video generation
- stock media
- search
- analytics APIs
- generic multimodal review
- external agent skills where contract fit is strong
- OSS tools/workflows where contract fit is strong
- MCP-style capabilities where contract fit is strong
- rendering infrastructure where practical

Do not confuse:

owning the decision

with:

owning the underlying model.

---

# 46. PROVIDER-INDEPENDENCE PRINCIPLE

Domain modules request capabilities.

They should not depend unnecessarily on:

- one model name
- one vendor-specific payload shape
- one provider-specific prompt format
- one provider-specific storage format

Adapters may translate stable FlowMind contracts into provider-specific calls.

Provider-specific features may be used.

They must remain isolated behind explicit adapters/capability contracts where practical.

---

# 47. VERSIONING PRINCIPLE

Version only what materially changes interpretation or reproducibility.

Relevant version dimensions may include:

- schema_version
- policy_version
- evaluation_policy_version
- feature_definition_version
- metric_definition_version
- provider/model version
- artifact version
- prompt-policy version where applicable
- Visual DNA version
- Output Specification version
- compliance-policy version
- QA-policy version

Avoid version spaghetti.

Do not reuse the same semantic version identifier for materially different content.

---

# 48. HUMAN ATTENTION PRINCIPLE

Human attention is expensive.

Reserve it for:

- ambiguity
- high risk
- policy promotion
- architecture change
- protected domains
- publication during V1
- unusual failure
- evidence conflict

Do not require Human review merely because:

- a deterministic stage succeeded
- a normal low-risk retry occurred
- routine evidence was collected

Human gates should protect risk.

They should not become workflow ceremony.

---

# 49. EVIDENCE PRINCIPLE

Critical FlowMind decisions should be evidence-backed.

Evidence may include:

- source refs
- hashes
- provider response metadata
- runtime measurements
- metrics snapshots
- rights evidence
- policy evidence
- QA measurements
- Human decisions
- incident records
- experiment membership
- evaluation snapshots

Do not store unsupported conclusions as if they were evidence.

Do not store hidden chain-of-thought.

Use structured reasons and references.

---

# 50. UNKNOWN PRINCIPLE

UNKNOWN is a legitimate state.

Do not automatically convert it to:

- LOW
- PASS
- FAIL
- zero
- average
- safe
- irrelevant

Handling depends on:

- domain
- risk
- available evidence
- policy

Critical UNKNOWN often requires:

- evidence retrieval
- Human Review
- HALT

Non-critical UNKNOWN may remain:

- warning
- incomplete evidence
- non-blocking state

The meaning must be explicit.

---

# 51. POLICY PROMOTION PRINCIPLE

A candidate policy is not active because it exists.

Required conceptual path:

HYPOTHESIS
-> TRIAL / VALIDATION
-> EVALUATION
-> POLICY PROPOSAL
-> HUMAN APPROVAL
-> CONTROL PLANE ACTIVATION
-> MONITOR
-> ROLLBACK IF REQUIRED

in V1.

Policy promotion must retain:

- source hypothesis
- evidence
- previous version
- candidate version
- changed fields
- scope
- risk
- guardrails
- rollback target

---

# 52. CAPABILITY PROMOTION PRINCIPLE

A provider/model candidate is not active because it is newer.

Required conceptual path:

DISCOVER
-> REGISTER CANDIDATE
-> BENCHMARK
-> CANARY
-> PROMOTION DECISION
-> CONTROLLED ACTIVATION
-> MONITOR
-> ROLLBACK IF REQUIRED

Capability changes must retain:

- provider/model identity
- benchmark evidence
- cost
- latency
- quality evidence
- error behaviour
- rights/terms context
- rollout decision

---

# 53. CLOUD-FIRST PRINCIPLE

The target runtime is cloud-first.

But architecture must not force premature infrastructure.

The always-on authority should eventually live independently of a personal computer.

Optional workers may come and go.

Canonical state and evidence must survive worker loss.

Cloud-first does not mean:

microservices-first.

Cloud-first means:

control and knowledge do not depend on one laptop being online.

---

# 54. CURRENT BUSINESS PRIORITY

FlowMind engineering priority remains:

1. SPEED
2. STABILITY
3. SCALE
4. OPTIMIZATION

Architecture should support scale.

It should not pre-build scale without evidence.

The first production objective after V3.2 promotion remains:

close the highest-value verified runtime gap
and achieve a crude but real end-to-end production path.

Quality hardening follows after the skeleton can complete real work.

---

# 55. IMPLEMENTATION REENTRY AFTER V3.2

After V3.2 becomes trusted:

do not immediately implement every missing architecture feature.

Required sequence:

1. use verified AS-IS runtime evidence
2. compare runtime against trusted V3.2
3. classify existing components:
   KEEP / MODIFY / REPLACE / REMOVE / MISSING
4. identify exactly one highest-value implementation gap
5. authorize one specific target
6. modify one controlled contour
7. validate with runtime evidence
8. commit
9. continue

Architecture priority alone does not define implementation priority.

---

# 56. AUTHORITY NOTE

This file is:

TRUSTED DETAILED TARGET ARCHITECTURE

Its authority role is assigned by:

FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

It is not:

- current operational authority
- runtime truth
- implementation evidence

Current operational state belongs only to:

FLOWMIND_ACTIVE_MAP.md

Runtime truth comes only from verified repo and runtime evidence.

Future target-architecture replacement must occur through the Authority Reconciliation / publication process defined by the active governance system.

This file must not self-promote a future replacement or redefine authority routing.

---

# 57. FINAL V3.2 PRINCIPLES

1. One Control Plane.
2. One active-policy binding authority.
3. Runtime evidence beats architectural assumption.
4. Architecture does not prove implementation.
5. Build decision logic; reuse commodity capabilities.
6. Provider identity remains replaceable.
7. Opportunity owns WHAT deserves attention and WHY NOW.
8. Editorial owns WHAT is promised and said.
9. Production owns HOW editorial intent becomes audiovisual execution.
10. Canonical Audio is downstream timing truth.
11. Exact shots are planned only after real audio exists.
12. Router operates inside Director-approved creative envelopes.
13. Renderer is deterministic and non-creative.
14. Hard QA owns objective final-artifact technical validation.
15. Soft QA detects semantic/visible defects without becoming Director.
16. Compliance evaluates rights/policy evidence without becoming autonomous legal authority.
17. UNKNOWN is first-class.
18. Human Review is not the same as Human Override.
19. Approval binds to exact artifact identity.
20. Delivery executes authorization; it does not invent eligibility.
21. Learning proposes policy; it does not activate policy.
22. V1 Content Learning promotion remains Human-gated.
23. Content Learning and Capability Evolution remain separate.
24. Raw evidence is more durable than premature derived labels.
25. Historical decisions and metrics are append-only where interpretation matters.
26. Publication and Human interventions are part of attribution truth.
27. Correlation is not causal proof.
28. Protected domains cannot be optimized away by performance.
29. Every promoted change remains reversible where rollback is valid.
30. Cost is a first-class runtime constraint.
31. Rights evidence is retained where practical.
32. No silent creative degradation.
33. No silent policy mutation.
34. No blind retry of ambiguous paid/external side effects.
35. No second production contour.
36. No second dispatcher.
37. No second policy activation authority.
38. No aggregate fake score is required where categorical evidence is more honest.
39. No universal magic threshold without a real basis.
40. No premature ML.
41. No automatic structural prompt rewriting.
42. No autonomous public upload in V1.
43. No autonomous Content Learning promotion in V1.
44. Knowledge belongs to FlowMind, not to one provider.
45. Cloud Core must not depend on a personal laptop remaining online.
46. Human attention is reserved for ambiguity and risk.
47. Every critical decision must remain auditable.
48. Simplicity wins unless complexity produces measurable value.
49. Speed first, then stability, then scale, then optimization.
50. Skeleton first, real end-to-end first, quality hardening second.
51. External capabilities may contribute execution, but FlowMind retains control, evidence, policy and verdict authority.

---

# 58. FINAL STATUS

V3.2 is the trusted detailed target architecture assigned by the Source of Truth Registry.

Its architecture review and authority-promotion checks are treated as completed evidence unless:

- this file materially changes
- a validation fails
- new material evidence reveals a specific defect
- a verified authority conflict directly requires re-evaluation

This document does not authorize implementation by itself.

Implementation work must proceed from:

FLOWMIND_ACTIVE_MAP.md

using verified current repo/runtime evidence compared against this trusted target.

No runtime executor changes are authorized merely by this document.

End.
