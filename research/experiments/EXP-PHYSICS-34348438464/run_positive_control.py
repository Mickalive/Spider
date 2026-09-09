#!/usr/bin/env python3
"""
Step 1: Run positive control (synthetic SPA) and save results.
"""

import json
import math
import random
import collections
import os
import numpy as np

EXPERIMENT_ID = "EXP-PHYSICS-34348438464"
SEED = 42
N_PERMUTATIONS = 100
ALPHA = 1.0

# Synthetic SPA model
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

SYNTHETIC_TRANSITIONS = {
    0: {"form_submit": 3, "button_click": 4, "link_nav": 6, "menu_select": 7},
    1: {"form_submit": 5, "button_click": 3, "link_nav": 4, "menu_select": 6},
    2: {"form_submit": 3, "button_click": 5, "link_nav": 7, "menu_select": 4},
    3: {"form_submit": 0, "button_click": 1, "link_nav": 2, "menu_select": 6},
    4: {"form_submit": 1, "button_click": 2, "link_nav": 0, "menu_select": 7},
    5: {"form_submit": 2, "button_click": 0, "link_nav": 1, "menu_select": 6},
    6: {"form_submit": 3, "button_click": 4, "link_nav": 5, "menu_select": 0},
    7: {"form_submit": 5, "button_click": 3, "link_nav": 6, "menu_select": 1},
}


def state_url_only(state):
    return state["url"]

def state_url_title(state):
    return (state["url"], state["title"])

def state_url_title_form(state):
    return (state["url"], state["title"], tuple(state["form_signals"]))


def extract_triples(transitions, state_fn):
    triples = []
    for t in transitions:
        s = state_fn(t["state_before"])
        a = t["action"]["action_type"]
        s_next = state_fn(t["state_after"])
        triples.append((s, a, s_next))
    return triples


def compute_pmi_stats(triples):
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "N": 0, "unique_states": 0, "unique_sa_pairs": 0}

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
        "N": N,
        "unique_states": len(state_counts),
        "unique_actions": len(set(a for _, a, _ in triples)),
        "unique_sa_pairs": len(state_action_counts),
    }


def generate_synthetic_trajectories(n_trajectories, trajectory_length, rng):
    state_ids = list(SYNTHETIC_STATES.keys())
    all_transitions = []
    for traj_id in range(n_trajectories):
        current_state = rng.choice(state_ids)
        for step in range(trajectory_length):
            action = rng.choice(SYNTHETIC_ACTIONS)
            next_state = SYNTHETIC_TRANSITIONS[current_state][action]
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


def cross_trajectory_shuffle(triple_groups, rng):
    trajectories = []
    for tid in sorted(triple_groups.keys()):
        triples = triple_groups[tid]
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
        trajectories.append((states, actions, nexts))
    action_sequences = [a for _, a, _ in trajectories]
    rng.shuffle(action_sequences)
    shuffled_groups = {}
    for i, (tid, (states, _, nexts)) in enumerate(zip(sorted(triple_groups.keys()), trajectories)):
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
        "p_value": p_value, "shuffled_means": shuffled_means,
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": null_mean, "null_std": null_std, "effect_size_d": effect_d,
    }


def extract_trajectory_groups(transitions, state_fn):
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(t)
    triple_groups = {}
    for tid, trans in groups.items():
        triple_groups[tid] = extract_triples(trans, state_fn)
    return triple_groups


def main():
    rng = random.Random(SEED)
    
    print("Running positive control (synthetic SPA)...")
    synthetic_transitions = generate_synthetic_trajectories(
        n_trajectories=25, trajectory_length=20, rng=rng)
    
    print(f"  Generated {len(synthetic_transitions)} synthetic transitions")
    
    # Compute PMI for all representations
    results = {}
    for rep_name, state_fn in [("url_only", state_url_only), ("url_title", state_url_title), ("url_title_form", state_url_title_form)]:
        triples = extract_triples(synthetic_transitions, state_fn)
        stats = compute_pmi_stats(triples)
        triple_groups = extract_trajectory_groups(synthetic_transitions, state_fn)
        perm = permutation_test(triple_groups, stats["mean_pmi"], N_PERMUTATIONS, SEED)
        results[rep_name] = {
            "mean_pmi": stats["mean_pmi"],
            "N": stats["N"],
            "unique_states": stats["unique_states"],
            "unique_sa_pairs": stats["unique_sa_pairs"],
            "permutation_p": perm["p_value"],
            "effect_size_d": perm["effect_size_d"],
        }
        print(f"  {rep_name}: PMI = {stats['mean_pmi']:.6f} bits, p = {perm['p_value']:.6f}")
    
    passes = results["url_only"]["mean_pmi"] >= 0.5
    print(f"\nPositive control passes (PMI >= 0.5): {passes}")
    
    # Save results
    out = {
        "positive_control": results,
        "passes": passes,
    }
    out_path = "research/experiments/EXP-PHYSICS-34348438464/positive_control_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Results saved to {out_path}")


if __name__ == "__main__":
    main()
