# EXP-PHYSICS-35538866166 preregistration

## Status: DESIGN — not yet frozen.

## Question

Can entropy-rate estimation H(Y|Z,A)-H(Y|Z) (global conditional entropy difference, not per-stratum KL weighting) detect the 1.52-bit CMI signal on the stochastic 12-state SPA while maintaining |shuffled-action null_mean| < 0.1 bits, thereby bypassing the plug-in KL bias-variance tradeoff?

## Background

The parent experiment (EXP-PHYSICS-35530591329) established a monotonic, irreconcilable tradeoff between sensitivity and null centering for plug-in KL estimation on the stochastic 12-state SPA at N=5000:

- alpha=0: K3=1.377 bits (sensitive) but |null_mean|=0.924 (biased)
- alpha=1.0: |null_mean|=0.064 (centered) but K3=0.099 (insensitive)
- No alpha achieves both C1 and C3.

The bias is intrinsic to per-stratum KL weighting across varying-size strata with Laplace smoothing. The CANDIDATES redesign (0% deterministic strata) did not resolve it. KSG CMI k=5 is k-invariant but insensitive (K3=0.000560). LR chi2 collapses history (K2=K3 exactly).

## Hypothesis

**H1 (alternative):** Entropy-rate CMI estimation computes H(Y|Z) - H(Y|Z,A) globally rather than summing per-stratum KL. This global computation may avoid the small-stratum bias that dominates plug-in KL at alpha<1.0. At least one tested alpha achieves BOTH |shuffled-action null_mean| < 0.1 bits AND positive_control_cmi >= 0.5 bits on the stochastic SPA at N=5000.

**H0 (null):** All tested alphas have |null_mean| >= 0.1 bits OR positive_control_cmi < 0.5 bits.

## Estimator

Entropy-rate CMI:

```
CMI = H(Y|Z) - H(Y|Z,A)

H(Y|Z) = -sum_{z,y} P(z,y) log2 P(y|z)
  where P(y|z) = sum_a P(z,a,y) / P(z)

H(Y|Z,A) = -sum_{z,a,y} P(z,a,y) log2 P(y|z,a)
```

Both conditional entropies estimated via histogram with Laplace smoothing (alpha variable).

**Key difference from plug-in KL:** Global computation over the full joint distribution, not per-stratum weighted sum of log-ratios. The per-stratum KL bias arises from weighting small-stratum PMI contributions heavily; entropy-rate avoids this by computing entropies over aggregated counts.

**Z conditioning:**
- K3: Z = (current_state, history_action_K=3)
- K2: Z = (current_state, history_state_K=2)

## Controls

### C1: Null centering
- Shuffled-action within-session null (500 permutations)
- |mean across permutations| < 0.1 bits
- Same framework as parent EXP-PHYSICS-35530591329
- Unit of permutation: action-label within session

### C3: Positive control sensitivity
- Deterministic 12-state SPA (hash routing only, no stochastic mixing)
- H(Y|Z,A) = 0 by construction (deterministic transitions given (z,a))
- H(Y|Z) = log2(4) = 2.0 bits (4 actions lead to 4 distinct states)
- CMI = 2.0 bits
- Threshold: >= 0.5 bits (conservative, 4x below true signal)
- Permutation p <= 0.001

### C6: SPA design verification
- 48/48 (state,action) pairs with 4 distinct candidates

### C7: Stratum coverage
- >= 2 non-empty stratum size buckets

## Baselines

### B-PLUGIN-KL-ALPHA1
Replicate parent plug-in KL alpha=1.0 for direct comparison.
Expected: K3 ~0.099, |null_mean| ~0.064.

### B-PLUGIN-KL-ALPHA0
Replicate parent plug-in KL alpha=0 (MLE) for direct comparison.
Expected: K3 ~1.377, |null_mean| ~0.924.

### B-ENTROPY-RATE-DEG
Entropy-rate CMI on deterministic SPA. Expected CMI = H(Y|Z) > 0.

## Alpha values tested
0.1, 0.5, 1.0 (representative range spanning the tradeoff region)

## Sample size
N = 5000 transitions (50 sessions x 100 steps), seed=42.
Same as parent for direct comparability.

## Decision rules

### FALSIFIED-IN-SETTING if ANY of:
1. C1: All alphas have |null_mean| >= 0.1 bits
2. C3: For any alpha passing C1, positive_control_cmi < 0.5 bits OR p > 0.001
3. C6: Design check fails

### MEASUREMENT_INVALID if:
4. < 30% strata have >= 5 records
5. < 2 non-empty stratum size buckets
6. Implementation fails

### SURVIVES_CURRENT_TEST requires ALL:
- C1: At least 1 alpha has |null_mean| < 0.1 bits
- C3: Positive control passes for that alpha
- C6: Design check passes
- C7: >= 2 non-empty buckets

### Phase 2 (beyond-Markov, only if SURVIVES):
- C2: K3 CMI - K2 CMI > 0.1 bits, bootstrap 95% CI lower > 0.0
- C4: |K2(N=50000) - K2(N=5000)| <= 0.3 bits

## Expected outcomes and consequences

**If H1 passes:** The per-stratum KL bias is estimator-specific, not fundamental to discrete CMI estimation. The CMI research program is unblocked for beyond-Markov testing. Opens path to production SPA testing with stochastic transitions and richer state representations.

**If H0 confirmed:** The null centering problem may be intrinsic to the stochastic SPA design or discrete CMI estimation broadly. Physics lane pivots to: (a) Bayesian model comparison or likelihood-ratio tests, (b) production Web data with continuous state representations, (c) abandoning CMI estimation pathway entirely.

## What this experiment is NOT

- Not a test of C-WEB-DYNAMICS on real Web transitions (all evidence is synthetic SPA)
- Not evidence for or against beyond-Markov dynamics (Phase 2 only)
- Not a test of production Web sites or browser-based collection
- Not evidence that entropy-rate CMI generalizes beyond this SPA class

## Inherited state preserved

From parent EXP-PHYSICS-35530591329 handoff:

**Established:**
- True I(Y;A|Z) = 1.52 bits on stochastic 12-state SPA (audit-confirmed)
- Plug-in KL alpha sweep tradeoff is monotonic and irreconcilable
- KSG CMI k=5 is k-invariant but insensitive (K3=0.000560)
- Null centering at alpha=1.0 is robust (|mean|=0.064)
- Design verification: 48/48 pairs with 4 candidates
- CANDIDATES redesign yields 0% deterministic strata but bias identical to parent

**Rejected:**
- Plug-in KL estimator class with Laplace smoothing alpha in {0, 0.01, 0.1, 0.5, 1.0} for simultaneous C1+C3
- Hyperparameter tuning (reduced smoothing alpha<=0.1) as remedy
- Deterministic/stochastic strata mixing as cause of bias
- KSG CMI k=5 insensitivity from insufficient neighborhood resolution

**Unknown:**
- Whether entropy-rate estimation bypasses per-stratum KL bias
- Whether Bayesian model comparison detects the signal
- Whether likelihood-ratio tests bypass the bias
- Whether N=50000 resolves the tradeoff
- Generalization beyond 12-state discrete SPA

**Do not assume:**
- This experiment closes C-WEB-DYNAMICS or the Physics lane
- CMI estimation is fundamentally impossible on discrete SPAs (MLE recovers 1.377 bits)
- The 1.52-bit signal is undetectable
- Production Web transitions generalize from this synthetic SPA
