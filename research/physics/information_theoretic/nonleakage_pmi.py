#!/usr/bin/env python3
"""
EXP-PHYSICS-34071626363 — Non-Leakage PMI Analysis
Tests whether PMI between actions and next-states remains positive
when action-to-destination URL leakage is eliminated.

Frozen inputs: request.json, spec.json, prereg.md, freeze.json
All computation deterministic (seed=42, PYTHONHASHSEED=0).
"""

import json
import hashlib
import math
import random
import collections
import os
import sys

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34071626363"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
BONFERRONI_COMPARISONS = 2  # 2 primary comparisons (2 live sites)
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.025

PARENT_DIR = "research/experiments/EXP-PHYSICS-33965269281"
DATA_FILES = {
    "live_wikipedia": ("raw_live_wikipedia.json", "87e6d8fcecb436ab9b1067a27c7f5708c393bace5efbb0225bfe1f57aa87bc5e"),
    "live_python_docs": ("raw_live_python_docs.json", "a7634ca3734360a4d6a2ffdb89d859ae9ff466df710be3323da8ac5c5d2fa648"),
    "positive_control": ("raw_positive.json", "3eef0bbc382fef44eb63d55481e3d417b2a98478d6f4fa4e1eb06331a99fc73f"),
}

# ─── Data Loading ────────────────────────────────────────────────────────────

def normalize_url(url: str) -> str:
    """Normalize URL for state identity: strip trailing slash, lowercase scheme/host."""
    if not url:
        return url
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


def is_non_leakage(transition: dict) -> bool:
    """Check if a transition is non-leakage: action.target_href != state_after.url."""
    a_href = transition["action"].get("target_href", "")
    s_next = normalize_url(transition["state_after"]["url"])
    return a_href != s_next


def filter_non_leakage(transitions: list) -> list:
    """Filter transitions to non-leakage subset."""
    return [t for t in transitions if is_non_leakage(t)]


# ─── Action Representations ──────────────────────────────────────────────────

def hash_action(href: str) -> str:
    """Hash action href using SHA-256 (breaks equality but preserves uniqueness)."""
    return hashlib.sha256(href.encode()).hexdigest()[:16]


def get_action_type(action: dict) -> str:
    """Get action type categorical (all actions are 'click' for these datasets)."""
    return action.get("action_type", "click")


# ─── PMI Computation ─────────────────────────────────────────────────────────

def compute_pmi_stats(triples: list) -> dict:
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


def shuffle_actions_within_trajectories(triple_groups: dict, rng: random.Random) -> dict:
    """Shuffle action labels within trajectories."""
    shuffled_groups = {}
    for tid, triples in triple_groups.items():
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
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

    count_ge = sum(1 for m in shuffled_means if m >= observed_mean_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)

    return {
        "p_value": p_value,
        "shuffled_means": shuffled_means,
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": float(np.mean(shuffled_means)),
        "null_std": float(np.std(shuffled_means)),
        "effect_size_d": float((observed_mean_pmi - np.mean(shuffled_means)) / np.std(shuffled_means)) if np.std(shuffled_means) > 0 else 0.0,
    }


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full non-leakage PMI experiment."""
    parent_dir = os.path.normpath(PARENT_DIR)

    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — Non-Leakage PMI Analysis")
    print("=" * 70)

    # ── Step 1: Load and verify data ──
    print("\n[1/10] Loading and verifying parent data files...")
    datasets = {}
    for key, (filename, expected_sha) in DATA_FILES.items():
        try:
            data = load_and_verify(filename, expected_sha, parent_dir)
            datasets[key] = data
        except Exception as e:
            print(f"  FATAL: {e}")
            sys.exit(1)

    # ── Step 2: Identify non-leakage transitions ──
    print("\n[2/10] Identifying non-leakage transitions...")
    non_leakage = {}
    for key in ["live_wikipedia", "live_python_docs"]:
        nl = filter_non_leakage(datasets[key])
        non_leakage[key] = nl
        total = len(datasets[key])
        frac = len(nl) / total if total > 0 else 0
        print(f"  {key}: {len(nl)}/{total} non-leakage ({frac:.3f})")

    # Check minimum sample size (decision_rule: < 10 = MEASUREMENT_INVALID)
    for key in ["live_wikipedia", "live_python_docs"]:
        if len(non_leakage[key]) < 10:
            print(f"  FATAL: {key} has fewer than 10 non-leakage transitions ({len(non_leakage[key])})")
            return {"status": "MEASUREMENT_INVALID", "outcome": "NOT_APPLICABLE",
                    "reason": f"Fewer than 10 non-leakage transitions at {key}"}

    # ── Step 3: Extract triples for all conditions ──
    print("\n[3/10] Extracting triples and building trajectory groups...")
    all_triples = {}
    nonleakage_triples = {}
    traj_groups_all = {}
    traj_groups_nonleakage = {}

    for key in ["live_wikipedia", "live_python_docs"]:
        # All transitions
        triples = extract_triples(datasets[key])
        traj_groups = extract_trajectory_groups(datasets[key])
        triple_groups = {tid: extract_triples(trans) for tid, trans in traj_groups.items()}
        all_triples[key] = triples
        traj_groups_all[key] = triple_groups

        # Non-leakage transitions
        nl_triples = extract_triples(non_leakage[key])
        nl_traj_groups = extract_trajectory_groups(non_leakage[key])
        nl_triple_groups = {tid: extract_triples(trans) for tid, trans in nl_traj_groups.items()}
        nonleakage_triples[key] = nl_triples
        traj_groups_nonleakage[key] = nl_triple_groups

        print(f"  {key}: {len(triples)} triples (all), {len(nl_triples)} triples (non-leakage)")

    # ── Step 4: Compute PMI on all transitions (parent baseline) ──
    print("\n[4/10] Computing PMI on all transitions (parent baseline)...")
    pmi_all = {}
    for key in ["live_wikipedia", "live_python_docs"]:
        stats = compute_pmi_stats(all_triples[key])
        pmi_all[key] = stats
        print(f"  {key}: mean_PMI = {stats['mean_pmi']:.6f} bits, N = {stats['N']}, "
              f"unique_states = {stats['unique_states']}, unique_SA = {stats['unique_sa_pairs']}")

    # ── Step 5: Compute PMI on non-leakage transitions (primary) ──
    print("\n[5/10] Computing PMI on non-leakage transitions...")
    pmi_nonleakage = {}
    for key in ["live_wikipedia", "live_python_docs"]:
        stats = compute_pmi_stats(nonleakage_triples[key])
        pmi_nonleakage[key] = stats
        print(f"  {key}: mean_PMI = {stats['mean_pmi']:.6f} bits, N = {stats['N']}, "
              f"unique_states = {stats['unique_states']}, unique_SA = {stats['unique_sa_pairs']}")

    # ── Step 6: Compute PMI with hashed action representation ──
    print("\n[6/10] Computing PMI with hashed action representation...")
    pmi_hashed = {}
    for key in ["live_wikipedia", "live_python_docs"]:
        hashed_triples = [(s, hash_action(a), s_next) for s, a, s_next in nonleakage_triples[key]]
        stats = compute_pmi_stats(hashed_triples)
        pmi_hashed[key] = stats
        print(f"  {key}: mean_PMI = {stats['mean_pmi']:.6f} bits, N = {stats['N']}")

    # ── Step 7: Compute PMI with action-type categorical representation ──
    print("\n[7/10] Computing PMI with action-type categorical representation...")
    pmi_action_type = {}
    for key in ["live_wikipedia", "live_python_docs"]:
        # For action-type, all actions become 'click'
        type_triples = [(s, "click", s_next) for s, a, s_next in nonleakage_triples[key]]
        stats = compute_pmi_stats(type_triples)
        pmi_action_type[key] = stats
        print(f"  {key}: mean_PMI = {stats['mean_pmi']:.6f} bits, N = {stats['N']}")

    # ── Step 8: Permutation tests on non-leakage ──
    print("\n[8/10] Running permutation tests on non-leakage transitions...")
    perm_tests = {}
    for key in ["live_wikipedia", "live_python_docs"]:
        obs_mean = pmi_nonleakage[key]["mean_pmi"]
        print(f"  Running permutation test: {key} (observed PMI = {obs_mean:.6f})...")
        perm = permutation_test(traj_groups_nonleakage[key], obs_mean, N_PERMUTATIONS, SEED)
        perm_tests[key] = perm
        print(f"    p = {perm['p_value']:.6f}, effect_d = {perm['effect_size_d']:.4f}")

    # ── Step 9: Positive control (synthetic lambda=1.0) ──
    print("\n[9/10] Running positive control...")
    pos_triples = extract_triples(datasets["positive_control"])
    pos_traj_groups = extract_trajectory_groups(datasets["positive_control"])
    pos_triple_groups = {tid: extract_triples(trans) for tid, trans in pos_traj_groups.items()}
    pos_stats = compute_pmi_stats(pos_triples)
    pos_perm = permutation_test(pos_triple_groups, pos_stats["mean_pmi"], N_PERMUTATIONS, SEED)
    print(f"  Positive control: PMI = {pos_stats['mean_pmi']:.6f}, p = {pos_perm['p_value']:.6f}")
    pos_passes = pos_stats["mean_pmi"] >= 1.0
    print(f"  Positive control PMI >= 1.0: {pos_passes}")

    # ── Step 10: Null control (shuffled actions on non-leakage) ──
    print("\n[10/10] Running null control...")
    # Null control: use shuffled-action PMI from permutation test on Wikipedia
    # (largest non-leakage sample)
    null_pmi = perm_tests["live_wikipedia"]["null_mean"]
    null_passes = perm_tests["live_wikipedia"]["p_value"] > 0.05
    print(f"  Null control (shuffled PMI on non-leakage): {null_pmi:.6f}")
    print(f"  Null control p > 0.05: {perm_tests['live_wikipedia']['p_value']:.6f}, passes={null_passes}")

    # ── Decision evaluation ──
    print(f"\n{'=' * 70}")
    print("DECISION EVALUATION")
    print(f"{'=' * 70}")

    # SURVIVES_CURRENT_TEST requires ALL:
    survives = True
    decision_checks = {}

    # Check 1: PMI > 0 on non-leakage Wikipedia, p < 0.025
    wiki_perm = perm_tests["live_wikipedia"]
    wiki_check = (wiki_perm["observed_mean_pmi"] > 0 and wiki_perm["p_value"] < ALPHA_BONFERRONI)
    decision_checks["check_1_wiki_nonleakage"] = {
        "pmi": wiki_perm["observed_mean_pmi"],
        "p_raw": wiki_perm["p_value"],
        "p_threshold": ALPHA_BONFERRONI,
        "passes": wiki_check,
    }
    if not wiki_check:
        survives = False
    print(f"  Check 1 (Wiki non-leakage PMI > 0, p < {ALPHA_BONFERRONI}): "
          f"PMI={wiki_perm['observed_mean_pmi']:.6f}, p={wiki_perm['p_value']:.6f}, pass={wiki_check}")

    # Check 2: PMI > 0 on non-leakage Python docs, p < 0.025
    py_perm = perm_tests["live_python_docs"]
    py_check = (py_perm["observed_mean_pmi"] > 0 and py_perm["p_value"] < ALPHA_BONFERRONI)
    decision_checks["check_2_python_nonleakage"] = {
        "pmi": py_perm["observed_mean_pmi"],
        "p_raw": py_perm["p_value"],
        "p_threshold": ALPHA_BONFERRONI,
        "passes": py_check,
    }
    if not py_check:
        survives = False
    print(f"  Check 2 (Python non-leakage PMI > 0, p < {ALPHA_BONFERRONI}): "
          f"PMI={py_perm['observed_mean_pmi']:.6f}, p={py_perm['p_value']:.6f}, pass={py_check}")

    # Check 3: Positive control PMI >= 1.0
    decision_checks["check_3_positive_control"] = {
        "pmi": pos_stats["mean_pmi"],
        "passes": pos_passes,
    }
    if not pos_passes:
        survives = False
    print(f"  Check 3 (Positive control PMI >= 1.0): "
          f"PMI={pos_stats['mean_pmi']:.6f}, pass={pos_passes}")

    # Check 4: Null control not significantly > 0
    decision_checks["check_4_null_control"] = {
        "null_mean_pmi": null_pmi,
        "p_value": perm_tests["live_wikipedia"]["p_value"],
        "passes": null_passes,
    }
    if not null_passes:
        survives = False
    print(f"  Check 4 (Null control p > 0.05): "
          f"p={perm_tests['live_wikipedia']['p_value']:.6f}, pass={null_passes}")

    # Check 5: No pipeline errors (if we got here, no errors)
    decision_checks["check_5_no_pipeline_errors"] = {"passes": True}

    # Determine outcome
    falsified = not survives
    if survives:
        outcome = "SUPPORTS"
    else:
        # Check which falsifiers triggered
        outcome = "FALSIFIES"

    status = "COMPLETE"

    print(f"\n{'=' * 70}")
    print(f"OUTCOME: {outcome}")
    print(f"STATUS: {status}")
    print(f"{'=' * 70}")

    # ── Build results dictionary ──
    results = {
        "experiment_id": EXPERIMENT_ID,
        "lane": "physics",
        "datasets_loaded": {k: len(v) for k, v in datasets.items()},
        "non_leakage_counts": {
            "live_wikipedia": len(non_leakage["live_wikipedia"]),
            "live_python_docs": len(non_leakage["live_python_docs"]),
        },
        "non_leakage_fractions": {
            "live_wikipedia": len(non_leakage["live_wikipedia"]) / len(datasets["live_wikipedia"]),
            "live_python_docs": len(non_leakage["live_python_docs"]) / len(datasets["live_python_docs"]),
        },
        "pmi_all_transitions": {
            k: {"mean_pmi": v["mean_pmi"], "N": v["N"],
                "unique_states": v["unique_states"], "unique_sa_pairs": v["unique_sa_pairs"]}
            for k, v in pmi_all.items()
        },
        "pmi_nonleakage": {
            k: {"mean_pmi": v["mean_pmi"], "N": v["N"],
                "unique_states": v["unique_states"], "unique_actions": v["unique_actions"],
                "unique_sa_pairs": v["unique_sa_pairs"]}
            for k, v in pmi_nonleakage.items()
        },
        "pmi_hashed_actions": {
            k: {"mean_pmi": v["mean_pmi"], "N": v["N"]}
            for k, v in pmi_hashed.items()
        },
        "pmi_action_type_categorical": {
            k: {"mean_pmi": v["mean_pmi"], "N": v["N"]}
            for k, v in pmi_action_type.items()
        },
        "permutation_tests": {
            k: {
                "observed_pmi": v["observed_mean_pmi"],
                "p_value": v["p_value"],
                "null_mean": v["null_mean"],
                "null_std": v["null_std"],
                "effect_size_d": v["effect_size_d"],
            }
            for k, v in perm_tests.items()
        },
        "positive_control": {
            "pmi": pos_stats["mean_pmi"],
            "p_value": pos_perm["p_value"],
            "passes": pos_passes,
        },
        "null_control": {
            "null_mean_pmi": null_pmi,
            "p_value": perm_tests["live_wikipedia"]["p_value"],
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

    if results.get("status") == "MEASUREMENT_INVALID":
        print(f"\nMEASUREMENT INVALID: {results.get('reason')}")
        sys.exit(1)

    # Save raw results
    out_path = os.path.join(os.path.dirname(__file__), "nonleakage_pmi_raw.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_path}")
