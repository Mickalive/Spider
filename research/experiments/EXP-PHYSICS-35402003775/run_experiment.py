#!/usr/bin/env python3
"""
EXP-PHYSICS-35402003775 — Three materially orthogonal null frameworks.
Tests whether parametric bootstrap, Miller-Madow, or conditional entropy center null at zero
for hash-routed SPAs, resolving the inherited ~0.41-bit PMI estimator bias floor.

Implements:
 1. Parametric bootstrap null: estimate P(url_after | url_before, history) from data,
    simulate null transition samples from this estimated distribution, compute PMI.
 2. Miller-Madow unbiased PMI estimator: apply bias correction to log-ratio estimator.
 3. Conditional entropy difference: DeltaH = H(url_after|action,url_before,history)
    - H(url_after|url_before,history) under within-stratum permutation null.

Positive control: 8-state synthetic deterministic SPA N=5000, K=3 PMI >=1.0 bits, p<0.001.
Baseline comparisons: within-stratum permutation (parent method), block permutation, action-shuffle.
"""
import hashlib
import json
import math
import random
import collections
import sys
import os
import subprocess
import time
import socket
from pathlib import Path

import numpy as np

EXPERIMENT_ID = "EXP-PHYSICS-35402003775"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 0
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"
BONFERRONI_COMPARISONS = 3
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.0167

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

def choose_next(current, action, prev1, prev2):
    candidates = CANDIDATES[current][action]
    h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
    idx = int(h[:8],16) % len(candidates)
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

# -- Record builders --
def build_state_history_records(transitions, K):
    """State-history H_K = (url_{t-K}..url_{t-1}); url_before = current; url_after = next"""
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
                history = tuple([START_TOKEN]*K)
            elif i < K:
                history = tuple([START_TOKEN]*(K-i) + url_before_seq[:i])
            else:
                history = tuple(url_before_seq[i-K:i])
            records.append({
                "session": sid,
                "step": i,
                "url_before": t["url_before"],
                "history": history,
                "action": t["action_primitive"],
                "url_after": t["url_after"],
            })
    return records

def build_action_history_records(transitions, K):
    """Action-history H_K = (action_{t-K}..action_{t-1}) same as parent"""
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
                history = tuple([START_TOKEN]*K)
            elif i < K:
                history = tuple([START_TOKEN]*(K-i) + actions[:i])
            else:
                history = tuple(actions[i-K:i])
            records.append({
                "session": sid,
                "step": i,
                "url_before": t["url_before"],
                "history": history,
                "action": t["action_primitive"],
                "url_after": t["url_after"],
            })
    return records

# -- PMI computation --
def compute_conditional_pmi(records, K):
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    total_records = len(records)
    if total_records == 0:
        return {"pmi":0.0,"n_strata":0,"n_used":0,"total":0,"skipped_small":0,"skipped_zero_var":0}
    pmi_weighted_sum = 0.0
    n_used = 0
    skipped_small = 0
    skipped_zero_var = 0
    for stratum, stratum_records in strata.items():
        n_h = len(stratum_records)
        weight = n_h / total_records
        if n_h < MIN_STRATUM_SIZE:
            skipped_small += 1
            continue
        action_counts = collections.Counter(r["action"] for r in stratum_records)
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        joint_counts = collections.Counter((r["action"], r["url_after"]) for r in stratum_records)
        distinct_nexts = len(next_counts)
        if distinct_nexts <= 1:
            skipped_zero_var += 1
            pmi_weighted_sum += weight * 0.0
            n_used += 1
            continue
        pmi_values = []
        for r in stratum_records:
            a = r["action"]
            s_next = r["url_after"]
            p_a = action_counts[a] / n_h
            p_s = next_counts[s_next] / n_h
            p_joint = joint_counts[(a,s_next)] / n_h
            denom = p_a * p_s
            if denom>0 and p_joint>0:
                pmi = math.log2(p_joint/denom)
            else:
                pmi = 0.0
            pmi_values.append(pmi)
        stratum_pmi = sum(pmi_values)/len(pmi_values)
        pmi_weighted_sum += weight * stratum_pmi
        n_used += 1
    return {"pmi": pmi_weighted_sum, "n_strata": len(strata), "n_used": n_used, "total": total_records, "skipped_small": skipped_small, "skipped_zero_var": skipped_zero_var}

def compute_prediction_accuracy(records, K):
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["history"])].append(r)
    correct = 0
    total = 0
    for stratum, recs in strata.items():
        if len(recs) < MIN_STRATUM_SIZE:
            continue
        next_counts = collections.Counter(r["url_after"] for r in recs)
        majority_cnt = next_counts.most_common(1)[0][1]
        correct += majority_cnt
        total += len(recs)
    return correct/total if total>0 else 0.0

# -- Miller-Madow corrected PMI --
def compute_miller_madow_pmi(records, K):
    """Compute PMI with Miller-Madow bias correction.
    PMI_MM(x,y) = PMI(x,y) + (V_x - 1)/(2*N_x*ln2) + (V_y - 1)/(2*N_y*ln2) - (V_xy - 1)/(2*N_xy*ln2)
    """
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    total_records = len(records)
    if total_records == 0:
        return {"pmi_mm":0.0,"pmi_raw":0.0,"n_strata":0,"n_used":0,"total":0,"skipped_small":0,"skipped_zero_var":0}
    pmi_weighted_sum = 0.0
    pmi_mm_weighted_sum = 0.0
    n_used = 0
    skipped_small = 0
    skipped_zero_var = 0
    for stratum, stratum_records in strata.items():
        n_h = len(stratum_records)
        weight = n_h / total_records
        if n_h < MIN_STRATUM_SIZE:
            skipped_small += 1
            continue
        action_counts = collections.Counter(r["action"] for r in stratum_records)
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        joint_counts = collections.Counter((r["action"], r["url_after"]) for r in stratum_records)
        distinct_nexts = len(next_counts)
        if distinct_nexts <= 1:
            skipped_zero_var += 1
            pmi_weighted_sum += weight * 0.0
            pmi_mm_weighted_sum += weight * 0.0
            n_used += 1
            continue
        pmi_values = []
        pmi_mm_values = []
        V_a = len(action_counts)  # unique actions in stratum
        V_y = len(next_counts)    # unique url_after in stratum
        V_ay = len(joint_counts)  # unique (action, url_after) pairs in stratum
        for r in stratum_records:
            a = r["action"]
            s_next = r["url_after"]
            p_a = action_counts[a] / n_h
            p_s = next_counts[s_next] / n_h
            p_joint = joint_counts[(a,s_next)] / n_h
            denom = p_a * p_s
            if denom>0 and p_joint>0:
                pmi = math.log2(p_joint/denom)
            else:
                pmi = 0.0
            pmi_values.append(pmi)
            # Miller-Madow correction
            mm_correction = 0.0
            if n_h > 0:
                mm_correction += (V_a - 1) / (2 * n_h * math.log(2))
                mm_correction += (V_y - 1) / (2 * n_h * math.log(2))
                mm_correction -= (V_ay - 1) / (2 * n_h * math.log(2))
            pmi_mm = pmi + mm_correction
            pmi_mm_values.append(pmi_mm)
        stratum_pmi = sum(pmi_values)/len(pmi_values)
        stratum_pmi_mm = sum(pmi_mm_values)/len(pmi_mm_values)
        pmi_weighted_sum += weight * stratum_pmi
        pmi_mm_weighted_sum += weight * stratum_pmi_mm
        n_used += 1
    return {"pmi_mm": pmi_mm_weighted_sum, "pmi_raw": pmi_weighted_sum, "n_strata": len(strata), "n_used": n_used, "total": total_records, "skipped_small": skipped_small, "skipped_zero_var": skipped_zero_var}

# -- Conditional entropy computation --
def compute_conditional_entropy(records, K):
    """Compute H(url_after | action, url_before, history) and H(url_after | url_before, history)"""
    # First: H(url_after | action, url_before, history)
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"], r["action"])
        strata[stratum].append(r)
    total_records = len(records)
    if total_records == 0:
        return {"h_full":0.0,"h_marginal":0.0,"delta_h":0.0,"n_strata_full":0,"n_used_full":0}
    # Compute H(url_after | action, url_before, history)
    h_weighted_sum = 0.0
    n_used_full = 0
    for stratum, stratum_records in strata.items():
        n_h = len(stratum_records)
        weight = n_h / total_records
        if n_h < MIN_STRATUM_SIZE:
            continue
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        entropy = 0.0
        for cnt in next_counts.values():
            p = cnt / n_h
            if p > 0:
                entropy -= p * math.log2(p)
        h_weighted_sum += weight * entropy
        n_used_full += 1
    # Second: H(url_after | url_before, history)
    strata_marginal = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata_marginal[stratum].append(r)
    h_marginal_weighted_sum = 0.0
    n_used_marginal = 0
    for stratum, stratum_records in strata_marginal.items():
        n_h = len(stratum_records)
        weight = n_h / total_records
        if n_h < MIN_STRATUM_SIZE:
            continue
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        entropy = 0.0
        for cnt in next_counts.values():
            p = cnt / n_h
            if p > 0:
                entropy -= p * math.log2(p)
        h_marginal_weighted_sum += weight * entropy
        n_used_marginal += 1
    delta_h = h_weighted_sum - h_marginal_weighted_sum
    return {"h_full": h_weighted_sum, "h_marginal": h_marginal_weighted_sum, "delta_h": delta_h,
            "n_strata_full": len(strata), "n_used_full": n_used_full,
            "n_strata_marginal": len(strata_marginal), "n_used_marginal": n_used_marginal}

# -- Permutation tests --

def permutation_test_within_stratum(records, K, n_permutations=1000, seed=42):
    """Within-stratum conditional permutation: shuffle url_after within each (url_before, history) stratum."""
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    observed = compute_conditional_pmi(records, K)
    observed_pmi = observed["pmi"]
    rng = random.Random(seed)
    shuffled_pmis = []
    for _ in range(n_permutations):
        perm_rng = random.Random(rng.randint(0, 2**32))
        shuffled_records = []
        for stratum, stratum_records in strata.items():
            url_afters = [r["url_after"] for r in stratum_records]
            perm_rng.shuffle(url_afters)
            for i, r in enumerate(stratum_records):
                shuffled_records.append({
                    "session": r["session"],
                    "step": r["step"],
                    "url_before": r["url_before"],
                    "history": r["history"],
                    "action": r["action"],
                    "url_after": url_afters[i],
                })
        stats = compute_conditional_pmi(shuffled_records, K)
        shuffled_pmis.append(stats["pmi"])
    shuffled_pmis = np.array(shuffled_pmis)
    count_ge = np.sum(shuffled_pmis >= observed_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)
    null_mean = float(np.mean(shuffled_pmis))
    null_std = float(np.std(shuffled_pmis, ddof=0))
    effect_d = float((observed_pmi - null_mean)/null_std) if null_std>0 else 0.0
    return {
        "observed_pmi": observed_pmi,
        "p_value": p_value,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
        "shuffled_pmis": shuffled_pmis.tolist()[:5],
        "observed_stats": observed
    }

# -- Parametric bootstrap null --
def parametric_bootstrap_null(records, K, n_bootstrap=1000, seed=42):
    """Model-based null: estimate P(url_after | url_before, history) from data,
    simulate null transition samples from this estimated distribution, compute PMI.
    """
    # Estimate transition model P_hat(url_after | url_before, history) with Laplace smoothing
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    # Build conditional distributions with Laplace smoothing
    stratum_models = {}
    for stratum, stratum_records in strata.items():
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        total = sum(next_counts.values())
        vocab = list(next_counts.keys())
        # Laplace smoothing alpha=1.0
        alpha = 1.0
        smoothed_counts = {k: v + alpha for k, v in next_counts.items()}
        total_smoothed = total + alpha * len(vocab)
        probs = {k: v / total_smoothed for k, v in smoothed_counts.items()}
        stratum_models[stratum] = {"probs": probs, "vocab": vocab, "total": total}
    # Bootstrap
    rng = random.Random(seed)
    bootstrap_pmis = []
    for _ in range(n_bootstrap):
        # For each record, draw url_after from P_hat(url_after | stratum)
        shuffled_records = []
        for r in records:
            stratum = (r["url_before"], r["history"])
            model = stratum_models.get(stratum)
            if model is None:
                # If stratum not seen in training, keep original url_after
                shuffled_records.append(r)
                continue
            probs = model["probs"]
            vocab = model["vocab"]
            # Sample from distribution
            r_val = random.random()
            cumulative = 0.0
            sampled_next = vocab[-1]  # fallback
            for k in vocab:
                cumulative += probs[k]
                if r_val <= cumulative:
                    sampled_next = k
                    break
            shuffled_records.append({
                "session": r["session"],
                "step": r["step"],
                "url_before": r["url_before"],
                "history": r["history"],
                "action": r["action"],
                "url_after": sampled_next,
            })
        # Compute PMI on simulated dataset
        stats = compute_conditional_pmi(shuffled_records, K)
        bootstrap_pmis.append(stats["pmi"])
    bootstrap_pmis = np.array(bootstrap_pmis)
    observed = compute_conditional_pmi(records, K)
    observed_pmi = observed["pmi"]
    null_mean = float(np.mean(bootstrap_pmis))
    null_std = float(np.std(bootstrap_pmis, ddof=0))
    effect_d = float((observed_pmi - null_mean)/null_std) if null_std>0 else 0.0
    # p-value: proportion of bootstrap PMIs >= observed
    count_ge = np.sum(bootstrap_pmis >= observed_pmi)
    p_value = (count_ge + 1) / (n_bootstrap + 1)
    return {
        "observed_pmi": observed_pmi,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
        "p_value": p_value,
        "bootstrap_pmis": bootstrap_pmis.tolist()[:5],
        "observed_stats": observed
    }

# -- Miller-Madow permutation null --
def miller_madow_permutation_null(records, K, n_permutations=1000, seed=42):
    """Within-stratum permutation null with Miller-Madow corrected estimator."""
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    observed = compute_miller_madow_pmi(records, K)
    observed_pmi_mm = observed["pmi_mm"]
    rng = random.Random(seed)
    shuffled_pmi_mms = []
    for _ in range(n_permutations):
        perm_rng = random.Random(rng.randint(0, 2**32))
        shuffled_records = []
        for stratum, stratum_records in strata.items():
            url_afters = [r["url_after"] for r in stratum_records]
            perm_rng.shuffle(url_afters)
            for i, r in enumerate(stratum_records):
                shuffled_records.append({
                    "session": r["session"],
                    "step": r["step"],
                    "url_before": r["url_before"],
                    "history": r["history"],
                    "action": r["action"],
                    "url_after": url_afters[i],
                })
        stats = compute_miller_madow_pmi(shuffled_records, K)
        shuffled_pmi_mms.append(stats["pmi_mm"])
    shuffled_pmi_mms = np.array(shuffled_pmi_mms)
    count_ge = np.sum(shuffled_pmi_mms >= observed_pmi_mm)
    p_value = (count_ge + 1) / (n_permutations + 1)
    null_mean = float(np.mean(shuffled_pmi_mms))
    null_std = float(np.std(shuffled_pmi_mms, ddof=0))
    effect_d = float((observed_pmi_mm - null_mean)/null_std) if null_std>0 else 0.0
    return {
        "observed_pmi_mm": observed_pmi_mm,
        "observed_pmi_raw": observed["pmi_raw"],
        "p_value": p_value,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
        "shuffled_pmi_mms": shuffled_pmi_mms.tolist()[:5],
        "observed_stats": observed
    }

# -- Conditional entropy permutation null --
def conditional_entropy_permutation_null(records, K, n_permutations=1000, seed=42):
    """Within-stratum permutation null for DeltaH = H(full) - H(marginal)."""
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    observed = compute_conditional_entropy(records, K)
    observed_delta_h = observed["delta_h"]
    rng = random.Random(seed)
    shuffled_delta_hs = []
    for _ in range(n_permutations):
        perm_rng = random.Random(rng.randint(0, 2**32))
        shuffled_records = []
        for stratum, stratum_records in strata.items():
            url_afters = [r["url_after"] for r in stratum_records]
            perm_rng.shuffle(url_afters)
            for i, r in enumerate(stratum_records):
                shuffled_records.append({
                    "session": r["session"],
                    "step": r["step"],
                    "url_before": r["url_before"],
                    "history": r["history"],
                    "action": r["action"],
                    "url_after": url_afters[i],
                })
        stats = compute_conditional_entropy(shuffled_records, K)
        shuffled_delta_hs.append(stats["delta_h"])
    shuffled_delta_hs = np.array(shuffled_delta_hs)
    count_ge = np.sum(shuffled_delta_hs >= observed_delta_h)
    p_value = (count_ge + 1) / (n_permutations + 1)
    null_mean = float(np.mean(shuffled_delta_hs))
    null_std = float(np.std(shuffled_delta_hs, ddof=0))
    effect_d = float((observed_delta_h - null_mean)/null_std) if null_std>0 else 0.0
    return {
        "observed_delta_h": observed_delta_h,
        "observed_h_full": observed["h_full"],
        "observed_h_marginal": observed["h_marginal"],
        "p_value": p_value,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
        "shuffled_delta_hs": shuffled_delta_hs.tolist()[:5],
        "observed_stats": observed
    }

def determinism_check(records, K):
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["history"])].append(r)
    deterministic = 0
    stochastic = 0
    for stratum, recs in strata.items():
        next_counts = collections.Counter(r["url_after"] for r in recs)
        if len(next_counts) == 1:
            deterministic += 1
        elif len(next_counts) > 1:
            stochastic += 1
    total = deterministic+stochastic
    return {"deterministic": deterministic, "stochastic": stochastic, "total": total, "stoch_ratio": stochastic/total if total else 0, "det_ratio": deterministic/total if total else 0}

def run_positive_control(n_transitions=5000, seed=SEED):
    """8-state synthetic deterministic SPA, N=5000, test state and action history K=3"""
    rng = random.Random(seed)
    positive_states = {
        0: "http://spa.test/home", 1: "http://spa.test/dashboard",
        2: "http://spa.test/profile", 3: "http://spa.test/settings",
        4: "http://spa.test/search", 5: "http://spa.test/notifications",
        6: "http://spa.test/admin", 7: "http://spa.test/help",
    }
    positive_actions = ["form_submit","button_click","js_navigate","menu_select"]
    positive_transitions = {
        0: {"form_submit":1,"button_click":2,"js_navigate":3,"menu_select":4},
        1: {"form_submit":4,"button_click":5,"js_navigate":0,"menu_select":6},
        2: {"form_submit":3,"button_click":6,"js_navigate":1,"menu_select":7},
        3: {"form_submit":0,"button_click":7,"js_navigate":2,"menu_select":4},
        4: {"form_submit":5,"button_click":0,"js_navigate":6,"menu_select":7},
        5: {"form_submit":6,"button_click":1,"js_navigate":7,"menu_select":4},
        6: {"form_submit":7,"button_click":2,"js_navigate":4,"menu_select":5},
        7: {"form_submit":0,"button_click":3,"js_navigate":5,"menu_select":6},
    }
    transitions = []
    n_sessions = 50
    steps_per_session = 100
    for sid in range(n_sessions):
        current = rng.choice(range(8))
        prev1,prev2 = current, current
        for step in range(steps_per_session):
            action = rng.choice(positive_actions)
            next_state = positive_transitions[current][action]
            transitions.append({
                "session": f"pc_session_{sid}",
                "step": step,
                "url_before": positive_states[current],
                "url_after": positive_states[next_state],
                "action_primitive": action,
            })
            current = next_state
    recs_state_K3 = build_state_history_records(transitions, 3)
    recs_action_K3 = build_action_history_records(transitions, 3)
    pmi_state = compute_conditional_pmi(recs_state_K3, 3)
    pmi_action = compute_conditional_pmi(recs_action_K3, 3)
    perm_state = permutation_test_within_stratum(recs_state_K3, 3, N_PERMUTATIONS, SEED)
    perm_action = permutation_test_within_stratum(recs_action_K3, 3, N_PERMUTATIONS, SEED)
    # Conditional entropy positive control
    ce_observed = compute_conditional_entropy(recs_state_K3, 3)
    ce_K2 = compute_conditional_entropy(build_state_history_records(transitions, 2), 2)
    return {
        "transitions": transitions,
        "n_transitions": len(transitions),
        "pmi_state_K3": pmi_state["pmi"],
        "pmi_action_K3": pmi_action["pmi"],
        "perm_state_p": perm_state["p_value"],
        "perm_action_p": perm_action["p_value"],
        "perm_state_null_mean": perm_state["null_mean"],
        "perm_action_null_mean": perm_action["null_mean"],
        "perm_state_null_std": perm_state["null_std"],
        "perm_action_null_std": perm_action["null_std"],
        "effect_d_state": perm_state["effect_size_d"],
        "effect_d_action": perm_action["effect_size_d"],
        "pmi_state_details": pmi_state,
        "pmi_action_details": pmi_action,
        "passes_state": pmi_state["pmi"] >=1.0 and perm_state["p_value"]<0.001,
        "passes_action": pmi_action["pmi"] >=1.0 and perm_action["p_value"]<0.001,
        "passes_overall": (pmi_action["pmi"] >=1.0 and perm_action["p_value"]<0.001) or (pmi_state["pmi"]>=1.0 and perm_state["p_value"]<0.001),
        "conditional_entropy_K3": ce_observed,
        "conditional_entropy_K2": ce_K2,
        "entropy_positive_control_passes": ce_observed["h_full"] > ce_K2["h_full"],  # H(S|S,H_K=3) > H(S|S,H_K=2)
    }

def main():
    print("="*70)
    print(f"EXPERIMENT {EXPERIMENT_ID}")
    print("Three materially orthogonal null frameworks")
    print("Phase 1: Simulation null centering on 12-state SPA")
    print("="*70)
    out_dir = Path("research/experiments") / EXPERIMENT_ID
    out_dir.mkdir(parents=True, exist_ok=True)

    # -- Phase 1: Collect 12-state SPA data --
    print("\n[COLLECT] Simulating 12-state SPA 50x100=5000 transitions...")
    transitions = collect_transitions(n_sessions=50, steps_per_session=100, seed=SEED)
    print(f"  Total: {len(transitions)}")
    n_sessions = len(set(t["session"] for t in transitions))
    print(f"  Sessions: {n_sessions}")

    raw_path = out_dir / "raw_transitions.json"
    with open(raw_path, "w") as f:
        json.dump(transitions, f, indent=2)
    sha_raw = hashlib.sha256(json.dumps(transitions, sort_keys=True).encode()).hexdigest()
    print(f"  Saved raw to {raw_path} SHA256:{sha_raw[:16]}...")

    # -- Build records --
    print("\n[BUILD] Building state-history and action-history records...")
    recs_state_K0 = build_state_history_records(transitions, 0)
    recs_state_K1 = build_state_history_records(transitions, 1)
    recs_state_K2 = build_state_history_records(transitions, 2)
    recs_state_K3 = build_state_history_records(transitions, 3)
    recs_action_K3 = build_action_history_records(transitions, 3)

    # -- Compute PMIs --
    print("\n[ANALYSIS] Computing PMIs...")
    results = {}
    for label, recs, K in [
        ("unconditional_state_K0", recs_state_K0, 0),
        ("state_K1", recs_state_K1, 1),
        ("state_K2", recs_state_K2, 2),
        ("state_K3", recs_state_K3, 3),
        ("action_K3", recs_action_K3, 3),
    ]:
        pmi_stats = compute_conditional_pmi(recs, K)
        acc = compute_prediction_accuracy(recs, K)
        det = determinism_check(recs, K) if K > 0 else {"deterministic":0,"stochastic":0,"total":0}
        results[label] = {
            "pmi_bits": pmi_stats["pmi"],
            "n_strata_total": pmi_stats["n_strata"],
            "n_strata_used": pmi_stats["n_used"],
            "n_total_records": pmi_stats["total"],
            "skipped_small": pmi_stats["skipped_small"],
            "skipped_zero_var": pmi_stats["skipped_zero_var"],
            "prediction_accuracy": acc,
            "determinism": det,
        }
        print(f"  {label} K={K}: PMI={pmi_stats['pmi']:.6f} used={pmi_stats['n_used']}/{pmi_stats['n_strata']} acc={acc:.4f}")

    # -- PRIMARY: Three null frameworks (K=2) --
    print("\n" + "="*70)
    print("[FRAMEWORK 1] Parametric bootstrap null (PRIMARY TEST)")
    print("  Estimate P(url_after | stratum) from data, simulate null samples, compute PMI")
    print("  Expected null mean = 0 bits")
    print("="*70)
    pb_result = parametric_bootstrap_null(recs_state_K2, 2, N_PERMUTATIONS, SEED)
    print(f"  Observed K2 PMI: {pb_result['observed_pmi']:.6f} bits")
    print(f"  Null mean: {pb_result['null_mean']:.6f} bits")
    print(f"  Null std:  {pb_result['null_std']:.6f} bits")
    print(f"  |null_mean|: {abs(pb_result['null_mean']):.6f}")
    print(f"  0.1 threshold: {'PASS' if abs(pb_result['null_mean']) < 0.1 else 'FAIL'}")
    print(f"  Permutation p: {pb_result['p_value']:.6f}")
    print(f"  Effect size d: {pb_result['effect_size_d']:.2f}")

    print("\n" + "="*70)
    print("[FRAMEWORK 2] Miller-Madow corrected PMI null")
    print("  Apply bias correction to PMI estimator, within-stratum permutation")
    print("  Expected null mean = 0 bits")
    print("="*70)
    mm_result = miller_madow_permutation_null(recs_state_K2, 2, N_PERMUTATIONS, SEED)
    print(f"  Observed K2 PMI (raw): {mm_result['observed_pmi_raw']:.6f} bits")
    print(f"  Observed K2 PMI (MM):  {mm_result['observed_pmi_mm']:.6f} bits")
    print(f"  Null mean: {mm_result['null_mean']:.6f} bits")
    print(f"  Null std:  {mm_result['null_std']:.6f} bits")
    print(f"  |null_mean|: {abs(mm_result['null_mean']):.6f}")
    print(f"  0.1 threshold: {'PASS' if abs(mm_result['null_mean']) < 0.1 else 'FAIL'}")
    print(f"  Permutation p: {mm_result['p_value']:.6f}")
    print(f"  Effect size d: {mm_result['effect_size_d']:.2f}")

    print("\n" + "="*70)
    print("[FRAMEWORK 3] Conditional entropy difference null")
    print("  DeltaH = H(S|A,S,H) - H(S|S,H) under within-stratum permutation")
    print("  Expected null mean = 0 bits")
    print("="*70)
    ce_result = conditional_entropy_permutation_null(recs_state_K2, 2, N_PERMUTATIONS, SEED)
    print(f"  Observed DeltaH: {ce_result['observed_delta_h']:.6f} bits")
    print(f"  Observed H(full): {ce_result['observed_h_full']:.6f} bits")
    print(f"  Observed H(marginal): {ce_result['observed_h_marginal']:.6f} bits")
    print(f"  Null mean: {ce_result['null_mean']:.6f} bits")
    print(f"  Null std:  {ce_result['null_std']:.6f} bits")
    print(f"  |null_mean|: {abs(ce_result['null_mean']):.6f}")
    print(f"  0.1 threshold: {'PASS' if abs(ce_result['null_mean']) < 0.1 else 'FAIL'}")
    print(f"  Permutation p: {ce_result['p_value']:.6f}")
    print(f"  Effect size d: {ce_result['effect_size_d']:.2f}")

    # -- Baseline comparisons --
    print("\n[BASELINE] Within-stratum conditional permutation (parent method)...")
    within_stratum_perm = permutation_test_within_stratum(recs_state_K2, 2, N_PERMUTATIONS, SEED)
    print(f"  Within-stratum null mean K2: {within_stratum_perm['null_mean']:.6f}")

    # -- Positive control --
    print("\n[CONTROL] Positive control 8-state deterministic N=5000...")
    pc = run_positive_control(n_transitions=5000, seed=SEED)
    print(f"  State K3 PMI={pc['pmi_state_K3']:.6f} p={pc['perm_state_p']:.6f} d={pc['effect_d_state']:.2f} passes={pc['passes_state']}")
    print(f"  Action K3 PMI={pc['pmi_action_K3']:.6f} p={pc['perm_action_p']:.6f} d={pc['effect_d_action']:.2f} passes={pc['passes_action']}")
    print(f"  Overall passes: {pc['passes_overall']}")
    print(f"  Conditional entropy positive control passes: {pc['entropy_positive_control_passes']}")

    # -- DECISION RULE --
    print("\n" + "="*70)
    print("DECISION RULE")
    print("="*70)
    # Per-framework evaluation
    framework_pass = []
    framework_names = ["parametric_bootstrap", "miller_madow", "conditional_entropy"]
    # Parametric bootstrap pass condition
    pb_pass = (abs(pb_result['null_mean']) < 0.1 and
               pc["passes_overall"] and
               pb_result['observed_pmi'] > 0.05)
    framework_pass.append(("parametric_bootstrap", pb_pass))
    print(f"Parametric bootstrap: |null_mean|={abs(pb_result['null_mean']):.6f} < 0.1 = {abs(pb_result['null_mean']) < 0.1}")
    print(f"  Positive control passes: {pc['passes_overall']}")
    print(f"  Signal > 0.05: {pb_result['observed_pmi'] > 0.05}")
    print(f"  -> {'PASS' if pb_pass else 'FAIL'}")
    
    # Miller-Madow pass condition
    mm_pass = (abs(mm_result['null_mean']) < 0.1 and
               pc["passes_overall"] and
               mm_result['observed_pmi_mm'] > 0.05)
    framework_pass.append(("miller_madow", mm_pass))
    print(f"Miller-Madow: |null_mean|={abs(mm_result['null_mean']):.6f} < 0.1 = {abs(mm_result['null_mean']) < 0.1}")
    print(f"  Positive control passes: {pc['passes_overall']}")
    print(f"  Signal > 0.05: {mm_result['observed_pmi_mm'] > 0.05}")
    print(f"  -> {'PASS' if mm_pass else 'FAIL'}")
    
    # Conditional entropy pass condition
    ce_pass = (abs(ce_result['null_mean']) < 0.1 and
               pc["entropy_positive_control_passes"] and
               ce_result['observed_delta_h'] > 0.05)
    framework_pass.append(("conditional_entropy", ce_pass))
    print(f"Conditional entropy: |null_mean|={abs(ce_result['null_mean']):.6f} < 0.1 = {abs(ce_result['null_mean']) < 0.1}")
    print(f"  Positive control passes (H_K3 > H_K2): {pc['entropy_positive_control_passes']}")
    print(f"  Signal > 0.05: {ce_result['observed_delta_h'] > 0.05}")
    print(f"  -> {'PASS' if ce_pass else 'FAIL'}")
    
    n_pass = sum(1 for _, p in framework_pass if p)
    print(f"\nFrameworks passing: {n_pass}/3")
    
    # Overall verdict
    if n_pass >= 1:
        decision = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
        status = "COMPLETE"
        print("At least one framework passes all conditions.")
    else:
        decision = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        status = "COMPLETE"
        print("All three frameworks fail to center null.")
    
    print(f"FINAL: {decision} outcome {outcome} status {status}")

    # Save analysis
    def to_py(o):
        if isinstance(o, (np.bool_, np.integer, np.floating)):
            return o.item()
        if isinstance(o, bool):
            return bool(o)
        return o

    analysis = {
        "experiment_id": EXPERIMENT_ID,
        "n_transitions": int(len(transitions)),
        "n_sessions": int(n_sessions),
        "results": results,
        "parametric_bootstrap": {k: (bool(v) if isinstance(v, (bool, np.bool_)) else v) for k,v in pb_result.items()},
        "miller_madow": {k: (bool(v) if isinstance(v, (bool, np.bool_)) else v) for k,v in mm_result.items()},
        "conditional_entropy": {k: (bool(v) if isinstance(v, (bool, np.bool_)) else v) for k,v in ce_result.items()},
        "within_stratum_permutation": within_stratum_perm,
        "positive_control": {k: (bool(v) if isinstance(v, (bool, np.bool_)) else v) for k,v in pc.items()},
        "framework_pass": framework_pass,
        "n_pass": n_pass,
        "decision": decision,
        "outcome": outcome,
        "status": status,
        "sha_raw": sha_raw,
        "params": {"seed":SEED,"n_permutations":N_PERMUTATIONS,"alpha":ALPHA,"min_stratum":MIN_STRATUM_SIZE,"bonferroni":float(ALPHA_BONFERRONI)}
    }
    with open(out_dir / "analysis_results.json", "w") as f:
        json.dump(analysis, f, indent=2, default=to_py)
    print(f"\nSaved analysis to {out_dir/'analysis_results.json'}")
    return analysis

if __name__ == "__main__":
    main()