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
    "rationale",
    "comparative_reasoning",
    "parent_handoff_disposition",
    "dependencies",
    "cognitive_reset",
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
    require(nonempty(allocation.get("portfolio_assessment")), "portfolio_assessment must be non-empty")
    priors = allocation.get("agent_priors_used")
    require(isinstance(priors, list), "agent_priors_used must be a list")
    require(all(isinstance(x, str) and x.strip() for x in priors), "agent_priors_used entries must be non-empty strings")
    surface = allocation.get("surface_research", [])
    require(isinstance(surface, list), "surface_research must be a list when present")

    allocs = allocation.get("allocations")
    require(isinstance(allocs, dict), "allocations must be an object")
    require(set(allocs) == set(lane_registry), "allocations must contain all lanes exactly once")

    for lane, cfg in lane_registry.items():
        item = allocs[lane]
        require(isinstance(item, dict), f"{lane}: allocation must be an object")
        missing = sorted(REQUIRED_LANE_KEYS - set(item))
        require(not missing, f"{lane}: missing allocation keys {missing}")

        action = item["action"]
        require(action in ACTIONS, f"{lane}: invalid action {action}")
        require(nonempty(item["rationale"]), f"{lane}: rationale must be non-empty")
        require(nonempty(item["comparative_reasoning"]), f"{lane}: comparative_reasoning must be non-empty")
        require(
            item["parent_handoff_disposition"] in HANDOFF_DISPOSITIONS,
            f"{lane}: invalid parent_handoff_disposition",
        )
        require(isinstance(item["cognitive_reset"], bool), f"{lane}: cognitive_reset must be boolean")
        require(isinstance(item["dependencies"], list), f"{lane}: dependencies must be a list")

        lane_state = snapshot["lanes"][lane]
        tunnel = bool(lane_state.get("tunnel_flag"))

        if action in ACTIVE_ACTIONS:
            claim_id = item["claim_id"]
            require(claim_id in (cfg.get("priority_claims") or []), f"{lane}: claim {claim_id} is not lane-eligible")
            require(nonempty(item["question"]), f"{lane}: active allocation requires question")

            if action == "CONTINUE":
                last_claim = lane_state.get("last_claim")
                if last_claim:
                    require(
                        claim_id == last_claim,
                        f"{lane}: CONTINUE must continue last_claim={last_claim}; use PIVOT/REOPEN for {claim_id}",
                    )

            if tunnel:
                require(item["cognitive_reset"] is True, f"{lane}: tunnel continuation/allocation requires cognitive_reset=true")
        else:
            require(item["question"] is None, f"{lane}: {action} question must be null")
            require(
                item["parent_handoff_disposition"] == "PARK",
                f"{lane}: {action} must PARK the parent handoff",
            )
            if item["claim_id"] is not None:
                require(item["claim_id"] in (cfg.get("priority_claims") or []), f"{lane}: parked claim is not lane-eligible")

    print(
        "SPIDER_GLOBAL_DIRECTION_OK "
        f"cycle={allocation['cycle_id']} "
        + " ".join(f"{lane}:{allocs[lane]['action']}" for lane in sorted(allocs))
    )


if __name__ == "__main__":
    main()
