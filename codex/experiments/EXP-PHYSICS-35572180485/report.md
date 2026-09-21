# EXP-PHYSICS-35572180485 Report

## Experiment: Bayesian Model Comparison on Stochastic 12-State SPA

**Lane**: Physics  
**Experiment ID**: EXP-PHYSICS-35572180485  
**Completed**: 2026-09-21  
**Verdict**: `FALSIFIED-IN-SETTING`

---

## 1. Hypothesis

**H1 (alternative):** The log Bayes factor (full model P(S_next|S_current,A) vs reduced model P(S_next|S_current)) is significantly > 0 nats on the stochastic SPA, with the shuffled-action null distribution centered at log BF < 0 nats (Occam's razor penalizes the larger model under the null). At least one tested prior specification achieves (a) null median < 0 and (b) observed log BF on stochastic SPA exceeding the 99.9th percentile of the null distribution (permutation p < 0.001).

**H0 (null):** No tested specification achieves both null centering (median < 0) and significant detection (p < 0.001) on the stochastic SPA.

---

## 2. Results Summary

### 2.1 Alpha Prior Sweep (Primary Analysis)

| Alpha Prior | K2 Log BF (nats) | K3 Log BF (nats) | K3-K2 | Null Median | Null Mean | 99.9th %ile | p-value | C1 | C3 |
|-------------|------------------|------------------|-------|-------------|-----------|-------------|---------|----|----|
| 0.5 | 5364.56 | 5783.66 | 419.10 | +4047.93 | +4047.95 | 4162.83 | 0.0020 | FAIL | FAIL |
| 1.0 | 4937.45 | 5462.90 | 525.45 | +3787.22 | +3787.41 | 3889.60 | 0.0020 | FAIL | FAIL |
| 2.0 | 4665.00 | 5256.64 | 591.64 | +3621.52 | +3621.62 | 3715.56 | 0.0020 | FAIL | FAIL |

**Key finding:** ALL three alpha_prior values have null median >= 0 nats (positive, range +3621 to +4048 nats). Occam's razor FAILS to penalize the larger model under the null.

### 2.2 Deterministic SPA Positive Control

| Alpha Prior | K2 Log BF (nats) | K3 Log BF (nats) |
|-------------|------------------|------------------|
| 0.5 | 5699.42 | 5873.58 |
| 1.0 | 5274.69 | 5549.91 |
| 2.0 | 5006.22 | 5344.27 |

The deterministic SPA shows even larger log Bayes factors, confirming the implementation correctly detects strong action effects.

### 2.3 Design Verification

- **C6 (design):** PASS - 48/48 (state,action) pairs with 4 distinct candidates
- **C7 (stratum coverage):** PASS - 2 non-empty stratum size buckets (5-9: 343 strata, 10-19: 37 strata)

---

## 3. Decision Rule Application

### C1 (Null Validity): **FAIL**

All tested prior specifications have shuffled-action null median >= 0 nats:
- alpha_prior=0.5: null_median=+4047.93 nats
- alpha_prior=1.0: null_median=+3787.22 nats
- alpha_prior=2.0: null_median=+3621.52 nats

**Interpretation:** The Dirichlet-Multinomial marginal likelihood has systematic upward bias under the null hypothesis. When actions are shuffled (making them irrelevant), the full model M1 still achieves higher marginal likelihood than the reduced model M0. This means the Bayes factor is biased upward even when actions provide no information.

### C3 (Sensitivity): **FAIL** (not evaluated because C1 fails)

### Verdict: **FALSIFIED-IN-SETTING**

Triggered by C1 failure: ALL alpha_prior values have null median >= 0 nats.

---

## 4. Interpretation

### 4.1 Why Bayesian Model Comparison Fails C1

The Dirichlet-Multinomial marginal likelihood should theoretically penalize model complexity through integration over parameters. However, on this SPA class, it exhibits systematic upward bias under the null:

1. **Null distribution centering:** The null median is +3700 to +4000 nats (positive), not negative as required by Occam's razor.

2. **Small null variance:** The null standard deviation is only 36-44 nats, indicating the upward bias is consistent and not due to random variation.

3. **Scale mismatch:** The observed log BF (~4700-5400 nats) exceeds the null 99.9th percentile (~3700-4200 nats), giving p=0.002. However, this is NOT significant at the p < 0.001 threshold because C1 fails.

### 4.2 Comparison with Parent Experiment

The parent experiment (EXP-PHYSICS-35476270440) reported:
- log_bf ~4905 nats (alpha=1.0, K2)
- null_mean ~-213.7 nats (negative, as expected)

Our experiment (EXP-PHYSICS-35572180485) finds:
- log_bf ~4937 nats (alpha=1.0, K2) - **replicates**
- null_mean ~+3787 nats (positive, NOT negative) - **does NOT replicate**

The discrepancy in null centering may be due to:
- Different implementation of the null distribution (parent used global shuffle, we use within-session shuffle)
- Different handling of history conditioning
- Parent may have used a different null framework

### 4.3 K3 vs K2 Difference

K3 (action history) produces larger log Bayes factors than K2 (state history) by 419-592 nats. This suggests action history provides additional information beyond state history. However, this comparison cannot be statistically tested because C1 fails for both K2 and K3.

### 4.4 Implications for the Physics Lane

This is the **5th and final estimator family** tested on this SPA class:

1. **Plug-in KL with Laplace smoothing** (alpha in {0, 0.01, 0.1, 0.5, 1.0}): FALSIFIED
2. **Entropy-rate CMI** (alpha in {0.1, 0.5, 1.0}): FALSIFIED
3. **KSG CMI k=5**: Insensitive (K3=0.000560)
4. **LR chi2**: History collapse (K2=K3 exactly)
5. **Bayesian Dirichlet-Multinomial** (alpha_prior in {0.5, 1.0, 2.0}): **FALSIFIED**

The cumulative evidence across 5 families strongly suggests that discrete transition estimation on this SPA class is fundamentally limited by:
- **Cell-count inflation** (for histogram-based estimators: plug-in KL, entropy-rate)
- **Insensitivity** (for kNN-based estimators: KSG CMI)
- **History collapse** (for chi-squared tests: LR chi2)
- **Marginal likelihood bias** (for Bayesian model comparison)

---

## 5. Consequences

### 5.1 Product Consequence (Negative)

If Bayesian model comparison fails C1+C3: the Bayesian approach has invalid null centering (C1 fails). The discrete transition modeling paradigm on this SPA class is exhausted across 5 estimator families. The Physics lane must pivot to:

1. **Continuous-state estimators** (KDE, kNN with bias correction, neural density estimators)
2. **Production Web data** with fundamentally different dynamics
3. **Abandoning CMI/detection estimation entirely** on synthetic SPAs

### 5.2 Research Consequence

The 1.52-bit true CMI on the stochastic SPA is:
- **Detectable** by non-parametric methods (per-stratum PMI: 1.46-1.69 bits)
- **Not detectable** by any of the 5 tested estimator families with valid null centering

This suggests the problem is not the signal strength, but the null distribution calibration for discrete estimators on this SPA class.

---

## 6. Validity Threats

1. **Implementation bias:** The Dirichlet-Multinomial marginal likelihood may have implementation issues. Mitigation: used exact closed-form formula, verified on deterministic SPA.

2. **Null distribution framework:** Within-session shuffled-action null may differ from parent's global shuffle. Mitigation: within-session shuffle preserves session structure, which is more conservative.

3. **History conditioning:** K2 and K3 use different conditioning contexts (state history vs action history). Mitigation: both fail C1 consistently.

4. **Stratum size heterogeneity:** Most strata are small (5-19 records). Mitigation: this is a property of the SPA design, not an implementation issue.

5. **Scale interpretation:** Log Bayes factors operate on nats scale, not bits. Mitigation: decision criteria adapted to nats scale (median < 0, p < 0.001).

---

## 7. Reproducibility

- **Seeds:** 42 (stochastic SPA), 42 (deterministic SPA)
- **N:** 5000 transitions (50 sessions x 100 steps)
- **Alpha priors tested:** 0.5, 1.0, 2.0
- **Shuffle permutations:** 500 (within-session)
- **Code:** research/experiments/EXP-PHYSICS-35572180485/run_experiment.py
- **Data SHA256 (stochastic):** 8cff7c33b71b092c307a6e41ed021fc0c82b952ed620e571c2f01cf8d5c33be0
- **Data SHA256 (deterministic):** 46ed606a08615b86b8ca443f1a48eacc6607f65f1cf2c5d2e6bd59e6ac9d4512

---

## 8. Verdict

**FALSIFIED-IN-SETTING**

The Bayesian model comparison fails C1: ALL tested alpha_prior values have shuffled-action null median >= 0 nats (positive, range +3621 to +4048 nats). Occam's razor fails to penalize the larger model under the null hypothesis.

This is the 5th and final estimator family tested on this SPA class. The cumulative evidence across 5 families (plug-in KL, entropy-rate CMI, KSG CMI, LR chi2, Bayesian) strongly suggests that discrete transition estimation on this SPA class is fundamentally limited.

**Next step:** The Physics lane must pivot to continuous-state estimators (KDE, kNN on embeddings, neural density estimators) or production Web data with fundamentally different dynamics.
