# EXP-PHYSICS-35130680344 — Non-trivial vs Trivial Encoding PMI Experiment

## Executive Summary

This experiment tests whether non-trivial response encoding (page content without explicit state labels) yields conditional PMI about next state on a branching FSM where action-history at K=3 does NOT fully determine next state (H > 0.2 bits). The experiment is **MEASUREMENT_INVALID** due to positive control failure: session-randomized control BC PMI remains high (0.640 bits), indicating the control does not break response-state correlation as intended.

## Key Findings

1. **Ceiling eliminated**: H(S_next|URL, H_K=3) = 1.1025 bits > 0.2 bits ✓
2. **Non-trivial BC PMI at K=3**: 0.7659 bits > 0.05 bits threshold ✓
3. **Bonferroni p-value**: 0.0759 > 0.0125 threshold ✗ (fails criterion C2)
4. **Trivial BC PMI at K=3**: 0.3449 bits (lower than non-trivial)
5. **Determinism check**: Passes for both conditions (accuracy=1.0) ✓
6. **Session-randomized positive control**: BC PMI = 0.6404 bits (not close to 0) ✗
7. **Cardinality**: Passes for non-trivial, fails for trivial (expected due to session-specific fields)

## Interpretation

The high non-trivial BC PMI (0.7659 bits) suggests that page-content structure (title, items, status) carries predictive information about next state. However, the measurement is invalid due to:

1. **Positive control failure**: Session randomization does not break response-state correlation because response is deterministic per state. The control design may be inappropriate for non-trivial encoding.

2. **Bonferroni p-value not significant**: Raw p-value 0.019 becomes 0.076 after Bonferroni correction across 4 comparisons.

3. **Trivial encoding cardinality degenerate**: Some strata have |R|/N >= 0.8, but this is expected due to session-specific response fields.

## Comparison with Parent Experiment

- Parent (EXP-PHYSICS-35040401992): MEASUREMENT_INVALID due to V1 (determinism check), V2 (positive control degeneracy), V10 (state label injection)
- This experiment: MEASUREMENT_INVALID due to positive control failure (session randomization ineffective for non-trivial encoding)

The parent's V10 concern (state label injection) is partially addressed: non-trivial BC PMI (0.7659) > trivial BC PMI (0.3449), suggesting page-content structure carries additional predictive information beyond explicit state labels. However, the measurement is invalid, so no scientific conclusion is justified.

## Validity Threats

1. **Positive control design**: Session randomization does not affect response content for non-trivial encoding. A different control (e.g., state randomization) may be needed.

2. **Deterministic state-response mapping**: Non-trivial response is deterministic per state, making PMI high by construction. The question is whether this reflects genuine predictive information or trivial mapping.

3. **Synthetic environment**: Locally-hosted Express SPA with deterministic transitions may not reflect production SPAs.

## Recommendations

1. Redesign positive control for non-trivial encoding (e.g., randomize state assignments instead of session assignments).
2. Consider whether deterministic state-response mapping is a valid test of predictive information.
3. Test with non-deterministic transitions or noisy observations to better approximate real web dynamics.

## Conclusion

The experiment does not provide valid scientific evidence for or against C-WEB-DYNAMICS due to measurement invalidity. The high non-trivial BC PMI is suggestive but not interpretable without a valid positive control.