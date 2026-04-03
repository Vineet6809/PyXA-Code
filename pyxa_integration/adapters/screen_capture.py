from __future__ import annotations

import importlib

from pyxa_integration.errors import AdapterUnavailableError
from pyxa_integration.utils.telemetry import get_telemetry_recorder, now_ms


class MssScreenCaptureAdapter:
    """Capture primary monitor frames with mss."""

    def capture_primary_png_bytes(self) -> bytes:
        recorder = get_telemetry_recorder()
        start = now_ms()
        status = "ok"
        try:
            mss_module = importlib.import_module("mss")
            tools = importlib.import_module("mss.tools")

            with mss_module.mss() as sct:
                if not sct.monitors:
                    raise AdapterUnavailableError("No monitors found for screen capture")
                monitor = sct.monitors[1]
                shot = sct.grab(monitor)
                png = tools.to_png(shot.rgb, shot.size)
                return png
        except Exception:
            status = "error"
            raise
        finally:
            recorder.record("adapter.screen_capture", now_ms() - start, status)
