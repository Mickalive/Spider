# EXP-PRODUCT-36091881382 — Preregistration (DESIGN, frozen before EXECUTE)

**Lane:** product — `research/lanes/registry.json: product` (allowed roots `src, tests, sdk, pyproject.toml`)  
**Claim:** `C-LLM-INHERIT` — “A real LLM agent benefits from SPIDER beyond strong memory/instruction baselines” (`research/claims/registry.json` HYPOTHESIS, next_gate `same model/tools/budget; cold vs instructions vs retrieval vs SPIDER`). Secondary inform: `C-PRODUCT-ECON` economics gate at f=10 only, and Pareto vs RAG/Stagehand/DSM `$0.002-0.092`.  
**Director mandate:** `research/experiments/EXP-PRODUCT-36091881382/request.json: director_mandate` (allocation `REOPEN`, `claim_id C-LLM-INHERIT`, `cognitive_reset true`, `parent_handoff_disposition USE`, comparative_reasoning vs CONTINUE distributed n>=800 Pareto and vs WebMCP-tool variant). Strategic question verbatim in `request.json` and `spec.json:question`. Parent handoff `research/experiments/EXP-PRODUCT-36089498872/handoff.json` (sha `fd3a98d004b0d51bb717b36a59e30b63017d3bc7b33e68f045c3862183025938`, `MEASUREMENT_INVALID`) is continuity evidence only per `research/EXPERIMENT_PACKET.md` §2 and AGENTS.md global direction discipline — retained as established/rejected/unknown/do_not_assume but MUST NOT override Director REOPEN; `USE` means retain dependencies but test the Director's binding question.  
**Mode:** DESIGN ONLY — no outcome-bearing measurements; all thresholds frozen before `freeze.json`.

---

## 1. Research question (Director binding, minimal high-information)

On **health-gated single-node HS256 sticky substrate** (`n_non304>=360, TTL 60s ETag W/body_sha conditional probe stratified TN 1.0`) with **Docker BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10** and **real gpt-4o-mini 15-step Playwright same model/tools/budget** (honest per-trajectory-reset sum counters `resolve+bind+verify+freshness+browser_steps`, `|rho_shuffled|<0.20`, `rho_proxy_real>=0.50`, per-stratum `|rho_length|<0.20`, 5000 family-stratified bootstrap + 5000 block-permutation), does **SPIDER** (`freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic repair correct-family reconstruction, verified_state MEA auditor, TTL conditional probe`) vs **B-COLD** vs **B-INSTRUCTIONS** vs **B-RAG-EMBED TAU0.30/QCR k5** vs **Stagehand cache** achieve **success margin >=0.12 vs each baseline** with `false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18`, verification `AUROC>=0.75 precision>=0.80`, and **honest amortized saving >=25% vs COLD at f=10** (and Pareto vs RAG/Stagehand/DSM `$0.002-0.092`) **before any distributed `n>=800` or `f=100` Pareto claim**, on **contamination-free Hard258 or rebuilt 192/36 orthogonal Jaccard 0.0 disjoint value_set_A intersect B empty holdout**?

This is the smallest discriminating test that can change the promotion decision per Director rationale: Product at `365` canonical experiments remains `MEASUREMENT_INVALID` on all claims, gated by honesty reform; `13` consecutive `C-PRODUCT-ECON` `MEASUREMENT_INVALID` on `M_total` Pareto vs RAG/Stagehand before demonstrating prerequisite single-family LLM gap; single-node `n>=360` reduces infra risk while preserving BrowserGym realism vs distributed `n>=800` which fails honesty prerequisite (per_hit falsified `1.005>0.85` rho `0.363<0.60` now superseded by `M_total` Pareto but honest `M_total` requires `variance>0` substrate). If SPIDER fails `>=0.12` here, `f=100` Pareto cannot survive; if it survives, it justifies larger amortized economics and informs Graph param-inherit scaling.

---

## 2. Hypotheses (falsifiable)

- **H1 (primary, `C-LLM-INHERIT` REOPEN):** With contamination-free holdout (rebuilt `101e481d` `0/36` or Hard258 `d6527566` when delivered, cross-family Jaccard `0.0` on `630` pairs via `qcr_bank_manifest TAU0.30 sha 8c69804b`, `L 8-14` family-constant orthogonal to `n`) + health-gated single-node HS256 sticky substrate at `/tmp/spider-runtime/shared.db WAL single-worker gunicorn 23.0.0 + nginx 1.24.0 $request_uri` (`n_non304>=360` stratified `180/endpoint`, `TN>=0.85`, `If-None-Match fraction 1.0` errors `0`, `TN_fresh 1.0 TN_sticky 1.0`) + durable kernel dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` committed durable (`d926279d` vs `HEAD 8af66ccf` must be equal) + provisioned Docker BrowserGym `0.14.3` `2000-node` `CDP getFullAXTree` `1280x720` `AX>10` + real `gpt-4o-mini 15-step Playwright` same model/tools/budget, SPIDER achieves at `f=10`: (a) margin `>=0.12` vs EACH baseline (Wilson+bootstrap CI excludes 0, `n0 success>=0.85`), (b) calibration `false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18`, (c) verification `AUROC>=0.75 precision>=0.80` non-degenerate, (d) `M_total_f10` saving `>=25%` vs COLD decomposed `tokens vs browser+latency vs accuracy` with `browser+latency >=20%` `accuracy>=0.85` and Pareto vs RAG/Stagehand/DSM, (e) correlated probe `accuracy>=0.90 saving>=30% delta>0.10` vs seeded-42 random `0.53` with `TN>=0.85`, (f) `rho_proxy_real>=0.50` pooled+per-stratum and per-stratum `|rho_shuffled|<0.20 p>=0.20 |rho_length|<0.20 |rho_shuffled_proxy|<0.20`.

- **H0 (null):** Margins, calibration, verification or saving fail with controls PASS non-degenerate, or substrate/BrowserGym health fails rendering `MEASUREMENT_INVALID` (not falsification). Prior per_hit `1.005>0.85` bounded rejection stands unless this M_total Pareto with rho+AUROC conjoint supersedes.

Prior plausibility: Scout correctly diagnosed honesty-gate tunnel (per-trajectory sum counters, trajectory-grouped 5000 bootstrap+permutation, If-None-Match/ETag, verified_state), `0.525` alias ceiling with `0/10` mixed, non-Pareto residual-novelty, physics falsification pattern; Director adopted Scout sequencing but constrained Graph distributed freshness as premature and Parked distributed `n>=800 f=100` until single-node stable-header variance>0. Agent priors used (sunk-cost bias `0.525 21/40`, HTTP fidelity path dependence `6` GRAPH param-inherit `MEASUREMENT_INVALID`, autonomous error accumulation JIT `59%->25%`, O(MxN) DOM pruning, measurement honesty `|rho_shuffled|<0.20`) are priors distinct from SPIDER evidence per `request.json:director_mandate.agent_priors_used`.

---

## 3. Carry-forward from parent (preserved distinctions, USE disposition)

Per `parent_handoff` `fd3a98d0...` (`EXP-PRODUCT-36089498872` `MEASUREMENT_INVALID` `2026-09-25`):

**Established (retain as dependencies, re-verify this packet):**
- Frozen inputs byte-identical verified (request `e22a635a...` spec `c0371de2...` prereg `62b71a80...` freeze `2026-09-25T03:19:00Z`) with `MEASUREMENT_INVALID` correctly declared, no bijective `n*3200/f*6.0/jitter` proxy, family-stratified trajectory-grouped `B=5000` bootstrap+block-permutation machinery intact (audit exact match).
- Contamination-free holdout RETAINED at MV2: rebuilt `webarena_verified_v2_tasks_192_36_rebuilt.json sha 101e481ddb610df9598b0e3e5650e8c163ec7cbdc4679c5efc1e31104b3074c5` (`0/36` pool+usage disjoint, cross-family bigram Jaccard `0.0` on `630` pairs via `qcr_bank_manifest sha 8c69804b TAU0.30`, `L 8-14`) — supersedes `391e8f6c` (`18/36` contaminated). Verified via `value_set_A intersect B` not SHA.
- Single-node HS256 sticky substrate health-gated PASS at `n_non304 400 200/200 >=360/180` (`WAL pid single-worker 66712/52069 gunicorn 23.0.0 PyJWT 2.14.0 nginx 1.24.0 $request_uri sticky`) with `n_304 351 TN 1.0 probe saving 0.40 delta 0.4067 >0.10` vs seeded-42 random `0.53` — re-verify per MV4.
- Correlated `TTL 60s ETag W/body_sha` probe discriminates (`hit 1.0` at `n==0`, `accuracy 1.0 false_accept 0.0` at `n0.25`, saving `0.40`).
- Kernel dot-regex functionally PASS `5/5` (`src/spider/kernel.py` working-tree `d926279d` pattern `\$\{[A-Za-z_][A-Za-z0-9_\.]*\}` confidence `0.85`) but NOT committed durable (`HEAD 8af66ccf` vs working-tree, `provenance kernel_durable false`) — must be committed durable before DIRECTOR promotion.
- PC3 MockEnv calibration non-vacuous PASS `AUROC 0.8714` vs shuffled `0.4681` precision `0.9491` ECE `0.107` — validates pipeline on MockEnv not transfer to BrowserGym.
- Honest economics ceiling diagnostic (diagnostic not claim): `SPIDER f10 1981 vs COLD 5992 saving 0.669` but ratio `1.506 vs RAG` FAIL diagnostic not falsification (17 null metrics, `MEASUREMENT_INVALID`).
- QCR orthogonality `0.0` and toolchain pins `gunicorn 23.0.0 PyJWT 2.14.0 Flask 3.1.3 playwright 1.63.0 cost_config 50/15/180/10` retained.

**Rejected (bounded, do not generalize beyond):**
- Canonical `192/36 sha 391e8f6c` contaminated `18/36` — must not reuse.
- NC1 shuffled null deterministic file-proxy honest counters (`rho_shuffled -0.136 p 0.0724` FAIL `p>=0.20`, `rho_length -0.287` per-stratum all `>0.20`) — deterministic coupling disclosed; must break coupling on real trajectories.
- No rejection of `C-LLM-INHERIT` `M_total` Pareto on honest substrate — `MEASUREMENT_INVALID` bounded to infrastructure (GHCR denied, `OPENAI_API_KEY` absent, `playwright accessibility()` removed, kernel not durable).
- Per_hit `1.005>0.85` bounded to file-proxy metric-design not to `M_total` Pareto conjoint.

**Unknown (remain unknown until EXECUTE on provisioned substrate):** GHCR `BrowserGym 0.14.3` authorization + `playwright 1.63` binaries + `OPENAI_API_KEY` for `gpt-4o-mini 15-step` with `AX>10` heterogeneity and `rho_proxy_real>=0.50`; kernel commit durability; NC1 coupling break on real trajectories (`|rho_shuffled|<0.20 p>=0.20 |rho_length|<0.20`); honest `M_total` Pareto vs RAG/Stagehand/DSM at `f=10`; per_hit supersession conjoint; Hard258 heterogeneous census.

**do_not_assume (explicitly unsafe):** `MEASUREMENT_INVALID` is infrastructure failure not falsification; probe saving `0.40` or ceiling `0.669` does NOT imply Pareto dominance; working-tree kernel not durable; Jaccard `0.0` ≠ value_set disjointness; `MockEnv AUROC 0.871` does not transfer to `gpt-4o-mini`; NC1 band PASS ≠ null valid (`p 0.0724` FAIL); `B-STAGEHAND-PC1 1.0` file-proxy ≠ Docker `2000-node AX>10`; per_hit `0.135/0.293` bounded not proof supersession.

Director **REOPEN USE** retains these as dependencies/evidential continuity but re-tests the identical frozen single-family honest LLM-inherit margins on health-gated single-node + real BrowserGym `2000-node` `gpt-4o-mini` before distributed `n>=800` or `f=100` Pareto per `dependencies` (runtime sticky `n_non304>=360`, graph freshness `TN>=0.85 FA<=0.10`, intel Hard258 `d6527566` / rebuilt `192/36` holdout).

---

## 4. Experimental design (smallest high-information, not pre-2.0 repeat)

**Population & holdout:** Contamination-free holdout as gating holdout — rebuilt `192/36` (`sha 101e481d` realized, fallback `c2763ebae9`, requested prefix `374ef8f6`) `0/36` pool+usage disjoint `L 8-14` family-constant orthogonal to `n` via `qcr_bank_manifest sha 8c69804b TAU0.30` **OR** Hard258/WebArena-Verified `812` census `hash d6527566` when Intel delivers with same disjointness proof (`64-char` digest, value_set `0/N` disjoint, Jaccard `0.0`). Audit must recompute `value_set_A intersect B` on ALL families via value_set not SHA. `TRAIN`-only induction. If Hard258 added, log `64-char` digest and site overlap `>0` for DSM non-degenerate extension; gating holdout remains whichever staged but rebuilt `192/36` is fallback gating.

**Substrate (MUST be health-gated for SURVIVES):**
- Single-node `HS256` sticky at `/tmp/spider-runtime/shared.db` `WAL` single `gunicorn 23.0.0` single-worker `HS256 PyJWT 2.14.0` + `nginx 1.24.0 $request_uri` consistent-hash sticky, `If-None-Match`/`ETag W/body_sha` conditional `200` vs `304`, `n_non304>=360` stratified (`180/endpoint` where two endpoints, `TN>=0.85`, `If-None-Match fraction 1.0` errors `0`) — re-measured this packet, logged `shared.db WAL worker=1 JWT alg TN n_non304 stratified sticky hash ETag n_304/n_200 distinct_worker_pids single_worker` (`substrate_probe.json`).
- Correlated `TTL 60s max-age ETag W/body_sha` probe `10tok+30ms` fresh at `n0 ~1.0` vs `~50%` stale at `n=0.25` vs `seeded-42 random 0.53` decoupled NC, per-step `probeHit/etagMatched/ttlValid` logged, `probe_is_correlated true` for SUT, saving `>=30%` accuracy `>=0.90` `falseAccept<0.05` `delta>0.10`.
- Kernel dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` committed durable (`cee979c2`-equivalent `d926279d` `HEAD == working-tree`) — `provenance` must show `working-tree == HEAD` committed, `kernel/commit` logged, `5/5 n0 EXECUTABLE confidence>=0.80`.

**Browser + LLM (MUST for SURVIVES, else MEASUREMENT_INVALID):**
- `Docker` `BrowserGym 0.14.3` `ghcr.io/servicenow/browsergym:0.14.3` + `playwright 1.63.0` with binaries + `OPENAI_API_KEY` for `gpt-4o-mini` `15-step` `Playwright` `1280x720` `CDP getFullAXTree` `2000-node` `AX>10` heterogeneous — logged `Docker` availability, image digest, `BrowserGym` version, node count, viewport, real `tokens` per step, `browser_calls`, `latency ms`, `AX nodes>10`. Proxy vs real `Spearman rho_proxy_real>=0.50` pooled+per-stratum required plus per-stratum `|rho_length|<0.20 |rho_shuffled_proxy|<0.20`.
- Same `model/tools/budget` across ALL conditions (`SPIDER/COLD/INSTRUCTIONS/RAG/STAGEHAND`) — logged `model id`, `steps`, `tools`, `budget`, `AX nodes` per trajectory. Mismatch => `MEASUREMENT_INVALID` for LLM-inherit sub-claim.

**Conditions (5, same holdout splits, same L, same honest counters, same BrowserGym/budget):**
1. `B-COLD` — no memory.
2. `B-INSTRUCTIONS` — `B-COLD` + site-specific NL instructions (same token budget as probe overhead).
3. `B-RAG-EMBED-TAU030-QCR-K5` — QCR frozen-bank `TAU0.30` top-`k=5` (k=1 sensitivity) `200tok+150ms` with verify fallback.
4. `B-STAGEHAND-CACHE` — `DOM-hash` cache without `TTL` correlation (2x `~30%` claim), `hit 1.0` at `n0` else `0`; DSM `$0.002-0.092` contrast for Pareto.
5. `P-SPIDER-LLM-INHERIT` — freshness-gated `0.95/0.85 Jaccard 0.85` + deterministic repair + correct-family + `TTL` probe + `MEA auditor` `softmax temp0.15+jitter`.

All TRAIN-only induction, `value_set_A intersect B empty` strictly on all families, cross-family `Jaccard max 0.0` via `qcr_bank`.

**Honest counters (f=10 primary — cognitive reset, no f=100 Pareto here):** Per-trajectory-reset integer sum counters `M_total_f10 = resolve+bind(10tok probe) + retrieval(200+150ms)/QCR k5 / Stagehand + verify(50tok+120ms) + browser_steps+latency ms from Playwright + distill amortized /f + auditor` — no `n*3200`, no `f*6.0`, no jitter. Decomposed `tokens vs browser+latency vs accuracy` Pareto at `f=10`. `ST-WebAgentBench CuP` safety logged non-inferior where BrowserGym exercised. `per_hit` secondary not gating unless Pareto conjoint.

**Novelty levels:** `n=0` (exact repeat), `n=0.25` (50% stale via `304`), optional `n=0.5` sensitivity — L held family-specific constant orthogonal to `n` within strata, trajectory-grouped unit. Family-stratified trajectory-grouped `B=5000` bootstrap + `5000` block-permutation.

---

## 5. Controls (stable identities, EXECUTE must reuse)

**Positive control `PC-SINGLE-NODE-LLM-INHERIT-CORRELATED` (any fail => MEASUREMENT_INVALID):**
- `PC1` Exact-repeat cache: `B-STAGEHAND-CACHE` at `n=0` must hit `1.0` `per_hit ~50` `5/5` per-family via `BrowserGym AX>10` AND `n>=360` stratified.
- `PC2` Orthogonal+correct-family+freshness: `Jaccard 0.0` via `qcr_bank 630` pairs; kernel `5/5 n0 EXECUTABLE confidence>=0.80`; `value_set` disjoint `0/36` verified; `P-SPIDER` correlated probe `fresh ~1.0` vs `stale ~0.5` `accuracy>=0.90 saving>=30% falseAccept<0.05 vs random 0.53 delta>0.10` logged per-step.
- `PC3` Non-vacuous verify+AUROC: forced shuffled probe/registry via same `BrowserGym` must yield `false_accept 0.10-0.60 confidence_std>0.05 AUROC shuffled 0.45-0.60` and `AUROC true>=0.75 precision>=0.80 UNKNOWN>=0.85 ECE<=0.15` empty bins `0`.
- `PC4` Frozen-formula audit: honest `M_total within 1e-6` vs summed counters, `rho_proxy_real` pooled+per-stratum `5000` bootstrap logged, `probeHit` per-step logged.
- `PC5` Health-gate + `BrowserGym` replication: `nginx $request_uri` sticky `n>=360` stratified `HS256 WAL` + `BrowserGym 2000-node 1.63.0 gpt-4o-mini 15-step health_gated If-None-Match` with `AX>10` and `rho_proxy` measurable.

**Null control `NC-SHUFFLE-LLM-INHERIT` (all via same pipeline, no simulated correctness):**
- `NC1` Shuffled probe+registry: trajectory-grouped block-permutation of `parameter_slots` AND swap `TTL` valid→`seeded-42 random 0.53` + swap correct-family keys before resolve; `mock wrong-bound p=0.15` → `UNKNOWN/AUROC` via same `BrowserGym`. Expect `|rho|<0.25 ns |rho_shuffled|<0.20 p>=0.20 per-stratum |rho_length|<0.20 |rho_shuffled_proxy|<0.20 success<=COLD false_accept 0.10-0.60 AUROC 0.45-0.60 M_total ratio~1.0`.
- `NC2` Random entry: independent random family/state keys → `UNKNOWN` expect `false_accept>=0.10 AUROC~0.5`.
- `NC3` Length-proportional constant cost: `cost=L*500+probe miss` regardless of novelty → `|rho|~0 R2<0.15`.
- `NC4` Ablations: `TTL correlated vs random delta>10%`, `TN` single-node `>=0.85` vs hypothetical `per-node 0.667` contrast `n>=360 vs <100`, `rho_proxy shuffled <0.20`. All `B=5000` trajectory-grouped block-permutation; `within-family std>0` required.

---

## 6. Measurement validity gates (MV1-MV12)

See `spec.json:measurement_validity` — 12 gates: `MV1` contamination-free holdout (`101e481d` or Hard258 `d6527566`, `0/36` disjoint `Jaccard 0.0` `8c69804b`, `L 8-14` orthogonal), `MV2` family hold-out zero-overlap orthogonal clean, `MV3` kernel dot-regex durability committed, `MV4` single-node `HS256` sticky `n_non304>=360` stratified `TN>=0.85 If-None-Match/ETag W/body_sha`, `MV5` correlated `TTL/ETag` stratified `saving>=30% accuracy>=0.90 delta>0.10`, `MV6` Docker `BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10` real `gpt-4o-mini 15-step` with `rho_proxy_real>=0.50` per-stratum, `MV7` same model/tools/budget LLM inheritance, `MV8` honest amortized sum counters decomposed at `f=10` with `saving>=25%` vs COLD `browser+latency>=20% accuracy>=0.85` Pareto vs RAG/Stagehand/DSM, `MV9` strong baselines identical splits `TAU0.30` same ranker, `MV10` calibration verification-derived (`false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18 per-class` with `B=5000` `confidence_std>0.05`), `MV11` statistics orthogonal `QCR` `B=5000` trajectory-grouped (`|rho_shuffled|<0.20 rho_proxy>=0.50 per-stratum |rho_length|<0.20`), `MV12` abstention repair (`deterministic single-field re-bind verified_state MEA auditor`, `CuP` safety).

Bijective proxies (`n*3200/f*6.0/jitter`), `CI[1.0,1.0]` degenerate, `within-family std==0`, `confidence_std<=0.05`, empty-bin `ECE` vacuous => `MEASUREMENT_INVALID`. No file-proxy surrogation for `SURVIVES` on browser-validated claim. Hard258 extension when available same gates with `64-char` digest.

---

## 7. Decision rule (frozen, precedence ordered)

Compute per-method `success`, `false_accept`, `UNKNOWN_precision`, `AUROC`, `precision`, `ECE_5bin` per-class, `M_total_f10` decomposed, `M_per_hit` secondary, `Spearman rho_novelty`, `rho_length` pooled+per-stratum, `rho_proxy_real` pooled+per-stratum, `R2`, `per_hit` parity ratios, probe saves via honest counters. `Wilson95%` for rates, trajectory-grouped family-stratified `bootstrap5000` for `rho/R2/ratio/ECE/AUROC/rho_proxy_real/n_non304` CIs, trajectory-grouped `block-permutation5000 p` with `|rho_shuffled|<0.20 p>=0.20` + per-stratum `|rho_length|<0.20` + `rho_proxy>=0.50` per-stratum + `|rho_shuffled_proxy|<0.20` + `n_non304>=360` stratified + `within-std>0 confidence_std>0.05` checks.

- **SURVIVES** (`C-LLM-INHERIT HYPOTHESIS->EXPERIMENTAL`, supersedes `per_hit 1.005>0.85` as economics gate) **iff ALL hold after `PC PASS` non-degenerate stratified with correct frozen controls and provisioned BrowserGym health:**
  - `C1` margin primary: `P-SPIDER` success margin `>=0.12` vs EACH baseline at `f=10` (`Wilson+bootstrap CI` lower excludes `0`, `success>=0.85` at `n0`) on real `BrowserGym gpt-4o-mini` trajectories;
  - `C2` calibration: `false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 bootstrap upper<=0.18` per-class;
  - `C3` verification: `AUROC>=0.75 precision>=0.80` non-degenerate;
  - `C4` economics at `f=10`: `M_total_f10` saving `>=25%` vs `B-COLD` (`bootstrap CI` lower excludes `0`) AND `browser+latency >=20%` vs `COLD` at `f=10` with `accuracy>=0.85` decomposed `tokens vs browser+latency vs accuracy` AND Pareto vs RAG/Stagehand/DSM where honest;
  - `C5` statistics+probe: per-stratum `B=5000` `|rho_shuffled|<0.20 p>=0.20` pooled+per-stratum, `|rho_length|<0.20`, `|rho_shuffled_proxy|<0.20`, `rho_proxy_real>=0.50` pooled+per-stratum (requires BrowserGym tokens), `correlated probe saving>=30% accuracy>=0.90 delta>0.10` vs `seeded-42 random 0.53 TN>=0.85` stratified.

- **FALSIFIES** (controls `PASS` non-degenerate but any `C1-C5` gate fails): `C-LLM-INHERIT` remains `HYPOTHESIS` bounded `REJECTED` for this SUT on health-gated single-node + `BrowserGym 15-step`; f=100 Pareto cannot survive per Director rationale; per_hit `1.005` falsification stands as metric-design artifact.

- **MEASUREMENT_INVALID** (no claim update): `PC` fails OR `n<360` OR `BrowserGym/OPENAI` absent OR fixtures contaminated OR degenerate OR `GHCR` pull denied without disclosure — irrespective of margins, no file-proxy surrogation. Hard258 absent is not invalid if rebuilt `192/36` staged.

Precedence: `MEASUREMENT_INVALID` checked before `FALSIFIES`/`SURVIVES`. All thresholds family-stratified trajectory-grouped `N=192` (rebuilt) or `258/812` if Hard258 extended `TRAIN`-warmed. `f=100` Pareto and distributed `n>=800` NOT tested here.

---

## 8. Baselines & product consequences

**Baselines:** `B-COLD`, `B-INSTRUCTIONS`, `B-RAG-EMBED-TAU030-QCR-K5` (`k=5` primary `k=1` sensitivity), `B-STAGEHAND-CACHE`, `P-SPIDER-LLM-INHERIT` — see `spec.json:baselines`. DSM `$0.002-0.092` compilation contrast for Pareto economics where site overlap `>0`.

**If SURVIVES with `PC PASS` non-degenerate stratified (`value_set` disjoint on ALL families `Jaccard 0.0`, kernel `d926279d` committed durable, `n>=360 TN>=0.85 AX>10 BrowserGym 0.14.3 1280x720 + gpt-4o-mini 15-step`, `probe saving>=30% accuracy>=0.90 delta>0.10`, `rho_proxy>=0.50` per-stratum) and all `C1-C5` hold at `f=10`:** `C-LLM-INHERIT HYPOTHESIS->EXPERIMENTAL` bounded to contamination-free holdout health-gated single-node + `BrowserGym` (single-family honest LLM-inherit gap `>=0.12` vs `cold/instructions/RAG-k5/Stagehand` with calibration/verification `>=25%` saving and Pareto). First valid single-family LLM gap on honest substrate. Justifies preregistering `M_total` gap as `PRODUCT_CORE` economics gate and authorizes `f=100` + distributed `n>=800` next; informs Graph `param-inherit` scaling. No `PRODUCT_CORE` without `DIRECTOR promote_to_product true` and `audit PASS`.

**If FALSIFIED with controls `PASS` non-degenerate (`n>=360 TN>=0.85 AX>10 rho_proxy>=0.50` per-stratum, `n_strat>=180`) but margin `<0.12` or calibration/verification/statistics fail or `saving<25%` at `f=10` or Pareto fails or probe `delta<=0.10`:** `C-LLM-INHERIT` remains `HYPOTHESIS` bounded `REJECTED` for this mechanism on health-gated single-node + `BrowserGym 15-step`; honest gap does NOT beat strong `RAG`/`instructions` even on honest substrate; Director to `PARK` product economics and pivot to alternative architectures (compilation `O(1) $0.002-0.092`, Intel diverse-site grounding, richer SPA sampling). `f=100` `MEASUREMENT_INVALID` history is not falsification. Per_hit `1.005` stands as metric-design artifact.

**If `MEASUREMENT_INVALID`:** No claim update; `handoff` retains contamination-free holdout, re-provision `GHCR/OPENAI_API_KEY/playwright 1.63`, fix `NC1` deterministic coupling on real trajectories, re-verify `n>=360 TN>=0.85` and kernel durability, and re-execute identical frozen REOPEN before distributed authorization.

---

## 9. Validity threats & disclosure

- **Shallow prior vs evidence:** Agent priors (`sunk-cost 17 failures 0.525 ceiling routing 0.0`, `LLM spurious similarity plateau`, measurement traps `X-Worker-Pid n_non304 If-None-Match AX>10`, `false_accept<=0.10 UNKNOWN>=0.85`, `O(MxN)` pruning, `local-optimum` alias trap) are priors explaining stalls, not SPIDER evidence; evidence is Codex `21/40 bound 0.525 [0.352,0.648] routing 0.0 p1.0 0/10 mixed`, `Frontier non-Pareto 36042599040 PASS`, `C-MEAS-VALID 36044045537 n850 0.7619 [0.7048,0.8190] variance 0.0 trivial`, `C-PRODUCT-ECON 13 MEASUREMENT_INVALID`, `Physics PMI 0` after leakage removal.
- **Representation loss:** `DOM hash` encoding `state_id` tautological (`MI 107-198%` `audit V1_v1_tautology`) disclosed; `AX>10` heterogeneity via `getFullAXTree 2000-node` required; single-prefix `field-path` relevance fix limits to `body.* headers.* url`; per-trajectory hard-reset sum counters vs bijective proxies distinguished (`|rho_shuffled|<0.20` honest, not jitter `Gaussian`); `DSM $0.002-0.092` excluded from primary `f=10` gap but included in Pareto.
- **Contamination risk:** `value_set_A intersect B` recomputed on ALL families via `value_set` not `SHA` equality; `qcr_bank TAU0.30` `8c69804b` frozen; `391e8f6c 18/36` contaminated must not be staged; Hard258 `d6527566` when available same proof with `64-char` digest.
- **Substrate leakage:** Shared `URLs` with synchronized `DB` can appear distributed; health gates (`X-Worker-Pid single_worker WAL n_non304>=360 If-None-Match/304 AX>10`) prevent; `per_hit 1.005>0.85` bounded to file-proxy not to `M_total` Pareto; `variance>0` prerequisite for distributed per Director dependencies.
- **Cross-site transfer leakage:** Holdout by `URL/host` + task-family stratification; `DOM hash` tautology and `PMI>0 K=3 under H=0` pipeline validation disclosed; residual-novelty economics falsified retrieval `0.525` ceiling.
- **Cost realism:** End-to-end economics includes `verification/repair/maintenance` amortized at `f=10` (this experiment) decomposed `tokens vs browser+latency vs accuracy` with `rho_proxy_real>=0.50` honesty; `f=100` explicitly NOT claimed before this gate per Director; `distributed n>=800` PARKed until single-node `variance>0` with natural header variation and enabled `HIT 330/330`.

---

## 10. Execution plan (no outcome data inspected)

1. Stage contamination-free holdout (`sha 101e481d` `0/36` disjoint `Jaccard 0.0` `8c69804b` fallback; if `Hard258 d6527566` available stage with `64-char` digest and site overlap `>0`) + `qcr_bank TAU0.30` + `cost_config 50/15/180/10` (provenance hashes `TRAIN`-only) — abort if any family overlaps via `value_set_A intersect B`.
2. Commit kernel dot-regex `d926279d` to `HEAD` durable (`cee979c2`-equivalent) — log `working-tree == HEAD` via `provenance` and `git log`.
3. Provision single-node `HS256` `WAL` at `/tmp/spider-runtime/shared.db` (`gunicorn 23.0.0` single-worker `PyJWT 2.14.0` `nginx 1.24.0 $request_uri` sticky) — run health probe `n_non304>=360` stratified `TN>=0.85 If-None-Match/ETag W/body_sha` `TTL 60s` (`substrate_probe.json` `n_304/n_200` `TN_fresh/TN_sticky` `saving 0.40 delta 0.4067` vs random `0.53`).
4. Provision Docker `BrowserGym 0.14.3` `ghcr.io/servicenow/browsergym:0.14.3` + `playwright 1.63.0` with binaries + `OPENAI_API_KEY` (`gpt-4o-mini 15-step`) — log image digest, `2000-node 1280x720 AX>10`, `rho_proxy_real` measurable; if unavailable => `MEASUREMENT_INVALID` for browser claim (disclosed, no file-proxy surrogation).
5. Execute `5 conditions × 3-5 novelty levels × 192 (or 258) ` trajectories + `NC1-NC4` `5000` permutations via honest per-trajectory-reset sum counters on `BrowserGym` — collect `success`, `false_accept`, `UNKNOWN`, `ECE`, `AUROC`, `M_total_f10` decomposed, `probeHit/etagMatched/ttlValid`, `rho_proxy`, `browser_steps/latency`, `safety CuP`.
6. Compute family-stratified trajectory-grouped `B=5000 bootstrap` + `5000 block-permutation` CIs per MV11 — compare to frozen thresholds without peeking then decide per §7, precedence `MEASUREMENT_INVALID` first.
7. Write `result.json` (required `schema_version, experiment_id, lane, status, outcome, metrics, controls, artifacts, observations, validity_notes, unresolved`) with stable metric/control IDs (`PC-SINGLE-NODE-LLM-INHERIT-CORRELATED` `NC-SHUFFLE-LLM-INHERIT` `MV1-MV12` `C1-C5`), `report.md` bounded by measurements, `provenance.json` (commits, run ids, `Docker` digest, `AX>10`, `n_non304` stratified, `value_set` disjoint hashes, `kernel commit`, `gpt-4o-mini` model id, `OPENAI` key presence redacted).

---

## 11. Estimated cost & information gain

**Cost:** Moderate health-gated single-node stratified + provisioned LLM `BrowserGym`: `192×5×3-5 ≈960` (or `258×5≈1290` for Hard258) trajectories + `NC` `~400` + probe `~200` + calibration `~200` ≈ `1760-2090` trials on `SQLite WAL` sticky `n>=360` plus `TFIDF` offline; `CPU <60min` (`<120min` with `Docker 2000-node`), storage `~2500-3500` rows `branch_traces`; with `Docker+gpt-4o-mini`: `~2880` calls `<$30` (`Hard258 <$40`) (see `spec.json:estimated_cost`).

**Information gain:** Decisive gating per Director `REOPEN` `cognitive_reset` true: first re-execution of single-family honest LLM-inherit on provisioned substrate after `MEASUREMENT_INVALID 36089498872` (GHCR denied, OPENAI absent, kernel undurable, NC1 coupling). Positive `->EXPERIMENTAL` retires `per_hit 1.005` gate and authorizes `f=100`/distributed next with Pareto dominance; negative `PARK`s product economics even on honest substrate before distributed authorization, pivoting to compilation `O(1) $0.002-0.092` / Intel `WebMCP` / richer SPA — both before `n>=800` (see `spec.json:expected_information_gain`). High leverage both directions vs `18th` alias variant `0.525` ceiling.

---

*Preregistration frozen before outcome data; any change after seeing outcomes is exploratory and requires new preregistration. Execution must not inspect `M_total` margins before `freeze.json`. Parent handoff USE disposition: established/rejected/unknown/do_not_assume preserved as above.*
