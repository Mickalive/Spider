"""WP-003B-v2 §6 S0: within-site label-permutation chance calibration.

Descriptive only by preregistration (not part of the decision rule): gives,
per fold, the chance distribution of balanced accuracy for each FIXED
predictor vector when test labels are permuted within the site, i.e. what
score the site's class marginals alone make reachable.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from physics.run_wp003 import balanced_acc
from physics.run_wp003b_v2 import DEFAULT_IN, RESULTS_DIR, git_commit, load_rows, run_folds, t1_signature

N_PERM = 500
SEED = 20260825


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IN
    rows, stats = load_rows(path)
    folds, fold_raw, labels = run_folds(rows, t1_signature)
    rng = np.random.default_rng(SEED)
    out = {"analysis": "wp003b_v2_s0_permutation_calibration",
           "note": "descriptive calibration; NOT part of the decision rule",
           "n_perm": N_PERM, "seed": SEED,
           "input_sha256": None,
           "git_commit_at_analysis": git_commit(),
           "folds": {}}
    import hashlib
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    out["input_sha256"] = h
    for name, fr in zip(folds.keys(), fold_raw):
        y, pm = fr["yte"], fr["pm"]
        vals_m, vals_bestnull = [], []
        nulls = list(fr["nulls"].values())
        for _ in range(N_PERM):
            yp = rng.permutation(y)
            vals_m.append(balanced_acc(yp, pm, fr["classes"]))
            bn = max(balanced_acc(yp, p, fr["classes"]) for p in nulls)
            vals_bestnull.append(bn)
        out["folds"][name] = {
            "M_mean_chance": round(float(np.mean(vals_m)), 4),
            "M_p95_chance": round(float(np.percentile(vals_m, 95)), 4),
            "bestnull_mean_chance": round(float(np.mean(vals_bestnull)), 4),
            "bestnull_p95_chance": round(float(np.percentile(vals_bestnull, 95)), 4),
            "observed_M": folds[name]["M_model"],
            "observed_best_null": folds[name]["best_null"],
        }
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "wp003b_v2_s0_calibration.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out["folds"], indent=1))


if __name__ == "__main__":
    main()
