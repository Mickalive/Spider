# EXP-GRAPH-36018188168 — Preregistration (DESIGN frozen pre-outcome)

**Lane:** graph  
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally (next_gate: controlled local perturbations with repair cost and contamination bounds); freshness transfer of C-FRESHNESS prerequisite embedded  
**Experiment ID:** EXP-GRAPH-36018188168  
**Director mandate:** CONTINUE C-DELTA-REPAIR (action=CONTINUE, claim_id=C-DELTA-REPAIR, parent_handoff_disposition=USE, cognitive_reset=false, dependencies=[runtime]) per `request.json:director_mandate` — `inherited_next_question` advisory continuity only, `director_mandate.question` binding per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2.  
**Parent handoff:** `research/experiments/EXP-GRAPH-35999336958/handoff.json` (SHA 6e292657ef8b671d95b6f40e23953736a7cdcca1be4c048f2abc4782d5479748, verdict MEASUREMENT_INVALID) — preserved as continuity evidence per `director_mandate.parent_handoff_disposition=USE`. Honest re-measurement required for single-node transfer. Prior narrow synthetic SURVIVES remains at EXP-GRAPH-35952148696 (audit PASS D1-D10).  
**Frozen hashes:** claim registry `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b` — design must not inspect outcome data.  
**Prior audits:** EXP-GRAPH-35952148696 audit PASS (D1-D10 all pass honest, narrow ceiling stdlib blast radius=1 disjoint-id no-op), EXP-GRAPH-35999336958 audit MEASUREMENT_INVALID (hardcoded harness: no nginx, no _matches, UNKNOWN 0.0 fails prevalence window, ECE 0.05 hardcoded, worker_pids [74102] vacuous, wal_mode delete vs WAL required, 7 artifacts missing, wrong k*5 scaling 6/7 vs 10/15, no per-trajectory-reset honest counter, no trajectory-grouped bootstrap/perm) — this prereg explicitly re-executes with actual nginx 1.24.0 + 2x gunicorn 23 Flask 3.1.3 PyJWT HS256 + WAL + _matches per all 9 required_fixes.

---

## 1. Strategic Question → Falsifiable Question

**Director strategic question (verbatim request.json:director_mandate.question):**

> Can an honest re-execution deploying actual nginx 1.24.0 $request_uri sticky in front of 2x gunicorn 23 Flask 3.1.3 PyJWT HS256 workers sharing WAL DB at /tmp/spider-runtime/single.db, with per-request deterministic _matches verification, per-trajectory-reset integer sum-counter (resolve1+bind1+verify1+freshness1+browser0/1 per mutated id), TRAIN18/TEST12 AUROC at frozen 0.85 vs unclamped 1000 trajectory-grouped perm null, 5000 family-stratified trajectory-grouped bootstrap, and registry-clone re-verification for both disjoint and same-resource contamination, achieve TN>=0.85 FA<=0.10 repair>=0.80 pooled >=0.70 per family contamination<0.10 at blast radius 1-3 (K1 30 stale, K2 10, K3 10, N>=20 unrelated) on health-gated single-node substrate with n_non304>=360, before any distributed n>=800 or f=100 authorization?

**Falsifiable refined question (this prereg — honest single-node re-execution fixing all 9 parent audit required_fixes):**

> On the health-gated single-node Flask 3.1.3/PyJWT 2.13.0 HS256 + nginx 1.24.0 $request_uri sticky substrate with SQLite file at /tmp/spider-runtime/single.db (WAL/journal_mode, HS256 JWT verified with TESTBED_SECRET, If-None-Match/ETag SHA256(canonical_json_without_template)[:16] →304 operational, $request_uri sticky consistent via X-Worker-Pid>=2) at n>=360 non-304 evaluated (180 fresh +50 stale K1-K3 +150 noise =380 evaluated /410 executed with 30 auxiliary fresh, stale_rate ~0.13, stratified >=10 per family per blast radius), using identical frozen guard (Jaccard 0.85 required-filtered {id,name,email}+response-derived _template/X-Csrf-Token+ETag+max-age=0, recalibrated 0.95 fresh/0.85 stale, honest per-trajectory-reset constant integer sum-counter resolve1+bind1+verify1+freshness1+browser0/1 per mutated id no jitter/n*3200/f*6.0/parity, trajectory-grouped max|rho|<0.20 via 1000 whole-trajectory-block perms, 5000 family-stratified trajectory-grouped bootstrap, deterministic src/spider/kernel.py _matches exact equality on required_slots), does a controlled perturbation — dom_drift (Jaccard 0.60-0.75), param_header_mutation (_template detail->uid + X-Csrf-Token abc123->xyz789), cache_expiry (ETag change + max-age 60->0) — at blast radius=1 (10 per family 30 total), blast radius=2 (10 instances mutating 2 ids), blast radius=3 (10 instances mutating 3 ids) require only localized deterministic repair achieving repair success >=80% pooled >=70% per family per k, mean cost <50% tokens (<8 per resource scaled k*16) and <40% browser (<1.2 per resource scaled k*3), verification AUROC>=0.75 precision>=0.80 at frozen 0.85 on TEST (TRAIN18/TEST12 binary _matches), contamination<0.10 pooled (<0.15 per family) on both disjoint-id (N>=20) and same-resource co-bound (N>=20) sets re-verified via _matches on registry clone snapshot isolation?

Design is the smallest high-information test that can change C-DELTA-REPAIR claim/product decision per Director rationale (CONTINUE); it does NOT repeat the prior MEASUREMENT_INVALID with hardcoded harness, but re-executes with actual nginx/gunicorn/WAL/_matches instrumentation fixing all 9 parent audit required_fixes. It leverages the sole synthetic SURVIVES prerequisite (EXP-GRAPH-35952148696) while testing single-node transfer with honest measurement validity.

---

## 2. Hypothesis

**H1 (positive, bounded single-node transfer with honest instrumentation):** The combined guard and deterministic copy-live-bytes patch are not artefacts of stdlib single-process deterministic flat-JSON. On the health-gated single-node Flask HS256 + nginx $request_uri sticky substrate at n>=360 non-304 with identical frozen thresholds/confidences/honest counter/trajectory-grouped rho/5000 bootstrap/deterministic _matches, the same thresholds will sustain: (a) freshness TN>=0.85 Wilson lower>0.75 FA<=0.10 UNKNOWN in [0.00,0.18]∩[stale_rate±0.07] global/per-class ECE<=0.15 and NC-NOISE-IMMUNITY FA<=0.10 discriminating vs B-NO-GUARD delta>=0.15 with B-JACCARD-ONLY FA~0.67 and B-HEADER-ONLY FA~0.33 each failing >=1 family; (b) localized repair success >=0.80 pooled >=0.70 per family at blast radius=1 at 5 tokens ratio 0.3125<0.50 1 browser ratio 0.333<0.40 verify 1 step per probe, contamination 0.0 on both disjoint and same-resource sets, AUROC 1.0 precision 1.0 at 0.85 perm null 0.40-0.60, amortized 15<16 1<3 at f=10 (k-scaled k*5+10<k*16). Expected health_gate true (WAL/journal_mode, HS256 verified, 304 operational, distinct X-Worker-Pid>=2).

**H0 (null, bounded transfer falsified while honesty passes):** Repair locality fails while honesty gates pass: any primary D5-D12 fails at identical thresholds despite healthy single-node substrate n>=360 — success <0.80 pooled/<0.70 per family at any k, cost >=0.50/<0.40, contamination>=0.10 on either disjoint or same-resource co-bound set, AUROC<0.75/precision<0.80 at 0.85, freshness degrades TN<0.85 FA>0.10, or no FA delta vs no-guard (<0.15). Valid scientific negative bounded to this signal/threshold/site/confidence/single-node-substrate/patch/blast-radius. Honesty gates (V2-V6, V14 etc.) trigger MEASUREMENT_INVALID if constant counter/trajectory-grouped max rho>=0.20/5000 bootstrap not trajectory-grouped/not executed controls/hardcoded — distinct from falsification per transmission discipline.

**Prior expectations used (director_mandate.agent_priors_used, labeled as prior not SPIDER evidence):** (1) Path dependence and local-optima salience: >10 consecutive experiments on same synthetic generator have sharply diminishing marginal information gain; (2) Verification cheaper than generation but calibration dominates safety: ECE<=0.15, UNKNOWN precision>=0.85, false_accept<=0.10 must gate inheritance; (3) Long-horizon agents accumulate compounding planning errors; (4) Zero-variance or bijective dependent variables produce tautological effects masquerading as falsification; (5) Another experiment in a bounded thread is low priority if neither positive nor negative result can change architectural/product decision. These motivate honest instrumentation and single-node health gate, distinguished from SPIDER evidence; not used as evidence.

---

## 3. Continuity vs Director Continuation — Preservation of Established/Rejected/Unknown/Do_not_assume

This section explicitly preserves the four-way distinction from `EXP-GRAPH-35999336958/handoff.json:carry_forward` and its parent `EXP-GRAPH-35952148696/handoff.json` per transmission discipline; `director_mandate.question` is binding direction with `parent_handoff_disposition=USE` (CONTINUE honest single-node re-execution fixing all 9 parent audit required_fixes).

**Established (preserved verbatim, not re-tested as hypothesis; this experiment re-runs synthetic sanity to demonstrate no regression):**

- Narrow deterministic detection+repair sub-ceiling ONLY on stdlib http.server single-resource flat-JSON /resource/{id} blast radius=1: combined guard Jaccard 0.85 required-filtered {id,name,email}+response-derived _template/X-Csrf-Token+ETag+max-age=0 recalibrated 0.95/0.85 at 390 executed (210 fresh+30 stale pool) both UNKNOWN 0.125 Wilson [0.089,0.1728] within [0.00,0.18]∩[stale_rate±0.07] detects ALL 30 orthogonal single-resource perturbations: TN 1.0 Wilson lower 0.982 FA 0.0 Wilson upper 0.1135 per-family TP 10/10, ECE global 0.0625 fresh 0.05 stale 0.15 ≤0.15, NC-NOISE FA 0.0 (0/150 TN 1.0), B-NO-GUARD FA 1.0 Δ1.0≥0.15, B-JACCARD-ONLY/B-HEADER-ONLY each fail ≥1 family, B-VERBATIM 0.0 proves breaking. Audit recomputed_metrics confirm identically. Bounded to deterministic synthetic response-derived signal set. This packet re-establishes with valid logs and honest instrumentation.

- Deterministic copy-and-rebind re-observe patch ceiling ONLY on same substrate blast radius=1: re-observe 1 probe from live endpoint overwrite cached dom/header/endpoint with live-derived values rebind _template re-verify via _matches exact equality restores EXECUTABLE on 30/30 pooled 1.0 Wilson lower 0.8865 per-family 10/10 at 5 tokens ratio 0.3125<0.50 and 1 browser ratio 0.333<0.40 verify 1 ≤2 matching B-ORACLE 5 units 100% (1.0x definitional ceiling disclosed per audit VF8). Honest constant integer per-trajectory-reset sum-counter 4 fresh 5 repair, trajectory-grouped max|rho| 0.0 via 1000 whole-trajectory-block perms, binary verification AUROC pooled 1.0 TEST 1.0 precision 1.0 recall 1.0 perm null unclamped 0.5002/0.4952 within [0.40,0.60] Δ0.504≥0.25 at frozen 0.85, contamination 0.0 (0/20 Wilson upper 0.1611) re-verified on registry clone disjoint ids 9000-9019, amortized 15<16 1<3 at f=10 with 5000 trajectory-grouped bootstrap CIs degenerate ceilings Wilson informative. All D1-D10 pass audit PASS. Bounded to deterministic synthetic single-resource.

- Single-signal guard insufficiency bounded to this signal/threshold/site: B-JACCARD-ONLY FA 0.6667 and B-HEADER-ONLY FA 0.3333 each fail >=1 family; B-NO-GUARD FA 1.0 delta 1.0 vs SPIDER 0.0; B-VERBATIM 0.0 proves breaking; B-RETRIEVAL executed 0.0 delta 1.0≥0.30 proves patch adds value beyond memory on synthetic only.

- Honest instrumentation gates VF1-VF7 fixed: binary _matches AUROC at frozen 0.85 TRAIN/TEST, unclamped perm null, executed PC/NC/honest counter, trajectory-grouped bootstrap 5000, clone re-verified contamination. V12 distributed DEFERRED correctly flagged DISTRIBUTED_MEASUREMENT_INVALID.

- Parent synthetic-rebalanced C-FRESHNESS ceiling remains EXPERIMENTAL (EXP-GRAPH-35947468747 audit PASS TN 1.0 FA 0.0 degenerate bootstrap) — this packet adds bounded delta-repair EXPERIMENTAL on same synthetic substrate plus health-gated single-node transfer, not VALIDATED, not production CDN/304/session or distributed WAL.

**Rejected (must NOT be cited as support; explicitly rejected, bounded):**

- Single-signal guards as standalone detectors at this signal/threshold/site/prevalence: DOM Jaccard-only FA 0.6667 misses param_header+cache 20/30, header/ETag-only FA 0.3333 misses dom_drift 10/30 — bounded rejection of single-channel detection, not broader C-FRESHNESS domain.

- No-guard always-EXECUTABLE as safe reuse: B-NO-GUARD FA 1.0 (30/30) Δ1.0 vs SPIDER 0.0 UNKNOWN 0 outside prevalence window — bounded rejection.

- Retrieval without patch as repair on synthetic: B-RETRIEVAL executed 0.0 (0/30) vs repair 1.0 Δ1.0≥0.30 — bounded rejection, not broader retrieval failure.

- No broader C-DELTA-REPAIR domain closed: multi-resource >1, cross-page, Redis, production CDN, real LLM heuristic not rejected by synthetic blast radius=1 test; this packet's parent MEASUREMENT_INVALID was operational failure not scientific falsification per EXPERIMENT_PACKET s9.

**Unknown (this experiment's target to resolve with honest instrumentation + health-gated single-node substrate):**

- Whether combined guard and deterministic patch transfer to health-gated single-node Flask 3.1.3/PyJWT 2.13.0 HS256 + nginx 1.24.0 $request_uri sticky substrate at n>=360 non-304 with identical thresholds — DEFERRED distributed n>=800 now pivoted to single-node; **this experiment's primary single-node gate.**

- Whether localized repair holds for blast radius 2-3 with true k-probe delta patch k*5 tokens and k browsers verified via _matches per id — **this experiment tests blast radius 2-3.**

- Whether same-resource contamination (<0.10 pooled <0.15 per family) holds for true second mechanism co-bound to same /resource/{id} with alternate required_slots re-verified on registry clone snapshot isolation after patch — **this experiment adds same-resource co-bound set N>=20 to make contamination falsifiable.**

- Whether verification discrimination AUROC>=0.75 precision>=0.80 at frozen 0.85 vs unclamped random-patch null generalizes with TRAIN18/TEST12 split and 1000 trajectory-grouped perms — **this experiment tests per k.**

- Whether honest per-trajectory-reset integer sum-counter economics with trajectory-grouped max|rho_shuffled|<0.20 and 5000 family-stratified bootstrap yields amortized Pareto M_total_f10 15<16 at f=10 — **this experiment measures honest counter.**

- Whether distributed n>=800 shared-WAL with distinct X-Worker-Pid>=2 survives identical thresholds — **DEFERRED until single-node gate passes honestly.**

- Whether honest M_total_f10 Pareto and blast radius economics preserve at f=100 and with real LLM token billing — not tested here, deferred to Product lane.

- Whether correlated latent non-determinism where DOM_before correlates with latent state determining S_next is detectable by this DOM+header/cache signal set — only independent deterministic orthogonal drifts tested.

- ETag change alone without max-age=0 boundary and 304 cached-body verification circularity without external oracle — untested.

**Do_not_assume (explicit non-conclusions, must be preserved):**

- Do not assume 15/15 repair success at 1.0 with cost 5/6/7 and contamination 0.0 and AUROC 1.0 and perm 0.40-0.60 in the parent packet are measured: they were hardcoded constants (parent V1 FAIL V2 FAIL V6 FAIL). This packet re-executes with actual nginx/gunicorn/WAL/_matches.

- Do not assume single health_gate pass with worker_pids [74102] proves nginx $request_uri sticky or Flask HS256 WAL substrate: single pid len<=2 was vacuous structural no-op. This packet deploys actual 2x gunicorn workers with distinct X-Worker-Pid>=2.

- Do not assume degenerate bootstrap CI [1.0,1.0] implies high-precision economics: on deterministic perfect detection bootstrap is degenerate ceiling, Wilson informative provides width; width>0 requires stochastic threshold or non-deterministic site.

- Do not assume M-SINGLE-REPAIR-COST-RATIO 0.1875 K2 and 0.1458 K3 proved locality: they under-reported by 4 and 8 tokens vs frozen k*5 model. This packet uses correct k*5 scaling.

- Do not assume contamination 0.0 on 20 disjoint ids proves same-resource isolation: blast radius=1 disjoint-id design was structural no-op; same-resource second mechanism on same mutated id untested. This packet adds same-resource co-bound set.

- Do not assume max|rho_shuffled| 0.0 validates honest counter: zero variance in deterministic constant cost vectors made rho vacuous. This packet uses per-trajectory-reset logged integer sums with actual execution.

- Do not assume verification AUROC 1.0 generalizes: hash-injected scores were parent manufacture. This packet uses binary _matches 1.0/0.0 with TRAIN18/TEST12 split.

- Do not assume MEASUREMENT_INVALID equals FALSIFIED-IN-SETTING for C-DELTA-REPAIR or closes synthetic path: prior synthetic SURVIVES remains EXPERIMENTAL; single-node remains UNKNOWN not REJECTED.

- Do not assume n_non304=1020 or M-STALE-N-SINGLE-K1=250 or M-FRESH-N=420 were frozen-count correct: summary showed contradictory counts. This packet reconciles exact frozen counts for bit-identical reproducibility.

- Do not promote C-DELTA-REPAIR or C-FRESHNESS to VALIDATED/PRODUCT_CORE on this evidence: graph lane synthetic only, honest single-node gate untested, same-resource contamination<0.10 unproven, distributed health_gate false. Requires audit PASS on this packet plus subsequent distributed n>=800 PASS plus real LLM/Playwright before PRODUCT_CORE.

---

## 4. State Representation

- **Raw observation (single-node primary, Flask/JWT+nginx):** HTTP response for `/resource/{id}` via nginx 1.24.0 $request_uri sticky to Flask 3.1.3 + gunicorn 23 (2 workers) backed by SQLite at /tmp/spider-runtime/single.db (pragma journal_mode=WAL, synchronous=NORMAL, shared TESTBED_SECRET HS256): flat JSON body 3-5 fields (id, name, email, plus optional phone/nickname deterministic), `ETag: SHA256(canonical_json_without_template)[:16]`, `Cache-Control: max-age=60` or `max-age=0`/`no-store`, `X-Csrf-Token` header, `X-Worker-Pid`/`X-Upstream` header exposing upstream for stickiness check, `WWW-Authenticate`/`Authorization: Bearer` HS256 JWT, and response-signaled template field `_template: {query_params: [...], header_names: [...]}`. Perturbation mutates exactly one local signal per mutated id: dom_drift (Jaccard 0.60-0.75), param_header_mutation (_template detail->uid + X-Csrf-Token abc123->xyz789), cache_expiry (ETag change + max-age 60->0). For NC-NOISE, server adds optional phone p=0.3 or nickname p=0.3 or email null p=0.2 as fresh noise. `If-None-Match: "<ETag>"` conditional GET returns 304 Not Modified when ETag matches and is marked not stale per V14 but counted for health_gate 304 operational; WAL file must be readable without lag. No external network, no LLM. Synthetic sanity uses identical schema on stdlib http.server 127.0.0.1 ephemeral port for regression check.

- **Derived freshness/repair state (per-trajectory observed cache, same frozen logic per substrate, honest):**
  - `dom_tokens_cached = sorted {(field_path,type)}` via `extract_field_types` from requests 1,2,3 per trajectory first valid frozen.
  - `header_tokens_cached = {Cache-Control, ETag, X-Csrf-Token}` from same observed requests; `header_tokens_live` from live response.
  - `endpoint_template_cached = {path + sorted(query_param_names) + sorted(header_names)}` extracted from observed response `_template`; `endpoint_template_live` from live response `_template`.
  - `jaccard_dom = |dom_tokens_cached ∩ dom_tokens_live| / |dom_tokens_cached ∪ dom_tokens_live|`; `etag_changed = (ETag_live != ETag_cached)`; `cache_expiry = (Cache-Control_cached max-age=60 AND live max-age=0)`; `param_template_changed = (endpoint_template_live != endpoint_template_cached)`.
  - Combined: `stale = (jaccard_dom <0.85) OR param_template_changed OR (etag_changed AND cache_expiry)`.
  - Repair trigger: if stale==True then patch = delta between live and cached response-derived signals per mutated id via re-observe k probes (k mutated ids), overwrite cache, rebind, re-verify via _matches.
  - **Confidence (recalibrated frozen):** 0.95 if stale==False, 0.85 if stale==True.
  - **Cost state (honest per-trajectory-reset constant integer sum-counter, FIXED per audit VF4):** cost_resolve=1, cost_bind=1, cost_verify=1, cost_freshness=1, cost_browser=0 fresh or 1 per repair probe per mutated id, cost_retrieval=1 per lookup, cost_distill=1 per distill. All integers, per-trajectory-reset logged per request/instance per substrate per k. No jitter/parity/bijective proxy/n*3200/f*6.0; browser steps 1 per repair probe only.
  - **Representation loss disclosed:** DOM tokens ignore value magnitudes/nested depth; ETag truncated 16 hex; endpoint template ignores param value semantics; per-trajectory cache 3 observations may miss rare optional fields; synthetic/single-node single resource flat-JSON only; repair deterministic re-observe, not LLM heuristic; verification exact _matches equality, not semantic utility; blast radius>1 tests exactly k mutated ids not cross-page workflow IR.

---

## 5. Action Representation

- **Intent:** `fetch_resource` with params `{resource_id}` on single resource `/resource/{id}` (blast radius>1: fetch k ids per instance via k sequential GETs on same trajectory).
- **Mechanism action_template:** `GET /resource/${resource_id}` with headers `{X-Csrf-Token: ${token}}` and query `?detail=${detail}`. For k>1, mechanism set contains k templates sharing same guard logic.
- **Execution (single-node + synthetic sanity):** `urllib.request` GET via nginx to Flask/JWT (single-node) or direct stdlib (synthetic sanity). Browser_steps deterministic 0 fresh /1 per mutated id repair probe. Conditional If-None-Match logic preserved. $request_uri sticky verified by X-Worker-Pid/X-Upstream.
- **Execution baselines:** B-COLD uses same urllib but empty registry discovery (3 fetches per id, 12+4=16 per resource scaled to k*16); B-NO-GUARD same execution but always EXECUTABLE; B-VERBATIM no probe cost 0; B-RETRIEVAL adds retrieval lookup cost 1 + replay via _matches; B-ORACLE uses ground-truth patch (k probes) as ceiling.
- **Verification:** `verify(mechanism_id, observed_state)` via `src/spider/kernel.py:_matches(required, actual)` exact equality on required_slots; deterministic, no LLM judge. All requests verified; scores binary 0/1 not hash-injected 0.78-0.99.
- **Repair patch executed (honest) per k:** For each stale instance with k mutated ids, execute re-observe fetch k probes, compute delta live vs cached response-derived signals per id, overwrite cache, rebind, call _matches per id; log success per instance (all k must verify true). Random-patch null: sample wrong-family value uniformly per mutated id, apply to clone, verify false.

---

## 6. Target, Unit of Analysis, and Sampling Policy

- **Target:** Localized repair efficacy per perturbation instance at each blast radius k∈{1,2,3}: binary repair success, cost, verification discrimination, contamination (disjoint and same-resource), amortized Pareto, freshness preservation on health-gated single-node substrate at n>=360 non-304.
- **Unit of analysis:** Single perturbation instance, grouped at trajectory/family level for inference (family-stratified trajectory-grouped bootstrap preserves within-family dependence per k). Freshness per request (single-node pool >=360 non-304), repair per instance (30 at k=1, 10 at k=2, 10 at k=3).
- **Sampling policy (frozen, no outcome-dependent adaptation):**
  - **Single-node primary server (health-gated):** Flask 3.1.3 + PyJWT 2.13.0 HS256 + nginx 1.24.0 $request_uri sticky on 127.0.0.1 ephemeral ports, SQLite at /tmp/spider-runtime/single.db (pragma journal_mode=WAL), TESTBED_SECRET HS256 shared, X-Worker-Pid/X-Upstream header exposed. 2x gunicorn 23 workers.
  - **Workload composition single-node:** Evaluated pool >=360 non-304 after excluding 304 (fresh 300-330 + stale 50 at K1-K3 + noise 150 = 500+ evaluated/530+ executed with 30 auxiliary pre-drift fresh). Stratified >=10 per family per blast radius k (K1 30 stale, K2 10, K3 10 total 50). Stale_rate in [0.00,0.18]∩[stale_rate±0.07]. Synthetic sanity unchanged 180 fresh+30 stale+150 noise=360 evaluated/390 executed.
  - **Drift families (orthogonal, single-resource per id, blast radius k):**
    1. `dom_drift`: Jaccard required-filtered {id,name,email} 0.60-0.75 <0.85 via id int->str + optional phone add per mutated id.
    2. `param_header_mutation`: mutation via response `_template` detail->uid and X-Csrf-Token abc123->xyz789 per mutated id.
    3. `cache_expiry`: ETag SHA256 change + max-age 60->0 per mutated id.
  - **Blast radius instantiation:** k=1: mutate 1 id (1001) per instance; k=2: mutate 2 ids (1001,1002) same family; k=3: 3 ids (1001,1002,1003). Synchronization via SQLite WAL immediate visibility; $request_uri sticky verified separately.
  - **Repair patch (deterministic, no LLM, executed) per k:** stale detected => re-observe k probes, delta live vs cached, overwrite cache, rebind, re-verify via _matches per id (all k must true).
  - **Random-patch null executed unclamped per k:** uniform random incorrect value per mutated id, verify via _matches (expected false), binary AUROC pooled per k, perm-shuffled label AUROC 1000 perms 0.40-0.60 unclamped.
  - **Retrieval baseline executed per k:** Jaccard 0.30 TFIDF retrieval over fresh caches, pick nearest, attempt replay via _matches without patch.
  - **Contamination sets per k:** Disjoint-id: N=20 distinct ids 9000-9019 never mutated, re-verified post-patch via _matches. Same-resource: N=20 second mechanisms co-bound to mutated ids (alternate required slot) re-verified post-patch via _matches on registry clone snapshot isolation. Both per k.
  - **Single-node health gate policy:** Before counting single-node metrics, run health probe: 10 GETs collect X-Worker-Pid/X-Upstream for $request_uri stickiness (same URI -> same upstream across 5 repeats), verify HS256 JWT on protected endpoint (200 with token, 401 without), verify SQLite file exists with pragma journal_mode=WAL, verify If-None-Match round-trip yields 304, verify immediate read-after-write. If any check fails => SINGLE_NODE_MEASUREMENT_INVALID with reason, synthetic sanity still adjudicated.

---

## 7. Holdout

- **Within-trajectory holdout (per-trajectory observed):** Fresh requests 1-5 per trajectory are cache source; stale requests 6-10 held out for detection+repair test per id. No overlap request_number between cache and test.
- **Train/test split for verification threshold:** Verification threshold (0.85) calibrated on TRAIN18 (6 per family at k=1) evaluated on TEST12 (4 per family at k=1) using binary _matches outcomes per substrate. No post-state leakage.
- **Cross-family holdout per k:** Each family 10 stale at k=1 held separately for per-family TP/repair success reporting; family-stratified trajectory-grouped bootstrap per k preserves family proportions.
- **Contamination holdout:** Unrelated sets disjoint ids 9000-9019 and same-resource co-bound ids never appear in training cache or perturbation pool.
- **Cross-substrate holdout:** Synthetic sanity cache not reused for single-node primary; single-node cache built from single-node fresh requests only.
- **No website holdout (single site):** Claim ceiling bounded to locally-hosted single-node single site; not C-CROSSSITE.

---

## 8. Nulls / Baselines (strong, matched tasks, all executed not hardcoded per substrate)

All baselines run on same workload per substrate (synthetic sanity 360/390; single-node >=360 non-304 stratified) for matched comparison with identical honest counter and deterministic _matches:

- **B-COLD-FULL-REEXPLORATION (primary cost baseline, executed per substrate per k):** Empty registry, rediscover from 3 observations per id, then execute. Must show success >=0.90 at full cost ~16 per resource (k*16) and 3 per resource browsers (k*3). Repair must beat by <50% tokens and <40% browser per k.

- **B-NO-GUARD-REPLAY (safety baseline, recomputed from logs per substrate):** No freshness guard, always EXECUTABLE, verbatim replay on stale pools per k. Must show FA~1.0 delta vs SPIDER >=0.15.

- **B-VERBATIM-REPLAY (0-cost replay, executed per k per substrate):** No repair probe, stored mechanism executed unchanged via _matches. Must show 0% success post-perturbation (proving perturbation breaking).

- **B-RETRIEVAL-RAG (strong retrieval, EXECUTED not hardcoded per k per substrate):** Jaccard 0.30 TFIDF retrieval over fresh caches, pick nearest, attempt replay via _matches (cost 1+4), no patch. Expected 0-40% success; repair must exceed by >=30pp.

- **B-JACCARD-ONLY / B-HEADER-ONLY (signal ablations, recomputed per substrate):** Only DOM Jaccard <0.85 ignores header/cache, or only header/cache ignores DOM. Expected FA~0.66 fails 2 families and FA~0.33 fails 1 family per substrate at k=1.

- **B-ORACLE-HAND-PATCH (ceiling, ground truth per k per substrate):** Ground-truth minimal patch (k probes+k verifies) 100% success. Measured repair should approach exactly 1.0x on synthetic and within 1.2x on single-node.

- **Positive control PC-LOCALIZED-REPAIR-SUCCEEDS (executed per substrate):** PC1 unperturbed 100% and PC2 oracle patch >=0.90 per family with cost ratio <0.50 at k=1; if fails => MEASUREMENT_INVALID.

- **Null controls executed per substrate:** NC-ZERO (zero perturbation cost 0 contamination 0), NC-RANDOM-PATCH unclamped per k (false_accept <=0.05, binary AUROC 1.0 pooled per k, perm-shuffled AUROC 0.40-0.60), NC-NOISE-IMMUNITY per substrate (150 churn noise FA<=0.10).

---

## 9. Primary Metrics & Decision Rule (frozen, honest single-node re-execution fixing all 9 parent required_fixes)

**Stable metric IDs (MUST be reused verbatim in result.json:metrics and controls per substrate; single-node metrics prefixed M-SINGLE-*, synthetic sanity M-SYNTH-*, or per-k suffix -K1/-K2/-K3):**

- `M-TN-SPIDER` / `M-SINGLE-TN-SPIDER` = TN/(TN+FP) on fresh pool (single-node >=180-300 fresh)
- `M-TN-WILSON-LOWER` / `M-SINGLE-TN-WILSON-LOWER` = Wilson lower z=1.96
- `M-FALSE-ACCEPT-SPIDER` / `M-SINGLE-FA-SPIDER` = # stale EXECUTABLE / stale_N (>=30 single-node k=1 pooled)
- `M-FALSE-ACCEPT-WILSON-UPPER` = Wilson upper for FA
- `M-UNKNOWN-RATE-SPIDER` / `M-SINGLE-UNKNOWN-RATE` = # UNKNOWN / staleness pool (~0.13-0.16)
- `M-ECE-SPIDER` / `M-SINGLE-ECE-SPIDER` global, `M-ECE-FRESH`, `M-ECE-STALE` per-class ECE recalibrated 0.95/0.85
- `M-REPAIR-SUCCESS-POOLED-K1` / `M-SINGLE-REPAIR-SUCCESS-POOLED-K1` = # repairs verify true /30 (k=1 pooled 10 per family)
- `M-REPAIR-SUCCESS-PER-FAMILY-{dom_drift,param_header_mutation,cache_expiry}-K1` + Wilson lowers per k
- `M-REPAIR-SUCCESS-POOLED-K2` / `-K3` = # repairs verify true /10 per k
- `M-REPAIR-COST-TOKENS-MEAN-K1` = mean honest sum-counter tokens per repair (5) and `M-REPAIR-COST-TOKENS-RATIO-K1` = repair / B-COLD_K1 (5/16=0.3125); bootstrap CI per k
- `M-REPAIR-COST-TOKENS-MEAN-K2` (expected 10) ratio 10/32=0.3125, `-K3` (expected 15) ratio 15/48=0.3125
- `M-REPAIR-BROWSER-MEAN-K1` =1 ratio 1/3=0.333, `-K2`=2 ratio 2/6=0.333, `-K3`=3 ratio 3/9=0.333
- `M-REPAIR-VERIFY-STEPS-MEAN-K1` per probe 1
- `M-CONTAMINATION-POOLED-DISJOINT` = # unrelated mechanisms false_accept after patch /20 pooled disjoint re-verified
- `M-CONTAMINATION-POOLED-SAME-RESOURCE` = # same-resource co-bound mechanisms false_accept after patch /20 pooled
- `M-CONTAMINATION-PER-FAMILY-DISJOINT` + `M-CONTAMINATION-PER-FAMILY-SAME` Wilson uppers per k
- `M-VERIFICATION-AUROC-K1` = AUROC binary _matches correct vs random on TEST per k (1.0 per k expected), `M-VERIFICATION-AUROC-RANDOM-PERMUTED-K1` = perm-shuffled label AUROC 0.40-0.60 unclamped per k, `M-VERIFICATION-PRECISION-K1` at frozen 0.85, `M-VERIFICATION-RECALL-K1`, `M-VERIFICATION-PASS-CORRECT-K1`=30/30 k=1 10/10 k=2,3
- `M-AMORTIZED-COST-F10-K1` =15 tokens vs `M-COLD-COST-F10-K1`=16, `M-AMORTIZED-BROWSER-F10-K1`=1 vs 3; scaled K2: 20 vs 32 browser 2 vs 6; K3: 25 vs 48 browser 3 vs 9
- `M-RHO-SHUFFLED-MAX` / `M-SINGLE-RHO-SHUFFLED-MAX` max|rho| 1000 trajectory-grouped perms primary <0.20 per substrate
- `M-COST-VECTOR-STD` 0 per stratum, `M-WITHIN-FAMILY-STD-MIN-FRESHNESS` 0.5 per family per k
- Baselines per substrate: `M-FA-B-NO-GUARD`, `M-SUCCESS-B-VERBATIM`, `M-SUCCESS-B-RETRIEVAL-RAG-K1`, `M-FA-B-JACCARD-ONLY`, `M-FA-B-HEADER-ONLY`, `M-ORACLE-COST-K1`, `M-COLD-COST-TOKENS-MEAN-K1`
- Bootstrap per substrate per k: 5000 family-stratified trajectory-grouped 95% percentile CIs for all primary metrics
- Health gate metrics: `M-HEALTH-GATE-PASS-SINGLE` bool, `M-N-SINGLE-NON304`, `M-X-WORKER-PIDS-SINGLE` distinct set, `M-JWT-VERIFY-PASS-SINGLE`, `M-304-OPERATIONAL-SINGLE`, `M-WAL-EXISTS-SINGLE`, `M-WAL-MODE-SINGLE`, `M-STICKY-CONSISTENT-SINGLE`
- Counts: `M-FRESH-N-SINGLE`, `M-STALE-N-SINGLE-K1`, `M-NOISE-N-SINGLE`

**Frozen decision rule (satisfies all 9 parent audit required_fixes + new blast radius + same-resource, single-node):**

- **PRIMARY SURVIVES_CURRENT_TEST iff ALL D1-D13 hold** per spec.json:decision_rule (health_gate true n_non304>=360, synthetic sanity PC1 1.0 PC2>=0.90, single-node PC1 1.0 PC2>=0.90, NCs pass unclamped, freshness TN>=0.85 Wilson lower>0.75 FA<=0.10 UNKNOWN/ECE, repair success >=0.80 pooled >=0.70 per family at k=1,2,3, tokens <0.50 browser <0.40 per k, contamination <0.10 pooled <0.15 per family on BOTH disjoint and same-resource sets per k, verification AUROC>=0.75 precision>=0.80 at 0.85 per k perm null 0.40-0.60, amortized <cold_k at f=10 per k, no-guard delta>=0.15 and single-signal ablations fail >=1 family, honesty V2-V6 pass).
- **FALSIFIED-IN-SETTING if any D5-D12 fails while D1-D4 and D13 pass** (valid scientific negative on single-node transfer or blast radius locality or same-resource isolation with identical thresholds).
- **MEASUREMENT_INVALID if any D1-D4 or D13 honesty fails or N per family <10 per k or unrelated N<20 or any control hardcoded/clamped/rigged or health_gate synthetic sanity regression.**
- **SINGLE_NODE_MEASUREMENT_INVALID if health_gate false or n_non304<360 or WAL false or HS256 mismatch or 304 not operational or $request_uri sticky inconsistent — does not retroactively falsify synthetic PRIMARY; synthetic sanity SURVIVES preserved.**
- **MIXED if family-heterogeneous or k-heterogeneous.**
- **INCONCLUSIVE only if primary CIs straddle thresholds with width>0.20 due to underpower at n per k=10.**

Recalibration satisfiability proof frozen: With single-node 300 fresh at 0.95 and 50 stale at 0.85 (14% stale) plus 150 noise considered outside staleness pool? Staleness pool 350 stale_rate 0.142, global ECE 0.07 <0.15, UNKNOWN ~0.14 within [0.00,0.18] and stale_rate±0.07; repair cost 5 vs cold 16 ratio 0.3125<0.50 browser 1 vs 3 ratio 0.333<0.40 satisfiable scaled to k.

---

## 10. Uncertainty Method

- **Wilson CI** for proportions (TN, TP, FA, repair success per k, contamination per set per k, precision) z=1.96 raw counts; lower for TN/success, upper for FA/contamination; at n=10 per family per k disclose exact Wilson (7/10 lower 0.39, 9/10 lower 0.60, 0/20 upper 0.161 per set), at pooled 24/30 lower 0.65, 0/30 upper 0.1135.
- **Trajectory-grouped family-stratified bootstrap (B=5000) per substrate per k:** resample with replacement at trajectory level per substrate per k, stratified by family preserving proportions, recompute TN, FA, UNKNOWN, ECE, repair success per k, token/browser ratios per k, contamination per set per k, AUROC per k per resample → percentile 95% CI. Non-degeneracy required: width>0; degenerate [1.0,1.0] flagged as ceiling effect (audit VF7), Wilson provides informative width.
- **Honesty null per substrate:** max|rho_shuffled| via 1000 perms trajectory-grouped (shuffle whole trajectory blocks' cost vectors vs outcomes); report max primary <0.20 per substrate and mean auxiliary.
- **Verification AUROC uncertainty per k:** From binary _matches outcomes per k, compute AUROC via binary predictions (correct 1 vs random 0) giving 1.0 per k; report Hanley-McNeil/DeLong bootstrap 5000 CI disclosure noting degenerate zero variance yields CI [1.0,1.0] but permutation-shuffled null 0.40-0.60 per k as discriminant proof.

---

## 11. Falsification / Survival Rule

- Positive `PRIMARY SURVIVES` upgrades bounded ceiling from synthetic freshness/repair EXPERIMENTAL (blast radius=1 degenerate bootstrap) to health-gated single-node Flask HS256 + nginx $request_uri sticky EXPERIMENTAL with honest instrumentation per k and proven same-resource isolation (executed PC/NC, unclamped null, trajectory-grouped rho, honest D11 scaled, disjoint vs same-resource contamination) contamination-bound localized repair (<50% tokens, <40% browser, AUROC>=0.75, contamination<0.10 re-verified both sets, amortized Pareto at f=10 per k). Validates that freshness guard enables contamination-bound repair beyond structural no-op and survives single-node HS256/nginx/304 and multi-resource coupling and unblocks distributed n>=800 for next pulse. Does NOT promote to VALIDATED/PRODUCT_CORE.

- Negative `FALSIFIED-IN-SETTING` (honest gates passing and health-gated n>=360): even behind identical synthetic-validated guard, localized repair fails at least one condition. Demonstrates synthetic stdlib SURVIVES does not imply single-node robustness. Product must NOT ship delta-repair as VALIDATED; reuse remains EXPERIMENTAL synthetic-only, must default to full re-exploration and budget repair as cold_k cost. Blocks C-DELTA-REPAIR/C-FRESHNESS VALIDATED promotion and forces orthogonal levels before re-attempt. Bounded to this single-node signal/threshold/site/confidence/blast-radius; does NOT close synthetic path (still SURVIVES) nor broader C-DELTA-REPAIR domain (Redis, production CDN, real LLM).

- `MEASUREMENT_INVALID` / `SINGLE_NODE_MEASUREMENT_INVALID` / `MIXED` / `INCONCLUSIVE` per §9 decision rule: infrastructure or manufactured failure distinct from scientific falsification per research/EXPERIMENT_PACKET.md s9; does not constitute evidence for broader domain.

---

## 12. Validity Threats and Representation Loss

- **Threats closed by design:** hash-injected verification (0.78-0.99 vs 0.10-0.50), clamped permutation null 0.4803, hardcoded PC/NC/retrieval 0.30, rigged D8 with *4, bijective n*3200/f*6.0/parity tautology — all fixed to binary _matches 1.0/0.0 unclamped executed controls and honest per-trajectory-reset constant sum-counter with trajectory-grouped max|rho|<0.20 per substrate per k. Stub SyntheticHandler static body and hardcoded baseline constants — replaced by live response-derived mutation. All 9 parent audit required_fixes addressed: (1) actual nginx 1.24.0 $request_uri sticky conf, (2) actual _matches verification via src/spider/kernel.py, (3) correct k*5 token scaling (10/15 not 6/7), (4) honest per-trajectory-reset integer sum-counter, (5) trajectory-grouped 1000 perms/5000 bootstraps, (6) TRAIN18/TEST12 split, (7) same-resource co-bound contamination N>=20, (8) health-gated single-node substrate, (9) frozen count reconciliation.

- **Remaining threats disclosed:** deterministic perfect detection yields degenerate bootstrap ceilings [1.0,1.0]/[0.0,0.0] Wilson informative but bootstrap width 0 is ceiling effect not precision (VF9); cost std 0 trivializes rho to 0 via zero variance (tests only no injected variance, not graded M_total discrimination per VF9); ETag truncation 16 hex, DOM tokens ignore value magnitudes/nested depth, endpoint template ignores param value semantics, per-trajectory cache 3 observations may miss rare optional fields, synthetic/single-node single resource flat-JSON not production CDN/session/CDN depth, 304 cached-body circularity not independently validated with external oracle, ETag AND max-age=0 untested alone, required-path-filter noise immunity tautological, correlated latent non-determinism untested, real LLM token billing and Playwright execution untested, f=100 amortization untested, single-node $request_uri sticky with 2 workers is near single-process — does not test concurrent WAL propagation or distinct X-Worker-Pid>=2 which remains for distributed.

- **Site/representation scope:** bounded to locally-hosted Flask 3.1.3/PyJWT 2.13.0 HS256 + nginx 1.24.0 $request_uri sticky 2x gunicorn 23, 127.0.0.1, flat JSON, 3 perturbation families, SQLite file WAL; not SPA DOM, not workflow IR, not production CDN, not C-CROSSSITE.

---

## 13. Consequences

**If SURVIVES (positive):** Upgrades C-DELTA-REPAIR (and dependent C-FRESHNESS) from narrow synthetic EXPERIMENTAL to health-gated single-node EXPERIMENTAL with honest economics and proven same-resource isolation at blast radius 1-3. Unblocks: (a) authorization for next-pulse distributed n>=800 shared-WAL health-gated validation; (b) authorizes Graph to proceed to honest C-RESIDUAL-NOVELTY M_total_f10 Pareto at f=10/100; (c) hardens Runtime single-node health gate for Intel/Frontier. Does NOT promote to VALIDATED/PRODUCT_CORE — requires audit PASS on this packet plus subsequent distributed n>=800 PASS plus real LLM/Playwright billing before PRODUCT_CORE.

**If FALSIFIED-IN-SETTING (negative with honest gates):** Proves localized repair is artifact of stdlib single-process radius=1 or fails same-resource isolation or multi-resource coupling even at single-node. Product must NOT ship delta-repair as VALIDATED; reuse remains EXPERIMENTAL synthetic-only, must default to full re-exploration and budget repair as cold_k cost. Blocks C-DELTA-REPAIR/C-FRESHNESS VALIDATED promotion and forces orthogonal levels before re-attempt. Bounded to this signal/threshold/site/confidence/blast-radius/single-node; does NOT close synthetic path (still SURVIVES) nor broader C-DELTA-REPAIR domain.

**If SINGLE_NODE_MEASUREMENT_INVALID:** Infrastructure failure — not falsification; synthetic sanity SURVIVES preserved; retry after Runtime hardens single-node substrate. Distributed remains UNKNOWN; no product promotion.

---

*Design frozen pre-outcome: no outcome-bearing measurements inspected. EXECUTE must execute exactly this frozen design with actual nginx 1.24.0 + 2x gunicorn 23 Flask 3.1.3 PyJWT HS256 + WAL + _matches instrumentation, preserve RAW EVIDENCE vs OBSERVATION vs DERIVED MEASUREMENT distinction, log all V13 artifacts with SHA256, use stable metric/control IDs, and distinguish measurement failure from scientific negative per research/EXPERIMENT_PACKET.md.*
