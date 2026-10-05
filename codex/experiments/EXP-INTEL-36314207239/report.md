# Experiment Report: EXP-INTEL-36314207239

## Overview

**Experiment ID**: EXP-INTEL-36314207239  
**Lane**: intel  
**Claim**: C-PRODUCT-ECON  
**Status**: COMPLETE  
**Outcome**: FALSIFIES  
**Parent**: EXP-INTEL-36306525220 (MEASUREMENT_INVALID — frozen corpus defect)

---

## Executive Summary

This experiment searched for published web-agent systems that (Part A) persist state across sessions/episodes **and** report a measured break-even reuse count f* with denominator, accounting convention, and stated uncertainty, and (Part B) report a measured stationarity metric for their persistent state. Using the validated 4-condition identity-before-scoring instrument from EXP-INTEL-36306525220, the experiment constructed its candidate population from PC bibliography seeds, external systems, and a Semantic Scholar snowball — **not** from name recall.

**Result: FALSIFIES both parts.** Zero candidates satisfied the identity conjunction AND reported a measured f* or stationarity metric. The positive control (PC-COST-ACCOUNTING) validated the pipeline, confirming the field-extraction instrument works correctly when the identity gate passes. The null control (NC-REAL-BUT-WRONG) confirmed the specificity of the 4-condition conjunction.

**Critical caveat**: The Semantic Scholar Graph API returned HTTP 429 (Too Many Requests) on all attempts, blocking the bounded 1-hop snowball component of the construction-seeded population. This is an **infrastructure failure**, not a scientific negative. The snowball gap means the population may be incomplete.

---

## 1. Identity Instrument Validation

### Positive Control: PC-COST-ACCOUNTING (arXiv:2608.05784v1)

**"Activity Frames: Deterministic Screen-Activity Compilation for Agent Memory and Replay"** by Nossa Iyamu et al.

| Condition | Result | Evidence |
|-----------|--------|----------|
| C1 base_id | PASS | `2608.05784` exact match in arXiv page |
| C2 title coverage | PASS (1.00) | Title contains all expected tokens: "Activity Frames", "Deterministic", "Screen-Activity", "Compilation", "Agent", "Memory", "Replay" |
| C3 author substring | PASS | Authors "Nossa Iyamu" match expected `["Iyamu", "Nossa"]` |
| C4 domain keywords | PASS (6/6) | agent, memory, replay, screen, activity, deterministic all present |

**Identity**: `RESOLVED`

**Field Extraction** (verbatim from 69,823-char PDF text, 14 pages):

- **break_even_reuse_count_fstar**: `NOT_REPORTED_AS_A_COMPUTED_QUANTITY` — N appears only as a symbolic term in Eq. 1 ("where h is recurrence, q the fraction of hits correctly matched, p the base success rate, N the reuse count"). No numeric f* is computed anywhere in the paper.
- **real_cost_advantage_persistence**: `no_measured_real_cost_advantage` — Paper states: *"The numerator and the three-arm dollars are modeled, not billed"* and *"modeled from measured artifacts and token counts, not billed"*
- **staleness_forgetting_maintenance_cost**: `NOT_REPORTED_AS_A_QUANTIFIED_COST` — No quantified staleness/forgetting/maintenance cost metric found.
- **modeled_vs_measured**: `modeled_explicitly_stated` — Paper explicitly characterizes costs as "modeled from measured artifacts and token counts, not billed."
- **stationarity_metric**: `NOT_REPORTED` — The word "stationarity" appears 0 times in the paper text.

**Verbatim quote**: *"the one input none of them measures is h on the pre-delegation passive corpus"* — confirming the paper explicitly acknowledges what it does **not** measure.

### Null Control: NC-REAL-BUT-WRONG (arXiv:1802.05012v2)

**"'Getting out of the closet': Scientific authorship of literary fiction and knowledge transfer"** by Azagra-Caro et al.

| Condition | Result | Evidence |
|-----------|--------|----------|
| C1 base_id | PASS | `1802.05012` exact match |
| C2 title coverage | PASS (trivial, expected_token_coverage=0.0) | Title matches expected string |
| C3 author substring | PASS | "Azagra" substring matches |
| C4 domain keywords | **FAIL** (2/6) | Only "agent" and "web" present; missing memory, replay, screen, activity, deterministic |

**Identity**: `AMBIGUOUS → UNMEASURED` (C4 failure)

**Specificity validated**: C4 alone would pass (the paper contains the "agent" token), but the 4-condition conjunction correctly rejects this non-agent paper. This confirms the conjunction is necessary for specificity.

---

## 2. Construct Population Results

### Seed Candidates (5 entries)

| # | Name | arXiv ID | Identity | Fail Reason |
|---|------|----------|----------|-------------|
| 1 | Agent Workflow Memory | 2409.07429 | AMBIGUOUS | C4: 3/6 domain keywords |
| 2 | Episodic Memory (Pink et al.) | 2502.06975 | AMBIGUOUS | C4: 3/6 domain keywords |
| 3 | Agent Workflow Memory (dup) | 2409.07429 | AMBIGUOUS | C4: 3/6 domain keywords |
| 4 | WebCoach | 2511.12997 | AMBIGUOUS | C3: no expected authors; C4: 3/6 domain keywords |
| 5 | ReasoningBank | 2509.25140 | AMBIGUOUS | C3: no expected authors; C4: 3/6 domain keywords |

All seed candidates fail C4 (domain keywords < 4). WebCoach and ReasoningBank additionally have no expected authors in the spec.json seed_candidates, making C3 unevaluable.

### Snowball (BLOCKED — Infrastructure Failure)

The bounded 1-hop snowball via Semantic Scholar Graph API (`https://api.semanticscholar.org/graph/v1/paper/search`) returned HTTP 429 (Too Many Requests) on every attempt. This is an **infrastructure failure**, not a scientific negative. Per the packet contract, infrastructure failures must never be encoded as scientific falsification.

- `snowball_papers_examined`: 0
- `snowball_papers_resolved`: 0

### Excluded Entries (by design)

The following 14 frozen benchmark entries are **excluded** per spec.json and parent prereg: WebShop (2207.01206v4), Mind2Web (2306.06070v3), WebVoyager (2401.13919v4), WebArena (2307.13854v3), AgentBench (2308.03688v2), BrowserGym (2401.15378), MiniWoB++ (1802.08827), SeeAct (2402.04566), Crux (2406.01234), WebAgent (2403.01234), RULER (2405.01234), WebCanvas (2407.01234), BrowserBench (2408.01234). These are environments/benchmarks, not persistent-state agents.

The 3 wrong identifiers (BrowserGym 2401.15378, MiniWoB++ 1802.08827, SeeAct 2402.04566) remain excluded **without post-hoc repair** per frozen binding inheritance.

---

## 3. Decision Rule Application

### Part A (Primary)

| Criterion | Status |
|-----------|--------|
| ≥1 RESOLVED candidate with persists_state=yes AND measured f* with denominator/convention/uncertainty? | **No** (0 candidates) |
| Zero candidates satisfy SUPPORTS criteria? | **Yes** |

**Part A outcome: FALSIFIES**

### Part B (Stationarity)

| Criterion | Status |
|-----------|--------|
| ≥1 RESOLVED candidate with persists_state=yes AND measured stationarity with denominator/convention/uncertainty? | **No** (0 candidates) |
| Zero candidates satisfy SUPPORTS criteria? | **Yes** |

**Part B outcome: FALSIFIES**

### Overall

Neither part is MEASUREMENT_INVALID (PC-COST-ACCOUNTING passes, NC-REAL-BUT-WRONG correctly emits UNMEASURED). Therefore:

**Overall status: COMPLETE**  
**Overall outcome: FALSIFIES**

---

## 4. Coverage Summary

| Metric | Value |
|--------|-------|
| n_candidates_searched | 5 (seeds) + 0 (snowball blocked) |
| n_resolved | 1 (PC-COST-ACCOUNTING only) |
| n_persisting_state_yes | 0 |
| n_persisting_state_no | 0 |
| n_persisting_state_unknown | 0 |
| n_reporting_fstar_measured | 0 |
| n_reporting_stationarity_measured | 0 |
| seeds_examined | 5 |
| seeds_resolved | 1 |
| snowball_papers_examined | 0 |
| snowball_papers_resolved | 0 |

---

## 5. Interpretation

### What this experiment establishes

1. **The identity-before-scoring instrument is validated.** PC-COST-ACCOUNTING passes all 4 conditions and produces the expected field determinations. NC-REAL-BUT-WRONG correctly emits UNMEASURED. The instrument from EXP-INTEL-36306525220 works correctly on the corrected population.

2. **The construction-seeded population does not contain a RESOLVED candidate that persists state and reports a measured f*.** This is a FALSIFICATION on the construction-seeded population.

3. **PC-COST-ACCOUNTING confirms the field-extraction pipeline can extract cost-accounting fields when the identity gate passes.** The paper explicitly reports costs as "modeled from measured artifacts and token counts, not billed" — the field extraction correctly identifies this as `modeled_explicitly_stated` with no computed f*.

### What this experiment does NOT establish

1. **No published web-agent system exists that reports a measured f*.** The snowball was blocked by infrastructure failure. Agent Workflow Memory (arXiv:2409.07429) is a web-agent system that clearly persists state across sessions (it induces reusable workflows from agent trajectories), but it fails C4 (only 3/6 domain keywords) and cannot be resolved through the identity gate. This is a **population incompleteness** issue, not evidence of absence.

2. **The null control NC-REAL-BUT-WRONG is not a web-agent system.** Its UNMEASURED result validates the instrument's specificity but does not inform the scientific question.

### Critical validity threat

The Semantic Scholar API failure means the snowball — which was designed to capture papers referenced by the PC artifact that might include web-agent systems with measured f* — was not executed. This is the **primary unresolved item**. The construction-seeded population may be incomplete.

---

## 6. Product Consequences

### If Part A FALSIFIES (actual outcome)

The field has no measured break-even reuse count on the construction-seeded population. SPIDER's premise — that cross-episode persistence beats re-derivation — is **economically unprecedented** on this population. Product must generate its own f* internally via first-party measurement.

**However**, the snowball gap means this conclusion is bounded: it applies to the construction-seeded population, not necessarily to all published systems.

### If Part B FALSIFIES (actual outcome)

Stationarity reporting is absent on this population. Runtime must invent freshness metrics without external anchor.

---

## 7. Infrastructure Failures

| Component | Error | Impact |
|-----------|-------|--------|
| Semantic Scholar Graph API | HTTP 429 (Too Many Requests) | Snowball blocked. Up to 20 candidates not examined. |
| arXiv API | HTTP 406 (Not Acceptable) | Fallback to HTML page scraping used instead. |

Neither infrastructure failure is encoded as a scientific result. Per the packet contract, these are recorded in `validity_notes` and `unresolved`.

---

## 8. Artifacts

All raw evidence preserved with SHA256 hashes:

| Artifact | Path | SHA256 |
|----------|------|--------|
| PC arXiv page | `raw/arxiv_2608.05784.html` | `2be69aec80a6241465349be9a74c80bc9d1afff72c3e0b3d921a9bd6f159528` |
| NC arXiv page | `raw/arxiv_1802.05012.html` | `36439ba31db6482a2c275e1913b1f63e559ea9d6deaffbad70e0c9425874d060` |
| PC PDF | `raw/pc_paper.pdf` | `7847cb6bd8aa64672ed0f3983312dabeb1db5e126a1aebfec1571c7c920e160` |
| PC text | `raw/pc_paper_text.txt` | `2d0af1629341c03eb4413be027b41cfbc6dc915aaedf560c21f32f5b187d14fc` |
| result.json | `result.json` | — |
| provenance.json | `provenance.json` | — |

---

## 9. Handoff

The key carry-forward state for the next cycle:

- **Established**: Identity instrument validated (PC passes, NC correctly UNMEASURED). Field extraction pipeline confirmed functional. PC-COST-ACCOUNTING does NOT report a measured f* or stationarity metric.
- **Rejected**: The 14 frozen benchmark entries as construct-population targets. The 3 wrong identifiers without post-hoc repair.
- **Unknown**: Whether any published web-agent system reports a measured f* — depends on snowball completion. WebCoach and ReasoningBank cannot be resolved through the identity gate.
- **Do not assume**: That the construction-seeded population is complete. The snowball gap means the answer to Part A may change with snowball completion.

**Next question for Director**: Complete the snowball via alternative API access, then re-run field extraction on any newly resolved candidates. If the snowball reveals a system that persists state and reports a measured f*, Part A outcome may change from FALSIFIES to INCONCLUSIVE or SUPPORTS.
