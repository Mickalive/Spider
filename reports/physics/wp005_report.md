# WP-005 REPORT — Fine-Grained Action-Conditioned Response Transfer Under Website Holdout

**Verdict: `FALSIFIED`** — on BOTH co-primary fine-grained targets, exactly as
frozen in `reports/physics/wp005_preregistration.md` (rules §7 applied once by
`physics/run_wp005.py`).

Cycle: Physics lane cycle 2, GitHub run 32689298051. Dataset: `wp005_v1`
(875 collected / 769 confirmed atomic transitions, 9 live sites, 2 new).
Results: `results/physics/wp005_results.json`; independent verification:
`results/physics/wp005_verification.json`; compact data committed at
`data/physics/wp005_transitions.jsonl.gz`
(sha256 `97e406ee48396103…`, manifest
`data/manifests/wp005_dataset_manifest.json`).

Per the Director's pre-declared decision horizon (`directives/PHYSICS.md`),
this two-level negative closes the cross-site universality question at both
tested granularities under uniform random-walk sampling. The lane stops
unless a genuinely different measurement instrument is proposed.

## 1. What was tested

Primary object per constitution §16:

    P(fine(s_{t+1}) | Z(s_t), a_t)

with ATOMIC single-action transitions (collector v3 resolves the cycle-1
attribution-fidelity finding by construction), true leave-one-site-out
holdout over 9 sites, and train-fold-only fitting of every fitted object
(fixed structural Z one-hot; per-fold action vocabularies).

Co-primary fine-grained targets (frozen before data):

- **T1_url_shape_transition**: host-change × path-depth-delta × query-delta
  pattern of the transition URL (13 classes observed; inert class
  `H1|D0|Qzero` = 74% of confirmed rows).
- **T2_dom_diff_signature**: DOM digest-change pattern × element-count delta
  bucket (6 classes; most frequent `DOM1|Ezero` 38%).

Mandatory baseline structure separating three explanations:
N_ACTION_ONLY (generic action semantics), N_PERSIST_FINE (training-free
inertness), N_NN_Z / N_NN_ZA (site-local memory), paired M_S ablation,
N_FREQ reported (degenerate, never strong), S0 shuffle chance scale.

## 2. Result

| target | mean D | fold wins | rand. p (≤0.025) | M_SA>M_S folds | status |
|---|---|---|---|---|---|
| T1_url_shape_transition | **−0.0432** | **1/9** | 0.898 | 2/9 | FALSIFIED |
| T2_dom_diff_signature   | **−0.0497** | **4/9** | 0.270 | 7/9 | FALSIFIED |

Overall verdict rule (§7): any SURVIVES → SURVIVES_CURRENT_TEST; both
FALSIFIED → **FALSIFIED**. Applied outcome: FALSIFIED.

Per-fold D_f vs the best strong null (macro balanced accuracy):

- T1: books −0.189, gutenberg −0.081, hackernews +0.000, internet −0.053,
  openlibrary +0.041, parabank −0.084, quotes −0.023, saucedemo +0.000,
  wikipedia +0.000.
- T2: books −0.058, gutenberg +0.104, hackernews +0.030, internet −0.409,
  openlibrary +0.020, parabank +0.109, quotes −0.085, saucedemo +0.000,
  wikipedia −0.159.

Coverage ≥ 0.90 on all scored folds (gutenberg 0.90, others 1.00);
action_coverage_scored = 1.00 everywhere (atomic primitive labels are
universally shared across sites — no unseen-action rows). Harsh variant
(unscoreable as errors) reported per fold in the results JSON; it never
reverses any comparison direction materially.

## 3. Interpretation (bounded)

1. **No transferable fine-grained environment response.** A state+action
   predictor trained on 8 sites does not beat site-local memory
   (NN_Z/NN_ZA), training-free inertness persistence, or even ACTION-ONLY
   generic semantics on held-out sites at either finer granularity.
2. **ACTION_ONLY is a strong null here** — best null on 3/9 T1 folds and
   3/9 T2 folds (e.g., internet T2 0.909 vs M_SA 0.500): much of the
   apparent "response predictability" is what the action type does to ANY
   page, not state-dependent physics.
3. **The T2 ablation asymmetry is informative**: M_SA > M_S on 7/9 folds
   cross-site (and in-site below) yet M_SA still loses to memory/action-only
   nulls — action-conditioned signal exists in fitting but its cross-site
   component is not competitive with retrieval.
4. Combined with cycle 1 (coarse structural family falsified), the accepted
   answer to the lane's universality question is negative at both tested
   granularities under uniform random-walk sampling with this instrument.

Bounded wording (prereg §8): these conclusions hold for THIS representation
family × THESE two fine-grained targets × uniform random-walk sampling ×
these nine websites. Nothing here proves web dynamics lack structure in
general; richer instruments (deliberate restart/revisit designs, matched
state sampling, within-site regime models) remain untested and would need
their own preregistrations.

## 4. Exploratory localization (frozen S10, cannot rescue primary)

In-site trajectory-split diagnostic mirrors cycle 1 at finer grain:
signal EXISTS within a site but is persistence + site-local retrieval:

- T2 in-site: M_SA beats PERSIST_FINE on every site with adequate splits;
  vs NN_ZA the edge is ≤ +0.088 (books) and often negative (parabank −0.047,
  saucedemo −0.029).
- T1 in-site: M_SA ≈ NN_ZA (books +0.000, gutenberg +0.008, quotes −0.061).

## 5. Descriptive findings worth keeping

- **Degenerate folds disclosed**: saucedemo T1 (single scored class → all
  predictors 1.000) and wikipedia T1 (uniform 0.333 for all predictors)
  satisfy frozen adequacy but carry zero discrimination; both contribute
  D_f = 0. Descriptive robustness check WITHOUT changing the frozen rule:
  excluding them leaves T1 wins 1/7, mean_D still negative, T2 wins 4/7 <
  majority 5 — verdict unchanged.
- Class imbalance is severe for T1 (74% inert class; rarest classes n=1–2)
  and moderate for T2 (max/min = 290/1). Macro balanced accuracy + coverage +
  harsh variant + per-class tables reported per prereg §5/S9.
- internet/hackernews walks again terminate early under logged-out
  conditions (27/25 collected rows); real environment response, consistent
  with cycle 1.
- openlibrary execution failures persist (36/120 confirmed), matching
  cycle-1 behavior; excluded rows are counted, never silently dropped.

## 6. Measurement integrity record

- Freeze discipline: prereg + collector v3 + analysis + verifier committed
  together at `d81aee5` (2026-08-24T04:47:56Z); dataset commit `9e19461`
  after collection; results commit `7c9b395`. Row timestamps all postdate
  the freeze commit. This time the provenance sentence is TRUE by
  construction (cycle-1 audit finding C6 not repeated).
- All validity gates PASS (G1 identity/alignment/atomicity, G2 execution
  filter 769/875, G2b no post-state inputs, G3 site disjointness asserted,
  G4 sha256 seeds, G6 support/coverage, G8 atomicity, G9 stored-target ==
  recomputed-from-raw on 100% of rows).
- Independent verifier (separate code path, own target re-derivation):
  D_f recompute matches bit-exact on all 18 target-folds; train-fold-only
  action vocabularies verified (P6); seed-formula integrity PASS (P4);
  softmax sanity PASS (P5); label-shuffle/random-feature collapse probes
  behave (P1/P2); verdict arithmetic reproduces from stored artifacts (P8).
- Methods gate 1 (P3 anomaly) resolved BEFORE this experiment:
  `results/physics/p3_bootstrap_diagnosis.json` — the cycle-1 grouped<naive
  width inversion is a nonlinear-statistic effect (class-composition lottery
  at ~8 clusters), reproduced bit-exact and bounded; primary inference here
  is fold-level sign/randomization; bootstrap CIs are secondary descriptive
  only (reported per fold).

### Pre-freeze disclosures (no outcome exposure)

- Site availability smoke tests (goto-only, no transitions recorded):
  saucedemo, parabank, demoblaze — 2026-08-24, before freeze.
- Pipeline dry-run on SYNTHETIC rows (/tmp, deleted; caught and fixed one
  bug in the exploratory in-site label mapping before freeze). No real
  outcome variable was examined before the freeze commit.

## 7. Limitations

- Two fine-grained families only; "below coarse" is not exhausted (e.g.,
  lexical/content-level response targets untested).
- Uniform random-walk policy: no deliberate restart/revisit design; WP-004
  identifiability remains BLOCKED (untouched this cycle, per directive).
- Raw DOM snapshots ephemeral (/tmp policy); compact rows preserve every
  analyzed field; raw page content unrecoverable later (disclosed).
- Snapshot settle times differ by action type (80 ms fill/check vs 350 ms
  default), uniform across sites/folds; part of the instrument.
- 769 confirmed transitions give limited power for small interaction
  effects; the frozen α=0.025 randomization + fold-majority rule demands
  effects large enough to beat strong nulls consistently — none found.
- Live-site content is seed-reproducible in policy but not bitwise
  reproducible in environment; disclosed by design.

## 8. Recommended next question (for Lane Director)

Per the pre-declared horizon, passive random-walk sampling at these
representations is EXHAUSTED as an instrument for transferable dynamics:
coarse (R2) and fine (this cycle) both decompose into persistence + local
memory + action-type semantics. The lane should stop unless a genuinely
different instrument is proposed — the natural candidate remains a
deliberate restart/matched-state design aimed at the WP-004 identifiability
gate (committor/barrier program), which would test within-site dynamical
structure rather than cross-site transferability.

---

## 9. Director integration note (appended by Physics Lane Director, 2026-08-24 — nothing above was altered)

Integrated into `lab/physics` after independent audit **PASS**
(`reports/audit/CYCLE_32689298051_PHYSICS.md`,
`results/audit/CYCLE_32689298051_PHYSICS_GATE.json`,
`required_fixes = []`). The auditor's frozen-pipeline rerun reproduced this
report's stored results bit-exact, and a from-scratch recomputation with a
materially different learner confirmed both FALSIFIED verdicts.

**Erratum (audit L2):** §2's parenthetical "(gutenberg 0.90, others 1.00)"
is wrong for openlibrary: its T1 coverage is **0.97** in the stored
artifacts (`results/physics/wp005_results.json`, fold `openlibrary`:
0.9722). The "coverage ≥ 0.90 on all scored folds" statement itself holds;
only the prose enumeration digit is corrected here. Artifacts were always
correct and are unchanged.

**Power bound (audit L3):** read every "no transferable signal" statement
above as "no detectable signal above strong nulls at n=769 with these
folds" — a bounded negative, not proof of absence.
