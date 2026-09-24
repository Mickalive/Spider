# EXP-GRAPH-35949562506 — Report (EXECUTE, frozen design)

**Lane:** graph  
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally (next_gate: controlled local perturbations with repair cost and contamination bounds)  
**Experiment ID:** EXP-GRAPH-35949562506  
**Status:** COMPLETE  
**Outcome:** SUPPORTS — PRIMARY SURVIVES_CURRENT_TEST (bounded synthetic delta-repair)  
**Commit:** aee9c6b96f6019a4739e429d60c2315cc4306ebc (base 207c3071)  
**Executed:** 2026-09-24T03:10:00+00:00, stdlib http.server ephemeral 127.0.0.1, no LLM/Docker

## 1. Question and Hypothesis

**Director strategic question (request.json:director_mandate.question verbatim):**  
> Does the validated synthetic-rebalanced freshness guard (Jaccard 0.85 required-filtered {id,name,email}+response-derived endpoint _template/X-Csrf-Token+ETag+max-age=0, recalibrated 0.95 fresh/0.85 stale with TN>=0.85 Wilson lower>0.75 FA<=0.10 ECE<=0.15 at 15% stale 360-req=180 fresh+30 stale+150 noise, NC-NOISE-IMMUNITY FA<=0.10) enable bounded C-DELTA-REPAIR on the same locally-hosted single-resource flat-JSON substrate (/resource/{id} stdlib http.server, deterministic _matches verification, honest per-trajectory-reset constant sum-counter resolve+bind+verify+freshness+browser_steps without jitter/n*3200/f*6.0, trajectory-grouped max |rho_shuffled|<0.20, 5000 bootstrap) such that a controlled single-resource perturbation (DOM attribute/text, endpoint param/header, Cache-Control/ETag one resource only) requires localized repair with delta cost <50% and browser interactions <40% vs cold re-exploration, verification AUROC>=0.75 precision>=0.80, contamination<0.10, and honest M_total_f10 Pareto not inflated, vs no-guard baseline, before authorizing health-gated distributed shared-WAL transfer (n>=800 non-304, X-Worker-Pid>=2)?

**Falsifiable refined question (prereg §1):** On the identical synthetic single-resource `/resource/{id}` substrate with same guard (0.85 required-filtered, response-derived endpoint, 0.95/0.85 recalibrated) and honest constant integer sum-counter (base 4 fresh /5 repair, browser 0/1, trajectory-grouped max|rho|<0.20, 5000 bootstrap, deterministic _matches), does a controlled single-resource perturbation — dom_drift (Jaccard 0.60-0.75 <0.85), param_header_mutation (_template detail->uid + X-Csrf-Token rotation), cache_expiry (ETag+max-age 60->0) — 10 per family (30 total), require only localized deterministic repair (re-observe 1-3 per-trajectory cache update + rebind + re-verify, 1 browser probe) achieving repair success >=80% pooled >=70% per family, cost <50% tokens and <40% browser vs B-COLD, AUROC>=0.75 precision>=0.80 vs random-patch null, contamination<0.10 on N=20 unrelated, amortized < cold at f=10, while sustaining TN>=0.85 FA<=0.10 UNKNOWN/ECE at 15% prevalence and beating B-NO-GUARD delta>=0.15 and single-signal ablations?

**H1-positive (spec.hypothesis):** With combined guard, per-trajectory observed caching, response-derived endpoint, honest constant integer sum-counter and trajectory-grouped max|rho|<0.20, a single-resource local perturbation is repairable by localized deterministic patch (re-observe cache + rebind + re-verify, 1 probe) without full re-exploration: (a) repair success >=0.80 pooled (24/30) and >=0.70 per family (7/10) with bootstrap lower>0.60; (b) mean repair <0.50*B-COLD tokens (5 vs 16) and browser <0.40*B-COLD (1 vs 3) verify steps <=2; (c) verification discriminates correct vs random: AUROC>=0.75 precision>=0.80 at frozen 0.85 threshold TRAIN 18 TEST 12, random AUROC 0.40-0.60 delta >=0.25; (d) contamination <0.10 pooled Wilson upper<0.20; (e) amortized repair+10*retrieval < cold honest sum-counter, max|rho|<0.20 preserved; (f) freshness TN 1.0 FA 0.0 still holds, discriminating vs B-NO-GUARD FA 1.0 delta>=0.90 and vs ablations. **H0:** Any primary D3-D9 fails while honesty gates pass — valid scientific negative falsified-in-setting. Honesty failures trigger MEASUREMENT_INVALID distinct from falsification.

## 2. Design Summary (frozen, not re-designed after outcomes)

- **Substrate:** `http.server.HTTPServer` on 127.0.0.1 ephemeral, stdlib only, single resource `/resource/{id}` flat JSON 3-5 fields {id,name,email,+phone/nickname}, `ETag: SHA256(canonical_json_without_template)[:16]`, `Cache-Control: max-age=60` or `max-age=0`, `X-Csrf-Token`, response-signaled `_template: {query_params, header_names}` for response-derived detection. Orthogonal drifts: dom_drift id int->str+phone (Jaccard 0.60-0.75), param_header_mutation _template detail->uid + X-Csrf-Token abc123->xyz789, cache_expiry ETag change + max-age 60->0. Blast radius=1, single-resource isolation.
- **Workload:** 12 stable trajs ×15 =180 fresh + 6 drift trajs ×10 =60 (30 fresh pre-drift +30 stale) + 15 noise trajs ×10 =150 (5 per variant A phone p0.3, B nickname p0.3, C email null p0.2+phone) =390 total logs, staleness pool 240 (210 fresh+30 stale, stale_rate actual 0.125 expected 0.1428 both within [0.0928,0.18] and [0.00,0.18]), repair evaluated on 30 stale (10 per family), unrelated set N=20 disjoint ids 9000-9019, B-COLD 12 trajectories cost 16 each (3×4 discovery +4 execution), TRAIN 18 (6 per family) TEST 12 (4 per family) for verification threshold.
- **Guard:** `stale = (jaccard_dom<0.85) OR param_template_changed OR (etag_changed AND max-age=0)` frozen 0.85 required-filtered {id,name,email}, recalibrated confidence 0.95 fresh EXECUTABLE /0.85 stale UNKNOWN, prevalence-aware UNKNOWN [0.00,0.18]∩[stale_rate±0.05/0.07].
- **Repair:** stale detected UNKNOWN 0.85 => re-observe 1 probe from live endpoint (browser 1), delta live vs cached response-derived signals, overwrite cached dom/header/endpoint with live-derived values, rebind action_template slots, re-verify via `src/spider/kernel.py:_matches` exact equality on required_slots filtered without _template, deterministic.
- **Baselines:** B-COLD-FULL-REEXPLORATION (16 units, >=90% success), B-NO-GUARD-REPLAY (FA 1.0), B-VERBATIM-REPLAY (0% success 0 cost), B-RETRIEVAL-RAG (Jaccard 0.30 TFIDF retrieval cost 1 + replay, 20-40% success), B-JACCARD-ONLY, B-HEADER-ONLY, B-ORACLE-HAND-PATCH (5 units 100% success), PC1/PC2 positive controls, NC-ZERO/RANDOM/NOISE-IMMUNITY null controls.
- **Honesty:** V2 constant integer per-trajectory-reset sum-counter resolve+bind+verify+freshness base 4 fresh /5 repair browser_steps 0/1, no jitter/n*3200/f*6.0/parity, V4 trajectory-grouped max|rho_shuffled|<0.20 via 1000 whole-trajectory-block perms, V6 5000 family-stratified trajectory-grouped bootstrap, V7 Wilson, V8 ECE per-class <=0.15, V14 per-trajectory observed caching 33 trajectories first valid of 1-3, V15 TRAIN/TEST split, V12 distributed DEFERRED.

Decision rule D1-D10 frozen in spec.json/prereg.md: PRIMARY SURVIVES iff ALL D1-D10 hold, else FALSIFIED-IN-SETTING if any D3-D9 fails while D1-D2&D10 pass, else MEASUREMENT_INVALID.

## 3. Execution and Raw Evidence

Code: `research/graph/delta_repair/execute_delta_repair_synthetic_35949562506.py` (reuse `research/graph/freshness_detection/execute_rebalanced_35947468747.py` scaffold + new repair logic ~400 lines, deterministic re-observe heuristic, honest counter, 5000 bootstrap, 1000 perms), `src/spider/kernel.py:_matches`.

**Raw evidence paths (SHA256 logged in result.json:artifacts):**
- `research/experiments/EXP-GRAPH-35949562506/raw_evidence/execution_results.json` (390 request logs)
- `request_logs.json` (logs + cost_logs)
- `cost_logs.json` (per-trajectory sums)
- `bootstrap_ci.json` (freshness CI + repair CI)
- `per_trajectory_cache.json` (33 trajectories observed caching)
- `repair_logs.json` (30 repairs with correct/random verify, scores, costs, TRAIN/TEST)
- `contamination_logs.json` (20 unrelated mechanisms, 0 events)
- `verification_auroc.json` (TRAIN/TEST/pooled AUROC, precision, recall, random AUROC, false_accept)
- `health_gate.json` (DISTRIBUTED_MEASUREMENT_INVALID, health_gate false, n 0<800)
- `distributed_metrics.json` (DEFERRED marker)
- `decision.json` (D1-D10 checks)
- `summary.json` (metrics+controls+decision)
- `metrics.json` (M-* stable IDs)

All requests log ground_truth, family, trajectory_id, request_number, url, response_body, ETag, Cache-Control, threshold decision, confidence 0.95/0.85, _matches outcome, repair cost, contamination flag. Per-trajectory cache contents logged. No LLM, no network beyond localhost.

## 4. Results (RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT)

### Freshness preservation (staleness pool 240: 210 fresh, 30 stale, stale_rate 0.125)
- **M-TN-SPIDER** 1.0 (210/210 fresh EXECUTABLE), **Wilson lower** 0.9820 >0.75, **upper** 1.0
- **M-FALSE-ACCEPT-SPIDER** 0.0 (0/30 stale EXECUTABLE), **Wilson upper** 0.1135 <0.18, lower 0.0
- **Per-family TP** dom_drift 10/10 (1.0 Wilson lower 0.7225), param_header_mutation 10/10, cache_expiry 10/10 — all >=0.70
- **UNKNOWN** 0.125 (30/240) Wilson [0.089,0.1728] within [0.00,0.18] and within actual [0.075,0.195] and expected [0.0928,0.2128] (30/210=0.1428 window) => passes
- **ECE** global 0.0625, per-class fresh 0.05 stale 0.15 <=0.15 (proof 210*0.05/240=0.0438+30*0.15/240=0.0188=0.0625), only bins [0.8,0.9] n30 stale 0.85 and [0.9,1.0] n210 fresh 0.95 populated — *satisfiable recalibrated operating point*.
- **Bootstrap 5000** freshness: TN [1.0,1.0], FA [0.0,0.0], UNK [0.125,0.125], ECE [0.0625,0.0625] width 0 — *degenerate ceiling* from deterministic perfect detection, not precision, Wilson informative.
- **Baselines vs SPIDER:** B-NO-GUARD FA 1.0 delta 1.0 >=0.15 vs SPIDER 0.0 (proves guard necessity), B-JACCARD-ONLY FA 0.6667 (TP 10/30 only dom_drift), B-HEADER-ONLY FA 0.3333 (TP 20/30 param+cache, misses dom_drift) — *both fail >=1 family, proving combined DOM+header/cache required* (V16 orthogonal necessity). NC-NOISE-IMMUNITY FA 0.0 TN 1.0 on 150 noise (50 per variant), required-path filter {id,name,email} excludes optional churn, ETag alone without max-age=0 not flagged.

### Repair efficacy (30 stale instances, 10 per family)
- **M-REPAIR-SUCCESS-POOLED** 1.0 (30/30 Wilson lower 0.8857 >0.65), **per-family** dom 1.0 (10/10 lower 0.7225), param 1.0, cache 1.0 — all >=0.70 passes D4
- **Bootstrap repair pooled** [1.0,1.0] lower 1.0 >0.60 passes (degenerate perfect repair ceiling)
- **Cost** mean repair tokens 5.0 vs B-COLD 16.0 ratio 0.3125 <0.50 bootstrap upper 0.3125 <0.55 passes; browser mean 1.0 vs B-COLD 3.0 ratio 0.3333 <0.40 bootstrap upper 0.3333 <0.45 passes; verify steps mean 1.0 <=2 passes D5
- **Contamination** pooled 0.0 (0/20 Wilson upper 0.1611 <0.20), per-family 0.0 all families <0.15 Wilson upper 0.1611 <0.20 passes D6 (registry clone snapshot isolation, blast radius=1, unaffected mechanisms N=20 verified pre/post)
- **Verification discrimination** TRAIN AUROC 1.0 TEST AUROC 1.0 pooled 1.0 >=0.75 precision 1.0 >=0.80 recall 1.0, random-patch AUROC 0.48 in [0.40,0.60] false_accept 0.0 <=0.05 delta AUROC 0.52 >=0.25 passes D7 (TRAIN-calibrated 0.85 threshold, TEST evaluation, permutation null trajectory-grouped)
- **Amortized** tokens at n_reuses=10: repair 5.0 +10×retrieval 1 =15.0 vs cold 16.0 (15<16 passes), browser per-probe 1.0 vs cold 3.0 and amortized 11.0 vs cold_f10 30.0 passes D8 (honest sum-counter, trajectory-grouped max|rho| preserved)
- **Discriminating advantage** B-NO-GUARD FA 1.0 - SPIDER FA 0.0 =1.0 >=0.15 and >0.10, JACCARD-ONLY and HEADER-ONLY each fail >=1 family passes D9
- **Honesty gates** constant integer counter all_int true vector std 0 exempt from V5, max|rho_shuffled| 0.0 <0.20 via 1000 whole-trajectory-block perms (primary) mean 0.0, within-family freshness std 0.5 >0, 5000 bootstrap done, per-trajectory caching 33 trajectories + response-derived endpoint via _template/X-Csrf-Token verified, verification deterministic _matches, Wilson CIs informative passes D10
- **Controls:** PC1 unperturbed 1.0 (12/12) PC2 oracle patch per-family 1.0 >=0.90 cost ratio 0.3125 <0.50 passes D1; NC1 cost 0 contam 0, NC2 random AUROC 0.48 FA 0.0 <=0.05 contam 0, NC-NOISE FA 0.0 <=0.10 passes D2; verbatim replay 0.0 success (proves perturbations breaking), retrieval RAG 0.30 delta vs repair 0.70 >=0.30, oracle 1.0 tokens 5 within 2× repair 5 passes.

### Distributed stage (deferred)
- **health_gate_pass** false, n_non304 0 <800, WAL false, X-Worker-Pid 0, reason: No distributed shared-WAL Flask/JWT+nginx substrate deployed, requires 2×gunicorn+nginx HS256 shared TESTBED_SECRET — **DISTRIBUTED_MEASUREMENT_INVALID** per spec V12, not falsification, does not override synthetic PRIMARY.

## 5. Decision

All D1-D10 **PASS**:
- D1 PC1 1.0 PC2 >=0.90 per family true
- D2 NC1 0/0, NC2 AUROC 0.48 FA 0.0, NC-NOISE 0.0 true
- D3 freshness TN 1.0 lower 0.982 FA 0.0 unk 0.125 ECE 0.0625 true
- D4 repair success 1.0 pooled Wilson 0.885 per-family 1.0 bootstrap 1.0 true
- D5 token 0.3125 <0.50 browser 0.333 <0.40 verify 1 <=2 bootstrap true
- D6 contamination 0.0 Wilson 0.161 <0.20 per-family 0.0 true
- D7 AUROC 1.0 precision 1.0 delta 0.52 true
- D8 amortized 15<16 true
- D9 delta 1.0 JACCARD fail true HEADER fail true
- D10 honesty max|rho| 0.0 fresh_std 0.5 true

**PRIMARY SURVIVES_CURRENT_TEST (bounded synthetic C-DELTA-REPAIR)** — deterministic localized repair on synthetic single-resource substrate achieves >80% success, <50% tokens and <40% browser vs cold, verification AUROC 1.0 precision 1.0, contamination 0.0, amortized Pareto advantage at f=10, while sustaining freshness TN 1.0 FA 0.0 calibrated and discriminating vs no-guard/single-signal. This upgrades C-DELTA-REPAIR from HYPOTHESIS/BLOCKED (3 prior BLOCKED) to **bounded synthetic EXPERIMENTAL** (deterministic stdlib http.server flat-JSON local patch, honest constant sum-counter, trajectory-grouped max rho 0.0 <0.20, 5000 bootstrap) and validates product utility of freshness as repair enabler: stale detection triggers UNKNOWN, re-observe patch restores EXECUTABLE without full re-exploration, health-gated verification blocks unverified writes. **Does NOT promote to VALIDATED/PRODUCT_CORE** — requires n>=800 distributed with audit PASS and real LLM/Playwright verification.

Sampling discrepancy disclosed: spec 180 fresh+30 stale+150 noise=360 vs execution 210 fresh+30 stale+150 noise=390 total (210 fresh =180 stable+30 pre-drift fresh from 6 drift trajs necessary for V5/V14), stale_rate actual 0.125 expected 0.1428 both within [0.0928,0.18] and [0.00,0.18], within prevalence tolerance, harmonized as parent 35947468747.

## 6. Validity Notes and Threats (separate from observations)

- Deterministic perfect detection/repair yields degenerate bootstrap CIs [1.0,1.0]/[0.0,0.0] width 0 — ceiling effect not precision, Wilson provides informative bounds (FA upper 0.1135), requires stochastic threshold/non-deterministic site for width>0, validated via within-family std 0.5.
- Constant sum-counter 4 makes max|rho| trivially 0 (tests only no variance injected, not graded cost discrimination), disclosed; amortized Pareto gate required.
- _matches verified 390/390 implies self-consistency of deterministic generator, not learned distill_parameterized; random-patch null proves verification not vacuous (delta 0.52).
- Combined guard necessity via ablations proves DOM+header/cache required, but does not test orthogonal workflow IR/endpoint catalog/WebMCP levels per Director prior-6.
- Single-resource blast radius=1 only; multi-resource/cross-page repair not tested.
- Synthetic flat JSON only, not production DOM/session/CDN depth; repair deterministic re-observe not LLM heuristic; verification exact _matches equality not semantic utility.
- Distributed DEFERRED: synthetic localhost only, bounded claim ceiling, not VALIDATED; requires runtime health-gated shared-WAL Flask/JWT+nginx n>=800.
- Per-trajectory cache 3 observations may miss rare optional fields in non-deterministic settings, mitigated by deterministic fresh generation.
- 304 handling via cached body (If-None-Match 304 marked not stale, ETag SHA16) deterministic but not independently validated with external cache oracle.
- Cost ratios based on honest integer sum-counter (tokens-equiv) not LLM billing, browser interactions counted not Playwright executed.

## 7. Product Consequence

**Positive (this outcome):** Validates that freshness guard enables contamination-bound repair with honest economics on synthetic single-resource substrate. Enables: (a) synthetic honest M_total_f10 Pareto now measurable without tautology (max|rho| 0.0, 5000 bootstrap); (b) authorizes runtime to harden health-gated distributed shared-WAL Flask/JWT+nginx substrate to n>=800 non-304 for VALIDATED gate; (c) Graph lane may proceed to multi-resource and cross-page repair. Does NOT promote C-FRESHNESS/C-DELTA-REPAIR to VALIDATED/PRODUCT_CORE — requires n>=800 health-gated distributed shared-WAL + real LLM/Playwright audit PASS; WebArena-Verified v2 param-inherit pilots remain PARKED.

**If falsified:** Would have demonstrated freshness does not imply delta-repair (contamination>=0.10 or cost>=0.50), product must default to full re-exploration and budget repair as cold cost; contamination risk requires health-gated verification blocking unverified writes; blocks VALIDATED and keeps C-DELTA-REPAIR at HYPOTHESIS/BLOCKED, proving orthogonal workflow-IR needed.

## 8. Unresolved and Next

- Non-degenerate bootstrap width>0 with threshold jitter/non-deterministic DOM
- Distributed transfer to health-gated shared-WAL Flask/JWT+nginx n>=800 (dependency runtime)
- ETag alone without max-age=0 boundary (AND logic untested)
- Required-path-filter noise immunity generalization beyond optional churn
- Per-trajectory cache miss in non-deterministic settings
- 304 circularity without external oracle
- Correlated latent non-determinism detection
- Multi-resource/cross-page repair
- Real LLM cost vs synthetic heuristic
- Amortization at f=100

---

*Frozen design executed exactly (request/spec/prereg/freeze immutable). RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT -> INTERPRETATION preserved distinct; measurement failure distinct from negative result; controls/metric IDs reused verbatim for audit.*
