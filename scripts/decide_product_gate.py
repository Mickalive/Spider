#!/usr/bin/env python3
"""Strict *advisory* product go/no-go gate; never promotes science.

Go means candidate for independent audit only. Prerecorded thresholds:
>=20% lower *fully loaded* USD/safe-success than the cheapest practical
comparator; <=2pp worse safe success rate; >=10 paired trials per family.
Refuse a task bank on which cold + retrieval sit at a 100% correctness ceiling.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from score_product_benchmark import read_trials, score


def decide(rows: list[dict], *, min_per_family: int = 10,
           min_saving: float = 0.2, max_success_deficit: float = 0.02) -> dict:
    descriptive = score(rows, public=True, require_native_cache=True)
    counts: dict[str, set[tuple[str,int]]] = {}
    for row in rows:
        counts.setdefault(row["family"], set()).add((row["task_id"], row["replicate"]))
    reasons = []
    if len(counts) < 2 or any(len(tasks) < min_per_family for tasks in counts.values()):
        reasons.append("insufficient paired tasks across independent families")
    if descriptive["baseline_ceiling_warning"]:
        reasons.append("cold and retrieval sit at ceiling; task bank non-discriminating")
    if reasons:
        return {"decision": "INCONCLUSIVE_FIX_EVIDENCE", "reasons": reasons,
                "per_family_count": {k: len(v) for k,v in counts.items()},
                "descriptive": descriptive}

    arms = descriptive["arms"]
    comparators = ["COLD", "INSTRUCTIONS", "RETRIEVAL", "COMPILED", "DIRECT_API",
                   "STAGEHAND_V4_SERVER_CACHE"]
    measured = [(n, arms[n]["cost_per_safe_success_usd"]) for n in comparators
                if arms[n]["cost_per_safe_success_usd"] is not None]
    if len(measured) != len(comparators):
        return {"decision": "INCONCLUSIVE_FIX_EVIDENCE",
                "reasons": ["one or more comparators cannot complete any safely verified task"],
                "descriptive": descriptive}
    strongest, best_cost = min(measured, key=lambda pair: pair[1])
    spider = arms["SPIDER"]
    own = spider["cost_per_safe_success_usd"]
    if own is None:
        return {"decision": "STOP_OR_PIVOT", "reasons": ["Spider has zero safe successes"],
                "strongest_comparator": strongest, "descriptive": descriptive}
    savings = (best_cost - own) / best_cost if best_cost > 0 else None
    reliability_floor = max(arms[a]["safe_success_rate"] for a in comparators) - max_success_deficit
    passes = (savings is not None and savings >= min_saving
              and spider["safe_success_rate"] >= reliability_floor
              and spider["unsafe_trials"] == 0)
    return {
        "decision": "CANDIDATE_GO_PENDING_INDEPENDENT_AUDIT" if passes else "STOP_OR_PIVOT",
        "reasons": [] if passes else ["cost/success/safety preregistered gate not met"],
        "best_comparator": strongest, "best_comparator_cost_usd": best_cost,
        "spider_cost_per_safe_success_usd": own,
        "savings_fraction_vs_cheapest": savings,
        "reliability_floor": reliability_floor,
        "per_family_count": {k: len(v) for k,v in counts.items()},
        "audit_gate": "Not independently audited; never auto-promote.",
        "descriptive": descriptive,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = decide(read_trials(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["decision"])


if __name__ == "__main__":
    main()
