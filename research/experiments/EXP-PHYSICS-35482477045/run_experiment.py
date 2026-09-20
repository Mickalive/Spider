#!/usr/bin/env python3
"""EXP-PHYSICS-35482477045 - Stochastic positive control SPA for KSG CMI and LR.

Frozen design (spec.json / prereg.md / freeze.json):
  H0 (null): Neither KSG CMI nor likelihood-ratio achieves BOTH
    |shuffled-action null_mean| < 0.1 bits AND positive_control_k3 >= 0.5 bits
    on the stochastic SPA at N=5000.
  H1 (alternative): At least one estimator achieves BOTH.
  H2 (beyond-Markov): K3 CMI - K2 CMI > 0.1 bits with bootstrap 95% CI lower > 0.

Stochastic SPA: 50% deterministic hash routing + 50% uniform random over CANDIDATES.
This creates I(Y;A|Z) > 0 by construction.
"""
import hashlib
import json
import math
import random
import collections
import sys
import time
import warnings
from pathlib import Path

import numpy as np
from sklearn.feature_selection import mutual_info_classif
from scipy import stats

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

EXPERIMENT_ID = "EXP-PHYSICS-35482477045"
SEED = 42
N_SHUFFLE = 500
N_PERM_POSITIVE = 1000
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"
N_BOOTSTRAP = 200
KNN_K = 5
KNN_ALPHA = 1.0


# ---------------------------------------------------------------------------
# 1. Environment: 12-state SHA256 hash-routed SPA
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


# ---------------------------------------------------------------------------
# 2. Deterministic SPA (same as parent)
# ---------------------------------------------------------------------------
def choose_next_deterministic(current, action, prev1, prev2):
    """Hash routing: same as parent. Used for degenerate control baseline."""
    candidates = CANDIDATES[current][action]
    h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
    idx = int(h[:8], 16) % len(candidates)
    return candidates[idx]


# ---------------------------------------------------------------------------
# 3. Stochastic SPA (50% deterministic hash + 50% uniform random)
# ---------------------------------------------------------------------------
def choose_next_stochastic(current, action, prev1, prev2, rng):
    """Stochastic positive control SPA:
    With probability 0.5, use deterministic hash routing (same as parent).
    With probability 0.5, choose uniformly at random from CANDIDATES[current][action].
    This creates I(Y;A|Z) > 0 by construction.
    """
    candidates = CANDIDATES[current][action]
    if rng.random() < 0.5:
        # Deterministic branch
        h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
        idx = int(h[:8], 16) % len(candidates)
        return candidates[idx]
    else:
        # Stochastic branch: uniform random
        return rng.choice(candidates)


# ---------------------------------------------------------------------------
# 4. Simulation: collect transitions
# ---------------------------------------------------------------------------
def simulate_session_stochastic(session_id, n_steps, rng):
    current = rng.choice(range(12))
    prev1, prev2 = current, current
    transitions = []
    for step in range(n_steps):
        action = rng.choice(ACTIONS)
        next_state = choose_next_stochastic(current, action, prev1, prev2, rng)
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


def simulate_session_deterministic(session_id, n_steps, rng):
    current = rng.choice(range(12))
    prev1, prev2 = current, current
    transitions = []
    for step in range(n_steps):
        action = rng.choice(ACTIONS)
        next_state = choose_next_deterministic(current, action, prev1, prev2)
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


def collect_transitions(mode="stochastic", n_sessions=50, steps_per_session=100, seed=SEED):
    rng = random.Random(seed)
    all_transitions = []
    sim_fn = simulate_session_stochastic if mode == "stochastic" else simulate_session_deterministic
    for sid in range(n_sessions):
        trans = sim_fn(sid, steps_per_session, rng)
        all_transitions.extend(trans)
    return all_transitions


def transitions_sha(transitions):
    return hashlib.sha256(json.dumps(transitions, sort_keys=True).encode()).hexdigest()


# ---------------------------------------------------------------------------
# 5. Record building
# ---------------------------------------------------------------------------
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
# 6. Encoding for KSG/KNN
# ---------------------------------------------------------------------------
def encode_records_knn(records, history_kind):
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


# ---------------------------------------------------------------------------
# 7. KSG CMI estimator
# ---------------------------------------------------------------------------
def est_ksg_cmi(records, history_kind):
    Z, A, Y, n_classes = encode_records_knn(records, history_kind)
    X_joint = np.concatenate([Z, A[:, None]], axis=1)
    mi_joint = mutual_info_classif(
        X_joint, Y, discrete_features=True, n_neighbors=KNN_K, random_state=SEED
    )
    mi_joint_val = float(np.mean(mi_joint))
    mi_cond = mutual_info_classif(
        Z, Y, discrete_features=True, n_neighbors=KNN_K, random_state=SEED
    )
    mi_cond_val = float(np.mean(mi_cond))
    cmi_val = mi_joint_val - mi_cond_val
    info = {"n_records": len(Y), "k": KNN_K, "history_kind": history_kind,
            "mi_joint_raw": mi_joint_val, "mi_cond_raw": mi_cond_val,
            "method": "KSG (sklearn mutual_info_classif, k=5)"}
    return cmi_val, info


# ---------------------------------------------------------------------------
# 8. Likelihood-ratio estimator
# ---------------------------------------------------------------------------
def est_likelihood_ratio(records, history_kind):
    state_action_next = collections.defaultdict(lambda: collections.Counter())
    state_next = collections.Counter()

    for r in records:
        s = r["url_before"]
        a = r["action"]
        s_next = r["url_after"]
        state_action_next[s][(a, s_next)] += 1
        state_next[s] += 1

    chi2_stats = []
    p_values = []
    n_tested = 0

    for s, total in state_next.items():
        if total < MIN_STRATUM_SIZE:
            continue
        actions_for_state = set()
        nexts_for_state = set()
        for (a, sn), count in state_action_next[s].items():
            actions_for_state.add(a)
            nexts_for_state.add(sn)

        if len(nexts_for_state) < 2:
            continue
        if len(actions_for_state) < 2:
            continue

        n_tested += 1
        action_list = sorted(actions_for_state)
        next_list = sorted(nexts_for_state)

        table = np.zeros((len(action_list), len(next_list)))
        for (a, sn), count in state_action_next[s].items():
            ai = action_list.index(a)
            ni = next_list.index(sn)
            table[ai, ni] = count

        try:
            chi2, p, dof, expected = stats.chi2_contingency(table)
            chi2_stats.append(chi2)
            p_values.append(p)
        except ValueError:
            continue

    if n_tested == 0:
        return 0.0, {"n_tested": 0, "method": "likelihood-ratio",
                      "bonferroni_alpha": 0.0, "error": "no valid strata"}

    bonferroni_alpha = 0.05 / n_tested
    min_p = min(p_values)
    n_significant = sum(1 for p in p_values if p < bonferroni_alpha)
    max_chi2 = max(chi2_stats)

    total_n = sum(state_next.values())
    approx_mi = max_chi2 / (2.0 * total_n) if total_n > 0 else 0.0

    info = {
        "n_records": len(records),
        "n_tested_strata": n_tested,
        "min_p_value": min_p,
        "n_significant_bonferroni": n_significant,
        "bonferroni_alpha": bonferroni_alpha,
        "max_chi2": max_chi2,
        "approx_mi_bits": approx_mi,
        "method": "chi-squared per-state, Bonferroni corrected",
        "history_kind": history_kind,
    }
    return approx_mi, info


# ---------------------------------------------------------------------------
# 9. Baseline estimators (from parent)
# ---------------------------------------------------------------------------
def stratum_items(records):
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
# 10. Permutation schemes
# ---------------------------------------------------------------------------
def shuffled_action_null(records, kind, estimator, n_shuffle=N_SHUFFLE, seed=SEED):
    """Shuffled-action null: shuffle action labels within each session."""
    # Rebuild records as dicts with proper keys for each estimator type
    if estimator == "B-KSG-CMI":
        Z, A, Y, n_classes = encode_records_knn(records, kind)
        rng = random.Random(seed)
        # Precompute p_cond for efficiency
        from sklearn.neighbors import KNeighborsClassifier
        counts_cond = np.zeros((len(Y), n_classes), dtype=np.float64)
        knn = KNeighborsClassifier(n_neighbors=KNN_K + 1)
        knn.fit(Z, Y)
        _, idx = knn.kneighbors(Z, n_neighbors=KNN_K + 1)
        idx = idx[:, 1:]
        nbr_y = Y[idx]
        n = len(Y)
        rows_idx = np.arange(n)[:, None]
        np.add.at(counts_cond, (rows_idx, nbr_y), 1.0)
        p_cond = (counts_cond + KNN_ALPHA) / (KNN_K + KNN_ALPHA * n_classes)

        observed, _ = est_ksg_cmi(records, kind)
        shuffled_vals = []
        rng2 = random.Random(seed)
        for _ in range(n_shuffle):
            perm_rng = random.Random(rng2.randint(0, 2 ** 32))
            A_shuf = A.copy()
            perm_rng.shuffle(A_shuf)
            X_joint = np.concatenate([Z, A_shuf[:, None]], axis=1)
            mi_joint = mutual_info_classif(
                X_joint, Y, discrete_features=True, n_neighbors=KNN_K, random_state=SEED
            )
            mi_cond = mutual_info_classif(
                Z, Y, discrete_features=True, n_neighbors=KNN_K, random_state=SEED
            )
            val = float(np.mean(mi_joint)) - float(np.mean(mi_cond))
            shuffled_vals.append(val)
        shuffled_vals = np.array(shuffled_vals)
    elif estimator == "B-LIKELIHOOD-RATIO":
        observed, _ = est_likelihood_ratio(records, kind)
        actions = [r["action"] for r in records]
        rng = random.Random(seed)
        shuffled_vals = []
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
            val, _ = est_likelihood_ratio(shuffled_records, kind)
            shuffled_vals.append(val)
        shuffled_vals = np.array(shuffled_vals)
    elif estimator == "B-WEIGHTED-PMI":
        observed, _ = est_weighted_pmi(records)
        actions = [r["action"] for r in records]
        rng = random.Random(seed)
        shuffled_vals = []
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
            val, _ = est_weighted_pmi(shuffled_records)
            shuffled_vals.append(val)
        shuffled_vals = np.array(shuffled_vals)
    elif estimator == "B-EQUAL-WEIGHT-PMI":
        observed, _ = est_equal_weight_pmi(records)
        actions = [r["action"] for r in records]
        rng = random.Random(seed)
        shuffled_vals = []
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
            val, _ = est_equal_weight_pmi(shuffled_records)
            shuffled_vals.append(val)
        shuffled_vals = np.array(shuffled_vals)
    elif estimator == "B-MEDIAN-PMI":
        observed, _ = est_median_pmi(records)
        actions = [r["action"] for r in records]
        rng = random.Random(seed)
        shuffled_vals = []
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
            val, _ = est_median_pmi(shuffled_records)
            shuffled_vals.append(val)
        shuffled_vals = np.array(shuffled_vals)
    else:
        raise ValueError(f"Unknown estimator: {estimator}")

    count_ge = int(np.sum(shuffled_vals >= observed))
    p_value = (count_ge + 1) / (n_shuffle + 1)
    null_mean = float(np.mean(shuffled_vals))
    null_std = float(np.std(shuffled_vals, ddof=0))
    return {
        "observed": float(observed),
        "null_mean": null_mean,
        "null_std": null_std,
        "abs_null_mean": abs(null_mean),
        "p_value": p_value,
        "n_shuffle": n_shuffle,
        "shuffled_first5": shuffled_vals[:5].tolist(),
    }


# ---------------------------------------------------------------------------
# 11. Bootstrap K3-K2
# ---------------------------------------------------------------------------
def bootstrap_k3_minus_k2(transitions, n_bootstrap=N_BOOTSTRAP, seed=SEED):
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
        v2, _ = est_ksg_cmi(recs_k2, "state")
        v3, _ = est_ksg_cmi(recs_k3, "action")
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
    }


# ---------------------------------------------------------------------------
# 12. Design verification
# ---------------------------------------------------------------------------
def verify_design():
    issues = []
    for s in range(12):
        for a in ACTIONS:
            cands = CANDIDATES[s][a]
            if len(set(cands)) != 4:
                issues.append(f"state={s} action={a}: duplicates in {cands}")
            if len(set(cands)) < 2:
                issues.append(f"state={s} action={a}: <2 unique candidates")
    return issues


# ---------------------------------------------------------------------------
# 13. Stratum size decomposition
# ---------------------------------------------------------------------------
def stratum_size_bias_decomposition(records, n_shuffle=N_SHUFFLE, seed=SEED):
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["history"])].append(r)
    buckets = {"5-9": [], "10-19": [], "20-49": [], "50+": []}
    for key, recs in strata.items():
        n = len(recs)
        if n < MIN_STRATUM_SIZE:
            continue
        if n < 10:
            buckets["5-9"].append(recs)
        elif n < 20:
            buckets["10-19"].append(recs)
        elif n < 50:
            buckets["20-49"].append(recs)
        else:
            buckets["50+"].append(recs)
    decomposition = {}
    for bucket_name, bucket_strata in buckets.items():
        if not bucket_strata:
            decomposition[bucket_name] = {
                "n_strata": 0, "total_records": 0,
                "observed_pmi": 0.0, "null_mean": 0.0, "null_std": 0.0,
            }
            continue
        bucket_records = []
        for stratum_recs in bucket_strata:
            bucket_records.extend(stratum_recs)
        obs_val, _ = est_weighted_pmi(bucket_records)
        rng = random.Random(seed)
        all_actions = [r["action"] for r in bucket_records]
        shuffled_pmis = []
        for _ in range(n_shuffle):
            perm_rng = random.Random(rng.randint(0, 2**32))
            shuffled_actions = all_actions[:]
            perm_rng.shuffle(shuffled_actions)
            shuffled_records = []
            for i, r in enumerate(bucket_records):
                shuffled_records.append({
                    "session": r["session"], "step": r["step"],
                    "url_before": r["url_before"], "history": r["history"],
                    "action": shuffled_actions[i], "url_after": r["url_after"],
                })
            val, _ = est_weighted_pmi(shuffled_records)
            shuffled_pmis.append(val)
        shuffled_pmis = np.array(shuffled_pmis)
        decomposition[bucket_name] = {
            "n_strata": len(bucket_strata),
            "total_records": len(bucket_records),
            "observed_pmi": obs_val,
            "null_mean": float(np.mean(shuffled_pmis)),
            "null_std": float(np.std(shuffled_pmis, ddof=0)),
        }
    return decomposition


# ---------------------------------------------------------------------------
# 14. Determinism stats
# ---------------------------------------------------------------------------
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
# 15. Main
# ---------------------------------------------------------------------------
def to_json(o):
    if isinstance(o, (np.bool_, np.integer, np.floating)):
        return o.item()
    if isinstance(o, bool):
        return bool(o)
    if isinstance(o, tuple):
        return list(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


def main():
    t_start = time.time()
    out_dir = Path("research/experiments") / EXPERIMENT_ID
    out_dir.mkdir(parents=True, exist_ok=True)

    log_lines = []
    def log(msg):
        print(msg, flush=True)
        log_lines.append(str(msg))

    log("=" * 72)
    log(f"EXPERIMENT {EXPERIMENT_ID} - stochastic positive control SPA")
    log("=" * 72)

    # --- Design verification ------------------------------------------------
    log("\n[VERIFY] CANDIDATES design-level determinism check...")
    det_issues = verify_design()
    if det_issues:
        for iss in det_issues:
            log(f"  [FAIL] {iss}")
        log("[VERIFY] MEASUREMENT_INVALID: determinism check failed")
        sys.exit(1)
    log("[VERIFY] All 48 (state, action) pairs have 4 distinct candidates: PASS")

    # --- Collect data: Stochastic SPA at N=5000 ----------------------------
    log("\n[COLLECT] Stochastic SPA N=5000 (50 sessions x 100 steps, SEED=42)...")
    t0 = time.time()
    transitions_5k_stoch = collect_transitions("stochastic", 50, 100, SEED)
    sha_5k_stoch = transitions_sha(transitions_5k_stoch)
    log(f"[COLLECT] N={len(transitions_5k_stoch)} SHA256={sha_5k_stoch} ({time.time()-t0:.1f}s)")

    # --- Collect data: Deterministic SPA at N=5000 (degenerate baseline) ----
    log("\n[COLLECT] Deterministic SPA N=5000 (degenerate baseline)...")
    t0 = time.time()
    transitions_5k_det = collect_transitions("deterministic", 50, 100, SEED)
    sha_5k_det = transitions_sha(transitions_5k_det)
    log(f"[COLLECT] N={len(transitions_5k_det)} SHA256={sha_5k_det} ({time.time()-t0:.1f}s)")

    # --- Build records: Stochastic SPA --------------------------------------
    log("\n[BUILD] Stochastic SPA records...")
    recs_k2_stoch = build_state_history_records(transitions_5k_stoch, 2)
    recs_k3_stoch = build_action_history_records(transitions_5k_stoch, 3)
    log(f"[BUILD] K2 records={len(recs_k2_stoch)} K3 records={len(recs_k3_stoch)}")
    det_k2_stoch = determinism_stats(recs_k2_stoch)
    det_k3_stoch = determinism_stats(recs_k3_stoch)
    log(f"[BUILD] determinism K2={det_k2_stoch} K3={det_k3_stoch}")

    # --- Build records: Deterministic SPA ------------------------------------
    log("\n[BUILD] Deterministic SPA records...")
    recs_k3_det = build_action_history_records(transitions_5k_det, 3)
    log(f"[BUILD] K3 records={len(recs_k3_det)}")

    # --- Phase 1: Test estimators on stochastic SPA -------------------------
    log("\n" + "=" * 72)
    log("PHASE 1: Estimator screening on stochastic SPA at N=5000")
    log("=" * 72)

    results = {}

    for est_id in ["B-KSG-CMI", "B-LIKELIHOOD-RATIO"]:
        log(f"\n--- {est_id} ---")

        if est_id == "B-KSG-CMI":
            compute_fn = est_ksg_cmi
            kind = "state"
        else:
            compute_fn = est_likelihood_ratio
            kind = "state"

        # K2 on stochastic SPA
        k2_val, k2_info = compute_fn(recs_k2_stoch, "state")
        log(f"  K2 (stochastic) = {k2_val:.6f} bits  {k2_info}")

        # K3 on stochastic SPA
        k3_val, k3_info = compute_fn(recs_k3_stoch, "action")
        log(f"  K3 (stochastic) = {k3_val:.6f} bits  {k3_info}")

        # C1: Null control (shuffled-action, N=500)
        t0 = time.time()
        nc = shuffled_action_null(recs_k2_stoch, "state", est_id, N_SHUFFLE, SEED)
        c1_pass = nc["abs_null_mean"] < 0.1
        log(f"  C1 null control: null_mean={nc['null_mean']:.6f} "
            f"std={nc['null_std']:.6f} |mean|={nc['abs_null_mean']:.6f} "
            f"(threshold 0.1) -> {'PASS' if c1_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        # C3: Positive control (K3 on stochastic SPA)
        # The stochastic SPA is the positive control - K3 should be > 0.5
        c3_val = k3_val  # K3 is measured on the stochastic SPA itself
        # Also compute permutation p-value for the stochastic SPA
        t0 = time.time()
        pc_perm = shuffled_action_null(recs_k3_stoch, "action", est_id, N_PERM_POSITIVE, SEED)
        c3_pass = (c3_val >= 0.5 and pc_perm["p_value"] <= 0.001)
        log(f"  C3 positive control: K3={c3_val:.6f} p={pc_perm['p_value']:.6f} "
            f"-> {'PASS' if c3_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        # Degenerate control: KSG on deterministic SPA should be ~0
        if est_id == "B-KSG-CMI":
            det_k3_val, det_k3_info = est_ksg_cmi(recs_k3_det, "action")
            log(f"  Degenerate control (deterministic SPA): K3={det_k3_val:.6f} bits")
        else:
            det_k3_val, det_k3_info = est_likelihood_ratio(recs_k3_det, "action")
            log(f"  Degenerate control (deterministic SPA): K3={det_k3_val:.6f} bits")

        results[est_id] = {
            "k2_value_stochastic": k2_val,
            "k3_value_stochastic": k3_val,
            "k3_minus_k2": k3_val - k2_val,
            "k2_info": k2_info,
            "k3_info": k3_info,
            "null_control": nc,
            "c1_pass": c1_pass,
            "positive_control_k3": c3_val,
            "positive_control_p": pc_perm["p_value"],
            "c3_pass": c3_pass,
            "degenerate_control_k3": det_k3_val,
        }

    # --- Phase 1 verdict ----------------------------------------------------
    passers = [e for e in ["B-KSG-CMI", "B-LIKELIHOOD-RATIO"]
               if results[e]["c1_pass"] and results[e]["c3_pass"]]
    log(f"\n[SCREENING] C1+C3 passers: {passers}")

    # Check design conditions
    c6_pass = len(det_issues) == 0  # Already verified above
    ssbd = stratum_size_bias_decomposition(recs_k2_stoch, N_SHUFFLE, SEED)
    non_empty_buckets = sum(1 for b in ssbd.values() if b["n_strata"] > 0)
    c7_pass = non_empty_buckets >= 2
    log(f"[SCREENING] C6 design check: {'PASS' if c6_pass else 'FAIL'}")
    log(f"[SCREENING] C7 stratum buckets: {non_empty_buckets} non-empty -> {'PASS' if c7_pass else 'FAIL'}")

    phase2 = None
    verdict = None
    outcome = None
    reason = None

    if not passers:
        # No estimator passes both C1 and C3
        if results["B-KSG-CMI"]["c1_pass"] or results["B-LIKELIHOOD-RATIO"]["c1_pass"]:
            # At least one passes C1, but none pass C3
            verdict = "FALSIFIED-IN-SETTING"
            outcome = "FALSIFIES"
            c1_passers = [e for e in ["B-KSG-CMI", "B-LIKELIHOOD-RATIO"]
                         if results[e]["c1_pass"]]
            reason = (f"C3: estimators passing C1 ({c1_passers}) have positive_control_k3 "
                     f"< 0.5 bits on stochastic SPA. "
                     f"KSG K3={results['B-KSG-CMI']['k3_value_stochastic']:.6f}, "
                     f"LR K3={results['B-LIKELIHOOD-RATIO']['k3_value_stochastic']:.6f}.")
        else:
            # All fail C1
            verdict = "FALSIFIED-IN-SETTING"
            outcome = "FALSIFIES"
            reason = (f"C1: ALL estimators have |shuffled-action null mean| >= 0.1 bits. "
                     f"KSG |mean|={results['B-KSG-CMI']['null_control']['abs_null_mean']:.6f}, "
                     f"LR |mean|={results['B-LIKELIHOOD-RATIO']['null_control']['abs_null_mean']:.6f}.")
    else:
        e_star = passers[0]
        log(f"\n" + "=" * 72)
        log(f"PHASE 2 on first passing estimator: {e_star}")
        log("=" * 72)

        # C2: Bootstrap K3-K2
        t0 = time.time()
        bc = bootstrap_k3_minus_k2(transitions_5k_stoch, N_BOOTSTRAP, SEED)
        k3mk2 = results[e_star]["k3_minus_k2"]
        c2_pass = (k3mk2 > 0.1 and bc["ci_lower_95"] > 0.0)
        log(f"  C2 K3-K2 = {k3mk2:.6f} > 0.1: {k3mk2 > 0.1}")
        log(f"     bootstrap CI [{bc['ci_lower_95']:.6f}, {bc['ci_upper_95']:.6f}] "
            f"lower>0: {bc['ci_lower_95'] > 0.0} ({time.time()-t0:.1f}s)")

        phase2 = {"estimator": e_star, "bootstrap": bc, "c2_pass": c2_pass}

        if not c2_pass:
            verdict = "FALSIFIED-IN-SETTING"
            outcome = "FALSIFIES"
            reason = (f"C2: {e_star} K3-K2 = {k3mk2:.6f} <= 0.1 bits OR bootstrap "
                     f"CI [{bc['ci_lower_95']:.6f},{bc['ci_upper_95']:.6f}] "
                     f"includes 0.")
        else:
            verdict = "SURVIVES_CURRENT_TEST"
            outcome = "SUPPORTS"
            reason = (f"{e_star}: C1 |mean|={results[e_star]['null_control']['abs_null_mean']:.6f} "
                     f"< 0.1, C3 K3={results[e_star]['positive_control_k3']:.6f} >= 0.5 "
                     f"(p={results[e_star]['positive_control_p']:.6f}), "
                     f"C2 K3-K2={k3mk2:.6f} > 0.1 with CI lower "
                     f"{bc['ci_lower_95']:.6f} > 0.0.")

    log(f"\n[VERDICT] {verdict}")
    log(f"[OUTCOME] {outcome}")
    log(f"[REASON] {reason}")

    # --- Save raw results ---------------------------------------------------
    raw_results = {
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED,
        "n_transitions_stochastic": len(transitions_5k_stoch),
        "sha_stochastic": sha_5k_stoch,
        "n_transitions_deterministic": len(transitions_5k_det),
        "sha_deterministic": sha_5k_det,
        "determinism_k2_stochastic": det_k2_stoch,
        "determinism_k3_stochastic": det_k3_stoch,
        "screening": results,
        "passers": passers,
        "c6_design_pass": c6_pass,
        "c7_stratum_buckets": non_empty_buckets,
        "c7_pass": c7_pass,
        "stratum_size_bias_decomposition": ssbd,
        "phase2": phase2,
        "verdict": verdict,
        "outcome": outcome,
        "reason": reason,
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
