# EXP-GRAPH-36314193643 — PREREGISTRATION

Lane: `graph` · Claim: `C-FRESHNESS` only · Cycle: `36313602258` · Director action: `PIVOT`
Frozen companion: `spec.json` (same directory). Freeze is performed by deterministic code over `request.json`, `spec.json`, `prereg.md` only.

---

## 1. Binding mandate and how it became this experiment

`request.json.director_mandate.allocation` targets **C-FRESHNESS** and asks a four-part strategic question. That question is binding research direction. `handoff.next_question` from the parent is advisory continuity and is explicitly **SUPERSEDED** by this mandate; it is used below only as evidence, never as authorization.

The four parts become **one** measurement transaction because they share one instrument and one substrate: a screen over real credential-free public HTTP.

| Mandate part | Becomes | Why it cannot be dropped |
|---|---|---|
| (i) measured prevalence of session-scoped action-gating state, per site and pooled with site-clustered intervals | `M-PREV-ITEM-POOL`, `M-PREV-ITEM-PERSITE`, `M-PREV-ITEM-ADMITTED`, `M-PREV-ITEM-ADMITTED-UP97` | It *is* the population. There is no population without it. |
| (ii) does the four-channel guard reach the operating point at realized prevalence ≥ 0.20 | `M-TN-CAND`, `M-FA-CAND`, ECE family, ablation family | The capability claim. |
| (iii) is the incumbent actually blind on the value-rotation family | `M-FA-INCUMBENT-D1V`, `M-PAIRED-FA-DIFF-D1V-CL-LOW` | The **only non-tautological discriminator**. Without it the result rests on `B-NO-GUARD-REPLAY`, whose false-accept is an algebraic identity. |
| (iv) measured cost of abstention vs re-acquisition, in requests and cl100k_base tokens | `M-R-REQUESTS`, `M-R-TOKENS`, `M-UBREAK-EVEN-ABSTAIN-*`, `M-ADMISSION-REGION` | Decides admissibility. Without it a passing guard is still an architecture liability. |

**One declared narrowing of the mandate.** Part (iv) is delivered as the guard's own measured break-even abstention rate and per-item admission region. The cost of *discovering* that a replayed value has failed is **not** measured, because discovering it requires issuing the write and the mandate forbids write verbs. `M-C-RECOVER` is therefore frozen to be reported as explicit `null` with a reason. Consequence, stated in advance: this packet does **not** decide replay-versus-re-derive globally. That is `SB-02` in `spec.json` and it is not a hidden omission.

---

## 2. What this experiment is not

`SB-01` … `SB-05` in `spec.json` are binding. In prose:

1. **Permission-boundary change is not tested.** The mandate names it as the second family on which the incumbent should be blind. It is unreachable on credential-free public origins. `D2_handle_rotation` is a **disclosed substitute, not coverage**. The exact next action for the missing coverage is a credentialed single-write freshness-vs-permission probe; no lane currently certifies a substrate for it.
2. **The behaviourally invisible stale cell is not measured.** A stale item whose exact value is byte-identical across sessions (server-side token recycling, server-side validity binding) can only be detected by submitting. `M-INVISIBLE-STALE-PREV` is frozen to be reported as `null`, never `0.0`, and may not satisfy any gate. What *is* measurable — the value-collision rate `M-VALUE-COLLISION-PREV` — is a **lower-bound proxy** and is labelled as such. This is the parent handoff's part-(iii) question, and it survives this packet unanswered.
3. No cross-site transfer, no parameterization to unseen identifiers, no LLM inheritance, no authenticated state, no write verb, no browser, no JavaScript, no Docker, no model call.
4. `C-PRODUCT-ECON`, `C-CROSSSITE`, `C-PARAM-INHERIT`, `C-LLM-INHERIT` and `C-DELTA-REPAIR` are **not** claimed. Emitting claim events for any of them would be scope inflation.

---

## 3. Substrate

Real, credential-free, publicly reachable HTTPS, `urllib.request` from the standard library only, `html.parser` only. No local server of any kind, no container, no local fixture.

This is chosen because it is the only substrate class in the recent Codex window that has repeatedly produced valid, decision-changing measurement, and because the Director explicitly **rejected** the local shared-WAL / multi-worker class (67/67 HTTP 404 with the route table never bound, `EXP-GRAPH-36302977302`).

### 3.1 Transport discipline (`V19`)

- Frozen User-Agent, one string, recorded.
- ≥ 2.0 s between requests to the same host.
- At most one retry, and **only** on connection error. Zero retries on any HTTP status.
- Per-host request cap 40. Global request cap 2500. Exceeding either stops the run and reports `DATA_INSUFFICIENT-BUDGET` with the exact count — never a negative.
- A host answering a bot-challenge status (401, 403 with challenge markers, 429, 503) is recorded `BLOCKED`, excluded from the scored population, and **never** counted as a negative or as a fresh item. Per-stratum blocked and unreachable rates are reported.
- Host selection is in frozen list order, so exclusion is not outcome-dependent.

### 3.2 Candidate pool — frozen, 48 origins, 9 strata

Full ordered list in `spec.json.host_pool.candidate_pool_frozen`. Strata: `S1` GitLab-family Rails `authenticity_token` (8); `S2` Trac/Launchpad/Bugzilla form tokens (6); `S3` phpBB forums (6); `S4` Discourse `<meta csrf-token>` (4); `S5` MediaWiki edit/create tokens (6); `S6` Django/Sphinx documentation (6); `S7` WordPress/Ghost (4); `S8` Gitea/Forgejo/SourceHut (4); `S9` other self-hosted (4).

The strata exist so that the screen's detection power can be assessed **across** token mechanisms rather than on a single construct. If admitted hosts come from one stratum only, claim ceiling `CC-01` applies.

**Disjointness (`V14`).** The pool is statically disjoint from the union of every host appearing anywhere in accepted Codex evidence for lanes frontier, physics, intel, graph, runtime and product (that union is enumerated verbatim in `spec.json`). Before screening, the pool is checked against any concurrently declared frontier/physics candidate list for cycle `36313602258`; overlapping hosts are removed in frozen list order and the removal is recorded. If those files are absent, `M-POOL-DISJOINT-DYNAMIC-VERIFIED` is `false` and recorded, and the static union stands as the enforced bound. Hosts are **never added** to restore stratum balance; a stratum dropping below 2 remaining hosts sets `M-STRATUM-IMBALANCE` and emits a validity note. After removal the pool must retain ≥ 24 hosts or `G0.5` fails terminally.

### 3.3 Calibration anchors — declared as instrument, not candidates

**Positive anchors, ≥ 2 of 5 must pass (`G0.2`).**

| id | url | expected | evidence class |
|---|---|---|---|
| `CAL-POS-1` | `https://gitlab.com/-/trial_registrations/new/` | server-minted `authenticity_token` varies across fresh sessions | `SPIDER_CORROBORATED` — `EXP-FRONTIER-36306528608` raw: 3 distinct values in 3 independent fresh sessions |
| `CAL-POS-2` | `https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount` | server-minted `wpCreateaccountToken` varies across fresh sessions | `SPIDER_CORROBORATED` — same packet, 3 distinct in 3 sessions |
| `CAL-POS-3` | `https://en.wikipedia.org/w/index.php?title=Special:UserLogin&action=form` | a `wpEditToken`-family token varies across fresh sessions | `SPIDER_PARTIAL` — the field was detected; **its distinctness across sessions was never verified**. Disclosed as weak evidence. |
| `CAL-POS-4` | `https://meta.discourse.org/` | `<meta name="csrf-token">` varies across fresh sessions | `A_PRIORI_CONSTRUCT` — general knowledge, **not** SPIDER evidence |
| `CAL-POS-5` | `https://bugs.launchpad.net/ubuntu/+reportbug` | server-minted form `auth_token` varies across fresh sessions | `A_PRIORI_CONSTRUCT` — general knowledge, **not** SPIDER evidence |

**Negative anchors, all 4 of 4 must be rejected (`G0.3`).**

| id | url | expected | informative rejection? |
|---|---|---|---|
| `CAL-NEG-1` | `https://www.iana.org/domains/reserved` | 200 across 4 sessions, no session-scoped AGSI | no — expected vacuous |
| `CAL-NEG-2` | `https://cdn.jsdelivr.net/gh/python/cpython@v3.12.0/README.rst` | 200, content-pinned and byte-stable, no non-GET form | no — expected vacuous. Chosen instead of `raw.githubusercontent.com`, which is in the static exclusion union. |
| `CAL-NEG-3` | `https://www.debian.org/` | 200, GET search form, no non-GET form with a session-scoped token | no |
| `CAL-NEG-4` | `https://httpbin.org/forms/post` | 200, genuine non-GET form carrying **no** capability token, so rejection must be on the session-scoping criterion | **yes** — `SPIDER_CORROBORATED`: `EXP-FRONTIER-36306528608` recorded 0 action-gating objects and `C3` passing on only 2 of 15 candidates |

`CAL-NEG-4` is a deliberate inversion of the anchor that made `EXP-FRONTIER-36306528608` a `MEASUREMENT_INVALID`: that packet used it as a *positive* anchor and it was factually false as served. Here it is a negative anchor with Codex-corroborated behaviour. Its host appears in the historical frontier/graph host union; it is declared **instrument**, is excluded from the candidate pool, and the collision is disclosed rather than hidden. The capture protocol differs from Frontier's and the host is static, so the collision risk is negligible.

`M-CAL-NEG-INFORMATIVE-REJECTIONS` is reported. If it is 0, specificity against a session-invariant action-gating construct is **not estimated** and `CC-05` applies.

### 3.4 Anchor verification timing (`V03`, `V01`)

DESIGN probed nothing. The anchors' asserted behaviours are recorded above **as assertions with an evidence class**, and are first tested at `G0.2`/`G0.3` on the execution date, before any candidate host is screened and before any item is scored. Any failure is terminal. This removes the exact defect that killed the previous frontier attempt, where a screen with no demonstrated detection power at its own calibration site was used anyway.

---

## 4. Populations, representation and ground truth

### 4.1 Sessions (`V05`, `NC-SESSION-ISOLATION`)

`K_total = 4` sessions per host. `S1` is the **recorded** episode. `S2`, `S3`, `S4` are the **current** sessions. 3 trials per item. The mandate's `K ≥ 3` is satisfied by `K_total = 4`.

Per session: a fresh `http.cookiejar.CookieJar`; **no** `Cookie` header on the session's first request; no validator headers carried in; a new TCP/TLS connection per request. Per-session cookie-jar digests are recorded in raw evidence. Any violation of any of these is terminal.

### 4.2 Action-gating state item (AGSI) — frozen structural definition

An AGSI is a `(host, path, name)` triple whose value is:

- **(a)** the value of an `<input>`, `<textarea>` or `<select>` belonging to a `<form>` whose method is **not** GET; or
- **(b)** the `content` of a `<meta>` element whose `name` is in the frozen capability-token name list; or
- **(c)** a `Set-Cookie` value set by the origin that is referenced in (i) the query string of any non-GET form action on the host, (ii) any `<meta>` or `<input>` on a host page reachable by GET, or (iii) any `Location` header inside the session's redirect chain.

**Gating is structural, never behavioural**, because write verbs are forbidden. This is the single largest representation loss in the packet and it is permanent for this design: we never observe that the value actually gates anything.

**Representation loss, declared (`V16`, `CC-02`).** Parsing is `html.parser` on raw bytes; no JavaScript is executed. Client-side-minted values, XHR/fetch-only gating, canvas-rendered content, values inside inline JS string literals, and anything behind authentication are **structurally invisible**. A non-zero prevalence here is a floor on the real prevalence, never an estimate of it.

**Frozen capability-token name list** (structural; used for the `P-SESSION-MINTED` predicate and for family labelling, never by the guard's decision path as a mechanism): `authenticity_token`, `authenticityToken`, `csrfmiddlewaretoken`, `_csrf`, `csrf_token`, `csrf-token`, `__RequestVerificationToken`, `__VIEWSTATE`, `__EVENTVALIDATION`, `wpEditToken`, `wpCreateaccountToken`, `wpCancelToken`, `form_token`, `__FORM_TOKEN`, `auth_token`, `os_authkey`, `bbl_`, `requesttoken`, `state`, `code`, `nonce`, `otp`, `user_token`, `session_token`, `authenticity`.

**Name-list disclosure.** This is a string-shape matcher, not a mechanism. Its economics are not interpretable and its accuracy is not claimed. It is used for two reporting/stratification purposes only, and any claim that depends on it inherits that limitation.

### 4.3 Session-scoped qualification — the mandate's exact criterion

An AGSI qualifies as **SESSION-SCOPED** iff, over the sessions in which its URL returned HTTP 200 (**≥ 3 of 4 required**):

```
n_distinct_exact_values  >= 2   AND   n_distinct_body_sha256  >= 2
```

A host is **ADMITTED** iff it produced ≥ 1 qualifying AGSI and was not `BLOCKED` or unreachable in any session.

**The body-hash criterion is deliberately weak and its weakness is measured, not hidden.** Real pages vary for many reasons. `NC-BODY-CHURN` reports the rate at which the body hash varies while the value does not — that population is exactly the benign-churn control. `NC-TIME-VS-SESSION` reports `M-WARMJAR-VARIATION-RATE` from warm-jar re-captures in the same window; if that rate is within 0.10 of the fresh-jar variation rate, the claim ceiling drops to *per-request or time-scale rotation* rather than *session-scale rotation*.

### 4.4 Ground truth — a raw observation, not an inference

For a trial (item `i`, current session `S_t`):

```
recorded_value(i)  = exact value observed in S1
live_value(i, t)   = exact value observed in S_t
label = STALE  iff  live_value != recorded_value   (byte-exact)
        FRESH  iff  live_value == recorded_value
```

**No drift is injected anywhere in this packet (`V04`).** There is no injector, no synthetic state, no local server, no fixture. Every label is a byte comparison between two real responses captured on different fresh sessions. This is the single most important difference from all three prior `C-FRESHNESS` attempts, and it is what makes the prevalence, the false-accept and the blindness result un-tautological.

Session-scoped qualification is recorded as a **separate property** and is never used to define the label. A trial whose label disagrees with its family's expectation is **retained and reported**, never dropped.

### 4.5 Drift families — frozen deterministic assignment, applied after decisions are recorded

| family | definition (frozen, from observed response features) |
|---|---|
| `D1V_value_rotation` | value varies across fresh sessions **while** field name, field type, form action, form method and input-name set are unchanged **AND** the host carried no transport validator in any session |
| `D1T_validator_rotation` | value varies **and** the host's transport validator also varied. Split from `D1V` precisely so the blindness test is not contaminated by an accidental validator change. |
| `D2_handle_rotation` | the AGSI is `Set-Cookie`-derived and its value varies across fresh sessions |
| `D3_churn` | value invariant across fresh sessions while the body hash varies — the benign-churn population |
| `D4_route_change` | form action, method or input-name set changed between sessions, irrespective of value |

`D1V` is the family the structural argument predicts the incumbent cannot see. `D1V` additionally uses the capability-token name list, so it inherits the matcher limitation; that is disclosed in the family labelling.

---

## 5. The guard (frozen, no tuned parameters)

### 5.1 Input contract and the anti-leakage device (`V07`, `NC-NO-LEAKAGE`)

- **Value-blind channels:** `CH-STRUCT-SIG`, `CH-TRANSPORT-VALIDATOR`, `CH-POSTCOND-SEM`.
- **Value-aware channel:** `CH-PRECOND-BINDING` only.
- The recorded value and the label are placed in a separate dict and only `ch_precond` receives it.
- **Executable device, not a promise:** per trial, the run emits an attestation that the input dicts passed to `ch_struct`, `ch_validator` and `ch_postcond` contain **no** key from the frozen forbidden set `{recorded_value, recorded_value_sha256, label, is_stale, is_fresh, family, site, admitted}`. Coverage must be 100 % of scored trials. Any leak is terminal.
- The guard function never receives the label, the family, the site or the trial index. Family assignment is applied strictly after decisions are recorded.

This device is the whole reason part (iii) is a measurement rather than an implementation artefact. If the value-blind channels could see the value, the blindness result would be self-fulfilling.

### 5.2 Channels

- **`CH-STRUCT-SIG`** — fires iff the multiset of `(field_name, type_class)` over the page's form/input/meta field set differs between recorded and live. Value-blind. `type_class ∈ {text, hidden, password, checkbox, radio, select, textarea, submit, meta, cookie, header, unknown}`.
- **`CH-TRANSPORT-VALIDATOR`** — fires iff `etag`, `last_modified`, `max_age` or `vary` differ, or `max_age_live == 0 and max_age_recorded != 0`. If neither session carried any of `ETag`, `Last-Modified`, `Cache-Control`, the channel is **INACTIVE** — recorded per item, and never counted as passing. `M-CH-VALIDATOR-ACTIVE-RATE` is reported; if it is 0, `A-CH-VALIDATOR` is declared `STRUCTURALLY_UNINFORMATIVE` and excluded from the three-of-four count with the exclusion recorded (`V12`).
- **`CH-PRECOND-BINDING`** — the only value-aware channel. Declared predicate, frozen by the name-shape rule: `P-SESSION-MINTED` if the item's name is in the token list or the item is `Set-Cookie`-derived, else `P-INHERITABLE`. If no recorded value exists the channel is **INACTIVE-UNKNOWN** and forces abstention. Otherwise it fires iff `live_value != recorded_value`.
  **Structural disclosure (`CC-03`):** for `P-SESSION-MINTED` items this channel is a **byte-equality revalidation of a recorded binding**, not an inference about server-side validity. That is a claim-ceiling matter and is stated here, not buried.
- **`CH-POSTCOND-SEM`** — fires iff the accepting form is **absent** from the live page, or its `(normalized action, method, input-name set)` differs from recorded. Value-blind. Path normalization replaces numeric and hex segments with a placeholder and lowercases the host.

### 5.3 Decision rule — frozen, parameter-free, monotone on evidential strength

Let `k` = number of `INACTIVE-UNKNOWN` channels, `a` = number of active channels firing.

| condition | decision | situation | raw confidence |
|---|---|---|---|
| `k >= 1` | `UNKNOWN` | — | — |
| `a == 0` | `REUSE` | 0 | 0.50 |
| `a == 1`, firing ∈ {`CH-STRUCT-SIG`, `CH-TRANSPORT-VALIDATOR`} | `REUSE` | 1 | 0.65 |
| `a == 1`, firing = `CH-POSTCOND-SEM` | `ABSTAIN` | 2 | 0.75 |
| `a == 1`, firing = `CH-PRECOND-BINDING` | `ABSTAIN` | 3 | 0.80 |
| `a >= 2` | `ABSTAIN` | 4 | 0.90 |

No parameter is fitted to outcomes. The raw confidence is a **diagnostic**; it is reported as `M-ECE-RAW-GLOBAL` and may never satisfy gate `B4`.

### 5.4 Calibration — leave-one-site-out (`V13`)

Calibrated confidence = isotonic regression (stdlib PAVA, unit-tested against a hand-checked table) mapping raw confidence to observed correctness of the `REUSE`/`ABSTAIN` decision, **fitted on the other admitted sites and applied out-of-fold to the held-out site**, then pooled. No fold ever sees its own site's data. Primary ECE uses equal-mass bins over realized levels; the 10-equal-width-bins version is auxiliary. `UNKNOWN` trials are excluded from reuse/abstain accuracy and are evaluated **only** by `M-UNKNOWN-PRECISION-CAND`.

**Anti-degeneracy (`V17`, `NC-NONDEGENERATE-ESTIMATOR`).** If `M-N-CONFIDENCE-LEVELS <= 2`, the calibration arm is `DEGENERATE-NOT-EVALUABLE` and **no calibration claim may be made**. A near-perfect rule that yields a trivially calibrated map must not be over-read as a calibration success.

---

## 6. Baselines, ablations, controls — stable identifiers

These identifiers are frozen in `spec.json.control_registry` and must be reused verbatim by EXECUTE, AUDIT and DIRECTOR.

### 6.1 Baselines

- **`B-NO-GUARD-REPLAY`** — always `REUSE`, confidence 1.0. Its false-accept is an **algebraic identity** equal to the item-level prevalence. **Mandatory disclosure:** it carries no information about the candidate and is *explicitly excluded from every accept and falsifier condition*. No decision in this packet rests on it.
- **`B-INCUMBENT-SIGNAL-ONLY`** — the incumbent rule of the two inherited audit-PASS `C-FRESHNESS` packets, restated on real responses: value-blind structure signature **OR** transport-validator change, any firing ⇒ `ABSTAIN`. Structurally incapable of reading a recorded value.

### 6.2 Ablations (4, one per channel)

`A-CH-POSTCOND`, `A-CH-PRECOND`, `A-CH-VALIDATOR`, `A-CH-STRUCT` — the full guard with exactly one channel removed, adjudicated by the same frozen rule. For each: differing-decision count, the site-clustered bootstrap 97.5 % lower bound of the paired false-accept difference, and whether its channel was ever active. Decision-distinct requires differing-decisions ≥ 5 **and** a site-clustered 97.5 % lower bound of the paired difference > 0.

`A-CH-PRECOND` is the ablation that tests the central structural claim, because it is the only channel that can read a recorded value.

### 6.3 Positive controls

- **`PC-CANDIDATE-SENSITIVITY`** — sensitivity is the **pooled two-sided Fisher exact contrast** `M-ANCHOR-POWER-FISHER-P < 0.05` on abstention between positive-anchor trials passing `G0.2` and all negative-anchor trials, over all nine anchors (`p = 5.4e-05` at the `G0.2` floor; exactly `1.0` under a screen that never abstains). `M-FA-CAND-POS` and `M-TN-CAND-POS` are reported with their exact Wilson intervals as **diagnostics only**; no bound on them may gate, because a Wilson upper `< 0.1525` on a zero count needs `n ≥ 22` trials on one anchor and only 3–5 are affordable. The anchors sit outside the scored population, so this control cannot be contaminated by candidate yield.
- **`PC-INCUMBENT-BLINDNESS`** — `M-FA-INCUMBENT-POS` is reported on the same anchors against the frozen structural prediction of **1.0**. A measured value materially below 1.0 is a **valid, decision-relevant finding that the structural argument is wrong on real pages**, and it is reported as such, not suppressed.

### 6.4 Null controls

| id | requirement | what defect it removes |
|---|---|---|
| `NC-CAL-NEG-ALL-REJECTED` | all 4 negative anchors rejected with a recorded reason code; any admission is terminal | a screen that admits everything has no specificity — the exact defect in the parent's screen |
| `NC-BODY-CHURN` | on `D3` trials, candidate false-accept ≤ 0.15 (Wilson upper < 0.30) and abstention ≤ 0.30 (Wilson upper < 0.45); requires `n_D3 ≥ 20`, and `unknown` with a `CC-05` disclosure below that — never a fail | the inherited positives' noise-immunity control was satisfiable by construction because the required-path filter excluded the very fields the noise touched. Here the churn is **real and unfiltered**. The `0.15`/`0.30` bound replaces a `0.10`/`0.1525` bound that admitted **no** integer count at `n_D3 = 20` and only `0` at `n = 30`. |
| `NC-TIME-VS-SESSION` | `M-WARMJAR-VARIATION-RATE`, `M-WARMJAR-VALUE-COLLISION-RATE`; ceiling rule if within 0.10 of fresh-jar variation | separates session-scale from time-scale rotation; without it a positive is uninterpretable |
| `NC-PERMUTED-LABELS` | 1000 within-site label permutations, frozen seed; observed false-accept strictly below the 0.5th percentile of the permuted distribution and `M-PERMUTED-P < 0.01` | `EXP-INTEL-36287179392`, where an estimator was bitwise invariant to its own null and demonstrated no power |
| `NC-SESSION-ISOLATION` | no `Cookie` on any session's first request; four jars pairwise disjoint on `(name, value)` | "session-scoped" must be an operational claim, not an assertion |
| `NC-NO-LEAKAGE` | 100 % per-trial channel input-schema attestation; terminal on any leak | part (iii) must be a property of the signal set, not of the implementation |
| `NC-NONDEGENERATE-ESTIMATOR` | ≥ 3 realized levels at n ≥ 20; ≥ 2 distinct decisions; every active channel both fires and abstains | a degenerate estimator satisfying a degenerate gate (`EXP-INTEL-36287179392` class) |
| `NC-ITEM-DEPENDENCE-DISCLOSURE` | site-clustered intervals are primary; item-clustered auxiliary; trial-level unclustered computed only as `M-DIAGNOSTIC-UNCLUSTERED-*` with a do-not-use flag | each item contributes 3 trials; an unclustered interval is anticonservative and manufactures significance |

---

## 7. Metrics — stable identifiers

Full registry with definitions and units in `spec.json.metric_registry`. Primary identifiers used by gates:

- **prevalence:** `M-PREV-ITEM-POOL`, `M-PREV-ITEM-PERSITE`, `M-PREV-ITEM-ADMITTED`, `M-PREV-ITEM-ADMITTED-UP97`, `M-N-ADMITTED`, `M-N-REACHABLE`, `M-N-BLOCKED`, `M-N-STRATA-ADMITTED`
- **operating point:** `M-TP-CAND`, `M-FA-CAND`, `M-N-CAND`, `M-N-DECISIONS`, `M-TN-CAND`, `M-TN-CAND-WILSON-LOW`, `M-FA-CAND-WILSON-UP`, `M-UNKNOWN-PRECISION-CAND`, `M-ECE-GLOBAL-CAND`, `M-ECE-FRESH-CAND`, `M-ECE-STALE-CAND`, `M-ECE-BOOTSTRAP-UP-CAND`, `M-ECE-RAW-GLOBAL`, `M-N-CONFIDENCE-LEVELS`, `M-DISTINCT-DECISIONS-A-CH-POSTCOND`, `M-DISTINCT-DECISIONS-A-CH-PRECOND`, `M-DISTINCT-DECISIONS-A-CH-STRUCT`, `M-DISTINCT-DECISIONS-A-CH-VALIDATOR`, `M-N-ABLATIONS-STRUCTURALLY-INFORMATIVE`, `M-AB-PAIRED-DIFF-LOW-<CH>`
- **blindness:** `M-FA-INCUMBENT`, `M-TN-INCUMBENT`, `M-FA-INCUMBENT-D1V`, `M-FA-INCUMBENT-D1V-WILSON-LOW`, `M-BLINDNESS-COMPONENT-KNIFE-EDGE`, `M-FA-CAND-D1V`, `M-PAIRED-FA-DIFF-D1V`, `M-PAIRED-FA-DIFF-D1V-CL-LOW`, `M-FA-INCUMBENT-PERSFAMILY`, `M-CH-VALIDATOR-ACTIVE-RATE`
- **invisible cell / diagnostics:** `M-VALUE-COLLISION-PREV`, `M-VALUE-COLLISION-WILSON-LOW`, `M-INVISIBLE-STALE-PREV` **(always `null`)**, `M-WARMJAR-VARIATION-RATE`, `M-INTRASESSION-MINT-RATE`, `M-PERMUTED-P`, `M-CAL-POS-SENSITIVITY`, `M-CAL-POS-SENSITIVITY-CORROBORATED`, `M-CAL-POS-FRONTIER-VERIFIED-PASSING`, `M-ANCHOR-POWER-FISHER-P`, `M-CAL-NEG-REJECTED`, `M-CAL-NEG-INFORMATIVE-REJECTIONS`
- **economics:** `M-FA-CAND-D3`, `M-ABSTAIN-RATE-D3`, `M-N-D3`, `M-COST-GUARD-REQUESTS/TOKENS`, `M-COST-REACQ-REQUESTS/TOKENS`, `M-R-REQUESTS`, `M-R-TOKENS`, `M-UBREAK-EVEN-COMBINED-REQUESTS`, `M-UBREAK-EVEN-COMBINED-TOKENS`, `M-UBREAK-EVEN-ABSTAIN-REQUESTS`, `M-UBREAK-EVEN-ABSTAIN-TOKENS`, `M-UBREAK-EVEN-ABSTAIN-AT-M`, `M-ADMISSION-REGION`, `M-C-RECOVER` **(always `null`)**

**Unit of analysis.** Trials within an item are **not** independent (3 per item), and items within a site are not independent. Point estimates are ratios of pooled counts; **all intervals are clustered**, resampling **sites**, `B = 10000`, percentile method, seed `36314193643` (`V09`). Item-clustered intervals are auxiliary. No gate reads a trial-level unclustered interval.

**Explicitly declared null metrics** (`M-INVISIBLE-STALE-PREV`, `M-C-RECOVER`) must appear in `result.json` with value `null` and a `reason_not_measured` field. They may never be rendered as `0.0`, and they may never satisfy a gate.

---

## 8. Frozen arithmetic reachability certificate (`V02`, falsifier (c))

Computed **before** freeze, from the gate thresholds alone, with no data.

Method: Wilson score interval, `z = 1.96`, 95 %, on raw integer counts; exact Clopper-Pearson where stated; two-sided Fisher exact for the anchor power contrast.

> **Correction record.** An earlier draft of this section asserted a blindness admissible set of `28..30` at `n_D1V = 30`, required **8** abstentions for `B3`, and gated `G0.2` on a per-anchor Wilson upper `< 0.1525`. Independent recomputation during design found **all three unsatisfiable**. Blindness at `n = 30` with a Wilson lower `> 0.90` admits the empty set; `B3` admits the empty set at `n = 8`; and the per-anchor bound needs `n >= 22` trials on one anchor when only 3-5 are affordable. Left uncorrected, the accept branch was **unreachable** and the packet would have terminated at `F9` on every run while the certificate claimed to have discharged `V02`. The values below are the corrected ones, and the repair is itself a worked instance of the `V17` failure mode.

| quantity | floor | admissible counts at the floor | count of admissible values |
|---|---|---|---|
| `B2` false-accept gate on `n_stale` | 45 | `0..2` | 3 (max admissible rate 0.0444, Wilson upper 0.1483) |
| `B1` true-negative gate on `n_fresh` | 60 | `52..60` | 9 (min admissible rate 0.8667) |
| Blindness on `n_D1V`, Wilson lower `> 0.85` | 30 | BLIND `30` | **1 - declared knife-edge** |
| `B3` unknown precision, Wilson lower `> 0.72` | 10 abstentions | `10` | 1 at the floor; `{19,20}` at `n = 20` |
| `NC-BODY-CHURN` false-accept, `<=0.15` / upper `<0.30` | `n_D3 = 20` | `0..1` | 2 |
| `NC-BODY-CHURN` abstention, `<=0.30` / upper `<0.45` | `n_D3 = 20` | `0..4` | 5 |
| Anchor power, Fisher two-sided, `p < 0.05` | 2 anchors x 3 sessions vs 4 x 3 | `p = 5.4e-05` | non-degenerate |
| Admitted sites | 4 | site-clustered bootstrap over 4 units, declared THIN | - |

**Blindness is thin, and says so.** At `n_D1V = 30`, `FA = 30/30 = 1.0` carries a Wilson lower of `0.8865`, so a *perfect* observation is consistent with a true incumbent false-accept as low as 0.8865. The blindness component of `B5` is therefore a **supporting, knife-edge** criterion, and `M-BLINDNESS-COMPONENT-KNIFE-EDGE` is set `true` whenever `n_D1V <= 33`. If `n_D1V < 30`, the component is still reported but `B5` is decided on the site-clustered paired contrast alone, with the thinness disclosed. **The load-bearing part of `B5` is `M-PAIRED-FA-DIFF-D1V >= 0.10` with a clustered 97.5 % lower bound `> 0`**, which is not knife-edge. The NOT-BLIND arm likewise rests on the same clustered contrast, so neither branch of `B5` depends on a single-count decision.

**Degenerate-gate guard (`V17`), exact bands.** For the false-accept gate: `n_stale <= 20` is **UNSATISFIABLE** (zero admissible counts); `22 <= n_stale <= 33` admits exactly one value (`FA = 0`) and is **degenerate**; `n_stale >= 34` is non-degenerate. Any landing in a degenerate or unsatisfiable band takes `DATA_INSUFFICIENT-DEGENERATION`, never a pass.

**Anchor power, and why the per-anchor bound was abandoned.** A Wilson upper `< 0.1525` on a zero count needs `n >= 22` trials on a single anchor. Instead, sensitivity is a **pooled two-sided Fisher exact contrast** on abstention between positive-anchor trials that pass `G0.2` and all negative-anchor trials: `p = 5.4e-05` at the `G0.2` floor, `< 1e-6` at the expected case, and **exactly 1.0** under a screen that never abstains. That is genuinely discriminative at the `n` actually available. No per-anchor upper or lower bound is claimed, and none may gate.

**`F8` is informative at low yield.** Exact 97.5 % Clopper-Pearson upper bound on the per-host admission probability over the 48-host pool, solved as `P(X <= k | u) = 0.025`: `k = 0 -> 0.0740`, `1 -> 0.1107`, `2 -> 0.1425`, `3 -> 0.1720`, `4 -> 0.1998`, `6 -> 0.2525`, `8 -> 0.3022`. Observing **zero** admitted hosts already bounds admission above at **0.074**.

**Accept branch is PROVEN reachable on the corrected values.** Configuration: 4 admitted sites, 15 session-scoped items (>= 10 in `D1V`), 20 session-invariant items, 3 trials/item => `n_stale = 45`, `n_fresh = 60`, `n_D1V = 30`, `n_scored = 105 >= 60`, realized item-level prevalence `15/35 = 0.4286 >= 0.20`. Working point: `FA = 2/45 = 0.0444` (Wilson upper 0.1483 < 0.1525); `TN = 52/60 = 0.8667` (Wilson lower 0.8641 > 0.75); incumbent `FA(D1V) = 30/30` (Wilson lower 0.8865 > 0.85); unknown precision `20/20` (Wilson lower 0.8387 > 0.72); churn `FA = 1/20` (Wilson upper 0.2361 < 0.30); anchor Fisher `p = 5.4e-05 < 0.05`. Every accept condition is simultaneously satisfiable. `G0.4` recomputes this at execution; a non-satisfiable gate at its declared floor is terminal `MEASUREMENT_INVALID`, never a scientific negative.

## 9. Decision rule — ordered, fail-closed, every branch pre-labelled

### GATE 0 — pre-execution, before any candidate is screened or any item scored

| gate | condition | blocking | failure branch |
|---|---|---|---|
| `G0.1` | `M-TOKENIZER-PROVISIONED` | **no** | cost arm → `DATA_INSUFFICIENT-TOKENIZER`; every other arm proceeds |
| `G0.2` | `M-CAL-POS-PASS ≥ 2 of 5` | **yes** | `F9` |
| `G0.3` | `M-CAL-NEG-REJECTED == 4 of 4` | **yes** | `F9` |
| `G0.4` | arithmetic certificate satisfiable at every declared floor | **yes** | `F9` |
| `G0.5` | `M-POOL-SIZE ≥ 24` after the `V14` removal | **yes** | `F9` |

Any blocking failure ⇒ `status = MEASUREMENT_INVALID`, `outcome = INCONCLUSIVE`, claim ceiling *"C-FRESHNESS unchanged; no claim-level statement licensed"*.

### ADEQUACY — after scoring, before any gate is read

`A1` `M-N-ADMITTED ≥ 4` · `A2` `n_stale ≥ 45` · `A3` `n_fresh ≥ 60` · `A4` `n_stale(D1V) ≥ 30` · `A5` `n_scored ≥ 60` with ≥ 3 realized levels at `n ≥ 20` · `A6` `M-PREV-ITEM-POOL ≥ 0.20` (the mandate's required realized-prevalence regime).

Any failure ⇒ `status = COMPLETE`, `outcome = INCONCLUSIVE`, branch `DATA_INSUFFICIENT`, satisfied partials reported, **no gate read, no falsification**.

### ACCEPT — all of `B1`–`B6`

- `B1` `M-TN-CAND ≥ 0.85` **and** `M-TN-CAND-WILSON-LOW > 0.75`
- `B2` `M-FA-CAND ≤ 0.10` **and** `M-FA-CAND-WILSON-UP < 0.1525`
- `B3` `M-UNKNOWN-PRECISION-CAND ≥ 0.85` (≥ **10** abstentions required for a Wilson lower above 0.72; fewer ⇒ `DATA_INSUFFICIENT-ABSTENTION` and `B3` is not read. Eight was the earlier draft value and admits the empty set, so it would have forced a guaranteed `DATA_INSUFFICIENT-ABSTAIN` branch)
- `B4` `M-ECE-GLOBAL-CAND ≤ 0.15` **and** `M-ECE-FRESH-CAND ≤ 0.15` **and** `M-ECE-STALE-CAND ≤ 0.15` **and** `M-ECE-BOOTSTRAP-UP-CAND ≤ 0.18`
- `B5` `M-PAIRED-FA-DIFF-D1V ≥ 0.10` **and** `M-PAIRED-FA-DIFF-D1V-CL-LOW > 0` — **the load-bearing condition**, reinforced by the supporting blindness component `M-FA-INCUMBENT-D1V ≥ 0.95` **and** `M-FA-INCUMBENT-D1V-WILSON-LOW > 0.85`. The Wilson threshold is `0.85`, not `0.90`: at `n_D1V = 30` the Wilson lower at `30/30` is `0.8865`, so a `0.90` requirement is **unsatisfiable** and would have made the accept branch unreachable. If `n_D1V < 30`, the blindness component is reported but `B5` is decided on the clustered paired contrast alone, and `M-BLINDNESS-COMPONENT-KNIFE-EDGE` is set `true` whenever `n_D1V ≤ 33`
- `B6` ≥ 3 of 4 ablations decision-distinct, each with differing-decisions ≥ 5 and a site-clustered 97.5 % lower bound of the paired false-accept difference > 0

ACCEPT ⇒ `status = COMPLETE`, `outcome = SUPPORTS`, bounded by `CC-01`…`CC-06`.

### FALSIFIERS — evaluated in order, only when adequacy is met

| id | trigger | classification | consequence |
|---|---|---|---|
| `F1` | not `B1` | bounded falsification of the guard capability | `status=COMPLETE`, `outcome=FALSIFIES`; ceiling `CC-02`; the domain is **not** closed |
| `F2` | not `B2` | bounded falsification | as above |
| `F3` | not `B3` | bounded falsification | as above |
| `F4` | not `B4` | bounded falsification, **calibration only** | detection may survive; the packet must say so explicitly |
| `F5` | not `B5` or not `B6` | bounded negative about **necessity** — **NOT a falsification of C-FRESHNESS** | guard collapses to the incumbent; ship the cheaper incumbent; this is an architecture simplification decided by measurement |
| `F6` | `M-VALUE-COLLISION-PREV > 0.10` with Wilson lower > 0.05 | ceiling finding, **not falsification** | even a false-accept-0 guard is architecturally exposed; replay-by-assumption **not** licensed |
| `F7` | `M-COST-REACQ-REQUESTS < M-COST-GUARD-REQUESTS` **and** `M-COST-REACQ-TOKENS < M-COST-GUARD-TOKENS` at every `m ∈ {1,2,4,8,16}`, while `F1`–`F4` do not fire | economic inadmissibility — the Director's falsifier (b) | C-FRESHNESS's capability ships as a **measurement-only signal with no economic role** |
| `F8` | all `GATE 0` blocking checks pass **and** `M-N-ADMITTED < 4` | **VALID POSITIVE FINDING** — the Director's falsifier (a) | `status=COMPLETE`, `outcome=MIXED`; report `M-PREV-ITEM-ADMITTED-UP97` as an exact upper bound; the public product must be scoped to **within-episode reuse unless credentials are assumed**; C-FRESHNESS neither advanced nor lowered |
| `F9` | any `GATE 0` blocking failure, any blocking `V*` failure, non-satisfiable arithmetic, or `M-POOL-SIZE < 24` | **terminal, not falsification** | `status=MEASUREMENT_INVALID`, `outcome=INCONCLUSIVE`, no claim-level statement in either direction |

**Part (iv) is a reported output, not a gate.** `M-UBREAK-EVEN-COMBINED-*`, `M-UBREAK-EVEN-ABSTAIN-*` and `M-ADMISSION-REGION` are computed in both units from measured `R`, `M-FA-CAND` and `M-UNKNOWN-RATE-CAND`; the admissibility verdict text is **derived** from them. `F7` is evaluated against them.

### 9.1 Economics derivation (frozen)

In guard-cost units: no-guard replay costs 0 and is correct on `FRESH` trials; the guard costs 1 and costs an additional `R` whenever it abstains or false-accepts; always-re-deriving costs `R`. The guard is admissible iff

```
1 + (M-FA-CAND + M-UNKNOWN-RATE-CAND) * R  <  R
  ⟺  M-FA-CAND + M-UNKNOWN-RATE-CAND  <  (R - 1) / R
```

Hence `M-UBREAK-EVEN-COMBINED := (R-1)/R` and `M-UBREAK-EVEN-ABSTAIN := (R-1)/R − M-FA-CAND`.

- `c_guard` = 1 GET to the item's own URL + cl100k_base tokens of the **full** response body, because `CH-STRUCT-SIG` and `CH-POSTCOND-SEM` require the whole document. This charges the guard honestly for the read it performs.
- `c_reacquire` = requests and body tokens of every **intermediate hop** actually traversed from the root, **plus** the tokens of the response-body **prefix** of the item's own URL up to and including the item's serialized occurrence, because a re-deriver needs only that prefix.
- `R_requests` = measured hop depth of the item's URL. `R_tokens ≤ 1` whenever the prefix is shorter than the full body, and exceeds 1 only when intermediate hops carry more tokens than the prefix saves. **Expected outcome, stated in advance:** for one-hop items `R_requests = 1` ⇒ `M-UBREAK-EVEN-COMBINED = 0` ⇒ the guard is inadmissible, and `R_tokens < 1` ⇒ also inadmissible in tokens. The guard is admissible only on items whose measured hop depth exceeds one. That is the measured admission region, not a global verdict.
- **Reuse-count sweep** `m ∈ {1,2,4,8,16}`: `R(m)` is asserted in advance to be **m-invariant** on this substrate, because both the guard's revalidation and the re-acquisition amortise once per session by memoising their verdict. The quantity that would break the invariance — within-session re-minting forcing one revalidation per use — is itself **measured** via `M-INTRASESSION-MINT-RATE` from two extra same-session re-reads per admitted item. The packet therefore reports `M-UBREAK-EVEN-ABSTAIN-AT-M` for every `m` and states, with evidence, whether the invariance is empirical or assumed. This is how falsifier (b) is discharged on a **measured** quantity rather than a modelled sweep.
- `M-C-RECOVER` is **`null`**: not measurable without write verbs, excluded from every derivation.

---

## 10. Threats to validity, declared in advance

1. **Anchor construct overfit.** Detection power is demonstrated on CSRF-style HTML/meta token constructs. Mitigation: the 9 frozen strata and `M-N-STRATA-ADMITTED`; if admitted hosts come from one stratum, `CC-01` bounds the claim to that construct.
2. **Weak anchor evidence.** `CAL-POS-3`–`CAL-POS-5` are `SPIDER_PARTIAL` or `A_PRIORI_CONSTRUCT`; only `CAL-POS-1` and `CAL-POS-2` are Codex-corroborated. Mitigation: `M-CAL-POS-SENSITIVITY` **and** `M-CAL-POS-SENSITIVITY-CORROBORATED` reported separately; `CC-01` if no corroborated anchor passes.
3. **Time-driven versus session-driven variation.** The mandated qualification rule is fresh-jar variation, but pages vary for clock, A/B, geo and CDN reasons too. Mitigation: `NC-TIME-VS-SESSION` and the frozen ceiling rule.
4. **Bot mitigation and host selection.** Many origins will block stdlib clients. `BLOCKED` hosts are excluded, never counted as negatives, but exclusion is still a selection effect. Mitigation: frozen list order, ≥ 2.0 s pacing, per-stratum blocked/unreachable reporting, `V19`.
5. **CDN edge and geo variation.** The runner's egress is not controllable. Mitigation: record egress once; disclose in `V20`.
6. **Representation loss.** No JavaScript, no submission, structural gating only. Permanent for this design. `V16`, `CC-02`.
7. **Non-independence.** 3 trials per item, items nested in sites. Mitigation: site-clustered primary intervals, item-clustered auxiliary, unclustered explicitly flagged do-not-use.
8. **Small site-cluster.** 4 admitted sites is the frozen floor and the clustered bootstrap over 4 units is declared **THIN** in every report.
9. **Thin abstention base.** `B3` needs ≥ **10** abstentions for a Wilson lower above 0.72; fewer ⇒ `DATA_INSUFFICIENT-ABSTENTION`, gate not read. At exactly 10 the admissible set is `{10/10}`, so a 10/10 result is consistent with a true precision as low as 0.7225; at `n = 20` it widens to `{19,20}`. The report must state which regime obtained.
10. **Leakage into the value-blind channels.** Mitigated by an executable per-trial attestation (`V07`), not by promise.
11. **Name-list matcher.** The token-name list and the `P-SESSION-MINTED` predicate bind by string shape, not by observed variability. Disclosed; their economics are not claimed.
12. **Post-freeze adaptivity.** Any change to a threshold, a name list, a channel or a family rule after freeze makes the affected claim **exploratory** and must be reported as such.
13. **Missing coverage that no outcome can repair.** Permission-boundary drift (`SB-01`) and the behavioural invisible cell (`SB-05`) remain open regardless of outcome, and a clean pass on the guard must not be allowed to close them.

---

## 11. Code identity, provenance and freeze discipline (`V18`, `V15`)

### 11.0 Validity-requirement identifier binding

The preregistration body cites these requirements by short tag. `spec.json.control_registry.validity_requirements` holds the canonical identifiers, and EXECUTE, AUDIT and DIRECTOR must cite the canonical form:

| short tag used above | canonical identifier in `spec.json` |
|---|---|
| `V01` | `V01_SCREEN-CALIBRATION-FAIL-CLOSED` |
| `V02` | `V02-ARITHMETIC-REACHABILITY` |
| `V03` | `V03-ANCHOR-VERIFICATION-IS-NOT-A-DESIGN-CLAIM` |
| `V04` | `V04-NO-INJECTED-DRIFT` |
| `V05` | `V05-SESSION-ISOLATION` |
| `V06` | `V06-CONDITIONAL-VALIDATOR-ISOLATION` |
| `V07` | `V07-ANTI-LEAKAGE-EXECUTION` |
| `V08` | `V08-ESTIMATOR-POWER` |
| `V09` | `V09-RESAMPLING-UNIT` |
| `V10` | `V10-SEED-DETERMINISM` |
| `V11` | `V11-POST-HOC-EDITABILITY` |
| `V12` | `V12-ABLATION-INFORMATIVENESS` |
| `V13` | `V13-CALIBRATION-HOLDOUT-BY-SITE` |
| `V14` | `V14-HOST-POOL-DISJOINTNESS` |
| `V15` | `V15-NO-ASSERTED-CONTROL-WITHOUT-ARTIFACT` |
| `V16` | `V16-REPRESENTATION-LOSS-DISCLOSURE` |
| `V17` | `V17-DEGENERATE-GATE-GUARD` |
| `V18` | `V18-CODE-IDENTITY-AT-EXECUTE-NOT-AT-FREEZE` |
| `V19` | `V19-TRANSPORT-AND-ANTIBOT-DISCLOSURE` |
| `V20` | `V20-TIME-WINDOW-RECORDED` |
| `V21` | `V21-BLOCKING-AND-NONBLOCKING-DISJOINTNESS` |

The two strings in `spec.json.control_registry.validity_requirements` that are not identifiers — the section preamble sentence and the `validity_requirements` key itself — are prose, not controls, and are not reportable entries. No other key in `control_registry` is an identifier either: `baselines`, `positive_controls`, `null_controls`, `falsifiers` and `declared_null_metrics` are **category names**, and the reportable controls are the ids nested inside them (`B-NO-GUARD-REPLAY`, `B-INCUMBENT-SIGNAL-ONLY`, `PC-*`, `NC-*`, `F1`…`F9`, `M-INVISIBLE-STALE-PREV`, `M-C-RECOVER`). EXECUTE must key `result.json.controls` by those nested ids, not by the category names.

### 11.1 No code-digest gate, and why

`scripts/freeze_experiment.py` writes exactly three sha256 keys — `request.json`, `spec.json`, `prereg.md` — and `check_scope.py` gives DESIGN `prefixes=[]`. **No code artifact can be cryptographically bound at freeze in any lane.** Therefore:

- **There is no code-digest validity gate in this packet.** Declaring one would be unsatisfiable by construction and its failure self-inflicted, exactly as the Director's portfolio assessment established at source.
- EXECUTE instead: hashes every producer source file (sha256, `role: "code"`) into `result.json.artifacts` and `provenance.json`; records the exact interpreter version, the complete package set before and after any install, and every `pip install` with reason and disclosure, in the manner `EXP-FRONTIER-36306528608` disclosed `tiktoken`; re-verifies the three frozen inputs against `freeze.json` **before the first request and again after the last**, terminally on mismatch; and records every absolute path written with its lane.
- **One optional build-time dependency:** `pip install tiktoken` for `cl100k_base`, disclosed in `provenance.json`, with the frozen fallback that its absence (`G0.1` false) degrades **only** the cost arm. Isotonic calibration uses a **stdlib PAVA** implementation, unit-tested against a hand-checked table, so no second dependency is introduced.
- **`V15`:** a control may be reported `pass: true` only if a named artifact with a per-control sha256 exists in `result.json.artifacts`. `unknown` is legal and expected for inapplicable controls. A control reported `pass` with no artifact is **terminal `MEASUREMENT_INVALID`**. This exists because the parent's nine controls all read `observed: "verified", pass: true` while the same file deferred 7 of 8 of those computations to *"needs full"*.

---

## 12. Reporting obligations for EXECUTE

- `result.json` must contain all mandatory top-level fields: `schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved`.
- `metrics` uses the frozen `M-*` identifiers verbatim. `M-INVISIBLE-STALE-PREV` and `M-C-RECOVER` are `null` with a `reason_not_measured` field — **never** `0.0`.
- `controls` is keyed by the frozen control identifiers from §6, each with expected behaviour, observed behaviour, `pass|fail|unknown`, and artifact references.
- `artifacts` entries are `{"path","sha256","role"}` with `role ∈ {raw, derived, fixture, code}`. Every raw record is one JSON object per line with a per-line sha256, appended during capture and never rewritten (`V11`). The scored population is closed by a manifest with its count and sha256 **before** any metric is computed.
- `observations` holds direct observations only. `validity_notes` holds representation loss, environment limits and measurement caveats. `unresolved` holds what the producer cannot settle from this run — and must include the two permanently open items (`SB-01`, `SB-05`).
- Every `status`/`outcome` pair must match `spec.json.transmission_contract.branch_to_status_outcome_map`.
- A valid negative is `status = COMPLETE` with `outcome = FALSIFIES` or `MIXED`. `MEASUREMENT_INVALID` is never used to encode a scientific negative, and a missing measurement is never converted into one.

---

## 13. Non-outcomes, stated before execution

- A `F9` terminal result is **not** a negative about `C-FRESHNESS` and does not lower its registry status.
- An adequacy failure is **not** a negative; it is a power statement.
- `F8` is **not** a success for `C-FRESHNESS`'s guard; it is a measured **scope finding** about the public credential-free Web, and C-FRESHNESS is neither advanced nor lowered.
- `F5` is **not** a falsification of `C-FRESHNESS`; it is a bounded negative about the **necessity** of two channels.
- `B-NO-GUARD-REPLAY` is **not** evidence of anything about the candidate.
- `M-ECE-RAW-GLOBAL` can never satisfy `B4`.
- No outcome licenses replay of a recorded value across sessions, replay-by-assumption, or promotion of any mechanism into Product Core.
- A bounded pass on the guard **must not** be allowed to close replay-versus-re-derivation: `SB-05` remains open on every branch.

---

## 14. Change control

`request.json`, `spec.json` and `prereg.md` become immutable at `freeze.json`. EXECUTE may not mutate them. AUDIT may not edit producer evidence. Any change to a threshold, a name list, a channel definition, a family rule, the candidate pool or the anchor set after freeze is **exploratory** and must be reported as such, with the affected claim bounded accordingly.
