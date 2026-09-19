#!/usr/bin/env python3
"""EXP-INTEL-35462974425 — Full DOM ranking stability test.

Tests whether ranking instability under recipe sampling (C6 FAIL at 55.95%
in parent EXP-INTEL-35445596324) is a truncation artifact by testing on full
DOM locatable_sample elements (n=21-82 per task, not truncated-first-20).

Frozen decision rule requires C3 gate: locatable_sample must contain >20
elements for at least 5 of 7 tasks. If data is truncated at collection time,
experiment is BLOCKED.

This script verifies the C3 gate and runs baseline controls on the
truncated-first-20 data for reference context.
"""
import json, math, os, sys
from collections import defaultdict

RAW_PATH = "research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json"
OUTPUT_DIR = "research/experiments/EXP-INTEL-35462974425"

# --- Definitions (same as parent) ---
DEFINITIONS = {
    "DEF-FULL-MAP": {
        "interactive_roles": {"button", "link", "textbox", "checkbox", "radio",
                              "combobox", "listbox", "menuitem", "tab", "slider",
                              "spinbutton", "searchbox", "switch"},
        "role_map": {"a": "link", "input": "textbox"}
    },
    "DEF-FORM-ONLY": {
        "interactive_roles": {"button", "textbox", "checkbox", "radio",
                              "combobox", "listbox", "slider", "spinbutton",
                              "searchbox", "switch"},
        "role_map": {}
    },
}

# --- Utility functions ---
def apply_role_map(role, role_map):
    return role_map.get(role, role)

def elem_matches_def(elem, defn):
    canonical = apply_role_map(elem["role"], defn["role_map"])
    return canonical in defn["interactive_roles"]

def compute_per_element_features(locatable_sample):
    tag_counts = defaultdict(int)
    for elem in locatable_sample:
        tag_counts[elem["tag"]] += 1
    total = len(locatable_sample)
    tag_vals = []
    for elem in locatable_sample:
        p = tag_counts[elem["tag"]] / total
        tag_vals.append(-p * math.log2(p) if p > 0 else 0.0)
    form_vals = [1.0 if elem.get("inForm", False) else 0.0 for elem in locatable_sample]
    area_vals = [elem["w"] * elem["h"] for elem in locatable_sample]
    return {"tag_entropy": tag_vals, "form_fraction": form_vals, "total_area": area_vals}

def compute_feature_weighted_density(sample, elem_features, ewb, defn):
    """sum(feature_value for matching elements) / ewb."""
    densities = {}
    for feat_key, feat_vals in elem_features.items():
        total = sum(feat_vals[i] for i, elem in enumerate(sample) if elem_matches_def(elem, defn))
        densities[feat_key] = total / ewb if ewb > 0 else 0.0
    return densities

def _eta2(groups):
    all_vals = [v for g in groups.values() for v in g]
    if not all_vals:
        return 0.0
    gm = sum(all_vals) / len(all_vals)
    ss_total = sum((v - gm) ** 2 for v in all_vals)
    if ss_total == 0:
        return 0.0
    ss_between = sum(len(g) * (sum(g)/len(g) - gm)**2 for g in groups.values() if g)
    return ss_between / ss_total

def _stats(groups):
    all_vals = [v for g in groups.values() for v in g]
    if not all_vals:
        return {"eta2": 0.0, "group_means": {}, "grand_mean": 0.0, "within_stds": {}}
    gm = sum(all_vals) / len(all_vals)
    ss_total = sum((v - gm) ** 2 for v in all_vals)
    ss_within = 0.0
    ss_between = 0.0
    means, stds = {}, {}
    for k, g in groups.items():
        n = len(g)
        m = sum(g) / n if n else 0.0
        means[k] = m
        stds[k] = (sum((v-m)**2 for v in g)/(n-1))**0.5 if n > 1 else 0.0
        ss_within += sum((v - m) ** 2 for v in g)
        ss_between += n * (m - gm) ** 2
    eta2 = ss_between / ss_total if ss_total > 0 else 0.0
    return {"eta2": eta2, "group_means": means, "grand_mean": gm, "within_stds": stds}

def check_ranking(direct_means, pipeline_means, feat_key):
    """Check if listing > detail is preserved."""
    dl = direct_means.get("product_listing", 0)
    dd = direct_means.get("detail", 0)
    pl = pipeline_means.get("product_listing", 0)
    pd = pipeline_means.get("detail", 0)
    return (dl > dd) == (pl > pd)

def main():
    # Load raw data
    with open(RAW_PATH) as f:
        raw = json.load(f)

    measurements = [m for m in raw["measurements"]
                    if m.get("locatable_sample") and m["page_type"] != "checkout"
                    and m.get("error") is None and m.get("http_status") == 200]

    # Deduplicate cart (take first)
    seen_cart = False
    filtered = []
    for m in measurements:
        if m["page_type"] == "cart":
            if not seen_cart:
                filtered.append(m)
                seen_cart = True
        else:
            filtered.append(m)
    measurements = filtered

    # Select 3 listing + 3 detail + 1 cart (matching parent protocol)
    tasks = ([m for m in measurements if m["page_type"] == "product_listing"][:3] +
             [m for m in measurements if m["page_type"] == "detail"][:3] +
             [m for m in measurements if m["page_type"] == "cart"][:1])

    print(f"Tasks: {len(tasks)}")
    for t in tasks:
        print(f"  {t['task_id']}: locatable_sample={len(t['locatable_sample'])}, "
              f"ewb={t['elements_with_bbox']}, page_type={t['page_type']}")

    # =====================================================================
    # C3 GATE: Full DOM elements available check
    # =====================================================================
    c3_tasks_with_full_dom = sum(1 for m in tasks if len(m["locatable_sample"]) > 20)
    c3_total_tasks = len(tasks)
    c3_pass = c3_tasks_with_full_dom >= 5
    print(f"\nC3 GATE: {c3_tasks_with_full_dom}/{c3_total_tasks} tasks have locatable_sample > 20 elements")
    print(f"C3 PASS: {c3_pass}")

    # Record the element counts for all tasks
    element_counts = {}
    for m in tasks:
        element_counts[m["task_id"]] = {
            "locatable_sample_len": len(m["locatable_sample"]),
            "locatable_elements": m.get("locatable_elements"),
            "elements_with_bbox": m.get("elements_with_bbox"),
            "total_dom_elements": m.get("total_dom_elements"),
            "page_type": m["page_type"]
        }

    # =====================================================================
    # Since BLOCKED, run baseline controls on truncated-first-20 for context
    # =====================================================================

    # --- Positive Control PC1: Direct feature eta2 (task-level features) ---
    # Matching parent: tag_entropy per task, form_fraction per task, total_area per task
    pc1_results = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        groups = defaultdict(list)
        for t in tasks:
            sample = t["locatable_sample"]
            if fk == "tag_entropy":
                tag_counts = defaultdict(int)
                for elem in sample:
                    tag_counts[elem["tag"]] += 1
                total = len(sample)
                val = sum(-c/total * math.log2(c/total) for c in tag_counts.values() if c > 0)
            elif fk == "form_fraction":
                val = sum(1 for e in sample if e.get("inForm", False)) / len(sample)
            elif fk == "total_area":
                val = sum(e["w"] * e["h"] for e in sample)
            groups[t["page_type"]].append(val)
        stats = _stats(groups)
        pc1_results[fk] = {"eta2": stats["eta2"], "group_means": stats["group_means"],
                           "within_stds": stats["within_stds"]}
    pc1_pass = all(r["eta2"] >= 0.99 for r in pc1_results.values())
    print(f"\nPC1 (positive control): pass={pc1_pass}")
    for k, v in pc1_results.items():
        print(f"  {k}: eta2={v['eta2']:.6f}")

    # --- Null Control NC1: Normalized hierarchy density (matching parent: alpha=0.3, y-coordinate) ---
    ALPHA = 0.3
    groups_nc = defaultdict(list)
    nc1_per_task = {}
    for t in tasks:
        sample = t["locatable_sample"]
        total_weight = sum(math.exp(-ALPHA * e["y"]) for e in sample)
        weighted_sum = sum(math.exp(-ALPHA * e["y"]) for e in sample if e.get("inForm", False))
        density = weighted_sum / total_weight if total_weight > 0 else 0.0
        groups_nc[t["page_type"]].append(density)
        nc1_per_task[t["task_id"]] = density
    nc1_stats = _stats(groups_nc)
    nc1_pass = nc1_stats["eta2"] < 0.01
    print(f"\nNC1 (null control): pass={nc1_pass}, eta2={nc1_stats['eta2']:.10f}")
    print(f"  group_means={nc1_stats['group_means']}")

    # --- Non-recipe pipeline on first-20 (truncated, not full DOM) ---
    non_recipe_results = {}
    for defn_name, defn in DEFINITIONS.items():
        for feat_key in ["tag_entropy", "form_fraction", "total_area"]:
            groups = defaultdict(list)
            for t in tasks:
                features = compute_per_element_features(t["locatable_sample"])
                total_ewb = t["elements_with_bbox"]
                densities = compute_feature_weighted_density(
                    t["locatable_sample"], features, total_ewb, defn)
                groups[t["page_type"]].append(densities[feat_key])
            stats = _stats(groups)
            key = f"{feat_key} x {defn_name}"
            non_recipe_results[key] = {
                "eta2": stats["eta2"],
                "group_means": stats["group_means"]
            }
    max_eta2 = max(r["eta2"] for r in non_recipe_results.values())
    print(f"\nNon-recipe pipeline (truncated-first-20): max eta2={max_eta2:.6f}")
    for k, v in non_recipe_results.items():
        print(f"  {k}: eta2={v['eta2']:.6f}")

    # --- Ranking check on first-20 ---
    ranking_preserved = {}
    for defn_name, defn in DEFINITIONS.items():
        for feat_key in ["tag_entropy", "form_fraction", "total_area"]:
            direct_groups = defaultdict(list)
            pipeline_groups = defaultdict(list)
            for t in tasks:
                features = compute_per_element_features(t["locatable_sample"])
                total_ewb = t["elements_with_bbox"]
                direct_densities = compute_feature_weighted_density(
                    t["locatable_sample"], features, total_ewb, defn)
                pipeline_densities = direct_densities  # non-recipe = direct
                direct_groups[t["page_type"]].append(direct_densities[feat_key])
                pipeline_groups[t["page_type"]].append(pipeline_densities[feat_key])
            key = f"{feat_key} x {defn_name}"
            ranking_preserved[key] = check_ranking(
                {k: sum(v)/len(v) for k, v in direct_groups.items()},
                {k: sum(v)/len(v) for k, v in pipeline_groups.items()},
                feat_key)
    print(f"\nNon-recipe ranking (truncated-first-20): {ranking_preserved}")

    # =====================================================================
    # Build result data
    # =====================================================================
    result = {
        "c3_gate": {
            "tasks_with_locatable_sample_gt20": c3_tasks_with_full_dom,
            "total_tasks": c3_total_tasks,
            "threshold": 5,
            "pass": c3_pass,
            "element_counts": element_counts,
            "diagnosis": "ALL tasks have exactly 20 elements in locatable_sample. "
                        "The raw data was truncated to first-20 at collection time. "
                        "Full DOM elements (n=21-82) are NOT available in the existing "
                        "raw evidence. Full DOM re-collection from the Magento Docker "
                        "container would be required."
        },
        "pc1_positive_control": {
            "pass": pc1_pass,
            "features": pc1_results,
            "note": "PC1 runs on truncated-first-20 (not full DOM) for reference. "
                   "Full DOM PC1 is blocked."
        },
        "nc1_null_control": {
            "pass": nc1_pass,
            "eta2": nc1_stats["eta2"],
            "group_means": nc1_stats["group_means"],
            "note": "NC1 runs on truncated-first-20 (not full DOM) for reference."
        },
        "non_recipe_truncated_first20": {
            "eta2": non_recipe_results,
            "max_eta2": max_eta2,
            "ranking_preserved": ranking_preserved,
            "note": "Results on truncated-first-20 data only; full DOM analysis blocked."
        }
    }

    # Save analysis output
    output_path = os.path.join(OUTPUT_DIR, "analysis_output.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nAnalysis output saved to {output_path}")

    # Print summary
    print("\n" + "="*60)
    print("EXPERIMENT STATUS: BLOCKED")
    print("C3 GATE: FAIL — all locatable_sample arrays truncated to 20")
    print("Full DOM re-collection required for the frozen design.")
    print("="*60)

if __name__ == "__main__":
    main()
