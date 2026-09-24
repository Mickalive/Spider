# EXP-GRAPH-35949562506 — Preregistration (DESIGN frozen pre-outcome)

**Lane:** graph  
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally (next_gate: controlled local perturbations with repair cost and contamination bounds)  
**Experiment ID:** EXP-GRAPH-35949562506  
**Director mandate:** REOPEN C-DELTA-REPAIR (action=REOPEN, parent_handoff_disposition=USE, cognitive_reset=false, dependencies=[runtime]) per `request.json:director_mandate` — comparative reasoning: vs immediate distributed VALIDATED (n>=800 shared-WAL HS256) rejected because runtime 51-exp distributed block predicts degenerate MEASUREMENT_INVALID [1.0,1.0] CI; vs WebGym param-inherit single-family A->B pilot (8 consecutive MEASUREMENT_INVALID, kernel durability fails) lower readiness; synthetic delta-repair has highest readiness/centrality. `inherited_next_question` advisory, `director_mandate.question` binding per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2.  
**Parent handoff:** `research/experiments/EXP-GRAPH-35947468747/handoff.json` (SHA 0188c57f4c7a0a597c2389f4a07aa17e33d5fc855d772fc546c2d15c6eff2704, verdict SURVIVES_CURRENT_TEST) — preserved as continuity evidence only per `director_mandate.parent_handoff_disposition=USE`; not automatic agenda.  
**Frozen hashes:** request `9a4d8c26ee34fceae17a87b8d77a85ea032323bcef8bf10e6e3b65413a93849e`, claim registry `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b` — design must not inspect outcome data.

---

## 1. Strategic Question → Falsifiable Question

**Director strategic question (verbatim request.json:director_mandate.question):**

> Does the validated synthetic-rebalanced freshness guard (Jaccard 0.85 required-filtered {id,name,email}+response-derived endpoint _template/X-Csrf-Token+ETag+max-age=0, recalibrated 0.95 fresh/0.85 stale with TN>=0.85 Wilson lower>0.75 FA<=0.10 ECE<=0.15 at 15% stale 360-req=180 fresh+30 stale+150 noise, NC-NOISE-IMMUNITY FA<=0.10) enable bounded C-DELTA-REPAIR on the same locally-hosted single-resource flat-JSON substrate (/resource/{id} stdlib http.server, deterministic _matches verification, honest per-trajectory-reset constant sum-counter resolve+bind+verify+freshness+browser_steps without jitter/n*3200/f*6.0, trajectory-grouped max |rho_shuffled|<0.20, 5000 bootstrap) such that a controlled single-resource perturbation (DOM attribute/text, endpoint param/header, Cache-Control/ETag one resource only) requires localized repair with delta cost <50% and browser interactions <40% vs cold re-exploration, verification AUROC>=0.75 precision>=0.80, contamination<0.10, and honest M_total_f10 Pareto not inflated, vs no-guard baseline, before authorizing health-gated distributed shared-WAL transfer (n>=800 non-304, X-Worker-Pid>=2)?

**Falsifiable refined question (this prereg — smallest high-information test):**

> On the identical locally-hosted synthetic single-resource `/resource/{id}` stdlib http.server flat-JSON substrate with the same deterministic guard (Jaccard 0.85 required-filtered {id,name,email}+response-derived _template/X-Csrf-Token+ETag+max-age=0, recalibrated 0.95 fresh/0.85 stale) and honest per-trajectory-reset constant integer sum-counter (resolve+bind+verify+freshness base 4 fresh /5 repair, browser_steps 0/1, no jitter/n*3200/f*6.0/parity/bijective proxy, trajectory-grouped max|rho_shuffled|<0.20, 5000 family-stratified trajectory-grouped bootstrap, deterministic src/spider/kernel.py _matches), does a controlled single-resource perturbation — dom_drift (field-set Jaccard 0.60-0.75 <0.85), param_header_mutation (response _template detail->uid + X-Csrf-Token rotation), cache_expiry (ETag+max-age 60->0) — 10 instances per family (30 total), require only localized deterministic repair (re-observe 1-3 per-trajectory cache update + rebind + re-verify, 1 browser probe) achieving repair success >=80% pooled >=70% per family, mean cost <50% tokens-equiv and <40% browser vs B-COLD, verification AUROC>=0.75 precision>=0.80 vs random-patch null, contamination<0.10 on N>=20 unrelated mechanisms, amortized cost at n_reuses=10 < cold, while sustaining freshness TN>=0.85 FA<=0.10 UNKNOWN/ECE at 15% prevalence and beating B-NO-GUARD delta>=0.15 and single-signal ablations, vs matched cold/verbatim/retrieval baselines?

Design is the smallest high-information test that can change C-DELTA-REPAIR claim/product decision per Director rationale; it does NOT repeat the 8 prior WebArena param-inherit pilots nor immediate degenerate distributed VALIDATED, and leverages the sole synthetic SURVIVES (EXP-GRAPH-35947468747) without requiring health-gated WAL.

---

## 2. Hypothesis

**H1 (positive):** Synthetic-rebalanced freshness SURVIVES translates to bounded delta-repair: with the combined guard, per-trajectory observed caching, response-derived endpoint, honest constant integer sum-counter and trajectory-grouped max|rho|<0.20, a single-resource local perturbation is repairable by a localized deterministic patch (delta = re-observe cache + rebind + re-verify, 1 probe) without full re-exploration. Expected: (a) repair success >=0.80 pooled (24/30) and >=0.70 per family (7/10) with family-stratified bootstrap lower >0.60; (b) mean repair tokens-equiv <0.50*B-COLD (e.g., 5 vs 16 units) and browser <0.40*B-COLD (1 vs ~3 probes) verify steps <=2; (c) verification discriminates correct patch vs random-patch null: AUROC>=0.75 precision>=0.80 at frozen 0.85 threshold (TRAIN-calibrated 18, TEST 12), random AUROC 0.40-0.60 delta >=0.25; (d) contamination <0.10 pooled (<=2/20) Wilson upper <0.20; (e) amortized repair+verify+10*retrieval (M_total_f10) < cold honest sum-counter, trajectory-grouped max|rho|<0.20 preserved (no tautology), M_total not inflated vs cold; (f) freshness TN 1.0 Wilson lower ~0.979 FA 0.0 upper 0.1135 still holds, discriminating vs B-NO-GUARD FA 1.0 delta>=0.90 and vs B-JACCARD-ONLY/B-HEADER-ONLY fails >=1 family. Orthogonal necessity (DOM+header/cache combined) explains detection, not pooled-metric salience.

**H0 (null):** Bounded locality fails while honesty gates pass: any primary D3-D9 fails — repair success <0.80 pooled or <0.70 per family, cost ratio >=0.50 tokens or >=0.40 browser, verification AUROC<0.75/precision<0.80, contamination>=0.10, amortized not cheaper than cold, or freshness degrades to TN<0.85 FA>0.10 at 15% prevalence, or no FA delta vs no-guard. Valid scientific negative. Honesty gates trigger MEASUREMENT_INVALID if constant counter, trajectory-grouped max rho, 5000 bootstrap, per-trajectory caching, or response-derived signals violated — distinct from falsification.

**Prior expectations used (director_mandate.agent_priors_used, labeled as prior not SPIDER evidence):** (1) long-horizon path-dependent salience pollution — single next-step PMI misses correlated-session dynamics, requires trajectory-grouped permutation and correct-family gating; (2) thresholded fingerprint caching trades correctness for speed, requires calibrated UNKNOWN/ECE<=0.15 else false_accept dominates — distinguished from SPIDER 0.95/0.85 recalibration and Jaccard 0.85+ETag partial mitigation; (3) parameterization only transfers when alias families orthogonal Jaccard<0.30 — distinguished from 8 MEASUREMENT_INVALID param-inherit pilots; (4) O(1) tool/API bypass dominates O(MxN) browsing when manifest normalized — distinguished from WebMCP Frontier mixed ceiling; (5) measurement degeneracy at ceiling 1.0 CI [1.0,1.0] signals insufficient diversity, requires heterogeneous |S|>=16 and 2000 bootstrap — distinguished from runtime 1.0 ceiling blocked gradients. These priors motivate honest sum-counter, trajectory-grouped rho, family-stratified bootstrap, and deferring distributed VALIDATED.

---

## 3. Continuity vs Director Supersede — Preservation of Established/Rejected/Unknown/Do_not_assume

This section explicitly preserves the four-way distinction from `EXP-GRAPH-35947468747/handoff.json:carry_forward` per transmission discipline; `director_mandate.question` is followed as binding direction, parent `next_question` not silently overridden but harmonized (USE disposition, REOPEN narrow delta-repair while retaining synthetic substrate).

**Established (preserved verbatim, not re-tested as hypothesis):**

- Bounded synthetic-rebalanced EXPERIMENTAL ceiling ONLY: locally-hosted stdlib http.server flat-JSON single-resource /resource/{id} (127.0.0.1 ephemeral, execution 210 fresh+30 stale=240 staleness pool +150 noise=390 total; spec expected 180 fresh+30 stale=210+150=360, stale_rate actual 0.125 expected 0.1428 both within [0.0928,0.18]) with deterministic orthogonal drifts — dom_drift Jaccard required-filtered {id,name,email} 0.5 <0.85 (id int->str + phone), param_header_mutation response-derived _template detail->uid + X-Csrf-Token abc123->xyz789, cache_expiry ETag SHA256(filtered_body)[:16] changed + Cache-Control max-age 60->0 with deterministic If-None-Match 304 marked not stale — guard Jaccard<0.85 OR param_template_changed OR (etag_changed AND max-age=0) with recalibrated 0.95 fresh/0.85 stale achieves M-TN-SPIDER 1.0 Wilson lower 0.982 (210/210, stable 180/180 lower 0.9791, per-family 10/10 lower 0.7225), M-FALSE-ACCEPT 0.0 Wilson upper 0.1135 (0/30) per-family TP 1.0 (10/10 each), audited PASS recomputed_metrics match producer. Extra 30 fresh are pre-drift requests 1-5 from 6 stale trajectories (2 per drift family) necessary for V5/V14, disclosed and within prevalence tolerance.
- Calibration at satisfiable recalibrated operating point: UNKNOWN 0.125 (30/240) Wilson [0.089,0.1728] within prevalence-aware [0.00,0.18] and within actual [0.075,0.195] and expected [0.0928,0.18], global ECE 0.0625 per-class fresh 0.05 stale 0.15 <=0.15 (proof at actual prevalence 210*0.05/240=0.0438+30*0.15/240=0.0188=0.0625, only bins [0.8,0.9] n30 stale conf0.85 and [0.9,1.0] n210 fresh conf0.95 populated), Wilson CIs non-degenerate width>0 (TN width 0.018, FA width 0.1135, UNKNOWN width 0.083) but bootstrap 5000 family-stratified trajectory-grouped CIs degenerate [1.0,1.0]/[0.0,0.0] width 0 — ceiling effect not precision, requires stochastic threshold/non-deterministic site for width>0, validated via within-family freshness std 0.5 >0.
- Signal isolation necessity replicated at sparsity: ablations prove combined DOM+header/cache signal required — B-JACCARD-ONLY FA 0.6667 TP 10/30 only dom_drift, B-HEADER-ONLY FA 0.3333 TP 20/30 (param_header+cache) misses dom_drift, B-NO-GUARD FA 1.0 delta 1.0 >=0.15 vs SPIDER 0.0, NC-NOISE-IMMUNITY FA 0.0 TN 1.0 on 150 noise (50 per churn variant A phone, B nickname, C email null+phone; required-path filter {id,name,email} excludes optional phone/nickname, ETag alone without max-age=0 not flagged). Audit baseline_findings confirm orthogonality.
- Measurement-validity fixes verified at rebalanced prevalence: V1 deterministic src/spider/kernel.py _matches exact equality, V2 honest constant integer sum-counter base 4 per request total 1560 all_int true vector std 0 valid per V2 narrowing exempt from V5, V3 no jitter/parity/f*6.0/n*3200/bijective proxy, V4 trajectory-grouped max|rho_shuffled| 0.0 <0.20 via 1000 whole-trajectory-block perms, V5 within-family freshness std 0.5 >0 (cost exempted), V6 5000 family-stratified trajectory-grouped bootstrap, V7 Wilson z=1.96, V8 recalibrated ECE+UNKNOWN satisfiable, V14 per-trajectory observed caching 33 trajectories first valid of 1-3 + response-derived endpoint, V-DIST correctly flagged MEASUREMENT_INVALID not falsification.
- Honest economics channel at rebalanced sparsity: per-trajectory-reset constant sum-counter with trajectory-grouped max|rho| closes prior n*3200/f*6.0/parity tautology and mean-vs-max misreporting; max|rho| 0.0 and observed rho 0.0 demonstrate no cost-outcome tautology injected, but constant cost makes rho trivially 0 (gate tests only no injected variance, not graded cost discrimination) per audit validity_findings; within-family freshness std 0.5 satisfies discrimination gate while cost std 0 exempted.

**Rejected (must NOT be cited as support; explicitly rejected):**

- Single-signal guards as standalone detectors at 0.85 threshold / 12.5% prevalence on this signal/site: DOM Jaccard-only FA 0.6667 and header/ETag-only FA 0.3333 insufficient — bounded rejection of single-channel detection at sparsity, not broader C-FRESHNESS domain (session/token/CDN, other thresholds, workflow IR levels per prior 6).
- No-guard baseline as safe reuse: B-NO-GUARD FA 1.0 delta 1.0 vs SPIDER 0.0 on 12.5% stale pool, UNKNOWN 0 outside [0.0928,0.18] — bounded rejection of always-EXECUTABLE, not general reuse claim.
- No bounded hypothesis rejected for C-FRESHNESS calibration/detection beyond this synthetic signal/threshold/site/prevalence/confidence: parent D3/D4 specification impossibilities replaced by satisfiable prevalence-aware bounds; does not close orthogonal workflow IR/endpoint catalog levels or production CDN/304/session rotation.
- Any inference that deterministic perfect detection at 12.5% implies non-degenerate bootstrap precision or distributed/WAL/session robustness — ceiling effect disclosed, not precision; distributed transfer remains untested.
- Single-signal repair sufficiency and zero-contamination without verification — bounded to synthetic 36-instance simulation ceiling (prior EXP-GRAPH-35741890679): pooled TEST 0.944 CI [0.742,0.990], token ratio 0.613 CI [0.569,0.661] failing <0.50, browser 0.431 failing <0.40, amortized 2.1x cold failing, AUROC 1.0 artefactual perfect separation, contamination 0.0046 hardcoded — that ceiling is simulation-only, not product evidence.

**Unknown (this experiment's target to resolve):**

- Whether localized delta-repair (repair success >=80% pooled >=70% per family, cost <50% tokens <40% browser, AUROC>=0.75 precision>=0.80, contamination<0.10, amortized < cold at f=10) holds on same synthetic substrate with honest constant counter and trajectory-grouped max|rho|<0.20 behind health-gated verification — **PRIMARY unknown, this experiment tests it** (prior handoff unresolved: C-DELTA-REPAIR untested after synthetic-rebalanced gate).
- Whether honest C-RESIDUAL-NOVELTY M_total_f10 Pareto (M_total = retrieval+distill+resolve+bind+verify+freshness+browser honest sum-counter over f=10/100, trajectory-grouped max|rho_shuffled|<0.20 vs Stagehand/RAG/TERX baselines) holds with honest counter — **secondary unknown, measured as M_total aggregation in same workload but not requiring separate WebArena census** (honest Pareto gate included as D8).
- Whether guard sustains non-degenerate 5000 family-stratified trajectory-grouped bootstrap CIs (width>0) with deterministic repair cost strata — current deterministic perfect detection yields degenerate ceilings; disclosure required per V7.
- Whether guard transfers to health-gated distributed shared-WAL Flask/JWT + nginx If-None-Match/304 substrate at n>=800 non-304 (single-node first, then 2x gunicorn+nginx HS256, distinct X-Worker-Pid>=2) with identical thresholds — **unknown but DEFERRED, not in this packet** per Director PARK and dependencies; runtime must harden before VALIDATED.
- Whether ETag change alone without max-age=0 (etag_changed AND max-age=0 boundary) should be flagged stale — AND logic untested; cache_expiry family tests only combined condition.
- Whether required-path-filter noise immunity ({id,name,email}) generalizes beyond optional-field churn — tautological by design.
- Whether per-trajectory cache using first valid of 3 misses rare optional fields in non-deterministic settings — mitigated by deterministic fresh generation.

**Do_not_assume (explicit non-conclusions):**

- SURVIVES at 12.5% stale deterministic synthetic (TN 1.0 FA 0.0) implies TN>=0.85 FA<=0.10 for delta-repair contamination<0.10 or for production Flask/JWT/WAL/CDN — prevalence, operational 304, and repair scope change operating point; repair locality not entailed by detection.
- Degenerate bootstrap CIs [1.0,1.0] TN, [0.0,0.0] FA, [0.125,0.125] UNKNOWN imply high-precision repair — they reflect deterministic ceiling, not precision; informativeness requires Wilson (TN lower 0.982, FA upper 0.1135) or stochastic site/threshold.
- Recalibrated 0.95/0.85 yielding ECE 0.0625 demonstrates general calibration — only 2 bins populated, per-class stale 0.15 at threshold tautological bound.
- Constant sum-counter 4 per request with max|rho| 0.0 proves honest M_total_f10 discriminates residual novelty — rho trivially 0 because cost variance 0 within strata (fresh vs repair); gate tests no jitter only, not graded cost discrimination; amortized Pareto gate required.
- _matches verified True 390/390 implies learned distill_parameterized validation — tautological self-consistency, not param induction.
- Combined guard necessity via ablations implies orthogonal workflow IR levels unnecessary — Director prior 6 requires orthogonal levels have higher information gain than threshold family; this tests only Jaccard+header/cache, not workflow IR etc.
- C-DELTA-REPAIR SURVIVES on synthetic implies VALIDATED/PRODUCT_CORE or distributed readiness — claim remains EXPERIMENTAL bounded to deterministic single-resource patch; requires n>=800 health-gated distributed shared-WAL + real LLM/Playwright + audit PASS before promotion; WebArena-Verified v2 param-inherit pilots remain PARKED.
- Any MEASUREMENT_INVALID equals FALSIFIED-IN-SETTING — distinct per transmission discipline; honest-cost failure is infra, not locality falsification.
- Successfully repairing one resource implies multi-resource or cross-page repair — single-resource only, blast radius=1, unaffected mechanisms N>=20 required.

---

## 4. State Representation

- **Raw observation (synthetic primary, stdlib http.server):** HTTP response for `/resource/{id}`: flat JSON body 3-5 fields (id, name, email, plus optional phone/nickname), `ETag: SHA256(canonical_json_without_template)[:16]`, `Cache-Control: max-age=60` or `max-age=0`/`no-store`, `X-Csrf-Token` header, and response-signaled template field `_template: {query_params: [...], header_names: [...]}` server emits for response-derived endpoint detection. Perturbation mutates exactly one local signal per instance: dom_drift changes field-set (id int->str, add phone), param_header_mutation rotates _template detail->uid and X-Csrf-Token value, cache_expiry flips ETag+max-age 60->0. For NC-NOISE, server adds optional phone/nickname p=0.3 or email null p=0.2 as fresh noise. No external network, no LLM.
- **Derived freshness/repair state (per-trajectory observed cache, same as parent):**
  - `dom_tokens_cached = sorted {(field_path,type)}` via `extract_field_types` (types string/integer/boolean/array/object) from requests 1,2,3 per trajectory first valid frozen.
  - `header_tokens_cached = {Cache-Control, ETag, X-Csrf-Token}` from same observed requests; `header_tokens_live` from live response.
  - `endpoint_template_cached = {path + sorted(query_param_names) + sorted(header_names)}` extracted from observed response `_template` (response-derived); `endpoint_template_live` from live response `_template`.
  - `jaccard_dom = |dom_tokens_cached ∩ dom_tokens_live| / |dom_tokens_cached ∪ dom_tokens_live|; etag_changed = (ETag_live != ETag_cached); cache_expiry = (Cache-Control_cached max-age=60 AND live max-age=0); param_template_changed = (endpoint_template_live != endpoint_template_cached)` exact set equality on response-derived names.
  - Combined: `stale = (jaccard_dom <0.85) OR param_template_changed OR (etag_changed AND cache_expiry)` threshold 0.85 frozen.
  - Repair trigger: if `stale==True` (UNKNOWN 0.85) then patch = delta between live and cached response-derived signals (field-set diff, _template diff, ETag diff) applied via re-observe update: re-fetch 1 probe from live endpoint, overwrite cached dom/header/endpoint with live-derived values, rebind mechanism via deterministic template, re-verify via _matches.
- **Confidence (recalibrated frozen):** `0.95` if `stale==False` (EXECUTABLE fresh/no repair), `0.85` if `stale==True` (UNKNOWN stale flagged/repair triggered). No 0.50 for correct stales.
- **Cost state (honest per-trajectory-reset constant sum-counter):** `cost_resolve`=1, `cost_bind`=1, `cost_verify`=1, `cost_freshness`=1, `cost_browser`=0 fresh or 1 repair probe, `cost_retrieval`=1 per lookup, `cost_distill`=1 per distill (synthetic distill is literal template capture, not LLM param induction). All integers, per-trajectory-reset (trajectory block sum, not global), logged per request/instance. No jitter/parity/bijective proxy.
- **Representation loss disclosed:** DOM tokens ignore value magnitudes/nested depth beyond flat keys; ETag truncated to 16 hex; endpoint template ignores param value semantics; per-trajectory cache 3 observations may miss rare optional fields; synthetic single resource flat-JSON only, not production DOM/session/CDN depth; repair is deterministic re-observe, not LLM heuristic reasoning; verification is exact _matches equality, not semantic utility.

---

## 5. Action Representation

- **Intent:** `fetch_resource` with params `{resource_id}` on single resource `/resource/{id}`.
- **Mechanism action_template:** `GET /resource/${resource_id}` with headers `{X-Csrf-Token: ${token}}` and query `?detail=${detail}` (param template). Literal mechanism via SPIDER kernel `distill` literal; `distill_parameterized` not under test for repair.
- **Execution (synthetic):** stdlib `urllib.request` GET to `http://127.0.0.1:{port}/resource/{id}?detail={detail}` with `X-Csrf-Token`. Browser_steps deterministic 0 fresh /1 repair probe (re-observe fetch), retained for honest counter. Conditional `If-None-Match` logic preserved but 304 not triggered on synthetic (deterministic ETag, marked handling).
- **Execution baselines:** B-COLD uses same urllib but empty registry discovery (3 fetches to build cache); B-NO-GUARD same execution but always EXECUTABLE; B-VERBATIM no probe; B-RETRIEVAL adds retrieval lookup cost; B-ORACLE uses ground-truth patch (1 probe) as ceiling.
- **Verification:** `verify(mechanism_id, observed_state)` via `src/spider/kernel.py:_matches(required, actual)` exact equality on required_slots = set(parameter_slots) | _template_slots(action_template) postconditions; deterministic, no LLM judge. Used for repair success (verify after patch == true) and contamination (verify unrelated mechanisms still true), and for AUROC ground truth (verify correct patch true, random patch false). All requests verified.

---

## 6. Target, Unit of Analysis, and Sampling Policy

- **Target:** Localized repair efficacy per perturbation instance: binary repair success (verify after patch true/false), cost (tokens-equiv honest sum-counter and browser steps), verification discrimination (AUROC/precision correct vs random patch), contamination (fraction unrelated mechanisms false_accept after patch), amortized Pareto (M_total at f=10 vs cold), and freshness preservation (TN/FA/UNKNOWN/ECE).
- **Unit of analysis:** Single perturbation instance (one resource instance from one trajectory's post-drift window), grouped at trajectory/family level for inference (family-stratified bootstrap preserves within-family dependence). Freshness computed per request (360 pool), repair per instance (30 pool).
- **Sampling policy (frozen, no outcome-dependent adaptation):**
  - **Synthetic primary server:** `http.server.HTTPServer` on 127.0.0.1 ephemeral port, stdlib only, no Docker/external network, single resource type only. Reuse scaffold `research/graph/freshness_detection/execute_rebalanced_35947468747.py` with added `research/graph/delta_repair/execute_delta_repair_synthetic_35949562506.py`.
  - **Workload composition (same rebalanced prevalence as parent):** 180 fresh pool (12 trajectories ×15 requests, no drift, for TN) + 30 stale pool (3 families ×2 trajectories ×10 with DRIFT_POINT=6 =>5 fresh+5 stale per traj, 10 stale per family =>30 stale) + 150 noise pool (15 trajectories ×10, 5 per variant A phone p=0.3, B nickname p=0.3, C email null p=0.2+phone p=0.3) =360 total. Repair evaluated on 30 stale instances (10 per family). B-COLD re-exploration baseline: 12 fresh trajectories ×1 re-exploration each (discovery 3 fetches + execution) =12 cold measurements. Unrelated mechanisms for contamination: N>=20 distinct resource ids not perturbed (sampled from fresh pool ids).
  - **Drift families (orthogonal, single-resource, blast radius=1):**
    1. `dom_drift`: 2 trajectories ×10 =20 (10 stale), Jaccard required-filtered {id,name,email} 0.60-0.75 <0.85 via id int->str + optional phone add.
    2. `param_header_mutation`: 2 trajectories ×10 =20 (10 stale), mutation via response `_template` detail->uid and X-Csrf-Token abc123->xyz789, response-derived detection.
    3. `cache_expiry`: 2 trajectories ×10 =20 (10 stale), ETag SHA256 change + max-age 60->0, ETag_changed AND max-age=0 detection.
  - **Repair patch (deterministic, no LLM):** stale detected (UNKNOWN 0.85) => re-observe 1 probe from live endpoint (browser_steps=1), compute delta live vs cached response-derived signals, overwrite cached dom/header/endpoint with live values, rebind action_template slots, re-verify via _matches. Cost = 1 browser + resolve+bind+verify+freshness (4) =5 units vs cold 16 units.
  - **Random-patch null:** for verification AUROC, propose random incorrect patch per stale instance: sample field-set/param/header value from different family uniformly, apply, verify; expected to fail.
  - **Distributed secondary policy:** DEFERRED. Not executed in this packet. Runtime health-gated Flask/JWT/WAL n>=800 stage logged as NOT_ATTEMPTED with dependency `runtime health-gated substrate (shared WAL /tmp/spider-runtime/*/shared.db WAL/journal_mode, 2x gunicorn 23 + nginx 1.24 HS256, If-None-Match 304, distinct X-Worker-Pid>=2)`; if health-gate later passes, identical thresholds will be re-evaluated.
  - No real network, no LLM API key required, no Docker for primary; seeds deterministic (port ephemeral, trajectory order fixed, perturbation seeds fixed via hashlib.sha256).

---

## 7. Holdout

- **Within-trajectory holdout (per-trajectory observed):** Fresh requests 1-5 per stale trajectory are cache source for that trajectory's mechanism; stale requests 6-10 held out for detection+repair test. No overlap request_number between cache and test; no global template leakage — cache per-trajectory observed, not precomputed. Repair patch derived from live observation of held-out requests only.
- **Train/test split for verification threshold:** Verification AUROC/precision threshold (staleness confidence 0.85) calibrated on TRAIN split (18 instances: 6 per family, trajectories 0 per family) and evaluated on TEST split (12 instances: 4 per family, trajectory 1 per family). Random-patch null similarly split. No post-state leakage into threshold fitting (threshold frozen pre-execution at 0.85).
- **Cross-family holdout:** Each family 10 stale held separately (per-family TP/repair success reported) to prevent header/body conflation; family-stratified bootstrap preserves family proportions (180 fresh +10 per family stale +150 noise + 30 repair). Contamination unrelated set disjoint ids from perturbed resources.
- **Leave-one-family-out robustness (exploratory but preregistered as auxiliary):** compute repair success when training threshold/patch logic on 2 families and testing on 3rd, to check generalization beyond family-specific delta.
- **No website holdout (synthetic):** Claim ceiling bounded to locally-hosted synthetic; not C-CROSSSITE. Distributed holdout deferred.

---

## 8. Nulls / Baselines (strong, matched tasks)

All baselines run on same rebalanced 360 synthetic workload (and same 30 repair instances where applicable) for matched comparison with identical honest counter, server state, and verification:

- **B-COLD-FULL-REEXPLORATION (primary cost baseline):** Empty registry, rediscover from 3 observations, then execute. Must show success >=90% at full cost ~16 units per trajectory. Repair must beat by <50% tokens-equiv and <40% browser.
- **B-NO-GUARD-REPLAY (safety baseline):** No freshness guard, always EXECUTABLE, verbatim replay on 30 stale. Must show FA~1.0 (30/30) delta vs SPIDER >=0.15 fails without guard, contamination high.
- **B-VERBATIM-REPLAY (0-cost replay):** No repair probe, stored mechanism executed unchanged. Must show 0% success post-perturbation (proving perturbation breaking), 0 cost; else family MEASUREMENT_INVALID.
- **B-RETRIEVAL-RAG (strong retrieval):** Jaccard 0.30 TFIDF retrieval over prior trajectories + nearest replay, retrieval cost 1 + replay, no patch. Expected 20-40% success; repair should exceed by >=30pp and lower contamination.
- **B-JACCARD-ONLY (signal ablation):** Only DOM Jaccard <0.85 ignores header/cache. Expected FA~0.66 fails 2 families, proving combined detection needed for correct repair triggering.
- **B-HEADER-ONLY (signal ablation):** Only header/cache + template ignores DOM. Expected FA~0.33 fails 1 family, complementary.
- **B-ORACLE-HAND-PATCH (ceiling):** Ground-truth minimal patch (1 probe+1 verify=5 units, 100% success). Measured deterministic repair should approach within 2x cost and equal success.
- **Positive control PC-LOCALIZED-REPAIR-SUCCEEDS:** Unperturbed execution 100% and oracle patch >=90% per family with cost ratio <0.50; if fails => MEASUREMENT_INVALID.
- **Null controls:** NC-ZERO (zero perturbation cost 0 contamination 0) and NC-RANDOM-PATCH (random incorrect patch AUROC 0.40-0.60 FA<=5% proves verification discriminates), plus NC-NOISE-IMMUNITY (150 churn noise FA<=0.10, no spurious repair).

Strong baseline justification: beating no-guard by delta >=0.90 necessary-but-weaker; beating both single-signal ablations by 0.33-0.66 and verbatim 0% while approaching oracle distinguishes true localized repair from pooled-metric salience or trivial replay; RAG baseline ensures repair adds value beyond retrieval memory; contamination on N>=20 unrelated distinguishes locality from global invalidation.

---

## 9. Primary Metrics & Decision Rule (frozen, satisfiable)

**Stable metric IDs (MUST be reused verbatim in result.json:metrics and controls):**

- `M-TN-SPIDER` = TN/(TN+FP) on 180 fresh — freshness preservation
- `M-TN-WILSON-LOWER` = Wilson lower z=1.96 for M-TN-SPIDER
- `M-FALSE-ACCEPT-SPIDER` = # stale EXECUTABLE/30 — false accept at 15% stale
- `M-FALSE-ACCEPT-WILSON-UPPER` = Wilson upper for FA (0/30 upper 0.1135)
- `M-UNKNOWN-RATE-SPIDER` = # UNKNOWN/210 staleness pool
- `M-ECE-SPIDER` global, `M-ECE-FRESH`, `M-ECE-STALE` per-class ECE recalibrated 0.95/0.85
- `M-REPAIR-SUCCESS-POOLED` = # repairs verify true/30 (pooled success)
- `M-REPAIR-SUCCESS-PER-FAMILY-{dom_drift,param_header_mutation,cache_expiry}` = per-family success (n=10 each) + Wilson lowers
- `M-REPAIR-COST-TOKENS-MEAN` = mean honest sum-counter tokens-equiv per repair (resolve+bind+verify+freshness+browser) and `M-REPAIR-COST-TOKENS-RATIO` = mean repair / mean B-COLD; bootstrap CI
- `M-REPAIR-BROWSER-MEAN` = mean browser steps per repair (1 probe) and `M-REPAIR-BROWSER-RATIO` = mean repair browser / mean B-COLD browser
- `M-REPAIR-VERIFY-STEPS-MEAN` = mean verification steps per repair (1-2)
- `M-CONTAMINATION-POOLED` = # unrelated mechanisms false_accept or invalidated /20 (or /N) pooled
- `M-CONTAMINATION-PER-FAMILY` + Wilson uppers
- `M-VERIFICATION-AUROC` = AUROC correct patch vs random-patch null on TRAIN/TEST split (sklearn-equivalent); `M-VERIFICATION-AUROC-RANDOM` = AUROC for random null ~0.50
- `M-VERIFICATION-PRECISION` = precision at frozen 0.85 threshold (TP/(TP+FP)) for verification
- `M-AMORTIZED-COST-F10` = (repair+verify+10*retrieval_cost) vs `M-COLD-COST-F10` = B-COLD cost; Pareto comparison; also `M-AMORTIZED-RATIO-F10`
- `M-M-TOTAL` trajectory aggregates and `M-M-TOTAL-F10` Pareto (sum-counter trajectory-grouped)
- Honesty: `M-RHO-SHUFFLED-MAX` = max|Pearson rho| 1000 trajectory-grouped perms primary, `M-RHO-SHUFFLED-MEAN` auxiliary, `M-COST-VECTOR` logged, `M-OBSERVED-RHO`, `M-WITHIN-FAMILY-STD-MIN-FRESHNESS`
- Baselines: `M-FA-B-NO-GUARD`, `M-SUCCESS-B-VERBATIM`, `M-SUCCESS-B-RETRIEVAL-RAG`, `M-FA-B-JACCARD-ONLY`, `M-FA-B-HEADER-ONLY`, `M-ORACLE-COST`
- Bootstrap: 5000 family-stratified trajectory-grouped 95% percentile CIs for all primary metrics (`M-TN-BOOT-CI`, `M-FA-BOOT-CI`, `M-REPAIR-SUCCESS-BOOT-CI`, `M-TOKEN-RATIO-BOOT-CI`, `M-BROWSER-RATIO-BOOT-CI`, `M-CONTAMINATION-BOOT-CI`, `M-AUROC-BOOT-CI`), width for non-degeneracy
- Freshness family metrics: `M-TP-FAMILY-{dom_drift,param_header_mutation,cache_expiry}` + Wilson

**Frozen decision rule (see spec.json:decision_rule, satisfiable by construction):**

- **PRIMARY SURVIVES_CURRENT_TEST (bounded synthetic delta-repair) iff ALL D1-D10 hold:**
  - D1 PC1 1.0 and PC2 >=0.90 per family, else MEASUREMENT_INVALID
  - D2 NC-ZERO cost 0 contamination 0 and NC-RANDOM AUROC 0.40-0.60 FA<=0.05 and NC-NOISE FA<=0.10, else MEASUREMENT_INVALID
  - D3 freshness TN>=0.85 Wilson lower>0.75 and FA<=0.10 and UNKNOWN in [0.00,0.18]∩[0.0928,0.2128] and global/per-class ECE<=0.15, else FALSIFIED (guard not enabling)
  - D4 repair success >=0.80 pooled (24/30) Wilson lower>0.65 and >=0.70 per family (7/10) bootstrap lower>0.60
  - D5 mean repair tokens-equiv <0.50*mean B-COLD and mean browser <0.40*B-COLD and verify steps <=2, bootstrap upper <0.55/<0.45
  - D6 contamination <0.10 pooled (<=2/20) and per-family <0.15 Wilson upper<0.20
  - D7 verification AUROC>=0.75 and precision>=0.80 at 0.85 threshold on TEST, random delta AUROC>=0.25
  - D8 amortized cost at n_reuses=10 < cold (tokens-equiv and browser) with honest counter
  - D9 B-NO-GUARD FA - SPIDER FA >=0.15 and B-NO-GUARD FA>0.10 and B-JACCARD-ONLY/B-HEADER-ONLY each fail >=1 family
  - D10 honesty V2-V6: constant integer counter, max|rho_shuffled|<0.20 trajectory-grouped, within-family freshness std>0, 5000 bootstrap done, per-trajectory caching+response-derived, verification deterministic, CIs width>0 or disclosed degenerate with Wilson informative
- **FALSIFIED-IN-SETTING if any D3-D9 fails while D1-D2 and D10 pass** (valid scientific negative on locality at realistic prevalence).
- **MEASUREMENT_INVALID if any D1-D2 or D10 fails or N<30 stale or per-family n<10 or unrelated N<20.**
- **MIXED if family-heterogeneous: >=1 family passes D4-D8 while another fails — report per-family ceilings.**
- **DISTRIBUTED CONDITIONAL DEFERRED:** Logged as NOT_ATTEMPTED_MEASUREMENT_DEFERRED, does not override synthetic PRIMARY; health-gated n>=800 stage is future VALIDATED blocker per runtime dependency.
- **INCONCLUSIVE only if primary CIs straddle thresholds with width>0.20 due to underpower at n=30** (disclosed but not expected).

Recalibration satisfiability proof frozen: With 180 fresh at 0.95 and 30 stale at 0.85, global ECE 0.0643 <0.15 (180*0.05/210=0.0429+30*0.15/210=0.0214), per-class fresh 0.05 stale 0.15 at threshold passes, UNKNOWN 0.1428 <0.18 passes; repair cost 5 vs cold 16 ratio 0.3125 <0.50, browser 1 vs ~3 ratio 0.33 <0.40 satisfiable by construction.

---

## 10. Uncertainty Method

- **Wilson CI** for proportions (TN, TP, FA, repair success, contamination, precision) z=1.96 raw counts; lower for TN/success, upper for FA/contamination; at n=10 per family disclose exact Wilson (7/10 lower 0.39, 9/10 lower 0.60, 0/20 upper 0.16); at pooled 24/30 lower 0.65, 0/30 upper 0.1135.
- **Trajectory-grouped family-stratified bootstrap (B=5000):** resample with replacement at trajectory level (12 fresh trajs 15 each=180, 6 stale trajs 2 per family x10 with 5+5, 15 noise trajs 10 each=150, plus 30 repair instances 10 per family, and 20 unrelated mechanisms), stratified by family preserving proportions, recompute TN, FA, UNKNOWN, ECE, repair success, token/browser ratios, contamination, AUROC, precision per resample → percentile 95% CI (2.5th,97.5th). Non-degeneracy required: width>0 to claim precision; degenerate [1.0,1.0] flagged as ceiling effect (audit validity_findings). Also bootstrap CI for D5/D6 ratios and D9 delta.
- **Honesty null:** max|rho_shuffled| via 1000 perms trajectory-grouped (shuffle whole trajectory blocks' cost vectors vs outcomes for repair success and for M_total vs freshness); report max primary <0.20 and mean auxiliary. Threshold <0.20.
- **Verification AUROC uncertainty:** DeLong-equivalent bootstrap (5000) or Hanley-McNeil for AUROC 95% CI; permutation null (random patch) AUROC 0.40-0.60 expected under null.
- **Adequacy rule:** N=30 stale +12 cold +20 unrelated ensures Wilson sensitivity at 0.80 pooled (half-width ~0.14) while per-family 10 gives informative per-family bound (7/10 lower 0.39); bootstrap 5000 preserves family strata. If N smaller => underpowered => MEASUREMENT_INVALID.
- **Distributed uncertainty:** DEFERRED; same Wilson+5000 bootstrap will apply at n>=800 non-304 health-gated stage when runtime substrate hardened.

---

## 11. Falsification / Survival Rule

- Positive `PRIMARY SURVIVES` upgrades bounded ceiling from synthetic freshness EXPERIMENTAL (EXP-GRAPH-35947468747: TN 1.0 FA 0.0) to synthetic delta-repair EXPERIMENTAL with contamination-bound localized repair (<50% tokens, <40% browser, AUROC>=0.75, contamination<0.10, amortized Pareto at f=10) under honest economics (max|rho|<0.20, 5000 bootstrap). This validates that freshness guard enables repair and provides honest M_total_f10 context without yet requiring distributed WAL, and authorizes runtime to harden health-gated distributed substrate to n>=800 for VALIDATED. Does NOT promote C-FRESHNESS/C-DELTA-REPAIR to VALIDATED/PRODUCT_CORE (needs distributed n>=800 + real LLM/Playwright audit PASS per registry); does NOT promote param-inherit pilots.
- Negative `FALSIFIED` bounded to this signal/threshold/site/substrate/patch/confidence: C-DELTA-REPAIR remains HYPOTHESIS/BLOCKED on synthetic, does NOT imply impossibility with orthogonal workflow-IR/endpoint-catalog levels, multi-resource, Redis, or real LLM repair — but proves cheapest localized deterministic patch is not sufficient/cheap/local on this single-resource substrate. Product must retain full replay budgeting and not rely on delta-repair for economics; honest Pareto remains inflated (freshness does not imply delta-repair, per Director comparative reasoning contamination>=0.10 triggers full replay accounting).
- `MEASUREMENT_INVALID` means honest-cost, trajectory-grouped rho, 5000 bootstrap, per-trajectory cache, response-derived endpoint, or verification substrate failed; or PC/NC failed; or N insufficient; no claim update for that gate, must not be cited as falsification; distributed stage INVALID does not retroactively falsify synthetic gate.
- `MIXED` family-heterogeneous outcome reports per-family ceilings (e.g., dom_drift survives while cache_expiry fails).

---

## 12. Validity Threats & Mitigations

- **Threat: Deterministic perfect repair AUROC=1.0 artefactual (prior simulation 1.0 perfect separation).** Mitigated by random-patch null AUROC 0.40-0.60 and requiring delta AUROC>=0.25 and TRAIN/TEST split; if both correct and random give AUROC 1.0 => measurement not discriminating => flagged as degenerate validity_notes, not SURVIVES.
- **Threat: Cost tautology jitter/n*3200/f*6.0/parity (prior 3 BLOCKED invalid).** Mitigated by V2 constant integer sum-counter base 4/5 no jitter, V3 no proxy, V4 trajectory-grouped max|rho|<0.20 (1000 perms), cost exempt from V5, verification via honest counter log.
- **Threat: Pooled-metric salience hiding per-family 0/10.** Mitigated by family-stratified trajectory-grouped bootstrap V6 and per-family success>=0.70 at n=10 (requires 7/10) and per-family contamination.
- **Threat: Header/body conflation (perturbation radius>1).** Mitigated by single-resource V9 isolation, orthogonal families 10 per family, separate ablations B-JACCARD-ONLY/B-HEADER-ONLY must fail, contamination measured on disjoint ids with blast radius 1.
- **Threat: Tautological verification (stale==true by construction then verify true after re-observe).** Disclosed ceiling: verification tests self-consistency of required vs actual from same deterministic generator, not learned param induction; but random-patch null must fail verification (precision discrimination) to prove verification is not vacuous; AUROC gate ensures this.
- **Threat: Degenerate CIs [1.0,1.0]/[0.0,0.0] masking precision.** Mitigated by V7 Wilson informative bounds (FA upper 0.1135 at 0/30, TN lower 0.979) and requiring bootstrap width>0 disclosure; deterministic ceiling flagged not claimed as high precision.
- **Threat: ECE 0.15 bound satisfiability at 15% stale.** Mitigated by recalibrated 0.95/0.85 and per-class ECE V8 with proof 0.0643 <0.15 at prevalence; UNKNOWN prevalence-aware [0.00,0.18].
- **Threat: Contamination hardcoded to 2 events artefactual (prior 0.0046).** Mitigated by measuring contamination on real unrelated mechanisms (N>=20) after applying actual patch to registry clone snapshot isolation (registry cloned before perturbation, patch operates on clone, delta measured on uninvolved set), not hardcoded; verification blocks unverified writes.
- **Threat: Amortization arithmetic consequence (prior 4744 vs 2226).** Mitigated by honest per-trajectory-reset sum-counter with identical retrieval cost (1 lookup) counted in both repair and cold; amortized comparison uses measured retrieval+verify+freshness, not hardcoded 320+180+1364.
- **Threat: Synthetic-to-real/distributed gap (51-streak runtime MEASUREMENT_INVALID).** Disclosed: primary stdlib flat JSON only, bounded to localhost single-resource deterministic patch; distributed health-gated n>=800 explicitly DEFERRED as dependency runtime, not conflated; claim ceiling remains synthetic EXPERIMENTAL, not VALIDATED.
- **Threat: Action→own-request tautology (live response-derived signal equals cached).** Mitigated by response-derived endpoint signals (server emits mutated _template, client compares response to response from different family) and per-trajectory cache; NC-NOISE tests independent optional churn not flagged as stale, not repaired.
- **Threat: Per-trajectory cache miss & 304 circularity.** Mitigated by 3 observed exemplars per trajectory and deterministic fresh generation without churn except noise pool; If-None-Match 304 logic preserved but not triggered on synthetic; repair re-observe is fresh fetch, not 304.
- **Threat: LLM BLOCK fallback to heuristic.** Mitigated by not requiring LLM API key: repair is deterministic re-observe heuristic disclosed as bounded synthetic ceiling; no LLM calls, no BLOCK risk; real LLM repair remains future VALIDATED work.

---

## 13. Estimated Cost & Information Gain

- **Cost:** Primary synthetic delta-repair low (~360 workload +30 repairs +12 cold + retrieval/baselines, <15 min CPU for 5000 bootstraps +1000 perms, <0.8 compute-hour, no LLM/browser/Docker, <$1). No distributed cost (deferred). Total bounded <1 compute-hour. Reuses parent scaffold to minimize code.
- **Gain:** Very high per Director REOPEN comparative reasoning: directly tests neglected blocking claim (C-DELTA-REPAIR 3 prior BLOCKED, sole freshness SURVIVES prerequisite, blocks C-RESIDUAL-NOVELTY honest M_total_f10 Pareto and C-PRODUCT-ECON). Either SURVIVES validates that freshness enables contamination-bound localized repair with honest economics (unblocking VALIDATED distributed gate and providing amortized context) or FALSIFIES proves freshness does not imply delta-repair (contamination>=0.10 => product must account full replay, per mandate) — both materially change next graph/runtime/product decision. Cannot be obtained by another WebArena param-inherit pilot (expected repeat MEASUREMENT_INVALID on durability, marginal info ~0) or immediate distributed pursuit (degenerate [1.0,1.0] CI, predicted MEASUREMENT_INVALID). Minimal deterministic single-resource test isolates locality without LLM BLOCK, harvesting synthetic leverage before distributed cost.

---

## 14. Execution Scope & Code Paths

- **Allowed roots:** `research/graph`, `research/harness` per `research/lanes/registry.json:graph.allowed_code_roots` (graph lane: cumulative operational inheritance, fragments, parameterization, semantic resolution, freshness boundaries).
- **Planned harness:** `research/graph/delta_repair/execute_delta_repair_synthetic_35949562506.py` (new, ~400 lines, deterministic repair logic: re-observe cache update + rebind + _matches verify, honest per-trajectory-reset counter, family-stratified bootstrap 5000, trajectory-grouped perms 1000) reusing `research/graph/freshness_detection/execute_rebalanced_35947468747.py` scaffold for server (`http.server.HTTPServer` 127.0.0.1 ephemeral, ETag SHA256[:16], Cache-Control, _template/X-Csrf-Token) and `src/spider/kernel.py` _matches verification. Also helper `research/harness/synthetic_single_resource_server.py` if refactor needed. Raw evidence to `research/experiments/EXP-GRAPH-35949562506/raw_evidence/` with `execution_results.json`, `request_logs.json`, `metrics.json`, `decision.json`, `cost_logs.json`, `bootstrap_ci.json`, `per_trajectory_cache.json`, `repair_logs.json`, `contamination_logs.json`, `verification_auroc.json`, and `health_gate.json` (DEFERRED marker). Also log SHA256 per artifact. No nginx/Flask/WAL/Playwright/openai required.
- **Freezing:** `freeze.json` will hash request/spec/prereg before execution; EXECUTE must not mutate frozen inputs; any pre-freeze work inconsistent with Director mandate superseded per architecture; distributed stage deferred does not require freeze violation.
- **Dependencies:** runtime honest sum-counter (already satisfied per parent V2-V4) and health-gated distributed substrate (`C-MEAS-VALID` HS256 shared-WAL) listed as dependency but DEFERRED — not required for synthetic PRIMARY SURVIVES; secondary stage gated, logged as NOT_ATTEMPTED, not BLOCKED.
- **Signals frozen pre-execution:** threshold 0.85, DRIFT_POINT=6, deterministic server mutations (id int->str/phone, _template detail->uid, X-Csrf-Token rotation, ETag+max-age 60->0), confidence 0.95/0.85, UNKNOWN bound [0.00,0.18]/[0.0928,0.2128], max rho procedure (1000 trajectory-grouped), noise stimulus p-values, per-trajectory cache size 3, verification threshold 0.85 TRAIN/TEST split, repair cost units (4 fresh/5 repair), retrieval cost 1, n_reuses=10 for amortized.

---

## 15. Prereg Timing & Transmission Discipline

Frozen before any outcome-bearing measurement for this experiment_id. Prior evidence cited is from Codex, `research/experiments/EXP-GRAPH-35947468747/*` audit/handoff, and `request.json:director_mandate` agent priors (labeled as prior not SPIDER evidence), not from new data. No material fact will exist only in Actions logs; all evidence paths/hashes will be in packet. Control/metric IDs frozen here will be reused verbatim in `result.json:metrics/controls` and `audit.json:recomputed_metrics` for downstream transmission. Status=COMPLETE with outcome FALSIFIES/MIXED is valid negative, not infrastructure failure; status=BLOCKED/MEASUREMENT_INVALID reserved for honesty/infra failure per packet §4, never encoded as falsification; distributed stage DEFERRED does not override synthetic PRIMARY. Direct # of staleness pool 30 and repair 10 per family chosen for realistic 15% prevalence power and per-family Wilson sensitivity, not post-hoc.

---

*Prereg follows SPIDER_MASTER_PROMPT.md §19 and Research 2.0 binding packet `research/EXPERIMENT_PACKET.md` §§3-5. DESIGN performed without outcome-bearing measurements per AGENTS.md work discipline.*

