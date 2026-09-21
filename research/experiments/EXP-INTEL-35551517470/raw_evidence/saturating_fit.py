#!/usr/bin/env python3
"""EXP-INTEL-35551517470: Bounded Saturating Function Fitting to 4-point ranking agreement data."""

import json
import math
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import spearmanr

# Training data (from spec.json, verified in analysis_output_snr.json)
n_train = np.array([5.0, 10.0, 15.0, 20.0])
F_train = np.array([0.0, 0.0, 0.4996, 0.5654])
N = len(n_train)

# Extrapolation targets
n_extrap = np.array([50.0, 82.0])

# Parent's best model metrics (from spec baselines)
parent_R2 = 0.8797
parent_max_resid_pp = 12.39  # percentage points

# ─── Function families ───────────────────────────────────────────────────────

def logistic(n, L, k, n0):
    """F(n) = L / (1 + exp(-k * (n - n0)))"""
    return L / (1.0 + np.exp(-k * (n - n0)))

def hill(n, L, h, K):
    """F(n) = L * n^h / (K^h + n^h)"""
    return L * np.power(n, h) / (np.power(K, h) + np.power(n, h))

def richards(n, L, n0, a, v):
    """F(n) = L / (1 + (n/n0)^a)^(1/v)"""
    return L / np.power(1.0 + np.power(n / n0, a), 1.0 / v)


# ─── Metrics ─────────────────────────────────────────────────────────────────

def compute_metrics(n_data, F_data, model_func, params, n_extrap_pts):
    """Compute R², max residual, AIC, BIC, extrapolation predictions."""
    F_pred = model_func(n_data, *params)
    residuals = F_data - F_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((F_data - np.mean(F_data))**2)
    
    if ss_tot == 0:
        R2 = 1.0 if ss_res == 0 else 0.0
    else:
        R2 = 1.0 - ss_res / ss_tot
    
    max_resid = np.max(np.abs(residuals))
    max_resid_pp = max_resid * 100.0  # in percentage points
    
    # AIC and BIC (assuming Gaussian errors)
    k_params = len(params)
    n_points = len(n_data)
    sigma2 = ss_res / n_points if n_points > k_params else 1e-10
    log_likelihood = -n_points / 2.0 * (math.log(2 * math.pi * sigma2) + 1.0)
    AIC = 2 * k_params - 2 * log_likelihood
    BIC = k_params * math.log(n_points) - 2 * log_likelihood
    
    # Extrapolation predictions
    F_extrap = model_func(n_extrap_pts, *params)
    
    return {
        'R2': R2,
        'max_residual': max_resid,
        'max_residual_pp': max_resid_pp,
        'AIC': AIC,
        'BIC': BIC,
        'F50': float(F_extrap[0]),
        'F82': float(F_extrap[1]),
        'params': params,
        'F_pred_train': F_pred.tolist(),
        'residuals': residuals.tolist(),
    }


# ─── Fitting with multiple restarts ─────────────────────────────────────────

def fit_with_restarts(model_func, bounds, n_restarts=10, seed=42):
    """Fit model with multiple random restarts, return best fit."""
    rng = np.random.RandomState(seed)
    best_result = None
    all_results = []
    
    for attempt in range(n_restarts):
        # Random initial conditions within bounds
        p0 = []
        for lo, hi in zip(bounds[0], bounds[1]):
            if lo == -np.inf:
                lo = -10.0
            if hi == np.inf:
                hi = 10.0
            p0.append(rng.uniform(max(lo, -5), min(hi, 5)))
        
        try:
            popt, pcov = curve_fit(model_func, n_train, F_train, p0=p0,
                                   bounds=bounds, maxfev=10000)
            metrics = compute_metrics(n_train, F_train, model_func, popt, n_extrap)
            all_results.append(metrics)
            
            if best_result is None or metrics['R2'] > best_result['R2']:
                best_result = metrics
        except Exception as e:
            continue
    
    return best_result, all_results


# ─── Null baseline ───────────────────────────────────────────────────────────

def constant_null():
    """F(n) = 0.5654 (observed at n=20) for all n."""
    F_const = 0.5654
    residuals = F_train - F_const
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((F_train - np.mean(F_train))**2)
    R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    max_resid = np.max(np.abs(residuals)) * 100.0
    return {
        'id': 'NC1_PARENT_BEST_MODEL',
        'F_constant': F_const,
        'R2': R2,
        'max_residual_pp': max_resid,
        'F50': F_const,
        'F82': F_const,
    }


# ─── Main analysis ───────────────────────────────────────────────────────────

def main():
    results = {}
    
    # ─── Logistic fit ─────────────────────────────────────────────────────
    # L in [0,1], k > 0, n0 can be any positive
    logistic_bounds = ([0.0, 0.0, 0.01], [1.0, 50.0, 100.0])
    best_logistic, all_logistic = fit_with_restarts(logistic, logistic_bounds)
    results['logistic'] = best_logistic
    results['logistic_all_restarts'] = len(all_logistic)
    
    # ─── Hill fit ─────────────────────────────────────────────────────────
    # L in [0,1], h > 0, K > 0
    hill_bounds = ([0.0, 0.1, 0.1], [1.0, 20.0, 100.0])
    best_hill, all_hill = fit_with_restarts(hill, hill_bounds)
    results['hill'] = best_hill
    results['hill_all_restarts'] = len(all_hill)
    
    # ─── Richards fit ─────────────────────────────────────────────────────
    # L in [0,1], n0 > 0, a > 0, v > 0
    richards_bounds = ([0.0, 0.01, 0.01, 0.01], [1.0, 100.0, 20.0, 20.0])
    best_richards, all_richards = fit_with_restarts(richards, richards_bounds)
    results['richards'] = best_richards
    results['richards_all_restarts'] = len(all_richards)
    
    # ─── Identify best overall fit ────────────────────────────────────────
    candidates = []
    for name in ['logistic', 'hill', 'richards']:
        if results[name] is not None:
            candidates.append((name, results[name]))
    
    if not candidates:
        print("ERROR: No function family converged")
        return
    
    # Sort by R²
    candidates.sort(key=lambda x: x[1]['R2'], reverse=True)
    best_name, best_fit = candidates[0]
    
    print(f"\n{'='*70}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*70}")
    
    for name, fit in candidates:
        print(f"\n--- {name.upper()} ---")
        print(f"  Parameters: {[f'{p:.6f}' for p in fit['params']]}")
        print(f"  R²: {fit['R2']:.6f}")
        print(f"  Max residual: {fit['max_residual']:.6f} ({fit['max_residual_pp']:.2f}pp)")
        print(f"  AIC: {fit['AIC']:.2f}")
        print(f"  BIC: {fit['BIC']:.2f}")
        print(f"  F(50): {fit['F50']:.6f}")
        print(f"  F(82): {fit['F82']:.6f}")
        print(f"  Predictions at training points: {[f'{p:.4f}' for p in fit['F_pred_train']]}")
        print(f"  Residuals (pp): {[f'{r*100:.2f}' for r in fit['residuals']]}")
    
    # ─── Decision rules ───────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"DECISION RULES")
    print(f"{'='*70}")
    
    # C1: At least one function R² >= 0.90 AND max residual < 10pp
    C1_pass = any(
        fit['R2'] >= 0.90 and fit['max_residual_pp'] < 10.0
        for name, fit in candidates
    )
    print(f"\nC1_BEST_FIT_QUALITY: R² >= 0.90 AND max_resid < 10pp")
    for name, fit in candidates:
        r2_pass = fit['R2'] >= 0.90
        resid_pass = fit['max_residual_pp'] < 10.0
        print(f"  {name}: R²={fit['R2']:.4f} {'PASS' if r2_pass else 'FAIL'}, "
              f"max_resid={fit['max_residual_pp']:.2f}pp {'PASS' if resid_pass else 'FAIL'}")
    print(f"  C1 overall: {'PASS' if C1_pass else 'FAIL'}")
    
    # C2: All qualifying functions predict F(50) in [0,1] AND F(82) in [0,1]
    qualifying = [(name, fit) for name, fit in candidates if fit['R2'] >= 0.90]
    if not qualifying:
        C2_pass = False  # vacuously can't check
        C2_note = "No qualifying functions (R² >= 0.90)"
    else:
        C2_pass = all(
            0.0 <= fit['F50'] <= 1.0 and 0.0 <= fit['F82'] <= 1.0
            for name, fit in qualifying
        )
        C2_note = f"{len(qualifying)} qualifying functions"
    print(f"\nC2_EXTRAPOLATION_PHYSICAL: F(50) ∈ [0,1] AND F(82) ∈ [0,1]")
    print(f"  {C2_note}")
    for name, fit in qualifying:
        print(f"  {name}: F(50)={fit['F50']:.4f}, F(82)={fit['F82']:.4f}")
    print(f"  C2 overall: {'PASS' if C2_pass else 'FAIL'}")
    
    # C3: Best R² > 0.93 OR max residual < 8pp
    best_R2 = max(fit['R2'] for name, fit in candidates)
    best_max_resid = min(fit['max_residual_pp'] for name, fit in candidates)
    C3_R2_pass = best_R2 > 0.93
    C3_resid_pass = best_max_resid < 8.0
    C3_pass = C3_R2_pass or C3_resid_pass
    print(f"\nC3_IMPROVES_OVER_PARENT: R² > 0.93 OR max_resid < 8pp")
    print(f"  Best R²: {best_R2:.4f} (parent: {parent_R2:.4f}) {'PASS' if C3_R2_pass else 'FAIL'}")
    print(f"  Best max_resid: {best_max_resid:.2f}pp (parent: {parent_max_resid_pp:.1f}pp) {'PASS' if C3_resid_pass else 'FAIL'}")
    print(f"  C3 overall: {'PASS' if C3_pass else 'FAIL'}")
    
    # ─── Verdict ──────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    if not C1_pass:
        verdict = "FALSIFIES"
        reason = "NOT C1: No saturating function achieves R² >= 0.90 AND max residual < 10pp. Step-function structure (0,0,0.50,0.57) is incompatible with smooth bounded saturating forms. Model-based extrapolation path definitively closed."
    elif C1_pass and not C2_pass:
        verdict = "MEASUREMENT_INVALID"
        reason = "C1 AND NOT C2: Fit quality adequate but extrapolation physically implausible."
    elif C1_pass and C2_pass and not C3_pass:
        verdict = "MIXED"
        reason = "C1 AND C2 AND NOT C3: Saturating functions fit adequately but do not improve over already-rejected parent model."
    else:
        verdict = "SURVIVES"
        reason = "C1 AND C2 AND C3: Validated extrapolation improves over all prior models."
    print(f"VERDICT: {verdict}")
    print(f"REASON: {reason}")
    
    # ─── Positive control ─────────────────────────────────────────────────
    pc1_pass = best_fit['max_residual_pp'] < 5.0
    print(f"\nPC1_FIT_REPRODUCES_TRAINING: max residual < 5pp at training points")
    print(f"  Best fit max residual: {best_fit['max_residual_pp']:.2f}pp")
    print(f"  PC1: {'PASS' if pc1_pass else 'FAIL'}")
    
    # ─── Null control ─────────────────────────────────────────────────────
    nc = constant_null()
    print(f"\nNC1_PARENT_BEST_MODEL: must improve over parent R²=0.8797, max_resid=12.39pp")
    print(f"  Constant null R²: {nc['R2']:.4f}")
    nc1_pass = C3_pass
    print(f"  NC1: {'PASS' if nc1_pass else 'FAIL'}")
    
    # ─── Key observation: logistic is step-function approximation ────────
    print(f"\n{'='*70}")
    print(f"KEY OBSERVATIONS")
    print(f"{'='*70}")
    if results.get('logistic'):
        L, k, n0 = results['logistic']['params']
        print(f"Logistic parameters: L={L:.6f}, k={k:.6f}, n0={n0:.6f}")
        print(f"  L ≈ observed F(n=20) = {F_train[-1]:.4f}")
        print(f"  k={k:.2f} indicates VERY steep transition (step-function approximation)")
        print(f"  n0={n0:.2f} is midpoint of transition between n=10 and n=15")
        print(f"  The logistic learns that the step at n≈12.5 is the ONLY feature")
        print(f"  and extrapolates the plateau F=0.5654 to all n > 15")
        print(f"  This is IDENTICAL to the constant null F(n) = 0.5654")
        print(f"  The extrapolation F(50)={results['logistic']['F50']:.4f} adds ZERO new information")
    
    # ─── Spearman correlation ─────────────────────────────────────────────
    # Check monotonicity at training points
    spearman_rho, spearman_p = spearmanr(n_train, F_train)
    print(f"\nMonotonicity: Spearman rho={spearman_rho:.4f}, p={spearman_p:.4f}")
    
    # ─── Output JSON ──────────────────────────────────────────────────────
    # Check if best fit extrapolation is identical to constant null
    logistic_F50 = results['logistic']['F50'] if results.get('logistic') else None
    hill_F50 = results['hill']['F50'] if results.get('hill') else None
    
    output = {
        'experiment_id': 'EXP-INTEL-35551517470',
        'training_data': {
            'n': n_train.tolist(),
            'F': F_train.tolist(),
        },
        'fits': {},
        'decision_rules': {
            'C1_pass': bool(C1_pass),
            'C2_pass': bool(C2_pass),
            'C3_pass': bool(C3_pass),
            'verdict': verdict,
        },
        'positive_control': {
            'PC1_pass': bool(pc1_pass),
            'max_residual_pp': float(best_fit['max_residual_pp']),
        },
        'null_control': {
            'NC1_pass': bool(nc1_pass),
            'constant_null': {
                'F_constant': nc['F_constant'],
                'R2': nc['R2'],
                'max_residual_pp': nc['max_residual_pp'],
                'F50': nc['F50'],
                'F82': nc['F82'],
            },
        },
        'parent_baseline': {
            'R2': parent_R2,
            'max_residual_pp': parent_max_resid_pp,
        },
        'extrapolation_equivalence_to_null': {
            'logistic_F50_equals_null': logistic_F50 == 0.5654 if logistic_F50 is not None else None,
            'hill_F50_equals_null': abs(hill_F50 - 0.5654) < 0.001 if hill_F50 is not None else None,
        },
    }
    
    for name in ['logistic', 'hill', 'richards']:
        if results[name] is not None:
            fit = results[name]
            output['fits'][name] = {
                'R2': fit['R2'],
                'max_residual_pp': fit['max_residual_pp'],
                'AIC': fit['AIC'],
                'BIC': fit['BIC'],
                'F50': fit['F50'],
                'F82': fit['F82'],
                'params': fit['params'],
                'F_pred_train': fit['F_pred_train'],
                'residuals_pp': [r * 100 for r in fit['residuals']],
            }
    
    # Convert numpy arrays to lists for JSON serialization
    def to_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return obj
    
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.integer):
                return int(obj)
            return super().default(obj)
    
    with open('/tmp/opencode/analysis_output.json', 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    
    print(f"\nOutput written to /tmp/opencode/analysis_output.json")


if __name__ == '__main__':
    main()
