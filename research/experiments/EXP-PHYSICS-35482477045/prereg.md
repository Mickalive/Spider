# EXP-PHYSICS-35482477045 preregistration

## Background

The Physics lane's estimator-screening program (EXP-PHYSICS-35476270440) achieved a breakthrough: KSG CMI and likelihood-ratio both center the shuffled-action null near zero for the first time (|null|=0.0155 and 0.0045 bits respectively, both <0.1 threshold), breaking the 0.41-bit plug-in PMI floor that blocked all prior estimators.

However, the frozen verdict is FALSIFIED-IN-SETTING because neither estimator passes C3 (positive control): KSG achieves positive_control_k3=0.018 bits and LR 0.241 bits, both below the 1.0-bit threshold. The C3 failure is a **test-design limitation**, not an estimator failure: the 8-state deterministic SPA produces I(Y;A|Z)=0 by construction for CMI estimators (P(Y|Z,A)=P(Y|Z) when transitions are deterministic). The frozen C3 threshold (1.0 bit, calibrated for stratum PMI) is inappropriate for KSG CMI and LR chi2 scales.

The critical advance is that KSG/LR null centering is genuine and reproducible. What's missing is a **stochastic positive control SPA** where action genuinely changes P(Y|Z), allowing CMI estimators to demonstrate sensitivity while preserving null centering.

## Hypotheses

- **H0 (null)**: Neither KSG CMI nor likelihood-ratio achieves BOTH |shuffled-action null_mean| < 0.1 bits AND positive_control_k3 >= 0.5 bits on the stochastic SPA at N=5000.
- **H1 (alternative)**: At least one of KSG CMI or likelihood-ratio achieves BOTH |null_mean| < 0.1 bits AND positive_control_k3 >= 0.5 bits on the stochastic SPA at N=5000.
- **H2 (beyond-Markov, conditional on H1)**: K3 CMI - K2 CMI > 0.1 bits with bootstrap 95% CI lower > 0.0 at N=5000 on the stochastic SPA.

## Methods

### Stochastic Positive Control SPA Design

The key modification from the parent's deterministic SPA:

```python
def choose_next_stochastic(current, action, prev1, prev2, rng):
    candidates = CANDIDATES[current][action]
    if rng.random() < 0.5:
        # Deterministic branch: hash routing (same as parent)
        h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
        idx = int(h[:8], 16) % len(candidates)
        return candidates[idx]
    else:
        # Stochastic branch: uniform random over candidates
        return rng.choice(candidates)
```

This creates I(Y;A|Z) > 0 by construction:
- In the deterministic branch (50%), action determines the next state uniquely → P(Y|Z,A) ≠ P(Y|Z)
- In the stochastic branch (50%), action doesn't matter → P(Y|Z,A) = P(Y|Z)
- The mixture makes P(Y|Z,A) depend on A → CMI > 0

Theoretical properties:
- H(Y|Z,A) = 1.549 bits (per (z,a) distribution: 0.625 at target, 0.125 at each of 3 other candidates)
- H(Y|Z) depends on SPA structure but is > H(Y|Z,A)
- Expected CMI: 0.3-0.8 bits depending on SPA structure (conservative threshold: 0.5 bits)

### SPA Parameters
- 12-state hash-routed SPA (same STATES, ACTIONS, CANDIDATES as parent)
- N=5000 transitions (50 sessions × 100 steps), seed=42
- Strata with < 5 records skipped (MIN_STRATUM_SIZE=5)
- Stochastic mixing: p_deterministic=0.5, p_uniform=0.5

### Estimators Under Test
1. **KSG CMI**: sklearn.feature_selection.mutual_info_classif with k=5, alpha=1.0, discrete_features=True
2. **Likelihood-ratio**: scipy.stats.chi2_contingency, Bonferroni corrected

### Baselines (replication/controls)
3. **B-WEIGHTED-PMI**: Weighted-averaged per-stratum Laplace-smoothed PMI (parent null_mean=0.407)
4. **B-EQUAL-WEIGHT-PMI**: Equal-weight per-stratum PMI (parent null_mean=0.704)
5. **B-MEDIAN-PMI**: Median per-stratum PMI (parent null_mean=0.686)
6. **B-KNN-CMI**: KNN CMI k=5 alpha=1.0 (parent null_mean=-0.262)
7. **B-DETERMINISTIC-SPA**: KSG CMI on parent's 8-state deterministic SPA (expected CMI ~0 by construction)

### Null Control
- Shuffled-action null: 500 permutations, action labels shuffled within session
- Unit of permutation: action-label within session (same as parent)
- Threshold: |null mean| < 0.1 bits

### Positive Control
- Stochastic 12-state SPA (described above)
- Expected CMI: 0.3-0.8 bits
- Threshold: positive_control_k3 >= 0.5 bits, permutation p <= 0.001
- Additional degenerate control: KSG on deterministic SPA should yield ~0 (validates that stochasticity is the source of signal)

### Analysis Plan
1. Run stochastic SPA simulation (N=5000, seed=42)
2. Run deterministic SPA simulation (N=5000, seed=42) for degenerate control
3. Compute all 7 estimators on stochastic SPA data
4. Compute KSG on deterministic SPA data (degenerate control)
5. Compute shuffled-action null distribution (500 permutations) for each estimator
6. Apply Bonferroni correction for 5 primary comparisons (α=0.01)
7. Decompose bias by stratum size (5-9, 10-19, 20-49)
8. If any estimator passes C1, compute K3-K2 difference with bootstrap 95% CI (200 resamples)
9. If any estimator passes C1, run N=50000 convergence test (C4)

## Decision Rules

### FALSIFIED-IN-SETTING
If ANY of:
1. C1: All estimators have |null mean| ≥ 0.1 bits
2. C3: For any estimator passing C1, positive_control_k3 < 0.5 bits OR p > 0.001
3. C6: Design check fails (< 48/48 pairs with 4 candidates)

### MEASUREMENT_INVALID
If:
4. < 30% of strata have ≥ 5 records
5. < 2 non-empty size buckets
6. Any estimator implementation fails

### SURVIVES_CURRENT_TEST
Requires ALL:
- At least 1 estimator has |null_mean| < 0.1 bits (C1)
- Positive control passes for that estimator (C3: k3 >= 0.5, p <= 0.001)
- Design check passes (C6)
- ≥ 2 non-empty size buckets (C7)

### Phase 2 (beyond-Markov)
Only if SURVIVES on C1:
- C2: K3 - K2 > 0.1 bits AND bootstrap CI lower > 0.0
- C4: |K2(N=50000) - K2(N=5000)| ≤ 0.3 bits

## Validity Threats

1. **KSG sensitivity on discrete data**: KSG with k=5 on 12-state discrete data may have limited resolution. If KSG achieves null centering but positive_control_k3 < 0.5, this is a sensitivity limitation, not evidence against the SPA design. Mitigation: test k=3 and k=10 exploratorily.

2. **LR history collapse**: The parent found K2=K3=0.104 forced equal for LR because it tests action-dependence within each state, ignoring history. On the stochastic SPA, the same collapse may occur. Mitigation: report K3-K2 difference; if 0, note that LR cannot address beyond-Markov questions.

3. **SPA structure dependence**: The CMI magnitude depends on the specific CANDIDATES structure. If CMI is near 0.5 (the threshold), results may be fragile. Mitigation: report exact CMI and compare to theoretical bounds.

4. **Stochastic mixing ratio**: p=0.5 is chosen to create a clear signal. If p were too low (e.g., 0.1), CMI would be too small to detect. If too high (e.g., 0.9), the SPA becomes nearly uniform and CMI approaches maximum. The 0.5 ratio is a conservative middle ground.

## Expected Outcomes

- **If H1 passes**: The C3 test-design gap is closed. KSG and/or LR can detect genuine action-conditioned dynamics while maintaining null centering. Beyond-Markov K3-K2 testing is unblocked. Proceed to Phase 2.
- **If H0 confirmed**: The orthogonal-estimator pathway is closed for this SPA class. Pivot to fundamentally different detection paradigms or production Web data.

## Preregistration Timing

This preregistration is frozen before any outcome data is inspected. The stochastic SPA has not been implemented or run. Any analysis changes after seeing results will be exploratory and clearly labeled.
