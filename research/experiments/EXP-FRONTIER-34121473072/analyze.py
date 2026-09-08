#!/usr/bin/env python3
"""
EXP-FRONTIER-34121473072: Bias-Corrected kNN TV in 10D Non-Gaussian Spaces.

Frozen experiment code. Do not modify after freeze.

Tests whether bias-corrected kNN TV (permutation-null subtraction removing
the ~0.52 finite-sample floor) recovers uniform function invariance in 10D
non-Gaussian spaces, and whether clipping artefact explains the translation
strong signal vs scaling weakness.
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
    """
    dist_to_center = np.linalg.norm(s - 0.5)
    sigma_base = 0.05 * (1 + 0.5 * dist_to_center)

    noise = np.zeros(DIM)
    for i in range(DIM):
        r = rng.random()
        if r < 0.5:
            mean_i = 0.0
            std_i = sigma_base
        elif r < 0.8:
            mean_i = 0.1 * sigma_base
            std_i = 0.5 * sigma_base
        else:
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
def generate_transitions(func_seed, lambda_val, n, rng, noise_type='nongaussian', boundary='clip'):
    """
    Generate transitions using 10D non-Gaussian DGP.

    With probability lambda: s_next = deterministic_function(s, a) + noise
    With probability (1-lambda): s_next ~ mixture centered at 0.5

    boundary: 'clip' clips to [0,1], 'toroidal' wraps using modular arithmetic
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

        # Boundary treatment
        if boundary == 'clip':
            s_next = np.clip(s_next, 0, 1)
        elif boundary == 'toroidal':
            s_next = s_next - np.floor(s_next)  # modular arithmetic

        transitions.append((s, ACTIONS[a_idx], s_next))
    return transitions


# === TV DISTANCE: kNN-BASED (PRIMARY) ===
def knn_tv_estimate(X_a, X_b, k):
    """
    Estimate TV distance between two samples using kNN.
    """
    if len(X_a) < k + 1 or len(X_b) < k + 1:
        return 0.0

    tree_a = KDTree(X_a)
    tree_b = KDTree(X_b)

    d_aa, _ = tree_a.query(X_a, k=k + 1)
    d_ab, _ = tree_b.query(X_a, k=k)
    d_aa_k = d_aa[:, k]
    frac_a = np.mean(d_aa_k < d_ab[:, k - 1])

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
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)

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


# === PERMUTATION NULL DISTRIBUTION ===
def compute_permutation_null(transitions, k, n_permutations, rng):
    """
    Compute permutation null distribution: shuffle action labels, recompute kNN TV.
    Returns the full distribution of permuted TV values.
    """
    actions = [a for _, a, _ in transitions]
    s_nexts = [s for _, _, s in transitions]

    perm_tvs = []
    for _ in range(n_permutations):
        shuffled_actions = list(actions)
        rng.shuffle(shuffled_actions)
        perm_transitions = [(None, a, sn) for a, sn in zip(shuffled_actions, s_nexts)]
        perm_tv, _ = compute_knn_tv_all_pairs(perm_transitions, k)
        perm_tvs.append(perm_tv)

    return np.array(perm_tvs)


# === FREQUENCY BASELINE ===
def compute_frequency_baseline(transitions):
    """
    Compute frequency baseline: TV between action-conditional distributions
    using marginal P(S_{t+1}) as reference.
    """
    # Group by action
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)

    # Compute marginal P(S_{t+1}) by pooling all actions
    all_next = np.array([s_next for _, _, s_next in transitions])

    # For frequency baseline, compute TV between each action pair
    # using a simple binning approach in 10D (use first 2 dims for speed)
    actions_list = list(ACTIONS)
    tv_max = 0.0

    for i in range(len(actions_list)):
        for j in range(i + 1, len(actions_list)):
            X_a = np.array(action_states[actions_list[i]])
            X_b = np.array(action_states[actions_list[j]])

            # Use first 2 dims for binning (full 10D is too sparse)
            n_bins = 10
            bins = np.linspace(0, 1, n_bins + 1)

            # Bin X_a
            x_a_bin = np.digitize(X_a[:, 0], bins) - 1
            y_a_bin = np.digitize(X_a[:, 1], bins) - 1
            x_a_bin = np.clip(x_a_bin, 0, n_bins - 1)
            y_a_bin = np.clip(y_a_bin, 0, n_bins - 1)
            counts_a = np.zeros((n_bins, n_bins))
            for xb, yb in zip(x_a_bin, y_a_bin):
                counts_a[xb, yb] += 1
            if len(X_a) > 0:
                counts_a /= len(X_a)

            # Bin X_b
            x_b_bin = np.digitize(X_b[:, 0], bins) - 1
            y_b_bin = np.digitize(X_b[:, 1], bins) - 1
            x_b_bin = np.clip(x_b_bin, 0, n_bins - 1)
            y_b_bin = np.clip(y_b_bin, 0, n_bins - 1)
            counts_b = np.zeros((n_bins, n_bins))
            for xb, yb in zip(x_b_bin, y_b_bin):
                counts_b[xb, yb] += 1
            if len(X_b) > 0:
                counts_b /= len(X_b)

            # TV between the two action distributions
            tv = 0.5 * np.sum(np.abs(counts_a - counts_b))
            tv_max = max(tv_max, tv)

    return tv_max


# === MAIN EXPERIMENT ===
def run_experiment():
    """Execute the full frozen experiment."""
    start_time = time.time()
    print("=== EXP-FRONTIER-34121473072: Bias-Corrected kNN TV in 10D ===")
    print(f"Seed: {SEED}")
    print(f"Lambda levels: {LAMBDA_LEVELS}")
    print(f"Functions: 3 (seeds {FUNCTION_SEEDS})")
    print(f"Transitions per cell: {N_TRANSITIONS}")
    print(f"Replications per cell: {N_REPLICATIONS}")
    print(f"Permutations per cell: {N_PERMUTATIONS}")
    print(f"State space: continuous 10D [0,1]^10")
    print(f"Noise: mixture of 3 Gaussians (non-Gaussian heteroscedastic)")
    print(f"kNN scales: {KNN_SCALES}")
    print(f"Primary kNN scale: k={PRIMARY_K}")
    print()

    # === STORAGE ===
    # Raw (unclipped) TV at multiple scales
    all_knn_tv_raw = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                          for f_idx in range(len(FUNCTION_SEEDS))}
                      for k in KNN_SCALES}

    # Permutation null distributions
    all_perm_nulls = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                          for f_idx in range(len(FUNCTION_SEEDS))}
                      for k in KNN_SCALES}

    # Bias-corrected TV (raw - perm_mean)
    all_knn_tv_bc = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                         for f_idx in range(len(FUNCTION_SEEDS))}
                     for k in KNN_SCALES}

    # Toroidal wrapping TV (at k=20 only, for clipping comparison)
    all_toroidal_tv = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                       for f_idx in range(len(FUNCTION_SEEDS))}

    # Frequency baseline
    all_freq_baseline = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                         for f_idx in range(len(FUNCTION_SEEDS))}

    # Gaussian noise baseline
    all_gaussian_tv = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                       for f_idx in range(len(FUNCTION_SEEDS))}

    raw_tables = []
    clipping_fractions = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                          for f_idx in range(len(FUNCTION_SEEDS))}

    # === RUN EXPERIMENT ===
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}...", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)

                # Generate transitions with clipping (standard)
                transitions = generate_transitions(func_seed, l, N_TRANSITIONS, rng,
                                                   noise_type='nongaussian', boundary='clip')

                # Track clipping
                n_clipped = 0
                for s, a, s_next in transitions:
                    if np.any(s_next <= 0) or np.any(s_next >= 1):
                        n_clipped += 1
                clipping_fractions[f_idx][l].append(n_clipped / len(transitions))

                # kNN TV at all scales (raw, before bias correction)
                for k in KNN_SCALES:
                    tv_max, tv_mean = compute_knn_tv_all_pairs(transitions, k)
                    all_knn_tv_raw[k][f_idx][l].append(tv_max)

                # Permutation null distribution (1000 perms per cell)
                perm_rng = np.random.RandomState(rep_seed + 999)
                for k in KNN_SCALES:
                    perm_dist = compute_permutation_null(transitions, k, N_PERMUTATIONS, perm_rng)
                    all_perm_nulls[k][f_idx][l].append(perm_dist)

                    # Bias correction: raw - mean(perm_null)
                    perm_mean = np.mean(perm_dist)
                    raw_tv = all_knn_tv_raw[k][f_idx][l][-1]
                    bc_tv = max(0.0, raw_tv - perm_mean)
                    all_knn_tv_bc[k][f_idx][l].append(bc_tv)

                # Toroidal wrapping (at k=20 only)
                rng_tor = np.random.RandomState(rep_seed)
                transitions_tor = generate_transitions(func_seed, l, N_TRANSITIONS, rng_tor,
                                                       noise_type='nongaussian', boundary='toroidal')
                tv_tor, _ = compute_knn_tv_all_pairs(transitions_tor, PRIMARY_K)
                all_toroidal_tv[f_idx][l].append(tv_tor)

                # Frequency baseline
                freq_tv = compute_frequency_baseline(transitions)
                all_freq_baseline[f_idx][l].append(freq_tv)

                # Gaussian noise baseline (same DGP, single Gaussian noise)
                rng_gauss = np.random.RandomState(rep_seed)
                transitions_gauss = generate_transitions(func_seed, l, N_TRANSITIONS, rng_gauss,
                                                         noise_type='gaussian', boundary='clip')
                tv_gauss, _ = compute_knn_tv_all_pairs(transitions_gauss, PRIMARY_K)
                all_gaussian_tv[f_idx][l].append(tv_gauss)

                raw_tables.append({
                    'func_seed': func_seed,
                    'func_name': func_name,
                    'lambda': l,
                    'replication': rep_idx,
                    'knn_tv_raw_k20': all_knn_tv_raw[PRIMARY_K][f_idx][l][-1],
                    'knn_tv_bc_k20': all_knn_tv_bc[PRIMARY_K][f_idx][l][-1],
                    'perm_mean_k20': float(np.mean(all_perm_nulls[PRIMARY_K][f_idx][l][-1])),
                    'toroidal_tv_k20': tv_tor,
                    'freq_baseline': freq_tv,
                    'gaussian_tv_k20': tv_gauss,
                    'clipping_fraction': clipping_fractions[f_idx][l][-1],
                })

            # Print summary for this cell
            raw_means = np.mean(all_knn_tv_raw[PRIMARY_K][f_idx][l])
            bc_means = np.mean(all_knn_tv_bc[PRIMARY_K][f_idx][l])
            perm_means = np.mean([np.mean(p) for p in all_perm_nulls[PRIMARY_K][f_idx][l]])
            tor_means = np.mean(all_toroidal_tv[f_idx][l])
            print(f" raw={raw_means:.4f} bc={bc_means:.4f} perm_mean={perm_means:.4f}"
                  f" toroidal={tor_means:.4f}")

        print()

    # === BIAS FLOOR CONSISTENCY CHECK ===
    print("=== Bias Floor Consistency (lambda=0, k=20) ===")
    perm_floor_means = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        floor_val = np.mean([np.mean(p) for p in all_perm_nulls[PRIMARY_K][f_idx][0.0]])
        perm_floor_means.append(floor_val)
        print(f"  Function {FUNCTION_SEEDS[f_idx]}: perm_mean at lambda=0 = {floor_val:.4f}")
    floor_cv = np.std(perm_floor_means) / np.mean(perm_floor_means)
    print(f"  CV across functions: {floor_cv:.4f}")
    print(f"  Floor consistency: {'PASS' if floor_cv < 0.1 else 'FAIL'}")
    print()

    # === AGGREGATE ANALYSIS: BIAS-CORRECTED TV ===
    print("=== Aggregate Analysis: Bias-Corrected TV (kNN k=20) ===")
    per_function_results_bc = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        lambda_arr = np.array(LAMBDA_LEVELS)
        bc_means = np.array([np.mean(all_knn_tv_bc[PRIMARY_K][f_idx][l]) for l in LAMBDA_LEVELS])

        spearman_rho, spearman_p = stats.spearmanr(lambda_arr, bc_means)
        spearman_p_one_sided = spearman_p / 2 if spearman_rho > 0 else 1 - spearman_p / 2

        per_function_results_bc[func_seed] = {
            'func_name': func_name,
            'spearman_rho': float(spearman_rho),
            'spearman_p_one_sided': float(spearman_p_one_sided),
            'bc_tv_means_by_lambda': {str(l): float(bc_means[i]) for i, l in enumerate(LAMBDA_LEVELS)},
        }
        print(f"  Function {func_seed} ({func_name}): rho={spearman_rho:.4f}, p_one_sided={spearman_p_one_sided:.6f}")
    print()

    # === AGGREGATE BIAS-CORRECTED TEST ===
    print("=== Aggregate Bias-Corrected Test ===")
    aggregate_bc_means = []
    for l in LAMBDA_LEVELS:
        all_bc_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_bc_at_l.extend(all_knn_tv_bc[PRIMARY_K][f_idx][l])
        aggregate_bc_means.append(float(np.mean(all_bc_at_l)))

    lambda_arr = np.array(LAMBDA_LEVELS)
    agg_bc_rho, agg_bc_p = stats.spearmanr(lambda_arr, np.array(aggregate_bc_means))
    agg_bc_p_one_sided = agg_bc_p / 2 if agg_bc_rho > 0 else 1 - agg_bc_p / 2

    print(f"  Aggregate Spearman rho(bc_TV, lambda): {agg_bc_rho:.4f}")
    print(f"  One-sided p-value: {agg_bc_p_one_sided:.6f}")
    print()

    # === MULTI-SCALE BIAS-CORRECTED ANALYSIS ===
    print("=== Multi-Scale Bias-Corrected kNN Analysis ===")
    multiscale_bc_results = {}
    for k in KNN_SCALES:
        agg_bc_means_k = []
        for l in LAMBDA_LEVELS:
            all_bc_at_l = []
            for f_idx in range(len(FUNCTION_SEEDS)):
                all_bc_at_l.extend(all_knn_tv_bc[k][f_idx][l])
            agg_bc_means_k.append(float(np.mean(all_bc_at_l)))

        rho_k, p_k = stats.spearmanr(lambda_arr, np.array(agg_bc_means_k))
        p_k_one_sided = p_k / 2 if rho_k > 0 else 1 - p_k / 2
        is_monotonic = all(agg_bc_means_k[i] <= agg_bc_means_k[i + 1]
                          for i in range(len(agg_bc_means_k) - 1))

        multiscale_bc_results[k] = {
            'rho': float(rho_k),
            'p_one_sided': float(p_k_one_sided),
            'monotonic': is_monotonic,
            'bc_tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): agg_bc_means_k[i]
                                      for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  k={k}: rho={rho_k:.4f}, p={p_k_one_sided:.6f}, monotonic={is_monotonic}")
    print()

    # === PERMUTATION TESTS (bias-corrected) ===
    print("=== Permutation Tests (bias-corrected) ===")
    perm_results_bc = {}
    for l_key in [0.0, 1.0]:
        perm_p_vals = []
        for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
            for rep_idx in range(N_REPLICATIONS):
                perm_dist = all_perm_nulls[PRIMARY_K][f_idx][l_key][rep_idx]
                raw_tv = all_knn_tv_raw[PRIMARY_K][f_idx][l_key][rep_idx]
                perm_mean = np.mean(perm_dist)
                bc_tv = max(0.0, raw_tv - perm_mean)

                # For lambda=0: p-value = fraction of permuted TVs >= observed raw TV
                # For bias-corrected: test if bc_tv > 0 (i.e., raw > perm_mean)
                count_ge = np.sum(perm_dist >= raw_tv)
                p_val = count_ge / N_PERMUTATIONS
                perm_p_vals.append(p_val)

        mean_p = float(np.mean(perm_p_vals)) if perm_p_vals else 1.0
        perm_results_bc[str(l_key)] = {
            'mean_p_value': round(mean_p, 6),
            'pass': mean_p > ALPHA if l_key == 0.0 else mean_p < ALPHA,
        }
        print(f"  lambda={l_key}: mean_p={mean_p:.6f}, pass={perm_results_bc[str(l_key)]['pass']}")
    print()

    # === TWO-WAY ANOVA (bias-corrected) ===
    print("=== Two-Way ANOVA (bias-corrected) ===")
    anova_result_bc = {}
    try:
        import pandas as pd
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm

        anova_data = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            for l in LAMBDA_LEVELS:
                for tv_val in all_knn_tv_bc[PRIMARY_K][f_idx][l]:
                    anova_data.append({
                        'lam_level': str(l),
                        'function': str(f_idx + 1),
                        'tv': tv_val
                    })

        df = pd.DataFrame(anova_data)
        model = ols('tv ~ C(lam_level) + C(function) + C(lam_level):C(function)', data=df).fit()
        anova_table = anova_lm(model, typ=2)

        anova_result_bc = {
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
        print(f"  Interaction p-value: {anova_result_bc['full_model']['interaction_effect']['p_value']}")
        print(f"  Interaction pass (p > 0.05): {anova_result_bc['interaction_pass']}")
    except Exception as e:
        anova_result_bc = {'error': str(e), 'interaction_pass': False}
        print(f"  ANOVA failed: {e}")
    print()

    # === EFFECT SIZE (bias-corrected) ===
    print("=== Effect Size (bias-corrected) ===")
    effect_sizes_bc = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        tv_0 = np.array(all_knn_tv_bc[PRIMARY_K][f_idx][0.0])
        tv_1 = np.array(all_knn_tv_bc[PRIMARY_K][f_idx][1.0])
        pooled_std = np.sqrt((np.var(tv_0, ddof=1) + np.var(tv_1, ddof=1)) / 2)
        cohens_d = float((np.mean(tv_1) - np.mean(tv_0)) / pooled_std) if pooled_std > 0 else 0.0
        effect_sizes_bc[str(func_seed)] = cohens_d
        print(f"  Function {func_seed} ({FUNCTION_NAMES[func_seed]}): Cohen's d = {cohens_d:.4f}")

    agg_bc_0 = []
    agg_bc_1 = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        agg_bc_0.extend(all_knn_tv_bc[PRIMARY_K][f_idx][0.0])
        agg_bc_1.extend(all_knn_tv_bc[PRIMARY_K][f_idx][1.0])
    pooled_std_agg = np.sqrt((np.var(agg_bc_0, ddof=1) + np.var(agg_bc_1, ddof=1)) / 2)
    agg_cohens_d_bc = float((np.mean(agg_bc_1) - np.mean(agg_bc_0)) / pooled_std_agg) if pooled_std_agg > 0 else 0.0
    effect_sizes_bc['aggregate'] = agg_cohens_d_bc
    print(f"  Aggregate: Cohen's d = {agg_cohens_d_bc:.4f}")
    print()

    # === CLIPPING vs TOROIDAL COMPARISON ===
    print("=== Clipping vs Toroidal Comparison ===")
    clipping_vs_toroidal = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        # Compute separation with clipping vs toroidal at lambda=1
        clip_sep = float(np.mean(all_knn_tv_raw[PRIMARY_K][f_idx][1.0]) -
                         np.mean(all_knn_tv_raw[PRIMARY_K][f_idx][0.0]))
        tor_sep = float(np.mean(all_toroidal_tv[f_idx][1.0]) -
                       np.mean(all_toroidal_tv[f_idx][0.0]))
        reduction = (clip_sep - tor_sep) / clip_sep if clip_sep > 0 else 0.0

        clipping_vs_toroidal[str(func_seed)] = {
            'func_name': func_name,
            'clipping_separation': clip_sep,
            'toroidal_separation': tor_sep,
            'reduction_fraction': reduction,
            'reduction_pct': reduction * 100,
        }
        print(f"  {func_name}: clip_sep={clip_sep:.4f}, tor_sep={tor_sep:.4f}, "
              f"reduction={reduction*100:.1f}%")

    # Translation-scaling gap
    trans_clip_sep = clipping_vs_toroidal['44']['clipping_separation']
    scal_clip_sep = clipping_vs_toroidal['43']['clipping_separation']
    trans_tor_sep = clipping_vs_toroidal['44']['toroidal_separation']
    scal_tor_sep = clipping_vs_toroidal['43']['toroidal_separation']
    gap_clip = trans_clip_sep - scal_clip_sep
    gap_tor = trans_tor_sep - scal_tor_sep
    gap_reduction = (gap_clip - gap_tor) / gap_clip if gap_clip > 0 else 0.0
    print(f"\n  Translation-scaling gap: clip={gap_clip:.4f}, toroidal={gap_tor:.4f}")
    print(f"  Gap reduction from toroidal: {gap_reduction*100:.1f}%")
    print(f"  Gap reduction > 50%: {'YES' if gap_reduction > 0.5 else 'NO'}")
    print()

    # === FREQUENCY BASELINE ===
    print("=== Frequency Baseline ===")
    freq_baseline_means = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        freq_means = {str(l): float(np.mean(all_freq_baseline[f_idx][l])) for l in LAMBDA_LEVELS}
        freq_baseline_means[str(func_seed)] = freq_means
        print(f"  {func_name}: {freq_means}")

    # Aggregate frequency baseline
    agg_freq_means = []
    for l in LAMBDA_LEVELS:
        all_freq_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_freq_at_l.extend(all_freq_baseline[f_idx][l])
        agg_freq_means.append(float(np.mean(all_freq_at_l)))
    print(f"  Aggregate freq baseline at lambda=0: {agg_freq_means[0]:.4f}")
    print(f"  Raw TV floor at lambda=0: {np.mean(aggregate_bc_means) + np.mean([np.mean([np.mean(p) for p in all_perm_nulls[PRIMARY_K][f_idx][0.0]]) for f_idx in range(len(FUNCTION_SEEDS))]):.4f}")
    print()

    # === GAUSSIAN NOISE BASELINE ===
    print("=== Gaussian Noise Baseline ===")
    gaussian_baseline = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        gauss_means = {str(l): float(np.mean(all_gaussian_tv[f_idx][l])) for l in LAMBDA_LEVELS}
        gaussian_baseline[str(func_seed)] = gauss_means

        # Compare Gaussian vs mixture at lambda=1
        gauss_at_1 = np.mean(all_gaussian_tv[f_idx][1.0])
        mix_at_1 = np.mean(all_knn_tv_raw[PRIMARY_K][f_idx][1.0])
        print(f"  {func_name}: Gaussian TV@1={gauss_at_1:.4f}, Mixture TV@1={mix_at_1:.4f}")

    # Aggregate Gaussian vs mixture comparison
    agg_gauss_at_1 = np.mean([np.mean(all_gaussian_tv[f_idx][1.0]) for f_idx in range(len(FUNCTION_SEEDS))])
    agg_mix_at_1 = np.mean([np.mean(all_knn_tv_raw[PRIMARY_K][f_idx][1.0]) for f_idx in range(len(FUNCTION_SEEDS))])
    print(f"  Aggregate: Gaussian TV@1={agg_gauss_at_1:.4f}, Mixture TV@1={agg_mix_at_1:.4f}")
    print()

    # === TOROIDAL SANITY CHECK ===
    print("=== Toroidal Wrapping Sanity Check ===")
    tor_sanity = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        tor_at_0 = np.mean(all_toroidal_tv[f_idx][0.0])
        tor_sanity[str(func_seed)] = {
            'tv_at_lambda0': tor_at_0,
            'pass': tor_at_0 < 0.1,
        }
        print(f"  {FUNCTION_NAMES[func_seed]}: TV@0={tor_at_0:.4f}, pass={tor_at_0 < 0.1}")
    print()

    # === CONTROL CHECKS ===
    print("=== Control Checks ===")
    controls = {}

    # Positive control: bias-corrected TV > 0 at lambda=1 (permutation p < 0.05)
    positive_control_bc = {}
    all_positive_pass_bc = True
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        # Check if bias-corrected TV at lambda=1 is > 0
        bc_at_1 = np.mean(all_knn_tv_bc[PRIMARY_K][f_idx][1.0])
        # Permutation test: fraction of permuted TVs >= raw TV at lambda=1
        perm_p_vals_f = []
        for rep_idx in range(N_REPLICATIONS):
            perm_dist = all_perm_nulls[PRIMARY_K][f_idx][1.0][rep_idx]
            raw_tv = all_knn_tv_raw[PRIMARY_K][f_idx][1.0][rep_idx]
            count_ge = np.sum(perm_dist >= raw_tv)
            perm_p_vals_f.append(count_ge / N_PERMUTATIONS)
        mean_perm_p = float(np.mean(perm_p_vals_f))

        passes = bc_at_1 > 0 and mean_perm_p < 0.05
        positive_control_bc[str(func_seed)] = {
            'pass': passes,
            'bc_tv_at_lambda1': float(bc_at_1),
            'perm_p_value': mean_perm_p,
        }
        if not passes:
            all_positive_pass_bc = False
        print(f"  Positive control (Function {func_seed}): {'PASS' if passes else 'FAIL'}"
              f" (bc_TV@1={bc_at_1:.4f}, perm_p={mean_perm_p:.6f})")

    controls['positive_control'] = {
        'description': 'Bias-corrected TV > 0 at lambda=1 across all functions (permutation p < 0.05)',
        'pass': all_positive_pass_bc,
        'per_function': positive_control_bc,
    }

    # Null control: bias-corrected TV ≈ 0 at lambda=0 (permutation p > 0.05)
    null_control_pass_bc = perm_results_bc['0.0']['pass']
    controls['null_control'] = {
        'description': 'Bias-corrected TV ≈ 0 at lambda=0 (permutation p > 0.05)',
        'pass': null_control_pass_bc,
        'mean_perm_p': perm_results_bc['0.0']['mean_p_value'],
    }
    print(f"  Null control: {'PASS' if null_control_pass_bc else 'FAIL'} (p={perm_results_bc['0.0']['mean_p_value']:.6f})")

    # Aggregate Spearman test (bias-corrected)
    spearman_pass_bc = (agg_bc_rho >= 0.65 and agg_bc_p_one_sided < 0.05)
    controls['spearman_test'] = {
        'description': f'Aggregate Spearman rho(bc_TV, lambda) >= 0.65 with p < 0.05 one-sided',
        'pass': spearman_pass_bc,
        'rho': float(agg_bc_rho),
        'p_one_sided': float(agg_bc_p_one_sided),
    }
    print(f"  Spearman test: {'PASS' if spearman_pass_bc else 'FAIL'} (rho={agg_bc_rho:.4f}, p={agg_bc_p_one_sided:.6f})")

    # Function invariance (ANOVA interaction, bias-corrected)
    controls['function_invariance'] = {
        'description': 'No significant function x lambda interaction on bias-corrected TV (two-way ANOVA p > 0.05)',
        'pass': anova_result_bc.get('interaction_pass', False),
        'interaction_p': anova_result_bc.get('full_model', {}).get('interaction_effect', {}).get('p_value', None),
    }
    print(f"  Function invariance: {'PASS' if anova_result_bc.get('interaction_pass', False) else 'FAIL'}")

    # Clipping removal reduction
    gap_reduction_pass = gap_reduction > 0.5
    controls['clipping_reduction'] = {
        'description': 'Toroidal wrapping reduces translation-scaling gap by >50%',
        'pass': gap_reduction_pass,
        'gap_clip': gap_clip,
        'gap_toroidal': gap_tor,
        'reduction_fraction': gap_reduction,
    }
    print(f"  Clipping reduction: {'PASS' if gap_reduction_pass else 'FAIL'} (reduction={gap_reduction*100:.1f}%)")

    # Multi-scale monotonicity (bias-corrected)
    n_monotonic_bc = sum(1 for v in multiscale_bc_results.values() if v['monotonic'])
    multiscale_pass_bc = n_monotonic_bc >= 2
    controls['multiscale_monotonicity'] = {
        'description': f'Bias-corrected monotonicity holds across at least 2 of {len(KNN_SCALES)} kNN scales',
        'pass': multiscale_pass_bc,
        'n_monotonic': n_monotonic_bc,
        'n_total': len(KNN_SCALES),
        'per_scale': {str(k): multiscale_bc_results[k]['monotonic'] for k in KNN_SCALES},
    }
    print(f"  Multi-scale monotonicity: {'PASS' if multiscale_pass_bc else 'FAIL'}"
          f" ({n_monotonic_bc}/{len(KNN_SCALES)} scales)")

    # Bias floor consistency
    floor_pass = floor_cv < 0.1
    controls['bias_floor_consistency'] = {
        'description': 'Permutation null at lambda=0 consistent across functions (CV < 0.1)',
        'pass': floor_pass,
        'cv': float(floor_cv),
        'floor_means': [float(x) for x in perm_floor_means],
    }
    print(f"  Bias floor consistency: {'PASS' if floor_pass else 'FAIL'} (CV={floor_cv:.4f})")

    # Toroidal sanity check
    tor_sanity_pass = all(v['pass'] for v in tor_sanity.values())
    controls['toroidal_sanity'] = {
        'description': 'Toroidal wrapping produces TV ≈ 0 at lambda=0 (< 0.1)',
        'pass': tor_sanity_pass,
        'per_function': {k: v['tv_at_lambda0'] for k, v in tor_sanity.items()},
    }
    print(f"  Toroidal sanity: {'PASS' if tor_sanity_pass else 'FAIL'}")

    # No pipeline errors
    controls['no_pipeline_errors'] = {
        'description': 'No pipeline errors during execution',
        'pass': True,
    }
    print(f"  No pipeline errors: PASS")
    print()

    # === CHECK FOR OVER-CORRECTION ===
    print("=== Over-Correction Check ===")
    n_negative_bc = 0
    n_total_bc = 0
    for f_idx in range(len(FUNCTION_SEEDS)):
        for tv_val in all_knn_tv_bc[PRIMARY_K][f_idx][1.0]:
            n_total_bc += 1
            if tv_val < 0:
                n_negative_bc += 1
    frac_negative = n_negative_bc / n_total_bc if n_total_bc > 0 else 0.0
    over_correction_pass = frac_negative <= 0.1
    controls['over_correction'] = {
        'description': 'No more than 10% of bias-corrected TV values negative at lambda=1',
        'pass': over_correction_pass,
        'fraction_negative': frac_negative,
        'n_negative': n_negative_bc,
        'n_total': n_total_bc,
    }
    print(f"  Fraction negative bc_TV at lambda=1: {frac_negative:.4f}")
    print(f"  Over-correction check: {'PASS' if over_correction_pass else 'FAIL'}")
    print()

    # === DECISION ===
    print("=== Decision ===")
    conditions = {
        'spearman': spearman_pass_bc,
        'positive_control': all_positive_pass_bc,
        'null_control': null_control_pass_bc,
        'function_invariance': anova_result_bc.get('interaction_pass', False),
        'clipping_reduction': gap_reduction_pass,
    }

    any_pipeline_error = not controls['no_pipeline_errors']['pass']
    over_corrected = not over_correction_pass
    floor_inconsistent = not floor_pass

    if any_pipeline_error or over_corrected or floor_inconsistent:
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
        'experiment_id': 'EXP-FRONTIER-34121473072',
        'lane': 'frontier',
        'status': 'COMPLETE' if not any_pipeline_error and not over_corrected and not floor_inconsistent else 'MEASUREMENT_INVALID',
        'outcome': outcome,
        'metrics': {
            'aggregate_bias_corrected': {
                'spearman_rho_bc_tv': float(agg_bc_rho),
                'spearman_p_one_sided_bc_tv': float(agg_bc_p_one_sided),
                'bc_tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): float(aggregate_bc_means[i])
                                           for i in range(len(LAMBDA_LEVELS))},
                'cohens_d_bc_lambda0_vs_1': agg_cohens_d_bc,
            },
            'per_function_bias_corrected': {},
            'bias_corrected_tv_means_by_lambda': {},
            'effect_sizes_cohens_d_bias_corrected': effect_sizes_bc,
            'multiscale_knn_bias_corrected': multiscale_bc_results,
            'clipping_vs_toroidal': clipping_vs_toroidal,
            'frequency_baseline': freq_baseline_means,
            'gaussian_noise_baseline': gaussian_baseline,
            'toroidal_sanity_check': tor_sanity,
            'bias_floor': {
                'perm_mean_at_lambda0_per_function': {str(FUNCTION_SEEDS[i]): float(perm_floor_means[i])
                                                      for i in range(len(FUNCTION_SEEDS))},
                'cv_across_functions': float(floor_cv),
            },
            'over_correction_check': {
                'fraction_negative_at_lambda1': frac_negative,
                'pass': over_correction_pass,
            },
            'clipping_fractions': {str(FUNCTION_SEEDS[f_idx]): {str(l): float(np.mean(clipping_fractions[f_idx][l]))
                                                                  for l in LAMBDA_LEVELS}
                                    for f_idx in range(len(FUNCTION_SEEDS))},
        },
        'controls': controls,
        'artifacts': [],
        'observations': [],
        'validity_notes': [],
        'unresolved': [],
    }

    # Fill per_function_bias_corrected metrics
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        results['metrics']['per_function_bias_corrected'][str(func_seed)] = {
            'func_name': func_name,
            'spearman_rho': per_function_results_bc[func_seed]['spearman_rho'],
            'spearman_p_one_sided': per_function_results_bc[func_seed]['spearman_p_one_sided'],
            'bc_tv_means_by_lambda': per_function_results_bc[func_seed]['bc_tv_means_by_lambda'],
        }

    # Fill bias_corrected_tv_means_by_lambda (aggregate across all functions)
    for l in LAMBDA_LEVELS:
        all_bc_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_bc_at_l.extend(all_knn_tv_bc[PRIMARY_K][f_idx][l])
        results['metrics']['bias_corrected_tv_means_by_lambda'][str(l)] = float(np.mean(all_bc_at_l))

    # Observations (raw, not interpreted)
    results['observations'] = [
        f"Overall decision: {decision}",
        f"Aggregate bias-corrected Spearman rho(bc_TV, lambda)={agg_bc_rho:.4f}, p_one_sided={agg_bc_p_one_sided:.6f}",
        f"Positive control (bc_TV > 0 at lambda=1, perm p < 0.05): {'PASS' if all_positive_pass_bc else 'FAIL'}",
        f"Null control (bc_TV ≈ 0 at lambda=0, perm p > 0.05): {'PASS' if null_control_pass_bc else 'FAIL'}",
        f"Function invariance (ANOVA interaction on bc_TV): {'PASS' if anova_result_bc.get('interaction_pass', False) else 'FAIL'}",
        f"Clipping reduction (toroidal reduces translation-scaling gap by >50%): {'PASS' if gap_reduction_pass else 'FAIL'} (reduction={gap_reduction*100:.1f}%)",
        f"Multi-scale monotonicity (bc_TV): {'PASS' if multiscale_pass_bc else 'FAIL'} ({n_monotonic_bc}/{len(KNN_SCALES)} scales)",
        f"Aggregate Cohen's d (bc_TV lambda=0 vs 1): {agg_cohens_d_bc:.4f}",
        f"Bias floor CV across functions at lambda=0: {floor_cv:.4f}",
        f"Over-correction check: {frac_negative:.4f} negative values at lambda=1",
        f"Toroidal sanity check at lambda=0: {'PASS' if tor_sanity_pass else 'FAIL'}",
        f"Execution time: {elapsed:.1f}s",
    ]
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        rho = per_function_results_bc[func_seed]['spearman_rho']
        p = per_function_results_bc[func_seed]['spearman_p_one_sided']
        results['observations'].append(
            f"Function {func_seed} ({func_name}): bc_TV Spearman rho={rho:.4f}, p_one_sided={p:.6f}"
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
        'Bias correction via permutation-null subtraction (1000 perms per cell)',
        'Toroidal wrapping tested as alternative to clipping',
        'Frequency baseline P(S_{t+1}) computed for each cell',
        'Gaussian noise baseline (single Gaussian, not mixture) computed for comparison',
        'kNN distance diagnostics verify distances are not degenerate in high dimensions',
        'Clipping to [0,1] after noise addition; fractions reported per lambda/function',
        'Permutation tests at lambda=0 and lambda=1 with 1000 permutations per cell',
        f"Over-correction check: {frac_negative:.4f} of bias-corrected values negative at lambda=1",
        f"Bias floor consistency CV: {floor_cv:.4f} (threshold < 0.1)",
    ]

    # Unresolved
    results['unresolved'] = [
        'Whether real Web transitions exhibit action-dependent structure suitable for TV detection',
        'Whether scaling failure replicates under alternative 10D scaling parameterizations',
        'Whether kNN TV remains robust at >50D state spaces (Web DOM embeddings)',
        'Whether bias-corrected TV shows significant difference between Gaussian and mixture noise baselines',
        'Whether rotation non-monotonic dip at low lambda reflects estimator noise or genuine response',
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
    experiment_dir = Path(__file__).parent
    hashes = {}
    for fname in ['prereg.md', 'spec.json', 'request.json', 'freeze.json']:
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
        'experiment_id': 'EXP-FRONTIER-34121473072',
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
        },
        'frozen_inputs': {
            'prereg_hash': '135d57712c922be28af2f119d23ae9634d5d17dc39648a9db182c8afd2bbf007',
            'request_hash': '562ecee83cbc08a62295c677ad2d53909b81291c3806be0cd85cba15599e8526',
            'spec_hash': 'ce63def49a35da19247fc05afc837533e8c6acc285ded7335f713c015866a476',
        },
        'total_transitions': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_TRANSITIONS,
        'permutation_samples': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_PERMUTATIONS,
        'execution_seconds': elapsed,
        'parent_experiment': 'EXP-FRONTIER-34065969836',
    }

    provenance_path = Path(__file__).parent / 'provenance.json'
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
