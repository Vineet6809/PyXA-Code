import pytest

from pyxa_integration.config import windows_i5_1235u_profile
from pyxa_integration.core.structured_planner import StructuredPlanner, parse_structured_plan
from pyxa_integration.errors import PlannerOutputError
from pyxa_integration.utils.retry import with_retries


def test_parse_structured_plan_valid_json():
    turn = parse_structured_plan(
        raw='{"tool_calls": [{"name": "click_text", "arguments": {"label": "OK"}}]}',
        prompt="click ok",
    )
    assert turn.tool_calls[0].name == "click_text"


def test_parse_structured_plan_invalid_json_raises():
    with pytest.raises(PlannerOutputError):
        parse_structured_plan(raw="not-json", prompt="x")


def test_structured_planner_retries_then_succeeds():
    calls = {"n": 0}

    def model_complete(_: str) -> str:
        calls["n"] += 1
        if calls["n"] == 1:
            return "bad-json"
        return '{"tool_calls": [{"name": "read_screen", "arguments": {}}]}'

    planner = StructuredPlanner(model_complete=model_complete, retries=1)
    turn = planner.plan("hello")
    assert turn.tool_calls[0].name == "read_screen"


def test_retry_utility():
    calls = {"n": 0}

    def flaky() -> int:
        calls["n"] += 1
        if calls["n"] < 2:
            raise ValueError("retry")
        return 42

    assert with_retries(flaky, retries=2, base_delay_s=0) == 42


def test_parse_structured_plan_schema_validation():
    from pyxa_integration.planning.tool_schema import default_tool_schema
    from pyxa_integration.core.schema_validator import build_schema_map

    schema_map = build_schema_map(default_tool_schema())
    with pytest.raises(PlannerOutputError):
        parse_structured_plan(
            raw='{"tool_calls": [{"name": "click_text", "arguments": {}}]}',
            prompt="click",
            schema_map=schema_map,
        )


def test_windows_profile_values():
    profile = windows_i5_1235u_profile()
    assert profile.ram_gb == 16
    assert profile.os_name == "Windows 11"
