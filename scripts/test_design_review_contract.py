#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    "decision_rule_reachability",
    "measurement_prerequisites",
    "baseline_identifiability",
    "control_sensitivity",
    "treatment_liveness",
    "freeze_artifacts_bound",
)


def check(status: str = "PASS") -> dict:
    return {"status": status, "reason": f"{status} regression fixture", "evidence_refs": []}


def run(spec: dict, review: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        spec_path = td / "spec.json"
        review_path = td / "review.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        review_path.write_text(json.dumps(review), encoding="utf-8")
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_design_review.py"),
                "--spec",
                str(spec_path),
                "--review",
                str(review_path),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )


def main() -> None:
    spec = {
        "experiment_id": "EXP-TEST-1",
        "lane": "product",
        "freeze_eligibility": {
            name: check("NOT_APPLICABLE" if name == "freeze_artifacts_bound" else "PASS")
            for name in CHECKS
        },
        "freeze_artifacts": [],
    }
    review = {
        "schema_version": 1,
        "experiment_id": "EXP-TEST-1",
        "lane": "product",
        "status": "PASS",
        "checks": {
            name: check("NOT_APPLICABLE" if name == "freeze_artifacts_bound" else "PASS")
            for name in CHECKS
        },
        "blocking_findings": [],
        "nonblocking_findings": [],
        "rationale": "All six checks are satisfiable in this regression fixture.",
        "evidence_refs": [],
    }

    good = run(spec, review)
    if good.returncode != 0:
        raise SystemExit("valid design review rejected:\n" + good.stdout + good.stderr)

    bad = json.loads(json.dumps(review))
    bad["checks"]["baseline_identifiability"] = check("FAIL")
    bad["status"] = "PASS"
    rejected = run(spec, bad)
    if rejected.returncode == 0:
        raise SystemExit("validator accepted PASS review containing a failed identifiability check")

    revise = json.loads(json.dumps(review))
    revise["checks"]["baseline_identifiability"] = check("FAIL")
    revise["status"] = "REVISE"
    accepted_revise = run(spec, revise)
    if accepted_revise.returncode != 0:
        raise SystemExit("validator rejected structurally valid REVISE review")

    print("SPIDER_DESIGN_REVIEW_CONTRACT_TEST_OK")


if __name__ == "__main__":
    main()
