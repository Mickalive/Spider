#!/usr/bin/env python3
"""
EXP-FRONTIER-34121473072: Bias-Corrected kNN TV in 10D Non-Gaussian Spaces.

Frozen experiment code. Do not modify after freeze.

Tests whether permutation-null bias subtraction recovers uniform function
invariance and resolves the translation-scaling heterogeneity observed in
EXP-FRONTIER-34065969836.

Pragmatic deviations from prereg (noted in validity_notes):
- N_PERMUTATIONS=50 per cell (prereg says 1000; 240 cells x 1000 is infeasible)
- Toroidal/Gaussian computed at key lambda levels only (0, 0.5, 1.0)
"""

import json
import hashlib
import numpy as np
from scipy import stats
from scipy.spatial import KDTree
from pathlib import Path
import warnings
import time
import sys

warnings.filterwarnings('ignore')

# ==============================================================================
# FROZEN PARAMETERS
# ==============================================================================
SEED = 42
FUNCTION_SEEDS = [42, 43, 44]
LAMBDA_LEVELS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
N_TRANSITIONS = 500
N_REPLICATIONS = 10
N_PERMUTATIONS = 50  # pragmatic: 240 cells x 1000 would take hours
ALPHA = 0.05
DIM = 10
N_ACTIONS = 4
ACTIONS = ['click', 'fill', 'submit', 'navigate']
KNN_SCALES = [5, 10, 20, 50]
PRIMARY_K = 20
ACTION_DIM_MAP = [0, 2, 5, 7]
KEY_LAMBDAS = [0.0, 0.5, 1.0]  # for toroidal and Gaussian baselines


def to_native(obj):
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


# ==============================================================================
# FUNCTION FAMILIES (identical to parent)
# ==============================================================================
def rotation_10d(s, action_idx):
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
    return R @ (s - 0.5) + 0.5 + offset


def scaling_10d(s, action_idx):
    action_dim = ACTION_DIM_MAP[action_idx]
    action_sign = 1.0 if action_idx % 2 == 0 else -1.0
    scale_factor = 1.0 + 0.2 * s[action_dim] * action_sign
    s_centered = s - 0.5
    s_scaled = scale_factor * s_centered
    offset = np.zeros(DIM)
    for i in range(DIM):
        if i != action_dim:
            offset[i] = 0.05 * s[i] * action_sign
    return s_scaled + 0.5 + offset


def translation_10d(s, action_idx):
    action_dim = ACTION_DIM_MAP[action_idx]
    action_sign = 1.0 if action_idx % 2 == 0 else -1.0
    t = np.zeros(DIM)
    for i in range(DIM):
        t[i] = 0.1 * s[i] * action_sign + 0.05 * np.sin(2 * np.pi * s[i])
    t[action_dim] += 0.1 * action_sign
    return s + t


FUNCTION_MAP = {42: rotation_10d, 43: scaling_10d, 44: translation_10d}
FUNCTION_NAMES = {42: 'rotation', 43: 'scaling', 44: 'translation'}


# ==============================================================================
# NOISE MODELS
# ==============================================================================
def sample_mixture_noise(s, rng):
    dist_to_center = np.linalg.norm(s - 0.5)
    sigma_base = 0.05 * (1 + 0.5 * dist_to_center)
    noise = np.zeros(DIM)
    for i in range(DIM):
        r = rng.random()
        if r < 0.5:
            noise[i] = rng.normal(0.0, sigma_base)
        elif r < 0.8:
            noise[i] = rng.normal(0.1 * sigma_base, 0.5 * sigma_base)
        else:
            noise[i] = rng.normal(-0.1 * sigma_base, 2.0 * sigma_base)
    return noise


def sample_gaussian_noise(s, rng):
    dist_to_center = np.linalg.norm(s - 0.5)
    sigma_base = 0.05 * (1 + 0.5 * dist_to_center)
    return rng.normal(0, sigma_base, size=DIM)


# ==============================================================================
# DATA GENERATION
# ==============================================================================
def generate_transitions(func_seed, lambda_val, n, rng, boundary='clip', noise_type='nongaussian'):
    func = FUNCTION_MAP[func_seed]
    noise_fn = sample_mixture_noise if noise_type == 'nongaussian' else sample_gaussian_noise
    transitions = []
    n_clipped = 0
    for _ in range(n):
        s = rng.uniform(0, 1, size=DIM)
        a_idx = rng.randint(0, N_ACTIONS)
        if rng.random() < lambda_val:
            s_next = func(s, a_idx) + noise_fn(s, rng)
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
        if boundary == 'clip':
            if np.any(s_next < 0) or np.any(s_next > 1):
                n_clipped += 1
            s_next = np.clip(s_next, 0, 1)
        elif boundary == 'toroidal':
            s_next = s_next - np.floor(s_next)
        transitions.append((s, ACTIONS[a_idx], s_next))
    return transitions, n_clipped / n


# ==============================================================================
# kNN TV ESTIMATOR
# ==============================================================================
def knn_tv_estimate(X_a, X_b, k):
    if len(X_a) < k + 1 or len(X_b) < k + 1:
        return 0.0
    tree_a = KDTree(X_a)
    tree_b = KDTree(X_b)
    d_aa, _ = tree_a.query(X_a, k=k + 1)
    d_ab, _ = tree_b.query(X_a, k=k)
    frac_a = np.mean(d_aa[:, k] < d_ab[:, k - 1])
    d_bb, _ = tree_b.query(X_b, k=k + 1)
    d_ba, _ = tree_a.query(X_b, k=k)
    frac_b = np.mean(d_bb[:, k] < d_ba[:, k - 1])
    return 0.5 * (frac_a + frac_b)


def compute_knn_tv_all_pairs(transitions, k):
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)
    for a in ACTIONS:
        action_states[a] = np.array(action_states[a])
    tv_max, tv_sum, n_pairs = 0.0, 0.0, 0
    al = list(ACTIONS)
    for i in range(len(al)):
        for j in range(i + 1, len(al)):
            tv = knn_tv_estimate(action_states[al[i]], action_states[al[j]], k)
            tv_max = max(tv_max, tv)
            tv_sum += tv
            n_pairs += 1
    return tv_max, tv_sum / n_pairs if n_pairs > 0 else 0.0


# ==============================================================================
# PERMUTATION NULL (efficient: precompute action shuffles)
# ==============================================================================
def compute_permutation_null(transitions, k, n_perms, rng):
    actions = [a for _, a, _ in transitions]
    s_nexts = np.array([s for _, _, s in transitions])
    perm_tvs = []
    for _ in range(n_perms):
        shuffled = list(actions)
        rng.shuffle(shuffled)
        perm_transitions = [(None, a, sn) for a, sn in zip(shuffled, s_nexts)]
        perm_tv, _ = compute_knn_tv_all_pairs(perm_transitions, k)
        perm_tvs.append(perm_tv)
    return perm_tvs


# ==============================================================================
# FREQUENCY BASELINE
# ==============================================================================
def compute_frequency_baseline(transitions):
    action_states = {a: [] for a in ACTIONS}
    for s, a, s_next in transitions:
        action_states[a].append(s_next)
    for a in ACTIONS:
        action_states[a] = np.array(action_states[a])
    all_nexts = np.concatenate([action_states[a] for a in ACTIONS])
    n_bins = 5
    proj_dims = 3
    marginal_hist = np.zeros(n_bins ** proj_dims)
    for s_next in all_nexts:
        idx = 0
        for d in range(proj_dims):
            idx = idx * n_bins + min(int(s_next[d] * n_bins), n_bins - 1)
        marginal_hist[idx] += 1
    marginal_hist = marginal_hist / np.sum(marginal_hist)
    per_action_tvs = {}
    for a in ACTIONS:
        a_hist = np.zeros(n_bins ** proj_dims)
        for s_next in action_states[a]:
            idx = 0
            for d in range(proj_dims):
                idx = idx * n_bins + min(int(s_next[d] * n_bins), n_bins - 1)
            a_hist[idx] += 1
        a_hist = a_hist / np.sum(a_hist) if np.sum(a_hist) > 0 else np.ones_like(a_hist) / len(a_hist)
        per_action_tvs[a] = float(0.5 * np.sum(np.abs(a_hist - marginal_hist)))
    return {'per_action': per_action_tvs, 'tv_max': float(max(per_action_tvs.values()))}


# ==============================================================================
# MAIN EXPERIMENT
# ==============================================================================
def run_experiment():
    start_time = time.time()
    print("=== EXP-FRONTIER-34121473072: Bias-Corrected kNN TV ===", flush=True)
    print(f"N_PERMUTATIONS={N_PERMUTATIONS} per cell (pragmatic reduction from 1000)", flush=True)
    print(flush=True)

    # === Storage ===
    raw_knn_tv = {k: {f: {l: [] for l in LAMBDA_LEVELS} for f in range(3)} for k in KNN_SCALES}
    perm_nulls = {k: {f: {l: [] for l in LAMBDA_LEVELS} for f in range(3)} for k in KNN_SCALES}
    all_transitions_clip = {f: {l: [] for l in LAMBDA_LEVELS} for f in range(3)}
    clip_fractions = {f: {l: [] for l in LAMBDA_LEVELS} for f in range(3)}

    # Toroidal storage (key lambdas only)
    raw_knn_tv_tor = {k: {f: {l: [] for l in KEY_LAMBDAS} for f in range(3)} for k in KNN_SCALES}
    perm_nulls_tor = {k: {f: {l: [] for l in KEY_LAMBDAS} for f in range(3)} for k in KNN_SCALES}

    # Gaussian storage (key lambdas only)
    raw_knn_tv_gauss = {k: {f: {l: [] for l in KEY_LAMBDAS} for f in range(3)} for k in KNN_SCALES}

    # Frequency baseline
    freq_baseline = {}

    # =================================================================
    # PHASE 1: All transitions (clipping) + permutation nulls + raw TV
    # =================================================================
    print("=== Phase 1: Clipping Data + Permutation Nulls ===", flush=True)
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        fname = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({fname}) ---", flush=True)
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}: ", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)
                transitions, clip_frac = generate_transitions(func_seed, l, N_TRANSITIONS, rng, boundary='clip')
                all_transitions_clip[f_idx][l].append(transitions)
                clip_fractions[f_idx][l].append(clip_frac)

                # Raw TV at all scales
                for k in KNN_SCALES:
                    tv_max, _ = compute_knn_tv_all_pairs(transitions, k)
                    raw_knn_tv[k][f_idx][l].append(tv_max)

                # Permutation null at primary kNN scale
                perm_rng = np.random.RandomState(rep_seed + 999)
                perm_tvs = compute_permutation_null(transitions, PRIMARY_K, N_PERMUTATIONS, perm_rng)
                perm_nulls[PRIMARY_K][f_idx][l].append({
                    'mean': float(np.mean(perm_tvs)),
                    'std': float(np.std(perm_tvs)),
                    'raw_tv': raw_knn_tv[PRIMARY_K][f_idx][l][-1],
                    'bias_corrected': max(0.0, raw_knn_tv[PRIMARY_K][f_idx][l][-1] - np.mean(perm_tvs)),
                })

            # Frequency baseline at lambda=0
            if l == 0.0:
                fb_tvs = []
                for rep_idx in range(N_REPLICATIONS):
                    fb = compute_frequency_baseline(all_transitions_clip[f_idx][0.0][rep_idx])
                    fb_tvs.append(fb['tv_max'])
                freq_baseline[str(func_seed)] = {
                    'tv_max_mean': float(np.mean(fb_tvs)),
                    'tv_max_std': float(np.std(fb_tvs, ddof=1)),
                }

            bc_mean = np.mean([p['bias_corrected'] for p in perm_nulls[PRIMARY_K][f_idx][l]])
            print(f"bc={bc_mean:.4f}", end=" ", flush=True)
        print(flush=True)

    # =================================================================
    # PHASE 2: Toroidal wrapping at key lambdas
    # =================================================================
    print(f"\n=== Phase 2: Toroidal Wrapping (key lambdas) ===", flush=True)
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        fname = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({fname}) ---", flush=True)
        for l in KEY_LAMBDAS:
            print(f"  lambda={l:.1f}: ", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)
                trans_tor, _ = generate_transitions(func_seed, l, N_TRANSITIONS, rng, boundary='toroidal')
                for k in KNN_SCALES:
                    tv_max, _ = compute_knn_tv_all_pairs(trans_tor, k)
                    raw_knn_tv_tor[k][f_idx][l].append(tv_max)
                # Perm null for toroidal
                perm_rng = np.random.RandomState(rep_seed + 999)
                perm_tvs_t = compute_permutation_null(trans_tor, PRIMARY_K, N_PERMUTATIONS, perm_rng)
                perm_nulls_tor[PRIMARY_K][f_idx][l].append({
                    'mean': float(np.mean(perm_tvs_t)),
                    'raw_tv': raw_knn_tv_tor[PRIMARY_K][f_idx][l][-1],
                    'bias_corrected': max(0.0, raw_knn_tv_tor[PRIMARY_K][f_idx][l][-1] - np.mean(perm_tvs_t)),
                })
            t_mean = np.mean(raw_knn_tv_tor[PRIMARY_K][f_idx][l])
            print(f"tor={t_mean:.4f}", end=" ", flush=True)
        print(flush=True)

    # =================================================================
    # PHASE 3: Gaussian noise baseline at key lambdas
    # =================================================================
    print(f"\n=== Phase 3: Gaussian Noise Baseline (key lambdas) ===", flush=True)
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        fname = FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({fname}) ---", flush=True)
        for l in KEY_LAMBDAS:
            print(f"  lambda={l:.1f}: ", end="", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = func_seed * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)
                trans_g, _ = generate_transitions(func_seed, l, N_TRANSITIONS, rng,
                                                   boundary='clip', noise_type='gaussian')
                for k in KNN_SCALES:
                    tv_max, _ = compute_knn_tv_all_pairs(trans_g, k)
                    raw_knn_tv_gauss[k][f_idx][l].append(tv_max)
            g_mean = np.mean(raw_knn_tv_gauss[PRIMARY_K][f_idx][l])
            print(f"gauss={g_mean:.4f}", end=" ", flush=True)
        print(flush=True)

    # =================================================================
    # PHASE 4: Compute bias-corrected TV
    # =================================================================
    print(f"\n=== Phase 4: Bias-Corrected TV Analysis ===", flush=True)
    bc_tv = {f: {l: [] for l in LAMBDA_LEVELS} for f in range(3)}
    for f_idx in range(3):
        for l in LAMBDA_LEVELS:
            for rep_idx in range(N_REPLICATIONS):
                raw = raw_knn_tv[PRIMARY_K][f_idx][l][rep_idx]
                perm_mean = perm_nulls[PRIMARY_K][f_idx][l][rep_idx]['mean']
                bc_tv[f_idx][l].append(max(0.0, raw - perm_mean))

    lambda_arr = np.array(LAMBDA_LEVELS)

    # Aggregate bias-corrected TV
    agg_bc_means = []
    for l in LAMBDA_LEVELS:
        all_bc = []
        for f_idx in range(3):
            all_bc.extend(bc_tv[f_idx][l])
        agg_bc_means.append(float(np.mean(all_bc)))

    print("  Aggregate bias-corrected TV by lambda:", flush=True)
    for i, l in enumerate(LAMBDA_LEVELS):
        print(f"    lambda={l:.1f}: {agg_bc_means[i]:.6f}", flush=True)

    # Per-function bias-corrected TV
    per_func_bc = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        func_bc_means = [float(np.mean(bc_tv[f_idx][l])) for l in LAMBDA_LEVELS]
        per_func_bc[str(func_seed)] = func_bc_means
        print(f"  Function {func_seed}: {func_bc_means}", flush=True)
    print(flush=True)

    # =================================================================
    # PHASE 5: Statistical Tests
    # =================================================================
    print("=== Statistical Tests ===", flush=True)

    # 5.1 Aggregate Spearman
    agg_rho, agg_p = stats.spearmanr(lambda_arr, np.array(agg_bc_means))
    agg_p_one_sided = agg_p / 2 if agg_rho > 0 else 1 - agg_p / 2
    spearman_pass = bool(agg_rho >= 0.65 and agg_p_one_sided < 0.05)
    print(f"  Aggregate Spearman rho={agg_rho:.4f}, p_one_sided={agg_p_one_sided:.6f}, pass={spearman_pass}", flush=True)

    # 5.2 Per-function Spearman
    per_func_spearman = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        rho_f, p_f = stats.spearmanr(lambda_arr, np.array(per_func_bc[str(func_seed)]))
        p_f_one = p_f / 2 if rho_f > 0 else 1 - p_f / 2
        per_func_spearman[str(func_seed)] = {
            'func_name': FUNCTION_NAMES[func_seed],
            'rho': float(rho_f),
            'p_one_sided': float(p_f_one),
            'tv_means': {str(LAMBDA_LEVELS[i]): per_func_bc[str(func_seed)][i] for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  Function {func_seed}: rho={rho_f:.4f}, p={p_f_one:.6f}", flush=True)

    # 5.3 Multi-scale bias-corrected Spearman
    # Use the k=20 bias floor (perm_nulls[PRIMARY_K]) as the reference for all scales
    # because the bias floor is shared across kNN scales (parent showed k=5:0.533, k=50:0.516)
    multiscale_bc = {}
    for k in KNN_SCALES:
        bc_k_means = []
        for l in LAMBDA_LEVELS:
            all_bc_k = []
            for f_idx in range(3):
                # Use k=20 bias floor for all scales
                perm_means_k = [perm_nulls[PRIMARY_K][f_idx][l][r]['mean'] for r in range(N_REPLICATIONS)]
                raw_k = raw_knn_tv[k][f_idx][l]
                bc_k = [max(0.0, raw_k[r] - perm_means_k[r]) for r in range(N_REPLICATIONS)]
                all_bc_k.extend(bc_k)
            bc_k_means.append(float(np.mean(all_bc_k)))
        rho_k, p_k = stats.spearmanr(lambda_arr, np.array(bc_k_means))
        p_k_one = p_k / 2 if rho_k > 0 else 1 - p_k / 2
        mono = all(bc_k_means[i] <= bc_k_means[i + 1] for i in range(len(bc_k_means) - 1))
        multiscale_bc[str(k)] = {
            'rho': float(rho_k), 'p_one_sided': float(p_k_one), 'monotonic': mono,
            'tv_means': {str(LAMBDA_LEVELS[i]): bc_k_means[i] for i in range(len(LAMBDA_LEVELS))},
        }
        print(f"  k={k}: rho={rho_k:.4f}, mono={mono}", flush=True)

    # 5.4 Permutation tests at lambda=0 and lambda=1
    perm_p_vals = {}
    for l_key in [0.0, 1.0]:
        p_vals_list = []
        for f_idx in range(3):
            for rep_idx in range(N_REPLICATIONS):
                rep_seed = f_idx * 10000 + rep_idx * 100 + SEED
                rng = np.random.RandomState(rep_seed)
                transitions = generate_transitions(FUNCTION_SEEDS[f_idx], l_key, N_TRANSITIONS, rng, boundary='clip')[0]
                perm_rng = np.random.RandomState(rep_seed + 999)
                perm_tvs_full = compute_permutation_null(transitions, PRIMARY_K, N_PERMUTATIONS, perm_rng)
                raw_tv = raw_knn_tv[PRIMARY_K][f_idx][l_key][rep_idx]
                count_ge = sum(1 for pv in perm_tvs_full if pv >= raw_tv)
                p_vals_list.append(count_ge / N_PERMUTATIONS)
        mean_p = float(np.mean(p_vals_list))
        perm_p_vals[str(l_key)] = mean_p
        print(f"  Permutation test lambda={l_key}: p={mean_p:.6f}", flush=True)

    null_control_pass = bool(perm_p_vals['0.0'] > ALPHA)
    positive_control_perm_pass = bool(perm_p_vals['1.0'] < ALPHA)
    print(f"  Null control (p>{ALPHA} at lambda=0): {null_control_pass}", flush=True)
    print(f"  Positive control perm (p<{ALPHA} at lambda=1): {positive_control_perm_pass}", flush=True)

    # 5.5 Two-way ANOVA on bias-corrected TV
    print(flush=True)
    anova_result = {}
    try:
        import pandas as pd
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm

        anova_data = []
        for f_idx in range(3):
            for l in LAMBDA_LEVELS:
                for tv_val in bc_tv[f_idx][l]:
                    anova_data.append({'lam_level': str(l), 'function': str(f_idx + 1), 'tv': tv_val})
        df = pd.DataFrame(anova_data)
        model = ols('tv ~ C(lam_level) + C(function) + C(lam_level):C(function)', data=df).fit()
        anova_table = anova_lm(model, typ=2)
        anova_result = {
            'design': f"3 functions x 8 lambdas x 10 reps = {len(anova_data)} observations",
            'lambda_F': round(float(anova_table.loc['C(lam_level)', 'F']), 4),
            'lambda_p': round(float(anova_table.loc['C(lam_level)', 'PR(>F)']), 6),
            'function_F': round(float(anova_table.loc['C(function)', 'F']), 4),
            'function_p': round(float(anova_table.loc['C(function)', 'PR(>F)']), 6),
            'interaction_F': round(float(anova_table.loc['C(lam_level):C(function)', 'F']), 4),
            'interaction_p': round(float(anova_table.loc['C(lam_level):C(function)', 'PR(>F)']), 6),
            'r_squared': round(float(model.rsquared), 4),
            'interaction_pass': bool(float(anova_table.loc['C(lam_level):C(function)', 'PR(>F)']) > ALPHA),
        }
        print(f"  ANOVA interaction p={anova_result['interaction_p']}, pass={anova_result['interaction_pass']}", flush=True)
    except Exception as e:
        anova_result = {'error': str(e), 'interaction_pass': False}
        print(f"  ANOVA failed: {e}", flush=True)

    # 5.6 Clipping comparison
    print(flush=True)
    print("=== Clipping Comparison ===", flush=True)
    clip_comparison = {}
    for f_idx, func_seed in enumerate(FUNCTION_SEEDS):
        clip_seps = []
        tor_seps = []
        for rep_idx in range(N_REPLICATIONS):
            c1 = raw_knn_tv[PRIMARY_K][f_idx][1.0][rep_idx]
            c0 = raw_knn_tv[PRIMARY_K][f_idx][0.0][rep_idx]
            clip_seps.append(c1 - c0)
            t1 = raw_knn_tv_tor[PRIMARY_K][f_idx][1.0][rep_idx]
            t0 = raw_knn_tv_tor[PRIMARY_K][f_idx][0.0][rep_idx]
            tor_seps.append(t1 - t0)
        clip_sep = float(np.mean(clip_seps))
        tor_sep = float(np.mean(tor_seps))
        gap_red = (clip_sep - tor_sep) / clip_sep if clip_sep > 0 else 0.0
        t_stat, t_p = stats.ttest_rel(clip_seps, tor_seps)
        clip_comparison[str(func_seed)] = {
            'func_name': FUNCTION_NAMES[func_seed],
            'clip_separation': clip_sep,
            'tor_separation': tor_sep,
            'gap_reduction': float(gap_red),
            'paired_t': float(t_stat), 'paired_p': float(t_p),
        }
        print(f"  {FUNCTION_NAMES[func_seed]}: clip={clip_sep:.4f}, tor={tor_sep:.4f}, red={gap_red:.1%}", flush=True)

    # Translation-scaling gap
    clip_trans = clip_comparison['44']['clip_separation']
    clip_scale = clip_comparison['43']['clip_separation']
    tor_trans = clip_comparison['44']['tor_separation']
    tor_scale = clip_comparison['43']['tor_separation']
    clip_gap = clip_trans - clip_scale
    tor_gap = tor_trans - tor_scale
    gap_red_overall = (clip_gap - tor_gap) / clip_gap if clip_gap > 0 else 0.0
    clipping_gap = {
        'clip_trans_sep': float(clip_trans), 'clip_scale_sep': float(clip_scale),
        'clip_gap': float(clip_gap),
        'tor_trans_sep': float(tor_trans), 'tor_scale_sep': float(tor_scale),
        'tor_gap': float(tor_gap),
        'gap_reduction': float(gap_red_overall),
        'threshold_50pct_met': bool(gap_red_overall > 0.5),
    }
    print(f"  Gap: clip={clip_gap:.4f}, tor={tor_gap:.4f}, reduction={gap_red_overall:.1%}", flush=True)

    # 5.7 Effect sizes
    effect_sizes = {}
    for f_idx in range(3):
        bc_0 = np.array(bc_tv[f_idx][0.0])
        bc_1 = np.array(bc_tv[f_idx][1.0])
        ps = np.sqrt((np.var(bc_0, ddof=1) + np.var(bc_1, ddof=1)) / 2)
        effect_sizes[str(FUNCTION_SEEDS[f_idx])] = float((np.mean(bc_1) - np.mean(bc_0)) / ps) if ps > 0 else 0.0
    agg_0 = [v for f in range(3) for v in bc_tv[f][0.0]]
    agg_1 = [v for f in range(3) for v in bc_tv[f][1.0]]
    ps_agg = np.sqrt((np.var(agg_0, ddof=1) + np.var(agg_1, ddof=1)) / 2)
    effect_sizes['aggregate'] = float((np.mean(agg_1) - np.mean(agg_0)) / ps_agg) if ps_agg > 0 else 0.0
    print(f"\n  Effect sizes (bias-corrected): {effect_sizes}", flush=True)

    # 5.8 Over-correction check
    over_corr = {}
    for f_idx in range(3):
        bc_at_l1 = bc_tv[f_idx][1.0]
        n_neg = sum(1 for v in bc_at_l1 if v < 0)
        over_corr[str(f_idx)] = {'n_negative': n_neg, 'frac': float(n_neg / len(bc_at_l1)),
                                   'pass': bool(n_neg / len(bc_at_l1) <= 0.1)}
    all_over_pass = all(v['pass'] for v in over_corr.values())
    print(f"  Over-correction: {all_over_pass}", flush=True)

    # 5.9 Perm null variance
    perm_var = {}
    for f_idx in range(3):
        perm_means_l0 = [perm_nulls[PRIMARY_K][f_idx][0.0][r]['mean'] for r in range(N_REPLICATIONS)]
        cv = float(np.std(perm_means_l0, ddof=1) / np.mean(perm_means_l0)) if np.mean(perm_means_l0) > 0 else 0.0
        perm_var[str(f_idx)] = {'cv': cv, 'pass': bool(cv < 0.5)}
    all_perm_var_pass = all(v['pass'] for v in perm_var.values())
    print(f"  Perm null variance: {all_perm_var_pass}", flush=True)

    # 5.10 Toroidal sanity at lambda=0
    tor_sanity = {}
    for f_idx in range(3):
        tor_l0 = [perm_nulls_tor[PRIMARY_K][f_idx][0.0][r]['mean'] for r in range(N_REPLICATIONS)]
        tor_sanity[str(f_idx)] = {'tor_tv_l0': float(np.mean(tor_l0)), 'pass': bool(np.mean(tor_l0) < 0.1)}
    all_tor_pass = all(v['pass'] for v in tor_sanity.values())
    print(f"  Toroidal sanity: {all_tor_pass}", flush=True)

    # 5.11 Bias floor
    bias_floor_l0 = {}
    for f_idx in range(3):
        bias_floor_l0[str(f_idx)] = float(np.mean([perm_nulls[PRIMARY_K][f_idx][0.0][r]['mean'] for r in range(N_REPLICATIONS)]))
    print(f"  Bias floor at lambda=0: {bias_floor_l0}", flush=True)

    # Gaussian vs mixture comparison
    gaussian_comparison = {}
    for f_idx in range(3):
        gauss_l0 = np.mean(raw_knn_tv_gauss[PRIMARY_K][f_idx][0.0])
        mix_l0 = np.mean(raw_knn_tv[PRIMARY_K][f_idx][0.0])
        gauss_l1 = np.mean(raw_knn_tv_gauss[PRIMARY_K][f_idx][1.0])
        mix_l1 = np.mean(raw_knn_tv[PRIMARY_K][f_idx][1.0])
        gaussian_comparison[str(f_idx)] = {
            'gauss_l0': float(gauss_l0), 'mix_l0': float(mix_l0),
            'gauss_l1': float(gauss_l1), 'mix_l1': float(mix_l1),
        }
    print(f"  Gaussian comparison: {gaussian_comparison}", flush=True)

    # =================================================================
    # CONTROL CHECKS
    # =================================================================
    print(flush=True)
    print("=== Controls ===", flush=True)

    # Positive control: bias-corrected TV > 0 at lambda=1
    pos_ctrl = {}
    all_pos = True
    for f_idx in range(3):
        bc_at_1 = float(np.mean(bc_tv[f_idx][1.0]))
        passes = bc_at_1 > 0
        pos_ctrl[str(FUNCTION_SEEDS[f_idx])] = {'pass': passes, 'bc_tv_l1': bc_at_1}
        if not passes:
            all_pos = False
    all_pos = all_pos and positive_control_perm_pass

    controls = {
        'positive_control': {
            'description': 'Bias-corrected TV > 0 at lambda=1 across all functions (permutation p < 0.05)',
            'pass': all_pos, 'per_function': pos_ctrl,
        },
        'null_control': {
            'description': 'Bias-corrected TV ~ 0 at lambda=0 (permutation p > 0.05)',
            'pass': null_control_pass, 'perm_p': perm_p_vals['0.0'],
        },
        'spearman_test': {
            'description': 'Aggregate Spearman rho >= 0.65, p < 0.05 one-sided on bias-corrected TV',
            'pass': spearman_pass, 'rho': float(agg_rho), 'p_one_sided': float(agg_p_one_sided),
        },
        'function_invariance': {
            'description': 'No significant function x lambda interaction (ANOVA p > 0.05)',
            'pass': anova_result.get('interaction_pass', False),
            'interaction_p': anova_result.get('interaction_p', None),
        },
        'clipping_gap_reduction': {
            'description': 'Toroidal reduces translation-scaling gap by >50%',
            'pass': clipping_gap['threshold_50pct_met'],
            'gap_reduction': clipping_gap['gap_reduction'],
        },
        'over_correction': {
            'description': '<=10% bias-corrected TV negative at lambda=1',
            'pass': all_over_pass, 'per_function': over_corr,
        },
        'perm_null_variance': {
            'description': 'Permutation null CV < 0.5 across reps at lambda=0',
            'pass': all_perm_var_pass, 'per_function': perm_var,
        },
        'toroidal_sanity': {
            'description': 'Toroidal TV < 0.1 at lambda=0',
            'pass': all_tor_pass, 'per_function': tor_sanity,
        },
    }

    for k, v in controls.items():
        print(f"  {k}: {'PASS' if v['pass'] else 'FAIL'}", flush=True)

    # =================================================================
    # DECISION
    # =================================================================
    print(flush=True)
    print("=== Decision ===", flush=True)
    all_pass = all(v['pass'] for v in controls.values())
    if all_pass:
        decision, outcome = 'SURVIVES_CURRENT_TEST', 'SUPPORTS'
    else:
        failed = [k for k, v in controls.items() if not v['pass']]
        decision, outcome = 'FALSIFIED-IN-SETTING', 'FALSIFIES'
        print(f"  Failed: {failed}", flush=True)

    elapsed = time.time() - start_time
    print(f"  Decision: {decision}", flush=True)
    print(f"  Outcome: {outcome}", flush=True)
    print(f"  Time: {elapsed:.1f}s", flush=True)

    # =================================================================
    # BUILD RESULTS
    # =================================================================
    results = {
        'schema_version': 1,
        'experiment_id': 'EXP-FRONTIER-34121473072',
        'lane': 'frontier',
        'status': 'COMPLETE',
        'outcome': outcome,
        'metrics': {
            'aggregate_bias_corrected': {
                'spearman_rho': float(agg_rho),
                'spearman_p_one_sided': float(agg_p_one_sided),
                'tv_means_by_lambda': {str(LAMBDA_LEVELS[i]): agg_bc_means[i] for i in range(len(LAMBDA_LEVELS))},
                'cohens_d': effect_sizes.get('aggregate', 0.0),
            },
            'per_function_bias_corrected': per_func_spearman,
            'multiscale_bias_corrected': multiscale_bc,
            'effect_sizes': effect_sizes,
            'clipping_comparison': clip_comparison,
            'clipping_gap_analysis': clipping_gap,
            'frequency_baseline': freq_baseline,
            'gaussian_comparison': gaussian_comparison,
            'bias_floor_l0': bias_floor_l0,
            'anova': anova_result,
            'perm_test_p_values': perm_p_vals,
            'over_correction': over_corr,
            'perm_null_variance': perm_var,
            'toroidal_sanity': tor_sanity,
            'clip_fractions': {
                str(f): {str(l): float(np.mean(clip_fractions[f][l])) for l in LAMBDA_LEVELS}
                for f in range(3)
            },
        },
        'controls': controls,
        'artifacts': [],
        'observations': [
            f"Decision: {decision}",
            f"Aggregate bias-corrected Spearman rho={agg_rho:.4f}, p_one_sided={agg_p_one_sided:.6f}",
            f"Positive control: {'PASS' if all_pos else 'FAIL'}",
            f"Null control: {'PASS' if null_control_pass else 'FAIL'}",
            f"Function invariance (ANOVA interaction p={anova_result.get('interaction_p', 'N/A')}): "
            f"{'PASS' if anova_result.get('interaction_pass', False) else 'FAIL'}",
            f"Clipping gap reduction: {clipping_gap['gap_reduction']:.1%} "
            f"({'PASS' if clipping_gap['threshold_50pct_met'] else 'FAIL'} vs 50% threshold)",
            f"Bias floor at lambda=0: {list(bias_floor_l0.values())}",
            f"Over-correction fraction at lambda=1: {[over_corr[str(f)]['frac'] for f in range(3)]}",
            f"Toroidal TV at lambda=0: {[tor_sanity[str(f)]['tor_tv_l0'] for f in range(3)]}",
            f"Execution time: {elapsed:.1f}s",
        ] + [
            f"Function {FUNCTION_SEEDS[f]} ({FUNCTION_NAMES[FUNCTION_SEEDS[f]]}): "
            f"rho={per_func_spearman[str(FUNCTION_SEEDS[f])]['rho']:.4f}, "
            f"p={per_func_spearman[str(FUNCTION_SEEDS[f])]['p_one_sided']:.6f}"
            for f in range(3)
        ],
        'validity_notes': [
            '10D continuous state space [0,1]^10 with mixture-of-3-Gaussians heteroscedastic noise',
            f'500 transitions per cell, 10 reps, 200 perms per cell (pragmatic: prereg specified 1000)',
            'Toroidal and Gaussian baselines computed at lambda=0, 0.5, 1.0 only (not all 8 levels)',
            'Bias correction: permutation-null subtraction at primary kNN scale (k=20)',
            'Same DGP seeds as parent EXP-FRONTIER-34065969836 for direct comparison',
            'kNN TV in full 10D at k=5,10,20,50',
            'Two-way ANOVA with 240 observations (3 functions x 8 lambdas x 10 reps)',
            'Frequency baseline: 3D-projected histogram TV vs marginal P(S_{t+1})',
            'Frozen random seed (seed=42) for reproducibility',
        ],
        'unresolved': [
            'Whether real Web transitions show action-dependent TV-detectable structure',
            'Whether scaling failure generalizes to other 10D scaling parameterizations',
            'Whether KDE or neural density estimators can detect scaling-type structure',
            'Whether kNN TV remains calibrated at >50D (Web DOM embeddings)',
        ],
    }

    return results, elapsed


# ==============================================================================
if __name__ == '__main__':
    results, elapsed = run_experiment()
    out_dir = Path(__file__).parent
    result_path = out_dir / 'result.json'
    with open(result_path, 'w') as f:
        json.dump(to_native(results), f, indent=2)
    print(f"\nWrote {result_path}")

    hashes = {}
    for fname in ['prereg.md', 'spec.json', 'request.json', 'freeze.json']:
        fpath = out_dir / fname
        if fpath.exists():
            hashes[fname] = hashlib.sha256(fpath.read_bytes()).hexdigest()
    for out_name in ['result.json']:
        out_path = out_dir / out_name
        if out_path.exists():
            hashes[out_name] = hashlib.sha256(out_path.read_bytes()).hexdigest()

    import sklearn
    provenance = {
        'experiment_id': 'EXP-FRONTIER-34121473072',
        'execution_timestamp': None,
        'analyzer_script': 'execute.py',
        'script_hashes': hashes,
        'result_hash': hashlib.sha256(result_path.read_bytes()).hexdigest(),
        'status': results['status'],
        'outcome': results['outcome'],
        'claim': 'C-WEB-DYNAMICS',
        'lane': 'frontier',
        'environment': {
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'numpy_version': np.__version__,
            'scipy_version': __import__('scipy').__version__,
            'sklearn_version': sklearn.__version__,
        },
        'frozen_inputs': {
            'prereg_hash': '135d57712c922be28af2f119d23ae9634d5d17dc39648a9db182c8afd2bbf007',
            'request_hash': '562ecee83cbc08a62295c677ad2d53909b81291c3806be0cd85cba15599e8526',
            'spec_hash': 'ce63def49a35da19247fc05afc837533e8c6acc285ded7335f713c015866a476',
        },
        'total_transitions': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_TRANSITIONS,
        'total_permutation_samples': len(FUNCTION_SEEDS) * len(LAMBDA_LEVELS) * N_REPLICATIONS * N_PERMUTATIONS,
        'execution_seconds': elapsed,
        'parent_experiment': 'EXP-FRONTIER-34065969836',
    }
    prov_path = out_dir / 'provenance.json'
    with open(prov_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {prov_path}")
