# EXP-GRAPH-38046502943 preregistration

DESIGN status: MANDATE-INFEASIBLE, FAIL LOUD. This packet is a pre-freeze constructibility certificate for the `>= 2`-anchor value-only-rotation (D1V) frame mandated by the Global Research Director. The certificate verdict is NEGATIVE and the DESIGN therefore fails loudly instead of freezing an experiment, per `research/portfolio/POLICY.md` line 115 ("If the mandate is infeasible, fail loudly. Do not invent a substitute research direction.") and the mandate's own explicit fail-loud/park fallback. No `freeze.json` is produced; `spec.freeze_eligibility` marks `decision_rule_reachability` and `baseline_identifiability` FAIL, which the deterministic freezer refuses.

This document is the durable bounded reason required by the mandate. It is NOT a frozen EXECUTE driver, NOT a claim update, and NOT a product decision.

## 1 Binding inputs

- `request.json` — `EXP-GRAPH-38046502943`, lane `graph`, claim `C-FRESHNESS`, `design_contract_version: 2`, `chain_depth: 0`.
- `director_mandate.allocation`: action `CONTINUE`, target claim `C-FRESHNESS`, `cognitive_reset: true`, `parent_handoff_disposition: USE`, with an explicit fail-loud/park fallback.
- Parent handoff: `research/experiments/EXP-GRAPH-37992949248/handoff.json`, sha256 `4dd5f69fc4909b8531e1901a1dc0cef5ad3eb76f18d1c2581ba797124a51c780`.

The mandate is binding. The parent handoff is continuity evidence only. Its `carry_forward` distinctions are preserved as inherited scientific state (see section 6), not treated as an automatic research agenda.

## 2 The mandate question (verbatim)

> On credential-free, server-rendered, no-JavaScript GET-only anchors, is a value-only-rotation (D1V: STALE AND NOT structural_change AND NOT transport_change) population spanning >= 2 independent anchors constructible AT ALL such that the anchor-clustered 97.5% lower bound of the incumbent value-blind guard's false-accept differential (M-PAIRED-FA-DIFF-D1V) is non-degenerate and M-N-D1V-ANCHORS >= 2 — either by admitting a materially different anchor population whose transport validators (ETag, Last-Modified, Cache-Control max-age, Vary, final_url) are provably independent of the rotating value, or by a principled instrument change that reclassifies transport-validator motion caused solely by the rotating value itself, with that reclassification justified structurally rather than assumed? The DESIGN must produce a pre-freeze constructibility certificate for the >= 2-anchor D1V frame (the exact anchors, the per-anchor transport-change cause, and the arithmetic showing the estimator is powered), and if no such population is constructible on this substrate it must FAIL LOUDLY and return the decisive positive-control-backed bounded reason that parks the four-anchor Part II route — so that freshness effort can then move to a broader-population guard false-accept/calibration measurement or another sub-mechanism, rather than freeze another structurally degenerate single-anchor read.

## 3 Pre-freeze constructibility certificate (NEGATIVE)

### 3.1 Frozen definitions (inherited, unchanged)

- **D1V**: STALE (byte-exact live value != recorded value) AND NOT `structural_change` AND NOT `transport_change`.
- **structural_change**: the `structure_signature` (type_class, form_action, form_method, sorted form_input_names) differs.
- **transport_change**: the `transport_signature` (ETag, Last-Modified, Cache-Control max-age, Vary) OR the `final_url` differs.
- **Guards**: `B-INCUMBENT-SIGNAL-ONLY` REUSEs iff none of CH-STRUCT-SIG / CH-TRANSPORT-VALIDATOR / CH-POSTCOND-SEM fires; `B-VALUE-AWARE` REUSEs iff live == recorded; false_accept = STALE label AND REUSE.

### 3.2 Exact anchors and per-anchor transport-change cause

The accepted credential-free, server-rendered, no-JavaScript GET-only repertoire is CAL-POS-1..4 (CAL-POS-5 retired: 404x4), K=4 fresh sessions, stdlib HTTP, one egress path, at two accepted capture dates (grandparent 2026-10-09, parent 2026-10-10).

| anchor | D1V blocker | byte-level transport-change cause |
|---|---|---|
| CAL-POS-1 | `BODY_DERIVED_ETAG` | On all four sessions `ETag == W/"<sha256(body)[:32]>"`; the body differs across sessions in many regions (per-request nonces, per-session `authenticity_token`), so any value rotation forces `transport_change`. `M-TRANSPORT-BODY-DERIVATION-CAL-POS-1 = true`. |
| CAL-POS-2 | `NONE` | The sole D1V anchor: transport signature and `final_url` are constant across sessions while the extracted in-list values rotate. Contributes all `M-N-D1V = 6` trials. |
| CAL-POS-3 | `TOKEN_BEARING_FINAL_URL` | `final_url` is distinct on all sessions, each carrying a 32-hex `centralauthLoginToken` that is NOT the rotating in-list `wpLoginToken` value. The transport change has an independent cause. |
| CAL-POS-4 | `NO_FIELD` | No value-bearing in-list fields in the retained bytes on any session; no trials can form. |

Re-derived at DESIGN on BOTH corpora with the frozen parent machine: `M-N-D1V = 6`, `M-N-D1V-ANCHORS = 1`, `anchors_with_d1v = ['CAL-POS-2']`, `M-D1V-BLOCKED-ANCHORS = 3`, `M-N-POSTCOND-DRIFT = 0`, `M-N-STRUCT-DRIFT = 16`, `M-N-TRANSPORT-DRIFT = 36`, `gate_b_branch = DATA-INSUFFICIENT-D1V-DEGENERATE`, `M-D1V-DEGENERACY-MODE = ANCHOR_TRANSPORT_COUPLING`, `LOW = null`, `UB97 = null`, and `M-TRANSPORT-COUPLING-STABILITY = UNCHANGED` on all four anchors at both dates. These equal the values published by the accepted packets.

### 3.3 Decisive degeneracy argument (why the mandate's positive object is unreachable)

Even if `M-N-D1V-ANCHORS >= 2` were achieved, the mandated non-degenerate bound cannot exist on this substrate:

1. On a D1V trial the incumbent `B-INCUMBENT-SIGNAL-ONLY` REUSEs unless CH-STRUCT-SIG, CH-TRANSPORT-VALIDATOR or CH-POSTCOND-SEM fires.
2. CH-STRUCT-SIG and CH-TRANSPORT-VALIDATOR are false by the D1V definition (no structural change, no transport change).
3. CH-POSTCOND-SEM (in-list field-name-set drift) is false on the accepted repertoire: `M-N-POSTCOND-DRIFT = 0` on both corpora.
4. Therefore the incumbent REUSEs (false-accepts) on every D1V trial — the **ceiling**.
5. D1V requires STALE (live != recorded), so `B-VALUE-AWARE` ABSTAINS on every D1V trial — the **floor**.
6. The per-trial paired false-accept differential is therefore identically 1 on every D1V trial. The anchor-clustered bootstrap of a constant 1 over ANY number of anchors returns the **zero-width interval [1, 1]**. There is no within-anchor variation to power a non-degenerate bound.

A non-degenerate read would require within-anchor variation of the incumbent decision, i.e. CH-POSTCOND-SEM field-name-set drift co-occurring with D1V. That is (i) absent on the accepted repertoire, (ii) a second independent channel rather than value-only rotation, and (iii) not pre-certifiable for a new anchor population without outcome-bearing anchor screening, which DESIGN is forbidden to perform. The estimator is not the problem; the object is.

### 3.4 Powered-estimator arithmetic (positive controls, verified at DESIGN)

The frozen estimator `estimator.anchor_clustered_paired_fa_diff` (B=10000, seed `37992949248`) is capable of non-degenerate output:

- `SYN-ESTIMATOR-2ANCHOR`: `LOW = 1/3`, `UB97 = 1/2`, `LOW < UB97`, non-degenerate.
- `SYN-ESTIMATOR-1ANCHOR`: `LOW = null`, `UB97 = null` (never 0.0).
- `SYN-ESTIMATOR-HOMOGENEOUS`: `[1/2, 1/2]` zero-width.
- `SYN-POWER-2ANCHOR-D1V`: 12 D1V trials over 2 pseudo-anchors + 1 FRESH trial -> `INCUMBENT-BLIND-CONFIRMED`, `LOW = 2/3`, `UB97 = 1.0`, pooled diff `10/12`, `M-N-D1V-ANCHORS = 2`.

`SYN-POWER-2ANCHOR-D1V` is powered ONLY because it injects within-anchor incumbent ABSTAINs (postcond drift) that do not exist in the real D1V family. This shows the degeneracy is a population/object property, not an estimator-power failure.

### 3.5 Mandate remedy (b): rejected at byte level

No structural, non-circular reclassification of transport motion can move CAL-POS-1/CAL-POS-3 into D1V: CAL-POS-1's ETag is a deterministic transform of the whole body (non-value deltas present), CAL-POS-3's `final_url` token has an independent cause, and CAL-POS-4 has no fields. Even if CAL-POS-1 were reclassified, section 3.3 still yields `[1, 1]`.

### 3.6 Mandate remedy (a): UNKNOWN and out of scope

Admitting a materially different anchor population requires outcome-bearing screening outside the accepted CC-A bound. It is UNKNOWN, not certified, and is handed to the Director. It is `do_not_assume`.

## 4 Controls

- `PC-ESTIMATOR-NONDEGENERATE`, `PC-ESTIMATOR-POWER-DEMO`, `PC-GUARD-LOGIC`, `PC-EXTRACTION-CANARY`, `PC-CERTIFICATE-RE-DERIVATION`.
- `NC-ESTIMATOR-CONTROL-SENSITIVITY`, `NC-EXTRACT-EMPTY-VALUE`, `NC-EXTRACT-JSSTRING`, `NC-PATH-INDEPENDENCE`, `NC-CROSS-CORPUS-REPRODUCTION`, `NC-CERTIFICATE-HASH`, `NC-NETWORK-CONTROL`, `NC-NO-FIELD-ANCHOR`.

DESIGN satisfiability probes (cheap, non-outcome-bearing, no new capture) imported the frozen parent modules and ran: fixtures (`CANARY_PASS=true`, `EMPTY_AGREE=true`, `JSSTRING=0`, `GUARD_FIXTURE_PASS=true`), estimator controls (`POS_CTRL=true`, `NC_SENS=true`), `path_independence_attestation` (`pass=true`), the frozen synthetic estimator fixtures above, and re-derivation of both retained corpora against the accepted published values (all equal).

## 5 Stable metric and control identities (reusable downstream)

Metrics: `M-PAIRED-FA-DIFF-D1V` (+ `-LOW`/`-UB97`), `M-N-D1V`, `M-N-D1V-ANCHORS`, `M-N-D1V-BLOCKED-ANCHORS`, `M-N-DECISIONS-D1V`, `M-D1V-BLOCKER-{anchor}`, `M-TRANSPORT-BODY-DERIVATION-{anchor}`, `M-TRANSPORT-COUPLING-STABILITY-{anchor}`, `M-D1V-DEGENERACY-MODE`, `M-N-POSTCOND-DRIFT`, `M-N-STRUCT-DRIFT`, `M-N-TRANSPORT-DRIFT`, `M-FA-INCUMBENT-D1V`, `M-FA-VALUEAWARE-D1V`. Controls: the `PC-*`/`NC-*` ids above. These identifiers are preserved verbatim so EXECUTE/AUDIT/DIRECTOR can refer to the exact same objects.

## 6 Inherited carry_forward (preserved, not rewritten)

- **Established**: GATE-C3 session-isolation predicate repaired and passing 8/8; extraction-defect confirmed and replicated (dual-path 4/4); transport-value coupling time-stable (`M-TRANSPORT-COUPLING-STABILITY=UNCHANGED` on all four anchors across two captures); estimator certified powered (GATE F PASS; `{1/2, 1/3}` -> `LOW 1/3`, `UB97 1/2`).
- **Rejected**: the four-anchor Part II route re-run under the same transport signature (CC-I).
- **Unknown**: broader-population constructibility; NO_FIELD-vs-token-list-limit distinction; whether any credential-free GET-only anchor has independent transport validators. All marked `do_not_assume`.

## 7 Why this is a DESIGN failure, not MEASUREMENT_INVALID

The certificate does not rest on a broken substrate. The retained corpora are present and hash-consistent, the frozen instrument imports cleanly and its canaries/controls PASS, and the estimator is demonstrably powered. The disposition is a DESIGN failure because the mandate's required positive branch is empty/unreachable (`decision_rule_reachability`) and the treatment/comparator pair is a guaranteed ceiling/floor on the object under test (`baseline_identifiability`). Encoding this honestly at DESIGN is cheaper and more informative than freezing an invalid or foregone measurement, exactly as the mandate requests. Nothing here falsifies `C-FRESHNESS` and nothing here is `MEASUREMENT_INVALID`.

## 8 Evidence and hashes

- Parent `result.json` sha256 `9156e97dd95858ded8942459aa6d7350b1b1635197048a47089af1af622ba97f`.
- Parent `freeze.json` sha256 `64450207760e901b733dbb011125d2938d26ad06106bde5076dd3277b7a32134`.
- Parent `raw/records.jsonl` sha256 `bdef74f6219ef0b2b8f18917fafffe3fac4eeb4cc7dcd98012017b426f5fc32f`.
- Grandparent `raw/records.jsonl` sha256 `00b60903320447799039d9f004da41d504d64e18f722353993c6a435fb8555e2`.
- Frozen instrument: `research/experiments/EXP-GRAPH-37992949248/code/` (7 modules).

## 9 Consequences

- The four-anchor Part II route is PARKED.
- `C-FRESHNESS` remains EXPERIMENTAL (`codex/claim_state.json` `effective_event_by_claim`). No claim event is emitted by this packet.
- No product promotion and no product behaviour change.
- Redirect (Director decision, not self-authorized): broader-population guard false-accept/calibration measurement, or another freshness sub-mechanism.

## 10 Falsifier (would revoke the park)

`F-POSITIVE-CONSTRUCTIBLE`: a pre-freezable demonstration, from already-accepted evidence and a structurally justified non-circular reclassification, of a `>= 2`-anchor D1V population whose anchor-clustered `M-PAIRED-FA-DIFF-D1V` 97.5% interval has `LOW < UB97`. Expected-empty on the accepted substrate.

## 11 Unresolved / do_not_assume

- Broader-population constructibility: UNKNOWN (CC-A bound); do_not_assume either way.
- Do NOT re-freeze the four anchors under the same transport signature expecting a non-degenerate Part II read (CC-I, SA-07).
- Do NOT read false-accept/blindness/value-awareness-necessity from the single-anchor descriptive point estimates.
- The `NO_FIELD` vs token-list-limit distinction for CAL-POS-4 remains an inherited unknown.
