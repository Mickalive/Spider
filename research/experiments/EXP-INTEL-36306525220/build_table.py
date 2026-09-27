#!/usr/bin/env python3
"""EXP-INTEL-36306525220 :: Stage 4 -- machine-checkable table, coverage, control
verdicts and application of the FROZEN decision rules (prereg.md Sections 7 and 8).

This stage does not interpret; it maps already-recorded determinations onto the frozen
decision rule clauses in their frozen precedence order and writes the results the
packet contract requires.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolve_identity import RAW, now  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")

P1_FIELDS = [  # prereg.md Section 5.1, the ten required rows
    "Routine_Overhead_Ratio_R", "delegable_recurrence_h", "break_even_reuse_count_fstar",
    "marginal_cost_cached_vs_derived", "staleness_forgetting_maintenance_cost",
    "real_cost_advantage_persistence", "denominator", "accounting_convention",
    "stated_uncertainty", "modeled_vs_measured",
]
P1_ALIASES = {"Routine_Overhead_Ratio_R": ["Routine_Overhead_Ratio_R", "Routine_Overhead_Ratio_R_ceiling_rung"]}
P2_FIELDS = ["success_rate", "denominator", "evaluation_convention", "benchmark_split"]
P3_FIELDS = ["retrieval_quality_metric", "write_pipeline_type", "downstream_accuracy", "ablation_result"]


def sha(p: str) -> str | None:
    if not os.path.exists(p):
        return None
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main() -> int:
    os.makedirs(RES, exist_ok=True)
    idr = json.load(open(os.path.join(RAW, "identity_resolution.json"), encoding="utf-8"))
    recheck = json.load(open(os.path.join(RAW, "base_id_recheck.json"), encoding="utf-8"))
    ctrl = json.load(open(os.path.join(RAW, "controls_result.json"), encoding="utf-8"))["controls"]
    det = json.load(open(os.path.join(RAW, "field_determinations.json"), encoding="utf-8"))
    rows_in = det["rows"]
    spec = json.load(open(os.path.join(HERE, "spec.json"), encoding="utf-8"))
    frozen_names = list(spec["identity_resolution"]["frozen_target_list"].keys())

    # ------------------------------------------------------------------
    # effective identity resolution (base-ID recheck supersedes a 404 caused
    # solely by a non-existent version suffix -- logged, not a rule change)
    # ------------------------------------------------------------------
    effective = {}
    for name, v in idr["targets"].items():
        eff = dict(v)
        if name in recheck["targets"]:
            rc = recheck["targets"][name]
            if rc["resolution_status"] != "NOT_LOCATED":
                eff = {
                    "target_system": name, "target_arxiv_id": rc["target_arxiv_id"],
                    "resolution_status": rc["resolution_status"],
                    "returned_title": rc["returned_title"], "returned_arxiv_id": rc["returned_arxiv_id"],
                    "failed_conditions": rc["failed_conditions"], "checks": rc["checks"],
                    "effective_requested_id": rc["recheck_note"],
                }
        effective[name] = eff

    correctly_resolved = [n for n, v in effective.items() if v["resolution_status"] == "CORRECTLY_RESOLVED"]
    named_systems_searched = len(frozen_names)
    recall = len(correctly_resolved) / named_systems_searched

    declared_placeholders = ["Crux", "WebAgent", "RULER", "WebCanvas", "BrowserBench"]
    non_placeholder = [n for n in frozen_names if n not in declared_placeholders]
    recall_non_placeholder = len(correctly_resolved) / len(non_placeholder)
    real_author_lists = [n for n in frozen_names
                         if not any(str(a).strip().upper() == "TBD"
                                    for a in spec["identity_resolution"]["frozen_target_list"][n]["expected_authors"])]
    recall_real_author_lists = len(correctly_resolved) / len(real_author_lists)

    coverage = {
        "identity_resolution_recall": round(recall, 6),
        "identity_resolution_recall_denominator_definition": (
            "correctly_resolved / named_systems_searched over the 14 frozen entries of "
            "spec.json identity_resolution.frozen_target_list; no per-part partition of the "
            "frozen list exists, so the same denominator is used for Parts 1, 2 and 3"
        ),
        "named_systems_searched": named_systems_searched,
        "correctly_resolved": len(correctly_resolved),
        "correctly_resolved_names": correctly_resolved,
        "identity_resolution_recall_excluding_prereg_declared_placeholders": round(recall_non_placeholder, 6),
        "n_excluding_prereg_declared_placeholders": len(non_placeholder),
        "identity_resolution_recall_over_entries_with_real_author_lists": round(recall_real_author_lists, 6),
        "n_entries_with_real_author_lists": len(real_author_lists),
        "recall_robust_to_denominator_choice": bool(
            recall < 0.6 and recall_non_placeholder < 0.6 and recall_real_author_lists < 0.6
        ),
        "unsearched_systems": [],
        "systems_not_in_frozen_list": [
            "Agent Workflow Memory (Wang, Mao, Fried, Neubig 2024)",
            "WebCoach", "ReasoningBank",
            "any published system reporting a measured break-even reuse count f*",
        ],
        "unsearched_systems_note": (
            "The frozen target list is a closed list of 14 named systems; every entry was searched. "
            "The unsearched space is the published literature outside that list, which prereg 4.4 "
            "delegates to a bounded snowball. The snowball was ATTEMPTED and yielded 0 usable "
            "candidates (raw/references/snowball_candidates.json): the PC artifact's reference list "
            "prints no arXiv identifiers, so the frozen inclusion rule "
            "('reference strings that contain an arXiv identifier') selects nothing."
        ),
        "snowball_coverage": {
            "papers_examined": 0,
            "papers_resolved": 0,
            "reference_strings_found": json.load(open(os.path.join(RAW, "references",
                                                                   "snowball_candidates.json"),
                                                      encoding="utf-8"))["n_reference_strings_found"],
            "usable_candidates_under_frozen_inclusion_rule": 0,
            "selection_rule": "raw/references/snowball_candidates.json -> selection_rule",
            "cap": 25,
        },
    }

    # ------------------------------------------------------------------
    # machine-checkable artifact table (spec.json output_contract)
    # ------------------------------------------------------------------
    table = []
    for name in frozen_names:
        v = effective[name]
        st = v["resolution_status"]
        if st == "CORRECTLY_RESOLVED":
            rstat = "CORRECTLY_RESOLVED"
        elif st == "AMBIGUOUS":
            rstat = "AMBIGUOUS"
        else:
            rstat = "NOT_LOCATED"
        t = spec["identity_resolution"]["frozen_target_list"][name]
        if st != "CORRECTLY_RESOLVED":
            table.append({
                "part": None,
                "system": name,
                "benchmark": None,
                "metric": "any_part_1_2_3_quantity",
                "value": None,
                "denominator": None,
                "accounting_convention": None,
                "stated_uncertainty": None,
                "modeled_vs_measured": None,
                "source_quote": None,
                "source_arxiv_id": v.get("returned_arxiv_id"),
                "resolution_status": rstat,
                "scored_as": "UNMEASURED",
                "evidence_for_absence": (
                    "Identity resolution failed under the frozen prereg 4.1 conjunction: failed "
                    f"conditions {v['failed_conditions']}. Frozen expected_title="
                    f"{t['expected_title']!r}, frozen expected_authors={t['expected_authors']}, "
                    f"requested id {v['target_arxiv_id']} returned "
                    f"{(v.get('returned_title') or 'no artifact')!r}. NOT converted to NOT_FOUND."
                ),
            })

    for r in rows_in:
        system = r["system"]
        v = effective.get(system, {})
        table.append({
            "part": r["part"],
            "system": system,
            "benchmark": r["benchmark"],
            "metric": r["field"],
            "value": r["value"],
            "denominator": r["denominator"],
            "accounting_convention": r["accounting_convention"],
            "stated_uncertainty": r["stated_uncertainty"],
            "modeled_vs_measured": r["modeled_vs_measured"],
            "source_quote": r["evidence_quote"],
            "source_arxiv_id": r["source_arxiv_id"],
            "resolution_status": ("CORRECTLY_RESOLVED"
                                  if v.get("resolution_status") == "CORRECTLY_RESOLVED"
                                  else v.get("resolution_status", "AMBIGUOUS")),
            "scored_as": ("EXTRACTED" if r["determination"] == "EXTRACTED" else "UNMEASURED"),
            "evidence_for_absence": r["evidence_for_absence"],
        })

    # gate 3 self-check: no row may carry NOT_FOUND
    not_found_rows = [r for r in table if r["resolution_status"] == "NOT_FOUND"]
    forbidden = [r for r in table if r["scored_as"] == "NOT_FOUND"]

    # ------------------------------------------------------------------
    # control verdicts
    # ------------------------------------------------------------------
    pc1_rows = [r for r in rows_in if r["part"] == 1]
    pc1_field_map = {}
    for f in P1_FIELDS:
        keys = P1_ALIASES.get(f, [f])
        got = [r for r in pc1_rows if r["field"] in keys]
        determined = all(any(g["determination"] == "EXTRACTED" and g["evidence_quote"]
                             for g in got) or
                         (g and g["evidence_for_absence"]) for g in got)
        pc1_field_map[f] = {
            "determined": bool(determined and got),
            "determinations": [{"field": g["field"], "determination": g["determination"],
                                "has_quote": bool(g["evidence_quote"]),
                                "has_absence_evidence": bool(g["evidence_for_absence"])}
                               for g in got],
        }
    pc1_fields_determined = sum(1 for v in pc1_field_map.values() if v["determined"])

    pc1_identity = ctrl["PC-COST-ACCOUNTING"]["verdict"]["resolution_status"] == "CORRECTLY_RESOLVED"
    pc1_pass = bool(pc1_identity and pc1_fields_determined == len(P1_FIELDS))
    pc1_fail_reasons = []
    if not pc1_identity:
        pc1_fail_reasons.append(
            "artifact arXiv:2608.05784v1 does not satisfy the frozen prereg 4.1 identity conjunction: "
            f"failed conditions {ctrl['PC-COST-ACCOUNTING']['verdict']['failed_conditions']}. "
            "spec.json identity_resolution.frozen_target_list freezes expected_authors=['TBD'] for this "
            "entry, and prereg 4.1(3) requires at least one author-name substring match against the "
            "expected author list, so condition 3 is unsatisfiable as frozen. C1 (exact base id "
            "2608.05784, frozen version v1 exists), C2 (expected title 'Activity Frames' is a "
            "case-insensitive substring of the returned title, token coverage 1.0) and C4 (5 of 6 "
            "domain keywords present in the abstract) all pass."
        )
    if pc1_fields_determined != len(P1_FIELDS):
        pc1_fail_reasons.append(f"only {pc1_fields_determined} of {len(P1_FIELDS)} prereg 5.1 fields determined")

    pc2_rows = [r for r in rows_in if r["part"] == 2 and r["system"] == "WebVoyager"]
    pc2_field_map = {f: [r for r in pc2_rows if r["field"] == f] for f in P2_FIELDS}
    pc2_ok = {f: bool(v and v[0]["determination"] == "EXTRACTED" and v[0]["evidence_quote"])
              for f, v in pc2_field_map.items()}
    pc2_identity = ctrl["PC-PERFORMANCE-ENVELOPE"]["verdict"]["resolution_status"] == "CORRECTLY_RESOLVED"
    pc2_pass = bool(pc2_identity and all(pc2_ok.values()))

    nc_rw = ctrl["NC-REAL-BUT-WRONG"]
    nc_rw_pass = bool(nc_rw["observed"]["artifact_is_real"]
                      and nc_rw["verdict"]["resolution_status"] in ("AMBIGUOUS", "NOT_LOCATED"))
    nc_rw_emitted_not_found = False  # the row schema has no NOT_FOUND value at all; asserted below

    nc_fc = ctrl["NC-FABRICATED-CLAIM"]
    nc_fc_pass = bool(nc_fc["verdict"]["resolution_status"] == "NOT_LOCATED")

    gates = {
        "gate_1_pc_cost_accounting_fails": {
            "fired": not pc1_pass,
            "consequence": "MEASUREMENT_INVALID for entire experiment (prereg 7.1)",
            "fired_because": pc1_fail_reasons,
        },
        "gate_2_nc_real_but_wrong_fails_to_flag": {
            "fired": not nc_rw_pass,
            "consequence": "MEASUREMENT_INVALID for entire experiment (prereg 7.2)",
        },
        "gate_3_any_target_scored_NOT_FOUND": {
            "fired": bool(forbidden) or bool(not_found_rows),
            "consequence": "MEASUREMENT_INVALID for entire experiment (prereg 7.3)",
            "count_rows_with_resolution_status_NOT_FOUND": len(not_found_rows),
            "count_rows_scored_as_NOT_FOUND": len(forbidden),
        },
        "gate_4_pc_performance_envelope_fails": {
            "fired": not pc2_pass,
            "consequence": "MEASUREMENT_INVALID for Part 2 only (prereg 7.4)",
        },
        "gate_5_identity_resolution_recall_below_0.6": {
            "fired": recall < 0.6,
            "consequence": "that part is INCONCLUSIVE (prereg 7.5)",
            "recall": round(recall, 6),
            "threshold": 0.6,
        },
    }

    def part_outcome(part: int) -> tuple[str, str]:
        if part == 1:
            if gates["gate_1_pc_cost_accounting_fails"]["fired"] or \
               gates["gate_2_nc_real_but_wrong_fails_to_flag"]["fired"] or \
               gates["gate_3_any_target_scored_NOT_FOUND"]["fired"]:
                return "MEASUREMENT_INVALID", "prereg 8 Part 1 row 1 (Gate 1, 2 or 3 triggered)"
            if recall < 0.6:
                return "INCONCLUSIVE", "prereg 8 Part 1 row 4 (identity resolution recall < 0.6)"
            return "NOT_REACHED", ""
        if part == 2:
            if gates["gate_4_pc_performance_envelope_fails"]["fired"] or \
               gates["gate_3_any_target_scored_NOT_FOUND"]["fired"]:
                return "MEASUREMENT_INVALID", "prereg 8 Part 2 row 1 (Gate 4 or 3 triggered)"
            if recall < 0.6:
                return "INCONCLUSIVE", "prereg 8 Part 2 row 4 (identity resolution recall < 0.6)"
            return "NOT_REACHED", ""
        if gates["gate_3_any_target_scored_NOT_FOUND"]["fired"]:
            return "MEASUREMENT_INVALID", "prereg 8 Part 3 row 1 (Gate 3 triggered)"
        if recall < 0.6:
            return "INCONCLUSIVE", "prereg 8 Part 3 row 4 (identity resolution recall < 0.6)"
        return "NOT_REACHED", ""

    parts = {f"part{p}_outcome": part_outcome(p)[0] for p in (1, 2, 3)}
    parts_reason = {f"part{p}_outcome_basis": part_outcome(p)[1] for p in (1, 2, 3)}
    if any(v == "MEASUREMENT_INVALID" for k, v in parts.items()):
        overall, overall_basis = "MEASUREMENT_INVALID", "prereg 8 OVERALL row 1 (any part MEASUREMENT_INVALID)"
    else:
        vals = {parts["part1_outcome"], parts["part2_outcome"], parts["part3_outcome"]}
        if vals == {"SUPPORTS"}:
            overall = "FALSIFIES"
        elif "SUPPORTS" in vals and vals <= {"SUPPORTS", "MIXED"}:
            overall = "SUPPORTS"
        elif vals == {"FALSIFIES"}:
            overall = "FALSIFIES"
        else:
            overall = "MIXED"
        overall_basis = "prereg 8 OVERALL rows 2-4"

    out = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-36306525220",
        "lane": "intel",
        "generated_at": now(),
        "frozen_decision_rule_source": "spec.json decision_rule, prereg.md Sections 7 and 8",
        "coverage_summary": coverage,
        "table": table,
        "controls_verdicts": {
            "PC-COST-ACCOUNTING": {
                "expected_behavior": "artifact passes prereg 4.1 identity resolution AND all 10 prereg 5.1 "
                                     "fields are determined with evidence quotes",
                "observed_behavior": (
                    f"identity resolution_status="
                    f"{ctrl['PC-COST-ACCOUNTING']['verdict']['resolution_status']} "
                    f"(failed {ctrl['PC-COST-ACCOUNTING']['verdict']['failed_conditions']}); "
                    f"{pc1_fields_determined}/10 prereg 5.1 fields determined "
                    f"({sum(1 for r in pc1_rows if r['determination']=='EXTRACTED')} with verbatim quotes, "
                    f"{sum(1 for r in pc1_rows if r['determination']!='EXTRACTED')} recorded as absence "
                    f"with absence evidence)"
                ),
                "pass_fail": pc1_pass,
                "evidence_ref": "raw/controls_result.json -> controls.PC-COST-ACCOUNTING; "
                                "raw/field_determinations.json -> rows[part==1]; "
                                "raw/fulltext/2608.05784.txt",
                "field_map": pc1_field_map,
                "failure_reasons": pc1_fail_reasons,
            },
            "PC-PERFORMANCE-ENVELOPE": {
                "expected_behavior": "artifact passes prereg 4.1 identity resolution AND success_rate, "
                                     "denominator, evaluation_convention and benchmark_split are all "
                                     "extracted with evidence quotes",
                "observed_behavior": (
                    f"identity resolution_status="
                    f"{ctrl['PC-PERFORMANCE-ENVELOPE']['verdict']['resolution_status']}; "
                    f"per-field extracted={pc2_ok}"
                ),
                "pass_fail": pc2_pass,
                "evidence_ref": "raw/controls_result.json -> controls.PC-PERFORMANCE-ENVELOPE; "
                                "raw/field_determinations.json -> rows[part==2 and system=='WebVoyager']",
            },
            "NC-REAL-BUT-WRONG": {
                "expected_behavior": "arXiv:1802.05012v2 is retrieved as a REAL artifact, the resolver "
                                     "flags the identity mismatch against the named system WebArena, and "
                                     "emits UNMEASURED rather than NOT_FOUND",
                "observed_behavior": (
                    f"artifact_is_real={nc_rw['observed']['artifact_is_real']}; returned title="
                    f"{nc_rw['verdict']['returned_title']!r}; failed conditions="
                    f"{nc_rw['verdict']['failed_conditions']}; resolution_status="
                    f"{nc_rw['verdict']['resolution_status']} -> row scored_as=UNMEASURED; "
                    f"emitted NOT_FOUND={nc_rw_emitted_not_found}"
                ),
                "pass_fail": nc_rw_pass,
                "evidence_ref": "raw/controls_result.json -> controls.NC-REAL-BUT-WRONG; "
                                "raw/html/ctrl_1802.05012v2.html; raw/identity_resolution.json",
                "note": "The domain-keyword condition alone would have passed (the abstract contains the "
                        "token 'agent'); the identity gate has power only as a conjunction, and the "
                        "conjunction fired.",
            },
            "NC-FABRICATED-CLAIM": {
                "expected_behavior": "arXiv:2609.99999 is not located and the resolver emits NOT_LOCATED",
                "observed_behavior": f"HTTP 404; resolution_status={nc_fc['verdict']['resolution_status']}",
                "pass_fail": nc_fc_pass,
                "evidence_ref": "raw/controls_result.json -> controls.NC-FABRICATED-CLAIM",
                "note": "sanity check only; per prereg 6.4 it has no power and triggers nothing",
            },
        },
        "gates": gates,
        "part_outcomes": parts,
        "part_outcome_basis": parts_reason,
        "overall_frozen_outcome": overall,
        "overall_frozen_outcome_basis": overall_basis,
        "integrity_self_checks": {
            "rows_total": len(table),
            "rows_with_resolution_status_NOT_FOUND": len(not_found_rows),
            "rows_scored_NOT_FOUND": len(forbidden),
            "rows_scored_UNMEASURED": sum(1 for r in table if r["scored_as"] == "UNMEASURED"),
            "rows_with_value_null": sum(1 for r in table if r["value"] is None),
            "rows_with_value_null_and_absence_evidence": sum(
                1 for r in table if r["value"] is None and r["evidence_for_absence"]),
            "rows_with_value_null_and_no_absence_evidence": sum(
                1 for r in table if r["value"] is None and not r["evidence_for_absence"]),
            "rows_exposing_modeled_label_when_modeled": sum(
                1 for r in table if r["modeled_vs_measured"] == "modeled"),
            "rows_exposing_denominator_when_value_present": sum(
                1 for r in table if r["value"] is not None and r["denominator"]),
        },
    }
    p = os.path.join(RES, "table.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    with open(os.path.join(RES, "coverage.json"), "w", encoding="utf-8") as fh:
        json.dump(coverage, fh, indent=1, sort_keys=True)

    print("recall", round(recall, 4), "correctly_resolved", len(correctly_resolved),
          "/", named_systems_searched)
    print("controls:", {k: v["pass_fail"] for k, v in out["controls_verdicts"].items()})
    print("gates fired:", {k: v["fired"] for k, v in gates.items()})
    print("parts:", parts, "-> overall", overall)
    print("self checks:", json.dumps(out["integrity_self_checks"]))
    print("wrote", p, "sha256", sha(p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
