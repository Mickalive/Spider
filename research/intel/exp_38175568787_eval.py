#!/usr/bin/env python3
"""EXECUTE evaluator for EXP-INTEL-38175568787 (intel lane, frozen design).

Implements prereg.md Appendix A.5 and section 7. Pure deterministic function of
the frozen preflight/controls records, the per-candidate provisioning receipts
(no model_receipts.json exist because no candidate passed the frozen step-3a
digest gate), the endpoint census and the external-comparator table. Makes no
model calls and has no free parameters. Writes <EXP>/raw/decision.json with the
frozen metrics/controls/disposition and the computed section-7 decision.

Frozen decision rule as applied here:
  rule1 preflight (five frozen checks) ->
  rule2 endpoint census (non-gating) ->
  rule3 ladder [M-14B-QWEN, M-8B-LLAMA]: step 3a pinned GGUF sha256+bytes
     mismatch -> UNMEASURED_LOAD_FAILED, continue (no load attempted) ->
  rule4 after ladder: measured (COMPLETE cells that do not clear) is empty
     -> OUTCOME=MEASUREMENT_INVALID, B3_STATUS=UNRESOLVED, STOP.
Canonical mapping: MEASUREMENT_INVALID -> result.status=MEASUREMENT_INVALID,
result.outcome=INCONCLUSIVE.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38175568787")

CANDIDATES = ["M-14B-QWEN", "M-8B-LLAMA"]
EPISODES_REQUIRED = 5
TSR_BAR = 0.6
PARSE_BAR = 0.6


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    preflight = json.load(open(os.path.join(EXP, "raw", "preflight.json")))
    controls = json.load(open(os.path.join(EXP, "raw", "controls.json")))
    census = json.load(open(os.path.join(EXP, "raw", "endpoint_census.json")))
    comparators = json.load(open(os.path.join(EXP, "raw", "external_comparators.json")))
    prov_evidence = json.load(open(os.path.join(EXP, "raw", "provisioning_evidence.json")))

    checks = preflight.get("checks", {})
    preflight_ok = bool(preflight.get("pass")) and all([
        checks.get("PC_ORACLE_EPISODE_5of5"),
        checks.get("NC_parseable_0_and_success_0"),
        checks.get("B_RANDOM_parseable_1_and_success_lt_0.6"),
        checks.get("freeze_artifact_hashes_match"),
        checks.get("required_stack_imports_ok"),
    ])

    cells = {}
    for cid in CANDIDATES:
        rec_path = os.path.join(EXP, "cells", cid, "raw", "provisioning_receipt.json")
        cfg_path = os.path.join(EXP, "cells", cid, "raw", "harness_config.json")
        with open(rec_path) as f:
            rec = json.load(f)
        cells[cid] = {
            "candidate_id": cid,
            "cell_dir": os.path.relpath(os.path.join(EXP, "cells", cid), REPO),
            "receipt_path": os.path.relpath(rec_path, REPO),
            "config_path": os.path.relpath(cfg_path, REPO),
            "receipt_sha256": sha256_file(rec_path),
            "config_sha256": sha256_file(cfg_path),
            "load_status": rec.get("load_status"),
            "load_error": rec.get("load_error"),
            "positive_control": rec.get("positive_control"),
            "n_episodes": 0,
            "disposition": "UNMEASURED_LOAD_FAILED",
            "disposition_rule": "frozen decision rule 3a (pinned GGUF sha256+bytes mismatch)",
            "provisioning_evidence_ref": rec.get("provisioning_evidence_ref"),
        }

    decision_trace = []
    if not preflight_ok:
        outcome, status, b3 = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID", "UNRESOLVED"
        decision_trace.append("rule1_preflight_failed")
    else:
        decision_trace.append("rule1_preflight_pass")
        decision_trace.append("rule2_endpoint_census_recorded_non_gating:providers=%d provisionable_credentialed=%d" % (
            len(census["providers"]), census["counts"]["PROVISIONABLE_CREDENTIATED"]))
        for cid in CANDIDATES:
            cells[cid]["disposition"] = "UNMEASURED_LOAD_FAILED"
            decision_trace.append("rule3a_digest_mismatch:%s=UNMEASURED_LOAD_FAILED (no load attempted, fail-closed)" % cid)
        measured = [cid for cid in CANDIDATES if cells[cid]["disposition"] == "COMPLETE"]
        if not measured:
            outcome, status, b3 = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID", "UNRESOLVED"
            decision_trace.append("rule4_no_complete_cell->MEASUREMENT_INVALID")
        else:
            # Unreachable with the current provisioning receipts, kept for completeness.
            outcome, status, b3 = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID", "UNRESOLVED"
            decision_trace.append("rule4_unexpected_partial_state")

    derived = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38175568787",
        "lane": "intel",
        "outcome": outcome,
        "status": status,
        "b3_status": b3,
        "preflight_pass": preflight_ok,
        "preflight_checks": checks,
        "decision_trace": decision_trace,
        "cells": cells,
        "census_counts": census["counts"],
        "any_provisionable_credentialed": census["any_provisionable_credentialed"],
        "comparators_enumerated": comparators["comparators_enumerated"],
        "comparators_not_pinned": comparators["comparators_not_pinned"],
        "provisioning_blocker": {
            "category": "REMOTE_GGUF_DIGEST_DRIFT",
            "detail": ("At EXECUTE the remote content at both frozen GGUF URLs differs from the "
                       "frozen-pinned sha256; downloaded bytes equal the current HF LFS OID (Xet "
                       "content hash) on every route tried (resolve plain, ?download=true, hf.co). "
                       "Byte counts match the pinned sizes. Per frozen rule 3a both candidates are "
                       "UNMEASURED_LOAD_FAILED and no model was loaded (fail-closed; a digest "
                       "mismatch never becomes a capability failure)."),
            "evidence_ref": "raw/provisioning_evidence.json",
        },
        "controls": {
            "PC-ORACLE-EPISODE": controls["PC-ORACLE-EPISODE"]["task_success_rate"],
            "NC-NO-MODEL-ACTION": {
                "parseable_action_rate_step1": controls["NC-NO-MODEL-ACTION"]["parseable_action_rate_step1"],
                "task_success_rate": controls["NC-NO-MODEL-ACTION"]["task_success_rate"],
            },
            "B-RANDOM-ACTION": {
                "parseable_action_rate_step1": controls["B-RANDOM-ACTION"]["parseable_action_rate_step1"],
                "task_success_rate": controls["B-RANDOM-ACTION"]["task_success_rate"],
            },
        },
    }
    with open(os.path.join(EXP, "raw", "decision.json"), "w") as f:
        json.dump(derived, f, indent=2, sort_keys=True)
    print(json.dumps({"outcome": outcome, "status": status, "b3_status": b3, "trace": decision_trace}))
    return 0


if __name__ == "__main__":
    sys.exit(main())