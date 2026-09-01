#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def status_paths():
    out = subprocess.check_output(["git","status","--porcelain=v1","-z"], cwd=ROOT)
    chunks = out.decode(errors="replace").split("\0")
    paths = []
    for item in chunks:
        if not item:
            continue
        path = item[3:]
        if " -> " in path:
            path = path.split(" -> ",1)[1]
        paths.append(path)
    return sorted(set(paths))

def allowed(path, prefixes, exact):
    return path in exact or any(path == p or path.startswith(p.rstrip("/")+"/") for p in prefixes)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--lane",required=True)
    ap.add_argument("--experiment-id",required=True)
    ap.add_argument("--stage",required=True,choices=["design","execute","audit","director"])
    args=ap.parse_args()
    lanes=json.loads((ROOT/"research/lanes/registry.json").read_text())
    cfg=lanes["lanes"][args.lane]
    exp=f"research/experiments/{args.experiment_id}"
    lane_state=f"research/lanes/{args.lane}"

    if args.stage=="design":
        prefixes=[exp]; exact=[]
    elif args.stage=="execute":
        prefixes=[exp] + cfg.get("allowed_code_roots",[]); exact=[]
    elif args.stage=="audit":
        prefixes=[]; exact=[f"{exp}/audit.json"]
    else:
        prefixes=[lane_state]; exact=[f"{exp}/verdict.json",f"{exp}/handoff.json"]

    bad=[p for p in status_paths() if not allowed(p,prefixes,exact)]
    if bad:
        print("\n".join(bad))
        raise SystemExit(2)
    print("SPIDER_SCOPE_OK")

if __name__=="__main__":
    main()
