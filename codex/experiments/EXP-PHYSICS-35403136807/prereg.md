# EXP-PHYSICS-35403136807 — Preregistration

## Status: DESIGN ONLY — not yet frozen

---

## 1. Experiment Identity

- **Experiment ID:** EXP-PHYSICS-35403136807
- **Lane:** physics
- **Claim:** C-WEB-DYNAMICS (HYPOTHESIS)
- **Parent:** EXP-PHYSICS-35402003775
- **Parent Handoff SHA256:** dc110667c4e09b4e196d07a4cf6819afed4be2b3b00ef432b7e07b906663116d

## 2. Question

Is the 0.933-bit K2 PMI signal on the 12-state hash-routed SPA primarily **Markov** (action determines next state given current state) or genuinely **beyond-Markov** (history K>2 adds predictive information beyond current state)?

This experiment directly resolves the interpretive ambiguity left by the null centering impasse in EXP-PHYSICS-35402003775. The K3 vs K2 comparison is a **ratio/difference test**, not an absolute significance test, and therefore does not require null centering.

## 3. Hypotheses

### H1 (beyond-Markov): 
I(S_next; action | S_current, prev_action, prev_state) > I(S_next; action | S_current) by > 0.1 bits at N=5000. History beyond current state adds predictive information.

### H0 (Markov):
K3 PMI ≈ K2 PMI (difference ≤ 0.1 bits). Current state alone captures all action-conditioned predictability.

### H2 (bias structure):
The null bias floor (0.36–0.42 bits at N=5000) scales inversely with sample size, indicating finite-sample origin.

## 4. Inherited State (from parent handoff)

### Established:
- K2 PMI = 0.933 bits (p=0.001, d~79) at N=5000 on 12-state SPA
- K3 PMI = 1.221 bits (p=0.001) at N=5000 on same SPA
- Null centering fails for all tested frameworks (parametric bootstrap 0.357, Miller-Madow 0.407, conditional entropy degenerate)
- Bias floor ~0.36–0.42 bits is intrinsic to PMI weighted averaging across deterministic/stochastic strata (31.5% deterministic)
- Positive control validates PMI pipeline on deterministic SPA

### Rejected:
- Parametric bootstrap, Miller-Madow, conditional entropy, within-stratum permutation as null centering methods

### Unknown:
- Whether the 0.933-bit K2 PMI signal is Markov or beyond-Markov
- Whether null bias is finite-sample or asymptotic

### Do Not Assume:
- C-WEB-DYNAMICS is globally false (signal is real and reproducible)
- Null bias is evidence against beyond-Markov signal
- All PMI null frameworks are exhausted

## 5. State Representation

- **SPA:** 12-state SHA256 hash-routed SPA (same as parent experiments)
- **States:** 12 discrete states, URLs = /state/{hash}
- **Actions:** 4 action types (form_submit, button_click, js_navigate, link_click)
- **Transitions:** Deterministic candidates (4 of 12 states) + stochastic hash routing
- **N:** 5000 transitions (primary), 50000 transitions (exploratory bias-scaling)
- **PMI estimator:** Laplace-smoothed (alpha=1.0) conditional PMI

## 6. Measurement Conditions

### Primary conditions (N=5000):
1. **K1 PMI** = I(S_next; action) — marginal action predictability
2. **K2 PMI** = I(S_next; action | S_current) — current-state-conditioned (parent: 0.933 bits)
3. **K3 PMI** = I(S_next; action | S_current, H_K=2) — history-conditioned (parent: 1.221 bits)
4. **K3 − K2 difference** — primary test statistic
5. **Bootstrap 95% CI for K3 − K2** — 200 trajectory-block resamples

### Exploratory condition (N=50000):
6. **K2 PMI at N=50000** — tests whether bias floor decreases with 10x sample

## 7. Controls

### Positive control:
- 8-state deterministic SPA: K3 PMI ≥ 1.0 bit, p ≤ 0.001
- Validates estimator pipeline on environment where H(S_next | S_current, action) = 0

### Null control:
- Shuffled-action permutation (N_SHUFFLE=1000): action labels randomly reassigned
- Expected: mean PMI centered near 0 for K2 comparison
- For K3 vs K2: null is that K3 − K2 ≤ 0 under permutation of additional history

## 8. Decision Rule

### Primary verdict:
- **SURVIVES_CURRENT_TEST:** K3 − K2 > 0.1 bits AND bootstrap CI lower bound > 0.0
- **FALSIFIED-IN-SETTING:** K3 − K2 ≤ 0.1 bits OR CI includes 0

### Secondary:
- **FALSIFIED-IN-SETTING:** K2 ≤ K1 + 0.05 (current state not contributing)

### Controls gating:
- **MEASUREMENT_INVALID:** Positive control K3 < 1.0 bit
- **MEASUREMENT_INVALID:** Null control mean PMI > |0.1|

### Exploratory:
- Bias at N=50000 reported; does not gate primary verdict

## 9. Metrics

| Metric ID | Description | Unit |
|-----------|-------------|------|
| `k1_pmi` | I(S_next; action) at N=5000 | bits |
| `k2_pmi` | I(S_next; action | S_current) at N=5000 | bits |
| `k3_pmi` | I(S_next; action | S_current, H_K=2) at N=5000 | bits |
| `k3_minus_k2` | K3 − K2 difference | bits |
| `k2_minus_k1` | K2 − K1 difference | bits |
| `bootstrap_ci_lower` | 95% CI lower bound for K3 − K2 | bits |
| `bootstrap_ci_upper` | 95% CI upper bound for K3 − K2 | bits |
| `k2_pmi_n50000` | K2 PMI at N=50000 (exploratory) | bits |
| `positive_control_k3` | K3 PMI on 8-state deterministic SPA | bits |
| `null_control_mean` | Mean PMI under shuffled-action permutation | bits |
| `null_control_std` | Std of PMI under shuffled-action permutation | bits |

## 10. Validity Threats

1. **Deterministic strata dilution:** 31.5% deterministic strata contribute PMI=0, diluting weighted average. Same as parent. Affects absolute PMI values but not K3 − K2 comparison (both K2 and K3 are equally diluted).

2. **Estimator bias:** Laplace smoothing (alpha=1.0) may introduce small-sample bias. Same estimator as parent; K3 − K2 comparison is more robust than absolute PMI.

3. **Trajectory correlation:** Transitions within a trajectory are not independent. Bootstrap uses trajectory-block resampling to preserve dependency structure.

4. **SPA specificity:** Results apply to 12-state hash-routed SPA only. No inference to production SPAs, stochastic transitions, or browser-collected data.

5. **N=50000 computational cost:** 10x larger sample may take 5-10x longer. Acceptable for bias-scaling test.

## 11. Consequences

### Positive outcome (beyond-Markov):
- The 0.933-bit K2 PMI signal is genuinely beyond-Markov
- History representation adds predictive value for SPIDER state modeling
- Supports richer state representation in operational knowledge layer
- Narrow scope: synthetic SPA only; production generalization untested

### Negative outcome (Markov):
- Current state alone captures all action-conditioned predictability
- History conditioning adds no information on this SPA class
- State representation need not extend beyond current state for hash-routed SPAs
- May reflect SPA design (hash routing = deterministic URL mapping) rather than general Web dynamics

## 12. Analysis Plan

1. Generate N=5000 transitions from 12-state hash-routed SPA (same RNG seed as parent for reproducibility)
2. Compute K1 PMI = I(S_next; action) using Laplace-smoothed estimator
3. Compute K2 PMI = I(S_next; action | S_current) (parent replicate)
4. Compute K3 PMI = I(S_next; action | S_current, H_K=2)
5. Compute K3 − K2 difference
6. Bootstrap 95% CI for K3 − K2 using 200 trajectory-block resamples
7. Run shuffled-action null (N_SHUFFLE=1000) for K2
8. Run positive control on 8-state deterministic SPA
9. Generate N=50000 transitions for exploratory bias-scaling
10. Apply frozen decision rule
