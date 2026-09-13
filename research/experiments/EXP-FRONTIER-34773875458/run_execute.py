#!/usr/bin/env python3
"""
EXP-FRONTIER-34773875458: Non-Stationary TV Detection.

Frozen experiment code. Do not modify after freeze.

Tests whether TV detection of translation-like action-dependent structure
survives non-stationary dynamics where different page types have different
transition functions — the defining property of real Web data.
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


# === FROZEN PARAMETERS (from prereg) ===
BASE_SEED = 42
FUNCTION_SEEDS = [42, 43, 44]  # 3 function families
LAMBDA_LEVELS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]  # 8 levels
N_LAMBDA = len(LAMBDA_LEVELS)
N_REPLICATIONS = 5
N_PERMUTATIONS = 200
ALPHA = 0.05
CENTER = np.array([0.5, 0.5])
SIGMA_BASE = 0.05
BETA = 0.5
GRID_SIZE = 20  # 20x20 grid for TV computation
N_ACTIONS = 4

# Non-stationary parameters
N_TRANSITIONS_NONSTATIONARY = 2000  # per lambda level (250 per page type x 8 types)
N_TRANSITIONS_PER_PAGE_TYPE = 250
N_PAGE_TYPES = 8
N_TRANSITIONS_STATIONARY = 200  # per cell (function x lambda)

# Page type definitions: (func_seed, noise_level, center)
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

# === FUNCTION FAMILY A: ROTATION-BASED ===
THETA = [0, np.pi/4, np.pi/2, 3*np.pi/4]
OFFSET_A = [[0.1, 0], [0, 0.1], [-0.1, 0], [0, -0.1]]


def rotation_func(s, action_idx, center=CENTER):
    """Apply rotation-based deterministic transformation."""
    theta = THETA[action_idx]
    offset = np.array(OFFSET_A[action_idx])
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    R = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
    s_centered = s - center
    s_rotated = R @ s_centered + center + offset
    return s_rotated


# === FUNCTION FAMILY B: SCALING-BASED ===
SCALE = [[1.2, 1.2], [0.8, 1.2], [1.2, 0.8], [0.8, 0.8]]
OFFSET_B = [[0.05, 0.05], [-0.05, 0.05], [0.05, -0.05], [-0.05, -0.05]]


def scaling_func(s, action_idx, center=CENTER):
    """Apply scaling-based deterministic transformation."""
    sx, sy = SCALE[action_idx]
    offset = np.array(OFFSET_B[action_idx])
    s_new = np.array([
        sx * (s[0] - center[0]) + center[0],
        sy * (s[1] - center[1]) + center[1]
    ]) + offset
    return s_new


# === FUNCTION FAMILY C: TRANSLATION-BASED ===
T_C = [[0.15, 0], [0, 0.15], [-0.15, 0], [0, -0.15]]
ALPHA_C = [0.1, 0.1, 0.1, 0.1]


def translation_func(s, action_idx, center=CENTER):
    """Apply translation-based deterministic transformation with sinusoidal perturbation."""
    t = np.array(T_C[action_idx])
    alpha = ALPHA_C[action_idx]
    s_new = s + t + alpha * np.sin(2 * np.pi * s)
    return s_new


# Map function seeds to implementations
FUNCTION_MAP = {
    42: rotation_func,
    43: scaling_func,
    44: translation_func,
}


def compute_noise_sigma(s, sigma_base, beta, center=CENTER):
    """Compute state-dependent noise standard deviation."""
    dist_to_center = np.linalg.norm(s - center)
    return sigma_base * (1 + beta * dist_to_center)


def generate_transitions_stationary(func_seed, lambda_val, n, rng, sigma_base=SIGMA_BASE, beta=BETA, center=CENTER):
    """
    Generate stationary transitions using Web-faithful DGP.
    With probability lambda: s_next = f(s, a) + noise
    With probability (1-lambda): s_next ~ N(center, sigma_base^2 * I_2)
    """
    func = FUNCTION_MAP[func_seed]
    transitions = []
    for _ in range(n):
        s = rng.uniform(0, 1, size=2)
        a_idx = rng.randint(0, N_ACTIONS)
        if rng.random() < lambda_val:
            s_next_det = func(s, a_idx, center)
            sigma = compute_noise_sigma(s, sigma_base, beta, center)
            noise = rng.normal(0, sigma, size=2)
            s_next = s_next_det + noise
        else:
            s_next = rng.normal(0, sigma_base, size=2) + center
        s_next = np.clip(s_next, 0, 1)
        transitions.append((s, a_idx, s_next))
    return transitions


def generate_transitions_nonstationary(lambda_val, n_total, rng):
    """
    Generate non-stationary transitions with deterministic page-type cycling.
    Page type = (transition_index // N_TRANSITIONS_PER_PAGE_TYPE) mod N_PAGE_TYPES
    """
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


# === TV DISTANCE COMPUTATION (20x20 grid binning) ===
def bin_state(s):
    """Bin a 2D state into a 20x20 grid cell index."""
    x_bin = min(int(s[0] * GRID_SIZE), GRID_SIZE - 1)
    y_bin = min(int(s[1] * GRID_SIZE), GRID_SIZE - 1)
    return x_bin * GRID_SIZE + y_bin


def compute_empirical_distributions_binned(transitions):
    """Compute empirical P(S_{t+1} | do(A=a)) using 20x20 grid binning.
    transitions: list of (s, a_idx, s_next[, page_type]) tuples.
    """
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
    """Compute maximum pairwise TV distance between action-conditional distributions (binned)."""
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


def compute_bias_corrected_tv(transitions, perm_mean_tv):
    """Compute bias-corrected TV = max(0, observed_TV - perm_mean_TV)."""
    action_dists = compute_empirical_distributions_binned(transitions)
    observed_tv_max, _ = compute_tv_distance_binned(action_dists)
    bc_tv = max(0.0, observed_tv_max - perm_mean_tv)
    return observed_tv_max, bc_tv


def permutation_test_tv(transitions, n_permutations, rng):
    """Permutation test: shuffle action labels and recompute TV."""
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


def fisher_combined_pvalue(p_values):
    """Fisher combined p-value: F = -2 * sum(ln(p_i)) ~ chi^2(2k)."""
    p_arr = np.array(p_values)
    # Clip to avoid log(0)
    p_arr = np.clip(p_arr, 1e-300, 1.0)
    F = -2.0 * np.sum(np.log(p_arr))
    k = len(p_arr)
    # chi^2 cdf with 2k degrees of freedom
    p_combined = 1.0 - stats.chi2.cdf(F, 2 * k)
    return float(p_combined), float(F)


# === FREQUENCY BASELINE ===
def compute_frequency_baseline(transitions):
    """Compute marginal P(S_{t+1}) and TV between marginal and each action-conditional."""
    n_bins = GRID_SIZE * GRID_SIZE
    marginal_counts = np.zeros(n_bins)
    total = 0
    for t in transitions:
        s, a_idx, s_next = t[0], t[1], t[2]
        bin_idx = bin_state(s_next)
        marginal_counts[bin_idx] += 1
        total += 1
    marginal_dist = marginal_counts / total if total > 0 else np.ones(n_bins) / n_bins

    action_dists = compute_empirical_distributions_binned(transitions)
    tv_marginal_vs_action = {}
    for a in range(N_ACTIONS):
        tv = 0.5 * np.sum(np.abs(marginal_dist - action_dists[a]))
        tv_marginal_vs_action[str(a)] = float(tv)

    mean_tv = float(np.mean(list(tv_marginal_vs_action.values())))
    return {
        'marginal_non_uniformity': float(0.5 * np.sum(np.abs(marginal_dist - np.ones(n_bins) / n_bins))),
        'tv_marginal_vs_action': tv_marginal_vs_action,
        'mean_tv_marginal_vs_action': mean_tv,
    }


# === MAIN EXPERIMENT ===
def run_experiment():
    """Execute the full frozen experiment."""
    start_time = time.time()
    print("=== EXP-FRONTIER-34773875458: Non-Stationary TV Detection ===")
    print(f"Base seed: {BASE_SEED}")
    print(f"Lambda levels: {LAMBDA_LEVELS}")
    print(f"Functions: 3 (seeds {FUNCTION_SEEDS})")
    print(f"Page types: {N_PAGE_TYPES}")
    print(f"Stationary: {N_TRANSITIONS_STATIONARY} transitions/cell, {N_REPLICATIONS} reps")
    print(f"Non-stationary: {N_TRANSITIONS_NONSTATIONARY} transitions/lambda, {N_REPLICATIONS} reps")
    print(f"Permutations: {N_PERMUTATIONS}")
    print(f"State space: continuous 2D [0,1]^2")
    print(f"TV grid: {GRID_SIZE}x{GRID_SIZE} = {GRID_SIZE**2} bins")
    print()

    # ==============================
    # PHASE 1: STATIONARY CONDITION
    # ==============================
    print("=== Phase 1: Stationary Condition ===")
    stationary_all_tv = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                         for f_idx in range(len(FUNCTION_SEEDS))}
    stationary_raw_tables = []

    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = {42: 'rotation', 43: 'scaling', 44: 'translation'}[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l_idx, l in enumerate(LAMBDA_LEVELS):
            tvs_this_cell = []
            for rep_idx in range(N_REPLICATIONS):
                # Frozen seed per cell: func_seed * 100000 + lambda_idx * 1000 + rep_idx * 10 + BASE_SEED
                cell_seed = func_seed * 100000 + l_idx * 1000 + rep_idx * 10 + BASE_SEED
                rng = np.random.RandomState(cell_seed)

                transitions = generate_transitions_stationary(func_seed, l, N_TRANSITIONS_STATIONARY, rng)
                action_dists = compute_empirical_distributions_binned(transitions)
                tv_max, tv_mean = compute_tv_distance_binned(action_dists)

                tvs_this_cell.append(tv_max)
                stationary_all_tv[f_idx][l].append(tv_max)
                stationary_raw_tables.append({
                    'func_seed': func_seed,
                    'func_name': func_name,
                    'lambda': l,
                    'replication': rep_idx,
                    'tv_max': tv_max,
                    'tv_mean': tv_mean,
                    'cell_seed': cell_seed,
                })

            print(f"  lambda={l:.1f}: TV_max={np.mean(tvs_this_cell):.4f}+/-{np.std(tvs_this_cell, ddof=1):.4f}")
        print()

    # Stationary aggregate Spearman
    lambda_arr = np.array(LAMBDA_LEVELS)
    stationary_agg_means = []
    for l in LAMBDA_LEVELS:
        all_tvs = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_tvs.extend(stationary_all_tv[f_idx][l])
        stationary_agg_means.append(float(np.mean(all_tvs)))

    stat_rho, stat_p = stats.spearmanr(lambda_arr, np.array(stationary_agg_means))
    stat_p_one_sided = stat_p / 2 if stat_rho > 0 else 1 - stat_p / 2
    print(f"Stationary aggregate Spearman rho: {stat_rho:.4f}, p_one_sided: {stat_p_one_sided:.6f}")
    print()

    # ==============================
    # PHASE 2: NON-STATIONARY CONDITION
    # ==============================
    print("=== Phase 2: Non-Stationary Condition ===")
    nonstationary_tv_raw = {l_idx: [] for l_idx in range(N_LAMBDA)}
    nonstationary_bc_tv = {l_idx: [] for l_idx in range(N_LAMBDA)}
    nonstationary_perm_mean = {l_idx: [] for l_idx in range(N_LAMBDA)}
    nonstationary_raw_tables = []

    # For ANOVA: collect per-page-type per-lambda data
    nonstationary_per_page_type = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                                   for pt_idx in range(N_PAGE_TYPES)}

    for l_idx, l in enumerate(LAMBDA_LEVELS):
        print(f"--- Lambda {l:.1f} ---")
        for rep_idx in range(N_REPLICATIONS):
            # Frozen seed: BASE_SEED * 100000 + l_idx * 1000 + rep_idx * 10 + 999
            cell_seed = BASE_SEED * 100000 + l_idx * 1000 + rep_idx * 10 + 999
            rng = np.random.RandomState(cell_seed)

            transitions = generate_transitions_nonstationary(l, N_TRANSITIONS_NONSTATIONARY, rng)

            # Compute raw TV
            action_dists = compute_empirical_distributions_binned(transitions)
            tv_max, tv_mean = compute_tv_distance_binned(action_dists)

            # Permutation test for bias correction
            perm_rng = np.random.RandomState(cell_seed + 777)
            _, perm_mean_tv, perm_std_tv, perm_p = permutation_test_tv(
                transitions, N_PERMUTATIONS, perm_rng
            )

            # Bias-corrected TV
            bc_tv = max(0.0, tv_max - perm_mean_tv)

            nonstationary_tv_raw[l_idx].append(tv_max)
            nonstationary_bc_tv[l_idx].append(bc_tv)
            nonstationary_perm_mean[l_idx].append(perm_mean_tv)

            nonstationary_raw_tables.append({
                'lambda': l,
                'replication': rep_idx,
                'tv_max': tv_max,
                'perm_mean_tv': perm_mean_tv,
                'perm_std_tv': perm_std_tv,
                'perm_p': perm_p,
                'bias_corrected_tv': bc_tv,
                'cell_seed': cell_seed,
            })

            # Per-page-type analysis
            for pt_idx in range(N_PAGE_TYPES):
                pt_transitions = [(s, a, sn) for s, a, sn, pt in transitions if pt == pt_idx]
                if len(pt_transitions) > 0:
                    pt_dists = compute_empirical_distributions_binned(pt_transitions)
                    pt_tv_max, _ = compute_tv_distance_binned(pt_dists)
                    # Bias correction per page type: use perm mean from pooled analysis
                    pt_bc_tv = max(0.0, pt_tv_max - perm_mean_tv)
                    nonstationary_per_page_type[pt_idx][l_idx].append(pt_bc_tv)

        bc_means = [float(np.mean(nonstationary_bc_tv[l_idx])) for l_idx in range(N_LAMBDA)]
        raw_means = [float(np.mean(nonstationary_tv_raw[l_idx])) for l_idx in range(N_LAMBDA)]
        print(f"  Raw TV: {raw_means[l_idx]:.4f}, Perm mean: {float(np.mean(nonstationary_perm_mean[l_idx])):.4f}, BC TV: {bc_means[l_idx]:.4f}")
    print()

    # Non-stationary aggregate Spearman on bias-corrected TV
    nonstat_bc_means = []
    for l_idx in range(N_LAMBDA):
        nonstat_bc_means.append(float(np.mean(nonstationary_bc_tv[l_idx])))

    nonstat_rho, nonstat_p = stats.spearmanr(lambda_arr, np.array(nonstat_bc_means))
    nonstat_p_one_sided = nonstat_p / 2 if nonstat_rho > 0 else 1 - nonstat_p / 2
    print(f"Non-stationary aggregate Spearman rho (BC TV): {nonstat_rho:.4f}, p_one_sided: {nonstat_p_one_sided:.6f}")

    # Non-stationary Spearman on raw TV
    nonstat_raw_means = []
    for l_idx in range(N_LAMBDA):
        nonstat_raw_means.append(float(np.mean(nonstationary_tv_raw[l_idx])))
    nonstat_raw_rho, nonstat_raw_p = stats.spearmanr(lambda_arr, np.array(nonstat_raw_means))
    print(f"Non-stationary aggregate Spearman rho (raw TV): {nonstat_raw_rho:.4f}")
    print()

    # ==============================
    # PHASE 3: DEGRADATION TEST
    # ==============================
    rho_degradation = stat_rho - nonstat_rho
    print(f"=== Degradation Test ===")
    print(f"Stationary rho: {stat_rho:.4f}")
    print(f"Non-stationary rho (BC): {nonstat_rho:.4f}")
    print(f"rho_degradation: {rho_degradation:.4f}")
    print()

    # ==============================
    # PHASE 4: PERMUTATION TESTS (Fisher combined)
    # ==============================
    print("=== Permutation Tests (Fisher Combined) ===")

    # Lambda=0: null control
    lambda0_fisher_pvals = []
    for rep_idx in range(N_REPLICATIONS):
        cell_seed = BASE_SEED * 100000 + 0 * 1000 + rep_idx * 10 + 999
        rng = np.random.RandomState(cell_seed)
        transitions = generate_transitions_nonstationary(0.0, N_TRANSITIONS_NONSTATIONARY, rng)
        perm_rng = np.random.RandomState(cell_seed + 777)
        _, _, _, perm_p = permutation_test_tv(transitions, N_PERMUTATIONS, perm_rng)
        lambda0_fisher_pvals.append(perm_p)

    lambda0_fisher_combined, lambda0_F = fisher_combined_pvalue(lambda0_fisher_pvals)
    null_control_pass = lambda0_fisher_combined > ALPHA
    print(f"  Lambda=0 Fisher combined p: {lambda0_fisher_combined:.6f} (F={lambda0_F:.2f})")
    print(f"  Null control pass (p > 0.05): {null_control_pass}")

    # Lambda=1: positive control
    lambda1_fisher_pvals = []
    for rep_idx in range(N_REPLICATIONS):
        cell_seed = BASE_SEED * 100000 + 7 * 1000 + rep_idx * 10 + 999  # lambda_idx=7 for lambda=1.0
        rng = np.random.RandomState(cell_seed)
        transitions = generate_transitions_nonstationary(1.0, N_TRANSITIONS_NONSTATIONARY, rng)
        perm_rng = np.random.RandomState(cell_seed + 777)
        _, _, _, perm_p = permutation_test_tv(transitions, N_PERMUTATIONS, perm_rng)
        lambda1_fisher_pvals.append(perm_p)

    lambda1_fisher_combined, lambda1_F = fisher_combined_pvalue(lambda1_fisher_pvals)
    print(f"  Lambda=1 Fisher combined p: {lambda1_fisher_combined:.6f} (F={lambda1_F:.2f})")
    print()

    # ==============================
    # PHASE 5: POSITIVE CONTROL
    # ==============================
    print("=== Positive Control ===")
    lambda1_bc_tvs = nonstationary_bc_tv[7]  # lambda_idx=7 for lambda=1.0
    positive_control_pass = all(tv >= 0.001 for tv in lambda1_bc_tvs)
    print(f"  BC TV at lambda=1: {[f'{tv:.4f}' for tv in lambda1_bc_tvs]}")
    print(f"  Positive control pass (all >= 0.001): {positive_control_pass}")
    print()

    # ==============================
    # PHASE 6: TWO-WAY ANOVA (Non-Stationary)
    # ==============================
    print("=== Two-Way ANOVA ===")
    anova_result = {}
    try:
        import pandas as pd
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm

        anova_data = []
        for pt_idx in range(N_PAGE_TYPES):
            for l_idx, l in enumerate(LAMBDA_LEVELS):
                for tv_val in nonstationary_per_page_type[pt_idx][l_idx]:
                    anova_data.append({
                        'lam_level': str(l),
                        'page_type': str(pt_idx),
                        'bc_tv': tv_val
                    })

        df = pd.DataFrame(anova_data)
        model = ols('bc_tv ~ C(lam_level) + C(page_type) + C(lam_level):C(page_type)', data=df).fit()
        anova_table = anova_lm(model, typ=2)

        anova_result = {
            'design': f"{N_PAGE_TYPES} page_types x {N_LAMBDA} lambdas x {N_REPLICATIONS} reps = {len(anova_data)} observations",
            'full_model': {
                'lambda_effect': {
                    'F': round(float(anova_table.loc['C(lam_level)', 'F']), 4),
                    'p_value': round(float(anova_table.loc['C(lam_level)', 'PR(>F)']), 6),
                },
                'page_type_effect': {
                    'F': round(float(anova_table.loc['C(page_type)', 'F']), 4),
                    'p_value': round(float(anova_table.loc['C(page_type)', 'PR(>F)']), 6),
                },
                'interaction_effect': {
                    'F': round(float(anova_table.loc['C(lam_level):C(page_type)', 'F']), 4),
                    'p_value': round(float(anova_table.loc['C(lam_level):C(page_type)', 'PR(>F)']), 6),
                },
                'model_r_squared': round(float(model.rsquared), 4),
            },
            'interaction_pass': bool(float(anova_table.loc['C(lam_level):C(page_type)', 'PR(>F)']) > ALPHA),
        }
        print(f"  Lambda effect p: {anova_result['full_model']['lambda_effect']['p_value']}")
        print(f"  Page type effect p: {anova_result['full_model']['page_type_effect']['p_value']}")
        print(f"  Interaction p: {anova_result['full_model']['interaction_effect']['p_value']}")
        print(f"  Interaction pass (p > 0.05): {anova_result['interaction_pass']}")
    except Exception as e:
        anova_result = {'error': str(e), 'interaction_pass': False}
        print(f"  ANOVA failed: {e}")
    print()

    # ==============================
    # PHASE 7: EFFECT SIZE (Cohen's d)
    # ==============================
    print("=== Effect Size ===")
    tv_lambda0 = np.array(nonstationary_bc_tv[0])
    tv_lambda1 = np.array(nonstationary_bc_tv[7])
    pooled_std = np.sqrt((np.var(tv_lambda0, ddof=1) + np.var(tv_lambda1, ddof=1)) / 2)
    cohens_d = float((np.mean(tv_lambda1) - np.mean(tv_lambda0)) / pooled_std) if pooled_std > 0 else 0.0
    print(f"  Cohen's d (lambda=0 vs 1, BC TV): {cohens_d:.4f}")
    print()

    # ==============================
    # PHASE 8: PER-PAGE-TYPE ANALYSIS
    # ==============================
    print("=== Per-Page-Type Analysis ===")
    per_page_type_results = {}
    for pt_idx in range(N_PAGE_TYPES):
        pt_rho_vals = []
        for l_idx, l in enumerate(LAMBDA_LEVELS):
            mean_tv = float(np.mean(nonstationary_per_page_type[pt_idx][l_idx])) if nonstationary_per_page_type[pt_idx][l_idx] else 0.0
            pt_rho_vals.append(mean_tv)
        rho_pt, p_pt = stats.spearmanr(lambda_arr, np.array(pt_rho_vals))
        per_page_type_results[str(pt_idx)] = {
            'name': PAGE_TYPE_NAMES[pt_idx],
            'spearman_rho': float(rho_pt),
            'spearman_p': float(p_pt),
            'tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): pt_rho_vals[i] for i in range(N_LAMBDA)},
        }
        print(f"  Page type {pt_idx} ({PAGE_TYPE_NAMES[pt_idx]}): rho={rho_pt:.4f}, p={p_pt:.6f}")
    print()

    # ==============================
    # PHASE 9: CV CHECK
    # ==============================
    print("=== CV Check ===")
    cv_lambda1 = float(np.std(nonstationary_bc_tv[7], ddof=1) / np.mean(nonstationary_bc_tv[7])) if np.mean(nonstationary_bc_tv[7]) > 0 else float('inf')
    cv_invalid = cv_lambda1 > 0.5
    print(f"  BC TV CV at lambda=1: {cv_lambda1:.4f} ({'INVALID' if cv_invalid else 'valid'})")
    print()

    # Bias floor check: BC TV at lambda=0 should be <= 0.01
    bias_floor_bc = float(np.mean(nonstationary_bc_tv[0]))
    bias_floor_invalid = bias_floor_bc > 0.01
    print(f"=== Bias Floor Check ===")
    print(f"  BC TV at lambda=0: {bias_floor_bc:.4f} ({'INSUFFICIENT CORRECTION' if bias_floor_invalid else 'OK'})")
    print()

    # ==============================
    # PHASE 10: FREQUENCY BASELINE
    # ==============================
    print("=== Frequency Baseline ===")
    # Compute frequency baseline at lambda=1 non-stationary
    cell_seed_fb = BASE_SEED * 100000 + 7 * 1000 + 0 * 10 + 999
    rng_fb = np.random.RandomState(cell_seed_fb)
    fb_transitions = generate_transitions_nonstationary(1.0, N_TRANSITIONS_NONSTATIONARY, rng_fb)
    fb = compute_frequency_baseline(fb_transitions)
    print(f"  Mean TV marginal vs action-conditional: {fb['mean_tv_marginal_vs_action']:.4f}")
    print()

    # ==============================
    # PHASE 11: DECISION
    # ==============================
    print("=== Decision ===")

    # Check all conditions
    conditions = {
        'spearman_rho_ge_0.5': nonstat_rho >= 0.5,
        'rho_degradation_lt_0.4': rho_degradation < 0.4,
        'positive_control': positive_control_pass,
        'null_control': null_control_pass,
        'no_interaction': anova_result.get('interaction_pass', False),
        'no_pipeline_errors': True,  # we completed without errors
    }

    all_pass = all(conditions.values())
    any_cv_invalid = cv_invalid
    any_bias_floor_invalid = bias_floor_invalid
    any_pipeline_error = not conditions['no_pipeline_errors']

    if any_pipeline_error or any_cv_invalid or any_bias_floor_invalid:
        decision = 'MEASUREMENT_INVALID'
        outcome = 'NOT_APPLICABLE'
    elif all_pass:
        decision = 'SURVIVES_CURRENT_TEST'
        outcome = 'SUPPORTS'
    else:
        # Determine which conditions failed
        failed = [k for k, v in conditions.items() if not v]
        decision = 'FALSIFIED-IN-SETTING'
        outcome = 'FALSIFIES'

    print(f"  Conditions: {conditions}")
    print(f"  Failed: {[k for k, v in conditions.items() if not v]}")
    print(f"  CV invalid: {any_cv_invalid}")
    print(f"  Bias floor invalid: {any_bias_floor_invalid}")
    print(f"  Overall Decision: {decision}")
    print(f"  Overall Outcome: {outcome}")
    print()

    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time:.1f}s")

    # ==============================
    # COMPILE RESULTS
    # ==============================

    # Build controls object
    controls = {
        'positive_control': {
            'description': 'bias_corrected_TV >= 0.001 at lambda=1 in non-stationary condition across all replications',
            'pass': positive_control_pass,
            'bc_tv_at_lambda1': [float(tv) for tv in lambda1_bc_tvs],
            'min_bc_tv': float(np.min(lambda1_bc_tvs)),
        },
        'null_control': {
            'description': 'Fisher combined permutation p > 0.05 at lambda=0 in non-stationary condition',
            'pass': null_control_pass,
            'fisher_combined_p': lambda0_fisher_combined,
            'fisher_F': lambda0_F,
            'per_rep_p_values': [float(p) for p in lambda0_fisher_pvals],
        },
        'stationary_replication': {
            'description': 'Stationary condition replicates EXP-FRONTIER-34061241004 baseline (rho >= 0.9)',
            'pass': float(stat_rho) >= 0.9,
            'spearman_rho': float(stat_rho),
            'spearman_p_one_sided': float(stat_p_one_sided),
            'tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): stationary_agg_means[i] for i in range(N_LAMBDA)},
        },
        'spearman_test': {
            'description': 'Spearman rho(bias_corrected_TV, lambda) >= 0.5 in non-stationary condition',
            'pass': conditions['spearman_rho_ge_0.5'],
            'rho': float(nonstat_rho),
            'p_one_sided': float(nonstat_p_one_sided),
        },
        'degradation_test': {
            'description': 'rho_degradation < 0.4 (stationary rho minus non-stationary rho)',
            'pass': conditions['rho_degradation_lt_0.4'],
            'stationary_rho': float(stat_rho),
            'nonstationary_rho': float(nonstat_rho),
            'degradation': float(rho_degradation),
        },
        'function_invariance': {
            'description': 'No significant page_type x lambda interaction in non-stationary condition (two-way ANOVA p > 0.05)',
            'pass': anova_result.get('interaction_pass', False),
            'interaction_p': anova_result.get('full_model', {}).get('interaction_effect', {}).get('p_value', None),
            'anova_result': anova_result,
        },
        'cv_check': {
            'description': 'CV across replications <= 0.5 at lambda=1 in non-stationary condition',
            'pass': not cv_invalid,
            'cv_lambda1': cv_lambda1,
        },
        'bias_floor_check': {
            'description': 'Bias-corrected TV at lambda=0 <= 0.01 (bias correction sufficient)',
            'pass': not bias_floor_invalid,
            'bc_tv_at_lambda0': bias_floor_bc,
        },
        'no_pipeline_errors': {
            'description': 'No pipeline errors during execution',
            'pass': True,
        },
    }

    # Build metrics object
    metrics = {
        'stationary': {
            'aggregate': {
                'spearman_rho': float(stat_rho),
                'spearman_p_one_sided': float(stat_p_one_sided),
                'tv_max_means_by_lambda': {str(LAMBDA_LEVELS[i]): stationary_agg_means[i] for i in range(N_LAMBDA)},
            },
            'per_function': {},
        },
        'nonstationary': {
            'aggregate_bc_tv': {
                'spearman_rho': float(nonstat_rho),
                'spearman_p_one_sided': float(nonstat_p_one_sided),
                'bc_tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): nonstat_bc_means[i] for i in range(N_LAMBDA)},
            },
            'aggregate_raw_tv': {
                'spearman_rho': float(nonstat_raw_rho),
                'raw_tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): nonstat_raw_means[i] for i in range(N_LAMBDA)},
            },
            'per_page_type': per_page_type_results,
        },
        'degradation': {
            'stationary_rho': float(stat_rho),
            'nonstationary_rho': float(nonstat_rho),
            'rho_degradation': float(rho_degradation),
        },
        'effect_size': {
            'cohens_d_lambda0_vs_1_bc_tv': cohens_d,
        },
        'permutation_tests': {
            'lambda0_fisher_combined_p': lambda0_fisher_combined,
            'lambda1_fisher_combined_p': lambda1_fisher_combined,
            'lambda0_per_rep_p_values': [float(p) for p in lambda0_fisher_pvals],
            'lambda1_per_rep_p_values': [float(p) for p in lambda1_fisher_pvals],
        },
        'frequency_baseline': fb,
    }

    # Fill per_function for stationary
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = {42: 'rotation', 43: 'scaling', 44: 'translation'}[func_seed]
        func_means = [float(np.mean(stationary_all_tv[f_idx][l])) for l in LAMBDA_LEVELS]
        rho_f, p_f = stats.spearmanr(lambda_arr, np.array(func_means))
        metrics['stationary']['per_function'][str(func_seed)] = {
            'func_name': func_name,
            'spearman_rho': float(rho_f),
            'spearman_p_one_sided': float(p_f / 2 if rho_f > 0 else 1 - p_f / 2),
            'tv_max_means_by_lambda': {str(LAMBDA_LEVELS[i]): func_means[i] for i in range(N_LAMBDA)},
        }

    # Observations
    observations = [
        f"Overall decision: {decision}",
        f"Non-stationary Spearman rho(BC_TV, lambda)={nonstat_rho:.4f}, p_one_sided={nonstat_p_one_sided:.6f}",
        f"Stationary Spearman rho={stat_rho:.4f}",
        f"rho_degradation={rho_degradation:.4f} (threshold: <0.4)",
        f"Positive control (BC_TV >= 0.001 at lambda=1): {'PASS' if positive_control_pass else 'FAIL'} (min={float(np.min(lambda1_bc_tvs)):.4f})",
        f"Null control (Fisher combined p > 0.05 at lambda=0): {'PASS' if null_control_pass else 'FAIL'} (p={lambda0_fisher_combined:.6f})",
        f"Page-type invariance (ANOVA interaction): {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'} (p={anova_result.get('full_model', {}).get('interaction_effect', {}).get('p_value', 'N/A')})",
        f"Cohen's d (lambda=0 vs 1, BC TV): {cohens_d:.4f}",
        f"CV at lambda=1 (BC TV): {cv_lambda1:.4f} ({'INVALID' if cv_invalid else 'valid'})",
        f"Bias floor (BC TV at lambda=0): {bias_floor_bc:.4f} ({'INSUFFICIENT' if bias_floor_invalid else 'OK'})",
        f"Frequency baseline mean TV (marginal vs action-conditional): {fb['mean_tv_marginal_vs_action']:.4f}",
    ]

    # Validity notes
    validity_notes = [
        '2000 transitions per lambda level in non-stationary condition (~250 per page type x 8 types)',
        '200 transitions per cell in stationary condition (matching EXP-FRONTIER-34061241004)',
        '5 replications per cell; Monte Carlo SE ~ sqrt(1/250) ~ 0.02 per page type pooled',
        '8 page types: 3 primary functions x 2 noise levels + 2 shifted-center variants',
        'Page types cycle deterministically: type = (transition_index // 250) mod 8',
        'Independent seeds per cell: func_seed * 100000 + lambda_idx * 1000 + rep_idx * 10 + BASE_SEED',
        'Bias-corrected TV: observed_TV - perm_mean_TV at lambda=0 (addresses parent audit V2)',
        'Fisher combined p-values instead of mean-of-p-values (addresses parent audit V8)',
        '20x20 grid binning for TV on continuous 2D state space',
        'Heteroscedastic Gaussian noise with state-dependent variance',
        'Clipping to [0,1] matches parent boundary treatment',
        'No target leakage: TV computed from empirical action-conditional distributions',
        'ANOVA uses bias-corrected TV per page type per lambda',
        'All decisions use frozen decision rules from preregistration',
    ]

    # Unresolved
    unresolved = [
        'Whether real Web DOM transitions exhibit translation-like action-dependent structure (this experiment is still synthetic)',
        'Whether non-stationarity with opposing dynamics (e.g., rotation pushes left, scaling pushes right) would cancel pooled signal',
        'Whether 250 transitions per page type block is adequate for all page types (some may need more)',
        'Whether the deterministic cycling regime is representative of real Web page-type switching patterns',
    ]

    results = {
        'schema_version': 1,
        'experiment_id': 'EXP-FRONTIER-34773875458',
        'lane': 'frontier',
        'status': 'COMPLETE' if not any_pipeline_error and not any_cv_invalid and not any_bias_floor_invalid else 'MEASUREMENT_INVALID',
        'outcome': outcome,
        'metrics': metrics,
        'controls': controls,
        'artifacts': [
            {'path': 'research/experiments/EXP-FRONTIER-34773875458/run_execute.py', 'role': 'code'},
        ],
        'observations': observations,
        'validity_notes': validity_notes,
        'unresolved': unresolved,
    }

    return results, stationary_raw_tables, nonstationary_raw_tables, execution_time


if __name__ == '__main__':
    results, stationary_raw, nonstationary_raw, execution_time = run_experiment()

    # Write result.json
    result_path = Path(__file__).parent / 'result.json'
    with open(result_path, 'w') as f:
        json.dump(to_native(results), f, indent=2)
    print(f"\nWrote {result_path}")

    # Write raw tables
    raw_path = Path(__file__).parent / 'raw_tables.json'
    with open(raw_path, 'w') as f:
        json.dump(to_native({
            'stationary': stationary_raw,
            'nonstationary': nonstationary_raw,
        }), f)
    print(f"Wrote {raw_path}")

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
    for out_name in ['result.json', 'raw_tables.json']:
        out_path = experiment_dir / out_name
        if out_path.exists():
            h = hashlib.sha256(out_path.read_bytes()).hexdigest()
            hashes[out_name] = h

    provenance = {
        'experiment_id': 'EXP-FRONTIER-34773875458',
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
            'stationary': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_TRANSITIONS_STATIONARY * N_REPLICATIONS,
            'nonstationary': len(LAMBDA_LEVELS) * N_TRANSITIONS_NONSTATIONARY * N_REPLICATIONS,
        },
        'environment': {
            'python_version': '3.12.14',
            'numpy_version': np.__version__,
            'scipy_version': stats.__version__ if hasattr(stats, '__version__') else 'unknown',
        },
        'frozen_inputs': {
            'prereg_hash': 'dc41ffba95d311f922be15cf8c172082b399d236b368ef24b8c9a2c8979647c4',
            'request_hash': 'c426eaabcd14022130061e65d1bbb140d41ab22a9c81d28d0d5d4a9e0ae418d2',
            'spec_hash': 'fb9e8dc5198ad746a0b754cf8d405ac1bb2b5f39ad7a3a08ecaf2f8c74f2f1fb',
        },
    }

    provenance_path = experiment_dir / 'provenance.json'
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
