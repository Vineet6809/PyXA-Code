import json
import subprocess


def test_cli_outputs_json():
    completed = subprocess.run(
        ["python", "-m", "pyxa_integration.cli", "click and type"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0
    payload = json.loads(completed.stdout)
    assert "summary" in payload
    assert len(payload["tool_results"]) >= 1
