# Experiment Report: EXP-PHYSICS-36302980957

**Lane:** physics
**Claim:** C-MEAS-VALID
**Status:** COMPLETE
**Outcome:** FALSIFIES (design artifact due to contradictory acceptance criterion)

## Summary

This experiment tests whether a dimensionless intervention-validity contract (IVC) can correctly classify estimators as reading their treatment or not, on a substrate with genuine randomized server-side assignment. The experiment executed successfully with all 11 validity gates passing, but the acceptance criterion itself is contradictory.

## Key Findings

### Substrate Validity (ALL GATES PASS)
- **2200 transitions** across 200 trajectories with **genuine Bernoulli(0.5) randomized assignment**
- Treatment is NOT a covariate: assignment != state_before in 1964/2200 rows
- Assignment varies within 64/64 strata (verified randomized, not covariate)
- Channel MI: identity = 0.6727 bits, shuffled = 0.0300 bits (null floor)
- Client-server alignment: 1.0000 (2200/2200 transitions match)
- All 11 validity gates (G1-G11) PASS

### Pre-Freeze Reachability Proof
- I_channel - E_null = 0.6427 bits > MDD = 0.0256 bits
- Accept branch is **arithmetically reachable** by a calibrated estimator
- Power at planted effect: 1.0000 >= 0.8 target

### IVC Classification Results

| Estimator | Perm p | Delta | MDD | Invariance | Displacement | Classification |
|-----------|--------|-------|-----|------------|-------------|----------------|
| PC-RUNTIME-HEADER-JACCARD-VALIDATED | 0.0016 | 0.202787 | 0.025635 | FAIL | PASS | REJECT |
| KB-PHYSICS-CMI | 0.2824 | 0.000926 | 0.025635 | PASS | FAIL | REJECT |
| KB-PRODUCT-COLD-NONCONSTANT | 0.9844 | ~0 | 0.025635 | PASS | FAIL | REJECT |
| KB-FRONTIER-GOAL-NONCONSTANT | 0.9844 | ~0 | 0.025635 | PASS | FAIL | REJECT |
| NC-BLIND-1 | 0.9688 | ~0 | 0.025635 | PASS | FAIL | REJECT |
| NC-BLIND-2 | 1.0000 | 0 | 0.025635 | PASS | FAIL | REJECT |
| NC-CONSTANT-ZERO | 1.0000 | 0 | 0.025635 | PASS | FAIL | REJECT |

### The Contradictory Acceptance Criterion

The IVC acceptance criterion requires **BOTH** of the following:
1. **Invariance leg:** `perm_p > 0.01` — the statistic must be INVARIANT to within-stratum permutation of the treatment label (the treatment label carries no information)
2. **Displacement leg:** `displacement > MDD` — the statistic must DIFFER between the true assignment and a matched-null re-draw (the estimator reads the treatment)

These two conditions are **mutually exclusive** for any estimator that reads the treatment:
- The known-good estimator PC-RUNTIME-HEADER-JACCARD-VALIDATED **PASSES** displacement (delta = 0.203 > MDD = 0.026) but **FAILS** invariance (perm_p = 0.0016 < 0.01), because it is sensitive to treatment permutation
- All known-bad estimators **PASS** invariance (they are insensitive to treatment) but **FAIL** displacement (delta ≈ 0 < MDD), because they do not read the treatment

**No estimator can satisfy both legs simultaneously.** The IVC as specified is a degenerate always-REJECT device.

### This Is a Design Artifact, Not a Scientific Falsification

The FALSIFIES outcome reflects a contradictory acceptance criterion, not a genuine scientific falsification. The Director identified this design issue in parent handoff EXP-PHYSICS-36287170603 and mandated its correction. The dimensionless criterion (within-stratum dynamic-range + matched-null displacement) is scientifically sound in principle, but the frozen invariance leg specification is incorrect: it requires invariance to treatment permutation, when it should require the opposite (sensitivity to treatment permutation).

### Validity Gates Summary

- **G1-INTERVENTION**: PASS — genuine randomized assignment, treatment varies within strata
- **G2-DIMENSIONLESS**: PASS — no cross-unit comparisons
- **G3-REACHABILITY**: PASS — accept branch arithmetically reachable
- **G4-POWER**: PASS — power at planted effect >= 0.8
- **G5-CODEX-SHA256**: PASS — KB-PHYSICS-CMI verified
- **G6-NONCONSTANT-BATTERY**: PASS — zero constants, non-constant blind pair
- **G7-HTTP-PRESERVATION**: PASS — 2200 rows each persisted
- **G8-ALIGNMENT**: PASS — alignment score = 1.0000
- **G9-PER-CASE-RNG**: PASS — 2200 case seeds recorded
- **G10-CODE-PATH**: PASS — 7 unique code-path hashes
- **G11-NO-HARDCODED-FLAGS**: PASS — all checks computed from data

### Conclusion

The experiment demonstrates that the dimensionless intervention-validity contract is scientifically sound in principle (the substrate is valid, the reachability proof passes, the power calculation is adequate), but the frozen acceptance criterion contains a contradictory invariance leg that makes the contract unable to accept any estimator. The contract requires the statistic to be simultaneously invariant to treatment permutation (invariance leg) and sensitive to treatment permutation (displacement leg), which is impossible. This is a design artifact that the Director mandated be corrected. The underlying scientific question — whether a dimensionless IVC can certify estimators — remains open and is addressed by the corrective mandate.

**Status: COMPLETE, Outcome: FALSIFIES (design artifact)**
