# EXP-GRAPH-35940399935 — Preregistration (DESIGN frozen pre-outcome)

**Lane:** graph  
**Claim:** C-FRESHNESS — SPIDER can detect when inherited knowledge is stale (next_gate: session/token/DOM/endpoint/permission drift with false-accept measurement)  
**Experiment ID:** EXP-GRAPH-35940399935  
**Director mandate:** REOPEN C-FRESHNESS (action=REOPEN, parent_handoff_disposition=USE, cognitive_reset=false) per `request.json:director_mandate` — comparative reasoning: Vs continuing WebArena add_to_cart pilots (expected repeat MEASUREMENT_INVALID on durability gates, marginal info ~0) and Vs pivoting to C-DELTA-REPAIR (blocked on same HIT substrate) and Vs PARKED (wastes idle lane where detached synthetic validation CAN run), REOPEN on C-FRESHNESS with isolatable synthetic single-resource probe dominates opportunity cost.  
**Parent handoff:** `research/experiments/EXP-GRAPH-35937576511/handoff.json` (SHA 5b1652f69bee2f3f01712b9f392279ed1eb3069dd10bb22532decfde1f8b5029, verdict MEASUREMENT_INVALID) — preserved as continuity evidence only per `director_mandate.parent_handoff_disposition=USE`; not an automatic agenda. `inherited_next_question` in request.json is advisory continuity, while `director_mandate.question` is binding.  
**Frozen hashes:** request `466b894c2af75bfaf12618b822c765d2cbf4a6c4b745ca5aaaa952b5caabdde4`, claim registry `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b` — design must not inspect outcome data.

---

## 1. Strategic Question → Falsifiable Question

**Director strategic question (verbatim para 24):**

> After re-deriving a satisfiable frozen decision rule (prevalence-aware UNKNOWN bound scaled to stale rate or selective-UNKNOWN policy and per-class ECE or recalibrated confidence >0.5 for correctly flagged stales), implementing honest constant per-trajectory-reset sum-counter (resolve+bind+verify+freshness+browser_steps without jitter/n*3200/f*6.0), computing M-RHO-SHUFFLED as max over 1000 trajectory-grouped permutations, executing the frozen NC-NOISE-IMMUNITY noise stimulus (optional-field churn/null fields), and using per-trajectory cached postconditions with response-derived endpoint signals, does the same single-resource deterministic freshness guard on a locally-hosted synthetic flat-JSON site with deterministic _matches verification (DOM token drift / endpoint param+header mutation / Cache-Control+ETag expiry on one resource only) maintain TN>=0.85 (Wilson lower>0.75) and FA<=0.10 with calibrated UNKNOWN/ECE and discriminating ablations (5000 family-stratified trajectory-grouped bootstraps) vs no-guard baseline?

**Falsifiable refined question (this prereg):**

> On the same locally-hosted synthetic flat-JSON site serving one resource type (`/resource/{id}`) with deterministic freshness signals, does a SPIDER freshness guard combining DOM field-set Jaccard, response-derived endpoint template (query param + header names from response), and Cache-Control+ETag — with per-trajectory observed caching, recalibrated confidence 0.95 fresh / 0.85 stale, prevalence-aware UNKNOWN bound [0.00,0.50] (≈ stale_rate+0.07), honest constant integer sum-counter (base 4), and trajectory-grouped max |rho_shuffled| — achieve TN≥0.85 (Wilson lower>0.75), FA≤0.10, global ECE≤0.15 and per-class ECE≤0.15, beating B-NO-GUARD by FA delta≥0.15 and beating single-signal ablations, with 5000 family-stratified trajectory-grouped bootstrap CIs and deterministic _matches verification, while passing NC-NOISE-IMMUNITY (optional-field churn/null FA≤0.10)?

Design is the smallest high-information test that can change C-FRESHNESS claim/product decision per Director rationale; it does NOT merely repeat the 8 prior WebArena add_to_cart param-inherit pilots nor the parent's impossible-threshold synthetic run.

---

## 2. Hypothesis

**H1 (positive):** After the five measurement-validity fixes, the single-resource guard detects all deterministic drifts (TN 1.0, TP 1.0 per family, Wilson lower 0.969/0.8865) with FA 0.0, UNKNOWN 0.4286 within prevalence-aware bound [0.3786,0.4986] (and [0.00,0.50]), global ECE≈0.093 and per-class ECE each ≤0.15 under recalibrated confidence (0.95/0.85), discriminating vs B-NO-GUARD (FA delta 1.0) and vs B-JACCARD-ONLY (FA 0.667) / B-HEADER-ONLY (FA 0.333), with max |rho_shuffled|<0.20 trajectory-grouped, constant integer cost, per-trajectory caching, response-derived endpoint detection, and noise-immunity FA≤0.10. Signal isolation (one resource, separate body vs header vs cache channels) is necessary and sufficient for detection at this threshold.

**H0 (null):** Guard fails any of D1-D8 while honesty gates pass: TN<0.85 or FA>0.10, or UNKNOWN outside prevalence-aware bound, or ECE>0.15 global or per-class, or no delta vs no-guard, or per-family TN/TP below threshold, or NC-NOISE-IMMUNITY FA>0.10 (noise conflated). Honesty gates may also trigger MEASUREMENT_INVALID if constant counter, trajectory-grouped max rho, 5000 bootstrap, per-trajectory caching, or response-derived signals violated — distinct from scientific falsification.

**Prior expectations used (director_mandate.agent_priors_used, not SPIDER evidence):** (1) path-dependence anchors early retrieval; (2) pooled metrics hide per-family 0/10 failures → trajectory-grouped bootstrap required; (3) PMI/CMI can detect action→own-request tautology unless latent-correlated DOM; (4) O(1) caching/compilation economics depend on correct routing/state normalization; (5) shared vs per-node SQLite WAL and jitter/bijective formulas must be frozen; honest sum-counter without f*6.0/n*3200 minimal trustworthy harness; (6) after repeated FALSIFIED-IN-SETTING on threshold family, orthogonal levels (workflow IR, endpoint catalog) have higher info gain than Jaccard tweak — reflected in response-derived endpoint and per-trajectory cache orthogonal fixes, not mere threshold tuning.

---

## 3. Continuity vs Director Supersede — Preservation of Established/Rejected/Unknown/Do_not_assume

This section explicitly preserves the four-way distinction from `EXP-GRAPH-35937576511/handoff.json:carry_forward` per transmission discipline; `director_mandate.question` is followed as binding direction, parent `next_question` is not silently overridden but harmonized (USE disposition, not SUPERSEDE).

**Established (preserved verbatim, not re-tested as hypothesis):**

- Bounded synthetic POC for deterministic signal isolation on same stdlib http.server single-resource /resource/{id} flat JSON 210 requests (120 fresh/90 stale, 30+30 per drift family, stable 30 fresh): guard with Jaccard<0.85 OR param_template_changed OR (ETag_changed AND max-age=0) detected ALL injected drifts — M-TN-SPIDER 1.0 Wilson lower 0.969, M-FALSE-ACCEPT 0.0 upper 0.0409, per-family TN/TP 1.0 lower 0.8865, verified via deterministic _matches, beating B-NO-GUARD delta 1.0 and ablations — audit recomputed metrics match. Ceiling is observation-only, not validated freshness capability.
- Ablation isolation confirms domain-channel necessity: DOM Jaccard alone insufficient for param/header+cache families, header/ETag alone insufficient for DOM drift — combined signal required for 1.0 TP.
- Honest integer sum-counter mechanics validated when interpreted as constant (base 4 resolve+bind+verify+freshness), and trajectory-grouped max |rho_shuffled| 0.1514 <0.20 passes when computed as frozen (auditor recomputation) — the rho bound itself is achievable with honest cost.
- Prior LOCAL orthogonality CONFIRMED delta 0.15 remains cleanest external ceiling: EXP-GRAPH-35389145821 r=0.0022 CI upper 0.0916 TOST p=0.0006 n480 etc., but distributed TN FALSIFIED (mean 0.667 session_status 0.0) without shared store.

**Rejected (must NOT be cited as support; explicitly rejected):**

- No bounded hypothesis rejected by parent packet: D3 UNKNOWN [0,0.15] and D4 ECE<=0.15 failures are specification arithmetic impossibilities at 42.8% prevalence under 0.9/0.5 confidences, not empirical falsification of calibration hypothesis.
- Client-internal param_header_mutation self-comparison as validation of response-derived detection.
- Cost vector with traj_idx%2 parity injection as honest counting.
- Any inference that C-FRESHNESS globally falsified — parent was synthetic single-resource isolation only and MEASUREMENT_INVALID on honesty gates.

**Unknown (this experiment's target to resolve):**

- Whether prevalence-aware re-freeze (UNKNOWN <=0.50 / stale_rate+0.07 and recalibrated confidence 0.95/0.85 with per-class ECE) can achieve TN>=0.85 FA<=0.10 with calibrated UNKNOWN/ECE while preserving perfect detection on same site — **primary unknown, this experiment tests it**.
- Whether guard distinguishes optional-field churn/null-valued structural noise from true staleness — **tested via frozen NC-NOISE-IMMUNITY stimulus**.
- Whether single global fresh template vs per-trajectory observed caching changes TN/FA/bootstrap degeneracy — **tested via FIX-6b per-trajectory caching**.
- Whether response-derived endpoint signals vs client-internal changes detection — **tested via FIX-6**.
- Whether honest constant cost with exempted V5 std gate, and trajectory-grouped max rho, change validity vs parent — **tested via FIX-1/2/3**.
- Whether rebalanced 15% stale prevalence would preserve detection — **NOT tested here (keeps 42.8% to preserve power, acknowledges CI degeneracy at ceiling as valid).**
- Transfer to real APIs with production ETag/Cache-Control/If-None-Match/304, session rotation, Flask/JWT/WAL/CDN — **NOT tested here, disclosed ceiling.**

**Do_not_assume (explicit non-conclusions):**

- MEASUREMENT_INVALID ≠ FALSIFIED-IN-SETTING for C-FRESHNESS.
- Perfect TN 1.0 FA 0.0 does NOT imply calibrated operating point or product readiness (UNKNOWN/ECE must be judged under satisfiable bound).
- B-NO-GUARD TN~0 expectation incoherent with TN defined as fresh retained.
- NC-NOISE-IMMUNITY was marked pass but never executed in parent — do not assume it passed.
- _matches verified=True 210/210 is tautological coverage (required derived from same generator) not learned mechanism validation.
- Cache_expiry 304 path vacuous in parent; now deterministically exercised or marked not-applicable.
- Cost std 0.4714 and freshness std 0.20 in parent were parity jitter/binary confidence artifacts, not natural variance.
- Parent does NOT promote to VALIDATED/PRODUCT_CORE; C-FRESHNESS remains HYPOTHESIS until n>=800 + real-API/distributed validation.
- WebArena-Verified v2 param pilots remain PARKED (director disposition USE, not reinstated).

---

## 4. State Representation

- **Raw observation:** HTTP response for `/resource/{id}`: JSON body flat object 3-5 fields (id, title, author, plus optional phone/nickname), `ETag: SHA256(canonical_json_body)[:16]`, `Cache-Control: max-age=60` or `max-age=0`/`no-store`, `X-Csrf-Token` header, and a response-signaled template field ` _template: {query_params: [...], header_names: [...]}` that the server emits to allow response-derived endpoint detection (server is source of truth for mutation, not client dict). For NC-NOISE stimuli, server adds optional `phone` or `nickname` field at random with documented p, or `email: null`.
- **Derived freshness state (per-trajectory observed cache):**
  - `dom_tokens_cached = sorted {(field_path, type)}` from body via `extract_field_types` (types normalized string/integer/boolean/array/object) taken from requests 1,2,3 per trajectory (3 observed fresh exemplars, majority vote or first valid — frozen to first valid to keep deterministic). Similarly `dom_tokens_live`.
  - `header_tokens_cached = {Cache-Control, ETag, X-Csrf-Token}` values from same observed requests; `header_tokens_live` from live response.
  - `endpoint_template_cached = {path + sorted(query_param_names) + sorted(header_names)}` extracted from observed response's `_template` field (response-derived); `endpoint_template_live` from live response's `_template`.
  - Cached mechanism postconditions: `postconditions = {dom_tokens_cached, header_tokens_cached, endpoint_template_cached, action_template: GET /resource/${resource_id}}` stored per trajectory.
- **Freshness score:** `jaccard_dom = |dom_tokens_cached ∩ dom_tokens_live| / |dom_tokens_cached ∪ dom_tokens_live|`; `etag_changed = (ETag_live != ETag_cached)`; `cache_expiry = (Cache-Control_cached max-age=60 AND Cache-Control_live max-age=0)`; `param_template_changed = (endpoint_template_live != endpoint_template_cached)` (exact set equality on response-derived param/header names). Combined decision: `stale = (jaccard_dom < 0.85) OR param_template_changed OR (etag_changed AND cache_expiry)`. Threshold 0.85 frozen pre-execution.
- **Confidence (recalibrated, frozen):** `confidence = 0.95` if `stale==False` (EXECUTABLE, fresh), `confidence = 0.85` if `stale==True` (stale/UNKNOWN, correctly flagged). No 0.50 confidence for correct stales — that was the parent impossibility. 0.50 reserved only for truly borderline abstentions if guard cannot decide (not triggered on deterministic site; but if triggered, counted in ECE).
- **Representation loss disclosed:** DOM tokens ignore value magnitudes and nested depth beyond top-level flat keys; ETag truncated to 16 hex chars loses full collision resistance (irrelevant for 360 requests); endpoint template ignores param value semantics (intentional — tests structural drift); per-trajectory cache uses only 3 observations so first trajectory's cache may miss rare optional fields (mitigated by deterministic fresh generation without churn except in NC-NOISE family where churn is fresh noise).

---

## 5. Action Representation

- **Intent:** `fetch_resource` with params `{resource_id}`.
- **Mechanism action_template:** `GET /resource/${resource_id}` with headers `{X-Csrf-Token: ${token}}` and query `?detail=${detail}` (param template). Distilled from fresh observations via literal mechanism (SPIDER kernel `distill` literal; no param induction needed for this probe; `distill_parameterized` not under test).
- **Execution:** stdlib `urllib.request` GET to `http://127.0.0.1:{port}/resource/{id}?detail={detail}` with header `X-Csrf-Token`. No browser automation (browser_steps=0 deterministic, retained in sum for honesty audit trail). Conditional path: when `If-None-Match: <cached ETag>` sent and server's live ETag matches, server returns 304 Not Modified deterministically — client marks not stale (exercise 304 handling; logged).
- **Verification:** `verify(mechanism_id, observed_state)` via `src/spider/kernel.py:_matches(required, actual)` exact equality on required_slots = set(parameter_slots) | _template_slots(action_template) postconditions; deterministic, no LLM judge. All 360 requests verified.

---

## 6. Target, Unit of Analysis, and Sampling Policy

- **Target:** Binary staleness classification per request (fresh vs stale) and abstention decision (EXECUTABLE vs UNKNOWN/EXPLORE vs false_accept), plus noise-immunity classification for optional-field churn.
- **Unit of analysis:** Single HTTP request/transition, grouped at trajectory/family level for inference (trajectory-grouped bootstrap preserves within-trajectory dependence per director prior on salience).
- **Sampling policy (frozen, no outcome-dependent adaptation):**
  - Synthetic server: `http.server.HTTPServer` on 127.0.0.1 ephemeral port, stdlib only, no Docker/external network, single resource type only.
  - **Staleness families (orthogonal, separate trajectories, no scheduling confound):** DRIFT_POINT=6 per trajectory (requests 1-5 fresh, 6-10 stale) exactly as parent.
    1. `dom_drift`: 6 trajectories ×10 =60 (30 fresh +30 stale) — server changes body field-set deterministically at request 6: add `phone`, or change `id` type int→str via generator, yielding Jaccard 0.75 or 0.60 with cached tokens (<0.85). Response-derived header/ETag also changes accordingly but DOM is primary.
    2. `param_header_mutation`: 6 trajectories ×10 =60 — at request 6 server mutates endpoint in RESPONSE: query param name `detail` -> `uid` (signaled via `_template.query_params` change) and `X-Csrf-Token` value `token-abc123` -> `token-xyz789` (header value + name stable, value rotation detectable via header_tokens). Client detects via comparing live response-derived template to cached response-derived template — not client dict self-comparison.
    3. `cache_expiry`: 6 trajectories ×10 =60 — at request 6 server changes `ETag` (SHA256 over new body) and `Cache-Control: max-age=60` -> `max-age=0`, and honors `If-None-Match` with 304 for fresh-stable ETags (deterministic). Detected via `etag_changed AND cache_expiry` clause.
  - **Control:** `stable` family 3 trajectories ×10 =30 fresh no drift, always fresh (tests NC-FRESH-RETAIN).
  - **NC-NOISE-IMMUNITY stimulus (frozen, not in parent execution):** 15 additional fresh trajectories (5 per churn variant, 10 requests each =150 noise requests, all fresh ground truth): (a) Variant A: optional `phone` field added with p=0.3 per request on otherwise fresh body; (b) Variant B: optional `nickname` added with p=0.3; (c) Variant C: `email: null` with p=0.2 and optional `phone` with p=0.3 mixed. These are FRESH (no staleness drift, ETag stable except for added optional field's hash, but Jaccard of required field-set should remain ≥0.85 when optional field is ignored per mechanism's required_slots). Guard must return EXECUTABLE with TN≥0.90 and FA (fresh flagged stale) ≤0.10.
  - **Total:** 210 staleness requests (120 fresh +90 stale) +150 noise requests =360. Stale_rate for primary decision D3 computed on 210 pool (90/210=0.4286) to keep power for per-family TP; noise evaluated separately for NC-NOISE gate.
  - No real network, no LLM, no Docker, seeds deterministic (port ephemeral, trajectory order fixed).

---

## 7. Holdout

- **Within-synthetic holdout (per-trajectory observed):** Fresh requests 1-5 per trajectory are the training/cache source for that trajectory's mechanism postconditions; stale/noise requests 6-10 (or all 10 for noise) are held out for detection test. No overlap in request_number between cache and test; no global template leakage — cache is per-trajectory observed, not precomputed.
- **Cross-family holdout:** Each family tested separately (per-family TN/TP reported) to prevent header/body conflation; family-stratified bootstrap preserves family proportions.
- **No website holdout:** Claim ceiling bounded to locally-hosted synthetic site; not a cross-site transfer claim (C-CROSSSITE separate, requires website holdout).
- **No data reuse across families for caching:** Each trajectory's cache built only from its own first 3 fresh observations.

---

## 8. Nulls / Baselines (strong, matched tasks)

All baselines run on same 210 staleness requests (and separately scored on 150 noise requests where applicable) for matched comparison:

- **B-NO-GUARD (primary):** No freshness gate; resolve always EXECUTABLE if preconditions pass. Measures unsafe reuse false_accept. Must show FA~1.0 and delta vs SPIDER ≥0.15.
- **B-JACCARD-ONLY:** Freshness uses only DOM Jaccard <0.85, ignoring Cache-Control/ETag and response-derived param_header mutation. Ablation should achieve FA ~0.667 (only dom_drift TP 30/90), proving combined signal necessary — discriminating ablation per director orthogonal-level requirement.
- **B-HEADER-ONLY:** Freshness uses only Cache-Control+ETag+response-derived header mutation, ignoring DOM token drift. Expected FA ~0.333 (TP 60/90), fails dom_drift family — complementary.
- **Positive control PC-STALE-DETECTION:** Injected stale must be flagged; TP≥0.85 per family. If PC fails → pipeline broken, result is MEASUREMENT_INVALID not falsification.
- **Null controls:** NC-FRESH-RETAIN (fresh TN≥0.85), NC-NOISE-IMMUNITY (fresh churn/null FA≤0.10). Both use deterministic _matches ground truth, per-trajectory caching, response-derived signals.

Strong baseline justification: beating no-guard by FA delta 1.0 is necessary-but-weak; beating single-signal ablations by 0.33-0.67 and passing noise-immunity distinguishes memory vs. genuine multi-channel detection; prior parent showed ablations degrade as expected, so replication of that ordering is required for SURVIVES.

---

## 9. Primary Metrics & Decision Rule (frozen, satisfiable)

**Stable metric IDs (MUST be reused verbatim in result.json:metrics and controls):**

- `M-TN-SPIDER` = TN / (TN+FP) on fresh pool (fresh = <DRIFT_POINT + stable family) — primary
- `M-TN-WILSON-LOWER` = Wilson lower (z=1.96) for M-TN-SPIDER
- `M-FALSE-ACCEPT-SPIDER` = FP_stale / (TP+FN)_stale = # stale resolved EXECUTABLE / # stale (false_accept = P(EXECUTABLE|stale))
- `M-FALSE-ACCEPT-WILSON-UPPER` = Wilson upper for M-FALSE-ACCEPT-SPIDER
- `M-UNKNOWN-RATE-SPIDER` = # UNKNOWN (stale flagged, confidence 0.85) / N_total (210)
- `M-ECE-SPIDER` (global) = ECE over 10 equal-width bins [0,0.1)...[0.9,1.0] on recalibrated confidence (0.95 fresh, 0.85 stale) — ECE = sum_b |acc_b - conf_b| * n_b/N
- `M-ECE-FRESH` = per-class ECE computed only on ground-truth fresh requests
- `M-ECE-STALE` = per-class ECE computed only on ground-truth stale requests
- Per-family `M-TN-FAMILY-{dom_drift,param_header_mutation,cache_expiry}` and `M-TP-FAMILY-{...}` plus Wilson lowers
- Honesty: `M-RHO-SHUFFLED-MAX` = max |Pearson rho| between shuffled cost and outcome over 1000 trajectory-grouped permutations (PRIMARY), `M-RHO-SHUFFLED-MEAN` auxiliary, `M-COST-SPIDER-SUM` integer, `M-WITHIN-FAMILY-STD-MIN-FRESHNESS`, `M-COST-SPIDER-VECTOR` logged, `M-OBSERVED-RHO`
- Noise: `M-FA-NOISE` = # noise fresh flagged stale / 150, `M-TN-NOISE`
- Baselines: `M-FA-B-NO-GUARD`, `M-FA-B-JACCARD-ONLY`, `M-FA-B-HEADER-ONLY`
- Bootstrap: 5000 family-stratified trajectory-grouped 95% percentile CIs for all primary metrics

**Frozen decision rule (see spec.json:decision_rule, satisfiable by construction):**

- **SURVIVES_CURRENT_TEST iff ALL D1-D9 hold:**
  - D1 TN_SPIDER ≥0.85 AND Wilson lower >0.75
  - D2 false_accept_SPIDER ≤0.10
  - D3 UNKNOWN in [0.00,0.50] AND within [stale_rate-0.05, stale_rate+0.07] (stale_rate 0.4286 → [0.3786,0.4986]; parent observed 0.4286 passes)
  - D4 global ECE ≤0.15 AND per-class ECE_fresh ≤0.15 AND per-class ECE_stale ≤0.15 under recalibrated 0.95/0.85 confidences (expected ECE 0.093 passes; parent's 0.2714 at 0.5 stale fails but recalibrated fixes)
  - D5 false_accept_NO_GUARD - false_accept_SPIDER ≥0.15 AND false_accept_NO_GUARD >0.10
  - D6 per-family TN ≥0.75 and per-family TP ≥0.85 for each of 3 families
  - D7 PC-STALE-DETECTION TP ≥0.85 per family
  - D8 NC-FRESH-RETAIN TN ≥0.85 AND NC-NOISE-IMMUNITY FA ≤0.10
  - D9 honesty gates V2-V6 pass: integer constant sum-counter without parity (V2/V3), max|rho_shuffled|<0.20 trajectory-grouped (V4), within-family freshness std>0 (V5, cost std exempted), 5000 bootstrap done (V6), per-trajectory caching and response-derived endpoint verified (V14)
- **FALSIFIED-IN-SETTING iff any D1-D8 fails while D9 passes** (valid scientific negative — e.g., calibration or noise-immunity fails despite honest measurement)
- **MEASUREMENT_INVALID iff any V2-V6 honesty gate fails, verification not deterministic _matches, 304 mishandling, per-trajectory caching not used, endpoint not response-derived, server failure, or N<60 fresh+60 stale**
- **INCONCLUSIVE only if CIs straddle thresholds with width>0.20 due to underpower** (not expected at N=360)

Recalibration satisfiability proof (frozen): With 120 fresh at 0.95 and 90 stale at 0.85, contribution fresh 0.05*120/210=0.0286, stale 0.15*90/210=0.0643 → global ECE 0.0929 <0.15. Per-class: fresh |1.0-0.95|=0.05 passes, stale |1.0-0.85|=0.15 at threshold passes. UNKNOWN 0.4286 <0.50 passes.

---

## 10. Uncertainty Method

- **Wilson CI** for proportions (TN, TP, FA) z=1.96 on raw counts, not smoothed.
- **Trajectory-grouped family-stratified bootstrap (B=5000):** resample with replacement at trajectory level (6 trajectories per drift family, 3 control, 15 noise trajectories), stratified by family (preserve count per family as original), recompute TN, FA, UNKNOWN, global ECE, per-class ECE per resample → percentile 95% CI (2.5th,97.5th). Trajectory-grouping avoids pooled-bootstrap hiding per-family 0/10 failures (director prior). Also compute bootstrap CI for D5 delta.
- **Honesty null:** max |rho_shuffled| via 1000 permutations trajectory-grouped (shuffle whole trajectory blocks' cost vectors vs outcomes); report max (primary) and mean. Threshold <0.20.
- **Adequacy rule:** N≥60 fresh +60 stale total ensures Wilson lower sensitivity at 0.85 (expected half-width ~0.08). Noise pool N=150 ensures FA-NOISE Wilson half-width ~0.05. If N smaller → underpowered → MEASUREMENT_INVALID.
- **No TOST needed** for single-resource isolation (prior orthogonality TOST failures at delta 0.15 were pooling artifacts across endpoints; here TN/FA direct).

---

## 11. Falsification / Survival Rule

- Positive `SURVIVES` authorizes bounded synthetic ceiling only: single-resource freshness guard at 0.85 threshold with recalibrated 0.95/0.85 confidence and prevalence-aware UNKNOWN on this stdlib http.server flat-JSON site; unblocks synthetic delta-repair contamination-bound experiments without distributed WAL; does NOT promote C-FRESHNESS to VALIDATED/PRODUCT_CORE (needs n≥800 + real-API/distributed shared-WAL with health-gated HS256, per registry).
- Negative `FALSIFIED` bounded to this signal/threshold/site/confidence scheme: C-FRESHNESS remains HYPOTHESIS, does NOT imply impossibility of freshness detection with other signals/thresholds/sites/session-correlated DOM. Product must retain UNKNOWN override and not rely on this gate for residual-novelty/per_hit economics.
- `MEASUREMENT_INVALID` means honest-cost, trajectory-grouped rho, per-trajectory cache, response-derived endpoint, or verification substrate failed; no claim update, must not be cited as falsification.

---

## 12. Validity Threats & Mitigations

- **Threat: Jitter/n*3200/f*6.0 tautology (prior PRODUCT-ECON failures).** Mitigated by honest constant integer sum-counter (base 4, V2/V3), trajectory-grouped max rho <0.20 (V4), cost std explicitly not a falsifier (V5 exempt), logged vector for audit.
- **Threat: Header/body conflation (prior TN 0.667).** Mitigated by single-resource isolation, orthogonal drift families, separate ablations B-JACCARD-ONLY/B-HEADER-ONLY must fail as expected, response-derived endpoint isolation.
- **Threat: Confounded scheduling (prior 304 inclusion).** Mitigated by deterministic DRIFT_POINT per trajectory, single resource no cross-family scheduling, 304 exercised deterministically and excluded from TN/FA (V14).
- **Threat: Pooled-metric salience (director prior).** Mitigated by family-stratified trajectory-grouped bootstrap (V6) and per-family TN/TP reporting, not pooled.
- **Threat: ECE miscalibration due to 0.5 stale confidence (parent impossibility).** Mitigated by recalibrated 0.95/0.85 and per-class ECE (V8) with satisfiability proof; UNKNOWN prevalence-aware bound (V8) instead of [0,0.15].
- **Threat: Degenerate bootstrap CI [1.0,1.0] at ceiling.** Mitigated by within-family freshness std>0 gate (V5) for outcome-bearing measures; CI degeneracy at perfect detection is reported as ceiling effect, not high precision, but still passes D1/D2 because Wilson lower already >0.75/upper <0.10.
- **Threat: Tautological verification (_matches from same generator).** Disclosed ceiling: verification tests self-consistency of required vs actual derived from same deterministic generator, not learned `distill_parameterized`; bounded synthetic ceiling only.
- **Threat: Synthetic-to-real gap.** Disclosed: stdlib http.server flat JSON only, not production Flask/JWT/SQLite/WAL/CDN/session-token rotation; result bounded synthetic, per Director portfolio assessment needs runtime health-gated shared-WAL before product promotion.
- **Threat: Action→own-request tautology (director prior).** Mitigated by requiring response-derived endpoint signals (server emits mutated template, client compares response to response) and DOM latent-state correlation not per-step independent noise — NC-NOISE tests independent noise is NOT flagged as staleness.
- **Threat: Per-trajectory cache miss.** Mitigated by using 3 observed exemplars per trajectory and deterministic fresh generation without churn except noise family; logged cache contents for audit.

---

## 13. Estimated Cost & Information Gain

- **Cost:** Low (~360 requests, <10 min CPU for 5000 bootstraps, <0.5 compute-hour, no LLM/browser/Docker, <$1) — smallest high-information test per Director mandate, same order as parent.
- **Gain:** Very high per Director REOPEN comparative reasoning: directly tests the neglected blocking claim (C-FRESHNESS 1/15 recent, prerequisite for C-RESIDUAL-NOVELTY rho≥0.60 and C-PRODUCT-ECON per_hit and C-DELTA-REPAIR). Fixes two spec impossibilities and two implementation deviations that made parent MEASUREMENT_INVALID (zero info about calibration) and restores discriminating test of detection vs calibration vs noise-immunity vs honest economics. Either SURVIVES (unblocks synthetic delta-repair, validates recalibrated operating point) or FALSIFIES (requires orthogonal workflow-IR/endpoint-catalog levels per director prior 6, not threshold tweak) changes next product decision; MEASUREMENT_INVALID would reveal remaining honesty/substrate failure blocking 70% audits. Cannot be obtained by another WebArena add_to_cart pilot (expected repeat invalid burn).

---

## 14. Execution Scope & Code Paths

- **Allowed roots:** `research/graph`, `research/harness` per `research/lanes/registry.json:graph.allowed_code_roots` (graph lane charter: cumulative operational inheritance, fragments, parameterization, semantic resolution, freshness boundaries).
- **Planned harness:** `research/graph/freshness_detection/execute_single_resource_staleness.py` (repair in place, ~400 lines, pattern from parent `execute.py` but with 5 fixes: honest constant counter, trajectory-grouped max rho, NC-NOISE-IMMUNITY generation, per-trajectory observed caching, response-derived endpoint comparison). Raw evidence to `research/experiments/EXP-GRAPH-35940399935/raw_evidence/` with `execution_results.json`, `request_logs.json`, `metrics.json`, `decision.json`, `cost_logs.json`, `bootstrap_ci.json` and SHA256 logs. Also log `per_trajectory_cache.json` for V14 audit.
- **Freezing:** `freeze.json` will hash request/spec/prereg before execution; EXECUTE must not mutate frozen inputs; any pre-freeze work inconsistent with Director mandate may be superseded per architecture.
- **Dependencies:** runtime honest sum-counter substrate (`C-MEAS-VALID` HS256 shared-WAL health-gated harness) listed as dependency but not required for this detached synthetic validation; result informs downstream runtime integration without blocking.
- **Staleness families and signals frozen pre-execution:** threshold 0.85, DRIFT_POINT=6, deterministic server mutations, confidence 0.95/0.85, UNKNOWN bound 0.50 / stale_rate+0.07, max rho procedure, noise stimulus p-values, per-trajectory cache size 3.

---

## 15. Prereg Timing & Transmission Discipline

Frozen before any outcome-bearing measurement for this experiment_id. Prior evidence cited is from Codex, `research/experiments/EXP-GRAPH-35937576511/*` audit/handoff, and `request.json:director_mandate` agent priors (labeled as prior not SPIDER evidence), not from new data. No material fact will exist only in Actions logs; all evidence paths/hashes will be in packet. Control/metric IDs frozen here will be reused verbatim in `result.json:metrics/controls` and `audit.json:recomputed_metrics` for downstream transmission. Status=COMPLETE with outcome FALSIFIES/MIXED is valid negative, not infrastructure failure; status=BLOCKED/MEASUREMENT_INVALID reserved for honesty/infra failure, never encoded as falsification.

---

*Prereg follows SPIDER_MASTER_PROMPT.md §19 and Research 2.0 binding packet `research/EXPERIMENT_PACKET.md` §§3-5. DESIGN performed without outcome-bearing measurements per AGENTS.md work discipline.*
