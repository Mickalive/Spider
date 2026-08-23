# WP-003B-v2 PREREGISTRATION — Action-Conditioned Next-State Structure Under Website Holdout

Frozen: 2026-08-23, cycle 32670239235, TEAM PHYSICS.
Status at freeze: **no new data collected, no outcome observed.**
This preregistration supersedes the historical (exploratory, audit-flagged)
`wp003b_targetB.json` analysis, which is retained as provenance only.

Authority: `directives/PHYSICS.md` items 3–8; master constitution §16–§25.

---

## 1. Hypothesis (H1, primary)

H1: The environment response of interactive websites,
`class(s_{t+1}) ~ P(· | Z(s_t), a_t)`,
has cross-site predictable structure: a mechanics-only model estimated on
K−1 sites predicts the coarse structural class of the next state on a held-out
site better than strong nulls that require no mechanical model.

This is an environment-dynamics target (`P(s' | s, a)`), not a
crawler-policy target. The action `a_t` is imposed by a documented uniform-ish
random policy and is treated as an intervention input, following §16.

Falsification meaning: if H1 fails under this test, the claim
"mechanics-only state+action structure predicts next-state structure across
unseen sites" is falsified AT THIS REPRESENTATION GRANULARITY AND CORPUS. It is
not a falsification of all possible Web physics (§20 narrow verdicts).

## 2. Data (collected strictly AFTER this freeze)

New corpus `wp003b_v2_transitions.jsonl`, collected by the corrected collector
(`physics/collector.py`, deterministic sha256 site offsets, per-row
`trajectory_id`, `step_id`, true `prev_action_label = primary_action(t−1)`).

Sites (7 distinct live hosts): books.toscrape.com, quotes.toscrape.com,
the-internet.herokuapp.com, en.wikipedia.org (/wiki/ article space only),
news.ycombinator.com, openlibrary.org, gutenberg.org.

Policy (documented input distribution, §16): uniform choice among available
actionable classes (click_link / click_button / fill_text / fill_password /
select_option / check_box); fill chains append a random button click with
p=0.6; fill values are fixed constants; 6 independent trajectories/site × 15
steps intended (≥90 steps/site target); collector seed base 20260823;
per-trajectory seed = base + sha256(site)[:8] + j·10007 (process-stable).

Pre-registered exclusion rule (mechanical, decided before any outcome):
a transition is excluded from analysis iff the FIRST action of its chain failed
(`action_labels[0].ok == false`) — the intended action was not effectively
applied to the environment. Partial-chain rows where the first action succeeded
are kept; this is noted as a limitation. Exclusion counts are reported.

## 3. Representation (frozen, semantics-ablated)

State features Z(s): exactly the 13 collector mechanics buckets
(`physics/run_wp003.py FEATURES`): link_bucket, button_bucket,
text_input_bucket, has_password, has_select, has_checkbox, has_file,
has_textarea, form_bucket, depth_bucket, query_bucket, login_capable,
internal_ratio_bucket. NO text, NO hrefs, NO site identifiers, NO embeddings.

Action descriptor A(a_t): one-hot primitive class of the chain's first action
∈ {click_link, click_button, fill_text, fill_password, select_option,
check_box} plus binary chain flag (chain length > 1). Both known strictly
before the outcome.

Leakage-by-construction control: the primary target deliberately EXCLUDES
URL-derived next-state components (depth_bucket', query_bucket'), because URL
grammar can make them near-deterministic functions of site identity rather than
of (Z(s), a_t).

## 4. Primary target (frozen)

T1 = signature class of s_{t+1}:
`(link_bucket', form_present')` with link_bucket' = {0:<10, 1:10–49, 2:≥50}
internal visible anchors captured, form_present' = 1 if ≥1 <form> captured.
Fixed thresholds, defined a priori → ≤6 classes, no post-hoc class filtering
(train-fit-only preprocessing; nothing about test labels is used to define or
filter classes — corrects a defect of the historical run).

Primary metric: multiclass balanced accuracy (macro recall over T1 classes
present in the fold's test rows), identical computation for model and nulls.

## 5. Unit, holdout, folds

Unit of analysis: transition. Holdout unit: WEBSITE (leave-one-site-out over
the 7 sites). Trajectories never span sites. Preprocessing (feature standard-
ization for NN, class priors for nulls, model weights) fit on TRAIN folds only.

Fold adequacy (frozen): a fold enters inference iff n_test ≥ 45 usable
transitions AND ≥ 4 independent trajectories. Overall DATA_INSUFFICIENT if
< 5 adequate folds OR total usable transitions < 400.

## 6. Model and nulls (all frozen)

- M: multinomial logistic regression on [onehot(Z) ⊕ onehot(A)] — the repo's
  deterministic full-batch softmax regression (iters=800, lr=0.5, L2=1e-3),
  trained on pooled K−1 sites. Deliberately simple: capacity parity with nulls.
  KNOWN LIMIT, accepted at freeze: a linear model cannot express conjunctions
  of state and action features. Consequence: an exploratory interaction-
  augmented arm (§9 S-E) is preregistered to probe this limit without being
  able to alter the primary verdict.
- N0: train-majority T1 class (global frequency null).
- N3: action-conditional train majority T1 class given first-action class
  (back off to N0 if unseen).
- N5: coarse conditional-frequency ("Markov-style") null:
  cell = (depth_bucket, link_bucket | s_t) × first-action-class → train
  majority T1 in that cell; back off N5→N3→N0. Strongest simple environment
  null that still uses (s, a).
- N4: 1-nearest-neighbour memory baseline: standardized onehot [Z ⊕ A],
  Euclidean, label of nearest pooled-train transition (retrieval/memory
  baseline per WP-002B lesson: NN matched rules in-distribution).
- S0 (calibration only, not in decision rule): within-site permutation of T1
  labels, 500 draws, reports chance distribution of balanced accuracy given
  site marginals.

Per-fold paired effect: d_s = balacc(M) − max(balacc(N0,N3,N4,N5)) on the same
test rows. M must beat the best null within folds, not merely on average
(guards against across-site frequency artifacts).

## 7. Uncertainty (frozen)

Trajectory-grouped nonparametric bootstrap: within each held-out site,
resample that site's trajectory_ids with replacement (same count), recompute
d_s, average d_s across folds, 2000 replicates, seed 20260824,
percentile CI. Resampling unit = independent trajectory = assumed independence
unit (transitions within a trajectory are autocorrelated; §18 uncertainty
integrity). No jitter/noise is added to point estimates.

## 8. Verdict rules (frozen, decided now)

Let CI = 95% percentile interval of mean paired effect, W = number of adequate
folds with d_s > 0, S = number of adequate folds.

- SURVIVES_CURRENT_TEST ⟺ CI.lower > 0 AND W ≥ ⌈S/2⌉.
- FALSIFIED (for H1 at this granularity/corpus) ⟺ CI.upper < 0.
- INCONCLUSIVE otherwise (includes CI straddling 0).
- DATA_INSUFFICIENT per §5 adequacy rule (takes precedence over the above).

No directional commitment was made ex ante (WP-001/WP-002B weakly positive
in-distribution; cross-site transfer genuinely untested); two-sided rules.

## 9. Secondary analyses (preregistered, cannot rescue primary)

- S-A: single-component targets, same protocol: link_bucket'; form_present';
  text_input_bucket'; has_password'. Descriptive support/localization.
- S-B: representation ablation: alternate legitimate bucketing (links
  {0:<5,1:5–29,2:≥30}; inputs/buttons/forms {0,1–2,≥3}); H1 conclusion should
  not qualitatively flip; report whether it does.
- S-C: WP-004 IDENTIFIABILITY GATE (blocks/unblocks committor work):
  state key κ = (site, url_shape, tuple(Z(s))). Independent visit = transition
  whose pre-state matches κ from a distinct trajectory_id (or same trajectory
  but ≥2 steps apart). G1 = #keys with ≥3 independent visits; G2 = #(those
  keys) with ≥2 distinct first-action classes AND ≥2 distinct observed T1
  outcomes. PASS iff G1 ≥ 50 AND G2 ≥ 20 → committor estimation MAY proceed to
  design review. FAIL → WP-004 stays BLOCKED; verdict for WP-004 feasibility
  on this corpus: DATA_INSUFFICIENT.
- S-D: policy documentation: per-site action-class marginals (verify the
  documented uniform-ish policy actually ran; separates policy from physics).
- S-E (exploratory, added at freeze for a stated reason): interaction-
  augmented model M-int = same logistic regression on [onehot(Z) ⊕ onehot(A)
  ⊕ A×Z crossings]. Rationale: the pre-freeze synthetic sensitivity check
  demonstrated that the linear primary model cannot fit conjunctive/parity
  channels even when clean signal exists; M-int bounds how much of any result
  is an artifact of that capacity limit. Cannot rescue or overturn primary.

## 10. Measurement-validity commitments

- Anti-leak assertions run pre-analysis (`validate_rows` + v2 checks):
  contiguity, prev-label alignment, prev==target rate guard, no post-state
  fields among predictors.
- Seed determinism verified across processes with randomized PYTHONHASHSEED
  (unit test committed before collection).
- Protocol sensitivity verified on SYNTHETIC data BEFORE freezing:
  (i) a planted LINEARLY-REPRESENTABLE cross-site channel must be detected;
  (ii) pure-noise targets must NOT yield survival. A first draft planted a
  parity channel; the linear primary model correctly failed to fit it — the
  channel was re-specified to be representable in the frozen model class, and
  the episode is recorded here as provenance that the harness can fail a
  protocol (see tests/test_cycle_32670239235.py, committed with this freeze).
- Raw DOM snapshots remain in /tmp (ephemeral, per §31); compact rows embed
  sha256 digests; dataset manifest with counts/digests committed.

## 11. Honest prior

P(SURVIVES) ≈ 0.2–0.3: in-distribution mechanical signal existed (WP-001/WP-002B
~+0.05 over shuffle) but NN matched rules there, and site-id dominates
next-state structure; website holdout is exactly where such signal usually dies.
A clean FALSIFIED or INCONCLUSIVE result is a publishable-in-ledger outcome that
localizes Web "physics" to memory + site-specific regularity at this
granularity. Expected information gain is high either way because every prior
attempt at this target was measurement-invalid or exploratory.
