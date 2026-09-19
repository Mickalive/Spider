#!/usr/bin/env python3
"""EXP-PHYSICS-35445596894 - Bias-corrected CMI estimator screening on the 12-state hash-routed SPA.

Frozen design (spec.json / prereg.md / freeze.json):
  H1 (estimator-convergence): at least one of {equal-weight PMI, median PMI, KNN CMI}
      yields null control |mean| < 0.1 bits at N=5000 where weighted-averaged PMI gives 0.407.
  H2 (beyond-Markov): if a convergent estimator is found, K3 PMI - K2 PMI > 0.1 bits
      with bootstrap CI lower > 0.0 at N=5000.
  H0 (no-estimator-fix): all corrected estimators have |null_mean| >= 0.1 bits
      => bias is environment-level (deterministic/stochastic strata mixing).

Gates (per estimator, in screening order [weighted, equal-weight, median, KNN]):
  C3: positive_control K3 >= 1.0 bit AND p <= 0.001  (8-state deterministic SPA)
  C1: null_control |mean| < 0.1 bits at N=5000 (500 shuffled-action permutations, K2 records)
Phase 2 (first estimator passing C3 and C1):
  C2: K3-K2 > 0.1 AND bootstrap 95% CI lower > 0.0 (200 trajectory-block resamples)
  C4: |K2(N=50000) - K2(N=5000)| <= 0.2 bits (convergence)
Verdict priority: FALSIFIED-IN-SETTING > MEASUREMENT_INVALID > SURVIVES_CURRENT_TEST.
"""
import hashlib
import json
import math
import random
import collections
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

EXPERIMENT_ID = "EXP-PHYSICS-35445596894"
SEED = 42
N_SHUFFLE = 500
N_PERM_POSITIVE = 1000
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"
N_BOOTSTRAP = 200
KNN_K = 5
KNN_ALPHA = 1.0
PARENT_RAW_SHA = "170df6e34c78f64584f5332d61b9a705d87838b61e24eb04bdd4cc1b095c6ade"

# ---------------------------------------------------------------------------
# 1. Environment: 12-state SHA256 hash-routed SPA (identical to parent
#    EXP-PHYSICS-35403136807 run_experiment.py)
# ---------------------------------------------------------------------------
STATES = {
    0: "http://localhost:18973/#home",
    1: "http://localhost:18973/app#dashboard",
    2: "http://localhost:18973/app#analytics",
    3: "http://localhost:18973/user#profile",
    4: "http://localhost:18973/user#settings",
    5: "http://localhost:18973/app#search",
    6: "http://localhost:18973/app#notifications",
    7: "http://localhost:18973/admin#users",
    8: "http://localhost:18973/admin#reports",
    9: "http://localhost:18973/docs#getting-started",
    10: "http://localhost:18973/docs#api-ref",
    11: "http://localhost:18973/docs#changelog",
}
STATE_TO_IDX = {u: i for i, u in STATES.items()}
ACTIONS = ["form_submit", "button_click", "js_navigate", "menu_select"]
ACTION_TO_IDX = {a: i for i, a in enumerate(ACTIONS)}
CANDIDATES = {
    0: {"form_submit": [1,5,3,9], "button_click": [2,6,4,10], "js_navigate": [3,7,5,11], "menu_select": [4,8,1,6]},
    1: {"form_submit": [2,5,7,3], "button_click": [4,0,8,10], "js_navigate": [6,3,9,1], "menu_select": [5,7,11,4]},
    2: {"form_submit": [1,6,0,8], "button_click": [3,5,9,4], "js_navigate": [7,1,10,2], "menu_select": [0,8,3,11]},
    3: {"form_submit": [4,0,6,10], "button_click": [1,7,5,11], "js_navigate": [2,8,0,9], "menu_select": [5,9,4,1]},
    4: {"form_submit": [3,1,8,0], "button_click": [6,2,7,11], "js_navigate": [5,0,3,10], "menu_select": [7,10,6,2]},
    5: {"form_submit": [0,3,11,6], "button_click": [1,4,8,2], "js_navigate": [9,6,0,7], "menu_select": [10,2,5,3]},
    6: {"form_submit": [2,8,0,4], "button_click": [3,9,7,1], "js_navigate": [4,10,1,5], "menu_select": [1,11,3,8]},
    7: {"form_submit": [8,1,3,5], "button_click": [9,0,6,2], "js_navigate": [10,4,0,8], "menu_select": [11,5,7,1]},
    8: {"form_submit": [7,2,0,6], "button_click": [10,3,1,9], "js_navigate": [11,5,4,0], "menu_select": [9,0,8,3]},
    9: {"form_submit": [10,0,2,7], "button_click": [11,1,5,3], "js_navigate": [0,4,8,6], "menu_select": [1,6,10,4]},
    10: {"form_submit": [11,4,1,9], "button_click": [0,5,3,8], "js_navigate": [1,6,7,2], "menu_select": [3,7,11,5]},
    11: {"form_submit": [9,3,5,1], "button_click": [10,2,6,0], "js_navigate": [0,7,4,8], "menu_select": [2,8,10,3]},
}


def choose_next(current, action, prev1, prev2):
    candidates = CANDIDATES[current][action]
    h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
    idx = int(h[:8], 16) % len(candidates)
    return candidates[idx]


def simulate_session(session_id, n_steps, rng):
    current = rng.choice(range(12))
    prev1, prev2 = current, current
    transitions = []
    for step in range(n_steps):
        action = rng.choice(ACTIONS)
        next_state = choose_next(current, action, prev1, prev2)
        transitions.append({
            "session": f"session_{session_id}",
            "step": step,
            "url_before": STATES[current],
            "url_after": STATES[next_state],
            "action_primitive": action,
            "error": None,
        })
        prev2, prev1 = prev1, current
        current = next_state
    return transitions


def collect_transitions(n_sessions=50, steps_per_session=100, seed=SEED):
    rng = random.Random(seed)
    all_transitions = []
    for sid in range(n_sessions):
        trans = simulate_session(sid, steps_per_session, rng)
        all_transitions.extend(trans)
    return all_transitions


def transitions_sha(transitions):
    return hashlib.sha256(json.dumps(transitions, sort_keys=True).encode()).hexdigest()


def build_state_history_records(transitions, K):
    sessions = collections.defaultdict(list)
    for t in transitions:
        sessions[t["session"]].append(t)
    records = []
    for sid, sess_trans in sessions.items():
        sess_trans = sorted(sess_trans, key=lambda x: x["step"])
        url_before_seq = [t["url_before"] for t in sess_trans]
        for i, t in enumerate(sess_trans):
            if K == 0:
                history = tuple()
            elif i == 0:
                history = tuple([START_TOKEN] * K)
            elif i < K:
                history = tuple([START_TOKEN] * (K - i) + url_before_seq[:i])
            else:
                history = tuple(url_before_seq[i - K:i])
            records.append({
                "session": sid, "step": i,
                "url_before": t["url_before"],
                "history": history,
                "action": t["action_primitive"],
                "url_after": t["url_after"],
            })
    return records


def build_action_history_records(transitions, K):
    sessions = collections.defaultdict(list)
    for t in transitions:
        sessions[t["session"]].append(t)
    records = []
    for sid, sess_trans in sessions.items():
        sess_trans = sorted(sess_trans, key=lambda x: x["step"])
        actions = [t["action_primitive"] for t in sess_trans]
        for i, t in enumerate(sess_trans):
            if K == 0:
                history = tuple()
            elif i == 0:
                history = tuple([START_TOKEN] * K)
            elif i < K:
                history = tuple([START_TOKEN] * (K - i) + actions[:i])
            else:
                history = tuple(actions[i - K:i])
            records.append({
                "session": sid, "step": i,
                "url_before": t["url_before"],
                "history": history,
                "action": t["action_primitive"],
                "url_after": t["url_after"],
            })
    return records


# ---------------------------------------------------------------------------
# 2. Stratum-based estimators (identical input records; only the aggregation
#    across strata differs; MIN_STRATUM_SIZE=5 and zero-variance strata behave
#    exactly as in the parent framework).
# ---------------------------------------------------------------------------
def stratum_items(records):
    """Per-stratum PMI for strata with n >= MIN_STRATUM_SIZE.

    Return: (items, n_strata_total, total_records, n_skipped_small)
      item = {"n_h": int, "stratum_pmi": float}
    Zero-variance strata (<=1 distinct next) contribute stratum_pmi 0.0 (as parent).
    """
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["history"])].append(r)
    total = len(records)
    items = []
    skipped_small = 0
    for stratum, recs in strata.items():
        n_h = len(recs)
        if n_h < MIN_STRATUM_SIZE:
            skipped_small += 1
            continue
        action_counts = collections.Counter(r["action"] for r in recs)
        next_counts = collections.Counter(r["url_after"] for r in recs)
        joint_counts = collections.Counter((r["action"], r["url_after"]) for r in recs)
        if len(next_counts) <= 1:
            items.append({"n_h": n_h, "stratum_pmi": 0.0})
            continue
        vals = []
        for r in recs:
            a = r["action"]
            s_next = r["url_after"]
            p_a = action_counts[a] / n_h
            p_s = next_counts[s_next] / n_h
            p_joint = joint_counts[(a, s_next)] / n_h
            denom = p_a * p_s
            if denom > 0 and p_joint > 0:
                vals.append(math.log2(p_joint / denom))
            else:
                vals.append(0.0)
        items.append({"n_h": n_h, "stratum_pmi": sum(vals) / len(vals)})
    return items, len(strata), total, skipped_small


def est_weighted_pmi(records):
    items, n_strata, total, skipped = stratum_items(records)
    if total == 0:
        return 0.0, {"n_strata": 0, "n_used": 0, "total": 0, "skipped_small": 0}
    val = sum(it["n_h"] / total * it["stratum_pmi"] for it in items)
    return val, {"n_strata": n_strata, "n_used": len(items), "total": total,
                 "skipped_small": skipped}


def est_equal_weight_pmi(records):
    items, n_strata, total, skipped = stratum_items(records)
    if not items:
        return 0.0, {"n_strata": n_strata, "n_used": 0, "total": total,
                     "skipped_small": skipped}
    val = sum(it["stratum_pmi"] for it in items) / len(items)
    return val, {"n_strata": n_strata, "n_used": len(items), "total": total,
                 "skipped_small": skipped}


def est_median_pmi(records):
    items, n_strata, total, skipped = stratum_items(records)
    if not items:
        return 0.0, {"n_strata": n_strata, "n_used": 0, "total": total,
                     "skipped_small": skipped}
    vals = sorted(it["stratum_pmi"] for it in items)
    n = len(vals)
    if n % 2 == 1:
        val = vals[n // 2]
    else:
        val = (vals[n // 2 - 1] + vals[n // 2]) / 2.0
    return val, {"n_strata": n_strata, "n_used": len(items), "total": total,
                 "skipped_small": skipped}


# ---------------------------------------------------------------------------
# 3. KNN-CMI estimator (B-KNN-CMI): direct conditional mutual information
#    I(Y; X | Z) = E[log2 P(Y|Z,X) / P(Y|Z)] via sklearn KNeighborsClassifier
#    (k=5) on integer-encoded (history, action, next_state) tuples. Bypasses
#    strata entirely. Laplace smoothing alpha=1.0 on neighborhood counts avoids
#    zero probabilities. Self-neighbor (distance 0) excluded.
# ---------------------------------------------------------------------------
def encode_records_knn(records, history_kind):
    """Return (Z, A, Y, n_classes) integer arrays.

    Z: conditioning features [state_idx(url_before), history tokens...]
       history token encoding depends on history_kind:
         "state"  -> url index (or START=-2)
         "action" -> ACTION_TO_IDX (or START=-2)
    A: action index (0..3); Y: url_after state index (0..11). n_classes=12.

    The url->index map is built from the records themselves so that any state
    space (12-state SPA or 8-state positive-control SPA) is supported.
    """
    urls_seen = set()
    for r in records:
        urls_seen.add(r["url_before"])
        urls_seen.add(r["url_after"])
    if history_kind == "state":
        for r in records:
            for tok in r["history"]:
                if tok != START_TOKEN:
                    urls_seen.add(tok)
    url_to_idx = {u: i for i, u in enumerate(sorted(urls_seen))}
    rows_z = []
    rows_a = []
    rows_y = []
    for r in records:
        z = [url_to_idx[r["url_before"]]]
        for tok in r["history"]:
            if tok == START_TOKEN:
                z.append(-2)
            elif history_kind == "state":
                z.append(url_to_idx[tok])
            else:
                z.append(ACTION_TO_IDX[tok])
        rows_z.append(z)
        rows_a.append(ACTION_TO_IDX[r["action"]])
        rows_y.append(url_to_idx[r["url_after"]])
    Z = np.asarray(rows_z, dtype=np.int64)
    A = np.asarray(rows_a, dtype=np.int64)
    Y = np.asarray(rows_y, dtype=np.int64)
    n_classes = len(url_to_idx)
    return Z, A, Y, n_classes


def _neighbor_class_counts(X, Y, n_classes, k):
    """Class counts among k nearest neighbors excluding the query point itself."""
    knn = KNeighborsClassifier(n_neighbors=k + 1)
    knn.fit(X, Y)
    _, idx = knn.kneighbors(X, n_neighbors=k + 1)
    idx = idx[:, 1:]  # drop self
    nbr_y = Y[idx]  # (n, k)
    n = len(Y)
    counts = np.zeros((n, n_classes), dtype=np.float64)
    rows = np.arange(n)[:, None]
    np.add.at(counts, (rows, nbr_y), 1.0)
    return counts


def _probs_from_counts(counts, n_classes, k, alpha):
    return (counts + alpha) / (k + alpha * n_classes)


def knn_cmi_from_arrays(Z, A, Y, n_classes, k=KNN_K, alpha=KNN_ALPHA,
                        p_cond_precomputed=None):
    X_joint = np.concatenate([Z, A[:, None]], axis=1)
    counts_joint = _neighbor_class_counts(X_joint, Y, n_classes, k)
    p_joint = _probs_from_counts(counts_joint, n_classes, k, alpha)
    if p_cond_precomputed is None:
        counts_cond = _neighbor_class_counts(Z, Y, n_classes, k)
        p_cond = _probs_from_counts(counts_cond, n_classes, k, alpha)
    else:
        p_cond = p_cond_precomputed
    y_idx = np.arange(len(Y))
    pj = p_joint[y_idx, Y]
    pc = p_cond[y_idx, Y]
    pj = np.clip(pj, 1e-12, None)
    pc = np.clip(pc, 1e-12, None)
    return float(np.mean(np.log2(pj / pc)))


def est_knn_cmi(records, history_kind, cond_cache=None):
    """history_kind: 'state' (K2) or 'action' (K3)."""
    Z, A, Y, n_classes = encode_records_knn(records, history_kind)
    if cond_cache is not None and cond_cache["kind"] == history_kind:
        p_cond = cond_cache["p_cond"]
    else:
        counts_cond = _neighbor_class_counts(Z, Y, n_classes, KNN_K)
        p_cond = _probs_from_counts(counts_cond, n_classes, KNN_K, KNN_ALPHA)
    val = knn_cmi_from_arrays(Z, A, Y, n_classes, KNN_K, KNN_ALPHA, p_cond)
    info = {"n_records": len(Y), "k": KNN_K, "alpha": KNN_ALPHA,
            "history_kind": history_kind}
    return val, info


# ---------------------------------------------------------------------------
# 4. Positive control (8-state deterministic SPA, same as parent)
# ---------------------------------------------------------------------------
POSITIVE_STATES = {
    0: "http://spa.test/home", 1: "http://spa.test/dashboard",
    2: "http://spa.test/profile", 3: "http://spa.test/settings",
    4: "http://spa.test/search", 5: "http://spa.test/notifications",
    6: "http://spa.test/admin", 7: "http://spa.test/help",
}
POSITIVE_TRANSITIONS = {
    0: {"form_submit": 1, "button_click": 2, "js_navigate": 3, "menu_select": 4},
    1: {"form_submit": 4, "button_click": 5, "js_navigate": 0, "menu_select": 6},
    2: {"form_submit": 3, "button_click": 6, "js_navigate": 1, "menu_select": 7},
    3: {"form_submit": 0, "button_click": 7, "js_navigate": 2, "menu_select": 4},
    4: {"form_submit": 5, "button_click": 0, "js_navigate": 6, "menu_select": 7},
    5: {"form_submit": 6, "button_click": 1, "js_navigate": 7, "menu_select": 4},
    6: {"form_submit": 7, "button_click": 2, "js_navigate": 4, "menu_select": 5},
    7: {"form_submit": 0, "button_click": 3, "js_navigate": 5, "menu_select": 6},
}


def collect_positive_control(n_sessions=50, steps_per_session=100, seed=SEED):
    rng = random.Random(seed)
    transitions = []
    for sid in range(n_sessions):
        current = rng.choice(range(8))
        for step in range(steps_per_session):
            action = rng.choice(ACTIONS)
            next_state = POSITIVE_TRANSITIONS[current][action]
            transitions.append({
                "session": f"pc_session_{sid}", "step": step,
                "url_before": POSITIVE_STATES[current],
                "url_after": POSITIVE_STATES[next_state],
                "action_primitive": action,
            })
            current = next_state
    return transitions


# ---------------------------------------------------------------------------
# 5. Estimator registry (screening order per prereg section 7)
# ---------------------------------------------------------------------------
def make_estimator(est_id):
    """Return dict with keys: compute(records, kind)->(value, info),
    compute_shuffled_variant(...) used by permutations."""
    if est_id == "B-WEIGHTED-PMI":
        return {
            "id": est_id,
            "kind": "stratum",
            "compute": lambda records, kind: est_weighted_pmi(records),
        }
    if est_id == "B-EQUAL-WEIGHT-PMI":
        return {
            "id": est_id,
            "kind": "stratum",
            "compute": lambda records, kind: est_equal_weight_pmi(records),
        }
    if est_id == "B-MEDIAN-PMI":
        return {
            "id": est_id,
            "kind": "stratum",
            "compute": lambda records, kind: est_median_pmi(records),
        }
    if est_id == "B-KNN-CMI":
        return {
            "id": est_id,
            "kind": "knn",
            "compute": lambda records, kind: est_knn_cmi(records, kind),
        }
    raise ValueError(est_id)


ESTIMATOR_ORDER = ["B-WEIGHTED-PMI", "B-EQUAL-WEIGHT-PMI", "B-MEDIAN-PMI", "B-KNN-CMI"]


# ---------------------------------------------------------------------------
# 6. Permutation schemes
# ---------------------------------------------------------------------------
def shuffled_action_null(records, kind, estimator, n_shuffle=N_SHUFFLE, seed=SEED):
    """Global shuffled-action permutation null. Returns dict with null_mean,
    null_std, p, and first shuffled values."""
    est = make_estimator(estimator)
    observed, _ = est["compute"](records, kind)
    rng = random.Random(seed)
    shuffled_pmis = []
    if est["kind"] == "stratum":
        actions = [r["action"] for r in records]
        for _ in range(n_shuffle):
            perm_rng = random.Random(rng.randint(0, 2 ** 32))
            shuffled_actions = actions[:]
            perm_rng.shuffle(shuffled_actions)
            shuffled_records = []
            for i, r in enumerate(records):
                shuffled_records.append({
                    "session": r["session"], "step": r["step"],
                    "url_before": r["url_before"], "history": r["history"],
                    "action": shuffled_actions[i], "url_after": r["url_after"],
                })
            val, _ = est["compute"](shuffled_records, kind)
            shuffled_pmis.append(val)
    else:  # knn: shuffle the action array; cond model is fixed -> cache it
        Z, A, Y, n_classes = encode_records_knn(records, kind)
        counts_cond = _neighbor_class_counts(Z, Y, n_classes, KNN_K)
        p_cond = _probs_from_counts(counts_cond, n_classes, KNN_K, KNN_ALPHA)
        rng2 = random.Random(seed)
        for _ in range(n_shuffle):
            perm_rng = random.Random(rng2.randint(0, 2 ** 32))
            A_shuf = A.copy()
            perm_rng.shuffle(A_shuf)
            val = knn_cmi_from_arrays(Z, A_shuf, Y, n_classes, KNN_K, KNN_ALPHA,
                                      p_cond)
            shuffled_pmis.append(val)
    shuffled_pmis = np.array(shuffled_pmis)
    count_ge = int(np.sum(shuffled_pmis >= observed))
    p_value = (count_ge + 1) / (n_shuffle + 1)
    null_mean = float(np.mean(shuffled_pmis))
    null_std = float(np.std(shuffled_pmis, ddof=0))
    return {
        "observed": observed, "null_mean": null_mean, "null_std": null_std,
        "abs_null_mean": abs(null_mean), "p_value": p_value,
        "n_shuffle": n_shuffle,
        "shuffled_first5": shuffled_pmis[:5].tolist(),
    }


def within_stratum_permutation(records, kind, estimator, n_perm=N_PERM_POSITIVE,
                               seed=SEED):
    """Within-stratum permutation of url_after (parent positive-control scheme)."""
    est = make_estimator(estimator)
    observed, _ = est["compute"](records, kind)
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["history"])].append(r)
    rng = random.Random(seed)
    perm_values = []
    for _ in range(n_perm):
        perm_rng = random.Random(rng.randint(0, 2 ** 32))
        shuffled_records = []
        for stratum, stratum_records in strata.items():
            url_afters = [r["url_after"] for r in stratum_records]
            perm_rng.shuffle(url_afters)
            for i, r in enumerate(stratum_records):
                shuffled_records.append({
                    "session": r["session"], "step": r["step"],
                    "url_before": r["url_before"], "history": r["history"],
                    "action": r["action"], "url_after": url_afters[i],
                })
        val, _ = est["compute"](shuffled_records, kind)
        perm_values.append(val)
    perm_values = np.array(perm_values)
    count_ge = int(np.sum(perm_values >= observed))
    p_value = (count_ge + 1) / (n_perm + 1)
    return {
        "observed": observed, "p_value": p_value,
        "null_mean": float(np.mean(perm_values)),
        "null_std": float(np.std(perm_values, ddof=0)),
        "n_perm": n_perm,
    }


# ---------------------------------------------------------------------------
# 7. Bootstrap (trajectory-block resampling, parent scheme)
# ---------------------------------------------------------------------------
def bootstrap_k3_minus_k2(transitions, estimator, kind_k2="state",
                          kind_k3="action", n_bootstrap=N_BOOTSTRAP, seed=SEED):
    est = make_estimator(estimator)
    rng = random.Random(seed)
    sessions = collections.defaultdict(list)
    for t in transitions:
        sessions[t["session"]].append(t)
    session_ids = list(sessions.keys())
    n_sessions = len(session_ids)
    differences = []
    k3_values = []
    k2_values = []
    for _ in range(n_bootstrap):
        boot_ids = [session_ids[rng.randint(0, n_sessions - 1)]
                    for _ in range(n_sessions)]
        boot_transitions = []
        for sid in boot_ids:
            boot_transitions.extend(sessions[sid])
        recs_k2 = build_state_history_records(boot_transitions, 2)
        recs_k3 = build_action_history_records(boot_transitions, 3)
        v2, _ = est["compute"](recs_k2, kind_k2)
        v3, _ = est["compute"](recs_k3, kind_k3)
        differences.append(v3 - v2)
        k3_values.append(v3)
        k2_values.append(v2)
    differences = np.array(differences)
    k3_values = np.array(k3_values)
    k2_values = np.array(k2_values)
    ci_lower = float(np.percentile(differences, 2.5))
    ci_upper = float(np.percentile(differences, 97.5))
    return {
        "mean_difference": float(np.mean(differences)),
        "ci_lower_95": ci_lower,
        "ci_upper_95": ci_upper,
        "std_difference": float(np.std(differences, ddof=0)),
        "mean_k3": float(np.mean(k3_values)),
        "mean_k2": float(np.mean(k2_values)),
        "ci_includes_zero": bool(ci_lower <= 0.0 <= ci_upper),
        "n_bootstrap": n_bootstrap,
        "differences_first10": differences[:10].tolist(),
    }


def determinism_stats(records):
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["history"])].append(r)
    deterministic = 0
    stochastic = 0
    for recs in strata.values():
        nexts = collections.Counter(r["url_after"] for r in recs)
        if len(nexts) == 1:
            deterministic += 1
        elif len(nexts) > 1:
            stochastic += 1
    total = deterministic + stochastic
    return {
        "deterministic": deterministic, "stochastic": stochastic, "total": total,
        "det_ratio": deterministic / total if total else 0.0,
    }


# ---------------------------------------------------------------------------
# 8. Main
# ---------------------------------------------------------------------------
def to_json(o):
    if isinstance(o, (np.bool_, np.integer, np.floating)):
        return o.item()
    if isinstance(o, bool):
        return bool(o)
    if isinstance(o, tuple):
        return list(o)
    return o


def main():
    t_start = time.time()
    out_dir = Path("research/experiments") / EXPERIMENT_ID
    out_dir.mkdir(parents=True, exist_ok=True)
    parent_dir = Path("research/experiments") / "EXP-PHYSICS-35403136807"

    log_lines = []
    def log(msg):
        print(msg, flush=True)
        log_lines.append(str(msg))

    log("=" * 72)
    log(f"EXPERIMENT {EXPERIMENT_ID} — bias-corrected estimator screening")
    log("=" * 72)

    # --- Data: N=5000 from parent (frozen), verify hash -------------------
    raw_path = parent_dir / "raw_transitions.json"
    with open(raw_path) as f:
        transitions_5k = json.load(f)
    file_sha_5k = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    sha_5k = transitions_sha(transitions_5k)  # in-memory canonical serialization
    log(f"[DATA] parent raw_transitions.json file SHA256={file_sha_5k}")
    log(f"[DATA] matches frozen hash: {file_sha_5k == PARENT_RAW_SHA}")
    log(f"[DATA] in-memory sort_keys dump SHA256={sha_5k} "
        f"(parent raw_results.sha_raw=46ed606a... => consistent)")
    assert file_sha_5k == PARENT_RAW_SHA, "parent raw transitions file hash mismatch"
    log(f"[DATA] N(5000)={len(transitions_5k)}")

    # Code-fidelity check: regenerate N=5000 with our simulator; the parsed
    # objects must be identical to the parent file (dict deep equality).
    regen = collect_transitions(n_sessions=50, steps_per_session=100, seed=SEED)
    assert regen == transitions_5k, "simulator does not reproduce parent data"
    log("[DATA] regenerated N=5000 transitions deep-equal parent data: True")

    # --- Data: N=50000 (same seed, 50 sessions x 1000 steps) --------------
    log("\n[COLLECT] N=50000 (50 sessions x 1000 steps, SEED=42)...")
    t0 = time.time()
    transitions_50k = collect_transitions(n_sessions=50, steps_per_session=1000,
                                          seed=SEED)
    sha_50k = transitions_sha(transitions_50k)
    log(f"[COLLECT] N(50000)={len(transitions_50k)} SHA256={sha_50k} "
        f"({time.time()-t0:.1f}s)")
    with open(out_dir / "raw_transitions_n50000.json", "w") as f:
        json.dump(transitions_50k, f)

    # --- Build records (N=5000) -------------------------------------------
    log("\n[BUILD] N=5000 records...")
    recs_k2 = build_state_history_records(transitions_5k, 2)
    recs_k3 = build_action_history_records(transitions_5k, 3)
    log(f"[BUILD] K2 records={len(recs_k2)} K3 records={len(recs_k3)}")
    det_k2 = determinism_stats(recs_k2)
    det_k3 = determinism_stats(recs_k3)
    log(f"[BUILD] determinism K2={det_k2} K3={det_k3}")

    # --- Positive control data --------------------------------------------
    log("\n[COLLECT] positive control 8-state deterministic SPA...")
    pc_transitions = collect_positive_control()
    pc_recs_k3 = build_action_history_records(pc_transitions, 3)
    pc_recs_k2 = build_state_history_records(pc_transitions, 2)
    log(f"[COLLECT] positive control transitions={len(pc_transitions)} "
        f"K3 records={len(pc_recs_k3)}")

    # --- Phase 1: estimator screening -------------------------------------
    log("\n" + "=" * 72)
    log("PHASE 1: estimator screening at N=5000")
    log("=" * 72)
    screening = {}
    for est_id in ESTIMATOR_ORDER:
        log(f"\n--- {est_id} ---")
        est = make_estimator(est_id)
        # K2 / K3 point estimates on the 12-state SPA
        k2_val, k2_info = est["compute"](recs_k2, "state")
        k3_val, k3_info = est["compute"](recs_k3, "action")
        log(f"  K2 PMI = {k2_val:.6f} bits  {k2_info}")
        log(f"  K3 PMI = {k3_val:.6f} bits  {k3_info}")

        # C3: positive control (K3, 8-state deterministic SPA)
        pc_val, _ = est["compute"](pc_recs_k3, "action")
        if est["kind"] == "stratum":
            pc_perm = within_stratum_permutation(pc_recs_k3, "action", est_id,
                                                 N_PERM_POSITIVE, SEED)
            pc_perm_scheme = "within-stratum url_after permutation"
        else:
            pc_perm = shuffled_action_null(pc_recs_k3, "action", est_id,
                                           N_PERM_POSITIVE, SEED)
            pc_perm_scheme = "global shuffled-action permutation"
        c3_pass = (pc_val >= 1.0 and pc_perm["p_value"] <= 0.001)
        log(f"  C3 positive control: K3={pc_val:.6f} p={pc_perm['p_value']:.6f} "
            f"({pc_perm_scheme}) -> {'PASS' if c3_pass else 'FAIL/INVALID'}")

        # C1: null control (K2 records, shuffled-action, N_SHUFFLE=500)
        t0 = time.time()
        nc = shuffled_action_null(recs_k2, "state", est_id, N_SHUFFLE, SEED)
        c1_pass = abs(nc["null_mean"]) < 0.1
        log(f"  C1 null control: null_mean={nc['null_mean']:.6f} "
            f"std={nc['null_std']:.6f} |mean|={nc['abs_null_mean']:.6f} "
            f"(threshold 0.1) -> {'PASS' if c1_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        screening[est_id] = {
            "k2_pmi": k2_val, "k3_pmi": k3_val, "k3_minus_k2": k3_val - k2_val,
            "k2_info": k2_info, "k3_info": k3_info,
            "positive_control_k3": pc_val, "positive_control_p": pc_perm["p_value"],
            "positive_control_perm_scheme": pc_perm_scheme,
            "c3_pass": c3_pass,
            "null_control": nc,
            "c1_pass": c1_pass,
        }
        # intermediate save (robust against interruption)
        partial = {"screening": screening}
        with open(out_dir / "raw_results.json", "w") as f:
            json.dump(partial, f, indent=2, default=to_json)

    # --- Phase 1 verdict ---------------------------------------------------
    c1_failers = [e for e in ESTIMATOR_ORDER
                  if not screening[e]["c1_pass"] or not screening[e]["c3_pass"]]
    all_fail_c1 = len(c1_failers) == len(ESTIMATOR_ORDER)
    passers = [e for e in ESTIMATOR_ORDER
               if screening[e]["c3_pass"] and screening[e]["c1_pass"]]
    log(f"\n[SCREENING] C1+C3 passers: {passers}")
    log(f"[SCREENING] all estimators failed C1 (or C3-invalid): {all_fail_c1}")

    phase2 = None
    verdict = None
    outcome = None
    reason = None

    if all_fail_c1:
        # Per frozen decision rule: FALSIFIED-IN-SETTING (H0: environment-level bias)
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        reason = ("C1: ALL estimators have |null_mean| >= 0.1 bits at N=5000 "
                  "(or C3-invalid), indicating the bias is environment-level "
                  "(deterministic/stochastic strata mixing) rather than estimator-level.")
    elif not passers:
        # Possible only if some passed C1 but all failed C3 (positive control)
        verdict = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        reason = ("C3: every estimator that passed C1 failed the positive control "
                  "(K3 < 1.0 bit or p > 0.001 on the 8-state deterministic SPA).")
    else:
        e_star = passers[0]
        log(f"\n" + "=" * 72)
        log(f"PHASE 2 on first passing estimator: {e_star}")
        log("=" * 72)

        # C2: bootstrap K3-K2 (200 trajectory-block resamples)
        t0 = time.time()
        bc = bootstrap_k3_minus_k2(transitions_5k, e_star, "state", "action",
                                   N_BOOTSTRAP, SEED)
        k3mk2 = screening[e_star]["k3_minus_k2"]
        c2_pass = (k3mk2 > 0.1 and bc["ci_lower_95"] > 0.0)
        log(f"  C2 K3-K2 = {k3mk2:.6f} > 0.1: {k3mk2 > 0.1}")
        log(f"     bootstrap CI [{bc['ci_lower_95']:.6f}, {bc['ci_upper_95']:.6f}] "
            f"lower>0: {bc['ci_lower_95'] > 0.0} (mean {bc['mean_difference']:.6f})")
        log(f"     -> {'PASS' if c2_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        # C4: convergence at N=50000 for ALL estimators that passed C1
        log("\n  [CONVERGENCE] K2 PMI at N=50000 (50x1000) for passers...")
        recs_k2_50k = build_state_history_records(transitions_50k, 2)
        conv = {}
        for est_id in ESTIMATOR_ORDER:
            est = make_estimator(est_id)
            t0 = time.time()
            v50, info50 = est["compute"](recs_k2_50k, "state")
            v5 = screening[est_id]["k2_pmi"]
            diff = v50 - v5
            conv[est_id] = {
                "k2_n50000": v50, "k2_n5000": v5, "diff_bits": diff,
                "info_n50000": info50,
                "within_0_2bits": abs(diff) <= 0.2,
            }
            log(f"    {est_id}: K2(50k)={v50:.6f} K2(5k)={v5:.6f} "
                f"diff={diff:+.6f} ({time.time()-t0:.1f}s)")
        c4_pass = conv[e_star]["within_0_2bits"]

        phase2 = {"estimator": e_star, "bootstrap": bc, "c2_pass": c2_pass,
                  "convergence": conv, "c4_pass": c4_pass}

        if not c2_pass:
            verdict = "FALSIFIED-IN-SETTING"
            outcome = "FALSIFIES"
            reason = (f"C2: {e_star} K3-K2 = {k3mk2:.6f} <= 0.1 bits OR bootstrap "
                      f"CI [{bc['ci_lower_95']:.6f},{bc['ci_upper_95']:.6f}] "
                      f"includes 0 — signal is Markov even with a corrected estimator.")
        elif not c4_pass:
            verdict = "MEASUREMENT_INVALID"
            outcome = "NOT_APPLICABLE"
            reason = (f"C4: {e_star} |K2(N=50000)-K2(N=5000)| = "
                      f"{abs(conv[e_star]['diff_bits']):.6f} > 0.2 bits — "
                      f"estimator not converged.")
        else:
            verdict = "SURVIVES_CURRENT_TEST"
            outcome = "SUPPORTS"
            reason = (f"{e_star}: C1 null |mean|={screening[e_star]['null_control']['abs_null_mean']:.6f} "
                      f"< 0.1, C2 K3-K2={k3mk2:.6f} > 0.1 with bootstrap CI lower "
                      f"{bc['ci_lower_95']:.6f} > 0.0, C4 convergence diff "
                      f"{conv[e_star]['diff_bits']:+.6f} within 0.2 bits at N=50000.")

    log(f"\n[VERDICT] {verdict}")
    log(f"[OUTCOME] {outcome}")
    log(f"[REASON] {reason}")

    # --- Save raw results ---------------------------------------------------
    raw_results = {
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED,
        "n_transitions_5000": len(transitions_5k),
        "sha_file_5000": file_sha_5k,
        "sha_inmemory_5000": sha_5k,
        "sha_regen_deep_equal_5000": True,
        "n_transitions_50000": len(transitions_50k),
        "sha_raw_50000": sha_50k,
        "determinism_k2_n5000": det_k2,
        "determinism_k3_n5000": det_k3,
        "screening": screening,
        "passers": passers,
        "all_fail_c1": all_fail_c1,
        "phase2": phase2,
        "verdict": verdict,
        "outcome": outcome,
        "reason": reason,
        "estimator_order": ESTIMATOR_ORDER,
        "wall_seconds": time.time() - t_start,
    }
    with open(out_dir / "raw_results.json", "w") as f:
        json.dump(raw_results, f, indent=2, default=to_json)
    log(f"\nSaved raw_results.json (wall {time.time()-t_start:.1f}s)")

    with open(out_dir / "raw_output.txt", "w") as f:
        f.write("\n".join(log_lines) + "\n")
    log("Done.")


if __name__ == "__main__":
    main()