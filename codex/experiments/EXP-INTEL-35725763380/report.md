# EXP-INTEL-35725763380 Report — Intel Dataset Verification for C-LLM-INHERIT

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35725763380
- **Lane**: Intel
- **Claims**: C-LLM-INHERIT (primary), C-CROSSSITE (secondary)
- **Status**: COMPLETE, outcome MIXED
- **Parent Handoff**: EXP-INTEL-35697055679 (verdict: MIXED, audit: PASS) — SUPERSEDED by Director mandate PIVOT
- **Director Mandate**: PIVOT to C-LLM-INHERIT with cognitive reset
- **Date**: 2026-09-22
- **Seed**: 35725763380

## 2. Summary

This experiment quantified whether WebArena-Verified v2 single shopping store provides an identifiable same-mechanism parameterized transfer substrate for C-LLM-INHERIT (within-store template-family hold-out), and whether Mind2Web cross-website splits show measurable same-mechanism overlap at task-sample level.

**Verdict: MIXED.** WebArena within-store axis is PARTIAL PASS (all quantitative thresholds met; AX consistency unverifiable from REUSED parent trees). Mind2Web cross-website axis FAILS (overlap exceeds shuffled null by only 0.0466, below the frozen 0.10 threshold).

## 3. RAW EVIDENCE (Census)

### WebArena-Verified v2

| Metric | Value | 95% CI | Frozen Threshold | Pass? |
|--------|-------|--------|------------------|-------|
| Shopping tasks | 192 | — | — | — |
| Distinct intent_templates | 49 | — | — | — |
| Families with ≥3 tasks | 36 | — | ≥5 | PASS |
| Families with ≥4 tasks | 34 | — | ≥3 | PASS |
| Duplication fraction | 0.9479 | [0.9167, 0.9792] | ≥0.5 | PASS |
| Exact-copy fraction | 0.0781 | [0.0417, 0.1198] | <0.2 | PASS |
| Parameterization (task) | 0.8958 | [0.8490, 0.9375] | ≥0.3 | PASS |
| Parameterization (template) | 0.8367 | — | — | — |
| Site tuples | 187 shopping, 5 shopping+reddit | — | — | — |

- Dataset: `assets/dataset/webarena-verified.json`, ServiceNow/WebArena-Verified commit `ef74e1bfd0d83d4bab1c55b2d1b4c2aeaac8e0d0`, sha256 `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30`
- 812 total tasks, 192 shopping tasks
- All metrics match parent EXP-INTEL-35697055679 exactly (confirming dataset integrity)

### Mind2Web (osunlp/Mind2Web)

| Metric | Value | Frozen Threshold | Pass? |
|--------|-------|------------------|-------|
| Tasks | 1009 | — | — |
| Websites | 73 | spec: 137 | DIVERGENCE |
| Domains | 3 | spec: 31 | DIVERGENCE |
| Train tasks | 595 | — | — |
| Test website tasks | 414 | — | — |
| Test domain tasks | 748 | — | — |
| Overlap (test_website) | 0.7407 | ≥0.15 | PASS |
| Overlap (test_domain) | 0.8205 | — | — |
| Shuffle null mean | 0.6942 | — | — |
| Overlap excess over null | 0.0466 | ≥0.10 | FAIL |
| Shuffle null p95 | 0.8929 | true must exceed p95 | FAIL |
| Parameterization prevalence | 0.6085 | ≥0.15 | PASS |
| PC2 (recurring cluster) | PASS (max=151) | ≥10 tasks across ≥3 websites | PASS |

- Dataset: `osunlp/Mind2Web` (HuggingFace), 1009 tasks, 73 websites, 3 domains
- **Spec divergence**: Dataset has 73 websites/3 domains vs spec.json's stated 137/31
- Shuffle null (1000 perms, seed 35725763380): mean=0.6942, p95=0.8929

## 4. OBSERVATIONS vs DERIVED MEASUREMENTS

### Raw Evidence → Derived Measurements

- **Duplication**: 182/192 tasks share intent_template → 0.9479 (bootstrap 2000 reps)
- **Exact-copy**: 15/192 tasks have identical template AND instantiation_dict → 0.0781
- **Parameterization**: 172/192 tasks have non-empty instantiation_dict → 0.8958
- **Family sizes**: 36/49 families have ≥3 tasks; 34 have ≥4; 33 have ≥5
- **Mind2Web overlap**: 33 distinct train mechanisms, 27 distinct test_website mechanisms, 20 overlapping → 0.7407
- **Shuffle null**: True overlap (0.7407) exceeds null mean (0.6942) by 0.0466, does NOT exceed null p95 (0.8929)

### Interpretation (Viability)

- **WebArena within-store axis**: PARTIAL PASS. All quantitative thresholds met (duplication ≥0.5, parameterization ≥0.3, exact-copy <0.2, families ≥5 with ≥3 tasks, families ≥3 with ≥4 tasks). However, AX consistency threshold (0.6) is NOT TESTABLE from REUSED parent trees. The parent sampled 1 task per family, so within-family AX consistency cannot be directly verified. PC1_WEB_SEARCH PASS and intent-to-element 5/5 PASS from parent support element-pattern consistency at the template description level.
- **Mind2Web cross-website axis**: FAIL. While overlap (0.7407) exceeds the absolute threshold (0.15), it fails the shuffle null comparison (excess 0.0466 < 0.10). The high null overlap (0.6942) reflects coarse mechanism clustering and structural similarity of web tasks across sites.
- **Clause 5**: High duplication (0.9479) is parameterized (exact-copy 0.0781 < 0.2). Parent MIXED duplication clause is SUPERSEDED per spec decision_rule clause 5.

## 5. Controls

| Control | Expected | Observed | Pass? |
|---------|----------|----------|-------|
| PC1_WEB_SEARCH | Search combobox+button on homepage | PASS (from parent AX trees) | PASS |
| PC2_MIND2WEB_RECURRENCE | Recurring cluster in ≥10 tasks across ≥3 websites | PASS (max cluster=151) | PASS |
| NC1_WIKIPEDIA_NULL | No shopping mechanisms | NOT EXERCISED | null |
| NC2_SHUFFLE_NULL | True overlap exceeds null by ≥0.10 | Excess=0.0466 <0.10 | FAIL |
| NC3_WEB_EXACT_COPY_NULL | Exact-copy <0.2 | 0.0781 <0.2 | PASS |

## 6. Validity Threats

1. **AX consistency unverifiable**: Parent sampled 1 task per family; within-family AX consistency requires 2+ tasks per family extracted via CDP Accessibility.getFullAXTree. Playwright not installed. This is a measurement limitation, not a falsification.
2. **Mind2Web spec divergence**: 73 websites/3 domains vs spec's 137/31. Overlap measurement on actual dataset may not generalize.
3. **Coarse mechanism clustering**: Mind2Web normalization produces only 33 distinct train mechanisms, inflating both true and null overlap. Finer-grained clustering could change results.
4. **Shuffle null high**: Null mean (0.6942) reflects structural similarity of web tasks, not random assignment. This is expected for web-task datasets.
5. **Below-fold exclusion**: Initial-viewport CDP trees only; post-checkout AX patterns not measured.
6. **Dataset integrity**: WebArena census matches parent exactly (192/49/0.9479/0.0781/0.8958), confirming no data corruption.

## 7. Decision Rule Evaluation

```
Gate 0: PASSED (datasets available)
Clause 1 (WebArena within-store): PARTIAL/FAIL
  - dup=0.9479 ≥0.5 ✓
  - param=0.8958 ≥0.3 ✓
  - copy=0.0781 <0.2 ✓
  - families≥3=36 ≥5 ✓
  - families≥4=34 ≥3 ✓
  - ax_check=False (ax_consistency=None, unverifiable) ✗
  - pc1=True ✓
Clause 2 (Mind2Web cross-website): FAIL
  - overlap=0.7407 ≥0.15 ✓
  - excess=0.0466 <0.10 ✗
  - param=0.6085 ≥0.15 ✓
  - pc2=True ✓
Clause 5: SUPERSEDED (high duplication is parameterized)
Verdict: MIXED (WebArena partial PASS, Mind2Web cross-website FAIL, AX unverifiable)
```

## 8. Product Consequence

**Positive (partial)**: WebArena within-store template-family hold-out is quantitatively viable for C-LLM-INHERIT (192 tasks, 49 families, 36 with ≥3 tasks, 0.8958 parameterized). Product/Graph lane can design within-store hold-out experiment.

**Negative (Mind2Web)**: Cross-website website-holdout design for C-CROSSSITE is NOT demonstrably same-mechanism (shuffle null exceeds excess threshold). Future website-holdout must be limited to within-store families or custom benchmark construction.

**Ceiling**: This experiment quantifies dataset substrate viability ONLY. It does NOT demonstrate LLM inheritance benefit, freshness, or repair. C-LLM-INHERIT remains EXPERIMENTAL pending future Product experiment (cold vs retrieval vs SPIDER on this substrate).

## 9. What This Experiment Is NOT

- NOT an LLM agent inheritance test (no cold vs retrieval vs SPIDER execution)
- NOT a browser end-to-end execution of cart/checkout flows
- NOT a re-tuning of viewport heuristics
- NOT a repetition of the 12-store cross-site question on v2 (already shown impossible)
- NOT a claim of freshness, delta-repair, or product economics beyond substrate viability

## 10. Artifacts

- `research/experiments/EXP-INTEL-35725763380/artifacts/derived/measurements.json` — all metrics, bootstrap CIs, shuffle null distribution
- `research/experiments/EXP-INTEL-35725763380/artifacts/raw/webarena-verified.json` — dataset (sha256 d6527566...)
- `research/intel/exp_35725763380_measure.py` — frozen measurement script
- `research/experiments/EXP-INTEL-35697055679/artifacts/raw/webarena-verified.json` — reused dataset
- `research/experiments/EXP-INTEL-35697055679/artifacts/derived/measurements.json` — reused parent measurements (10 AX trees)
- `research/experiments/EXP-INTEL-35697055679/artifacts/raw/axtree_task_*.json` — reused AX trees (REUSED label)
