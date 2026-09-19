#!/usr/bin/env python3
"""EXP-INTEL-35445596324 — Sample-size effect on OECD/COINr pipeline ranking stability.

Tests whether ranking instability under recipe sampling (C4 FAIL in parent
EXP-INTEL-35434771791) is a sample-size artifact of truncated-first-20.

Design (frozen):
  - Effective sample sizes n ∈ {5, 10, 15, 20}: use first n elements from each task's locatable_sample
  - Recipe sampling at each n: canonical (shared subset p=0.5) and per-task (independent p=0.5 per task), 10 seeds × 1000 iterations
  - Bootstrap resampling at each n: B=1000, ranking agreement per bootstrap
  - Spearman correlation test for monotonic improvement (C5)
  - Ranking agreement threshold at n=20 (C6)
"""
import json, math, os, random
from collections import defaultdict
from statistics import mean, stdev

RAW_PATH = "research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json"
OUTPUT_DIR = "research/experiments/EXP-INTEL-35445596324"

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

EFFECTIVE_NS = [5, 10, 15, 20]
B_BOOTSTRAP = 1000
RECIPE_SEEDS = 10
RECIPE_ITERS = 1000

def apply_role_map(role, role_map):
    return role_map.get(role, role)

def elem_matches_def(elem, defn):
    canonical = apply_role_map(elem["role"], defn["role_map"])
    return canonical in defn["interactive_roles"]

def compute_per_element_features(locatable_sample):
    """Per-element features: tag_entropy, form_fraction, total_area."""
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

def check_ranking(direct_means, pipeline_means, feat_key):
    """Check if pipeline preserves listing > detail for tag_entropy."""
    # Expected direct ranking for tag_entropy: listing > detail (listing_mean > detail_mean)
    # We check listing vs detail ordering is preserved
    dl = direct_means.get("product_listing", 0)
    dd = direct_means.get("detail", 0)
    pl = pipeline_means.get("product_listing", 0)
    pd = pipeline_means.get("detail", 0)
    # Both should have listing > detail
    return (dl > dd) == (pl > pd)

def main():
    with open(RAW_PATH) as f:
        raw = json.load(f)

    # Filter tasks (same as parent)
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

    # Compute task-level direct features (for ranking reference)
    task_direct_features = {}
    for t in tasks:
        sample = t["locatable_sample"]
        tag_counts = defaultdict(int)
        for elem in sample:
            tag_counts[elem["tag"]] += 1
        total = len(sample)
        t["tag_entropy"] = sum(-c/total * math.log2(c/total) for c in tag_counts.values() if c > 0)
        t["form_fraction"] = sum(1 for e in sample if e.get("inForm", False)) / total
        t["total_area"] = sum(e["w"] * e["h"] for e in sample)
        task_direct_features[t["task_id"]] = compute_per_element_features(t["locatable_sample"])

    # Direct rankings (from all 20 elements)
    direct_rankings = {}
    for fk in ["tag_entropy", "form_fraction", "total_area"]:
        groups = defaultdict(list)
        for t in tasks:
            groups[t["page_type"]].append(t[fk])
        means = {k: sum(v)/len(v) for k, v in groups.items()}
        direct_rankings[fk] = means

    print(f"Tasks: {len(tasks)}")
    for t in tasks:
        print(f"  {t['task_id']}: {t['page_type']}, ewb={t['elements_with_bbox']}, "
              f"sample_size={len(t['locatable_sample'])}, "
              f"tag_ent={t['tag_entropy']:.4f}, form_frac={t['form_fraction']:.2f}, total_area={t['total_area']:.1f}")

    # ============================================================
    # PC1: Direct feature eta2 (full sample)
    # ============================================================
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

    # ============================================================
    # NC1: Normalized hierarchy density
    # ============================================================
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

    # ============================================================
    # Subsample analysis at each effective_n
    # ============================================================
    subsample_results = {}

    for n_eff in EFFECTIVE_NS:
        print(f"\n=== Effective N = {n_eff} ===")
        n_results = {
            "pipeline_eta2": {},
            "pipeline_stats": {},
            "non_recipe_ranking_agreement": {},
            "recipe_canonical_ranking_agreement_mean": {},
            "recipe_canonical_ranking_agreement_std": {},
            "recipe_canonical_eta2_mean": {},
            "recipe_canonical_eta2_std": {},
            "recipe_pertask_ranking_agreement_mean": {},
            "recipe_pertask_ranking_agreement_std": {},
            "recipe_pertask_eta2_mean": {},
            "recipe_pertask_eta2_std": {},
        }

        # Compute per-element features on the subsample (first n elements)
        subsample_features = {}
        for t in tasks:
            subsample = t["locatable_sample"][:n_eff]
            subsample_features[t["task_id"]] = compute_per_element_features(subsample)

        # Non-recipe pipeline: feature-weighted density eta2
        for fk in ["tag_entropy", "form_fraction", "total_area"]:
            for dn, defn in DEFINITIONS.items():
                key = f"{fk} x {dn}"
                densities = {}
                for t in tasks:
                    subsample = t["locatable_sample"][:n_eff]
                    d = compute_feature_weighted_density(subsample, subsample_features[t["task_id"]],
                                                          t["elements_with_bbox"], defn)
                    densities[t["task_id"]] = d[fk]
                groups = defaultdict(list)
                for t in tasks:
                    groups[t["page_type"]].append(densities[t["task_id"]])
                n_results["pipeline_eta2"][key] = _eta2(groups)
                n_results["pipeline_stats"][key] = _stats(groups)

                # Non-recipe ranking agreement for tag_entropy
                if fk == "tag_entropy":
                    pipeline_means = n_results["pipeline_stats"][key]["group_means"]
                    n_results["non_recipe_ranking_agreement"][key] = check_ranking(
                        direct_rankings[fk], pipeline_means, fk)

        # Print non-recipe results
        for key in ["tag_entropy x DEF-FULL-MAP", "tag_entropy x DEF-FORM-ONLY"]:
            eta = n_results["pipeline_eta2"][key]
            agree = n_results["non_recipe_ranking_agreement"].get(key, "N/A")
            print(f"  Non-recipe {key}: eta2={eta:.6f}, ranking_agree={agree}")

        # ============================================================
        # Recipe sampling at this effective_n
        # ============================================================
        # Canonical recipe: shared subset p=0.5 (same roles sampled for all tasks)
        # Per-task recipe: independent p=0.5 per task
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
                            subsample = t["locatable_sample"][:n_eff]
                            feat_vals = subsample_features[t["task_id"]][fk]
                            total = sum(feat_vals[i]
                                        for i, elem in enumerate(subsample)
                                        if apply_role_map(elem["role"], defn["role_map"]) in active_roles)
                            task_d_canon[t["task_id"]] = total / t["elements_with_bbox"]

                        g = defaultdict(list)
                        for t in tasks:
                            g[t["page_type"]].append(task_d_canon[t["task_id"]])
                        canon_iter_etas.append(_eta2(g))

                        # Ranking agreement for tag_entropy
                        if fk == "tag_entropy":
                            gmeans = {k: sum(v)/len(v) for k, v in g.items() if v}
                            canon_iter_agrees.append(check_ranking(direct_rankings[fk], gmeans, fk))

                    canon_etas.append(sum(canon_iter_etas) / len(canon_iter_etas))
                    if canon_iter_agrees:
                        canon_ranking_agrees.append(sum(canon_iter_agrees) / len(canon_iter_agrees))

                    # Per-task recipe: independent active_roles per task
                    pertask_iter_etas = []
                    pertask_iter_agrees = []
                    for it in range(RECIPE_ITERS):
                        task_d_pertask = {}
                        for t in tasks:
                            random.seed(seed * RECIPE_ITERS + it + hash(t["task_id"]) % 100000)
                            active_roles_pt = {r for r in defn["interactive_roles"] if random.random() < 0.5}
                            subsample = t["locatable_sample"][:n_eff]
                            feat_vals = subsample_features[t["task_id"]][fk]
                            total = sum(feat_vals[i]
                                        for i, elem in enumerate(subsample)
                                        if apply_role_map(elem["role"], defn["role_map"]) in active_roles_pt)
                            task_d_pertask[t["task_id"]] = total / t["elements_with_bbox"]

                        g = defaultdict(list)
                        for t in tasks:
                            g[t["page_type"]].append(task_d_pertask[t["task_id"]])
                        pertask_iter_etas.append(_eta2(g))

                        if fk == "tag_entropy":
                            gmeans = {k: sum(v)/len(v) for k, v in g.items() if v}
                            pertask_iter_agrees.append(check_ranking(direct_rankings[fk], gmeans, fk))

                    pertask_etas.append(sum(pertask_iter_etas) / len(pertask_iter_etas))
                    if pertask_iter_agrees:
                        pertask_ranking_agrees.append(sum(pertask_iter_agrees) / len(pertask_iter_agrees))

                # Aggregate across seeds
                n_results["recipe_canonical_eta2_mean"][key] = mean(canon_etas)
                n_results["recipe_canonical_eta2_std"][key] = stdev(canon_etas) if len(canon_etas) > 1 else 0.0
                n_results["recipe_pertask_eta2_mean"][key] = mean(pertask_etas)
                n_results["recipe_pertask_eta2_std"][key] = stdev(pertask_etas) if len(pertask_etas) > 1 else 0.0

                if canon_ranking_agrees:
                    n_results["recipe_canonical_ranking_agreement_mean"][key] = mean(canon_ranking_agrees)
                    n_results["recipe_canonical_ranking_agreement_std"][key] = stdev(canon_ranking_agrees) if len(canon_ranking_agrees) > 1 else 0.0
                else:
                    n_results["recipe_canonical_ranking_agreement_mean"][key] = None
                    n_results["recipe_canonical_ranking_agreement_std"][key] = None

                if pertask_ranking_agrees:
                    n_results["recipe_pertask_ranking_agreement_mean"][key] = mean(pertask_ranking_agrees)
                    n_results["recipe_pertask_ranking_agreement_std"][key] = stdev(pertask_ranking_agrees) if len(pertask_ranking_agrees) > 1 else 0.0
                else:
                    n_results["recipe_pertask_ranking_agreement_mean"][key] = None
                    n_results["recipe_pertask_ranking_agreement_std"][key] = None

        # Print recipe results for tag_entropy x DEF-FULL-MAP
        key = "tag_entropy x DEF-FULL-MAP"
        print(f"  Canonical recipe {key}: eta2={n_results['recipe_canonical_eta2_mean'][key]:.4f} ± "
              f"{n_results['recipe_canonical_eta2_std'][key]:.4f}, "
              f"ranking_agree={n_results['recipe_canonical_ranking_agreement_mean'][key]}")
        print(f"  Per-task recipe {key}: eta2={n_results['recipe_pertask_eta2_mean'][key]:.4f} ± "
              f"{n_results['recipe_pertask_eta2_std'][key]:.4f}, "
              f"ranking_agree={n_results['recipe_pertask_ranking_agreement_mean'][key]}")

        key2 = "tag_entropy x DEF-FORM-ONLY"
        print(f"  Canonical recipe {key2}: eta2={n_results['recipe_canonical_eta2_mean'][key2]:.4f} ± "
              f"{n_results['recipe_canonical_eta2_std'][key2]:.4f}, "
              f"ranking_agree={n_results['recipe_canonical_ranking_agreement_mean'][key2]}")

        subsample_results[n_eff] = n_results

    # ============================================================
    # Bootstrap ranking agreement at each effective_n
    # ============================================================
    print("\n=== Bootstrap Ranking Agreement (tag_entropy x DEF-FULL-MAP, canonical recipe) ===")
    bootstrap_results = {}
    for n_eff in EFFECTIVE_NS:
        boot_agrees = []
        for b in range(B_BOOTSTRAP):
            # Bootstrap: sample tasks with replacement within each page_type
            boot_tasks = []
            for pt in ["product_listing", "detail"]:
                pt_tasks = [t for t in tasks if t["page_type"] == pt]
                sampled = [random.choice(pt_tasks) for _ in range(len(pt_tasks))]
                boot_tasks.extend(sampled)
            # Cart n=1, always include
            cart_tasks = [t for t in tasks if t["page_type"] == "cart"]
            if cart_tasks:
                boot_tasks.append(cart_tasks[0])

            # Compute bootstrap ranking agreement for tag_entropy x DEF-FULL-MAP
            subsample_features_boot = {}
            for t in boot_tasks:
                subsample = t["locatable_sample"][:n_eff]
                subsample_features_boot[t["task_id"]] = compute_per_element_features(subsample)

            # Canonical recipe (one iteration per bootstrap)
            random.seed(b)
            active_roles = {r for r in DEFINITIONS["DEF-FULL-MAP"]["interactive_roles"] if random.random() < 0.5}
            task_d = {}
            for t in boot_tasks:
                subsample = t["locatable_sample"][:n_eff]
                feat_vals = subsample_features_boot[t["task_id"]]["tag_entropy"]
                total = sum(feat_vals[i]
                            for i, elem in enumerate(subsample)
                            if apply_role_map(elem["role"], DEFINITIONS["DEF-FULL-MAP"]["role_map"]) in active_roles)
                task_d[t["task_id"]] = total / t["elements_with_bbox"]

            g = defaultdict(list)
            for t in boot_tasks:
                g[t["page_type"]].append(task_d[t["task_id"]])
            gmeans = {k: sum(v)/len(v) for k, v in g.items() if v}
            boot_agrees.append(check_ranking(direct_rankings["tag_entropy"], gmeans, "tag_entropy"))

        bootstrap_results[n_eff] = {
            "mean": mean(boot_agrees),
            "std": stdev(boot_agrees) if len(boot_agrees) > 1 else 0.0,
            "n_true": sum(boot_agrees),
            "n_total": len(boot_agrees),
        }
        print(f"  n={n_eff}: agree={bootstrap_results[n_eff]['mean']:.4f} ± "
              f"{bootstrap_results[n_eff]['std']:.4f} ({sum(boot_agrees)}/{len(boot_agrees)})")

    # ============================================================
    # Decision Rule C5: Sample Size Effect
    # ============================================================
    print("\n=== C5: Sample Size Effect ===")
    # Use canonical recipe ranking agreement for tag_entropy x DEF-FULL-MAP
    agree_values = []
    for n_eff in EFFECTIVE_NS:
        val = subsample_results[n_eff]["recipe_canonical_ranking_agreement_mean"].get("tag_entropy x DEF-FULL-MAP")
        agree_values.append(val if val is not None else 0.0)

    print(f"  Effective ns: {EFFECTIVE_NS}")
    print(f"  Ranking agreement: {agree_values}")

    # Spearman correlation (rank-based)
    def spearman_correlation(x, y):
        n = len(x)
        rx = [sorted(range(n), key=lambda i: x[i]).index(i) for i in range(n)]
        ry = [sorted(range(n), key=lambda i: y[i]).index(i) for i in range(n)]
        d_sq = sum((rx[i] - ry[i])**2 for i in range(n))
        return 1 - 6 * d_sq / (n * (n**2 - 1))

    spearman_corr = spearman_correlation(EFFECTIVE_NS, agree_values)
    print(f"  Spearman correlation: {spearman_corr:.4f}")

    # (b) agreement at n=20 >= agreement at n=5 + 0.10
    improve = agree_values[-1] - agree_values[0]
    print(f"  Improvement n=20 vs n=5: {improve:.4f} (need >= 0.10)")

    c5_spearman = spearman_corr >= 0.6
    c5_improve = improve >= 0.10
    c5_pass = c5_spearman and c5_improve
    print(f"  C5 PASS: {c5_pass} (spearman={c5_spearman}, improve={c5_improve})")

    # ============================================================
    # Decision Rule C6: Ranking Stability at Full Effective_n
    # ============================================================
    print("\n=== C6: Ranking Stability at Full Effective_n (n=20) ===")
    c6_agree = subsample_results[20]["recipe_canonical_ranking_agreement_mean"].get("tag_entropy x DEF-FULL-MAP")
    print(f"  Canonical recipe tag_entropy x DEF-FULL-MAP agreement at n=20: {c6_agree}")
    c6_pass = c6_agree is not None and c6_agree >= 0.80
    print(f"  C6 PASS: {c6_pass}")

    # ============================================================
    # Full decision rule evaluation
    # ============================================================
    print("\n=== Full Decision Rules ===")
    max_pipeline_eta2 = max(v for v in subsample_results[20]["pipeline_eta2"].values()) if subsample_results[20]["pipeline_eta2"] else 0.0

    c1 = pc1_pass
    c2 = nc1_pass
    c3 = max_pipeline_eta2 >= 0.05
    # C4: Natural ranking preserved at n=20, non-recipe, for tag_entropy both definitions
    c4_te_fmap = subsample_results[20]["non_recipe_ranking_agreement"].get("tag_entropy x DEF-FULL-MAP", False)
    c4_te_fonly = subsample_results[20]["non_recipe_ranking_agreement"].get("tag_entropy x DEF-FORM-ONLY", False)
    c4 = c4_te_fmap and c4_te_fonly
    c5 = c5_pass
    c6 = c6_pass

    print(f"  C1 (raw reproduce): {c1}")
    print(f"  C2 (hierarchy anchor): {c2}")
    print(f"  C3 (pipeline non-zero, max={max_pipeline_eta2:.6f}): {c3}")
    print(f"  C4 (natural ranking preserved): {c4} (DEF-FULL-MAP={c4_te_fmap}, DEF-FORM-ONLY={c4_te_fonly})")
    print(f"  C5 (sample size effect): {c5} (spearman={spearman_corr:.4f}, improve={improve:.4f})")
    print(f"  C6 (ranking stability at n=20): {c6} (agree={c6_agree})")

    if not c1:
        verdict, reason = "MEASUREMENT_INVALID", "C1 FAIL: raw features don't reproduce."
    elif not c2:
        verdict, reason = "MEASUREMENT_INVALID", "C2 FAIL: hierarchy anchor fails."
    elif not c3:
        verdict, reason = "FALSIFIES", f"C3 FAIL: pipeline collapses ALL discrimination at n=20. Max eta2={max_pipeline_eta2:.6f}"
    elif not c4:
        verdict, reason = "MIXED", "C4 FAIL: pipeline doesn't preserve natural ranking at n=20."
    elif not c5:
        verdict, reason = "MIXED", f"C5 FAIL: sample-size effect not confirmed. Spearman={spearman_corr:.4f}, improve={improve:.4f}"
    elif not c6:
        verdict, reason = "MIXED", f"C6 FAIL: ranking agreement at n=20 is {c6_agree}, below 80% threshold."
    else:
        verdict, reason = "SURVIVES", f"All C1-C6 pass. Sample-size artifact confirmed. Max pipeline eta2={max_pipeline_eta2:.6f}"

    print(f"\n  VERDICT: {verdict}")
    print(f"  REASON: {reason}")

    # ============================================================
    # Build output
    # ============================================================
    # Convert subsample_results to serializable format
    serializable_subsample = {}
    for n_eff, nr in subsample_results.items():
        serializable_subsample[str(n_eff)] = {
            "pipeline_eta2": nr["pipeline_eta2"],
            "non_recipe_ranking_agreement": nr["non_recipe_ranking_agreement"],
            "recipe_canonical_eta2_mean": nr["recipe_canonical_eta2_mean"],
            "recipe_canonical_eta2_std": nr["recipe_canonical_eta2_std"],
            "recipe_canonical_ranking_agreement_mean": nr["recipe_canonical_ranking_agreement_mean"],
            "recipe_canonical_ranking_agreement_std": nr["recipe_canonical_ranking_agreement_std"],
            "recipe_pertask_eta2_mean": nr["recipe_pertask_eta2_mean"],
            "recipe_pertask_eta2_std": nr["recipe_pertask_eta2_std"],
            "recipe_pertask_ranking_agreement_mean": nr["recipe_pertask_ranking_agreement_mean"],
            "recipe_pertask_ranking_agreement_std": nr["recipe_pertask_ranking_agreement_std"],
        }

    output = {
        "tasks_used": [{"task_id": t["task_id"], "page_type": t["page_type"],
                        "elements_with_bbox": t["elements_with_bbox"],
                        "locatable_count": len(t["locatable_sample"]),
                        "tag_entropy": t["tag_entropy"],
                        "form_fraction": t["form_fraction"],
                        "total_area": t["total_area"]} for t in tasks],
        "pc1_direct_eta2": {fk: {"eta2": pc1[fk]["eta2"], "group_means": pc1[fk]["group_means"],
                                  "within_stds": pc1[fk]["within_stds"]} for fk in pc1},
        "nc1_hierarchy": {"densities": hier_densities, "stats": hier_stats},
        "subsample_results": serializable_subsample,
        "bootstrap_results": {str(k): v for k, v in bootstrap_results.items()},
        "c5_spearman_correlation": spearman_corr,
        "c5_ranking_agreement_values": {str(n): v for n, v in zip(EFFECTIVE_NS, agree_values)},
        "c5_improvement": improve,
        "c5_pass": c5_pass,
        "c6_agreement_at_n20": c6_agree,
        "c6_pass": c6_pass,
        "decision_rules": {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5, "C6": c6,
                           "verdict": verdict, "reason": reason},
    }

    with open(os.path.join(OUTPUT_DIR, "analysis_output.json"), "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nOutput written to {OUTPUT_DIR}/analysis_output.json")

if __name__ == "__main__":
    main()
