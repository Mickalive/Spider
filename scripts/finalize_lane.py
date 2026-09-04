#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIM_STATUSES = {"HYPOTHESIS", "EXPERIMENTAL", "VALIDATED", "PRODUCT_CORE", "SHIPPED", "REJECTED", "BLOCKED", "MEASUREMENT_INVALID", "SUPERSEDED"}
AUDIT_STATUSES = {"PASS", "REVISE", "FAIL", "MEASUREMENT_INVALID", "BLOCKED"}
RESULT_STATUSES = {"COMPLETE", "BLOCKED", "MEASUREMENT_INVALID"}
RESULT_OUTCOMES = {"SUPPORTS", "FALSIFIES", "MIXED", "INCONCLUSIVE", "NOT_APPLICABLE"}
LANES = {"graph", "physics", "runtime", "product", "intel", "frontier"}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def require_keys(obj, keys, label):
    if not isinstance(obj, dict):
        raise ValueError(f"{label} must be a JSON object")
    for key in keys:
        if key not in obj:
            raise ValueError(f"{label} missing {key}")


def require_identity(obj, req, label):
    require_keys(obj, ["schema_version", "experiment_id", "lane"], label)
    if obj["schema_version"] != 1:
        raise ValueError(f"{label} unsupported schema_version: {obj['schema_version']}")
    if obj["experiment_id"] != req["experiment_id"]:
        raise ValueError(f"{label} experiment_id mismatch")
    if obj["lane"] != req["lane"]:
        raise ValueError(f"{label} lane mismatch")


def require_list(obj, key, label):
    if not isinstance(obj[key], list):
        raise ValueError(f"{label} {key} must be a list")


def require_dict(obj, key, label):
    if not isinstance(obj[key], dict):
        raise ValueError(f"{label} {key} must be an object")


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


def validate_result(exp, req):
    for f in ["result.json", "report.md", "provenance.json"]:
        if not (exp / f).exists():
            raise ValueError(f"execute missing {f}")

    result = json.loads((exp / "result.json").read_text())
    require_identity(result, req, "result")
    require_keys(result, ["status", "outcome", "metrics", "controls", "artifacts", "observations", "validity_notes", "unresolved"], "result")
    if result["status"] not in RESULT_STATUSES:
        raise ValueError(f"invalid result status: {result['status']}")
    if result["outcome"] not in RESULT_OUTCOMES:
        raise ValueError(f"invalid result outcome: {result['outcome']}")
    require_dict(result, "metrics", "result")
    require_dict(result, "controls", "result")
    for key in ["artifacts", "observations", "validity_notes", "unresolved"]:
        require_list(result, key, "result")

    provenance = json.loads((exp / "provenance.json").read_text())
    if not isinstance(provenance, dict):
        raise ValueError("provenance must be a JSON object")
    if "experiment_id" in provenance and provenance["experiment_id"] != req["experiment_id"]:
        raise ValueError("provenance experiment_id mismatch")
    if "lane" in provenance and provenance["lane"] != req["lane"]:
        raise ValueError("provenance lane mismatch")


def validate_audit(exp, req):
    audit = json.loads((exp / "audit.json").read_text())
    require_identity(audit, req, "audit")
    require_keys(audit, ["status", "producer_claim_supported", "required_fixes", "validity_findings", "baseline_findings", "recomputed_metrics", "claim_ceiling", "evidence_refs", "unresolved"], "audit")
    if audit["status"] not in AUDIT_STATUSES:
        raise ValueError("invalid audit status")
    if not isinstance(audit["producer_claim_supported"], bool):
        raise ValueError("audit producer_claim_supported must be boolean")
    for key in ["required_fixes", "validity_findings", "baseline_findings", "evidence_refs", "unresolved"]:
        require_list(audit, key, "audit")
    require_dict(audit, "recomputed_metrics", "audit")
    if not isinstance(audit["claim_ceiling"], str) or not audit["claim_ceiling"].strip():
        raise ValueError("audit claim_ceiling must be a non-empty string")
    return audit


def validate_verdict_and_handoff(exp, req):
    verdict = json.loads((exp / "verdict.json").read_text())
    require_identity(verdict, req, "verdict")
    require_keys(verdict, ["decision", "claim_updates", "product_action", "promote_to_product", "continue", "next_question", "reason", "evidence_refs"], "verdict")
    if not isinstance(verdict["claim_updates"], list):
        raise ValueError("claim_updates must be a list")
    if not isinstance(verdict["promote_to_product"], bool):
        raise ValueError("promote_to_product must be boolean")
    if not isinstance(verdict["continue"], bool):
        raise ValueError("continue must be boolean")
    if verdict["next_question"] is not None and not isinstance(verdict["next_question"], str):
        raise ValueError("next_question must be string or null")
    if not isinstance(verdict["reason"], str) or not verdict["reason"].strip():
        raise ValueError("verdict reason must be a non-empty string")
    require_list(verdict, "evidence_refs", "verdict")

    known = {c["id"] for c in json.loads((ROOT / "research/claims/registry.json").read_text())["claims"]}
    for event in verdict["claim_updates"]:
        if not isinstance(event, dict):
            raise ValueError("claim update must be an object")
        if event.get("claim_id") not in known:
            raise ValueError(f"unknown claim update id: {event.get('claim_id')}")
        if event.get("status") not in CLAIM_STATUSES:
            raise ValueError(f"invalid claim update status: {event.get('status')}")
        if not event.get("reason"):
            raise ValueError("claim update requires reason")

    if not (exp / "handoff.json").exists():
        raise ValueError("director missing handoff.json")
    handoff = json.loads((exp / "handoff.json").read_text())
    require_identity(handoff, req, "handoff")
    require_keys(handoff, ["target_lane", "next_question", "why_next", "carry_forward", "dependencies", "evidence_refs", "recommended_action"], "handoff")
    target = handoff["target_lane"]
    if target is not None and target not in LANES:
        raise ValueError(f"invalid handoff target_lane: {target}")
    if handoff["next_question"] != verdict["next_question"]:
        raise ValueError("handoff next_question must equal verdict next_question")
    if not isinstance(handoff["why_next"], str):
        raise ValueError("handoff why_next must be a string")
    require_dict(handoff, "carry_forward", "handoff")
    for key in ["established", "rejected", "unknown", "do_not_assume"]:
        if key not in handoff["carry_forward"]:
            raise ValueError(f"handoff carry_forward missing {key}")
        if not isinstance(handoff["carry_forward"][key], list):
            raise ValueError(f"handoff carry_forward {key} must be a list")
    for key in ["dependencies", "evidence_refs"]:
        require_list(handoff, key, "handoff")
    if not isinstance(handoff["recommended_action"], str):
        raise ValueError("handoff recommended_action must be a string")

    return verdict, handoff


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
            if not (exp / "freeze.json").exists():
                raise ValueError("design did not produce freeze.json")

        elif args.stage == "execute":
            validate_result(exp, req)

        elif args.stage == "audit":
            validate_audit(exp, req)

        elif args.stage == "director":
            audit = json.loads((exp / "audit.json").read_text())
            verdict, handoff = validate_verdict_and_handoff(exp, req)
            if verdict["promote_to_product"] and req["lane"] != "product":
                raise ValueError("only Product lane can promote product code")
            if verdict["promote_to_product"] and audit.get("status") != "PASS":
                raise ValueError("product promotion requires PASS audit")

            state_path = ROOT / "research/lanes" / req["lane"] / "state.json"
            state = json.loads(state_path.read_text()) if state_path.exists() else {"lane": req["lane"]}
            state.update({
                "active_experiment_id": None,
                "last_experiment_id": args.experiment_id,
                "last_verdict": verdict["decision"],
                "last_handoff_sha256": sha(exp / "handoff.json"),
                "continue_immediately": bool(verdict["continue"]),
                "next_question": verdict["next_question"],
                "promotion_ready": bool(verdict["promote_to_product"]) if req["lane"] == "product" else False,
                "consecutive_failures": 0,
                "last_failure_retryable": None,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            })
            state_path.write_text(json.dumps(state, indent=2) + "\n")

        if (exp / "failure.json").exists():
            (exp / "failure.json").unlink()
        print(f"SPIDER_STAGE_OK stage={args.stage} experiment={args.experiment_id}")
    except Exception as exc:
        failure(exp, req, args.stage, "VALIDATION_FAILURE", str(exc), False)
        raise


if __name__ == "__main__":
    main()
