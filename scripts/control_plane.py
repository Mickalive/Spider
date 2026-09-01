#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

CONTROL_ROOTS = [
    ".gitignore",
    ".github/scripts",
    "scripts",
    ".opencode/agents",
    "AGENTS.md",
    "SPIDER_ARCHITECTURE_RESEARCH2.md",
    "research/claims/registry.json",
    "research/lanes/registry.json",
    "research/EXPERIMENT_PACKET.md",
    "config/models.json",
]


def run(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git_text(root: Path, *args: str, check: bool = True) -> str:
    return run(root, "git", *args, check=check).stdout.decode("utf-8", errors="replace")


def files_at(root: Path, ref: str, path: str) -> set[str]:
    out = git_text(root, "ls-tree", "-r", "--name-only", ref, "--", path, check=False)
    return {line.strip() for line in out.splitlines() if line.strip()}


def local_files(root: Path, path: str) -> set[str]:
    p = root / path
    if p.is_file() or p.is_symlink():
        return {path}
    if not p.exists():
        return set()
    return {x.relative_to(root).as_posix() for x in p.rglob("*") if x.is_file() or x.is_symlink()}


def blob(root: Path, ref: str, path: str) -> bytes:
    return run(root, "git", "show", f"{ref}:{path}").stdout


def materialize(root: Path, ref: str) -> None:
    for control_root in CONTROL_ROOTS:
        expected = files_at(root, ref, control_root)
        current = local_files(root, control_root)
        for extra in sorted(current - expected, reverse=True):
            p = root / extra
            if p.exists() or p.is_symlink():
                p.unlink()
        for rel in sorted(expected):
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(blob(root, ref, rel))


def verify(root: Path, ref: str) -> list[str]:
    bad: list[str] = []
    for control_root in CONTROL_ROOTS:
        expected = files_at(root, ref, control_root)
        current = local_files(root, control_root)
        if current != expected:
            bad.extend(sorted((current ^ expected)))
            continue
        for rel in sorted(expected):
            expected_sha = git_text(root, "rev-parse", f"{ref}:{rel}").strip()
            local_sha = git_text(root, "hash-object", rel).strip() if (root / rel).exists() else "MISSING"
            if local_sha != expected_sha:
                bad.append(rel)
    return sorted(set(bad))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["stage", "restore", "check"])
    ap.add_argument("--root", default=os.environ.get("GITHUB_WORKSPACE", "."))
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if args.mode in {"stage", "check"}:
        run(root, "git", "fetch", "-q", "origin", "main")
        ref = "origin/main"
    else:
        ref = "HEAD"

    if args.mode == "check":
        bad = verify(root, ref)
        if bad:
            print("SPIDER_CONTROL_OVERLAY_DIRTY")
            print("\n".join(bad))
            raise SystemExit(2)
        print("SPIDER_CONTROL_OVERLAY_OK")
        return

    materialize(root, ref)
    print(f"SPIDER_CONTROL_OVERLAY_{args.mode.upper()} ref={ref}")


if __name__ == "__main__":
    main()
