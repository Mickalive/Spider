# Preregistration: EXP-FRONTIER-38188815194 (FRONTIER)

## 1. Experiment identity
- experiment_id: EXP-FRONTIER-38188815194
- lane: frontier
- design_contract_version: 2
- request: research/experiments/EXP-FRONTIER-38188815194/request.json (director_mandate PIVOT on C-CROSSSITE runner-up; cognitive_reset true)
- parent_handoff: research/experiments/EXP-FRONTIER-38184956362/handoff.json (bounded negative; discovery axis closed on this substrate/frame/channels/K=3; continue=false, non-authorizing)

## 2. Scientific question
On the frozen credential-free GET-only 20-host/556-item frame, against the measured same-host BFS path cost (ordinal mean 166.0, min 31, max 250 GETs over 208 admitted deep items) as cold re-derivation comparator, does revalidating a persisted deep state-carrying path (fresh GETs/bytes for liveness and change detection, scaling with hop and elapsed time) plus a bounded session-scale stale-replay false-accept rate undercut cold re-derivation, and at what break-even hop/elapsed time does persistence stop paying?

This is the mandate’s conditional runner-up (feeds C-FRESHNESS/C-PRODUCT-ECON; owned with Graph/Product). Discovery rerun is excluded.

## 3. Claims
- C-CROSSSITE: bounded mechanism (site-native discovery shortcut) already falsified on this substrate class by parent; this experiment does not reopen discovery.
- C-FRESHNESS: tests economics/validity of revalidation (liveness+change detection) under session-scale bounds.
- C-PRODUCT-ECON: measures whether persistence pays (cost reduction) vs cold re-derivation with explicit break-even.

## 4. Design
- Substrate: credential-free GET-only stdlib HTTP (no model key, browser, Docker, credentials, pip installs required). Reuse parent’s frozen 20-host/556-item frame.
- Treatment: persisted deep path with revalidation at windows w in {0, 300, 900, 1800 s} (elapsed from “persist” time). Revalidation = fresh GETs/bytes for liveness and change detection; count cost components separately (GETs, bytes_in, bytes_out, elapsed_s).
- Comparators/baselines: B-COLD-SAME-HOST-BFS (per item from parent metrics; mean 166.0). B-EXACT-PATH-REPLAY-NAIVE included as guard only (honor P2-REPLAY-COST ~1.002x; not assumed win).
- Population: 208 admitted deep state-carrying items from frozen items.jsonl (exclude items not admitted). Use frozen set (do not redefine “state-carrying” mid-run).

## 5. Controls
Primary controls:
- MC-FRAME-INTEGRITY: hash match for structural.jsonl and item counts (208 admitted). 
- MC-BASELINE-AVAILABLE: cold cost present for every admitted item; distribution consistent with parent (tolerance declared).
- MC-LIVENESS-CHANGE-DETECT: calibration set shows change detection fires on synthetic modification and does not spuriously fire on identical content; record pass/fail/measurement-failure.
- MC-SESSION-SCALE-BOUND: false-accept rate (if estimated) bounded to session-scale regime only; if not measurable, record “not_measurable” with justification (forbid day-scale extrapolation). This reflects legacy program finding day-scale staleness undecidable on committed corpora.
- MC-BUDGET: total GETs/bytes within ceiling; all fetches accounted.

## 6. Decision rule (preregistered)
For each window w, compute persistence cost = revalidation_cost_w + delta_false_accept_w (in same units) vs cold_cost_i. 
Decision mapping:
- SUPPORTS if any window shows persistence pays with min_effect (>=10% relative OR >=5 GETs absolute, whichever larger) and all required controls pass; report break-even hop/elapsed.
- FALSIFIES if no window shows persistence pays (reval_cost >= cold_cost across all windows, within tolerance) with valid measurement, OR structurally cannot bound false-accepts as required (MC-SESSION-SCALE-BOUND fails in the sense that only day-scale claim would be needed).
- MIXED if pays for some stratification (e.g. hop>h0, short elapsed) but not others.
- INCONCLUSIVE if measurement invalid/blocked (any required control fails irrecoverably, budget overflow with no valid subset, infrastructure failure) — treat separately; do not infer negative.

Primary statistic: break-even analysis (per-item and stratified by hop class). Report absolute and relative effect sizes.

## 7. Validity & scope
- Do not claim freshness detector for day-scale hazard; any staleness/false-accept statement strictly session-scale or explicitly not claimed.
- Inherit scope boundaries: JS-rendered ON_SITE_SEARCH gap is known; single-vantage egress is caveat (cross-vantage not mandated).
- Discovery axis is closed on this substrate/frame/channels/K=3 (parent bounded negative). Do not repeat identical design.
- Parent claim ceiling applies: bounded to credential-free GET-only substrate, this frozen frame, 208 admitted deep items, five channels context only as needed for frame identity.
- Treat measurement failure separately from scientific negative (packet invariant).

## 8. Data collection
- Reuse frozen fixtures: structural.jsonl, items.jsonl, census.jsonl, parent metrics.json/audit.json/result.json (hash-verified).
- For each persisted deep path: record hop count (from frozen path info), number of revalidation probes, GETs, bytes_in/out, elapsed_s per probe and total per window.
- Liveness check: confirm reachable (HTTP 200, expected structure) or mark dead with reason.
- Change detection: compare against persisted snapshot (content hash/signature of relevant parts); calibration set includes synthetic change + no-change.
- False-accept: bounded session-scale estimate only if feasible without day-scale span; otherwise set to not_measurable.
- Cold cost: taken directly from parent baseline per item (no recomputation of parent BFS required).
- Budget tracking: cumulative GETs/bytes/elapsed; stop if projected > ceiling and cannot recover valid subset.

## 9. Analysis plan
- Per item: cold_cost vs reval_cost_w for each window; break-even when reval_cost_w + delta_fa_w < cold_cost - tol.
- Aggregate: mean/median, stratify by hop (low/mid/high based on distribution), by elapsed window. Report distributions (min/max) to match parent reporting style.
- Sensitivity: tolerance on equality (tol >= 0; declare), effect threshold as above.
- Guard: naive replay cost computed if feasible (or use legacy bound) to confirm replay alone not win.

## 10. Pre-freeze satisfiability (design_contract_v2)
- decision_rule_reachability: PASS (all branches defined)
- measurement_prerequisites: PASS (frame+baseline+measurable units)
- baseline_identifiability: PASS (stable ids, parent refs)
- control_sensitivity: PASS (liveness+change detect + session-scale bound)
- treatment_liveness: NOT_APPLICABLE (no SPIDER kernel treatment arm; measurement experiment)
- freeze_artifacts_bound: PASS (fixtures/evidence listed; mutable interpretation deps bound)

Freeze artifacts (interpretation dependencies): structural.jsonl, metrics.json, items.jsonl, census.jsonl, audit.json, result.json from parent EXP-FRONTIER-38184956362.

## 11. Stop/pivot triggers
- If revalidation cost >= cold cost across all windows and measurement valid → FALSIFIES; PARK persistence subthread (no discovery rerun).
- If cannot bound false-accepts to session-scale (would need day-scale) → record limitation; outcome may be FALSIFIES on “economically justified with bounded false-accept” or INCONCLUSIVE depending on rule, but must not claim day-scale freshness.
- If measurement fails (controls fail irrecoverably) → INCONCLUSIVE, treat failure separately, do not weaken prereg.
- Budget overflow with no recoverable valid subset → INCONCLUSIVE (infrastructure failure).
- If break-even only appears under implausible assumptions → do not claim SUPPORTS.

## 12. Ethics/scope notes
- No external credentials, no model endpoint calls, no user data. 
- Do not generalize bounded negative beyond stated substrate/frame/channels/K context. 
- Scout/Director non-evidentiary labels respected. 
- Cross-lane coordination noted (Graph/Product for C-FRESHNESS/C-PRODUCT-ECON) but no cross-lane code writes.
- Do not repeat identical discovery design per Frontier discipline and parent handoff.
