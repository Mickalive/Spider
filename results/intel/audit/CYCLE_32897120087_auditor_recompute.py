"""INTEL_AUDITOR independent recomputation - cycle 6, run 32897120087.

Re-derives every headline number of reports/intel/reproductions/cycle6_report.md
from raw committed rows WITHOUT using intel/experiments/ code for the arithmetic
(the frozen evaluator was separately rerun byte-identically; this script is the
auditor's independent second path).

Run from /tmp/spider_intel_repro:
  python3 /home/runner/work/Spider/Spider/results/intel/audit/CYCLE_32897120087_auditor_recompute.py
"""
import hashlib
import json
import math
import random
import statistics
import sys
from collections import Counter

BASE = "results/intel/reproductions/cycle6/"
ok = True


def check(name, cond, detail=""):
    global ok
    print(f"[{'OK ' if cond else 'FAIL'}] {name} {detail}")
    ok = ok and cond


P = json.load(open(BASE + "passes_raw.json"))
E = json.load(open(BASE + "decision_rule_evaluation.json"))


def measured(arm, task):
    return [p for p in P if p["arm"] == arm and p["task"] == task
            and p.get("kind") != "warmup"]


# ---- 1. FORM task-level economics -------------------------------------------
a = {r["rep"]: r for r in measured("A", "T_HTTPBIN_FORM")}
b = {r["rep"]: r for r in measured("B", "T_HTTPBIN_FORM")}
valid = [r for r in sorted(set(a) & set(b))
         if a[r]["payload_ok"] and b[r]["payload_ok"]]
ams = [a[r]["wall_ms"] for r in valid]
bms = [b[r]["wall_ms"] for r in valid]
sp = statistics.median(ams) / statistics.median(bms)
check("FORM medians", round(statistics.median(ams), 1) == 628.9
      and round(statistics.median(bms), 1) == 66.4,
      f"A={statistics.median(ams)} B={statistics.median(bms)}")
check("FORM speedup_median", round(sp, 2) == 9.47, f"{sp:.3f}")
d = [math.log(x / y) for x, y in zip(ams, bms)]
rng = random.Random(20260826)
lo, hi = [], []
for _ in range(10000):
    s = sorted(rng.choice(d) for _ in d)
    lo.append(s[int(0.05 * len(s))])
    hi.append(s[min(len(s) - 1, int(0.95 * len(s)))])
bci = E["clause_2_economics"]["tasks"]["T_HTTPBIN_FORM"]
check("FORM CI direction consistent",
      statistics.median(lo) > 0 and bci["bca_logratio_ci_low"] > 0,
      f"auditor percentile [{statistics.median(lo):.3f},{statistics.median(hi):.3f}] "
      f"vs BCa [{bci['bca_logratio_ci_low']},{bci['bca_logratio_ci_high']}]")
check("FORM B actions all zero", all(r["actions"] == 0
                                     for r in measured("B", "T_HTTPBIN_FORM")))

# ---- 2. COOKIE defect row 4 --------------------------------------------------
bc_all = measured("B", "T_HTTPBIN_COOKIE")
check("COOKIE B 30x REPLAY_OK", len(bc_all) == 30 and
      all(r["code"] == "REPLAY_OK" for r in bc_all))
check("COOKIE B payload_ok false on ALL (defect row 4)",
      sum(1 for r in bc_all if r["payload_ok"]) == 0)
ac_med = statistics.median([r["wall_ms"] for r in measured("A", "T_HTTPBIN_COOKIE")])
check("COOKIE A median 482.2", ac_med == 482.2, f"{ac_med}")

# ---- 3. zero-valid-pair tasks -> invalidity condition ------------------------
zero = []
for t in ("T_HTTPBIN_COOKIE", "T_PETSTORE_FIND", "T_DEMOBLAZE_CART"):
    aa = {r["rep"]: r for r in measured("A", t)}
    bb = {r["rep"]: r for r in measured("B", t)}
    v = [r for r in sorted(set(aa) & set(bb))
         if aa[r]["payload_ok"] and bb[r]["payload_ok"]]
    if len(v) < 3:
        zero.append(t)
check("invalidity: 3 tasks <3 valid pairs", len(zero) == 3, str(zero))
check("evaluator verdict MEASUREMENT_INVALID", E["verdict"] == "MEASUREMENT_INVALID")

# ---- 4. mutation arm artifacts (row 5) ---------------------------------------
ma = json.load(open(BASE + "mutation_arm.json"))
res = ma["results"]
pu = [x for x in res if x.get("fired_code") == "PARAM_UNRESOLVED"]
ben = [x for x in res if str(x.get("kind", "")).startswith("B")]
fp = [x for x in ben if x.get("fired_code") != "REPLAY_OK"]
check("10 benign FPs are ALL PARAM_UNRESOLVED artifacts",
      len(fp) == 10 and all(x["fired_code"] == "PARAM_UNRESOLVED" for x in fp))
check("FP targets exactly page/id-starved endpoints",
      {x["target"] for x in fp} == {"replica_list_items", "replica_get_post"})
m25 = [x for x in res if x["kind"] in ("M2_type_change",
                                       "M5_pagination_shape_change")]
check("M2/M5 never executed a request",
      len(m25) == 4 and all(x["fired_code"] == "PARAM_UNRESOLVED" for x in m25))
m13 = [x for x in res if x["kind"] in ("M1_field_removal", "M3_nesting_change",
                                       "M6_error_format_change")]
check("M1/M3/M6 detected twice each",
      len(m13) == 6 and all(x["fired_code"] == "SCHEMA_MISMATCH" for x in m13))

# ---- 5. schedule sealing ------------------------------------------------------
sys.path.insert(0, ".")
from intel.experiments.unbrowse_ladder_multihost.schedule import (  # noqa: E402
    build_schedule, schedule_hash)
rev = json.load(open(BASE + "mutation_schedule_revealed.json"))
SEALED = "276132df2f6a57a466d3b84d918e03acc177c10d2e82f745d028f9f02c4efbb8"
check("revealed steps == deterministic rebuild", rev["steps"] == build_schedule())
check("steps hash == sealed value", schedule_hash(rev["steps"]) == SEALED)
check("mutation arm recorded verified=True",
      ma["summary"]["schedule_hash_verified"] is True)

# ---- 6. demoblaze text/html write endpoint (row 2) ---------------------------
mf = json.load(open(BASE + "discovery/T_DEMOBLAZE_CART_manifests.json"))
mfs = mf if isinstance(mf, list) else [mf]
at = [(e["method"], e.get("resp_content_type"))
      for m in mfs for e in m["entries"]
      if e.get("url", "").endswith("/addtocart")]
check("addtocart answered text/html in both discovery runs",
      len(at) == 2 and all(c and c.startswith("text/html") for _, c in at),
      str(at))

# ---- 7. petstore empty intent (row 3) ----------------------------------------
rt = json.load(open(BASE + "discovery/T_PETSTORE_FIND_routes.json"))
check("petstore routes learned with intent=''",
      len(rt) == 2 and all(r["intent"] == "" for r in rt))

# ---- 8. pointer-only checker false alarm (row 7) -----------------------------
rb = json.load(open(BASE + "discovery/rb_routestore.json"))
routes = rb if isinstance(rb, list) else rb.get("routes", [])
auth = [r for r in routes if r.get("route_id") == "rb_auth"
        or "auth" in str(r.get("intent", ""))]
shape = json.dumps(auth[0].get("body_template", {}).get("shape", ""))
check('rb_auth shape contains type-name sketch "password": "str"',
      '"password": "str"' in shape, shape[:60])

# ---- 9. RB probes ------------------------------------------------------------
pe = json.load(open(BASE + "probe_events_rb.json"))["summary"]
check("Q1 both creations refused", pe["Q1_detail"] ==
      [{"bid": None, "ok": False, "reason": "booking_creation_refused"}] * 2)

# ---- 10. evaluator output integrity ------------------------------------------
blob = open(BASE + "decision_rule_evaluation.json", "rb").read()
print(f"[INFO] committed decision_rule_evaluation.json sha256 "
      f"{hashlib.sha256(blob).hexdigest()}")

print("\nAUDITOR RECOMPUTATION:", "ALL CHECKS PASS" if ok else "FAILURES PRESENT")
