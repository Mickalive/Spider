"""Frozen metric estimators for EXP-GRAPH-36279237023 + their unit tests.

prereg.md 14 requires the ECE estimator and the UNKNOWN-precision estimator to
be verified by unit test. Both tests run as part of experiment_runner.py before
any arm executes, and their results are logged as OBS-ESTIMATOR-UNIT-TESTS.

Definitions implemented here, verbatim from the frozen design:

  mechanism_identity_accuracy (prereg 6.1)
      over applicable goals: selected_mechanism_id == target_mechanism_id.
      An abstention (selected_mechanism_id is None) is an incorrect outcome,
      because the frozen definition compares the selected id to the target id.

  false_accept_rate (prereg 6.2)
      fraction of EXECUTABLE decisions whose selected_mechanism_id != the target
      mechanism id, pooled across all 80 goals. A goal with no applicable
      mechanism has target None, so any EXECUTABLE decision on such a goal is a
      false accept by construction.

  unknown_precision (prereg 6.2 / V6)
      TP_abstain / (TP_abstain + FP_abstain) with
        TP_abstain = no mechanism applies AND the arm abstained,
        FP_abstain = a mechanism applies AND the arm abstained.
      NOT an OOD abstention rate. When TP_abstain + FP_abstain == 0 the
      quantity is vacuous and is reported as 1.0 (prereg 4.7).

  ece (prereg 6.2 / V5)
      10 equal-mass bins, closed top bin, no rows dropped. Rows are sorted by
      confidence and split into 10 contiguous groups of near-equal size; the
      top bin is closed because it contains the highest ranks and every row is
      assigned to exactly one bin. For a class with fewer than 10 rows the bin
      count is min(10, n) and the binning actually used is logged.

  paired family-blocked bootstrap (prereg 6.1 / V10)
      10,000 resamples; the resampling unit is the resource family; candidate
      and null are evaluated on the SAME resampled goals; the statistic is the
      difference in mechanism_identity_accuracy; one-sided alpha = 0.05.
"""

from __future__ import annotations

import math
from typing import Any, Sequence

N_BOOTSTRAP = 10000
BOOTSTRAP_SEED = 36279237023
N_BINS = 10
HEADROOM_THRESHOLD = 0.90


# --- point estimates -------------------------------------------------------
def mechanism_identity_accuracy(rows: Sequence[dict], key: str = "selected") -> float:
    """rows: dicts with `correct` bool (already resolved)."""
    if not rows:
        return float("nan")
    return sum(1 for r in rows if r["correct"]) / len(rows)


def false_accept_rate(executable_rows: Sequence[dict]) -> float | None:
    if not executable_rows:
        return None
    return sum(1 for r in executable_rows if not r["correct"]) / len(executable_rows)


def unknown_precision(all_rows: Sequence[dict]) -> float | None:
    """V6 definition. `abstained` and `applies_any` per row."""
    tp = sum(1 for r in all_rows if r["abstained"] and not r["applies_any"])
    fp = sum(1 for r in all_rows if r["abstained"] and r["applies_any"])
    if tp + fp == 0:
        return 1.0  # vacuous, per prereg 4.7
    return tp / (tp + fp)


def ece(rows: Sequence[dict], n_bins: int = N_BINS) -> dict:
    """rows: dicts with `confidence` in [0,1] and `outcome` in {0,1}."""
    n = len(rows)
    if n == 0:
        return {"ece": None, "n": 0, "bins": [], "n_bins": 0, "note": "no rows"}
    k = min(n_bins, n)
    ordered = sorted(rows, key=lambda r: (r["confidence"], r.get("tiebreak", 0)))
    # equal-mass contiguous groups; every row lands in exactly one group
    sizes = [n // k] * k
    for i in range(n % k):
        sizes[i] += 1
    bins: list[dict] = []
    idx = 0
    for b in range(k):
        take = sizes[b]
        chunk = ordered[idx : idx + take]
        idx += take
        conf = sum(r["confidence"] for r in chunk) / take
        acc = sum(r["outcome"] for r in chunk) / take
        bins.append(
            {
                "bin": b,
                "n": take,
                "lo": chunk[0]["confidence"],
                "hi": chunk[-1]["confidence"],
                "mean_confidence": conf,
                "empirical_accuracy": acc,
                "gap": abs(conf - acc),
            }
        )
    value = sum(b["n"] * b["gap"] for b in bins) / n
    closed_top = bins[-1]
    return {
        "ece": value,
        "n": n,
        "n_bins": k,
        "bins": bins,
        "top_bin_closed": True,
        "top_bin_hi": closed_top["hi"],
        "rows_dropped": 0,
        "top_bin_contains_max_confidence": closed_top["hi"] == max(r["confidence"] for r in rows),
    }


# --- uncertainty -----------------------------------------------------------
def _blocks(rows: Sequence[dict]) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for i, r in enumerate(rows):
        out.setdefault(r["family"], []).append(i)
    return out


def paired_family_blocked_bootstrap(
    candidate_rows: Sequence[dict],
    null_rows: Sequence[dict],
    n_resamples: int = N_BOOTSTRAP,
    seed: int = BOOTSTRAP_SEED,
) -> dict:
    """Candidate and null must be row-aligned (same goals, same order)."""
    if len(candidate_rows) != len(null_rows):
        raise ValueError("paired bootstrap requires row-aligned arms")
    cand = [1.0 if r["correct"] else 0.0 for r in candidate_rows]
    null = [1.0 if r["correct"] else 0.0 for r in null_rows]
    blocks = _blocks(candidate_rows)
    keys = sorted(blocks)
    import random

    rng = random.Random(seed)
    diffs: list[float] = []
    for _ in range(n_resamples):
        picked: list[int] = []
        for _ in range(len(keys)):
            k = keys[rng.randrange(len(keys))]
            picked.extend(blocks[k])
        c = sum(cand[i] for i in picked) / len(picked)
        u = sum(null[i] for i in picked) / len(picked)
        diffs.append(c - u)
    diffs.sort()

    def q(p: float) -> float:
        if not diffs:
            return float("nan")
        idx = min(len(diffs) - 1, max(0, int(round(p * (len(diffs) - 1)))))
        return diffs[idx]

    point = mechanism_identity_accuracy(candidate_rows) - mechanism_identity_accuracy(null_rows)
    return {
        "n_resamples": n_resamples,
        "seed": seed,
        "n_blocks": len(keys),
        "blocks": keys,
        "rows_per_block": {k: len(blocks[k]) for k in keys},
        "point_estimate_difference": point,
        "one_sided_lower_95": q(0.05),
        "ci_lower_95_two_sided": q(0.025),
        "ci_upper_95_two_sided": q(0.975),
        "p_value_one_sided": sum(1 for d in diffs if d <= 0) / len(diffs),
        "passes_alpha_0_05_one_sided": q(0.05) > 0.0,
    }


def bootstrap_upper(rows: Sequence[dict], n_resamples: int = N_BOOTSTRAP, seed: int = BOOTSTRAP_SEED) -> dict:
    """Family-blocked bootstrap upper bound of a single-arm ECE."""
    import random

    blocks = _blocks(rows)
    keys = sorted(blocks)
    rng = random.Random(seed)
    values: list[float] = []
    for _ in range(n_resamples):
        picked: list[int] = []
        for _ in range(len(keys)):
            k = keys[rng.randrange(len(keys))]
            picked.extend(blocks[k])
        sub = [rows[i] for i in picked]
        out = ece(sub)
        if out["ece"] is not None:
            values.append(out["ece"])
    if not values:
        return {"upper_95": None, "n_resamples": 0, "note": "no valid resample"}
    values.sort()
    idx = min(len(values) - 1, max(0, int(round(0.95 * (len(values) - 1)))))
    return {
        "upper_95": values[idx],
        "point": ece(rows)["ece"],
        "n_resamples": n_resamples,
        "seed": seed,
        "n_blocks": len(keys),
    }


# --- unit tests required by prereg.md 14 ----------------------------------
def unit_tests() -> dict:
    results: dict[str, dict] = {}

    # 1. closed top bin: rows with confidence exactly 1.0 must be in the top bin
    rows = [{"confidence": 1.0, "outcome": 1}, {"confidence": 0.95, "outcome": 1}] + [
        {"confidence": c / 100, "outcome": 1} for c in range(90)
    ]
    out = ece(rows, n_bins=10)
    results["closed_top_bin"] = {
        "n_rows": len(rows),
        "rows_dropped": out["rows_dropped"],
        "top_bin_contains_confidence_1_0": out["top_bin_hi"] == 1.0,
        "top_bin_contains_max_confidence": out["top_bin_contains_max_confidence"],
        "pass": out["rows_dropped"] == 0
        and out["top_bin_hi"] == 1.0
        and out["top_bin_contains_max_confidence"],
    }

    # 2. hand-computed ECE cases
    #    all rows at confidence 1.0 with outcome 1 -> ECE 0
    #    all rows at confidence 1.0 with outcome 0 -> ECE 1
    #    5 rows (conf 1.0, outcome 1) + 5 rows (conf 0.0, outcome 0) -> ECE 0
    perfect = [{"confidence": 1.0, "outcome": 1} for _ in range(10)]
    wrong = [{"confidence": 1.0, "outcome": 0} for _ in range(10)]
    mixed = [{"confidence": 1.0, "outcome": 1} for _ in range(5)] + [
        {"confidence": 0.0, "outcome": 0} for _ in range(5)
    ]
    results["ece_perfect_zero"] = {"ece": ece(perfect)["ece"], "pass": abs(ece(perfect)["ece"]) < 1e-12}
    results["ece_worst_one"] = {"ece": ece(wrong)["ece"], "pass": abs(ece(wrong)["ece"] - 1.0) < 1e-12}
    results["ece_mixed_zero"] = {"ece": ece(mixed)["ece"], "pass": abs(ece(mixed)["ece"]) < 1e-12}
    # constant-confidence half-right case: confidence 0.5, half the outcomes correct
    half = [{"confidence": 0.5, "outcome": 1} for _ in range(5)] + [
        {"confidence": 0.5, "outcome": 0} for _ in range(5)
    ]
    results["ece_half_at_0_5"] = {"ece": ece(half)["ece"], "pass": abs(ece(half)["ece"] - 0.5) < 1e-12}

    # 3. UNKNOWN precision: hand-computed TP/FP case, NOT an OOD abstention rate
    sample = [
        {"abstained": True, "applies_any": False},   # TP
        {"abstained": True, "applies_any": False},   # TP
        {"abstained": True, "applies_any": False},   # TP
        {"abstained": True, "applies_any": True},    # FP
        {"abstained": False, "applies_any": True},   # no abstention -> ignored
        {"abstained": False, "applies_any": False},  # no abstention -> ignored
    ]
    got = unknown_precision(sample)
    results["unknown_precision_tp_fp"] = {
        "value": got,
        "expected": 0.75,
        "pass": abs(got - 0.75) < 1e-12,
    }
    results["unknown_precision_vacuous"] = {
        "value": unknown_precision([{"abstained": False, "applies_any": True}]),
        "pass": unknown_precision([{"abstained": False, "applies_any": True}]) == 1.0,
    }

    # 4. abstention on an applicable goal must not count as a true abstention
    anti = unknown_precision([{"abstained": True, "applies_any": True}])
    results["unknown_precision_not_ood_rate"] = {
        "value": anti,
        "expected": 0.0,
        "pass": anti == 0.0,
    }

    # 5. false_accept_rate counts only EXECUTABLE decisions
    fa = false_accept_rate([{"correct": True}, {"correct": False}, {"correct": False}])
    results["false_accept_rate"] = {"value": fa, "expected": 2 / 3, "pass": abs(fa - 2 / 3) < 1e-12}
    results["false_accept_rate_empty_is_null"] = {
        "value": false_accept_rate([]),
        "pass": false_accept_rate([]) is None,
    }

    # 6. paired family-blocked bootstrap is reproducible and family-blocked
    a = [
        {"family": "f1", "correct": True},
        {"family": "f1", "correct": True},
        {"family": "f2", "correct": False},
        {"family": "f2", "correct": True},
    ]
    b = [
        {"family": "f1", "correct": False},
        {"family": "f1", "correct": True},
        {"family": "f2", "correct": False},
        {"family": "f2", "correct": False},
    ]
    t1 = paired_family_blocked_bootstrap(a, b, n_resamples=500, seed=7)
    t2 = paired_family_blocked_bootstrap(a, b, n_resamples=500, seed=7)
    results["paired_bootstrap_reproducible"] = {
        "n_blocks": t1["n_blocks"],
        "pass": t1 == t2 and t1["n_blocks"] == 2,
    }

    return {
        "all_pass": all(v.get("pass") for v in results.values()),
        "checks": results,
    }


if __name__ == "__main__":
    import json

    out = unit_tests()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["all_pass"] else 1)
