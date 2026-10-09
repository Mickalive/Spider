# EXP-FRONTIER-37385647440 — stationarity of interface state on the credential-free public HTTP substrate

**Lane:** frontier · **Stage:** EXECUTE · **Status:** `MEASUREMENT_INVALID` · **Outcome:** `INCONCLUSIVE`
**Frozen decision branch applied:** `CONTROLS_FAIL` (from `spec.json decision_rule.outcome_mapping`)
**Canonical machine handoff:** `result.json` · `provenance.json`

This report explains and does not exceed `result.json`. Every number below is emitted from
`derived/*.json` by `research/frontier/emit_result_37385647440.py`; nothing is hand-transcribed.

---

## 1. Headline

The frozen experiment cannot return a scientific answer, and the reason is not that the web
misbehaved — it is that **the frozen instrument could not have returned its own negative or its
own positive.**

Two of the four frozen controls failed, and the frozen `controls_gate` maps any control FAIL to
`status=MEASUREMENT_INVALID`. Independently of the live substrate, the frozen falsifier's trigger
region is provably empty (VN-07): its cost condition compares shortest-path re-acquisition against
breadth-first re-derivation, and breadth-first can never be cheaper, so `outcome=FALSIFIES` was
unreachable for any execution of this design.

What the run *does* deliver is a trustworthy instrument-validity finding and three substrate
observations that are consistent with, and bounded by, the parent handoff.

---

## 2. What was executed

| | |
|---|---|
| Frozen targets | 6 (`gitlab`, `wikimedia`, `wikipedia`, `bitbucket`, `httpbin`, `postman_echo`) — no substitution |
| Sessions per target | K=5, disjoint cookie jars, min measured inter-session delay **93.81 s** (≥ 60 s required) |
| Requests | **359 GET, 0 non-GET**, 250 content-addressed bodies, 71.4 MB uncompressed, 487.3 s wall clock |
| Admitted items | 32 (19 discovered, 13 declared controls); **29 classified, 3 unclassifiable** |
| Sites with ≥1 classified item | 5 (frozen floor: ≥20 items and ≥4 sites — **met**) |
| Substrate | stdlib HTTP, GET only, no browser, no Docker, no credentials, no model key |
| Tokenizer | `cl100k_base` via tiktoken 0.14.0 (**not** declared in `pyproject.toml` — see VN-11) |

Everything admitted sits at **crawl hop 0 (14 items) or hop 1 (5 items)**; the 13 declared controls
have no hop by construction. This is the extreme-favourable case for handle persistence (VN-18).

---

## 3. Layer 1 — RAW EVIDENCE (durable, hashed)

| Artifact | SHA256 (prefix) | Content |
|---|---|---|
| `raw/http.jsonl` | `290dfb18` | 359 request/response records with status, headers, redirects, token cost |
| `raw/observations.jsonl` | `63029c85` | 320 per-item/per-session extraction records |
| `raw/session_timing.jsonl` | `5390fba2` | 24 inter-session delay measurements |
| `raw/controls_verification.jsonl` | `95db345d` | live per-item, per-control verdicts |
| `raw/responses_cache/` | 250 files | `<sha256-of-uncompressed-body>.json.gz`; the name is the verification handle (VN-12) |
| `derived/items.json` | `0c789a8d` | admitted items, sessions, cold crawl, implementation choices IC-01…IC-10 |
| `derived/classification.json` | `129e5512` | per-item class with the frozen rule that matched |
| `derived/classification_sensitivity.json` | `a32227db` | disclosed ambiguity variants |
| `derived/costs.json` | `3664efe5` | per-item re-acquisition / re-derivation / break-even |
| `derived/analysis.json` | `21209fbf` | aggregate metrics, controls, CI, falsifier, attainability audit |
| `derived/run_manifest.json` | `0645e8c4` | execution manifest |

Frozen inputs were re-hashed at emit time and match `freeze.json` exactly. No frozen file was
written by any code path in this lane.

---

## 4. Layer 2 — OBSERVATIONS (what was seen; `result.json observations`)

`OBS-01`…`OBS-17`, all of which are reproduced in `result.json observations`:

- **OBS-01 / OBS-02** — 359 GETs, 0 non-GETs; K=5 disjoint cookie jars; minimum inter-session
  delay 93.81 s over 24 timing records. The measurement substrate was available and behaved
  as frozen.
- **OBS-03** — 29 of 32 admitted items received a class: 12 `session_invariant`, 17
  `request_scoped`, 0 `session_scoped`, 0 `time_scoped`, 0 `rotating`.
- **OBS-04** — Both server-minted CSRF handles behaved worse than the parent packet reported:
  5 distinct values across 5 sessions **and** 5 distinct values across 5 GETs inside a single
  session (`https://auth.wikimedia.org/…/Special:CreateAccount`,
  `https://gitlab.com/-/trial_registrations/new/`).
- **OBS-05** — The null arm fired: `httpbin.org/uuid` gave 5 distinct values across sessions and
  5 within one session; `httpbin.org/headers` `X-Request-Id` reported its explicit `prng` fallback
  every session and gave 5 distinct values.
- **OBS-06 / OBS-07 / OBS-14** — Live drift, recorded not repaired: the prereg-named control anchor
  `https://gitlab.com/users/sign_in` returns **HTTP 403** credential-free;
  `httpbin.org/sitemap.xml` returns **404** (OBS-07, excluded by the frozen conditional);
  `https://gitlab.com/explore` does not exist on the page
  `gitlab.com` actually serves (it redirects to `about.gitlab.com`, which has no `/explore`).
- **OBS-08 / OBS-09** — 4 of 6 frozen roots redirect off their nominal host (`gitlab.com`→`about.gitlab.com`,
  `auth.wikimedia.org`→`www.wikimedia.org`, `en.wikipedia.org`→`/wiki/Main_Page`,
  `postman-echo.com`→`www.postman.com/…`). `wikimedia` and `postman_echo` admitted 0 items under the
  frozen host-pinned crawl. **"Site" is not a stable unit on this substrate.**
- **OBS-10** — Every one of the 12 `session_invariant` items has re-acquisition cost *exactly equal*
  to re-derivation cost (1 request, identical token count).
- **OBS-11** — Depth-1 wikipedia items: re-acquisition 2 requests / ~93k tokens vs re-derivation
  15–26 requests / 0.97–1.50M tokens. Root-hosted bitbucket items: re-acquisition and re-derivation
  are the *same single GET* differing by ~13 tokens, and the frozen formula returns break-even
  counts spanning **1 to 34,299** for economically identical items (VN-08).
- **OBS-12 / OBS-14** — Under the value-only channel the distribution moves to 12 / 5 with 12 of 29
  items unmatched; and the frozen `KNOWN_STATIONARY_CONTROL` anchor for `gitlab/explore` was
  unobservable in all 5 sessions because the page `gitlab.com` actually serves has no such link.
- **OBS-15** — The `KNOWN_STATIONARY_CONTROL` anchor `https://en.wikipedia.org/wiki/Main_Page`
  (the site self-link) had 1 distinct value across 5 sessions but 5 distinct page body hashes,
  so the frozen rule classified it `request_scoped`.
- **OBS-16 / OBS-17** — The class-level break-even numbers are computed over mismatched
  denominators (VN-19), and among the 20 items where both costs are measurable, re-derivation ≥
  re-acquisition on both units for **20 of 20**.

---

## 5. Layer 3 — DERIVED MEASUREMENTS (`result.json metrics`)

### `class_distribution` (denominator = 29 classified items)

| Class | Count | Proportion | CI95 (site-clustered, 10k, seed `37385647440`) |
|---|---:|---:|---|
| `session_invariant` | 12 | 0.414 | 0.045 – 0.759 |
| `session_scoped` | **0** | 0.000 | 0.000 – 0.000 |
| `request_scoped` | 17 | 0.586 | 0.241 – 0.955 |
| `time_scoped` | **0** | 0.000 | 0.000 – 0.000 |
| `rotating` | **0** | 0.000 | 0.000 – 0.000 |

The CIs are degenerate: every class is perfectly separated at site level, so resampling sites
collapses to the two extreme proportions (VN-09). They are reported for contract compliance and
carry no useful precision.

Three of these five numbers are **0 by construction, not by observation** (VN-05): the frozen rule
order tests `session_scoped` before `time_scoped` and `rotating`, so both are unreachable for any
item whose value changes within a session — which is most of them.

### `value_only_sensitivity` (IC-01 disclosure)

| Class | Primary (value + page hash) | Value-only |
|---|---:|---:|
| `session_invariant` | 12 | 12 |
| `request_scoped` | **17** | **5** |

12 of 29 classified items are unmatched by the frozen value-only table. The choice of channel is
decision-relevant, not cosmetic (VN-06).

### `break_even_reuse_count_per_class` (baseline `COLD_REEXPLORATION`)

| Class | n | median re-acq (tok) | median re-deriv (tok) | class break-even | median item-level break-even | denominators match |
|---|---:|---:|---:|---:|---:|:--:|
| `session_invariant` | 12 | 37,357 (CI 113–71,673) / 1 req | 71,673 / 1 req | 2 | **infinite** | ❌ 12 vs 7 |
| `session_scoped` | 0 | — | — | `null` | `null` | — |
| `request_scoped` | 17 | 93,986 (CI 224–445,881) / 1 req | 445,894 / 1 req | 1 | 1,256 | ❌ 17 vs 13 |
| `time_scoped` | 0 | — | — | `null` | `null` | — |
| `rotating` | 0 | — | — | `null` | `null` | — |

Read the **item-level** column. At item level the entire `session_invariant` class has infinite
break-even: re-acquiring a byte-stable object costs exactly what re-deriving it costs. The class
number `2` is an artifact of comparing a 12-item re-acquisition median against a 7-item
re-derivation median whose 5 missing items are the cheap static files (VN-19, OBS-16).

`ORACLE_PERFECT_TRANSFER` is **not available for 29 of 29** items (0 items have re-acquisition
strictly below re-derivation). `RETRIEVAL_BASELINE` was **not exercised** (no prior episodes) and is
recorded as `null`, as frozen.

### `falsifier_triggered`

`false`. `majority_non_stationary = true` (17 non-stationary vs 12 stationary, majority class
`request_scoped`); `cost_condition = false`. **Both conditions were required**, and the second was
unreachable: for every reachable item the breadth-first re-derivation route is itself a shortest
path and sums a superset of the same responses, so `re_derivation ≥ re_acquisition` on both units
holds by construction, confirmed empirically at 20/20 (OBS-17).

### `controls_pass`

`false`.

| Control | Verdict | Designated items | Pass / Fail / Unobservable |
|---|---|---:|---|
| `KNOWN_STATIONARY_CONTROL` | **FAIL** | 6 | 3 / 1 / 1 |
| `REVERIFIED_NON_STATIONARY` | **FAIL** | 2 (+1 information-only) | 0 / 1 / 1 |
| `INTER_SESSION_DELAY` | PASS | 1 | 1 / 0 / 0 |
| `NULL_STATIONARITY_ARM` | PASS | 4 | 2 / 1 / 1 |
| `PRE_FREEZE_CONTROL_VERIFICATION_GATE` | **FAIL** (process finding, outside the four-count) | 4 | all `PENDING` at freeze |

The `NULL_STATIONARITY_ARM` passes on its own frozen criterion ("at least one non-stationary
classification on known-non-stationary probes"), and it passes the informative way: it fired on both
of its real non-stationary probes. Its `NOT_FIRED` item is the randomising `robots.txt?cache_buster`
probe, which is byte-stable by design — a correct classifier outcome, not a null-arm failure. Its
`/date` probe is unobservable (HTTP 404).

---

## 6. Layer 4 — INTERPRETATION (bounded, at the ceiling stated in `result.json`)

This transaction supports **no claim update**. Three statements are admissible, and only these:

1. **On this substrate, the objects a persistent agent would replay across episodes are dominated by
   objects that are already stale inside a single episode.** Both CSRF handles and both httpbin
   nonces changed five times in five GETs issued seconds apart *within one session*. Whatever these
   objects are, they are not safely replayable even within an episode, let alone across episodes.
   This sharpens, and does not reverse, the inherited parent conclusion that persistence over this
   object class can only amortize a procedure, never a stored handle.

2. **The class of objects that *is* byte-stable across episodes carries no amortization surface at
   all.** All 12 `session_invariant` items have re-acquisition exactly equal to re-derivation:
   re-acquiring a stable object costs precisely what re-deriving it costs, so its break-even reuse
   count is infinite. There is no number of reuses at which persisting it pays.

3. **The instrument was not in a state to decide the question.** The frozen taxonomy's middle class
   (`session_scoped`) has 0 members and is unreachable in two of its five classes by rule order; the
   primary classification channel (whole-page hash) moves 12 of 29 items relative to the value-only
   channel; the falsifier cannot trigger; and the break-even formula is ill-conditioned and
   denominator-mismatched. The frozen design would have produced a confident number even while being
   structurally incapable of falsifying its own hypothesis.

**Claim ceiling:** these are substrate observations and an instrument-validity finding, not a
validated stationarity taxonomy, not a Web prevalence estimate, and not a mechanism claim about
`request_scoped`.

---

## 7. Why the branch is `MEASUREMENT_INVALID`

`spec.json decision_rule.controls_gate` states: *"All four pre-freeze controls must PASS. If any
control FAILS, the experiment status is MEASUREMENT_INVALID regardless of classification results."*
Two failed. The frozen `outcome_mapping` for `CONTROLS_FAIL` is
`status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE`. The emitter asserts this branch was the one
selected; it cannot silently choose another.

This is **not** a scientific negative. Recording it as one would convert a broken instrument into a
claim about the world.

### Frozen design defects found (all pre-existing; none introduced or repaired here)

| ID | Defect | Consequence for the next design |
|---|---|---|
| VN-07 | Falsifier's cost condition is unsatisfiable by construction | A falsifiable version needs a re-derivation baseline that is *strictly* more expensive by construction — e.g. an adversarial full-site crawl with no path memory, or a cost model charging for re-deriving the whole procedure rather than re-walking a known shortest path. |
| VN-05 | Rule order tests `session_scoped` before `time_scoped`/`rotating` | Two of five classes are unreachable. Order must be: invariant → within-session-varying → then time/rotating, with a declared sampling schedule to separate them. |
| VN-06 | Primary rule hashes the whole containing page | `request_scoped` becomes a near-catch-all; 12 of 29 items depend on this choice. The channel must be declared per item as an explicit hypothesis, not left ambiguous (IC-01). |
| VN-04 | `REVERIFIED_NON_STATIONARY` accept list excludes `request_scoped` | Both observable anchors fell into `request_scoped` — demonstrating non-stationarity *more* strongly than the control anticipated — and were still rejected. The control could only ever fail. |
| VN-03 | `KNOWN_STATIONARY_CONTROL` designates 5 anchors; 2 do not exist on the live web and a 3rd is not stationary | A "known stationary" calibration class with 1 genuinely stationary anchor cannot calibrate a 5-class taxonomy. |
| VN-08/19 | Break-even formula is ill-conditioned and compares medians over different item sets | Guard the denominator and require `re_derivation − re_acquisition` to exceed a materiality threshold before reporting a break-even. |
| VN-02 | All four `controls_pre_freeze_verification` entries were `PENDING` when `freeze.json` existed | Violates prereg §7 and §14. The design was frozen unvalidated; this is the root cause of shipping an instrument that could not decide the question. |

---

## 8. Validity threats and representation loss

- **VN-01 (decisive).** Two of four controls failed; per the frozen `controls_gate` this alone
  fixes the status at `MEASUREMENT_INVALID`. Nothing in sections 5-6 may be read as a validated
  scientific answer.
- **Substrate drift** (VN-10) is not a producer defect, but it bounds what this pool can say: the
  prereg-named GitLab control anchor returns HTTP 403 credential-free, the prereg-named httpbin
  sitemap anchor returns 404, and 4 of 6 roots redirect off their nominal host — so **"site" is not a
  stable unit here**, and the drift was recorded rather than repaired.
- **Representation loss.** The pool is 32 hand-picked items on 6 sites, discovered only from
  root-page links and form inputs. `wikimedia` and `postman_echo` contributed nothing. This is a
  sample of a hand-picked credential-free pool, **not Web prevalence** (frozen `target_pool`).
- **Live-web measurement.** Not byte-reproducible; re-running produces a new measurement. Only the
  input hashes, code hashes and shipped artifacts reproduce exactly.
- **Two discarded passes** (VN-13): a relative-`href` matching bug, and an item-identity collision
  that silently dropped the prereg-named GitLab anchor's observations. Both defects are recorded in
  the shipped executor as IC-09/IC-10; both passes and their evidence were deleted. Only the shipped
  pass is authoritative.
- **Marginal stability** (VN-14): in one discarded pass ~20 minutes earlier the GitLab favicon was
  byte-unstable and classified `request_scoped`; in the shipped pass it was byte-stable. The
  designated "known stationary" asset class is therefore not robust at the scale of minutes. The
  discarded evidence is not retained, so this is unreplicated and informational.
- **Undeclared tokenizer** (VN-11): tiktoken is environment-provisioned, not declared, so this run
  does **not** claim a pure-stdlib substrate as `spec.measurement_validity.substrate` requires.
  Frontier may not edit `pyproject.toml`.
- **Storage deviation** (VN-12): gzip-wrapped content-addressed bodies.
- **Unclassifiable items** (VN-17): 3 of 32 (gitlab `/explore` anchor absent, GitLab `/users/sign_in`
  HTTP 403, httpbin `/date` HTTP 404) are excluded from the class denominator and reported
  separately rather than forced into a class.
- **Lineage** (VN-15 / VN-16): `request.json base_sha` `0a3b7f96…` is an ancestor of execution HEAD
  `0b89abe4…`; the two executor files are untracked. The `director_mandate` names predecessor
  `EXP-FRONTIER-36314209725`, which failed on installation; this packet is the reallocated CONTINUE
  transaction and answers that mandate's question.
- **11 of 32 items were never reached** by the frozen crawl, so their re-derivation cost is
  genuinely unmeasured and reported as `null`, never imputed (OBS-13, UR-06).

---

## 9. Consequences of each branch — none was reachable, and that is the finding

| Branch | Would have meant | Actually happened |
|---|---|---|
| `CONTROLS_FAIL` | no admissible scientific answer | **taken** |
| `FALSIFIER_TRIGGERED` | bounded negative for HANDLE PERSISTENCE on this substrate | **unreachable by construction** (VN-07): would have been an artifact of instrument definition, not of the web |
| `FALSIFIER_NOT_TRIGGERED` | stationarity distribution measurable and a finite break-even exists for ≥1 class | **unreachable**: unreachable by the same argument, and the class-level finite break-even that would have satisfied it (2 reuses for `session_invariant`) is a denominator artifact (VN-19) |

Had the controls passed and the rule been sound, the branch reached here would still have been
`SUPPORTS`-shaped, and the honest reading of the numbers would have been the *negative* one —
observation 2 above — rather than the finite-break-even one. That inversion is the practical
argument for re-freezing with a falsifiable rule before this question is asked again.

---

## 10. What this does **not** establish

- That `session_scoped` does not exist on this substrate. It has 0 members here, but the frozen rule's
  page-hash channel can mask it (UR-01).
- That the observed proportions describe the Web. They describe 32 hand-picked items (UR-02).
- That no item is `time_scoped` or `rotating`. Both classes are unreachable under the frozen rule
  order (UR-03).
- That the 3 unclassifiable items would classify on a browser or credential-bearing substrate. Drift
  was recorded, not repaired, and a parent-cited URL was never substituted for a prereg-named anchor
  (UR-04).
- That cross-episode persistence is worthless in general. The bound is: on **credential-free,
  GET-only, stdlib-HTTP** substrates, for **this object class**. It says nothing about authenticated
  sessions, browser-mediated flows, or write verbs.
- Any promotion. Nothing here is `VALIDATED`, `PRODUCT_CORE` or `SHIPPED`, and this report does not
  attempt it.

## 11. Smallest next actions (from `result.json unresolved`)

1. **Re-freeze with a satisfiable falsifier** (UR-05) — a baseline structurally more expensive than
   re-acquisition, with a materiality guard on the break-even denominator.
2. **Fix rule order and declare the channel per item** (UR-02, UR-03) so `time_scoped`/`rotating`
   are reachable and the value-vs-page-hash choice stops moving 12 of 29 items.
3. **Re-specify the two broken controls against anchors that exist** (UR-07), with an accept list
   that includes `request_scoped`.
4. **Verify controls before freeze** (VN-02) — this is the single highest-value process repair, and
   the one whose absence caused every other problem here.
5. **Measure at real depth** (UNRESOLVED/UR-06 + VN-18): every admitted item was at hop ≤1, the
   friendliest possible case for persistence.

## 12. Reproduction

```bash
python3 -m py_compile research/frontier/stationarity_37385647440.py \
                      research/frontier/analyze_stationarity_37385647440.py \
                      research/frontier/emit_result_37385647440.py
python3 research/frontier/stationarity_37385647440.py    # live GET-only pass (~490 s)
python3 research/frontier/analyze_stationarity_37385647440.py   # offline, deterministic
python3 research/frontier/emit_result_37385647440.py           # offline, deterministic
```

The emitter re-hashes every frozen input and asserts they match `freeze.json`; it also asserts that
the branch it selected is the branch the frozen `outcome_mapping` assigns, so it cannot quietly
report a different outcome. Only the analyzer and emitter are bit-deterministic; the executor is not.

No git commit, push, branch or reset operation was performed. Paths touched are limited to
`research/frontier/` (three new scripts) and
`research/experiments/EXP-FRONTIER-37385647440/{raw,derived}/`.