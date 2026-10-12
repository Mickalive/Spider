#!/usr/bin/env python3
"""Deterministic unit tests for FREE provider preflight. NO model requests."""
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_free_provider import PROBE_TOKEN, allowed_candidates, classify, run_probe

def run():
    assert classify("Error: Upstream request failed: Invalid credential", 1) == "AUTH_INVALID"
    assert classify("HTTP 401\nError 503", 1) == "AUTH_INVALID"
    assert classify("The user has specified a rule which prevents you from using this specific tool call.", 1) == "PERMISSION_DENIED"
    assert classify("Upstream request failed: Model is unavailable", 1) == "SERVICE_UNAVAILABLE"
    assert classify('{"name": "UnknownError", "data": {"message": "Unexpected server error."}}', 1) == "SERVICE_UNAVAILABLE"
    assert classify("   " + PROBE_TOKEN + "\n", 0) == "READY"
    assert classify("printed " + PROBE_TOKEN + " in echo\n", 0) == "NO_ATTESTED_OUTPUT"
    assert classify("Model is unavailable\n"+PROBE_TOKEN, 1) == "SERVICE_UNAVAILABLE"
    assert classify("", 124, timeout=True) == "TIMEOUT"
    repo = Path(__file__).resolve().parents[1]
    config = json.loads((repo / "config/models.json").read_text())
    models = allowed_candidates(config, 3)
    assert len(models) == 3 and all(m in config["free_only_allowed_models"] for m in models)
    try:
        allowed_candidates({**config, "free_only": False}, 3)
    except ValueError:
        pass
    else:
        raise AssertionError("must reject paid routing")
    with patch("probe_free_provider.subprocess.Popen") as fake:
        proc = fake.return_value
        proc.communicate.return_value = (PROBE_TOKEN+"\n", "")
        proc.returncode = 0
        assert run_probe("fake-opencode", models[0], 5) == "READY"
        args = fake.call_args.args[0]
        assert "--model" in args and args[args.index("--model")+1] in config["free_only_allowed_models"]
        assert args[args.index("--agent")+1] == "spider_provider_probe"
    runner = (repo / ".github/scripts/run-opencode-resilient.sh").read_text()
    pulse = (repo / ".github/workflows/factory-pulse.yml").read_text()
    assert "SPIDER_PROVIDER_AUTH_INVALID" in runner and "provider-auth-invalid" in runner
    assert "SPIDER_PROVIDER_GATE_BLOCKED" in pulse
    assert "steps.provider.outputs.ready" in pulse
    assert "scripts/probe_free_provider.py" in pulse
    assert ".spider-runtime/provider_preflight.json" in pulse
    probe_agent = (repo / ".opencode/agents/spider_provider_probe.md").read_text()
    assert "bash: deny" in probe_agent and "edit: deny" in probe_agent
    print("SPIDER_FREE_PROVIDER_PREFLIGHT_TEST_OK")

if __name__ == "__main__":
    run()
