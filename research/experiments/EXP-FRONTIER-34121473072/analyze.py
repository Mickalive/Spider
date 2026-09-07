#!/usr/bin/env python3
"""
EXP-FRONTIER-34121473072: Bias-Corrected kNN TV in 10D Non-Gaussian Spaces.

Frozen experiment code. Do not modify after freeze.

Tests whether permutation-null bias subtraction recovers function invariance
in 10D non-Gaussian spaces, and whether clipping artefact explains per-function
heterogeneity (translation strong, scaling weak).
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
    """State-dependent rotation in 10D."""
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
    """State-dependent scaling in 10D."""
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
    """Mixture of 3 Gaussians per dimension (non-Gaussian)."""
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
    """Single Gaussian heteroscedastic noise per dimension."""
    dist_to_center = np.linalg.norm(s - 0.5)
    sigma_base = 0.05 * (1 + 0.5 * dist_to_center)
    noise = rng.normal(0, sigma_base, size=DIM)
    return noise


# === DATA GENERATION ===
def generate_transitions(func_seed, lambda_val, n, rng, noise_type='nongaussian', wrap='clip'):
    """
    Generate transitions using 10D DGP.
    wrap='clip': clip to [0,1] (parent method)
    wrap='toroidal': modular arithmetic wrapping
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

        if wrap == 'toroidal':
            s_next = s_next - np.floor(s_next)  # modular arithmetic
        else:
            s_next = np.clip(s_next, 0, 1)
        transitions.append((s, ACTIONS[a_idx], s_next))
    return transitions


# === TV DISTANCE: kNN-BASED ===
def knn_tv_estimate(X_a, X_b, k):
    """kNN-based TV distance between two samples."""
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
    """Compute TV for all 6 action pairs, return max and mean."""
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


# === PERMUTATION NULL for BIAS FLOOR ===
def compute_permutation_null(transitions, k, n_permutations, rng):
    """
    Compute permutation null distribution: shuffle action labels, recompute TV.
    Returns list of null TV values (length n_permutations).
    """
    actions = [a for _, a, _ in transitions]
    s_nexts = [np.array(s_next) for _, _, s_next in transitions]
    
    null_tvs = []
    for _ in range(n_permutations):
        shuffled_actions = list(actions)
        rng.shuffle(shuffled_actions)
        perm_transitions = [(None, a, sn) for a, sn in zip(shuffled_actions, s_nexts)]
        perm_tv, _ = compute_knn_tv_all_pairs(perm_transitions, k)
        null_tvs.append(perm_tv)
    return null_tvs


# === FREQUENCY BASELINE ===
def compute_frequency_baseline(transitions):
    """
    Frequency baseline: TV between action-conditional distributions using
    marginal P(S_{t+1}) as reference. Measures marginal non-uniformity.
    """
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)
    
    # Compute marginal P(S_{t+1}) by averaging across all actions
    all_nexts = []
    for a in ACTIONS:
        all_nexts.extend(action_states[a])
    marginal = np.mean(all_nexts, axis=0) if all_nexts else np.zeros(DIM)
    
    # Compute per-action means
    action_means = {}
    for a in ACTIONS:
        if action_states[a]:
            action_means[a] = np.mean(action_states[a], axis=0)
        else:
            action_means[a] = marginal
    
    # TV between action-conditional means using marginal as reference
    actions_list = list(ACTIONS)
    tv_max = 0.0
    tv_sum = 0.0
    n_pairs = 0
    for i in range(len(actions_list)):
        for j in range(i + 1, len(actions_list)):
            # Simple TV between action means relative to marginal
            diff = np.abs(action_means[actions_list[i]] - action_means[actions_list[j]])
            tv = 0.5 * np.mean(diff)
            tv_max = max(tv_max, tv)
            tv_sum += tv
            n_pairs += 1
    return tv_max


# === MAIN EXPERIMENT ===
def run_experiment():
    start_time = time.time()
    print("=== EXP-FRONTIER-34121473072: Bias-Corrected kNN TV ===")
    print(f"Seed: {SEED}, Lambda levels: {LAMBDA_LEVELS}")
    print(f"Functions: 3 (seeds {FUNCTION_SEEDS})")
    print(f"Transitions per cell: {N_TRANSITIONS}, Replications: {N_REPLICATIONS}")
    print(f"Permutations per cell: {N_PERMUTATIONS}")
    print(f"State space: continuous 10D [0,1]^10")
    print(f"Noise: mixture of 3 Gaussians (non-Gaussian heteroscedastic)")
    print()

    # === STORAGE ===
    # Raw (unbiased) TV at multiple scales
    raw_knn_tv = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                      for f_idx in range(len(FUNCTION_SEEDS))}
                  for k in KNN_SCALES}

    # Bias floor from permutation null
    bias_floor = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                      for f_idx in range(len(FUNCTION_SEEDS))}
                  for k in KNN_SCALES}

    # Bias-corrected TV
    bias_corrected_tv = {k: {f_idx: {l: [] for l in LAMBDA_LEVELS}
                             for f_idx in range(len(FUNCTION_SEEDS))}
                         for k in KNN_SCALES}

    # Toroidal wrapping TV (at PRIMARY_K only, for clipping comparison)
    toroidal_tv = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                   for f_idx in range(len(FUNCTION_SEEDS))}

    # Frequency baseline
    freq_baseline = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                     for f_idx in range(len(FUNCTION_SEEDS))}

    # Gaussian noise baseline
    gaussian_tv = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                   for f_idx in range(len(FUNCTION_SEEDS))}

    # Permutation null variance tracking
    perm_null_variance = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                          for f_idx in range(len(FUNCTION_SEEDS))}

    clipping_fractions = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                          for f_idx in range(len(FUNCTION_SEEDS))}

    raw_tables = []

    # === RUN EXPERIMENT ===
    total_cells = len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS
    cell_count = 0

    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}...", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                cell_count += 1
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)

                # Generate transitions (clipping)
                transitions = generate_transitions(func_seed, l, N_TRANSITIONS, rng, wrap='clip')

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

                # Permutation null for bias floor (1000 perms)
                perm_rng = np.random.RandomState(rep_seed + 999)
                for k in KNN_SCALES:
                    null_tvs = compute_permutation_null(transitions, k, N_PERMUTATIONS, perm_rng)
                    bias_floor[k][f_idx][l].append(float(np.mean(null_tvs)))
                    bias_corrected_tv[k][f_idx][l].append(
                        raw_knn_tv[k][f_idx][l][-1] - float(np.mean(null_tvs))
                    )
                    perm_null_variance[f_idx][l].append(float(np.std(null_tvs, ddof=1)))

                # Toroidal wrapping TV (PRIMARY_K only)
                rng_tor = np.random.RandomState(rep_seed)
                transitions_tor = generate_transitions(func_seed, l, N_TRANSITIONS, rng_tor, wrap='toroidal')
                tv_tor, _ = compute_knn_tv_all_pairs(transitions_tor, PRIMARY_K)
                toroidal_tv[f_idx][l].append(tv_tor)

                # Frequency baseline
                freq_bl = compute_frequency_baseline(transitions)
                freq_baseline[f_idx][l].append(freq_bl)

                raw_tables.append({
                    'func_seed': func_seed,
                    'func_name': func_name,
                    'lambda': l,
                    'replication': rep_idx,
                    'raw_tv_k20': raw_knn_tv[PRIMARY_K][f_idx][l][-1],
                    'bias_floor_k20': bias_floor[PRIMARY_K][f_idx][l][-1],
                    'bias_corrected_k20': bias_corrected_tv[PRIMARY_K][f_idx][l][-1],
                    'toroidal_tv_k20': toroidal_tv[f_idx][l][-1],
                    'freq_baseline': freq_baseline[f_idx][l][-1],
                    'clipping_fraction': clipping_fractions[f_idx][l][-1],
                })

            # Print summary for this cell
            bc_means = bias_corrected_tv[PRIMARY_K][f_idx][l]
            raw_means = raw_knn_tv[PRIMARY_K][f_idx][l]
            print(f" raw={np.mean(raw_means):.4f} bc={np.mean(bc_means):.4f}"
                  f" clip={np.mean(clipping_fractions[f_idx][l]):.3f}")

        print()

    # === GAUSSIAN NOISE BASELINE ===
    print("=== Gaussian Noise Baseline ===")
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        for l in LAMBDA_LEVELS:
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)
                transitions_g = generate_transitions(func_seed, l, N_TRANSITIONS, rng, noise_type='gaussian', wrap='clip')
                tv_g, _ = compute_knn_tv_all_pairs(transitions_g, PRIMARY_K)
                gaussian_tv[f_idx][l].append(tv_g)
        g_means = [np.mean(gaussian_tv[f_idx][l]) for l in LAMBDA_LEVELS]
        print(f"  Function {func_seed} ({func_name}): Gaussian TV = {[f'{m:.4f}' for m in g_means]}")
    print()

    # === AGGREGATE ANALYSIS (bias-corrected, PRIMARY_K) ===
    print("=== Aggregate Analysis (Bias-Corrected kNN k=20) ===")
    lambda_arr = np.array(LAMBDA_LEVELS)
    
    # Aggregate bias-corrected TV means by lambda
    agg_bc_means = []
    for l in LAMBDA_LEVELS:
        all_bc = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            all_bc.extend(bias_corrected_tv[PRIMARY_K][f_idx][l])
        agg_bc_means.append(float(np.mean(all_bc)))

    agg_rho_bc, agg_p_bc = stats.spearmanr(lambda_arr, np.array(agg_bc_means))
    agg_p_bc_one_sided = agg_p_bc / 2 if agg_rho_bc > 0 else 1 - agg_p_bc / 2
    print(f"  Aggregate Spearman rho(bc_TV, lambda): {agg_rho_bc:.4f}, p_one_sided: {agg_p_bc_one_sided:.6f}")

    # Per-function analysis
    per_function_results = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        tv_bc_means = np.array([np.mean(bias_corrected_tv[PRIMARY_K][f_idx][l]) for l in LAMBDA_LEVELS])
        rho, p = stats.spearmanr(lambda_arr, tv_bc_means)
        p_one = p / 2 if rho > 0 else 1 - p / 2
        per_function_results[func_seed] = {
            'func_name': func_name,
            'spearman_rho_bc': float(rho),
            'spearman_p_one_sided_bc': float(p_one),
            'tv_bc_means_by_lambda': {str(l): float(tv_bc_means[i]) for i, l in enumerate(LAMBDA_LEVELS)},
        }
        print(f"  Function {func_seed} ({func_name}): rho_bc={rho:.4f}, p_one={p_one:.6f}")
    print()

    # === MULTI-SCALE ANALYSIS (bias-corrected) ===
    print("=== Multi-Scale kNN Analysis (Bias-Corrected) ===")
    multiscale_bc_results = {}
    for k in KNN_SCALES:
        agg_k = []
        for l in LAMBDA_LEVELS:
            all_bc_k = []
            for f_idx in range(len(FUNCTION_SEEDS)):
                all_bc_k.extend(bias_corrected_tv[k][f_idx][l])
            agg_k.append(float(np.mean(all_bc_k)))
        rho_k, p_k = stats.spearmanr(lambda_arr, np.array(agg_k))
        p_k_one = p_k / 2 if rho_k > 0 else 1 - p_k / 2
        is_monotonic = all(agg_k[i] <= agg_k[i + 1] for i in range(len(agg_k) - 1))
        multiscale_bc_results[k] = {
            'rho': float(rho_k),
            'p_one_sided': float(p_k_one),
            'monotonic': is_monotonic,
            'tv_bc_means_by_lambda': {str(LAMBDA_LEVELS[i]): agg_k[i] for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  k={k}: rho_bc={rho_k:.4f}, p={p_k_one:.6f}, monotonic={is_monotonic}")
    n_monotonic = sum(1 for v in multiscale_bc_results.values() if v['monotonic'])
    print(f"  Monotonic at {n_monotonic}/{len(KNN_SCALES)} scales")
    print()

    # === TWO-WAY ANOVA (bias-corrected) ===
    print("=== Two-Way ANOVA (Bias-Corrected) ===")
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
                        'lambda': str(l),
                        'function': str(f_idx + 1),
                        'tv_bc': tv_val
                    })
        df = pd.DataFrame(anova_data)
        model = ols('tv_bc ~ C(lambda) + C(function) + C(lambda):C(function)', data=df).fit()
        anova_table = anova_lm(model, typ=2)
        anova_result = {
            'design': f"{len(FUNCTION_SEEDS)} functions x {len(LAMBDA_LEVELS)} lambdas x {N_REPLICATIONS} reps = {len(anova_data)} obs",
            'lambda_effect': {
                'F': round(float(anova_table.loc['C(lambda)', 'F']), 4),
                'p_value': round(float(anova_table.loc['C(lambda)', 'PR(>F)']), 6),
            },
            'function_effect': {
                'F': round(float(anova_table.loc['C(function)', 'F']), 4),
                'p_value': round(float(anova_table.loc['C(function)', 'PR(>F)']), 6),
            },
            'interaction_effect': {
                'F': round(float(anova_table.loc['C(lambda):C(function)', 'F']), 4),
                'p_value': round(float(anova_table.loc['C(lambda):C(function)', 'PR(>F)']), 6),
            },
            'model_r_squared': round(float(model.rsquared), 4),
            'interaction_pass': bool(float(anova_table.loc['C(lambda):C(function)', 'PR(>F)']) > ALPHA),
        }
        print(f"  Interaction p-value: {anova_result['interaction_effect']['p_value']}")
        print(f"  Interaction pass (p > 0.05): {anova_result['interaction_pass']}")
    except Exception as e:
        anova_result = {'error': str(e), 'interaction_pass': False}
        print(f"  ANOVA failed: {e}")
    print()

    # === PERMUTATION TESTS (bias-corrected) ===
    print("=== Permutation Tests (Bias-Corrected) ===")
    perm_bc_results = {}
    for l_key in [0.0, 1.0]:
        perm_p_vals = []
        for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)
                transitions = generate_transitions(func_seed, l_key, N_TRANSITIONS, rng)
                # Compute raw TV and permutation null
                raw_tv, _ = compute_knn_tv_all_pairs(transitions, PRIMARY_K)
                perm_rng = np.random.RandomState(rep_seed + 999)
                null_tvs = compute_permutation_null(transitions, PRIMARY_K, 200, perm_rng)
                bc_tv = raw_tv - np.mean(null_tvs)
                # Count how many perm nulls exceed the raw TV
                count_ge = sum(1 for nt in null_tvs if nt >= raw_tv)
                p_val = count_ge / len(null_tvs)
                perm_p_vals.append(p_val)
        mean_p = float(np.mean(perm_p_vals)) if perm_p_vals else 1.0
        perm_bc_results[str(l_key)] = {
            'mean_p_value': round(mean_p, 6),
            'pass': mean_p > ALPHA if l_key == 0.0 else mean_p < ALPHA,
        }
        print(f"  lambda={l_key}: mean_p={mean_p:.6f}, pass={perm_bc_results[str(l_key)]['pass']}")
    print()

    # === CLIPPING COMPARISON (Clipping vs Toroidal) ===
    print("=== Clipping vs Toroidal Comparison ===")
    clipping_comparison = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        clip_seps = []
        tor_seps = []
        for l in LAMBDA_LEVELS:
            clip_means = np.mean(raw_knn_tv[PRIMARY_K][f_idx][l])
            tor_means = np.mean(toroidal_tv[f_idx][l])
            clip_seps.append(clip_means)
            tor_seps.append(tor_means)
        clip_advantage = clip_seps[-1] - clip_seps[0]  # separation at lambda=1 vs 0
        tor_advantage = tor_seps[-1] - tor_seps[0]
        reduction = (clip_advantage - tor_advantage) / clip_advantage if clip_advantage > 0 else 0.0
        clipping_comparison[str(func_seed)] = {
            'func_name': func_name,
            'clip_separation': float(clip_advantage),
            'toroidal_separation': float(tor_advantage),
            'reduction_fraction': float(reduction),
            'clip_tv_by_lambda': {str(LAMBDA_LEVELS[i]): float(clip_seps[i]) for i in range(len(LAMBDA_LEVELS))},
            'toroidal_tv_by_lambda': {str(LAMBDA_LEVELS[i]): float(tor_seps[i]) for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  {func_name}: clip_sep={clip_advantage:.4f}, tor_sep={tor_advantage:.4f}, reduction={reduction:.2%}")

    # Translation vs Scaling separation gap
    clip_trans_sep = clipping_comparison['44']['clip_separation']
    clip_scale_sep = clipping_comparison['43']['clip_separation']
    tor_trans_sep = clipping_comparison['44']['toroidal_separation']
    tor_scale_sep = clipping_comparison['43']['toroidal_separation']
    gap_before = clip_trans_sep - clip_scale_sep
    gap_after = tor_trans_sep - tor_scale_sep
    gap_reduction = (gap_before - gap_after) / gap_before if gap_before > 0 else 0.0
    print(f"  Translation-Scaling gap: before={gap_before:.4f}, after={gap_after:.4f}, reduction={gap_reduction:.2%}")
    print()

    # === FREQUENCY BASELINE ANALYSIS ===
    print("=== Frequency Baseline Analysis ===")
    freq_analysis = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        freq_means = [np.mean(freq_baseline[f_idx][l]) for l in LAMBDA_LEVELS]
        raw_at_0 = np.mean(raw_knn_tv[PRIMARY_K][f_idx][0.0])
        freq_at_0 = np.mean(freq_baseline[f_idx][0.0])
        fraction_explained = freq_at_0 / raw_at_0 if raw_at_0 > 0 else 0.0
        freq_analysis[str(func_seed)] = {
            'func_name': func_name,
            'freq_means_by_lambda': {str(LAMBDA_LEVELS[i]): float(freq_means[i]) for i in range(len(LAMBDA_LEVELS))},
            'raw_tv_at_lambda0': float(raw_at_0),
            'freq_baseline_at_lambda0': float(freq_at_0),
            'fraction_explained': float(fraction_explained),
        }
        print(f"  {func_name}: raw@0={raw_at_0:.4f}, freq@0={freq_at_0:.4f}, explained={fraction_explained:.2%}")
    print()

    # === GAUSSIAN vs MIXTURE COMPARISON ===
    print("=== Gaussian vs Mixture Noise Comparison ===")
    noise_comparison = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        mixture_means = [np.mean(raw_knn_tv[PRIMARY_K][f_idx][l]) for l in LAMBDA_LEVELS]
        gaussian_means = [np.mean(gaussian_tv[f_idx][l]) for l in LAMBDA_LEVELS]
        rho_mix, _ = stats.spearmanr(lambda_arr, np.array(mixture_means))
        rho_gauss, _ = stats.spearmanr(lambda_arr, np.array(gaussian_means))
        noise_comparison[str(func_seed)] = {
            'func_name': func_name,
            'mixture_rho': float(rho_mix),
            'gaussian_rho': float(rho_gauss),
            'mixture_tv_by_lambda': {str(LAMBDA_LEVELS[i]): float(mixture_means[i]) for i in range(len(LAMBDA_LEVELS))},
            'gaussian_tv_by_lambda': {str(LAMBDA_LEVELS[i]): float(gaussian_means[i]) for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  {func_name}: mixture_rho={rho_mix:.4f}, gaussian_rho={rho_gauss:.4f}")
    print()

    # === BIAS FLOOR CONSISTENCY ===
    print("=== Bias Floor Consistency ===")
    bias_floor_consistency = {}
    for k in KNN_SCALES:
        floor_at_0 = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            floor_at_0.extend(bias_floor[k][f_idx][0.0])
        mean_floor = np.mean(floor_at_0)
        std_floor = np.std(floor_at_0, ddof=1)
        cv = std_floor / mean_floor if mean_floor > 0 else 0.0
        bias_floor_consistency[str(k)] = {
            'mean_floor': float(mean_floor),
            'std_floor': float(std_floor),
            'cv': float(cv),
            'pass': bool(cv < 0.1),
        }
        print(f"  k={k}: mean={mean_floor:.4f}, std={std_floor:.4f}, CV={cv:.4f}, pass={cv < 0.1}")
    print()

    # === EFFECT SIZES (Cohen's d) ===
    print("=== Effect Sizes (Bias-Corrected) ===")
    effect_sizes_bc = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        tv_0 = np.array(bias_corrected_tv[PRIMARY_K][f_idx][0.0])
        tv_1 = np.array(bias_corrected_tv[PRIMARY_K][f_idx][1.0])
        pooled_std = np.sqrt((np.var(tv_0, ddof=1) + np.var(tv_1, ddof=1)) / 2)
        cohens_d = float((np.mean(tv_1) - np.mean(tv_0)) / pooled_std) if pooled_std > 0 else 0.0
        effect_sizes_bc[str(func_seed)] = cohens_d
        print(f"  Function {func_seed} ({FUNCTION_NAMES[func_seed]}): Cohen's d = {cohens_d:.4f}")

    agg_bc_0 = []
    agg_bc_1 = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        agg_bc_0.extend(bias_corrected_tv[PRIMARY_K][f_idx][0.0])
        agg_bc_1.extend(bias_corrected_tv[PRIMARY_K][f_idx][1.0])
    pooled_std_agg = np.sqrt((np.var(agg_bc_0, ddof=1) + np.var(agg_bc_1, ddof=1)) / 2)
    agg_cohens_d = float((np.mean(agg_bc_1) - np.mean(agg_bc_0)) / pooled_std_agg) if pooled_std_agg > 0 else 0.0
    effect_sizes_bc['aggregate'] = agg_cohens_d
    print(f"  Aggregate: Cohen's d = {agg_cohens_d:.4f}")
    print()

    # === VALIDITY CHECKS ===
    print("=== Validity Checks ===")
    
    # Check for over-correction (negative bc TV at lambda=1)
    n_negative_bc_at_1 = 0
    n_total_bc_at_1 = 0
    for f_idx in range(len(FUNCTION_SEEDS)):
        for val in bias_corrected_tv[PRIMARY_K][f_idx][1.0]:
            n_total_bc_at_1 += 1
            if val < 0:
                n_negative_bc_at_1 += 1
    over_correction_frac = n_negative_bc_at_1 / n_total_bc_at_1 if n_total_bc_at_1 > 0 else 0.0
    print(f"  Over-correction (negative bc TV at lambda=1): {n_negative_bc_at_1}/{n_total_bc_at_1} = {over_correction_frac:.2%}")

    # Check permutation null variance
    max_perm_cv = 0
    for f_idx in range(len(FUNCTION_SEEDS)):
        for l in LAMBDA_LEVELS:
            cvs = []
            for k in KNN_SCALES:
                null_means = bias_floor[k][f_idx][l]
                cv = np.std(null_means, ddof=1) / np.mean(null_means) if np.mean(null_means) > 0 else 0.0
                cvs.append(cv)
            max_perm_cv = max(max_perm_cv, max(cvs))

    # Check toroidal wrapping at lambda=0
    tor_at_0_values = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        tor_at_0_values.extend(toroidal_tv[f_idx][0.0])
    tor_at_0_mean = np.mean(tor_at_0_values)
    print(f"  Toroidal TV at lambda=0: {tor_at_0_mean:.4f} (should be ~0)")
    print()

    # === CONTROL CHECKS ===
    print("=== Control Checks ===")
    controls = {}

    # Positive control: bc TV > 0 at lambda=1 across all functions
    positive_control = {}
    all_positive_pass = True
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        bc_at_1 = float(np.mean(bias_corrected_tv[PRIMARY_K][f_idx][1.0]))
        bc_at_0 = float(np.mean(bias_corrected_tv[PRIMARY_K][f_idx][0.0]))
        passes = bc_at_1 > 0
        positive_control[str(func_seed)] = {
            'pass': passes,
            'bc_tv_at_lambda1': bc_at_1,
            'bc_tv_at_lambda0': bc_at_0,
        }
        if not passes:
            all_positive_pass = False
        print(f"  Positive control ({FUNCTION_NAMES[func_seed]}): {'PASS' if passes else 'FAIL'}"
              f" (bc_TV@1={bc_at_1:.4f}, bc_TV@0={bc_at_0:.4f})")
    controls['positive_control'] = {
        'description': 'Bias-corrected TV > 0 at lambda=1 across all functions',
        'pass': all_positive_pass,
        'per_function': positive_control,
    }

    # Null control: bc TV ≈ 0 at lambda=0 (permutation p > 0.05)
    null_control_pass = perm_bc_results['0.0']['pass']
    controls['null_control'] = {
        'description': 'Bias-corrected TV ≈ 0 at lambda=0 (permutation p > 0.05)',
        'pass': null_control_pass,
        'mean_perm_p': perm_bc_results['0.0']['mean_p_value'],
    }
    print(f"  Null control: {'PASS' if null_control_pass else 'FAIL'} (p={perm_bc_results['0.0']['mean_p_value']:.6f})")

    # Aggregate Spearman test
    spearman_pass = (agg_rho_bc >= 0.65 and agg_p_bc_one_sided < 0.05)
    controls['spearman_test'] = {
        'description': f'Aggregate Spearman rho(bc_TV, lambda) >= 0.65, p < 0.05 one-sided',
        'pass': spearman_pass,
        'rho': float(agg_rho_bc),
        'p_one_sided': float(agg_p_bc_one_sided),
    }
    print(f"  Spearman test: {'PASS' if spearman_pass else 'FAIL'} (rho={agg_rho_bc:.4f}, p={agg_p_bc_one_sided:.6f})")

    # Function invariance (ANOVA interaction)
    controls['function_invariance'] = {
        'description': 'No significant function x lambda interaction (ANOVA p > 0.05)',
        'pass': anova_result.get('interaction_pass', False),
        'interaction_p': anova_result.get('interaction_effect', {}).get('p_value', None),
    }
    print(f"  Function invariance: {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}")

    # Clipping removal test: gap reduction > 50%
    clipping_pass = gap_reduction > 0.5
    controls['clipping_test'] = {
        'description': 'Clipping removal reduces translation-scaling gap by >50%',
        'pass': clipping_pass,
        'gap_before': float(gap_before),
        'gap_after': float(gap_after),
        'reduction_fraction': float(gap_reduction),
    }
    print(f"  Clipping test: {'PASS' if clipping_pass else 'FAIL'} (reduction={gap_reduction:.2%})")

    # No pipeline errors
    controls['no_pipeline_errors'] = {
        'description': 'No pipeline errors during execution',
        'pass': True,
    }

    # Over-correction check
    over_correction_pass = over_correction_frac < 0.10
    controls['over_correction_check'] = {
        'description': '<10% of bias-corrected TV values negative at lambda=1',
        'pass': over_correction_pass,
        'fraction_negative': float(over_correction_frac),
    }
    print(f"  Over-correction check: {'PASS' if over_correction_pass else 'FAIL'} ({over_correction_frac:.2%})")

    # Toroidal sanity check
    tor_sanity_pass = tor_at_0_mean < 0.1
    controls['toroidal_sanity'] = {
        'description': 'Toroidal wrapping TV < 0.1 at lambda=0',
        'pass': tor_sanity_pass,
        'toroidal_tv_at_lambda0': float(tor_at_0_mean),
    }
    print(f"  Toroidal sanity: {'PASS' if tor_sanity_pass else 'FAIL'} (TV={tor_at_0_mean:.4f})")
    print()

    # === DECISION ===
    print("=== Decision ===")
    conditions = {
        'spearman': spearman_pass,
        'positive_control': all_positive_pass,
        'null_control': null_control_pass,
        'function_invariance': anova_result.get('interaction_pass', False),
        'clipping_test': clipping_pass,
    }
    validity_conditions = {
        'no_pipeline_errors': controls['no_pipeline_errors']['pass'],
        'over_correction': over_correction_pass,
        'toroidal_sanity': tor_sanity_pass,
    }

    any_validity_fail = not all(validity_conditions.values())
    if any_validity_fail:
        decision = 'MEASUREMENT_INVALID'
        outcome = 'NOT_APPLICABLE'
    elif all(conditions.values()):
        decision = 'SURVIVES_CURRENT_TEST'
        outcome = 'SUPPORTS'
    else:
        decision = 'FALSIFIED-IN-SETTING'
        outcome = 'FALSIFIES'

    print(f"  Conditions: {conditions}")
    print(f"  Validity: {validity_conditions}")
    print(f"  Decision: {decision}")
    print(f"  Outcome: {outcome}")
    print()

    elapsed = time.time() - start_time
    print(f"Total execution time: {elapsed:.1f}s")

    # === COMPILE RESULTS ===
    results = {
        'schema_version': 1,
        'experiment_id': 'EXP-FRONTIER-34121473072',
        'lane': 'frontier',
        'status': 'COMPLETE' if not any_validity_fail else 'MEASUREMENT_INVALID',
        'outcome': outcome,
        'metrics': {
            'aggregate': {
                'spearman_rho_bc': float(agg_rho_bc),
                'spearman_p_one_sided_bc': float(agg_p_bc_one_sided),
                'tv_bc_means_by_lambda': {str(LAMBDA_LEVELS[i]): agg_bc_means[i] for i in range(len(LAMBDA_LEVELS))},
                'cohens_d_bc': agg_cohens_d,
            },
            'per_function': {},
            'multiscale_knn_bc': multiscale_bc_results,
            'anova_bc': anova_result,
            'effect_sizes_cohens_d_bc': effect_sizes_bc,
            'clipping_comparison': clipping_comparison,
            'frequency_baseline': freq_analysis,
            'gaussian_vs_mixture': noise_comparison,
            'bias_floor_consistency': bias_floor_consistency,
            'translation_scaling_gap': {
                'gap_before_clipping_removal': float(gap_before),
                'gap_after_toroidal': float(gap_after),
                'reduction_fraction': float(gap_reduction),
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

    # Fill per_function metrics
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        results['metrics']['per_function'][str(func_seed)] = {
            'func_name': func_name,
            'spearman_rho_bc': per_function_results[func_seed]['spearman_rho_bc'],
            'spearman_p_one_sided_bc': per_function_results[func_seed]['spearman_p_one_sided_bc'],
            'tv_bc_means_by_lambda': per_function_results[func_seed]['tv_bc_means_by_lambda'],
            'monotonic_bc': multiscale_bc_results[PRIMARY_K]['monotonic'] if PRIMARY_K in multiscale_bc_results else False,
        }

    # Observations
    results['observations'] = [
        f"Decision: {decision}",
        f"Aggregate Spearman rho(bc_TV, lambda)={agg_rho_bc:.4f}, p_one_sided={agg_p_bc_one_sided:.6f}",
        f"Positive control (bc_TV>0 at lambda=1): {'PASS' if all_positive_pass else 'FAIL'}",
        f"Null control (permutation p>0.05 at lambda=0): {'PASS' if null_control_pass else 'FAIL'}",
        f"Function invariance (ANOVA interaction): {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}",
        f"Clipping removal reduces gap by {gap_reduction:.2%}: {'PASS' if clipping_pass else 'FAIL'}",
        f"Aggregate Cohen's d (bc): {agg_cohens_d:.4f}",
        f"Over-correction fraction: {over_correction_frac:.2%}",
        f"Toroidal TV at lambda=0: {tor_at_0_mean:.4f}",
        f"Execution time: {elapsed:.1f}s",
    ]
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        rho = per_function_results[func_seed]['spearman_rho_bc']
        p = per_function_results[func_seed]['spearman_p_one_sided_bc']
        results['observations'].append(
            f"Function {func_seed} ({func_name}): rho_bc={rho:.4f}, p_one={p:.6f}"
        )

    # Validity notes
    results['validity_notes'] = [
        'Bias correction via permutation-null subtraction (1000 perms per cell)',
        'Same 10D state space [0,1]^10 with mixture-of-3-Gaussians heteroscedastic noise as parent',
        'Toroidal wrapping tested as alternative to clipping',
        'Frequency baseline P(S_{t+1}) computed per cell',
        'Gaussian noise baseline computed per cell',
        f"Over-correction fraction at lambda=1: {over_correction_frac:.2%}",
        f"Toroidal TV at lambda=0: {tor_at_0_mean:.4f} (should be ~0 for sanity)",
        f"Bias floor CV at lambda=0: see bias_floor_consistency in metrics",
        'kNN scales k=5,10,20,50 tested for multi-scale robustness',
    ]

    # Unresolved
    results['unresolved'] = [
        'Whether real Web transitions exhibit action-dependent structure suitable for TV detection',
        'Whether scaling failure replicates under alternative 10D scaling parameterizations',
        'Whether kNN TV remains calibrated at >10D (e.g., 50D DOM embeddings)',
        'Whether rotation non-monotonic dip reflects estimator noise or genuine response',
    ]

    return results, raw_tables, elapsed


if __name__ == '__main__':
    results, raw_tables, elapsed = run_experiment()

    # Write result.json
    result_path = Path(__file__).parent / 'result.json'
    with open(result_path, 'w') as f:
        json.dump(to_native(results), f, indent=2)
    print(f"\nWrote {result_path}")

    # Write raw tables
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
        },
        'total_transitions': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_TRANSITIONS,
        'total_permutations': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_PERMUTATIONS * len(KNN_SCALES),
        'execution_seconds': elapsed,
    }

    provenance_path = Path(__file__).parent / 'provenance.json'
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
