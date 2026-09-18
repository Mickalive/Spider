# EXP-GRAPH-35191029030 Report: Fixed Co-occurring Drift+Noise Orthogonality for C-FRESHNESS

## Executive Summary

**Status: MEASUREMENT_INVALID** — The experiment cannot support or falsify the orthogonality hypothesis due to a measurement design flaw: session_invalidation drift produces constant behavioral signal (std=0) because API endpoints do not check session validity.

**Descriptive observations:**
- Pooled Pearson r = 0.0498 (|r| = 0.0498) — very low, directionally consistent with orthogonality
- p = 0.4486 — not statistically significant due to zero-variance conditions reducing effective sample size
- permission_boundary conditions alone: r = 0.0514 (proper within-condition variation)

**Decision criteria:**
- **C1 (drift TP >= 0.85)**: mean TP = 1.0000 -> PASS
- **C2 (observability >= 80%)**: rate = 0.9917 -> PASS
- **C3 (orthogonality |r| < 0.3)**: |r| = 0.0498, p = 0.4486 -> FAIL (p not < 0.05)
- **C4 (null FP = 0.0)**: FP = 0.0000 -> PASS

**Validity gate**: 4/8 conditions have within-condition variance -> **MEASUREMENT_INVALID** per frozen decision rule (requires >= 6/8).

## Measurement Validity Issue

The session_invalidation drift clears the server-side session store, but the API endpoints (`/api/read`, `/api/write`, `/api/admin`) only check JWT token validity and permissions — they do NOT check session validity. Therefore:

- `session_state_changes` is always 1 (session is always invalid after drift)
- `token_validation_failures` is always 0 (token remains valid)
- `auth_boundary_shifts` is always 0 (no permission changes)
- **Behavioral composite is constant at 3.0** for all 120 session_invalidation samples

This means 4/8 co-occurring conditions have zero behavioral variance, making paired Pearson correlation undefined for those conditions. The pooled r=0.0498 is dominated by the constant behavioral values from session_invalidation conditions.

**This is a measurement design flaw, not evidence against orthogonality.** The session_invalidation signal IS detectable — but only via the `/session/status` endpoint, not via API endpoint probing.

## Design Changes from Parent (EXP-GRAPH-35166507358)

| Aspect | Parent | This Experiment |
|--------|--------|-----------------|
| Co-occurring drift patterns | signing_key_rotation, session_invalidation, permission_boundary | permission_boundary, session_invalidation ONLY |
| Structural probe | Response body from authenticated /api/read | Unauthenticated /schema endpoint |
| signing_key_rotation | Included (blocks ALL endpoints → structural=0.0) | EXCLUDED |
| Within-condition variation | Deterministic (constant per condition) | Stochastic (random permission subsets, token expiry jitter) |
| Correlation computation | Pooled condition means | Paired per-sample (behavioral_i, structural_i) |
| Number of co-occurring conditions | 15 (3 drift × 5 schema sizes) | 8 (2 drift × 4 noise) |

## Experimental Conditions

### Co-occurring Conditions (8 total)

| Condition | Drift Pattern | Noise Pattern | Samples | Behavioral Std | Structural Std |
|-----------|---------------|---------------|---------|----------------|----------------|
| permission_boundary + optional_field_addition | permission_boundary | optional_field_addition | 30 | 0.1652 | 1.1596 |
| permission_boundary + description_change | permission_boundary | description_change | 30 | 0.1571 | 0.6283 |
| permission_boundary + response_time_jitter | permission_boundary | response_time_jitter | 30 | 0.1571 | 0.9775 |
| permission_boundary + field_type_normalization | permission_boundary | field_type_normalization | 30 | 0.1633 | 0.6236 |
| session_invalidation + optional_field_addition | session_invalidation | optional_field_addition | 30 | **0.0000** | 1.0205 |
| session_invalidation + description_change | session_invalidation | description_change | 30 | **0.0000** | 0.6669 |
| session_invalidation + response_time_jitter | session_invalidation | response_time_jitter | 30 | **0.0000** | 0.9286 |
| session_invalidation + field_type_normalization | session_invalidation | field_type_normalization | 30 | **0.0000** | 0.6768 |

### Per-Condition Pearson r (Exploratory)

| Condition | r | p | Note |
|-----------|---|---|------|
| permission_boundary + optional_field_addition | 0.1924 | 0.3084 | Proper variation |
| permission_boundary + description_change | -0.3189 | 0.0859 | Proper variation |
| permission_boundary + response_time_jitter | 0.3135 | 0.0917 | Proper variation |
| permission_boundary + field_type_normalization | -0.2728 | 0.1447 | Proper variation |
| session_invalidation + * | null | null | Zero behavioral variance |

### Per-Drift-Pattern Pearson r (Exploratory)

| Drift Pattern | Samples | r | Note |
|---------------|---------|---|------|
| permission_boundary | 120 | 0.0514 | Proper variation, exploratory |
| session_invalidation | 120 | null | Zero behavioral variance |

## Primary Analysis

### Pooled Pearson Correlation

- **r = 0.0498** (|r| = 0.0498)
- **p = 0.4486** (permutation test, 1000 permutations)
- **n = 240** paired samples (8 conditions × 30 samples)
- **Note**: The low r value is partly driven by 120 constant behavioral values (3.0) from session_invalidation conditions. The effective sample size for correlation is reduced.

### Signal Observability

- **Both > 0**: 238/240 = 0.9917
- **C2 threshold**: >= 80% -> PASS
- Both behavioral and structural signals are non-trivially observable on nearly all samples.

### Within-Condition Variance

- **Conditions with variance (both signals std > 0)**: 4/8 (only permission_boundary conditions)
- **Measurement validity**: INVALID per frozen decision rule (requires >= 6/8 conditions with variance)

## Controls

### Positive Control: permission_boundary Detection

- **Observed rate**: 1.0000 (30/30)
- **Threshold**: >= 0.90
- **Pass**: YES

### Null Control: Noise-Only FP

- **Observed FP rate**: 0.0000 (0/120)
- **Threshold**: FP = 0.0
- **Pass**: YES

## Validity Threats

1. **session_invalidation behavioral signal is constant**: API endpoints do not check session validity, so session_state_changes is always 1. The behavioral signal from session_invalidation is only detectable via /session/status, not via API probing. This is the primary measurement validity issue.

2. **Deterministic mock server**: All measurements on localhost Flask, not production APIs.

3. **Limited drift patterns**: Only permission_boundary and session_invalidation tested.

4. **Unauthenticated /schema endpoint**: Synthetic construct not present in real APIs.

5. **Pooled Pearson r**: The pooled r is dominated by 120 constant behavioral values from session_invalidation conditions.

6. **Composite score weighting**: Behavioral weights (2, 3, 1) inherited from parent, not optimized.

## Interpretation

The experiment is MEASUREMENT_INVALID per the frozen decision rule because only 4/8 conditions have within-condition variance. The orthogonality hypothesis is **untested, not falsified**.

However, the descriptive data is informative:

1. **permission_boundary conditions show proper variation**: r = 0.0514 across 120 samples, with all 4 per-condition r values in [-0.32, 0.32]. This is directionally consistent with orthogonality but underpowered for individual conditions (n=30 each).

2. **The structural signal from /schema is genuinely independent of auth state**: 99.17% of samples have both behavioral > 0 AND structural > 0, confirming the measurement design achieves signal observability.

3. **The parent's C4 failure (r=0.593) was indeed caused by zero-imputation**: The new design achieves r=0.0498 (12x lower) even with the session_invalidation confound, because the /schema endpoint provides non-zero structural values on all conditions.

## Recommended Next Step

Redesign the session_invalidation behavioral measurement to include session-checking in the probe sequence. Specifically, add a `/session/status` check as part of the behavioral signal computation for session_invalidation conditions, so that session_state_changes varies within conditions (e.g., random session TTL affects when the session becomes invalid).

Alternatively, restrict the orthogonality test to permission_boundary conditions only (n=120, r=0.0514), which have proper within-condition variation and show directionally low correlation.

## Product Consequences

**UNKNOWN** — The measurement is invalid, so no product decision is authorized. The descriptive direction (r ≈ 0.05) is encouraging but not confirmatory.
