#!/usr/bin/env python3
"""
EXP-PHYSICS-35353016293 — Self-contained experiment execution.

Simulates the 12-state SPA with beyond-Markov transitions in-memory,
collects transitions, and runs the full PMI analysis.  No external server
required.

The SPA simulation uses:
- 12 unique hash-based URL states (multiple states share base path)
- 4 action primitives (form_submit, button_click, js_navigate, menu_select)
- Stochastic transitions conditioned on previous 2 states (K=2)
- Hash-based selection: SHA256(prev1:prev2:current:action) mod 4 → candidate index

This creates genuine beyond-Markov structure: (url_before, H_K=3) does NOT
fully determine url_after because the transition depends on url_{t-2} which
is outside H_K=3 when H_K=3 only contains actions.
"""

import hashlib
import json
import math
import random
import collections
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

import numpy as np

EXPERIMENT_ID = "EXP-PHYSICS-35353016293"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 0
BONFERRONI_COMPARISONS = 3
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS
MIN_STRATUM_SIZE = 5
MIN_NL_TRANSITIONS = 100
START_TOKEN = "<START>"
HISTORY_LENGTHS = [0, 1, 3]

# ── SPA State Definitions ──────────────────────────────────────────
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

# ── Transition Table ────────────────────────────────────────────────
# For each (current_state, action), 4 candidate successors.
# Actual successor = candidates[SHA256(prev1:prev2:current:action) mod 4]
CANDIDATES = {
    0: {
        "form_submit":   [1, 5, 3, 9],
        "button_click":  [2, 6, 4, 10],
        "js_navigate":   [3, 7, 5, 11],
        "menu_select":   [4, 8, 1, 6],
    },
    1: {
        "form_submit":   [2, 5, 7, 3],
        "button_click":  [4, 0, 8, 10],
        "js_navigate":   [6, 3, 9, 1],
        "menu_select":   [5, 7, 11, 4],
    },
    2: {
        "form_submit":   [1, 6, 0, 8],
        "button_click":  [3, 5, 9, 4],
        "js_navigate":   [7, 1, 10, 2],
        "menu_select":   [0, 8, 3, 11],
    },
    3: {
        "form_submit":   [4, 0, 6, 10],
        "button_click":  [1, 7, 5, 11],
        "js_navigate":   [2, 8, 0, 9],
        "menu_select":   [5, 9, 4, 1],
    },
    4: {
        "form_submit":   [3, 1, 8, 0],
        "button_click":  [6, 2, 7, 11],
        "js_navigate":   [5, 0, 3, 10],
        "menu_select":   [7, 10, 6, 2],
    },
    5: {
        "form_submit":   [0, 3, 11, 6],
        "button_click":  [1, 4, 8, 2],
        "js_navigate":   [9, 6, 0, 7],
        "menu_select":   [10, 2, 5, 3],
    },
    6: {
        "form_submit":   [2, 8, 0, 4],
        "button_click":  [3, 9, 7, 1],
        "js_navigate":   [4, 10, 1, 5],
        "menu_select":   [1, 11, 3, 8],
    },
    7: {
        "form_submit":   [8, 1, 3, 5],
        "button_click":  [9, 0, 6, 2],
        "js_navigate":   [10, 4, 0, 8],
        "menu_select":   [11, 5, 7, 1],
    },
    8: {
        "form_submit":   [7, 2, 0, 6],
        "button_click":  [10, 3, 1, 9],
        "js_navigate":   [11, 5, 4, 0],
        "menu_select":   [9, 0, 8, 3],
    },
    9: {
        "form_submit":   [10, 0, 2, 7],
        "button_click":  [11, 1, 5, 3],
        "js_navigate":   [0, 4, 8, 6],
        "menu_select":   [1, 6, 10, 4],
    },
    10: {
        "form_submit":   [11, 4, 1, 9],
        "button_click":  [0, 5, 3, 8],
        "js_navigate":   [1, 6, 7, 2],
        "menu_select":   [3, 7, 11, 5],
    },
    11: {
        "form_submit":   [9, 3, 5, 1],
        "button_click":  [10, 2, 6, 0],
        "js_navigate":   [0, 7, 4, 8],
        "menu_select":   [2, 8, 10, 3],
    },
}


def choose_next(current, action, prev1, prev2):
    """Choose next state based on (prev1, prev2, current, action)."""
    candidates = CANDIDATES[current][action]
    h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
    idx = int(h[:8], 16) % len(candidates)
    return candidates[idx]


def simulate_session(session_id, n_steps, rng):
    """Simulate one session of SPA navigation."""
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


def collect_transitions():
    """Collect all transitions from simulated SPA."""
    rng = random.Random(SEED)
    all_transitions = []
    
    n_sessions = 20
    steps_per_session = 50
    
    for session_id in range(n_sessions):
        trans = simulate_session(session_id, steps_per_session, rng)
        all_transitions.extend(trans)
    
    return all_transitions


def save_raw_data(transitions):
    """Save raw transition data."""
    out_dir = Path("research/experiments") / EXPERIMENT_ID
    out_dir.mkdir(parents=True, exist_ok=True)
    
    raw_path = out_dir / "raw_transitions.json"
    with open(raw_path, "w") as f:
        json.dump(transitions, f, indent=2)
    
    sha = hashlib.sha256(json.dumps(transitions, sort_keys=True).encode()).hexdigest()
    print(f"Saved {len(transitions)} transitions to {raw_path}")
    print(f"SHA256: {sha}")
    
    return raw_path, sha


# ── PMI Analysis Functions ──────────────────────────────────────────

def build_action_histories(transitions, K):
    """Build action history records for history-conditioned PMI.
    
    Accepts either:
    - A list of transition dicts (each with 'session' key), or
    - A list of session dicts with {"session": ..., "transitions": [...]}
    """
    records = []
    sessions = {}
    for t in transitions:
        if "transitions" in t:
            # Session dict format
            sid = t.get("session", "unknown")
            if sid not in sessions:
                sessions[sid] = []
            sessions[sid].extend(t["transitions"])
        else:
            # Raw transition dict
            sid = t["session"]
            if sid not in sessions:
                sessions[sid] = []
            sessions[sid].append(t)
    
    for sid, session_trans in sessions.items():
        actions = [t["action_primitive"] for t in session_trans if t.get("action_primitive") is not None]
        if not actions:
            continue
        for i, t in enumerate(session_trans):
            if i == 0:
                history = tuple([START_TOKEN] * K)
            elif i < K:
                history = tuple([START_TOKEN] * (K - i) + actions[:i])
            else:
                history = tuple(actions[i - K:i])
            records.append({
                "url_before": t["url_before"],
                "history": history,
                "action": t["action_primitive"],
                "url_after": t["url_after"],
            })
    return records


def compute_conditional_pmi(records, K):
    """Compute conditional PMI I(url_after; action | url_before, H_K) with alpha=0."""
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    total_records = len(records)
    if total_records == 0:
        return {"pmi": 0.0, "n_strata": 0, "n_used": 0, "total": 0,
                "skipped_small": 0, "skipped_zero_var": 0}
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
            count_a = action_counts[a]
            count_s = next_counts[s_next]
            count_as = joint_counts[(a, s_next)]
            p_a = count_a / n_h
            p_s = count_s / n_h
            p_joint = count_as / n_h
            denom = p_a * p_s
            if denom > 0 and p_joint > 0:
                pmi = math.log2(p_joint / denom)
            else:
                pmi = 0.0
            pmi_values.append(pmi)
        stratum_pmi = sum(pmi_values) / len(pmi_values)
        pmi_weighted_sum += weight * stratum_pmi
        n_used += 1
    return {"pmi": pmi_weighted_sum, "n_strata": len(strata), "n_used": n_used,
            "total": total_records, "skipped_small": skipped_small, "skipped_zero_var": skipped_zero_var}


def permutation_test(transitions_by_session, K, n_permutations, seed):
    """Permutation test: shuffle action labels within sessions."""
    rng = random.Random(seed)
    all_records = []
    session_keys = sorted(transitions_by_session.keys())
    for sid in session_keys:
        session_trans = transitions_by_session[sid]
        records = build_action_histories([{"transitions": session_trans}], K)
        all_records.extend(records)
    if not all_records:
        return {"p_value": 1.0, "observed_pmi": 0.0, "null_mean": 0.0, "null_std": 0.0, "effect_size_d": 0.0}
    observed = compute_conditional_pmi(all_records, K)
    observed_pmi = observed["pmi"]
    shuffled_means = []
    for _ in range(n_permutations):
        perm_rng = random.Random(rng.randint(0, 2**32))
        shuffled_records = []
        for sid in session_keys:
            trans = transitions_by_session[sid]
            actions = [t["action_primitive"] for t in trans if t.get("action_primitive") is not None]
            shuffled_actions = actions[:]
            perm_rng.shuffle(shuffled_actions)
            urls_before = [t["url_before"] for t in trans]
            urls_after = [t["url_after"] for t in trans]
            for i in range(len(trans)):
                if i == 0:
                    history = tuple([START_TOKEN] * K)
                elif i < K:
                    history = tuple([START_TOKEN] * (K - i) + shuffled_actions[:i])
                else:
                    history = tuple(shuffled_actions[i - K:i])
                shuffled_records.append({
                    "url_before": urls_before[i], "history": history,
                    "action": shuffled_actions[i], "url_after": urls_after[i],
                })
        stats = compute_conditional_pmi(shuffled_records, K)
        shuffled_means.append(stats["pmi"])
    count_ge = sum(1 for m in shuffled_means if m >= observed_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)
    null_mean = float(np.mean(shuffled_means))
    null_std = float(np.std(shuffled_means))
    effect_d = float((observed_pmi - null_mean) / null_std) if null_std > 0 else 0.0
    return {"p_value": p_value, "observed_pmi": observed_pmi,
            "null_mean": null_mean, "null_std": null_std, "effect_size_d": effect_d}


def compute_prediction_accuracy(all_records, K):
    """Compute majority-vote prediction accuracy at K."""
    strata = collections.defaultdict(list)
    for r in all_records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    correct = 0
    total = 0
    stratum_details = []
    for stratum, stratum_records in strata.items():
        if len(stratum_records) < MIN_STRATUM_SIZE:
            continue
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        majority_url, majority_count = next_counts.most_common(1)[0]
        correct += majority_count
        total += len(stratum_records)
        stratum_details.append({
            "url_before": stratum[0],
            "history": str(stratum[1]),
            "n": len(stratum_records),
            "majority": majority_url,
            "majority_count": majority_count,
            "accuracy": majority_count / len(stratum_records),
            "distinct_nexts": len(next_counts),
        })
    accuracy = correct / total if total > 0 else 0.0
    return {"accuracy": accuracy, "correct": correct, "total": total,
            "n_strata": len(stratum_details), "details": stratum_details[:10]}


# ── Positive Control ────────────────────────────────────────────────

def run_positive_control():
    """8-state synthetic deterministic SPA with known beyond-Markov structure."""
    rng = random.Random(SEED)
    positive_states = {
        0: "http://spa.test/home", 1: "http://spa.test/dashboard",
        2: "http://spa.test/profile", 3: "http://spa.test/settings",
        4: "http://spa.test/search", 5: "http://spa.test/notifications",
        6: "http://spa.test/admin", 7: "http://spa.test/help",
    }
    positive_actions = ["form_submit", "button_click", "js_navigate", "menu_select"]
    positive_transitions = {
        0: {"form_submit": 1, "button_click": 2, "js_navigate": 3, "menu_select": 4},
        1: {"form_submit": 4, "button_click": 5, "js_navigate": 0, "menu_select": 6},
        2: {"form_submit": 3, "button_click": 6, "js_navigate": 1, "menu_select": 7},
        3: {"form_submit": 0, "button_click": 7, "js_navigate": 2, "menu_select": 4},
        4: {"form_submit": 5, "button_click": 0, "js_navigate": 6, "menu_select": 7},
        5: {"form_submit": 6, "button_click": 1, "js_navigate": 7, "menu_select": 4},
        6: {"form_submit": 7, "button_click": 2, "js_navigate": 4, "menu_select": 5},
        7: {"form_submit": 0, "button_click": 3, "js_navigate": 5, "menu_select": 6},
    }
    
    sessions = {}
    for session_id in range(100):
        current_state = rng.choice(range(8))
        session_trans = []
        for step in range(50):
            action = rng.choice(positive_actions)
            next_state = positive_transitions[current_state][action]
            session_trans.append({
                "url_before": positive_states[current_state],
                "url_after": positive_states[next_state],
                "action_primitive": action,
                "session": str(session_id),
                "step": step,
                "error": None,
            })
            current_state = next_state
        sessions[str(session_id)] = session_trans
    
    all_records = []
    for sid, trans in sessions.items():
        records = build_action_histories([{"transitions": trans}], 3)
        all_records.extend(records)
    
    pmi_stats = compute_conditional_pmi(all_records, 3)
    perm = permutation_test(sessions, 3, N_PERMUTATIONS, SEED)
    accuracy = compute_prediction_accuracy(all_records, 3)
    
    passes_pmi = pmi_stats["pmi"] >= 1.0
    passes_perm = perm["p_value"] < 0.001
    passes = passes_pmi and passes_perm
    
    return {
        "pmi_k3": pmi_stats["pmi"],
        "permutation_p": perm["p_value"],
        "effect_size_d": perm["effect_size_d"],
        "prediction_accuracy": accuracy["accuracy"],
        "n_transitions": len(all_records),
        "passes_pmi": passes_pmi,
        "passes_perm": passes_perm,
        "passes": passes,
    }


# ── Main Experiment ────────────────────────────────────────────────

def run_experiment():
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID}")
    print("Beyond-Markov URL-level PMI on 12-state SPA Simulation")
    print("=" * 70)
    
    # ── Collect transitions ──
    print("\n[COLLECT] Simulating 12-state SPA transitions...")
    transitions = collect_transitions()
    raw_path, raw_sha = save_raw_data(transitions)
    
    n_sessions = len(set(t["session"] for t in transitions))
    print(f"  Sessions: {n_sessions}")
    print(f"  Steps per session: 50")
    print(f"  Total transitions: {len(transitions)}")
    
    # Verify automatability pilot
    automatability_pass = len(transitions) >= 200
    print(f"  Automatability pilot (>=200 raw): {automatability_pass}")
    
    # ── Unique URL states ──
    unique_urls = set(t["url_after"] for t in transitions)
    print(f"  Unique URL states visited: {len(unique_urls)}")
    for url in sorted(unique_urls):
        count = sum(1 for t in transitions if t["url_after"] == url)
        print(f"    {url}: {count}")
    
    # ── Action distribution ──
    action_counts = collections.Counter(t["action_primitive"] for t in transitions)
    print(f"  Action distribution:")
    for a, c in action_counts.most_common():
        print(f"    {a}: {c}")
    
    # ── Non-leakage transitions ──
    nl_transitions = [t for t in transitions if t.get("action_primitive") != "link_click"]
    print(f"\n  Non-leakage transitions: {len(nl_transitions)}")
    nl_pass = len(nl_transitions) >= MIN_NL_TRANSITIONS
    print(f"  NL threshold (>= {MIN_NL_TRANSITIONS}): {nl_pass}")
    
    # ── Positive control ──
    print("\n[CONTROL] Positive control (8-state deterministic SPA)...")
    positive_control = run_positive_control()
    print(f"  K=3 PMI: {positive_control['pmi_k3']:.6f} bits (threshold >= 1.0)")
    print(f"  Perm p: {positive_control['permutation_p']:.6f} (threshold < 0.001)")
    print(f"  Prediction accuracy: {positive_control['prediction_accuracy']:.4f}")
    print(f"  Passes: {positive_control['passes']}")
    
    # ── PMI Analysis ──
    print("\n[ANALYSIS] Computing PMI at K=0, K=1, K=3...")
    sessions = {}
    for t in nl_transitions:
        sid = t["session"]
        if sid not in sessions:
            sessions[sid] = []
        sessions[sid].append(t)
    
    analysis_results = {}
    for K in HISTORY_LENGTHS:
        all_records = []
        for sid, trans in sessions.items():
            records = build_action_histories([{"transitions": trans}], K)
            all_records.extend(records)
        
        pmi_stats = compute_conditional_pmi(all_records, K)
        perm = permutation_test(sessions, K, N_PERMUTATIONS, SEED)
        accuracy = compute_prediction_accuracy(all_records, K)
        
        analysis_results[f"K{K}"] = {
            "pmi_bits": pmi_stats["pmi"],
            "n_strata": pmi_stats["n_strata"],
            "n_used": pmi_stats["n_used"],
            "n_total": pmi_stats["total"],
            "skipped_small": pmi_stats["skipped_small"],
            "skipped_zero_var": pmi_stats["skipped_zero_var"],
            "permutation_p": perm["p_value"],
            "null_mean": perm["null_mean"],
            "null_std": perm["null_std"],
            "effect_size_d": perm["effect_size_d"],
            "prediction_accuracy": accuracy["accuracy"],
            "prediction_correct": accuracy["correct"],
            "prediction_total": accuracy["total"],
            "prediction_n_strata": accuracy["n_strata"],
        }
        
        r = analysis_results[f"K{K}"]
        print(f"\n  K={K}:")
        print(f"    PMI: {r['pmi_bits']:.6f} bits")
        print(f"    Permutation p: {r['permutation_p']:.6f}")
        print(f"    Effect size d: {r['effect_size_d']:.4f}")
        print(f"    Prediction accuracy: {r['prediction_accuracy']:.4f}")
        print(f"    Strata used: {r['n_used']}/{r['n_strata']}")
        print(f"    Total records: {r['n_total']}")
    
    # ── Null control ──
    print("\n[NULL] Null control (shuffled actions)...")
    null_perm = permutation_test(sessions, 3, N_PERMUTATIONS, SEED + 1)
    null_control = {
        "description": "Shuffled action labels within sessions; expected mean = 0.0 bits",
        "mean_pmi": null_perm["null_mean"],
        "observed_pmi": null_perm["observed_pmi"],
        "p_value": null_perm["p_value"],
        "null_std": null_perm["null_std"],
        "pass": abs(null_perm["null_mean"]) < 3 * max(null_perm["null_std"], 1e-10),
    }
    print(f"  Mean shuffled PMI: {null_control['mean_pmi']:.6f} bits")
    print(f"  Pass: {null_control['pass']}")
    
    # ── Determinism check ──
    print("\n[CHECK] Determinism verification...")
    # For each (url_before, H_K=3) stratum, check if url_after is deterministic
    all_records_k3 = []
    for sid, trans in sessions.items():
        records = build_action_histories([{"transitions": trans}], 3)
        all_records_k3.extend(records)
    
    strata_k3 = collections.defaultdict(list)
    for r in all_records_k3:
        stratum = (r["url_before"], r["history"])
        strata_k3[stratum].append(r)
    
    deterministic_strata = 0
    stochastic_strata = 0
    for stratum, stratum_records in strata_k3.items():
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        if len(next_counts) == 1:
            deterministic_strata += 1
        else:
            stochastic_strata += 1
    
    total_strata = deterministic_strata + stochastic_strata
    determinism_ratio = deterministic_strata / total_strata if total_strata > 0 else 0
    print(f"  Deterministic strata (K=3): {deterministic_strata}/{total_strata} ({determinism_ratio:.2%})")
    print(f"  Stochastic strata: {stochastic_strata}/{total_strata}")
    
    # ── Decision Rule ──
    print("\n" + "=" * 70)
    print("DECISION RULE APPLICATION")
    print("=" * 70)
    
    k3 = analysis_results["K3"]
    k0 = analysis_results["K0"]
    
    # Decision conditions from prereg
    c1_k3_pmi = k3["pmi_bits"] > 0.05
    c1_k3_perm = k3["permutation_p"] < ALPHA_BONFERRONI
    c1 = c1_k3_pmi and c1_k3_perm
    
    c2_positive = positive_control["passes"]
    
    c3_nlt = len(nl_transitions) >= MIN_NL_TRANSITIONS
    
    c4_k0_pmi = k0["pmi_bits"] > 0.05
    
    c5_automatability = len(transitions) >= 200
    
    print(f"\n  C1 (K=3 PMI > 0.05, Bonferroni p < {ALPHA_BONFERRONI:.4f}):")
    print(f"    K=3 PMI = {k3['pmi_bits']:.6f} > 0.05: {c1_k3_pmi}")
    print(f"    K=3 perm p = {k3['permutation_p']:.6f} < {ALPHA_BONFERRONI:.4f}: {c1_k3_perm}")
    print(f"    C1 PASSES: {c1}")
    
    print(f"\n  C2 (Positive control K=3 PMI >= 1.0, p < 0.001):")
    print(f"    Positive control PMI = {positive_control['pmi_k3']:.6f}")
    print(f"    Positive control p = {positive_control['permutation_p']:.6f}")
    print(f"    C2 PASSES: {c2_positive}")
    
    print(f"\n  C3 (>= {MIN_NL_TRANSITIONS} NL transitions):")
    print(f"    NL transitions = {len(nl_transitions)}")
    print(f"    C3 PASSES: {c3_nlt}")
    
    print(f"\n  C4 (K=0 PMI > 0.05):")
    print(f"    K=0 PMI = {k0['pmi_bits']:.6f}")
    print(f"    C4 PASSES: {c4_k0_pmi}")
    
    print(f"\n  C5 (Automatability pilot >= 200 raw):")
    print(f"    Raw transitions = {len(transitions)}")
    print(f"    C5 PASSES: {c5_automatability}")
    
    # Apply decision rule (order matters: FALSIFIED checked before MEASUREMENT_INVALID)
    if c1 and c2 and c3 and c4 and c5_automatability:
        decision = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif not c1:
        decision = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not c5_automatability:
        decision = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif not c2 or not c3:
        decision = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    else:
        decision = "INCONCLUSIVE"
        outcome = "MIXED"
        status = "COMPLETE"
    
    print(f"\n  FINAL DECISION: {decision}")
    print(f"  OUTCOME: {outcome}")
    print(f"  STATUS: {status}")
    
    return {
        "analysis": analysis_results,
        "positive_control": positive_control,
        "null_control": null_control,
        "nl_count": len(nl_transitions),
        "raw_count": len(transitions),
        "n_sessions": n_sessions,
        "n_unique_urls": len(unique_urls),
        "deterministic_strata_k3": deterministic_strata,
        "stochastic_strata_k3": stochastic_strata,
        "determinism_ratio": determinism_ratio,
        "decision": decision,
        "outcome": outcome,
        "status": status,
    }


if __name__ == "__main__":
    results = run_experiment()
    
    out_path = Path("research/experiments") / EXPERIMENT_ID / "analysis_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved analysis to {out_path}")
