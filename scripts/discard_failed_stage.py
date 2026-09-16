#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    "execute": ["result.json", "report.md", "provenance.json"],
    "audit": ["audit.json"],
    "director": ["verdict.json", "handoff.json"],
}


def run(*args: str, check: bool = False):
    return subprocess.run(args, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=check)


def exists_at(ref: str, path: str) -> bool:
    return run("git", "cat-file", "-e", f"{ref}:{path}").returncode == 0


def restore_path(ref: str, path: str) -> None:
    if exists_at(ref, path):
        run("git", "restore", f"--source={ref}", "--staged", "--worktree", "--", path)
    else:
        run("git", "rm", "-r", "-f", "--ignore-unmatch", "--", path)
        p = ROOT / path
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.exists() or p.is_symlink():
            p.unlink(missing_ok=True)
    # Remove files created by the failed attempt that do not exist at the base.
    run("git", "clean", "-fd", "--", path)


def clean_failed_execute(exp_id: str, exp: Path) -> None:
    req = json.loads((exp / "request.json").read_text())
    lane = req["lane"]
    registry = json.loads((ROOT / "research/lanes/registry.json").read_text())
    roots = registry["lanes"][lane].get("allowed_code_roots", [])
    checkpoint = json.loads((exp / "execution_checkpoint.json").read_text())
    base = checkpoint.get("pre_execute_sha")
    if not base:
        raise RuntimeError("execution checkpoint missing pre_execute_sha")

    # Preserve only the durable diagnostic receipts from the failed attempt.
    preserved: dict[str, bytes] = {}
    for name in ["failure.json", "model_execute.json"]:
        p = exp / name
        if p.exists():
            preserved[name] = p.read_bytes()

    # Scientific/code mutations from an unsuccessful execute must never become
    # the starting point of its retry. Restore every registry-authorized code
    # root to the immutable pre-execution commit.
    for root in roots:
        restore_path(base, root)

    # The execute stage is allowed to create arbitrary raw evidence/scripts under
    # the experiment directory. On failure those are a mixed/partial attempt and
    # must not contaminate a later provider. Restore the packet to current HEAD
    # (which contains the frozen inputs + execution checkpoint), then reattach the
    # two diagnostic receipts above.
    rel_exp = f"research/experiments/{exp_id}"
    restore_path("HEAD", rel_exp)
    for name, data in preserved.items():
        (exp / name).parent.mkdir(parents=True, exist_ok=True)
        (exp / name).write_bytes(data)


def discard_stage_outputs(exp_id: str, exp: Path, stage: str) -> None:
    for name in OUTPUTS[stage]:
        rel = f"research/experiments/{exp_id}/{name}"
        if exists_at("HEAD", rel):
            run("git", "restore", "--source=HEAD", "--staged", "--worktree", "--", rel)
        else:
            p = exp / name
            if p.exists():
                p.unlink()
            run("git", "reset", "-q", "HEAD", "--", rel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    ap.add_argument("--stage", required=True, choices=sorted(OUTPUTS))
    args = ap.parse_args()
    exp = ROOT / "research/experiments" / args.experiment_id

    if args.stage == "execute":
        clean_failed_execute(args.experiment_id, exp)
    else:
        discard_stage_outputs(args.experiment_id, exp, args.stage)
    print(f"SPIDER_DISCARDED_INVALID_STAGE_OUTPUTS stage={args.stage}")


if __name__ == "__main__":
    main()
