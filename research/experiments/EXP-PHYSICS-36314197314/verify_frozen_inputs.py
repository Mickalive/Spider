#!/usr/bin/env python3
"""Frozen-input integrity verifier for EXP-PHYSICS-36314197314.

Recomputes the three freeze.json digests against the on-disk frozen files and
checks that no executor-owned file has overwritten a frozen input. Read-only.
"""
import hashlib
import json
import os
import sys

EXPDIR = os.path.dirname(os.path.abspath(__file__))
FROZEN = ["prereg.md", "request.json", "spec.json"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    freeze = json.load(open(os.path.join(EXPDIR, "freeze.json")))
    out = {"experiment_id": freeze.get("experiment_id"), "frozen_at": freeze.get("frozen_at"),
           "checks": [], "all_match": True,
           "frozen_files_referenced_by_freeze_json": sorted(freeze.get("hashes", {})),
           "prereg_referenced_artifacts_present": {}, "prereg_referenced_artifacts_absent": []}
    for name in FROZEN:
        p = os.path.join(EXPDIR, name)
        got = sha256(p) if os.path.exists(p) else None
        want = freeze["hashes"].get(name)
        ok = (got == want)
        out["all_match"] &= ok
        out["checks"].append({"file": name, "expected_sha256": want, "observed_sha256": got,
                              "match": ok})
    # prereg section 15 artifact table: which of the declared artifacts exist
    for art in ["frozen_origins.json", "raw_responses/", "response_signatures.jsonl",
                "mechanism_pool.json", "split.json", "predictions.jsonl",
                "baseline_predictions.jsonl", "control_predictions.jsonl",
                "permutation_nulls.json", "bootstrap_cis.json", "pilot_data.json",
                "power_calculation.json"]:
        p = os.path.join(EXPDIR, art)
        exists = os.path.exists(p)
        out["prereg_referenced_artifacts_present"][art] = exists
        if not exists:
            out["prereg_referenced_artifacts_absent"].append(art)
    json.dump(out, open(os.path.join(EXPDIR, "raw", "frozen_input_verification.json"), "w"),
              indent=1)
    print(json.dumps(out["checks"], indent=1))
    print("ALL_MATCH", out["all_match"])
    print("ABSENT_AT_FREEZE", out["prereg_referenced_artifacts_absent"])
    return 0 if out["all_match"] else 1


if __name__ == "__main__":
    sys.exit(main())
