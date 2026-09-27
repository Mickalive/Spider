#!/usr/bin/env python3
"""EXP-INTEL-36306525220 :: Stage 5 -- packet contract self-validation.

Checks the produced artifacts against the shapes that research/EXPERIMENT_PACKET.md
and spec.json output_contract require, so the producer does not ship a malformed
packet.  This is a producer self-check, NOT the independent audit.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SPEC_ROW_KEYS = {"part", "system", "benchmark", "metric", "value", "denominator",
                 "accounting_convention", "stated_uncertainty", "modeled_vs_measured",
                 "source_quote", "source_arxiv_id", "resolution_status", "evidence_for_absence"}
RESOLUTION_VALUES = {"CORRECTLY_RESOLVED", "AMBIGUOUS", "NOT_LOCATED", "UNMEASURED"}
MVM_VALUES = {"modeled", "measured", "not_reported", None}
RESULT_KEYS = ["schema_version", "experiment_id", "lane", "status", "outcome", "metrics",
               "controls", "artifacts", "observations", "validity_notes", "unresolved"]
STATUS_VALUES = {"COMPLETE", "BLOCKED", "MEASUREMENT_INVALID"}
OUTCOME_VALUES = {"SUPPORTS", "FALSIFIES", "MIXED", "INCONCLUSIVE", "NOT_APPLICABLE"}
PROV_KEYS = ["schema_version", "experiment_id", "lane"]


def main() -> int:
    fails: list[str] = []
    warns: list[str] = []

    spec = json.load(open(os.path.join(HERE, "spec.json"), encoding="utf-8"))
    res = os.path.join(HERE, "results", "table.json")
    tab = json.load(open(res, encoding="utf-8"))

    # --- spec output_contract row schema ---
    for i, row in enumerate(tab["table"]):
        missing = SPEC_ROW_KEYS - set(row)
        if missing:
            fails.append(f"table row {i} missing mandatory spec.json output_contract keys: {sorted(missing)}")
        if row.get("resolution_status") not in RESOLUTION_VALUES:
            fails.append(f"table row {i} resolution_status not in spec enum: {row.get('resolution_status')!r}")
        if row.get("resolution_status") == "NOT_FOUND":
            fails.append(f"table row {i} violates spec 'No row may have resolution_status=NOT_FOUND'")
        if row.get("modeled_vs_measured") not in MVM_VALUES:
            fails.append(f"table row {i} modeled_vs_measured outside spec enum: {row.get('modeled_vs_measured')!r}")
        if row.get("value") is None and not row.get("evidence_for_absence"):
            fails.append(f"table row {i} has value=null with no evidence_for_absence")
        if row.get("modeled_vs_measured") == "modeled" and not (
                row.get("accounting_convention") or "").strip():
            fails.append(f"table row {i} labeled modeled without an accounting_convention")

    # --- frozen metrics required by prereg 9.2 ---
    result_path = os.path.join(HERE, "result.json")
    if not os.path.exists(result_path):
        fails.append("result.json not yet written")
    else:
        r = json.load(open(result_path, encoding="utf-8"))
        for k in RESULT_KEYS:
            if k not in r:
                fails.append(f"result.json missing mandatory top-level key {k!r} (EXPERIMENT_PACKET section 4)")
        if r.get("status") not in STATUS_VALUES:
            fails.append(f"result.json status {r.get('status')!r} outside contract enum")
        if r.get("outcome") not in OUTCOME_VALUES:
            fails.append(f"result.json outcome {r.get('outcome')!r} outside contract enum")
        for k in ("part1_outcome", "part2_outcome", "part3_outcome", "overall_outcome",
                  "identity_resolution_recall_part1", "identity_resolution_recall_part2",
                  "identity_resolution_recall_part3", "pc_cost_accounting_pass",
                  "pc_performance_envelope_pass", "nc_real_but_wrong_pass",
                  "nc_fabricated_claim_pass", "coverage_summary", "artifact_table_path"):
            if k not in r.get("metrics", {}):
                fails.append(f"result.json metrics missing prereg 9.2 key {k!r}")
        for cid in ("PC-COST-ACCOUNTING", "PC-PERFORMANCE-ENVELOPE", "NC-REAL-BUT-WRONG",
                    "NC-FABRICATED-CLAIM"):
            e = r.get("controls", {}).get(cid)
            if e is None:
                fails.append(f"result.json controls missing frozen control id {cid!r}")
            else:
                for k in ("expected_behavior", "observed_behavior", "pass_fail", "evidence_ref"):
                    if k not in e:
                        fails.append(f"result.json controls[{cid}] missing prereg 9.3 key {k!r}")
        if not r.get("artifacts"):
            fails.append("result.json artifacts is empty")
        for a in r.get("artifacts", []):
            if "path" not in a or "role" not in a:
                fails.append(f"result.json artifact entry lacks path/role: {a!r}")
            if "sha256" not in a:
                warns.append(f"artifact without sha256: {a.get('path')!r}")
        for k in ("observations", "validity_notes", "unresolved"):
            if not isinstance(r.get(k), list):
                fails.append(f"result.json {k} must be a list")
        if r.get("outcome") == "NOT_APPLICABLE" and r.get("status") != "MEASUREMENT_INVALID":
            warns.append("outcome=NOT_APPLICABLE with a status other than MEASUREMENT_INVALID")

    # --- provenance ---
    prov_path = os.path.join(HERE, "provenance.json")
    if not os.path.exists(prov_path):
        fails.append("provenance.json not yet written")
    else:
        pv = json.load(open(prov_path, encoding="utf-8"))
        for k in PROV_KEYS:
            if k not in pv:
                fails.append(f"provenance.json missing {k!r}")
        if "deviations_from_frozen_design" not in pv:
            fails.append("provenance.json missing deviations_from_frozen_design (prereg section 14)")

    # --- report ---
    if not os.path.exists(os.path.join(HERE, "report.md")):
        fails.append("report.md not yet written")

    # --- immutability of frozen inputs ---
    import hashlib
    fr = json.load(open(os.path.join(HERE, "freeze.json"), encoding="utf-8"))
    for name, want in fr["hashes"].items():
        got = hashlib.sha256(open(os.path.join(HERE, name), "rb").read()).hexdigest()
        if got != want:
            fails.append(f"FROZEN INPUT MUTATED: {name} sha256 {got} != frozen {want}")

    print("=" * 78)
    for w in warns:
        print("WARN ", w)
    for f in fails:
        print("FAIL ", f)
    print(f"contract self-validation: {len(fails)} failures, {len(warns)} warnings")
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
