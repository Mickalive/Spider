#!/usr/bin/env python3
"""Exploratory addendum for EXP-PHYSICS-35445596894 (non-gating, descriptive).

The frozen Phase 2 gates (C2 bootstrap, C4 convergence) are NOT triggered
because no estimator passed C1. This script adds purely descriptive evidence:
  1. K2 PMI at N=50000 for all four estimators (frozen design calls for the
     N=50000 collection; used as convergence-context documentation only).
  2. Per-stratum-size PMI bias decomposition under the shuffled-action null for
     the weighted estimator, to document WHY equal-weight/median bias is worse.
These measurements do not feed any frozen gate and do not change the verdict.
"""
import json
import random
import math
import collections
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

import run_experiment as rx

EXPERIMENT_ID = "EXP-PHYSICS-35445596894"
out_dir = Path("research/experiments") / EXPERIMENT_ID

# --- load raw results and N=50000 data -----------------------------------
raw = json.load(open(out_dir / "raw_results.json"))
transitions_50k = json.load(open(out_dir / "raw_transitions_n50000.json"))
print(f"N(50000) records: {len(transitions_50k)}")

recs_k2_50k = rx.build_state_history_records(transitions_50k, 2)
recs_k3_50k = rx.build_action_history_records(transitions_50k, 3)
print(f"K2 records(50k): {len(recs_k2_50k)}  K3 records(50k): {len(recs_k3_50k)}")

# --- 1. descriptive K2/K3 at N=50000 for all four estimators --------------
conv = {}
for est_id in rx.ESTIMATOR_ORDER:
    est = rx.make_estimator(est_id)
    v50_k2, info50_k2 = est["compute"](recs_k2_50k, "state")
    v50_k3, info50_k3 = est["compute"](recs_k3_50k, "action")
    v5_k2 = raw["screening"][est_id]["k2_pmi"]
    v5_k3 = raw["screening"][est_id]["k3_pmi"]
    conv[est_id] = {
        "k2_n50000": v50_k2, "k3_n50000": v50_k3,
        "k2_n5000": v5_k2, "k3_n5000": v5_k3,
        "k2_diff_50000_vs_5000": v50_k2 - v5_k2,
        "k3_diff_50000_vs_5000": v50_k3 - v5_k3,
        "k3_minus_k2_n50000": v50_k3 - v50_k2,
        "info_k2_n50000": info50_k2,
    }
    print(f"{est_id}: K2(50k)={v50_k2:.6f} (diff vs 5k {v50_k2 - v5_k2:+.6f}) "
          f"K3(50k)={v50_k3:.6f} (diff {v50_k3 - v5_k3:+.6f})")

# --- 2. per-stratum-size bias decomposition (weighted estimator, K2 null) --
# Bias per stratum under shuffled action labels, bucketed by stratum size.
recs_k2 = rx.build_state_history_records(
    json.load(open("research/experiments/EXP-PHYSICS-35403136807/raw_transitions.json")), 2)
N_SHUFFLE = 100
rng = random.Random(rx.SEED)
actions = [r["action"] for r in recs_k2]

# observed per-stratum PMI items (weighted framework)
items, n_strata, total, skipped = rx.stratum_items(recs_k2)

# null per-stratum PMI for each of N_SHUFFLE action shuffles
per_stratum_null = collections.defaultdict(list)  # n_h -> list of stratum pmi
for _ in range(N_SHUFFLE):
    perm_rng = random.Random(rng.randint(0, 2 ** 32))
    shuffled_actions = actions[:]
    perm_rng.shuffle(shuffled_actions)
    shuffled_records = []
    for i, r in enumerate(recs_k2):
        shuffled_records.append({
            "session": r["session"], "step": r["step"],
            "url_before": r["url_before"], "history": r["history"],
            "action": shuffled_actions[i], "url_after": r["url_after"],
        })
    # recompute per-stratum PMIs for the shuffled records, grouped by n_h
    strata = collections.defaultdict(list)
    for r in shuffled_records:
        strata[(r["url_before"], r["history"])].append(r)
    for stratum, recs in strata.items():
        n_h = len(recs)
        if n_h < rx.MIN_STRATUM_SIZE:
            continue
        action_counts = collections.Counter(r["action"] for r in recs)
        next_counts = collections.Counter(r["url_after"] for r in recs)
        joint_counts = collections.Counter((r["action"], r["url_after"]) for r in recs)
        if len(next_counts) <= 1:
            pmi = 0.0
        else:
            vals = []
            for r in recs:
                a, s = r["action"], r["url_after"]
                p_a = action_counts[a] / n_h
                p_s = next_counts[s] / n_h
                p_j = joint_counts[(a, s)] / n_h
                vals.append(math.log2(p_j / (p_a * p_s)))
            pmi = sum(vals) / len(vals)
        per_stratum_null[n_h].append(pmi)

buckets = {}
for n_h, pmis in sorted(per_stratum_null.items()):
    b = "5-9" if n_h < 10 else ("10-19" if n_h < 20 else ("20-49" if n_h < 50 else "50+"))
    buckets.setdefault(b, []).extend(pmis)
bias_by_bucket = {
    b: {"n_stratum_obs": len(vals),
        "mean_null_stratum_pmi": float(np.mean(vals)),
        "median_null_stratum_pmi": float(np.median(vals))}
    for b, vals in sorted(buckets.items())
}
print("\nPer-stratum-size null bias (weighted framework, 100 shuffles, K2):")
for b, d in bias_by_bucket.items():
    print(f"  size {b}: n_obs={d['n_stratum_obs']:6d} "
          f"mean_null_pmi={d['mean_null_stratum_pmi']:+.4f} "
          f"median={d['median_null_stratum_pmi']:+.4f}")

expl = {
    "experiment_id": EXPERIMENT_ID,
    "role": "exploratory-descriptive-non-gating",
    "n50000_descriptive": conv,
    "stratum_size_bias_buckets": bias_by_bucket,
    "n_shuffle_bias_decomposition": N_SHUFFLE,
    "note": ("NOT part of the frozen measurement plan. Frozen gates C2/C4 are "
             "not applicable because no estimator passed C1 at N=5000."),
}
with open(out_dir / "raw_exploratory.json", "w") as f:
    json.dump(expl, f, indent=2)
print("\nSaved raw_exploratory.json")