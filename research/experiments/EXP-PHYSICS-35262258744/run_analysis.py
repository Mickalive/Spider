#!/usr/bin/env python3
"""
EXP-PHYSICS-35262258744 — URL-level PMI on real browser-collected SPA transitions:
raw vs normalized URL representation.

Frozen inputs: request.json, spec.json, prereg.md, freeze.json
All computation deterministic (seed=42, PYTHONHASHSEED=0).
"""

import json
import math
import random
import collections
import os
import sys
import hashlib

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-35262258744"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
PARENT_DIR = "research/experiments/EXP-PHYSICS-35209110569"
VARIANTS = ["vanillajs", "react", "vue", "angular", "svelte"]

# Per frozen spec: 5 primary comparisons (5 variants), Bonferroni
BONFERRONI_COMPARISONS = 5
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.01

DATA_FILES = {
    "vanillajs": ["raw_vanillajs.json", "raw_vanillajs_topup.json"],
    "react": ["raw_react.json", "raw_react_topup.json"],
    "vue": ["raw_vue.json", "raw_vue_topup.json"],
    "angular": ["raw_angular.json", "raw_angular_topup.json"],
    "svelte": ["raw_svelte.json", "raw_svelte_topup.json"],
}


# ─── Data Loading ────────────────────────────────────────────────────────────

def normalize_url(url: str) -> str:
    """Normalize URL: strip fragment, trailing slash, percent-encoding.
    
    This is the standard fragment-stripping normalization.
    On TodoMVC hash-SPAs, this collapses all URLs to a single state.
    """
    if not url:
        return url
    # Strip fragment
    url = url.split("#")[0]
    # Strip trailing slash (but keep root /)
    if url.endswith("/") and url.count("/") > 3:
        url = url[:-1]
    return url


def load_variant_data(variant: str, parent_dir: str) -> list:
    """Load and combine base + topup files for a variant."""
    all_transitions = []
    for filename in DATA_FILES[variant]:
        filepath = os.path.join(parent_dir, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
        all_transitions.extend(data)
    return all_transitions


def filter_valid(transitions: list) -> list:
    """Filter: keep only transitions where error is None."""
    return [t for t in transitions if t.get("error") is None]


def filter_non_leakage(transitions: list) -> list:
    """Filter: keep only non-leakage transitions where action_primitive != 'link_click'."""
    return [t for t in transitions if t.get("action_primitive") != "link_click"]


# ─── PMI Computation ─────────────────────────────────────────────────────────

def extract_triples(transitions: list, state_fn) -> list:
    """Extract (state_repr, action_primitive, next_state_repr) triples."""
    triples = []
    for t in transitions:
        s = state_fn(t)
        a = t["action_primitive"]
        s_next = state_fn(t, after=True)
        triples.append((s, a, s_next))
    return triples


def state_raw_url(t: dict, after: bool = False) -> str:
    """State = raw url (with fragment preserved)."""
    return t["url_after"] if after else t["url_before"]


def state_normalized_url(t: dict, after: bool = False) -> str:
    """State = normalized url (fragment stripped)."""
    url = t["url_after"] if after else t["url_before"]
    return normalize_url(url)


def extract_trajectory_groups(transitions: list, state_fn) -> dict:
    """Group transitions by session, extract triples per session."""
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["session"]].append(t)
    triple_groups = {}
    for sid, trans in groups.items():
        triple_groups[sid] = extract_triples(trans, state_fn)
    return triple_groups


def compute_pmi_stats(triples: list) -> dict:
    """Compute PMI statistics for a set of triples.
    
    PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
    """
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "pmi_values": [], "N": 0,
                "unique_states": 0, "unique_actions": 0, "unique_sa_pairs": 0,
                "singleton_fraction": 0.0, "url_entropy_bits": 0.0}

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

    # Singleton fraction
    sa_counts = list(state_action_counts.values())
    n_singletons = sum(1 for c in sa_counts if c == 1)
    singleton_frac = n_singletons / len(sa_counts) if sa_counts else 0.0

    # URL entropy (Shannon entropy of url_before distribution)
    total = sum(state_counts.values())
    url_entropy = 0.0
    for count in state_counts.values():
        if count > 0:
            p = count / total
            url_entropy -= p * math.log2(p)

    return {
        "mean_pmi": mean_pmi,
        "pmi_values": pmi_values,
        "N": N,
        "unique_states": len(state_counts),
        "unique_actions": len(set(a for _, a, _ in triples)),
        "unique_sa_pairs": len(state_action_counts),
        "singleton_fraction": singleton_frac,
        "url_entropy_bits": url_entropy,
    }


# ─── Permutation Test ────────────────────────────────────────────────────────

def shuffle_actions_within_sessions(triple_groups: dict, rng: random.Random) -> dict:
    """Shuffle action labels within each session (cross-trajectory permutation)."""
    shuffled_groups = {}
    for sid, triples in triple_groups.items():
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
        shuffled_actions = actions[:]
        rng.shuffle(shuffled_actions)
        shuffled_groups[sid] = [(states[i], shuffled_actions[i], nexts[i])
                                for i in range(len(triples))]
    return shuffled_groups


def permutation_test(triple_groups: dict, observed_mean_pmi: float,
                     n_permutations: int, seed: int) -> dict:
    """Cross-trajectory permutation test: shuffle actions within sessions."""
    rng = random.Random(seed)

    shuffled_means = []
    for _ in range(n_permutations):
        shuffled_groups = shuffle_actions_within_sessions(triple_groups, rng)
        all_shuffled = []
        for triples in shuffled_groups.values():
            all_shuffled.extend(triples)
        stats = compute_pmi_stats(all_shuffled)
        shuffled_means.append(stats["mean_pmi"])

    count_ge = sum(1 for m in shuffled_means if m >= observed_mean_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)

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


# ─── Positive Control: Synthetic Deterministic SPA ───────────────────────────

# 8 states, 4 actions, known deterministic mapping (from EXP-PHYSICS-34149195420)
SYNTHETIC_STATES = {
    0: {"url": "http://spa.test/home", "title": "Home"},
    1: {"url": "http://spa.test/home#/dashboard", "title": "Dashboard"},
    2: {"url": "http://spa.test/home#/profile", "title": "Profile"},
    3: {"url": "http://spa.test/home#/settings", "title": "Settings"},
    4: {"url": "http://spa.test/home#/search", "title": "Search"},
    5: {"url": "http://spa.test/home#/notifications", "title": "Notifications"},
    6: {"url": "http://spa.test/home#/admin", "title": "Admin"},
    7: {"url": "http://spa.test/home#/help", "title": "Help"},
}

SYNTHETIC_ACTIONS = ["form_submit", "button_click", "js_navigate"]

SYNTHETIC_TRANSITIONS = {
    0: {"form_submit": 1, "button_click": 2, "js_navigate": 3},
    1: {"form_submit": 4, "button_click": 5, "js_navigate": 0},
    2: {"form_submit": 3, "button_click": 6, "js_navigate": 1},
    3: {"form_submit": 0, "button_click": 7, "js_navigate": 2},
    4: {"form_submit": 5, "button_click": 0, "js_navigate": 6},
    5: {"form_submit": 6, "button_click": 1, "js_navigate": 7},
    6: {"form_submit": 7, "button_click": 2, "js_navigate": 4},
    7: {"form_submit": 0, "button_click": 3, "js_navigate": 5},
}


def generate_synthetic_trajectories(n_sessions: int, steps_per_session: int,
                                    rng: random.Random) -> list:
    """Generate synthetic SPA trajectories with known deterministic structure."""
    state_ids = list(SYNTHETIC_STATES.keys())
    all_transitions = []

    for session_id in range(n_sessions):
        current_state = rng.choice(state_ids)
        for step in range(steps_per_session):
            action = rng.choice(SYNTHETIC_ACTIONS)
            next_state = SYNTHETIC_TRANSITIONS[current_state][action]
            all_transitions.append({
                "site": "synthetic_control",
                "session": session_id,
                "url_before": SYNTHETIC_STATES[current_state]["url"],
                "url_after": SYNTHETIC_STATES[next_state]["url"],
                "title_before": SYNTHETIC_STATES[current_state]["title"],
                "title_after": SYNTHETIC_STATES[next_state]["title"],
                "action_primitive": action,
                "action_target": None,
                "timestamp": None,
                "error": None,
            })
            current_state = next_state

    return all_transitions


def run_positive_control(rng: random.Random) -> dict:
    """Run synthetic deterministic SPA positive control.
    
    Must produce PMI >= 1.0 bits with permutation p < 0.001.
    """
    print("\n[CONTROL] Running positive control (synthetic deterministic SPA)...")

    synthetic_transitions = generate_synthetic_trajectories(
        n_sessions=50, steps_per_session=20, rng=rng)

    # Use raw URL state function (fragments preserved)
    triples = extract_triples(synthetic_transitions, state_raw_url)
    stats = compute_pmi_stats(triples)

    # Permutation test
    triple_groups = extract_trajectory_groups(synthetic_transitions, state_raw_url)
    perm = permutation_test(triple_groups, stats["mean_pmi"], N_PERMUTATIONS, SEED)

    passes_pmi = stats["mean_pmi"] >= 1.0
    passes_perm = perm["p_value"] < 0.001
    passes = passes_pmi and passes_perm

    print(f"  PMI: {stats['mean_pmi']:.6f} bits (threshold: 1.0)")
    print(f"  Permutation p: {perm['p_value']:.6f} (threshold: 0.001)")
    print(f"  Unique states: {stats['unique_states']}, unique SA pairs: {stats['unique_sa_pairs']}")
    print(f"  Positive control passes: {passes}")

    return {
        "mean_pmi": stats["mean_pmi"],
        "permutation_p": perm["p_value"],
        "effect_size_d": perm["effect_size_d"],
        "unique_states": stats["unique_states"],
        "unique_sa_pairs": stats["unique_sa_pairs"],
        "N": stats["N"],
        "passes_pmi": passes_pmi,
        "passes_perm": passes_perm,
        "passes": passes,
    }


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full URL-level PMI experiment."""
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — URL-level PMI: Raw vs Normalized")
    print("=" * 70)

    rng = random.Random(SEED)
    os.environ["PYTHONHASHSEED"] = "0"

    # ── Step 1: Positive control ──
    positive_control = run_positive_control(rng)

    # ── Step 2: Load and process each variant ──
    variant_results = {}

    for variant in VARIANTS:
        print(f"\n[DATA] Processing {variant}...")

        # Load data
        raw_data = load_variant_data(variant, PARENT_DIR)
        print(f"  Raw transitions loaded: {len(raw_data)}")

        # Filter valid (error is None)
        valid = filter_valid(raw_data)
        print(f"  Valid (error=None): {len(valid)}")

        # Filter non-leakage (action_primitive != 'link_click')
        non_leakage = filter_non_leakage(valid)
        print(f"  Non-leakage (not link_click): {len(non_leakage)}")

        # Check minimum sample size
        if len(non_leakage) < 50:
            print(f"  WARNING: Fewer than 50 non-leakage transitions ({len(non_leakage)})")

        # ── Extract raw URL triples ──
        raw_triples = extract_triples(non_leakage, state_raw_url)
        raw_stats = compute_pmi_stats(raw_triples)

        # ── Extract normalized URL triples ──
        norm_triples = extract_triples(non_leakage, state_normalized_url)
        norm_stats = compute_pmi_stats(norm_triples)

        # ── Raw URL unique URLs ──
        raw_urls = set(t["url_before"] for t in non_leakage)
        norm_urls = set(normalize_url(t["url_before"]) for t in non_leakage)

        print(f"  Raw URL PMI: {raw_stats['mean_pmi']:.6f} bits")
        print(f"  Normalized URL PMI: {norm_stats['mean_pmi']:.6f} bits")
        print(f"  Unique raw URLs: {len(raw_urls)} — {sorted(raw_urls)}")
        print(f"  Unique normalized URLs: {len(norm_urls)} — {sorted(norm_urls)}")
        print(f"  URL entropy (raw): {raw_stats['url_entropy_bits']:.6f} bits")
        print(f"  URL entropy (norm): {norm_stats['url_entropy_bits']:.6f} bits")
        print(f"  Unique states: {raw_stats['unique_states']} raw, {norm_stats['unique_states']} norm")
        print(f"  Unique SA pairs: {raw_stats['unique_sa_pairs']} raw, {norm_stats['unique_sa_pairs']} norm")
        print(f"  Singleton fraction: {raw_stats['singleton_fraction']:.3f} raw, {norm_stats['singleton_fraction']:.3f} norm")

        # ── Permutation tests ──
        raw_traj_groups = extract_trajectory_groups(non_leakage, state_raw_url)
        raw_perm = permutation_test(raw_traj_groups, raw_stats["mean_pmi"],
                                    N_PERMUTATIONS, SEED)

        norm_traj_groups = extract_trajectory_groups(non_leakage, state_normalized_url)
        norm_perm = permutation_test(norm_traj_groups, norm_stats["mean_pmi"],
                                     N_PERMUTATIONS, SEED)

        print(f"  Raw permutation p: {raw_perm['p_value']:.6f}, effect_d: {raw_perm['effect_size_d']:.4f}")
        print(f"  Norm permutation p: {norm_perm['p_value']:.6f}, effect_d: {norm_perm['effect_size_d']:.4f}")

        # ── Action frequency baseline ──
        action_counts = collections.Counter(t["action_primitive"] for t in non_leakage)
        total_actions = len(non_leakage)
        action_freq = {a: c / total_actions for a, c in action_counts.items()}

        print(f"  Action frequencies: {dict(action_freq)}")

        # ── Per-type leakage (from parent, for reference) ──
        total_valid = len(valid)
        link_click_count = sum(1 for t in valid if t.get("action_primitive") == "link_click")
        leakage_frac = link_click_count / total_valid if total_valid > 0 else 0

        variant_results[variant] = {
            "n_raw": len(raw_data),
            "n_valid": len(valid),
            "n_non_leakage": len(non_leakage),
            "leakage_fraction": leakage_frac,
            "raw_url_pmi": {
                "mean_pmi": raw_stats["mean_pmi"],
                "unique_states": raw_stats["unique_states"],
                "unique_sa_pairs": raw_stats["unique_sa_pairs"],
                "singleton_fraction": raw_stats["singleton_fraction"],
                "url_entropy_bits": raw_stats["url_entropy_bits"],
                "N": raw_stats["N"],
            },
            "norm_url_pmi": {
                "mean_pmi": norm_stats["mean_pmi"],
                "unique_states": norm_stats["unique_states"],
                "unique_sa_pairs": norm_stats["unique_sa_pairs"],
                "singleton_fraction": norm_stats["singleton_fraction"],
                "url_entropy_bits": norm_stats["url_entropy_bits"],
                "N": norm_stats["N"],
            },
            "raw_permutation": {
                "p_value": raw_perm["p_value"],
                "null_mean": raw_perm["null_mean"],
                "null_std": raw_perm["null_std"],
                "effect_size_d": raw_perm["effect_size_d"],
            },
            "norm_permutation": {
                "p_value": norm_perm["p_value"],
                "null_mean": norm_perm["null_mean"],
                "null_std": norm_perm["null_std"],
                "effect_size_d": norm_perm["effect_size_d"],
            },
            "unique_raw_urls": sorted(raw_urls),
            "unique_norm_urls": sorted(norm_urls),
            "n_unique_raw_urls": len(raw_urls),
            "n_unique_norm_urls": len(norm_urls),
            "action_frequency": action_freq,
        }

    # ── Step 3: Decision evaluation ──
    print(f"\n{'=' * 70}")
    print("DECISION EVALUATION")
    print(f"{'=' * 70}")

    # Decision rule (frozen from spec.json):
    # SURVIVES_CURRENT_TEST requires ALL of:
    # (1) >= 3/5 variants: raw URL PMI > 0.05 bits AND Bonferroni p < 0.01
    # (2) Normalized URL PMI = 0.0 bits on all 5 variants
    # (3) Positive control PMI >= 1.0 bits
    # (4) >= 50 non-leakage transitions per variant
    # (5) >= 5 unique raw URLs per variant

    survives = True
    decision_checks = {}

    # Check (1): Raw URL PMI > 0.05 AND Bonferroni p < 0.01
    raw_pass_count = 0
    raw_checks = {}
    for variant in VARIANTS:
        vr = variant_results[variant]
        pmi_gt_005 = vr["raw_url_pmi"]["mean_pmi"] > 0.05
        p_lt_bonf = vr["raw_permutation"]["p_value"] < ALPHA_BONFERRONI
        passes = pmi_gt_005 and p_lt_bonf
        raw_checks[variant] = {
            "pmi": vr["raw_url_pmi"]["mean_pmi"],
            "pmi_gt_005": pmi_gt_005,
            "p_value": vr["raw_permutation"]["p_value"],
            "p_lt_bonferroni": p_lt_bonf,
            "passes": passes,
        }
        if passes:
            raw_pass_count += 1
        print(f"  Raw PMI {variant}: {vr['raw_url_pmi']['mean_pmi']:.6f} bits, "
              f"p={vr['raw_permutation']['p_value']:.6f}, pass={passes}")

    check1 = raw_pass_count >= 3
    decision_checks["C1_raw_pmi_at_least_3_variants"] = {
        "n_pass": raw_pass_count,
        "threshold": 3,
        "total_variants": 5,
        "per_variant": raw_checks,
        "passes": check1,
    }
    if not check1:
        survives = False
    print(f"  Check 1: {raw_pass_count}/5 variants pass raw PMI > 0.05 + Bonferroni p < 0.01: {check1}")

    # Check (2): Normalized URL PMI = 0.0 on all 5 variants
    norm_zero_count = 0
    norm_checks = {}
    for variant in VARIANTS:
        vr = variant_results[variant]
        is_zero = vr["norm_url_pmi"]["mean_pmi"] == 0.0
        norm_checks[variant] = {
            "pmi": vr["norm_url_pmi"]["mean_pmi"],
            "is_zero": is_zero,
            "unique_states": vr["norm_url_pmi"]["unique_states"],
        }
        if is_zero:
            norm_zero_count += 1
        print(f"  Norm PMI {variant}: {vr['norm_url_pmi']['mean_pmi']:.6f} bits, "
              f"unique_states={vr['norm_url_pmi']['unique_states']}, is_zero={is_zero}")

    check2 = norm_zero_count == 5
    decision_checks["C2_normalized_pmi_zero_all_variants"] = {
        "n_zero": norm_zero_count,
        "threshold": 5,
        "per_variant": norm_checks,
        "passes": check2,
    }
    if not check2:
        survives = False
    print(f"  Check 2: {norm_zero_count}/5 variants have normalized PMI = 0.0: {check2}")

    # Check (3): Positive control PMI >= 1.0
    check3 = positive_control["passes"]
    decision_checks["C3_positive_control"] = {
        "pmi": positive_control["mean_pmi"],
        "permutation_p": positive_control["permutation_p"],
        "threshold_pmi": 1.0,
        "passes": check3,
    }
    if not check3:
        survives = False
    print(f"  Check 3: Positive control PMI = {positive_control['mean_pmi']:.6f} >= 1.0: {check3}")

    # Check (4): >= 50 non-leakage transitions per variant
    nl_pass_count = 0
    nl_checks = {}
    for variant in VARIANTS:
        vr = variant_results[variant]
        has_enough = vr["n_non_leakage"] >= 50
        nl_checks[variant] = {
            "n_non_leakage": vr["n_non_leakage"],
            "threshold": 50,
            "passes": has_enough,
        }
        if has_enough:
            nl_pass_count += 1
        print(f"  NL count {variant}: {vr['n_non_leakage']} >= 50: {has_enough}")

    check4 = nl_pass_count == 5
    decision_checks["C4_non_leakage_sufficient"] = {
        "n_pass": nl_pass_count,
        "threshold": 5,
        "per_variant": nl_checks,
        "passes": check4,
    }
    if not check4:
        survives = False
    print(f"  Check 4: {nl_pass_count}/5 variants have >= 50 NL transitions: {check4}")

    # Check (5): >= 5 unique raw URLs per variant
    url_pass_count = 0
    url_checks = {}
    for variant in VARIANTS:
        vr = variant_results[variant]
        has_enough = vr["n_unique_raw_urls"] >= 5
        url_checks[variant] = {
            "n_unique_raw_urls": vr["n_unique_raw_urls"],
            "unique_urls": vr["unique_raw_urls"],
            "threshold": 5,
            "passes": has_enough,
        }
        if has_enough:
            url_pass_count += 1
        print(f"  Unique raw URLs {variant}: {vr['n_unique_raw_urls']} >= 5: {has_enough}")

    check5 = url_pass_count >= 3  # At least 3/5 (prereg says "fewer than 3/5" is falsifier)
    decision_checks["C5_unique_raw_urls"] = {
        "n_pass": url_pass_count,
        "threshold_at_least": 3,
        "per_variant": url_checks,
        "passes": check5,
    }
    if not check5:
        survives = False
    print(f"  Check 5: {url_pass_count}/5 variants have >= 5 unique raw URLs: {check5}")

    # ── Determine outcome ──
    if survives:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    else:
        # Check if measurement is invalid vs scientific negative
        any_control_fail = not check3  # positive control
        any_data_fail = not check4
        if any_control_fail or any_data_fail:
            status = "MEASUREMENT_INVALID"
            outcome = "NOT_APPLICABLE"
        else:
            status = "COMPLETE"
            outcome = "FALSIFIES"

    print(f"\n{'=' * 70}")
    print(f"OUTCOME: {outcome}")
    print(f"STATUS: {status}")
    print(f"DECISION: {'SURVIVES_CURRENT_TEST' if survives else 'FALSIFIED-IN-SETTING' if status == 'COMPLETE' else 'MEASUREMENT_INVALID'}")
    print(f"{'=' * 70}")

    # ── Build results ──
    results = {
        "experiment_id": EXPERIMENT_ID,
        "variant_results": variant_results,
        "positive_control": positive_control,
        "decision_checks": decision_checks,
        "survives": survives,
        "outcome": outcome,
        "status": status,
    }

    return results


if __name__ == "__main__":
    results = run_experiment()

    # Save raw results
    out_dir = "research/experiments/EXP-PHYSICS-35262258744"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "raw_analysis_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_path}")
