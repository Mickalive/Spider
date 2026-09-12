#!/usr/bin/env python3
"""
EXP-PHYSICS-34674671762 — Network-Request PMI Analysis

Computes Pointwise Mutual Information between actions and next-states,
using network-request signatures as state representation.

Compares network-request PMI vs URL-only PMI baseline.
"""

import json
import hashlib
import math
import random
import collections
import os
import sys
from typing import Any, Dict, List, Tuple, Optional

import numpy as np

# ─── Configuration ───────────────────────────────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34674671762"
SEED = 42
N_PERMUTATIONS = 1000
SMOOTHING_ALPHA = 1.0
BONFERRONI_COMPARISONS = 3  # multistep_form, dashboard, wizard (3 genuine sites)
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS

INPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'experiments', EXPERIMENT_ID)
OUTPUT_DIR = INPUT_DIR

# ─── Network-Request State Discretization ────────────────────────────────────

def hash_request(req: dict) -> str:
    """SHA-256(endpoint_url_path + HTTP_method + status_code + request_body_fragment).
    
    Includes the endpoint path (not origin), method, status, and a fragment
    from the request body/payload to capture state-dependent variation.
    This ensures that identical endpoints with different payloads produce
    different hashes.
    """
    endpoint = req.get('endpoint_url', '')
    method = req.get('http_method', 'GET')
    status = req.get('status_code', 200)
    body = req.get('request_body', '') or req.get('body', '')
    
    # Normalize endpoint: extract path only (no origin), strip query
    try:
        from urllib.parse import urlparse
        parsed = urlparse(endpoint)
        endpoint = parsed.path
    except:
        pass
    
    # Include body fragment (first 200 chars) to capture state variation
    body_frag = body[:200] if body else ''
    
    raw = f"{endpoint}|{method}|{status}|{body_frag}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def network_requests_to_state(network_requests: list) -> str:
    """Convert list of network requests to a state representation.
    
    Sorted tuple of per-request hashes, then hashed to a single string.
    """
    if not network_requests:
        return hashlib.sha256(b'empty').hexdigest()[:16]
    
    request_hashes = sorted([hash_request(r) for r in network_requests])
    combined = '|'.join(request_hashes)
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def url_to_state(url: str) -> str:
    """URL-only state: normalized URL path (no query, no hash)."""
    if not url:
        return 'unknown'
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path = parsed.path
        if path.endswith('/') and len(path) > 1:
            path = path[:-1]
        return path or '/'
    except:
        return url


# ─── PMI Computation ─────────────────────────────────────────────────────────

def compute_pmi_stats(triples: list, alpha: float = 1.0) -> dict:
    """Compute PMI statistics for (state, action, next_state) triples.
    
    PMI(s, a, s') = log2[ P(s' | s, a) / P(s' | s) ]
    """
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "pmi_values": [], "N": 0, "unique_states": 0, "unique_sa_pairs": 0}
    
    state_counts = collections.Counter()
    state_action_counts = collections.Counter()
    state_next_counts = collections.Counter()
    triple_counts = collections.Counter()
    
    for s, a, s_next in triples:
        state_counts[s] += 1
        state_action_counts[(s, a)] += 1
        state_next_counts[(s, s_next)] += 1
        triple_counts[(s, a, s_next)] += 1
    
    pmi_values = []
    
    for s, a, s_next in triples:
        count_s = state_counts[s]
        count_sa = state_action_counts[(s, a)]
        count_ss_next = state_next_counts[(s, s_next)]
        count_sas_next = triple_counts[(s, a, s_next)]
        
        distinct_next_s = sum(1 for (si, sni) in state_next_counts if si == s)
        
        # P(s' | s, a) with Laplace smoothing
        p_s_next_given_sa = (count_sas_next + alpha) / (count_sa + alpha * distinct_next_s)
        # P(s' | s) with Laplace smoothing
        p_s_next_given_s = (count_ss_next + alpha) / (count_s + alpha * distinct_next_s)
        
        if p_s_next_given_s > 0 and p_s_next_given_sa > 0:
            pmi = math.log2(p_s_next_given_sa / p_s_next_given_s)
        else:
            pmi = 0.0
        
        pmi_values.append(pmi)
    
    mean_pmi = sum(pmi_values) / len(pmi_values) if pmi_values else 0.0
    
    return {
        "mean_pmi": mean_pmi,
        "pmi_values": pmi_values,
        "N": N,
        "unique_states": len(state_counts),
        "unique_sa_pairs": len(state_action_counts),
    }


def extract_triples(transitions: list, state_type: str) -> list:
    """Extract (state, action, next_state) triples from transitions.
    
    For network-request state: chains transitions so that the network state
    AFTER transition i becomes the state BEFORE transition i+1.
    For URL-only state: uses state_before.url and state_after.url from each transition.
    """
    if state_type == 'url':
        triples = []
        for t in transitions:
            s = url_to_state(t['state_before']['url'])
            s_next = url_to_state(t['state_after']['url'])
            a = t['action'].get('target_href', '') or t['action'].get('type', '')
            triples.append((s, a, s_next))
        return triples
    
    # Network-request state: chain transitions
    if not transitions:
        return []
    
    # Group by trajectory
    traj_groups = collections.defaultdict(list)
    for t in transitions:
        traj_groups[t['trajectory_id']].append(t)
    
    triples = []
    for tid, traj_trans in traj_groups.items():
        # Sort by step if available
        traj_trans.sort(key=lambda x: x.get('step', 0))
        
        # Initial state: empty network requests (before any action)
        prev_net_state = network_requests_to_state([])
        
        for t in traj_trans:
            curr_net_state = network_requests_to_state(t.get('network_requests', []))
            a = t['action'].get('target_href', '') or t['action'].get('type', '')
            triples.append((prev_net_state, a, curr_net_state))
            prev_net_state = curr_net_state  # Chain: current becomes previous for next
    
    return triples


def extract_trajectory_groups(transitions: list) -> dict:
    """Group transitions by trajectory_id."""
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t['trajectory_id']].append(t)
    return dict(groups)


def shuffle_actions_within_trajectories(triple_groups: dict, rng: random.Random) -> dict:
    """Shuffle action labels within trajectories (null control)."""
    shuffled_groups = {}
    for tid, triples in triple_groups.items():
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
        shuffled_actions = actions[:]
        rng.shuffle(shuffled_actions)
        shuffled_groups[tid] = [(states[i], shuffled_actions[i], nexts[i]) for i in range(len(triples))]
    return shuffled_groups


def permutation_test(triple_groups: dict, observed_mean_pmi: float, 
                     n_permutations: int, seed: int, alpha: float = 1.0) -> dict:
    """Permutation test: shuffle actions within trajectories, recompute mean PMI."""
    rng = random.Random(seed)
    all_triples = []
    for triples in triple_groups.values():
        all_triples.extend(triples)
    
    shuffled_means = []
    for _ in range(n_permutations):
        shuffled_groups = shuffle_actions_within_trajectories(triple_groups, rng)
        all_shuffled = []
        for triples in shuffled_groups.values():
            all_shuffled.extend(triples)
        stats = compute_pmi_stats(all_shuffled, alpha)
        shuffled_means.append(stats["mean_pmi"])
    
    count_ge = sum(1 for m in shuffled_means if m >= observed_mean_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)
    
    null_mean = float(np.mean(shuffled_means)) if shuffled_means else 0.0
    null_std = float(np.std(shuffled_means)) if shuffled_means else 0.0
    effect_d = (observed_mean_pmi - null_mean) / null_std if null_std > 0 else 0.0
    
    return {
        "p_value": p_value,
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
    }


def temporal_split(transitions: list, train_ratio: float = 0.8) -> Tuple[list, list]:
    """Split transitions temporally."""
    n = len(transitions)
    split_idx = int(n * train_ratio)
    return transitions[:split_idx], transitions[split_idx:]


def classify_within_url(transitions: list) -> list:
    """Filter to within-URL transitions."""
    result = []
    for t in transitions:
        url_before = url_to_state(t['state_before']['url'])
        url_after = url_to_state(t['state_after']['url'])
        if url_before == url_after:
            result.append(t)
    return result


def alpha_sensitivity(triple_groups: dict, alphas: list = [0.0, 0.5, 1.0, 2.0]) -> dict:
    """Compute PMI at different smoothing alpha values."""
    results = {}
    all_triples = []
    for triples in triple_groups.values():
        all_triples.extend(triples)
    
    for alpha in alphas:
        stats = compute_pmi_stats(all_triples, alpha)
        results[f'alpha_{alpha}'] = stats['mean_pmi']
    
    return results


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full network-request PMI experiment."""
    print("=" * 70)
    print(f"{EXPERIMENT_ID} — Network-Request PMI Analysis")
    print("=" * 70)
    
    random.seed(SEED)
    np.random.seed(SEED)
    
    # ── Step 1: Load Captured Data ──
    print("\n[1/7] Loading captured data...")
    captures_path = os.path.join(INPUT_DIR, 'raw_network_captures.json')
    with open(captures_path) as f:
        all_captures = json.load(f)
    
    for key, transitions in all_captures.items():
        print(f"  {key}: {len(transitions)} transitions")
    
    # ── Step 2: Classify Within-URL Transitions ──
    print("\n[2/7] Classifying within-URL transitions...")
    
    within_url = {}
    for key, transitions in all_captures.items():
        within = classify_within_url(transitions)
        within_url[key] = within
        print(f"  {key}: {len(within)}/{len(transitions)} within-URL")
    
    # ── Step 3: Synthetic Positive Control ──
    print("\n[3/7] Analyzing synthetic positive control...")
    
    synth_within = within_url['synthetic']
    synth_triples_net = extract_triples(synth_within, 'network')
    synth_triples_url = extract_triples(synth_within, 'url')
    
    synth_stats_net = compute_pmi_stats(synth_triples_net, SMOOTHING_ALPHA)
    synth_stats_url = compute_pmi_stats(synth_triples_url, SMOOTHING_ALPHA)
    
    # Permutation test for synthetic
    synth_traj_groups = extract_trajectory_groups(synth_within)
    synth_triple_groups_net = {}
    for tid, trans in synth_traj_groups.items():
        synth_triple_groups_net[tid] = extract_triples(trans, 'network')
    
    synth_perm = permutation_test(
        synth_triple_groups_net, synth_stats_net['mean_pmi'],
        N_PERMUTATIONS, SEED, SMOOTHING_ALPHA
    )
    
    print(f"  Network PMI: {synth_stats_net['mean_pmi']:.6f} bits")
    print(f"  URL PMI: {synth_stats_url['mean_pmi']:.6f} bits")
    print(f"  Permutation p: {synth_perm['p_value']:.6f}")
    
    # ── Step 4: Null Control ──
    print("\n[4/7] Running null control (shuffled labels)...")
    
    # Use synthetic data with shuffled actions as null control
    synth_all_triples = []
    for triples in synth_triple_groups_net.values():
        synth_all_triples.extend(triples)
    
    # Create shuffled version
    rng_null = random.Random(SEED + 1000)
    null_triples = list(synth_all_triples)
    null_actions = [t[1] for t in null_triples]
    rng_null.shuffle(null_actions)
    null_triples_shuffled = [(null_triples[i][0], null_actions[i], null_triples[i][2]) 
                             for i in range(len(null_triples))]
    
    null_stats = compute_pmi_stats(null_triples_shuffled, SMOOTHING_ALPHA)
    
    # Permutation test for null
    null_traj_groups = {}
    traj_ids = list(synth_triple_groups_net.keys())
    for i, tid in enumerate(traj_ids):
        triples = synth_triple_groups_net[tid]
        start = sum(len(synth_triple_groups_net[traj_ids[j]]) for j in range(i))
        end = start + len(triples)
        null_traj_groups[tid] = null_triples_shuffled[start:end]
    
    null_perm = permutation_test(
        null_traj_groups, null_stats['mean_pmi'],
        N_PERMUTATIONS, SEED + 1000, SMOOTHING_ALPHA
    )
    
    print(f"  Null PMI: {null_stats['mean_pmi']:.6f} bits")
    print(f"  Null permutation p: {null_perm['p_value']:.6f}")
    
    # ── Step 5: Genuine SPA Analysis ──
    print("\n[5/7] Analyzing genuine SPAs...")
    
    genuine_results = {}
    perm_tests = {}
    alpha_sensitivity_results = {}
    
    for site_key in ['multistep_form', 'dashboard', 'wizard']:
        transitions = within_url.get(site_key, [])
        if len(transitions) < 20:
            print(f"  {site_key}: insufficient within-URL transitions ({len(transitions)}), skipping")
            continue
        
        # Temporal split
        train, test = temporal_split(transitions, 0.8)
        if len(test) < 10:
            test = transitions
            train = []
        
        print(f"\n  [{site_key}] train={len(train)}, test={len(test)}")
        
        # Compute PMI for network-request state
        triples_net = extract_triples(test, 'network')
        stats_net = compute_pmi_stats(triples_net, SMOOTHING_ALPHA)
        
        # Compute PMI for URL-only state
        triples_url = extract_triples(test, 'url')
        stats_url = compute_pmi_stats(triples_url, SMOOTHING_ALPHA)
        
        improvement = stats_net['mean_pmi'] - stats_url['mean_pmi']
        
        print(f"    Network PMI: {stats_net['mean_pmi']:.6f} bits ({stats_net['unique_states']} states, {stats_net['unique_sa_pairs']} SA pairs)")
        print(f"    URL PMI: {stats_url['mean_pmi']:.6f} bits ({stats_url['unique_states']} states)")
        print(f"    Improvement: {improvement:+.6f} bits")
        
        # Permutation test for network-request state
        traj_groups = extract_trajectory_groups(test)
        triple_groups_net = {}
        for tid, trans in traj_groups.items():
            triple_groups_net[tid] = extract_triples(trans, 'network')
        
        perm_net = permutation_test(
            triple_groups_net, stats_net['mean_pmi'],
            N_PERMUTATIONS, SEED, SMOOTHING_ALPHA
        )
        
        # Permutation test for URL-only state
        triple_groups_url = {}
        for tid, trans in traj_groups.items():
            triple_groups_url[tid] = extract_triples(trans, 'url')
        
        perm_url = permutation_test(
            triple_groups_url, stats_url['mean_pmi'],
            N_PERMUTATIONS, SEED + 1, SMOOTHING_ALPHA
        )
        
        # Bonferroni-corrected p-value
        perm_p_bonf = min(perm_net['p_value'] * BONFERRONI_COMPARISONS, 1.0)
        
        print(f"    Network perm p: {perm_net['p_value']:.6f} (bonf: {perm_p_bonf:.6f})")
        print(f"    URL perm p: {perm_url['p_value']:.6f}")
        
        # Alpha sensitivity
        alpha_sens = alpha_sensitivity(triple_groups_net)
        alpha_sensitivity_results[site_key] = alpha_sens
        
        genuine_results[site_key] = {
            'network_pmi': stats_net['mean_pmi'],
            'url_pmi': stats_url['mean_pmi'],
            'improvement_bits': improvement,
            'n_within_url': len(transitions),
            'n_test': len(test),
            'n_train': len(train),
            'unique_states_net': stats_net['unique_states'],
            'unique_states_url': stats_url['unique_states'],
            'unique_sa_pairs_net': stats_net['unique_sa_pairs'],
            'unique_sa_pairs_url': stats_url['unique_sa_pairs'],
            'perm_p_network': perm_net['p_value'],
            'perm_p_network_bonf': perm_p_bonf,
            'perm_p_url': perm_url['p_value'],
            'effect_d_network': perm_net['effect_size_d'],
            'effect_d_url': perm_url['effect_size_d'],
        }
        
        perm_tests[f'{site_key}_network'] = perm_net
        perm_tests[f'{site_key}_url'] = perm_url
    
    # ── Step 6: Decision Evaluation ──
    print("\n[6/7] Evaluating decision rules...")
    
    # Positive control
    positive_control_pmi = synth_stats_net['mean_pmi']
    positive_control_perm_p = synth_perm['p_value']
    positive_control_passes = positive_control_pmi >= 0.5 and positive_control_perm_p < 0.001
    
    # Null control
    null_control_pmi = null_stats['mean_pmi']
    null_control_perm_p = null_perm['p_value']
    null_control_passes = null_control_perm_p > 0.01
    
    # Primary condition: network-request PMI exceeds URL-only by >= 0.1 bits
    sites_passing = 0
    sites_total = len(genuine_results)
    primary_per_site = {}
    
    for site_key, site_res in genuine_results.items():
        passes = (site_res['improvement_bits'] >= 0.1 and 
                  site_res['perm_p_network_bonf'] < 0.05)
        primary_per_site[site_key] = {
            'improvement_bits': site_res['improvement_bits'],
            'perm_p_network_bonf': site_res['perm_p_network_bonf'],
            'passes': passes,
        }
        if passes:
            sites_passing += 1
    
    primary_condition = sites_passing >= max(1, int(sites_total * 2 / 3)) if sites_total > 0 else False
    
    # Data sufficiency
    data_sufficient = all(
        genuine_results[s]['n_within_url'] >= 30 for s in genuine_results
    ) if genuine_results else False
    
    # Decision
    if positive_control_passes and null_control_passes and primary_condition and data_sufficient:
        outcome = 'SUPPORTS'
        status = 'COMPLETE'
    elif sites_total > 0 and not primary_condition:
        outcome = 'FALSIFIES'
        status = 'COMPLETE'
    elif not positive_control_passes or not null_control_passes:
        outcome = 'NOT_APPLICABLE'
        status = 'MEASUREMENT_INVALID'
    else:
        outcome = 'INCONCLUSIVE'
        status = 'COMPLETE'
    
    print(f"\n{'=' * 70}")
    print(f"DECISION SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Positive control PMI: {positive_control_pmi:.6f} (>= 0.5 required)")
    print(f"  Positive control perm p: {positive_control_perm_p:.6f} (< 0.001 required)")
    print(f"  Positive control passes: {positive_control_passes}")
    print(f"  Null control PMI: {null_control_pmi:.6f}")
    print(f"  Null control perm p: {null_control_perm_p:.6f} (> 0.01 required)")
    print(f"  Null control passes: {null_control_passes}")
    print(f"  Primary condition: {primary_condition} ({sites_passing}/{sites_total} sites)")
    print(f"  Data sufficient: {data_sufficient}")
    print(f"  OUTCOME: {outcome}")
    print(f"  STATUS: {status}")
    print(f"{'=' * 70}")
    
    # ── Build Results ──
    results = {
        "experiment_id": EXPERIMENT_ID,
        "lane": "physics",
        "status": status,
        "outcome": outcome,
        "metrics": {
            "positive_control_pmi": positive_control_pmi,
            "positive_control_perm_p": positive_control_perm_p,
            "positive_control_passes": positive_control_passes,
            "null_control_pmi": null_control_pmi,
            "null_control_perm_p": null_control_perm_p,
            "null_control_passes": null_control_passes,
            "primary_condition": primary_condition,
            "sites_passing_primary": sites_passing,
            "sites_total": sites_total,
            "data_sufficient": data_sufficient,
            "n_permutations": N_PERMUTATIONS,
            "smoothing_alpha": SMOOTHING_ALPHA,
            "bonferroni_alpha": ALPHA_BONFERRONI,
            "bonferroni_comparisons": BONFERRONI_COMPARISONS,
            "per_site_results": primary_per_site,
            "site_results": genuine_results,
            "alpha_sensitivity": alpha_sensitivity_results,
            "synthetic_url_pmi": synth_stats_url['mean_pmi'],
            "synthetic_network_pmi": synth_stats_net['mean_pmi'],
        },
        "controls": {
            "positive_control_synthetic_spa": {
                "description": "Synthetic SPA with deterministic network-request evolution (8 states, 4 actions)",
                "expected": "Network-request PMI >= 0.5 bits, permutation p < 0.001",
                "observed_pmi": positive_control_pmi,
                "observed_perm_p": positive_control_perm_p,
                "result": "PASS" if positive_control_passes else "FAIL",
            },
            "null_control_shuffled_labels": {
                "description": "Synthetic SPA data with shuffled action labels",
                "expected": "Permutation p > 0.01",
                "observed_pmi": null_control_pmi,
                "observed_perm_p": null_control_perm_p,
                "result": "PASS" if null_control_passes else "FAIL",
            },
        },
        "permutation_tests": perm_tests,
    }
    
    return results


if __name__ == "__main__":
    os.environ["PYTHONHASHSEED"] = "0"
    results = run_experiment()
    
    out_path = os.path.join(OUTPUT_DIR, 'pmi_results.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {out_path}")
