#!/usr/bin/env python3
"""
EXP-PHYSICS-36279239922 — Calibration Experiment Execution
Browser-free, deterministic, seed=42. Implements the frozen spec exactly.

Calibration banks with known ground truth:
- B-INDEPENDENT-REGIME-NULL: regime-independent, matched marginals → p_bonf > 0.10, |BC| < 0.05
- CTRL_POS_NONCOPY_REGIME: non-copy regime-injected → p_bonf < 0.01, BC > 0.05, gap >= 0.05

Gates:
- G0: |perm_mean - analytic_mean| < 0.03 AND |analytic_mean| < 0.1 for each R on BOTH banks
- G1: Null bank p_bonf > 0.10 AND |BC| < 0.05
- G2: Positive bank p_bonf < 0.01 AND BC > 0.05 AND (BC_pos - BC_null) >= 0.05
- G3: MI(R; regime) > 0.3 AND MI(R; latent_state_index) < 0.9 on positive bank
"""

import json
import hashlib
import numpy as np
from scipy.special import gammaln, polygamma, digamma
from collections import defaultdict, Counter
from pathlib import Path
import sys

# Frozen seeds
SEED = 42
PYTHONHASHSEED = 0
N_PERMUTATIONS = 1000
N_TRAJECTORIES = 40
N_STEPS = 40
N_STATES = 5
N_ACTIONS = 5
N_REGIMES = 2

np.random.seed(SEED)
rng = np.random.default_rng(SEED)

# ──────────────────────────────────────────────────────────────
# 1. Latent FSM and Bank Construction
# ──────────────────────────────────────────────────────────────

ACTIONS = ['click', 'fill', 'select', 'navigate', 'type']
REGIMES = ['A', 'B']

# Transition kernels: P(next_state | cur_state, action, regime)
# Null bank: SAME kernel for both regimes
# Positive bank: DIFFERENT kernels per regime

# Base transition matrix: [cur_state, action, next_state] -> prob
# We'll use a fixed stochastic matrix for reproducibility
def build_transition_kernels():
    """Build transition kernels for null (same) and positive (different) banks."""
    rng_kernels = np.random.default_rng(SEED + 1000)
    
    # Null kernel: same for both regimes
    null_kernel = np.zeros((N_STATES, N_ACTIONS, N_STATES))
    for s in range(N_STATES):
        for a in range(N_ACTIONS):
            probs = rng_kernels.dirichlet(np.ones(N_STATES) * 0.5)
            null_kernel[s, a] = probs
    
    # Positive kernels: different per regime
    pos_kernel_A = np.zeros((N_STATES, N_ACTIONS, N_STATES))
    pos_kernel_B = np.zeros((N_STATES, N_ACTIONS, N_STATES))
    for s in range(N_STATES):
        for a in range(N_ACTIONS):
            probs_A = rng_kernels.dirichlet(np.ones(N_STATES) * 0.5)
            probs_B = rng_kernels.dirichlet(np.ones(N_STATES) * 0.5)
            pos_kernel_A[s, a] = probs_A
            pos_kernel_B[s, a] = probs_B
    
    return null_kernel, pos_kernel_A, pos_kernel_B

NULL_KERNEL, POS_KERNEL_A, POS_KERNEL_B = build_transition_kernels()

def sample_next_state(kernel, cur_state, action):
    """Sample next_state from kernel[cur_state, action]."""
    return int(rng.choice(N_STATES, p=kernel[cur_state, action]))

def generate_url(state):
    return f"https://fsm.local/state/{state}"

def generate_title(state):
    return f"State {state}"

def generate_dom_cluster(state):
    # Simple clustering: states 0,1 -> cluster 0; 2,3 -> cluster 1; 4 -> cluster 2
    return state // 2

def hash_state(state, title, dom_cluster):
    """16-char SHA256 of (url_after, title_after, dom_cluster)."""
    s = f"{generate_url(state)}|{title}|{dom_cluster}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def build_history_context(url_before, history_deque):
    """C = (URL_before_norm, H_K=3) where H_K=3 is 3-step URL history."""
    url_norm = url_before.replace("https://fsm.local/state/", "s")
    hist = tuple(list(history_deque)[-3:])  # last 3 URLs
    return (url_norm, hist)

def generate_R_channels(cur_state, action, regime, bank_type, noise_rate=0.10):
    """
    Generate four R channels from latent variables.
    Bank 1 (null): R depends on (cur_state, action) ONLY — no regime info.
    Bank 2 (positive): R depends on (cur_state, action, regime) through STOCHASTIC MIXING CHANNEL.
    """
    base_str = f"{cur_state}:{action}"
    
    if bank_type == "null":
        # Null bank: regime NOT used in R generation
        regime_for_hash = ""  # empty - no regime info
    else:
        # Positive bank: regime enters through XOR mixing channel
        regime_for_hash = regime
    
    channels = {}
    
    # R_visible_text_hash: SHA256(f"vis:{cur_state}:{action}:{regime}")[:16] with relabel noise
    if bank_type == "null":
        vis_str = f"vis:{cur_state}:{action}"
    else:
        # XOR mixing: hash(cur_state, action) XOR hash(regime) + noise
        h1 = hashlib.sha256(f"{cur_state}:{action}".encode()).digest()
        h2 = hashlib.sha256(regime.encode()).digest()
        xor_bytes = bytes(a ^ b for a, b in zip(h1, h2))
        vis_str = f"vis:{xor_bytes.hex()[:16]}"
    
    if rng.random() < noise_rate:
        vis_str = f"noise_{rng.integers(1000000)}"
    channels['R_visible_text_hash'] = hashlib.sha256(vis_str.encode()).hexdigest()[:16]
    
    # R_visual: SHA256(f"vis:{cur_state}:{action}")[:16] with relabel noise
    visual_str = f"vis:{cur_state}:{action}"
    if rng.random() < noise_rate:
        visual_str = f"noise_{rng.integers(1000000)}"
    channels['R_visual'] = hashlib.sha256(visual_str.encode()).hexdigest()[:16]
    
    # R_computed_style: SHA256(f"css:{cur_state}:{action}")[:16] with relabel noise
    css_str = f"css:{cur_state}:{action}"
    if rng.random() < noise_rate:
        css_str = f"noise_{rng.integers(1000000)}"
    channels['R_computed_style'] = hashlib.sha256(css_str.encode()).hexdigest()[:16]
    
    # R_AX: SHA256(f"ax:{cur_state}:{action}")[:16] with relabel noise (0.08)
    ax_str = f"ax:{cur_state}:{action}"
    if rng.random() < 0.08:
        ax_str = f"noise_{rng.integers(1000000)}"
    channels['R_AX'] = hashlib.sha256(ax_str.encode()).hexdigest()[:16]
    
    return channels

def build_bank(bank_type, kernel_A=None, kernel_B=None):
    """
    Build a calibration bank.
    bank_type: 'null' (B-INDEPENDENT-REGIME-NULL) or 'positive' (CTRL_POS_NONCOPY_REGIME)
    """
    transitions = []
    trajectory_ids = []
    
    for traj_id in range(N_TRAJECTORIES):
        regime = REGIMES[traj_id % 2]  # Alternate A, B
        cur_state = rng.integers(N_STATES)
        history = []
        
        for step in range(N_STEPS):
            url_before = generate_url(cur_state)
            action = ACTIONS[rng.integers(N_ACTIONS)]
            
            # Build context C
            C = build_history_context(url_before, history)
            
            # Sample next_state
            if bank_type == "null":
                next_state = sample_next_state(NULL_KERNEL, cur_state, rng.integers(N_ACTIONS))
            else:
                kernel = POS_KERNEL_A if regime == 'A' else POS_KERNEL_B
                next_state = sample_next_state(kernel, cur_state, rng.integers(N_ACTIONS))
            
            # S_next hash
            title_after = generate_title(next_state)
            dom_cluster = generate_dom_cluster(next_state)
            S_next = hash_state(next_state, title_after, dom_cluster)
            
            # Generate R channels
            R_channels = generate_R_channels(cur_state, action, regime, bank_type)
            
            transition = {
                'trajectory_id': traj_id,
                'step': step,
                'regime': regime,
                'cur_state': cur_state,
                'action': action,
                'url_before': url_before,
                'C': C,
                'S_next': S_next,
                'R': R_channels,
                'latent_state_index': cur_state  # for MI(R; latent_state) computation
            }
            transitions.append(transition)
            trajectory_ids.append(traj_id)
            
            # Update history and current state
            history.append(url_before)
            cur_state = next_state
    
    return transitions

def build_iid_null_bank(positive_transitions):
    """Build B-IID-MARGINAL-NULL by resampling S_next from marginal of positive bank."""
    # Get marginal distribution of S_next from positive bank
    S_next_list = [t['S_next'] for t in positive_transitions]
    S_next_values, counts = np.unique(S_next_list, return_counts=True)
    probs = counts / counts.sum()
    
    iid_transitions = []
    for t in positive_transitions:
        new_S_next = rng.choice(S_next_values, p=probs)
        new_t = t.copy()
        new_t['S_next'] = new_S_next
        iid_transitions.append(new_t)
    return iid_transitions

def build_history_markov_baseline(transitions):
    """Build B-HISTORY-MARKOV: P(S_next | C, A) without R."""
    # This is just the transitions with R removed - we'll compute baseline CMI = 0
    return transitions  # Same transitions, baseline uses no R

# ──────────────────────────────────────────────────────────────
# 2. Entropy Estimation: Exact Dirichlet-Multinomial Plug-in
# ──────────────────────────────────────────────────────────────

def compute_dm_entropy(counts, K, alpha):
    """
    Exact Dirichlet-Multinomial plug-in entropy in bits.
    counts: array of observed counts for each state (length = observed states)
    K: total support size (n_states_observed in TRAIN)
    alpha: concentration parameter = 1/K
    Returns H in bits.
    """
    N = counts.sum()
    alpha0 = K * alpha
    
    # Expected probability for each observed state
    p_obs = (counts + alpha) / (N + alpha0)
    # Expected probability for each unobserved state
    p_unobs = alpha / (N + alpha0)
    n_unobs = K - len(counts)
    
    # Entropy = -Σ p_i log2(p_i)
    H = -np.sum(p_obs * np.log2(p_obs))
    if n_unobs > 0:
        H -= n_unobs * p_unobs * np.log2(p_unobs)
    
    return H

def compute_conditional_entropy(transitions, strata_key_fn, K_per_stratum, alpha_per_stratum):
    """
    Compute H(S_next | C) or H(S_next | C, R) using DM plug-in with shared support.
    Returns weighted average entropy in bits.
    Strata not in TRAIN (no K/alpha) are skipped.
    """
    # Group by stratum
    strata = defaultdict(list)
    for t in transitions:
        strata[strata_key_fn(t)].append(t['S_next'])
    
    total_N = len(transitions)
    H_weighted = 0.0
    used_N = 0
    
    for stratum, S_next_list in strata.items():
        if len(S_next_list) < 2:
            continue
        if stratum not in K_per_stratum:
            continue  # Skip strata not in TRAIN
        counts = np.array([v for v in Counter(S_next_list).values()])
        K = K_per_stratum[stratum]
        alpha = alpha_per_stratum[stratum]
        H_stratum = compute_dm_entropy(counts, K, alpha)
        H_weighted += (len(S_next_list) / total_N) * H_stratum
        used_N += len(S_next_list)
    
    return H_weighted

# ──────────────────────────────────────────────────────────────
# 3. Representation-Dependent Analytic Null (G0)
# ──────────────────────────────────────────────────────────────

def compute_analytic_null(transitions, strata_key_fn, K_per_stratum, alpha_per_stratum):
    """
    Compute per-stratum Dirichlet-Multinomial log marginal likelihood in BITS.
    Returns (analytic_mean, analytic_std) in bits.
    Strata not in TRAIN (no K/alpha) are skipped.
    """
    strata = defaultdict(list)
    for t in transitions:
        strata[strata_key_fn(t)].append(t['S_next'])
    
    total_N = len(transitions)
    log_marginal_weighted = 0.0
    trigamma_weighted = 0.0
    used_N = 0
    
    for stratum, S_next_list in strata.items():
        N_c = len(S_next_list)
        if N_c < 2:
            continue
        if stratum not in K_per_stratum:
            continue  # Skip strata not in TRAIN
        counts = np.array([v for v in Counter(S_next_list).values()])
        K_c = K_per_stratum[stratum]
        alpha_c = alpha_per_stratum[stratum]
        alpha0 = K_c * alpha_c  # = 1.0
        
        # log marginal likelihood in nats
        log_marginal_nats = (gammaln(alpha0) - gammaln(N_c + alpha0) + 
                            np.sum(gammaln(counts + alpha_c) - gammaln(alpha_c)))
        # Convert to bits
        log_marginal_bits = log_marginal_nats / np.log(2)
        
        # Trigamma for variance
        trigamma_c = abs(polygamma(1, alpha0) - polygamma(1, N_c + alpha0))
        
        weight = N_c / total_N
        log_marginal_weighted += weight * log_marginal_bits
        trigamma_weighted += weight * trigamma_c
        used_N += N_c
    
    analytic_mean = log_marginal_weighted
    analytic_std = np.sqrt(trigamma_weighted / np.log(2)**2) if used_N > 0 else 0.0
    
    return analytic_mean, analytic_std

# ──────────────────────────────────────────────────────────────
# 4. Permutation Test
# ──────────────────────────────────────────────────────────────

def compute_cmi_for_R(transitions, R_channel, C_key_fn, R_key_fn, K_per_stratum, alpha_per_stratum):
    """Compute I(S_next; R | C) for a specific R channel."""
    # H(S_next | C)
    H_C = compute_conditional_entropy(transitions, C_key_fn, K_per_stratum, alpha_per_stratum)
    
    # H(S_next | C, R)
    def CR_key_fn(t):
        return (C_key_fn(t), R_key_fn(t))
    H_CR = compute_conditional_entropy(transitions, CR_key_fn, K_per_stratum, alpha_per_stratum)
    
    # CMI = H(S_next|C) - H(S_next|C,R) — guaranteed >= 0 with shared K, alpha
    cmi = H_C - H_CR
    return max(0.0, cmi), H_C, H_CR

def permute_within_strata(transitions, C_key_fn, R_key_fn, rng_perm):
    """Trajectory-grouped shuffle within each C stratum."""
    # Group by (trajectory_id, C_stratum)
    groups = defaultdict(list)
    for i, t in enumerate(transitions):
        key = (t['trajectory_id'], C_key_fn(t))
        groups[key].append(i)
    
    # Shuffle R values within each C stratum (not within trajectory groups)
    # Actually: trajectory-grouped shuffle means we permute trajectory IDs within each C stratum
    strata_to_traj = defaultdict(set)
    for key in groups:
        traj_id, C_stratum = key
        strata_to_traj[C_stratum].add(traj_id)
    
    # Build mapping: for each C stratum, permute trajectory IDs
    traj_perm = {}
    for C_stratum, traj_ids in strata_to_traj.items():
        traj_list = list(traj_ids)
        permuted = rng_perm.permutation(traj_list)
        for orig, perm in zip(traj_list, permuted):
            traj_perm[(orig, C_stratum)] = perm
    
    # Create permuted transitions
    permuted_transitions = []
    for t in transitions:
        orig_traj = t['trajectory_id']
        C_stratum = C_key_fn(t)
        new_traj = traj_perm.get((orig_traj, C_stratum), orig_traj)
        new_t = t.copy()
        new_t['trajectory_id'] = new_traj
        # R stays with the original transition (we're shuffling which trajectory gets which R)
        # Actually, we need to shuffle R values across trajectories within each C stratum
        permuted_transitions.append(new_t)
    
    # Now we need to reassign R values based on permuted trajectory IDs
    # Build lookup of R by (trajectory_id, step) for original
    R_lookup = {}
    for t in transitions:
        R_lookup[(t['trajectory_id'], t['step'])] = t['R']
    
    # Assign R from permuted trajectory
    for t in permuted_transitions:
        orig_key = (traj_perm.get((t['trajectory_id'], C_key_fn(t)), t['trajectory_id']), t['step'])
        # This is getting complex. Let me simplify: just permute R within each C stratum
        pass
    
    # Simpler approach: permute R values within each C stratum directly
    strata_indices = defaultdict(list)
    for i, t in enumerate(transitions):
        strata_indices[C_key_fn(t)].append(i)
    
    permuted = [t.copy() for t in transitions]
    for stratum, indices in strata_indices.items():
        # Get R values for this stratum
        R_values = [transitions[i]['R'][R_channel] for i in indices]
        # Shuffle
        shuffled = rng_perm.permutation(R_values)
        # Assign back
        for idx, new_R in zip(indices, shuffled):
            permuted[idx]['R'][R_channel] = new_R
    
    return permuted

def run_permutation_test(transitions, R_channel, C_key_fn, R_key_fn, 
                         K_per_stratum, alpha_per_stratum, n_perms=N_PERMUTATIONS):
    """Run permutation test for one R channel."""
    # Observed CMI
    obs_cmi, H_C, H_CR = compute_cmi_for_R(transitions, R_channel, C_key_fn, R_key_fn, 
                                            K_per_stratum, alpha_per_stratum)
    
    # Permutation distribution
    perm_cmis = []
    rng_perm = np.random.default_rng(SEED + 10000)  # Fixed seed for reproducibility
    
    for _ in range(n_perms):
        # Permute R within each C stratum
        permuted = [t.copy() for t in transitions]
        strata_indices = defaultdict(list)
        for i, t in enumerate(transitions):
            strata_indices[C_key_fn(t)].append(i)
        
        for stratum, indices in strata_indices.items():
            R_values = [transitions[i]['R'][R_channel] for i in indices]
            shuffled = rng_perm.permutation(R_values)
            for idx, new_R in zip(indices, shuffled):
                permuted[idx]['R'][R_channel] = new_R
        
        perm_cmi, _, _ = compute_cmi_for_R(permuted, R_channel, C_key_fn, R_key_fn,
                                           K_per_stratum, alpha_per_stratum)
        perm_cmis.append(perm_cmi)
    
    perm_cmis = np.array(perm_cmis)
    perm_mean = perm_cmis.mean()
    perm_std = perm_cmis.std()
    
    # p-value
    n_exceed = np.sum(perm_cmis >= obs_cmi)
    p_raw = (1 + n_exceed) / (n_perms + 1)
    
    return {
        'obs_cmi': obs_cmi,
        'perm_mean': perm_mean,
        'perm_std': perm_std,
        'perm_cmis': perm_cmis,
        'p_raw': p_raw,
        'H_C': H_C,
        'H_CR': H_CR
    }

# ──────────────────────────────────────────────────────────────
# 5. MI Computation for Identifiability (G3)
# ──────────────────────────────────────────────────────────────

def compute_mi(x_vals, y_vals):
    """Compute MI(X;Y) in bits using plug-in estimator."""
    joint = Counter(zip(x_vals, y_vals))
    px = Counter(x_vals)
    py = Counter(y_vals)
    N = len(x_vals)
    
    mi = 0.0
    for (x, y), count in joint.items():
        p_xy = count / N
        p_x = px[x] / N
        p_y = py[y] / N
        if p_x > 0 and p_y > 0:
            mi += p_xy * np.log2(p_xy / (p_x * p_y))
    return mi

# ──────────────────────────────────────────────────────────────
# 6. Main Experiment Execution
# ──────────────────────────────────────────────────────────────

def run_experiment():
    print("=" * 70)
    print("EXP-PHYSICS-36279239922 — Calibration Experiment")
    print("=" * 70)
    
    # Build calibration banks
    print("\n[1/7] Building calibration banks...")
    null_bank = build_bank("null")
    positive_bank = build_bank("positive")
    iid_null_bank = build_iid_null_bank(positive_bank)
    history_baseline_bank = build_history_markov_baseline(positive_bank)
    
    print(f"  Null bank: {len(null_bank)} transitions")
    print(f"  Positive bank: {len(positive_bank)} transitions")
    print(f"  IID null bank: {len(iid_null_bank)} transitions")
    print(f"  History baseline: {len(history_baseline_bank)} transitions")
    
    # TRAIN/TEST split (70/30 by trajectory_id)
    print("\n[2/7] TRAIN/TEST split (70/30 by trajectory_id)...")
    traj_ids = list(range(N_TRAJECTORIES))
    rng_split = np.random.default_rng(SEED)
    permuted = rng_split.permutation(traj_ids)
    n_train = int(0.7 * N_TRAJECTORIES)
    train_traj = set(permuted[:n_train])
    test_traj = set(permuted[n_train:])
    
    def split_bank(bank):
        train = [t for t in bank if t['trajectory_id'] in train_traj]
        test = [t for t in bank if t['trajectory_id'] in test_traj]
        return train, test
    
    null_train, null_test = split_bank(null_bank)
    pos_train, pos_test = split_bank(positive_bank)
    iid_train, iid_test = split_bank(iid_null_bank)
    hist_train, hist_test = split_bank(history_baseline_bank)
    
    print(f"  Null: train={len(null_train)}, test={len(null_test)}")
    print(f"  Positive: train={len(pos_train)}, test={len(pos_test)}")
    
    # Build strata and vocabularies on TRAIN only
    print("\n[3/7] Building strata and vocabularies (TRAIN only)...")
    
    def C_key_fn(t):
        return t['C']
    
    def R_key_fn(t, channel):
        return t['R'][channel]
    
    R_channels = ['R_visible_text_hash', 'R_visual', 'R_computed_style', 'R_AX']
    
    # Get all unique S_next in TRAIN for each bank
    def get_K_per_stratum(train_transitions):
        strata_S_next = defaultdict(set)
        for t in train_transitions:
            strata_S_next[C_key_fn(t)].add(t['S_next'])
        return {stratum: len(states) for stratum, states in strata_S_next.items()}
    
    K_null = get_K_per_stratum(null_train)
    K_pos = get_K_per_stratum(pos_train)
    K_iid = get_K_per_stratum(iid_train)
    K_hist = get_K_per_stratum(hist_train)
    
    alpha_null = {s: 1.0/K_null[s] for s in K_null}
    alpha_pos = {s: 1.0/K_pos[s] for s in K_pos}
    alpha_iid = {s: 1.0/K_iid[s] for s in K_iid}
    alpha_hist = {s: 1.0/K_hist[s] for s in K_hist}
    
    print(f"  Null bank: {len(K_null)} strata, K per stratum: {list(K_null.values())[:5]}...")
    print(f"  Positive bank: {len(K_pos)} strata, K per stratum: {list(K_pos.values())[:5]}...")
    
    # Compute metrics on TEST set using TRAIN-fitted parameters
    print("\n[4/7] Computing metrics on TEST set...")
    
    def compute_bank_metrics(bank_name, test_transitions, K_per_stratum, alpha_per_stratum):
        metrics = {}
        for R_channel in R_channels:
            print(f"  {bank_name} - {R_channel}...")
            
            # Permutation test
            perm_result = run_permutation_test(
                test_transitions, R_channel, C_key_fn, 
                lambda t, ch=R_channel: R_key_fn(t, ch),
                K_per_stratum, alpha_per_stratum
            )
            
            # Analytic null
            analytic_mean, analytic_std = compute_analytic_null(
                test_transitions, C_key_fn, K_per_stratum, alpha_per_stratum
            )
            
            # BC = obs - perm_mean
            BC = perm_result['obs_cmi'] - perm_result['perm_mean']
            
            metrics[R_channel] = {
                'M_OBS_CMI_bits': perm_result['obs_cmi'],
                'M_PERM_MEAN_bits': perm_result['perm_mean'],
                'M_PERM_STD_bits': perm_result['perm_std'],
                'M_BC_PERM_bits': BC,
                'M_P_RAW': perm_result['p_raw'],
                'M_ANALYTIC_MEAN_bits': analytic_mean,
                'M_ANALYTIC_STD_bits': analytic_std,
                'M_CONS_bits': abs(perm_result['perm_mean'] - analytic_mean),
                'M_H_Snext_given_C_bits': perm_result['H_C'],
                'M_H_Snext_given_CR_bits': perm_result['H_CR'],
            }
        
        # Collinearity check: pairwise BC correlation
        BC_vals = [metrics[ch]['M_BC_PERM_bits'] for ch in R_channels]
        if len(R_channels) > 1:
            BC_array = np.array([BC_vals])
            if np.std(BC_vals) > 0:
                corr_matrix = np.corrcoef(BC_array)
                effective_n_tests = 0
                for i in range(len(R_channels)):
                    for j in range(i+1, len(R_channels)):
                        if abs(corr_matrix[i, j]) < 0.95:
                            effective_n_tests += 1
                effective_n_tests = max(1, effective_n_tests + 1)
            else:
                # All BC values identical - perfect collinearity
                effective_n_tests = 1
        else:
            effective_n_tests = 1
        
        # Bonferroni correction
        for R_channel in R_channels:
            p_bonf = min(1.0, metrics[R_channel]['M_P_RAW'] * effective_n_tests)
            metrics[R_channel]['M_P_BONF'] = max(0.001, p_bonf)
            metrics[R_channel]['M_REL_SEP'] = (metrics[R_channel]['M_BC_PERM_bits'] / 
                                               max(metrics[R_channel]['M_ANALYTIC_STD_bits'], 
                                                   metrics[R_channel]['M_PERM_STD_bits'], 0.005))
        
        metrics['M_effective_n_tests'] = effective_n_tests
        metrics['M_K_observed'] = list(K_per_stratum.values())
        metrics['M_N_strata'] = len(K_per_stratum)
        metrics['M_N_transitions'] = len(test_transitions)
        
        return metrics
    
    null_metrics = compute_bank_metrics("Null", null_test, K_null, alpha_null)
    pos_metrics = compute_bank_metrics("Positive", pos_test, K_pos, alpha_pos)
    iid_metrics = compute_bank_metrics("IID_Null", iid_test, K_iid, alpha_iid)
    hist_metrics = compute_bank_metrics("History", hist_test, K_hist, alpha_hist)
    
    # Compute MI for identifiability (G3) on positive bank TRAIN
    print("\n[5/7] Computing identifiability metrics (G3)...")
    MI_R_regime = {}
    MI_R_latent = {}
    for R_channel in R_channels:
        R_vals = [t['R'][R_channel] for t in pos_train]
        regime_vals = [t['regime'] for t in pos_train]
        latent_vals = [t['latent_state_index'] for t in pos_train]
        MI_R_regime[R_channel] = compute_mi(R_vals, regime_vals)
        MI_R_latent[R_channel] = compute_mi(R_vals, latent_vals)
        print(f"  {R_channel}: MI(R;regime)={MI_R_regime[R_channel]:.4f}, MI(R;latent)={MI_R_latent[R_channel]:.4f}")
    
    # Gap: BC_pos - BC_null (averaged over channels)
    print("\n[6/7] Computing gates...")
    BC_null_avg = np.mean([null_metrics[ch]['M_BC_PERM_bits'] for ch in R_channels])
    BC_pos_avg = np.mean([pos_metrics[ch]['M_BC_PERM_bits'] for ch in R_channels])
    gap = BC_pos_avg - BC_null_avg
    print(f"  BC_null_avg = {BC_null_avg:.6f}")
    print(f"  BC_pos_avg = {BC_pos_avg:.6f}")
    print(f"  Gap = {gap:.6f}")
    
    # Gate checks
    print("\n[7/7] Checking gates...")
    
    # G0: Analytic centering
    G0_pass = True
    G0_details = {}
    for bank_name, bank_metrics in [("Null", null_metrics), ("Positive", pos_metrics)]:
        for R_channel in R_channels:
            cons = bank_metrics[R_channel]['M_CONS_bits']
            analytic_mean = bank_metrics[R_channel]['M_ANALYTIC_MEAN_bits']
            pass_g0 = (cons < 0.03) and (abs(analytic_mean) < 0.1)
            G0_details[f"{bank_name}_{R_channel}"] = {
                'consistency': cons,
                'analytic_mean': analytic_mean,
                'pass': pass_g0
            }
            if not pass_g0:
                G0_pass = False
            print(f"  G0 {bank_name} {R_channel}: cons={cons:.6f}, analytic_mean={analytic_mean:.6f}, PASS={pass_g0}")
    
    # G1: Null bank validity
    G1_pass = True
    G1_details = {}
    for R_channel in R_channels:
        p_bonf = null_metrics[R_channel]['M_P_BONF']
        BC = null_metrics[R_channel]['M_BC_PERM_bits']
        pass_g1 = (p_bonf > 0.10) and (abs(BC) < 0.05)
        G1_details[R_channel] = {'p_bonf': p_bonf, 'BC': BC, 'pass': pass_g1}
        if not pass_g1:
            G1_pass = False
        print(f"  G1 Null {R_channel}: p_bonf={p_bonf:.6f}, BC={BC:.6f}, PASS={pass_g1}")
    
    # G2: Positive bank sensitivity
    G2_pass = True
    G2_details = {}
    for R_channel in R_channels:
        p_bonf = pos_metrics[R_channel]['M_P_BONF']
        BC = pos_metrics[R_channel]['M_BC_PERM_bits']
        gap_ch = BC - null_metrics[R_channel]['M_BC_PERM_bits']
        pass_g2 = (p_bonf < 0.01) and (BC > 0.05) and (gap_ch >= 0.05)
        G2_details[R_channel] = {'p_bonf': p_bonf, 'BC': BC, 'gap': gap_ch, 'pass': pass_g2}
        if not pass_g2:
            G2_pass = False
        print(f"  G2 Pos {R_channel}: p_bonf={p_bonf:.6f}, BC={BC:.6f}, gap={gap_ch:.6f}, PASS={pass_g2}")
    
    # G3: Identifiability (non-copy)
    G3_pass = True
    G3_details = {}
    for R_channel in R_channels:
        mi_regime = MI_R_regime[R_channel]
        mi_latent = MI_R_latent[R_channel]
        pass_g3 = (mi_regime > 0.3) and (mi_latent < 0.9)
        G3_details[R_channel] = {'MI_R_regime': mi_regime, 'MI_R_latent': mi_latent, 'pass': pass_g3}
        if not pass_g3:
            G3_pass = False
        print(f"  G3 {R_channel}: MI(R;regime)={mi_regime:.4f}, MI(R;latent)={mi_latent:.4f}, PASS={pass_g3}")
    
    all_gates_pass = G0_pass and G1_pass and G2_pass and G3_pass
    print(f"\n{'='*70}")
    print(f"G0 (Analytic Centering): {'PASS' if G0_pass else 'FAIL'}")
    print(f"G1 (Null Bank Validity): {'PASS' if G1_pass else 'FAIL'}")
    print(f"G2 (Positive Bank Sensitivity): {'PASS' if G2_pass else 'FAIL'}")
    print(f"G3 (Identifiability Non-Copy): {'PASS' if G3_pass else 'FAIL'}")
    print(f"OVERALL: {'CALIBRATED' if all_gates_pass else 'NOT_INSTRUMENTED'}")
    print(f"{'='*70}")
    
    # Prepare outputs
    return {
        'null_bank': null_bank,
        'positive_bank': positive_bank,
        'iid_null_bank': iid_null_bank,
        'history_baseline_bank': history_baseline_bank,
        'null_metrics': null_metrics,
        'pos_metrics': pos_metrics,
        'iid_metrics': iid_metrics,
        'hist_metrics': hist_metrics,
        'MI_R_regime': MI_R_regime,
        'MI_R_latent': MI_R_latent,
        'G0_pass': G0_pass,
        'G1_pass': G1_pass,
        'G2_pass': G2_pass,
        'G3_pass': G3_pass,
        'G0_details': G0_details,
        'G1_details': G1_details,
        'G2_details': G2_details,
        'G3_details': G3_details,
        'all_gates_pass': all_gates_pass,
        'BC_null_avg': BC_null_avg,
        'BC_pos_avg': BC_pos_avg,
        'gap': gap,
        'R_channels': R_channels,
        'train_traj': train_traj,
        'test_traj': test_traj,
        'K_null': K_null,
        'K_pos': K_pos,
        'K_iid': K_iid,
        'K_hist': K_hist,
    }

if __name__ == "__main__":
    results = run_experiment()
    
    # Save raw evidence
    exp_dir = Path("/home/runner/work/Spider/Spider/research/experiments/EXP-PHYSICS-36279239922")
    
    # Save raw banks
    for name, bank in [('raw_transitions_null_bank.json', results['null_bank']),
                       ('raw_transitions_positive_bank.json', results['positive_bank']),
                       ('raw_transitions_iid_null.json', results['iid_null_bank']),
                       ('raw_transitions_history_baseline.json', results['history_baseline_bank'])]:
        with open(exp_dir / name, 'w') as f:
            json.dump(bank, f, indent=2)
    
    # Save derived artifacts
    analytic_stats = {}
    for bank_name, bank_metrics in [('Null', results['null_metrics']), ('Positive', results['pos_metrics'])]:
        for R_channel in results['R_channels']:
            analytic_stats[f"{bank_name}_{R_channel}"] = {
                'analytic_mean': bank_metrics[R_channel]['M_ANALYTIC_MEAN_bits'],
                'analytic_std': bank_metrics[R_channel]['M_ANALYTIC_STD_bits'],
            }
    with open(exp_dir / 'analytic_null_stats.json', 'w') as f:
        json.dump(analytic_stats, f, indent=2)
    
    # Save permutation results (summary only, full arrays too large)
    perm_summary = {}
    for bank_name, bank_metrics in [('Null', results['null_metrics']), ('Positive', results['pos_metrics'])]:
        for R_channel in results['R_channels']:
            perm_summary[f"{bank_name}_{R_channel}"] = {
                'perm_mean': bank_metrics[R_channel]['M_PERM_MEAN_bits'],
                'perm_std': bank_metrics[R_channel]['M_PERM_STD_bits'],
                'obs_cmi': bank_metrics[R_channel]['M_OBS_CMI_bits'],
                'p_raw': bank_metrics[R_channel]['M_P_RAW'],
            }
    with open(exp_dir / 'permutation_results.json', 'w') as f:
        json.dump(perm_summary, f, indent=2)
    
    print("\nRaw evidence and derived artifacts saved.")
    print("Now computing final packet outputs...")