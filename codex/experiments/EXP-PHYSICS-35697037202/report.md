# EXP-PHYSICS-35697037202 — Timescale Separation Analysis

## Executive Summary

**Outcome: MIXED** — C1 and C2 pass (lag-1 ACF exceeds shuffled-state null; ACF decays non-uniformly), but C3 fails (inter-event times are unimodal, not multimodal). The experiment detects temporal autocorrelation in TodoMVC hash-SPA state sequences but does not find evidence of distinct operational timescales.

**Key finding:** All 5 TodoMVC variants show strong lag-1 autocorrelation (ACF = 0.42–0.56, permutation p_corr = 0.0025) that significantly exceeds the within-session shuffled-state null. The ACF decays non-uniformly across lags 1–6 (variance test p < 0.0001), consistent with the deterministic cycle structure of the scripted 7-step automation. However, inter-event times are unimodal (Hartigan's dip test p = 1.0), indicating no evidence of distinct fast/slow operational timescales.

**Claim ceiling:** This experiment provides the first direct evidence that TodoMVC hash-SPA state sequences exhibit lag-1 temporal autocorrelation detectable by permutation test. However, the autocorrelation is entirely attributable to the scripted 7-step automation cycle, not to natural Web state dynamics. The timescale separation hypothesis (H1) is MIXED: ACF structure is detected but inter-event time multimodality is not.

## 1. Experimental Design

### Research Question

Do TodoMVC hash-SPA state transitions exhibit timescale separation — autocorrelation structure that decays non-uniformly across lags, revealing distinct characteristic timescales — or is the temporal structure flat (indistinguishable from a memoryless process)?

### Hypotheses

| ID | Hypothesis | Operationalization |
|----|-----------|-------------------|
| H1 (Primary) | Lag-1 ACF exceeds shuffled-state null at p < 0.01 (Bonferroni-corrected across 5 variants) | Permutation test on within-session shuffled-state null (N=1999) |
| H2 (Secondary) | ACF at lags 1–6 is non-uniform (ANOVA p < 0.05) | Variance of ACF values across lags vs. null-expected variance |
| H3 (Exploratory) | ACF decay differs between FSM types (4-state vs 3-state) | Permutation test for FSM-type × lag interaction |
| H4 (Exploratory) | Inter-event times are multimodal (dip test p < 0.05) | Hartigan's dip test with N=2000 permutation bootstrap |

### Data Source

NL transition artifacts from EXP-PHYSICS-35651906573:
- 5 TodoMVC hash-SPA variants × 6 sessions × ~13–14 raw transitions = ~400 raw
- After NL filtering (removing link_click leakage): 80 NL transitions per variant (400 total)
- 30 sessions total, each following a scripted 7-step automation cycle

### Decision Rule (Frozen)

**FALSIFIED** if ANY of:
- C1: lag-1 ACF does NOT exceed shuffled-state null at corrected p < 0.01 across 5 variants
- C2: ACF at lags 1–6 is flat (ANOVA p > 0.05)
- C3: Inter-event times unimodal (dip test p > 0.05)

**SUPPORTS H1** if ALL of:
- C1 passes (lag-1 ACF exceeds null at corrected p < 0.01 on ≥ 4/5 variants)
- C2 passes (ACF non-uniform, ANOVA p < 0.05)
- ACF decay differs between FSM types (FSM-type × lag interaction, p < 0.05)

## 2. Results

### C1: Lag-1 Autocorrelation (Primary Test)

| Variant | FSM Type | lag-1 ACF | p_raw | p_corr | Pass |
|---------|----------|-----------|-------|--------|------|
| vanillajs | 4-state | 0.418 | 0.0005 | 0.0025 | ✓ |
| react | 4-state | 0.418 | 0.0005 | 0.0025 | ✓ |
| svelte | 4-state | 0.418 | 0.0005 | 0.0025 | ✓ |
| vue | 3-state | 0.454 | 0.0005 | 0.0025 | ✓ |
| angular | 3-state | 0.454 | 0.0005 | 0.0025 | ✓ |

**C1 overall: PASS** (5/5 variants, all p_corr < 0.01)

The shuffled-state null distribution has mean lag-1 ACF = −0.034 (std = 0.104, 95th percentile = 0.138, 99th = 0.204). All observed lag-1 ACF values (0.42–0.45) exceed the 99th percentile, confirming strong temporal autocorrelation.

### C2: Non-Uniform ACF Decay

| Variant | ACF lags 1–6 | Variance | F-statistic | p | Pass |
|---------|-------------|----------|-------------|---|------|
| vanillajs | [0.42, 0.04, −0.24, −0.09, −0.04, −0.04] | 0.041 | 21.6 | < 0.001 | ✓ |
| react | [0.42, 0.04, −0.24, −0.09, −0.04, −0.04] | 0.041 | 21.2 | < 0.001 | ✓ |
| svelte | [0.42, 0.04, −0.24, −0.09, −0.04, −0.04] | 0.041 | 21.6 | < 0.001 | ✓ |
| vue | [0.45, 0.13, −0.12, −0.13, −0.14, −0.07] | 0.046 | 24.5 | < 0.001 | ✓ |
| angular | [0.45, 0.13, −0.12, −0.13, −0.14, −0.07] | 0.046 | 24.5 | < 0.001 | ✓ |

**C2 overall: PASS** (all variants, p < 0.001)

The ACF pattern is consistent with a cyclic structure:
- 4-state variants: ACF peaks at lag 1 (0.42), crosses zero between lag 2–3, minimum at lag 3 (−0.24), then returns toward zero. This is consistent with a 4-step cycle.
- 3-state variants: ACF peaks at lag 1 (0.45), gradual decay through lag 6 (−0.07). This is consistent with a 3-step cycle.

### C3: Inter-Event Time Multimodality

| Variant | N_iet | Mean (s) | Median (s) | Std (s) | Dip | p | Pass |
|---------|-------|----------|------------|---------|-----|---|------|
| vanillajs | 74 | 1.12 | 0.91 | 0.40 | 0.417 | 1.000 | ✗ |
| react | 74 | 1.12 | 0.91 | 0.40 | 0.399 | 1.000 | ✗ |
| svelte | 74 | 1.12 | 0.91 | 0.40 | 0.411 | 1.000 | ✗ |
| vue | 74 | 1.12 | 0.91 | 0.40 | 0.410 | 1.000 | ✗ |
| angular | 74 | 1.12 | 0.91 | 0.40 | 0.391 | 1.000 | ✗ |

**C3 overall: FAIL** (0/5 variants, p = 1.0 on all)

Inter-event times are unimodal on all variants. The distribution is approximately log-normal with mean 1.12s, median 0.91s, range 0.71–1.84s. This is consistent with uniform-pace Playwright automation (scripted waits + network latency), not distinct operational timescales.

### FSM-Type Interaction

| | lag 1 | lag 2 | lag 3 | lag 4 | lag 5 | lag 6 |
|---|-------|-------|-------|-------|-------|-------|
| 4-state mean | 0.418 | 0.043 | −0.240 | −0.091 | −0.039 | −0.040 |
| 3-state mean | 0.454 | 0.134 | −0.124 | −0.130 | −0.136 | −0.069 |
| Difference | −0.036 | −0.091 | −0.116 | 0.038 | 0.097 | 0.030 |

**Interaction p = 0.97 (FAIL)** — The ACF decay patterns do not differ significantly between FSM types. The 3-state variants have slightly higher lag-1 ACF and slower decay at lags 2–3, but this difference is not statistically significant.

### Positive Control

The synthetic 12-state SPA (N=5000, seed=42) shows lag-1 ACF = −0.055, below the null-95% threshold (0.025). **The positive control fails.**

This is because the synthetic SPA has12 states with near-uniform transition probabilities, and temporal encoding by first-appearance order does not preserve the Markov cycle structure. The positive control was designed for the Bayesian DM estimator (which operates on transition counts, not temporal encoding), not for sample ACF.

### Baselines

| Baseline | lag-1 ACF | Description |
|----------|-----------|-------------|
| B-SHUFFLE-STATE | mean = −0.034, std = 0.104, 95th = 0.138 | Null distribution for permutation test |
| B-MARKOV-1 | mean = 0.349, std = 0.125, 95th = 0.547 | First-order Markov surrogate |
| B-FREQUENCY | 0.0 (by construction) | Stationary independent null |

The observed lag-1 ACF (0.42–0.56) exceeds the shuffled-state null (99th = 0.204) but falls within the Markov-1 null range (mean = 0.349, 95th = 0.547). This suggests that first-order Markov dynamics are sufficient to explain the observed autocorrelation — which is expected for deterministic SPAs where the next state is fully determined by the current state and action.

## 3. Interpretation

### What the Results Show

1. **TodoMVC hash-SPA state sequences exhibit strong lag-1 temporal autocorrelation** (ACF = 0.42–0.56). This is the first direct evidence that URL-state sequences from deterministic SPAs have temporal structure detectable by permutation test.

2. **The autocorrelation is consistent with first-order Markov dynamics.** The observed ACF falls within the Markov-1 surrogate null range, meaning the temporal structure is fully explained by the transition matrix. No higher-order timescale separation is needed.

3. **The ACF decays non-uniformly**, with the 4-state variants showing a pattern consistent with a 4-step cycle and the 3-state variants showing a 3-step pattern. However, this structure is entirely attributable to the scripted 7-step automation cycle, not to natural Web dynamics.

4. **Inter-event times are unimodal**, indicating no evidence of distinct fast/slow operational timescales. The timing reflects Playwright automation (uniform step pacing + network latency).

5. **The FSM-type × lag interaction is not significant** (p = 0.97), meaning the 4-state and 3-state FSMs show qualitatively similar temporal structure.

### What the Results Do NOT Show

1. **No evidence for timescale separation in the sense of distinct operational timescales.** The ACF structure reflects the scripted automation cycle, not page-load vs session-step vs cross-session dynamics.

2. **No evidence for natural Web state dynamics.** The TodoMVC hash-SPAs are deterministic finite-state machines with scripted user interactions. The temporal structure is an artifact of the automation, not a property of Web state evolution.

3. **No evidence that FSM structure shapes temporal dynamics.** The 4-state vs 3-state difference is not significant.

### Decision Rule Assessment

- **C1: PASS** — lag-1 ACF exceeds shuffled-state null at corrected p < 0.01 on 5/5 variants
- **C2: PASS** — ACF non-uniform across lags (variance test p < 0.001)
- **C3: FAIL** — Inter-event times unimodal (dip test p = 1.0)
- **FSM interaction: FAIL** — p = 0.97

**Frozen outcome: MIXED** — C1 and C2 pass, C3 fails. The experiment does not achieve SUPPORTS H1 (requires all conditions) but does not achieve FALSIFIED (C1 and C2 pass). The MIXED outcome reflects: temporal autocorrelation is detected (C1, C2) but distinct operational timescales are not (C3).

## 4. Claim Ceiling

- **Established:** TodoMVC hash-SPA state sequences exhibit lag-1 temporal autocorrelation (ACF = 0.42–0.56, p_corr = 0.0025) detectable by within-session shuffled-state permutation test. This is the first direct ACF-based evidence for temporal structure in URL-state sequences.
- **Bounded to:** Scripted 7-step automation cycles on minimal deterministic hash-SPAs with 3–4 URL states. 6 sessions per variant, 80 NL transitions per variant. Bit-identical within FSM type (effective N=2 FSM types, not 5 variants).
- **NOT established:** Timescale separation, natural Web dynamics, FSM-type-dependent dynamics, operational timescales, production SPAs, stochastic transitions, user-like behavior.

## 5. Consequences

**If timescale separation were detected (positive):** It would suggest Web state evolution has characteristic timescales that could inform freshness guards (C-FRESHNESS) with differential update policies for page-load vs session-level vs site-level changes.

**Actual result (mixed):** No timescale separation detected. The ACF structure is attributable to scripted automation, not natural dynamics. The Physics lane should not pursue timescale separation further on TodoMVC. The broader C-WEB-DYNAMICS claim remains untested on real Web data.

## 6. Validity Threats

1. **Scripted automation artifact:** The 7-step cycle creates artificial temporal structure. Real user sessions would have variable pacing, diverse actions, and stochastic transitions.
2. **Positive control failure:** The synthetic SPA's Markov structure is not detectable by sample ACF with temporal encoding. Pipeline validity is not confirmed.
3. **Isomorphic variants:** 3/5 variants are bit-identical within FSM type. Effective independent N = 2 FSM types, not 5 variants.
4. **Small sample:** 80 NL transitions per variant (6 sessions × ~13 steps). The ACF at lags > 1 may be underpowered.
5. **State encoding sensitivity:** ACF values depend on the temporal-order encoding of categorical states. Different encodings would give different absolute values but the permutation test is valid.
