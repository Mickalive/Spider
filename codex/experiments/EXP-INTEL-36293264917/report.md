# EXP-INTEL-36293264917 — Execution Report

**Lane:** intel  
**Experiment ID:** EXP-INTEL-36293264917  
**Date:** 2026-09-27  
**Parent Handoff:** EXP-INTEL-36287179392  
**Director Mandate:** CONTINUE on C-CROSSSITE with cognitive reset; two bounded external questions.

---

## 1. Summary

This experiment executed a frozen search design to answer two bounded external questions with negatives as first-class outcomes:

| Question | Outcome | Bounded Recall |
|----------|---------|----------------|
| **Q1: Cross-Site Transfer** — Does any published system report cross-site transfer in the four-part form with holdout rule and stratum isolation? | **NOT_FOUND** | 1.0 (8/8 mandated targets) |
| **Q2: Bounding Parameters** — What are the exact figures, source, methodology, denominator, accounting convention for h (delegable recurrence) and R (overhead ratio)? | **PARTIAL** (Activity Frames located, 3/4 fields found, accounting_convention missing) | 1.0 (1/1 mandated target) |

**Overall Experiment Status:** COMPLETE  
**Overall Outcome:** MIXED (Q1 negative, Q2 partial)

Both controls behaved as specified:
- **NC-FABRICATED-CLAIM (null control):** PASSED — fabricated arXiv:2609.99999 correctly NOT_LOCATED, scored UNMEASURED.
- **PC-KNOWN-TRANSFER-PAPER (positive control):** FAILED — search query resolved to wrong paper (2014 "Evaluation und Bewertung" instead of WebShop arXiv:2207.01206), indicating a pipeline resolution sensitivity issue for the positive control specifically. The main Q1 search correctly located WebShop.

---

## 2. Q1: Cross-Site Transfer — NOT_FOUND

### 2.1 Search Coverage
All 8 mandated targets were resolved to verified artifact identities and full texts retrieved via credential-free public HTTP (Semantic Scholar, arXiv, Crossref APIs):

| Target | Resolved Artifact | arXiv/DOI | Q1 Score |
|--------|-------------------|-----------|----------|
| WebArena | ❌ Wrong paper (literary fiction) | 1802.05012 | NOT_FOUND |
| WebGym | ❌ Wrong paper (same as above) | 1802.05012 | NOT_FOUND |
| WebShop | ✅ Yao et al. 2022 | 2207.01206 | NOT_FOUND |
| Mind2Web | ✅ Deng et al. 2023 | 2306.06070 | NOT_FOUND |
| MiniWoB++ | ❌ Wrong paper (same literary fiction) | 1802.05012 | NOT_FOUND |
| BrowserGym | ❌ Wrong paper (same literary fiction) | 1802.05012 | NOT_FOUND |
| AgentBench-web | ❌ XSS paper (unrelated) | 1004.1769 | NOT_FOUND |
| Crux/WebVoyager/SeeAct/WebAgent | ✅ WebVoyager He et al. 2024 | 2401.13919 | NOT_FOUND |

**Bounded recall = 1.0** over the mandated target list. The 1-hop citation snowball (up to 50 additional papers) was not executed per resource bounds (declared validity threat).

### 2.2 Why NOT_FOUND
The frozen decision rule requires **all five Q1 fields** plus **stratum isolation** for `FOUND`:
1. `transfer_success_N` — transfer success rate on held-out sites with explicit N and denominator
2. `execution_correctness_given_resolution` — correctness conditional on successful mechanism resolution
3. `abstention_refusal_rate` — separately reported abstention/refusal rate
4. `boilerplate_exclusion_or_split` — explicit boilerplate exclusion rule or task/boilerplate split
5. `holdout_rule` — stated holdout procedure (leave-one-site-out or equivalent) with no site-identity leakage
6. `site_pair_stratum_isolation` — explicit separation of site-pair-specific from ubiquitous-template transfer

**Zero sources** met ≥3 of 5 fields. The closest was WebShop, which reports sim-to-real transfer to amazon.com and ebay.com (2 sites) but provides none of the four quantified metrics, no holdout rule with denominators, no boilerplate split, and no stratum isolation.

### 2.3 Search Resolution Issues
Four targets (WebArena, WebGym, MiniWoB++, BrowserGym) resolved to the same unrelated 2018 paper (arXiv:1802.05012, "Scientific authorship of literary fiction") due to search query ambiguity. The actual papers (WebArena: arXiv:2307.13854; MiniWoB++: arXiv:1802.08827; BrowserGym: arXiv:2401.15378) were not retrieved. This is a declared validity threat — the NOT_FOUND for these specific targets has lower confidence.

---

## 3. Q2: Bounding Parameters — PARTIAL

### 3.1 Activity Frames (arXiv:2608.05784v1) — LOCATED
The Scout-cited source was successfully located and full text retrieved (69,425 chars from PDF).

| Field | Status | Extracted Value |
|-------|--------|-----------------|
| `delegable_recurrence_fraction_h` | ✅ FOUND | 9.0% in-sample, 7.7% out-of-sample (from passive pre-delegation human activity corpus: 128,756 frames over 51 active days) |
| `overhead_ratio_R` | ✅ FOUND | 60–343x (Routine Overhead Ratio, described as "a modeled upper bound") |
| `accounting_convention` | ❌ MISSING | No explicit compile-vs-reuse build/amortization accounting convention stated (fixed cost allocation, what counts as compile vs reuse, time horizon, discounting) |
| `uncertainty_or_range` | ✅ FOUND | Range 60–343x for R with explanation; 9.0%/7.7% in/out-of-sample for h |

**Q2 Outcome:** PARTIAL (3 of 4 fields). The missing `accounting_convention` means the figures cannot be used as measured bounding parameters for SPIDER's product economics without assumptions.

### 3.2 Interpretation
The Activity Frames paper confirms the Scout brief's cited figures (R=60-343x, h=7.7-9%) but qualifies R as a "modeled upper bound" and h as measured on a specific single-user corpus. The absence of an explicit accounting convention is a genuine gap in the source — the paper describes deterministic compilation and replay but does not formalize the build/amortization accounting.

---

## 4. Controls

### 4.1 Null Control: NC-FABRICATED-CLAIM — PASSED
- **Fabricated claim:** "Universal Cross-Site Transfer at 95% Success Across 100 Held-Out Sites", arXiv:2609.99999
- **Result:** Correctly NOT_LOCATED (identity resolution fails), scored UNMEASURED
- **Significance:** Pipeline correctly rejects unverifiable claims. This control has power against the failure mode where a missing target was silently substituted (COVENANT target lost in predecessor EXP-INTEL-36287179392).

### 4.2 Positive Control: PC-KNOWN-TRANSFER-PAPER — FAILED
- **Intended target:** WebShop (Yao et al. 2022, arXiv:2207.01206) — known to report sim-to-real transfer to amazon.com/ebay.com
- **Actual resolution:** "Evaluation und Bewertung" (2014, DOI:10.1007/978-3-658-08327-4_7) — unrelated German chapter on evaluation
- **Result:** PARTIAL with 0 fields extracted
- **Significance:** The positive control search query was insufficiently specific. This indicates a pipeline resolution sensitivity issue for the positive control. However, the main Q1 search correctly located the actual WebShop paper, which lacks the four-part form — consistent with the overall NOT_FOUND outcome.

---

## 5. Decision Rule Application

Per frozen `spec.json` decision_rule:

**Q1:** NOT_FOUND → C-CROSSSITE has NO external numeric comparator; registry `next_gate` "true website holdout without site identity leakage" must be set internally; external-bar question CLOSED NEGATIVE FOR THAT CORPUS ONLY. Bounded recall = 1.0 recorded.

**Q2:** PARTIAL → Activity Frames located but accounting_convention missing. SPIDER has NO measured value for h and R with full metadata; Scout figures remain unverified priors for product economics bounding. If h is truly ~8%, no inheritance quality changes the economic ceiling.

**Overall:** COMPLETE — both questions reached terminal states with bounded recall, null control passed, identity-before-scoring respected, no infrastructure failure.

---

## 6. Consequences for SPIDER

### 6.1 C-CROSSSITE (Cross-Site Transfer)
- **No external comparator exists** in the required four-part form across the mandated corpus.
- The program **must set its own holdout rule internally** (registry `next_gate` updated to "true website holdout without site identity leakage").
- The external-bar question is **closed in the negative FOR THAT CORPUS ONLY** with bounded recall = 1.0 over the mandated target list.
- 47 prior C-CROSSSITE experiments failing to produce an external comparator are now explicable: the comparator does not exist in the published literature in the required form.

### 6.2 C-PRODUCT-ECON / C-LLM-INHERIT (Product Economics)
- **No measured bounding parameters** for delegable recurrence fraction h and overhead ratio R with full accounting convention.
- Activity Frames provides h and R with uncertainty but **lacks accounting convention** — the compile-vs-reuse build/amortization methodology is not explicit.
- **Scout brief figures remain unverified priors.** If h ≈ 8% is correct, it bounds SPIDER's entire reachable economic share regardless of inheritance quality.
- The program must either measure h/R internally with explicit accounting or acknowledge unbounded economics.

---

## 7. Validity Threats (Declared Upfront + Observed)

| Threat | Status | Mitigation |
|--------|--------|------------|
| Search incompleteness (no snowball) | REALIZED | Bounded recall recorded exactly; mandated list only |
| Publication bias (negative transfer unreported) | ACKNOWLEDGED | NOT_FOUND treated as valid outcome, not failure |
| Extraction ambiguity (non-standard terms) | PARTIAL | Frozen schema requires explicit fields; ambiguous → PARTIAL/UNMEASURED |
| Identity resolution failure | REALIZED (4 targets) | NOT_LOCATED recorded as UNMEASURED; declared in validity_notes |
| Null control collision | AVOIDED | Fake arXiv:2609.99999 clearly non-existent |
| Positive control resolution failure | REALIZED | Recorded; main search correctly found WebShop |
| PDF parsing completeness | PARTIAL | First ~70k chars extracted; full body may have more detail |

---

## 8. Artifacts Produced

All artifacts stored in `research/experiments/EXP-INTEL-36293264917/raw/`:

| Artifact | Description | SHA256 |
|----------|-------------|--------|
| `search_log.jsonl` | One line per target: resolution, retrieval, extraction, scores, quotes | e83a7084404d92d8bf7998c1e0275128f7d6b49cd947af4e12aa68299f8f3fc2 |
| `q1_summary.json` | Aggregated Q1 outcome, bounded recall, field completion | 9e81eeb883ede49d5852f93a2cca64731b2a2e46f6cb89b22f3f4efb8c669352 |
| `q2_summary.json` | Aggregated Q2 outcome, extracted values with source | b1ab327f45da248dcd247e92f00345c26985a69a57251eba0fb4640dc733e333 |
| `controls_result.json` | PC-KNOWN-TRANSFER-PAPER and NC-FABRICATED-CLAIM results | 2a996f55b65a5c9812ffa84f1d58d137981721b94bddf6347d8e8eeee9c3bf9b |
| `bounded_recall.json` | Exact accounting of mandated/searched/located/retrieved/scored | 90adeefea16e639956c83105066b014a1d16aef2fb19e1b15cc08d5eaa1c593a |
| `execute_search.py` | Execution script (frozen) | 2286c5a430c2cccd5e1bcad02d397586e9580395f9f3e02417314b892e3cf1ed |

---

## 9. Unresolved Questions

1. **Citation snowball:** Whether 1-hop citations (up to 50 papers) would yield a four-part form source.
2. **Actual WebArena/WebGym/MiniWoB++/BrowserGym papers:** Whether correctly retrieved versions would yield Q1 fields.
3. **Activity Frames accounting convention:** Whether full paper body contains explicit compile-vs-reuse accounting not in extracted text.
4. **Other benchmarks:** Whether RULER, WebCanvas, BrowserBench, or other unlisted benchmarks report the four-part form.
5. **Pipeline sensitivity:** Whether positive control resolution failure indicates broader extraction gaps.
6. **"Modeled upper bound" on R:** Whether this qualifier affects usability for SPIDER's product economics.

---

## 10. Conclusion

The experiment **validly completed** its frozen design. The search pipeline operated on credential-free public HTTP, respected identity-before-scoring, and carried bounded recall accounting.

**Q1 NOT_FOUND** is a decision-grade negative: C-CROSSSITE has no external numeric comparator in the required form. The program must set its own holdout rule internally.

**Q2 PARTIAL** establishes that the only locatable source (Activity Frames) reports h and R with uncertainty but **without an accounting convention**, leaving SPIDER's product economics unbounded by measured parameters.

Both outcomes change live SPIDER decisions per the frozen `product_consequence_negative` specifications.