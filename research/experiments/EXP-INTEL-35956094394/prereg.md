# EXP-INTEL-35956094394 — preregistration

## 1. Experiment Identity
- **experiment_id:** EXP-INTEL-35956094394  
- **lane:** intel  
- **claim_ids:** C-CROSSSITE (primary), C-RESIDUAL-NOVELTY, C-PRODUCT-ECON (downstream economics ceiling)  
- **parent_handoff:** research/experiments/EXP-INTEL-35947486685/handoff.json sha256 fd40d3c0159e64c7b7c166a02d0ecc868816c5e4acaab52ccf851e2d81c1b9dd  
- **parent disposition:** **SUPERSEDE** per Global Director mandate cycle 35955604667 (PIVOT from degenerate product-page AX longest-prefix). Inherited handoff is continuity evidence only.  
- **binding direction:** request.json director_mandate (action PIVOT, target C-CROSSSITE, question cited below). This prereg converts the Director's strategic question into the smallest falsifiable experiment; it does **not** re-authorize the parent's H1/H2/H3 N=20 full-tree longest-prefix program.

## 2. Director's Strategic Question (verbatim, binding)

> Can Intel deliver the durable census and external baseline substrate that unblocks cross-site transfer: (1) acquire WebArena-Verified v2 812-task census via durable pinned source (HuggingFace OpenEnv BrowserGym hosted layer or Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb with 64-char hash, byte-identical manifest) and repair fragment extraction for BrowserGym CDP Accessibility.getFullAXTree 1280x720 AX>10 noise handling, and (2) blindly reproduce external SOTA baselines (Agentic Compilation DSM 99% + deterministic JSON IR + HITL patching $0.002-0.092, TraceCompiler def-use 0.928/0.943, browser-memory catalog deterministic replay) on SPIDER's synthetic 40-task alias-OOD (30 orthogonal header/body/auth +10 mixed multi-channel) with trajectory-grouped bootstrap coverage/CIs and honest per-trajectory-reset sum-counter M_total_f10 Pareto f=10/100 vs SPIDER alias-catalog/routing/WebMCP, measuring where SPIDER must beat O(1) compilation to claim residual-novelty economics?

Prior evidence distinguished from SPIDER evidence (agent priors labeled in mandate): path dependence/context salience (Jaccard ≥0.6 over-match), compounding planning errors requiring |rho_shuffled|<0.20 trajectory-grouped CIs, tool/API bypass vs DOM/AX volatility requiring hybrid dispatch, and calibration/abstention gating (ECE≤0.15, UNKNOWN precision≥0.85, FA≤0.10) — used to weight priors, not treated as SPIDER observations.

## 3. Why this pivot, not the parent continuation

- Parent N=20 product-page full-tree AX program is 7th repeat of same degenerate substrate: homepage-biased (18/20 identical 1430-node captures, CI [0.7,1.0], shuffle p=1.0, Stagehand HIT 0.0), adequacy <5 families vs frozen ≥10, WebGym 0/50 (401/404), Gate0 0 transitions — audit identifies 6 blocking infra fixes (FIX-A 8s timeout vs ≥300s, FIX-B missing packages/pip freeze empty, FIX-C salted hash determinism, FIX-D missing body regex, FIX-E provenance hash corruption, FIX-F max 2 product families vs 10). Expected outcome of another repeat is MEASUREMENT_INVALID, not discriminating.
- Exhaustive alternatives (567 MB LFS test.zip, 420-task CAP enumeration) already judged ABANDONED / falsified as vacuous single-store 0.9479 duplication.
- Global portfolio assessment: 327 exps, 33% MEASUREMENT_INVALID overall, 10/15 last pulse invalid; C-MEAS-VALID blocked after 92 exps, C-PARAM-INHERIT 8 consecutive invalid on WebArena-Verified v2 hold-out. Bottleneck is measurement substrate validity. Delivering durable census + external baseline ceiling has highest marginal information: directly unblocks Graph ≥10-family hold-out and Product Stagehand/WebMCP Pareto, decides true website-holdout gate without site-identity leakage.

## 4. Hypotheses (falsifiable, per spec)

**H_A_DURABLE_CENSUS:** A byte-identical durable pin (HF or Docker, ≥2 genuine attempts, 64-char digest) can yield a verifiable WebArena-Verified v2 census (812 tasks ±10, 192 shopping/184 shopping_admin, 36 families_ge3) and a repaired fragment pipeline at 1280×720 (BrowserGym-core 0.14.3, AgentLab 0.4.2, Playwright 1.63.0, CDP Accessibility.getFullAXTree) achieving median AX>10, median DOM≥2000 across ≥10 probe captures, outerHTML SHA256 recomputed AFTER page.content()+AX with 9 base + expanded (form_key/uenc/store/session/timestamp/nonce) + body-regex stripping, grammar hash recomputed live, SHA stability before==after TRUE and after mutation != TRUE on ≥10 families, richer AX bbox/computedStyle present.

**H_B_SOTA_CEILING:** On SPIDER's synthetic 40-task alias-OOD (10 header-param +10 body-param +10 auth-param +10 mixed, deterministic seed, generation code hash), blind reproduction of B-AGENTIC-DSM (99% IR), B-TRACECOMPILER-DEFUSE (0.928/0.943), B-BMEM-CATALOG (deterministic replay) yields coverage + honest per-trajectory-reset sum-counter M_total_f10/f100 (resolve+bind+verify+freshness+browser_steps, amortized f=10/100) with trajectory-grouped bootstrap 95% CIs (B=2000, unit=task/trajectory), alongside identically-measured SPIDER baselines (alias, routing, WebMCP), quantifying the O(1) compilation cost ceiling SPIDER must beat for residual-novelty economics.

Do_not_assume carried forward: 0/20 valid captures ≠ impossibility; Stagehand 0/36 ≠ disproof; WebGym 0/50 and Gate0 0 are MEASUREMENT_INVALID not negatives; sampling determinism and body regex not yet repaired.

## 5. Designs — coordinated two-module experiment

### 5.1 Module A — Durable census & fragment repair

**A1. Durable-source acquisition (two paths, each ≥2 genuine attempts):**
- SRC-HF: GET https://huggingface.co/datasets/.../BrowserGym or ServiceNow WebGym manifest raw + Hub API /v2/repositories/.../tags, with `Authorization: Bearer HF_TOKEN` when token set. Capture URL, HTTP status, bytes, sha256 hex, manifest byte length. HF_TOKEN presence logged (true/false) — not required true, but attempts must log header use.
- SRC-DOCKER: Verify 64-char digest sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb via Hub API 200 + local `docker pull am1n3e/webarena-verified-shopping@sha256:...` (timeout ≥300s) or `docker load < cached.tar` / ghcr mirror fallback. Capture `docker images --digests`, `docker pull` stdout/stderr/returncode, Hub API digest substring 64 hex. Run health check `curl http://localhost:7770` 3 retries.
- Byte-identical manifest: sha256 hex equality stored. If only one source succeeds, single pinned sha256 + 2 log files suffices; cross-source equality explicitly marked unavailable.
- Census artifact: `research/intel/manifests/webarena_verified_pin.json` (or experiment artifacts/raw) with pinned URL, digest 64 hex, byte length, download log, census counts: total tasks, shopping, shopping_admin, families_ge3, family size histogram, product-page-capable filter count, WebGym 292k sample ≥50 diverse eTLD+1 slice if manifest available (otherwise census still valid for WebArena portion). Verification that file content hash equals logged sha256.

**A2. Fragment extraction repair probe:**
- Stack: BrowserGym-core==0.14.3, AgentLab==0.4.2, Playwright==1.63.0, `playwright install --with-deps chromium`, viewport 1280×720. Evidence: `pip freeze` non-empty sha256, `playwright --version` capture, chromium path check.
- Method: CDP Accessibility.getFullAXTree via `page.context().newCDPSession(page)` → `client.send("Accessibility.getFullAXTree")` (not `page.accessibility.snapshot()` fallback). Captures heading/price/add-to-cart/main/contentinfo product-subtree anchoring (role+name+CSS) and full-tree traversal (no [:20] truncation).
- Stripping & hash: outerHTML → strip 9 base regex + 6 expanded + body regex `<body[^>]*>.*?</body>` DOTALL via `page.evaluate` before SHA256, recomputed AFTER `page.content()`+AX, grammar file `research/intel/grammar_fulltree_358885.py` repaired to include body regex and expanded patterns, hash recomputed live at capture (not hardcoded).
- Probes: ≥10 captures (synthetic Flask fixture qualifies if Docker unreachable; otherwise WebArena product pages). Synthetic fixture localhost product page with fixed DOM (heading, price, add-to-cart, main, contentinfo) provides deterministic 20-node AX tree — required as positive control. Measure median AX nodes, median DOM bytes, richer AX fields (bbox, computedStyle) presence, SHA stability both directions (identical on re-capture, changed on visible textContent/name mutation via `page.evaluate`).
- Artifacts: `artifacts/raw/ax_captures.jsonl`, `artifacts/derived/ax_consistency_fulltree.json` (bootstrap reps 2000, shuffle perms 1000, trajectory-grouped).

### 5.2 Module B — External SOTA reproduction on synthetic 40-task alias-OOD

**B0. Synthetic fixture:** `research/intel/synthetic_alias_ood_40.json` (generate deterministically if missing; seed 360360, generation script hash logged). 40 tasks: 10 header-param orthogonal, 10 body-param orthogonal, 10 auth-param orthogonal, 10 mixed multi-channel (header+body+auth). Each task records channel label orthogonality (no cross-channel leakage). Distribution shift: training sees alias value A, test requires unseen alias B per channel; family = mechanism family, task_id = trajectory.

**B1. External baselines (BLIND — implement per paper recipe without tuning to synthetic channel labels):**
- B-AGENTIC-DSM: Deep-Structure Model template → deterministic JSON IR → HITL patch hook. Measure coverage (EXECUTABLE+verify pass) and cost: USD ($0.002-0.092 per paper) + M_total honest counter.
- B-TRACECOMPILER-DEFUSE: trace → def-use chain → IR compilation per 0.928/0.943 spec. Coverage likewise.
- B-BMEM-CATALOG: exact selector replay without alias slot handling (deterministic). Expected to dominate on no-shift, collapse on alias-OOD — demonstrates alias problem.
- Implementation constraint: same 40-task split in single run, per-task log written (`artifacts/derived/sota_blind_results.jsonl` with task_id, baseline id, success bool, per-channel label, cost counters, IR snippet hash).

**B2. SPIDER baselines (identically-measured honest costs for Pareto):**
- B-SPIDER-ALIAS, B-SPIDER-ROUTING, B-SPIDER-WEBMCP, B-COLD-LLM. Each runs on identical 40-task split, same honest sum-counter harness (per-trajectory reset). WebMCP prevalence logged as tool bypass rate, amortized f=10 and f=100. Routing includes param-slot-count tie-break + recalibrated confidence 0.95/0.85.

**B3. Honest cost instrumentation (critical — replaces pre-2.0 invalid proxies):**
- Per-trajectory-reset sum-counter: M_total(task) = resolve + bind + verify + freshness_check + browser_steps (each counted per attempt, reset at trajectory start). Sum across 40 tasks → M_total_f10 amortized ( / min(f, N) with f=10) and M_total_f100 (f=100). No `n*3200`, no `f*6.0`, no Gaussian jitter. Logged per task in jsonl; total and per-channel breakdowns.
- Trajectory-grouped bootstrap: B=2000 resamples with replacement on task/trajectory unit (not transition or step), 95% percentile CI [lower,upper] for coverage and for M_total_f10/f100 × non-degenerate width reported, variance>0.
- Shuffle control |rho_shuffled| and coverage shuffle: within-stratum permutation of family/alias mapping, 1000 perms, trajectory-grouped.

## 6. Baselines table (stable IDs downstream can reuse)

| ID | Type | Purpose | Expected vs null |
|---|---|---|---|
| B-DURABLE-HF | durability | HF pin durability | 200 + byte-identical sha256 |
| B-DURABLE-DOCKER | durability | Docker 64-char digest + reachable | digest_valid + reachable true |
| B-TRUNCATED-20 | fragment null | [:20] truncation vs full-tree | delta_vs_truncated ≥0.20 |
| B-AGENTIC-DSM | external_sota | O(1) compilation ceiling | 0.95-0.99 single-channel |
| B-TRACECOMPILER-DEFUSE | external_sota | def-use ceiling | 0.928 / 0.943 |
| B-BMEM-CATALOG | external_sota | exact replay ceiling | collapses on alias shift |
| B-SPIDER-ALIAS | spider | SPIDER alias-catalog | compare to DSM |
| B-SPIDER-ROUTING | spider | routing + slot-count tie-break | compare to TraceCompiler |
| B-SPIDER-WEBMCP | spider | tool bypass prevalence | f=10 vs f=100 Pareto |
| B-COLD-LLM | cold | floor | lowest coverage |

## 7. Controls (stable IDs)

**Positive controls (must pass or MEASUREMENT_INVALID):**
- PC-A (PC-SYNTHETIC-FIXTURE): synthetic Flask product fixture at 1280×720, 20 AX nodes fixed. Expect median AX>10, DOM≥2000, SHA before==after identical TRUE, SHA after textContent mutation != TRUE. Validates AX pipeline can succeed.
- PC-B (PC-TOY-DSM): toy single-header param task compiles via DSM IR to 1.0 coverage. Validates external harness not scaffolding-broken.

**Null controls (must be computed trajectory-grouped):**
- NC1-SHUFFLED (NC-SHUFFLED-AND-TRUNCATION subset): family-label permutation of duplication prevalence and coverage (1000 trajectory-grouped perms). Expect |rho_shuffled|<0.20, coverage shuffle mean ~ chance, gap real−shuffle ≥0.20, p>0.05.
- NC2-TRUNCATED (B-TRUNCATED-20): `tokens[:20]` / `selectors[:20]` baseline vs full-tree. Expect delta_vs_truncated ≥0.20 for full-tree to be non-vacuous; shuffled version <0.05.
- NC3-NO-HITL: Agentic DSM with HITL hook replaced by no-op/random patch. Expect coverage drop ≥0.30 vs HITL, isolating patch contribution.

## 8. Metrics (stable names for result.json / audit.json)

Census & fragment (Module A):
- M_A1_SRC_HF_SUCCESS (bool), M_A1_SRC_DOCKER_SUCCESS (bool), M_A2_MANIFEST_SHA256 (hex), M_A2_BYTE_IDENTICAL (bool), M_A3_CENSUS_TOTAL_TASKS (int), M_A3_FAMILIES_GE3 (int), M_A3_SHOPPING (int), M_A3_SHOPPING_ADMIN (int), M_A3_DIVERSE_ETLD_PLUS1 (int, optional), M_AX_VALID_CAPTURES (int), M_AX_FAMILIES_FOUND (int), M_AX_NODES_MEDIAN (int), M_DOM_BYTES_MEDIAN (int), M_SHA_STABILITY_IDENTICAL (bool), M_SHA_MUTATION_CHANGED (bool), M_AX_RICHER_BBOX (bool), M_AX_CONSISTENCY_MEAN, M_AX_CONSISTENCY_CI_LOWER/UPPER (trajectory-grouped), M_AX_SHUFFLE_P (trajectory-grouped), M_AX_DELTA_TRUNCATED

Blind reproduction & economics (Module B):
- M_COV_AGT_DSM (prop), M_COV_AGT_DSM_CI_LOWER/UPPER, M_COV_TRACE (prop), M_COV_BMEM (prop), M_COV_SPIDER_ALIAS / ROUTING / WEBMCP / COLD (prop each, per-channel split orthogonal vs mixed)
- M_TOTAL_F10_AGT_DSM, M_TOTAL_F10_TRACE, M_TOTAL_F10_BMEM, M_TOTAL_F10_SPIDER_ALIAS/ROUTING/WEBMCP, with CI_LOWER/UPPER each (honest per-trajectory-reset sum-counter, B=2000 trajectory-grouped)
- M_TOTAL_F100_* (same, amortized f=100)
- M_COST_USD_AGT_DSM (mean USD per task), CI
- M_RHO_SHUFFLED (cost vs length correlation), M_FALSE_ACCEPT (mechanism FA rate)
- Pareto entries: Pareto f=10 and f=100 table (coverage vs M_total amortized) for all 6 baselines

## 9. Measurement validity gates (MV1-MV8 — see spec.json)

Failure on any MV is MEASUREMENT_INVALID, not falsification:
- MV1 ≥2 genuine attempts per durable source with logged evidence (timeout ≥300s or docker load).
- MV2 byte-identical sha256 + 64-char digest explicit; cross-source equality not assumed.
- MV3 versions/viewport/CDP path/grammar hash recomputed live; fallback snapshot = invalid.
- MV4 SHA stability both directions on ≥10 families (or ≥2 repeats on synthetic fixture if Docker unreachable).
- MV5 synthetic 40-task split deterministic, orthogonality verified, generation hash logged.
- MV6 honest per-trajectory-reset sum-counters only; trajectory-grouped bootstrap B=2000; no n*3200/jitter proxies.
- MV7 blind implementation per cited recipe, per-task logs for all 40×6.
- MV8 every durable/cost path provenance path+sha256 captured.

Representation loss disclosed: DOM outerHTML normalized before hash loses page height/scroll state/visual computed style beyond AX bbox; AX tree at 1280×720 loses mobile viewport variance; synthetic alias-OOD loses real site DOM volatility and auth/session expiry dynamics — bounded CEO stated.

## 10. Decision rule (frozen, three-way — precedence A > B > C)

**A. MEASUREMENT_INVALID** if any MV1-MV8 fails (fewer than 2 genuine attempts, missing 64-char digest/byte hash, pip freeze empty or version/viewport mismatch, body regex absent, honest-counter proxy or ungrouped CI detected). Then no SURVIVES/FALSIFIED inference.

**B. SURVIVES_CURRENT_TEST** iff A passes AND:
- H_A_SURVIVES: (SRC_HF_SUCCESS OR SRC_DOCKER_SUCCESS) with census artifact manifest_sha256 pinned, total_tasks in 700-812, families_ge3 ≥30 recorded, AND AX repair probe median AX>10 & median DOM≥2000 with SHA stability both directions TRUE and richer AX present (≥10 captures); AND
- H_B_SURVIVES: all three external baselines executed blind on 40 alias-OOD with per-task logs, coverage point estimates + trajectory-grouped 95% CIs non-degenerate, honest M_total_f10/f100 with CIs + costs, |rho_shuffled|<0.20, SPIDER baselines measured identically for Pareto, PC-A/PC-B passed.

Unreadable/degenerate signals (full-page LCP 0.0 variance 0 from prior degenerate captures, CI[null,null] or CI[1,1] with variance 0) explicitly NOT counted as valid.

**C. FALSIFIED_IN_SETTING** if A passes (measurement valid) but B thresholds fail after genuine attempts: both durable sources persistent 401/404 or byte mismatch after 2 attempts, or AX median ≤10 / SHA stability false, or external baselines fail to run blind or are indistinguishable from NC1/NC2/NC3 shuffles (coverage within null CI, |rho|≥0.20, delta_vs_truncated<0.05, HITL null not worse by ≥0.30). Outcome MIXED if one module survives and the other falsified.

## 11. Validity threats and mitigations

- **Network/HF_TOKEN variability:** Mitigated by ≥2 attempts each source + HF_TOKEN true/false logged; failure with token false still informative (2-attempt precedence satisfied). Do not assume token false = source unavailable.
- **Docker pull size/time:** 5.4GB; mitigated by ≥300s timeout + docker load cached tar/ghcr fallback; script-imposed 8s cap is MEASUREMENT_INVALID per parent audit FIX-A.
- **Determinism (PYTHONHASHSEED):** mitigated by sha256/int derivation for within-family sampling and deterministic synthetic generation seed + hash.
- **Body regex miss:** grammar sha256 without body pattern fails MV3 — must repair file and re-verify live.
- **Synthetic orthogonal leakage:** header/body/auth channels independently parameterized; generation script asserts cross-channel independence; mixed tasks combine all three channels.
- **Honest cost contamination:** per-trajectory reset counters prevent n*3200 inflation; trajectory-grouped bootstrap prevents transition-independence pseudoreplication.
- **Blindness leakage:** external baselines coded from paper recipe docs before seeing synthetic labels; code hash logged pre-run.

## 12. Estimated cost and information gain

Cost: see spec estimated_cost (2.5-4h runner, docker pull 5.4GB, 120+120 task executions, no LLM calls needed).

Information gain: High — decides whether durable artifact delivery unblocks Graph hold-out (≥10 families) and Product Pareto vs O(1) compilation; quantifies ceiling SPIDER must beat; supersedes degenerate AX repeat and vacuous LFS/CAP alternatives.

## 13. Consequences

**If SURVIVES:** Census artifacts become Codex dependencies; Graph next can attempt parameterized hold-out on durable pin; Product can run Stagehand/WebMCP vs compilation Pareto with honest costs to decide promotion; Intel census substrate considered delivered (promotion to artifact dependency, not kernel code).

**If FALSIFIED:** No durable pin at current coordinates — try WebMall/Mind2Web-2 loopback; or alias-OOD misaligned with external baseline domains — redesign synthetic channels before Product claims economics. C-CROSSSITE stays HYPOTHESIS.

**If MEASUREMENT_INVALID:** No claim update; smallest repair is infra fix per MV1-MV8 and re-run identical frozen design.

## 14. Execution plan (no outcome-bearing measurements in DESIGN)

1. Resolve durable sources: 2 genuine HF manifest GETs + 2 docker pulls/loads with provenance captures; write byte-identical pin.
2. Run census counts on pinned manifest; write census json with sha256.
3. Provision BrowserGym-stack (pip install, playwright install --with-deps, viewport 1280x720), verify pip freeze hash.
4. Repair grammar file (add body regex if missing), recompute hash live.
5. Execute AX repair probe (synthetic fixture + WebArena if reachable) for ≥10 captures, mutation stability both ways.
6. Generate/validate synthetic 40 tasks (or load existing), verify 30+10 split and orthogonality.
7. Blind-run 6 baselines (3 external + 3 SPIDER + cold) on identical 40-task split with honest per-trajectory counters; collect per-task logs.
8. Compute trajectory-grouped bootstrap CIs, NC shuffles, delta_vs_truncated, HITL ablation.
9. Emit result.json (schema_version 1, status COMPLETE/MEASUREMENT_INVALID/BLOCKED, outcome SUPPORTS/FALSIFIES/MIXED/NOT_APPLICABLE), report.md, provenance.json with all path+sha256, plus artifacts per spec.

## 15. Preregistration freeze

This prereg.md together with spec.json (hashes in freeze.json) constitute the frozen design. Any analysis change after outcomes is exploratory; a new confirmatory claim requires a new prereg and untouched evidence. This design does not inspect outcome measurements; only the binding request/director mandate, parentハンドオフ establishment quadrants, and Codex statistics were consulted.

