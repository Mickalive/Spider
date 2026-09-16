#!/usr/bin/env python3
"""
EXP-INTEL-35083033552 Analysis Script
Tests whether a canonical ROLE_MAP definition can stabilize interactive element density ordering
across 5 definitions, applied to truncated-first-20 locatable_sample data from 7 tasks.
"""

import json
import sys
import os
from collections import defaultdict
from math import sqrt

# === ROLE_MAP DEFINITIONS ===
# Each definition specifies:
#   - INTERACTIVE_ROLES: set of roles counted as interactive
#   - ROLE_MAP: mapping from raw role to canonical role (or None for passthrough)

DEFINITIONS = {
    "DEF-FORM-ONLY": {
        "description": "Most restrictive: form elements only, no links",
        "INTERACTIVE_ROLES": {"button", "textbox", "checkbox", "radio", "combobox", "listbox", "slider", "spinbutton", "searchbox", "switch"},
        "ROLE_MAP": {}  # raw roles used as-is
    },
    "DEF-FORM-AND-BUTTON-LINK": {
        "description": "Form elements + semantic link role (not 'a' elements)",
        "INTERACTIVE_ROLES": {"button", "link", "textbox", "checkbox", "radio", "combobox", "listbox", "slider", "spinbutton", "searchbox", "switch"},
        "ROLE_MAP": {}  # raw roles used as-is
    },
    "DEF-FORM-AND-A-TEXTBOX": {
        "description": "Form elements + input→textbox mapping (but NOT a→link)",
        "INTERACTIVE_ROLES": {"button", "link", "textbox", "checkbox", "radio", "combobox", "listbox", "slider", "spinbutton", "searchbox", "switch"},
        "ROLE_MAP": {"input": "textbox"}
    },
    "DEF-FULL-MAP": {
        "description": "Parent with_map: a→link, input→textbox",
        "INTERACTIVE_ROLES": {"button", "link", "textbox", "checkbox", "radio", "combobox", "listbox", "menuitem", "tab", "slider", "spinbutton", "searchbox", "switch"},
        "ROLE_MAP": {"a": "link", "input": "textbox"}
    },
    "DEF-ALL-LOCATABLE": {
        "description": "All locatable elements regardless of role",
        "INTERACTIVE_ROLES": None,  # None means all elements count
        "ROLE_MAP": {}
    }
}

def canonical_role(raw_role, role_map):
    """Apply role mapping to get canonical role."""
    return role_map.get(raw_role, raw_role)

def count_interactive(locatable_sample, defn):
    """Count interactive elements in locatable_sample for a given definition."""
    if defn["INTERACTIVE_ROLES"] is None:
        # DEF-ALL-LOCATABLE: count all elements
        return len(locatable_sample)
    
    count = 0
    for elem in locatable_sample:
        raw_role = elem.get("role", "")
        canon = canonical_role(raw_role, defn["ROLE_MAP"])
        if canon in defn["INTERACTIVE_ROLES"]:
            count += 1
    return count

def compute_density(task, count):
    """Compute density = count / elements_with_bbox."""
    return count / task["elements_with_bbox"]

def load_data():
    """Load raw data and extract 7 successful tasks."""
    raw_path = "research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json"
    with open(raw_path, "r") as f:
        raw = json.load(f)
    
    # Filter successful tasks (exclude checkout failures)
    tasks = []
    for m in raw["measurements"]:
        if m.get("error") is None and m.get("http_status") == 200 and "locatable_sample" in m:
            tasks.append(m)
    
    return tasks

def run_analysis(tasks):
    """Run full analysis for all 5 definitions."""
    results = {}
    
    for def_name, defn in DEFINITIONS.items():
        def_result = {
            "description": defn["description"],
            "per_task": {},
            "per_type": {},
            "ordering": [],
            "ordering_values": {}
        }
        
        type_counts = defaultdict(list)
        type_bboxes = defaultdict(list)
        type_densities = defaultdict(list)
        
        for task in tasks:
            task_id = task["task_id"]
            page_type = task["page_type"]
            locatable_sample = task["locatable_sample"]
            
            count = count_interactive(locatable_sample, defn)
            density = compute_density(task, count)
            
            def_result["per_task"][task_id] = {
                "page_type": page_type,
                "tightened_locatable_count": count,
                "elements_with_bbox": task["elements_with_bbox"],
                "density_bbox": density
            }
            
            type_counts[page_type].append(count)
            type_bboxes[page_type].append(task["elements_with_bbox"])
            type_densities[page_type].append(density)
        
        # Compute per-type means
        for ptype in ["product_listing", "detail", "cart"]:
            if ptype in type_densities:
                vals = type_densities[ptype]
                mean_d = sum(vals) / len(vals)
                def_result["per_type"][ptype] = {
                    "n": len(vals),
                    "mean_density_bbox": mean_d,
                    "values_density_bbox": vals,
                    "cv": (sqrt(sum((v - mean_d)**2 for v in vals) / len(vals)) / mean_d) if mean_d > 0 and len(vals) > 1 else 0.0
                }
                def_result["ordering_values"][ptype] = mean_d
        
        # Sort by density descending
        sorted_types = sorted(def_result["ordering_values"].items(), key=lambda x: x[1], reverse=True)
        def_result["ordering"] = [t[0] for t in sorted_types]
        
        results[def_name] = def_result
    
    return results

def compute_pairwise_agreement(results):
    """Compute pairwise ordering agreement across definitions."""
    def_names = list(DEFINITIONS.keys())
    agreements = {}
    total_pairs = 0
    agreeing_pairs = 0
    
    for i in range(len(def_names)):
        for j in range(i+1, len(def_names)):
            d1, d2 = def_names[i], def_names[j]
            order1 = results[d1]["ordering"]
            order2 = results[d2]["ordering"]
            agree = order1 == order2
            agreements[f"{d1} vs {d2}"] = {
                "ordering_1": order1,
                "ordering_2": order2,
                "agree": agree
            }
            total_pairs += 1
            if agree:
                agreeing_pairs += 1
    
    return {
        "total_pairs": total_pairs,
        "agreeing_pairs": agreeing_pairs,
        "agreement_fraction": agreeing_pairs / total_pairs if total_pairs > 0 else 0,
        "pair_details": agreements
    }

def compute_adjacency_agreement(results):
    """Compute adjacency agreement (consecutive definitions)."""
    def_names = list(DEFINITIONS.keys())
    adj_agreements = {}
    
    for i in range(len(def_names) - 1):
        d1, d2 = def_names[i], def_names[i+1]
        order1 = results[d1]["ordering"]
        order2 = results[d2]["ordering"]
        adj_agreements[f"{d1} vs {d2}"] = {
            "ordering_1": order1,
            "ordering_2": order2,
            "agree": order1 == order2
        }
    
    agreeing = sum(1 for v in adj_agreements.values() if v["agree"])
    total = len(adj_agreements)
    
    return {
        "total": total,
        "agreeing": agreeing,
        "agreement_fraction": agreeing / total if total > 0 else 0,
        "pair_details": adj_agreements
    }

def compute_link_sensitivity(results):
    """Compute sensitivity to link inclusion."""
    # Compare definitions that include 'link' vs exclude it
    with_link = ["DEF-FORM-AND-BUTTON-LINK", "DEF-FORM-AND-A-TEXTBOX", "DEF-FULL-MAP"]
    without_link = ["DEF-FORM-ONLY"]
    
    sensitivities = {}
    for ptype in ["product_listing", "detail", "cart"]:
        densities_with = []
        densities_without = []
        for d in with_link:
            if ptype in results[d]["ordering_values"]:
                densities_with.append(results[d]["ordering_values"][ptype])
        for d in without_link:
            if ptype in results[d]["ordering_values"]:
                densities_without.append(results[d]["ordering_values"][ptype])
        
        if densities_with and densities_without:
            avg_with = sum(densities_with) / len(densities_with)
            avg_without = sum(densities_without) / len(densities_without)
            sensitivities[ptype] = {
                "mean_density_with_link": avg_with,
                "mean_density_without_link": avg_without,
                "absolute_difference": abs(avg_with - avg_without)
            }
    
    avg_sensitivity = sum(v["absolute_difference"] for v in sensitivities.values()) / len(sensitivities) if sensitivities else 0
    return {
        "per_type": sensitivities,
        "mean_absolute_difference": avg_sensitivity
    }

def compute_discrimination_ratios(results):
    """Compute between/within type variance for each definition."""
    ratios = {}
    for def_name, def_result in results.items():
        # Collect all densities by type
        type_densities = defaultdict(list)
        for task_id, task_data in def_result["per_task"].items():
            ptype = task_data["page_type"]
            type_densities[ptype].append(task_data["density_bbox"])
        
        # Compute between-type variance
        all_means = []
        all_values = []
        for ptype, vals in type_densities.items():
            mean = sum(vals) / len(vals)
            all_means.append(mean)
            all_values.extend(vals)
        
        if len(all_means) < 2:
            ratios[def_name] = {"between_variance": 0, "within_variance": 0, "ratio": float('inf')}
            continue
        
        grand_mean = sum(all_values) / len(all_values)
        between_var = sum((m - grand_mean)**2 for m in all_means) / (len(all_means) - 1)
        
        # Compute within-type variance
        within_var_sum = 0
        total_within = 0
        for ptype, vals in type_densities.items():
            if len(vals) > 1:
                mean = sum(vals) / len(vals)
                within_var_sum += sum((v - mean)**2 for v in vals)
                total_within += len(vals) - 1
        
        within_var = within_var_sum / total_within if total_within > 0 else 0
        
        ratio = between_var / within_var if within_var > 0 else float('inf')
        
        ratios[def_name] = {
            "between_variance": between_var,
            "within_variance": within_var,
            "ratio": ratio
        }
    
    return ratios

def check_controls(results):
    """Check positive and null controls."""
    controls = {}
    
    # Positive control: all definitions produce >0 on all tasks
    all_positive = True
    positive_details = {}
    for def_name, def_result in results.items():
        for task_id, task_data in def_result["per_task"].items():
            if task_data["tightened_locatable_count"] == 0:
                all_positive = False
                positive_details[f"{def_name}:{task_id}"] = "ZERO"
            else:
                positive_details[f"{def_name}:{task_id}"] = task_data["tightened_locatable_count"]
    
    controls["positive_control"] = {
        "description": "All 5 definitions produce tightened_locatable_count > 0 on all 7 tasks",
        "pass": all_positive,
        "details": positive_details
    }
    
    # Null control: DEF-ALL-LOCATABLE yields count = locatable_sample length
    null_pass = True
    null_details = {}
    for def_name in DEFINITIONS:
        if def_name == "DEF-ALL-LOCATABLE":
            continue  # Skip self
    
    # Actually check DEF-ALL-LOCATABLE count = len(locatable_sample)
    raw_path = "research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json"
    with open(raw_path, "r") as f:
        raw = json.load(f)
    
    for m in raw["measurements"]:
        if m.get("error") is None and m.get("http_status") == 200 and "locatable_sample" in m:
            task_id = m["task_id"]
            locatable_len = len(m["locatable_sample"])
            all_loc_count = results["DEF-ALL-LOCATABLE"]["per_task"][task_id]["tightened_locatable_count"]
            match = locatable_len == all_loc_count
            null_details[task_id] = {
                "locatable_sample_len": locatable_len,
                "def_all_locatable_count": all_loc_count,
                "match": match
            }
            if not match:
                null_pass = False
    
    controls["null_control"] = {
        "description": "DEF-ALL-LOCATABLE yields tightened_count = locatable_sample length on all tasks",
        "pass": null_pass,
        "details": null_details
    }
    
    # Baseline comparison
    controls["baseline_comparison"] = {
        "description": "DEF-FULL-MAP ordering matches parent with_map ordering (cart>listing>detail)",
        "expected_with_map": ["cart", "product_listing", "detail"],
        "observed_DEF_FULL_MAP": results["DEF-FULL-MAP"]["ordering"],
        "pass": results["DEF-FULL-MAP"]["ordering"] == ["cart", "product_listing", "detail"]
    }
    
    return controls

def main():
    print("Loading data...")
    tasks = load_data()
    print(f"Loaded {len(tasks)} successful tasks")
    
    print("Running analysis...")
    results = run_analysis(tasks)
    
    print("Computing pairwise agreement...")
    pairwise = compute_pairwise_agreement(results)
    
    print("Computing adjacency agreement...")
    adjacency = compute_adjacency_agreement(results)
    
    print("Computing link sensitivity...")
    link_sensitivity = compute_link_sensitivity(results)
    
    print("Computing discrimination ratios...")
    discrimination = compute_discrimination_ratios(results)
    
    print("Checking controls...")
    controls = check_controls(results)
    
    # Determine verdict based on decision rule
    verdict = "UNKNOWN"
    
    # SURVIVES_CURRENT_TEST if ANY of:
    # 1. At least 2 semantically adjacent definitions produce the same ordering
    # 2. Ordering invariant to link-inclusion
    survives_adjacent = adjacency["agreeing"] >= 2
    survives_link = link_sensitivity["mean_absolute_difference"] == 0  # No difference = invariant
    
    # FALSIFIED-IN-SETTING if ALL of:
    # 1. All 5 definitions produce different orderings
    # 2. No adjacent pair agrees
    all_different = len(set(tuple(r["ordering"]) for r in results.values())) == 5
    no_adjacent_agree = adjacency["agreeing"] == 0
    
    if survives_adjacent or survives_link:
        verdict = "SURVIVES_CURRENT_TEST"
    elif all_different and no_adjacent_agree:
        verdict = "FALSIFIED_IN_SETTING"
    else:
        verdict = "MIXED"
    
    print(f"\nVerdict: {verdict}")
    print(f"Pairwise agreement: {pairwise['agreeing_pairs']}/{pairwise['total_pairs']}")
    print(f"Adjacency agreement: {adjacency['agreeing']}/{adjacency['total']}")
    
    # Save full results
    full_results = {
        "definitions": {k: {"ordering": v["ordering"], "ordering_values": v["ordering_values"], "per_type": v["per_type"]} for k, v in results.items()},
        "pairwise_agreement": pairwise,
        "adjacency_agreement": adjacency,
        "link_sensitivity": link_sensitivity,
        "discrimination_ratios": discrimination,
        "controls": controls,
        "verdict": verdict
    }
    
    out_path = "/tmp/opencode/rolemap_analysis.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(full_results, f, indent=2)
    
    print(f"\nResults saved to {out_path}")
    
    # Print detailed orderings
    print("\n=== ORDERINGS ===")
    for def_name, def_result in results.items():
        print(f"{def_name}: {def_result['ordering']} (values: {def_result['ordering_values']})")
    
    print("\n=== DISCRIMINATION RATIOS ===")
    for def_name, ratio in discrimination.items():
        print(f"{def_name}: ratio={ratio['ratio']:.2f}")
    
    print("\n=== PAIRWISE AGREEMENT ===")
    for pair, detail in pairwise["pair_details"].items():
        status = "AGREE" if detail["agree"] else "DISAGREE"
        print(f"  {pair}: {status} ({detail['ordering_1']} vs {detail['ordering_2']})")
    
    print("\n=== ADJACENCY AGREEMENT ===")
    for pair, detail in adjacency["pair_details"].items():
        status = "AGREE" if detail["agree"] else "DISAGREE"
        print(f"  {pair}: {status}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
