#!/usr/bin/env python3
"""
EXP-PHYSICS-34348438464 — EXECUTE phase: Analysis of collected data
Runs PMI computation, permutation tests, and decision evaluation on existing data.
Reports MEASUREMENT_INVALID due to insufficient non-leakage transitions.
"""

import json
import math
import random
import collections
import os
import sys
import hashlib
from datetime import datetime, timezone

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34348438464"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0
BONFERRONI_COMPARISONS = 2
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS
MIN_NON_LEAKAGE = 30
EXPT_DIR = "research/experiments/EXP-PHYSICS-34348438464"


# ─── State Representations ───────────────────────────────────────────────────

def state_url_only(state):
    return state["url"]

def state_url_title(state):
    return (state["url"], state["title"])

def state_url_title_form(state):
    return (state["url"], state["title"], tuple(state["form_signals"]))

REPRESENTATIONS = {
    "url_only": state_url_only,
    "url_title": state_url_title,
    "url_title_form": state_url_title_form,
}


# ─── PMI Computation ─────────────────────────────────────────────────────────

def extract_triples(transitions, state_fn):
    triples = []
    for t in transitions:
        s = state_fn(t["state_before"])
        a = t["action"]["action_type"]
        s_next = state_fn(t["state_after"])
        triples.append((s, a, s_next))
    return triples


def extract_trajectory_groups(transitions, state_fn):
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(t)
    triple_groups = {}
    for tid, trans in groups.items():
        triple_groups[tid] = extract_triples(trans, state_fn)
    return triple_groups


def compute_pmi_stats(triples):
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "pmi_values": [], "N": 0,
                "unique_states": 0, "unique_actions": 0, "unique_sa_pairs": 0}

    state_counts = collections.Counter()
    state_action_counts = collections.Counter()
    state_next_counts = collections.Counter()
    triple_counts = collections.Counter()

    for s, a, s_next in triples:
        state_counts[s] += 1
        state_action_counts[(s, a)] += 1
        state_next_counts[(s, s_next)] += 1
        triple_counts[(s, a, s_next)] += 1

    pmi_values = []
    for s, a, s_next in triples:
        count_s = state_counts[s]
        count_sa = state_action_counts[(s, a)]
        count_ss_next = state_next_counts[(s, s_next)]
        count_sas_next = triple_counts[(s, a, s_next)]

        distinct_actions_s = sum(1 for (si, ai) in state_action_counts if si == s)
        distinct_next_s = sum(1 for (si, sni) in state_next_counts if si == s)

        p_a_given_s = (count_sa + ALPHA) / (count_s + ALPHA * distinct_actions_s)
        p_s_next_given_s = (count_ss_next + ALPHA) / (count_s + ALPHA * distinct_next_s)
        p_joint_given_s = count_sas_next / count_s

        denom = p_a_given_s * p_s_next_given_s
        if denom > 0 and p_joint_given_s > 0:
            pmi = math.log2(p_joint_given_s / denom)
        else:
            pmi = 0.0

        pmi_values.append(pmi)

    mean_pmi = sum(pmi_values) / len(pmi_values)

    return {
        "mean_pmi": mean_pmi,
        "pmi_values": pmi_values,
        "N": N,
        "unique_states": len(state_counts),
        "unique_actions": len(set(a for _, a, _ in triples)),
        "unique_sa_pairs": len(state_action_counts),
    }


# ─── Cross-Trajectory Permutation ────────────────────────────────────────────

def cross_trajectory_shuffle(triple_groups, rng):
    """Shuffle action labels across entire trajectories.
    
    Handles variable-length trajectories by grouping by length first,
    then shuffling action sequences within each length group.
    """
    # Group trajectories by length
    length_groups = collections.defaultdict(list)
    for tid in sorted(triple_groups.keys()):
        triples = triple_groups[tid]
        traj_len = len(triples)
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
        length_groups[traj_len].append((tid, states, actions, nexts))
    
    shuffled_groups = {}
    for traj_len, trajectories in length_groups.items():
        if len(trajectories) < 2:
            # Can't shuffle with fewer than 2 trajectories
            for tid, states, actions, nexts in trajectories:
                shuffled_groups[tid] = list(zip(states, actions, nexts))
            continue
        
        # Shuffle action sequences within this length group
        action_sequences = [a for _, _, a, _ in trajectories]
        rng.shuffle(action_sequences)
        
        for i, (tid, states, _, nexts) in enumerate(trajectories):
            shuffled_actions = action_sequences[i]
            shuffled_groups[tid] = [(states[j], shuffled_actions[j], nexts[j])
                                    for j in range(len(states))]
    
    return shuffled_groups


def permutation_test(triple_groups, observed_mean_pmi, n_permutations, seed):
    rng = random.Random(seed)

    shuffled_means = []
    for _ in range(n_permutations):
        shuffled_groups = cross_trajectory_shuffle(triple_groups, rng)
        all_shuffled = []
        for triples in shuffled_groups.values():
            all_shuffled.extend(triples)
        stats = compute_pmi_stats(all_shuffled)
        shuffled_means.append(stats["mean_pmi"])

    count_gt = sum(1 for m in shuffled_means if m > observed_mean_pmi)
    p_value = (count_gt + 1) / (n_permutations + 1)

    null_mean = float(np.mean(shuffled_means))
    null_std = float(np.std(shuffled_means))
    effect_d = float((observed_mean_pmi - null_mean) / null_std) if null_std > 0 else 0.0

    return {
        "p_value": p_value,
        "shuffled_means": shuffled_means,
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
    }


# ─── Synthetic Positive Control ──────────────────────────────────────────────

SYNTHETIC_STATES = {
    0: {"url": "http://spa.test/form", "title": "Checkout Form",
        "form_signals": [1, 1, 1, 0]},
    1: {"url": "http://spa.test/form", "title": "Login Form",
        "form_signals": [1, 1, 1, 0]},
    2: {"url": "http://spa.test/form", "title": "Registration Form",
        "form_signals": [1, 1, 1, 1]},
    3: {"url": "http://spa.test/dashboard", "title": "User Dashboard",
        "form_signals": [0, 0, 0, 0]},
    4: {"url": "http://spa.test/dashboard", "title": "Admin Dashboard",
        "form_signals": [0, 1, 0, 0]},
    5: {"url": "http://spa.test/dashboard", "title": "Analytics Dashboard",
        "form_signals": [0, 0, 0, 0]},
    6: {"url": "http://spa.test/settings", "title": "Account Settings",
        "form_signals": [1, 0, 0, 0]},
    7: {"url": "http://spa.test/settings", "title": "Privacy Settings",
        "form_signals": [1, 1, 0, 0]},
}

SYNTHETIC_ACTIONS = ["form_submit", "button_click", "link_nav", "menu_select"]

SYNTHETIC_TRANSITIONS_MAP = {
    0: {"form_submit": 3, "button_click": 4, "link_nav": 6, "menu_select": 7},
    1: {"form_submit": 5, "button_click": 3, "link_nav": 4, "menu_select": 6},
    2: {"form_submit": 3, "button_click": 5, "link_nav": 7, "menu_select": 4},
    3: {"form_submit": 0, "button_click": 1, "link_nav": 2, "menu_select": 6},
    4: {"form_submit": 1, "button_click": 2, "link_nav": 0, "menu_select": 7},
    5: {"form_submit": 2, "button_click": 0, "link_nav": 1, "menu_select": 6},
    6: {"form_submit": 3, "button_click": 4, "link_nav": 5, "menu_select": 0},
    7: {"form_submit": 5, "button_click": 3, "link_nav": 6, "menu_select": 1},
}


def generate_synthetic_trajectories(n_trajectories, trajectory_length, rng):
    state_ids = list(SYNTHETIC_STATES.keys())
    all_transitions = []
    for traj_id in range(n_trajectories):
        current_state = rng.choice(state_ids)
        for step in range(trajectory_length):
            action = rng.choice(SYNTHETIC_ACTIONS)
            next_state = SYNTHETIC_TRANSITIONS_MAP[current_state][action]
            target_href = f"http://dummy.test/action_{action}_{current_state}_{step}"
            all_transitions.append({
                "trajectory_id": traj_id,
                "state_before": {
                    "url": SYNTHETIC_STATES[current_state]["url"],
                    "title": SYNTHETIC_STATES[current_state]["title"],
                    "form_signals": SYNTHETIC_STATES[current_state]["form_signals"],
                },
                "action": {"action_type": action, "target_href": target_href},
                "state_after": {
                    "url": SYNTHETIC_STATES[next_state]["url"],
                    "title": SYNTHETIC_STATES[next_state]["title"],
                    "form_signals": SYNTHETIC_STATES[next_state]["form_signals"],
                },
            })
            current_state = next_state
    return all_transitions


def run_positive_control(rng):
    """Run synthetic SPA positive control."""
    print("\n[CONTROL] Running positive control (synthetic SPA)...")
    
    synthetic_transitions = generate_synthetic_trajectories(
        n_trajectories=25, trajectory_length=20, rng=rng)
    
    n_leakage = sum(1 for t in synthetic_transitions 
                    if t["action"]["target_href"] == t["state_after"]["url"])
    print(f"  Synthetic transitions: {len(synthetic_transitions)}, leakage violations: {n_leakage}")
    
    triples_url = extract_triples(synthetic_transitions, state_url_only)
    stats_url = compute_pmi_stats(triples_url)
    
    triples_title = extract_triples(synthetic_transitions, state_url_title)
    stats_title = compute_pmi_stats(triples_title)
    
    triple_groups = extract_trajectory_groups(synthetic_transitions, state_url_only)
    perm = permutation_test(triple_groups, stats_url["mean_pmi"], N_PERMUTATIONS, SEED)
    
    passes = stats_url["mean_pmi"] >= 0.5
    
    print(f"  URL-only PMI: {stats_url['mean_pmi']:.6f} bits")
    print(f"  URL+title PMI: {stats_title['mean_pmi']:.6f} bits")
    print(f"  Permutation p: {perm['p_value']:.6f}")
    print(f"  Positive control passes (PMI >= 0.5): {passes}")
    
    return {
        "url_only_pmi": stats_url["mean_pmi"],
        "url_title_pmi": stats_title["mean_pmi"],
        "permutation_p": perm["p_value"],
        "effect_size_d": perm["effect_size_d"],
        "passes": passes,
        "n_transitions": len(synthetic_transitions),
    }


def classify_non_leakage(transitions):
    non_leakage = []
    leakage_count = 0
    for t in transitions:
        if t["action"]["target_href"] == t["state_after"]["url"]:
            leakage_count += 1
        else:
            non_leakage.append(t)
    return non_leakage, leakage_count


def analyze_site(site_key, site_name, transitions):
    """Full PMI analysis for a single site's transitions."""
    print(f"\n  === {site_name} ({site_key}) ===")
    
    # Classify non-leakage
    non_leakage, n_leakage = classify_non_leakage(transitions)
    print(f"  Total transitions: {len(transitions)}")
    print(f"  Non-leakage: {len(non_leakage)}")
    print(f"  Leakage: {n_leakage}")
    print(f"  Leakage fraction: {n_leakage/len(transitions):.1%}")
    
    if len(non_leakage) < MIN_NON_LEAKAGE:
        print(f"  WARNING: Below {MIN_NON_LEAKAGE} threshold. MEASUREMENT_INVALID for this site.")
    
    # Compute PMI for all representations
    pmi_results = {}
    for rep_name, state_fn in REPRESENTATIONS.items():
        triples = extract_triples(non_leakage, state_fn)
        stats = compute_pmi_stats(triples)
        pmi_results[rep_name] = stats
        print(f"    {rep_name}: mean_PMI = {stats['mean_pmi']:.6f} bits, "
              f"N = {stats['N']}, unique_states = {stats['unique_states']}, "
              f"unique_SA = {stats['unique_sa_pairs']}")
    
    # Permutation tests (only if enough trajectories for shuffling)
    perm_tests = {}
    traj_ids = sorted(set(t["trajectory_id"] for t in non_leakage))
    n_trajectories = len(traj_ids)
    
    if n_trajectories >= 3:
        for rep_name, state_fn in REPRESENTATIONS.items():
            triple_groups = extract_trajectory_groups(non_leakage, state_fn)
            obs_mean = pmi_results[rep_name]["mean_pmi"]
            perm = permutation_test(triple_groups, obs_mean, N_PERMUTATIONS, SEED)
            perm_tests[rep_name] = perm
            print(f"    Permutation {rep_name}: p = {perm['p_value']:.6f}, "
                  f"effect_d = {perm['effect_size_d']:.4f}")
    else:
        print(f"    Skipping permutation tests (only {n_trajectories} trajectories)")
        for rep_name in REPRESENTATIONS:
            perm_tests[rep_name] = {
                "p_value": 1.0, "observed_mean_pmi": pmi_results[rep_name]["mean_pmi"],
                "null_mean": 0.0, "null_std": 1.0, "effect_size_d": 0.0,
                "shuffled_means": [],
            }
    
    # Null control
    if n_trajectories >= 3:
        url_title_shuffled = perm_tests["url_title"]["shuffled_means"]
        url_title_observed = perm_tests["url_title"]["observed_mean_pmi"]
        count_shuffled_gt = sum(1 for m in url_title_shuffled if m > url_title_observed)
        null_p_value_gt = count_shuffled_gt / N_PERMUTATIONS if N_PERMUTATIONS > 0 else 1.0
        null_passes = count_shuffled_gt < (0.05 * N_PERMUTATIONS)
    else:
        count_shuffled_gt = 0
        null_p_value_gt = 1.0
        null_passes = False
    
    print(f"    Null control: shuffled > observed: {count_shuffled_gt}/{N_PERMUTATIONS}")
    print(f"    Null control P(shuffled > observed): {null_p_value_gt:.6f}, passes={null_passes}")
    
    # Representation comparison
    url_only_pmi = pmi_results["url_only"]["mean_pmi"]
    url_title_pmi = pmi_results["url_title"]["mean_pmi"]
    url_title_form_pmi = pmi_results["url_title_form"]["mean_pmi"]
    richer_than_url = url_title_pmi > url_only_pmi or url_title_form_pmi > url_only_pmi
    
    print(f"    URL-only PMI: {url_only_pmi:.6f}")
    print(f"    URL+title PMI: {url_title_pmi:.6f}")
    print(f"    URL+title+form PMI: {url_title_form_pmi:.6f}")
    print(f"    Richer > URL-only: {richer_than_url}")
    
    # Title analysis
    titles = [t["state_before"]["title"] for t in non_leakage]
    unique_titles = len(set(titles))
    print(f"    Unique titles (non-leakage): {unique_titles}/{len(titles)}")
    
    # Action type distribution
    action_types = collections.Counter(t["action"]["action_type"] for t in non_leakage)
    print(f"    Action types: {dict(action_types)}")
    
    # URL/title form signals variance
    form_sigs = set(tuple(t["state_before"]["form_signals"]) for t in non_leakage)
    print(f"    Unique form_signals: {len(form_sigs)}")
    
    return {
        "name": site_name,
        "n_raw_transitions": len(transitions),
        "n_non_leakage": len(non_leakage),
        "n_leakage": n_leakage,
        "leakage_fraction": n_leakage / len(transitions) if transitions else 0,
        "n_trajectories": n_trajectories,
        "pmi_by_representation": {
            rep: {
                "mean_pmi": stats["mean_pmi"],
                "N": stats["N"],
                "unique_states": stats["unique_states"],
                "unique_actions": stats["unique_actions"],
                "unique_sa_pairs": stats["unique_sa_pairs"],
            }
            for rep, stats in pmi_results.items()
        },
        "permutation_tests": {
            rep: {
                "observed_pmi": perm["observed_mean_pmi"],
                "p_value": perm["p_value"],
                "null_mean": perm["null_mean"],
                "null_std": perm["null_std"],
                "effect_size_d": perm["effect_size_d"],
            }
            for rep, perm in perm_tests.items()
        },
        "null_control": {
            "shuffled_gt_observed": count_shuffled_gt,
            "p_value": null_p_value_gt,
            "passes": null_passes,
        },
        "representation_comparison": {
            "url_only_pmi": url_only_pmi,
            "url_title_pmi": url_title_pmi,
            "url_title_form_pmi": url_title_form_pmi,
            "richer_than_url": richer_than_url,
            "url_title_improvement_pct": ((url_title_pmi - url_only_pmi) / url_only_pmi * 100) if url_only_pmi > 0 else 0,
        },
        "title_analysis": {
            "unique_titles": unique_titles,
            "total_titles": len(titles),
        },
        "action_type_distribution": dict(action_types),
        "form_signals_variance": len(form_sigs),
    }


def run_experiment():
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — Real SPA Title-Aware PMI")
    print("=" * 70)
    
    rng = random.Random(SEED)
    os.environ["PYTHONHASHSEED"] = "0"
    
    # ── Step 1: Positive control ──
    positive_control = run_positive_control(rng)
    if not positive_control["passes"]:
        print("\nFATAL: Positive control failed.")
        return None
    
    # ── Step 2: Load and analyze browser data ──
    all_data_path = os.path.join(EXPT_DIR, "all_browser_transitions.json")
    with open(all_data_path) as f:
        all_data = json.load(f)
    
    site_results = {}
    for site_key, site_data in all_data.items():
        site_name = {"github": "GitHub", "mdn": "MDN Web Docs"}.get(site_key, site_key)
        site_results[site_key] = analyze_site(
            site_key, site_name, site_data["raw_transitions"])
    
    # ── Step 3: Decision evaluation ──
    print(f"\n{'=' * 70}")
    print("DECISION EVALUATION (frozen rules)")
    print(f"{'=' * 70}")
    
    survives = True
    decision_checks = {}
    
    # Check 1: Positive control
    decision_checks["positive_control"] = {
        "url_only_pmi": positive_control["url_only_pmi"],
        "passes": positive_control["passes"],
    }
    if not positive_control["passes"]:
        survives = False
    print(f"  [1] Positive control PMI >= 0.5: {positive_control['url_only_pmi']:.6f}, "
          f"pass={positive_control['passes']}")
    
    # Check 2: Data sufficiency
    for site_key, sr in site_results.items():
        has_sufficient = sr["n_non_leakage"] >= MIN_NON_LEAKAGE
        decision_checks[f"data_sufficiency_{site_key}"] = {
            "n_non_leakage": sr["n_non_leakage"],
            "threshold": MIN_NON_LEAKAGE,
            "passes": has_sufficient,
        }
        if not has_sufficient:
            survives = False
        print(f"  [2] Data sufficiency {site_key}: {sr['n_non_leakage']} >= {MIN_NON_LEAKAGE}, "
              f"pass={has_sufficient}")
    
    # Check 3: URL+title > URL-only on both sites
    url_title_better_count = 0
    for site_key, sr in site_results.items():
        rc = sr["representation_comparison"]
        url_title_better = rc["url_title_pmi"] > rc["url_only_pmi"]
        url_title_better_count += int(url_title_better)
        decision_checks[f"representation_{site_key}"] = {
            "url_only_pmi": rc["url_only_pmi"],
            "url_title_pmi": rc["url_title_pmi"],
            "url_title_better": url_title_better,
        }
        print(f"  [3] URL+title > URL-only {site_key}: {rc['url_title_pmi']:.6f} > "
              f"{rc['url_only_pmi']:.6f}, pass={url_title_better}")
    
    both_sites_title_better = url_title_better_count == 2
    if not both_sites_title_better:
        survives = False
    print(f"  [3] Both sites: {both_sites_title_better}")
    
    # Check 4: URL+title PMI > 0.5 on at least one site
    any_title_above = any(
        sr["representation_comparison"]["url_title_pmi"] > 0.5
        for sr in site_results.values()
    )
    decision_checks["title_above_threshold"] = {"any_site": any_title_above, "threshold": 0.5}
    if not any_title_above:
        survives = False
    print(f"  [4] URL+title PMI > 0.5 on any site: {any_title_above}")
    
    # Check 5: Permutation p < 0.001 on at least one site
    any_perm_sig = any(
        sr["permutation_tests"].get("url_title", {}).get("p_value", 1.0) < 0.001
        for sr in site_results.values()
    )
    decision_checks["permutation_significance"] = {"any_site": any_perm_sig, "threshold": 0.001}
    if not any_perm_sig:
        survives = False
    print(f"  [5] Permutation p < 0.001 on any site: {any_perm_sig}")
    
    # Determine outcome
    any_insufficient = any(sr["n_non_leakage"] < MIN_NON_LEAKAGE for sr in site_results.values())
    
    if survives:
        status = "COMPLETE"
        outcome = "SUPPORTS"
    elif any_insufficient:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    else:
        status = "COMPLETE"
        outcome = "FALSIFIES"
    
    print(f"\n{'=' * 70}")
    print(f"STATUS: {status}")
    print(f"OUTCOME: {outcome}")
    print(f"{'=' * 70}")
    
    return {
        "experiment_id": EXPERIMENT_ID,
        "positive_control": positive_control,
        "site_results": site_results,
        "decision_checks": decision_checks,
        "survives": survives,
        "outcome": outcome,
        "status": status,
    }


if __name__ == "__main__":
    results = run_experiment()
    if results is None:
        print("Experiment failed.")
        sys.exit(1)
    
    out_path = os.path.join(EXPT_DIR, "raw_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_path}")
