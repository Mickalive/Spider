#!/usr/bin/env python3
"""
EXP-INTEL-35572177756 Full-DOM Ranking Stability Analysis
Applies frozen decision rule C1-C7 from EXP-INTEL-35462974425/spec.json
on full-DOM locatable_sample data.
"""

import json, math, os, random, sys
from collections import defaultdict
from statistics import mean, stdev

# Paths
RAW_PATH = "research/experiments/EXP-INTEL-35572177756/raw_evidence/exp355_fulldom_raw_results.json"
OUTPUT_DIR = "research/experiments/EXP-INTEL-35572177756"

# Definitions (same as parent)
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

# Constants
RECIPE_SEEDS = 10
RECIPE_ITERS = 1000
B_BOOTSTRAP = 1000

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
    dl = direct_means.get("product_listing", 0)
    dd = direct_means.get("detail", 0)
    pl = pipeline_means.get("product_listing", 0)
    pd = pipeline_means.get("detail", 0)
    return (dl > dd) == (pl > pd)

def main():
    # Load full-DOM raw data
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

    # Select 3 listing + 3 detail + 1 cart
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

    # Record element counts
    element_counts = {}
    for m in tasks:
        element_counts[m["task_id"]] = {
            "locatable_sample_len": len(m["locatable_sample"]),
            "locatable_elements": m.get("locatable_elements"),
            "elements_with_bbox": m.get("elements_with_bbox"),
            "total_dom_elements": m.get("total_dom_elements"),
            "page_type": m["page_type"]
        }

    if not c3_pass:
        print("C3 FAIL: Experiment BLOCKED")
        # Save partial result
        result = {
            "c3_gate": {
                "tasks_with_locatable_sample_gt20": c3_tasks_with_full_dom,
                "total_tasks": c3_total_tasks,
                "threshold": 5,
                "pass": c3_pass,
                "element_counts": element_counts
            }
        }
        with open(os.path.join(OUTPUT_DIR, "analysis_output.json"), "w") as f:
            json.dump(result, f, indent=2)
        sys.exit(1)

    # =====================================================================
    # Positive Control PC1: Direct feature eta2 (full DOM)
    # =====================================================================
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

    # =====================================================================
    # Null Control NC1: Normalized hierarchy density (full DOM)
    # =====================================================================
    ALPHA = 0.3
    groups_nc = defaultdict(list)
    for t in tasks:
        sample = t["locatable_sample"]
        total_weight = sum(math.exp(-ALPHA * e["y"]) for e in sample)
        weighted_sum = sum(math.exp(-ALPHA * e["y"]) for e in sample if e.get("inForm", False))
        density = weighted_sum / total_weight if total_weight > 0 else 0.0
        groups_nc[t["page_type"]].append(density)
    nc1_stats = _stats(groups_nc)
    nc1_pass = nc1_stats["eta2"] < 0.01
    print(f"\nNC1 (null control): pass={nc1_pass}, eta2={nc1_stats['eta2']:.10f}")
    print(f"  group_means={nc1_stats['group_means']}")

    # =====================================================================
    # Non-recipe pipeline eta2 (full DOM)
    # =====================================================================
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
    print(f"\nNon-recipe pipeline (full DOM): max eta2={max_eta2:.6f}")
    for k, v in non_recipe_results.items():
        print(f"  {k}: eta2={v['eta2']:.6f}")

    # C4: pipeline eta2 >= 0.05
    c4_pass = max_eta2 >= 0.05
    print(f"\nC4 (pipeline eta2 >= 0.05): pass={c4_pass}, max_eta2={max_eta2:.6f}")

    # =====================================================================
    # Recipe sampling at full DOM (no subsampling)
    # =====================================================================
    # Compute direct rankings for each feature (full DOM)
    direct_rankings = {}
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
        direct_rankings[fk] = {k: sum(v)/len(v) for k, v in groups.items() if v}

    # Recipe results for each definition and feature
    recipe_results = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        for dn, defn in DEFINITIONS.items():
            key = f"{fk} x {dn}"
            canon_etas = []
            canon_ranking_agrees = []
            pertask_etas = []
            pertask_ranking_agrees = []

            for seed in range(RECIPE_SEEDS):
                # Canonical recipe: shared active_roles
                canon_iter_etas = []
                canon_iter_agrees = []
                for it in range(RECIPE_ITERS):
                    random.seed(seed * RECIPE_ITERS + it)
                    active_roles = {r for r in defn["interactive_roles"] if random.random() < 0.5}

                    task_d_canon = {}
                    for t in tasks:
                        sample = t["locatable_sample"]
                        features = compute_per_element_features(sample)
                        feat_vals = features[fk]
                        total = sum(feat_vals[i]
                                    for i, elem in enumerate(sample)
                                    if apply_role_map(elem["role"], defn["role_map"]) in active_roles)
                        task_d_canon[t["task_id"]] = total / t["elements_with_bbox"]

                    g = defaultdict(list)
                    for t in tasks:
                        g[t["page_type"]].append(task_d_canon[t["task_id"]])
                    canon_iter_etas.append(_eta2(g))

                    if fk == "tag_entropy":
                        gmeans = {k: sum(v)/len(v) for k, v in g.items() if v}
                        canon_iter_agrees.append(check_ranking(direct_rankings[fk], gmeans, fk))

                canon_etas.append(mean(canon_iter_etas))
                if canon_iter_agrees:
                    canon_ranking_agrees.append(mean(canon_iter_agrees))

                # Per-task recipe: independent active_roles per task
                pertask_iter_etas = []
                pertask_iter_agrees = []
                for it in range(RECIPE_ITERS):
                    task_d_pertask = {}
                    for t in tasks:
                        random.seed(seed * RECIPE_ITERS + it + hash(t["task_id"]) % 100000)
                        active_roles_pt = {r for r in defn["interactive_roles"] if random.random() < 0.5}
                        sample = t["locatable_sample"]
                        features = compute_per_element_features(sample)
                        feat_vals = features[fk]
                        total = sum(feat_vals[i]
                                    for i, elem in enumerate(sample)
                                    if apply_role_map(elem["role"], defn["role_map"]) in active_roles_pt)
                        task_d_pertask[t["task_id"]] = total / t["elements_with_bbox"]

                    g = defaultdict(list)
                    for t in tasks:
                        g[t["page_type"]].append(task_d_pertask[t["task_id"]])
                    pertask_iter_etas.append(_eta2(g))

                    if fk == "tag_entropy":
                        gmeans = {k: sum(v)/len(v) for k, v in g.items() if v}
                        pertask_iter_agrees.append(check_ranking(direct_rankings[fk], gmeans, fk))

                pertask_etas.append(mean(pertask_iter_etas))
                if pertask_iter_agrees:
                    pertask_ranking_agrees.append(mean(pertask_iter_agrees))

            recipe_results[key] = {
                "canonical_eta2_mean": mean(canon_etas),
                "canonical_eta2_std": stdev(canon_etas) if len(canon_etas) > 1 else 0.0,
                "canonical_ranking_agreement_mean": mean(canon_ranking_agrees) if canon_ranking_agrees else None,
                "canonical_ranking_agreement_std": stdev(canon_ranking_agrees) if len(canon_ranking_agrees) > 1 else 0.0,
                "pertask_eta2_mean": mean(pertask_etas),
                "pertask_eta2_std": stdev(pertask_etas) if len(pertask_etas) > 1 else 0.0,
                "pertask_ranking_agreement_mean": mean(pertask_ranking_agrees) if pertask_ranking_agrees else None,
                "pertask_ranking_agreement_std": stdev(pertask_ranking_agrees) if len(pertask_ranking_agrees) > 1 else 0.0,
            }

    # Focus on tag_entropy x DEF-FULL-MAP
    key_main = "tag_entropy x DEF-FULL-MAP"
    canonical_agree = recipe_results[key_main]["canonical_ranking_agreement_mean"]
    pertask_agree = recipe_results[key_main]["pertask_ranking_agreement_mean"]
    print(f"\nCanonical recipe {key_main}: ranking_agree={canonical_agree}")
    print(f"Per-task recipe {key_main}: ranking_agree={pertask_agree}")

    # C5: full DOM exceeds truncated-first-20 by >=5pp (55.95% + 5pp = 60.95%)
    c5_pass = canonical_agree is not None and canonical_agree > 0.6095
    print(f"\nC5 (full DOM > 60.95%): pass={c5_pass}, canonical_agree={canonical_agree}")

    # C6: canonical recipe agreement >= 75%
    c6_pass = canonical_agree is not None and canonical_agree >= 0.75
    print(f"C6 (canonical >= 75%): pass={c6_pass}")

    # C7: per-task recipe agreement >= 85%
    c7_pass = pertask_agree is not None and pertask_agree >= 0.85
    print(f"C7 (per-task >= 85%): pass={c7_pass}")

    # =====================================================================
    # Bootstrap CI for canonical recipe ranking agreement
    # =====================================================================
    print("\n=== Bootstrap Ranking Agreement (tag_entropy x DEF-FULL-MAP, canonical recipe) ===")
    boot_agrees = []
    for b in range(B_BOOTSTRAP):
        boot_tasks = []
        for pt in ["product_listing", "detail"]:
            pt_tasks = [t for t in tasks if t["page_type"] == pt]
            sampled = [random.choice(pt_tasks) for _ in range(len(pt_tasks))]
            boot_tasks.extend(sampled)
        cart_tasks = [t for t in tasks if t["page_type"] == "cart"]
        if cart_tasks:
            boot_tasks.append(cart_tasks[0])

        # Compute bootstrap ranking agreement
        boot_features = {}
        for t in boot_tasks:
            boot_features[t["task_id"]] = compute_per_element_features(t["locatable_sample"])

        random.seed(b)
        active_roles = {r for r in DEFINITIONS["DEF-FULL-MAP"]["interactive_roles"] if random.random() < 0.5}
        task_d = {}
        for t in boot_tasks:
            sample = t["locatable_sample"]
            feat_vals = boot_features[t["task_id"]]["tag_entropy"]
            total = sum(feat_vals[i]
                        for i, elem in enumerate(sample)
                        if apply_role_map(elem["role"], DEFINITIONS["DEF-FULL-MAP"]["role_map"]) in active_roles)
            task_d[t["task_id"]] = total / t["elements_with_bbox"]

        g = defaultdict(list)
        for t in boot_tasks:
            g[t["page_type"]].append(task_d[t["task_id"]])
        gmeans = {k: sum(v)/len(v) for k, v in g.items() if v}
        boot_agrees.append(check_ranking(direct_rankings["tag_entropy"], gmeans, "tag_entropy"))

    boot_mean = mean(boot_agrees)
    boot_std = stdev(boot_agrees)
    boot_ci_lower = max(0, boot_mean - 1.96 * boot_std)
    boot_ci_upper = min(1, boot_mean + 1.96 * boot_std)
    print(f"Bootstrap mean: {boot_mean:.4f}, std: {boot_std:.4f}")
    print(f"Bootstrap 95% CI: [{boot_ci_lower:.4f}, {boot_ci_upper:.4f}]")

    # =====================================================================
    # Build result
    # =====================================================================
    result = {
        "c3_gate": {
            "tasks_with_locatable_sample_gt20": c3_tasks_with_full_dom,
            "total_tasks": c3_total_tasks,
            "threshold": 5,
            "pass": c3_pass,
            "element_counts": element_counts,
        },
        "pc1_positive_control": {
            "pass": pc1_pass,
            "features": pc1_results,
        },
        "nc1_null_control": {
            "pass": nc1_pass,
            "eta2": nc1_stats["eta2"],
            "group_means": nc1_stats["group_means"],
        },
        "non_recipe_pipeline": {
            "eta2": non_recipe_results,
            "max_eta2": max_eta2,
            "c4_pass": c4_pass,
        },
        "recipe_results": recipe_results,
        "c5_full_dom_exceeds_truncated": {
            "canonical_agreement": canonical_agree,
            "threshold": 0.6095,
            "pass": c5_pass,
        },
        "c6_ranking_stability": {
            "canonical_agreement": canonical_agree,
            "threshold": 0.75,
            "pass": c6_pass,
        },
        "c7_pertask_improves": {
            "pertask_agreement": pertask_agree,
            "threshold": 0.85,
            "pass": c7_pass,
        },
        "bootstrap_ci": {
            "mean": boot_mean,
            "std": boot_std,
            "ci_lower": boot_ci_lower,
            "ci_upper": boot_ci_upper,
            "n_bootstraps": B_BOOTSTRAP,
        },
        "verdict": {
            "c1_pass": pc1_pass,
            "c2_pass": nc1_pass,
            "c3_pass": c3_pass,
            "c4_pass": c4_pass,
            "c5_pass": c5_pass,
            "c6_pass": c6_pass,
            "c7_pass": c7_pass,
            "overall": pc1_pass and nc1_pass and c3_pass and c4_pass and c5_pass and c6_pass and c7_pass,
        }
    }

    # Save analysis output
    output_path = os.path.join(OUTPUT_DIR, "analysis_output.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nAnalysis output saved to {output_path}")

    # Print summary
    print("\n" + "="*60)
    print("VERDICT RULES:")
    print(f"  C1 (PC1): {'PASS' if pc1_pass else 'FAIL'}")
    print(f"  C2 (NC1): {'PASS' if nc1_pass else 'FAIL'}")
    print(f"  C3 (full DOM): {'PASS' if c3_pass else 'FAIL'}")
    print(f"  C4 (pipeline eta2): {'PASS' if c4_pass else 'FAIL'}")
    print(f"  C5 (exceeds truncated): {'PASS' if c5_pass else 'FAIL'}")
    print(f"  C6 (canonical >= 75%): {'PASS' if c6_pass else 'FAIL'}")
    print(f"  C7 (per-task >= 85%): {'PASS' if c7_pass else 'FAIL'}")
    print("="*60)


if __name__ == "__main__":
    main()