# EXP-INTEL-35353016702 preregistration

## Status

DESIGN NOT YET FROZEN.

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35353016702
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID
- **Created**: 2026-09-18T13:55:05.550962+00:00
- **Origin Run**: 35353016702
- **Request Reason**: pulse

## Inherited State

**Parent**: EXP-INTEL-35330747199 (handoff sha256: f1cb221b32b91f2669012155a9298493474d471bf6c8536b6b81851643f16341)

**Inherited Last Verdict**: REVISE — Producer's MIXED outcome is not justified per frozen decision_rule. The observed C-pattern (C1 PASS, C2 FAIL, C3 PASS, C4 PASS, C5 PASS) has no frozen bucket: MIXED requires NOT C5 but C5 passes (null_ci_gte_13x true, dominance within 15%). This is a preregistration coverage defect (audit V1_DECISION_RULE_UNCLASSIFIABLE), not a scientific result. Additionally, C2_DOMINANCE_INFORMATIVE is construct-impossible with exactly 2 recipes (all dominance necessarily 0%/100%, audit V2), C3_CI_INFORMATIVE compares rank-width to density-range in incommensurable units (audit V3), C4 chi-square never computed and N=14 vs frozen 21 (audit V4), and C5 null dominance is tautological with 2 recipes (audit V5). The OECD/COINr framework as operationalized is not informative for MIXED outcome handling in the 2-recipe setting. The parent's next question (full-DOM C2 reversal persistence) remains blocked by the runtime locatableSample cap. C-MEAS-VALID status unchanged: remains EXPERIMENTAL.

**Inherited Next Question**: Can a third recipe variant (e.g., meta-analytic combination of canonical and weighted, or a new structural recipe) break the 2-recipe dominance degeneracy and make the OECD/COINr framework informative for MIXED outcome handling — and does this reformulated decision rule survive on full-DOM data after the runtime lane removes the locatableSample cap?

**Why This Experiment Diverges from Inherited Next Question**: This experiment directly addresses the first part of the inherited next question: whether a third recipe breaks the 2-recipe degeneracy. The inherited question also asks about full-DOM survival, but that remains BLOCKED by the runtime locatableSample cap. This experiment tests the theoretical viability of the 3-recipe approach on existing truncated-first-20 data. If the 3-recipe approach is FALSIFIED (still degenerate), the full-DOM re-run with 3 recipes cannot produce a promotable result, and the MIXED outcome strategy must pivot before wasting a runtime-lane cycle.

### Carry-Forward from Parent Chain

**Established** (inherited verbatim):
1. Recipe reversal is genuine, NOT an implementation artifact: per-task weighted C2 TRUE vs canonical per-iteration C2 FALSE, divergence 0.38. (EXP-INTEL-35264637598 handoff.json established[0-1])
2. Recipe choice is a MATERIAL determinant of C-MEAS-VALID density metric conclusion. (EXP-INTEL-35264637598 handoff.json established[1])
3. Canonical per-iteration p=0.5 recipe remains principled choice for C-MEAS-VALID. (EXP-INTEL-35264637598 handoff.json established[2])
4. OECD/COINr sensitivity analysis framework provides principled MIXED-outcome handling method in theory: systematically vary aggregation methods and weights, quantify ranking stability via dominance pairs and CIs, report robustness bounds. Non-systematic synthesis ceiling, interpretive analogy to SPIDER. (EXP-INTEL-35290611333 result.json M4, audit.json B2)
5. Recipe choice ambiguity is documented across psychometrics, econometrics, meta-analysis, and IR. Non-systematic synthesis ceiling. (EXP-INTEL-35280397316, EXP-INTEL-35290611333)
6. Principled resolution methods exist across fields: recipe-as-question-binding, sensitivity reporting, micro/macro/weighted framework, OECD sensitivity analysis. (EXP-INTEL-35280397316, EXP-INTEL-35290611333)
7. Canonical and per-task weighted recipes occupy fundamentally different density regimes: 84.7x cross-recipe ratio, mean absolute difference 0.50. Recipe choice is a structural regime change, not a parameter sensitivity. (EXP-INTEL-35330747199 result.json M1, M10)
8. Within each recipe, the three definitions (DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK) produce highly correlated rankings (Spearman r > 0.98). Definition choice is not the primary source of recipe sensitivity. (EXP-INTEL-35330747199 result.json OBS-6)

**Rejected** (inherited verbatim):
1. Frozen SURVIVES_REVERSAL_PERSISTS decision rule not achievable. (EXP-INTEL-35264637598 handoff.json rejected[0])
2. Parent stored per-task weighted null mean ~0.28 not precisely reproducible. (EXP-INTEL-35264637598 handoff.json rejected[1])
3. Parent stored canonical null mean 0.5273 not precisely reproducible. (EXP-INTEL-35264637598 handoff.json rejected[2])
4. Producer SURVIVES at systematic-review ceiling not justified: web-search-API not systematic databases. (EXP-INTEL-35290611333 audit V1)
5. OECD/COINr dominance framework is NOT informative for 2-recipe comparisons: dominance is necessarily 0%/100% (binary), all42 task-definition-recipe triples degenerate, hypothesis (a) was a priori unfalsifiable in this design. (EXP-INTEL-35330747199 result.json OBS-3, VN-1; audit V2)
6. Producer MIXED outcome is not justified per frozen decision_rule: MIXED requires NOT C5 but C5 passes. This is a preregistration coverage defect (V1), not a scientific result. (EXP-INTEL-35330747199 audit V1)

**Unknown** (relevant subset):
1. Full-DOM generalization of C2 FALSE/TRUE reversal: bounded to truncated-first-20 (7 tasks, 1 site, 3 definitions, locatable_sample cap 20). BLOCKED by runtime substrate. (EXP-INTEL-35264637598 handoff.json unknown[0], EXP-INTEL-35330747199 result.json U-1)
2. Whether a third recipe variant would produce non-degenerate dominance pairs under OECD/COINr framework. ADDRESSED BY THIS EXPERIMENT — meta-analytic mean is the simplest possible third recipe. (EXP-INTEL-35330747199 result.json U-2)
3. Whether the near-zero canonical density (mean 0.006) reflects actual page structure or is an artifact of p=0.5 independent inclusion model on sparse DOM elements. NOT ADDRESSED. (EXP-INTEL-35330747199 result.json U-3)
4. Correct reformulation of C2_DOMINANCE_INFORMATIVE for 2-recipe comparisons (density ratio vs ranking reversal rate). SUPERSEDED — 3-recipe approach makes this reformulation unnecessary if it works. (EXP-INTEL-35330747199 result.json U-4)
5. Proper unit-consistent C3 CI width vs density range comparison after fixing normalization. NOT ADDRESSED. (EXP-INTEL-35330747199 audit V3, U-5)
6. Informative null control for dominance that does not preserve binary structure when n_recipes=2. SUPERSEDED — 3-recipe approach makes this irrelevant if it works. (EXP-INTEL-35330747199 audit V5, U-6)
7. Whether the 84.7x cross-recipe gap persists with full locatable_sample data (21-82 elements vs cap 20). NOT ADDRESSED. (EXP-INTEL-35330747199 result.json U-1)
8. Social choice theory axioms applicable to SPIDER. NOT ADDRESSED. (EXP-INTEL-35290611333 carry_forward unknown[3])
9. Meta-analytic heterogeneity adaptation. NOT ADDRESSED. (EXP-INTEL-35290611333 carry_forward unknown[4])
10. Cross-site generalization. NOT ADDRESSED. (EXP-INTEL-35290611333 carry_forward unknown[8])
11. MIXED outcome decision rule formalization: requires either OECD framework operationalization with 3+ recipes, or alternative approach. PARTIALLY ADDRESSED — this experiment tests 3-recipe viability. (EXP-INTEL-35330747199 carry_forward unknown[11])

**Do Not Assume** (inherited verbatim):
1. Do NOT use OECD/COINr framework with only 2 recipes to justify recipe choice — dominance is necessarily degenerate (0%/100%) by construction, not by scientific finding.
2. Do NOT assume the 84.7x cross-recipe density ratio is a validated scientific result — it is observed on truncated-first-20 data (locatable_sample cap 20) and may change with full DOM enumeration.
3. Do NOT assume the OECD/COINr framework has been validated for SPIDER's density metric — the 2-recipe experiment demonstrated it is NOT informative in the 2-recipe setting (construct failure, not empirical validation).
4. Do NOT assume SPIDER-to-field applicability mappings are established results — they are interpretive analogies bounded by audit findings.
5. Do NOT assume the non-systematic literature search captured all relevant prior art — a formal systematic review may yield additional methods.
6. Do NOT assume the FALSIFIED conclusion generalizes to full-DOM — truncated-first-20 is a non-representative slice.
7. Do NOT assume the per-iteration recipe is universally canonical beyond this experiment's scope.
8. Do NOT assume the density metric is entirely useless — ordering-based discrimination is definition-sensitive and recipe-sensitive, not that density values are uninformative.
9. Do NOT assume recipe choice is a nuisance parameter — it is a MATERIAL determinant of the scientific conclusion.
10. Do NOT assume C-MEAS-VALID status changed from this experiment — it remains EXPERIMENTAL; this experiment attempted framework operationalization, not empirical measurement validation.
11. Do NOT assume quantitative parent values are reliable — deviations exceed frozen thresholds.
12. Do NOT assume the MIXED outcome decision rule is resolved — it remains open pending either third-recipe operationalization or full-DOM empirical validation.
13. Do NOT assume the meta-analytic mean recipe is the optimal third recipe — it is the simplest computable third recipe. A structural recipe (DOM hierarchy depth) or other non-linear combination might perform differently.

## 1. Scientific Question

Does a third recipe variant (meta-analytic mean of canonical per-iteration and per-task weighted density) break the 2-recipe dominance degeneracy under the OECD/COINr framework on truncated-first-20 density data, producing at least one non-degenerate dominance pair (10% < dominance < 90%)?

## 2. Hypothesis

The OECD/COINr framework's 2-recipe degeneracy is a mathematical artifact of having exactly 2 alternatives (dominance is necessarily 0% or 100% by definition). Adding a third recipe (meta-analytic mean of the two existing recipes) makes dominance ternary (0%, 50%, 100%), and because recipe sensitivity is task-dependent (established: recipe choice is MATERIAL, EXP-INTEL-35264637598), some task-definition pairs will show the meta-analytic mean ranking between the two original recipes, producing non-degenerate dominance values.

## 3. Falsifier

The framework is falsified if ANY of:
- F1: All 63 dominance pairs (21 task-definition pairs x 3 pairwise comparisons) remain degenerate (0% or 100%) with the third recipe added
- F2: The third recipe produces identical rankings to one of the existing recipes across all 21 task-definition pairs (meta-analytic mean is a linear combination that preserves ranking)
- F3: The third recipe produces NaN or error on >20% of pairs due to ties or density reconstruction failures

## 4. Data Source

Per-task density values reconstructed from existing truncated-first-20 raw evidence:
- Primary: EXP-INTEL-34782350557 raw_results.json (source measurement data, locatable_sample capped at 20)
- The 7 tasks: 3 product_listing, 3 detail, 1 cart (from Magento site)
- The 3 definitions: DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK
- The 2 original recipes: canonical per-iteration (p=0.5) and per-task weighted
- The 3rd recipe: meta-analytic mean = (canonical + weighted) / 2

Note: Density values were computed in-memory during EXP-INTEL-35264637598 and EXP-INTEL-35330747199 but not persisted to result.json. Reconstruction is required from the raw locatable_sample data using the density computation code from those experiments.

## 5. Sampling Policy

No new data collection. Analysis is offline on reconstructed data from existing truncated-first-20 sample. All 21 task-definition pairs (7 tasks x 3 definitions) with both original recipe density values constitute the analysis population. The meta-analytic mean is deterministically computed from these values.

## 6. Unit of Analysis

Task-definition pair: each of the 21 (task, definition) combinations receives a density score from each of the 3 recipes (canonical, weighted, meta-analytic mean), plus derived dominance for all 3 pairwise comparisons.

## 7. Holdout

None. This is a framework operationalization exercise, not a predictive model. All data is used for framework evaluation.

## 8. Baselines

- B1: 2-recipe OECD framework (all pairs degenerate, from EXP-INTEL-35330747199)
- B2: Random third recipe (shuffled density values)
- B3: Monotone third recipe (always ranks between the two originals — theoretical bound)

## 9. Positive Control

PC1: Framework executes on 3-recipe x 21-pair density matrix without error. Meta-analytic mean computable for all 21 pairs.

## 10. Null Control

NC1: Shuffled third recipe produces fewer non-degenerate pairs than real third recipe, or shuffled non-degenerate values are closer to 50% (less informative).

## 11. Primary Metrics

- M1: DOMINANCE_PAIRS_3RECIPE — list of (task, definition, comparison, dominance%) for all 63 comparisons (21 pairs x 3 comparisons: canonical vs weighted, canonical vs mean, weighted vs mean). Dominance = % of task-definition pairs where the primary recipe ranks higher.
- M2: NONDEGENERATE_COUNT — number of dominance pairs with 10% < dominance < 90% across all 63 comparisons.
- M3: RANKING_CHANGE_COUNT — number of task-definition pairs where the meta-analytic mean ranking differs from both original recipe rankings (not simply between them).
- M4: NULL_NONDEGENERATE_COUNT — number of non-degenerate pairs under shuffled third recipe (1000 permutations).
- M5: NULL_DOMINANCE_MEAN — mean dominance under shuffled third recipe.
- M6: DENSITY_MATRIX — the full 7x3x3 density matrix (tasks x definitions x recipes) for reproducibility.

## 12. Expected Direction

- At least 1 non-degenerate dominance pair exists with the 3rd recipe (M2 >= 1).
- The meta-analytic mean produces different rankings from both originals on >= 3 pairs (M3 >= 3).
- Shuffled third recipe produces fewer or equal non-degenerate pairs (M4 <= M2).

## 13. Uncertainty Method

No uncertainty estimation needed — this is a deterministic computation on a fixed dataset. Bootstrap CIs are not appropriate for dominance pairs computed from a single density matrix. The null control uses permutation (shuffling recipe labels) to establish whether non-degeneracy is artifactual.

## 14. Adequacy Rule

The 3-recipe framework is adequate for MIXED outcome handling if it passes C1-C4 (spec.json decision_rule). If SURVIVES, the framework is viable pending full-DOM validation. If FALSIFIED, the density metric program must pivot.

## 15. Decision Rule

Conjunctive (from spec.json):
- SURVIVES: C1 AND C2 AND C3 AND C4
- MIXED: C1 AND C2 AND NOT C4
- FALSIFIED-IN-SETTING: C1 AND NOT C2
- MEASUREMENT_INVALID: NOT C1

## 16. Validity Threats

1. **Truncated-sample scope**: All results apply only to truncated-first-20 locatable sample (7 tasks, 1 site, 3 definitions). No extrapolation to full-DOM or cross-site.
2. **Meta-analytic mean is a linear combination**: The simplest third recipe is a weighted average of the two existing recipes. If the two recipes have perfectly correlated rankings across tasks (rank correlation = 1.0), the mean will preserve those rankings and produce no non-degenerate pairs. This is a mathematical constraint, not an empirical finding.
3. **Data reconstruction risk**: Per-task density values must be reconstructed from prior experiments. Reconstruction fidelity depends on raw evidence availability and analysis code reproducibility.
4. **Small sample**: 7 tasks (3 types, cart n=1) may be too few for stable dominance estimation. Dominance percentages are necessarily multiples of 1/7 ≈ 14.3%.
5. **Definition set limited**: Only 3 of 5 definitions used. OECD framework results may differ with full 5-definition set.
6. **Threshold sensitivity**: Non-degeneracy threshold (10% < dominance < 90%) is chosen to exclude ties (which produce 50% dominance for all pairs in 3-recipe setting). The threshold may need adjustment if ties are common.
7. **Not a structural recipe**: The meta-analytic mean is a numerical combination, not a structurally different recipe (e.g., DOM hierarchy depth). A structural recipe might produce genuinely different rankings.

## 17. Claim Ceiling

If SURVIVES: The 3-recipe OECD/COINr framework is operationalizable for SPIDER's density metric recipe ambiguity at truncated-first-20 ceiling. Non-degenerate dominance pairs provide a principled MIXED outcome decision rule. This resolves the MIXED outcome amendment blocker for C-MEAS-VALID promotion, but does NOT promote C-MEAS-VALID itself (pending full-DOM empirical validation). The framework must be re-validated on full-DOM data before any claim generalization.

If FALSIFIED: The 3-recipe OECD/COINr framework is not operationalizable for SPIDER's density metric on this data. The degeneracy is not solely a 2-recipe artifact; the density metric itself lacks sufficient task-dependent recipe sensitivity. The MIXED outcome decision rule must use an alternative approach (density ratio, ranking reversal rate) or the density metric program must restrict to recipe-insensitive task-definition pairs.

## 18. Product Consequence

- Positive: Product lane gains a concrete MIXED outcome protocol (3-recipe dominance pairs, sensitivity classification) for the full-DOM re-run. This unblocks the frozen spec amendment needed before any SURVIVES promotion.
- Negative: MIXED outcome decision rule remains unresolved, blocking C-MEAS-VALID promotion even after substrate fix and full-DOM re-run. Product lane must develop alternative MIXED handling or abandon density metric for recipe-sensitive pairs.

## 19. Relationship to Inherited Next Question

This experiment directly addresses the first clause of the inherited next question: "Can a third recipe variant break the 2-recipe dominance degeneracy?" The inherited question also asks about full-DOM survival, which remains BLOCKED by the runtime locatableSample cap. The sequence is:
1. This experiment: test 3-recipe viability on truncated data → determine if framework is worth pursuing
2. If SURVIVES: Runtime lane removes cap → full-DOM re-run with 3 recipes and frozen decision rule
3. If FALSIFIED: Pivot MIXED outcome strategy before wasting runtime-lane cycle on a re-run that cannot produce a promotable result

The meta-analytic mean is chosen as the simplest possible third recipe to minimize implementation cost while directly testing whether the 2-recipe degeneracy is a mathematical artifact or a property of the density metric. If the mean fails, a structural recipe (DOM hierarchy depth) could be tested as a follow-up, but this would require additional implementation effort.
