#!/usr/bin/env python3
"""
EXP-PHYSICS-34724244876 — Conditional PMI Analysis

Computes I(S_next; DOM | URL, ActionHistory) on 3 deterministic SPAs
to test whether DOM adds predictive value beyond action-history memory.

Frozen preregistration: research/experiments/EXP-PHYSICS-34724244876/prereg.md
"""

import json
import math
import os
import sys
from collections import Counter, defaultdict

# Deterministic seed for reproducibility
import random
random.seed(42)

# ── Configuration ──────────────────────────────────────────────────────────
RAW_DATA_PATH = "research/experiments/EXP-PHYSICS-34719136202/raw_dom_captures.json"
OUTPUT_DIR = "research/experiments/EXP-PHYSICS-34724244876"
SPAS = ["dashboard", "multistep_form", "wizard"]
HISTORY_LENGTHS = [1, 2, 3]
N_PERMUTATIONS = 1000
ALPHA = 0.05
N_SITES = 3
BONFERRONI_ALPHA = ALPHA / N_SITES  # 0.0167
START_TOKEN = "<START>"
MIN_STRATUM_COUNT = 5  # minimum transitions per stratum for valid computation


def load_data():
    """Load raw DOM captures from parent experiment."""
    with open(RAW_DATA_PATH) as f:
        data = json.load(f)
    return data


def get_action_label(action):
    """Extract a hashable action label from action dict."""
    return f"{action['type']}:{action['target_href']}"


def build_action_histories(transitions, K):
    """Build action history sequences of length K for each transition.
    
    For transitions at step t in a trajectory:
    - History is the sequence of last K action labels (including current).
    - For t < K-1, pad with START_TOKEN at the beginning.
    """
    histories = []
    for t in transitions:
        traj = t["trajectory_id"]
        step = t["step"]
        action = get_action_label(t["action"])
        histories.append(action)  # will rebuild below
    
    # Group by trajectory to get proper sequences
    trajectories = defaultdict(list)
    for t in transitions:
        trajectories[t["trajectory_id"]].append(t)
    
    history_map = {}  # (trajectory_id, step) -> action history tuple
    for traj_id, steps in trajectories.items():
        steps_sorted = sorted(steps, key=lambda x: x["step"])
        action_seq = [get_action_label(s["action"]) for s in steps_sorted]
        for i, s in enumerate(steps_sorted):
            # Build history of length K ending at position i
            start = max(0, i - K + 1)
            hist = action_seq[start:i+1]
            # Pad with START_TOKEN if needed
            while len(hist) < K:
                hist = [START_TOKEN] + hist
            history_map[(traj_id, s["step"])] = tuple(hist)
    
    return history_map


def compute_conditional_pmi(transitions, history_map):
    """Compute I(S_next; DOM | URL, ActionHistory) via empirical conditional PMI.
    
    For each action-history stratum h, compute:
        PMI_h = sum_{r,s} P(r,s|h) * log2[P(r,s|h) / (P(r|h) * P(s|h))]
    
    Then average across strata weighted by stratum frequency.
    """
    # Group transitions by action-history stratum
    strata = defaultdict(list)
    for t in transitions:
        key = (t["trajectory_id"], t["step"])
        h = history_map[key]
        strata[h].append(t)
    
    total_pmi = 0.0
    total_weight = 0
    stratum_details = {}
    
    for h, h_transitions in strata.items():
        n_h = len(h_transitions)
        if n_h < MIN_STRATUM_COUNT:
            continue
        
        # Compute P(r, s | h), P(r | h), P(s | h)
        joint = Counter()
        marginal_r = Counter()
        marginal_s = Counter()
        
        for t in h_transitions:
            r = t["state_before"]["dom_features"]["visible_text_hash"]
            s = t["state_after"]["dom_features"]["visible_text_hash"]
            joint[(r, s)] += 1
            marginal_r[r] += 1
            marginal_s[s] += 1
        
        # Compute PMI for this stratum
        stratum_pmi = 0.0
        for (r, s), count in joint.items():
            p_rs = count / n_h
            p_r = marginal_r[r] / n_h
            p_s = marginal_s[s] / n_h
            if p_rs > 0 and p_r > 0 and p_s > 0:
                stratum_pmi += p_rs * math.log2(p_rs / (p_r * p_s))
        
        weight = n_h / len(transitions)
        total_pmi += weight * stratum_pmi
        total_weight += n_h
        
        stratum_details[str(h)] = {
            "count": n_h,
            "pmi": stratum_pmi,
            "n_joint": len(joint),
            "n_marginal_r": len(marginal_r),
            "n_marginal_s": len(marginal_s),
        }
    
    return total_pmi, stratum_details, total_weight


def compute_unconditional_pmi(transitions):
    """Compute I(S_next; DOM | URL) — unconditional PMI (URL is structural zero)."""
    joint = Counter()
    marginal_r = Counter()
    marginal_s = Counter()
    
    for t in transitions:
        r = t["state_before"]["dom_features"]["visible_text_hash"]
        s = t["state_after"]["dom_features"]["visible_text_hash"]
        joint[(r, s)] += 1
        marginal_r[r] += 1
        marginal_s[s] += 1
    
    n = len(transitions)
    pmi = 0.0
    for (r, s), count in joint.items():
        p_rs = count / n
        p_r = marginal_r[r] / n
        p_s = marginal_s[s] / n
        if p_rs > 0 and p_r > 0 and p_s > 0:
            pmi += p_rs * math.log2(p_rs / (p_r * p_s))
    
    return pmi, {"n_transitions": n, "n_joint": len(joint), "n_r": len(marginal_r), "n_s": len(marginal_s)}


def permutation_test_conditional_pmi(transitions, history_map, n_perms=N_PERMUTATIONS):
    """Shuffle DOM labels within action-history strata, recompute conditional PMI.
    
    This preserves the action-history distribution while destroying DOM-S_next association.
    """
    # Group by stratum
    strata = defaultdict(list)
    for t in transitions:
        key = (t["trajectory_id"], t["step"])
        h = history_map[key]
        strata[h].append(t)
    
    perm_pmis = []
    for perm_i in range(n_perms):
        # Shuffle DOM labels within each stratum
        shuffled_transitions = []
        for h, h_trans in strata.items():
            # Extract DOM before hashes and shuffle them
            dom_before = [t["state_before"]["dom_features"]["visible_text_hash"] for t in h_trans]
            random.shuffle(dom_before)
            for i, t in enumerate(h_trans):
                t_copy = dict(t)
                t_copy["state_before"] = dict(t["state_before"])
                t_copy["state_before"]["dom_features"] = dict(t["state_before"]["dom_features"])
                t_copy["state_before"]["dom_features"]["visible_text_hash"] = dom_before[i]
                shuffled_transitions.append(t_copy)
        
        # Compute conditional PMI on shuffled data
        perm_pmi, _, _ = compute_conditional_pmi(shuffled_transitions, history_map)
        perm_pmis.append(perm_pmi)
    
    return perm_pmis


def compute_action_history_prediction(transitions, history_map):
    """Compute accuracy of predicting S_next from ActionHistory alone.
    
    For each stratum h, predict the most frequent S_next.
    """
    strata = defaultdict(list)
    for t in transitions:
        key = (t["trajectory_id"], t["step"])
        h = history_map[key]
        strata[h].append(t)
    
    correct = 0
    total = 0
    stratum_accuracy = {}
    
    for h, h_trans in strata.items():
        n_h = len(h_trans)
        if n_h < MIN_STRATUM_COUNT:
            continue
        
        # Most frequent S_next in this stratum
        s_next_counts = Counter()
        for t in h_trans:
            s_next = t["state_after"]["dom_features"]["visible_text_hash"]
            s_next_counts[s_next] += 1
        
        most_frequent = s_next_counts.most_common(1)[0][0]
        stratum_correct = sum(1 for t in h_trans 
                             if t["state_after"]["dom_features"]["visible_text_hash"] == most_frequent)
        
        correct += stratum_correct
        total += n_h
        stratum_accuracy[str(h)] = {
            "count": n_h,
            "accuracy": stratum_correct / n_h if n_h > 0 else 0,
            "most_frequent_s_next": most_frequent,
        }
    
    return correct / total if total > 0 else 0, stratum_accuracy, total


def compute_determinism_check(transitions):
    """Check if P(S_next | S_current, Action) is deterministic (100% accuracy).
    
    On deterministic SPAs, each (S_current, Action) pair should map to exactly one S_next.
    """
    state_action_to_snext = defaultdict(Counter)
    for t in transitions:
        s_current = t["state_before"]["dom_features"]["visible_text_hash"]
        action = get_action_label(t["action"])
        s_next = t["state_after"]["dom_features"]["visible_text_hash"]
        state_action_to_snext[(s_current, action)][s_next] += 1
    
    total = 0
    deterministic = 0
    details = {}
    for (s, a), snext_counts in state_action_to_snext.items():
        n = sum(snext_counts.values())
        most_common_count = snext_counts.most_common(1)[0][1]
        acc = most_common_count / n
        details[f"({s}, {a})"] = {
            "count": n,
            "accuracy": acc,
            "n_unique_next": len(snext_counts),
            "distribution": dict(snext_counts),
        }
        total += n
        deterministic += most_common_count
    
    return deterministic / total if total > 0 else 0, details, total


def frequency_null_accuracy(transitions):
    """Baseline: predict S_next from marginal P(S_next). Expected: 1/|S|."""
    s_next_counts = Counter()
    for t in transitions:
        s_next = t["state_after"]["dom_features"]["visible_text_hash"]
        s_next_counts[s_next] += 1
    
    most_frequent_count = s_next_counts.most_common(1)[0][1]
    return most_frequent_count / len(transitions), dict(s_next_counts)


def compute_synthetic_conditional_pmi(data):
    """Positive control: synthetic SPA where DOM is independent of action history.
    
    Conditional PMI should be zero (pipeline correctly detects independence).
    """
    synthetic = data["synthetic"]
    # Build history map for synthetic
    history_map = build_action_histories(synthetic, K=1)
    pmi, details, weight = compute_conditional_pmi(synthetic, history_map)
    return pmi, details, weight


def main():
    print("=" * 70)
    print("EXP-PHYSICS-34724244876 — Conditional PMI Analysis")
    print("=" * 70)
    
    data = load_data()
    results = {
        "site_results": {},
        "synthetic_control": {},
        "controls": {},
    }
    
    all_site_pass = True
    
    for spa in SPAS:
        print(f"\n{'─' * 50}")
        print(f"Site: {spa}")
        print(f"{'─' * 50}")
        transitions = data[spa]
        print(f"  Transitions: {len(transitions)}")
        
        spa_result = {"n_transitions": len(transitions)}
        
        # ── Unconditional PMI ──
        uncond_pmi, uncond_details = compute_unconditional_pmi(transitions)
        spa_result["unconditional_pmi"] = uncond_pmi
        spa_result["unconditional_details"] = uncond_details
        print(f"  Unconditional PMI: {uncond_pmi:.4f} bits")
        
        # ── Determinism check ──
        det_acc, det_details, det_total = compute_determinism_check(transitions)
        spa_result["determinism_accuracy"] = det_acc
        spa_result["determinism_details"] = det_details
        spa_result["determinism_total"] = det_total
        print(f"  Determinism (S_current,Action)->S_next accuracy: {det_acc:.4f} ({det_total} transitions)")
        
        if det_acc < 1.0:
            print(f"  WARNING: Determinism check failed! SPA may not be deterministic.")
            all_site_pass = False
        
        # ── Frequency null ──
        freq_acc, freq_dist = frequency_null_accuracy(transitions)
        spa_result["frequency_null_accuracy"] = freq_acc
        spa_result["frequency_distribution"] = freq_dist
        print(f"  Frequency null accuracy: {freq_acc:.4f}")
        
        # ── Conditional PMI for each history length ──
        spa_result["conditional_pmi"] = {}
        spa_result["permutation_tests"] = {}
        spa_result["action_history_prediction"] = {}
        
        for K in HISTORY_LENGTHS:
            print(f"\n  History length K={K}:")
            
            history_map = build_action_histories(transitions, K)
            
            # Conditional PMI
            cond_pmi, stratum_details, weight = compute_conditional_pmi(transitions, history_map)
            spa_result["conditional_pmi"][f"K{K}"] = {
                "value": cond_pmi,
                "stratum_details": stratum_details,
                "weighted_transitions": weight,
            }
            print(f"    Conditional PMI: {cond_pmi:.6f} bits")
            print(f"    Strata with sufficient data: {len(stratum_details)}")
            
            # Action-history prediction accuracy
            ah_acc, ah_details, ah_total = compute_action_history_prediction(transitions, history_map)
            spa_result["action_history_prediction"][f"K{K}"] = {
                "accuracy": ah_acc,
                "details": ah_details,
                "total": ah_total,
            }
            print(f"    Action-history prediction accuracy: {ah_acc:.4f} ({ah_total} transitions)")
            
            # Permutation test
            perm_pmis = permutation_test_conditional_pmi(transitions, history_map, n_perms=N_PERMUTATIONS)
            n_exceed = sum(1 for p in perm_pmis if p >= cond_pmi)
            p_value = n_exceed / N_PERMUTATIONS
            
            spa_result["permutation_tests"][f"K{K}"] = {
                "observed_pmi": cond_pmi,
                "n_exceed": n_exceed,
                "n_perms": N_PERMUTATIONS,
                "p_value": p_value,
                "p_value_bonferroni": min(p_value * N_SITES, 1.0),
                "perm_mean": sum(perm_pmis) / len(perm_pmis),
                "perm_std": (sum((p - sum(perm_pmis)/len(perm_pmis))**2 for p in perm_pmis) / len(perm_pmis))**0.5,
                "perm_pmi_values_sample": perm_pmis[:20],  # first 20 for raw evidence
            }
            print(f"    Permutation p-value: {p_value:.4f} (Bonferroni: {min(p_value * N_SITES, 1.0):.4f})")
            
            # Delta (unconditional - conditional)
            delta = uncond_pmi - cond_pmi
            spa_result["conditional_pmi"][f"K{K}"]["delta_unconditional_minus_conditional"] = delta
            print(f"    Delta (uncond - cond): {delta:.6f} bits")
        
        results["site_results"][spa] = spa_result
    
    # ── Synthetic positive control ──
    print(f"\n{'─' * 50}")
    print("Positive Control: Synthetic SPA")
    print(f"{'─' * 50}")
    syn_pmi, syn_details, syn_weight = compute_synthetic_conditional_pmi(data)
    results["synthetic_control"] = {
        "conditional_pmi": syn_pmi,
        "stratum_details": syn_details,
        "weighted_transitions": syn_weight,
        "expected": 0.0,
        "pass": syn_pmi <= 0.1,
    }
    print(f"  Synthetic conditional PMI: {syn_pmi:.6f} bits (expected ~0)")
    print(f"  Control pass: {results['synthetic_control']['pass']}")
    
    # ── Null control: shuffled DOM on real data (using K=1 for dashboard) ──
    print(f"\n{'─' * 50}")
    print("Null Control: Shuffled DOM labels (dashboard, K=1)")
    print(f"{'─' * 50}")
    dashboard_trans = data["dashboard"]
    hist_map_d = build_action_histories(dashboard_trans, K=1)
    null_perm_pmis = permutation_test_conditional_pmi(dashboard_trans, hist_map_d, n_perms=100)
    null_mean = sum(null_perm_pmis) / len(null_perm_pmis)
    results["null_control"] = {
        "site": "dashboard",
        "K": 1,
        "null_perm_mean_pmi": null_mean,
        "null_perm_pmis_sample": null_perm_pmis[:20],
        "expected": 0.0,
        "pass": null_mean <= 0.1,
    }
    print(f"  Shuffled DOM mean PMI: {null_mean:.6f} bits (expected ~0)")
    print(f"  Control pass: {results['null_control']['pass']}")
    
    # ── Summary assessment ──
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    
    # Decision criteria (spec.json):
    # SURVIVES_CURRENT_TEST if:
    #   1. Conditional PMI > 0.1 bits on >= 2/3 sites
    #   2. Bonferroni p < 0.0167 on those sites
    #   3. No pipeline errors
    #   4. Determinism control passes
    
    sites_surviving = 0
    for spa in SPAS:
        spa_r = results["site_results"][spa]
        # Use K=1 (most conservative — shortest history)
        cond_pmi_k1 = spa_r["conditional_pmi"]["K1"]["value"]
        perm_test_k1 = spa_r["permutation_tests"]["K1"]
        passes_pmi = cond_pmi_k1 > 0.1
        passes_perm = perm_test_k1["p_value_bonferroni"] < BONFERRONI_ALPHA
        det_passes = spa_r["determinism_accuracy"] >= 1.0
        
        spa_survives = passes_pmi and passes_perm and det_passes
        if spa_survives:
            sites_surviving += 1
        
        print(f"\n  {spa}:")
        print(f"    Conditional PMI (K=1): {cond_pmi_k1:.6f} bits {'> 0.1' if passes_pmi else '<= 0.1'}")
        print(f"    Bonferroni p: {perm_test_k1['p_value_bonferroni']:.4f} {'< 0.0167' if passes_perm else '>= 0.0167'}")
        print(f"    Determinism: {spa_r['determinism_accuracy']:.4f} {'PASS' if det_passes else 'FAIL'}")
        print(f"    Survives: {spa_survives}")
    
    print(f"\n  Sites surviving: {sites_surviving}/{N_SITES}")
    
    if sites_surviving >= 2:
        verdict = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
    elif not all_site_pass:
        verdict = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    else:
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
    
    print(f"  Overall verdict: {verdict}")
    print(f"  Outcome: {outcome}")
    
    results["summary"] = {
        "verdict": verdict,
        "outcome": outcome,
        "sites_surviving_pmi_threshold": sites_surviving,
        "n_sites": N_SITES,
        "determinism_control_passes": all_site_pass,
        "synthetic_control_passes": results["synthetic_control"]["pass"],
        "null_control_passes": results["null_control"]["pass"],
        "bonferroni_alpha": BONFERRONI_ALPHA,
        "pmi_threshold": 0.1,
    }
    
    # Save raw results
    output_path = os.path.join(OUTPUT_DIR, "raw_analysis_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nRaw results saved to {output_path}")
    
    return results


if __name__ == "__main__":
    main()
