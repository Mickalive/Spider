#!/usr/bin/env python3
"""
EXP-PHYSICS-34629310987 — Accessibility Tree PMI Experiment (v2)
Tests whether the accessibility tree provides predictive state information
beyond URL on form-heavy SPAs with client-side routing.

Frozen inputs: request.json, spec.json, prereg.md, freeze.json
All computation deterministic (seed=42, PYTHONHASHSEED=0).

Changes from v1:
- Fixed null control: use permutation p-value on shuffled a11y labels, not shuffled mean <= 0
- Improved real site automation: overlay dismissal, better error handling, more candidates
- Added proper null control permutation test (shuffle a11y labels, check p > 0.01)
"""

import json
import math
import random
import collections
import os
import sys
import hashlib
import time
import traceback
from pathlib import Path

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34629310987"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
BONFERRONI_COMPARISONS = 4  # 2 sites x 2 conditions (within-URL and overall)
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.0125

# ─── Synthetic SPA Configuration ──────────────────────────────────────────────

SYNTHETIC_SPA_PATH = Path(__file__).parent / "synthetic_spa.html"

# 8 states with same URL but different accessibility trees
SYNTHETIC_STATES = {
    0: {"url_suffix": "", "title": "Checkout Form",
        "a11y_signature": ["textbox:Shipping Name", "textbox:Shipping Address", "textbox:City"]},
    1: {"url_suffix": "", "title": "Login Form",
        "a11y_signature": ["textbox:Username", "textbox:Password", "checkbox:Remember me"]},
    2: {"url_suffix": "", "title": "Registration Form",
        "a11y_signature": ["textbox:Email", "textbox:Password", "textbox:Confirm Password", "checkbox:I agree to terms"]},
    3: {"url_suffix": "", "title": "User Dashboard",
        "a11y_signature": ["heading:Profile", "text:Name: John Doe", "heading:Statistics", "text:Orders: 5"]},
    4: {"url_suffix": "", "title": "Admin Dashboard",
        "a11y_signature": ["heading:System Status", "text:Users: 1,234", "button:System Settings", "button:Manage Users"]},
    5: {"url_suffix": "", "title": "Analytics Dashboard",
        "a11y_signature": ["heading:Traffic", "text:Visitors: 12,345", "heading:Conversions", "text:Signups: 234"]},
    6: {"url_suffix": "", "title": "Account Settings",
        "a11y_signature": ["textbox:Display Name", "combobox:Email Preferences", "checkbox:Enable two-factor auth"]},
    7: {"url_suffix": "", "title": "Privacy Settings",
        "a11y_signature": ["combobox:Profile Visibility", "checkbox:Show activity status", "checkbox:Allow data sharing"]}
}

# Transition matrix (same as spec)
SYNTHETIC_TRANSITIONS = {
    0: {"form_submit": 3, "button_click": 4, "link_nav": 6, "menu_select": 7},
    1: {"form_submit": 5, "button_click": 3, "link_nav": 4, "menu_select": 6},
    2: {"form_submit": 3, "button_click": 5, "link_nav": 7, "menu_select": 4},
    3: {"form_submit": 0, "button_click": 1, "link_nav": 2, "menu_select": 6},
    4: {"form_submit": 1, "button_click": 2, "link_nav": 0, "menu_select": 7},
    5: {"form_submit": 2, "button_click": 0, "link_nav": 1, "menu_select": 6},
    6: {"form_submit": 3, "button_click": 4, "link_nav": 5, "menu_select": 0},
    7: {"form_submit": 5, "button_click": 3, "link_nav": 6, "menu_select": 1}
}


# ─── Accessibility Tree Processing ────────────────────────────────────────────

def parse_aria_snapshot(snapshot_str):
    """Parse aria_snapshot() string into semantic signature.
    
    Format: lines like "- button \"Click me\"", "- textbox", etc.
    Returns list of strings like "role:name" or "role:name:state"
    """
    import re
    signature = []
    lines = snapshot_str.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line.startswith('-'):
            continue
        
        # Remove leading "- " and indentation
        content = line.lstrip('-').strip()
        
        # Parse role and name
        match = re.match(r'(\w+)\s*"([^"]*)"(?:\s*\[([^\]]*)\])?', content)
        if match:
            role, name, attrs = match.groups()
        else:
            match = re.match(r'(\w+)(?:\s*\[([^\]]*)\])?', content)
            if match:
                role, attrs = match.groups()
                name = ''
            else:
                continue
        
        # Filter out presentation/none roles
        if role in ["presentation", "none", "generic", "document", "main", "article", "text"]:
            continue
        
        state_parts = []
        if attrs:
            if "selected" in attrs:
                state_parts.append("selected")
            if "checked" in attrs:
                state_parts.append("checked")
            if "disabled" in attrs:
                state_parts.append("disabled")
        
        if name:
            sig = f"{role}:{name}"
        else:
            sig = role
        
        if state_parts:
            sig += ":" + ":".join(state_parts)
        
        signature.append(sig)
    
    return signature


def compute_a11y_hash(signature):
    """Compute deterministic hash of accessibility tree signature."""
    sorted_sig = sorted(signature)
    sig_str = "|".join(sorted_sig)
    return hashlib.sha256(sig_str.encode()).hexdigest()[:16]


# ─── PMI Computation ─────────────────────────────────────────────────────────

def compute_pmi_stats(triples):
    """Compute PMI statistics for a set of triples.
    
    PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
    """
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "pmi_values": [], "N": 0,
                "unique_states": 0, "unique_actions": 0, "unique_sa_pairs": 0}

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

        distinct_actions_s = sum(1 for (si, ai) in state_action_counts if si == s)
        distinct_next_s = sum(1 for (si, sni) in state_next_counts if si == s)

        p_a_given_s = (count_sa + ALPHA) / (count_s + ALPHA * distinct_actions_s)
        p_s_next_given_s = (count_ss_next + ALPHA) / (count_s + ALPHA * distinct_next_s)
        p_joint_given_s = count_sas_next / count_s

        denom = p_a_given_s * p_s_next_given_s
        if denom > 0 and p_joint_given_s > 0:
            pmi = math.log2(p_joint_given_s / denom)
        else:
            pmi = 0.0

        pmi_values.append(pmi)

    mean_pmi = sum(pmi_values) / len(pmi_values)

    return {
        "mean_pmi": mean_pmi,
        "pmi_values": pmi_values,
        "N": N,
        "unique_states": len(state_counts),
        "unique_actions": len(set(a for _, a, _ in triples)),
        "unique_sa_pairs": len(state_action_counts),
    }


# ─── Permutation Test ────────────────────────────────────────────────────────

def permutation_test(triples, observed_mean_pmi, n_permutations, seed):
    """Permutation test for PMI significance.
    
    Shuffles next_states to break action->next_state dependency
    while preserving state->action marginal.
    """
    rng = random.Random(seed)
    
    states = [t[0] for t in triples]
    actions = [t[1] for t in triples]
    next_states = [t[2] for t in triples]
    
    shuffled_means = []
    for _ in range(n_permutations):
        shuffled_next = next_states.copy()
        rng.shuffle(shuffled_next)
        shuffled_triples = list(zip(states, actions, shuffled_next))
        stats = compute_pmi_stats(shuffled_triples)
        shuffled_means.append(stats["mean_pmi"])
    
    count_gt = sum(1 for m in shuffled_means if m > observed_mean_pmi)
    p_value = (count_gt + 1) / (n_permutations + 1)
    
    null_mean = float(np.mean(shuffled_means))
    null_std = float(np.std(shuffled_means))
    effect_d = float((observed_mean_pmi - null_mean) / null_std) if null_std > 0 else 0.0
    
    return {
        "p_value": p_value,
        "shuffled_means": shuffled_means,
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
    }


def null_control_permutation_test(triples, n_permutations, seed):
    """Null control: shuffle a11y labels and check PMI is not significant.
    
    Per the prereg: "Permute accessibility-tree hashes across transitions.
    Expected: PMI not significantly > 0 (permutation p > 0.01)."
    
    This shuffles BOTH source and target a11y labels (preserving pairing)
    to destroy all a11y-based structure, then runs a permutation test
    on this shuffled data to verify no spurious structure is detected.
    """
    rng = random.Random(seed)
    
    # Shuffle a11y labels: randomly reassign a11y hashes to transitions
    # This destroys the true a11y->a11y_next dependency
    a11y_hashes = [t[0] for t in triples]  # source a11y
    a11y_next_hashes = [t[2] for t in triples]  # target a11y
    actions = [t[1] for t in triples]
    
    # Create shuffled triples by permuting a11y labels
    shuffled_a11y = a11y_hashes.copy()
    shuffled_a11y_next = a11y_next_hashes.copy()
    rng.shuffle(shuffled_a11y)
    rng.shuffle(shuffled_a11y_next)
    
    shuffled_triples = list(zip(shuffled_a11y, actions, shuffled_a11y_next))
    shuffled_stats = compute_pmi_stats(shuffled_triples)
    shuffled_pmi = shuffled_stats["mean_pmi"]
    
    # Now run permutation test on this shuffled data to get p-value
    # (shuffling next_states again should not find more structure)
    perm = permutation_test(shuffled_triples, shuffled_pmi, min(n_permutations, 200), seed + 1000)
    
    return {
        "shuffled_pmi": shuffled_pmi,
        "shuffled_n_transitions": len(shuffled_triples),
        "shuffled_unique_states": shuffled_stats["unique_states"],
        "permutation_p": perm["p_value"],
        "permutation_null_mean": perm["null_mean"],
        "passes": perm["p_value"] > 0.01,  # prereg: p > 0.01 means shuffled data is not significant
    }


# ─── Entropy Analysis ────────────────────────────────────────────────────────

def compute_entropy(values):
    """Compute Shannon entropy of a list of values."""
    counts = collections.Counter(values)
    N = len(values)
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / N
            entropy -= p * math.log2(p)
    return entropy


# ─── Synthetic SPA Experiment ────────────────────────────────────────────────

def run_synthetic_experiment():
    """Run experiment on synthetic SPA with deterministic accessibility tree evolution."""
    print("=" * 70)
    print(f"SYNTHETIC SPA EXPERIMENT — {EXPERIMENT_ID}")
    print("=" * 70)
    
    try:
        from playwright.sync_api import sync_playwright
        
        # Create file URL
        file_url = f"file://{SYNTHETIC_SPA_PATH.resolve()}"
        print(f"\n[1/6] File URL: {file_url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # Navigate to synthetic SPA
            print("\n[2/6] Navigating to synthetic SPA...")
            page.goto(file_url)
            page.wait_for_load_state("networkidle")
            
            # Collect transitions
            transitions = []
            n_trajectories = 25
            trajectory_length = 20
            
            print(f"\n[3/6] Collecting {n_trajectories} trajectories of length {trajectory_length}...")
            
            rng = random.Random(SEED)
            actions = list(SYNTHETIC_TRANSITIONS[0].keys())
            
            for traj_id in range(n_trajectories):
                # Start at random state
                current_state = rng.choice(list(SYNTHETIC_STATES.keys()))
                
                # Navigate to initial state
                for _ in range(5):
                    action = rng.choice(actions)
                    page.evaluate(f"takeAction('{action}')")
                    page.wait_for_timeout(100)
                
                # Collect transitions
                for step in range(trajectory_length):
                    url_before = page.url
                    
                    # Extract accessibility tree
                    try:
                        a11y_snapshot_str = page.locator('body').aria_snapshot()
                        a11y_sig = parse_aria_snapshot(a11y_snapshot_str)
                        a11y_hash = compute_a11y_hash(a11y_sig)
                    except Exception as e:
                        print(f"  Warning: a11y snapshot failed: {e}")
                        a11y_sig = []
                        a11y_hash = "empty"
                    
                    # Take action
                    action = rng.choice(actions)
                    page.evaluate(f"takeAction('{action}')")
                    page.wait_for_timeout(100)
                    
                    # Get next state
                    url_after = page.url
                    try:
                        a11y_snapshot_after_str = page.locator('body').aria_snapshot()
                        a11y_sig_after = parse_aria_snapshot(a11y_snapshot_after_str)
                        a11y_hash_after = compute_a11y_hash(a11y_sig_after)
                    except Exception as e:
                        a11y_sig_after = []
                        a11y_hash_after = "empty"
                    
                    transitions.append({
                        "trajectory_id": traj_id,
                        "state_before": {"url": url_before, "a11y_hash": a11y_hash, "a11y_signature": a11y_sig},
                        "action": action,
                        "state_after": {"url": url_after, "a11y_hash": a11y_hash_after, "a11y_signature": a11y_sig_after}
                    })
            
            print(f"  Collected {len(transitions)} transitions")
            
            # Analyze transitions
            print("\n[4/6] Analyzing transitions...")
            
            within_url_transitions = [t for t in transitions if t["state_before"]["url"] == t["state_after"]["url"]]
            all_non_leakage = transitions  # All synthetic transitions are non-leakage
            
            print(f"  Total: {len(transitions)}, Non-leakage: {len(all_non_leakage)}, Within-URL: {len(within_url_transitions)}")
            
            # Compute PMI for different state representations
            print("\n[5/6] Computing PMI...")
            
            url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in all_non_leakage]
            a11y_triples = [(t["state_before"]["a11y_hash"], t["action"], t["state_after"]["a11y_hash"]) for t in all_non_leakage]
            combined_triples = [((t["state_before"]["url"], t["state_before"]["a11y_hash"]),
                                t["action"],
                                (t["state_after"]["url"], t["state_after"]["a11y_hash"]))
                               for t in all_non_leakage]
            
            url_stats = compute_pmi_stats(url_triples)
            a11y_stats = compute_pmi_stats(a11y_triples)
            combined_stats = compute_pmi_stats(combined_triples)
            
            within_url_url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in within_url_transitions]
            within_url_a11y_triples = [(t["state_before"]["a11y_hash"], t["action"], t["state_after"]["a11y_hash"]) for t in within_url_transitions]
            
            within_url_url_stats = compute_pmi_stats(within_url_url_triples)
            within_url_a11y_stats = compute_pmi_stats(within_url_a11y_triples)
            
            print(f"  URL-only PMI (all): {url_stats['mean_pmi']:.6f} bits")
            print(f"  A11y-only PMI (all): {a11y_stats['mean_pmi']:.6f} bits")
            print(f"  Combined PMI (all): {combined_stats['mean_pmi']:.6f} bits")
            print(f"  URL-only PMI (within-URL): {within_url_url_stats['mean_pmi']:.6f} bits")
            print(f"  A11y-only PMI (within-URL): {within_url_a11y_stats['mean_pmi']:.6f} bits")
            
            # Permutation tests
            print("\n[6/6] Running permutation tests...")
            
            url_perm = permutation_test(url_triples, url_stats["mean_pmi"], N_PERMUTATIONS, SEED)
            a11y_perm = permutation_test(a11y_triples, a11y_stats["mean_pmi"], N_PERMUTATIONS, SEED)
            within_url_a11y_perm = permutation_test(within_url_a11y_triples, within_url_a11y_stats["mean_pmi"],
                                                    N_PERMUTATIONS, SEED)
            
            # Null control: shuffle a11y labels and check PMI is not significant
            null_ctrl = null_control_permutation_test(a11y_triples, N_PERMUTATIONS, SEED)
            
            print(f"  URL-only permutation p: {url_perm['p_value']:.6f}")
            print(f"  A11y-only permutation p: {a11y_perm['p_value']:.6f}")
            print(f"  Within-URL A11y permutation p: {within_url_a11y_perm['p_value']:.6f}")
            print(f"  Null control shuffled PMI: {null_ctrl['shuffled_pmi']:.6f}")
            print(f"  Null control permutation p: {null_ctrl['permutation_p']:.6f}")
            print(f"  Null control passes: {null_ctrl['passes']}")
            
            # Decision evaluation
            print(f"\n{'=' * 70}")
            print("DECISION EVALUATION")
            print(f"{'=' * 70}")
            
            # Condition 1: A11y PMI > URL-only PMI by >= 0.1 bits on within-URL transitions
            gain_within_url = within_url_a11y_stats["mean_pmi"] - within_url_url_stats["mean_pmi"]
            condition_1 = gain_within_url >= 0.1
            print(f"  Condition 1: A11y gain >= 0.1 bits: {gain_within_url:.6f} >= 0.1 = {condition_1}")
            
            # Condition 2: A11y permutation p < 0.01 after Bonferroni
            condition_2 = within_url_a11y_perm["p_value"] < ALPHA_BONFERRONI
            print(f"  Condition 2: A11y perm p < {ALPHA_BONFERRONI}: {within_url_a11y_perm['p_value']:.6f} < {ALPHA_BONFERRONI} = {condition_2}")
            
            # Condition 3: Positive control passes (synthetic SPA PMI >= 0.5)
            condition_3 = a11y_stats["mean_pmi"] >= 0.5
            print(f"  Condition 3: A11y PMI >= 0.5: {a11y_stats['mean_pmi']:.6f} >= 0.5 = {condition_3}")
            
            # Condition 4: Null control passes (shuffled PMI not > 0, p > 0.01)
            # Fixed: use permutation p-value on shuffled data, not shuffled mean <= 0
            condition_4 = null_ctrl["passes"]
            print(f"  Condition 4: Null control (shuffled perm p > 0.01): {null_ctrl['permutation_p']:.6f} > 0.01 = {condition_4}")
            
            # Condition 5: A11y varies within URL (entropy > 0)
            a11y_hashes_within_url = [t["state_before"]["a11y_hash"] for t in within_url_transitions]
            unique_a11y_within_url = len(set(a11y_hashes_within_url))
            a11y_entropy_within_url = compute_entropy(a11y_hashes_within_url) if a11y_hashes_within_url else 0.0
            condition_5 = unique_a11y_within_url > 1
            print(f"  Condition 5: A11y varies within URL: {unique_a11y_within_url} unique hashes, entropy={a11y_entropy_within_url:.4f} bits > 0 = {condition_5}")
            
            # Condition 6: Data sufficiency
            condition_6 = len(all_non_leakage) >= 50
            print(f"  Condition 6: Data sufficiency: {len(all_non_leakage)} >= 50 = {condition_6}")
            
            # Overall decision
            survives = all([condition_1, condition_2, condition_3, condition_4, condition_5, condition_6])
            outcome = "SUPPORTS" if survives else "FALSIFIES"
            
            print(f"\n  SURVIVES_CURRENT_TEST: {survives}")
            print(f"  OUTCOME: {outcome}")
            
            # Entropy analysis
            url_entropy = compute_entropy([t["state_before"]["url"] for t in transitions])
            a11y_entropy = compute_entropy([t["state_before"]["a11y_hash"] for t in transitions])
            a11y_entropy_given_url = compute_entropy(
                [(t["state_before"]["url"], t["state_before"]["a11y_hash"]) for t in transitions]
            ) - url_entropy
            
            results = {
                "experiment_id": EXPERIMENT_ID,
                "synthetic_spa": {
                    "n_transitions": len(transitions),
                    "n_trajectories": n_trajectories,
                    "trajectory_length": trajectory_length,
                    "within_url_transitions": len(within_url_transitions),
                    "unique_a11y_hashes": len(set(t["state_before"]["a11y_hash"] for t in transitions)),
                },
                "pmi_results": {
                    "url_only_all": url_stats["mean_pmi"],
                    "a11y_only_all": a11y_stats["mean_pmi"],
                    "combined_all": combined_stats["mean_pmi"],
                    "url_only_within_url": within_url_url_stats["mean_pmi"],
                    "a11y_only_within_url": within_url_a11y_stats["mean_pmi"],
                },
                "permutation_tests": {
                    "url_only": {"p_value": url_perm["p_value"], "null_mean": url_perm["null_mean"], "effect_d": url_perm["effect_size_d"]},
                    "a11y_only": {"p_value": a11y_perm["p_value"], "null_mean": a11y_perm["null_mean"], "effect_d": a11y_perm["effect_size_d"]},
                    "within_url_a11y": {"p_value": within_url_a11y_perm["p_value"], "null_mean": within_url_a11y_perm["null_mean"], "effect_d": within_url_a11y_perm["effect_size_d"]},
                },
                "null_control": {
                    "shuffled_pmi": null_ctrl["shuffled_pmi"],
                    "permutation_p": null_ctrl["permutation_p"],
                    "permutation_null_mean": null_ctrl["permutation_null_mean"],
                    "passes": null_ctrl["passes"],
                },
                "entropy_analysis": {
                    "url_entropy": url_entropy,
                    "a11y_entropy": a11y_entropy,
                    "a11y_entropy_given_url": a11y_entropy_given_url,
                },
                "decision_conditions": {
                    "gain_within_url_bits": gain_within_url,
                    "condition_1_gain_ge_0.1": condition_1,
                    "condition_2_permutation_p": within_url_a11y_perm["p_value"],
                    "condition_2_passes": condition_2,
                    "condition_3_positive_control_pmi": a11y_stats["mean_pmi"],
                    "condition_3_passes": condition_3,
                    "condition_4_null_control_p": null_ctrl["permutation_p"],
                    "condition_4_passes": condition_4,
                    "condition_5_a11y_unique_hashes": unique_a11y_within_url,
                    "condition_5_a11y_entropy_bits": a11y_entropy_within_url,
                    "condition_5_passes": condition_5,
                    "condition_6_data_sufficiency": len(all_non_leakage),
                    "condition_6_passes": condition_6,
                },
                "survives_current_test": survives,
                "outcome": outcome,
                "status": "COMPLETE",
            }
            
            return results, transitions
            
    except Exception as e:
        print(f"Synthetic SPA experiment failed: {e}")
        traceback.print_exc()
        raise


# ─── Real Site Experiment ─────────────────────────────────────────────────────

def try_dismiss_overlays(page):
    """Try to dismiss common overlay/modal elements."""
    overlay_selectors = [
        '[class*="modal"] button[class*="close"]',
        '[class*="overlay"] button[class*="close"]',
        '[class*="dialog"] button[class*="close"]',
        'button[aria-label="Close"]',
        'button[aria-label="Dismiss"]',
        '[class*="cookie"] button',
        '[class*="consent"] button',
        '[class*="banner"] button',
        '[data-testid*="close"]',
        '[class*="popup"] button',
    ]
    dismissed = 0
    for sel in overlay_selectors:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                el.click(force=True)
                page.wait_for_timeout(300)
                dismissed += 1
        except:
            pass
    return dismissed


def safe_click(page, selector, timeout=5000):
    """Try to click an element with force=True to bypass overlay interception."""
    try:
        el = page.query_selector(selector)
        if el and el.is_visible():
            el.click(force=True, timeout=timeout)
            return True
    except:
        pass
    return False


def extract_page_state(page):
    """Extract URL and accessibility tree hash from current page state."""
    url = page.url
    try:
        snapshot = page.locator('body').aria_snapshot()
        sig = parse_aria_snapshot(snapshot)
        a11y_hash = compute_a11y_hash(sig)
        return url, a11y_hash, sig
    except Exception as e:
        return url, "error", []


def try_interact_with_page(page):
    """Try various strategies to interact with the page and advance state."""
    # Strategy 1: Try Next/Continue/Submit buttons
    for text in ["Next", "Continue", "Submit", "Continue to next step", "Next step", "next"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn and btn.is_visible():
                btn.click(force=True, timeout=3000)
                return f"click_{text.lower()}"
        except:
            pass
    
    # Strategy 2: Try primary/submit buttons
    for sel in ['button[type="submit"]', 'button.primary', 'button.btn-primary', 
                'button[data-testid*="next"]', 'button[data-testid*="continue"]',
                'button[class*="next"]', 'button[class*="continue"]']:
        if safe_click(page, sel, timeout=2000):
            return f"click_{sel}"
    
    # Strategy 3: Try any visible button
    try:
        buttons = page.query_selector_all("button")
        for btn in buttons:
            if btn.is_visible():
                btn.click(force=True, timeout=2000)
                return "click_button"
    except:
        pass
    
    # Strategy 4: Try links
    try:
        links = page.query_selector_all("a[href]")
        for link in links:
            if link.is_visible():
                link.click(force=True, timeout=2000)
                return "click_link"
    except:
        pass
    
    # Strategy 5: Fill input and submit form
    try:
        inputs = page.query_selector_all("input:visible")
        if inputs:
            inputs[0].fill("test_value")
            inputs[0].press("Enter")
            return "fill_and_submit"
    except:
        pass
    
    return "no_action"


def run_real_site_experiment(site_name, site_url, max_steps=30):
    """Run experiment on a real form-heavy SPA."""
    print(f"\n{'=' * 70}")
    print(f"REAL SITE EXPERIMENT — {site_name}")
    print(f"URL: {site_url}")
    print(f"{'=' * 70}")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # Navigate to site
            print(f"\n[1/4] Navigating...")
            try:
                page.goto(site_url, timeout=30000, wait_until="networkidle")
            except:
                try:
                    page.goto(site_url, timeout=30000, wait_until="domcontentloaded")
                    page.wait_for_timeout(3000)
                except Exception as e:
                    print(f"  Failed to navigate: {e}")
                    return None
            
            # Dismiss overlays
            time.sleep(2)
            dismissed = try_dismiss_overlays(page)
            if dismissed:
                print(f"  Dismissed {dismissed} overlays")
            
            # Collect initial state
            url0, a11y0, sig0 = extract_page_state(page)
            print(f"  Initial URL: {url0}")
            print(f"  Initial a11y hash: {a11y0}")
            print(f"  Initial a11y sig length: {len(sig0)}")
            
            if len(sig0) == 0:
                print("  WARNING: Empty accessibility tree — page may not have loaded")
            
            # Collect transitions
            transitions = []
            prev_url = url0
            prev_hash = a11y0
            
            for step in range(max_steps):
                action = try_interact_with_page(page)
                page.wait_for_timeout(1500)
                
                # Try dismissing overlays again
                try_dismiss_overlays(page)
                
                url, a11y_hash, sig = extract_page_state(page)
                
                transitions.append({
                    "step": step,
                    "state_before": {"url": prev_url, "a11y_hash": prev_hash},
                    "action": action,
                    "state_after": {"url": url, "a11y_hash": a11y_hash}
                })
                
                if step % 10 == 0:
                    print(f"  Step {step}: action={action}, url_changed={url != prev_url}, a11y_changed={a11y_hash != prev_hash}")
                
                prev_url = url
                prev_hash = a11y_hash
            
            print(f"\n  Collected {len(transitions)} transitions")
            
            # Analyze
            within_url = [t for t in transitions if t["state_before"]["url"] == t["state_after"]["url"]]
            non_leakage = [t for t in transitions if t["action"] not in ["no_action"]]
            
            print(f"  Non-leakage: {len(non_leakage)}, Within-URL: {len(within_url)}")
            
            if len(non_leakage) < 10:
                print("  Insufficient transitions for reliable PMI")
                return {"site_name": site_name, "site_url": site_url, "status": "INSUFFICIENT_DATA",
                        "n_transitions": len(transitions), "n_non_leakage": len(non_leakage)}
            
            # Compute PMI
            url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in non_leakage]
            a11y_triples = [(t["state_before"]["a11y_hash"], t["action"], t["state_after"]["a11y_hash"]) for t in non_leakage]
            
            url_stats = compute_pmi_stats(url_triples)
            a11y_stats = compute_pmi_stats(a11y_triples)
            
            within_url_url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in within_url]
            within_url_a11y_triples = [(t["state_before"]["a11y_hash"], t["action"], t["state_after"]["a11y_hash"]) for t in within_url]
            
            within_url_url_stats = compute_pmi_stats(within_url_url_triples) if within_url_url_triples else {"mean_pmi": 0.0}
            within_url_a11y_stats = compute_pmi_stats(within_url_a11y_triples) if within_url_a11y_triples else {"mean_pmi": 0.0}
            
            # Permutation tests
            a11y_perm = permutation_test(a11y_triples, a11y_stats["mean_pmi"], N_PERMUTATIONS, SEED) if len(a11y_triples) >= 10 else None
            within_url_a11y_perm = permutation_test(within_url_a11y_triples, within_url_a11y_stats["mean_pmi"], N_PERMUTATIONS, SEED) if len(within_url_a11y_triples) >= 10 else None
            
            # Null control
            null_ctrl = null_control_permutation_test(a11y_triples, N_PERMUTATIONS, SEED) if len(a11y_triples) >= 10 else None
            
            # Entropy
            url_entropy = compute_entropy([t["state_before"]["url"] for t in transitions])
            a11y_entropy = compute_entropy([t["state_before"]["a11y_hash"] for t in transitions])
            unique_a11y = len(set(t["state_before"]["a11y_hash"] for t in transitions))
            unique_urls = len(set(t["state_before"]["url"] for t in transitions))
            
            print(f"\n  Results:")
            print(f"    URL-only PMI: {url_stats['mean_pmi']:.6f} bits")
            print(f"    A11y-only PMI: {a11y_stats['mean_pmi']:.6f} bits")
            print(f"    URL-only PMI (within-URL): {within_url_url_stats['mean_pmi']:.6f} bits")
            print(f"    A11y-only PMI (within-URL): {within_url_a11y_stats['mean_pmi']:.6f} bits")
            print(f"    Unique URLs: {unique_urls}, Unique a11y hashes: {unique_a11y}")
            print(f"    URL entropy: {url_entropy:.4f}, A11y entropy: {a11y_entropy:.4f}")
            if a11y_perm:
                print(f"    A11y permutation p: {a11y_perm['p_value']:.6f}")
            if within_url_a11y_perm:
                print(f"    Within-URL A11y perm p: {within_url_a11y_perm['p_value']:.6f}")
            if null_ctrl:
                print(f"    Null control shuffled PMI: {null_ctrl['shuffled_pmi']:.6f}, p: {null_ctrl['permutation_p']:.6f}, passes: {null_ctrl['passes']}")
            
            results = {
                "site_name": site_name,
                "site_url": site_url,
                "status": "COMPLETE",
                "n_transitions": len(transitions),
                "n_non_leakage": len(non_leakage),
                "n_within_url": len(within_url),
                "unique_a11y_hashes": unique_a11y,
                "unique_urls": unique_urls,
                "pmi_results": {
                    "url_only_all": url_stats["mean_pmi"],
                    "a11y_only_all": a11y_stats["mean_pmi"],
                    "url_only_within_url": within_url_url_stats["mean_pmi"],
                    "a11y_only_within_url": within_url_a11y_stats["mean_pmi"],
                },
                "permutation_tests": {
                    "a11y_only": {"p_value": a11y_perm["p_value"], "null_mean": a11y_perm["null_mean"]} if a11y_perm else None,
                    "within_url_a11y": {"p_value": within_url_a11y_perm["p_value"], "null_mean": within_url_a11y_perm["null_mean"]} if within_url_a11y_perm else None,
                },
                "null_control": {
                    "shuffled_pmi": null_ctrl["shuffled_pmi"],
                    "permutation_p": null_ctrl["permutation_p"],
                    "passes": null_ctrl["passes"],
                } if null_ctrl else None,
                "entropy_analysis": {
                    "url_entropy": url_entropy,
                    "a11y_entropy": a11y_entropy,
                },
                "raw_transitions": transitions,
            }
            
            browser.close()
            return results
            
    except Exception as e:
        print(f"  Experiment failed: {e}")
        traceback.print_exc()
        return {"site_name": site_name, "site_url": site_url, "status": "EXCEPTION", "error": str(e)}


# ─── Main Experiment ─────────────────────────────────────────────────────────

def main():
    """Run the full accessibility tree PMI experiment."""
    os.environ["PYTHONHASHSEED"] = "0"
    
    print("=" * 70)
    print(f"ACCESSIBILITY TREE PMI EXPERIMENT (v2) — {EXPERIMENT_ID}")
    print("=" * 70)
    
    # 1. Synthetic SPA experiment (positive control)
    synthetic_results, synthetic_transitions = run_synthetic_experiment()
    
    # Save raw results
    out_dir = Path(__file__).parent
    raw_results_path = out_dir / "raw_results_v2.json"
    with open(raw_results_path, "w") as f:
        json.dump(synthetic_results, f, indent=2, default=str)
    print(f"\nRaw results saved to {raw_results_path}")
    
    transitions_path = out_dir / "synthetic_transitions_v2.json"
    with open(transitions_path, "w") as f:
        json.dump(synthetic_transitions, f, indent=2, default=str)
    
    # 2. Real site experiments (best effort, multiple candidates)
    real_site_configs = [
        ("tally_form", "https://tally.so/r/wAqjQj"),
        ("google_form_example", "https://docs.google.com/forms/d/e/1FAIpQLScexample/viewform"),
    ]
    
    real_site_results = []
    for name, url in real_site_configs:
        result = run_real_site_experiment(name, url, max_steps=30)
        if result:
            real_site_results.append(result)
    
    # Save real site results
    if real_site_results:
        real_results_path = out_dir / "real_site_results_v2.json"
        with open(real_results_path, "w") as f:
            json.dump(real_site_results, f, indent=2, default=str)
        print(f"\nReal site results saved to {real_results_path}")
    
    # Summary
    print(f"\n{'=' * 70}")
    print("EXPERIMENT SUMMARY")
    print(f"{'=' * 70}")
    print(f"Synthetic SPA: {synthetic_results['outcome']} (survives={synthetic_results['survives_current_test']})")
    print(f"Real sites tested: {len(real_site_results)}")
    for r in real_site_results:
        print(f"  {r.get('site_name', '?')}: {r.get('status', '?')}")
    
    return synthetic_results, real_site_results


if __name__ == "__main__":
    main()
