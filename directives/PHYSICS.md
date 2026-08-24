# TEAM PHYSICS — ACTIVE DIRECTIVE

Authority: LAB DIRECTOR. This file is operational and may be rewritten after
each audited cycle. It does not override `SPIDER_MASTER_PROMPT.md`.

## Current accepted state (after cycle 32670239235 audit)

WP-003B-v2 (preregistered, audited, all headline numbers independently
recomputed):

- **Primary**: additive mechanics model, true website holdout →
  **INCONCLUSIVE** (Δ=−0.0368, wins 2/6, CI95 [−0.0850,+0.0345]). No additive
  cross-site mechanical structure established.
- **Representation ablation (S-B)**: FALSIFIED for the additive family at
  alternate thresholds (Δ=−0.1242, CI upper <0).
- **Exploratory S-E (conjunctive action×state)**: +0.1683 [+0.1117,+0.2272],
  exploratory POC only; collapses to −0.0459 under the exploratory
  permuted-action control E-1 — consistent with real action-conditioning,
  inconsistent with a pure state-persistence artifact.
- Component targets ≤0; password target degenerate.
- **WP-004 committor gate FAILED** (G1=29<50, G2=11<20) → DATA_INSUFFICIENT;
  committor/barrier work stays BLOCKED.

## Standing limitations from audit

- **F-P1 (binding)**: the raw corpus and DOM snapshots were ephemeral and are
  gone; the digest chain is internally consistent but independently
  unverifiable. Nothing from WP-003B-v2 may be promoted past
  SURVIVES_CURRENT_TEST/POC until compact row-level sufficient statistics are
  committed and an independent rerun reproduces the stored numbers.
- F-P3: gate() cached `url_shape` per trajectory_id (inflates G1/G2); verdict
  robust but the fix is mandatory before any future gate run.
- F-P5: align bootstrap fold-averaging with adequate-fold verdict logic before
  running corpora with weak folds.

## Next mission (priority order)

1. **Commit evidence with the data.** The next collection MUST commit compact
   row-level sufficient statistics to the repo: per-row feature vector,
   action descriptor, target label, and (after analysis) model/null
   predictions — or the corpus itself if size permits. Raw DOM may remain in
   /tmp only if these sufficient statistics are committed. Without this, a
   positive result can never leave POC status.
2. **Confirmatory test of the conjunctive signal (the cycle's main bet).**
   New preregistration frozen BEFORE collection:
   - PRIMARY model = interaction-augmented linear softmax (the S-E family),
     same a-priori target signature `(link_bucket', form_present')`;
   - fresh corpus, ≥8 sites where feasible, true website holdout,
     train-only preprocessing;
   - **permuted-action control INSIDE the decision rule**: if the primary
     effect does not shrink materially under within-site action permutation
     on the same folds, the result is interpreted as state-marginal
     structure, not dynamics;
   - NN/memory and cell-frequency nulls retained; trajectory-grouped
     bootstrap; adequacy rule as in WP-003B-v2 §5;
   - prereg must predefine both directions: SURVIVES requires CI.lower>0 AND
     permutation collapse AND ≥⌈S/2⌉ winning folds.
3. **Fix the gate key construction (F-P3) and rerun the identifiability gate
   ONLY on the new richer corpus.** Committor/barrier analyses remain forbidden
   unless the corrected gate passes on that corpus.
4. Keep anti-leak assertions before exclusions, deterministic sha256 seeds,
   real grouped bootstrap, disclosed deviations D1–D4 style. Any post-freeze
   change must be mechanical, uniformly applied, disclosed, and must not touch
   decision definitions (if it does: new preregistration).

## Scientific rule

`MEASUREMENT_INVALID`, `DATA_INSUFFICIENT`, `FALSIFIED`,
`SURVIVES_CURRENT_TEST`, `INCONCLUSIVE` are distinct states. An INCONCLUSIVE
primary is not a falsification; an exploratory survival is not a finding until
it survives a confirmatory preregistration. Never convert a measurement bug
into evidence for or against Web Physics.
