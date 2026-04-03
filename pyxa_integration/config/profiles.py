from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeProfile:
    name: str
    os_name: str
    cpu: str
    ram_gb: int
    preferred_llm: str
    stt_model: str
    ocr_mode: str
    capture_fps_target: int


def windows_i5_1235u_profile() -> RuntimeProfile:
    return RuntimeProfile(
        name="windows_i5_1235u_16gb",
        os_name="Windows 11",
        cpu="Intel Core i5-1235U",
        ram_gb=16,
        preferred_llm="gpt-5.3-codex",
        stt_model="faster-whisper int8",
        ocr_mode="windows_media_ocr",
        capture_fps_target=5,
    )
