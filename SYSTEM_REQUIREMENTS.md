# PyXA-Inspired MVP System Requirements

This baseline is extracted from the `Pyxa-v1-0/research` recommendations and normalized into actionable requirements.

## Target Hardware (Windows MVP)

- **CPU:** Intel Core i5-1235U class (hybrid 2P + 8E)
- **RAM:** 16 GB minimum
- **OS:** Windows 11
- **Storage:** SSD strongly recommended (model load/unload behavior)

## Runtime Requirements

- Python **3.10+**
- Pip/venv workflow
- Windows accessibility permissions for desktop automation tools

## Core Packages

- `pynput` (global kill-switch)
- `mss` + `Pillow` + `imagehash` (fast capture + delta detection)
- `uiautomation` (primary Windows UI automation driver)
- `llama-cpp-python` (local inference runtime)
- `lancedb` (embedded memory store)
- `openai` (cloud fallback/codex integration)

## Optional Capability Packs

### Speech
- `RealtimeSTT`
- `faster-whisper`
- `kokoro`

### Windows OCR
- `winrt-Windows.Media.Ocr`

### Deep document OCR
- DeepSeek-OCR2 model artifacts (load on demand only)

## Operational Constraints

- Treat available agent memory budget as ~8 GB effective on a 16 GB machine.
- Prefer lightweight "reflex" loops for high-frequency verification.
- Load heavy analysis models only for explicit user requests.
- Provide a hard stop/kill switch at all times.
