# EXP-PHYSICS-38121193195 preregistration

Lane: `physics` · Claim: `C-WEB-DYNAMICS` (HYPOTHESIS) · Guards: `C-MEAS-VALID`, `C-CROSSSITE`
Design contract: v2 · Reason: `global-director-REOPEN` (cycle 38120577942)
Title: Cross-vantage transfer of endpoint intrinsic access-barrier persistence and anchor-built intrinsic-denylist validity.

DESIGN NOT YET FROZEN.

## 1. Why this experiment exists

The only accepted Physics positive (`EXP-PHYSICS-38074818597`, verdict `S1_STATIONARY_ADOPTED_AUDIT_PASS`) measured
intrinsic access-barrier persistence (BLOCK_403_CHALLENGE / TRANSPORT_ERROR), an anchor-built intrinsic-denylist
validity horizon right-censored at 1800 s, and a stationarity skill of 0.3196 nats on the frozen 57-endpoint
credential-free GET pool — but on exactly ONE egress vantage. The audit itself (VF5) and the frozen spec declared
the source-vantage axis a scope boundary. The Global Research Director's mandate is to vary that factor. This is
not a repeat of the answered window/timescale axis: pool, classifier, window ladder and rules are held frozen so
that ONLY the egress vantage changes.

The parent handoff four-way distinction is preserved in `spec.json#parent_handoff_disposition`. In short:
*established* — measurement-valid S1_STATIONARY on one egress, CLASS_PERSISTENCE 1.0, denylist valid to a
right-censored 1800 s, skill 0.3196 nats (p=9.999e-05, CI lower 0.142), all controls pass. *rejected* — all three
S0 change classes absent there; a pooled any-barrier denylist is not as valid (ANYBARRIER_FALSE_ACCEPT=0.125); any
reading above HYPOTHESIS or licensing a product denylist; the pre-freeze certificate text as durable evidence.
*unknown* — source-vantage generalization (this experiment), horizon past 1800 s, ONSET, pool generalization,
protocol self-induction, rate behaviour beyond single 429 events. *do_not_assume* — no promotion above HYPOTHESIS,
no generalization beyond pool/client/UA/egress/window, no horizon beyond censoring, no non-GET substrates, no
conflation with C-FRESHNESS or C-MEAS-VALID, no treating the parent failure observations as falsification.

## 2. Frozen inputs (immutable interpretation dependencies)

Pool: the 57 endpoints of `research/experiments/EXP-PHYSICS-38074818597/spec.json` (`frozen_universe.endpoints`,
sha256 `ef50435dc10dcaba4ae56a7e7f6eb7e63be2b8fd2216900367c56a59fd3b17dd`), byte-identical, in the frozen order.
Classifier: the frozen intrinsic classifier of `research/physics/exp_38074818597_lib.py`
(sha256 `c0ff938b0dd7883dcf67722eda215e2af74bdd458dc25ff663279c807d81557e`), including `CHALLENGE_RE_LITERAL`,
`barrier_set = {RATE_LIMIT_429, BLOCK_403_CHALLENGE, TRANSPORT_ERROR}` and
`intrinsic_classes = {BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`.
Parent raw replay fixture: `research/experiments/EXP-PHYSICS-38074818597/raw/ambient_collection.jsonl`
(228 rows, sha256 `a418f66f82cac16b66893f6081bd30d1c6fe9eb6a3bd9ff7f845a2a12f7af96f`).
EXECUTE must **import** the classifier from the bound module (or byte-replicate its constants) and pass replay with
0/228 mismatches (MV5).

## 3. Vantages

* **V1 — direct runner egress.** No proxy. Record public IP, ASN, country at session start/mid/end.
* **V2 — second independent egress, pinned Tor exit.** `apt-get install -y tor`; torrc with `SocksPort 0`,
  `HTTPTunnelPort 127.0.0.1:19051`, `ControlPort 127.0.0.1:19052`, `CookieAuthentication 1`,
  `MaxCircuitDirtiness 7200`, `NewCircuitPeriod 7200`. Pin exactly one exit relay via
  `SETCONF ExitNodes=<fingerprint> StrictNodes=1` (or an equivalent ip-literal pin) and verify pre/mid/post identity.
  Every V2 GET goes through the HTTPTunnelPort CONNECT proxy.

DESIGN pre-freeze probe (2026-10-11, non-outcome-bearing; no frozen endpoint was touched): tor 0.4.9.11 installed
(rc=0); bootstrapped 100% in 73 s; unpinned exits rotated; ip-literal pin returned `250 OK`, `SIGNAL NEWNYM`
returned `250 OK`, and the post-NEWNYM exit IP equalled the pinned target; V2 exit observed in NL
(192.42.116.14 / 192.42.116.95), `check.torproject.org` `IsTor=true`, distinct from V1 (AS8075, US); all 7 oracle
hosts classified correctly through the tunnel and on V1.

**Construct-validity caveat (frozen):** a public Tor exit is a genuinely independent egress but carries a
Tor-specific blocking policy. Therefore a POSITIVE is a *conservative* robustness result; a NEGATIVE bounds the
reading to "V2 differs from V1 under a Tor exit" and cannot by itself separate generic vantage-specificity from
Tor-specific blocking — a non-Tor egress re-test is required before attributing a negative to generic vantage.
This is an interpretation bound, not a measurement failure.

## 4. Protocol

Nominal rungs 0/300/900/1800 s from session t0 (first V2 GET of rung 0); `delta_ref` = actual offset of rung 1800,
required `>= 1500 s`. Within each rung, endpoints are visited in a deterministic shuffle seeded by
`(38121193195 + rung_index)`; for each endpoint one V2 GET (through the tunnel) then one V1 GET (direct), then the
next endpoint. HTTP: GET, 30 s timeout, redirects followed, TLS verified, **fresh CookieJar per call**, one frozen
User-Agent, **zero retries**, credential-free, no JS/browser. 456 GETs total. Raw per-call fields are recorded as
listed in `spec.json#sweep_protocol.raw_record_fields`.

Anchors: `V1_anchor`/`V2_anchor` = classes at rung 0; `V1_delta`/`V2_delta` = classes at rung 1800. An intrinsic
endpoint is one whose class is in `intrinsic_classes`.

## 5. Estimators

* Plugin binary MI in nats, `I(X;Y) = Σ p(x,y) ln(p(x,y)/(p(x)p(y)))`, on barrier indicators.
* `V2_STATIONARITY_SKILL_nats = I(B_V2_anchor; B_V2_delta)`; `CV_SKILL_nats = I(B_V1_anchor; B_V2_anchor)`.
* Permutation nulls, 10000 permutations, seed 38121193195: `B_EXCHANGE_V2` permutes `B_V2_delta` across endpoints;
  `B_CROSSVANTAGE` permutes `B_V2_anchor` across endpoints. `p = (1 + #{perm >= obs}) / (1 + 10000)`.
* Cluster bootstrap, 5000 resamples: endpoint clusters (57) **and** registrable-domain clusters (53, collapsing the
  archlinux.org / djangoproject.com / spring.io multi-endpoint domains). A significance clause requires BOTH 95%
  lower bounds `> 0`.
* Baselines: `B_CONSTANT_USABLE`, `B_MARGINAL_V2`, `B_LASTSWEEP_V2` computed from the same raw records.
* Agreement diagnostics: `CV_INTRINSIC_CLASS_AGREEMENT`, `CV_CLASS_AGREEMENT_ANY`, `CV_MI_CLASS_T0`.

## 6. Frozen decision rule

**Zero-denominator convention (frozen):** for any ratio `num/den`, if `den > 0` use `num/den`; if `den == 0` the
rate is defined as `0.0` and the companion boolean `<NAME>_ESTIMABLE` is set `false`. A clause evaluated with a
0.0-convention rate is satisfied by that 0.0.

Clauses:

1. `V2_INTRINSIC_PERSISTENT`: `V2_n_t0_intrinsic >= 3` **and** every intrinsic class present at the V2 anchor has
   `V2_CLASS_PERSISTENCE[class] >= 0.80`. If `V2_n_t0_intrinsic < 3` the clause is false and routes to
   `S0_VANTAGE_SPECIFIC` with change class `v2_intrinsic_absent_or_insufficient`, **not** to
   `MEASUREMENT_INVALID` (see the low-V2-intrinsic convention in §7).
2. `V2_DENYLIST_INTRINSIC_VALID`: `V2_DENYLIST_FALSE_ACCEPT <= 0.20` **and** `V2_DENYLIST_FALSE_REJECT <= 0.20`.
3. `V2_STAT_SIG`: `V2_STATIONARITY_SKILL_nats >= 0.05` **and** `V2_STATIONARITY_PERM_P < 0.05` **and** both CI lower
   bounds `> 0`.
4. `CV_AGREEMENT_SIG`: `CV_SKILL_nats >= 0.05` **and** `CV_STATIONARITY_PERM_P < 0.05` **and** both CI lower bounds
   `> 0`.
5. `CV_DENYLIST_TRANSFER_VALID`: `#(V1-anchor intrinsic) >= 1` **and** `CV_DENYLIST_FALSE_ACCEPT <= 0.20`
   **and** `CV_DENYLIST_FALSE_REJECT <= 0.20`.

Branch precedence:

1. `MEASUREMENT_INVALID` — if ANY of MV1–MV10 fails or any live oracle control fails. Never reported as FALSIFIES.
2. `S1_CROSS_VANTAGE_ROBUST` — MV1–MV10 (incl. MV3a, MV6a) hold AND all five clauses true. Reading: one shared
   intrinsic denylist is licensed modulo the frozen pool and the two tested vantages.
3. `S0_VANTAGE_SPECIFIC` — MV1–MV10 (incl. MV3a, MV6a) hold and clause 1..5 not all true. Change classes, with primary =
   first-listed applicable: `v2_intrinsic_absent_or_insufficient` (clause 1 false via `V2_n_t0_intrinsic < 3`),
   `v2_intrinsic_break` (clause 1 false via some class persistence `< 0.80`), `v2_intrinsic_denylist_violation`
   (clause 2 false), `v2_within_vantage_nonstationary` (clause 3 false), `cross_vantage_class_disagreement`
   (clause 4 false), `cross_vantage_transfer_violation` (clause 5 false).

## 7. Measurement-validity prerequisites (any failure → `MEASUREMENT_INVALID`)

MV1 V1/V2 distinct in public IP, ASN and country; MV2 V2 exit pinned and identical start/mid/end; MV3 57/57 anchor
and 57/57 delta on both vantages; MV3a the pool exercises the classifier — at least one anchor has ≥1 intrinsic
endpoint and at least one has ≥1 non-intrinsic endpoint (zero intrinsic at BOTH anchors ⇒ INVALID); MV4
`delta_ref_actual >= 1500 s`; MV5 classifier replay 0/228 on the bound parent raw file and 0 live
double-classification mismatches; MV6 live oracle controls pass at both vantages each rung; MV6a a V2
endpoint-level `TRANSPORT_ERROR` is accepted as an intrinsic class only when the same-rung V2 control-plane fetches
succeeded (a proxy-level failure to `127.0.0.1:19051` is a tunnel failure ⇒ INVALID, never an endpoint class);
MV7 **all** declared synthetic controls pass their frozen thresholds — `PC_CROSS_SYNTHETIC_STATIONARY >= 0.80`,
`PC_SYNTHETIC_STATIONARY >= 0.80`, `NC_SYNTHETIC_EXCHANGEABLE <= 0.05`, `NC_INDEPENDENT_STATIONARY <= 0.05`,
`NC_CROSS_SUPERSET == 0`; MV8 V1 ASN constant across rungs; MV9 tunnel reached bootstrap 100% and served every V2
GET; MV10 the 57 endpoint URLs are byte-identical to the bound pool.

**Low-V2-intrinsic convention (frozen).** The parent single-vantage packet mapped `n_t0_intrinsic < 3` to
`MEASUREMENT_INVALID` because that floor certified persistence could be estimated at all. Here the research object
changed to the *vantage* factor: a validly measured second egress that exhibits `< 3` intrinsic endpoints is
scientific evidence of cross-vantage class disagreement, so it routes to `S0_VANTAGE_SPECIFIC` with change class
`v2_intrinsic_absent_or_insufficient`, not to `MEASUREMENT_INVALID`. Only `MV3a` (zero intrinsic endpoints at BOTH
anchors) is an instrument-exercise failure. This deviation is deliberate, justified by the changed object, and
frozen before outcomes.

## 8. Controls and their DESIGN calibration

All synthetic controls use the parent anchor marginal (`CLEAN 45, OTHER_NONBARRIER 4, BLOCK_403_CHALLENGE 6,
TRANSPORT_ERROR 1, RATE_LIMIT_429 1`, n=57) as the frozen design prior.

* `PC_CROSS_SYNTHETIC_STATIONARY` (rho=0.98, perfect cross-vantage anchor agreement, seed 38121193195): frozen
  in-run R=400, perms=2000, boot=500; require T1 fraction `>= 0.80`. DESIGN pre-freeze calibration (R=300,
  perms=1000, boot=1000): **0.9333** (CV-significant 0.9767); rho=0.92 → 0.76.
* `PC_SYNTHETIC_STATIONARY` (rho=0.98): require S1 fraction `>= 0.80`. DESIGN calibration **0.9333**.
* `NC_SYNTHETIC_EXCHANGEABLE` (i.i.d. draws; seed 38121193196): require T1 fraction `<= 0.05`. DESIGN calibration
  **0.0**, CV-significant 0.01.
* `NC_INDEPENDENT_STATIONARY` (each vantage internally stationary, mutually independent; seed 38121193197): require
  T1 `<= 0.05`. DESIGN calibration **0.0**, CV-significant 0.0067.
* `NC_CROSS_SUPERSET` (V2 blocks strictly more than V1; seed 38121193198): require T1 `= 0`. DESIGN calibration
  **0.0** with CV-significant 0.7933 — evidence the transfer clause, not the agreement clause, is discriminating.
* `PC_ORACLE_BARRIER` (live, both vantages, every rung): httpbin/httpbingo 429 → RATE_LIMIT_429;
  no-such-host.invalid → TRANSPORT_ERROR; httpbin 403 → UNAVAILABLE_403.
* `NC_CLEAN_ORACLE` (live, both vantages, every rung): httpbin 200, httpbin uuid, example.com → CLEAN.
* `SUBSTRATE_PINNED`, `CLASSIFIER_REPLAY` as in MV2/MV5.

All controls above are gated by MV7 (any failure ⇒ `MEASUREMENT_INVALID`), including the falsification-direction
controls `NC_INDEPENDENT_STATIONARY` and `NC_CROSS_SUPERSET`, so none is decorative.

**Treatment identity (frozen).** The treatment is a *specific pinned exit relay*, not "Tor in general". EXECUTE
records the pinned exit-relay fingerprint in `result.json` / `provenance.json`; changing it mid-session is MV2
INVALID; switching to another exit after inspecting outcomes would be a new treatment instantiation and is not
licensed by this packet.

## 9. Consequences

* **Positive (`S1_CROSS_VANTAGE_ROBUST`)** — the program's only accepted Physics positive generalizes across two
  independent egress vantages on the frozen pool; one shared class-conditional intrinsic denylist is licensed;
  C-WEB-DYNAMICS may be considered for EXPERIMENTAL only through the normal DIRECTOR verdict path (DESIGN claims no
  promotion).
* **Negative (`S0_VANTAGE_SPECIFIC`)** — no vantage-blind shared denylist is licensed; barrier/scheduling policy
  must be per-egress, and (given the Tor confound) a non-Tor re-test is required before calling the result generic.
* **Invalid** — record the exact failing prerequisite and raw evidence; do not substitute a single-vantage run.

## 10. Scope boundaries and non-duplication

Two egress vantages only, frozen pool/window/classifier, no horizon claim past censoring, no non-GET substrates,
no product code. The endpoint access-decision object is kept distinct from C-FRESHNESS content drift and from
Runtime C-MEAS-VALID instrument-drift controls.
