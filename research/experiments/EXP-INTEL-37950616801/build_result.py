#!/usr/bin/env python3
"""Assemble the canonical result.json for EXP-INTEL-37950616801.

Reads the raw derived artifacts produced by run_determination.py and emits the
producer handoff with the exact required top-level shape.
"""
import hashlib
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw")


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def rel(p):
    return os.path.relpath(p, os.path.dirname(os.path.dirname(os.path.dirname(BASE))))


with open(os.path.join(RAW, "metrics.json")) as fh:
    metrics = json.load(fh)
with open(os.path.join(RAW, "classification.json")) as fh:
    cls = json.load(fh)
with open(os.path.join(RAW, "spans.json")) as fh:
    spans = json.load(fh)
with open(os.path.join(RAW, "controls_result.json")) as fh:
    ctl = json.load(fh)

pc_alg = ctl["PC-ALGEBRA"]
nc_div = ctl["NC-DIVERGENT"]
nc_conv = ctl["NC-CONVENTION"]
b_pub = ctl["B-PUBLISHED-NUMBERS-ONLY"]
b_fleet = ctl["B-FLEET-CEILING"]
pc_read = ctl["PC-READING"]
pc_ext = ctl["PC-EXTRACT"]

controls = {
    "PC-ALGEBRA": {
        "expected_behavior": pc_alg["expected"],
        "observed_behavior": {
            "engine_f_star": pc_alg["direct_f_star"],
            "hand_f_star": pc_alg["hand_f_star"],
            "rel_error": pc_alg["rel_error"],
            "two_implementations_agree": pc_alg["implementations_agree"],
        },
        "pass": pc_alg["pass"],
        "evidence_ref": "raw/controls_result.json#PC-ALGEBRA",
    },
    "NC-DIVERGENT": {
        "expected_behavior": nc_div["expected"],
        "observed_behavior": {
            "divergent_cell": nc_div["cell_g_le_zero"],
            "unreachable_cell": nc_div["cell_unreachable"],
            "divergent_fires": nc_div["divergent_fires"],
            "unreachable_fires": nc_div["unreachable_fires"],
        },
        "pass": nc_div["pass"],
        "evidence_ref": "raw/controls_result.json#NC-DIVERGENT",
    },
    "PC-READING": {
        "expected_behavior": ("derive numerator-line/denominator-line (division) "
                             "parsing rule from Eqs. (2)-(3), apply to Eq. (1)"),
        "observed_behavior": {
            "checks": pc_read["checks"],
            "selected_primary_reading": pc_read["selected_primary_reading"],
            "selected_cold_term": pc_read["selected_cold_term"],
            "selected_write_term": pc_read["selected_write_term"],
        },
        "pass": bool(pc_read["rule_derived"] and
                     pc_read["selected_primary_reading"] == "VAR-LIT"),
        "evidence_ref": "raw/spans.json#pc_reading",
    },
    "PC-EXTRACT": {
        "expected_behavior": ("independently re-extract frozen anchors (R 60/343, "
                             "h slice, q~82%, compile 0 tokens, guard 0.415, "
                             "5,508/614 routines, max occ 181, arm dollars)"),
        "observed_behavior": {
            "anchors_total": len(pc_ext["anchors"]),
            "anchors_found": sum(1 for a in pc_ext["anchors"] if a["found"]),
            "anchors_missing": [a["id"] for a in pc_ext["anchors"] if not a["found"]],
            "anchor_lines": {a["id"]: a["line"] for a in pc_ext["anchors"]},
        },
        "pass": pc_ext["pass"],
        "evidence_ref": "raw/spans.json",
    },
    "NC-CONVENTION": {
        "expected_behavior": nc_conv["expected"],
        "observed_behavior": {"cells": nc_conv["cells"], "detail": nc_conv["detail"]},
        "pass": nc_conv["pass"],
        "evidence_ref": "raw/controls_result.json#NC-CONVENTION",
    },
    "B-PUBLISHED-NUMBERS-ONLY": {
        "expected_behavior": b_pub["expected"],
        "observed_behavior": {"term_hits": b_pub["term_hits"]},
        "pass": b_pub["pass"],
        "evidence_ref": "raw/controls_result.json#B-PUBLISHED-NUMBERS-ONLY",
    },
    "B-FLEET-CEILING": {
        "expected_behavior": b_fleet["expected"],
        "observed_behavior": {
            "all_fleet_ceiling_value": b_fleet["all_fleet_ceiling_value"],
            "has_cwrite_term": b_fleet["has_cwrite_term"],
            "has_cold_arm": b_fleet["has_cold_arm"],
            "inversion_fails": b_fleet["inversion_fails"],
        },
        "pass": b_fleet["pass"],
        "evidence_ref": "raw/controls_result.json#B-FLEET-CEILING",
    },
}

artifacts = []
for name, role in [
    ("run_determination.py", "code"),
    ("raw/spans.json", "raw"),
    ("raw/regime_table.json", "raw"),
    ("raw/controls_result.json", "raw"),
    ("raw/classification.json", "raw"),
    ("raw/metrics.json", "raw"),
]:
    p = os.path.join(BASE, name)
    artifacts.append({"path": rel(p), "sha256": sha(p), "role": role})

observations = [
    "EVIDENCE VERIFIED: the frozen text layer "
    "research/experiments/EXP-INTEL-36306525220/raw/fulltext/2608.05784v1.txt has "
    "sha256 e286167a6ae51eebe1552f655876bae5a9c1728e16793b31e4adac4e9b154dbf, "
    "70,219 bytes, 69,607 characters, 1,447 lines -- all matching spec.json.",
    "Eq. (1) located verbatim at lines 231-240: 'E[$/task] = (1-hq) Cmiss' / 'p "
    "+hq(C hit+Cverify)' / '+h(1-q)C wrong + Cwrite' / 'N ,' with the cold term "
    "written as Cmiss over p and the write term as Cwrite over N.",
    "Eqs. (2)-(3) at lines 826-854 confirm stacked fractions are OCR-linearized "
    "as numerator-line over denominator-line (division), e.g. 'wh/750' and "
    "Cagent(k) over C replay(k); applied to Eq. (1) this selects VAR-LIT "
    "(cold = Cmiss/p, write = Cwrite/N) as the primary reading.",
    "The artifact publishes ZERO occurrences of 'break-even', 'breakeven', 'break "
    "even', 'payback' and 'f*'; exactly ONE 'amortiz' (line 228) and ONE 'reuse "
    "count' (line 237, the Eq. (1) definition of N); ZERO 'stationar'.",
    "Published anchors re-extracted with line numbers: R_inject=60x (line 876, IQR "
    "59-62), R_info=343x (line 880), h=9.0% (line 973), h=13.1% URL (line 995), "
    "h=8.6% training (line 1010), h=7.7% out-of-sample (lines 1010/1014), entity "
    "typing ~82% and q<1 (lines 1214/1218), compile '<=0.5ms, 0 tokens' (line 912), "
    "median guard coverage 0.415 (lines 943/1171), 614 recurring routines / 5,508 "
    "instances (lines 908-909), max occurrences 181 (lines 893/919), modeled arm "
    "dollars $125.81/$20.96/$74.46 (lines 954-957).",
    "g (the dimensionless saving bracket) at the artifact's published point "
    "estimates (r=1/60, b=0, c=1, p=1): g=+0.6263 at q=0.82 (entity typing), "
    "g=+0.9833 at q=1.0, and g=-0.1769 at q=0.415 (the guard-coverage proxy, not "
    "Eq. (1)'s q). g is independent of h and w, so structural divergence does not "
    "hold at the published q~0.82.",
    "Conditional on accepting the frozen placeholder w sweep, f* at the published "
    "point estimate (h=0.077, q=0.82, r=1/60, b=0, c=1, p=1) is: 0.346 for "
    "w=1/60, 0.0605 for w=1/343, 20.74 for w=1, 207.35 for w=10; f*=0 at w=0. At "
    "h=0.090 the same w values give 0.296, 0.0517, 17.74 and 177.40.",
    "The artifact prints compile cost only as '0 tokens' (a zero dollar write, "
    "f*=0, not a positive break-even) and capture/storage cost only as '9.5GB', "
    "'~0.19GB per active day' and 'OCR runs on 96% of frames' (lines 1202-1207); "
    "it never prints Cwrite in dollars-per-task commensurable with Cmiss. The base "
    "success rate p ('base success rate', line 237) is never published numerically; "
    "Cverify and Cwrong are likewise not published.",
    "The two independent implementations of the f* engine (direct cold/warm "
    "evaluator and dimensionless closed form f*=w/(h*g)) agree at all 1,680 primary "
    "regime cells and all 17,280 sensitivity cells with zero mismatches.",
    "PC-ALGEBRA reproduces the hand-computed f*=2.0 at h=0.5,q=1,p=1,Chit=Cverify="
    "Cwrong=0,Cwrite=1 to relative error 0.0; NC-DIVERGENT fires both the g<=0 "
    "divergent branch and the f*>N_reach unreachable branch; NC-CONVENTION shows "
    "AMORTIZE-ONCE f*=20.74 versus PER-REUSE NO_FSTAR_DEGENERATE on the same cell.",
    "The artifact's strongest published economics quantity, the all-fleet ceiling "
    "h(1-1/R_info), evaluates to 0.07677 (7.7%) -- a saving fraction with no "
    "Cwrite term and no cold arm, so it cannot be inverted into a break-even.",
    "PRIMARY CLASSIFICATION (no artifact-internal commensurable w): all four "
    "(reading, convention) combinations classify FINITE_NOT_EVALUABLE -- g>0 "
    "somewhere, but no artifact-internal commensurable Cwrite/Cmiss anchors a "
    "numeric f*. Verdict per frozen gate_2: FALSIFIES.",
    "CONDITIONAL SENSITIVITY: if the frozen placeholder w sweep is accepted as a "
    "reportable input, all four combinations classify REACHABLE, and the reachable "
    "region includes h<=0.077 for w in {1/60, 1/343, 1} (h*<=0.0088); w=10 needs "
    "h>=0.0882. This conditional branch is recorded, not adopted.",
]

validity_notes = [
    "Scope: this is a reportability determination about ONE hash-pinned artifact "
    "(arXiv:2608.05784v1 text layer), not a prevalence claim over persistent-state "
    "economics literature.",
    "ADJUDICATED AXIS (frozen by spec, decided here): no artifact-internal "
    "commensurable w=Cwrite/Cmiss exists. The compile cost is literally 0 tokens "
    "(degenerate f*=0, not a positive break-even), while the real persistent-write "
    "cost includes capture, printed only in GB/wall-clock; p, Cverify and Cwrong "
    "are never published in commensurable units. Hence the primary class is "
    "FINITE_NOT_EVALUABLE and only the critical-h locus h*(w)=w/(N_reach*g) is "
    "reportable without external inputs.",
    "The opposite adjudication (accepting the swept placeholder w) yields "
    "REACHABLE and is reported as an explicit conditional sensitivity in "
    "metrics['M-REACH'] and observations; the DIRECTOR may reopen that axis, but "
    "as frozen the placeholder values are not artifact measurements.",
    "The preserved equation is OCR-linearized; the multiply-vs-divide ambiguity "
    "(Cmiss/p vs Cmiss*p; Cwrite/N vs Cwrite*N) is reported per reading and never "
    "silently collapsed. PC-READING selected VAR-LIT as primary; VAR-MAN is "
    "carried as the mandate's literal secondary reading.",
    "p is unpublished numerically and swept over {0.5,0.8,1.0}; the reported "
    "classification is not robust to p only through g, and the published-slice "
    "cells with g>0 persist under the primary parameters.",
    "The corpus is one professional over 51 active days / 128,756 frames; R's "
    "numerator, the three-arm dollars and the all-fleet ceiling are explicitly "
    "'modeled, not billed' (lines 1160-1168); this experiment preserves those "
    "labels.",
    "Non-adoption bar preserved: no quantity from arXiv:2608.05784v1 enters a "
    "SPIDER cost model, break-even derivation, product plan or investor-facing "
    "material. The artifact is the object of a reportability analysis, not a "
    "comparator or input.",
    "Measurement validity: gate_0 passed all checks -- evidence hash/byte/char/line "
    "match, PC-EXTRACT recovered all 34 anchors, PC-READING derived the rule, "
    "PC-ALGEBRA reproduced the hand value, NC-DIVERGENT fired both branches, "
    "NC-CONVENTION fired, and the two table implementations agree at every cell.",
    "f* is reported as a real number with the integer horizon ceil(f*) noted; "
    "reachability is f*<=N_reach=181, the artifact's own maximum routine "
    "occurrences (the most generous horizon), so a positive finding would be "
    "conservative.",
    "Outcome FALSIFIES is a statement about reportability from THIS artifact: a "
    "numeric f* with a stated denominator is not derivable from the artifact's own "
    "published values. It is NOT a literature-level negative and does not measure "
    "SPIDER's own recurrence.",
]

unresolved = [
    "Whether any OTHER published persistent-state artifact reports Cwrite/Cmiss in "
    "commensurable units, which would make a measured f* reportable; not examined "
    "here and out of scope.",
    "Whether the frozen placeholder w sweep should be treated as a legitimate "
    "'explicitly-swept input' for a REACHABLE class (the conditional branch "
    "recorded here) or as an external assumption (the primary FINITE_NOT_EVALUABLE "
    "class). This is the single adjudication that moves the verdict between "
    "FALSIFIES and SUPPORTS; DIRECTOR owns the bounded decision.",
    "SPIDER's own first-party marginal recurrence h(N) and write cost Cwrite on the "
    "shipped path remain unmeasured.",
    "Whether the compile 0-token cost and the separately printed capture cost "
    "(GB/active-day, OCR duty cycle) can be converted into a commensurable "
    "dollar-per-task Cwrite using the artifact's own Sonnet pricing; the artifact "
    "does not do so and this experiment did not adopt external prices.",
]

result = {
    "schema_version": 1,
    "experiment_id": "EXP-INTEL-37950616801",
    "lane": "intel",
    "status": "COMPLETE",
    "outcome": "FALSIFIES",
    "metrics": metrics,
    "controls": controls,
    "artifacts": artifacts,
    "observations": observations,
    "validity_notes": validity_notes,
    "unresolved": unresolved,
}

with open(os.path.join(BASE, "result.json"), "w") as fh:
    json.dump(result, fh, indent=2)

print("wrote result.json:", os.path.join(BASE, "result.json"))
print("status", result["status"], "outcome", result["outcome"])
print("controls pass:",
      {k: v["pass"] for k, v in controls.items()})
