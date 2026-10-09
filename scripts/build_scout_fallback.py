#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

LANES = ["graph", "physics", "runtime", "product", "intel", "frontier"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--reason", default="Scout unavailable")
    args = ap.parse_args()

    snapshot = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    candidates = {}
    stalled = []

    for lane in LANES:
        state = snapshot.get("lanes", {}).get(lane, {})
        suggestions = []
        parent = state.get("parent_handoff_proposal")
        if isinstance(parent, str) and parent.strip():
            suggestions.append(parent.strip())
        for claim in state.get("neglected_priority_claims", [])[:2]:
            suggestions.append(
                f"Reassess whether {claim} is now the highest-value claim for {lane}; "
                "use the Director snapshot and canonical evidence, not local continuity alone."
            )
        candidates[lane] = suggestions[:3]

        if state.get("active_stage") in {"IDLE", "PREFREEZE", "BROKEN_REFERENCE"}:
            stalled.append(
                {
                    "lane": lane,
                    "status": state.get("active_stage"),
                    "suggested_reactivation": (
                        "Global Director must explicitly decide REOPEN/PIVOT/PARK from canonical evidence."
                    ),
                }
            )

    brief = {
        "schema_version": 1,
        "cycle_id": snapshot.get("cycle_id"),
        "executive_assessment": (
            f"DEGRADED SCOUT MODE: {args.reason}. "
            "No external reconnaissance or Scout synthesis is available this cycle. "
            "The Global Research Director must reason directly from the machine snapshot, "
            "canonical Codex state, lane missions and targeted packets. "
            "Do not treat this fallback as scientific evidence."
        ),
        "spider_evidence": [],
        "external_directional_context": [],
        "agent_priors": [],
        "cross_lane_dependencies": [],
        "stalled_or_idle_lanes": stalled,
        "candidate_directions": candidates,
        "questions_for_director": [
            "Which current blocker most constrains the core claim that later-agent cost should track residual novelty?",
            "Which lanes are repeating measurement-repair work whose prerequisite should instead be repaired once in Runtime/Product?",
            "Which active or dormant thread would you choose if no parent handoff existed?"
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(brief, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"SPIDER_SCOUT_FALLBACK cycle={brief['cycle_id']} reason={args.reason}")


if __name__ == "__main__":
    main()
