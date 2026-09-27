# EXP-GRAPH-36302977302 — Preregistration (DESIGN frozen pre-outcome)

**Lane:** graph
**Claim:** C-FRESHNESS — "SPIDER can detect when inherited knowledge is stale"
(registry status `HYPOTHESIS`, `research/claims/registry.json`; `next_gate`: session/token/DOM/endpoint/permission drift with false-accept measurement). Registry sha256 recorded in `request.json` as `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b`.
**Experiment ID:** EXP-GRAPH-36302977302
**Director mandate:** `PIVOT`, `claim_id=C-FRESHNESS`, `parent_handoff_disposition=SUPERSEDE`, `cognitive_reset=true` (`request.json:director_mandate`). Binding direction per AGENTS.md precedence and `research/EXPERIMENT_PACKET.md` §2. The inherited `parent_handoff` is continuity evidence only; its `next_question` (a fifth C-SEMANTIC-RESOLVE pass on contamination-free goal authoring) is **not** pursued, because the mandate explicitly PARKED C-SEMANTIC-RESOLVE pending a control-plane fix and refused a fourth pass in the same shape.
**Parent handoff (read, not followed):** `research/experiments/EXP-GRAPH-36287167610/handoff.json`, sha256 `ccb69760b5bbe9ba4ee8873affb7b046d7a4066da96be491e29bd9cd5545640a`, as cited in `request.json.parent_handoff`. Its four-way distinction is preserved verbatim in §3 below.
**Design status:** frozen pre-outcome. No outcome-bearing measurement was taken, inspected or simulated during DESIGN. The only environment facts recorded in §4.2 are pre-execution substrate feasibility probes (module imports and binary presence), which are not outcome measurements and are not used as evidence for any claim.

---

## 1. Director strategic question → the smallest falsifiable question

**Director question (verbatim, `request.json:director_mandate.question`):**

> On Runtime's already-certified distributed shared-WAL plain-HTTP substrate (stable-header representation, HMAC-SHA256 per auth_state, real If-None-Match/ETag 304, verified X-Worker-Pid spread) and, only where Runtime's capability ledger certifies it, the public-API Chromium DOM/AX path: does SPIDER's response-derived freshness guard detect stale inherited knowledge at the preregistered operating point across a full drift matrix of session/token rotation, endpoint parameter and header mutation, permission-boundary change, and conditional-request revalidation, at true-negative rate >= 0.85 with Wilson lower > 0.75, false-accept <= 0.10, UNKNOWN precision >= 0.85, and global and per-class ECE <= 0.15 with bootstrap upper <= 0.18, against no-guard and single-signal baselines, at a stale prevalence and sample size preregistered to give the estimator power and declared non-degenerate intervals; and, scored as its own arm rather than folded into the guard, does a fresh no-memory re-derivation of the same object avoid stale-accept risk entirely at a measured re-derivation cost, so that the guard's value is established exactly where inheritance has something to protect rather than assumed?

**Refinement into the smallest test that can still change a decision.** The mandate is one sentence containing two separable claims and one substrate clause. This prereg keeps all three and separates what must be decided from what need not be:

1. **Safety claim (gated).** Does the guard detect stale inherited knowledge on the four mandated families at the mandated operating point? This is a *conjunction* of TN, FA, UNKNOWN precision, calibration and selectivity, and it is the only part that can move C-FRESHNESS.
2. **Economic claim (gated, separable).** Is the guard admissible at all, given that a memoryless re-derivation exists and its cost is measurable? This is scored as **its own arm** and reduced to a single comparison: the guard path costs `1 + u·R` requests per reuse, the re-derivation path costs `R`, so the guard is admissible iff `u <= u* = (R-1)/R`. Both `u` and `R` are measured. This is the only way to honour the mandate's "scored as its own arm rather than folded into the guard" without falling into the trap of scoring re-derivation's stale-accept rate as a measured 0.0 — see §2, Arm B.
3. **Substrate clause (scoped, with the substitution made explicit).** The mandated substrate properties are the distributed shared-WAL plain-HTTP certificate. Two of the mandate's own dependencies are **not landed** (§2.3), so the design engages the substrate clause by reproducing its *certified properties as executed health-gate floors* in a graph-authored stdlib substrate, and by declining to inherit Runtime's per-packet fixture, which Runtime's own handoff forbids. The deviation is declared, not hidden.

**What is deliberately excluded.** No browser arm (§2.3). No LLM, no real agent, no token economics. No real public website. No cross-site transfer. No `dom_drift` family by that name, because there is no DOM on this substrate (§12, V12). No repair, no patching, no contamination measurement — C-DELTA-REPAIR is the Director's next cycle and running two unmeasured instruments in one packet is exactly what the mandate warned against.

---

## 2. Hypothesis

### 2.1 H1 (positive, bounded)

On the graph-authored distributed shared-WAL plain-HTTP substrate defined in §4, at the frozen drift matrix of §6, with no fitted parameter anywhere (§5, V5):

- **(a) Safety.** `A-CANDIDATE` reaches pooled `M-TN-SPIDER >= 0.85` with `M-TN-WILSON-LOWER > 0.75` (n_fresh = 720); `M-FA-SPIDER <= 0.10` with `M-FA-WILSON-UPPER < 0.1525` (n_stale = 180); `M-UNKNOWN-PRECISION-SPIDER >= 0.85` (n_unknown = 204 at the feasibility boundary); `M-ECE-GLOBAL <= 0.15` and `M-ECE-FRESH <= 0.15` and `M-ECE-STALE <= 0.15` with `M-ECE-BOOTSTRAP-UPPER-975 <= 0.18`, over at least three realized confidence levels; selectivity `M-UNKNOWN-RATE-PATIENT` in (0.15, 0.85]; and per-family FA Wilson upper < 0.20 for every reached family.
- **(b) Economics.** Measured abstention `u = M-UNKNOWN-RATE-PATIENT` satisfies `u <= U-BREAKEVEN = (R-1)/R` where `R = M-REDERIVE-PATH-REQUESTS` is the measured per-item request count of the re-derivation arm, so the guard path `1 + u·R` is at or below the re-derivation path `R`, on all three measured cost bases (requests, wire bytes, wall-clock ms).
- **(c) Incremental value.** `M-FA-B-NO-GUARD-REPLAY - M-FA-A-CANDIDATE >= 0.15`, and the incumbent `B-INCUMBENT-GUARD` is strictly worse than the candidate on at least one mandated family, and at least three of four single-channel ablations are decision-distinct from the candidate.

### 2.2 H0 (bounded negative, and the two halves are deliberately separable)

With GATE 0 (all validity and control gates) fully passed:

- **Safety falsified in setting** if any of F1–F6, F8, F9 fires: the guard misses stale inherited knowledge at a bounded false-accept rate, or abstains non-selectively, or the incumbent signal set already carries all the value.
- **Economics falsified in setting** if F7 alone fires: the guard is safe enough but `1 + u·R > R` on the measured cost basis, so it is a pure cost. Coded `outcome=MIXED`, `decision=FALSIFIES_ECONOMIC_ONLY`, with the safety evidence explicitly preserved and explicitly *not* withdrawn. The packet is built so that these two cannot be conflated — this is the single most important structural choice in the design, because the parent thread's most decision-relevant quantity (the deferral policy's cost) was absent from `result.json`, `report.md` and the derived evidence, and had to be recomputed by the auditor and again by the Director.

A safety falsification is a valid negative **at this operating point on this substrate with this signal set**. It does not close the C-FRESHNESS domain, does not authorise retiring the mechanism, and does not downgrade the claim below its current registry ceiling.

### 2.3 Arm B, and why its stale-accept rate is `null` and not `0.0`

`B-FRESH-REDERIVE` runs with an **empty registry**: it holds no inherited mechanism, so there is no inherited knowledge that could be accepted stale. Reporting that as a measured `M-REDERIVE-STALE-ACCEPT = 0.0` would be a control that cannot fail — precisely the defect class the Director's portfolio assessment and the parent handoff both name, and the class that made `unknown_precision = 1.0` in `EXP-GRAPH-36287167610` an artifact of inertness. The packet therefore records:

- `M-REDERIVE-STALE-ACCEPT` = **`null`**, with `validity_notes` stating: structural property of an empty registry, not a measurement, not a measured zero.
- The **measured** quantities for Arm B are `M-REDERIVE-SUCCESS` (does it obtain the post-drift object?), `M-REDERIVE-PATH-REQUESTS`, `M-REDERIVE-PATH-WIRE-BYTES`, `M-REDERIVE-PATH-WALLCLOCK-MS`, and `M-COLD-PATH-*` for the full-discovery reference. Every one of these **can fail**. If re-derivation cannot reconstruct the post-drift object on a family at a success rate the guard path also cannot reach, that is a real negative for both arms and is reported as such.

**Dependency honesty (V15).** Two mandated dependencies are unmet and are handled by declared scope exclusion with an exact smallest next action each. Neither is substituted.

1. **Runtime's authorship/transport generalization of the intervention oracle did not land.** `EXP-RUNTIME-36293257855` is absent from `codex/index.json`, absent from `research/experiments/` on this branch, and closed at execute with `failure.json`: `stage=execute`, `category=EXECUTION_FAILURE`, `message="stage exited with code 76"`, `retryable=false`, `fingerprint=32fb61131a26107aaf831564`, `github_run_id=36293257855`. Its frozen question was precisely to break the *authorship* and *transport* confounds of the intervention oracle, on the browser path. **Consequence for this design:** the confound is broken *locally and by executed construction* instead of being inherited as a result — separate injector and detector modules, arm-blind scoring with a written-then-hashed ordering, and machine-checked non-violation that aborts the packet (§5, V3, V4, NC-AUTHORSHIP-SEPARATION, NC-ARM-BLIND-SCORE-ORDER). The claim ceiling is bounded to exactly the bound Runtime itself used: *"the validated object is a measurement instrument tested against a planted surface."* Here the planted surface is graph-authored, and that is disclosed, not inherited.
2. **The public-API Chromium DOM/AX path is not intervention-valid, so no browser arm is engaged.** In the certified ledger `research/experiments/EXP-RUNTIME-36129163700/artifacts/capability_ledger.json` (source_ref `origin/lab2/runtime`, source_ref_head `e685fb1eea8d506cafb1c2afdeff746ce9e41e52`, `verdict.json` sha256 `ea5f80f07442ef6b510f0b3d1814a5032d7b53947098b3f704d8f3186791579e`), `CAP-CHROMIUM-LAUNCH` is `AVAILABLE` but the `browser_B` scope is, in Runtime's own words, *"satisfied as a launch fact and unsatisfied as an intervention-validity fact"*: the in-process SPA write click executed but the exception fired before `artifacts/B-WAL-EVIDENCE.jsonl` was written, so **no durable before/after WAL record of a browser-mediated write exists**. The mandate's own condition was *"only where Runtime's capability ledger certifies it."* It does not.
   **Smallest next action (exact):** the Global Research Director re-allocates to Runtime a bounded experiment re-running the frozen `EXP-RUNTIME-36293257855` design, and publishes a ledger component `CAP-CHROMIUM-BROWSER-WRITE` with a durable `B-WAL-EVIDENCE` artifact; until that component exists, **no** lane may preregister a browser-mediated staleness or revalidation arm, and this packet's claim ceiling is not extended to any transport other than plain HTTP. **No substitute transport is used in this packet.**
3. **Runtime's per-packet substrate is not inheritable, by Runtime's own instruction.** `EXP-RUNTIME-36129163700/handoff.json` `do_not_assume`: *"Do not treat the three 'certified substrate' packets as replications of one component, and do not design a downstream lane to inherit the app, routes, schema, auth boundary or detector from them. Each packet re-authors them inside its own run_experiment.py; the substrate is a per-packet fixture that must be rebuilt or extracted before anyone can preregister against it."* Accordingly the substrate in §4 is **graph-authored and stdlib-only**, and it is bound by executed health-gate floors rather than by inheritance. It is explicitly **not** a replication of `C-MEAS-VALID` and may not be cited as one.
   **Smallest next action (exact):** Runtime publishes `research/runtime/` as a durable, ledger-certified substrate component on `main` with a versioned contract; until then, every lane re-authors its own substrate and every cross-lane claim is bounded to its own instance.
4. **No model credential.** `CAP-POLICY-MODEL-CREDENTIAL` is `UNAVAILABLE` in the certified ledger. Consequence: no LLM, no token economics, and §12/V8 requires the cost basis to be measured requests, wire bytes and wall clock — never tokens. Smallest next action: configure the policy-model credential env key, then re-probe the ledger.

---

## 3. Preservation of the parent handoff's four-way distinction

`EXP-GRAPH-36287167610/handoff.json` (sha256 `ccb69760…`), preserved as continuity evidence per AGENTS.md and `research/EXPERIMENT_PACKET.md` §2. Its `next_question` is **not** this packet's mandate.

**Established (preserved, not re-tested, not weakened):**
- `EXP-GRAPH-36287167610` is a valid `MEASUREMENT_INVALID` over-determined outcome; `C-SEMANTIC-RESOLVE` stays at `HYPOTHESIS`; nothing about that thread is retired.
- `EXP-GRAPH-36287167610/V9-CODE-BOUND-VIA-PREREG` — namespaced by its own experiment id, because this packet's own `V9` is `V9-PREVALENCE-AND-POWER`, a different condition, and the two must never be conflated — is unsatisfiable in **every** lane because `scripts/freeze_experiment.py` writes exactly three sha256 keys and `scripts/check_scope.py:124-127` gives stage `design` `prefixes=[]` with `exact={spec.json, prereg.md, failure.json, model_design.json}`. **This packet therefore contains no code-digest gate at all** (V14) and substitutes an executed health gate (V1). The third of three consecutive Graph measurement-invalid packets in that thread was lost to a false `V9 PASS` attested over a literal `[FILLED_AT_FREEZE]` placeholder, so *this packet must never emit a PASS for a check it did not compute.*
- A reference arm algebraically identical to the candidate tests no gate (`argmax_i sigma(w·cos_i + b) = argmax_i cos_i`, mechanism_id identical on 52/52). **This packet computes ablation distinctness** (V11, NC-ABLATION-DECISION-DISTINCTNESS) rather than asserting it.
- A positive control that cannot fail, a null control that cannot be satisfied, and an ECE target unattainable under the frozen parameterisation are all pre-registered defect classes. **This packet's PC, NC and ECE are each constructed to be able to fail, and §10 carries the attainability arithmetic.**
- 8 of 13 validity conditions in that packet were code literals assigned `True`. **Every condition in this packet is computed at execute time or is not stated** (§5, V1–V15).

**Rejected (must not be cited as support, in either direction):**
- That `C-SEMANTIC-RESOLVE` is falsified, closed, retired, or downgraded to `MEASUREMENT_INVALID` as a claim state.
- `0.9286 / 0.8654 / 0.8333 / 0.8261` as "semantic resolution accuracy" without a named denominator.
- The parent's paraphrase figures `"19/20 vs 15/20"` — they belong to `EXP-GRAPH-36279237023` and were hard-coded into that packet; do not import them.
- `provenance.json` digests, the `'local-execution'` run id, and the "two independent executions produced byte-identical evidence" note from that packet.
- Any future design in the shape of a fourth C-SEMANTIC-RESOLVE pass.

**Unknown (inherited, still open, and not this packet's business):**
- Whether the joint selection-and-safety problem is feasible at all on a self-authored bound-slot fixture class; whether learned abstention can be calibrated; whether the C-SEMANTIC-RESOLVE thread's paradigm is exhausted; whether the control plane will ever provide a satisfiable code-binding mechanism; who deleted `failure.json` from that packet; and whether the parent and grandparent paraphrase numbers can both be right.
- These are carried, unresolved, into whoever next writes a `handoff.json` for that thread. **This packet must not import them as if it had re-measured them.**

**Do not assume (preserved, and binding on this packet's readers):**
- Do not read a `MEASUREMENT_INVALID` at GATE 0 as a scientific negative about `C-FRESHNESS`, and do not encode it as one.
- Do not read the fact that three prior graph packets closed `COMPLETE/SUPPORTS` with `audit=PASS` as evidence that the guard generalises: those three built their drift families **out of the guard's own features** (required-filtered Jaccard, server-signaled template, `ETag` + `max-age`), so their positives and their tautology risk are entangled and cannot be separated by re-analysis. `EXP-GRAPH-36018188168` is a `C-DELTA-REPAIR` packet whose own audit recorded ECE as *"satisfiable by construction"* and noise immunity as passable by construction.
- Do not assume the three `EXP-RUNTIME` "certified substrate" packets replicate one component. They do not; each re-authors its own fixture.
- Do not treat `result.json controls.V-SUBSTRATE-CERTIFICATE pass=false` in `EXP-RUNTIME-36129163700` as a failed gate — it is a reporting bug; the raw certificate says `pass=true`.
- Do not read `EXP-RUNTIME-36129163700`'s `C-MEAS-VALID=VALIDATED` as validating any shared component or any downstream lane's measurement surface.
- Do not treat a deleted bootstrap interval of width 0 as high precision, and do not accept a control as discriminating merely because it reports `pass`.

---

## 4. State representation

### 4.1 Substrate (graph-authored, stdlib-only, distributed, shared-WAL, plain HTTP)

| Component | Frozen specification |
|---|---|
| Workers | 3 separate OS processes, each an independent `http.server` instance on `127.0.0.1:19870/19871/19872` |
| Shared store | one SQLite database at `/tmp/spider-graph-36302977302/shared.db`, `PRAGMA journal_mode=WAL`, `PRAGMA wal_autocheckpoint=0`; tables `resources`, `sessions`, `grants`, `injection_ledger` |
| Proxy | one stdlib round-robin reverse proxy on `127.0.0.1:19860`, preserving method, path, query, headers and body, so that `X-Worker-Pid` genuinely varies across requests |
| Representation | stable-header JSON; every response carries `X-Worker-Pid`, `X-Upstream-Port`, `ETag: "<16 hex>"`, `Cache-Control` |
| Auth | `Authorization: Bearer <session_token>`; the server recomputes `HMAC-SHA256(canonical_json(auth_state), key)` on **every** request and compares in constant time; `auth_state = {session_id, principal, scopes[], issued_at, epoch}` |
| Permission | `resources.required_scope` must be in the verified `auth_state.scopes`, else `403` with an error envelope whose field-path/type token set is **identical** to the `200` body, and error responses carry no `ETag` |
| Conditional requests | real `If-None-Match`: a matching validator on a cacheable resource returns a genuine `304` with no body |
| Endpoints | `GET /health`, `GET /api/resource/{id}`, `GET /api/resource/{id}/detail?detail=1`, `GET /api/permission/{id}` (scope `read:perm`) |
| Mechanism | `src/spider/kernel.py` is used as-is: `resolve()` for applicability, `verify()`/`_matches()` for deterministic postcondition verification. No product-kernel change is in scope for the graph lane (`allowed_code_roots = ["research/harness", "research/graph"]`) |

**No pip install, no browser, no docker, no model key, no external network.** The substrate is stdlib-only by design: this program has repeatedly lost packets to provisioning failure, and every dependency removed is a provisioning failure removed.

### 4.2 Pre-execution substrate feasibility (recorded, not evidence)

Recorded at DESIGN time in the author's sandbox, to be re-verified authoritatively by the V1 health gate at EXECUTE: `nginx`, `sqlite3` binaries present; `flask`, `jwt`, `gunicorn`, `requests`, `playwright`, `numpy`, `scipy` **absent** in this sandbox. This is precisely why §4.1 is stdlib-only: the substrate must not depend on packages the lane workflow does not install (`.github/workflows/spider-lane.yml` has no `pip install` step). The V1 health gate, not this note, is the authority; if the health gate fails the packet is `BLOCKED`/`MEASUREMENT_INVALID` with the smallest next action, never falsified.

### 4.3 Derived guard state — the four channels

Per item, the guard issues **one** revalidation request: a conditional `GET` with `If-None-Match: <cached ETag>` when an ETag is cached, otherwise an unconditional `GET`. From that single exchange, and from nothing else:

- `stale_post` (C1) `= NOT _matches(mechanism.postconditions, live_body)`. Undefined when the response is `304` (no body observed) — then C1 does not fire, by frozen policy.
- `stale_pre` (C2) `= NOT _matches(mechanism.preconditions ∪ applicability_guards, live_auth_context)`, where `live_auth_context` is recomputed from the HMAC-verified `auth_state` and the resource's `required_scope`.
- `stale_transport` (C3) `= (status != 200) OR (etag_cached is not None AND etag_live != etag_cached) OR cache-control weakened` (`max-age=A` → `no-store`/`no-cache`/`max-age=0`, or a newly present `immutable` conflict).
- `stale_struct` (C4) `= (jaccard(fieldpath_type_tokens_cached, fieldpath_type_tokens_live) < 0.85) OR (endpoint_template_live != endpoint_template_cached)`, threshold **0.85 inherited unchanged** from the incumbent guard. `endpoint_template = {path, sorted(query_param_names), sorted(required_header_names)}` as recorded by the mechanism at authoring time and as signalled by the live response.

`stale = stale_post OR stale_pre OR stale_transport OR stale_struct` (frozen OR; no weights, no fitted parameters, no learned threshold).

**Confidence map (frozen, pre-declared, four levels, response-derived):**

| Fires | Level | Justification for the level |
|---|---|---|
| nothing | `0.95` | four independent response-derived channels agree the inheritance is valid |
| C3 only, or C4 only | `0.92` | a weak or ambiguous single indicator; weak channels are cheap to move spuriously |
| exactly one of C1, C2 | `0.85` | a direct contradiction of the stored postcondition or of the auth/precondition context |
| two or more of C1, C2, C4, or any of C1/C2 together with a transport anomaly | `0.60` | a strong but heterogeneous evidence pattern that this frozen map cannot express finely |

The level is a function of *which channels fired*, never a hand-assigned branch value, and it is measured against the injector's ground truth rather than against the guard's own output. The attainability arithmetic and the power of the ECE gate are in §10.

### 4.4 Representation loss (disclosed, per V12)

There is **no HTML DOM, no CSSOM, no accessibility tree and no JavaScript** on this substrate. C4 is a field-path/type token signature plus a server-signaled endpoint template. The prior graph packets' family name `dom_drift` is therefore **not reused**, because it would misrepresent what was measured; its honest analogue here is `structural_field_drift`, and it is carried inside F2 rather than presented as a separate family. Additional losses: the ETag is truncated to 16 hex; field values' magnitudes, nested depth, array order and query-parameter value semantics are discarded; a value change that leaves field-shape, headers, status, validator and the mechanism's own postcondition all unchanged is **structurally undetectable** by any revalidation-based guard, and §8's X1 probe measures the price of that blind spot rather than pretending it away.

---

## 5. Action representation

- **Intent:** `fetch_resource` with `{resource_id}`; a second intent `fetch_resource_detail` with `{resource_id, detail}` for F2.
- **Mechanism action template:** the recorded `GET` path + query-parameter names + required header names + the stored `Authorization` value + the stored `ETag` (when a conditional revalidation was recorded at authoring time). Authoring consumes 3 observed requests per resource, from which the mechanism's preconditions, postconditions, parameter slots, cached ETag and cached token set are recorded response-derived.
- **Execution of the guard:** exactly one request per item, through the proxy, with the stored `Authorization` and the stored `If-None-Match` where available.
- **Execution of `B-NO-GUARD-REPLAY`:** zero requests; the stored mechanism is replayed and scored against ground truth.
- **Execution of `B-FRESH-REDERIVE`:** empty registry; read the live responses, construct the object from what is live, verify the postcondition deterministically. Cost counted honestly per request.
- **Execution of `B-COLD-EXPLORE`:** empty registry; 3 discovery observations per resource before execution.
- **Verification:** `src/spider/kernel.py:verify()` → `_matches(mechanism.postconditions, observed_state)`, exact equality, binary, no LLM judge, no heuristic score, no injected hash.
- **Ablations and the incumbent guard** are recomputed from the **same single exchange** as the candidate, so the arm comparison is exactly matched on requests, bytes and milliseconds and cannot be confounded by transport differences.

**Validity identity table (the sixteen `V*` ids of `spec.json.measurement_validity`, quoted here so that the short forms used above are unambiguous).** Every one is **computed at execute time by the runner**; none is a code literal, a branch value or an author assertion, and the runner must emit no `PASS` for a check it did not compute.

| Short form used above | Full identity | What is actually computed |
|---|---|---|
| V1 | `V1-SUBSTRATE-HEALTH-GATE` | the 8 substrate properties of §4.1, as floors measured over ≥ 6 health probes and ≥ 30 instrumented items |
| V2 | `V2-DRIFT-MATRIX-REACHABILITY` | the injector's plan record **and** an independent post-hoc WAL check, per family and per counterpart |
| V3 | `V3-AUTHORSHIP-AND-ARBITRATION-SEPARATION` | module graph and detector source scan; ground truth from the injector plan, never from a response body |
| V4 | `V4-ARM-BLIND-SCORING` | `detector_output.jsonl` sha256 + file creation order vs the arm-label file (metric `M-ARM-BLIND-SCORE-ORDER-OK`) |
| V5 | `V5-NO-FITTED-PARAMETERS` | diff of the executed rule set against this preregistration; threshold 0.85 and the 4-level map unchanged |
| V6 | `V6-NON-DEGENERATE-INTERVALS` | realized level counts, ECE and precision bootstrap widths |
| V7 | `V7-ECE-ATTAINABILITY-AND-NON-TAUTOLOGY` | level assignment recomputed from the recorded channel set for every item, and the §10 arithmetic re-derived |
| V8 | `V8-ECONOMIC-COST-BASIS` | requests, wire bytes both directions, wall clock ms, from the real exchange |
| V9 | `V9-PREVALENCE-AND-POWER` | realized prevalence and the exact MDE table of §10 |
| V10 | `V10-JOINT-OPERATING-POINT-FEASIBILITY` | the precision/TN joint check on realized counts, not the design-point derivation |
| V11 | `V11-ABLATION-DISTINCTNESS-IS-COMPUTED-NOT-ASSERTED` | per-ablation differing-decision counts; a zero-difference arm is `INVALID` |
| V12 | `V12-REPRESENTATION-LOSS-DISCLOSURE` | the four losses of §4.4 restated per item class, including the structurally-undetectable cell |
| V13 | `V13-RAW-EVIDENCE-AND-RECOMPUTABILITY` | full request/response logging, per-row sha256, and a replay of the scorer reproducing every decision bit-identically |
| V14 | `V14-NO-CODE-DIGEST-GATE` | absence check: the packet contains no gate requiring a code digest or code-bound attestation |
| V15 | `V15-DEPENDENCY-HONESTY` | the four unmet dependencies of §2.3 each reported `null` with the exact smallest next action, and no substitute transport or substrate in use |
| V16 | `V16-METRIC-IDENTITY-ALIASES` | the alias table of §9 carried into `result.json` without two numbers for one quantity |

---

## 6. Drift matrix (the full matrix, frozen)

**Ground truth** is `stale_inherited_knowledge ∈ {0,1}`, assigned by the **injector's plan ledger** and confirmed by an independent post-hoc check against the WAL/injector record, never by response content, never by the detector. The detector cannot see the label: the server exposes no drift marker on the wire.

### 6.1 Stale stratum — 180 items, 45 per family

| Family | Sub-instances (15 each) | Mechanism by which the inheritance is stale | Channel expected to fire |
|---|---|---|---|
| **F1 `auth_token_rotation`** | (a) old token revoked, new token minted for the same principal and scopes — data unchanged, *binding* invalid; (b) old token revoked, new token minted with reduced scopes; (c) session deleted | the stored `Authorization` value no longer executes | C2, C3 |
| **F2 `endpoint_param_header_mutation`** | (a) required query param renamed `detail`→`uid`, server rejects the unknown param with `400`; (b) required query param renamed, server *silently ignores* the unknown param and returns the default projection; (c) required header renamed `X-Csrf-Token`→`X-CSRF-Token`, `400` | the stored template no longer produces the intended result | (a)(c) C3; (b) C1 or C4 |
| **F3 `permission_boundary_change`** | (a) `read:extra` removed from the session's scopes; (b) `resources.required_scope` raised `read:basic`→`read:admin`; (c) the endpoint moved under an `/admin/` prefix requiring `read:admin` | a previously-200 request is now `403`, **with the same field-path/type token set and no ETag change**, so C4 and C3 are structurally blind | C2, C3 |
| **F4 `conditional_request_revalidation`** | (a) the server stops honouring the conditional: a request that returned `304` now returns `200` with a changed body and a new ETag; (b) `Cache-Control: max-age=300, immutable`→`no-store` and the ETag now rotates on every response; (c) the ETag is recomputed over a **stable subset** (`id`,`name`) so a `email` value change leaves the ETag and the field-shape unchanged and `max-age=300, immutable` remains | the cached value is wrong while the validator says it is fine | (a)(b) C3; (c) C1 or C4 only |

F3 and F4c are the two hard cells of the matrix, and they are the reason the incumbent signal set is carried as a baseline rather than assumed sufficient.

### 6.2 Fresh stratum — 720 items: 240 `stable` + 480 benign counterparts (120 each)

Every benign counterpart perturbs **the same observable channel** as its stale counterpart and differs only in whether the inherited knowledge remains valid. This is the property the prior three packets could not construct: their `NC-NOISE-IMMUNITY` passed at `FA=0.0` because the required-path filter `{id,name,email}` *excluded* the very fields the noise (optional `phone`, `nickname`, null `email`) touched, which their own audits recorded as satisfiable by construction.

| Counterpart | Sub-instances (30 each) | Same channel as | Inherited knowledge |
|---|---|---|---|
| **B1 `benign_token_reissue_overlap`** | new token minted inside the server's overlap/grace window; `auth_state` HMAC recomputed; token string changes | F1 | **still valid** — the stored token still executes `200` |
| **B2 `benign_template_extension`** | a new *optional* query param and a new *optional* response header appear | F2 | **still valid** — the stored template still satisfies the endpoint |
| **B3 `benign_permission_noise_elsewhere`** | scope reduced for a resource the mechanism never touches; 30 of the 120 carry a genuine `403` on `/api/permission/{id}` while the target resource stays `200` | F3 | **still valid** |
| **B4 `benign_conditional_revalidation`** | honest `304` with an unchanged ETag; 30 carry a changed ETag with a content-identical `200` revalidation body | F4 | **still valid** |

`stable` (240): valid auth, in-scope permission, honest validator, unmutated template, unchanged body.

### 6.3 Positive-control items — 120

- `PC-UNPERTURBED-INHERITANCE` — 60 no-op items. Expected `EXECUTABLE` 60/60, verification true 60/60, abstention 0. **Can fail**: it fails if the guard over-abstains on healthy inheritance, the guard's most expensive failure mode and the one no prior packet in this thread could detect.
- `PC-PLANTED-BREAK-DETECTED` — 30 items with an asserted, independently confirmed break. Expected `UNKNOWN` 30/30. **Can fail**: it fails if the guard misses a provable break.
- `PC-CONDITIONAL-304-HONEST` — 30 items with an honest validator returning a real `304`. Expected `EXECUTABLE` 30/30. **Can fail**: it fails if the guard treats an honest `304` as staleness.

All three are executed against the live substrate and scored through the identical code path as the primary. Any failure is `MEASUREMENT_INVALID` — the instrument is not adjudicated — never a scientific negative.

### 6.4 Auxiliary, non-gated — 60 items

`X1-VALIDATOR-LIE-304` (30 items): the server returns `304` while the body has actually changed. Run under **both** frozen revalidation policies:

- `POLICY-CONDITIONAL` (the default above): structurally undetectable. A miss is a **documented ceiling**, never a falsification.
- `POLICY-UNCONDITIONAL`: the guard issues an unconditional `GET`. Detection here is expected and is a **policy** finding that changes the product's cache policy.

`M-COST-DELTA-UNCONDITIONAL-VS-CONDITIONAL` (bytes and ms) is the measured price of the blind spot. These 60 items gate **nothing** and are reported under every verdict. They were declared before freeze precisely because a target that no setting of the frozen architecture can reach must be *deleted before freeze*, not scored after: a guard that re-reads a lying validator's `304` cannot detect the lie, and pretending otherwise would manufacture a `MEASUREMENT_INVALID` out of a correct implementation.

---

## 7. Holdout, target, unit of analysis, sampling

- **Unit of analysis:** one evaluated item (one mechanism × one resource × one stratum). Dependence is handled by stratification, not by treating correlated items as independent.
- **No fitted parameters exist anywhere in this design** (V5). The rule set, the threshold `0.85` and the four-level confidence map are pre-declared and frozen. There is therefore no train/validation/test selection surface, and no quantity may be chosen after any outcome is visible.
- **Declared split-integrity check (not a selection split):** the 900 items are split into two disjoint resource halves A and B by a frozen seed rule. `M-HALF-SPLIT-TN-A/B` and `M-HALF-SPLIT-FA-A/B` are reported. If either half violates TN point ≥ 0.85 or FA point ≤ 0.10, the outcome is `MIXED` with `decision=RESOURCE_HETEROGENEOUS`. This catches a result driven by one resource family without selecting on anything.
- **Uncertainty:** Wilson score intervals (z = 1.959964) on every primary proportion, used for every gate, non-degenerate by construction. Auxiliary bootstrap: 2000 resamples, stratified by stratum × family, percentile method, used for `M-ECE-BOOTSTRAP-UPPER-975`, `M-UNKNOWN-PRECISION-BOOT-CI` and reported widths only. A bootstrap interval of width 0 is declared `DEGENERATE` and satisfies no gate.
- **Sampling policy:** frozen, no outcome-dependent adaptation. Item ids, family assignment, resource ids, auth states and injection order are generated from seed `36302977302 mod 2^32` by a pre-declared generator, and the **seeded order is archived before execution** as `raw_evidence/seeded_order.json`, adopting `EXP-RUNTIME-36129163700/artifacts/A-SEEDED-ORDER.json` as an executed design property.

---

## 8. Nulls, baselines, controls — and why each can fire

| Id | Kind | Can it fail? | Expected |
|---|---|---|---|
| `NC-BENIGN-COUNTERPART-IMMUNITY` | null control, **mandatory** | **Yes, by construction** — all 480 items perturb the same channel as their stale counterpart | abstention ≤ 0.10 pooled, ≤ 0.20 per family |
| `NC-PERMUTED-GROUND-TRUTH` | honesty null | **Yes** — if the scorer's discrimination is chance, the permuted band is not entered | 1000 family-level label permutations; the candidate's decision/label association must sit inside the preregistered null band, proving the scoring code has power (the absence-of-power defect that made `EXP-INTEL-36293264917` score resolved-but-wrong artifacts as `NOT_FOUND`) |
| `NC-ABLATION-DECISION-DISTINCTNESS` | design-validity null | **Yes** | ≥ 3 of 4 ablations differ from the candidate on ≥ 1 item; a zero-difference ablation is declared `INVALID` and not scored |
| `NC-ARM-BLIND-SCORE-ORDER` | design-validity null | **Yes** | detector output written and sha256-recorded before the arm-label file exists; verified by hash plus file creation order |
| `NC-AUTHORSHIP-SEPARATION` | design-validity null | **Yes** | injector and detector in separate files; detector source contains no reference to the injector module; runner aborts the packet on violation |
| `NC-NO-HARDCODED-OUTCOME` | honesty null | **Yes** | replaying the scorer over the raw log reproduces 900/900 decisions bit-identically |
| `PC-UNPERTURBED-INHERITANCE` | positive control | **Yes** | 60/60 `EXECUTABLE` |
| `PC-PLANTED-BREAK-DETECTED` | positive control | **Yes** | 30/30 `UNKNOWN` |
| `PC-CONDITIONAL-304-HONEST` | positive control | **Yes** | 30/30 `EXECUTABLE` |

Baselines: `B-NO-GUARD-REPLAY`, `B-INCUMBENT-GUARD` (the exact prior signal set C3∨C4 at threshold 0.85, confidences 0.95/0.85), `B-POSTCOND-ONLY`, `B-PERMISSION-ONLY`, `B-VALIDATOR-ONLY`, `B-STRUCTURE-ONLY`, `B-FRESH-REDERIVE` (Arm B), `B-COLD-EXPLORE`. Full definitions in `spec.json.baselines`. All are recomputed from the candidate's single exchange except the two cost arms, which issue their own requests and are counted on the same instrument.

---

## 9. Stable metric and control identities (reuse these verbatim in `result.json`)

**Primary guard metrics**
`M-TN-SPIDER` · `M-TN-WILSON-LOWER` · `M-TN-WILSON-UPPER` · `M-FA-SPIDER` · `M-FA-WILSON-UPPER` · `M-TP-SPIDER` · `M-UNKNOWN-PRECISION-SPIDER` · `M-UNKNOWN-PRECISION-WILSON-LOWER` · `M-UNKNOWN-PRECISION-BOOT-CI` · `M-UNKNOWN-RATE-SPIDER` · `M-UNKNOWN-RATE-PATIENT` (= unknown rate over the 720 fresh items) · `M-ECE-GLOBAL` · `M-ECE-FRESH` · `M-ECE-STALE` · `M-ECE-BOOTSTRAP-UPPER-975` · `M-ECE-BOOTSTRAP-WIDTH` · `M-UNKNOWN-PRECISION-BOOTSTRAP-WIDTH` · `M-N-CONFIDENCE-LEVELS-REALIZED` · `M-N-CONFIDENCE-LEVELS-FRESH` · `M-N-CONFIDENCE-LEVELS-STALE` · `M-STALE-PREVALENCE-REALIZED` · `M-N-FRESH` · `M-N-STALE` · `M-N-EVALUATED-NON304`

**Per-family / per-counterpart (all four of each, `null` if unreached)**
`M-FA-PER-FAMILY-F1|F2|F3|F4` + `M-FA-PER-FAMILY-<F>-WILSON-UPPER` · `M-TP-PER-FAMILY-F1|F2|F3|F4` · `M-ABSTENTION-PER-BENIGN-B1|B2|B3|B4` + Wilson uppers · `M-REACH-F1|F2|F3|F4` · `M-REACH-B1|B2|B3|B4`

**Half-split stability**
`M-HALF-SPLIT-TN-A` · `M-HALF-SPLIT-TN-B` · `M-HALF-SPLIT-FA-A` · `M-HALF-SPLIT-FA-B`

**Baseline contrasts**
`M-FA-B-NO-GUARD-REPLAY` · `M-TN-B-NO-GUARD-REPLAY` · `M-FA-B-INCUMBENT-GUARD` · `M-TN-B-INCUMBENT-GUARD` · `M-ECE-B-INCUMBENT-GUARD` · `M-FA-B-POSTCOND-ONLY` · `M-FA-B-PERMISSION-ONLY` · `M-FA-B-VALIDATOR-ONLY` · `M-FA-B-STRUCTURE-ONLY` · `M-DISTINCT-ITEMS-B-POSTCOND-ONLY` · `M-DISTINCT-ITEMS-B-PERMISSION-ONLY` · `M-DISTINCT-ITEMS-B-VALIDATOR-ONLY` · `M-DISTINCT-ITEMS-B-STRUCTURE-ONLY`

**Economics (measured basis: requests, wire bytes, wall-clock ms — no tokens)**
`M-REDERIVE-SUCCESS` · `M-REDERIVE-STALE-ACCEPT` (**`null` by construction, §2.3**) · `M-REDERIVE-PATH-REQUESTS` · `M-REDERIVE-PATH-WIRE-BYTES` · `M-REDERIVE-PATH-WALLCLOCK-MS` · `M-COLD-PATH-REQUESTS` · `M-COLD-PATH-WIRE-BYTES` · `M-COLD-PATH-WALLCLOCK-MS` · `M-GUARD-PATH-REQUESTS-F1` · `M-GUARD-PATH-REQUESTS-F10` · `M-REDERIVE-PATH-REQUESTS-F10` · `M-GUARD-OVERHEAD-RATIO-F10` · `U-BREAKEVEN` · `M-BREAKEVEN-F-GRID` (the smallest `f ∈ {1,2,5,10}` at which the guard path is cheaper on all three bases) · `M-NO-GUARD-PATH-REQUESTS-F10` (= 0 by construction; reported for completeness, not as an economic winner, because it buys its zero cost with the measured FA)

**Auxiliary, non-gated**
`M-X1-DETECTION-POLICY-CONDITIONAL` · `M-X1-DETECTION-POLICY-UNCONDITIONAL` · `M-COST-DELTA-UNCONDITIONAL-VS-CONDITIONAL-BYTES` · `M-COST-DELTA-UNCONDITIONAL-VS-CONDITIONAL-MS`

**Health / instrument**
`M-HEALTH-GATE-PASS` · `M-N-DISTINCT-WORKER-PID` · `M-CROSS-WORKER-VISIBILITY` · `M-WAL-JOURNAL-MODE` · `M-REAL-304-COUNT` · `M-HMAC-AUTH-VERIFIED` · `M-PROXY-ROUNDROBIN-SPREAD` · `M-ARM-BLIND-SCORE-ORDER-OK` · `M-AUTHORSHIP-SEPARATION-OK` · `M-NO-HARDCODED-OUTCOME-OK` · `M-NONDEGENERATE-INTERVAL-OK` · `M-N-PERMUTED-TRIALS` · `M-PERMUTED-ASSOCIATION-BAND-LOW` · `M-PERMUTED-ASSOCIATION-BAND-HIGH`

**Control identities:** `PC-UNPERTURBED-INHERITANCE` · `PC-PLANTED-BREAK-DETECTED` · `PC-CONDITIONAL-304-HONEST` · `NC-BENIGN-COUNTERPART-IMMUNITY` · `NC-PERMUTED-GROUND-TRUTH` · `NC-ABLATION-DECISION-DISTINCTNESS` · `NC-ARM-BLIND-SCORE-ORDER` · `NC-AUTHORSHIP-SEPARATION` · `NC-NO-HARDCODED-OUTCOME`.
**Baseline identities:** `B-NO-GUARD-REPLAY` · `B-INCUMBENT-GUARD` · `B-POSTCOND-ONLY` · `B-PERMISSION-ONLY` · `B-VALIDATOR-ONLY` · `B-STRUCTURE-ONLY` · `B-FRESH-REDERIVE` · `B-COLD-EXPLORE`.

**Metric-identity aliases (V16-METRIC-IDENTITY-ALIASES).** Two names in this packet denote one quantity and are declared equivalent, so EXECUTE and AUDIT cannot silently split them: `M-TN-A-CANDIDATE` is an alias of `M-TN-SPIDER` (pooled TN of `A-CANDIDATE` over the 720 fresh items), and `M-FA-A-CANDIDATE` is an alias of `M-FA-SPIDER` (pooled FA over the 180 stale items). The alias form appears in `spec.json.falsifier` and `spec.json.decision_rule` because those clauses name the arm; the canonical form is the one in §9. `result.json` must report the canonical form and must never report two different numbers for one quantity. The wildcard forms `M-HALF-SPLIT-*` and `M-DISTINCT-ITEMS-B-*` in `spec.json` are exactly the eight expanded identities in §9; the expansion introduces no new quantity. `X1-VALIDATOR-LIE` and `X1-VALIDATOR-LIE-304` are **one** probe, not two, with outcomes `M-X1-DETECTION-POLICY-CONDITIONAL` and `M-X1-DETECTION-POLICY-UNCONDITIONAL`. **Inventory authority:** §9 above is the complete canonical metric inventory of this packet and is hashed by the freezer together with `spec.json`; the `M-` ids appearing inline in `spec.json` are a non-exhaustive subset consisting only of the metrics referenced by the falsifier, the decision rule or a `V-` condition. No metric in §9 was invented after freeze, and none of them is a quantity absent from the frozen design.

---

## 10. Power, prevalence, attainability and non-degeneracy — the arithmetic, frozen before freeze

**Sample and prevalence.** `pi_stale = 0.20` declared; `n_stale = 180` (45 per family), `n_fresh = 720` (240 stable + 480 benign), `n_evaluated = 900` non-304 items.

**Exact one-sided binomial tests, alpha = 0.05, target power 0.80.** MDEs are quoted to 6 decimals because the 4-decimal roundings of `0.1651` and `0.8829` sit a few units below the true MDE and would otherwise show power 0.7997 and 0.7989 on recomputation:

| Quantity | n | Null | Rejection rule | alpha at the null | MDE (p1 at power exactly 0.80) |
|---|---|---|---|---|---|
| FA (pooled) | 180 | 0.10 | `>= 26/180` | 0.0362 | **0.165129** (0.1651) |
| TN (pooled) | 720 | 0.85 | `>= 629/720` | 0.0402 | **0.882946** (0.8829) |
| UNKNOWN precision | 204 | 0.85 | `>= 183/204` | 0.0326 | **0.911151** (0.9112) |
| FA (per family) | 45 | 0.10 | `>= 9/45` | 0.0320 | **0.243264** (0.2433) |

Every rejection rule is conservative at alpha ≤ 0.05, and every MDE is attained at power ≥ 0.80 by construction. **These are design-point power figures, not a licence to stop early:** the packet runs the full frozen `n` with no sequential testing, no optional stopping and no outcome-dependent adaptation (§7).

**Accept-side Wilson boundaries at the design point:** FA `0/180` upper `0.0209`; FA `18/180` (= 0.10) upper `0.1525`; TN `720/720` lower `0.9947`; TN `684/720` (= 0.95) lower `0.9316`; UNKNOWN precision `180/204` = `0.8824`, lower `0.8309`. The gate is stated as `FA <= 0.10 AND Wilson upper < 0.1525` so the bound is exact rather than asymptotic.

**Joint-operating-point feasibility (V10), frozen.** TN ≥ 0.85 and UNKNOWN precision ≥ 0.85 are *not* independent. Solving `TP / (TP + FN_fresh) >= 0.85` for `FN_fresh <= 0.15·TP/0.85 = 0.17647·TP`, with `n_stale = 180` and `n_fresh = 720`:

| TP (stale items flagged) | max `FN_fresh` | required TN | precision at that boundary | precision one step worse |
|---|---|---|---|---|
| 153 (= 0.85 × 180) | **27** | **0.9625** | 153/180 = 0.8500 | 153/181 = 0.8453 |
| 170 | 30 | 0.9583 | 170/200 = 0.8500 | 170/201 = 0.8458 |
| 180 (= 100% of stale) | **31** | **0.9569** | 180/211 = 0.8531 | 180/212 = 0.8491 |

So A1 and A3 are a genuine joint requirement: even at **perfect detection** (TP = 180) the guard must still keep `FN_fresh <= 31`, i.e. TN ≥ 0.9569, and at 85% detection TN ≥ 0.9625. The pair is attainable (TN = 1, TP = 180 → precision 1.0) and genuinely falsifiable (TN = 0.85 with TP = 153 → unknowns = 153 + 108 = 261 → precision `153/261 = 0.586`, a clear fail). **Design consequence, frozen:** the expected operating point is high specificity *and* high sensitivity, with the abstention rate near the stale prevalence; an abstention rate far above the stale prevalence fails A3 through its effect on TN, and a high abstention rate is *not* a safe fallback. Safety and calibration failures are reported as separate fields so neither can hide inside the other. These are design-point feasibility bounds computed from the frozen `n`; at execute time V10 recomputes the same inequality on the **realized** counts, so a run that passes A1 and A3 by a hair is distinguishable from one that passes with margin.

**ECE attainability and non-tautology (V7), frozen.** With every decision correct, global ECE as a function of the confidence-level mix `(p0.95, p0.92, p0.85, p0.60)`:

| mix | ECE |
|---|---|
| (0.55, 0.05, 0.40, 0.00) | **0.0915** |
| (0.40, 0.10, 0.50, 0.00) | 0.1030 |
| (0.30, 0.10, 0.60, 0.00) | 0.1130 |
| (0.20, 0.15, 0.65, 0.00) | 0.1195 |
| (0.10, 0.20, 0.70, 0.00) | 0.1260 |

So the 0.15 target has real headroom, and it is **not** satisfiable by construction: a level-0.85 bin of accuracy 0.50 at mass 0.40 alone gives `0.55·0.05 + 0.05·0.08 + 0.40·0.35 = 0.1715` (**FAIL**), and a fresh bin with 0.20 false negatives at mass 0.40 gives **0.124** (pass but materially worse). Simulated bootstrap over 900 items at the ideal point: ECE point `0.070`, 97.5% upper `0.0727`, width `0.0052` — comfortably inside the `0.18` upper bound and **non-degenerate**, so the `width > 0.002` requirement is satisfiable. **Frozen interpretive boundary:** if the realized mass at confidence ≤ 0.60 exceeds `0.20`, the calibration arm is reported `INCONCLUSIVE_BY_LEVEL_MIX` with that stated reason and the map is **not** re-tuned — because the frozen map cannot express fine confidence for a heterogeneous evidence pattern, and rewriting it after seeing the mix would be exactly the post-hoc adaptation this thread has already paid for three times.

**Non-degeneracy (V6), frozen.** `M-NONDEGENERATE-INTERVAL-OK` requires: ≥ 3 distinct realized confidence levels overall; ≥ 2 within the fresh class; ≥ 2 within the stale class; ECE bootstrap width > 0.002; UNKNOWN-precision bootstrap width > 0.002. This targets the exact recorded defects of the parent thread — `EXP-GRAPH-35947468747`'s `[1.0, 1.0]` and `[0.0, 0.0]` bootstrap intervals, and `EXP-GRAPH-35940399935`'s two-populated-bin ECE "satisfiable by construction".

---

## 11. Decision rule (frozen; identical to `spec.json.decision_rule`)

**GATE 0 — preconditions and validity, short-circuits. Any failure ⇒ `status=MEASUREMENT_INVALID` (or `BLOCKED`), `outcome=INCONCLUSIVE`, no claim-level statement, each false gate carrying an exact smallest next action. Never a scientific negative.**
`G1` health gate · `G2` arm-blind scoring, authorship separation, no-hardcoded-outcome · `G3` non-degenerate intervals · `G4` drift reachability ≥ 3/4 stale and ≥ 3/4 benign · `G5` all seven controls evaluated, all three PCs pass, `NC-BENIGN-COUNTERPART-IMMUNITY` ≤ 0.10 pooled and ≤ 0.20 per family, `NC-PERMUTED-GROUND-TRUTH` inside band, ≥ 3/4 ablations decision-distinct.

**GATE 1 — the frozen accept branch, reached only if GATE 0 fully passes.** `SUPPORTS` iff **all nine** of these hold, enumerated one-to-one with `spec.json.decision_rule` so that AUDIT can match them by identity and not by prose:
**A1** `M-TN-SPIDER >= 0.85` and `M-TN-WILSON-LOWER > 0.75` · **A2** `M-FA-SPIDER <= 0.10` and `M-FA-WILSON-UPPER < 0.1525` · **A3** `M-UNKNOWN-PRECISION-SPIDER >= 0.85` · **A4** `M-ECE-GLOBAL <= 0.15` and `M-ECE-FRESH <= 0.15` and `M-ECE-STALE <= 0.15` and `M-ECE-BOOTSTRAP-UPPER-975 <= 0.18` · **A5** selectivity `M-UNKNOWN-RATE-PATIENT ∈ (0.15, 0.85]` · **A6** `M-FA-PER-FAMILY-<F>-WILSON-UPPER < 0.20` for every reached family · **A7** `M-FA-B-NO-GUARD-REPLAY - M-FA-SPIDER >= 0.15` · **A8** `M-GUARD-PATH-REQUESTS-F10 <= M-REDERIVE-PATH-REQUESTS-F10` and `M-UNKNOWN-RATE-PATIENT <= U-BREAKEVEN` · **A9** `M-FA-B-INCUMBENT-GUARD > M-FA-SPIDER + 0.02` or `M-TN-B-INCUMBENT-GUARD < M-TN-SPIDER - 0.02`.
(`M-TN-A-CANDIDATE` ≡ `M-TN-SPIDER` and `M-FA-A-CANDIDATE` ≡ `M-FA-SPIDER` per V16.)

`FALSIFIES` iff GATE 0 passed and **any** of the nine falsifiers holds, enumerated one-to-one with `spec.json.falsifier`: **F1** `M-TN-SPIDER < 0.85` or `M-TN-WILSON-LOWER <= 0.75` · **F2** `M-FA-SPIDER > 0.10` or `M-FA-WILSON-UPPER >= 0.1525` · **F3** `M-UNKNOWN-PRECISION-SPIDER < 0.85` · **F4** `M-ECE-GLOBAL > 0.15` or `M-ECE-BOOTSTRAP-UPPER-975 > 0.18` or `M-ECE-FRESH > 0.15` or `M-ECE-STALE > 0.15` · **F5** `M-UNKNOWN-RATE-PATIENT > 0.85` or `M-UNKNOWN-RATE-PATIENT <= 0.15` (non-selective) · **F6** per-family FA Wilson upper > 0.20 for at least two of the four mandated families · **F7** `M-GUARD-PATH-REQUESTS-F10 > M-REDERIVE-PATH-REQUESTS-F10` on requests, bytes and milliseconds · **F8** `M-FA-B-NO-GUARD-REPLAY - M-FA-SPIDER < 0.15` · **F9** `M-FA-B-INCUMBENT-GUARD <= M-FA-SPIDER + 0.02` and `M-TN-B-INCUMBENT-GUARD >= M-TN-SPIDER - 0.02`.

**Safety falsifiers are F1–F6, F8, F9. The economic falsifier is F7 alone.**
`MIXED` in exactly two preregistered ways: **F7 alone** → `decision=FALSIFIES_ECONOMIC_ONLY` (safety evidence preserved, product prefers re-derivation); **A1–A4 pass with confidence mass ≤ 0.60 above 0.20** → `decision=CALIBRATION_INCONCLUSIVE_BY_LEVEL_MIX`; **either half-split violated** → `decision=RESOURCE_HETEROGENEOUS`.
`INCONCLUSIVE` only when a primary interval straddles its threshold with width > 0.20 at the frozen `n`, which the MDE arithmetic of §10 makes a narrow band.
`X1-VALIDATOR-LIE-304` under either policy is reported under every verdict and gates nothing.

**Explicit non-outcomes.** `MEASUREMENT_INVALID` at GATE 0 is not a falsification of `C-FRESHNESS` and does not lower its registry status. `BLOCKED` is not `FALSIFIES`. A valid `FALSIFIES` does not close the domain and does not authorise retiring the mechanism. A valid `SUPPORTS` moves `C-FRESHNESS` at most to `EXPERIMENTAL`, on this substrate, with no LLM, no browser, no real site, one seed, one run, no replication — and promotion beyond that is a Director decision, not a producer one.

---

## 12. Validity threats, disclosure, and what would change the verdict

**Threats closed by construction, and by machine check rather than by assertion:**
- *Drift engineered to match the guard.* The four mandated families are defined by the environmental intervention, not by any guard feature. F3 and F4c are constructed so that the incumbent signal set is **structurally blind**, and the incumbent is carried as `B-INCUMBENT-GUARD`, so the blindness becomes a measurement (`M-FA-B-INCUMBENT-GUARD` per family) instead of a hidden assumption.
- *A null control that cannot fire.* `NC-BENIGN-COUNTERPART-IMMUNITY` perturbs the same channels as its stale counterparts; the prior thread's filter-excluded noise fields are gone.
- *A positive control that cannot fail.* All three PCs fail on over-abstention, on a miss, or on mishandling an honest `304`.
- *A reference arm algebraically identical to the candidate.* `NC-ABLATION-DECISION-DISTINCTNESS` counts differing decisions and invalidates a zero-difference arm.
- *Unattainable or construction-satisfiable numeric targets.* §10 gives exact MDEs, Wilson boundaries, a joint-feasibility derivation and ECE attainability/power before freeze; the one declared-unreachable target (the lying validator under `POLICY-CONDITIONAL`) is declared **non-gated** before freeze.
- *Author/measurer and arbiter/ground-truth confounds.* Separate modules, arm-blind output hashed before the label file exists, both machine-checked with abort-on-violation.
- *A cost basis the program authored.* Requests, wire bytes and wall clock from the real exchange; no abstract units, no tokens.
- *A gate the control plane cannot satisfy.* No code-digest or code-bound gate anywhere in this packet (V14); the binding is the executed health gate.

**Threats that remain, disclosed:**
1. One locally hosted, stdlib-only, flat-JSON, single-service substrate. Not a real website; not C-CROSSSITE; not TLS, HTTP/2, CDN or multi-host.
2. No HTML DOM / accessibility tree / JavaScript, so C4 is a field-path/type signature, not a DOM signature (§4.4).
3. A value change invisible to field-shape, headers, status, validator and postcondition is structurally undetectable; X1 measures the price, not the absence.
4. One seed, one run, no replication, no model, no browser. `EXP-GRAPH-35940399935` reached `M-UNKNOWN-RATE-SPIDER 0.4286` at prevalence `0.4286` on 210 items in one run; nothing here licenses a distributional statement.
5. The permutation null band for `NC-PERMUTED-GROUND-TRUTH` is computed at execute time from the realized family structure and frozen into `result.json`; it is a check that the scorer has power, not a hypothesis test of the guard.
6. The economic comparison stops at a **break-even abstention rate**. It does not price a wrong action, because no real agent and no model are available; so the packet delivers "the guard is admissible iff `u <= u*`", and the Director supplies the price of an error.
7. Representation loss on the endpoint template relies on a server-signaled template, which is a convenience this substrate provides. On a site that does not advertise its parameter contract, C4's endpoint-template half would have to be inferred from the request/response exchange, and this packet does not measure that.

**What would change the verdict, in both directions.** *Positive:* the guard passes GATE 0 and A1–A9 → `C-FRESHNESS` to `EXPERIMENTAL` at a named ceiling, the product may expose freshness as an `UNKNOWN`-before-execute gate, `C-DELTA-REPAIR` gets its preregistered guard prerequisite at `EXPERIMENTAL`, and the revalidation policy is chosen from the measured X1 cost delta. *Negative, safety:* GATE 0 passes and F1–F6/F8–F9 fire → the product defaults to re-derivation plus caching, ships no replay-on-assumption-of-freshness path, and the signal set must be re-derived at a different level of description rather than re-thresholded, because `0.85` is not the binding constraint. *Negative, economic:* F7 alone → do not ship the guard as a mechanism; ship re-derivation with response caching, and revisit guarding only where `R` is small. *Negative, no incremental value:* F9 → the incumbent signal set plus re-derivation is the whole answer, and the added channel architecture does not earn its maintenance surface. None of the three retires the claim or closes the domain.

---

## 13. Execution obligations

EXECUTE must execute exactly this frozen design. It must (i) write raw evidence before any derived measurement, with per-row sha256 and the request/response exchange needed to recompute every decision; (ii) keep `RAW EVIDENCE` → `OBSERVATION` → `DERIVED MEASUREMENT` → `INTERPRETATION` distinct; (iii) reuse the metric and control identifiers in §9 verbatim in `result.json`; (iv) record `null` with a reason for every unreachable family, metric and dependency, and never substitute a substitute; (v) distinguish measurement failure from a scientific negative, and never convert the former into the latter; (vi) report `M-REDERIVE-STALE-ACCEPT` as `null`, never as `0.0`; (vii) report the X1 probe under every verdict and gate nothing with it; (viii) not emit a PASS for any check it did not compute — the parent thread's most serious process failure was a `V9 PASS` attested over a `[FILLED_AT_FREEZE]` placeholder, and this packet contains no such gate; and (ix) make no git commit, push, switch or reset, and edit no file outside `research/experiments/EXP-GRAPH-36302977302/`, `research/harness/` and `research/graph/`.

*Design frozen pre-outcome. No outcome-bearing measurement was taken, inspected or simulated during DESIGN.*
