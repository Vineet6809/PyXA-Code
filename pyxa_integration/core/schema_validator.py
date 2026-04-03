from __future__ import annotations

from typing import Any, Dict, List

from pyxa_integration.errors import PlannerOutputError


def build_schema_map(tool_schema: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    schema_map: Dict[str, Dict[str, Any]] = {}
    for entry in tool_schema:
        name = entry.get("name")
        if isinstance(name, str) and name:
            schema_map[name] = entry
    return schema_map


def validate_tool_call_against_schema(name: str, arguments: Dict[str, Any], schema_map: Dict[str, Dict[str, Any]]) -> None:
    if name not in schema_map:
        raise PlannerOutputError(f"Tool '{name}' is not in allowed tool schema")

    input_schema = schema_map[name].get("input_schema", {})
    required = input_schema.get("required", [])
    properties = input_schema.get("properties", {})

    for required_key in required:
        if required_key not in arguments:
            raise PlannerOutputError(f"Tool '{name}' is missing required argument '{required_key}'")

    for key, value in arguments.items():
        prop = properties.get(key)
        if prop is None:
            continue
        expected = prop.get("type")
        if expected == "string" and not isinstance(value, str):
            raise PlannerOutputError(f"Tool '{name}' argument '{key}' must be string")
        if expected == "boolean" and not isinstance(value, bool):
            raise PlannerOutputError(f"Tool '{name}' argument '{key}' must be boolean")
        if expected == "integer" and not isinstance(value, int):
            raise PlannerOutputError(f"Tool '{name}' argument '{key}' must be integer")
