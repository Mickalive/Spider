#!/usr/bin/env python3
"""Reproducible matched task matrix. Plan-only by default; no provider call."""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

from spider.pilot_portal import DATA

ARMS = ("COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER", "CACHE")


def make_plan(seed: int = 20261011, replicates: int = 1) -> list[dict]:
    if replicates < 1:
        raise ValueError("replicates must be positive")
    rng = random.Random(seed)
    rows = []
    for replicate in range(replicates):
        for family, entries in DATA.items():
            for identifier in entries:
                arms = list(ARMS)
                rng.shuffle(arms)
                for arm in arms:
                    rows.append({
                        "task_id": f"{family}:{identifier}",
                        "family": family,
                        "identifier": identifier,
                        "arm": arm,
                        "replicate": replicate,
                    })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261011)
    ap.add_argument("--replicates", type=int, default=1)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--allow-model-charges", action="store_true")
    ap.add_argument("--max-trials", type=int, default=20)
    ap.add_argument("--provider", choices=("google", "browser-use"), default="google")
    ap.add_argument("--model")
    ap.add_argument("--seeded-fixture", action="store_true")
    args = ap.parse_args()

    plan = make_plan(args.seed, args.replicates)
    if len(plan) > args.max_trials:
        ap.error(f"plan has {len(plan)} trials; max-trials is {args.max_trials}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plan_path = args.output.with_suffix(".plan.json")
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"SPIDER_PILOT_PLAN trials={len(plan)} path={plan_path} (no money spent yet)")
    if not args.execute:
        return
    if not args.allow_model_charges:
        ap.error("--execute requires explicit --allow-model-charges")
    runner = Path(__file__).with_name("run_real_agent_pilot.py")
    for row in plan:
        cmd = [sys.executable, str(runner), "--arm", row["arm"], "--family",
               row["family"], "--id", row["identifier"],
               "--provider", args.provider, "--replicate", str(row["replicate"]),
               "--allow-model-charges",
               "--output", str(args.output)]
        if args.model:
            cmd += ["--model", args.model]
        if args.seeded_fixture and row["arm"] == "SPIDER":
            cmd += ["--seeded-fixture"]
        subprocess.run(cmd, check=True)
    print("SPIDER_PILOT_RAW_TRACES_COMPLETE (cost_accounting_complete=false; no market claim)")


if __name__ == "__main__":
    main()
