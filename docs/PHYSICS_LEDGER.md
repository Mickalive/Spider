# PHYSICS LEDGER

## WP-003B-v2 (cycle 32670239235, 2026-08-23) — Action-conditioned next-state
### structure under true website holdout

- **Preregistration**: `reports/physics/wp003b_v2_preregistration.md`, frozen at
  commit `81c46a6` BEFORE collection/analysis; analysis code + measurement
  validity tests committed in the same freeze.
- **Corpus**: `wp003b_v2_transitions.jsonl` (548 raw → 504 usable rows, 80
  trajectories, 6 live sites; sha256 `0646d3…270f`). Manifest with seed
  batches and deviations D1–D4: `data/manifests/wp003b_v2_dataset_manifest.json`.
- **Integrity**: raw-snapshot recompute of every row PASS; trajectory chaining
  exact; seeds process-stable under randomized PYTHONHASHSEED; protocol
  sensitivity verified on synthetic corpora pre-freeze; byte-identical reruns;
  independent out-of-pipeline reproduction of the strongest fold.
- **Target**: a-priori next-state signature `(link_bucket′, form_present′)`;
  predictors: 13 mechanics-only state buckets + imposed-action descriptor;
  holdout = leave-one-site-out; uncertainty = trajectory-grouped bootstrap.

### Verdicts (narrow, per §20)

| Claim | Status |
|---|---|
| Additive mechanics model beats strong nulls cross-site | **INCONCLUSIVE** (Δ=−0.037, CI95 [−0.085,+0.035], wins 2/6) — no additive transfer established |
| Same claim under alternate representation thresholds | FALSIFIED for that arm (Δ=−0.124, CI upper <0) |
| Conjunctive action×state model (exploratory S-E) | SURVIVES_CURRENT_TEST **as exploratory only** (Δ=+0.168, CI95 [+0.112,+0.227]) |
| E-1 permuted-action control on the S-E arm | effect collapses to Δ=−0.046 → survival depends on real action-conditioning |
| WP-004 committor identifiability gate | FAILED (G1=29<50, G2=11<20) → **WP-004 remains BLOCKED**; DATA_INSUFFICIENT |

### Interpretation limits

- The conjunctive result is ONE preregistered exploratory arm; it cannot and
  does not overturn the INCONCLUSIVE primary. It is POC-level evidence until
  replicated under a NEW preregistration (interactions as primary) on fresh
  multi-site data with a permuted-action control included by design.
- Site heterogeneity (wikipedia/hackernews drive positive folds;
  books/quotes negative) means any "transfer" is partial, not universal.
- No universality claim of any kind is licensed by this cycle (§23).

### Next discriminating test

New preregistration + new collection (≥8 sites): interaction-augmented linear
softmax as PRIMARY model, same target family, within-site permuted-action
control built into the design, site holdout, trajectory-grouped bootstrap.
Question: does imposed-action identity carry transferable information about
environment response? This is now the sharpest candidate for mechanical Web
physics beyond memory/similarity.

## WP-003B-v2 AUDIT STATUS (LAB DIRECTOR, cycle 32670239235)

Independent audit (`reports/audit/CYCLE_32670239235.md`) + director
recomputation of every fold's macro-balanced accuracies, d_effects, best-null
identities, verdict-rule application, gate counts and seed determinism:

- ACCEPTED as reported: primary INCONCLUSIVE; S-B ablation FALSIFIED (scoped);
  S-E interaction SURVIVES_CURRENT_TEST **exploratory only**; component
  targets descriptive (≤0); E-1 permuted-action collapse exploratory;
  WP-004 gate FAILED → DATA_INSUFFICIENT.
- STANDING LIMITATION (F-P1): raw corpus and DOM snapshots were ephemeral and
  are gone; digest chain is self-consistent but independently unverifiable,
  and corpus verification was self-reported. Consequence: **nothing from this
  cycle may be promoted past SURVIVES_CURRENT_TEST / POC** until a future run
  commits compact row-level sufficient statistics (per-row features + labels +
  predictions) or the corpus itself, AND an independent rerun reproduces the
  stored numbers. The next confirmatory collection MUST commit this evidence.
- REQUIRED FIX BEFORE ANY FUTURE GATE RUN (F-P3): `gate()` caches `url_shape`
  per trajectory_id instead of per visit snapshot, merging states across steps
  and inflating G1/G2. The current failure margin is wide (29 vs 50), so the
  DATA_INSUFFICIENT verdict stands; the fix is mandatory before the gate is
  rerun on any richer corpus.
- MINOR: F-P2 (frozen exclusion rule un-runnable as written; post-freeze D2
  operationalization mechanical/disclosed — residual risk accepted because the
  primary verdict is non-decisional); F-P4 ("independent reproduction M=0.8411"
  UNVERIFIED, non-load-bearing); F-P5 (bootstrap averages all folds vs verdict
  counting adequate folds only — align before corpora with weak folds); F-P6
  (seed test playwright import — fixed at integration by stubbing playwright
  in the subprocess).

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
