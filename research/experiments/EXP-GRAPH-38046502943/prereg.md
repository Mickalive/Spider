# PREREGISTRATION — EXP-GRAPH-38046502943

**Design-contract version 2 — DESIGN_ONLY_FAIL_LOUD_CERTIFICATE (no EXECUTE phase)**

Status: preregistered PRIOR TO any freeze attempt and PRIOR TO any outcome-bearing
measurement ("guard decision / false-accept" computation). The design-time satisfiability
probe produced drift labels and headers/body-hash facts only (mandate option A allowance).

---

## 1. Identity

- experiment_id: `EXP-GRAPH-38046502943`
- lane: GRAPH
- claim: `C-FRESHNESS` — the freshness guard protects storage-cache REUSE decisions
  against stale web-form values via transport metadata and value-recency signals.
- parent: `EXP-GRAPH-37992949248` (frozen packet; claim state C-FRESHNESS EXPERIMENTAL,
  bounded by a single-anchor degenerate read).
- grandparent: `EXP-GRAPH-37978902447` (raw records capture date 2026-10-09).
- director mandate (request.json): CONTINUE on C-FRESHNESS with option A — bounded
  design-time screen; freeze a powered Part II read IF constructible on a materially
  different population; otherwise emit a fail-loud certificate with exact anchors,
  per-anchor transport-change cause, estimator power arithmetic, positive/negative
  controls, and park the route with a bounded reason. CAL-POS-1..4 must not be refetched.

## 2. Question

Is there a constructible >=2-anchor D1V frame on a materially different population on
which a powered non-degenerate `M-PAIRED-FA-DIFF-D1V` read can decide
INCUMBENT-BLIND-CONFIRMED vs INCUMBENT-NOT-BLIND?

Definitions (frozen, inherited): D1V = value STALE AND NOT structural_change AND NOT
transport_change. Per-anchor incumbent FA on the D1V subset = 1.0 by the closed-form
guard theorem (no channel fires => REUSE); value-aware FA = 0.0 (CH-PRECOND-BINDING
always fires). The pooled estimator is non-degenerate (LOW < UB97) iff some anchor has
per-anchor incumbent FA != 1.0 iff CH-POSTCOND-SEM fires on at least one D1V pair.

## 3. Pre-declared branches

- Branch A (certificate PASS): a constructible >=2-anchor frame with >=2 D1V trials on
  which the would-be read would realize a non-degenerate interval (LOW > 0 AND
  LOW < UB97) => propose freeze and EXECUTE the powered Part II read.
- Branch B (certificate FAIL_LOUD): no such frame constructible; the would-be read
  deterministically lands in DATA-INSUFFICIENT-D1V-DEGENERATE => decision_rule_reachability
  = FAIL, freeze refused, certificate is the terminal deliverable, route parked with
  bounded reason, no claim-change, product answer for C-FRESHNESS remains UNKNOWN.

Both branches are acceptable scientific outcomes. The certificate does not decide
blindness; it decides whether a powered read is constructible.

## 4. Design-time satisfiability probes (non-outcome-bearing)

Licensed by mandate option A under the v2 pre-freeze allowance. These produce drift
labels, headers, hashes, and satisfiability arithmetic — never guard decisions or
false-accept metrics on live evidence.

4.1 Zero-network instrument controls (local fixtures, no network):
- M-FIXTURE-CANARY-PASS, M-FIXTURE-EMPTY-AGREE, M-GUARD-FIXTURE-PASS.
- Frozen estimator at its binding (B = estimator.DEFAULT_B = 10000, seed = FROZEN_SEED =
  37992949248 — identical to a would-be EXECUTE):
  - SYN-ESTIMATOR-2ANCHOR (heterogeneous): expect non-degenerate LOW=1/3, UB97=1/2 (PASS).
  - SYN-ESTIMATOR-1ANCHOR: expect degenerate, reason n_anchors<2.
  - SYN-ESTIMATOR-HOMOGENEOUS (2 anchors, equal per-anchor FA): expect zero-width
    [0.5,0.5], reason zero_width_interval — the population-diagnostic showing
    zero-width is not an estimator failure.
- PC-POSTCOND-CLASSIFIER-SENSITIVITY (SYN-POSTCOND-HET: differing in-list field-name
  sets): expect CH-POSTCOND-SEM to FIRE, all guard variants ABSTAIN.
- NC-POSTCOND-NULL (SYN-POSTCOND-NULL: identical field-name sets): expect CH-POSTCOND-SEM
  NOT to fire; incumbent REUSE, value-aware ABSTAIN (CH-PRECOND-BINDING fires).

4.2 Inherited-evidence replay: reconstruct the parent trial matrix from frozen raw
records with parent-exact construction; expect exact reproduction (48 trials;
CAL-POS-2: 6 D1V, 0 postcond drift; CAL-POS-1: 24 trials; CAL-POS-3: 12 trials).

4.3 Live candidate screen (K=4 cookieless GET-only sessions per candidate, fresh empty
CookieJar per (anchor,session), no JS, no submissions, pacing >=3.0s, 10 candidates,
iana.org control before/after; 42 requests total on 2026-10-10 12:51:42Z..12:53:19Z):
- Record per session: status, final_url, headers (ETag, Last-Modified, Cache-Control,
  Vary), body_sha256 (verify against recomputed hash), extracted in-list fields and
  byte-exact values where VALUE-state, session in-list field-name set.
- Classify every pair per frozen definitions; verify path A/B pair-set agreement on all
  40 sessions.
- NO guard decision and NO false-accept number is computed on live evidence at any point.

## 5. Decision inputs and pre-declared branch determinacy

The two decisive branches are reachable ONLY via a would-be read with LOW > 0 AND
LOW < UB97 (Branch A) vs the realization that this is arithmetically impossible on the
observed population because per-anchor incumbent FA = 1.0 on every D1V-capable anchor
(0 postcond fires) => LOW == UB97 == 1.0, and pooled = 1.0 => INCUMBENT-NOT-BLIND also
unreachable (Branch B).

Note: a would-be frame satisfying M-N-D1V-ANCHORS>=2 and M-N-DECISIONS-D1V>=2 is NOT
sufficient for Branch A — the interval must also be non-degenerate. This was the exact
gap of the prior attempt's planned read.

## 6. Controls (stable ids, reused by EXECUTE/AUDIT)

- PC-CLASSIFIER-SENSITIVITY: inherited-evidence replay reproduces parent drift facts.
- PC-EXTRACTION-CANARY: PA.extract byte-identical value recovery on live + inherited.
- PC-POSTCOND-CLASSIFIER-SENSITIVITY: CH-POSTCOND-SEM fires when in-list field sets differ.
- NC-POSTCOND-NULL: CH-POSTCOND-SEM silent when field sets identical.
- PC-ESTIMATOR-NONDEGENERATE: frozen estimator non-degenerate on heterogeneous synthetic.
- NC-ESTIMATOR-CONTROL-SENSITIVITY: frozen estimator 1-anchor and homogeneous forms.
- NC-OPEN-GET-ONLY, NC-CREDENTIAL-FREE, NC-NETWORK-CONTROL (iana.org 200 before/after).

## 7. Validity disciplines

- V01 probe-session exclusion: probe sessions are never part of a future scored
  population unless re-harvested under frozen EXECUTE.
- V02 substrate re-verification for any future EXECUTE.
- V03 classifier continuity + path A/B agreement.
- V04 timing/pacing; new-anchor facts are single-date; union with CAL-POS-2 spans two
  capture dates (2026-10-09, 2026-10-10).
- V05 contextual rotation; no assertion about WHY values rotate.
- V06 transport-signature time-variability disclosed (P1/P6 same-day divergence).
- V07 evidence embedded verbatim in spec; recomputable by downstream auditors.

## 8. Pre-declared consequences

- Positive (Branch A, not realized): freeze + EXECUTE the powered read; blindness
  confirmation licenses channel consolidation and C-FRESHNESS route update.
- Negative (Branch B, realized): route parked; product answer UNKNOWN; no claim change;
  redirects pre-registered but NOT designed: (a) FRESH/STALE guard calibration over the
  two live D1V anchors with their constant wpEditToken controls, (b) false-outage
  calibration, (c) transport-coupling generalizability certificate
  (BODY_DERIVED_ETAG now on 3 platform families).

## 9. Scope

Only `spec.json` and `prereg.md` are written in this experiment directory. No
modification of inherited evidence; no refetch of CAL-POS-1..4; no git mutations.
Session-local probe artifacts (/tmp/opencode/) are not bound artifacts.

## 10. Timing / immutability

This preregistration is written before any freeze attempt. `spec.json` is immutable
once `freeze.json` would exist — here freeze is refused by the certificate itself, and
`spec.json` + `prereg.md` are the terminal deliverables for DIRECTOR/AUDIT review.