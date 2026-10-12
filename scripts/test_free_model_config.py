#!/usr/bin/env python3
"""Static no-paid-model regressions; actual provider uptime is independently external."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
config = json.loads((root / "config/models.json").read_text(encoding="utf-8"))
shell = (root / ".github/scripts/run-opencode-resilient.sh").read_text(encoding="utf-8")
assert config["free_only"] is True
allowed = set(config["free_only_allowed_models"])
assert allowed
assert all(m.startswith("opencode/") for m in allowed)
assert all(m.endswith("-free") or m == "opencode/big-pickle" for m in allowed)
assert "opencode/exo-free" not in allowed
for role, candidates in config["roles"].items():
    assert candidates, role
    assert len(set(candidates)) == len(candidates), role
    assert all(m in allowed for m in candidates), role
assert "SPIDER_UNAPPROVED_MODEL" in shell
assert "DISCOVERED=()" not in shell
assert "has been deprecated" in shell
assert any(m != config["roles"]["research"][0] for m in config["roles"]["design_review"])

# Headless execution must not ask a non-existent human or silently consume a paid model.
permissions = json.loads((root / ".github/scripts/opencode-ci-permissions.json").read_text(encoding="utf-8"))
policy = permissions["permission"]
assert policy["bash"] == "allow"
assert policy["question"] == "deny"
assert policy["doom_loop"] == "deny"
assert policy["external_directory"]["*"] == "deny"
assert policy["read"]["*.env"] == "deny"
assert 'OPENCODE_CONFIG_CONTENT' in shell
assert 'SPIDER_HEADLESS_PERMISSION_DENIED' in shell
assert 'headless-permission-denied' in shell
assert 'MAX_ATTEMPTS="${SPIDER_MODEL_MAX_ATTEMPTS:-3}"' in shell
assert 'MAX_RUNTIME_SECONDS="${SPIDER_MODEL_MAX_RUNTIME_SECONDS:-1200}"' in shell
assert all(len(candidates) <= 4 for candidates in config["roles"].values())
assert config["roles"]["research"][0] != config["roles"]["audit"][0]
assert config["roles"]["research"][0] != config["roles"]["design_review"][0]
pulse = (root / ".github/workflows/factory-pulse.yml").read_text(encoding="utf-8")
assert 'cron: "17 * * * *"' in pulse
assert '"codex/**"' not in pulse
assert 'group: spider-r2-factory-pulse' in pulse

print("SPIDER_FREE_MODEL_CONFIG_OK")
