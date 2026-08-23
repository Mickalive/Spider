# PHYSICS LEDGER

## WP-003 (2026-08-23) — Website-holdout universality of transition structure
- **Hypothesis**: mechanics-only state features Z transfer across websites for
  predicting next-action-class beyond strong nulls.
- **Operational definition**: LOO-website balanced accuracy, softmax vs
  frequency/Markov/NN/shuffle nulls; frozen prereg before collection.
- **Dataset**: 557 usable transitions, 7 live sites, uniform random policy,
  event-driven snapshots. Manifest committed.
- **Falsifier**: CI of mean diff ≤0 or wins <4/7 → FALSIFIED.
- **Result**: mean Δ(M1 − best null) = −0.348, CI [−0.363,−0.333], 0/7 wins.
- **Verdict: FALSIFIED** (representation family Z, action-class target,
  unbiased-policy regime).
- **Alternative explanations kept alive**: (a) N2 dominance may be a sampler
  artifact — goal-directed policy is the control; (b) state-level phenomena
  (attractors/barriers/timing) untested by this design.
- **Next discriminating test**: WP-004 committor/barrier on login regimes;
  WP-003b target-B (next-page structure); policy-sensitivity rerun.

## Prior carried from earlier program (not reproduced this run)
- Mind2Web reconstruction: operation inventory ≠ causal mechanics (§33).
- WP-001: +0.05 dim-acc over shuffle, unverified post-state.
- WP-002B: true S,A,S' data; rule ≈ NN > shuffle in-distribution; no site
  holdout. WP-003 now supplies the missing website-holdout test and the
  signal does not survive it against trivial nulls.

## Measurement infrastructure status
- Collector hardened after two invalid/degraded episodes (documented in
  wp003_report.md). Raw snapshots retained in /tmp only (policy §40);
  manifests + compact features committed.
