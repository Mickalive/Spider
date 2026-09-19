# EXP-INTEL-35445596324 — Report

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35445596324
- **Lane**: intel
- **Parent**: EXP-INTEL-35434771791 (MIXED verdict, C4 FAIL)
- **Claims**: C-MEAS-VALID

## Question

Is the OECD/COINr pipeline's ranking instability under recipe sampling (C4 FAIL in parent: canonical recipe 58%/48% agreement) a sample-size artifact of the truncated-first-20 locatable_sample, or is the instability structural?

## Verdict: MIXED

**C6 FAILS**: Canonical recipe ranking agreement for tag_entropy × DEF-FULL-MAP at effective_n=20 is 55.95%, below the 80% threshold. The ranking instability is **partially sample-size-dependent but not fully resolved** at the maximum available sample size.

## Decision Rule Evaluation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| C1: Raw features reproduce | **PASS** | All three features eta2=1.0, within-type std=0.0 |
| C2: Hierarchy anchor | **PASS** | eta2=0.0, all means 3.69e-07 |
| C3: Pipeline non-zero | **PASS** | Max eta2=0.999645 at n=20 |
| C4: Natural ranking preserved | **PASS** | tag_entropy preserves listing > detail for both definitions at n=20 |
| C5: Sample size effect | **PASS** | Spearman=1.0 (perfect monotonic), improvement=55.95pp |
| C6: Ranking stability at n=20 | **FAIL** | Agreement=55.95% < 80% threshold |

**Verdict**: C1 AND C2 AND C3 AND C4 AND C5 AND NOT C6 → MIXED (partial improvement, full-DOM testing still needed)

## Key Findings

### 1. Sample-Size Effect Is Real and Monotonic (C5 PASS)

The ranking agreement for tag_entropy × DEF-FULL-MAP under canonical recipe improves monotonically with effective sample size:

| Effective N | Agreement | eta2 |
|-------------|-----------|------|
| 5 | 0.0% | 0.485 |
| 10 | 0.0% | 0.736 |
| 15 | 49.98% | 0.829 |
| 20 | 55.95% | 0.921 |

Spearman correlation = 1.0 (perfect monotonic). The 55.95 percentage-point improvement from n=5 to n=20 far exceeds the 10pp threshold.

### 2. But Agreement Plateaus Below 80% (C6 FAIL)

At n=20 — the maximum available from the truncated-first-20 sample — canonical recipe ranking agreement is only 55.95%. The bootstrap 95% CI is approximately 7%-107% (57.1% ± 49.5%), indicating the ranking is **not a stable property** of this sample. This means:

- The ranking instability is NOT purely a sample-size artifact
- Recipe sampling (shared subset p=0.5) inherently destabilizes rankings even at the maximum available sample size
- Full DOM testing (n=21-82) is still needed for a definitive answer, but the n=20 result strongly suggests structural instability

### 3. Per-Task Recipe Outperforms Canonical Recipe

A striking finding: per-task recipe (independent p=0.5 per task) achieves **78.65%** ranking agreement at n=20, compared to canonical recipe's 55.95%. This is despite per-task recipe having much lower eta2 (0.37 vs 0.92):

| Recipe | Ranking Agreement (n=20) | eta2 (n=20) |
|--------|-------------------------|-------------|
| Canonical (shared subset) | 55.95% | 0.921 |
| Per-task (independent) | 78.65% | 0.366 |

This inverse relationship between eta2 and ranking agreement suggests that independent per-task sampling captures diverse discriminative elements that contribute to ranking stability, even though it degrades the overall between-type variance.

### 4. Non-Recipe Pipeline Ranking Also Depends on Sample Size

The non-recipe pipeline's ranking agreement for tag_entropy × DEF-FULL-MAP:

| Effective N | Ranking Agreement |
|-------------|-------------------|
| 5 | FALSE |
| 10 | FALSE |
| 15 | TRUE |
| 20 | TRUE |

This shows that even without recipe sampling, the pipeline requires ≥15 elements to preserve listing > detail ranking. The threshold is not linear — it appears to be a phase transition around n=15 where sufficient discriminative elements become available.

### 5. Bootstrap Variance Confirms Instability

At n=20, the bootstrap ranking agreement is 57.1% ± 49.5% (571/1000 bootstrap samples agree). The extremely high variance (std ≈ 50%) means the ranking is essentially random for individual bootstrap samples — it depends heavily on which tasks happen to be in the resample. This is the strongest evidence that the ranking instability is structural, not a sample-size artifact.

## Interpretation

The experiment resolves the parent's critical ambiguity (MIXED, C4 FAIL) as follows:

1. **The sample-size effect is real**: Ranking agreement improves monotonically from 0% to 56% as effective_n increases from 5 to 20. More elements per definition do help.

2. **But the improvement is insufficient**: At the maximum available sample size (n=20), canonical recipe agreement is only 56% — far below the 80% threshold. The bootstrap CI spans essentially 0%-100%, confirming the ranking is not reliably preserved.

3. **The recipe mechanism is the bottleneck**: The canonical recipe's shared subset strategy (p=0.5 applied uniformly) degrades both eta2 and ranking agreement. Per-task independent sampling preserves ranking better (79%) but degrades eta2 more (0.37).

4. **Full DOM testing is warranted but may not rescue**: The monotonic improvement suggests agreement could reach 80% at n>20, but the plateau from n=15 (50%) to n=20 (56%) — only 6pp improvement over the last quintile — suggests diminishing returns. The bootstrap variance at n=20 indicates the ranking is fundamentally unstable for this task set.

## Product Consequences

Per frozen spec.json:

- **C5 PASSES, C6 FAILS**: MIXED — partial improvement, full-DOM testing still needed
- **Product lane must use non-recipe density only** (which preserves ranking at 100% per parent B2, but with eta2 reduction)
- **Do not promote recipe-based density to Product Core**
- **Full DOM testing (n=21-82) is still warranted** as the final check, but the n=20 result strongly suggests the structural interpretation
- The 31x recipe material gap (EXP-INTEL-35264637598) remains relevant but recipe-based ranking is unstable

## Validity Threats

1. **Truncation ceiling**: Raw data contains only truncated-first-20 locatable elements. Full DOM (n=21-82) not tested. The n=20 result is the maximum from this dataset.

2. **First-n subsampling**: Uses first n elements by DOM position, not random subsampling. This preserves DOM-sequential structure but may not represent random element subsets.

3. **Small task set**: Only 3 tasks per type (listing, detail), 1 cart. Bootstrap CI is extremely wide (±50%). More tasks would provide more reliable agreement estimates.

4. **Cart n=1 degeneracy**: Within-type variance for cart is degenerate. Comparison focuses on listing vs detail.

5. **Template invariance**: Within-type template identity makes eta2 trivially high. The test is ranking preservation, which is the appropriate discriminating measure.

6. **Single Magento site**: Cross-site generalization not tested.
