# EXP-PRODUCT-36095578013 — Preregistration (DESIGN, frozen before EXECUTE)

**Lane:** product — `research/lanes/registry.json: product` (allowed roots `src, tests, sdk, pyproject.toml`)  
**Claim:** `C-PRODUCT-ECON` — “SPIDER saves total cost per successful task after retrieval, verification and maintenance” (`research/claims/registry.json` HYPOTHESIS, next_gate `end-to-end amortized economics on real agents`). Secondary inform: `C-LLM-INHERIT` same-model budget gap (`>=0.12` vs each baseline) and `C-RESIDUAL-NOVELTY` / `C-FRESHNESS` freshness+repair gating at `f=10` only, and Pareto vs `RAG/Stagehand/DSM $0.002-0.092`.  
**Director mandate:** `research/experiments/EXP-PRODUCT-36095578013/request.json: director_mandate` (allocation `REOPEN`, `claim_id C-PRODUCT-ECON`, `cognitive_reset false`, `parent_handoff_disposition USE`, comparative_reasoning vs PIVOT to narrower `C-LLM-INHERIT` alone or duplicate Frontier `f=100` compilation). Strategic question verbatim in `request.json` and `spec.json:question`. Parent handoff `research/experiments/EXP-PRODUCT-36091881382/handoff.json` (sha `a2e412fc58c5692a18987a33d65fddb5316da0e8ba9861ca56d59accf59b6217`, `MEASUREMENT_INVALID`) is continuity evidence only per `research/EXPERIMENT_PACKET.md` §2 and AGENTS.md global direction discipline — retained as established/rejected/unknown/do_not_assume but MUST NOT override Director REOPEN; `USE` means retain dependencies but test the Director's binding question.  
**Mode:** DESIGN ONLY — no outcome-bearing measurements; all thresholds frozen before `freeze.json`.

---

## 1. Research question (Director binding, minimal high-information)

On **health-gated single-node HS256 sticky substrate** (`n_non304>=360, TTL 60s ETag W/body_sha conditional probe stratified TN 1.0`) with **Docker BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10** and **real gpt-4o-mini 15-step Playwright same model/tools/budget** (honest per-trajectory-reset sum counters `resolve+bind+verify+freshness+browser_steps` `5/10/15 tokens k*5`, `|rho_shuffled|<0.20`, `rho_proxy_real>=0.50` per-stratum, per-stratum `|rho_length|<0.20`, 5000 family-stratified bootstrap + 5000 block-permutation), does **SPIDER** (`freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic localized repair + correct-family reconstruction via verified_state MEA auditor, TTL conditional probe`) vs **B-COLD** vs **B-INSTRUCTIONS** vs **B-RAG-EMBED TAU0.30/QCR k5** vs **Stagehand selector-cache** achieve **success margin >=0.12 vs each baseline** with `false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18`, verification `AUROC>=0.75 precision>=0.80`, and **honest amortized M_total saving >=25% vs COLD at f=10** (and Pareto dominance vs RAG/Stagehand/DSM `$0.002-0.092` before distributed `n>=800` or `f=100`) **on contamination-free Hard258 or rebuilt 192/36 orthogonal Jaccard 0.0 disjoint value_set_A intersect B empty holdout with ST-WebAgentBench safety CuP non-inferior**?

This is the smallest discriminating test that can change the promotion decision per Director rationale: Product at `370` canonical experiments remains measurement-gated (single-node `n>=360` now `EXPERIMENTAL` via `EXP-RUNTIME-36089494979` but `C-PRODUCT-ECON` at `13` consecutive `MEASUREMENT_INVALID`, `C-LLM-INHERIT` at `3` consecutive `MEASUREMENT_INVALID`, `per_hit` falsified `1.005>0.85 rho 0.363<0.60` superseded by `M_total` Pareto but not yet gated with honest `M_total` + `BrowserGym` + calibration). If SPIDER fails `>=0.12` or `>=25%` here, `f=100` Pareto cannot survive; if it survives with `CuP` non-inferior and `Pareto` vs `RAG/Stagehand/DSM`, it justifies `C-PRODUCT-ECON -> EXPERIMENTAL` and supersession of `per_hit` gate, informing Graph `param-inherit` scaling and Frontier `O(1)` compilation comparison. Single-node `n>=360` reduces infra risk while preserving BrowserGym realism vs distributed `n>=800` which requires honesty prerequisite.

---

## 2. Hypotheses (falsifiable)

- **H1 (primary, `C-PRODUCT-ECON` REOPEN):** With contamination-free holdout (rebuilt `101e481d` `0/36` or Hard258 `d6527566` when delivered, cross-family Jaccard `0.0` on `630` pairs via `qcr_bank_manifest TAU0.30 sha 8c69804b`, `L 8-14` family-constant orthogonal to `n`) + health-gated single-node HS256 sticky substrate at `/tmp/spider-runtime/shared.db WAL single-worker gunicorn 23.0.0 + nginx 1.24.0 $request_uri` (`n_non304>=360` stratified `180/endpoint`, `TN>=0.85`, `If-None-Match fraction 1.0` errors `0`, `TN_fresh 1.0 TN_sticky 1.0`) + durable kernel dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` committed durable (`d926279d` vs `HEAD 8af66ccf` must be equal) + provisioned Docker BrowserGym `0.14.3` `2000-node` `CDP getFullAXTree` `1280x720` `AX>10` + real `gpt-4o-mini 15-step Playwright` same model/tools/budget with `k*5` `5/10/15` tok accounting, SPIDER achieves at `f=10`: (a) margin `>=0.12` vs EACH baseline (Wilson+bootstrap CI excludes 0, `n0 success>=0.85`), (b) calibration `false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18` per-class, (c) verification `AUROC>=0.75 precision>=0.80` non-degenerate, (d) `M_total_f10` saving `>=25%` vs COLD decomposed `tokens vs browser+latency vs accuracy` with `browser+latency >=20%` `accuracy>=0.85` and Pareto vs RAG/Stagehand/DSM `ratio<=0.85`, (e) correlated probe `accuracy>=0.90 saving>=30% delta>0.10` vs seeded-42 random `0.53` with `TN>=0.85`, (f) `rho_proxy_real>=0.50` pooled+per-stratum and per-stratum `|rho_shuffled|<0.20 p>=0.20 |rho_length|<0.20 |rho_shuffled_proxy|<0.20`, (g) `ST-WebAgentBench CuP` safety non-inferior `delta >= -0.02`.

- **H0 (null):** Margins, calibration, verification, saving, Pareto or safety fail with controls PASS non-degenerate, or substrate/BrowserGym health fails rendering `MEASUREMENT_INVALID` (not falsification). Prior `per_hit 1.005>0.85` bounded rejection stands unless this `M_total` Pareto with `rho+AUROC+CuP` conjoint supersedes per Director supersession gate.

Prior plausibility: Scout correctly diagnosed honesty-gate tunnel (per-trajectory sum counters `k*5`, trajectory-grouped 5000 bootstrap+permutation, If-None-Match/ETag `W/body_sha`, verified_state `MEA`), `0.525` alias ceiling with `0/10` mixed, non-Pareto residual-novelty, physics leakage `92-98%` `target_href==url`; Director adopted Scout sequencing but constrained Graph distributed freshness as premature and PARKed distributed `n>=800 f=100` until single-node stable-header variance>0. Agent priors used (long-horizon compounding `98%->55%` at 10 steps requiring `UNKNOWN` abstention `precision>=0.85 FA<=0.10`, `P(A|history)` vs `P(S'|S,A)` `Gamma-ratio |perm-analytic|<0.03`, retrieval diversity plateau `0.525 alias` `routing 0.0 p=1.0`, residual-novelty honest counters `|rho_shuffled|<0.20`, Frontier basin escape `TreeWalker 99% + DAG <0.1ms 0 tokens`) are priors distinct from SPIDER evidence per `request.json:director_mandate.agent_priors_used`.

---

## 3. Carry-forward from parent (preserved distinctions, USE disposition)

Per `parent_handoff` `a2e412fc...` (`EXP-PRODUCT-36091881382` `MEASUREMENT_INVALID` `2026-09-25`):

**Established (retain as dependencies, re-verify this packet):**
- Frozen inputs byte-identical verified (request `8ef872700c...` spec `afec9c54...` prereg `1e67c0f9...` freeze `2026-09-25T03:52:38Z`) with `MEASUREMENT_INVALID` correctly declared, no bijective `n*3200/f*6.0/jitter` proxy, family-stratified trajectory-grouped `B=5000` bootstrap+block-permutation machinery intact (audit exact match, `recomputed_metrics` exact).
- Contamination-free holdout RETAINED at MV2: rebuilt `webarena_verified_v2_tasks_192_36_rebuilt.json sha 101e481ddb610df9598b0e3e5650e8c163ec7cbdc4679c5efc1e31104b3074c5` (`0/36` pool+usage disjoint, cross-family bigram Jaccard `0.0` on `630` pairs via `qcr_bank_manifest sha 8c69804b TAU0.30`, `L 8-14`) — supersedes `391e8f6c` (`18/36` contaminated). Verified via `value_set_A intersect B` not SHA, audit recomputed via value_set.
- Single-node HS256 sticky substrate health-gated PASS at `n_non304 400 200/200 >=360/180` (`WAL pid single-worker 58721 gunicorn 23.0.0 PyJWT 2.14.0 nginx 1.24.0 $request_uri sticky`) with `n_304 351 TN 1.0 probe saving 0.40 delta 0.4067 >0.10` vs seeded-42 random `0.53` — re-verify per MV4.
- Correlated `TTL 60s ETag W/body_sha` probe discriminates (`hit 1.0` at `n==0`, `accuracy 1.0 false_accept 0.0` at `n0.25`, saving `0.40` vs `0.53` delta `0.4067`).
- Kernel dot-regex functionally PASS `5/5` (`src/spider/kernel.py` working-tree `d926279d` pattern `\$\{[A-Za-z_][A-Za-z0-9_\.]*\}` confidence `0.85`) but NOT committed durable (`HEAD 8af66ccf` vs working-tree at execute, `provenance kernel_durable false`) — must be committed durable before DIRECTOR promotion (now `HEAD 00428213` post-commit requires fresh re-execute).
- PC3 MockEnv calibration non-vacuous PASS `AUROC 0.8714` vs shuffled `0.4681` precision `0.9491` ECE `0.107` `confidence_std 0.4543` — validates pipeline on MockEnv not transfer to BrowserGym.
- Honest economics ceiling diagnostic (diagnostic not claim): `SPIDER f10 1981 vs COLD 5992 saving 0.669 CI[0.652,0.687]` but ratio `1.506 vs RAG CI[1.479,1.531] >0.85` FAIL diagnostic not falsification (audit diagnostic, `M_total Pareto` null with reasons).
- QCR orthogonality `0.0` and toolchain pins `gunicorn 23.0.0 PyJWT 2.14.0 Flask 3.1.3 playwright 1.63.0 cost_config 50/15/180/10` retained.

**Rejected (bounded, do not generalize beyond):**
- Canonical `192/36 sha 391e8f6c` contaminated `18/36` — must not reuse.
- NC1 shuffled null deterministic file-proxy honest counters (`rho_shuffled -0.136 p 0.0724` FAIL `p>=0.20`, `rho_length -0.287` per-stratum all `>0.20`) — deterministic coupling from `reused=max(0,L-n_novel*2)` disclosed; must break coupling on real trajectories.
- No rejection of `C-PRODUCT-ECON` `M_total` Pareto on honest substrate — `MEASUREMENT_INVALID` bounded to infrastructure (GHCR denied, `OPENAI_API_KEY` absent, `playwright` MISSING, kernel not durable) not scientific falsification; prior `per_hit 1.005>0.85` bounded REJECTED for `per_hit` metric-design on file-proxy only remains, not for `M_total f10` Pareto (ceiling `0.669` meets but ratio `1.506` fails are diagnostic not falsification).
- No rejection of `RAG-EMBED TAU0.30/QCR k5` or `Stagehand cache` on honest substrate — all unmeasured beyond file-proxy diagnostic.

**Unknown (remain unknown until EXECUTE on provisioned substrate):** GHCR `BrowserGym 0.14.3` authorization + `playwright 1.63` binaries + `OPENAI_API_KEY` for `gpt-4o-mini 15-step` with `AX>10` heterogeneity and `rho_proxy_real>=0.50` + `k*5` `5/10/15` tokens; kernel commit durability; NC1 coupling break on real trajectories (`|rho_shuffled|<0.20 p>=0.20 |rho_length|<0.20`); honest `M_total` Pareto vs RAG/Stagehand/DSM at `f=10` with `k*5` and `CuP` non-inferior; per_hit supersession conjoint; Hard258 heterogeneous census with `site overlap >0`.

**do_not_assume (explicitly unsafe):** `MEASUREMENT_INVALID` is infrastructure failure not falsification; probe saving `0.40` or ceiling `0.669` does NOT imply Pareto dominance (ratio `1.506` fails diagnostic); working-tree kernel not durable; Jaccard `0.0` ≠ value_set disjointness; `MockEnv AUROC 0.871` does not transfer to `gpt-4o-mini`; NC1 band PASS ≠ null valid (`p 0.0724` FAIL); `B-STAGEHAND-PC1 1.0` file-proxy ≠ Docker `2000-node AX>10`; honest counter ratio `>0.85` vs RAG on synthetic does not prove RAG dominates generally; `per_hit 0.135/0.293` not proof supersession; do not claim `M_total 0.669` saving implies `PARK` or promotion without `AUROC>=0.75` and `CuP`.

Director **REOPEN USE** retains these as dependencies/evidential continuity but re-tests the identical frozen single-family honest econ margins on health-gated single-node + real BrowserGym `2000-node` `gpt-4o-mini` before distributed `n>=800` or `f=100` Pareto per `dependencies` (runtime sticky `n_non304>=360`, graph freshness `Jaccard 0.85`, intel Hard258 `374ef8f625be` / rebuilt `192/36` holdout) with `k*5` and `CuP` added per mandate.

---

## 4. Experimental design (smallest high-information, not pre-2.0 repeat)

**Population & holdout:** Contamination-free holdout as gating holdout — rebuilt `192/36` (`sha 101e481d` realized, fallback `c2763ebae9`, requested prefix `374ef8f6`) `0/36` pool+usage disjoint `L 8-14` family-constant orthogonal to `n` via `qcr_bank_manifest sha 8c69804b TAU0.30` **OR** Hard258/WebArena-Verified `812` census `hash d6527566` when Intel delivers with same disjointness proof (`64-char` digest, value_set `0/N` disjoint, Jaccard `0.0`). Audit must recompute `value_set_A intersect B` on ALL families via value_set not SHA. `TRAIN`-only induction. If Hard258 added, log `64-char` digest and site overlap `>0` for DSM non-degenerate extension; gating holdout remains whichever staged but rebuilt `192/36` is fallback gating. `ST-WebAgentBench` holdout for `CuP` safety uses disjoint `CuP` tasks where `SPIDER` safety measured.

**Substrate (MUST be health-gated for SURVIVES):**
- Single-node `HS256` sticky at `/tmp/spider-runtime/shared.db` `WAL` single `gunicorn 23.0.0` single-worker `HS256 PyJWT 2.14.0` + `nginx 1.24.0 $request_uri` consistent-hash sticky, `If-None-Match`/`ETag W/body_sha` conditional `200` vs `304`, `n_non304>=360` stratified (`180/endpoint` where two endpoints, `TN>=0.85`, `If-None-Match fraction 1.0` errors `0`) — re-measured this packet, logged `shared.db WAL worker=1 JWT alg TN n_non304 stratified sticky hash ETag n_304/n_200 distinct_worker_pids single_worker` (`substrate_probe.json`).
- Correlated `TTL 60s max-age ETag W/body_sha` probe `10tok+30ms` fresh at `n0 ~1.0` vs `~50%` stale at `n=0.25` vs `seeded-42 random 0.53` decoupled NC, per-step `probeHit/etagMatched/ttlValid` logged, `probe_is_correlated true` for SUT, saving `>=30%` accuracy `>=0.90` `falseAccept<0.05` `delta>0.10`.
- Kernel dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` committed durable (`cee979c2`-equivalent `d926279d` `HEAD == working-tree`) — `provenance` must show `working-tree == HEAD` committed, `5/5 n0 EXECUTABLE confidence>=0.80`.

**Browser + LLM (MUST for SURVIVES, else MEASUREMENT_INVALID):**
- `Docker` `BrowserGym 0.14.3` `ghcr.io/servicenow/browsergym:0.14.3` + `playwright 1.63.0` with binaries + `OPENAI_API_KEY` for `gpt-4o-mini` `15-step` `Playwright` `1280x720` `CDP getFullAXTree` `2000-node` `AX>10` heterogeneous — logged `Docker` availability, image digest, `BrowserGym` version, node count, viewport, real `tokens` per step (`k*5` `5/10/15`), `browser_calls`, `latency ms`, `AX nodes>10`. Proxy vs real `Spearman rho_proxy_real>=0.50` pooled+per-stratum required plus per-stratum `|rho_length|<0.20 |rho_shuffled_proxy|<0.20`.
- Same `model/tools/budget` across ALL conditions (`SPIDER/COLD/INSTRUCTIONS/RAG/STAGEHAND`) — logged `model id`, `steps`, `tools`, `budget`, `AX nodes` per trajectory; `ST-WebAgentBench CuP` via same `BrowserGym` pipeline. Mismatch => `MEASUREMENT_INVALID` for econ sub-claim.

**Conditions (5, same holdout splits, same L, same honest counters k*5, same BrowserGym/budget):**
1. `B-COLD` — no memory.
2. `B-INSTRUCTIONS` — `B-COLD` + site-specific NL instructions (same token budget as probe overhead).
3. `B-RAG-EMBED-TAU030-QCR-K5` — QCR frozen-bank `TAU0.30` top-`k=5` (k=1 sensitivity) `200tok+150ms` with verify fallback.
4. `B-STAGEHAND-CACHE` — `DOM-hash` cache without `TTL` correlation (2x `~30%` claim), `hit 1.0` at `n0` else `0`; DSM `$0.002-0.092` contrast for Pareto where `site overlap >0`.
5. `P-SPIDER-ECON` — freshness-gated `0.95/0.85 Jaccard 0.85` + deterministic repair + correct-family + `TTL` probe + `MEA auditor` `softmax temp0.15+jitter`, `k*5` accounting.

All TRAIN-only induction, `value_set_A intersect B empty` strictly on all families, cross-family `Jaccard max 0.0` via `qcr_bank`.

**Honest counters (f=10 primary — single-node Pareto gate):** Per-trajectory-reset integer sum counters `M_total_f10 = resolve+bind(10tok probe k*5) + retrieval(200+150ms)/QCR k5 / Stagehand + verify(50tok+120ms) + browser_steps+latency ms from Playwright + distill amortized /f + auditor` — no `n*3200`, no `f*6.0`, no jitter beyond `k*5` `5/10/15` per step. Decomposed `tokens vs browser+latency vs accuracy` Pareto at `f=10` with `k*5`. `per_hit` secondary not gating unless Pareto conjoint. `ST-WebAgentBench CuP` safety logged non-inferior where BrowserGym exercised.

**Novelty levels:** `n=0` (exact repeat), `n=0.25` (50% stale via `304`), optional `n=0.5` sensitivity — L held family-specific constant orthogonal to `n` within strata, trajectory-grouped unit. Family-stratified trajectory-grouped `B=5000` bootstrap + `5000` block-permutation. `CuP` measured on `ST-WebAgentBench` safety split where `BrowserGym` exercised.

---

## 5. Controls (stable identities, EXECUTE must reuse)

**Positive control `PC-SINGLE-NODE-ECON-CORRELATED` (any fail => MEASUREMENT_INVALID):**
- `PC1` Exact-repeat cache: `B-STAGEHAND-CACHE` at `n=0` must hit `1.0` `per_hit ~50` `5/5` per-family via `BrowserGym AX>10` AND `n>=360` stratified.
- `PC2` Orthogonal+correct-family+freshness: `Jaccard 0.0` via `qcr_bank 630` pairs; kernel `5/5 n0 EXECUTABLE confidence>=0.80`; `value_set` disjoint `0/36` verified; `P-SPIDER` correlated probe `fresh ~1.0` vs `stale ~0.5` `accuracy>=0.90 saving>=30% falseAccept<0.05 vs random 0.53 delta>0.10` logged per-step `k*5`.
- `PC3` Non-vacuous verify+AUROC: forced shuffled probe/registry via same `BrowserGym` must yield `false_accept 0.10-0.60 confidence_std>0.05 AUROC shuffled 0.45-0.60` and `AUROC true>=0.75 precision>=0.80 UNKNOWN>=0.85 ECE<=0.15` empty bins `0`.
- `PC4` Frozen-formula audit: honest `M_total within 1e-6` vs summed counters with `k*5`, `rho_proxy_real` pooled+per-stratum `5000` bootstrap logged, `probeHit` per-step logged.
- `PC5` Health-gate + `BrowserGym` replication: `nginx $request_uri` sticky `n>=360` stratified `HS256 WAL` + `BrowserGym 2000-node 1.63.0 gpt-4o-mini 15-step health_gated If-None-Match` with `AX>10` and `rho_proxy` measurable and `CuP` safety measurable.

**Null control `NC-SHUFFLE-ECON` (all via same pipeline, no simulated correctness):**
- `NC1` Shuffled probe+registry: trajectory-grouped block-permutation of `parameter_slots` AND swap `TTL` valid→`seeded-42 random 0.53` + swap correct-family keys before resolve; `mock wrong-bound p=0.15` → `UNKNOWN/AUROC` via same `BrowserGym`. Expect `|rho|<0.25 ns |rho_shuffled|<0.20 p>=0.20 per-stratum |rho_length|<0.20 |rho_shuffled_proxy|<0.20 success<=COLD false_accept 0.10-0.60 AUROC 0.45-0.60 M_total ratio~1.0`.
- `NC2` Random entry: independent random family/state keys → `UNKNOWN` expect `false_accept>=0.10 AUROC~0.5`.
- `NC3` Length-proportional constant cost: `cost=L*500+probe miss` regardless of novelty → `|rho|~0 R2<0.15`.
- `NC4` Ablations: `TTL correlated vs random delta>10%`, `TN` single-node `>=0.85` vs hypothetical `per-node 0.667` contrast `n>=360 vs <100`, `rho_proxy shuffled <0.20`, `CuP` shuffled vs real. All `B=5000` trajectory-grouped block-permutation; `within-family std>0` required.

---

## 6. Measurement validity gates (MV1-MV12)

See `spec.json:measurement_validity` — 12 gates: `MV1` contamination-free holdout (`101e481d` or Hard258 `d6527566`, `0/36` disjoint `Jaccard 0.0` `8c69804b`, `L 8-14` orthogonal), `MV2` family hold-out zero-overlap orthogonal clean, `MV3` kernel dot-regex durability committed, `MV4` single-node `HS256` sticky `n_non304>=360` stratified `TN>=0.85 If-None-Match/ETag W/body_sha` with `k*5`, `MV5` correlated `TTL/ETag` stratified `saving>=30% accuracy>=0.90 delta>0.10`, `MV6` Docker `BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10` real `gpt-4o-mini 15-step` with `k*5` `rho_proxy_real>=0.50` per-stratum, `MV7` same model/tools/budget + `CuP` safety, `MV8` honest amortized sum counters `k*5` decomposed at `f=10` with `saving>=25%` vs COLD `browser+latency>=20% accuracy>=0.85` Pareto vs RAG/Stagehand/DSM + `CuP` non-inferior, `MV9` strong baselines identical splits `TAU0.30` same ranker, `MV10` calibration verification-derived (`false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18` per-class with `B=5000` `confidence_std>0.05`), `MV11` statistics orthogonal `QCR` `B=5000` trajectory-grouped (`|rho_shuffled|<0.20 rho_proxy>=0.50 per-stratum |rho_length|<0.20`), `MV12` abstention repair + `CuP` safety (`deterministic single-field re-bind verified_state MEA auditor`, `CuP delta >= -0.02`).

Bijective proxies (`n*3200/f*6.0/jitter` beyond `k*5`), `CI[1.0,1.0]` degenerate, `within-family std==0`, `confidence_std<=0.05`, empty-bin `ECE` vacuous => `MEASUREMENT_INVALID`. No file-proxy surrogation for `SURVIVES` on browser-validated claim. Hard258 extension when available same gates with `64-char` digest.

---

## 7. Decision rule (frozen, precedence ordered)

Compute per-method `success`, `false_accept`, `UNKNOWN_precision`, `AUROC`, `precision`, `ECE_5bin` per-class, `M_total_f10` decomposed `k*5`, `M_per_hit` secondary, `Spearman rho_novelty`, `rho_length` pooled+per-stratum, `rho_proxy_real` pooled+per-stratum, `R2`, `per_hit` parity ratios, probe saves via honest counters `k*5`, `CuP` safety. `Wilson95%` for rates, trajectory-grouped family-stratified `bootstrap5000` for `rho/R2/ratio/ECE/AUROC/rho_proxy_real/n_non304/CuP` CIs, trajectory-grouped `block-permutation5000 p` with `|rho_shuffled|<0.20 p>=0.20` + per-stratum `|rho_length|<0.20` + `rho_proxy>=0.50` per-stratum + `|rho_shuffled_proxy|<0.20` + `n_non304>=360` stratified + `within-std>0 confidence_std>0.05` checks.

- **SURVIVES** (`C-PRODUCT-ECON HYPOTHESIS->EXPERIMENTAL`, supersedes `per_hit 1.005>0.85` as economics gate) **iff ALL hold after `PC PASS` non-degenerate stratified with correct frozen controls and provisioned BrowserGym health and `k*5`:**
  - `C1` margin primary: `P-SPIDER` success margin `>=0.12` vs EACH baseline at `f=10` (`Wilson+bootstrap CI` lower excludes `0`, `success>=0.85` at `n0`) on real `BrowserGym gpt-4o-mini` trajectories;
  - `C2` calibration: `false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 bootstrap upper<=0.18` per-class;
  - `C3` verification: `AUROC>=0.75 precision>=0.80` non-degenerate;
  - `C4` economics at `f=10`: `M_total_f10` saving `>=25%` vs `B-COLD` (`bootstrap CI` lower excludes `0`) AND `browser+latency >=20%` vs `COLD` at `f=10` with `accuracy>=0.85` decomposed `tokens vs browser+latency vs accuracy` AND Pareto vs RAG/Stagehand/DSM where honest (`ratio <=0.85` bootstrap upper `<0.85`);
  - `C5` statistics+probe+safety: per-stratum `B=5000` `|rho_shuffled|<0.20 p>=0.20` pooled+per-stratum, `|rho_length|<0.20`, `|rho_shuffled_proxy|<0.20`, `rho_proxy_real>=0.50` pooled+per-stratum (requires BrowserGym tokens `k*5`), `correlated probe saving>=30% accuracy>=0.90 delta>0.10` vs `seeded-42 random 0.53 TN>=0.85` stratified, and `CuP` safety non-inferior `delta >= -0.02`.

- **FALSIFIES** (controls `PASS` non-degenerate but any `C1-C5` gate fails): `C-PRODUCT-ECON` remains `HYPOTHESIS` bounded `REJECTED` for this SUT on health-gated single-node + `BrowserGym 15-step`; f=100 Pareto cannot survive per Director rationale; `per_hit 1.005` falsification stands as metric-design artifact not superseded.

- **MEASUREMENT_INVALID** (no claim update): `PC` fails OR `n<360` OR `BrowserGym/OPENAI` absent OR fixtures contaminated OR degenerate OR `GHCR` pull denied without disclosure — irrespective of margins, no file-proxy surrogation. Hard258 absent is not invalid if rebuilt `192/36` staged.

Precedence: `MEASUREMENT_INVALID` checked before `FALSIFIES`/`SURVIVES`. All thresholds family-stratified trajectory-grouped `N=192` (rebuilt) or `258/812` if Hard258 extended `TRAIN`-warmed with `k*5`. `f=100` Pareto and distributed `n>=800` NOT tested here per Director gating.

---

## 8. Baselines & product consequences

**Baselines:** `B-COLD`, `B-INSTRUCTIONS`, `B-RAG-EMBED-TAU030-QCR-K5` (`k=5` primary `k=1` sensitivity), `B-STAGEHAND-CACHE`, `P-SPIDER-ECON` — see `spec.json:baselines`. DSM `$0.002-0.092` compilation contrast for Pareto economics where `site overlap >0` else disclosed degenerate. All with `k*5` `5/10/15` tok per step.

**If SURVIVES with `PC PASS` non-degenerate stratified (`value_set` disjoint on ALL families `Jaccard 0.0`, kernel `d926279d` committed durable, `n>=360 TN>=0.85 AX>10 BrowserGym 0.14.3 1280x720 + gpt-4o-mini 15-step k*5`, `probe saving>=30% accuracy>=0.90 delta>0.10`, `rho_proxy>=0.50` per-stratum, `CuP` non-inferior) and all `C1-C5` hold at `f=10`:** `C-PRODUCT-ECON HYPOTHESIS->EXPERIMENTAL` bounded to contamination-free holdout health-gated single-node + `BrowserGym` (single-family honest econ gap `>=0.12` vs `cold/instructions/RAG-k5/Stagehand` with calibration/verification `>=25%` saving and Pareto `k*5` with `CuP`). First valid single-family econ gap on honest substrate with `BrowserGym` `k*5` and `CuP`. Justifies preregistering `M_total` gap as `PRODUCT_CORE` economics gate (superseding `per_hit 1.005`) and authorizes `f=100` + distributed `n>=800` next; informs Graph `param-inherit` scaling. No `PRODUCT_CORE` without `DIRECTOR promote_to_product true` and `audit PASS`.

**If FALSIFIED with controls `PASS` non-degenerate (`n>=360 TN>=0.85 AX>10 rho_proxy>=0.50` per-stratum, `n_strat>=180` `k*5` `CuP` measured) but margin `<0.12` or calibration/verification/statistics fail or `saving<25%` at `f=10` or Pareto fails or `CuP` inferior or probe `delta<=0.10`:** `C-PRODUCT-ECON` remains `HYPOTHESIS` bounded `REJECTED` for this mechanism on health-gated single-node + `BrowserGym 15-step k*5`; honest gap does NOT beat strong `RAG`/`instructions` even on honest substrate; Director to `PARK` product economics and pivot to alternative architectures (compilation `O(1) $0.002-0.092`, Intel diverse-site grounding, richer SPA sampling). `f=100` `MEASUREMENT_INVALID` history is not falsification. Per_hit `1.005` stands as metric-design artifact.

**If `MEASUREMENT_INVALID`:** No claim update; `handoff` retains contamination-free holdout, re-provision `GHCR/OPENAI_API_KEY/playwright 1.63` with `k*5`, fix `NC1` deterministic coupling on real trajectories, re-verify `n>=360 TN>=0.85` and kernel durability, and re-execute identical frozen REOPEN before distributed authorization.

---

## 9. Validity threats & disclosure

- **Shallow prior vs evidence:** Agent priors (long-horizon compounding `98%->55%`, `P(A|history)` vs `P(S'|S,A)` `Gamma-ratio |perm-analytic|<0.03`, retrieval diversity plateau `0.525 alias` `routing 0.0 p=1.0`, honest counters `|rho_shuffled|<0.20 k*5`, Frontier basin escape `99% + DAG <0.1ms`) are priors explaining stalls, not SPIDER evidence; evidence is Codex `21/40 bound 0.525 [0.352,0.648] routing 0.0 p1.0 0/10 mixed`, `Frontier non-Pareto 36042599040 PASS`, `C-PRODUCT-ECON 13 MEASUREMENT_INVALID` `per_hit 1.005>0.85`, `C-MEAS-VALID 36089494979 PASS n>=360 TN 1.0`, `C-LLM-INHERIT 3 MEASUREMENT_INVALID`.
- **Representation loss:** `DOM hash` encoding `state_id` tautological (`MI 107-198%` `audit V1_v1_tautology`) disclosed; `AX>10` heterogeneity via `getFullAXTree 2000-node` required; single-prefix `field-path` relevance fix limits to `body.* headers.* url`; per-trajectory hard-reset sum counters with `k*5` `5/10/15` tok per step vs bijective proxies distinguished (`|rho_shuffled|<0.20` honest); `DSM $0.002-0.092` excluded from primary `f=10` gap but included in Pareto where `site overlap >0`; `CuP` safety measured on `ST-WebAgentBench` disjoint from econ holdout.
- **Contamination risk:** `value_set_A intersect B` recomputed on ALL families via `value_set` not `SHA` equality; `qcr_bank TAU0.30` `8c69804b` frozen; `391e8f6c 18/36` contaminated must not be staged; Hard258 `d6527566` when available same proof with `64-char` digest + `Jaccard 0.0`.
- **Substrate leakage:** Shared `URLs` with synchronized `DB` can appear distributed; health gates (`X-Worker-Pid single_worker WAL n_non304>=360 If-None-Match/304 AX>10`) prevent; `per_hit 1.005>0.85` bounded to file-proxy not to `M_total` Pareto; `variance>0` prerequisite for distributed per Director dependencies; `k*5` verification via per-step logs.
- **Cross-site transfer leakage:** Holdout by `URL/host` + task-family stratification; `DOM hash` tautology disclosed; residual-novelty economics falsified retrieval `0.525` ceiling not repeated; `CuP` non-inferior ensures safety not sacrificed for econ.
- **Cost realism:** End-to-end economics includes `verification/repair/maintenance` amortized at `f=10` (this experiment) decomposed `tokens (k*5) vs browser+latency vs accuracy` with `rho_proxy_real>=0.50` honesty + `CuP`; `f=100` explicitly NOT claimed before this gate per Director; `distributed n>=800` PARKed until single-node `variance>0` with natural header variation and enabled `HIT 330/330`.

---

## 10. Execution plan (no outcome data inspected)

1. Stage contamination-free holdout (`sha 101e481d` `0/36` disjoint `Jaccard 0.0` `8c69804b` fallback; if `Hard258 d6527566` available stage with `64-char` digest and site overlap `>0`) + `qcr_bank TAU0.30` + `cost_config 50/15/180/10` (provenance hashes `TRAIN`-only) — abort if any family overlaps via `value_set_A intersect B`; stage `ST-WebAgentBench` safety split disjoint.
2. Commit kernel dot-regex `d926279d` to `HEAD` durable (`cee979c2`-equivalent) — log `working-tree == HEAD` via `provenance` and `git log`.
3. Provision single-node `HS256` `WAL` at `/tmp/spider-runtime/shared.db` (`gunicorn 23.0.0` single-worker `PyJWT 2.14.0` `nginx 1.24.0 $request_uri` sticky) — run health probe `n_non304>=360` stratified `TN>=0.85 If-None-Match/ETag W/body_sha` `TTL 60s` (`substrate_probe.json` `n_304/n_200` `TN_fresh/TN_sticky` `saving 0.40 delta 0.4067` vs random `0.53` `k*5`).
4. Provision Docker `BrowserGym 0.14.3` `ghcr.io/servicenow/browsergym:0.14.3` + `playwright 1.63.0` with binaries + `OPENAI_API_KEY` (`gpt-4o-mini 15-step` `k*5`) — log image digest, `2000-node 1280x720 AX>10`, `rho_proxy_real` measurable and `CuP` measurable; if unavailable => `MEASUREMENT_INVALID` for browser claim (disclosed, no file-proxy surrogation).
5. Execute `5 conditions × 3-5 novelty levels × 192 (or 258) ` trajectories + `NC1-NC4` `5000` permutations + `CuP` safety via honest per-trajectory-reset sum counters `k*5` on `BrowserGym` — collect `success`, `false_accept`, `UNKNOWN`, `ECE`, `AUROC`, `M_total_f10` decomposed `k*5`, `probeHit/etagMatched/ttlValid`, `rho_proxy`, `browser_steps/latency`, `safety CuP`.
6. Compute family-stratified trajectory-grouped `B=5000 bootstrap` + `5000 block-permutation` CIs per MV11 — compare to frozen thresholds without peeking then decide per §7, precedence `MEASUREMENT_INVALID` first.
7. Write `result.json` (required `schema_version, experiment_id, lane, status, outcome, metrics, controls, artifacts, observations, validity_notes, unresolved`) with stable metric/control IDs (`PC-SINGLE-NODE-ECON-CORRELATED` `NC-SHUFFLE-ECON` `MV1-MV12` `C1-C5` `CuP`), `report.md` bounded by measurements, `provenance.json` (commits, run ids, `Docker` digest, `AX>10`, `n_non304` stratified, `value_set` disjoint hashes, `kernel commit`, `gpt-4o-mini` model id, `k*5`, `CuP`, `OPENAI` key presence redacted).

---

## 11. Estimated cost & information gain

**Cost:** Moderate health-gated single-node stratified + provisioned LLM `BrowserGym` + `CuP`: `192×5×3-5 ≈960` (or `258×5≈1290` for Hard258) trajectories + `NC` `~400` + probe `~200` + calibration `~200` + `CuP` `~100` ≈ `1860-2190` trials on `SQLite WAL` sticky `n>=360` plus `TFIDF` offline; `CPU <60min` (`<120min` with `Docker 2000-node`), storage `~2500-3500` rows `branch_traces`; with `Docker+gpt-4o-mini` `k*5`: `~2880` calls `<$30` (`Hard258 <$40`) + `CuP` overhead (see `spec.json:estimated_cost`).

**Information gain:** Decisive gating per Director `REOPEN` `cognitive_reset false` on `C-PRODUCT-ECON`: first re-execution of single-family honest econ on provisioned substrate after `MEASUREMENT_INVALID 36091881382` (GHCR denied, OPENAI absent, kernel undurable, NC1 coupling) with `k*5` and `CuP` added per mandate. Positive `->EXPERIMENTAL` retires `per_hit 1.005` gate (supersession via honest `M_total` Pareto `tokens vs browser+latency vs accuracy` `k*5` with `CuP`) and authorizes `f=100`/distributed next with Pareto dominance vs `RAG/Stagehand/DSM`; negative `PARK`s product economics even on honest substrate before distributed authorization, pivoting to compilation `O(1) $0.002-0.092` / Intel `WebMCP` / richer SPA — both before `n>=800` (see `spec.json:expected_information_gain`). High leverage both directions vs `18th` alias variant `0.525` ceiling with `CuP` gating.

---

*Preregistration frozen before outcome data; any change after seeing outcomes is exploratory and requires new preregistration. Execution must not inspect `M_total` margins or `CuP` before `freeze.json`. Parent handoff USE disposition: established/rejected/unknown/do_not_assume preserved as above. Director mandate `C-PRODUCT-ECON` REOPEN with `k*5` and `CuP` non-inferior is binding.*
