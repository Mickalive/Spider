#!/usr/bin/env python3
"""EXP-INTEL-36306525220 :: Stage 3b -- field determinations with verbatim evidence.

Every quoted string is produced by locating an anchor substring in the retrieved text
and slicing a window around it, so the quote is verbatim by construction and the
script re-verifies it.  A field is only EXTRACTED when such a window exists; a field
that no pattern reached is recorded NOT_REPORTED_IN_RETRIEVED_TEXT together with the
retrieval scope, which is the instrument-level form of ABSENCE_AS_ABSENCE
(spec.json measurement_validity[4]): absence from the retrieved text is never
converted into a negative value or into a NOT_FOUND row.

The determinations below were authored after reading raw/spans.json, i.e. after the
RAW EVIDENCE stage.  They are DERIVED MEASUREMENTS, not observations.
"""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolve_identity import RAW, now  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(RAW, "fulltext")
ART = os.path.join(RAW, "artifacts")


def text_for(cid: str) -> tuple[str, str]:
    base = cid.split("v")[0]
    for p in (os.path.join(TXT, base + ".txt"), os.path.join(TXT, cid + ".txt")):
        if os.path.exists(p):
            return open(p, encoding="utf-8", errors="replace").read(), "full_text"
    for p in (os.path.join(ART, cid + ".json"), os.path.join(ART, "ctrl_" + cid + ".json"),
              os.path.join(ART, base + "_base.json")):
        if os.path.exists(p):
            rec = json.load(open(p, encoding="utf-8"))
            return ((rec.get("title") or "") + ". " + (rec.get("abstract") or "")), "abstract_only"
    return "", "none"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def quote(cid: str, anchor: str, pre: int = 0, post: int = 200) -> dict | None:
    t, scope = text_for(cid)
    nt = norm(t)
    na = norm(anchor)
    i = nt.find(na)
    if i < 0:
        return None
    s = max(0, i - pre)
    e = min(len(nt), i + len(na) + post)
    w = nt[s:e]
    return {"quote": w, "scope": scope, "anchor": na, "quote_len_chars": len(w),
            "anchor_offset_normalized": i, "source_chars_searched": len(t)}


# ---------------------------------------------------------------------------
# Determinations.  value semantics: a number, a string, or None (=not reported).
# ---------------------------------------------------------------------------
AF = "2608.05784v1"
WV = "2401.13919v4"
WA = "2307.13854v3"
M2W = "2306.06070v3"
WS = "2207.01206v4"
AB = "2308.03688v2"

D: list[dict] = []


def add(part, system, benchmark, field, value, denominator, convention, uncertainty,
        mvm, anchor, pre=0, post=220, absence=None, cid=AF, note=None, extra=None,
        determination=None):
    q = quote(cid, anchor, pre, post) if anchor else None
    if determination is None:
        determination = "EXTRACTED" if q else "NOT_REPORTED_IN_RETRIEVED_TEXT"
    row = {
        "part": part, "system": system, "benchmark": benchmark, "field": field,
        "value": value, "denominator": denominator, "accounting_convention": convention,
        "stated_uncertainty": uncertainty, "modeled_vs_measured": mvm,
        "source_arxiv_id": cid, "evidence_quote": q["quote"] if q else None,
        "evidence_quote_scope": q["scope"] if q else None,
        "evidence_for_absence": absence,
        "determination": determination,
        "note": note,
    }
    if extra:
        row.update(extra)
    D.append(row)


# ===== Part 1 : cost accounting, target: PC artifact arXiv:2608.05784v1 =====
add(1, "ActivityFrames", None, "Routine_Overhead_Ratio_R", 60.0,
    "per routine instance; Rinject computed on the 20 most frequent action routines "
    "(614 recurring routines / 5,508 routine instances at action granularity)",
    "R = Cagent(k)/Creplay(k). NUMERATOR MODELED (what a memoryless screenshot-driven loop would "
    "spend, computed without executing an agent, an upper bound), DENOMINATOR MEASURED (the emitted "
    "guarded plan / minimal script, tokenized deterministically). Tokens counted "
    "with tiktoken under cl100k_base; priced with Anthropic's w*h/750 image-token rule "
    "plus a 350-token context read and 180 reasoning-output tokens per step",
    "IQR 59-62x across the 20 compiled plans; min-max 167-509x",
    "modeled",
    "the median is Rinject = 60", pre=140, post=260,
    note="Ladder: operational rung Rinject=60x (guarded skill plan, median plan 248 tokens); "
         "ceiling rung Rinfo=343x (minimal replay script, median 40 tokens); recurrence-weighted "
         "mean 337x; across screen resolutions 259-425x.")

add(1, "ActivityFrames", None, "Routine_Overhead_Ratio_R_ceiling_rung", 343.0,
    "per routine instance; 614 recurring / 5,508 instances action granularity; 261 recurring / "
    "1,303 instances URL granularity",
    "same as operational rung: Rinfo = Cagent(k) / bare-information-content token count, NUMERATOR "
    "MODELED and DENOMINATOR MEASURED",
    "IQR 297-390x action granularity; 165-228x URL granularity; min-max 167-509x / 67-301x",
    "modeled",
    "the information-content ceilingRinfo = 343", pre=120, post=240)

add(1, "ActivityFrames", None, "delegable_recurrence_h", 0.09,
    "fraction of all action steps on the corpus; in-sample; 51 active days / 128,756 frames",
    "fraction of action steps falling inside a >=2-named-target recurring n-gram (k in 3..60, "
    "recurs >=3 times, sessions cut at inter-action gaps > 90 s)",
    "URL-granularity counterpart 13.1%; raw recurrence h_raw=83.1%; temporal holdout "
    "out-of-sample 7.7% vs in-sample-on-training-days 8.6%",
    "measured",
    "delegablerate is hspecific = 9.0", pre=60, post=300,
    note="h is measured, not modeled. The two competing recurrences the paper declines to "
         "claim (Web-era page-revisit rates 40-58%) are explicitly excluded.")

add(1, "ActivityFrames", None, "delegable_recurrence_h_out_of_sample", 0.077,
    "fraction of action steps on the held-out final 11 active days of a 51-day corpus; "
    "routine table fit on the first 40 active days (4,847 routine signatures)",
    "temporal within-user holdout (same user, later in time; NOT a cross-population holdout)",
    "in-sample on the training days themselves 8.6%; drop 8.6%->7.7% attributed to "
    "within-user temporal drift",
    "measured",
    "The out-of-sample predicted hit rate is7.7", pre=170, post=300)

add(1, "ActivityFrames", None, "break_even_reuse_count_fstar", None, None, None, None, None,
    "where h is recurrence, q the fraction of hits correctly matched, p the base success rate, "
    "N the reuse count, and the C-terms per-branch costs", pre=200, post=340,
    absence="NOT_REPORTED_AS_A_COMPUTED_QUANTITY. The reuse count N appears only as a symbol "
            "inside the piecewise cost model of Eq. (1); the paper states 'the one input none of "
            "them measures is h on the pre-delegation passive corpus' and never solves Eq. (1) "
            "for a break-even N, so no f* is reported. Absence established over 69,607 characters "
            "of retrieved full text; 0 pattern hits for break-even/breakeven/break even reuse/"
            "reuse count/payback/amortization point/f*.")

add(1, "ActivityFrames", None, "marginal_cost_cached_vs_derived", 6.0,
    "per routine occurrence, 20 recurring routines, fleet total 32.8 Mtok / $125.81 under arm A",
    "three-arm modeled comparison at Sonnet-class list rates ($3/$15 per Mtok, output fraction "
    "0.07), modeled from measured artifacts and token counts, NOT BILLED; arm B = compiled plan "
    "in context, arm C = deterministic local replay",
    "arm B modeled 83.3% token saving; arm C modeled 40.8% ($74.46, 1.7x); the only live in-loop "
    "comparison saved only ~14%",
    "modeled",
    "injecting the plan (arm B) saves83.3%", pre=120, post=340,
    note="Value reported is the per-occurrence 6.0x reduction for arm B. This is a MODELED "
         "per-occurrence reduction, not a break-even reuse count and not a billed figure.")

add(1, "ActivityFrames", None, "staleness_forgetting_maintenance_cost", None, None, None, None, None,
    "it is exposed to interface drift that a live run must confirm", pre=210, post=300,
    absence="NO_QUANTIFIED_STALENESS_FORGETTING_OR_MAINTENANCE_COST. The only staleness-adjacent "
            "statements are (a) unquantified 'interface drift that a live run must confirm', (b) "
            "'stale attribution' which is a REPAIRED INPUT-RECORDER DEFECT (re-attributed to the "
            "temporally nearest snapshot), not a cost of retained state, and (c) a capture operating "
            "cost (9.5 GB corpus, ~0.19 GB per active day, OCR on 96% of frames, a11y tree present on "
            "81.5% of frames so 18.5% would fall back to coordinates). No forgetting function, no "
            "refresh/invalidation cost, no measured cost of a stale replay is reported. Absence "
            "established over 69,607 characters of retrieved full text.")

add(1, "ActivityFrames", None, "real_cost_advantage_persistence", "no_measured_real_cost_advantage",
    None,
    "the paper reserves live billing; the on-hit zero-token case is live-confirmed once, the "
    "dollar savings are not",
    "the single live confirmation is one two-step routine, plan seeded from live accessibility "
    "names, guard-miss deopt path not exercised",
    "modeled",
    "The full live three-arm billing with real usage JSON remains reserved", pre=330, post=420,
    note="Closest available statement of a realized advantage is measured: local replay executed "
         "with zero model tokens at execution on a guard-matched two-step routine, versus ~10.5k "
         "tokens per step for the accessibility snapshots an in-loop agent would read. A separate "
         "live comparison keeping the model in the loop saved only ~14%.")

add(1, "ActivityFrames", None, "denominator", "corpus_and_ladder_denominators_declared", 
    "Rinject over the 20 most frequent action routines out of 614 recurring action routines / 5,508 "
    "routine instances; Rinfo additionally over 261 recurring URL routines / 1,303 instances; "
    "R numerator priced per step at a typical 1512x982 capture (~2,500 tokens/step); compile cost "
    "median 0.5 ms at zero token cost; guard coverage median 0.415",
    "tokens under cl100k_base for both numerator components and denominator; dollars only in the "
    "modeled three-arm table",
    "corpus = one user, 51 active days, 128,756 frames, 232,898 input events (numerator/replay "
    "freeze); Section 6 systems numbers use an earlier freeze (61 days, 46 active, 109,735 frames)",
    "measured",
    "Rinject is computed on the20most frequent action routines", pre=90, post=300)

add(1, "ActivityFrames", None, "accounting_convention", "tokens_cl100k_base_plus_modeled_dollars", 
    None,
    "token counts via tiktoken cl100k_base for C_replay; C_agent priced from the Anthropic "
    "w*h/750 image-token rule plus fixed 350-token context read and 180-token reasoning write, "
    "WITHOUT EXECUTING AN AGENT; dollars at Sonnet-class list rates ($3/$15 per Mtok, output "
    "fraction 0.07) and explicitly not billed",
    "screen-configuration band 259-425x (1280x800 conservative to 1728x1117 retina)",
    "modeled",
    "it is an", pre=280, post=420,
    note="The paper states the numerator is an upper bound assuming a screenshot baseline with no "
         "cross-step prompt caching and no accessibility-tree grounding.")

add(1, "ActivityFrames", None, "stated_uncertainty", "IQRs_reported_no_credible_interval_on_R_itself",
    None,
    "interquartile range over the 20 compiled plans; min-max over all routines; a temporal-holdout "
    "gap for h; an explicit modeler-disagreement band from re-pricing the numerator at three screen "
    "configurations",
    "no confidence interval, standard error or significance test is attached to R or to h; the only "
    "Wilson 95% CI in the paper (91.7-99.7%) belongs to the Section 6.2 QA accuracy, not to R or h",
    "measured",
    "Across screen resolutions 259", pre=200, post=300)

add(1, "ActivityFrames", None, "modeled_vs_measured", "modeled",
    None,
    "the paper's own three disciplines: no rung of R is multiplied by the 86x context compression; R "
    "is never combined with prompt-cache or KV-cache discounts; both the numerator and the three-arm "
    "dollars are modeled and reported as ceilings",
    None,
    "modeled",
    "the numerator and the three-arm dollars are", pre=260, post=420,
    note="Verbatim source of the labeling: 'The numerator is modeled' and 'The denominator is "
         "measured, and we report it as a ladder'.")

add(1, "ActivityFrames", None, "all_fleet_ceiling_h_times_1_minus_1_over_Rinfo", 0.077,
    "all action steps across the fleet, not just the recurring subset",
    "h * (1 - 1/Rinfo) with Rinfo = 343; reported as a ceiling, ~9.0% in-sample and ~7.7% "
    "out-of-sample",
    "carries the 7.7% out-of-sample h; the paper instructs that this is the recurrence the cost "
    "accounting should carry",
    "modeled",
    "all-fleet ceilingh (1", pre=200, post=380)

add(1, "ActivityFrames", None, "published_limitation_count", 5,
    "five limitations stated in Section 8.4 bounding the overhead measurements",
    "limitation list, not a cost accounting quantity",
    "single user; modeled-not-billed numerator and dollars; one two-step live confirmation with "
    "three named bounds; capture is not free; replay coverage bounded by guard coverage",
    "measured",
    "Five limitations bound the results of this half of the paper", pre=0, post=420)

# ===== Part 2 : performance envelope =====
add(2, "WebVoyager", "WebVoyager (own benchmark, 15 sites)", "success_rate", 0.591,
    "643 tasks total, 40-45 tasks per website; judged by GPT-4V over all screenshots and all "
    "actions; a 300-task subset carries three independent human annotators",
    "Task Success Rate, following the WebArena convention: successful completion of tasks "
    "without considering whether the steps are optimal",
    "per-site values reported with +/- (e.g. 56.9% +/- 2.8%)",
    "measured",
    "achieves a 59.1% task success rate on our benchmark", pre=60, post=300, cid=WV,
    extra={"system_comparison_in_artifact": "GPT-4 (All Tools) 30.8%; WebVoyager text-only 40.1%; "
                                           "SeeAct online test set 30% vs best SeeAct agent 26%"})

add(2, "WebVoyager", "SeeAct online test set", "success_rate", 0.30,
    "the 50 tasks used in SeeAct agent's online evaluation",
    "same Task Success Rate convention as above", None, "measured",
    "has a success rate of 30% on the SeeAct online test set", pre=90, post=260,
    cid=WV)

add(2, "WebVoyager", "WebVoyager (own benchmark, 15 sites)", "denominator",
    "643 tasks",
    "643 tasks total, 40-45 per website; judged by GPT-4V over all screenshots and all actions; "
    "a 300-task subset carries three independent human annotators",
    "count of benchmark task instances, one success counted per instance",
    "a 300-task human-agreement subset with three annotators each",
    "measured",
    "resulting in a total of 643 tasks", pre=90, post=200, cid=WV)

add(2, "WebVoyager", "WebVoyager (own benchmark, 15 sites)", "evaluation_convention",
    "Task_Success_Rate_following_WebArena", None,
    "Following WebArena (Zhou et al., 2023), the primary evaluation metric is the Task Success Rate, "
    "measuring successful completion of tasks without considering whether the steps are optimal; "
    "an LLM judge is shown the whole web trajectory (all screenshots and all actions) and returns a "
    "binary judgment of whether the agent successfully completed the task",
    "human-label agreement and Cohen's kappa are reported against a 300-task subset",
    "measured",
    "the primary evaluation metric we adopt is the Task Success Rate", pre=60, post=260, cid=WV)

add(2, "WebVoyager", "WebVoyager (own benchmark, 15 sites)", "benchmark_split",
    "643_tasks_over_15_websites_40_to_45_tasks_each", None,
    "single held-out benchmark built by the authors; no train/dev/test split is frozen or reported",
    "per-site task counts range 40 to 45",
    "measured",
    "Each website contains 40 to 45 tasks", pre=60, post=200, cid=WV,
    extra={"note": "The paper also reports a 50-task SeeAct online test set and a GAIA subset "
                   "(50 tasks) as separate evaluations; the 643-task WebVoyager benchmark is its "
                   "primary split."})

add(2, "WebArena", "WebArena", "success_rate", 0.1441,
    "812 long-horizon web-based tasks (812 test examples)",
    "end-to-end task success rate judged by functional correctness of task completions; "
    "human performance 78.24% on the same benchmark",
    None, "measured",
    "an end-to-end task success rate of 14.41", pre=170, post=280, cid=WA)

add(2, "Mind2Web", "Mind2Web TestCross-Task", "success_rate", 0.071,
    "macro average across tasks; MINDACT with Flan-T5L; Step Success Rate 50.3% on the same split",
    "each step evaluated independently WITH THE GROUND TRUTH ACTION HISTORY PROVIDED; a step counts "
    "as successful only if both the selected element and the predicted operation are correct; whole-task "
    "Success Rate is the conjunction over steps",
    "GPT-4 numbers use only 50 tasks per setting due to limited budget", "measured",
    "w/ Flan-T5L 53.4 75.7 50.3 7.1 39.2 67 .1 35 .3 1 .1 39 .7 67 .2 37 .3 2 .7", pre=60, post=20, cid=M2W,
    extra={"element_accuracy": 0.534, "operation_f1": 0.757, "step_success_rate": 0.503,
           "note": "quoted run of the Table 2 numeric row, column order "
                   "Cross-Task Ele.Acc / Op.F1 / Step SR / SR"})

add(2, "Mind2Web", "Mind2Web TestCross-Website", "success_rate", 0.011,
    "177 tasks from 10 websites (one per remaining top-level domain); MINDACT with Flan-T5L; "
    "Step Success Rate 35.3%",
    "same oracle-action-history convention as TestCross-Task", None, "measured",
    "w/ Flan-T5L 53.4 75.7 50.3 7.1 39.2 67 .1 35 .3 1 .1 39 .7 67 .2 37 .3 2 .7", pre=60, post=20, cid=M2W,
    extra={"step_success_rate": 0.353})

add(2, "Mind2Web", "Mind2Web TestCross-Domain", "success_rate", 0.027,
    "912 tasks from 73 websites, holding out two top-level domains (Information and Service); "
    "MINDACT with Flan-T5L; Step Success Rate 37.3%",
    "same oracle-action-history convention as TestCross-Task", None, "measured",
    "w/ Flan-T5L 53.4 75.7 50.3 7.1 39.2 67 .1 35 .3 1 .1 39 .7 67 .2 37 .3 2 .7", pre=60, post=20, cid=M2W,
    extra={"step_success_rate": 0.373})

add(2, "WebShop", "WebShop test split", "success_rate", 0.291,
    "500 test instances of 12,087 total instructions (train/dev/test 10,587/1,000/500); "
    "human expert 59%, rule-based heuristic 9.6%",
    "two metrics reported together: Task Score = 100 x average reward, and Success Rate = the "
    "portion of instructions where the final reward r = 1",
    None, "measured",
    "Our best model achieves a task success rate of 29", pre=60, post=300, cid=WS)

add(2, "AgentBench-web", "AgentBench-web (Cross Domain test set)", "success_rate", None,
    "912 tasks from 73 websites for the Cross Domain test set; 8 environments in the suite; "
    "per-environment #Test counts in Table 2",
    "Success Rate (SR) as the per-environment evaluation metric, with an estimated #Avg. Turn",
    None, "measured",
    "We adopt the success rate (SR) as the evaluation metric", pre=0, post=340, cid=AB,
    absence="NO_SINGLE_HEADLINE_SUCCESS_RATE_EXTRACTED_FOR_THE_WEB_SUBSET. The retrieved full text "
            "reports SR per environment in a table whose numeric cells are not linearised by the PDF "
            "text layer, and the artifact's own '912 tasks from 73 websites' cross-domain figure is "
            "attributed to a cross-domain test set the paper reuses from another benchmark. Reporting "
            "absence rather than a number, per spec.json ABSENCE_AS_ABSENCE.",
    determination="NOT_REPORTED_IN_RETRIEVED_TEXT")

# ===== Part 3 : retrieval vs write =====
add(3, "ActivityFrames", "8-day downstream QA (own)", "write_pipeline_type",
    "three_representations_compared", None,
    "raw rows serialized as search-API JSON (126,812 tokens) vs compiled schema-v1 document "
    "(222 frames, 34,815 tokens) vs compact context block (1,469 tokens) vs an LLM summary of the "
    "same capture", None, "measured",
    "we compare three representations an agent could receive", pre=110, post=430, cid=AF)

add(3, "ActivityFrames", "8-day downstream QA (own)", "downstream_accuracy", 0.984,
    "8 days, 64 ground-truth questions, graded against an independent SQL oracle, run at two "
    "model tiers",
    "answers questions about the user's day; the compiled block is graded against the same oracle "
    "as the other representations",
    "Wilson 95% CI 91.7-99.7%", "measured",
    "answers questions about the day at98.4%accuracy", pre=110, post=320, cid=AF,
    extra={"write_pipeline_comparator_llm_summary_accuracy": "66-80%"})

add(3, "ActivityFrames", "8-day downstream QA (own)", "retrieval_quality_metric", None, None,
    None, None, None, None, absence=
    "NOT_REPORTED_AND_NOT_VARIED. The artifact varies the WRITE representation while holding the "
    "RETRIEVED CONTEXT CONSTANT (the whole compiled day is placed in the system prompt, 'small "
    "enough to include in every system prompt'). It therefore reports no recall, precision, nDCG, "
    "hit rate or MRR over relevant context, and cannot separate retrieval quality from write "
    "sophistication. The only retrieval-adjacent quantity is the temporal-holdout routine hit rate "
    "(7.7%), which measures recurrence, not retrieval quality. Absence established over 69,607 "
    "characters of retrieved full text.")

add(3, "ActivityFrames", "8-day downstream QA (own)", "ablation_result",
    "write_pipeline_only_retrieval_held_constant", None,
    "single-factor contrast of representation type at fixed context", None, "measured",
    "reading that block answers questions about the day at98.4", pre=170, post=380, cid=AF,
    extra={"note": "The contrast reported is 98.4% (deterministic compiled block) vs 66-80% (LLM "
                   "summary of the same capture), and a mid-tier model reading the block matches a "
                   "frontier one. Because retrieval is constant, this is evidence about write "
                   "sophistication only and is not a retrieval-vs-write variance decomposition."})


def main() -> int:
    unresolved = [r for r in D if r["evidence_quote"] is None and r["evidence_for_absence"] is None]
    bad = [r for r in D if r["determination"] == "EXTRACTED" and r["evidence_quote"] is None]
    out = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-36306525220",
        "stage": "field_determinations",
        "generated_at": now(),
        "quote_construction": "every evidence_quote is a verbatim whitespace-normalized slice of the "
                              "retrieved text located by its anchor; anchors are listed per row",
        "rows": D,
        "integrity": {
            "n_rows": len(D),
            "n_extracted": sum(1 for r in D if r["determination"] == "EXTRACTED"),
            "n_not_reported": sum(1 for r in D if r["determination"] == "NOT_REPORTED_IN_RETRIEVED_TEXT"),
            "rows_without_quote_and_without_absence_evidence": len(unresolved),
            "rows_claiming_extracted_without_quote": len(bad),
        },
    }
    p = os.path.join(RAW, "field_determinations.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    for r in D:
        flag = "OK " if (r["evidence_quote"] or r["evidence_for_absence"]) else "BAD"
        print(f"{flag} p{r['part']} {r['system']:14s} {r['field']:46s} {r['determination']}")
    print("integrity:", json.dumps(out["integrity"]))
    print("wrote", p)
    return 1 if (unresolved or bad) else 0


if __name__ == "__main__":
    sys.exit(main())
