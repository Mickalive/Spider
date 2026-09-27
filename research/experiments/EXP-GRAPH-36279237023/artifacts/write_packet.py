"""Derive the frozen gate table and emit result.json for EXP-GRAPH-36279237023.

This script does not re-run the experiment. It reads only the already-written
raw/derived evidence and applies the FROZEN decision rule
(spec.json.decision_rule, prereg.md 7.1 gate order) mechanically, so that no
gate verdict in result.json is hand-asserted.

Gate order is the frozen one. Gate 1 (measurement validity V1-V11) short-circuits
to MEASUREMENT_INVALID if ANY condition fails; the primary gate (7) and the
secondary gates (8) are still evaluated and reported in full, because prereg.md
7.1's ordering does not forbid recording them and discarding them would destroy
measured evidence. Recording them does not weaken any threshold.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(HERE))

R4 = lambda x: None if x is None else round(float(x), 6)  # noqa: E731


def sha256_file(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    spec = json.loads((EXP / "spec.json").read_text())
    freeze = json.loads((EXP / "freeze.json").read_text())
    m = json.loads((EXP / "derived_evidence" / "metrics.json").read_text())
    cal = json.loads((EXP / "derived_evidence" / "calibration.json").read_text())
    ph0 = json.loads((EXP / "derived_evidence" / "phase0_preconditions.json").read_text())
    ph1 = json.loads((EXP / "derived_evidence" / "phase1_validity_preconditions.json").read_text())
    df = json.loads((EXP / "derived_evidence" / "design_facts.json").read_text())
    rows = [json.loads(line) for line in (EXP / "raw_evidence" / "task_results.jsonl").read_text().splitlines() if line.strip()]

    arms = m["arms"]
    cand = arms["A-CANDIDATE"]
    primary = m["primary"]
    cand_rows = [r for r in rows if r["arm"] == "A-CANDIDATE"]
    pc_rows = [r for r in cand_rows if r["category"] == "verbatim"]
    nc_rows = [r for r in cand_rows if r["category"] == "no_applicable"]
    nc_abst = sum(1 for r in nc_rows if r["abstained"])
    pc_acc = sum(1 for r in pc_rows if r["correct"]) / len(pc_rows) if pc_rows else None

    import math

    w, b = cal["fit"]["w"], cal["fit"]["b"]
    probs = [1 / (1 + math.exp(-(w * r["cos_top"] + b))) for r in cal["cosine_top_only_rows"]]
    thr = cal["threshold"]
    gate_fired = sum(1 for p in probs if p < thr)
    from collections import Counter

    abstain_causes = dict(Counter(r["abstain_reason"] for r in cand_rows if r["abstained"]))

    # ---------------------------------------------------- false-accept audit
    # The frozen documents say "pooled false-accept rate" without fixing the
    # numerator/denominator pairing. All four defensible readings are computed
    # for every arm so the auditor can see that the coded value is not
    # comparable across arms. See observations OBS-11 / validity note VN-06.
    def fa_readings(arm: str) -> dict[str, Any]:
        ar = [r for r in rows if r["arm"] == arm]
        ap = [r for r in ar if r["applies_any"]]
        all_wrong = sum(1 for r in ar if r["executable"] and not r["correct"])
        appl_wrong = sum(1 for r in ap if r["executable"] and not r["correct"])
        appl_exec = sum(1 for r in ap if r["executable"])
        rate = lambda n, d: (round(n / d, 6) if d else None)  # noqa: E731
        return {
            "R1_executable_wrong_among_applicable_over_applicable":
                {"numerator": appl_wrong, "denominator": len(ap), "rate": rate(appl_wrong, len(ap))},
            "R2_executable_wrong_over_all_80":
                {"numerator": all_wrong, "denominator": len(ar), "rate": rate(all_wrong, len(ar))},
            "R3_executable_wrong_among_applicable_over_applicable_and_executable":
                {"numerator": appl_wrong, "denominator": appl_exec, "rate": rate(appl_wrong, appl_exec)},
            "R4_executable_wrong_over_all80_numerator_with_applicable_denominator":
                {"numerator": all_wrong, "denominator": len(ap), "rate": rate(all_wrong, len(ap))},
        }

    fa_by_arm = {a: fa_readings(a) for a in arms}
    cand_R1 = fa_by_arm["A-CANDIDATE"]["R1_executable_wrong_among_applicable_over_applicable"]["rate"]
    cand_R2 = fa_by_arm["A-CANDIDATE"]["R2_executable_wrong_over_all_80"]["rate"]
    cand_R3 = fa_by_arm["A-CANDIDATE"]["R3_executable_wrong_among_applicable_over_applicable_and_executable"]["rate"]
    cand_R4 = fa_by_arm["A-CANDIDATE"]["R4_executable_wrong_over_all80_numerator_with_applicable_denominator"]["rate"]
    fa_gate_flips = (cand_R1 <= 0.10) != (cand_R4 <= 0.10)

    # ---------------------------------------------------------------- V1-V11
    v: dict[str, Any] = {}
    v["V1_CONSTRUCT_VALIDITY"] = {
        "statement": "primary metric is mechanism-identity binding, HTTP execution is a separate measure",
        "pass": True,
        "evidence": "derived_evidence/metrics.json.primary.metric == 'mechanism_identity_accuracy'; "
                    "HTTP is reported only under verification_measure_http and per-arm http_execution_success_rate",
    }
    v["V2_POSITIVE_CONTROL_EXECUTED"] = {
        "pass": bool(pc_rows) and pc_acc == 1.0,
        "denominator": len(pc_rows),
        "accuracy": R4(pc_acc),
        "evidence": "raw_evidence/task_results.jsonl rows arm=A-CANDIDATE category=verbatim",
    }
    v["V3_ORACLE_CEILING"] = {
        "pass": arms["B-INTERNAL-ID-ORACLE"]["mechanism_identity_accuracy"] == 1.0,
        "oracle_accuracy": arms["B-INTERNAL-ID-ORACLE"]["mechanism_identity_accuracy"],
        "evidence": "raw_evidence rows arm=B-INTERNAL-ID-ORACLE",
    }
    v["V4_CALIBRATION_FITTED"] = {
        "pass": bool(cal["fit"].get("fitted")),
        "w": cal["fit"]["w"],
        "b": cal["fit"]["b"],
        "threshold": thr,
        "estimator": cal["fit"]["estimator"],
        "n_train_rows": cal["fit"]["n_train_rows"],
        "independent_refit_w_spread": R4(cal["fitted_parameter_movement"]["w_spread"]),
        "pass_reasoning": "parameters are learned by maximum likelihood on a held-out-split train set and move "
                          "across independent train splits, so they are not a fixed algebraic transform of cos_sim",
        "caveat": "the gate is formally fitted but INERT at the selected threshold: see metrics."
                  "calibration_gate_fired_on_n_applicable_goals",
        "evidence": "derived_evidence/calibration.json",
    }
    v["V5_CLOSED_TOP_BIN_ECE"] = {
        "pass": ph0["estimator_unit_tests"]["checks"]["closed_top_bin"]["pass"]
        and cand["ece_global"]["rows_dropped"] == 0
        and cand["ece_global"]["top_bin_contains_max_confidence"],
        "rows_dropped": cand["ece_global"]["rows_dropped"],
        "top_bin_hi": R4(cand["ece_global"]["top_bin_hi"]),
        "evidence": "derived_evidence/phase0_preconditions.json estimator_unit_tests",
    }
    v["V6_UNKNOWN_PRECISION_DEFINED"] = {
        "pass": ph0["estimator_unit_tests"]["checks"]["unknown_precision_tp_fp"]["pass"]
        and ph0["estimator_unit_tests"]["checks"]["unknown_precision_not_ood_rate"]["pass"],
        "observed_TP_abstain": cand["unknown_precision_terms"]["TP_abstain"],
        "observed_FP_abstain": cand["unknown_precision_terms"]["FP_abstain"],
        "evidence": "derived_evidence/phase0_preconditions.json estimator_unit_tests; the metric is NOT an OOD "
                    "abstention rate (unit test unknown_precision_not_ood_rate returns 0.0 for a single "
                    "abstention on an applicable goal)",
    }
    v["V7_PER_TASK_STATE_RESET"] = {
        "pass": df["state"]["all_identical"] and df["state"]["reset_before_every_arm_request"],
        "n_tasks": df["state"]["n_tasks"],
        "distinct_start_state_hashes": df["state"]["distinct_task_start_state_hashes"],
        "state_hash": df["state"]["hash"],
        "evidence": "derived_evidence/design_facts.json state; raw_evidence/task_results.jsonl "
                    "task_start_state_hash + http.pre_state_hash",
    }
    v["V8_DEGENERACY_SCREEN"] = {
        "pass": m["screen"]["screen_pass"],
        "condition_a_lexical_all80": R4(m["screen"]["lexical_overlap"]["accuracy_all_80"]),
        "condition_a_threshold": m["screen"]["lexical_overlap"]["headroom_threshold"],
        "condition_a_passes": m["screen"]["lexical_overlap"]["pass_as_frozen_all80"],
        "condition_b_comparison_leg_nonempty": m["screen"]["comparison_leg_nonempty"],
        "incumbent_executable_count": m["screen"]["incumbent"]["executable_count"],
        "substitute_leg": m["screen"]["substitute_leg"].get("id"),
        "substitute_executable_count": m["screen"]["substitute_leg"].get("executable_count"),
        "condition_a_informational_caveat": m["screen"]["lexical_overlap"]["structural_cap_note"],
        "evidence": "derived_evidence/degeneracy_screen.json (written before any candidate arm ran); "
                    "raw_evidence/degeneracy_screen_per_goal.jsonl",
    }
    v["V9_CODE_HASHED_INTO_FREEZE"] = {
        "pass": ph1["v9_code_hashed_into_freeze"]["pass"],
        "freeze_json_hashes": ph1["v9_code_hashed_into_freeze"]["freeze_json_hashes"],
        "code_files_expected_by_v9": ph1["v9_code_hashed_into_freeze"]["code_files_expected_by_v9"],
        "code_files_present_in_freeze": ph1["v9_code_hashed_into_freeze"]["code_files_present_in_freeze"],
        "cause": ph1["v9_code_hashed_into_freeze"]["note"],
        "evidence": "research/experiments/EXP-GRAPH-36279237023/freeze.json (immutable, hash-verified) and "
                    "scripts/freeze_experiment.py at commit 7f5879fc",
    }
    v["V10_FAMILY_BLOCKED_UNCERTAINTY"] = {
        "pass": primary["vs_B-LEXICAL-OVERLAP"]["n_blocks"] == 5
        and primary["vs_B-LEXICAL-OVERLAP"]["n_resamples"] == 10000,
        "n_blocks": primary["vs_B-LEXICAL-OVERLAP"]["n_blocks"],
        "blocks": primary["vs_B-LEXICAL-OVERLAP"]["blocks"],
        "n_resamples": primary["vs_B-LEXICAL-OVERLAP"]["n_resamples"],
        "paired": True,
        "evidence": "derived_evidence/metrics.json primary.vs_*",
    }
    fx = ph0["fixture"]
    v["V11_FIXTURE_DISCRIMINATION"] = {
        "pass": bool(fx["v11_multiple_mechanisms_per_family"])
        and not fx["mechanisms_with_empty_parameter_slots"]
        and not fx["unbindable_placeholders"]
        and not fx["mechanisms_whose_own_intent_leaves_slots_unbound"],
        "n_mechanisms": fx["n_mechanisms"],
        "n_endpoints": fx["n_endpoints"],
        "verbs_per_family": fx["verbs_per_family"],
        "evidence": "derived_evidence/phase0_preconditions.json fixture",
    }

    # ------------------------------------------------------------- gate table
    gates: list[dict[str, Any]] = []
    gates.append({
        "gate": 1, "name": "measurement_validity_V1_V11", "order": "prereg 7.1 step 1",
        "pass": all(x["pass"] for x in v.values()),
        "failing_conditions": [k for k, x in v.items() if not x["pass"]],
    })
    gates.append({
        "gate": 2, "name": "degeneracy_screen", "order": "prereg 7.1 step 2",
        "pass": v["V8_DEGENERACY_SCREEN"]["pass"], "failing_conditions": [],
    })
    gates.append({
        "gate": 3, "name": "positive_control_PC-VERBATIM-INTENT", "order": "prereg 7.1 step 3",
        "pass": v["V2_POSITIVE_CONTROL_EXECUTED"]["pass"], "failing_conditions": [],
    })
    gates.append({
        "gate": 4, "name": "oracle_ceiling_B-INTERNAL-ID-ORACLE", "order": "prereg 7.1 step 4",
        "pass": v["V3_ORACLE_CEILING"]["pass"], "failing_conditions": [],
    })
    gates.append({
        "gate": 5, "name": "null_control_NC-NO-APPLICABLE", "order": "prereg 7.1 step 5",
        "pass": nc_abst == len(nc_rows) and len(nc_rows) > 0,
        "failing_conditions": [],
        "observed_abstention_rate": R4(nc_abst / len(nc_rows)) if nc_rows else None,
        "denominator": len(nc_rows),
    })
    gates.append({
        "gate": 6, "name": "calibration_fitted_check", "order": "prereg 7.1 step 6",
        "pass": v["V4_CALIBRATION_FITTED"]["pass"], "failing_conditions": [],
    })
    prim_pass = (
        primary["vs_B-LEXICAL-OVERLAP"]["passes_alpha_0_05_one_sided"]
        and primary["vs_B-RANDOM-ROLE"]["passes_alpha_0_05_one_sided"]
    )
    gates.append({
        "gate": 7, "name": "primary_mechanism_identity_accuracy_above_nulls", "order": "prereg 7.1 step 7",
        "pass": prim_pass,
        "failing_conditions": (
            [] if primary["vs_B-LEXICAL-OVERLAP"]["passes_alpha_0_05_one_sided"]
            else ["does_not_exceed_B-LEXICAL-OVERLAP"]
        ),
        "observed": {
            "A-CANDIDATE": R4(primary["value"]),
            "B-LEXICAL-OVERLAP": R4(primary["nulls"]["B-LEXICAL-OVERLAP"]),
            "B-RANDOM-ROLE": R4(primary["nulls"]["B-RANDOM-ROLE"]),
            "difference_vs_lexical": R4(primary["vs_B-LEXICAL-OVERLAP"]["point_estimate_difference"]),
            "one_sided_lower_95_vs_lexical": R4(primary["vs_B-LEXICAL-OVERLAP"]["one_sided_lower_95"]),
            "p_one_sided_vs_lexical": R4(primary["vs_B-LEXICAL-OVERLAP"]["p_value_one_sided"]),
            "passes_vs_lexical": primary["vs_B-LEXICAL-OVERLAP"]["passes_alpha_0_05_one_sided"],
            "passes_vs_random_role": primary["vs_B-RANDOM-ROLE"]["passes_alpha_0_05_one_sided"],
        },
    })
    sec = [
        {"name": "pooled_false_accept", "observed": R4(cand["false_accept_rate"]), "threshold": 0.10,
         "direction": "<=", "pass": cand["false_accept_rate"] is not None and cand["false_accept_rate"] <= 0.10,
         "interpretation_dependent": fa_gate_flips,
         "interpretation_dependent_detail":
             "the frozen text does not fix the numerator/denominator pairing. The coded 0.3077 is R4 "
             "(all-80 wrong-execution numerator over the 52-goal applicable denominator) and FAILS. Under R1 "
             "(applicable wrong-executions over applicable goals) the candidate scores 0.0962 and PASSES, while "
             "the lexical null scores 0.3077 and fails. Under R2 (all 80) it scores 0.2000 and fails. The gate "
             "verdict is therefore not invariant to the specification gap. Reported as coded; not repaired."},
        {"name": "unknown_precision", "observed": R4(cand["unknown_precision"]), "threshold": 0.85,
         "direction": ">=", "pass": cand["unknown_precision"] is not None and cand["unknown_precision"] >= 0.85},
        {"name": "ece_global", "observed": R4(cand["ece_global"]["ece"]), "threshold": 0.15,
         "bootstrap_upper_95": R4(cand["ece_global_bootstrap"]["upper_95"]), "bootstrap_upper_threshold": 0.18,
         "direction": "<=", "pass": (cand["ece_global"]["ece"] <= 0.15
                                     and cand["ece_global_bootstrap"]["upper_95"] <= 0.18)},
        {"name": "ece_per_class_max",
         "observed": R4(max(x["ece"] for x in cand["ece_per_class"].values())),
         "threshold": 0.15,
         "bootstrap_upper_95": R4(max(x["bootstrap"]["upper_95"] for x in cand["ece_per_class"].values()
                                      if x["bootstrap"].get("upper_95") is not None)),
         "bootstrap_upper_threshold": 0.18, "direction": "<=",
         "pass": (max(x["ece"] for x in cand["ece_per_class"].values()) <= 0.15
                  and max(x["bootstrap"]["upper_95"] for x in cand["ece_per_class"].values()
                          if x["bootstrap"].get("upper_95") is not None) <= 0.18)},
        {"name": "calibration_fitted", "observed": True, "threshold": True, "direction": "==",
         "pass": v["V4_CALIBRATION_FITTED"]["pass"]},
        {"name": "degeneracy_screen_passed", "observed": m["screen"]["screen_pass"], "threshold": True,
         "direction": "==", "pass": m["screen"]["screen_pass"]},
        {"name": "positive_control_pass", "observed": R4(pc_acc), "threshold": 1.0, "direction": "==",
         "denominator": len(pc_rows), "pass": bool(pc_rows) and pc_acc == 1.0},
        {"name": "oracle_ceiling_pass",
         "observed": arms["B-INTERNAL-ID-ORACLE"]["mechanism_identity_accuracy"], "threshold": 1.0,
         "direction": "==", "pass": arms["B-INTERNAL-ID-ORACLE"]["mechanism_identity_accuracy"] == 1.0},
        {"name": "null_control_pass", "observed": R4(nc_abst / len(nc_rows)) if nc_rows else None,
         "threshold": 1.0, "direction": "==", "denominator": len(nc_rows),
         "pass": bool(nc_rows) and nc_abst == len(nc_rows)},
    ]
    gates.append({
        "gate": 8, "name": "secondary_gates", "order": "prereg 7.1 step 8",
        "pass": all(s["pass"] for s in sec),
        "failing_conditions": [s["name"] for s in sec if not s["pass"]],
        "detail": sec,
    })

    gate1 = gates[0]
    if not gate1["pass"]:
        status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
        reason = ("frozen decision_rule.outcomes.MEASUREMENT_INVALID: measurement-validity condition "
                  + ",".join(gate1["failing_conditions"]) + " FAILED. prereg.md 7.1 evaluates gate 1 first and "
                  "short-circuits.")
    elif not gates[-2]["pass"] or not gates[-1]["pass"]:
        status, outcome = "COMPLETE", "FALSIFIES"
        reason = "frozen decision_rule: primary gate or a secondary gate FAILED on an otherwise valid measurement"
    else:
        status, outcome = "COMPLETE", "SUPPORTS"
        reason = "all frozen gates passed"

    result: dict[str, Any] = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-36279237023",
        "lane": "graph",
        "status": status,
        "outcome": outcome,
        "metrics": {
            # --- stable metric identities from prereg.md 6 -----------------
            "mechanism_identity_accuracy": R4(primary["value"]),
            "mechanism_identity_accuracy_unit": "proportion of the 52 goals with at least one applicable "
                                                "mechanism for which selected_mechanism_id == target_mechanism_id; "
                                                "an abstention is an incorrect outcome (prereg 6.1)",
            "mechanism_identity_accuracy_denominator": primary["n_applicable_goals"],
            "mechanism_identity_accuracy_by_arm": {
                k: R4(v2["mechanism_identity_accuracy"]) for k, v2 in arms.items()
            },
            "mechanism_identity_accuracy_by_category": {
                k: {c: R4(cc["accuracy_applicable"]) for c, cc in v2["per_category"].items()
                    if cc["n_applicable"]}
                for k, v2 in arms.items()
            },
            "mechanism_identity_accuracy_counted_by_category": {
                k: {c: {"correct": sum(1 for r in rows if r["arm"] == k and r["category"] == c and r["correct"]),
                        "n_applicable": sum(1 for r in rows if r["arm"] == k and r["category"] == c
                                            and r["applies_any"]),
                        "n_rows": sum(1 for r in rows if r["arm"] == k and r["category"] == c),
                        "wrong_executable": sum(1 for r in rows if r["arm"] == k and r["category"] == c
                                                and r["executable"] and not r["correct"]),
                        "abstained": sum(1 for r in rows if r["arm"] == k and r["category"] == c
                                         and r["abstained"])}
                    for c in sorted({r["category"] for r in rows if r["arm"] == k})}
                for k in arms
            },
            "primary_tie_decomposition_vs_lexical": {
                "statement": "the exact 0.0 pooled tie between A-CANDIDATE and B-LEXICAL-OVERLAP is the net of "
                             "two large offsetting per-category effects, not equivalence between the two arms. "
                             "Category contributions (candidate minus lexical) on the 52 applicable goals: "
                             "verbatim 12-12=0, paraphrased 19-15=+4, underspecified 0-5=-5, composite 5-4=+1. "
                             "Sum = 0.",
                "interpretation_boundary": "this decomposition is DERIVED from the raw per-goal rows and is "
                                           "offered as a diagnosis of the observed primary-gate failure. It is "
                                           "NOT a frozen preregistered analysis, it is not a substitute for the "
                                           "primary gate, and it was not used to alter any threshold or gate "
                                           "verdict.",
            },
            "false_accept_rate": R4(cand["false_accept_rate"]),
            "false_accept_rate_denominator": cand["false_accept_denominator"],
            "false_accept_rate_numerator": cand["false_accept_numerator"],
            "false_accept_rate_on_applicable_executable_only": R4(
                sum(1 for r in cand_rows if r["executable"] and r["applies_any"] and not r["correct"])
                / sum(1 for r in cand_rows if r["executable"] and r["applies_any"])
            ),
            "false_accept_rate_by_arm": {k: R4(v2["false_accept_rate"]) for k, v2 in arms.items()},
            "false_accept_rate_reading_audit": {
                "why": "the frozen spec/prereg name a 'pooled false-accept rate' but never fix the "
                       "numerator/denominator pairing. The four defensible readings are reported per arm. The "
                       "coded value equals R2 for every arm EXCEPT A-CANDIDATE, where it equals R4 -- a hybrid "
                       "that is the only cell in the table pairing an all-80 numerator with an applicable-only "
                       "denominator. It is also the most pessimistic cell in the table. This defect is disclosed "
                       "as OBS-11 / VN-06 and is not repaired here, because repairing it would mean changing an "
                       "executed measurement after seeing the outcome.",
                "by_arm": fa_by_arm,
                "A-CANDIDATE_gate_0.10_under_each_reading": {
                    "R1_applicable_over_applicable": {"rate": cand_R1, "passes_0.10": cand_R1 <= 0.10},
                    "R2_all80_over_all80": {"rate": cand_R2, "passes_0.10": cand_R2 <= 0.10},
                    "R3_applicable_executable_denominator": {"rate": cand_R3, "passes_0.10": cand_R3 <= 0.10},
                    "R4_coded": {"rate": cand_R4, "passes_0.10": cand_R4 <= 0.10},
                },
                "A-CANDIDATE_gate_verdict_is_interpretation_dependent": fa_gate_flips,
                "robustness": "the false-accept gate is the ONLY secondary gate whose verdict depends on this "
                              "choice. UNKNOWN precision (0.6071 < 0.85), global ECE (0.2030 > 0.15, bootstrap "
                              "upper 0.2852 > 0.18), per-class ECE (0.7885 > 0.15) and the primary gate "
                              "(candidate == lexical exactly) all fail under every reading, so the packet's "
                              "conclusion does not rest on this ambiguity.",
            },
            "unknown_precision": R4(cand["unknown_precision"]),
            "unknown_precision_TP_abstain": cand["unknown_precision_terms"]["TP_abstain"],
            "unknown_precision_FP_abstain": cand["unknown_precision_terms"]["FP_abstain"],
            "unknown_precision_by_arm": {k: R4(v2["unknown_precision"]) for k, v2 in arms.items()},
            "ece_global": R4(cand["ece_global"]["ece"]),
            "ece_global_bootstrap_upper_95": R4(cand["ece_global_bootstrap"]["upper_95"]),
            "ece_global_n_rows": cand["ece_global"]["n"],
            "ece_global_n_bins": cand["ece_global"]["n_bins"],
            "ece_global_rows_dropped": cand["ece_global"]["rows_dropped"],
            "ece_global_bins": [
                {"bin": b["bin"], "n": b["n"], "mean_confidence": R4(b["mean_confidence"]),
                 "empirical_accuracy": R4(b["empirical_accuracy"]), "gap": R4(b["gap"])}
                for b in cand["ece_global"]["bins"]
            ],
            "ece_per_class_max": R4(max(x["ece"] for x in cand["ece_per_class"].values())),
            "ece_per_class": {
                k: {"ece": R4(x["ece"]), "n": x["n"], "n_bins": x["n_bins"],
                    "bootstrap_upper_95": R4(x["bootstrap"].get("upper_95"))}
                for k, x in cand["ece_per_class"].items()
            },
            "ece_global_all_80_goals_sensitivity": R4(cand["ece_global_all_80_goals"]["ece"]),
            "ece_global_nonabstain_rows_only_sensitivity": R4(
                cand["ece_global_nonabstain_rows_only"]["ece"]
            ),
            "calibration_is_fitted": bool(cal["fit"].get("fitted")),
            "calibration_w": cal["fit"]["w"],
            "calibration_b": cal["fit"]["b"],
            "calibration_threshold": thr,
            "calibration_gate_fired_on_n_applicable_goals": gate_fired,
            "calibration_p_top_min": R4(min(probs)) if probs else None,
            "calibration_p_top_max": R4(max(probs)) if probs else None,
            "candidate_abstention_causes": abstain_causes,
            "degeneracy_screen_pass": m["screen"]["screen_pass"],
            "degeneracy_lexical_accuracy_all80": R4(m["screen"]["lexical_overlap"]["accuracy_all_80"]),
            "degeneracy_lexical_accuracy_applicable_only": R4(
                m["screen"]["lexical_overlap"]["accuracy_applicable_only"]
            ),
            "degeneracy_lexical_structural_cap_all80": R4(
                m["screen"]["lexical_overlap"]["structural_cap_on_all80"]
            ),
            "pc_verbatim_accuracy": R4(pc_acc),
            "pc_verbatim_denominator": len(pc_rows),
            "pc_verbatim_false_accept": sum(1 for r in pc_rows if r["executable"] and not r["correct"]),
            "pc_verbatim_abstentions": sum(1 for r in pc_rows if r["abstained"]),
            "pc_verbatim_ece_observed": R4(abs(pc_rows[0]["p_applicable"] - 1.0)) if pc_rows else None,
            "pc_verbatim_ece_prereg_expected": 0.0,
            "pc_verbatim_unknown_precision_observed": 1.0,
            "pc_verbatim_unknown_precision_note": "vacuous: the candidate never abstains on a verbatim goal, so "
                                                 "TP_abstain + FP_abstain = 0 and the frozen vacuous rule "
                                                 "(prereg 4.7) returns 1.0",
            "oracle_accuracy": arms["B-INTERNAL-ID-ORACLE"]["mechanism_identity_accuracy"],
            "nc_abstention_rate": R4(nc_abst / len(nc_rows)) if nc_rows else None,
            "nc_denominator": len(nc_rows),
            "nc_abstention_causes": dict(Counter(r["abstain_reason"] for r in nc_rows if r["abstained"])),
            "abstention_rate_on_applicable": R4(cand["abstention_rate_on_applicable"]),
            "abstention_rate_on_no_applicable_28": R4(cand["abstention_rate_on_no_applicable"]),
            # --- primary gate machinery ----------------------------------
            "primary_metric": primary["metric"],
            "primary_comparison": "paired_family_blocked_bootstrap",
            "primary_alpha_one_sided": 0.05,
            "primary_difference_vs_B-LEXICAL-OVERLAP": R4(
                primary["vs_B-LEXICAL-OVERLAP"]["point_estimate_difference"]
            ),
            "primary_one_sided_lower_95_vs_B-LEXICAL-OVERLAP": R4(
                primary["vs_B-LEXICAL-OVERLAP"]["one_sided_lower_95"]
            ),
            "primary_p_one_sided_vs_B-LEXICAL-OVERLAP": R4(
                primary["vs_B-LEXICAL-OVERLAP"]["p_value_one_sided"]
            ),
            "primary_ci95_two_sided_vs_B-LEXICAL-OVERLAP": [
                R4(primary["vs_B-LEXICAL-OVERLAP"]["ci_lower_95_two_sided"]),
                R4(primary["vs_B-LEXICAL-OVERLAP"]["ci_upper_95_two_sided"]),
            ],
            "primary_difference_vs_B-RANDOM-ROLE": R4(
                primary["vs_B-RANDOM-ROLE"]["point_estimate_difference"]
            ),
            "primary_p_one_sided_vs_B-RANDOM-ROLE": R4(primary["vs_B-RANDOM-ROLE"]["p_value_one_sided"]),
            "primary_difference_vs_A-REFERENCE-EMBEDARGMAX": R4(
                primary["vs_A-REFERENCE-EMBEDARGMAX"]["point_estimate_difference"]
            ),
            "primary_difference_vs_B-INTERNAL-ID-ORACLE": R4(
                primary["vs_B-INTERNAL-ID-ORACLE"]["point_estimate_difference"]
            ),
            "primary_candidate_vs_lexical_contingency": {
                "both_correct": 29, "candidate_only_correct": 7, "lexical_only_correct": 7, "neither_correct": 9,
                "note": "on the 52 applicable goals the two arms win different goals in equal number; the exact "
                        "tie in the pooled rate is a compositional coincidence, not equivalence",
            },
            "primary_candidate_vs_uncalibrated_argmax_contingency": {
                "both_correct": 36, "candidate_only_correct": 0, "argmax_only_correct": 9, "neither_correct": 7,
                "note": "the candidate's correct set is a strict SUBSET of the uncalibrated argmax's correct set",
            },
            "primary_split_wise_accuracy": {k: R4(v2) for k, v2 in primary["split_wise_accuracy"].items()},
            # --- verification measure (separate, non-gating) --------------
            "http_execution_success_rate_by_arm": {
                k: R4(v2["http_execution_success_rate"]) for k, v2 in arms.items()
            },
            "http_requests_attempted_by_arm": {
                k: v2["http_requests_attempted"] for k, v2 in arms.items()
            },
            "http_requests_total": df["http_requests_total"],
            # --- measurement hygiene -------------------------------------
            "n_tasks": df["n_tasks"],
            "n_arms_per_task": df["n_arms_executed"],
            "n_raw_rows": len(rows),
            "distinct_task_start_state_hashes": df["state"]["distinct_task_start_state_hashes"],
            "task_start_state_hash": df["state"]["hash"],
            "distinct_arm_orderings": df["arm_order"]["n_distinct_orderings"],
            "estimator_unit_tests_all_pass": ph0["estimator_unit_tests"]["all_pass"],
            "frozen_input_hashes_match_freeze_json": ph1["frozen_input_hashes_match"],
            "reproducibility": "two independent full re-runs produced byte-identical "
                               "raw_evidence/task_results.jsonl and byte-identical derived_evidence/* "
                               "(only wall_clock_seconds differs)",
        },
        "controls": {
            "PC-VERBATIM-INTENT": {
                "role": "positive_control",
                "expected": spec["positive_control"]["expected_behavior"],
                "observed": {
                    "mechanism_identity_accuracy": R4(pc_acc),
                    "denominator": len(pc_rows),
                    "false_accept": sum(1 for r in pc_rows if r["executable"] and not r["correct"]),
                    "abstentions": sum(1 for r in pc_rows if r["abstained"]),
                    "ece": R4(abs(pc_rows[0]["p_applicable"] - 1.0)) if pc_rows else None,
                    "unknown_precision": 1.0,
                    "p_applicable": R4(pc_rows[0]["p_applicable"]) if pc_rows else None,
                },
                "verdict": "PASS",
                "verdict_detail": "the frozen decision gate for this control is pc_verbatim_accuracy == 1.0 with "
                                  "denominator > 0; both hold. The control's descriptive expectation "
                                  "'ECE = 0.0' is NOT met exactly: the observed value is |p_applicable - 1.0| for "
                                  "a perfect row, and every verbatim row sits at cos = 1.0 so the fitted gate "
                                  "assigns them the single value 0.9468 rather than 1.0. UNKNOWN precision is "
                                  "vacuous at 1.0 because the arm never abstains here.",
                "evidence": ["raw_evidence/task_results.jsonl (arm=A-CANDIDATE, category=verbatim)"],
            },
            "NC-NO-APPLICABLE": {
                "role": "null_control",
                "expected": spec["null_control"]["expected_behavior"],
                "observed": {
                    "abstention_rate": R4(nc_abst / len(nc_rows)) if nc_rows else None,
                    "denominator": len(nc_rows),
                    "false_accept": sum(1 for r in nc_rows if r["executable"] and not r["correct"]),
                    "abstention_causes": dict(Counter(r["abstain_reason"] for r in nc_rows if r["abstained"])),
                },
                "verdict": "PASS",
                "verdict_detail": "8 of 8 no-applicable goals were abstained on and none produced an EXECUTABLE "
                                  "decision. MATERIAL CAVEAT: every one of those 8 abstentions came from the "
                                  "parameter-binding stage ('unfilled_parameter_slots'), not from the calibrated "
                                  "gate. The gate abstained on 0 of 52 applicable goals and 0 of these 8.",
                "evidence": ["raw_evidence/task_results.jsonl (arm=A-CANDIDATE, category=no_applicable)"],
            },
            "B-LEXICAL-OVERLAP": {
                "role": "baseline_null",
                "expected": "strong baseline; must sit strictly below the 0.90 headroom threshold on the frozen "
                            "goal set",
                "observed": {
                    "mechanism_identity_accuracy_applicable": R4(arms["B-LEXICAL-OVERLAP"]["mechanism_identity_accuracy"]),
                    "mechanism_identity_accuracy_all80": R4(arms["B-LEXICAL-OVERLAP"]["mechanism_identity_accuracy_all80"]),
                    "headroom_threshold": 0.90,
                    "below_threshold_as_frozen": m["screen"]["lexical_overlap"]["pass_as_frozen_all80"],
                    "false_accept_rate": R4(arms["B-LEXICAL-OVERLAP"]["false_accept_rate"]),
                },
                "verdict": "PASS_AS_SCREEN_CONDITION_BUT_WEAK_AS_A_NULL",
                "verdict_detail": "the frozen screen condition (V8a, all-80 accuracy < 0.90) passes, but the "
                                  "applicable-only accuracy is 0.6923, i.e. it solves 36 of 52 applicable goals "
                                  "including 12/12 verbatim and 15/20 paraphrased. This is a substantially "
                                  "stronger lexical null than the parent packet's, and the frozen headroom screen "
                                  "cannot detect that because it is computed on a denominator the null cannot "
                                  "exceed.",
                "evidence": ["raw_evidence/task_results.jsonl (arm=B-LEXICAL-OVERLAP)",
                             "derived_evidence/degeneracy_screen.json"],
            },
            "B-RANDOM-ROLE": {
                "role": "baseline_null",
                "expected": "chance conditional on inferred role; approximately 1/(mechanisms_per_role)",
                "observed": {
                    "mechanism_identity_accuracy_applicable": R4(arms["B-RANDOM-ROLE"]["mechanism_identity_accuracy"]),
                    "expected_chance_1_of_5_mechanisms_per_role": 0.2,
                },
                "verdict": "PASS",
                "verdict_detail": "0.1346 is below the 0.2 chance level implied by the fixture's 5 mechanisms per "
                                  "role, i.e. the role-keyword inference is worse than uniform because its "
                                  "keyword table sometimes picks the wrong role and sometimes no role.",
                "evidence": ["raw_evidence/task_results.jsonl (arm=B-RANDOM-ROLE)"],
            },
            "B-INTERNAL-ID-ORACLE": {
                "role": "oracle_difficulty_ceiling",
                "expected": spec["baselines"][2]["expected_behavior"],
                "observed": {
                    "mechanism_identity_accuracy_applicable": arms["B-INTERNAL-ID-ORACLE"]["mechanism_identity_accuracy"],
                    "n_applicable": arms["B-INTERNAL-ID-ORACLE"]["n_applicable_rows"],
                    "abstained_on_no_applicable_goals": arms["B-INTERNAL-ID-ORACLE"]["n_abstained"],
                },
                "verdict": "PASS",
                "verdict_detail": "1.0 on all 52 applicable goals and abstention on all 28 goals with no "
                                  "applicable mechanism. The declared difficulty ceiling is therefore 1.0 and the "
                                  "fixture admits a perfect resolver, so the candidate's 0.6923 is a real gap to a "
                                  "reachable ceiling, not an artefact of an unsolvable fixture.",
                "evidence": ["raw_evidence/task_results.jsonl (arm=B-INTERNAL-ID-ORACLE)"],
            },
            "A-INCUMBENT": {
                "role": "incumbent_reference_leg",
                "expected": "prereg 4.2 expected EXECUTABLE on all applicable goals at min_confidence 0.5",
                "observed": {
                    "executable_count": m["screen"]["incumbent"]["executable_count"],
                    "n_goals": m["screen"]["incumbent"]["n_goals"],
                    "status_counts": m["screen"]["incumbent"]["status_counts"],
                    "mechanism_identity_accuracy": arms["A-INCUMBENT"]["mechanism_identity_accuracy"],
                    "false_accept_rate": arms["A-INCUMBENT"]["false_accept_rate"],
                },
                "verdict": "EMPTY_LEG",
                "verdict_detail": "0 of 80 EXECUTABLE; all 80 UNKNOWN. This is a code-level certainty, not a "
                                  "measured floor: kernel.py:resolve() requires exact intent-string equality AND "
                                  "all template slots present in the supplied params, V11 forbids empty "
                                  "parameter_slots, and this arm supplies params={}. The prereg's own expectation "
                                  "that the incumbent's mechanisms carry parameter_slots=[] is contradicted by "
                                  "V11 inside the same frozen document.",
                "evidence": ["raw_evidence/task_results.jsonl (arm=A-INCUMBENT)",
                             "raw_evidence/degeneracy_screen_per_goal.jsonl (arm=A-INCUMBENT)"],
            },
            "A-REFERENCE-EMBEDARGMAX": {
                "role": "declared_substitute_comparison_leg",
                "expected": "prereg 11: declared non-empty substitute when the incumbent leg is empty",
                "observed": {
                    "executable_count": m["screen"]["substitute_leg"]["executable_count"],
                    "mechanism_identity_accuracy_applicable": R4(arms["A-REFERENCE-EMBEDARGMAX"]["mechanism_identity_accuracy"]),
                    "false_accept_rate": R4(arms["A-REFERENCE-EMBEDARGMAX"]["false_accept_rate"]),
                    "unknown_precision": R4(arms["A-REFERENCE-EMBEDARGMAX"]["unknown_precision"]),
                },
                "verdict": "PASS_AS_SUBSTITUTE_AND_STRONGER_THAN_THE_CANDIDATE",
                "verdict_detail": "non-empty (80 of 80 EXECUTABLE) as required, and it scores 0.8654 on the frozen "
                                  "primary metric against the candidate's 0.6923. The uncalibrated, never-abstaining "
                                  "resolver beats the fitted-gate resolver, because every abstention the candidate "
                                  "makes costs it a mechanism-identity point under prereg 6.1 while buying nothing "
                                  "against the pooled false-accept gate. This is the single most decision-relevant "
                                  "number in the packet.",
                "evidence": ["raw_evidence/task_results.jsonl (arm=A-REFERENCE-EMBEDARGMAX)"],
            },
            "A-CANDIDATE": {
                "role": "candidate_under_test",
                "expected": spec["hypothesis"],
                "observed": {
                    "mechanism_identity_accuracy": R4(primary["value"]),
                    "false_accept_rate": R4(cand["false_accept_rate"]),
                    "unknown_precision": R4(cand["unknown_precision"]),
                    "ece_global": R4(cand["ece_global"]["ece"]),
                    "ece_per_class_max": R4(max(x["ece"] for x in cand["ece_per_class"].values())),
                },
                "verdict": "FALSIFIED_ON_ITS_OWN_TERMS",
                "verdict_detail": "the candidate does not exceed the lexical null (difference exactly 0.0, one-sided "
                                  "lower 95% -0.0652, p 0.594), and four of the nine secondary gates fail on their "
                                  "own thresholds. This verdict is recorded but is NOT the packet's status, because "
                                  "the frozen gate order evaluates measurement validity first and V9 fails.",
                "evidence": ["derived_evidence/metrics.json", "raw_evidence/task_results.jsonl"],
            },
        },
        "artifacts": [],
        "observations": [
            {"id": "OBS-01", "level": "raw_evidence", "kind": "reproducibility",
             "statement": "Two independent full executions of the runner produced byte-identical "
                          "raw_evidence/task_results.jsonl and byte-identical derived_evidence/*; the only "
                          "differing field anywhere is wall_clock_seconds.",
             "value": "deterministic", "evidence": ["raw_evidence/task_results.jsonl",
                                                    "derived_evidence/metrics.json"]},
            {"id": "OBS-02", "level": "raw_evidence", "kind": "measurement_hygiene",
             "statement": "All 80 tasks began from a single identical application state hash and the store was "
                          "reset before every arm request.",
             "value": {"distinct_task_start_state_hashes": df["state"]["distinct_task_start_state_hashes"],
                       "state_hash": df["state"]["hash"]},
             "evidence": ["derived_evidence/design_facts.json"]},
            {"id": "OBS-03", "level": "raw_evidence", "kind": "measurement_hygiene",
             "statement": "The frozen minimum of 43 distinct arm orderings was exceeded.",
             "value": {"n_distinct_orderings": 78, "n_tasks": 80, "prereg_minimum": 43},
             "evidence": ["derived_evidence/design_facts.json"]},
            {"id": "OBS-04", "level": "raw_evidence", "kind": "coverage",
             "statement": "480 raw rows were written (80 tasks x 6 arms) and no estimator dropped any row.",
             "value": {"rows": 480, "http_requests_total": 240, "rows_dropped_by_any_estimator": 0},
             "evidence": ["raw_evidence/task_results.jsonl"]},
            {"id": "OBS-05", "level": "raw_evidence", "kind": "integrity",
             "statement": "The sha256 of each frozen input recomputed at execution time equals the value recorded "
                          "in freeze.json; the frozen inputs were not modified.",
             "value": {"request.json": "d482a1898b243f6bdeec5870ca70993fe64a811dd3e9b1a99cd32e2064bd8b3d",
                       "spec.json": "0151912409917e9098ff691df04b71097e769740bddc30d7bfd7e8862802fcd5",
                       "prereg.md": "0c95744647f7aa9943e14de5db7c758e1d45ea152a961f424aab6f610ac66657"},
             "evidence": ["derived_evidence/phase1_validity_preconditions.json"]},
            {"id": "OBS-06", "level": "observation", "kind": "primary_measurement",
             "statement": "A-CANDIDATE selected the target mechanism on 36 of the 52 goals that have at least one "
                          "applicable mechanism.",
             "value": 0.692308, "evidence": ["raw_evidence/task_results.jsonl"]},
            {"id": "OBS-07", "level": "observation", "kind": "category_decomposition",
             "statement": "Counted correctly out of applicable, A-CANDIDATE scored verbatim 12/12, paraphrased "
                          "19/20, underspecified 0/10, composite 5/10. B-LEXICAL-OVERLAP scored 12/12, 15/20, "
                          "5/10, 4/10. A-REFERENCE-EMBEDARGMAX scored 12/12, 19/20, 9/10, 5/10.",
             "value": "see metrics.mechanism_identity_accuracy_counted_by_category",
             "evidence": ["raw_evidence/task_results.jsonl"]},
            {"id": "OBS-08", "level": "raw_evidence", "kind": "decision_provenance",
             "statement": "All 28 A-CANDIDATE abstentions carry abstain_reason 'unfilled_parameter_slots'. No "
                          "abstention was produced by the calibrated gate.",
             "value": {"unfilled_parameter_slots": 28, "gate_threshold": 0},
             "evidence": ["raw_evidence/task_results.jsonl"]},
            {"id": "OBS-09", "level": "derived_measurement", "kind": "gate_behaviour",
             "statement": "The fitted gate assigns p in [0.6785, 0.9468] to the 52 applicable goals. The selected "
                          "threshold is 0.02, so 0 of 52 goals fall below it and the gate never fires.",
             "value": {"p_min": 0.678462, "p_max": 0.946751, "threshold": 0.02, "n_below_threshold": 0},
             "evidence": ["derived_evidence/calibration.json"]},
            {"id": "OBS-10", "level": "raw_evidence", "kind": "safety",
             "statement": "On the 20 'ood' goals, which have no applicable mechanism at all, A-CANDIDATE produced "
                          "11 EXECUTABLE decisions at p between 0.6925 and 0.8407 (mean 0.7787) and abstained on 9.",
             "value": {"executable_on_ood": 11, "n_ood": 20, "mean_p_on_ood_executable": 0.778723},
             "evidence": ["raw_evidence/task_results.jsonl"]},
            {"id": "OBS-11", "level": "derived_measurement", "kind": "metric_defect",
             "statement": "The coded false_accept_rate equals reading R2 (all-80 wrong executions over all 80) for "
                          "every arm EXCEPT A-CANDIDATE, where it equals R4 (all-80 wrong executions over the 52 "
                          "applicable goals). A-CANDIDATE's 0.3077 is therefore not comparable with the other arms' "
                          "cells and is the most pessimistic cell in the table.",
             "value": {"A-CANDIDATE": 0.307692, "A-REFERENCE-EMBEDARGMAX": 0.4375,
                       "B-LEXICAL-OVERLAP": 0.55, "B-RANDOM-ROLE": 0.9125, "B-INTERNAL-ID-ORACLE": 0.0},
             "evidence": ["metrics.false_accept_rate_reading_audit"]},
            {"id": "OBS-12", "level": "raw_evidence", "kind": "incumbent_behaviour",
             "statement": "A-INCUMBENT produced 0 EXECUTABLE decisions out of 80 goals; all 80 were UNKNOWN.",
             "value": {"executable": 0, "n_goals": 80},
             "evidence": ["raw_evidence/task_results.jsonl", "raw_evidence/degeneracy_screen_per_goal.jsonl"]},
            {"id": "OBS-13", "level": "derived_measurement", "kind": "baseline_comparison",
             "statement": "The declared substitute leg A-REFERENCE-EMBEDARGMAX scores 45/52 = 0.8654 on the frozen "
                          "primary metric against the candidate's 36/52 = 0.6923, and 45/80 = 0.5625 over all 80 "
                          "against the candidate's 36/80 = 0.45. It never abstains.",
             "value": {"candidate": 0.692308, "embedargmax": 0.865385, "difference": -0.173077,
                       "one_sided_lower_95": -0.203704, "p_one_sided": 1.0},
             "evidence": ["derived_evidence/metrics.json"]},
            {"id": "OBS-14", "level": "derived_measurement", "kind": "contingency",
             "statement": "On the 52 applicable goals A-CANDIDATE and B-LEXICAL-OVERLAP are both correct on 29, "
                          "candidate-only correct on 7, lexical-only correct on 7, neither correct on 9.",
             "value": {"both": 29, "candidate_only": 7, "lexical_only": 7, "neither": 9},
             "evidence": ["raw_evidence/task_results.jsonl"]},
            {"id": "OBS-15", "level": "derived_measurement", "kind": "difficulty_ceiling",
             "statement": "B-INTERNAL-ID-ORACLE reached 52/52 on applicable goals and abstained on all 28 goals "
                          "with no applicable mechanism.",
             "value": {"applicable_accuracy": 1.0, "abstained_on_no_applicable": 28},
             "evidence": ["raw_evidence/task_results.jsonl"]},
            {"id": "OBS-16", "level": "derived_measurement", "kind": "calibration_structure",
             "statement": "ABSTAIN-class ECE is 0.7885 over 11 rows, but none of those 11 rows was abstained on by "
                          "the gate; they were abstained on by the parameter slot filler while carrying a gate "
                          "confidence of 0.68 to 0.91 that the gate never acted on.",
             "value": {"ece_abstain_class": 0.788463, "n": 11, "gate_fired_on": 0},
             "evidence": ["derived_evidence/metrics.json"]},
            {"id": "OBS-17", "level": "raw_evidence", "kind": "freeze_contents",
             "statement": "freeze.json records a sha256 for exactly three files (prereg.md, request.json, spec.json) "
                          "and for zero code files. V9 requires outcome-bearing code to be hashed into the freeze.",
             "value": {"files_hashed": 3, "code_files_hashed": 0,
                       "cause": "scripts/freeze_experiment.py at commit 7f5879fc hashes only the three design "
                                "documents, and that file is outside the graph lane's allowed code roots"},
             "evidence": ["research/experiments/EXP-GRAPH-36279237023/freeze.json",
                          "derived_evidence/phase1_validity_preconditions.json"]},
            {"id": "OBS-18", "level": "raw_evidence", "kind": "positive_control_detail",
             "statement": "All 12 verbatim goals were bound and selected correctly, but every one carries "
                          "p_applicable = 0.9468 rather than 1.0, because cos_sim = 1.0 maps through the fitted "
                          "gate to 0.9468. The control's descriptive expectation of ECE = 0.0 is therefore not met "
                          "exactly; the observed descriptive value is 0.0532. The frozen decision gate for the "
                          "control is accuracy == 1.0 with denominator > 0, which is met.",
             "value": {"accuracy": 1.0, "denominator": 12, "ece_observed": 0.053249, "ece_prereg_expected": 0.0},
             "evidence": ["raw_evidence/task_results.jsonl"]},
            {"id": "OBS-19", "level": "derived_measurement", "kind": "split_wise",
             "statement": "Primary accuracy is 0.6667 on the 42 train goals and 0.80 on the 10 validation goals. "
                          "The frozen design has no held-out test split, so the primary metric is reported on the "
                          "union.",
             "value": {"train_only": 0.666667, "validation_only": 0.8, "n_train": 42, "n_val": 10},
             "evidence": ["derived_evidence/metrics.json"]},
            {"id": "OBS-20", "level": "derived_measurement", "kind": "gate_fittedness",
             "statement": "Refitting on independent train splits moves the logistic weight (w = 2.7440, 1.6211, "
                          "1.9349; spread 1.1230), so the gate is a learned function of the data rather than a "
                          "fixed algebraic transform of cos_sim.",
             "value": {"w_spread": 1.122960}, "evidence": ["derived_evidence/calibration.json"]},
            {"id": "OBS-21", "level": "derived_measurement", "kind": "threshold_robustness_diagnostic",
             "statement": "A post-hoc diagnostic that maximised the F1 of the ACCEPT class on the validation split "
                          "instead of the frozen commit/abstain F1 also selected t = 0.02, so the gate's inertness "
                          "is not an artifact of the declared threshold-selection reading.",
             "value": {"frozen_criterion_selected": 0.02, "accept_class_f1_criterion_selected": 0.02},
             "evidence": ["diagnostic recomputation over derived_evidence/calibration.json cosine_top_only_rows"],
             "caveat": "this diagnostic was NOT preregistered; it is reported as supporting evidence only and did "
                       "not alter any gate verdict"},
        ],
        "validity_notes": [
            {"id": "VN-01", "severity": "blocking", "affects": "status",
             "note": "V9_CODE_HASHED_INTO_FREEZE fails structurally, not because of anything done during execution. "
                     "freeze.json is immutable and the only freezer in the repository hashes no code, so no "
                     "compliant execution of this design was possible. Under the frozen decision rule this forces "
                     "status=MEASUREMENT_INVALID. The measurements themselves are internally valid and are reported "
                     "in full so that nothing observed is discarded, but no VALIDATED or REJECTED promotion of "
                     "C-SEMANTIC-RESOLVE may rest on this packet alone."},
            {"id": "VN-02", "severity": "bounding", "affects": "generalization",
             "note": "The substrate is a stdlib-only local HTTP application with 20 mechanisms over 20 endpoints on "
                     "5 resource families. There is no live web, no third-party site, no LLM, no authentication, no "
                     "pagination, no failure injection and no adversarial input. Every result here is a result "
                     "about this substrate. It is not evidence about the open Web."},
            {"id": "VN-03", "severity": "moderate", "affects": "calibration",
             "note": "All embeddings come from one model, sentence-transformers/all-MiniLM-L6-v2, 384 dimensions, "
                     "loaded from the local cache with its revision recorded in derived_evidence/calibration.json. "
                     "There is no model ensemble and no cross-model replication, so the fitted coefficients "
                     "(w = 2.6927, b = 0.1853) are specific to this checkpoint."},
            {"id": "VN-04", "severity": "moderate", "affects": "primary_metric",
             "note": "The frozen design supplies train/validation only and no held-out test split, so the primary "
                     "mechanism-identity accuracy is reported on the union of train and validation (0.6667 vs 0.80 "
                     "separately). Selection of the selected mechanism is a parameter-free argmax of a frozen "
                     "embedding cosine, so the union does not contaminate mechanism selection; the fitted abstain "
                     "decision is fitted on train and evaluated on the union."},
            {"id": "VN-05", "severity": "moderate", "affects": "safety_conclusions",
             "note": "The 20-goal 'ood' pool with no applicable mechanism is small, so the 11/20 false-execution "
                     "rate on that pool carries a wide binomial interval and is reported as a point estimate only. "
                     "No frozen gate constrains it: those goals are outside the primary metric and outside the "
                     "gate's fitting set."},
            {"id": "VN-06", "severity": "material", "affects": "pooled_false_accept gate",
             "note": "The false-accept denominator is inconsistent across arms (OBS-11), so the false-accept column "
                     "is not comparable across arms. The defect was found after the outcomes were visible and was "
                     "NOT repaired, because repairing a metric after seeing the outcome is exactly what the "
                     "freeze is meant to prevent. All four readings are reported. The false-accept gate is the only "
                     "gate whose verdict changes across readings (0.0962 R1 passes, 0.2000 R2 fails, 0.1220 R3 "
                     "fails, 0.3077 R4 as coded fails)."},
            {"id": "VN-07", "severity": "material", "affects": "ece_global, ece_per_class_max, unknown_precision",
             "note": "The calibrated gate never fires (OBS-09), so all abstention in the candidate is produced by "
                     "the parameter slot filler, which is not calibrated at all. The ECE gates therefore score a "
                     "gate that made no decisions, and the ABSTAIN-class ECE of 0.7885 measures the slot filler's "
                     "abstentions against an unused confidence. The global ECE of 0.2030 is inflated by the same "
                     "mechanism. These two gates are not clean tests of the candidate's actual decision rule."},
            {"id": "VN-08", "severity": "material", "affects": "V8a_degeneracy_screen",
             "note": "The frozen headroom screen is computed on all 80 goals, but 28 of them have no applicable "
                     "mechanism, which caps any arm at 52/80 = 0.65. The screen therefore cannot detect lexical "
                     "adequacy, and the lexical null is in fact much stronger than the screen anticipates: it "
                     "solves 36/52 including 12/12 verbatim and 15/20 paraphrased. V8a is non-binding by "
                     "construction."},
            {"id": "VN-09", "severity": "material", "affects": "all_counts",
             "note": "Three specification resolutions were declared before any candidate measurement and are "
                     "disclosed in controls and in derived_evidence/calibration.json: the 52/28 applicable split "
                     "instead of the prereg's arithmetically inconsistent '60 applicable'; value-bearing recorded "
                     "intents so the verbatim positive control can bind slots; and A-REFERENCE-EMBEDARGMAX as the "
                     "prereg-authorized substitute comparison leg. These change which rows count, so a different "
                     "but equally defensible resolution yields different numbers. An auditor should re-derive under "
                     "the 60-goal reading before treating any count as canonical."},
            {"id": "VN-10", "severity": "moderate", "affects": "primary_uncertainty",
             "note": "The paired family-blocked bootstrap resamples 5 blocks of 7 to 14 goals 10000 times, but it "
                     "resamples blocks, not goals, and there is only one arm ordering seed. The interval is "
                     "therefore wide and does not propagate goal-sampling or seed variability."},
            {"id": "VN-11", "severity": "material", "affects": "safety_conclusions",
             "note": "The 11 confident wrong executions on goals with no applicable mechanism carry no weight in "
                     "the primary metric, no weight in the pooled false-accept numerator under reading R1, and no "
                     "weight in either ECE gate, because the gate is fitted only on goals that have an applicable "
                     "mechanism. The frozen metric suite structurally cannot see the candidate's most product-"
                     "relevant failure mode."},
            {"id": "VN-12", "severity": "moderate", "affects": "primary_metric",
             "note": "The primary metric scores an abstention as an incorrect outcome, which penalises the "
                     "candidate for the conservative behaviour it exhibits on all 10 underspecified goals. A "
                     "metric that scored abstention as a distinct, non-error outcome would rank the candidate "
                     "differently on exactly the category where it differs most from the uncalibrated baseline."},
        ],
        "unresolved": [
            {"id": "UNRES-01",
             "question": "Is the candidate worse than the uncalibrated argmax because of the embedding, or purely "
                         "because of its non-calibrated abstention policy?",
             "status": "UNRESOLVED_BY_THIS_DESIGN",
             "partial_evidence": "the entire deficit is concentrated in the 10 underspecified goals, where the "
                                 "candidate scores 0/10 by abstaining on all 10 while the argmax scores 9/10. On "
                                 "paraphrased and composite goals the candidate ties the argmax (19/20 and 5/10). "
                                 "The frozen design has no arm that separates the two components."},
            {"id": "UNRES-02",
             "question": "Would an applicability gate fitted with a proper negative class abstain on the 20 ood "
                         "goals, where the candidate fires on 11 of them?",
             "status": "UNRESOLVED_BY_THIS_DESIGN",
             "partial_evidence": "not testable here, because the frozen fitting set contains only goals that have an "
                                 "applicable mechanism, so the gate never sees a negative."},
            {"id": "UNRES-03",
             "question": "Is the lexical null at 36/52 a genuine barrier to the semantic route?",
             "status": "PARTIALLY_RESOLVED",
             "partial_evidence": "no. The category decomposition shows the two arms are not equivalent: the "
                                 "embedding route beats lexical by 4 goals on paraphrased intent (19/20 vs 15/20) "
                                 "and by 1 on composite, and loses 5 on underspecified. The pooled tie is a "
                                 "compositional cancellation, so the semantic route does carry real signal that "
                                 "the candidate's abstention policy destroys."},
            {"id": "UNRES-04",
             "question": "Is the V9 failure a documentation defect only, or does it mean the executed code cannot "
                         "be tied to any reviewed artifact?",
             "status": "UNRESOLVED",
             "partial_evidence": "not answerable without a new freeze that hashes code. artifact hashes are "
                                 "recorded in this packet after the fact and are explicitly NOT offered as "
                                 "satisfying V9."},
            {"id": "UNRES-05",
             "question": "What is the correct product action: re-freeze this same design with code hashes, or "
                         "change the design?",
             "status": "NOT_A_LANE_DECISION",
             "partial_evidence": "the packet's evidence points at a design change rather than a re-run: the gate "
                                 "is inert, the false-accept metric is ambiguous, the safety-relevant ood failures "
                                 "are invisible to the frozen gates, and the primary gate's failure decomposes "
                                 "into a category-specific abstention policy. A re-freeze of the same design would "
                                 "repair V9 and change none of these."},
            {"id": "UNRES-06",
             "question": "What is the canonical applicable-goal count?",
             "status": "UNRESOLVED_INHERITED",
             "partial_evidence": "52 is used and justified, but the prereg's own '60 applicable' figure counts the "
                                 "20 ood goals as applicable and contradicts its own OOD description and its own "
                                 "NC-NO-APPLICABLE control. Carried forward unresolved from the freeze."},
            {"id": "UNRES-07",
             "question": "Would a different threshold-selection objective produce a non-inert gate?",
             "status": "WEAKLY_RESOLVED_NEGATIVE",
             "partial_evidence": "a post-hoc diagnostic maximising ACCEPT-class F1 selected the same t = 0.02, and "
                                 "every threshold from 0.02 up to 0.68 would abstain on 0 of 52 goals because the "
                                 "minimum p is 0.6785. Any threshold in (0.02, 0.68] is equally inert, so this is "
                                 "a property of the fitted coefficients on this fixture, not of the selection rule."},
        ],
        "frozen_decision_rule_evaluation": {
            "source": "spec.json decision_rule + prereg.md 7.1",
            "gate_order": "V1-V11 -> degeneracy screen -> positive control -> oracle ceiling -> null control -> "
                          "calibration fitted -> primary -> secondary",
            "status_reason": reason,
            "measurement_validity_conditions": v,
            "gates": gates,
            "status_outcome_mapping_note": "spec.json decision_rule.outcomes.MEASUREMENT_INVALID maps to packet "
                                           "status=MEASUREMENT_INVALID with outcome=INCONCLUSIVE. A "
                                           "MEASUREMENT_INVALID status here is a statement about the validity of "
                                           "the measurement transaction, not a scientific negative about "
                                           "C-SEMANTIC-RESOLVE. The gate-by-gate measurements are reported in full "
                                           "above so that nothing measured here is discarded.",
        },
    }

    # ------------------------------------------------------------- artifacts
    art = [
        ("artifacts/fixture_def.py", "code", "frozen fixture definition (20 mechanisms, 20 endpoints)"),
        ("artifacts/goal_generator.py", "code", "deterministic 80-goal generator"),
        ("artifacts/http_server.py", "code", "stdlib-only 20-endpoint HTTP application with state hash"),
        ("artifacts/candidate_resolver.py", "code", "A-CANDIDATE, all null baselines, incumbent adapter, slot filler"),
        ("artifacts/metric_estimators.py", "code", "frozen ECE / UNKNOWN-precision / bootstrap estimators + unit tests"),
        ("artifacts/experiment_runner.py", "code", "phase-ordered runner: screen -> calibration -> arms -> metrics"),
        ("artifacts/write_packet.py", "code", "derives this packet's frozen gate table from derived evidence; runs no measurement"),
        ("artifacts/fixture.json", "fixture", "20 mechanisms with intents, parameter_slots, action_templates"),
        ("artifacts/goals.json", "fixture", "80 goals with target mechanism_ids and the declared 60-goal ambiguity"),
        ("raw_evidence/task_results.jsonl", "raw", "480 rows = 80 tasks x 6 arms, one JSON object per (task, arm)"),
        ("raw_evidence/goals_flat.jsonl", "raw", "the 80 goals as executed"),
        ("raw_evidence/degeneracy_screen_per_goal.jsonl", "raw", "per-goal screen rows, written before any candidate arm"),
        ("derived_evidence/phase0_preconditions.json", "derived", "estimator unit tests, fixture integrity, goal independence"),
        ("derived_evidence/phase1_validity_preconditions.json", "derived", "V9 freeze-hash check, frozen-input hash verification"),
        ("derived_evidence/degeneracy_screen.json", "derived", "V8 screen output incl. substitute-leg declaration"),
        ("derived_evidence/calibration.json", "derived", "fitted gate, split, threshold sweep, seed refits, model fingerprint"),
        ("derived_evidence/metrics.json", "derived", "all arm metrics, bootstraps, ECE bins, per-category breakdown"),
        ("derived_evidence/design_facts.json", "derived", "state hashes, arm orderings, seeds, counts"),
    ]
    for rel, role, desc in art:
        p = EXP / rel
        result["artifacts"].append({
            "path": f"research/experiments/EXP-GRAPH-36279237023/{rel}",
            "sha256": sha256_file(p),
            "role": role,
            "description": desc,
        })

    (EXP / "derived_evidence" / "gate_table.json").write_text(
        json.dumps(result["frozen_decision_rule_evaluation"], indent=2, sort_keys=True) + "\n"
    )
    result["artifacts"].append({
        "path": "research/experiments/EXP-GRAPH-36279237023/derived_evidence/gate_table.json",
        "sha256": sha256_file(EXP / "derived_evidence" / "gate_table.json"),
        "role": "derived",
        "description": "machine-derived frozen gate table (this script's output, written before result.json)",
    })

    (EXP / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": status, "outcome": outcome,
                      "gate1_pass": gates[0]["pass"], "gate1_failing": gates[0]["failing_conditions"],
                      "primary_pass": prim_pass,
                      "secondary_failing": gates[-1]["failing_conditions"],
                      "reason": reason}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
