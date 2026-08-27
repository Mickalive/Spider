# WP-003B-R2 PREREGISTRATION — Action-Conditioned Next-State Structure Under Website Holdout

Frozen: 2026-08-24, SPIDER Team Physics, cycle 1 (GitHub run 32676578274), BEFORE
any R2 dataset existed and before any R2 outcome was observed. Preceded by:
WP-003 audit verdict MEASUREMENT_INVALID (see `results/physics/WP003_AUDIT_STATUS.json`);
`docs/NEXT_PHYSICS.md` immediate objective; `directives/PHYSICS.md`.

This experiment replaces the invalidated WP-003 primary target with the
environment-response target demanded by the constitution §16:

    P(class(s_{t+1}) | Z(s_t), a_t)

No committor/barrier work is performed (WP-004 stays blocked).

## 1. Hypothesis (primary, falsifiable)

H-R2: The coarse structural class of the environment's next state is
predictable from the current mechanics-only state plus the executed action,
with signal that TRANSFERS ACROSS WEBSITES: a multinomial logistic predictor
trained on K-1 sites predicts the held-out site's next-state structural class
better than all pre-declared strong nulls, at the trajectory-grouped 95% level.

If H-R2 fails, cross-site transferable environment dynamics do NOT exist at
this representation granularity (FALSIFIED for this family). This is a real
possible outcome and is not a measurement failure.

## 2. Data (collected AFTER this freeze)

Fresh live-site random-walk corpus "wp003b_r2_v1", collected by the corrected
collector (`physics/collector.py`) with deterministic identity fields:

- 7 sites (distinct hosts/apps): books.toscrape.com, quotes.toscrape.com,
  the-internet.herokuapp.com, en.wikipedia.org (/wiki/ article space only),
  news.ycombinator.com, www.gutenberg.org, openlibrary.org.
- Target per site: 8 independent trajectories x 15 transitions (~120/site).
- Sampling policy (declared, identical across sites): at each state choose an
  action CLASS uniformly from the classes available in that state, then an
  element uniformly within the class; fill values are fixed canned strings;
  with p=0.6 a fill is followed by a uniformly chosen enabled button click.
  This is the documented exploration policy; it is policy-matched across folds
  by construction. Any policy-dependent finding would be labelled as such.
- A transition record stores: site, trajectory_id, step_id, pre/post feature
  vectors, action chain labels, execution ok flags, url_changed, load_ms,
  prev_action_label = primary action of transition t-1 ("<START>" at t=0),
  sha256 of raw pre/post DOM snapshots (raw DOM gzipped under /tmp only).
- Confirmatory rows: ONLY transitions where every chain step executed with
  ok=true (`any_ok`). Exclusions are counted and reported.

## 3. Representations (frozen)

State features Z (13 mechanics-only dims, no text, no site identifiers):
link_bucket, button_bucket, text_input_bucket, has_password, has_select,
has_checkbox, has_file, has_textarea, form_bucket, depth_bucket, query_bucket,
login_capable, internal_ratio_bucket (bucket edges as implemented in
`physics/collector.py`; one-hot expanded for bucket dims {0,1,2}x7).

Action conditioning a_t (frozen definition): one-hot of LAST chain label
(proximal cause) + one-hot of FIRST chain label when the chain has >1 step
else a zero block. Vocabulary observed from data; no hand-authored mapping.

Primary TARGET: structural class of s_{t+1} =
(depth_bucket, has_password, link_bucket, text_input_bucket) of the POST state.

## 4. Unit, holdout, adequacy (frozen)

- Unit of analysis: one transition.
- Holdout level: WEBSITE, leave-one-site-out over adequate folds (true
  website holdout; no site/task content crosses folds).
- A fold is ADEQUATE iff n_confirmed >= 20 AND n_trajectories >= 4.
- Adequacy rule: at least 5 adequate folds among the 7 attempted, else the
  PRIMARY verdict is DATA_INSUFFICIENT (no claim about H-R2 either way).

## 5. Label space and scoring (frozen)

Per fold: train vocabulary V_tr = target classes with >= 3 occurrences on
train sites. Test rows whose target class is outside V_tr are EXCLUDED from
the scored subset; coverage = scored/test_confirmed is REPORTED per fold.
Secondary harsh variant counts excluded rows as errors for every predictor.

Metric: macro balanced accuracy = mean recall over classes PRESENT in the
scored test subset (recalls weighted equally). Per-fold chance scale reported
via S0 shuffle (below); raw accuracy also reported for transparency.

## 6. Predictors and nulls (frozen)

- M_SA (candidate): multinomial logistic regression, full-batch gradient
  descent, lr=0.5, 800 iterations, L2=1e-3 (deterministic implementation
  inherited from corrected `physics/run_wp003.py`), inputs [onehot(Z),
  onehot(first), onehot(last)], trained on K-1 sites.
- N_PERSIST (structural persistence null): predict class(s_t) itself. Uses
  NO training data; cannot leak; tests whether anything beyond "pages stay
  structurally put" is being predicted.
- N_MAJ (frequency null): train-sites majority target class.
- N_NN_Z (memory null): 1-nearest-neighbour from each test state to pooled
  train states in standardized Z (train mean/sd), label = neighbour's target.
- N_NN_ZA (action-conditioned memory null): 1-NN in standardized
  [Z, onehot(last)] space, label = neighbour's target. Stronger retrieval
  baseline per the WP-002B lesson.
- S0 (chance reference, not in max-null rule): 500 within-fold label
  shuffles, seed 21 -> null distribution of balanced accuracy given test
  marginals; p95 reported per fold.

Fold statistic (frozen): D_f = M_SA - max(N_PERSIST, N_MAJ, N_NN_Z, N_NN_ZA)
on the fold's scored subset. Primary aggregate: mean(D_f) over adequate folds.

## 7. Uncertainty (frozen)

Trajectory-grouped nonparametric bootstrap: within EACH adequate fold
resample that fold's trajectories with replacement (same count), recompute
all predictors' balanced accuracies on the resampled rows, recompute D_f;
aggregate mean across folds; 1000 replicates; numpy default_rng(17);
percentile CI. No refitting inside the bootstrap; no jittering of point
estimates. Correlated transitions are respected by resampling whole
trajectories (dependency unit = trajectory).

## 8. Verdict rules (frozen, applied exactly once)

Let F_ad = set of adequate folds, need |F_ad| >= 5 else DATA_INSUFFICIENT.

- SURVIVES_CURRENT_TEST iff bootstrap 95% CI of mean(D_f) lies entirely
  above 0 AND D_f > 0 in at least ceil((|F_ad|+1)/2) adequate folds.
- Otherwise FALSIFIED (for representation family Z x this action encoding x
  coarse structural target; bounded claim, not universal physics).
- Any hard assertion/gate failure during analysis => MEASUREMENT_INVALID
  (no substantive interpretation follows).

Expected direction declared honestly: prior from WP-002B (in-distribution
signal ~ NN-level, no holdout evidence) gives low-to-moderate prior (~0.3)
on survival; persistence null expected to be strong on low-navigation
actions; a FALSIFIED result localizes predictability to memory +
site-specific structure + structural persistence.

## 9. Frozen secondary / exploratory items (cannot rescue the primary verdict)

S1 Action-ablation (exploratory): M_S = same LR on [onehot(Z)] only. Report
paired M_SA - M_S difference per fold with the same grouped bootstrap CI.
Addresses whether explicit action conditioning adds transferable information
beyond state alone.

S2 In-distribution diagnostic (exploratory): within each site, hold out half
the trajectories (grouped split), train M_SA / evaluate persistence / N_NN_ZA
on held-out trajectories of the SAME site. Localizes whether any failure is
"no signal anywhere" vs "signal exists but site-specific".

S3 Per-class recall table (M_SA vs best null per fold); component-marginal
accuracy for each of the 4 target components (descriptive).

S4 Identifiability-gate diagnostics for future WP-004 (descriptive only):
counts of repeated states (url_shape and structural-class level) visited
from independent trajectories, and outcome-branching counts at repeated
states. No committor/barrier estimation. WP-004 remains BLOCKED; these
numbers only inform whether the gate can plausibly be run later.

## 10. Validity gates (hard assertions, fail closed => MEASUREMENT_INVALID)

G1 Identity/alignment: every row has trajectory_id, integer step_id starting
at 0, contiguous steps, prev_action_label == primary action of t-1,
"<START>" at t=0; target==primary chain semantics preserved.
G2 No post-state information in pre-state inputs: pre features computed
before action execution by construction; asserted structurally in code
review + recomputation of features from stored raw digests where available.
Included rows have any_ok=true (execution actually happened).
G3 Site-disjointness: train/test site sets disjoint per fold; each
trajectory belongs to exactly one site.
G4 Determinism: all RNGs are seeded integers (sha256-derived site offsets +
fixed constants); Python salted hash() is forbidden and absent.
G5 Bootstrap integrity: resampling unit = trajectory; no refit inside
bootstrap; fixed seeds; percentile method only.
G6 Class support handled per frozen Section 5; coverage reported; no
post-hoc filtering using held-out outcomes.
G7 Arithmetic/metric checks: balanced accuracy recomputed independently;
verdict recomputed from stored per-fold artifacts.

## 11. Provenance commitments

Derived compact transition rows (no raw DOM) are committed for audit
recomputation, together with sha256 manifests and collector seeds. Raw DOM
snapshots remain ephemeral in /tmp per data policy; what cannot be recomputed
later is exactly the raw-page content, disclosed here. Analysis code is
committed in the same freeze commit as this file; results files are new
files; historical JSONs are never overwritten.
