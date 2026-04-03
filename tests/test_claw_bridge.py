from pyxa_integration.integrations.claw_bridge import ClawBridgeConfig, ClawCodeCliBridge


def test_cli_bridge_with_python_echo():
    bridge = ClawCodeCliBridge(
        ClawBridgeConfig(
            executable="python",
            base_args=("-c", "import sys; data=sys.stdin.read(); print(data)"),
            timeout_s=5,
        )
    )

    result = bridge.submit("hello")
    assert result.ok
    assert '"prompt": "hello"' in result.stdout
