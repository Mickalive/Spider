#!/usr/bin/env python3
"""Descriptive paired benchmark scoring; NOT a benchmark executor or claim promotion.

Input: one JSONL row per (task_id, replicate, arm). Fully-loaded cost includes
model, browser, memory, retrieval, verification, repair, and amortized writes.
No synthetic results are produced and incomplete paired trials are rejected.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

ARMS = ("COLD", "INSTRUCTIONS", "RETRIEVAL", "SPIDER")
COMPETITOR_ARM = "CACHE"  # independently measured Stagehand/compiled workflow, never synthesized
REQUIRED = ("task_id", "replicate", "family", "phase", "arm",
            "success", "safe", "cost_usd", "latency_ms", "tokens", "cost_accounting_complete")


def read_trials(path: Path) -> list[dict]:
    rows = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        row = json.loads(raw)
        missing = set(REQUIRED).difference(row)
        if missing:
            raise ValueError(f"line {lineno}: missing {sorted(missing)}")
        if row["arm"] not in ARMS + (COMPETITOR_ARM,):
            raise ValueError(f"line {lineno}: unknown arm")
        if row["cost_accounting_complete"] is not True:
            raise ValueError(f"line {lineno}: incomplete cost accounting; do not score raw pilot traces")
        if type(row["success"]) is not bool or type(row["safe"]) is not bool:
            raise ValueError(f"line {lineno}: success and safe must be booleans")
        for metric in ("cost_usd", "latency_ms", "tokens"):
            number = row[metric]
            if type(number) not in (float, int) or not math.isfinite(number) or number < 0:
                raise ValueError(f"line {lineno}: invalid {metric}")
        for name in ("task_id", "family", "phase"):
            if not isinstance(row[name], str) or not row[name].strip():
                raise ValueError(f"line {lineno}: empty {name}")
        if type(row["replicate"]) is not int or row["replicate"] < 0:
            raise ValueError(f"line {lineno}: invalid replicate")
        rows.append(row)
    if not rows:
        raise ValueError("empty benchmark")
    return rows


def score(rows: list[dict], *, require_cache: bool = False) -> dict:
    arms = ARMS + ((COMPETITOR_ARM,) if require_cache else ())
    paired = defaultdict(dict)
    for r in rows:
        if r.get("cost_accounting_complete") is not True:
            raise ValueError("incomplete cost accounting; a raw pilot is not an economic benchmark")
        key = (r["task_id"], r["replicate"])
        if r["arm"] in paired[key]:
            raise ValueError(f"duplicate arm {r['arm']} for {key}")
        paired[key][r["arm"]] = r
    for key, group in paired.items():
        if set(group) != set(arms):
            raise ValueError(f"incomplete paired task {key}: expected {arms}, observed {sorted(group)}")
        if len({(r["family"], r["phase"]) for r in group.values()}) != 1:
            raise ValueError(f"family/phase mismatch for {key}")
    samples = {arm: [group[arm] for group in paired.values()] for arm in arms}
    stats = {}
    for arm, sample in samples.items():
        n = len(sample)
        successes = sum(r["success"] and r["safe"] for r in sample)
        costs = sum(r["cost_usd"] for r in sample)
        stats[arm] = {
            "n": n,
            "verified_safe_successes": successes,
            "safe_success_rate": successes / n,
            "unsafe_trials": sum(not r["safe"] for r in sample),
            "total_cost_usd": costs,
            "cost_per_safe_success_usd": costs / successes if successes else None,
            "mean_latency_ms": sum(r["latency_ms"] for r in sample) / n,
            "total_tokens": sum(r["tokens"] for r in sample),
        }
    comparator_rates = [stats[a]["safe_success_rate"] for a in ("COLD", "RETRIEVAL")]
    return {
        "status": "DESCRIPTIVE_ONLY_NOT_AN_AUDITED_PRODUCT_CLAIM",
        "paired_tasks": len(paired),
        "families": sorted({r["family"] for r in rows}),
        "phases": sorted({r["phase"] for r in rows}),
        "baseline_ceiling_warning": all(rate == 1 for rate in comparator_rates),
        "strong_cache_competitor_included": require_cache,
        "arms": stats,
        "note": "External-agent validation, task provenance, setup amortization and preregistration must be independently audited.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--require-cache", action="store_true", help="Require a genuine per-task fifth Stagehand/compiled-workflow baseline")
    args = ap.parse_args()
    result = score(read_trials(args.input), require_cache=args.require_cache)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
