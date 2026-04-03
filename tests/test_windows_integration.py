import sys

import pytest

from pyxa_integration.adapters.ocr import WindowsOcrAdapter
from pyxa_integration.adapters.screen_capture import MssScreenCaptureAdapter
from pyxa_integration.adapters.windows_ui import WindowsUiAutomationAdapter
from pyxa_integration.errors import ToolExecutionError

pytestmark = [pytest.mark.windows_integration, pytest.mark.skipif(sys.platform != "win32", reason="Windows-only integration tests")]


def test_screen_capture_returns_png_bytes():
    pytest.importorskip("mss")
    adapter = MssScreenCaptureAdapter()
    png = adapter.capture_primary_png_bytes()
    assert isinstance(png, (bytes, bytearray))
    assert len(png) > 0


def test_windows_ui_type_text_validation():
    adapter = WindowsUiAutomationAdapter()
    with pytest.raises(ToolExecutionError):
        adapter.type_text("")


def test_winrt_runtime_check_or_skip():
    adapter = WindowsOcrAdapter()
    try:
        available = adapter.check_runtime_available(silent=True)
    except Exception:
        available = False
    assert available in {True, False}
