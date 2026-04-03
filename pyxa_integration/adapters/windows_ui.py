from __future__ import annotations

import importlib

from pyxa_integration.errors import AdapterUnavailableError, ToolExecutionError
from pyxa_integration.utils.telemetry import get_telemetry_recorder, now_ms


class WindowsUiAutomationAdapter:
    """Minimal UIA adapter for clicking controls by Name and typing text."""

    def _automation(self):
        return importlib.import_module("uiautomation")

    def click_by_name(self, label: str, timeout_s: float = 2.0) -> str:
        recorder = get_telemetry_recorder()
        start = now_ms()
        status = "ok"
        try:
            if not label:
                raise ToolExecutionError("Empty label is not valid for click_by_name")

            automation = self._automation()
            window = automation.GetForegroundControl()
            if window is None:
                raise AdapterUnavailableError("Could not access foreground window via UIAutomation")

            control = window.Control(Name=label, searchDepth=30)
            if not control.Exists(timeout_s):
                raise ToolExecutionError(f"Control '{label}' not found")

            control.Click()
            return f"clicked:{label}"
        except Exception:
            status = "error"
            raise
        finally:
            recorder.record("adapter.windows_ui.click", now_ms() - start, status, {"label": label})

    def type_text(self, text: str, press_enter: bool = False) -> str:
        """Type text into currently focused control using UIAutomation keyboard input."""

        recorder = get_telemetry_recorder()
        start = now_ms()
        status = "ok"
        try:
            if not text:
                raise ToolExecutionError("Empty text is not valid for type_text")

            automation = self._automation()
            focused = automation.GetFocusedControl()
            if focused is None:
                raise AdapterUnavailableError("No focused control available for typing")

            focused.SendKeys(text, waitTime=0.01)
            if press_enter:
                focused.SendKeys("{Enter}", waitTime=0.01)

            return f"typed:{text}"
        except Exception:
            status = "error"
            raise
        finally:
            recorder.record(
                "adapter.windows_ui.type",
                now_ms() - start,
                status,
                {"chars": len(text), "press_enter": press_enter},
            )
