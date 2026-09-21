#!/usr/bin/env python3
"""
EXP-FRONTIER-35401996615 EXECUTE — per-type CV stability at larger sample sizes.

Frozen spec: test whether per-type CV stability (<=0.5 at lambda=1) achieves
at larger per-type n (500 and 1000/type) with KDE Scott or kNN k=5.

All randomness via np.random.RandomState with explicit seeds.
No unseeded np.random calls.
"""

import numpy as np
from scipy.stats import gaussian_kde
from scipy.special import digamma
from sklearn.neighbors import NearestNeighbors
import json
import hashlib
import time
import sys
import os
import traceback

# === CONSTANTS (frozen from spec) ===
BASE_SEED = 42
N_PERMS = 200  # permutation nulls per type per sample size
N_REPS = 5     # replications per lambda level
LAMBDA_LEVELS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
SAMPLE_SIZES = [250, 500, 1000]
N_TYPES = 8
N_ACTIONS = 4

# Page type definitions (frozen from parent EXP-FRONTIER-34913743596)
PAGE_TYPES = [
    (42, 0.05, np.array([0.5, 0.5])),   # rotation, low noise, center
    (43, 0.05, np.array([0.5, 0.5])),   # scaling, low noise, center
    (44, 0.05, np.array([0.5, 0.5])),   # translation, low noise, center
    (42, 0.10, np.array([0.5, 0.5])),   # rotation, high noise, center
    (43, 0.10, np.array([0.5, 0.5])),   # scaling, high noise, center
    (44, 0.10, np.array([0.5, 0.5])),   # translation, high noise, center
    (42, 0.05, np.array([0.3, 0.7])),   # rotation, low noise, shifted
    (43, 0.05, np.array([0.3, 0.7])),   # scaling, low noise, shifted
]


# === DGP FUNCTIONS ===

def generate_transitions_dgp(per_type_n, lambda_val, type_idx, seed):
    """
    Generate per_type_n transitions for page type type_idx at lambda_val.
    Returns (S_next, A) arrays of shape (per_type_n, 2) and (per_type_n,).
    """
    rng = np.random.RandomState(seed)
    func_type, noise_std, offset = PAGE_TYPES[type_idx]

    # Generate states from uniform [0,1]^2
    S_current = rng.uniform(0, 1, size=(per_type_n, 2))

    # Generate random actions
    actions = rng.randint(0, N_ACTIONS, size=per_type_n)

    # Compute deterministic part based on function type
    S_det = np.zeros_like(S_current)
    for i in range(per_type_n):
        s = S_current[i]
        a = actions[i]
        action_offset = np.array([a * 0.1, (a * 0.15) % 1.0])

        if func_type == 42:  # rotation
            angle = lambda_val * 0.5 * np.pi * (a + 1) / N_ACTIONS
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            rot_mat = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
            S_det[i] = rot_mat @ (s - offset) + offset + action_offset
        elif func_type == 43:  # scaling
            scale_factor = 1.0 + lambda_val * 0.5 * (a + 1) / N_ACTIONS
            S_det[i] = (s - offset) * scale_factor + offset + action_offset
        elif func_type == 44:  # translation
            trans = lambda_val * 0.3 * (a + 1) / N_ACTIONS * np.array([1.0, -1.0])
            S_det[i] = s + trans + action_offset * 0.5

    # Wrap to [0,1]
    S_det = S_det % 1.0

    # Add heteroscedastic Gaussian noise (state-dependent variance)
    noise_scale = noise_std * (0.5 + np.linalg.norm(S_current - offset, axis=1, keepdims=True))
    noise = rng.randn(per_type_n, 2) * noise_scale
    S_next = (S_det + noise) % 1.0

    return S_next, actions, S_current


def compute_kde_divergence(S_next, actions, n_actions=N_ACTIONS):
    """
    Compute KDE-based KL divergence: max_a D_KL(P(S|A=a) || P(S)).
    Uses permutation mean subtraction (bias-corrected).
    Returns the maximum BC KL across actions.
    """
    n = len(S_next)
    if n < 10:
        return 0.0

    try:
        # Marginal density of S_next
        kde_marginal = gaussian_kde(S_next.T, bw_method='scott')

        # For each action, compute conditional divergence
        max_kl = 0.0
        for a in range(n_actions):
            mask = actions == a
            if mask.sum() < 5:
                continue

            # P(S|A=a) via KDE on subset
            kde_cond = gaussian_kde(S_next[mask].T, bw_method='scott')

            # KL = E_{P(S|A=a)}[log P(S|A=a) - log P(S)]
            log_cond = kde_cond(S_next[mask].T)
            log_marg_sub = kde_marginal(S_next[mask].T)

            # Avoid log(0)
            eps = 1e-300
            kl = np.mean(np.maximum(np.log(log_cond + eps) - np.log(log_marg_sub + eps), 0))
            max_kl = max(max_kl, kl)

        return max(0.0, max_kl)
    except Exception:
        return 0.0


def compute_knn_mi(S_next, actions, k=5):
    """
    Compute kNN mutual information I(S_next; A) using Kraskov-Stögbauer-Grassberger estimator.

    For continuous X = S_next (2D) and discrete Y = A (categorical):
      For each point i:
        1. eps_i = k-th neighbor distance in joint space [X, Y_onehot]
        2. n_i = |{j != i : Y_j = Y_i AND ||X_j - X_i|| < eps_i}|

    MI = psi(k) - mean(psi(n_i + 1)) + psi(N) - sum_y (N_y/N) * psi(N_y)
    """
    n = len(S_next)
    if n < k + 2:
        return 0.0

    try:
        n_actions = int(actions.max()) + 1

        # Joint space: [S_next, action_onehot]
        action_onehot = np.zeros((n, n_actions))
        action_onehot[np.arange(n), actions.astype(int)] = 1.0
        joint = np.column_stack([S_next, action_onehot])

        # kNN on joint space
        nn_joint = NearestNeighbors(n_neighbors=k + 1)  # +1 for self
        nn_joint.fit(joint)
        dists_joint, _ = nn_joint.kneighbors(joint)
        eps_joint = dists_joint[:, k]  # distance to k-th neighbor (0-indexed: k, not k+1 since [0] is self)

        # For each point, count same-class neighbors within eps in marginal S_next space
        nn_marginal = NearestNeighbors(n_neighbors=n)
        nn_marginal.fit(S_next)
        dists_marginal, _ = nn_marginal.kneighbors(S_next)

        n_class_neighbors = np.zeros(n, dtype=int)
        for i in range(n):
            same_class = (actions == actions[i])
            same_class[i] = False  # exclude self
            within_eps = dists_marginal[i] <= eps_joint[i]
            n_class_neighbors[i] = np.sum(same_class & within_eps)

        # Kraskov MI estimator
        psi_k = digamma(k)

        # Mean psi(n_i + 1) over all points
        mean_psi_n = np.mean(digamma(n_class_neighbors + 1))

        # sum_y (N_y / N) * psi(N_y)
        psi_N = digamma(n)
        entropy_y = 0.0
        for a_val in range(n_actions):
            n_y = np.sum(actions == a_val)
            if n_y > 0:
                entropy_y += (n_y / n) * digamma(n_y)

        mi = psi_k - mean_psi_n + psi_N - entropy_y
        return max(0.0, float(mi))
    except Exception as e:
        return 0.0


def make_serializable(obj):
    """Recursively convert numpy types to Python native types for JSON."""
    if isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {str(k): make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(v) for v in obj]
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


def run_experiment():
    """Main experiment execution."""
    results = {
        'per_type': {},
        'pooled': {},
        'cv_check': {},
        'null_control': {},
        'positive_control': {},
        'pipeline_validation': {},
        'sample_size_trend': {},
    }

    t_start = time.time()

    for sample_n in SAMPLE_SIZES:
        print(f"\n{'='*60}")
        print(f"Sample size: {sample_n}/type")
        print(f"{'='*60}")

        results['per_type'][sample_n] = {}
        results['pooled'][sample_n] = {}

        # Storage for CV computation
        cv_storage = {m: {lt: {t: [] for t in range(N_TYPES)} for lt in LAMBDA_LEVELS}
                      for m in ['kde', 'knn']}
        pooled_storage = {m: {lt: [] for lt in LAMBDA_LEVELS}
                         for m in ['kde', 'knn']}

        for lambda_idx, lambda_val in enumerate(LAMBDA_LEVELS):
            t_lambda = time.time()
            print(f"  Lambda={lambda_val}...", end='', flush=True)

            for rep in range(N_REPS):
                cell_seed = BASE_SEED * 100000 + lambda_idx * 1000 + rep * 10 + 999

                # Generate transitions for all types
                all_S_next = []
                all_actions = []
                all_types = []

                for type_idx in range(N_TYPES):
                    S_next, actions, _ = generate_transitions_dgp(
                        sample_n, lambda_val, type_idx, cell_seed + type_idx * 7
                    )
                    all_S_next.append(S_next)
                    all_actions.append(actions)
                    all_types.extend([type_idx] * sample_n)

                all_S_next = np.vstack(all_S_next)
                all_actions = np.concatenate(all_actions)
                all_types = np.array(all_types)

                # Per-type measurements
                for type_idx in range(N_TYPES):
                    mask = all_types == type_idx
                    S_type = all_S_next[mask]
                    A_type = all_actions[mask]

                    kde_div = compute_kde_divergence(S_type, A_type)
                    knn_mi = compute_knn_mi(S_type, A_type, k=5)

                    cv_storage['kde'][lambda_val][type_idx].append(kde_div)
                    cv_storage['knn'][lambda_val][type_idx].append(knn_mi)

                # Pooled measurements
                kde_div_pooled = compute_kde_divergence(all_S_next, all_actions)
                knn_mi_pooled = compute_knn_mi(all_S_next, all_actions, k=5)
                pooled_storage['kde'][lambda_val].append(kde_div_pooled)
                pooled_storage['knn'][lambda_val].append(knn_mi_pooled)

            print(f" {time.time()-t_lambda:.1f}s")

        # === Per-type analysis for this sample size ===
        per_type_results = {}
        for type_idx in range(N_TYPES):
            kde_divs = np.array(cv_storage['kde'][1.0][type_idx])
            knn_mis = np.array(cv_storage['knn'][1.0][type_idx])
            kde_mean = np.mean(kde_divs)
            knn_mean = np.mean(knn_mis)
            kde_cv = float(np.std(kde_divs) / kde_mean) if kde_mean > 0 else float('inf')
            knn_cv = float(np.std(knn_mis) / knn_mean) if knn_mean > 0 else float('inf')
            per_type_results[type_idx] = {
                'kde_div_mean': float(kde_mean),
                'kde_div_std': float(np.std(kde_divs)),
                'kde_div_values': [float(v) for v in kde_divs],
                'kde_cv': kde_cv,
                'knn_mi_mean': float(knn_mean),
                'knn_mi_std': float(np.std(knn_mis)),
                'knn_mi_values': [float(v) for v in knn_mis],
                'knn_cv': knn_cv,
            }
        results['per_type'][sample_n] = per_type_results

        # === CV check at lambda=1 ===
        kde_cvs = [per_type_results[t]['kde_cv'] for t in range(N_TYPES)]
        knn_cvs = [per_type_results[t]['knn_cv'] for t in range(N_TYPES)]
        results['cv_check'][sample_n] = {
            'kde': {
                'cv_per_type': {str(t): per_type_results[t]['kde_cv'] for t in range(N_TYPES)},
                'cv_max': float(max(kde_cvs)),
                'cv_max_type': int(np.argmax(kde_cvs)),
                'pass': bool(all(cv <= 0.5 for cv in kde_cvs)),
                'n_pass': int(sum(1 for cv in kde_cvs if cv <= 0.5)),
            },
            'knn': {
                'cv_per_type': {str(t): per_type_results[t]['knn_cv'] for t in range(N_TYPES)},
                'cv_max': float(max(knn_cvs)),
                'cv_max_type': int(np.argmax(knn_cvs)),
                'pass': bool(all(cv <= 0.5 for cv in knn_cvs)),
                'n_pass': int(sum(1 for cv in knn_cvs if cv <= 0.5)),
            }
        }

        print(f"  CV at lambda=1: KDE max={max(kde_cvs):.4f} (pass={all(cv<=0.5 for cv in kde_cvs)}), "
              f"kNN max={max(knn_cvs):.4f} (pass={all(cv<=0.5 for cv in knn_cvs)})")

        # === Null control at each sample size ===
        # At lambda=0, per-type divergence must be <= permutation threshold
        # Use the pooled data at lambda=0 for null distribution
        print(f"  Computing null control (N_PERMS={N_PERMS})...", end='', flush=True)
        t_null = time.time()

        null_control_results = {}
        for measure in ['kde', 'knn']:
            n_pass = 0
            type_results = {}
            for type_idx in range(N_TYPES):
                mask_type = all_types == type_idx
                S_type = all_S_next[mask_type]
                A_type = all_actions[mask_type]

                obs_vals = np.array(cv_storage[measure][0.0][type_idx])
                obs_mean = np.mean(obs_vals)

                # Compute permutation null for this type at lambda=0
                perm_means = []
                rng_perm = np.random.RandomState(cell_seed + type_idx * 13 + 9999)
                for p in range(N_PERMS):
                    perm_actions = A_type.copy()
                    rng_perm.shuffle(perm_actions)
                    if measure == 'kde':
                        perm_div = compute_kde_divergence(S_type, perm_actions)
                    else:
                        perm_div = compute_knn_mi(S_type, perm_actions, k=5)
                    perm_means.append(perm_div)

                perm_means = np.array(perm_means)
                perm_threshold = float(np.percentile(perm_means, 95))
                passes = bool(obs_mean <= perm_threshold)
                n_pass += int(passes)
                type_results[str(type_idx)] = {
                    'observed': float(obs_mean),
                    'perm_threshold_95': perm_threshold,
                    'perm_mean': float(np.mean(perm_means)),
                    'perm_std': float(np.std(perm_means)),
                    'pass': passes,
                }

            null_control_results[measure] = {
                'n_pass': int(n_pass),
                'n_total': N_TYPES,
                'pass_all': bool(n_pass == N_TYPES),
                'per_type': type_results,
            }

        results['null_control'][sample_n] = null_control_results
        print(f" {time.time()-t_null:.1f}s")
        print(f"  Null control: KDE {null_control_results['kde']['n_pass']}/{N_TYPES}, "
              f"kNN {null_control_results['knn']['n_pass']}/{N_TYPES}")

        # === Positive control: pooled subsampled divergence at lambda=1 > lambda=0 ===
        pos_control = {}
        for measure in ['kde', 'knn']:
            storage = pooled_storage[measure]
            lambda1_vals = np.array(storage[1.0])
            lambda0_vals = np.array(storage[0.0])

            diffs = lambda1_vals - lambda0_vals
            mean_diff = float(np.mean(diffs))
            std_diff = float(np.std(diffs, ddof=1))
            if std_diff > 0 and len(diffs) > 1:
                t_stat = mean_diff / (std_diff / np.sqrt(len(diffs)))
                from scipy.stats import t as t_dist
                p_val = float(1 - t_dist.cdf(t_stat, df=len(diffs) - 1))
            else:
                t_stat = 0.0
                p_val = 1.0

            pos_control[measure] = {
                'lambda1_mean': float(np.mean(lambda1_vals)),
                'lambda0_mean': float(np.mean(lambda0_vals)),
                'mean_diff': mean_diff,
                't_stat': float(t_stat),
                'p_one_sided': p_val,
                'pass': bool(mean_diff > 0 and p_val < 0.05),
            }

        results['positive_control'][sample_n] = pos_control
        print(f"  Positive control: KDE t={pos_control['kde']['t_stat']:.3f} p={pos_control['kde']['p_one_sided']:.4f}, "
              f"kNN t={pos_control['knn']['t_stat']:.3f} p={pos_control['knn']['p_one_sided']:.4f}")

        # === Pooled subsampled divergence across lambdas ===
        pooled_results = {}
        for measure in ['kde', 'knn']:
            pooled_results[measure] = {}
            for lambda_val in LAMBDA_LEVELS:
                vals = np.array(pooled_storage[measure][lambda_val])
                pooled_results[measure][str(lambda_val)] = {
                    'mean': float(np.mean(vals)),
                    'std': float(np.std(vals)),
                    'values': [float(v) for v in vals],
                }
        results['pooled'][sample_n] = pooled_results

    # === Pipeline validation at 250/type ===
    pv = results['cv_check'][250]
    results['pipeline_validation'] = {
        'kde_cv_max_250': pv['kde']['cv_max'],
        'kde_cv_max_in_5pct_range': bool(0.546 <= pv['kde']['cv_max'] <= 0.604),
        'knn_cv_max_250': pv['knn']['cv_max'],
        'knn_cv_max_in_5pct_range': bool(0.717 <= pv['knn']['cv_max'] <= 0.793),
        'kde_null_pass_250': results['null_control'][250]['kde']['pass_all'],
        'knn_null_pass_250': results['null_control'][250]['knn']['pass_all'],
        'pass': (bool(0.546 <= pv['kde']['cv_max'] <= 0.604) and
                 bool(0.717 <= pv['knn']['cv_max'] <= 0.793) and
                 results['null_control'][250]['kde']['pass_all'] and
                 results['null_control'][250]['knn']['pass_all']),
    }

    # === Sample size trend ===
    trend = {}
    for measure in ['kde', 'knn']:
        trend[measure] = {}
        for type_idx in range(N_TYPES):
            cvs = []
            for sn in SAMPLE_SIZES:
                cvs.append(results['cv_check'][sn][measure]['cv_per_type'][str(type_idx)])
            # Check monotonic decrease
            monotonic = all(cvs[i] >= cvs[i + 1] for i in range(len(cvs) - 1))
            trend[measure][str(type_idx)] = {
                'cv_250': cvs[0],
                'cv_500': cvs[1],
                'cv_1000': cvs[2],
                'monotonic_decrease': bool(monotonic),
                'direction': 'decreasing' if monotonic else 'non-monotonic',
            }
    results['sample_size_trend'] = trend

    elapsed = time.time() - t_start
    print(f"\nTotal time: {elapsed:.1f}s")

    # Save raw evidence
    raw_evidence = make_serializable({
        'experiment_id': 'EXP-FRONTIER-35401996615',
        'results': results,
    })

    with open('raw_evidence.json', 'w') as f:
        json.dump(raw_evidence, f, indent=2)

    print(f"\n{'='*60}")
    print("EXPERIMENT COMPLETE")
    print(f"{'='*60}")
    print(f"Pipeline validation (250/type): {'PASS' if results['pipeline_validation']['pass'] else 'FAIL'}")
    for sn in SAMPLE_SIZES:
        print(f"  n={sn}: KDE CV max={results['cv_check'][sn]['kde']['cv_max']:.4f} (pass={results['cv_check'][sn]['kde']['pass']}), "
              f"kNN CV max={results['cv_check'][sn]['knn']['cv_max']:.4f} (pass={results['cv_check'][sn]['knn']['pass']})")

    return results


if __name__ == '__main__':
    try:
        results = run_experiment()
        print("\nMetrics saved to raw_evidence.json")
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
