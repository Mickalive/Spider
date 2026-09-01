# EXP-PHYSICS-33528829431 Preregistration

## Status: DESIGN — NOT YET FROZEN

---

## 1. Hypothesis

A properly instrumented browser harness can collect (S, A, S') triples from live Web interactions where:
1. No target information leaks into features
2. Site identity does not leak across train/test
3. Seeds are deterministic across processes
4. The collected data shows non-random action-conditioned transition structure above a shuffle null

## 2. State Representation

- **S (state)**: DOM accessibility tree + page URL + visible text elements + form state
- **A (action)**: {click, type, scroll, navigate} with target element selector
- **S' (next state)**: Same representation as S, after action execution

Raw observables preserved: DOM tree, accessibility structure, URL, action target, timing.

Derived variables (for analysis only): element embedding (if available), action type encoding, URL path segments.

## 3. Action Representation

- Action type: one of {click, type_text, scroll_down, scroll_up, navigate_url}
- Action target: CSS selector or accessibility role + text for click targets; input field identifier for type actions
- Action parameters: typed text content (for type actions), scroll amount, navigation URL

## 4. Target

Primary target: Can we predict S' given (S, A) better than null models?

Secondary target: Is the harness implementation valid (no leakage, proper splits, deterministic seeds)?

## 5. Sampling Policy

- **Positive control**: Synthetic navigation graph with 5 states, 3 action types, deterministic transitions. Run 50 trajectories of length 10.
- **Null control**: Random clicks on Wikipedia main page (high-entropy, unstructured navigation). Run 20 trajectories of length 10.
- **Live test**: Simple 2-3 site interaction (e.g., a news site homepage, a search engine). Run 30 trajectories of length 10.

All runs use fixed random seeds (numpy RandomState with seed=42, 43, 44 for different sites).

## 6. Unit of Analysis

Each (trajectory_id, step_index) tuple is one transition. Trajectories are the dependency unit.

## 7. Holdout

- Site-level holdout: each site's data is either entirely train or entirely test
- For this initial experiment: synthetic positive control is train, live sites are test
- No cross-site leakage in either direction

## 8. Nulls/Baselines

1. **Shuffle null**: Randomly permute S' labels within each trajectory to break action-conditioning
2. **Action-frequency null**: For each action type, predict the most common S' regardless of S
3. **First-order Markov**: Predict S' from S only, ignoring A
4. **Random policy null**: Transitions from random-click runs on unstructured pages

## 9. Primary Metric

- **Positive control**: Transition prediction accuracy (fraction of correctly predicted S' given (S, A))
- **Live test**: Comparison of action-conditioned transition entropy vs. state-only entropy vs. shuffle entropy
  - If H(S'|S,A) < H(S'|S) < H(S'|shuffle), action-conditioning provides information
  - Report entropy reduction as percentage

## 10. Expected Direction

Positive control should show near-perfect accuracy (>95%) confirming harness captures transitions correctly.

Live test: We expect some action-conditioned structure (entropy reduction > 5%) but do not claim a specific magnitude.

## 11. Uncertainty Method

- Bootstrap confidence intervals (1000 resamples) grouped by trajectory
- Bonferroni correction for multiple null comparisons (3 nulls)
- Report both raw p-values and corrected p-values

## 12. Adequacy Rule

The substrate is measurement-valid if and only if:
1. Positive control accuracy > 90%
2. No validity gate failures (leakage, contamination, seed issues)
3. Shuffle null is distinguishable from signal (p < 0.05 after correction)

## 13. Falsification/Survival Rule

- **FALSIFIED**: If positive control accuracy < 90% OR validity gates fail OR no live test shows entropy reduction above shuffle after correction
- **SURVIVES_CURRENT_TEST**: If all validity gates pass AND positive control succeeds AND at least one live test shows significant entropy reduction
- **MEASUREMENT_INVALID**: If infrastructure fails to produce usable data

## 14. Claim Scope

This experiment tests:
- C-MEAS-VALID: Can we build a measurement-valid substrate?
- C-WEB-DYNAMICS (preliminary): Is there any action-conditioned structure in Web transitions?

This experiment does NOT test:
- Cross-site transfer (C-CROSSSITE)
- Universal physical laws
- Attractors, barriers, or committors
- Generalization beyond tested sites

## 15. Validity Threats

1. **Representation loss**: Reducing DOM to accessibility tree + URL may lose relevant state. Mitigation: preserve raw DOM as artifact.
2. **Policy confounding**: Agent actions may reflect browser/agent limitations, not environment dynamics. Mitigation: explicitly label policy-dependent vs. environment observations.
3. **Small sample**: 30 trajectories per site may miss rare transitions. Mitigation: this is a substrate validation, not a final physics claim.
4. **Site selection bias**: Tested sites may not be representative. Mitigation: acknowledge limitation; future experiments expand coverage.
