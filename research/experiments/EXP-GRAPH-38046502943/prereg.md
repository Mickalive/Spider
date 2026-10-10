# PREREGISTRATION — EXP-GRAPH-38046502943

**Design-contract v2 — CONSTRUCTIBILITY SCREEN WITH CONDITIONAL D1V READ**

Status: preregistered before freeze and before any outcome-bearing measurement on the
screened population. The DESIGN-time satisfiability probes were local, zero-network
instrument checks only (estimator fixtures and guard fixtures); no guard decision,
false-accept rate or interval was computed on any live evidence.

- experiment_id: `EXP-GRAPH-38046502943`
- lane: `graph`
- claim: `C-FRESHNESS` (effective registry status EXPERIMENTAL at allocation)
- parent frozen packet: `EXP-GRAPH-37992949248` (sha256 of its `handoff.json`
  `4dd5f69f...` as referenced by request.json)
- grandparent: `EXP-GRAPH-37978902447`
- Director mandate: CONTINUE on `C-FRESHNESS`; settle whether a `>=2`-anchor D1V frame
  with a **non-degenerate** anchor-clustered 97.5% lower bound is constructible on a
  materially different credential-free GET-only population; if not, park the four-anchor
  Part II route with a decisive, positive-control-backed bounded reason. `CAL-POS-1..4`
  are not refetched.

## 1. Why this experiment exists now

The inherited Part II read is degenerate for a reason that is *structural*, not
statistical: on a D1V trial the structural and transport channels are false by
definition, so the value-blind incumbent `B-INCUMBENT-SIGNAL-ONLY` REUSEs exactly when
`CH-POSTCOND-SEM` is silent, while `B-VALUE-AWARE` always ABSTAINs (the value rotated).
The paired per-trial differential therefore equals the postcond-silence indicator. A
non-degenerate anchor-clustered interval exists **iff** at least one D1V trial realizes a
postcond fire so the incumbent D1V decision set is `{REUSE, ABSTAIN}` and per-anchor
REUSE rates differ. The parent proved the estimator can produce such an interval
(GATE F PASS) but could not power it because its D1V family spanned a single anchor
(`M-N-D1V-ANCHORS=1`). This experiment tests whether a materially different
pre-registered population supplies a `>=2`-anchor D1V frame with the required
heterogeneity, and it freezes the *decision procedure* rather than pre-committing to an
outcome.

The mandate's Route B (a structurally justified instrument reclassification of
transport-validator motion as caused solely by the rotating value) is **not** adopted:
on inherited frozen evidence the `CAL-POS-1` body-derived ETag moves with non-token body
regions (per-request nonce / correlation id) and the `CAL-POS-3` `final_url` token is a
different token from the body `wpLoginToken`, so the motion is not caused solely by the
rotating value and a reclassification would not be justified. Route A (materially
different population) is taken instead.

## 2. Pre-registered population and protocol

`spec.candidate_population` fixes 14 candidate anchors across MediaWiki, Gitea/Forgejo,
GitLab, Drupal, phpBB, NodeBB, Discourse, Redmine, Moodle and Bugzilla families, plus one
negative anchor (`NC-IANA`). No outcome-dependent additions; candidates may be dropped
only by the pre-declared unreachability/blocker rules.

Capture: `K=4` fresh cookieless GET-only sessions per candidate (fresh empty CookieJar
per session), no JavaScript, no submissions, no credentials, stdlib HTTP only, pacing
`>=3.0s`, request cap 200, one iana.org control before and after. `CAL-POS-1..4` are not
refetched.

## 3. Frozen definitions, estimator and decision rule

Definitions and the four guard variants are inherited unchanged (see
`spec.frozen_definitions`, `spec.baselines`). The estimator is the shared frozen
`anchor_clustered_paired_fa_diff` at `B=10000`, nearest-rank percentile, seed
`37992949248`, resampling unit = anchors.

Decision rule (ordered, both families reachable):

1. **READ — INCUMBENT-BLIND-CONFIRMED**: `M-D1V-POSITIVE-WIDTH=true`, `M-N-D1V>=6`,
   `M-N-D1V-ANCHORS>=2`, `M-N-DECISIONS-D1V>=2`, channels non-degenerate,
   `M-PAIRED-FA-DIFF-D1V>=0.10` and `M-PAIRED-FA-DIFF-D1V-LOW>0`.
2. **READ — INCUMBENT-NOT-BLIND**: same adequacy preconditions, but the differential is
   `<0.10` or `LOW<=0`.
3. **NO-READ — DATA-INSUFFICIENT-D1V**: adequacy (`cluster_precondition_ok`) fails with
   `M-N-D1V-ANCHORS>=2` (identically-REUSE D1V decisions, or degenerate channels).
4. **NO-READ — DATA-INSUFFICIENT-D1V-DEGENERATE**: GATE F fails, or
   `M-N-D1V-ANCHORS<2`, or the clustered interval is zero-width (`LOW==UB97`); degeneracy
   mode `ESTIMATOR_DEGENERATE`, `ANCHOR_TRANSPORT_COUPLING` or `ANCHOR_SCARCITY_OTHER`.

These labels are exactly the frozen `run_experiment.py :: guard_statistics`
`gate_b_branch` outputs (fail-closed order); EXECUTE calls that function unchanged.

Branches 1-2 precede branches 3-4, so no branch is shadowed. A NO-READ branch is a
pre-declared power/feasibility statement, never a blindness/necessity result and never a
claim-status change.

### Reachability arithmetic (why no branch is empty)

The frozen estimator at the frozen binding gives, on satisfiability constructions
(re-verified end-to-end against the bound `run_experiment.py :: guard_statistics` at
design time; no live evidence):

| construction | `gate_b_branch` | `LOW` | `UB97` | note |
|---|---|---|---|---|
| 2 D1V anchors, one at 4/6 incumbent REUSE, + `>=1` FRESH trial (value-mixed population) | `INCUMBENT-BLIND-CONFIRMED` | 2/3 | 1.0 | channels nondegenerate: POSTCOND `2/12`, PRECOND `12/2` fire/not-fire |
| same 2-anchor D1V frame but ALL-STALE (PRECOND fires on every trial) | `DATA-INSUFFICIENT-D1V` | 2/3 | 1.0 | `nondegenerate=false` despite positive width — the frozen channel rule runs over ALL trials |
| 2 anchors, every D1V pair postcond-silent | `DATA-INSUFFICIENT-D1V` / `-DEGENERATE` | [1,1] | [1,1] | zero-width, decision set `{REUSE}` |
| 1 anchor | `DATA-INSUFFICIENT-D1V-DEGENERATE` | null | null | `n_anchors<2` |

The first row is a READ (`INCUMBENT-BLIND-CONFIRMED`) and is reachable whenever a D1V
frame with postcond heterogeneity coexists with at least one FRESH trial; the latter
rows are NO-READ. Note the READ branch is only reachable on a **value-mixed** realized
population, so anchors that yield invariant values (`RECOVERED_INVARIANT`, FRESH-only)
are informative for the READ and must NOT be discarded. These are instrument
satisfiability demonstrations, not observations about the screened anchors; the realized
frame is computed only at EXECUTE.

## 4. Controls (stable ids reused by EXECUTE/AUDIT)

- `PC-ESTIMATOR-NONDEGENERATE` — `SYN-ESTIMATOR-2ANCHOR`: `LOW=1/3`, `UB97=1/2`.
- `NC-ESTIMATOR-CONTROL-SENSITIVITY` — `SYN-ESTIMATOR-1ANCHOR` null; `SYN-ESTIMATOR-HOMOGENEOUS` `[0.5,0.5]` zero-width.
- `PC-POSTCOND-CLASSIFIER-SENSITIVITY` — `SYN-GUARD-POSTCOND` fires `CH-POSTCOND-SEM`.
- `PC-CLASSIFIER-SENSITIVITY` — inherited 48-trial matrix reproduced exactly.
- `PC-EXTRACTION-CANARY` — path A/B byte-identical value recovery.
- `NC-POSTCOND-NULL`, `NC-OPEN-GET-ONLY`, `NC-CREDENTIAL-FREE`, `NC-NETWORK-CONTROL`,
  `NC-NO-FIELD-ANCHOR`.

## 5. Consequence in both directions

- **Positive (a READ):** the first multi-anchor incumbent false-accept bound on a
  credential-free GET-only population. `INCUMBENT-BLIND-CONFIRMED` supports retaining
  `CH-PRECOND-BINDING`; `INCUMBENT-NOT-BLIND` permits consolidating the value-aware
  channel. Bounded to the screened population, brand, capture date and egress path; no
  automatic promotion (DIRECTOR only).
- **Negative (a NO-READ):** the four-anchor Part II route is parked with a measured,
  positive-control-backed bounded reason (exact per-anchor transport-change causes and
  the postcond-homogeneity attribution); the product answer for `C-FRESHNESS` remains
  UNKNOWN; no claim change; budget is not spent on a structurally degenerate read.

## 6. Validity disciplines

`specific_measurement_validity` V01-V10: raw-before-derived separation, runtime substrate
re-verification, classifier continuity with path A/B agreement, single-date timing,
contextual-rotation neutrality, live transport time-variability, synthetic-fixture
boundary, standalone-driver no-reimplementation, NO-READ-as-power-statement, and
verbatim embedded evidence for downstream recomputation.

## 7. Scope and immutability

Only `spec.json` and `prereg.md` are written at DESIGN. `CAL-POS-1..4` are not refetched.
No git mutation by the agent; no shipped `src/` code is touched. Environment references
to the parent experiment are read-only `freeze_artifacts` hashed into `freeze.json`.
After freeze this file and `spec.json` are immutable inputs to EXECUTE and AUDIT.
