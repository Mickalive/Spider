# EXP-GRAPH-35947468747 — Preregistration (DESIGN frozen pre-outcome)

**Lane:** graph  
**Claim:** C-FRESHNESS — SPIDER can detect when inherited knowledge is stale (next_gate: session/token/DOM/endpoint/permission drift with false-accept measurement at realistic prevalence)  
**Experiment ID:** EXP-GRAPH-35947468747  
**Director mandate:** CONTINUE C-FRESHNESS (action=CONTINUE, parent_handoff_disposition=USE, cognitive_reset=false, dependencies=[runtime]) per `request.json:director_mandate` — comparative reasoning: Vs re-dispatching WebArena-Verified v2 param-inherit pilot (8 consecutive MEASUREMENT_INVALID on durability gates `distill_parameterized` distinct slot/field-path filter/Jaccard>=0.75 via grep/sha256/git diff — marginal value 0 until durability proof), Vs immediate delta-repair BLOCKED upstream on same substrate, Vs per-value alias handling lower urgency; freshness gate is prerequisite. `inherited_next_question` advisory, `director_mandate.question` binding per AGENTS.md precedence.  
**Parent handoff:** `research/experiments/EXP-GRAPH-35940399935/handoff.json` (SHA 8b85b91d1d769610a823075cc2e0511b5abc7647b976f493f5b110d7a7537265, verdict SURVIVES_CURRENT_TEST) — preserved as continuity evidence only per `director_mandate.parent_handoff_disposition=USE`; not automatic agenda.  
**Frozen hashes:** request `71bc4fb1f95e4f55b9392d4717501f5cfa2ad210aafcc03f00d209e8d29b97b9`, claim registry `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b` — design must not inspect outcome data.

---

## 1. Strategic Question → Falsifiable Question

**Director strategic question (verbatim request.json:director_mandate.question):**

> On the same locally-hosted synthetic single-resource flat-JSON substrate with honest per-trajectory-reset sum-counter (resolve+bind+verify+freshness+browser_steps without jitter/n*3200/f*6.0, trajectory-grouped max |rho_shuffled|<0.20 within-f std>0) and deterministic _matches verification, does the validated freshness guard (Jaccard 0.85 required-filtered + response-derived endpoint _template/X-Csrf-Token + ETag+max-age=0, recalibrated 0.95 fresh/0.85 stale) sustain TN>=0.85 (Wilson lower>0.75) FA<=0.10 calibrated (per-class ECE<=0.15, UNKNOWN prevalence-aware [0.00,0.18] at 15% stale prevalence with non-degenerate Wilson/bootstrap CIs, NC-NOISE-IMMUNITY fresh-only optional-field churn) when rebalanced to realistic 15% stale prevalence, and when transferred to health-gated distributed shared-WAL Flask/JWT + nginx If-None-Match/304 substrate at n>=800 non-304 (single-node first then distributed), vs no-guard baseline, thereby testing the step from bounded synthetic EXPERIMENTAL to VALIDATED required before bounded C-DELTA-REPAIR (localized repair cost delta < full-task, contamination<0.10) and honest C-RESIDUAL-NOVELTY M_total_f10 Pareto can be attempted?

**Falsifiable refined question (this prereg — smallest high-information test):**

> On the same synthetic single-resource `/resource/{id}` stdlib http.server flat-JSON substrate with the identical deterministic guard and recalibrated 0.95/0.85, honest constant integer sum-counter (base 4 per request) and trajectory-grouped max |rho_shuffled|<0.20, deterministic `src/spider/kernel.py:_matches` verification, does the guard sustain TN≥0.85 (Wilson lower>0.75), FA≤0.10, UNKNOWN in prevalence-aware [0.00,0.18] and stale_rate±0.07, global ECE≤0.15 and per-class ECE≤0.15 each, with non-degenerate Wilson (n_fresh=180 lower~0.979) and 5000 family-stratified trajectory-grouped bootstrap CIs (width>0) and NC-NOISE-IMMUNITY FA≤0.10, beating B-NO-GUARD by FA delta≥0.15 and both single-signal ablations, when rebalanced to realistic 15% stale prevalence (180 fresh + 30 stale + 150 noise =360; stale_rate 30/210=0.1428); and conditional on runtime health-gate passing, does the same guard sustain the identical TN/FA/ECE gates at n≥800 non-304 on a health-gated distributed shared-WAL Flask/JWT + nginx If-None-Match/304 substrate (single-node Flask health-gated first, then 2×gunicorn+nginx round-robin HS256), vs matched no-guard baseline?

Design is the smallest high-information test that can change C-FRESHNESS claim/product decision per Director rationale; it does NOT merely repeat the 42.8% stale degenerate-CI synthetic run nor the 8 prior WebArena add_to_cart param-inherit pilots.

---

## 2. Hypothesis

**H1 (positive):** Prevalence rebalancing to 15% stale does not break the guard: on the rebalanced synthetic site (180 fresh, 30 stale =10 per family, 150 noise) the combined DOM+header/cache guard remains satisfiable — TN≥0.85 Wilson lower>0.75 (180/180 gives 1.0 lower 0.979, or 162/180 gives 0.90 lower 0.853), FA≤0.10 on 30 stale (0/30 gives upper 0.1135, 3/30=0.10 passes), UNKNOWN=stale_rate=0.1428 within [0.0928,0.2128]∩[0.00,0.18] => [0.0928,0.18], global ECE ~0.0643 and per-class each ≤0.15 under 0.95/0.85, per-family TP≥0.85 (9/10 per family), discriminating vs B-NO-GUARD FA~1.0 delta≥0.90 and vs B-JACCARD-ONLY FA~0.66 / B-HEADER-ONLY FA~0.33, max|rho_shuffled|<0.20 trajectory-grouped, constant integer cost, per-trajectory observed caching, response-derived endpoint, noise-immunity FA≤0.10, with non-degenerate 5000 bootstrap CIs (width>0). Health-gated distributed transfer at n≥800 non-304 will sustain identical gates if the runtime substrate is healthy (shared WAL, distinct X-Worker-Pid≥2, HS256 verified, 304 operational); otherwise that stage is MEASUREMENT_INVALID without falsifying the synthetic gate. Orthogonal signal necessity (DOM+header/cache) explains detection, not pooled-metric salience or cost tautology.

**H0 (null):** Guard fails any of D1-D8 at realistic sparsity while honesty gates pass: TN<0.85 or FA>0.10 at n_stale=30, UNKNOWN outside prevalence-aware bound, ECE>0.15 global/per-class, no FA delta vs no-guard, per-family TP<0.85 at 10 per family, or NC-NOISE-IMMUNITY FA>0.10 (noise conflated). Honesty gates may trigger MEASUREMENT_INVALID if constant counter, trajectory-grouped max rho, 5000 bootstrap, per-trajectory caching, or response-derived signals violated — distinct from scientific falsification.

**Prior expectations used (director_mandate.agent_priors_used, labeled as prior not SPIDER evidence):** (1) path-dependence and stale context salience without calibrated freshness/UNKNOWN abstention (ECE≤0.15, precision≥0.85) compounds multiplicatively; (2) memory beating no-memory trivial, real leverage requires beating Stagehand DOM-hash cache / RAG TFIDF / TERX replay on amortized M_total_f10, not tautological per_hit — drives per_hit retirement; (3) compression-reuse tradeoff specificity (LCP) vs generalization (slots/alias) fails when DOM variance not prefix-aligned — per-value alias/program synthesis likely needed; (4) long-horizon planning errors compound, localized delta-repair <50% tokens plausible only behind health-gated verification blocking unverified writes — MEA auditor pattern necessary; (5) near-deterministic SPAs with low H(S_next|URL,H_K=3) hide dynamics; correlated environmental non-determinism (session/permission per-trajectory) cheapest way to inject H>0.2.

---

## 3. Continuity vs Director Supersede — Preservation of Established/Rejected/Unknown/Do_not_assume

This section explicitly preserves the four-way distinction from `EXP-GRAPH-35940399935/handoff.json:carry_forward` per transmission discipline; `director_mandate.question` is followed as binding direction, parent `next_question` not silently overridden but harmonized (USE disposition).

**Established (preserved verbatim, not re-tested as hypothesis):**

- Bounded synthetic EXPERIMENTAL ceiling ONLY: locally-hosted stdlib http.server flat-JSON single-resource `/resource/{id}` (127.0.0.1 ephemeral, N=210 staleness 120 fresh+90 stale 30+30 per drift family +30 stable +150 noise 50 per churn variant total 360) with deterministic orthogonal drifts — dom_drift Jaccard required-filtered {id,name,email} 0.5 <0.85, param_header_mutation response-derived _template detail->uid + X-Csrf-Token abc123->xyz789, cache_expiry ETag SHA256[:16] changed + Cache-Control 60->0 with deterministic 304 — guard Jaccard<0.85 OR param_template_changed OR (etag_changed AND max-age=0) achieves M-TN-SPIDER 1.0 Wilson lower 0.969 (120/120), M-FALSE-ACCEPT 0.0 upper 0.0409 (0/90) per-family TP/TN 1.0 lower 0.8865 (30/30 each), audited PASS recomputed metrics match.
- Calibration at satisfiable operating point: UNKNOWN 0.4286 = stale_rate within [0.00,0.50] and [0.3786,0.4986], global ECE 0.0929 per-class fresh 0.05 stale 0.15 at recalibrated 0.95/0.85 (120*0.05/210=0.0286+90*0.15/210=0.0643=0.0929) ≤0.15, degenerate CIs [1.0,1.0]/[0.0,0.0]/[0.4286,0.4286]/[0.0929,0.0929] reported as ceiling effect not precision, validated via within-family freshness std 0.5 >0.
- Signal isolation necessity: ablations prove combined signal required — B-JACCARD-ONLY FA 0.6667 TP 30/90 only dom_drift, B-HEADER-ONLY FA 0.3333 TP 60/90 misses dom_drift, B-NO-GUARD FA 1.0 delta 1.0 vs SPIDER 0.0, NC-NOISE-IMMUNITY FA 0.0 TN 1.0 on 150 noise (required-path filter, ETag alone without max-age=0 not flagged).
- Measurement-validity fixes verified: honest constant integer sum-counter base 4, trajectory-grouped max|rho| 0.0 <0.20 via 1000 whole-trajectory perms, within-family std 0.5, 5000 family-stratified bootstrap, V1 deterministic _matches exact equality, V14 per-trajectory caching with response-derived endpoint, V7 Wilson z=1.96, V8 recalibrated ECE+UNKNOWN satisfiable, honest economics channel max|rho| 0.0 demonstrates no tautology but constant cost makes rho trivially 0.

**Rejected (must NOT be cited as support; explicitly rejected):**

- Single-signal guards as standalone detectors at 0.85 threshold and header/ETag-only insufficient — bounded rejection, not broader C-FRESHNESS domain.
- No-guard baseline as safe reuse: B-NO-GUARD FA 1.0 bounded rejection of always-EXECUTABLE.
- No bounded hypothesis rejected for calibration beyond this signal/threshold/site: prior D3 UNKNOWN [0,0.15] and D4 ECE failures were specification impossibilities, not empirical falsifications — replaced by satisfiable prevalence-aware bounds.
- Any inference that C-FRESHNESS globally falsified or deterministic ceiling implies product readiness — bounded synthetic POC only, MEASUREMENT_INVALID≠FALSIFIED.

**Unknown (this experiment's target to resolve):**

- Whether guard sustains TN≥0.85 FA≤0.10 calibrated at realistic 15% stale prevalence (180 fresh+30 stale +150 noise) with non-degenerate Wilson lower>0.75 / FA upper informative and 5000 trajectory-grouped bootstrap CIs width>0 instead of degenerate [1.0,1.0]/[0.0,0.0] at 42.8% ceiling — **PRIMARY unknown, this experiment tests it on synthetic-rebalanced**.
- Whether guard transfers to health-gated distributed shared-WAL Flask/JWT + nginx If-None-Match/304 substrate at n≥800 non-304 with single-node first then distributed HS256 X-Worker-Pid≥2 — **SECONDARY unknown, health-gated in this packet**.
- Whether correlated latent non-determinism where DOM_before correlates with latent state (session/permission) detectable by DOM+header/cache — only independent deterministic drift tested.
- Whether ETag change alone without max-age=0 should be stale — AND logic boundary untested.
- Whether localized delta-repair and C-RESIDUAL-NOVELTY Pareto hold on same substrate with honest counter — unblocked but not yet measured after synthetic-rebalanced gate; **NOT in this packet**.
- Whether required-path-filter noise immunity generalizes beyond optional-field churn — tautological by design.
- Whether per-trajectory cache using first valid of 3 misses rare optional fields in non-deterministic settings.
- Whether 304 via cached body circular — deterministic marked not stale per spec but not independently validated.

**Do_not_assume (explicit non-conclusions):**

- SURVIVES at 42.8% stale with TN 1.0 FA 0.0 implies TN≥0.85 FA≤0.10 at 15% stale or on Flask/JWT/WAL/CDN — prevalence, operational 304, session non-replication change operating point.
- Degenerate bootstrap CIs [1.0,1.0] imply high-precision — they reflect deterministic ceiling effect, not precision; informativeness requires non-degenerate CIs at 15% rebalanced.
- Recalibrated 0.95/0.85 yielding ECE 0.0929 demonstrates general calibration — only 2 bins populated, per-class stale at threshold 0.15 tautological.
- UNKNOWN 0.4286 within [0.00,0.50] implies calibrated abstention generally — exactly equals stale_rate by construction; gate satisfiable at 42.8% not sparsity.
- NC-NOISE-IMMUNITY FA 0.0 proves robustness to real churn — noise is optional-field churn excluded by filter and ETag alone without max-age=0; does not distinguish structural noise.
- Constant sum-counter 4 with max|rho| 0.0 proves honest economics discriminates — rho trivially 0 because cost variance 0; gate tests no jitter only.
- _matches verified True 360/360 implies learned distillation — tautological self-consistency, not param induction.
- Combined guard necessity implies orthogonal levels unnecessary — director prior 6 requires workflow IR/endpoint catalog/WebMCP/hierarchical retrieval have higher information gain than threshold tweak; this tests only Jaccard+header/cache.
- C-FRESHNESS reaches VALIDATED/PRODUCT_CORE from any bounded synthetic POC — requires n≥800 + health-gated shared-WAL + audit PASS; this packet authorizes no promotion.
- MEASUREMENT_INVALID = FALSIFIED-IN-SETTING — distinct per transmission discipline.
- B-NO-GUARD TN 1.0 implies strong baseline — discriminating power is FA delta and per-family TP.

---

## 4. State Representation

- **Raw observation (synthetic primary):** HTTP response for `/resource/{id}`: JSON body flat object 3-5 fields (id, title, author, plus optional phone/nickname), `ETag: SHA256(canonical_json_body)[:16]`, `Cache-Control: max-age=60` or `max-age=0`/`no-store`, `X-Csrf-Token` header, and response-signaled template field `_template: {query_params: [...], header_names: [...]}` server emits for response-derived endpoint detection. For NC-NOISE, server adds optional `phone`/`nickname` p=0.3 or `email: null` p=0.2 as fresh noise.
- **Raw observation (distributed secondary, health-gated):** Same `/resource/{id}` but served by Flask 3.1.3 + PyJWT 2.13.0 HS256 on `/health`, `/auth`, `/resource/{id}` with JWT Bearer token, SQLite WAL `/tmp/spider-runtime/<run>/shared.db` (journal_mode WAL) or Redis, 2×gunicorn 23.0.0 sync workers + nginx 1.24.0 round-robin, operational `If-None-Match: <ETag>` → 304 handling, `X-Worker-Pid` header exposing worker. Only counted if health-gate passes.
- **Derived freshness state (per-trajectory observed cache, both substrates):**
  - `dom_tokens_cached = sorted {(field_path,type)}` via `extract_field_types` (types string/integer/boolean/array/object) from requests 1,2,3 per trajectory first valid frozen.
  - `header_tokens_cached = {Cache-Control, ETag, X-Csrf-Token}` from same observed requests; `header_tokens_live` from live response.
  - `endpoint_template_cached = {path + sorted(query_param_names) + sorted(header_names)}` extracted from observed response `_template` (response-derived); `endpoint_template_live` from live response `_template`.
  - `jaccard_dom = |dom_tokens_cached ∩ dom_tokens_live| / |dom_tokens_cached ∪ dom_tokens_live|; etag_changed = (ETag_live != ETag_cached); cache_expiry = (Cache-Control_cached max-age=60 AND live max-age=0); param_template_changed = (endpoint_template_live != endpoint_template_cached)` exact set equality on response-derived names. Combined: `stale = (jaccard_dom <0.85) OR param_template_changed OR (etag_changed AND cache_expiry)` threshold 0.85 frozen.
- **Confidence (recalibrated frozen):** `0.95` if `stale==False` (EXECUTABLE fresh), `0.85` if `stale==True` (UNKNOWN stale flagged). No 0.50 for correct stales.
- **Representation loss disclosed:** DOM tokens ignore value magnitudes/nested depth beyond flat keys; ETag truncated to 16 hex; endpoint template ignores param value semantics; per-trajectory cache 3 observations may miss rare optional fields; synthetic site single resource flat-JSON only, not production DOM/session/CDN depth; distributed stage adds JWT/session but still single resource flat JSON.

---

## 5. Action Representation

- **Intent:** `fetch_resource` with params `{resource_id}`.
- **Mechanism action_template:** `GET /resource/${resource_id}` with headers `{X-Csrf-Token: ${token}}` and query `?detail=${detail}` (param template). Literal mechanism via SPIDER kernel `distill` literal; `distill_parameterized` not under test for freshness.
- **Execution (synthetic):** stdlib `urllib.request` GET to `http://127.0.0.1:{port}/resource/{id}?detail={detail}` with `X-Csrf-Token`. No browser (browser_steps=0 deterministic, retained for honest counter). Conditional `If-None-Match: <cached ETag>` → 304 marked not stale deterministically.
- **Execution (distributed health-gated):** Same but via `http://127.0.0.1:{nginx_port}/resource/{id}` through nginx→gunicorn, with `Authorization: Bearer <JWT>` (HS256 shared TESTBED_SECRET), same If-None-Match handling operational.
- **Verification:** `verify(mechanism_id, observed_state)` via `src/spider/kernel.py:_matches(required, actual)` exact equality on required_slots = set(parameter_slots) | _template_slots(action_template) postconditions; deterministic, no LLM judge. All requests verified synthetic and distributed (if health-gated).

---

## 6. Target, Unit of Analysis, and Sampling Policy

- **Target:** Binary staleness classification per request (fresh vs stale) and abstention decision (EXECUTABLE vs UNKNOWN/false_accept), plus noise-immunity for optional-field churn; distributed conditional target same but with operational 304 semantics.
- **Unit of analysis:** Single HTTP request/transition, grouped at trajectory/family level for inference (trajectory-grouped bootstrap preserves within-trajectory dependence).
- **Sampling policy (frozen, no outcome-dependent adaptation):**
  - **Synthetic primary server:** `http.server.HTTPServer` on 127.0.0.1 ephemeral port, stdlib only, no Docker/external network, single resource type only.
  - **Rebalanced prevalence:** Stale_rate 30/210=0.1428 (15% target). Composition: 180 fresh pool (12 trajectories ×15 requests, no drift) + 30 stale pool (3 families ×2 trajectories ×5 fresh+5 stale? Actually 10 stale per family =30 stale, each trajectory DRIFT_POINT=6, 5 fresh before drift per stale trajectory) =210 staleness pool; plus 150 noise pool (15 trajectories ×10, 5 per churn variant A/B/C) =360 total. DRIFT_POINT=6 per stale trajectory (requests 1-5 fresh, 6-10 stale) exactly as parent.
    1. `dom_drift`: 2 trajectories ×10 =20 (10 fresh+10 stale) stale family slice 10 stale, Jaccard 0.60-0.75 <0.85.
    2. `param_header_mutation`: 2 trajectories ×10 =20 (10 stale), mutation via response `_template` detail->uid and X-Csrf-Token rotation, response-derived detection.
    3. `cache_expiry`: 2 trajectories ×10 =20 (10 stale), ETag SHA256 change + max-age 60->0, If-None-Match 304 path deterministic.
  - **Control stable fresh:** included in 180 fresh pool (no separate stable family needed; 180 fresh covers NC-FRESH-RETAIN).
  - **NC-NOISE-IMMUNITY stimulus frozen:** 15 fresh trajectories (5 per variant ×10 req =150 all fresh): variant A phone p=0.3, variant B nickname p=0.3, variant C email null p=0.2 + phone p=0.3, all fresh ground truth, Jaccard required-filtered should remain ≥0.85.
  - **Distributed secondary policy (health-gated):** Flask/JWT/WAL substrate only if V-DIST-HEALTH-GATE passes: Flask 3.1.3+PyJWT HS256, 2×gunicorn 23.0.0 sync workers sharing SQLite WAL at `/tmp/spider-runtime/EXP-GRAPH-35947468747/shared.db` (WAL mode) or Redis, nginx 1.24.0 round-robin, HS256 shared secret probe, distinct X-Worker-Pid≥2 across 10 probes, If-None-Match→304 operational, n≥800 non-304 stratified ≥250 per family (dom_drift, param_header, cache_expiry) plus stable fresh; same deterministic drifts but via Flask response mutation. If health-gate fails, secondary stage logged as MEASUREMENT_INVALID with n_actual and reason, synthetic primary still adjudicated.
  - No real network, no LLM, no Docker for primary; distributed gated stage uses local Docker-free gunicorn+nginx only, seeds deterministic (port ephemeral, trajectory order fixed).

---

## 7. Holdout

- **Within-synthetic holdout (per-trajectory observed):** Fresh requests 1-5 per stale trajectory are cache source for that trajectory's mechanism; stale/noise requests 6-10 (or all 10 for fresh trajectories) held out for detection test. No overlap request_number between cache and test; no global template leakage — cache per-trajectory observed, not precomputed.
- **Cross-family holdout:** Each family 10 stale held separately (per-family TP reported) to prevent header/body conflation; family-stratified bootstrap preserves family proportions (180 fresh +10 per family stale +150 noise).
- **No website holdout (synthetic):** Claim ceiling bounded to locally-hosted synthetic; not C-CROSSSITE.
- **Distributed holdout:** Per-trajectory observed same as synthetic; additionally endpoint holdout — mechanisms cached on one endpoint family not leaked to another before test; n≥800 ensures per-endpoint Wilson sensitivity.

---

## 8. Nulls / Baselines (strong, matched tasks)

All baselines run on same rebalanced 180+30+150=360 synthetic requests (and n≥800 distributed if health-gated) for matched comparison:

- **B-NO-GUARD (primary):** No freshness gate; resolve always EXECUTABLE if preconditions pass. Must show FA~1.0 on 30 stale (30/30) and delta vs SPIDER ≥0.15, UNKNOWN 0 fails prevalence-aware bound.
- **B-JACCARD-ONLY:** Freshness uses only DOM Jaccard <0.85, ignoring Cache-Control/ETag and response-derived param_header mutation. Expected FA~0.66 (only dom_drift 10/10, others 0/10), proving combined signal necessary at sparsity.
- **B-HEADER-ONLY:** Freshness uses only Cache-Control+ETag+response-derived header mutation, ignoring DOM drift. Expected FA~0.33 (TP 20/30), fails dom_drift family — complementary ablation.
- **Positive control PC-STALE-DETECTION:** Injected stale must be flagged per family TP≥0.85 (9/10). If PC fails → pipeline broken, MEASUREMENT_INVALID not falsification. Distributed PC-DISTR same at n≥800 if gated.
- **Null controls:** NC-FRESH-RETAIN (180 fresh TN≥0.85), NC-NOISE-IMMUNITY (150 churn/null FA≤0.10). Both deterministic _matches, per-trajectory caching, response-derived signals. Distributed NC-DISTR same if gated.

Strong baseline justification: beating no-guard by delta ≥0.88 necessary-but-weaker; beating both single-signal ablations by 0.33-0.66 and passing noise-immunity distinguishes multi-channel detection from pooled-metric salience at realistic sparsity; parent parent showed ablations degrade as expected at 42.8%, replication at 15% required for VALIDATED.

---

## 9. Primary Metrics & Decision Rule (frozen, satisfiable)

**Stable metric IDs (MUST be reused verbatim in result.json:metrics and controls):**

- `M-TN-SPIDER` = TN/(TN+FP) on 180 fresh pool — primary
- `M-TN-WILSON-LOWER` = Wilson lower (z=1.96) for M-TN-SPIDER (180 n)
- `M-FALSE-ACCEPT-SPIDER` = FP_stale/(TP+FN)_stale = # stale EXECUTABLE / 30 — rebalanced FA
- `M-FALSE-ACCEPT-WILSON-UPPER` = Wilson upper for M-FALSE-ACCEPT-SPIDER (30 n, 0/30 upper 0.1135)
- `M-UNKNOWN-RATE-SPIDER` = # UNKNOWN (stale flagged, 0.85) / 210 staleness pool
- `M-UNKNOWN-WILSON-LOWER/UPPER` = Wilson interval for UNKNOWN
- `M-ECE-SPIDER` (global) = ECE over 10 equal-width bins [0,0.1)...[0.9,1.0] on recalibrated 0.95/0.85 — ECE = sum_b |acc_b - conf_b|*n_b/N
- `M-ECE-FRESH` = per-class ECE on ground-truth fresh (180 n)
- `M-ECE-STALE` = per-class ECE on ground-truth stale (30 n)
- Per-family `M-TN-FAMILY-{dom_drift,param_header_mutation,cache_expiry,stable}` and `M-TP-FAMILY-{...}` plus Wilson lowers (n=10 per stale family)
- Honesty: `M-RHO-SHUFFLED-MAX` = max |Pearson rho| 1000 trajectory-grouped perms (PRIMARY), `M-RHO-SHUFFLED-MEAN` auxiliary, `M-COST-SPIDER-SUM` integer, `M-WITHIN-FAMILY-STD-MIN-FRESHNESS`, `M-COST-SPIDER-VECTOR` logged, `M-OBSERVED-RHO`
- Noise: `M-FA-NOISE` = # noise fresh flagged stale /150, `M-TN-NOISE`, Wilson for noise
- Baselines: `M-FA-B-NO-GUARD`, `M-FA-B-JACCARD-ONLY` (`M-TP-FAMILY-JACCARD`), `M-FA-B-HEADER-ONLY`
- Bootstrap: 5000 family-stratified trajectory-grouped 95% percentile CIs for all primary metrics (`M-TN-BOOT-CI`, `M-FA-BOOT-CI`, `M-UNKNOWN-BOOT-CI`, `M-ECE-BOOT-CI`, `M-ECE-FRESH-BOOT-CI`, `M-ECE-STALE-BOOT-CI`), width reported for non-degeneracy
- Distributed health-gated (logged if gated, else validity_notes): `M-TN-DISTR`, `M-FA-DISTR`, `M-UNKNOWN-DISTR`, `M-ECE-DISTR`, per-family TP-DISTR, `M-N-DISTR-NON304`, `M-HEALTH-GATE-PASS`, `M-X-WORKER-PIDS`, `M-JWT-VERIFY-PASS`, `M-304-OPERATIONAL`

**Frozen decision rule (see spec.json:decision_rule, satisfiable by construction):**

- **PRIMARY SURVIVES_CURRENT_TEST (synthetic-rebalanced) iff ALL D1-D9 hold:**
  - D1 TN_SPIDER ≥0.85 AND Wilson lower >0.75 (n=180)
  - D2 false_accept_SPIDER ≤0.10 on 30 stale (point ≤0.10; Wilson upper <0.18 reported for non-degeneracy)
  - D3 UNKNOWN in [0.00,0.18] AND within [stale_rate-0.05, stale_rate+0.07] (stale_rate 0.1428 => [0.0928,0.2128] ∩ [0.00,0.18] => [0.0928,0.18]; expected 0.1428 passes)
  - D4 global ECE ≤0.15 AND per-class ECE_fresh ≤0.15 AND per-class ECE_stale ≤0.15 under recalibrated 0.95/0.85 (expected 0.0643 passes: 180*0.05/210=0.0429 +30*0.15/210=0.0214)
  - D5 false_accept_NO_GUARD - false_accept_SPIDER ≥0.15 AND false_accept_NO_GUARD >0.10 (expected delta ~0.90)
  - D6 per-family TN ≥0.75 and per-family TP ≥0.85 for each 3 families (≥9/10 per family)
  - D7 PC-STALE-DETECTION TP ≥0.85 per family
  - D8 NC-FRESH-RETAIN TN ≥0.85 AND NC-NOISE-IMMUNITY FA ≤0.10 (≤15/150)
  - D9 honesty gates V2-V6 pass: integer constant sum-counter without parity (V2/V3), max|rho_shuffled|<0.20 trajectory-grouped (V4), within-family freshness std>0 (V5, cost exempt), 5000 bootstrap done non-degenerate width>0 (V6/V7), per-trajectory caching and response-derived endpoint verified (V14), N≥180+30
- **FALSIFIED-IN-SETTING iff any D1-D8 fails while D9 passes** (valid scientific negative on calibration/detection at realistic sparsity — prior 42.8% ceiling inflated)
- **MEASUREMENT_INVALID iff any V2-V6 honesty gate fails, verification not deterministic _matches, 304 mishandling, per-trajectory caching not used, endpoint not response-derived, server failure, or N<180+30**
- **DISTRIBUTED CONDITIONAL:** If V-DIST-HEALTH-GATE passes and n_non304≥800, evaluate same D1-D8 on distributed substrate overall and per endpoint (per-endpoint TN≥0.85 FA≤0.10); CONDITIONAL_SURVIVES if all pass, else DISTRIBUTED_FALSIFIED. If health-gate fails or n<800 => DISTRIBUTED_MEASUREMENT_INVALID for that stage (logged in validity_notes/unresolved, does not override synthetic PRIMARY verdict). Overall packet SURVIVES requires PRIMARY SURVIVES; DISTRIBUTED SURVIVES upgrades ceiling toward VALIDATED but not required for PRIMARY.
- **INCONCLUSIVE only if primary CIs straddle thresholds with width>0.20 due to underpower at n_stale=30** (disclosed but not expected; 0/30 Wilson width 0.1135 <0.20).

Recalibration satisfiability proof frozen: With 180 fresh at 0.95 and 30 stale at 0.85, contribution fresh 0.05*180/210=0.0429, stale 0.15*30/210=0.0214 => global ECE 0.0643 <0.15. Per-class fresh |1.0-0.95|=0.05 passes, stale |1.0-0.85|=0.15 at threshold passes, UNKNOWN 0.1428 <0.18 passes.

---

## 10. Uncertainty Method

- **Wilson CI** for proportions (TN, TP, FA, UNKNOWN) z=1.96 on raw counts not smoothed; lower for TN, upper for FA; at rebalanced n_stale=30 disclose exact Wilson 0/30 upper 0.1135 vs 90/90 upper 0.0409, power implications.
- **Trajectory-grouped family-stratified bootstrap (B=5000):** resample with replacement at trajectory level (12 fresh trajs, 6 stale trajs per family? rebalanced: 12 fresh trajs + 6 stale trajs (2 per family) +15 noise trajs), stratified by family (preserve 180 fresh +10 per family stale +150 noise), recompute TN, FA, UNKNOWN, global ECE, per-class ECE per resample → percentile 95% CI (2.5th,97.5th). Non-degeneracy required: CI width>0 (lower<1.0 and upper>0.0) to claim precision; degenerate [1.0,1.0] flagged as ceiling effect. Also bootstrap CI for D5 delta.
- **Honesty null:** max |rho_shuffled| via 1000 perms trajectory-grouped (shuffle whole trajectory blocks' cost vectors vs outcomes); report max primary <0.20 and mean auxiliary. Threshold <0.20.
- **Adequacy rule:** N≥180 fresh +30 stale +150 noise total 360 ensures Wilson lower sensitivity at 0.85 (half-width ~0.06 on fresh) while 30 stale gives informative upper 0.1135 (not degenerate 0.04). If N smaller => underpowered => MEASUREMENT_INVALID for primary.
- **Distributed uncertainty:** same Wilson and 5000 bootstrap on n≥800 non-304 with health-gated stratification; per-endpoint Wilson lower>0.75 required.

---

## 11. Falsification / Survival Rule

- Positive `PRIMARY SURVIVES` upgrades bounded synthetic ceiling from degenerate 42.8% EXPERIMENTAL to non-degenerate honest 15% prevalence-aware EXPERIMENTAL with trajectory-grouped max rho<0.20, prevalence-aware UNKNOWN [0.00,0.18], per-class ECE, noise-immunity; unblocks synthetic delta-repair contamination-bound and honest M_total_f10 Pareto on same substrate without distributed WAL; does NOT promote C-FRESHNESS to VALIDATED/PRODUCT_CORE (needs distributed n≥800 health-gated + audit PASS per registry). Conditional distributed SURVIVES upgrades ceiling toward VALIDATED within same packet.
- Negative `FALSIFIED` bounded to this signal/threshold/site/prevalence/confidence: C-FRESHNESS remains HYPOTHESIS/EXPERIMENTAL, does NOT imply impossibility with other signals/thresholds/sites/session-correlated DOM. Product must retain UNKNOWN override and not rely on this gate for residual-novelty/per_hit economics; orthogonal workflow-IR/endpoint-catalog levels required per prior 6.
- `MEASUREMENT_INVALID` means honest-cost, trajectory-grouped rho, per-trajectory cache, response-derived endpoint, or verification substrate failed; or distributed health-gate failed (that stage only); no claim update for that stage, must not be cited as falsification.

---

## 12. Validity Threats & Mitigations

- **Threat: Prevalence inflation (prior 42.8% synthetic hitting satisfiable 0.50 bound).** Mitigated by rebalanced 15% stale (180+30) with prevalence-aware [0.00,0.18] and stale_rate±0.07 requiring UNKNOWN~0.14, not 0.42; Wilson lower>0.75 still sensitive at n=180, FA upper 0.1135 informative.
- **Threat: Degenerate CIs [1.0,1.0]/[0.0,0.0] masking precision.** Mitigated by requiring non-degenerate bootstrap CIs width>0 (V6/V7) and reporting Wilson exactly; 15% prevalence with imperfect separation at threshold makes perfect 180/180 less tautological.
- **Threat: Jitter/n*3200/f*6.0 tautology.** Mitigated by honest constant integer sum-counter base 4 (V2/V3), trajectory-grouped max rho<0.20 (V4), cost std exempt (V5).
- **Threat: Header/body conflation.** Mitigated by single-resource isolation, orthogonal families 10 per family, separate ablations B-JACCARD-ONLY/B-HEADER-ONLY must fail as expected, response-derived endpoint isolation.
- **Threat: Pooled-metric salience hiding per-family 0/10.** Mitigated by family-stratified trajectory-grouped bootstrap (V6) and per-family TP≥0.85 at n=10 (requires 9/10).
- **Threat: ECE 0.5 stale confidence impossibility (parent).** Mitigated by recalibrated 0.95/0.85 and per-class ECE (V8) with satisfiability proof 0.0643 <0.15 at 15% prevalence; UNKNOWN prevalence-aware not [0,0.15].
- **Threat: n_stale=30 low power straddling threshold.** Mitigated by Wilson upper 0.1135 at 0/30 still <0.18, requiring point FA≤0.10 not upper≤0.10; disclose width>0.20 inconclusive boundary.
- **Threat: Tautological verification.** Disclosed ceiling: verification tests self-consistency of required vs actual from same deterministic generator, not learned distill_parameterized; bounded synthetic ceiling only.
- **Threat: Synthetic-to-real/distributed gap.** Disclosed: primary stdlib flat JSON only; distributed health-gated stage explicitly tests Flask/JWT/WAL/304 transfer within same packet if healthy; otherwise logged as DISTRIBUTED_MEASUREMENT_INVALID, not conflated with synthetic falsification.
- **Threat: Action→own-request tautology.** Mitigated by response-derived endpoint signals (server emits mutated template, client compares response to response) and per-trajectory cache; NC-NOISE tests independent noise NOT flagged.
- **Threat: Per-trajectory cache miss & 304 circularity.** Mitigated by 3 observed exemplars per trajectory and deterministic fresh generation without churn except noise pool; If-None-Match 304 exercises operational path deterministically, marked not stale and excluded from FA counting but included in health-gate verification.
- **Threat: Distributed health-gate flakiness (51-streak).** Mitigated by explicit V-DIST-HEALTH-GATE with X-Worker-Pid≥2 and HS256 JWT and 304 checks before counting n≥800; failure yields MEASUREMENT_INVALID for that stage only, not synthetic falsification.

---

## 13. Estimated Cost & Information Gain

- **Cost:** Primary synthetic-rebalanced low (~360 requests, <12 min CPU for 5000 bootstraps, <0.6 compute-hour, no LLM/browser/Docker, <$1). Secondary health-gated distributed if runtime substrate healthy: Flask+PyJWT+2×gunicorn+nginx at ~5 req/s n≥800 ~3 min + bootstraps ~3 min, <1 compute-hour, <$2; if health-gate fails secondary cost zero. Total bounded <1.5 compute-hour.
- **Gain:** Very high per Director CONTINUE comparative reasoning: directly tests neglected blocking claim (C-FRESHNESS 1/15 recent, prerequisite for C-RESIDUAL-NOVELTY rho≥0.60 and C-PRODUCT-ECON per_hit and C-DELTA-REPAIR 4×BLOCKED). Fixes degenerate prevalence/CI ceiling and restores discriminating test of detection vs calibration vs noise-immunity vs honest economics at realistic sparsity. Either PRIMARY SURVIVES (validates recalibrated prevalence-aware operating point toward VALIDATED) or FALSIFIES (requires orthogonal workflow-IR/endpoint-catalog levels, not threshold tweak) changes next product decision; distributed conditional stage then tests synthetic-to-distributed gap that is explicit VALIDATED blocker. Cannot be obtained by another WebArena add_to_cart pilot (expected repeat invalid burn, marginal info ~0).

---

## 14. Execution Scope & Code Paths

- **Allowed roots:** `research/graph`, `research/harness` per `research/lanes/registry.json:graph.allowed_code_roots` (graph lane: cumulative operational inheritance, fragments, parameterization, semantic resolution, freshness boundaries).
- **Planned harness:** `research/graph/freshness_detection/execute_single_resource_staleness.py` (repair in place for rebalanced prevalence: adjust FRESH_TRAJS=12, STALE_TRAJS_PER_FAMILY=2, DRIFT_POINT=6, confidence 0.95/0.85, UNKNOWN bound 0.18, Wilson z=1.96, 5000 trajectory-grouped bootstrap logic) and optionally `research/harness/distributed_flask_nginx.py` wrapper for health-gated secondary stage (reuse runtime harness if available via research/harness, no new infra attempted if health-gate fails). Raw evidence to `research/experiments/EXP-GRAPH-35947468747/raw_evidence/` with `execution_results.json`, `request_logs.json`, `metrics.json`, `decision.json`, `cost_logs.json`, `bootstrap_ci.json`, `per_trajectory_cache.json`, and distributed `health_gate.json`/`distributed_metrics.json` if gated. Also log SHA256 per artifact.
- **Freezing:** `freeze.json` will hash request/spec/prereg before execution; EXECUTE must not mutate frozen inputs; any pre-freeze work inconsistent with Director mandate superseded per architecture.
- **Dependencies:** runtime honest sum-counter and health-gated distributed substrate (`C-MEAS-VALID` HS256 shared-WAL) listed as dependency but not required for synthetic PRIMARY; secondary stage gated, logged as MEASUREMENT_INVALID if unavailable.
- **Signals frozen pre-execution:** threshold 0.85, DRIFT_POINT=6, deterministic server mutations, confidence 0.95/0.85, UNKNOWN bound [0.00,0.18]/[0.0928,0.2128], max rho procedure, noise stimulus p-values, per-trajectory cache size 3, health-gate X-Worker-Pid≥2, HS256 shared secret, n_non304≥800.

---

## 15. Prereg Timing & Transmission Discipline

Frozen before any outcome-bearing measurement for this experiment_id. Prior evidence cited is from Codex, `research/experiments/EXP-GRAPH-35940399935/*` audit/handoff, and `request.json:director_mandate` agent priors (labeled as prior not SPIDER evidence), not from new data. No material fact will exist only in Actions logs; all evidence paths/hashes will be in packet. Control/metric IDs frozen here will be reused verbatim in `result.json:metrics/controls` and `audit.json:recomputed_metrics` for downstream transmission. Status=COMPLETE with outcome FALSIFIES/MIXED is valid negative, not infrastructure failure; status=BLOCKED/MEASUREMENT_INVALID reserved for honesty/infra failure per packet §4, never encoded as falsification; distributed stage INVALID does not override synthetic PRIMARY. Direct # of staleness pool 30 and fresh 180 chosen for realistic 15% prevalence power, not post-hoc.

---

*Prereg follows SPIDER_MASTER_PROMPT.md §19 and Research 2.0 binding packet `research/EXPERIMENT_PACKET.md` §§3-5. DESIGN performed without outcome-bearing measurements per AGENTS.md work discipline.*
