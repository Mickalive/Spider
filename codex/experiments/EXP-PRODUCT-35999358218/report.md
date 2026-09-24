# EXP-PRODUCT-35999358218 — EXECUTE report (product lane, C-PRODUCT-ECON)

- schema_version: 1
- status: **MEASUREMENT_INVALID**
- outcome: **INCONCLUSIVE**
- claim_ids: C-PRODUCT-ECON (primary, Director PIVOT: honest M_total Pareto superseding falsified per_hit)
- Lane: product

## 1. What was frozen and why

The experiment asks whether, on a health-gated single-node HS256 sticky substrate with a
TTL-60s correlated conditional probe PLUS Docker BrowserGym 0.14.3 (2000-node 1280x720 CDP)
with the **same** real gpt-4o-mini 15-step model/tools/budget, SPIDER's honest
per-trajectory-reset `M_total_f10/f100` counters Pareto-dominate strong baselines
(B-COLD, B-RAG-EMBED-TAU030-QCR-K5, B-STAGEHAND-CACHE, B-DSM-O1-COMPILE, B-SGDR-AWM) —
saving >=25% vs COLD, ratio <=0.85x vs RAG at both f, margin >=0.12 vs each baseline,
browser+latency saving >=20%, accuracy >=0.85 — and whether that dominance formally
supersedes the falsified per_hit artifact (1.005>0.85, rho 0.363<0.60) as the PRODUCT_CORE
viability gate.

The frozen falsifier gives explicit precedence: clause (1) => MEASUREMENT_INVALID if
BrowserGym 0.14.3 + gpt-4o-mini 15-step are unavailable (rho_proxy_real unmeasurable) or
fixtures are missing/contaminated — **no file-proxy surrogation for SURVIVES**.

## 2. What actually happened (raw evidence -> observation -> derived)

All raw evidence lives in `artifacts/` (env_audit, probe_traces.jsonl, substrate_start,
fixture_checks, pc1/pc3/mv3/null_controls, attempts_log). Derived metrics are in `result.json`.

### 2.1 Substrate half — MEASURED VALID (passes frozen gates)
- nginx 1.24.0 + gunicorn 23.0.0 single worker + Flask + PyJWT 2.14.0 HS256, SQLite **WAL**
  at `/tmp/spider-runtime/shared.db`, single worker pid, jwt alg HS256 only.
- `n_non304 = 840` stratified exactly **420/420** across ep-a/ep-b (>=800 required), 0 errors,
  If-None-Match exercised on **100%** of 846 requests, ETag `W/body_sha` honored (200 vs 304).
- Sticky: nginx `hash $request_uri consistent` -> single upstream `127.0.0.1:18929`.
- Correlated conditional probe (TTL 60s): n0 hit rate 1.0 (150/150), n0.25 accuracy 1.0 with
  stale fraction 0.5, false_accept 0.0, token saving **0.40** (>=0.30), seeded-42 random
  contrast accuracy 0.4867 -> delta **+0.5133** (>=0.10). Substrate gate: PASS.

### 2.2 Positive-control half — MIXED
- PC1 (B-STAGEHAND-CACHE exact-repeat n=0): 5/5 hit_rate 1.0. PASS (file-proxy DOM hash,
  disclosed; Docker AX required for SURVIVES is separately unavailable).
- PC3 (non-vacuous verification calibration, MV10 MockEnv wrong-bound p=0.15, B=5000 CIs):
  AUROC true 0.9195, shuffled null 0.4818, precision 0.9683, forced-execute wrong-accept
  0.1691 in [0.10,0.60], confidence_std 0.4529>0.05, UNKNOWN precision 0.9829, ECE 0.1026. PASS.
- PC4 (frozen-formula parity): per_hit via `(M_total-retrieval-distill/compile-auditor)/L`
  equals summed counters with **max abs diff 0.0 (<=1e-6)** on 192 disclosed tasks;
  `rho_proxy_real` **NULL** (requires real tokens). Parity PASS, proxy-real gate NOT MEASURABLE.
- PC5: substrate half PASS (2.1); BrowserGym+LLM half FAIL (unavailable, see 2.4).
- PC2: Jaccard max 0.0 over 630 family pairs (PASS), kernel dot-regex MV3 5/5 EXECUTABLE +
  wrong-family UNKNOWN at patched sha d926279d (PASS), DSM 714/2147 staged (PASS), sgdr 36
  (PASS), cost_config 50/15/800/10 (PASS) — but **value_set disjointness FAILS**: 18/36
  even families are TRAIN-contaminated at pool level and usage level. PC2 => FAIL.

### 2.3 Null controls — NC1 FAIL on deterministic counters (non-degenerate but length-coupled)
- NC1 (corrected to frozen trajectory-grouped family-stratified block-permutation of
  parameter slots, replacing the parent's degenerate within-trajectory re-sample):
  rho_shuffled **-0.1367** (|.|<0.20), null CI95 [-0.1696, 0.0917] — non-degenerate, no
  [1,1] CI. But block_permutation_p **0.0724** (<0.20) and rho_length_pooled **-0.2871**
  (>|0.20|), per-stratum rho_length {0.5: -0.4669, 1.0: -0.3034} > |0.20| => NC1 FAIL.
  This is a property of the disclosed deterministic counter formula over the contaminated
  192/36 census — precisely why the frozen design requires the real LLM+BrowserGym
  trajectory-grouped measurement.
- NC2 (random family/state keys): AUROC 0.4798 (~0.5), false_accept 0.104 (>=0.10). PASS.
- NC3 (length-proportional constant cost): rho ~0.008, R2 4.3e-05 (<0.15). PASS.
- NC4 correlate: correlated-vs-random probe delta +0.5133 (>10%). PASS (substrate half).

### 2.4 Environment gates — BLOCKED (frozen clause (1) fires)
- `docker pull ghcr.io/servicenow/browsergym:0.14.3` -> exit 1, `manifest unknown` (even
  after GH_TOKEN `docker login` succeeded). Image not obtainable.
- `OPENAI_API_KEY` absent -> gpt-4o-mini 15-step cannot run -> `rho_proxy_real` unmeasurable,
  no honest real-token M_total, no ST-WebAgentBench CuP, no MV6/MV7 replication.
- Hard258 pip census unavailable (`pip index webarena` -> no matching distribution);
  disclosed fallback WebArena-Verified v2 192/36 staged byte-identical to canonical source
  (sha 391e8f6c...) but it is TRAIN-contaminated on 18/36 families (MV2 violation).

## 3. Interpretation

Under the frozen decision rule this is **MEASUREMENT_INVALID / INCONCLUSIVE**, not a
scientific negative: the primary economics (C1-C5), the supersede test, rho_proxy_real, and
the real-trajectory nulls cannot be measured with the required substrate+model substrate
missing, and the only disclosed census is TRAIN-contaminated. A valid file-proxy SURVIVES
is explicitly prohibited by the frozen falsifier. Substrate mechanics (sticky HS256 WAL,
If-None-Match 304, correlated probe) and calibration mechanics (PC1/PC3/PC4 parity, MV3
kernel dot-regex) DID measure validly and repeat the parent's substrate results; the
correlated-probe gate passed, and the NC1 correction eliminated the parent's [1,1]-CI
degeneracy at the deterministic-counter level (though length coupling persists there).

## 4. Consequences (per frozen product_consequence clauses)

- Positive path (SURVIVES): **not demonstrated** — blocked by clause (1).
- Negative path (FALSIFIED): **not demonstrated** — no valid economics measurement exists.
- Supersede path: **not testable**; parent per_hit falsification (1.005>0.85, rho 0.363<0.60)
  stands bounded. No claim update is possible from this run.

## 5. Smallest next actions (for handoff, not self-authorizing)

1. Provide GHCR `ghcr.io/servicenow/browsergym:0.14.3` (playwright 1.63.0 importable,
   2000-node 1280x720 CDP getFullAXTree AX>10) and `OPENAI_API_KEY` for gpt-4o-mini 15-step.
2. Rebuild the census: Hard258 pip-census or a rebuild of the 192/36 fallback with
   per-family disjoint A/B alphabets (value_set_A ∩ B empty on ALL 36 families) — the
   canonical 192/36 file is contaminated on 18/36 even families and cannot serve MV2.
3. Re-run the full battery with real trajectory-grouped nulls (B=5000 block-permutation)
   and honest M_total sum counters once 1+2 hold.
4. If the substrate+LLM gates still cannot be provisioned, this thread stays BLOCKED at
   clause (1); do not weaken prereg after outcomes.