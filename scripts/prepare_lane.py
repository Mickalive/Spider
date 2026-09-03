#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parent_handoff_from_state(state: dict) -> dict | None:
    parent_id = state.get("last_experiment_id")
    if not parent_id:
        return None
    rel = Path("research") / "experiments" / parent_id / "handoff.json"
    path = ROOT / rel
    if not path.exists():
        return None
    return {
        "experiment_id": parent_id,
        "path": rel.as_posix(),
        "sha256": file_sha256(path),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--reason", default="pulse")
    ap.add_argument("--chain-depth", type=int, default=0)
    ap.add_argument("--experiment-id", default="")
    args = ap.parse_args()

    lanes = json.loads((ROOT / "research/lanes/registry.json").read_text())
    if args.lane not in lanes["lanes"] or not lanes["lanes"][args.lane].get("enabled"):
        raise SystemExit(f"lane not enabled: {args.lane}")

    lane_dir = ROOT / "research/lanes" / args.lane
    lane_dir.mkdir(parents=True, exist_ok=True)
    state_path = lane_dir / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {
        "lane": args.lane,
        "human_paused": False,
        "active_experiment_id": None,
        "last_experiment_id": None,
        "last_verdict": None,
        "continue_immediately": False,
        "next_question": None,
        "promotion_ready": False,
        "consecutive_failures": 0,
    }

    if args.experiment_id:
        exp_id = args.experiment_id
        exp = ROOT / "research/experiments" / exp_id
        req_path = exp / "request.json"
        if not req_path.exists():
            raise SystemExit(f"resume experiment not found: {exp_id}")
        req = json.loads(req_path.read_text())
        if req.get("lane") != args.lane:
            raise SystemExit("resume lane identity mismatch")
        state["active_experiment_id"] = exp_id
        print(f"SPIDER_RESUME experiment_id={exp_id} request_id={req['request_id']}")
    else:
        exp_id = f"EXP-{args.lane.upper()}-{args.run_id}"
        exp = ROOT / "research/experiments" / exp_id
        exp.mkdir(parents=True, exist_ok=True)
        req_path = exp / "request.json"
        if req_path.exists():
            req = json.loads(req_path.read_text())
            if req["lane"] != args.lane:
                raise SystemExit("existing request identity mismatch")
        else:
            claims_bytes = (ROOT / "research/claims/registry.json").read_bytes()
            base_sha = os.environ.get("SPIDER_START_SHA") or os.environ.get("GITHUB_SHA") or "unknown"
            seed = {
                "schema_version": 1,
                "experiment_id": exp_id,
                "lane": args.lane,
                "origin_github_run_id": str(args.run_id),
                "reason": args.reason,
                "chain_depth": args.chain_depth,
                "base_sha": base_sha,
                "claim_registry_sha256": hashlib.sha256(claims_bytes).hexdigest(),
            }
            inherited = parent_handoff_from_state(state)
            if inherited is not None:
                seed["parent_handoff"] = inherited
                seed["inherited_next_question"] = state.get("next_question")
                seed["inherited_last_verdict"] = state.get("last_verdict")

            request_id = hashlib.sha256(canonical(seed)).hexdigest()[:24]
            req = dict(seed, request_id=request_id, created_at=datetime.now(timezone.utc).isoformat())
            req["request_hash"] = hashlib.sha256(canonical({k: v for k, v in req.items() if k != "request_hash"})).hexdigest()
            req_path.write_text(json.dumps(req, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            spec = {
                "experiment_id": exp_id,
                "lane": args.lane,
                "claim_ids": [],
                "question": "",
                "hypothesis": "",
                "falsifier": "",
                "baselines": [],
                "positive_control": "",
                "null_control": "",
                "measurement_validity": [],
                "decision_rule": "",
                "product_consequence_positive": "",
                "product_consequence_negative": "",
                "estimated_cost": "",
                "expected_information_gain": "",
            }
            (exp / "spec.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
            (exp / "prereg.md").write_text(f"# {exp_id} preregistration\n\nDESIGN NOT YET FROZEN.\n", encoding="utf-8")
            print(f"SPIDER_NEW experiment_id={exp_id} request_id={request_id}")
            if inherited is not None:
                print(f"SPIDER_PARENT_HANDOFF experiment_id={inherited['experiment_id']} sha256={inherited['sha256']}")
        state.update({
            "active_experiment_id": exp_id,
            "continue_immediately": False,
            "promotion_ready": False,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })

    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    out = Path(os.environ.get("GITHUB_OUTPUT", "/tmp/spider_prepare_output"))
    with out.open("a", encoding="utf-8") as fh:
        fh.write(f"experiment_id={exp_id}\n")
        fh.write(f"experiment_dir=research/experiments/{exp_id}\n")
        fh.write(f"request_id={req['request_id']}\n")
        fh.write(f"frozen={'true' if (exp / 'freeze.json').exists() else 'false'}\n")
        fh.write(f"executed={'true' if (exp / 'result.json').exists() else 'false'}\n")
        fh.write(f"audited={'true' if (exp / 'audit.json').exists() else 'false'}\n")
        fh.write(f"finalized={'true' if (exp / 'verdict.json').exists() else 'false'}\n")


if __name__ == "__main__":
    main()
