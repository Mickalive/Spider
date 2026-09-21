# EXP-FRONTIER-35401996615 — Executive Report

## Experiment Summary

**Question**: Does per-type CV stability (<=0.5 at lambda=1) achieve at larger per-type n (500 and 1000/type) with KDE Scott or kNN k=5 under spec-compliant measurement?

**Decision**: MEASUREMENT_INVALID — Multiple frozen decision_rule triggers fire. No valid inference about per-type CV stability at larger sample sizes is possible from this experiment.

## Key Results

| Metric | n=250/type | n=500/type | n=1000/type |
|--------|-----------|-----------|------------|
| KDE CV max (lambda=1) | 0.350 | 0.296 | 0.270 |
| kNN CV max (lambda=1) | 0.058 | 0.062 | 0.056 |
| KDE null control | 6/8 | 7/8 | 7/8 |
| kNN null control | 7/8 | 6/8 | 8/8 |
| KDE positive control | p=0.074 | p=0.816 | p=0.002 |
| kNN positive control | p=0.475 | p=0.909 | p=0.288 |

## MEASUREMENT_INVALID Triggers

Three independent frozen decision_rule triggers fire:

1. **Pipeline validation at 250/type FAILS**: KDE CV max=0.350 (expected 0.546-0.604, 38% below range); kNN CV max=0.058 (expected 0.717-0.793, 92% below range). The DGP implementation produces qualitatively different divergence magnitudes from the parent.

2. **kNN positive control fails at ALL sample sizes**: Pooled kNN MI at lambda=1 is indistinguishable from lambda=0 (p>0.28 at all n). The kNN Kraskov estimator is not detecting lambda-dependent action conditioning.

3. **KDE null control never achieves 8/8 pass**: At lambda=0, KDE produces non-zero divergence for 1-2 types at every sample size, indicating the KDE estimator has residual bias at lambda=0.

## Root Cause Analysis

The primary failure is a **DGP implementation mismatch** with parent EXP-FRONTIER-34913743596:

- **Divergence magnitudes are ~10x smaller**: Parent KDE max at lambda=1 ~0.18; this experiment ~0.05. Parent kNN max at lambda=1 ~0.14; this experiment ~1.3 (but note: kNN units differ).

- **kNN MI values are near-constant**: kNN CV max=0.058 (13x smaller than parent 0.755), indicating the estimator returns nearly identical values regardless of lambda, sample size, or page type. The Kraskov estimator implementation likely differs from the parent.

- **Null control residuals**: At lambda=0, some page types show non-zero KDE divergence, suggesting the DGP has residual action-dependent structure even at lambda=0 (despite the lambda-scaling fix).

## What This Experiment Does NOT Establish

- Whether per-type CV stability <=0.5 achieves at 500-1000/type (UNTESTED due to measurement invalidity)
- Whether KDE or kNN can detect lambda-dependent structure at larger sample sizes
- Any claim about C-WEB-DYNAMICS (all evidence remains synthetic)

## Required Next Steps

1. **Recover parent DGP parameters**: Reverse-engineer the exact DGP implementation from parent EXP-FRONTIER-34913743596 result.json metrics (KDE CV max=0.5745, kNN CV max=0.7550 at 250/type) before re-running.

2. **Validate kNN implementation**: The Kraskov MI estimator must produce values consistent with the parent before sample-size scaling can be tested. The 13x CV discrepancy indicates a fundamental implementation difference.

3. **Fix null control residuals**: Investigate why KDE produces non-zero divergence at lambda=0 for some page types.

## Frozen Decision Rule Evaluation

Per the frozen decision_rule:
- **SURVIVES_CURRENT_TEST**: Requires CV <=0.5 for all 8 types AND null control 8/8 AND positive control pass AND pipeline validation pass. **NOT MET** (pipeline fails, positive control fails for kNN, null control fails for KDE).
- **FALSIFIED-IN-SETTING**: Requires CV >0.5 for any type at BOTH KDE and kNN at n=1000 AND null+positive pass. **NOT MET** (CV passes for both at 1000, but controls fail).
- **MEASUREMENT_INVALID**: Pipeline validation fails OR positive control fails for either measure. **TRIGGERED**.

**Final decision: MEASUREMENT_INVALID**
