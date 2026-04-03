from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class HardwareProfile:
    """Target hardware envelope for the MVP."""

    cpu: str
    ram_gb: int
    os: str
    notes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class SoftwareRequirements:
    """Pinned capabilities and package-level requirements for Windows MVP."""

    python_min_version: str
    core_packages: List[str]
    optional_packages: Dict[str, List[str]]
    model_recommendations: Dict[str, str]


def default_windows_mvp_requirements() -> tuple[HardwareProfile, SoftwareRequirements]:
    """Return a conservative requirements profile derived from the research notes."""

    hardware = HardwareProfile(
        cpu="Intel Core i5-1235U (2P+8E)",
        ram_gb=16,
        os="Windows 11",
        notes=[
            "Assume ~8GB effective free RAM after OS and UI overhead.",
            "Prioritize CPU-efficient and memory-light models for steady latency.",
            "Use reflex/fast perception (native OCR) for action verification loops.",
        ],
    )

    software = SoftwareRequirements(
        python_min_version="3.10",
        core_packages=[
            "pynput>=1.7.7",
            "mss>=9.0.1",
            "imagehash>=4.3.1",
            "Pillow>=10.4.0",
            "uiautomation>=2.0.20",
            "llama-cpp-python>=0.2.90",
            "lancedb>=0.18.0",
            "openai>=1.50.0",
        ],
        optional_packages={
            "speech": [
                "RealtimeSTT>=0.3.100",
                "faster-whisper>=1.1.0",
                "kokoro>=0.9.0",
            ],
            "windows_ocr": [
                "winrt-Windows.Media.Ocr>=3.2.1",
            ],
            "document_vision": [
                "deepseek-ocr2 (model artifact; loaded on demand)",
            ],
        },
        model_recommendations={
            "local_reasoning": "Qwen 2.5 3B Instruct (GGUF Q4_K_M)",
            "fast_ocr": "Windows.Media.Ocr",
            "deep_ocr": "DeepSeek-OCR2 (deferred/explicit use)",
            "tts": "Kokoro ONNX",
            "stt": "Faster-Whisper int8 via RealtimeSTT",
        },
    )

    return hardware, software
