from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Sequence

from pyxa_integration.utils.logging import get_logger
from pyxa_integration.utils.retry import with_retries
from pyxa_integration.utils.telemetry import get_telemetry_recorder, now_ms


@dataclass(frozen=True)
class ClawBridgeConfig:
    executable: str = "claw-code"
    base_args: Sequence[str] = ()
    timeout_s: int = 120
    retries: int = 1


@dataclass(frozen=True)
class ClawBridgeResult:
    ok: bool
    stdout: str
    stderr: str
    return_code: int


class ClawCodeCliBridge:
    """Thin CLI bridge to a local claw-code executable.

    This keeps integration low-risk: PyXA can invoke claw-code as a subprocess
    without importing or copying any project internals.
    """

    def __init__(self, config: ClawBridgeConfig | None = None) -> None:
        self.config = config or ClawBridgeConfig()
        self.logger = get_logger("pyxa_integration.claw_bridge")

    def submit(self, prompt: str) -> ClawBridgeResult:
        recorder = get_telemetry_recorder()
        payload = json.dumps({"prompt": prompt})
        command = [self.config.executable, *self.config.base_args]

        def _run_once() -> ClawBridgeResult:
            start = now_ms()
            status = "ok"
            self.logger.info("claw_bridge.invoke executable=%s", self.config.executable)
            try:
                completed = subprocess.run(
                    command,
                    input=payload,
                    text=True,
                    capture_output=True,
                    timeout=self.config.timeout_s,
                    check=False,
                )
                result = ClawBridgeResult(
                    ok=completed.returncode == 0,
                    stdout=completed.stdout,
                    stderr=completed.stderr,
                    return_code=completed.returncode,
                )
                if not result.ok:
                    status = "error"
                return result
            except Exception:
                status = "error"
                raise
            finally:
                recorder.record(
                    "integration.claw_bridge.submit",
                    now_ms() - start,
                    status,
                    {"return_code": locals().get("completed").returncode if "completed" in locals() else None},
                )

        return with_retries(_run_once, retries=self.config.retries)
