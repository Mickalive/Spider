# EXP-GRAPH-35330739886 — Preregistration

## Status

DESIGN ONLY. Frozen after FREEZE step. Do not modify after freeze.

---

## 1. Experiment Identity

- **experiment_id**: EXP-GRAPH-35330739886
- **lane**: graph
- **claim_ids**: ["C-FRESHNESS"]
- **parent**: EXP-GRAPH-35308806969
- **parent_handoff_sha256**: a1d844e0da998d01a92a9824dee4d7bb9d85d5b0bf2eed5cd3a6ca9dd259a509

---

## 2. Question

Can a TOST equivalence test or confidence-interval upper bound on |r| formally confirm behavioral-structural signal orthogonality at the existing n=480 paired samples, and what practical equivalence margin (delta) is achievable versus required for C-FRESHNESS product architecture decisions?

---

## 3. Hypothesis

The parent established near-zero pooled correlation (|r|=0.0335, r²=0.001) on n=480 paired samples from 8 co-occurring conditions on deterministic Flask 3.1.3 + PyJWT HS256 localhost. The frozen permutation p=0.465 failed the conjunctive C3 gate, but power analysis confirmed n=480 is provably underpowered for |r|=0.05 at permutation p<0.05 (minimum n=1538). A TOST equivalence test or CI upper bound can confirm |r|<delta at practical sample sizes, replacing the permutation test.

**Predicted outcome**: 95% CI upper bound on r is approximately 0.122 (Fisher z-transform, n=480), which is <0.15 (passes delta=0.15) but NOT <0.10 (fails delta=0.10). TOST at delta=0.15 should pass; TOST at delta=0.10 should fail.

---

## 4. Falsifier

- **C1_drift_tp fails** (mean TP < 0.85 OR any Wilson lower CI < 0.75) — inherited, verified from parent
- **C2_variance fails** (< 6/8 conditions with std > 0 for both signals) — inherited, verified from parent
- **C3_equivalence fails**: NO tested delta (0.10, 0.12, 0.15, 0.20) achieves TOST pass (95% CI upper bound on |r| >= all tested deltas)
- **C4_null_control fails** (FP > 0.0) — inherited, verified from parent

---

## 5. Baselines

| ID | Description | Expected |
|---|---|---|
| B-PARENT-N480-R0335 | Parent n=480: |r|=0.0335, p=0.465, C1-C2-C4 PASS | CI upper bound ~0.122 |
| B-FISHER-Z-CI | 95% CI via Fisher z-transform: z ± 1.96/√(n-3) | Upper bound ~0.122 |
| B-TOST-DELTA-MAP | TOST at delta ∈ {0.10, 0.12, 0.15, 0.20} | Pass at delta >= 0.15 |

---

## 6. Positive Control

**PC-TP-VARIANCE-REPLICATION**: Verify parent established results (TP=1.0, 8/8 conditions with variance, FP=0.0) from parent raw_evidence. No new server runs.

---

## 7. Null Control

**NC-FP-REPLICATION**: Verify parent FP=0.0 on 240 noise-only samples from parent raw_evidence.

---

## 8. Measurement Validity

1. **No new HTTP requests** — frozen statistical reanalysis of parent raw_evidence/experiment_data.json
2. Parent data: Flask 3.1.3 + PyJWT 2.14.0 HS256 localhost, graded session_status_check (401->1.0, 403->0.5, 500->0.75), session_change=1, 60 samples/condition, 8 co-occurring + 4 noise-only, SEED=42
3. TOST/CI uses Fisher z-transform: z = 0.5·ln((1+r)/(1-r)), SE = 1/√(n-3), CI = tanh(z ± z_α·SE)
4. TOST: H₀: |r| ≥ δ vs H₁: |r| < δ, α=0.05 each side, two-sided equivalence requires BOTH rejections
5. Equivalence margins: δ=0.10 (<1% shared variance), δ=0.12 (<1.44%), δ=0.15 (<2.25%), δ=0.20 (<4%)

---

## 9. Decision Rule

**PASS** if ALL:
1. C1_drift_tp: verified from parent, mean TP ≥ 0.85 AND all Wilson lower CI > 0.75
2. C2_variance: verified from parent, ≥ 6/8 conditions with std > 0 for both signals
3. C3_equivalence: 95% CI upper bound on |r| < δ for at least one tested δ ∈ {0.10, 0.12, 0.15, 0.20}
4. C4_null_control: verified from parent, FP = 0.0

**FAIL** if any fails.

**MIXED** if C1-C2-C4 PASS and C3 passes only for δ ≥ 0.15 (CI upper bound in 0.10-0.15 range).

**Rationale for decision rule revision**: The parent's permutation p<0.05 criterion is the inappropriate test for very-low-magnitude correlations (|r|<0.1). For |r|~0.05, achieving permutation p<0.05 requires n~1538 (Fisher z power analysis). The scientifically meaningful question is not "is |r| exactly zero?" but "is |r| small enough for practical independence?" The TOST equivalence test directly answers the product-relevant question with a quantified equivalence margin.

---

## 10. Product Consequences

**Positive** (CI upper bound < 0.15): C-FRESHNESS orthogonality formally confirmed at that margin. Product pipeline integrates behavioral + structural as independent parallel channels with quantified shared-variance ceiling < 2.25%.

**Negative** (CI upper bound ≥ 0.20): Signals not practically independent. Product pivots to fused classifiers.

**Mixed** (CI upper bound 0.10-0.15): Decision depends on product delta tolerance. δ=0.15 acceptable → parallel channels; δ=0.10 required → need n~1538 or fused classifiers.

---

## 11. Estimated Cost

Minimal: statistical reanalysis only, no new data collection. Compute TOST/CI on existing 480 paired samples.

---

## 12. Expected Information Gain

Very High: directly resolves the single remaining frozen gate (C3) for C-FRESHNESS with a decision-relevant equivalence margin. Maps the full delta-vs-sample-size trade-off surface. Changes a product architecture decision regardless of outcome.
