from pyxa_integration.core.agent import AgentRuntime, RulePlanner
from pyxa_integration.core.tools import builtin_tool_registry


def test_runtime_executes_default_read_screen():
    runtime = AgentRuntime(planner=RulePlanner(), tools=builtin_tool_registry())
    result = runtime.run_turn("hello")
    assert result.results[0].name == "read_screen"
    assert result.results[0].ok


def test_runtime_executes_click_and_type():
    runtime = AgentRuntime(planner=RulePlanner(), tools=builtin_tool_registry())
    result = runtime.run_turn("please click and type")
    names = [r.name for r in result.results]
    assert "click_text" in names
    assert "type_text" in names
