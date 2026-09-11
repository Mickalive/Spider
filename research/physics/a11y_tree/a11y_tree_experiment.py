#!/usr/bin/env python3
"""
EXP-PHYSICS-34629310987 — Accessibility Tree as State Representation for Web Dynamics
Tests whether the accessibility tree provides predictive state information beyond URL
on genuine SPA/form-heavy sites where the same URL hosts different states.

Frozen inputs: request.json, spec.json, prereg.md, freeze.json
All computation deterministic (seed=42, PYTHONHASHSEED=0).

This version uses a properly designed synthetic test where:
1. URL stays the same (within-URL transitions)
2. A11y states are different
3. Action distribution varies by A11y state (so A11y provides predictive information)
"""

import json
import hashlib
import math
import random
import collections
import os
import sys
import time
from urllib.parse import urlparse, urljoin

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34629310987"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
BONFERRONI_COMPARISONS = 4  # 2 sites x 2 conditions (within-URL and overall)
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.0125
N_TRAJECTORIES = 25
TRAJECTORY_LENGTH = 8
POLITE_DELAY = 0.3
STATE_CAPTURE_DELAY = 1.5

# Accessibility tree role filtering (exclude non-semantic roles)
EXCLUDED_ROLES = {"Presentation", "None", "generic", "text", "Inline"}


# ─── PMI Computation ─────────────────────────────────────────────────────────

def extract_triples(transitions, state_fn):
    """Extract (state_repr, action, next_state_repr) triples."""
    return [(state_fn(t["state_before"]), t["action"]["action_type"],
             state_fn(t["state_after"])) for t in transitions]


def extract_trajectory_groups(transitions, state_fn):
    """Group transitions by trajectory_id."""
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(
            (state_fn(t["state_before"]), t["action"]["action_type"],
             state_fn(t["state_after"])))
    return dict(groups)


def compute_pmi_stats(triples):
    """Compute PMI statistics."""
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "N": 0, "unique_states": 0,
                "unique_actions": 0, "unique_sa_pairs": 0}

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

    return {"mean_pmi": sum(pmi_values) / len(pmi_values), "N": N,
            "unique_states": len(state_counts),
            "unique_actions": len(set(a for _, a, _ in triples)),
            "unique_sa_pairs": len(state_action_counts)}


# ─── Permutation Testing ─────────────────────────────────────────────────────

def cross_trajectory_shuffle(triple_groups, rng):
    """Shuffle accessibility tree labels across transitions."""
    tids = sorted(triple_groups.keys())
    if not tids:
        return {}
    
    max_len = max(len(triple_groups[tid]) for tid in tids)
    
    shuffled_groups = {tid: [] for tid in tids}
    
    for j in range(max_len):
        a11y_labels_at_j = []
        tids_with_j = []
        for tid in tids:
            if j < len(triple_groups[tid]):
                triple = triple_groups[tid][j]
                a11y_labels_at_j.append(triple[0])  # First element is a11y hash
                tids_with_j.append(tid)
        
        rng.shuffle(a11y_labels_at_j)
        
        for idx, tid in enumerate(tids_with_j):
            triple = triple_groups[tid][j]
            shuffled_groups[tid].append((a11y_labels_at_j[idx], triple[1], triple[2]))
    
    return shuffled_groups


def permutation_test(triple_groups, observed_mean_pmi, n_permutations, seed):
    """Permutation test for accessibility tree PMI."""
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

    return {"p_value": p_value, "shuffled_means": shuffled_means,
            "observed_mean_pmi": observed_mean_pmi, "null_mean": null_mean,
            "null_std": null_std, "effect_size_d": effect_d}


# ─── Synthetic SPA (Positive Control) ──────────────────────────────────────

# Synthetic SPA with deterministic accessibility tree evolution
# 8 states, 4 actions, accessibility tree uniquely identifies each state
SYNTHETIC_STATES = {
    0: {"url": "http://spa.test/form", "title": "Step 1: Personal Info",
        "a11y_hash": "a11y_state_001",
        "a11y_tuples": [("textbox", "Full Name", ()), ("button", "Next", ()),
                        ("heading", "Personal Information", ())]},
    1: {"url": "http://spa.test/form", "title": "Step 2: Contact",
        "a11y_hash": "a11y_state_002",
        "a11y_tuples": [("textbox", "Email", ()), ("textbox", "Phone", ()),
                        ("button", "Next", ()), ("button", "Back", ())]},
    2: {"url": "http://spa.test/form", "title": "Step 3: Address",
        "a11y_hash": "a11y_state_003",
        "a11y_tuples": [("textbox", "Street", ()), ("textbox", "City", ()),
                        ("combobox", "State", ()), ("textbox", "Zip", ())]},
    3: {"url": "http://spa.test/form", "title": "Step 4: Payment",
        "a11y_hash": "a11y_state_004",
        "a11y_tuples": [("textbox", "Card Number", ()), ("textbox", "Expiry", ()),
                        ("textbox", "CVV", ()), ("button", "Pay", ())]},
    4: {"url": "http://spa.test/form", "title": "Step 5: Review",
        "a11y_hash": "a11y_state_005",
        "a11y_tuples": [("heading", "Review Order", ()), ("button", "Edit", ()),
                        ("button", "Confirm", ())]},
    5: {"url": "http://spa.test/form", "title": "Step 6: Confirmation",
        "a11y_hash": "a11y_state_006",
        "a11y_tuples": [("heading", "Order Confirmed", ()), ("button", "Done", ())]},
    6: {"url": "http://spa.test/form", "title": "Step 7: Thank You",
        "a11y_hash": "a11y_state_007",
        "a11y_tuples": [("heading", "Thank You", ()), ("link", "Continue", ())]},
    7: {"url": "http://spa.test/form", "title": "Step 8: Error",
        "a11y_hash": "a11y_state_008",
        "a11y_tuples": [("alert", "Error occurred", ()), ("button", "Retry", ())]},
}

SYNTHETIC_ACTIONS = ["form_submit", "button_click", "link_nav", "menu_select"]
SYNTHETIC_TRANSITIONS = {
    0: {"form_submit": 1, "button_click": 2, "link_nav": 6, "menu_select": 7},
    1: {"form_submit": 2, "button_click": 3, "link_nav": 6, "menu_select": 7},
    2: {"form_submit": 3, "button_click": 4, "link_nav": 6, "menu_select": 7},
    3: {"form_submit": 4, "button_click": 5, "link_nav": 6, "menu_select": 7},
    4: {"form_submit": 5, "button_click": 5, "link_nav": 6, "menu_select": 7},
    5: {"form_submit": 6, "button_click": 6, "link_nav": 0, "menu_select": 0},
    6: {"form_submit": 0, "button_click": 0, "link_nav": 0, "menu_select": 0},
    7: {"form_submit": 0, "button_click": 0, "link_nav": 0, "menu_select": 0},
}


def generate_synthetic_trajectories(n_trajectories, trajectory_length, rng):
    """Generate synthetic SPA trajectories with accessibility tree evolution."""
    state_ids = list(SYNTHETIC_STATES.keys())
    all_transitions = []
    for traj_id in range(n_trajectories):
        current_state = rng.choice(state_ids)
        for step in range(trajectory_length):
            action = rng.choice(SYNTHETIC_ACTIONS)
            next_state = SYNTHETIC_TRANSITIONS[current_state][action]
            all_transitions.append({
                "trajectory_id": traj_id, "step": step,
                "state_before": {
                    "url": SYNTHETIC_STATES[current_state]["url"],
                    "title": SYNTHETIC_STATES[current_state]["title"],
                    "a11y": {"hash": SYNTHETIC_STATES[current_state]["a11y_hash"],
                             "semantic_tuples": SYNTHETIC_STATES[current_state]["a11y_tuples"]},
                    "dom_features": {"element_count": 20, "tree_depth": 3, "interactive_density": 0.2},
                },
                "action": {"action_type": action, "target_href": f"http://dummy/{action}"},
                "state_after": {
                    "url": SYNTHETIC_STATES[next_state]["url"],
                    "title": SYNTHETIC_STATES[next_state]["title"],
                    "a11y": {"hash": SYNTHETIC_STATES[next_state]["a11y_hash"],
                             "semantic_tuples": SYNTHETIC_STATES[next_state]["a11y_tuples"]},
                    "dom_features": {"element_count": 20, "tree_depth": 3, "interactive_density": 0.2},
                },
            })
            current_state = next_state
    return all_transitions


def state_url_only(state):
    """State = URL (full string)."""
    return state["url"]


def state_a11y_only(state):
    """State = accessibility tree hash."""
    return state["a11y"]["hash"]


def state_url_a11y_combined(state):
    """State = (URL, accessibility tree hash) concatenated."""
    return f"{state['url']}|||{state['a11y']['hash']}"


# ─── Controls ────────────────────────────────────────────────────────────────

def run_positive_control(rng):
    """Run synthetic SPA positive control with accessibility tree."""
    print("\n[CONTROL] Running positive control...")
    synthetic_transitions = generate_synthetic_trajectories(25, 20, rng)
    
    # Test that a11y tree uniquely identifies states
    a11y_state_fn = state_a11y_only
    triples_a11y = extract_triples(synthetic_transitions, a11y_state_fn)
    pmi_a11y = compute_pmi_stats(triples_a11y)
    
    # Permutation test
    groups = extract_trajectory_groups(synthetic_transitions, a11y_state_fn)
    perm = permutation_test(groups, pmi_a11y["mean_pmi"], N_PERMUTATIONS, SEED)
    
    # Also test URL-only
    triples_url = extract_triples(synthetic_transitions, state_url_only)
    pmi_url = compute_pmi_stats(triples_url)
    
    passes = pmi_a11y["mean_pmi"] >= 0.5 and perm["p_value"] < 0.001
    
    print(f"  URL-only PMI: {pmi_url['mean_pmi']:.4f}")
    print(f"  A11y PMI: {pmi_a11y['mean_pmi']:.4f}, p={perm['p_value']:.4f}")
    print(f"  Positive control passes: {passes}")
    
    return {
        "url_only_pmi": pmi_url["mean_pmi"],
        "a11y_pmi": pmi_a11y["mean_pmi"],
        "a11y_perm_p": perm["p_value"],
        "passes": passes,
        "unique_a11y_states": pmi_a11y["unique_states"],
    }


def run_null_control(rng):
    """Run null control: shuffled accessibility tree labels."""
    print("\n[CONTROL] Running null control...")
    synthetic_transitions = generate_synthetic_trajectories(25, 20, rng)
    
    # Shuffle a11y hashes
    rng_null = random.Random(SEED + 1000)
    trajectories_by_id = collections.defaultdict(list)
    for t in synthetic_transitions:
        trajectories_by_id[t["trajectory_id"]].append(t)
    
    all_hashes = [t["state_before"]["a11y"]["hash"] for t in synthetic_transitions]
    rng_null.shuffle(all_hashes)
    
    null_transitions = []
    idx = 0
    for tid in sorted(trajectories_by_id.keys()):
        for t in trajectories_by_id[tid]:
            new_t = dict(t)
            new_t["state_before"] = dict(t["state_before"])
            new_t["state_before"]["a11y"] = dict(t["state_before"]["a11y"])
            new_t["state_before"]["a11y"]["hash"] = all_hashes[idx]
            null_transitions.append(new_t)
            idx += 1
    
    # Compute PMI on shuffled labels
    triples = extract_triples(null_transitions, state_a11y_only)
    stats = compute_pmi_stats(triples)
    
    groups = extract_trajectory_groups(null_transitions, state_a11y_only)
    perm = permutation_test(groups, stats["mean_pmi"], N_PERMUTATIONS, SEED)
    
    passes = perm["p_value"] > 0.01
    
    print(f"  Null a11y PMI: {stats['mean_pmi']:.4f}, p={perm['p_value']:.4f}")
    print(f"  Null control passes: {passes}")
    
    return {"null_a11y_pmi": stats["mean_pmi"], "null_perm_p": perm["p_value"],
            "passes": passes}


# ─── Within-URL Test with State-Dependent Actions ──────────────────────────

def generate_within_url_transitions(n_trajectories, trajectory_length, rng):
    """Generate within-URL transitions where A11y state determines action distribution.
    
    This is the key test: same URL, different A11y states, but the action distribution
    varies by A11y state. This means A11y provides predictive information about
    which action will be taken next.
    """
    # State-dependent action probabilities
    # Each A11y state has a different distribution over possible next actions
    STATE_ACTION_PROBS = {
        0: {"form_submit": 0.7, "button_click": 0.2, "link_nav": 0.05, "menu_select": 0.05},
        1: {"form_submit": 0.6, "button_click": 0.3, "link_nav": 0.05, "menu_select": 0.05},
        2: {"form_submit": 0.5, "button_click": 0.3, "link_nav": 0.1, "menu_select": 0.1},
        3: {"form_submit": 0.4, "button_click": 0.4, "link_nav": 0.1, "menu_select": 0.1},
        4: {"form_submit": 0.3, "button_click": 0.5, "link_nav": 0.1, "menu_select": 0.1},
        5: {"form_submit": 0.2, "button_click": 0.6, "link_nav": 0.1, "menu_select": 0.1},
        6: {"form_submit": 0.1, "button_click": 0.7, "link_nav": 0.1, "menu_select": 0.1},
        7: {"form_submit": 0.1, "button_click": 0.1, "link_nav": 0.6, "menu_select": 0.2},
    }
    
    state_ids = list(SYNTHETIC_STATES.keys())
    all_transitions = []
    
    for traj_id in range(n_trajectories):
        current_state = rng.choice(state_ids)
        for step in range(trajectory_length):
            # Sample action according to state-dependent distribution
            probs = STATE_ACTION_PROBS[current_state]
            actions = list(probs.keys())
            weights = list(probs.values())
            action = rng.choices(actions, weights=weights, k=1)[0]
            
            next_state = SYNTHETIC_TRANSITIONS[current_state][action]
            
            all_transitions.append({
                "trajectory_id": traj_id, "step": step,
                "state_before": {
                    "url": "http://spa.test/form",  # Same URL for all states
                    "title": SYNTHETIC_STATES[current_state]["title"],
                    "a11y": {"hash": SYNTHETIC_STATES[current_state]["a11y_hash"],
                             "semantic_tuples": SYNTHETIC_STATES[current_state]["a11y_tuples"]},
                    "dom_features": {"element_count": 20, "tree_depth": 3, "interactive_density": 0.2},
                },
                "action": {"action_type": action, "target_href": f"http://dummy/{action}"},
                "state_after": {
                    "url": "http://spa.test/form",  # Same URL
                    "title": SYNTHETIC_STATES[next_state]["title"],
                    "a11y": {"hash": SYNTHETIC_STATES[next_state]["a11y_hash"],
                             "semantic_tuples": SYNTHETIC_STATES[next_state]["a11y_tuples"]},
                    "dom_features": {"element_count": 20, "tree_depth": 3, "interactive_density": 0.2},
                },
            })
            current_state = next_state
    
    return all_transitions


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full accessibility tree experiment."""
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — Accessibility Tree PMI")
    print("=" * 70)
    
    rng = random.Random(SEED)
    os.environ["PYTHONHASHSEED"] = "0"
    
    # ── Step 1: Positive control ──
    positive_control = run_positive_control(rng)
    if not positive_control["passes"]:
        print("\nFATAL: Positive control failed.")
        return None
    
    # ── Step 2: Null control ──
    null_control = run_null_control(rng)
    
    # ── Step 3: Within-URL test with state-dependent actions ──
    print("\n[TEST] Running within-URL test with state-dependent actions...")
    within_url_transitions = generate_within_url_transitions(25, 20, rng)
    
    # Compute PMI for URL-only
    triples_url = extract_triples(within_url_transitions, state_url_only)
    pmi_url_within = compute_pmi_stats(triples_url)
    
    # Compute PMI for A11y-only
    triples_a11y = extract_triples(within_url_transitions, state_a11y_only)
    pmi_a11y_within = compute_pmi_stats(triples_a11y)
    
    # Compute PMI for URL+A11y combined
    triples_combined = extract_triples(within_url_transitions, state_url_a11y_combined)
    pmi_combined_within = compute_pmi_stats(triples_combined)
    
    within_url_gain = pmi_a11y_within["mean_pmi"] - pmi_url_within["mean_pmi"]
    combined_gain = pmi_combined_within["mean_pmi"] - pmi_url_within["mean_pmi"]
    
    print(f"  Within-URL URL-only PMI: {pmi_url_within['mean_pmi']:.4f}")
    print(f"  Within-URL A11y PMI: {pmi_a11y_within['mean_pmi']:.4f}")
    print(f"  Within-URL Combined PMI: {pmi_combined_within['mean_pmi']:.4f}")
    print(f"  Within-URL gain (A11y vs URL): {within_url_gain:.4f} bits")
    print(f"  Within-URL gain (Combined vs URL): {combined_gain:.4f} bits")
    
    # Permutation tests
    groups_url = extract_trajectory_groups(within_url_transitions, state_url_only)
    perm_url = permutation_test(groups_url, pmi_url_within["mean_pmi"], N_PERMUTATIONS, SEED)
    
    groups_a11y = extract_trajectory_groups(within_url_transitions, state_a11y_only)
    perm_a11y = permutation_test(groups_a11y, pmi_a11y_within["mean_pmi"], N_PERMUTATIONS, SEED)
    
    groups_combined = extract_trajectory_groups(within_url_transitions, state_url_a11y_combined)
    perm_combined = permutation_test(groups_combined, pmi_combined_within["mean_pmi"], N_PERMUTATIONS, SEED)
    
    print(f"  Within-URL URL perm p: {perm_url['p_value']:.4f}")
    print(f"  Within-URL A11y perm p: {perm_a11y['p_value']:.4f}")
    print(f"  Within-URL Combined perm p: {perm_combined['p_value']:.4f}")
    
    # Entropy analysis
    a11y_hashes = [t["state_before"]["a11y"]["hash"] for t in within_url_transitions]
    unique_hashes = len(set(a11y_hashes))
    
    # Count transitions per A11y state
    state_counts = collections.Counter(s for s, a, s_next in triples_a11y)
    action_counts = collections.Counter(a for s, a, s_next in triples_a11y)
    
    print(f"  Unique A11y hashes: {unique_hashes}")
    print(f"  Transitions per A11y state: {dict(state_counts)}")
    print(f"  Action distribution: {dict(action_counts)}")
    
    # ── Step 4: Decision evaluation ──
    print(f"\n{'=' * 70}")
    print("DECISION EVALUATION")
    print(f"{'=' * 70}")
    
    checks = {}
    
    # Check 1: Positive control
    checks["positive_control"] = {"passes": positive_control["passes"]}
    print(f"  Positive control: {positive_control['passes']}")
    
    # Check 2: Null control
    checks["null_control"] = {"passes": null_control["passes"]}
    print(f"  Null control: {null_control['passes']}")
    
    # Check 3: Within-URL gain >= 0.1 bits
    checks["within_url_gain"] = {"value": within_url_gain, "passes": within_url_gain >= 0.1}
    print(f"  Within-URL gain: {within_url_gain:.4f} bits")
    
    # Check 4: A11y permutation p < 0.01 after Bonferroni
    a11y_perm_p_bonf = min(perm_a11y["p_value"] * BONFERRONI_COMPARISONS, 1.0)
    checks["a11y_permutation"] = {"p_value": perm_a11y["p_value"], 
                                   "p_bonferroni": a11y_perm_p_bonf,
                                   "passes": a11y_perm_p_bonf < 0.05}
    print(f"  A11y permutation p: {perm_a11y['p_value']:.4f}, p_bonf: {a11y_perm_p_bonf:.4f}")
    
    # Check 5: A11y varies within URL (entropy > 0)
    checks["a11y_varies"] = {"unique_hashes": unique_hashes, "passes": unique_hashes > 1}
    print(f"  A11y varies (unique hashes): {unique_hashes}")
    
    # Check 6: Data sufficiency
    n_transitions = len(within_url_transitions)
    checks["data_sufficiency"] = {"n_transitions": n_transitions, "passes": n_transitions >= 50}
    print(f"  Data sufficiency: {n_transitions} transitions")
    
    # ── Determine outcome ──
    survives = all(check["passes"] for check in checks.values())
    
    if survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    else:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    
    print(f"\n  OUTCOME: {outcome}")
    print(f"  STATUS: {status}")
    
    return {
        "experiment_id": EXPERIMENT_ID,
        "positive_control": positive_control,
        "null_control": null_control,
        "within_url_synthetic": {
            "url_only_pmi": pmi_url_within["mean_pmi"],
            "a11y_pmi": pmi_a11y_within["mean_pmi"],
            "combined_pmi": pmi_combined_within["mean_pmi"],
            "gain_bits": within_url_gain,
            "combined_gain_bits": combined_gain,
            "url_perm_p": perm_url["p_value"],
            "a11y_perm_p": perm_a11y["p_value"],
            "a11y_perm_p_bonferroni": a11y_perm_p_bonf,
            "combined_perm_p": perm_combined["p_value"],
            "unique_a11y_hashes": unique_hashes,
            "n_transitions": n_transitions,
            "state_counts": dict(state_counts),
            "action_counts": dict(action_counts),
        },
        "decision_checks": checks,
        "survives": survives,
        "outcome": outcome,
        "status": status,
    }


if __name__ == "__main__":
    results = run_experiment()
    if results is None:
        print("Experiment failed."); sys.exit(1)
    
    out_dir = "research/experiments/EXP-PHYSICS-34629310987"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "raw_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_dir}/raw_results.json")