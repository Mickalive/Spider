#!/usr/bin/env python3
"""
EXP-PHYSICS-35353016293 — PMI analysis for beyond-Markov URL-level PMI.

Computes:
- Unconditional PMI (K=0): I(url_after; action | url_before)
- Conditional PMI K=1: I(url_after; action | url_before, H_1)
- Conditional PMI K=3: I(url_after; action | url_before, H_3)
- Permutation tests for each K level
- Action-history prediction accuracy at each K level

Frozen parameters from spec.json:
- alpha=0 (no Laplace smoothing)
- N_PERMUTATIONS=1000
- Bonferroni alpha = 0.05/3 = 0.0167
- MIN_STRATUM_SIZE = 5
- Decision threshold: K=3 PMI > 0.05 bits
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
ALPHA = 0  # No Laplace smoothing
BONFERRONI_COMPARISONS = 3
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # ≈ 0.0167
MIN_STRATUM_SIZE = 5
MIN_NL_TRANSITIONS = 100
START_TOKEN = "<START>"
HISTORY_LENGTHS = [0, 1, 3]

# 12-state SPA simulation states (must match server)
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


def build_action_histories(transitions, K):
    """Build action history records for history-conditioned PMI."""
    records = []
    # Group by session
    sessions = {}
    for t in transitions:
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
    for stratum, stratum_records in strata.items():
        if len(stratum_records) < MIN_STRATUM_SIZE:
            continue
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        majority_url, majority_count = next_counts.most_common(1)[0]
        correct += majority_count
        total += len(stratum_records)
    accuracy = correct / total if total > 0 else 0.0
    return {"accuracy": accuracy, "correct": correct, "total": total}


def run_positive_control():
    """Run positive control: 8-state synthetic deterministic SPA with known beyond-Markov structure."""
    rng = random.Random(SEED)
    positive_states = {
        0: {"url": "http://spa.test/home"},
        1: {"url": "http://spa.test/dashboard"},
        2: {"url": "http://spa.test/profile"},
        3: {"url": "http://spa.test/settings"},
        4: {"url": "http://spa.test/search"},
        5: {"url": "http://spa.test/notifications"},
        6: {"url": "http://spa.test/admin"},
        7: {"url": "http://spa.test/help"},
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
        current_state = rng.choice(list(positive_states.keys()))
        session_trans = []
        for step in range(50):
            action = rng.choice(positive_actions)
            next_state = positive_transitions[current_state][action]
            trans = {
                "url_before": positive_states[current_state]["url"],
                "url_after": positive_states[next_state]["url"],
                "action_primitive": action,
                "session": str(session_id),
                "step": step,
                "error": None,
            }
            session_trans.append(trans)
            current_state = next_state
        sessions[str(session_id)] = session_trans
    
    # Build K=3 records
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


def run_null_control(transitions_by_session):
    """Run null control: shuffled-action permutation test on real data."""
    perm = permutation_test(transitions_by_session, 3, N_PERMUTATIONS, SEED + 1)
    return {
        "description": "Shuffled action labels within sessions; expected mean = 0.0 bits",
        "mean_pmi": perm["null_mean"],
        "observed_pmi": perm["observed_pmi"],
        "p_value": perm["p_value"],
        "null_std": perm["null_std"],
        "pass": abs(perm["null_mean"]) < 3 * max(perm["null_std"], 1e-10),
    }


def analyze(transitions):
    """Run full PMI analysis on collected transitions."""
    # Group by session
    sessions = {}
    for t in transitions:
        sid = t["session"]
        if sid not in sessions:
            sessions[sid] = []
        sessions[sid].append(t)
    
    results = {}
    
    # For each K level
    for K in HISTORY_LENGTHS:
        all_records = []
        for sid, trans in sessions.items():
            records = build_action_histories([{"transitions": trans}], K)
            all_records.extend(records)
        
        pmi_stats = compute_conditional_pmi(all_records, K)
        perm = permutation_test(sessions, K, N_PERMUTATIONS, SEED)
        accuracy = compute_prediction_accuracy(all_records, K)
        
        results[f"K{K}"] = {
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
        }
    
    return results


def main():
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — PMI Analysis")
    print("=" * 70)
    
    # Load raw transitions
    raw_path = Path("research/experiments") / EXPERIMENT_ID / "raw_transitions.json"
    if not raw_path.exists():
        print(f"ERROR: {raw_path} not found. Run collect_data.py first.")
        sys.exit(1)
    
    with open(raw_path) as f:
        transitions = json.load(f)
    
    print(f"\nLoaded {len(transitions)} transitions")
    n_sessions = len(set(t["session"] for t in transitions))
    print(f"Sessions: {n_sessions}")
    
    # Filter non-leakage transitions (exclude link_click)
    nl_transitions = [t for t in transitions if t.get("action_primitive") != "link_click"]
    print(f"Non-leakage transitions: {len(nl_transitions)}")
    
    if len(nl_transitions) < MIN_NL_TRANSITIONS:
        print(f"WARNING: Only {len(nl_transitions)} NL transitions (need >= {MIN_NL_TRANSITIONS})")
    
    # ── Positive control ──
    print("\n[CONTROL] Positive control (synthetic 8-state deterministic SPA)...")
    positive_control = run_positive_control()
    print(f"  K=3 PMI: {positive_control['pmi_k3']:.6f} bits (threshold >= 1.0)")
    print(f"  Perm p: {positive_control['permutation_p']:.6f} (threshold < 0.001)")
    print(f"  Passes: {positive_control['passes']}")
    
    # ── Main analysis ──
    print("\n[ANALYSIS] Computing PMI at K=0, K=1, K=3...")
    sessions = {}
    for t in nl_transitions:
        sid = t["session"]
        if sid not in sessions:
            sessions[sid] = []
        sessions[sid].append(t)
    
    analysis = analyze(nl_transitions)
    
    for K in HISTORY_LENGTHS:
        r = analysis[f"K{K}"]
        print(f"\n  K={K}:")
        print(f"    PMI: {r['pmi_bits']:.6f} bits")
        print(f"    Permutation p: {r['permutation_p']:.6f}")
        print(f"    Effect size d: {r['effect_size_d']:.4f}")
        print(f"    Prediction accuracy: {r['prediction_accuracy']:.4f}")
        print(f"    Strata used: {r['n_used']}/{r['n_strata']}")
        print(f"    Total records: {r['n_total']}")
    
    # ── Null control ──
    print("\n[NULL] Null control (shuffled actions)...")
    null_control = run_null_control(sessions)
    print(f"  Mean shuffled PMI: {null_control['mean_pmi']:.6f} bits")
    print(f"  Pass: {null_control['pass']}")
    
    # ── Decision rule ──
    print("\n" + "=" * 70)
    print("DECISION RULE APPLICATION")
    print("=" * 70)
    
    k3 = analysis["K3"]
    k0 = analysis["K0"]
    
    # Decision conditions
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
    
    # Apply decision rule
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
        "analysis": analysis,
        "positive_control": positive_control,
        "null_control": null_control,
        "nl_count": len(nl_transitions),
        "raw_count": len(transitions),
        "n_sessions": n_sessions,
        "decision": decision,
        "outcome": outcome,
        "status": status,
    }


if __name__ == "__main__":
    results = main()
    
    # Save analysis results
    out_path = Path("research/experiments") / EXPERIMENT_ID / "analysis_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved analysis to {out_path}")
