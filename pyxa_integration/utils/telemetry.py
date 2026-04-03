from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from .logging import get_logger


@dataclass
class TelemetryEvent:
    action: str
    latency_ms: float
    status: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp_unix_ms: int = 0


class TelemetryRecorder:
    def __init__(self) -> None:
        self.logger = get_logger("pyxa_integration.telemetry")
        self.events: List[TelemetryEvent] = []

    def record(self, action: str, latency_ms: float, status: str, metadata: Dict[str, Any] | None = None) -> None:
        event = TelemetryEvent(
            action=action,
            latency_ms=latency_ms,
            status=status,
            metadata=metadata or {},
            timestamp_unix_ms=int(time.time() * 1000),
        )
        self.events.append(event)
        self.logger.info("telemetry %s", json.dumps(asdict(event), sort_keys=True))


_GLOBAL_RECORDER = TelemetryRecorder()


def get_telemetry_recorder() -> TelemetryRecorder:
    return _GLOBAL_RECORDER


def now_ms() -> float:
    return time.perf_counter() * 1000.0
