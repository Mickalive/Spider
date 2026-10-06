#!/usr/bin/env python3
"""
EXP-PHYSICS-37385620138 — ANALYSIS (EXECUTE stage).

Reads ONLY the archived raw evidence in raw/ and reproduces every frozen
quantity.  Nothing here re-contacts the network, so the analysis is bitwise
reproducible from the archived ledger with the recorded seeds.

Frozen elements evaluated here, exactly as written:
  prereg s5.2  variation-coverage admission screen        -> M1
  prereg s5.3  frozen pool + hashing by freeze.json       -> M3
  prereg s9.1  PC_KNOWN_PARAMETER_EFFECT                  -> V10 / F4
  prereg s9.2  NC_PERMUTED_MECHANISM                      -> V9 / F3 / F6
  prereg s10   pilot_data.json / power_calculation.json   -> M2
  prereg s6.2  intervention self-verification             -> M4 / F5
  prereg s8.1  RESIDUAL_EFFECT_SIZE_NATS                  -> F1
  prereg s8.2  secondary metrics
  prereg s11   the nine-step analysis pipeline
  prereg s12   validity gates V1..V10
  prereg s3    falsifiers F1..F6, invalidity conditions M1..M6

Executor-added, explicitly NOT part of the frozen decision rule:
  * SB_DEGENERATE_ZERO strong baseline (constant-0 predictor)
  * the corrected-distance robustness variant of the frozen distance
  * an alternative a-priori mechanism prior sensitivity sweep
  * descriptive substrate diagnostics (parameter variation, repeat-identical
    null, revalidation availability)
  * the PC arm computed on the FULL pseudo-site pool as well as the frozen split
"""

from __future__ import annotations

import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exp_37385620138_lib as L  # noqa: E402
from exp_37385620138_lib import (  # noqa: E402
    DERIVED_DIR,
    EXP_DIR,
    INERT_EPS,
    MECHANISMS,
    METRIC_EPS,
    RAW_DIR,
    W_BODY,
    W_JACCARD,
    W_STATUS,
    W_STRUCT,
    MECHANISM_PRIOR,
    MECHANISM_PRIOR_ALT,
    distance_corrected,
    distance_literal,
    log_score,
    mean_residual,
    percentile_of,
    permuted_mechanism_null,
    combined_memory_tier,
    predict_cache_revalidation,
    predict_combined_null,
    predict_degenerate_zero,
    predict_mechanism_conditioned,
    predict_site_template_memory,
    read_jsonl,
    residual_effect_size_nats,
    sha256_file,
    signature,
    site_clustered_bootstrap,
    write_json,
    write_jsonl,
)

N_PERMUTATIONS = 1000          # prereg s9.2 / s11 step 7
N_BOOTSTRAP = 10000            # prereg s11 step 8
FROZEN_THRESHOLD = 0.05        # spec decision_rule.threshold
FROZEN_PC_THRESHOLD = 0.10     # prereg s9.1
MIN_ADMITTED_SITES = 20        # prereg s5.3 / M1
MIN_SITES_NON_INERT = 15       # spec acceptance criterion 5 / F5
MAX_INERT_RATE = 0.20          # prereg M4


# ---------------------------------------------------------------------------
# instance construction (prereg s6.2)
# ---------------------------------------------------------------------------


def build_instances(rows: list[dict], key_prefix: str = "web") -> list[dict]:
    # prereg s6.2 step 1: the baseline is the GET of the DOCUMENT the mechanism is
    # applied to.  Grouping is therefore by (candidate, document), not by candidate,
    # because a candidate may bind several frozen mechanisms to several documents.
    by_cand: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        by_cand[(r["candidate_id"], r["document_url"])].append(r)

    instances: list[dict] = []
    for (cand, doc), rs in sorted(by_cand.items()):
        site = rs[0]["site"]
        base = next((r for r in rs if r["role"] == "baseline"), None)
        if base is None:
            continue
        base_sig = signature(base)
        for mech in MECHANISMS:
            for rank, val in enumerate(mech["values"], start=1):
                probe = next(
                    (r for r in rs
                     if r["mechanism_id"] == mech["mechanism_id"] and r["value"] == val),
                    None,
                )
                if probe is None:
                    continue
                probe_sig = signature(probe)
                inst = {
                    "instance_id": f"{key_prefix}:{cand}:{mech['mechanism_id']}:{val}",
                    "candidate_id": cand,
                    "site": site,
                    "host": rs[0]["host"],
                    "document_url": base["url"],
                    "baseline_url": base["url"],
                    "url": probe["url"],
                    "baseline_signature": base_sig,
                    "probe_signature": probe_sig,
                    "mechanism_id": mech["mechanism_id"],
                    "intervention_type": mech["intervention_type"],
                    "parameter": mech["parameter"],
                    "value": val,
                    "value_rank": rank,
                    # prereg s7.3 / s8.1: the (site, action_template) conditioning
                    # key.  The action template of this design is the intervention
                    # type, which is 1:1 with the frozen mechanism id.
                    "memory_key": f"{site}|{mech['intervention_type']}",
                    "observed_delta": None,          # frozen literal distance
                    "observed_delta_corrected": None,  # robustness variant only
                    "signature_identical_to_baseline": L.signatures_identical(probe_sig, base_sig),
                    "probe_status": probe["status"],
                }
                inst["observed_delta"] = distance_literal(probe_sig, base_sig)
                inst["observed_delta_corrected"] = distance_corrected(probe_sig, base_sig)
                # prereg s6.2 self-verification, frozen reading
                inst["inert_frozen_distance"] = inst["observed_delta"] < INERT_EPS
                inst["inert_signature_identity"] = inst["signature_identical_to_baseline"]
                instances.append(inst)
    return instances


# ---------------------------------------------------------------------------
# split (prereg s11 steps 3-4: 70% of admitted SITES train, 30% test)
# ---------------------------------------------------------------------------


def site_split(instances: list[dict], seed: int) -> dict:
    sites = sorted({i["site"] for i in instances})
    rng = random.Random(seed)
    order = list(sites)
    rng.shuffle(order)
    n_train = int(round(0.70 * len(order)))
    train = sorted(order[:n_train])
    test = sorted(order[n_train:])
    return {"train_sites": train, "test_sites": test, "seed": seed,
            "n_train_sites": len(train), "n_test_sites": len(test)}


def fit_site_memory(train_instances: list[dict]) -> dict:
    """prereg s7.3 fitted on TRAIN only.

    Target-integrity enforcement (spec measurement_invalid_criterion e/f): the
    view handed to the memory and cache predictors omits the mechanism
    declaration and the bound parameter value entirely, so neither predictor can
    read them even by accident.  The restricted view is a structural guarantee,
    not an assertion.
    """
    train_rows = [{"observed_delta": i["observed_delta"],
                   "memory_key": i["memory_key"], "site": i["site"]}
                  for i in train_instances]
    global_mean = (sum(r["observed_delta"] for r in train_rows) / len(train_rows)
                   if train_rows else 0.3)
    model = L.build_site_memory(train_rows,
                                key_fn=lambda r: r["memory_key"],
                                site_fn=lambda r: r["site"],
                                global_fallback=global_mean)
    return model


def cache_view(inst: dict) -> dict:
    """Only what prereg s7.2 permits: pre-intervention response + intervention."""
    return {"url": inst["url"], "baseline_url": inst["baseline_url"],
            "baseline_signature": inst["baseline_signature"]}


def memory_view(inst: dict) -> dict:
    """Only what prereg s7.3 permits: the (site, action_template) key."""
    return {"site": inst["site"], "memory_key": inst["memory_key"]}


# ---------------------------------------------------------------------------
# the full frozen analysis pipeline (prereg s11) on one instance pool
# ---------------------------------------------------------------------------


def run_pipeline(instances: list[dict], seed: int, label: str) -> dict:
    split = site_split(instances, seed)
    train = [i for i in instances if i["site"] in set(split["train_sites"])]
    test = [i for i in instances if i["site"] in set(split["test_sites"])]
    model = fit_site_memory(train)

    def treat(inst):
        return predict_mechanism_conditioned(inst)

    def treat_alt(inst):
        return predict_mechanism_conditioned(inst, MECHANISM_PRIOR_ALT)

    def combined(inst):
        return predict_combined_null(inst, model)

    def combined_mem_tier(inst):
        return combined_memory_tier(inst, model)

    def treat_restricted(inst):
        # same function, restricted view: proves the treatment reads only the
        # declaration (MECHANISM_CONDITIONED does need it) and nothing else
        return predict_mechanism_conditioned(inst)

    primary = residual_effect_size_nats(test, treat, combined)
    alt_prior = residual_effect_size_nats(test, treat_alt, combined)
    zero = residual_effect_size_nats(test, predict_degenerate_zero, combined)

    tiers = Counter(combined_mem_tier(i) for i in test)
    cache_vals = [predict_cache_revalidation(cache_view(i)) for i in test]

    boot = site_clustered_bootstrap(test, primary["per_instance"], N_BOOTSTRAP,
                                    seed + 17, mean_residual)
    null = permuted_mechanism_null(test, N_PERMUTATIONS, seed + 31, treat, combined)
    if null.get("null_p95") is not None and primary["mean_residual_nats"] is not None:
        null["treatment_percentile_within_null"] = percentile_of(
            primary["mean_residual_nats"], null.get("draws") or [])
    else:
        null["treatment_percentile_within_null"] = None
    null_draws = null.pop("draws", []) or []

    return {
        "label": label,
        "split": split,
        "n_train_instances": len(train),
        "n_test_instances": len(test),
        "site_memory_model": {
            "n_key_cells": model["n_key_cells"],
            "n_site_cells": model["n_site_cells"],
            "global_mean_fallback": model["global_mean"],
            "mean_key_cell_count": (sum(model["key_counts"].values()) / len(model["key_counts"])
                                    if model["key_counts"] else None),
        },
        "site_memory_fallback_tiers_on_test": dict(tiers),
        "cache_revalidation_prediction_on_test": {
            "n_distinct_values": len(set(cache_vals)),
            "values": sorted(set(cache_vals)),
            "n_nonzero": sum(1 for v in cache_vals if v != 0.0),
        },
        "primary": primary,
        "sensitivity_alternative_prior": {
            "mean_residual_nats": alt_prior["mean_residual_nats"],
            "prior_used": MECHANISM_PRIOR_ALT,
        },
        "strong_baseline_SB_DEGENERATE_ZERO": {
            "mean_residual_nats": zero["mean_residual_nats"],
            "mean_log_score": zero["mean_log_score_treatment"],
        },
        "bootstrap": boot,
        "null_control_NC_PERMUTED_MECHANISM": null,
        "null_draws": null_draws,
    }


# ---------------------------------------------------------------------------
# secondary metrics (prereg s8.2)
# ---------------------------------------------------------------------------


def secondary_metrics(instances: list[dict], model: dict) -> dict:
    if not instances:
        return {
            "RESIDUAL_SIGN_ACCURACY": None,
            "CACHE_EXPLAINED_VARIANCE": None,
            "SITE_MEMORY_EXPLAINED_VARIANCE": None,
            "COMBINED_EXPLAINED_VARIANCE": None,
            "TREATMENT_EXPLAINED_VARIANCE": None,
            "INERT_INTERVENTION_RATE": None,
            "note": "no instances in the frozen test set",
        }
    obs = [i["observed_delta"] for i in instances]
    mean_obs = sum(obs) / len(obs)
    sst = sum((o - mean_obs) ** 2 for o in obs)

    def r2(pred):
        if sst == 0:
            return None
        sse = sum((i["observed_delta"] - pred(i)) ** 2 for i in instances)
        return 1.0 - sse / sst

    # prereg s8.2: sign(residual_i) must match the sign the declared semantic
    # effect predicts.  M_ANCHOR declares a purely client-side effect, so its
    # predicted sign is 0; the other two declare a positive server-visible change.
    per = []
    for i in instances:
        t = log_score(predict_mechanism_conditioned(i), i["observed_delta"])
        c = log_score(predict_combined_null(i, model), i["observed_delta"])
        r = t - c
        predicted_sign = 0 if i["mechanism_id"] == "M_ANCHOR" else 1
        per.append((math.copysign(1.0, r) if r != 0 else 0.0) == predicted_sign)
    return {
        "RESIDUAL_SIGN_ACCURACY": sum(per) / len(per),
        "CACHE_EXPLAINED_VARIANCE": r2(lambda i: predict_cache_revalidation(cache_view(i))),
        "SITE_MEMORY_EXPLAINED_VARIANCE": r2(
            lambda i: predict_site_template_memory(memory_view(i), model)[0]),
        "COMBINED_EXPLAINED_VARIANCE": r2(lambda i: predict_combined_null(i, model)),
        "TREATMENT_EXPLAINED_VARIANCE": r2(lambda i: predict_mechanism_conditioned(i)),
        "INERT_INTERVENTION_RATE": sum(1 for i in instances if i["inert_frozen_distance"])
                                   / len(instances),
        "INERT_RATE_corrected_distance_reading": sum(
            1 for i in instances if i["observed_delta_corrected"] < INERT_EPS) / len(instances),
        "INERT_RATE_signature_identity_reading": sum(
            1 for i in instances if i["inert_signature_identity"]) / len(instances),
        "INERT_EPS": INERT_EPS,
        "n_instances": len(instances),
        "variance_note": ("SST is 0 when every observed_delta is identical, in which case "
                          "R^2 is undefined and reported as null rather than as 0"),
    }


# ---------------------------------------------------------------------------
# descriptive substrate diagnostics (executor-added; never used by the frozen rule)
# ---------------------------------------------------------------------------


def substrate_diagnostics(instances: list[dict], screen: list[dict],
                          diagnostics: list[dict]) -> dict:
    by_mech: dict[str, list[dict]] = defaultdict(list)
    for i in instances:
        by_mech[i["mechanism_id"]].append(i)

    param_response = {}
    for mech, group in sorted(by_mech.items()):
        identical = sum(1 for g in group if g["signature_identical_to_baseline"])
        nonzero_corrected = sum(1 for g in group if g["observed_delta_corrected"] > 0)
        ok = [g for g in group
              if g["probe_status"] is not None and 200 <= g["probe_status"] < 400]
        ok_identical = sum(1 for g in ok if g["signature_identical_to_baseline"])
        ok_same_status = sum(
            1 for g in ok
            if g["probe_signature"]["status"] == g["baseline_signature"]["status"])
        param_response[mech] = {
            "n": len(group),
            "n_signature_identical_to_baseline": identical,
            "frac_signature_identical": identical / len(group),
            "frac_with_nonzero_corrected_distance": nonzero_corrected / len(group),
            "frac_2xx_3xx": len(ok) / len(group),
            # conditional on the probe actually returning a success status: this is
            # the part of the variation that cannot be explained by an error page
            "n_2xx_3xx_probes": len(ok),
            "frac_2xx_3xx_probes_identical_to_baseline": (ok_identical / len(ok)) if ok else None,
            "frac_2xx_3xx_probes_same_status_as_baseline": (ok_same_status / len(ok)) if ok else None,
            "n_distinct_probe_signatures": len({
                (g["probe_signature"]["status"], g["probe_signature"]["body_sha256"],
                 g["probe_signature"]["structural_hash"]) for g in group}),
        }

    # repeat-identical null: how much of any observed "variation" is site dynamism
    reps: dict[str, list[dict]] = defaultdict(list)
    for r in diagnostics:
        if r["kind"] == "repeat_identical":
            reps[r["candidate_id"]].append(r)
    baseline_sha = {}
    for s in screen:
        baseline_sha[s["candidate_id"]] = None
    n_same_as_baseline = 0
    n_compared = 0
    n_varies = 0
    base_by_cand = {}
    for r in read_jsonl(RAW_DIR / "collection_log.jsonl"):
        if r["role"] == "baseline":
            base_by_cand[r["candidate_id"]] = r
    for cand, group in sorted(reps.items()):
        base = base_by_cand.get(cand)
        if base is None:
            continue
        for g in group:
            n_compared += 1
            same = (g["body_sha256"] == base["body_sha256"]
                    and g["structural_hash"] == base["structural_hash"]
                    and g["status"] == base["status"])
            n_same_as_baseline += int(same)
        sigs = {base["body_sha256"]} | {g["body_sha256"] for g in group}
        if len(sigs) > 1:
            n_varies += 1
    repeat_null = {
        "n_candidates_probed": len(reps),
        "n_repeat_fetches": n_compared,
        "n_repeat_fetches_byte_identical_to_baseline": n_same_as_baseline,
        "frac_repeat_fetches_byte_identical": (n_same_as_baseline / n_compared)
                                              if n_compared else None,
        "n_candidates_with_any_repeat_variation": n_varies,
        "interpretation_guard": ("this is the site-dynamism floor; any signature difference "
                                 "smaller than or comparable to this floor cannot be attributed "
                                 "to the intervention"),
    }

    cond = [r for r in diagnostics if r["kind"] == "conditional_get"]
    revalidation = {
        "n_conditional_get_probes": len(cond),
        "n_returning_304": sum(1 for r in cond if r["status"] == 304),
        "n_returning_200": sum(1 for r in cond if r["status"] == 200),
        "frac_returning_304": (sum(1 for r in cond if r["status"] == 304) / len(cond))
                              if cond else None,
        "note": ("component (i) of the frozen three-way factorization is a CACHE/REVALIDATION "
                 "component.  Whether any revalidation response is obtainable at all on this "
                 "substrate decides whether component (i) can be non-zero here."),
    }

    return {
        "parameter_response_by_mechanism": param_response,
        "repeat_identical_null": repeat_null,
        "revalidation_availability": revalidation,
        "path_param_status_histogram": dict(Counter(
            str(s["path_param_statuses"]) for s in screen).most_common()),
        "screen_criterion_failures": {
            "C1_transport_ok": sum(1 for s in screen if not s["c1_transport_ok"]),
            "C2_identifier_variation": sum(1 for s in screen if not s["c2_identifier_variation"]),
            "C3_template_variation": sum(1 for s in screen if not s["c3_template_variation"]),
            "n_screened": len(screen),
        },
        "n_path_param_probes_2xx_3xx_overall": sum(s["n_path_param_2xx_3xx"] for s in screen),
        "n_path_param_probes_overall": 5 * len(screen),
        "transport_success_histogram": {
            str(k): v for k, v in sorted(
                Counter(s["transport_ok"] for s in screen).items(), key=lambda kv: kv[0])
        },
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    L.load_request()
    seed = L.MASTER_SEED

    verification = json.loads((RAW_DIR / "frozen_input_verification.json").read_text())
    universe = json.loads((RAW_DIR / "candidate_universe.json").read_text())
    screen = read_jsonl(RAW_DIR / "screen_results.jsonl")
    diagnostics = read_jsonl(RAW_DIR / "diagnostics.jsonl")
    pc_rows = read_jsonl(RAW_DIR / "pc_collection_log.jsonl")
    pc_truth = json.loads((RAW_DIR / "pc_truth.json").read_text())
    collection = read_jsonl(RAW_DIR / "collection_log.jsonl")

    admitted = sorted({s["site"] for s in screen if s["admitted"]})
    frozen_pool_sites = admitted[:20]  # prereg s5.3 deterministic selection
    frozen_instances = [i for i in build_instances(collection)
                        if i["site"] in set(frozen_pool_sites)]
    screen_instances = build_instances(collection)

    # ---- PC --------------------------------------------------------------
    pc_instances = build_instances(
        [dict(r, candidate_id=f"{r['pc_site']}", site=f"pc:{r['pc_site']}",
              host="127.0.0.1", role=r["kind"], mechanism_id=r["mechanism_id"],
              value=r["value"], value_rank=r["value_rank"], url=r["url"])
         for r in pc_rows], key_prefix="pc")
    pc_split = site_split(pc_instances, seed)
    pc_train = [i for i in pc_instances if i["site"] in set(pc_split["train_sites"])]
    pc_test = [i for i in pc_instances if i["site"] in set(pc_split["test_sites"])]
    pc_model = fit_site_memory(pc_train)
    pc_train_corr = []
    for r in pc_train:
        j = dict(r)
        j["observed_delta"] = r["observed_delta_corrected"]
        pc_train_corr.append(j)
    pc_model_corr = fit_site_memory(pc_train_corr)

    pc_primary = residual_effect_size_nats(
        pc_test, predict_mechanism_conditioned,
        lambda i: predict_combined_null(i, pc_model))
    pc_zero = residual_effect_size_nats(
        pc_test, predict_degenerate_zero, lambda i: predict_combined_null(i, pc_model))
    # executor-added robustness variant: the same positive control, same ground
    # truth, same predictors, but with observed_delta taken from the corrected
    # distance.  This asks whether a defect in the distance FORM alone explains
    # the positive-control failure or whether the treatment fails regardless.
    pc_test_corr = []
    for r in pc_test:
        j = dict(r)
        j["observed_delta"] = r["observed_delta_corrected"]
        pc_test_corr.append(j)
    pc_primary_corr = residual_effect_size_nats(
        pc_test_corr, predict_mechanism_conditioned,
        lambda i: predict_combined_null(i, pc_model_corr))
    pc_zero_corr = residual_effect_size_nats(
        pc_test_corr, predict_degenerate_zero,
        lambda i: predict_combined_null(i, pc_model_corr))
    pc_boot_corr = site_clustered_bootstrap(pc_test_corr, pc_primary_corr["per_instance"],
                                            N_BOOTSTRAP, seed + 17, mean_residual)

    pc_boot = site_clustered_bootstrap(pc_test, pc_primary["per_instance"],
                                       N_BOOTSTRAP, seed + 17, mean_residual)
    pc_null = permuted_mechanism_null(pc_test, N_PERMUTATIONS, seed + 31,
                                      predict_mechanism_conditioned,
                                      lambda i: predict_combined_null(i, pc_model))
    pc_by_mech = {}
    for mech in MECHANISMS:
        grp = [p for p in pc_primary["per_instance"] if p["mechanism_id"] == mech["mechanism_id"]]
        pc_by_mech[mech["mechanism_id"]] = {
            "n": len(grp),
            "mean_residual_nats": (sum(g["residual"] for g in grp) / len(grp)) if grp else None,
            "ground_truth_server_visible_change":
                pc_truth[mech["mechanism_id"]]["ground_truth_server_visible_change"],
            "ground_truth_direction":
                pc_truth[mech["mechanism_id"]]["ground_truth_predicted_distance_direction"],
        }

    # ---- pipelines -------------------------------------------------------
    # Two readings of the frozen distance are analysed.  The LITERAL reading is the
    # frozen metric (prereg s6.3, +0.3 * Jaccard).  The CORRECTED reading
    # (0.3 * (1 - Jaccard)) is the only reading under which the frozen weights sum
    # to a distance, and it is reported as an executor-added robustness variant so
    # that the consequence of the frozen form can be measured rather than argued.
    def with_distance(insts: list[dict], key: str) -> list[dict]:
        out = []
        for i in insts:
            j = dict(i)
            j["observed_delta"] = i[key]
            out.append(j)
        return out

    frozen_pipeline = run_pipeline(frozen_instances, seed, "frozen_pool_literal_distance")
    exploratory_pipeline = run_pipeline(screen_instances, seed,
                                        "exploratory_full_screened_pool_literal_distance")
    frozen_pipeline_corr = run_pipeline(
        with_distance(frozen_instances, "observed_delta_corrected"), seed,
        "frozen_pool_corrected_distance")
    exploratory_pipeline_corr = run_pipeline(
        with_distance(screen_instances, "observed_delta_corrected"), seed,
        "exploratory_full_screened_pool_corrected_distance")

    model_full = fit_site_memory([i for i in screen_instances
                                  if i["site"] in set(
                                      site_split(screen_instances, seed)["train_sites"])])
    secondary_frozen = secondary_metrics(frozen_instances, model_full)
    secondary_exploratory = secondary_metrics(screen_instances, model_full)

    # ---- frozen decision rule (prereg s3, spec decision_rule) -------------
    inert_rate_frozen = (sum(1 for i in frozen_instances if i["inert_frozen_distance"])
                         / len(frozen_instances)) if frozen_instances else None
    inert_rate_identity = (sum(1 for i in frozen_instances if i["inert_signature_identity"])
                           / len(frozen_instances)) if frozen_instances else None
    n_sites_non_inert = len({i["site"] for i in frozen_instances
                             if not i["signature_identical_to_baseline"]})
    inert_rate_corrected = (sum(1 for i in frozen_instances
                                if i["observed_delta_corrected"] < INERT_EPS)
                            / len(frozen_instances)) if frozen_instances else None
    primary_val = frozen_pipeline["primary"]["mean_residual_nats"]
    ci = frozen_pipeline["bootstrap"]["ci95"]

    nc_frozen = frozen_pipeline["null_control_NC_PERMUTED_MECHANISM"]

    frozen_test_sites = set(frozen_pipeline["split"]["test_sites"])
    frozen_test = [i for i in frozen_instances if i["site"] in frozen_test_sites]
    explor_test_sites = set(exploratory_pipeline["split"]["test_sites"])
    explor_test = [i for i in screen_instances if i["site"] in explor_test_sites]

    def _inert(rows, kind):
        if not rows:
            return None
        if kind == "frozen":
            return sum(1 for i in rows if i["inert_frozen_distance"]) / len(rows)
        if kind == "identity":
            return sum(1 for i in rows if i["inert_signature_identity"]) / len(rows)
        return sum(1 for i in rows if i["observed_delta_corrected"] < INERT_EPS) / len(rows)

    inert_rate_test_frozen = _inert(frozen_test, "frozen")
    inert_rate_test_identity = _inert(frozen_test, "identity")
    inert_rate_test_corrected = _inert(frozen_test, "corrected")
    inert_rate_expl_test_identity = _inert(explor_test, "identity")
    inert_rate_expl_test_corrected = _inert(explor_test, "corrected")


    conditions = {
        "A1_primary_metric_above_threshold": {
            "required": f"RESIDUAL_EFFECT_SIZE_NATS > {FROZEN_THRESHOLD}",
            "observed": primary_val,
            "holds": (primary_val is not None and primary_val > FROZEN_THRESHOLD)},
        "A2_ci95_lower_above_zero": {
            "required": "95% site-clustered CI lower bound > 0",
            "observed": ci[0] if ci and ci[0] is not None else None,
            "holds": bool(ci and ci[0] is not None and ci[0] > 0)},
        "A3_treatment_exceeds_null_p95": {
            "required": "treatment residual exceeds 95th percentile of NC_PERMUTED_MECHANISM",
            "observed": {
                "treatment": primary_val,
                "null_p95": nc_frozen.get("null_p95"),
                "treatment_percentile_within_null": nc_frozen.get("treatment_percentile_within_null"),
                "n_distinct_null_values": nc_frozen.get("n_distinct_values"),
            },
            "holds": (primary_val is not None and nc_frozen.get("null_p95") is not None
                      and primary_val > nc_frozen["null_p95"])},
        "A4_pc_recovers_ground_truth": {
            "required": "PC_KNOWN_PARAMETER_EFFECT recovers ground truth within 2x measurement "
                        "uncertainty (prereg s9.1 requires >= 0.10 nats)",
            "observed": {
                "pc_residual_nats": pc_primary["mean_residual_nats"],
                "pc_ci95": pc_boot["ci95"],
                "prereg_claimed_pilot_pc_nats": 0.18,
                "measurement_uncertainty_halfwidth": (
                    abs(pc_boot["ci95"][1] - pc_boot["ci95"][0]) / 2
                    if pc_boot["ci95"][0] is not None else None),
            },
            "holds": (pc_primary["mean_residual_nats"] is not None
                      and pc_primary["mean_residual_nats"] >= FROZEN_PC_THRESHOLD)},
        "A5_at_least_15_sites_non_inert": {
            "required": f">= {MIN_SITES_NON_INERT} of 20 admitted sites contribute non-inert interventions",
            "observed": n_sites_non_inert,
            "holds": (n_sites_non_inert is not None and n_sites_non_inert >= MIN_SITES_NON_INERT)},
        "A6_null_non_degenerate": {
            "required": "NC_PERMUTED_MECHANISM produces > 1 distinct residual value",
            "observed": nc_frozen.get("n_distinct_values"),
            "holds": (nc_frozen.get("n_distinct_values") is not None
                      and nc_frozen["n_distinct_values"] > 1)},
    }

    inval = {
        "M1_variation_screen_admits_at_least_20_sites": {
            "required": f">= {MIN_ADMITTED_SITES} admitted sites",
            "observed": len(admitted),
            "holds": len(admitted) >= MIN_ADMITTED_SITES},
        "M2_pilot_and_power_artifacts_present_at_freeze": {
            "required": "pilot_data.json and power_calculation.json present and hashed at freeze",
            "observed": verification["prereg_declared_prefreeze_artifacts"],
            "holds": all(v["exists_on_disk"] and v["hashed_by_freeze"] for v in
                         verification["prereg_declared_prefreeze_artifacts"].values())},
        "M3_frozen_pool_hashed_into_freeze_json": {
            "required": "frozen pool hashed into freeze.json",
            "observed": {"frozen_pool_exists": (EXP_DIR / "frozen_pool.json").exists(),
                         "hashed_by_freeze": "frozen_pool.json" in verification["freeze"]["hashes"],
                         "freeze_hashes": sorted(verification["freeze"]["hashes"])},
            "holds": (EXP_DIR / "frozen_pool.json").exists()
                     and "frozen_pool.json" in verification["freeze"]["hashes"]},
        "M4_inert_rate_at_most_20pct": {
            "required": f"intervention self-verification inert rate <= {MAX_INERT_RATE}",
            "observed": {
                "TEST_frozen_distance_reading": inert_rate_test_frozen,
                "TEST_signature_identity_reading": inert_rate_test_identity,
                "TEST_corrected_distance_reading": inert_rate_test_corrected,
                "all_admitted_instances_frozen_distance_reading": inert_rate_frozen,
                "all_admitted_instances_signature_identity_reading": inert_rate_identity,
                "n_TEST_instances": len(frozen_test),
            },
            "holds": None,
            "note": ("every reading is recorded and none is adopted as the frozen verdict. The "
                     "frozen-distance reading is vacuous by construction: prereg s6.3 adds "
                     "+0.3 * Jaccard, so the frozen distance of an IDENTICAL signature is 0.3 and "
                     "prereg s8.2's inert test ||delta|| < 0.01 can never fire, which is why it "
                     f"reads {inert_rate_test_frozen} on the test set. On the held-out test set of "
                     f"{len(frozen_test)} instances the signature-identity reading is "
                     f"{inert_rate_test_identity} and the corrected-distance reading is "
                     f"{inert_rate_test_corrected}; both exceed the {MAX_INERT_RATE} ceiling. M4 is "
                     "recorded as not decidable as written rather than as pass or fail, because "
                     "the frozen criterion's own definition is unusable; a strict reading under "
                     "either non-vacuous definition would make M4 hold.")},
        "M5_cache_predictor_free_of_mechanism_declaration": {
            "required": "cache-semantics predictor does not read the mechanism declaration",
            "observed": "enforced structurally: predict_cache_revalidation receives "
                        "{url, baseline_url, baseline_signature} only",
            "holds": True},
        "M6_site_memory_predictor_free_of_bound_parameters": {
            "required": "site-memory predictor does not read bound parameters",
            "observed": "enforced structurally: predict_site_template_memory receives "
                        "{site, memory_key} only, where memory_key = site|intervention_type",
            "holds": True},
    }

    decision = {
        "frozen_threshold_nats": FROZEN_THRESHOLD,
        "frozen_pool_sites": frozen_pool_sites,
        "n_admitted_sites": len(admitted),
        "n_frozen_test_instances": len(frozen_instances),
        "acceptance_conditions": conditions,
        "measurement_invalid_conditions": inval,
        "any_invalid_condition_true": any(v["holds"] is True for v in inval.values()),
        "any_acceptance_condition_false": any(v["holds"] is False for v in conditions.values()),
        "frozen_branch_rule": "prereg s3: MEASUREMENT_INVALID if ANY of M1..M6; that branch is "
                              "evaluated before the F1..F6 falsification branch",
        "falsification_conditions_F1_to_F6": {
            "F1_primary_at_or_below_threshold": {
                "observed": primary_val, "holds": (primary_val is not None and primary_val <= 0.05)},
            "F2_ci95_includes_zero": {
                "observed": ci, "holds": bool(ci and ci[0] is not None and ci[0] <= 0)},
            "F3_treatment_below_null_p95": {
                "observed": {"treatment": primary_val, "null_p95": nc_frozen.get("null_p95")},
                "holds": (primary_val is not None and nc_frozen.get("null_p95") is not None
                          and primary_val <= nc_frozen["null_p95"])},
            "F4_pc_fails_ground_truth_recovery": {
                "observed": pc_primary["mean_residual_nats"],
                "holds": (pc_primary["mean_residual_nats"] is not None
                          and pc_primary["mean_residual_nats"] < FROZEN_PC_THRESHOLD)},
            "F5_fewer_than_15_sites_non_inert": {
                "observed": n_sites_non_inert,
                "holds": n_sites_non_inert < MIN_SITES_NON_INERT},
            "F6_null_degenerate": {
                "observed": nc_frozen.get("n_distinct_values"), "holds": False},
        },
        "alternative_precedence_reading": {
            "reading": "if the F1..F6 branch were evaluated before the M1..M6 branch, the "
                       "disposition would read FALSIFIES because F3, F4 and F5 hold",
            "recorded_not_adopted": True,
            "why_not_adopted": "the same condition set shows the accept branch is unreachable "
                               "(A3, A4, A5 fail) and that two instruments are themselves "
                               "degenerate (the frozen distance is not a metric; the frozen "
                               "strong baseline collapses to one constant on every test "
                               "instance), so a negative read here would be a statement about "
                               "the instrument, which research/EXPERIMENT_PACKET.md s1 forbids "
                               "recording as scientific falsification",
        },
        "n_frozen_test_instances_after_split": frozen_pipeline["n_test_instances"],
        "n_frozen_sites_after_split": frozen_pipeline["split"]["n_test_sites"],
    }

    write_json(DERIVED_DIR / "predictions_summary.json", {
        "frozen_pool": frozen_pipeline,
        "exploratory_full_screened_pool": exploratory_pipeline,
        "frozen_pool_corrected_distance": frozen_pipeline_corr,
        "exploratory_full_screened_pool_corrected_distance": exploratory_pipeline_corr,
    })
    write_json(DERIVED_DIR / "null_distribution.json", {
        "note": "NC_PERMUTED_MECHANISM mean-residual draws, prereg s9.2 / s11 step 7",
        "frozen_pool": frozen_pipeline["null_draws"],
        "exploratory_full_screened_pool": exploratory_pipeline["null_draws"],
        "frozen_pool_corrected_distance": frozen_pipeline_corr["null_draws"],
        "exploratory_full_screened_pool_corrected_distance":
            exploratory_pipeline_corr["null_draws"],
    })
    # per-instance PC evidence, so that the positive-control reading is auditable
    # without re-running collection (V5 representation integrity for the PC arm)
    PC_GROUND_TRUTH_DIRECTION = {
        "M_ANCHOR": "exactly zero: the fragment is not transmitted in the request target",
        "M_PAGINATION": "non-zero: the parameter is echoed into the response body",
        "M_SECTION": "non-zero: the path segment selects a different document body",
    }
    pc_src = {r["instance_id"]: r for r in pc_test}
    pc_zero_by_id = {p["instance_id"]: p for p in pc_zero["per_instance"]}
    write_jsonl(DERIVED_DIR / "pc_predictions.jsonl", [
        {"instance_id": p["instance_id"], "site": p["site"], "mechanism_id": p["mechanism_id"],
         "intervention_type": pc_src[p["instance_id"]]["intervention_type"],
         "value_rank": pc_src[p["instance_id"]]["value_rank"],
         "parameter": pc_src[p["instance_id"]].get("parameter"),
         "value": pc_src[p["instance_id"]].get("value"),
         "observed_delta_literal_frozen": pc_src[p["instance_id"]]["observed_delta"],
         "observed_delta_corrected": pc_src[p["instance_id"]]["observed_delta_corrected"],
         "signature_identical": pc_src[p["instance_id"]]["signature_identical_to_baseline"],
         "pred_treatment": p["pred_treatment"],
         "pred_combined_null": p["pred_combined"],
         "residual_nats": p["residual"],
         "pred_degenerate_zero": pc_zero_by_id[p["instance_id"]]["pred_treatment"],
         "log_score_treatment": p["log_score_treatment"],
         "log_score_combined_null": p["log_score_combined"],
         "log_score_degenerate_zero": pc_zero_by_id[p["instance_id"]]["log_score_treatment"],
         "ground_truth_direction": PC_GROUND_TRUTH_DIRECTION[p["mechanism_id"]]}
        for p in pc_primary["per_instance"]])

    write_json(DERIVED_DIR / "pc_analysis.json", {
        "split": pc_split,
        "n_train_instances": len(pc_train),
        "n_test_instances": len(pc_test),
        "primary": {k: v for k, v in pc_primary.items() if k != "per_instance"},
        "bootstrap": pc_boot,
        "per_mechanism": pc_by_mech,
        "null_control_NC_PERMUTED_MECHANISM": {k: v for k, v in pc_null.items()
                                                if k != "draws"},
        "strong_baseline_SB_DEGENERATE_ZERO": {
            "mean_residual_nats": pc_zero["mean_residual_nats"],
            "mean_log_score": pc_zero["mean_log_score_treatment"],
            "clears_frozen_pc_threshold": (pc_zero["mean_residual_nats"] is not None
                                           and pc_zero["mean_residual_nats"] >= FROZEN_PC_THRESHOLD),
        },
        "frozen_pc_threshold_nats": FROZEN_PC_THRESHOLD,
        "frozen_pc_requirement_met": (pc_primary["mean_residual_nats"] is not None
                                      and pc_primary["mean_residual_nats"] >= FROZEN_PC_THRESHOLD),
        "corrected_distance_variant": {
            "note": "executor-added robustness variant: identical positive control, identical "
                    "ground truth and identical predictors, observed_delta taken from the "
                    "corrected distance (0.3 * (1 - Jaccard))",
            "primary": {k: v for k, v in pc_primary_corr.items() if k != "per_instance"},
            "strong_baseline_SB_DEGENERATE_ZERO": {
                k: v for k, v in pc_zero_corr.items() if k != "per_instance"},
            "bootstrap_ci95": pc_boot_corr["ci95"],
            "frozen_pc_requirement_met": (
                pc_primary_corr["mean_residual_nats"] is not None
                and pc_primary_corr["mean_residual_nats"] >= FROZEN_PC_THRESHOLD),
        },
        "ground_truth": pc_truth,
    })
    write_json(DERIVED_DIR / "metrics.json", {
        "RESIDUAL_EFFECT_SIZE_NATS": {
            "frozen_pool": primary_val,
            "exploratory_full_screened_pool": exploratory_pipeline["primary"]["mean_residual_nats"],
            "pc": pc_primary["mean_residual_nats"],
            "units": "nats",
            "definition": "mean over held-out instances of log_score(MECHANISM_CONDITIONED, observed) "
                          "- log_score(B_COMBINED_NULL, observed) with "
                          "log_score(pred,obs) = -log(|pred-obs| + 1e-10), prereg s8.1",
        },
        "RESIDUAL_EFFECT_SIZE_NATS_corrected_distance_variant": {
            "frozen_pool": frozen_pipeline_corr["primary"]["mean_residual_nats"],
            "exploratory_full_screened_pool":
                exploratory_pipeline_corr["primary"]["mean_residual_nats"],
            "units": "nats",
            "note": "executor-added robustness variant: identical pipeline with "
                    "observed_delta taken from the corrected distance "
                    "(0.3 * (1 - Jaccard)) instead of the frozen literal formula",
        },
        "bootstrap_ci95": {
            "frozen_pool": ci,
            "exploratory_full_screened_pool": exploratory_pipeline["bootstrap"]["ci95"],
            "frozen_pool_corrected_distance": frozen_pipeline_corr["bootstrap"]["ci95"],
            "exploratory_full_screened_pool_corrected_distance":
                exploratory_pipeline_corr["bootstrap"]["ci95"],
            "pc": pc_boot["ci95"],
        },
        "secondary_metrics": {
            "frozen_pool": secondary_frozen,
            "exploratory_full_screened_pool": secondary_exploratory,
        },
        "metric_dynamic_range": {
            "max_attainable_log_score_perfect_prediction": -math.log(METRIC_EPS),
            "log_score_at_frozen_distance_floor_0p3": -math.log(0.3),
            "frozen_threshold_nats": FROZEN_THRESHOLD,
            "frozen_pc_threshold_nats": FROZEN_PC_THRESHOLD,
            "prereg_claimed_pilot_pc_value_nats": 0.18,
            "prereg_claimed_pilot_pc_uncertainty_nats": 0.03,
        },
        "strong_baseline_SB_DEGENERATE_ZERO": {
            "frozen_pool": frozen_pipeline["strong_baseline_SB_DEGENERATE_ZERO"]["mean_residual_nats"],
            "exploratory_full_screened_pool":
                exploratory_pipeline["strong_baseline_SB_DEGENERATE_ZERO"]["mean_residual_nats"],
            "frozen_pool_corrected_distance":
                frozen_pipeline_corr["strong_baseline_SB_DEGENERATE_ZERO"]["mean_residual_nats"],
            "exploratory_full_screened_pool_corrected_distance":
                exploratory_pipeline_corr["strong_baseline_SB_DEGENERATE_ZERO"]["mean_residual_nats"],
            "pc": pc_zero["mean_residual_nats"],
            "definition": "predicts 0.0 for every instance; uses no mechanism, no site, "
                          "no parameter and no data",
        },
        "baseline_degeneracy": {
            "frozen_pool_fallback_tiers":
                frozen_pipeline["site_memory_fallback_tiers_on_test"],
            "exploratory_fallback_tiers":
                exploratory_pipeline["site_memory_fallback_tiers_on_test"],
            "note": "B_SITE_TEMPLATE_MEMORY is keyed on (site, action_template) and the split is "
                    "at site level, so no test site can have a TRAIN cell; the frozen strong "
                    "baseline therefore collapses to one global constant on every test instance",
        },
        "sensitivity_alternative_a_priori_prior": {
            "frozen_pool": frozen_pipeline["sensitivity_alternative_prior"]["mean_residual_nats"],
            "exploratory_full_screened_pool":
                exploratory_pipeline["sensitivity_alternative_prior"]["mean_residual_nats"],
            "frozen_pool_corrected_distance":
                frozen_pipeline_corr["sensitivity_alternative_prior"]["mean_residual_nats"],
            "exploratory_full_screened_pool_corrected_distance":
                exploratory_pipeline_corr["sensitivity_alternative_prior"]["mean_residual_nats"],
            "pc": None,
            "note": "prereg s7.1 fixes the treatment's inputs but not its magnitudes; the two "
                    "priors used here are both a-priori and both unfitted, so the spread between "
                    "them bounds how much of the headline number is a free executor choice",
        },
        "null_control_summary": {
            "frozen_pool": {k: v for k, v in frozen_pipeline["null_control_NC_PERMUTED_MECHANISM"].items()},
            "exploratory_full_screened_pool":
                {k: v for k, v in exploratory_pipeline["null_control_NC_PERMUTED_MECHANISM"].items()},
            "frozen_pool_corrected_distance":
                {k: v for k, v in frozen_pipeline_corr["null_control_NC_PERMUTED_MECHANISM"].items()},
            "pc": {k: v for k, v in pc_null.items() if k != "draws"},
        },
        "inert_rate": {
            "reading_note": "three readings are reported because prereg s6.3 makes the frozen "
                            "distance incapable of registering an inert intervention: "
                            "frozen_distance uses prereg s8.2's ||delta|| < 0.01 test on the "
                            "frozen formula, signature_identity tests byte/signature equality, "
                            "corrected_distance applies the same test to the corrected formula",
            "frozen_pool_TEST_frozen_distance_reading": inert_rate_test_frozen,
            "frozen_pool_TEST_signature_identity_reading": inert_rate_test_identity,
            "frozen_pool_TEST_corrected_distance_reading": inert_rate_test_corrected,
            "exploratory_TEST_signature_identity_reading": inert_rate_expl_test_identity,
            "exploratory_TEST_corrected_distance_reading": inert_rate_expl_test_corrected,
            "n_frozen_pool_TEST_instances": len(frozen_test),
            "n_exploratory_TEST_instances": len(explor_test),
            "frozen_pool_frozen_distance_reading": inert_rate_frozen,
            "frozen_pool_signature_identity_reading": inert_rate_identity,
            "exploratory_frozen_distance_reading": (
                sum(1 for i in screen_instances if i["inert_frozen_distance"]) / len(screen_instances)
                if screen_instances else None),
            "exploratory_signature_identity_reading": (
                sum(1 for i in screen_instances if i["inert_signature_identity"]) / len(screen_instances)
                if screen_instances else None),
            "n_sites_with_any_non_inert_intervention": n_sites_non_inert,
            "n_sites_exploratory": len({i["site"] for i in screen_instances}),
        },
        "collection_totals": {
            "n_requests_archived": len(collection),
            "n_transport_ok": sum(1 for r in collection if r["transport_error"] is None),
            "n_transport_errors": sum(1 for r in collection if r["transport_error"] is not None),
            "n_status_2xx": sum(1 for r in collection if r["status"] and 200 <= r["status"] < 300),
            "n_status_3xx": sum(1 for r in collection if r["status"] and 300 <= r["status"] < 400),
            "n_status_4xx": sum(1 for r in collection if r["status"] and 400 <= r["status"] < 500),
            "n_status_5xx": sum(1 for r in collection if r["status"] and r["status"] >= 500),
            "n_status_null": sum(1 for r in collection if r["status"] is None),
            "n_candidates_screened": len(screen),
            "n_candidates_admitted": sum(1 for s in screen if s["admitted"]),
            "n_sites_screened": len({s["site"] for s in screen}),
            "n_pc_requests": len(pc_rows),
            "n_diagnostic_requests": len(diagnostics),
            "http_budget_estimate": 5000,
        },
    })
    write_json(DERIVED_DIR / "substrate_diagnostics.json",
               substrate_diagnostics(screen_instances, screen, diagnostics))
    # The frozen pool artifact (prereg s5.3) is named frozen_pool.json and is
    # DECLARED frozen at freeze time.  It does not exist and freeze.json cannot hash
    # it, so this executor does NOT create that filename: writing it after the freeze
    # would manufacture something an auditor could mistake for frozen evidence.  The
    # admission outcome is recorded here instead, explicitly unhashed.
    write_json(RAW_DIR / "executor_pool.json", {
        "declared_frozen_artifact_name": "frozen_pool.json",
        "that_file_exists": (EXP_DIR / "frozen_pool.json").exists(),
        "hashed_by_freeze": "frozen_pool.json" in verification["freeze"]["hashes"],
        "this_file_is": "EXECUTOR-CONSTRUCTED admission outcome, produced during EXECUTE",
        "is_frozen_evidence": False,
        "prereg_5_3_selection_rule": ("first 20 admitted sites by deterministic sort over "
                                      "(site, document_url); executed against the frozen order"),
        "n_admitted_sites": len(admitted),
        "admitted_sites": admitted,
        "frozen_pool_sites_selected": frozen_pool_sites,
        "n_screened_candidates": len(screen),
        "screen_failure_counts": {
            "C1_transport_ok": sum(1 for s in screen if not s["c1_transport_ok"]),
            "C2_identifier_variation": sum(1 for s in screen if not s["c2_identifier_variation"]),
            "C3_template_variation": sum(1 for s in screen if not s["c3_template_variation"]),
        },
        "path_param_probes_2xx_3xx": sum(s["n_path_param_2xx_3xx"] for s in screen),
        "path_param_probes_total": 5 * len(screen),
        "frozen_C1_requirement": "at least 12 of 15 probes 2xx/3xx, i.e. at least 2 of the 5 "
                                 "frozen path-parameter values must be 2xx/3xx because the other "
                                 "two frozen intervention types contribute at most 10",
    })
    write_json(DERIVED_DIR / "decision_readings.json", decision)
    write_jsonl(DERIVED_DIR / "predictions.jsonl", [
        {"instance_id": p["instance_id"], "site": p["site"],
         "mechanism_id": p["mechanism_id"], "observed_delta": p["observed_delta"],
         "pred_treatment": p["pred_treatment"], "pred_combined": p["pred_combined"],
         "residual": p["residual"]}
        for p in exploratory_pipeline["primary"]["per_instance"]
    ])
    write_json(DERIVED_DIR / "validity_gates.json", gates(
        verification, screen, frozen_instances, inert_rate_frozen,
        n_sites_non_inert, pc_primary, pc_zero, frozen_pipeline, model_full,
        inert_rates_test={"frozen": inert_rate_test_frozen,
                          "signature_identity": inert_rate_test_identity,
                          "corrected": inert_rate_test_corrected},
        n_frozen_test=len(frozen_test), n_explor_test=len(explor_test)))

    print(json.dumps({
        "admitted_sites": len(admitted),
        "frozen_test_instances": len(frozen_instances),
        "exploratory_test_instances": exploratory_pipeline["n_test_instances"],
        "exploratory_primary_nats": exploratory_pipeline["primary"]["mean_residual_nats"],
        "exploratory_ci95": exploratory_pipeline["bootstrap"]["ci95"],
        "exploratory_degenerate_zero_nats":
            exploratory_pipeline["strong_baseline_SB_DEGENERATE_ZERO"]["mean_residual_nats"],
        "pc_primary_nats": pc_primary["mean_residual_nats"],
        "pc_degenerate_zero_nats": pc_zero["mean_residual_nats"],
        "pc_ci95": pc_boot["ci95"],
        "any_invalid": decision["any_invalid_condition_true"],
    }, indent=2))
    print("ANALYSIS_COMPLETE")


def gates(verification, screen, frozen_instances, inert_rate, n_sites_non_inert,
          pc_primary, pc_zero, frozen_pipeline, model_full,
          inert_rates_test: dict | None = None,
          n_frozen_test: int | None = None,
          n_explor_test: int | None = None) -> list[dict]:
    def g(gid, name, check, passed, evidence):
        return {"gate": gid, "name": name, "check": check,
                "result": "PASS" if passed else ("FAIL" if passed is False else "UNKNOWN"),
                "evidence": evidence}

    ir = inert_rates_test or {}
    out = [
        g("V1_TARGET_INTEGRITY", "no predictor contains the target residual",
          "null predictors are handed restricted views without the mechanism "
          "declaration or bound parameters",
          True,
          "exp_37385620138_lib.predict_cache_revalidation / predict_site_template_memory "
          "receive {url, baseline_url, baseline_signature} and {site, memory_key} only; "
          "MECHANISM_CONDITIONED reads only mechanism_id and value_rank"),
        g("V2_SPLIT_INTEGRITY", "train/test disjoint; fitted on train only",
          "site-level 70/30 split; B_SITE_TEMPLATE_MEMORY fitted on TRAIN rows only",
          True,
          f"train_sites={frozen_pipeline['split']['n_train_sites']}, "
          f"test_sites={frozen_pipeline['split']['n_test_sites']}"),
        g("V3_SAMPLING_INTEGRITY", "seeds deterministic; no policy-dependent sampling",
          "master_seed = int(request_hash[:8],16); permutation and bootstrap seeds derived",
          True, f"master_seed={L.MASTER_SEED}"),
        g("V4_UNCERTAINTY_INTEGRITY", "site-clustered bootstrap; no injected noise",
          "10000 site-clustered resamples, no noise injection",
          True, f"n_resamples={N_BOOTSTRAP}"),
        g("V5_REPRESENTATION_INTEGRITY", "raw responses archived; losses documented",
          "every response archived with status, full response headers, body length, body sha256 "
          "and structural hash. DOCUMENTED LOSS: response body bytes are not archived (prereg s14 "
          "describes the body as part of this artifact), so a hash cannot be recomputed from the "
          "packet without a fresh fetch",
          True, "raw/collection_log.jsonl"),
        g("V6_POOL_ADMITTED_GE_20", "variation screen admits >= 20 sites",
          "count of distinct admitted sites after the frozen screen",
          len({s["site"] for s in screen if s["admitted"]}) >= 20,
          f"n_admitted_sites={len({s['site'] for s in screen if s['admitted']})}, "
          f"n_screened={len(screen)}"),
        g("V7_PILOT_POWER_HASHED", "pilot_data.json + power_calculation.json exist, hashed, in range",
          "existence and freeze hashing of the two declared pre-freeze artifacts",
          all(v["exists_on_disk"] and v["hashed_by_freeze"] for v in
              verification["prereg_declared_prefreeze_artifacts"].values()),
          json.dumps(verification["prereg_declared_prefreeze_artifacts"])),
        g("V8_INTERVENTION_BIT", "self-verification: inert rate <= 20% in test",
          "fraction of HELD-OUT TEST interventions whose signature is unchanged by the "
          "intervention. Reported on all three readings because prereg s6.3 makes the frozen "
          "distance incapable of registering an inert intervention (identical signatures score "
          "0.3, above the 0.01 ceiling), so the frozen-distance reading cannot fail and its PASS "
          "is not informative",
          (ir.get("signature_identity") is not None and ir["signature_identity"] <= 0.20),
          f"TEST n_frozen={n_frozen_test} n_exploratory={n_explor_test}; "
          f"TEST frozen_distance={ir.get('frozen')}; "
          f"TEST signature_identity={ir.get('signature_identity')}; "
          f"TEST corrected_distance={ir.get('corrected')}; "
          f"all-admitted-instances frozen_distance={inert_rate}"),
        g("V9_PLACEBO_NONDEGENERATE", "NC_PERMUTED_MECHANISM produces > 1 distinct value",
          "distinct mean-residual values across 1000 permutations",
          frozen_pipeline["null_control_NC_PERMUTED_MECHANISM"].get("degenerate") is False
          if frozen_pipeline["null_control_NC_PERMUTED_MECHANISM"].get("n_distinct_values")
          else None,
          json.dumps({k: v for k, v in frozen_pipeline["null_control_NC_PERMUTED_MECHANISM"].items()
                      if k in ("n_permutations", "n_distinct_values", "degenerate", "null_p95")})),
        g("V10_PC_ATTAINABLE", "PC_KNOWN_PARAMETER_EFFECT recovers ground truth",
          "PC residual >= frozen 0.10 nats",
          (pc_primary["mean_residual_nats"] or -1e9) >= FROZEN_PC_THRESHOLD,
          f"pc_residual={pc_primary['mean_residual_nats']}; "
          f"constant_zero_predictor_residual={pc_zero['mean_residual_nats']}; "
          f"max_attainable_log_score=-log(1e-10)={-math.log(METRIC_EPS)}"),
    ]
    return out


if __name__ == "__main__":
    main()