# EXP-GRAPH-35937576511 — Preregistration (DESIGN frozen pre-outcome)

**Lane:** graph  
**Claim:** C-FRESHNESS — SPIDER can detect when inherited knowledge is stale (next_gate: session/token/DOM/endpoint drift with false-accept measurement)  
**Experiment ID:** EXP-GRAPH-35937576511  
**Director mandate:** PIVOT to C-FRESHNESS (action=PIVOT, cognitive_reset=true, parent_handoff_disposition=SUPERSEDE) per `request.json:director_mandate` — comparative_reasoning: 9th identical add_to_cart param pilot has near-zero marginal gain vs neglected freshness prerequisite.  
**Parent handoff:** `research/experiments/EXP-GRAPH-35932480731/handoff.json` (8th consecutive MEASUREMENT_INVALID on kernel durability gates) — **inherited state preserved but superseded per Director**; next_question NOT pursued (see §14).

## 1. Strategic Question → Falsifiable Question

Director strategic question (verbatim, para 25 of request.json):

> After 8 consecutive MEASUREMENT_INVALID WebArena-Verified v2 family holdout param-inherit pilots on identical single-family add_to_cart with failed kernel durability gates (grep/sha/diff, zero unsubstituted templates), does a controlled single-resource staleness probe — DOM token drift / endpoint param+header mutation / Cache-Control+ETag expiry on one resource only on a locally-hosted synthetic site with deterministic freshness signal — enable detection with TN>=0.85 (Wilson lower>0.75), false_accept<=0.10, UNKNOWN in [0.00,0.15] ECE<=0.15 vs no-guard baseline, measured with deterministic _matches verification and honest per-trajectory-reset sum counters (resolve+bind+verify+freshness+browser_steps, no jitter, no n*3200, |rho_shuffled|<0.20 within-f std>0) with 5000 family-stratified bootstrap trajectory-grouped CIs?

Falsifiable refined question (this prereg):

> On a locally-hosted synthetic site serving one resource type (`/resource/{id}`) with deterministic freshness signal, does a SPIDER freshness guard that combines DOM field-set tokens, endpoint query/body/headers param template, and Cache-Control+ETag achieve TN>=0.85 (Wilson lower>0.75), false_accept<=0.10, UNKNOWN∈[0.00,0.15] ECE<=0.15, beating a no-guard baseline by false_accept delta >=0.15, under honest per-trajectory-reset sum counters and trajectory-grouped family-stratified bootstrap?

## 2. Hypothesis

H1 (positive): Single-resource freshness guard with deterministic signals detects staleness at required operating point (TN≥0.85 lower>0.75, FA≤0.10, UNKNOWN calibrated, ECE≤0.15) and shows ≥0.15 false_accept improvement over no-guard. Signal isolation (one resource, separate body vs header vs cache channels, deterministic scheduling) restores the TN 0.85 target that prior confounded multi-resource scheduling (TN 0.667) and header/body conflation failed, and the stratified |r| orthogonality issue at delta 0.15 is side-stepped by single-resource isolation (not pooled across endpoints).

H0 (null): Guard performs at or below no-guard baseline (TN<0.85 or FA>0.10 or UNKNOWN miscalibrated or no delta), or honesty gates reveal cost tautology (|rho_shuffled|≥0.20) or degenerate variance.

## 3. State Representation

- **Raw observation:** HTTP response for `/resource/{id}`: JSON body (flat object with 3-5 fields), ETag header (SHA256(canonical_json_body)[:16]), Cache-Control header (max-age=60 or max-age=0/no-store), X-Csrf-Token header, query string for param mutation family.
- **Derived freshness state:** 
  - `dom_tokens = sorted {(field_path, type)}` from body via `extract_field_types` (type via normalized Python types → string/integer/boolean/array/object).
  - `header_tokens = {Cache-Control, ETag, X-Csrf-Token}` values.
  - `endpoint_template = url path + query param names` (param names, not values).
- **Cached mechanism postcondition:** stored `dom_tokens` + `header_tokens` + `action_template` from pre-drift fresh observations (3-5 successful observations per trajectory before drift point).
- **Freshness score:** Jaccard(dom_tokens_cached, dom_tokens_live) for DOM family; Jaccard(header_tokens_cached, header_tokens_live) + ETag equality check for cache family; endpoint template equality (exact match of param names + header names) for param family. Combined decision: `stale = (jaccard_dom < 0.85) OR (param_template_changed) OR (ETag_changed AND Cache-Control indicates expiry)`. Threshold 0.85 frozen pre-execution (matches prior freshness_detection execute.py).
- **Confidence:** 0.90 if not stale (fresh), 0.50 if stale/UNKNOWN. Used for ECE binning.

Representation loss disclosed: DOM tokens ignore value magnitudes and nested depth beyond top-level; ETag ignores timing jitter; param mutation ignores value semantics — these are the intended isolated signals.

## 4. Action Representation

- **Intent:** `fetch_resource` with params `{resource_id}`.
- **Mechanism action_template:** `GET /resource/${resource_id}` with headers `{X-Csrf-Token: ${token}}` and query `?detail=${detail}` (param template). Distilled from fresh observations via literal mechanism (SPIDER kernel `distill` literal, no param induction needed for this probe).
- **Execution:** stdlib `urllib.request` GET to `http://127.0.0.1:{port}/resource/{id}` with headers. No browser automation required (browser_steps counter = 0 but retained in sum for honesty).
- **Verification:** `verify(mechanism_id, observed_state)` via `_matches(postconditions, observed_state)` exact equality on body fields + header equality for ETag/Cache-Control where applicable.

## 5. Target, Unit of Analysis, and Sampling Policy

- **Target:** Binary staleness classification per request (fresh vs stale) and abstention decision (EXECUTABLE vs UNKNOWN/EXPLORE vs false_accept).
- **Unit of analysis:** Single HTTP request/transition, grouped at trajectory/family level for inference (trajectory-grouped bootstrap preserves within-trajectory dependence).
- **Sampling policy:**
  - Synthetic server: `http.server.HTTPServer` on 127.0.0.1 ephemeral port, 3 drift families × 60 requests (30 fresh before DRIFT_POINT + 30 stale after) = 180 plus 30 fresh-only control family (users_stable-like) = 210 total.
  - Drift injection deterministic: `DRIFT_POINT = 6` per trajectory (i.e., requests 1-5 fresh, 6-10 stale per family trajectory, replicated across 6 trajectories per family to reach 30+30). Same as `research/graph/freshness_detection/execute.py` pattern but scaled to 6 trajectories per family.
  - Families:
    1. `dom_drift`: body field add (phone), remove (author), change type (id int→str) — same as FRESH_POSTCONDITIONS drift spec.
    2. `param_header_mutation`: query param `detail` value domain shift + `X-Csrf-Token` rotation (header value change).
    3. `cache_expiry`: ETag changes (body SHA) + Cache-Control `max-age=60` → `max-age=0` + If-None-Match 304 logic (deterministic).
  - Control: `stable` family no drift, always fresh (tests null control).
  - No real network, no LLM, no Docker.

## 6. Holdout

- **Within-synthetic holdout:** Fresh trajectories (requests 1-5 per family) are the training/cache source for mechanism postconditions; stale trajectories (requests 6-10) are held out for detection test. No overlap in request_number between cache and test. No site holdout needed (locally-hosted single resource is the testbed).
- **Cross-family holdout:** Each family tested separately (per-family TN/TP reported) to prevent header/body conflation.
- **No website holdout:** Claim ceiling bounded to locally-hosted synthetic site; not a cross-site transfer claim (C-CROSSSITE separate).

## 7. Nulls / Baselines (strong)

- **B-NO-GUARD (primary):** No freshness gate; resolve always EXECUTABLE if preconditions pass. Measures natural false_accept without abstention. Strong baseline because it is the unsafe reuse that freshness must improve.
- **B-JACCARD-ONLY:** Freshness uses only DOM Jaccard <0.85, ignores header/cache. Ablation that should fail param_header and cache families (tests signal isolation).
- **B-HEADER-ONLY:** Freshness uses only header/ETag equality, ignores DOM. Should fail dom_drift family.
- **Positive control:** PC-STALE-DETECTION — injected stale responses must be flagged; TP≥0.85 per family. If PC fails, pipeline broken.
- **Null control:** NC-FRESH-RETAIN — fresh responses not flagged; NC-NOISE-IMMUNITY — noise-only (optional_field churn) not flagged.

Comparison uses matched tasks (same 210 requests for all baselines/controls).

## 8. Primary Metric & Decision Rule (frozen)

**Primary metrics (stable ids):**
- `M-TN-SPIDER` = TN / (TN+FP) on fresh pool (fresh = <DRIFT_POINT + stable family)
- `M-TN-WILSON-LOWER` = Wilson lower (z=1.96) for `M-TN-SPIDER`
- `M-FALSE-ACCEPT-SPIDER` = FP / (TN+FP) on stale-flagged? Actually FP = fresh flagged stale? Better: false_accept = stale accepted as EXECUTABLE (i.e., FN of staleness detection) = FN / (TP+FN) where positive = stale. For product framing: false_accept = P(EXECUTABLE | stale ground truth). Use that definition. Formal: `M-FALSE-ACCEPT-SPIDER` = # stale requests resolved EXECUTABLE / # stale requests.
- `M-UNKNOWN-RATE-SPIDER` = # UNKNOWN / N_total
- `M-ECE-SPIDER` = ECE over 10 bins on confidence (0.90 fresh, 0.50 stale/UNKNOWN)
- Per-family `M-TN-FAMILY-{dom,param,cache}` and `M-TP-FAMILY-{dom,param,cache}`
- Honesty: `M-RHO-SHUFFLED` = max |Pearson rho| between shuffled cost and outcome (1000 perms trajectory-grouped)
- `M-WITHIN-FAMILY-STD-MIN` = min within-family std of freshness score across families
- Cost: `M-COST-SPIDER-SUM` and `M-COST-NO-GUARD-SUM` (per-trajectory-reset integers)

**Decision rule (exact, see spec.json:decision_rule):**
- SURVIVES_CURRENT_TEST iff ALL D1-D9 hold (D1 TN≥0.85 & Wilson lower>0.75, D2 FA≤0.10, D3 UNKNOWN∈[0.00,0.15], D4 ECE≤0.15, D5 delta vs no-guard ≥0.15, D6 per-family TN≥0.75, D7 PC TP≥0.85, D8 NC TN≥0.85, D9 honesty gates pass).
- FALSIFIED-IN-SETTING iff any D1-D8 fails while D9 passes.
- MEASUREMENT_INVALID iff any honesty gate fails (V3-V6), non-deterministic verification, 304 mishandling, server failure, or N<60 fresh+60 stale.
- INCONCLUSIVE only if CIs straddle thresholds with width>0.20 (underpower).

All metrics reported with 5000 family-stratified trajectory-grouped bootstrap 95% CIs (percentile method, resampling trajectories within family, preserving family proportions).

## 9. Uncertainty Method

- **Wilson CI** for proportions (TN, TP, false_accept) with z=1.96.
- **Trajectory-grouped family-stratified bootstrap** (B=5000): resample with replacement at trajectory level (6 trajectories per family), stratified by family (same number per family as original), recompute all metrics per resample → percentile 95% CI (2.5th, 97.5th). Also report bootstrap CI for UNKNOWN and ECE (ECE via binning per resample).
- **TOST not needed** for this single-resource isolation probe (prior orthogonality TOST failures at delta 0.15 were pooling artifacts; here we test TN/FA directly). Report honesty null: `|rho_shuffled|` via 1000 permutations (trajectory-grouped shuffle of cost labels).
- **Adequacy rule:** N≥60 fresh + 60 stale total ensures Wilson lower sensitivity at 0.85 (expected half-width ~0.08). If N smaller, mark underpowered.

## 10. Falsification / Survival Rule

- Positive `SURVIVES` authorizes bounded product use of single-resource freshness guard at this threshold/site; does NOT promote C-FRESHNESS to VALIDATED/PRODUCT_CORE (needs n≥800 and real-API validation per prior handoffs).
- Negative `FALSIFIED` bounded to this signal/threshold/site; C-FRESHNESS remains HYPOTHESIS, does NOT imply impossibility of freshness detection with other signals.
- `MEASUREMENT_INVALID` means honest-cost or verification substrate failed; no claim update.

## 11. Product Consequences

- **Positive:** Unblocks residual-novelty economics (later-agent cost tracks residual novelty) and per_hit product-econ at f=10 with calibration guarantees; enables delta-repair contamination bound experiments on same synthetic substrate without distributed WAL.
- **Negative:** Provides calibrated abstention baseline (UNKNOWN/ECE) showing guard at 0.85 threshold insufficient for safe reuse; product must retain UNKNOWN override and not rely on this freshness gate for residual-novelty claims; does NOT revert to WebArena param pilots.

## 12. Validity Threats & Mitigations

- **Threat:** Jitter/n*3200 tautology (prior PRODUCT-ECON failures) → Mitigated by honest integer sum counter, shuffled rho bound, within-f std check (prereg §5, V2-V5).
- **Threat:** Header/body conflation (prior TN 0.667) → Mitigated by single-resource isolation, separate ablation baselines (B-JACCARD-ONLY, B-HEADER-ONLY), orthogonal drift families not pooled.
- **Threat:** Confounded scheduling (prior 304 inclusion) → Mitigated by deterministic DRIFT_POINT per trajectory, single resource no cross-family scheduling, 304 excluded from TN/FA (V9, V14).
- **Threat:** Degenerate bootstrap CI [1.0,1.0] → Mitigated by within-family std>0 gate and per-trajectory grouping.
- **Threat:** ECE miscalibration due to single-bin degeneracy (n=16 prior) → Mitigated by N≥120, 10-bin ECE, UNKNOWN in [0,0.15] required.
- **Threat:** Synthetic-to-real gap → Disclosed ceiling: locally-hosted stdlib http.server only, not production Flask/JWT/SQLite/WAL/CDN/network; result bounded to synthetic, not VALIDATED.

## 13. Estimated Cost & Information Gain

- **Cost:** Low (~210 requests, <5 min CPU for 5000 bootstraps, <0.5 compute-hour, no LLM/browser/Docker, <$1) — smallest high-information test per Director mandate.
- **Gain:** Very high per Director portfolio_assessment: directly tests the neglected blocking claim (C-FRESHNESS 1/15 recent, prerequisite for C-RESIDUAL-NOVELTY rho≥0.60 and C-PRODUCT-ECON per_hit and C-DELTA-REPAIR), isolates prior confounds, and decides safe-reuse gating without heavy distributed infra.

## 14. Continuity vs Director Supersede

- **Inherited from EXP-GRAPH-35932480731 handoff:** Established: narrow synthetic ceilings only (EXP-PRODUCT-33528829801 10/10, EXP-PRODUCT-33741671686 21/21 harness-only); no durable kernel-integrated live WebArena evidence. Unknown: whether durable distill_parameterized would achieve EXECUTABLE≥0.75 on WebArena-Verified v2. Do_not_assume: kernel contains distill_parameterized, census exists, MEASUREMENT_INVALID equals falsification — all still MEASUREMENT_INVALID per handoff.
- **Disposition per Director:** PIVOT + SUPERSEDE + cognitive_reset=true → this experiment does NOT pursue handoff.next_question (WebArena Verified v2 add_to_cart pilot). That pilot remains PARKED pending durable substrate. This probe is orthogonal (C-FRESHNESS single-resource synthetic) and intentionally minimal to unblock freshness prerequisite before any future param-inherit re-attempt.
- **Dependencies:** C-MEAS-VALID (honest sum-counter substrate must be valid, as measured), C-DELTA-REPAIR (blocked pending this freshness gate) — reported per mandate.

## 15. Execution Scope & Code Paths

- **Allowed roots:** `research/graph`, `research/harness` per `research/lanes/registry.json:graph.allowed_code_roots`.
- **Planned harness:** `research/graph/freshness_detection/execute_single_resource_staleness.py` (new, ~350 lines, pattern from `execute.py` but single resource, deterministic signals, honest counters). Raw evidence to `research/experiments/EXP-GRAPH-35937576511/raw_evidence/` with `execution_results.json`, `request_logs.json`, `metrics.json`, `decision.json`, `cost_logs.json`, `bootstrap_ci.json` and SHA256 logs.
- **Freezing:** `freeze.json` will hash request/spec/prereg before execution; EXECUTE must not mutate frozen inputs.

## 16. Prereg Timing

Frozen before any outcome-bearing measurement for this experiment_id. Prior evidence cited is from Codex and .spider-runtime/pre2/SPIDER_CODEX_ULTIME.md (searched for relevant prior evidence only) and parent handoff — not from new data.

---
*Prereg follows SPIDER_MASTER_PROMPT.md §19 and RESEARCH 2.0 binding packet `research/EXPERIMENT_PACKET.md` §§3-5.*

