"""Anchor-clustered percentile bootstrap — the SINGLE shared estimator for
EXP-GRAPH-37992949248 (V12/V16).

V16 (ESTIMATOR-CONTROL-BINDING): PC-ESTIMATOR-NONDEGENERATE and
NC-ESTIMATOR-CONTROL-SENSITIVITY MUST be computed by the same bootstrap
function that computes M-PAIRED-FA-DIFF-D1V-LOW/-UB97; the code path is
identical (same B, same seed derivation, same resampling unit). This module is
that single code path; the runner never re-implements the bootstrap.

Resampling unit (V12): ANCHORS with replacement over the D1V-bearing anchors;
each resample pools the trials of the drawn anchors (pooled-cluster pooling,
identical to the parent packet); percentile method; B=10000; seed = the frozen
packet seed 37992949248 passed by the caller. Python process-randomized
hash() is never used as a seed or key (V09).

Degenerate bound semantics: with fewer than 2 anchors every resample is
identical, so LOW and UB97 are returned as null (never 0.0). With >= 2 anchors
the realized interval may still collapse to a point (LOW == UB97); that is a
zero-width degenerate interval, reported as such.
"""
from __future__ import annotations

import random

DEFAULT_B = 10000


def percentile(sorted_vals, q):
    """Nearest-rank percentile on an ascending-sorted list (parent-compatible:
    index = int(q/100 * n), clamped)."""
    if not sorted_vals:
        return None
    idx = int((q / 100.0) * len(sorted_vals))
    idx = max(0, min(len(sorted_vals) - 1, idx))
    return sorted_vals[idx]


def anchor_clustered_paired_fa_diff(
    trials,
    seed,
    B=DEFAULT_B,
    guard_i="B-INCUMBENT-SIGNAL-ONLY",
    guard_v="B-VALUE-AWARE",
):
    """Anchor-clustered percentile bootstrap of the paired false-accept
    difference P(REUSE | guard_i) - P(REUSE | guard_v) over D1V trials.

    Returns a dict:
      LOW            : 2.5th percentile of the paired-diff distribution
                       (null when degenerate-by-construction).
      UB97           : 97.5th percentile (null when degenerate-by-construction).
      fa_inc_ub97    : 97.5th percentile of the guard_i REUSE-rate marginal
                       (null when degenerate-by-construction).
      fa_va_ub97     : 97.5th percentile of the guard_v REUSE-rate marginal.
      degenerate     : True when n_anchors < 2 (null bound) or LOW == UB97.
      degenerate_reason : 'n_anchors<2' | 'zero_width_interval' | None.
      n_anchors, n_trials, B, seed, n_resamples : provenance of the computation.
    """
    anchors = sorted({t["anchor_id"] for t in trials})
    n_anchors = len(anchors)
    n_trials = len(trials)
    if n_anchors < 2:
        return {
            "LOW": None,
            "UB97": None,
            "fa_inc_ub97": None,
            "fa_va_ub97": None,
            "degenerate": True,
            "degenerate_reason": "n_anchors<2",
            "n_anchors": n_anchors,
            "n_trials": n_trials,
            "B": B,
            "seed": seed,
            "n_resamples": 0,
        }
    by_anchor = {a: [t for t in trials if t["anchor_id"] == a] for a in anchors}
    rng = random.Random(seed)
    inc_dist, va_dist, diff_dist = [], [], []
    for _ in range(B):
        sample = [rng.choice(anchors) for _ in range(n_anchors)]
        pooled = [t for a in sample for t in by_anchor[a]]
        if not pooled:
            continue
        pi = sum(1 for t in pooled if t[guard_i] == "REUSE") / len(pooled)
        pv = sum(1 for t in pooled if t[guard_v] == "REUSE") / len(pooled)
        inc_dist.append(pi)
        va_dist.append(pv)
        diff_dist.append(pi - pv)
    inc_dist.sort()
    va_dist.sort()
    diff_dist.sort()
    low = percentile(diff_dist, 2.5)
    ub = percentile(diff_dist, 97.5)
    degenerate = bool(low == ub)
    return {
        "LOW": low,
        "UB97": ub,
        "fa_inc_ub97": percentile(inc_dist, 97.5),
        "fa_va_ub97": percentile(va_dist, 97.5),
        "degenerate": degenerate,
        "degenerate_reason": "zero_width_interval" if degenerate else None,
        "n_anchors": n_anchors,
        "n_trials": n_trials,
        "B": B,
        "seed": seed,
        "n_resamples": len(diff_dist),
    }
