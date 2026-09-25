# EXP-PRODUCT-36089498872 — Preregistration (DESIGN, frozen before EXECUTE)

**Lane:** product — `research/lanes/registry.json: product` (allowed roots `src, tests, sdk, pyproject.toml`)  
**Claim:** `C-LLM-INHERIT` — “A real LLM agent benefits from SPIDER beyond strong memory/instruction baselines” (`research/claims/registry.json` HYPOTHESIS, next_gate `same model/tools/budget; cold vs instructions vs retrieval vs SPIDER`). Secondary inform: `C-PRODUCT-ECON` economics gate at f=10 only.  
**Director mandate:** `research/experiments/EXP-PRODUCT-36089498872/request.json: director_mandate` (allocation `PIVOT`, `claim_id C-LLM-INHERIT`, `cognitive_reset true`, `parent_handoff_disposition SUPERSEDE`, comparative_reasoning vs CONTINUE n>=800 Pareto and vs PARK). Strategic question verbatim in `request.json` and `spec.json:question`. Parent handoff `research/experiments/EXP-PRODUCT-36046064994/handoff.json` is continuity evidence only per `research/EXPERIMENT_PACKET.md` §2 and AGENTS.md global direction discipline — retained as established/rejected/unknown/do_not_assume but MUST NOT override Director PIVOT.  
**Mode:** DESIGN ONLY — no outcome-bearing measurements; all thresholds frozen before `freeze.json`.

---

## 1. Research question (Director binding, minimal high-information)

On **health-gated single-node HS256 sticky substrate** (`n_non304>=360, TTL 60s ETag W/body_sha conditional probe`) with **Docker BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10** and **real gpt-4o-mini 15-step Playwright same model/tools/budget** (honest per-trajectory-reset sum counters `resolve+bind+verify+freshness+browser_steps`, `|rho_shuffled|<0.20`, `rho_proxy_real>=0.50`, per-stratum `|rho_length|<0.20`, 5000 family-stratified bootstrap + 5000 block-permutation), does **SPIDER** (`freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic repair, correct-family reconstruction`) vs **B-COLD** vs **B-INSTRUCTIONS** vs **B-RAG-EMBED TAU0.30/QCR k5** vs **Stagehand cache** achieve **success margin >=0.12 vs each baseline** with `false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18`, verification `AUROC>=0.75 precision>=0.80`, and **honest amortized saving >=25% vs COLD at f=10** before any distributed `n>=800` or `f=100` Pareto claim?

This is the smallest discriminating test that can change the promotion decision per Director rationale: 14/19 recent `C-PRODUCT-ECON` `MEASUREMENT_INVALID` on `M_total_f10/f100` Pareto vs RAG/Stagehand before demonstrating the prerequisite single-family LLM gap. If SPIDER fails `>=0.12` here, `f=100` Pareto cannot survive; if it survives, it justifies larger amortized economics.

---

## 2. Hypotheses (falsifiable)

- **H1 (primary, `C-LLM-INHERIT`):** With contamination-free holdout + health-gated substrate + durable kernel + provisioned BrowserGym + same budget, SPIDER achieves at `f=10`: (a) margin `>=0.12` vs EACH baseline (Wilson+bootstrap CI excludes 0, `n0 success>=0.85`), (b) calibration `false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18`, (c) verification `AUROC>=0.75 precision>=0.80`, (d) `M_total_f10` saving `>=25%` vs COLD decomposed `tokens vs browser+latency vs accuracy` with `browser+latency >=20%` and `accuracy>=0.85`, (e) correlated probe `accuracy>=0.90 saving>=30% delta>0.10` vs seeded-42 random `0.53` with `TN>=0.85`, (f) `rho_proxy_real>=0.50` pooled+per-stratum and per-stratum `|rho_shuffled|<0.20 p>=0.20 |rho_length|<0.20 |rho_shuffled_proxy|<0.20`.

- **H0 (null):** Margins, calibration, verification or saving fail with controls PASS non-degenerate, or substrate/BrowserGym health fails rendering `MEASUREMENT_INVALID` (not falsification).

Prior plausibility: Scout correctly flagged central stall (no `VALIDATED` claim, Product `f=100` Pareto premature); Director adopted Scout sequencing but PIVOTed Product from distributed `n>=800` to single-family `n>=360` honest gap first. Agent priors used (sunk-cost bias at `0.525` ceiling `21/40` with `0.0` routing gain, LLM spurious similarity plateau `10/10` vs `0/10`, measurement traps `X-Worker-Pid>=10 n_non304>=360`, false-accept gating) are priors distinct from SPIDER evidence per `request.json:director_mandate.agent_priors_used`.

---

## 3. Carry-forward from parent (preserved distinctions, SUPERSEDE disposition)

Per `parent_handoff` `52cae0ba...` (`EXP-PRODUCT-36046064994`):

**Established (retain, not re-assumed):**
- Frozen-inputs byte-identical verified (audit PASS, no bijective `n*3200/f*6.0`, trajectory-grouped `B=5000` intact) — but must be re-verified on this packet; prior is evidence not auto-valid.
- Contamination-free holdout RETAINED at MV2: rebuilt `webarena_verified_v2_tasks_192_36_rebuilt.json sha 101e481d...` (requested prefix `374ef8f6...` flank-case rebuild `18` even families `135` remapped, `0/36` pool+usage disjoint, Jaccard `0.0` on `630` pairs via `qcr_bank_manifest 8c69804b TAU0.30) — supersedes `391e8f6c` (`18/36` contaminated). Must recompute via `value_set_A intersect B`.
- Single-node HS256 sticky substrate health-gated PASS at `n_non304 400 200/200 >=360/180` (`WAL pid 52069 gunicorn 23.0.0 PyJWT 2.14.0 nginx 1.24.0 $request_uri sticky`) with `n_304 351 TN 1.0 probe saving 0.40 delta 0.4067` — re-verify per MV4; prior `400` alone insufficient.
- Correlated `TTL 60s ETag W/body_sha` probe discriminates (`hit 1.0` at `n==0`, `accuracy 1.0 false_accept 0.0` at `n0.25`, saving `0.40` delta `0.4067>0.10` vs seeded-42 random `0.53`).
- Kernel dot-regex functionally PASS `5/5` (`src/spider/kernel.py` working-tree `d926279d` pattern `\$\{[A-Za-z_][A-Za-z0-9_\.]*\}`) but NOT committed durable (`HEAD 8af66ccf` vs working-tree, `provenance kernel_durable false`, audit validity_finding 5) — must be committed at `cee979c2`.
- `PC3 MockEnv AUROC 0.871` vs shuffled `0.468` precision `0.949` ECE `0.107` (MockEnv only, not transfer to BrowserGym).
- Honest per-trajectory-reset economics ceiling `SPIDER f10 1981 vs COLD 5992 saving 0.669` but ratio `1.506 vs RAG` FAIL diagnostic not falsification (17 null metrics, `MEASUREMENT_INVALID`).

**Rejected (bounded, do not generalize beyond):**
- Canonical `192/36 sha 391e8f6c` contaminated (`18/36` value overlap) — must not reuse.
- `NC1` shuffled null as deterministic file-proxy honest counters (`rho_shuffled -0.136 p 0.0724` FAIL `p>=0.20`, `rho_length -0.287` per-stratum all `>0.20`) — deterministic coupling disclosed; must break coupling on real trajectories.
- No rejection of `C-PRODUCT-ECON M_total` Pareto on honest substrate — previous `MEASUREMENT_INVALID` bounded to infrastructure (GHCR denied, `OPENAI_API_KEY` absent, `playwright 1.44 vs 1.63`, `DSM 0` overlap).

**Unknown (remain unknown until EXECUTE on provisioned substrate):** GHCR `BrowserGym 0.14.3` authorization, `OPENAI_API_KEY` + `playwright 1.63`, kernel commit durability, `NC1` coupling on real trajectories, honest `M_total` Pareto vs `RAG` at `f=10/100`, DSM `80-94%` compile on overlapping sites, per_hit supersession conjoint, `ST-WebAgentBench CuP` safety.

**do_not_assume (explicitly unsafe):** `MEASUREMENT_INVALID` is infrastructure failure not falsification; probe saving `0.40` or ceiling `0.669` does NOT imply Pareto dominance; working-tree kernel patch not durable; Jaccard `0.0` not equal to value_set disjointness; `MockEnv AUROC 0.871` does not transfer to `gpt-4o-mini`; `NC1 -0.136` band PASS does not mean null valid (`p 0.0724` FAIL); `B-STAGEHAND-PC1 1.0` file-proxy `DOM hash 5/5` not equal to Docker `2000-node AX>10`; `DSM f10 6236>5992` on `0/36` overlap not proof compilation fails generally.

Director **SUPERSEDE** retains these established facts as dependencies but replaces `parent_handoff.next_question` (Pareto `f10/f100` before distributed `n>=800`) with the smaller single-family LLM gap test as the binding next question (see `request.json:director_mandate.allocation.parent_handoff_disposition SUPERSEDE` and `portfolio_assessment`).

---

## 4. Experimental design (smallest high-information, not pre-2.0 repeat)

**Population & holdout:** Rebuilt `192/36` (`101e481d`, fallback `c2763ebae9`, requested prefix `374ef8f6`) — 192 TRAIN / 36 TEST per family-stratified split? Actually `192` total tasks across 36 families? Wait corpus is `192/36` tasks? Use as `N=192` pooled with `36` families? Predeclares `192 rebuilt` (or `258 Hard258` extension if `pip webarena_verified` digest `64-char` with disjoint value_sets available) — but gating holdout remains rebuilt `192/36` with `0/36` disjoint and `L 8-14` family-specific constant orthogonal to `n` within strata. `qcr_bank_manifest sha 8c69804b TAU0.30` frozen ranker same for `RAG`/`SGDR`. If `Hard258` added, must log `64-char` digest and site overlap `>0` for non-degenerate DSM (currently `0/36` degenerates).

**Substrate (MUST be health-gated for SURVIVES):**
- Single-node `HS256` sticky at `/tmp/spider-runtime/shared.db` `WAL` single `gunicorn 23.0.0` single-worker `HS256 PyJWT 2.14.0` + `nginx 1.24.0 $request_uri` consistent-hash sticky, `If-None-Match`/`ETag W/body_sha` conditional `200` vs `304`, `n_non304>=360` stratified (`180/endpoint` where two endpoints, `TN>=0.85`, `If-None-Match fraction 1.0` errors `0`) — re-measured this packet, logged `shared.db WAL worker=1 JWT alg TN n_non304 stratified sticky hash ETag n_304/n_200` (`substrate_probe.json`).
- Correlated `TTL 60s max-age ETag W/body_sha` probe `10tok+30ms` fresh at `n0 ~1.0` vs `~50%` stale at `n=0.25` vs `seeded-42 random 0.53` decoupled NC, per-step `probeHit/etagMatched/ttlValid` logged, `probe_is_correlated true` for SUT, saving `>=30%` accuracy `>=0.90` `falseAccept<0.05` `delta>0.10`.
- Kernel dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` committed at `cee979c2` (`d926279d`) — `provenance` must show `working-tree == HEAD` committed, `kernel/commit` logged, `5/5 n0 EXECUTABLE confidence>=0.80`.

**Browser + LLM (MUST for SURVIVES, else MEASUREMENT_INVALID):**
- `Docker` `BrowserGym 0.14.3` `ghcr.io/servicenow/browsergym:0.14.3` + `playwright 1.63.0` with binaries + `OPENAI_API_KEY` for `gpt-4o-mini` `15-step` `Playwright` `1280x720` `CDP getFullAXTree` `2000-node` `AX>10` heterogeneous — logged `Docker` availability, image digest, `BrowserGym` version, node count, viewport, real `tokens` per step, `browser_calls`, `latency ms`, `AX nodes>10`. Proxy vs real `Spearman rho_proxy_real>=0.50` pooled+per-stratum required plus per-stratum `|rho_length|<0.20 |rho_shuffled_proxy|<0.20`.
- Same `model/tools/budget` across ALL conditions (`SPIDER/COLD/INSTRUCTIONS/RAG/STAGEHAND`) — logged `model id`, `steps`, `tools`, `budget`, `AX nodes` per trajectory. Mismatch => `MEASUREMENT_INVALID` for LLM-inherit sub-claim.

**Conditions (5, same rebuilt splits, same L, same honest counters, same BrowserGym/budget):**
1. `B-COLD` — no memory.
2. `B-INSTRUCTIONS` — `B-COLD` + site-specific NL instructions (same token budget as probe overhead).
3. `B-RAG-EMBED-TAU030-QCR-K5` — QCR frozen-bank `TAU0.30` top-`k=5` (k=1 sensitivity) `200tok+150ms` with verify fallback.
4. `B-STAGEHAND-CACHE` — `DOM-hash` cache without `TTL` correlation (2x `~30%` claim), `hit 1.0` at `n0` else `0`.
5. `P-SPIDER-LLM-INHERIT` — freshness-gated `0.95/0.85 Jaccard 0.85` + deterministic repair + correct-family + `TTL` probe + `MEA auditor` `softmax temp0.15+jitter`.

All TRAIN-only induction, `value_set_A intersect B empty` strictly on all `36` families, cross-family `Jaccard max 0.0` via `qcr_bank`.

**Honest counters (f=10 only — cognitive reset, no f=100 Pareto here):** Per-trajectory-reset integer sum counters `M_total_f10 = resolve+bind(10tok probe) + retrieval(200+150ms)/SGDR(180)/DSM(15) + verify(50tok+120ms) + browser_steps+latency ms from Playwright + distill amortized /f + auditor` — no `n*3200`, no `f*6.0`, no jitter. Decomposed `tokens vs browser+latency vs accuracy`. `ST-WebAgentBench CuP` safety logged per trajectory where BrowserGym exercised but not gating `MEASUREMENT_INVALID` for this single-family gap? Actually logged but `product_consequence` requires non-inferior at `f=10`? For `C-LLM-INHERIT` single-family, safety is secondary; we require reporting but not blocking SURVIVES — however `spec.json:measurement_validity MV12` logs repair vs contamination. Decision rule gates only on success/margin, calibration, verification, saving, probe, rho — safety is `UNKNOWN` if not measured (disclosed) not `MEASUREMENT_INVALID`. Parity `per_hit` secondary.

**Novelty levels:** `n=0` (exact repeat), `n=0.25` (50% stale via `304`), optional `n=0.5` sensitivity — L held family-specific constant orthogonal to `n` within strata, trajectory-grouped unit.

---

## 5. Controls (stable identities, EXECUTE must reuse)

**Positive control `PC-SINGLE-NODE-LLM-INHERIT-CORRELATED` (any fail => MEASUREMENT_INVALID):**
- `PC1` Exact-repeat cache: `B-STAGEHAND-CACHE` at `n=0` must hit `1.0` `per_hit ~50` `5/5` per-family via `BrowserGym AX>10` AND `n>=360` stratified.
- `PC2` Orthogonal+correct-family+freshness: `Jaccard 0.0` via `qcr_bank 630` pairs; kernel `5/5 n0 EXECUTABLE confidence>=0.80`; `value_set` disjoint verified; `P-SPIDER` correlated probe `fresh ~1.0` vs `stale ~0.5` `accuracy>=0.90 saving>=30% falseAccept<0.05 vs random 0.53 delta>0.10` logged per-step.
- `PC3` Non-vacuous verify+AUROC: forced shuffled probe/registry via same `BrowserGym` must yield `false_accept 0.10-0.60 confidence_std>0.05 AUROC shuffled 0.45-0.60` and `AUROC true>=0.75 precision>=0.80 UNKNOWN>=0.85 ECE<=0.15`.
- `PC4` Frozen-formula audit: honest `M_total within 1e-6` vs summed counters, `rho_proxy_real` pooled+per-stratum `5000` bootstrap logged, `probeHit` per-step logged.
- `PC5` Health-gate + `BrowserGym` replication: `nginx $request_uri` sticky `n>=360` stratified `HS256 WAL` + `BrowserGym 2000-node 1.63.0 gpt-4o-mini 15-step health_gated If-None-Match` with `AX>10` and `rho_proxy` measurable.

**Null control `NC-SHUFFLE-LLM-INHERIT` (all via same pipeline, no simulated correctness):**
- `NC1` Shuffled probe+registry: trajectory-grouped block-permutation of `parameter_slots` AND swap `TTL` valid→`seeded-42 random 0.53` + swap correct-family keys before resolve; `mock wrong-bound p=0.15` → `UNKNOWN/AUROC` via same `BrowserGym`. Expect `|rho|<0.25 ns |rho_shuffled|<0.20 p>=0.20 per-stratum |rho_length|<0.20 |rho_shuffled_proxy|<0.20 success<=COLD false_accept 0.10-0.60 AUROC 0.45-0.60 M_total ratio~1.0.
- `NC2` Random entry: independent random family/state keys → `UNKNOWN` expect `false_accept>=0.10 AUROC~0.5`.
- `NC3` Length-proportional constant cost: `cost=L*500+probe miss` regardless of novelty → `|rho|~0 R2<0.15`.
- `NC4` Ablations: `TTL correlated vs random delta>10%`, `TN` single-node `>=0.85` vs hypothetical `per-node 0.667` contrast `n>=360 vs <100`, `rho_proxy shuffled <0.20`. All `B=5000` trajectory-grouped block-permutation; `within-family std>0` required.

---

## 6. Measurement validity gates (MV1-MV12)

See `spec.json:measurement_validity` — 12 gates: `MV1` rebuilt `192/36` contamination-free holdout (`101e481d`, `c2763ebae9`, prefix `374ef8f6`, `0/36` disjoint `Jaccard 0.0` `8c69804b`, `L 8-14` orthogonal), `MV2` family hold-out zero-overlap orthogonal clean, `MV3` kernel dot-regex durability at `cee979c2`, `MV4` single-node `HS256` sticky `n_non304>=360` stratified `TN>=0.85 If-None-Match/ETag W/body_sha`, `MV5` correlated `TTL/ETag` single-node stratified `saving>=30% accuracy>=0.90 delta>0.10`, `MV6` Docker `BrowserGym 0.14.3 2000-node 1280x720 CDP AX>10` real `gpt-4o-mini 15-step` with `rho_proxy_real>=0.50` per-stratum, `MV7` same model/tools/budget LLM inheritance, `MV8` honest amortized sum counters decomposed at `f=10` with `saving>=25%` vs COLD `browser+latency>=20% accuracy>=0.85`, `MV9` strong baselines identical splits honest accounting `TAU0.30` same ranker, `MV10` calibration verification-derived (`false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 upper<=0.18 per-class` with `B=5000` bootstrap `confidence_std>0.05`), `MV11` statistics orthogonal `QCR` `B=5000` trajectory-grouped (`|rho_shuffled|<0.20 rho_proxy>=0.50 per-stratum |rho_length|<0.20`), `MV12` abstention repair (`deterministic single-field re-bind verified_state MEA auditor`).

Bijective proxies (`n*3200/f*6.0/jitter`), `CI[1.0,1.0]` degenerate, `within-family std==0`, `confidence_std<=0.05`, empty-bin `ECE` vacuous => `MEASUREMENT_INVALID`. No file-proxy surrogation for `SURVIVES` on browser-validated claim.

---

## 7. Decision rule (frozen, precedence ordered)

Compute per-method `success`, `false_accept`, `UNKNOWN_precision`, `AUROC`, `precision`, `ECE_5bin` per-class, `M_total_f10` decomposed, `M_per_hit` secondary, `Spearman rho_novelty`, `rho_length` pooled+per-stratum, `rho_proxy_real` pooled+per-stratum, `R2`, `probe saves` via honest counters. `Wilson95%` for rates, trajectory-grouped family-stratified `bootstrap5000` for `rho/R2/ratio/ECE/AUROC/rho_proxy/n_non304` CIs, trajectory-grouped `block-permutation5000 p` with `|rho_shuffled|<0.20 p>=0.20` + per-stratum `|rho_length|<0.20` + `rho_proxy>=0.50` per-stratum + `|rho_shuffled_proxy|<0.20` + `n_non304>=360` stratified + `within-std>0 confidence_std>0.05` checks.

- **SURVIVES** (`C-LLM-INHERIT HYPOTHESIS->EXPERIMENTAL`, supersedes `per_hit 1.005>0.85` as economics gate) **iff ALL hold after `PC PASS` non-degenerate stratified with correct frozen controls and provisioned BrowserGym health:**
  - `C1` margin primary: `P-SPIDER` success margin `>=0.12` vs EACH baseline at `f=10` (`Wilson+bootstrap CI` lower excludes `0`, `success>=0.85` at `n0`) on real `BrowserGym gpt-4o-mini` trajectories;
  - `C2` calibration: `false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 bootstrap upper<=0.18` per-class;
  - `C3` verification: `AUROC>=0.75 precision>=0.80` non-degenerate;
  - `C4` economics at `f=10`: `M_total_f10` saving `>=25%` vs `B-COLD` (`bootstrap CI` lower excludes `0`) AND `browser+latency >=20%` vs `COLD` at `f=10` with `accuracy>=0.85` decomposed `tokens vs browser+latency vs accuracy`;
  - `C5` statistics+probe: per-stratum `B=5000` `|rho_shuffled|<0.20 p>=0.20` pooled+per-stratum, `|rho_length|<0.20`, `|rho_shuffled_proxy|<0.20`, `rho_proxy_real>=0.50` pooled+per-stratum (requires BrowserGym tokens), `correlated probe saving>=30% accuracy>=0.90 delta>0.10` vs `seeded-42 random 0.53 TN>=0.85` stratified.

- **FALSIFIES** (controls `PASS` non-degenerate but any `C1-C5` gate fails): `C-LLM-INHERIT` remains `HYPOTHESIS` bounded `REJECTED` for this SUT on health-gated single-node + `BrowserGym 15-step`; f=100 Pareto cannot survive per Director rationale; per_hit `1.005` falsification stands.

- **MEASUREMENT_INVALID** (no claim update): `PC` fails OR `n<360` OR `BrowserGym/OPENAI` absent OR fixtures contaminated OR degenerate OR `GHCR` pull denied without disclosure — irrespective of margins, no file-proxy surrogation.

Precedence: `MEASUREMENT_INVALID` checked before `FALSIFIES`/`SURVIVES`. All thresholds family-stratified trajectory-grouped `N=192` (or `258` if Hard258 extended) `TRAIN`-warmed.

---

## 8. Baselines & product consequences

**Baselines:** `B-COLD`, `B-INSTRUCTIONS`, `B-RAG-EMBED-TAU030-QCR-K5` (`k=5` primary `k=1` sensitivity), `B-STAGEHAND-CACHE`, `P-SPIDER-LLM-INHERIT` — see `spec.json:baselines`.

**If SURVIVES with `PC PASS` non-degenerate stratified (`value_set` disjoint on ALL `36` families `Jaccard 0.0`, kernel `d926279d` at `cee979c2`, `n>=360 TN>=0.85 AX>10 BrowserGym 0.14.3 1280x720 + gpt-4o-mini 15-step`, `probe saving>=30% accuracy>=0.90 delta>0.10`, `rho_proxy>=0.50` per-stratum) and all `C1-C5` hold at `f=10`:** `C-LLM-INHERIT HYPOTHESIS->EXPERIMENTAL` bounded to rebuilt `192/36` health-gated single-node + `BrowserGym` (single-family honest LLM-inherit gap `>=0.12` vs `cold/instructions/RAG-k5/Stagehand` with calibration/verification `>=25%` saving). First valid single-family LLM gap on honest substrate. Justifies preregistering `M_total` gap as `PRODUCT_CORE` economics gate and authorizes `f=100` + distributed `n>=800` next; informs Graph `param-inherit` scaling. No `PRODUCT_CORE` without `DIRECTOR promote_to_product true` and `audit PASS`.

**If FALSIFIED with controls `PASS` non-degenerate (`n>=360 TN>=0.85 AX>10 rho_proxy>=0.50` per-stratum, `n_strat>=180`) but margin `<0.12` or calibration/verification/statistics fail or `saving<25%` at `f=10` or probe `delta<=0.10`:** `C-LLM-INHERIT` remains `HYPOTHESIS` bounded `REJECTED` for this mechanism on health-gated single-node + `BrowserGym 15-step`; honest gap does NOT beat strong `RAG`/`instructions` even on honest substrate; Director to `PARK` product economics and pivot to alternative architectures (compilation `O(1) $0.002-0.092`, Intel diverse-site grounding). `f=100` `MEASUREMENT_INVALID` history is not falsification.

**If `MEASUREMENT_INVALID`:** No claim update; `handoff` retains rebuilt `192/36` holdout, re-provision `GHCR/OPENAI_API_KEY/playwright 1.63`, fix `NC1` deterministic coupling on real trajectories, re-verify `n>=360 TN>=0.85` and kernel durability.

---

## 9. Validity threats & disclosure

- **Shallow prior vs evidence:** Agent priors (`sunk-cost bias 17 failures 0.525 ceiling routing gain 0.0`, `LLM spurious similarity plateau`, measurement traps `X-Worker-Pid n_non304 If-None-Match/304 AX>10`, `false_accept<=0.10 UNKNOWN>=0.85`) are priors explaining stalls, not SPIDER evidence; evidence is Codex `21/40 bound 0.525`, `C-FRESHNESS SURVIVES` synthetic, `C-MEAS-VALID EXPERIMENTAL_BOUNDED 36044045537`, `C-PRODUCT-ECON 14/19 MEASUREMENT_INVALID`, `C-CROSSSITE 28-streak MIXED`.
- **Representation loss:** `DOM hash` encoding `state_id` tautological (`MI 107-198%`) disclosed; `AX>10` heterogeneity via `getFullAXTree` required; single-prefix `field-path` relevance fix limits to `body.* headers.* url`; per-trajectory hard-reset sum counters vs bijective proxies distinguished (`|rho_shuffled|<0.20` honest, not jitter `Gaussian`).
- **Contamination risk:** `value_set_A intersect B` recomputed on ALL `36` families via `value_set` not `SHA` equality; `qcr_bank TAU0.30` `8c69804b` frozen; `391e8f6c 18/36` contaminated must not be staged.
- **Substrate leakage:** Shared `URLs` with synchronized `DB` can appear distributed; health gates (`X-Worker-Pid>=10 n_non304>=360 If-None-Match/304 AX>10`) prevent; `per_hit 1.005>0.85` bounded to file-proxy not to `M_total` Pareto.
- **Cross-site transfer leakage:** Holdout by `URL/host` + task-family stratification; `DOM hash` tautology and `PMI>0 K=3 under H=0` pipeline validation disclosed.
- **Cost realism:** End-to-end economics includes `verification/repair/maintenance` amortized at `f=10` (this experiment) — `f=100` explicitly NOT claimed before this gate per Director.

---

## 10. Execution plan (no outcome data inspected)

1. Stage contamination-free rebuilt `192/36` (`sha 101e481d` `0/36` disjoint `Jaccard 0.0` `8c69804b`) + `qcr_bank TAU0.30` + `cost_config 50/15/180/10` (provenance hashes `TRAIN`-only) — abort if any family overlaps.
2. Commit kernel dot-regex `d926279d` to `HEAD` at `cee979c2` — log `working-tree == HEAD`.
3. Provision single-node `HS256` `WAL` at `/tmp/spider-runtime/shared.db` (`gunicorn 23.0.0` single-worker `PyJWT 2.14.0` `nginx 1.24.0 $request_uri` sticky) — run health probe `n_non304>=360` stratified `TN>=0.85 If-None-Match/ETag W/body_sha` `TTL 60s` (`substrate_probe.json`).
4. Provision Docker `BrowserGym 0.14.3` + `playwright 1.63.0` + `OPENAI_API_KEY` (`gpt-4o-mini 15-step`) — log image digest, `2000-node 1280x720 AX>10`, `rho_proxy_real` measurable; if unavailable => `MEASUREMENT_INVALID` for browser claim (disclosed, no file-proxy surrogation).
5. Execute `5 conditions × 3-5 novelty levels × 192` trajectories + `NC1-NC4` `5000` permutations via honest per-trajectory-reset sum counters on `BrowserGym` — collect `success`, `false_accept`, `UNKNOWN`, `ECE`, `AUROC`, `M_total_f10` decomposed, `probeHit`, `rho_proxy`.
6. Compute family-stratified trajectory-grouped `B=5000 bootstrap` + `5000 block-permutation` CIs per MV11 — compare to frozen thresholds without peeking then decide per §7.
7. Write `result.json` (required `schema_version, experiment_id, lane, status, outcome, metrics, controls, artifacts, observations, validity_notes, unresolved`) with stable metric/control IDs, `report.md` bounded by measurements, `provenance.json` (commits, run ids, `Docker` digest, `AX>10`, `n_non304` stratified, `value_set` disjoint hashes, `kernel commit`, `gpt-4o-mini` model id).

---

## 11. Estimated cost & information gain

**Cost:** Moderate health-gated single-node stratified + provisioned LLM `BrowserGym`: `192×5×3-5 ≈960` trajectories + `NC` `~400` + probe `~200` + calibration `~200` ≈ `1760` trials on `SQLite WAL` sticky `n>=360` plus `TFIDF` offline; `CPU <60min` (`<120min` with `Docker 2000-node`), storage `~2500-3500` rows `branch_traces`; with `Docker+gpt-4o-mini`: `~2880` calls `<$30` (see `spec.json:estimated_cost`).

**Information gain:** Decisive gating per Director `REOPEN` `cognitive_reset SUPERSEDE`: first discriminating single-family honest LLM-inherit test before `f=100` Pareto; positive `->EXPERIMENTAL` and retires `per_hit 1.005` gate authorizing distributed next, negative `PARK`s product economics even on honest substrate (see `spec.json:expected_information_gain`). Scout breadth vs Intel deep verification respected; Frontier alias basin `0.525` ceiling not repeated.

---

*Preregistration frozen before outcome data; any change after seeing outcomes is exploratory and requires new preregistration. Execution must not inspect `M_total` margins before `freeze.json`.*
