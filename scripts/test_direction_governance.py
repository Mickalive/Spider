#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANES = json.loads((ROOT / "research/lanes/registry.json").read_text())["lanes"]


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def base_snapshot() -> dict:
    return {
        "schema_version": 1,
        "cycle_id": "TEST-CYCLE",
        "lanes": {
            lane: {
                "last_claim": cfg["priority_claims"][0],
                "tunnel_flag": lane == "physics",
            }
            for lane, cfg in LANES.items()
        },
    }


def base_allocation() -> dict:
    allocs = {}
    for lane, cfg in LANES.items():
        claim = cfg["priority_claims"][0]
        action = "PIVOT"
        if lane == "physics":
            # Regression: strategic CONTINUE may cross the last finalized
            # claim-id boundary and a tunnel diagnostic must not veto judgment.
            claim = "C-WEB-DYNAMICS"
            action = "CONTINUE"
        allocs[lane] = {
            "action": action,
            "claim_id": claim,
            "question": f"Test strategic question for {lane}",
            "rationale": "Materially useful next direction.",
            "comparative_reasoning": "Preferred after comparing the full program.",
            "parent_handoff_disposition": "USE" if action == "CONTINUE" else "SUPERSEDE",
            "dependencies": [],
            "cognitive_reset": False,
        }
    return {
        "schema_version": 1,
        "cycle_id": "TEST-CYCLE",
        "portfolio_assessment": "Global assessment.",
        "scout_assessment": "Scout advice considered.",
        "agent_priors_used": ["General agent prior, explicitly not SPIDER evidence."],
        "allocations": allocs,
    }


def run_validator(snapshot: dict, allocation: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        snap = td / "snapshot.json"
        alloc = td / "allocation.json"
        write_json(snap, snapshot)
        write_json(alloc, allocation)
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_portfolio_allocation.py"),
                "--snapshot",
                str(snap),
                "--allocation",
                str(alloc),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )


def main() -> None:
    good = run_validator(base_snapshot(), base_allocation())
    if good.returncode != 0:
        raise SystemExit(
            "valid reasoned allocation was rejected:\n"
            + good.stdout
            + good.stderr
        )

    bad = base_allocation()
    bad["allocations"]["intel"]["claim_id"] = "C-FRESHNESS"
    rejected = run_validator(base_snapshot(), bad)
    if rejected.returncode == 0:
        raise SystemExit("validator accepted a lane-ineligible claim")

    missing = base_allocation()
    del missing["allocations"]["graph"]["comparative_reasoning"]
    rejected = run_validator(base_snapshot(), missing)
    if rejected.returncode == 0:
        raise SystemExit("validator accepted a structurally incomplete mandate")

    print("SPIDER_DIRECTION_GOVERNANCE_TEST_OK")


if __name__ == "__main__":
    main()
