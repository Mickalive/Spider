# EXP-GRAPH-37992949248 preregistration

Lane: graph. Claim: **C-FRESHNESS** (only). Director mandate cycle_id **37991758372**, action
`CONTINUE`, target claim C-FRESHNESS, parent_handoff_disposition `SUPERSEDE`.
Parent: `EXP-GRAPH-37978902447` (handoff sha256
`6d576cc5fd0bd22ed4a4c5c7cb1853be1eaee78e65701ba3a4a3728b7a8b7d68`).

This preregistration is written before any anchor is contacted in this transaction. No
outcome-bearing measurement was performed during DESIGN. The only DESIGN computation is a
synthetic, network-free satisfiability/identifiability dry-run recorded in
`spec.pre_freeze_satisfiability_dry_run`; it cannot pre-empt the confirmatory objects
(extraction validity, guard behaviour, per-anchor D1V coverage).

## 1. What the Director asked, and how this design answers it

The mandate asks to **complete PART II of C-FRESHNESS on the four pinned credential-free
anchors**: obtain `M-N-D1V >= 6` spanning MORE THAN ONE anchor so that the incumbent
value-blind guard's false-accept differential `M-PAIRED-FA-DIFF-D1V` is evaluable with a
non-degenerate anchor-clustered 97.5% lower bound, and to report
`EXTRACTION-DEFECT-CONFIRMED` (E3 PASS, D1 >= 3/4) **or the bounded reason why the
population remains degenerate**.

The mandate contains an explicit escape clause: the bounded reason is an acceptable
deliverable. This design pre-registers **both** a reachable guard-differential read and a
reachable, fail-loud feasibility/degeneracy certificate, so that neither branch is empty.

The parent proved on its own capture that the four anchors yield a **single-anchor** D1V
population (`M-N-D1V=6`, `M-N-D1V-ANCHORS=1`, only CAL-POS-2) and that the anchor-clustered
lower bound is therefore degenerate by construction. The parent handoff explicitly warns
*not* to re-freeze the same four anchors under the same transport signature and expect a
different result. This experiment therefore does **not** merely repeat the parent: it adds a
new object that decides *why* the bound is degenerate and whether the estimator is even
capable of the non-degenerate read the mandate wants.

## 2. Hypotheses

- **H-MAIN (Part I, replication).** With the corrected GATE-C3 predicate
  (`first_request_cookieless AND pairwise_disjoint_on_name_value_after_filter`, with
  `session_identifying_disjoint` demoted to a non-gating diagnostic), both independently
  written stdlib paths recover >=2 distinct non-empty exact values on >=3 of 4 anchors and
  agree (`M-EXTRACT-AGREE-VALUESET >= 3` AND `M-EXTRACT-AGREE-VERDICT >= 3`), so
  `M-N-SESSION-SCOPED-CONFIRMED >= 3 of 4` and branch `EXTRACTION-DEFECT-CONFIRMED`
  replicates on a fresh capture.
- **H-GUARD (Part II, read only if D1 and GATE F pass and the population is evaluable).**
  `M-PAIRED-FA-DIFF-D1V >= 0.10` with anchor-clustered 97.5% lower bound `> 0` **and a
  positive-width interval (`LOW < UB97`)**, i.e. the value-blind incumbent false-accepts real
  value-only rotation more than the value-aware comparator. Evaluability requires `M-N-D1V >= 6`,
  `M-N-DECISIONS-D1V >= 2` for the **incumbent** guard (pinned per-guard: a structurally constant
  incumbent realises only `REUSE` on strict D1V and must not be called non-degenerate by the
  value-aware comparator's trivial `ABSTAIN`s), `M-N-D1V-ANCHORS >= 2`, non-degeneracy of all
  active channels (with the pre-declared `INACTIVE-ON-POPULATION` waiver), and a realized
  positive-width interval. The parent reported `M-N-DECISIONS-D1V=2`, but that was the *union*
  across both comparators; under this pinned definition the parent incumbent realised only 1.
- **H-FEAS (decision-enabling; the mandate's escape clause).** The D1V population on the
  frozen four anchors spans **exactly one** anchor because the frozen `transport_signature`
  is: a body-derived ETag on CAL-POS-1 (`BODY_DERIVED_ETAG`), a per-session
  `centralauthLoginToken` in `final_url` on CAL-POS-3 (`TOKEN_BEARING_FINAL_URL`), and
  `NO_FIELD` on CAL-POS-4. Hence `M-N-D1V-ANCHORS == 1` and branch
  `DATA-INSUFFICIENT-D1V-DEGENERATE`, with `M-D1V-DEGENERACY-MODE ==
  ANCHOR_TRANSPORT_COUPLING`.
- **H-ESTIMATOR (positive/negative control).** The anchor-clustered bootstrap is *capable* of a
  non-degenerate bound and its width tracks between-anchor heterogeneity: on the synthetic
  heterogeneous 2-anchor fixture (paired false-accept differences 1/2 and 1/3, both strictly
  inside (0,1)) it returns `LOW = 1/3 > 0`, `UB97 = 1/2 < 1` and `LOW < UB97`; on the synthetic
  single-anchor fixture it returns the degenerate/null bound; and on the synthetic homogeneous
  2-anchor fixture (both differences 1/2) it returns a zero-width interval. Therefore a live
  single-anchor degeneracy is attributable to the population, not to the estimator. (An earlier
  drafted {1,0} fixture was rejected during DESIGN self-attack: with 2 anchors it yields
  `LOW = 0`, `UB97 = 1`, making the positive control arithmetically unsatisfiable.)

## 3. Falsifiers (all pre-labelled)

`F-CERT` (certificate failure -> MEASUREMENT_INVALID), `F-INSTR` (instrument insensitivity),
`F-ESTIMATOR` (**new**: the heterogeneous 2-anchor control fails to return `LOW>0`,
`UB97<1` and `LOW<UB97`; or the single-anchor control returns a non-null bound; or the
homogeneous 2-anchor control returns a non-zero-width interval -> the bootstrap is defective
and **no degeneracy/feasibility claim may be made**), `F-REPLOSS`, `F-UNRELIABLE`, `F-BLIND`
(`M-PAIRED-FA-DIFF-D1V < 0.10` or `LOW <= 0` -> `INCUMBENT-NOT-BLIND`), `F-BLIND-DEGENERATE`
(`M-N-D1V-ANCHORS < 2`), and **`F-NONDEGENERATE`** (new: `M-N-D1V-ANCHORS >= 2` on the fresh
capture falsifies H-FEAS and triggers the GATE-B read).

## 4. Frozen design

The anchors (`CAL-POS-1..4`), negatives (`CAL-NEG-1..4`), K=4 fresh cookie-free sessions,
the two independently written stdlib extraction paths, the AGSI instance keying, the frozen
token-name list, the four-channel guard, the D1V definition, the `transport_signature` and
the anchor-clustered bootstrap unit are inherited **unchanged** from the parent. No threshold
is re-fit, no new anchor is admitted, no transport or D1V redefinition is authorized
(`SB-05`, `SB-06`). The only additions are:

1. **GATE F** (estimator capability) before any GATE-B read, with
   `PC-ESTIMATOR-NONDEGENERATE` (`SYN-ESTIMATOR-2ANCHOR`) and
   `NC-ESTIMATOR-CONTROL-SENSITIVITY` (`SYN-ESTIMATOR-1ANCHOR` + `SYN-ESTIMATOR-HOMOGENEOUS`)
   computed by the *same* bootstrap function as the real read (`V16`). The positive control
   requires `LOW > 0`, `UB97 < 1` **and** `LOW < UB97` (reference arithmetic `LOW = 1/3`,
   `UB97 = 1/2`), so a point interval cannot masquerade as non-degenerate.
2. **`M-D1V-DEGENERACY-MODE`**, which attributes a degenerate bound to
   `ANCHOR_TRANSPORT_COUPLING` vs `ESTIMATOR_DEGENERATE`.
3. **`M-TRANSPORT-COUPLING-STABILITY-{anchor}`**, testing whether the parent's per-anchor
   blocker is time-stable or whether a fresh capture re-opens a second D1V anchor.
4. Zero-extra-cost **descriptive** value-rotation-any-transport metrics, explicitly
   `do_not_use` for gates (`CC-K`).

The estimator control fixtures are instrument unit tests on synthetic pseudo-anchors and are
**never scored** (`CC-J`).

## 5. Decision rule (ordered, fail-closed)

GATE C certificate (C1 route/field; C2 negatives = 0; C3 corrected predicate + non-vacuous) ->
`F-CERT`/MEASUREMENT_INVALID on failure. GATE F estimator capability -> `F-ESTIMATOR` on
failure. GATE E instrument (canary, fixtures, path-independence, trial-construction
stability) -> `F-INSTR` on failure; E3 agreement -> `EXTRACTION-UNRELIABLE` if it fails, else
D1 `EXTRACTION-DEFECT-CONFIRMED` / D2 `REPRESENTATION-LOSS-CONFIRMED` / D3 `MIXED-ANCHORS`.
GATE B (Part II, only if D1 and GATE F pass): if not evaluable, `DATA-INSUFFICIENT-D1V` or
`DATA-INSUFFICIENT-D1V-DEGENERATE` (with the degenerate mode and blockers), else
`INCUMBENT-BLIND-CONFIRMED` / `INCUMBENT-NOT-BLIND`. GATE B is non-status-changing.

## 6. Claim ceilings and scope

All results are scoped to the four pinned credential-free, server-rendered, no-JavaScript,
GET-only anchors, K=4 fresh sessions, stdlib HTTP, one capture date and one egress ASN
(`CC-A`). **This packet does not advance C-FRESHNESS**: Part I is a replication and Part II is
expected to remain degenerate; any status change is the DIRECTOR's decision (`CC-B`). A
degenerate Part II is a **power/feasibility statement**, not a blindness, necessity or
prevalence result, and does not falsify C-FRESHNESS or the freshness mechanism (`CC-I`,
`SB-08`). `M-INVISIBLE-STALE-PREV` is reported `null`, never `0.0` (`SB-04`). No product
promotion or replay-by-assumption is authorized.

## 7. Timing, seed and evidence

Frozen seed `37992949248`; bootstrap B=10000, percentile method, resampling anchors. Raw
bodies and per-request records are retained and re-analyzable (`V10`); frozen inputs are
re-verified before and after execution (`V11`). `request.json`, `spec.json` and `prereg.md`
are immutable after `freeze.json`.

## 8. DESIGN self-attack (recorded pre-freeze)

DESIGN actively tried to disprove its own satisfiability (details in
`spec.pre_freeze_satisfiability_dry_run.self_attack_findings`). Binding fixes, not EXECUTE
surprises:

- **SA-01 (blocking).** The first estimator positive-control fixture (`{1,0}` per-anchor
  differences) was arithmetically unsatisfiable for `LOW>0 AND UB97<1`; replaced with the
  heterogeneous interior fixture `{1/2, 1/3}` (`LOW=1/3`, `UB97=1/2`), verified by a synthetic
  pre-freeze probe.
- **SA-02 (blocking).** `ANCHOR_TRANSPORT_COUPLING` was unreachable because CAL-POS-4 is
  `NO_FIELD`; the mode is now defined over *value-bearing* non-D1V anchors only.
- **SA-03 (major).** `M-N-DECISIONS-D1V` was an across-comparator union in the parent; it is now
  pinned to the incumbent guard (parent value would be 1, not 2).
- **SA-04 (major).** Equal per-anchor rates produce a degenerate interval even with >=2 anchors;
  a pre-registered positive-width (`LOW < UB97`) evaluability condition was added.
- **SA-05/SA-06 (minor).** Orphan feasibility branch now emitted; GATE-C3 truth-table
  post-filter fields made consistent with the predicate.
- **SA-07 (disclosed residual).** Uniform incumbent blindness yields a degenerate `[1,1]`
  interval even with `M-N-D1V-ANCHORS >= 2`; the non-degenerate read additionally requires
  within-anchor incumbent variation, pre-declared with a reachable
  `DATA-INSUFFICIENT-D1V-DEGENERATE` / `ANCHOR_SCARCITY_OTHER` fallback.

All estimator fixtures, the corrected predicate and every decision branch were checked
satisfiable on pinned synthetic inputs before freeze (`V15`).
