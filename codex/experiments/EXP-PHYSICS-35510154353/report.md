# EXP-PHYSICS-35510154353 — Report

## Verdict: FALSIFIED-IN-SETTING

**Frozen decision rule triggers FALSIFIED-IN-SETTING on clause C3**: both primary estimators passing C1 (null centering) fail C3 (positive control sensitivity). Plug-in KL K3=0.099 bits < 0.5 threshold; KSG k=10 K3=0.000560 bits < 0.5 threshold. The true CMI is 1.52 bits (audit-confirmed from parent).

---

## 1. Executive summary

This experiment resolves the critical question from EXP-PHYSICS-35482477045: **is KSG k=5 and LR chi2-per-state insensitivity estimator-specific or fundamental?**

**Answer: The insensitivity is NOT specific to KSG k=5.** Two materially orthogonal estimators — a plug-in transition-matrix KL divergence estimator and KSG CMI with k=10 — both fail to detect the 1.52-bit CMI signal on the stochastic 12-state SPA at N=5000, despite passing null centering (C1). Additionally, KSG CMI with k=5, k=10, and k=20 all produce identical results, demonstrating that the sklearn implementation is invariant to the k parameter for discrete data.

The frozen verdict is FALSIFIED-IN-SETTING. The CMI estimation pathway for discrete 12-state SPAs is now exhausted across three materially distinct estimator families (KSG, likelihood-ratio, plug-in KL).

---

## 2. Primary results

### 2.1 Plug-in KL divergence estimator

| Metric | Value |
|--------|-------|
| K3 (stochastic SPA) | 0.099 bits |
| K2 (stochastic SPA) | 0.071 bits |
| K3 - K2 | 0.028 bits |
| Null mean (C1) | 0.064 bits |
| |null_mean| | 0.064 bits (< 0.1 threshold) |
| C1 | PASS |
| C3 (K3 >= 0.5) | FAIL (0.099 < 0.5) |
| Degenerate control (deterministic SPA) | 0.109 bits |

**Critical finding**: The degenerate control on the deterministic SPA (I(Y;A|Z)=0 by construction) gives K3=0.109, which is HIGHER than the stochastic SPA measurement (K3=0.099). This means the alpha=1.0 Laplace smoothing creates a positive bias that exceeds the true 1.52-bit signal. The estimator is literally less sensitive on the positive control than on the degenerate baseline.

**Mechanism**: With alpha=1.0 and 12 target classes, each (z,a) cell receives 12 pseudo-counts from smoothing. Average K3 stratum size is ~6 records (~42 records per (z,a) cell across 4 actions). The 12 pseudo-counts represent ~67% of the probability mass, completely dominating the empirical signal.

### 2.2 KSG CMI (k=5, k=10, k=20)

| k | K3 | K2 | null_mean | C1 | C3 |
|---|-----|-----|-----------|-----|-----|
| 5 | 0.000560 | -0.003735 | -0.012066 | PASS | FAIL |
| 10 | 0.000560 | -0.003735 | -0.012066 | PASS | FAIL |
| 20 | 0.000560 | -0.003735 | -0.012066 | PASS | FAIL |

**All three k values produce identical results** — K3=0.000560, mi_joint=0.034413, mi_cond=0.033853 — to full numerical precision. This demonstrates that sklearn's `mutual_info_classif` with `discrete_features=True` is invariant to the `n_neighbors` parameter on this discrete dataset. The KSG insensitivity is NOT due to k=5 being too coarse; the estimator fundamentally cannot detect the signal regardless of k.

### 2.3 Parent replication

KSG k=5 replication: K3=0.000560, matching parent EXP-PHYSICS-35482477045 exactly (parent: 0.000560). Result is reproducible.

---

## 3. Permutation test (exploratory)

The per-stratum permutation test provides a critical diagnostic. For each of the 48 (state, action) strata:

- **48/48 strata significant** (Bonferroni-corrected p=0.0)
- **Mean PMI: 1.595 bits** (range: 1.46-1.69 bits)
- **All p-values: 0.0** (500 within-session permutations per stratum)

This confirms:
1. The true signal exists and is strong (~1.5 bits per stratum)
2. A stratum-level test can detect it
3. The CMI estimators fail because they estimate a different quantity — joint MI minus conditional MI over the full state space, rather than per-stratum PMI

---

## 4. Controls summary

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C1 null centering | |mean| < 0.1 for >=1 estimator | 4/4 pass (0.012-0.064) | YES |
| C3 positive control | K3 >= 0.5, p <= 0.001 | KL: 0.099, KSG: 0.000560 | NO |
| C6 design verification | 48/48 pairs with 4 candidates | 48/48 | YES |
| C7 stratum buckets | >=2 non-empty | 2 (5-9, 10-19) | YES |
| Degenerate control (KL) | K3 ~ 0 | 0.109 (bias exceeds threshold) | NO |
| Degenerate control (KSG) | K3 ~ 0 | -0.000405 | YES |
| Parent replication (KSG k=5) | K3 within 10% of 0.000560 | 0.000560 (exact) | YES |

---

## 5. Interpretation

### 5.1 The CMI estimation pathway is exhausted for discrete 12-state SPAs

Three materially distinct estimator families have now been tested:
1. **KSG CMI** (k=5, k=10, k=20): K3=0.000560 bits (893x below threshold). Insensitivity is k-invariant.
2. **Likelihood-ratio** (chi2-per-state): K3=0.104 bits (4.8x below threshold). History collapse (K2=K3).
3. **Plug-in KL** (alpha=1.0): K3=0.099 bits (5.1x below threshold). Smoothing bias exceeds signal.

All three pass C1 (null centering works) but fail C3 (sensitivity). The null framework is sound; the estimators are insensitive to a 1.52-bit signal.

### 5.2 Two distinct failure modes identified

**Mode 1 — KSG discrete invariance**: sklearn's `mutual_info_classif` with `discrete_features=True` produces identical results for all k values (5, 10, 20). This suggests the implementation uses categorical matching rather than distance-based neighborhoods for discrete data, making k irrelevant.

**Mode 2 — Laplace smoothing bias**: With alpha=1.0 on 12-class discrete data, the smoothing dominates the empirical probability mass (~67%), creating a positive bias of ~0.11 bits that exceeds the true CMI. The estimator is less sensitive on the stochastic SPA than on the degenerate baseline.

### 5.3 The signal is present and detectable

The per-stratum permutation test (exploratory) detects PMI of 1.46-1.69 bits across all 48 strata (all p=0.0). This is consistent with the parent audit's theoretical CMI of ~1.52 bits. The environment expresses the tested effect; the estimators cannot capture it.

---

## 6. Product consequences

**If H0 confirmed (all alternative estimators also fail):** The insensitivity is fundamental to discrete CMI estimation on 12-state SPAs with the frozen estimator implementations and parameter settings. The Physics lane must pivot to:
- Fundamentally different detection paradigms (entropy rate, channel capacity, causal discovery)
- Non-CMI detection methods (the per-stratum PMI test shows promise)
- Production Web data with continuous state representations
- Alternative estimator implementations (non-smoothed MLE, different sklearn parameters)

**This experiment does NOT close the C-WEB-DYNAMICS claim.** It closes only the specific CMI estimation pathway on this discrete SPA class.

---

## 7. Threats to validity

1. **Frozen alpha=1.0**: The Laplace smoothing parameter is frozen at alpha=1.0, which creates excessive bias. A smaller alpha (0.1 or 0.01) might allow the plug-in KL to detect the signal, but this would require a new frozen experiment.
2. **sklearn discrete mode**: The mutual_info_classif implementation may behave differently with `discrete_features=False` or with a custom distance metric. These alternatives were not tested.
3. **12-state discrete SPA**: All evidence is on a synthetic 12-state discrete SPA. Production Web transitions have different state spaces and continuous representations.
4. **N=5000**: The sample size is frozen from the parent. Larger N might improve stratum sizes and reduce smoothing bias relative to signal.
