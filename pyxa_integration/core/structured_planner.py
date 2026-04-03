from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

from pyxa_integration.errors import PlannerOutputError
from pyxa_integration.utils.retry import with_retries

from .models import AgentTurn, ToolCall
from .schema_validator import build_schema_map, validate_tool_call_against_schema


@dataclass
class StructuredPlanner:
    """Parse strict JSON planner outputs into ToolCall structures."""

    model_complete: Callable[[str], str]
    retries: int = 2
    tool_schema: List[Dict[str, Any]] = field(default_factory=list)

    def plan(self, prompt: str) -> AgentTurn:
        schema_map = build_schema_map(self.tool_schema) if self.tool_schema else None

        def _single_attempt() -> AgentTurn:
            raw = self.model_complete(prompt)
            return parse_structured_plan(raw=raw, prompt=prompt, schema_map=schema_map)

        return with_retries(_single_attempt, retries=self.retries)


def parse_structured_plan(raw: str, prompt: str, schema_map: Dict[str, Dict[str, Any]] | None = None) -> AgentTurn:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PlannerOutputError(f"Planner output is not valid JSON: {exc}") from exc

    calls = payload.get("tool_calls")
    if not isinstance(calls, list):
        raise PlannerOutputError("Planner output must contain a list field: tool_calls")

    tool_calls: list[ToolCall] = []
    for item in calls:
        if not isinstance(item, dict):
            raise PlannerOutputError("Each tool call entry must be an object")

        name = item.get("name")
        args = item.get("arguments", {})
        if not isinstance(name, str) or not name:
            raise PlannerOutputError("Tool call name must be a non-empty string")
        if not isinstance(args, dict):
            raise PlannerOutputError("Tool call arguments must be an object")

        if schema_map is not None:
            validate_tool_call_against_schema(name=name, arguments=args, schema_map=schema_map)

        tool_calls.append(ToolCall(name=name, arguments=args))

    return AgentTurn(user_prompt=prompt, tool_calls=tool_calls)
