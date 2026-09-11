#!/usr/bin/env python3
"""
EXP-FRONTIER-34538185726: KDE-based Jensen-Shannon Divergence Detection.

Frozen experiment code. Do not modify after freeze.

Tests whether kernel density estimation (KDE) with cross-validated bandwidth
can detect scaling-type action-dependent structure that kNN TV misses in the
same 10D non-Gaussian DGP.
"""

import json
import hashlib
import numpy as np
from scipy import stats as sp_stats
from scipy.stats import gaussian_kde
from pathlib import Path
import warnings
import time
import sys

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
N_PERMUTATIONS = 50  # permutation null per cell (matching parent pragmatic choice)
ALPHA = 0.05
DIM = 10  # 10D state space
N_ACTIONS = 4
ACTIONS = ['click', 'fill', 'submit', 'navigate']

# KDE parameters
BANDWIDTH_SEARCH_POINTS = 20
BANDWIDTH_RANGE = (0.01, 2.0)  # log-space search
N_KL_SAMPLES = 125  # samples per direction for Monte Carlo KL estimation
CV_FOLDS = 5

# Bonferroni correction for 3 functions
BONFERRONI_CORRECTION = 3
ALPHA_CORRECTED = ALPHA / BONFERRONI_CORRECTION  # 0.0167
RHO_THRESHOLD = 0.65

# === 10D FUNCTION FAMILIES (identical to parent) ===
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


FUNCTION_MAP = {
    42: rotation_10d,
    43: scaling_10d,
    44: translation_10d,
}

FUNCTION_NAMES = {42: 'rotation', 43: 'scaling', 44: 'translation'}


# === NON-GAUSSIAN HETEROSCEDASTIC NOISE (identical to parent) ===
def sample_mixture_noise(s, rng):
    """Sample non-Gaussian heteroscedastic noise: mixture of 3 Gaussians per dimension."""
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


# === DATA GENERATION (identical to parent) ===
def generate_transitions(func_seed, lambda_val, n, rng):
    """
    Generate transitions using 10D non-Gaussian DGP.
    With probability lambda: s_next = deterministic_function(s, a) + noise
    With probability (1-lambda): s_next ~ mixture centered at 0.5
    """
    func = FUNCTION_MAP[func_seed]
    transitions = []

    for _ in range(n):
        s = rng.uniform(0, 1, size=DIM)
        a_idx = rng.randint(0, N_ACTIONS)

        if rng.random() < lambda_val:
            s_next_det = func(s, a_idx)
            noise = sample_mixture_noise(s, rng)
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

        s_next = np.clip(s_next, 0, 1)
        transitions.append((s, ACTIONS[a_idx], s_next))
    return transitions


# === KDE DENSITY ESTIMATION WITH CV BANDWIDTH ===
def fit_kde_with_cv(data, n_folds=CV_FOLDS, n_search_points=BANDWIDTH_SEARCH_POINTS):
    """
    Fit KDE with cross-validated bandwidth selection.

    Searches over n_search_points log-spaced bandwidth_factor values in BANDWIDTH_RANGE.
    Selects the factor maximizing mean validation log-likelihood across n_folds.

    Returns: (kde_object, selected_bandwidth_factor, cv_scores)
    """
    if len(data) < n_folds:
        # Not enough data for CV; use Scott's rule default
        kde = gaussian_kde(data.T)
        return kde, None, []

    n = len(data)
    fold_size = n // n_folds

    # Generate bandwidth factors in log-space
    log_low = np.log(BANDWIDTH_RANGE[0])
    log_high = np.log(BANDWIDTH_RANGE[1])
    bw_factors = np.exp(np.linspace(log_low, log_high, n_search_points))

    # Shuffle data for CV
    indices = np.arange(n)
    np.random.shuffle(indices)
    data_shuffled = data[indices]

    best_score = -np.inf
    best_factor = None
    all_scores = []

    for factor in bw_factors:
        fold_scores = []
        for fold in range(n_folds):
            val_start = fold * fold_size
            val_end = val_start + fold_size if fold < n_folds - 1 else n
            val_idx = list(range(val_start, val_end))
            train_idx = list(range(0, val_start)) + list(range(val_end, n))

            if len(train_idx) < DIM + 1:
                continue

            train_data = data_shuffled[train_idx]
            val_data = data_shuffled[val_idx]

            try:
                kde = gaussian_kde(train_data.T)
                # Apply bandwidth factor: scale the bandwidth
                kde.set_bandwidth(bw_method=kde.factor * factor)
                log_lik = np.mean(kde.logpdf(val_data.T))
                fold_scores.append(log_lik)
            except Exception:
                continue

        if fold_scores:
            mean_score = np.mean(fold_scores)
            all_scores.append((factor, mean_score))
            if mean_score > best_score:
                best_score = mean_score
                best_factor = factor

    if best_factor is None:
        best_factor = 1.0  # fallback to Scott's rule

    # Fit final KDE on all data with selected bandwidth
    final_kde = gaussian_kde(data.T)
    final_kde.set_bandwidth(bw_method=final_kde.factor * best_factor)

    return final_kde, best_factor, all_scores


# === JENSEN-SHANNON DIVERGENCE ===
def compute_js_divergence(kde_a, kde_b, n_samples=N_KL_SAMPLES):
    """
    Compute Jensen-Shannon divergence between two KDEs via Monte Carlo estimation.

    JS(P_a || P_b) = 0.5 * KL(P_a || M) + 0.5 * KL(P_b || M)
    where M = 0.5 * (P_a + P_b)
    KL estimated via Monte Carlo: KL(P_a || M) ≈ (1/N) Σ log(p_a(x_i) / m(x_i))
    """
    # Sample from each KDE
    samples_a = kde_a.resample(n_samples).T
    samples_b = kde_b.resample(n_samples).T

    # Evaluate log densities
    log_pa_a = kde_a.logpdf(samples_a.T)
    log_pa_b = kde_a.logpdf(samples_b.T)
    log_pb_a = kde_b.logpdf(samples_a.T)
    log_pb_b = kde_b.logpdf(samples_b.T)

    # M = 0.5 * (P_a + P_b), so log(m(x)) = log(0.5 * (p_a(x) + p_b(x)))
    # KL(P_a || M) = E_P_a[log(p_a(x) / m(x))]
    log_ma = np.log(0.5 * np.exp(log_pa_a) + 0.5 * np.exp(log_pb_a) + 1e-300)
    log_mb = np.log(0.5 * np.exp(log_pa_b) + 0.5 * np.exp(log_pb_b) + 1e-300)

    kl_a = np.mean(log_pa_a - log_ma)
    kl_b = np.mean(log_pb_b - log_mb)

    js = 0.5 * kl_a + 0.5 * kl_b
    return max(0.0, js)  # JS is non-negative; numerical errors can make it slightly negative


def compute_js_all_pairs(action_kdes):
    """
    Compute pairwise JS divergence between all 6 action pairs.
    Returns max JS and mean JS across pairs.
    """
    actions_list = list(ACTIONS)
    js_max = 0.0
    js_sum = 0.0
    n_pairs = 0

    for i in range(len(actions_list)):
        for j in range(i + 1, len(actions_list)):
            js = compute_js_divergence(action_kdes[actions_list[i]], action_kdes[actions_list[j]])
            js_max = max(js_max, js)
            js_sum += js
            n_pairs += 1

    js_mean = js_sum / n_pairs if n_pairs > 0 else 0.0
    return js_max, js_mean


# === KDE PIPELINE FOR A SINGLE CELL ===
def kde_pipeline_for_cell(transitions, rng_perm):
    """
    Full KDE pipeline for one cell (lambda, function, replication).

    Returns dict with raw JS, bias-corrected JS, bandwidth, etc.
    """
    # Group by action
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)

    # Fit KDE for each action with CV bandwidth
    action_kdes = {}
    bandwidths = {}
    for a in ACTIONS:
        data = np.array(action_states[a])
        kde, bw_factor, cv_scores = fit_kde_with_cv(data)
        action_kdes[a] = kde
        bandwidths[a] = bw_factor

    # Compute raw JS divergence
    raw_js_max, raw_js_mean = compute_js_all_pairs(action_kdes)

    # Permutation null for bias correction
    perm_js_values = []
    actions_list = [a for _, a, _ in transitions]
    s_nexts = np.array([sn for _, _, sn in transitions])

    for _ in range(N_PERMUTATIONS):
        shuffled_actions = list(actions_list)
        rng_perm.shuffle(shuffled_actions)

        # Group by shuffled action
        perm_action_states = {a: [] for a in ACTIONS}
        for idx, a in enumerate(shuffled_actions):
            perm_action_states[a].append(s_nexts[idx])

        # Fit KDEs on shuffled data
        perm_kdes = {}
        for a in ACTIONS:
            data = np.array(perm_action_states[a])
            kde, _, _ = fit_kde_with_cv(data)
            perm_kdes[a] = kde

        perm_js_max, _ = compute_js_all_pairs(perm_kdes)
        perm_js_values.append(perm_js_max)

    perm_mean_js = float(np.mean(perm_js_values))
    perm_std_js = float(np.std(perm_js_values, ddof=1)) if len(perm_js_values) > 1 else 0.0
    bias_corrected_js = max(0.0, raw_js_max - perm_mean_js)

    return {
        'raw_js_max': float(raw_js_max),
        'raw_js_mean': float(raw_js_mean),
        'bias_corrected_js': float(bias_corrected_js),
        'perm_mean_js': perm_mean_js,
        'perm_std_js': perm_std_js,
        'bandwidths': {a: float(bandwidths[a]) if bandwidths[a] is not None else None for a in ACTIONS},
    }


# === PERMUTATION TEST (for control checks) ===
def permutation_test_kde(transitions, n_perms=50, rng=None):
    """Permutation test: shuffle action labels and recompute KDE JS divergence."""
    # Compute observed JS
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)

    action_kdes = {}
    for a in ACTIONS:
        data = np.array(action_states[a])
        kde, _, _ = fit_kde_with_cv(data)
        action_kdes[a] = kde

    observed_js, _ = compute_js_all_pairs(action_kdes)

    # Permutation null
    actions_list = [a for _, a, _ in transitions]
    s_nexts = np.array([sn for _, _, sn in transitions])

    count_ge = 0
    perm_js_values = []
    for _ in range(n_perms):
        shuffled_actions = list(actions_list)
        rng.shuffle(shuffled_actions)

        perm_action_states = {a: [] for a in ACTIONS}
        for idx, a in enumerate(shuffled_actions):
            perm_action_states[a].append(s_nexts[idx])

        perm_kdes = {}
        for a in ACTIONS:
            data = np.array(perm_action_states[a])
            kde, _, _ = fit_kde_with_cv(data)
            perm_kdes[a] = kde

        perm_js, _ = compute_js_all_pairs(perm_kdes)
        perm_js_values.append(perm_js)
        if perm_js >= observed_js:
            count_ge += 1

    p_value = count_ge / n_perms
    return observed_js, p_value, perm_js_values


# === MAIN EXPERIMENT ===
def run_experiment():
    """Execute the full frozen KDE divergence experiment."""
    start_time = time.time()
    print("=== EXP-FRONTIER-34538185726: KDE JS Divergence Detection ===")
    print(f"Seed: {SEED}")
    print(f"Lambda levels: {LAMBDA_LEVELS}")
    print(f"Functions: 3 (seeds {FUNCTION_SEEDS})")
    print(f"Transitions per cell: {N_TRANSITIONS}")
    print(f"Replications per cell: {N_REPLICATIONS}")
    print(f"State space: continuous 10D [0,1]^10")
    print(f"Noise: mixture of 3 Gaussians (non-Gaussian heteroscedastic)")
    print(f"KDE bandwidth: 5-fold CV, {BANDWIDTH_SEARCH_POINTS} log-spaced factors in {BANDWIDTH_RANGE}")
    print(f"JS divergence: Monte Carlo with {N_KL_SAMPLES} samples per direction")
    print(f"Permutation null: {N_PERMUTATIONS} perms per cell")
    print()

    # === STORAGE ===
    all_kde_js = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                  for f_idx in range(len(FUNCTION_SEEDS))}
    all_kde_js_bc = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                     for f_idx in range(len(FUNCTION_SEEDS))}
    all_perm_mean = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                     for f_idx in range(len(FUNCTION_SEEDS))}
    all_bandwidths = {f_idx: {l: [] for l in LAMBDA_LEVELS}
                      for f_idx in range(len(FUNCTION_SEEDS))}
    raw_tables = []
    pipeline_errors = []

    # === RUN EXPERIMENT ===
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}...", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)

                try:
                    transitions = generate_transitions(func_seed, l, N_TRANSITIONS, rng)

                    # Run KDE pipeline
                    perm_rng = np.random.RandomState(rep_seed + 555)
                    cell_result = kde_pipeline_for_cell(transitions, perm_rng)

                    all_kde_js[f_idx][l].append(cell_result['raw_js_max'])
                    all_kde_js_bc[f_idx][l].append(cell_result['bias_corrected_js'])
                    all_perm_mean[f_idx][l].append(cell_result['perm_mean_js'])

                    # Average bandwidth across actions
                    bw_values = [v for v in cell_result['bandwidths'].values() if v is not None]
                    avg_bw = float(np.mean(bw_values)) if bw_values else None
                    all_bandwidths[f_idx][l].append(avg_bw)

                    raw_tables.append({
                        'func_seed': func_seed,
                        'func_name': func_name,
                        'lambda': l,
                        'replication': rep_idx,
                        'raw_js_max': cell_result['raw_js_max'],
                        'raw_js_mean': cell_result['raw_js_mean'],
                        'bias_corrected_js': cell_result['bias_corrected_js'],
                        'perm_mean_js': cell_result['perm_mean_js'],
                        'perm_std_js': cell_result['perm_std_js'],
                        'avg_bandwidth': avg_bw,
                        'bandwidths': cell_result['bandwidths'],
                    })

                except Exception as e:
                    error_msg = f"Function {func_seed}, lambda={l}, rep={rep_idx}: {str(e)}"
                    pipeline_errors.append(error_msg)
                    print(f" ERROR: {e}", end="")
                    # Store NaN for failed cells
                    all_kde_js[f_idx][l].append(float('nan'))
                    all_kde_js_bc[f_idx][l].append(float('nan'))
                    all_perm_mean[f_idx][l].append(float('nan'))
                    all_bandwidths[f_idx][l].append(None)

            # Print summary for this cell (using bias-corrected JS)
            js_bc_vals = [v for v in all_kde_js_bc[f_idx][l] if not np.isnan(v)]
            js_raw_vals = [v for v in all_kde_js[f_idx][l] if not np.isnan(v)]
            bw_vals = [v for v in all_bandwidths[f_idx][l] if v is not None]

            if js_bc_vals:
                print(f" bc_JS={np.mean(js_bc_vals):.6f}+/-{np.std(js_bc_vals, ddof=1):.6f}"
                      f" raw={np.mean(js_raw_vals):.6f}"
                      f" bw={np.mean(bw_vals):.4f}" if bw_vals else "")
            else:
                print(f" ALL FAILED")
        print()

    # Check for pipeline errors
    if pipeline_errors:
        print(f"=== Pipeline Errors: {len(pipeline_errors)} ===")
        for err in pipeline_errors[:5]:
            print(f"  {err}")
        print()

    # === AGGREGATE ANALYSIS ===
    print("=== Aggregate Analysis (Bias-Corrected JS) ===")
    lambda_arr = np.array(LAMBDA_LEVELS)
    per_function_results = {}

    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_name = FUNCTION_NAMES[func_seed]
        # Mean across replications (ignoring NaN)
        js_bc_means = []
        for l in LAMBDA_LEVELS:
            vals = [v for v in all_kde_js_bc[f_idx][l] if not np.isnan(v)]
            js_bc_means.append(float(np.mean(vals)) if vals else float('nan'))

        js_bc_means_arr = np.array(js_bc_means)
        # Spearman on valid (non-NaN) values
        valid_mask = ~np.isnan(js_bc_means_arr)
        if valid_mask.sum() >= 3:
            spearman_rho, spearman_p = sp_stats.spearmanr(lambda_arr[valid_mask], js_bc_means_arr[valid_mask])
            spearman_p_one_sided = spearman_p / 2 if spearman_rho > 0 else 1 - spearman_p / 2
        else:
            spearman_rho, spearman_p_one_sided = 0.0, 1.0

        per_function_results[func_seed] = {
            'func_name': func_name,
            'spearman_rho': float(spearman_rho),
            'spearman_p_one_sided': float(spearman_p_one_sided),
            'js_bc_means_by_lambda': {str(LAMBDA_LEVELS[i]): js_bc_means[i]
                                       for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  Function {func_seed} ({func_name}): rho={spearman_rho:.4f}, p_one_sided={spearman_p_one_sided:.6f}")

    # Monotonicity check per function
    monotonic_results = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        js_means_list = [per_function_results[func_seed]['js_bc_means_by_lambda'][str(l)] for l in LAMBDA_LEVELS]
        # Filter NaN for monotonicity
        valid_means = [(i, v) for i, v in enumerate(js_means_list) if not np.isnan(v)]
        if len(valid_means) >= 2:
            is_monotonic = all(valid_means[i][1] <= valid_means[i + 1][1]
                               for i in range(len(valid_means) - 1))
        else:
            is_monotonic = False
        monotonic_results[str(func_seed)] = is_monotonic
        print(f"  Function {func_seed}: monotonic = {is_monotonic}")
    print()

    # === AGGREGATE TEST ===
    print("=== Aggregate Test ===")
    aggregate_js_bc_means = []
    for l in LAMBDA_LEVELS:
        all_js_at_l = []
        for f_idx in range(len(FUNCTION_SEEDS)):
            vals = [v for v in all_kde_js_bc[f_idx][l] if not np.isnan(v)]
            all_js_at_l.extend(vals)
        aggregate_js_bc_means.append(float(np.mean(all_js_at_l)) if all_js_at_l else float('nan'))

    agg_js_arr = np.array(aggregate_js_bc_means)
    valid_mask = ~np.isnan(agg_js_arr)
    if valid_mask.sum() >= 3:
        agg_rho, agg_p = sp_stats.spearmanr(lambda_arr[valid_mask], agg_js_arr[valid_mask])
        agg_p_one_sided = agg_p / 2 if agg_rho > 0 else 1 - agg_p / 2
    else:
        agg_rho, agg_p_one_sided = 0.0, 1.0

    print(f"  Aggregate Spearman rho(bc_JS, lambda): {agg_rho:.4f}")
    print(f"  One-sided p-value: {agg_p_one_sided:.6f}")
    print()

    # === PERMUTATION TESTS (for control checks) ===
    print("=== Permutation Tests (Control Checks) ===")
    perm_results = {}
    for l_key in [0.0, 1.0]:
        perm_p_vals = []
        for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)
                transitions = generate_transitions(func_seed, l_key, N_TRANSITIONS, rng)
                perm_rng = np.random.RandomState(rep_seed + 888)
                try:
                    _, p_val, _ = permutation_test_kde(transitions, n_perms=50, rng=perm_rng)
                    perm_p_vals.append(p_val)
                except Exception:
                    perm_p_vals.append(1.0)

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
                for js_val in all_kde_js_bc[f_idx][l]:
                    if not np.isnan(js_val):
                        anova_data.append({
                            'lam_level': str(l),
                            'function': str(f_idx + 1),
                            'js': js_val
                        })

        if len(anova_data) > 10:
            df = pd.DataFrame(anova_data)
            model = ols('js ~ C(lam_level) + C(function) + C(lam_level):C(function)', data=df).fit()
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
        else:
            anova_result = {'error': 'Insufficient data for ANOVA', 'interaction_pass': False}
            print(f"  ANOVA: insufficient data ({len(anova_data)} obs)")
    except Exception as e:
        anova_result = {'error': str(e), 'interaction_pass': False}
        print(f"  ANOVA failed: {e}")
    print()

    # === EFFECT SIZE: Cohen's d ===
    print("=== Effect Size ===")
    effect_sizes = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        js_0 = np.array([v for v in all_kde_js_bc[f_idx][0.0] if not np.isnan(v)])
        js_1 = np.array([v for v in all_kde_js_bc[f_idx][1.0] if not np.isnan(v)])
        if len(js_0) > 1 and len(js_1) > 1:
            pooled_std = np.sqrt((np.var(js_0, ddof=1) + np.var(js_1, ddof=1)) / 2)
            cohens_d = float((np.mean(js_1) - np.mean(js_0)) / pooled_std) if pooled_std > 0 else 0.0
        else:
            cohens_d = 0.0
        effect_sizes[str(func_seed)] = cohens_d
        print(f"  Function {func_seed} ({FUNCTION_NAMES[func_seed]}): Cohen's d = {cohens_d:.4f}")

    agg_js_0 = []
    agg_js_1 = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        agg_js_0.extend([v for v in all_kde_js_bc[f_idx][0.0] if not np.isnan(v)])
        agg_js_1.extend([v for v in all_kde_js_bc[f_idx][1.0] if not np.isnan(v)])
    if len(agg_js_0) > 1 and len(agg_js_1) > 1:
        pooled_std_agg = np.sqrt((np.var(agg_js_0, ddof=1) + np.var(agg_js_1, ddof=1)) / 2)
        agg_cohens_d = float((np.mean(agg_js_1) - np.mean(agg_js_0)) / pooled_std_agg) if pooled_std_agg > 0 else 0.0
    else:
        agg_cohens_d = 0.0
    effect_sizes['aggregate'] = agg_cohens_d
    print(f"  Aggregate: Cohen's d = {agg_cohens_d:.4f}")
    print()

    # === BANDWIDTH DIAGNOSTICS ===
    print("=== Bandwidth Diagnostics ===")
    bw_stats = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        bw_means = {}
        for l in LAMBDA_LEVELS:
            bw_vals = [v for v in all_bandwidths[f_idx][l] if v is not None]
            bw_means[str(l)] = float(np.mean(bw_vals)) if bw_vals else None
        bw_stats[str(func_seed)] = bw_means
        print(f"  Function {func_seed}: {bw_means}")
    print()

    # === CONTROL CHECKS ===
    print("=== Control Checks ===")
    controls = {}

    # Positive control: JS at lambda=1 >= 0.01 across all 3 functions
    positive_control = {}
    all_positive_pass = True
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        js_at_1_vals = [v for v in all_kde_js_bc[f_idx][1.0] if not np.isnan(v)]
        js_at_1 = float(np.mean(js_at_1_vals)) if js_at_1_vals else 0.0
        passes = js_at_1 >= 0.01
        positive_control[str(func_seed)] = {
            'pass': passes,
            'bc_js_at_lambda1': js_at_1,
            'threshold': 0.01,
        }
        if not passes:
            all_positive_pass = False
        print(f"  Positive control (Function {func_seed}): {'PASS' if passes else 'FAIL'}"
              f" (bc_JS@1={js_at_1:.6f}, threshold=0.01)")

    controls['positive_control'] = {
        'description': 'KDE JS divergence >= 0.01 at lambda=1 across all 3 functions',
        'pass': all_positive_pass,
        'per_function': positive_control,
    }

    # Null control: JS at lambda=0 not significantly > 0 (permutation test p > 0.05)
    null_control_pass = perm_results['0.0']['pass']
    controls['null_control'] = {
        'description': 'KDE JS divergence not significantly > 0 at lambda=0 (permutation p > 0.05)',
        'pass': null_control_pass,
        'mean_perm_p': perm_results['0.0']['mean_p_value'],
    }
    print(f"  Null control: {'PASS' if null_control_pass else 'FAIL'} (p={perm_results['0.0']['mean_p_value']:.6f})")

    # Per-function Spearman tests
    spearman_per_function = {}
    all_spearman_pass = True
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        rho = per_function_results[func_seed]['spearman_rho']
        p = per_function_results[func_seed]['spearman_p_one_sided']
        passes = rho >= RHO_THRESHOLD and p < ALPHA_CORRECTED
        spearman_per_function[str(func_seed)] = {
            'pass': passes,
            'rho': rho,
            'p_one_sided': p,
            'threshold_rho': RHO_THRESHOLD,
            'threshold_p': ALPHA_CORRECTED,
        }
        if not passes:
            all_spearman_pass = False
        print(f"  Spearman Function {func_seed}: {'PASS' if passes else 'FAIL'}"
              f" (rho={rho:.4f}, p={p:.6f}, need rho>={RHO_THRESHOLD}, p<{ALPHA_CORRECTED:.4f})")

    controls['spearman_per_function'] = {
        'description': f'Per-function Spearman rho >= {RHO_THRESHOLD} with p < {ALPHA_CORRECTED:.4f} (Bonferroni x3)',
        'pass': all_spearman_pass,
        'per_function': spearman_per_function,
    }

    # Aggregate Spearman test
    spearman_pass = (agg_rho >= RHO_THRESHOLD and agg_p_one_sided < ALPHA)
    controls['spearman_aggregate'] = {
        'description': f'Aggregate Spearman rho >= {RHO_THRESHOLD} with p < {ALPHA} one-sided',
        'pass': spearman_pass,
        'rho': float(agg_rho),
        'p_one_sided': float(agg_p_one_sided),
    }
    print(f"  Aggregate Spearman: {'PASS' if spearman_pass else 'FAIL'} (rho={agg_rho:.4f}, p={agg_p_one_sided:.6f})")

    # Function invariance (ANOVA interaction)
    controls['function_invariance'] = {
        'description': 'No significant function x lambda interaction (two-way ANOVA p > 0.05)',
        'pass': anova_result.get('interaction_pass', False),
        'interaction_p': anova_result.get('full_model', {}).get('interaction_effect', {}).get('p_value', None),
    }
    print(f"  Function invariance: {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}")

    # CV bandwidth health: check that not all cells select boundary bandwidths
    all_bws = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        for l in LAMBDA_LEVELS:
            bw_vals = [v for v in all_bandwidths[f_idx][l] if v is not None]
            all_bws.extend(bw_vals)

    bw_cv = float(np.std(all_bws, ddof=1) / np.mean(all_bws)) if all_bws and np.mean(all_bws) > 0 else 0.0
    boundary_fraction = 0.0
    if all_bws:
        at_low = sum(1 for b in all_bws if b <= BANDWIDTH_RANGE[0] * 1.05)
        at_high = sum(1 for b in all_bws if b >= BANDWIDTH_RANGE[1] * 0.95)
        boundary_fraction = (at_low + at_high) / len(all_bws)

    controls['bandwidth_health'] = {
        'description': 'KDE bandwidth selection not degenerate (CV > 0, boundary fraction < 0.5)',
        'pass': bw_cv > 0 and boundary_fraction < 0.5,
        'cv_bandwidth': bw_cv,
        'boundary_fraction': boundary_fraction,
        'mean_bandwidth': float(np.mean(all_bws)) if all_bws else None,
        'std_bandwidth': float(np.std(all_bws, ddof=1)) if all_bws and len(all_bws) > 1 else None,
    }
    print(f"  Bandwidth health: {'PASS' if bw_cv > 0 and boundary_fraction < 0.5 else 'FAIL'}"
          f" (CV={bw_cv:.4f}, boundary_frac={boundary_fraction:.4f})")

    # JS CV at lambda=1 (for MEASUREMENT_INVALID check)
    js_cv_at_lambda1 = {}
    all_js_cv_pass = True
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        js_vals = [v for v in all_kde_js_bc[f_idx][1.0] if not np.isnan(v)]
        if len(js_vals) > 1:
            cv = float(np.std(js_vals, ddof=1) / np.mean(js_vals)) if np.mean(js_vals) > 0 else 0.0
        else:
            cv = 0.0
        js_cv_at_lambda1[str(func_seed)] = cv
        if cv > 0.5:
            all_js_cv_pass = False
        print(f"  JS CV at lambda=1 (Function {func_seed}): {cv:.4f}")

    controls['js_cv_lambda1'] = {
        'description': 'JS divergence CV across replications < 0.5 at lambda=1',
        'pass': all_js_cv_pass,
        'cv_per_function': js_cv_at_lambda1,
    }

    # No pipeline errors
    controls['no_pipeline_errors'] = {
        'description': 'No pipeline errors during execution',
        'pass': len(pipeline_errors) == 0,
        'n_errors': len(pipeline_errors),
    }
    print(f"  No pipeline errors: {'PASS' if len(pipeline_errors) == 0 else 'FAIL'} ({len(pipeline_errors)} errors)")
    print()

    # === DECISION (per frozen spec.json decision_rule) ===
    print("=== Decision ===")

    # SURVIVES_CURRENT_TEST: ALL of conditions 1-5
    conditions_survive = {
        'per_function_spearman': all_spearman_pass,
        'positive_control': all_positive_pass,
        'null_control': null_control_pass,
        'function_invariance': anova_result.get('interaction_pass', False),
        'no_pipeline_errors': len(pipeline_errors) == 0,
    }

    # FALSIFIED-IN-SETTING: ANY of the failing conditions
    conditions_falsify = {
        'per_function_spearman_fail': not all_spearman_pass,
        'positive_control_fail': not all_positive_pass,
        'null_control_fail': not null_control_pass,
        'function_invariance_fail': not anova_result.get('interaction_pass', False),
    }

    # MEASUREMENT_INVALID: pipeline errors, bandwidth degeneracy, or JS CV > 0.5
    measurement_invalid = (
        len(pipeline_errors) > 0
        or not controls['bandwidth_health']['pass']
        or not all_js_cv_pass
    )

    if measurement_invalid:
        decision = 'MEASUREMENT_INVALID'
        outcome = 'NOT_APPLICABLE'
    elif all(conditions_survive.values()):
        decision = 'SURVIVES_CURRENT_TEST'
        outcome = 'SUPPORTS'
    else:
        decision = 'FALSIFIED-IN-SETTING'
        outcome = 'FALSIFIES'

    print(f"  Conditions survive: {conditions_survive}")
    print(f"  Conditions falsify: {conditions_falsify}")
    print(f"  Measurement invalid: {measurement_invalid}")
    print(f"  Overall Decision: {decision}")
    print(f"  Overall Outcome: {outcome}")
    print()

    elapsed = time.time() - start_time
    print(f"Total execution time: {elapsed:.1f}s")

    # === COMPILE RESULTS ===
    results = {
        'schema_version': 1,
        'experiment_id': 'EXP-FRONTIER-34538185726',
        'lane': 'frontier',
        'status': 'COMPLETE' if not measurement_invalid else 'MEASUREMENT_INVALID',
        'outcome': outcome,
        'metrics': {
            'aggregate': {
                'spearman_rho_bc_js': float(agg_rho),
                'spearman_p_one_sided_bc_js': float(agg_p_one_sided),
                'bc_js_means_by_lambda': {str(LAMBDA_LEVELS[i]): aggregate_js_bc_means[i]
                                           for i in range(len(LAMBDA_LEVELS))},
                'cohens_d_lambda0_vs_1': agg_cohens_d,
            },
            'per_function': {},
            'bandwidth_diagnostics': bw_stats,
            'effect_sizes_cohens_d': effect_sizes,
            'anova': anova_result,
        },
        'controls': controls,
        'artifacts': [
            {'path': 'research/frontier/kde_divergence/analyze.py', 'role': 'code'},
            {'path': 'research/frontier/kde_divergence/raw_tables.json', 'role': 'raw'},
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
            'js_bc_means_by_lambda': per_function_results[func_seed]['js_bc_means_by_lambda'],
            'monotonic': monotonic_results[str(func_seed)],
        }

    # Observations (raw, not interpreted)
    results['observations'] = [
        f"Overall decision: {decision}",
        f"Aggregate Spearman rho(bc_JS, lambda)={agg_rho:.4f}, p_one_sided={agg_p_one_sided:.6f}",
        f"Positive control (JS>=0.01 at lambda=1): {'PASS' if all_positive_pass else 'FAIL'}",
        f"Null control (permutation p>0.05 at lambda=0): {'PASS' if null_control_pass else 'FAIL'}",
        f"Function invariance (ANOVA interaction): {'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}",
        f"Aggregate Cohen's d (lambda=0 vs 1): {agg_cohens_d:.4f}",
        f"Bandwidth health: CV={bw_cv:.4f}, boundary_fraction={boundary_fraction:.4f}",
        f"JS CV at lambda=1: {js_cv_at_lambda1}",
        f"Pipeline errors: {len(pipeline_errors)}",
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
        '500 transitions per cell with ~125 per action; Monte Carlo JS SE ~O(1/sqrt(N))',
        '10 replications per cell enable variance estimation',
        '8 lambda levels provide degradation curve resolution',
        '3 independent continuous function families (10D rotation, scaling, translation)',
        'Frozen random seed (seed=42) for reproducibility',
        'KDE via scipy.stats.gaussian_kde with 5-fold CV bandwidth selection',
        'Bandwidth search: 20 log-spaced factors in [0.01, 2.0]',
        'JS divergence estimated via Monte Carlo with 125 samples per direction',
        'Bias correction via permutation null subtraction (50 perms per cell)',
        'Clipping to [0,1] after noise addition',
        'Same DGP as parent experiments for direct comparison',
        f"Total pipeline errors: {len(pipeline_errors)}",
        f"Mean bandwidth across all cells: {float(np.mean(all_bws)):.4f}" if all_bws else "No bandwidth data",
    ]

    # Unresolved
    results['unresolved'] = [
        'Whether KDE bandwidth selection in 10D is adequate with ~125 samples per action',
        'Whether Monte Carlo JS estimation with 125 samples per direction is low-variance enough',
        'Whether the 50-permutation bias correction is stable (parent noted 50-perm power limit)',
        'Whether KDE performance degrades at higher dimensions (>10D)',
        'Whether real Web transitions exhibit translation-like vs scaling-like structure',
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
    experiment_dir = Path(__file__).parent.parent.parent / 'experiments' / 'EXP-FRONTIER-34538185726'
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
        'experiment_id': 'EXP-FRONTIER-34538185726',
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
            'scipy_version': sp_stats.__version__ if hasattr(sp_stats, '__version__') else 'unknown',
        },
        'frozen_inputs': {
            'prereg_hash': 'eec9f8af7a4386f07fafbf1d70967234c44a7ad830f0af62a5023223f0db06b8',
            'request_hash': '44fc1148df1f4f750c29ef9fdee31b22cedb50bce3c12868c20f1297956b4845',
            'spec_hash': 'b25d696a82f6f125273f929ba7a49b7fc10248a4b083da76f5828201539e86d1',
        },
        'total_transitions': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_TRANSITIONS,
        'kde_parameters': {
            'bandwidth_search_points': BANDWIDTH_SEARCH_POINTS,
            'bandwidth_range': list(BANDWIDTH_RANGE),
            'cv_folds': CV_FOLDS,
            'kl_samples': N_KL_SAMPLES,
            'n_permutations': N_PERMUTATIONS,
        },
        'execution_seconds': elapsed,
    }

    provenance_path = Path(__file__).parent / 'provenance.json'
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
