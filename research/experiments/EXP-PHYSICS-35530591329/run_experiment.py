#!/usr/bin/env python3
"""EXP-PHYSICS-35530591329 - Alpha sweep for plug-in KL on stochastic SPA.

Frozen design (spec.json / prereg.md / freeze.json):
  H0 (null): For all tested alpha values (0, 0.01, 0.1, 0.5, 1.0), plug-in KL
    fails to achieve BOTH |shuffled-action null_mean| < 0.1 bits AND
    positive_control_k3 >= 0.5 bits on the stochastic SPA at N=5000.
  H1 (alternative): At least one alpha achieves BOTH |null_mean| < 0.1 bits
    AND positive_control_k3 >= 0.5 bits on the stochastic SPA at N=5000.
  H2 (beyond-Markov, conditional on H1): K3 CMI - K2 CMI > 0.1 bits
    with bootstrap 95% CI lower > 0.0 at N=5000 for the best alpha passing C1+C3.

Stochastic SPA: 50% deterministic hash routing + 50% uniform random over CANDIDATES.
True I(Y;A|Z) ~ 1.52 bits (audit-confirmed from parent EXP-PHYSICS-35482477045).

Key difference from parent EXP-PHYSICS-35510154353:
  Parent tested alpha=1.0 only. This experiment tests alpha=0, 0.01, 0.1, 0.5, 1.0.
  Parent measured null_mean only for alpha=1.0; this measures for each alpha.
  This resolves whether reduced smoothing preserves null centering while
  recovering sensitivity.
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

EXPERIMENT_ID = "EXP-PHYSICS-35530591329"
SEED = 42
N_SHUFFLE = 500
N_PERM_POSITIVE = 1000
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"
N_BOOTSTRAP = 200
ALPHA_VALUES = [0, 0.01, 0.1, 0.5, 1.0]


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
# 6. Plug-in KL estimator with variable alpha
#    D_KL(P(Y|Z,A) || P(Y|Z)) = sum_{z,a,y} P(z,a,y) * log2[P(y|z,a)/P(y|z)]
#    with Laplace smoothing (alpha variable)
# ---------------------------------------------------------------------------
def est_plugin_kl(records, history_kind, alpha=1.0):
    """Compute I(Y;A;Z) = D_KL(P(Y|Z,A) || P(Y|Z)) on empirical transitions.

    alpha=0: MLE (no smoothing), may produce log(0) for empty cells.
    alpha>0: Laplace smoothing.
    """
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
    all_z = set(z_counts.keys())
    all_a = set(ACTIONS)
    all_y = set(r["url_after"] for r in records)

    n_z = len(all_z)
    n_a = len(all_a)
    n_y = len(all_y)

    # KL divergence with Laplace smoothing
    kl_div = 0.0
    if alpha > 0:
        n_smoothed = n_total + alpha * n_z * n_a * n_y
    else:
        n_smoothed = n_total  # MLE: no smoothing

    for z_key in all_z:
        for a in all_a:
            count_za = za_counts.get((z_key, a), 0)
            if count_za == 0 and alpha == 0:
                # MLE: if (z,a) never observed, P(y|z,a) undefined but P(z,a)=0
                # so contribution is 0*log2(...) = 0 by convention
                continue
            for y in all_y:
                count_joy = zay_counts.get((z_key, a, y), 0)
                p_joy = (count_joy + alpha) / n_smoothed

                if alpha > 0:
                    p_y_given_za = (count_joy + alpha) / (count_za + alpha * n_y)
                else:
                    # MLE: P(y|z,a) = count_joy / count_za (count_za > 0 here)
                    p_y_given_za = count_joy / count_za

                count_zy = zy_counts.get((z_key, y), 0)
                if alpha > 0:
                    p_y_given_z = (count_zy + alpha) / (z_counts[z_key] + alpha * n_y)
                else:
                    # MLE: P(y|z) = count_zy / z_counts[z_key]
                    p_y_given_z = count_zy / z_counts[z_key]

                if p_y_given_za > 0 and p_y_given_z > 0:
                    kl_div += p_joy * math.log2(p_y_given_za / p_y_given_z)

    info = {
        "n_records": n_total,
        "n_strata_z": n_z,
        "n_actions": n_a,
        "n_targets_y": n_y,
        "history_kind": history_kind,
        "method": f"plug-in KL (alpha={alpha})",
        "alpha": alpha,
    }
    return kl_div, info


# ---------------------------------------------------------------------------
# 7. Within-session shuffled-action null (for variable alpha)
# ---------------------------------------------------------------------------
def shuffled_action_null_within_session(records, kind, alpha, n_shuffle=N_SHUFFLE, seed=SEED):
    """Shuffle action labels within each session (preserving session structure)."""
    sessions = collections.defaultdict(list)
    for r in records:
        sessions[r["session"]].append(r)

    observed, _ = est_plugin_kl(records, kind, alpha=alpha)

    rng = random.Random(seed)
    shuffled_vals = []

    for _ in range(n_shuffle):
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

        val, _ = est_plugin_kl(shuffled_records, kind, alpha=alpha)
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
# 8. Bootstrap K3-K2 (for best alpha passing C1+C3)
# ---------------------------------------------------------------------------
def bootstrap_k3_minus_k2(transitions, alpha, n_bootstrap=N_BOOTSTRAP, seed=SEED):
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

        v2, _ = est_plugin_kl(recs_k2, "state", alpha=alpha)
        v3, _ = est_plugin_kl(recs_k3, "action", alpha=alpha)

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
# 9. Design verification
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
# 10. Stratum size decomposition
# ---------------------------------------------------------------------------
def stratum_size_bias_decomposition(records, alpha, n_shuffle=100, seed=SEED):
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
        obs_val, _ = est_plugin_kl(bucket_records, "state", alpha=alpha)
        rng = random.Random(seed)
        sessions = collections.defaultdict(list)
        for r in bucket_records:
            sessions[r["session"]].append(r)
        shuffled_vals = []
        for _ in range(min(n_shuffle, 100)):
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
            val, _ = est_plugin_kl(shuffled_records, "state", alpha=alpha)
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
# 11. Determinism stats
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
# 12. JSON serialization helper
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
# 13. Main
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
    log(f"EXPERIMENT {EXPERIMENT_ID} - alpha sweep for plug-in KL on stochastic SPA")
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
    # ALPHA SWEEP: For each alpha, measure C1 and C3
    # =========================================================================
    log("\n" + "=" * 72)
    log("ALPHA SWEEP: plug-in KL with alpha in {0, 0.01, 0.1, 0.5, 1.0}")
    log("=" * 72)

    results = {}
    for alpha in ALPHA_VALUES:
        alpha_label = f"alpha_{alpha}"
        log(f"\n--- alpha={alpha} ---")

        # K2 on stochastic SPA
        t0 = time.time()
        k2_val, k2_info = est_plugin_kl(recs_k2_stoch, "state", alpha=alpha)
        log(f"  K2 (stochastic) = {k2_val:.6f} bits ({time.time()-t0:.1f}s)")

        # K3 on stochastic SPA
        t0 = time.time()
        k3_val, k3_info = est_plugin_kl(recs_k3_stoch, "action", alpha=alpha)
        log(f"  K3 (stochastic) = {k3_val:.6f} bits ({time.time()-t0:.1f}s)")

        # C1: Null control (within-session shuffled-action, N=500)
        t0 = time.time()
        nc = shuffled_action_null_within_session(
            recs_k2_stoch, "state", alpha, N_SHUFFLE, SEED
        )
        c1_pass = nc["abs_null_mean"] < 0.1
        log(f"  C1 null control: null_mean={nc['null_mean']:.6f} "
            f"std={nc['null_std']:.6f} |mean|={nc['abs_null_mean']:.6f} "
            f"(threshold 0.1) -> {'PASS' if c1_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        # C3: Positive control (K3 on stochastic SPA, perm test on K3)
        c3_val = k3_val
        t0 = time.time()
        pc_perm = shuffled_action_null_within_session(
            recs_k3_stoch, "action", alpha, N_PERM_POSITIVE, SEED
        )
        c3_pass = (c3_val >= 0.5 and pc_perm["p_value"] <= 0.001)
        log(f"  C3 positive control: K3={c3_val:.6f} p={pc_perm['p_value']:.6f} "
            f"-> {'PASS' if c3_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        # Degenerate control: on deterministic SPA
        t0 = time.time()
        det_k3_val, det_k3_info = est_plugin_kl(recs_k3_det, "action", alpha=alpha)
        log(f"  Degenerate control (deterministic SPA): K3={det_k3_val:.6f} bits ({time.time()-t0:.1f}s)")

        results[alpha_label] = {
            "alpha": alpha,
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

    # --- Alpha sweep summary ------------------------------------------------
    c1_passers = [a for a in ALPHA_VALUES if results[f"alpha_{a}"]["c1_pass"]]
    c3_passers = [a for a in ALPHA_VALUES if results[f"alpha_{a}"]["c3_pass"]]
    both_passers = [a for a in ALPHA_VALUES
                    if results[f"alpha_{a}"]["c1_pass"] and results[f"alpha_{a}"]["c3_pass"]]
    log(f"\n[SCREENING] C1 passers: {c1_passers}")
    log(f"[SCREENING] C3 passers: {c3_passers}")
    log(f"[SCREENING] C1+C3 passers: {both_passers}")

    # --- C7: stratum size decomposition (using alpha=0.1 as representative) -
    ssbd = stratum_size_bias_decomposition(recs_k2_stoch, alpha=0.1, n_shuffle=100, seed=SEED)
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

    if both_passers:
        # At least one alpha passes both C1 and C3
        e_star_alpha = both_passers[0]
        log(f"\n" + "=" * 72)
        log(f"PHASE 2 on first passing alpha: {e_star_alpha}")
        log("=" * 72)

        # C2: Bootstrap K3-K2
        t0 = time.time()
        bc = bootstrap_k3_minus_k2(transitions_stoch, e_star_alpha, N_BOOTSTRAP, SEED)
        k3mk2 = results[f"alpha_{e_star_alpha}"]["k3_minus_k2"]
        c2_pass = (k3mk2 > 0.1 and bc["ci_lower_95"] > 0.0)
        log(f"  C2 K3-K2 = {k3mk2:.6f} > 0.1: {k3mk2 > 0.1}")
        log(f"     bootstrap CI [{bc['ci_lower_95']:.6f}, {bc['ci_upper_95']:.6f}] "
            f"lower>0: {bc['ci_lower_95'] > 0.0} ({time.time()-t0:.1f}s)")

        phase2 = {"alpha": e_star_alpha, "bootstrap": bc, "c2_pass": c2_pass}

        if not c2_pass:
            verdict = "FALSIFIED-IN-SETTING"
            outcome = "FALSIFIES"
            reason = (f"C2: alpha={e_star_alpha} K3-K2 = {k3mk2:.6f} <= 0.1 bits OR bootstrap "
                     f"CI [{bc['ci_lower_95']:.6f},{bc['ci_upper_95']:.6f}] "
                     f"includes 0.")
        else:
            verdict = "SURVIVES_CURRENT_TEST"
            outcome = "SUPPORTS"
            reason = (f"alpha={e_star_alpha}: C1 |mean|={results[f'alpha_{e_star_alpha}']['null_control']['abs_null_mean']:.6f} "
                     f"< 0.1, C3 K3={results[f'alpha_{e_star_alpha}']['positive_control_k3']:.6f} >= 0.5 "
                     f"(p={results[f'alpha_{e_star_alpha}']['positive_control_p']:.6f}), "
                     f"C2 K3-K2={k3mk2:.6f} > 0.1 with CI lower "
                     f"{bc['ci_lower_95']:.6f} > 0.0.")
    elif c1_passers:
        # At least one alpha passes C1, but none pass C3
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        # Find the best C3 among C1 passers
        best_c3 = max(c1_passers, key=lambda a: results[f"alpha_{a}"]["positive_control_k3"])
        reason = (f"C3: alphas passing C1 ({c1_passers}) have "
                 f"positive_control_k3 < 0.5 bits on stochastic SPA. "
                 f"Best: alpha={best_c3} K3={results[f'alpha_{best_c3}']['k3_value_stochastic']:.6f}.")
    else:
        # All fail C1
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        reason = (f"C1: ALL alpha values have |shuffled-action null mean| >= 0.1 bits. "
                 f"Values: " + ", ".join(
                     f"alpha={a} |mean|={results[f'alpha_{a}']['null_control']['abs_null_mean']:.6f}"
                     for a in ALPHA_VALUES) + ".")

    log(f"\n[VERDICT] {verdict}")
    log(f"[OUTCOME] {outcome}")
    log(f"[REASON] {reason}")

    # --- Save raw results ---------------------------------------------------
    raw_results = {
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED,
        "alpha_values_tested": ALPHA_VALUES,
        "n_transitions_stochastic": len(transitions_stoch),
        "sha_stochastic": sha_stoch,
        "n_transitions_deterministic": len(transitions_det),
        "sha_deterministic": sha_det,
        "determinism_k2_stochastic": det_k2_stoch,
        "determinism_k3_stochastic": det_k3_stoch,
        "alpha_sweep": results,
        "c1_passers": c1_passers,
        "c3_passers": c3_passers,
        "both_passers": both_passers,
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
