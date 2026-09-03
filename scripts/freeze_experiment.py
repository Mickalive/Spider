#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prereg_is_substantive(path: Path, experiment_id: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    # The DESIGN agent may legitimately retain a human-readable status line such as
    # "DESIGN NOT YET FROZEN" until this deterministic freezer runs. Reject only the
    # untouched scaffold / trivially incomplete prereg, not that phrase by itself.
    scaffold = f"# {experiment_id} preregistration\n\nDESIGN NOT YET FROZEN.".strip()
    if text == scaffold:
        return False
    if len(text) < 500:
        return False
    if experiment_id not in text:
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    args = ap.parse_args()
    exp = ROOT / "research/experiments" / args.experiment_id
    if (exp / "freeze.json").exists():
        print("SPIDER_ALREADY_FROZEN")
        return

    req = json.loads((exp / "request.json").read_text())
    spec = json.loads((exp / "spec.json").read_text())
    required = [
        "experiment_id", "lane", "claim_ids", "question", "hypothesis", "falsifier",
        "baselines", "positive_control", "null_control", "measurement_validity",
        "decision_rule", "product_consequence_positive", "product_consequence_negative",
        "estimated_cost", "expected_information_gain",
    ]
    missing = [k for k in required if k not in spec or spec[k] in ("", None, [])]
    if missing:
        raise SystemExit(f"cannot freeze incomplete spec: {missing}")
    if spec["experiment_id"] != args.experiment_id or spec["lane"] != req["lane"]:
        raise SystemExit("spec/request identity mismatch")
    if not prereg_is_substantive(exp / "prereg.md", args.experiment_id):
        raise SystemExit("preregistration remains scaffold or is structurally incomplete")

    claims = json.loads((ROOT / "research/claims/registry.json").read_text())
    known = {c["id"] for c in claims["claims"]}
    unknown = set(spec["claim_ids"]) - known
    if unknown:
        raise SystemExit(f"unknown claim ids: {sorted(unknown)}")

    freeze = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "hashes": {
            "request.json": sha(exp / "request.json"),
            "spec.json": sha(exp / "spec.json"),
            "prereg.md": sha(exp / "prereg.md"),
        },
    }
    (exp / "freeze.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
    print(f"SPIDER_FROZEN {args.experiment_id}")


if __name__ == "__main__":
    main()
