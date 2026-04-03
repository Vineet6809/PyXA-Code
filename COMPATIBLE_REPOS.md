# Compatible Repositories for Your System (Windows 11, i5-1235U, 16GB RAM)

This list focuses on compact, practical integrations that match your personal hardware constraints.

## Recommended first-wave integrations

| Repo | Category | Why useful now | Fit for your system |
|---|---|---|---|
| https://github.com/yinkaisheng/Python-UIAutomation-for-Windows | Windows actuation | Reliable UI element targeting without fragile pixel clicking. | Excellent |
| https://github.com/BoboTiG/python-mss | Screen capture | Very fast screen grabbing for verify-after-action loops. | Excellent |
| https://github.com/SYSTRAN/faster-whisper | Speech-to-text | Efficient CPU inference via CTranslate2. | Strong (with int8/small models) |
| https://github.com/KoljaB/RealtimeSTT | Speech pipeline | Streaming STT pipeline with VAD behavior. | Strong (careful tuning) |
| https://github.com/abetlen/llama-cpp-python | Local LLM runtime | Quantized local models for low-RAM operation. | Strong (small models) |
| https://github.com/lancedb/lancedb | Vector memory | Embedded memory store, no heavy service overhead. | Strong |
| https://github.com/openai/openai-python | Cloud LLM client | Offloads heavy reasoning to cloud when local models are slow. | Excellent |

## Claw-code status

- Repo: https://github.com/ultraworkers/claw-code
- Recommended usage in this project: **CLI-level bridge first**, architecture reference second.
- Keep legal/licensing review in the loop before deep coupling.

## Integration order for your machine

1. UI automation + screen verification loop.
2. STT pipeline (faster-whisper / RealtimeSTT).
3. Cloud Codex fallback (OpenAI SDK).
4. Optional local LLM via llama.cpp.
5. Long-term memory via LanceDB.
6. Experimental claw-code bridge.
