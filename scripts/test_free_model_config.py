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
assert "opencode/exo-free" in allowed
# Provider official pricing list at audit date, not inferred from -free suffix.
verified_free = {
    "opencode/big-pickle",
    "opencode/mimo-v2.6-flash-free",
    "opencode/mimo-v2.5-free",
    "opencode/ling-3.1-flash-free",
    "opencode/ling-3.0-flash-fin-free",
    "opencode/nemotron-3-ultra-free",
    "opencode/nemotron-3.5-lightning-free",
    "opencode/muse-spark-1.3-contributor-free",
    "opencode/space-bunny-free",
    "opencode/longcat-2.5-preview-free",
    "opencode/step-5-preview-free",
    "opencode/exo-free",
}
assert config["free_price_evidence_url"] == "https://dev.opencode.ai/v2/docs/console/models"
assert config["free_price_checked_date"] == "2026-10-12"
assert allowed == verified_free, "all twelve official free text models must be selectable"
assert allowed <= verified_free, "unverified promotional model added"
# Quality priors are anchored in independent/public benchmarks, never invented
# SPIDER internal performance numbers. The ranking is a provisional fallback
# and role-specific (coding is not the same skill as portfolio synthesis).
ranking = config["ranking_provenance"]
assert ranking["version"] == 1
assert len(ranking["sources"]) >= 3
assert ranking["date"] == "2026-10-12"
assert "NOT SPIDER" in ranking["method"]
MUSE = "opencode/muse-spark-1.3-contributor-free"
LING = "opencode/ling-3.1-flash-free"
MIMO = "opencode/mimo-v2.6-flash-free"
SPACE = "opencode/space-bunny-free"
LONGCAT = "opencode/longcat-2.5-preview-free"
assert config["roles"]["coding"][:5] == [MIMO, MUSE, SPACE, LONGCAT, LING]
assert config["roles"]["research"][:3] == [MUSE, LING, MIMO]
assert config["roles"]["director"][:3] == [MUSE, LING, MIMO]
assert config["roles"]["audit"][:2] == [LING, MUSE]
assert config["roles"]["scout"][:2] == [LING, MUSE]
assert config["free_only_allowed_models"][:3] == [MUSE, LING, MIMO]
assert config["roles"]["research"][0] != config["roles"]["audit"][0]


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
assert 'The user has specified a rule which prevents you from using this specific tool call' in shell
assert 'MAX_ATTEMPTS="${SPIDER_MODEL_MAX_ATTEMPTS:-6}"' in shell
assert 'MAX_RUNTIME_SECONDS="${SPIDER_MODEL_MAX_RUNTIME_SECONDS:-1200}"' in shell
assert all(set(candidates) == allowed for candidates in config["roles"].values())
assert config["roles"]["research"][0] != config["roles"]["audit"][0]
assert config["roles"]["research"][0] != config["roles"]["design_review"][0]
pulse = (root / ".github/workflows/factory-pulse.yml").read_text(encoding="utf-8")
assert 'cron: "17 * * * *"' in pulse
assert '"codex/**"' not in pulse
assert 'group: spider-r2-factory-pulse' in pulse
assert 'SPIDER_PREFERRED_FREE_MODEL' in shell
assert 'SPIDER_PREFERRED_FREE_MODEL:' in pulse
lane = (root / ".github/workflows/spider-lane.yml").read_text(encoding="utf-8")
assert "preferred_free_model" in lane
assert "SPIDER_PREFERRED_FREE_MODEL:" in lane

print("SPIDER_FREE_MODEL_CONFIG_OK")
