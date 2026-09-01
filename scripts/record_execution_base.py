#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    args = ap.parse_args()
    exp = ROOT / "research/experiments" / args.experiment_id
    path = exp / "execution_checkpoint.json"
    if path.exists():
        print("SPIDER_EXECUTION_BASE_EXISTS")
        return
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    payload = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "pre_execute_sha": sha,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"SPIDER_EXECUTION_BASE {sha}")


if __name__ == "__main__":
    main()
