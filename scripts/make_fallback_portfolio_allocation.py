#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSED = {"REJECTED", "SUPERSEDED", "SHIPPED"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    snapshot = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    lanes = snapshot["lanes"]
    claims = snapshot["claims"]
    recent = snapshot["global"]["claim_recent_counts"]

    allocations = {}
    used = 0

    for lane, state in lanes.items():
        eligible = [
            claim_id
            for claim_id in state.get("priority_claims", [])
            if claims.get(claim_id, {}).get("effective_status") not in CLOSED
        ]
        if not eligible:
            allocations[lane] = {
                "action": "PARK",
                "claim_id": None,
                "question": None,
                "mechanism_family": None,
                "budget_units": 0,
                "decision_impact": "No open eligible claim is available in the lane charter.",
                "rationale": "Deterministic fallback parks the lane rather than inventing work.",
                "opportunity_cost": "Zero new research attention is consumed.",
                "parent_handoff_disposition": "PARK",
                "cognitive_reset": bool(state.get("tunnel_flag")),
                "exceptional_continue_justification": None,
            }
            continue

        last_claim = state.get("last_claim")
        alternatives = [c for c in eligible if c != last_claim]
        pool = alternatives or eligible
        target = min(
            pool,
            key=lambda c: (
                recent.get(c, 0),
                claims.get(c, {}).get("total_experiments", 0),
                c,
            ),
        )
        action = "PIVOT" if target != last_claim else "CONTINUE"
        budget = 10
        exceptional = None
        if action == "CONTINUE":
            budget = max(budget, int(state.get("min_continue_budget", 5)))
            if state.get("tunnel_flag"):
                exceptional = (
                    "Fallback could not find an alternative open charter-eligible claim; "
                    "continuation is permitted only to preserve liveness."
                )

        next_gate = claims.get(target, {}).get("next_gate") or "the next falsifiable gate"
        question = (
            f"What is the smallest discriminating experiment for {target} that directly tests "
            f"its current gate ({next_gate}) using accepted evidence, rather than extending the "
            "previous local thread by default?"
        )

        allocations[lane] = {
            "action": action,
            "claim_id": target,
            "question": question,
            "mechanism_family": f"fallback-{target.lower()}",
            "budget_units": budget,
            "decision_impact": (
                f"Reduce uncertainty on neglected claim {target} or close its current gate."
            ),
            "rationale": (
                "Model portfolio allocation was unavailable/invalid. Deterministic fallback "
                "selects the least-recent open claim eligible for this lane and avoids the "
                "current claim when an alternative exists."
            ),
            "opportunity_cost": (
                f"This spends {budget} units that could otherwise continue the inherited "
                "local thread; the fallback prefers neglected coverage."
            ),
            "parent_handoff_disposition": "SUPERSEDE" if action == "PIVOT" else "USE",
            "cognitive_reset": bool(state.get("tunnel_flag") or action == "PIVOT"),
            "exceptional_continue_justification": exceptional,
        }
        used += budget

    # If conservative defaults somehow exceed the cycle budget, park the most
    # expensive allocations until valid. This is preferable to silently
    # overspending or weakening the validator.
    if used > snapshot["total_budget_units"]:
        ordered = sorted(
            allocations,
            key=lambda lane: allocations[lane]["budget_units"],
            reverse=True,
        )
        for lane in ordered:
            if used <= snapshot["total_budget_units"]:
                break
            item = allocations[lane]
            if item["budget_units"] == 0:
                continue
            used -= item["budget_units"]
            item.update(
                {
                    "action": "PARK",
                    "claim_id": item["claim_id"],
                    "question": None,
                    "mechanism_family": None,
                    "budget_units": 0,
                    "decision_impact": "Deferred by deterministic budget cap.",
                    "rationale": "Fallback budget cap parks this allocation for the next cycle.",
                    "opportunity_cost": "The claim waits one portfolio cycle.",
                    "parent_handoff_disposition": "PARK",
                    "exceptional_continue_justification": None,
                }
            )

    payload = {
        "schema_version": 1,
        "cycle_id": snapshot["cycle_id"],
        "total_budget_units": snapshot["total_budget_units"],
        "budget_used": used,
        "portfolio_rationale": (
            "DETERMINISTIC FALLBACK: allocate toward least-recent eligible open claims, "
            "prefer pivots away from current threads, preserve budget and scientific liveness."
        ),
        "reset_question": snapshot["reset_question"],
        "allocations": allocations,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"SPIDER_PORTFOLIO_FALLBACK cycle={snapshot['cycle_id']} budget={used}")


if __name__ == "__main__":
    main()
