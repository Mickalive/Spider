# EXP-GRAPH-35940399935 — Single-Resource Deterministic Freshness Guard (REOPEN)

**Lane:** graph · **Claim:** C-FRESHNESS · **Mode:** EXECUTE (frozen design)  
**Experiment ID:** EXP-GRAPH-35940399935 · **Director mandate:** REOPEN C-FRESHNESS per `request.json:director_mandate` comparative reasoning vs WebArena pilots (expected repeat MEASUREMENT_INVALID) and vs PARKED  
**Parent handoff:** `EXP-GRAPH-35937576511/handoff.json` SHA 5b1652f... MEASUREMENT_INVALID — preserved four-way distinction not re-tested as hypothesis, director disposition USE  
**Frozen hashes:** request 9b5ff151 spec 6ad01edf prereg 9010e1fd freeze 2026-09-24T00:57:15

---

## Summary

After the five measurement-validity fixes, the same single-resource deterministic freshness guard (`Jaccard<0.85 OR param_template_changed OR (ETag_changed AND Cache-Control max-age=0)`) **SURVIVES_CURRENT_TEST** on the locally-hosted synthetic flat-JSON site `/resource/{id}` (stdlib `http.server` on 127.0.0.1 ephemeral). All nine frozen decision-rule conditions D1–D9 pass including the satisfiable recalibrated operating point (prevalence-aware UNKNOWN bound, 0.95/0.85 confidence, per-class ECE).

This is a bounded synthetic ceiling only (not VALIDATED/PRODUCT_CORE, needs n≥800 + real-API/distributed shared-WAL). It unblocks downstream C-DELTA-REPAIR contamination-bound and C-RESIDUAL-NOVELTY honest sum-counter experiments on the same substrate without distributed WAL.

---

## Method (frozen per spec/prereg, no outcome-adaptive change)

**Site:** single resource `/resource/{id}` only, stdlib `http.server` no Docker/network/LLM/browser/distributed. 3 staleness families orthogonal in separate trajectories, header/body/cache signals separated.

**Sampling (frozen):**
- DRIFT_POINT=6 per trajectory (req 1-5 fresh, 6-10 stale)
- dom_drift: 6×10=60 (30 fresh+30 stale) server changes body `id` int→str + adds `phone`, Jaccard on sorted `(field_path,type)` required-filtered `{id,name,email}` <0.85
- param_header_mutation: 6×10=60 server mutates endpoint in RESPONSE `_template.query_params` `detail→uid` and `X-Csrf-Token` `abc123→xyz789`, detected via endpoint_template equality on response body/header names (not client dict)
- cache_expiry: 6×10=60 server changes `ETag=SHA256(filtered_body)[:16]` + `Cache-Control max-age 60→0`, detected via `etag_changed AND max-age=0`, `If-None-Match` returns 304 only when fresh ETag matches (deterministic, marked not stale)
- stable control: 3×10=30 always fresh
- NC-NOISE-IMMUNITY 15 extra fresh trajectories (5 per churn variant ×10=150 all fresh ground truth): A phone p0.3, B nickname p0.3, C email null p0.2 + phone p0.3 — field unused by mechanism via required-path filtering and NoneType→string normalization, `etag_changed` alone without `max-age=0` not flagged
- Total staleness N=210 (120 fresh+90 stale, stale_rate 0.4286) + noise 150 =360 requests

**Mechanism:** `GET /resource/${resource_id}?detail=${detail}` with `X-Csrf-Token`. Distilled literal mechanism via `distill` (no param induction under test). Verification via `src/spider/kernel.py:_matches(required,actual)` exact equality on postconditions filtered without `_template`.

**Per-trajectory observed caching (FIX-6b):** `per_trajectory_cache.json` 36 trajectories, each cached from first valid of requests 1-3 per trajectory (not single global precomputed). `dom_tokens_cached` filtered required, `header_tokens`, `endpoint_template` from response-derived `_template` + header `X-Csrf-Token`. Conditional 304 path exercised deterministically.

**Honest sum-counter (FIX-1):** per-trajectory-reset integer `resolve+bind+verify+freshness+browser_steps(0)` base 4 per request constant, no `traj_idx%2` parity, no `f*6.0`/`n*3200`/`n*4096`, no jitter/bijective proxy. Logged per request and per-trajectory sum in `cost_logs.json`. Vector std 0 is VALID per V2 narrowing (V5 applies only to outcome-bearing freshness/accuracy, stable exempted).

**Rho (FIX-2/3):** `M-RHO-SHUFFLED-MAX` as max `|Pearson rho|` over 1000 permutations shuffling whole trajectory blocks (trajectory-grouped preserving within-dependence) between shuffled cost labels and outcome, mean auxiliary. Require max <0.20.

**ECE (FIX-5 recalibration):** 10 equal-width bins `[0,0.1)...[0.9,1.0]` on recalibrated confidence 0.95 fresh EXECUTABLE /0.85 stale UNKNOWN. Global `ECE = sum_b |acc_b-conf_b|*n_b/N` ≤0.15 and per-class `ECE_fresh`/`ECE_stale` each ≤0.15. UNKNOWN bound prevalence-aware `[0.00,0.50]` capped and `[stale_rate-0.05, stale_rate+0.07]=[0.3786,0.4986]` satisfiable (stale_rate 0.4286).

**Bootstrap:** 5000 family-stratified trajectory-grouped percentile 95% CIs resampling trajectory groups preserving family proportions, Wilson z=1.96 on raw counts.

---

## Results (RAW → OBSERVATION → DERIVED → INTERPRETATION preserved)

**Raw evidence:** `raw_evidence/execution_results.json` 360 logs with `ground_truth`, `family`, `request_number`, `trajectory_id`, `url`, `response_body` (with `_template`), `ETag`, `Cache-Control`, `X-Csrf-Token`, `jaccard`, `param_header_changed`, `etag_changed`, `spider_status`, `spider_confidence`, `verified`, `cost`, `status_code`; `per_trajectory_cache.json` 36 entries; `cost_logs.json`; `bootstrap_ci.json`; `decision.json` SHA fbc62ce.

**Observations (direct):**
- TN 120/120 fresh retained EXECUTABLE, FP 0
- TP 90/90 stale flagged UNKNOWN, FN 0
- Per-family `dom_drift` 30/30 fresh TN +30/30 stale TP, `param_header_mutation` 30/30 +30/30, `cache_expiry` 30/30 +30/30, `stable` 30/30 fresh TN
- Noise 150/150 fresh retained EXECUTABLE (50+50+50 per variant)
- UNKNOWN count 90/210 staleness pool
- ECE bins: `[0.8,0.9]` n90 stale acc1.0 conf0.85 contrib0.0643, `[0.9,1.0]` n120 fresh acc1.0 conf0.95 contrib0.0286, others n0
- Cost vector 360×4
- Rho permutations 1000 trajectory-grouped

**Derived measurements (metrics.json):**
- `M-TN-SPIDER 1.0 Wilson lower 0.969` on 120/120
- `M-FALSE-ACCEPT-SPIDER 0.0 Wilson upper 0.0409` on 0/90
- `M-UNKNOWN-RATE-SPIDER 0.4286`
- `M-ECE-SPIDER 0.0929`, `M-ECE-FRESH 0.05`, `M-ECE-STALE 0.15`
- `M-COST-SPIDER-SUM 1440` `M-RHO-SHUFFLED-MAX 0.0` `M-RHO-SHUFFLED-MEAN 0.0` `M-RHO-OBSERVED 0.0`
- `M-WITHIN-FAMILY-STD-MIN-FRESHNESS 0.5`, `M-FA-NOISE 0.0`, `M-TN-NOISE 1.0`
- Baselines: `B-NO-GUARD FA 1.0 delta 1.0`, `B-JACCARD-ONLY FA 0.6667 TP 30/90`, `B-HEADER-ONLY FA 0.3333 TP 60/90`
- Bootstrap 95% CIs: `TN [1.0,1.0]`, `FA [0.0,0.0]`, `unk [0.4286,0.4286]`, `ECE [0.0929,0.0929]` degenerate at ceiling but valid per non-degenerate freshness std gate

**Interpretation (decision rule D1–D9, all must pass for SURVIVES):**
- D1 TN≥0.85 and Wilson lower>0.75: **PASS** 1.0 and 0.969
- D2 false_accept ≤0.10: **PASS** 0.0 upper 0.0409
- D3 UNKNOWN in [0.00,0.50] and [0.3786,0.4986]: **PASS** 0.4286
- D4 global ECE≤0.15 and per-class fresh ≤0.15 and stale ≤0.15: **PASS** 0.0929, 0.05, 0.15 (stale at threshold)
- D5 false_accept_NO_GUARD - false_accept_SPIDER ≥0.15 and false_accept_NO_GUARD>0.10: **PASS** 1.0 delta
- D6 per-family TN≥0.75 and TP≥0.85 for each 3 families: **PASS** all 1.0 lower 0.8865
- D7 PC TP≥0.85 per family: **PASS** 1.0 each
- D8 NC-FRESH TN≥0.85 and NC-NOISE FA≤0.10: **PASS** stable 1.0, noise 0.0
- D9 honesty gates integer constant sum-counter without parity, max|rho|<0.20 trajectory-grouped, within-family freshness std>0, 5000 bootstrap done, per-trajectory caching and response-derived endpoint verified: **PASS** (cost all_int true, max rho 0.0, freshness min 0.5, 36 caches, _template response-derived, 304 handled)

**Frozen falsifier:** none of F1–F7 triggered; honesty gates M1–M8 all pass ⇒ not MEASUREMENT_INVALID ⇒ **SURVIVES_CURRENT_TEST** (`status=COMPLETE`, `outcome=SUPPORTS`).

---

## Controls (frozen IDs reused verbatim)

`B-NO-GUARD` large delta 1.0 discriminating but weak (TN 1.0 on fresh pool, FA 1.0 on stale pool) — necessary-but-weak baseline beaten.  
`B-JACCARD-ONLY` FA 0.6667 captures only dom_drift (TP 30/90).  
`B-HEADER-ONLY` FA 0.3333 captures param_header+cache (TP 60/90) but misses dom_drift.  
Combined signal necessary; orthogonality per director prior 6 demonstrated (not mere threshold tweak).  
`PC-STALE-DETECTION` all 1.0 per family; `NC-FRESH-RETAIN` 1.0; `NC-NOISE-IMMUNITY` 0.0 on 150 structural-noise fresh requests (required-filtered Jaccard stays 1.0, etag change without max-age=0 not flagged, email null normalized to string).  
Honesty: trajectory-grouped max rho 0.0 with constant cost closes prior `n*3200`/`f*6.0`/parity tautology; within-family freshness std 0.5 preserves discrimination signal; per-trajectory caching and response-derived endpoint close prior client-internal self-comparison and global-template gaps.

---

## Validity & Limitations

**Passes:** V1 deterministic `_matches`, V2 honest constant sum-counter (std 0 valid), V3 no jitter, V4 trajectory-grouped max rho, V5 freshness std>0 (cost exempted, stable exempted), V6 5000 bootstrap, V7 Wilson, V8 recalibrated ECE+UNKNOWN satisfiable, V9 single-resource isolation, V10 deterministic response-derived signals, V11 family-stratified, V12 local synthetic, V13 ground-truth logging, V14 per-trajectory observed caching + response-derived endpoint + 304 handling, V15 orthogonal-levels audit (ablations fail as frozen).

**Representation loss disclosed:** DOM field-set tokens ignore value magnitudes/nested depth beyond flat keys and normalize `NoneType→string` for noise email-null; ETag truncated 16 hex; endpoint template ignores param value semantics; per-trajectory cache uses first valid of 3 observations; required-path filter `{id,name,email}` excludes optional `phone`/`nickname` for Jaccard — intentional isolation to test structural vs optional noise boundary; Jaccard threshold 0.85 frozen pre-execution; cache_expiry requires `etag_changed AND max-age=0` (ETag change alone not stale).

**Ceiling:** Bounded synthetic POC on stdlib `http.server` flat JSON only. Does not claim cross-site, multi-resource, or production CDN/Flask/JWT/WAL/CDN/session rotation. `C-FRESHNESS` remains HYPOTHESIS per registry gate (needs n≥800 + real-API/distributed health-gated shared-WAL). Does not authorize WebArena-Verified v2 param-inherit re-attempt until runtime honest-WAL substrate health-gated.

**CIs degenerate:** TN/FA ` [1.0,1.0]`/`[0.0,0.0]` reflect perfect detection at deterministic ceiling (120/120, 90/90) not high-precision estimation; reported as ceiling effect, validity via non-degenerate freshness std 0.5 and Wilson lower/upper.

---

## Product Consequences

Per `spec.json:product_consequence_positive`: C-FRESHNESS single-resource staleness detection **survives at bounded synthetic ceiling** with honest constant sum-counter, recalibrated calibration, trajectory-grouped max rho<0.20, and noise-immunity. This unblocks downstream `C-DELTA-REPAIR` contamination-bound and `C-RESIDUAL-NOVELTY rho_novelty≥0.60` with honest `M_total_f10` Pareto on same synthetic substrate without distributed WAL; does not yet promote to VALIDATED/PRODUCT_CORE.

Any reuse gating at this 0.85 threshold with 0.95/0.85 confidence is authorized only within this signal/site/threshold scope and with prevalence-aware UNKNOWN handling.

---

## Reproduction

Artifacts in `raw_evidence/` with SHA256 in `provenance.json` and `result.json:artifacts`. Code paths: `research/graph/freshness_detection/execute_single_resource_staleness.py` (SHA ef8b3460), `src/spider/kernel.py` (SHA 46929b3a). Command: `python research/graph/freshness_detection/execute_single_resource_staleness.py` (<10 min CPU, 360 requests). Frozen inputs immutable per `freeze.json`. No material fact outside packet.

---

*Prereg timing: frozen before outcome-bearing measurement per AGENTS.md. Transmission discipline: stable IDs reused verbatim for AUDIT/DIRECTOR, RAW→OBSERVATION→MEASUREMENT→INTERPRETATION distinct, measurement-invalid not encoded as falsification.*
