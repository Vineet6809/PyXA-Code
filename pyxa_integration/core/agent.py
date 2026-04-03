from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from pyxa_integration.errors import ToolExecutionError
from pyxa_integration.utils.logging import get_logger
from pyxa_integration.utils.telemetry import get_telemetry_recorder, now_ms

from .models import AgentTurn, ToolCall, TurnExecution
from .tools import ToolRegistry


class Planner(Protocol):
    def plan(self, prompt: str) -> AgentTurn:
        ...


@dataclass
class RulePlanner:
    """Simple deterministic planner for local/offline execution."""

    def plan(self, prompt: str) -> AgentTurn:
        calls: list[ToolCall] = [ToolCall(name="read_screen", arguments={})]
        if "click" in prompt.lower():
            calls.append(ToolCall(name="click_text", arguments={"label": "OK"}))
        if "type" in prompt.lower():
            calls.append(ToolCall(name="type_text", arguments={"text": "hello"}))
        return AgentTurn(user_prompt=prompt, tool_calls=calls)


@dataclass
class AgentRuntime:
    planner: Planner
    tools: ToolRegistry

    def run_turn(self, prompt: str) -> TurnExecution:
        logger = get_logger("pyxa_integration.runtime")
        recorder = get_telemetry_recorder()
        turn_start = now_ms()
        logger.info("run_turn.start")

        turn = self.planner.plan(prompt)
        results = []

        for call in turn.tool_calls:
            tool_start = now_ms()
            status = "ok"
            try:
                result = self.tools.execute(call)
                results.append(result)
                logger.info("tool.executed name=%s ok=%s", result.name, result.ok)
                if not result.ok:
                    status = "error"
            except Exception as exc:
                status = "error"
                logger.exception("tool.execution_failed name=%s", call.name)
                raise ToolExecutionError(f"Tool execution failed for {call.name}: {exc}") from exc
            finally:
                recorder.record(
                    "runtime.tool_execute",
                    now_ms() - tool_start,
                    status,
                    {"tool": call.name},
                )

        summary = "; ".join(f"{r.name}={'ok' if r.ok else 'err'}" for r in results)
        recorder.record(
            "runtime.turn",
            now_ms() - turn_start,
            "ok",
            {"tool_calls": len(turn.tool_calls)},
        )
        logger.info("run_turn.done")
        return TurnExecution(turn=turn, results=results, summary=summary)
