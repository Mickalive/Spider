#!/usr/bin/env python3
"""
EXP-INTEL-35112013458 Analysis Script
Three null-model tests on truncated-sample pairwise ordering agreement:
1. Random ROLE_MAP null (1000 iterations, seed=42)
2. Single-role definitions (11 roles)
3. Isolated a→link definition (a→link without menuitem/tab)
"""

import json
import random
import os
from collections import defaultdict
from math import sqrt

# === CONSTANTS ===
RAW_DATA_PATH = "research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json"
SEED = 42
N_RANDOM_ITERATIONS = 1000

# Raw roles observed in the data
ALL_RAW_ROLES = {"a", "button", "combobox", "div", "form", "input", "label", "link", "menuitem", "span", "tab"}

# DEF-FULL-MAP definition (parent's with_map)
DEF_FULL_MAP = {
    "INTERACTIVE_ROLES": {"button", "link", "textbox", "checkbox", "radio", "combobox", "listbox", "menuitem", "tab", "slider", "spinbutton", "searchbox", "switch"},
    "ROLE_MAP": {"a": "link", "input": "textbox"}
}

# Parent's observed orderings for reference
PARENT_ORDERINGS = {
    "DEF-FORM-ONLY": ["product_listing", "cart", "detail"],
    "DEF-FULL-MAP": ["cart", "product_listing", "detail"]
}

# === FUNCTIONS ===

def canonical_role(raw_role, role_map):
    return role_map.get(raw_role, raw_role)

def count_interactive(locatable_sample, interactive_roles, role_map):
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
    return count / elements_with_bbox

def get_ordering(type_densities):
    """Return ordered list of page types by mean density (descending)."""
    sorted_types = sorted(type_densities.items(), key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_types]

def load_tasks():
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
    
    # Mean per type
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

def compute_parent_pairwise_agreement():
    """Compute the 0.3 value from the parent: 5 definitions, 3 agree on listing>cart>detail, 1 agrees on cart>listing>detail."""
    # Parent had 5 definitions, 3 of which agree on product_listing>cart>detail
    # 1 (DEF-FULL-MAP) agrees on cart>product_listing>detail
    # 1 (DEF-ALL-LOCATABLE) was different
    # 10 total pairs, 3 agreeing pairs = 0.3
    # We replicate this from the parent result.json
    return 3, 10, 0.3

# === TEST 1: Random ROLE_MAP Null ===
def test_random_null(tasks, observed_agreement=0.3):
    """Randomly assign each raw role to interactive/not with p=0.5, repeat N_ITER times."""
    rng = random.Random(SEED)
    
    # Get the set of raw roles present in the data
    raw_roles_in_data = set()
    for task in tasks:
        for elem in task["locatable_sample"]:
            raw_roles_in_data.add(elem.get("role", ""))
    
    null_agreements = []
    null_orderings = []
    
    for _ in range(N_RANDOM_ITERATIONS):
        # Random assignment: each role independently included/excluded with p=0.5
        random_roles = set()
        for role in raw_roles_in_data:
            if rng.random() < 0.5:
                random_roles.add(role)
        
        # Compute ordering for this random assignment
        ordering, means = compute_ordering_for_def(tasks, random_roles, {})
        null_orderings.append(ordering)
    
    # Compute pairwise agreement across all null orderings
    agreeing, total_pairs, agreement_frac = compute_pairwise_agreement(null_orderings)
    
    # Also compute the distribution of how many times each ordering appears
    ordering_counts = defaultdict(int)
    for o in null_orderings:
        ordering_counts[tuple(o)] += 1
    
    # Find the proportion of null orderings that match the observed ordering patterns
    # Observed: 3/5 definitions agree on product_listing>cart>detail
    # We test whether the fraction of agreeing pairs in the null exceeds observed 0.3
    
    # Count how many null pairwise agreement fractions exceed 0.3
    # (We need per-iteration agreement to build a distribution)
    # Actually, let's compute the distribution of ordering diversity
    # and test whether observed 0.3 is extreme
    
    # Simpler: compute the probability that a random pair of null orderings agrees
    # This is the expected pairwise agreement under the null
    # Then test if observed 0.3 exceeds this
    
    # From the null sample, compute the expected pairwise agreement
    # by sampling pairs from the null orderings
    n_pairs_to_sample = 10000
    pair_agreements = []
    for _ in range(n_pairs_to_sample):
        i, j = rng.sample(range(len(null_orderings)), 2)
        pair_agreements.append(1 if null_orderings[i] == null_orderings[j] else 0)
    
    null_mean_agreement = sum(pair_agreements) / len(pair_agreements)
    
    # Compute 95th percentile of null pairwise agreement
    # Sort the pair agreements and find the 95th percentile
    pair_agreements_sorted = sorted(pair_agreements)
    p95_index = int(0.95 * len(pair_agreements_sorted))
    p95_value = pair_agreements_sorted[p95_index]
    
    # Test: does observed 0.3 exceed the null?
    exceeds_chance = observed_agreement > null_mean_agreement
    exceeds_p95 = observed_agreement > p95_value
    
    # Also compute a direct test: for each null iteration, compute how many
    # of the 5 parent definitions' orderings it matches
    # (simplified: just check the ordering diversity)
    
    return {
        "n_iterations": N_RANDOM_ITERATIONS,
        "n_raw_roles": len(raw_roles_in_data),
        "raw_roles": sorted(raw_roles_in_data),
        "null_mean_pairwise_agreement": null_mean_agreement,
        "null_p95_pairwise_agreement": p95_value,
        "observed_agreement": observed_agreement,
        "exceeds_null_mean": exceeds_chance,
        "exceeds_null_p95": exceeds_p95,
        "ordering_distribution": {str(k): v for k, v in sorted(ordering_counts.items(), key=lambda x: -x[1])},
        "unique_orderings_in_null": len(ordering_counts),
        "top_ordering_fraction": max(ordering_counts.values()) / N_RANDOM_ITERATIONS
    }

# === TEST 2: Single-Role Definitions ===
def test_single_role(tasks):
    """Test each individual role in isolation."""
    results = {}
    
    for role in sorted(ALL_RAW_ROLES):
        # Create definition that counts ONLY this role
        interactive_roles = {role}
        role_map = {}
        
        ordering, means = compute_ordering_for_def(tasks, interactive_roles, role_map)
        
        # Count total elements across all tasks for this role
        total_count = 0
        per_task_counts = {}
        for task in tasks:
            count = count_interactive(task["locatable_sample"], interactive_roles, role_map)
            total_count += count
            per_task_counts[task["task_id"]] = count
        
        # Check if ordering is degenerate (same type for all, or too few elements)
        degenerate = total_count < 2 or len(set(ordering)) < len(ordering)
        
        results[role] = {
            "ordering": ordering,
            "ordering_values": means,
            "total_elements": total_count,
            "per_task_counts": per_task_counts,
            "degenerate": degenerate
        }
    
    # Check if any single-role ordering matches the parent family orderings
    parent_orderings = [
        ["product_listing", "cart", "detail"],  # DEF-FORM-ONLY
        ["cart", "product_listing", "detail"]    # DEF-FULL-MAP
    ]
    
    matches_parent = {}
    for role, res in results.items():
        matches_parent[role] = res["ordering"] in parent_orderings
    
    # Check ordering diversity across single-role definitions
    unique_orderings = set(tuple(r["ordering"]) for r in results.values() if not r["degenerate"])
    
    return {
        "per_role": results,
        "matches_parent_ordering": matches_parent,
        "n_unique_orderings": len(unique_orderings),
        "unique_orderings": [list(o) for o in unique_orderings],
        "n_degenerate": sum(1 for r in results.values() if r["degenerate"]),
        "any_matches_parent": any(matches_parent.values())
    }

# === TEST 3: Isolated a→link Definition ===
def test_isolated_a_link(tasks):
    """Test a definition with a→link mapping but WITHOUT menuitem/tab."""
    # Same as DEF-FORM-AND-A-TEXTBOX but with a→link added
    interactive_roles = {"button", "link", "textbox", "checkbox", "radio", "combobox", "listbox", "slider", "spinbutton", "searchbox", "switch"}
    role_map = {"a": "link", "input": "textbox"}
    
    ordering, means = compute_ordering_for_def(tasks, interactive_roles, role_map)
    
    # Compare with DEF-FULL-MAP
    full_map_ordering, full_map_means = compute_ordering_for_def(
        tasks, DEF_FULL_MAP["INTERACTIVE_ROLES"], DEF_FULL_MAP["ROLE_MAP"]
    )
    
    matches_full_map = ordering == full_map_ordering
    
    # Also compare with DEF-FORM-ONLY (no a→link)
    form_only_ordering, form_only_means = compute_ordering_for_def(
        tasks, 
        {"button", "textbox", "checkbox", "radio", "combobox", "listbox", "slider", "spinbutton", "searchbox", "switch"},
        {}
    )
    
    matches_form_only = ordering == form_only_ordering
    
    return {
        "isolated_a_link_ordering": ordering,
        "isolated_a_link_means": means,
        "def_full_map_ordering": full_map_ordering,
        "def_full_map_means": full_map_means,
        "def_form_only_ordering": form_only_ordering,
        "def_form_only_means": form_only_means,
        "matches_def_full_map": matches_full_map,
        "matches_def_form_only": matches_form_only,
        "interpretation": "a→link alone drives reversal" if matches_full_map else "a→link alone does NOT drive reversal"
    }

# === MAIN ===
def main():
    print("Loading tasks...")
    tasks = load_tasks()
    print(f"Loaded {len(tasks)} successful tasks")
    print(f"Page types: {[t['page_type'] for t in tasks]}")
    
    # Verify parent baselines
    print("\n=== PARENT BASELINE VERIFICATION ===")
    full_map_ordering, full_map_means = compute_ordering_for_def(
        tasks, DEF_FULL_MAP["INTERACTIVE_ROLES"], DEF_FULL_MAP["ROLE_MAP"]
    )
    form_only_ordering, form_only_means = compute_ordering_for_def(
        tasks,
        {"button", "textbox", "checkbox", "radio", "combobox", "listbox", "slider", "spinbutton", "searchbox", "switch"},
        {}
    )
    print(f"DEF-FULL-MAP ordering: {full_map_ordering} (expected: cart>listing>detail)")
    print(f"DEF-FORM-ONLY ordering: {form_only_ordering} (expected: listing>cart>detail)")
    print(f"DEF-FULL-MAP means: {full_map_means}")
    print(f"DEF-FORM-ONLY means: {form_only_means}")
    
    # Compute raw role counts in data
    raw_role_counts = defaultdict(int)
    for task in tasks:
        for elem in task["locatable_sample"]:
            raw_role_counts[elem.get("role", "")] += 1
    print(f"\nRaw role counts in data: {dict(sorted(raw_role_counts.items()))}")
    
    # Test 1: Random null
    print("\n=== TEST 1: RANDOM ROLE_MAP NULL ===")
    null_result = test_random_null(tasks, observed_agreement=0.3)
    print(f"Null mean pairwise agreement: {null_result['null_mean_pairwise_agreement']:.4f}")
    print(f"Null 95th percentile: {null_result['null_p95_pairwise_agreement']:.4f}")
    print(f"Observed agreement: {null_result['observed_agreement']}")
    print(f"Exceeds null mean: {null_result['exceeds_null_mean']}")
    print(f"Exceeds null p95: {null_result['exceeds_null_p95']}")
    print(f"Unique orderings in null: {null_result['unique_orderings_in_null']}")
    print(f"Top ordering fraction: {null_result['top_ordering_fraction']:.4f}")
    print(f"Ordering distribution (top 10):")
    for k, v in list(null_result['ordering_distribution'].items())[:10]:
        print(f"  {k}: {v}")
    
    # Test 2: Single-role definitions
    print("\n=== TEST 2: SINGLE-ROLE DEFINITIONS ===")
    single_role_result = test_single_role(tasks)
    for role in sorted(single_role_result["per_role"].keys()):
        res = single_role_result["per_role"][role]
        match_str = "MATCHES PARENT" if single_role_result["matches_parent_ordering"][role] else ""
        degenerate_str = "DEGENERATE" if res["degenerate"] else ""
        print(f"  {role}: ordering={res['ordering']}, total={res['total_elements']}, {match_str} {degenerate_str}")
    print(f"Any matches parent: {single_role_result['any_matches_parent']}")
    print(f"Unique non-degenerate orderings: {single_role_result['n_unique_orderings']}")
    
    # Test 3: Isolated a→link
    print("\n=== TEST 3: ISOLATED a→link ===")
    a_link_result = test_isolated_a_link(tasks)
    print(f"Isolated a→link ordering: {a_link_result['isolated_a_link_ordering']}")
    print(f"DEF-FULL-MAP ordering: {a_link_result['def_full_map_ordering']}")
    print(f"DEF-FORM-ONLY ordering: {a_link_result['def_form_only_ordering']}")
    print(f"Matches DEF-FULL-MAP: {a_link_result['matches_def_full_map']}")
    print(f"Matches DEF-FORM-ONLY: {a_link_result['matches_def_form_only']}")
    print(f"Interpretation: {a_link_result['interpretation']}")
    
    # === DECISION RULE ===
    print("\n=== DECISION RULE EVALUATION ===")
    
    # Condition 1: Random null mean < 0.3 AND observed 0.3 > 95th percentile
    cond1 = (null_result['null_mean_pairwise_agreement'] < 0.3 and 
             null_result['exceeds_null_p95'])
    print(f"Condition 1 (null confirms significance): {cond1}")
    print(f"  Null mean < 0.3: {null_result['null_mean_pairwise_agreement'] < 0.3}")
    print(f"  Observed > p95: {null_result['exceeds_null_p95']}")
    
    # Condition 2: No single-role definition produces invariant ordering
    cond2 = not single_role_result['any_matches_parent']
    print(f"Condition 2 (no single-role invariant): {cond2}")
    
    # Condition 3: Isolated a→link produces same ordering as DEF-FULL-MAP
    cond3 = a_link_result['matches_def_full_map']
    print(f"Condition 3 (isolated a→link matches DEF-FULL-MAP): {cond3}")
    
    if cond1 and cond2 and cond3:
        verdict = "SURVIVES_CURRENT_TEST"
    elif not cond1 or not cond2 or not cond3:
        verdict = "FALSIFIED-IN-SETTING"
    else:
        verdict = "MIXED"
    
    print(f"\nVERDICT: {verdict}")
    
    # Save results
    all_results = {
        "experiment_id": "EXP-INTEL-35112013458",
        "parent_baselines": {
            "DEF_FULL_MAP_ordering": full_map_ordering,
            "DEF_FULL_MAP_means": full_map_means,
            "DEF_FORM_ONLY_ordering": form_only_ordering,
            "DEF_FORM_ONLY_means": form_only_means
        },
        "raw_role_counts": dict(raw_role_counts),
        "test1_random_null": null_result,
        "test2_single_role": single_role_result,
        "test3_isolated_a_link": a_link_result,
        "decision": {
            "cond1_null_confirms": cond1,
            "cond2_no_single_role_invariant": cond2,
            "cond3_a_link_matches": cond3,
            "verdict": verdict
        }
    }
    
    out_path = "/tmp/opencode/null_model_results.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nFull results saved to {out_path}")
    return 0

if __name__ == "__main__":
    exit(main())
