#!/usr/bin/env python3
"""
EXP-PHYSICS-34149195420 — SPA PMI Analysis: Richer State Representations
Tests whether PMI between actions and next-states detects genuine dynamical
structure in non-leakage SPA transitions when the state representation is
enriched beyond URL to include title and form signals.

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

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34149195420"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
BONFERRONI_COMPARISONS = 2  # URL+title, URL+title+form_signals
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.025

# ─── Synthetic SPA Model ─────────────────────────────────────────────────────

# 8 states, 3 unique URLs repeated with different titles
# Each state has 4 actions leading to specific next states
STATES = {
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

ACTIONS = ["form_submit", "button_click", "link_nav", "menu_select"]

# Deterministic transition mapping: (state, action) -> next_state
# Designed so that same URL states have different action->next-state mappings
TRANSITIONS = {
    0: {"form_submit": 3, "button_click": 4, "link_nav": 6, "menu_select": 7},
    1: {"form_submit": 5, "button_click": 3, "link_nav": 4, "menu_select": 6},
    2: {"form_submit": 3, "button_click": 5, "link_nav": 7, "menu_select": 4},
    3: {"form_submit": 0, "button_click": 1, "link_nav": 2, "menu_select": 6},
    4: {"form_submit": 1, "button_click": 2, "link_nav": 0, "menu_select": 7},
    5: {"form_submit": 2, "button_click": 0, "link_nav": 1, "menu_select": 6},
    6: {"form_submit": 3, "button_click": 4, "link_nav": 5, "menu_select": 0},
    7: {"form_submit": 5, "button_click": 3, "link_nav": 6, "menu_select": 1},
}

# Positive control: 8 states with unique URLs (no ambiguity)
POSITIVE_STATES = {
    0: {"url": "http://unique0.test/page", "title": "Page A",
        "form_signals": [1, 0, 0, 0]},
    1: {"url": "http://unique1.test/page", "title": "Page B",
        "form_signals": [0, 1, 0, 0]},
    2: {"url": "http://unique2.test/page", "title": "Page C",
        "form_signals": [0, 0, 1, 0]},
    3: {"url": "http://unique3.test/page", "title": "Page D",
        "form_signals": [0, 0, 0, 1]},
    4: {"url": "http://unique4.test/page", "title": "Page E",
        "form_signals": [1, 1, 0, 0]},
    5: {"url": "http://unique5.test/page", "title": "Page F",
        "form_signals": [0, 1, 1, 0]},
    6: {"url": "http://unique6.test/page", "title": "Page G",
        "form_signals": [1, 0, 0, 1]},
    7: {"url": "http://unique7.test/page", "title": "Page H",
        "form_signals": [0, 0, 1, 1]},
}

POSITIVE_TRANSITIONS = {
    0: {"form_submit": 1, "button_click": 2, "link_nav": 3, "menu_select": 4},
    1: {"form_submit": 5, "button_click": 6, "link_nav": 7, "menu_select": 0},
    2: {"form_submit": 3, "button_click": 4, "link_nav": 0, "menu_select": 1},
    3: {"form_submit": 7, "button_click": 0, "link_nav": 1, "menu_select": 2},
    4: {"form_submit": 6, "button_click": 7, "link_nav": 0, "menu_select": 3},
    5: {"form_submit": 2, "button_click": 3, "link_nav": 4, "menu_select": 5},
    6: {"form_submit": 0, "button_click": 1, "link_nav": 2, "menu_select": 6},
    7: {"form_submit": 4, "button_click": 5, "link_nav": 6, "menu_select": 7},
}


# ─── Data Generation ─────────────────────────────────────────────────────────

def generate_trajectories(states, transitions, n_trajectories, trajectory_length, rng):
    """Generate trajectories of (state, action, next_state) transitions."""
    state_ids = list(states.keys())
    all_transitions = []

    for traj_id in range(n_trajectories):
        current_state = rng.choice(state_ids)
        for step in range(trajectory_length):
            action = rng.choice(ACTIONS)
            next_state = transitions[current_state][action]
            # Non-leakage by construction: target_href is a dummy that never matches
            target_href = f"http://dummy.test/action_{action}_{current_state}_{step}"
            all_transitions.append({
                "trajectory_id": traj_id,
                "state_before": {
                    "url": states[current_state]["url"],
                    "title": states[current_state]["title"],
                    "form_signals": states[current_state]["form_signals"],
                },
                "action": {
                    "action_type": action,
                    "target_href": target_href,
                },
                "state_after": {
                    "url": states[next_state]["url"],
                    "title": states[next_state]["title"],
                    "form_signals": states[next_state]["form_signals"],
                },
            })
            current_state = next_state

    return all_transitions


def verify_non_leakage(transitions):
    """Verify all transitions are non-leakage."""
    violations = 0
    for t in transitions:
        target = t["action"]["target_href"]
        actual = t["state_after"]["url"]
        if target == actual:
            violations += 1
    return violations


# ─── State Representations ───────────────────────────────────────────────────

def state_url_only(state):
    """State = URL string."""
    return state["url"]


def state_url_title(state):
    """State = (URL, title) tuple."""
    return (state["url"], state["title"])


def state_url_title_form(state):
    """State = (URL, title, form_signals) tuple."""
    return (state["url"], state["title"], tuple(state["form_signals"]))


REPRESENTATIONS = {
    "url_only": state_url_only,
    "url_title": state_url_title,
    "url_title_form": state_url_title_form,
}


# ─── PMI Computation ─────────────────────────────────────────────────────────

def extract_triples(transitions, state_fn):
    """Extract (state_repr, action, next_state_repr) triples."""
    triples = []
    for t in transitions:
        s = state_fn(t["state_before"])
        a = t["action"]["action_type"]
        s_next = state_fn(t["state_after"])
        triples.append((s, a, s_next))
    return triples


def extract_trajectory_groups(transitions, state_fn):
    """Group transitions by trajectory_id, extract triples."""
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(t)
    triple_groups = {}
    for tid, trans in groups.items():
        triple_groups[tid] = extract_triples(trans, state_fn)
    return triple_groups


def compute_pmi_stats(triples):
    """Compute PMI statistics for a set of triples.

    PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
    """
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

    Reassigns trajectory IDs to action sequences, breaking action->outcome
    dependency while preserving trajectory structure.
    """
    # Collect all trajectories as (states, actions, nexts) sequences
    trajectories = []
    for tid in sorted(triple_groups.keys()):
        triples = triple_groups[tid]
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
        trajectories.append((states, actions, nexts))

    # Shuffle action sequences across trajectories
    action_sequences = [a for _, a, _ in trajectories]
    rng.shuffle(action_sequences)

    # Reassemble with original state sequences
    shuffled_groups = {}
    for i, (tid, (states, _, nexts)) in enumerate(zip(sorted(triple_groups.keys()), trajectories)):
        shuffled_actions = action_sequences[i]
        shuffled_groups[tid] = [(states[j], shuffled_actions[j], nexts[j])
                                for j in range(len(states))]
    return shuffled_groups


def permutation_test(triple_groups, observed_mean_pmi, n_permutations, seed):
    """Cross-trajectory permutation test."""
    rng = random.Random(seed)

    shuffled_means = []
    for _ in range(n_permutations):
        shuffled_groups = cross_trajectory_shuffle(triple_groups, rng)
        all_shuffled = []
        for triples in shuffled_groups.values():
            all_shuffled.extend(triples)
        stats = compute_pmi_stats(all_shuffled)
        shuffled_means.append(stats["mean_pmi"])

    count_ge = sum(1 for m in shuffled_means if m >= observed_mean_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)

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


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full SPA PMI experiment."""
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — SPA Richer Representation PMI")
    print("=" * 70)

    rng = random.Random(SEED)

    # ── Step 1: Generate primary SPA dataset ──
    print("\n[1/8] Generating primary SPA dataset...")
    primary_transitions = generate_trajectories(
        STATES, TRANSITIONS, n_trajectories=25, trajectory_length=20, rng=rng)
    n_leakage = verify_non_leakage(primary_transitions)
    print(f"  Generated {len(primary_transitions)} transitions across 25 trajectories")
    print(f"  Non-leakage violations: {n_leakage} (expected 0)")
    assert n_leakage == 0, f"Non-leakage violation: {n_leakage}"

    # Verify structure: count unique (state, action) pairs per representation
    print("  State distribution:")
    state_counts = collections.Counter(t["state_before"]["url"] for t in primary_transitions)
    for url, count in sorted(state_counts.items()):
        print(f"    {url}: {count}")

    # ── Step 2: Generate positive control dataset ──
    print("\n[2/8] Generating positive control dataset...")
    positive_transitions = generate_trajectories(
        POSITIVE_STATES, POSITIVE_TRANSITIONS, n_trajectories=10, trajectory_length=20, rng=rng)
    n_leakage_pos = verify_non_leakage(positive_transitions)
    print(f"  Generated {len(positive_transitions)} transitions across 10 trajectories")
    print(f"  Non-leakage violations: {n_leakage_pos} (expected 0)")
    assert n_leakage_pos == 0, f"Positive control non-leakage violation: {n_leakage_pos}"

    # ── Step 3: Compute PMI for all representations on primary dataset ──
    print("\n[3/8] Computing PMI for all representations...")
    pmi_results = {}
    for rep_name, state_fn in REPRESENTATIONS.items():
        triples = extract_triples(primary_transitions, state_fn)
        stats = compute_pmi_stats(triples)
        pmi_results[rep_name] = stats
        print(f"  {rep_name}: mean_PMI = {stats['mean_pmi']:.6f} bits, N = {stats['N']}, "
              f"unique_states = {stats['unique_states']}, unique_SA = {stats['unique_sa_pairs']}")

    # ── Step 4: Cross-trajectory permutation tests on primary dataset ──
    print("\n[4/8] Running cross-trajectory permutation tests (1000 each)...")
    perm_tests = {}
    for rep_name, state_fn in REPRESENTATIONS.items():
        triple_groups = extract_trajectory_groups(primary_transitions, state_fn)
        obs_mean = pmi_results[rep_name]["mean_pmi"]
        print(f"  Running permutation test: {rep_name} (observed PMI = {obs_mean:.6f})...")
        perm = permutation_test(triple_groups, obs_mean, N_PERMUTATIONS, SEED)
        perm_tests[rep_name] = perm
        print(f"    p = {perm['p_value']:.6f}, effect_d = {perm['effect_size_d']:.4f}")

    # ── Step 5: Positive control PMI ──
    print("\n[5/8] Running positive control...")
    pos_triples = extract_triples(positive_transitions, state_url_only)
    pos_stats = compute_pmi_stats(pos_triples)
    pos_triple_groups = extract_trajectory_groups(positive_transitions, state_url_only)
    pos_perm = permutation_test(pos_triple_groups, pos_stats["mean_pmi"], N_PERMUTATIONS, SEED)
    print(f"  Positive control: PMI = {pos_stats['mean_pmi']:.6f}, p = {pos_perm['p_value']:.6f}")
    pos_passes_threshold = pos_stats["mean_pmi"] >= 0.5
    print(f"  Positive control PMI >= 0.5: {pos_passes_threshold}")

    # ── Step 6: Null control ──
    print("\n[6/8] Running null control...")
    # Null control: cross-trajectory shuffled PMI on primary dataset (URL+title representation)
    null_pmi = perm_tests["url_title"]["null_mean"]
    null_p_value = perm_tests["url_title"]["p_value"]
    null_passes = null_p_value > 0.05
    print(f"  Null control (shuffled PMI): {null_pmi:.6f}")
    print(f"  Null control p > 0.05: {null_p_value:.6f}, passes={null_passes}")

    # ── Step 7: Representation comparison ──
    print("\n[7/8] Comparing representations...")
    url_only_pmi = pmi_results["url_only"]["mean_pmi"]
    url_title_pmi = pmi_results["url_title"]["mean_pmi"]
    url_title_form_pmi = pmi_results["url_title_form"]["mean_pmi"]
    print(f"  URL-only PMI: {url_only_pmi:.6f}")
    print(f"  URL+title PMI: {url_title_pmi:.6f}")
    print(f"  URL+title+form PMI: {url_title_form_pmi:.6f}")
    richer_than_url_only = url_title_pmi > url_only_pmi or url_title_form_pmi > url_only_pmi
    print(f"  Richer > URL-only: {richer_than_url_only}")

    # ── Step 8: Decision evaluation ──
    print(f"\n{'=' * 70}")
    print("DECISION EVALUATION")
    print(f"{'=' * 70}")

    survives = True
    decision_checks = {}

    # Check 1: Positive control PMI >= 0.5 bits
    decision_checks["positive_control"] = {
        "pmi": pos_stats["mean_pmi"],
        "p_value": pos_perm["p_value"],
        "threshold": 0.5,
        "passes": pos_passes_threshold,
    }
    if not pos_passes_threshold:
        survives = False
    print(f"  Positive control PMI >= 0.5: {pos_stats['mean_pmi']:.6f}, p={pos_perm['p_value']:.6f}, pass={pos_passes_threshold}")

    # Check 2: Null control p > 0.05
    decision_checks["null_control"] = {
        "null_mean_pmi": null_pmi,
        "p_value": null_p_value,
        "passes": null_passes,
    }
    if not null_passes:
        survives = False
    print(f"  Null control p > 0.05: {null_p_value:.6f}, pass={null_passes}")

    # Check 3: At least one representation has PMI > 0 with Bonferroni-corrected p < 0.05
    url_title_sig = (url_title_pmi > 0 and perm_tests["url_title"]["p_value"] < ALPHA_BONFERRONI)
    url_title_form_sig = (url_title_form_pmi > 0 and perm_tests["url_title_form"]["p_value"] < ALPHA_BONFERRONI)
    any_sig = url_title_sig or url_title_form_sig
    decision_checks["representation_significance"] = {
        "url_title_pmi": url_title_pmi,
        "url_title_p": perm_tests["url_title"]["p_value"],
        "url_title_sig": url_title_sig,
        "url_title_form_pmi": url_title_form_pmi,
        "url_title_form_p": perm_tests["url_title_form"]["p_value"],
        "url_title_form_sig": url_title_form_sig,
        "bonferroni_threshold": ALPHA_BONFERRONI,
        "passes": any_sig,
    }
    if not any_sig:
        survives = False
    print(f"  URL+title significant: PMI={url_title_pmi:.6f}, p={perm_tests['url_title']['p_value']:.6f}, sig={url_title_sig}")
    print(f"  URL+title+form significant: PMI={url_title_form_pmi:.6f}, p={perm_tests['url_title_form']['p_value']:.6f}, sig={url_title_form_sig}")

    # Check 4: Richer representation PMI > URL-only PMI
    decision_checks["richer_vs_url_only"] = {
        "url_only_pmi": url_only_pmi,
        "url_title_pmi": url_title_pmi,
        "url_title_form_pmi": url_title_form_pmi,
        "passes": richer_than_url_only,
    }
    if not richer_than_url_only:
        survives = False
    print(f"  Richer > URL-only: {richer_than_url_only}")

    # Determine outcome
    status = "COMPLETE"
    if survives:
        outcome = "SUPPORTS"
    else:
        outcome = "FALSIFIES"

    print(f"\n{'=' * 70}")
    print(f"OUTCOME: {outcome}")
    print(f"STATUS: {status}")
    print(f"{'=' * 70}")

    # ── Build results dictionary ──
    results = {
        "experiment_id": EXPERIMENT_ID,
        "primary_dataset": {
            "n_transitions": len(primary_transitions),
            "n_trajectories": 25,
            "trajectory_length": 20,
            "non_leakage_violations": n_leakage,
            "unique_urls": len(set(t["state_before"]["url"] for t in primary_transitions)),
            "unique_titles": len(set(t["state_before"]["title"] for t in primary_transitions)),
        },
        "positive_control_dataset": {
            "n_transitions": len(positive_transitions),
            "n_trajectories": 10,
            "trajectory_length": 20,
            "non_leakage_violations": n_leakage_pos,
        },
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
        "positive_control": {
            "pmi": pos_stats["mean_pmi"],
            "p_value": pos_perm["p_value"],
            "passes": pos_passes_threshold,
        },
        "null_control": {
            "null_mean_pmi": null_pmi,
            "p_value": null_p_value,
            "passes": null_passes,
        },
        "decision_checks": decision_checks,
        "survives": survives,
        "outcome": outcome,
        "status": status,
    }

    return results


if __name__ == "__main__":
    os.environ["PYTHONHASHSEED"] = "0"
    results = run_experiment()

    # Save raw results
    out_dir = "research/experiments/EXP-PHYSICS-34149195420"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "raw_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_path}")
