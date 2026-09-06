#!/usr/bin/env python3
"""
EXP-PHYSICS-34038570933 — PMI Analysis of Web Transitions
Pointwise mutual information between actions and next-states, conditioned on current state.
Re-uses parent experiment raw data. All computation is deterministic (seed=42, PYTHONHASHSEED=0).
"""

import json
import hashlib
import math
import random
import collections
import os
import sys
from typing import Any

import numpy as np

# ─── Configuration ───────────────────────────────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34038570933"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing for marginal probability estimates
BONFERRONI_COMPARISONS = 4
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.0125

PARENT_DIR = "research/experiments/EXP-PHYSICS-33965269281"
DATA_FILES = {
    "live_wikipedia": ("raw_live_wikipedia.json", "87e6d8fcecb436ab9b1067a27c7f5708c393bace5efbb0225bfe1f57aa87bc5e"),
    "live_python_docs": ("raw_live_python_docs.json", "a7634ca3734360a4d6a2ffdb89d859ae9ff466df710be3323da8ac5c5d2fa648"),
    "positive_control": ("raw_positive.json", "3eef0bbc382fef44eb63d55481e3d417b2a98478d6f4fa4e1eb06331a99fc73f"),
    "null_control": ("raw_null.json", "3ae136b4cc36b5f736252af8b819613d1864625fc9647cfbdd649b13c72c713e"),
}

# ─── Data Loading ────────────────────────────────────────────────────────────

def normalize_url(url: str) -> str:
    """Normalize URL for state identity: strip trailing slash, lowercase scheme/host."""
    if not url:
        return url
    # Simple normalization: strip trailing slash
    if url.endswith("/") and url.count("/") > 3:
        url = url[:-1]
    return url


def load_and_verify(filename: str, expected_sha256: str, parent_dir: str) -> list:
    """Load JSON file and verify SHA-256 hash."""
    filepath = os.path.join(parent_dir, filename)
    with open(filepath, "rb") as f:
        raw = f.read()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != expected_sha256:
        raise ValueError(f"SHA-256 mismatch for {filename}: expected {expected_sha256}, got {actual_sha}")
    data = json.loads(raw)
    print(f"  Loaded {filename}: {len(data)} transitions, SHA-256 verified")
    return data


def extract_triples(transitions: list) -> list:
    """Extract (state_url, action_href, next_url) triples."""
    triples = []
    for t in transitions:
        s_url = normalize_url(t["state_before"]["url"])
        a_href = t["action"].get("target_href", "")
        s_next = normalize_url(t["state_after"]["url"])
        triples.append((s_url, a_href, s_next))
    return triples


def extract_trajectory_groups(transitions: list) -> dict:
    """Group transitions by trajectory_id."""
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(t)
    return groups


def extract_triple_groups(trajectory_groups: dict) -> dict:
    """Extract trajectory-grouped triples."""
    triple_groups = {}
    for tid, trans in trajectory_groups.items():
        triple_groups[tid] = extract_triples(trans)
    return triple_groups

# ─── PMI Computation ─────────────────────────────────────────────────────────

def compute_pmi_stats(triples: list) -> dict:
    """Compute PMI statistics for a set of triples.

    PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]

    Using Laplace smoothing for marginal estimates.
    """
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "pmi_values": [], "N": 0}

    # Count transitions per state
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

        # Number of distinct actions from state s
        distinct_actions_s = sum(1 for (si, ai) in state_action_counts if si == s)
        # Number of distinct next-states from state s
        distinct_next_s = sum(1 for (si, sni) in state_next_counts if si == s)

        # P(a | s) with Laplace smoothing
        p_a_given_s = (count_sa + ALPHA) / (count_s + ALPHA * distinct_actions_s)
        # P(s' | s) with Laplace smoothing
        p_s_next_given_s = (count_ss_next + ALPHA) / (count_s + ALPHA * distinct_next_s)
        # P(a, s' | s) = count(s, a, s') / count(s)
        p_joint_given_s = count_sas_next / count_s

        # PMI = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
        denom = p_a_given_s * p_s_next_given_s
        if denom > 0 and p_joint_given_s > 0:
            pmi = math.log2(p_joint_given_s / denom)
        else:
            pmi = 0.0  # Should not happen with Laplace smoothing, but defensive

        pmi_values.append(pmi)

    mean_pmi = sum(pmi_values) / len(pmi_values)

    return {
        "mean_pmi": mean_pmi,
        "pmi_values": pmi_values,
        "N": N,
        "state_counts": dict(state_counts),
        "unique_states": len(state_counts),
        "unique_state_action_pairs": len(state_action_counts),
    }


def compute_trajectory_mean_pmi(triple_groups: dict) -> list:
    """Compute per-trajectory mean PMI."""
    per_traj_pmi = []
    for tid, triples in triple_groups.items():
        stats = compute_pmi_stats(triples)
        per_traj_pmi.append(stats["mean_pmi"])
    return per_traj_pmi


def shuffle_actions_within_trajectories(triple_groups: dict, rng: random.Random) -> dict:
    """Shuffle action labels within trajectories."""
    shuffled_groups = {}
    for tid, triples in triple_groups.items():
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
        # Shuffle actions only
        shuffled_actions = actions[:]
        rng.shuffle(shuffled_actions)
        shuffled_groups[tid] = [(states[i], shuffled_actions[i], nexts[i]) for i in range(len(triples))]
    return shuffled_groups


def permutation_test(triple_groups: dict, observed_mean_pmi: float, n_permutations: int, seed: int) -> dict:
    """Permutation test: shuffle actions within trajectories, recompute mean PMI."""
    rng = random.Random(seed)
    all_triples = []
    for triples in triple_groups.values():
        all_triples.extend(triples)

    shuffled_means = []
    for _ in range(n_permutations):
        shuffled_groups = shuffle_actions_within_trajectories(triple_groups, rng)
        all_shuffled = []
        for triples in shuffled_groups.values():
            all_shuffled.extend(triples)
        stats = compute_pmi_stats(all_shuffled)
        shuffled_means.append(stats["mean_pmi"])

    # One-sided p-value: fraction of shuffled >= observed
    count_ge = sum(1 for m in shuffled_means if m >= observed_mean_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)

    return {
        "p_value": p_value,
        "shuffled_means": shuffled_means,
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": np.mean(shuffled_means),
        "null_std": np.std(shuffled_means),
        "effect_size_d": (observed_mean_pmi - np.mean(shuffled_means)) / np.std(shuffled_means) if np.std(shuffled_means) > 0 else 0.0,
    }


def compute_self_loop_stats(transitions: list) -> dict:
    """Compute self-loop statistics."""
    total = len(transitions)
    self_loops = 0
    for t in transitions:
        s_url = normalize_url(t["state_before"]["url"])
        s_next = normalize_url(t["state_after"]["url"])
        if s_url == s_next:
            self_loops += 1
    return {
        "total": total,
        "self_loops": self_loops,
        "self_loop_fraction": self_loops / total if total > 0 else 0.0,
    }

# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full PMI experiment."""
    import os
    parent_dir = os.path.join(os.path.dirname(__file__), "..", "..", "experiments", "EXP-PHYSICS-33965269281")
    parent_dir = os.path.normpath(parent_dir)

    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — PMI Analysis")
    print("=" * 70)

    # ── Step 1: Load and verify data ──
    print("\n[1/8] Loading and verifying parent data files...")
    datasets = {}
    for key, (filename, expected_sha) in DATA_FILES.items():
        try:
            data = load_and_verify(filename, expected_sha, parent_dir)
            datasets[key] = data
        except Exception as e:
            print(f"  FATAL: {e}")
            sys.exit(1)

    # ── Step 2: Extract triples ──
    print("\n[2/8] Extracting (state, action, next) triples...")
    all_data = {}
    for key, data in datasets.items():
        triples = extract_triples(data)
        traj_groups = extract_trajectory_groups(data)
        triple_groups = extract_trajectory_groups(data)
        all_data[key] = {
            "triples": triples,
            "traj_groups": traj_groups,
            "triple_groups": {tid: extract_triples(trans) for tid, trans in traj_groups.items()},
        }
        print(f"  {key}: {len(triples)} triples, {len(traj_groups)} trajectories")

    # ── Step 3: Self-loop statistics ──
    print("\n[3/8] Computing self-loop statistics...")
    self_loop_stats = {}
    for key in ["live_wikipedia", "live_python_docs"]:
        stats = compute_self_loop_stats(datasets[key])
        self_loop_stats[key] = stats
        print(f"  {key}: {stats['self_loops']}/{stats['total']} self-loops ({stats['self_loop_fraction']:.3f})")

    # ── Step 4: Compute PMI for all datasets ──
    print("\n[4/8] Computing PMI on all transitions...")
    pmi_results = {}
    for key in ["live_wikipedia", "live_python_docs", "positive_control", "null_control"]:
        stats = compute_pmi_stats(all_data[key]["triples"])
        pmi_results[key] = stats
        print(f"  {key}: mean_PMI = {stats['mean_pmi']:.6f} bits, N = {stats['N']}, "
              f"unique_states = {stats['unique_states']}, unique_SA_pairs = {stats['unique_state_action_pairs']}")

    # ── Step 5: Compute PMI on non-self-loop transitions ──
    print("\n[5/8] Computing PMI on non-self-loop transitions...")
    pmi_nonself = {}
    for key in ["live_wikipedia", "live_python_docs"]:
        nonself_triples = []
        for t in datasets[key]:
            s_url = normalize_url(t["state_before"]["url"])
            s_next = normalize_url(t["state_after"]["url"])
            if s_url != s_next:
                a_href = t["action"].get("target_href", "")
                nonself_triples.append((s_url, a_href, s_next))
        stats = compute_pmi_stats(nonself_triples)
        pmi_nonself[key] = stats
        print(f"  {key} (non-self): mean_PMI = {stats['mean_pmi']:.6f} bits, N = {stats['N']}")

    # ── Step 6: Permutation tests (4 primary comparisons) ──
    print("\n[6/8] Running permutation tests (1000 permutations each)...")
    perm_tests = {}
    conditions = {
        "live_wikipedia": {
            "all": all_data["live_wikipedia"]["triple_groups"],
            "nonself": None,  # built below
        },
        "live_python_docs": {
            "all": all_data["live_python_docs"]["triple_groups"],
            "nonself": None,
        },
    }

    # Build non-self-loop triple groups for permutation tests
    for key in ["live_wikipedia", "live_python_docs"]:
        nonself_groups = {}
        for tid, triples in all_data[key]["triple_groups"].items():
            nonself = []
            for s, a, s_next in triples:
                if s != s_next:
                    nonself.append((s, a, s_next))
            if nonself:
                nonself_groups[tid] = nonself
        conditions[key]["nonself"] = nonself_groups

    # Run all 4 primary permutation tests
    for site_key in ["live_wikipedia", "live_python_docs"]:
        for cond_key, cond_groups in conditions[site_key].items():
            test_name = f"{site_key}_{cond_key}"
            # Compute observed mean PMI from all triples in this condition
            all_triples = []
            for triples in cond_groups.values():
                all_triples.extend(triples)
            obs_stats = compute_pmi_stats(all_triples)
            obs_mean = obs_stats["mean_pmi"]

            print(f"  Running permutation test: {test_name} (observed PMI = {obs_mean:.6f})...")
            perm_result = permutation_test(cond_groups, obs_mean, N_PERMUTATIONS, SEED)
            perm_tests[test_name] = perm_result
            print(f"    p = {perm_result['p_value']:.6f}, effect_d = {perm_result['effect_size_d']:.4f}")

    # ── Step 7: Permutation test on positive control ──
    print("\n[7/8] Permutation test on positive control...")
    pos_ctrl_groups = all_data["positive_control"]["triple_groups"]
    pos_obs = compute_pmi_stats(all_data["positive_control"]["triples"])
    pos_perm = permutation_test(pos_ctrl_groups, pos_obs["mean_pmi"], N_PERMUTATIONS, SEED)
    perm_tests["positive_control"] = pos_perm
    print(f"  Positive control: observed PMI = {pos_obs['mean_pmi']:.6f}, p = {pos_perm['p_value']:.6f}")

    # Null control: permutation test on shuffled null data
    null_ctrl_groups = all_data["null_control"]["triple_groups"]
    null_obs = compute_pmi_stats(all_data["null_control"]["triples"])
    null_perm = permutation_test(null_ctrl_groups, null_obs["mean_pmi"], N_PERMUTATIONS, SEED)
    perm_tests["null_control"] = null_perm
    print(f"  Null control: observed PMI = {null_obs['mean_pmi']:.6f}, p = {null_perm['p_value']:.6f}")

    # ── Step 8: Decision evaluation ──
    print("\n[8/8] Evaluating decision rules...")

    # SURVIVES_CURRENT_TEST requires ALL:
    survives_checks = {}
    survives = True

    # Check 1-4: PMI > 0 on live data after Bonferroni correction
    for test_name in ["live_wikipedia_all", "live_python_docs_all",
                       "live_wikipedia_nonself", "live_python_docs_nonself"]:
        perm = perm_tests[test_name]
        p_bonf = min(perm["p_value"] * BONFERRONI_COMPARISONS, 1.0)
        passes = perm["observed_mean_pmi"] > 0 and p_bonf < 0.05
        survives_checks[test_name] = {
            "observed_pmi": perm["observed_mean_pmi"],
            "p_raw": perm["p_value"],
            "p_bonferroni": p_bonf,
            "passes": passes,
        }
        if not passes:
            survives = False
        print(f"  {test_name}: PMI={perm['observed_mean_pmi']:.6f}, p_bonf={p_bonf:.6f}, pass={passes}")

    # Check 5: Positive control PMI >= 1.0
    pos_passes = pos_obs["mean_pmi"] >= 1.0
    survives_checks["positive_control"] = {
        "pmi": pos_obs["mean_pmi"],
        "passes": pos_passes,
    }
    if not pos_passes:
        survives = False
    print(f"  Positive control PMI >= 1.0: {pos_obs['mean_pmi']:.6f}, pass={pos_passes}")

    # Check 6: Null control PMI not significantly > 0
    null_passes = null_perm["p_value"] > 0.05
    survives_checks["null_control"] = {
        "pmi": null_obs["mean_pmi"],
        "p": null_perm["p_value"],
        "passes": null_passes,
    }
    if not null_passes:
        survives = False
    print(f"  Null control p > 0.05: {null_perm['p_value']:.6f}, pass={null_passes}")

    # Check 7: PMI does not exceed shuffled baseline (already included in 1-4)
    # Check 8: Non-self PMI >= All PMI
    nonself_check = {}
    for site_key in ["live_wikipedia", "live_python_docs"]:
        pmi_all = pmi_results[site_key]["mean_pmi"]
        pmi_ns = pmi_nonself[site_key]["mean_pmi"]
        passes = pmi_ns >= pmi_all
        nonself_check[site_key] = {
            "pmi_all": pmi_all,
            "pmi_nonself": pmi_ns,
            "passes": passes,
        }
        if not passes:
            survives = False
        print(f"  {site_key} non-self >= all: {pmi_ns:.6f} >= {pmi_all:.6f}, pass={passes}")

    # FALSIFIED-IN-SETTING if any of the falsifiers
    falsified = False
    falsification_reasons = []
    for test_name, check in survives_checks.items():
        if not check["passes"]:
            falsified = True
            falsification_reasons.append(f"{test_name} failed")

    # Determine outcome
    if survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif falsified:
        outcome = "FALSIFIES"
        status = "COMPLETE"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    print(f"\n{'=' * 70}")
    print(f"OUTCOME: {outcome}")
    print(f"STATUS: {status}")
    if falsification_reasons:
        print(f"FALSIFICATION REASONS: {', '.join(falsification_reasons)}")
    print(f"{'=' * 70}")

    # ── Build results dictionary ──
    results = {
        "experiment_id": EXPERIMENT_ID,
        "lane": "physics",
        "datasets_loaded": {k: len(v) for k, v in datasets.items()},
        "self_loop_stats": self_loop_stats,
        "pmi_all_transitions": {k: {"mean_pmi": v["mean_pmi"], "N": v["N"],
                                      "unique_states": v["unique_states"],
                                      "unique_SA_pairs": v["unique_state_action_pairs"]}
                                  for k, v in pmi_results.items()},
        "pmi_nonself_transitions": {k: {"mean_pmi": v["mean_pmi"], "N": v["N"]}
                                     for k, v in pmi_nonself.items()},
        "permutation_tests": {k: {
            "observed_pmi": v["observed_mean_pmi"],
            "p_value": v["p_value"],
            "null_mean": v["null_mean"],
            "null_std": v["null_std"],
            "effect_size_d": v["effect_size_d"],
        } for k, v in perm_tests.items()},
        "survives_checks": survives_checks,
        "nonself_vs_all": nonself_check,
        "survives": survives,
        "falsified": falsified,
        "falsification_reasons": falsification_reasons,
        "outcome": outcome,
        "status": status,
    }

    return results


if __name__ == "__main__":
    os.environ["PYTHONHASHSEED"] = "0"
    results = run_experiment()

    # Save raw results
    out_path = os.path.join(os.path.dirname(__file__), "raw_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_path}")
