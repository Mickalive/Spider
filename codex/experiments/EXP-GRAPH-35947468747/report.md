# EXP-GRAPH-35947468747 — Rebalanced synthetic freshness at 15% stale (graph lane)

**Experiment ID:** EXP-GRAPH-35947468747  
**Lane:** graph — C-FRESHNESS  
**Status:** COMPLETE  
**Outcome:** SUPPORTS (PRIMARY SURVIVES synthetic-rebalanced) with DISTRIBUTED_MEASUREMENT_INVALID secondary  
**Frozen inputs:** request `43e79ba7`, spec `cfe1e040`, prereg `3c8fe385`, freeze 2026-09-24T02:34:28Z  
**Execution:** `research/graph/freshness_detection/execute_rebalanced_35947468747.py` (sha fde76caf) on stdlib http.server, 390 requests, 5000 bootstrap, honest sum-counter 4

---

## 1. Frozen question → execution

Director mandate CONTINUE C-FRESHNESS: on same locally-hosted synthetic single-resource flat-JSON substrate with honest per-trajectory-reset sum-counter and deterministic `_matches` verification, does the validated freshness guard (Jaccard 0.85 required-filtered + response-derived endpoint _template/X-Csrf-Token + ETag+max-age=0, recalibrated 0.95 fresh/0.85 stale) sustain TN≥0.85 FA≤0.10 calibrated (global/per-class ECE≤0.15, UNKNOWN prevalence-aware) at realistic 15% stale prevalence with non-degenerate Wilson/bootstrap CIs and NC-NOISE-IMMUNITY, and when health-gated transferred to distributed shared-WAL Flask/JWT+nginx at n≥800 non-304, vs no-guard baseline, thereby testing synthetic EXPERIMENTAL → VALIDATED step before C-DELTA-REPAIR and honest M_total_f10 Pareto?

**Execution sampling (discrepancy disclosed):** spec says 180 fresh +30 stale +150 noise =360 (30/210=0.1428). Execution produced 210 fresh +30 stale =240 staleness pool +150 noise =390 total: 12 stable trajs ×15 =180 fresh plus 2 per drift family ×10 =60 (30 fresh pre-drift +30 stale at DRIFT_POINT=6) plus 15 noise trajs ×10 =150 (5 per variant). Stale_rate actual 30/240=0.125 vs expected 0.1428, delta 0.0178 within tolerance, UNKNOWN 0.125 satisfies both actual [0.075,0.195] and expected [0.0928,0.18] intersect [0.00,0.18]. The extra 30 fresh pre-drift are required for V5 freshness std>0 and per-trajectory observed caching (first 3), and are correctly counted as fresh not hidden. Wilson TN lower for 210 vs 180 is 0.982 vs 0.979 both >0.75; FA upper 0.1135 identical at n_stale=30 (<0.18). Family-stratified bootstrap correctly preserves 12+2+5 trajectories.

---

## 2. RAW EVIDENCE (separate from derived)

Raw evidence paths/hashes in `result.json:artifacts` and `raw_evidence/`:

- `execution_results.json` 390 request logs with ground_truth, response_body, ETag, Cache-Control, X-Csrf-Token, _template, jaccard, param/header/etag flags, spider_status/confidence, verified
- `request_logs.json` same plus cost_logs
- `metrics.json` derived metrics (TN, FA, UNKNOWN, ECE, per-family, baselines, within_std, wilson)
- `bootstrap_ci.json` 5000 bootstrap CIs
- `cost_logs.json` per-trajectory sums (12 stable sums 60, drift/noise sums 40, total 1560)
- `per_trajectory_cache.json` 33 trajectories (6 drift +12 stable +15 noise) observed from first valid of 1-3, response-derived
- `health_gate.json` / `distributed_metrics.json` distributed health check

Server: `http.server.HTTPServer` on 127.0.0.1 ephemeral, path `/resource/{id}` deterministic drifts: dom_drift id int→str + phone Jaccard 0.5, param_header_mutation _template detail→uid + X-Csrf-Token abc123→xyz789, cache_expiry ETag SHA256[:16] changed + max-age 60→0 with If-None-Match 304 deterministically marked not stale. All verified via `src/spider/kernel.py:_matches` exact equality on required_slots filtered without `_template`.

Cost: constant integer 4 per request = resolve(1)+bind(1)+verify(1)+freshness(1)+browser_steps(0), per-trajectory reset, no jitter, no n*3200/f*6.0, no parity, all_int true, vector std 0.0 valid per V2 narrowing.

---

## 3. OBSERVATIONS (direct, not interpretations)

- **TN_SPIDER 1.0** (210/210 fresh EXECUTABLE) Wilson lower **0.982** >0.75, upper 1.0, per-family stable 180/180 lower 0.9791, drift pre-drift fresh 10/10 each lower 0.7225
- **false_accept 0.0** (0/30 stale EXECUTABLE) Wilson upper **0.1135**, lower 0.0, per-family TP 1.0 (10/10 each) lower 0.7225 >0.60
- **B-NO-GUARD FA 1.0** (30/30) delta vs SPIDER **1.0** ≥0.15
- **B-JACCARD-ONLY FA 0.6667** TP 10/30 only dom_drift 10/10, param_header 0/10 cache 0/10
- **B-HEADER-ONLY FA 0.3333** TP 20/30 param_header 10/10 cache 10/10 dom 0/10
- **UNKNOWN 0.125** (30/240) Wilson [0.089,0.1728] width 0.083 within [0.00,0.18] and within actual stale window [0.075,0.195] and expected [0.0928,0.18]
- **ECE global 0.0625** ≤0.15, per-class fresh 0.05 ≤0.15, stale 0.15 at threshold, bins [0.8,0.9] n30 stale conf 0.85 contrib 0.0188, [0.9,1.0] n210 fresh conf 0.95 contrib 0.0438, proof 210*0.05/240=0.0438 +30*0.15/240=0.0188 =0.0625
- **NC-NOISE-IMMUNITY FA 0.0** (0/150) TN 1.0 (150/150) across 50 per variant
- **Honest counter:** all_int true, vector std 0.0, trajectory sums 40/60, total 1560
- **Trajectory-grouped max |rho| 0.0** <0.20 (1000 perms shuffling whole blocks 12+2+5), mean 0.0, observed 0.0
- **Within-family freshness std min 0.5** >0 for 3 drift families (dom 0.5 param 0.5 cache 0.5), stable/noise 0.0 exempted
- **Bootstrap 5000** TN [1.0,1.0] FA [0.0,0.0] unk [0.125,0.125] ECE [0.0625,0.0625] — degenerate at deterministic ceiling; Wilson intervals are non-degenerate (TN lower <1.0, FA upper >0, UNKNOWN width 0.083)
- **Per-trajectory caching:** 33 trajectories, observed_count 1-3 first valid, response-derived endpoint via `_template` field and X-Csrf-Token header vs cached response, 304 exercised and not flagged
- **Distributed:** health_gate_pass **false**, wal_exists false, X-Worker-Pids [], JWT false, 304 false, n_non304 0 <800 → **DISTRIBUTED_MEASUREMENT_INVALID**

---

## 4. DERIVED MEASUREMENTS (decision rule D1-D9)

Frozen decision_rule PRIMARY SURVIVES iff ALL D1-D9:

- **D1 TN≥0.85 and Wilson lower>0.75:** 1.0 ≥0.85 and 0.982 >0.75 → **PASS** (210/210 gives 0.982; spec expectation 180/180 gives 0.979 both pass)
- **D2 false_accept≤0.10:** 0.0 ≤0.10 (Wilson upper 0.1135 reported) → **PASS**
- **D3 UNKNOWN in [0.00,0.18] and [stale_rate±]:** 0.125 in [0.00,0.18] and in [0.075,0.195] actual and [0.0928,0.18] expected → **PASS**
- **D4 global ECE≤0.15 and per-class ≤0.15:** 0.0625, 0.05, 0.15 all ≤0.15 → **PASS**
- **D5 B-NO-GUARD delta≥0.15 and FA>0.10:** 1.0 ≥0.15 and 1.0>0.10 → **PASS**
- **D6 per-family TN≥0.75 and TP≥0.85:** all drift families 1.0 ≥ thresholds → **PASS** (min Wilson lower 0.7225 at n=10 still >0.60 positive control)
- **D7 PC per-family TP≥0.85:** 1.0 each → **PASS**
- **D8 NC-FRESH-RETAIN TN≥0.85 and NC-NOISE FA≤0.10:** 1.0 and 0.0 → **PASS**
- **D9 honesty gates V2-V6:** cost_all_int true, fresh_std 0.5>0, max|rho| 0.0<0.20, 5000 bootstrap done, per-trajectory caching 33≥33 and response-derived `query_params` present, N 210≥180 and 30≥30, Wilson non-degenerate width>0 → **PASS** (bootstrap degenerate noted as ceiling, not gating falsification per F8)

**Overall PRIMARY:** all D1-D9 true → **SURVIVES_CURRENT_TEST** (synthetic-rebalanced). `falsified_in_setting` false, `measurement_invalid` false for primary.

**DISTRIBUTED CONDITIONAL:** V-DIST-HEALTH-GATE fails (false) and V-DIST-N-SUFFICIENCY n=0<800 → **DISTRIBUTED_MEASUREMENT_INVALID** for that stage, per spec does not override synthetic SURVIVES.

---

## 5. INTERPRETATION (distinct from observations)

The combined DOM+header/cache guard remains satisfiable at realistic 12.5% stale prevalence (spec target 15% 0.1428): TN 1.0 FA 0.0 calibrated at recalibrated 0.95/0.85 with per-class ECE at thresholds, UNKNOWN prevalence-aware, and strong discrimination vs no-guard (delta 1.0) and vs single-signal ablations (JACCARD 0.6667, HEADER 0.333). Signal necessity stays orthogonal (not pooled salience). Honest constant sum-counter and trajectory-grouped max rho 0.0 close prior cost tautology; degenerate bootstrap is deterministic ceiling not precision, but Wilson upper 0.1135 <0.18 provides informative bound at n_stale=30 (per spec F8).

This upgrades C-FRESHNESS from degenerate 42.8% synthetic EXPERIMENTAL (prior TN 1.0 FA 0.0 but UNKNOWN 0.428 and degenerate CIs) to non-degenerate honest prevalence-aware EXPERIMENTAL with Wilson non-degenerate width 0.083 and realistic stale sparsity. It does **not** promote to VALIDATED/PRODUCT_CORE: that requires health-gated distributed shared-WAL at n≥800 with audit PASS, which is correctly flagged DISTRIBUTED_MEASUREMENT_INVALID here.

Product consequence positive (bounded): synthetic-rebalanced SURVIVES unblocks bounded C-DELTA-REPAIR contamination-bound localized repair and honest M_total_f10 Pareto on same synthetic substrate without distributed WAL, per director mandate dependencies. No product promotion authorized; WebArena add_to_cart param-inherit pilots remain PARKED until kernel durability and distributed WAL gates pass.

---

## 6. Validity threats & mitigations

- Prevalence inflation prior 42.8% → mitigated by rebalanced 12.5% with prevalence-aware [0.00,0.18] and actual [0.075,0.195]; still satisfiable.
- Degenerate CIs → Wilson TN 0.982 and FA 0.1135 non-degenerate width>0 mitigate; bootstrap degenerate [1.0,1.0] disclosed as ceiling effect via freshness std 0.5, not claimed as precision.
- Jitter/n*3200 tautology → constant integer 4, trajectory-grouped max rho 0.0 with whole-block shuffling.
- Header/body conflation → single-resource isolation, orthogonal 10 per family, ablations fail as expected, response-derived _template isolation.
- Pooled-metric salience → family-stratified bootstrap and per-family TP 1.0 at n=10 (requires 9/10) reported.
- ECE impossibility → recalibrated 0.95/0.85 proof 0.0625 <0.15, per-class at thresholds.
- n_stale=30 power → Wilson upper 0.1135 <0.18 still informative; point FA 0.0 ≤0.10 governs, not upper ≤0.10.
- Tautological verification → disclosed: _matches is self-consistency, not learned distill_parameterized.
- Synthetic-to-distributed gap → disclosed: primary stdlib flat JSON only; distributed stage correctly invalid, not conflated.
- Sampling 390 vs 360 → disclosed: extra 30 fresh pre-drift required for V5/caching, stale_rate 0.125 vs 0.1428 both valid.

---

## 7. Economics & next steps

Cost primary <0.6 compute-hour, 390 requests at ~0.3s, 5000 bootstraps CPU-only <2 min, <$1, no LLM/browser/Docker. Distributed stage cost zero due to health-gate fail, logged as invalid per V-DIST.

**Do not promote C-FRESHNESS.** Next highest-information steps per parent handoff: (a) run bounded C-DELTA-REPAIR and honest M_total_f10 Pareto on same synthetic substrate with honest counter (now unblocked); (b) runtime lane harden health-gated distributed shared-WAL (SQLite WAL at /tmp/spider-runtime/*/shared.db, 2×gunicorn+nginx HS256, operational 304) and re-run this guard rebalanced to 12.5-15% at n≥800 to reach VALIDATED; (c) keep WebArena pilots PARKED.

---

*All control/metric IDs frozen from prereg reused verbatim; no material fact exists only in Actions log; artifacts hashed in result.json/provenance.json.*
