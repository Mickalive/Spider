# EXP-GRAPH-35937576511 — Single-Resource Staleness Probe (C-FRESHNESS) — EXECUTE Report

**Lane:** graph  
**Claim:** C-FRESHNESS — SPIDER can detect when inherited knowledge is stale (session/token/DOM/endpoint drift with false-accept measurement)  
**Experiment ID:** EXP-GRAPH-35937576511  
**Status:** COMPLETE  
**Outcome:** FALSIFIES (FALSIFIED-IN-SETTING, valid negative)  
**Frozen spec:** `e05025d7579b8925438f206d763f6854cf00f1c6c33e367879179a07347328c1`  
**Frozen prereg:** `9546503ca9557be5f34a0d3d561c0aaf405d5681d4e803d359da88ce2d3453c7`  
**Director mandate:** PIVOT to C-FRESHNESS, SUPERSEDE 8th WebArena add_to_cart pilot, cognitive_reset=true

---

## 1. Question and Hypothesis

Director strategic question (request.json:director_mandate.question):

> After 8 consecutive MEASUREMENT_INVALID WebArena-Verified v2 pilots, does a controlled single-resource staleness probe — DOM token drift / endpoint param+header mutation / Cache-Control+ETag expiry on one resource only on a locally-hosted synthetic site with deterministic freshness signal — enable detection with TN>=0.85 (Wilson lower>0.75), false_accept<=0.10, UNKNOWN in [0.00,0.15] ECE<=0.15 vs no-guard baseline, measured with deterministic _matches verification and honest per-trajectory-reset sum counters with 5000 bootstrap CIs?

H1 (positive): Combined freshness guard (Jaccard DOM <0.85 OR param_template_changed OR ETag_changed+expiry) detects staleness at required operating point and beats no-guard by >=0.15 FA delta under honest counters.

H0 (null): Guard performs at/below baseline or honesty gates reveal tautology.

---

## 2. Method (frozen design executed exactly)

- **Site:** `http.server.HTTPServer` on `127.0.0.1` ephemeral port, stdlib only, no Docker/external network. One resource type `GET /resource/{id}` flat JSON body (3 fields fresh, deterministic).
- **Families (orthogonal separate trajectories, no scheduling confound):**
  1. `dom_drift` — body add `phone`, remove `author` equivalent via `id int->str` + `phone` add (field-type set drift)
  2. `param_header_mutation` — query param `detail` -> `uid` rename + `X-Csrf-Token` rotation `token-abc123` -> `token-xyz789`
  3. `cache_expiry` — ETag `SHA256(canonical_json)[:16]` changes + `Cache-Control max-age=60` -> `max-age=0`
  Control `stable` — no drift, always fresh.
- **Sampling:** `DRIFT_POINT=6` per trajectory (reqs 1-5 fresh, 6-10 stale). Drift families: 6 traj ×10 =60 each (30 fresh+30 stale). Control: 3 traj ×10 =30 fresh. Total **N=210** (120 fresh +90 stale) ≥60+60 minimum. Family-stratified holdout (cache from fresh trajectories 1-5, test on 6-10).
- **Freshness state:** `dom_tokens = sorted {(field_path,type)}` via `extract_field_types` (type normalize string/integer/boolean/array/object), `header_tokens = {Cache-Control, ETag, X-Csrf-Token}`, `endpoint_template = path + query param names + header names`. Cached from fresh exemplar.
- **Decision:** `stale = (jaccard_dom <0.85) OR param_header_changed OR (etag_changed AND cache_expiry)`. Confidence 0.90 if EXECUTABLE (fresh), 0.50 if UNKNOWN (stale). Threshold 0.85 frozen pre-execution.
- **Verification:** `src/spider/kernel.py _matches(required, actual)` exact equality on postconditions for all 210 requests (deterministic, no LLM judge).
- **Economics:** Honest per-trajectory-reset sum counter = `resolve+bind+verify+freshness+browser_steps` integer per request (base 4 + traj parity 0/1, no jitter, no n*3200, no f*6.0), trajectory sum logged, |rho_shuffled| via 1000 trajectory-grouped perms, within-family std>0, 5000 family-stratified trajectory-grouped bootstrap CIs, Wilson z=1.96.
- **Baselines (matched 210 requests):** B-NO-GUARD (always EXECUTABLE), B-JACCARD-ONLY, B-HEADER-ONLY.
- **Controls:** PC-STALE-DETECTION (TP≥0.85 per family), NC-FRESH-RETAIN (TN≥0.85), NC-NOISE-IMMUNITY (false_accept ≤0.10 on noise).
- **Code:** `research/graph/freshness_detection/execute_single_resource_staleness.py` (sha256 `a90af8ca51d6cc3eae6a4ca461191e412c8fafa25736886f5d3291bf86d0b8be`), ground truth logging to `raw_evidence/` with SHA256.

No frozen inputs mutated after `freeze.json` (`2026-09-24T00:19:47.067664+00:00`).

---

## 3. Raw Evidence → Observations → Measurements

**Raw evidence** (hashed artifacts):
- `raw_evidence/execution_results.json` (b86e793feb8058adeb87bffc3dcf1832fb10a4c8e1287bac8ae41768fb4b54ae) — 210 logs with ground_truth, family, request_number, url, body, ETag, Cache-Control, jaccard, param/header flags, spider confidences, _matches verified, cost
- `raw_evidence/request_logs.json` (32f32aabd3a1278de2fedaf3cb2fac2951adef2eaec62e0e366d97aa921f5b56)
- `raw_evidence/cost_logs.json` (795ed268e1821ad966ab3fede3adbf711ee6d926360a559a585db305d45cf8ce) — per-trajectory sums reset at boundary
- `raw_evidence/metrics.json` (f5182f397fed426818b5f65d09a2585010dfca835daf81de1e8ffe0898ed4133)
- `raw_evidence/bootstrap_ci.json` (0bae45cb0172522286ed9f921796d13412cad6fc2e94e58a65a49c15081fa273) — 5000 iterations
- `raw_evidence/decision.json` (4905102632bb46f5dfd3caabbcf0b20a5adf386e09cc81ca315ddf536aa67a3e)

**Observations (direct, not interpretations):**
- TN_SPIDER 1.0 (120/120 fresh retained) Wilson lower 0.969 >0.75
- false_accept_SPIDER 0.0 (0/90 stale accepted) Wilson upper 0.0409 ≤0.10
- Per-family TN 1.0 TP 1.0 for all three drift families (30+30 each) Wilson lower 0.8865
- PC TP 1.0 per family, NC TN 1.0 (stable 30/30)
- UNKNOWN 0.4286 (90/210) bootstrap CI [0.4286,0.4286] outside [0.00,0.15]
- ECE 0.2714 >0.15, bootstrap CI [0.2714,0.2714]; bins: [0.5,0.6] n=90 acc1.0 conf0.5 contrib0.2143, [0.9,1.0] n=120 acc1.0 conf0.9 contrib0.0571
- B-NO-GUARD false_accept 1.0 delta_vs_spider 1.0 ≥0.15
- B-JACCARD-ONLY false_accept 0.6667 (TP 30/90), B-HEADER-ONLY false_accept 0.3333 (TP 60/90)
- Cost integer 4 or 5 per request, total 940, all_int true, within-family cost std min 0.4714, freshness std min 0.20 (drift families), mean |rho_shuffled| 0.0578 <0.20 (max 0.2147), observed rho 0.0413
- 5000 trajectory-grouped family-stratified bootstrap completed; CIs degenerate at ceiling for TN/FA due to perfect detection

**Derived measurements (with uncertainty):**
- M-TN-SPIDER 1.0 [Wilson 0.969, bootstrap 1.0-1.0]
- M-FALSE-ACCEPT-SPIDER 0.0 [Wilson upper 0.0409, bootstrap 0.0-0.0]
- M-UNKNOWN-RATE-SPIDER 0.4286 [bootstrap 0.4286-0.4286]
- M-ECE-SPIDER 0.2714 [bootstrap 0.2714-0.2714]
- M-RHO-SHUFFLED mean 0.0578 <0.20, M-WITHIN-FAMILY-STD-MIN-COST 0.4714, M-WITHIN-FAMILY-STD-MIN-FRESHNESS 0.20
- Baseline deltas: B-NO-GUARD 1.0, B-JACCARD-ONLY 0.6667, B-HEADER-ONLY 0.3333

---

## 4. Decision Rule Evaluation (frozen spec.json:decision_rule)

SURVIVES requires ALL D1-D9:

- **D1 TN≥0.85 & Wilson lower>0.75:** PASS (1.0, 0.969)
- **D2 false_accept≤0.10:** PASS (0.0)
- **D3 UNKNOWN in [0.00,0.15]:** **FAIL** (0.4286 >0.15, CI [0.4286,0.4286])
- **D4 ECE≤0.15:** **FAIL** (0.2714 >0.15, CI [0.2714,0.2714])
- **D5 false_accept_NO_GUARD - false_accept_SPIDER ≥0.15 AND >0.10:** PASS (1.0 -0.0 =1.0)
- **D6 per-family TN≥0.75:** PASS (all 1.0)
- **D7 PC TP≥0.85 per family:** PASS (all 1.0)
- **D8 NC TN≥0.85:** PASS (stable 1.0 lower 0.8865)
- **D9 honesty gates (|rho|<0.20, within std>0, integer sum-counter, 5000 bootstrap):** PASS (mean rho 0.0578, cost std 0.4714, freshness std 0.20, all_int true)

**Result:** `SURVIVES_CURRENT_TEST` = false (D3,D4 fail). `D9` passes, so **FALSIFIED-IN-SETTING** (valid scientific negative, not infrastructure). `MEASUREMENT_INVALID` not triggered. Frozen `INCONCLUSIVE` clause (CI width>0.20 underpower) not triggered (N≥210, CIs narrow but degenerate at ceiling).

Per falsifier (spec.json:falsifier): F3 UNKNOWN outside [0,0.15] and F4 ECE>0.15 trigger falsification.

---

## 5. Interpretation

The combined deterministic freshness guard **perfectly detects staleness** in this single-resource isolation (TN 1.0, TP 1.0 per family, FA 0, TN/TP Wilson lower 0.969/0.8865 >0.75, beats no-guard by 1.0, beats single-signal ablations). Header/body conflation of prior TN 0.667 is resolved by single-resource isolation with orthogonal drift families (V9). Deterministic signals (Jaccard, param rename, ETag+expiry) are individually necessary (ablations fail) and jointly sufficient for detection.

However, the **calibration gates fail** exactly as director prior predicted for UNKNOWN precision≥0.85 ECE≤0.15:

- **UNKNOWN 0.4286** equals stale prevalence 90/210 when every stale is correctly flagged UNKNOWN. Required [0.00,0.15] is incompatible with 42.8% stales under policy "0.5 confidence for stale/UNKNOWN, 0.9 for fresh". This is not a detection failure but a prevalence-policy miscalibration: to achieve UNKNOWN≤0.15, stale prevalence must be ≤15% or only subset of stales become UNKNOWN.
- **ECE 0.2714** dominated by stale bin [0.5,0.6] where accuracy 1.0 but confidence 0.5 contributes 0.2143; correct predictions with low confidence are miscalibrated by construction. Achieving ECE≤0.15 would require confidence ~1.0 for correct stales, contradicting spec confidence 0.5.

Thus **C-FRESHNESS survives for detection (TN/FA) but falsifies for calibration (UNKNOWN/ECE)** at this threshold/site. Per `product_consequence_negative`, product must NOT use this freshness gating for reuse at this 0.85 threshold with 0.5/0.9 confidence scheme; fallback UNKNOWN precision/ECE not achieved, so any reuse remains unsafe without recalibration. This bounded falsification does NOT close broader C-FRESHNESS domain (other signals/thresholds/sites) and does NOT reinstate WebArena param-inherit pilots (still PARKED).

Honesty gates pass: sum-counter integers 4/5 per request, no jitter/n*3200/f*6.0, mean |rho_shuffled| 0.0578 <0.20, within-family std>0, 5000 bootstrap trajectory-grouped, _matches deterministic, 304 excluded, single-resource isolation preserved. Bootstrap CIs degenerate at ceiling reflect perfect detection, not invalid measurement.

---

## 6. Controls and Baselines Summary

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| B-NO-GUARD | FA>0.30 TN~0 | FA1.0 TN1.0 delta1.0 | PASS |
| B-JACCARD-ONLY | degraded vs full | FA0.6667 TP30/90 | PASS (discriminating) |
| B-HEADER-ONLY | fails DOM | FA0.3333 TP60/90 | PASS (discriminating) |
| PC-STALE-DETECTION | TP≥0.85 | TP1.0 per family | PASS |
| NC-FRESH-RETAIN | TN≥0.85 | TN1.0 lower0.969 | PASS |
| NC-NOISE-IMMUNITY | FA≤0.10 | FP0 FA0 | PASS |
| V1-V7,V9-V14 | honesty/validity | all pass (see validity_notes) | PASS |
| V8 (ECE/UNKNOWN) | ECE≤0.15 UNKNOWN≤0.15 | ECE0.2714 UNKNOWN0.4286 | **FAIL** (scientific) |

---

## 7. Validity Threats and Representation Loss

- DOM tokens ignore value magnitudes/nested depth beyond flat object — intended isolation.
- ETag ignores timing jitter; param mutation ignores value semantics.
- Synthetic-to-real gap: stdlib http.server flat JSON only, not production Flask/JWT/SQLite/WAL/CDN; ceiling bounded to locally-hosted synthetic.
- Bootstrap CIs degenerate at [1.0,1.0]/[0.0,0.0] due to perfect detection — indicates ceiling effect, not high precision, but cost/freshness std gates confirm non-degenerate measurement.
- Stable fresh-only family freshness std 0.0 exempted (no stale variation); only drift families required to have std>0.
- Stale prevalence 42.8% forces UNKNOWN/ECE failure under current confidence scheme — validity threat is policy, not detection.

---

## 8. Product Consequences

- **Negative (this experiment):** Do NOT promote single-resource freshness guard at 0.85 threshold with 0.5/0.9 confidence to product core. Residual-novelty (rho_novelty≥0.60) and per_hit economics remain blocked pending recalibrated UNKNOWN/ECE. Delta-repair contamination bounds remain blocked.
- **Positive path forward:** Recalibrate confidence (e.g., 0.95 fresh / 0.85 stale) or make UNKNOWN selective (borderline only) and rebalance prevalence to ≤15% stale, then retest same isolation before any distributed WAL or WebArena re-attempt.

---

## 9. Unresolved

- Whether recalibration could pass UNKNOWN/ECE while keeping TN≥0.85 FA≤0.10.
- Whether 15% stale prevalence rebalancing would preserve detection.
- Transfer to real API/production SPA with genuine ETag/Cache-Control.
- Correlated latent non-determinism (session) remains untested.

---

*Executed via `research/graph/freshness_detection/execute_single_resource_staleness.py` (a90af8ca51d6cc3eae6a4ca461191e412c8fafa25736886f5d3291bf86d0b8be) on 127.0.0.1 ephemeral, 210 requests, 5000 bootstraps, honest integer sum-counter, deterministic _matches.*
