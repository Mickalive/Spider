# Preregistration: EXP-INTEL-35551517470

## Bounded Saturating Function Extrapolation of Ranking Agreement

**Experiment ID**: EXP-INTEL-35551517470  
**Lane**: Intel  
**Date**: 2026-09-21  
**Status**: DESIGN (pre-freeze)

---

## 1. Background and Rationale

### 1.1 Parent Chain Summary

The Intel lane has been investigating whether recipe-based density sampling can achieve stable task-type ranking for the MIXED program. Five consecutive model-based extrapolation approaches have failed:

1. **Phi(mean(SNR_i))** with within-iteration SE — REJECTED at C1 (40-50pp residual)
2. **Phi(mean/std)** using margin_std — REJECTED at C1 (17.8pp at n=20)
3. **Phi(median/std)** — REJECTED at C1 (34.59pp at n=15, 18.96pp at n=20)
4. **Saturating sign-fraction power law** — REJECTED at C1/C2 (12.39pp at n=15, R2=0.8797)
5. **Empirical CDF linear extrapolation** — REJECTED at C3 (F(82)=1.3813 >1.0 impossible)

The common root cause is step-function structure in proportion(margin>0): `(0, 0, 0.50, 0.57)` at n=5/10/15/20 with 7.6x growth deceleration (plateau/jump ratio 0.132).

### 1.2 Current State

- **Established**: Sample-size effect on ranking agreement is real and monotonic (0% → 50% → 56% from n=5/10/15/20)
- **Established**: Ranking agreement plateaus below 80% at maximum available sample size (56.5% at n=20)
- **Established**: Template invariance makes ranking agreement = proportion(margin>0) exactly
- **Unknown**: Whether ranking stabilizes at full DOM (n=21-82)
- **Blocked**: Docker image am1n3e/webarena-verified-shopping:latest unavailable for direct full-DOM measurement

### 1.3 Why This Experiment

This is the FINAL model-based attempt before Docker pivot. A bounded saturating function (logistic, Hill, Richards) has correct asymptotic properties:
- Bounded [0,1] — cannot produce physically impossible predictions
- Monotonic — consistent with observed trend
- Saturating — captures the 7.6x growth deceleration

If this class of functions also fails, the model-based extrapolation path is definitively closed after six consecutive failures.

---

## 2. Hypotheses

### H1: Fit Quality
At least one saturating function achieves R² ≥ 0.95 and maximum residual < 5pp at training points.

### H2: Physical Extrapolation
The fitted function predicts F(50) < 0.80 (consistent with plateau hypothesis).

### H3: Improvement Over Parent
The fitted function improves over the parent's best model (sign-fraction power law, R²=0.8797) by ≥ 0.05 in R².

---

## 3. Data

### 3.1 Training Data
- **Source**: EXP-INTEL-35476271877/snr_per_iteration_tag_entropy.json.gz (sha256 ce3dda6e021137ef0c911c19d8897c24f26342e8bd6da77242e1a026e08c1b7a)
- **Derived**: EXP-INTEL-35476271877/analysis_output_snr.json (sha256 f7f6986753774125966be2654a30744de386e2ab93790b02ec84d035ff1358b2)
- **Definition**: tag_entropy × DEF-FULL-MAP canonical recipe
- **Training points**: n=[5, 10, 15, 20], F(n)=[0.0, 0.0, 0.4996, 0.5654]
- **N iterations**: 10,000 per n (with cart n=1 excluded per parent protocol)

### 3.2 Template Invariance
Under template invariance (verified in parent chain), ranking agreement = proportion(margin_i > 0) exactly. The empirical CDF mapping is the true data-generating process at training points.

---

## 4. Candidate Function Families

### 4.1 Logistic
```
F(n) = L / (1 + exp(-k * (n - n0)))
```
Parameters: L (asymptote, bounded [0,1]), k (steepness), n0 (midpoint)

### 4.2 Hill
```
F(n) = L * n^h / (K^h + n^h)
```
Parameters: L (asymptote, bounded [0,1]), h (Hill coefficient), K (half-max)

### 4.3 Richards
```
F(n) = L / (1 + (n/n0)^a)^(1/v)
```
Parameters: L (asymptote, bounded [0,1]), n0 (scale), a (shape), v (asymmetry)

All functions are bounded to [0,1] by construction through parameter constraints.

---

## 5. Analysis Protocol

### 5.1 Fitting
- Use `scipy.optimize.curve_fit` with bounds
- L ∈ [0, 1], all other parameters > 0
- N=10 random restarts per function family (different initial conditions)
- Select best fit by R² (primary) and AIC/BIC (secondary)

### 5.2 Metrics
- **R²**: Coefficient of determination on training points
- **Max residual**: Maximum absolute residual at any training point
- **AIC**: Akaike Information Criterion (2k - 2ln(L))
- **BIC**: Bayesian Information Criterion (k*ln(n) - 2ln(L))
- **F(50)**: Predicted agreement at n=50 (full-DOM)
- **F(82)**: Predicted agreement at n=82 (maximum full-DOM)

### 5.3 Baseline Comparison
- Parent's best model: sign-fraction power law, R²=0.8797, max residual 12.39pp
- Linear null: F(n) = 0.5654 for all n

---

## 6. Decision Rules

### C1: Best Fit Quality
At least one saturating function achieves R² ≥ 0.90 AND maximum absolute residual < 10pp at all 4 training points.

### C2: Physical Extrapolation
All saturating functions that achieve R² ≥ 0.90 predict F(50) ∈ [0.0, 1.0] AND F(82) ∈ [0.0, 1.0].

### C3: Improves Over Parent
The best saturating function achieves R² > 0.93 (improving over parent's 0.8797 by ≥ 0.05) OR maximum residual < 8pp (improving over parent's 12.39pp).

### Verdict Rules
- **NOT C1** → FALSIFIES: Step-function structure incompatible with smooth bounded forms. Model-based path definitively closed.
- **C1 AND NOT C2** → MEASUREMENT_INVALID: Fit quality adequate but extrapolation physically implausible.
- **C1 AND C2 AND NOT C3** → MIXED: Adequate fit but no improvement over rejected parent model.
- **C1 AND C2 AND C3** → SURVIVES: Validated extrapolation improves over all prior models.

---

## 7. Positive Control

**PC1_FIT_REPRODUCES_TRAINING**: Best-fit function reproduces observed ranking agreement at all training points within 5pp. Expected: trivially PASS for any reasonable fit.

---

## 8. Null Control

**NC1_PARENT_BEST_MODEL**: Saturating function must improve over parent's best model (R²=0.8797, max residual 12.39pp). If no function achieves R² > 0.93 or max residual < 8pp, no new information gained.

---

## 9. Validity Threats

1. **Overfitting**: With 4 data points and 2-3 parameters per function, overfitting is almost guaranteed. R² thresholds are set high (0.90) to account for this.
2. **Step-function incompatibility**: Smooth functions cannot perfectly capture the 0→0.50 jump. The fit will be approximate, and residuals at n=10 and n=15 may be large.
3. **Extrapolation uncertainty**: With only 4 training points, extrapolation to n=50/82 is highly uncertain even for the best-fitting function.
4. **Local minima**: Multiple random restarts (N=10) mitigate but do not eliminate local minima risk.
5. **Parameter degeneracy**: Some function families may have degenerate parameter combinations for this sparse data.

---

## 10. Consequences

### Positive Outcome (C1 AND C2 AND C3)
- A validated bounded extrapolation exists
- Product decision on Docker re-collection can be made from the extrapolation
- If F(50) < 0.80: plateau is structural, recipe density limited, use non-recipe density
- If F(50) >= 0.80: plateau breaks at full DOM, Docker re-collection justified

### Negative Outcome (NOT C1)
- Model-based extrapolation path definitively closed after six consecutive failures
- Docker-based direct full-DOM measurement is the ONLY remaining path
- Product lane should NOT invest in recipe density design until Docker data available
- The step-function structure (0,0,0.50,0.57) is a genuine threshold phenomenon, not a smooth saturation

---

## 11. Frozen Inputs

- `snr_per_iteration_tag_entropy.json.gz`: sha256 ce3dda6e021137ef0c911c19d8897c24f26342e8bd6da77242e1a026e08c1b7a
- `analysis_output_snr.json`: sha256 f7f6986753774125966be2654a30744de386e2ab93790b02ec84d035ff1358b2

---

## 12. Estimated Cost

- Compute: <60 seconds (fitting 3 functions × 10 restarts each)
- LLM tokens: <1000 (analysis code)
- Data collection: NONE (existing data only)
- Browser/network: NONE

---

## 13. Expected Information Gain

HIGH — this is the FINAL model-based attempt before Docker pivot. Either outcome definitively resolves the model-based extrapolation question:
- Positive: validated extrapolation enables concrete product decision
- Negative: definitively closes model-based path, justifies Docker investment
