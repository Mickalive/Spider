#!/usr/bin/env python3
"""
EXP-PHYSICS-35290611436 - History-conditioned URL PMI on TodoMVC hash-SPAs:
testing beyond-Markov structure.

Frozen inputs: request.json, spec.json, prereg.md, freeze.json
All computation deterministic (seed=42, PYTHONHASHSEED=0).
"""

import json
import math
import random
import collections
import os
import sys

import numpy as np

EXPERIMENT_ID = "EXP-PHYSICS-35290611436"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 0
PARENT_DIR = "research/experiments/EXP-PHYSICS-35209110569"
VARIANTS = ["vanillajs", "react", "vue", "angular", "svelte"]
HISTORY_LENGTHS = [0, 1, 3]
BONFERRONI_COMPARISONS = 5
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"

DATA_FILES = {
    "vanillajs": ["raw_vanillajs.json", "raw_vanillajs_topup.json"],
    "react": ["raw_react.json", "raw_react_topup.json"],
    "vue": ["raw_vue.json", "raw_vue_topup.json"],
    "angular": ["raw_angular.json", "raw_angular_topup.json"],
    "svelte": ["raw_svelte.json", "raw_svelte_topup.json"],
}

def load_variant_data(variant, parent_dir):
    all_transitions = []
    for filename in DATA_FILES[variant]:
        filepath = os.path.join(parent_dir, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
        all_transitions.extend(data)
    return all_transitions

def filter_valid(transitions):
    return [t for t in transitions if t.get("error") is None]

def filter_non_leakage(transitions):
    return [t for t in transitions if t.get("action_primitive") != "link_click"]

def group_by_session(transitions):
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["session"]].append(t)
    for sid in groups:
        groups[sid].sort(key=lambda t: t.get("timestamp") or "")
    return dict(groups)

def build_action_histories(session_transitions, K):
    records = []
    actions = [t["action_primitive"] for t in session_transitions]
    for i, t in enumerate(session_transitions):
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
    contributing_weight = 0.0
    
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
            contributing_weight += weight
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
        contributing_weight += weight
        n_used += 1
    
    return {
        "pmi": pmi_weighted_sum,
        "n_strata": len(strata),
        "n_used": n_used,
        "total": total_records,
        "skipped_small": skipped_small,
        "skipped_zero_var": skipped_zero_var,
        "contributing_weight": contributing_weight,
    }

def permutation_test(session_groups, K, n_permutations, seed):
    rng = random.Random(seed)
    
    original_records = []
    session_keys = []
    for sid in sorted(session_groups.keys()):
        records = build_action_histories(session_groups[sid], K)
        original_records.extend(records)
        session_keys.append(sid)
    
    observed = compute_conditional_pmi(original_records, K)
    observed_pmi = observed["pmi"]
    
    shuffled_means = []
    for _ in range(n_permutations):
        perm_rng = random.Random(rng.randint(0, 2**32))
        shuffled_records = []
        for sid in session_keys:
            trans = session_groups[sid]
            actions = [t["action_primitive"] for t in trans]
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
                    "url_before": urls_before[i],
                    "history": history,
                    "action": shuffled_actions[i],
                    "url_after": urls_after[i],
                })
        
        stats = compute_conditional_pmi(shuffled_records, K)
        shuffled_means.append(stats["pmi"])
    
    count_ge = sum(1 for m in shuffled_means if m >= observed_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)
    
    null_mean = float(np.mean(shuffled_means))
    null_std = float(np.std(shuffled_means))
    effect_d = float((observed_pmi - null_mean) / null_std) if null_std > 0 else 0.0
    
    return {
        "p_value": p_value,
        "observed_pmi": observed_pmi,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
    }

def compute_prediction_accuracy(all_records, K):
    strata = collections.defaultdict(list)
    for r in all_records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    
    correct = 0
    total = 0
    strata_used = 0
    for stratum, stratum_records in strata.items():
        if len(stratum_records) < MIN_STRATUM_SIZE:
            continue
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        majority_url, majority_count = next_counts.most_common(1)[0]
        correct += majority_count
        total += len(stratum_records)
        strata_used += 1
    
    accuracy = correct / total if total > 0 else 0.0
    return {"accuracy": accuracy, "correct": correct, "total": total, "strata_used": strata_used}

SYNTHETIC_STATES = {
    0: {"url": "http://spa.test/home"},
    1: {"url": "http://spa.test/home#/dashboard"},
    2: {"url": "http://spa.test/home#/profile"},
    3: {"url": "http://spa.test/home#/settings"},
    4: {"url": "http://spa.test/home#/search"},
    5: {"url": "http://spa.test/home#/notifications"},
    6: {"url": "http://spa.test/home#/admin"},
    7: {"url": "http://spa.test/home#/help"},
}
SYNTHETIC_ACTIONS = ["form_submit", "button_click", "js_navigate"]
SYNTHETIC_TRANSITIONS = {
    0: {"form_submit": 1, "button_click": 2, "js_navigate": 3},
    1: {"form_submit": 4, "button_click": 5, "js_navigate": 0},
    2: {"form_submit": 3, "button_click": 6, "js_navigate": 1},
    3: {"form_submit": 0, "button_click": 7, "js_navigate": 2},
    4: {"form_submit": 5, "button_click": 0, "js_navigate": 6},
    5: {"form_submit": 6, "button_click": 1, "js_navigate": 7},
    6: {"form_submit": 7, "button_click": 2, "js_navigate": 4},
    7: {"form_submit": 0, "button_click": 3, "js_navigate": 5},
}

def generate_synthetic_trajectories(n_sessions, steps_per_session, rng):
    state_ids = list(SYNTHETIC_STATES.keys())
    all_transitions = []
    for session_id in range(n_sessions):
        current_state = rng.choice(state_ids)
        for step in range(steps_per_session):
            action = rng.choice(SYNTHETIC_ACTIONS)
            next_state = SYNTHETIC_TRANSITIONS[current_state][action]
            all_transitions.append({
                "site": "synthetic_control",
                "session": session_id,
                "url_before": SYNTHETIC_STATES[current_state]["url"],
                "url_after": SYNTHETIC_STATES[next_state]["url"],
                "action_primitive": action,
                "action_target": None,
                "timestamp": None,
                "error": None,
            })
            current_state = next_state
    return all_transitions

def run_positive_control(rng):
    print("\n[CONTROL] Running positive control (synthetic deterministic SPA)...")
    synthetic = generate_synthetic_trajectories(100, 50, rng)
    valid = filter_valid(synthetic)
    sessions = group_by_session(valid)
    
    all_records = []
    for sid, trans in sessions.items():
        records = build_action_histories(trans, 3)
        all_records.extend(records)
    
    stats = compute_conditional_pmi(all_records, 3)
    perm = permutation_test(sessions, 3, N_PERMUTATIONS, SEED)
    
    passes_pmi = stats["pmi"] >= 1.0
    passes_perm = perm["p_value"] < 0.001
    passes = passes_pmi and passes_perm
    
    print(f"  PMI at K=3: {stats['pmi']:.6f} bits (threshold: 1.0)")
    print(f"  Permutation p: {perm['p_value']:.6f} (threshold: 0.001)")
    print(f"  Positive control passes: {passes}")
    
    return {
        "pmi_k3": stats["pmi"],
        "permutation_p": perm["p_value"],
        "effect_size_d": perm["effect_size_d"],
        "n_strata": stats["n_strata"],
        "n_used": stats["n_used"],
        "total": stats["total"],
        "passes_pmi": passes_pmi,
        "passes_perm": passes_perm,
        "passes": passes,
    }

def normalize_url(url):
    if not url:
        return url
    url = url.split("#")[0]
    if url.endswith("/") and url.count("/") > 3:
        url = url[:-1]
    return url

def run_experiment():
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — History-conditioned URL PMI")
    print("=" * 70)
    
    rng = random.Random(SEED)
    os.environ["PYTHONHASHSEED"] = "0"
    
    positive_control = run_positive_control(rng)
    
    variant_results = {}
    
    for variant in VARIANTS:
        print(f"\n[DATA] Processing {variant}...")
        
        raw_data = load_variant_data(variant, PARENT_DIR)
        print(f"  Raw transitions loaded: {len(raw_data)}")
        
        valid = filter_valid(raw_data)
        print(f"  Valid (error=None): {len(valid)}")
        
        non_leakage = filter_non_leakage(valid)
        print(f"  Non-leakage (not link_click): {len(non_leakage)}")
        
        if len(non_leakage) < 50:
            print(f"  WARNING: Fewer than 50 non-leakage transitions ({len(non_leakage)})")
        
        sessions = group_by_session(non_leakage)
        
        k_results = {}
        for K in HISTORY_LENGTHS:
            all_records = []
            for sid, trans in sessions.items():
                records = build_action_histories(trans, K)
                all_records.extend(records)
            
            pmi_stats = compute_conditional_pmi(all_records, K)
            accuracy = compute_prediction_accuracy(all_records, K)
            perm = permutation_test(sessions, K, N_PERMUTATIONS, SEED)
            
            k_results[K] = {
                "pmi": pmi_stats["pmi"],
                "n_strata": pmi_stats["n_strata"],
                "n_used": pmi_stats["n_used"],
                "total": pmi_stats["total"],
                "skipped_small": pmi_stats["skipped_small"],
                "skipped_zero_var": pmi_stats["skipped_zero_var"],
                "permutation_p": perm["p_value"],
                "null_mean": perm["null_mean"],
                "null_std": perm["null_std"],
                "effect_size_d": perm["effect_size_d"],
                "prediction_accuracy": accuracy["accuracy"],
                "accuracy_correct": accuracy["correct"],
                "accuracy_total": accuracy["total"],
            }
            
            print(f"  K={K}: PMI={pmi_stats['pmi']:.6f}, "
                  f"perm_p={perm['p_value']:.6f}, d={perm['effect_size_d']:.4f}, "
                  f"accuracy={accuracy['accuracy']:.4f}, "
                  f"strata_used={pmi_stats['n_used']}/{pmi_stats['n_strata']}")
        
        # Normalized URL PMI (null control, K=0)
        norm_records_k0 = []
        for sid, trans in sessions.items():
            records = build_action_histories(trans, 0)
            for r in records:
                norm_records_k0.append({
                    "url_before": normalize_url(r["url_before"]),
                    "history": r["history"],
                    "action": r["action"],
                    "url_after": normalize_url(r["url_after"]),
                })
        norm_pmi = compute_conditional_pmi(norm_records_k0, 0)
        print(f"  Normalized URL PMI (K=0): {norm_pmi['pmi']:.10f} bits")
        
        variant_results[variant] = {
            "n_raw": len(raw_data),
            "n_valid": len(valid),
            "n_non_leakage": len(non_leakage),
            "k_results": k_results,
            "normalized_pmi_k0": norm_pmi["pmi"],
        }
    
    print(f"\n{'=' * 70}")
    print("DECISION EVALUATION")
    print(f"{'=' * 70}")
    
    survives = True
    decision_checks = {}
    
    # Check (1): Conditional PMI at K=3 > 0.05 AND Bonferroni p < 0.01 on >=3/5 variants
    k3_pass_count = 0
    k3_checks = {}
    for variant in VARIANTS:
        vr = variant_results[variant]
        k3 = vr["k_results"][3]
        pmi_gt = k3["pmi"] > 0.05
        p_lt_bonf = k3["permutation_p"] < ALPHA_BONFERRONI
        passes = pmi_gt and p_lt_bonf
        k3_checks[variant] = {
            "pmi": k3["pmi"], "pmi_gt_005": pmi_gt,
            "p_value": k3["permutation_p"], "p_lt_bonferroni": p_lt_bonf, "passes": passes,
        }
        if passes:
            k3_pass_count += 1
        print(f"  K=3 PMI {variant}: {k3['pmi']:.6f}, p={k3['permutation_p']:.6f}, pass={passes}")
    
    check1 = k3_pass_count >= 3
    decision_checks["C1_conditional_pmi_k3"] = {
        "n_pass": k3_pass_count, "threshold": 3, "total_variants": 5,
        "per_variant": k3_checks, "passes": check1,
    }
    if not check1:
        survives = False
    print(f"  Check 1: {k3_pass_count}/5 variants pass K=3 PMI>0.05 + p<0.01: {check1}")
    
    # Check (2): Positive control PMI at K=3 >= 1.0
    check2 = positive_control["passes"]
    decision_checks["C2_positive_control"] = {
        "pmi_k3": positive_control["pmi_k3"], "permutation_p": positive_control["permutation_p"],
        "threshold_pmi": 1.0, "passes": check2,
    }
    if not check2:
        survives = False
    print(f"  Check 2: Positive control PMI at K=3 = {positive_control['pmi_k3']:.6f} >= 1.0: {check2}")
    
    # Check (3): >= 50 NL per variant
    nl_pass_count = 0
    nl_checks = {}
    for variant in VARIANTS:
        vr = variant_results[variant]
        has_enough = vr["n_non_leakage"] >= 50
        nl_checks[variant] = {"n_non_leakage": vr["n_non_leakage"], "threshold": 50, "passes": has_enough}
        if has_enough:
            nl_pass_count += 1
        print(f"  NL count {variant}: {vr['n_non_leakage']} >= 50: {has_enough}")
    
    check3 = nl_pass_count == 5
    decision_checks["C3_non_leakage_sufficient"] = {
        "n_pass": nl_pass_count, "threshold": 5, "per_variant": nl_checks, "passes": check3,
    }
    if not check3:
        survives = False
    print(f"  Check 3: {nl_pass_count}/5 variants have >= 50 NL transitions: {check3}")
    
    # Check (4): Unconditional PMI at K=0 > 0.05 on >=3/5
    k0_pass_count = 0
    k0_checks = {}
    for variant in VARIANTS:
        vr = variant_results[variant]
        k0 = vr["k_results"][0]
        pmi_gt = k0["pmi"] > 0.05
        p_lt_bonf = k0["permutation_p"] < ALPHA_BONFERRONI
        passes = pmi_gt and p_lt_bonf
        k0_checks[variant] = {
            "pmi": k0["pmi"], "pmi_gt_005": pmi_gt,
            "p_value": k0["permutation_p"], "p_lt_bonferroni": p_lt_bonf, "passes": passes,
        }
        if passes:
            k0_pass_count += 1
        print(f"  K=0 PMI {variant}: {k0['pmi']:.6f}, p={k0['permutation_p']:.6f}, pass={passes}")
    
    check4 = k0_pass_count >= 3
    decision_checks["C4_unconditional_pmi_k0"] = {
        "n_pass": k0_pass_count, "threshold": 3, "total_variants": 5,
        "per_variant": k0_checks, "passes": check4,
    }
    if not check4:
        survives = False
    print(f"  Check 4: {k0_pass_count}/5 variants pass K=0 PMI>0.05 + p<0.01: {check4}")
    
    # Determine outcome
    any_control_fail = not check2
    any_data_fail = not check3
    
    if survives:
        outcome = "SUPPORTS"
        decision = "SURVIVES_CURRENT_TEST"
        status = "COMPLETE"
    elif any_control_fail or any_data_fail:
        outcome = "NOT_APPLICABLE"
        decision = "MEASUREMENT_INVALID"
        status = "MEASUREMENT_INVALID"
    else:
        outcome = "FALSIFIES"
        decision = "FALSIFIED-IN-SETTING"
        status = "COMPLETE"
    
    print(f"\n{'=' * 70}")
    print(f"OUTCOME: {outcome}")
    print(f"STATUS: {status}")
    print(f"DECISION: {decision}")
    print(f"{'=' * 70}")
    
    return {
        "experiment_id": EXPERIMENT_ID,
        "variant_results": variant_results,
        "positive_control": positive_control,
        "decision_checks": decision_checks,
        "survives": survives,
        "outcome": outcome,
        "status": status,
        "decision": decision,
    }

if __name__ == "__main__":
    results = run_experiment()
    out_dir = "research/experiments/EXP-PHYSICS-35290611436"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "raw_analysis_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_path}")
