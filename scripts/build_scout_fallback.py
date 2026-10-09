#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--reason", default="Scout model unavailable")
    args = ap.parse_args()

    snapshot = load(args.snapshot)
    lanes = snapshot.get("lanes", {})

    stalled = []
    candidates = {}
    for lane, state in lanes.items():
        stage = state.get("active_stage") or "UNKNOWN"
        if stage in {"IDLE", "PREFREEZE", "BROKEN_REFERENCE"} or state.get("same_failure_count", 0):
            stalled.append({
                "lane": lane,
                "status": stage,
                "suggested_reactivation": (
                    "Global Research Director should decide from the snapshot; "
                    "this fallback does not choose a direction."
                ),
            })

        lane_candidates: list[str] = []
        inherited = state.get("parent_handoff_proposal")
        if isinstance(inherited, str) and inherited.strip():
            lane_candidates.append(
                "LOCAL HANDOFF PROPOSAL ONLY: " + inherited.strip()
            )
        neglected = state.get("neglected_priority_claims") or []
        if neglected:
            lane_candidates.append(
                "Reassess neglected charter-eligible claims from accepted evidence: "
                + ", ".join(str(x) for x in neglected[:4])
            )
        if not lane_candidates:
            lane_candidates.append(
                "Reassess this lane from the current accepted snapshot; no Scout recommendation is available."
            )
        candidates[lane] = lane_candidates

    global_state = snapshot.get("global", {})
    payload = {
        "schema_version": 1,
        "cycle_id": snapshot.get("cycle_id"),
        "executive_assessment": (
            "DEGRADED SCOUT BRIEF. The model-based Research Scout was unavailable. "
            "This brief is deterministic and contains no external reconnaissance or "
            "new scientific interpretation. The Global Research Director must reason "
            "from the accepted machine snapshot and targeted canonical packets."
        ),
        "spider_evidence": [
            {
                "finding": (
                    f"Accepted directional snapshot contains "
                    f"{global_state.get('canonical_experiments', 'unknown')} canonical experiments, "
                    f"{global_state.get('quarantined_experiments', 'unknown')} quarantined packets, "
                    f"and {len(global_state.get('starved_claims') or [])} starved claims."
                ),
                "evidence_refs": [str(args.snapshot)],
            }
        ],
        "external_directional_context": [],
        "agent_priors": [],
        "cross_lane_dependencies": [],
        "stalled_or_idle_lanes": stalled,
        "candidate_directions": candidates,
        "questions_for_director": [
            "Scout was unavailable. Do not interpret missing reconnaissance as evidence.",
            "Use the accepted snapshot, lane missions and targeted canonical packets to choose direction.",
            f"Operational reason: {args.reason}",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "SPIDER_SCOUT_FALLBACK "
        f"cycle={payload['cycle_id']} stalled={len(stalled)}"
    )


if __name__ == "__main__":
    main()
