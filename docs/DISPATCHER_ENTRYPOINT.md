# DISPATCHER ENTRYPOINT

Status: ACTIVE CONTROL TRUTH  
Branch: `cashflow-mode`

## Canonical rule

For `cashflow-mode`, the canonical dispatcher has one operational command surface.

There is no root launcher.
There is no alternative entrypoint.
There is no legacy integration layer.

## Active entrypoint

The only valid user-facing dispatcher entrypoint is:

- `tools/dispatcher.sh`

## CLI layer

- `tools/dispatcher_cli.py`

This file implements the canonical CLI logic and must not be treated as the primary operator-facing command surface.

## Validation entrypoint

- `tools/check_dispatcher.sh`

This is the supported validation command for dispatcher checks.

## Not allowed

It is forbidden to treat any of the following as dispatcher entrypoints:

- `main.py`
- `dispatcher/engine.py`
- `dispatcher/engine_v16.py`
- `engine/canonical_dispatcher.py`
- `tools/run_dispatcher_checks.py`

## Operational truth

All manual dispatcher interaction must go through:

`./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json <command>`

## Final statement

For `cashflow-mode`, there is:
- one control brain
- one state model
- one command surface

No alternatives.


