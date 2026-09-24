# EXP-GRAPH-35952148696 — Preregistration (DESIGN frozen pre-outcome)

**Lane:** graph  
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally (next_gate: controlled local perturbations with repair cost and contamination bounds)  
**Experiment ID:** EXP-GRAPH-35952148696  
**Director mandate:** REOPEN C-DELTA-REPAIR (action=REOPEN, claim_id=C-DELTA-REPAIR, parent_handoff_disposition=USE, cognitive_reset=false, dependencies=[runtime single-node honesty gate]) per `request.json:director_mandate` — comparative reasoning: vs durable param-inherit pilot (8 consecutive MEASUREMENT_INVALID on identical kernel durability gate single-prefix/_is_allowed_path/Jaccard>=0.75, low marginal value without new durability proof) rejected; vs immediate distributed VALIDATED freshness (needs runtime HS256+nginx n>=800 not yet proven) blocked; vs direct C-RESIDUAL-NOVELTY duplication avoided. `inherited_next_question` advisory continuity, `director_mandate.question` binding per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2.  
**Parent handoff:** `research/experiments/EXP-GRAPH-35949562506/handoff.json` (SHA 46ada681e47a0ae6bb710b44c1cba71e5d82ad72bb7ea6c40101da7cd24e8970, verdict MEASUREMENT_INVALID, producer_claim_supported=false, 4 critical VF1-VF4 + VF5) — preserved as continuity evidence only per `director_mandate.parent_handoff_disposition=USE`; not automatic agenda. Honest re-measurement required.  
**Frozen hashes:** request `38eb3b3c568ec98075778a3e296517965d470cac76579785935af26afa0a7d91`, claim registry `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b` — design must not inspect outcome data.  
**Prior audit:** EXP-GRAPH-35949562506 audit MEASUREMENT_INVALID with 7 required_fixes (VF1 manufactured hash-score AUROC, VF2 clamped null AUROC, VF3 hardcoded PC/NC, VF4 D8 browser 11<12 not 11<3, VF5 fabricated retrieval 0.30, VF6 390 vs 360 deviation, VF7 instance-level bootstrap) and 5 unresolved (null design degenerate, same-resource contamination, amortized Pareto mixing, AUROC uncertainty degenerate, workload prevalence). This prereg explicitly resolves all 7.

---

## 1. Strategic Question → Falsifiable Question

**Director strategic question (verbatim request.json:director_mandate.question):**

> Does the validated synthetic-rebalanced freshness guard (Jaccard 0.85 required-filtered {id,name,email}+response-derived endpoint _template/X-Csrf-Token+ETag+max-age=0, recalibrated 0.95 fresh/0.85 stale, TN>=0.85 Wilson lower>0.75 FA<=0.10 ECE<=0.15 at 15% stale 360-req=180 fresh+30 stale+150 noise, NC-NOISE-IMMUNITY FA<=0.10) enable bounded C-DELTA-REPAIR with honest instrumentation on the same locally-hosted single-resource flat-JSON stdlib http.server substrate (deterministic _matches verification, honest per-trajectory-reset sum counters resolve+bind+verify+freshness+browser_steps without jitter/n*3200/f*6.0, trajectory-grouped max |rho_shuffled|<0.20, 5000 family-stratified bootstrap) such that a controlled single-resource perturbation (DOM attribute/text via Jaccard, endpoint param/header via _template/X-Csrf-Token, Cache-Control/ETag one resource only) requires localized repair with delta cost <50% tokens and browser <40% vs cold re-exploration, verification AUROC>=0.75 precision>=0.80, contamination<0.10 behind health-gated verification, and honest M_total_f10 not inflated, vs B-NO-GUARD and single-signal baselines, before authorizing health-gated distributed shared-WAL transfer (n>=800 non-304, X-Worker-Pid>=2)?

**Falsifiable refined question (this prereg — smallest high-information test with honest instrumentation):**

> On the identical locally-hosted synthetic single-resource `/resource/{id}` stdlib http.server flat-JSON substrate with the same deterministic guard (Jaccard 0.85 required-filtered {id,name,email}+response-derived _template/X-Csrf-Token+ETag+max-age=0, recalibrated 0.95 fresh/0.85 stale, honest per-trajectory-reset constant integer sum-counter resolve 1+bind 1+verify 1+freshness 1=4 base fresh /5 repair with 1 deterministic re-observe probe browser 0/1 retrieval 1 no jitter/n*3200/f*6.0/parity, trajectory-grouped max|rho_shuffled|<0.20 via 1000 whole-trajectory-block perms, 5000 family-stratified trajectory-grouped bootstrap, deterministic src/spider/kernel.py _matches exact equality), does a controlled single-resource perturbation — dom_drift (field-set Jaccard 0.60-0.75 <0.85), param_header_mutation (response _template detail->uid + X-Csrf-Token abc123->xyz789), cache_expiry (ETag SHA256[:16] changed + max-age 60->0) — 10 instances per family (30 total), require only localized deterministic repair (re-observe 1 probe from live endpoint, overwrite cached dom/header/endpoint with live response-derived values, rebind _template, re-verify via _matches) achieving repair success >=80% pooled >=70% per family, mean cost <50% tokens-equiv (5 vs 16 ratio 0.3125) and <40% browser (1 vs 3 ratio 0.333) verify steps <=2, verification AUROC>=0.75 precision>=0.80 at frozen 0.85 threshold on TEST (TRAIN 18 / TEST 12 split, binary _matches outcomes correct 30 true vs random 0 true pooled AUROC 1.0, permutation-shuffled null 0.40-0.60 unclamped), contamination<0.10 on N>=20 unrelated mechanisms re-verified after patch (disjoint ids 9000-9019, blast radius=1, registry clone isolation), amortized tokens 15 (5+10*1) <16 and browser 1 (1+10*0) <3 at f=10 with retrieval browser 0, while sustaining freshness TN>=0.85 FA<=0.10 UNKNOWN/ECE calibrated and beating B-NO-GUARD delta>=0.15 and single-signal ablations each fail >=1 family, vs matched cold/verbatim/executed-retrieval baselines, with all 7 prior audit required_fixes applied (executed PC/NC, unclamped null, honest D8, exact 360 evaluated /390 executed harmonization, trajectory-grouped bootstrap)?

Design is the smallest high-information test that can change C-DELTA-REPAIR claim/product decision per Director rationale; it does NOT repeat the 8 prior param-inherit durability pilots nor immediate degenerate distributed VALIDATED (n>=800), and leverages the sole synthetic SURVIVES freshness prerequisite (EXP-GRAPH-35947468747 audit PASS, TN 1.0 FA 0.0 Wilson upper 0.1135) without requiring health-gated WAL, while fixing measurement validity so result is discriminating not artefactual.

---

## 2. Hypothesis

**H1 (positive, bounded synthetic with honest instrumentation):** Synthetic-rebalanced freshness SURVIVES translates to bounded delta-repair when instrumentation is honest: with combined guard, per-trajectory observed caching, response-derived endpoint, honest constant integer sum-counter, trajectory-grouped max|rho|<0.20 and executed controls, a single-resource local perturbation is repairable by a localized deterministic patch (delta = re-observe 1 probe + rebind + re-verify) without full re-exploration. Expected: (a) repair success 1.0 pooled (30/30 Wilson lower 0.8865) >=0.80 and 1.0 per family (10/10 Wilson lower 0.7225) >=0.70 with family-stratified trajectory-grouped bootstrap lower>0.60; (b) mean tokens 5 vs cold 16 ratio 0.3125 <0.50 and browser 1 vs 3 ratio 0.333 <0.40 verify steps 1.0 <=2 bootstrap upper <0.55/<0.45; (c) verification discrimination at frozen 0.85 on TEST: correct patches all verify true (30/30), random incorrect patches (wrong-family values) all verify false (0/30) false_accept 0.0 <=0.05, binary AUROC 1.0 >=0.75 precision 1.0 >=0.80 recall at 0.85 on TEST ~0.58-1.0 depending on binary threshold but precision at 0.85 is 1.0, permutation-shuffled label AUROC 0.40-0.60 unclamped; (d) contamination 0.0 pooled (0/20 Wilson upper 0.1611) <0.10 Wilson upper<0.20 re-verified after patch on disjoint ids; (e) honest amortized 15 tokens <16 and 1 browser <3 at f=10 with retrieval cost 1 token 0 browser per reuse, trajectory-grouped max|rho|<0.20 preserved; (f) freshness TN 1.0 Wilson lower 0.982 FA 0.0 upper 0.1135 still holds, UNKNOWN 0.125 within [0.00,0.18]∩[stale_rate±0.07], global ECE 0.0625 per-class 0.05/0.15 <=0.15, vs B-NO-GUARD FA 1.0 delta 1.0 >=0.15 and vs B-JACCARD-ONLY 0.6667 / B-HEADER-ONLY 0.3333 each fail >=1 family, B-VERBATIM 0.0, B-RETRIEVAL executed 0.20-0.40. Orthogonal necessity (combined guard) explains detection, not pooled salience; cost 1.0x oracle is definitional copy-and-rebind on this deterministic substrate (disclosed).

**H0 (null, bounded locality fails while honesty passes):** Repair locality fails while honesty gates pass: any primary D3-D9 fails — success <0.80 pooled or <0.70 per family, cost ratio >=0.50 tokens or >=0.40 browser, verification AUROC<0.75/precision<0.80 at 0.85, contamination>=0.10 re-verified, amortized not cheaper than cold (15>=16 or 1>=3), or freshness degrades TN<0.85 FA>0.10, or no FA delta vs no-guard (<0.15). Valid scientific negative. Honesty gates (V2-V6) trigger MEASUREMENT_INVALID if constant counter, trajectory-grouped max rho>=0.20, 5000 trajectory-grouped bootstrap not done, per-trajectory caching/response-derived violated, or PC/NC/retrieval hardcoded/clamped — distinct from falsification per transmission discipline.

**Prior expectations used (director_mandate.agent_priors_used, labeled as prior not SPIDER evidence):** (1) path-dependent salience pollution — single next-step Jaccard misses correlated-session dynamics, requires trajectory-grouped permutation and correct-family gating; (2) thresholded fingerprint caching without UNKNOWN/ECE calibration → false_accept dominates, distinguished from SPIDER 0.95/0.85 recalibration and Jaccard 0.85+ETag partial mitigation; (3) parameterization only transfers when alias families orthogonal Jaccard<0.30 — distinguished from 8 MEASUREMENT_INVALID param-inherit pilots; (4) O(1) tool/API bypass dominates O(MxN) browsing when manifest normalized — distinguished from WebMCP Frontier mixed ceiling; (5) measurement degeneracy at ceiling 1.0 CI [1.0,1.0] signals insufficient diversity, requires heterogeneous |S| and 5000 bootstrap — distinguished from runtime 1.0 ceiling blocked gradients; (6) barrier/rewind-memory hypothesis (|rho_length|~|rho_novelty| unless delta-repair localizes) motivates product honest M_total_f10 and frontier shift. These priors motivate honest sum-counter, trajectory-grouped rho, family-stratified bootstrap, deferring distributed VALIDATED.

---

## 3. Continuity vs Director Supersede — Preservation of Established/Rejected/Unknown/Do_not_assume

This section explicitly preserves the four-way distinction from `EXP-GRAPH-35949562506/handoff.json:carry_forward` per transmission discipline; `director_mandate.question` is binding direction, parent `next_question` harmonized (USE disposition, REOPEN narrow delta-repair while retaining synthetic substrate and fixing honesty).

**Established (preserved verbatim, not re-tested as hypothesis):**

- Narrow deterministic detection sub-ceiling ONLY: locally-hosted stdlib http.server single-resource flat-JSON /resource/{id} at 12.5% stale actual (210 fresh+30 stale pool 240 +150 noise=390, spec 180+30 pool 210 stale 0.1428 both within [0.00,0.18] and [stale_rate±0.07]) the combined guard (Jaccard 0.85 required-filtered {id,name,email} + response-derived _template detail->uid / X-Csrf-Token abc123->xyz789 + ETag SHA256[:16] changed AND max-age 60->0) detects ALL 30 orthogonal single-resource perturbations: M-TN-SPIDER 1.0 (210/210 Wilson lower 0.9820) M-FA-SPIDER 0.0 (0/30 Wilson upper 0.1135) per-family TP 10/10 each Wilson lower 0.7225, UNKNOWN 0.125 Wilson [0.089,0.1728] ECE global 0.0625 fresh 0.05 stale 0.15 <=0.15, NC-NOISE-IMMUNITY FA 0.0 (0/150) TN 1.0, B-NO-GUARD FA 1.0 delta 1.0 >=0.15, B-JACCARD-ONLY FA 0.6667 B-HEADER-ONLY FA 0.3333 each fail >=1 family proving combined signal required, B-VERBATIM 0.0. Audit recomputed_metrics confirm identically. Bounded to deterministic synthetic flat-JSON response-derived signal set, recalibrated 0.95/0.85, honest constant sum-counter, trajectory-grouped max|rho| 0.0.

- Deterministic copy-and-rebind re-observe patch ceiling ONLY (audit VF8): re-observe 1 probe from live endpoint, overwrite cached dom/header/endpoint with live-derived values, rebind _template, re-verify via _matches restores EXECUTABLE on 30/30 at 5 tokens ratio 0.3125 <0.50 and 1 browser ratio 0.333 <0.40 verify 1 step, matching oracle 5 units 100% because it is same operation. Cost logs 390 at 4 base all_int true vector std 0, max|rho_shuffled| 0.0 via 1000 whole-trajectory-block perms <0.20 but vacuous via zero variance per VF9, within-family freshness std 0.5 >0 valid, per-trajectory cache 33 trajs first valid of 1-3 response-derived. Disclosed in prereg s227 and audit VF8 as definitional success on this construction: proves only 'copy-live-bytes-and-rebind at 5 units restores equality' not general repair capability; contamination 0.0 on 20 disjoint ids is structural no-op not measured (lines 728-730 constants) — to be re-measured honestly this cycle.

- Measurement-validity gates V1-V5 partially verified as disclosed but vacuous in constant-cost regime: V1 _matches deterministic equality holds 390/390 true, V2 constant integer per-trajectory-reset sum-counter 4 fresh/5 repair no jitter, V3 no jitter/proxy holds, V4 trajectory-grouped max|rho| 0.0 <0.20 holds, V5 within-family freshness std 0.5 >0 holds; bootstrap 5000 performed but degenerate [1.0,1.0] width 0 ceiling effect (Wilson informative), per audit VF9 honest gates do not test graded cost discrimination. V14 per-trajectory observed caching response-derived verified, V12 distributed DEFERRED correctly flagged DISTRIBUTED_MEASUREMENT_INVALID (health_gate false n 0<800).

- Parent synthetic-rebalanced C-FRESHNESS ceiling remains EXPERIMENTAL (EXP-GRAPH-35947468747 audit PASS, TN 1.0 lower 0.982 FA 0.0 upper 0.1135 at 12.5% prevalence, degenerate bootstrap) — parent packet adds no VALIDATED evidence and is bounded to synthetic stdlib http.server flat-JSON single-resource, same guard/threshold/confidence/prevalence, not production CDN/304/session or distributed WAL.

**Rejected (must NOT be cited as support; explicitly rejected):**

- Single-signal guards as standalone detectors at this threshold/site/prevalence: DOM Jaccard-only FA 0.6667 misses param_header+cache 20/30, header/ETag-only FA 0.3333 misses dom_drift 10/30 — bounded rejection of single-channel detection at sparsity, not broader C-FRESHNESS domain (session/token/CDN, workflow IR).

- No-guard always-EXECUTABLE as safe reuse: B-NO-GUARD FA 1.0 (30/30) delta 1.0 vs SPIDER 0.0 UNKNOWN 0 outside prevalence window — bounded rejection, not general reuse claim.

- No bounded scientific hypothesis rejected for C-DELTA-REPAIR locale (success<0.80, cost>=0.50, browser>=0.40, contamination>=0.10, AUROC<0.75/precision<0.80, amortized not cheaper) because prior measurement invalid per 4 critical findings (VF1-VF4): no inference that localized repair is impossible or freshness does not imply repair; D4/D5 numbers are tautological artefacts safeguarded only by manufactured random-patch null, so they cannot support falsification either.

- Any inference that perfect detection (TN 1.0) or degenerate bootstrap [1.0,1.0] proves high-precision calibration or distributed robustness — disclosed ceiling effect, Wilson provides informative width, distributed transfer remains untested.

**Unknown (this experiment's target to resolve with honest instrumentation):**

- Whether genuine _matches-outcome AUROC/precision at frozen 0.85 threshold discriminates correct patch vs random-patch null on this deterministic substrate when scores are binary _matches outcomes (not hash-injected 0.78-0.99 vs 0.10-0.50) and null is unclamped (not 0.4803 clamped) with permutation-shuffled AUROC 0.40-0.60: correct patch always passes (30 true), random patch always fails (0 true) gives perfect separation AUROC 1.0 but random-patch null design is degenerate (substrate cannot produce occasional random accept); audit unresolved 1 notes null design needs operationalization — this experiment operationalizes via binary outcomes + permutation null and reports Hanley-McNeil CI disclosure.

- Whether SAME-resource contamination (patch on resource A breaking second mechanism bound to same A) is measurable under blast radius=1 disjoint-id design: frozen V9 contamination on unrelated ids 9000-9019 is no-op by construction, so contamination<0.10 gate is uninformative for same-resource blast radius>1 (audit unresolved 2) — this experiment re-measures via registry clone re-verification (still blast radius=1 disclosure, but executed not asserted).

- Whether amortized Pareto at f=10 is well-defined as formulated: frozen D8 previously compared 11 vs 3 (11<3 false literal) but honest retrieval browser 0 gives 1 vs 3 pass; mixed bases (total-over-10 vs single cold) conflated per-use vs total — this experiment fixes D8 to frozen cost model (tokens 5+10*1=15<16, browser 1+10*0=1<3, comparator 3 not 12, no invented retrieval browser).

- Whether AUROC uncertainty (DeLong/Hanley-McNeil bootstrap per s206) can be computed from binary _matches with zero overlap (degenerate) or threshold needs stochastic variance (audit unresolved 4) — this experiment reports binary AUROC 1.0 with disclosure that CI is degenerate and Wilson/perm null provides informativeness.

- Whether frozen 360 workload (180 fresh+30 stale+150 noise pool 210 stale 0.1428) vs executed 390 (210+30+150 pool 240 stale 0.125) governs claim ceiling (audit VF6) — this experiment freezes harmonized 360 evaluated /390 executed with 30 auxiliary pre-drift fresh disclosed, formal amendment same as parent, so VF6 resolved.

- Whether guard and patch transfer to health-gated distributed shared-WAL Flask/JWT+nginx If-None-Match/304 at n>=800 non-304 with identical thresholds — DEFERRED this packet health_gate false, dependency runtime lane not hardened, logged as NOT_ATTEMPTED.

- Whether multi-resource (2-3 resources) or cross-page drift locality, real LLM token billing and Playwright execution vs synthetic heuristic, residual-novelty M_total_f10 Pareto at f=100 vs f=10, latent correlated non-determinism, per-trajectory cache misses, 304 circularity via external oracle — all deferred.

**Do_not_assume (explicit non-conclusions):**

- SURVIVES detection (TN 1.0 FA 0.0 at 12.5% synthetic) implies bounded C-DELTA-REPAIR locality (contamination<0.10, AUROC>=0.75, cost<50%): detection necessary not sufficient — prior packet proves detection sub-measurement can pass while verification/null/contamination/amortization instrumentation wholly invalid; freshness does not imply delta-repair (Director comparative reasoning contamination>=0.10 triggers full replay).

- Degenerate bootstrap CIs [1.0,1.0] TN, [0.0,0.0] FA reflect deterministic perfect detection and homogeneous constants, not precision; Wilson informative (TN lower 0.982 FA upper 0.1135) provides width; requires stochastic threshold/non-deterministic site for width>0.

- Hash-injected verification scores 0.78-0.99 correct vs 0.10-0.50 random yielding AUROC 0.9967/1.0 are fabricated via hashlib — not _matches outcomes; this experiment recomputes from binary _matches at 0.85 (audit required_fix 1).

- Clamped random-patch AUROC 0.4803/0.5083 in [0.40,0.60] is label-scramble artifact clamped into range that cannot fail — this experiment unclamps and reports permutation-shuffled distribution (required_fix 2).

- Hardcoded PC1 1.0 PC2 1.0 NC1 cost 0 (lines 908-913) prove instrumentation health — controls that cannot fail cannot validate D1/D2; this experiment executes them (required_fix 3).

- B-RETRIEVAL-RAG 0.30 hardcoded proves retrieval-plus-patch advantage — retrieval success was invented inside expected window; this experiment executes retrieval via Jaccard 0.30 TFIDF (required_fix 4).

- Amortized tokens 15<16 and browser 11<30 with cold_browser*4=12 comparator proves Pareto advantage — literal rule is 11<3 false; honest retrieval browser 0 gives 1<3 pass but prior recorded metrics and gate logic rigged via '# ensure passes'; this experiment records honest 1<3 with comparator 3 (required_fix 4).

- Repair success 30/30 at ratio 0.3125 proves general localized repair capability at <50% cost with contamination<0.10 — proves only narrow tautological ceiling 'copy live response bytes and rebind restores _matches at 5 units' on single-resource blast radius=1 deterministic substrate; needs LLM heuristic, multi-resource blast radius>1 disclosure (audit VF8).

- Constant sum-counter 4 with max|rho| 0.0 proves honest economics discriminates residual novelty — rho trivially 0 via zero variance tests only no injected variance, not graded M_total_f10 discrimination (audit VF9); amortization gate required but prior rigged — this experiment fixes D8.

- Any MEASUREMENT_INVALID equals FALSIFIED-IN-SETTING for C-DELTA-REPAIR or closes synthetic path — per EXPERIMENT_PACKET s9 operational/manufactured failure distinct from scientific negative; claim remains HYPOTHESIS/BLOCKED not REJECTED (5 Graph attempts: 1 simulation REVISE + 3 BLOCKED + 1 SURVIVES +1 MEASUREMENT_INVALID), no update to distributed/Redis/production CDN.

---

## 4. State Representation

- **Raw observation (synthetic primary, stdlib http.server):** HTTP response for `/resource/{id}`: flat JSON body 3-5 fields (id, name, email, plus optional phone/nickname), `ETag: SHA256(canonical_json_without_template)[:16]`, `Cache-Control: max-age=60` or `max-age=0`/`no-store`, `X-Csrf-Token` header, and response-signaled template field `_template: {query_params: [...], header_names: [...]}` server emits for response-derived endpoint detection. Perturbation mutates exactly one local signal per instance: dom_drift changes field-set (id int->str, add phone) type diff, param_header_mutation rotates _template detail->uid and X-Csrf-Token abc123->xyz789, cache_expiry flips ETag+max-age 60->0. For NC-NOISE, server adds optional phone p=0.3 or nickname p=0.3 or email null p=0.2 as fresh noise. No external network, no LLM.

- **Derived freshness/repair state (per-trajectory observed cache, same as parent, honest):**
  - `dom_tokens_cached = sorted {(field_path,type)}` via `extract_field_types` (types string/integer/boolean/array/object) from requests 1,2,3 per trajectory first valid frozen.
  - `header_tokens_cached = {Cache-Control, ETag, X-Csrf-Token}` from same observed requests; `header_tokens_live` from live response.
  - `endpoint_template_cached = {path + sorted(query_param_names) + sorted(header_names)}` extracted from observed response `_template` (response-derived); `endpoint_template_live` from live response `_template`.
  - `jaccard_dom = |dom_tokens_cached ∩ dom_tokens_live| / |dom_tokens_cached ∪ dom_tokens_live|; etag_changed = (ETag_live != ETag_cached); cache_expiry = (Cache-Control_cached max-age=60 AND live max-age=0); param_template_changed = (endpoint_template_live != endpoint_template_cached)` exact set equality on response-derived names.
  - Combined: `stale = (jaccard_dom <0.85) OR param_template_changed OR (etag_changed AND cache_expiry)` threshold 0.85 frozen.
  - Repair trigger: if `stale==True` (UNKNOWN 0.85) then patch = delta between live and cached response-derived signals (field-set diff, _template diff, ETag diff) applied via re-observe update: re-fetch 1 probe from live endpoint, overwrite cached dom/header/endpoint with live-derived values, rebind mechanism via deterministic template, re-verify via _matches.
- **Confidence (recalibrated frozen):** `0.95` if `stale==False` (EXECUTABLE fresh/no repair), `0.85` if `stale==True` (UNKNOWN stale flagged/repair triggered).
- **Cost state (honest per-trajectory-reset constant integer sum-counter, FIXED per audit VF4):** `cost_resolve`=1, `cost_bind`=1, `cost_verify`=1, `cost_freshness`=1, `cost_browser`=0 fresh or 1 per repair probe deterministic, `cost_retrieval`=1 per lookup (no browser), `cost_distill`=1 per distill (literal template capture). All integers, per-trajectory-reset (trajectory block sum, not global), logged per request/instance. No jitter/parity/bijective proxy/n*3200/f*6.0; browser steps 1 per repair probe only, retrieval adds 0 browser.
- **Representation loss disclosed:** DOM tokens ignore value magnitudes/nested depth beyond flat keys; ETag truncated to 16 hex; endpoint template ignores param value semantics; per-trajectory cache 3 observations may miss rare optional fields; synthetic single resource flat-JSON only, not production DOM/session/CDN depth; repair deterministic re-observe, not LLM heuristic reasoning; verification exact _matches equality, not semantic utility; contamination blast radius=1 disjoint ids structural no-op disclosure.

---

## 5. Action Representation

- **Intent:** `fetch_resource` with params `{resource_id}` on single resource `/resource/{id}`.
- **Mechanism action_template:** `GET /resource/${resource_id}` with headers `{X-Csrf-Token: ${token}}` and query `?detail=${detail}` (param template). Literal mechanism via SPIDER kernel `distill` literal; `distill_parameterized` not under test for repair.
- **Execution (synthetic):** stdlib `urllib.request` GET to `http://127.0.0.1:{port}/resource/{id}?detail={detail}` with `X-Csrf-Token`. Browser_steps deterministic 0 fresh /1 repair probe (re-observe fetch), retained for honest counter. Conditional `If-None-Match` logic preserved but 304 not triggered on synthetic (deterministic ETag, marked handling).
- **Execution baselines:** B-COLD uses same urllib but empty registry discovery (3 fetches to build cache, 12+4=16); B-NO-GUARD same execution but always EXECUTABLE; B-VERBATIM no probe cost 0; B-RETRIEVAL adds retrieval lookup cost 1 + replay via _matches (executed, not hardcoded 0.30); B-ORACLE uses ground-truth patch (1 probe) as ceiling.
- **Verification:** `verify(mechanism_id, observed_state)` via `src/spider/kernel.py:_matches(required, actual)` exact equality on required_slots = set(parameter_slots) | _template_slots(action_template) postconditions; deterministic, no LLM judge. Used for repair success (verify after patch true), contamination (verify unrelated mechanisms still true after patch on registry clone), and AUROC ground truth (verify correct patch true vs random patch false). All requests verified; scores are binary 0/1 not hash-injected 0.78-0.99.
- **Repair patch executed (honest):** For each stale instance, execute re-observe fetch 1 probe, compute delta live vs cached response-derived signals, overwrite cache, rebind, call _matches; log success. Random-patch null: sample wrong-family value uniformly, apply to cloned mechanism, verify false (0/30 expected), log.

---

## 6. Target, Unit of Analysis, and Sampling Policy

- **Target:** Localized repair efficacy per perturbation instance: binary repair success (verify after patch true/false), cost (tokens-equiv honest sum-counter and browser steps), verification discrimination (binary AUROC/precision correct vs random patch via _matches, permutation null), contamination (fraction unrelated mechanisms false_accept after patch re-verified), amortized Pareto (honest M_total at f=10 vs cold), freshness preservation (TN/FA/UNKNOWN/ECE).
- **Unit of analysis:** Single perturbation instance (one resource instance from one trajectory's post-drift window), grouped at trajectory/family level for inference (family-stratified trajectory-grouped bootstrap preserves within-family dependence). Freshness computed per request (210-pool), repair per instance (30-pool).
- **Sampling policy (frozen, no outcome-dependent adaptation, resolves VF6):**
  - **Synthetic primary server:** `http.server.HTTPServer` on 127.0.0.1 ephemeral port, stdlib only, no Docker/external network, single resource type only. New harness `research/graph/delta_repair/execute_delta_repair_synthetic_35952148696.py` fixing 7 audit failures, reusing parent scaffold.
  - **Workload composition harmonized (explicit amendment to resolve VF6):** Evaluated workload for staleness metrics =180 fresh (12 trajectories ×15 no drift) +30 stale (3 families ×2 trajectories ×10 with DRIFT_POINT=6 =>5 fresh+5 stale per traj:10 stale per family =>30 stale) +150 noise (15 trajectories ×10, 5 per variant A phone p=0.3, B nickname p=0.3, C email null p=0.2+phone p=0.3) =360 evaluated (pool 210 staleness +150 noise). Executed total =390 includes 30 auxiliary pre-drift fresh (2 per family x5 fresh) required for V5 within-family std>0 and V14 per-trajectory caching, disclosed same as parent harmonization; stale_rate evaluated 30/210=0.1428, executed pool 30/240=0.125 both within [0.00,0.18] and [stale_rate±0.07]. Repair evaluated on 30 stale instances (10 per family). B-COLD: 12 fresh trajectories ×1 re-exploration each (discovery 3 fetches + execution) =12 cold measurements executed (not asserted). Unrelated mechanisms for contamination: N=20 distinct resource ids 9000-9019 not perturbed, cloned registry, re-verified post-patch via _matches.
  - **Drift families (orthogonal, single-resource, blast radius=1):**
    1. `dom_drift`: 2 trajectories ×10 =20 (10 stale), Jaccard required-filtered {id,name,email} 0.60-0.75 <0.85 via id int->str + optional phone add.
    2. `param_header_mutation`: 2 trajectories ×10 =20 (10 stale), mutation via response `_template` detail->uid and X-Csrf-Token abc123->xyz789, response-derived detection.
    3. `cache_expiry`: 2 trajectories ×10 =20 (10 stale), ETag SHA256 change + max-age 60->0, ETag_changed AND max-age=0 detection.
  - **Repair patch (deterministic, no LLM, executed):** stale detected (UNKNOWN 0.85) => re-observe 1 probe, delta live vs cached response-derived signals, overwrite cache, rebind, re-verify via _matches. Cost =1 browser +4 base =5 units vs cold 16.
  - **Random-patch null executed unclamped:** for each stale instance sample field-set/param/header value from different family uniformly, apply to clone, verify via _matches (expected false 0/30), compute binary AUROC pooled (1.0), precision at 0.85 (1.0), and permutation-shuffled label AUROC distribution (1000 shuffles) 0.40-0.60 unclamped.
  - **Retrieval baseline executed:** Jaccard 0.30 TFIDF retrieval over 12 fresh trajectory caches, pick nearest, attempt replay via _matches without patch, log success (expected 0.20-0.40).
  - **Distributed secondary policy:** DEFERRED. Not executed. Runtime health-gated Flask/JWT/WAL n>=800 stage logged as NOT_ATTEMPTED with dependency `runtime health-gated substrate (shared WAL /tmp/spider-runtime/*/shared.db WAL/journal_mode, 2x gunicorn 23 + nginx 1.24 HS256, If-None-Match 304, distinct X-Worker-Pid>=2)`; if health-gate later passes, identical thresholds will be re-evaluated.
  - No real network, no LLM API key required, no Docker for primary; seeds deterministic (port ephemeral, trajectory order fixed, perturbation seeds fixed via hashlib but not for scores).

---

## 7. Holdout

- **Within-trajectory holdout (per-trajectory observed):** Fresh requests 1-5 per stale trajectory are cache source for that trajectory's mechanism; stale requests 6-10 held out for detection+repair test. No overlap request_number between cache and test; no global template leakage — cache per-trajectory observed, not precomputed. Repair patch derived from live observation of held-out requests only.
- **Train/test split for verification threshold (fixes VF1):** Verification AUROC/precision threshold (staleness confidence 0.85) calibrated on TRAIN split (18 instances: 6 per family, trajectory 0 per family) and evaluated on TEST split (12 instances: 4 per family, trajectory 1 per family) using binary _matches outcomes (1 for correct patch verify true, 0 for random patch verify false). Random-patch null similarly split. No post-state leakage into threshold fitting (threshold frozen pre-execution at 0.85). Precision at 0.85 reported, not at 0.60; Hanley-McNeil/DeLong bootstrap 5000 for AUROC CI disclosed even if degenerate.
- **Cross-family holdout:** Each family 10 stale held separately (per-family TP/repair success reported) to prevent header/body conflation; family-stratified trajectory-grouped bootstrap preserves family proportions (180 fresh +10 per family stale +150 noise +30 repair). Contamination unrelated set disjoint ids 9000-9019.
- **Leave-one-family-out robustness (exploratory but preregistered as auxiliary):** compute repair success when training threshold/patch logic on 2 families and testing on 3rd, to check generalization beyond family-specific delta.
- **No website holdout (synthetic):** Claim ceiling bounded to locally-hosted synthetic; not C-CROSSSITE. Distributed holdout deferred.

---

## 8. Nulls / Baselines (strong, matched tasks, all executed not hardcoded)

All baselines run on same rebalanced 360 evaluated /390 executed synthetic workload (and same 30 repair instances where applicable) for matched comparison with identical honest counter, server state, and deterministic _matches:

- **B-COLD-FULL-REEXPLORATION (primary cost baseline, executed):** Empty registry, rediscover from 3 observations, then execute. Must show success >=90% at full cost ~16 units (12 discovery+4 execution) and 3 browsers. Repair must beat by <50% tokens and <40% browser. Previously asserted; now executed for 12 trajectories.

- **B-NO-GUARD-REPLAY (safety baseline, recomputed from logs):** No freshness guard, always EXECUTABLE, verbatim replay on 30 stale. Must show FA~1.0 (30/30) delta vs SPIDER >=0.15 fails without guard, contamination high. Validated via request logs.

- **B-VERBATIM-REPLAY (0-cost replay, executed):** No repair probe, stored mechanism executed unchanged via _matches. Must show 0% success post-perturbation (proving perturbation breaking), 0 cost; else family MEASUREMENT_INVALID.

- **B-RETRIEVAL-RAG (strong retrieval, now EXECUTED not 0.30 hardcoded):** Jaccard 0.30 TFIDF retrieval over prior trajectories + nearest replay via _matches (cost 1+4), no patch. Expected 20-40% success; repair must exceed by >=30pp and lower contamination. Fixes VF5.

- **B-JACCARD-ONLY (signal ablation, recomputed):** Only DOM Jaccard <0.85 ignores header/cache. Expected FA~0.66 fails 2 families, proving combined detection needed.

- **B-HEADER-ONLY (signal ablation, recomputed):** Only header/cache + template ignores DOM. Expected FA~0.33 fails 1 family, complementary.

- **B-ORACLE-HAND-PATCH (ceiling, ground truth):** Ground-truth minimal patch (1 probe+1 verify=5 units, 100% success). Measured deterministic repair should approach exactly 1.0x on this substrate (disclosed definitional).

- **Positive control PC-LOCALIZED-REPAIR-SUCCEEDS (executed):** PC1 unperturbed 100% and PC2 oracle patch >=90% per family with cost ratio <0.50; if fails => MEASUREMENT_INVALID. Fixes VF3.

- **Null controls executed:** NC-ZERO (zero perturbation cost 0 contamination 0 executed), NC-RANDOM-PATCH unclamped (random incorrect patch false_accept <=0.05, binary AUROC 1.0 pooled, permutation-shuffled AUROC 0.40-0.60), NC-NOISE-IMMUNITY (150 churn noise FA<=0.10). Fixes VF3/VF2.

Strong baseline justification: beating no-guard by delta >=0.15 necessary-but-weaker; beating both single-signal ablations by 0.33-0.66 and verbatim 0% while approaching oracle 1.0x distinguishes true localized repair from pooled-metric salience or trivial replay; executing retrieval (not 0.30) ensures repair adds value beyond retrieval memory; re-verified contamination on N>=20 distinguishes locality from global invalidation; permutation null proves verification discrimination not hash artefacts.

---

## 9. Primary Metrics & Decision Rule (frozen, satisfies 7 required_fixes)

**Stable metric IDs (MUST be reused verbatim in result.json:metrics and controls):**

- `M-TN-SPIDER` = TN/(TN+FP) on 180 fresh (210 fresh executed variant) — freshness preservation
- `M-TN-WILSON-LOWER` = Wilson lower z=1.96 for M-TN-SPIDER
- `M-FALSE-ACCEPT-SPIDER` = # stale EXECUTABLE/30 — false accept at ~14% stale
- `M-FALSE-ACCEPT-WILSON-UPPER` = Wilson upper for FA (0/30 upper 0.1135)
- `M-UNKNOWN-RATE-SPIDER` = # UNKNOWN / staleness pool (30/210=0.1428 evaluated, 30/240=0.125 executed harmonized) 
- `M-ECE-SPIDER` global, `M-ECE-FRESH`, `M-ECE-STALE` per-class ECE recalibrated 0.95/0.85
- `M-REPAIR-SUCCESS-POOLED` = # repairs verify true via _matches /30 (pooled)
- `M-REPAIR-SUCCESS-PER-FAMILY-{dom_drift,param_header_mutation,cache_expiry}` = per-family success n=10 each + Wilson lowers
- `M-REPAIR-COST-TOKENS-MEAN` = mean honest sum-counter tokens per repair (5) and `M-REPAIR-COST-TOKENS-RATIO` = repair / B-COLD (5/16=0.3125); bootstrap CI
- `M-REPAIR-BROWSER-MEAN` = mean browser steps per repair (1) and `M-REPAIR-BROWSER-RATIO` = 1/3=0.333
- `M-REPAIR-VERIFY-STEPS-MEAN` = mean verification steps per repair (1)
- `M-CONTAMINATION-POOLED` = # unrelated mechanisms false_accept after patch /20 pooled (re-verified via _matches on registry clone, not asserted) 
- `M-CONTAMINATION-PER-FAMILY` + Wilson uppers
- `M-VERIFICATION-AUROC` = AUROC from binary _matches outcomes correct patch (1) vs random patch (0) on TEST (pooled 1.0), `M-VERIFICATION-AUROC-RANDOM-PERMUTED` = permutation-shuffled label AUROC 0.40-0.60 unclamped, `M-VERIFICATION-PRECISION` at frozen 0.85, `M-VERIFICATION-RECALL` at 0.85
- `M-VERIFICATION-PASS-CORRECT` = 30/30 correct patches verify true, `M-VERIFICATION-PASS-RANDOM` = 0/30 random patches verify true
- `M-AMORTIZED-COST-F10` = 15 tokens (5+10*1) vs `M-COLD-COST-F10`=16 single (or 160 for 10), `M-AMORTIZED-BROWSER-F10`=1 (1+10*0) vs `M-COLD-BROWSER-F10`=3, honest frozen cost model retrieval browser 0
- `M-M-TOTAL` trajectory aggregates
- Honesty: `M-RHO-SHUFFLED-MAX` max|rho| 1000 trajectory-grouped perms primary <0.20, `M-RHO-SHUFFLED-MEAN` auxiliary, `M-COST-VECTOR-STD` 0, `M-WITHIN-FAMILY-STD-MIN-FRESHNESS` 0.5
- Baselines: `M-FA-B-NO-GUARD`=1.0, `M-SUCCESS-B-VERBATIM`=0.0, `M-SUCCESS-B-RETRIEVAL-RAG` executed, `M-FA-B-JACCARD-ONLY`=0.6667, `M-FA-B-HEADER-ONLY`=0.3333, `M-ORACLE-COST`=5, `M-COLD-COST-TOKENS-MEAN`=16 `M-COLD-BROWSER-MEAN`=3
- Bootstrap: 5000 family-stratified trajectory-grouped 95% percentile CIs for all primary metrics (`M-BOOTSTRAP-TN-CI`, `M-BOOTSTRAP-FA-CI`, `M-BOOTSTRAP-REPAIR-POOLED-CI`, `M-TOKEN-RATIO-BOOT-CI`, `M-BROWSER-RATIO-BOOT-CI`, `M-CONTAMINATION-BOOT-CI`, `M-AUROC-BOOT-CI`), width for non-degeneracy disclosure
- Freshness family metrics: `M-TP-FAMILY-{dom_drift,param_header_mutation,cache_expiry}` + Wilson

**Frozen decision rule (satisfies 7 required_fixes, see spec.json:decision_rule):**

- **PRIMARY SURVIVES_CURRENT_TEST iff ALL D1-D10 hold:**
  - D1 PC1 1.0 executed and PC2 >=0.90 per family executed, else MEASUREMENT_INVALID (fixes VF3)
  - D2 NC1 0/0 executed and NC2 random-patch false_accept<=0.05 executed with binary AUROC 1.0 and permutation null 0.40-0.60 unclamped and NC-NOISE FA<=0.10, else MEASUREMENT_INVALID (fixes VF1/VF2/VF3)
  - D3 freshness TN>=0.85 Wilson lower>0.75 and FA<=0.10 and UNKNOWN in [0.00,0.18]∩[stale_rate±0.07] and global/per-class ECE<=0.15, else FALSIFIED
  - D4 repair success >=0.80 pooled (24/30) Wilson lower>0.65 and >=0.70 per family bootstrap lower>0.60
  - D5 mean tokens <0.50*cold and browser <0.40*cold and verify steps <=2 bootstrap upper <0.55/<0.45
  - D6 contamination <0.10 pooled re-verified and per-family <0.15 Wilson upper<0.20 (fixes VF5 contamination assert)
  - D7 verification AUROC>=0.75 and precision>=0.80 at frozen 0.85 on TEST via binary _matches, random delta AUROC>=0.25, Hanley-McNeil CI disclosed (fixes VF1 score fabrication at 0.60 threshold)
  - D8 amortized 15<16 tokens and 1<3 browser at f=10 honest cost model retrieval browser 0, comparator 3 not 12, no invented retrieval browser (fixes VF4)
  - D9 B-NO-GUARD FA - SPIDER FA >=0.15 and B-NO-GUARD FA>0.10 and each single-signal ablation fails >=1 family
  - D10 honesty V2-V6: constant integer per-trajectory-reset counter, max|rho_shuffled|<0.20 trajectory-grouped (1000 perms), within-family freshness std>0, 5000 family-stratified trajectory-grouped bootstrap done (not instance-level), per-trajectory caching+response-derived, verification deterministic _matches, Wilson informative (fixes VF6/VF7)
- **FALSIFIED-IN-SETTING if any D3-D9 fails while D1-D2 and D10 pass** (valid scientific negative).
- **MEASUREMENT_INVALID if any D1-D2 or D10 fails or N<30 stale or per-family n<10 or unrelated N<20 or any control hardcoded/clamped/rigged.**
- **MIXED if family-heterogeneous.**
- **DISTRIBUTED CONDITIONAL DEFERRED:** Logged as NOT_ATTEMPTED_MEASUREMENT_DEFERRED, does not override synthetic PRIMARY; health-gated n>=800 stage is future VALIDATED blocker.
- **INCONCLUSIVE only if primary CIs straddle thresholds with width>0.20 due to underpower at n=30.**

Recalibration satisfiability proof frozen: With 180 fresh at 0.95 and 30 stale at 0.85, global ECE 0.0643 <0.15 (180*0.05/210=0.0429+30*0.15/210=0.0214), per-class fresh 0.05 stale 0.15 at threshold passes, UNKNOWN 0.1428 <0.18 passes; evaluated pool 30/210 and executed 30/240 both within [0.00,0.18] and [stale_rate±0.07]; repair cost 5 vs cold 16 ratio 0.3125 <0.50, browser 1 vs 3 ratio 0.333 <0.40 satisfiable.

---

## 10. Uncertainty Method

- **Wilson CI** for proportions (TN, TP, FA, repair success, contamination, precision) z=1.96 raw counts; lower for TN/success, upper for FA/contamination; at n=10 per family disclose exact Wilson (7/10 lower 0.39, 9/10 lower 0.60, 0/20 upper 0.161), at pooled 24/30 lower 0.65, 0/30 upper 0.1135.
- **Trajectory-grouped family-stratified bootstrap (B=5000) FIXED to trajectory level:** resample with replacement at trajectory level (12 fresh trajs 15 each=180, 6 stale trajs 2 per family x10 with 5+5, 15 noise trajs 10 each=150, plus 30 repairs 10 per family, and 20 unrelated mechanisms), stratified by family preserving proportions, recompute TN, FA, UNKNOWN, ECE, repair success, token/browser ratios, contamination, AUROC, precision per resample → percentile 95% CI (2.5th,97.5th). Non-degeneracy required: width>0 to claim precision; degenerate [1.0,1.0] flagged as ceiling effect (audit VF7), Wilson provides informative width. Previously instance-level within family (lines 872-883) is replaced.
- **Honesty null:** max|rho_shuffled| via 1000 perms trajectory-grouped (shuffle whole trajectory blocks' cost vectors vs outcomes for repair success and for M_total vs freshness); report max primary <0.20 and mean auxiliary. Cost std 0 exempted but perm still run.
- **Verification AUROC uncertainty FIXED:** From binary _matches outcomes (not hash scores), compute AUROC via sklearn-equivalent on binary predictions (correct 1 vs random 0) giving 1.0; report Hanley-McNeil / DeLong bootstrap 5000 CI disclosure noting degenerate zero variance (all correct 1, all random 0) yields CI [1.0,1.0] but permutation-shuffled null (labels shuffled 1000 perms) yields 0.40-0.60 as discriminant proof. Previously hash-injected 0.78-0.99 vs 0.10-0.50 and 0.60 threshold are replaced by binary at 0.85.
- **Adequacy rule:** N=30 stale +12 cold +20 unrelated ensures Wilson sensitivity at 0.80 pooled (half-width ~0.14) while per-family 10 gives informative per-family bound (7/10 lower 0.39); bootstrap 5000 preserves family strata. If N smaller => MEASUREMENT_INVALID.
- **Distributed uncertainty:** DEFERRED; same Wilson+5000 bootstrap will apply at n>=800 non-304 health-gated stage when runtime substrate hardened.

---

## 11. Falsification / Survival Rule

- Positive `PRIMARY SURVIVES` upgrades bounded ceiling from synthetic freshness EXPERIMENTAL (TN 1.0 FA 0.0) to synthetic delta-repair EXPERIMENTAL with honest instrumentation (executed PC/NC, unclamped null, trajectory-grouped rho, honest D8 1<3, executed retrieval) contamination-bound localized repair (<50% tokens, <40% browser, AUROC>=0.75, contamination<0.10 re-verified, amortized Pareto at f=10). Validates that freshness guard enables honest repair economics and authorizes runtime to harden distributed shared-WAL to n>=800 for VALIDATED. Does NOT promote to VALIDATED/PRODUCT_CORE (needs distributed n>=800 + real LLM/Playwright audit PASS per registry); param-inherit pilots remain PARKED.
- Negative `FALSIFIED` bounded to this signal/threshold/site/substrate/patch/confidence with honest gates passing: C-DELTA-REPAIR remains HYPOTHESIS/BLOCKED on synthetic, does NOT imply impossibility with orthogonal workflow-IR/endpoint-catalog levels, multi-resource, Redis, or real LLM repair — but proves cheapest deterministic patch not sufficient/cheap/local on this substrate with honest measurement. Product must retain full replay budgeting and not rely on delta-repair for economics; honest Pareto remains inflated (freshness does not imply delta-repair, per Director contamination>=0.10 triggers full replay).
- `MEASUREMENT_INVALID` means honest-cost, trajectory-grouped rho, 5000 trajectory-grouped bootstrap, per-trajectory cache, response-derived endpoint, or executed PC/NC/retrieval failed; or N insufficient; or any control hardcoded/clamped/rigged; no claim update for that gate, must not be cited as falsification; distributed stage INVALID does not retroactively falsify synthetic gate.
- `MIXED` family-heterogeneous outcome reports per-family ceilings (e.g., dom_drift survives while cache_expiry fails due to ETag AND logic).

---

## 12. Validity Threats & Mitigations (including 7 audit fixes)

- **Threat: Manufactured verification scores (VF1) — hash-derived 0.78-0.99 vs 0.10-0.50 giving AUROC 0.9967 at 0.60 threshold.** Mitigated by required_fix 1: recompute AUROC/precision/recall from deterministic _matches binary outcomes at frozen 0.85 threshold (correct 30 true vs random 0 true), TRAIN 18 / TEST 12 split, Hanley-McNeil CI disclosure, report precision/recall at 0.85 (recall ~0.58 at 0.85 if using prior hash ranges, but binary 1.0/0.0 gives precision 1.0 recall 1.0 at 0.85 when threshold is binary). No hash scores.
- **Threat: Clamped null AUROC (VF2) 0.4803 in [0.40,0.60] via force-clamp that cannot fail.** Mitigated by required_fix 2: unclamped random-patch null — generate random incorrect patches from wrong family, verify via _matches (expected 0/30 false_accept <=0.05), compute binary AUROC 1.0 pooled, and permutation-shuffled label AUROC 0.40-0.60 (1000 perms) as null discriminant; never clamp into range.
- **Threat: Hardcoded PC1/PC2/NC1 constants (VF3) 1.0 that cannot fail.** Mitigated by required_fix 3: execute PC1 (12 fresh unperturbed verifies), PC2 per-family oracle patches, NC1 zero-perturbation (10 fresh without mutation) via actual runs, log rates and costs; D1/D2 now falsifiable.
- **Threat: D8 amortized browser rigged (VF4) 11<12 with cold_browser*4 comparator and invented retrieval browser 1.** Mitigated by required_fix 4: honest frozen cost model — retrieval 1 token 0 browser, repair browser 1, amortized tokens 5+10*1=15<16, browser 1+10*0=1<3 vs cold 3, comparator 3 not 12, recorded M-AMORTIZED-BROWSER-F10=1 not 11; gate not wired to pass.
- **Threat: Fabricated retrieval baseline (VF5) 0.30 # approx.** Mitigated by required_fix 4: execute B-RETRIEVAL-RAG via Jaccard 0.30 TFIDF retrieval + replay via _matches for 30 stale instances, log measured success (expected 0.20-0.40) not hardcoded.
- **Threat: Sampling deviation 390 vs 360 (VF6) shifting stale_rate 0.1428 vs 0.125 and UNKNOWN/ECE proof.** Mitigated by required_fix 5: formally harmonize to 360 evaluated /390 executed with 30 auxiliary pre-drift fresh disclosed, staleness pool 210 evaluated (30/210=0.1428) and 240 executed (30/240=0.125) both within [0.00,0.18] and [stale_rate±0.07]; D3 UNKNOWN window covers both, ECE proof 0.0643 vs 0.0625 both <0.15; frozen spec now matches execution.
- **Threat: Repair bootstrap not trajectory-grouped (VF7) instance-level within family.** Mitigated by required_fix 6: 5000 family-stratified trajectory-grouped bootstrap resampling at trajectory/family level (12+6+15 trajectories), not instance resampling lines 872-883; degenerate CIs still [1.0,1.0] but procedure correct.
- **Threat: Structurally guaranteed repair success (VF8) definitional copy-and-rebind at 5 units matching oracle 1.0x.** Mitigated by disclosure: D4/D5 numbers support only narrow ceiling 'copy-live-bytes-and-rebind at 5 units restores _matches' not general repair; safeguard is honest random-patch null (now unclamped binary) proving verification discriminates correct vs incorrect patch (VF1/VF2 fixes) and re-verified contamination (fix 7); claim ceiling bounded accordingly.
- **Threat: Honesty gates vacuous (VF9) constant cost std 0 → rho 0.0 tests only no injected variance.** Disclosed: gate tests no jitter only, not graded cost discrimination; amortized Pareto D8 (now honest) required for economics; per-family freshness std 0.5 satisfies discrimination.
- **Threat: Tautological verification (stale==true by construction then verify true after re-observe).** Disclosed ceiling: verification tests self-consistency, not learned param induction; but random-patch null (now binary 0/30 false) must fail verification (precision 1.0) to prove verification not vacuous; AUROC gate ensures this.
- **Threat: Degenerate CIs [1.0,1.0]/[0.0,0.0] masking precision.** Mitigated by Wilson informative bounds (FA upper 0.1135, TN lower 0.982) and requiring width>0 disclosure; deterministic ceiling flagged not claimed as high precision.
- **Threat: Contamination asserted 0 not re-verified (required_fix 7).** Mitigated by required_fix 7: contamination measured on registry clone snapshot isolation (clone before perturbation, patch on clone, re-verify 20 unrelated ids 9000-9019 via _matches post-patch), not asserted constants lines 728-730.
- **Threat: Amortization arithmetic mixed bases.** Fixed per VF4 honest model with consistent per-trajectory-reset sums.
- **Threat: Synthetic-to-real/distributed gap (51-streak MEASUREMENT_INVALID).** Disclosed: primary stdlib flat JSON only, bounded to localhost single-resource deterministic patch; distributed health-gated n>=800 explicitly DEFERRED as dependency runtime, not conflated; claim remains synthetic EXPERIMENTAL.

---

## 13. Estimated Cost & Information Gain

- **Cost:** Primary synthetic delta-repair honest low (~360 evaluated +30 auxiliary +30 repairs +12 cold + retrieval, 5000 trajectory-grouped bootstraps +1000 perms <15 min CPU, <0.9 compute-hour, no LLM/browser/Docker, <$1). No distributed cost (deferred). Reuses parent scaffold plus fixes 7 audit failures (~50 lines changed). Total bounded <1 compute-hour.
- **Gain:** Very high per Director REOPEN comparative reasoning: directly tests neglected blocking claim (C-DELTA-REPAIR 5 prior BLOCKED/MEASUREMENT_INVALID, sole freshness SURVIVES prerequisite TN 1.0 FA 0.0, blocks C-RESIDUAL-NOVELTY honest M_total_f10 Pareto and C-PRODUCT-ECON). Honest instrumentation makes result discriminating: either SURVIVES with honest economics (executed PC/NC, unclamped null, trajectory-grouped bootstrap, honest D8) validates freshness enables contamination-bound repair and unblocks VALIDATED distributed gate and honest M_total_f10 context, or FALSIFIES with honest gates proves freshness does not imply delta-repair (contamination>=0.10 re-verified) and forces product to budget full replay — both materially change next graph/runtime/product decision per Director mandate vs alternatives (durable param-inherit 8 MEASUREMENT_INVALID marginal info ~0, immediate distributed degenerate [1.0,1.0] predicted MEASUREMENT_INVALID). Minimal deterministic single-resource test isolates locality without LLM BLOCK, harvesting synthetic leverage before distributed cost, and resolves prior manufactured artefacts so negative is scientific not infra.

---

## 14. Execution Scope & Code Paths

- **Allowed roots:** `research/graph`, `research/harness` per `research/lanes/registry.json:graph.allowed_code_roots` (cumulative operational inheritance, fragments, parameterization, semantic resolution, freshness boundaries).
- **Planned harness:** `research/graph/delta_repair/execute_delta_repair_synthetic_35952148696.py` (new, ~450 lines, deterministic repair with honest fixes: binary _matches AUROC at 0.85 TRAIN/TEST, unclamped random null with permutation, executed PC1/PC2/NC1, executed Jaccard 0.30 retrieval, trajectory-grouped bootstrap 5000, trajectory-grouped perm 1000, re-verified contamination via clone, honest D8) reusing `research/graph/freshness_detection/execute_rebalanced_35947468747.py` scaffold for server (`http.server.HTTPServer` 127.0.0.1 ephemeral, ETag SHA256[:16], Cache-Control, _template/X-Csrf-Token) and `src/spider/kernel.py` _matches verification. Also helper `research/harness/synthetic_single_resource_server.py` if refactor. Raw evidence to `research/experiments/EXP-GRAPH-35952148696/raw_evidence/` with `execution_results.json`, `request_logs.json`, `metrics.json`, `decision.json`, `cost_logs.json`, `bootstrap_ci.json`, `per_trajectory_cache.json`, `repair_logs.json`, `contamination_logs.json`, `verification_auroc.json` (binary outcomes + perm null), and `health_gate.json` (DEFERRED marker). SHA256 per artifact. No nginx/Flask/WAL/Playwright/openai required for primary.
- **Freezing:** `freeze.json` will hash request/spec/prereg before execution; EXECUTE must not mutate frozen inputs; any pre-freeze work inconsistent with Director mandate superseded per architecture; distributed stage deferred does not require freeze violation. Exact 360/390 harmonization frozen here prevents VF6 deviation.
- **Dependencies:** runtime honest sum-counter (already satisfied per parent V2-V4) and health-gated distributed substrate (`C-MEAS-VALID` HS256 shared-WAL) listed as dependency but DEFERRED — not required for synthetic PRIMARY SURVIVES; secondary stage gated, logged as NOT_ATTEMPTED, not BLOCKED.
- **Signals frozen pre-execution:** threshold 0.85, DRIFT_POINT=6, deterministic server mutations (id int->str/phone, _template detail->uid, X-Csrf-Token rotation, ETag+max-age 60->0), confidence 0.95/0.85, UNKNOWN bound [0.00,0.18]/[stale_rate±0.07], max rho procedure (1000 trajectory-grouped), noise stimulus p-values, per-trajectory cache size 3, verification threshold 0.85 TRAIN 18 / TEST 12 split, repair cost units (4 fresh/5 repair), retrieval cost 1 token 0 browser, n_reuses=10 for amortized, permutation null 1000 shuffles.

---

## 15. Prereg Timing & Transmission Discipline

Frozen before any outcome-bearing measurement for this experiment_id. Prior evidence cited is from Codex, `research/experiments/EXP-GRAPH-35947468747/*` and `35949562506` audit/handoff (MEASUREMENT_INVALID with 7 required_fixes), and `request.json:director_mandate` agent priors (labeled as prior not SPIDER evidence), not from new data. No material fact will exist only in Actions logs; all evidence paths/hashes will be in packet. Control/metric IDs frozen here will be reused verbatim in `result.json:metrics/controls` and `audit.json:recomputed_metrics` for downstream transmission. Status=COMPLETE with outcome FALSIFIES/MIXED is valid negative, not infrastructure failure; status=BLOCKED/MEASUREMENT_INVALID reserved for honesty/infra failure (hardcoded controls, clamped null, rigged D8) per packet §4, never encoded as falsification; distributed stage DEFERRED does not override synthetic PRIMARY. Number of staleness pool 30 and repair 10 per family chosen for realistic 14% prevalence power and per-family Wilson sensitivity (0/30 upper 0.1135, 10/10 lower 0.7225), not post-hoc. All 7 audit required_fixes are frozen as discriminating safeguards so downstream audit can verify execution vs hardcoded constants.

---

*Prereg follows SPIDER_MASTER_PROMPT.md §19 and Research 2.0 binding packet `research/EXPERIMENT_PACKET.md` §§3-5. DESIGN performed without outcome-bearing measurements per AGENTS.md work discipline. Director mandate is binding research direction; parent handoff is continuity evidence with established/rejected/unknown/do_not_assume preserved per transmission discipline.*
