# PyXA Integration Utilities

This repository now includes a practical starter kit based on the Pyxa-v1-0 research notes:

- System/hardware requirement profile for the Windows MVP.
- Safety-first execution controller with cooperative stop.
- Global kill-switch helper abstraction.
- Perception delta utilities (dHash + change threshold).
- Initial tool-calling schema for desktop action planning.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-mvp.txt
```

## Included modules

- `pyxa_integration.requirements`: structured hardware/software requirements.
- `pyxa_integration.controller`: execution loop + kill-switch components.
- `pyxa_integration.perception`: fast change detection helpers.
- `pyxa_integration.planning`: default JSON tool schema for LLM tool calling.
