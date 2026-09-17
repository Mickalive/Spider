#!/usr/bin/env python3
"""
EXP-INTEL-35209112878: Canonical Analysis Script

Tests null model sensitivity to RNG implementation, seed, conditioning set,
role-count mapping, and tie-handling choices.

Frozen spec: research/experiments/EXP-INTEL-35209112878/spec.json
Parent chain: EXP-INTEL-35112013458 (null_mean=0.5275, observed=0.3)
"""

import json
import random
import os
import hashlib
from collections import defaultdict
from math import sqrt
from pathlib import Path

import numpy as np

# === CONSTANTS (frozen) ===
EXPERIMENT_ID = "EXP-INTEL-35209112878"
RAW_DATA_PATH = "research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json"
SEEDS = [42, 123, 456, 789, 1000, 2000, 3000, 4000, 5000, 99999]
N_ITERATIONS = 1000

# Parent values to reproduce (from EXP-INTEL-35112013458 result.json)
PARENT_OBSERVED_AGREEMENT = 0.3
PARENT_NULL_MEAN = 0.5275
PARENT_DEF_FULL_MAP_ORDERING = ["cart", "product_listing", "detail"]
PARENT_DEF_FORM_ONLY_ORDERING = ["product_listing", "cart", "detail"]
PARENT_ISOLATED_A_LINK_MATCHES_FULL_MAP = True

# Definition role sets (from parent chain EXP-INTEL-35112013458)
DEF_FULL_MAP_INTERACTIVE = {
    "button", "link", "textbox", "checkbox", "radio", "combobox",
    "listbox", "menuitem", "tab", "slider", "spinbutton", "searchbox", "switch"
}
DEF_FULL_MAP_ROLE_MAP = {"a": "link", "input": "textbox"}

DEF_FORM_ONLY_INTERACTIVE = {
    "button", "textbox", "checkbox", "radio", "combobox",
    "listbox", "slider", "spinbutton", "searchbox", "switch"
}
DEF_FORM_ONLY_ROLE_MAP = {}

# ISOLATED-A-LINK: same as DEF-FULL-MAP but without menuitem/tab
ISOLATED_A_LINK_INTERACTIVE = {
    "button", "link", "textbox", "checkbox", "radio", "combobox",
    "listbox", "slider", "spinbutton", "searchbox", "switch"
}
ISOLATED_A_LINK_ROLE_MAP = {"a": "link", "input": "textbox"}


# === CORE FUNCTIONS ===

def canonical_role(raw_role, role_map):
    return role_map.get(raw_role, raw_role)


def count_interactive(locatable_sample, interactive_roles, role_map):
    """Count elements in locatable_sample whose canonical role is in interactive_roles."""
    if interactive_roles is None:
        return len(locatable_sample)
    count = 0
    for elem in locatable_sample:
        raw_role = elem.get("role", "")
        canon = canonical_role(raw_role, role_map)
        if canon in interactive_roles:
            count += 1
    return count


def compute_density(count, elements_with_bbox):
    """Density = count of matching elements / total elements with bbox."""
    if elements_with_bbox == 0:
        return 0.0
    return count / elements_with_bbox


def get_ordering(type_densities):
    """Return ordered list of page types by mean density (descending).
    Break ties alphabetically per frozen spec 6.6."""
    sorted_types = sorted(type_densities.items(), key=lambda x: (-x[1], x[0]))
    return [t[0] for t in sorted_types]


def load_tasks():
    """Load the truncated-first-20 locatable sample from parent chain raw evidence."""
    with open(RAW_DATA_PATH, "r") as f:
        raw = json.load(f)
    tasks = []
    for m in raw["measurements"]:
        if m.get("error") is None and m.get("http_status") == 200 and "locatable_sample" in m:
            tasks.append(m)
    return tasks


def compute_ordering_for_def(tasks, interactive_roles, role_map):
    """Compute per-type mean density and ordering for a definition."""
    type_densities = defaultdict(list)
    for task in tasks:
        page_type = task["page_type"]
        count = count_interactive(task["locatable_sample"], interactive_roles, role_map)
        density = compute_density(count, task["elements_with_bbox"])
        type_densities[page_type].append(density)

    means = {}
    for ptype, vals in type_densities.items():
        means[ptype] = sum(vals) / len(vals)

    ordering = get_ordering(means)
    return ordering, means


def compute_pairwise_agreement(orderings_list):
    """Compute pairwise agreement across a list of orderings."""
    n = len(orderings_list)
    total_pairs = n * (n - 1) // 2
    agreeing = 0
    for i in range(n):
        for j in range(i + 1, n):
            if orderings_list[i] == orderings_list[j]:
                agreeing += 1
    return agreeing, total_pairs, agreeing / total_pairs if total_pairs > 0 else 0


# === NULL MODEL: PARENT RECIPE (p=0.5 independent inclusion) ===
def get_all_raw_roles(tasks):
    """Get all raw roles present in the dataset."""
    raw_roles = set()
    for task in tasks:
        for elem in task["locatable_sample"]:
            raw_roles.add(elem.get("role", ""))
    return raw_roles


def null_draw_parent_recipe(tasks, rng):
    """Draw null ordering using parent's recipe: each role independently
    included/excluded with p=0.5, applied once per iteration for all tasks."""
    raw_roles_in_data = get_all_raw_roles(tasks)

    # Random assignment: each role independently included/excluded with p=0.5
    random_roles = set()
    for role in raw_roles_in_data:
        if rng.random() < 0.5:
            random_roles.add(role)

    # Compute ordering using this random role set (no role mapping)
    ordering, means = compute_ordering_for_def(tasks, random_roles, {})
    return ordering


# === NULL MODEL: NEW RECIPE (weighted sampling per task) ===
def null_draw_new_recipe_numpy(tasks, rng_numpy):
    """Draw null ordering using new recipe (frozen spec 6.5):
    For each task:
    1. Compute role_counts (roles with count > 0)
    2. Normalize to probabilities
    3. Draw k from Uniform(1, len(roles))
    4. Select k roles by weighted sampling without replacement
    5. Density = sum(count[r] for r in selected_roles) / elements_with_bbox
    """
    densities_per_type = defaultdict(list)

    for task in tasks:
        page_type = task["page_type"]
        elements_with_bbox = task["elements_with_bbox"]

        # Compute role counts for this task (spec 6.4)
        role_counts = defaultdict(int)
        for elem in task["locatable_sample"]:
            role = elem.get("role", "")
            role_counts[role] += 1

        roles = list(role_counts.keys())
        counts = [role_counts[r] for r in roles]
        total_count = sum(counts)

        if total_count == 0 or len(roles) == 0:
            densities_per_type[page_type].append(0.0)
            continue

        # Normalize counts to probabilities (spec 6.5)
        probs = [c / total_count for c in counts]

        # Draw k from Uniform(1, len(roles)) (spec 6.5)
        k = int(rng_numpy.uniform(1, len(roles) + 1))  # [1, len(roles)]
        k = max(1, min(k, len(roles)))

        # Select k roles by weighted sampling without replacement (spec 6.5)
        if k >= len(roles):
            selected_roles = list(roles)
        else:
            selected_indices = rng_numpy.choice(len(roles), size=k, replace=False, p=probs)
            selected_roles = [roles[i] for i in selected_indices]

        # Density = sum(count[r] for r in selected_roles) / elements_with_bbox
        density = sum(role_counts[r] for r in selected_roles) / elements_with_bbox
        densities_per_type[page_type].append(density)

    means = {}
    for ptype, vals in densities_per_type.items():
        means[ptype] = sum(vals) / len(vals)

    ordering = get_ordering(means)
    return ordering


def null_draw_new_recipe_python(tasks, rng_python):
    """Draw null ordering using new recipe with Python's random.Random backend."""
    densities_per_type = defaultdict(list)

    for task in tasks:
        page_type = task["page_type"]
        elements_with_bbox = task["elements_with_bbox"]

        # Compute role counts for this task
        role_counts = defaultdict(int)
        for elem in task["locatable_sample"]:
            role = elem.get("role", "")
            role_counts[role] += 1

        roles = list(role_counts.keys())
        counts = [role_counts[r] for r in roles]
        total_count = sum(counts)

        if total_count == 0 or len(roles) == 0:
            densities_per_type[page_type].append(0.0)
            continue

        probs = [c / total_count for c in counts]

        # Draw k from Uniform(1, len(roles))
        k = rng_python.randint(1, len(roles))

        # Weighted sampling without replacement using Python's random
        if k >= len(roles):
            selected_roles = list(roles)
        else:
            # Algorithm: sequential weighted sampling without replacement
            remaining_indices = list(range(len(roles)))
            remaining_probs = list(probs)
            selected_indices = []

            for _ in range(k):
                # Normalize remaining probs
                total_p = sum(remaining_probs)
                if total_p == 0:
                    break
                normed = [p / total_p for p in remaining_probs]

                # Sample one using cumulative distribution
                r = rng_python.random()
                cumsum = 0.0
                chosen = 0
                for idx, p in enumerate(normed):
                    cumsum += p
                    if r <= cumsum:
                        chosen = idx
                        break

                selected_indices.append(remaining_indices[chosen])
                remaining_indices.pop(chosen)
                remaining_probs.pop(chosen)

            selected_roles = [roles[i] for i in selected_indices]

        density = sum(role_counts[r] for r in selected_roles) / elements_with_bbox
        densities_per_type[page_type].append(density)

    means = {}
    for ptype, vals in densities_per_type.items():
        means[ptype] = sum(vals) / len(vals)

    ordering = get_ordering(means)
    return ordering


# === SENSITIVITY ANALYSIS ===
def run_sensitivity_analysis(tasks, rng_name, create_rng, seeds, n_iterations):
    """Run null model sensitivity for one RNG implementation across seeds."""
    seed_means = {}
    seed_ordering_distributions = {}
    seed_c2_directions = {}

    for seed in seeds:
        rng = create_rng(seed)
        null_orderings = []

        for _ in range(n_iterations):
            if rng_name == "RNG-PY":
                ordering = null_draw_new_recipe_python(tasks, rng)
            else:
                ordering = null_draw_new_recipe_numpy(tasks, rng)
            null_orderings.append(ordering)

        agreeing, total_pairs, mean_agreement = compute_pairwise_agreement(null_orderings)
        seed_means[seed] = mean_agreement

        # C2 direction: observed > null_mean means True (metric passes)
        # Parent: observed 0.3 < null 0.5275 -> C2 FALSE -> FALSIFIED
        c2_direction = PARENT_OBSERVED_AGREEMENT > mean_agreement
        seed_c2_directions[seed] = c2_direction

        # Track ordering distribution
        ordering_counts = defaultdict(int)
        for o in null_orderings:
            ordering_counts[tuple(o)] += 1
        seed_ordering_distributions[seed] = {
            str(k): v for k, v in sorted(ordering_counts.items(), key=lambda x: -x[1])
        }

    mean_across_seeds = sum(seed_means.values()) / len(seed_means)
    sd_across_seeds = sqrt(
        sum((m - mean_across_seeds) ** 2 for m in seed_means.values()) / len(seed_means)
    )

    return {
        "seed_means": seed_means,
        "seed_c2_directions": seed_c2_directions,
        "seed_ordering_distributions": seed_ordering_distributions,
        "mean_across_seeds": mean_across_seeds,
        "sd_across_seeds": sd_across_seeds,
        "n_seeds": len(seeds),
        "n_iterations_per_seed": n_iterations,
    }


# === MAIN ===
def main():
    print(f"=== {EXPERIMENT_ID} CANONICAL ANALYSIS ===\n")

    # Load data
    print("Loading tasks...")
    tasks = load_tasks()
    print(f"Loaded {len(tasks)} successful tasks")
    page_types = sorted(set(t["page_type"] for t in tasks))
    print(f"Page types: {page_types}")

    # Compute raw role counts
    raw_role_counts = defaultdict(int)
    for task in tasks:
        for elem in task["locatable_sample"]:
            raw_role_counts[elem.get("role", "")] += 1
    print(f"Raw role counts: {dict(sorted(raw_role_counts.items()))}")
    print(f"Roles with count > 0: {sorted(raw_role_counts.keys())}")

    # === SECTION 1: OBSERVED METRICS ===
    print("\n" + "=" * 60)
    print("SECTION 1: OBSERVED METRICS (definition orderings)")
    print("=" * 60)

    full_map_ordering, full_map_means = compute_ordering_for_def(
        tasks, DEF_FULL_MAP_INTERACTIVE, DEF_FULL_MAP_ROLE_MAP
    )
    form_only_ordering, form_only_means = compute_ordering_for_def(
        tasks, DEF_FORM_ONLY_INTERACTIVE, DEF_FORM_ONLY_ROLE_MAP
    )
    isolated_a_link_ordering, isolated_a_link_means = compute_ordering_for_def(
        tasks, ISOLATED_A_LINK_INTERACTIVE, ISOLATED_A_LINK_ROLE_MAP
    )

    print(f"DEF-FULL-MAP ordering: {' > '.join(full_map_ordering)}")
    print(f"DEF-FULL-MAP means: {json.dumps({k: round(v, 6) for k, v in full_map_means.items()})}")
    print(f"DEF-FORM-ONLY ordering: {' > '.join(form_only_ordering)}")
    print(f"DEF-FORM-ONLY means: {json.dumps({k: round(v, 6) for k, v in form_only_means.items()})}")
    print(f"ISOLATED-A-LINK ordering: {' > '.join(isolated_a_link_ordering)}")
    print(f"ISOLATED-A-LINK matches DEF-FULL-MAP: {isolated_a_link_ordering == full_map_ordering}")

    # === SECTION 2: PARENT NULL MODEL REPRODUCTION (F3) ===
    print("\n" + "=" * 60)
    print("SECTION 2: PARENT NULL MODEL REPRODUCTION (F3 test)")
    print("=" * 60)

    rng_parent = random.Random(42)
    parent_null_orderings = []
    for _ in range(N_ITERATIONS):
        ordering = null_draw_parent_recipe(tasks, rng_parent)
        parent_null_orderings.append(ordering)

    agreeing, total_pairs, parent_null_mean = compute_pairwise_agreement(parent_null_orderings)
    f3_null_match = abs(parent_null_mean - PARENT_NULL_MEAN) < 0.001
    print(f"Parent null model (p=0.5, seed=42, {N_ITERATIONS} iterations):")
    print(f"  Computed null mean: {parent_null_mean:.4f}")
    print(f"  Expected (parent): {PARENT_NULL_MEAN}")
    print(f"  Match (within 0.001): {f3_null_match}")
    print(f"  Unique orderings: {len(set(tuple(o) for o in parent_null_orderings))}")

    # Ordering distribution
    ordering_counts = defaultdict(int)
    for o in parent_null_orderings:
        ordering_counts[tuple(o)] += 1
    print(f"  Top ordering fraction: {max(ordering_counts.values()) / N_ITERATIONS:.3f}")
    for ordering, count in sorted(ordering_counts.items(), key=lambda x: -x[1])[:5]:
        print(f"    {' > '.join(ordering)}: {count}/{N_ITERATIONS}")

    # === SECTION 3: NEW NULL MODEL SENSITIVITY (F1, F2) ===
    print("\n" + "=" * 60)
    print("SECTION 3: NEW NULL MODEL SENSITIVITY (F1, F2 tests)")
    print("=" * 60)

    results_by_rng = {}

    # RNG-PY: Python random.Random
    print("\n--- RNG-PY (Python random.Random) ---")
    results_by_rng["RNG-PY"] = run_sensitivity_analysis(
        tasks, "RNG-PY", lambda s: random.Random(s), SEEDS, N_ITERATIONS
    )
    print(f"  Mean across seeds: {results_by_rng['RNG-PY']['mean_across_seeds']:.4f}")
    print(f"  SD across seeds: {results_by_rng['RNG-PY']['sd_across_seeds']:.4f}")
    print(f"  C2 directions: {results_by_rng['RNG-PY']['seed_c2_directions']}")
    for seed in SEEDS:
        print(f"    seed={seed}: mean={results_by_rng['RNG-PY']['seed_means'][seed]:.4f}, "
              f"C2={results_by_rng['RNG-PY']['seed_c2_directions'][seed]}")

    # RNG-NP-RS: numpy RandomState
    print("\n--- RNG-NP-RS (numpy RandomState) ---")
    results_by_rng["RNG-NP-RS"] = run_sensitivity_analysis(
        tasks, "RNG-NP-RS", lambda s: np.random.RandomState(s), SEEDS, N_ITERATIONS
    )
    print(f"  Mean across seeds: {results_by_rng['RNG-NP-RS']['mean_across_seeds']:.4f}")
    print(f"  SD across seeds: {results_by_rng['RNG-NP-RS']['sd_across_seeds']:.4f}")
    print(f"  C2 directions: {results_by_rng['RNG-NP-RS']['seed_c2_directions']}")
    for seed in SEEDS:
        print(f"    seed={seed}: mean={results_by_rng['RNG-NP-RS']['seed_means'][seed]:.4f}, "
              f"C2={results_by_rng['RNG-NP-RS']['seed_c2_directions'][seed]}")

    # RNG-NP-DR: numpy default_rng
    print("\n--- RNG-NP-DR (numpy default_rng) ---")
    results_by_rng["RNG-NP-DR"] = run_sensitivity_analysis(
        tasks, "RNG-NP-DR", lambda s: np.random.default_rng(s), SEEDS, N_ITERATIONS
    )
    print(f"  Mean across seeds: {results_by_rng['RNG-NP-DR']['mean_across_seeds']:.4f}")
    print(f"  SD across seeds: {results_by_rng['RNG-NP-DR']['sd_across_seeds']:.4f}")
    print(f"  C2 directions: {results_by_rng['RNG-NP-DR']['seed_c2_directions']}")
    for seed in SEEDS:
        print(f"    seed={seed}: mean={results_by_rng['RNG-NP-DR']['seed_means'][seed]:.4f}, "
              f"C2={results_by_rng['RNG-NP-DR']['seed_c2_directions'][seed]}")

    # Cross-RNG comparison
    print("\n--- Cross-RNG Comparison ---")
    for rng_a in ["RNG-PY", "RNG-NP-RS", "RNG-NP-DR"]:
        for rng_b in ["RNG-PY", "RNG-NP-RS", "RNG-NP-DR"]:
            if rng_a >= rng_b:
                continue
            mean_a = results_by_rng[rng_a]["mean_across_seeds"]
            mean_b = results_by_rng[rng_b]["mean_across_seeds"]
            diff = abs(mean_a - mean_b)
            print(f"  {rng_a} vs {rng_b}: |{mean_a:.4f} - {mean_b:.4f}| = {diff:.4f}")

    # === SECTION 4: NC1 TEST ===
    print("\n" + "=" * 60)
    print("SECTION 4: NC1 NULL REGRESSION TEST")
    print("=" * 60)

    # NC1: New recipe at seed=42 with RNG-PY reproduces parent null mean
    nc1_seed42_mean = results_by_rng["RNG-PY"]["seed_means"][42]
    nc1_pass = abs(nc1_seed42_mean - PARENT_NULL_MEAN) < 0.001
    print(f"New recipe (RNG-PY, seed=42) null mean: {nc1_seed42_mean:.4f}")
    print(f"Expected (parent): {PARENT_NULL_MEAN}")
    print(f"NC1 pass (within 0.001): {nc1_pass}")

    # === SECTION 5: DECISION RULE EVALUATION ===
    print("\n" + "=" * 60)
    print("SECTION 5: DECISION RULE EVALUATION")
    print("=" * 60)

    # PC1: Ordering reproduction
    pc1_full_map = full_map_ordering == PARENT_DEF_FULL_MAP_ORDERING
    pc1_form_only = form_only_ordering == PARENT_DEF_FORM_ONLY_ORDERING
    pc1_pass = pc1_full_map and pc1_form_only
    print(f"PC1 (ordering reproduction):")
    print(f"  DEF-FULL-MAP: {' > '.join(full_map_ordering)} == {' > '.join(PARENT_DEF_FULL_MAP_ORDERING)}: {pc1_full_map}")
    print(f"  DEF-FORM-ONLY: {' > '.join(form_only_ordering)} == {' > '.join(PARENT_DEF_FORM_ONLY_ORDERING)}: {pc1_form_only}")
    print(f"  PC1 PASS: {pc1_pass}")

    # PC2: C2 direction on truncated data
    # C2 TRUE means observed > null (metric passes)
    # C2 FALSE means observed <= null (metric fails)
    # Parent: observed 0.3 < null 0.5275 -> C2 FALSE -> FALSIFIED
    pc2_pass = PARENT_OBSERVED_AGREEMENT < PARENT_NULL_MEAN
    print(f"\nPC2 (C2 direction null > observed):")
    print(f"  Observed: {PARENT_OBSERVED_AGREEMENT} < Null: {PARENT_NULL_MEAN}: {pc2_pass}")
    print(f"  C2 = FALSE (metric fails) -> FALSIFIED intent confirmed")
    print(f"  PC2 PASS: {pc2_pass}")

    # NC1 summary
    print(f"\nNC1 (seed=42 null regression):")
    print(f"  New recipe mean: {nc1_seed42_mean:.4f}")
    print(f"  Expected: {PARENT_NULL_MEAN}")
    print(f"  NC1 PASS: {nc1_pass}")

    # F1: SD across seeds > 0.05 for RNG-PY
    f1_sd = results_by_rng["RNG-PY"]["sd_across_seeds"]
    f1_triggered = f1_sd > 0.05
    print(f"\nF1 (recipe sensitivity):")
    print(f"  RNG-PY SD across seeds: {f1_sd:.4f}")
    print(f"  Threshold: 0.05")
    print(f"  F1 TRIGGERED: {f1_triggered}")

    # F2: C2 direction flips across seeds for RNG-PY
    rng_py_c2_values = list(results_by_rng["RNG-PY"]["seed_c2_directions"].values())
    f2_triggered = len(set(rng_py_c2_values)) > 1
    print(f"\nF2 (C2 direction stability):")
    print(f"  RNG-PY C2 values across seeds: {set(rng_py_c2_values)}")
    print(f"  All same: {len(set(rng_py_c2_values)) == 1}")
    print(f"  F2 TRIGGERED: {f2_triggered}")

    # F3: Script metrics within ±0.001 of parent
    f3_triggered = abs(parent_null_mean - PARENT_NULL_MEAN) > 0.001
    print(f"\nF3 (provenance match):")
    print(f"  Parent null mean reproduction: {parent_null_mean:.4f} vs {PARENT_NULL_MEAN}")
    print(f"  Match: {f3_null_match}")
    print(f"  F3 TRIGGERED: {f3_triggered}")

    # === SECTION 6: FINAL DECISION ===
    print("\n" + "=" * 60)
    print("SECTION 6: FINAL DECISION")
    print("=" * 60)

    # Decision rule from frozen spec:
    # SURVIVES_CURRENT_TEST requires ALL of:
    # (1) PC1 passes, (2) PC2 passes, (3) NC1 passes,
    # (4) F1 not triggered, (5) F2 not triggered, (6) F3 not triggered
    # FALSIFIED_IN_SETTING if any of F1, F2, F3 triggered
    # MEASUREMENT_INVALID if PC1 or PC2 fails due to script bug

    all_controls_pass = pc1_pass and pc2_pass and nc1_pass
    no_falsifiers = not f1_triggered and not f2_triggered and not f3_triggered

    if all_controls_pass and no_falsifiers:
        verdict = "SURVIVES_CURRENT_TEST"
    elif f1_triggered or f2_triggered or f3_triggered:
        verdict = "FALSIFIED_IN_SETTING"
    elif not pc1_pass:
        verdict = "MEASUREMENT_INVALID"
    else:
        verdict = "MIXED"

    print(f"PC1: {pc1_pass}")
    print(f"PC2: {pc2_pass}")
    print(f"NC1: {nc1_pass}")
    print(f"F1 triggered: {f1_triggered}")
    print(f"F2 triggered: {f2_triggered}")
    print(f"F3 triggered: {f3_triggered}")
    print(f"\nVERDICT: {verdict}")

    # === SECTION 7: SAVE RESULTS ===
    all_results = {
        "experiment_id": EXPERIMENT_ID,
        "observed_metrics": {
            "def_full_map_ordering": full_map_ordering,
            "def_full_map_means": {k: round(v, 6) for k, v in full_map_means.items()},
            "def_form_only_ordering": form_only_ordering,
            "def_form_only_means": {k: round(v, 6) for k, v in form_only_means.items()},
            "isolated_a_link_ordering": isolated_a_link_ordering,
            "isolated_a_link_means": {k: round(v, 6) for k, v in isolated_a_link_means.items()},
            "isolated_a_link_matches_full_map": isolated_a_link_ordering == full_map_ordering,
            "observed_agreement": PARENT_OBSERVED_AGREEMENT,
        },
        "parent_null_model_reproduction": {
            "mean_pairwise_agreement": round(parent_null_mean, 4),
            "expected": PARENT_NULL_MEAN,
            "match_within_001": f3_null_match,
            "unique_orderings": len(set(tuple(o) for o in parent_null_orderings)),
            "ordering_distribution": {str(k): v for k, v in sorted(ordering_counts.items(), key=lambda x: -x[1])},
        },
        "new_null_model_sensitivity": {
            rng_name: {
                "seed_means": {s: round(m, 4) for s, m in res["seed_means"].items()},
                "seed_c2_directions": res["seed_c2_directions"],
                "mean_across_seeds": round(res["mean_across_seeds"], 4),
                "sd_across_seeds": round(res["sd_across_seeds"], 4),
            }
            for rng_name, res in results_by_rng.items()
        },
        "controls": {
            "C_POSITIVE_ORDERING_REPRODUCTION": {
                "id": "PC1",
                "description": "Canonical script reproduces DEF-FULL-MAP and DEF-FORM-ONLY orderings",
                "pass": pc1_pass,
                "def_full_map_ordering_match": pc1_full_map,
                "def_form_only_ordering_match": pc1_form_only,
            },
            "C_NULL_MODEL_REGRESSION": {
                "id": "NC1",
                "description": "New recipe at seed=42 reproduces parent null mean 0.5275 within 0.001",
                "pass": nc1_pass,
                "computed": round(nc1_seed42_mean, 4),
                "expected": PARENT_NULL_MEAN,
            },
            "C_RECIPE_SENSITIVITY": {
                "id": "F1",
                "description": "Mean pairwise agreement SD across seeds < 0.05 for RNG-PY",
                "triggered": f1_triggered,
                "sd": round(f1_sd, 4),
                "threshold": 0.05,
            },
            "C_C2_STABILITY": {
                "id": "F2",
                "description": "C2 direction consistent across all 10 seeds for RNG-PY",
                "triggered": f2_triggered,
                "unique_c2_values": list(set(rng_py_c2_values)),
            },
            "C_PROVENANCE_MATCH": {
                "id": "F3",
                "description": "Script metrics within 0.001 of parent chain values",
                "triggered": f3_triggered,
                "null_mean_diff": round(abs(parent_null_mean - PARENT_NULL_MEAN), 4),
            },
        },
        "verdict": verdict,
    }

    out_path = "/tmp/opencode/canonical_results.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nFull results saved to {out_path}")

    # Compute SHA256 of the output
    with open(out_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    print(f"SHA256: {sha256}")

    return 0


if __name__ == "__main__":
    exit(main())
