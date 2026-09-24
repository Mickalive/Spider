# EXP-PRODUCT-36036421062 — Report (Product REOPEN C-PRODUCT-ECON — honest M_total Pareto supersession on health-gated single-node n>=360 + BrowserGym 0.14.3)

**Lane:** product — **Claim:** C-PRODUCT-ECON (primary, REOPEN superseding falsified per_hit 1.005>0.85)
**Status:** MEASUREMENT_INVALID — **Outcome:** INCONCLUSIVE
**Director mandate:** REOPEN cognitive_reset=true, target C-PRODUCT-ECON, single-node HS256 sticky n_non304>=360 stratified + GHCR BrowserGym 0.14.3 2000-node + gpt-4o-mini 15-step same model/tools/budget honest sum-counter before distributed n>=800 authorization.

---

## 1. Summary

On the rebuilt contamination-free 192/36 holdout (c2763ebae9..., 0/36 pool and 0/36 usage disjoint, Jaccard max 0.0 on 630 pairs, L 8-14) with health-gated single-node HS256 sticky substrate (n_non304=400 stratified 200/200 >=360/180, WAL single-worker pid 51939, nginx 1.24.0 $request_uri sticky, PyJWT 2.14.0 HS256, If-None-Match 1.0, TN 1.0) and functionally correct kernel dot-regex (d926279d, 5/5 EXECUTABLE), the honest per-trajectory-reset integer counters produced a **disclosed single-node-only bounded ceiling**: SPIDER f10 1981.1 f100 1891.1 vs COLD 5992.7 **saving 0.669 CI [0.652,0.687] meets cost gate but ratio vs RAG 1.506 CI [1.479,1.531] >0.85 FAIL** at f10 (1.438 at f100). The browser-validated Pareto claim remains **MEASUREMENT_INVALID** because the provisioned BrowserGym/LLM substrate required by MV6/MV7 (GHCR 0.14.3 2000-node CDP AX>10, gpt-4o-mini 15-step, rho_proxy_real>=0.50 per-stratum, safety CuP) was not provisioned (GHCR pull denied, OPENAI_API_KEY absent, playwright 1.44 vs 1.63) and PC5+MV6+kernel-durability-via-commit fail per frozen falsifier precedence. No file-proxy surrogation for SURVIVES is permitted, so outcome is INCONCLUSIVE not falsification.

---

## 2. Frozen Inputs Verified

- **request.json** sha 0e857301..., spec sha cf7dfd2272..., prereg c765d738..., freeze 2026-09-24T17:48:39Z byte-identical.
- **Execution base** b0df0948 head 2e660f25.
- **Rebuilt holdout:** research/experiments/EXP-PRODUCT-36036421062/fixtures/webarena_verified_v2_tasks_192_36_rebuilt.json sha c2763ebae943b94dd... (rebuilt via even-family disjoint B = flank+Z+index+flank, 18 families rebuilt, 135 values remapped, 0 fallbacks). Note SHA differs from prereg 374ef8f6 expectation due to flank-case rebuild rule, but passes MV2 zero-overlap 0/36 + Jaccard 0.0 (audit must recompute contamination not SHA equality). Canonical contaminated 391e8f6c not reused.
- **qcr_bank_manifest** 8c69804b TAU 0.30 staged, dsm 714/2147 af3c18e5 staged, sgdr 36 staged, cost_config 50/15/180/10 staged, kernel working-tree d926279d pattern r'\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}' functional 5/5 (head 8af66ccf not committed -> durability false).

---

## 3. Controls

### Positive Control PC-SINGLE-NODE-ECON-PARETO-CORRELATED — PARTIAL (fail => MEASUREMENT_INVALID)

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| PC1 exact-repeat at n0 | hit 1.0 5/5 via BrowserGym 2000-node AX>10 + n>=360 | 1.0 via file-proxy DOM hash disclosed, n>=360 PASS but BrowserGym half absent | PARTIAL |
| PC2 orthogonal+kernel+disjoint+probe | Jaccard 0.0 <0.30, 5/5 confidence>=0.80, 0/36 disjoint, probe acc>=0.90 saving>=30% TN>=0.85, registry 714/2147 80-94% | All PASS except DSM lookup sub-clause site overlap 0 not 1.0, BrowserGym half absent | PASS* |
| PC3 non-vacuous verify | AUROC true>=0.75 [0.45,0.60] null, precision>=0.80, false_accept [0.10,0.60], conf_std>0.05 | true 0.871 vs 0.468, precision 0.949, FA 0.1607, std 0.454, UNKNOWN 0.9837, ECE 0.107 | PASS |
| PC4 frozen formula + rho_proxy | parity 1e-6, rho_proxy>=0.50 pooled+per-stratum logged | parity 5.68e-14 PASS but rho_proxy NULL (no LLM tokens) | FAIL |
| PC5 health-gate n>=360 + BrowserGym | sticky HS256 WAL n>=360 If-None-Match 1.0 AX>10 rho_proxy measurable | substrate 400 200/200 WAL single-worker HS256 sticky INM 1.0 TN1.0 PASS but BrowserGym AX>10 / rho_proxy / playwright 1.63 missing | FAIL |

**Verdict:** Any PC fail => MEASUREMENT_INVALID per spec precedence (1). PC4/PC5 fail due to GHCR/OPENAI absence, not scientific falsification.

### Null Control NC-SHUFFLE-ECON-PARETO — MIXED (fails due to deterministic counter coupling, bounded)

- **NC1 shuffled:** rho_shuffled -0.1367 PASS band but p 0.0724 FAIL (<0.20), rho_length pooled -0.287 FAIL, per-stratum -0.084 to -0.657 all FAIL >0.20. Shuffled-n bin rho near-null by construction (n near-constant per bin). Per-family rho_shuffled distribution shows residual coupling (e.g., -0.92, 1.0).
- **NC1b swapped family keys:** nonexistent family UNKNOWN 1.0 PASS, value-swap EXECUTABLE (kernel binds structurally by slot name, value errors surface only at verify -> disclosed limitation).
- **NC1c shuffled AUROC:** 0.46 PASS (0.45-0.60).
- **NC2 random keys:** UNKNOWN 0.654 FA 0.346 AUROC 0.462 PASS.
- **NC3 length-constant cost:** rho 0.0079 R2 0.0 PASS (R2<0.15).
- **NC4:** correlated-vs-random delta 0.4067 PASS (>0.10), DSM on/off delta -46740 (compile ADDS cost on 0-overlap), TN sticky 1.0 vs direct 1.0 (no per-node artifact).

NC1 deterministic coupling is the **bounded REJECTED** file-proxy null from parent handoff; must be re-measured on real BrowserGym trajectories where |rho_shuffled_proxy|<0.20.

---

## 4. Economics (bounded ceiling, honest sum counters, not claim inference)

All conditions same rebuilt splits, same L 8-14 orthogonal to n, same honest counters (probe 10, retrieval 200, SGDR 180, DSM tool 15, etc., no n*3200), family-stratified B=5000.

| Condition | M_total f10 | f100 | per_hit mean | resolve_rate |
|-----------|-------------|------|--------------|--------------|
| B-COLD | 5992.7 | 5992.7 | 550.0 | 0.0 |
| B-RAG k5 | 1315.1 | 1315.1 | 103.9 | 0.234 |
| B-STAGEHAND | 4719.3 | 4719.3 | 432.8 | 0.234 |
| B-DSM O1 | 6236.1 | 6164.1 | 562.1 | 0.0 (overlap 0) |
| B-SGDR | 1295.1 | 1295.1 | 103.9 | 0.234 |
| P-SPIDER SUT | **1981.1** | **1891.1** | 168.6 | **1.0** |

- **Saving vs COLD f10:** 0.669 [0.652,0.687] (>=25% **met on ceiling**)
- **Ratio vs RAG f10:** 1.506 [1.479,1.531] (>0.85 **FAILED on ceiling**; f100 1.438 also fails) — probe+repair+auditor+distill overhead per-trajectory exceeds once-per-trajectory retrieval on this fixture.
- **Browser+latency saving:** 0.494 (>=20% met on ceiling model).
- **Resolve margins (diagnostic, not success):** SPIDER vs COLD 1.0, vs RAG/STAGEHAND/SGDR 0.766, vs DSM 1.0 — kernel.resolve 192/192 EXECUTABLE bound_ok 1.0 via dot-regex.
- **Per_hit normalized vs COLD step (550):** 0.135 at n0 and 0.293 at n0.25 both <0.85 (raw 74 and 161 tokens); supersede conjoint cannot trigger because Pareto dominance fails.
- **Rho diagnostics (file-proxy, not claim):** rho_novelty pooled 0.762 [0.688,0.823], per-family 1.0, rho_length -0.287.

DSM site overlap 0/36 disclosed degenerate (registry sites considered 0 due to site field absent, task sites 36). Cost $0.002-0.092 not measured.

---

## 5. Substrate & Freshness Gate

- **Single-node HS256 WAL:** /tmp/spider-runtime/shared.db, gunicorn 23.0.0 single-worker pid 51939, nginx 1.24.0 $request_uri consistent hash single upstream 127.0.0.1:18929, PyJWT 2.14.0 HS256 only.
- **Health gate:** n_non304 400 stratified 200/200 >=360/180 PASS, n_requests 406 If-None-Match 1.0 errors 0, n_304 351, n_200 745, single_worker true, INM exercised 1096 log rows.
- **Correlated probe:** n0 1.0 (150/150 304), n0.25 accuracy 1.0, false_accept 0.0, TN 1.0, saving 0.40 vs full-fetch, random 0.593 delta 0.406 >0.10 required.
- **TN contrast:** sticky 1.0 vs direct 1.0.
- **SQLite WAL verification:** journal_mode wal, shared.db path, sticky log 1053 lines upstream set 127.0.0.1:18929.

Re-verified on this packet; prior 400 not sufficient without re-measurement per MV4 — now re-measured.

---

## 6. Browser/LLM Substrate (MV6/MV7 — not provisioned)

- **GHCR:** docker pull ghcr.io/servicenow/browsergym:0.14.3 denied (manifest unknown).
- **Playwright:** 1.44.0 importable vs frozen 1.63.0 required.
- **BrowserGym:** no package metadata (browsergym-core missing), webarena_verified not installed.
- **OPENAI_API_KEY:** ABSENT — no real gpt-4o-mini 15-step tokens, rho_proxy_real NULL, safety CuP NULL.
- **Supplementary signal:** local playwright synthetic 60-node DOM AX 46 (>10) proves AX enumeration, but not GHCR 2000-node CDP; honest browser_steps/latency and rho_proxy remain null.

Per spec, BrowserGym/LLM absence => MEASUREMENT_INVALID for Pareto dominance vs RAG/Stagehand/DSM/SGDR at f=10/100, irrespective of token saving. No file-proxy surrogation.

---

## 7. Interpretation (INTERPRETATION distinct from RAW EVIDENCE)

- **RAW EVIDENCE:** probe_traces.jsonl 162k lines per-request, substrate_probe.json, fixture_checks.json, economics_per_trajectory.csv 193 rows, null_controls with 5000 block-permutations.
- **DERIVED MEASUREMENT:** gaps, CIs, AUROC, rho diagnostics via family-stratified bootstrap/permutation.
- **INTERPRETATION:** Single-node substrate and correlated freshness are **validated** (TN 1.0, saving 0.40). Contamination-free holdout **retained** (0/36 disjoint). Kernel **functionally durable** (5/5) but not commit-durable. Economics **ceiling** shows saving vs COLD but ratio vs RAG fails on synthetic counters; this is **diagnostic not falsification** because browser/LLM gates blocked. The honest Pareto dominance vs RAG/Stagehand/DSM/SGDR at f=10/100 with safety non-inferior remains **unknown** pending provisioned substrate.
- **No promotion:** C-PRODUCT-ECON remains HYPOTHESIS; per_hit falsification 1.005>0.85 bounded to file-proxy remains, not superseded; distributed n>=800 not authorized.

---

## 8. Validity Threats

- **GHCR/LLM lockout:** Primary threat; blocks rho_proxy, safety, browser steps. Mitigation: retain single-node gate and honest counters; disclose ceiling.
- **NC1 deterministic coupling:** Honest counters reuse=max(0,L-n_novel*2) bakes in rho_length -0.287; blocks null validity. Requires real-trajectory re-measurement.
- **DSM overlap 0:** Synthetic fixture not overlapping compiled registry; DSM economics degenerate; requires Hard258 or overlapping fixture.
- **Kernel durability:** Working-tree correct but not committed to cee979c2-equivalent; cross-checkout durability unproven.
- **Playwright version drift & missing deps:** Blocks SURVIVES; does not affect counter ceiling validity.
- **SHA divergence:** Rebuilt holdout SHA c2763ebae9 vs requested 374ef8f6 due to flank-case rule; threat is distribution shift; mitigated by verified 0/36 disjoint + Jaccard 0.0.
- **File-proxy vs BrowserGym gap:** Synthetic costs do not measure real DOM heterogeneity, browser latency, or LLM token distributions.

---

## 9. Product Consequences

**Positive if SURVIVES:** Not met (MEASUREMENT_INVALID). Would have promoted C-PRODUCT-ECON HYPOTHESIS -> EXPERIMENTAL bounded to rebuilt + health-gated BrowserGym, superseded per_hit, authorized distributed n>=800.

**This packet (MEASUREMENT_INVALID):** No claim update. Correct handoff is smallest unblockers in order: (1) commit kernel d926279d to HEAD durable, (2) resolve GHCR pull (auth) + playwright 1.63.0 + OPENAI_API_KEY + BrowserGym 2000-node AX>10 to enable rho_proxy>=0.50 and safety, (3) stage overlapping DSM sites or Hard258 live sites for non-degenerate DSM vs inheritance, (4) break NC1 coupling on real trajectories to pass |rho_shuffled|<0.20 etc., (5) re-verify n>=360 and re-execute identical frozen PIVOT with 5000 bootstrap/permutation full C1-C5 gates.

---

## 10. References to Evidence

- `artifacts/env_audit.json` (pins 23.0.0/2.14.0 PASS, docker denied, OPENAI absent, kernel sha d926279d vs head 8af66ccf)
- `artifacts/fixture_checks.json` (0/36 disjoint, Jaccard 0.0, qcr 8c69804b, 714/2147)
- `artifacts/substrate_probe.json` (400 200/200, saving 0.40 delta 0.406)
- `artifacts/mv3_kernel_spot_check.json` (5/5 PASS)
- `artifacts/economics.json` (saving 0.669 ratio 1.506)
- `artifacts/null_controls.json` (p 0.072, rho_length -0.287)
- `artifacts/browser_health.json` (playwright 1.44 vs 1.63, AX synthetic 46)
- `src/spider/kernel.py` sha d926279d

All measurements preserve trajectory-grouped family-stratified B=5000 per spec. No bijective proxy.
