# EXP-PHYSICS-35697037202 — Preregistration

## Status

DESIGN ONLY. Not yet frozen.

## Experiment Identity

- **Experiment ID:** EXP-PHYSICS-35697037202
- **Lane:** physics
- **Claim:** C-WEB-DYNAMICS
- **Director Mandate:** PIVOT from K=3-4 estimator tuning to timescale separation
- **Parent:** EXP-PHYSICS-35651906573 (SURVIVES_CURRENT_TEST, negative BF, audit REVISE)

## Strategic Context

The Global Research Director identified that Physics has 41 consecutive C-WEB-DYNAMICS experiments, the Bayesian estimator is validated on synthetic SPA but shows negative log BF on real TodoMVC, and the parent handoff proposes K=3-4 tuning on the same URL-level representation. The Director chose to PIVOT to an orthogonal question — timescale separation — rather than continue estimator refinement within a constrained basin.

This experiment tests whether TodoMVC hash-SPA state transitions exhibit temporal structure at multiple timescales, which is a fundamentally different question from whether actions add predictive information beyond memory.

## Research Question

Do TodoMVC hash-SPA state transitions exhibit timescale separation — autocorrelation structure that decays non-uniformly across lags, revealing distinct characteristic timescales — or is the temporal structure flat (indistinguishable from a memoryless process)?

## Hypotheses

### H1 (Primary): Lag-1 Autocorrelation Exceeds Null

The empirical autocorrelation function (ACF) of URL-state sequences at lag 1 exceeds the within-session shuffled-action null distribution at p < 0.01 (Bonferroni-corrected across 5 variants).

**Operationalization:**
- State representation: full URL (including hash fragment), e.g., `https://todomvc.com/examples/javascript-es6/dist/#/`
- ACF computation: for each variant, concatenate NL transitions across sessions in chronological order; encode each URL as an integer index; compute sample ACF at lags 0-6
- Null: for each of N_SHUFFLE=1999 permutations, shuffle action labels within each session (preserving state sequence), recompute ACF
- Test: one-sided permutation test at each lag; Bonferroni correction across 5 variants

### H2 (Secondary): Non-Uniform ACF Decay

The ACF at lags 1-6 is not flat (one-way ANOVA on lag-1 through lag-6 ACF values, p < 0.05), indicating characteristic timescales rather than exponential decay.

### H3 (Exploratory): FSM-Type Differences

The ACF decay pattern differs between the two effective FSM types ({vanillajs,react,svelte} 4-state vs {vue,angular} 3-state), tested via FSM-type × lag interaction in a two-way ANOVA.

### H4 (Exploratory): Inter-Event Time Multimodality

Inter-event time distributions (time between consecutive NL transitions within a session) show multimodal structure (Hartigan's dip test p < 0.05), consistent with distinct operational timescales (fast page-load vs slower session-step).

## Data Source

NL transition artifacts from EXP-PHYSICS-35651906573:
- `nl_transitions_vanillajs.json` (80 NL transitions, 6 sessions)
- `nl_transitions_react.json` (80 NL transitions, 6 sessions)
- `nl_transitions_svelte.json` (80 NL transitions, 6 sessions)
- `nl_transitions_vue.json` (80 NL transitions, 6 sessions)
- `nl_transitions_angular.json` (80 NL transitions, 6 sessions)

Total: ~400 NL transitions across 5 variants, 30 sessions.

## Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-SHUFFLE-ACTION | Within-session shuffled-action null (N=1999) | ACF at lag 1 ≈ 0 |
| B-SHUFFLE-STATE | Within-session shuffled-state null (N=1999) | ACF similar to empirical if driven by self-loops |
| B-MARKOV-1 | First-order Markov surrogate (N=500) | ACF matches empirical if first-order dynamics sufficient |
| B-FREQUENCY | State-frequency stationary null | ACF = 0 at all lags > 0 |

## Controls

| ID | Type | Expected Behavior |
|----|------|-------------------|
| POS-DETERMINISTIC-SPA | Positive control | Significant lag-1 ACF, non-uniform decay |
| NULL-RANDOM-WALK | Null control | lag-1 ACF ≈ 1/n_states, uniform decay |

## Decision Rule

**FALSIFIED** if ANY of:
- C1: lag-1 ACF does NOT exceed shuffled-action null at corrected p < 0.01 across 5 variants
- C2: ACF at lags 1-6 is flat (ANOVA p > 0.05)
- C3: Inter-event times unimodal (dip test p > 0.05)

**SUPPORTS H1** if ALL of:
- C1 passes (lag-1 ACF exceeds null at corrected p < 0.01 on ≥ 4/5 variants)
- C2 passes (ACF non-uniform, ANOVA p < 0.05)
- ACF decay differs between FSM types (FSM-type × lag interaction, p < 0.05)

**MIXED** if some conditions pass and others fail.

**INCONCLUSIVE** if measurement validity fails.

## Measurement Validity Requirements

1. Timestamps valid ISO 8601, monotonic within sessions, >1ms resolution
2. NL transitions only (use parent's filtered artifacts directly)
3. Effective independent FSM types = 2 (report per-type ACF)
4. Minimum 40 NL transitions per FSM type for lag-6 ACF
5. Bonferroni correction across 5 variants for C1

## Consequences

**Positive:** Timescale separation detected → new detection paradigm for Web dynamical structure; informs freshness guards (C-FRESHNESS) with differential update policies.

**Negative:** No timescale separation on TodoMVC → minimal deterministic SPAs lack temporal complexity; Physics should test richer environments (production SPAs, stochastic transitions, client-side state).

## Analysis Plan

1. Load NL transition artifacts; verify timestamp quality
2. Encode URL states as integer indices per variant
3. Compute sample ACF at lags 0-6 for each variant
4. Generate shuffled-action nulls (N=1999); compute null ACF distribution
5. Compute permutation p-values for lag-1 ACF; apply Bonferroni correction
6. Test ACF uniformity across lags (ANOVA)
7. Compute inter-event times; apply Hartigan's dip test
8. Compare ACF between FSM types (two-way ANOVA)
9. Run positive control on synthetic SPA data
10. Report all metrics, controls, and validity checks
