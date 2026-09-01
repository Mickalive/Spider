#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_ROOTS = [
    ".gitignore", ".github/scripts", "scripts", ".opencode/agents", "AGENTS.md",
    "SPIDER_ARCHITECTURE_RESEARCH2.md", "research/claims/registry.json",
    "research/lanes/registry.json", "research/EXPERIMENT_PACKET.md", "config/models.json",
]


def run(*args, check=True):
    return subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def status_paths():
    out = run("git", "status", "--porcelain=v1", "-z").stdout
    chunks = out.split("\0")
    paths = []
    for item in chunks:
        if not item:
            continue
        path = item[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return sorted(set(paths))


def under(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")


def is_control(path: str) -> bool:
    return any(under(path, root) for root in CONTROL_ROOTS)


def allowed(path, prefixes, exact):
    return path in exact or any(under(path, p) for p in prefixes)


def exists_in_head(path):
    return run("git", "cat-file", "-e", f"HEAD:{path}", check=False).returncode == 0


def restore(path):
    run("git", "reset", "-q", "HEAD", "--", path, check=False)
    if exists_in_head(path):
        run("git", "restore", "--source=HEAD", "--worktree", "--", path, check=False)
    else:
        p = ROOT / path
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.exists() or p.is_symlink():
            p.unlink(missing_ok=True)


def verify_control_overlay(repair: bool) -> None:
    helper = Path(os.environ.get("SPIDER_CONTROL_HELPER", "/tmp/spider-control-plane.py"))
    if not helper.exists():
        raise SystemExit("SPIDER_CONTROL_HELPER_MISSING")
    cmd = ["python", str(helper), "check", "--root", str(ROOT)]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode == 0:
        return
    if repair:
        subprocess.run(["python", str(helper), "stage", "--root", str(ROOT)], cwd=ROOT, check=False)
    print("SPIDER_CONTROL_SCOPE_VIOLATION")
    print(proc.stdout)
    print(proc.stderr)
    raise SystemExit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--experiment-id", required=True)
    ap.add_argument("--stage", required=True, choices=["design", "execute", "audit", "director"])
    ap.add_argument("--repair", action="store_true")
    args = ap.parse_args()

    verify_control_overlay(args.repair)

    lanes = json.loads((ROOT / "research/lanes/registry.json").read_text())
    cfg = lanes["lanes"][args.lane]
    exp = f"research/experiments/{args.experiment_id}"
    lane_state = f"research/lanes/{args.lane}/state.json"

    protected = set()
    if args.stage == "design":
        prefixes = []
        exact = [f"{exp}/spec.json", f"{exp}/prereg.md", f"{exp}/failure.json", f"{exp}/model_design.json"]
        protected = {f"{exp}/request.json", lane_state}
    elif args.stage == "execute":
        prefixes = [exp] + cfg.get("allowed_code_roots", [])
        exact = []
        protected = {f"{exp}/{x}" for x in ["request.json", "spec.json", "prereg.md", "freeze.json", "execution_checkpoint.json"]} | {lane_state}
    elif args.stage == "audit":
        prefixes = []
        exact = [f"{exp}/audit.json", f"{exp}/failure.json", f"{exp}/model_audit.json"]
        protected = {f"{exp}/{x}" for x in ["request.json", "spec.json", "prereg.md", "freeze.json", "execution_checkpoint.json", "result.json", "report.md", "provenance.json", "model_execute.json"]} | {lane_state}
    else:
        prefixes = []
        exact = [f"{exp}/verdict.json", f"{exp}/handoff.json", f"{exp}/failure.json", f"{exp}/model_director.json"]
        protected = {f"{exp}/{x}" for x in ["request.json", "spec.json", "prereg.md", "freeze.json", "execution_checkpoint.json", "result.json", "report.md", "provenance.json", "audit.json", "model_execute.json", "model_audit.json"]} | {lane_state}

    changed = [p for p in status_paths() if not is_control(p)]
    bad = sorted({p for p in changed if p in protected or not allowed(p, prefixes, exact)})
    if bad and args.repair:
        for path in bad:
            restore(path)
    if bad:
        print("SPIDER_SCOPE_VIOLATION")
        print("\n".join(bad))
        raise SystemExit(2)
    print("SPIDER_SCOPE_OK")


if __name__ == "__main__":
    main()
