FLOWMIND WORK PROTOCOL V1

Status: TRANSITIONAL REFERENCE / COMPATIBILITY DOCUMENT Project:
FlowMind / Imagine What If Scope: compatibility pointer for historical
references; no independent permanent execution rules and no current
operational state

1. Purpose

This file is retained temporarily because existing FlowMind documents or
historical work may reference:

docs/FLOWMIND_WORK_PROTOCOL_V1.md

Permanent operating and execution discipline is now owned by:

FLOWMIND_CORE_RULES.md

This file must not duplicate that rule set.

2. Canonical execution discipline

For all current FlowMind work, use:

FLOWMIND_CORE_RULES.md

That includes:

-   logical-action execution
-   evidence discipline
-   verification sufficiency
-   anti-loop behavior
-   execution momentum
-   fresh-file discipline
-   full-file replacement
-   API preflight discipline
-   Future Impact Gate
-   security and reliability
-   Git discipline
-   response discipline
-   new-chat recovery behavior

If historical wording in this Work Protocol conflicts with
FLOWMIND_CORE_RULES.md:

FLOWMIND_CORE_RULES.md wins.

3. Important execution clarification

The unit of work is a LOGICALLY COMPLETED ACTION.

It is not one command, one terminal output, or one mechanical substep.

One logical action may contain multiple sequential commands and
validations when they serve one objective and do not require a new
decision between them.

Do not force unnecessary user turns between mechanical substeps.

4. Current operational state

This file does not own:

-   current mode
-   current target
-   current step
-   current next action
-   current allowed production work
-   current forbidden production work
-   current exit condition
-   runtime implementation status

Current operational state belongs only to:

FLOWMIND_ACTIVE_MAP.md

5. Authority routing

Permanent operating/execution rules: FLOWMIND_CORE_RULES.md

Current operational state: FLOWMIND_ACTIVE_MAP.md

Product intent: FLOWMIND_WORKING_TARGET.md

Authority classification and reference routing:
FLOWMIND_SOURCE_OF_TRUTH_REGISTRY.md

Detailed architecture: CURRENT_TRUSTED_DETAILED_TARGET as resolved by
the Registry

Control-plane semantics: CANONICAL_DISPATCHER_SPEC.md

Runtime truth: verified current repo and runtime evidence

6. Historical references

Historical references to sections of the former long Work Protocol may
be used only as historical evidence.

They must not override:

-   FLOWMIND_CORE_RULES.md
-   FLOWMIND_ACTIVE_MAP.md
-   newer verified repo/runtime evidence

Do not reconstruct the retired long protocol merely because an old
handoff, commit, or document references it.

7. Migration behavior

During the governance simplification transaction:

-   runtime implementation remains frozen
-   unrelated architecture work remains frozen
-   active references to this Work Protocol should be migrated when
    their owning file is processed
-   no duplicate permanent execution authority should be recreated

This compatibility file may remain until active authority references
have been reconciled and final cross-file validation passes.

8. Retirement condition

After:

-   active authority routing points to FLOWMIND_CORE_RULES.md
-   FLOWMIND_ACTIVE_MAP.md is compact and current
-   cross-file authority validation passes
-   the governance simplification block is committed and pushed
-   required Project Sources are synchronized

this file may be classified as FROZEN LEGACY or otherwise removed from
the active authority set.

Until then, it exists only for compatibility and reference continuity.

End.
