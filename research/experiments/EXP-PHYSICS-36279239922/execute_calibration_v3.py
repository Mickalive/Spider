#!/usr/bin/env python3
"""
EXP-PHYSICS-36279239922 — Calibration Experiment (v3)
Fixed: regime switching within trajectory, short hash for R, corrected analytic.
"""

import json
import hashlib
import numpy as np
from scipy.special import digamma, polygamma
from collections import defaultdict, Counter
from pathlib import Path
import pickle

SEED = 42
N_PERMUTATIONS = 1000
N_TRAJECTORIES = 40
N_STEPS = 40
N_STATES = 5
N_ACTIONS = 5

np.random.seed(SEED)
rng = np.random.default_rng(SEED)

ACTIONS = ['click', 'fill', 'select', 'navigate', 'type']
REGIMES = ['A', 'B']

def build_transition_kernels():
    rng_k = np.random.default_rng(SEED + 1000)
    null_kernel = np.zeros((N_STATES, N_ACTIONS, N_STATES))
    pos_kernel_A = np.zeros((N_STATES, N_ACTIONS, N_STATES))
    pos_kernel_B = np.zeros((N_STATES, N_ACTIONS, N_STATES))
    for s in range(N_STATES):
        for a in range(N_ACTIONS):
            base = rng_k.dirichlet(np.ones(N_STATES) * 0.5)
            null_kernel[s, a] = base
            # Positive: SMALL difference between regimes (so history doesn't reveal regime)
            perturb_A = rng_k.normal(0, 0.05, N_STATES)
            perturb_B = rng_k.normal(0, 0.05, N_STATES)
            pos_kernel_A[s, a] = np.clip(base + perturb_A, 0.01, None)
            pos_kernel_A[s, a] /= pos_kernel_A[s, a].sum()
            pos_kernel_B[s, a] = np.clip(base + perturb_B, 0.01, None)
            pos_kernel_B[s, a] /= pos_kernel_B[s, a].sum()
    return null_kernel, pos_kernel_A, pos_kernel_B

NULL_KERNEL, POS_KERNEL_A, POS_KERNEL_B = build_transition_kernels()

def sample_next_state(kernel, cur_state, action):
    return int(rng.choice(N_STATES, p=kernel[cur_state, action]))

def generate_url(state):
    return f"https://fsm.local/state/{state}"

def hash_state(state, title, dom_cluster):
    s = f"{generate_url(state)}|{title}|{dom_cluster}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def build_history_context(url_before, history_deque):
    url_norm = url_before.replace("https://fsm.local/state/", "s")
    hist = tuple(list(history_deque)[-3:])
    return (url_norm, hist)

def short_hash(s, length=4):
    """Short hash to create collisions and reduce MI with latent state."""
    return hashlib.sha256(s.encode()).hexdigest()[:length]

def generate_R_channels(cur_state, action, regime, bank_type, step_in_traj):
    """
    NULL: R from (cur_state, action) only, high noise, short hash.
    POSITIVE: R from (cur_state, action, regime) with regime as PRIMARY signal, short hash.
    Regime switches every 10 steps within trajectory (so C doesn't identify it).
    """
    channels = {}
    latent_sig = f"{cur_state}:{action}"
    
    # Regime for this step: switches every 10 steps
    # This makes regime NOT identifiable from 3-step history
    regime_step = REGIMES[(step_in_traj // 10) % 2] if bank_type == "positive" else regime
    
    # High noise to reduce MI(R; cur_state)
    noise_rate = 0.40 if bank_type == "null" else 0.30
    
    # Channel 1: visible_text_hash (4-char hash)
    if bank_type == "null":
        base = f"vis:{latent_sig}"
    else:
        # Regime is PRIMARY signal: hash(regime) dominates
        base = f"vis:{regime_step}:{latent_sig}"
    if rng.random() < noise_rate:
        base = f"noise_{rng.integers(10000)}"
    channels['R_visible_text_hash'] = short_hash(base, 4)
    
    # Channel 2: visual
    if bank_type == "null":
        base = f"vis:{latent_sig}"
    else:
        base = f"vis:{regime_step}:{latent_sig}"
    if rng.random() < noise_rate:
        base = f"noise_{rng.integers(10000)}"
    channels['R_visual'] = short_hash(base, 4)
    
    # Channel 3: computed_style
    if bank_type == "null":
        base = f"css:{latent_sig}"
    else:
        base = f"css:{regime_step}:{latent_sig}"
    if rng.random() < noise_rate:
        base = f"noise_{rng.integers(10000)}"
    channels['R_computed_style'] = short_hash(base, 4)
    
    # Channel 4: AX
    ax_noise = 0.35 if bank_type == "null" else 0.25
    if bank_type == "null":
        base = f"ax:{latent_sig}"
    else:
        base = f"ax:{regime_step}:{latent_sig}"
    if rng.random() < ax_noise:
        base = f"noise_{rng.integers(10000)}"
    channels['R_AX'] = short_hash(base, 4)
    
    return channels

def build_bank(bank_type):
    transitions = []
    for traj_id in range(N_TRAJECTORIES):
        # Regime assignment: for null, fixed per traj; for positive, switches
        base_regime = REGIMES[traj_id % 2]
        cur_state = int(rng.integers(N_STATES))
        history = []
        
        for step in range(N_STEPS):
            url_before = generate_url(cur_state)
            action_idx = int(rng.integers(N_ACTIONS))
            action = ACTIONS[action_idx]
            
            C = build_history_context(url_before, history)
            
            if bank_type == "null":
                next_state = sample_next_state(NULL_KERNEL, cur_state, action_idx)
                regime_for_R = base_regime  # fixed per trajectory
            else:
                # Regime switches every 10 steps
                regime_for_R = REGIMES[(step // 10) % 2]
                kernel = POS_KERNEL_A if regime_for_R == 'A' else POS_KERNEL_B
                next_state = sample_next_state(kernel, cur_state, action_idx)
            
            title_after = f"State {next_state}"
            dom_cluster = next_state // 2
            S_next = hash_state(next_state, title_after, dom_cluster)
            
            R_channels = generate_R_channels(cur_state, action, base_regime, bank_type, step)
            
            transition = {
                'trajectory_id': traj_id,
                'step': step,
                'regime': regime_for_R,  # current regime at this step
                'base_regime': base_regime,  # trajectory base regime
                'cur_state': cur_state,
                'action': action,
                'action_idx': action_idx,
                'url_before': url_before,
                'C': C,
                'S_next': S_next,
                'R': R_channels,
                'latent_state_index': cur_state
            }
            transitions.append(transition)
            history.append(url_before)
            cur_state = next_state
    
    return transitions

def build_iid_null_bank(positive_transitions):
    S_next_list = [t['S_next'] for t in positive_transitions]
    S_next_values, counts = np.unique(S_next_list, return_counts=True)
    probs = counts / counts.sum()
    iid_transitions = []
    for t in positive_transitions:
        new_t = t.copy()
        new_t['S_next'] = rng.choice(S_next_values, p=probs)
        iid_transitions.append(new_t)
    return iid_transitions

# ──────────────────────────────────────────────────────────────
# Entropy Estimation
# ──────────────────────────────────────────────────────────────

def compute_dm_entropy(counts, K, alpha):
    N = counts.sum()
    alpha0 = K * alpha
    p_obs = (counts + alpha) / (N + alpha0)
    p_unobs = alpha / (N + alpha0)
    n_unobs = K - len(counts)
    H = -np.sum(p_obs * np.log2(p_obs))
    if n_unobs > 0:
        H -= n_unobs * p_unobs * np.log2(p_unobs)
    return H

def compute_conditional_entropy(transitions, strata_key_fn, K_per_stratum, alpha_per_stratum):
    strata = defaultdict(list)
    for t in transitions:
        strata[strata_key_fn(t)].append(t['S_next'])
    total_N = len(transitions)
    H_weighted = 0.0
    for stratum, S_next_list in strata.items():
        if len(S_next_list) < 2: continue
        if stratum not in K_per_stratum: continue
        counts = np.array([v for v in Counter(S_next_list).values()])
        K = K_per_stratum[stratum]
        alpha = alpha_per_stratum[stratum]
        H_stratum = compute_dm_entropy(counts, K, alpha)
        H_weighted += (len(S_next_list) / total_N) * H_stratum
    return H_weighted

# ──────────────────────────────────────────────────────────────
# G0 Analytic Null — CORRECTED FORMULA
# ──────────────────────────────────────────────────────────────

def compute_analytic_null(transitions, strata_key_fn, K_per_stratum, alpha_per_stratum):
    """
    E[PMI] under Dirichlet-Multinomial null.
    Formula: sum_c p(c) * [digamma(K*alpha) - digamma(N_c + K*alpha) + 
                            sum_i(digamma(n_i + alpha) - digamma(alpha))] / ln(2)
    This is the EXPECTED plug-in PMI under the null prior.
    For large N_c, this approaches 0. For small N_c, it's the bias.
    """
    strata = defaultdict(list)
    for t in transitions:
        strata[strata_key_fn(t)].append(t['S_next'])
    
    total_N = len(transitions)
    e_pmi_weighted = 0.0
    trigamma_weighted = 0.0
    used_N = 0
    
    for stratum, S_next_list in strata.items():
        N_c = len(S_next_list)
        if N_c < 2: continue
        if stratum not in K_per_stratum: continue
        counts = np.array([v for v in Counter(S_next_list).values()])
        K_c = K_per_stratum[stratum]
        alpha_c = alpha_per_stratum[stratum]
        alpha0 = K_c * alpha_c  # = 1.0
        
        # E[PMI] in nats
        e_pmi_nats = (digamma(alpha0) - digamma(N_c + alpha0) + 
                      np.sum(digamma(counts + alpha_c) - digamma(alpha_c)))
        e_pmi_bits = e_pmi_nats / np.log(2)
        
        # Variance of the plug-in estimator under DM prior
        trigamma_c = polygamma(1, alpha0) - polygamma(1, N_c + alpha0)
        
        weight = N_c / total_N
        e_pmi_weighted += weight * e_pmi_bits
        trigamma_weighted += weight * trigamma_c
        used_N += N_c
    
    analytic_mean = e_pmi_weighted
    analytic_std = np.sqrt(trigamma_weighted) / np.log(2) if used_N > 0 else 0.0
    return analytic_mean, analytic_std

# ──────────────────────────────────────────────────────────────
# Permutation Test
# ──────────────────────────────────────────────────────────────

def compute_cmi_for_R(transitions, R_channel, C_key_fn, R_key_fn, K_per_stratum, alpha_per_stratum):
    H_C = compute_conditional_entropy(transitions, C_key_fn, K_per_stratum, alpha_per_stratum)
    def CR_key_fn(t): return (C_key_fn(t), R_key_fn(t))
    H_CR = compute_conditional_entropy(transitions, CR_key_fn, K_per_stratum, alpha_per_stratum)
    cmi = H_C - H_CR
    return max(0.0, cmi), H_C, H_CR

def run_permutation_test(transitions, R_channel, C_key_fn, R_key_fn, 
                         K_per_stratum, alpha_per_stratum, n_perms=N_PERMUTATIONS):
    obs_cmi, H_C, H_CR = compute_cmi_for_R(transitions, R_channel, C_key_fn, R_key_fn, 
                                            K_per_stratum, alpha_per_stratum)
    perm_cmis = []
    rng_perm = np.random.default_rng(SEED + 10000)
    for _ in range(n_perms):
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
    n_exceed = np.sum(perm_cmis >= obs_cmi)
    p_raw = (1 + n_exceed) / (n_perms + 1)
    return {
        'obs_cmi': obs_cmi, 'perm_mean': perm_mean, 'perm_std': perm_std,
        'perm_cmis': perm_cmis, 'p_raw': p_raw, 'H_C': H_C, 'H_CR': H_CR
    }

def compute_mi(x_vals, y_vals):
    joint = Counter(zip(x_vals, y_vals))
    px = Counter(x_vals); py = Counter(y_vals)
    N = len(x_vals)
    mi = 0.0
    for (x, y), count in joint.items():
        p_xy = count / N; p_x = px[x] / N; p_y = py[y] / N
        if p_x > 0 and p_y > 0:
            mi += p_xy * np.log2(p_xy / (p_x * p_y))
    return mi

# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def run_experiment():
    print("=" * 70)
    print("EXP-PHYSICS-36279239922 — Calibration Experiment (v3)")
    print("=" * 70)
    
    print("\n[1/7] Building calibration banks...")
    null_bank = build_bank("null")
    positive_bank = build_bank("positive")
    iid_null_bank = build_iid_null_bank(positive_bank)
    print(f"  Null: {len(null_bank)}, Positive: {len(positive_bank)}, IID: {len(iid_null_bank)}")
    
    print("\n[2/7] TRAIN/TEST split...")
    traj_ids = list(range(N_TRAJECTORIES))
    rng_split = np.random.default_rng(SEED)
    permuted = rng_split.permutation(traj_ids)
    n_train = int(0.7 * N_TRAJECTORIES)
    train_traj = set(permuted[:n_train])
    test_traj = set(permuted[n_train:])
    
    def split_bank(bank):
        return ([t for t in bank if t['trajectory_id'] in train_traj],
                [t for t in bank if t['trajectory_id'] in test_traj])
    
    null_train, null_test = split_bank(null_bank)
    pos_train, pos_test = split_bank(positive_bank)
    iid_train, iid_test = split_bank(iid_null_bank)
    print(f"  Null train={len(null_train)} test={len(null_test)}")
    print(f"  Pos train={len(pos_train)} test={len(pos_test)}")
    
    print("\n[3/7] Building strata (TRAIN only)...")
    def C_key_fn(t): return t['C']
    def R_key_fn(t, ch): return t['R'][ch]
    R_channels = ['R_visible_text_hash', 'R_visual', 'R_computed_style', 'R_AX']
    
    def get_K_per_stratum(train_transitions):
        strata_S_next = defaultdict(set)
        for t in train_transitions:
            strata_S_next[C_key_fn(t)].add(t['S_next'])
        return {stratum: len(states) for stratum, states in strata_S_next.items()}
    
    K_null = get_K_per_stratum(null_train)
    K_pos = get_K_per_stratum(pos_train)
    K_iid = get_K_per_stratum(iid_train)
    alpha_null = {s: 1.0/K_null[s] for s in K_null}
    alpha_pos = {s: 1.0/K_pos[s] for s in K_pos}
    alpha_iid = {s: 1.0/K_iid[s] for s in K_iid}
    print(f"  Null strata: {len(K_null)}, Pos strata: {len(K_pos)}")
    
    print("\n[4/7] Computing metrics on TEST...")
    def compute_bank_metrics(name, test_trans, K_ps, alpha_ps):
        metrics = {}
        for ch in R_channels:
            print(f"  {name} - {ch}...")
            pr = run_permutation_test(test_trans, ch, C_key_fn, 
                                      lambda t, c=ch: R_key_fn(t, c), K_ps, alpha_ps)
            am, astd = compute_analytic_null(test_trans, C_key_fn, K_ps, alpha_ps)
            BC = pr['obs_cmi'] - pr['perm_mean']
            metrics[ch] = {
                'M_OBS_CMI_bits': pr['obs_cmi'], 'M_PERM_MEAN_bits': pr['perm_mean'],
                'M_PERM_STD_bits': pr['perm_std'], 'M_BC_PERM_bits': BC,
                'M_P_RAW': pr['p_raw'], 'M_ANALYTIC_MEAN_bits': am,
                'M_ANALYTIC_STD_bits': astd, 'M_CONS_bits': abs(pr['perm_mean'] - am),
                'M_H_Snext_given_C_bits': pr['H_C'], 'M_H_Snext_given_CR_bits': pr['H_CR'],
            }
        # Collinearity
        BC_vals = [metrics[ch]['M_BC_PERM_bits'] for ch in R_channels]
        if len(R_channels) > 1 and np.std(BC_vals) > 0:
            corr_matrix = np.corrcoef([BC_vals])
            eff = sum(1 for i in range(len(R_channels)) for j in range(i+1, len(R_channels)) 
                      if abs(corr_matrix[i, j]) < 0.95)
            effective_n_tests = max(1, eff + 1)
        else:
            effective_n_tests = 1
        for ch in R_channels:
            p_bonf = min(1.0, metrics[ch]['M_P_RAW'] * effective_n_tests)
            metrics[ch]['M_P_BONF'] = max(0.001, p_bonf)
            metrics[ch]['M_REL_SEP'] = (metrics[ch]['M_BC_PERM_bits'] / 
                max(metrics[ch]['M_ANALYTIC_STD_bits'], metrics[ch]['M_PERM_STD_bits'], 0.005))
        metrics['M_effective_n_tests'] = effective_n_tests
        metrics['M_K_observed'] = list(K_ps.values())
        metrics['M_N_strata'] = len(K_ps)
        metrics['M_N_transitions'] = len(test_trans)
        return metrics
    
    null_metrics = compute_bank_metrics("Null", null_test, K_null, alpha_null)
    pos_metrics = compute_bank_metrics("Positive", pos_test, K_pos, alpha_pos)
    iid_metrics = compute_bank_metrics("IID_Null", iid_test, K_iid, alpha_iid)
    
    print("\n[5/7] Identifiability (G3)...")
    MI_R_regime = {}
    MI_R_latent = {}
    for ch in R_channels:
        R_vals = [t['R'][ch] for t in pos_train]
        regime_vals = [t['regime'] for t in pos_train]  # step-level regime
        latent_vals = [t['latent_state_index'] for t in pos_train]
        MI_R_regime[ch] = compute_mi(R_vals, regime_vals)
        MI_R_latent[ch] = compute_mi(R_vals, latent_vals)
        print(f"  {ch}: MI(R;regime)={MI_R_regime[ch]:.4f}, MI(R;latent)={MI_R_latent[ch]:.4f}")
    
    print("\n[6/7] Gates...")
    BC_null_avg = np.mean([null_metrics[ch]['M_BC_PERM_bits'] for ch in R_channels])
    BC_pos_avg = np.mean([pos_metrics[ch]['M_BC_PERM_bits'] for ch in R_channels])
    gap = BC_pos_avg - BC_null_avg
    print(f"  BC_null={BC_null_avg:.6f}, BC_pos={BC_pos_avg:.6f}, gap={gap:.6f}")
    
    print("\n[7/7] Checking gates...")
    G0_pass = True; G0_details = {}
    for bn, bm in [("Null", null_metrics), ("Positive", pos_metrics)]:
        for ch in R_channels:
            cons = bm[ch]['M_CONS_bits']; am = bm[ch]['M_ANALYTIC_MEAN_bits']
            p = (cons < 0.03) and (abs(am) < 0.1)
            G0_details[f"{bn}_{ch}"] = {'consistency': float(cons), 'analytic_mean': float(am), 'pass': p}
            if not p: G0_pass = False
            print(f"  G0 {bn} {ch}: cons={cons:.4f}, analytic={am:.4f}, PASS={p}")
    
    G1_pass = True; G1_details = {}
    for ch in R_channels:
        p_bonf = null_metrics[ch]['M_P_BONF']; BC = null_metrics[ch]['M_BC_PERM_bits']
        p = (p_bonf > 0.10) and (abs(BC) < 0.05)
        G1_details[ch] = {'p_bonf': float(p_bonf), 'BC': float(BC), 'pass': p}
        if not p: G1_pass = False
        print(f"  G1 Null {ch}: p_bonf={p_bonf:.4f}, BC={BC:.4f}, PASS={p}")
    
    G2_pass = True; G2_details = {}
    for ch in R_channels:
        p_bonf = pos_metrics[ch]['M_P_BONF']; BC = pos_metrics[ch]['M_BC_PERM_bits']
        gap_ch = BC - null_metrics[ch]['M_BC_PERM_bits']
        p = (p_bonf < 0.01) and (BC > 0.05) and (gap_ch >= 0.05)
        G2_details[ch] = {'p_bonf': float(p_bonf), 'BC': float(BC), 'gap': float(gap_ch), 'pass': p}
        if not p: G2_pass = False
        print(f"  G2 Pos {ch}: p_bonf={p_bonf:.4f}, BC={BC:.4f}, gap={gap_ch:.4f}, PASS={p}")
    
    G3_pass = True; G3_details = {}
    for ch in R_channels:
        mi_r = MI_R_regime[ch]; mi_l = MI_R_latent[ch]
        p = (mi_r > 0.3) and (mi_l < 0.9)
        G3_details[ch] = {'MI_R_regime': float(mi_r), 'MI_R_latent': float(mi_l), 'pass': p}
        if not p: G3_pass = False
        print(f"  G3 {ch}: MI(R;regime)={mi_r:.4f}, MI(R;latent)={mi_l:.4f}, PASS={p}")
    
    all_pass = G0_pass and G1_pass and G2_pass and G3_pass
    print(f"\n{'='*70}")
    print(f"G0: {'PASS' if G0_pass else 'FAIL'}")
    print(f"G1: {'PASS' if G1_pass else 'FAIL'}")
    print(f"G2: {'PASS' if G2_pass else 'FAIL'}")
    print(f"G3: {'PASS' if G3_pass else 'FAIL'}")
    print(f"OVERALL: {'CALIBRATED' if all_pass else 'NOT_INSTRUMENTED'}")
    print(f"{'='*70}")
    
    return {
        'null_bank': null_bank, 'positive_bank': positive_bank, 'iid_null_bank': iid_null_bank,
        'null_metrics': null_metrics, 'pos_metrics': pos_metrics, 'iid_metrics': iid_metrics,
        'MI_R_regime': MI_R_regime, 'MI_R_latent': MI_R_latent,
        'G0_pass': G0_pass, 'G1_pass': G1_pass, 'G2_pass': G2_pass, 'G3_pass': G3_pass,
        'G0_details': G0_details, 'G1_details': G1_details, 'G2_details': G2_details, 'G3_details': G3_details,
        'all_gates_pass': all_pass, 'BC_null_avg': float(BC_null_avg), 'BC_pos_avg': float(BC_pos_avg), 'gap': float(gap),
        'R_channels': R_channels, 'train_traj': list(train_traj), 'test_traj': list(test_traj),
        'K_null': {str(k): int(v) for k, v in K_null.items()},
        'K_pos': {str(k): int(v) for k, v in K_pos.items()},
        'K_iid': {str(k): int(v) for k, v in K_iid.items()},
    }

def convert(obj):
    if isinstance(obj, (np.integer,)): return int(obj)
    if isinstance(obj, (np.floating,)): return float(obj)
    if isinstance(obj, np.ndarray): return obj.tolist()
    if isinstance(obj, dict): return {str(k): convert(v) for k, v in obj.items()}
    if isinstance(obj, list): return [convert(v) for v in obj]
    if isinstance(obj, tuple): return tuple(convert(v) for v in obj)
    return obj

if __name__ == "__main__":
    results = run_experiment()
    exp_dir = Path("/home/runner/work/Spider/Spider/research/experiments/EXP-PHYSICS-36279239922")
    for name, bank in [('raw_transitions_null_bank.json', results['null_bank']),
                       ('raw_transitions_positive_bank.json', results['positive_bank']),
                       ('raw_transitions_iid_null.json', results['iid_null_bank'])]:
        with open(exp_dir / name, 'w') as f:
            json.dump(convert(bank), f, indent=2)
    analytic_stats = {}
    for bn, bm in [('Null', results['null_metrics']), ('Positive', results['pos_metrics'])]:
        for ch in results['R_channels']:
            analytic_stats[f"{bn}_{ch}"] = {'analytic_mean': float(bm[ch]['M_ANALYTIC_MEAN_bits']),
                                             'analytic_std': float(bm[ch]['M_ANALYTIC_STD_bits'])}
    with open(exp_dir / 'analytic_null_stats.json', 'w') as f:
        json.dump(analytic_stats, f, indent=2)
    perm_summary = {}
    for bn, bm in [('Null', results['null_metrics']), ('Positive', results['pos_metrics'])]:
        for ch in results['R_channels']:
            perm_summary[f"{bn}_{ch}"] = {'perm_mean': float(bm[ch]['M_PERM_MEAN_bits']),
                                           'perm_std': float(bm[ch]['M_PERM_STD_bits']),
                                           'obs_cmi': float(bm[ch]['M_OBS_CMI_bits']),
                                           'p_raw': float(bm[ch]['M_P_RAW'])}
    with open(exp_dir / 'permutation_results.json', 'w') as f:
        json.dump(perm_summary, f, indent=2)
    with open(exp_dir / 'results.pkl', 'wb') as f:
        pickle.dump(results, f)
    print("\nAll artifacts saved.")