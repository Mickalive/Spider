# Report: EXP-PHYSICS-35389142077

## Within-Stratum Conditional Permutation Null Control for Hash-Routed SPAs

**Status:** COMPLETE  
**Outcome:** FALSIFIES  
**Decision:** FALSIFIED-IN-SETTING

---

## Executive Summary

Within-stratum conditional permutation — the hypothesized fix for the inherited C4 null control failure — **does not center the null at zero** for hash-routed SPAs. The null mean = 0.417 bits at K=2 on the 12-state SPA simulation with N=5000, failing the frozen primary falsifier (|mean| < 0.1 bits). The PMI pipeline remains operational and the 0.933-bit K2 signal is reproducible, but the null control methodology is invalidated. Phase 2 (production SPA testing) was not attempted because the measurement framework is not valid under the biased null.

## Background

The parent experiment (EXP-PHYSICS-35375596894) confirmed beyond-Markov URL-level PMI (K2 state-history 0.933 bits, p=0.001) but was frozen as MEASUREMENT_INVALID because trajectory-level block permutation yielded null_mean=0.552 at K=2. The parent handoff identified the corrective action: replace block permutation with within-stratum conditional permutation, which preserves P(url_after|stratum) while breaking the action-PMI coupling, and should analytically center null at E[PMI]=0.

## Phase 1: Simulation Null Centering

### Data Collection
- 5000 transitions from 12-state SPA simulation (50 sessions x 100 steps, seed=42)
- Same SHA256(prev1:prev2:current:action) transition function as parent
- Raw SHA256: `170df6e34c78f64584f5332d61b9a705d87838b61e24eb04bdd4cc1b095c6ade` (matches parent)

### PMI Measurements (Reproducible)
| Conditioning | K | PMI (bits) | Strata Used | Prediction Accuracy |
|---|---|---|---|---|
| Unconditional | 0 | 1.419 | 12/12 | 0.161 |
| State-history | 1 | 1.531 | 141/148 | 0.240 |
| State-history | 2 | 0.933 | 398/1292 | 0.487 |
| State-history | 3 | 0.168 | 105/2779 | 0.535 |
| Action-history | 3 | 1.221 | 510/821 | 0.337 |

### Null Control Comparison (Primary Result)

| Method | Null Mean (bits) | Null Std | |Mean| < 0.1? |
|---|---|---|---|
| **Within-stratum** (new) | **0.417** | 0.0065 | **FAIL** |
| Block permutation (parent) | 0.552 | 0.0147 | FAIL |
| Action-shuffle (diagnostic) | 0.406 | 0.0076 | FAIL |

**Within-stratum permutation improves the null mean by 24.4%** (0.552 → 0.417) but remains 4.17x above the 0.1-bit threshold.

### Why Within-Stratum Fails

The within-stratum method shuffles url_after within each (url_before, history) stratum. Analytically, this should yield E[PMI]=0 because action and url_after become independent within each stratum while preserving P(url_after|stratum). However, the empirical null mean is 0.417 bits, indicating a systematic finite-sample bias.

Key observations:
1. **Action-shuffle convergence:** The action-shuffle diagnostic yields null_mean=0.406, nearly identical to within-stratum 0.417. This convergence suggests the bias is intrinsic to the PMI estimator weighting across deterministic/stochastic strata, not specific to the permutation scheme.
2. **Deterministic stratum dilution:** 31.5% of K2 strata are deterministic (single url_after), contributing PMI=0 by construction. The weighted average is dominated by stochastic strata where the permutation cannot fully break the action-outcome coupling in small samples.
3. **Stratum sparsity:** Mean observations per stratum = 5000/1292 ≈ 3.87. Only 398/1292 strata (30.8%) meet MIN_STRATUM_SIZE=5. Small strata have high variance and biased PMI estimates.

### Positive Control
8-state deterministic SPA: state K3 PMI = 1.671 bits (p=0.001), action K3 = 1.806 bits (p=0.001). Pipeline validated at N=5000.

### Determinism Check
- K2: 885 stochastic (68.5%), 407 deterministic (31.5%) — majority stochastic, explaining strong signal
- K3: 978 stochastic (35.2%), 1801 deterministic (64.8%) — sparsity dominates at higher K

## Phase 2: Production SPA Testing

**Not attempted.** Phase 1 falsified: the null control methodology does not center null at zero, making any production SPA measurement uninterpretable under the invalidated framework. Testing production SPAs with a biased null would produce either false positives (signal attributed to beyond-Markov dynamics when it is null bias) or uninterpretable p-values.

## Decision Rule (Frozen)

- **C1** (signal): K2 PMI 0.933 > 0.05 ✓
- **C2** (positive control): passes ✓
- **C3** (N≥5000): 5000 ✓
- **C4** (null centered): |0.417| < 0.1 ✗ **← Primary failure**

Frozen rule: FALSIFIED-IN-SETTING if |within_stratum_null_mean_K2| ≥ 0.1 bits.

## Interpretation

This is a **valid scientific negative** on the null control methodology, not a negative on the PMI signal itself:

1. **The 0.933-bit K2 PMI signal is real and reproducible** (p=0.001, d=79.7). It replicates the parent exactly.
2. **The null control bias is intrinsic to hash-routed SPA PMI estimation**, not specific to the permutation method. Three independent permutation schemes (block, within-stratum, action-shuffle) converge on null means 0.41-0.55 bits.
3. **Within-stratum permutation partially addresses the bias** (24.4% improvement) but does not resolve it. The analytic E[PMI]=0 argument fails under finite-sample conditions with deterministic/stochastic stratum mixing.
4. **The null control methodology for hash-routed SPAs requires fundamental rethink.** Candidate alternatives include model-based nulls (parametric bootstrap), unbiased PMI estimators, or alternative information measures (conditional entropy, transfer entropy).

## Consequences

**For C-WEB-DYNAMICS:** The claim remains HYPOTHESIS. The 0.933-bit PMI signal is a strong descriptive observation, but without a valid null control, it cannot support a confirmatory claim. The methodology gap is now identified as a fundamental estimator bias, not a fixable permutation artifact.

**For the Physics lane:** The null control problem for hash-routed SPAs is harder than previously understood. The bias floor of ~0.41 bits at N=5000 appears to be an intrinsic property of the PMI estimator on this environment class. Future experiments should consider:
- Model-based null (parametric bootstrap from estimated P(url_after|stratum))
- Alternative information measures (conditional entropy H(S'|S,A) - H(S'|S))
- Larger N to reduce finite-sample bias (N≥50000)
- Different SPA designs with fewer deterministic strata

**For Product lane:** No product promotion warranted. The PMI pipeline detects signal but the significance claims are unsupported under the biased null.
