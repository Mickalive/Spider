# EXP-INTEL-35280397316 — Literature Synthesis Report

## Executive Summary

**Outcome: SURVIVES_CURRENT_TEST** — Principled methods for resolving recipe choice ambiguity exist in established measurement frameworks (code coverage, information retrieval, web analytics), and these methods directly inform SPIDER's density metric recipe choice problem.

The recipe choice instability discovered in the parent experiment (canonical per-iteration C2 FALSE vs per-task weighted C2 TRUE) is a known phenomenon in measurement theory with established resolution approaches. The density metric problem is NOT fundamentally different from known measurement ambiguity problems.

## 1. Question and Hypothesis

**Question**: How do established measurement frameworks handle recipe choice ambiguity when aggregating metrics across multiple definitions or dimensions, and can principled resolution methods inform SPIDER's density metric recipe choice problem?

**Hypothesis**: There exist principled methods for resolving recipe choice ambiguity in multi-definition metrics, and these methods can inform SPIDER's density metric recipe choice problem.

## 2. Evidence from Established Frameworks

### 2.1 Code Coverage Metrics

Code coverage frameworks support multiple coverage definitions with configurable aggregation recipes:

| Coverage Type | What It Measures | Aggregation Recipe |
|---|---|---|
| Line coverage | Executed lines / total lines | Set union across test suites |
| Branch coverage | Covered branches / total branches | Set union with partial coverage tracking |
| Path coverage | Executed paths / total paths | Exponential; bounded variants (basis path, n-length sub-path) |
| Condition coverage | Individual condition outcomes | Per-condition, then aggregated |

**Recipe choice ambiguity**: The choice of which coverage metric (line vs branch vs path) AND how to aggregate across test suites (set union, weighted merge, per-module thresholds) is a well-documented recipe choice problem. Datadog merges coverage reports via set union (a line is "covered" if ANY report marks it covered). Coverage.py uses set union for parallel execution. Different aggregation recipes yield different coverage percentages.

**Key insight**: Different coverage metrics answer different questions. Line coverage asks "did we execute this code?" Branch coverage asks "did we exercise both sides of decisions?" Path coverage asks "did we follow all execution paths?" The recipe choice is tied to the question being asked.

**Sources**: Datadog Code Coverage Calculation docs, coverage.py documentation, PHPUnit 13.0 Code Coverage manual, BullseyeCoverage metrics documentation.

### 2.2 Information Retrieval (Strongest Parallel)

IR has the most direct parallel to SPIDER's density metric recipe choice:

**Micro-averaging**: Pool all per-document decisions across classes, then compute the metric on the pooled counts.
- Micro-precision = ΣTP / (ΣTP + ΣFP)
- Gives equal weight to each per-document classification decision
- Dominated by large classes
- Equivalent to accuracy in single-label multiclass

**Macro-averaging**: Compute metric per class, then take unweighted mean.
- Macro-F1 = (1/C) Σ F1_c
- Gives equal weight to each class regardless of size
- Sensitive to rare classes
- Preferred when minority classes matter equally

**Weighted averaging**: Per-class metrics averaged with weights proportional to class support.
- Weighted-F1 = Σ (n_k/N) × F1_k
- Between micro and macro in spirit
- Reflects real-world traffic distribution

**Critical finding**: Two distinct formulas for "macro F1" exist in the literature (ar5iv:1911.03347):
1. Averaged F1: F1 = (1/n) Σ F1_i (arithmetic mean of per-class F1)
2. F1 of averages: F1 = H(P̄, R̄) (harmonic mean of average precision and recall)

These diverge by up to 0.5 in extreme cases and can lead to different classifier rankings. This is exactly the kind of recipe choice ambiguity SPIDER faces.

**Source**: Stanford NLP textbook (Manning et al.), scikit-learn documentation, Sokolova & Lapalme (2019), "A Closer Look at Classification Evaluation Metrics" (TACL 2024).

### 2.3 Web Analytics

Web analytics has recipe choice ambiguity in engagement metrics:

| Metric | Definition A (UA) | Definition B (GA4) |
|---|---|---|
| Bounce rate | Single-page sessions / all sessions | Non-engaged sessions / all sessions |
| Session duration | Wall-clock time start-to-last-hit | Foreground engagement time |
| Time on page | Gap between consecutive pageviews | Direct measurement via engagement events |

**Recipe choice ambiguity**: GA4 redefined bounce rate from "single-page sessions" to "non-engaged sessions," changing the recipe entirely. A user reading a 3000-word article for 6 minutes and leaving counts as a bounce in UA but NOT in GA4. The choice of which definition to use changes the conclusion.

**Source**: Google Analytics documentation, Analytics Edge, PMC9140287 (comparison study).

## 3. Mapping to SPIDER's Density Metric Problem

SPIDER's density metric recipe choice maps directly to the IR micro/macro/weighted aggregation distinction:

| SPIDER Recipe | IR Analog | What It Answers |
|---|---|---|
| Canonical per-iteration (p=0.5) | Micro-averaging | Do definitions disagree more than random across ALL iterations? (uniform weight per iteration) |
| Per-task weighted | Macro-averaging | Do definitions disagree more than random within each TASK on average? (equal weight per task) |

The parent experiment found:
- Canonical per-iteration: C2 FALSE (definitions disagree MORE than random)
- Per-task weighted: C2 TRUE (definitions agree MORE than random)

This is exactly the kind of recipe-dependent reversal documented in IR: "microaveraged results are really a measure of effectiveness on the large classes" while macroaveraged results "give equal weight to each class." The recipes answer different scientific questions.

## 4. Principled Resolution Methods

The resolution across all three fields is consistent:

1. **Recipe choice is a design decision, not an implementation detail.** Each recipe answers a different scientific question.

2. **State which recipe you use and justify it by the question you are answering.** The canonical per-iteration recipe is principled for C-MEAS-VALID because it tests the right question (uniform application across definitions, controls for role preferences).

3. **Report sensitivity to recipe choice when possible.** If both recipes survive on full-DOM data, recipe ambiguity becomes the central scientific issue requiring principled resolution (possibly a third recipe or meta-analytic approach).

4. **Prevalence calibration** (from macro F1 literature): When class/definition distributions are imbalanced, calibrate by making all classes equally prevalent before computing metrics. This could inform SPIDER's approach to definition-weighting.

## 5. Decision Rule Evaluation

**SURVIVES_CURRENT_TEST** requires ALL of:

1. ✅ **PC1 passes**: 3 well-documented cases of recipe choice ambiguity found (code coverage, IR, web analytics)
2. ✅ **PC2 passes**: 3 principled resolution methods identified (recipe-as-question-answer binding, sensitivity reporting, micro/macro/weighted framework)
3. ✅ **F1 not triggered**: Principled methods exist in at least 1 established field (all 3 fields)
4. ✅ **F2 not triggered**: Density metric problem is NOT fundamentally different from known problems (maps directly to IR micro/macro/weighted)

## 6. Product Consequence

**SURVIVES** informs spec amendment for MIXED outcomes and provides principled resolution methods for the recipe choice problem. Product lane gains a theoretically grounded approach to recipe selection, enabling advancement beyond the current blocking ambiguity.

The canonical recipe assumption (per-iteration p=0.5) is validated as the principled choice for C-MEAS-VALID because it answers the right question (uniform application across definitions). However, sensitivity to recipe choice should be reported when possible.

## 7. Limitations

- Literature search used web search, not a systematic review protocol
- Claim ceiling bounded to published literature only (no new empirical measurement)
- The applicability mapping (SPIDER → IR) is an interpretation, not an established result
- Full-DOM enumeration results remain unknown and may change the recipe choice landscape
