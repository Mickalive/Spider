#!/usr/bin/env python3
"""Deterministic regression for the Spider vs. healthy Lex model-health failure."""
import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_free_provider import (PROBE_TOKEN, allowed_candidates, classify,
                                  clean_environment, query_catalog, run_probe)


def run():
    # Never mark printed text as proof that the tool-capable agent works.
    assert classify("SPIDER_FREE_TOOL_OK", 0) == "NO_TOOL_ATTESTATION"
    assert classify("printed " + PROBE_TOKEN + " in echo", 0) == "NO_TOOL_ATTESTATION"
    assert classify("\x1b[0m"+PROBE_TOKEN+"\x1b[0m\n", 0) == "NO_TOOL_ATTESTATION"
    assert classify("No stdout", 0, marker_ok=True) == "READY"
    assert classify("Model is unavailable\n", 1, marker_ok=True) == "SERVICE_UNAVAILABLE"
    assert classify("Error: Upstream request failed: Invalid credential", 1) == "AUTH_INVALID"
    assert classify("HTTP 401\nError 503", 1) == "AUTH_INVALID"
    assert classify("The user has specified a rule which prevents you from using this specific tool call.", 1) == "PERMISSION_DENIED"
    assert classify('{"name":"UnknownError","data":{"message":"Unexpected server error."}}',1) == "SERVICE_UNAVAILABLE"
    assert classify("", 124, timeout=True) == "TIMEOUT"

    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / "config/models.json").read_text())
    models = allowed_candidates(config, 3)
    all_free = allowed_candidates(config, 12)
    assert len(models) == 3
    assert len(all_free) == 12
    assert set(all_free) == set(config["free_only_allowed_models"])
    assert "opencode/mimo-v2.6-flash-free" in all_free
    assert "opencode/exo-free" in all_free
    for candidate in all_free:
        assert candidate.startswith("opencode/") and (
            candidate.endswith("-free") or candidate == "opencode/big-pickle"
        )
    try:
        allowed_candidates({**config, "free_only": False}, 3)
    except ValueError:
        pass
    else:
        raise AssertionError("refuse any paid routing")

    # Dynamic actual CLI catalogue: free model absent => skip instead of
    # spending a provider request against a stale hardcoded ID.
    from unittest.mock import Mock
    with patch("probe_free_provider.subprocess.run") as fake:
        fake.return_value = Mock(returncode=0, stdout="opencode/mimo-v2.6-flash-free\nopencode/nemotron-3-ultra-free\n")
        available, status = query_catalog("opencode")
        assert status == "OK"
        assert available == {"opencode/mimo-v2.6-flash-free", "opencode/nemotron-3-ultra-free"}
        assert fake.call_args.args[0] == ["opencode", "models", "opencode"]

    # The main Spider-specific bug: its earlier probe only asked an agent to
    # print a magic token, without tools. The repaired probe requires a real
    # side effect and never loads the 4,613-file scientific repo.
    with patch("probe_free_provider.subprocess.Popen", side_effect=FileNotFoundError):
        assert run_probe("not-installed", models[0], 5) == "BINARY_UNAVAILABLE"
    with patch("probe_free_provider.subprocess.Popen") as fake:
        proc = fake.return_value
        proc.communicate.return_value = (PROBE_TOKEN+"\n", "")
        proc.returncode = 0
        assert run_probe("fake-opencode", models[0], 5) == "NO_TOOL_ATTESTATION"
        args = fake.call_args.args[0]
        assert "--model" in args and args[args.index("--model")+1] in config["free_only_allowed_models"]
        assert args[args.index("--agent")+1] == "spider_provider_probe"
        assert fake.call_args.kwargs["cwd"] != root
        assert fake.call_args.kwargs["cwd"].name.startswith("spider-provider-")
        assert "OPENCODE_CONFIG_CONTENT" not in fake.call_args.kwargs["env"]

    # Simulated LLM used the bash tool and wrote the exact marker.
    def create_marker(*a, **kwargs):
        target = kwargs["cwd"] / "marker.txt"
        target.write_text(PROBE_TOKEN)
        p = Mock()
        p.returncode = 0
        p.communicate.return_value = ("Tool complete\n", "")
        return p
    with patch("probe_free_provider.subprocess.Popen", side_effect=create_marker):
        assert run_probe("fake-opencode", models[0], 5) == "READY"

    with patch.dict("os.environ", {"GH_TOKEN":"mock-private","OPENCODE_CONFIG_CONTENT":"override"},clear=False):
        assert "GH_TOKEN" not in clean_environment()
        assert "OPENCODE_CONFIG_CONTENT" not in clean_environment()

    runner = (root / ".github/scripts/run-opencode-resilient.sh").read_text()
    pulse = (root / ".github/workflows/factory-pulse.yml").read_text()
    assert "SPIDER_PROVIDER_AUTH_INVALID" in runner
    assert "SPIDER_PROVIDER_GATE_BLOCKED" in pulse
    assert "steps.provider.outputs.ready" in pulse
    assert "scripts/probe_free_provider.py" in pulse
    assert ".spider-runtime/provider_preflight.json" in pulse
    probe_src = (root / "scripts/probe_free_provider.py").read_text()
    assert "default=12" in probe_src
    assert "selected_model" in probe_src
    assert "query_catalog" in probe_src
    assert "tempfile.TemporaryDirectory" in probe_src
    assert "marker.read_bytes()" in probe_src
    probe_agent = (root / ".opencode/agents/spider_provider_probe.md").read_text()
    assert "bash: allow" in probe_agent and "edit: deny" in probe_agent
    assert "mode: primary" in probe_agent
    print("SPIDER_FREE_PROVIDER_REAL_TOOL_PROBE_OK")


if __name__ == "__main__":
    run()
