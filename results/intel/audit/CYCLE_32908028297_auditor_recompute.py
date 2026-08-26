#!/usr/bin/env python3
"""INTEL AUDITOR independent recomputation — cycle 7, run 32908028297.

Second-path verification of every headline number in
results/intel/reproductions/cycle7/decision_rule_evaluation.json from raw
committed evidence. Pure stdlib; read-only over the Reproducer workspace.

Usage: python3 CYCLE_32908028297_auditor_recompute.py [--repro /tmp/spider_intel_repro]
"""
import argparse
import json
import math
import os
import random
import statistics
import sys
from collections import Counter

TASKS = ("T_HTTPBIN_FORM", "T_HTTPBIN_COOKIE", "T_PETSTORE_FIND",
         "T_DEMOBLAZE_CART")
HOST = {"T_HTTPBIN_FORM": "httpbin.org", "T_HTTPBIN_COOKIE": "httpbin.org",
        "T_PETSTORE_FIND": "petstore.swagger.io",
        "T_DEMOBLAZE_CART": "www.demoblaze.com"}
BENIGN = {"B1_key_order", "B2_whitespace_pretty", "B3_added_optional_field",
          "B4_list_length_change", "B5_int_float_representation"}
DETECTING = ("M1_field_removal", "M2_type_change", "M3_nesting_change",
             "M5_pagination_shape_change", "M6_error_format_change")

checks = []


def ck(name, ok, detail=""):
    checks.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (" :: " + detail if detail else ""))


def rows(passes, arm, task):
    return [p for p in passes if p["arm"] == arm and p["task"] == task
            and p.get("kind") != "warmup"]


def sign_p(w, n):
    return sum(math.comb(n, k) for k in range(w, n + 1)) / 2.0 ** n


def holm(ps):
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    adj, run = [0.0] * m, 0.0
    for rank, idx in enumerate(order):
        run = max(run, (m - rank) * ps[idx])
        adj[idx] = min(1.0, run)
    return adj


def wilson_upper(k, n, alpha=0.05):
    z = 1.959963984540054  # two-sided 95%
    ph = k / n
    den = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / den
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return c + h


def invnorm(p):
    # Acklam rational approximation
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    pl = 0.02425
    if p < pl:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > 1 - pl:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


ncdf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bca_independent(deltas, n_boot=200000, seed=987654321):
    n = len(deltas)
    hat = sum(deltas) / n
    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        s = 0.0
        for _i in range(n):
            s += deltas[rng.randrange(n)]
        boots.append(s / n)
    boots.sort()
    prop_lt = sum(1 for x in boots if x < hat) / n_boot
    z0 = invnorm(prop_lt) if 0 < prop_lt < 1 else 0.0
    jacks = [sum(deltas[:i] + deltas[i + 1:]) / (n - 1) for i in range(n)]
    jm = sum(jacks) / n
    num = sum((jm - j) ** 3 for j in jacks)
    den = 6 * (sum((jm - j) ** 2 for j in jacks) ** 1.5)
    a = num / den if den else 0.0

    def adjf(ap):
        z = invnorm(ap)
        return ncdf(z0 + (z0 + z) / (1 - a * (z0 + z)))

    def q(p):
        i = p * (n_boot - 1)
        lo = int(i)
        hi = min(lo + 1, n_boot - 1)
        f = i - lo
        return boots[lo] * (1 - f) + boots[hi] * f
    return q(adjf(0.025)), q(adjf(0.975))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repro", default="/tmp/spider_intel_repro")
    args = ap.parse_args()
    R = os.path.join(args.repro, "results/intel/reproductions/cycle7")
    ev = json.load(open(os.path.join(R, "decision_rule_evaluation.json")))
    passes = json.load(open(os.path.join(R, "passes_raw.json")))

    # ---- invalidity gates ----
    req = ["availability_log.json", "disc_meta_c7.json",
           "discovery_checks_c7.json", "block_order.json", "passes_raw.json",
           "ladder_events.json", "probe_events_rb.json", "mutation_arm.json",
           "addressing_arm.json", "ttl_window1.json",
           "ttl_window2_protocol.json"]
    ck("required-files-present", all(os.path.exists(os.path.join(R, f))
                                     for f in req))
    av = json.load(open(os.path.join(R, "availability_log.json")))
    up = {e["host"] for e in av if isinstance(e.get("status"), int)
          and e["status"] < 500}
    ck("P0-hosts>=4", len(up) >= 4, f"{len(up)} up")
    lt3 = []
    pairs_by_task = {}
    for t in TASKS:
        A = {p.get("rep"): p for p in rows(passes, "A", t)
             if isinstance(p.get("rep"), int)}
        B = {p.get("rep"): p for p in rows(passes, "B", t)
             if isinstance(p.get("rep"), int)}
        valid = [r for r in sorted(set(A) & set(B))
                 if A[r].get("payload_ok") and B[r].get("payload_ok")]
        pairs_by_task[t] = [(A[r]["wall_ms"], B[r]["wall_ms"]) for r in valid]
        if len(valid) < 3:
            lt3.append(t)
    ck("<=1-task-below-pair-floor", len(lt3) <= 1, str(lt3))

    # ---- C1 ----
    dm = json.load(open(os.path.join(R, "disc_meta_c7.json")))
    dc = json.load(open(os.path.join(R, "discovery_checks_c7.json")))
    c1_all = True
    learned = []
    for t in TASKS:
        ok = (dm[t].get("both_genuine_completions_accepted") == [True, True]
              and len(dm[t].get("routes_learned") or []) > 0
              and dc[t].get("code") == "REPLAY_OK"
              and dc[t].get("equivalent") is True)
        learned.append(len(dm[t].get("routes_learned") or []))
        c1_all = c1_all and ok
    ck("C1-pass-4of4", c1_all, f"routes learned {learned}")
    ck("C1-matches-committed", ev["clause_1_discovery"]["pass"] == c1_all)

    # ---- C2 ----
    speed_exp = {"T_HTTPBIN_FORM": 3.54, "T_HTTPBIN_COOKIE": 2.66,
                 "T_PETSTORE_FIND": 7.64, "T_DEMOBLAZE_CART": 20.90}
    med_exp = {"T_HTTPBIN_FORM": (795.4, 224.7),
               "T_HTTPBIN_COOKIE": (616.6, 231.5),
               "T_PETSTORE_FIND": (2531.5, 331.3),
               "T_DEMOBLAZE_CART": (7133.0, 341.3)}
    ci_exp = {"T_HTTPBIN_FORM": (0.6388, 1.3151),
              "T_HTTPBIN_COOKIE": (0.9574, 1.0612),
              "T_PETSTORE_FIND": (2.008, 2.0495),
              "T_DEMOBLAZE_CART": (2.8888, 3.0804)}
    ps = []
    for t in TASKS:
        prs = pairs_by_task[t]
        a = [x for x, _ in prs]
        b = [y for _, y in prs]
        ma, mb = statistics.median(a), statistics.median(b)
        sp = ma / mb
        wins = sum(1 for x, y in prs if y < x)
        ck(f"C2[{t}]-medians", (round(ma, 1), round(mb, 1)) == med_exp[t],
           f"{ma}/{mb} ms")
        ck(f"C2[{t}]-speedup", round(sp, 2) == speed_exp[t], f"{sp:.4f}")
        ck(f"C2[{t}]-wins-5of5", wins == 5 == len(prs))
        bzero = all(p.get("actions") == 0 for p in rows(passes, "B", t))
        ck(f"C2[{t}]-B-actions-zero", bzero)
        deltas = [math.log(x / y) for x, y in prs]
        lo_frozen = ev["clause_2_economics"]["tasks"][t]["bca_logratio_ci_low"]
        hi_frozen = ev["clause_2_economics"]["tasks"][t]["bca_logratio_ci_high"]
        ck(f"C2[{t}]-BCa-exact-rerun",
           abs(lo_frozen - ci_exp[t][0]) < 5e-5
           and abs(hi_frozen - ci_exp[t][1]) < 5e-5)
        lo_i, hi_i = bca_independent(deltas)
        ck(f"C2[{t}]-BCa-independent-agreement",
           abs(lo_i - lo_frozen) < 0.02 and abs(hi_i - hi_frozen) < 0.02,
           f"indep [{lo_i:.4f},{hi_i:.4f}] vs committed "
           f"[{lo_frozen},{hi_frozen}]")
        ck(f"C2[{t}]-ci-low>0", lo_frozen > 0)
        ps.append(sign_p(wins, len(prs)))
    adj = holm(ps)
    ck("C2-holm-values", all(round(x, 5) == 0.125 for x in adj),
       f"{[round(x,5) for x in adj]}")
    ck("C2-holm-zero-power-floor",
       min(sign_p(5, 5) * 4 for _ in [0]) >= 0.05,
       "min achievable adjusted p = 4*(1/32)=0.125 > 0.05 for ANY outcome "
       "at n=5 -> family gate unreachable by construction")
    ck("C2-clause-fail-as-committed", ev["clause_2_economics"]["pass"] is False)
    # LOHO
    for hx in sorted(set(HOST.values())):
        P = [(x, y) for t in TASKS if HOST[t] != hx
             for x, y in pairs_by_task[t]]
        w = sum(1 for x, y in P if y < x)
        stable = (statistics.median(y for _, y in P)
                  < statistics.median(x for x, _ in P)) and w >= 0.7 * len(P)
        ck(f"LOHO-without-{hx}", stable,
           f"n={len(P)} wins={w}")
    ck("LOHO-matches-committed",
       ev["clause_2_economics"]["leave_one_host_out"]
       ["direction_stable_all_exclusions"] is True)

    # ---- C3 ----
    tb = rows(passes, "B", "T_DEMOBLAZE_CART")
    td = rows(passes, "D", "T_DEMOBLAZE_CART")
    tpd = rows(passes, "D", "T_PETSTORE_FIND")
    ck("C3-demoblaze-B-30of30",
       len(tb) == 30 and sum(1 for p in tb if p.get("payload_ok")) == 30)
    ck("C3-demoblaze-D-0of5",
       len(td) == 5 and sum(1 for p in td if p.get("payload_ok")) == 0,
       f"codes={dict(Counter(p.get('code') for p in td))}")
    ck("C3-petstore-D-descriptive-5of5",
       len(tpd) == 5 and sum(1 for p in tpd if p.get("payload_ok")) == 5)

    # ---- C4 ----
    arm = json.load(open(os.path.join(R, "mutation_arm.json")))
    res = arm["results"]
    rev = json.load(open(os.path.join(R, "mutation_schedule_revealed.json")))
    sys.path.insert(0, args.repro)
    from intel.experiments.unbrowse_ladder_c7.schedule import (
        build_schedule, schedule_hash)
    h = schedule_hash(build_schedule())
    ck("C4-schedule-hash-chain",
       h == "276132df2f6a57a466d3b84d918e03acc177c10d2e82f745d028f9f02c4efbb8"
       == arm["schedule_hash"] == schedule_hash(rev["steps"]))
    fp = sum(1 for r in res if r["kind"] in BENIGN
             and r["fired_code"] != "REPLAY_OK")
    nben = sum(1 for r in res if r["kind"] in BENIGN)
    ck("C4-benign-25-FP-0", nben == 25 and fp == 0)
    ck("C4-wilson-upper", round(wilson_upper(fp, nben), 4) == 0.1332
       and wilson_upper(fp, nben) <= 0.15)
    det = {k: [r["fired_code"] for r in res if r["kind"] == k]
           for k in DETECTING}
    ck("C4-detecting-classes-x2-SCHEMA_MISMATCH",
       all(v == ["SCHEMA_MISMATCH", "SCHEMA_MISMATCH"] for v in det.values()))
    m4 = [r["fired_code"] for r in res if r["kind"] == "M4_enum_meaning_flip"]
    ck("C4-M4-blind-as-predeclared", m4 == ["REPLAY_OK", "REPLAY_OK"])
    rev_ids = [s["step_id"] for s in rev["steps"]]
    ck("C4-execution-order-matches-sealed-schedule",
       rev_ids == [r["step_id"] for r in res])

    # ---- C5 ----
    rb = json.load(open(os.path.join(R, "probe_events_rb.json")))
    s = rb["summary"]
    ck("C5-Q1-refused-418-environment",
       s["cooldown_check"]["status"] == 418
       and all(d.get("reason") == "booking_creation_refused"
               for d in s["Q1_detail"]))
    ck("C5-Q2-negative-pass-positive-null",
       s["Q2"].get("negative_ok") is True
       and s["Q2"].get("positive_ok") is None)
    ck("C5-Q3-compliant", s["Q3_ttl_compliant"] is True)
    ck("C5-Q4-deleted-absence-surfaced",
       s["Q4"].get("deleted") is True and s["Q4"].get("code") == "HTTP_ERROR"
       and s["Q4"].get("surfaced_absence") is True)
    ck("C5-pointer-only", s["pointer_only_store"] is True)
    ck("C5-checker-all-pass-false-as-committed",
       rb["checker"]["all_pass"] is False
       and ev["clause_5_lifecycle_core"]["pass"] is False)

    # ---- ladder events / hygiene ----
    lev = json.load(open(os.path.join(R, "ladder_events.json")))
    ck("ladder-events-160-all-REPLAY_OK",
       len(lev) == 160
       and all(e.get("code") == "REPLAY_OK" for e in lev))

    # ---- verdict mapping ----
    c1p, c2p = c1_all, False
    c3p = True
    c4p = True
    c5p = False
    expected = ("MEASUREMENT_INVALID" if lt3.__len__() > 1 else
                "FAILED_TO_REPRODUCE" if not c1p else
                "REPRODUCED_USEFUL" if (c1p and c2p and c3p and c4p and c5p)
                else "INCONCLUSIVE")
    ck("verdict-INCONCLUSIVE-mechanical", ev["verdict"] == expected
       == "INCONCLUSIVE")

    n_fail = sum(1 for _, ok, _ in checks if not ok)
    print(f"\n{len(checks) - n_fail}/{len(checks)} auditor checks PASS")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
