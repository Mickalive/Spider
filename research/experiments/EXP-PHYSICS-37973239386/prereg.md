# EXP-PHYSICS-37973239386 — preregistration (DESIGN, frozen)

Lane: `physics`. Claim: `C-WEB-DYNAMICS` (HYPOTHESIS). Binding direction: the exact
`director_mandate` in `request.json` (allocation.action `CONTINUE`, `cognitive_reset` true,
`parent_handoff_disposition` `SUPERSEDE`). Parent `EXP-PHYSICS-37385620138` is continuity
evidence only and is NOT the agenda.

This preregistration is one of the only two files DESIGN may emit
(`research/EXPERIMENT_PACKET.md` §2). Every pre-freeze pilot, power and control value is
written **literally here and in `spec.json`**, never referenced as a separately hashed
artifact, because `scripts/freeze_experiment.py` hashes exactly `request.json`, `spec.json`
and `prereg.md` (verified at source; the parent packet's handoff §`freeze-control-plane`
documents this for all 67 manifests). If a value must be frozen, it lives in these two files.

---

## 1. What is measured (observable object)

Unit of analysis: an **admitted action-gating field**

```
field = (registrable_site, document_url, locator_type in {cookie, input.hidden, meta}, locator_name)
```

Observable per observation: the raw minted value, the ordered `(session_index,
request_index)`, the wall-clock epoch, the HTTP status, and the same-session cookie
`name -> value` pairs. This is a **value-sequence predictability** observable, deliberately
different from the retired response-signature density/divergence estimators whose
rank/magnitude Codex found non-identifiable from an HTTP signature (parent packet,
`established`: `IDENTIFIABILITY LIMIT`).

Action-gating taxonomy (frozen; `spec.json`.`observable_object`):

- `SESSION` — cookie names matching `session|sessid|sid|jsessionid|phpsessid|asp.net_sessionid|connect.sid|_forum_session|authsession|auth_session|laravel_session|ci_session|codeigniter|symfony|rack.session|gitea|i_like_gitea|play_session` (case-insensitive).
- `CSRF` — cookie/input/meta names matching `csrf|xsrf|_token|authenticity|csrftoken|csrfmiddlewaretoken|__RequestVerificationToken`.
- `TOKEN` — names matching `token` (e.g. `wpLoginToken`, `wpCreateaccountToken`).
- `NONCE` — meta names matching `nonce` (e.g. CSP nonce). Reported as a **separate stratum** and
  excluded from the primary metric by default.

Excluded by a frozen name pattern (`spec.json`.`observable_object`.`excluded_name_pattern`):
analytics, consent, advertising, experiment and bot-management identifiers (`_ga`, `_fbp`,
`__cf_bm`, `ajs_anonymous_id`, `atlCohort`, `_abck`, `bm_sz`, `cid`, `euid`, `WMF-Uniq`,
`GU_mvt_id`, `kndctr_*`, `cfz_*`, ...). Rationale: the mandate's object is *server-side
action-gating* state, not client tracking identifiers. The census confirmed the distinction is
load-bearing (most cross-session-varying cookies are trackers, not action gates).

Non-GET requests and credentials are prohibited. JavaScript is not executed.

---

## 2. Frozen candidate universe

The **57 credential-free endpoints** listed verbatim in `spec.json`.`candidate_universe`
span Rails/GitLab (gitlab.gnome.org, invent.kde.org, gitlab.archlinux.org, ...), Gitea,
Discourse, MediaWiki (Wikipedia, MediaWiki, Wikidata, Arch, Gentoo, OpenStreetMap),
Django, PyPI, Reddit, dev.to, Flarum, forum and login/search stacks. The list is frozen;
EXECUTE may not substitute, add or delete endpoints (measurement-invalid condition (g)).

## 3. Collection protocol (frozen)

Per endpoint: `K = 8` **independent fresh sessions**, each with a **disjoint in-memory cookie
jar** and no shared state; each session issues `J = 3` GETs of the **same** document URL.
Fixed User-Agent, 20 s timeout, body read cap 600 000 bytes. Fresh sessions are the mandate's
"independent fresh sessions with disjoint cookie jars". Request count is bounded by
`57 x 8 x 3 = 1368` GETs. No conditional/cache requests are issued.

Master seed: `master_seed = int(request_hash[:8], 16) = int("92124686", 16) = 2450671238`
(`request_hash 92124686699fdafc6d8a6e7c620506602a301d390e95edfb9d109238ae5fee12`). Session
scheduling and field ordering use `master_seed`-derived offsets; the rule family is not fitted
to real fields, so there is no outcome-dependent selection to randomise.

## 4. Admission criterion (frozen)

A field is **admitted** iff all hold:

1. locator/name is in the action-gating taxonomy and not in the excluded pattern;
2. `>= 2` distinct raw values across the fresh collection (**cross-session variation** — the mandate's "vary across independent fresh sessions");
3. present in `>= 2` distinct sessions;
4. `>= N_MIN_OBS = 4` total observations.

Fields present but constant across sessions are **not** admitted (they would be trivially
memory-repeat-predictable and are outside the mandate's "vary across fresh sessions" object).
The `NONCE` stratum is admitted but excluded from the primary metric; an `ALL_PLUS_NONCE`
sensitivity is reported separately.

## 5. Frozen rule family (algorithm; do not retune after outcomes)

Eleven **armed** non-baseline rules plus three **baseline** predictors. All predicates are
fixed functions of the field's own values and same-session cookie values only. Full predicates
are in `spec.json`.`frozen_rule_family`; summary:

Armed (count as predictable if they fire):

- `R_INT_INCR`, `R_HEX_INCR`, `R_B62_INCR` — all values parse as decimal / base-16 / base-62 integers and consecutive deltas are a single nonzero constant.
- `R_PREFIX_COUNTER` — constant prefix `P` and suffix `S` (shell length `>= max(4, 0.25*min_len)`) with a varying integer middle of constant nonzero delta.
- `R_ORDER_LINEAR` — integer values fit `v_i = a + b*i` (`b != 0`) on the first half and reproduce the held-out second half exactly.
- `R_SESSION_BIND` — `>= 0.75` of values equal / start with / end with / contain (`len >= 8`) a same-session cookie value.
- `R_HASH_BIND` — `>= 0.75` of values equal the md5 / sha1 / sha256 hex digest of a same-session cookie value.
- `R_WALLCLOCK_DEC` / `R_WALLCLOCK_HEX` / `R_WALLCLOCK_B64` — a decimal substring (`>= 10`), hex substring (`>= 8`), or 4-byte base64 window decodes to epoch within `+/- 3600 s` of the observation wall-clock, at second or millisecond scale.
- `R_CONST_SUBSTRING` — the longest common substring over all values has length `>= max(6, 0.40*min_len)` while values are not all identical.

Baselines (never counted as predictable): `R_MEMORY_REPEAT` (identity), `R_MARKOV1`
(first-order successor table, held-out on last 30%, mode fallback), `R_CONSTANT_MODE`
(training mode).

**Class attribution priority** (single label per firing field, for the class breakdown only):
`SESSION_BIND > HASH_BIND > WALLCLOCK_B64 > WALLCLOCK_HEX > WALLCLOCK_DEC > INT_INCR >
PREFIX_COUNTER > HEX_INCR > ORDER_LINEAR > B62_INCR > CONST_SUBSTRING > MEMORY_ONLY >
UNPREDICTABLE`.

## 6. Predictability indicator and primary metric

A field is **`PREDICTABLE = 1`** iff it is admitted AND at least one **armed non-baseline rule
fires** AND the firing rule's detection fraction exceeds `B_MEMORY_REPEAT` held-out accuracy by
at least `DELTA_MEM = 0.10`. (For varying fields a deterministic rule scores ~1.0 while
`B_MEMORY_REPEAT` scores ~0, so this is a real separation from the mandated memory baseline,
not a formality.)

`B_MARKOV1` is reported as a sensitivity check but is **not** a disqualifier: the mandate's
predictability classes explicitly include "the previous value" under a nontrivial transform, so
a counter that a Markov table could also track is still a predictable class.

**Primary metric** `PREDICTABLE_PREVALENCE_POOLED = N_PREDICTABLE / N_INDICATOR_FIELDS`, where
`N_INDICATOR_FIELDS` = admitted fields with `>= 4` observations and a computable indicator.

**Secondary**: per-site prevalence, per-class prevalence, `ADMITTED_FIELDS`,
`ADMITTED_SITES`, `ADMITTED_ENDPOINTS`, `B_MEMORY_REPEAT_ACC_MEAN`, `B_MARKOV1_ACC_MEAN`,
`B_CONSTANT_MODE_ACC_MEAN`, `NULL_FP_AGGREGATE`, `PC_POWER_MIN`, `TRANSPORT_ERROR_RATE`,
`NON_GET_REQUESTS` (must be 0).

**Uncertainty**: site-clustered nonparametric bootstrap, `10 000` resamples, cluster =
registrable domain (eTLD+1 approximation = last two dot-labels; no multi-label public suffix
occurs in the frozen universe — documented). Two-sided 95% percentile interval on the pooled
prevalence. Publish the field-to-cluster map and the number of distinct cluster resamples; if
`< 1000` distinct resamples the interval is flagged uninformative and the outcome is capped at
`MIXED` even if the point thresholds are crossed.

## 7. Controls (frozen; literal DESIGN values, re-verified at EXECUTE)

### 7.1 Positive control `PC_PLANTED_CLASSES`
Eight by-construction-predictable classes, `200` trials each, RNG seed `5000 + trial`,
`n_obs in {8,10,12}`: `P_INT_INCR` (+7), `P_HEX_INCR` (+3), `P_PREFIX_COUNTER` (shell + middle
+5), `P_DEC_TS` (+30 s), `P_HEX_TS`, `P_B64_TS` (6-byte big-endian epoch seconds), `P_SESSION_BIND`
(value equals a same-session cookie), `P_HASH_BIND` (sha256 of a same-session cookie).

Literal DESIGN power: **all eight classes = 1.0.**
Pass: every class `>= PC_POWER_MIN = 0.8` at EXECUTE re-run. Construct boundary: author-authored,
so it certifies the code path, not the real-Web construct boundary — disclosed, not hidden.

### 7.2 Null control `NC_PLANTED_RANDOM_PLUS_LIVE`
- `NC_PLANTED_RANDOM`: cryptographic values over the regimes
  `{uuid4, hex32, hex64, b64_16, b64_32, b62_20, b62_43, dec16}`, `200` fields/regime,
  `n_obs = 12`, `epoch0 = 1760000000`, RNG seed `9000 + regime_index`.
  Literal DESIGN result: **1 field fired / 1600, aggregate FP = 0.000625**; per-rule max FP
  `0.000625` (`R_WALLCLOCK_B64`); **all 11 non-baseline rules armed at `ALPHA_RULE = 0.05`**.
- `NC_LIVE_HTTPBIN_UUID`: out-of-author live `GET https://httpbin.org/uuid`, batched to
  `>= 12` uuid4 values per field across `K = 8` fresh sessions. DESIGN liveness: HTTP `200`,
  deterministic uuid4 battery fires on `0/200` fields.

Pass: `NC_PLANTED_RANDOM` aggregate FP `<= 0.05` AND live-null fired-field fraction `<= 0.05`
at EXECUTE. The null has **demonstrated discriminating power**: the same rule family detects
all planted classes at 1.0 while firing on 1/1600 null fields.

### 7.3 Baselines
`B_MEMORY_REPEAT` (mandated), `B_MARKOV1` (sensitivity), `B_CONSTANT_MODE` (triviality anchor,
registered in response to the parent's mechanism-free-constant finding so no threshold is an
unanchored absolute).

## 8. Branch precedence and decision rule (frozen)

Evaluated strictly in this order:

```
1. MEASUREMENT_INVALID  if ANY measurement-invalid condition (a)-(h) holds.
                        status=MEASUREMENT_INVALID, outcome=NOT_APPLICABLE.
                        PRECEDES S0 and S1: instrument/substrate failure is NEVER FALSIFIES.
2. SUPPORTS (S1)        PV >= P_HI = 0.25  AND  site-clustered CI lower bound > P_FLOOR = 0.10.
3. FALSIFIES (S0)       PV <= P_FLOOR = 0.10  AND  site-clustered CI upper bound < P_HI = 0.25.
4. MIXED/INCONCLUSIVE   otherwise (including any CI straddling a threshold or < 1000 distinct
                        cluster resamples).
```

Measurement-invalid conditions (frozen, `spec.json`.`decision_rule`): (a) `< 20` indicator
fields; (b) `< 8` registrable sites; (c) null pass fails; (d) some planted class power `< 0.8`;
(e) transport error rate `> 0.30` or any non-GET/credentialed request; (f) `> 0.30` of admitted
fields have no frozen locator type; (g) the frozen 57-endpoint universe is not used verbatim;
(h) the rule family differs from the frozen set or a threshold is changed post hoc.

Frozen thresholds: `P_FLOOR = 0.10`, `P_HI = 0.25`, `ALPHA_RULE = 0.05`, `PC_POWER_MIN = 0.8`,
`NULL_FP_MAX = 0.05`, `DELTA_MEM = 0.10`, `N_MIN_OBS = 4`, `M_MIN_FIELDS = 20`,
`S_MIN_SITES = 8`, `TRANSPORT_ERROR_MAX = 0.30`, `CLUSTERED_BOOTSTRAP_RESAMPLES = 10000`.

## 9. Pre-freeze attainability certificate (arithmetic; literal)

- Census (`K = 3`, `J = 1`, 57 endpoints): **16 endpoints admitted (28.07%)**, **33 varying
  action-gating fields** (32 SESSION/CSRF/TOKEN + 1 `csp-nonce` NONCE), across **14 distinct
  registrable sites** (15 hostnames).
- `M_MIN_FIELDS = 20` vs pilot `33` → margin ratio `1.65x` (32 non-nonce → `1.60x`).
- `S_MIN_SITES = 8` vs pilot `14` → margin ratio `1.75x`.
- **Monotonicity argument**: the confirmatory `K = 8, J = 3` protocol observes strictly more
  values per endpoint than the census `K = 3, J = 1`, and both the variation criterion
  (`>= 2` distinct) and presence criterion (`>= 2` sessions) are monotone in the number of
  observations; the only new constraint `N_MIN_OBS = 4` is satisfied by construction at
  `K = 8, J = 3`. Admission at EXECUTE can therefore only be `>=` the census admission,
  absent server-side change.
- If, despite this certificate, EXECUTE admits `< 20` fields or `< 8` sites, the run selects
  **MEASUREMENT_INVALID** (conditions (a)/(b)) and NOT `FALSIFIES`.

## 10. Validity threats and representation loss

1. **Author-authored positive control** (Director agent prior on instruments validated only
   against their author's interventions). Mitigation: out-of-author live null
   `NC_LIVE_HTTPBIN_UUID`, 1600-field cryptographic null, and the confirmatory real-Web
   measurement. The construct boundary remains a disclosed residual threat.
2. **DESIGN-time admission census used the frozen universe.** Only *admission* (substrate
   liveness) was observed; **no real-field predictability outcome was computed**. Rule criteria
   are fixed a priori, so no selection on outcomes occurred. EXECUTE must recompute admission on
   a fresh collection; this is disclosed, not concealed.
3. **Pool and window are not a probability sample of the Web** (parent handoff
   `do_not_assume`). All rates describe the frozen 57-endpoint universe in one collection
   window on one stdlib client.
4. **Rule-family multiplicity.** 11 armed rules raise per-field false-positive risk; mitigated
   by the 1600-field calibration (aggregate FP 0.000625) and by requiring detection to exceed
   `B_MEMORY_REPEAT` by `DELTA_MEM`. The class-attribution priority can mislabel when several
   rules fire (e.g. `R_B62_INCR` also fires on digit strings); this affects the class
   breakdown, not the pooled `PREDICTABLE` indicator.
5. **Representation loss.** No JavaScript/DOM/SPA/authenticated/edge/mobile/WebSocket/GraphQL
   token is observable. Response bodies are not archived (only field values and a body sha256),
   so body-level re-derivation is not reconstructable from the packet.
6. **Live sources are nondeterministic**; `NC_LIVE_HTTPBIN_UUID` is a liveness check, not a
   frozen metric. The comparison of interest (real vs cryptographic null) is aggregate.
7. **Cluster count.** With ~14 clusters the site-clustered interval is wide; a genuinely low
   prevalence can still land in `MIXED` rather than `FALSIFIES`. This is honest, not a defect:
   the mandate asks for a prevalence with site-clustered intervals, and `MIXED` is a valid
   reported outcome.

## 11. Claim ceiling and scope

A `SUPPORTS` outcome moves `C-WEB-DYNAMICS` **at most to `EXPERIMENTAL`** for this substrate
class and window; it cannot `VALIDATE` the claim and authorises **no** Product promotion. A
`FALSIFIES` outcome is bounded to this substrate class and window; per `AGENTS.md` physics
discipline it does not close `C-WEB-DYNAMICS` or the Physics domain. `C-MEAS-VALID` and
`C-CROSSSITE` receive no event from this packet; `C-MEAS-VALID`'s substrate-side controls and
`C-CROSSSITE`'s transfer question are untouched.

## 12. Consequences of both outcomes (decision-changing by construction)

- **Positive (`S1`)**: value-level persistence has a measurable surface on credential-free
  action-gating state; a freshness/repair engine can anticipate or cheaply re-derive the next
  valid session/CSRF/nonce value from observable context (previous-value transform, issue
  order, session bind, embedded counter/timestamp). Informs the persist-values side of the
  architecture decision. Product Core still requires a separate authorising verdict.
- **Negative (`S0`)**: server-minted action-gating state is observation-bound on this substrate
  and window; value-level memoization/replay is not viable and the architecture must **persist
  procedures and paths and re-observe values fresh**. This directly informs the
  persist-procedures side of the decision.
- **Inconclusive (`SX`)**: bounds the estimate but does not decide; `UNKNOWN` remains a valid
  product answer.

## 13. DESIGN-time activity disclosure

DESIGN ran only non-outcome-bearing work: synthetic null/positive-power batteries, an admission
census (does a field vary across fresh sessions), and reachability/liveness probes. It did **not**
compute `PREDICTABLE_PREVALENCE` or apply the rule family to real minted values. The census
observed the same frozen universe; because rule criteria are fixed a priori and predictability
was never inspected, this is a substrate-attainability certificate, not an outcome — and it is
why the confirmatory admission is recomputed fresh.

## 14. EXECUTE contract and do-not-assume

EXECUTE must:

1. use the frozen `request.json`, `spec.json`, `prereg.md`, `freeze.json` and execute **exactly**
   this design;
2. keep RAW EVIDENCE, OBSERVATIONS, DERIVED MEASUREMENTS and INTERPRETATION distinct in
   `result.json`; a valid negative is `status=COMPLETE` with a negative/mixed `outcome`, and an
   instrument/substrate failure is `status=MEASUREMENT_INVALID` with `outcome=NOT_APPLICABLE`;
3. preserve the frozen identifiers `B_MEMORY_REPEAT`, `B_MARKOV1`, `B_CONSTANT_MODE`,
   `B_IRREDUCIBILITY_NULL`, `PC_PLANTED_CLASSES`, `NC_PLANTED_RANDOM_PLUS_LIVE`,
   `PREDICTABLE_PREVALENCE_POOLED`, `PREDICTABLE_PREVALENCE_SITE`,
   `PREDICTABLE_PREVALENCE_BY_CLASS`;
4. re-run the frozen null and positive-control batteries with the frozen seeds and report the
   EXECUTE re-run **separately** from the DESIGN-embedded literal values;
5. publish the field-to-cluster map, the ordered observation series, per-field firing rules, and
   the exact evidence paths/hashes;
6. not add/remove/retune a rule, not substitute an endpoint, not issue a non-GET or credentialed
   request, and not treat the absence of a separately hashed pilot file as a failure (the freeze
   control plane hashes only three files; see §top).

Do **not** assume: that this packet has already falsified or validated `C-WEB-DYNAMICS`; that
the retired response-signature estimators are revived; that the census is evidence about
predictability; that a CSP nonce is a session/CSRF token; or that the 57-endpoint pool is a
probability sample of the Web.

## 15. Evidence references

- `research/experiments/EXP-PHYSICS-37973239386/request.json` — binding `director_mandate` (claim `C-WEB-DYNAMICS`, action `CONTINUE`, `parent_handoff_disposition` `SUPERSEDE`).
- `research/experiments/EXP-PHYSICS-37385620138/handoff.json` — parent four-way `carry_forward` (preserved by reference; not silently overridden), including the `freeze-control-plane` and `identifiability-limit` findings reused here.
- `codex/experiments/EXP-FRONTIER-36293269574/report.md` — session-scoped stable-identifier prevalence 0.000 (inherited prior; motivates a prevalence estimate beyond a single value).
- `codex/experiments/EXP-FRONTIER-37385647440/report.md` — CSRF handles changed 5x/5 GETs within one session; motivates collecting intra-session `J = 3` sequences and using memory baselines.
- `codex/experiments/EXP-FRONTIER-36306528608/report.md` — `rederivable_fraction` null; mis-specified calibration anchor; motivates a calibrated null and literal pre-freeze values.
- `research/claims/registry.json` — `C-WEB-DYNAMICS` HYPOTHESIS, next_gate "orthogonal falsifiable programs on effect factorization, barriers, timescales, geometry, multiscale dynamics or other measurable mechanisms".
- `research/EXPERIMENT_PACKET.md` §1, §2, §3 — mandatory-key semantics; failure must never be encoded as falsification; DESIGN emits only `spec.json` and `prereg.md`.
