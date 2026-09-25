# EXP-PRODUCT-36095578013 — EXECUTE Report (product, C-PRODUCT-ECON REOPEN)

**Status:** `MEASUREMENT_INVALID` — `INCONCLUSIVE` (no claim update)
**Lane:** product — `research/lanes/registry.json: product` (allowed roots `src, tests, sdk, pyproject.toml`)
**Claim:** `C-PRODUCT-ECON` (`research/claims/registry.json` HYPOTHESIS, next_gate `end-to-end amortized economics on real agents`)
**Director mandate:** `request.json: director_mandate` REOPEN cognitive_reset false — honest M_total Pareto at f=10 before distributed n>=800 or f=100, single-node HS256 sticky n>=360 + BrowserGym 2000-node 1280x720 + gpt-4o-mini 15-step same model/tools/budget with k*5 5/10/15 and ST-WebAgentBench CuP safety

Frozen inputs byte-identical verified (freeze.json hashes `request 33fb2ce5e28952033d9b02e177950396de0d3bcf7727b477e2d2a02b031b6f92` `spec 397ffc124ea4a02e4adf0ecbbf6d06a74192649da06f35e066f1b3980c6c90c0` `prereg 190a9f8a5eac3f2616a8c54249d0d0a39abc94d2b82f55b5aebb170a2d5e14a8` frozen_at 2026-09-25T04:47:47Z) — no frozen file modified.

---

## 1. Question and hypothesis

See `spec.json:question` and `prereg.md` §1 verbatim. Primary hypothesis H1 requires contamination-free holdout 0/36 disjoint Jaccard 0.0 + single-node HS256 sticky n_non304>=360 stratified + durable kernel dot-regex + BrowserGym 0.14.3 2000-node CDP AX>10 + gpt-4o-mini 15-step with honest per-trajectory-reset sum counters k*5 to achieve at f=10: margin>=0.12 vs each baseline, calibration false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18, verification AUROC>=0.75 precision>=0.80, saving>=25% vs COLD browser+latency>=20% accuracy>=0.85 Pareto vs RAG/Stagehand/DSM ratio<=0.85, probe saving>=30% accuracy>=0.90 delta>0.10, rho_proxy>=0.50 per-stratum, CuP non-inferior.

---

## 2. What was actually measured (raw evidence vs observations vs derived)

**RAW EVIDENCE** preserved separately as artifacts (see `result.json:artifacts`). Key raw files:
- `artifacts/substrate_probe.json` (sha bdf399ba) — 406 health-gate requests, 150+150 probe traces with per-step probeHit/etagMatched/ttlValid
- `artifacts/probe_traces.jsonl` (sha 6ade74b2) — per-request status/etag/latency
- `artifacts/env_audit.json` (sha d905d68) — docker pull denied, OPENAI absent, pins
- `artifacts/browser_health.json` (sha 500b251f) — browser health null
- `artifacts/economics_per_trajectory.csv` (sha 5e4830c5) — 192 trajectories per-trajectory counters
- `artifacts/nc_trajectory_counters.json` — NC counters

**OBSERVATIONS** (direct, see `result.json:observations` 14 rows): OBS-1 GHCR denied, OBS-2 OPENAI absent, OBS-3 playwright missing, OBS-4 kernel not durable, OBS-5 fixtures 0/36 staged, OBS-6 Jaccard 0.0, OBS-7 substrate 400 200/200 pass, OBS-8 correlated delta 0.407, OBS-9 TN 1.0, OBS-10 MV3 5/5, OBS-11 PC3 AUROC 0.871, OBS-12 economics diagnostic saving 0.669 ratio 1.506, OBS-13 NC1 p 0.072 rho_length -0.287, OBS-14 CuP null.

**DERIVED MEASUREMENTS** (metrics in result.json): fixtures pass true, kernel_mv3 pass true functional but durable false, substrate_mv4 pass true, pc3 pass true, bounded ceiling economics saving 0.669 CI[0.652,0.687] ratio 1.506 CI[1.48,1.53] — all honest sum counters with k*5, not claim gates. Claim-level metrics (C1-C5 margins, AUROC real, rho_proxy per-stratum, CuP) are explicit null per EXPERIMENT_PACKET mandatory semantics.

**INTERPRETATION:** Per frozen falsifier precedence, at least four independent MEASUREMENT_INVALID gates fire before any FALSIFIES/SURVIVES evaluation: GHCR manifest denied, OPENAI_API_KEY absent, playwright missing, kernel not durable. Infrastructure failure is not scientific negative per AGENTS.md failure discipline and EXPERIMENT_PACKET s9. Outcome is INCONCLUSIVE.

---

## 3. Controls

**PC-SINGLE-NODE-ECON-CORRELATED (5 checks):** Substrate half PASS (n_non304 400 200/200 TN1.0 saving 0.40 delta 0.407 WAL single-worker HS256 sticky 1053 lines). Browser/LLM half NOT TESTABLE (GHCR denied, OPENAI absent, playwright missing, CuP null) → UNKNOWN per precedence. Evidence refs in result.json.

**NC-SHUFFLE-ECON (4 nulls):** NC1 rho_shuffled -0.137 (|.|<0.20) but block-permutation p 0.072 FAIL <0.20 and rho_length pooled -0.287 FAIL |.|>=0.20 per-stratum -0.084 to -0.657 all FAIL; NC2 UNKNOWN 0.654 AUROC 0.462 PASS; NC3 R2 4.3e-05 PASS; NC4 delta 0.407 logged; rho_proxy shuffled null. Overall FAIL at bounded ceiling — deterministic coupling disclosed, must break on real trajectories.

**Baselines B-COLD/B-INSTRUCTIONS/B-RAG-K5/B-STAGEHAND-CACHE:** Bounded-ceiling honest counters only (see metrics). No claim success/accuracy measured on BrowserGym trajectories — explicit null UNKNOWN per precedence. RAG cheapest at 1315 tokens vs SPIDER 1981 ratio 1.506 is honest-counter diagnostic, not Pareto proof.

All control identifiers stable per spec.json (PC-SINGLE-NODE-ECON-CORRELATED, NC-SHUFFLE-ECON) and prereg.

---

## 4. Measurement validity gates MV1-MV12

- MV1 contamination-free holdout PASS 0/36 pool+usage disjoint sha 101e481d (realized) fallback allowed, Hard258 not staged
- MV2 family hold-out zero-overlap Jaccard 0.0 on 630 pairs PASS
- MV3 kernel dot-regex functional 5/5 PASS but durable via_commit false — GHCR-style gate pending commit → triggers MEASUREMENT_INVALID per falsifier (1)
- MV4 single-node HS256 sticky n_non304 400 stratified 200/200 PASS TN>=0.85, If-None-Match 1.0
- MV5 correlated TTL 60s ETag W/body_sha saving 0.40 accuracy 1.0 false_accept 0.0 delta 0.407 >0.10 PASS substrate only
- MV6 Docker BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10 BLOCKED (pull denied) — triggers MEASUREMENT_INVALID
- MV7 same model/tools/budget gpt-4o-mini 15-step BLOCKED (OPENAI absent, playwright missing) — triggers MEASUREMENT_INVALID
- MV8 honest amortized sum counters k*5 5/10/15 honored PASS diagnostics but claim Pareto null
- MV9 strong baselines identical splits PASS diagnostics honest but claim margins null
- MV10 calibration MockEnv PASS AUROC 0.871 but real trajectories null
- MV11 statistics B=5000 family-stratified trajectory-grouped bootstrap + block-permutation machinery intact; NC1 coupling FAIL at ceiling
- MV12 abstention repair verified_state MEA diagnostic PASS on MockEnv but CuP safety null

Any single MV6/MV7/MV3-durable failure suffices for MEASUREMENT_INVALID irrespective of diagnostic economics.

---

## 5. Decision rule (precedence ordered)

Per spec.json falsifier: (1) MEASUREMENT_INVALID if any PC check fails OR n<360 OR BrowserGym absent OR fixtures contaminated OR kernel not durable OR GHCR/OPENAI absent without disclosure — irrespective of margins, no file-proxy surrogation. This packet fires on GHCR denied + OPENAI absent + playwright missing + kernel not durable. Therefore status MEASUREMENT_INVALID outcome INCONCLUSIVE without reaching C1-C5 FALSIFIES/SURVIVES evaluation. Diagnostic economics (saving 0.669 vs COLD, ratio 1.506 vs RAG) are not gated as claim evidence and are disclosed as bounded ceiling only.

---

## 6. Product consequences

No C-PRODUCT-ECON promotion. Claim remains HYPOTHESIS (bounded, not rejected on honest substrate). Per prereg product_consequence_negative for MEASUREMENT_INVALID: no claim update; handoff retains contamination-free holdout 0/36 Jaccard 0.0, substrate health 400 TN1.0, kernel dot fix working-tree, probe delta 0.407; requires re-provision GHCR 0.14.3 + OPENAI_API_KEY + playwright 1.63.0 with k*5 5/10/15 + CuP ST-WebAgentBench, commit kernel to HEAD durable, fix NC1 deterministic coupling on real trajectories, re-verify n>=360 before distributed n>=800 or f=100 authorization. Per_hit 1.005>0.85 bounded rejection stands not superseded (requires conjoint Pareto dominance + rho>=0.50 + AUROC>=0.75 + safety).

---

## 7. Validity threats and disclosure

- Synthetic freshness driver via body_sha counter not real-world rate distribution
- Localhost latency not WAN
- MockEnv AUROC 0.871 does not transfer to gpt-4o-mini
- Jaccard 0.0 is bigram over first-slot pool values, not value_set intersection (which is separately verified 0/36)
- Single-node n=400 is frozen minimum; distributed n>=800 out of scope
- sklearn/pandas absent but not gating pins_pass true
- Cost realism includes verification/repair at f=10 but claim Pareto requires full decomposition vs browser+latency vs accuracy with real tokens — not measured here

---

## 8. Unresolved and next actions

See result.json unresolved UNR-1..UNR-6: re-provision BrowserGym GHCR, OPENAI key, playwright 1.63 binaries + ST-WebAgentBench, commit kernel, re-execute identical frozen REOPEN with trajectory-grouped 5000 bootstrap/5000 block-permutation and k*5 and CuP before any f=100 or distributed claim. Ordered unblockers in handoff carry_forward.

---

*Report is explanatory; canonical JSON is in result.json per EXPERIMENT_PACKET. No contradiction between report and result.json; frozen claim not exceeded.*

