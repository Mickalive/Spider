#!/usr/bin/env python3
"""
EXP-PHYSICS-34038570933: PMI Analysis of Live Web Transitions

Computes pointwise mutual information (PMI) between actions and next-states,
conditioned on current state, for live Web transitions from parent experiment.

Usage: python3 pmi_analysis.py
"""

import json
import hashlib
import math
import os
import random
from collections import Counter, defaultdict
from pathlib import Path

# Deterministic random seed
RANDOM_SEED = 42
PYTHONHASHSEED = 0
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
BONFERRONI_COMPARISONS = 4  # 2 sites x 2 conditions

# Paths to parent experiment data
PARENT_DIR = Path("research/experiments/EXP-PHYSICS-33965269281")
EXPECTED_HASHES = {
    "raw_live_wikipedia.json": "87e6d8fcecb436ab9b1067a27c7f5708c393bace5efbb0225bfe1f57aa87bc5e",
    "raw_live_python_docs.json": "a7634ca3734360a4d6a2ffdb89d859ae9ff466df710be3323da8ac5c5d2fa648",
    "raw_positive.json": "3eef0bbc382fef44eb63d55481e3d417b2a98478d6f4fa4e1eb06331a99fc73f",
    "raw_null.json": "3ae136b4cc36b5f736252af8b819613d1864625fc9647cfbdd649b13c72c713e",
}


def sha256_file(path):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_url(url):
    """Normalize URL for comparison: strip trailing slash, lowercase scheme/host."""
    if not url:
        return url
    # Simple normalization: strip trailing slash, lowercase
    url = url.rstrip("/")
    # Split into scheme://host/path
    if "://" in url:
        scheme, rest = url.split("://", 1)
        host, *path_parts = rest.split("/", 1)
        path = "/" + path_parts[0] if path_parts else ""
        return f"{scheme}://{host.lower()}{path}"
    return url.lower()


def load_transitions(filepath):
    """Load transitions from JSON file, extract (state_url, action_href, next_url) triples."""
    with open(filepath) as f:
        data = json.load(f)
    
    transitions = []
    trajectories = defaultdict(list)
    
    for i, t in enumerate(data):
        state_url = normalize_url(t["state_before"]["url"])
        action_href = t["action"].get("target_href", "")
        next_url = normalize_url(t["state_after"]["url"])
        transitions.append((state_url, action_href, next_url))
    
    return transitions


def group_by_trajectory(transitions):
    """Group consecutive transitions into trajectory groups.
    
    The parent experiment collects transitions in trajectory order,
    so we group by consecutive states (each transition's state_after
    becomes the next transition's state_before).
    """
    # For PMI analysis, we treat each transition independently
    # but for shuffling, we shuffle action labels within trajectories
    # The parent data is collected in trajectory order
    # We'll use a simple approach: group consecutive transitions
    # where state_before matches the previous state_after
    trajectories = []
    current_traj = []
    
    for i, (s, a, s_next) in enumerate(transitions):
        if i == 0:
            current_traj = [(s, a, s_next)]
        else:
            prev_s_next = transitions[i-1][2]
            if s == prev_s_next:
                current_traj.append((s, a, s_next))
            else:
                if current_traj:
                    trajectories.append(current_traj)
                current_traj = [(s, a, s_next)]
    
    if current_traj:
        trajectories.append(current_traj)
    
    return trajectories


def compute_pmi(transitions, alpha=ALPHA):
    """Compute pointwise mutual information for transitions.
    
    PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
    
    With Laplace smoothing on marginal estimates.
    """
    # Count transitions from each state
    state_counts = Counter()
    state_action_counts = Counter()
    state_next_counts = Counter()
    state_action_next_counts = Counter()
    
    for s, a, s_next in transitions:
        state_counts[s] += 1
        state_action_counts[(s, a)] += 1
        state_next_counts[(s, s_next)] += 1
        state_action_next_counts[(s, a, s_next)] += 1
    
    pmi_values = []
    
    for s, a, s_next in transitions:
        count_s = state_counts[s]
        count_s_a = state_action_counts[(s, a)]
        count_s_s_next = state_next_counts[(s, s_next)]
        count_s_a_s_next = state_action_next_counts[(s, a, s_next)]
        
        # Number of distinct actions from state s
        n_actions_s = sum(1 for (s2, _) in state_action_counts if s2 == s)
        n_next_s = sum(1 for (s2, _) in state_next_counts if s2 == s)
        
        # Laplace-smoothed marginals
        p_a_given_s = (count_s_a + alpha) / (count_s + alpha * n_actions_s)
        p_s_next_given_s = (count_s_s_next + alpha) / (count_s + alpha * n_next_s)
        
        # Joint conditional (no smoothing for joint - use raw counts)
        p_a_s_next_given_s = count_s_a_s_next / count_s
        
        # PMI
        if p_a_s_next_given_s > 0 and p_a_given_s > 0 and p_s_next_given_s > 0:
            pmi = math.log2(p_a_s_next_given_s / (p_a_given_s * p_s_next_given_s))
            pmi_values.append(pmi)
        else:
            # If joint probability is 0, PMI is undefined (treat as very negative)
            pmi_values.append(-10.0)  # Floor value
    
    return pmi_values


def shuffle_actions_within_trajectories(transitions, trajectories, rng):
    """Shuffle action labels within trajectories."""
    shuffled = []
    traj_idx = 0
    trans_idx = 0
    
    for traj in trajectories:
        # Extract actions from this trajectory
        actions = [t[1] for t in traj]
        rng.shuffle(actions)
        
        # Reconstruct with shuffled actions
        for i, (s, a, s_next) in enumerate(traj):
            shuffled.append((s, actions[i], s_next))
    
    return shuffled


def permutation_test(transitions, trajectories, n_permutations=N_PERMUTATIONS, seed=RANDOM_SEED):
    """Permutation test for PMI > 0."""
    rng = random.Random(seed)
    
    # Observed PMI
    observed_pmi_values = compute_pmi(transitions)
    observed_mean_pmi = sum(observed_pmi_values) / len(observed_pmi_values) if observed_pmi_values else 0
    
    # Null distribution
    null_pmi_values = []
    for _ in range(n_permutations):
        shuffled = shuffle_actions_within_trajectories(transitions, trajectories, rng)
        pmi_vals = compute_pmi(shuffled)
        null_mean = sum(pmi_vals) / len(pmi_vals) if pmi_vals else 0
        null_pmi_values.append(null_mean)
    
    # One-sided p-value: P(null_pmi >= observed_pmi)
    count_ge = sum(1 for null in null_pmi_values if null >= observed_mean_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)
    
    return observed_mean_pmi, null_pmi_values, p_value


def compute_effect_size(observed_values, null_values):
    """Compute Cohen's d effect size."""
    import statistics
    if not observed_values or not null_values:
        return 0.0
    
    obs_mean = statistics.mean(observed_values)
    null_mean = statistics.mean(null_values)
    
    # Pooled standard deviation
    obs_var = statistics.variance(observed_values) if len(observed_values) > 1 else 0
    null_var = statistics.variance(null_values) if len(null_values) > 1 else 0
    n_obs = len(observed_values)
    n_null = len(null_values)
    
    pooled_var = ((n_obs - 1) * obs_var + (n_null - 1) * null_var) / (n_obs + n_null - 2)
    pooled_std = math.sqrt(pooled_var) if pooled_var > 0 else 1e-10
    
    return (obs_mean - null_mean) / pooled_std


def main():
    """Main analysis pipeline."""
    import statistics
    
    print("EXP-PHYSICS-34038570933: PMI Analysis")
    print("=" * 60)
    
    # Set environment for reproducibility
    os.environ["PYTHONHASHSEED"] = str(PYTHONHASHSEED)
    
    # Verify SHA-256 hashes
    print("\n1. Verifying SHA-256 hashes...")
    for filename, expected_hash in EXPECTED_HASHES.items():
        filepath = PARENT_DIR / filename
        actual_hash = sha256_file(filepath)
        status = "PASS" if actual_hash == expected_hash else "FAIL"
        print(f"  {filename}: {status} (expected: {expected_hash[:16]}..., got: {actual_hash[:16]}...)")
        if status == "FAIL":
            print(f"    ERROR: Hash mismatch for {filename}")
            return None
    
    # Load data
    print("\n2. Loading transition data...")
    datasets = {}
    for name in ["raw_live_wikipedia", "raw_live_python_docs", "raw_positive", "raw_null"]:
        filepath = PARENT_DIR / f"{name}.json"
        transitions = load_transitions(filepath)
        trajectories = group_by_trajectory(transitions)
        datasets[name] = {
            "transitions": transitions,
            "trajectories": trajectories,
            "n_transitions": len(transitions),
            "n_trajectories": len(trajectories),
        }
        print(f"  {name}: {len(transitions)} transitions, {len(trajectories)} trajectories")
    
    # Check minimum transition count
    for name in ["raw_live_wikipedia", "raw_live_python_docs"]:
        if datasets[name]["n_transitions"] < 100:
            print(f"  ERROR: Fewer than 100 transitions for {name}")
            return None
    
    # Analyze each dataset
    results = {}
    for name, data in datasets.items():
        print(f"\n3. Analyzing {name}...")
        transitions = data["transitions"]
        trajectories = data["trajectories"]
        
        # Self-loop analysis
        self_loops = sum(1 for s, a, s_next in transitions if s == s_next)
        self_loop_fraction = self_loops / len(transitions) if transitions else 0
        
        # Unique states and actions
        unique_states = len(set(s for s, a, s_next in transitions))
        unique_actions = len(set(a for s, a, s_next in transitions))
        unique_sa_pairs = len(set((s, a) for s, a, s_next in transitions))
        
        # PMI on all transitions
        pmi_all = compute_pmi(transitions)
        mean_pmi_all = statistics.mean(pmi_all) if pmi_all else 0
        std_pmi_all = statistics.stdev(pmi_all) if len(pmi_all) > 1 else 0
        
        # PMI on non-self-loop transitions
        non_self = [(s, a, s_next) for s, a, s_next in transitions if s != s_next]
        pmi_nonself = compute_pmi(non_self) if non_self else []
        mean_pmi_nonself = statistics.mean(pmi_nonself) if pmi_nonself else 0
        std_pmi_nonself = statistics.stdev(pmi_nonself) if len(pmi_nonself) > 1 else 0
        
        # PMI on self-loop transitions only
        self_only = [(s, a, s_next) for s, a, s_next in transitions if s == s_next]
        pmi_self = compute_pmi(self_only) if self_only else []
        mean_pmi_self = statistics.mean(pmi_self) if pmi_self else 0
        
        # Permutation tests
        print(f"  Running permutation tests ({N_PERMUTATIONS} permutations)...")
        mean_pmi_obs_all, null_dist_all, p_all = permutation_test(
            transitions, trajectories, N_PERMUTATIONS, RANDOM_SEED
        )
        
        mean_pmi_obs_nonself, null_dist_nonself, p_nonself = permutation_test(
            non_self, group_by_trajectory(non_self), N_PERMUTATIONS, RANDOM_SEED
        ) if non_self else (0, [], 1.0)
        
        # Effect sizes
        effect_all = compute_effect_size(pmi_all, null_dist_all) if null_dist_all else 0
        effect_nonself = compute_effect_size(pmi_nonself, null_dist_nonself) if null_dist_nonself else 0
        
        # Confidence intervals (95% CI using normal approximation)
        ci_all_low = mean_pmi_all - 1.96 * std_pmi_all / math.sqrt(len(pmi_all)) if pmi_all else 0
        ci_all_high = mean_pmi_all + 1.96 * std_pmi_all / math.sqrt(len(pmi_all)) if pmi_all else 0
        
        # Bonferroni-corrected p-values
        p_all_corrected = min(p_all * BONFERRONI_COMPARISONS, 1.0)
        p_nonself_corrected = min(p_nonself * BONFERRONI_COMPARISONS, 1.0)
        
        # Entropy calculations
        action_counts = Counter(a for s, a, s_next in transitions)
        total_actions = sum(action_counts.values())
        h_a = -sum((c/total_actions) * math.log2(c/total_actions) 
                   for c in action_counts.values() if c > 0)
        
        next_given_s_counts = defaultdict(Counter)
        for s, a, s_next in transitions:
            next_given_s_counts[s][s_next] += 1
        
        h_s_prime_given_s = 0
        for s, counts in next_given_s_counts.items():
            total = sum(counts.values())
            h_s_prime_given_s += (total / len(transitions)) * sum(
                -(c/total) * math.log2(c/total) for c in counts.values() if c > 0
            )
        
        results[name] = {
            "n_transitions": len(transitions),
            "n_trajectories": len(trajectories),
            "n_self_loops": self_loops,
            "self_loop_fraction": round(self_loop_fraction, 4),
            "unique_states": unique_states,
            "unique_actions": unique_actions,
            "unique_sa_pairs": unique_sa_pairs,
            "mean_pmi_all": round(mean_pmi_all, 6),
            "std_pmi_all": round(std_pmi_all, 6),
            "ci_95_all": [round(ci_all_low, 6), round(ci_all_high, 6)],
            "p_value_all": round(p_all, 6),
            "p_value_all_corrected": round(p_all_corrected, 6),
            "effect_size_all": round(effect_all, 4),
            "mean_pmi_nonself": round(mean_pmi_nonself, 6),
            "std_pmi_nonself": round(std_pmi_nonself, 6),
            "n_nonself": len(non_self),
            "p_value_nonself": round(p_nonself, 6),
            "p_value_nonself_corrected": round(p_nonself_corrected, 6),
            "effect_size_nonself": round(effect_nonself, 4),
            "mean_pmi_self": round(mean_pmi_self, 6),
            "entropy_h_a": round(h_a, 6),
            "entropy_h_s_prime_given_s": round(h_s_prime_given_s, 6),
            "pmi_values_all": [round(v, 6) for v in pmi_all],
            "null_distribution_all": [round(v, 6) for v in null_dist_all],
            "null_distribution_nonself": [round(v, 6) for v in null_dist_nonself],
        }
        
        print(f"  Mean PMI (all): {mean_pmi_all:.6f} +/- {std_pmi_all:.6f}")
        print(f"  Mean PMI (non-self): {mean_pmi_nonself:.6f}")
        print(f"  P-value (all, corrected): {p_all_corrected:.6f}")
        print(f"  P-value (non-self, corrected): {p_nonself_corrected:.6f}")
        print(f"  Self-loop fraction: {self_loop_fraction:.4f}")
    
    # Positive control analysis
    print("\n4. Positive control (synthetic lambda=1.0)...")
    pos_data = datasets["raw_positive"]
    pos_pmi = compute_pmi(pos_data["transitions"])
    mean_pmi_pos = statistics.mean(pos_pmi) if pos_pmi else 0
    print(f"  Mean PMI (positive control): {mean_pmi_pos:.6f}")
    print(f"  Expected: >= 1.0 bit")
    print(f"  PASS: {mean_pmi_pos >= 1.0}")
    
    # Null control analysis
    print("\n5. Null control (shuffled actions)...")
    null_data = datasets["raw_null"]
    null_pmi = compute_pmi(null_data["transitions"])
    mean_pmi_null = statistics.mean(null_pmi) if null_pmi else 0
    print(f"  Mean PMI (null control): {mean_pmi_null:.6f}")
    
    # Permutation test on null control
    mean_pmi_obs_null, null_dist_null, p_null = permutation_test(
        null_data["transitions"], null_data["trajectories"], N_PERMUTATIONS, RANDOM_SEED
    )
    print(f"  P-value (null control): {p_null:.6f}")
    print(f"  Expected: > 0.05 (not significant)")
    print(f"  PASS: {p_null > 0.05}")
    
    # Decision evaluation
    print("\n6. Decision evaluation...")
    wiki = results.get("raw_live_wikipedia", {})
    python = results.get("raw_live_python_docs", {})
    
    decision_criteria = {
        "wiki_all_pmi_gt_0": wiki.get("mean_pmi_all", 0) > 0,
        "wiki_all_p_corrected": wiki.get("p_value_all_corrected", 1) < 0.05,
        "python_all_pmi_gt_0": python.get("mean_pmi_all", 0) > 0,
        "python_all_p_corrected": python.get("p_value_all_corrected", 1) < 0.05,
        "wiki_nonself_pmi_gt_0": wiki.get("mean_pmi_nonself", 0) > 0,
        "wiki_nonself_p_corrected": wiki.get("p_value_nonself_corrected", 1) < 0.05,
        "python_nonself_pmi_gt_0": python.get("mean_pmi_nonself", 0) > 0,
        "python_nonself_p_corrected": python.get("p_value_nonself_corrected", 1) < 0.05,
        "positive_control_pass": mean_pmi_pos >= 1.0,
        "null_control_pass": p_null > 0.05,
    }
    
    all_pass = all(decision_criteria.values())
    any_fail = not all_pass
    
    print("  Decision criteria:")
    for criterion, passed in decision_criteria.items():
        status = "PASS" if passed else "FAIL"
        print(f"    {criterion}: {status}")
    
    print(f"\n  Overall: {'SURVIVES_CURRENT_TEST' if all_pass else 'FALSIFIED-IN-SETTING'}")
    
    # Save results
    output = {
        "experiment_id": "EXP-PHYSICS-34038570933",
        "datasets": results,
        "positive_control": {
            "mean_pmi": round(mean_pmi_pos, 6),
            "pass": mean_pmi_pos >= 1.0,
        },
        "null_control": {
            "mean_pmi": round(mean_pmi_null, 6),
            "p_value": round(p_null, 6),
            "pass": p_null > 0.05,
        },
        "decision_criteria": decision_criteria,
        "outcome": "SURVIVES_CURRENT_TEST" if all_pass else "FALSIFIED-IN-SETTING",
    }
    
    output_path = Path("research/physics/information_theoretic/pmi_results.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {output_path}")
    return output


if __name__ == "__main__":
    main()
