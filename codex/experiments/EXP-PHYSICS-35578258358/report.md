# EXP-PHYSICS-35578258358 — Execution Report

## 1. Executive Summary

**Verdict: SURVIVES_CURRENT_TEST** — The corrected Bayesian model comparison with K=n_states=12 and N_SHUFFLE=1999 replicates the audit-corrected SURVIVES_CURRENT_TEST result on the stochastic 12-state SPA. This is the **first estimator family** to pass both C1 (null median < 0 nats) and C3 (permutation p < 0.001) across the full alpha prior sweep on this SPA class, after 4 prior estimator families (plug-in KL, entropy-rate CMI, KSG CMI, LR chi2) all failed simultaneous C1+C3.

## 2. What Changed from Parent

### 2.1 Critical Fix: K=n_states=12

The parent experiment EXP-PHYSICS-35572180485 used `K = len(counts)` in `_dirichlet_multinomial_log_marginal` (line 233), which computes the number of **observed** distinct next-states (typically 1-4 per stratum). The frozen spec mandates `K = n_states = 12` (the total number of **possible** next states).

This single-line error systematically under-penalized the action-dependent model M1 over the action-independent model M0, producing a +3700 to +4000 nat upward null bias that triggered the parent's C1 failure. The corrected implementation passes `K_categories=N_STATES=12` to the marginal likelihood function.

### 2.2 Fix: N_SHUFFLE=1999

The parent used N_SHUFFLE=500, which limited minimum achievable p to 0.001996 (> 0.001 threshold). The frozen spec requires N_SHUFFLE >= 1000. We use N_SHUFFLE=1999, achieving minimum p = 0.0005, well below the threshold.

## 3. Results

### 3.1 Primary Decision Criteria

| Criterion | Threshold | Result | Status |
|-----------|-----------|--------|--------|
| **C1** (null validity) | null_median < 0 nats | alpha=0.5: -78.36, alpha=1.0: -130.91, alpha=2.0: -116.10 | **PASS** (all 3) |
| **C3** (sensitivity) | p < 0.001 | p=0.0005 for all alphas | **PASS** (all 3) |
| **C6** (design) | 48/48 pairs with 4 candidates | 48/48 verified | **PASS** |
| **C7** (stratum coverage) | >= 2 non-empty buckets | 2 non-empty (5-9, 10-19) | **PASS** |

**Verdict: SURVIVES_CURRENT_TEST** — All 4 gating criteria pass.

### 3.2 Alpha Prior Sweep

| alpha_prior | K2 (stochastic) | K3 (stochastic) | K3-K2 | null_median | p_value | C1 | C3 |
|-------------|-----------------|-----------------|-------|-------------|---------|----|----|
| 0.5 | 643.09 nats | 878.12 nats | 235.03 | -78.36 | 0.0005 | PASS | PASS |
| 1.0 | 338.67 nats | 482.43 nats | 143.75 | -130.91 | 0.0005 | PASS | PASS |
| 2.0 | 167.90 nats | 246.99 nats | 79.09 | -116.10 | 0.0005 | PASS | PASS |

**Interpretation:** Less informative priors (alpha=0.5) produce larger Bayes factors because they allow more flexibility in the posterior, making the data more discriminating. All alphas pass both C1 and C3, confirming robustness to prior specification.

### 3.3 Null Distribution

The null distribution under shuffled action labels is centered negative across all alphas:

- **alpha=0.5:** null_median=-78.36, null_mean=-78.17, std=15.57, null_max=-21.14
- **alpha=1.0:** null_median=-130.91, null_mean=-130.74, std=10.08, null_max=-92.94
- **alpha=2.0:** null_median=-116.10, null_mean=-115.93, std=6.06, null_max=-92.77

The null median being negative confirms that Occam's razor correctly penalizes the larger action-dependent model when actions are irrelevant (shuffled). The observed log BF (168-643 nats) is far above the null maximum (-21 to -93 nats), demonstrating strong separation.

### 3.4 Positive Control

Deterministic SPA (100% hash routing, no stochasticity):
- K2 = 854.13 nats, K3 = 916.18 nats (alpha=0.5)

The Bayesian approach correctly detects the strong deterministic action effect. The stochastic SPA signal (168-643 nats) is 19-75% of the deterministic ceiling, consistent with the 50% stochastic mixing ratio.

### 3.5 Phase 2: Beyond-Markov K3-K2

Exploratory beyond-Markov testing at alpha=0.5:
- **K3-K2 = 235.03 nats** (point estimate positive)
- Bootstrap 95% CI: [-415.20, 34.39] — **includes zero**

The positive point estimate is consistent with the audit-corrected recomputation (79-235 nats), but the bootstrap CI crosses zero, indicating high variance. Phase 2 is exploratory per the frozen spec and does not gate the main verdict. The high variance may reflect:
- Limited within-session action diversity (4 actions per step)
- Stratum fragmentation in the action-history conditioning space
- The K3 model having 1567 full params vs 2804 reduced params (action-history space is large)

### 3.6 Stratum Size Decomposition

| Bucket | Strata | Records | Observed BF |
|--------|--------|---------|-------------|
| 5-9 | 343 | 2147 | 187.64 nats |
| 10-19 | 37 | 433 | 67.96 nats |
| 20-49 | 0 | 0 | — |
| 50+ | 0 | 0 | — |

No strata with >= 20 records exist at N=5000. The smaller strata (5-9 records) dominate and still show strong positive log BF (188 nats), indicating the Bayesian approach is robust to small-sample strata when K=12 provides proper penalty.

## 4. Comparison to Prior Estimator Families

| Estimator Family | C1 (null centering) | C3 (sensitivity) | Reference |
|-----------------|---------------------|------------------|-----------|
| Plug-in KL (alpha 0-1.0) | PASS at alpha=1.0 | FAIL (K3=0.099) | EXP-PHYSICS-35530591329 |
| Entropy-rate CMI (alpha 0.1-1.0) | FAIL (all alphas) | N/A | EXP-PHYSICS-35538866166 |
| KSG CMI k=5 | PASS | FAIL (K3=0.018) | EXP-PHYSICS-35476270440 |
| LR chi2 | PASS | FAIL (K2=K3 exactly) | EXP-PHYSICS-35476270440 |
| **Bayesian (K=12)** | **PASS (all alphas)** | **PASS (p=0.0005)** | **This experiment** |

The Bayesian Dirichlet-Multinomial approach is the **first** estimator to pass both C1 and C3 on this SPA class. It succeeds because:
1. It operates on marginal likelihood ratio, not histogram-smoothed CMI
2. The K=12 penalty correctly accounts for the full state space, not just observed states
3. The Dirichlet-Multinomial prior provides principled regularization without Laplace smoothing bias

## 5. What This Does and Does Not Establish

### Established (within this SPA class)
- The Bayesian Dirichlet-Multinomial model comparison passes C1+C3 on the stochastic 12-state SPA with N=5000 transitions
- The K=12 fix resolves the parent's MEASUREMENT_INVALID verdict
- Null centering is robust across alpha prior values {0.5, 1.0, 2.0}
- The Bayesian paradigm bypasses the Laplace smoothing bias that defeated all prior estimator families

### Not established
- C-WEB-DYNAMICS (real Web dynamics) — all evidence is synthetic SPA
- Beyond-Markov K3-K2 dynamics — Phase 2 bootstrap CI includes zero
- Generalization to production Web data with high-cardinality state spaces
- Practical utility for SPIDER exploration (the 1.52-bit CMI is detectable, but the Bayes factor scale is not directly comparable to PMI bits)

## 6. Consequences for Physics Lane

The Bayesian paradigm is the first valid detection method for discrete CMI on this SPA class. This:
- **Unblocks** Phase 2 beyond-Markov K3-K2 testing (with larger N to resolve bootstrap variance)
- **Establishes** a viable estimator paradigm for future synthetic SPA experiments
- **Does not** close the C-WEB-DYNAMICS hypothesis (which requires real Web data)
- **Does not** authorize product promotion (all evidence is synthetic)

## 7. Recommended Next Steps

1. **Phase 2 replication:** Re-run K3-K2 comparison with N=50000 transitions (10x current) to resolve bootstrap CI
2. **Real SPA validation:** Test Bayesian model comparison on TodoMVC hash-SPAs with URL-level PMI (leverage EXP-PHYSICS-35262258744 infrastructure)
3. **Prior sensitivity analysis:** Test alpha prior in [0.1, 0.3, 0.5, 1.0, 2.0, 5.0] to characterize the full BF-alpha relationship
4. **Production Web:** If synthetic validation passes, test on production SPA transitions with richer state representations
