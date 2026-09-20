#!/usr/bin/env python3
"""EXP-PHYSICS-35510154353 - Alternative CMI estimators on stochastic SPA.

Frozen design (spec.json / prereg.md / freeze.json):
  H0 (null): Neither plug-in KL nor KSG k=10 achieves BOTH
    |shuffled-action null_mean| < 0.1 bits AND positive_control_k3 >= 0.5 bits
    on the stochastic SPA at N=5000.
  H1 (alternative): At least one estimator achieves BOTH.
  H2 (beyond-Markov, conditional on H1): K3 CMI - K2 CMI > 0.1 bits
    with bootstrap 95% CI lower > 0.0 at N=5000.

Stochastic SPA: 50% deterministic hash routing + 50% uniform random over CANDIDATES.
True I(Y;A|Z) ≈ 1.52 bits (audit-confirmed from parent EXP-PHYSICS-35482477045).

Key difference from parent: within-session shuffle (parent used global shuffle).
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

EXPERIMENT_ID = "EXP-PHYSICS-35510154353"
SEED = 42
N_SHUFFLE = 500
N_PERM_POSITIVE = 1000
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"
N_BOOTSTRAP = 200
LAPLACE_ALPHA = 1.0


# ---------------------------------------------------------------------------
# 1. Environment: 12-state SHA256 hash-routed SPA (identical to parent)
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
# 2. Deterministic SPA (degenerate control baseline)
# ---------------------------------------------------------------------------
def choose_next_deterministic(current, action, prev1, prev2):
    candidates = CANDIDATES[current][action]
    h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
    idx = int(h[:8], 16) % len(candidates)
    return candidates[idx]


# ---------------------------------------------------------------------------
# 3. Stochastic SPA (50% deterministic hash + 50% uniform random)
# ---------------------------------------------------------------------------
def choose_next_stochastic(current, action, prev1, prev2, rng):
    candidates = CANDIDATES[current][action]
    if rng.random() < 0.5:
        h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
        idx = int(h[:8], 16) % len(candidates)
        return candidates[idx]
    else:
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
# 5. Record building (state history K2 and action history K3)
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
# 7. KSG CMI estimator (parameterized k)
# ---------------------------------------------------------------------------
def est_ksg_cmi(records, history_kind, k=5):
    Z, A, Y, n_classes = encode_records_knn(records, history_kind)
    X_joint = np.concatenate([Z, A[:, None]], axis=1)
    mi_joint = mutual_info_classif(
        X_joint, Y, discrete_features=True, n_neighbors=k, random_state=SEED
    )
    mi_joint_val = float(np.mean(mi_joint))
    mi_cond = mutual_info_classif(
        Z, Y, discrete_features=True, n_neighbors=k, random_state=SEED
    )
    mi_cond_val = float(np.mean(mi_cond))
    cmi_val = mi_joint_val - mi_cond_val
    info = {"n_records": len(Y), "k": k, "history_kind": history_kind,
            "mi_joint_raw": mi_joint_val, "mi_cond_raw": mi_cond_val,
            "method": f"KSG (sklearn mutual_info_classif, k={k})"}
    return cmi_val, info


# ---------------------------------------------------------------------------
# 8. Plug-in transition-matrix KL divergence estimator
#    D_KL(P(Y|Z,A) || P(Y|Z)) = sum_{z,a,y} P(z,a,y) * log2[P(y|z,a)/P(y|z)]
#    with Laplace smoothing (alpha=1.0)
# ---------------------------------------------------------------------------
def est_plugin_kl(records, history_kind):
    """Compute I(Y;A;Z) = D_KL(P(Y|Z,A) || P(Y|Z)) on empirical transitions.

    This bypasses CMI estimation entirely: it works directly on the transition
    matrix with Laplace smoothing.
    """
    # Count transitions (z, a, y)
    zay_counts = collections.Counter()
    za_counts = collections.Counter()
    zy_counts = collections.Counter()
    z_counts = collections.Counter()

    for r in records:
        z_key = (r["url_before"], r["history"])
        a = r["action"]
        y = r["url_after"]
        zay_counts[(z_key, a, y)] += 1
        za_counts[(z_key, a)] += 1
        zy_counts[(z_key, y)] += 1
        z_counts[z_key] += 1

    n_total = len(records)
    alpha = LAPLACE_ALPHA

    # Collect all unique z, a, y values
    all_z = set(z_counts.keys())
    all_a = set(ACTIONS)
    all_y = set(r["url_after"] for r in records)

    n_z = len(all_z)
    n_a = len(all_a)
    n_y = len(all_y)

    # KL divergence with Laplace smoothing
    kl_div = 0.0
    n_smoothed = n_total + alpha * n_z * n_a * n_y  # total smoothed count

    for z_key in all_z:
        for a in all_a:
            for y in all_y:
                # Smoothed joint P(z,a,y)
                count_joy = zay_counts.get((z_key, a, y), 0)
                p_joy = (count_joy + alpha) / n_smoothed

                # Smoothed conditional P(y|z,a)
                count_za = za_counts.get((z_key, a), 0)
                p_y_given_za = (count_joy + alpha) / (count_za + alpha * n_y)

                # Smoothed conditional P(y|z)
                count_zy = zy_counts.get((z_key, y), 0)
                p_y_given_z = (count_zy + alpha) / (z_counts[z_key] + alpha * n_y)

                # KL term: P(z,a,y) * log2[P(y|z,a) / P(y|z)]
                if p_y_given_za > 0 and p_y_given_z > 0:
                    kl_div += p_joy * math.log2(p_y_given_za / p_y_given_z)

    info = {
        "n_records": n_total,
        "n_strata_z": n_z,
        "n_actions": n_a,
        "n_targets_y": n_y,
        "history_kind": history_kind,
        "method": f"plug-in KL (alpha={LAPLACE_ALPHA})",
    }
    return kl_div, info


# ---------------------------------------------------------------------------
# 9. Within-session shuffled-action null (correcting parent deviation)
# ---------------------------------------------------------------------------
def shuffled_action_null_within_session(records, kind, estimator_id, n_shuffle=N_SHUFFLE, seed=SEED):
    """Shuffle action labels within each session (preserving session structure)."""
    # Group records by session
    sessions = collections.defaultdict(list)
    for r in records:
        sessions[r["session"]].append(r)

    # Compute observed value
    if estimator_id == "B-PLUGIN-KL":
        observed, _ = est_plugin_kl(records, kind)
    elif estimator_id in ("B-KSG-CMI-K10", "B-KSG-CMI-K5", "B-KSG-CMI-K20"):
        k_map = {"B-KSG-CMI-K10": 10, "B-KSG-CMI-K5": 5, "B-KSG-CMI-K20": 20}
        observed, _ = est_ksg_cmi(records, kind, k=k_map[estimator_id])
    else:
        raise ValueError(f"Unknown estimator: {estimator_id}")

    rng = random.Random(seed)
    shuffled_vals = []

    for _ in range(n_shuffle):
        # For each session, shuffle action labels within that session
        shuffled_records = []
        for sid, sess_recs in sessions.items():
            sess_actions = [r["action"] for r in sess_recs]
            perm_rng = random.Random(rng.randint(0, 2**32))
            perm_rng.shuffle(sess_actions)
            for r, new_action in zip(sess_recs, sess_actions):
                shuffled_records.append({
                    "session": r["session"], "step": r["step"],
                    "url_before": r["url_before"], "history": r["history"],
                    "action": new_action, "url_after": r["url_after"],
                })

        if estimator_id == "B-PLUGIN-KL":
            val, _ = est_plugin_kl(shuffled_records, kind)
        elif estimator_id in ("B-KSG-CMI-K10", "B-KSG-CMI-K5", "B-KSG-CMI-K20"):
            k_map = {"B-KSG-CMI-K10": 10, "B-KSG-CMI-K5": 5, "B-KSG-CMI-K20": 20}
            val, _ = est_ksg_cmi(shuffled_records, kind, k=k_map[estimator_id])
        shuffled_vals.append(val)

    shuffled_vals = np.array(shuffled_vals)
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
# 10. Bootstrap K3-K2 (for best estimator passing C1+C3)
# ---------------------------------------------------------------------------
def bootstrap_k3_minus_k2(transitions, estimator_id, n_bootstrap=N_BOOTSTRAP, seed=SEED):
    rng = random.Random(seed)
    sessions = collections.defaultdict(list)
    for t in transitions:
        sessions[t["session"]].append(t)
    session_ids = list(sessions.keys())
    n_sessions = len(session_ids)
    differences = []
    k3_values = []
    k2_values = []

    k_map = {"B-PLUGIN-KL": None, "B-KSG-CMI-K10": 10, "B-KSG-CMI-K5": 5}

    for _ in range(n_bootstrap):
        boot_ids = [session_ids[rng.randint(0, n_sessions - 1)]
                    for _ in range(n_sessions)]
        boot_transitions = []
        for sid in boot_ids:
            boot_transitions.extend(sessions[sid])
        recs_k2 = build_state_history_records(boot_transitions, 2)
        recs_k3 = build_action_history_records(boot_transitions, 3)

        if estimator_id == "B-PLUGIN-KL":
            v2, _ = est_plugin_kl(recs_k2, "state")
            v3, _ = est_plugin_kl(recs_k3, "action")
        else:
            k = k_map.get(estimator_id, 10)
            v2, _ = est_ksg_cmi(recs_k2, "state", k=k)
            v3, _ = est_ksg_cmi(recs_k3, "action", k=k)

        differences.append(v3 - v2)
        k3_values.append(v3)
        k2_values.append(v2)

    differences = np.array(differences)
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
# 11. Permutation test (exploratory, conditioned on (state, action) strata)
# ---------------------------------------------------------------------------
def permutation_test_stratified(records, n_perms=500, seed=SEED):
    """For each (state, action) stratum with >=5 records, test whether observed
    action labels produce PMI significantly above shuffled-action null via
    within-session permutation."""
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["action"])].append(r)

    rng = random.Random(seed)
    stratum_results = []
    for (state, action), recs in strata.items():
        if len(recs) < MIN_STRATUM_SIZE:
            continue

        # Compute observed PMI for this stratum
        next_counts = collections.Counter(r["url_after"] for r in recs)
        n_h = len(recs)
        if len(next_counts) <= 1:
            stratum_results.append({
                "state": state, "action": action, "n": n_h,
                "pmi_observed": 0.0, "p_value": 1.0, "n_perms": 0,
                "degenerate": True,
            })
            continue

        # Observed: fraction of transitions to each next state
        obs_frac = {s: c / n_h for s, c in next_counts.items()}

        # Permutation null: shuffle action labels within session for this stratum
        # Since we're looking at a specific (state, action) stratum, we need to
        # compare against the marginal next-state distribution
        # Use overall next-state distribution as null
        all_next = collections.Counter(r["url_after"] for r in records)
        total_all = len(records)
        null_frac = {s: c / total_all for s, c in all_next.items()}

        # Compute PMI for observed
        pmi_obs = 0.0
        for s, f in obs_frac.items():
            p_null = null_frac.get(s, 1e-10)
            if f > 0:
                pmi_obs += f * math.log2(f / p_null)

        # Permutation: shuffle across all records (not just this stratum)
        perm_pmis = []
        for _ in range(n_perms):
            perm_rng = random.Random(rng.randint(0, 2**32))
            all_next_shuf = list(all_next.elements())
            perm_rng.shuffle(all_next_shuf)
            # Take the first n_h elements as the permuted next-state distribution
            perm_counts = collections.Counter(all_next_shuf[:n_h])
            perm_frac = {s: c / n_h for s, c in perm_counts.items()}
            pmi_perm = 0.0
            for s, f in perm_frac.items():
                p_null = null_frac.get(s, 1e-10)
                if f > 0:
                    pmi_perm += f * math.log2(f / p_null)
            perm_pmis.append(pmi_perm)

        perm_pmis = np.array(perm_pmis)
        p_value = float(np.sum(perm_pmis >= pmi_obs)) / n_perms

        stratum_results.append({
            "state": state, "action": action, "n": n_h,
            "pmi_observed": pmi_obs,
            "p_value": p_value,
            "n_perms": n_perms,
            "degenerate": False,
        })

    n_tested = len([r for r in stratum_results if not r["degenerate"]])
    n_significant = len([r for r in stratum_results
                         if not r["degenerate"] and r["p_value"] < 0.05 / max(n_tested, 1)])
    return {
        "n_strata_tested": n_tested,
        "n_significant_bonferroni": n_significant,
        "bonferroni_alpha": 0.05 / max(n_tested, 1),
        "stratum_results": stratum_results[:10],  # First 10 for brevity
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
        obs_val, _ = est_plugin_kl(bucket_records, "state")
        # Quick null for decomposition
        rng = random.Random(seed)
        sessions = collections.defaultdict(list)
        for r in bucket_records:
            sessions[r["session"]].append(r)
        shuffled_vals = []
        for _ in range(min(n_shuffle, 100)):  # Reduced for speed
            shuffled_records = []
            for sid, sess_recs in sessions.items():
                sess_actions = [r["action"] for r in sess_recs]
                perm_rng = random.Random(rng.randint(0, 2**32))
                perm_rng.shuffle(sess_actions)
                for r, new_action in zip(sess_recs, sess_actions):
                    shuffled_records.append({
                        "session": r["session"], "step": r["step"],
                        "url_before": r["url_before"], "history": r["history"],
                        "action": new_action, "url_after": r["url_after"],
                    })
            val, _ = est_plugin_kl(shuffled_records, "state")
            shuffled_vals.append(val)
        shuffled_pmis = np.array(shuffled_vals)
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
# 15. JSON serialization helper
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


# ---------------------------------------------------------------------------
# 16. Main
# ---------------------------------------------------------------------------
def main():
    t_start = time.time()
    out_dir = Path("research/experiments") / EXPERIMENT_ID
    out_dir.mkdir(parents=True, exist_ok=True)

    log_lines = []
    def log(msg):
        print(msg, flush=True)
        log_lines.append(str(msg))

    log("=" * 72)
    log(f"EXPERIMENT {EXPERIMENT_ID} - alternative CMI estimators on stochastic SPA")
    log("=" * 72)

    # --- Design verification ------------------------------------------------
    log("\n[VERIFY] CANDIDATES design-level check...")
    det_issues = verify_design()
    if det_issues:
        for iss in det_issues:
            log(f"  [FAIL] {iss}")
    c6_pass = len(det_issues) == 0
    log(f"[VERIFY] C6: {'PASS (48/48 pairs with 4 distinct candidates)' if c6_pass else 'FAIL'}")

    # --- Collect data: Stochastic SPA at N=5000 ----------------------------
    log("\n[COLLECT] Stochastic SPA N=5000 (50 sessions x 100 steps, SEED=42)...")
    t0 = time.time()
    transitions_stoch = collect_transitions("stochastic", 50, 100, SEED)
    sha_stoch = transitions_sha(transitions_stoch)
    log(f"[COLLECT] N={len(transitions_stoch)} SHA256={sha_stoch} ({time.time()-t0:.1f}s)")

    # --- Collect data: Deterministic SPA (degenerate baseline) ---------------
    log("\n[COLLECT] Deterministic SPA N=5000 (degenerate baseline)...")
    t0 = time.time()
    transitions_det = collect_transitions("deterministic", 50, 100, SEED)
    sha_det = transitions_sha(transitions_det)
    log(f"[COLLECT] N={len(transitions_det)} SHA256={sha_det} ({time.time()-t0:.1f}s)")

    # --- Build records: Stochastic SPA --------------------------------------
    log("\n[BUILD] Stochastic SPA records...")
    recs_k2_stoch = build_state_history_records(transitions_stoch, 2)
    recs_k3_stoch = build_action_history_records(transitions_stoch, 3)
    log(f"[BUILD] K2 records={len(recs_k2_stoch)} K3 records={len(recs_k3_stoch)}")
    det_k2_stoch = determinism_stats(recs_k2_stoch)
    det_k3_stoch = determinism_stats(recs_k3_stoch)
    log(f"[BUILD] determinism K2={det_k2_stoch} K3={det_k3_stoch}")

    # --- Build records: Deterministic SPA ------------------------------------
    log("\n[BUILD] Deterministic SPA records...")
    recs_k3_det = build_action_history_records(transitions_det, 3)
    log(f"[BUILD] K3 records={len(recs_k3_det)}")

    # =========================================================================
    # PHASE 1: Estimator screening on stochastic SPA at N=5000
    # =========================================================================
    log("\n" + "=" * 72)
    log("PHASE 1: Estimator screening on stochastic SPA at N=5000")
    log("=" * 72)

    PRIMARY_ESTIMATORS = ["B-PLUGIN-KL", "B-KSG-CMI-K10"]
    ALL_ESTIMATORS = PRIMARY_ESTIMATORS + ["B-KSG-CMI-K5", "B-KSG-CMI-K20"]
    results = {}

    for est_id in ALL_ESTIMATORS:
        log(f"\n--- {est_id} ---")

        # Select compute function
        if est_id == "B-PLUGIN-KL":
            compute_fn = lambda recs, kind: est_plugin_kl(recs, kind)
            k_label = "N/A (plug-in)"
        else:
            k_map = {"B-KSG-CMI-K5": 5, "B-KSG-CMI-K10": 10, "B-KSG-CMI-K20": 20}
            k = k_map[est_id]
            compute_fn = lambda recs, kind, k=k: est_ksg_cmi(recs, kind, k=k)
            k_label = str(k)

        # K2 on stochastic SPA
        k2_val, k2_info = compute_fn(recs_k2_stoch, "state")
        log(f"  K2 (stochastic) = {k2_val:.6f} bits")

        # K3 on stochastic SPA
        k3_val, k3_info = compute_fn(recs_k3_stoch, "action")
        log(f"  K3 (stochastic) = {k3_val:.6f} bits")

        # C1: Null control (within-session shuffled-action, N=500)
        t0 = time.time()
        nc = shuffled_action_null_within_session(
            recs_k2_stoch, "state", est_id, N_SHUFFLE, SEED
        )
        c1_pass = nc["abs_null_mean"] < 0.1
        log(f"  C1 null control: null_mean={nc['null_mean']:.6f} "
            f"std={nc['null_std']:.6f} |mean|={nc['abs_null_mean']:.6f} "
            f"(threshold 0.1) -> {'PASS' if c1_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        # C3: Positive control (K3 on stochastic SPA, perm test on K3)
        c3_val = k3_val
        t0 = time.time()
        pc_perm = shuffled_action_null_within_session(
            recs_k3_stoch, "action", est_id, N_PERM_POSITIVE, SEED
        )
        c3_pass = (c3_val >= 0.5 and pc_perm["p_value"] <= 0.001)
        log(f"  C3 positive control: K3={c3_val:.6f} p={pc_perm['p_value']:.6f} "
            f"-> {'PASS' if c3_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        # Degenerate control: on deterministic SPA
        if est_id == "B-PLUGIN-KL":
            det_k3_val, det_k3_info = est_plugin_kl(recs_k3_det, "action")
        else:
            k = k_map.get(est_id, 10)
            det_k3_val, det_k3_info = est_ksg_cmi(recs_k3_det, "action", k=k)
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
    primary_passers = [e for e in PRIMARY_ESTIMATORS
                       if results[e]["c1_pass"] and results[e]["c3_pass"]]
    all_passers = [e for e in ALL_ESTIMATORS
                   if results[e]["c1_pass"] and results[e]["c3_pass"]]
    log(f"\n[SCREENING] Primary C1+C3 passers: {primary_passers}")
    log(f"[SCREENING] All C1+C3 passers: {all_passers}")

    # Check C7: stratum size decomposition
    ssbd = stratum_size_bias_decomposition(recs_k2_stoch, N_SHUFFLE, SEED)
    non_empty_buckets = sum(1 for b in ssbd.values() if b["n_strata"] > 0)
    c7_pass = non_empty_buckets >= 2
    log(f"[SCREENING] C7 stratum buckets: {non_empty_buckets} non-empty -> {'PASS' if c7_pass else 'FAIL'}")

    # =========================================================================
    # Decision rule application
    # =========================================================================
    phase2 = None
    verdict = None
    outcome = None
    reason = None

    if not primary_passers:
        # Check if any primary passes C1
        c1_passers = [e for e in PRIMARY_ESTIMATORS if results[e]["c1_pass"]]
        if c1_passers:
            # At least one passes C1, but none pass C3
            verdict = "FALSIFIED-IN-SETTING"
            outcome = "FALSIFIES"
            reason = (f"C3: primary estimators passing C1 ({c1_passers}) have "
                     f"positive_control_k3 < 0.5 bits on stochastic SPA. "
                     f"Plug-in KL K3={results['B-PLUGIN-KL']['k3_value_stochastic']:.6f}, "
                     f"KSG k=10 K3={results['B-KSG-CMI-K10']['k3_value_stochastic']:.6f}.")
        else:
            # All fail C1
            verdict = "FALSIFIED-IN-SETTING"
            outcome = "FALSIFIES"
            reason = (f"C1: ALL primary estimators have |shuffled-action null mean| >= 0.1 bits. "
                     f"Plug-in KL |mean|={results['B-PLUGIN-KL']['null_control']['abs_null_mean']:.6f}, "
                     f"KSG k=10 |mean|={results['B-KSG-CMI-K10']['null_control']['abs_null_mean']:.6f}.")
    else:
        e_star = primary_passers[0]
        log(f"\n" + "=" * 72)
        log(f"PHASE 2 on first passing estimator: {e_star}")
        log("=" * 72)

        # C2: Bootstrap K3-K2
        t0 = time.time()
        bc = bootstrap_k3_minus_k2(transitions_stoch, e_star, N_BOOTSTRAP, SEED)
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

    # --- Exploratory: Permutation test ---------------------------------------
    log("\n" + "=" * 72)
    log("EXPLORATORY: Permutation test (stratified)")
    log("=" * 72)
    perm_test = permutation_test_stratified(recs_k3_stoch, 500, SEED)
    log(f"  Strata tested: {perm_test['n_strata_tested']}")
    log(f"  Significant (Bonferroni): {perm_test['n_significant_bonferroni']}")

    # --- Save raw results ---------------------------------------------------
    raw_results = {
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED,
        "n_transitions_stochastic": len(transitions_stoch),
        "sha_stochastic": sha_stoch,
        "n_transitions_deterministic": len(transitions_det),
        "sha_deterministic": sha_det,
        "determinism_k2_stochastic": det_k2_stoch,
        "determinism_k3_stochastic": det_k3_stoch,
        "screening": results,
        "primary_passers": primary_passers,
        "all_passers": all_passers,
        "c6_design_pass": c6_pass,
        "c7_stratum_buckets": non_empty_buckets,
        "c7_pass": c7_pass,
        "stratum_size_bias_decomposition": ssbd,
        "phase2": phase2,
        "permutation_test_exploratory": perm_test,
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
