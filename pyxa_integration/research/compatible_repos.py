from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RepoCandidate:
    name: str
    url: str
    category: str
    why_useful: str
    system_fit_note: str


def curated_repo_candidates() -> List[RepoCandidate]:
    """Curated repos aligned with the current PyXA MVP architecture."""

    return [
        RepoCandidate(
            name="ultraworkers/claw-code",
            url="https://github.com/ultraworkers/claw-code",
            category="agent-harness",
            why_useful="Agent loop + tool orchestration reference for code-first workflows.",
            system_fit_note="Use as architecture reference; avoid direct coupling until license is explicit.",
        ),
        RepoCandidate(
            name="abetlen/llama-cpp-python",
            url="https://github.com/abetlen/llama-cpp-python",
            category="local-llm-runtime",
            why_useful="Python bindings for llama.cpp; supports quantized local models.",
            system_fit_note="Strong fit for 16GB RAM systems with small quantized models.",
        ),
        RepoCandidate(
            name="SYSTRAN/faster-whisper",
            url="https://github.com/SYSTRAN/faster-whisper",
            category="speech-to-text",
            why_useful="Fast Whisper inference on CPU/GPU via CTranslate2.",
            system_fit_note="Good fit for command-style STT with int8 models on i5-class CPUs.",
        ),
        RepoCandidate(
            name="KoljaB/RealtimeSTT",
            url="https://github.com/KoljaB/RealtimeSTT",
            category="speech-pipeline",
            why_useful="Realtime wrapper around STT with VAD and streaming behavior.",
            system_fit_note="Useful for low-latency voice loop if tuned for CPU budget.",
        ),
        RepoCandidate(
            name="yinkaisheng/Python-UIAutomation-for-Windows",
            url="https://github.com/yinkaisheng/Python-UIAutomation-for-Windows",
            category="windows-actuation",
            why_useful="Direct Windows UI Automation access; robust element discovery.",
            system_fit_note="Primary fit for your Windows desktop action layer.",
        ),
        RepoCandidate(
            name="BoboTiG/python-mss",
            url="https://github.com/BoboTiG/python-mss",
            category="screen-capture",
            why_useful="Fast screenshot capture for verification loops.",
            system_fit_note="Lightweight and suitable for frequent capture/delta checks.",
        ),
        RepoCandidate(
            name="lancedb/lancedb",
            url="https://github.com/lancedb/lancedb",
            category="memory-vector-db",
            why_useful="Embedded vector storage for local long-term memory.",
            system_fit_note="Good desktop fit due to embedded architecture.",
        ),
        RepoCandidate(
            name="openai/openai-python",
            url="https://github.com/openai/openai-python",
            category="cloud-llm-client",
            why_useful="Official OpenAI Python SDK for Codex API integration.",
            system_fit_note="Cloud offload reduces local compute pressure on i5 hardware.",
        ),
    ]


def recommend_for_windows_i5_16gb() -> List[RepoCandidate]:
    candidates = curated_repo_candidates()
    preferred_categories = {
        "windows-actuation",
        "screen-capture",
        "speech-to-text",
        "speech-pipeline",
        "local-llm-runtime",
        "memory-vector-db",
        "cloud-llm-client",
    }
    return [repo for repo in candidates if repo.category in preferred_categories]
