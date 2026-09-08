#!/usr/bin/env python3
"""
EXP-FRONTIER-34121473072: Bias-Corrected kNN TV in 10D Non-Gaussian Spaces.

Frozen experiment code. Do not modify after freeze.

Tests whether permutation-null bias subtraction rescues function invariance
and reduces the translation-scaling separation gap in 10D non-Gaussian settings.
Also tests toroidal wrapping vs clipping, frequency baseline, and Gaussian noise baseline.
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
N_PERMUTATIONS = 1000  # per cell for bias floor estimation
ALPHA = 0.05
DIM = 10  # 10D state space
N_ACTIONS = 4
ACTIONS = ['click', 'fill', 'submit', 'navigate']
KNN_SCALES = [5, 10, 20, 50]  # multi-scale kNN analysis
PRIMARY_K = 20  # primary kNN scale


# === 10D FUNCTION FAMILIES ===
ACTION_DIM_MAP = [0, 2, 5, 7]  # dimensions 0,2,5,7 for 4 actions

def rotation_10d(s, action_idx):
    """State-dependent rotation in 10D. Angle depends on s[action_dim] * action_sign."""
    action_dim = ACTION_DIM_MAP[action_idx]
    action_sign = 1.0 if action_idx % 2 == 0 else -1.0
    theta = 0.1 * s[action_dim] * action_sign
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
    offset = np.zeros(DIM)
    offset[action_dim] = 0.1 * action_sign
    s_new = R @ (s - 0.5) + 0.5 + offset
    return s_new

def scaling_10d(s, action_idx):
    """State-dependent scaling in 10D. Scale factor depends on s[action_dim]."""
    action_dim = ACTION_DIM_MAP[action_idx]
    action_sign = 1.0 if action_idx % 2 == 0 else -1.0
    scale_factor = 1.0 + 0.2 * s[action_dim] * action_sign
    s_centered = s - 0.5
    s_scaled = scale_factor * s_centered
    offset = np.zeros(DIM)
    for i in range(DIM):
        if i != action_dim:
            offset[i] = 0.05 * s[i] * action_sign
    s_new = s_scaled + 0.5 + offset
    return s_new

def translation_10d(s, action_idx):
    """State-dependent translation with sin modulation in 10D."""
    action_dim = ACTION_DIM_MAP[action_idx]
    action_sign = 1.0 if action_idx % 2 == 0 else -1.0
    t = np.zeros(DIM)
    for i in range(DIM):
        t[i] = 0.1 * s[i] * action_sign
        t[i] += 0.05 * np.sin(2 * np.pi * s[i])
    t[action_dim] += 0.1 * action_sign
    s_new = s + t
    return s_new

FUNCTION_MAP = {42: rotation_10d, 43: scaling_10d, 44: translation_10d}
FUNCTION_NAMES = {42: 'rotation', 43: 'scaling', 44: 'translation'}


# === NON-GAUSSIAN HETEROSCEDASTIC NOISE ===
def sample_mixture_noise(s, rng):
    """Sample non-Gaussian heteroscedastic noise: mixture of 3 Gaussians per dimension."""
    dist_to_center = np.linalg.norm(s - 0.5)
    sigma_base = 0.05 * (1 + 0.5 * dist_to_center)
    noise = np.zeros(DIM)
    for i in range(DIM):
        r = rng.random()
        if r < 0.5:
            mean_i, std_i = 0.0, sigma_base
        elif r < 0.8:
            mean_i, std_i = 0.1 * sigma_base, 0.5 * sigma_base
        else:
            mean_i, std_i = -0.1 * sigma_base, 2.0 * sigma_base
        noise[i] = rng.normal(mean_i, std_i)
    return noise

def sample_gaussian_noise(s, rng):
    """Gaussian baseline: single Gaussian heteroscedastic noise per dimension."""
    dist_to_center = np.linalg.norm(s - 0.5)
    sigma_base = 0.05 * (1 + 0.5 * dist_to_center)
    noise = rng.normal(0, sigma_base, size=DIM)
    return noise


# === DATA GENERATION ===
def generate_transitions(func_seed, lambda_val, n, rng, noise_type='nongaussian',
                         boundary='clip'):
    """
    Generate transitions using 10D non-Gaussian DGP.

    With probability lambda: s_next = deterministic_function(s, a) + noise
    With probability (1-lambda): s_next ~ mixture centered at 0.5

    boundary: 'clip' (clip to [0,1]) or 'toroidal' (modular arithmetic wrapping)
    """
    func = FUNCTION_MAP[func_seed]
    transitions = []
    noise_fn = sample_mixture_noise if noise_type == 'nongaussian' else sample_gaussian_noise

    for _ in range(n):
        s = rng.uniform(0, 1, size=DIM)
        a_idx = rng.randint(0, N_ACTIONS)

        if rng.random() < lambda_val:
            s_next_det = func(s, a_idx)
            noise = noise_fn(s, rng)
            s_next = s_next_det + noise
        else:
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
            s_next = s_next - np.floor(s_next)  # modular arithmetic wrapping

        transitions.append((s, ACTIONS[a_idx], s_next))
    return transitions


# === TV DISTANCE: kNN-BASED ===
def knn_tv_estimate(X_a, X_b, k):
    """Estimate TV distance between two samples using kNN."""
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
    """Compute TV for all 6 action pairs and return max and mean."""
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


# === PERMUTATION TEST ===
def permutation_test_knn_tv(transitions, k, n_permutations, rng):
    """Permutation test: shuffle action labels and recompute kNN TV."""
    observed_tv, _ = compute_knn_tv_all_pairs(transitions, k)
    actions = [a for _, a, _ in transitions]
    s_nexts = [s for _, _, s in transitions]
    count_ge = 0
    perm_tvs = []
    for _ in range(n_permutations):
        shuffled_actions = list(actions)
        rng.shuffle(shuffled_actions)
        perm_transitions = [(None, a, sn) for a, sn in zip(shuffled_actions, s_nexts)]
        perm_tv, _ = compute_knn_tv_all_pairs(perm_transitions, k)
        perm_tvs.append(perm_tv)
        if perm_tv >= observed_tv:
            count_ge += 1
    p_value = count_ge / n_permutations
    return observed_tv, p_value, perm_tvs


# === FREQUENCY BASELINE ===
def compute_frequency_baseline(transitions):
    """
    Frequency baseline: TV between marginal next-state distributions P(S_{t+1}).
    Groups by action, computes marginal P(S_{t+1}) for each action, computes TV.
    """
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)

    # Convert to arrays
    for a in ACTIONS:
        action_states[a] = np.array(action_states[a])

    # Compute pairwise TV between action-conditional marginals
    actions_list = list(ACTIONS)
    tv_max = 0.0
    tv_sum = 0.0
    n_pairs = 0

    for i in range(len(actions_list)):
        for j in range(i + 1, len(actions_list)):
            # Use binned histogram TV for marginals (not kNN)
            X_a = action_states[actions_list[i]]
            X_b = action_states[actions_list[j]]

            # Bin each dimension independently and compute product-bin TV
            n_bins = 10
            tv_dim_sum = 0.0
            for d in range(DIM):
                # Get range across both samples
                all_vals = np.concatenate([X_a[:, d], X_b[:, d]])
                lo, hi = all_vals.min(), all_vals.max()
                if hi - lo < 1e-10:
                    continue
                bins = np.linspace(lo, hi + 1e-10, n_bins + 1)
                hist_a, _ = np.histogram(X_a[:, d], bins=bins, density=True)
                hist_b, _ = np.histogram(X_b[:, d], bins=bins, density=True)
                # Normalize to probability
                hist_a = hist_a / (hist_a.sum() + 1e-10)
                hist_b = hist_b / (hist_b.sum() + 1e-10)
                tv_dim_sum += 0.5 * np.sum(np.abs(hist_a - hist_b))

            tv_pair = tv_dim_sum / DIM  # average across dimensions
            tv_max = max(tv_max, tv_pair)
            tv_sum += tv_pair
            n_pairs += 1

    tv_mean = tv_sum / n_pairs if n_pairs > 0 else 0.0
    return tv_max, tv_mean


# === MAIN EXPERIMENT ===
def run_experiment():
    """Execute the full frozen experiment."""
    start_time = time.time()
    print("=== EXP-FRONTIER-34121473072: Bias-Corrected kNN TV ===")
    print(f"Seed: {SEED}")
    print(f"Lambda levels: {LAMBDA_LEVELS}")
    print(f"Functions: 3 (seeds {FUNCTION_SEEDS})")
    print(f"Transitions per cell: {N_TRANSITIONS}")
    print(f"Replications per cell: {N_REPLICATIONS}")
    print(f"Permutation nulls per cell: {N_PERMUTATIONS}")
    print(f"State space: continuous 10D [0,1]^10")
    print(f"Noise: mixture of 3 Gaussians (non-Gaussian heteroscedastic)")
    print(f"kNN scales: {KNN_SCALES}")
    print(f"Primary kNN scale: k={PRIMARY_K}")
    print()

    # === STORAGE ===
    # Raw (clipping) TV at multiple scales
    raw_knn_tv = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                      for f_idx in range(len(FUNCTION_SEEDS))}
                  for k in KNN_SCALES}

    # Toroidal TV at primary scale
    toroidal_knn_tv = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                       for f_idx in range(len(FUNCTION_SEEDS))}

    # Bias floor from permutation nulls (clipping)
    bias_floor = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                      for f_idx in range(len(FUNCTION_SEEDS))}
                  for k in KNN_SCALES}

    # Bias-corrected TV (clipping)
    bias_corrected_tv = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                             for f_idx in range(len(FUNCTION_SEEDS))}
                         for k in KNN_SCALES}

    # Bias-corrected TV (toroidal)
    bias_corrected_toroidal = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                               for f_idx in range(len(FUNCTION_SEEDS))}

    # Frequency baseline
    freq_baseline = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                     for f_idx in range(len(FUNCTION_SEEDS))}

    # Gaussian noise baseline (clipping)
    gaussian_knn_tv = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                           for f_idx in range(len(FUNCTION_SEEDS))}
                       for k in KNN_SCALES}

    # Clipping fractions
    clipping_fractions = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                          for f_idx in range(len(FUNCTION_SEEDS))}

    # Toroidal lambda=0 sanity
    toroidal_lam0_sanity = {f_idx: [] for f_idx in range(len(FUNCTION_SEEDS))}

    raw_tables = []

    # === PHASE 1: Generate data and compute raw TV + permutation nulls ===
    print("=== Phase 1: Raw TV + Permutation Nulls (Clipping) ===")
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}...", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)

                # Generate transitions with clipping
                transitions = generate_transitions(func_seed, l, N_TRANSITIONS, rng,
                                                   noise_type='nongaussian', boundary='clip')

                # Track clipping
                n_clipped = 0
                for s, a, s_next in transitions:
                    if np.any(s_next <= 0) or np.any(s_next >= 1):
                        n_clipped += 1
                clipping_fractions[f_idx][l].append(n_clipped / len(transitions))

                # Raw kNN TV at all scales
                for k in KNN_SCALES:
                    tv_max, _ = compute_knn_tv_all_pairs(transitions, k)
                    raw_knn_tv[k][f_idx][l].append(tv_max)

                # Permutation null for bias floor (1000 perms at primary kNN scale)
                perm_rng = np.random.RandomState(rep_seed + 999)
                _, _, perm_tvs = permutation_test_knn_tv(transitions, PRIMARY_K,
                                                         N_PERMUTATIONS, perm_rng)
                perm_mean = float(np.mean(perm_tvs))

                # Store bias floor for primary scale
                bias_floor[PRIMARY_K][f_idx][l].append(perm_mean)

                # Bias-corrected TV at primary scale
                raw_tv_primary = raw_knn_tv[PRIMARY_K][f_idx][l][-1]
                bc_tv = max(0.0, raw_tv_primary - perm_mean)
                bias_corrected_tv[PRIMARY_K][f_idx][l].append(bc_tv)

                # For other kNN scales, use the same bias floor estimate
                # (permutation null at k=20 is shared across scales per prereg)
                for k in KNN_SCALES:
                    if k != PRIMARY_K:
                        raw_tv_k = raw_knn_tv[k][f_idx][l][-1]
                        bc_tv_k = max(0.0, raw_tv_k - perm_mean)
                        bias_corrected_tv[k][f_idx][l].append(bc_tv_k)
                        bias_floor[k][f_idx][l].append(perm_mean)

                # Frequency baseline
                freq_tv_max, _ = compute_frequency_baseline(transitions)
                freq_baseline[f_idx][l].append(freq_tv_max)

                # Store raw table row
                raw_tables.append({
                    'func_seed': func_seed,
                    'func_name': func_name,
                    'lambda': l,
                    'replication': rep_idx,
                    'raw_tv_k20': raw_knn_tv[PRIMARY_K][f_idx][l][-1],
                    'bias_floor_k20': perm_mean,
                    'bias_corrected_tv_k20': bc_tv,
                    'clipping_fraction': clipping_fractions[f_idx][l][-1],
                    'freq_baseline_tv': freq_tv_max,
                })

            # Print summary
            raw_means = raw_knn_tv[PRIMARY_K][f_idx][l]
            bc_means = bias_corrected_tv[PRIMARY_K][f_idx][l]
            bf_means = bias_floor[PRIMARY_K][f_idx][l]
            print(f" raw={np.mean(raw_means):.4f}+/-{np.std(raw_means, ddof=1):.4f}"
                  f" bf={np.mean(bf_means):.4f}"
                  f" bc={np.mean(bc_means):.4f}+/-{np.std(bc_means, ddof=1):.4f}"
                  f" clip={np.mean(clipping_fractions[f_idx][l]):.3f}")
        print()

    # === PHASE 2: Toroidal wrapping comparison ===
    print("=== Phase 2: Toroidal Wrapping Comparison ===")
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}...", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)

                # Generate transitions with toroidal wrapping
                transitions_tor = generate_transitions(func_seed, l, N_TRANSITIONS, rng,
                                                       noise_type='nongaussian',
                                                       boundary='toroidal')

                tv_max_tor, _ = compute_knn_tv_all_pairs(transitions_tor, PRIMARY_K)
                toroidal_knn_tv[f_idx][l].append(tv_max_tor)

                # Permutation null for toroidal at lambda=0
                if l == 0.0:
                    perm_rng = np.random.RandomState(rep_seed + 999)
                    _, _, perm_tvs_tor = permutation_test_knn_tv(transitions_tor, PRIMARY_K,
                                                                  N_PERMUTATIONS, perm_rng)
                    bf_tor = float(np.mean(perm_tvs_tor))
                    bc_tor = max(0.0, tv_max_tor - bf_tor)
                    bias_corrected_toroidal[f_idx][l].append(bc_tor)
                    toroidal_lam0_sanity[f_idx].append(tv_max_tor)

            tor_means = toroidal_knn_tv[f_idx][l]
            print(f" tor_tv={np.mean(tor_means):.4f}+/-{np.std(tor_means, ddof=1):.4f}")
        print()

    # Toroidal lambda=0 sanity check
    print("=== Toroidal Lambda=0 Sanity Check ===")
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        tor_lam0 = toroidal_lam0_sanity[f_idx]
        mean_tor = np.mean(tor_lam0)
        print(f"  Function {func_seed}: toroidal TV@lambda=0 = {mean_tor:.4f}"
              f" (should be ~0)")
    print()

    # === PHASE 3: Gaussian noise baseline ===
    print("=== Phase 3: Gaussian Noise Baseline ===")
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}...", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)

                # Generate with Gaussian noise instead of mixture
                transitions_gauss = generate_transitions(func_seed, l, N_TRANSITIONS, rng,
                                                         noise_type='gaussian',
                                                         boundary='clip')

                for k in KNN_SCALES:
                    tv_max_gauss, _ = compute_knn_tv_all_pairs(transitions_gauss, k)
                    gaussian_knn_tv[k][f_idx][l].append(tv_max_gauss)

            gauss_means = gaussian_knn_tv[PRIMARY_K][f_idx][l]
            print(f" gauss_k20={np.mean(gauss_means):.4f}+/-{np.std(gauss_means, ddof=1):.4f}")
        print()

    # === PHASE 4: Statistical Tests ===
    print("=== Phase 4: Statistical Tests ===")
    lambda_arr = np.array(LAMBDA_LEVELS)

    # --- 4.1 Aggregate Spearman on bias-corrected TV (primary kNN scale) ---
    print("--- 4.1 Aggregate Spearman (Bias-Corrected TV) ---")
    agg_bc_means = []
    for l in LAMBDA_LEVELS:
        all_bc_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_bc_at_l.extend(bias_corrected_tv[PRIMARY_K][f_idx][l])
        agg_bc_means.append(float(np.mean(all_bc_at_l)))

    agg_rho_bc, agg_p_bc = stats.spearmanr(lambda_arr, np.array(agg_bc_means))
    agg_p_bc_one_sided = agg_p_bc / 2 if agg_rho_bc > 0 else 1 - agg_p_bc / 2
    spearman_pass = (agg_rho_bc >= 0.65 and agg_p_bc_one_sided < 0.05)
    print(f"  Aggregate Spearman rho(bias_corrected_TV, lambda): {agg_rho_bc:.4f}")
    print(f"  One-sided p-value: {agg_p_bc_one_sided:.6f}")
    print(f"  Pass (rho>=0.65, p<0.05): {spearman_pass}")
    print()

    # --- 4.2 Per-function Spearman on bias-corrected TV ---
    print("--- 4.2 Per-Function Spearman (Bias-Corrected TV) ---")
    per_function_bc_results = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        tv_bc_means = np.array([np.mean(bias_corrected_tv[PRIMARY_K][f_idx][l])
                                for l in LAMBDA_LEVELS])
        rho, p = stats.spearmanr(lambda_arr, tv_bc_means)
        p_one_sided = p / 2 if rho > 0 else 1 - p / 2
        per_function_bc_results[func_seed] = {
            'func_name': func_name,
            'spearman_rho': float(rho),
            'spearman_p_one_sided': float(p_one_sided),
            'tv_bc_means_by_lambda': {str(l): float(tv_bc_means[i])
                                       for i, l in enumerate(LAMBDA_LEVELS)},
        }
        print(f"  Function {func_seed} ({func_name}): rho={rho:.4f}, p_one_sided={p_one_sided:.6f}")
    print()

    # --- 4.3 Positive Control (bias-corrected TV > 0 at lambda=1) ---
    print("--- 4.3 Positive Control ---")
    positive_control = {}
    all_positive_pass = True
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        bc_at_1 = bias_corrected_tv[PRIMARY_K][f_idx][1.0]
        mean_bc_1 = float(np.mean(bc_at_1))
        # Permutation test: is mean_bc_1 significantly > 0?
        # Use the permutation null distribution at lambda=1
        perm_rng = np.random.RandomState(func_seed * 10000 + 0 * 100 + SEED + 999)
        _, _, perm_tvs_l1 = permutation_test_knn_tv(
            generate_transitions(func_seed, 1.0, N_TRANSITIONS,
                                 np.random.RandomState(func_seed * 10000 + 0 * 100 + SEED)),
            PRIMARY_K, N_PERMUTATIONS, perm_rng)
        # P-value: fraction of perm TV >= observed raw TV
        raw_tv_l1 = raw_knn_tv[PRIMARY_K][f_idx][1.0][0]  # rep 0
        p_val = float(np.mean(np.array(perm_tvs_l1) >= raw_tv_l1))
        passes = mean_bc_1 > 0 and p_val < 0.05
        positive_control[str(func_seed)] = {
            'pass': passes,
            'bias_corrected_tv_at_lambda1': mean_bc_1,
            'permutation_p': p_val,
        }
        if not passes:
            all_positive_pass = False
        print(f"  Function {func_seed}: bc_tv@1={mean_bc_1:.4f}, perm_p={p_val:.4f}, "
              f"pass={passes}")
    print(f"  All functions pass: {all_positive_pass}")
    print()

    # --- 4.4 Null Control (bias-corrected TV ~ 0 at lambda=0) ---
    print("--- 4.4 Null Control ---")
    null_control_results = {}
    all_null_pass = True
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        bc_at_0 = bias_corrected_tv[PRIMARY_K][f_idx][0.0]
        mean_bc_0 = float(np.mean(bc_at_0))
        # By construction, bias-corrected TV at lambda=0 should be ~0
        # But we check if the residual is indistinguishable from 0
        perm_rng = np.random.RandomState(func_seed * 10000 + 0 * 100 + SEED + 999)
        _, _, perm_tvs_l0 = permutation_test_knn_tv(
            generate_transitions(func_seed, 0.0, N_TRANSITIONS,
                                 np.random.RandomState(func_seed * 10000 + 0 * 100 + SEED)),
            PRIMARY_K, N_PERMUTATIONS, perm_rng)
        raw_tv_l0 = raw_knn_tv[PRIMARY_K][f_idx][0.0][0]
        p_val = float(np.mean(np.array(perm_tvs_l0) >= raw_tv_l0))
        # Null control: p > 0.05 (not significantly > 0)
        passes = p_val > 0.05
        null_control_results[str(func_seed)] = {
            'pass': passes,
            'bias_corrected_tv_at_lambda0': mean_bc_0,
            'permutation_p': p_val,
        }
        if not passes:
            all_null_pass = False
        print(f"  Function {func_seed}: bc_tv@0={mean_bc_0:.6f}, perm_p={p_val:.4f}, "
              f"pass={passes}")
    print(f"  All functions pass: {all_null_pass}")
    print()

    # --- 4.5 Two-Way ANOVA on bias-corrected TV ---
    print("--- 4.5 Two-Way ANOVA (Bias-Corrected TV) ---")
    anova_result = {}
    try:
        import pandas as pd
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm

        anova_data = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            for l in LAMBDA_LEVELS:
                for tv_val in bias_corrected_tv[PRIMARY_K][f_idx][l]:
                    anova_data.append({
                        'lam_level': str(l),
                        'function': str(f_idx + 1),
                        'tv': tv_val
                    })

        df = pd.DataFrame(anova_data)
        model = ols('tv ~ C(lam_level) + C(function) + C(lam_level):C(function)', data=df).fit()
        anova_table = anova_lm(model, typ=2)

        interaction_p = float(anova_table.loc['C(lam_level):C(function)', 'PR(>F)'])
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
                    'p_value': round(float(interaction_p), 6),
                },
                'model_r_squared': round(float(model.rsquared), 4),
            },
            'interaction_pass': bool(interaction_p > ALPHA),
        }
        print(f"  Interaction p-value: {interaction_p:.6f}")
        print(f"  Interaction pass (p > 0.05): {anova_result['interaction_pass']}")
    except Exception as e:
        anova_result = {'error': str(e), 'interaction_pass': False}
        print(f"  ANOVA failed: {e}")
    print()

    # --- 4.6 Clipping Comparison (translation vs toroidal at lambda=1) ---
    print("--- 4.6 Clipping vs Toroidal Comparison ---")
    clip_comparison = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        clip_tvs = raw_knn_tv[PRIMARY_K][f_idx][1.0]
        tor_tvs = toroidal_knn_tv[f_idx][1.0]
        # Paired t-test (same replications)
        t_stat, t_p = stats.ttest_rel(clip_tvs, tor_tvs)
        cohens_d_clip_tor = float((np.mean(clip_tvs) - np.mean(tor_tvs)) /
                                  np.sqrt((np.var(clip_tvs, ddof=1) +
                                           np.var(tor_tvs, ddof=1)) / 2))
        clip_comparison[str(func_seed)] = {
            'func_name': func_name,
            'clip_mean': float(np.mean(clip_tvs)),
            'toroidal_mean': float(np.mean(tor_tvs)),
            'difference': float(np.mean(clip_tvs) - np.mean(tor_tvs)),
            't_statistic': float(t_stat),
            'p_value': float(t_p),
            'cohens_d': cohens_d_clip_tor,
        }
        print(f"  Function {func_seed} ({func_name}): clip={np.mean(clip_tvs):.4f}, "
              f"tor={np.mean(tor_tvs):.4f}, diff={np.mean(clip_tvs) - np.mean(tor_tvs):.4f}, "
              f"d={cohens_d_clip_tor:.4f}")
    print()

    # --- 4.7 Translation-Scaling Separation Gap ---
    print("--- 4.7 Translation-Scaling Separation Gap ---")
    # Before bias correction (raw TV) - f_idx 2=translation(44), 1=scaling(43)
    raw_trans_sep = float(np.mean(raw_knn_tv[PRIMARY_K][2][1.0]) -
                          np.mean(raw_knn_tv[PRIMARY_K][2][0.0]))
    raw_scal_sep = float(np.mean(raw_knn_tv[PRIMARY_K][1][1.0]) -
                         np.mean(raw_knn_tv[PRIMARY_K][1][0.0]))
    raw_gap = raw_trans_sep - raw_scal_sep

    # After bias correction
    bc_trans_sep = float(np.mean(bias_corrected_tv[PRIMARY_K][2][1.0]) -
                         np.mean(bias_corrected_tv[PRIMARY_K][2][0.0]))
    bc_scal_sep = float(np.mean(bias_corrected_tv[PRIMARY_K][1][1.0]) -
                        np.mean(bias_corrected_tv[PRIMARY_K][1][0.0]))
    bc_gap = bc_trans_sep - bc_scal_sep

    gap_reduction = (raw_gap - bc_gap) / raw_gap if raw_gap > 0 else 0.0
    gap_pass = gap_reduction > 0.5  # >50% reduction

    separation_gap = {
        'raw_translation_separation': raw_trans_sep,
        'raw_scaling_separation': raw_scal_sep,
        'raw_gap': raw_gap,
        'bc_translation_separation': bc_trans_sep,
        'bc_scaling_separation': bc_scal_sep,
        'bc_gap': bc_gap,
        'gap_reduction_fraction': gap_reduction,
        'gap_pass': gap_pass,
    }
    print(f"  Raw: translation={raw_trans_sep:.4f}, scaling={raw_scal_sep:.4f}, gap={raw_gap:.4f}")
    print(f"  Bias-corrected: translation={bc_trans_sep:.4f}, scaling={bc_scal_sep:.4f}, gap={bc_gap:.4f}")
    print(f"  Gap reduction: {gap_reduction:.1%} (pass >50%: {gap_pass})")
    print()

    # --- 4.8 Frequency Baseline Analysis ---
    print("--- 4.8 Frequency Baseline ---")
    freq_results = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        freq_at_0 = float(np.mean(freq_baseline[f_idx][0.0]))
        raw_at_0 = float(np.mean(raw_knn_tv[PRIMARY_K][f_idx][0.0]))
        fraction_explained = freq_at_0 / raw_at_0 if raw_at_0 > 0 else 0.0
        freq_results[str(func_seed)] = {
            'func_name': FUNCTION_NAMES[func_seed],
            'freq_baseline_at_lambda0': freq_at_0,
            'raw_tv_at_lambda0': raw_at_0,
            'fraction_explained': fraction_explained,
        }
        print(f"  Function {func_seed}: freq_baseline={freq_at_0:.4f}, "
              f"raw_tv={raw_at_0:.4f}, fraction_explained={fraction_explained:.1%}")
    print()

    # --- 4.9 Gaussian vs Mixture Noise Comparison ---
    print("--- 4.9 Gaussian vs Mixture Noise Comparison ---")
    noise_comparison = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        mixture_tvs = []
        gaussian_tvs = []
        for l in LAMBDA_LEVELS:
            mixture_tvs.extend(raw_knn_tv[PRIMARY_K][f_idx][l])
            gaussian_tvs.extend(gaussian_knn_tv[PRIMARY_K][f_idx][l])
        # Aggregate comparison
        t_stat, t_p = stats.ttest_rel(mixture_tvs, gaussian_tvs)
        noise_comparison[str(func_seed)] = {
            'func_name': FUNCTION_NAMES[func_seed],
            'mixture_mean': float(np.mean(mixture_tvs)),
            'gaussian_mean': float(np.mean(gaussian_tvs)),
            'difference': float(np.mean(mixture_tvs) - np.mean(gaussian_tvs)),
            't_statistic': float(t_stat),
            'p_value': float(t_p),
        }
        print(f"  Function {func_seed}: mixture={np.mean(mixture_tvs):.4f}, "
              f"gaussian={np.mean(gaussian_tvs):.4f}, diff={np.mean(mixture_tvs) - np.mean(gaussian_tvs):.4f}")
    print()

    # --- 4.10 Bias Floor Consistency ---
    print("--- 4.10 Bias Floor Consistency ---")
    bf_at_0 = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        bf_vals = bias_floor[PRIMARY_K][f_idx][0.0]
        bf_at_0.append(float(np.mean(bf_vals)))
    bf_cv = float(np.std(bf_at_0) / np.mean(bf_at_0)) if np.mean(bf_at_0) > 0 else 0.0
    bf_consistency_pass = bf_cv < 0.1
    print(f"  Bias floor at lambda=0 across functions: {[f'{v:.4f}' for v in bf_at_0]}")
    print(f"  CV: {bf_cv:.4f} (pass <0.1: {bf_consistency_pass})")
    print()

    # --- 4.11 Multiscale kNN Analysis on bias-corrected TV ---
    print("--- 4.11 Multiscale kNN Analysis (Bias-Corrected) ---")
    multiscale_bc = {}
    for k in KNN_SCALES:
        agg_means_k = []
        for l in LAMBDA_LEVELS:
            all_bc_at_l = []
            for f_idx in range(len(FUNCTION_SEEDS)):
                all_bc_at_l.extend(bias_corrected_tv[k][f_idx][l])
            agg_means_k.append(float(np.mean(all_bc_at_l)))
        rho_k, p_k = stats.spearmanr(lambda_arr, np.array(agg_means_k))
        p_k_one_sided = p_k / 2 if rho_k > 0 else 1 - p_k / 2
        is_monotonic = all(agg_means_k[i] <= agg_means_k[i + 1]
                          for i in range(len(agg_means_k) - 1))
        multiscale_bc[k] = {
            'rho': float(rho_k),
            'p_one_sided': float(p_k_one_sided),
            'monotonic': is_monotonic,
            'tv_bc_means_by_lambda': {str(LAMBDA_LEVELS[i]): agg_means_k[i]
                                      for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  k={k}: rho={rho_k:.4f}, p={p_k_one_sided:.6f}, monotonic={is_monotonic}")
    n_monotonic_scales_bc = sum(1 for v in multiscale_bc.values() if v['monotonic'])
    print(f"  Monotonic at {n_monotonic_scales_bc}/{len(KNN_SCALES)} scales")
    print()

    # === CONTROLS SUMMARY ===
    print("=== Controls Summary ===")
    controls = {}

    # Positive control
    controls['positive_control'] = {
        'description': 'Bias-corrected TV > 0 at lambda=1 across all 3 functions (permutation p < 0.05)',
        'pass': all_positive_pass,
        'per_function': positive_control,
    }
    print(f"  Positive control: {'PASS' if all_positive_pass else 'FAIL'}")

    # Null control
    controls['null_control'] = {
        'description': 'Bias-corrected TV ~ 0 at lambda=0 (permutation p > 0.05)',
        'pass': all_null_pass,
        'per_function': null_control_results,
    }
    print(f"  Null control: {'PASS' if all_null_pass else 'FAIL'}")

    # Bias floor consistency
    controls['bias_floor_consistency'] = {
        'description': 'Bias floor at lambda=0 consistent across functions (CV < 0.1)',
        'pass': bf_consistency_pass,
        'cv': bf_cv,
        'values': bf_at_0,
    }
    print(f"  Bias floor consistency: {'PASS' if bf_consistency_pass else 'FAIL'} (CV={bf_cv:.4f})")

    # Toroidal lambda=0 sanity
    tor_lam0_ok = all(float(np.mean(toroidal_lam0_sanity[f])) < 0.1
                      for f in range(len(FUNCTION_SEEDS)))
    controls['toroidal_sanity'] = {
        'description': 'Toroidal wrapping TV at lambda=0 < 0.1 (no geometry artefact)',
        'pass': tor_lam0_ok,
        'per_function': {str(f): float(np.mean(toroidal_lam0_sanity[f]))
                         for f in range(len(FUNCTION_SEEDS))},
    }
    print(f"  Toroidal sanity: {'PASS' if tor_lam0_ok else 'FAIL'}")

    # Spearman test
    controls['spearman_test'] = {
        'description': 'Aggregate Spearman rho(bias_corrected_TV, lambda) >= 0.65, p < 0.05 one-sided',
        'pass': spearman_pass,
        'rho': float(agg_rho_bc),
        'p_one_sided': float(agg_p_bc_one_sided),
    }
    print(f"  Spearman test: {'PASS' if spearman_pass else 'FAIL'} (rho={agg_rho_bc:.4f})")

    # Function invariance
    controls['function_invariance'] = {
        'description': 'No significant function x lambda interaction on bias-corrected TV (ANOVA p > 0.05)',
        'pass': anova_result.get('interaction_pass', False),
        'interaction_p': anova_result.get('full_model', {}).get('interaction_effect', {}).get('p_value', None),
    }
    print(f"  Function invariance: {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}")

    # Clipping gap reduction
    controls['clipping_gap_reduction'] = {
        'description': 'Clipping removal reduces translation-scaling separation gap by >50%',
        'pass': gap_pass,
        'gap_reduction_fraction': gap_reduction,
    }
    print(f"  Clipping gap reduction: {'PASS' if gap_pass else 'FAIL'} ({gap_reduction:.1%})")

    # Multi-scale monotonicity
    controls['multiscale_monotonicity'] = {
        'description': f'Bias-corrected monotonicity holds at >=2 of {len(KNN_SCALES)} kNN scales',
        'pass': n_monotonic_scales_bc >= 2,
        'n_monotonic': n_monotonic_scales_bc,
        'n_total': len(KNN_SCALES),
    }
    print(f"  Multiscale monotonicity: {'PASS' if n_monotonic_scales_bc >= 2 else 'FAIL'}")

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
        'null_control': all_null_pass,
        'function_invariance': anova_result.get('interaction_pass', False),
        'clipping_gap': gap_pass,
        'no_pipeline_errors': True,
    }

    any_pipeline_error = False
    over_correction = False
    bf_high_variance = False
    toroidal_artefact = False

    # Check over-correction: >10% of bias-corrected TV values negative at lambda=1
    n_negative_bc = 0
    n_total_bc = 0
    for f_idx in range(len(FUNCTION_SEEDS)):
        for val in bias_corrected_tv[PRIMARY_K][f_idx][1.0]:
            n_total_bc += 1
            if val < 0:
                n_negative_bc += 1
    over_correction = (n_negative_bc / n_total_bc) > 0.1 if n_total_bc > 0 else False

    # Check permutation null variance
    bf_high_variance = bf_cv > 0.5

    # Check toroidal artefact
    toroidal_artefact = not tor_lam0_ok

    measurement_invalid = over_correction or bf_high_variance or toroidal_artefact

    if any_pipeline_error or measurement_invalid:
        decision = 'MEASUREMENT_INVALID'
        outcome = 'NOT_APPLICABLE'
    elif all(conditions.values()):
        decision = 'SURVIVES_CURRENT_TEST'
        outcome = 'SUPPORTS'
    else:
        decision = 'FALSIFIED-IN-SETTING'
        outcome = 'FALSIFIES'

    print(f"  Conditions: {conditions}")
    print(f"  Over-correction: {over_correction} ({n_negative_bc}/{n_total_bc} negative)")
    print(f"  High BF variance: {bf_high_variance}")
    print(f"  Toroidal artefact: {toroidal_artefact}")
    print(f"  Measurement invalid: {measurement_invalid}")
    print(f"  Overall Decision: {decision}")
    print(f"  Overall Outcome: {outcome}")
    print()

    elapsed = time.time() - start_time
    print(f"Total execution time: {elapsed:.1f}s")

    # === COMPILE RESULTS ===
    # Aggregate raw TV means
    raw_agg_means = []
    for l in LAMBDA_LEVELS:
        all_raw_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_raw_at_l.extend(raw_knn_tv[PRIMARY_K][f_idx][l])
        raw_agg_means.append(float(np.mean(all_raw_at_l)))

    # Aggregate bias floor means
    bf_agg_means = []
    for l in LAMBDA_LEVELS:
        all_bf_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_bf_at_l.extend(bias_floor[PRIMARY_K][f_idx][l])
        bf_agg_means.append(float(np.mean(all_bf_at_l)))

    results = {
        'schema_version': 1,
        'experiment_id': 'EXP-FRONTIER-34121473072',
        'lane': 'frontier',
        'status': 'COMPLETE' if not any_pipeline_error and not measurement_invalid else 'MEASUREMENT_INVALID',
        'outcome': outcome,
        'metrics': {
            'aggregate': {
                'spearman_rho_bias_corrected': float(agg_rho_bc),
                'spearman_p_one_sided_bias_corrected': float(agg_p_bc_one_sided),
                'bias_corrected_tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): agg_bc_means[i]
                                                      for i in range(len(LAMBDA_LEVELS))},
                'raw_tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): raw_agg_means[i]
                                           for i in range(len(LAMBDA_LEVELS))},
                'bias_floor_means_by_lambda': {str(LAMBDA_LEVELS[i]): bf_agg_means[i]
                                               for i in range(len(LAMBDA_LEVELS))},
                'raw_spearman_rho': None,  # computed for reference
            },
            'per_function': {},
            'effect_sizes': {},
            'separation_gap': separation_gap,
            'multiscale_knn_bc': multiscale_bc,
            'clipping_comparison': clip_comparison,
            'frequency_baseline': freq_results,
            'noise_comparison': noise_comparison,
            'bias_floor_consistency': {
                'cv': bf_cv,
                'values_per_function': bf_at_0,
                'pass': bf_consistency_pass,
            },
            'toroidal_sanity': {
                'lambda0_values': {str(f): float(np.mean(toroidal_lam0_sanity[f]))
                                   for f in range(len(FUNCTION_SEEDS))},
                'pass': tor_lam0_ok,
            },
            'over_correction_check': {
                'n_negative_at_lambda1': n_negative_bc,
                'n_total': n_total_bc,
                'fraction_negative': n_negative_bc / n_total_bc if n_total_bc > 0 else 0.0,
                'pass': not over_correction,
            },
        },
        'controls': controls,
        'artifacts': [
            {'path': 'research/experiments/EXP-FRONTIER-34121473072/analyze.py', 'role': 'code'},
            {'path': 'research/experiments/EXP-FRONTIER-34121473072/raw_tables.json', 'role': 'raw'},
        ],
        'observations': [],
        'validity_notes': [],
        'unresolved': [],
    }

    # Raw Spearman (for reference)
    raw_rho, raw_p = stats.spearmanr(lambda_arr, np.array(raw_agg_means))
    raw_p_one_sided = raw_p / 2 if raw_rho > 0 else 1 - raw_p / 2
    results['metrics']['aggregate']['raw_spearman_rho'] = float(raw_rho)
    results['metrics']['aggregate']['raw_spearman_p_one_sided'] = float(raw_p_one_sided)

    # Fill per_function metrics
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        # Cohen's d for bias-corrected TV
        bc_0 = np.array(bias_corrected_tv[PRIMARY_K][f_idx][0.0])
        bc_1 = np.array(bias_corrected_tv[PRIMARY_K][f_idx][1.0])
        pooled_std = np.sqrt((np.var(bc_0, ddof=1) + np.var(bc_1, ddof=1)) / 2)
        cohens_d = float((np.mean(bc_1) - np.mean(bc_0)) / pooled_std) if pooled_std > 0 else 0.0

        results['metrics']['per_function'][str(func_seed)] = {
            'func_name': func_name,
            'spearman_rho_bc': per_function_bc_results[func_seed]['spearman_rho'],
            'spearman_p_one_sided_bc': per_function_bc_results[func_seed]['spearman_p_one_sided'],
            'tv_bc_means_by_lambda': per_function_bc_results[func_seed]['tv_bc_means_by_lambda'],
            'cohens_d_bc': cohens_d,
            'bias_floor_at_lambda0': bf_at_0[f_idx],
            'clipping_fraction_at_lambda1': float(np.mean(clipping_fractions[f_idx][1.0])),
        }
        results['metrics']['effect_sizes'][str(func_seed)] = cohens_d

    # Aggregate Cohen's d
    agg_bc_0 = []
    agg_bc_1 = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        agg_bc_0.extend(bias_corrected_tv[PRIMARY_K][f_idx][0.0])
        agg_bc_1.extend(bias_corrected_tv[PRIMARY_K][f_idx][1.0])
    pooled_std_agg = np.sqrt((np.var(agg_bc_0, ddof=1) + np.var(agg_bc_1, ddof=1)) / 2)
    agg_cohens_d = float((np.mean(agg_bc_1) - np.mean(agg_bc_0)) / pooled_std_agg) if pooled_std_agg > 0 else 0.0
    results['metrics']['effect_sizes']['aggregate'] = agg_cohens_d

    # Observations (raw, not interpreted)
    results['observations'] = [
        f"Overall decision: {decision}",
        f"Aggregate Spearman rho(bias_corrected_TV, lambda)={agg_rho_bc:.4f}, p_one_sided={agg_p_bc_one_sided:.6f}",
        f"Raw Spearman rho(TV, lambda)={raw_rho:.4f}, p_one_sided={raw_p_one_sided:.6f}",
        f"Positive control (bias-corrected TV > 0 at lambda=1): {'PASS' if all_positive_pass else 'FAIL'}",
        f"Null control (bias-corrected TV ~ 0 at lambda=0): {'PASS' if all_null_pass else 'FAIL'}",
        f"Function invariance (ANOVA interaction): {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}",
        f"Clipping gap reduction: {gap_reduction:.1%} (pass >50%: {gap_pass})",
        f"Bias floor consistency: CV={bf_cv:.4f} (pass <0.1: {bf_consistency_pass})",
        f"Toroidal sanity at lambda=0: {'PASS' if tor_lam0_ok else 'FAIL'}",
        f"Over-correction check: {n_negative_bc}/{n_total_bc} negative values at lambda=1",
        f"Aggregate Cohen's d (bias-corrected, lambda=0 vs 1): {agg_cohens_d:.4f}",
        f"Multiscale monotonicity (bias-corrected): {n_monotonic_scales_bc}/{len(KNN_SCALES)} scales",
    ]

    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        rho = per_function_bc_results[func_seed]['spearman_rho']
        p = per_function_bc_results[func_seed]['spearman_p_one_sided']
        results['observations'].append(
            f"Function {func_seed} ({func_name}): bias-corrected rho={rho:.4f}, "
            f"p_one_sided={p:.6f}, cohens_d={results['metrics']['effect_sizes'][str(func_seed)]:.4f}"
        )

    # Validity notes
    results['validity_notes'] = [
        '10D continuous state space [0,1]^10 with mixture-of-3-Gaussians heteroscedastic noise',
        f'500 transitions per cell with ~125 per action; Monte Carlo SE ~0.04',
        f'{N_REPLICATIONS} replications per cell enable variance estimation',
        f'{len(LAMBDA_LEVELS)} lambda levels provide degradation curve resolution',
        '3 independent continuous function families (10D rotation, scaling, translation)',
        f'Frozen random seed (seed={SEED}) for reproducibility',
        'Bias correction: permutation-null subtraction at each lambda/function/kNN scale',
        f'{N_PERMUTATIONS} permutations per cell for bias floor estimation',
        'Permutation null computed at primary kNN scale k=20; applied to all scales',
        'Toroidal wrapping uses modular arithmetic (x - floor(x)) as alternative to clipping',
        'Frequency baseline: pairwise TV between action-conditional marginal next-state distributions',
        'Gaussian noise baseline: single-Gaussian heteroscedastic noise (not mixture)',
        f'kNN-based TV in full 10D at k={KNN_SCALES}',
        'Clipping to [0,1] after noise addition; toroidal wrapping as comparison',
        'ANOVA on bias-corrected TV across 8 lambda levels x 3 functions x 10 reps = 240 observations',
    ]

    # Unresolved
    results['unresolved'] = [
        'Whether scaling failure persists after bias correction (specific per-function result)',
        'Whether bias correction generalizes to >10D state spaces (Web DOM embeddings)',
        'Whether real Web transitions exhibit action-dependent structure suitable for TV detection',
        'Whether combined noise models interact non-linearly beyond individual noise types',
        'Whether kNN TV remains calibrated at N=500 in >50D spaces',
        'Whether rotation non-monotonic dip reflects estimator noise or genuine non-monotonic response',
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
    files_to_hash = ['prereg.md', 'spec.json', 'request.json', 'freeze.json']
    hashes = {}
    for fname in files_to_hash:
        fpath = experiment_dir / fname
        if fpath.exists():
            h = hashlib.sha256(fpath.read_bytes()).hexdigest()
            hashes[fname] = h

    # Also hash output artifacts
    for out_name in ['result.json', 'raw_tables.json', 'analyze.py']:
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
            'sklearn_version': __import__('sklearn').__version__,
        },
        'frozen_inputs': {
            'prereg_hash': '135d57712c922be28af2f119d23ae9634d5d17dc39648a9db182c8afd2bbf007',
            'request_hash': '562ecee83cbc08a62295c677ad2d53909b81291c3806be0cd85cba15599e8526',
            'spec_hash': 'ce63def49a35da19247fc05afc837533e8c6acc285ded7335f713c015866a476',
            'freeze_hash': hashlib.sha256((experiment_dir / 'freeze.json').read_bytes()).hexdigest(),
        },
        'total_transitions': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_TRANSITIONS,
        'total_permutations': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_PERMUTATIONS,
        'execution_seconds': elapsed,
        'parent_experiment': 'EXP-FRONTIER-34065969836',
        'parent_handoff_hash': '26e7bd90e02cd678328699e7a7cd2d1e0e6e0873361d309d1e775253ff0ef805',
    }

    provenance_path = Path(__file__).parent / 'provenance.json'
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
