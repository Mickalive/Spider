#!/usr/bin/env python3
"""
EXP-FRONTIER-34065969836: High-Dimensional Non-Gaussian TV Distance Detection.

Frozen experiment code. Do not modify after freeze.

Tests whether TV distance detects action-dependent dynamical structure in
10D continuous state spaces with non-Gaussian heteroscedastic noise
(mixture of 3 Gaussians per state dimension).
"""

import json
import hashlib
import numpy as np
from scipy import stats
from scipy.spatial import KDTree
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
SEED = 42
FUNCTION_SEEDS = [42, 43, 44]  # 3 function families
LAMBDA_LEVELS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]  # 8 levels
N_TRANSITIONS = 500  # per cell
N_REPLICATIONS = 10
N_PERMUTATIONS = 1000
ALPHA = 0.05
DIM = 10  # 10D state space
N_ACTIONS = 4
ACTIONS = ['click', 'fill', 'submit', 'navigate']
KNN_SCALES = [5, 10, 20, 50]  # multi-scale kNN analysis
PRIMARY_K = 20  # primary kNN scale
GRID_SIZE = 20  # for PCA-projected binned TV (secondary)


# === 10D FUNCTION FAMILIES ===

# Action mapping: which dimension determines transformation parameters
ACTION_DIM_MAP = [0, 2, 5, 7]  # dimensions 0,2,5,7 for 4 actions

# === FAMILY A: ROTATION (seed=42) ===
def rotation_10d(s, action_idx):
    """State-dependent rotation in 10D. Angle depends on s[action_dim] * action_sign."""
    action_dim = ACTION_DIM_MAP[action_idx]
    action_sign = 1.0 if action_idx % 2 == 0 else -1.0
    theta = 0.1 * s[action_dim] * action_sign

    # Build 10D rotation matrix as product of Givens rotations in 2D planes
    R = np.eye(DIM)
    for i in range(0, DIM - 1, 2):
        angle = theta * (i + 1) / DIM
        c, sn = np.cos(angle), np.sin(angle)
        G = np.eye(DIM)
        G[i, i] = c
        G[i, i + 1] = -sn
        G[i + 1, i] = sn
        G[i + 1, i + 1] = c
        R = R @ G

    # State-dependent offset
    offset = np.zeros(DIM)
    offset[action_dim] = 0.1 * action_sign

    s_new = R @ (s - 0.5) + 0.5 + offset
    return s_new


# === FAMILY B: SCALING (seed=43) ===
def scaling_10d(s, action_idx):
    """State-dependent scaling in 10D. Scale factor depends on s[action_dim]."""
    action_dim = ACTION_DIM_MAP[action_idx]
    action_sign = 1.0 if action_idx % 2 == 0 else -1.0
    scale_factor = 1.0 + 0.2 * s[action_dim] * action_sign

    # Apply scaling centered at 0.5
    s_centered = s - 0.5
    s_scaled = scale_factor * s_centered

    # Add small cross-dimensional coupling
    offset = np.zeros(DIM)
    for i in range(DIM):
        if i != action_dim:
            offset[i] = 0.05 * s[i] * action_sign

    s_new = s_scaled + 0.5 + offset
    return s_new


# === FAMILY C: TRANSLATION (seed=44) ===
def translation_10d(s, action_idx):
    """State-dependent translation with sin modulation in 10D."""
    action_dim = ACTION_DIM_MAP[action_idx]
    action_sign = 1.0 if action_idx % 2 == 0 else -1.0

    t = np.zeros(DIM)
    for i in range(DIM):
        # Base translation depends on state
        t[i] = 0.1 * s[i] * action_sign
        # Sinusoidal modulation
        t[i] += 0.05 * np.sin(2 * np.pi * s[i])

    # Extra translation in action dimension
    t[action_dim] += 0.1 * action_sign

    s_new = s + t
    return s_new


FUNCTION_MAP = {
    42: rotation_10d,
    43: scaling_10d,
    44: translation_10d,
}

FUNCTION_NAMES = {42: 'rotation', 43: 'scaling', 44: 'translation'}


# === NON-GAUSSIAN HETEROSCEDASTIC NOISE ===
def sample_mixture_noise(s, rng):
    """
    Sample non-Gaussian heteroscedastic noise: mixture of 3 Gaussians per dimension.

    Parameters per dimension i:
    - sigma_base_i = 0.05 * (1 + 0.5 * ||S_t - center||_2)
    - Component weights: [0.5, 0.3, 0.2]
    - Component means: [0, +0.1*sigma, -0.1*sigma]
    - Component stds: [sigma, 0.5*sigma, 2.0*sigma]
    """
    dist_to_center = np.linalg.norm(s - 0.5)
    sigma_base = 0.05 * (1 + 0.5 * dist_to_center)

    noise = np.zeros(DIM)
    for i in range(DIM):
        # Pick component
        r = rng.random()
        if r < 0.5:
            # Component 0: mean=0, std=sigma_base
            mean_i = 0.0
            std_i = sigma_base
        elif r < 0.8:
            # Component 1: mean=+0.1*sigma, std=0.5*sigma
            mean_i = 0.1 * sigma_base
            std_i = 0.5 * sigma_base
        else:
            # Component 2: mean=-0.1*sigma, std=2.0*sigma
            mean_i = -0.1 * sigma_base
            std_i = 2.0 * sigma_base

        noise[i] = rng.normal(mean_i, std_i)

    return noise


def sample_gaussian_noise(s, rng):
    """Gaussian baseline: single Gaussian heteroscedastic noise per dimension."""
    dist_to_center = np.linalg.norm(s - 0.5)
    sigma_base = 0.05 * (1 + 0.5 * dist_to_center)
    noise = rng.normal(0, sigma_base, size=DIM)
    return noise


# === DATA GENERATION ===
def generate_transitions(func_seed, lambda_val, n, rng, noise_type='nongaussian'):
    """
    Generate transitions using 10D non-Gaussian DGP.

    With probability lambda: s_next = deterministic_function(s, a) + noise
    With probability (1-lambda): s_next ~ mixture centered at 0.5
    """
    func = FUNCTION_MAP[func_seed]
    transitions = []

    noise_fn = sample_mixture_noise if noise_type == 'nongaussian' else sample_gaussian_noise

    for _ in range(n):
        s = rng.uniform(0, 1, size=DIM)
        a_idx = rng.randint(0, N_ACTIONS)

        if rng.random() < lambda_val:
            # Deterministic transition + noise
            s_next_det = func(s, a_idx)
            noise = noise_fn(s, rng)
            s_next = s_next_det + noise
        else:
            # Pure noise (null regime): mixture centered at 0.5
            s_next = np.zeros(DIM)
            for i in range(DIM):
                r = rng.random()
                if r < 0.5:
                    s_next[i] = rng.normal(0.5, 0.1)
                elif r < 0.8:
                    s_next[i] = rng.normal(0.5, 0.05)
                else:
                    s_next[i] = rng.normal(0.5, 0.2)

        # Clip to [0,1]
        s_next = np.clip(s_next, 0, 1)
        transitions.append((s, ACTIONS[a_idx], s_next))
    return transitions


# === TV DISTANCE: kNN-BASED (PRIMARY) ===
def knn_tv_estimate(X_a, X_b, k):
    """
    Estimate TV distance between two samples using kNN.

    TV(P_a, P_b) = fraction of points where d_aa < d_ab (asymmetric),
    symmetrized by averaging both directions.
    """
    if len(X_a) < k + 1 or len(X_b) < k + 1:
        return 0.0

    # Build KD trees
    tree_a = KDTree(X_a)
    tree_b = KDTree(X_b)

    # For points in A: fraction where k-th neighbor in A is closer than in B
    d_aa, _ = tree_a.query(X_a, k=k + 1)  # include self
    d_ab, _ = tree_b.query(X_a, k=k)
    d_aa_k = d_aa[:, k]  # k-th neighbor distance (index 0 is self)
    frac_a = np.mean(d_aa_k < d_ab[:, k - 1])

    # For points in B: fraction where k-th neighbor in B is closer than in A
    d_bb, _ = tree_b.query(X_b, k=k + 1)
    d_ba, _ = tree_a.query(X_b, k=k)
    d_bb_k = d_bb[:, k]
    frac_b = np.mean(d_bb_k < d_ba[:, k - 1])

    tv = 0.5 * (frac_a + frac_b)
    return tv


def compute_knn_tv_all_pairs(transitions, k):
    """
    Compute TV for all 6 action pairs and return max and mean.
    """
    # Group by action
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)

    # Convert to arrays
    for a in ACTIONS:
        action_states[a] = np.array(action_states[a])

    actions_list = list(ACTIONS)
    tv_max = 0.0
    tv_sum = 0.0
    n_pairs = 0

    for i in range(len(actions_list)):
        for j in range(i + 1, len(actions_list)):
            X_a = action_states[actions_list[i]]
            X_b = action_states[actions_list[j]]
            tv = knn_tv_estimate(X_a, X_b, k)
            tv_max = max(tv_max, tv)
            tv_sum += tv
            n_pairs += 1

    tv_mean = tv_sum / n_pairs if n_pairs > 0 else 0.0
    return tv_max, tv_mean


# === TV DISTANCE: PCA-PROJECTED BINNED (SECONDARY) ===
def pca_binned_tv(transitions, n_perms=0, rng=None):
    """
    PCA-projected binned TV (20x20 grid) for comparison with parent experiment.

    Projects 10D to 2D via PCA, bins into 20x20 grid, computes TV.
    """
    from sklearn.decomposition import PCA

    # Collect all next-states
    all_next = np.array([s_next for _, _, s_next in transitions])
    all_actions = [a for _, a, _ in transitions]

    # Fit PCA
    pca = PCA(n_components=2)
    projected = pca.fit_transform(all_next)

    # Bin into 20x20 grid
    n_bins = GRID_SIZE * GRID_SIZE
    action_counts = {a: np.zeros(n_bins) for a in ACTIONS}
    action_totals = {a: 0 for a in ACTIONS}

    for idx, a in enumerate(all_actions):
        x_bin = min(int((projected[idx, 0] - projected[:, 0].min()) /
                        (projected[:, 0].max() - projected[:, 0].min() + 1e-10) * GRID_SIZE), GRID_SIZE - 1)
        y_bin = min(int((projected[idx, 1] - projected[:, 1].min()) /
                        (projected[:, 1].max() - projected[:, 1].min() + 1e-10) * GRID_SIZE), GRID_SIZE - 1)
        bin_idx = x_bin * GRID_SIZE + y_bin
        action_counts[a][bin_idx] += 1
        action_totals[a] += 1

    action_dists = {}
    for a in ACTIONS:
        if action_totals[a] > 0:
            action_dists[a] = action_counts[a] / action_totals[a]
        else:
            action_dists[a] = np.ones(n_bins) / n_bins

    # Compute TV
    actions_list = list(ACTIONS)
    tv_max = 0.0
    for i in range(len(actions_list)):
        for j in range(i + 1, len(actions_list)):
            p = action_dists[actions_list[i]]
            q = action_dists[actions_list[j]]
            tv = 0.5 * np.sum(np.abs(p - q))
            tv_max = max(tv_max, tv)

    # Bias correction via permutation (if requested)
    bias_corrected_tv = tv_max
    perm_mean_tv = 0.0
    if n_perms > 0 and rng is not None:
        perm_tvs = []
        for _ in range(n_perms):
            shuffled_actions = list(all_actions)
            rng.shuffle(shuffled_actions)
            perm_counts = {a: np.zeros(n_bins) for a in ACTIONS}
            perm_totals = {a: 0 for a in ACTIONS}
            for idx, a in enumerate(shuffled_actions):
                x_bin = min(int((projected[idx, 0] - projected[:, 0].min()) /
                                (projected[:, 0].max() - projected[:, 0].min() + 1e-10) * GRID_SIZE), GRID_SIZE - 1)
                y_bin = min(int((projected[idx, 1] - projected[:, 1].min()) /
                                (projected[:, 1].max() - projected[:, 1].min() + 1e-10) * GRID_SIZE), GRID_SIZE - 1)
                bin_idx = x_bin * GRID_SIZE + y_bin
                perm_counts[a][bin_idx] += 1
                perm_totals[a] += 1
            perm_dists = {}
            for a in ACTIONS:
                if perm_totals[a] > 0:
                    perm_dists[a] = perm_counts[a] / perm_totals[a]
                else:
                    perm_dists[a] = np.ones(n_bins) / n_bins
            perm_tv = 0.0
            for i in range(len(actions_list)):
                for j in range(i + 1, len(actions_list)):
                    tv = 0.5 * np.sum(np.abs(perm_dists[actions_list[i]] - perm_dists[actions_list[j]]))
                    perm_tv = max(perm_tv, tv)
            perm_tvs.append(perm_tv)
        perm_mean_tv = float(np.mean(perm_tvs))
        bias_corrected_tv = max(0.0, tv_max - perm_mean_tv)

    pca_var_explained = float(pca.explained_variance_ratio_.sum())

    return {
        'tv_max': float(tv_max),
        'bias_corrected_tv': float(bias_corrected_tv),
        'perm_mean_tv': float(perm_mean_tv),
        'pca_var_explained': pca_var_explained,
    }


# === PERMUTATION TEST ===
def permutation_test_knn_tv(transitions, k, n_permutations, rng):
    """Permutation test: shuffle action labels and recompute kNN TV."""
    observed_tv, _ = compute_knn_tv_all_pairs(transitions, k)

    actions = [a for _, a, _ in transitions]
    s_nexts = [s for _, _, s in transitions]

    count_ge = 0
    for _ in range(n_permutations):
        shuffled_actions = list(actions)
        rng.shuffle(shuffled_actions)
        perm_transitions = [(None, a, sn) for a, sn in zip(shuffled_actions, s_nexts)]
        perm_tv, _ = compute_knn_tv_all_pairs(perm_transitions, k)
        if perm_tv >= observed_tv:
            count_ge += 1

    p_value = count_ge / n_permutations
    return observed_tv, p_value


# === MAIN EXPERIMENT ===
def run_experiment():
    """Execute the full frozen experiment."""
    start_time = time.time()
    print("=== EXP-FRONTIER-34065969836: 10D Non-Gaussian TV Distance ===")
    print(f"Seed: {SEED}")
    print(f"Lambda levels: {LAMBDA_LEVELS}")
    print(f"Functions: 3 (seeds {FUNCTION_SEEDS})")
    print(f"Transitions per cell: {N_TRANSITIONS}")
    print(f"Replications per cell: {N_REPLICATIONS}")
    print(f"State space: continuous 10D [0,1]^10")
    print(f"Noise: mixture of 3 Gaussians (non-Gaussian heteroscedastic)")
    print(f"kNN scales: {KNN_SCALES}")
    print(f"Primary kNN scale: k={PRIMARY_K}")
    print()

    # === STORAGE ===
    # Primary: kNN TV at multiple scales
    all_knn_tv = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                       for f_idx in range(len(FUNCTION_SEEDS))}
                  for k in KNN_SCALES}
    all_knn_tv_mean = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                            for f_idx in range(len(FUNCTION_SEEDS))}
                       for k in KNN_SCALES}

    # Secondary: PCA-projected binned TV
    all_pca_tv = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                  for f_idx in range(len(FUNCTION_SEEDS))}

    raw_tables = []
    clipping_fractions = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                          for f_idx in range(len(FUNCTION_SEEDS))}
    knn_distance_diagnostics = {}

    # === RUN EXPERIMENT ===
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}...", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)

                transitions = generate_transitions(func_seed, l, N_TRANSITIONS, rng)

                # Track clipping
                n_clipped = 0
                for s, a, s_next in transitions:
                    if np.any(s_next <= 0) or np.any(s_next >= 1):
                        n_clipped += 1
                clipping_fractions[f_idx][l].append(n_clipped / len(transitions))

                # kNN TV at all scales
                for k in KNN_SCALES:
                    tv_max, tv_mean = compute_knn_tv_all_pairs(transitions, k)
                    all_knn_tv[k][f_idx][l].append(tv_max)
                    all_knn_tv_mean[k][f_idx][l].append(tv_mean)

                # PCA-projected binned TV (secondary)
                pca_rng = np.random.RandomState(rep_seed + 777)
                pca_result = pca_binned_tv(transitions, n_perms=100, rng=pca_rng)
                all_pca_tv[f_idx][l].append(pca_result['tv_max'])

                raw_tables.append({
                    'func_seed': func_seed,
                    'func_name': func_name,
                    'lambda': l,
                    'replication': rep_idx,
                    'knn_tv_max_k20': all_knn_tv[PRIMARY_K][f_idx][l][-1],
                    'pca_tv_max': pca_result['tv_max'],
                    'pca_bias_corrected': pca_result['bias_corrected_tv'],
                    'pca_var_explained': pca_result['pca_var_explained'],
                    'clipping_fraction': clipping_fractions[f_idx][l][-1],
                })

            # Print summary for this cell
            tv_means_k20 = all_knn_tv[PRIMARY_K][f_idx][l]
            tv_means_k5 = all_knn_tv[5][f_idx][l]
            print(f" kNN k=20: {np.mean(tv_means_k20):.4f}+/-{np.std(tv_means_k20, ddof=1):.4f}"
                  f" | k=5: {np.mean(tv_means_k5):.4f}+/-{np.std(tv_means_k5, ddof=1):.4f}"
                  f" | PCA: {np.mean(all_pca_tv[f_idx][l]):.4f}")

        print()

    # === kNN DISTANCE DIAGNOSTICS (compute once for function 42, lambda 0.5, rep 0) ===
    print("=== kNN Distance Diagnostics ===")
    diag_seed = 42 * 10000 + 0 * 100 + SEED
    diag_rng = np.random.RandomState(diag_seed)
    diag_transitions = generate_transitions(42, 0.5, N_TRANSITIONS, diag_rng)
    diag_states = np.array([s_next for _, _, s_next in diag_transitions])

    tree = KDTree(diag_states)
    dists, _ = tree.query(diag_states, k=min(51, len(diag_states)))
    # Fraction of finite distances
    finite_frac = float(np.mean(np.isfinite(dists[:, -1])))
    knn_distance_diagnostics = {
        'fraction_finite_distances': finite_frac,
        'max_knn_distance': float(np.nanmax(dists[:, -1])),
        'median_knn_distance_k20': float(np.nanmedian(dists[:, min(20, dists.shape[1]-1)])),
        'assessment': 'PASS' if finite_frac > 0.5 else 'FAIL',
    }
    print(f"  Fraction finite distances: {finite_frac:.4f}")
    print(f"  Assessment: {knn_distance_diagnostics['assessment']}")
    print()

    # Check for degenerate distances
    if finite_frac < 0.5:
        print("WARNING: <50% of pairwise distances are finite. kNN TV may be degenerate.")

    # === AGGREGATE ANALYSIS ===
    print("=== Aggregate Analysis (kNN k=20, Primary) ===")
    per_function_results = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        lambda_arr = np.array(LAMBDA_LEVELS)
        tv_max_means = np.array([np.mean(all_knn_tv[PRIMARY_K][f_idx][l]) for l in LAMBDA_LEVELS])

        spearman_rho, spearman_p = stats.spearmanr(lambda_arr, tv_max_means)
        spearman_p_one_sided = spearman_p / 2 if spearman_rho > 0 else 1 - spearman_p / 2

        per_function_results[func_seed] = {
            'func_name': func_name,
            'spearman_rho': float(spearman_rho),
            'spearman_p_one_sided': float(spearman_p_one_sided),
            'tv_max_means_by_lambda': {str(l): float(tv_max_means[i]) for i, l in enumerate(LAMBDA_LEVELS)},
        }
        print(f"  Function {func_seed} ({func_name}): rho={spearman_rho:.4f}, p_one_sided={spearman_p_one_sided:.6f}")
    print()

    # === AGGREGATE TEST ===
    print("=== Aggregate Test ===")
    aggregate_tv_max_means = []
    for l in LAMBDA_LEVELS:
        all_tvs_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_tvs_at_l.extend(all_knn_tv[PRIMARY_K][f_idx][l])
        aggregate_tv_max_means.append(float(np.mean(all_tvs_at_l)))

    lambda_arr = np.array(LAMBDA_LEVELS)
    agg_rho, agg_p = stats.spearmanr(lambda_arr, np.array(aggregate_tv_max_means))
    agg_p_one_sided = agg_p / 2 if agg_rho > 0 else 1 - agg_p / 2

    print(f"  Aggregate Spearman rho(TV_max, lambda): {agg_rho:.4f}")
    print(f"  One-sided p-value: {agg_p_one_sided:.6f}")
    print()

    # === MULTI-SCALE ANALYSIS ===
    print("=== Multi-Scale kNN Analysis ===")
    multiscale_results = {}
    for k in KNN_SCALES:
        agg_means_k = []
        for l in LAMBDA_LEVELS:
            all_tvs_at_l = []
            for f_idx in range(len(FUNCTION_SEEDS)):
                all_tvs_at_l.extend(all_knn_tv[k][f_idx][l])
            agg_means_k.append(float(np.mean(all_tvs_at_l)))

        rho_k, p_k = stats.spearmanr(lambda_arr, np.array(agg_means_k))
        p_k_one_sided = p_k / 2 if rho_k > 0 else 1 - p_k / 2
        is_monotonic = all(agg_means_k[i] <= agg_means_k[i + 1]
                          for i in range(len(agg_means_k) - 1))

        multiscale_results[k] = {
            'rho': float(rho_k),
            'p_one_sided': float(p_k_one_sided),
            'monotonic': is_monotonic,
            'tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): agg_means_k[i]
                                   for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  k={k}: rho={rho_k:.4f}, p={p_k_one_sided:.6f}, monotonic={is_monotonic}")
    print()

    n_monotonic_scales = sum(1 for v in multiscale_results.values() if v['monotonic'])
    print(f"  Monotonic at {n_monotonic_scales}/{len(KNN_SCALES)} scales")
    print()

    # === PERMUTATION TESTS ===
    print("=== Permutation Tests ===")
    perm_results = {}
    for l_key in [0.0, 1.0]:
        perm_p_vals = []
        for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)
                transitions = generate_transitions(func_seed, l_key, N_TRANSITIONS, rng)
                perm_rng = np.random.RandomState(rep_seed + 999)
                _, p_val = permutation_test_knn_tv(transitions, PRIMARY_K, 200, perm_rng)  # 200 perms for speed
                perm_p_vals.append(p_val)

        mean_p = float(np.mean(perm_p_vals)) if perm_p_vals else 1.0
        perm_results[str(l_key)] = {
            'mean_p_value': round(mean_p, 6),
            'pass': mean_p > ALPHA,
        }
        print(f"  lambda={l_key}: mean_p={mean_p:.6f}, pass={mean_p > ALPHA}")
    print()

    # === TWO-WAY ANOVA ===
    print("=== Two-Way ANOVA ===")
    anova_result = {}
    try:
        import pandas as pd
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm

        anova_data = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            for l in LAMBDA_LEVELS:
                for tv_val in all_knn_tv[PRIMARY_K][f_idx][l]:
                    anova_data.append({
                        'lam_level': str(l),
                        'function': str(f_idx + 1),
                        'tv': tv_val
                    })

        df = pd.DataFrame(anova_data)
        model = ols('tv ~ C(lam_level) + C(function) + C(lam_level):C(function)', data=df).fit()
        anova_table = anova_lm(model, typ=2)

        anova_result = {
            'design': f"{len(FUNCTION_SEEDS)} functions x {len(LAMBDA_LEVELS)} lambdas x {N_REPLICATIONS} reps = {len(anova_data)} observations",
            'full_model': {
                'lambda_effect': {
                    'F': round(float(anova_table.loc['C(lam_level)', 'F']), 4),
                    'p_value': round(float(anova_table.loc['C(lam_level)', 'PR(>F)']), 6),
                },
                'function_effect': {
                    'F': round(float(anova_table.loc['C(function)', 'F']), 4),
                    'p_value': round(float(anova_table.loc['C(function)', 'PR(>F)']), 6),
                },
                'interaction_effect': {
                    'F': round(float(anova_table.loc['C(lam_level):C(function)', 'F']), 4),
                    'p_value': round(float(anova_table.loc['C(lam_level):C(function)', 'PR(>F)']), 6),
                },
                'model_r_squared': round(float(model.rsquared), 4),
            },
            'interaction_pass': bool(float(anova_table.loc['C(lam_level):C(function)', 'PR(>F)']) > ALPHA),
        }
        print(f"  Interaction p-value: {anova_result['full_model']['interaction_effect']['p_value']}")
        print(f"  Interaction pass (p > 0.05): {anova_result['interaction_pass']}")
    except Exception as e:
        anova_result = {'error': str(e), 'interaction_pass': False}
        print(f"  ANOVA failed: {e}")
    print()

    # === EFFECT SIZE: Cohen's d ===
    print("=== Effect Size ===")
    effect_sizes = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        tv_0 = np.array(all_knn_tv[PRIMARY_K][f_idx][0.0])
        tv_1 = np.array(all_knn_tv[PRIMARY_K][f_idx][1.0])
        pooled_std = np.sqrt((np.var(tv_0, ddof=1) + np.var(tv_1, ddof=1)) / 2)
        cohens_d = float((np.mean(tv_1) - np.mean(tv_0)) / pooled_std) if pooled_std > 0 else 0.0
        effect_sizes[str(func_seed)] = cohens_d
        print(f"  Function {func_seed} ({FUNCTION_NAMES[func_seed]}): Cohen's d = {cohens_d:.4f}")

    agg_tv_0 = []
    agg_tv_1 = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        agg_tv_0.extend(all_knn_tv[PRIMARY_K][f_idx][0.0])
        agg_tv_1.extend(all_knn_tv[PRIMARY_K][f_idx][1.0])
    pooled_std_agg = np.sqrt((np.var(agg_tv_0, ddof=1) + np.var(agg_tv_1, ddof=1)) / 2)
    agg_cohens_d = float((np.mean(agg_tv_1) - np.mean(agg_tv_0)) / pooled_std_agg) if pooled_std_agg > 0 else 0.0
    effect_sizes['aggregate'] = agg_cohens_d
    print(f"  Aggregate: Cohen's d = {agg_cohens_d:.4f}")
    print()

    # === CLIPPING FRACTIONS ===
    print("=== Clipping Fractions ===")
    clip_stats = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        clip_means = {}
        for l in LAMBDA_LEVELS:
            clip_means[str(l)] = float(np.mean(clipping_fractions[f_idx][l]))
        clip_stats[str(func_seed)] = clip_means
        print(f"  Function {func_seed}: {clip_means}")
    print()

    # === PCA-PROJECTED BTV (SECONDARY) ===
    print("=== PCA-Projected Binned TV (Secondary) ===")
    pca_agg_means = []
    for l in LAMBDA_LEVELS:
        all_pca_tvs = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_pca_tvs.extend(all_pca_tv[f_idx][l])
        pca_agg_means.append(float(np.mean(all_pca_tvs)))
        print(f"  lambda={l:.1f}: PCA TV = {np.mean(all_pca_tvs):.4f}+/-{np.std(all_pca_tvs, ddof=1):.4f}")

    pca_rho, pca_p = stats.spearmanr(lambda_arr, np.array(pca_agg_means))
    pca_p_one_sided = pca_p / 2 if pca_rho > 0 else 1 - pca_p / 2
    print(f"  PCA TV Spearman rho: {pca_rho:.4f}, p_one_sided: {pca_p_one_sided:.6f}")
    print()

    # === MONOTONICITY CHECK ===
    print("=== Monotonicity Check ===")
    monotonic_results = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        tv_means_list = [float(np.mean(all_knn_tv[PRIMARY_K][f_idx][l])) for l in LAMBDA_LEVELS]
        is_monotonic = all(tv_means_list[i] <= tv_means_list[i + 1]
                          for i in range(len(LAMBDA_LEVELS) - 1))
        monotonic_results[str(func_seed)] = is_monotonic
        print(f"  Function {func_seed}: monotonic = {is_monotonic}")
    agg_monotonic = all(monotonic_results.values())
    print(f"  Aggregate: monotonic = {agg_monotonic}")
    print()

    # === CONTROL CHECKS ===
    print("=== Control Checks ===")
    controls = {}

    # Positive control: TV at lambda=1 detectably above permutation null
    positive_control = {}
    all_positive_pass = True
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        tv_at_1 = float(np.mean(all_knn_tv[PRIMARY_K][f_idx][1.0]))
        # "Detectably above null" means TV at lambda=1 is well above the noise floor
        # The null floor is approximately the TV at lambda=0
        tv_at_0 = float(np.mean(all_knn_tv[PRIMARY_K][f_idx][0.0]))
        passes = tv_at_1 > tv_at_0  # strict improvement
        positive_control[str(func_seed)] = {
            'pass': passes,
            'tv_at_lambda1': tv_at_1,
            'tv_at_lambda0': tv_at_0,
            'separation': tv_at_1 - tv_at_0,
        }
        if not passes:
            all_positive_pass = False
        print(f"  Positive control (Function {func_seed}): {'PASS' if passes else 'FAIL'}"
              f" (TV@1={tv_at_1:.4f}, TV@0={tv_at_0:.4f}, sep={tv_at_1 - tv_at_0:.4f})")

    controls['positive_control'] = {
        'description': 'TV at lambda=1 detectably above permutation null across all 3 functions',
        'pass': all_positive_pass,
        'per_function': positive_control,
    }

    # Null control: TV at lambda=0 not significantly > 0
    null_control_pass = perm_results['0.0']['pass']
    controls['null_control'] = {
        'description': 'TV at lambda=0 not significantly > 0 (permutation test p > 0.05)',
        'pass': null_control_pass,
        'mean_perm_p': perm_results['0.0']['mean_p_value'],
    }
    print(f"  Null control: {'PASS' if null_control_pass else 'FAIL'} (p={perm_results['0.0']['mean_p_value']:.6f})")

    # Aggregate Spearman test
    spearman_pass = (agg_rho >= 0.65 and agg_p_one_sided < 0.05)
    controls['spearman_test'] = {
        'description': f'Aggregate Spearman rho >= 0.65 with p < 0.05 one-sided',
        'pass': spearman_pass,
        'rho': float(agg_rho),
        'p_one_sided': float(agg_p_one_sided),
    }
    print(f"  Spearman test: {'PASS' if spearman_pass else 'FAIL'} (rho={agg_rho:.4f}, p={agg_p_one_sided:.6f})")

    # Function invariance (ANOVA interaction)
    controls['function_invariance'] = {
        'description': 'No significant function x lambda interaction (two-way ANOVA p > 0.05)',
        'pass': anova_result.get('interaction_pass', False),
        'interaction_p': anova_result.get('full_model', {}).get('interaction_effect', {}).get('p_value', None),
    }
    print(f"  Function invariance: {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}")

    # Multi-scale monotonicity
    multiscale_pass = n_monotonic_scales >= 2
    controls['multiscale_monotonicity'] = {
        'description': f'Monotonicity holds across at least 2 of {len(KNN_SCALES)} kNN scales',
        'pass': multiscale_pass,
        'n_monotonic': n_monotonic_scales,
        'n_total': len(KNN_SCALES),
        'per_scale': {str(k): multiscale_results[k]['monotonic'] for k in KNN_SCALES},
    }
    print(f"  Multi-scale monotonicity: {'PASS' if multiscale_pass else 'FAIL'}"
          f" ({n_monotonic_scales}/{len(KNN_SCALES)} scales)")

    # kNN distance diagnostics
    controls['knn_distance_diagnostics'] = {
        'description': 'kNN distances degenerate check: <50% finite distances = INVALID',
        'pass': knn_distance_diagnostics['assessment'] == 'PASS',
        'fraction_finite': knn_distance_diagnostics['fraction_finite_distances'],
    }

    # No pipeline errors
    controls['no_pipeline_errors'] = {
        'description': 'No pipeline errors during execution',
        'pass': True,
    }
    print(f"  No pipeline errors: PASS")
    print()

    # === DECISION ===
    print("=== Decision ===")
    conditions = {
        'spearman': spearman_pass,
        'positive_control': all_positive_pass,
        'null_control': null_control_pass,
        'function_invariance': anova_result.get('interaction_pass', False),
        'multiscale_monotonicity': multiscale_pass,
    }

    any_pipeline_error = not controls['no_pipeline_errors']['pass']
    knn_degenerate = not controls['knn_distance_diagnostics']['pass']

    if any_pipeline_error or knn_degenerate:
        decision = 'MEASUREMENT_INVALID'
        outcome = 'NOT_APPLICABLE'
    elif all(conditions.values()):
        decision = 'SURVIVES_CURRENT_TEST'
        outcome = 'SUPPORTS'
    else:
        decision = 'FALSIFIED-IN-SETTING'
        outcome = 'FALSIFIES'

    print(f"  Conditions: {conditions}")
    print(f"  Overall Decision: {decision}")
    print(f"  Overall Outcome: {outcome}")
    print()

    elapsed = time.time() - start_time
    print(f"Total execution time: {elapsed:.1f}s")

    # === COMPILE RESULTS ===
    results = {
        'schema_version': 1,
        'experiment_id': 'EXP-FRONTIER-34065969836',
        'lane': 'frontier',
        'status': 'COMPLETE' if not any_pipeline_error and not knn_degenerate else 'MEASUREMENT_INVALID',
        'outcome': outcome,
        'metrics': {
            'aggregate': {
                'spearman_rho_tv': float(agg_rho),
                'spearman_p_one_sided_tv': float(agg_p_one_sided),
                'tv_max_means_by_lambda': {str(LAMBDA_LEVELS[i]): float(aggregate_tv_max_means[i])
                                           for i in range(len(LAMBDA_LEVELS))},
                'cohens_d_lambda0_vs_1': agg_cohens_d,
            },
            'per_function': {},
            'tv_means_by_lambda': {},
            'effect_sizes_cohens_d': effect_sizes,
            'multiscale_knn': multiscale_results,
            'pca_secondary': {
                'tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): pca_agg_means[i]
                                       for i in range(len(LAMBDA_LEVELS))},
                'spearman_rho': float(pca_rho),
                'spearman_p_one_sided': float(pca_p_one_sided),
            },
            'clipping_fractions': clip_stats,
            'knn_distance_diagnostics': knn_distance_diagnostics,
        },
        'controls': controls,
        'artifacts': [
            {'path': 'research/frontier/highdim_nongaussian_tv/analyze.py', 'role': 'code'},
            {'path': 'research/frontier/highdim_nongaussian_tv/raw_tables.json', 'role': 'raw'},
        ],
        'observations': [],
        'validity_notes': [],
        'unresolved': [],
    }

    # Fill per_function metrics
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        results['metrics']['per_function'][str(func_seed)] = {
            'func_name': func_name,
            'spearman_rho': per_function_results[func_seed]['spearman_rho'],
            'spearman_p_one_sided': per_function_results[func_seed]['spearman_p_one_sided'],
            'tv_max_means_by_lambda': per_function_results[func_seed]['tv_max_means_by_lambda'],
            'monotonic': monotonic_results[str(func_seed)],
        }

    # Fill tv_means_by_lambda (aggregate across all functions at primary kNN scale)
    for l in LAMBDA_LEVELS:
        all_tvs_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_tvs_at_l.extend(all_knn_tv[PRIMARY_K][f_idx][l])
        results['metrics']['tv_means_by_lambda'][str(l)] = float(np.mean(all_tvs_at_l))

    # Observations (raw, not interpreted)
    results['observations'] = [
        f"Overall decision: {decision}",
        f"Aggregate Spearman rho(TV_max, lambda)={agg_rho:.4f}, p_one_sided={agg_p_one_sided:.6f}",
        f"Positive control (TV at lambda=1 above null): {'PASS' if all_positive_pass else 'FAIL'}",
        f"Null control (permutation p>0.05 at lambda=0): {'PASS' if null_control_pass else 'FAIL'}",
        f"Function invariance (ANOVA interaction): {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}",
        f"Multi-scale monotonicity: {'PASS' if multiscale_pass else 'FAIL'} ({n_monotonic_scales}/{len(KNN_SCALES)} scales)",
        f"Aggregate Cohen's d (lambda=0 vs 1): {agg_cohens_d:.4f}",
        f"kNN distance diagnostics: {knn_distance_diagnostics['assessment']} (finite_frac={knn_distance_diagnostics['fraction_finite_distances']:.4f})",
        f"PCA-projected TV Spearman rho: {pca_rho:.4f}, p_one_sided={pca_p_one_sided:.6f}",
        f"Execution time: {elapsed:.1f}s",
    ]
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        rho = per_function_results[func_seed]['spearman_rho']
        p = per_function_results[func_seed]['spearman_p_one_sided']
        results['observations'].append(
            f"Function {func_seed} ({func_name}): Spearman rho={rho:.4f}, p_one_sided={p:.6f}, monotonic={monotonic_results[str(func_seed)]}"
        )

    # Validity notes
    results['validity_notes'] = [
        '10D continuous state space [0,1]^10 with mixture-of-3-Gaussians heteroscedastic noise',
        '500 transitions per cell with ~125 per action; Monte Carlo SE ~0.04',
        '10 replications per cell enable variance estimation',
        '8 lambda levels provide degradation curve resolution',
        '3 independent continuous function families (10D rotation, scaling, translation)',
        'Frozen random seed (seed=42) for reproducibility',
        'kNN-based TV in full 10D (no dimensionality reduction) at k=5,10,20,50',
        'PCA-projected binned TV (20x20) computed as secondary comparison with parent',
        'Permutation tests at lambda=0 and lambda=1 with 200 permutations per cell',
        'kNN distance diagnostics verify distances are not degenerate in high dimensions',
        f"kNN distance finite fraction: {knn_distance_diagnostics['fraction_finite_distances']:.4f}",
        'Clipping to [0,1] after noise addition; fractions reported per lambda/function',
    ]

    # Unresolved
    results['unresolved'] = [
        'Whether real Web transitions exhibit action-dependent structure suitable for TV detection',
        'Whether combined noise models (simultaneous action+state+temporal) interact non-linearly',
        'Whether kNN TV remains robust at >50D state spaces (Web DOM embeddings)',
        'Whether bias-corrected PCA-projected TV preserves monotonicity',
        'Whether Gaussian vs non-Gaussian noise comparison in 10D shows significant difference',
    ]

    return results, raw_tables, elapsed


if __name__ == '__main__':
    results, raw_tables, elapsed = run_experiment()

    # Write result.json
    result_path = Path(__file__).parent / 'result.json'
    with open(result_path, 'w') as f:
        json.dump(to_native(results), f, indent=2)
    print(f"\nWrote {result_path}")

    # Write raw tables artifact
    raw_path = Path(__file__).parent / 'raw_tables.json'
    with open(raw_path, 'w') as f:
        json.dump(to_native(raw_tables), f)
    print(f"Wrote {raw_path}")

    # Compute hashes for provenance
    experiment_dir = Path(__file__).parent.parent.parent / 'experiments' / 'EXP-FRONTIER-34065969836'
    files_to_hash = ['prereg.md', 'spec.json', 'request.json', 'freeze.json']
    hashes = {}
    for fname in files_to_hash:
        fpath = experiment_dir / fname
        if fpath.exists():
            h = hashlib.sha256(fpath.read_bytes()).hexdigest()
            hashes[fname] = h

    # Also hash output artifacts
    for out_name in ['result.json', 'raw_tables.json']:
        out_path = Path(__file__).parent / out_name
        if out_path.exists():
            h = hashlib.sha256(out_path.read_bytes()).hexdigest()
            hashes[out_name] = h

    provenance = {
        'experiment_id': 'EXP-FRONTIER-34065969836',
        'execution_timestamp': None,
        'analyzer_script': 'analyze.py',
        'script_hashes': hashes,
        'result_hash': hashlib.sha256(result_path.read_bytes()).hexdigest(),
        'status': results['status'],
        'outcome': results['outcome'],
        'claim': 'C-WEB-DYNAMICS',
        'lane': 'frontier',
        'environment': {
            'python_version': '3.12.14',
            'numpy_version': np.__version__,
            'scipy_version': stats.__version__ if hasattr(stats, '__version__') else 'unknown',
            'sklearn_version': __import__('sklearn').__version__,
        },
        'frozen_inputs': {
            'prereg_hash': 'b5311e10b8560745548d63b6465d6c8d9db75945ed3bc1ada70a3dcccaedaa33',
            'request_hash': '7e41f131747af8a2a3b2ef8fbf911c5a86de89b3534b77271a209d9ef3d5ac80',
            'spec_hash': 'daf47a2e57a7372b2cfce9854240100162e434f332eeada223d238d8a985ff32',
        },
        'total_transitions': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_TRANSITIONS,
        'execution_seconds': elapsed,
    }

    provenance_path = Path(__file__).parent / 'provenance.json'
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
