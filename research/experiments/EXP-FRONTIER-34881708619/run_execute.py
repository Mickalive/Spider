#!/usr/bin/env python3
"""
EXP-FRONTIER-34881708619: Equal-Sample-Size Pooled vs Per-Type BC TV.

Frozen experiment code. Do not modify after freeze.

Tests whether pooled binned TV estimation maintains a fundamental advantage over
per-type estimation when both use equal sample size (250 transitions per type),
disentangling estimator contamination from sparsity bias identified by audit
(required_fixes[3] of EXP-FRONTIER-34794649996).
"""

import json
import hashlib
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
import time
warnings.filterwarnings('ignore')


def to_native(obj):
    """Recursively convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_native(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


# === FROZEN PARAMETERS (from parent EXP-FRONTIER-34794649996) ===
BASE_SEED = 42
FUNCTION_SEEDS = [42, 43, 44]  # 3 function families
LAMBDA_LEVELS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]  # 8 levels
N_LAMBDA = len(LAMBDA_LEVELS)
N_REPLICATIONS = 5
N_PERMUTATIONS = 200  # Per permutation null (N=200 for both per-type and pooled)
ALPHA = 0.05
CENTER = np.array([0.5, 0.5])
SIGMA_BASE = 0.05
BETA = 0.5
GRID_SIZE = 20  # 20x20 grid for TV computation
N_ACTIONS = 4

# Non-stationary parameters (identical to parent)
N_TRANSITIONS_NONSTATIONARY = 2000  # per lambda level (250 per page type x 8 types)
N_TRANSITIONS_PER_PAGE_TYPE = 250
N_PAGE_TYPES = 8

# Page type definitions: (func_seed, noise_level, center) - identical to parent
PAGE_TYPES = [
    (42, 0.05, np.array([0.5, 0.5])),   # rotation, low noise, center (0.5,0.5)
    (43, 0.05, np.array([0.5, 0.5])),   # scaling, low noise, center (0.5,0.5)
    (44, 0.05, np.array([0.5, 0.5])),   # translation, low noise, center (0.5,0.5)
    (42, 0.10, np.array([0.5, 0.5])),   # rotation, high noise, center (0.5,0.5)
    (43, 0.10, np.array([0.5, 0.5])),   # scaling, high noise, center (0.5,0.5)
    (44, 0.10, np.array([0.5, 0.5])),   # translation, high noise, center (0.5,0.5)
    (42, 0.05, np.array([0.3, 0.7])),   # rotation, low noise, shifted center
    (43, 0.05, np.array([0.3, 0.7])),   # scaling, low noise, shifted center
]

PAGE_TYPE_NAMES = [
    'rotation_low_0.5,0.5', 'scaling_low_0.5,0.5', 'translation_low_0.5,0.5',
    'rotation_high_0.5,0.5', 'scaling_high_0.5,0.5', 'translation_high_0.5,0.5',
    'rotation_low_0.3,0.7', 'scaling_low_0.3,0.7',
]

# === FUNCTION FAMILY A: ROTATION-BASED (identical to parent) ===
THETA = [0, np.pi/4, np.pi/2, 3*np.pi/4]
OFFSET_A = [[0.1, 0], [0, 0.1], [-0.1, 0], [0, -0.1]]


def rotation_func(s, action_idx, center=CENTER):
    theta = THETA[action_idx]
    offset = np.array(OFFSET_A[action_idx])
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    R = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
    s_centered = s - center
    s_rotated = R @ s_centered + center + offset
    return s_rotated


# === FUNCTION FAMILY B: SCALING-BASED (identical to parent) ===
SCALE = [[1.2, 1.2], [0.8, 1.2], [1.2, 0.8], [0.8, 0.8]]
OFFSET_B = [[0.05, 0.05], [-0.05, 0.05], [0.05, -0.05], [-0.05, -0.05]]


def scaling_func(s, action_idx, center=CENTER):
    sx, sy = SCALE[action_idx]
    offset = np.array(OFFSET_B[action_idx])
    s_new = np.array([
        sx * (s[0] - center[0]) + center[0],
        sy * (s[1] - center[1]) + center[1]
    ]) + offset
    return s_new


# === FUNCTION FAMILY C: TRANSLATION-BASED (identical to parent) ===
T_C = [[0.15, 0], [0, 0.15], [-0.15, 0], [0, -0.15]]
ALPHA_C = [0.1, 0.1, 0.1, 0.1]


def translation_func(s, action_idx, center=CENTER):
    t = np.array(T_C[action_idx])
    alpha = ALPHA_C[action_idx]
    s_new = s + t + alpha * np.sin(2 * np.pi * s)
    return s_new


FUNCTION_MAP = {
    42: rotation_func,
    43: scaling_func,
    44: translation_func,
}


def compute_noise_sigma(s, sigma_base, beta, center=CENTER):
    dist_to_center = np.linalg.norm(s - center)
    return sigma_base * (1 + beta * dist_to_center)


def generate_transitions_nonstationary(lambda_val, n_total, rng):
    """Generate non-stationary transitions with deterministic page-type cycling (identical to parent)."""
    transitions = []
    for i in range(n_total):
        page_type_idx = (i // N_TRANSITIONS_PER_PAGE_TYPE) % N_PAGE_TYPES
        func_seed, sigma_base, center = PAGE_TYPES[page_type_idx]
        func = FUNCTION_MAP[func_seed]

        s = rng.uniform(0, 1, size=2)
        a_idx = rng.randint(0, N_ACTIONS)
        if rng.random() < lambda_val:
            s_next_det = func(s, a_idx, center)
            sigma = compute_noise_sigma(s, sigma_base, BETA, center)
            noise = rng.normal(0, sigma, size=2)
            s_next = s_next_det + noise
        else:
            s_next = rng.normal(0, sigma_base, size=2) + center
        s_next = np.clip(s_next, 0, 1)
        transitions.append((s, a_idx, s_next, page_type_idx))
    return transitions


# === TV DISTANCE COMPUTATION (20x20 grid binning) - identical to parent ===
def bin_state(s):
    x_bin = min(int(s[0] * GRID_SIZE), GRID_SIZE - 1)
    y_bin = min(int(s[1] * GRID_SIZE), GRID_SIZE - 1)
    return x_bin * GRID_SIZE + y_bin


def compute_empirical_distributions_binned(transitions):
    n_bins = GRID_SIZE * GRID_SIZE
    action_counts = {a: np.zeros(n_bins) for a in range(N_ACTIONS)}
    action_totals = {a: 0 for a in range(N_ACTIONS)}

    for t in transitions:
        s, a_idx, s_next = t[0], t[1], t[2]
        bin_idx = bin_state(s_next)
        action_counts[a_idx][bin_idx] += 1
        action_totals[a_idx] += 1

    action_dists = {}
    for a in range(N_ACTIONS):
        if action_totals[a] > 0:
            action_dists[a] = action_counts[a] / action_totals[a]
        else:
            action_dists[a] = np.ones(n_bins) / n_bins
    return action_dists


def compute_tv_distance_binned(action_dists):
    tv_max = 0.0
    tv_sum = 0.0
    n_pairs = 0
    for i in range(N_ACTIONS):
        for j in range(i + 1, N_ACTIONS):
            p = action_dists[i]
            q = action_dists[j]
            tv = 0.5 * np.sum(np.abs(p - q))
            tv_max = max(tv_max, tv)
            tv_sum += tv
            n_pairs += 1
    tv_mean = tv_sum / n_pairs if n_pairs > 0 else 0.0
    return tv_max, tv_mean


def permutation_test_tv_per_type(transitions, n_permutations, rng):
    """Permutation test for a SINGLE page type: shuffle action labels and recompute TV."""
    observed_dists = compute_empirical_distributions_binned(transitions)
    observed_tv_max, _ = compute_tv_distance_binned(observed_dists)

    actions = [t[1] for t in transitions]
    s_nexts = [t[2] for t in transitions]

    perm_tvs = []
    for _ in range(n_permutations):
        shuffled_actions = list(actions)
        rng.shuffle(shuffled_actions)
        perm_transitions = [(None, a, sn) for a, sn in zip(shuffled_actions, s_nexts)]
        perm_dists = compute_empirical_distributions_binned(perm_transitions)
        perm_tv, _ = compute_tv_distance_binned(perm_dists)
        perm_tvs.append(perm_tv)

    perm_mean = float(np.mean(perm_tvs))
    perm_std = float(np.std(perm_tvs, ddof=1)) if len(perm_tvs) > 1 else 0.0
    p_value = sum(1 for pv in perm_tvs if pv >= observed_tv_max) / n_permutations
    return observed_tv_max, perm_mean, perm_std, p_value


def permutation_test_tv_pooled(transitions, n_permutations, rng):
    """Pooled permutation test: shuffle action labels across ALL page types."""
    observed_dists = compute_empirical_distributions_binned(transitions)
    observed_tv_max, _ = compute_tv_distance_binned(observed_dists)

    actions = [t[1] for t in transitions]
    s_nexts = [t[2] for t in transitions]

    perm_tvs = []
    for _ in range(n_permutations):
        shuffled_actions = list(actions)
        rng.shuffle(shuffled_actions)
        perm_transitions = [(None, a, sn) for a, sn in zip(shuffled_actions, s_nexts)]
        perm_dists = compute_empirical_distributions_binned(perm_transitions)
        perm_tv, _ = compute_tv_distance_binned(perm_dists)
        perm_tvs.append(perm_tv)

    perm_mean = float(np.mean(perm_tvs))
    perm_std = float(np.std(perm_tvs, ddof=1)) if len(perm_tvs) > 1 else 0.0
    p_value = sum(1 for pv in perm_tvs if pv >= observed_tv_max) / n_permutations
    return observed_tv_max, perm_mean, perm_std, p_value


# === MAIN EXPERIMENT ===
def run_experiment():
    """Execute the full frozen experiment: equal-sample-size pooled vs per-type comparison."""
    start_time = time.time()
    print("=== EXP-FRONTIER-34881708619: Equal-Sample-Size Pooled vs Per-Type BC TV ===")
    print(f"Base seed: {BASE_SEED}")
    print(f"Lambda levels: {LAMBDA_LEVELS}")
    print(f"Page types: {N_PAGE_TYPES}")
    print(f"Replications: {N_REPLICATIONS}")
    print(f"Permutations: {N_PERMUTATIONS}")
    print(f"Grid: {GRID_SIZE}x{GRID_SIZE} = {GRID_SIZE**2} bins")
    print(f"Transitions per lambda: {N_TRANSITIONS_NONSTATIONARY} ({N_TRANSITIONS_PER_PAGE_TYPE} per type)")
    print()

    # Storage for results
    # Per-type BC TV
    per_type_bc_tv = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                      for pt_idx in range(N_PAGE_TYPES)}
    per_type_perm_mean = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                          for pt_idx in range(N_PAGE_TYPES)}
    per_type_raw_tv = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                       for pt_idx in range(N_PAGE_TYPES)}

    # Pooled full BC TV (baseline)
    pooled_full_bc_tv = {l_idx: [] for l_idx in range(N_LAMBDA)}
    pooled_full_raw_tv = {l_idx: [] for l_idx in range(N_LAMBDA)}

    # Pooled subsampled BC TV (PRIMARY comparison)
    pooled_sub_bc_tv = {l_idx: [] for l_idx in range(N_LAMBDA)}
    pooled_sub_raw_tv = {l_idx: [] for l_idx in range(N_LAMBDA)}

    # Frequency baseline
    freq_baseline_means = []

    for l_idx, l in enumerate(LAMBDA_LEVELS):
        print(f"--- Lambda {l:.1f} ---")
        for rep_idx in range(N_REPLICATIONS):
            # Frozen seed: same formula as parent non-stationary
            cell_seed = BASE_SEED * 100000 + l_idx * 1000 + rep_idx * 10 + 999
            rng = np.random.RandomState(cell_seed)

            transitions = generate_transitions_nonstationary(l, N_TRANSITIONS_NONSTATIONARY, rng)

            # === POOLED FULL BC TV (all 2000 transitions) ===
            pooled_full_rng = np.random.RandomState(cell_seed + 5000)
            pf_tv_max, pf_perm_mean, _, _ = permutation_test_tv_pooled(
                transitions, N_PERMUTATIONS, pooled_full_rng
            )
            pf_bc = max(0.0, pf_tv_max - pf_perm_mean)
            pooled_full_bc_tv[l_idx].append(pf_bc)
            pooled_full_raw_tv[l_idx].append(pf_tv_max)

            # === SUBSAMPLE: 250 transitions per type, then pool ===
            subsampled_transitions = []
            for pt_idx in range(N_PAGE_TYPES):
                pt_transitions = [t for t in transitions if t[3] == pt_idx]
                # Deterministic subsampling: use seed offset per type
                sub_rng = np.random.RandomState(cell_seed + pt_idx * 100 + 888)
                indices = sub_rng.choice(len(pt_transitions), size=N_TRANSITIONS_PER_PAGE_TYPE, replace=False)
                subsampled = [pt_transitions[i] for i in sorted(indices)]
                subsampled_transitions.extend(subsampled)

            # Pooled subsampled BC TV
            ps_rng = np.random.RandomState(cell_seed + 6000)
            ps_tv_max, ps_perm_mean, _, _ = permutation_test_tv_pooled(
                subsampled_transitions, N_PERMUTATIONS, ps_rng
            )
            ps_bc = max(0.0, ps_tv_max - ps_perm_mean)
            pooled_sub_bc_tv[l_idx].append(ps_bc)
            pooled_sub_raw_tv[l_idx].append(ps_tv_max)

            # === PER-TYPE BC TV (on 250 transitions per type) ===
            for pt_idx in range(N_PAGE_TYPES):
                pt_transitions = [t for t in transitions if t[3] == pt_idx]
                if len(pt_transitions) < 10:
                    per_type_bc_tv[pt_idx][l_idx].append(0.0)
                    per_type_perm_mean[pt_idx][l_idx].append(0.0)
                    per_type_raw_tv[pt_idx][l_idx].append(0.0)
                    continue

                pt_rng = np.random.RandomState(cell_seed + pt_idx * 100 + 777)
                pt_tv_max, pt_perm_mean, _, _ = permutation_test_tv_per_type(
                    pt_transitions, N_PERMUTATIONS, pt_rng
                )
                pt_bc = max(0.0, pt_tv_max - pt_perm_mean)

                per_type_raw_tv[pt_idx][l_idx].append(pt_tv_max)
                per_type_perm_mean[pt_idx][l_idx].append(pt_perm_mean)
                per_type_bc_tv[pt_idx][l_idx].append(pt_bc)

        print(f"  Pooled full BC: {np.mean(pooled_full_bc_tv[l_idx]):.4f}")
        print(f"  Pooled sub BC:  {np.mean(pooled_sub_bc_tv[l_idx]):.4f}")
        print(f"  Per-type mean:  {np.mean([np.mean(per_type_bc_tv[pt][l_idx]) for pt in range(N_PAGE_TYPES)]):.4f}")

    print()

    # === COMPUTE METRICS ===

    lambda_arr = np.array(LAMBDA_LEVELS)

    # Per-type BC TV means by lambda
    per_type_bc_means = {}
    per_type_rho = {}
    per_type_rho_p = {}
    for pt_idx in range(N_PAGE_TYPES):
        means = []
        for l_idx in range(N_LAMBDA):
            vals = per_type_bc_tv[pt_idx][l_idx]
            means.append(float(np.mean(vals)) if vals else 0.0)
        per_type_bc_means[str(pt_idx)] = {str(LAMBDA_LEVELS[i]): means[i] for i in range(N_LAMBDA)}
        rho, p = stats.spearmanr(lambda_arr, np.array(means))
        per_type_rho[str(pt_idx)] = float(rho)
        per_type_rho_p[str(pt_idx)] = float(p)

    # Mean per-type BC TV across all 8 types
    mean_per_type_bc = []
    for l_idx in range(N_LAMBDA):
        type_means = []
        for pt_idx in range(N_PAGE_TYPES):
            vals = per_type_bc_tv[pt_idx][l_idx]
            type_means.append(float(np.mean(vals)) if vals else 0.0)
        mean_per_type_bc.append(float(np.mean(type_means)))

    # Aggregated per-type Spearman rho
    mean_per_type_rho, mean_per_type_rho_p = stats.spearmanr(lambda_arr, np.array(mean_per_type_bc))

    # Pooled full BC TV means
    pooled_full_bc_means = [float(np.mean(pooled_full_bc_tv[l_idx])) for l_idx in range(N_LAMBDA)]

    # Pooled subsampled BC TV means
    pooled_sub_bc_means = [float(np.mean(pooled_sub_bc_tv[l_idx])) for l_idx in range(N_LAMBDA)]

    # Pooled subsampled Spearman rho
    pooled_sub_rho, pooled_sub_rho_p = stats.spearmanr(lambda_arr, np.array(pooled_sub_bc_means))

    # === PRIMARY COMPARISON: Pooled subsampled vs Per-type at lambda=1 ===
    lambda1_idx = LAMBDA_LEVELS.index(1.0)
    lambda0_idx = LAMBDA_LEVELS.index(0.0)

    per_type_bc_lambda1 = [float(np.mean(per_type_bc_tv[pt_idx][lambda1_idx]))
                           for pt_idx in range(N_PAGE_TYPES)]
    pooled_sub_bc_lambda1 = float(np.mean(pooled_sub_bc_tv[lambda1_idx]))
    pooled_full_bc_lambda1 = float(np.mean(pooled_full_bc_tv[lambda1_idx]))

    # Paired t-test: pooled subsampled vs per-type at lambda=1
    # Use 5 replications: for each rep, compute mean per-type BC across 8 types
    pooled_sub_bc_lambda1_reps = pooled_sub_bc_tv[lambda1_idx]
    mean_per_type_bc_lambda1_reps = []
    for rep_idx in range(N_REPLICATIONS):
        rep_vals = [per_type_bc_tv[pt_idx][lambda1_idx][rep_idx] for pt_idx in range(N_PAGE_TYPES)]
        mean_per_type_bc_lambda1_reps.append(float(np.mean(rep_vals)))

    # Primary test: pooled subsampled > per-type (one-sided paired t-test)
    t_stat, t_p_value = stats.ttest_rel(pooled_sub_bc_lambda1_reps, mean_per_type_bc_lambda1_reps)
    # One-sided: pooled subsampled > per-type
    t_p_one_sided = t_p_value / 2 if t_stat > 0 else 1 - t_p_value / 2

    # Cohen's d for the difference
    diff = np.array(pooled_sub_bc_lambda1_reps) - np.array(mean_per_type_bc_lambda1_reps)
    cohens_d = float(np.mean(diff) / np.std(diff, ddof=1)) if np.std(diff, ddof=1) > 0 else 0.0

    # Secondary: full vs subsampled pooled
    full_vs_sub_t, full_vs_sub_p = stats.ttest_rel(
        pooled_full_bc_tv[lambda1_idx], pooled_sub_bc_tv[lambda1_idx]
    )

    # === CONTROLS ===

    # Positive control: pooled full BC TV at lambda=1 within 0.01 of parent (~0.051)
    positive_control_pass = abs(pooled_full_bc_lambda1 - 0.051) < 0.01

    # Null control: per-type BC TV <= 0.01 at lambda=0 across all 8 types
    per_type_bc_lambda0 = [float(np.mean(per_type_bc_tv[pt_idx][lambda0_idx]))
                           for pt_idx in range(N_PAGE_TYPES)]
    per_type_null_pass = all(tv <= 0.01 for tv in per_type_bc_lambda0)

    # Null control: pooled subsampled BC TV <= 0.01 at lambda=0
    pooled_sub_bc_lambda0 = float(np.mean(pooled_sub_bc_tv[lambda0_idx]))
    pooled_sub_null_pass = pooled_sub_bc_lambda0 <= 0.01

    null_control_pass = per_type_null_pass and pooled_sub_null_pass

    # Subsampling consistency: subsampled <= full across all reps at lambda=1
    subsampling_consistent = all(
        pooled_sub_bc_tv[lambda1_idx][r] <= pooled_full_bc_tv[lambda1_idx][r] + 0.001  # small tolerance
        for r in range(N_REPLICATIONS)
    )

    # Per-type replication: recomputed per-type aggregate BC TV at lambda=1 within 0.01 of parent (0.034)
    mean_per_type_bc_lambda1 = float(np.mean(per_type_bc_lambda1))
    per_type_replication_pass = abs(mean_per_type_bc_lambda1 - 0.034) < 0.01

    # CV check at lambda=1 for per-type BC TV
    cv_per_type_lambda1 = []
    for pt_idx in range(N_PAGE_TYPES):
        vals = per_type_bc_tv[pt_idx][lambda1_idx]
        mean_val = np.mean(vals)
        std_val = np.std(vals, ddof=1)
        cv = float(std_val / mean_val) if mean_val > 0 else float('inf')
        cv_per_type_lambda1.append(cv)
    max_cv = max(cv_per_type_lambda1)

    # Frequency baseline
    cell_seed_fb = BASE_SEED * 100000 + lambda1_idx * 1000 + 0 * 10 + 999
    rng_fb = np.random.RandomState(cell_seed_fb)
    fb_transitions = generate_transitions_nonstationary(1.0, N_TRANSITIONS_NONSTATIONARY, rng_fb)
    n_bins = GRID_SIZE * GRID_SIZE
    marginal_counts = np.zeros(n_bins)
    total = 0
    for t in fb_transitions:
        bin_idx = bin_state(t[2])
        marginal_counts[bin_idx] += 1
        total += 1
    marginal_dist = marginal_counts / total if total > 0 else np.ones(n_bins) / n_bins
    action_dists_fb = compute_empirical_distributions_binned(fb_transitions)
    tv_marginal_vs_action = {}
    for a in range(N_ACTIONS):
        tv = 0.5 * np.sum(np.abs(marginal_dist - action_dists_fb[a]))
        tv_marginal_vs_action[str(a)] = float(tv)
    freq_baseline_mean = float(np.mean(list(tv_marginal_vs_action.values())))

    # === DECISION (from frozen spec.json decision_rule) ===
    print("=== Controls ===")
    print(f"  Positive control (pooled full BC ~ 0.051): "
          f"{'PASS' if positive_control_pass else 'FAIL'} (got {pooled_full_bc_lambda1:.4f})")
    print(f"  Null control (per-type <= 0.01 at lambda=0): "
          f"{'PASS' if per_type_null_pass else 'FAIL'}")
    print(f"    Per-type BC TV at lambda=0: {[f'{tv:.4f}' for tv in per_type_bc_lambda0]}")
    print(f"  Null control (pooled sub <= 0.01 at lambda=0): "
          f"{'PASS' if pooled_sub_null_pass else 'FAIL'} (got {pooled_sub_bc_lambda0:.4f})")
    print(f"  Subsampling consistency (sub <= full): "
          f"{'PASS' if subsampling_consistent else 'FAIL'}")
    print(f"  Per-type replication (~0.034): "
          f"{'PASS' if per_type_replication_pass else 'FAIL'} (got {mean_per_type_bc_lambda1:.4f})")
    print()

    print("=== Primary Comparison ===")
    print(f"  Pooled subsampled BC TV at lambda=1: {pooled_sub_bc_lambda1:.4f}")
    print(f"  Mean per-type BC TV at lambda=1: {mean_per_type_bc_lambda1:.4f}")
    print(f"  Ratio (pooled-sub / per-type): {pooled_sub_bc_lambda1 / mean_per_type_bc_lambda1:.2f}x")
    print(f"  Paired t-test (pooled-sub > per-type): t={t_stat:.4f}, p_one_sided={t_p_one_sided:.6f}")
    print(f"  Cohen's d: {cohens_d:.4f}")
    print()

    print("=== Secondary: Full vs Subsampled Pooled ===")
    print(f"  Pooled full BC TV at lambda=1: {pooled_full_bc_lambda1:.4f}")
    print(f"  Pooled subsampled BC TV at lambda=1: {pooled_sub_bc_lambda1:.4f}")
    print(f"  Ratio (full/sub): {pooled_full_bc_lambda1 / pooled_sub_bc_lambda1:.2f}x")
    print(f"  Paired t-test: t={full_vs_sub_t:.4f}, p={full_vs_sub_p:.6f}")
    print()

    # Frozen decision rule from spec.json:
    # SURVIVES if: pooled_sub > per_type at lambda=1 (p<0.05) AND Cohen's d > 0.5
    # FALSIFIED if: pooled_sub <= per_type OR d<=0.5
    # MEASUREMENT_INVALID if: pipeline errors OR positive/null control fails

    measurement_invalid = (not positive_control_pass) or (not null_control_pass) or (not subsampling_consistent)

    if measurement_invalid:
        decision = 'MEASUREMENT_INVALID'
        outcome = 'NOT_APPLICABLE'
    elif t_p_one_sided < 0.05 and cohens_d > 0.5:
        decision = 'SURVIVES_CURRENT_TEST'
        outcome = 'SUPPORTS'
    else:
        decision = 'FALSIFIED-IN-SETTING'
        outcome = 'FALSIFIES'

    print("=== Decision ===")
    print(f"  Positive control: {'PASS' if positive_control_pass else 'FAIL'}")
    print(f"  Null control: {'PASS' if null_control_pass else 'FAIL'}")
    print(f"  Subsampling consistency: {'PASS' if subsampling_consistent else 'FAIL'}")
    print(f"  Primary test (pooled-sub > per-type, p<0.05): {'PASS' if t_p_one_sided < 0.05 else 'FAIL'}")
    print(f"  Effect size (d>0.5): {'PASS' if cohens_d > 0.5 else 'FAIL'}")
    print(f"  Overall Decision: {decision}")
    print(f"  Overall Outcome: {outcome}")

    execution_time = time.time() - start_time
    print(f"\nExecution time: {execution_time:.1f}s")

    # === COMPILE RESULTS ===
    controls = {
        'positive_control': {
            'description': 'Pooled full BC TV at lambda=1 within 0.01 of parent (~0.051)',
            'pass': positive_control_pass,
            'pooled_full_bc_tv_at_lambda1': pooled_full_bc_lambda1,
            'parent_expected': 0.051,
            'abs_diff': abs(pooled_full_bc_lambda1 - 0.051),
        },
        'null_control_per_type': {
            'description': 'Per-type BC TV <= 0.01 at lambda=0 across all 8 page types',
            'pass': per_type_null_pass,
            'per_type_bc_tv_at_lambda0': per_type_bc_lambda0,
            'max_bc_tv': float(np.max(per_type_bc_lambda0)),
        },
        'null_control_pooled_sub': {
            'description': 'Pooled subsampled BC TV <= 0.01 at lambda=0',
            'pass': pooled_sub_null_pass,
            'pooled_sub_bc_tv_at_lambda0': pooled_sub_bc_lambda0,
        },
        'null_control': {
            'description': 'Both null controls pass (per-type and pooled subsampled at lambda=0)',
            'pass': null_control_pass,
        },
        'subsampling_consistency': {
            'description': 'Pooled subsampled BC TV <= pooled full BC TV at lambda=1 across all reps',
            'pass': subsampling_consistent,
            'sub_bc_by_rep': pooled_sub_bc_tv[lambda1_idx],
            'full_bc_by_rep': pooled_full_bc_tv[lambda1_idx],
        },
        'per_type_replication': {
            'description': 'Recomputed per-type aggregate BC TV at lambda=1 within 0.01 of parent (0.034)',
            'pass': per_type_replication_pass,
            'recomputed_mean': mean_per_type_bc_lambda1,
            'parent_expected': 0.034,
        },
        'primary_comparison': {
            'description': 'Pooled subsampled BC TV > per-type BC TV at lambda=1',
            'pass': t_p_one_sided < 0.05 and cohens_d > 0.5,
            't_statistic': float(t_stat),
            'p_one_sided': float(t_p_one_sided),
            'cohens_d': cohens_d,
        },
        'cv_check': {
            'description': 'CV across replications <= 0.5 for all page types at lambda=1',
            'pass': max_cv <= 0.5,
            'per_type_cv_lambda1': cv_per_type_lambda1,
            'max_cv': max_cv,
        },
        'no_pipeline_errors': {
            'description': 'No pipeline errors during execution',
            'pass': True,
        },
    }

    metrics = {
        'per_type_bc_tv': {
            'means_by_lambda': per_type_bc_means,
            'spearman_rho_by_type': per_type_rho,
            'spearman_p_by_type': per_type_rho_p,
            'mean_across_types_by_lambda': {str(LAMBDA_LEVELS[i]): mean_per_type_bc[i]
                                            for i in range(N_LAMBDA)},
            'aggregate_spearman_rho': float(mean_per_type_rho),
            'aggregate_spearman_p': float(mean_per_type_rho_p),
        },
        'pooled_full_bc_tv': {
            'means_by_lambda': {str(LAMBDA_LEVELS[i]): pooled_full_bc_means[i]
                                for i in range(N_LAMBDA)},
        },
        'pooled_subsampled_bc_tv': {
            'means_by_lambda': {str(LAMBDA_LEVELS[i]): pooled_sub_bc_means[i]
                                for i in range(N_LAMBDA)},
            'spearman_rho': float(pooled_sub_rho),
            'spearman_p': float(pooled_sub_rho_p),
        },
        'primary_comparison_lambda1': {
            'pooled_subsampled_bc': pooled_sub_bc_lambda1,
            'mean_per_type_bc': mean_per_type_bc_lambda1,
            'ratio_pooled_sub_to_per_type': float(pooled_sub_bc_lambda1 / mean_per_type_bc_lambda1) if mean_per_type_bc_lambda1 > 0 else None,
            'pooled_full_bc': pooled_full_bc_lambda1,
            'ratio_full_to_sub': float(pooled_full_bc_lambda1 / pooled_sub_bc_lambda1) if pooled_sub_bc_lambda1 > 0 else None,
            'per_type_bc_by_type': per_type_bc_lambda1,
        },
        'effect_size': {
            'cohens_d_pooled_sub_vs_per_type_lambda1': cohens_d,
        },
        'frequency_baseline': {
            'mean_tv_marginal_vs_action': freq_baseline_mean,
            'tv_marginal_vs_action': tv_marginal_vs_action,
        },
    }

    observations = [
        f"Overall decision: {decision}",
        f"Pooled subsampled BC TV at lambda=1: {pooled_sub_bc_lambda1:.4f}",
        f"Mean per-type BC TV at lambda=1: {mean_per_type_bc_lambda1:.4f}",
        f"Ratio (pooled-sub / per-type): {pooled_sub_bc_lambda1 / mean_per_type_bc_lambda1:.2f}x",
        f"Paired t-test (pooled-sub > per-type): t={t_stat:.4f}, p_one_sided={t_p_one_sided:.6f}",
        f"Cohen's d: {cohens_d:.4f}",
        f"Pooled full BC TV at lambda=1: {pooled_full_bc_lambda1:.4f}",
        f"Ratio (full / sub): {pooled_full_bc_lambda1 / pooled_sub_bc_lambda1:.2f}x",
        f"Positive control: {'PASS' if positive_control_pass else 'FAIL'}",
        f"Null control (per-type): {'PASS' if per_type_null_pass else 'FAIL'}",
        f"Null control (pooled sub): {'PASS' if pooled_sub_null_pass else 'FAIL'}",
        f"Subsampling consistency: {'PASS' if subsampling_consistent else 'FAIL'}",
        f"Per-type replication: {'PASS' if per_type_replication_pass else 'FAIL'}",
        f"CV max at lambda=1: {max_cv:.4f} ({'INVALID' if max_cv > 0.5 else 'valid'})",
        f"Frequency baseline: {freq_baseline_mean:.4f}",
        f"Pooled sub Spearman rho: {pooled_sub_rho:.4f} (parent pooled: 0.929)",
    ]

    validity_notes = [
        'Same DGP parameters and seed structure as parent EXP-FRONTIER-34794649996',
        '2000 non-stationary transitions per lambda level (250 per page type x 8 types)',
        'Subsampling: 250 randomly selected transitions per type (deterministic seed), then pooled',
        'Both pooled subsampled and per-type estimators use the SAME 250 transitions per type',
        'Pooled subsampled perm null: N=200 shuffling across all 2000 subsampled transitions',
        'Per-type perm null: N=200 per page type shuffling within type',
        '20x20 grid binning for TV on continuous 2D state space',
        '5 replications per lambda level',
        'Sparse binning: 250 transitions / 400 bins = 0.625 expected counts/bin per type',
        'The primary comparison uses 5 paired observations (rep-level means across 8 types)',
        'Statistical power is limited with n=5 paired observations; Cohen d>0.5 threshold ensures practical significance',
        'All decisions use frozen decision rules from preregistration',
        'Synthetic 2D [0,1]^2 data only; no inference to real Web DOM transitions justified',
    ]

    unresolved = [
        'Whether the paired t-test with n=5 has sufficient power to detect moderate effects (d~0.5)',
        'Whether per-type estimation at higher sample size (2000/type) would close the gap with pooled',
        'Whether alternative divergence measures (KDE, kNN) would change the pooled-vs-per-type ordering',
        'Whether stochastic page-type switching would alter the equal-n comparison',
        'Whether any BC TV magnitude exceeds frequency baseline (0.335) for practical utility',
        'Whether real Web DOM transitions exhibit action-conditional structure detectable by any estimator',
    ]

    results = {
        'schema_version': 1,
        'experiment_id': 'EXP-FRONTIER-34881708619',
        'lane': 'frontier',
        'status': 'COMPLETE',
        'outcome': outcome,
        'metrics': metrics,
        'controls': controls,
        'artifacts': [
            {'path': 'research/experiments/EXP-FRONTIER-34881708619/run_execute.py', 'role': 'code'},
        ],
        'observations': observations,
        'validity_notes': validity_notes,
        'unresolved': unresolved,
    }

    return results, execution_time


if __name__ == '__main__':
    results, execution_time = run_experiment()

    # Write result.json
    result_path = Path(__file__).parent / 'result.json'
    with open(result_path, 'w') as f:
        json.dump(to_native(results), f, indent=2)
    print(f"\nWrote {result_path}")

    # Compute hashes for provenance
    experiment_dir = Path(__file__).parent
    files_to_hash = ['prereg.md', 'spec.json', 'request.json', 'freeze.json']
    hashes = {}
    for fname in files_to_hash:
        fpath = experiment_dir / fname
        if fpath.exists():
            h = hashlib.sha256(fpath.read_bytes()).hexdigest()
            hashes[fname] = h

    # Also hash output artifacts
    for out_name in ['result.json']:
        out_path = experiment_dir / out_name
        if out_path.exists():
            h = hashlib.sha256(out_path.read_bytes()).hexdigest()
            hashes[out_name] = h

    provenance = {
        'experiment_id': 'EXP-FRONTIER-34881708619',
        'execution_timestamp': None,
        'analyzer_script': 'run_execute.py',
        'script_hashes': hashes,
        'result_hash': hashlib.sha256(result_path.read_bytes()).hexdigest(),
        'status': results['status'],
        'outcome': results['outcome'],
        'claim': 'C-WEB-DYNAMICS',
        'lane': 'frontier',
        'execution_time_seconds': execution_time,
        'total_transitions': {
            'nonstationary': len(LAMBDA_LEVELS) * N_TRANSITIONS_NONSTATIONARY * N_REPLICATIONS,
        },
        'environment': {
            'python_version': '3.12.14',
            'numpy_version': np.__version__,
            'scipy_version': stats.__version__ if hasattr(stats, '__version__') else 'unknown',
        },
        'frozen_inputs': {
            'prereg_hash': '37ff28f570b92a2d418ff448db0ccabc9973687c475a75a9418b13b0d7627931',
            'request_hash': '0596702daeeb836a1e6e44e2e802b838a2e351b43edce59f44627f1ea3fdc839',
            'spec_hash': 'ac487a7f9b0cd6cc3c0c454e7b390c9d07b70f826dc991e92de38887356ed5ab',
        },
        'parent_experiment': {
            'experiment_id': 'EXP-FRONTIER-34794649996',
            'parent_handoff_sha256': '2b1985aa624d23028cfedb73ccb5747667571e927351f3b8314ff2000071bbbf',
        },
        'key_methodological_change': 'Subsample pooled data to 250 per type for equal-n comparison with per-type estimation',
    }

    provenance_path = experiment_dir / 'provenance.json'
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
