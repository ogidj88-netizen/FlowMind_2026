# DISPATCHER ENTRYPOINT

Status: LOCKED  
Branch: `cashflow-mode`

## Canonical rule

У поточній гілці `cashflow-mode` canonical dispatcher **не інтегрований у `fm.py`**, тому що `fm.py` у корені репозиторію відсутній.

Canonical dispatcher entrypoints:

- `engine/canonical_dispatcher.py` — core logic
- `tools/dispatcher_cli.py` — canonical CLI entrypoint
- `tools/dispatcher.sh` — short local runner
- `tools/run_dispatcher_checks.py` — consolidated validation
- `tools/check_dispatcher.sh` — one-command local dispatcher check

## Operational rule

До окремого audit + migration decision заборонено:

- інтегрувати dispatcher у старі dispatcher-шари
- підключати dispatcher до `cashflow/dispatcher`
- підключати dispatcher до `./dispatcher`
- створювати новий альтернативний entrypoint
- називати будь-який інший launcher “canonical dispatcher”

## Current command set

### Show state
```bash
./tools/dispatcher.sh --state /path/to/PROJECT_STATE.json show
