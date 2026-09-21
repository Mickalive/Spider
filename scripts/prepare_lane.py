#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from research2_contract import PORTFOLIO_ACTIVE_ACTIONS

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
        raise RuntimeError(f"lane state references parent {parent_id} but {rel.as_posix()} is missing")
    got = file_sha256(path)
    expected = state.get("last_handoff_sha256")
    if expected and got != expected:
        raise RuntimeError(f"parent handoff hash mismatch for {parent_id}: expected {expected}, got {got}")
    return {
        "experiment_id": parent_id,
        "path": rel.as_posix(),
        "sha256": got,
    }


def decode_portfolio_allocation(encoded: str, lane: str) -> dict:
    if not encoded:
        raise RuntimeError("portfolio allocation required before allocating a new experiment")
    try:
        raw = base64.b64decode(encoded.encode("ascii"), validate=True)
        payload = json.loads(raw)
    except Exception as exc:
        raise RuntimeError(f"invalid portfolio allocation payload: {exc}") from exc
    if payload.get("schema_version") != 1:
        raise RuntimeError("unsupported portfolio allocation schema")
    allocations = payload.get("allocations")
    if not isinstance(allocations, dict) or lane not in allocations:
        raise RuntimeError(f"portfolio allocation missing lane: {lane}")
    item = allocations[lane]
    if not isinstance(item, dict):
        raise RuntimeError(f"portfolio allocation lane payload invalid: {lane}")
    action = item.get("action")
    if action not in PORTFOLIO_ACTIVE_ACTIONS:
        raise RuntimeError(
            f"portfolio action {action!r} does not authorize a new experiment for lane {lane}"
        )
    if not item.get("claim_id") or not item.get("question"):
        raise RuntimeError(f"portfolio allocation missing claim/question for lane {lane}")
    return payload


def all_exist(exp: Path, names: list[str]) -> bool:
    return all((exp / name).exists() for name in names)


def packet_stage_flags(exp: Path) -> tuple[bool, bool, bool, bool]:
    frozen = all_exist(exp, ["spec.json", "prereg.md", "freeze.json"])
    executed = frozen and all_exist(exp, ["result.json", "report.md", "provenance.json"])
    audited = executed and (exp / "audit.json").exists()
    finalized = audited and all_exist(exp, ["verdict.json", "handoff.json"])
    return frozen, executed, audited, finalized


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--reason", default="pulse")
    ap.add_argument("--chain-depth", type=int, default=0)
    ap.add_argument("--experiment-id", default="")
    ap.add_argument("--portfolio-allocation-b64", default="")
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
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        print(f"SPIDER_RESUME experiment_id={exp_id} request_id={req['request_id']}")
    else:
        portfolio_allocation = decode_portfolio_allocation(args.portfolio_allocation_b64, args.lane)
        lane_allocation = portfolio_allocation["allocations"][args.lane]

        # Product promotion is a durable transaction boundary. Never allocate a
        # child experiment until product-promote has acknowledged the accepted
        # code delta on main and cleared this latch.
        if args.lane == "product" and state.get("promotion_ready"):
            raise SystemExit(
                f"product promotion pending for {state.get('last_experiment_id')}; refusing to allocate a new experiment"
            )

        # Refuse to create a child experiment if the previous handoff has been
        # lost or altered. Silent continuity loss is worse than a loud stop.
        inherited = parent_handoff_from_state(state)
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
                "portfolio_allocation": portfolio_allocation,
            }
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
            print(
                "SPIDER_PORTFOLIO_MANDATE "
                f"cycle={portfolio_allocation.get('cycle_id')} "
                f"action={lane_allocation.get('action')} "
                f"claim={lane_allocation.get('claim_id')} "
                f"budget={lane_allocation.get('budget_units')}"
            )
        state.update({
            "active_experiment_id": exp_id,
            "continue_immediately": False,
            "promotion_ready": False,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })

    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    frozen, executed, audited, finalized = packet_stage_flags(exp)

    out = Path(os.environ.get("GITHUB_OUTPUT", "/tmp/spider_prepare_output"))
    with out.open("a", encoding="utf-8") as fh:
        fh.write(f"experiment_id={exp_id}\n")
        fh.write(f"experiment_dir=research/experiments/{exp_id}\n")
        fh.write(f"request_id={req['request_id']}\n")
        fh.write(f"frozen={'true' if frozen else 'false'}\n")
        fh.write(f"executed={'true' if executed else 'false'}\n")
        fh.write(f"audited={'true' if audited else 'false'}\n")
        fh.write(f"finalized={'true' if finalized else 'false'}\n")


if __name__ == "__main__":
    main()
