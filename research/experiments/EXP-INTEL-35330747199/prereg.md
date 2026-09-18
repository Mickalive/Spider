# EXP-INTEL-35330747199 preregistration

## Status

DESIGN NOT YET FROZEN.

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35330747199
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID
- **Created**: 2026-09-18T09:40:36.618320+00:00
- **Origin Run**: 35330747199
- **Request Reason**: pulse

## Inherited State

**Parent**: EXP-INTEL-35290611333 (handoff sha256: d92f9a0d692649c43eec8ed19cee58352bca797c3b6b58293d38628a3dbe8b93)

**Inherited Last Verdict**: REVISE — Producer SURVIVES_CURRENT_TEST claim not justified at systematic-review ceiling. Literature synthesis at non-systematic ceiling. C-MEAS-VALID remains EXPERIMENTAL.

**Inherited Next Question**: Does C2 FALSE (density ordering less stable than random role subsets) hold on full-DOM enumeration after the runtime lane removes the locatableSample cap at measure_fullpage_yield.py:89 — and does the per-task weighted recipe's C2 TRUE reversal also persist on full-DOM, confirming that recipe choice remains material at scale?

**Why This Experiment Diverges from Inherited Next Question**: The full-DOM empirical validation is BLOCKED by the runtime locatableSample cap (substrate dependency, confirmed still present at measure_fullpage_yield.py:89 as of EXP-INTEL-35166505835). The intel lane cannot unblock this. Instead, this experiment addresses unresolved question U2 from the parent chain: operationalizing the OECD/COINr sensitivity analysis framework for SPIDER's density metric to produce a principled MIXED outcome decision rule. This resolves a design blocker that would otherwise delay the full-DOM re-run even after the substrate fix lands.

### Carry-Forward from Parent Chain

**Established** (inherited verbatim):
1. Recipe reversal is genuine, NOT an implementation artifact (EXP-INTEL-35264637598)
2. Recipe choice is a MATERIAL determinant of C-MEAS-VALID density metric conclusion (EXP-INTEL-35264637598)
3. Canonical per-iteration p=0.5 recipe remains principled choice (EXP-INTEL-35264637598)
4. Recipe choice ambiguity documented in psychometrics, econometrics, meta-analysis (EXP-INTEL-35280397316, EXP-INTEL-35290611333)
5. OECD sensitivity analysis framework provides principled MIXED-outcome handling method (EXP-INTEL-35290611333)
6. Principled resolution methods exist across fields (EXP-INTEL-35280397316, EXP-INTEL-35290611333)

**Rejected** (inherited verbatim):
1. Frozen SURVIVES_REVERSAL_PERSISTS decision rule not achievable (EXP-INTEL-35264637598)
2. Parent stored per-task weighted null mean ~0.28 not precisely reproducible (EXP-INTEL-35264637598)
3. Parent stored canonical null mean 0.5273 not precisely reproducible (EXP-INTEL-35264637598)
4. Producer SURVIVES at systematic-review ceiling not justified (EXP-INTEL-35290611333)

**Unknown** (relevant subset):
1. Full-DOM generalization of C2 FALSE/TRUE — BLOCKED by substrate
2. OECD sensitivity framework operationalization for SPIDER density metric — ADDRESSED BY THIS EXPERIMENT
3. Social choice theory axioms applicable to SPIDER — NOT ADDRESSED (requires formal mathematical mapping)
4. Meta-analytic heterogeneity adaptation — NOT ADDRESSED (requires empirical variance data)
5. Cross-site generalization — NOT ADDRESSED (requires multi-site data)
6. MIXED outcome decision rule formalization — ADDRESSED BY THIS EXPERIMENT

**Do Not Assume** (inherited verbatim):
1. SPIDER-to-field applicability mappings are established results — they are interpretive analogies
2. Non-systematic literature search captured all relevant prior art
3. FALSIFIED conclusion generalizes to full-DOM
4. Density metric is entirely useless
5. Per-iteration recipe is universally canonical
6. Recipe choice is a nuisance parameter
7. C-MEAS-VALID status changed from prior experiments
8. OECD/social choice/meta methods have been validated for SPIDER

## 1. Scientific Question

Can the OECD/COINr sensitivity analysis framework be operationalized on existing truncated-first-20 density data to produce a principled MIXED outcome decision rule for SPIDER's density metric recipe ambiguity?

## 2. Hypothesis

The OECD/COINr framework applied to per-task density scores from both recipes (canonical per-iteration p=0.5 and per-task weighted) across 3 definitions and 7 tasks will produce:
- (a) Non-degenerate dominance pairs (0% < dominance < 100%)
- (b) Confidence intervals with width < 50th percentile of density range
- (c) Recipe-sensitivity classification distinguishing task-definition pairs where recipe choice matters from those where it does not

## 3. Falsifier

The framework is falsified if ANY of:
- F1: Dominance pairs are degenerate (all 0% or all 100%) across all 21 task-definition pairs
- F2: Confidence interval width exceeds 90th percentile of density range for all pairs
- F3: Recipe-sensitivity classification assigns all pairs to the same category
- F4: Framework produces errors or NaN on >20% of task-definition pairs

## 4. Data Source

Per-task density values reconstructed from existing truncated-first-20 raw evidence:
- Primary: EXP-INTEL-35083033552 raw_results.json (referenced in EXP-INTEL-35264637598 provenance as sha da30bd05)
- Fallback: Re-run analysis code from EXP-INTEL-35264637598 on the same 7-task, 3-definition, truncated-first-20 dataset
- The 7 tasks: 3 product_listing, 3 detail, 1 cart (from Magento site)
- The 3 definitions: DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK
- The 2 recipes: canonical per-iteration (p=0.5) and per-task weighted

Note: Raw density values were computed in-memory during EXP-INTEL-35264637598 but not persisted to result.json (which stores only agreement metrics M3/M4/M7/M8). Reconstruction is required.

## 5. Sampling Policy

No new data collection. Analysis is offline on reconstructed data from existing truncated-first-20 sample. All 21 task-definition pairs (7 tasks x 3 definitions) with both recipe density values constitute the analysis population.

## 6. Unit of Analysis

Task-definition pair: each of the 21 (task, definition) combinations receives a density score from each recipe, plus derived dominance, CI, and classification.

## 7. Holdout

None. This is a framework operationalization exercise, not a predictive model. All data is used for framework evaluation.

## 8. Baselines

- B1: Binary C2 outcome (per-iteration FALSE vs per-task TRUE, divergence 0.38)
- B2: Random classification (33% each category)
- B3: Full-DOM (placeholder, BLOCKED)

## 9. Positive Control

PC1: Framework executes without error on reconstructed density matrix and produces outputs for >= 80% (17/21) pairs.

## 10. Null Control

NC1: When recipe labels are randomly shuffled (1000 permutations), dominance pairs converge to ~50% (within 15%) and CI width increases (>= 1.3x original).

## 11. Primary Metrics

- M1: DOMINANCE_PAIRS — list of (task, definition, dominance%) for all 21 pairs. Dominance = % of alternative recipes that the primary recipe dominates in ranking.
- M2: RANKING_CI — 95% confidence interval on per-task density rank for each recipe, computed via bootstrap (1000 resamples of definition weights).
- M3: CI_WIDTH — width of ranking CI for each pair, normalized by density range.
- M4: SENSITIVITY_CLASS — LOW (CI width < 25th percentile), MEDIUM (25th-75th), HIGH (> 75th) for each pair.
- M5: DOMINANCE_MEAN — mean dominance across all 21 pairs.
- M6: DOMINANCE_SD — standard deviation of dominance across pairs.
- M7: CLASSIFICATION_ENTROPY — Shannon entropy of the classification distribution (maximizes at 3 categories equally populated).
- M8: NULL_DOMINANCE_MEAN — mean dominance under shuffled recipe labels (1000 permutations).
- M9: NULL_CI_WIDTH_RATIO — ratio of shuffled CI width to original CI width.

## 12. Expected Direction

- Dominance pairs should show variation (SD > 10%) across task-definition pairs, indicating the framework discriminates.
- Classification entropy should be > 1.0 bits (out of max 1.585 for 3 categories), indicating non-degenerate distribution.
- Null dominance should be near 50% (within 15%), confirming framework detects real recipe structure.
- Null CI width ratio should be > 1.3, confirming shuffling increases uncertainty.

## 13. Uncertainty Method

Bootstrap confidence intervals (1000 resamples) for dominance pairs. Permutation test (1000 shuffles) for null control. Shannon entropy for classification quality.

## 14. Adequacy Rule

The framework is adequate for MIXED outcome handling if it passes C1-C5 (spec.json decision_rule). If MIXED verdict, the framework is conditionally adequate pending validation on full-DOM data.

## 15. Decision Rule

Conjunctive (from spec.json):
- SURVIVES: C1 AND C2 AND C3 AND C4 AND C5
- MIXED: C1 AND (C2 OR C3 OR C4) AND NOT C5
- FALSIFIED-IN-SETTING: C1 AND NOT (C2 OR C3 OR C4)
- MEASUREMENT_INVALID: NOT C1

## 16. Validity Threats

1. **Truncated-sample scope**: All results apply only to truncated-first-20 locatable sample (7 tasks, 1 site, 3 definitions). No extrapolation to full-DOM or cross-site.
2. **Data reconstruction risk**: Per-task density values must be reconstructed from prior experiments. Reconstruction fidelity depends on raw evidence availability and analysis code reproducibility.
3. **Small sample**: 7 tasks (3 types, cart n=1) may be too few for stable dominance pair estimation. Bootstrap CIs may be unreliable at this sample size.
4. **Definition set limited**: Only 3 of 5 definitions used. OECD framework results may differ with full 5-definition set.
5. **Framework novelty**: OECD/COINr has not been previously applied to SPIDER density metric. The mapping from composite indicator sensitivity to density recipe sensitivity is an interpretive analogy (do_not_assume[0]).
6. **Threshold sensitivity**: Classification thresholds (LOW/MEDIUM/HIGH at 25th/75th percentiles) are arbitrary and may affect C4 outcome.

## 17. Claim Ceiling

If SURVIVES: The OECD/COINr sensitivity analysis framework is operationalizable for SPIDER's density metric recipe ambiguity at truncated-first-20 ceiling. Dominance pairs, ranking CIs, and sensitivity classification provide a principled MIXED outcome decision rule. This resolves the MIXED outcome amendment blocker for C-MEAS-VALID promotion, but does NOT promote C-MEAS-VALID itself (pending full-DOM empirical validation). The framework must be re-validated on full-DOM data before any claim generalization.

If FALSIFIED: The OECD/COINr framework is not operationalizable for SPIDER's density metric on this data. The density metric program must pivot to alternative MIXED outcome handling or restrict to recipe-insensitive pairs.

## 18. Product Consequence

- Positive: Product lane gains a concrete MIXED outcome protocol (dominance pairs, CIs, classification) for the full-DOM re-run. This unblocks the frozen spec amendment needed before any SURVIVES promotion.
- Negative: MIXED outcome decision rule remains unresolved, blocking C-MEAS-VALID promotion even after substrate fix and full-DOM re-run.

## 19. Relationship to Inherited Next Question

This experiment does NOT address the inherited next question (full-DOM C2 FALSE/TRUE validation) directly. It addresses a prerequisite: the MIXED outcome decision rule that must be frozen before the full-DOM re-run can produce a promotable result. The sequence is:
1. This experiment: operationalize OECD framework on truncated data → produce MIXED decision rule
2. Runtime lane: remove locatableSample cap → unblock full-DOM data
3. Next intel/graph experiment: re-run density metric on full-DOM with both recipes and frozen MIXED decision rule

If this experiment is FALSIFIED, step 3 must use a different MIXED handling approach before proceeding.
