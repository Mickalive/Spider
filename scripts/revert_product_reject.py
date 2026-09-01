#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args, check=True):
    return subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    args = ap.parse_args()
    exp = ROOT / "research/experiments" / args.experiment_id
    verdict = json.loads((exp / "verdict.json").read_text())
    if verdict.get("promote_to_product"):
        print("SPIDER_PRODUCT_CODE_ACCEPTED")
        return
    base = json.loads((exp / "execution_checkpoint.json").read_text())["pre_execute_sha"]
    roots = ["src", "tests", "sdk", "pyproject.toml"]
    changed = run("git", "diff", "--name-only", base, "HEAD", "--", *roots).stdout.splitlines()
    for path in sorted(set(filter(None, changed))):
        present = run("git", "cat-file", "-e", f"{base}:{path}", check=False).returncode == 0
        if present:
            run("git", "checkout", base, "--", path)
        else:
            run("git", "rm", "-f", "--ignore-unmatch", "--", path, check=False)
            p = ROOT / path
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            elif p.exists() or p.is_symlink():
                p.unlink(missing_ok=True)
    print(f"SPIDER_PRODUCT_CODE_REVERTED files={len(changed)} base={base}")


if __name__ == "__main__":
    main()
