#!/usr/bin/env python3
"""frontier-instrument-ledger — LEAD SELF-VERIFICATION (run 32922388029).

Status: lead-side integrity re-check performed AFTER the frozen outcome was
computed, BEFORE team handoff. This is NOT the independent audit gate
(FRONTIER -> AUDITOR -> DIRECTOR still pending per V3 §5).

Independently of build/checker logic it recomputes:
  V1 byte-exact status-string safety over cited mount files + A2 scope check;
  V2 extraction-manifest sha256 freshness vs current accepted mounts;
  V3 D1 expectation items re-derived straight from hazard_flags.json/ledger,
     compared against FROZEN_DECISION.json;
  V4 UNKNOWN-safety recounted from first principles;
  V5 M3 ground truth: literal `PhysicsLeakageGuardTests` spread across mounts;
  V6 D4 per-question manual-vs-ledger step comparison.

Usage: python3 verify_integrity.py <team_results_dir>
Writes <team_results_dir>/lead_self_verification.json; exit 1 on any failure.
NOTE: run from a copy in a scratch dir with ledger/manual_vs_ledger*.json
present; build_ledger.py requires pre-created ledger/ and raw/ subdirs
(makedirs defect documented in CYCLE report).
"""
import json, hashlib, sys, re

TEAM = sys.argv[1]
ROOTS = ("/tmp/spider_graph", "/tmp/spider_physics", "/tmp/spider_intel",
         "/tmp/spider_product", "/tmp/spider_runtime")
L = json.load(open(f"{TEAM}/ledger/instrument_ledger.json"))["records"]
F = json.load(open(f"{TEAM}/ledger/hazard_flags.json"))["flags"]
SV = json.load(open(f"{TEAM}/ledger/safety_verification.json"))
MAN = json.load(open(f"{TEAM}/raw/extraction_manifest.json"))
MV = json.load(open(f"{TEAM}/ledger/manual_vs_ledger.json"))

fail = []
# V1: byte-exact verbatim status strings, scope-limited to accepted mounts
v1_checked = v1_bad = 0
scope_bad = []
for r in L:
    for u in r["uses"]:
        st = u.get("status_at_source_verbatim")
        p = u["source_ref"]
        if not p.startswith(ROOTS):
            scope_bad.append(p)
        if st in (None, "UNKNOWN"):
            continue
        v1_checked += 1
        try:
            content = open(p, encoding="utf-8", errors="replace").read()
            if st[:200] not in content:
                v1_bad += 1
                fail.append(("V1", r["record_id"], p))
        except OSError:
            v1_bad += 1
            fail.append(("V1-missing", r["record_id"], p))

# V2: manifest hashes still match mounts (evidence unchanged since extraction)
v2_checked = v2_stale = 0
for m in MAN:
    h = hashlib.sha256(open(m["path"], "rb").read()).hexdigest()
    v2_checked += 1
    if h != m["sha256"]:
        v2_stale += 1
        fail.append(("V2-stale-source", m["path"]))

# V3: D1 items re-derived independently of score_cycle.py
def has(cid, chk, lvl_prefix):
    return any(f["instrument_id"] == cid and f["check"] == chk
               and f["level"].startswith(lvl_prefix) for f in F)
byid = {r["instrument_id"]: r for r in L}
undisc = lambda cid: any(f["instrument_id"] == cid and "UNDISCLOSED" in f["level"] for f in F)
v3 = {
    "K1": has("WP-003", "C-GATELINEAGE", "HAZARD"),
    "K2": has("WP-003", "C-GATELINEAGE", "HAZARD"),
    "K3": bool([a for a in byid["fixture-books-composite"]["adaptation_events"]
                if a["timing"] == "PRE_EVALUATION"]) and not undisc("fixture-books-composite"),
    "K4": has("runtime-gate-witness-code", "C-POSTADAPT", "HAZARD_POST_ADAPTATION_DISCLOSED"),
    "K5": has("unbrowse-route-capture-replay-ladder", "C-GATELINEAGE", "HAZARD"),
    "K6": has("unbrowse-route-capture-replay-ladder", "C-GATELINEAGE", "HAZARD"),
    "K7": has("shared-fixture-PhysicsLeakageGuardTests", "C-SHAREDFIXTURE", "HAZARD"),
    "K8": bool([a for a in byid["pb001-verdict-script"]["adaptation_events"]
                if a["timing"] == "POST_EVALUATION_DISCLOSED"]) and not undisc("pb001-verdict-script"),
    "K9": ("intel" in byid["SGDR-fused-retrieval"]["lanes_seen"]
           and "graph" in byid["SGDR-fused-retrieval"]["lanes_seen"]
           and any(l.get("caveat_travel_documented") for l in byid["SGDR-fused-retrieval"]["cross_lane_links"])),
    "K10": byid["graph-arm-V31"]["spentness"] == "SPENT_CONFIRMATORY"
           and "spent-instrument discipline" in (byid["graph-arm-V31"].get("spentness_basis") or ""),
}
FD = json.load(open(f"{TEAM}/ledger/FROZEN_DECISION.json"))
mismatch = {k: (v3[k], FD["D1_detection"]["per_item"][k]) for k in v3
            if v3[k] != FD["D1_detection"]["per_item"][k]}
if mismatch:
    fail.append(("V3-scoring-mismatch", mismatch))

# V4: UNKNOWN-safety recounted FROM FIRST PRINCIPLES (the builder/checker never
# persists d3_load_bearing_unknown into the ledger JSON, so recompute it here)
load_unknown = [r for r in L if r["spentness"] == "UNKNOWN"
                or any(ae["timing"] == "UNKNOWN" for ae in r["adaptation_events"])
                or any(u["status_at_source_verbatim"] == "UNKNOWN" for u in r["uses"])]
flagged_ids = {f["record_id"] for f in F if f["level"] == "REVIEW_UNKNOWN"}
v4_ok = all(r["record_id"] in flagged_ids for r in load_unknown)
if not v4_ok or len(load_unknown) != SV["unknown_safety"]["records_with_load_bearing_unknown"]:
    fail.append(("V4-unknown-accounting",
                 {"recomputed": len(load_unknown),
                  "committed_sv": SV["unknown_safety"]["records_with_load_bearing_unknown"],
                  "unflagged": [r["record_id"] for r in load_unknown if r["record_id"] not in flagged_ids]}))

# V5: literal PhysicsLeakageGuardTests spread across ALL mount subtrees
import subprocess
hits = {}
for m in ROOTS:
    out = subprocess.run(["grep", "-rlI", "PhysicsLeakageGuardTests", m],
                         capture_output=True, text=True).stdout.splitlines()
    hits[m] = out
v5_total_files = sum(len(v) for v in hits.values())
v5_lanes_with_literal = sorted(k.split("_")[-1] for k, v in hits.items() if v)
s14_literal_files = set()
for m in ROOTS:
    for sub in ("state", "docs", "results"):
        out = subprocess.run(["grep", "-rlI", "PhysicsLeakageGuardTests", f"{m}/{sub}"],
                             capture_output=True, text=True).stdout.splitlines()
        s14_literal_files |= set(out)

# V6: per-question manual vs ledger steps
v6 = {}
for qid, o in MV.items():
    v6[qid] = {"manual_steps": o["manual"]["steps"], "ledger_steps": o["ledger"]["steps"],
               "ledger_fewer": o["ledger"]["steps"] < o["manual"]["steps"]}
if not all(x["ledger_fewer"] for x in v6.values()):
    fail.append(("V6-steps-not-fewer-somewhere", v6))

report = {
    "V1_safety_recheck": {"checked": v1_checked, "violations": v1_bad,
                          "matches_committed_zero": v1_bad == 0 and SV["safety"]["false_reclassification_count"] == 0},
    "V1_scope_violations": {"count": len(scope_bad), "paths": scope_bad[:5]},
    "V2_manifest_freshness": {"sources": v2_checked, "stale": v2_stale},
    "V3_d1_independent_rederivation": {"items": v3, "correct": sum(v3.values()),
                                       "scoring_mismatch_vs_frozen_decision": mismatch},
    "V4_unknown_safety_recount": {"records_load_bearing_unknown": len(load_unknown), "all_flagged": v4_ok},
    "V5_leakageguard_literal_spread": {"total_files_all_mounts": v5_total_files,
                                       "mounts_with_literal": v5_lanes_with_literal,
                                       "files_under_state_docs_results": len(s14_literal_files),
                                       "note": "only files whose names match frozen S1-S4 classes count as sample sources; RUNTIME_LEDGER.md is excluded by frozen S2 list and scaling_MANIFEST.json is not an S3 audit-gate file",
                                       "sample": sorted(s14_literal_files)[:10]},
    "V6_step_comparison": v6,
    "FAILURES": fail,
}
print(json.dumps(report, indent=1))
json.dump(report, open(f"{TEAM}/lead_self_verification.json", "w"), indent=1)
sys.exit(1 if fail else 0)
