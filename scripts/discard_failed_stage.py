#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    "execute": ["result.json", "report.md", "provenance.json"],
    "audit": ["audit.json"],
    "director": ["verdict.json", "handoff.json"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    ap.add_argument("--stage", required=True, choices=sorted(OUTPUTS))
    args = ap.parse_args()
    exp = ROOT / "research/experiments" / args.experiment_id
    for name in OUTPUTS[args.stage]:
        rel = f"research/experiments/{args.experiment_id}/{name}"
        present = subprocess.run(["git", "cat-file", "-e", f"HEAD:{rel}"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        if present:
            subprocess.run(["git", "restore", "--source=HEAD", "--staged", "--worktree", "--", rel], cwd=ROOT, check=False)
        else:
            p = exp / name
            if p.exists(): p.unlink()
            subprocess.run(["git", "reset", "-q", "HEAD", "--", rel], cwd=ROOT, check=False)
    print(f"SPIDER_DISCARDED_INVALID_STAGE_OUTPUTS stage={args.stage}")


if __name__ == "__main__":
    main()
