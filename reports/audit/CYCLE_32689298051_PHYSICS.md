# INDEPENDENT AUDIT — PHYSICS LANE, CYCLE 2 (GitHub run 32689298051)

Auditor: Independent Auditor, Physics lane (repair round 0 — first audit of
this cycle). Date: 2026-08-24.

Team branch audited: completed team workspace `/tmp/spider_physics_team`
(head `6963545`, "Physics cycle 2: WP-005 report + ledger entry …"). Base
under audit write-scope: current checkout `physics-audit-base` (`894d120`,
untouched accepted Physics state). Subject: **WP-005 — Fine-Grained
Action-Conditioned Response Transfer Under Website Holdout**. Team verdict:
**FALSIFIED** on both co-primary targets; team invokes the Director's
pre-declared two-level-negative stop rule.

Audit method: git forensics on the freeze timeline; sha256 verification of
the committed dataset and manifest; full rerun of the team's frozen pipeline
and verifier in an auditor sandbox against the committed data; and a FULL
INDEPENDENT RECOMPUTATION of every headline number from the committed rows
using a from-scratch implementation
(`/tmp/opencode/audit_wp005/independent_recompute.py`) that imports no team
code and uses a materially different learner (standardized multinomial LR
with bias term, 4000 iterations vs the team's unstandardized 800-iteration
fit), own target derivation, own balanced accuracy, own NN, own randomization
seed. No team file was edited.

---

## 0. Gate decision up front

**GATE = PASS** (`results/audit/CYCLE_32689298051_PHYSICS_GATE.json`).
The FALSIFIED verdict is a valid negative result, honestly represented and
correctly bounded; its measurement survives adversarial inspection and
independent recomputation. PASS means safe for the Lane Director to consider;
it does not upgrade any claim beyond the wording audited below.

---

## 1. Claims checked and statuses

### C1. Dataset `wp005_v1`: 875 collected / 769 confirmed / 106 not-ok, 9 sites, per-site counts as reported — **VALIDATED_FOR_CURRENT_TEST**
- EVIDENCE: `data/physics/wp005_transitions.jsonl.gz`,
  `data/manifests/wp005_dataset_manifest.json`, results JSON.
- RECOMPUTATION: gz sha256 = `97e406ee48396103…c5144c5b4` and uncompressed
  sha256 = `b76525bd674606898593f7ab48cbe65bcb26c7f2b260f1eef30033a2ac074ff6`
  both match the manifest exactly; 875 rows; ok=true = 769; per-site
  collected {books 120, quotes 120, internet 27, wikipedia 120,
  hackernews 25, gutenberg 120, openlibrary 120, saucedemo 120, parabank 103}
  and confirmed {..., wikipedia 99, gutenberg 119, openlibrary 36} match the
  manifest and report §5 exactly.
- FAILURE MODES TESTED: hidden exclusions, silent row drops, count inflation.
  None found. Exclusions are counted in artifacts (report §5 discloses
  openlibrary 36/120 and early-terminating internet/hackernews walks).

### C2. Preregistration timing and provenance sentences are TRUE this time (cycle-1 defect C6 not repeated) — **VALIDATED_FOR_CURRENT_TEST**
- EVIDENCE: freeze commit `d81aee5` (2026-08-24T04:47:56Z) contains exactly
  the six files named in prereg §11 provenance paragraph (prereg +
  `spider_common.py`, `collector_wp005.py`, `run_wp005_collection.py`,
  `run_wp005.py`, `verify_wp005.py`); dataset commit `9e19461`
  (05:25:50Z); results commit `7c9b395` (05:28:03Z).
- RECOMPUTATION: all 875 row timestamps lie in [04:52:14, 05:20:11] UTC —
  every row postdates the freeze commit; zero rows predate it.
  Methods-gate-1 diagnosis committed at `0a83912` (04:34:22Z), i.e. BEFORE
  the freeze, as claimed.
- LIMIT (disclosed): "no WP-005 dataset exists in /tmp at freeze time" is not
  provable from git alone; git absence + all-row timestamp ordering is the
  strongest available evidence. Pre-freeze smoke tests (goto-only) and a
  synthetic-row dry run were disclosed in prereg/report §6. Accepted with
  this standard caveat.

### C3. Target construction and G9 label consistency — **VALIDATED_FOR_CURRENT_TEST**
- EVIDENCE: `physics/spider_common.py` (t1_label/t2_label), collector writes
  labels from pre/post observables; verifier P7 re-derives independently.
- RECOMPUTATION (own code): recomputed T1 for all 875 rows from
  pre_url/post_url and T2 from dom digests + element counts — 0 mismatches.
  Class distributions confirmed: T1 inert `H1|D0|Qzero` = 569/769 = 74.0%;
  rarest classes n=1–2; T2 `DOM1|Ezero` = 290/769 = 37.7%, max/min = 290/1 —
  matching the imbalance disclosures in report §5.
- FAILURE MODES TESTED: target leakage into inputs (none — targets derive
  only from post observables: post_url, post digest/count deltas; predictor
  inputs are PRE-state features + current action label by code construction
  in `collector_wp005.collect_trajectory`, where `pre_feat = features(cur)`
  is computed before action selection/execution), post-state leakage via
  trajectory chaining (`cur = post` is the next transition's legitimate
  pre-state), hidden site identifier in Z (features are structural buckets
  only; my independent expansion asserted all bucket values within the fixed
  spec ranges).

### C4. Split integrity / train-fold-only fitting (methods gate 2) — **VALIDATED_FOR_CURRENT_TEST**
- EVIDENCE: `run_wp005.py` LOSO loop; verifier P6.
- RECOMPUTATION: site disjointness holds per fold by construction of the
  site index and is asserted in code; each trajectory maps to exactly one
  site (validated across all 72 trajectories). Action vocabularies are fit
  per fold on train rows only (`vocab_a` from `tr_use`); I verified
  independently that NO held-out-site action label is unseen in any fold
  (action_coverage_scored = 1.00 on all 18 target-folds, confirming the
  report claim). State block uses the FIXED structural one-hot spec
  (`ONEHOT_SPEC`) — nothing fitted from data, so transductive encoding is
  structurally impossible in Z. NN standardization uses train stats only;
  LR class spaces are train-local.
- FAILURE MODES TESTED: pooled-corpus encoding (cycle-1 C3) — absent;
  duplicated content across folds (sites are distinct domains; no cross-site
  row duplication possible); trajectory overlap across folds — none.

### C5. Headline arithmetic, frozen rules, verdict application — **VALIDATED_FOR_CURRENT_TEST**
- EVIDENCE: `results/physics/wp005_results.json`; report §2 table.
- RECOMPUTATION:
  (a) I reran the UNMODIFIED frozen pipeline (`run_wp005.py`) on the
  committed dataset in an auditor sandbox: output JSON is IDENTICAL to the
  stored results JSON (verdict FALSIFIED; T1 mean_D −0.0432, wins 1/9,
  p=0.897605, M_SA>M_S 2/9; T2 mean_D −0.0497, wins 4/9, p=0.269537,
  M_SA>M_S 7/9). Code↔data↔report consistency is bit-exact.
  (b) Fully independent implementation (my own LR/NN/metrics/labels):
  T1 mean_D −0.0312, wins 3/9, M_SA>M_S 5/9, own-seed randomization
  p=0.9969; T2 mean_D −0.0474, wins 2/9, M_SA>M_S 8/9, p=0.60782. Per-fold
  values differ modestly (learner-dependent, e.g. hackernews T1 +0.200 mine
  vs +0.000 stored; wikipedia T1 −0.096 mine vs 0.000 stored) but NO rule
  outcome changes: both targets remain far below R1 (p ≤ 0.025), R2
  (majority ≥5/9), and R3 (mean_D > 0) under a materially different,
  better-conditioned learner. The negative does NOT depend on the team's
  specific optimizer or metric implementation.
  (c) Frozen-rule trace: ties count against M_SA in R2 as preregistered;
  Bonferroni α=0.025×2 co-primary as declared; adequacy 9/9 folds ≥ frozen
  thresholds (n_scored≥20, trajectories≥4, vocab≥2 — verified per fold);
  overall verdict rule applied correctly (both FALSIFIED → FALSIFIED).

### C6. Uncertainty at the correct dependency unit; P3 anomaly resolved pre-freeze (methods gate 1) — **VALIDATED_FOR_CURRENT_TEST**
- EVIDENCE: primary inference = trajectory-clustered sign-flip randomization
  pooled across adequate folds (flips jointly per trajectory — matches the
  actual within-trajectory dependence unit), plus conservative fold-majority;
  grouped bootstrap demoted to SECONDARY DESCRIPTIVE ONLY.
- RECOMPUTATION: `results/physics/p3_bootstrap_diagnosis.json` reproduces the
  cycle-1 P3 numbers bit-exact, shows the linear-statistic case gives
  grouped/naive width ratio 1.0 at the measured ICC≈0.013, and attributes the
  cycle-1 grouped<narrower anomaly to the nonlinear statistic (class-drop
  re-weighting + recall ratios + max-over-nulls at ~8 clusters). This
  satisfies directive emphasis #6 (estimator sanity at actual cluster count)
  by bounding widths as descriptive-only BEFORE the confirmatory experiment.
  My own-seed randomization p-values differ numerically (expected: obs near
  the center of a coarse discrete null) but agree in conclusion (p ≫ α).
- FAILURE MODES TESTED: arbitrary-noise-as-bootstrap (cycle-1 WP-003 defect)
  — absent here; CI widths support no claim in this cycle.

### C7. Null strength, degenerate-null handling, policy confounding — **VALIDATED_FOR_CURRENT_TEST (negative result adequately supported)**
- The mandatory ACTION_ONLY baseline (directive #8) is present and is
  honestly reported as the BEST null on 3/9 folds per target (e.g., internet
  T2: N_ACTION_ONLY 0.909 vs M_SA 0.500) — the team interprets this against
  its own interest, which is correct practice.
- N_PERSIST_FINE (training-free inertness) and N_NN_Z/N_NN_ZA memory nulls
  implemented as preregistered; S0 shuffle p95 reported per fold.
- N_FREQ is REPORTED but excluded from the strong-null max per cycle-1 audit
  C8 and directive #9 (degenerate under macro balanced accuracy) — correct.
- Policy: identical `choose_action_atomic` mechanism for all sites (uniform
  over available action classes, then uniform within class; canned fill
  values; select-first-option confirmed in `shared/browser.act`; no chained
  submit — one primitive per recorded transition, atomicity enforced by
  field equality and validated on all rows). Observed per-site action-class
  mixtures differ (environment-driven availability), which is exactly why
  ACTION_ONLY matters; the sampling MECHANISM is policy-matched across
  folds/sites in code, not merely in prose. Wikipedia's allow/deny prefix
  scope restriction is uniform within that site and disclosed in WALKS.
- Degenerate folds disclosed: saucedemo T1 (single scored class → all
  predictors 1.000; S0 p95 = 1.000 confirms zero information) and wikipedia
  T1 contribute D_f = 0 and count AGAINST M_SA via tie-breaking; descriptive
  exclusion leaves wins 1/7 (T1) and 4/7 (T2) — verdict unchanged. Reported
  without altering the frozen rule.

### C8. Exploratory in-site diagnostic (S10) honesty — **VALIDATED_FOR_CURRENT_TEST**
- Stored S10 numbers match report §4 claims exactly: T2 M_SA beats
  N_PERSIST_FINE on every listed site; vs N_NN_ZA edge ≤ +0.088 (books
  +0.0882) and negative on parabank (−0.0474)/saucedemo (−0.0294); T1
  M_SA ≈ NN_ZA (books 0.000, gutenberg +0.0078, quotes −0.0611). Global
  label space used is flagged exploratory-only and cannot rescue the primary.
- Verifier P1/P2 probes: T2 books behaves (real 0.308 > shuffled 0.033 >
  randomized-features 0.221); T1 books returns real == shuffled-label
  accuracy (0.200 = 0.200, status NOTE in the artifact) — consistent with
  there being nothing to learn there (stored D_f −0.189). Report phrase
  "probes behave" is mildly generous for T1/books but the artifact discloses
  the raw values; probe is diagnostic, not a gate.

### C9. Stop-rule invocation and bounded wording — **VALIDATED_FOR_CURRENT_TEST**
- `directives/PHYSICS.md` (accepted base) pre-declares: two-level FALSIFIED
  above all baselines ⇒ accepted answer to the cross-site universality
  question at random-walk resolution; lane stops unless a genuinely different
  instrument is proposed. The team invokes exactly this horizon and proposes
  no self-serving extension.
- Bounded wording (prereg §8 / report §3): conclusions restricted to THIS
  representation family × these two fine-grained targets × uniform
  random-walk sampling × these nine sites. Limitations §7 correctly lists
  untested families (lexical/content-level targets), power limits (769 rows,
  strict α/fold-majority demands), settle-time instrument asymmetry, and
  ephemeral raw DOM (loss disclosed; compact rows preserve every analyzed
  field). WP-004 identifiability remains BLOCKED and untouched — no
  committor/barrier overreach anywhere.
- Ledger entry (`docs/PHYSICS_LEDGER.md`) is append-only, marks the result
  "TEAM RESULT, pending independent audit", and matches the artifacts.

## 2. Failure modes searched for and NOT found

Target/post-state leakage; lagged-variable misalignment (prev_action chain
validated on all 875 rows, contiguity + alignment violations = 0); hidden
site/task identifiers; duplicated content across folds; pooled/transductive
encoding; Python `hash()` seeds (grep + P4 formula check; sha256 offsets
only); Gaussian-jitter uncertainty; degenerate frequency null accepted as
strong; unmatched denominators (all predictors scored on the identical
per-fold subset; harsh variant uses the correct full-holdout denominator);
post hoc rule changes (pipeline rerun reproduces stored artifacts bit-exact —
rules could not have been silently altered after seeing outcomes without
leaving inconsistency, and none exists); hand-coded decomposition; editing of
Graph-lane or shared history files (three-dot diff vs merge-base `086e287`
touches ONLY Physics-lane files).

## 3. Findings that limit (non-blocking)

- **L1 (process, minor)**: `verify_wp005.py` re-derives TARGETS with its own
  implementations but imports predictor/scoring helpers (`lr_predict_local`,
  `nn_predict`, `balanced_acc`, `onehot_expand`, `build_action_block`) from
  the analysis modules — so the "independent verification" is independent in
  target derivation and bookkeeping but NOT in learner/metric code. A shared
  bug there would escape it. Mitigated in THIS audit by my fully independent
  recomputation agreeing on the verdict; future verifiers should implement
  their own metric+learner reference path.
- **L2 (wording, trivial)**: report §2 parenthetical "(gutenberg 0.90,
  others 1.00)" — openlibrary T1 coverage is 0.97 in the stored JSON. The
  "coverage ≥ 0.90" statement holds; one enumeration digit is wrong in prose
  only (artifacts correct).
- **L3 (power, inherent)**: small folds (hackernews 25, internet 27,
  openlibrary 36 confirmed rows) make per-fold estimates noisy; the frozen
  design already handles this conservatively (ties count against; fold
  majority; strict α), and mean_D is negative regardless, so this weakens
  no conclusion drawn.

None of L1–L3 is repairable-relevant: L1/L2 are recorded for provenance and
the next directive; converting them into required fixes would be bureaucracy,
not integrity repair. They do not affect the verdict's validity or honesty.

## 4. Corrected interpretation (what the Director should integrate)

WP-005 is a measurement-valid FALSIFIED result: at fine granularity
(URL-shape transition class; DOM-diff signature), a state+action predictor
trained on 8 sites does NOT beat action-type semantics, training-free
inertness, or site-local 1-NN memory on the held-out site, under true
leave-one-site-out holdout with train-only fitting and atomic single-action
transitions. Combined with audited cycle 1 (coarse family), the accepted
answer to the lane's cross-site universality question is negative at BOTH
tested granularities under uniform random-walk sampling — bounded to this
instrument family. Apparent response predictability decomposes into
persistence/diff inertia + site-local retrieval + generic action-type
semantics. Per the pre-declared Director horizon, the passive random-walk
instrument is exhausted; continuation requires a genuinely different
instrument (e.g., deliberate restart/matched-state designs aimed at the
WP-004 identifiability gate) with a fresh preregistration.

## 5. Required fixes

None. `required_fixes = []`. The gate is PASS with `safe_to_integrate: true`.

## 6. Provenance of this audit

Independent artifacts (auditor-generated, outside team history):
`/tmp/opencode/audit_wp005/independent_recompute.py`,
`/tmp/opencode/audit_wp005/independent_summary.json`,
sandbox reproduction of the frozen pipeline + verifier under
`/tmp/opencode/audit_wp005/repro/` (output compared byte-for-byte against
committed `results/physics/wp005_results.json`). Team files untouched.
