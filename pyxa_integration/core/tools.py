from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from pyxa_integration.adapters import MssScreenCaptureAdapter, WindowsOcrAdapter, WindowsUiAutomationAdapter
from .models import ToolCall, ToolResult

ToolFn = Callable[[dict], str]


@dataclass
class ToolRegistry:
    _tools: Dict[str, ToolFn]

    def __init__(self) -> None:
        self._tools = {}

    def register(self, name: str, func: ToolFn) -> None:
        self._tools[name] = func

    def execute(self, call: ToolCall) -> ToolResult:
        if call.name not in self._tools:
            return ToolResult(name=call.name, ok=False, output="Unknown tool")

        output = self._tools[call.name](call.arguments)
        return ToolResult(name=call.name, ok=True, output=output)


def builtin_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    def read_screen(_: dict) -> str:
        return "screen_text: <placeholder>"

    def click_text(args: dict) -> str:
        label = args.get("label", "")
        return f"clicked:{label}"

    def type_text(args: dict) -> str:
        text = args.get("text", "")
        return f"typed:{text}"

    registry.register("read_screen", read_screen)
    registry.register("click_text", click_text)
    registry.register("type_text", type_text)
    return registry


def windows_tool_registry() -> ToolRegistry:
    """Adapter-backed tools for Windows hosts.

    Falls back to explicit errors if required adapters are unavailable.
    """

    registry = ToolRegistry()
    capture = MssScreenCaptureAdapter()
    ocr = WindowsOcrAdapter()
    ui = WindowsUiAutomationAdapter()

    def read_screen(_: dict) -> str:
        png = capture.capture_primary_png_bytes()
        text = ocr.recognize_png_bytes(png, allow_fallback=True)
        return text

    def click_text(args: dict) -> str:
        label = args.get("label", "")
        return ui.click_by_name(label)

    def type_text(args: dict) -> str:
        text = args.get("text", "")
        press_enter = bool(args.get("press_enter", False))
        return ui.type_text(text=text, press_enter=press_enter)

    registry.register("read_screen", read_screen)
    registry.register("click_text", click_text)
    registry.register("type_text", type_text)
    return registry
