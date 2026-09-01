#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    args = ap.parse_args()
    exp = ROOT/"research/experiments"/args.experiment_id
    if (exp/"freeze.json").exists():
        print("SPIDER_ALREADY_FROZEN")
        return

    req = json.loads((exp/"request.json").read_text())
    spec = json.loads((exp/"spec.json").read_text())
    required = ["experiment_id","lane","claim_ids","question","hypothesis","falsifier","baselines","positive_control","null_control","measurement_validity","decision_rule","product_consequence_positive","product_consequence_negative","estimated_cost","expected_information_gain"]
    missing = [k for k in required if k not in spec or spec[k] in ("", None, [])]
    if missing:
        raise SystemExit(f"cannot freeze incomplete spec: {missing}")
    if spec["experiment_id"] != args.experiment_id or spec["lane"] != req["lane"]:
        raise SystemExit("spec/request identity mismatch")
    if "DESIGN NOT YET FROZEN" in (exp/"prereg.md").read_text():
        raise SystemExit("preregistration placeholder not replaced")

    claims = json.loads((ROOT/"research/claims/registry.json").read_text())
    known = {c["id"] for c in claims["claims"]}
    unknown = set(spec["claim_ids"]) - known
    if unknown:
        raise SystemExit(f"unknown claim ids: {sorted(unknown)}")

    freeze = {"schema_version":1,"experiment_id":args.experiment_id,"frozen_at":datetime.now(timezone.utc).isoformat(),"hashes":{"request.json":sha(exp/"request.json"),"spec.json":sha(exp/"spec.json"),"prereg.md":sha(exp/"prereg.md")}}
    (exp/"freeze.json").write_text(json.dumps(freeze, indent=2, sort_keys=True)+"\n")
    print(f"SPIDER_FROZEN {args.experiment_id}")

if __name__ == "__main__":
    main()
