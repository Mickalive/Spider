#!/usr/bin/env python3
"""Finalize EXP-PHYSICS-37385620138 (EXECUTE stage).

Reads the frozen inputs and the derived analysis artifacts and emits the three
stage-output files required by research/EXPERIMENT_PACKET.md:

    result.json       schema_version/experiment_id/lane/status/outcome/metrics/
                      controls/artifacts/observations/validity_notes/unresolved
    report.md         narrative, must not contradict result.json
    provenance.json   reproducibility context

Nothing here re-measures anything and nothing here changes a frozen input.  This
script only renders what the collection and analysis stages already wrote.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP_DIR = ROOT / "research" / "experiments" / "EXP-PHYSICS-37385620138"
RAW_DIR = EXP_DIR / "raw"
DERIVED_DIR = EXP_DIR / "derived"
CODE_DIR = ROOT / "research" / "physics"

sys.path.insert(0, str(CODE_DIR))
import exp_37385620138_lib as L  # noqa: E402
import exp_37385620138_analyze as A  # noqa: E402

EXPERIMENT_ID = "EXP-PHYSICS-37385620138"
LANE = "physics"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def git(*args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                             text=True, timeout=30)
        if out.returncode != 0:
            return None
        return out.stdout.strip()
    except Exception:
        return None


def main() -> None:
    # ---- inputs ----------------------------------------------------------
    verification = read_json(RAW_DIR / "frozen_input_verification.json")
    universe = read_json(RAW_DIR / "candidate_universe.json")
    executor_pool = read_json(RAW_DIR / "executor_pool.json")
    truth = read_json(RAW_DIR / "pc_truth.json")
    metrics = read_json(DERIVED_DIR / "metrics.json")
    dec = read_json(DERIVED_DIR / "decision_readings.json")
    gates = read_json(DERIVED_DIR / "validity_gates.json")
    substrate = read_json(DERIVED_DIR / "substrate_diagnostics.json")
    pc = read_json(DERIVED_DIR / "pc_analysis.json")
    predsum = read_json(DERIVED_DIR / "predictions_summary.json")
    null_dist = read_json(DERIVED_DIR / "null_distribution.json")

    mc = dec["measurement_invalid_conditions"]
    ac_all = dec["acceptance_conditions"]

    frozen_pool = metrics["RESIDUAL_EFFECT_SIZE_NATS"]["frozen_pool"]
    explor_pool = metrics["RESIDUAL_EFFECT_SIZE_NATS"]["exploratory_full_screened_pool"]
    pc_resid = metrics["RESIDUAL_EFFECT_SIZE_NATS"]["pc"]
    corr = metrics["RESIDUAL_EFFECT_SIZE_NATS_corrected_distance_variant"]
    ci = metrics["bootstrap_ci95"]
    sb0 = metrics["strong_baseline_SB_DEGENERATE_ZERO"]
    ncs = metrics["null_control_summary"]
    totals = metrics["collection_totals"]
    sec = metrics["secondary_metrics"]
    inert = metrics["inert_rate"]

    pc_corr = pc["corrected_distance_variant"]
    thresh = dec["frozen_threshold_nats"]

    # ---- artifacts -------------------------------------------------------
    artifact_specs = [
        (RAW_DIR / "frozen_input_verification.json", "raw",
         "SHA256 verification of the three frozen inputs against freeze.json"),
        (RAW_DIR / "candidate_universe.json", "raw",
         "executor-constructed seeded candidate (site, document) universe; NOT the "
         "freeze-hashed fixture the prereg named, because no freeze-hashed universe exists"),
        (RAW_DIR / "robots_screen.jsonl", "raw", "per-host robots.txt allow/deny screen"),
        (RAW_DIR / "collection_log.jsonl", "raw",
         "every HTTP request/response actually issued: status, response headers, body "
         "length, body SHA256, structural hash, requested URL, parameter, value, rank"),
        (RAW_DIR / "screen_results.jsonl", "raw",
         "per-candidate admission readings against the frozen C1/C2/C3 screen"),
        (RAW_DIR / "diagnostics.jsonl", "raw",
         "site-dynamism floor (repeat identical fetches) and conditional-GET revalidation probes"),
        (RAW_DIR / "pc_collection_log.jsonl", "raw",
         "every positive-control request/response against the local stdlib server"),
        (RAW_DIR / "pc_truth.json", "raw", "declared positive-control ground truth"),
        (RAW_DIR / "executor_pool.json", "raw",
         "executor-constructed admission outcome; explicitly labelled is_frozen_evidence=false "
         "because frozen_pool.json does not exist"),
        (DERIVED_DIR / "predictions.jsonl", "derived",
         "per-instance held-out predictions of the exploratory full-screened pool"),
        (DERIVED_DIR / "pc_predictions.jsonl", "derived",
         "per-instance positive-control predictions and ground-truth direction"),
        (DERIVED_DIR / "metrics.json", "derived", "primary, secondary and control metrics"),
        (DERIVED_DIR / "predictions_summary.json", "derived",
         "frozen-pool and exploratory pipeline fits, splits, predictor outputs, fallbacks"),
        (DERIVED_DIR / "pc_analysis.json", "derived",
         "positive-control reading under the frozen distance and under the corrected distance"),
        (DERIVED_DIR / "substrate_diagnostics.json", "derived",
         "descriptive substrate facts: parameter response, status histograms, dynamism floor"),
        (DERIVED_DIR / "decision_readings.json", "derived",
         "frozen M1-M6, A1-A6 and F1-F6 condition readings with the branch actually taken"),
        (DERIVED_DIR / "validity_gates.json", "derived", "frozen V1-V10 gate results"),
        (DERIVED_DIR / "null_distribution.json", "derived",
         "NC_PERMUTED_MECHANISM permutation draws for every pool and reading"),
        (CODE_DIR / "exp_37385620138_lib.py", "code", "frozen primitives, predictors, metric"),
        (CODE_DIR / "exp_37385620138_candidates.py", "code", "executor-constructed candidate curation"),
        (CODE_DIR / "exp_37385620138_collect.py", "code", "collection phases 0-5"),
        (CODE_DIR / "exp_37385620138_analyze.py", "code", "derived analysis and gate computation"),
        (CODE_DIR / "exp_37385620138_finalize.py", "code", "renders result.json, report.md, provenance.json"),
        (EXP_DIR / "request.json", "fixture", "frozen request"),
        (EXP_DIR / "spec.json", "fixture", "frozen spec"),
        (EXP_DIR / "prereg.md", "fixture", "frozen preregistration"),
        (EXP_DIR / "freeze.json", "fixture", "frozen hash manifest"),
    ]
    artifacts = []
    for path, role, desc in artifact_specs:
        if not path.exists():
            artifacts.append({"path": rel(path), "sha256": None, "role": role,
                              "description": desc, "exists": False})
            continue
        artifacts.append({"path": rel(path), "sha256": sha256_file(path),
                          "role": role, "description": desc, "exists": True})

    # ---- metrics ---------------------------------------------------------
    metric_block = {
        "RESIDUAL_EFFECT_SIZE_NATS": {
            "definition": metrics["RESIDUAL_EFFECT_SIZE_NATS"]["definition"],
            "units": "nats",
            "frozen_pool": frozen_pool,
            "exploratory_full_screened_pool": explor_pool,
            "pc_known_parameter_effect": pc_resid,
            "frozen_threshold": thresh,
            "admissibility": "NOT_ADMISSIBLE_FOR_CLAIM_INFERENCE: prereg s3 M1, M2 and M3 all hold, "
                             "so the frozen decision branch is MEASUREMENT_INVALID and no value "
                             "here may be read as evidence for or against C-WEB-DYNAMICS",
        },
        "BOOTSTRAP_CI95_SITE_CLUSTERED": {
            "units": "nats",
            "n_resamples": A.N_BOOTSTRAP,
            "frozen_pool": ci["frozen_pool"],
            "exploratory_full_screened_pool": ci["exploratory_full_screened_pool"],
            "pc_known_parameter_effect": ci["pc"],
            "n_clusters_frozen_pool_test": predsum["frozen_pool"]["bootstrap"]["n_clusters"],
            "n_distinct_cluster_resamples_frozen_pool_test":
                predsum["frozen_pool"]["bootstrap"]["n_distinct_cluster_resamples"],
        },
        "RESIDUAL_EFFECT_SIZE_NATS_CORRECTED_DISTANCE_VARIANT": {
            "units": "nats",
            "definition": corr["note"],
            "provenance": "EXECUTOR_ADDED_ROBUSTNESS_VARIANT; not a frozen metric and not "
                          "registered as a replacement for the frozen metric",
            "frozen_pool": corr["frozen_pool"],
            "exploratory_full_screened_pool": corr["exploratory_full_screened_pool"],
            "pc_known_parameter_effect": pc_corr["primary"]["mean_residual_nats"],
        },
        "STRONG_BASELINE_SB_DEGENERATE_ZERO_RESIDUAL": {
            "definition": sb0["definition"],
            "units": "nats",
            "frozen_pool": sb0["frozen_pool"],
            "exploratory_full_screened_pool": sb0["exploratory_full_screened_pool"],
            "pc_known_parameter_effect": sb0["pc"],
            "frozen_pool_corrected_distance": sb0["frozen_pool_corrected_distance"],
            "exploratory_full_screened_pool_corrected_distance":
                sb0["exploratory_full_screened_pool_corrected_distance"],
            "pc_known_parameter_effect_corrected_distance":
                pc_corr["strong_baseline_SB_DEGENERATE_ZERO"]["mean_residual_nats"],
        },
        "RESIDUAL_SIGN_ACCURACY": {
            "exploratory_full_screened_pool": sec["exploratory_full_screened_pool"][
                "RESIDUAL_SIGN_ACCURACY"],
            "frozen_pool": sec["frozen_pool"]["RESIDUAL_SIGN_ACCURACY"],
        },
        "TREATMENT_EXPLAINED_VARIANCE": {
            "exploratory_full_screened_pool": sec["exploratory_full_screened_pool"][
                "TREATMENT_EXPLAINED_VARIANCE"],
            "frozen_pool": sec["frozen_pool"]["TREATMENT_EXPLAINED_VARIANCE"],
            "variance_note": sec["exploratory_full_screened_pool"]["variance_note"],
        },
        "SITE_MEMORY_EXPLAINED_VARIANCE": {
            "exploratory_full_screened_pool": sec["exploratory_full_screened_pool"][
                "SITE_MEMORY_EXPLAINED_VARIANCE"],
            "frozen_pool": sec["frozen_pool"]["SITE_MEMORY_EXPLAINED_VARIANCE"],
        },
        "CACHE_EXPLAINED_VARIANCE": {
            "exploratory_full_screened_pool": sec["exploratory_full_screened_pool"][
                "CACHE_EXPLAINED_VARIANCE"],
            "frozen_pool": sec["frozen_pool"]["CACHE_EXPLAINED_VARIANCE"],
        },
        "COMBINED_EXPLAINED_VARIANCE": {
            "exploratory_full_screened_pool": sec["exploratory_full_screened_pool"][
                "COMBINED_EXPLAINED_VARIANCE"],
            "frozen_pool": sec["frozen_pool"]["COMBINED_EXPLAINED_VARIANCE"],
        },
        "INERT_INTERVENTION_RATE": {
            "definition": "prereg s8.2 inert test ||observed_delta|| < "
                          f"{sec['exploratory_full_screened_pool']['INERT_EPS']}",
            "frozen_distance_reading_frozen_pool": inert["frozen_pool_frozen_distance_reading"],
            "signature_identity_reading_frozen_pool": inert["frozen_pool_signature_identity_reading"],
            "frozen_distance_reading_exploratory_pool":
                inert["exploratory_frozen_distance_reading"],
            "signature_identity_reading_exploratory_pool":
                inert["exploratory_signature_identity_reading"],
            "frozen_ceiling": 0.20,
            "reading_caveat": "the frozen-distance reading cannot discriminate: prereg s6.3 adds "
                              "+0.3 * Jaccard, so an identical signature scores 0.3 and the "
                              "< 0.01 inert test is unreachable under that formula",
        },
        "N_SITES_WITH_ANY_NON_INERT_INTERVENTION": {
            "exploratory_pool": inert["n_sites_with_any_non_inert_intervention"],
            "n_sites_exploratory_pool": inert["n_sites_exploratory"],
            "frozen_pool": dec["acceptance_conditions"]["A5_at_least_15_sites_non_inert"]["observed"],
            "frozen_requirement": dec["acceptance_conditions"]["A5_at_least_15_sites_non_inert"]["required"],
        },
        "COLLECTION_TOTALS": totals,
        "VARIATION_SCREEN": {
            "n_candidates_curated": universe["actual_pairs"],
            "n_e_tld_plus_one_curated": universe["actual_etld1"],
            "n_hosts_curated": universe["actual_hosts"],
            "frozen_target_pairs": universe["frozen_target_pairs"],
            "frozen_target_etld1": universe["frozen_target_etld1"],
            "target_met": (universe["actual_pairs"] >= universe["frozen_target_pairs"]
                           and universe["actual_etld1"] >= universe["frozen_target_etld1"]),
            "source_arm_used": universe["source_arm_used"],
            "source_arms_not_reproducible": universe["source_arms_not_reproducible"],
            "n_candidates_screened": totals["n_candidates_screened"],
            "n_candidates_admitted": totals["n_candidates_admitted"],
            "n_sites_admitted": dec["n_admitted_sites"],
            "screen_failure_counts": substrate["screen_criterion_failures"],
            "frozen_pool_requirement": dec["measurement_invalid_conditions"]["M1_variation_screen_admits_at_least_20_sites"]["required"],
        },
        "PATH_PARAMETER_RESPONSE": {
            "n_path_param_probes": substrate["n_path_param_probes_overall"],
            "n_path_param_probes_2xx_3xx": substrate["n_path_param_probes_2xx_3xx_overall"],
            "frac_2xx_3xx": substrate["n_path_param_probes_2xx_3xx_overall"]
                             / substrate["n_path_param_probes_overall"],
            "path_param_status_histogram": substrate["path_param_status_histogram"],
            "by_mechanism": substrate["parameter_response_by_mechanism"],
        },
        "SITE_DYNAMISM_FLOOR": substrate["repeat_identical_null"],
        "REVALIDATION_AVAILABILITY": substrate["revalidation_availability"],
        "CACHE_REVALIDATION_PREDICTOR_DEGENERACY": {
            "frozen_pool_n_distinct_predictions_on_test":
                predsum["frozen_pool"]["cache_revalidation_prediction_on_test"]["n_distinct_values"],
            "frozen_pool_n_nonzero_on_test":
                predsum["frozen_pool"]["cache_revalidation_prediction_on_test"]["n_nonzero"],
            "exploratory_n_distinct_predictions_on_test":
                predsum["exploratory_full_screened_pool"]["cache_revalidation_prediction_on_test"]["n_distinct_values"],
            "exploratory_n_nonzero_on_test":
                predsum["exploratory_full_screened_pool"]["cache_revalidation_prediction_on_test"]["n_nonzero"],
        },
        "B_SITE_TEMPLATE_MEMORY_FALLBACK_TIERS": metrics["baseline_degeneracy"],
        "SENSITIVITY_ALTERNATIVE_A_PRIORI_PRIOR": metrics[
            "sensitivity_alternative_a_priori_prior"],
        "NC_PERMUTED_MECHANISM_DISTRIBUTION": ncs,
    }

    # ---- controls --------------------------------------------------------
    frozen_train_sites = predsum["frozen_pool"]["split"]["train_sites"]
    frozen_test_sites = predsum["frozen_pool"]["split"]["test_sites"]
    controls = {
        "MECHANISM_CONDITIONED": {
            "role": "treatment",
            "expected": "predicts a response-signature change from the mechanism's declared "
                        "semantic effect and the rank of the bound parameter value; prereg s7.1",
            "observed": {
                "frozen_pool_mean_log_score":
                    predsum["frozen_pool"]["primary"]["mean_log_score_treatment"],
                "exploratory_mean_log_score":
                    predsum["exploratory_full_screened_pool"]["primary"]["mean_log_score_treatment"],
                "pc_mean_log_score": pc["primary"]["mean_log_score_treatment"],
                "n_distinct_predictions_on_exploratory_test":
                    predsum["exploratory_full_screened_pool"]["n_test_instances"],
            },
            "result": "RUN",
            "admissible_as_evidence": False,
            "evidence": ["derived/predictions_summary.json", "derived/pc_analysis.json"],
        },
        "B_CACHE_REVALIDATION": {
            "role": "frozen null baseline, component (i)",
            "expected": "explains the revalidation part of the signature change from the request "
                        "target, the baseline target and cache headers alone, without reading the "
                        "mechanism declaration or bound parameters",
            "observed": {
                "restricted_view": "predict_cache_revalidation receives "
                                   "{url, baseline_url, baseline_signature} only",
                "reads_mechanism_or_parameters": False,
                "n_distinct_predictions_frozen_pool_test":
                    predsum["frozen_pool"]["cache_revalidation_prediction_on_test"]["n_distinct_values"],
                "explained_variance_exploratory_pool":
                    sec["exploratory_full_screened_pool"]["CACHE_EXPLAINED_VARIANCE"],
            },
            "result": "DEGENERATE_ON_FROZEN_POOL",
            "degenerate_detail": "the predictor emitted exactly one value on all "
                                 f"{predsum['frozen_pool']['n_test_instances']} frozen-pool test "
                                 "instances; it carries no per-instance information there, so it "
                                 "cannot be contrasted with the treatment on that pool",
            "admissible_as_evidence": True,
            "evidence": ["derived/predictions_summary.json", "derived/substrate_diagnostics.json"],
        },
        "B_SITE_TEMPLATE_MEMORY": {
            "role": "frozen strong baseline, component (ii)",
            "expected": "explains the change from site and template identity alone, fitted on "
                        "TRAIN rows, keyed on (site, action_template), without reading bound "
                        "parameters",
            "observed": {
                "restricted_view": "predict_site_template_memory receives {site, memory_key} only",
                "reads_mechanism_or_parameters": False,
                "memory_key_form": "site|intervention_type",
                "fallback_tiers_frozen_pool_test":
                    predsum["frozen_pool"]["site_memory_fallback_tiers_on_test"],
                "fallback_tiers_exploratory_test":
                    predsum["exploratory_full_screened_pool"]["site_memory_fallback_tiers_on_test"],
                "n_site_cells_fitted_frozen_pool":
                    predsum["frozen_pool"]["site_memory_model"]["n_site_cells"],
                "explained_variance_exploratory_pool":
                    sec["exploratory_full_screened_pool"]["SITE_MEMORY_EXPLAINED_VARIANCE"],
            },
            "result": "STRUCTURALLY_COLLAPSED_TO_CONSTANT",
            "degenerate_detail": "the split is at site level and the memory key contains the site, "
                                 "so no test site can have a TRAIN cell; on 100% of test instances "
                                 "in both pools the baseline emits one global constant, and the "
                                 "frozen component (ii) vs treatment contrast was never exercised",
            "admissible_as_evidence": True,
            "evidence": ["derived/predictions_summary.json", "derived/metrics.json"],
        },
        "B_COMBINED_NULL": {
            "role": "frozen comparison arm for the primary metric",
            "expected": "per prereg s8.1, the reference prediction against which "
                        "RESIDUAL_EFFECT_SIZE_NATS is measured",
            "observed": {
                "frozen_pool_mean_log_score":
                    predsum["frozen_pool"]["primary"]["mean_log_score_combined"],
                "exploratory_mean_log_score":
                    predsum["exploratory_full_screened_pool"]["primary"]["mean_log_score_combined"],
                "pc_mean_log_score": pc["primary"]["mean_log_score_combined"],
                "effective_prediction_on_test": "a single global constant (the TRAIN mean of "
                                                "observed_delta), because B_SITE_TEMPLATE_MEMORY "
                                                "always fell back to global_mean and B_CACHE_REVALIDATION "
                                                "contributed only where its own non-degenerate "
                                                "condition fired",
            },
            "result": "RUN_EFFECTIVELY_CONSTANT",
            "admissible_as_evidence": True,
            "evidence": ["derived/predictions_summary.json"],
        },
        "SB_DEGENERATE_ZERO": {
            "role": "executor-added strong baseline (the frozen design declares none)",
            "expected": "a predictor that uses no mechanism, no site, no parameter and no data; it "
                        "bounds how much of any reported gain can be attributed to mechanism "
                        "information rather than to the metric's shape",
            "observed": sb0,
            "result": "RUN",
            "admissible_as_evidence": True,
            "rationale_for_adding": "research/AGENTS.md requires strong baselines; the frozen "
                                    "control set contains no trivial-information floor, so the "
                                    "0.05 nats threshold has no stated triviality reference point",
            "evidence": ["derived/metrics.json", "derived/pc_analysis.json"],
        },
        "PC_KNOWN_PARAMETER_EFFECT": {
            "role": "frozen positive control",
            "expected": f"RESIDUAL_EFFECT_SIZE_NATS >= {thresh} nats on a local server whose "
                        "mechanism declarations are true by construction; prereg s9.1",
            "observed": {
                "pc_residual_nats": pc_resid,
                "pc_ci95": pc["bootstrap"]["ci95"],
                "per_mechanism_residual_nats": {
                    k: v["mean_residual_nats"] for k, v in pc["per_mechanism"].items()},
                "ground_truth": truth,
                "n_pc_sites": truth["n_pc_sites"],
                "n_test_sites": pc["split"]["n_test_sites"],
                "n_test_instances": pc["primary"]["n"],
                "prereg_claimed_pilot_pc_nats": 0.18,
                "prereg_claimed_pilot_uncertainty_nats": 0.03,
                "prereg_pilot_artifact_exists": False,
            },
            "result": "FAIL_UNDER_FROZEN_DISTANCE",
            "corrected_distance_variant": {
                "pc_residual_nats": pc_corr["primary"]["mean_residual_nats"],
                "constant_zero_baseline_nats":
                    pc_corr["strong_baseline_SB_DEGENERATE_ZERO"]["mean_residual_nats"],
                "constant_zero_share_of_treatment_gain": (
                    pc_corr["strong_baseline_SB_DEGENERATE_ZERO"]["mean_residual_nats"]
                    / pc_corr["primary"]["mean_residual_nats"]),
                "note": pc_corr["note"],
            },
            "admissible_as_evidence": True,
            "admissible_because": "the positive control's ground truth is known by construction, "
                                  "so a reading against it is a statement about the instrument and "
                                  "does not require any assumption about real sites",
            "evidence": ["derived/pc_analysis.json", "derived/pc_predictions.jsonl",
                         "raw/pc_truth.json", "raw/pc_collection_log.jsonl"],
        },
        "NC_PERMUTED_MECHANISM": {
            "role": "frozen null control",
            "expected": "permute the mechanism declaration within the same intervention_type, "
                        "holding (site, document, instant, intervention_type) fixed; the treatment "
                        "residual must exceed its 95th percentile",
            "observed": ncs["frozen_pool"],
            "result": "NON_DEGENERATE_BUT_CENTRED_ON_THE_TREATMENT",
            "non_degeneracy": {
                "requirement": "> 1 distinct residual value across 1000 permutations",
                "observed": ncs["frozen_pool"]["n_distinct_values"],
                "holds": dec["acceptance_conditions"]["A6_null_non_degenerate"]["holds"],
            },
            "discrimination": {
                "requirement": dec["acceptance_conditions"]["A3_treatment_exceeds_null_p95"]["required"],
                "treatment": frozen_pool,
                "null_p95": ncs["frozen_pool"]["null_p95"],
                "treatment_percentile_within_null":
                    ncs["frozen_pool"]["treatment_percentile_within_null"],
                "holds": dec["acceptance_conditions"]["A3_treatment_exceeds_null_p95"]["holds"],
            },
            "admissible_as_evidence": True,
            "evidence": ["derived/null_distribution.json", "derived/decision_readings.json"],
        },
    }

    # ---- observations ----------------------------------------------------
    obs_dyn = substrate["repeat_identical_null"]
    hist_404_only = substrate["path_param_status_histogram"].get("[404]", 0)
    n_screen = substrate["screen_criterion_failures"]["n_screened"]
    fail = substrate["screen_criterion_failures"]
    anchor = substrate["parameter_response_by_mechanism"]["M_ANCHOR"]
    pag = substrate["parameter_response_by_mechanism"]["M_PAGINATION"]
    secm = substrate["parameter_response_by_mechanism"]["M_SECTION"]
    reval = substrate["revalidation_availability"]

    observations = [
        {"id": "OBS-01", "class": "RAW_EVIDENCE",
         "statement": "All three frozen inputs hash-match freeze.json; master_seed resolves to "
                      f"{verification['master_seed']}.",
         "evidence": ["raw/frozen_input_verification.json", "freeze.json"]},
        {"id": "OBS-02", "class": "RAW_EVIDENCE",
         "statement": "freeze.json hashes exactly prereg.md, request.json and spec.json. "
                      "pilot_data.json, power_calculation.json, candidate_universe.json and "
                      "frozen_pool.json are absent from disk and unhashed.",
         "evidence": ["freeze.json", "derived/decision_readings.json"]},
        {"id": "OBS-03", "class": "OBSERVATION",
         "statement": f"The executor curated {universe['actual_pairs']} (site, document) candidate "
                      f"pairs over {universe['actual_etld1']} eTLD+1 domains and screened "
                      f"{totals['n_candidates_screened']} of them after a robots screen; "
                      f"{totals['n_candidates_admitted']} candidates on {dec['n_admitted_sites']} "
                      "sites were admitted.",
         "evidence": ["raw/candidate_universe.json", "raw/screen_results.jsonl",
                      "derived/substrate_diagnostics.json"]},
        {"id": "OBS-04", "class": "OBSERVATION",
         "statement": f"Of {substrate['n_path_param_probes_overall']} path-parameter probes, "
                      f"{substrate['n_path_param_probes_2xx_3xx_overall']} returned 2xx/3xx "
                      f"({substrate['n_path_param_probes_2xx_3xx_overall'] / substrate['n_path_param_probes_overall']:.4f}). "
                      "The per-candidate status pattern [404] alone occurs "
                      f"{substrate['path_param_status_histogram']['[404]']} times.",
         "evidence": ["raw/screen_results.jsonl", "derived/substrate_diagnostics.json"]},
        {"id": "OBS-05", "class": "OBSERVATION",
         "statement": "Frozen screen criterion failures: C1 "
                      f"{substrate['screen_criterion_failures']['C1_transport_ok']} of "
                      f"{substrate['screen_criterion_failures']['n_screened']}, C2 "
                      f"{substrate['screen_criterion_failures']['C2_identifier_variation']}, C3 "
                      f"{substrate['screen_criterion_failures']['C3_template_variation']}.",
         "evidence": ["derived/substrate_diagnostics.json"]},
        {"id": "OBS-06", "class": "OBSERVATION",
         "statement": f"Conditioned on a probe returning 2xx/3xx, M_ANCHOR produced a "
                      f"byte-identical signature to the baseline in "
                      f"{anchor['frac_2xx_3xx_probes_identical_to_baseline']:.4f} of "
                      f"{anchor['n_2xx_3xx_probes']} cases and the same status in "
                      f"{anchor['frac_2xx_3xx_probes_same_status_as_baseline']:.4f} of them.",
         "evidence": ["raw/collection_log.jsonl", "derived/substrate_diagnostics.json"]},
        {"id": "OBS-07", "class": "OBSERVATION",
         "statement": f"Conditioned on a probe returning 2xx/3xx, M_PAGINATION changed the body at "
                      f"the same status in "
                      f"{1 - pag['frac_2xx_3xx_probes_identical_to_baseline']:.4f} of "
                      f"{pag['n_2xx_3xx_probes']} cases.",
         "evidence": ["raw/collection_log.jsonl", "derived/substrate_diagnostics.json"]},
        {"id": "OBS-08", "class": "OBSERVATION",
         "statement": f"M_SECTION returned 2xx/3xx in only "
                      f"{secm['frac_2xx_3xx']:.4f} of its {secm['n']} probes; its overall signature "
                      f"variation fraction of {secm['frac_signature_identical']:.4f} identical is "
                      "dominated by 404-versus-200 status differences rather than by section "
                      "selection.",
         "evidence": ["raw/collection_log.jsonl", "derived/substrate_diagnostics.json"]},
        {"id": "OBS-09", "class": "OBSERVATION",
         "statement": f"Repeat-identical probes: "
                      f"{obs_dyn['n_repeat_fetches_byte_identical_to_baseline']} of "
                      f"{obs_dyn['n_repeat_fetches']} repeat fetches of an unchanged URL were "
                      f"byte-identical to the original "
                      f"({obs_dyn['frac_repeat_fetches_byte_identical']:.4f}); "
                      f"{obs_dyn['n_candidates_with_any_repeat_variation']} of "
                      f"{obs_dyn['n_candidates_probed']} candidates varied on at least one repeat.",
         "evidence": ["raw/diagnostics.jsonl", "derived/substrate_diagnostics.json"]},
        {"id": "OBS-10", "class": "OBSERVATION",
         "statement": f"{reval['n_returning_304']} of {reval['n_conditional_get_probes']} "
                      f"conditional GETs returned 304 ({reval['frac_returning_304']:.4f}); "
                      f"{reval['n_returning_200']} returned 200. The frozen collection protocol "
                      "issues no conditional requests, so none of these probes are part of any "
                      "frozen metric.",
         "evidence": ["raw/diagnostics.jsonl", "derived/substrate_diagnostics.json"]},
        {"id": "OBS-11", "class": "OBSERVATION",
         "statement": f"B_CACHE_REVALIDATION emitted exactly "
                      f"{predsum['frozen_pool']['cache_revalidation_prediction_on_test']['n_distinct_values']} distinct value on "
                      f"all {predsum['frozen_pool']['n_test_instances']} frozen-pool test instances; "
                      f"on the exploratory test set it emitted "
                      f"{predsum['exploratory_full_screened_pool']['cache_revalidation_prediction_on_test']['n_distinct_values']} "
                      "distinct values, "
                      f"{predsum['exploratory_full_screened_pool']['cache_revalidation_prediction_on_test']['n_nonzero']} "
                      "of which were non-zero.",
         "evidence": ["derived/predictions_summary.json"]},
        {"id": "OBS-12", "class": "OBSERVATION",
         "statement": f"B_SITE_TEMPLATE_MEMORY fell back to "
                      f"{list(predsum['frozen_pool']['site_memory_fallback_tiers_on_test'])[0]} on "
                      f"{predsum['frozen_pool']['site_memory_fallback_tiers_on_test']['global_mean']} "
                      f"of {predsum['frozen_pool']['n_test_instances']} frozen-pool test instances "
                      f"and on "
                      f"{predsum['exploratory_full_screened_pool']['site_memory_fallback_tiers_on_test']['global_mean']} "
                      f"of {predsum['exploratory_full_screened_pool']['n_test_instances']} "
                      "exploratory test instances.",
         "evidence": ["derived/predictions_summary.json"]},
        {"id": "OBS-13", "class": "DERIVED_MEASUREMENT",
         "statement": f"RESIDUAL_EFFECT_SIZE_NATS on the admitted frozen pool = {frozen_pool:.6f} "
                      f"nats over {predsum['frozen_pool']['n_test_instances']} held-out instances from "
                      f"{len(frozen_test_sites)} test sites (train sites {len(frozen_train_sites)}); "
                      f"site-clustered bootstrap CI95 {ci['frozen_pool']} from "
                      f"{predsum['frozen_pool']['bootstrap']['n_clusters']} clusters and "
                      f"{predsum['frozen_pool']['bootstrap']['n_distinct_cluster_resamples']} distinct "
                      "cluster resamples.",
         "evidence": ["derived/metrics.json", "derived/predictions_summary.json"]},
        {"id": "OBS-14", "class": "DERIVED_MEASUREMENT",
         "statement": f"RESIDUAL_EFFECT_SIZE_NATS on the full screened pool = {explor_pool:.6f} nats "
                      f"over {predsum['exploratory_full_screened_pool']['n_test_instances']} held-out "
                      f"instances from "
                      f"{predsum['exploratory_full_screened_pool']['split']['n_test_sites']} test "
                      f"sites; CI95 {ci['exploratory_full_screened_pool']}.",
         "evidence": ["derived/metrics.json"]},
        {"id": "OBS-15", "class": "DERIVED_MEASUREMENT",
         "statement": f"PC_KNOWN_PARAMETER_EFFECT residual = {pc_resid:.6f} nats over "
                      f"{pc['primary']['n']} held-out instances from {pc['split']['n_test_sites']} "
                      f"pseudo-sites; per-mechanism residuals "
                      + ", ".join(f"{k}={v['mean_residual_nats']:.4f}"
                                  for k, v in pc["per_mechanism"].items()) + ".",
         "evidence": ["derived/pc_analysis.json", "derived/pc_predictions.jsonl"]},
        {"id": "OBS-16", "class": "DERIVED_MEASUREMENT",
         "statement": "Under the corrected distance, the same positive control with the same "
                      f"ground truth and the same predictors gives "
                      f"{pc_corr['primary']['mean_residual_nats']:.6f} nats for the treatment and "
                      f"{pc_corr['strong_baseline_SB_DEGENERATE_ZERO']['mean_residual_nats']:.6f} "
                      "nats for SB_DEGENERATE_ZERO.",
         "evidence": ["derived/pc_analysis.json"]},
        {"id": "OBS-17", "class": "OBSERVATION",
         "statement": "On the positive control the observed signature distance takes at most two "
                      "distinct values across the five parameter ranks for M_PAGINATION and exactly "
                      "one for M_SECTION, while MECHANISM_CONDITIONED emits five distinct "
                      "rank-ordered values for both.",
         "evidence": ["derived/pc_predictions.jsonl"]},
        {"id": "OBS-18", "class": "OBSERVATION",
         "statement": "All 20 positive-control pseudo-sites are behaviourally identical, so the "
                      "site-clustered bootstrap over its 6 test clusters returns a zero-width CI "
                      f"{pc['bootstrap']['ci95']}.",
         "evidence": ["derived/pc_analysis.json", "raw/pc_collection_log.jsonl"]},
        {"id": "OBS-19", "class": "DERIVED_MEASUREMENT",
         "statement": f"NC_PERMUTED_MECHANISM produced "
                      f"{ncs['frozen_pool']['n_distinct_values']} distinct residual values over "
                      f"{ncs['frozen_pool']['n_permutations']} permutations "
                      f"(non-degenerate), with null mean "
                      f"{ncs['frozen_pool']['null_mean']:.6f} and null p95 "
                      f"{ncs['frozen_pool']['null_p95']:.6f}; the treatment residual sits at "
                      f"percentile {ncs['frozen_pool']['treatment_percentile_within_null']}.",
         "evidence": ["derived/null_distribution.json", "derived/decision_readings.json"]},
        {"id": "OBS-20", "class": "OBSERVATION",
         "statement": "The frozen inert test ||observed_delta|| < 0.01 cannot be satisfied under "
                      "the frozen distance formula, because prereg s6.3 adds +0.3 * Jaccard so an "
                      "identical signature scores 0.3. Measured inert rates are "
                      f"{inert['frozen_pool_frozen_distance_reading']:.4f} (frozen-distance "
                      f"reading) and "
                      f"{inert['frozen_pool_TEST_signature_identity_reading']:.4f} "
                      "(signature-identity reading) on the frozen pool's held-out test set of "
                      f"{inert['n_frozen_pool_TEST_instances']} instances.",
         "evidence": ["derived/metrics.json", "prereg.md"]},
        {"id": "OBS-21", "class": "OBSERVATION",
         "statement": f"TREATMENT_EXPLAINED_VARIANCE on the exploratory pool is "
                      f"{sec['exploratory_full_screened_pool']['TREATMENT_EXPLAINED_VARIANCE']:.6f} "
                      f"while SITE_MEMORY_EXPLAINED_VARIANCE is "
                      f"{sec['exploratory_full_screened_pool']['SITE_MEMORY_EXPLAINED_VARIANCE']:.6f}; "
                      f"RESIDUAL_SIGN_ACCURACY is "
                      f"{sec['exploratory_full_screened_pool']['RESIDUAL_SIGN_ACCURACY']:.4f}.",
         "evidence": ["derived/metrics.json"]},
        {"id": "OBS-22", "class": "OBSERVATION",
         "statement": "All 2,896 collection requests returned a transport-level response "
                      f"({totals['n_transport_errors']} transport errors); status distribution "
                      f"{totals['n_status_2xx']} 2xx, {totals['n_status_3xx']} 3xx, "
                      f"{totals['n_status_4xx']} 4xx, {totals['n_status_5xx']} 5xx.",
         "evidence": ["raw/collection_log.jsonl", "derived/metrics.json"]},
        {"id": "OBS-23", "class": "DERIVED_MEASUREMENT",
         "statement": f"Frozen condition readings: M1={mc['M1_variation_screen_admits_at_least_20_sites']['holds']}, "
                      f"M2={mc['M2_pilot_and_power_artifacts_present_at_freeze']['holds']}, "
                      f"M3={mc['M3_frozen_pool_hashed_into_freeze_json']['holds']}, "
                      f"M4={mc['M4_inert_rate_at_most_20pct']['holds']} (not decidable), "
                      f"M5={mc['M5_cache_predictor_free_of_mechanism_declaration']['holds']}, "
                      f"M6={mc['M6_site_memory_predictor_free_of_bound_parameters']['holds']}. "
                      f"A1={dec['acceptance_conditions']['A1_primary_metric_above_threshold']['holds']}, "
                      f"A2={dec['acceptance_conditions']['A2_ci95_lower_above_zero']['holds']}, "
                      f"A3={dec['acceptance_conditions']['A3_treatment_exceeds_null_p95']['holds']}, "
                      f"A4={dec['acceptance_conditions']['A4_pc_recovers_ground_truth']['holds']}, "
                      f"A5={dec['acceptance_conditions']['A5_at_least_15_sites_non_inert']['holds']}, "
                      f"A6={dec['acceptance_conditions']['A6_null_non_degenerate']['holds']}.",
         "evidence": ["derived/decision_readings.json"]},
        {"id": "OBS-24", "class": "OBSERVATION",
         "statement": f"Validity gates: "
                      + ", ".join(f"{g['gate'].split('_')[0]}={g['result']}" for g in gates)
                      + ".",
         "evidence": ["derived/validity_gates.json"]},
    ]

    # ---- validity notes --------------------------------------------------
    validity_notes = [
        "STATUS MEANING. status=MEASUREMENT_INVALID and outcome=NOT_APPLICABLE are used because "
        "prereg s3 makes the experiment MEASUREMENT_INVALID if ANY of M1..M6 holds and no "
        "inference is then permitted in either direction. M1 (fewer than 20 admitted sites; 6), "
        "M2 (pilot_data.json and power_calculation.json absent and unhashed) and M3 "
        "(frozen_pool.json absent and unhashed) all hold. This is not an infrastructure failure: "
        "the collection and analysis stages completed and every request/response is archived.",

        "NOT A SCIENTIFIC NEGATIVE. Nothing in this run may be read as evidence that "
        "C-WEB-DYNAMICS is false, or that interactive Web transformations contain no "
        "mechanism-semantic structure. The frozen decision rule forbids the inference because the "
        "measurement apparatus did not meet its own admission and pre-registration conditions.",

        "ALTERNATIVE BRANCH READING RECORDED, NOT ADOPTED. prereg F3, F4 and F5 also hold, so an "
        "alternative precedence that evaluated the falsification branch first would read "
        "FALSIFIES. That reading is recorded in derived/decision_readings.json and not adopted, "
        "because the same condition set shows the accept branch is unreachable and two instruments "
        "are themselves defective; research/EXPERIMENT_PACKET.md s1 forbids recording a statement "
        "about the instrument as scientific falsification. The lane Director owns this precedence "
        "choice.",

        "REPRESENTATION LOSS, BODIES NOT ARCHIVED. prereg s14 describes raw/collection_log.jsonl as "
        "carrying the response body. Each response is archived as status, full response headers, "
        "body length, body SHA256 and a structural hash, but not the body bytes. Structural hashes "
        "and body hashes are therefore not recomputable from the packet alone; any re-derivation "
        "requires a fresh fetch, which the substrate is not guaranteed to permit. prereg V5 is "
        "satisfied in its own wording ('raw responses archived; losses documented') with this loss "
        "documented, but the artifact-table wording is not fully met.",

        "REPRESENTATION LOSS, STRUCTURAL HASH IS A SUMMARY. The structural component is a hash of "
        "the HTML tag skeleton, not the rendered document, not the DOM after scripts, and not the "
        "visual layout. Any mechanism whose declared effect is visual or client-side is invisible "
        "to it by construction.",

        "INSTRUMENT SCOPE BOUNDARY: NO CLIENT-SIDE LAYER. stdlib HTTP sends no JavaScript, no "
        "cookies and no browser state, and observes no rendering. The frozen mechanism table "
        "declares M_ANCHOR's effect as client-side scrolling, which such a client cannot observe by "
        "definition; only the server-side absence of that effect is measurable. Any mechanism-semantic "
        "component is therefore restricted to server-visible change, which is a subset of the "
        "mechanism's declared semantics.",

        "SUBSTRATE DEVIATION, POSITIVE CONTROL SERVER. prereg s9.1 specifies Flask. Flask is not "
        "installed in this environment, so the positive control is implemented on "
        "http.server.ThreadingHTTPServer with the same endpoints, the same conditional and "
        "validator headers and the same status codes. The request-target semantics under test "
        "(query parameter, path segment, fragment not transmitted) are identical, so this "
        "deviation does not touch the mechanism being measured; it is recorded anyway.",

        "SUBSTRATE DEVIATION, CANDIDATE UNIVERSE IS EXECUTOR-CONSTRUCTED AND NOT REPRODUCIBLE FROM "
        "THE PACKET. prereg s10 freezes a candidate universe and prereg s13 hashes a frozen pool "
        "into freeze.json; neither artifact exists. The executor therefore curated "
        f"{universe['actual_pairs']} candidate pairs manually and named the admission outcome "
        "raw/executor_pool.json, which carries is_frozen_evidence=false. Creating a file named "
        "frozen_pool.json after the fact would have manufactured the appearance of frozen "
        "evidence, so it was deliberately not done.",

        "REPRESENTATION LOSS, no Tranco or Common Crawl arm. The prereg's candidate sourcing arms "
        "beyond manual curation could not be reproduced, so the screened pool is a curated sample "
        "of public HTML documents and is not a probability sample of the Web. Rate-style "
        "quantities in this packet describe this curated pool only.",

        "MEASUREMENT INSTRUMENT DEFECT, FROZEN DISTANCE IS NOT A METRIC. prereg s6.3 uses "
        "+0.3 * Jaccard(cache_headers) where a distance requires 0.3 * (1 - Jaccard). As written "
        "the term increases with header similarity, an identical signature scores exactly 0.3, and "
        "the prereg s8.2 inert test ||delta|| < 0.01 is unreachable. This defect is a property of "
        "the frozen specification, was not introduced by the executor, and is quantified in "
        "OBS-20, OBS-17 and the corrected-distance variant metrics.",

        "MEASUREMENT INSTRUMENT DEFECT, the frozen strong baseline cannot be exercised. "
        "B_SITE_TEMPLATE_MEMORY is keyed on (site, action_template) while the split is at site "
        "level, so no test site can own a TRAIN memory cell. The frozen contrast between "
        "component (ii) and the treatment therefore reduces to the treatment versus one global "
        "constant. See OBS-12.",

        "MEASUREMENT INSTRUMENT DEFECT, the frozen null cannot discriminate. "
        "NC_PERMUTED_MECHANISM permutes mechanism declarations within an intervention_type, and "
        "each frozen intervention_type contains exactly one mechanism, so a permutation only "
        "reassigns which instance receives which parameter rank. Its null mean "
        f"({ncs['frozen_pool']['null_mean']:.6f}) is consequently near the treatment "
        f"({frozen_pool:.6f}). The null is non-degenerate as required but is structurally incapable "
        "of separating the mechanism declaration from a random rank alignment. See OBS-19.",

        "POWER. The frozen-pool CI95 rests on "
        f"{predsum['frozen_pool']['bootstrap']['n_clusters']} site clusters with "
        f"{predsum['frozen_pool']['bootstrap']['n_distinct_cluster_resamples']} distinct resamples, "
        "far below the frozen assumption of 20 sites. No power claim is made from it. The "
        "exploratory CI95 rests on "
        f"{predsum['exploratory_full_screened_pool']['bootstrap']['n_clusters']} clusters.",

        "VALIDITY GATES. V6, V7, V8 and V10 FAIL. V4 passes by construction (10,000 site-clustered "
        "resamples, no noise injection) but is not informative at two clusters. V5 passes with the "
        "documented body loss above. V8 FAILS on the held-out test set: the signature-identity "
        f"reading is {inert['frozen_pool_TEST_signature_identity_reading']:.4f} and the "
        f"corrected-distance reading is "
        f"{inert['frozen_pool_TEST_corrected_distance_reading']:.4f}, both above the 0.20 ceiling; "
        "only the frozen-distance reading passes, and that reading is vacuous per OBS-20.",

        "UNVERIFIABLE FROZEN CLAIM, threshold attainability. spec.json asserts a pilot range of "
        "[0.02, 0.15] nats and prereg s9.1 asserts a positive-control pilot of 0.18 +/- 0.03 "
        "nats. No pilot_data.json exists, so neither claim can be checked against its own artifact; "
        "the measured positive-control reading is "
        f"{pc_resid:.6f} +/- 0.000000 nats, which does not contain the asserted value.",

        "SEEDS AND DETERMINISM. master_seed = "
        f"{verification['master_seed']} = int(request_hash[:8], 16); bootstrap and permutation "
        "seeds are derived from it. The analysis stage is deterministic and re-runnable; the "
        "collection stage is not, because the public Web is not frozen.",

        "EXECUTOR-ADDED MATERIAL IS LABELLED AS SUCH. Three items are not in the frozen design "
        "and are labelled in the metric ids and in controls: SB_DEGENERATE_ZERO (a strong "
        "triviality floor, absent from the frozen control set), the corrected-distance robustness "
        "variant, and the descriptive substrate diagnostics. None of them replaces or overrides a "
        "frozen quantity.",

        "SCOPE COMPLIANCE. All executor code is under research/physics, an allowed code root for "
        "the physics lane in research/lanes/registry.json; research/harness does not exist. "
        "SPIDER_CODEX.md and all constitutional files are unmodified. No frozen input was edited; "
        "the three frozen hashes still match. No commit, push, branch switch or reset was "
        "performed.",

        "ARTIFACT NAME DEVIATIONS against prereg s14. derived/bootstrap_cis.json was not produced "
        "separately; bootstrap CIs are inside derived/metrics.json under "
        "BOOTSTRAP_CI95_SITE_CLUSTERED. raw/frozen_pool.json was not produced at all, by design, "
        "because the frozen pool never existed; raw/executor_pool.json records the executor's "
        "admission outcome instead. pilot_data.json and power_calculation.json were pre-freeze "
        "requirements and are correctly absent from an execution stage.",
    ]

    # ---- unresolved ------------------------------------------------------
    unresolved = [
        "Whether any prereg artifact other than the three hashed files (pilot_data.json, "
        "power_calculation.json, frozen_pool.json, candidate_universe.json) existed at freeze time "
        "and was lost, or was never produced. The freeze manifest cannot distinguish these.",

        "What RESIDUAL_EFFECT_SIZE_NATS would be for C-WEB-DYNAMICS under a distance that is "
        "actually a distance and a strong baseline that can be exercised. This run cannot answer "
        "it: the frozen branch forbids inference, and the corrected-distance variant was measured "
        "on a pool selected by a frozen screen whose C1 criterion is near-unreachable on public "
        "HTML documents.",

        "Whether the pagination body variation measured in OBS-07 is caused by the bound parameter "
        "or by the site-dynamism floor of OBS-09. 25.5% of successful same-status body changes "
        f"versus a {obs_dyn['frac_repeat_fetches_byte_identical']:.4f} byte-identical repeat rate "
        "is suggestive but not separated: no frozen arm fixes the parameter and varies only the "
        "instant with the same host, and the executor did not add one.",

        "Whether the query-parameter variation that does exist on public HTML documents is "
        "mechanism-semantic or merely template rotation, which is exactly the discrimination the "
        "frozen B_SITE_TEMPLATE_MEMORY arm was designed to make and could not make because it "
        "collapsed to a constant (OBS-12).",

        "Whether the frozen C1 admission criterion is achievable at all on credential-free public "
        "HTML documents. OBS-04 shows path-parameter probes return 2xx/3xx in 7.8% of cases, and "
        "C1 requires at least two of five path values to succeed; this run cannot distinguish "
        "'no public HTML document has path-parameterized content' from 'the criterion is too "
        "strict'.",

        "The correct precedence between the prereg s3 MEASUREMENT_INVALID branch and the F1..F6 "
        "falsification branch when both sets of conditions hold. The Director owns this choice; "
        "both readings are recorded in derived/decision_readings.json.",

        "Whether the corrected distance is the only admissible repair. The executor measured one "
        "repair; it did not establish that 0.3 * (1 - Jaccard) is correct rather than merely "
        "better than the frozen form, and it did not test any distance that separates mechanism "
        "semantics from template rotation.",

        "Whether revalidation responses, available on 73.75% of the credential-free probes in "
        "OBS-10, carry mechanism-distinguishable information. The frozen design never issued a "
        "conditional request inside any metric, so this is unmeasured rather than null.",
    ]

    # ---- write result.json ----------------------------------------------
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": "MEASUREMENT_INVALID",
        "outcome": "NOT_APPLICABLE",
        "claim": {
            "claim_id": "C-WEB-DYNAMICS",
            "registry_status_before_this_run": "HYPOTHESIS",
            "what_was_attempted": "frozen interventional effect-factorization of response-signature "
                                  "change into cache/revalidation semantics, site/template memory, "
                                  "and a mechanism-semantic residual",
            "claim_disposition": "UNCHANGED. This run produces no admissible evidence for or "
                                 "against the claim and does not update its registry status. The "
                                 "producer does not promote, demote or supersede anything.",
        },
        "decision_rule_application": {
            "frozen_branch_rule": dec["frozen_branch_rule"],
            "branch_taken": "MEASUREMENT_INVALID",
            "measurement_invalid_conditions": dec["measurement_invalid_conditions"],
            "acceptance_conditions": dec["acceptance_conditions"],
            "falsification_conditions_F1_to_F6": dec["falsification_conditions_F1_to_F6"],
            "any_acceptance_condition_false": dec["any_acceptance_condition_false"],
            "any_invalid_condition_true": dec["any_invalid_condition_true"],
            "alternative_precedence_reading": dec["alternative_precedence_reading"],
        },
        "validity_gates": gates,
        "metrics": metric_block,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    (EXP_DIR / "result.json").write_text(json.dumps(result, indent=2) + "\n")

    # ---- write provenance.json ------------------------------------------
    provenance = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "stage": "EXECUTE",
        "github": {
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "workflow_sha_env": os.environ.get("GITHUB_SHA"),
            "head_commit": git("rev-parse", "HEAD"),
            "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "remote": git("config", "--get", "remote.origin.url"),
            "note": "No commit, push, branch switch or reset was performed by this stage. All new "
                    "files are untracked working-tree files under the granted scope.",
        },
        "frozen_inputs": {
            "freeze_manifest": {
                "path": rel(EXP_DIR / "freeze.json"),
                "sha256": sha256_file(EXP_DIR / "freeze.json"),
            },
            "verification": verification,
            "immutability": "the three frozen inputs were read only; their hashes still match "
                            "freeze.json after execution",
        },
        "seeds": {
            "request_hash": verification.get("request_hash"),
            "master_seed": verification["master_seed"],
            "master_seed_derivation": "int(request_hash[:8], 16)",
            "bootstrap_seed_offsets": {"primary": 17, "permutations": 31},
            "n_bootstrap_resamples": A.N_BOOTSTRAP,
            "n_permutations": A.N_PERMUTATIONS,
            "freeze_time": verification.get("freeze_time"),
        },
        "environment": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "third_party_packages_used": [],
            "third_party_packages_unavailable": ["numpy", "scipy", "flask", "requests",
                                                 "beautifulsoup4", "pandas"],
            "standard_library_only": True,
            "positive_control_server": "http.server.ThreadingHTTPServer on 127.0.0.1 (prereg "
                                       "s9.1 specifies Flask, which is not installed)",
            "network_access": "outbound HTTPS to public sites succeeded; "
                              f"{totals['n_transport_errors']} transport errors over "
                              f"{totals['n_requests_archived']} archived collection requests",
            "client": "stdlib urllib; no browser, no JavaScript execution, no cookies, no credentials",
        },
        "code": [
            {"path": rel(CODE_DIR / "exp_37385620138_lib.py"),
             "sha256": sha256_file(CODE_DIR / "exp_37385620138_lib.py"),
             "role": "frozen primitives: signature, distance, log_score, four predictors, "
                     "site-clustered bootstrap, permuted-mechanism null, freeze verification"},
            {"path": rel(CODE_DIR / "exp_37385620138_candidates.py"),
             "sha256": sha256_file(CODE_DIR / "exp_37385620138_candidates.py"),
             "role": "executor-constructed candidate curation (not a frozen fixture)"},
            {"path": rel(CODE_DIR / "exp_37385620138_collect.py"),
             "sha256": sha256_file(CODE_DIR / "exp_37385620138_collect.py"),
             "role": "collection phases 0-5: freeze verification, seeded universe, robots screen, "
                     "baseline plus 15 probes per candidate, substrate diagnostics, positive control"},
            {"path": rel(CODE_DIR / "exp_37385620138_analyze.py"),
             "sha256": sha256_file(CODE_DIR / "exp_37385620138_analyze.py"),
             "role": "derived analysis: pipelines, controls, bootstrap, null, gates, decision rule"},
            {"path": rel(CODE_DIR / "exp_37385620138_finalize.py"),
             "sha256": sha256_file(CODE_DIR / "exp_37385620138_finalize.py"),
             "role": "renders result.json, report.md and provenance.json from derived artifacts"},
        ],
        "datasets_and_fixtures": {
            "candidate_universe": {
                "path": rel(RAW_DIR / "candidate_universe.json"),
                "role": "executor-constructed, NOT the freeze-hashed fixture named by prereg",
                "frozen": False,
            },
            "frozen_pool": {
                "declared_name": "frozen_pool.json",
                "exists": False,
                "hashed_by_freeze": False,
                "substitute": rel(RAW_DIR / "executor_pool.json"),
                "reason": "manufacturing a file named frozen_pool.json after the freeze would "
                          "create the appearance of pre-registered frozen evidence",
            },
            "pilot_data": {"declared_name": "pilot_data.json", "exists": False,
                           "hashed_by_freeze": False},
            "power_calculation": {"declared_name": "power_calculation.json", "exists": False,
                                  "hashed_by_freeze": False},
            "positive_control_truth": {"path": rel(RAW_DIR / "pc_truth.json"), "frozen": False,
                                       "role": "known ground truth for PC_KNOWN_PARAMETER_EFFECT"},
            "external_sources": [
                {"name": "public HTML documents", "role": "measurement substrate",
                 "frozen": False,
                 "note": "the public Web is not frozen; a rerun may observe different responses, "
                         "which is why every response is archived with status, headers, length, "
                         "body SHA256 and structural hash"},
                {"name": "robots.txt", "role": "access precondition screening", "frozen": False},
            ],
        },
        "commands": [
            {"step": "collect",
             "command": "python3 -u research/physics/exp_37385620138_collect.py",
             "material_because": "one pass performs freeze verification, the seeded universe, the "
                                 "robots screen, all Web collection, the substrate diagnostics "
                                 "and the positive control, and it writes every raw artifact"},
            {"step": "analyze",
             "command": "python3 -u research/physics/exp_37385620138_analyze.py",
             "material_because": "deterministic; all seeds derive from master_seed, so a rerun "
                                 "reproduces every derived number exactly"},
            {"step": "finalize",
             "command": "python3 -u research/physics/exp_37385620138_finalize.py",
             "material_because": "renders the three packet files from derived artifacts"},
        ],
        "artifacts": artifacts,
        "reproducibility": {
            "analysis_deterministic": True,
            "collection_deterministic": False,
            "collection_nondeterminism_sources": [
                "public Web responses may change between runs",
                "HTTP server-side request ordering and edge caching",
                "no frozen candidate universe exists, so the curated pool is fixed only in this "
                "working tree",
            ],
            "recompute_from_packet": "every derived quantity in result.json can be recomputed from "
                                     "the archived raw artifacts plus the four code files; only "
                                     "HTTP response bodies are not archived, so a re-derivation "
                                     "that needs a body requires a fresh fetch",
        },
        "scope_compliance": {
            "allowed_code_roots_from_lane_charter": ["research/harness", "research/physics"],
            "code_written_under": rel(CODE_DIR),
            "artifacts_written_under": rel(EXP_DIR),
            "constitutional_files_modified": [],
            "codex_modified": [],
            "other_lanes_modified": [],
            "frozen_inputs_modified": [],
            "git_operations_performed": [],
        },
        "lineage": {
            "parent_experiment": "EXP-PHYSICS-36314197314",
            "parent_handoff": "research/experiments/EXP-PHYSICS-36314197314/handoff.json",
            "parent_handoff_sha256":
                "a1346a86430ccda146d0c97c32c5624264ea21da409a7083e08a736e37c07f39",
            "parent_claim_status": "HYPOTHESIS",
            "director_mandate": "PIVOT with cognitive_reset=true, "
                                "parent_handoff_disposition=SUPERSEDE",
        },
    }
    (EXP_DIR / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")

    # ---- write report.md -------------------------------------------------
    def f6(x):
        return "n/a" if x is None else f"{x:.6f}"

    def j(x):
        return json.dumps(x)

    m1 = dec["measurement_invalid_conditions"]["M1_variation_screen_admits_at_least_20_sites"]
    m2 = dec["measurement_invalid_conditions"]["M2_pilot_and_power_artifacts_present_at_freeze"]
    m3 = dec["measurement_invalid_conditions"]["M3_frozen_pool_hashed_into_freeze_json"]
    ac = dec["acceptance_conditions"]
    fc = dec["falsification_conditions_F1_to_F6"]
    nc_f = ncs["frozen_pool"]

    n_pairs = universe["actual_pairs"]
    report = f"""# EXP-PHYSICS-37385620138 — EXECUTE report

**Lane:** physics  ·  **Claim under test:** C-WEB-DYNAMICS (registry status before this run:
`HYPOTHESIS`)  ·  **Stage:** EXECUTE

**Disposition: `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`.**
The claim's registry status is unchanged. This run produces no admissible evidence for or
against C-WEB-DYNAMICS. It does produce a large amount of admissible evidence about the frozen
measurement apparatus itself, and that evidence is what the Director and AUDIT should read first.

---

## 1. What was run

The frozen interventional effect-factorization design was executed as written: a frozen
variation-coverage screen over credential-free public HTML documents, a baseline fetch plus 15
parameterised probes per candidate, a frozen four-predictor comparison
(`MECHANISM_CONDITIONED` against `B_COMBINED_NULL`, with `B_CACHE_REVALIDATION` and
`B_SITE_TEMPLATE_MEMORY` as component nulls), a site-clustered bootstrap, the frozen
`NC_PERMUTED_MECHANISM` null, and `PC_KNOWN_PARAMETER_EFFECT` on a local server with known
ground truth.

| | |
|---|---|
| frozen inputs verified | 3 of 3 hash-match `freeze.json`; `master_seed = {verification['master_seed']}` |
| collection requests archived | {totals['n_requests_archived']} ({totals['n_transport_errors']} transport errors) |
| candidates curated / screened / admitted | {n_pairs} / {totals['n_candidates_screened']} / {totals['n_candidates_admitted']} |
| sites admitted | {dec['n_admitted_sites']} (frozen requirement: {m1['required']}) |
| positive control | 20 pseudo-sites, 360 requests, {pc['primary']['n']} held-out instances |
| analysis | deterministic, {A.N_BOOTSTRAP} site-clustered resamples, {A.N_PERMUTATIONS} permutations |

## 2. Why the disposition is MEASUREMENT_INVALID

prereg §3 makes the experiment MEASUREMENT_INVALID if **any** of M1–M6 holds, and permits no
inference in either direction when it does. Three hold, and two of them are structural facts about
the freeze that no amount of good execution could repair.

| condition | required | observed | holds |
|---|---|---|---|
| M1 | {m1['required']} | {m1['observed']} admitted sites | **{m1['holds']}** |
| M2 | pilot_data.json and power_calculation.json present and hashed at freeze | both absent, unhashed | **{m2['holds']}** |
| M3 | frozen pool hashed into freeze.json | `freeze.json` hashes only `prereg.md`, `request.json`, `spec.json`; no `frozen_pool.json` | **{m3['holds']}** |
| M4 | inert rate ≤ 0.20 in test | not decidable as written; the two non-vacuous readings give {inert['frozen_pool_TEST_signature_identity_reading']:.4f} and {inert['frozen_pool_TEST_corrected_distance_reading']:.4f} on the test set (§5.1) | **not decidable** |
| M5 | cache predictor free of mechanism and parameters | structurally enforced | **{mc['M5_cache_predictor_free_of_mechanism_declaration']['holds']}** |
| M6 | site-memory predictor free of bound parameters | structurally enforced | **{mc['M6_site_memory_predictor_free_of_bound_parameters']['holds']}** |

M1 is not a bad-luck screen. Its dominant cause is measured: of
{substrate['n_path_param_probes_overall']} path-parameter probes only
{substrate['n_path_param_probes_2xx_3xx_overall']} returned 2xx/3xx
({substrate['n_path_param_probes_2xx_3xx_overall'] / substrate['n_path_param_probes_overall']:.2%}),
and {hist_404_only} candidates returned 404 for all five
path values. Frozen criterion C1 requires at least 12 of 15 probes to be 2xx/3xx, and since the
other two intervention types can contribute at most 10, that requires at least two of the five
path values to succeed. On credential-free public HTML documents this criterion is close to
unreachable, and C1 is the single largest screen failure
({fail['C1_transport_ok']} of {n_screen}).

## 3. What the frozen numbers are, and why they are not evidence

These are reported for completeness and for audit. Under prereg §3 they carry no inferential
weight.

| quantity | value (nats) |
|---|---|
| `RESIDUAL_EFFECT_SIZE_NATS`, admitted frozen pool | {f6(frozen_pool)}, CI95 {j([round(x, 6) for x in ci['frozen_pool']])} |
| `RESIDUAL_EFFECT_SIZE_NATS`, full screened pool (exploratory) | {f6(explor_pool)}, CI95 {j([round(x, 6) for x in ci['exploratory_full_screened_pool']])} |
| `PC_KNOWN_PARAMETER_EFFECT` | {f6(pc_resid)}, CI95 {j([round(x, 6) for x in pc['bootstrap']['ci95']])} |
| `NC_PERMUTED_MECHANISM` p95 | {f6(nc_f['null_p95'])} (treatment percentile {nc_f['treatment_percentile_within_null']}) |

| acceptance condition | A1 metric > 0.05 | A2 CI lower > 0 | A3 > null p95 | A4 PC recovers | A5 >= 15 sites | A6 null non-degenerate |
|---|---|---|---|---|---|---|
| holds | {ac['A1_primary_metric_above_threshold']['holds']} | {ac['A2_ci95_lower_above_zero']['holds']} | {ac['A3_treatment_exceeds_null_p95']['holds']} | {ac['A4_pc_recovers_ground_truth']['holds']} | {ac['A5_at_least_15_sites_non_inert']['holds']} | {ac['A6_null_non_degenerate']['holds']} |

| falsification condition | F1 <= 0.05 | F2 CI includes 0 | F3 <= null p95 | F4 PC fails | F5 < 15 sites | F6 null degenerate |
|---|---|---|---|---|---|---|
| holds | {fc['F1_primary_at_or_below_threshold']['holds']} | {fc['F2_ci95_includes_zero']['holds']} | {fc['F3_treatment_below_null_p95']['holds']} | {fc['F4_pc_fails_ground_truth_recovery']['holds']} | {fc['F5_fewer_than_15_sites_non_inert']['holds']} | {fc['F6_null_degenerate']['holds']} |

An alternative precedence that evaluated F1–F6 first would read FALSIFIES. That reading is recorded
in `derived/decision_readings.json` and **not adopted**, because the same condition set shows the
accept branch is unreachable and two instruments are themselves defective; the packet contract
forbids recording a statement about the instrument as scientific falsification. The Director owns
this precedence choice.

## 4. Substrate facts that are admissible regardless of disposition

These are direct observations of credential-free public HTML documents, not claims about mechanism
semantics. Each is bounded to the curated pool and to a single collection window.

* **Fragment interventions are inert as HTTP requires.** Conditioned on a 2xx/3xx response,
  `M_ANCHOR` returned a byte-identical signature at the same status in
  {anchor['frac_2xx_3xx_probes_identical_to_baseline']:.1%} of {anchor['n_2xx_3xx_probes']} cases.
  Fragments are not transmitted in a request target, so the frozen mechanism's declared effect
  (client-side scrolling) is **definitionally unobservable** by a stdlib HTTP client.
* **Query parameters do produce body variation, above the measured noise floor.** Conditioned on a
  2xx/3xx response, `M_PAGINATION` changed the body at the same status in
  {1 - pag['frac_2xx_3xx_probes_identical_to_baseline']:.1%} of {pag['n_2xx_3xx_probes']} cases,
  against a repeat-identical rate of
  {obs_dyn['frac_repeat_fetches_byte_identical']:.1%}
  ({obs_dyn['n_repeat_fetches_byte_identical_to_baseline']}/{obs_dyn['n_repeat_fetches']} repeat
  fetches of an unchanged URL were byte-identical). This is the first positive, bounded substrate
  result in this lineage and it contradicts the inherited expectation that public HTML documents
  show no per-identifier variation.
* **Path parameters are mostly absent, and their absence shows up as 404.** `M_SECTION` returned
  2xx/3xx in only {secm['frac_2xx_3xx']:.1%} of probes. Its apparent signature variation is
  dominated by 404-versus-200 status changes, which is a transport effect, not section selection.
* **Revalidation responses are available and were never used.** {reval['n_returning_304']} of
  {reval['n_conditional_get_probes']} conditional GETs returned 304 ({reval['frac_returning_304']:.1%}).
  The frozen collection protocol issues no conditional requests, so component (i) — the
  cache/revalidation component the design is built around — is unmeasurable by the frozen design
  even though the substrate supplies it.
* **The site-dynamism floor is low but non-zero.**
  {obs_dyn['n_candidates_with_any_repeat_variation']} of {obs_dyn['n_candidates_probed']}
  candidates changed on at least one repeat fetch, so any signature difference at or below that
  floor cannot be attributed to an intervention.

## 5. The apparatus defects, measured rather than argued

These are the durable outputs of this run. Each is a property of the frozen specification, was
verified directly, and is quantified in `result.json`.

### 5.1 The frozen distance is not a distance

prereg §6.3 uses `+0.3 * Jaccard(cache_headers)` where a distance requires
`0.3 * (1 - Jaccard)`. As written, the term **increases** with header similarity. Consequences,
all measured:

* an identical signature scores exactly `0.3`, so the prereg §8.2 inert test `||delta|| < 0.01`
  can never fire; on the {inert['n_frozen_pool_TEST_instances']}-instance held-out test set the
  frozen reading is {inert['frozen_pool_TEST_frozen_distance_reading']:.4f} while the
  signature-identity reading is
  {inert['frozen_pool_TEST_signature_identity_reading']:.4f} and the corrected reading is
  {inert['frozen_pool_TEST_corrected_distance_reading']:.4f}, both above the 0.20 inert ceiling;
* the positive control's provably inert fragment arm is scored at `0.3`, indistinguishable from a
  real change;
* correcting this one sign moves the positive control from **{f6(pc_resid)} nats** to
  **{f6(pc_corr['primary']['mean_residual_nats'])} nats** — same ground truth, same predictors,
  same server. The distance form alone accounts for the positive-control failure.

### 5.2 The frozen strong baseline cannot be exercised

`B_SITE_TEMPLATE_MEMORY` is keyed on `(site, action_template)` while the split is at site level,
so no test site can own a TRAIN memory cell. It fell back to a global constant on
{predsum['frozen_pool']['site_memory_fallback_tiers_on_test']['global_mean']}/
{predsum['frozen_pool']['n_test_instances']} frozen-pool test instances and
{predsum['exploratory_full_screened_pool']['site_memory_fallback_tiers_on_test']['global_mean']}/
{predsum['exploratory_full_screened_pool']['n_test_instances']} exploratory test instances. The
frozen contrast between component (ii) and the treatment was therefore never tested: the entire
comparison is the treatment against one constant.

### 5.3 The frozen null cannot discriminate

`NC_PERMUTED_MECHANISM` permutes mechanism declarations within an `intervention_type`, and each
frozen `intervention_type` contains exactly one mechanism, so a permutation only reassigns which
instance receives which parameter rank. It is non-degenerate as required
({nc_f['n_distinct_values']} distinct values over {nc_f['n_permutations']} permutations — the
inherited placebo defect is genuinely repaired), but its mean
({f6(nc_f['null_mean'])}) sits on top of the treatment ({f6(frozen_pool)}), placing the treatment
at percentile {nc_f['treatment_percentile_within_null']}. As specified it cannot separate the
mechanism declaration from a random rank alignment.

### 5.4 Rank magnitude is not identifiable from an HTTP signature

The executor added `SB_DEGENERATE_ZERO`, a predictor that uses no mechanism, no site, no parameter
and no data, because the frozen control set contains no triviality floor for the 0.05 nats
threshold.

On the positive control, where the mechanism declarations are true by construction, the observed
signature distance takes **at most two** distinct values across the five parameter ranks for
`M_PAGINATION` and **exactly one** for `M_SECTION`, while `MECHANISM_CONDITIONED` emits five
distinct rank-ordered values for both. A single constant is therefore closer to the truth than the
rank-ordered treatment on two of three mechanisms. Under the corrected distance the same positive
control gives {f6(pc_corr['primary']['mean_residual_nats'])} nats for the treatment and
{f6(pc_corr['strong_baseline_SB_DEGENERATE_ZERO']['mean_residual_nats'])} nats for the
mechanism-free constant — the constant recovers
{pc_corr['strong_baseline_SB_DEGENERATE_ZERO']['mean_residual_nats'] / pc_corr['primary']['mean_residual_nats']:.0%}
of the treatment's gain. On the real Web pools under the corrected distance the ordering reverses
outright: the constant scores
{f6(sb0['exploratory_full_screened_pool_corrected_distance'])} nats against the treatment's
{f6(corr['exploratory_full_screened_pool'])}.

The mechanism declaration predicts *how much* a parameter changed a document. HTTP exposes only
*whether* the signature changed. A magnitude prior over parameter rank has no observable
counterpart — this is a statement about the observable, not about the mechanisms.

### 5.5 Variance inverts the ordering

Under `TREATMENT_EXPLAINED_VARIANCE` the treatment scores
{sec['exploratory_full_screened_pool']['TREATMENT_EXPLAINED_VARIANCE']:.4f} on the exploratory
pool while `SITE_MEMORY_EXPLAINED_VARIANCE` scores
{sec['exploratory_full_screened_pool']['SITE_MEMORY_EXPLAINED_VARIANCE']:.4f}, and
`RESIDUAL_SIGN_ACCURACY` is {sec['exploratory_full_screened_pool']['RESIDUAL_SIGN_ACCURACY']:.4f}.
The frozen log-score metric prefers the treatment only because it is singular at zero error.

## 6. Validity gates

{chr(10).join(f"* **{g['gate']}** — {g['result']}: {g['check']}. Evidence: `{g['evidence']}`" for g in gates)}

V8 **FAILS**. Its frozen-distance reading is vacuous per §5.1 — it reads
{inert['frozen_pool_TEST_frozen_distance_reading']:.4f} on the test set only because an inert
intervention cannot be registered by that formula at all. The two non-vacuous readings on the same
{inert['n_frozen_pool_TEST_instances']}-instance held-out test set are
{inert['frozen_pool_TEST_signature_identity_reading']:.4f} (signature identity) and
{inert['frozen_pool_TEST_corrected_distance_reading']:.4f} (corrected distance), both above the
0.20 ceiling. M4 itself is recorded as **not decidable** rather than as pass or fail, because its
frozen definition cannot discriminate; a strict reading under either non-vacuous definition would
make M4 hold as well.

## 7. What this run does and does not establish

Established, at the stated ceiling:

1. Three preregistered pre-freeze artifacts do not exist and were never hashed. The design's power
   and threshold-attainability claims are unverifiable, and the measured positive control
   ({f6(pc_resid)} ± 0.000000) does not contain the asserted pilot value (0.18 ± 0.03).
2. The frozen distance formula is not a metric, and that single defect accounts for the
   positive-control failure (§5.1).
3. The frozen strong baseline and the frozen null control cannot, as specified, discriminate the
   mechanism-semantics component from a global constant or from a random rank alignment (§5.2,
   §5.3).
4. On credential-free public HTML documents, fragment interventions are inert, query parameters do
   produce body variation above the dynamism floor, path parameters are usually absent, and
   revalidation responses are available but unused (§4).

**Not** established, and explicitly unsafe to assume:

* that C-WEB-DYNAMICS is false, weakly supported, or blocked — this run carries no admissible
  evidence about the claim;
* that the {f6(frozen_pool)} nats figure, or its {f6(corr['frozen_pool'])} corrected-distance
  counterpart, indicates mechanism semantics — on both readings a mechanism-free constant is
  competitive or better;
* that query-parameter variation is mechanism-semantic rather than template rotation — that is
  precisely the discrimination the collapsed `B_SITE_TEMPLATE_MEMORY` arm was designed to make;
* that the {obs_dyn['frac_repeat_fetches_byte_identical']:.1%} dynamism floor licenses attributing
  the {1 - pag['frac_2xx_3xx_probes_identical_to_baseline']:.1%} pagination variation to the bound
  parameter rather than to host dynamism;
* that anything here generalises beyond one curated pool and one collection window, on one
  credential-free stdlib HTTP client with no JavaScript, no cookies and no rendering.

## 8. Smallest next actions that would unblock a real measurement

1. Fix the distance to `0.3 * (1 - Jaccard)` (or another form with `d = 0` iff signatures are
   equal) and re-freeze. This is a one-line specification repair with a measured effect (§5.1).
2. Re-key `B_SITE_TEMPLATE_MEMORY` on `(site, document_template)` fitted across train sites, or
   hold out documents within sites, so the split can actually exercise component (ii) (§5.2).
3. Re-specify `NC_PERMUTED_MECHANISM` to permute across mechanisms *and* intervention types, or
   to permute the declared effect against the bound parameter independently, so the null can
   separate a mechanism declaration from a rank alignment (§5.3).
4. Register a triviality floor (`SB_DEGENERATE_ZERO`) as a required control and make the acceptance
   threshold relative to it, not an absolute 0.05 nats (§5.4).
5. Lower or restructure C1: the ≥12-of-15 criterion requires path-parameterized content that
   credential-free public HTML documents do not expose, and it dominates screen failure (§2).
6. Decide the branch-precedence question in §3 explicitly in the next preregistration.

## 9. Packet contents

`result.json` (this run's structured output), `provenance.json` (reproducibility, hashes,
environment, scope compliance), `raw/` (every request/response, the screen, the diagnostics, the
positive control), `derived/` (predictions, metrics, null distribution, gate and decision
readings), and the four executor code files under `research/physics/`. Artifact paths and SHA256
hashes for all of them are listed in `result.json.artifacts` and `provenance.json.artifacts`.

No frozen input was modified. No commit, push, branch switch or reset was performed.
`SPIDER_CODEX.md` is unmodified.
"""
    (EXP_DIR / "report.md").write_text(report)

    # ---- self-check ------------------------------------------------------
    required_top = ["schema_version", "experiment_id", "lane", "status", "outcome", "metrics",
                    "controls", "artifacts", "observations", "validity_notes", "unresolved"]
    missing = [k for k in required_top if k not in result]
    assert not missing, f"result.json missing mandatory keys: {missing}"
    for k in required_top:
        assert result[k] is not None, f"result.json key {k} is null"
    assert result["schema_version"] == 1
    assert result["experiment_id"] == EXPERIMENT_ID
    assert result["lane"] == LANE
    assert result["status"] in ("COMPLETE", "BLOCKED", "MEASUREMENT_INVALID")
    assert result["outcome"] in ("SUPPORTS", "FALSIFIES", "MIXED", "INCONCLUSIVE",
                                 "NOT_APPLICABLE")
    assert isinstance(result["artifacts"], list) and result["artifacts"]
    assert isinstance(result["observations"], list) and result["observations"]
    assert isinstance(result["validity_notes"], list) and result["validity_notes"]
    assert isinstance(result["unresolved"], list) and result["unresolved"]
    assert result["metrics"] and result["controls"]
    json.loads((EXP_DIR / "result.json").read_text())
    json.loads((EXP_DIR / "provenance.json").read_text())
    assert (EXP_DIR / "report.md").read_text().strip()

    print("FINALIZE_COMPLETE")
    print(json.dumps({
        "status": result["status"],
        "outcome": result["outcome"],
        "n_artifacts": len(result["artifacts"]),
        "n_artifacts_missing": sum(1 for a in result["artifacts"] if not a["exists"]),
        "n_observations": len(result["observations"]),
        "n_controls": len(result["controls"]),
        "n_validity_notes": len(result["validity_notes"]),
        "n_unresolved": len(result["unresolved"]),
        "n_metric_ids": len(result["metrics"]),
    }, indent=2))


if __name__ == "__main__":
    main()
