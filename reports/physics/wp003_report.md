# WP-003 REPORT — Website-Holdout Universality of Transition Structure

**AUDIT VERDICT: MEASUREMENT_INVALID.**

Date of original run: 2026-08-23. Historical raw result artifact:
`results/physics/wp003_results.json`.

## Why the original verdict is invalid

The original report declared `FALSIFIED` because a global first-order Markov
null N2 appeared to dominate mechanics-only state features on every website.
Post-run audit found a fatal target-leakage bug in the collector:

- `target_action` was defined as the first action of the **current** transition;
- `prev_action_label` was defined as the last action of that **same** transition;
- for single-action transitions, which dominate the corpus,
  `prev_action_label == target_action` by construction.

Therefore N2 often received the answer it was supposed to predict. Its near-
perfect cross-site scores (including 1.000 on some folds) are not evidence of
a universal Web regularity.

The analysis also labelled its uncertainty interval a bootstrap, but the
implementation added `rng.normal(0, 0.02)` noise around fold-level point
estimates rather than nonparametrically resampling paired predictions or
independent trajectories. The reported CI `[-0.363, -0.333]` is therefore not
a valid bootstrap confidence interval.

A third reproducibility defect was found: the collector used Python's salted
`hash(site)` to perturb the random seed. Because Python hash randomization can
change between processes, the supposedly frozen seed did not uniquely define
identical walks across fresh runners.

## Consequence

The historical numerical output is preserved for provenance but must not be
used as scientific evidence. In particular, the following claims are
**withdrawn**:

- `WP-003 = FALSIFIED`;
- `last-action -> next-action transfers universally`;
- `mean Δ = -0.348` as a valid model-vs-null effect;
- the reported 95% interval as a valid uncertainty estimate.

The correct status is:

> **MEASUREMENT_INVALID — target leakage + invalid uncertainty estimator.**

This does **not** count as evidence for or against the existence of effective
Web physics.

## What remains useful from run 1

- the live-site collector and browser hardening work;
- the mechanics-only feature family as one candidate representation;
- website-holdout as the correct generalization direction;
- the habit of invalidating failed measurement episodes rather than hiding
  them;
- the secondary idea of predicting environment response/next-state structure,
  which is conceptually closer to `P(s' | s, a)` than predicting the crawler's
  next action.

## Required correction before any new verdict

1. `prev_action_label` must come from transition `t-1`, never from transition
   `t`.
2. Every row must carry `trajectory_id` and `step_id` so resampling can respect
   temporal dependence.
3. The seed must be deterministic across processes/runners.
4. Add explicit anti-leak invariants before analysis.
5. Uncertainty must use a real grouped/trajectory bootstrap or another
   justified estimator.
6. The primary physics target should move toward environment dynamics,
   especially `P(s_{t+1} | s_t, a_t)`, not merely agent-policy action choice.
7. WP-003B must be rerun from a clean corrected dataset; the historical
   `wp003b_targetB.json` is exploratory only and cannot rescue WP-003.
8. Do not launch WP-004 committor/barrier measurement until an identifiability
   gate shows the available data contain enough independent revisits/branching
   to estimate a policy-robust committor.
