# Preregistration: EXP-PHYSICS-35353016293

## Background

The parent experiment (EXP-PHYSICS-35308806126) attempted to test beyond-Markov URL-level PMI on production SPAs but failed due to anti-bot blocking (0 non-leakage transitions on all 3 sites). The parent's carry_forward explicitly states:

- **Established:** URL-level PMI (fragment-preserving) reproduces parent signal exactly: 0.187-0.204 bits unconditional K=0. K=3 conditional PMI = 0.0 bits on ALL 5 TodoMVC variants. PMI pipeline correctly detects beyond-Markov structure when present (positive control PMI=1.496-1.769 bits at K=3).
- **Rejected:** Beyond-Markov URL-level PMI on TodoMVC hash-SPAs: 0/5 variants achieve K=3 PMI > 0.05 bits. Title-aware PMI on TodoMVC: 0/5 variants have >=2 unique titles.
- **Unknown:** Whether production SPAs with >10 unique URL states, stochastic transitions, and history-based routing exhibit beyond-Markov URL-level PMI at K=3 or higher where H_K=3 does NOT determine next state. Whether locally-hosted production-like SPA simulation (>10 states, stochastic transitions, history routing) can serve as valid testbed for beyond-Markov detection while being automatable via Playwright.
- **Do not assume:** C-WEB-DYNAMICS is globally false based on TodoMVC falsification. TodoMVC's 3-4 state deterministic ceiling trivially satisfies H_K=3 determination; production SPAs with larger state spaces may not.

The current experiment tests the dominant unknown: whether a locally-hosted production-like SPA simulation (>10 states, stochastic transitions, history routing) can serve as an automatable testbed for beyond-Markov URL-level PMI detection.

## Hypothesis

**H1 (beyond-Markov):** I(url_after; action | url_before, H_K=3) > 0.05 bits on the SPA simulation, demonstrating that action provides predictive information about the next URL beyond what the previous 3 actions and current URL determine. This would indicate beyond-Markov structure required by C-WEB-DYNAMICS.

**H0 (Markov-only):** I(url_after; action | url_before, H_K=3) <= 0.05 bits on the SPA simulation, demonstrating the signal is entirely explained by Markov predictability.

## Methods

### Testbed Design

Build a locally-hosted Express.js SPA simulation with:
- **>10 unique URL states** (12 states implemented)
- **Stochastic transitions**: next state depends on previous K states (K=2) with randomized choice among possible successors
- **History-based routing**: hash-based routing where URL alone is ambiguous (multiple states share same base URL but different hash fragments)
- **Action primitives**: form_submit, button_click, js_navigate (same as TodoMVC)
- **Automatability**: Playwright can navigate without anti-bot blocking (localhost)

The simulation will be a simple finite-state machine where transition probabilities depend on the previous 2 states, creating genuine beyond-Markov structure.

### Data Collection

- Playwright browser collection with cookie/session support
- Collect 500 raw transitions in a single session (pilot validation: >=200 raw transitions required before freeze)
- Action primitives extracted from Playwright page interactions
- Session grouping: group transitions by session field to form trajectories

### Filtering

- Non-leakage filter: action_primitive != 'link_click' (link clicks are leakage per prior audit)
- Minimum 100 non-leakage transitions after filtering

### History Construction

For each transition at step t in a trajectory:
- H_K = (action_{t-K}, ..., action_{t-1}) is the sequence of K action labels preceding the current action
- For t < K, pad with START_TOKEN at the beginning

### PMI Estimation

- alpha=0 (no Laplace smoothing) for all PMI computations
- Conditional PMI: for each action-history stratum h = (url_before, H_K), compute PMI between action_t and url_after_t within the stratum, then average across strata weighted by stratum frequency
- Permutation test: 1000 within-trajectory shuffles of action labels, seed=42
- Bonferroni correction: 3 primary comparisons (K=0, K=1, K=3), alpha = 0.05/3 ≈ 0.0167

### Controls

- **Positive control:** 8-state synthetic deterministic SPA with known beyond-Markov structure (same as parent). Conditional PMI at K=3 must be >= 1.0 bits with permutation p < 0.001.
- **Null control:** Shuffled-action permutation test within trajectories. Expected mean shuffled PMI = 0.0 bits.
- **Automatability pilot:** Collect >=200 raw transitions in a single session before freeze.

## Analysis Plan

1. Compute unconditional PMI (K=0) for the SPA simulation
2. Compute conditional PMI at K=1 and K=3
3. Run permutation tests for each K level
4. Compute action-history prediction accuracy at each K level
5. Evaluate positive and null controls
6. Apply frozen decision rule

## Decision Rule

If ALL of:
1. Conditional PMI at K=3 > 0.05 bits AND Bonferroni-corrected permutation p < 0.0167
2. Positive control conditional PMI at K=3 >= 1.0 bits
3. >= 100 non-leakage transitions collected
4. Unconditional PMI at K=0 is positive (> 0.05 bits)
5. Automatability pilot passes (>=200 raw transitions in single session)

Verdict = SURVIVES_CURRENT_TEST (beyond-Markov structure demonstrated on SPA simulation)

If conditional PMI at K=3 <= 0.05 bits:
Verdict = FALSIFIED-IN-SETTING (signal is entirely Markov on this SPA simulation; no beyond-memory structure)

If controls fail or data quality insufficient:
Verdict = MEASUREMENT_INVALID

## Expected Outcomes

**Positive outcome:** Beyond-Markov URL-level PMI on SPA simulation. This elevates C-WEB-DYNAMICS from HYPOTHESIS to EXPERIMENTAL and validates locally-hosted SPA simulation as automatable testbed for future physics experiments.

**Negative outcome:** URL-level PMI is entirely Markov on SPA simulation. This narrows the claim ceiling and suggests orthogonal detection methods (DOM, accessibility tree, visual layout) or alternative claims.

**Invalid outcome:** Infrastructure failure or data quality issues. No scientific inference.

## Validity Threats

1. **Simulation fidelity:** Locally-hosted SPA may not capture genuine production SPA complexity. Mitigation: design simulation with >10 states, stochastic transitions, history routing.
2. **Action representation loss:** URL-only representation discards DOM, visual, and network information. This is acknowledged and bounded in the claim ceiling.
3. **Leakage misclassification:** Some link clicks may be non-leakage. Mitigation: conservative link_click filter per prior audit.
4. **Sample size:** 500 raw transitions may yield <100 NL transitions after filtering. Mitigation: collect extra transitions.
5. **Stochastic transitions:** SPA simulation may have stochastic transitions but H_K=3 may still determine next state. Mitigation: design simulation where transition probabilities depend on previous 2 states.
6. **Representation loss:** URL-only representation discards DOM, visual, and network information. This is acknowledged and bounded in the claim ceiling.
7. **Model/agent policy dependence:** Action primitives are extracted from Playwright, not from an LLM agent. This is bounded in the claim ceiling.
8. **Non-stationarity:** SPA simulation is deterministic and local, so non-stationarity is not a concern.
9. **Session continuity:** Browser sessions may not capture genuine user sessions. Mitigation: use separate browser contexts with distinct cookies.

## Representation Loss

- URL-only representation discards DOM, visual, and network information
- Action primitives are categorical (form_submit, button_click, etc.) and discard action parameters
- Session grouping by cookie may not capture genuine user sessions
- Link click filter may remove non-leakage transitions
- Bonferroni correction for 3 tests is conservative

## Parent Handoff Reference

Parent: EXP-PHYSICS-35308806126 (handoff.json sha256 e33d732263fae685d3ac3f6629f1f87f50f595045a9184b246ccc3021ce23371)

Carry forward from parent:
- **Established:** URL-level PMI (fragment-preserving) reproduces parent signal exactly: 0.187-0.204 bits unconditional K=0. K=3 conditional PMI = 0.0 bits on ALL 5 TodoMVC variants. PMI pipeline correctly detects beyond-Markov structure when present (positive control PMI=1.496-1.769 bits at K=3).
- **Rejected:** Beyond-Markov URL-level PMI on TodoMVC hash-SPAs: 0/5 variants achieve K=3 PMI > 0.05 bits. Title-aware PMI on TodoMVC: 0/5 variants have >=2 unique titles.
- **Unknown:** Whether production SPAs with >10 unique URL states, stochastic transitions, and history-based routing exhibit beyond-Markov URL-level PMI at K=3 or higher where H_K=3 does NOT determine next state. Whether locally-hosted production-like SPA simulation (>10 states, stochastic transitions, history routing) can serve as valid testbed for beyond-Markov detection while being automatable via Playwright.
- **Do not assume:** C-WEB-DYNAMICS is globally false based on TodoMVC falsification. TodoMVC's 3-4 state deterministic ceiling trivially satisfies H_K=3 determination; production SPAs with larger state spaces may not.

## Stable Metric/Control Identities

- **Primary metric:** conditional_pmi_k3 (bits)
- **Baseline metrics:** unconditional_pmi_k0, conditional_pmi_k1, prediction_accuracy_by_k
- **Positive control:** POSITIVE_CONTROL_SYNTHETIC_SPA
- **Null control:** NULL_CONTROL_SHUFFLED_ACTIONS
- **Automatability pilot:** AUTOMATABILITY_PILOT (>=200 raw transitions)
- **Decision threshold:** 0.05 bits, Bonferroni alpha = 0.0167
- **Minimum NL transitions:** 100
- **Minimum raw transitions for pilot:** 200