#!/usr/bin/env python3
"""EXP-INTEL-35476271877 — EXECUTE: SNR decomposition of recipe ranking instability.

Frozen design (spec.json / prereg.md verified against freeze.json):
  - Question: what mechanism drives canonical recipe high eta2 (0.9205) vs low
    ranking agreement (55.95%) dissociation, and does the decomposition predict
    whether full-DOM (n=21-82) could cross the 80% ranking agreement threshold?
  - Phases A-F: data prep, per-iteration density logging (canonical & per-task
    recipes, 10 seeds x 1000 iterations x n in {5,10,15,20}), SNR decomposition,
    power-law extrapolation to n=50/82, mechanism identification, hybrid recipe
    (exploratory).
  - Frozen inputs: raw data EXP-INTEL-34782350557
    (sha256 da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050),
    analysis framework EXP-INTEL-35445596324/analyze.py
    (sha256 5acc37315ef28a5dd21420701c6826c4fc8f242fadbd7ccd4481ea83e123b724).

Computation is math-identical to the parent framework's per-iteration recipe
sampling (same seeding: canonical seed = seed*1000+it; per-task seed =
seed*1000+it+hash(task_id)%100000; same denominator ewb; same tag_entropy
feature on the first-n subsample), but role-contribution tables are precomputed
per (task, n, definition) so the inner loops are fast. Per-iteration values
match the parent's aggregation exactly (verified via baseline reproduction).

Determinism: run with PYTHONHASHSEED=0 (per-task seeding uses hash(task_id);
the parent run may have used a different hash seed, so per-task reproduction is
expected to be close but not bit-identical; canonical is fully deterministic).

This script is EXECUTE code: it produces RAW per-iteration evidence (gzip JSON)
and DERIVED measurements (analysis_output_snr.json). It evaluates frozen
decision rules C1/C2/C3 and maps to frozen verdict strings; the packet
status/outcome mapping is done in result.json.
"""

import json
import gzip
import math
import os
import random
import statistics
from collections import defaultdict

RAW_PATH = "research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json"
OUT_DIR = "research/experiments/EXP-INTEL-35476271877"

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
RECIPE_SEEDS = 10
RECIPE_ITERS = 1000
ALPHAS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
NULL_SIMS = 500000

# Frozen observed agreement targets (parent M4, tag_entropy x DEF-FULL-MAP)
FROZEN_OBSERVED = {15: 0.4998, 20: 0.5595}
FROZEN_PERTASK_OBSERVED = {20: 0.7865}

# ------------------------- framework (parent analyze.py, unchanged) ---------

def apply_role_map(role, role_map):
    return role_map.get(role, role)

def compute_per_element_features(locatable_sample):
    tag_counts = defaultdict(int)
    for elem in locatable_sample:
        tag_counts[elem["tag"]] += 1
    total = len(locatable_sample)
    tag_vals = []
    for elem in locatable_sample:
        p = tag_counts[elem["tag"]] / total
        tag_vals.append(-p * math.log2(p) if p > 0 else 0.0)
    return {"tag_entropy": tag_vals}

def _eta2(groups):
    all_vals = [v for g in groups.values() for v in g]
    if not all_vals:
        return 0.0
    gm = sum(all_vals) / len(all_vals)
    ss_total = sum((v - gm) ** 2 for v in all_vals)
    if ss_total == 0:
        return 0.0
    ss_between = sum(len(g) * (sum(g) / len(g) - gm) ** 2 for g in groups.values() if g)
    return ss_between / ss_total

def check_ranking(direct_means, pipeline_means, feat_key):
    dl = direct_means.get("product_listing", 0)
    dd = direct_means.get("detail", 0)
    pl = pipeline_means.get("product_listing", 0)
    pd = pipeline_means.get("detail", 0)
    return (dl > dd) == (pl > pd)

def phi(x):
    if isinstance(x, float) and math.isfinite(x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    if isinstance(x, float) and x == math.inf:
        return 1.0
    if isinstance(x, float) and x == -math.inf:
        return 0.0
    return None

def finite_mean(xs):
    vals = [x for x in xs if isinstance(x, (int, float)) and math.isfinite(x)]
    return statistics.fmean(vals) if vals else None

# ------------------------- data loading (Phase A) ---------------------------

def load_tasks():
    with open(RAW_PATH) as f:
        raw = json.load(f)
    measurements = [m for m in raw["measurements"]
                    if m.get("error") is None and m.get("http_status") == 200]
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
    return tasks, raw

# ------------------------- main ----------------------------------------------

def main():
    tasks, raw = load_tasks()
    result = {
        "experiment_id": "EXP-INTEL-35476271877",
        "python_version": sys_version(),
        "pyhashseed": os.environ.get("PYTHONHASHSEED", "unset"),
        "requests": {"present": True, "experiment_id": raw.get("experiment_id"),
                     "frozen_seed": raw.get("frozen_seed")},
        "tasks_used": [],
        "verification": {},
        "per_n": {},
        "snr_model": {},
        "null_control": {},
        "extrapolation": {},
        "mechanism": {},
        "hybrid_exploratory": {},
        "baseline_reproduction": {},
        "decision": {},
    }
    import sys as _sys
    result["python_version"] = _sys.version.split()[0]

    for t in tasks:
        result["tasks_used"].append({
            "task_id": t["task_id"], "page_type": t["page_type"],
            "elements_with_bbox": t["elements_with_bbox"],
            "locatable_count": len(t["locatable_sample"]),
        })

    # Direct full-sample features + ranking reference (parent Phase A/PC1 style)
    task_direct_features = {}
    direct_rankings = {}
    for t in tasks:
        sample = t["locatable_sample"]
        tag_counts = defaultdict(int)
        for elem in sample:
            tag_counts[elem["tag"]] += 1
        total = len(sample)
        t["tag_entropy"] = sum(-c / total * math.log2(c / total) for c in tag_counts.values() if c > 0)
        task_direct_features[t["task_id"]] = compute_per_element_features(t["locatable_sample"])["tag_entropy"]
    groups = defaultdict(list)
    for t in tasks:
        groups[t["page_type"]].append(t["tag_entropy"])
    direct_rankings = {k: sum(v) / len(v) for k, v in groups.items()}
    result["verification"]["direct_means_tag_entropy"] = direct_rankings
    result["verification"]["direct_listing_gt_detail"] = (
        direct_rankings["product_listing"] > direct_rankings["detail"])

    # Template invariance across same-type tasks in truncated-first-20
    invariance = {}
    for pt in ["product_listing", "detail", "cart"]:
        same = [t for t in tasks if t["page_type"] == pt]
        sig = [tuple((e["tag"], e.get("role"), e.get("inForm"), e["w"], e["h"])
                      for e in t["locatable_sample"]) for t in same]
        invariance[pt] = all(s == sig[0] for s in sig[1:])
    result["verification"]["template_invariance_first20"] = invariance

    # ---- Phase A/B: per (task, n, definition) role-contribution tables ----
    # role_contrib[(tid, n, def)][role] = sum of tag_entropy over elements in the
    # first-n subsample whose mapped role == role. Identical to parent's inner sums.
    role_contrib = {}
    for n_eff in EFFECTIVE_NS:
        for t in tasks:
            subsample = t["locatable_sample"][:n_eff]
            feat_vals = compute_per_element_features(subsample)["tag_entropy"]
            for dn, defn in DEFINITIONS.items():
                contrib = defaultdict(float)
                for i, elem in enumerate(subsample):
                    mapped = apply_role_map(elem["role"], defn["role_map"])
                    if mapped in defn["interactive_roles"]:
                        contrib[mapped] += feat_vals[i]
                role_contrib[(t["task_id"], n_eff, dn)] = dict(contrib)

    listing_tasks = [t["task_id"] for t in tasks if t["page_type"] == "product_listing"]
    detail_tasks = [t["task_id"] for t in tasks if t["page_type"] == "detail"]

    task_ids = [t["task_id"] for t in tasks]
    task_ewb = {t["task_id"]: t["elements_with_bbox"] for t in tasks}

    per_iter_storage = {}   # raw: {n: {def: {recipe: [per-iteration dicts]}}}
    hybrid_storage = {}     # raw: {n: {def: {recipe: [d_task lists]}}} (for Phase F)

    for n_eff in EFFECTIVE_NS:
        per_iter_storage[n_eff] = {}
        hybrid_storage[n_eff] = {}
        for dn in DEFINITIONS:
            per_iter_storage[n_eff][dn] = {"canonical": [], "pertask": []}
            hybrid_storage[n_eff][dn] = {"canonical": [], "pertask": []}

        for dn, defn in DEFINITIONS.items():
            role_lists = {tid: role_contrib[(tid, n_eff, dn)] for tid in task_ids}

            for seed in range(RECIPE_SEEDS):
                for it in range(RECIPE_ITERS):
                    # ---------------- canonical (shared subset) ----------------
                    random.seed(seed * RECIPE_ITERS + it)
                    active_roles = {r for r in defn["interactive_roles"] if random.random() < 0.5}
                    d_canon = {}
                    for tid in task_ids:
                        contrib = role_lists[tid]
                        total = sum(v for r, v in contrib.items() if r in active_roles)
                        d_canon[tid] = total / task_ewb[tid]

                    # ---------------- per-task (independent subsets) -----------
                    d_pt = {}
                    for tid in task_ids:
                        random.seed(seed * RECIPE_ITERS + it + hash(tid) % 100000)
                        active_pt = {r for r in defn["interactive_roles"] if random.random() < 0.5}
                        contrib = role_lists[tid]
                        total = sum(v for r, v in contrib.items() if r in active_pt)
                        d_pt[tid] = total / task_ewb[tid]

                    d_by_recipe = {"canonical": d_canon, "pertask": d_pt}
                    for recipe, d in d_by_recipe.items():
                        listing = [d[tid] for tid in listing_tasks]
                        detail = [d[tid] for tid in detail_tasks]
                        mu_l = sum(listing) / len(listing)
                        mu_d = sum(detail) / len(detail)
                        margin = mu_l - mu_d
                        se_l = (statistics.stdev(listing) / math.sqrt(len(listing))
                                if len(listing) > 1 else 0.0)
                        se_d = (statistics.stdev(detail) / math.sqrt(len(detail))
                                if len(detail) > 1 else 0.0)
                        se_tot = math.sqrt(se_l ** 2 + se_d ** 2)
                        snr = margin / se_tot if se_tot > 0 else (math.inf if margin > 0 else -math.inf)
                        # eta2 over all 3 page types (matches parent grouping)
                        g = defaultdict(list)
                        for t in tasks:
                            g[t["page_type"]].append(d[t["task_id"]])
                        gmeans = {k: sum(v) / len(v) for k, v in g.items() if v}
                        agree = check_ranking(direct_rankings, gmeans, "tag_entropy")
                        eta = _eta2(g)
                        # JSON-safe SNR serialization (snr can be +/-inf when se_tot==0)
                        snr_out = snr
                        snr_flag = None
                        if isinstance(snr, float) and not math.isfinite(snr):
                            snr_out = None
                            snr_flag = "+inf" if snr == math.inf else ("-inf" if snr == -math.inf else "nan")
                        per_iter_storage[n_eff][dn][recipe].append({
                            "seed": seed, "it": it,
                            "margin": margin, "se_l": se_l, "se_d": se_d,
                            "snr": snr_out, "snr_flag": snr_flag,
                            "agree": 1 if agree else 0, "eta2": eta,
                            "d": {tid: d[tid] for tid in task_ids},
                        })
                        if n_eff == 20 and dn == "DEF-FULL-MAP":
                            hybrid_storage[n_eff][dn][recipe].append(
                                [d[tid] for tid in task_ids])

    # ---- Phase B aggregation: per-n summary (canonical & per-task) -----------
    for n_eff in EFFECTIVE_NS:
        n_res = {}
        for dn in DEFINITIONS:
            key = f"tag_entropy x {dn}"
            n_res[key] = {}
            for recipe in ("canonical", "pertask"):
                recs = per_iter_storage[n_eff][dn][recipe]
                margins = [r["margin"] for r in recs]
                snrs = [r["snr"] for r in recs]
                se_ls = [r["se_l"] for r in recs]
                se_ds = [r["se_d"] for r in recs]
                etas = [r["eta2"] for r in recs]
                agrees = [r["agree"] for r in recs]
                se_tots = [math.sqrt(a * a + b * b) for a, b in zip(se_ls, se_ds)]
                # within-type CV of per-task density (across iterations,
                # computed from the 3 d values per type per iteration)
                cv_l_iters, cv_d_iters = [], []
                for r in recs:
                    dl = [r["d"][tid] for tid in listing_tasks]
                    dd = [r["d"][tid] for tid in detail_tasks]
                    ml = sum(dl) / len(dl)
                    md = sum(dd) / len(dd)
                    if ml != 0:
                        cv_l_iters.append(statistics.stdev(dl) / ml if len(dl) > 1 else 0.0)
                    if md != 0:
                        cv_d_iters.append(statistics.stdev(dd) / md if len(dd) > 1 else 0.0)
                n_res[key][recipe] = {
                    "ranking_agreement": sum(agrees) / len(agrees),
                    "eta2_mean": statistics.fmean(etas),
                    "eta2_std": statistics.stdev(etas) if len(etas) > 1 else 0.0,
                    "margin_mean": statistics.fmean(margins),
                    "margin_std": statistics.stdev(margins) if len(margins) > 1 else 0.0,
                    "se_l_mean": statistics.fmean(se_ls),
                    "se_d_mean": statistics.fmean(se_ds),
                    "se_tot_mean": statistics.fmean(se_tots),
                    "snr_mean": finite_mean(snrs),
                    "phi_mean_snr": phi(finite_mean(snrs)),
                    "cv_listing_mean": statistics.fmean(cv_l_iters) if cv_l_iters else None,
                    "cv_detail_mean": statistics.fmean(cv_d_iters) if cv_d_iters else None,
                }
                # rho of density across tasks of same type (canonical & per-task)
                def _rho(recs_, type_tasks):
                    xs_by_task = {tid: [r["d"][tid] for r in recs_] for tid in type_tasks}
                    ids = list(xs_by_task.keys())
                    rhos = []
                    for a in range(len(ids)):
                        for b in range(a + 1, len(ids)):
                            x, y = xs_by_task[ids[a]], xs_by_task[ids[b]]
                            n = len(x)
                            mx = sum(x) / n
                            my = sum(y) / n
                            num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
                            dx = math.sqrt(sum((x[i] - mx) ** 2 for i in range(n)))
                            dy = math.sqrt(sum((y[i] - my) ** 2 for i in range(n)))
                            rhos.append(num / (dx * dy) if dx > 0 and dy > 0 else 0.0)
                    return statistics.fmean(rhos) if rhos else None
                n_res[key][recipe]["rho_listing"] = _rho(recs, listing_tasks)
                n_res[key][recipe]["rho_detail"] = _rho(recs, detail_tasks)
        result["per_n"][str(n_eff)] = n_res

    # ===================== Phase C: SNR model validation =====================
    def cmod(n_eff):
        return result["per_n"][str(n_eff)]["tag_entropy x DEF-FULL-MAP"]["canonical"]

    pred15 = cmod(15)["phi_mean_snr"]
    pred20 = cmod(20)["phi_mean_snr"]
    obs15 = FROZEN_OBSERVED[15]
    obs20 = FROZEN_OBSERVED[20]
    result["snr_model"] = {
        "model": "agreement ~ Phi(mean(SNR_i)), SNR_i = M_i / sqrt(SE_l_i^2 + SE_d_i^2)",
        "predicted_agreement_n15": pred15,
        "predicted_agreement_n20": pred20,
        "observed_agreement_n15_frozen_target": obs15,
        "observed_agreement_n20_frozen_target": obs20,
        "observed_agreement_n15_this_run": cmod(15)["ranking_agreement"],
        "observed_agreement_n20_this_run": cmod(20)["ranking_agreement"],
        "residual_n15": None if pred15 is None else abs(pred15 - obs15),
        "residual_n20": None if pred20 is None else abs(pred20 - obs20),
        "C1_pass": (pred15 is not None and pred20 is not None
                    and abs(pred15 - obs15) <= 0.10 and abs(pred20 - obs20) <= 0.10),
    }

    # ===================== Null control NC1: random noise ====================
    random.seed(12345)
    null_agrees = []
    for _ in range(NULL_SIMS):
        listing = [random.gauss(0, 1) for _ in range(3)]
        detail = [random.gauss(0, 1) for _ in range(3)]
        null_agrees.append(1 if sum(listing) / 3 > sum(detail) / 3 else 0)
    null_agree = sum(null_agrees) / len(null_agrees)
    result["null_control"] = {
        "model": "3 listing + 3 detail densities ~ N(0,1); agreement = P(mean_l > mean_d)",
        "n_simulations": NULL_SIMS,
        "predicted_agreement": null_agree,
        "expected": "50% +/- 5%",
        "pass": abs(null_agree - 0.5) <= 0.05,
        "snr_error_minus_null_error_n15": (None if pred15 is None else
                                           abs(pred15 - obs15) - abs(null_agree - obs15)),
        "snr_error_minus_null_error_n20": (None if pred20 is None else
                                           abs(pred20 - obs20) - abs(null_agree - obs20)),
    }

    # ===================== Phase D: extrapolation (power laws) ===============
    ns = EFFECTIVE_NS
    margins = [cmod(n)["margin_mean"] for n in ns]
    se_tots = [cmod(n)["se_tot_mean"] for n in ns]

    extrap = {"ns": ns, "margins": margins, "se_tots": se_tots,
              "fit_note": "margin(n)=a*n^b and SE(n)=c*n^d power laws on the 4 points"}

    # Margin crosses zero if sign(v) changes across n (n=5/10 observed 0% agreement
    # => negative margins). Power law needs positive magnitudes: fit |margin| and
    # re-apply the sign observed at n=20.
    signs = [1.0 if m >= 0 else -1.0 for m in margins]
    extrap["margin_sign_by_n"] = signs
    extrap["margin_sign_crosses_zero"] = len(set(signs)) > 1
    sign_extrap = signs[-1]

    def fit_powerlaw(xs, ys):
        lx = [math.log(x) for x in xs]
        ly = [math.log(y) for y in ys]
        n = len(lx)
        mx = sum(lx) / n
        my = sum(ly) / n
        num = sum((lx[i] - mx) * (ly[i] - my) for i in range(n))
        den = sum((lx[i] - mx) ** 2 for i in range(n))
        b = num / den if den else 0.0
        a = math.exp(my - b * mx)
        return a, b

    mags = [abs(m) for m in margins]
    a_m, b_m = fit_powerlaw(ns, mags)
    a_s, b_s = fit_powerlaw(ns, se_tots)
    extrap["margin_fit"] = {"a": a_m, "b": b_m, "on": "|margin|"}
    extrap["se_fit"] = {"a": a_s, "b": b_s}

    def predict_snr(n_target):
        return sign_extrap * a_m * (n_target ** b_m) / (a_s * (n_target ** b_s))

    def bootstrap_pi(n_target, n_boot=2000, seed_val=999):
        rng = random.Random(seed_val)
        lx = [math.log(x) for x in ns]
        ly_m = [math.log(y) for y in mags]
        ly_s = [math.log(y) for y in se_tots]
        resid_m = [ly_m[i] - (math.log(a_m) + b_m * lx[i]) for i in range(4)]
        resid_s = [ly_s[i] - (math.log(a_s) + b_s * lx[i]) for i in range(4)]
        snr_sims = []
        for _ in range(n_boot):
            rm = [rng.choice(resid_m) for _ in range(4)]
            rs = [rng.choice(resid_s) for _ in range(4)]
            ym = [math.log(a_m) + b_m * lx[i] + rm[i] for i in range(4)]
            ys_ = [math.log(a_s) + b_s * lx[i] + rs[i] for i in range(4)]
            aa_m, bb_m = fit_powerlaw(ns, [math.exp(v) for v in ym])
            aa_s, bb_s = fit_powerlaw(ns, [math.exp(v) for v in ys_])
            snr_sims.append(sign_extrap * aa_m * (n_target ** bb_m) / (aa_s * (n_target ** bb_s)))
        agrees = sorted(phi(s) for s in snr_sims)
        return {"lo90": agrees[int(0.05 * len(agrees))], "hi90": agrees[int(0.95 * len(agrees))],
                "n_boot": n_boot, "seed": seed_val}

    for n_target in (50, 82):
        snr_pred = predict_snr(n_target)
        extrap[str(n_target)] = {
            "predicted_snr": snr_pred,
            "predicted_agreement": phi(snr_pred),
            "predicted_agreement_pi90": bootstrap_pi(n_target),
            "margin_hat": a_m * (n_target ** b_m),
            "se_hat": a_s * (n_target ** b_s),
        }
    extrap["C3_falsifies_full_dom"] = (
        extrap["50"]["predicted_agreement"] is not None
        and extrap["50"]["predicted_agreement"] < 0.80)
    result["extrapolation"] = extrap

    # ===================== Phase E: mechanism identification =================
    c20 = cmod(20)
    margin_se_ratio = (c20["margin_mean"] / c20["se_tot_mean"]
                       if c20["se_tot_mean"] else None)
    cv_max = max([c20["cv_listing_mean"], c20["cv_detail_mean"]])
    rho_max = max([c20["rho_listing"], c20["rho_detail"]])
    mechanisms = {
        "margin_deficit": (margin_se_ratio is not None and margin_se_ratio < 3.0),
        "task_variance": cv_max is not None and cv_max > 0.1,
        "correlated_noise": rho_max is not None and rho_max > 0.3,
    }
    result["mechanism"] = {
        "margin_se_ratio_n20": margin_se_ratio,
        "cv_listing_n20": c20["cv_listing_mean"],
        "cv_detail_n20": c20["cv_detail_mean"],
        "rho_listing_n20": c20["rho_listing"],
        "rho_detail_n20": c20["rho_detail"],
        "classification": mechanisms,
        "C2_pass": any(mechanisms.values()),
    }

    # ===================== Phase F: hybrid recipe (exploratory) ==============
    hybrid = {"alpha": ALPHAS, "eta2": {}, "agreement": {}}
    canon_n20 = hybrid_storage[20]["DEF-FULL-MAP"]["canonical"]
    pt_n20 = hybrid_storage[20]["DEF-FULL-MAP"]["pertask"]
    for alpha in ALPHAS:
        etas, agrees = [], []
        for i in range(len(canon_n20)):
            d_hyb = {}
            for j, tid in enumerate(task_ids):
                d_hyb[tid] = alpha * canon_n20[i][j] + (1 - alpha) * pt_n20[i][j]
            g = defaultdict(list)
            for t in tasks:
                g[t["page_type"]].append(d_hyb[t["task_id"]])
            gmeans = {k: sum(v) / len(v) for k, v in g.items() if v}
            agrees.append(1 if check_ranking(direct_rankings, gmeans, "tag_entropy") else 0)
            etas.append(_eta2(g))
        hybrid["eta2"][str(alpha)] = statistics.fmean(etas)
        hybrid["agreement"][str(alpha)] = statistics.fmean(agrees)
    hybrid["sweet_spot_exists"] = any(
        hybrid["eta2"][str(a)] >= 0.80 and hybrid["agreement"][str(a)] >= 0.80 for a in ALPHAS)
    result["hybrid_exploratory"] = hybrid

    # ===================== Baseline reproduction (B1-B6) =====================
    b = {}
    for n_eff in EFFECTIVE_NS:
        c = result["per_n"][str(n_eff)]["tag_entropy x DEF-FULL-MAP"]["canonical"]
        p = result["per_n"][str(n_eff)]["tag_entropy x DEF-FULL-MAP"]["pertask"]
        b[f"canonical_agreement_n{n_eff}"] = c["ranking_agreement"]
        b[f"canonical_eta2_n{n_eff}"] = c["eta2_mean"]
        b[f"pertask_agreement_n{n_eff}"] = p["ranking_agreement"]
        b[f"pertask_eta2_n{n_eff}"] = p["eta2_mean"]
    result["baseline_reproduction"] = b

    # ===================== Decision rules (frozen) ===========================
    c1 = result["snr_model"]["C1_pass"]
    c2 = result["mechanism"]["C2_pass"]
    c3 = result["extrapolation"]["C3_falsifies_full_dom"]
    if not c1:
        verdict = "MEASUREMENT_INVALID"
        reason = ("C1 FAIL: SNR model predicts Phi(mean(SNR)) at n=15/n=20 "
                  "(respectively " + str(pred15) + "/" + str(pred20) + ") outside "
                  "10pp of observed 0.4998/0.5595; decomposition unreliable per frozen rule.")
    elif not c2:
        verdict = "MIXED"
        reason = "C1 PASS, C2 FAIL: model valid but mechanism unclear."
    elif c3:
        verdict = "FALSIFIES-FULL-DOM"
        reason = ("C1 PASS, C2 PASS, C3 PASS: extrapolated agreement at n=50 = "
                  + str(extrap["50"]["predicted_agreement"]) + " < 80%.")
    else:
        verdict = "SUPPORTS-FULL-DOM"
        reason = ("C1 PASS, C2 PASS, C3 FAIL: extrapolated agreement at n=50 = "
                  + str(extrap["50"]["predicted_agreement"]) + " >= 80%.")
    result["decision"] = {
        "C1_SNR_MODEL_VALID": c1,
        "C2_MECHANISM_IDENTIFIED": c2,
        "C3_EXTRAPOLATION_FALSIFIES_FULL_DOM": c3,
        "verdict": verdict,
        "reason": reason,
    }

    # -------------------- write artifacts ------------------------------------
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "analysis_output_snr.json"), "w") as f:
        json.dump(result, f, indent=2, allow_nan=False)
    with gzip.open(os.path.join(OUT_DIR, "snr_per_iteration_tag_entropy.json.gz"), "wt") as f:
        json.dump({"experiment_id": result["experiment_id"],
                   "per_iteration": {str(k): v for k, v in per_iter_storage.items()}},
                  f, indent=1, allow_nan=False)
    with gzip.open(os.path.join(OUT_DIR, "hybrid_per_iteration_densities_n20.json.gz"), "wt") as f:
        json.dump({"experiment_id": result["experiment_id"],
                   "tasks": task_ids,
                   "hybrid_storage_n20": hybrid_storage[20]}, f, indent=1, allow_nan=False)

    print(json.dumps(result["decision"], indent=2))
    print(json.dumps(result["snr_model"], indent=2))
    print(json.dumps(result["mechanism"], indent=2))
    print(json.dumps(result["extrapolation"], indent=2, default=str))
    print(json.dumps(result["null_control"], indent=2))
    print(json.dumps(result["hybrid_exploratory"], indent=2))
    print("BASELINES:", json.dumps(result["baseline_reproduction"], indent=2))

def sys_version():
    import sys as _sys
    return _sys.version.split()[0]

if __name__ == "__main__":
    main()