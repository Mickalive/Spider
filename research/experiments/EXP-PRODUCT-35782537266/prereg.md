# EXP-PRODUCT-35782537266 preregistration

**Experiment ID:** EXP-PRODUCT-35782537266
**Lane:** product
**Claim:** C-RESIDUAL-NOVELTY — Later-agent cost tracks residual novelty rather than full task length
**Secondary claim (product econ consequence):** C-PRODUCT-ECON — SPIDER saves total cost per successful task after retrieval, verification and maintenance
**Status:** DESIGN — not yet frozen (freeze via deterministic freeze.json before EXECUTE)
**Director mandate:** PIVOT, SUPERSEDE — target claim C-RESIDUAL-NOVELTY, cognitive_reset false, parent_handoff EXP-PRODUCT-35777355953 SUPERSEDE disposition. The inherited next_question (product kernel port to live BrowserGym WebShop/ALFWorld N_live>=20) is continuity evidence only and does not drive this design per AGENTS.md precedence and research/EXPERIMENT_PACKET.md §2.
**Requested strategic question (Director binding, request.json:director_mandate.question verbatim):**
> On WebArena-Verified v2 36 families >=3 (192 tasks, 49 templates, duplication 0.9479, param_task 0.8958) with controlled novelty fraction 0/25/50/75/100% (train on resource A, test on never-observed B within same family), does later-agent cost (tokens, browser interactions, retrieval+reconstruction+verification+repair amortized at f=10) track residual novelty (Spearman rho_novelty >0.6, R2_delta >0.5) rather than full task length (rho_length per stratum |r|<0.20) when SPIDER parameterized inheritance (kernel distill_parameterized with Jaccard>=0.75 constant-anchor, freshness gating 0.25, calibrated UNKNOWN <0.80, ECE<=0.15) is measured with genuine execution (not bijective formula) vs COLD vs instructions vs RAG-EMBED vs Stagehand DOM-hash serverCache vs TERX 0-token replay, reporting family-stratified bootstrap CIs, false_accept<=0.10, UNKNOWN precision>=0.85, and honest amortized saving >=25% vs cold?

---

## 1. Question (falsifiable refinement)

On the **WebArena-Verified v2 census 192 tasks across 36 families with ≥3 tasks each (49 templates, task duplication 0.9479, parameterized-task fraction 0.8958)** — already censused and file-available (no BrowserGym live-health dependency, which is currently 0/0 per Director comparative reasoning) — with **controlled residual novelty fraction n ∈ {0.00, 0.25, 0.50, 0.75, 1.00} within family (train on resource A identifiers, test on never-observed B identifiers within same family)**, does **later-agent cost at repeat frequency f=10 (tokens + browser interactions + retrieval + reconstruction + verification + repair, amortized: distill 1000/f only for SPIDER, instruction 200/f for B-INSTRUCTION)** track **residual novelty (Spearman rho_novelty ≥0.60, R²_delta = R²_novelty − R²_length ≥0.50 with R²_novelty ≥0.30)** rather than **full task length (within-stratum Spearman rho_length |r|<0.20)** when **SPIDER parameterized inheritance (src/spider/kernel.py or harness distill_parameterized with Jaccard ≥0.75 constant-value anchor, behavioral freshness gating 0.25, confidence-gated UNKNOWN <0.80 with ECE ≤0.15, verification+repair)** is measured via **genuine execution (cost summed from executed branches per task — retrieval/verify/exec/repair via actual MechanismRegistry/_bind/confidence/freshness/verify — not a bijective formula M=250+500·novelty)** against **B-COLD vs B-INSTRUCTION vs B-RAG-EMBED vs B-STAGEHAND-CACHE (shipped Stagehand DOM-hash+exact-selector 2×/ ~30% baseline, Feb 2026) vs B-TERX-REPLAY (0-token replay with LLM fallback)**, reporting **family-stratified bootstrap 95% CIs (5000, family as resampling unit), false_accept ≤0.10, UNKNOWN precision ≥0.85, and honest amortized saving ≥25% vs COLD at f=10 (SPIDER/COLD ≤0.75)** ?

Refined thresholds for decision (frozen): pooled rho_novelty ≥0.60 with two-sided block-permutation p<0.01 and bootstrap CI lower >0.35; slope>0 p<0.01; R²_delta ≥0.50 (with R²_novelty ≥0.30 disclosed) and |rho_length|<0.20 in all five n-strata; false_accept ≤0.10, UNKNOWN precision ≥0.85, ECE ≤0.15 (5 bins, derived confidence std>0.05).

---

## 2. Motivation and inherited state

### 2.1 Director mandate and strategic context (binding)

Global Research Director cycle 35781743260, lane product, **action PIVOT** to **C-RESIDUAL-NOVELTY** with **parent_handoff_disposition SUPERSEDE**.

**Portfolio assessment (Director):** At 251 canonical experiments SPIDER has converged synthetic-only proofs (C-SEMANTIC-RESOLVE 40/40 alias-OOD, nginx HIT 960/960 loopback, Bayesian K=12 null-centering) but is **blocked on all live/distributed product economics**: Gate0 0/3 real SPAs after 20+61 enumerations, paid-tier CDN HIT/SWR/SIE/304 NOT_MEASURED, distributed session replication TN 0.667, 44-deep runtime tunnel. No claim has advanced to VALIDATED or PRODUCT_CORE on live substrate. Highest marginal information now comes from **substrate-available orthogonal tests** (correlated-state physics, BrowserGym-pinned loopback, Stagehand cache baseline, **residual-novelty honest cost**, hierarchical retrieval) rather than another synthetic parameterization.

**Comparative reasoning for this PIVOT (Director):** Parent handoff proposes extending synthetic alias kernel port to live BrowserGym WebShop/ALFWorld N_live≥20 with PC-BROWSERGYM-HEALTH ≥80%. That continuation inherits the same **BrowserGym 0.14.3 liveness failure that just gave 0/0 health and that Intel showed as 0/4 envs after 12 attempts** — repeating now has high probability of another MEASUREMENT_INVALID with no economics learned. **Fresh Codex view with no handoff would prioritize the neglected residual-novelty cost experiment** that actually executes LLM agent steps (gpt-4o-mini 15 steps Playwright) with **family-stratified hold-out already censused (192 tasks, 36 families)**, directly measuring the **pay for novelty, not full length** hypothesis that Graph's product promises. **Frontier will meanwhile test beyond-RAG retrieval complementarity on same alias splits, so product's comparative advantage is end-to-end economics**, not another alias-OOD correctness point.

**Further portfolio assessment line (deduplicated from Scout brief):** Scout brief was treated as staff advice, not authority; Director adopted Scout's parking of paid-tier CDN and exhaustive LFS but **superseded Scout's single live-browser generalization handoff for frontier/product where substrate_unavailable evidence (0/4 BrowserGym envs live after 12 attempts) predicts MEASUREMENT_INVALID**, scaling instead to substrate-available orthogonal tests.

**Rationale for C-RESIDUAL-NOVELTY (Director):** Product is **IDLE after EXP-PRODUCT-35777355953 SURVIVES synthetic-only (40/40 alias-OOD, ECE 0.065, but live health 0/0)** and **3 consecutive C-PARAM-INHERIT MEASUREMENT_INVALID due to distill double-prefix bug**. **C-RESIDUAL-NOVELTY is neglected (2 recent, both MEASUREMENT_INVALID because cost was bijective formula M=250+500·novelty, registry never consulted, UNKNOWN never exercised, baselines starved)**. It is **central to commercial viability (C-PRODUCT-ECON)** and is **substrate-available: WebArena-Verified v2 census already replicated (192 tasks, 36 families) and does not require BrowserGym live health**. Honest amortized cost vs the now-shipped **Stagehand DOM-hash cache (2× speedup, ~30% cost)** is the competitive falsifier SPIDER must beat before claiming work compression.

**Agent priors used (Director, separately labeled, not SPIDER evidence):** (1) Local-optimum trap in synthetic tuning — repeated estimator hyperparameter search on same synthetic DGP yields diminishing information once per-function heterogeneity established; (2) Cache invalidation harder than caching — DOM-hash validation catches structural drift not semantic drift (auth/permission/body JSON field); (3) Compounding planning errors over long horizons (11+ steps, Online-Mind2Web hard split) make residual-novelty cost dominated by verification/repair loops, not execution length; (4) Tool/API bypass dominance — discovery of endpoint+method+auth scope is higher-leverage inheritance than DOM selector caching; (5) Path dependence and salience — LLM agents over-sample recent context and anchor on first retrieval without calibrated UNKNOWN they over-apply stale mechanisms (ECE/abstention calibration).

**Dependencies (Director):** intel, runtime (sample-level mechanism overlap verification and distributed replication are prerequisites for Docker/full-DOM scale-up, but **not gating for this file-based proxy isolation test**).

### 2.2 Established (must not be re-assumed beyond ceiling, but informs validity)

- **C-SEMANTIC-RESOLVE narrow synthetic SURVIVES via product kernel port EXP-PRODUCT-35777355953 (audit PASS, 40/40 pooled 1.0, Wilson [0.912,1.0], binomial p=1e-40 vs 0.10, McNemar p=6.98e-10 vs B-EXACT-MATCH 0/40, orthogonal 30/30, mixed 10/10, held-out 9/9, per-family 10/10, false_accept 0.0 gap 1.0 vs B-VERBATIM-REPLAY, exact-match 12/12, UNKNOWN precision 1.0, ECE 0.0653 CI [0.0538,0.0769] vs proxy 0.0803, std 0.400, parity gap 0.0, controls C1-C8 PASS; Chromium+CDP AX healthy at 1280×720). Ceiling is synthetic only (minimal derived dict tautologically encodes answer via bound-then-parse; 0/0 BrowserGym live, correctly bounded to exploratory per frozen C1 clause). This is continuity evidence only per SUPERSEDE; do not assume it implies live or economics.
- **C-PARAM-INHERIT narrow ceiling:** Single-slot committed-code synthetic single-slot with template-only binding (EXP-PRODUCT-35132898840 Fix1+Fix2+Fix3, slot_prefixes '' for 2/3 mechanisms), harness-level 21/21 multi-param EXECUTABLE but **kernel integration FALSIFIED ×3 (double-prefix bind fail, noise-field over-parameterization, structure-similarity hallucination)** per EXP-PRODUCT-35767859554 rationale. Kernel `distill_parameterized` with Jaccard≥0.75 constant-anchor is specified but not yet kernel-validated at scale — this experiment tests its **economic consequence** with genuine execution (not just slot induction).
- **C-MEAS-VALID narrow EXPERIMENTAL:** localhost Flask 3.1.3 + PyJWT JWT + gunicorn+nginx loopback (10/10 C1-C10) and header/body discrimination narrow SURVIVES, but distributed replication FALSIFIED (TN 0.667). Not gating for file-based WebArena census.
- **C-RESIDUAL-NOVELTY ceiling is neglect/MEASUREMENT_INVALID, not support:** Latest two product residual-novelty experiments:
  - **EXP-PRODUCT-35725756862** — doc survey inflate M1 0.818→0.311 after correction, heuristic M2, tautological PC/NC, no cost measurement.
  - **EXP-PRODUCT-35741913862** (parent of 357257 redesign) — repaired spec to honest branch-derived cost, block-permutation, retrievable baselines, but **still MEASUREMENT_INVALID before this cycle**: token proxy is not real LLM, synthetic L=10 mock artificial isolation R²_length≡0, harness-level distill, single-family. Provides **repair pattern (RF1-RF9)** but not validated magnitude.
  - No experiment has measured **cost vs novelty with family-stratified WebArena hold-out and honest Stagehand/TERX strong baselines that hit at n=0**.
- **WebArena-Verified v2 census** as enumerated: 192 tasks, 36 families ≥3, 49 templates, duplication 0.9479, param_task 0.8958 — file-available, replicated, satisfies Director's substrate-available claim vs BrowserGym live 0/0.
- **Stagehand Stagehand DOM-hash+exact-selector serverCache** (Feb 2026: 2× speedup, ~30% cost) is **shipped external baseline** SPIDER must beat — adopted as strong baseline per Director's cache-invalidation prior.

### 2.3 Rejected / bounded

- That exact-intent matching (kernel L97) or TFIDF/RAG alone solves orthogonal aliasing — bounded rejection 0/40 vs 40/40 McNemar p=6.98e-10 (EXP-PRODUCT-35777355953), but ceiling is synthetic tautological.
- That pooled r=-0.53 kernel freshness wiring demonstrates orthogonality at delta=0.15 — rejected; orthogonality holds only from three stochastic mocks (r≈0.04, TOST p~2e-08) not kernel wiring.
- That bijective cost definition `tokens = 250+500·int(10n)` with Spearman rho=1.0 CI[1,1] / R²=0.995 demonstrates residual-novelty work compression — **bounded rejection as MEASUREMENT_INVALID** (VF1/VF6: arithmetic identity, not measurement; block-permutation exact two-sided p=0.0167 >0.01 fails frozen C3).
- That success 1.0 / false_accept 0.0 / UNKNOWN 0.0 with flat NC controls validated parameterization/ranking — bounded rejection: constants assigned in code (VF3-VF4, VF7), binding error rate >0.20 and MIXED flat-cost outcome structurally unreachable (VF10).
- That SPIDER beats RAG/REPLAY/INSTR at low novelty per those mocks — bounded rejection: REPLAY hit_rate 0/100 including n=0 where frozen expected 1.0, RAG 1/100 retrievable, so ratios (0.06 vs 0.80 etc.) are handicaps not advantages (VF6-VF8).
- That C-PRODUCT-ECON logistic extrapolation validates token economics — **REJECTED** (vacuous step, 4 pts/3 params, COLD 7.5× cheaper).
- No broader rejection: residual-novelty economics globally, parameterization generalizability, Stagehand caching-vs-generalization tension are **not closed** — falsifiers were unreachable, claim remains HYPOTHESIS.

### 2.4 Unknown (this experiment answers the bold one; others remain open)

- **Whether later-agent cost is proportional to residual novelty vs full length under genuine parameterized inheritance with honest Stagehand/TERX/RAG-EMBED strong baselines on WebArena-Verified v2 family hold-out (36 families) with calibrated UNKNOWN/ECE and family-stratified CIs — this is the unknown under test.**
- Whether Jaccard≥0.75 constant-anchor slot induction generalizes beyond single-char synthetic POC to WebArena family templates with real header/body/query/auth aliasing and mixed multi-channel within one request.
- Whether freshness gating 0.25 + confidence <0.80 + verification+repair prevents contamination at n=1.0 and what honest amortized cost via UNKNOWN fallback truly is (prior M-UNKNOWN 0.0 at all bins).
- Whether SPIDER advantage persists vs **retrievable** RAG-EMBED and **hitting** Stagehand/TERX at n=0 vs starved mocks, with honest accounting (distill only SPIDER, instruction 200/f).
- Whether proxy token/browser cost is robust to ±50% sensitivity and to real LLM measurement (gpt-4o-mini 15 steps Playwright) — proxy disclosed, real LLM is exploratory for this file-based isolation.
- Whether effect persists when full length co-varies with novelty (prior L=10 constant was artificial isolation guaranteeing R²_length≈0) — now length varies 8-14 across families, so within-stratum rho_length test is non-trivial.
- Whether harness-level distill_parameterized generalizes to kernel-committed `src/spider/kernel.py` at scale (prior 3× FALSIFIED) — ceiling remains harness unless committed code hash verified.

### 2.5 Do NOT assume

- Do not assume **C-RESIDUAL-NOVELTY is supported or EXPERIMENTAL** — audit MEASUREMENT_INVALID, producer_claim_supported false; no promotion authorized; prior rho=1.0/R²=0.995 are formula identities.
- Do not assume **SPIDER beats Stagehand 2×/~30% or TERX 0-token at low novelty** — prior REPLAY hit_rate 0/100 at n=0 where spec expects 1.0; honest accounting with hit inside set (RF3) is required.
- Do not assume **success 1.0 / false_accept 0.0 / UNKNOWN 0.0** demonstrate correctness/abstention at 100% novelty — all constants assigned; binding error >0.20 trigger and MIXED outcome must be reachable via genuine verification-derived variability.
- Do not assume **synthetic L=10 artifact or token proxy** generalizes to production DOM complexity, real LLM tokens, cross-site transfer, or paid-tier CDN economics — ceiling explicitly bounded to file-based census (192/36) + proxy unless real LLM measured; Intel sample-level overlap and Runtime distributed replication remain prerequisites for Docker scale-up.
- Do not assume **inflated M1=0.818** — corrected 0.311 is honest bound; do not assume WebArena has official instance splits (M3 false without manual family hold-out).
- Do not import **frontier TV/KDE rho=1.0 translation-only signal** as Web dynamics or residual-novelty evidence — synthetic 2D only.
- Do not assume **C-SEMANTIC-RESOLVE 40/40 synthetic 1.0** implies live AX denoising or economics — synthetic copies observed keys verbatim (adopt-any-observed-key-not-in-registry), not evidence of WebArena extraction.
- Do not assume **BrowserGym health 0/0 is MEASUREMENT_INVALID** — per frozen C1 it correctly bounds live to exploratory; WebArena census does not need it.
- Do not assume **pooled ECE 0.065 with 3 empty bins** implies calibrated live confidence — pooled not stratified, live ECE unmeasured.

---

## 3. Hypothesis

**H1 (primary, C-RESIDUAL-NOVELTY):** Later-agent cost under SPIDER parameterized inheritance (Jaccard≥0.75 constant-anchor, freshness gating 0.25, calibrated UNKNOWN <0.80 ECE≤0.15, verification+repair, genuine branch-derived cost not formula) is proportional to residual novelty fraction n (resource B never-observed within same family), not full task length, on WebArena-Verified v2 family-stratified hold-out.

Formally: `cost_SPIDER(n) = C_fixed + C_novel · n` where `C_fixed = retrieval (200 tok+150ms) + reconstruction + verification (50 tok+120ms)`, `C_novel << C_cold` (500 tok+2 calls per novel/failed-verification step). At n=0.0 (exact repeat within family) SPIDER cost is ≥25% cheaper than B-COLD at f=10 (SPIDER/COLD ≤0.75, within 1.20× of hitting Stagehand/TERX) with reused fraction ≥0.90; at n=1.0 (fully novel B) SPIDER via calibrated UNKNOWN fallback is ≤1.10× COLD (no worse than cold, false_accept≤0.10). Spearman rho(cost_SPIDER, n) ≥0.60 (two-sided family-stratified block-permutation p<0.01, bootstrap CI lower >0.35, slope>0 p<0.01) and R²_delta = R²_novelty − R²_length ≥0.50 (R²_novelty≥0.30) while within-stratum rho_length |r|<0.20 for all n bins.

**H2 (strong-baseline superiority, shared with C-PRODUCT-ECON):** SPIDER amortized cost per success at f=10 beats B-RAG-EMBED (retrievable, hits at n=0) by ≥20% at n=0.0 and n=0.25 (ratio ≤0.80) and beats B-STAGEHAND-CACHE (shipped 2×/ ~30%) where parameterization beats structural hash at n≥0.25, and beats B-TERX-REPLAY at every n≥0.25 (cost_SPIDER < cost_TERX at 0.25,0.50,0.75,1.00 at f=10) and beats B-INSTRUCTION by ≥15% at same bins — demonstrating parameterized inheritance adds commercial value beyond retrieval and caching with honest accounting (distill only SPIDER, instruction 200/f, bootstrap CIs).

**Null (H0):** Cost flat vs novelty (rho≈0, R²≈0, R²_delta<0.15) or SPIDER not cheaper than retrievable RAG/Stagehand/TERX at low novelty, indicating pay-full-length or no advantage over caching — residual-novelty economics do not exist in this setting or are offset by retrieval/verification/repair overhead (captured via MIXED if C1 passes but C3/C4 fail). MEASUREMENT_INVALID is substrate failure (mechanism not executed, bijective formula, baselines still starved, binding error >0.20), not H0.

---

## 4. Design Overview (smallest high-information)

### 4.1 Task families (measured census, controlled novelty, honest retrievability)

- **Source:** WebArena-Verified v2 **file-based census 192 tasks across 36 families ≥3 (49 templates)**. Attempt to load JSON fixtures from `/tmp/webarena` or repo-cached manifest (as enumerated in EXP-INTEL-35651934683 and portfolio assessment duplication 0.9479 param_task 0.8958); if unavailable generate **synthetic family-structured mock replicating exactly 36 families, 49 templates, duplication/param_task ratios** with template-parameterized catalog flows (family-specific workflow 8-14 steps: `search → filter → open → select → add_to_cart → checkout → verify` with family-specific parameter slots `${sku}`, `${store_id}`, `${variant}`, `${category}`, header/body/query/auth aliasing). Provenance, source identifiers, hashes, seeds logged; ceiling disclosed as synthetic/WebArena-inspired mock if mock used. **No BrowserGym live health required** for this file-based census (avoids 0/0 MEASUREMENT_INVALID trap per Director comparative reasoning); if Playwright is used for browser interactions, health ≥80% with AX nodes>10 else exploratory.
- **Training set (resource A):** 5 demonstrations per family on **A identifiers disjoint from B** (e.g., `A_SKU_001..050`, `A_STORE_01..06`) stored as observations. **Actual `distill_parameterized`** with `_extract_varying_values` (field-path-relevant, Jaccard ≥0.75, constant-value anchor, structure-similarity ≥0.75 as validated in EXP-PRODUCT-33741671686 but still harness-level per 3× kernel FALSIFIED) induces one parameterized mechanism per family with slots `${sku}`, `${store_id}` (and possibly `${variant}`) via **code path, not hard-coded registry**. Registry confidence 0.90. Train vs test B sets zero overlap except as controlled by n. Registry via `MechanismRegistry` exercised.
- **Test set (family hold-out, exact-repeat fix):** 36 families × ~5.33 tasks avg =192 test tasks stratified as:
  - `n=0.00`: 100% identifiers from A **and test sequence exactly equals a training trajectory** (exact repeat, not just pool overlap) so **B-TERX and B-STAGEHAND hit_rate=1.0 reachable inside compared set** (honest accounting, fixes prior 0/100 starvation).
  - `n=0.25`: 25% slots unseen B, 75% A (expected RAG Jaccard ~0.75, not 0.2)
  - `n=0.50`: 50% unseen B
  - `n=0.75`: 75% unseen B
  - `n=1.00`: 100% unseen B (fully novel)
  Assignment deterministic, stratified by slot position/family to avoid ordering confounds. Overall bins ~38-39 tasks each (192/5) for family-stratified power. Seeds PYTHONHASHSEED=0, random 42.

### 4.2 SPIDER system under test (genuine execution per Director)

- **Harness-level** (kernel `distill` is literal-only at HEAD; parameterized logic lives in harness `run_experiment.py` or committed `src/spider/kernel.py` if `distill_parameterized` present — same as parent but **actually executed**, not stub). At test time per task:
  1. `resolve(intent, context, params)` with test `params` (contains B identifiers for novel slots) via actual `SpiderKernel.resolve` consulting `MechanismRegistry`, checking `required_slots = set(parameter_slots) | template_slots`, scoring candidates (slot count, path segments, query/header/body key presence, prefix structure).
  2. **Freshness gating 0.25:** probe `mechanism.freshness.probe_url` if present (reuse Flask JWT HS256 mock 0.8 on 401/403 vs 0.0 on 200 threshold 0.25 where available) — exercised as branch, can trigger UNKNOWN.
  3. **Confidence gating <0.80:** if `best.confidence <0.80` (softmax temp 0.15 + deterministic jitter, std>0.05, not hardcoded) → UNKNOWN (calibrated, ECE 5 bins).
  4. If **UNKNOWN** → fallback to B-COLD simulated LLM cost for remaining novel steps (honest abstention, not contamination).
  5. If **EXECUTABLE** → `bound_action = _bind(action_template, params)` via actual `_bind` and **verification** against simulated observed_state/postconditions; on verification failure charge **repair** (1 LLM step 500 tok+2 calls) and count false_accept if binding wrong. Genuine variability so rho can be <1 and MIXED reachable.
- **Cost model (frozen proxy, measured from branches):** retrieval 200 tok+150ms, verification 50+120ms, reused verified step 0 tok, novel/failed-verification step 500+2 calls, repair 500+2 calls. Summed from **executed branches per task**, not `250+500·int(10n)` formula. Distill 1000 amortized only to SPIDER at f=10 (primary), instruction 200/f correctly. Sensitivity analysis ±50% in report. If **gpt-4o-mini 15 steps Playwright 1280×720 4096 tok temp 0 seed 42** is available (LANE allowed_code `src`), measure real tokens/browser interactions and report alongside proxy; no outcome inspection before freeze regardless.

### 4.3 Baselines (identical splits, retrievable, honest accounting)

All run on same 192 tasks with same proxy/verification fallback via same harness:

- **B-COLD:** Every step novel: 8-14 ×500 tok + 2 calls/step. Retrieval 0.
- **B-INSTRUCTION:** Instruction tokens 200/f (20 at f=10) + full exploration (saves one reasoning step: (L-1)×500).
- **B-RAG-EMBED:** Embedding cosine (all-MiniLM-L6-v2 offline deterministic if available, else TFIDF/Jaccard TAU 0.30 fallback, fit on train registry only). **Retrievable by construction at n=0 (hit 1.0, Jaccard 1.0)** and proportionally at n=0.25; success verification-derived after fallback, not hash bands.
- **B-STAGEHAND-CACHE:** DOM-hash+exact-selector structural cache (Stagehand Feb 2026 2×/~30% at hit): hit iff DOM structure identical (n=0 exact repeat, hash match); miss → COLD fallback. Hit cost 50 tok verification +120ms (~30% COLD); miss 5000+50.
- **B-TERX-REPLAY:** Exact string equality on `action_template` (no parameterization). Hit 0 tok+50 verif+1 call at n=0 exact repeat (1.0 inside set enforced), miss → COLD.

### 4.4 Controls (real semantics + fail-able demonstration)

- **PC1 (PC-PARAM-AND-REPLAY):** B-TERX and B-STAGEHAND at n=0 must be 50 tok verification +1 browser call, success 1.0, hit_rate 1.0 **measured inside main 192 set** (not hand-injected row). PC2: SPIDER at n=0 on same A set must be EXECUTABLE via actual pipeline with reused≥0.90 (measured, not forced). Failure → MEASUREMENT_INVALID.
- **NC1 shuffled:** Permute learned slot→identifier mapping (e.g., `${sku}`↔`${store_id}`) before resolve on same 192 via actual registry/_bind/verify (real costs from verification outcomes, not flat formula). Expect |rho|<0.25 p≥0.05, success≤B-COLD.
- **NC2 random retrieval:** SPIDER retrieval returns random registry entry instead of ranked, UNKNOWN disabled. Expect false_accept≥0.30 (verification-derived) and flat cost vs novelty.
- **NC3 B-LENGTH-PROPORTIONAL fail-able control:** cost = L × unit cost regardless of novelty (flat vs novelty) — expected to **fail C3/C4** (rho≈0, R²≈0), demonstrating environment can express not only SURVIVES but also MIXED/FALSIFIED (addresses prior unreachable falsifier VF10).

### 4.5 Sample size and power (family-stratified)

- `N_SPIDER≈192` paired cost-novelty observations (36 families, ~38 per bin) gives >0.95 power to detect Spearman rho≥0.60 at α=0.01 (requires n≥44) **under genuine variability** (branch decisions) not 20-fold ties of 5 values, so power claim honest. Family-stratified bootstrap 5000 is primary (resample families with replacement, then tasks within family); block-permutation p (permute n labels within families or exact 120 if 5 bins treated as blocks) is complementary. Wilson CI for rates per bin; stratified bootstrap for ratios. Two-sided tests throughout. If proxy variance 0, degenerate bootstrap [value,value] flagged, not claimed as precision.

---

## 5. Metrics (stable IDs for result.json, auditable via raw CSV)

| ID | Definition | Unit |
|----|------------|------|
| `M-SUCCESS-SPIDER` | Success rate per novelty bin and overall for SPIDER (verified postconditions, not assigned) | fraction |
| `M-SUCCESS-COLD`, `M-SUCCESS-RAG-EMBED`, `M-SUCCESS-STAGEHAND`, `M-SUCCESS-TERX`, `M-SUCCESS-INSTR`, `M-SUCCESS-LENGTH` | Success per baseline (verification-derived) | fraction |
| `M-FALSE-ACCEPT-SPIDER` | EXECUTABLE with wrong binding that fails verification | fraction |
| `M-UNKNOWN-PRECISION-SPIDER` | Correct UNKNOWN (abstained when no applicable or gated) / all UNKNOWN | fraction |
| `M-UNKNOWN-RATE-SPIDER` | Abstention rate per bin (genuine UNKNOWN branch) | fraction |
| `M-ECE-5BIN-SPIDER` | ECE over 5 confidence bins using derived confidence (softmax+jitter, std>0.05, 3 empty bins disclosed) | ECE |
| `M-CONFIDENCE-STD-SPIDER` | Std of derived confidence across tasks | std |
| `M-COST-TOKENS-SPIDER` | Sum proxy tokens per task (retrieval+verify+exec+repair) measured from branches | tokens |
| `M-COST-BROWSER-SPIDER` | Browser calls per task (measured) | count |
| `M-COST-LATENCY-SPIDER` | Latency per task (browser_calls·120ms + retrieval·150ms + tokens·2ms) | ms |
| `M-COST-AMORTIZED-SPIDER-f10` | Amortized cost per success at f=10: (total_cost + 1000/10)/success where 1000 only SPIDER | tokens |
| `M-COST-*_COLD/RAG/STAGEHAND/TERX/INSTR/LENGTH-f10` | Same amortized for each baseline (distill NOT added; INSTR 200/f) | tokens/ms |
| `M-COST-RATIO-SPIDER-COLD-0pct-f10` | Amortized SPIDER/COLD at n=0.0 | ratio |
| `M-COST-RATIO-SPIDER-STAGEHAND-0pct-f10` | Amortized SPIDER/Stagehand at n=0.0 (honest units) | ratio |
| `M-COST-RATIO-SPIDER-RAG-0pct-f10`, `M-COST-RATIO-SPIDER-RAG-25pct-f10` | SPIDER/RAG at n=0.0, 0.25 | ratio |
| `M-COST-RATIO-SPIDER-TERX-25pct-f10` etc. | SPIDER/TERX at n≥0.25 | ratio |
| `M-COST-RATIO-SPIDER-COLD-100pct-f10` | SPIDER/COLD at n=1.0 (UNKNOWN fallback) | ratio |
| `M-REUSED-FRACTION-SPIDER-0pct` | Fraction steps reused without LLM at n=0 (measured) | fraction |
| `M-SPEARMAN-RHO-NOVELTY` | Spearman rho between amortized cost at f=10 and n (family-stratified) | rho |
| `M-SPEARMAN-P-BLOCK` | Two-sided family-stratified block-permutation p (primary) | p |
| `M-SPEARMAN-P-NORMAL` | Normal approx p (secondary) | p |
| `M-SLOPE-NOVELTY` | Linear regression slope cost~n | tok per 100% |
| `M-R2-NOVELTY`, `M-R2-LENGTH-POOLED`, `M-R2-LENGTH-PER-STRATUM` | R² cost~novelty and cost~length (per-stratum and pooled) | R² |
| `M-R2-DELTA` | R²_novelty − R²_length_pooled | delta |
| `M-RHO-LENGTH-PER-STRATUM` | Spearman rho_length within each n bin (5 values) | rho |
| `M-CORRELATION-NC-SHUFFLE` | rho for NC1 shuffled (block-permutation) | rho |
| `M-FALSE-ACCEPT-NC2` | False accept for NC2 random retrieval (verification-derived) | fraction |
| `M-HIT-RATE-TERX-0pct`, `M-HIT-RATE-STAGEHAND-0pct`, `M-HIT-RATE-RAG-0pct` | Hit rates in main set at n=0 | fraction |
| `M-BOOTSTRAP-CI-RHO`, `M-BOOTSTRAP-CI-RATIO-COLD-0-f10` | Stratified bootstrap 95% CIs on same units as decisions, degenerate flagged | interval |

All computed from `artifacts/raw_per_task.csv` (task_id, family_id, template_id, novelty_fraction, length, system, success, false_accept, unknown, unknown_precision, tokens, browser_calls, latency_ms, reused_steps, hit, verification_passed, repair_triggered, confidence, ece_bin) with hashes.

---

## 6. Decision Rule (frozen, family-stratified, block-permutation primary)

**SURVIVES_CURRENT_TEST** requires **ALL of C1–C6 measured via genuine pipeline**:

- **C1 (correctness + calibrated abstention, verification-derived):** SPIDER `M-SUCCESS-SPIDER` at n=0.0 ≥0.85 (Wilson lower ≥0.72) and mean success across n bins ≥0.80, with `M-FALSE-ACCEPT-SPIDER` ≤0.10 overall, `M-UNKNOWN-PRECISION-SPIDER` ≥0.85, `M-ECE-5BIN-SPIDER` ≤0.15 (std>0.05, 3 empty bins disclosed, not hardcoded).

- **C2 (positive controls, honest inside set):** PC1 `M-HIT-RATE-TERX-0pct` =1.0 and `M-HIT-RATE-STAGEHAND-0pct` =1.0 in main 192 set with 50 tok verification-only cost and success 1.0; `M-HIT-RATE-RAG-0pct` ≥0.90; PC2 `M-REUSED-FRACTION-SPIDER-0pct` ≥0.90 via measured pipeline with 5/5 per-family spot-check binding correctness on A. Failure → MEASUREMENT_INVALID.

- **C3 (novelty tracking, Director rho>0.6 block-permutation):** `M-SPEARMAN-RHO-NOVELTY` ≥0.60 with two-sided family-stratified `M-SPEARMAN-P-BLOCK` <0.01 and bootstrap CI lower >0.35, and `M-SLOPE-NOVELTY` >0 p<0.01.

- **C4 (residual-novelty explains cost, not length, Director R²_delta>0.5 |r|<0.20):** `M-R2-DELTA` ≥0.50 (and `M-R2-NOVELTY` ≥0.30 reported; `M-R2-LENGTH-POOLED` expected <0.05) and `M-RHO-LENGTH-PER-STRATUM` |r|<0.20 for all 5 n strata (report 5 values, pooled). If length varies 8-14 this is non-trivial; at pooled R²_length≈0 pass requires R²_novelty≥0.50.

- **C5 (honest work compression vs strong baselines at f=10):** `M-COST-RATIO-SPIDER-COLD-0pct-f10` ≤0.75 (≥25% cheaper than cold) with bootstrap CI upper <0.85; `M-COST-RATIO-SPIDER-STAGEHAND-0pct-f10` ≤1.20 (within 20% of shipped Stagehand at exact repeat — beating at n=0 not required); **additionally** `M-COST-RATIO-SPIDER-RAG-0pct-f10` ≤0.80 and `M-COST-RATIO-SPIDER-RAG-25pct-f10` ≤0.80 (retrievable RAG, hits at 0); **and** `M-COST-RATIO-SPIDER-TERX` <1.0 at each n≥0.25 (0.25,0.50,0.75,1.00) where TERX misses but SPIDER generalizes; at n=1.0 `M-COST-RATIO-SPIDER-COLD-100pct-f10` ≤1.10 (not more expensive via UNKNOWN). CIs on same amortized units.

- **C6 (null controls, real semantics):** NC1 `M-CORRELATION-NC-SHUFFLE` |rho|<0.25 p≥0.05 and success ≤B-COLD; NC2 `M-FALSE-ACCEPT-NC2` ≥0.30 or |rho|<0.25; NC3 B-LENGTH-PROPORTIONAL |rho|<0.25 and R²_novelty<0.15 (demonstrates falsifiable environment, not guaranteed flat-cost as before).

**FALSIFIED** if any C3–C6 fails while C1–C2 PASS (valid scientific negative — stratified cost does not track residual novelty or no honest saving vs Stagehand/RAG/TERX where they honestly hit).

**MIXED** if C1 passes but C3 or C4 fails: mechanisms are correct/low false_accept (parameterization works) but cost flat vs novelty (rho~0, R²_delta~0) — constant overhead (retrieval/verification/repair) dominates, indicating reuse without compression (captures Director's long-horizon verification/repair prior).

**MEASUREMENT_INVALID** if: (i) PC1/PC2 fail due to harness binding errors (success<0.50 at n=0 for all, binding error>0.20, hit_rate at n=0 <0.90 where by construction hit=1.0), (ii) bijective formula detected (cost variance 0 or cost==250+500·int(10n) rho=1.0 degenerate CI[1,1]), (iii) registry never consulted / UNKNOWN never exercised (UNKNOWN 0 at n=1.0 by construction), (iv) infrastructure failure (registry I/O, Flask mock unreachable when used, embedding model missing with no fallback), or (v) block-permutation null variance degenerate with zero behavioral variability. Record `status=MEASUREMENT_INVALID`, not falsification. Producer must report degenerate bootstrap handling.

All recomputations use frozen `result.json` IDs and raw CSV; family-stratified block-permutation p is primary audit metric.

---

## 7. Validity Threats and Mitigations (including prior RF1-RF9 repairs)

1. **Bijective cost formula (prior VF1 RF1/RF2) →** Fixed: cost summed from **executed branches** (retrieval/verify/exec/repair via actual resolve/_bind/verify), not formula. Success/false_accept/UNKNOWN verification-derived with variability; degenerate CI flagged; family-stratified permutation primary.

2. **Mechanism not executed (VF2) →** Fixed: actual `MechanismRegistry` write/read, `required_slots` check, Jaccard≥0.75 constant-anchor, `_bind`, freshness 0.25, confidence<0.80 UNKNOWN branch evaluated per task; trace logged.

3. **Success/false_accept constants (VF3-VF4) →** Fixed: verification postconditions with failures+repairs; rates measured, not assigned; binding error >0.20 trigger reachable.

4. **Frozen baseline semantics contradiction / starved baselines (VF6 RF3 RF4) →** Fixed: **exact-repeat semantics at n=0** (test sequence == training trajectory) frozen here; B-TERX/B-STAGEHAND hit_rate 1.0 inside set required and measured; B-RAG-EMBED retrievable at n=0 (overlap 1.0, TAU 0.30) with verification-derived success, not hash bands; hit_rates reported and must be 1.0/1.0/≥0.90 at n=0.

5. **Statistics on tied constructed data (VF5 RF5) →** Fixed: family-stratified bootstrap 5000 and block-permutation p primary; data has genuine variability via pipeline decisions, not 20-fold ties; degenerate handling disclosed.

6. **Inconsistent accounting (VF8 RF6) →** Fixed: `amortized_cost = (total_cost + distill/f)/success` adds 1000/f **only to SPIDER**, instruction 200/f correctly, CIs on same amortized units. Stagehand/TERX at hit is 50 verif tok, not 0.

7. **Flat-cost controls guaranteed (VF7) →** Fixed: NC1/NC2 go through actual binding/ranking/verification incurring real costs based on verification outcomes (mismatched binds fail → repair/fallback), so |rho|<0.25 not guaranteed; PC2 reused measured not forced 1.0.

8. **Environment cannot express falsifier/MIXED (VF10 RF9) →** Fixed: NC3 B-LENGTH-PROPORTIONAL (flat vs novelty by construction, rho≈0 R²≈0) demonstrations MIXED reachable; binding error trigger reachable.

9. **Proxy vs real LLM economics →** Proxy values frozen and disclosed; sensitivity ±50% in report appendix; robustness of SURVIVES to proxy choice reported. No real LLM keys needed for file-based isolation, but scale-up to gpt-4o-mini 15 steps Playwright is disclosed as next step if available — not claimed as measured unless actually executed.

10. **Synthetic vs WebArena file-based DOM complexity →** Mock or cached JSON lacks full DOM accessibility-tree complexity (800-element pages, truncation, duplication 0.9479 design param if mock). Mitigation: **disclose ceiling as file-based census** (192/36) at single-platform bounded evidence; do not claim cross-site transfer or production Docker hosting. Intel sample-level mechanism overlap and Runtime distributed replication remain prerequisites for Docker scale-up (Director dependencies intel/runtime) but not gating.

11. **Parameterization ceiling (harness-level) →** Jaccard≥0.75 constant-anchor POC validated only on single-char/path+body tests; may not generalize to richer WebArena form fields. Limit claim to slots `${sku}` etc. with disclosed heuristic; report slot induction success rate via actual induction per family.

12. **Stagehand baseline strength →** Stagehand DOM-hash catches structural drift not semantic (auth/permission/body JSON per Director prior 2). Our test includes mixed header+body+query aliasing and orthogonal behavioral-structural freshness to frame Stagehand 2×/~30% as the falsifier SPIDER must beat only at >0% novelty, not at exact repeat.

13. **Length constant is artificial (prior L=10) →** Fixed: length now varies 8-14 across families; within-stratum rho_length test is non-trivial; report that pooled R²_length≈0 is not artifactual.

14. **Freshness gating not stressed →** Catalog mock has no real auth/session drift beyond Flask JWT probe. Gating exercised via probe but not primary metric; its false_accept contribution reported separately with genuine UNKNOWN rate.

---

## 8. Execution Plan (no outcome data inspected)

1. Freeze proxy constants, seeds, SKU sets, families, decision thresholds (this file + `spec.json` → `freeze.json` via deterministic freezer; verify hashes).
2. Attempt to load WebArena-Verified v2 shopping fixtures from `/tmp/webarena` or repo cache; else generate synthetic family-structured mock replicating exactly 36 families ≥3, 49 templates, duplication/param_task ratios; write fixtures to `fixtures/tasks.json` with manifest and hashes (36 families, 192 tasks, 5/ family demos).
3. Build harness: actual `distill_parameterized` from 5 A observations per family → `MechanismRegistry` (Jaccard≥0.75 etc.), SPIDER resolve with required_slots/freshness 0.25/confidence<0.80/verify/repair branches; baseline implementations (COLD, INSTRUCTION, RAG-EMBED with offline embedding, STAGEHAND DOM-hash cache, TERX exact equality, LENGTH-PROPORTIONAL) with identical proxy and honest amortization; controls NC1 shuffled via permuted _bind, NC2 random retrieval.
4. Execute ~1150-1350 trials deterministically (PYTHONHASHSEED=0, random 42) across 36 family strata, writing `artifacts/raw_per_task.csv` (with hit, verification_passed, repair_triggered, reused_steps, confidence), `artifacts/registry.jsonl` per family, `artifacts/cost_config.json`, `artifacts/branch_traces.json`.
5. Compute metrics per §5, family-stratified bootstrap 5000 CIs, block-permutation p, linear regressions (robust SE), ECE 5-bin, cost ratios at f=10 with honest accounting, per-stratum rho_length; write `result.json` with required top-level shape (`schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved`) preserving stable IDs.
6. Report sensitivity ±50% on tokens/step and browser latency, per-family breakdown, and duplicate handling.

No LLM keys, Docker, or browser automation required for file-based census (proxy isolation). If gpt-4o-mini+Playwright available, run optional 15-step validation and report separately without affecting primary decision.

---

## 9. Product Consequences

- **If SURVIVES (C1–C6 PASS, family-stratified):** C-RESIDUAL-NOVELTY advances **HYPOTHESIS→EXPERIMENTAL** at bounded file-based WebArena-Verified v2 ceiling (192/36 file/mock as logged, token proxy or gpt-4o-mini 15-step Playwright where measured, harness or committed kernel Jaccard≥0.75). Provides **first non-bijective evidence that amortized cost tracks residual novelty (rho>0.6, R²_delta>0.5) not length (|r|<0.20)** with calibrated abstention (false_accept≤0.10, UNKNOWN precision≥0.85, ECE≤0.15) and **honest saving ≥25% vs cold at f=10 beating retrievable RAG-EMBED and shipped Stagehand 2×/~30% at >0% novelty and TERX at ≥25%** (family-stratified CIs, reachable falsifiers). **Unblocks C-PRODUCT-ECON scale-up** to Docker full-DOM hosting + real LLM measurement with measured effect size as prior (Intel sample-level overlap + Runtime distributed replication next prerequisites). No **PRODUCT_CORE** promotion; replication with production WebArena Docker hosting + real LLM tokens + kernel-committed `distill_parameterized` required before promotion.

- **If FALSIFIED / MIXED (C3-C6 fail, C1-C2 PASS):** C-RESIDUAL-NOVELTY stays **HYPOTHESIS (bounded REJECTED for file-based proxy setting only)**. If flat cost (MIXED), investigate constant overhead (retrieval/verification/repair dominates). If not beating retrievable RAG / hitting Stagehand/TERX, **parameterized inheritance adds no economics beyond retrieval/caching** — caching-vs-generalization tension upheld (TERX/Stagehand dominance at 0% acknowledged, but SPIDER fails to beat at >0%). Redirect Product lane per Director to **C-FRESHNESS, C-DELTA-REPAIR (runtime nginx HIT/SWR/SIE)** or **C-SEMANTIC-RESOLVE** before revisiting economics. Prevents premature C-PRODUCT-ECON scale-up. No global falsification of residual novelty beyond this DGP.

- **If MEASUREMENT_INVALID:** Fix harness/binding substrate (RF1-RF9, Jaccard/freshness/UNKNOWN calibration, retrievable baselines) before re-testing economics; do not advance claim. Do NOT treat as falsification.

---

## 10. Related Claims and Lanes

- **C-PARAM-INHERIT:** prior narrow single-char POC (EXPERIMENTAL) and harness 21/21 multi-param — this experiment tests its **economic consequence** with genuine family hold-out, not just slot induction.
- **C-PRODUCT-ECON:** closed logistic REJECTED (vacuous step, COLD 7.5× cheaper) — this experiment provides the **missing direct cost-vs-novelty measurement that could justify reopening**, but does not itself claim commercial viability at scale (file-based bound).
- **C-FRESHNESS / C-DELTA-REPAIR:** Orthogonal; product must not import freshness r=-0.53 anti-correlation as validation — remains EXPERIMENTAL at localhost mock; runtime nginx substrate (960/960 HIT) is next dependency for delta-repair per comparative reasoning.
- **Frontier lane:** will test beyond-RAG hierarchical retrieval complementarity on same alias splits — product's comparative advantage is **end-to-end economics** vs retrieval, not alias correctness alone (Director allocation).
- **Dependencies:** Intel sample-level mechanism overlap verification, Graph parameterized reuse beyond single-char, Runtime header isolation / distributed replication — not prerequisites for this file-based isolation but **prerequisites for Docker/full-DOM scale-up** (Director deps intel/runtime). Logged.
- **Fresh-context transmission:** All identities (`experiment_id`, `claim_ids`, metric IDs `M-*`, control IDs `PC*`/`NC*`/`B-*`) are stable for EXECUTE→AUDIT→DIRECTOR. `request.json:request_hash 10af109a...` and `freeze.json` hashes immutable; provenance must match actual artifact hashes.

---

## 11. Preregistration Integrity

No outcome-bearing measurement has been run. `spec.json` and this `prereg.md` are the frozen preregistration. Any change after `freeze.json` is exploratory. A new confirmatory claim requires a new experiment ID and untouched evidence. This design **directly implements the Director's PIVOT/SUPERSEDE** from synthetic alias port's live BrowserGym 0/0 trap to **substrate-available WebArena-Verified v2 family hold-out honest economics**, repairs the 9 substrate failures (bijective formula, unexecuted mechanism, starved baselines, degenerate p, inconsistent accounting, flat controls, unreachable falsifiers) flagged in the last two C-RESIDUAL-NOVELTY audits, and introduces the **shipped Stagehand DOM-hash cache as the competitive falsifier SPIDER must beat** before claiming work compression — the first valid test of commercial viability's core promise at family-stratified resolution.

