# PyXA Integration Utilities

This repository is a runnable **v1 completion sprint** foundation for a personal-use PyXA-style desktop operator stack on constrained hardware.

## What is included

- Requirements/profile support for i5-1235U + 16GB RAM + Windows 11.
- Safety primitives: cooperative controller + kill switch abstraction.
- Perception helpers: dHash-based screen delta checks.
- Structured planning: strict JSON tool-call parsing.
- Core runtime: deterministic planner + tool registry + turn execution engine.
- Real adapter paths: `mss` capture, `uiautomation` click+type path, WinRT OCR path with fallback.
- Integration bridge: subprocess-based `claw-code` CLI adapter with retry/logging.
- Provider wrapper: OpenAI Codex client wrapper with retry/logging.
- Curated compatible-repo recommendations for your system.
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
python -m pyxa_integration.cli "click and type"
```

## Modules

- `pyxa_integration.core`: runtime loop, planners, tool registry, execution models.
- `pyxa_integration.adapters`: real adapter classes for capture/UIA/OCR paths.
- `pyxa_integration.controller`: execution loop + kill-switch components.
- `pyxa_integration.perception`: fast change detection helpers.
- `pyxa_integration.planning`: default JSON tool schema for LLM tool calling.
- `pyxa_integration.integrations`: claw-code CLI bridge.
- `pyxa_integration.providers`: OpenAI Codex provider wrapper.
- `pyxa_integration.config`: machine-targeted runtime profiles.
- `pyxa_integration.research`: curated compatible repository metadata.

## Docs

- `SYSTEM_REQUIREMENTS.md`: practical system requirement baseline.
- `COMPATIBLE_REPOS.md`: useful/compatible GitHub repos and adoption order.
- `INTEGRATION_PYXA_CLAWCODE.md`: detailed integration strategy and risk guidance.
- `docs/WINDOWS_CI.md`: setup and CI guidance for Windows integration test runs.


## Testing notes

- Standard test run: `python -m pytest -q`
- Windows-only integration tests are marked with `windows_integration`.
```

## Included modules

- `pyxa_integration.requirements`: structured hardware/software requirements.
- `pyxa_integration.controller`: execution loop + kill-switch components.
- `pyxa_integration.perception`: fast change detection helpers.
- `pyxa_integration.planning`: default JSON tool schema for LLM tool calling.
