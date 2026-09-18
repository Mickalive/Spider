# EXP-INTEL-35290611333 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35290611333
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID
- **Parent**: EXP-INTEL-35280397316 (literature synthesis on recipe choice ambiguity in IR/code coverage/web analytics)
- **Request reason**: pulse (scheduled follow-up addressing audit unresolved items)

## 2. Scientific Question

Does a formal systematic search of psychometrics, econometrics, and meta-analysis literature on aggregation methods yield additional relevant prior art for SPIDER's density metric recipe choice problem, beyond the IR micro/macro/weighted framework identified in EXP-INTEL-35280397316?

## 3. Hypothesis

Psychometrics (e.g., test score aggregation, reliability generalization), econometrics (e.g., panel data aggregation, index construction), and meta-analysis (e.g., effect size pooling, heterogeneity quantification) contain principled aggregation methods that either:

(a) strengthen the existing IR analogy with additional evidence from independent fields,  
(b) provide alternative resolution frameworks more appropriate for SPIDER's density metric structure, or  
(c) inform the MIXED outcome decision-rule amendment needed for claim promotion.

## 4. Falsifiers

**F1**: No relevant prior art is found in psychometrics, econometrics, or meta-analysis that addresses aggregation recipe choice ambiguity — these fields either (a) use a single canonical recipe without ambiguity, (b) treat recipe choice as arbitrary, or (c) are fundamentally different from SPIDER's density metric problem.

**F2**: All found methods are weaker than the existing IR framework and do not improve the theoretical grounding for recipe selection.

## 5. Baselines

1. **Current SPIDER approach**: IR micro/macro/weighted analogy (interpretive, not established result; EXP-INTEL-35280397316)
2. **Null hypothesis**: Psychometrics, econometrics, and meta-analysis do not address aggregation recipe choice ambiguity, or their methods do not apply to SPIDER's density metric problem

## 6. Positive Controls

**PC1**: At least 2 well-documented aggregation recipe choice problems found in psychometrics or econometrics (analogous to IR micro/macro/weighted).

**PC2**: At least 1 principled method found that directly addresses the MIXED outcome problem (e.g., sensitivity analysis frameworks, heterogeneity quantification methods, or decision rules for conflicting aggregation results).

## 7. Null Controls

**NC1**: Systematic search finds no relevant prior art in psychometrics, econometrics, or meta-analysis that addresses aggregation recipe choice ambiguity for multi-definition metrics.

**NC2**: All found methods are already covered by the IR framework and provide no additional resolution power.

## 8. Measurement Validity

1. **Search protocol**: Three databases (PubMed for psychometrics, EconLit for economics, Cochrane for meta-analysis) with documented search strings and date range (2000-2026).
2. **Inclusion criteria**: Papers must address aggregation of multiple definitions/dimensions/indicators into a composite score, where the aggregation recipe choice affects the conclusion.
3. **Exclusion criteria**: Papers that (a) use a single canonical recipe without discussing alternatives, (b) treat recipe choice as arbitrary without principled justification, (c) are not in English, (d) are not peer-reviewed (except for working papers from established research groups).
4. **Reproducibility artifact**: Search strings, result counts, screening log, inclusion decisions documented in provenance.json.
5. **Claim ceiling**: Literature synthesis only, no new empirical measurement; claim ceiling is bounded to published literature in these three fields.

## 9. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
1. PC1 passes (at least 2 well-documented aggregation recipe choice problems found in psychometrics or econometrics)
2. PC2 passes (at least 1 method found that addresses MIXED outcome handling)
3. F1 not triggered (relevant prior art exists)
4. F2 not triggered (found methods improve on IR framework)

**FALSIFIED_IN_SETTING** if F1 triggered (no relevant prior art).

**MEASUREMENT_INVALID** if search protocol is insufficient or synthesis methodology is flawed.

## 10. Product Consequences

**Positive (SURVIVES)**: Provides stronger theoretical grounding for recipe selection and informs the MIXED outcome decision-rule amendment. Product lane gains (a) additional evidence that recipe choice is a principled design decision, (b) potentially a stronger resolution framework than IR micro/macro/weighted, and (c) a concrete proposal for handling MIXED outcomes in the decision rule. This unblocks DIRECTOR from promoting C-MEAS-VALID beyond EXPERIMENTAL once full-DOM data is available.

**Negative (FALSIFIED_IN_SETTING)**: The IR analogy remains the sole theoretical grounding, and it is an interpretive mapping not established in literature. Product lane must treat recipe choice as requiring empirical resolution (full-DOM re-run) without additional theoretical support. MIXED outcome handling remains unresolved.

## 11. Estimated Cost

Low: <1 GPU-hour. Literature search and synthesis only. No browser/network/model calls. No new data collection.

## 12. Expected Information Gain

High. Directly addresses audit unresolved item V1 (non-systematic search) and audit unresolved[4] (psychometrics/econometrics/meta-analysis). Either outcome materially changes the claim trajectory: SURVIVES provides stronger theoretical grounding and MIXED outcome proposal; FALSIFIED_IN_SETTING confirms the IR analogy is the best available framework and empirical resolution is required.

## 13. Validity Threats

1. **Search coverage**: Even with three databases, relevant papers may be missed if they use different terminology (e.g., "composite indicator" vs "aggregation recipe").
2. **Applicability mapping**: Like the IR analogy, any psychometrics/econometrics mapping will be an interpretive analogy, not an established result.
3. **Publication bias**: Fields with canonical recipes may not publish on recipe choice ambiguity because it is not considered a problem.
4. **Language bias**: Excluding non-English papers may miss relevant work in German, French, or Chinese psychometrics/econometrics traditions.

## 14. Inherited State (from parent handoff)

**Established**:
- Recipe choice ambiguity is a known phenomenon in established measurement frameworks (IR, code coverage, web analytics)
- Principled resolution methods exist (recipe-as-question-binding, sensitivity reporting, micro/macro/weighted framework)
- Recipe reversal is genuine (canonical per-iteration C2 FALSE vs per-task weighted C2 TRUE)
- Recipe choice is MATERIAL determinant of C-MEAS-VALID conclusion
- Canonical per-iteration p=0.5 recipe remains principled choice for C-MEAS-VALID

**Rejected**:
- Frozen SURVIVES_REVERSAL_PERSISTS decision rule (spec design failure, no MIXED branch)
- Parent stored values not precisely reproducible under corrected implementation
- F1 triggered (no principled methods exist) is ROBUSTLY NOT TRIGGERED

**Unknown**:
- Whether C2 FALSE and C2 TRUE reversal both hold on full-DOM enumeration
- Whether IR framework is OPTIMAL resolution framework
- Whether sensitivity reporting is sufficient
- Whether density metric has additional structure not captured by IR analogy
- Cross-site generalization
- Spec decision-rule amendment for MIXED outcomes

**Do Not Assume**:
- SPIDER-to-IR applicability mapping is established result (it is interpretive analogy)
- Non-systematic search captured all relevant prior art
- Web analytics case represents same class of concurrent recipe choice ambiguity
- FALSIFIED conclusion generalizes to full-DOM
- Per-iteration recipe is universally canonical
- Density metric is entirely useless
- Recipe choice is nuisance parameter
- C-MEAS-VALID status changed from this experiment
- Quantitative parent values are reliable

## 15. Dependencies

- **Substrate**: None (literature search only)
- **Data**: None (no new data collection)
- **Design**: None (design is this experiment)

## 16. Scope Limits

- This is a literature synthesis experiment; no new empirical measurement
- Claim ceiling is bounded to published literature in psychometrics, econometrics, and meta-analysis
- The SPIDER-to-field applicability mappings will be interpretive analogies, not established results
- This experiment does not resolve the empirical recipe choice at scale (requires full-DOM data)
