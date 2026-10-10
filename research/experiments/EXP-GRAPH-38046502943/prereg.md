# EXP-GRAPH-38046502943 — Pre-registration (DESIGN packet)

**Status: DESIGN COMPLETE — freeze SUPPRESSED. NOT FROZEN.**
This document, together with `spec.json`, is the pre-freeze constructibility
certificate deliverable mandated by the Global Research Director. No EXECUTE
is authorized by this packet and none should be derived from it.

## 1. Identity

- Experiment: `EXP-GRAPH-38046502943`
- Lane: `graph`
- Claim: `C-FRESHNESS` (freshness sub-mechanism: session/token drift with
  false-accept measurement)
- Design contract version: 2
- Parent (bounded): `EXP-GRAPH-37992949248`
- Type: `DESIGN_ONLY_FAIL_LOUD_CERTIFICATE`

## 2. The question (as bound by the Director mandate)

> On credential-free, server-rendered, no-JavaScript GET-only anchors, is a
> value-only-rotation (D1V: STALE AND NOT structural_change AND NOT
> transport_change) population spanning >= 2 independent anchors constructible
> AT ALL such that the anchor-clustered 97.5% lower bound of the incumbent
> value-blind guard's false-accept differential (M-PAIRED-FA-DIFF-D1V) is
> non-degenerate and M-N-D1V-ANCHORS >= 2 — either (option A) by admitting a
> materially different anchor population whose transport validators (ETag,
> Last-Modified, Cache-Control max-age, Vary, final_url) are provably
> independent of the rotating value, or (option B) by a principled instrument
> change that reclassifies transport-validator motion caused solely by the
> rotating value itself, justified structurally rather than assumed?

The DESIGN must produce a pre-freeze constructibility certificate (exact
anchors, per-anchor transport-change cause, estimator power arithmetic). If no
such population is constructible, it must FAIL LOUDLY and return the decisive
positive-control-backed bounded reason that parks the four-anchor Part II
route, so freshness effort can move to a broader-population guard
false-accept/calibration measurement or another sub-mechanism — rather than
freeze another structurally degenerate single-anchor read.

## 3. Hypothesis and falsifier

- Hypothesis `H-CONSTRUCTIBLE`: a powered, non-degenerate >=2-anchor D1V frame
  is constructible on this substrate via option A and/or option B.
- Falsifier `F-NONDEGENERATE-CERT`: demonstration that every constructible D1V
  frame on the observed substrate realizes per-anchor false-accept identically
  (homogeneous blindness), forcing LOW == UB97 == 1.0 — i.e., the power of the
  estimator is not certifiable → FAIL LOUDLY.

## 4. Design: certificate-first satisfiability assessment (no outcome measurements)

The experiment is a DESIGN-time certificate. It used:

1. **Bounded live screen** of 8 candidate anchors (3 cookieless GET-only
   sessions each, pacing >= 3s, same-day, single egress). Recorded: status,
   final_url, body sha256, transport headers (ETag, Last-Modified,
   Cache-Control, Vary), in-list token names, per-session extracted values,
   and the frozen drift labels (structural/transport/postcond/endpoint change)
   computed with the parent packet's **exact trial-construction semantics**
   (per-field occurrence ordinal keying, per-pair structure comparison).
   **Drift labels only.** No guard decisions, no false-accept rates, no
   intervals were computed at any point — those are EXECUTE-read outcomes.
2. **Zero-network replay** of the frozen inherited evidence (CAL-POS-1..3 raw
   records + bodies) under the same parent-exact construction, as the
   classifier sensitivity control.
3. **Closed-form estimator power arithmetic** using the frozen guard logic and
   the frozen anchor-clustered bootstrap.

### Screen results (2026-10-10)

| Candidate | URL (registration path) | Result |
|---|---|---|
| P1-OSM-RAILS | openstreetmap.org/user/new | **D1V-capable**, 6/6 D1V trials (authenticity_token, csrf-token); transport byte-stable |
| P3-MW-ARCH | wiki.archlinux.org Special:CreateAccount | **D1V-capable**, 3/6 (wpCreateaccountToken; wpEditToken constant FRESH); transport byte-stable |
| P4-MW-GENTOO | wiki.gentoo.org Special:CreateAccount | **D1V-capable**, 3/6 (wpCreateaccountToken); transport byte-stable |
| P6-MASTODON | mastodon.social/auth/sign_up | **D1V-capable**, 6/6 D1V trials (authenticity_token, csrf-token); transport byte-stable |
| P2-DRUPAL | drupal.org/user/register | NO_FIELD (Keycloak SSO redirect) |
| P5-PHPBB | phpbb.com/community/app.php/user/register | UNREACHABLE (HTTP 403 x3) |
| P7-WORDPRESS | wordpress.org SSO login | NO_FIELD (login.wordpress.org redirect) |
| P8-XWIKI | xwiki.org Main | NO_FIELD (JS-bound flow) |

Transport signatures on all four value-bearing candidates: ETag=None,
Last-Modified=None, Cache-Control constant, Vary constant, final_url constant.
**Postcond (session field-name set) never fired on any candidate.**

Inherited control replay (parent-exact): CAL-POS-2 → 6 D1V trials (reproduces
parent M-N-D1V=6); CAL-POS-1 → BODY_DERIVED_ETAG, transport change 6/6 pairs,
structural change 4/6 pairs; CAL-POS-3 → TOKEN_BEARING_FINAL_URL, struct +
transport + endpoint change 6/6 pairs. All reproduce the parent trial matrix.

Option B re-verification on frozen evidence: CAL-POS-1 body diffs include
nonces/arkose/snowplow beyond the token → ETag motion not caused solely by the
rotating value; CAL-POS-3 final_url centralauthLoginToken is a different,
concurrently/mutually-orthogonally rotating value than body wpLoginToken
(byte-suffix drift) → not same-value leakage. **Option B closed for both.**

## 5. The power arithmetic (the certificate's core)

- On any D1V trial: B-VALUE-AWARE ABSTAINS (CH-PRECOND-BINDING fires since
  live != recorded) → value-aware FA = 0.
- B-INCUMBENT-SIGNAL-ONLY REUSEs on every D1V trial (D1V excludes structural,
  transport, and postcond firing) → per-anchor incumbent FA on D1V trials =
  1 − postcond_fire_fraction(a).
- Pooled differential = anchor-clustered weighted mean of per-anchor FA.
- LOW < UB97 (non-degenerate 97.5% interval) **iff** per-anchor FA is
  heterogeneous **iff** CH-POSTCOND-SEM fires on >= 1 D1V pair of some anchor.
- Observed: postcond fires 0 times on 0 D1V pairs across 5 D1V-capable anchors
  (CAL-POS-2 + P1/P3/P4/P6), 3 capture dates, 4 platform families
  (WMF, OSMF, Arch Linux, Gentoo, Mastodon).
- Therefore on ANY constructible frame (e.g., {P1,P3,P4,P6}, K=4 → 36 D1V
  trials, 4 anchors — satisfying M-N-D1V-ANCHORS>=2): per-anchor FA = 1.0
  everywhere → LOW == UB97 == 1.0 → **zero-width degenerate interval**,
  would-be mode `DATA-INSUFFICIENT-D1V-DEGENERATE` / `ANCHOR_SCARCITY_OTHER`.

### Branch reachability of the would-be frozen decision rule

- INCUMBENT-BLIND-CONFIRMED requires LOW>0 AND LOW<UB97 → **unreachable**.
- INCUMBENT-NOT-BLIND (F-BLIND) requires LOW<=0 or pooled<0.10 → pooled=1.0 →
  **unreachable**.
- Sole reachable outcome: DATA-INSUFFICIENT-D1V-DEGENERATE.

## 6. Controls

- **PC-CLASSIFIER-SENSITIVITY**: inherited-evidence replay reproduces parent
  drift facts exactly (see §4); the "no change" verdicts on candidates are true
  observations, not classifier blind spots.
- **PC-EXTRACTION-CANARY**: PA.extract recovers in-list values byte-identically
  on all live candidates and inherited bodies.
- **PC-ESTIMATOR-NONDEGENERATE** (inherited GATE-F PASS): on a synthetic
  heterogeneous 2-anchor fixture the bootstrap returns LOW=1/3, UB97=1/2 —
  the estimator machinery yields non-degenerate intervals whenever the
  population supports them. The forced degeneracy is a population property.
- **NC-NONDEGENERATE-ESTIMATOR, NC-OPEN-GET-ONLY, NC-CREDENTIAL-FREE**
  (inherited); **NC-NETWORK-CONTROL** (iana.org 200 before probe).

## 7. Pre-registered outcomes and consequences

- **Certificate PASS** (had postcond heterogeneity been observed): freeze and
  execute the powered read on the certified frame; blindness confirmation
  licensed. — *Not realized.*
- **Certificate FAIL (realized)**: FAIL LOUDLY per mandate. Freeze is refused
  (`decision_rule_reachability = FAIL`); the certificate is the terminal
  deliverable; C-FRESHNESS status unchanged (UNKNOWN); the four-anchor Part II
  route is **parked with a positive-control-backed bounded reason**:
  the blindness confirmation is unfalsifiable at the anchor level on this
  substrate (incumbent REUSEs on every D1V trial; field-set homogeneity
  collapses the differential's dynamic range to zero). Notably,
  ANCHOR_TRANSPORT_COUPLING is **repudiated as the general blocker** — the new
  population is transport-stable; the operative attribution is population-wide
  field-set homogeneity. A re-run would deterministically land in
  DATA-INSUFFICIENT-D1V-DEGENERATE again.
- **Pre-registered redirect recommendation** (not designed here): (a)
  broader-population guard false-accept/calibration measurement — the four new
  live anchors make a multi-anchor calibration study concretely feasible; (b)
  another freshness sub-mechanism (e.g., FRESH-trial false-outage/calibration).

## 8. Measurement validity

- V01-NEW: probe produced drift labels and transport facts only; NO guard
  decisions / false-accept measurements. Probe sessions are excluded from any
  future scored population unless re-harvested under a frozen EXECUTE with
  re-verified substrate certificate.
- V02: any future EXECUTE on these anchors must re-verify C-ANCHOR-802-200-LIVE /
  C-ANCHOR-MISC-105-REUSE-LOCK, C-SESSION-ISOLATION-REPAIRED (runtime re-check,
  not assumption).
- V03: frozen classifier and in-list TOKEN_NAME_LIST reused unchanged; verified
  live (canary).
- V04: same-day captures (3s+ pacing); cross-date inference rests solely on
  inherited CAL-POS-2 evidence merged with the probe date.
- V05: rotation is server-side per-request minting; the certificate does not
  depend on asserting why values rotate, only that they do and nothing else
  moves.

## 9. Key definitions carried forward (frozen)

- D1V = STALE AND NOT structural_change AND NOT transport_change.
- structural_change: structure_signature = (type_class, form_action,
  form_method, tuple(form_input_names)) differs per pair.
- transport_change: transport_signature = (ETag, Last-Modified, Cache-Control
  max-age, Vary) differs, OR final_url differs.
- postcond_change (CH-POSTCOND-SEM): session in-list field-name set differs.
- label STALE: live value != recorded value byte-exact.
- Trial construction: per-field occurrence ordinal keying across the session
  extraction order; pairs over recorded-vs-current sessions; per-pair channel
  comparisons; value/state filters — exactly as frozen in the parent packet.

## 10. What this packet does NOT claim

- No false-accept measurements, no guard decisions, no intervals (none were
  computed).
- No claim status change for C-FRESHNESS.
- No statement that postcond heterogeneity is impossible in general — only that
  it is unobserved on this substrate across 3 dates / 5 anchors; the
  certificate is falsifiable by a future observation of it.

## 11. Transmission notes

- Reading order for downstream agents: this prereg → `spec.json` (certificate
  + embedded evidence with body hashes) → parent packet only as needed.
- The probe raw evidence is session-local and NOT committed; all certificate
  facts are embedded in `spec.json` (headers, final_urls, body sha256
  prefixes, extracted value prefixes, parent-exact drift classifications).
- Next decision stages: lane DIRECTOR (redirect adjudication) and AUDIT
  (independent certificate review). The fail-loud terminal outcome is the
  deliverable; no EXECUTE handoff is produced.