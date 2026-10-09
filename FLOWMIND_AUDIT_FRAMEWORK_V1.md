# FLOWMIND AUDIT FRAMEWORK V1.0

Status: APPROVED METHODOLOGY / PUBLISHED IN REPOSITORY
Project: FlowMind / Imagine What If
Scope: system-wide evidence-driven audit methodology, not current operational state

## 1. Authority and boundaries

This document defines HOW a system-wide audit is performed. It is a reference methodology, not a seventh canonical authority, not a dispatcher, and not a current-state checkpoint.

- Permanent execution rules: FLOWMIND_CORE_RULES.md
- Current target, checkpoint, NOT DONE and next action: FLOWMIND_ACTIVE_MAP.md
- Authority routing and classification: FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md
- Product intent: FLOWMIND_WORKING_TARGET.md
- Detailed target architecture: CURRENT_TRUSTED_DETAILED_TARGET resolved by the Registry
- Control-plane semantics: CANONICAL_DISPATCHER_SPEC.md
- Runtime implementation truth: verified current repository and runtime evidence

If this methodology conflicts with a canonical authority, STOP and resolve the conflict through the appropriate owner. This document must not override runtime facts or establish its own active operational state.

## 2. Audit objective

Determine whether the actual end-to-end FlowMind pipeline can reliably produce editorially acceptable, legally usable and economically viable videos without hidden fallbacks, lost Director intent, fixture-specific assumptions, or unbounded cost.

Audit actual modules and contracts discovered in the current repository; do not assume that target architecture blocks correspond one-to-one with implemented modules. The conceptual architecture may describe blocks 00-06, but their existence must be proven in runtime.

## 3. Evidence standard

For every material finding record:

- claim / requirement
- source of authority or contract
- exact implementation or artifact location
- reproducible evidence or test command and result
- evidence status: VERIFIED, PARTIAL, UNKNOWN
- impact, affected upstream/downstream boundaries and next decision

VERIFIED: sufficient direct evidence supports the narrow claim.
PARTIAL: some evidence exists, but coverage or conclusion is incomplete.
UNKNOWN: evidence is missing or insufficient; do not invent PASS or FAIL.

A known defect can be recorded as VERIFIED FAILURE when evidence proves it. Distinguish defect from unavailable provider, missing credentials, quota, or environment failures. Historical reports do not establish current runtime status without freshness verification.

## 4. Hard Gates (independent of numerical scores)

A material failure in any applicable gate blocks the relevant production readiness claim, regardless of aggregate scores:

1. Contract integrity: schemas, required fields, producer/consumer semantics, versioning and traceability.
2. Editorial safety: no visible technical prompt text, diagnostic placeholders, misleading fake success or unintended fallback content in published output.
3. Director intent: visual_intent, must_show, must_not_show, overlay_intent and other actual required instructions survive relevant downstream transformations; applicability follows the verified contract.
4. Framing and composition: aspect ratio, crop, black bars, readability, temporal fit and visual suitability for the requested format.
5. Reliability: deterministic failure reporting, idempotency where applicable, resumability and absence of silent errors.
6. Cost and provider control: bounded calls, rate/quota handling, measured costs, no uncontrolled retries or purchases.
7. Rights and licensing: provenance and permitted usage for generated and sourced assets.
8. Editorial quality: narrative clarity, visual relevance, pacing, repetition and meaningful viewer value.

Gate outcomes: PASS / FAIL / UNKNOWN / NOT APPLICABLE, each with evidence. UNKNOWN is not silently converted to FAIL; it prevents an unsupported readiness assertion when the gate is material.

## 5. MQS-100 — Module Quality Score

Assess only actual modules verified in the repository. Define module-specific weighted criteria totaling 100 BEFORE scoring; use dimensions relevant to each module such as contract compliance, correctness, resilience, observability, cost and downstream preservation.

Do not fabricate numeric scores for unverified dimensions. Report evidence coverage and UNKNOWN dimensions separately. Scores are comparative audit aids, never substitutes for Hard Gates or proof of end-to-end quality.

## 6. FDS-100 — Fix Decision Score

Prioritize candidate changes against the explicit baseline option DO NOTHING / MINIMAL CHANGE. Evaluate:

- verified root-cause impact and affected production outputs
- cross-module and future-format compatibility
- cost, implementation time and expected ROI
- regression probability and blast radius
- reversibility and expected cost of failure
- effect on complexity and source-of-truth ownership

Define weights for the current decision before assigning any score. Do not present FDS numbers without evidence and weights. Prefer the smallest production-safe fix; defer speculative infrastructure.

## 7. VQS-100 — Video Quality Score

Evaluate the actual rendered output separately from technical pipeline validity. Relevant dimensions may include hook, clarity, pacing, narrative continuity, visual relevance, composition, audio quality, novelty and editorial trust.

Define the rubric and weights for the video format before scoring. Technical render PASS does not imply editorial PASS. Viewer retention, CTR, watch time, revenue and other YouTube metrics are separate observed business evidence, not simulated VQS outcomes.

## 8. Future Impact Gate

Before approving a fix, evaluate its effects on:

- Long 16:9 and Shorts 9:16 where supported
- variable scene, beat, shot and visual-unit counts
- variable duration and Director requirements
- different provider outputs and supported configurations
- contract ownership, upstream/downstream compatibility
- retries, idempotency, observability, cost and scaling

Do not hardcode to a single R2 or R3 fixture. Do not build hypothetical adapters or infrastructure without evidence of need. Follow the existing Core Rules Future Impact Gate; do not duplicate its authority.

## 9. Execution sequence

1. Runtime Evidence: recover last verified checkpoint, inspect current repo state and reproduce only the necessary baseline.
2. Impact Triage: identify high-impact blockers and evidence gaps; separate runtime defects from provider/configuration failures.
3. Contract & Module Audit: trace real artifacts and producer-consumer boundaries; apply Hard Gates and evidence-qualified MQS.
4. Targeted Quality Hardening: choose fixes using FDS against minimal-change baseline.
5. Downstream Regression: prove preserved Director intent, contract validity and absence of new failures.
6. Integrated Validation: exercise representative Long/Shorts, variable scene counts and material failure modes as supported.
7. Production Readiness: decide based on Hard Gates, measured VQS, actual cost and remaining UNKNOWN items.

Each phase is a decision boundary, not a requirement to run every possible check. Use the Core Rules smallest-sufficient-evidence and anti-loop discipline.

## 10. Known historical evidence: R2

Prior review reported a technically rendered R2 video with serious editorial defects: visible technical-prompt placeholder beats, portrait stock creating black bars, weak visual relevance and incomplete preservation of Director requirements. These are historical audit inputs, not proof that the current repo or R3 still has the same defects. Reconfirm freshness before treating them as active failures.

Do not infer that FFmpeg created technical text overlays: prior evidence attributed visible text to deterministic visual-provider PNG generation. Verify the current implementation before choosing a fix.

## 11. Stop, release and recovery discipline

- Never declare production-ready when a material Hard Gate is FAIL or material UNKNOWN is unresolved.
- Record blockers, decisions, proof and the single next action in FLOWMIND_ACTIVE_MAP.md; do not create a parallel handoff.
- Register this methodology as a reference in the Source of Truth Registry without changing canonical ownership.
- Commit only validated, intended governance changes; do not stage unrelated project runtime artifacts.
- Push and synchronize relevant Project Sources when the governance transaction is ready for publication.
- Verify new-chat recovery using Core Rules + Active Map; consult this framework only when the active audit decision requires it.
- No autonomous monitoring is implied by this file. Compliance checks occur during normal decision/execution workflow unless a separate actual runner is implemented and verified.

## 12. Acceptance criteria for publication

- Framework file exists in current repository with exact reviewed content.
- Registry points to it as a reference methodology, not a canonical owner.
- Active Map names SYSTEM AUDIT as current target, captures verified boundary, material NOT DONE and one next action.
- Cross-file authority and reference consistency checked.
- Git diff and status inspected; unrelated untracked runtime evidence excluded.
- Validated governance block committed/pushed as appropriate; Project Sources synchronized and recovery checked.

End of FlowMind Audit Framework V1.0.
