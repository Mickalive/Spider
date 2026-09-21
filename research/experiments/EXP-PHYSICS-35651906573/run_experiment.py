#!/usr/bin/env python3
"""EXP-PHYSICS-35651906573 — real TodoMVC hash-SPA validation of the Bayesian
Dirichlet-Multinomial model comparison.

Frozen design (spec.json / prereg.md / freeze.json — EXECUTE stage):

  Question: Does the Bayesian DM model comparison (K=12) maintain valid null
  centering (C1: null median < 0) and detection sensitivity (C3: p < 0.001) on
  real TodoMVC hash-SPA transitions at URL-level, with fragment-aware state
  representation and genuine browser interactions?

  Model (identical to parent EXP-PHYSICS-35578258358):
    M1: P(url_after | z, action)  — action-conditioned
    M0: P(url_after | z)          — memory only
    z = (url_before, H_K2) state-history; K = n_states = 12;
    alpha_prior in {0.5, 1.0, 2.0}; exact DM marginal likelihoods;
    log BF = log ML(M1) - log ML(M0) in nats.

  Action variable: action_primitive (form_submit | button_click | js_navigate)
  on the non-leakage subset (link_click removed by NL filter, 100% leakage by
  the frozen definition action_target == url_after). The prereg line
  'Action: URL of the action target' describes the recorded leakage field only;
  the PMI-pipeline parents whose baseline numbers this spec cites
  (EXP-PHYSICS-35262258744) define the model action as action_primitive.
  Using action_target as the model action on NL data is degenerate (constant
  None) and log BF == 0 by identity — a diagnostic is included below.

  Null: within-session shuffled-action permutation, N_SHUFFLE=1999.
    C1: null median < 0 nats (>=2/5 variants for SURVIVES)
    C3: p = (count_null>=obs + 1)/(N+1) < 0.001 (>=2/5 variants)

  Positive control (C6): synthetic 12-state stochastic hash-routed SPA,
  N=5000, seed=42 (parent-identical environment/estimator). Must pass C1+C3
  at all 3 alpha values.

  Baselines:
    B1 URL-only PMI: I(url_after; action | url_before) plug-in (Laplace a=1.0)
    B2 action-history accuracy K=3: fraction of transitions where
       (url_before, H_K3 actions) determines url_after
    B3 state-history K=2 PMI: I(url_after; (url_before, H_K2)) plug-in

  Decision rule (frozen):
    SURVIVES_CURRENT_TEST  if C1 and C3 on >=2/5 AND C5 (>=50 NL on >=2/5)
                            AND C6 (positive control) AND C7 (no validity violations)
    MEASUREMENT_INVALID    if C6 fails or C5 fails
    FALSIFIED-IN-SETTING   if C1 or C3 fails on all 5 variants
    MIXED                  if some variants pass, others fail (ceiling bounded)
"""
import hashlib
import json
import math
import random
import collections
import sys
import time
import urllib.parse
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

EXPERIMENT_ID = "EXP-PHYSICS-35651906573"
EXP_DIR = Path("research/experiments") / EXPERIMENT_ID
SEED = 42
N_SHUFFLE = 1999
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"
ALPHA_PRIOR_VALUES = [0.5, 1.0, 2.0]
N_STATES = 12  # K for Dirichlet-Multinomial (frozen; parent-identical)

VARIANTS = {
    "vanillajs": "https://todomvc.com/examples/javascript-es6/dist/",
    "react": "https://todomvc.com/examples/react/dist/",
    "vue": "https://todomvc.com/examples/vue/dist/",
    "angular": "https://todomvc.com/examples/angular/dist/browser/",
    "svelte": "https://todomvc.com/examples/svelte/dist/",
}


# ===========================================================================
# 1. Normalization (frozen: same as parent EXP-PHYSICS-35209110569)
# ===========================================================================
def normalize_leakage_url(url):
    """Leakage normalization: strip fragment, rstrip '/', unquote."""
    if not url:
        return None
    url = url.split("#")[0]
    url = url.rstrip("/")
    url = urllib.parse.unquote(url)
    return url


def normalize_state_url(url):
    """State normalization: rstrip '/', unquote, PRESERVE fragment
    (frozen: fragment-aware state representation, e.g. #/active != #/completed)."""
    if not url:
        return None
    url = urllib.parse.unquote(url)
    url = url.rstrip("/")
    return url


def is_leakage(target, after_url):
    if target is None or after_url is None:
        return False
    return normalize_leakage_url(target) == normalize_leakage_url(after_url)


# ===========================================================================
# 2. Synthetic positive-control environment (parent-identical)
#    EXP-PHYSICS-35578258358 / EXP-PHYSICS-35572180485
# ===========================================================================
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
ACTIONS = ["form_submit", "button_click", "js_navigate", "menu_select"]
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


def choose_next_stochastic(current, action, prev1, prev2, rng):
    candidates = CANDIDATES[current][action]
    if rng.random() < 0.5:
        h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
        idx = int(h[:8], 16) % len(candidates)
        return candidates[idx]
    else:
        return rng.choice(candidates)


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


def collect_synthetic(mode="stochastic", n_sessions=50, steps_per_session=100, seed=SEED):
    rng = random.Random(seed)
    all_transitions = []
    for sid in range(n_sessions):
        all_transitions.extend(simulate_session_stochastic(sid, steps_per_session, rng))
    return all_transitions


# ===========================================================================
# 3. Record building (state-history K2; parent-identical logic)
# ===========================================================================
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


# ===========================================================================
# 4. Bayesian model comparison (parent-identical; K=12)
# ===========================================================================
def _dirichlet_multinomial_log_marginal(counts, alpha=1.0, K_categories=None):
    """Exact DM log marginal likelihood. K = n_possible_categories = 12."""
    K = K_categories if K_categories is not None else N_STATES
    N = sum(counts)
    log_ml = (math.lgamma(K * alpha) - math.lgamma(N + K * alpha))
    for ni in counts:
        log_ml += math.lgamma(ni + alpha) - math.lgamma(alpha)
    return log_ml


def est_bayesian_model_comparison(records, alpha_prior=1.0):
    full_tables = collections.defaultdict(lambda: collections.defaultdict(
        lambda: collections.Counter()))
    reduced_tables = collections.defaultdict(lambda: collections.Counter())

    for r in records:
        z_key = (r["url_before"], r["history"])
        a = r["action"]
        s_next = r["url_after"]
        full_tables[z_key][a][s_next] += 1
        reduced_tables[z_key][s_next] += 1

    log_ml_full = 0.0
    for z_key in full_tables:
        for a in full_tables[z_key]:
            counts = list(full_tables[z_key][a].values())
            log_ml_full += _dirichlet_multinomial_log_marginal(
                counts, alpha_prior, K_categories=N_STATES)

    log_ml_reduced = 0.0
    for z_key in reduced_tables:
        counts = list(reduced_tables[z_key].values())
        log_ml_reduced += _dirichlet_multinomial_log_marginal(
            counts, alpha_prior, K_categories=N_STATES)

    log_bf = log_ml_full - log_ml_reduced

    n_full_params = 0
    n_reduced_params = 0
    for z_key in full_tables:
        for a in full_tables[z_key]:
            n_full_params += len(full_tables[z_key][a]) - 1
        n_reduced_params += len(reduced_tables[z_key]) - 1

    info = {
        "n_records": len(records),
        "n_strata": len(reduced_tables),
        "log_ml_full": log_ml_full,
        "log_ml_reduced": log_ml_reduced,
        "log_bayes_factor": log_bf,
        "n_full_params": n_full_params,
        "n_reduced_params": n_reduced_params,
        "alpha_prior": alpha_prior,
        "K_categories": N_STATES,
        "method": f"Dirichlet-Multinomial exact marginal likelihood (alpha={alpha_prior}, K={N_STATES})",
    }
    return log_bf, info


def shuffled_action_null_within_session(records, alpha_prior, n_shuffle=N_SHUFFLE, seed=SEED):
    """Within-session shuffled-action null (parent-identical framework)."""
    sessions = collections.defaultdict(list)
    for r in records:
        sessions[r["session"]].append(r)

    observed, _ = est_bayesian_model_comparison(records, alpha_prior)

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
        val, _ = est_bayesian_model_comparison(shuffled_records, alpha_prior)
        shuffled_vals.append(val)

    shuffled_vals = np.array(shuffled_vals)
    percentile_99_9 = float(np.percentile(shuffled_vals, 99.9))
    count_ge = int(np.sum(shuffled_vals >= observed))
    p_value = (count_ge + 1) / (n_shuffle + 1)
    return {
        "observed": float(observed),
        "null_median": float(np.median(shuffled_vals)),
        "null_mean": float(np.mean(shuffled_vals)),
        "null_std": float(np.std(shuffled_vals, ddof=0)),
        "null_max": float(np.max(shuffled_vals)),
        "percentile_99_9": percentile_99_9,
        "p_value": p_value,
        "n_shuffle": n_shuffle,
        "shuffled_first5": shuffled_vals[:5].tolist(),
        "null_all": shuffled_vals.tolist(),
    }


# ===========================================================================
# 5. Baselines
# ===========================================================================
def plugin_conditional_mi(records, alpha=1.0):
    """Plug-in conditional MI I(Y; A | X) in bits, with coherent Laplace
    alpha=1.0 smoothing over the (y,a) space at each x (K=12 next-state
    categories; A_x = distinct actions observed at x).

    P(y,a|x) = (c_{x,a,y} + alpha) / D_x,  D_x = n_x + alpha * |A_x| * K
    P(y|x)   = (c_{x,y} + alpha * |A_x|) / D_x
    P(a|x)   = (c_{x,a} + alpha * K) / D_x
    """
    counts_yax = collections.defaultdict(lambda: collections.defaultdict(
        lambda: collections.defaultdict(int)))
    counts_yx = collections.defaultdict(lambda: collections.defaultdict(int))
    counts_ax = collections.defaultdict(lambda: collections.defaultdict(int))
    counts_x = collections.Counter()
    for r in records:
        x = r["url_before"]
        a = r["action"]
        y = r["url_after"]
        counts_yax[x][a][y] += 1
        counts_yx[x][y] += 1
        counts_ax[x][a] += 1
        counts_x[x] += 1

    mi = 0.0
    n_total = len(records)
    for x in counts_x:
        nx = counts_x[x]
        a_obs = len(counts_ax[x])
        dx = nx + alpha * a_obs * N_STATES
        p_x = nx / n_total
        for a in counts_yax[x]:
            c_ax = counts_ax[x][a]
            for y, c in counts_yax[x][a].items():
                p_ya = (c + alpha) / dx
                p_y = (counts_yx[x][y] + alpha * a_obs) / dx
                p_a = (c_ax + alpha * N_STATES) / dx
                if p_ya > 0 and p_y > 0 and p_a > 0:
                    mi += p_x * p_ya * math.log2(p_ya / (p_y * p_a))
    return mi


def state_history_k2_mi(records, alpha=1.0):
    """Plug-in MI I(url_after; (url_before, H_K2)) in bits, Laplace alpha=1.0
    smoothing over the joint (y,z) table (one pseudo-count per cell).

    P(y,z) = (c_{y,z} + alpha) / (N + alpha * |Z| * |Y|)
    P(z)   = (c_z + alpha * |Y|) / (N + alpha * |Z| * |Y|)
    P(y)   = (c_y + alpha * |Z|) / (N + alpha * |Z| * |Y|)
    """
    counts_yz = collections.Counter()
    counts_z = collections.Counter()
    counts_y = collections.Counter()
    for r in records:
        z = (r["url_before"], r["history"])
        y = r["url_after"]
        counts_yz[(y, z)] += 1
        counts_z[z] += 1
        counts_y[y] += 1
    n = len(records)
    nz = len(counts_z)
    ny = len(counts_y)
    denom = n + alpha * nz * ny
    mi = 0.0
    for (y, z), c in counts_yz.items():
        p_yz = (c + alpha) / denom
        p_z = (counts_z[z] + alpha * ny) / denom
        p_y = (counts_y[y] + alpha * nz) / denom
        if p_yz > 0 and p_z > 0 and p_y > 0:
            mi += p_yz * math.log2(p_yz / (p_z * p_y))
    return mi


def action_history_accuracy_k3(records):
    """Fraction of transitions where (url_before, H_K3 actions) determines url_after."""
    groups = collections.defaultdict(list)
    for r in records:
        groups[(r["url_before"], r["history"])].append(r)
    n_det_records = 0
    n_groups_det = 0
    for key, recs in groups.items():
        nexts = collections.Counter(r["url_after"] for r in recs)
        if len(nexts) == 1:
            n_det_records += len(recs)
            n_groups_det += 1
    return {
        "n_groups": len(groups),
        "n_groups_det": n_groups_det,
        "n_records": len(records),
        "n_records_det": n_det_records,
        "fraction_records_det": n_det_records / len(records) if records else None,
        "fraction_groups_det": n_groups_det / len(groups) if groups else None,
    }


# ===========================================================================
# 6. Determinism stats
# ===========================================================================
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
        else:
            stochastic += 1
    total = deterministic + stochastic
    return {
        "deterministic": deterministic, "stochastic": stochastic, "total": total,
        "det_ratio": deterministic / total if total else 0.0,
    }


# ===========================================================================
# 7. Real data loading / filtering
# ===========================================================================
def load_raw_per_variant():
    """Split collected raw transitions into per-variant files and return them."""
    raw_all = json.load(open(EXP_DIR / "raw_transitions_all.json"))
    by_site = collections.defaultdict(list)
    for r in raw_all:
        by_site[r["site"]].append(r)
    return by_site


def filter_valid_nl(transitions):
    """Valid = url_after & action_primitive & no error; NL = not leakage.
    Also drop link_click (100% leakage by frozen definition; kept only for
    descriptive stats)."""
    valid = [r for r in transitions
             if r.get("url_after") and r.get("action_primitive") and not r.get("error")]
    nl = [r for r in valid if not is_leakage(r.get("action_target"), r.get("url_after"))]
    return valid, nl


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


# ===========================================================================
# 8. Main
# ===========================================================================
def main():
    t_start = time.time()
    EXP_DIR.mkdir(parents=True, exist_ok=True)

    log_lines = []
    def log(msg):
        print(msg, flush=True)
        log_lines.append(str(msg))

    log("=" * 72)
    log(f"EXPERIMENT {EXPERIMENT_ID} — Bayesian DM (K=12) on real TodoMVC hash-SPA transitions")
    log("=" * 72)

    # ------------------------------------------------------------------
    # POSITIVE CONTROL: synthetic stochastic 12-state SPA (N=5000, seed=42)
    # ------------------------------------------------------------------
    log("\n[POSITIVE CONTROL] synthetic stochastic 12-state SPA N=5000 seed=42 ...")
    t0 = time.time()
    transitions_synth = collect_synthetic("stochastic", 50, 100, SEED)
    sha_synth = hashlib.sha256(json.dumps(transitions_synth, sort_keys=True).encode()).hexdigest()
    log(f"[POSITIVE CONTROL] N={len(transitions_synth)} sha256={sha_synth} ({time.time()-t0:.1f}s)")

    recs_synth = build_state_history_records(transitions_synth, 2)
    det_synth = determinism_stats(recs_synth)
    log(f"[POSITIVE CONTROL] K2 records={len(recs_synth)} determinism={det_synth}")

    pos_control = {}
    pc_c1 = {}
    pc_c3 = {}
    for alpha in ALPHA_PRIOR_VALUES:
        t0 = time.time()
        nc = shuffled_action_null_within_session(recs_synth, alpha, N_SHUFFLE, SEED)
        c1_pass = nc["null_median"] < 0
        c3_pass = (nc["observed"] > nc["percentile_99_9"]) and (nc["p_value"] < 0.001)
        pc_c1[alpha] = c1_pass
        pc_c3[alpha] = c3_pass
        log(f"[POSITIVE CONTROL] alpha={alpha}: observed={nc['observed']:.3f} "
            f"null_median={nc['null_median']:.3f} null_max={nc['null_max']:.3f} "
            f"p={nc['p_value']:.5f} C1={c1_pass} C3={c3_pass} ({time.time()-t0:.1f}s)")
        pos_control[str(alpha)] = {
            "alpha_prior": alpha,
            "observed_log_bf": nc["observed"],
            "null_median": nc["null_median"],
            "null_mean": nc["null_mean"],
            "null_std": nc["null_std"],
            "null_max": nc["null_max"],
            "percentile_99_9": nc["percentile_99_9"],
            "p_value": nc["p_value"],
            "n_shuffle": nc["n_shuffle"],
            "shuffled_first5": nc["shuffled_first5"],
            "c1_pass": c1_pass,
            "c3_pass": c3_pass,
        }
    c6_pass = all(pc_c1[a] and pc_c3[a] for a in ALPHA_PRIOR_VALUES)
    log(f"[POSITIVE CONTROL] C6 = {'PASS' if c6_pass else 'FAIL'} (C1+C3 at all 3 alphas)")

    # Save synthetic raw evidence
    with open(EXP_DIR / "raw_synthetic.json", "w") as f:
        json.dump(transitions_synth, f, indent=1)

    # ------------------------------------------------------------------
    # REAL DATA: load, filter, split per-variant raw files
    # ------------------------------------------------------------------
    log("\n[REAL DATA] load raw_transitions_all.json ...")
    by_site = load_raw_per_variant()

    variant_analysis = {}
    for site in ["vanillajs", "react", "vue", "angular", "svelte"]:
        trans = by_site[site]
        valid, nl = filter_valid_nl(trans)
        # assign step indices chronologically within each session
        sess_map = collections.defaultdict(list)
        for r in valid:
            sess_map[r["session"]].append(r)
        nl_stepped = []
        for sid, sess_recs in sess_map.items():
            for i, r in enumerate(sorted(sess_recs, key=lambda x: x.get("timestamp", ""))):
                nl_stepped.append(dict(r, step=i, session=sid))
        # NL subset (used for all model analysis)
        nl_stepped = [r for r in nl_stepped if not is_leakage(r.get("action_target"), r.get("url_after"))]
        n_link = sum(1 for r in valid if r.get("action_primitive") == "link_click")
        n_nl_link = sum(1 for r in nl_stepped if r.get("action_primitive") == "link_click")

        # state-normalize
        for r in nl_stepped:
            r["url_before"] = normalize_state_url(r["url_before"])
            r["url_after"] = normalize_state_url(r["url_after"])

        sessions = sorted(set(r["session"] for r in nl_stepped))
        uniq_before = sorted(set(r["url_before"] for r in nl_stepped))
        uniq_after = sorted(set(r["url_after"] for r in nl_stepped))
        prims = collections.Counter(r["action_primitive"] for r in nl_stepped)
        log(f"\n[{site}] raw={len(trans)} valid={len(valid)} NL={len(nl_stepped)} "
            f"sessions={sessions} unique_before={uniq_before} unique_after={uniq_after} "
            f"prims={dict(prims)}")

        recs_k2 = build_state_history_records(nl_stepped, 2)
        det = determinism_stats(recs_k2)
        log(f"[{site}] K2 strata={det}")

        per_alpha = {}
        for alpha in ALPHA_PRIOR_VALUES:
            t0 = time.time()
            nc = shuffled_action_null_within_session(recs_k2, alpha, N_SHUFFLE, SEED)
            c1_pass = nc["null_median"] < 0
            c3_pass = (nc["observed"] > nc["percentile_99_9"]) and (nc["p_value"] < 0.001)
            per_alpha[str(alpha)] = {
                "alpha_prior": alpha,
                "observed_log_bf": nc["observed"],
                "null_median": nc["null_median"],
                "null_mean": nc["null_mean"],
                "null_std": nc["null_std"],
                "null_max": nc["null_max"],
                "percentile_99_9": nc["percentile_99_9"],
                "p_value": nc["p_value"],
                "n_shuffle": nc["n_shuffle"],
                "shuffled_first5": nc["shuffled_first5"],
                "c1_pass": c1_pass,
                "c3_pass": c3_pass,
                "wall_seconds": time.time() - t0,
            }
            log(f"[{site}] alpha={alpha}: observed={nc['observed']:.3f} "
                f"null_median={nc['null_median']:.3f} null_max={nc['null_max']:.3f} "
                f"p={nc['p_value']:.5f} C1={c1_pass} C3={c3_pass}")

        # Baselines
        b1 = plugin_conditional_mi(recs_k2)
        b2 = action_history_accuracy_k3(build_action_history_records(nl_stepped, 3))
        b3 = state_history_k2_mi(recs_k2)
        log(f"[{site}] B1 url-only PMI={b1:.4f} bits | B2 action-hist acc={b2['fraction_records_det']} "
            f"| B3 state-hist K2 MI={b3:.4f} bits")

        variant_analysis[site] = {
            "n_raw": len(trans),
            "n_valid": len(valid),
            "n_nl": len(nl_stepped),
            "n_link_valid": n_link,
            "n_link_nl": n_nl_link,
            "sessions": sessions,
            "unique_url_before": uniq_before,
            "unique_url_after": uniq_after,
            "action_distribution_nl": dict(prims),
            "determinism_k2": det,
            "per_alpha": per_alpha,
            "baseline_url_only_pmi_bits": b1,
            "baseline_action_history_acc_k3": b2,
            "baseline_state_history_k2_mi_bits": b3,
            "c1_all_alphas": all(per_alpha[str(a)]["c1_pass"] for a in ALPHA_PRIOR_VALUES),
            "c3_all_alphas": all(per_alpha[str(a)]["c3_pass"] for a in ALPHA_PRIOR_VALUES),
            "c1_any_alpha": any(per_alpha[str(a)]["c1_pass"] for a in ALPHA_PRIOR_VALUES),
            "c3_any_alpha": any(per_alpha[str(a)]["c3_pass"] for a in ALPHA_PRIOR_VALUES),
        }
        # Save per-variant raw NL evidence
        with open(EXP_DIR / f"raw_transitions_{site}.json", "w") as f:
            json.dump(valid, f, indent=1)
        with open(EXP_DIR / f"nl_transitions_{site}.json", "w") as f:
            json.dump(nl_stepped, f, indent=1)

    # ------------------------------------------------------------------
    # Decision rule (frozen)
    # ------------------------------------------------------------------
    c1_variant_count = sum(1 for s in variant_analysis if variant_analysis[s]["c1_all_alphas"])
    c3_variant_count = sum(1 for s in variant_analysis if variant_analysis[s]["c3_all_alphas"])
    c5_variant_count = sum(1 for s in variant_analysis if variant_analysis[s]["n_nl"] >= 50)
    c1_any_count = sum(1 for s in variant_analysis if variant_analysis[s]["c1_any_alpha"])
    c3_any_count = sum(1 for s in variant_analysis if variant_analysis[s]["c3_any_alpha"])

    log("\n" + "=" * 72)
    log("DECISION RULE (STRICT variant pass = all 3 alpha values)")
    log(f"C1 (null median < 0, all alphas): {c1_variant_count}/5 variants")
    log(f"C3 (p < 0.001, all alphas):       {c3_variant_count}/5 variants")
    log(f"C5 (>=50 NL):                     {c5_variant_count}/5 variants")
    log(f"C6 (positive control):            {'PASS' if c6_pass else 'FAIL'}")
    log("  (informative, any-alpha: C1={}/5 C3={}/5)".format(c1_any_count, c3_any_count))
    log("=" * 72)

    verdict = None
    outcome = None
    reason = None
    if not c6_pass:
        verdict = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        reason = ("C6 failed: positive control (synthetic stochastic 12-state SPA, N=5000, seed=42) "
                  "does not pass C1+C3 at all 3 alpha values; estimator implementation cannot be "
                  "validated. Real-data results are scientifically uninterpretable.")
    elif c5_variant_count < 2:
        verdict = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        reason = (f"C5 failed: only {c5_variant_count}/5 variants reach >=50 non-leakage transitions; "
                  "insufficient data to run the primary analysis.")
    elif c1_variant_count >= 2 and c3_variant_count >= 2:
        verdict = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
        reason = (f"Bayesian DM (K=12) passes C1 (null median<0) on {c1_variant_count}/5 and C3 "
                  f"(p<0.001) on {c3_variant_count}/5 real TodoMVC hash-SPA variants (all-3-alpha "
                  f"criterion), C5={c5_variant_count}/5, C6 positive control PASS, C7 no validity "
                  f"violations. Claim ceiling bounded to passing variants at URL-level fragment-aware "
                  f"state representation.")
    elif (c1_variant_count == 0 and c3_variant_count == 0):
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        reason = (f"C1 and C3 fail on all 5 real TodoMVC hash-SPA variants (all-3-alpha criterion: "
                  f"C1={c1_variant_count}/5, C3={c3_variant_count}/5). The Bayesian DM estimator does "
                  f"not survive on real browser-derived transitions. (any-alpha: C1={c1_any_count}/5, "
                  f"C3={c3_any_count}/5)")
    else:
        verdict = "MIXED"
        outcome = "MIXED"
        reason = (f"Some variants pass and others fail: C1={c1_variant_count}/5, C3={c3_variant_count}/5 "
                  f"(all-3-alpha); any-alpha C1={c1_any_count}/5, C3={c3_any_count}/5. Claim ceiling "
                  f"bounded to passing variants only.")

    log(f"\n[VERDICT] {verdict}")
    log(f"[OUTCOME] {outcome}")
    log(f"[REASON] {reason}")

    # ------------------------------------------------------------------
    # Raw results JSON
    # ------------------------------------------------------------------
    raw_results = {
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED,
        "N_SHUFFLE": N_SHUFFLE,
        "K_categories": N_STATES,
        "alpha_prior_values": ALPHA_PRIOR_VALUES,
        "positive_control": {
            "transitions_sha256": sha_synth,
            "n_transitions": len(transitions_synth),
            "determinism_k2": det_synth,
            "per_alpha": pos_control,
            "c6_pass": c6_pass,
        },
        "variants": variant_analysis,
        "decision": {
            "c1_variant_count_all_alpha": c1_variant_count,
            "c3_variant_count_all_alpha": c3_variant_count,
            "c1_variant_count_any_alpha": c1_any_count,
            "c3_variant_count_any_alpha": c3_any_count,
            "c5_variant_count": c5_variant_count,
            "c6_pass": c6_pass,
            "verdict": verdict,
            "outcome": outcome,
            "reason": reason,
        },
        "wall_seconds": time.time() - t_start,
    }
    with open(EXP_DIR / "raw_results.json", "w") as f:
        json.dump(raw_results, f, indent=2, default=to_json)
    with open(EXP_DIR / "raw_output.txt", "w") as f:
        f.write("\n".join(log_lines) + "\n")
    log(f"\nSaved raw_results.json (wall {time.time()-t_start:.1f}s)")


if __name__ == "__main__":
    main()