# Preregistration: EXP-PHYSICS-35375596894

## Background

The parent experiment (EXP-PHYSICS-35353016293) tested beyond-Markov URL-level PMI on a 12-state SPA simulation with hash-based routing. Key findings:

- **K=3 action-history PMI = 0.048 bits** — fails the 0.05 threshold by 0.0015 bits (3% margin)
- **Environment HAS beyond-Markov structure**: 254/565 (45%) K=3 strata are stochastic (multiple successors per determinism_check_k3)
- **Estimator severely underpowered**: only 8/565 strata (1.4%) have >=5 records at N=1000; 557 strata skipped
- **Null control biased**: mean shuffled PMI = 0.054 > 3*0.017 = 0.051, indicating permutation bias for hash-routed SPA
- **In-memory simulation, not Playwright**: automatability pilot validated Python loop, not browser session

The parent handoff (sha256 b940d73598dadfe945f5c5bd48ea0c0fa721750fcd94718329851a64ae6ebe66) identified three orthogonal improvements:

1. **N>=5000** to achieve mean >=5 obs/stratum for >50% of K3 strata (audit V1 sparsity fix)
2. **State-history conditioning** (prev URL states instead of action-history) to directly test SHA256(prev1:prev2) dependence (audit V5 identifiability fix)
3. **Playwright browser automation** to validate automatable testbed (audit V3)

The current experiment tests improvements (1) and (2) together — both purely computational — while adding (3) as a diagnostic automatability check.

### Parent carry_forward

- **Established:** URL-level PMI (fragment-preserving) reproduces parent signal exactly: unconditional K=0 PMI = 1.441 bits (p=0.001, d=58.5) on 12-state SPA simulation. K=1 conditional PMI = 1.509 bits (p=0.001, d=24.1). Strong state-conditioned predictability confirmed. PMI pipeline correctly detects beyond-Markov structure when present: positive control K3 PMI = 1.769 bits (p=0.001, d=103.2). 12-state SPA has beyond-Markov structure BY CONSTRUCTION: 254/565 (45%) K=3 strata are stochastic. Fragment-stripping normalization destroys all state information.
- **Rejected:** Beyond-Markov URL-level PMI on TodoMVC hash-SPAs: 0/5 variants achieve K3 PMI > 0.05 bits. Title-aware PMI on TodoMVC: 0/5 variants have >=2 unique titles. K3 PMI on 12-state SPA via action-history conditioning at N=1000: 0.04848 bits <= 0.05 threshold.
- **Unknown:** Whether N>=5000 with state-history conditioning detects beyond-Markov PMI. Whether Playwright browser automation yields same transition distribution. Whether permutation null bias is intrinsic to hash-routed SPA. Whether production SPAs exhibit beyond-Markov URL-level PMI.
- **Do not assume:** C-WEB-DYNAMICS is globally false. The environment HAS beyond-Markov structure; the estimator failed to detect it. URL-level PMI is not useless (K0=1.44, K1=1.51 are highly significant). The PMI pipeline is not broken (positive control validates it).

## Hypothesis

**H1 (state-history beyond-Markov):** I(url_after; action | url_before, prev_state_1, prev_state_2) > 0.05 bits at K=2 (state-history conditioning) with N=5000 on the 12-state SPA simulation, demonstrating that previous URL states provide predictive information about the next URL beyond what the current URL alone determines.

**H0 (state-history Markov-only):** I(url_after; action | url_before, prev_state_1, prev_state_2) <= 0.05 bits at K=2, demonstrating the signal is entirely explained by first-order Markov predictability.

**Rationale for state-history over action-history:** The SPA transition function `choose_next(prev1, prev2, current, action)` depends on the previous two URL states, not on the action history. With 12 states and 4 actions, action-history H_K=3 cannot uniquely identify the state history — multiple state sequences produce the same action sequence. Directly conditioning on (prev1, prev2) is the causal parents of the transition, making the identifiability argument stronger and the test more powerful.

## Methods

### Testbed

Same 12-state SPA simulation as parent (EXP-PHYSICS-35353016293):
- 12 unique URL states with hash-based routing
- 4 action primitives: form_submit, button_click, js_navigate, menu_select
- Stochastic transitions: choose_next(prev1, prev2, current, action) selects from 4 candidates via SHA256(prev1:prev2:current:action) mod 4
- In-memory simulation (same as parent — Playwright automatability tested separately)

### Data Collection

- N=5000 transitions from 12-state SPA simulation
- 50 sessions of 100 steps each (same SPA, fresh session per 100 steps)
- Same seed mechanism as parent for reproducibility

### State-History Construction

For each transition at step t in a trajectory:
- **State-history H_K^state** = (url_{t-K}, ..., url_{t-1}) is the sequence of K URL states preceding the current URL
- For t < K, pad with START_TOKEN at the beginning
- K=2: H_2^state = (url_{t-2}, url_{t-1}) — tests dependence on previous 2 states (the causal parents)
- K=3: H_3^state = (url_{t-3}, url_{t-2}, url_{t-1}) — tests dependence on previous 3 states

### Action-History Construction (Comparison Baseline)

- **Action-history H_K^action** = (action_{t-K}, ..., action_{t-1}) — same as parent
- K=3 only — comparison baseline for sample-size confound control
- At N=5000, this directly tests whether the parent's N=1000 sparsity was the sole bottleneck

### PMI Estimation

- alpha=0 (no Laplace smoothing) for all PMI computations
- MIN_STRATUM_SIZE=5 (same as parent)
- Conditional PMI: for each stratum h = (url_before, H_K), compute PMI between action_t and url_after_t within the stratum, then average across strata weighted by stratum frequency
- Permutation test: 1000 trajectory-level block permutations, seed=42
  - Block permutation: shuffle (url_before, url_after) pairs within each trajectory
  - This preserves trajectory structure while breaking state transition dependencies
  - Addresses parent V2_null_control_bias where action-label shuffling preserved implicit state information
- Bonferroni correction: 3 confirmatory tests (state-history K=2, K=3, action-history K=3 comparison), alpha = 0.05/3 = 0.0167

### Controls

- **Positive control:** 8-state synthetic deterministic SPA with known beyond-Markov structure (same as parent). N=5000. K=3 PMI must be >= 1.0 bits with permutation p < 0.001.
- **Null control:** Trajectory-level block permutation. Expected mean PMI ~0 bits.
- **Automatability check:** 200 Playwright browser transitions on spa_server.js (diagnostic only, not part of primary decision rule). Validates that the SPA testbed is automatable via browser.

### Derived Metrics

For each conditioning strategy (state-history K=2, K=3; action-history K=3):
- PMI bits
- Permutation p-value
- Null mean and standard deviation
- Effect size (Cohen's d)
- Prediction accuracy
- Number of strata total, used, skipped (small), skipped (zero variance)

Additional diagnostics:
- Determinism check at K=2 and K=3 state-history (fraction of stochastic strata)
- Per-stratum PMI distribution for stochastic strata only (does the signal come from stochastic strata?)
- Stratum coverage at N=5000 (fraction of strata with >=5 records)

## Analysis Plan

1. Collect N=5000 transitions from 12-state SPA simulation
2. Run Playwright automatability check (200 transitions, diagnostic)
3. Compute unconditional PMI (K=0) at N=5000
4. Compute state-history conditional PMI at K=1, K=2, K=3
5. Compute action-history conditional PMI at K=3 (comparison baseline)
6. Run trajectory-level block permutation tests for each K level
7. Compute determinism check at K=2 and K=3 state-history
8. Evaluate positive and null controls
9. Compare state-history K=2 PMI to parent action-history K=3 PMI at N=1000
10. Apply frozen decision rule

## Decision Rule

**SURVIVES_CURRENT_TEST** if ALL:
1. State-history K=2 conditional PMI > 0.05 bits AND Bonferroni-corrected permutation p < 0.0167
2. Positive control passes (K=3 PMI >= 1.0 bits, p < 0.001)
3. >= 5000 transitions collected
4. Null control passes (mean PMI < 3*std)

**FALSIFIED-IN-SETTING** if:
- State-history K=2 PMI <= 0.05 bits (primary)
- OR both state-history K=2 AND K=3 PMI <= 0.05 bits (secondary — rules out that K=2 was the wrong history length)

**MEASUREMENT_INVALID** if:
- Controls fail or data quality insufficient
- < 5000 transitions collected
- Pipeline errors

**Note:** The action-history K=3 comparison at N=5000 is exploratory. It controls for the sample-size confound (parent had N=1000) but is not part of the primary SURVIVES/FALSIFIED decision. A positive action-history K=3 at N=5000 would indicate the parent's failure was purely due to sparsity. A negative action-history K=3 at N=5000 would indicate the parent's failure was due to both sparsity AND action-history proxy limitations.

## Expected Outcomes

**Outcome A (state-history K=2 > 0.05, action-history K=3 > 0.05):** Both improvements work. Beyond-Markov signal is real and detectable. C-WEB-DYNAMICS advances. The parent's failure was due to sparsity AND conditioning strategy.

**Outcome B (state-history K=2 > 0.05, action-history K=3 <= 0.05):** State-history conditioning is necessary. Beyond-Markov signal is real but requires causal-parent conditioning. C-WEB-DYNAMICS advances with narrowed ceiling to state-history conditioning only.

**Outcome C (state-history K=2 <= 0.05, action-history K=3 > 0.05):** Sample size was sufficient but state-history conditioning introduced noise. The parent's failure was purely due to sparsity. Action-history is adequate. C-WEB-DYNAMICS advances with action-history conditioning.

**Outcome D (both <= 0.05):** Neither improvement suffices. Beyond-Markov URL-level PMI is not detectable on 12-state hash-routed SPAs regardless of conditioning strategy or N<=5000. Claim ceiling narrows definitively. Research should consider richer state representations or alternative claims.

## Validity Threats

1. **Stratum explosion at K=3 state-history:** 12^4 = 20736 possible strata at K=3. At N=5000, mean 0.24 obs/stratum — almost all strata will be skipped. This is expected; K=3 state-history is exploratory. The primary test is K=2 (12^3 = 1728 strata, mean 2.9 obs/stratum at N=5000).
2. **Deterministic vs stochastic strata dilution:** Same as parent — deterministic strata (PMI=0 by construction) dilute the weighted average. This is addressed by reporting per-stratum diagnostics for stochastic strata only.
3. **In-memory simulation fidelity:** Same as parent. The transition function is identical whether run in-memory or via Playwright. Playwright automatability is tested separately as diagnostic.
4. **Trajectory-level block permutation validity:** Block permutation preserves within-trajectory structure. If trajectories are short (100 steps), blocks may not capture long-range dependencies. Mitigation: 50 trajectories of 100 steps each.
5. **Multiple testing:** 3 confirmatory tests with Bonferroni correction. State-history K=2 is the primary test; K=3 and action-history K=3 are secondary/comparison.

## Representation Loss

- URL-only state representation discards DOM, visual, network, and accessibility information
- Action primitives are categorical and discard action parameters (URLs, form values)
- Session grouping by fresh context may not capture genuine user sessions
- In-memory simulation does not test browser-specific behavior (fragment handling, history API, anti-bot)
- Bonferroni correction for 3 tests is conservative

## Parent Handoff Reference

Parent: EXP-PHYSICS-35353016293 (handoff.json sha256 b940d73598dadfe945f5c5bd48ea0c0fa721750fcd94718329851a64ae6ebe66)

Carry forward preserved exactly from parent handoff (see Background section above).

## Stable Metric/Control Identities

- **Primary metric:** state_history_pmi_k2 (bits)
- **Secondary metrics:** state_history_pmi_k3, action_history_pmi_k3, unconditional_pmi_k0, state_history_pmi_k1
- **Positive control:** POSITIVE_CONTROL_SYNTHETIC_SPA (N=5000, K=3 PMI >= 1.0 bits)
- **Null control:** NULL_CONTROL_BLOCK_PERMUTATION (trajectory-level block shuffle, expected mean ~0)
- **Automatability check:** AUTOMATABILITY_PILOT_BROWSER (>=200 Playwright transitions, diagnostic)
- **Decision threshold:** 0.05 bits, Bonferroni alpha = 0.0167 (3 tests)
- **Minimum transitions:** 5000
- **Permutation count:** 1000, seed=42
- **MIN_STRATUM_SIZE:** 5
