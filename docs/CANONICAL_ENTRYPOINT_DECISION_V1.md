# CANONICAL ENTRYPOINT DECISION V1

## Status
Phase 2 active.
Control-layer cleanup in progress.

## Decision
The active canonical entrypoint will reuse existing canonical dispatcher tooling.

### KEEP
- tools/dispatcher_cli.py
- tools/dispatcher.sh
- tools/check_dispatcher.sh

## Meaning
- tools/dispatcher_cli.py is the active canonical dispatcher entrypoint.
- tools/dispatcher.sh is the shell wrapper for canonical dispatcher usage.
- tools/check_dispatcher.sh is the canonical dispatcher validation entrypoint.

## Not Allowed
- Do not restore legacy main.py control flow.
- Do not restore dispatcher/engine.py control flow.
- Do not restore dispatcher/engine_v16.py control flow.
- Do not introduce a new parallel entrypoint without strong practical need.

## Current Rule
During Phase 2, do not create a new root entrypoint if the existing canonical dispatcher CLI already satisfies active control-layer needs.

## Practical Conclusion
The repository does not currently need a newly invented entrypoint.
It needs control-layer alignment around the already existing canonical dispatcher entry tooling.
