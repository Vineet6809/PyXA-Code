from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass
class ControllerConfig:
    poll_interval_s: float = 0.05


class ExecutionController:
    """Safety-first execution loop with cooperative stop semantics."""

    def __init__(self, config: ControllerConfig | None = None) -> None:
        self.config = config or ControllerConfig()
        self.stop_event = threading.Event()
        self._lock = threading.Lock()
        self._active_step = "idle"

    @property
    def active_step(self) -> str:
        with self._lock:
            return self._active_step

    def request_stop(self) -> None:
        self.stop_event.set()

    def run_plan(self, steps: Iterable[Callable[[], None]]) -> None:
        for idx, step in enumerate(steps, start=1):
            if self.stop_event.is_set():
                break

            with self._lock:
                self._active_step = f"step_{idx}:{getattr(step, '__name__', 'anonymous')}"

            step()
            time.sleep(self.config.poll_interval_s)

        with self._lock:
            self._active_step = "stopped" if self.stop_event.is_set() else "completed"
