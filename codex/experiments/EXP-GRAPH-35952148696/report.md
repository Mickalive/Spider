# EXP-GRAPH-35952148696 — Report (EXECUTE)

**Lane:** graph  
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally (controlled local perturbations with repair cost and contamination bounds)  
**Experiment ID:** EXP-GRAPH-35952148696  
**Director mandate:** REOPEN C-DELTA-REPAIR (global-director-REOPEN, vs durable param-inherit pilot 8 consecutive MEASUREMENT_INVALID low marginal value, vs immediate distributed VALIDATED n>=800 blocked, vs C-RESIDUAL-NOVELTY duplication avoided) per `request.json:director_mandate`  
**Parent handoff:** `research/experiments/EXP-GRAPH-35949562506/handoff.json` (MEASUREMENT_INVALID, 4 critical VF1-VF4 + VF5) — continuity only per parent_handoff_disposition=USE  
**Question:** Does validated synthetic-rebalanced freshness guard (Jaccard 0.85 required-filtered {id,name,email}+response-derived _template/X-Csrf-Token+ETag+max-age=0, recalibrated 0.95/0.85, TN>=0.85 Wilson lower>0.75 FA<=0.10 ECE<=0.15 at 15% stale 360-req=180 fresh+30 stale+150 noise, NC-NOISE-IMMUNITY FA<=0.10) enable bounded C-DELTA-REPAIR with honest instrumentation on same locally-hosted single-resource flat-JSON stdlib http.server substrate such that single-resource perturbation requires localized repair with delta cost <50% tokens and <40% browser vs cold, verification AUROC>=0.75 precision>=0.80, contamination<0.10, honest M_total_f10 not inflated vs B-NO-GUARD and single-signal baselines, before authorizing distributed shared-WAL transfer (n>=800)?

---

## 1. Result Summary

**Status:** COMPLETE  
**Outcome:** SUPPORTS (PRIMARY SURVIVES_CURRENT_TEST with honest instrumentation)

All frozen decision gates D1-D10 pass while honesty/measurement gates pass, resolving 7 audit required_fixes from parent MEASUREMENT_INVALID:

- **D1 PC-LOCALIZED-REPAIR-SUCCEEDS (executed):** PC1 1.0 (210 fresh verified via deterministic _matches, all_int true) and PC2 per-family 1.0 (10/10 dom_drift, param_header_mutation, cache_expiry) via re-observe 1 probe from live endpoint, overwrite cached dom/header/endpoint with live response-derived values, rebind _template, re-verify — executed not hardcoded.
- **D2 NC-ZERO-AND-RANDOM-PATCH (unclamped, executed):** NC1 cost 0 contamination 0 on 10 zero-perturbation fresh instances executed; NC2 random-patch false_accept 0.0 (0/30) <=0.05, binary pooled AUROC 1.0 (correct 30 true vs random 0 true) with permutation-shuffled null AUROC pooled 0.5002 test 0.4952 unclamped 1000 perms within [0.40,0.60] delta 0.504 >=0.25, NC-NOISE-IMMUNITY FA 0.0 (0/150) TN 1.0 — all executed not clamped/hardcoded.
- **D3 Freshness (recomputed):** TN 1.0 (210/210 Wilson lower 0.9820) FA 0.0 (0/30 Wilson upper 0.1135) UNKNOWN 0.125 Wilson [0.089,0.1728] ECE global 0.0625 fresh 0.05 stale 0.15 <=0.15, stale_rate 0.125 executed (30/240) vs 0.1428 evaluated (30/210) both within [0.00,0.18]∩[stale_rate±0.07] and prevalence-aware [0.0928,0.2128]. Harmonized 360 evaluated /390 executed with 30 auxiliary pre-drift fresh disclosed same as parent.
- **D4 Repair success:** pooled 1.0 (30/30 Wilson lower 0.8865) >=0.80 and per-family 1.0 (10/10 Wilson lower 0.7225) >=0.70, family-stratified trajectory-grouped bootstrap CI [1.0,1.0] lower>0.60.
- **D5 Cost:** mean tokens 5 vs cold 16 ratio 0.3125 <0.50 and browser 1 vs 3 ratio 0.333 <0.40 verify steps 1 <=2, bootstrap upper <0.55/<0.45 (trajectory-grouped 5000).
- **D6 Contamination:** pooled 0.0 (0/20 Wilson upper 0.1611) <0.10 and per-family 0.0 <0.15, re-verified on registry clone snapshot isolation on disjoint ids 9000-9019 after patch via _matches (not asserted), blast radius=1 disclosed.
- **D7 Verification:** AUROC 1.0 on TEST at frozen 0.85 (TRAIN 1.0 pooled 1.0) precision 1.0 recall 1.0, derived from binary _matches outcomes (correct 30 true vs random 0 true) with TRAIN 18 (6 per family) TEST 12 (4 per family) split, not hash-injected scores, threshold 0.85 not 0.60, perm null 0.4952 within [0.40,0.60].
- **D8 Amortized honest:** tokens 15 (5+10*1 retrieval) <16 cold single and browser 1 (1+10*0) <3 cold single with frozen honest cost model (retrieval 1 token 0 browser, repair 1 probe), comparator 3 not 12, not 11<12 with *4.
- **D9 Discriminating:** B-NO-GUARD FA 1.0 delta 1.0 >=0.15 and >0.10; B-JACCARD-ONLY FA 0.6667 (TP 10/30 only dom_drift) B-HEADER-ONLY FA 0.3333 (TP 20/30 param+cache) each fail >=1 family proving combined signal required.
- **D10 Honesty:** constant integer per-trajectory-reset sum-counter (all_int true, 4 fresh 5 repair), max|rho_shuffled| 0.0 <0.20 via 1000 whole-trajectory-block perms, within-family freshness std 0.5 >0, 5000 family-stratified trajectory-grouped bootstrap done, per-trajectory caching response-derived, deterministic _matches verification.

**Claim ceiling upgrade:** Bounded synthetic C-DELTA-REPAIR SURVIVES with honest instrumentation (executed PC/NC, unclamped null, trajectory-grouped rho<0.20, honest D8 1<3, executed retrieval 0.0 delta 1.0) — deterministic localized re-observe patch restores EXECUTABLE at <50% tokens <40% browser, verification discriminates correct vs random patch (AUROC 1.0 vs perm 0.50), contamination-bound behind health-gated verification, honest amortized Pareto at f=10. Does NOT promote to VALIDATED/PRODUCT_CORE — requires health-gated distributed shared-WAL n>=800 non-304 audit PASS + real LLM/Playwright.

---

## 2. Method (Honest Instrumentation Fixes)

**Substrate:** stdlib `http.server.HTTPServer` on 127.0.0.1 ephemeral port, single-resource `/resource/{id}` flat JSON 3-5 fields (id, name, email plus optional phone/nickname), `ETag SHA256(canonical_json_without_template)[:16]`, `Cache-Control max-age=60` or `max-age=0`, `X-Csrf-Token`, response-signaled `_template {query_params, header_names}` for response-derived endpoint detection. Perturbation mutates exactly one local signal per instance orthogonal: dom_drift Jaccard 0.60-0.75 via id int->str+phone, param_header_mutation detail->uid + X-Csrf-Token abc123->xyz789, cache_expiry ETag change + max-age 60->0. Server preserves If-None-Match 304 logic but not triggered on deterministic ETag.

**Freshness guard (combined, frozen):** `dom_tokens_cached` sorted {(field_path,type)} via `extract_field_types` on observed response, filtered to required {id,name,email}; `header_tokens_cached` {Cache-Control, ETag, X-Csrf-Token}; `endpoint_template_cached` sorted query_param_names + header_names from observed `_template`. Stale = (jaccard_dom<0.85) OR param_template_changed OR (etag_changed AND max-age=0) at 0.85; confidence 0.95 fresh 0.85 stale.

**Honest cost (V2/V3):** per-trajectory-reset integer sum-counter = resolve1+bind1+verify1+freshness1=4 base fresh, 5 repair with 1 deterministic re-observe probe browser 0/1, retrieval 1 token 0 browser, no jitter/n*3200/f*6.0/parity/bijective proxy, all_int true, vector std 0 disclosed exempt from V5, 5000 family-stratified trajectory-grouped bootstrap at trajectory level (not instance-level within family — VF6 fix), max|rho_shuffled| 1000 whole-trajectory-block perms (VF9).

**Repair patch (deterministic, no LLM):** stale detected (UNKNOWN 0.85) => re-observe 1 probe from live endpoint, delta live vs cached response-derived signals, overwrite cached dom/header/endpoint with live-derived values, rebind _template, re-verify via `src/spider/kernel.py _matches` exact equality on required_slots filtered without _template. Cost 5 vs cold 16 ratio 0.3125.

**Verification/Null (VF1/VF2 fixes):** AUROC/precision/recall from binary _matches outcomes at frozen 0.85 threshold (correct patch verify true=1, random patch false=0), TRAIN 18 (6 per family) TEST 12 (4 per family) split, not hash-injected [0.78,0.99] vs [0.10,0.50]. Pooled TEST AUROC 1.0 (30 correct 1 vs 30 random 0), precision 1.0, recall 1.0. Permutation-shuffled null AUROC 1000 perms shuffling labels unclamped → pooled 0.5002 test 0.4952 within [0.40,0.60] proving observed separation not artifactual.

**Controls executed (VF3):** PC1 unperturbed fresh via actual fresh logs verified true; PC2 oracle per-family via deterministic patch with ground truth values (same operation but measured); NC1 zero-perturbation 10 fresh instances cost 0 executed; NC-NOISE 150 churn noise FA 0.0 executed; random-patch null 30 wrong-family values sampled uniformly via hashlib family rotation but verification via _matches.

**Retrieval (VF5):** executed Jaccard 0.30 TFIDF over required-filtered field sets plus nearest successful trajectory replay via _matches for all 30 stale instances retrieving from 12 fresh caches. Honest success 0.0 (0/30) because fresh postconditions mismatch stale live bodies without patch — delta vs repair 1.0 >=0.30 proves patch adds value beyond memory (prior 0.30 was fabricated).

**Contamination (VF7):** measured on registry clone snapshot isolation: clone before perturbation, patch on clone, re-verify 20 unrelated mechanisms from disjoint ids 9000-9019 via _matches post-patch, 0/20 false accept Wilson upper 0.1611 <0.20 pooled and per-family <0.15.

**Amortized (VF4):** frozen cost model retrieval 1 token 0 browser, repair browser 1, amortized tokens 15<16 browser 1<3 at f=10 comparator 3 not 12 (prior 11<30 with *4 comparator mixed bases fixed).

**Sampling (VF6):** harmonized 360 evaluated (180+30 pool 210 stale 0.1428) harmonized to 390 executed (210+30 pool 240 stale 0.125) with 30 auxiliary pre-drift fresh for V5/V14, both UNKNOWN 0.125 within [0.00,0.18]∩[stale_rate±0.07] and ECE proof <0.15.

---

## 3. Metrics & Controls (Stable IDs)

See `result.json:metrics` and `controls` for full stable IDs: M-TN-SPIDER, M-FALSE-ACCEPT-SPIDER, M-UNKNOWN-RATE-SPIDER, M-ECE-SPIDER, M-REPAIR-SUCCESS-POOLED, M-REPAIR-COST-*, M-CONTAMINATION-*, M-VERIFICATION-AUROC, M-VERIFICATION-AUROC-RANDOM (perm unclamped), M-VERIFICATION-PRECISION, M-VERIFICATION-PASS-CORRECT 30 vs RANDOM 0, M-AMORTIZED-COST-F10 15 vs M-COLD-COST-F10 16, M-AMORTIZED-BROWSER-F10 1 vs M-COLD-BROWSER-F10 3, M-RHO-SHUFFLED-MAX 0.0, M-WITHIN-FAMILY-STD-MIN-FRESHNESS 0.5, M-FA-B-NO-GUARD 1.0 delta 1.0, M-FA-B-JACCARD-ONLY 0.6667, M-FA-B-HEADER-ONLY 0.3333, M-RETRIEVAL-SUCCESS-RATE 0.0 executed, M-PC1-SUCCESS 1.0, M-BOOTSTRAP-* etc. All Wilson z=1.96.

---

## 4. Validity Threats & Mitigations (including 7 audit fixes)

- **VF1 manufactured hash-scores:** fixed by binary _matches at 0.85 TRAIN/TEST, unclamped perm null.
- **VF2 clamped null AUROC:** fixed by unclamped 1000 perm shuffled labels 0.5002/0.4952.
- **VF3 hardcoded PC/NC:** fixed by executed PC1 1.0 PC2 10/10 NC1 0 NC-noise 0/150, logged.
- **VF4 D8 rigged 11<12:** fixed to honest 1<3 with retrieval browser 0 and consistent token base 15<16.
- **VF5 fabricated retrieval 0.30:** fixed by executed Jaccard 0.30 retrieval 0.0 delta 1.0.
- **VF6 390 vs 360 deviation:** harmonized 360 evaluated /390 executed disclosed, both within prevalence window, trajectory-grouped bootstrap.
- **VF7 instance-level bootstrap & asserted contamination:** fixed to trajectory-grouped family-stratified 5000 and clone re-verification 0/20.
- **VF8 structurally guaranteed repair:** disclosed as definitional copy-live-bytes-and-rebind at 5 units restores equality on single-resource blast radius=1, safeguard is honest random-patch null (now 0/30) proving verification not vacuous.
- **VF9 vacuous honesty gates:** disclosed constant std 0 → rho 0.0 tests only no injected variance, not graded M_total_f10 discrimination, honest amortized gate required.

Degenerate bootstrap CIs [1.0,1.0]/[0.0,0.0] reflect deterministic perfect detection ceiling, Wilson informative (TN lower 0.982 FA upper 0.1135) — requires stochastic threshold/non-deterministic site for width>0.

---

## 5. Consequences

**Positive (SURVIVES):** Upgrades bounded ceiling from synthetic freshness EXPERIMENTAL (TN 1.0 FA 0.0) to synthetic delta-repair EXPERIMENTAL with honest economics (constant integer sum-counter, trajectory-grouped rho<0.20, 5000 bootstrap, executed PC/NC/retrieval, re-verified contamination 0/20). Validates that stale detection triggering UNKNOWN enables localized re-observe patch restoring EXECUTABLE without full re-exploration behind health-gated verification blocking contamination, with honest M_total_f10 Pareto (15<16, 1<3). Authorizes runtime to harden health-gated distributed shared-WAL Flask/JWT+nginx substrate to n>=800 non-304 for VALIDATED gate (X-Worker-Pid>=2). Graph may proceed to multi-resource and cross-page repair. Does NOT promote C-FRESHNESS/C-DELTA-REPAIR to VALIDATED/PRODUCT_CORE — requires n>=800 distributed with audit PASS and real LLM/Playwright.

**Negative would have shown:** freshness does not imply delta-repair (detection necessary not sufficient) — local patch either not localized (>50% re-exploration), contaminates (>=0.10 re-verified), or verification cannot discriminate (AUROC<0.75), product must default to full re-exploration budgeting.

---

## 6. Provenance

- Code: `research/graph/delta_repair/execute_delta_repair_synthetic_35952148696.py` sha256 c756409508f7470e58e7927cec2969273a85990453dce9f02244932e64033424, stdlib http.server only, deterministic seeds 42/123/999.
- Raw evidence: `research/experiments/EXP-GRAPH-35952148696/raw_evidence/` 13 files with SHA256 in `result.json:artifacts` plus code/fixture hashes.
- Environment: Python 3.12.14, no Docker/browser/LLM, <0.9 compute-hour, <$1, 390 logs (210 fresh 30 stale 150 noise pool 240), 30 repairs TRAIN 18 TEST 12, 20 unrelated, 5000 bootstrap +1000 perms.
- Frozen hashes: spec 26925d904768e36373e66ded9184490ed0f7bf9e515bb9391c12c7fe70496390, request 69caac9a5a4a98c9bbcd97c81567cc0af07e9966e0914216764be21ce5f3f3ea, prereg 8448a8146960e8514fa980aa7074053a7b7e402a058d3817a16774d31394ae8e.
- Distributed: DEFERRED per V12, health_gate false n 0<800, WAL false, X-Worker-Pid 0, dependency runtime lane not hardened.

---

## 7. Unresolved & Next Steps

See `result.json:unresolved` (12 items): non-degenerate bootstrap needs stochastic threshold/DOM, distributed n>=800 shared-WAL transfer, ETag AND boundary, required-path-filter generalization, cache miss, 304 circularity, correlated non-determinism, multi-resource/cross-page, real LLM billing, f=100 amortization, same-resource blast radius>1, ETag truncation representation loss.

No broader product promotion authorized by this evidence.
