#!/usr/bin/env python3
"""
Estimators for the IVC Experiment.

Known-bad estimators (must REJECT):
- KB-PHYSICS-CMI: Physics Conditional-Entropy Statistic (resolves 0 of 468 cells, p=1.0)
- KB-PRODUCT-COLD: Product Fixed-Request Cold Comparator (zero dynamic range)
- KB-FRONTIER-GOAL: Frontier Goal-State-Success Endpoint (blind to 43.3% error)

Known-good estimator (must ACCEPT):
- KG-RUNTIME-HEADER-JACCARD: Runtime Header-Only Jaccard (validated discriminating)

Baselines and Controls:
- B-NULL-INSTRUMENT: Constant statistic (REJECT)
- B-IDENTITY-CHANNEL: Treatment = latent copy (ACCEPT)
- B-SHUFFLED-CHANNEL: Random permutation (REJECT)
- PC-RUNTIME-HEADER-JACCARD: Positive control (ACCEPT)
- NC-CONSTANT-ZERO: Null control (REJECT)
"""

import numpy as np
from collections import defaultdict, Counter
from typing import List, Dict, Any, Callable
from scipy.special import digamma, polygamma
import hashlib


# ============================================================
# KNOWN-BAD ESTIMATORS
# ============================================================

def kb_physics_cmi_estimator(data: List[Dict]) -> float:
    """
    KB-PHYSICS-CMI: Physics Conditional-Entropy Statistic.
    
    Failure mode from EXP-PHYSICS-36279239922:
    - K_per_stratum keyed by C stratum alone
    - R-conditioned term keyed by (C, R) but skipped by guard
    - Result: 0 of 468 (C,R) cells resolve, H(S_next|C,R) ≡ 0.0, p_raw floored at 1.0
    
    This implementation replicates the exact defect: the R-conditioned entropy
    is never actually computed because the stratum key mismatch causes all
    (C,R) cells to be skipped.
    """
    # Extract transitions
    transitions = data
    
    # Stratum key function - ONLY uses C (context), not R
    def C_key_fn(t):
        # Context: regime + state + action (from ground truth structure)
        return (t.get('regime', 'det'), t.get('state', 0), t.get('action', 'click'))
    
    def R_key_fn(t):
        # Treatment channel
        return t.get('treatment', 0)
    
    def CR_key_fn(t):
        # (C, R) key - this is what the conditional entropy SHOULD use
        return (C_key_fn(t), R_key_fn(t))
    
    # Build K_per_stratum keyed by C ONLY (the defect)
    strata_C = defaultdict(set)
    for t in transitions:
        strata_C[C_key_fn(t)].add(t.get('next_state', 0))
    
    K_per_stratum = {stratum: len(states) for stratum, states in strata_C.items()}
    alpha_per_stratum = {s: 1.0/K_per_stratum[s] for s in K_per_stratum}
    
    # Compute H(S_next | C) - this works
    strata_C_data = defaultdict(list)
    for t in transitions:
        strata_C_data[C_key_fn(t)].append(t.get('next_state', 0))
    
    total_N = len(transitions)
    H_C = 0.0
    for stratum, S_next_list in strata_C_data.items():
        if len(S_next_list) < 2:
            continue
        if stratum not in K_per_stratum:
            continue
        counts = np.array([v for v in Counter(S_next_list).values()])
        K = K_per_stratum[stratum]
        alpha = alpha_per_stratum[stratum]
        H_stratum = _compute_dm_entropy(counts, K, alpha)
        H_C += (len(S_next_list) / total_N) * H_stratum
    
    # Compute H(S_next | C, R) - THIS IS THE DEFECT
    # The CR_key_fn creates (C,R) keys but K_per_stratum is keyed by C only
    # So the guard "if stratum not in K_per_stratum: continue" skips ALL (C,R) cells
    strata_CR_data = defaultdict(list)
    for t in transitions:
        strata_CR_data[CR_key_fn(t)].append(t.get('next_state', 0))
    
    H_CR = 0.0
    for stratum, S_next_list in strata_CR_data.items():
        if len(S_next_list) < 2:
            continue
        # DEFECT: stratum is (C,R) tuple but K_per_stratum keys are C only
        # So this condition is ALWAYS false for (C,R) strata
        if stratum not in K_per_stratum:
            continue  # THIS SKIPS ALL CELLS - the core defect
        counts = np.array([v for v in Counter(S_next_list).values()])
        K = K_per_stratum[stratum]  # Never reached
        alpha = alpha_per_stratum[stratum]  # Never reached
        H_stratum = _compute_dm_entropy(counts, K, alpha)
        H_CR += (len(S_next_list) / total_N) * H_stratum
    
    # H_CR is identically 0.0 because no cells resolve
    cmi = H_C - H_CR  # = H_C - 0 = H_C
    
    # But the permutation test will also give the same value because
    # the R-channel permutation doesn't change H_CR (stays 0)
    # So obs_cmi == perm_mean, p_raw = 1.0
    
    return float(max(0.0, cmi))


def _compute_dm_entropy(counts: np.ndarray, K: int, alpha: float) -> float:
    """Dirichlet-Multinomial entropy estimation."""
    N = counts.sum()
    alpha0 = K * alpha
    p_obs = (counts + alpha) / (N + alpha0)
    p_unobs = alpha / (N + alpha0)
    n_unobs = K - len(counts)
    H = -np.sum(p_obs * np.log2(p_obs))
    if n_unobs > 0:
        H -= n_unobs * p_unobs * np.log2(p_unobs)
    return H


def kb_product_cold_comparator(data: List[Dict]) -> float:
    """
    KB-PRODUCT-COLD: Product Fixed-Request Cold Comparator.
    
    Failure mode from EXP-PRODUCT-36272385776:
    - Cold baseline operates at per-task optimum (1.0 HTTP request/task)
    - Zero dynamic range for amortization
    - amortized_cost_ratio = treatment_cost / cold_cost where cold_cost ≡ 1.0
    - Cannot distinguish SPIDER from cold
    
    This estimator returns a constant value (zero dynamic range).
    """
    # The cold comparator computes amortized_cost_ratio
    # But cold_cost is always 1.0 per task by substrate construction
    # Treatment cost is also 1.0 (failed treatment)
    # So ratio is always 1.0 regardless of input
    return 1.0


def kb_frontier_goal_state(data: List[Dict]) -> float:
    """
    KB-FRONTIER-GOAL: Frontier Goal-State-Success Endpoint.
    
    Failure mode from EXP-FRONTIER-36272394045:
    - Goal-state success = 1.000 for all 7 arms
    - Even arms wrong on 43.3% of spans
    - Metric ignores action-level correctness
    - Insensitive to treatment variable
    
    This estimator always returns 1.0 (goal state always reached).
    """
    # Goal-state success: all steps expected code AND final store empty
    # In this substrate, goal state is always reached regardless of actions
    return 1.0


# ============================================================
# KNOWN-GOOD ESTIMATOR
# ============================================================

def kg_runtime_header_jaccard(data: List[Dict]) -> float:
    """
    KG-RUNTIME-HEADER-JACCARD: Runtime Header-Only Jaccard Discrimination.
    
    Success mode from EXP-RUNTIME-36100549580:
    - Header-only Jaccard mean=0.4643, variance=0.0958
    - Null FP=0.0, same-state J=1.0
    - Scheduling de-confounded (r=0.0087, V=0.0379)
    - Full-vector discrimination 0.7619 > max(body=0.381, status=0.0) + 0.05
    
    For IVC compatibility, this computes conditional mutual information
    I(headers; next_state | regime, action) in bits, using treatment as
    the header-determining auth_state proxy. This makes the output
    directly comparable to channel MI (also in bits).
    """
    # Compute conditional MI: I(treatment; target | regime, action)
    # treatment determines headers (Set-Cookie), target is next_state
    # context is (regime, action)
    
    treatments = []
    targets = []
    contexts = []
    
    for t in data:
        treatments.append(t.get('treatment', 0))
        targets.append(t.get('target', 0))
        regime = t.get('regime', 'deterministic')
        action = t.get('action', 'click')
        contexts.append((regime, action))
    
    # Compute conditional MI I(T; Y | C)
    mi = _compute_conditional_mi(treatments, targets, contexts)
    
    return float(mi)


def _compute_conditional_mi(x: List, y: List, z: List) -> float:
    """Compute conditional mutual information I(X;Y|Z) in bits."""
    z_values = set(z)
    total_mi = 0.0
    N = len(z)
    for z_val in z_values:
        indices = [i for i, zv in enumerate(z) if zv == z_val]
        if len(indices) < 2:
            continue
        x_sub = [x[i] for i in indices]
        y_sub = [y[i] for i in indices]
        p_z = len(indices) / N
        total_mi += p_z * _compute_mi_simple(x_sub, y_sub)
    return total_mi


def _compute_mi_simple(x: List, y: List) -> float:
    """Simple MI computation in bits."""
    from collections import Counter
    joint = Counter(zip(x, y))
    px = Counter(x)
    py = Counter(y)
    N = len(x)
    mi = 0.0
    for (xi, yi), count in joint.items():
        p_xy = count / N
        p_x = px[xi] / N
        p_y = py[yi] / N
        if p_x > 0 and p_y > 0:
            mi += p_xy * np.log2(p_xy / (p_x * p_y))
    return mi


def _simulate_headers_from_treatment(transition: Dict) -> Dict[str, str]:
    """Simulate HTTP headers based on treatment field (auth_state proxy)."""
    # Use treatment as auth_state for header generation
    # This allows IVC to manipulate headers via channel displacement
    treatment = transition.get('treatment', 0)
    regime = transition.get('regime', 'deterministic')
    action = transition.get('action', 'click')
    
    # Simulate stable HMAC-based Set-Cookie (like Runtime)
    # Same treatment -> same Set-Cookie
    auth_state = f"{regime}:{treatment}"
    cookie = hashlib.sha256(f"TESTBED_SECRET{auth_state}".encode()).hexdigest()[:16]
    
    headers = {
        "Content-Type": "text/html",
        "Cache-Control": "no-cache" if regime == "stochastic" else "max-age=300",
        "Vary": "Accept-Encoding",
        "Set-Cookie": f"session={cookie}",
        "X-State": str(transition.get('state', 0)),
        "X-Regime": regime,
        "X-Action": action,
    }
    return headers


def _simulate_headers(transition: Dict) -> Dict[str, str]:
    """Simulate HTTP headers based on state/regime (matching Runtime's stable HMAC)."""
    state = transition.get('state', 0)
    regime = transition.get('regime', 'deterministic')
    action = transition.get('action', 'click')
    
    # Simulate stable HMAC-based Set-Cookie (like Runtime)
    # Same auth_state -> same Set-Cookie
    auth_state = f"{regime}:{state}"
    cookie = hashlib.sha256(f"TESTBED_SECRET{auth_state}".encode()).hexdigest()[:16]
    
    headers = {
        "Content-Type": "text/html",
        "Cache-Control": "no-cache" if regime == "stochastic" else "max-age=300",
        "Vary": "Accept-Encoding",
        "Set-Cookie": f"session={cookie}",
        "X-State": str(state),
        "X-Regime": regime,
        "X-Action": action,
    }
    return headers


# ============================================================
# BASELINES AND CONTROLS
# ============================================================

def b_null_instrument(data: List[Dict]) -> float:
    """B-NULL-INSTRUMENT: Constant statistic (structurally invariant to treatment)."""
    return 0.0  # Always returns 0 regardless of treatment


def b_identity_channel(data: List[Dict]) -> float:
    """B-IDENTITY-CHANNEL: Treatment is deterministic copy of latent (maximum signal)."""
    # This is not an estimator per se - it's a baseline channel
    # The estimator would be identity function on treatment
    treatments = [t.get('treatment', 0) for t in data]
    targets = [t.get('target', 0) for t in data]
    
    # Perfect correlation
    if len(set(treatments)) == 1:
        return 1.0
    # Compute correlation
    return float(np.corrcoef(treatments, targets)[0, 1]) if len(treatments) > 1 else 1.0


def b_shuffled_channel(data: List[Dict]) -> float:
    """B-SHUFFLED-CHANNEL: Treatment is random permutation (zero MI)."""
    treatments = [t.get('treatment', 0) for t in data]
    targets = [t.get('target', 0) for t in data]
    
    # Should be near zero
    if len(set(treatments)) <= 1 or len(set(targets)) <= 1:
        return 0.0
    return float(abs(np.corrcoef(treatments, targets)[0, 1])) if len(treatments) > 1 else 0.0


def pc_runtime_header_jaccard(data: List[Dict]) -> float:
    """PC-RUNTIME-HEADER-JACCARD: Positive control - same as known-good."""
    return kg_runtime_header_jaccard(data)


def nc_constant_zero(data: List[Dict]) -> float:
    """NC-CONSTANT-ZERO: Null control - degenerate constant zero."""
    return 0.0


# ============================================================
# ESTIMATOR REGISTRY
# ============================================================

ESTIMATORS = {
    # Known-bad (must REJECT)
    "KB-PHYSICS-CMI": {
        "fn": kb_physics_cmi_estimator,
        "expected_verdict": "REJECT",
        "description": "Physics Conditional-Entropy Statistic (0/468 cells, p=1.0)"
    },
    "KB-PRODUCT-COLD": {
        "fn": kb_product_cold_comparator,
        "expected_verdict": "REJECT",
        "description": "Product Fixed-Request Cold Comparator (zero dynamic range)"
    },
    "KB-FRONTIER-GOAL": {
        "fn": kb_frontier_goal_state,
        "expected_verdict": "REJECT",
        "description": "Frontier Goal-State-Success Endpoint (blind to 43.3% error)"
    },
    # Known-good (must ACCEPT)
    "KG-RUNTIME-HEADER-JACCARD": {
        "fn": kg_runtime_header_jaccard,
        "expected_verdict": "ACCEPT",
        "description": "Runtime Header-Only Jaccard (validated discriminating)"
    },
    # Baselines
    "B-NULL-INSTRUMENT": {
        "fn": b_null_instrument,
        "expected_verdict": "REJECT",
        "description": "Constant statistic (zero dynamic range)"
    },
    "B-IDENTITY-CHANNEL": {
        "fn": b_identity_channel,
        "expected_verdict": "ACCEPT",
        "description": "Treatment = latent copy (maximum signal)"
    },
    "B-SHUFFLED-CHANNEL": {
        "fn": b_shuffled_channel,
        "expected_verdict": "REJECT",
        "description": "Random permutation within strata (zero MI)"
    },
    # Controls
    "PC-RUNTIME-HEADER-JACCARD": {
        "fn": pc_runtime_header_jaccard,
        "expected_verdict": "ACCEPT",
        "description": "Positive control: Runtime header Jaccard"
    },
    "NC-CONSTANT-ZERO": {
        "fn": nc_constant_zero,
        "expected_verdict": "REJECT",
        "description": "Null control: degenerate constant zero"
    },
}


def get_estimator(estimator_id: str) -> Callable:
    """Get estimator function by ID."""
    if estimator_id not in ESTIMATORS:
        raise ValueError(f"Unknown estimator: {estimator_id}")
    return ESTIMATORS[estimator_id]["fn"]


def get_expected_verdict(estimator_id: str) -> str:
    """Get expected verdict for estimator."""
    return ESTIMATORS[estimator_id]["expected_verdict"]


def get_all_estimator_ids() -> List[str]:
    """Get all estimator IDs in evaluation order."""
    return list(ESTIMATORS.keys())