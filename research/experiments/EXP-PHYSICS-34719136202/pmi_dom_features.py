#!/usr/bin/env python3
"""
EXP-PHYSICS-34719136202 — DOM Feature PMI Analysis

Computes Pointwise Mutual Information between actions and next-states,
using DOM-based state representation (rendered page structural features).

Tests whether DOM structural features provide predictive PMI on locally-hosted
SPAs where network-request signals fail (multistep_form, wizard) or are
tautological (dashboard).

Frozen inputs: request.json, spec.json, prereg.md, freeze.json
All computation deterministic (seed=42, PYTHONHASHSEED=0).
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

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34719136202"
SEED = 42
N_PERMUTATIONS = 1000
SMOOTHING_ALPHA = 1.0
BONFERRONI_COMPARISONS = 3  # dashboard, multistep_form, wizard
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS
N_BINS = 5  # quantile bins per numeric feature

INPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = INPUT_DIR


# ─── State Discretization Functions ──────────────────────────────────────────

def fit_quantile_bins(values: list, n_bins: int = 5) -> list:
    """Fit quantile bin edges from training data only."""
    if not values:
        return [0, 1]
    sorted_vals = sorted(set(values))
    if len(sorted_vals) <= n_bins:
        # Use unique values as edges
        edges = list(sorted_vals) + [sorted_vals[-1] + 1]
        return edges
    n = len(sorted_vals)
    edges = []
    for i in range(n_bins + 1):
        idx = min(int(i * (n - 1) / n_bins), n - 1)
        edges.append(sorted_vals[idx])
    return sorted(set(edges))


def discretize_value(value, edges: list) -> int:
    """Discretize a value into bin index."""
    for i in range(len(edges) - 1):
        if value < edges[i + 1]:
            return i
    return len(edges) - 2


def dom_features_to_state(dom_features: dict, bin_edges: dict) -> tuple:
    """Convert DOM features to a discretized state representation.
    
    Numeric features: element_count, tree_depth, interactive_density,
    form_count, input_count, button_count — quantile-binned.
    Categorical features: visible_text_hash, attribute_pattern_hash — exact match.
    """
    ec = discretize_value(dom_features.get('element_count', 0), bin_edges.get('ec', [0, 1]))
    td = discretize_value(dom_features.get('tree_depth', 0), bin_edges.get('td', [0, 1]))
    id_ = discretize_value(dom_features.get('interactive_density', 0), bin_edges.get('id', [0, 1]))
    fc = discretize_value(dom_features.get('form_count', 0), bin_edges.get('fc', [0, 1]))
    ic = discretize_value(dom_features.get('input_count', 0), bin_edges.get('ic', [0, 1]))
    bc = discretize_value(dom_features.get('button_count', 0), bin_edges.get('bc', [0, 1]))
    vth = dom_features.get('visible_text_hash', 'missing')
    aph = dom_features.get('attribute_pattern_hash', 'missing')
    
    return (ec, td, id_, fc, ic, bc, vth, aph)


def url_to_state(url: str) -> str:
    """URL-only state: normalized URL path (no query, no hash fragment)."""
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


def fit_bin_edges(transitions: list) -> dict:
    """Fit quantile bin edges from training data (numeric features only)."""
    element_counts = []
    tree_depths = []
    interactive_densities = []
    form_counts = []
    input_counts = []
    button_counts = []
    
    for t in transitions:
        df = t.get('state_before', {}).get('dom_features', {})
        element_counts.append(df.get('element_count', 0))
        tree_depths.append(df.get('tree_depth', 0))
        interactive_densities.append(df.get('interactive_density', 0))
        form_counts.append(df.get('form_count', 0))
        input_counts.append(df.get('input_count', 0))
        button_counts.append(df.get('button_count', 0))
    
    return {
        'ec': fit_quantile_bins(element_counts, N_BINS),
        'td': fit_quantile_bins(tree_depths, N_BINS),
        'id': fit_quantile_bins(interactive_densities, N_BINS),
        'fc': fit_quantile_bins(form_counts, N_BINS),
        'ic': fit_quantile_bins(input_counts, N_BINS),
        'bc': fit_quantile_bins(button_counts, N_BINS),
    }


# ─── PMI Computation ─────────────────────────────────────────────────────────

def compute_pmi_stats(triples: list, alpha: float = 1.0) -> dict:
    """Compute PMI statistics for (state, action, next_state) triples.
    
    PMI(s, a, s') = log2[ P(s' | s, a) / P(s' | s) ]
    """
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "pmi_values": [], "N": 0,
                "unique_states": 0, "unique_sa_pairs": 0}
    
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


def extract_triples(transitions: list, state_type: str, bin_edges: dict = None) -> list:
    """Extract (state, action, next_state) triples from transitions.
    
    For DOM-based states: discretize features using bin edges fit on train.
    For URL-only states: normalize URL path.
    """
    triples = []
    
    if state_type == 'url':
        for t in transitions:
            s = url_to_state(t['state_before']['url'])
            s_next = url_to_state(t['state_after']['url'])
            a = t['action'].get('target_href', '') or t['action'].get('type', '')
            triples.append((s, a, s_next))
        return triples
    
    elif state_type == 'dom':
        # Chain transitions: state AFTER transition i is state BEFORE transition i+1
        traj_groups = collections.defaultdict(list)
        for t in transitions:
            traj_groups[t['trajectory_id']].append(t)
        
        triples = []
        for tid, traj_trans in traj_groups.items():
            traj_trans.sort(key=lambda x: x.get('step', 0))
            prev_dom = traj_trans[0].get('state_before', {}).get('dom_features', {})
            prev_state = dom_features_to_state(prev_dom, bin_edges)
            
            for t in traj_trans:
                curr_dom = t.get('state_after', {}).get('dom_features', {})
                curr_state = dom_features_to_state(curr_dom, bin_edges)
                a = t['action'].get('target_href', '') or t['action'].get('type', '')
                triples.append((prev_state, a, curr_state))
                prev_state = curr_state
        
        return triples
    
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


def compute_mutual_information(x_list: list, y_list: list) -> float:
    """Compute mutual information I(X; Y)."""
    n = len(x_list)
    if n == 0:
        return 0.0
    
    x_counts = collections.Counter(x_list)
    y_counts = collections.Counter(y_list)
    joint_counts = collections.Counter(zip(x_list, y_list))
    
    mi = 0.0
    for (x, y), joint_count in joint_counts.items():
        if joint_count > 0:
            p_joint = joint_count / n
            p_x = x_counts[x] / n
            p_y = y_counts[y] / n
            if p_x > 0 and p_y > 0:
                mi += p_joint * math.log2(p_joint / (p_x * p_y))
    
    return mi


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full DOM feature PMI experiment."""
    print("=" * 70)
    print(f"{EXPERIMENT_ID} — DOM Feature PMI Analysis")
    print("=" * 70)
    
    random.seed(SEED)
    np.random.seed(SEED)
    os.environ["PYTHONHASHSEED"] = "0"
    
    # ── Step 1: Load Captured Data ──
    print("\n[1/10] Loading captured data...")
    captures_path = os.path.join(INPUT_DIR, 'raw_dom_captures.json')
    if not os.path.exists(captures_path):
        print(f"  FATAL: {captures_path} not found. Run capture_dom_features.js first.")
        return None
    
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
    
    # ── Step 3: Synthetic Positive Control ──
    print("\n[3/10] Analyzing synthetic positive control...")
    
    synth_within = within_url.get('synthetic', [])
    synth_train, synth_test = temporal_split(synth_within, 0.8)
    print(f"  Synthetic: train={len(synth_train)}, test={len(synth_test)}")
    
    # Fit bin edges on TRAIN only
    synth_bin_edges = fit_bin_edges(synth_train)
    
    # DOM-feature PMI on test split
    synth_triples_dom_test = extract_triples(synth_test, 'dom', synth_bin_edges)
    synth_stats_dom_test = compute_pmi_stats(synth_triples_dom_test, SMOOTHING_ALPHA)
    
    # URL-only PMI on test split
    synth_triples_url_test = extract_triples(synth_test, 'url')
    synth_stats_url_test = compute_pmi_stats(synth_triples_url_test, SMOOTHING_ALPHA)
    
    # Permutation test for synthetic DOM
    synth_traj_groups_test = extract_trajectory_groups(synth_test)
    synth_triple_groups_dom_test = {}
    for tid, trans in synth_traj_groups_test.items():
        synth_triple_groups_dom_test[tid] = extract_triples(trans, 'dom', synth_bin_edges)
    
    synth_perm_dom = permutation_test(
        synth_triple_groups_dom_test, synth_stats_dom_test['mean_pmi'],
        N_PERMUTATIONS, SEED, SMOOTHING_ALPHA
    )
    
    print(f"  DOM-feature PMI (test): {synth_stats_dom_test['mean_pmi']:.6f} bits")
    print(f"  URL-only PMI (test): {synth_stats_url_test['mean_pmi']:.6f} bits")
    print(f"  Permutation p: {synth_perm_dom['p_value']:.6f}")
    
    # ── Step 4: Null Control (shuffled labels on real SPA data) ──
    print("\n[4/10] Running null control (shuffled labels on real SPA data)...")
    
    # Combine real SPA data (dashboard, multistep_form, wizard) for null control
    realSPA_data = []
    for site_key in ['dashboard', 'multistep_form', 'wizard']:
        realSPA_data.extend(within_url.get(site_key, []))
    
    # Fit bin edges on real data (for null control we use the combined fit)
    real_bin_edges_for_null = fit_bin_edges(realSPA_data)
    
    # Use DOM state for null control
    real_traj_groups = extract_trajectory_groups(realSPA_data)
    real_triple_groups_dom = {}
    for tid, trans in real_traj_groups.items():
        real_triple_groups_dom[tid] = extract_triples(trans, 'dom', real_bin_edges_for_null)
    
    # Observed PMI on real data
    all_real_triples_dom = []
    for triples in real_triple_groups_dom.values():
        all_real_triples_dom.extend(triples)
    real_stats_dom = compute_pmi_stats(all_real_triples_dom, SMOOTHING_ALPHA)
    
    # Shuffled null
    rng_null = random.Random(SEED + 1000)
    shuffled_groups = shuffle_actions_within_trajectories(real_triple_groups_dom, rng_null)
    all_shuffled = []
    for triples in shuffled_groups.values():
        all_shuffled.extend(triples)
    null_stats = compute_pmi_stats(all_shuffled, SMOOTHING_ALPHA)
    
    # Permutation test for null
    null_perm = permutation_test(
        shuffled_groups, null_stats['mean_pmi'],
        N_PERMUTATIONS, SEED + 1000, SMOOTHING_ALPHA
    )
    
    print(f"  Real SPA DOM PMI: {real_stats_dom['mean_pmi']:.6f} bits")
    print(f"  Null (shuffled) PMI: {null_stats['mean_pmi']:.6f} bits")
    print(f"  Null permutation p: {null_perm['p_value']:.6f}")
    
    # ── Step 5: Genuine SPA Analysis ──
    print("\n[5/10] Analyzing genuine SPAs (DOM-feature, URL-only)...")
    
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
        
        # Fit bin edges on TRAIN only
        bin_edges = fit_bin_edges(train)
        
        print(f"\n  [{site_key}] train={len(train)}, test={n_test}")
        
        # DOM-feature PMI (primary)
        triples_dom = extract_triples(test, 'dom', bin_edges)
        stats_dom = compute_pmi_stats(triples_dom, SMOOTHING_ALPHA)
        
        # URL-only PMI (trivial baseline)
        triples_url = extract_triples(test, 'url')
        stats_url = compute_pmi_stats(triples_url, SMOOTHING_ALPHA)
        
        # Improvements over URL-only
        dom_improvement = stats_dom['mean_pmi'] - stats_url['mean_pmi']
        
        print(f"    DOM-feature PMI: {stats_dom['mean_pmi']:.6f} bits ({stats_dom['unique_states']} states)")
        print(f"    URL-only PMI:    {stats_url['mean_pmi']:.6f} bits ({stats_url['unique_states']} states)")
        print(f"    DOM vs URL:      {dom_improvement:+.6f} bits")
        
        # Permutation test for DOM-feature
        traj_groups = extract_trajectory_groups(test)
        triple_groups_dom = {}
        for tid, trans in traj_groups.items():
            triple_groups_dom[tid] = extract_triples(trans, 'dom', bin_edges)
        
        perm_dom = permutation_test(
            triple_groups_dom, stats_dom['mean_pmi'],
            N_PERMUTATIONS, SEED, SMOOTHING_ALPHA
        )
        
        # Bonferroni-corrected p-value
        perm_p_bonf = min(perm_dom['p_value'] * BONFERRONI_COMPARISONS, 1.0)
        
        print(f"    DOM perm p: {perm_dom['p_value']:.6f} (bonf: {perm_p_bonf:.6f})")
        
        # Alpha sensitivity for DOM-feature
        alpha_sens = alpha_sensitivity(triple_groups_dom)
        alpha_sensitivity_results[site_key] = alpha_sens
        
        # Tautology check: MI(action_label; DOM_state) for dashboard
        if site_key == 'dashboard':
            action_labels = []
            dom_state_list = []
            for t in test:
                action_labels.append(t['action'].get('target_href', '') or t['action'].get('type', ''))
                dom_state = dom_features_to_state(
                    t['state_after'].get('dom_features', {}), bin_edges)
                dom_state_list.append(str(dom_state))
            
            mi_action_dom = compute_mutual_information(action_labels, dom_state_list)
            
            tautology_results[site_key] = {
                'mi_action_dom_state': mi_action_dom,
                'dom_pmi': stats_dom['mean_pmi'],
                'fraction_tautological': mi_action_dom / stats_dom['mean_pmi'] if stats_dom['mean_pmi'] > 0 else 0
            }
            print(f"    Dashboard tautology check: I(action; DOM_state) = {mi_action_dom:.6f} bits")
            print(f"    Fraction of DOM PMI attributable to action->DOM: {tautology_results[site_key]['fraction_tautological']:.1%}")
        
        genuine_results[site_key] = {
            'dom_pmi': stats_dom['mean_pmi'],
            'url_pmi': stats_url['mean_pmi'],
            'dom_vs_url_bits': dom_improvement,
            'n_within_url': len(transitions),
            'n_test': n_test,
            'n_train': len(train),
            'unique_states_dom': stats_dom['unique_states'],
            'unique_states_url': stats_url['unique_states'],
            'unique_sa_pairs_dom': stats_dom['unique_sa_pairs'],
            'perm_p_dom': perm_dom['p_value'],
            'perm_p_dom_bonf': perm_p_bonf,
            'effect_d_dom': perm_dom['effect_size_d'],
        }
        
        perm_tests[f'{site_key}_dom'] = perm_dom
    
    # ── Step 6: Decision Evaluation ──
    print("\n[6/10] Evaluating decision rules...")
    
    # Positive control
    positive_control_pmi = synth_stats_dom_test['mean_pmi']
    positive_control_perm_p = synth_perm_dom['p_value']
    positive_control_passes = positive_control_pmi >= 0.5 and positive_control_perm_p < 0.001
    
    # Null control
    null_control_perm_p = null_perm['p_value']
    null_control_passes = null_control_perm_p > 0.01
    
    # Primary condition: DOM-feature PMI exceeds URL-only by >= 0.1 bits on >= 2/3 sites
    sites_passing = 0
    sites_total = len(genuine_results)
    primary_per_site = {}
    
    for site_key, site_res in genuine_results.items():
        passes = (site_res['dom_vs_url_bits'] >= 0.1 and
                  site_res['perm_p_dom_bonf'] < ALPHA_BONFERRONI)
        primary_per_site[site_key] = {
            'dom_vs_url_bits': site_res['dom_vs_url_bits'],
            'perm_p_dom_bonf': site_res['perm_p_dom_bonf'],
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
    
    # Decision per spec
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
    print(f"  Positive control DOM PMI (test): {positive_control_pmi:.6f} (>= 0.5 required)")
    print(f"  Positive control perm p:         {positive_control_perm_p:.6f} (< 0.001 required)")
    print(f"  Positive control passes:         {positive_control_passes}")
    print(f"  Null control perm p:             {null_control_perm_p:.6f} (> 0.01 required)")
    print(f"  Null control passes:             {null_control_passes}")
    print(f"  Primary condition:               {primary_condition} ({sites_passing}/{sites_total} sites >= {threshold})")
    print(f"  Data sufficient:                 {data_sufficient}")
    print(f"  OUTCOME: {outcome}")
    print(f"  STATUS:  {status}")
    print(f"{'=' * 70}")
    
    # ── Step 7: Per-Site Summary ──
    print("\n[7/10] Per-site summary...")
    for site_key, site_res in genuine_results.items():
        print(f"\n  [{site_key}]")
        print(f"    DOM-feature PMI:  {site_res['dom_pmi']:.6f} bits")
        print(f"    URL-only PMI:     {site_res['url_pmi']:.6f} bits")
        print(f"    DOM > URL by:     {site_res['dom_vs_url_bits']:+.6f} bits")
        print(f"    Primary passes:   {primary_per_site[site_key]['passes']}")
    
    # ── Step 8: Build Results ──
    print("\n[8/10] Building results structure...")
    
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
        },
        "controls": {
            "positive_control_synthetic_dom": {
                "description": "Synthetic SPA with deterministic DOM evolution (8 states, 4 actions, state-specific DOM features)",
                "expected": "DOM-feature PMI >= 0.5 bits, permutation p < 0.001 on 80/20 test split",
                "observed_pmi": positive_control_pmi,
                "observed_perm_p": positive_control_perm_p,
                "result": "PASS" if positive_control_passes else "FAIL",
            },
            "null_control_shuffled_real_labels": {
                "description": "Shuffled action labels on real SPA DOM-feature data (dashboard, multistep_form, wizard)",
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
    results = run_experiment()
    if results is None:
        print("Experiment failed.")
        sys.exit(1)
    
    out_path = os.path.join(OUTPUT_DIR, 'pmi_results_dom_features.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {out_path}")
