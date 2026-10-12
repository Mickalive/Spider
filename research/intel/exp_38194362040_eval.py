#!/usr/bin/env python3
"""EXECUTE evaluator for EXP-INTEL-38194362040 (intel lane, frozen design).

Implements prereg.md section 7. Pure deterministic function of the frozen
preflight/controls records, the per-candidate provisioning receipts, the frozen
runner's per-candidate model_receipts.json, the endpoint census and the
external-comparator table. Makes no model calls and has no free parameters.
Writes raw/decision.json with the frozen metrics/controls/disposition and the
computed section-7 OUTCOME / B3_STATUS.

Frozen decision rule:
  rule1 preflight (five checks) -> rule2 endpoint census (non-gating) ->
  rule3 ladder [M-14B-QWEN, M-8B-LLAMA] with early stop on first CLEARS ->
  rule4 after ladder: measured (COMPLETE, not CLEARS) empty -> MEASUREMENT_INVALID;
       else FALSIFIES and B3_STATUS=NOT_SATISFIED iff all hosted providers are
       CREDENTIAL_REQUIRED/UNREACHABLE/CREDENTIAL_FREE_OPERATIONALLY_CAPPED else UNRESOLVED.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38194362040")

CANDIDATES = ["M-14B-QWEN", "M-8B-LLAMA"]
EPISODES_REQUIRED = 5
TSR_BAR = 0.6
PARSE_BAR = 0.6
NON_PROVISIONABLE = {"CREDENTIAL_REQUIRED", "UNREACHABLE", "CREDENTIAL_FREE_OPERATIONALLY_CAPPED"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def cell_metrics(receipts):
    """Compute metrics for one loaded candidate cell from its model receipt."""
    eps = receipts.get("episodes", []) or []
    pc = receipts.get("positive_control") or {}
    n = len(eps)
    parse_step1 = [1 if e.get("step1_parse_ok") else 0 for e in eps]
    success = [1 if e.get("task_success") else 0 for e in eps]
    answer_emitted = []
    lat, toks = [], []
    for e in eps:
        has_answer = any((s.get("action") or {}).get("action") == "answer" and s.get("parse_ok")
                         for s in (e.get("steps") or []))
        answer_emitted.append(1 if has_answer else 0)
        for s in (e.get("steps") or []):
            if s.get("latency_s") is not None:
                lat.append(s["latency_s"])
            if s.get("completion_tokens") is not None:
                toks.append(s["completion_tokens"])
    pc_probes = pc.get("probes", []) or []
    for p in pc_probes:
        if p.get("latency_s") is not None:
            lat.append(p["latency_s"])
        if p.get("completion_tokens") is not None:
            toks.append(p["completion_tokens"])

    def frac(xs):
        return (sum(xs) / len(xs)) if xs else None

    return {
        "positive_control_pass_rate": pc.get("pass_rate"),
        "positive_control_n_pass": pc.get("n_pass"),
        "positive_control_n_total": pc.get("n_total"),
        "parseable_action_rate_step1": frac(parse_step1),
        "answer_action_emission_rate": frac(answer_emitted),
        "task_success_rate": frac(success),
        "mean_inference_latency_s": (round(sum(lat) / len(lat), 3) if lat else None),
        "mean_completion_tokens": (round(sum(toks) / len(toks), 2) if toks else None),
        "n_episodes": n,
        "n_calls_latency": len(lat),
        "n_calls_tokens": len(toks),
    }


def main():
    preflight = load_json(os.path.join(EXP, "raw", "preflight.json"), {})
    controls = load_json(os.path.join(EXP, "raw", "controls.json"), {})
    census = load_json(os.path.join(EXP, "raw", "endpoint_census.json"), {"providers": [], "counts": {},
                                                                          "any_provisionable_credentialed": False})
    comparators = load_json(os.path.join(EXP, "raw", "external_comparators.json"), {})
    prov = load_json(os.path.join(EXP, "raw", "provisioning_evidence.json"), {"candidates": []})

    checks = preflight.get("checks", {})
    preflight_ok = bool(preflight.get("pass")) and all([
        checks.get("PC_ORACLE_EPISODE_5of5"),
        checks.get("NC_parseable_0_and_success_0"),
        checks.get("B_RANDOM_parseable_1_and_success_lt_0.6"),
        checks.get("freeze_artifact_hashes_match"),
        checks.get("required_stack_imports_ok"),
    ])

    cells = {}
    decision_trace = []
    outcome = status = b3 = None
    early_stop_candidate = None

    if not preflight_ok:
        outcome, status, b3 = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID", "UNRESOLVED"
        decision_trace.append("rule1_preflight_failed")
    else:
        decision_trace.append("rule1_preflight_pass")
        decision_trace.append(
            "rule2_endpoint_census_recorded_non_gating:providers=%d provisionable_credentialed=%d" % (
                len(census.get("providers", [])), census.get("counts", {}).get("PROVISIONABLE_CREDENTIATED", 0)))
        # rule3 ladder
        for cid in CANDIDATES:
            cell = {"candidate_id": cid}
            cell_dir = os.path.join(EXP, "cells", cid)
            prov_rec = load_json(os.path.join(cell_dir, "raw", "provisioning_receipt.json"), {})
            receipts_path = os.path.join(cell_dir, "raw", "model_receipts.json")
            model_receipts = load_json(receipts_path, None)
            receipt = None
            if isinstance(model_receipts, list):
                for r in model_receipts:
                    if r.get("candidate_id") == cid:
                        receipt = r
            # identity
            identity_pass = bool(prov_rec.get("identity_pass"))
            cell["identity_pass"] = identity_pass
            cell["provisioning_receipt_path"] = os.path.relpath(
                os.path.join(cell_dir, "raw", "provisioning_receipt.json"), REPO)
            cell["observed_sha256"] = prov_rec.get("observed_sha256")
            cell["observed_bytes"] = prov_rec.get("observed_bytes")
            if not identity_pass:
                cell["cell_state"] = "UNMEASURED_LOAD_FAILED"
                cell["reason"] = "frozen step 3a: served-body content identity did not match frozen pins; no load attempted"
                cell["load_attempted"] = False
                cell["metrics"] = None
                cells[cid] = cell
                decision_trace.append("rule3a_identity_fail:%s=UNMEASURED_LOAD_FAILED" % cid)
                continue
            if receipt is None:
                cell["cell_state"] = "UNMEASURED_LOAD_FAILED"
                cell["reason"] = "no model receipt present (frozen runner not executed for this candidate)"
                cell["load_attempted"] = False
                cell["metrics"] = None
                cells[cid] = cell
                decision_trace.append("rule3_no_receipt:%s=UNMEASURED_LOAD_FAILED" % cid)
                continue
            load_status = receipt.get("load_status")
            cell["load_status"] = load_status
            cell["load_error"] = receipt.get("load_error")
            cell["load_time_s"] = receipt.get("load_time_s")
            cell["run_status"] = receipt.get("run_status")
            if load_status != "LOADED":
                cell["cell_state"] = "UNMEASURED_LOAD_FAILED"
                cell["reason"] = "model failed to load: %s" % (receipt.get("load_error") or load_status)
                cell["load_attempted"] = True
                cell["metrics"] = None
                cells[cid] = cell
                decision_trace.append("rule3b_load_failed:%s=UNMEASURED_LOAD_FAILED" % cid)
                continue
            pc = receipt.get("positive_control") or {}
            m = cell_metrics(receipt)
            cell["load_attempted"] = True
            cell["model_receipt_path"] = os.path.relpath(receipts_path, REPO)
            if not pc.get("pass"):
                cell["cell_state"] = "UNMEASURED_TREATMENT_PC_FAILED"
                cell["reason"] = "positive-control constrained-decoding gate did not pass (%s/%s)" % (
                    pc.get("n_pass"), pc.get("n_total"))
                cell["metrics"] = m
                cells[cid] = cell
                decision_trace.append("rule3c_pc_fail:%s=UNMEASURED_TREATMENT_PC_FAILED" % cid)
                continue
            if m["n_episodes"] == EPISODES_REQUIRED:
                cell["cell_state"] = "COMPLETE"
                clears = (m["task_success_rate"] is not None and m["task_success_rate"] >= TSR_BAR
                          and m["parseable_action_rate_step1"] is not None and m["parseable_action_rate_step1"] >= PARSE_BAR)
                cell["clears"] = clears
                cell["metrics"] = m
                cells[cid] = cell
                decision_trace.append("rule3c_complete:%s tsr=%s parse=%s clears=%s" % (
                    cid, m["task_success_rate"], m["parseable_action_rate_step1"], clears))
                if clears:
                    early_stop_candidate = cid
                    decision_trace.append("rule3d_clears:%s->SUPPORTS (early stop)" % cid)
                    break
                decision_trace.append("rule3e_fails_bar:%s=TREATMENT_FAILS_BAR" % cid)
            else:
                cell["cell_state"] = "PARTIAL"
                cell["reason"] = "PC passed but %d/%d episode records present" % (m["n_episodes"], EPISODES_REQUIRED)
                cell["metrics"] = m
                cells[cid] = cell
                decision_trace.append("rule3c_partial:%s n_episodes=%d" % (cid, m["n_episodes"]))

        # rule4 / SUPPORTS
        if early_stop_candidate is not None:
            outcome, status, b3 = "SUPPORTS", "COMPLETE", "SATISFIED"
        else:
            measured = [cid for cid, c in cells.items() if c.get("cell_state") == "COMPLETE" and not c.get("clears")]
            if not measured:
                outcome, status, b3 = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID", "UNRESOLVED"
                decision_trace.append("rule4_no_complete_cell->MEASUREMENT_INVALID")
            else:
                classes = {p.get("classification") for p in census.get("providers", [])}
                if classes and classes <= NON_PROVISIONABLE:
                    b3 = "NOT_SATISFIED"
                else:
                    b3 = "UNRESOLVED"
                outcome, status = "FALSIFIES", "COMPLETE"
                decision_trace.append("rule4_complete_cells_no_clear->FALSIFIES b3=%s" % b3)

    # control records for result.json.controls
    def ctrl_summary(cid):
        c = controls.get(cid, {})
        if not c:
            return {"present": False}
        out = {"present": True}
        if "task_success_rate" in c:
            out["task_success_rate"] = c["task_success_rate"]
        if "parseable_action_rate_step1" in c:
            out["parseable_action_rate_step1"] = c["parseable_action_rate_step1"]
        return out

    decision = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38194362040",
        "lane": "intel",
        "outcome": outcome,
        "status": status,
        "b3_status": b3,
        "preflight_pass": preflight_ok,
        "preflight_checks": checks,
        "decision_trace": decision_trace,
        "early_stop_candidate": early_stop_candidate,
        "cells": cells,
        "cell_order": CANDIDATES,
        "capability_bar": {"task_success_rate": TSR_BAR, "parseable_action_rate_step1": PARSE_BAR, "episodes": EPISODES_REQUIRED},
        "controls": {
            "PC-ORACLE-EPISODE": ctrl_summary("PC-ORACLE-EPISODE"),
            "NC-NO-MODEL-ACTION": ctrl_summary("NC-NO-MODEL-ACTION"),
            "B-RANDOM-ACTION": ctrl_summary("B-RANDOM-ACTION"),
        },
        "census_counts": census.get("counts", {}),
        "any_provisionable_credentialed": census.get("any_provisionable_credentialed", False),
        "comparators_enumerated": comparators.get("comparators_enumerated"),
        "comparators_not_pinned": comparators.get("comparators_not_pinned"),
        "provisioning_candidates": [
            {"candidate_id": e.get("candidate_id"), "identity_pass": e.get("identity_pass"),
             "observed_sha256": e.get("observed_sha256"), "observed_bytes": e.get("observed_bytes"),
             "n_download_attempts": e.get("n_download_attempts")}
            for e in prov.get("candidates", [])
        ],
    }
    with open(os.path.join(EXP, "raw", "decision.json"), "w") as f:
        json.dump(decision, f, indent=2, sort_keys=True)
    print(json.dumps({"outcome": outcome, "status": status, "b3_status": b3,
                      "early_stop": early_stop_candidate, "trace": decision_trace}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
