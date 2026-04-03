from __future__ import annotations

from typing import Any, Dict, List


def default_tool_schema() -> List[Dict[str, Any]]:
    """Tool schema designed for local function-calling LLMs."""

    return [
        {
            "name": "read_screen",
            "description": "Return current OCR text and visible UI regions.",
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "click_text",
            "description": "Click a visible UI element by text label.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "label": {"type": "string", "description": "Visible text to click."},
                    "retry": {"type": "integer", "minimum": 0, "maximum": 3},
                },
                "required": ["label"],
            },
        },
        {
            "name": "type_text",
            "description": "Type text into the currently focused field.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "press_enter": {"type": "boolean", "default": False},
                },
                "required": ["text"],
            },
        },
    ]
