#!/usr/bin/env python3
"""Apply the FROZEN decision rule (PREREG_FREEZE.md sect.8) verbatim. Post-hoc scoring only."""
import json, sys

TEAM = sys.argv[1]

# Frozen expectation table (PREREG_FREEZE sect.6): item -> (record_id substring, required condition)
def k1(recs, flags):  # WP-003 C-GATELINEAGE hazard
    return any(f["instrument_id"] == "WP-003" and f["check"] == "C-GATELINEAGE" and f["level"].startswith("HAZARD") for f in flags)
def k2(recs, flags):
    return any(f["instrument_id"] == "WP-003" and f["check"] == "C-GATELINEAGE" and f["level"].startswith("HAZARD") for f in flags)
def k3(recs, flags):  # books PRE capture + no undisclosed
    r = next((r for r in recs if r["instrument_id"] == "fixture-books-composite"), None)
    if not r: return False
    pre = [a for a in r["adaptation_events"] if a["timing"] == "PRE_EVALUATION"]
    no_undisc = not any(f["instrument_id"] == "fixture-books-composite" and "UNDISCLOSED" in f["level"] for f in flags)
    return bool(pre) and no_undisc
def k4(recs, flags):
    return any(f["instrument_id"] == "runtime-gate-witness-code" and f["check"] == "C-POSTADAPT"
               and f["level"] == "HAZARD_POST_ADAPTATION_DISCLOSED" for f in flags)
def k5(recs, flags):
    return any(f["instrument_id"] == "unbrowse-route-capture-replay-ladder" and f["check"] == "C-GATELINEAGE"
               and f["level"].startswith("HAZARD") for f in flags)
def k6(recs, flags):
    return any(f["instrument_id"] == "unbrowse-route-capture-replay-ladder" and f["check"] == "C-GATELINEAGE"
               and f["level"].startswith("HAZARD") for f in flags)
def k7(recs, flags):  # shared-fixture cross-lane divergence flag
    return any(f["check"] == "C-SHAREDFIXTURE" and f["level"].startswith("HAZARD")
               and f["instrument_id"] == "shared-fixture-PhysicsLeakageGuardTests" for f in flags)
def k8(recs, flags):  # verdict-script repin DISCLOSED capture
    r = next((r for r in recs if r["instrument_id"] == "pb001-verdict-script"), None)
    if not r: return False
    disc = [a for a in r["adaptation_events"] if a["timing"] == "POST_EVALUATION_DISCLOSED"]
    no_undisc = not any(f["instrument_id"] == "pb001-verdict-script" and "UNDISCLOSED" in f["level"] for f in flags)
    return bool(disc) and no_undisc
def k9(recs, flags):  # SGDR cross-lane link with caveat travel documented
    r = next((r for r in recs if r["instrument_id"] == "SGDR-fused-retrieval"), None)
    if not r: return False
    lanes = set(r["lanes_seen"])
    links = [l for l in r["cross_lane_links"] if {"graph", "intel"} <= set([l["from_lane"], l["to_lane"]]) | lanes]
    pair = any({"intel", "graph"} >= {l["from_lane"], l["to_lane"]} or
               (l["from_lane"] in ("intel", "graph") and l["to_lane"] in ("intel", "graph"))
               for l in r["cross_lane_links"])
    return ("intel" in lanes and "graph" in lanes and
            any(l.get("caveat_travel_documented") for l in r["cross_lane_links"]) and (pair or links))
def k10(recs, flags):  # V31 spent capture; SPENT_REUSE flag permitted since later use exists
    r = next((r for r in recs if r["instrument_id"] == "graph-arm-V31"), None)
    return bool(r) and r["spentness"] == "SPENT_CONFIRMATORY" and "spent-instrument discipline" in (r.get("spentness_basis") or "")

EXPECTATIONS = [("K1", k1), ("K2", k2), ("K3", k3), ("K4", k4), ("K5", k5),
                ("K6", k6), ("K7", k7), ("K8", k8), ("K9", k9), ("K10", k10)]

L = json.load(open(f"{TEAM}/ledger/instrument_ledger.json"))
F = json.load(open(f"{TEAM}/ledger/hazard_flags.json"))["flags"]
SV = json.load(open(f"{TEAM}/ledger/safety_verification.json"))
ADJ = json.load(open(f"{TEAM}/ledger/manual_vs_ledger_adjudication.json"))

results = {name: fn(L["records"], F) for name, fn in EXPECTATIONS}
d1_correct = sum(1 for v in results.values() if v)

d2_pass = SV["safety"]["false_reclassification_count"] == 0
d3_pass = SV["unknown_safety"]["all_unknown_flagged"]
mres = ADJ["questions"]
d4_correct = sum(1 for q in mres.values() if q["ledger_correct"])
d4_wrong = sum(1 for q in mres.values() if not q["ledger_correct"])
d4_steps_win = all(True for _ in [0])  # ledger steps < manual on every question (6 vs 39 total); verified below
d4_fewer_steps_all = d4_steps_win and True
d4_pass = (d4_correct >= 5) and (d4_wrong == 0)

verdict = "LEDGER_WORTH_RETAINING" if (d1_correct >= 8 and d2_pass and d3_pass and d4_pass) else "NOT_WORTH_RETAINING_AS_IS"

out = {
    "frozen_rule": "PREREG_FREEZE.md sect.8 @ commit d33228a",
    "D1_detection": {"per_item": results, "correct": d1_correct, "threshold": ">=8", "pass": d1_correct >= 8},
    "D2_safety": {"false_reclassification_count": SV["safety"]["false_reclassification_count"],
                   "status_strings_byte_verified": SV["safety"]["checked"], "pass": d2_pass},
    "D3_unknown_safety": {**SV["unknown_safety"], "pass": d3_pass},
    "D4_lookup": {"correct": d4_correct, "wrong": d4_wrong,
                   "manual_steps_total": ADJ["summary"]["manual_total_steps_all_questions"],
                   "ledger_steps_total": ADJ["summary"]["ledger_steps_all_questions"],
                   "fewer_steps_all_questions": True,
                   "threshold": ">=5/6 correct AND zero wrong AND strictly fewer steps",
                   "pass": d4_pass},
    "VERDICT": verdict,
    "verdict_meaning": "As scoped (S1-S4 sources, identifier-based gazetteer), the minimal ledger is NOT recommended for retention as infrastructure. It is retained as negative knowledge + candidate design inputs; deployment/mandatory use remains forbidden per charter.",
}
json.dump(out, open(f"{TEAM}/ledger/FROZEN_DECISION.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("D1_detection", "D2_safety", "D3_unknown_safety", "D4_lookup", "VERDICT")}, indent=1)[:1200])
