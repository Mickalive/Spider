#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

CHECKS = (
    "decision_rule_reachability",
    "measurement_prerequisites",
    "baseline_identifiability",
    "control_sensitivity",
    "treatment_liveness",
    "freeze_artifacts_bound",
)
CHECK_STATUSES = {"PASS", "NOT_APPLICABLE", "FAIL"}


def require(cond: bool, message: str) -> None:
    if not cond:
        raise SystemExit(message)


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--review", required=True)
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    review = json.loads(Path(args.review).read_text(encoding="utf-8"))

    require(review.get("schema_version") == 1, "design review schema_version must be 1")
    require(review.get("experiment_id") == spec.get("experiment_id"), "design review experiment_id mismatch")
    require(review.get("lane") == spec.get("lane"), "design review lane mismatch")
    require(review.get("status") in {"PASS", "REVISE"}, "design review status invalid")
    require(nonempty(review.get("rationale")), "design review rationale must be non-empty")

    checks = review.get("checks")
    require(isinstance(checks, dict), "design review checks must be an object")
    require(set(checks) == set(CHECKS), "design review checks must contain the exact six required checks")

    failed = []
    for name in CHECKS:
        item = checks[name]
        require(isinstance(item, dict), f"{name}: review check must be an object")
        status = item.get("status")
        require(status in CHECK_STATUSES, f"{name}: invalid review status {status}")
        require(nonempty(item.get("reason")), f"{name}: reason must be non-empty")
        refs = item.get("evidence_refs")
        require(isinstance(refs, list), f"{name}: evidence_refs must be a list")
        require(all(isinstance(x, str) and x.strip() for x in refs), f"{name}: invalid evidence ref")
        if status == "FAIL":
            failed.append(name)

    for key in ("blocking_findings", "nonblocking_findings", "evidence_refs"):
        require(isinstance(review.get(key), list), f"design review {key} must be a list")

    if failed:
        require(review["status"] == "REVISE", "design review with failed checks must be REVISE")
    else:
        require(review["status"] == "PASS", "design review without failed checks must be PASS")

    if review["status"] == "PASS":
        eligibility = spec.get("freeze_eligibility")
        require(isinstance(eligibility, dict), "PASS review requires spec.freeze_eligibility")
        require(set(eligibility) == set(CHECKS), "spec.freeze_eligibility must contain exact required checks")
        for name in CHECKS:
            item = eligibility[name]
            require(isinstance(item, dict), f"freeze_eligibility.{name} must be object")
            require(item.get("status") in {"PASS", "NOT_APPLICABLE"}, f"freeze_eligibility.{name} is not freeze-eligible")
            require(nonempty(item.get("reason")), f"freeze_eligibility.{name} requires reason")

    print(
        "SPIDER_DESIGN_REVIEW_OK "
        f"experiment={review['experiment_id']} status={review['status']} failed={','.join(failed) if failed else 'none'}"
    )


if __name__ == "__main__":
    main()
