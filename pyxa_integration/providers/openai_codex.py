from __future__ import annotations

import importlib
import os
from dataclasses import dataclass

from pyxa_integration.utils.logging import get_logger
from pyxa_integration.utils.retry import with_retries
from pyxa_integration.utils.telemetry import get_telemetry_recorder, now_ms


@dataclass(frozen=True)
class CodexConfig:
    model: str = "gpt-5.3-codex"
    temperature: float = 0.2
    retries: int = 2


class OpenAICodexClient:
    """Small wrapper around the official OpenAI Python SDK."""

    def __init__(self, config: CodexConfig | None = None) -> None:
        self.config = config or CodexConfig()
        self.logger = get_logger("pyxa_integration.openai_codex")
        openai_module = importlib.import_module("openai")
        self._client = openai_module.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def complete(self, prompt: str) -> str:
        recorder = get_telemetry_recorder()

        def _call() -> str:
            start = now_ms()
            status = "ok"
            usage_payload = {}
            self.logger.info("codex.complete model=%s", self.config.model)
            try:
                response = self._client.responses.create(
                    model=self.config.model,
                    input=prompt,
                    temperature=self.config.temperature,
                )
                usage = getattr(response, "usage", None)
                if usage is not None:
                    usage_payload = {
                        "input_tokens": getattr(usage, "input_tokens", None),
                        "output_tokens": getattr(usage, "output_tokens", None),
                        "total_tokens": getattr(usage, "total_tokens", None),
                    }
                return response.output_text
            except Exception:
                status = "error"
                raise
            finally:
                recorder.record(
                    "provider.openai.complete",
                    now_ms() - start,
                    status,
                    {"model": self.config.model, **usage_payload},
                )

        return with_retries(_call, retries=self.config.retries)
