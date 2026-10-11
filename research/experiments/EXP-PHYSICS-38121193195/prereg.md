# EXP-PHYSICS-38121193195 preregistration

Cross-vantage transfer of endpoint intrinsic ACCESS-BARRIER persistence and the anchor-built
intrinsic-denylist validity horizon. Lane: physics. Claim: C-WEB-DYNAMICS (ceiling HYPOTHESIS).
Design contract v2. Status: DESIGN COMPLETE, PENDING FREEZE.

## 1. Purpose and question

The accepted Physics positive (EXP-PHYSICS-38074818597, S1_STATIONARY, audit PASS) measured
endpoint intrinsic access-barrier persistence `{BLOCK_403_CHALLENGE, TRANSPORT_ERROR}` and an
anchor-built intrinsic-denylist validity horizon right-censored at 1800 s on ONE egress and ONE
~2041 s session, and declared the source-vantage axis a scope boundary (audit finding VF5, echoed
in request.json.inherited_last_verdict). The Director REOPENs C-WEB-DYNAMICS with the question:
does that result transfer across independent source vantages, or is it an artifact of the single
network vantage and window?

This experiment answers it with a PAIRED two-vantage session on the SAME frozen 57-endpoint pool,
SAME frozen intrinsic classifier and SAME nominal window ladder (0/300/900/1800 s):

- V1 = the runner's direct datacenter egress (reference; AS8075 Microsoft, Canada, recorded per rung);
- V2 = a SECOND independent egress — a single PINNED Tor exit, distinct public IP / ASN / geography,
  held constant across all rungs (control-port `SETCONF ExitNodes=<ip> StrictNodes=1` + `NEWNYM`,
  verified per rung).

Per rung, each endpoint is fetched V2-then-V1 through one stdlib client realized as two openers
(direct; and `urllib.request.ProxyHandler` through the Tor `HTTPTunnelPort` CONNECT proxy, a
byte-transparent TLS tunnel so origin responses are preserved).

The three mandate questions map to frozen quantities:
- Q1 -> `V2_INTRINSIC_PERSISTENT` (per-class `V2_CLASS_PERSISTENCE[c] >= 0.80` at delta_ref for each
  intrinsic class present at the V2 anchor; `n_t0_intrinsic_V2 >= 3`);
- Q2 -> `V2_DENYLIST_INTRINSIC_VALID` (`V2_DENYLIST_FALSE_ACCEPT <= 0.20`, `V2_DENYLIST_FALSE_REJECT
  <= 0.20`) AND `V2_STAT_SIG` (`V2_STATIONARITY_SKILL >= 0.05` nats, `B_EXCHANGE_V2` permutation
  p < 0.05, endpoint-clustered CI lower > 0);
- Q3 -> `CV_AGREEMENT_SIG` (`CV_SKILL = I(B_V1_T0; B_V2_T0) >= 0.05` nats, `B_CROSSVANTAGE`
  permutation p < 0.05, endpoint-clustered CI lower > 0) AND `CV_DENYLIST_TRANSFER_VALID`
  (`CV_DENYLIST_FALSE_ACCEPT <= 0.20`, `CV_DENYLIST_FALSE_REJECT <= 0.20`, denylist built on the
  V1 anchor intrinsic set, tested at V2 delta_ref).

Branch: `T1_VANTAGE_ROBUST` iff all five decision quantities hold; `T0_VANTAGE_SPECIFIC` otherwise
with change classes enumerated among {v2_intrinsic_break, v2_denylist_violation,
v2_no_anchor_information, no_cross_vantage_information, cross_vantage_transfer_violation};
`MEASUREMENT_INVALID` exclusively for prerequisite/control/substrate failure (incl. any egress-gate
violation or tor-provision failure — recorded as the exact blocker receipt the mandate allows).

## 2. Frozen protocol (literal; see spec.json for the verbatim constants)

- Universe: the frozen 57 credential-free HTTP GET endpoints of EXP-PHYSICS-37992957068, inherited
  verbatim (spec.json:frozen_universe). No substitution, addition, or dropping.
- Classifier: frozen intrinsic classifier (spec.json:frozen_intrinsic_classifier), including
  CHALLENGE_RE_LITERAL
  `(?i)(just a moment|cf-browser-verification|cf[-_]chl[-_]|challenge-platform|cf-challenge|cdn-cgi/challenge|attention required|checking your browser|enable javascript and cookies|verify you are human|please complete the security check|g-recaptcha|hcaptcha|recaptcha|cf-turnstile|<title>\s*just a moment)`
  matched on the first 262144 decoded bytes of the body; classes CLEAN/RATE_LIMIT_429/
  BLOCK_403_CHALLENGE/UNAVAILABLE_403/TRANSPORT_ERROR/OTHER_NONBARRIER; barrier_set and
  intrinsic_classes as in the parent. Classification is a pure function of one request's stored
  fields (status, cf-mitigated, body prefix).
- Client: Python 3.12 stdlib ONLY (numpy not required/imported); User-Agent
  `SPIDER-research2/1.0 (+credential-free access-state persistence probe)`; Accept `*/*`; GET only;
  redirects <= 5; timeout 30 s; retries 0; TLS verify on. One implementation, two openers:
  V1 = direct default route; V2 = `ProxyHandler({'http','https'}: http://127.0.0.1:19051)`.
- V2 substrate (EXECUTE-provisioned): `sudo apt-get install -y tor` if missing; dedicated instance
  with `SocksPort 0`, `HTTPTunnelPort 127.0.0.1:19051`, `ControlPort 127.0.0.1:19054`,
  `CookieAuthentication 1`, `MaxCircuitDirtiness 7200`, `NewCircuitPeriod 7200`; wait for
  `Bootstrapped 100%` (observed ~7 s). Pre-flight pinning: discover exit IP via
  `https://api.ipify.org` through the tunnel; `SETCONF ExitNodes=<ip> StrictNodes=1`; `SIGNAL
  NEWNYM`; re-fetch ipify and require the same IP; up to 3 attempts, else MEASUREMENT_INVALID with
  the exact error series. Pin the exact IP literal, NEVER a /24 (the /24 was observed to rotate
  within the subnet; ip-literal pinning held 5/5 consecutive checks; unpinned exits rotated within
  ~2 min — all pre-freeze observations).
- Session start S = completion of pre-flight (pin verified, oracle battery passed on both vantages,
  anchor egress identity recorded). Rungs at nominal offsets 0/300/900/1800 s from S. Within a rung,
  endpoints in the frozen seeded order (seed 38121193195); per endpoint: V2 fetch first, then V1
  fetch; inter-endpoint gap 0.30 s; fresh cookie jar per (endpoint, vantage) request.
- Per-rung pre-checks (any failure => MEASUREMENT_INVALID): (i) V2 exit IP via ipify through the
  tunnel must equal the pinned IP; (ii) V2 route health `https://httpbin.org/status/200` through
  the tunnel must classify CLEAN; (iii) V1 ipify direct; (iv) V1 ASN via `http://ip-api.com/json`
  must equal the anchor ASN.
- Anchor egress identity: V2: ipify, `https://ifconfig.co/json` (IP/ASN/asn_org/country/hostname),
  `https://ipwho.is/` (redundant), `https://check.torproject.org/api/ip` (IsTor must be true); V1:
  ip-api.com/json and ipify. Gates: V2 IP != V1 IP AND V2 ASN != V1 ASN AND V2 country != V1
  country. (ipinfo.io and ip-api.com through the tunnel are documented Tor-blocks and are never
  used for V2 identity.)
- Oracles (pre-flight, both vantages): PC_ORACLE_BARRIER: httpbin.org/status/429 -> RATE_LIMIT_429,
  httpbingo.org/status/429 -> RATE_LIMIT_429, no-such-host.invalid -> TRANSPORT_ERROR (through the
  tunnel the recorded error class observed pre-freeze is `Tunnel connection failed: 503 Service
  Unavailable (resolve failed)`, still status None -> TRANSPORT_ERROR), httpbin.org/status/403 ->
  UNAVAILABLE_403; NC_CLEAN_ORACLE: httpbin.org/status/200, httpbin.org/uuid, example.com -> CLEAN;
  2 requests each. Any misclassification on any vantage => MEASUREMENT_INVALID.
- Analysis: all decision quantities, secondary metrics and gates exactly as spec.json:decision_rule
  and spec.json:stable_identifiers. Classification replay must be 0 mismatches.
- No induced-transience probe (parent Q3 answered); stratum_stress endpoints stay in the primary
  population and the 52 non-stress endpoints form the NO_STRESS robustness replicas and the
  per-vantage self-induction trend controls.
- Wall-clock cap 75 min; budget ~520 requests.

## 3. Decision rule (frozen thresholds; verbatim in spec.json)

T1_VANTAGE_ROBUST iff (all thresholds frozen): V2_INTRINSIC_PERSISTENT (per-class >= 0.80, n>=3)
AND V2_DENYLIST_INTRINSIC_VALID (FA <= 0.20, FR <= 0.20) AND V2_STAT_SIG (skill >= 0.05 nats,
B_EXCHANGE_V2 p < 0.05, clustered CI lower > 0) AND CV_AGREEMENT_SIG (CV_SKILL >= 0.05 nats,
B_CROSSVANTAGE p < 0.05, clustered CI lower > 0) AND CV_DENYLIST_TRANSFER_VALID (FA <= 0.20, FR <=
0.20). Otherwise T0_VANTAGE_SPECIFIC with enumerated change classes. MEASUREMENT_INVALID only for
prerequisite/control/substrate/egress failure. Claim ceiling: C-WEB-DYNAMICS stays HYPOTHESIS in
every branch; no PRODUCT_CORE; no EXPERIMENTAL upgrade from one egress-pair/window ladder.

## 4. Null calibration and branch reachability (pre-freeze, offline)

Script `/tmp/opencode/phys381/calibrate_cv.py` sha256 7b35e2e0e0e78fb638269127b0053a5bfe06a52abadaec64472982e194ae14db,
output `/tmp/opencode/phys381/calibrate_cv_out.json` sha256
fbaabfeac1f4e9c612f9b4e34b9190ad63e75d01f2f2fa000b627370bce5a6bc (DESIGN-local, /tmp, NOT
interpretation dependencies; EXECUTE re-derives all gates from its own code/data). The EXACT frozen
branch rule — including both permutation tests and both endpoint-clustered bootstrap CI clauses —
was applied on synthetic worlds built from the parent pilot marginal (46 CLEAN / 5
BLOCK_403_CHALLENGE / 1 TRANSPORT_ERROR / 5 OTHER_NONBARRIER), n=57, R=300:

- PC planted robust-transfer, rho=0.98 (V2 anchor = V1 anchor exactly; V2 delta = V1 anchor with
  prob rho): T1 in 245/300 = 0.8167 (>= 0.80 gate PASS); CV permutation-significant 300/300;
  mean CV_SKILL 0.3312 nats.
- PC rho=0.92: T1 in 219/300 = 0.73 (reported, not a gate).
- NC exchangeable (V1/V2/V2-delta independent draws): T1 in 0/300; CV permutation-significant
  fraction 0.04 (<= 0.05 gate PASS); mean CV_SKILL 0.0106 nats; T1-fraction-given-floors 0.0.
- NEG vantage-superset (V2 blocks >= 11 of the 50 V1-clean endpoints -> CV_FR ~ 0.30 > 0.20):
  T1 in 0/300; CV agreement itself significant in 0.92 of reps — proving the TRANSFER clause adds
  real discrimination beyond the agreement MI clause; T0 change class
  `cross_vantage_transfer_violation`.
- NEG independent-but-stationary (each vantage internally stationary at rho=0.98, vantages
  uncorrelated): T1 in 0/300; CV permutation-significant fraction 0.023; T0 change class
  `no_cross_vantage_information`.

Reachability statements: T1 and all five T0 change classes are each producible via the exact rule.
Threshold arithmetic is attainable: with n_t0_intrinsic_V2 >= 3 and persistence, V2_STATIONARITY_SKILL
>= H(3/57) ~ 0.206 > 0.05; CV_SKILL <= H(f_b) ~ 0.41 with f_b ~ 0.14, well above the 0.05 threshold
under agreement and below it under exchangeability (mean 0.0106); FA tolerance 1/7, FR tolerance
10/50. No empty or unreachable branch exists.

EXECUTE re-runs PC_CROSS_SYNTHETIC_STATIONARY (seed 38121193195, R=300, perms 500, boot 500; gate
T1-fraction >= 0.80 at rho=0.98) and NC_CROSS_SYNTHETIC_EXCHANGEABLE (seed 38121193196, R=300, perms
10000; gate CV permutation-significant fraction <= 0.05) as frozen controls.

## 5. Attainability certificate (pre-freeze probes; /tmp artifacts, hashes in
spec.json.measurement_validity.activity_disclosure)

All probes touched NEUTRAL/ORACLE hosts ONLY. The frozen 57-endpoint pool was NEVER probed from V2
in DESIGN: its V2-side classes ARE the scientific outcome (Q1/Q3), so a DESIGN census would be an
outcome-bearing measurement and is prohibited.

1. Direct egress (V1 analog): 20.220.118.2, AS8075 Microsoft, Quebec, Canada; ipify/ip-api/
   check.torproject all reachable; stable across repeated calls.
2. tor provision: `sudo apt-get install -y tor` -> tor 0.4.9.11 installed on this runner; dedicated
   instance (torrc in /tmp/opencode/torprobe/torrc_tunnel, sha256 629a64c47110296efa7f1312bdd880cb397e5c11f6d48f6b2491cebfd2d56edc)
   bootstrapped 100% in ~7 s.
3. Tunnel + classifier identity: the stdlib urllib client with ProxyHandler through the CONNECT
   tunnel classified the full oracle battery IDENTICALLY to the direct opener: httpbin/200, uuid,
   example.com -> CLEAN; httpbin/429, httpbingo/429 -> RATE_LIMIT_429; httpbin/403 ->
   UNAVAILABLE_403; no-such-host.invalid -> TRANSPORT_ERROR both ways (tunnel error string
   recorded). CONNECT tunnels are byte-transparent for TLS, so response status/headers/body reach
   the frozen classifier untouched; this is the mechanism, plus the identical control
   classifications, on which egress-invariance of the classifier path rests (probe_tunnel.py sha256
   ba96913d25c7343a28f39bd3eb6e2e020fb669289cab3c55f11cf9df56b6e3bc; output
   /tmp/opencode/phys381/probe_tunnel_out.jsonl sha256
   ae7586a75338a7b5c1ac689659d0766555195feae2d56f33aef9deaa1d89e90a).
4. Constant second egress: unpinned Tor exit rotation observed within ~2-3 min (23.129.64.164 ->
   192.42.116.21 -> 192.42.116.103) despite MaxCircuitDirtiness 7200 — unpinned is NOT a stable
   second vantage. Control-port pinning `SETCONF ExitNodes=<ip> StrictNodes=1` + `NEWNYM` held the
   exit at exactly 204.8.96.85 across 5/5 consecutive checks; /24 pinning rotated within the subnet
   (204.8.96.85 -> 204.8.96.163, tor74.quintex.com) — so the IP literal is pinned, and the per-rung
   constancy gate enforces it (pin_test.py sha256 59f62f4c1e89b0b6c67a1874fba3e03653b75a94721d47a71dbfd11c2c38558b;
   output /tmp/opencode/phys381/pin_test_out.jsonl sha256 94db550abb39f768fa22dd192ad3cf4be7ae7e87ba114d8e7d036ba1788fc702).
5. Egress identity services through the tunnel: api.ipify.org (IP), ifconfig.co/json (204.8.96.163,
   AS62744 QUINTEX, US, tor74.quintex.com), ipwho.is (ASN/geo), cloudflare cdn-cgi/trace (ip, loc),
   check.torproject.org/api/ip ({"IsTor":true,"IP":...})  — all reachable and classified CLEAN.
   ipinfo.io returns 403 through the tunnel (Tor-blocked) and ip-api.com returns
   RemoteDisconnected — both excluded from the V2 identity pipeline.
6. V2 anchor floors n_t0_intrinsic_V2 >= 3 and n_t0_barrier_V2 >= 3 are NOT measurable in DESIGN
   (probing the pool from V2 is the outcome). They rest on the disclosed general prior that web
   application firewalls challenge anonymized exits broadly on this pool (the pool is 6-7
   Cloudflare-challenged endpoints from the parent's V1), and are verified at the EXECUTE anchor.
   A shortfall is recorded as the exact blocker receipt (MEASUREMENT_INVALID, per the mandate), NOT
   as a scientific negative, and NO single-vantage substitution is permitted.

Certificate conclusion: the second independent egress IS provisionable, holdable constant, and
classifier-transparent on controls; the experiment proceeds.

## 6. Controls and gates (restated for EXECUTE)

- PC_CROSS_SYNTHETIC_STATIONARY gate: T1-fraction >= 0.80 at rho=0.98 (fresh cal 0.8167).
- NC_CROSS_SYNTHETIC_EXCHANGEABLE gate: CV permutation-significant fraction <= 0.05 (fresh cal 0.04).
- PC_ORACLE_BARRIER / NC_CLEAN_ORACLE: every request classified to its expected class on BOTH
  vantages; else MEASUREMENT_INVALID.
- C_VANTAGE_EVIDENCE gates (per rung): EGRESS_V2_CONSTANT (pinned ipify equal), EGRESS_DISTINCT
  (anchor IP/ASN/country distinct from V1), EGRESS_V1_ASN_CONSTANT, V2 route-health CLEAN; any
  failure => MEASUREMENT_INVALID with the exact egress series.
- C_PROBE_SELF_INDUCTION: per-vantage barrier-prevalence trends on the 52 non-stress endpoints,
  reported with clustered CI; no gate.
- CLASSIFIER_REPLAY_MISMATCHES must be 0.
- PARENT_DENYLIST_VERIFIED_AGAINST_RAW: recomputing the bound parent raw ambient_collection.jsonl's
  T0 sweep through the frozen classifier must reproduce the frozen 7-endpoint parent intrinsic set
  (spec.json:strata.stratum_intrinsic_candidates); mismatch => MEASUREMENT_INVALID.

## 7. Assumptions, validity threats and construct boundaries

1. Egress-invariance of the classifier path holds through a CONNECT tunnel (mechanism: byte-
   transparent TLS relay; verified on all 7 oracle hosts). This is the only substrate assumption on
   measurement identity.
2. The V2 anchor-floor prior (n_t0_intrinsic_V2 >= 3, n_t0_barrier_V2 >= 3) is a GENERAL PRIOR
   (WAFs challenge anonymized exits), not an observation; it is verified at the EXECUTE anchor and a
   shortfall is the mandate's blocker receipt.
3. Tor exit stability beyond the pinning verification: relays can fail mid-session. A failed stream
   classifies TRANSPORT_ERROR (frozen semantics) and per-rung egress checks detect rotation; total
   route loss is caught by the per-rung health oracle. Residual ambiguity between genuine mass
   blind-blocking and route failure is disclosed via elapsed-time distributions and error strings.
4. The egress pair is datacenter <-> Tor (purpose-built anonymity exit). A T0 driven by broad V2
   over-blocking is bounded to the Tor-egress type and does NOT rule out transfer across two
   residential/datacenter egresses. A T1 licenses shared-denylist use across the tested pair only;
   product adoption requires at least one non-Tor replication.
5. Paired V2-then-V1 probing touches the same endpoint from two egresses seconds apart. The
   within-vantage same-endpoint spacing stays >= 300 s (parent semantics), but the cross-vantage
   spacing is new; any origin-side joint state (e.g., a path-wide challenge deployment) affects both
   vantages symmetrically and would load in favor of agreement (T1); asymmetric per-IP treatment
   loads toward T0. Both directions are measured honestly; the pairing order is fixed and frozen.
6. The V1 arm replicates, not re-derives, the parent's supported result: same-session V1 metrics are
   reported (V1_REPLICATION_PARENT_DENYLIST_OVERLAP) but are diagnostic; the reference for transfer
   is the same-session V1 anchor.
7. PARENT_DENYLIST_TRANSFER (secondary) conflates session-time with vantage; it is reported with
   that caveat and never gates.
8. The denylist horizon is right-censored at delta_ref = 1800 s nominal (actual >= 1500 s);
   no claim about longer horizons.
9. Per-rung time skew between vantages: per-endpoint inter-vantage skew is seconds (V2-then-V1
   pairing); with-in-rung start alignment at nominal offsets; actual deltas recorded per vantage.
10. Synthetic controls validate the estimator on the pilot marginal; they do not assert real-world
    stationarity. Power is reported at the observed V2 counts, not gated.
11. ipinfo.io and ip-api.com are Tor-blocked (observed); V2 identity relies on ipify/ifconfig.co/
    ipwho.is/cf-trace/check.torproject — if ALL ASN sources fail at EXECUTE anchor, the distinctness
    certificate is incomplete and the run is MEASUREMENT_INVALID.
12. A single hidden confounder cannot be removed: any global (both-vantage) reconfiguration of a
    challenge provider during the 40-min window would change both arms' classes together; the
    within-session ladder and the parent comparison bound, but do not eliminate, this.

## 8. Legacy comparison (pre-2.0 Codex evidence)

- P2-WP003 (MEASUREMENT_INVALID; prev_action target leakage): NOT replicated — the frozen classifier
  uses a single request's stored fields only; no history features; no prev-action conditioning;
  label_determinism is explicit in spec.
- P2-WP003B (HISTORICAL_BOUNDED; different observables warrant new experiments): respected — the
  observables here (endpoint intrinsic class sequences over a window ladder from two egresses) are a
  new, distinct observable set; no state-feature tests are rerun.
- P2-WP002B (HISTORICAL_BOUNDED; 901 transitions; no website holdout; guard: do not claim cross-site
  transfer of next-state prediction): the guard is honored and operationalized — the mandate's Q3
  'shared denylist' is NOT assumed but MEASURED with an endpoint-clustered bootstrap CI and a global
  permutation null (B_CROSSVANTAGE), and the claim ceiling keeps C-WEB-DYNAMICS at HYPOTHESIS.
- Parent R2 accepted packet (S1_STATIONARY): replicated as the V1 arm's metric family and the
  within-V2 replication; extended by the second egress factor. Distinct_extension relative to legacy:
  the legacy corpus has zero barrier/denylist/vantage work (per request.json comparative_reasoning).
- This design does NOT repeat the single-vantage 1800 s ladder (explicitly forbidden), does NOT
  rerun next-request classification/value derivation/C-FRESHNESS/Runtime drift, and does NOT run the
  parent's induced-transience probe.

## 9. Inherited handoff disposition

From the parent packet (USE, per director_mandate.allocation.parent_handoff_disposition):
established = S1_STATIONARY (per-class CLASS_PERSISTENCE 1.0 both intrinsic classes; denylist
FA/FR 0.0 right-censored at 1800 s; STATIONARITY_SKILL 0.3196 nats, p 9.999e-05, CI95 [0.1424,
0.4954]; NC FP 0.0267; PC power 0.8233; CLASS_CONDITIONAL_TRANSIENCE true, recovery half-life 2 s;
oracles pass; audit PASS VF1/VF4/VF5; C-WEB-DYNAMICS retained HYPOTHESIS). rejected = value
prediction; history-feature skill; request-economy predictiveness; any promotion. unknown = the
source-vantage axis (VF5); horizon beyond 1800 s; ONSET outside the burst. do_not_assume =
single-vantage generalization; denylist validity beyond 1800 s; measurement failure as falsification;
C-FRESHNESS/Runtime conflation; single-vantage ladder repeats. The experiment targets the unknown
(VF5) exclusively.

## 10. Satisfiability self-attack (design-contract v2 analysis)

- Empty/unreachable branches: none — T1 and each T0 change class are produced by the exact rule in
  calibration (section 4); MEASUREMENT_INVALID paths are each concretely instantiable (pin failure,
  oracle failure, egress rotation, route loss).
- Arithmetic impossibility: none — thresholds sit inside attainable ranges (section 4).
- Ceiling/floor baselines: B_CONSTANT_USABLE and the exchangeable nulls sit at logloss/MI values far
  from the decision threshold; PC mean 0.33 nats vs NC mean 0.011 nats on the same statistic.
- Treatment/comparator identity: V1 vs V2 are proven distinct (IP/ASN/geo gates) and V2 is proven
  constant (pin + per-rung gate); the two openers differ ONLY in routing.
- Insensitive controls: PC/NC sensitivities demonstrated (0.82 power vs 0.04 FP on the exact rule);
  oracles discriminate all six classes on both egresses; C_VANTAGE_EVIDENCE has observed failing
  modes (unpinned rotation, /24 rotation).
- Missing prerequisites: tor provision, bootstrap, pinning, identity services, oracle reachability
  through the tunnel, V1 direct route — all probed PASS pre-freeze (section 5).
- Unbound mutable artifacts: the one mutable interpretation dependency (parent raw file for the
  PARENT_DENYLIST secondary) is bound in freeze_artifacts; every other constant is literal in
  spec/prereg and hashed by the deterministic freezer; EXECUTE code is authored as a literal
  realization and hash-pinned in provenance.json.

## 11. EXECUTE requirements (successor instructions)

- Author `research/physics/exp_38121193195_lib.py` and `_run.py` (and `_finalize.py`) as literal
  realizations of spec.json constants; stdlib-only; record their sha256 in provenance.json.
- Raw evidence files (frozen names): raw/ambient_collection_v1.jsonl, raw/ambient_collection_v2.jsonl,
  raw/oracles.jsonl, raw/egress_series.jsonl, raw/collection_meta.json.
- Re-verify ALL floors, controls, gates and the classifier replay from own data before branching;
  any shortfall => MEASUREMENT_INVALID with the exact error series (blocker receipt), never T0.
- Do not probe the frozen pool beyond the protocol; do not substitute endpoints; do not drop
  post-outcome; do not run the induced-transience probe; do not modify any frozen file.
- Report all stable_identifiers metrics; preserve branch ids T1_VANTAGE_ROBUST / T0_VANTAGE_SPECIFIC
  and the B_EXCHANGE_V2/B_CROSSVANTAGE null ids.

## 12. Successor notes

T1 => propose POLICY_SHARED_DENYLIST for the tested egress pair and request at least one non-Tor
independent-egress replication before product adoption. T0 => propose POLICY_PER_EGRESS_DENYLIST and
bound the shared-denylist prior to per-egress scheduling on this pool; C-WEB-DYNAMICS stays
HYPOTHESIS. MEASUREMENT_INVALID => the blocker receipt is itself the bounded mandate outcome; PARK
the thread on the named dependency. Nothing here authorizes promotion of C-WEB-DYNAMICS.