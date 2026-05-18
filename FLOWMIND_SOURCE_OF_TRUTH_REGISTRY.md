# FLOWMIND SOURCE OF TRUTH REGISTRY

Status: ACTIVE INDEX
Authority: Subordinate to FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md

## Purpose

This file is an operational index of document authority.

It does not replace FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md.

The trusted boundary file remains the higher authority for deciding what is trusted, frozen, or unverified.

## Authority Rule

Primary authority:

- FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md

This registry must not contradict the trusted boundary list.

If this registry and the trusted boundary list disagree, the trusted boundary list wins.

## Status Model

This registry uses the same trust model as the trusted boundary list:

- TRUSTED
- FROZEN LEGACY
- UNVERIFIED

No separate authority model is allowed here.

## Active Truth

FlowMind is a niche-driven media intelligence and production system.

FlowMind receives input parameters such as niche, language, format, audience, style, allowed sources, and business goal.

FlowMind analyzes validated sources, competitors, YouTube, Reddit, and other signals to identify under-covered or poorly covered content opportunities.

Production comes after topic validation.

FlowMind is not a horror-content system.

Imagine What If is not equal to FlowMind Core.

A channel, niche, or style config must not be treated as FlowMind Core.

## Current Document Index

| Document | Status | Rule |
|---|---:|---|
| FLOWMIND_TRUSTED_BOUNDARY_LIST_V1.md | TRUSTED | Primary authority for trust boundaries. |
| FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md | TRUSTED | Operational index only; subordinate to trusted boundary list. |
| FLOWMIND_SYSTEM_MAP_V1.md | TRUSTED | Active recovery guidance. |
| FLOWMIND_ACTION_SEQUENCE_V1.md | TRUSTED | Active recovery sequence guidance. |
| FLOWMIND_REPO_TRUST_BOUNDARY_V1.md | TRUSTED | Repo trust boundary guidance. |
| docs/FLOWMIND_HARD_RULESET_V1.md | TRUSTED | Work discipline and decision behavior. |
| docs/FLOWMIND_WORK_PROTOCOL_V1.md | TRUSTED | Work protocol for Evgen and ChatGPT. |
| CANONICAL_DISPATCHER_SPEC.md | TRUSTED | Trusted as control-policy and architectural-alignment document. Not automatic proof that every referenced implementation is valid. |
| FLOWMIND_WORKING_TARGET.md | TRUSTED | Trusted only as target-shape and system-intent guidance. Not trusted as proof of implemented runtime. |
| main.py | TRUSTED | Trusted only as blocking tombstone for retired legacy entrypoint. Not an active runtime launcher. |
| cashflow/topic_intelligence/niche_profile_schema.json | TRUSTED | Niche profile structure. |
| cashflow/topic_intelligence/profiles/debt_trap_us_v1.json | TRUSTED | Reviewed niche profile example. |
| cashflow/topic_intelligence/profiles/hidden_fees_us_v1.json | TRUSTED | Reviewed niche profile example. |
| cashflow/topic_intelligence/profiles/finance_legacy_v1.json | UNVERIFIED | Must be reviewed before use. |
| FLOWMIND_CANONICAL_MAP.md | FROZEN LEGACY | Historical dual-system snapshot only. Must not guide current architecture. |
| MASTER_PROMPTS_v2_FULL.txt | FROZEN LEGACY | External/old prompt artifact. Not valid as repo truth. |
| IronCore v3.5 references | FROZEN LEGACY | Historical context only unless explicitly re-approved. |
| Imagine What If horror rules | UNVERIFIED | May become niche/style config only after review. Not FlowMind Core. |

## Docs Index — TRUSTED

| Document | Status | Rule |
|---|---:|---|
| docs/BOOTSTRAP_AUDIT_V1.md | TRUSTED | Bootstrap/init audit checkpoint. Trusted as review evidence, not redesign plan. |
| docs/CANONICAL_DISPATCHER_ENTRYPOINTS.md | TRUSTED | Locked canonical dispatcher entrypoint decision. |
| docs/CANONICAL_ENTRYPOINT_DECISION_V1.md | TRUSTED | Active control-layer entrypoint decision. |
| docs/CANONICAL_MANIFEST_SPEC.md | TRUSTED | Canonical manifest/state contract. |
| docs/CONTROL_LAYER_AUDIT_V1.md | TRUSTED | Control-layer audit verdict for one active contour. |
| docs/DISPATCHER_CHEAT_SHEET.md | TRUSTED | Operational cheat sheet for canonical dispatcher commands. |
| docs/DISPATCHER_ENGINE_STATUS.md | TRUSTED | Audit truth for retired dispatcher/engine.py legacy tombstone. |
| docs/DISPATCHER_ENTRYPOINT.md | TRUSTED | Active dispatcher command-surface truth. |
| docs/FLOWMIND_HARD_RULESET_V1.md | TRUSTED | Work discipline and decision behavior. |
| docs/FLOWMIND_WORK_PROTOCOL_V1.md | TRUSTED | Cooperation protocol for FlowMind work. |
| docs/INTEGRATION_AUDIT_V1.md | TRUSTED | Integration audit checkpoint for legacy/canonical separation. |
| docs/MAIN_PY_STATUS.md | TRUSTED | Audit truth for main.py retired legacy tombstone. |
| docs/PHASE2_AUDIT_STANDARD.md | TRUSTED | Audit standard for cleanup and one-contour recovery. |
| docs/RUNTIME_AUDIT_V1.md | TRUSTED | Runtime audit checkpoint for canonical state-control layer. |

## Docs Index — FROZEN LEGACY

| Document | Status | Rule |
|---|---:|---|
| docs/COMPAT_ADAPTER_SMOKE_CHECK_V1.md | FROZEN LEGACY | Historical compatibility adapter smoke note. Not active execution path. |
| docs/MIGRATION_ROADMAP_V1.md | FROZEN LEGACY | Historical migration roadmap. Not current cleanup strategy. |
| docs/READ_ONLY_ADAPTER_USAGE_V1.md | FROZEN LEGACY | Historical read-only adapter usage note. Not active adapter work. |
| docs/READ_ONLY_COMPATIBILITY_BRIDGE.md | FROZEN LEGACY | Historical compatibility bridge plan. Not active implementation plan. |

## Docs Index — UNVERIFIED

| Document | Status | Rule |
|---|---:|---|
| docs/FLOWMIND_6_CORE_ENGINES_CONTRACTS_V1.md | UNVERIFIED | Production architecture claim. Must not guide implementation until reviewed against current FlowMind Core. |
| docs/FLOWMIND_CANONICAL_ARCHITECTURE_V1.md | UNVERIFIED | Contains possible outdated scope. Must not guide decisions until reviewed. |
| docs/FLOWMIND_DIRECTOR_ENGINE_V1.md | UNVERIFIED | Creative/production engine specification. Must not guide current architecture until reviewed. |
| docs/FLOWMIND_SHOT_SCHEMA_V1.md | UNVERIFIED | Shot/visual production schema. Must not guide current architecture until reviewed. |
| docs/LEGACY_TO_CANONICAL_PHASE_MAPPING.md | UNVERIFIED | Migration mapping document. Must not guide current architecture until reviewed. |
| docs/M3_BOUNDARY_AUDIT.md | UNVERIFIED | Migration boundary audit. Must not guide active cleanup until reviewed. |
| docs/M4_READ_ONLY_ADAPTER_CONTRACT.md | UNVERIFIED | Migration adapter contract. Must not guide active cleanup until reviewed. |
| docs/M5_ADAPTER_NON_AUTHORITY_RULE.md | UNVERIFIED | Migration adapter rule. Must not guide active cleanup until reviewed. |
| docs/M6_LEGACY_READ_SCOPE_RULE.md | UNVERIFIED | Migration adapter read-scope rule. Must not guide active cleanup until reviewed. |
| docs/M7_ADAPTER_VERSIONING_RULE.md | UNVERIFIED | Migration adapter versioning rule. Must not guide active cleanup until reviewed. |
| docs/M8_ADAPTER_FAIL_CLOSED_RULE.md | UNVERIFIED | Migration adapter fail-closed rule. Must not guide active cleanup until reviewed. |
| docs/M9_ADAPTER_REQUIRED_FIELDS_RULE.md | UNVERIFIED | Migration adapter required-fields rule. Must not guide active cleanup until reviewed. |
| docs/MIGRATION_ADAPTER_PACK_SUMMARY.md | UNVERIFIED | Migration adapter summary. Must not guide active cleanup until reviewed. |
| docs/MIGRATION_STATUS_V1.md | UNVERIFIED | Migration status document. Must not guide active cleanup until reviewed. |

## Runtime Index — engine/

| Path | Status | Rule |
|---|---:|---|
| engine/canonical_dispatcher.py | TRUSTED | Canonical dispatcher logic for phase transitions, HALT/resume, QA approval, and upload approval state transitions. |
| engine/state_store.py | TRUSTED | Canonical atomic state persistence layer. State writes must go through this layer or approved dispatcher paths. |
| engine/state_validator.py | TRUSTED | Canonical PROJECT_STATE.json and manifest validation layer. |
| engine/legacy_guard.py | TRUSTED | Trusted only as fail-fast blocker for frozen legacy station pipeline. Not a production engine. |
| engine/global_hard_gate_v1.py | TRUSTED | Trusted only as legacy tombstone that imports legacy_guard and blocks frozen station execution. |
| engine/modules/s1_strategy.py | TRUSTED | Trusted only as frozen legacy module tombstone. Must not be executed as production module. |
| engine/module_runner.py | UNVERIFIED | Phase-to-module runner that can route to legacy/station-style modules. Must not be used until reviewed. |
| engine/modules/s2_script.py | UNVERIFIED | Script module with direct PROJECT_STATE.json write path and OpenAI call. Must not be executed until reviewed or converted to canonical executor contract. |

## Runtime Prohibitions — engine/

Do not treat engine/module_runner.py as an active phase runner.

Do not execute engine/modules/s2_script.py as active runtime.

Do not allow direct PROJECT_STATE.json writes outside canonical dispatcher/state_store authority.

Do not treat legacy tombstones as production modules.

Do not reactivate engine/modules/* without explicit review and registry update.

## Runtime Index — tools/ TRUSTED

| Path | Status | Rule |
|---|---:|---|
| tools/dispatcher.sh | TRUSTED | Official user-facing canonical dispatcher shell entrypoint. |
| tools/dispatcher_cli.py | TRUSTED | Canonical dispatcher CLI implementation used by tools/dispatcher.sh. |
| tools/check_dispatcher.sh | TRUSTED | Canonical dispatcher validation entrypoint. |
| tools/run_dispatcher_checks.py | TRUSTED | Dispatcher smoke/guard checks using canonical dispatcher and state_store. |
| tools/smoke_test_dispatcher.py | TRUSTED | Dispatcher smoke test using canonical dispatcher and state_store. |
| tools/bootstrap_project.sh | TRUSTED | Shell wrapper for canonical PROJECT_STATE bootstrap. |
| tools/bootstrap_project_state.py | TRUSTED | Canonical PROJECT_STATE bootstrap implementation using state_store and manifest hash logic. |
| tools/preflight.sh | TRUSTED | Pre-commit/preflight safety runner. |
| tools/shell_lint_quick.sh | TRUSTED | Shell syntax lint helper for tools/*.sh. |
| tools/json_lint_quick.sh | TRUSTED | JSON lint helper for repository JSON files. |
| tools/manifest_guard_scan.py | TRUSTED | Guard scanner for direct ExecutionManifest.json write risks. |
| tools/code_check.py | TRUSTED | Code check helper. Trusted only as validation support, not runtime authority. |

## Runtime Index — tools/ FROZEN LEGACY

| Path | Status | Rule |
|---|---:|---|
| tools/contract_validation.py | FROZEN LEGACY | Frozen station-pipeline validator blocked through legacy_guard. Must not be used as active validation. |

## Runtime Index — tools/ UNVERIFIED

| Path | Status | Rule |
|---|---:|---|
| tools/README_SAFE_EDITING.md | UNVERIFIED | Conflicts with active no-heredoc editing discipline. Must not guide editing until rewritten and reviewed. |
| tools/build_compat_payload.sh | UNVERIFIED | Compatibility payload helper. Must not guide active cleanup until reviewed. |
| tools/cleanup_manifest_guard_worktree.sh | UNVERIFIED | Worktree cleanup helper for manifest guard work. Must not be used until reviewed. |
| tools/fm_edit.sh | UNVERIFIED | Editing helper. Must not guide file edits until reviewed against full-replacement/no-heredoc rule. |
| tools/git_commit_core_tools.sh | UNVERIFIED | Git helper. Must not be used until reviewed. |
| tools/git_stage_core_tools.sh | UNVERIFIED | Git staging helper. Must not be used until reviewed. |
| tools/git_stage_manifest_single_writer_fix.sh | UNVERIFIED | Git staging helper for manifest single-writer changes. Must not be used until reviewed. |
| tools/install_githooks.sh | UNVERIFIED | Git hook installer. Must not be used until reviewed. |
| tools/json_autofix_s2_or_quarantine.sh | UNVERIFIED | JSON autofix/quarantine helper. Must be reviewed before use. |
| tools/json_repair_or_quarantine.sh | UNVERIFIED | JSON repair/quarantine helper. Must be reviewed before use. |
| tools/json_write_locked.sh | UNVERIFIED | JSON writer helper. Must be reviewed before use as approved write path. |
| tools/json_write_safe.sh | UNVERIFIED | JSON writer helper. Must be reviewed before use as approved write path. |
| tools/manifest_write.py | UNVERIFIED | Manifest writer helper. Must be reviewed before use. |
| tools/rewrite_json_write_safe.sh | UNVERIFIED | Regenerates json_write_safe.sh using heredoc. Must not be used under active no-heredoc discipline until reviewed. |
| tools/run_topic_pipeline.sh | UNVERIFIED | Topic intelligence runner. Must not be treated as production entrypoint until reviewed. |
| tools/safe_write.sh | UNVERIFIED | Base64 write helper. Must not guide active editing until reviewed. |
| tools/selftest_manifest_single_writer.sh | UNVERIFIED | ExecutionManifest single-writer selftest. Must not guide active runtime until reviewed. |
| tools/semantic_validation.py | UNVERIFIED | Legacy S1/S2 semantic validator. Must not guide active validation until reviewed. |
| tools/structural_validation.py | UNVERIFIED | Legacy S1/S2 structural validator. Must not guide active validation until reviewed. |
| tools/test_profile_runtime_collector.py | UNVERIFIED | Topic intelligence profile test using finance_legacy profile. Must not guide active runtime until reviewed. |
| tools/test_topic_intelligence_core.py | UNVERIFIED | Topic intelligence test helper. Must not guide active runtime until reviewed. |
| tools/verify_canonical_map.sh | UNVERIFIED | Verifies frozen historical canonical map. Must not guide current architecture until reviewed. |
| tools/write_text_atomic.sh | UNVERIFIED | Text writer helper using stdin flow and heredoc-style usage comments. Must not guide active editing until reviewed. |

## Runtime Prohibitions — tools/

Do not use tools/README_SAFE_EDITING.md as active editing policy.

Do not use heredoc-based editing instructions as active FlowMind workflow.

Do not use tools/rewrite_json_write_safe.sh under active no-heredoc discipline until reviewed.

Do not use tools/safe_write.sh or tools/write_text_atomic.sh as active editing standard until reviewed.

Do not treat tools/run_topic_pipeline.sh as production topic runtime until reviewed.

Do not treat legacy S1/S2 validators as active validation for current FlowMind Core.

Do not use git helper scripts unless explicitly reviewed and listed as trusted.

## Prohibitions

Do not treat unlisted files as trusted.

Do not treat unverified files as architecture.

Do not treat frozen legacy as active guidance.

Do not treat a channel, niche, or style config as equal to FlowMind Core.

Do not delete files before runtime reference check.
