from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolResult:
    name: str
    ok: bool
    output: str


@dataclass(frozen=True)
class AgentTurn:
    user_prompt: str
    tool_calls: List[ToolCall]


@dataclass(frozen=True)
class TurnExecution:
    turn: AgentTurn
    results: List[ToolResult]
    summary: str
