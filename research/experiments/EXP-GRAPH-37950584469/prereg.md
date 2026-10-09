# EXP-GRAPH-37950584469 — PREREGISTRATION

Lane: `graph` · Claim: `C-FRESHNESS` only · Cycle: `37949204501` · Director action: `CONTINUE` (not PIVOT, not PARK) · `cognitive_reset: true` · `parent_handoff_disposition: USE`.
Frozen companion: `spec.json` (same directory). Freeze is deterministic over `request.json`, `spec.json`, `prereg.md` only. This document is a faithful prose mirror of `spec.json`; where the two disagree, `spec.json` governs.

---

## 1. Binding mandate and how it became this experiment

`request.json.director_mandate` targets **C-FRESHNESS** and asks one two-part strategic question. That question is binding direction. The parent handoff (`EXP-GRAPH-36314193643`) is used as **continuity evidence only**; its `next_question` is advisory and is **not** the authorization. The Director explicitly **rejected** a PIVOT to `C-PARAM-INHERIT` and rejected PARKing the Graph lane.

The mandate's two parts become **one small transaction** because they share a single instrument over a single frozen anchor set:

| Mandate part | Becomes | Why it cannot be dropped |
|---|---|---|
| (i) do TWO independently written stdlib extraction paths agree on the recovered value set **and** the session-scoped verdict for at least 3 of 4 anchors, thereby separating an extraction defect from genuine representation loss | `P-EXTRACT-A`, `P-EXTRACT-B`, `M-EXTRACT-AGREE-VALUESET`, `M-EXTRACT-AGREE-VERDICT`, `M-N-SESSION-SCOPED-CONFIRMED`, gates `GATE-C1..C4`, `GATE-E1..E3` | This is the primary, load-bearing object. Single-path agreement cannot distinguish a parser bug from representation loss. |
| (ii) conditional on verified extraction, is the incumbent value-blind signal set materially more false-accepting than the value-aware channel on real value-only-rotation (`D1V`) trials | `M-FA-INCUMBENT-D1V`, `M-FA-VALUEAWARE-D1V`, `M-PAIRED-FA-DIFF-D1V`, `M-PAIRED-FA-DIFF-D1V-LOW`, `GATE B` | This is the only non-tautological discriminator, and it is predeclared **subordinate and thin**. |

**The director-mandated pre-freeze substrate.** The mandate requires a "route-valid, independently health-certified substrate BEFORE freeze" and that a screen's detection power be "measured rather than asserted." `V01` forbids DESIGN from running outcome-bearing measurements. These are reconciled by `spec.substrate_certificate` (`V02`): the certificate is built **only** from already-frozen, producer-independent Codex raw artifacts, is frozen with this design, and is **re-measured fail-closed at `GATE C`** before any confirmatory extraction. The certificate runs only a neutral presence-only detector — it extracts no values — so it cannot pre-empt the confirmatory object.

**The decisive contrast.** The parent's instrument reported **zero** distinct `wpCreateaccountToken` values on `https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount`, while accepted Codex `EXP-FRONTIER-36306528608` — producer-independent, standard library HTTP — extracted **3 distinct** `wpCreateaccountToken` values from the *identical URL* in 3 fresh sessions on the same day (2026-09-27). That same-URL discrepancy is the crux this experiment resolves.

---

## 2. What this experiment is and is not

`SB-01` … `SB-05` in `spec.json` are binding. In prose:

1. **No JavaScript, no browser, no headless rendering, no Docker, no local server, no credentials, no write verb, no side effect, no model call.** Only raw HTTP response bytes are parsed. Any zero recovery is therefore a fact about the raw bytes. `V05` declares V16 representation loss: client-side-minted values, XHR/fetch-only gating, canvas content and authenticated state are structurally invisible and remain open.
2. **Permission-boundary change is not tested** (`SB-02`). It is unreachable on credential-free public origins. The `D1V` family is value-only rotation.
3. **No cross-site transfer, no mechanism parameterization, no LLM inheritance, no delta repair, no residual-novelty economics** (`SB-03`). No event may be emitted for `C-CROSSSITE`, `C-PARAM-INHERIT`, `C-LLM-INHERIT`, `C-DELTA-REPAIR`, `C-PRODUCT-ECON` or `C-SEMANTIC-RESOLVE`.
4. **The behaviourally invisible stale cell is not measured** (`SB-04`). `M-INVISIBLE-STALE-PREV` is reported `null`, never `0.0`, and may satisfy no gate.
5. **This is not another threshold retune and not another full guard trial** (`SB-05`). No existing guard threshold is re-fit. The measured object is the *instrument's extraction validity over byte-identical stored bodies*, plus a thin conditional channel-necessity read. The parent's candidate-host pool is deliberately **not** screened.
6. `C-MEAS-VALID` is a non-owned advisory dependency (runtime/physics), **not** a claim id; this packet emits no `C-MEAS-VALID` event.

---

## 3. Substrate certificate (`V02`) — frozen and re-verified

### 3.1 Certificate evidence artifacts (already frozen, producer-independent)

| path | sha256 | role | establishes |
|---|---|---|---|
| `codex/experiments/EXP-FRONTIER-36306528608/result.json` | recorded at EXECUTE | accepted_codex | 3 distinct `wpCreateaccountToken` across 3 fresh sessions on `CAL-POS-2`; 3 distinct `authenticity_token` across 3 fresh sessions on `CAL-POS-1`; body hashes differed 3/3. |
| `codex/experiments/EXP-FRONTIER-36306528608/raw/token_stability.jsonl` | `1bbde51d4cf12c739bc68a435d03e4b0dc844672cb55acd570538b12eac3d429` | raw | The raw cross-session token-stability probe underlying the above; captured 2026-09-27T08:33Z. |
| `research/experiments/EXP-GRAPH-36314193643/raw_evidence/raw_evidence.jsonl` | `d71ee7d82a761697b04707ac31a5f170d1be02a8f776618822ccb89b521c3ace` | raw | Route validity (HTTP 200) and body variation 4/4 across four fresh sessions for `CAL-POS-1/2/3/4`; `CAL-POS-5` 404×4. |
| `research/experiments/EXP-GRAPH-36314193643/provenance.json` | `2e3109b876a10cba1817f6740460f1e04f048a86fffb5fb808f6b542509d59cc` | derived | Corroborated digests and the stdlib-only execution context of the parent capture. |

### 3.2 Anchor certificate

**Positive anchors** (`CAL-POS-5` is RETIRED: HTTP 404×4 in the parent, retained for identity continuity only, excluded from every denominator, counted as neither positive nor negative):

| id | url | evidence class | expected |
|---|---|---|---|
| `CAL-POS-1` | `https://gitlab.com/-/trial_registrations/new/` | `SPIDER_CORROBORATED` | HTTP 200; body varies 4/4; `authenticity_token` varies across fresh sessions (Frontier 3 distinct/3; parent 4 distinct/4) |
| `CAL-POS-2` | `https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount` | `SPIDER_CORROBORATED` | HTTP 200; body varies 4/4; `wpCreateaccountToken` varies (Frontier 3 distinct/3) — **the reconciliation anchor** |
| `CAL-POS-3` | `https://en.wikipedia.org/w/index.php?title=Special:UserLogin&action=form` | `SPIDER_PARTIAL` | HTTP 200; body varies 4/4; an in-list token field was detected but distinctness was never verified |
| `CAL-POS-4` | `https://meta.discourse.org/` | `A_PRIORI_CONSTRUCT` | HTTP 200; body varies 4/4; a meta csrf field was reported present but not SPIDER-corroborated |

**Negative anchors** (all four must yield zero in-list values under both paths):

`CAL-NEG-1` `https://www.iana.org/domains/reserved` · `CAL-NEG-2` `https://cdn.jsdelivr.net/gh/python/cpython@v3.12.0/README.rst` · `CAL-NEG-3` `https://www.debian.org/` · `CAL-NEG-4` `https://httpbin.org/forms/post`. All four passed the parent's `G0.3` 4/4.

### 3.3 Certificate re-measurement at GATE C

`certificate_tolerances`: route validity requires HTTP 200 in **≥ 3 of the 4** fresh sessions (the parent's 4/4 is the prior, not a hard equality); body variation requires **≥ 2** distinct `body_sha256`; the neutral presence detector must find ≥ 1 in-list field-name occurrence in ≥ 3 sessions on ≥ 3 of the 4 positive anchors. `unresolved_property`: extraction validity (whether a value is present and recoverable in the raw bytes) is deliberately **not** asserted by the certificate — it is the confirmatory object.

---

## 4. Populations, sessions and ground truth

### 4.1 Sessions (`V06`, `NC-SESSION-ISOLATION`)

`K_total = 4` sessions: `S1` is the **recorded** episode; `S2`, `S3`, `S4` are **current** sessions. Per session: a fresh `http.cookiejar.CookieJar`; **no** `Cookie` header on the first request; the four jars pairwise disjoint on `(name, value)`; `Connection: close`; a new TCP/TLS connection per request; ≥ 2.0 s between same-host requests. `NC-SESSION-ISOLATION` is `GATE-C3`, terminal on violation. A warm-jar diagnostic (`NC-TIME-VS-SESSION`, 2 same-jar re-captures per anchor) separates session-scale from time-scale rotation.

### 4.2 AGSI and recovered value

An **ACTION-GATING STATE ITEM (AGSI)** is a `(anchor, field_name)` pair whose value is (a) the `value` attribute of an `<input>`, `<textarea>` or `<select>` belonging to a `<form>` whose method is not GET; or (b) the `content` attribute of a `<meta>` element whose `name` is in the frozen capability-token name list. Gating is **structural, never behavioural**.

The **recovered exact value** is the literal attribute string after entity decoding, byte-for-byte; empty string is `PRESENT-EMPTY`; absent attribute/field is `ABSENT`. Comparison is byte-exact.

**Frozen capability-token name list** (string-shape matcher, not a mechanism — `CC-D`): `authenticity_token`, `authenticityToken`, `csrfmiddlewaretoken`, `_csrf`, `csrf_token`, `csrf-token`, `__RequestVerificationToken`, `__VIEWSTATE`, `__EVENTVALIDATION`, `wpEditToken`, `wpCreateaccountToken`, `wpCreateaccounttoken`, `wpLoginToken`, `wpCancelToken`, `form_token`, `__FORM_TOKEN`, `auth_token`, `os_authkey`, `bbl_`, `requesttoken`, `state`, `code`, `nonce`, `otp`, `user_token`, `session_token`, `authenticity`.

### 4.3 Session-scoped qualification and per-anchor verdict

An anchor's AGSI qualifies **SESSION-SCOPED** (per path) iff its URL returned HTTP 200 in ≥ 3 of 4 sessions **AND** `n_distinct_exact_values >= 2` **AND** `n_distinct_body_sha256 >= 2` (the parent's exact criterion, reused for identity continuity).

Per anchor and per path, verdict ∈ `{RECOVERED_SESSION_SCOPED, RECOVERED_INVARIANT, RECOVERED_EMPTY, NO_FIELD, UNREACHABLE}` via `spec.frozen_populations.anchor_verdict_rule`. The anchor-level verdict is the pair `(verdict_A, verdict_B)` and is **AGREED iff `verdict_A == verdict_B`**.

### 4.4 Ground truth (a raw observation, no injected drift)

For a trial `(AGSI i, current session St)`: `recorded_value` = exact value in `S1`; `live_value` = exact value in `St`; `label = STALE` iff `live_value != recorded_value` byte-exact, else `FRESH`. No drift is injected anywhere.

### 4.5 D1V (value-only rotation) family

A `D1V` trial is recorded in `S1` and current in `St` (t ∈ {S2,S3,S4}) with `live != recorded` (STALE), **and** field name, type class, form action, form method and input-name set unchanged between `S1` and `St`, **and** no transport validator (ETag, Last-Modified, Cache-Control max-age, Vary) varied. Family labels stratify reporting only; the guard never sees a family label.

---

## 5. The two extraction paths and the instrument (`V03`, `V04`, `V07`, `V08`)

- **`P-EXTRACT-A` (HTMLPARSER)** — a subclass of stdlib `html.parser.HTMLParser`; walks the tag stream and collects `<form>`, `<input>`, `<textarea>`, `<select>`, `<meta>` with attributes; entity decoding via stdlib `html.unescape`; records per in-list field the exact value / `PRESENT-EMPTY` / `ABSENT` and the structural context.
- **`P-EXTRACT-B` (REGEXLEX)** — an **independently written** byte-level lexer using `re` only for tag/attribute token boundaries plus a hand-written quote/whitespace/attribute state machine and a **hand-written** entity decoder (not `html.unescape`). It must not import `P-EXTRACT-A` or any shared extraction helper. `NC-PATH-INDEPENDENCE` requires an AST import-graph attestation and separate source hashes; a one-character perturbation of a frozen fixture must not change the agreement classification.
- **Same input guarantee (`V04`)** — both paths receive the byte-identical stored body for each `(anchor, session)`; the body sha256 is recorded and both paths must hash the same bytes.
- **Neutral certificate detector** — a third, deliberately minimal presence-only raw-byte regex for in-list `name=` occurrences, used only at `GATE C`. It extracts no values, so it cannot pre-empt the confirmatory extraction.
- **No anchor special-casing (`V07`)** — neither path, the token-name list, nor the presence detector contains anchor-, host- or URL-specific rules; an attestation confirms absence of any literal host/anchor token.

**Instrument fixtures (unit tests only, never scored — `V08`):** `SYN-CANARY-BOTH` (both paths recover exactly the same 2 `(name,value)` pairs), `SYN-EMPTY-VALUE` (both classify `PRESENT-EMPTY` and agree), `SYN-JSSTRING` (a token name only inside a JS string literal; both must recover 0 values). Fixtures are the only permitted synthetic bytes.

---

## 6. Baselines, controls and stable identifiers

Identifiers below are frozen in `spec.control_registry` and must be reused verbatim by EXECUTE, AUDIT and DIRECTOR.

### 6.1 Baselines

- **`B-SINGLE-PATH-A`** — `P-EXTRACT-A` alone; cannot self-certify.
- **`B-SINGLE-PATH-B`** — `P-EXTRACT-B` alone.
- **`B-PARENT-METHOD-REIMPL`** — documented best-effort reconstruction of the parent's recorded method (html.parser on raw bytes, non-GET form token fields and frozen-list meta tokens, no JS) over the same stored bodies. The parent preserved no code, so reconstruction is disclosed in `validity_notes`; **no gate depends on it**.
- **`B-INCUMBENT-SIGNAL-ONLY`** — the parent's value-blind signal set `CH-STRUCT-SIG + CH-TRANSPORT-VALIDATOR + CH-POSTCOND-SEM`. Used only in the conditional part-(ii) read.
- **`B-VALUE-AWARE`** — `CH-PRECOND-BINDING` only: fires iff `live exact value != recorded exact value`; a byte-equality revalidation of a recorded binding, not an inference about server-side validity.
- **`B-NO-GUARD-REPLAY`** — always reuse; raw-observation reference for STALE/FRESH accounting only.

### 6.2 Positive controls

- **`PC-EXTRACT-CANARY`** — on real `CAL-POS-1` (whose `authenticity_token` rotation is `SPIDER_CORROBORATED`), **both** paths must recover ≥ 2 distinct non-empty exact values across the 4 fresh sessions (`M-CANARY-PASS`). Failure is `MEASUREMENT_INVALID` (`F-INSTR`), never a negative about the substrate.
- **`PC-INCUMBENT-BLINDNESS`** — conditional: the incumbent's `M-FA-INCUMBENT-D1V` is reported against the frozen structural prediction of `1.0`. A measured value materially below `1.0` is a valid, decision-relevant finding that the structural argument is wrong on real pages. This tests a pre-registered prediction on real pages; incidental structural churn can break it.

### 6.3 Null controls

| id | requirement | terminal? |
|---|---|---|
| `NC-CAL-NEG-ALL-REJECTED` | all 4 negatives yield 0 in-list values under BOTH paths; any admitted value is terminal | yes (`GATE-C2`) |
| `NC-EXTRACT-EMPTY-VALUE` | both paths classify `SYN-EMPTY-VALUE` as `PRESENT-EMPTY` and agree | yes (`F-INSTR`) |
| `NC-EXTRACT-JSSTRING` | both paths recover 0 values from `SYN-JSSTRING` | yes (`F-INSTR`) |
| `NC-PATH-INDEPENDENCE` | AST import attestation + separate source hashes + perturbation invariance | yes (`F-INSTR`) |
| `NC-SESSION-ISOLATION` | disjoint jars; no first-request Cookie | yes (`GATE-C3`) |
| `NC-TIME-VS-SESSION` | warm-jar re-captures; if `M-WARMJAR-VARIATION-RATE` is within 0.10 of the fresh-jar rate, the anchor is labelled per-request/time-scale and the ceiling drops | diagnostic, no pass/fail |
| `NC-NONDEGENERATE-ESTIMATOR` | part (ii) read only if ≥ 2 distinct decisions realized and every active channel both fires and abstains once; else `DEGENERATE-NOT-EVALUABLE` | blocks part (ii) only |

### 6.4 Falsifiers

`F-INSTR` (no demonstrated instrument sensitivity → `MEASUREMENT_INVALID`), `F-REPLOSS` (both paths agree on zero/empty recovery while bodies vary → genuine representation loss, bounded), `F-UNRELIABLE` (paths disagree on ≥ 2 of 4 anchors → extraction validity not established), `F-BLIND` (part (ii): `M-PAIRED-FA-DIFF-D1V < 0.10` or clustered 97.5% lower bound ≤ 0 → incumbent not blind), `F-CERT` (substrate certificate fails at `GATE C` → `MEASUREMENT_INVALID`).

---

## 7. Metrics (stable identifiers; full registry in `spec.metric_registry`)

- **Certificate:** `M-CERT-ROUTE-OK`, `M-CERT-BODY-VARIABLE`, `M-CERT-FIELD-PRESENT`, `M-CERT-SESSION-ISOLATION-PASS`, `M-CERT-NEG-VALUES-A`, `M-CERT-NEG-VALUES-B`.
- **Extraction:** `M-DISTINCT-VALUES-A-{anchor}`, `M-DISTINCT-VALUES-B-{anchor}`, `M-EXTRACT-RATE-A-{anchor}`, `M-EXTRACT-RATE-B-{anchor}`, `M-ANCHOR-VERDICT-{anchor}`, `M-EXTRACT-AGREE-VALUESET`, `M-EXTRACT-AGREE-VERDICT`, `M-EXTRACT-KAPPA`, `M-CANARY-PASS`, `M-FIXTURE-CANARY-PASS`, `M-FIXTURE-EMPTY-AGREE`, `M-FIXTURE-JSSTRING-VALUES`, `M-N-SESSION-SCOPED-CONFIRMED`, `M-N-REPRESENTATION-LOSS`, `M-N-EXTRACTION-UNRELIABLE`, `M-WARMJAR-VARIATION-RATE`, `M-WARMJAR-BODY-VARIATION-RATE`.
- **Blindness (conditional):** `M-FA-INCUMBENT-D1V`, `M-FA-VALUEAWARE-D1V`, `M-PAIRED-FA-DIFF-D1V`, `M-PAIRED-FA-DIFF-D1V-LOW`, `M-N-D1V`, `M-N-DECISIONS-D1V`.

**Resampling unit (`V12`).** Part (ii) intervals resample **anchors** with replacement, `B = 10000`, percentile method, seed `36314193643`. No gate uses a trial-level unclustered interval; unclustered quantities are `M-DIAGNOSTIC-UNCLUSTERED-*` with an explicit do-not-use flag. **Seed determinism (`V09`):** all randomness derives from `random.Random(36314193643)`; process-randomized `hash()` is never used as a seed or key.

---

## 8. Decision rule — ordered, fail-closed, every branch pre-labelled

Every branch is pre-labelled `MEASUREMENT_INVALID`, `DATA-INSUFFICIENT`, `BOUNDED NEGATIVE`, or `VALID RESULT`. No branch converts a missing measurement into a scientific negative.

### GATE C — pre-confirmatory substrate certificate (runs before any extraction)

- `GATE-C1` — `M-CERT-ROUTE-OK >= 3` **and** `M-CERT-FIELD-PRESENT >= 3` (of 4).
- `GATE-C2` — `M-CERT-NEG-VALUES-A == 0` **and** `M-CERT-NEG-VALUES-B == 0` (all four negatives rejected by both paths).
- `GATE-C3` — `M-CERT-SESSION-ISOLATION-PASS == true`.
- Any `C1/C2/C3` failure ⇒ `status = MEASUREMENT_INVALID`, `outcome = INCONCLUSIVE`, branch `F-CERT`, no claim-level statement.
- `GATE-C4` (non-blocking) — `M-CERT-BODY-VARIABLE`: if < 3 of 4 anchors have ≥ 2 distinct body hashes ⇒ `status = COMPLETE`, `outcome = INCONCLUSIVE`, branch `NO-BODY-VARIATION`, no confirmatory read.

### GATE E — part (i), after GATE C passes

- `GATE-E1` — `M-CANARY-PASS == true`.
- `GATE-E2` — `M-FIXTURE-CANARY-PASS == true` **and** `M-FIXTURE-EMPTY-AGREE == true` **and** `M-FIXTURE-JSSTRING-VALUES == 0` **and** `NC-PATH-INDEPENDENCE` passes.
- Any `E1/E2` failure ⇒ `status = MEASUREMENT_INVALID`, `outcome = INCONCLUSIVE`, branch `F-INSTR`, no claim-level statement (no demonstrated instrument sensitivity).
- `GATE-E3` — `M-EXTRACT-AGREE-VALUESET >= 3` **and** `M-EXTRACT-AGREE-VERDICT >= 3`.
  - `E3` FAILS ⇒ `status = COMPLETE`, `outcome = MIXED`, branch `EXTRACTION-UNRELIABLE` (`M-N-EXTRACTION-UNRELIABLE >= 2`); no substrate verdict; instrument repair required.
  - `E3` PASSES ⇒ extraction VALIDATED; read anchor verdicts:
    - `D1` `M-N-SESSION-SCOPED-CONFIRMED >= 3 of 4` ⇒ `status = COMPLETE`, `outcome = SUPPORTS`, branch `EXTRACTION-DEFECT-CONFIRMED`.
    - `D2` `M-N-REPRESENTATION-LOSS >= 3 of 4` ⇒ `status = COMPLETE`, `outcome = FALSIFIES`, branch `REPRESENTATION-LOSS-CONFIRMED` (bounded: genuine V16 representation loss on this substrate class).
    - `D3` otherwise ⇒ `status = COMPLETE`, `outcome = MIXED`, branch `MIXED-ANCHORS` (report per-anchor).

### GATE B — part (ii), ONLY if D1

- If `M-N-D1V < 6` **or** `M-N-DECISIONS-D1V < 2` ⇒ branch `DATA-INSUFFICIENT-D1V`; part (ii) is reported `null` and no architectural claim is made (**not** a failure).
- Else if `M-PAIRED-FA-DIFF-D1V >= 0.10` **and** `M-PAIRED-FA-DIFF-D1V-LOW > 0` ⇒ branch `INCUMBENT-BLIND-CONFIRMED`; the bounded blindness claim is added.
- Else ⇒ branch `INCUMBENT-NOT-BLIND` (`F-BLIND`): the incumbent value-blind signal set is not materially more false-accepting than the value-aware channel on real `D1V` trials — an architecture simplification decided by measurement.
- `GATE B` branches do not change `status`/`outcome`; they are recorded under `controls` and `observations`.

### Status/outcome map (must match `spec.transmission_contract.branch_to_status_outcome_map`)

| condition | status | outcome |
|---|---|---|
| `GATE C` or `GATE E` blocking failure | `MEASUREMENT_INVALID` | `INCONCLUSIVE` |
| `C4 NO-BODY-VARIATION` | `COMPLETE` | `INCONCLUSIVE` |
| `E3` fail `EXTRACTION-UNRELIABLE` | `COMPLETE` | `MIXED` |
| `D1 EXTRACTION-DEFECT-CONFIRMED` | `COMPLETE` | `SUPPORTS` |
| `D2 REPRESENTATION-LOSS-CONFIRMED` | `COMPLETE` | `FALSIFIES` |
| `D3 MIXED-ANCHORS` | `COMPLETE` | `MIXED` |

---

## 9. Claim ceilings (`CC-A` … `CC-F`) and product consequences

- **`CC-A`** — all results are scoped to the 4 pinned credential-free, server-rendered, no-JavaScript, credential-free, GET-only anchor URLs, `K=4` fresh sessions, stdlib HTTP, on the recorded capture dates. Prevalence over "the Web" is **not** measured and must never be quoted.
- **`CC-B`** — `EXTRACTION-DEFECT-CONFIRMED` establishes only that extraction was the parent's failure mode on these anchors; it does not establish a guard operating point, a session-scope prevalence, or an economic break-even. `C-FRESHNESS` may advance at most to `EXPERIMENTAL`, only via the DIRECTOR.
- **`CC-C`** — `REPRESENTATION-LOSS-CONFIRMED` closes only the credential-free stdlib no-JS anchor-calibration path for these anchors; client-side/XHR-minted values, canvas content, authenticated state and permission-boundary change remain open.
- **`CC-D`** — the capability-token name list is a string-shape matcher, not a mechanism; family/verdict labels that depend on it inherit that limitation.
- **`CC-E`** — part (ii) is thin by construction; its gate uses an anchor-clustered interval and a declared floor; if the floor is not reached the branch is `DATA-INSUFFICIENT-D1V` and no blindness claim is made.
- **`CC-F`** — the two extraction paths are independently written but share a single authoring context; independence is **structural** (different algorithms, no shared code, AST-verified) and is corroborated by the real canary, the empty-value and JS-string fixtures, and the four negatives — not by external authorship.

**Product consequence — positive branch.** If `EXTRACTION-DEFECT-CONFIRMED` is reached, the parent's GATE 0 failure is established as an instrument/extraction defect rather than a property of the credential-free Web, the credential-free stdlib no-JS substrate remains a usable calibration substrate, and a properly-instrumented guard program is unblocked. `C-FRESHNESS` may advance at most to `EXPERIMENTAL`, only via the DIRECTOR and bounded by `CC-A..CC-F`. If `INCUMBENT-BLIND-CONFIRMED` is also reached, the value-aware channel (`CH-PRECOND-BINDING`) is confirmed necessary on real `D1V` trials and the incumbent-only guard must not be shipped as sufficient. **No promotion into Product Core is authorized by this packet.**

**Product consequence — negative branches.** If `REPRESENTATION-LOSS-CONFIRMED`, no stdlib no-JS guard can be calibrated on this anchor class; SPIDER must not ship such a gate, the public-GET program needs an explicit scope decision, and replay-by-assumption is not licensed (bounded: client-side/authenticated state remain open). If `EXTRACTION-UNRELIABLE`, no guard measurement may proceed until the instrument is repaired; keep the extraction layer under versioned dual-path test. If `INCUMBENT-NOT-BLIND`, the value-aware channel may be deleted — a real simplification decided by measurement. If `F-INSTR` or `F-CERT`, no product change is authorized. In every branch, `M-INVISIBLE-STALE-PREV` is reported `null`, never `0.0`.

---

## 10. Measurement validity (`V01` … `V12`) and reporting obligations

- **`V01`** — this spec and prereg are written before any anchor is contacted in this transaction. DESIGN performed **no** outcome-bearing measurement: no HTTP request, no extraction, no anchor/candidate probe. Anchors' behaviours are recorded as assertions with evidence class; extraction validity is left unresolved.
- **`V02`** — the substrate certificate is frozen and re-verified fail-closed at `GATE C` before any confirmatory extraction; it runs no extraction path and reports no values.
- **`V03`** — extraction-path independence (AST import attestation). **`V04`** — same byte-identical bodies to both paths. **`V05`** — no JS/browser; V16 representation loss declared. **`V06`** — session isolation. **`V07`** — no anchor special-casing. **`V08`** — anti-overfit controls (fixtures + four negatives). **`V09`** — seed determinism. **`V10`** — raw-evidence retention: full raw body per `(anchor, session)`, every record carries UTC timestamp, final URL after redirects, status, headers of interest, `body_sha256`, storage path/digest, cookie-jar digest, and the neutral detector's field-name occurrences; both paths emit per-field extracted-value artifacts. **`V11`** — frozen-input re-verification: `request.json`, `spec.json`, `prereg.md` against `freeze.json` before the first request and again after the last; any mismatch terminal; EXECUTE hashes every producer source file into `result.json.artifacts` (`role: "code"`) and `provenance.json`. **`V12`** — anchor-clustered resampling unit.

The short tags above are used in this prose; `spec.control_registry.validity_requirements` holds the canonical identifiers, which EXECUTE, AUDIT and DIRECTOR must cite:

| short tag | canonical identifier in `spec.json` |
|---|---|
| `V01` | `V01-PRE-REGISTRATION-NO-DESIGN-OUTCOME` |
| `V02` | `V02-SUBSTRATE-CERTIFICATE-FROZEN-AND-RE-VERIFIED` |
| `V03` | `V03-EXTRACTION-PATH-INDEPENDENCE` |
| `V04` | `V04-SAME-BYTES-BOTH-PATHS` |
| `V05` | `V05-NO-JS-REPRESENTATION-LOSS-DECLARED` |
| `V06` | `V06-SESSION-ISOLATION` |
| `V07` | `V07-NO-ANCHOR-SPECIAL-CASING` |
| `V08` | `V08-ANTI-OVERFIT-CONTROLS` |
| `V09` | `V09-SEED-DETERMINISM` |
| `V10` | `V10-RAW-EVIDENCE-RETENTION` |
| `V11` | `V11-FROZEN-INPUT-RE-VERIFICATION` |
| `V12` | `V12-RESAMPLING-UNIT` |

`spec.control_registry` keys such as `baselines`, `positive_controls`, `null_controls`, `falsifiers`, `gates`, `branches` and `validity_requirements` are **category names**, not identifiers; `result.json.controls` must be keyed by the nested ids (`B-*`, `PC-*`, `NC-*`, `F-*`, `GATE-*`, `CAL-*`, `SYN-*`), not by the category names.

**Code binding (`spec.code_binding`).** `scripts/freeze_experiment.py` writes exactly three sha256 keys (`request.json`, `spec.json`, `prereg.md`), and `check_scope.py` grants DESIGN `prefixes=[]`; therefore **no code artifact can be cryptographically bound at freeze, and there is deliberately no code-digest validity gate.** EXECUTE instead records hashes of every producer source file (including both extraction paths as separate files), the exact interpreter version and the stdlib-only dependency set.

**EXECUTE reporting (`spec.transmission_contract`).** `result.json` must contain all mandatory top-level fields: `schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved`. `metrics` uses the frozen `M-*` identifiers verbatim; `M-INVISIBLE-STALE-PREV` is `null` with a `reason_not_measured` field, never `0.0`. `controls` is keyed by the frozen control identifiers (`B-*`, `PC-*`, `NC-*`, `F-*`, `GATE-*`, `CAL-*`, `SYN-*`). `artifacts` entries are `{"path","sha256","role"}` with `role ∈ {raw, derived, fixture, code}`. `status`/`outcome` must match the map in §8.

---

## 11. Threats to validity and non-outcomes, stated before execution

**Threats.** (1) *Anchor construct overfit* — mitigated by the frozen name list, the same code on all anchors and negatives, and `V07`. (2) *Weak anchor evidence* — only `CAL-POS-1`/`CAL-POS-2` are Codex-corroborated; `CAL-POS-3` is `SPIDER_PARTIAL` and `CAL-POS-4` is `A_PRIORI_CONSTRUCT`; `CC-A` bounds the claim. (3) *Time- vs session-driven variation* — mitigated by `NC-TIME-VS-SESSION`. (4) *CDN/edge/geo variation* — disclosed in provenance. (5) *Representation loss* — permanent; `V05`, `CC-C`. (6) *Thin clusters and thin part-(ii) base* — `CC-E`, `DATA-INSUFFICIENT-D1V` branch. (7) *Shared authoring context* — `CC-F`. (8) *Post-freeze adaptivity* — any change to the name list, gates, paths or family rules after freeze makes the affected claim exploratory.

**Non-outcomes.** A `F-CERT`/`F-INSTR` terminal result is **not** a negative about `C-FRESHNESS` and does not lower its registry status. A `DATA-INSUFFICIENT` outcome is a power statement, not a negative. `F-REPLOSS` is a **bounded** falsification about this credential-free stdlib substrate class, not a global falsification of `C-FRESHNESS`. `F-UNRELIABLE` is an instrument finding, not a substrate verdict. `F-BLIND` is a bounded negative about the **necessity** of the value-aware channel, not a falsification of `C-FRESHNESS`. `B-NO-GUARD-REPLAY` is evidence of nothing about the candidate. No outcome licenses replay-by-assumption or promotion of any mechanism into Product Core.

---

## 12. Change control

`request.json`, `spec.json` and `prereg.md` become immutable at `freeze.json`. EXECUTE may not mutate them. AUDIT may not edit producer evidence. Any change to a gate, a threshold, the name list, an extraction path, a family rule, the anchor set or a control identifier after freeze is **exploratory** and must be reported as such, with the affected claim bounded accordingly.
