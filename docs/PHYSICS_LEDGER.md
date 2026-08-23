# PHYSICS LEDGER

## WP-003 (2026-08-23) — Website-holdout transition structure

- **Original hypothesis**: mechanics-only state features Z transfer across
  websites for predicting next-action-class beyond strong nulls.
- **Historical dataset**: 557 transitions, 7 live sites.
- **Original reported verdict**: `FALSIFIED`.
- **POST-RUN AUDIT VERDICT: `MEASUREMENT_INVALID`.**

### Fatal defects found

1. `prev_action_label` was assigned from the current transition's final action,
   while `target_action` was the current transition's first action. For the
   dominant one-action transitions the Markov baseline therefore received the
   target itself.
2. The reported confidence interval was not a nonparametric paired bootstrap;
   the code added Gaussian noise to fold-level point estimates.
3. The supposedly frozen random seed used Python `hash(site)`, which is salted
   across fresh processes and therefore not reproducible.

### Consequence

The historical Δ=-0.348, 0/7 fold result and "universal last-action→next-action"
claim are retained only as invalidated provenance. They provide **no evidence
for or against Web Physics**.

### Corrected infrastructure now present

- deterministic site seed offsets;
- independent `trajectory_id` and `step_id`;
- true `prev_action_label = action(t-1)`;
- hard pre-analysis anti-leak assertions;
- trajectory-grouped bootstrap;
- corrected WP-003B family conditioned on `(s_t, a_t)` to predict coarse
  `s_{t+1}` structure.

These corrections require a **new dataset and new result files**. Historical
JSON files are never silently overwritten.

## WP-004 gate

Committor/barrier work is **BLOCKED pending identifiability**. Before estimating
`q(s)=P(reach B before A | s)`, Team Physics must show enough independent
restarts/revisits/branching from comparable states and a null separating a
dynamical barrier from a graph bottleneck. Failure of this gate yields
`DATA_INSUFFICIENT`, not a physics result.

## Prior carried from earlier program

- Mind2Web reconstruction: operation inventory != causal mechanics.
- WP-001: ~+0.05 dimension-accuracy over shuffle, but post-state proxy was not
  a verified next state.
- WP-002B: true `(S,A,S')`; rule ~ NN > shuffle in-distribution; no website
  holdout claim.

WP-003 does not supersede WP-002B because WP-003's historical measurement is
invalid.
