# EXP-INTEL-35280397316 preregistration

## 1. Experiment ID and Lane

- **Experiment ID**: EXP-INTEL-35280397316
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID

## 2. Question

How do established measurement frameworks (code coverage, information retrieval, web analytics) handle recipe choice ambiguity when aggregating metrics across multiple definitions or dimensions, and can principled resolution methods inform SPIDER's density metric recipe choice problem?

## 3. Hypothesis

There exist principled methods for resolving recipe choice ambiguity in multi-definition metrics, and these methods can inform SPIDER's density metric recipe choice problem. The recipe choice instability (canonical per-iteration C2 FALSE vs per-task weighted C2 TRUE) is a known phenomenon in measurement theory with established resolution approaches.

## 4. Falsifier

- **F1**: No principled methods exist in established measurement frameworks for resolving recipe choice ambiguity. Recipe choice is treated as an arbitrary implementation decision in all relevant fields (code coverage, information retrieval, web analytics).
- **F2**: The density metric recipe choice problem is fundamentally different from known measurement ambiguity problems and cannot be informed by prior art.

## 5. Baselines

- **Current SPIDER approach**: Principled justification (prereg §4) but not empirically validated on full-DOM data
- **Null hypothesis**: Recipe choice is arbitrary and no principled resolution methods exist

## 6. Positive Control

Well-documented cases of recipe choice ambiguity in established fields:
1. **Code coverage metrics**: Line vs branch vs path coverage aggregation (how to combine coverage across multiple test suites or definition families)
2. **Information retrieval**: Precision/recall aggregation across query sets (micro vs macro averaging, topic-weighted vs uniform)
3. **Web analytics**: Page density/engagement metrics across definition families (how to aggregate when definitions disagree)

## 7. Null Control

Systematic search finds no principled methods for resolving recipe choice ambiguity in any established measurement framework.

## 8. Measurement Validity

- Systematic literature search with reproducible search criteria (databases, keywords, date range)
- Documented inclusion/exclusion criteria for relevant prior art
- Reproducible synthesis methodology (structured comparison matrix)
- Bounded claim ceiling to published literature only (no new empirical measurement)

## 9. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
1. PC1 passes (at least 2 well-documented cases of recipe choice ambiguity found in established fields)
2. PC2 passes (at least 1 principled resolution method identified that is applicable to SPIDER's density metric problem)
3. F1 not triggered (principled methods exist in at least 1 established field)
4. F2 not triggered (density metric problem is not fundamentally different from known problems)

**FALSIFIED_IN_SETTING** if F1 triggered (no principled methods exist).

**MEASUREMENT_INVALID** if literature search is insufficient or synthesis methodology is flawed.

## 10. Product Consequence

**Positive**: SURVIVES informs spec amendment for MIXED outcomes and provides principled resolution methods for the recipe choice problem. Product lane gains a theoretically grounded approach to recipe selection, enabling advancement beyond the current blocking ambiguity.

**Negative**: FALSIFIED_IN_SETTING (F1 triggered: no principled methods exist) means recipe choice remains an unresolved fundamental issue. The density metric program cannot advance until the recipe ambiguity is resolved by empirical means (full-DOM re-run with both recipes).

## 11. Validity Threats

- **Threat 1**: Literature search may miss relevant prior art in niche fields. Mitigation: Use multiple databases (ACM DL, IEEE Xplore, arXiv, Google Scholar) and cross-reference citations.
- **Threat 2**: Synthesis may overgeneralize from limited examples. Mitigation: Document exact search criteria and inclusion/exclusion decisions; bound claims to published literature only.
- **Threat 3**: Density metric problem may be fundamentally different from known problems. Mitigation: F2 falsifier explicitly tests this; if triggered, acknowledge the gap and recommend empirical resolution.

## 12. Parent Handoff Inheritance

This experiment inherits from EXP-INTEL-35264637598 with the following carry-forward:

### Established
- Recipe reversal is genuine (canonical FALSE vs per-task weighted TRUE)
- Recipe choice is MATERIAL determinant of C-MEAS-VALID density metric conclusion
- Canonical per-iteration p=0.5 recipe remains principled choice for C-MEAS-VALID
- Parent MEASUREMENT_INVALID resolved into valid scientific finding within truncated-first-20 scope

### Rejected
- Frozen SURVIVES_REVERSAL_PERSISTS decision rule not achievable
- Parent stored per-task weighted null mean not precisely reproducible
- Parent stored canonical null mean not precisely reproducible

### Unknown
- Whether C2 FALSE and C2 TRUE reversal both hold on full-DOM enumeration
- Cross-site generalization
- Spec decision-rule amendment for MIXED outcomes

### Do Not Assume
- FALSIFIED conclusion generalizes to full-DOM
- Per-iteration recipe universally canonical beyond this experiment's scope
- Density metric entirely useless
- Recipe choice is a nuisance parameter
- C-MEAS-VALID status changed from parent experiment

## 13. Dependencies

- **None**: This experiment is pure literature synthesis and does not require blocked substrate or data.

## 14. Expected Outcome

If SURVIVES: The recipe choice problem is a known phenomenon with principled resolution methods. SPIDER can adopt established approaches to resolve the ambiguity, informing the spec amendment and enabling advancement.

If FALSIFIED_IN_SETTING: Recipe choice remains an unresolved fundamental issue requiring empirical resolution. The full-DOM re-run with both recipes becomes the critical next step.
