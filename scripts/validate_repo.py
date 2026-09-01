#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def main():
    claims = load("research/claims/registry.json")
    lanes = load("research/lanes/registry.json")
    models = load("config/models.json")

    claim_ids = [c["id"] for c in claims["claims"]]
    if len(claim_ids) != len(set(claim_ids)):
        raise SystemExit("duplicate claim id")

    known = set(claim_ids)
    for lane, cfg in lanes["lanes"].items():
        if not cfg.get("mission"):
            raise SystemExit(f"lane {lane}: missing mission")
        unknown = set(cfg.get("priority_claims", [])) - known
        if unknown:
            raise SystemExit(f"lane {lane}: unknown claims {sorted(unknown)}")

    for role, candidates in models["roles"].items():
        if not candidates or len(candidates) != len(set(candidates)):
            raise SystemExit(f"model role {role}: empty or duplicate candidates")

    required = {"request.json","spec.json","prereg.md","freeze.json","result.json","report.md","provenance.json","audit.json","verdict.json","handoff.json"}
    exp_root = ROOT / "research/experiments"
    if exp_root.exists():
        for exp in exp_root.glob("*"):
            if not exp.is_dir() or not (exp / "verdict.json").exists():
                continue
            missing = sorted(x for x in required if not (exp / x).exists())
            if missing:
                raise SystemExit(f"{exp.name}: finalized packet missing {missing}")

    print(f"SPIDER_R2_VALIDATE_OK claims={len(claim_ids)} lanes={len(lanes['lanes'])} roles={len(models['roles'])}")

if __name__ == "__main__":
    main()
