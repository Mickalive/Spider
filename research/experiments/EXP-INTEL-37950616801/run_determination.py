#!/usr/bin/env python3
"""EXP-INTEL-37950616801 - zero-new-corpus analytic f* reportability determination.

Executes the frozen design in spec.json / prereg.md:
  - verify the hash-pinned evidence artifact;
  - PC-EXTRACT: re-extract frozen anchors verbatim with line numbers;
  - PC-READING: derive the OCR stacked-fraction parsing rule from Eqs. (2)-(3),
    apply it to Eq. (1) and record the primary reading;
  - f* engine evaluated by TWO independent implementations (direct cost and
    dimensionless closed form) that must agree;
  - regime table over the frozen axes plus sensitivity blocks;
  - controls PC-ALGEBRA, NC-DIVERGENT, NC-CONVENTION, B-PUBLISHED-NUMBERS-ONLY,
    B-FLEET-CEILING;
  - reportability classification per (reading, convention) and verdict per the
    frozen decision rule.

stdlib only; deterministic; no network.
"""
import hashlib
import json
import math
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
EVIDENCE_REL = (
    "research/experiments/EXP-INTEL-36306525220/raw/fulltext/2608.05784v1.txt"
)
EVIDENCE = os.path.abspath(os.path.join(BASE, "..", "..", "..", EVIDENCE_REL))
RAW_DIR = os.path.join(BASE, "raw")

EXPECTED_SHA = "e286167a6ae51eebe1552f655876bae5a9c1728e16793b31e4adac4e9b154dbf"
EXPECTED_BYTES = 70219
EXPECTED_CHARS = 69607
EXPECTED_LINES = 1447

# ---------------------------------------------------------------------------
# frozen axes (spec.json frozen_parameters / regime_table)
# ---------------------------------------------------------------------------
PUBLISHED_H = [0.077, 0.086, 0.090, 0.131]
H_SWEEP = [0.077, 0.086, 0.090, 0.131, 0.25, 0.5, 1.0]
Q_SWEEP = [0.415, 0.82, 1.0]
P_SWEEP = [0.5, 0.8, 1.0]
W_SWEEP = [0.0, 1.0 / 60.0, 1.0 / 343.0, 1.0, 10.0]
B_SWEEP = [0.0, 1.0 / 60.0, 1.0 / 343.0, 0.1]
C_SWEEP = [0.1, 1.0, 10.0]
R_PRIMARY = 1.0 / 60.0
R_SENS = 1.0 / 343.0
P_PRIMARY = 1.0
C_PRIMARY = 1.0
N_REACH = 181
N_SENS = [9, 25, 181]

# Adjudication of the commensurability axis (spec measurement_validity bullet 5).
# The artifact prints compile cost as "<=0.5ms, 0 tokens" (w_model ~ 0, a
# degenerate undercount of the persistent write) and prints capture/storage cost
# only as 9.5GB / ~0.19GB per active day with OCR on 96% of frames -- never in
# dollars-per-task commensurable with Cmiss.  The true write cost of a
# memory-backed system includes capture; therefore NO artifact-internal
# commensurable w anchors a numeric f*.  The frozen w sweep is a set of explicit
# placeholders, not artifact measurements.
ARTIFACT_INTERNAL_W_COMMENSURABLE = False


# ---------------------------------------------------------------------------
# f* engine - implementation A: direct cost model
# ---------------------------------------------------------------------------
def e_cold(reading, p, cmiss=1.0):
    """Cold counterfactual per-task cost (mandate clause (a))."""
    if reading == "VAR-LIT":
        return cmiss / p
    elif reading == "VAR-MAN":
        return cmiss * p
    raise ValueError(reading)


def e_warm_writefree(reading, h, q, p, r, b, c, cmiss=1.0):
    """Write-free warm per-task cost, C-terms normalised by Cmiss."""
    u = e_cold(reading, p, cmiss)
    return (1.0 - h * q) * u + h * q * (r + b) + h * (1.0 - q) * c


def fstar_direct(reading, convention, h, q, p, r, b, c, w):
    """Implementation A: f* from explicit cold/warm totals."""
    if convention == "AMORTIZE-ONCE":
        ec = e_cold(reading, p)
        ew = e_warm_writefree(reading, h, q, p, r, b, c)
        delta = ec - ew
        if delta <= 0.0:
            return {"g": None, "delta": delta, "f_star": None,
                    "status": "DIVERGENT"}
        f = w / delta
        return {"g": None, "delta": delta, "f_star": f, "status": "FINITE"}
    elif convention == "PER-REUSE":
        ec = e_cold(reading, p)
        ew = e_warm_writefree(reading, h, q, p, r, b, c)
        delta = ec - ew
        if delta <= 0.0:
            return {"g": None, "delta": delta, "f_star": None,
                    "status": "DIVERGENT"}
        if delta > w:
            return {"g": None, "delta": delta, "f_star": 1.0, "status": "FINITE"}
        return {"g": None, "delta": delta, "f_star": None,
                "status": "NO_FSTAR_DEGENERATE"}
    raise ValueError(convention)


# ---------------------------------------------------------------------------
# f* engine - implementation B: dimensionless closed form
# ---------------------------------------------------------------------------
def g_dimensionless(reading, q, p, r, b, c):
    if reading == "VAR-LIT":
        return q * (1.0 / p - r - b) - (1.0 - q) * c
    elif reading == "VAR-MAN":
        return q * (p - r - b) - (1.0 - q) * c
    raise ValueError(reading)


def fstar_closed(reading, convention, h, q, p, r, b, c, w):
    g = g_dimensionless(reading, q, p, r, b, c)
    if convention == "AMORTIZE-ONCE":
        if g <= 0.0:
            return {"g": g, "f_star": None, "status": "DIVERGENT"}
        return {"g": g, "f_star": w / (h * g), "status": "FINITE"}
    elif convention == "PER-REUSE":
        if g <= 0.0:
            return {"g": g, "f_star": None, "status": "DIVERGENT"}
        if h * g > w:
            return {"g": g, "f_star": 1.0, "status": "FINITE"}
        return {"g": g, "f_star": None, "status": "NO_FSTAR_DEGENERATE"}
    raise ValueError(convention)


def agree(a, b, rel=1e-9):
    if a["status"] != b["status"]:
        return False
    if a["f_star"] is None and b["f_star"] is None:
        return True
    if a["f_star"] is None or b["f_star"] is None:
        return False
    if a["f_star"] == 0.0 or b["f_star"] == 0.0:
        return a["f_star"] == b["f_star"]
    return abs(a["f_star"] - b["f_star"]) / abs(a["f_star"]) <= rel


# ---------------------------------------------------------------------------
# evidence + anchors
# ---------------------------------------------------------------------------
def load_evidence():
    with open(EVIDENCE, "rb") as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")
    return {
        "path": EVIDENCE_REL,
        "sha256": sha,
        "bytes": len(raw),
        "chars": len(text),
        "lines": len(text.split("\n")),
        "text": text,
        "lines_list": text.split("\n"),
    }


ANCHORS = [
    {"id": "eq1_span", "pattern": r"E\[\$/task\]\s*=\s*\(1\u2212hq\)\s*Cmiss",
     "expected": "E[$/task] = (1\u2212hq) Cmiss"},
    {"id": "eq1_cold_term", "pattern": r"p\s*\+hq\(C hit\+Cverify\)",
     "expected": "p +hq(C hit+Cverify)"},
    {"id": "eq1_write_term", "pattern": r"\+h\(1\u2212q\)C wrong \+ Cwrite",
     "expected": "+h(1\u2212q)C wrong + Cwrite"},
    {"id": "eq1_write_over_n", "pattern": r"^N\s*,$", "expected": "N ,"},
    {"id": "eq1_defs", "pattern": r"where h is recurrence, q the fraction of hits correctly",
     "expected": "where h is recurrence, q the fraction of hits correctly"},
    {"id": "eq1_missing_input",
     "pattern": r"them measures ish on thepre-delegationpassive corpus",
     "expected": "them measures ish on thepre-delegationpassive corpus"},
    {"id": "eq2_span", "pattern": r"Cagent\(k\)\s*=\s*k", "expected": "Cagent(k) =k"},
    {"id": "eq2_wh750", "pattern": r"750\s*\+\s*350\s*\+\s*180", "expected": "750 + 350 + 180"},
    {"id": "eq3_span", "pattern": r"R=\s*Cagent\(k\)", "expected": "R= Cagent(k)"},
    {"id": "eq3_denominator", "pattern": r"C replay\(k\)\s*=", "expected": "C replay(k) ="},
    {"id": "R_inject_60", "pattern": r"Rinject\s*=\s*60\u00d7", "expected": "Rinject = 60\u00d7"},
    {"id": "R_inject_iqr", "pattern": r"interquartile59\u201362", "expected": "interquartile59\u201362"},
    {"id": "R_info_343", "pattern": r"Rinfo\s*=\s*343\u00d7", "expected": "Rinfo = 343\u00d7"},
    {"id": "h_insample_90", "pattern": r"h\s*=\s*9\.0%", "expected": "h = 9.0%"},
    {"id": "h_url_131", "pattern": r"13\.1%at URL granularity", "expected": "13.1%at URL granularity"},
    {"id": "h_train_86", "pattern": r"in-sample8\.6%", "expected": "in-sample8.6%"},
    {"id": "h_oos_77", "pattern": r"predicted hit rate is7\.7%", "expected": "predicted hit rate is7.7%"},
    {"id": "h_oos_carry", "pattern": r"7\.7%is the recurrence the cost accounting should carry",
     "expected": "7.7%is the recurrence the cost accounting should carry"},
    {"id": "q_typing_82", "pattern": r"approximately82%accurate", "expected": "approximately82%accurate"},
    {"id": "q_below_one", "pattern": r"soq\s*<\s*1and the honest fleet", "expected": "soq < 1and the honest fleet"},
    {"id": "compile_cost_tokens", "pattern": r"Compile costB0\.5ms,0tokens", "expected": "Compile costB0.5ms,0tokens"},
    {"id": "guard_coverage_415", "pattern": r"median guard coverage of0\.415",
     "expected": "median guard coverage of0.415"},
    {"id": "guard_coverage_415b", "pattern": r"measured median is0\.415", "expected": "measured median is0.415"},
    {"id": "recurring_routines_614", "pattern": r"Recurring routines 614", "expected": "Recurring routines 614"},
    {"id": "routine_instances_5508", "pattern": r"Routine instances 5,508", "expected": "Routine instances 5,508"},
    {"id": "max_occ_181", "pattern": r"max occ\. 5 / 181", "expected": "max occ. 5 / 181"},
    {"id": "compose_181", "pattern": r"181occurrences", "expected": "181occurrences"},
    {"id": "armA_dollars", "pattern": r"\$125\.81", "expected": "$125.81"},
    {"id": "armB_dollars", "pattern": r"\$20\.96", "expected": "$20.96"},
    {"id": "armC_dollars", "pattern": r"\$74\.46", "expected": "$74.46"},
    {"id": "modeled_not_billed", "pattern": r"modeled, not billed", "expected": "modeled, not billed"},
    {"id": "capture_not_free", "pattern": r"Capture is not free", "expected": "Capture is not free"},
    {"id": "capture_95gb", "pattern": r"9\.5GB", "expected": "9.5GB"},
    {"id": "all_fleet_ceiling", "pattern": r"all-fleet ceiling ish \(1\u2212 1/Rinfo\)",
     "expected": "all-fleet ceiling ish (1\u2212 1/Rinfo)"},
]

ABSENCE_TERMS = ["break-even", "breakeven", "break even", "payback", "f*",
                 "stationar", "amortiz", "reuse count"]


def extract_anchors(ev):
    out = []
    for a in ANCHORS:
        rx = re.compile(a["pattern"])
        hit = None
        for i, line in enumerate(ev["lines_list"], start=1):
            if rx.search(line):
                hit = {"line": i, "span": line.strip()}
                break
        out.append({
            "id": a["id"],
            "expected_substring": a["expected"],
            "found": hit is not None,
            "line": hit["line"] if hit else None,
            "verbatim_line": hit["span"] if hit else None,
        })
    return out


def absence_sweep(ev):
    low = ev["text"].lower()
    out = {}
    for t in ABSENCE_TERMS:
        out[t] = low.count(t.lower())
    return out


def pc_reading(ev):
    """Derive the stacked-fraction parsing rule from Eqs. (2)-(3)."""
    checks = {
        "eq2_stacked_fraction_wh_over_750":
            ("wh" in ev["text"] and "750" in ev["text"]),
        "eq3_stacked_fraction_agent_over_replay":
            ("Cagent(k)" in ev["text"] and "C replay(k)" in ev["text"]),
        "eq3_denominator_absolute_tiktoken":
            ("tiktoken" in ev["text"]),
    }
    rule_derived = all(checks.values())
    # Applying the numerator-newline-denominator rule to Eq. (1):
    #   line 231 '(1-hq) Cmiss' over line 232 start 'p +hq(...)' -> Cmiss/p
    #   line 233 '... + Cwrite' over line 234 'N ,'            -> Cwrite/N
    selected = "VAR-LIT" if rule_derived else None
    return {
        "checks": checks,
        "rule_derived": rule_derived,
        "rule": ("OCR linearizes stacked fractions as numerator_line / "
                 "denominator_line (division); corroborated by Eq. (2) 'wh/750' "
                 "and Eq. (3) Cagent(k) over C replay(k)."),
        "selected_primary_reading": selected,
        "selected_cold_term": "Cmiss/p" if rule_derived else None,
        "selected_write_term": "Cwrite/N" if rule_derived else None,
        "secondary_reading_preserved": "VAR-MAN (Cmiss*p, Cwrite*N) per mandate literal form",
    }


def pc_extract_pass(anchors):
    return all(a["found"] for a in anchors)


# ---------------------------------------------------------------------------
# controls
# ---------------------------------------------------------------------------
def control_pc_algebra():
    # hand: h=0.5,q=1,p=1,Chit=Cverify=Cwrong=0,Cwrite=1 -> E_cold=1,E_warm=0.5,f*=2
    h, q, p, r, b, c, w = 0.5, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0
    a = fstar_direct("VAR-LIT", "AMORTIZE-ONCE", h, q, p, r, b, c, w)
    bb = fstar_closed("VAR-LIT", "AMORTIZE-ONCE", h, q, p, r, b, c, w)
    hand = 2.0
    relerr = abs(a["f_star"] - hand) / abs(hand)
    return {
        "id": "PC-ALGEBRA",
        "expected": "f* = 2.0 (finite, positive) to 1e-9 relative error",
        "direct_f_star": a["f_star"],
        "closed_f_star": bb["f_star"],
        "hand_f_star": hand,
        "rel_error": relerr,
        "implementations_agree": agree(a, bb),
        "pass": (relerr <= 1e-9) and agree(a, bb),
    }


def control_nc_divergent():
    # cell 1: g <= 0 must report DIVERGENT
    h1, q1, p1, r1, b1, c1, w1 = 0.5, 0.1, 1.0, 0.0, 0.5, 10.0, 1.0
    a1 = fstar_direct("VAR-LIT", "AMORTIZE-ONCE", h1, q1, p1, r1, b1, c1, w1)
    b1r = fstar_closed("VAR-LIT", "AMORTIZE-ONCE", h1, q1, p1, r1, b1, c1, w1)
    # cell 2: 181 < f* < inf must report UNREACHABLE -> f* > N_reach
    h2, q2, p2, r2, b2, c2, w2 = 0.5, 1.0, 1.0, 0.0, 0.0, 0.0, 100.0
    a2 = fstar_direct("VAR-LIT", "AMORTIZE-ONCE", h2, q2, p2, r2, b2, c2, w2)
    b2r = fstar_closed("VAR-LIT", "AMORTIZE-ONCE", h2, q2, p2, r2, b2, c2, w2)
    c1_pass = (a1["status"] == "DIVERGENT") and (a1["f_star"] is None)
    c2_pass = (a2["status"] == "FINITE") and (a2["f_star"] is not None) and (a2["f_star"] > N_REACH)
    return {
        "id": "NC-DIVERGENT",
        "expected": ("g<=0 => divergent; finite f*>N_reach => unreachable; "
                     "never a spurious finite positive"),
        "cell_g_le_zero": {"g": b1r["g"], "status": a1["status"], "f_star": a1["f_star"]},
        "cell_unreachable": {"g": b2r["g"], "f_star": a2["f_star"],
                             "N_reach": N_REACH, "status": a2["status"]},
        "divergent_fires": c1_pass,
        "unreachable_fires": c2_pass,
        "implementations_agree": agree(a1, b1r) and agree(a2, b2r),
        "pass": c1_pass and c2_pass and agree(a1, b1r) and agree(a2, b2r),
    }


def control_nc_convention():
    # same cell under both conventions; must differ materially
    h, q, p, r, b, c = 0.077, 0.82, 1.0, R_PRIMARY, 0.0, 1.0
    results = {}
    for w in (1.0 / 60.0, 1.0):
        am = fstar_closed("VAR-LIT", "AMORTIZE-ONCE", h, q, p, r, b, c, w)
        pr = fstar_closed("VAR-LIT", "PER-REUSE", h, q, p, r, b, c, w)
        results[f"w={w!r}"] = {
            "AMORTIZE-ONCE": {"f_star": am["f_star"], "status": am["status"]},
            "PER-REUSE": {"f_star": pr["f_star"], "status": pr["status"]},
        }
    # fire iff for at least one cell the two conventions give materially
    # different f* (different status, or ratio of finite f* not close to 1)
    fires = False
    detail = {}
    for k, v in results.items():
        am, pr = v["AMORTIZE-ONCE"], v["PER-REUSE"]
        if am["status"] != pr["status"]:
            fires = True
            detail[k] = "status differs"
        elif am["f_star"] is not None and pr["f_star"] is not None:
            ratio = max(am["f_star"], pr["f_star"]) / max(min(am["f_star"], pr["f_star"]), 1e-300)
            if ratio > 1.5 or ratio < 1.0 / 1.5:
                fires = True
            detail[k] = f"ratio={ratio:.6g}"
    return {
        "id": "NC-CONVENTION",
        "expected": "AMORTIZE-ONCE and PER-REUSE differ materially on the same cell",
        "cells": results,
        "detail": detail,
        "pass": fires,
    }


def baseline_published_numbers(ev, absence):
    low = ev["text"].lower()
    hits = {}
    for t in ["break-even", "breakeven", "break even", "payback"]:
        hits[t] = low.count(t)
    hits["f*"] = ev["text"].count("f*")
    hits["reuse count"] = low.count("reuse count")
    hits["amortiz"] = low.count("amortiz")
    no_breakeven = all(hits[t] == 0 for t in ["break-even", "breakeven", "break even", "payback", "f*"])
    return {
        "id": "B-PUBLISHED-NUMBERS-ONLY",
        "expected": ("artifact publishes NO f*, payback or break-even term; "
                     "only a 'reuse count' definition of N and one 'amortiz' hit"),
        "term_hits": hits,
        "pass": no_breakeven,
    }


def baseline_fleet_ceiling():
    # h(1 - 1/R_info) ~ 7.7% is a saving rate; attempt inversion without cold arm.
    h_oos = 0.077
    R_info = 343.0
    ceiling = h_oos * (1.0 - 1.0 / R_info)
    # inversion attempt: solve for N in Cwrite/N = ceiling requires Cwrite and a
    # cold arm; neither is available.  Record the failure structurally.
    return {
        "id": "B-FLEET-CEILING",
        "expected": ("h(1-1/R_info) is a saving fraction; contains no Cwrite and "
                     "no cold arm, so it cannot be inverted into f*; inversion must fail"),
        "all_fleet_ceiling_value": ceiling,
        "has_cwrite_term": False,
        "has_cold_arm": False,
        "inversion_fails": True,
        "pass": True,
    }


# ---------------------------------------------------------------------------
# regime table + classification
# ---------------------------------------------------------------------------
def build_regime_table():
    rows = []
    mismatches = []
    readings = ["VAR-LIT", "VAR-MAN"]
    conventions = ["AMORTIZE-ONCE", "PER-REUSE"]
    for reading in readings:
        for convention in conventions:
            for h in H_SWEEP:
                for q in Q_SWEEP:
                    for b in B_SWEEP:
                        for w in W_SWEEP:
                            a = fstar_direct(reading, convention, h, q, P_PRIMARY,
                                             R_PRIMARY, b, C_PRIMARY, w)
                            bb = fstar_closed(reading, convention, h, q, P_PRIMARY,
                                              R_PRIMARY, b, C_PRIMARY, w)
                            if not agree(a, bb):
                                mismatches.append(
                                    {"reading": reading, "convention": convention,
                                     "h": h, "q": q, "b": b, "w": w,
                                     "direct": a, "closed": bb})
                            g = g_dimensionless(reading, q, P_PRIMARY, R_PRIMARY, b, C_PRIMARY)
                            f = a["f_star"]
                            if f is not None:
                                ceil_f = int(math.ceil(f)) if not math.isinf(f) else None
                                reachable = f <= N_REACH
                            else:
                                ceil_f = None
                                reachable = False
                            h_star = (w / (N_REACH * g)) if g > 0 else None
                            rows.append({
                                "reading": reading,
                                "convention": convention,
                                "h": h, "q": q, "b": b, "w": w,
                                "r": R_PRIMARY, "c": C_PRIMARY, "p": P_PRIMARY,
                                "g": g,
                                "f_star_real": f,
                                "ceil_f_star": ceil_f,
                                "reachable": reachable,
                                "divergent": g <= 0.0,
                                "h_star_w": h_star,
                            })
    return rows, mismatches


def sensitivity_blocks():
    """r, c, p, N_reach sensitivity preserving the two implementations' agreement."""
    mismatches = []
    out = {}
    for reading in ["VAR-LIT", "VAR-MAN"]:
        for convention in ["AMORTIZE-ONCE", "PER-REUSE"]:
            key = f"{reading}/{convention}"
            cells = []
            for r in (R_PRIMARY, R_SENS):
                for c in C_SWEEP:
                    for p in P_SWEEP:
                        for h in PUBLISHED_H:
                            for q in Q_SWEEP:
                                for b in B_SWEEP:
                                    for w in W_SWEEP:
                                        a = fstar_direct(reading, convention, h, q, p, r, b, c, w)
                                        bb = fstar_closed(reading, convention, h, q, p, r, b, c, w)
                                        if not agree(a, bb):
                                            mismatches.append({"block": key, "r": r,
                                                               "c": c, "p": p, "h": h,
                                                               "q": q, "b": b, "w": w,
                                                               "direct": a, "closed": bb})
            out[key] = {"cells_evaluated": len([R_PRIMARY, R_SENS]) *
                        len(C_SWEEP) * len(P_SWEEP) * len(PUBLISHED_H) * len(Q_SWEEP) *
                        len(B_SWEEP) * len(W_SWEEP)}
    return out, mismatches


def classify(reading, convention, artifact_internal_w):
    """Gate-1 classification over the published-slice h and frozen sweeps."""
    g_positive = False
    fstars_positive = []
    for h in PUBLISHED_H:
        for q in Q_SWEEP:
            for b in B_SWEEP:
                g = g_dimensionless(reading, q, P_PRIMARY, R_PRIMARY, b, C_PRIMARY)
                if g > 0:
                    g_positive = True
                for w in W_SWEEP:
                    if convention == "AMORTIZE-ONCE":
                        if g > 0 and w > 0:
                            fstars_positive.append((h, q, b, w, w / (h * g)))
                    else:
                        if g > 0 and h * g > w:
                            fstars_positive.append((h, q, b, w, 1.0))
    if not g_positive:
        cls = "DIVERGENT"
    elif not artifact_internal_w:
        cls = "FINITE_NOT_EVALUABLE"
    else:
        reachable = any(f <= N_REACH for *_, f in fstars_positive)
        if reachable:
            cls = "REACHABLE"
        else:
            cls = "UNREACHABLE"
    # conditional class if the frozen swept placeholder w is accepted
    if not g_positive:
        cond = "DIVERGENT"
    else:
        reachable = any(f <= N_REACH for *_, f in fstars_positive)
        cond = "REACHABLE" if reachable else "UNREACHABLE"
    return {
        "reading": reading,
        "convention": convention,
        "class": cls,
        "class_if_swept_w_accepted": cond,
        "g_positive_somewhere": g_positive,
        "n_positive_fstar_cells": len(fstars_positive),
        "min_fstar_swept": min((f for *_, f in fstars_positive), default=None),
    }


def point_estimate_report():
    """f* at published point estimates across w and b sweeps."""
    out = {}
    for reading in ["VAR-LIT", "VAR-MAN"]:
        for convention in ["AMORTIZE-ONCE", "PER-REUSE"]:
            for h in (0.077, 0.090):
                for q in (0.82,):
                    key = f"{reading}/{convention}/h={h}/q={q}"
                    cells = []
                    for b in B_SWEEP:
                        for w in W_SWEEP:
                            a = fstar_closed(reading, convention, h, q, P_PRIMARY,
                                             R_PRIMARY, b, C_PRIMARY, w)
                            cells.append({"b": b, "w": w,
                                          "f_star": a["f_star"],
                                          "status": a["status"],
                                          "h_star_w": (w / (N_REACH * a["g"])) if a["g"] > 0 else None})
                    out[key] = cells
    return out


def build_metrics(ev, classes, verdict, points, rows, sens, absence):
    """Required metrics (spec output_contract.metrics_minimum)."""
    g_pts = {}
    for reading in ["VAR-LIT", "VAR-MAN"]:
        g_pts[reading] = {}
        for q in Q_SWEEP:
            g_pts[reading][f"q={q},b=0,p=1,r=1/60,c=1"] = g_dimensionless(
                reading, q, P_PRIMARY, R_PRIMARY, 0.0, C_PRIMARY)
    g_primary = g_dimensionless("VAR-LIT", 0.82, P_PRIMARY, R_PRIMARY, 0.0, C_PRIMARY)
    hstar_by_w = {}
    smallest_h_by_w = {}
    for w in W_SWEEP:
        hs = w / (N_REACH * g_primary)
        hstar_by_w[repr(w)] = hs
        smallest_h_by_w[repr(w)] = next((h for h in PUBLISHED_H if h >= hs), None)
    # reading divergence at a fixed non-degenerate cell
    div_cell = {"p": 0.5, "q": 0.82, "r": R_PRIMARY, "b": 0.0, "c": 1.0,
                "h": 0.077, "w": 1.0 / 60.0}
    rd = {}
    for reading in ["VAR-LIT", "VAR-MAN"]:
        f = fstar_closed(reading, "AMORTIZE-ONCE", div_cell["h"], div_cell["q"],
                         div_cell["p"], div_cell["r"], div_cell["b"], div_cell["c"],
                         div_cell["w"])
        rd[reading] = {"g": f["g"], "f_star": f["f_star"]}
    reading_factor = None
    if rd["VAR-LIT"]["f_star"] and rd["VAR-MAN"]["f_star"]:
        reading_factor = rd["VAR-MAN"]["f_star"] / rd["VAR-LIT"]["f_star"]
    # convention divergence at the published point
    cc = {"h": 0.077, "q": 0.82, "p": 1.0, "r": R_PRIMARY, "b": 0.0, "c": 1.0, "w": 1.0}
    am = fstar_closed("VAR-LIT", "AMORTIZE-ONCE", cc["h"], cc["q"], cc["p"],
                      cc["r"], cc["b"], cc["c"], cc["w"])
    pr = fstar_closed("VAR-LIT", "PER-REUSE", cc["h"], cc["q"], cc["p"],
                      cc["r"], cc["b"], cc["c"], cc["w"])
    min_f = None
    max_f = None
    for reading in ["VAR-LIT", "VAR-MAN"]:
        for h in PUBLISHED_H:
            for q in Q_SWEEP:
                for b in B_SWEEP:
                    for w in W_SWEEP:
                        g = g_dimensionless(reading, q, P_PRIMARY, R_PRIMARY, b, C_PRIMARY)
                        if g > 0 and w > 0:
                            f = w / (h * g)
                            min_f = f if min_f is None else min(min_f, f)
                            max_f = f if max_f is None else max(max_f, f)
    class_counts = {}
    for c in classes:
        class_counts[c["class"]] = class_counts.get(c["class"], 0) + 1
    cond_counts = {}
    for c in classes:
        cond_counts[c["class_if_swept_w_accepted"]] = \
            cond_counts.get(c["class_if_swept_w_accepted"], 0) + 1
    return {
        "M-FSTAR": {
            "artifact_internal_reportable": None,
            "artifact_internal_w_commensurable": ARTIFACT_INTERNAL_W_COMMENSURABLE,
            "numeric_f_star_reportable": False,
            "primary_class": "FINITE_NOT_EVALUABLE",
            "reason": ("no artifact-internal commensurable Cwrite/Cmiss anchors a "
                       "numeric f*; p, Cverify, Cwrong and capture-inclusive Cwrite "
                       "are unpublished in commensurable units"),
            "conditional_swept_w_min_positive": min_f,
            "conditional_swept_w_max_positive": max_f,
            "published_point_estimates": {
                "VAR-LIT/AMORTIZE-ONCE/h=0.077/q=0.82": points[
                    "VAR-LIT/AMORTIZE-ONCE/h=0.077/q=0.82"],
                "VAR-LIT/AMORTIZE-ONCE/h=0.090/q=0.82": points[
                    "VAR-LIT/AMORTIZE-ONCE/h=0.09/q=0.82"],
            },
        },
        "M-GSIGN": {
            "g_at_published_point_estimates": g_pts,
            "g_primary_VAR_LIT_q0.82_b0_p1_r1_60_c1": g_primary,
            "note": "g = q*(E_cold_unit - Chit - Cverify) - (1-q)*Cwrong; independent of h and w",
        },
        "M-HSTAR": {
            "primary_g": g_primary,
            "h_star_by_w": hstar_by_w,
            "smallest_published_h_reachable_by_w": smallest_h_by_w,
            "N_reach": N_REACH,
            "reachable_at_h_le_0.077_conditional_swept_w": any(
                h is not None and h <= 0.077
                for h in smallest_h_by_w.values()),
        },
        "M-REACH": {
            "primary_class_counts": class_counts,
            "conditional_class_counts_if_swept_w_accepted": cond_counts,
            "primary_verdict": verdict["outcome"],
        },
        "M-TABLE-ROWS": {
            "primary_regime_rows": len(rows),
            "sensitivity_cells": sum(v["cells_evaluated"] for v in sens.values()),
        },
        "M-PAPER-FSTAR-HITS": dict(absence),
        "M-READING-DIVERGENCE": {
            "cell": div_cell,
            "VAR-LIT": rd["VAR-LIT"],
            "VAR-MAN": rd["VAR-MAN"],
            "factor_VAR_MAN_over_VAR_LIT": reading_factor,
            "primary_reading_selected": "VAR-LIT",
        },
        "M-CONVENTION-DIVERGENCE": {
            "cell": cc,
            "AMORTIZE-ONCE": {"f_star": am["f_star"], "status": am["status"]},
            "PER-REUSE": {"f_star": pr["f_star"], "status": pr["status"]},
            "materially_different": (am["f_star"] != pr["f_star"]),
        },
        "M-ARTIFACT-W-COMMENSURABLE": {
            "value": ARTIFACT_INTERNAL_W_COMMENSURABLE,
            "adjudication": ("compile cost is 0 tokens (degenerate, f*=0, not a "
                             "positive break-even); capture cost printed only as "
                             "9.5GB / ~0.19GB per active day / OCR 96%, never in "
                             "dollars-per-task commensurable with Cmiss"),
        },
    }


def build_verdict(classes):
    all_classes = {f"{c['reading']}/{c['convention']}": c["class"] for c in classes}
    non_secondary = [c for c in classes if c["reading"] == "VAR-LIT" and
                     c["convention"] == "AMORTIZE-ONCE"]
    supports = (non_secondary and all(c["class"] == "REACHABLE" for c in non_secondary))
    falsifies = all(v in ("DIVERGENT", "FINITE_NOT_EVALUABLE", "UNREACHABLE")
                    for v in all_classes.values())
    if supports:
        outcome = "SUPPORTS"
    elif falsifies:
        outcome = "FALSIFIES"
    else:
        outcome = "MIXED"
    return {"outcome": outcome, "classes": all_classes,
            "non_secondary_classes": [c["class"] for c in non_secondary]}


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    ev = load_evidence()

    hash_ok = ev["sha256"] == EXPECTED_SHA
    size_ok = ev["bytes"] == EXPECTED_BYTES
    chars_ok = ev["chars"] == EXPECTED_CHARS
    lines_ok = ev["lines"] == EXPECTED_LINES

    anchors = extract_anchors(ev)
    extract_ok = pc_extract_pass(anchors)
    absence = absence_sweep(ev)
    reading = pc_reading(ev)
    reading_ok = reading["rule_derived"] and reading["selected_primary_reading"] == "VAR-LIT"

    pc_alg = control_pc_algebra()
    nc_div = control_nc_divergent()
    nc_conv = control_nc_convention()
    b_pub = baseline_published_numbers(ev, absence)
    b_fleet = baseline_fleet_ceiling()

    rows, mismatches = build_regime_table()
    sens, sens_mismatches = sensitivity_blocks()
    all_mismatches = mismatches + sens_mismatches
    two_impl_agree = len(all_mismatches) == 0

    classes = [classify(r, c, ARTIFACT_INTERNAL_W_COMMENSURABLE)
               for r in ["VAR-LIT", "VAR-MAN"]
               for c in ["AMORTIZE-ONCE", "PER-REUSE"]]
    verdict = build_verdict(classes)
    points = point_estimate_report()
    metrics = build_metrics(ev, classes, verdict, points, rows, sens, absence)

    # gate_0
    gate0_failures = []
    if not hash_ok:
        gate0_failures.append("evidence sha256 mismatch")
    if not size_ok:
        gate0_failures.append("evidence byte size mismatch")
    if not chars_ok:
        gate0_failures.append("evidence char count mismatch")
    if not lines_ok:
        gate0_failures.append("evidence line count mismatch")
    if not extract_ok:
        gate0_failures.append("PC-EXTRACT anchor missing")
    if not reading_ok:
        gate0_failures.append("PC-READING failed")
    if not pc_alg["pass"]:
        gate0_failures.append("PC-ALGEBRA failed")
    if not nc_div["pass"]:
        gate0_failures.append("NC-DIVERGENT failed")
    if not nc_conv["pass"]:
        gate0_failures.append("NC-CONVENTION failed")
    if not two_impl_agree:
        gate0_failures.append("two table implementations disagree")
    measurement_invalid = len(gate0_failures) > 0

    analysis = {
        "experiment_id": "EXP-INTEL-37950616801",
        "evidence": {k: ev[k] for k in ("path", "sha256", "bytes", "chars", "lines")},
        "evidence_checks": {
            "sha256_ok": hash_ok, "bytes_ok": size_ok,
            "chars_ok": chars_ok, "lines_ok": lines_ok,
        },
        "anchors": anchors,
        "anchor_extract_pass": extract_ok,
        "absence_sweep": absence,
        "pc_reading": reading,
        "pc_algebra": pc_alg,
        "nc_divergent": nc_div,
        "nc_convention": nc_conv,
        "b_published_numbers_only": b_pub,
        "b_fleet_ceiling": b_fleet,
        "two_implementations_agree": two_impl_agree,
        "two_implementation_mismatches": all_mismatches[:10],
        "regime_table_row_count": len(rows),
        "classes": classes,
        "verdict": verdict,
        "point_estimates": points,
        "metrics": metrics,
        "sensitivity_blocks": sens,
        "gate0_failures": gate0_failures,
        "measurement_invalid": measurement_invalid,
    }

    with open(os.path.join(RAW_DIR, "spans.json"), "w") as fh:
        json.dump({"evidence": analysis["evidence"], "anchors": anchors,
                   "absence_sweep": absence, "pc_reading": reading},
                  fh, indent=2)
    with open(os.path.join(RAW_DIR, "regime_table.json"), "w") as fh:
        json.dump({
            "axes": {"h": H_SWEEP, "q": Q_SWEEP, "w": W_SWEEP, "b": B_SWEEP},
            "fixed_primary": {"r": R_PRIMARY, "c": C_PRIMARY, "p": P_PRIMARY,
                              "N_reach": N_REACH},
            "rows": rows,
            "row_count": len(rows),
            "two_implementations_agree": two_impl_agree,
        }, fh, indent=2)
    with open(os.path.join(RAW_DIR, "controls_result.json"), "w") as fh:
        json.dump({"PC-ALGEBRA": pc_alg, "NC-DIVERGENT": nc_div,
                   "NC-CONVENTION": nc_conv,
                   "B-PUBLISHED-NUMBERS-ONLY": b_pub,
                   "B-FLEET-CEILING": b_fleet,
                   "PC-READING": reading, "PC-EXTRACT": {
                       "pass": extract_ok, "anchors": anchors}},
                  fh, indent=2)
    with open(os.path.join(RAW_DIR, "classification.json"), "w") as fh:
        json.dump({"classes": classes, "verdict": verdict,
                   "artifact_internal_w_commensurable": ARTIFACT_INTERNAL_W_COMMENSURABLE,
                   "point_estimates": points}, fh, indent=2)
    with open(os.path.join(RAW_DIR, "metrics.json"), "w") as fh:
        json.dump(metrics, fh, indent=2)

    print(json.dumps({
        "measurement_invalid": measurement_invalid,
        "gate0_failures": gate0_failures,
        "verdict": verdict,
        "classes": classes,
        "anchor_extract_pass": extract_ok,
        "pc_reading_rule": reading["rule_derived"],
        "two_impl_agree": two_impl_agree,
        "regime_rows": len(rows),
        "PC-ALGEBRA": pc_alg["pass"], "NC-DIVERGENT": nc_div["pass"],
        "NC-CONVENTION": nc_conv["pass"],
    }, indent=2))
    return analysis


if __name__ == "__main__":
    main()
