from __future__ import annotations

import argparse
import json

from .core.agent import AgentRuntime, RulePlanner
from .core.tools import builtin_tool_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PyXA Integration CLI")
    parser.add_argument("prompt", help="User prompt to process")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    runtime = AgentRuntime(planner=RulePlanner(), tools=builtin_tool_registry())
    execution = runtime.run_turn(args.prompt)

    print(
        json.dumps(
            {
                "summary": execution.summary,
                "tool_results": [r.__dict__ for r in execution.results],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
