from pyxa_integration.core.agent import AgentRuntime, RulePlanner
from pyxa_integration.core.tools import builtin_tool_registry
from pyxa_integration.utils.telemetry import get_telemetry_recorder


def test_runtime_records_telemetry_events():
    recorder = get_telemetry_recorder()
    baseline = len(recorder.events)

    runtime = AgentRuntime(planner=RulePlanner(), tools=builtin_tool_registry())
    runtime.run_turn("click and type")

    assert len(recorder.events) > baseline
    assert any(event.action == "runtime.turn" for event in recorder.events[baseline:])
