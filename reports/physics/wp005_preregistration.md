# WP-005 PREREGISTRATION — Fine-Grained Action-Conditioned Response Transfer Under Website Holdout

Frozen: 2026-08-24, SPIDER Team Physics, cycle 2 (GitHub run 32689298051),
BEFORE any WP-005 dataset existed and before any WP-005 outcome was observed.
Context: cycle-1 WP-003B-R2 FALSIFIED the coarse structural family
(audited VALIDATED_FOR_CURRENT_TEST); `directives/PHYSICS.md` sets WP-005 as
the decisive finer-grain test with a pre-declared stop rule.

Provenance (verifiable against git): THIS COMMIT contains this preregistration,
`physics/spider_common.py`, `physics/collector_wp005.py`,
`physics/run_wp005_collection.py`, `physics/run_wp005.py` and
`physics/verify_wp005.py`. No WP-005 dataset exists in /tmp or in git at
freeze time. Pre-freeze instrument work disclosed: availability smoke tests
(goto-only) of candidate NEW sites saucedemo/parabank/demoblaze on 2026-08-24;
no transitions were recorded and no target-level outcomes were examined.
Methods gate 1 (P3 bootstrap anomaly) was resolved and committed BEFORE this
freeze (`results/physics/p3_bootstrap_diagnosis.json`).

## 1. Hypotheses (primary, falsifiable)

H-WP5: A state+action predictor trained on K−1 sites predicts the FINE-GRAINED
environment response class of held-out-site atomic transitions better than ALL
pre-declared strong nulls — i.e., action-conditioned environment response
contains signal that transfers across websites at a granularity BELOW the
falsified coarse structural class.

Two CO-PRIMARY fine-grained targets are declared (multiplicity handled in §7):

- **T1_url_shape_transition**: URL-shape transition class of the transition
  (pre_url → post_url), label = `H{host_same}|D{depth_delta_bucket}|Q{query_delta_sign}`
  where host_same ∈ {0,1}; depth_delta = (#non-empty path segments post) −
  (pre), bucketed {m2plus ≤ −2, m1 = −1, 0, p1 = +1, p2plus ≥ +2};
  query_delta sign of (#query params post) − (pre) ∈ {neg, zero, pos}.
  Maximum inventory 30 classes.
- **T2_dom_diff_signature**: compact DOM-diff signature, label =
  `DOM{digest_same}|E{element_delta_bucket}` where digest_same = 1 iff
  pre_dom_sha256 == post_dom_sha256; element_delta_bucket ∈ {neg, zero, pos}
  from n_elements_post − n_elements_pre. Maximum inventory 6 classes.

Falsification meaning: if H-WP5 fails on BOTH targets above all baselines,
then NO transferable action-conditioned environment regularity exists at
either tested granularity under uniform random-walk sampling, and per the
Director's pre-declared horizon the lane stops absent a genuinely different
instrument proposal.

## 2. Data (collected AFTER this freeze)

Fresh corpus "wp005_v1" via collector v3 (`physics/collector_wp005.py`),
**ATOMIC single-action transitions** — resolves the cycle-1 attribution-fidelity
finding by construction (every row's pre/post snapshots fully bracket exactly
one primitive action; no hidden intermediate states).

- 9 sites: books.toscrape.com, quotes.toscrape.com, the-internet.herokuapp.com,
  en.wikipedia.org (/wiki/ article space only), news.ycombinator.com,
  www.gutenberg.org, openlibrary.org, PLUS new sites www.saucedemo.com and
  parabank.parasoft.com/parabank/ (never used by cycle 1).
- Target per site: 8 independent trajectories × 15 atomic steps (~120/site).
- Sampling policy (declared, identical across sites): choose an action CLASS
  uniformly from those available in the current state, then an element
  uniformly within the class; canned fill values ("spider walk",
  "spiderbot", "research@example.com", password "notasecret-42"); select_option
  picks the first option; NO chained submit. Dialogs auto-dismissed. This is
  policy-matched across folds by construction; any policy-dependent finding
  would be labelled as such.
- Instrument notes (uniform across sites/folds): bounded goto retries (3);
  one longer-settle resnapshot before declaring an absorbing empty state;
  snapshot settle 350 ms default vs 80 ms after fill/check (as R2); raw DOM
  snapshots ephemeral under /tmp (constitution §29).
- Row identity: trajectory_id `{site}-seed20260826-r{j:02d}`; step_id
  contiguous from 0; prev_action_label = previous step's primitive
  ("<START>" at step 0); seed mechanism = base + sha256(site)[:8] int +
  j*10007 (no Python hash()).
- Confirmatory rows: ONLY transitions whose single primitive executed ok.
  Exclusions counted/reported.

The wp003b_r2_v1 corpus is NOT confirmatory evidence for these targets
(its URL-shape outcomes were examined descriptively in cycle 1).

## 3. Representations (frozen)

State features Z: the same frozen 13 mechanics-only dimensions as R2
(`link_bucket … internal_ratio_bucket`; edges as implemented in
`physics/spider_common.py`). One-hot expansion uses the FIXED structural spec
(bucket values 0–2 mapped deterministically to columns) — nothing about Z is
fitted from data, so no transductive encoding can arise in the state block.

Action encoding a_t: one-hot over the primitive action label of the current
atomic transition, vocabulary fit ON THE TRAIN SITES OF EACH FOLD only;
test rows with unseen labels receive an all-zero block (incidence reported as
action_coverage_scored). This corrects cycle-1's pooled-vocabulary caveat C3.

Predictor inputs therefore contain: pre-state features computed before action
execution, and the executed action label fixed before s_{t+1} exists.
Post-state observables enter ONLY the targets.

## 4. Unit, holdout, adequacy (frozen)

- Unit of analysis: one atomic transition.
- Holdout: WEBSITE, leave-one-site-out (true website holdout; site-disjoint
  asserted per fold; each trajectory belongs to exactly one site).
- Fold adequacy (per target): n_scored ≥ 20 AND n_trajectories_scored ≥ 4 AND
  train vocab has ≥ 2 classes.
- Adequacy rule: at least 5 adequate folds among 9 attempted per target,
  else that target's status is DATA_INSUFFICIENT.

## 5. Label space and scoring (frozen)

Per fold per target: train vocabulary V_tr = target classes with ≥ 3
occurrences on TRAIN sites. Scored subset = held-out rows whose class ∈ V_tr;
coverage reported per fold. Harsh variant counts unscoreable rows as errors
for every predictor (reported). Metric: macro balanced accuracy = mean recall
over classes present in the scored subset (recalls weighted equally, actual
class-value set — corrected convention from cycle 1). Chance scale S0:
500 within-fold label shuffles, seed 21, p95 reported per fold.
N_FREQ (train-majority constant) is REPORTED but excluded from the strong-null
max: it is degenerate under macro balanced accuracy (cycle-1 audit C8).

## 6. Predictors and nulls (frozen)

All fitted objects use TRAIN-fold data only:

- M_SA (candidate): multinomial logistic regression (full-batch GD, lr=0.5,
  800 iterations, L2=1e-3, local class indexing) on [onehot(Z) | onehot(A)].
- M_S (paired ablation): same LR on [onehot(Z)] alone.
- N_ACTION_ONLY: same LR on [onehot(A)] alone — separates generic action
  semantics from state-dependent physics.
- N_PERSIST_FINE: training-free constant prediction of the inert class
  (T1: "H1|D0|Qzero"; T2: "DOM1|Ezero") — the persistence analog at fine
  granularity ("the page stays put"). If the inert class is outside V_tr for
  a fold, falls back to that fold's train-majority class (disclosed per fold).
- N_NN_Z / N_NN_ZA: 1-nearest-neighbour memory nulls in standardized
  (train-stats) [Z] / [Z|A] space; neighbour's target as label.
- N_FREQ: reported, not strong (above).
- S0: chance reference (not in max-null rule).

Fold statistic D_f = acc(M_SA) − max over STRONG NULLS
{N_ACTION_ONLY, N_PERSIST_FINE, N_NN_Z, N_NN_ZA}.

## 7. Primary inference (frozen; P3-gated)

Per co-primary target T, on its adequate folds:

- R1 (randomization test): trajectory-clustered sign-flip randomization of
  row-level discordances between M_SA and the fold's best strong null.
  Discordance w_i = 1[M_SA correct] − 1[best-null correct] ∈ {−1,0,+1};
  whole trajectories are flipped jointly (preserves within-trajectory
  dependence under H0); flips independent across all trajectories of all
  adequate folds; 20000 replicates, numpy default_rng(43); one-sided
  p = (1 + #{S_rep ≥ S_obs}) / (1 + 20000). Requirement: p_T ≤ 0.025
  (Bonferroni split of α=0.05 across the two co-primary targets).
- R2 (fold majority): D_f > 0 in a strict majority of adequate folds
  (ties count against M_SA).
- R3: mean_D(T) > 0.
- R4 (action-conditioning gate): paired ablation acc(M_SA) > acc(M_S) in a
  strict majority of adequate folds.

Per-target status:
- SURVIVES_CURRENT_TEST_T iff R1 ∧ R2 ∧ R3 ∧ R4.
- STATE_ONLY_SURVIVOR_T iff R1 ∧ R2 ∧ R3 but ¬R4 (transferable response
  signal exists but is carried by state alone; action conditioning adds
  nothing transferable).
- Otherwise FALSIFIED_T.
- DATA_INSUFFICIENT_T if fewer than 5 adequate folds.

Overall verdict (exactly one constitutional status):
- SURVIVES_CURRENT_TEST if any target is SURVIVES_CURRENT_TEST_T;
- FALSIFIED if both targets are FALSIFIED_T;
- DATA_INSUFFICIENT if both targets are DATA_INSUFFICIENT_T;
- INCONCLUSIVE otherwise (decompositions reported explicitly).

Bootstrap CIs (trajectory-grouped, seed 17, 1000 reps, percentile) are
SECONDARY DESCRIPTIVE ONLY and never support the verdict — mandated by
methods gate 1 and `results/physics/p3_bootstrap_diagnosis.json`.

## 8. Verdict application (frozen, applied exactly once)

The rules of §7 are applied once, by `physics/run_wp005.py`, on the fresh
corpus. Any hard gate failure (§9) => MEASUREMENT_INVALID with no
substantive interpretation. Bounded wording follows R2 §8 practice: any
FALSIFIED claim is bounded to this representation family × these two
fine-grained targets × uniform random-walk sampling × these sites; any
SURVIVES_CURRENT_TEST claim is bounded likewise and requires replication on
fresh sites before GENERALIZATION wording (directive).

Expected direction declared honestly: given R2 (persistence dominates; NN
saturates in-site signal; action-conditioning adds ~0 even in-distribution)
and that T2's inert class will dominate wherever pages rarely change, prior
on survival is LOW (~0.15–0.25). A FALSIFIED outcome is a real scientific
possibility and closes the two-level question under the Director's stop rule.

## 9. Validity gates (hard assertions, fail closed => MEASUREMENT_INVALID)

- G1 Identity/alignment/atomicity: contiguous step_id from 0; prev_action_label
  == previous step's action ("<START>" at 0); every row has exactly one
  primitive action (chain_len==1 semantics enforced via field equality);
  prev==target rate < 0.98 anti-leak guard.
- G2 Execution filter: scored rows have ok=true; exclusions counted.
- G2b No post-state information in inputs: inputs = PRE-state features +
  current action label only (structural, by construction of
  spider_common.features and the action block).
- G3 Site disjointness per fold; one site per trajectory.
- G4 Determinism: sha256/integer seeds only; no Python hash() anywhere.
- G6 Support/coverage rules per §5 applied without using held-out outcomes
  beyond the frozen scoring definition; coverage + harsh variant reported.
- G7 Arithmetic/metric checks: balanced accuracy recomputed independently in
  the verifier; verdict recomputed from stored per-fold artifacts.
- G8 Atomicity: confirmed rows satisfy chain_len==1 and ok=true.
- G9 Target consistency: stored t1/t2 labels equal recomputation from raw
  pre/post URLs, DOM digests and element counts on 100% of rows.

## 10. Frozen secondary / exploratory items (cannot rescue primary)

- S9 Per-class recall tables (M_SA vs best null), coverage, harsh variant,
  class-imbalance counts per fold/target.
- S10 In-site diagnostic: within-site trajectory-split for each target with
  M_SA/M_S/N_PERSIST_FINE/N_NN_ZA (train-half fit), exploratory only.
- S11 Secondary descriptive grouped-bootstrap CI of mean D per target.
- S12 Descriptive identifiability-gate diagnostics remain OUT OF SCOPE here
  (WP-004 stays BLOCKED).

## 11. Provenance commitments

Compact transition rows (no raw DOM) will be committed at
`data/physics/wp005_transitions.jsonl.gz` with a sha256 manifest at
`data/manifests/wp005_dataset_manifest.json`, plus collection logs. Raw DOM
snapshots stay ephemeral in /tmp; what cannot be recomputed later is exactly
the raw-page content, disclosed here. All five code files listed in the
provenance paragraph above are committed in THIS freeze commit together with
this preregistration (audited against git; cycle-1's §11 misstatement is not
repeated). Results files are new files; historical JSONs are never overwritten.
