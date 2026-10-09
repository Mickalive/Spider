#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def under(path: str, root: str) -> bool:
    root = root.rstrip("/")
    return path == root or path.startswith(root + "/")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    args = ap.parse_args()

    exp = ROOT / "research/experiments" / args.experiment_id
    req = json.loads((exp / "request.json").read_text(encoding="utf-8"))
    spec = json.loads((exp / "spec.json").read_text(encoding="utf-8"))
    lane = req["lane"]

    build_required = spec.get("build_required", False)
    artifacts = spec.get("freeze_artifacts", [])
    if not isinstance(build_required, bool):
        raise SystemExit("spec.build_required must be boolean")
    if not isinstance(artifacts, list) or any(not isinstance(x, str) or not x.strip() for x in artifacts):
        raise SystemExit("spec.freeze_artifacts must be a list of non-empty repository-relative paths")
    if len(artifacts) != len(set(artifacts)):
        raise SystemExit("spec.freeze_artifacts contains duplicates")
    if build_required and not artifacts:
        raise SystemExit("build_required=true requires at least one freeze_artifact")

    lanes = json.loads((ROOT / "research/lanes/registry.json").read_text(encoding="utf-8"))
    roots = lanes["lanes"][lane].get("allowed_code_roots", [])
    exp_root = f"research/experiments/{args.experiment_id}"

    manifest = {}
    for rel in artifacts:
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts:
            raise SystemExit(f"unsafe freeze_artifact path: {rel}")
        if not (under(rel, exp_root) or any(under(rel, root) for root in roots)):
            raise SystemExit(f"freeze_artifact outside lane-authorized roots: {rel}")
        full = ROOT / rel
        if not full.is_file():
            raise SystemExit(f"freeze_artifact missing or not a file: {rel}")
        manifest[rel] = sha(full)

    pre_build_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()

    receipt = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "lane": lane,
        "build_required": build_required,
        "pre_build_sha": pre_build_sha,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": manifest,
    }
    (exp / "build_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "SPIDER_BUILD_RECEIPT "
        f"experiment={args.experiment_id} artifacts={len(manifest)} required={str(build_required).lower()}"
    )


if __name__ == "__main__":
    main()
