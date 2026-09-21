#!/usr/bin/env python3
"""EXP-PHYSICS-35572180485 - Bayesian model comparison on stochastic 12-state SPA.

Frozen design (spec.json / prereg.md / freeze.json):
  H0 (null): No tested prior specification achieves BOTH null centering
    (median < 0 nats) AND significant detection (p < 0.001) on the stochastic SPA.
  H1 (alternative): At least one tested prior specification achieves
    (a) null median < 0 nats AND (b) observed log BF on stochastic SPA
    exceeding the 99.9th percentile of the null distribution (p < 0.001).

Bayesian model comparison:
  Model M1 (action-dependent): P(S_next | S_current, A_current) with separate
    Dirichlet-Multinomial for each (state,action) pair.
  Model M0 (action-independent): P(S_next | S_current) with separate
    Dirichlet-Multinomial for each state.
  
  Exact log marginal likelihood under Dirichlet-Multinomial:
    log ML = sum_{cells} [lgamma(K*alpha) - lgamma(N_cell + K*alpha) + 
             sum_i (lgamma(n_i + alpha) - lgamma(alpha))]
  
  Log Bayes factor = log ML(M1) - log ML(M0) in nats.

Stochastic SPA: 50% deterministic hash routing + 50% uniform random over CANDIDATES.
True I(Y;A|Z) ~ 1.52 bits (audit-confirmed from parent EXP-PHYSICS-35530591329).
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

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

EXPERIMENT_ID = "EXP-PHYSICS-35572180485"
SEED = 42
N_SHUFFLE = 500
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"
N_BOOTSTRAP = 200
ALPHA_PRIOR_VALUES = [0.5, 1.0, 2.0]


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
# 2. Deterministic SPA (positive control baseline)
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
# 6. Bayesian Model Comparison (exact Dirichlet-Multinomial marginal likelihoods)
# ---------------------------------------------------------------------------
def _dirichlet_multinomial_log_marginal(counts, alpha=1.0):
    """Log marginal likelihood for Dirichlet-Multinomial.

    p(data | alpha) = Gamma(K*alpha) / Gamma(N + K*alpha) * prod_i Gamma(n_i + alpha) / Gamma(alpha)

    where K = number of categories, N = total count, n_i = category counts.
    """
    K = len(counts)
    N = sum(counts)
    log_ml = (math.lgamma(K * alpha) - math.lgamma(N + K * alpha))
    for ni in counts:
        log_ml += math.lgamma(ni + alpha) - math.lgamma(alpha)
    return log_ml


def est_bayesian_model_comparison(records, history_kind, alpha_prior=1.0):
    """Bayesian model comparison using exact Dirichlet-Multinomial marginal likelihoods.

    The model comparison depends on history_kind:
    
    - history_kind="state" (K2): 
        Full model: P(S_next | Z, A) where Z = (url_before, history[-2:])
        Reduced model: P(S_next | Z)
        Tests whether action provides information beyond state history.
    
    - history_kind="action" (K3):
        Full model: P(S_next | Z, A) where Z = (url_before, history[-3:])
        Reduced model: P(S_next | Z)
        Tests whether action provides information beyond action history.

    Compare via log Bayes factor = log ML(full) - log ML(reduced).
    If log BF > 0, full model is favored (action provides information).
    """
    # Build contingency tables using the history field as part of the conditioning variable
    full_tables = collections.defaultdict(lambda: collections.defaultdict(
        lambda: collections.Counter()))
    reduced_tables = collections.defaultdict(lambda: collections.Counter())

    for r in records:
        # Z = (url_before, history) - the full conditioning context
        z_key = (r["url_before"], r["history"])
        a = r["action"]
        s_next = r["url_after"]
        full_tables[z_key][a][s_next] += 1
        reduced_tables[z_key][s_next] += 1

    # Log marginal likelihood for full model
    log_ml_full = 0.0
    for z_key in full_tables:
        for a in full_tables[z_key]:
            counts = list(full_tables[z_key][a].values())
            log_ml_full += _dirichlet_multinomial_log_marginal(counts, alpha_prior)

    # Log marginal likelihood for reduced model
    log_ml_reduced = 0.0
    for z_key in reduced_tables:
        counts = list(reduced_tables[z_key].values())
        log_ml_reduced += _dirichlet_multinomial_log_marginal(counts, alpha_prior)

    log_bf = log_ml_full - log_ml_reduced

    # Parameter counts for diagnostics
    n_full_params = 0
    n_reduced_params = 0
    for z_key in full_tables:
        for a in full_tables[z_key]:
            K_za = len(full_tables[z_key][a])
            n_full_params += K_za - 1
        K_z = len(reduced_tables[z_key])
        n_reduced_params += K_z - 1

    info = {
        "n_records": len(records),
        "n_strata": len(reduced_tables),
        "log_ml_full": log_ml_full,
        "log_ml_reduced": log_ml_reduced,
        "log_bayes_factor": log_bf,
        "n_full_params": n_full_params,
        "n_reduced_params": n_reduced_params,
        "alpha_prior": alpha_prior,
        "history_kind": history_kind,
        "method": f"Dirichlet-Multinomial exact marginal likelihood (alpha={alpha_prior}, history={history_kind})",
    }
    return log_bf, info


# ---------------------------------------------------------------------------
# 7. Within-session shuffled-action null (for Bayesian model comparison)
# ---------------------------------------------------------------------------
def shuffled_action_null_within_session(records, kind, alpha_prior, n_shuffle=N_SHUFFLE, seed=SEED):
    """Shuffle action labels within each session (preserving session structure)."""
    sessions = collections.defaultdict(list)
    for r in records:
        sessions[r["session"]].append(r)

    observed, _ = est_bayesian_model_comparison(records, kind, alpha_prior)

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

        val, _ = est_bayesian_model_comparison(shuffled_records, kind, alpha_prior)
        shuffled_vals.append(val)

    shuffled_vals = np.array(shuffled_vals)
    # For Bayes factor, we want to check if observed > 99.9th percentile of null
    # Null should be centered negative (Occam's razor penalizes larger model)
    percentile_99_9 = float(np.percentile(shuffled_vals, 99.9))
    count_ge = int(np.sum(shuffled_vals >= observed))
    p_value = (count_ge + 1) / (n_shuffle + 1)
    null_median = float(np.median(shuffled_vals))
    null_mean = float(np.mean(shuffled_vals))
    null_std = float(np.std(shuffled_vals, ddof=0))
    return {
        "observed": float(observed),
        "null_median": null_median,
        "null_mean": null_mean,
        "null_std": null_std,
        "percentile_99_9": percentile_99_9,
        "p_value": p_value,
        "n_shuffle": n_shuffle,
        "shuffled_first5": shuffled_vals[:5].tolist(),
    }


# ---------------------------------------------------------------------------
# 8. Design verification
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
# 9. Stratum size decomposition
# ---------------------------------------------------------------------------
def stratum_size_bias_decomposition(records, alpha_prior, n_shuffle=100, seed=SEED):
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
                "observed_bf": 0.0, "null_mean": 0.0, "null_std": 0.0,
            }
            continue
        bucket_records = []
        for stratum_recs in bucket_strata:
            bucket_records.extend(stratum_recs)
        obs_val, _ = est_bayesian_model_comparison(bucket_records, "state", alpha_prior)
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
            val, _ = est_bayesian_model_comparison(shuffled_records, "state", alpha_prior)
            shuffled_vals.append(val)
        shuffled_bfs = np.array(shuffled_vals)
        decomposition[bucket_name] = {
            "n_strata": len(bucket_strata),
            "total_records": len(bucket_records),
            "observed_bf": obs_val,
            "null_mean": float(np.mean(shuffled_bfs)),
            "null_std": float(np.std(shuffled_bfs, ddof=0)),
        }
    return decomposition


# ---------------------------------------------------------------------------
# 10. Determinism stats
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
# 11. JSON serialization helper
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
# 12. Main
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
    log(f"EXPERIMENT {EXPERIMENT_ID} - Bayesian model comparison on stochastic SPA")
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

    # --- Collect data: Deterministic SPA (positive control) ------------------
    log("\n[COLLECT] Deterministic SPA N=5000 (positive control)...")
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
    recs_k2_det = build_state_history_records(transitions_det, 2)
    recs_k3_det = build_action_history_records(transitions_det, 3)
    log(f"[BUILD] K2 records={len(recs_k2_det)} K3 records={len(recs_k3_det)}")

    # =========================================================================
    # ALPHA PRIOR SWEEP: For each alpha_prior, measure C1 and C3
    # =========================================================================
    log("\n" + "=" * 72)
    log("ALPHA PRIOR SWEEP: Bayesian model comparison with alpha_prior in {0.5, 1.0, 2.0}")
    log("=" * 72)

    results = {}
    for alpha_prior in ALPHA_PRIOR_VALUES:
        alpha_label = f"alpha_{alpha_prior}"
        log(f"\n--- alpha_prior={alpha_prior} ---")

        # K2 on stochastic SPA
        t0 = time.time()
        k2_val, k2_info = est_bayesian_model_comparison(recs_k2_stoch, "state", alpha_prior)
        log(f"  K2 (stochastic) = {k2_val:.6f} nats ({time.time()-t0:.1f}s)")

        # K3 on stochastic SPA
        t0 = time.time()
        k3_val, k3_info = est_bayesian_model_comparison(recs_k3_stoch, "action", alpha_prior)
        log(f"  K3 (stochastic) = {k3_val:.6f} nats ({time.time()-t0:.1f}s)")

        # Deterministic SPA control (positive control)
        t0 = time.time()
        det_k2_val, det_k2_info = est_bayesian_model_comparison(recs_k2_det, "state", alpha_prior)
        det_k3_val, det_k3_info = est_bayesian_model_comparison(recs_k3_det, "action", alpha_prior)
        log(f"  Deterministic SPA control: K2={det_k2_val:.6f} K3={det_k3_val:.6f} nats ({time.time()-t0:.1f}s)")

        # C1: Null control (within-session shuffled-action, N=500)
        t0 = time.time()
        nc = shuffled_action_null_within_session(
            recs_k2_stoch, "state", alpha_prior, N_SHUFFLE, SEED
        )
        # C1: null median < 0 nats (Occam's razor penalizes larger model under null)
        c1_pass = nc["null_median"] < 0
        log(f"  C1 null control: null_median={nc['null_median']:.6f} "
            f"null_mean={nc['null_mean']:.6f} std={nc['null_std']:.6f} "
            f"(threshold median<0) -> {'PASS' if c1_pass else 'FAIL'} ({time.time()-t0:.1f}s)")

        # C3: Sensitivity (observed log BF exceeds 99.9th percentile of null)
        c3_pass = c1_pass and (k2_val > nc["percentile_99_9"])
        log(f"  C3 sensitivity: observed={k2_val:.6f} > 99.9th={nc['percentile_99_9']:.6f} "
            f"p={nc['p_value']:.6f} -> {'PASS' if c3_pass else 'FAIL'}")

        results[alpha_label] = {
            "alpha_prior": alpha_prior,
            "k2_value_stochastic": k2_val,
            "k3_value_stochastic": k3_val,
            "k3_minus_k2": k3_val - k2_val,
            "k2_info": k2_info,
            "k3_info": k3_info,
            "null_control": nc,
            "c1_pass": c1_pass,
            "c3_pass": c3_pass,
            "deterministic_control_k2": det_k2_val,
            "deterministic_control_k3": det_k3_val,
        }

    # --- Alpha prior sweep summary ------------------------------------------------
    c1_passers = [a for a in ALPHA_PRIOR_VALUES if results[f"alpha_{a}"]["c1_pass"]]
    c3_passers = [a for a in ALPHA_PRIOR_VALUES if results[f"alpha_{a}"]["c3_pass"]]
    both_passers = [a for a in ALPHA_PRIOR_VALUES
                    if results[f"alpha_{a}"]["c1_pass"] and results[f"alpha_{a}"]["c3_pass"]]
    log(f"\n[SCREENING] C1 passers (null median < 0): {c1_passers}")
    log(f"[SCREENING] C3 passers (p < 0.001): {c3_passers}")
    log(f"[SCREENING] C1+C3 passers: {both_passers}")

    # --- C7: stratum size decomposition (using alpha_prior=1.0 as representative) -
    ssbd = stratum_size_bias_decomposition(recs_k2_stoch, alpha_prior=1.0, n_shuffle=100, seed=SEED)
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
        # At least one alpha_prior passes both C1 and C3
        e_star_alpha = both_passers[0]
        log(f"\n" + "=" * 72)
        log(f"PHASE 2 on first passing alpha_prior: {e_star_alpha}")
        log("=" * 72)

        # Phase 2: K3 vs K2 comparison (beyond-Markov)
        k3mk2 = results[f"alpha_{e_star_alpha}"]["k3_minus_k2"]
        # Bootstrap K3-K2
        rng = random.Random(SEED)
        sessions = collections.defaultdict(list)
        for t in transitions_stoch:
            sessions[t["session"]].append(t)
        session_ids = list(sessions.keys())
        n_sessions = len(session_ids)
        differences = []
        k3_values = []
        k2_values = []
        for _ in range(N_BOOTSTRAP):
            boot_ids = [session_ids[rng.randint(0, n_sessions - 1)]
                        for _ in range(n_sessions)]
            boot_transitions = []
            for sid in boot_ids:
                boot_transitions.extend(sessions[sid])
            recs_k2_boot = build_state_history_records(boot_transitions, 2)
            recs_k3_boot = build_action_history_records(boot_transitions, 3)
            v2, _ = est_bayesian_model_comparison(recs_k2_boot, "state", e_star_alpha)
            v3, _ = est_bayesian_model_comparison(recs_k3_boot, "action", e_star_alpha)
            differences.append(v3 - v2)
            k3_values.append(v3)
            k2_values.append(v2)
        differences = np.array(differences)
        ci_lower = float(np.percentile(differences, 2.5))
        ci_upper = float(np.percentile(differences, 97.5))
        bc = {
            "mean_difference": float(np.mean(differences)),
            "ci_lower_95": ci_lower,
            "ci_upper_95": ci_upper,
            "std_difference": float(np.std(differences, ddof=0)),
            "mean_k3": float(np.mean(k3_values)),
            "mean_k2": float(np.mean(k2_values)),
            "ci_includes_zero": bool(ci_lower <= 0.0 <= ci_upper),
            "n_bootstrap": N_BOOTSTRAP,
        }

        # C2: K3-K2 > 0 with CI lower > 0
        c2_pass = (k3mk2 > 0 and bc["ci_lower_95"] > 0.0)
        log(f"  C2 K3-K2 = {k3mk2:.6f} > 0: {k3mk2 > 0}")
        log(f"     bootstrap CI [{bc['ci_lower_95']:.6f}, {bc['ci_upper_95']:.6f}] "
            f"lower>0: {bc['ci_lower_95'] > 0.0} ({time.time()-t0:.1f}s)")

        phase2 = {"alpha_prior": e_star_alpha, "bootstrap": bc, "c2_pass": c2_pass}

        if not c2_pass:
            verdict = "FALSIFIED-IN-SETTING"
            outcome = "FALSIFIES"
            reason = (f"C2: alpha_prior={e_star_alpha} K3-K2 = {k3mk2:.6f} <= 0 nats OR bootstrap "
                     f"CI [{bc['ci_lower_95']:.6f},{bc['ci_upper_95']:.6f}] "
                     f"includes 0.")
        else:
            verdict = "SURVIVES_CURRENT_TEST"
            outcome = "SUPPORTS"
            reason = (f"alpha_prior={e_star_alpha}: C1 null median={results[f'alpha_{e_star_alpha}']['null_control']['null_median']:.6f} "
                     f"< 0, C3 observed={results[f'alpha_{e_star_alpha}']['k2_value_stochastic']:.6f} > "
                     f"99.9th={results[f'alpha_{e_star_alpha}']['null_control']['percentile_99_9']:.6f} "
                     f"(p={results[f'alpha_{e_star_alpha}']['null_control']['p_value']:.6f}), "
                     f"C2 K3-K2={k3mk2:.6f} > 0 with CI lower "
                     f"{bc['ci_lower_95']:.6f} > 0.0.")
    elif c1_passers:
        # At least one alpha_prior passes C1, but none pass C3
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        best_c3 = max(c1_passers, key=lambda a: results[f"alpha_{a}"]["k2_value_stochastic"])
        reason = (f"C3: alpha_priors passing C1 ({c1_passers}) have "
                 f"observed log BF not exceeding 99.9th percentile of null on stochastic SPA. "
                 f"Best: alpha_prior={best_c3} log_bf={results[f'alpha_{best_c3}']['k2_value_stochastic']:.6f}.")
    else:
        # All fail C1
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        reason = (f"C1: ALL alpha_prior values have null median >= 0 nats (Occam's razor fails). "
                 f"Values: " + ", ".join(
                     f"alpha_prior={a} null_median={results[f'alpha_{a}']['null_control']['null_median']:.6f}"
                     for a in ALPHA_PRIOR_VALUES) + ".")

    log(f"\n[VERDICT] {verdict}")
    log(f"[OUTCOME] {outcome}")
    log(f"[REASON] {reason}")

    # --- Save raw results ---------------------------------------------------
    raw_results = {
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED,
        "alpha_prior_values_tested": ALPHA_PRIOR_VALUES,
        "n_transitions_stochastic": len(transitions_stoch),
        "sha_stochastic": sha_stoch,
        "n_transitions_deterministic": len(transitions_det),
        "sha_deterministic": sha_det,
        "determinism_k2_stochastic": det_k2_stoch,
        "determinism_k3_stochastic": det_k3_stoch,
        "alpha_prior_sweep": results,
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
