#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANES = {"graph", "physics", "runtime", "product", "intel", "frontier"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--brief", required=True)
    args = ap.parse_args()

    snapshot = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))

    require(brief.get("schema_version") == 1, "scout brief schema_version must be 1")
    require(brief.get("cycle_id") == snapshot.get("cycle_id"), "scout brief cycle_id mismatch")
    require(nonempty(brief.get("executive_assessment")), "scout brief executive_assessment must be non-empty")

    for key in (
        "spider_evidence",
        "external_directional_context",
        "agent_priors",
        "cross_lane_dependencies",
        "stalled_or_idle_lanes",
        "questions_for_director",
    ):
        require(isinstance(brief.get(key), list), f"scout brief {key} must be a list")

    candidates = brief.get("candidate_directions")
    require(isinstance(candidates, dict), "scout brief candidate_directions must be an object")
    require(set(candidates) == LANES, "scout brief must cover all six lanes")
    for lane, items in candidates.items():
        require(isinstance(items, list), f"scout brief candidate_directions[{lane}] must be a list")
        require(all(isinstance(x, str) and x.strip() for x in items), f"scout brief candidate_directions[{lane}] has invalid item")

    print(
        "SPIDER_SCOUT_BRIEF_OK "
        f"cycle={brief['cycle_id']} "
        f"external={len(brief['external_directional_context'])} "
        f"priors={len(brief['agent_priors'])}"
    )


if __name__ == "__main__":
    main()
