#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIM_STATUSES = {"HYPOTHESIS", "EXPERIMENTAL", "VALIDATED", "PRODUCT_CORE", "SHIPPED", "REJECTED", "BLOCKED", "MEASUREMENT_INVALID", "SUPERSEDED"}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def update_failure_state(req, retryable):
    state_path = ROOT / "research/lanes" / req["lane"] / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"lane": req["lane"]}
    state["active_experiment_id"] = req["experiment_id"]
    state["consecutive_failures"] = int(state.get("consecutive_failures", 0)) + 1
    state["last_failure_retryable"] = bool(retryable)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_path.write_text(json.dumps(state, indent=2) + "\n")


def failure(exp, req, stage, category, message, retryable):
    payload = {"stage": stage, "category": category, "message": message, "retryable": bool(retryable), "recorded_at": datetime.now(timezone.utc).isoformat(), "github_run_id": os.environ.get("GITHUB_RUN_ID"), "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT")}
    (exp / "failure.json").write_text(json.dumps(payload, indent=2) + "\n")
    update_failure_state(req, retryable)


def verify_freeze(exp):
    freeze = json.loads((exp / "freeze.json").read_text())
    for name, expected in freeze["hashes"].items():
        got = sha(exp / name)
        if got != expected:
            raise ValueError(f"frozen file changed: {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    ap.add_argument("--stage", required=True, choices=["design", "execute", "audit", "director"])
    ap.add_argument("--exit-code", type=int, default=0)
    ap.add_argument("--category", default="")
    args = ap.parse_args()
    exp = ROOT / "research/experiments" / args.experiment_id
    req = json.loads((exp / "request.json").read_text())
    try:
        if (exp / "freeze.json").exists(): verify_freeze(exp)
        if args.exit_code != 0:
            retryable = args.exit_code in (75, 124)
            failure(exp, req, args.stage, args.category or "OPERATIONAL_FAILURE", f"stage exited with code {args.exit_code}", retryable)
            print("SPIDER_STAGE_FAILURE_RECORDED")
            return
        if args.stage == "design":
            if not (exp / "freeze.json").exists(): raise ValueError("design did not produce freeze.json")
        elif args.stage == "execute":
            for f in ["result.json", "report.md", "provenance.json"]:
                if not (exp / f).exists(): raise ValueError(f"execute missing {f}")
            result = json.loads((exp / "result.json").read_text())
            for k in ["status", "metrics", "controls", "artifacts"]:
                if k not in result: raise ValueError(f"result missing {k}")
        elif args.stage == "audit":
            audit = json.loads((exp / "audit.json").read_text())
            if audit.get("status") not in {"PASS", "REVISE", "FAIL", "MEASUREMENT_INVALID", "BLOCKED"}: raise ValueError("invalid audit status")
            for k in ["producer_claim_supported", "required_fixes", "validity_findings", "baseline_findings", "recomputed_metrics", "claim_ceiling"]:
                if k not in audit: raise ValueError(f"audit missing {k}")
        elif args.stage == "director":
            verdict = json.loads((exp / "verdict.json").read_text())
            audit = json.loads((exp / "audit.json").read_text())
            for k in ["decision", "claim_updates", "product_action", "promote_to_product", "continue", "next_question", "reason"]:
                if k not in verdict: raise ValueError(f"verdict missing {k}")
            if not isinstance(verdict["claim_updates"], list): raise ValueError("claim_updates must be a list")
            known = {c["id"] for c in json.loads((ROOT / "research/claims/registry.json").read_text())["claims"]}
            for event in verdict["claim_updates"]:
                if not isinstance(event, dict): raise ValueError("claim update must be an object")
                if event.get("claim_id") not in known: raise ValueError(f"unknown claim update id: {event.get('claim_id')}")
                if event.get("status") not in CLAIM_STATUSES: raise ValueError(f"invalid claim update status: {event.get('status')}")
                if not event.get("reason"): raise ValueError("claim update requires reason")
            if verdict["promote_to_product"] and req["lane"] != "product": raise ValueError("only Product lane can promote product code")
            if verdict["promote_to_product"] and audit.get("status") != "PASS": raise ValueError("product promotion requires PASS audit")
            if not (exp / "handoff.json").exists(): raise ValueError("director missing handoff.json")
            state_path = ROOT / "research/lanes" / req["lane"] / "state.json"
            state = json.loads(state_path.read_text()) if state_path.exists() else {"lane": req["lane"]}
            state.update({
                "active_experiment_id": None,
                "last_experiment_id": args.experiment_id,
                "last_verdict": verdict["decision"],
                "continue_immediately": bool(verdict["continue"]),
                "next_question": verdict["next_question"],
                "promotion_ready": bool(verdict["promote_to_product"]) if req["lane"] == "product" else False,
                "consecutive_failures": 0,
                "last_failure_retryable": None,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            })
            state_path.write_text(json.dumps(state, indent=2) + "\n")
        if (exp / "failure.json").exists(): (exp / "failure.json").unlink()
        print(f"SPIDER_STAGE_OK stage={args.stage} experiment={args.experiment_id}")
    except Exception as exc:
        failure(exp, req, args.stage, "VALIDATION_FAILURE", str(exc), False)
        raise


if __name__ == "__main__":
    main()
