#!/usr/bin/env python3
"""EXECUTE evaluator for EXP-INTEL-38164607941 (intel lane, frozen design).

Implements prereg.md Appendix A.5 and section 7. It is a pure deterministic
function of the frozen per-cell raw receipts (raw/model_receipts.json) plus the
preflight/controls records; it makes no model calls and has no free parameters.
It writes <EXP>/raw/decision.json with the frozen metrics/controls/disposition
and the computed section-7 decision. The producer then assembles the canonical
result.json/report.md/provenance.json from this derived record.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38164607941")
PARENT_RESULT = os.path.join(REPO, "research", "experiments", "EXP-INTEL-37982024058", "result.json")

CANDIDATES = ["M-7B-QWEN", "M-3B-QWEN"]
CONDITIONS = ["P-TREAT-GOAL-SCHEMA", "P-COMP-UNDERSPECIFIED"]
TREAT = "P-TREAT-GOAL-SCHEMA"
COMP = "P-COMP-UNDERSPECIFIED"
EPISODES_REQUIRED = 5
TSR_BAR = 0.6
PARSE_BAR = 0.6


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def cell_path(candidate, condition):
    return os.path.join(EXP, "cells", candidate, condition)


def load_cell(candidate, condition):
    cd = cell_path(candidate, condition)
    rec_path = os.path.join(cd, "raw", "model_receipts.json")
    cfg_path = os.path.join(cd, "raw", "harness_config.json")
    info = {
        "cell": "%s|%s" % (candidate, condition),
        "candidate": candidate,
        "condition": condition,
        "cell_dir": os.path.relpath(cd, REPO),
        "receipt_path": os.path.relpath(rec_path, REPO) if os.path.exists(rec_path) else None,
        "config_path": os.path.relpath(cfg_path, REPO) if os.path.exists(cfg_path) else None,
        "exists": os.path.exists(rec_path),
    }
    if not os.path.exists(rec_path):
        info["status"] = "MISSING"
        return info
    info["receipt_sha256"] = sha256_file(rec_path)
    info["config_sha256"] = sha256_file(cfg_path) if os.path.exists(cfg_path) else None
    with open(rec_path) as f:
        receipts = json.load(f)
    # the runner appends one receipt per candidate to this list
    rec = None
    for r in receipts:
        if r.get("candidate_id") == candidate:
            rec = r
    if rec is None:
        info["status"] = "MISSING_RECEIPT_FOR_CANDIDATE"
        return info
    info["load_status"] = rec.get("load_status")
    info["run_status"] = rec.get("run_status")
    info["load_error"] = rec.get("load_error")
    info["run_error"] = rec.get("run_error")
    info["positive_control"] = rec.get("positive_control")
    info["positive_control_excluded"] = rec.get("positive_control_excluded", False)
    episodes = rec.get("episodes") or []
    info["n_episodes"] = len(episodes)
    info["episodes"] = episodes
    info["config_sampling"] = rec.get("config_sampling")
    return info


def cell_metrics(info):
    if not info.get("exists"):
        return None
    pc = info.get("positive_control")
    episodes = info.get("episodes") or []
    pc_pass = bool(pc and pc.get("pass") and pc.get("pass_rate") == 1.0)
    n = len(episodes)
    if n > 0:
        parse1 = sum(1 for e in episodes if e.get("step1_parse_ok")) / n
        answer_emit = sum(
            1 for e in episodes
            if any((s.get("parse_ok") and s.get("action", {}).get("action") == "answer") for s in (e.get("steps") or []))
        ) / n
        tsr = sum(1 for e in episodes if e.get("task_success")) / n
    else:
        parse1 = answer_emit = tsr = None

    lat = []
    toks = []
    if pc:
        for p in pc.get("probes", []):
            if p.get("latency_s") is not None:
                lat.append(p["latency_s"])
            toks.append(p.get("completion_tokens", 0))
    for e in episodes:
        for s in (e.get("steps") or []):
            if s.get("latency_s") is not None:
                lat.append(s["latency_s"])
            toks.append(s.get("completion_tokens", 0))

    m = {
        "positive_control_pass_rate": {"value": pc.get("pass_rate") if pc else None,
                                       "k": pc.get("n_pass") if pc else None,
                                       "n": pc.get("n_total") if pc else None,
                                       "unit": "fraction"},
        "parseable_action_rate_step1": {"value": parse1,
                                        "k": sum(1 for e in episodes if e.get("step1_parse_ok")) if n else None,
                                        "n": n if n else None, "unit": "fraction"},
        "answer_action_emission_rate": {"value": answer_emit,
                                        "k": sum(1 for e in episodes if any((s.get("parse_ok") and s.get("action", {}).get("action") == "answer") for s in (e.get("steps") or []))) if n else None,
                                        "n": n if n else None, "unit": "fraction"},
        "task_success_rate": {"value": tsr,
                              "k": sum(1 for e in episodes if e.get("task_success")) if n else None,
                              "n": n if n else None, "unit": "fraction"},
        "mean_inference_latency_s": {"value": round(sum(lat) / len(lat), 4) if lat else None,
                                     "n_calls": len(lat), "unit": "s"},
        "mean_completion_tokens": {"value": round(sum(toks) / len(toks), 4) if toks else None,
                                   "n_calls": len(toks), "unit": "tokens"},
        "pc_gate_passed": pc_pass,
        "n_episodes": n,
    }
    return m


def disposition(m):
    if m is None:
        return "MISSING"
    if m.get("load_status") not in (None, "LOADED"):
        return "OPERATIONAL_FAILURE"
    if not m["pc_gate_passed"]:
        return "EXCLUDED"
    if m["n_episodes"] < EPISODES_REQUIRED:
        return "PARTIAL"
    if m["n_episodes"] == EPISODES_REQUIRED:
        return "COMPLETE"
    return "PARTIAL"


def main():
    preflight = json.load(open(os.path.join(EXP, "raw", "preflight.json")))
    controls = json.load(open(os.path.join(EXP, "raw", "controls.json")))
    parent = json.load(open(PARENT_RESULT))

    cells = {}
    for cand in CANDIDATES:
        for cond in CONDITIONS:
            info = load_cell(cand, cond)
            m = cell_metrics(info)
            d = disposition({**(info or {}), **(m or {})})
            cells["%s|%s" % (cand, cond)] = {
                "candidate": cand, "condition": cond, "info": info, "metrics": m, "disposition": d,
            }

    # preflight checks (rule 1)
    checks = preflight.get("checks", {})
    preflight_ok = bool(preflight.get("pass")) and all([
        checks.get("PC_ORACLE_EPISODE_5of5"),
        checks.get("NC_parseable_0_and_success_0"),
        checks.get("B_RANDOM_parseable_1_and_success_lt_0.6"),
        checks.get("freeze_artifact_hashes_match"),
        checks.get("required_stack_imports_ok"),
        checks.get("gguf_digest_checks_pass"),
    ])

    decision_trace = []
    outcome = None
    status = None
    result_notes = {}
    if not preflight_ok:
        outcome, status = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID"
        decision_trace.append("rule1_preflight_failed")
    else:
        decision_trace.append("rule1_preflight_pass")
        for cand in CANDIDATES:
            tkey = "%s|%s" % (cand, TREAT)
            ckey = "%s|%s" % (cand, COMP)
            tc = cells[tkey]
            cc = cells[ckey]
            td, cd = tc["disposition"], cc["disposition"]
            tm, cm = tc["metrics"], cc["metrics"]
            decision_trace.append("rule2a_run_pair:%s treat=%s comp=%s" % (cand, td, cd))
            if td == "OPERATIONAL_FAILURE" or cd == "OPERATIONAL_FAILURE":
                decision_trace.append("rule2b_operational_failure:%s" % cand)
                outcome, status = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID"
                break
            if td == "EXCLUDED":
                tc["disposition_label"] = "UNMEASURED_TREATMENT_PC_FAILED"
                decision_trace.append("rule2b_treat_excluded:%s" % cand)
                continue
            if td == "PARTIAL" or cd == "PARTIAL":
                decision_trace.append("rule2c_partial:%s" % cand)
                outcome, status = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID"
                break
            if cd == "CONFOUND" or (cm and (cm["task_success_rate"]["value"] >= TSR_BAR or cm["parseable_action_rate_step1"]["value"] < PARSE_BAR)):
                decision_trace.append("rule2d_comp_confound:%s" % cand)
                outcome, status = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID"
                break
            # 2e comparator disposition
            if cd == "COMPLETE":
                exact = (cm["task_success_rate"]["value"] == 0.0 and cm["parseable_action_rate_step1"]["value"] == 1.0
                         and cm["answer_action_emission_rate"]["value"] == 0.0)
                tc["comparator_disposition"] = "REPLICATION_ANCHOR_EXACT" if exact else "REPLICATION_ANCHOR_DRIFT"
            elif cd == "EXCLUDED":
                tc["comparator_disposition"] = "COMP_UNANCHORED"
            else:
                tc["comparator_disposition"] = "COMP_%s" % cd
            decision_trace.append("rule2e_comparator:%s=%s" % (cand, tc["comparator_disposition"]))

            clears = tm and tm["task_success_rate"]["value"] >= TSR_BAR and tm["parseable_action_rate_step1"]["value"] >= PARSE_BAR
            tc["clears"] = bool(clears)
            if clears and cd == "COMPLETE":
                decision_trace.append("rule2f_supports_prompt_attributed:%s" % cand)
                outcome, status = "SUPPORTS", "COMPLETE"
                break
            if clears and cd == "EXCLUDED":
                decision_trace.append("rule2g_unattributable_clearing:%s" % cand)
                outcome, status = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID"
                break
            if td == "COMPLETE" and not clears:
                tc["disposition_label"] = "TREATMENT_FAILS_BAR"
                decision_trace.append("rule2h_treatment_fails_bar:%s" % cand)
                continue
            # td COMPLETE and clears handled above; fallthrough
        if outcome is None:
            complete_treats = [c for c in cells.values() if c["condition"] == TREAT and c["disposition"] == "COMPLETE"]
            if complete_treats and not any(c.get("clears") for c in complete_treats):
                outcome, status = "FALSIFIES", "COMPLETE"
                decision_trace.append("rule3_falsifies")
            else:
                outcome, status = "MEASUREMENT_INVALID", "MEASUREMENT_INVALID"
                decision_trace.append("rule4_no_complete_treat")

    derived = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38164607941",
        "lane": "intel",
        "outcome": outcome,
        "status": status,
        "preflight_pass": preflight_ok,
        "preflight_checks": checks,
        "decision_trace": decision_trace,
        "cells": cells,
        "parent_anchor": {
            "M-7B-QWEN": parent["metrics"]["M-7B-QWEN"],
            "M-3B-QWEN": parent["metrics"]["M-3B-QWEN"],
        },
    }
    out = os.path.join(EXP, "raw", "decision.json")
    with open(out, "w") as f:
        json.dump(derived, f, indent=2, sort_keys=True)
    print(json.dumps({"outcome": outcome, "status": status, "trace": decision_trace}))
    for k, v in cells.items():
        print(k, v["disposition"], (v["metrics"] or {}).get("task_success_rate"), (v["metrics"] or {}).get("parseable_action_rate_step1"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
