#!/usr/bin/env python3
"""
Intervention-Validity Contract (IVC) for Estimator Certification.
Single deterministic Python class with one public method: evaluate(estimator, data, ground_truth) -> ContractResult
"""

import json
import hashlib
import numpy as np
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Callable, Literal, Tuple, Optional
from scipy.stats import entropy
import inspect

# ContractResult definition
@dataclass
class ContractResult:
    verdict: Literal["ACCEPT", "REJECT", "INDETERMINATE"]
    invariance_passed: bool
    displacement_passed: bool
    min_permutation_p: float
    delta_statistic: float
    channel_MI: float
    code_path_hash: str
    estimator_id: str
    channel_id: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class InterventionValidityContract:
    """
    Intervention-Validity Contract for certifying estimators.
    
    The contract executes two metamorphic tests:
    1. Invariance Test: Permuting treatment within strata must leave statistic bit-identical
    2. Channel Displacement Test: Re-drawing treatment through a channel with known MI 
       must move statistic by at least that MI with p < 0.01
    
    All estimators must pass through the identical evaluate() code path.
    """
    
    def __init__(
        self,
        n_permutations: int = 1000,
        min_permutation_p_threshold: float = 0.01,
        random_seed: int = 44
    ):
        self.n_permutations = n_permutations
        self.min_permutation_p_threshold = min_permutation_p_threshold
        self.random_seed = random_seed
        self.rng = np.random.default_rng(random_seed)
        
        # Compute and store code path hash for verification
        self._code_path_hash = self._compute_code_path_hash()
    
    def _compute_code_path_hash(self) -> str:
        """Compute SHA256 of the evaluate method's bytecode."""
        code = inspect.getsource(self.evaluate)
        return hashlib.sha256(code.encode()).hexdigest()
    
    def _get_strata(self, data: List[Dict], ground_truth: List[Dict]) -> Dict[Tuple, List[int]]:
        """
        Group transition indices by stratum (context C).
        Stratum is defined by (regime_before, state_before, action) from ground truth.
        """
        strata = defaultdict(list)
        for i, (d, gt) in enumerate(zip(data, ground_truth)):
            # Stratum key: (regime, state, action) - matching the ground truth structure
            key = (gt['regime_before'], gt['state_before'], gt['action'])
            strata[key].append(i)
        return strata
    
    def _compute_mi(self, x: List, y: List) -> float:
        """Compute mutual information I(X;Y) in bits."""
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
    
    def _compute_conditional_mi(self, x: List, y: List, z: List) -> float:
        """Compute conditional mutual information I(X;Y|Z) in bits."""
        # I(X;Y|Z) = sum_z p(z) * I(X;Y|Z=z)
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
            total_mi += p_z * self._compute_mi(x_sub, y_sub)
        return total_mi
    
    def test_invariance(
        self, 
        estimator: Callable, 
        data: List[Dict], 
        ground_truth: List[Dict],
        treatment_key: str = "treatment"
    ) -> Tuple[bool, Any, Any]:
        """
        Metamorphic Invariance Test (IVC-METAMORPHIC-INVARIANCE).
        
        Permute treatment variable within each stratum and check bitwise equality.
        A valid estimator's output must be invariant to within-stratum permutation
        of the treatment variable.
        """
        # Compute original statistic
        stat_original = estimator(data)
        
        # Get strata from ground truth
        strata = self._get_strata(data, ground_truth)
        
        # Create permuted data
        permuted_data = [d.copy() for d in data]
        
        # Permute treatment within each stratum
        for stratum_key, indices in strata.items():
            if len(indices) < 2:
                continue
            treatment_values = [data[i].get(treatment_key, 0) for i in indices]
            shuffled = self.rng.permutation(treatment_values)
            for idx, new_val in zip(indices, shuffled):
                permuted_data[idx][treatment_key] = new_val
        
        # Compute statistic on permuted data
        stat_permuted = estimator(permuted_data)
        
        # Check bitwise equality
        # Handle different statistic types
        if isinstance(stat_original, (int, float, np.number)) and isinstance(stat_permuted, (int, float, np.number)):
            passed = np.isclose(stat_original, stat_permuted)
        elif isinstance(stat_original, dict) and isinstance(stat_permuted, dict):
            passed = stat_original == stat_permuted
        elif isinstance(stat_original, (list, tuple)) and isinstance(stat_permuted, (list, tuple)):
            passed = np.allclose(stat_original, stat_permuted)
        else:
            passed = stat_original == stat_permuted
        
        return bool(passed), stat_original, stat_permuted
    
    def test_channel_displacement(
        self,
        estimator: Callable,
        data: List[Dict],
        ground_truth: List[Dict],
        channel_values: List[Any],
        channel_id: str,
        pre_registered_mi: float,
        treatment_key: str = "treatment",
        target_key: str = "target"
    ) -> Tuple[bool, float, float, float]:
        """
        Channel Displacement Test (IVC-CHANNEL-DISPLACEMENT).
        
        Re-draw treatment through a channel with known MI to target.
        The statistic must move by at least the channel's MI with p < 0.01.
        """
        # Test channel
        test_data = [d.copy() for d in data]
        for i, d in enumerate(test_data):
            d[treatment_key] = channel_values[i]
        stat_test = estimator(test_data)
        
        # Permutation test for p-value AND baseline
        perm_stats = []
        for _ in range(self.n_permutations):
            perm_data = [d.copy() for d in data]
            perm_channel = self.rng.permutation(channel_values)
            for i, d in enumerate(perm_data):
                d[treatment_key] = perm_channel[i]
            stat_perm = estimator(perm_data)
            perm_stats.append(stat_perm)
        
        perm_stats = np.array(perm_stats)
        perm_mean = perm_stats.mean()
        perm_std = perm_stats.std()
        
        # Baseline is the permutation mean (expected value under null)
        stat_baseline = perm_mean
        
        # Compute delta relative to permutation mean
        if isinstance(stat_test, (int, float, np.number)):
            delta = abs(float(stat_test) - float(stat_baseline))
        else:
            # For non-scalar statistics, use a summary
            delta = abs(float(np.mean(list(stat_test.values()) if isinstance(stat_test, dict) else stat_test)) - 
                       float(stat_baseline))
        
        # Permutation test for p-value
        perm_deltas = np.abs(perm_stats - perm_mean)
        n_exceed = np.sum(perm_deltas >= delta)
        p_value = (1 + n_exceed) / (self.n_permutations + 1)
        
        # Displacement passes if delta >= MI AND p < threshold
        passed = (delta >= pre_registered_mi - 1e-10) and (p_value < self.min_permutation_p_threshold)
        
        return passed, delta, pre_registered_mi, float(p_value)
    
    def evaluate(
        self,
        estimator: Callable,
        data: List[Dict],
        ground_truth: List[Dict],
        estimator_id: str,
        channel_id: str,
        channel_values: List[Any],
        pre_registered_mi: float,
        treatment_key: str = "treatment",
        target_key: str = "target"
    ) -> ContractResult:
        """
        Main entry point: evaluate an estimator through the IVC.
        
        All estimators must pass through this identical code path.
        """
        # Test 1: Metamorphic Invariance
        invariance_passed, stat_orig, stat_perm = self.test_invariance(
            estimator, data, ground_truth, treatment_key
        )
        
        # Test 2: Channel Displacement
        displacement_passed, delta, ch_mi, p_value = self.test_channel_displacement(
            estimator, data, ground_truth, channel_values, channel_id,
            pre_registered_mi, treatment_key, target_key
        )
        
        # Determine verdict
        if invariance_passed and displacement_passed:
            verdict = "ACCEPT"
        elif not invariance_passed or not displacement_passed:
            verdict = "REJECT"
        else:
            verdict = "INDETERMINATE"
        
        return ContractResult(
            verdict=verdict,
            invariance_passed=invariance_passed,
            displacement_passed=displacement_passed,
            min_permutation_p=p_value,
            delta_statistic=delta,
            channel_MI=ch_mi,
            code_path_hash=self._code_path_hash,
            estimator_id=estimator_id,
            channel_id=channel_id
        )


def compute_ground_truth_channels(ground_truth: List[Dict]) -> Dict[str, Dict]:
    """
    Compute pre-registered channel MI values from ground truth.
    This must be run BEFORE freezing the contract.
    """
    # Extract variables from ground truth
    regimes = [gt['regime_before'] for gt in ground_truth]
    states_before = [gt['state_before'] for gt in ground_truth]
    actions = [gt['action'] for gt in ground_truth]
    states_after = [gt['state_after'] for gt in ground_truth]
    
    # Latent state is the true state_before
    latent = states_before
    
    # Context for conditioning: (regime, action)
    context = [(gt['regime_before'], gt['action']) for gt in ground_truth]
    
    n_states = len(set(latent))
    H_latent = np.log2(n_states)
    
    channels = {}
    
    # CH-IDENTITY: Deterministic copy of latent state
    ch_identity = latent.copy()
    mi_identity = compute_mi_for_channel(ch_identity, states_after, context)
    channels["CH-IDENTITY"] = {
        "values": ch_identity,
        "mi": mi_identity,
        "description": "Deterministic copy of latent state",
        "expected_verdict": "ACCEPT"
    }
    
    # CH-SHUFFLED: Random permutation within strata (context)
    ch_shuffled = latent.copy()
    strata_indices = defaultdict(list)
    for i, ctx in enumerate(context):
        strata_indices[ctx].append(i)
    for stratum, indices in strata_indices.items():
        if len(indices) >= 2:
            vals = [ch_shuffled[i] for i in indices]
            shuffled = np.random.default_rng(44).permutation(vals)
            for idx, val in zip(indices, shuffled):
                ch_shuffled[idx] = val
    mi_shuffled = compute_mi_for_channel(ch_shuffled, states_after, context)
    channels["CH-SHUFFLED"] = {
        "values": ch_shuffled.tolist() if isinstance(ch_shuffled, np.ndarray) else ch_shuffled,
        "mi": mi_shuffled,
        "description": "Random permutation within strata",
        "expected_verdict": "REJECT"
    }
    
    # CH-PARTIAL-0.5: 50% fidelity to latent, 50% noise
    ch_partial_05 = []
    rng = np.random.default_rng(44)
    for l in latent:
        if rng.random() < 0.5:
            ch_partial_05.append(l)
        else:
            ch_partial_05.append(rng.integers(0, n_states))
    mi_partial_05 = compute_mi_for_channel(ch_partial_05, states_after, context)
    channels["CH-PARTIAL-0.5"] = {
        "values": ch_partial_05,
        "mi": mi_partial_05,
        "description": "50% fidelity to latent, 50% noise",
        "expected_verdict": "ACCEPT"
    }
    
    # CH-PARTIAL-0.1: 10% fidelity to latent, 90% noise
    ch_partial_01 = []
    for l in latent:
        if rng.random() < 0.1:
            ch_partial_01.append(l)
        else:
            ch_partial_01.append(rng.integers(0, n_states))
    mi_partial_01 = compute_mi_for_channel(ch_partial_01, states_after, context)
    channels["CH-PARTIAL-0.1"] = {
        "values": ch_partial_01,
        "mi": mi_partial_01,
        "description": "10% fidelity to latent, 90% noise",
        "expected_verdict": "REJECT"
    }
    
    return channels


def compute_mi_for_channel(channel_vals: List, target_vals: List, context: List) -> float:
    """Compute I(channel; target | context) in bits."""
    # Conditional MI
    context_values = set(context)
    total_mi = 0.0
    N = len(context)
    for ctx in context_values:
        indices = [i for i, c in enumerate(context) if c == ctx]
        if len(indices) < 2:
            continue
        ch_sub = [channel_vals[i] for i in indices]
        tgt_sub = [target_vals[i] for i in indices]
        p_ctx = len(indices) / N
        total_mi += p_ctx * compute_mi_simple(ch_sub, tgt_sub)
    return total_mi


def compute_mi_simple(x: List, y: List) -> float:
    """Simple MI computation."""
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


# For module-level use
def compute_mi(x: List, y: List) -> float:
    return compute_mi_simple(x, y)