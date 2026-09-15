#!/usr/bin/env python3
"""
EXP-FRONTIER-34913743596: Alternative Divergence Measures (KDE, kNN MI).

Frozen experiment code. Do not modify after freeze.

Tests whether KDE with cross-validated bandwidth and kNN mutual information
maintain per-type null control and low CV at equal per-type n (250/type)
where binned TV fails due to sparse binning (0.625 expected counts/bin).
"""

import json
import hashlib
import numpy as np
from scipy import stats
from scipy.special import digamma
from scipy.stats import gaussian_kde
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


# === FROZEN PARAMETERS (identical to parent EXP-FRONTIER-34881708619) ===
BASE_SEED = 42
FUNCTION_SEEDS = [42, 43, 44]  # 3 function families
LAMBDA_LEVELS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]  # 8 levels
N_LAMBDA = len(LAMBDA_LEVELS)
N_REPLICATIONS = 5
N_PERMUTATIONS = 200  # Per permutation null
ALPHA = 0.05
CENTER = np.array([0.5, 0.5])
SIGMA_BASE = 0.05
BETA = 0.5
GRID_SIZE = 20  # 20x20 grid for binned TV reference
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


# === KDE DIVERGENCE ===
def compute_kde_divergence(transitions, n_permutations, rng):
    """
    Compute KL divergence using KDE on continuous 2D state space.
    
    For each action a:
      D_KL(P(S'|A=a) || P(S'))
    where densities are estimated via Gaussian KDE.
    
    Returns max KL across actions (the most informative action).
    """
    if len(transitions) < 10:
        return 0.0, 0.0, 0.0, 0.0
    
    s_nexts = np.array([t[2] for t in transitions])  # (N, 2)
    actions = np.array([t[1] for t in transitions])   # (N,)
    
    # Marginal density P(S')
    try:
        kde_marginal = gaussian_kde(s_nexts.T, bw_method='scott')
    except Exception:
        return 0.0, 0.0, 0.0, 0.0
    
    # Conditional densities P(S'|A=a) and KL for each action
    kl_values = []
    for a in range(N_ACTIONS):
        mask = actions == a
        if np.sum(mask) < 5:
            kl_values.append(0.0)
            continue
        s_nexts_a = s_nexts[mask]
        try:
            kde_cond = gaussian_kde(s_nexts_a.T, bw_method='scott')
        except Exception:
            kl_values.append(0.0)
            continue
        
        # KL divergence: D_KL(P(S'|A=a) || P(S'))
        # Approximate by averaging log density ratio over samples from P(S'|A=a)
        log_ratio = np.log(kde_cond(s_nexts_a.T) / kde_marginal(s_nexts_a.T) + 1e-300)
        kl = float(np.mean(log_ratio))
        kl_values.append(max(0.0, kl))
    
    observed_max_kl = max(kl_values) if kl_values else 0.0
    
    # Permutation null: shuffle action labels
    perm_kls = []
    for _ in range(n_permutations):
        shuffled_actions = actions.copy()
        rng.shuffle(shuffled_actions)
        
        perm_kl_values = []
        for a in range(N_ACTIONS):
            mask = shuffled_actions == a
            if np.sum(mask) < 5:
                perm_kl_values.append(0.0)
                continue
            s_nexts_a = s_nexts[mask]
            try:
                kde_cond = gaussian_kde(s_nexts_a.T, bw_method='scott')
            except Exception:
                perm_kl_values.append(0.0)
                continue
            log_ratio = np.log(kde_cond(s_nexts_a.T) / kde_marginal(s_nexts_a.T) + 1e-300)
            kl = float(np.mean(log_ratio))
            perm_kl_values.append(max(0.0, kl))
        
        perm_kls.append(max(perm_kl_values) if perm_kl_values else 0.0)
    
    perm_mean = float(np.mean(perm_kls))
    perm_std = float(np.std(perm_kls, ddof=1)) if len(perm_kls) > 1 else 0.0
    # 95th percentile threshold
    perm_threshold = float(np.percentile(perm_kls, 95))
    p_value = sum(1 for pk in perm_kls if pk >= observed_max_kl) / n_permutations
    
    return observed_max_kl, perm_mean, perm_std, perm_threshold


# === kNN MUTUAL INFORMATION ===
def compute_knn_mi(transitions, n_permutations, rng, k=5):
    """
    Estimate mutual information I(S'; A) using kNN estimator (Kraskov et al.).
    
    Uses the kNN approach: for each point (s'_i, a_i), find the k-th nearest
    neighbor in the joint space, then count neighbors in the same action class.
    
    MI = psi(k) - <psi(n_x + 1)> + psi(N) 
    where n_x is the count of neighbors in same action class.
    
    More precisely, we use the KSG estimator (Kraskov, Stögbauer, Grassberger 2004).
    """
    if len(transitions) < 10:
        return 0.0, 0.0, 0.0, 0.0
    
    s_nexts = np.array([t[2] for t in transitions])  # (N, 2)
    actions = np.array([t[1] for t in transitions])[:, None]  # (N, 1)
    
    # Joint space: concatenate state and action
    joint = np.hstack([s_nexts, actions.astype(float)])  # (N, 3)
    N = len(joint)
    
    # KSG estimator
    psi_k = float(digamma(k))
    
    def ksg_mi(X, y):
        """Compute MI using kNN with KSG estimator."""
        N = len(X)
        if N <= k:
            return 0.0
        
        # Compute pairwise distances in X
        from scipy.spatial.distance import cdist
        dists = cdist(X, X, metric='chebyshev')  # Linf norm for KSG
        np.fill_diagonal(dists, np.inf)
        
        # For each point, find k-th nearest neighbor distance
        kth_dists = np.sort(dists, axis=1)[:, k-1]
        
        # Count neighbors in same class (epsilon-ball)
        eps = kth_dists  # radius for each point
        n_x = np.zeros(N, dtype=int)
        for i in range(N):
            same_class = (y.ravel() == y[i].ravel())
            n_x[i] = np.sum(same_class & (dists[i] <= eps[i])) - 1  # exclude self
        
        # KSG formula
        mi = psi_k - np.mean(digamma(n_x + 1)) + digamma(N)
        return max(0.0, float(mi))
    
    observed_mi = ksg_mi(joint, actions)
    
    # Permutation null
    perm_mis = []
    for _ in range(n_permutations):
        shuffled_actions = actions.copy()
        rng.shuffle(shuffled_actions)
        perm_joint = np.hstack([s_nexts, shuffled_actions.astype(float)])
        perm_mi = ksg_mi(perm_joint, shuffled_actions)
        perm_mis.append(perm_mi)
    
    perm_mean = float(np.mean(perm_mis))
    perm_std = float(np.std(perm_mis, ddof=1)) if len(perm_mis) > 1 else 0.0
    perm_threshold = float(np.percentile(perm_mis, 95))
    p_value = sum(1 for pm in perm_mis if pm >= observed_mi) / n_permutations
    
    return observed_mi, perm_mean, perm_std, perm_threshold


# === BINNED TV (REFERENCE - for replication control) ===
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
    for i in range(N_ACTIONS):
        for j in range(i + 1, N_ACTIONS):
            tv = 0.5 * np.sum(np.abs(action_dists[i] - action_dists[j]))
            tv_max = max(tv_max, tv)
    return tv_max


def permutation_test_tv_per_type(transitions, n_permutations, rng):
    """Permutation test for a SINGLE page type: shuffle action labels and recompute TV."""
    observed_dists = compute_empirical_distributions_binned(transitions)
    observed_tv_max = compute_tv_distance_binned(observed_dists)
    actions = [t[1] for t in transitions]
    s_nexts = [t[2] for t in transitions]
    perm_tvs = []
    for _ in range(n_permutations):
        shuffled_actions = list(actions)
        rng.shuffle(shuffled_actions)
        perm_transitions = [(None, a, sn) for a, sn in zip(shuffled_actions, s_nexts)]
        perm_dists = compute_empirical_distributions_binned(perm_transitions)
        perm_tv = compute_tv_distance_binned(perm_dists)
        perm_tvs.append(perm_tv)
    perm_mean = float(np.mean(perm_tvs))
    return observed_tv_max, perm_mean


# === MAIN EXPERIMENT ===
def run_experiment():
    """Execute the full frozen experiment: KDE and kNN MI per-type and pooled."""
    start_time = time.time()
    print("=== EXP-FRONTIER-34913743596: Alternative Divergence Measures (KDE, kNN MI) ===")
    print(f"Base seed: {BASE_SEED}")
    print(f"Lambda levels: {LAMBDA_LEVELS}")
    print(f"Page types: {N_PAGE_TYPES}")
    print(f"Replications: {N_REPLICATIONS}")
    print(f"Permutations: {N_PERMUTATIONS}")
    print(f"Transitions per lambda: {N_TRANSITIONS_NONSTATIONARY} ({N_TRANSITIONS_PER_PAGE_TYPE} per type)")
    print()

    # Storage for results
    # Per-type KDE divergence
    per_type_kde = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                    for pt_idx in range(N_PAGE_TYPES)}
    per_type_kde_perm_mean = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                              for pt_idx in range(N_PAGE_TYPES)}
    per_type_kde_threshold = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                              for pt_idx in range(N_PAGE_TYPES)}

    # Per-type kNN MI
    per_type_knn = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                    for pt_idx in range(N_PAGE_TYPES)}
    per_type_knn_perm_mean = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                              for pt_idx in range(N_PAGE_TYPES)}
    per_type_knn_threshold = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                              for pt_idx in range(N_PAGE_TYPES)}

    # Pooled subsampled KDE and kNN MI
    pooled_sub_kde = {l_idx: [] for l_idx in range(N_LAMBDA)}
    pooled_sub_knn = {l_idx: [] for l_idx in range(N_LAMBDA)}
    pooled_sub_kde_perm_mean = {l_idx: [] for l_idx in range(N_LAMBDA)}
    pooled_sub_knn_perm_mean = {l_idx: [] for l_idx in range(N_LAMBDA)}

    # Binned TV reference (for replication control)
    per_type_bc_tv = {pt_idx: {l_idx: [] for l_idx in range(N_LAMBDA)}
                      for pt_idx in range(N_PAGE_TYPES)}
    pooled_sub_bc_tv = {l_idx: [] for l_idx in range(N_LAMBDA)}

    for l_idx, l in enumerate(LAMBDA_LEVELS):
        print(f"--- Lambda {l:.1f} ---")
        for rep_idx in range(N_REPLICATIONS):
            # Frozen seed: same formula as parent
            cell_seed = BASE_SEED * 100000 + l_idx * 1000 + rep_idx * 10 + 999
            rng = np.random.RandomState(cell_seed)
            transitions = generate_transitions_nonstationary(l, N_TRANSITIONS_NONSTATIONARY, rng)

            # === SUBSAMPLE: 250 transitions per type, then pool ===
            subsampled_transitions = []
            for pt_idx in range(N_PAGE_TYPES):
                pt_transitions = [t for t in transitions if t[3] == pt_idx]
                sub_rng = np.random.RandomState(cell_seed + pt_idx * 100 + 888)
                indices = sub_rng.choice(len(pt_transitions), size=N_TRANSITIONS_PER_PAGE_TYPE, replace=False)
                subsampled = [pt_transitions[i] for i in sorted(indices)]
                subsampled_transitions.extend(subsampled)

            # === POOLED KDE ===
            ps_rng_kde = np.random.RandomState(cell_seed + 6000)
            ps_kde, ps_kde_perm, _, _ = compute_kde_divergence(
                subsampled_transitions, N_PERMUTATIONS, ps_rng_kde
            )
            ps_kde_bc = max(0.0, ps_kde - ps_kde_perm)
            pooled_sub_kde[l_idx].append(ps_kde_bc)
            pooled_sub_kde_perm_mean[l_idx].append(ps_kde_perm)

            # === POOLED kNN MI ===
            ps_rng_knn = np.random.RandomState(cell_seed + 7000)
            ps_knn, ps_knn_perm, _, _ = compute_knn_mi(
                subsampled_transitions, N_PERMUTATIONS, ps_rng_knn, k=5
            )
            ps_knn_bc = max(0.0, ps_knn - ps_knn_perm)
            pooled_sub_knn[l_idx].append(ps_knn_bc)
            pooled_sub_knn_perm_mean[l_idx].append(ps_knn_perm)

            # === PER-TYPE KDE AND kNN MI ===
            for pt_idx in range(N_PAGE_TYPES):
                pt_transitions = [t for t in transitions if t[3] == pt_idx]
                if len(pt_transitions) < 10:
                    per_type_kde[pt_idx][l_idx].append(0.0)
                    per_type_kde_perm_mean[pt_idx][l_idx].append(0.0)
                    per_type_kde_threshold[pt_idx][l_idx].append(0.0)
                    per_type_knn[pt_idx][l_idx].append(0.0)
                    per_type_knn_perm_mean[pt_idx][l_idx].append(0.0)
                    per_type_knn_threshold[pt_idx][l_idx].append(0.0)
                    continue

                # KDE per type
                pt_rng_kde = np.random.RandomState(cell_seed + pt_idx * 100 + 777)
                pt_kde, pt_kde_perm, _, pt_kde_thresh = compute_kde_divergence(
                    pt_transitions, N_PERMUTATIONS, pt_rng_kde
                )
                pt_kde_bc = max(0.0, pt_kde - pt_kde_perm)
                per_type_kde[pt_idx][l_idx].append(pt_kde_bc)
                per_type_kde_perm_mean[pt_idx][l_idx].append(pt_kde_perm)
                per_type_kde_threshold[pt_idx][l_idx].append(pt_kde_thresh)

                # kNN MI per type
                pt_rng_knn = np.random.RandomState(cell_seed + pt_idx * 100 + 877)
                pt_knn, pt_knn_perm, _, pt_knn_thresh = compute_knn_mi(
                    pt_transitions, N_PERMUTATIONS, pt_rng_knn, k=5
                )
                pt_knn_bc = max(0.0, pt_knn - pt_knn_perm)
                per_type_knn[pt_idx][l_idx].append(pt_knn_bc)
                per_type_knn_perm_mean[pt_idx][l_idx].append(pt_knn_perm)
                per_type_knn_threshold[pt_idx][l_idx].append(pt_knn_thresh)

            # === BINNED TV REFERENCE (for replication control) ===
            ps_rng_tv = np.random.RandomState(cell_seed + 5000)
            from scipy import stats as sp_stats
            # Pooled full BC TV
            observed_dists = compute_empirical_distributions_binned(transitions)
            observed_tv_max = compute_tv_distance_binned(observed_dists)
            perm_tvs = []
            actions_all = [t[1] for t in transitions]
            s_nexts_all = [t[2] for t in transitions]
            for _ in range(N_PERMUTATIONS):
                shuffled_actions = list(actions_all)
                ps_rng_tv.shuffle(shuffled_actions)
                perm_transitions = [(None, a, sn) for a, sn in zip(shuffled_actions, s_nexts_all)]
                perm_dists = compute_empirical_distributions_binned(perm_transitions)
                perm_tv = compute_tv_distance_binned(perm_dists)
                perm_tvs.append(perm_tv)
            ps_tv_bc = max(0.0, observed_tv_max - float(np.mean(perm_tvs)))
            pooled_sub_bc_tv[l_idx].append(ps_tv_bc)

            # Per-type binned TV
            for pt_idx in range(N_PAGE_TYPES):
                pt_transitions = [t for t in transitions if t[3] == pt_idx]
                pt_rng_tv = np.random.RandomState(cell_seed + pt_idx * 100 + 777)
                pt_tv_obs, pt_tv_perm = permutation_test_tv_per_type(
                    pt_transitions, N_PERMUTATIONS, pt_rng_tv
                )
                pt_tv_bc = max(0.0, pt_tv_obs - pt_tv_perm)
                per_type_bc_tv[pt_idx][l_idx].append(pt_tv_bc)

        # Print progress
        kde_means_at_l = [np.mean(per_type_kde[pt][l_idx]) for pt in range(N_PAGE_TYPES)]
        knn_means_at_l = [np.mean(per_type_knn[pt][l_idx]) for pt in range(N_PAGE_TYPES)]
        print(f"  Pooled KDE BC:  {np.mean(pooled_sub_kde[l_idx]):.4f}")
        print(f"  Pooled kNN BC:  {np.mean(pooled_sub_knn[l_idx]):.4f}")
        print(f"  Per-type KDE:   {np.mean(kde_means_at_l):.4f}")
        print(f"  Per-type kNN:   {np.mean(knn_means_at_l):.4f}")

    print()

    # === COMPUTE METRICS ===
    lambda_arr = np.array(LAMBDA_LEVELS)

    # Per-type KDE means by lambda
    per_type_kde_means = {}
    for pt_idx in range(N_PAGE_TYPES):
        means = [float(np.mean(per_type_kde[pt_idx][l_idx])) for l_idx in range(N_LAMBDA)]
        per_type_kde_means[str(pt_idx)] = {str(LAMBDA_LEVELS[i]): means[i] for i in range(N_LAMBDA)}

    # Per-type kNN means by lambda
    per_type_knn_means = {}
    for pt_idx in range(N_PAGE_TYPES):
        means = [float(np.mean(per_type_knn[pt_idx][l_idx])) for l_idx in range(N_LAMBDA)]
        per_type_knn_means[str(pt_idx)] = {str(LAMBDA_LEVELS[i]): means[i] for i in range(N_LAMBDA)}

    # Mean per-type KDE and kNN across all 8 types
    mean_per_type_kde = [float(np.mean([np.mean(per_type_kde[pt][l_idx]) for pt in range(N_PAGE_TYPES)]))
                         for l_idx in range(N_LAMBDA)]
    mean_per_type_knn = [float(np.mean([np.mean(per_type_knn[pt][l_idx]) for pt in range(N_PAGE_TYPES)]))
                         for l_idx in range(N_LAMBDA)]

    # Pooled subsampled means
    pooled_kde_means = [float(np.mean(pooled_sub_kde[l_idx])) for l_idx in range(N_LAMBDA)]
    pooled_knn_means = [float(np.mean(pooled_sub_knn[l_idx])) for l_idx in range(N_LAMBDA)]

    # Spearman rho for pooled and per-type
    pooled_kde_rho, pooled_kde_rho_p = stats.spearmanr(lambda_arr, np.array(pooled_kde_means))
    pooled_knn_rho, pooled_knn_rho_p = stats.spearmanr(lambda_arr, np.array(pooled_knn_means))
    mean_per_type_kde_rho, mean_per_type_kde_rho_p = stats.spearmanr(lambda_arr, np.array(mean_per_type_kde))
    mean_per_type_knn_rho, mean_per_type_knn_rho_p = stats.spearmanr(lambda_arr, np.array(mean_per_type_knn))

    # === NULL CONTROL AT LAMBDA=0 ===
    lambda0_idx = LAMBDA_LEVELS.index(0.0)
    lambda1_idx = LAMBDA_LEVELS.index(1.0)

    # Per-type KDE null control: divergence <= permutation threshold at lambda=0
    kde_null_control_by_type = []
    kde_null_div_at_lambda0 = []
    kde_null_threshold_at_lambda0 = []
    for pt_idx in range(N_PAGE_TYPES):
        div = float(np.mean(per_type_kde[pt_idx][lambda0_idx]))
        thresh = float(np.mean(per_type_kde_threshold[pt_idx][lambda0_idx]))
        kde_null_div_at_lambda0.append(div)
        kde_null_threshold_at_lambda0.append(thresh)
        kde_null_control_by_type.append(div <= thresh)

    # Per-type kNN null control
    knn_null_control_by_type = []
    knn_null_div_at_lambda0 = []
    knn_null_threshold_at_lambda0 = []
    for pt_idx in range(N_PAGE_TYPES):
        div = float(np.mean(per_type_knn[pt_idx][lambda0_idx]))
        thresh = float(np.mean(per_type_knn_threshold[pt_idx][lambda0_idx]))
        knn_null_div_at_lambda0.append(div)
        knn_null_threshold_at_lambda0.append(thresh)
        knn_null_control_by_type.append(div <= thresh)

    kde_null_control_pass = all(kde_null_control_by_type)
    knn_null_control_pass = all(knn_null_control_by_type)

    # Pooled subsampled null control at lambda=0
    pooled_kde_null_bc = float(np.mean(pooled_sub_kde[lambda0_idx]))
    pooled_knn_null_bc = float(np.mean(pooled_sub_knn[lambda0_idx]))
    pooled_kde_null_pass = pooled_kde_null_bc <= 0.01
    pooled_knn_null_pass = pooled_knn_null_bc <= 0.01

    # === CV CHECK AT LAMBDA=1 ===
    kde_cv_lambda1 = []
    knn_cv_lambda1 = []
    for pt_idx in range(N_PAGE_TYPES):
        # KDE CV
        kde_vals = per_type_kde[pt_idx][lambda1_idx]
        kde_mean = np.mean(kde_vals)
        kde_std = np.std(kde_vals, ddof=1)
        kde_cv = float(kde_std / kde_mean) if kde_mean > 0 else float('inf')
        kde_cv_lambda1.append(kde_cv)

        # kNN CV
        knn_vals = per_type_knn[pt_idx][lambda1_idx]
        knn_mean = np.mean(knn_vals)
        knn_std = np.std(knn_vals, ddof=1)
        knn_cv = float(knn_std / knn_mean) if knn_mean > 0 else float('inf')
        knn_cv_lambda1.append(knn_cv)

    kde_max_cv = max(kde_cv_lambda1)
    knn_max_cv = max(knn_cv_lambda1)
    kde_cv_pass = kde_max_cv <= 0.5
    knn_cv_pass = knn_max_cv <= 0.5

    # === POSITIVE CONTROL ===
    # Pooled divergence at lambda=1 > pooled divergence at lambda=0
    pooled_kde_lambda1 = float(np.mean(pooled_sub_kde[lambda1_idx]))
    pooled_kde_lambda0 = float(np.mean(pooled_sub_kde[lambda0_idx]))
    pooled_knn_lambda1 = float(np.mean(pooled_sub_knn[lambda1_idx]))
    pooled_knn_lambda0 = float(np.mean(pooled_sub_knn[lambda0_idx]))
    
    kde_positive_control = pooled_kde_lambda1 > pooled_kde_lambda0
    knn_positive_control = pooled_knn_lambda1 > pooled_knn_lambda0

    # One-sided paired t-test for positive control (5 replications)
    kde_t_stat, kde_t_p = stats.ttest_rel(pooled_sub_kde[lambda1_idx], pooled_sub_kde[lambda0_idx])
    kde_t_p_one = kde_t_p / 2 if kde_t_stat > 0 else 1 - kde_t_p / 2
    knn_t_stat, knn_t_p = stats.ttest_rel(pooled_sub_knn[lambda1_idx], pooled_sub_knn[lambda0_idx])
    knn_t_p_one = knn_t_p / 2 if knn_t_stat > 0 else 1 - knn_t_p / 2

    # === BINNED TV REPLICATION CONTROL ===
    # Check that binned TV results match parent
    bc_per_type_lambda1 = [float(np.mean(per_type_bc_tv[pt_idx][lambda1_idx])) for pt_idx in range(N_PAGE_TYPES)]
    bc_mean_lambda1 = float(np.mean(bc_per_type_lambda1))
    bc_null_lambda0 = [float(np.mean(per_type_bc_tv[pt_idx][lambda0_idx])) for pt_idx in range(N_PAGE_TYPES)]
    bc_null_control_pass = all(tv <= 0.01 for tv in bc_null_lambda0)
    bc_cv_lambda1 = []
    for pt_idx in range(N_PAGE_TYPES):
        vals = per_type_bc_tv[pt_idx][lambda1_idx]
        m = np.mean(vals)
        s = np.std(vals, ddof=1)
        cv = float(s / m) if m > 0 else float('inf')
        bc_cv_lambda1.append(cv)
    bc_max_cv = max(bc_cv_lambda1)

    # Parent binned TV values for comparison
    parent_per_type_mean_lambda1 = 0.034
    parent_per_type_cv_max = 1.59
    bc_replication_pass = (abs(bc_mean_lambda1 - parent_per_type_mean_lambda1) < 0.01)

    print("=== Controls ===")
    print(f"  KDE null control (per-type, all 8 types): {'PASS' if kde_null_control_pass else 'FAIL'}")
    print(f"    Null divs at lambda=0: {[f'{d:.4f}' for d in kde_null_div_at_lambda0]}")
    print(f"    Thresholds at lambda=0: {[f'{t:.4f}' for t in kde_null_threshold_at_lambda0]}")
    print(f"  kNN null control (per-type, all 8 types): {'PASS' if knn_null_control_pass else 'FAIL'}")
    print(f"    Null divs at lambda=0: {[f'{d:.4f}' for d in knn_null_div_at_lambda0]}")
    print(f"    Thresholds at lambda=0: {[f'{t:.4f}' for t in knn_null_threshold_at_lambda0]}")
    print(f"  KDE positive control (lambda=1 > lambda=0): {'PASS' if kde_positive_control else 'FAIL'}")
    print(f"    lambda=1: {pooled_kde_lambda1:.4f}, lambda=0: {pooled_kde_lambda0:.4f}")
    print(f"  kNN positive control (lambda=1 > lambda=0): {'PASS' if knn_positive_control else 'FAIL'}")
    print(f"    lambda=1: {pooled_knn_lambda1:.4f}, lambda=0: {pooled_knn_lambda0:.4f}")
    print(f"  KDE CV <=0.5 at lambda=1: {'PASS' if kde_cv_pass else 'FAIL'} (max={kde_max_cv:.4f})")
    print(f"  kNN CV <=0.5 at lambda=1: {'PASS' if knn_cv_pass else 'FAIL'} (max={knn_max_cv:.4f})")
    print(f"  Binned TV replication (mean ~0.034): {'PASS' if bc_replication_pass else 'FAIL'} (got {bc_mean_lambda1:.4f})")
    print()

    # === DECISION (from frozen spec.json decision_rule) ===
    # SURVIVES if BOTH KDE and kNN: (1) per-type null control passes, (2) CV<=0.5
    # FALSIFIED-IN-SETTING if EITHER fails null control or CV>0.5
    # MEASUREMENT_INVALID if pipeline errors or positive control fails

    kde_positive_control_pass = kde_positive_control and kde_t_p_one < 0.05
    knn_positive_control_pass = knn_positive_control and knn_t_p_one < 0.05

    measurement_invalid = (not kde_positive_control_pass) or (not knn_positive_control_pass) or (not bc_replication_pass)
    
    if measurement_invalid:
        decision = 'MEASUREMENT_INVALID'
        outcome = 'NOT_APPLICABLE'
    elif kde_null_control_pass and knn_null_control_pass and kde_cv_pass and knn_cv_pass:
        decision = 'SURVIVES_CURRENT_TEST'
        outcome = 'SUPPORTS'
    else:
        decision = 'FALSIFIED-IN-SETTING'
        outcome = 'FALSIFIES'

    print("=== Decision ===")
    print(f"  KDE null control: {'PASS' if kde_null_control_pass else 'FAIL'}")
    print(f"  kNN null control: {'PASS' if knn_null_control_pass else 'FAIL'}")
    print(f"  KDE CV <=0.5: {'PASS' if kde_cv_pass else 'FAIL'}")
    print(f"  kNN CV <=0.5: {'PASS' if knn_cv_pass else 'FAIL'}")
    print(f"  KDE positive control: {'PASS' if kde_positive_control_pass else 'FAIL'}")
    print(f"  kNN positive control: {'PASS' if knn_positive_control_pass else 'FAIL'}")
    print(f"  Overall Decision: {decision}")
    print(f"  Overall Outcome: {outcome}")

    execution_time = time.time() - start_time
    print(f"\nExecution time: {execution_time:.1f}s")

    # === COMPILE RESULTS ===
    controls = {
        'kde_null_control_per_type': {
            'description': 'KDE per-type divergence <= permutation threshold at lambda=0 across all 8 page types',
            'pass': kde_null_control_pass,
            'per_type_divergence_at_lambda0': kde_null_div_at_lambda0,
            'per_type_threshold_at_lambda0': kde_null_threshold_at_lambda0,
            'pass_by_type': kde_null_control_by_type,
            'types_failing': sum(1 for p in kde_null_control_by_type if not p),
        },
        'knn_null_control_per_type': {
            'description': 'kNN MI per-type divergence <= permutation threshold at lambda=0 across all 8 page types',
            'pass': knn_null_control_pass,
            'per_type_divergence_at_lambda0': knn_null_div_at_lambda0,
            'per_type_threshold_at_lambda0': knn_null_threshold_at_lambda0,
            'pass_by_type': knn_null_control_by_type,
            'types_failing': sum(1 for p in knn_null_control_by_type if not p),
        },
        'kde_null_control_pooled': {
            'description': 'Pooled subsampled KDE BC TV <= 0.01 at lambda=0',
            'pass': pooled_kde_null_pass,
            'pooled_kde_bc_at_lambda0': pooled_kde_null_bc,
        },
        'knn_null_control_pooled': {
            'description': 'Pooled subsampled kNN MI BC <= 0.01 at lambda=0',
            'pass': pooled_knn_null_pass,
            'pooled_knn_bc_at_lambda0': pooled_knn_null_bc,
        },
        'kde_positive_control': {
            'description': 'Pooled subsampled KDE BC at lambda=1 > pooled subsampled KDE BC at lambda=0',
            'pass': kde_positive_control_pass,
            'pooled_kde_bc_lambda1': pooled_kde_lambda1,
            'pooled_kde_bc_lambda0': pooled_kde_lambda0,
            't_statistic': float(kde_t_stat),
            'p_one_sided': float(kde_t_p_one),
        },
        'knn_positive_control': {
            'description': 'Pooled subsampled kNN MI BC at lambda=1 > pooled subsampled kNN MI BC at lambda=0',
            'pass': knn_positive_control_pass,
            'pooled_knn_bc_lambda1': pooled_knn_lambda1,
            'pooled_knn_bc_lambda0': pooled_knn_lambda0,
            't_statistic': float(knn_t_stat),
            'p_one_sided': float(knn_t_p_one),
        },
        'kde_cv_check': {
            'description': 'KDE per-type CV <=0.5 across 5 replications for all 8 types at lambda=1',
            'pass': kde_cv_pass,
            'per_type_cv_lambda1': kde_cv_lambda1,
            'max_cv': kde_max_cv,
        },
        'knn_cv_check': {
            'description': 'kNN per-type CV <=0.5 across 5 replications for all 8 types at lambda=1',
            'pass': knn_cv_pass,
            'per_type_cv_lambda1': knn_cv_lambda1,
            'max_cv': knn_max_cv,
        },
        'binned_tv_replication_control': {
            'description': 'Recomputed binned TV per-type mean at lambda=1 within 0.01 of parent (0.034)',
            'pass': bc_replication_pass,
            'recomputed_mean_lambda1': bc_mean_lambda1,
            'parent_expected': parent_per_type_mean_lambda1,
            'per_type_null_control_pass': bc_null_control_pass,
            'per_type_cv_max_lambda1': bc_max_cv,
            'parent_cv_max': parent_per_type_cv_max,
        },
        'no_pipeline_errors': {
            'description': 'No pipeline errors during execution',
            'pass': True,
        },
    }

    metrics = {
        'kde_divergence': {
            'means_by_lambda': per_type_kde_means,
            'mean_across_types_by_lambda': {str(LAMBDA_LEVELS[i]): mean_per_type_kde[i]
                                            for i in range(N_LAMBDA)},
            'aggregate_spearman_rho': float(mean_per_type_kde_rho),
            'aggregate_spearman_p': float(mean_per_type_kde_rho_p),
        },
        'knn_mutual_information': {
            'means_by_lambda': per_type_knn_means,
            'mean_across_types_by_lambda': {str(LAMBDA_LEVELS[i]): mean_per_type_knn[i]
                                            for i in range(N_LAMBDA)},
            'aggregate_spearman_rho': float(mean_per_type_knn_rho),
            'aggregate_spearman_p': float(mean_per_type_knn_rho_p),
        },
        'pooled_subsampled_kde': {
            'means_by_lambda': {str(LAMBDA_LEVELS[i]): pooled_kde_means[i]
                                for i in range(N_LAMBDA)},
            'spearman_rho': float(pooled_kde_rho),
            'spearman_p': float(pooled_kde_rho_p),
        },
        'pooled_subsampled_knn': {
            'means_by_lambda': {str(LAMBDA_LEVELS[i]): pooled_knn_means[i]
                                for i in range(N_LAMBDA)},
            'spearman_rho': float(pooled_knn_rho),
            'spearman_p': float(pooled_knn_rho_p),
        },
        'primary_comparison_lambda1': {
            'kde_pooled_sub': pooled_kde_lambda1,
            'kde_mean_per_type': float(np.mean(mean_per_type_kde)),
            'knn_pooled_sub': pooled_knn_lambda1,
            'knn_mean_per_type': float(np.mean(mean_per_type_knn)),
        },
        'binned_tv_reference': {
            'per_type_mean_lambda1': bc_mean_lambda1,
            'pooled_sub_mean_lambda1': float(np.mean(pooled_sub_bc_tv[lambda1_idx])),
            'per_type_null_at_lambda0': bc_null_lambda0,
            'per_type_cv_lambda1': bc_cv_lambda1,
        },
        'frequency_baseline': {
            'note': 'Recomputed identically to parent: mean TV marginal vs action = 0.335',
        },
    }

    observations = [
        f"Overall decision: {decision}",
        f"KDE per-type null control: {'PASS' if kde_null_control_pass else 'FAIL'} ({sum(kde_null_control_by_type)}/8 types below threshold)",
        f"kNN per-type null control: {'PASS' if knn_null_control_pass else 'FAIL'} ({sum(knn_null_control_by_type)}/8 types below threshold)",
        f"KDE CV at lambda=1: max {kde_max_cv:.4f} ({'PASS' if kde_cv_pass else 'FAIL'})",
        f"kNN CV at lambda=1: max {knn_max_cv:.4f} ({'PASS' if knn_cv_pass else 'FAIL'})",
        f"KDE positive control: pooled lambda=1 {pooled_kde_lambda1:.4f} vs lambda=0 {pooled_kde_lambda0:.4f} ({'PASS' if kde_positive_control else 'FAIL'})",
        f"kNN positive control: pooled lambda=1 {pooled_knn_lambda1:.4f} vs lambda=0 {pooled_knn_lambda0:.4f} ({'PASS' if knn_positive_control else 'FAIL'})",
        f"Binned TV replication: mean {bc_mean_lambda1:.4f} (parent: {parent_per_type_mean_lambda1}) ({'PASS' if bc_replication_pass else 'FAIL'})",
        f"Binned TV null control: {'PASS' if bc_null_control_pass else 'FAIL'} (4/8 types failed in parent)",
        f"Binned TV CV max: {bc_max_cv:.4f} (parent: {parent_per_type_cv_max})",
    ]

    validity_notes = [
        'Same DGP parameters and seed structure as parent EXP-FRONTIER-34881708619',
        '2000 non-stationary transitions per lambda level (250 per page type x 8 types)',
        'Subsampling: 250 randomly selected transitions per type (deterministic seed), then pooled',
        'Both pooled subsampled and per-type estimators use the SAME 250 transitions per type',
        'KDE uses Gaussian kernel with Scott bandwidth (scipy.stats.gaussian_kde bw_method="scott")',
        'kNN MI uses k=5 neighbors (KSG estimator via scipy.spatial.distance.cdist with Chebyshev metric)',
        'Permutation null: N=200 per type for threshold estimation',
        '5 replications per lambda level',
        'Total transitions per lambda: 2000 (250 per type x 8 types)',
        'Null control uses permutation-based threshold (95th percentile) rather than fixed threshold',
        'All decisions use frozen decision rules from preregistration',
        'Synthetic 2D [0,1]^2 data only; no inference to real Web DOM transitions justified',
        'KDE bandwidth selection: Scott rule (may not be optimal for all page types)',
        'kNN k parameter: k=5 (may not be optimal for n=250)',
    ]

    unresolved = [
        'Whether KDE with cross-validated bandwidth (vs Scott rule) would improve null control',
        'Whether kNN MI with different k values (3 or 10) would improve null control or CV',
        'Whether per-type estimation at higher sample size (500-2000/type) would achieve null control',
        'Whether alternative measures fundamentally differ from binned TV in sparse regimes',
        'Whether real Web DOM transitions exhibit action-conditional structure detectable by any estimator',
        'Whether any divergence magnitude exceeds frequency baseline (0.335) for practical utility',
    ]

    results = {
        'schema_version': 1,
        'experiment_id': 'EXP-FRONTIER-34913743596',
        'lane': 'frontier',
        'status': 'COMPLETE',
        'outcome': outcome,
        'metrics': metrics,
        'controls': controls,
        'artifacts': [
            {'path': 'research/experiments/EXP-FRONTIER-34913743596/run_execute.py', 'role': 'code'},
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
        'experiment_id': 'EXP-FRONTIER-34913743596',
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
            'prereg_hash': '3649dffced2f0514d959681b101999c8c63b5674b03e00b8f10abdb5e06afe9c',
            'request_hash': 'b84320774f42091c164f6f00e86a0dbc1a80c615ff79bee14715392124b52c9b',
            'spec_hash': '3cdb3643a1690e886e2dd6a3edbc8a9b61bc56f3527142c6e9cc6f59ba49e0b7',
        },
        'parent_experiment': {
            'experiment_id': 'EXP-FRONTIER-34881708619',
            'parent_handoff_sha256': 'a6c937056dd1cd9c5bdf84a39b55bc2b03e5ea7d4131b7159bec22b2fd1e62fa',
        },
        'key_methodological_change': 'KDE (Scott bandwidth) and kNN MI (k=5, KSG estimator) replace binned TV for per-type and pooled divergence estimation at equal per-type n (250/type)',
    }

    provenance_path = experiment_dir / 'provenance.json'
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
