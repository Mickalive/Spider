#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIONS = {"CONTINUE", "PIVOT", "PARK", "REOPEN", "TERMINATE"}
ACTIVE_ACTIONS = {"CONTINUE", "PIVOT", "REOPEN"}
HANDOFF_DISPOSITIONS = {"USE", "SUPERSEDE", "PARK"}
REQUIRED_LANE_KEYS = {
    "action",
    "claim_id",
    "question",
    "mechanism_family",
    "budget_units",
    "decision_impact",
    "rationale",
    "opportunity_cost",
    "parent_handoff_disposition",
    "cognitive_reset",
    "exceptional_continue_justification",
}


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--allocation", required=True)
    args = ap.parse_args()

    snapshot = load(args.snapshot)
    allocation = load(args.allocation)
    lane_registry = json.loads(
        (ROOT / "research/lanes/registry.json").read_text(encoding="utf-8")
    )["lanes"]

    require(allocation.get("schema_version") == 1, "portfolio allocation schema_version must be 1")
    require(allocation.get("cycle_id") == snapshot.get("cycle_id"), "portfolio allocation cycle_id mismatch")
    require(
        allocation.get("total_budget_units") == snapshot.get("total_budget_units"),
        "portfolio allocation total_budget_units mismatch",
    )
    require(nonempty(allocation.get("portfolio_rationale")), "portfolio_rationale must be non-empty")
    require(
        allocation.get("reset_question") == snapshot.get("reset_question"),
        "portfolio reset_question mismatch",
    )

    allocs = allocation.get("allocations")
    require(isinstance(allocs, dict), "allocations must be an object")
    require(set(allocs) == set(lane_registry), "allocations must contain all lanes exactly once")

    total = 0
    active_claims: list[str] = []
    active_lanes = 0

    for lane, cfg in lane_registry.items():
        item = allocs[lane]
        require(isinstance(item, dict), f"{lane}: allocation must be an object")
        missing = sorted(REQUIRED_LANE_KEYS - set(item))
        require(not missing, f"{lane}: missing allocation keys {missing}")

        action = item["action"]
        require(action in ACTIONS, f"{lane}: invalid action {action}")
        budget = item["budget_units"]
        require(isinstance(budget, int) and not isinstance(budget, bool), f"{lane}: budget_units must be integer")
        require(0 <= budget <= 100, f"{lane}: invalid budget_units {budget}")
        total += budget

        require(nonempty(item["rationale"]), f"{lane}: rationale must be non-empty")
        require(nonempty(item["opportunity_cost"]), f"{lane}: opportunity_cost must be non-empty")
        require(
            item["parent_handoff_disposition"] in HANDOFF_DISPOSITIONS,
            f"{lane}: invalid parent_handoff_disposition",
        )
        require(isinstance(item["cognitive_reset"], bool), f"{lane}: cognitive_reset must be boolean")

        lane_state = snapshot["lanes"][lane]
        tunnel = bool(lane_state.get("tunnel_flag"))

        if action in ACTIVE_ACTIONS:
            active_lanes += 1
            claim_id = item["claim_id"]
            require(claim_id in (cfg.get("priority_claims") or []), f"{lane}: claim {claim_id} is not lane-eligible")
            require(nonempty(item["question"]), f"{lane}: active allocation requires question")
            require(nonempty(item["mechanism_family"]), f"{lane}: active allocation requires mechanism_family")
            require(nonempty(item["decision_impact"]), f"{lane}: active allocation requires decision_impact")
            require(budget >= 5, f"{lane}: active allocation requires at least 5 budget units")
            active_claims.append(claim_id)

            if action == "CONTINUE":
                last_claim = lane_state.get("last_claim")
                if last_claim:
                    require(
                        claim_id == last_claim,
                        f"{lane}: CONTINUE must continue last_claim={last_claim}; use PIVOT/REOPEN for {claim_id}",
                    )
                require(
                    budget >= int(lane_state.get("min_continue_budget", 5)),
                    f"{lane}: CONTINUE budget below depth-priced minimum {lane_state.get('min_continue_budget')}",
                )

            if tunnel:
                require(item["cognitive_reset"] is True, f"{lane}: tunnel continuation/allocation requires cognitive_reset=true")
                if action == "CONTINUE":
                    require(
                        nonempty(item["exceptional_continue_justification"]),
                        f"{lane}: tunnel CONTINUE requires exceptional_continue_justification",
                    )
            elif item["exceptional_continue_justification"] is not None:
                require(
                    nonempty(item["exceptional_continue_justification"]),
                    f"{lane}: exceptional_continue_justification must be null or non-empty",
                )
        else:
            require(budget == 0, f"{lane}: {action} must consume zero budget")
            require(item["question"] is None, f"{lane}: {action} question must be null")
            require(item["mechanism_family"] is None, f"{lane}: {action} mechanism_family must be null")
            require(
                item["parent_handoff_disposition"] == "PARK",
                f"{lane}: {action} must PARK the parent handoff",
            )
            if item["claim_id"] is not None:
                require(item["claim_id"] in (cfg.get("priority_claims") or []), f"{lane}: parked claim is not lane-eligible")

    require(total == allocation.get("budget_used"), "budget_used must equal sum of lane budgets")
    require(total <= snapshot.get("total_budget_units", 100), "portfolio budget exceeded")

    starved = set(snapshot.get("global", {}).get("starved_claims") or [])
    eligible_starved = {
        claim
        for lane, cfg in lane_registry.items()
        for claim in (cfg.get("priority_claims") or [])
        if claim in starved
    }
    if eligible_starved and active_lanes:
        require(
            bool(set(active_claims) & eligible_starved),
            "portfolio ignores every eligible starved claim",
        )

    if active_lanes >= 3:
        require(
            len(set(active_claims)) >= 2,
            "portfolio collapses 3+ active lanes onto a single claim",
        )

    print(
        "SPIDER_PORTFOLIO_ALLOCATION_OK "
        f"cycle={allocation['cycle_id']} budget={total}/{allocation['total_budget_units']} "
        f"active_lanes={active_lanes} distinct_claims={len(set(active_claims))} "
        f"starved_targeted={len(set(active_claims) & eligible_starved)}"
    )


if __name__ == "__main__":
    main()
