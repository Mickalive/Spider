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
print("SPIDER_FREE_MODEL_CONFIG_OK")
