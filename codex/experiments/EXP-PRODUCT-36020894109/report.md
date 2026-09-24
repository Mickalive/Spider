# EXP-PRODUCT-36020894109 — Execute Report (Product PIVOT C-PRODUCT-ECON, single-node n≥360 gate)

**Lane:** product · **Claim:** C-PRODUCT-ECON (M_total Pareto gate, per_hit superseded per Director mandate)
**Status:** MEASUREMENT_INVALID · **Outcome:** INCONCLUSIVE (no claim inference; see §4)
**Frozen inputs:** `request.json`, `spec.json`, `prereg.md`, `freeze.json` (2026-09-24T15:35:36Z) — unmodified.
**Parent:** EXP-PRODUCT-35999358218 (MEASUREMENT_INVALID) — disposition SUPERSEDE per Director PIVOT.

## 1. What was executed (frozen design, no redesign)

1. **Env audit** — pins gunicorn 23.0.0 / PyJWT 2.14.0 / Flask 3.1.3 / numpy 2.5.3 / scipy 1.18.1 /
   sklearn 1.9.1 / pandas 3.0.6 / python 3.12.14 (all PASS); OPENAI_API_KEY ABSENT; playwright 1.44.0
   (frozen toolchain 1.63.0 — mismatch disclosed); `docker pull ghcr.io/servicenow/browsergym:0.14.3`
   → exit 1 `manifest unknown`; no local servicenow image.
2. **Fixture staging + contamination-free rebuild (MV2 fix).** The canonical 192/36 census
   (`391e8f6c`, 18/36 even families sharing A/B alphabets by rotation) was read read-only and rebuilt:
   even-family B pools replaced by the odd-family `LZL` disjoint-alphabet convention, task B-position
   values remapped by old-B index (135 values, 0 fallbacks). Verified: pool A∩B empty **36/36**,
   usage demo-vs-testB empty **36/36**, demos TRAIN-A-only, cross-family bigram Jaccard max **0.0**/630,
   L family-constant 8–14, novelty distribution preserved. New sha `374ef8f6…`. QCR TAU0.30 (`8c69804b`),
   DSM 714/2147, SGDR 36 TRAIN-only, cost_config 50/15/180/10 all staged and passing.
3. **Hard258 census staged offline** — 258 hard IDs (`3b0a4df2`) + 812-task `webarena-verified` 1.2.3
   package (6 sites, 114 intent templates). Live execution BLOCKED (no self-hosted WebArena Docker,
   no OPENAI key); census is the heterogeneity definition, rebuilt 192/36 the executable fallback (MV1).
4. **Kernel dot-regex (MV3 fix).** `src/spider/kernel.py` patched to the frozen dotted language; working
   tree sha `d926279d…` reproduces the parent-recorded patch byte-identically. 5/5 dotted-path
   EXECUTABLE (confidence 0.85) + wrong-family UNKNOWN; `tests/test_kernel.py` 3/3 pass (product scope
   `src`, tested as required). Uncommitted — EXECUTE may not commit.
5. **Single-node substrate** — `/tmp/spider-runtime/shared.db` WAL, single gunicorn 23.0.0 worker,
   nginx 1.24.0 `$request_uri` consistent-hash sticky, PyJWT HS256-only. Health gate **400 ≥ 360**
   (200/200 ≥ 180/endpoint), If-None-Match on 1096/1096 requests, 0 errors, single upstream.
6. **Correlated probe** — n0 hit 1.0; n0.25 accuracy 1.0 (stale 0.5), false_accept 0.0, TN 1.0, token
   saving 0.40 (≥0.30), delta +0.407 vs seeded-42 random (0.593).
7. **Six-condition economics on honest per-trajectory-reset sum counters** (no n·3200/f·6.0/jitter),
   family-stratified B=5000 bootstrap + B=5000 block permutation — disclosed single-node-only ceiling.
8. **Nulls via actual kernel pipeline** (NC1 family-stratified permutation, NC1b family-gating,
   NC1c shuffled AUROC, NC2 random keys, NC3 length-constant, NC4 ablations) + PC1/PC3/PC4 + DSM
   lookup/overlap + supplementary playwright AX (46 nodes > 10, non-BrowserGym).

Raw evidence (`probe_traces.jsonl`, `economics_per_trajectory.csv`, `nc_trajectory_counters.json`,
`env_audit.json`, `substrate_start.json`) is preserved separately from derived measurements; this
report interprets without contradicting `result.json`.

## 2. Observations (see `result.json:observations`; selected)

- **MV2 contamination closed** on the executable holdout (0/36 pool, 0/36 usage, Jaccard 0.0).
- **Ceiling economics:** SPIDER f10 1981 tok/traj — saving **0.669** vs COLD (cost gate met) but ratio
  **1.506** vs RAG (RAG gate failed: probe-per-step + per-novel-slot repair + auditor + distill
  amortization exceed once-per-trajectory retrieval + verbatim bind at frozen knobs). f100: 0.684 / 1.438.
  Browser+latency saving vs COLD 0.494. SPIDER kernel resolve 192/192 EXECUTABLE, bound_ok 1.0.
- **Deterministic coupling reproduced exactly:** rho_length pooled **−0.2871** (identical to parent),
  per-bin −0.084…−0.657; NC1 rho_shuffled −0.1367, permutation p **0.0724** (< 0.20).
- **Kernel validates context, not values:** nonexistent family → UNKNOWN 1.0; foreign-family value in a
  correct slot → EXECUTABLE (verify/repair must catch it).
- **DSM baseline degenerates** on the synthetic fixture (site overlap 0/36 → COLD + wasted lookup).
- **Normalized per_hit vs COLD step:** 0.135 @n0, 0.294 @n0.25 — raw tokens incommensurable with the
  frozen 0.85 ratio gate; supersede conjoint not triggered (Pareto fails on ceiling).

## 3. Calibration / controls summary

PC1 1.0 PASS · PC3 MockEnv AUROC 0.871 vs null 0.468, precision 0.949, forced-accept 0.161,
conf_std 0.454, UNKNOWN 0.984, ECE 0.107, 0 empty bins — PASS · PC4 parity 5.7e-14 PASS, rho_proxy NULL ·
PC5 substrate half PASS, BrowserGym/LLM half absent (PARTIAL) · NC2/NC3 PASS · NC4 deltas logged
(correlated-vs-random +0.407; DSM on/off −46740; sticky-vs-direct TN 1.0/1.0).

## 4. Decision (frozen rule applied, precedence ordered)

1. Full SURVIVES is not authorized: composite PC is PARTIAL (PC5 browser half, PC2 DSM-transfer
   sub-clause on a zero-overlap synthetic fixture), rho_proxy_real/safety/real-success are null, and the
   kernel patch is uncommitted. No file-proxy surrogation for the browser-validated gate.
2. Null degeneracy (falsifier 2) does not trigger (|rho_shuffled| 0.137 < 0.35, p 0.0724 not < 0.01,
   AUROC null non-degenerate, bootstraps non-degenerate).
3. FALSIFIES requires controls PASS non-degenerate — not met (NC1 length/p fail; PC partial). The
   ceiling ratio 1.51 is therefore a **diagnostic, not a falsification** of C-PRODUCT-ECON.
4. ⇒ **status MEASUREMENT_INVALID, outcome INCONCLUSIVE.** All claim-level metrics stay null with
   reasons (`result.json:metrics_null_reasons`); C-PRODUCT-ECON remains HYPOTHESIS; the prior bounded
   per_hit falsification is untouched (different metric/units).

## 5. Consequences

- **Negative consequence does not fire** (no FALSIFIES): do not PARK C-PRODUCT-ECON on this evidence.
- **Positive consequence does not fire** (no SURVIVES): no EXPERIMENTAL promotion, no distributed
  n≥800 authorization, no PRODUCT_CORE.
- **What changed (bounded, honest):** MV2 rebuilt contamination-free (new sha `374ef8f6…`); MV3 patch
  reproduced byte-identically and functionally verified (pending commit); n≥360 single-node gate passes
  with margin (400, TN 1.0); Hard258 census staged with digests; the full Pareto machinery runs
  end-to-end on honest counters and already discriminates (RAG overhead finding). Remaining unblockers,
  in order: (1) commit kernel patch durably; (2) GHCR BrowserGym 0.14.3 + OPENAI_API_KEY + playwright
  1.63.0 for rho_proxy_real ≥ 0.50 and real browser/latency/safety; (3) re-measure NC1 on real
  trajectories to break deterministic length coupling; (4) re-execute frozen gates; then DIRECTOR/AUDIT
  adjudicate. DSM-on-synthetic-fixture transfer (0/36 overlap) should be fixed by overlapping or live sites.
- This packet's chain is RAW EVIDENCE → OBSERVATION → DERIVED MEASUREMENT → INTERPRETATION as labeled
  per artifact; downstream AUDIT may challenge any interpretation but must preserve the evidence.
