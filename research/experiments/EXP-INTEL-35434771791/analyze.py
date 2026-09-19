#!/usr/bin/env python3
"""EXP-INTEL-35434771791 OECD/COINr pipeline feature discrimination test."""
import json, math, os, random
from collections import defaultdict

RAW_PATH = "research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json"
OUTPUT_DIR = "research/experiments/EXP-INTEL-35434771791"

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
    "ISOLATED-A-LINK": {
        "interactive_roles": {"link"},
        "role_map": {}
    },
}

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

def compute_feature_weighted_density(locatable_sample, elem_features, ewb, defn):
    densities = {}
    for feat_key, feat_vals in elem_features.items():
        total = sum(feat_vals[i] for i, elem in enumerate(locatable_sample) if elem_matches_def(elem, defn))
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
        return {"eta2": 0.0, "group_means": {}, "grand_mean": 0.0, "within_stds": {}, "ss_between": 0.0, "ss_within": 0.0}
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
    return {"eta2": eta2, "group_means": means, "grand_mean": gm, "within_stds": stds, "ss_between": ss_between, "ss_within": ss_within}

def main():
    with open(RAW_PATH) as f:
        raw = json.load(f)

    measurements = [m for m in raw["measurements"] if m.get("error") is None and m.get("http_status") == 200]
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

    tasks = [m for m in measurements if m["page_type"] == "product_listing"][:3] + \
            [m for m in measurements if m["page_type"] == "detail"][:3] + \
            [m for m in measurements if m["page_type"] == "cart"][:1]

    for t in tasks:
        sample = t["locatable_sample"]
        tag_counts = defaultdict(int)
        for elem in sample:
            tag_counts[elem["tag"]] += 1
        total = len(sample)
        t["tag_entropy"] = sum(-c/total * math.log2(c/total) for c in tag_counts.values() if c > 0)
        t["form_fraction"] = sum(1 for e in sample if e.get("inForm", False)) / total
        t["total_area"] = sum(e["w"] * e["h"] for e in sample)

    task_features = {t["task_id"]: compute_per_element_features(t["locatable_sample"]) for t in tasks}

    print(f"Tasks: {len(tasks)}")
    for t in tasks:
        print(f"  {t['task_id']}: {t['page_type']}, ewb={t['elements_with_bbox']}, "
              f"tag_ent={t['tag_entropy']:.4f}, form_frac={t['form_fraction']:.2f}, total_area={t['total_area']:.1f}")

    # PC1: Direct feature eta2
    print("\n=== PC1: Direct Feature eta2 ===")
    pc1 = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        groups = defaultdict(list)
        for t in tasks:
            groups[t["page_type"]].append(t[fk])
        pc1[fk] = _stats(groups)
        print(f"  {fk}: eta2={pc1[fk]['eta2']:.6f}, means={pc1[fk]['group_means']}, stds={pc1[fk]['within_stds']}")
    pc1_pass = all(pc1[f]["eta2"] >= 0.99 and all(s < 0.001 for s in pc1[f]["within_stds"].values()) for f in pc1)
    print(f"  PC1 PASS: {pc1_pass}")

    # NC1: Normalized hierarchy density
    print("\n=== NC1: Normalized Hierarchy Density ===")
    alpha = 0.3
    hier_densities = {}
    for t in tasks:
        sample = t["locatable_sample"]
        total_weight = sum(math.exp(-alpha * e["y"]) for e in sample)
        weighted_sum = sum(math.exp(-alpha * e["y"]) for e in sample if e.get("inForm", False))
        hier_densities[t["task_id"]] = weighted_sum / total_weight if total_weight > 0 else 0.0
    hier_groups = defaultdict(list)
    for t in tasks:
        hier_groups[t["page_type"]].append(hier_densities[t["task_id"]])
    hier_stats = _stats(hier_groups)
    nc1_pass = hier_stats["eta2"] < 0.01
    print(f"  eta2={hier_stats['eta2']:.10f}, means={hier_stats['group_means']}")
    print(f"  NC1 PASS: {nc1_pass}")

    # Pipeline: feature-weighted density eta2 by feature x definition
    print("\n=== Pipeline eta2 by Feature x Definition ===")
    pipeline_eta2 = {}
    pipeline_stats = {}
    pipeline_densities = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        for dn, defn in DEFINITIONS.items():
            densities = {}
            for t in tasks:
                d = compute_feature_weighted_density(t["locatable_sample"], task_features[t["task_id"]], t["elements_with_bbox"], defn)
                densities[t["task_id"]] = d[fk]
            groups = defaultdict(list)
            for t in tasks:
                groups[t["page_type"]].append(densities[t["task_id"]])
            key = f"{fk} x {dn}"
            pipeline_eta2[key] = _eta2(groups)
            pipeline_stats[key] = _stats(groups)
            pipeline_densities[key] = densities
            print(f"  {key}: eta2={pipeline_eta2[key]:.6f}, means={pipeline_stats[key]['group_means']}")

    # Recipe sampling
    print("\n=== Recipe-Sampled eta2 (10 seeds x 1000 iter) ===")
    recipe_results = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        for dn, defn in DEFINITIONS.items():
            key = f"{fk} x {dn}"
            canon_etas = []
            for seed in range(10):
                iter_etas = []
                for it in range(1000):
                    random.seed(seed * 1000 + it)
                    active_roles = {r for r in defn["interactive_roles"] if random.random() < 0.5}
                    task_d = {}
                    for t in tasks:
                        total = sum(task_features[t["task_id"]][fk][i]
                                    for i, elem in enumerate(t["locatable_sample"])
                                    if apply_role_map(elem["role"], defn["role_map"]) in active_roles)
                        task_d[t["task_id"]] = total / t["elements_with_bbox"]
                    g = defaultdict(list)
                    for t in tasks:
                        g[t["page_type"]].append(task_d[t["task_id"]])
                    iter_etas.append(_eta2(g))
                canon_etas.append(sum(iter_etas) / len(iter_etas))
            recipe_results[key] = {"mean": sum(canon_etas)/len(canon_etas), "std": (sum((e-sum(canon_etas)/len(canon_etas))**2 for e in canon_etas)/len(canon_etas))**0.5}
            print(f"  {key}: canonical={recipe_results[key]['mean']:.4f} +/- {recipe_results[key]['std']:.4f}")

    # Ranking analysis
    print("\n=== Ranking Analysis ===")
    direct_rankings = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        groups = defaultdict(list)
        for t in tasks:
            groups[t["page_type"]].append(t[fk])
        means = {k: sum(v)/len(v) for k, v in groups.items()}
        direct_rankings[fk] = sorted(means.keys(), key=lambda k: -means[k])
        print(f"  Direct {fk}: {direct_rankings[fk]}")

    ranking_agreement = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        for dn in DEFINITIONS:
            key = f"{fk} x {dn}"
            pr = sorted(pipeline_stats[key]["group_means"].keys(), key=lambda k: -pipeline_stats[key]["group_means"][k])
            dr = direct_rankings[fk]
            agree = (pr.index("product_listing") - pr.index("detail")) * (dr.index("product_listing") - dr.index("detail")) > 0
            ranking_agreement[key] = agree
            print(f"  {key}: pipeline={pr}, agree={agree}")

    # Decision rules
    print("\n=== Decision Rules ===")
    max_pipeline_eta2 = max(pipeline_eta2.values()) if pipeline_eta2 else 0.0
    c1 = pc1_pass
    c2 = nc1_pass
    c3 = max_pipeline_eta2 >= 0.05
    c4 = any(all(ranking_agreement.get(f"{f} x {d}", False) for d in DEFINITIONS) for f in ["tag_entropy", "form_fraction", "total_area"])
    c5 = max_pipeline_eta2 > hier_stats["eta2"] + 0.01

    print(f"  C1 (raw reproduce): {c1}")
    print(f"  C2 (hierarchy anchor): {c2}")
    print(f"  C3 (pipeline non-zero, max={max_pipeline_eta2:.6f}): {c3}")
    print(f"  C4 (ranking preserved): {c4}")
    print(f"  C5 (feature > hierarchy): {c5}")

    if not c1:
        verdict, reason = "MEASUREMENT_INVALID", "C1 FAIL: raw features dont reproduce."
    elif not c2:
        verdict, reason = "MEASUREMENT_INVALID", "C2 FAIL: hierarchy anchor fails."
    elif not c3:
        verdict, reason = "FALSIFIES", f"C3 FAIL: pipeline collapses ALL discrimination. Max eta2={max_pipeline_eta2:.6f}"
    elif not c4:
        verdict, reason = "MIXED", "C4 FAIL: pipeline reverses ranking for all features."
    elif not c5:
        verdict, reason = "MIXED", f"C5 FAIL: max feature eta2={max_pipeline_eta2:.6f} not > hierarchy + 0.01."
    else:
        verdict, reason = "SURVIVES", f"All C1-C5 pass. Max pipeline eta2={max_pipeline_eta2:.6f}"

    print(f"\n  VERDICT: {verdict}")
    print(f"  REASON: {reason}")

    # Build full output
    metrics_9 = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        for dn in DEFINITIONS:
            key = f"{fk} x {dn}"
            metrics_9[key] = {"eta2": pipeline_eta2[key], "group_means": pipeline_stats[key]["group_means"], "within_stds": pipeline_stats[key]["within_stds"], "grand_mean": pipeline_stats[key]["grand_mean"]}

    output = {
        "tasks_used": [{"task_id": t["task_id"], "page_type": t["page_type"], "elements_with_bbox": t["elements_with_bbox"], "locatable_count": len(t["locatable_sample"]),
                        "tag_entropy": t["tag_entropy"], "form_fraction": t["form_fraction"], "total_area": t["total_area"]} for t in tasks],
        "pc1_direct_eta2": pc1,
        "nc1_hierarchy": {"densities": hier_densities, "stats": hier_stats},
        "pipeline_eta2_9": metrics_9,
        "recipe_results": recipe_results,
        "direct_rankings": direct_rankings,
        "ranking_agreement": ranking_agreement,
        "decision_rules": {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5, "verdict": verdict, "reason": reason},
    }
    with open(os.path.join(OUTPUT_DIR, "analysis_output.json"), "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nOutput written to {OUTPUT_DIR}/analysis_output.json")

if __name__ == "__main__":
    main()
