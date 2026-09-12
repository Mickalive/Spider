#!/usr/bin/env python3
"""
EXP-PHYSICS-34695057869 — Response-Side PMI Analysis

Computes Pointwise Mutual Information between actions and next-states,
using response-side signals (content-type, body digest, status) as state
representation.

Compares:
  - Response-side PMI (primary)
  - Request-side PMI (baseline from parent)
  - URL-only PMI (trivial baseline)
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

EXPERIMENT_ID = "EXP-PHYSICS-34695057869"
SEED = 42
N_PERMUTATIONS = 1000
SMOOTHING_ALPHA = 1.0
BONFERRONI_COMPARISONS = 3  # dashboard, multistep_form, wizard
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS

INPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'experiments', EXPERIMENT_ID)
OUTPUT_DIR = INPUT_DIR

# ─── State Discretization Functions ──────────────────────────────────────────

def hash_response_side(req: dict) -> str:
    """SHA-256(content_type + response_body_hash[:16] + status_code) per request.
    
    This captures response-side variation: different content types,
    response body digests, and status codes produce different hashes.
    """
    content_type = req.get('content_type', 'unknown')
    body_hash = req.get('response_body_hash', 'missing')
    status = req.get('status_code', 200)
    
    raw = f"{content_type}|{body_hash[:16]}|{status}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def hash_request_side(req: dict) -> str:
    """SHA-256(endpoint_path + method + status + request_body_fragment[:200]).
    
    Request-side state discretization from parent experiment.
    """
    endpoint = req.get('endpoint_url', '')
    method = req.get('http_method', 'GET')
    status = req.get('status_code', 200)
    body = req.get('request_body', '') or ''
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(endpoint)
        endpoint = parsed.path
    except:
        pass
    
    body_frag = body[:200] if body else ''
    raw = f"{endpoint}|{method}|{status}|{body_frag}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def network_requests_to_state(network_requests: list, hash_fn) -> str:
    """Convert list of network requests to a state representation.
    
    Sorted tuple of per-request hashes, then hashed to a single string.
    """
    if not network_requests:
        return hashlib.sha256(b'empty').hexdigest()[:16]
    
    request_hashes = sorted([hash_fn(r) for r in network_requests])
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
        
        p_s_next_given_sa = (count_sas_next + alpha) / (count_sa + alpha * distinct_next_s)
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
    
    For network-request states: chains transitions so that the network state
    AFTER transition i becomes the state BEFORE transition i+1.
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
    
    traj_groups = collections.defaultdict(list)
    for t in transitions:
        traj_groups[t['trajectory_id']].append(t)
    
    hash_fn = hash_response_side if state_type == 'response' else hash_request_side
    
    triples = []
    for tid, traj_trans in traj_groups.items():
        traj_trans.sort(key=lambda x: x.get('step', 0))
        prev_net_state = network_requests_to_state([], hash_fn)
        
        for t in traj_trans:
            curr_net_state = network_requests_to_state(t.get('network_requests', []), hash_fn)
            a = t['action'].get('target_href', '') or t['action'].get('type', '')
            triples.append((prev_net_state, a, curr_net_state))
            prev_net_state = curr_net_state
    
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
    """Split transitions temporally (80/20)."""
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


def compute_mutual_information(actions: list, response_hashes: list) -> float:
    """Compute mutual information I(action; response_body_hash)."""
    n = len(actions)
    if n == 0:
        return 0.0
    
    action_counts = collections.Counter(actions)
    response_counts = collections.Counter(response_hashes)
    joint_counts = collections.Counter(zip(actions, response_hashes))
    
    mi = 0.0
    for (a, r), joint_count in joint_counts.items():
        if joint_count > 0:
            p_joint = joint_count / n
            p_action = action_counts[a] / n
            p_response = response_counts[r] / n
            if p_action > 0 and p_response > 0:
                mi += p_joint * math.log2(p_joint / (p_action * p_response))
    
    return mi


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full response-side PMI experiment."""
    print("=" * 70)
    print(f"{EXPERIMENT_ID} — Response-Side PMI Analysis")
    print("=" * 70)
    
    random.seed(SEED)
    np.random.seed(SEED)
    
    # ── Step 1: Load Captured Data ──
    print("\n[1/10] Loading captured data...")
    captures_path = os.path.join(INPUT_DIR, 'raw_network_captures_response_side.json')
    with open(captures_path) as f:
        all_captures = json.load(f)
    
    for key, transitions in all_captures.items():
        print(f"  {key}: {len(transitions)} transitions")
    
    # ── Step 2: Classify Within-URL Transitions ──
    print("\n[2/10] Classifying within-URL transitions...")
    
    within_url = {}
    for key, transitions in all_captures.items():
        within = classify_within_url(transitions)
        within_url[key] = within
        print(f"  {key}: {len(within)}/{len(transitions)} within-URL")
    
    # ── Step 3: Quality Check — Response Body Capture Rate ──
    print("\n[3/10] Response body capture quality check...")
    
    quality_stats = {}
    for key, transitions in within_url.items():
        total_reqs = sum(len(t.get('network_requests', [])) for t in transitions)
        with_body = sum(
            1 for t in transitions
            for r in t.get('network_requests', [])
            if r.get('response_body_hash', 'missing') not in ('missing', 'unavailable')
        )
        capture_rate = with_body / total_reqs if total_reqs > 0 else 0
        quality_stats[key] = {
            'total_requests': total_reqs,
            'with_body': with_body,
            'capture_rate': capture_rate
        }
        status = 'PASS' if capture_rate >= 0.9 else 'WARN'
        print(f"  {key}: {with_body}/{total_reqs} ({capture_rate:.1%}) {status}")
    
    # ── Step 4: Synthetic Positive Control ──
    print("\n[4/10] Analyzing synthetic positive control...")
    
    synth_within = within_url['synthetic']
    synth_train, synth_test = temporal_split(synth_within, 0.8)
    print(f"  Synthetic: train={len(synth_train)}, test={len(synth_test)}")
    
    # Response-side PMI on test split
    synth_triples_resp_test = extract_triples(synth_test, 'response')
    synth_stats_resp_test = compute_pmi_stats(synth_triples_resp_test, SMOOTHING_ALPHA)
    
    # Request-side PMI on test split
    synth_triples_req_test = extract_triples(synth_test, 'request')
    synth_stats_req_test = compute_pmi_stats(synth_triples_req_test, SMOOTHING_ALPHA)
    
    # URL-only PMI on test split
    synth_triples_url_test = extract_triples(synth_test, 'url')
    synth_stats_url_test = compute_pmi_stats(synth_triples_url_test, SMOOTHING_ALPHA)
    
    # Permutation test for synthetic response-side
    synth_traj_groups_test = extract_trajectory_groups(synth_test)
    synth_triple_groups_resp_test = {}
    for tid, trans in synth_traj_groups_test.items():
        synth_triple_groups_resp_test[tid] = extract_triples(trans, 'response')
    
    synth_perm_resp = permutation_test(
        synth_triple_groups_resp_test, synth_stats_resp_test['mean_pmi'],
        N_PERMUTATIONS, SEED, SMOOTHING_ALPHA
    )
    
    print(f"  Response-side PMI (test): {synth_stats_resp_test['mean_pmi']:.6f} bits")
    print(f"  Request-side PMI (test): {synth_stats_req_test['mean_pmi']:.6f} bits")
    print(f"  URL-only PMI (test): {synth_stats_url_test['mean_pmi']:.6f} bits")
    print(f"  Permutation p: {synth_perm_resp['p_value']:.6f}")
    
    # ── Step 5: Null Control (shuffled labels on real SPA data) ──
    print("\n[5/10] Running null control (shuffled labels on real SPA data)...")
    
    # Combine real SPA data (dashboard, multistep_form, wizard) for null control
    realSPA_data = []
    for site_key in ['dashboard', 'multistep_form', 'wizard']:
        realSPA_data.extend(within_url.get(site_key, []))
    
    # Use response-side state for null control
    real_traj_groups = extract_trajectory_groups(realSPA_data)
    real_triple_groups_resp = {}
    for tid, trans in real_traj_groups.items():
        real_triple_groups_resp[tid] = extract_triples(trans, 'response')
    
    # Observed PMI on real data
    all_real_triples_resp = []
    for triples in real_triple_groups_resp.values():
        all_real_triples_resp.extend(triples)
    real_stats_resp = compute_pmi_stats(all_real_triples_resp, SMOOTHING_ALPHA)
    
    # Shuffled null
    rng_null = random.Random(SEED + 1000)
    shuffled_groups = shuffle_actions_within_trajectories(real_triple_groups_resp, rng_null)
    all_shuffled = []
    for triples in shuffled_groups.values():
        all_shuffled.extend(triples)
    null_stats = compute_pmi_stats(all_shuffled, SMOOTHING_ALPHA)
    
    # Permutation test for null
    null_perm = permutation_test(
        shuffled_groups, null_stats['mean_pmi'],
        N_PERMUTATIONS, SEED + 1000, SMOOTHING_ALPHA
    )
    
    print(f"  Real SPA response PMI: {real_stats_resp['mean_pmi']:.6f} bits")
    print(f"  Null (shuffled) PMI: {null_stats['mean_pmi']:.6f} bits")
    print(f"  Null permutation p: {null_perm['p_value']:.6f}")
    
    # ── Step 6: Genuine SPA Analysis ──
    print("\n[6/10] Analyzing genuine SPAs (response-side, request-side, URL-only)...")
    
    genuine_results = {}
    perm_tests = {}
    alpha_sensitivity_results = {}
    tautology_results = {}
    
    for site_key in ['dashboard', 'multistep_form', 'wizard']:
        transitions = within_url.get(site_key, [])
        if len(transitions) < 20:
            print(f"  {site_key}: insufficient within-URL transitions ({len(transitions)}), skipping")
            continue
        
        # Temporal split
        train, test = temporal_split(transitions, 0.8)
        n_test = len(test)
        
        if n_test < 30:
            print(f"\n  [{site_key}] EXCLUDED: n_test={n_test} < 30 (data sufficiency fails)")
            continue
        
        print(f"\n  [{site_key}] train={len(train)}, test={n_test}")
        
        # Response-side PMI (primary)
        triples_resp = extract_triples(test, 'response')
        stats_resp = compute_pmi_stats(triples_resp, SMOOTHING_ALPHA)
        
        # Request-side PMI (baseline)
        triples_req = extract_triples(test, 'request')
        stats_req = compute_pmi_stats(triples_req, SMOOTHING_ALPHA)
        
        # URL-only PMI (trivial baseline)
        triples_url = extract_triples(test, 'url')
        stats_url = compute_pmi_stats(triples_url, SMOOTHING_ALPHA)
        
        # Improvements over URL-only
        resp_improvement = stats_resp['mean_pmi'] - stats_url['mean_pmi']
        req_improvement = stats_req['mean_pmi'] - stats_url['mean_pmi']
        resp_vs_req = stats_resp['mean_pmi'] - stats_req['mean_pmi']
        
        print(f"    Response-side PMI: {stats_resp['mean_pmi']:.6f} bits ({stats_resp['unique_states']} states)")
        print(f"    Request-side PMI:  {stats_req['mean_pmi']:.6f} bits ({stats_req['unique_states']} states)")
        print(f"    URL-only PMI:      {stats_url['mean_pmi']:.6f} bits ({stats_url['unique_states']} states)")
        print(f"    Response vs URL:   {resp_improvement:+.6f} bits")
        print(f"    Request vs URL:    {req_improvement:+.6f} bits")
        print(f"    Response vs Request: {resp_vs_req:+.6f} bits")
        
        # Permutation test for response-side
        traj_groups = extract_trajectory_groups(test)
        triple_groups_resp = {}
        for tid, trans in traj_groups.items():
            triple_groups_resp[tid] = extract_triples(trans, 'response')
        
        perm_resp = permutation_test(
            triple_groups_resp, stats_resp['mean_pmi'],
            N_PERMUTATIONS, SEED, SMOOTHING_ALPHA
        )
        
        # Permutation test for request-side
        triple_groups_req = {}
        for tid, trans in traj_groups.items():
            triple_groups_req[tid] = extract_triples(trans, 'request')
        
        perm_req = permutation_test(
            triple_groups_req, stats_req['mean_pmi'],
            N_PERMUTATIONS, SEED + 2, SMOOTHING_ALPHA
        )
        
        # Bonferroni-corrected p-value for response-side
        perm_p_bonf = min(perm_resp['p_value'] * BONFERRONI_COMPARISONS, 1.0)
        
        print(f"    Response perm p: {perm_resp['p_value']:.6f} (bonf: {perm_p_bonf:.6f})")
        print(f"    Request perm p:  {perm_req['p_value']:.6f}")
        
        # Alpha sensitivity for response-side
        alpha_sens = alpha_sensitivity(triple_groups_resp)
        alpha_sensitivity_results[site_key] = alpha_sens
        
        # Dashboard tautology check: I(action_label; response_body_hash)
        if site_key == 'dashboard':
            action_labels = []
            response_hashes_list = []
            for t in test:
                action_labels.append(t['action'].get('target_href', '') or t['action'].get('type', ''))
                for r in t.get('network_requests', []):
                    response_hashes_list.append(r.get('response_body_hash', 'missing'))
            
            # Truncate to same length for MI computation
            min_len = min(len(action_labels), len(response_hashes_list))
            if min_len > 0:
                mi_action_response = compute_mutual_information(
                    action_labels[:min_len], response_hashes_list[:min_len]
                )
            else:
                mi_action_response = 0.0
            
            tautology_results[site_key] = {
                'mi_action_response_body': mi_action_response,
                'response_pmi': stats_resp['mean_pmi'],
                'fraction_tautological': mi_action_response / stats_resp['mean_pmi'] if stats_resp['mean_pmi'] > 0 else 0
            }
            print(f"    Dashboard tautology check: I(action; response_body) = {mi_action_response:.6f} bits")
            print(f"    Fraction of response PMI attributable to action→response: {tautology_results[site_key]['fraction_tautological']:.1%}")
        
        genuine_results[site_key] = {
            'response_pmi': stats_resp['mean_pmi'],
            'request_pmi': stats_req['mean_pmi'],
            'url_pmi': stats_url['mean_pmi'],
            'resp_vs_url_bits': resp_improvement,
            'req_vs_url_bits': req_improvement,
            'resp_vs_req_bits': resp_vs_req,
            'n_within_url': len(transitions),
            'n_test': n_test,
            'n_train': len(train),
            'unique_states_resp': stats_resp['unique_states'],
            'unique_states_req': stats_req['unique_states'],
            'unique_states_url': stats_url['unique_states'],
            'unique_sa_pairs_resp': stats_resp['unique_sa_pairs'],
            'unique_sa_pairs_req': stats_req['unique_sa_pairs'],
            'perm_p_response': perm_resp['p_value'],
            'perm_p_response_bonf': perm_p_bonf,
            'perm_p_request': perm_req['p_value'],
            'effect_d_response': perm_resp['effect_size_d'],
            'effect_d_request': perm_req['effect_size_d'],
        }
        
        perm_tests[f'{site_key}_response'] = perm_resp
        perm_tests[f'{site_key}_request'] = perm_req
    
    # ── Step 7: Decision Evaluation ──
    print("\n[7/10] Evaluating decision rules...")
    
    # Positive control
    positive_control_pmi = synth_stats_resp_test['mean_pmi']
    positive_control_perm_p = synth_perm_resp['p_value']
    positive_control_passes = positive_control_pmi >= 0.5 and positive_control_perm_p < 0.001
    
    # Null control
    null_control_perm_p = null_perm['p_value']
    null_control_passes = null_control_perm_p > 0.01
    
    # Primary condition: response-side PMI exceeds URL-only by >= 0.1 bits on >= 2/3 sites
    sites_passing = 0
    sites_total = len(genuine_results)
    primary_per_site = {}
    
    for site_key, site_res in genuine_results.items():
        passes = (site_res['resp_vs_url_bits'] >= 0.1 and
                  site_res['perm_p_response_bonf'] < ALPHA_BONFERRONI)
        primary_per_site[site_key] = {
            'resp_vs_url_bits': site_res['resp_vs_url_bits'],
            'perm_p_response_bonf': site_res['perm_p_response_bonf'],
            'passes': passes,
        }
        if passes:
            sites_passing += 1
    
    threshold = max(1, int(sites_total * 2 / 3)) if sites_total > 0 else 0
    primary_condition = sites_passing >= threshold
    
    # Data sufficiency
    data_sufficient = all(
        genuine_results[s]['n_test'] >= 30 for s in genuine_results
    ) if genuine_results else False
    
    # Decision
    if (positive_control_passes and null_control_passes and
        primary_condition and data_sufficient):
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
    print(f"  Positive control PMI (test): {positive_control_pmi:.6f} (>= 0.5 required)")
    print(f"  Positive control perm p:     {positive_control_perm_p:.6f} (< 0.001 required)")
    print(f"  Positive control passes:     {positive_control_passes}")
    print(f"  Null control perm p:         {null_control_perm_p:.6f} (> 0.01 required)")
    print(f"  Null control passes:         {null_control_passes}")
    print(f"  Primary condition:           {primary_condition} ({sites_passing}/{sites_total} sites >= {threshold})")
    print(f"  Data sufficient:             {data_sufficient}")
    print(f"  OUTCOME: {outcome}")
    print(f"  STATUS:  {status}")
    print(f"{'=' * 70}")
    
    # ── Step 8: Per-Site Summary ──
    print("\n[8/10] Per-site summary...")
    for site_key, site_res in genuine_results.items():
        print(f"\n  [{site_key}]")
        print(f"    Response-side PMI: {site_res['response_pmi']:.6f} bits")
        print(f"    Request-side PMI:  {site_res['request_pmi']:.6f} bits")
        print(f"    URL-only PMI:      {site_res['url_pmi']:.6f} bits")
        print(f"    Response > URL by: {site_res['resp_vs_url_bits']:+.6f} bits")
        print(f"    Response > Request by: {site_res['resp_vs_req_bits']:+.6f} bits")
        print(f"    Primary passes: {primary_per_site[site_key]['passes']}")
    
    # ── Step 9: Build Results ──
    print("\n[9/10] Building results structure...")
    
    results = {
        "experiment_id": EXPERIMENT_ID,
        "lane": "physics",
        "status": status,
        "outcome": outcome,
        "metrics": {
            "positive_control_pmi_test": positive_control_pmi,
            "positive_control_perm_p": positive_control_perm_p,
            "positive_control_passes": positive_control_passes,
            "null_control_perm_p": null_control_perm_p,
            "null_control_passes": null_control_passes,
            "primary_condition": primary_condition,
            "sites_passing_primary": sites_passing,
            "sites_total": sites_total,
            "primary_threshold": threshold,
            "data_sufficient": data_sufficient,
            "n_permutations": N_PERMUTATIONS,
            "smoothing_alpha": SMOOTHING_ALPHA,
            "bonferroni_alpha": ALPHA_BONFERRONI,
            "bonferroni_comparisons": BONFERRONI_COMPARISONS,
            "per_site_results": primary_per_site,
            "site_results": genuine_results,
            "alpha_sensitivity": alpha_sensitivity_results,
            "tautology_check": tautology_results,
            "quality_stats": quality_stats,
        },
        "controls": {
            "positive_control_synthetic_response_side": {
                "description": "Synthetic SPA with deterministic response-side variation (8 states, 4 actions, state-specific response bodies)",
                "expected": "Response-side PMI >= 0.5 bits, permutation p < 0.001 on 80/20 test split",
                "observed_pmi": positive_control_pmi,
                "observed_perm_p": positive_control_perm_p,
                "result": "PASS" if positive_control_passes else "FAIL",
            },
            "null_control_shuffled_real_labels": {
                "description": "Shuffled action labels on real SPA response-side data (dashboard, multistep_form, wizard)",
                "expected": "Permutation p > 0.01",
                "observed_perm_p": null_control_perm_p,
                "result": "PASS" if null_control_passes else "FAIL",
            },
            "data_sufficiency": {
                "description": "Each site has n_test >= 30 on held-out test set after 80/20 temporal split",
                "expected": "n_test >= 30 per site",
                "per_site_n_test": {s: genuine_results[s]['n_test'] for s in genuine_results},
                "result": "PASS" if data_sufficient else "FAIL",
            },
        },
        "permutation_tests": perm_tests,
    }
    
    return results


if __name__ == "__main__":
    os.environ["PYTHONHASHSEED"] = "0"
    results = run_experiment()
    
    out_path = os.path.join(OUTPUT_DIR, 'pmi_results_response_side.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {out_path}")
