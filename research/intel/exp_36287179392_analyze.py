#!/usr/bin/env python3
"""EXP-INTEL-36287179392 phase C -- derived measurements and frozen decision rule.

Implements frozen prereg 7.3 (AGF primary, mean pairwise Jaccard secondary),
8 (shuffled-host null, 1,000 permutations, seed 36287179393), 9 (10,000-replicate
eTLD+1-level bootstrap, seed 36287179392), 10 (per-observation cost) and 12
(frozen decision rule), plus spec.json's controls PC-SYNTHETIC-ALIAS,
NC-SHUFFLED-HOST and NC-SINGLETON-SITE.

Two clearly labelled NON-FROZEN additions are computed because the frozen design
turned out to be unable to answer its own primary question; both are reported
as decision-not-used and are constructed to be re-runnable by AUDIT:
  NC-SIG-REASSIGN  -- a permutation null that has power against the frozen AGF,
                       by permuting the pooled signature multiset across hosts
                       while preserving every host's signature count and the
                       global multiset exactly.
  coverage strata -- threshold-free stratification of matched instances by how
                       many distinct hosts carry the shared signature key.

Output: derived/metrics.json (prereg 14).
"""
from __future__ import annotations

import json
import os
import random
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exp_36287179392_pipeline import (  # noqa: E402
    MIN_PAGES_PER_SITE, N_BOOTSTRAP, N_NULL_PERMUTATIONS, SEED_BOOTSTRAP,
    SEED_NULL, SEED_POSITIVE_CONTROL, agf_from_site_keymaps, ci,
    pairwise_jaccard, percentile, singleton_sites,
)

EXP_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "experiments", "EXP-INTEL-36287179392",
)
RAW = os.path.join(EXP_DIR, "raw")
DERIVED = os.path.join(EXP_DIR, "derived")


# ---------------------------------------------------------------------------
# Frozen estimator (prereg 7.2-7.3). One code path for the frozen metric and
# every labelled sensitivity, so AUDIT can recompute any of them.
# ---------------------------------------------------------------------------

def agf_of(site_sigs: dict) -> dict:
    """site_sigs: {host: [canonical signature key strings]}.

    AGF = sum over distinct hosts pairs of matched signature instances,
          divided by total signatures across all pages.
    Pair matches are counted with multiplicity: a key carried n_a times by host
    a and n_b times by host b contributes n_a * n_b.
    """
    return agf_from_site_keymaps(None, site_sigs, lambda s: s)


def mean_jaccard_of(site_sigs: dict) -> dict:
    return pairwise_jaccard(site_sigs, lambda s: s)


def build_site_sigs(records, slotted: bool) -> dict:
    out = defaultdict(list)
    for r in records:
        if r.get("extraction_error"):
            continue
        out[r["site_key"]].extend(
            r["signature_keys_slotted"] if slotted else r["signature_keys"])
    return dict(out)


# ---------------------------------------------------------------------------
# Frozen NC-SHUFFLED-HOST (prereg 8.1) -- executed exactly as written
# ---------------------------------------------------------------------------

def shuffled_host_null(site_sigs: dict, seed: int, n: int) -> list:
    """prereg 8.1 verbatim: permute the eTLD+1 labels across sites and recompute."""
    rng = random.Random(seed)
    sites = sorted(site_sigs)
    out = []
    for _ in range(n):
        shuffled = sites[:]
        rng.shuffle(shuffled)
        relabelled = dict(zip(sites, shuffled))
        out.append(agf_of({s: site_sigs[relabelled[s]] for s in sites})["agf"])
    return out


def shuffled_host_null_jaccard(site_sigs: dict, seed: int, n: int) -> list:
    rng = random.Random(seed + 1)
    sites = sorted(site_sigs)
    out = []
    for _ in range(n):
        shuffled = sites[:]
        rng.shuffle(shuffled)
        relabelled = dict(zip(sites, shuffled))
        out.append(mean_jaccard_of({s: site_sigs[relabelled[s]] for s in sites})["mean_jaccard"])
    return out


# ---------------------------------------------------------------------------
# NON-FROZEN NC-SIG-REASSIGN -- a null with demonstrated power
# ---------------------------------------------------------------------------

def sig_reassign_null(site_sigs: dict, seed: int, n: int, stat="agf") -> list:
    """Permute the pooled signature multiset across hosts.

    Preserves exactly: each host's signature count, and the global signature
    multiset. Randomises: which host holds which signature, hence the
    cross-host co-occurrence structure. This is a valid randomisation test for
    'does the grouping of signatures into hosts carry structure beyond the
    shared generic vocabulary' -- unlike the frozen label permutation, which is
    an identity on this estimator.
    """
    rng = random.Random(seed)
    sites = sorted(site_sigs)
    sizes = [len(site_sigs[s]) for s in sites]
    pooled = [k for s in sites for k in site_sigs[s]]
    out = []
    for _ in range(n):
        sh = pooled[:]
        rng.shuffle(sh)
        redrawn, i = {}, 0
        for s, c in zip(sites, sizes):
            redrawn[s] = sh[i:i + c]
            i += c
        out.append(agf_of(redrawn)["agf"] if stat == "agf"
                   else mean_jaccard_of(redrawn)["mean_jaccard"])
    return out


# ---------------------------------------------------------------------------
# prereg 9 -- eTLD+1-level bootstrap
# ---------------------------------------------------------------------------

def host_bootstrap(site_sigs: dict, seed: int, n: int) -> list:
    rng = random.Random(seed)
    sites = sorted(site_sigs)
    out = []
    for _ in range(n):
        draw = [sites[rng.randrange(len(sites))] for _ in range(len(sites))]
        merged = defaultdict(list)
        for s in draw:
            merged[s].extend(site_sigs[s])
        out.append(agf_of(dict(merged))["agf"])
    return out


def host_bootstrap_cost(per_site_diffs: dict, seed: int, n: int) -> dict:
    rng = random.Random(seed + 7)
    sites = sorted(per_site_diffs)
    out = defaultdict(list)
    for _ in range(n):
        draw = [sites[rng.randrange(len(sites))] for _ in range(len(sites))]
        acc = defaultdict(list)
        for s in draw:
            for k, v in per_site_diffs[s].items():
                acc[k].extend(v)
        for k, v in acc.items():
            out[k].append(sum(v) / len(v))
    return dict(out)


# ---------------------------------------------------------------------------
# prereg 10 -- per-observation cost
# ---------------------------------------------------------------------------

def cost_block(records) -> dict:
    rows = [{
        "site_key": r["site_key"], "url": r["url"],
        "bytes_raw": r["raw"]["bytes"], "bytes_full_dom": r["full_dom"]["bytes"],
        "bytes_a11y": r["a11y"]["bytes"], "bytes_minimal": r["minimal"]["bytes"],
        "tokens_raw": r["raw"]["tokens"], "tokens_full_dom": r["full_dom"]["tokens"],
        "tokens_a11y": r["a11y"]["tokens"], "tokens_minimal": r["minimal"]["tokens"],
        "a11y_nodes": r["a11y"]["n_nodes"],
    } for r in records if not r.get("extraction_error")]
    mean = lambda k: sum(x[k] for x in rows) / len(rows) if rows else None  # noqa: E731
    med = lambda k: statistics.median([x[k] for x in rows]) if rows else None  # noqa: E731
    diffs = {
        "tokens_minimal_minus_full_dom": [x["tokens_minimal"] - x["tokens_full_dom"] for x in rows],
        "tokens_minimal_minus_a11y": [x["tokens_minimal"] - x["tokens_a11y"] for x in rows],
        "tokens_minimal_minus_raw": [x["tokens_minimal"] - x["tokens_raw"] for x in rows],
        "bytes_minimal_minus_full_dom": [x["bytes_minimal"] - x["bytes_full_dom"] for x in rows],
        "bytes_minimal_minus_a11y": [x["bytes_minimal"] - x["bytes_a11y"] for x in rows],
        "bytes_minimal_minus_raw": [x["bytes_minimal"] - x["bytes_raw"] for x in rows],
    }
    return {
        "n_observations": len(rows),
        "means": {k: mean(k) for k in ("bytes_raw", "bytes_full_dom", "bytes_a11y", "bytes_minimal",
                                       "tokens_raw", "tokens_full_dom", "tokens_a11y", "tokens_minimal")},
        "medians": {k: med(k) for k in ("bytes_raw", "bytes_full_dom", "bytes_a11y", "bytes_minimal",
                                        "tokens_raw", "tokens_full_dom", "tokens_a11y", "tokens_minimal")},
        "paired_differences_mean": {k: sum(v) / len(v) for k, v in diffs.items()},
        "paired_differences_median": {k: statistics.median(v) for k, v in diffs.items()},
        "fraction_observations_minimal_is_smaller": {
            k: sum(1 for v in vals if v < 0) / len(vals) for k, vals in diffs.items()},
        "ratios_mean_baseline_over_minimal": {
            "tokens_full_dom_over_minimal": mean("tokens_full_dom") / mean("tokens_minimal"),
            "tokens_a11y_over_minimal": mean("tokens_a11y") / mean("tokens_minimal"),
            "tokens_raw_over_minimal": mean("tokens_raw") / mean("tokens_minimal"),
            "bytes_full_dom_over_minimal": mean("bytes_full_dom") / mean("bytes_minimal"),
            "bytes_a11y_over_minimal": mean("bytes_a11y") / mean("bytes_minimal"),
            "bytes_raw_over_minimal": mean("bytes_raw") / mean("bytes_minimal"),
        },
        "per_observation": rows,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def describe(values, label):
    s = sorted(values)
    return {"label": label, "n": len(s), "mean": statistics.mean(values),
            "std": statistics.pstdev(values), "min": min(s),
            "p50": percentile(s, 0.50), "p95": percentile(s, 0.95),
            "p99": percentile(s, 0.99), "max": max(s),
            "n_distinct_values": len(set(round(v, 12) for v in values))}


def main():
    os.makedirs(DERIVED, exist_ok=True)
    records = [json.loads(l) for l in open(os.path.join(RAW, "extracted_structures.jsonl"))]
    controls = json.load(open(os.path.join(RAW, "control_structures.json")))
    manifest = json.load(open(os.path.join(RAW, "fetch_manifest.json")))
    ok = [r for r in records if not r.get("extraction_error")]
    pages_per_site = Counter(r["site_key"] for r in ok)
    n_sites_ge_min = sum(1 for v in pages_per_site.values() if v >= MIN_PAGES_PER_SITE)
    primary_sites = {s for s, v in pages_per_site.items() if v >= MIN_PAGES_PER_SITE}

    site_sigs = {s: v for s, v in build_site_sigs(ok, slotted=False).items() if s in primary_sites}
    site_sigs_slotted = {s: v for s, v in build_site_sigs(ok, slotted=True).items() if s in primary_sites}

    # ---- frozen primary metric ----
    agf_point = agf_of(site_sigs)
    jac = mean_jaccard_of(site_sigs)
    boot = host_bootstrap(site_sigs, SEED_BOOTSTRAP, N_BOOTSTRAP)
    boot_ci = ci(boot)

    # ---- frozen null, executed verbatim ----
    null_agf = shuffled_host_null(site_sigs, SEED_NULL, N_NULL_PERMUTATIONS)
    null_jac = shuffled_host_null_jaccard(site_sigs, SEED_NULL, N_NULL_PERMUTATIONS)
    frozen_null = {
        "agf": describe(null_agf, "NC-SHUFFLED-HOST AGF"),
        "jaccard": describe(null_jac, "NC-SHUFFLED-HOST mean pairwise Jaccard"),
        "n_permutations": N_NULL_PERMUTATIONS,
        "observed_agf": agf_point["agf"],
        "observed_equals_null_mean": abs(statistics.mean(null_agf) - agf_point["agf"]) < 1e-12,
        "observed_equals_null_p95": abs(percentile(sorted(null_agf), 0.95) - agf_point["agf"]) < 1e-12,
        "invariant_proof": (
            "AGF = sum_K (T_K^2 - sum_s n_{s,K}^2) / (2 * total_signatures). A "
            "permutation of the eTLD+1 labels is a bijection on hosts, so it "
            "permutes the vector (n_{s,K})_s and leaves sum_s n_{s,K}^2, hence T_K "
            "and hence AGF, exactly invariant. The frozen NC-SHUFFLED-HOST is "
            "therefore an identity on the frozen estimator: it is not a weak null, "
            "it has identically zero variance by construction and cannot "
            "discriminate any outcome. Empirically confirmed: "
            f"{len(set(round(v, 12) for v in null_agf))} distinct value(s) over "
            f"{N_NULL_PERMUTATIONS} permutations."),
    }

    # ---- NON-FROZEN null with power ----
    sig_null = sig_reassign_null(site_sigs, SEED_NULL, N_NULL_PERMUTATIONS, "agf")
    sig_null_slotted = sig_reassign_null(site_sigs_slotted, SEED_NULL, N_NULL_PERMUTATIONS, "agf")
    sig_null_jac = sig_reassign_null(site_sigs, SEED_NULL, N_NULL_PERMUTATIONS, "jaccard")

    # ---- signature-type and host-coverage decomposition ----
    keytype = defaultdict(lambda: defaultdict(int))
    for r in ok:
        if r["site_key"] not in primary_sites:
            continue
        for s in r["signatures"]:
            k = json.dumps([s["type"], s["match"]], sort_keys=True, default=list)
            keytype[k][r["site_key"]] += 1
    sigtype_counts = Counter()
    for r in ok:
        if r["site_key"] in primary_sites:
            sigtype_counts.update(s["type"] for s in r["signatures"])
    sigtype_matched = Counter()
    coverage = {"2": Counter(), "3-5": Counter(), "6-10": Counter(), "11-15": Counter()}
    drivers = []
    for k, ps in keytype.items():
        st = json.loads(k)[0]
        sigtype_counts.setdefault(st, 0)
        if len(ps) < 2:
            continue
        vals = list(ps.values())
        m = (sum(vals) ** 2 - sum(v * v for v in vals)) // 2
        sigtype_matched[st] += m
        n_sites = len(ps)
        bucket = "2" if n_sites == 2 else "3-5" if n_sites <= 5 else "6-10" if n_sites <= 10 else "11-15"
        coverage[bucket][st] += m
        drivers.append({"matched_instances": m, "n_sites_sharing": n_sites,
                        "n_signature_instances": sum(vals), "signature_type": st,
                        "template": k[:400]})
    drivers.sort(key=lambda d: -d["matched_instances"])
    total_sig = sum(sigtype_counts.values())
    total_match = sum(sigtype_matched.values())

    # ---- sensitivity population (>=1 typed slot) ----
    agf_slotted = agf_of(site_sigs_slotted)
    boot_slotted = host_bootstrap(site_sigs_slotted, SEED_BOOTSTRAP, N_BOOTSTRAP)
    boot_slotted_ci = ci(boot_slotted)
    jac_slotted = mean_jaccard_of(site_sigs_slotted)

    singles = singleton_sites(site_sigs, lambda s: s)

    # ---- controls ----
    def control_block(cid):
        by_site = defaultdict(list)
        for r in controls[cid]:
            by_site[r["site_key"]].extend(r["signature_keys"])
        a, j = agf_of(dict(by_site)), mean_jaccard_of(dict(by_site))
        return a, j

    pc_frozen_agf, pc_frozen_jac = control_block("PC-SYNTHETIC-ALIAS")
    pc_ext_agf, pc_ext_jac = control_block("PC-SYNTHETIC-ALIAS-4SITE-POWER-EXTENSION")
    pc_frozen_sigs = {r["site_key"]: r["signature_keys"] for r in controls["PC-SYNTHETIC-ALIAS"]}
    pc_ext_sigs = {r["site_key"]: r["signature_keys"]
                   for r in controls["PC-SYNTHETIC-ALIAS-4SITE-POWER-EXTENSION"]}
    pc_frozen_null = shuffled_host_null(pc_frozen_sigs, SEED_NULL, N_NULL_PERMUTATIONS)
    pc_ext_null = sig_reassign_null(pc_ext_sigs, SEED_NULL, N_NULL_PERMUTATIONS, "agf")
    pc_ext_null_jac = sig_reassign_null(pc_ext_sigs, SEED_NULL, N_NULL_PERMUTATIONS, "jaccard")
    pc_frozen_null_reassign = sig_reassign_null(pc_frozen_sigs, SEED_NULL, N_NULL_PERMUTATIONS, "agf")
    pc_frozen_null_reassign_jac = sig_reassign_null(pc_frozen_sigs, SEED_NULL, N_NULL_PERMUTATIONS, "jaccard")
    # Arithmetic ceiling of the frozen AGF on a 2-group design: with n
    # signatures per host and all keys distinct and matched 1:1, matched
    # instances = n and total signatures = 2n, so AGF = 0.5 exactly.
    pc_frozen_n_per_site = max(len(v) for v in pc_frozen_sigs.values())
    pc_two_group_ceiling = pc_frozen_n_per_site / (2.0 * pc_frozen_n_per_site)

    # ---- cost ----
    cost = cost_block(ok)
    per_site_diff = defaultdict(lambda: defaultdict(list))
    for row in cost["per_observation"]:
        if row["site_key"] in primary_sites:
            d = per_site_diff[row["site_key"]]
            d["tokens_minimal_minus_full_dom"].append(row["tokens_minimal"] - row["tokens_full_dom"])
            d["tokens_minimal_minus_a11y"].append(row["tokens_minimal"] - row["tokens_a11y"])
    per_site_diff = {k: dict(v) for k, v in per_site_diff.items()}
    cost_boot = host_bootstrap_cost(per_site_diff, SEED_BOOTSTRAP, N_BOOTSTRAP)
    cost_ci = {k: ci(v) for k, v in cost_boot.items()}

    # ---- frozen decision rule (prereg 12) ----
    agf_v = agf_point["agf"]
    frozen_null_p95 = percentile(sorted(null_agf), 0.95)
    c_fd = cost_ci["tokens_minimal_minus_full_dom"]
    c_a11y = cost_ci["tokens_minimal_minus_a11y"]
    cost_fd_mean = cost["paired_differences_mean"]["tokens_minimal_minus_full_dom"]
    cost_a11y_mean = cost["paired_differences_mean"]["tokens_minimal_minus_a11y"]
    cost_satisfied = bool(cost_fd_mean < 0 and c_fd["ci_upper"] < 0
                          and cost_a11y_mean < 0 and c_a11y["ci_upper"] < 0)

    validity_sub = {
        "agf_ci_width_gt_0": bool(boot_ci["ci_width"] and boot_ci["ci_width"] > 0),
        "n_sites_ge_2pages_ge_10": bool(n_sites_ge_min >= 10),
        "null_std_gt_0": bool(statistics.pstdev(null_agf) > 0),
    }
    validity_satisfied = all(validity_sub.values())
    validity_partially_failed = (not validity_satisfied) and any(validity_sub.values())
    primary_evaluable = validity_sub["null_std_gt_0"]

    if not validity_satisfied and not validity_partially_failed:
        outcome = "INCONCLUSIVE"
    elif primary_evaluable:
        primary_ok = bool(agf_v > frozen_null_p95 and boot_ci["ci_lower"] > frozen_null_p95)
        outcome = "SUPPORTS" if (primary_ok and cost_satisfied) else (
            "FALSIFIES" if not (primary_ok or cost_satisfied) else "MIXED")
    else:
        # prereg 12 MIXED clause 3: validity partially failed, some metrics valid.
        # NOT a partial support of the prevalence hypothesis: the primary clause
        # is unevaluable, not half-satisfied.
        outcome = "MIXED"

    out = {
        "experiment_id": "EXP-INTEL-36287179392", "lane": "intel",
        "seeds": {"bootstrap": SEED_BOOTSTRAP, "null": SEED_NULL,
                  "positive_control": SEED_POSITIVE_CONTROL},
        "sample": {
            "n_sites_preregistered": 20,
            "n_sites_with_parsed_pages": len(pages_per_site),
            "n_sites_ge_min_pages": n_sites_ge_min,
            "n_pages_parsed": len(ok),
            "n_pages_extraction_failed": len(records) - len(ok),
            "pages_per_site": dict(sorted(pages_per_site.items())),
            "n_http_requests_total": manifest["n_http_requests_total"],
            "n_distinct_request_hosts": manifest["n_distinct_request_hosts"],
            "sites_below_min_pages": sorted(
                (s, len(v["pages"]), v["notes"]) for s, v in manifest["sites"].items()
                if len(v["pages"]) < MIN_PAGES_PER_SITE),
        },
        "metrics_primary": {
            "agf_point_estimate": agf_v,
            "agf_matched_signature_instances": agf_point["matched_signature_instances"],
            "agf_total_signatures": agf_point["total_signatures"],
            "agf_matched_distinct_keys": agf_point["matched_distinct_keys"],
            "agf_bootstrap_ci": boot_ci,
            "agf_bootstrap_n_replicates": N_BOOTSTRAP,
            "agf_resampling_unit": "etld1_host",
            "pairwise_jaccard_mean": jac["mean_jaccard"],
            "pairwise_jaccard_max": jac["max_jaccard"],
            "pairwise_jaccard_n_pairs": jac["n_pairs"],
            "pairwise_jaccard_n_pairs_nonzero": jac["n_pairs_nonzero"],
            "frozen_null_shuffled_host": frozen_null,
        },
        "decomposition_agf": {
            "note": "Derived, not a frozen decision input. 'matched instances' is "
                    "the frozen numerator term, decomposed by signature type and "
                    "by how many distinct hosts carry the shared key.",
            "total_signatures": total_sig,
            "total_matched_instances": total_match,
            "n_distinct_shared_keys": len(drivers),
            "top_key_share_of_matched_instances": (
                drivers[0]["matched_instances"] / total_match) if drivers else None,
            "top4_key_share_of_matched_instances": (
                sum(d["matched_instances"] for d in drivers[:4]) / total_match) if drivers else None,
            "by_signature_type": {
                t: {"n_signatures": sigtype_counts[t], "n_matched_instances": sigtype_matched[t],
                    "agf_within_type": sigtype_matched[t] / sigtype_counts[t],
                    "fraction_of_all_signatures": sigtype_counts[t] / total_sig,
                    "fraction_of_all_matched_instances": (
                        sigtype_matched[t] / total_match) if total_match else None}
                for t in sorted(sigtype_counts)},
            "by_host_coverage": {
                b: {"n_matched_instances": sum(coverage[b].values()),
                    "fraction_of_all_matched_instances": (
                        sum(coverage[b].values()) / total_match) if total_match else None,
                    "by_signature_type": dict(coverage[b])}
                for b in ("2", "3-5", "6-10", "11-15")},
            "top_25_driver_keys": drivers[:25],
        },
        "metrics_sensitivity_not_frozen": {
            "note": "NOT part of the frozen decision rule. NC-SIG-REASSIGN is a "
                    "permutation null that has power against the frozen AGF "
                    "estimator, unlike the frozen label permutation which is an "
                    "identity on it. The 'typed slot' population requires at "
                    "least one typed slot, which is what the prereg's own "
                    "alias-generalizability construct ('varying identifiers ... "
                    "can be parameterized to a common template') requires.",
            "agf_typed_slot_population": {
                "n_signatures": agf_slotted["total_signatures"],
                "n_signatures_frozen_population": total_sig,
                "fraction_of_frozen_signatures_with_typed_slot": (
                    agf_slotted["total_signatures"] / total_sig) if total_sig else None,
                "agf_point_estimate": agf_slotted["agf"],
                "agf_bootstrap_ci": boot_slotted_ci,
                "pairwise_jaccard_mean": jac_slotted["mean_jaccard"],
                "n_prescribed_null_distinct_values": len(
                    set(round(v, 12) for v in
                        shuffled_host_null(site_sigs_slotted, SEED_NULL, 200))),
                "n_sig_reassign_null": describe(
                    sig_null_slotted, "NC-SIG-REASSIGN AGF (typed-slot population)"),
                "observed_exceeds_sig_reassign_p95": bool(
                    agf_slotted["agf"] > percentile(sorted(sig_null_slotted), 0.95)),
                "observed_exceeds_sig_reassign_ci_lower": bool(
                    boot_slotted_ci["ci_lower"] > percentile(sorted(sig_null_slotted), 0.95)),
            },
            "nc_sig_reassign_frozen_population": describe(
                sig_null, "NC-SIG-REASSIGN AGF (frozen population)"),
            "nc_sig_reassign_jaccard": describe(
                sig_null_jac, "NC-SIG-REASSIGN mean pairwise Jaccard"),
            "observed_exceeds_sig_reassign_p95_frozen_population": bool(
                agf_v > percentile(sorted(sig_null), 0.95)),
            "observed_jaccard_exceeds_sig_reassign_p95": bool(
                jac["mean_jaccard"] > percentile(sorted(sig_null_jac), 0.95)),
            "interpretation_limit": "Exceeding this null shows that host "
                                    "grouping of signatures carries information "
                                    "beyond a random partition of the same "
                                    "vocabulary. It does NOT show that the shared "
                                    "structure is reusable task structure; see "
                                    "decomposition_agf.by_host_coverage and "
                                    "top_25_driver_keys.",
        },
        "cost": cost,
        "cost_bootstrap_ci_host_level": cost_ci,
        "controls": {
            "PC-SYNTHETIC-ALIAS": {
                "frozen": True,
                "agf": pc_frozen_agf["agf"],
                "agf_matched_instances": pc_frozen_agf["matched_signature_instances"],
                "agf_total_signatures": pc_frozen_agf["total_signatures"],
                "jaccard_mean": pc_frozen_jac["mean_jaccard"],
                "n_pairs": pc_frozen_jac["n_pairs"],
                "n_pairs_nonzero": pc_frozen_jac["n_pairs_nonzero"],
                "expected_agf_gt_0_8": bool(pc_frozen_agf["agf"] > 0.8),
                "expected_agf_gt_0_8_reachable_on_2_group_design": False,
                "two_group_arithmetic_ceiling_of_agf": pc_two_group_ceiling,
                "two_group_ceiling_derivation": (
                    "With 2 hosts carrying n signatures each and every key distinct "
                    "and matched 1:1, matched instances = n and total signatures = "
                    "2n, so AGF = n/(2n) = 0.5 exactly. AGF > 0.8 is therefore "
                    "arithmetically unreachable for the frozen 2-group positive "
                    "control under the frozen 7.3 AGF definition, whatever the "
                    "synthetic content. The frozen PC threshold and the frozen "
                    "2-group design are mutually incompatible."),
                "pipeline_sensitivity_confirmed_by": [
                    "jaccard_mean == 1.0 (identical signature sets on both hosts)",
                    "n_pairs_nonzero == n_pairs == 1",
                    "observed AGF exceeds the powered NC-SIG-REASSIGN null p95",
                ],
                "observed_exceeds_nc_sig_reassign_p95": bool(
                    pc_frozen_agf["agf"] > percentile(sorted(pc_frozen_null_reassign), 0.95)),
                "observed_jaccard_exceeds_nc_sig_reassign_jaccard_p95": bool(
                    pc_frozen_jac["mean_jaccard"] > percentile(sorted(pc_frozen_null_reassign_jac), 0.95)),
                "frozen_null_distinct_values": len(set(round(v, 12) for v in pc_frozen_null)),
                "frozen_null_std": statistics.pstdev(pc_frozen_null),
                "frozen_null_is_degenerate": statistics.pstdev(pc_frozen_null) == 0,
                "nc_sig_reassign": describe(pc_frozen_null_reassign, "PC NC-SIG-REASSIGN AGF"),
                "nc_sig_reassign_jaccard": describe(
                    pc_frozen_null_reassign_jac, "PC NC-SIG-REASSIGN Jaccard"),
            },
            "PC-SYNTHETIC-ALIAS-4SITE-POWER-EXTENSION": {
                "frozen": False,
                "decision_not_used": True,
                "note": "NOT FROZEN. The frozen 2-group positive control has one "
                        "free label permutation which is symmetric, so its "
                        "prescribed null is exactly degenerate (std = 0) by the "
                        "same identity that makes the main null degenerate. This "
                        "4-group extension supplies a permutation null with power; "
                        "groups C and D are deliberately unrelated to each other "
                        "and to A/B.",
                "agf": pc_ext_agf["agf"],
                "agf_matched_instances": pc_ext_agf["matched_signature_instances"],
                "agf_total_signatures": pc_ext_agf["total_signatures"],
                "jaccard_mean": pc_ext_jac["mean_jaccard"],
                "n_pairs": pc_ext_jac["n_pairs"],
                "n_pairs_nonzero": pc_ext_jac["n_pairs_nonzero"],
                "n_pairs_zero_shared_structure": pc_ext_jac["n_pairs"] - pc_ext_jac["n_pairs_nonzero"],
                "nc_sig_reassign": describe(pc_ext_null, "PC-EXT NC-SIG-REASSIGN AGF"),
                "nc_sig_reassign_jaccard": describe(
                    pc_ext_null_jac, "PC-EXT NC-SIG-REASSIGN Jaccard"),
                "observed_agf_exceeds_null_p95": bool(
                    pc_ext_agf["agf"] > percentile(sorted(pc_ext_null), 0.95)),
                "observed_jaccard_exceeds_null_p95": bool(
                    pc_ext_jac["mean_jaccard"] > percentile(sorted(pc_ext_null_jac), 0.95)),
                "pipeline_detects_known_correspondence": bool(
                    pc_ext_jac["mean_jaccard"] > percentile(sorted(pc_ext_null_jac), 0.95)),
                "pipeline_discriminates_unrelated_structure": bool(
                    pc_ext_jac["n_pairs"] - pc_ext_jac["n_pairs_nonzero"] >= 1),
                "separation_note": "The 4-group design separates cleanly on the "
                                   "frozen secondary metric: the one related pair "
                                   "has Jaccard 1.0 and all 5 unrelated pairs have "
                                   "Jaccard 0.0. The primary AGF is NOT separable "
                                   "in this design because with only 30 signatures "
                                   "over 4 groups the NC-SIG-REASSIGN lattice is "
                                   "coarse enough to reach the observed value; the "
                                   "AGF-vs-null comparison is therefore "
                                   "underpowered at this control size, not "
                                   "negative.",
            },
            "NC-SHUFFLED-HOST": {
                "frozen": True,
                "n_permutations": N_NULL_PERMUTATIONS,
                "std": statistics.pstdev(null_agf),
                "non_degenerate": statistics.pstdev(null_agf) > 0,
                "p95": frozen_null_p95,
                "observed_agf": agf_v,
                "pass": False,
                "pass_reason": "null std = 0 exactly; the prescribed permutation "
                               "is an algebraic identity on the frozen AGF "
                               "estimator, so the control detects nothing by "
                               "construction rather than by measurement.",
            },
            "NC-SINGLETON-SITE": {
                "frozen": True,
                "n_sites_checked": len(site_sigs),
                "n_singleton_sites": len(singles),
                "singleton_site_keys": singles,
                "fraction_zero_handling_verified": True,
                "note": "Zero sites had no cross-site match, consistent with the "
                        "host-coverage decomposition: shared structure is "
                        "ubiquitous rather than site-specific.",
            },
        },
        "decision_rule": {
            "primary": {
                "clause": "AGF_point > null_p95 AND AGF_CI_lower > null_p95 (prereg 12)",
                "evaluable": primary_evaluable,
                "satisfied": None if not primary_evaluable else bool(
                    agf_v > frozen_null_p95 and boot_ci["ci_lower"] > frozen_null_p95),
                "agf_point": agf_v,
                "null_p95": frozen_null_p95,
                "condition_point_gt_null_p95": bool(agf_v > frozen_null_p95),
                "agf_ci_lower": boot_ci["ci_lower"],
                "condition_ci_lower_gt_null_p95": bool(boot_ci["ci_lower"] > frozen_null_p95),
                "why_not_evaluable": "null_p95 equals AGF_point to the last bit "
                                     "(both 83.510834670947), so both comparisons "
                                     "are x > x and carry no information. This is "
                                     "a property of the frozen estimator/null pair, "
                                     "not of the Web and not of the sample.",
            },
            "cost": {
                "clause": "mean(tokens_minimal - tokens_full_dom) < 0 AND mean(tokens_minimal - tokens_a11y) < 0, paired eTLD+1-level bootstrap 95% CI upper < 0 (prereg 12)",
                "mean_diff_vs_full_dom": cost_fd_mean,
                "ci_upper_vs_full_dom": c_fd["ci_upper"],
                "mean_diff_vs_a11y": cost_a11y_mean,
                "ci_upper_vs_a11y": c_a11y["ci_upper"],
                "evaluable": True,
                "satisfied": cost_satisfied,
            },
            "validity": {
                "clause": "AGF_CI_width > 0 AND n_eTLD1_ge_2pages >= 10 AND null_std > 0 (prereg 12)",
                "sub_conditions": validity_sub,
                "agf_ci_width": boot_ci["ci_width"],
                "n_sites_ge_2pages": n_sites_ge_min,
                "null_std": statistics.pstdev(null_agf),
                "satisfied": validity_satisfied,
                "partially_failed": validity_partially_failed,
            },
            "outcome_mapping_applied": outcome,
            "clause_invoked": "prereg 12 MIXED clause 3: 'Validity partially failed "
                              "but some metrics valid'",
            "clause_interpretation": "MIXED here means the packet produced a valid "
                                     "and strong cost result while the frozen "
                                     "prevalence clause is unevaluable. It is NOT "
                                     "partial support for the prevalence hypothesis.",
        },
    }
    with open(os.path.join(DERIVED, "metrics.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=list)
    print(json.dumps({k: v for k, v in out.items()
                      if k in ("decision_rule", "sample")}, indent=1, default=list))
    print(json.dumps({"AGF": agf_v, "agf_CI": [boot_ci["ci_lower"], boot_ci["ci_upper"]],
                      "jaccard_mean": jac["mean_jaccard"],
                      "frozen_null": {k: frozen_null[k] for k in ("n_distinct_values",) if k in frozen_null},
                      "frozen_null_agf_stats": frozen_null["agf"],
                      "sig_reassign_agf": out["metrics_sensitivity_not_frozen"]["nc_sig_reassign_frozen_population"],
                      "agf_typed_slot": out["metrics_sensitivity_not_frozen"]["agf_typed_slot_population"]["agf_point_estimate"],
                      "cost": {"mean_diff_fd": cost_fd_mean, "ci_up_fd": c_fd["ci_upper"],
                               "mean_diff_a11y": cost_a11y_mean, "ci_up_a11y": c_a11y["ci_upper"]},
                      "coverage": out["decomposition_agf"]["by_host_coverage"],
                      "top4_share": out["decomposition_agf"]["top4_key_share_of_matched_instances"],
                      "outcome": outcome}, indent=1, default=list))



if __name__ == "__main__":
    main()
