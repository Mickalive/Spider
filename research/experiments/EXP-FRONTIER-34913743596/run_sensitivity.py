#!/usr/bin/env python3
"""
EXP-FRONTIER-34913743596: EXPLORATORY Sensitivity Analysis
Prereg §9.1: KDE bandwidth sensitivity (leave-one-out CV bandwidth)
Prereg §9.2: kNN k parameter sensitivity (k=3, k=10)

This script is labeled EXPLORATORY per prereg §14.
Cannot support confirmatory claims; results inform interpretation only.
"""
import json, hashlib, numpy as np, warnings, time, sys
from scipy import stats
from scipy.special import digamma
from scipy.spatial import cKDTree
from pathlib import Path

warnings.filterwarnings('ignore')

# === SHARED PARAMETERS (frozen DGP) ===
BASE_SEED = 42
LAMBDA_LEVELS = [0.0, 1.0]  # only null and signal regimes for sensitivity
N_REPLICATIONS = 5
N_PERMUTATIONS = 200
CENTER = np.array([0.5, 0.5])
SIGMA_BASE = 0.05
BETA = 0.5
N_ACTIONS = 4
N_TRANSITIONS_NONSTATIONARY = 2000
N_TRANSITIONS_PER_PAGE_TYPE = 250
N_PAGE_TYPES = 8
PAGE_TYPES = [
    (42, 0.05, np.array([0.5, 0.5])),
    (43, 0.05, np.array([0.5, 0.5])),
    (44, 0.05, np.array([0.5, 0.5])),
    (42, 0.10, np.array([0.5, 0.5])),
    (43, 0.10, np.array([0.5, 0.5])),
    (44, 0.10, np.array([0.5, 0.5])),
    (42, 0.05, np.array([0.3, 0.7])),
    (43, 0.05, np.array([0.3, 0.7])),
]
THETA = [0, np.pi/4, np.pi/2, 3*np.pi/4]
OFFSET_A = [[0.1, 0], [0, 0.1], [-0.1, 0], [0, -0.1]]
SCALE = [[1.2, 1.2], [0.8, 1.2], [1.2, 0.8], [0.8, 0.8]]
OFFSET_B = [[0.05, 0.05], [-0.05, 0.05], [0.05, -0.05], [-0.05, -0.05]]
T_C = [[0.15, 0], [0, 0.15], [-0.15, 0], [0, -0.15]]
ALPHA_C = [0.1, 0.1, 0.1, 0.1]
FUNCTION_MAP = {42: None, 43: None, 44: None}

def rotation_func(s, action_idx, center=CENTER):
    theta = THETA[action_idx]; offset = np.array(OFFSET_A[action_idx])
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    R = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
    return R @ (s - center) + center + offset
def scaling_func(s, action_idx, center=CENTER):
    sx, sy = SCALE[action_idx]; offset = np.array(OFFSET_B[action_idx])
    return np.array([sx*(s[0]-center[0])+center[0], sy*(s[1]-center[1])+center[1]]) + offset
def translation_func(s, action_idx, center=CENTER):
    t = np.array(T_C[action_idx]); alpha = ALPHA_C[action_idx]
    return s + t + alpha * np.sin(2 * np.pi * s)
FUNCTION_MAP[42] = rotation_func
FUNCTION_MAP[43] = scaling_func
FUNCTION_MAP[44] = translation_func

def compute_noise_sigma(s, sigma_base, beta, center=CENTER):
    return sigma_base * (1 + beta * np.linalg.norm(s - center))

def generate_transitions_nonstationary(lambda_val, n_total, rng):
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
            s_next = s_next_det + rng.normal(0, sigma, size=2)
        else:
            s_next = rng.normal(0, sigma_base, size=2) + center
        s_next = np.clip(s_next, 0, 1)
        transitions.append((s, a_idx, s_next, page_type_idx))
    return transitions


# === kNN MI (from main script, with k parameter) ===
def kraskov_mi_once(x, y, k=5):
    n = x.shape[0]
    if n <= k:
        return 0.0
    y_arr = np.asarray(y).reshape(n, 1).astype(float)
    y_scaled = y_arr / 3.0
    joint = np.hstack([x, y_scaled])
    try:
        tree_joint = cKDTree(joint)
        dists, _ = tree_joint.query(joint, k=k+1, p=np.inf)
        eps = dists[:, -1]
        eps = np.nextafter(eps, 0)
        tree_x = cKDTree(x)
        tree_y = cKDTree(y_scaled)
        n_x = np.zeros(n, dtype=int)
        n_y = np.zeros(n, dtype=int)
        for i in range(n):
            n_x[i] = len(tree_x.query_ball_point(x[i], r=eps[i], p=np.inf)) - 1
            n_y[i] = len(tree_y.query_ball_point(y_scaled[i], r=eps[i], p=np.inf)) - 1
        mi = digamma(k) + digamma(n) - np.mean(digamma(n_x+1) + digamma(n_y+1))
        return max(0.0, float(mi))
    except Exception:
        return 0.0

def compute_knn_mi(s_next, actions, n_permutations, rng, k=5):
    if len(s_next) < 10:
        return 0.0, 0.0, 0.0, 0.0
    observed = kraskov_mi_once(s_next, actions, k=k)
    perm_vals = []
    for _ in range(n_permutations):
        perm_actions = rng.permutation(actions)
        v = kraskov_mi_once(s_next, perm_actions, k=k)
        perm_vals.append(v)
    perm_vals = np.array(perm_vals)
    perm_mean = float(np.mean(perm_vals))
    perm_std = float(np.std(perm_vals, ddof=1)) if len(perm_vals) > 1 else 0.0
    perm_threshold = float(np.percentile(perm_vals, 95))
    return observed, perm_mean, perm_std, perm_threshold


# === Custom KDE with bandwidth parameter ===
def pairwise_sq_dist(x):
    """Compute n x n matrix of squared Euclidean distances."""
    d = x - x[:, np.newaxis, :]
    return np.sum(d**2, axis=2)

def kde_loglik_loo(x, h):
    """Leave-one-out log-likelihood for Gaussian KDE with bandwidth h."""
    n = x.shape[0]
    d = x.shape[1]
    D2 = pairwise_sq_dist(x)
    # kernel K(u) = (2*pi*h^2)^{-d/2} exp(-||u||^2 / (2*h^2))
    W = np.exp(-D2 / (2.0 * h**2))  # n x n
    rowsum = np.sum(W, axis=1)  # n
    # LOO: exclude self (W[i,i]=1)
    log_constants = -0.5 * d * np.log(2.0 * np.pi * h**2)
    log_loo = np.log((rowsum - 1.0 + 1e-300) / (n - 1)) + log_constants
    return np.sum(log_loo)

def kde_select_bandwidth_loo(x, h_grid):
    """Select bandwidth by LOO likelihood maximization."""
    best_h = h_grid[0]
    best_ll = -np.inf
    for h in h_grid:
        ll = kde_loglik_loo(x, h)
        if ll > best_ll:
            best_ll = ll
            best_h = h
    return best_h, best_ll

def kde_conditional_density_fixed_h(x_eval, x_train, h):
    """KDE density of x_eval using Gaussian kernel with bandwidth h, trained on x_train."""
    n = x_train.shape[0]
    d = x_train.shape[1]
    D2 = np.sum((x_eval[:, np.newaxis, :] - x_train[np.newaxis, :, :])**2, axis=2)  # (n_eval, n_train)
    W = np.exp(-D2 / (2.0 * h**2))
    return np.mean(W, axis=1) * (2.0 * np.pi * h**2)**(-d/2.0)

def kde_max_kl_fixed_h(s_next, actions, h, rng, n_permutations=200):
    """KDE max KL divergence with fixed bandwidth h and permutation null."""
    n = len(s_next)
    if n < 10:
        return 0.0, 0.0, 0.0, 0.0
    # marginal density at all points
    marg = kde_conditional_density_fixed_h(s_next, s_next, h)
    marg = np.maximum(marg, 1e-300)

    def obs_kl(act_labels):
        max_kl = -1e9
        for a in range(N_ACTIONS):
            mask = act_labels == a
            n_a = np.sum(mask)
            if n_a < 5:
                continue
            pts = s_next[mask]
            cond = kde_conditional_density_fixed_h(pts, pts, h)
            marg_at_pts = marg[mask]
            cond = np.maximum(cond, 1e-300)
            kl = np.mean(np.log(cond / marg_at_pts))
            if kl > max_kl:
                max_kl = kl
        return max(0.0, float(max_kl)) if max_kl > -1e8 else 0.0

    observed = obs_kl(actions)
    perm_vals = []
    for _ in range(n_permutations):
        perm_actions = rng.permutation(actions)
        perm_vals.append(obs_kl(perm_actions))
    perm_vals = np.array(perm_vals)
    perm_mean = float(np.mean(perm_vals))
    perm_std = float(np.std(perm_vals, ddof=1)) if len(perm_vals) > 1 else 0.0
    perm_threshold = float(np.percentile(perm_vals, 95))
    return observed, perm_mean, perm_std, perm_threshold


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


def run_sensitivity():
    start_time = time.time()
    results = {}

    # KDE bandwidth grid for LOO-CV (Scott for n=250, 2D: ~0.115; grid covers 0.03-0.50)
    h_grid = np.linspace(0.03, 0.50, 30)

    for config_name, config in [
        ("knn_k3", {"type": "knn", "k": 3}),
        ("knn_k10", {"type": "knn", "k": 10}),
        ("kde_loocv", {"type": "kde_cv"}),
    ]:
        print(f"\n=== Sensitivity: {config_name} ===")
        per_type_data = {pt: {"lambda0": [], "lambda1": []} for pt in range(N_PAGE_TYPES)}
        per_type_raw = {pt: {"lambda0": [], "lambda1": []} for pt in range(N_PAGE_TYPES)}
        per_type_thresh = {pt: {"lambda0": [], "lambda1": []} for pt in range(N_PAGE_TYPES)}
        pooled_bc = {"lambda0": [], "lambda1": []}

        for l_idx, l in enumerate(LAMBDA_LEVELS):
            lkey = "lambda0" if l == 0.0 else "lambda1"
            for rep_idx in range(N_REPLICATIONS):
                cell_seed = BASE_SEED * 100000 + l_idx * 1000 + rep_idx * 10 + 999
                rng = np.random.RandomState(cell_seed)
                transitions = generate_transitions_nonstationary(l, N_TRANSITIONS_NONSTATIONARY, rng)

                # subsample per-type (same deterministic subsampling)
                subsampled = []
                for pt_idx in range(N_PAGE_TYPES):
                    pt_trans = [t for t in transitions if t[3] == pt_idx]
                    sub_rng = np.random.RandomState(cell_seed + pt_idx * 100 + 888)
                    idx = sub_rng.choice(len(pt_trans), size=N_TRANSITIONS_PER_PAGE_TYPE, replace=False)
                    subsampled.extend([pt_trans[i] for i in sorted(idx)])

                s_sub = np.array([t[2] for t in subsampled])
                a_sub = np.array([t[1] for t in subsampled])

                if config["type"] == "knn":
                    k = config["k"]
                    rng_knn = np.random.RandomState(cell_seed + 7000)
                    obs, pm, _, thresh = compute_knn_mi(s_sub, a_sub, N_PERMUTATIONS, rng_knn, k=k)
                    bc = max(0.0, obs - pm)
                    pooled_bc[lkey].append(bc)
                    for pt_idx in range(N_PAGE_TYPES):
                        pt_trans = [t for t in transitions if t[3] == pt_idx]
                        s_pt = np.array([t[2] for t in pt_trans])
                        a_pt = np.array([t[1] for t in pt_trans])
                        rng_k = np.random.RandomState(cell_seed + pt_idx * 100 + 877)
                        obs2, pm2, _, thresh2 = compute_knn_mi(s_pt, a_pt, N_PERMUTATIONS, rng_k, k=k)
                        bc2 = max(0.0, obs2 - pm2)
                        per_type_data[pt_idx][lkey].append(bc2)
                        per_type_raw[pt_idx][lkey].append(obs2)
                        per_type_thresh[pt_idx][lkey].append(thresh2)

                elif config["type"] == "kde_cv":
                    # select bandwidth by LOO-CV on pooled data
                    h_sel, ll_sel = kde_select_bandwidth_loo(s_sub, h_grid)
                    rng_kde = np.random.RandomState(cell_seed + 6000)
                    obs, pm, _, thresh = kde_max_kl_fixed_h(s_sub, a_sub, h_sel, rng_kde, N_PERMUTATIONS)
                    bc = max(0.0, obs - pm)
                    pooled_bc[lkey].append(bc)
                    for pt_idx in range(N_PAGE_TYPES):
                        pt_trans = [t for t in transitions if t[3] == pt_idx]
                        s_pt = np.array([t[2] for t in pt_trans])
                        a_pt = np.array([t[1] for t in pt_trans])
                        # select bandwidth per-type for LOO-CV (realistic operational use)
                        h_pt, _ = kde_select_bandwidth_loo(s_pt, h_grid)
                        rng_k = np.random.RandomState(cell_seed + pt_idx * 100 + 777)
                        obs2, pm2, _, thresh2 = kde_max_kl_fixed_h(s_pt, a_pt, h_pt, rng_k, N_PERMUTATIONS)
                        bc2 = max(0.0, obs2 - pm2)
                        per_type_data[pt_idx][lkey].append(bc2)
                        per_type_raw[pt_idx][lkey].append(obs2)
                        per_type_thresh[pt_idx][lkey].append(thresh2)

            print(f"  Lambda {l:.1f} pooled BC {np.mean(pooled_bc[lkey]):.4f}  elapsed {time.time()-start_time:.1f}s")

        # Analyze
        # Null control at lambda=0: per-type observed_raw <= perm_threshold
        null_results = []
        for pt in range(N_PAGE_TYPES):
            obs_mean = np.mean(per_type_raw[pt]["lambda0"])
            thresh_mean = np.mean(per_type_thresh[pt]["lambda0"])
            null_results.append({
                "observed_raw": float(obs_mean),
                "threshold_95th": float(thresh_mean),
                "pass": bool(obs_mean <= thresh_mean),
            })
        null_pass = all(r["pass"] for r in null_results)

        # CV at lambda=1: BC across reps per type
        cv_results = []
        for pt in range(N_PAGE_TYPES):
            vals = per_type_data[pt]["lambda1"]
            m = np.mean(vals)
            s = np.std(vals, ddof=1)
            cv = float(s / m) if m > 0 else float('inf')
            cv_results.append({"mean_bc": float(m), "cv": cv, "pass": bool(cv <= 0.5)})
        cv_pass = all(r["pass"] for r in cv_results)
        max_cv = max(r["cv"] for r in cv_results)

        results[config_name] = {
            "description": f"EXPLORATORY sensitivity: {config_name}",
            "null_control": {
                "pass": bool(null_pass),
                "n_types_passing": sum(1 for r in null_results if r["pass"]),
                "per_type": null_results,
            },
            "cv_check": {
                "pass": bool(cv_pass),
                "max_cv": float(max_cv),
                "per_type": cv_results,
            },
            "pooled_bc_lambda0": float(np.mean(pooled_bc["lambda0"])),
            "pooled_bc_lambda1": float(np.mean(pooled_bc["lambda1"])),
        }
        print(f"  Null control: {null_pass} ({sum(1 for r in null_results if r['pass'])}/8)")
        print(f"  CV check: {cv_pass} (max {max_cv:.4f})")
        print(f"  Pooled BC lambda0={np.mean(pooled_bc['lambda0']):.4f} lambda1={np.mean(pooled_bc['lambda1']):.4f}")

    execution_time = time.time() - start_time
    print(f"\n=== Sensitivity analysis complete: {execution_time:.1f}s ===")
    print(f"knn_k3 null={results['knn_k3']['null_control']['pass']} cv={results['knn_k3']['cv_check']['pass']} max_cv={results['knn_k3']['cv_check']['max_cv']:.4f}")
    print(f"knn_k10 null={results['knn_k10']['null_control']['pass']} cv={results['knn_k10']['cv_check']['pass']} max_cv={results['knn_k10']['cv_check']['max_cv']:.4f}")
    print(f"kde_loocv null={results['kde_loocv']['null_control']['pass']} cv={results['kde_loocv']['cv_check']['pass']} max_cv={results['kde_loocv']['cv_check']['max_cv']:.4f}")

    output = {
        "experiment_id": "EXP-FRONTIER-34913743596",
        "analysis_type": "EXPLORATORY sensitivity (prereg §9.1-9.2)",
        "labeled_as": "EXPLORATORY per prereg §14 - cannot support confirmatory claims",
        "frozen_knn_k": 5,
        "frozen_kde_bw": "scott",
        "sensitivities": results,
        "execution_time_seconds": float(execution_time),
    }
    out_path = Path(__file__).parent / "sensitivity_exploratory.json"
    with open(out_path, "w") as f:
        json.dump(to_native(output), f, indent=2)
    print(f"Wrote {out_path}")
    return output

if __name__ == "__main__":
    run_sensitivity()
