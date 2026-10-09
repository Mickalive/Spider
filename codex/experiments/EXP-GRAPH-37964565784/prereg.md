# EXP-GRAPH-37964565784 — PREREGISTRATION

Lane: `graph` · Claim: `C-FRESHNESS` only · Director cycle: `37963219735` · Action: `CONTINUE` (not PIVOT, not PARK) · `cognitive_reset: true` · `parent_handoff_disposition: USE`.
Frozen companion: `spec.json` (same directory). Freeze is deterministic over `request.json`, `spec.json`, `prereg.md` only. This document is a faithful prose mirror of `spec.json`; where the two disagree, `spec.json` governs.

---

## 1. Binding mandate and how it became this experiment

`request.json.director_mandate` targets **C-FRESHNESS** and asks one strategic question: with the frozen GATE-C3 session-isolation predicate **repaired at design time exactly as the audit requires**, does a re-frozen freshness-detection experiment across the four frozen credential-free anchors yield a **valid, decision-bearing measurement of session/token/endpoint drift with an explicit false-accept bound**, and does C-FRESHNESS move off HYPOTHESIS? That question is binding direction. The parent handoff (`EXP-GRAPH-37950584469`) is used as **continuity evidence only**; its `next_question` is advisory and is **not** the authorization. The Director explicitly rejected a PIVOT away from C-FRESHNESS and rejected PARKing the Graph lane.

The mandate becomes **one small transaction with two arms over one instrument and one frozen anchor set**:

| Mandate part | Becomes | Why it cannot be dropped |
|---|---|---|
| Repair GATE-C3 and re-run so the blocked read becomes licensed | `NC-SESSION-ISOLATION-REPAIRED`, `M-CERT-SESSION-ISOLATION-PASS`, `GATE-C1..C4`, `GATE-E1..E3`, `D1/D2/D3` | This converts the parent's instrument-level 4/4 dual-path agreement into a licensed `EXTRACTION-DEFECT-CONFIRMED`. |
| A valid, decision-bearing measurement of session/token/endpoint drift **with an explicit false-accept bound** | repaired trial construction (`agsi_instance_key`), `M-N-D1V`, `M-FA-INCUMBENT-D1V`, `M-FA-INCUMBENT-D1V-UB97`, `M-FA-VALUEAWARE-D1V`, `M-PAIRED-FA-DIFF-D1V[-LOW/-UB97]`, `GATE-B` | This is the genuinely new object. The parent keyed AGSIs by `field_name` alone and required exactly one occurrence, so CAL-POS-1's four `authenticity_token` forms contributed **zero** trials and `M-N-D1V` collapsed to 3. |

**The audit fix is implemented verbatim.** `audit.json` of the parent has `required_fixes[0]`: redesign GATE-C3 to exclude server-set constant configuration cookies (`preferred_language`, `GeoIP`, `NetworkProbeLimit`, `WMF-Last-Access`, `WMF-Last-Access-Global`, `CentralAuthAnonTopLevel`) from the pairwise-disjoint requirement and require disjointness only on session-identifying cookie names (or on `(name,value)` after filtering known constant names). This spec freezes exactly that predicate. `required_fixes[1]` (restore `codex/experiments/EXP-FRONTIER-36306528608/raw/token_stability.jsonl`) is a **provenance dependency only**: the file lives under `codex/`, is owned by the Codex synchronization step, and DESIGN must not create or edit it; EXECUTE records its presence/absence and hash, and GATE C re-measures live so validity does not depend on it.

**The decisive contrast remains.** The grandparent's instrument reported **zero** distinct `wpCreateaccountToken` values on `https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount`, while Frontier independently extracted **3 distinct** and the parent packet's two independent paths recovered **5 distinct** from the same URL. The parent could not license a claim because GATE-C3 failed closed on a structurally unsatisfiable literal predicate. This packet repairs the predicate before freeze and re-runs the same design.

---

## 2. What this experiment is and is not

`SB-01` … `SB-06` in `spec.json` are binding. In prose:

1. **No JavaScript, no browser, no headless rendering, no Docker, no local server, no credentials, no write verb, no side effect, no model call** (`SB-01`). Only raw HTTP response bytes are parsed. Any zero recovery is a fact about the raw bytes; `V05` declares V16 representation loss.
2. **Permission-boundary change is not tested** (`SB-02`); it is unreachable on credential-free public origins.
3. **No cross-site transfer, mechanism parameterization, LLM inheritance, delta repair or product economics** (`SB-03`). No event may be emitted for `C-CROSSSITE`, `C-PARAM-INHERIT`, `C-LLM-INHERIT`, `C-DELTA-REPAIR`, `C-PRODUCT-ECON` or `C-SEMANTIC-RESOLVE`.
4. **The behaviourally invisible stale cell is not measured** (`SB-04`): `M-INVISIBLE-STALE-PREV` is `null`, never `0.0`.
5. **This is a bounded frozen-anchor drift-and-guard-bound measurement**, not a prevalence study and not a full guard operating-point calibration (no authenticated/permission state, no product economics) (`SB-05`). The parent's candidate-host pool is not screened.
6. **No threshold is re-fit and no new mechanism is invented** (`SB-06`). The only design changes are the repaired session-isolation predicate and the repaired trial construction — changes to the measurement instrument, not to the guard.

`C-MEAS-VALID` is a non-owned advisory dependency (runtime/physics), **not** a claim id; this packet emits no `C-MEAS-VALID` event.

---

## 3. Repaired GATE-C3 predicate (`V06`, `V13`, audit required_fixes[0])

The parent's predicate — "the four fresh jars are pairwise disjoint on `(name, value)`" — is **structurally unsatisfiable** on these anchors because servers set constant configuration cookies with identical `(name, value)` in independent sessions. The repaired predicate is:

- **Allowlist (closed, frozen):** `preferred_language`, `GeoIP`, `NetworkProbeLimit`, `WMF-Last-Access`, `WMF-Last-Access-Global`, `CentralAuthAnonTopLevel`.
- **Exemption rule:** a shared cookie **name** is exempt iff it is an exact member of that frozen allowlist. Any name outside it is treated as session-identifying; if any pair of sessions for one anchor shares such a name (regardless of value), the predicate **FAILS**. New/unknown constant cookies are **not** auto-exempted (`CC-G`).
- **Sub-predicates:** `first_request_cookieless` (every first request carried no `Cookie` header); `session_identifying_disjoint` (no shared name outside the allowlist); `pairwise_disjoint_on_name_value_after_filter` (after removing allowlisted names, `(name,value)` sets disjoint).
- **Anti-gaming:** `NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS` injects a synthetic pair sharing both an allowlisted name and `_gitlab_session`; the predicate **must FAIL**. A predicate that passes this fixture is vacuous and terminal (`F-CERT`).

Observed session-identifying names (for diagnosis, not hard-coded): `_gitlab_session`, `WMF-Uniq`, `authSession`, `enwikiSession`.

---

## 4. Substrate certificate (`V02`) — frozen and re-verified

### 4.1 Certificate evidence artifacts (already frozen)

| path | sha256 | role | establishes |
|---|---|---|---|
| `research/experiments/EXP-GRAPH-37950584469/raw/records.jsonl` | `9885176e893d9651ed71e1470ebb5c5fc0db3cde410ff013d2dd5ffbbd215d69` | raw | Parent live captures: HTTP 200, `body_sha256`, cookie names/values, `jar_was_empty_before_request`, neutral-detector field-name occurrences. **No extracted values** — cannot pre-empt the extraction. |
| `research/experiments/EXP-GRAPH-37950584469/derived/session_isolation_diagnostic.json` | `adc6987dab415697562c7eebe792e9e0222ee3ca18d8df656bfe59fedcfd805c` | derived | The repair evidence: all shared pairs are constant configuration cookies; no session-identifying value is shared; all first requests cookie-free. |
| `research/experiments/EXP-GRAPH-37950584469/result.json` | `1130991374070841a94f585f3f10f9ec9fe3ea27b4e7aead6ce60c7ca3344717` | derived | Parent terminal `MEASUREMENT_INVALID` at GATE-C3 and the instrument-level 4/4 agreement + `M-N-D1V=3`. Used **only** as evidence-class corroboration and to define the trial-construction defect. |
| `research/experiments/EXP-GRAPH-37950584469/audit.json` | `8960a9f9e0b9e89216280f290b9a8ce4439a14431f757d083d1ed4d969cb647e` | derived | The independent audit naming the design defect; binding input for the repaired predicate. |
| `codex/experiments/EXP-FRONTIER-36306528608/result.json` | `7b0347ba0a34c273bca746263514665ef656803a79b2bb508b4db5638e2d0279` | accepted_codex | Producer-independent: 3 distinct `wpCreateaccountToken` / `authenticity_token` in 3 fresh sessions; body hashes differed 3/3. |
| `codex/experiments/EXP-FRONTIER-36306528608/raw/token_stability.jsonl` | `1bbde51d4cf12c739bc68a435d03e4b0dc844672cb55acd570538b12eac3d429` | raw | Raw token-stability probe; **reported absent** at parent EXECUTE time. EXECUTE records presence/absence + hash; GATE C does not depend on it. |
| `research/experiments/EXP-GRAPH-36314193643/raw_evidence/raw_evidence.jsonl` | `d71ee7d82a761697b04707ac31a5f170d1be02a8f776618822ccb89b521c3ace` | raw | Route validity (HTTP 200) and body variation 4/4 for CAL-POS-1/2/3/4; CAL-POS-5 404×4. |

### 4.2 Anchor certificate

**Positive anchors** (`CAL-POS-5` is RETIRED: 404×4, retained for identity continuity only, excluded from every denominator, counted as neither positive nor negative):

| id | url | evidence class | expected |
|---|---|---|---|
| `CAL-POS-1` | `https://gitlab.com/-/trial_registrations/new/` | `SPIDER_CORROBORATED` | HTTP 200; body varies 4/4; `authenticity_token` varies (Frontier 3 distinct/3; parent packet 16 distinct/4 — the four forms per session are the key multi-occurrence case) |
| `CAL-POS-2` | `https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount` | `SPIDER_CORROBORATED` | HTTP 200; body varies 4/4; `wpCreateaccountToken` varies (Frontier 3; parent packet 5) — **the reconciliation anchor** |
| `CAL-POS-3` | `https://en.wikipedia.org/w/index.php?title=Special:UserLogin&action=form` | `SPIDER_PARTIAL` | HTTP 200; body varies 4/4; `wpLoginToken` varies at instrument level (5 distinct/4) |
| `CAL-POS-4` | `https://meta.discourse.org/` | `A_PRIORI_CONSTRUCT` | HTTP 200; body varies 4/4; the parent found **no** in-list field under both paths (expected representation-loss candidate) |

**Negative anchors** (all four must yield zero in-list values under both paths): `CAL-NEG-1` `https://www.iana.org/domains/reserved` · `CAL-NEG-2` `https://cdn.jsdelivr.net/gh/python/cpython@v3.12.0/README.rst` · `CAL-NEG-3` `https://www.debian.org/` · `CAL-NEG-4` `https://httpbin.org/forms/post`.

### 4.3 Certificate re-measurement at GATE C

Route validity requires HTTP 200 in **≥ 3 of 4** fresh sessions (the prior 4/4 is not a hard equality); body variation requires **≥ 2** distinct `body_sha256`; the neutral presence detector must find ≥ 1 in-list field-name occurrence in ≥ 3 sessions on ≥ 3 of the 4 positive anchors; the repaired session-isolation predicate must pass. The certificate runs only the presence-only detector — it extracts no values and computes no guard trials — so it cannot pre-empt the confirmatory objects.

---

## 5. Populations, sessions, drift and ground truth

### 5.1 Sessions (`V06`, `NC-SESSION-ISOLATION-REPAIRED`)

`K_total = 4` sessions: `S1` is the **recorded** episode; `S2`, `S3`, `S4` are **current**. Per session: a fresh `http.cookiejar.CookieJar`; **no** `Cookie` header on the first request; the repaired disjointness predicate above; `Connection: close`; a new TCP/TLS connection per request; ≥ 2.0 s between same-host requests. The warm-jar diagnostic (`NC-TIME-VS-SESSION`, 2 same-jar re-captures per anchor) separates session-scale from time-scale rotation.

### 5.2 AGSI and recovered value

An **ACTION-GATING STATE ITEM (AGSI)** is an `(anchor, field_name)` pair whose value is (a) the `value` attribute of an `<input>`, `<textarea>` or `<select>` belonging to a `<form>` whose method is not GET; or (b) the `content` attribute of a `<meta>` element whose `name` is in the frozen capability-token name list. Gating is structural, never behavioural. The **recovered exact value** is the literal attribute string after entity decoding, byte-for-byte; empty is `PRESENT-EMPTY`; absent is `ABSENT`.

**Frozen capability-token name list** (string-shape matcher, not a mechanism — `CC-D`): `authenticity_token`, `authenticityToken`, `csrfmiddlewaretoken`, `_csrf`, `csrf_token`, `csrf-token`, `__RequestVerificationToken`, `__VIEWSTATE`, `__EVENTVALIDATION`, `wpEditToken`, `wpCreateaccountToken`, `wpCreateaccounttoken`, `wpLoginToken`, `wpCancelToken`, `form_token`, `__FORM_TOKEN`, `auth_token`, `os_authkey`, `bbl_`, `requesttoken`, `state`, `code`, `nonce`, `otp`, `user_token`, `session_token`, `authenticity`.

### 5.3 AGSI instance key (the trial-construction repair — `V13`)

An AGSI instance is keyed on `(anchor_id, field_name, structure_signature)` plus a **document-order occurrence ordinal** among occurrences of the same key within a session. A key contributes trials **iff its occurrence count is identical** in the recorded and current session of every pair considered; unequal-count keys are **excluded** and counted in `M-N-AGSI-EXCLUDED-UNSTABLE`. The included-key set is computed independently on both paths and must be identical. This repairs the parent's `field_name`-only keying, which required exactly one occurrence and therefore dropped CAL-POS-1's four forms entirely. This rule is frozen before any guard statistic is computed (`NC-TRIAL-CONSTRUCTION-STABILITY`).

### 5.4 Trial population and drift families

**Trial population:** all ordered recorded/current session pairs `(Sr, Sc)` with `r < c` among `S1..S4` (6 pairs), for every included AGSI instance. The `S1 → {S2,S3,S4}` subset is reported separately for continuity with the parent but is **not** the whole population.

**Drift families** (stratifications for reporting only; the guard never sees a family label): `F-FRESH`, `F-VALUE (D1V)`, `F-STRUCT`, `F-ENDPOINT` (a subset of `F-STRUCT` where `form_action` specifically differs), `F-TRANSPORT`, `F-POSTCOND`.

**D1V (value-only rotation):** `live != recorded` (STALE), field name/type class/form action/form method/input-name set unchanged, and no transport validator (`ETag`, `Last-Modified`, `Cache-Control max-age`, `Vary`) varied. This is the parent's exact D1V definition; postcond change is allowed but stratified.

### 5.5 Ground truth

For a trial `(AGSI instance i, recorded Sr, current Sc)`: `recorded_value` = exact value in `Sr`; `live_value` = exact value in `Sc`; `label = STALE` iff `live_value != recorded_value` byte-exact, else `FRESH`. This is a raw observation — no drift is injected anywhere.

---

## 6. The two extraction paths and the instrument (`V03`, `V04`, `V07`, `V08`)

- **`P-EXTRACT-A` (HTMLPARSER)** — a subclass of stdlib `html.parser.HTMLParser`; collects `<form>`, `<input>`, `<textarea>`, `<select>`, `<meta>` and records per in-list field the exact value / `PRESENT-EMPTY` / `ABSENT` plus form structural context; entity decoding via `html.unescape`.
- **`P-EXTRACT-B` (REGEXLEX)** — an **independently written** byte-level lexer using `re` only for tag/attribute token boundaries plus a hand-written attribute state machine and a **hand-written** entity decoder (not `html.unescape`). It must not import `P-EXTRACT-A` or any shared extraction helper; `NC-PATH-INDEPENDENCE` requires an AST import attestation and separate source hashes.
- **Same-input guarantee (`V04`)** — both paths receive the byte-identical stored body for each `(anchor, session)`, and both the extraction read and the guard-trial read are computed from those same bytes.
- **Neutral certificate detector** — a third, deliberately minimal presence-only raw-byte regex for in-list `name=` occurrences, used only at GATE C; it extracts no values.
- **No anchor special-casing (`V07`)** — no path, name list, detector or guard contains anchor-, host- or URL-specific rules; an attestation confirms the absence of literal host/anchor tokens.
- **Reuse note** — EXECUTE may base its files on `research/graph/freshness_detection/exp_37950584469/*` but must write separate producer files for this experiment and hash them.

**Instrument fixtures (`V08`, unit tests only, never scored):** `SYN-CANARY-BOTH`, `SYN-EMPTY-VALUE`, `SYN-JSSTRING` (extraction), and `SYN-GUARD-D1V`, `SYN-GUARD-FRESH`, `SYN-GUARD-POSTCOND` (guard logic). Synthetic bytes are permitted only here.

---

## 7. Guard model, baselines, controls and stable identifiers

Identifiers below are frozen in `spec.control_registry` and must be reused verbatim by EXECUTE, AUDIT and DIRECTOR. Decision set is `{REUSE, ABSTAIN}`; `ABSTAIN` is the product-preferred UNKNOWN/unsafe outcome.

### 7.1 Channels

| channel | activation input | fires when |
|---|---|---|
| `CH-STRUCT-SIG` | `(type_class, form_action, form_method, sorted form_input_names)` | structure differs |
| `CH-TRANSPORT-VALIDATOR` | `(ETag, Last-Modified, Cache-Control max-age, Vary)` + `final_url` | transport differs |
| `CH-POSTCOND-SEM` | in-list field-name set | field-name set differs |
| `CH-PRECOND-BINDING` | recorded vs live exact value | `live != recorded` byte-exact |

### 7.2 Baselines

- **`B-SINGLE-PATH-A`** / **`B-SINGLE-PATH-B`** — each path alone; neither can self-certify.
- **`B-PARENT-METHOD-REIMPL`** — documented best-effort reconstruction of the grandparent's recorded method over the same stored bodies; reconstruction disclosed in `validity_notes`; no gate depends on it.
- **`B-INCUMBENT-SIGNAL-ONLY`** — the value-blind incumbent: `REUSE` iff none of `CH-STRUCT-SIG`, `CH-TRANSPORT-VALIDATOR`, `CH-POSTCOND-SEM` fires. **The candidate shipped guard subject to the mandate's false-accept bound.**
- **`B-VALUE-AWARE`** — `CH-PRECOND-BINDING` only: `REUSE` iff `live == recorded`; a byte-equality revalidation, not an inference about server-side validity.
- **`B-FULL-GUARD`** — `REUSE` iff none of the four channels fires.
- **`B-NO-GUARD-REPLAY`** — always `REUSE`; raw-observation reference only.

### 7.3 Positive controls

- **`PC-EXTRACT-CANARY`** — on real `CAL-POS-1`, **both** paths must recover ≥ 2 distinct non-empty exact `authenticity_token` values across the 4 fresh sessions (`M-CANARY-PASS`). Failure is `MEASUREMENT_INVALID` (`F-INSTR`), never a negative about the substrate.
- **`PC-GUARD-LOGIC`** — on `SYN-GUARD-D1V`, the incumbent must `REUSE` and the value-aware guard must `ABSTAIN`; on `SYN-GUARD-FRESH` both must `REUSE`; on `SYN-GUARD-POSTCOND` `CH-POSTCOND-SEM` must fire and the incumbent must `ABSTAIN`. Any mismatch is terminal (`F-INSTR`).

### 7.4 Null controls

| id | requirement | terminal? |
|---|---|---|
| `NC-CAL-NEG-ALL-REJECTED` | all 4 negatives yield 0 in-list values under BOTH paths | yes (`GATE-C2`) |
| `NC-EXTRACT-EMPTY-VALUE` | both paths classify `SYN-EMPTY-VALUE` as `PRESENT-EMPTY` and agree | yes (`F-INSTR`) |
| `NC-EXTRACT-JSSTRING` | both paths recover 0 values from `SYN-JSSTRING` | yes (`F-INSTR`) |
| `NC-PATH-INDEPENDENCE` | AST import attestation + separate source hashes + perturbation invariance | yes (`F-INSTR`) |
| `NC-SESSION-ISOLATION-REPAIRED` | repaired predicate passes for every anchor/session | yes (`GATE-C3`) |
| `NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS` | a shared session-identifying name must FAIL the predicate | yes (`F-CERT`) |
| `NC-TRIAL-CONSTRUCTION-STABILITY` | keying/exclusion frozen; identical included-key set on both paths | yes (`F-INSTR`) |
| `NC-TIME-VS-SESSION` | warm-jar re-captures; timescale classification | diagnostic |
| `NC-NONDEGENERATE-ESTIMATOR` | part II read only if `M-N-D1V ≥ 6`, ≥ 2 decisions, every active channel fires and not-fires; inactive channels waived with reason and left UNKNOWN | blocks part II only |
| `NC-OPEN-GET-ONLY` | every scored request is a credential-free idempotent GET; no write/side effect | yes (`F-INSTR`) |

### 7.5 Falsifiers

`F-INSTR` (no demonstrated instrument/guard sensitivity → `MEASUREMENT_INVALID`), `F-CERT` (repaired certificate fails → `MEASUREMENT_INVALID`), `F-REPLOSS` (both paths agree on zero/empty recovery while bodies vary → genuine representation loss, bounded), `F-UNRELIABLE` (paths disagree on ≥ 2 of 4 anchors), `F-BLIND` (part II: `M-PAIRED-FA-DIFF-D1V < 0.10` or clustered 97.5% lower bound ≤ 0 → incumbent not blind).

---

## 8. Metrics (stable identifiers; full registry in `spec.metric_registry`)

- **Certificate:** `M-CERT-ROUTE-OK`, `M-CERT-BODY-VARIABLE`, `M-CERT-FIELD-PRESENT`, `M-CERT-SESSION-ISOLATION-PASS`, `M-CERT-FIRST-REQUEST-COOKIELESS`, `M-CERT-SESSION-IDENTIFYING-DISJOINT`, `M-CERT-CONSTCONFIG-SHARED-NAMES`, `M-CERT-UNEXPECTED-SHARED-NAMES`, `M-CERT-NEG-VALUES-A`, `M-CERT-NEG-VALUES-B`.
- **Extraction:** `M-DISTINCT-VALUES-A/B-{anchor}`, `M-EXTRACT-RATE-A/B-{anchor}`, `M-ANCHOR-VERDICT-{anchor}`, `M-EXTRACT-AGREE-VALUESET`, `M-EXTRACT-AGREE-VERDICT`, `M-EXTRACT-KAPPA`, `M-CANARY-PASS`, `M-FIXTURE-CANARY-PASS`, `M-FIXTURE-EMPTY-AGREE`, `M-FIXTURE-JSSTRING-VALUES`, `M-N-SESSION-SCOPED-CONFIRMED`, `M-N-REPRESENTATION-LOSS`, `M-N-EXTRACTION-UNRELIABLE`, `M-WARMJAR-VARIATION-RATE`, `M-WARMJAR-BODY-VARIATION-RATE`, `M-WARMJAR-FRESH-VALUE-VARIATION-RATE`, `M-ROTATION-TIMESCALE-{anchor}`.
- **Drift & guard (mandated false-accept bound):** `M-N-AGSI-INSTANCES`, `M-N-AGSI-EXCLUDED-UNSTABLE`, `M-N-TRIALS`, `M-N-FRESH`, `M-N-D1V`, `M-N-D1V-ANCHORS`, `M-N-STRUCT-DRIFT`, `M-N-ENDPOINT-DRIFT`, `M-N-TRANSPORT-DRIFT`, `M-N-POSTCOND-DRIFT`, `M-FA-INCUMBENT-D1V`, `M-FA-INCUMBENT-D1V-UB97`, `M-FA-VALUEAWARE-D1V`, `M-FA-VALUEAWARE-D1V-UB97`, `M-PAIRED-FA-DIFF-D1V`, `M-PAIRED-FA-DIFF-D1V-LOW`, `M-PAIRED-FA-DIFF-D1V-UB97`, `M-FA-INCUMBENT-ALL`, `M-FA-VALUEAWARE-ALL`, `M-FR-INCUMBENT-FRESH`, `M-FR-VALUEAWARE-FRESH`, `M-N-DECISIONS-D1V`, `M-GUARD-FIXTURE-PASS`, `M-INVISIBLE-STALE-PREV` (null).

**Resampling unit (`V12`).** Part II intervals resample **anchors** with replacement, `B = 10000`, percentile method, seed `37964565784`; a trial-level unclustered interval is reported only as `M-DIAGNOSTIC-UNCLUSTERED-*` with a do-not-use flag. **Seed determinism (`V09`):** all randomness derives from `random.Random(37964565784)`; process-randomized `hash()` is never used as a seed or key. The parent seed `36314193643` is retained only where a parent-derived quantity is explicitly recomputed for continuity.

---

## 9. Decision rule — ordered, fail-closed, every branch pre-labelled

Every branch is pre-labelled `MEASUREMENT_INVALID`, `DATA-INSUFFICIENT`, `BOUNDED NEGATIVE`, or `VALID RESULT`. No branch converts a missing or invalid measurement into a scientific negative.

### GATE C — pre-confirmatory certificate (runs before any extraction)

- `GATE-C1` — `M-CERT-ROUTE-OK ≥ 3` **and** `M-CERT-FIELD-PRESENT ≥ 3` (of 4).
- `GATE-C2` — `M-CERT-NEG-VALUES-A == 0` **and** `M-CERT-NEG-VALUES-B == 0`.
- `GATE-C3` — `M-CERT-SESSION-ISOLATION-PASS == true` (repaired) **and** `NC-CONSTCONFIG-EXCLUSION-NOT-VACUOUS == true`.
- Any `C1/C2/C3` failure ⇒ `status = MEASUREMENT_INVALID`, `outcome = INCONCLUSIVE`, branch `F-CERT`, no claim-level statement.
- `GATE-C4` (non-blocking) — `M-CERT-BODY-VARIABLE < 3` ⇒ `COMPLETE` / `INCONCLUSIVE` / branch `NO-BODY-VARIATION`.

### GATE E — Part I (after GATE C passes)

- `GATE-E1` — `M-CANARY-PASS == true`.
- `GATE-E2` — `M-FIXTURE-CANARY-PASS` **and** `M-FIXTURE-EMPTY-AGREE` **and** `M-FIXTURE-JSSTRING-VALUES == 0` **and** `M-GUARD-FIXTURE-PASS` **and** `NC-PATH-INDEPENDENCE` **and** `NC-TRIAL-CONSTRUCTION-STABILITY`.
- Any `E1/E2` failure ⇒ `MEASUREMENT_INVALID` / `INCONCLUSIVE` / branch `F-INSTR`.
- `GATE-E3` — `M-EXTRACT-AGREE-VALUESET ≥ 3` **and** `M-EXTRACT-AGREE-VERDICT ≥ 3`.
  - `E3` FAILS ⇒ `COMPLETE` / `MIXED` / branch `EXTRACTION-UNRELIABLE` (`M-N-EXTRACTION-UNRELIABLE ≥ 2`).
  - `E3` PASSES ⇒ extraction VALIDATED; read anchor verdicts:
    - `D1` `M-N-SESSION-SCOPED-CONFIRMED ≥ 3 of 4` ⇒ `COMPLETE` / `SUPPORTS` / branch `EXTRACTION-DEFECT-CONFIRMED`.
    - `D2` `M-N-REPRESENTATION-LOSS ≥ 3 of 4` ⇒ `COMPLETE` / `FALSIFIES` / branch `REPRESENTATION-LOSS-CONFIRMED` (bounded).
    - `D3` otherwise ⇒ `COMPLETE` / `MIXED` / branch `MIXED-ANCHORS`.

### GATE B — Part II, the mandated explicit false-accept bound (ONLY if D1)

- If `M-N-D1V < 6` **or** `M-N-DECISIONS-D1V < 2` **or** `NC-NONDEGENERATE-ESTIMATOR` fails (after its pre-registered `INACTIVE-ON-POPULATION` waiver) ⇒ branch `DATA-INSUFFICIENT-D1V`; Part II reported `null` with its reason and no false-accept/blindness claim (**not** a failure).
- Else if `M-PAIRED-FA-DIFF-D1V ≥ 0.10` **and** `M-PAIRED-FA-DIFF-D1V-LOW > 0` ⇒ branch `INCUMBENT-BLIND-CONFIRMED`: report `M-FA-INCUMBENT-D1V` and its `UB97` as the explicit false-accept bound; value-aware binding is necessary on this class.
- Else ⇒ branch `INCUMBENT-NOT-BLIND` (`F-BLIND`): the incumbent value-blind set is not materially more false-accepting than the value-aware channel on real `D1V` trials — a measured architecture simplification.
- `GATE B` branches do not change `status`/`outcome`; they are recorded under `metrics`, `controls` and `observations`.

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

## 10. Claim ceilings (`CC-A` … `CC-H`) and product consequences

- **`CC-A`** — scoped to the 4 pinned credential-free, server-rendered, no-JS, GET-only anchors, `K=4` fresh sessions, stdlib HTTP, recorded capture date(s) and one egress ASN; prevalence over "the Web" is never quoted.
- **`CC-B`** — `EXTRACTION-DEFECT-CONFIRMED` establishes the parent's failure mode on these anchors; combined with a **read** Part II bound it measures the incumbent guard's behaviour on real value-only rotation. `C-FRESHNESS` may advance at most to `EXPERIMENTAL`, only via the DIRECTOR.
- **`CC-C`** — `REPRESENTATION-LOSS-CONFIRMED` closes only the credential-free stdlib no-JS calibration path for these anchors.
- **`CC-D`** — the token-name list and drift-family labels are string/structure-shape matchers, not mechanisms.
- **`CC-E`** — Part II bounds are anchor-clustered, descriptive and coarse with few anchors; no prevalence may be read.
- **`CC-F`** — the two paths are independently written but share one authoring context; independence is structural (AST-verified) and corroborated by the canary, fixtures and negatives.
- **`CC-G`** — the repaired predicate exempts only the closed, frozen constant-configuration allowlist; any other shared name fails GATE-C3.
- **`CC-H`** — if `M-ROTATION-TIMESCALE` is `PER_REQUEST_SCALE`, a value-binding verdict on that anchor is bounded to per-request/time-scale applicability and must not be described as session-scoped durability.

**Product consequence — positive.** If `EXTRACTION-DEFECT-CONFIRMED` is reached, the grandparent's 4/5 zero-distinct failure is established as an instrument/extraction defect rather than a property of the credential-free Web, and the credential-free stdlib no-JS substrate remains usable for C-FRESHNESS; C-FRESHNESS may advance at most to `EXPERIMENTAL`, only via the DIRECTOR. If `INCUMBENT-BLIND-CONFIRMED`, the measured false-accept bound shows the value-blind incumbent guard is unsafe on real value-only rotation, so the shipped architecture must retain `CH-PRECOND-BINDING`; the value-aware guard's near-zero bound is the operating evidence. If `PER_REQUEST_SCALE`, recording a token yields no durable freshness, so the guard must be a short-lived applicability check, not a cache. **No promotion into Product Core is authorized by this packet.**

**Product consequence — negative.** If `REPRESENTATION-LOSS-CONFIRMED`, no stdlib no-JS guard can be calibrated on this anchor class; SPIDER must not ship such a gate, the public-GET program needs an explicit scope decision, and replay-by-assumption is not licensed (bounded). If `EXTRACTION-UNRELIABLE`, no guard measurement may proceed until the instrument is repaired. If `INCUMBENT-NOT-BLIND`, the value-aware channel may be deleted — a real simplification. If `DATA-INSUFFICIENT-D1V`, Part II is null and only the Part I read is licensed; this is a power statement, not a negative. If `F-INSTR` or `F-CERT`, no product change is authorized; C-FRESHNESS stays HYPOTHESIS. In every branch `M-INVISIBLE-STALE-PREV` is `null`, never `0.0`.

---

## 11. Measurement validity (`V01` … `V14`) and reporting obligations

- **`V01`** — written before any anchor is contacted; DESIGN ran no outcome-bearing measurement.
- **`V02`** — the certificate is frozen and re-verified fail-closed at GATE C; it runs no extraction and reports no values.
- **`V03`** — path independence. **`V04`** — same byte-identical bodies for the extraction and guard reads. **`V05`** — no JS/browser; V16 representation loss declared. **`V06`** — repaired session-isolation predicate. **`V07`** — no anchor special-casing. **`V08`** — anti-overfit controls (fixtures incl. guard fixtures + four negatives). **`V09`** — seed determinism. **`V10`** — raw-evidence retention: full raw body per `(anchor, session)`; every record carries UTC timestamp, final URL after redirects, status, headers of interest (incl. `ETag`, `Last-Modified`, `Cache-Control`, `Vary`), `body_sha256`, storage path/digest, cookie-jar digest, and neutral-detector names; both paths emit per-field extracted values and the guard emits per-trial decisions. **`V11`** — frozen-input re-verification before and after execution. **`V12`** — anchor-clustered resampling unit. **`V13`** — trial-construction stability. **`V14`** — guard non-degeneracy.

| short tag | canonical identifier in `spec.json` |
|---|---|
| `V01` | `V01-PRE-REGISTRATION-NO-DESIGN-OUTCOME` |
| `V02` | `V02-SUBSTRATE-CERTIFICATE-FROZEN-AND-RE-VERIFIED` |
| `V03` | `V03-EXTRACTION-PATH-INDEPENDENCE` |
| `V04` | `V04-SAME-BYTES-BOTH-PATHS` |
| `V05` | `V05-NO-JS-REPRESENTATION-LOSS-DECLARED` |
| `V06` | `V06-SESSION-ISOLATION-REPAIRED` |
| `V07` | `V07-NO-ANCHOR-SPECIAL-CASING` |
| `V08` | `V08-ANTI-OVERFIT-CONTROLS` |
| `V09` | `V09-SEED-DETERMINISM` |
| `V10` | `V10-RAW-EVIDENCE-RETENTION` |
| `V11` | `V11-FROZEN-INPUT-RE-VERIFICATION` |
| `V12` | `V12-RESAMPLING-UNIT` |
| `V13` | `V13-TRIAL-CONSTRUCTION-STABILITY` |
| `V14` | `V14-GUARD-NONDEGENERACY` |

`spec.control_registry` keys such as `baselines`, `positive_controls`, `null_controls`, `falsifiers`, `gates`, `branches`, `guard_channels` and `validity_requirements` are **category names**, not identifiers; `result.json.controls` must be keyed by the nested ids (`B-*`, `PC-*`, `NC-*`, `F-*`, `GATE-*`, `CH-*`, `CAL-*`, `SYN-*`), not by the category names.

**Code binding (`spec.code_binding`).** `scripts/freeze_experiment.py` writes exactly three sha256 keys (`request.json`, `spec.json`, `prereg.md`), and `check_scope.py` grants DESIGN no code prefix; therefore no code artifact can be cryptographically bound at freeze and there is deliberately no code-digest validity gate. EXECUTE instead records hashes of every producer source file (both extraction paths and the guard as separate files), the interpreter version and the stdlib-only dependency set.

**EXECUTE reporting (`spec.transmission_contract`).** `result.json` must contain all mandatory top-level fields: `schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved`. `metrics` uses the frozen `M-*` identifiers verbatim; the Part II quantities and `M-INVISIBLE-STALE-PREV` are reported `null` with an explicit `reason_not_measured` when not read, never `0.0`. `controls` is keyed by the frozen control identifiers. `artifacts` entries are `{"path","sha256","role"}` with `role ∈ {raw, derived, fixture, code}`. `status`/`outcome` must match the map in §9.

---

## 12. Threats to validity and non-outcomes, stated before execution

**Threats.** (1) *Anchor construct overfit* — mitigated by the frozen name list, the same code on all anchors and negatives, and `V07`. (2) *Weak anchor evidence* — only `CAL-POS-1`/`CAL-POS-2` are Codex-corroborated; `CAL-POS-3` is `SPIDER_PARTIAL` and `CAL-POS-4` is `A_PRIORI_CONSTRUCT`; `CC-A` bounds the claim. (3) *Time- vs session-driven variation* — mitigated by `NC-TIME-VS-SESSION` and the timescale classification (`CC-H`). (4) *CDN/edge/geo variation* — disclosed in provenance. (5) *Representation loss* — permanent; `V05`, `CC-C`. (6) *Thin anchor clusters for Part II* — `CC-E`; `DATA-INSUFFICIENT-D1V` is available. (7) *Guard tautology* — the incumbent's D1V false accept is structurally ~1.0; `NC-NONDEGENERATE-ESTIMATOR` plus the non-D1V strata (`M-FA-INCUMBENT-ALL`, `M-FR-*-FRESH`) are reported so the point estimate is not over-read. (8) *Inactive channel* — `CH-POSTCOND-SEM` may never fire if the field-name set is constant; it is then reported `INACTIVE-ON-POPULATION` with its reason and the postcond drift family stays `UNKNOWN` (exercised only by the unscored fixture). (9) *Shared authoring context* — `CC-F`. (10) *Post-freeze adaptivity* — any change to the name list, predicate, gates, paths, keying or family rules after freeze makes the affected claim exploratory.

**Non-outcomes.** `F-CERT`/`F-INSTR` are **not** negatives about `C-FRESHNESS` and do not lower its registry status. `DATA-INSUFFICIENT-D1V` is a power statement, not a negative. `F-REPLOSS` is a **bounded** falsification about this credential-free stdlib substrate class, not a global falsification of `C-FRESHNESS`. `F-UNRELIABLE` is an instrument finding, not a substrate verdict. `F-BLIND` is a bounded negative about the **necessity** of the value-aware channel, not a falsification of `C-FRESHNESS`. `B-NO-GUARD-REPLAY` is evidence of nothing about the candidate. No outcome licenses replay-by-assumption or promotion of any mechanism into Product Core. `M-INVISIBLE-STALE-PREV` and `SB-02` permission drift remain unmeasured by design.

---

## 13. Change control

`request.json`, `spec.json` and `prereg.md` become immutable at `freeze.json`. EXECUTE may not mutate them. AUDIT may not edit producer evidence. Any change to a gate, threshold, the name list, the repaired predicate, an extraction path, the trial-keying rule, a family rule, the anchor set or a control identifier after freeze is **exploratory** and must be reported as such, with the affected claim bounded accordingly.
