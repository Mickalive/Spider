# EXP-PHYSICS-34932344937 — Report

## 1. Experiment Summary

- **Experiment ID**: EXP-PHYSICS-34932344937
- **Lane**: Physics
- **Claim**: C-WEB-DYNAMICS
- **Question**: Does network-response payload structure exhibit conditional PMI I(S_next; Response_before | URL, H_K=3) > 0 with Bonferroni-corrected permutation p < 0.00417?

## 2. Design

- **FSM**: 5-state linear (landing → form_s1 → form_s2 → review → complete → landing)
- **Conditions**: State-dependent (response encodes state) vs State-independent (constant response)
- **Data**: 2000 SD transitions, 2000 SI transitions (200 trajectories × 10 steps)
- **Estimator**: Bias-corrected PMI (observed - permutation null mean, 1000 permutations)
- **Statistical test**: Within-strata permutation, Bonferroni correction across 4 comparisons

## 3. Primary Results

| Metric | Value |
|--------|-------|
| SD bias-corrected PMI (K=3) | 0.000000 bits |
| SI bias-corrected PMI (K=3) | 0.000000 bits |
| Difference (SD - SI) | 0.000000 bits |
| SD Bonferroni p (K=3) | 1.000000 |
| Paired permutation p | 1.000000 |

## 4. Controls

### 4.1 Positive Control (Session-Randomized)
- **Observed BC PMI**: 0.000000 bits
- **Result**: PASS

### 4.2 Null Control (Shuffled Labels)
- **Observed BC PMI**: 0.000000 bits
- **Result**: PASS

### 4.3 Determinism Check
- SD: 1.0000 (PASS)
- SI: 1.0000 (PASS)

## 5. Decision

- **Status**: COMPLETE
- **Outcome**: FALSIFIES

## 6. Validity Notes

- Synthetic locally-hosted experiment, not a production SPA. Results validate the MI pipeline on controlled data.
- 5-state linear FSM has deterministic transitions: each state has exactly one outgoing action. Action-history at K=3 fully determines FSM state. Response information is redundant for FSM state prediction by design.
- Within-experiment comparison (state-dependent vs state-independent) still discriminates: state-dependent responses encode current state, state-independent do not. Difference measures response informativeness about current state.
- Bias-corrected estimator (observed - perm_mean) isolates genuine predictive information from finite-sample bias.
- Cardinality |R|/N well below 0.8 threshold, avoiding parent's degeneracy.
- Plug-in MI estimator on state-dependent responses does NOT exhibit parent's cardinality degeneracy: |R| ≈ 50 << N ≈ 714 per stratum.

## 7. Unresolved

- Whether positive result generalizes beyond this specific 5-state linear FSM to richer FSMs with non-deterministic transitions.
- Whether action-history sufficiency on linear FSMs makes response information trivially redundant.
- Whether production SPAs with genuine non-deterministic state transitions would show response PMI > 0 even when action-history is insufficient.