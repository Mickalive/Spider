# EXP-PRODUCT-35741913862 — Preregistration

**Experiment:** C-RESIDUAL-NOVELTY residual-novelty economics — real pipeline
**Lane:** product
**Claim:** C-RESIDUAL-NOVELTY (HYPOTHESIS → EXPERIMENTAL if SURVIVES)
**Created:** 2026-09-22
**Director Mandate:** REOPEN C-RESIDUAL-NOVELTY, action REOPEN, cognitive_reset true, parent_handoff_disposition SUPERSEDE (EXP-PRODUCT-35725756862 handoff is continuity evidence only, not research direction). Binding strategic question in request.json director_mandate.question is the research direction.
**Frozen:** BEFORE any outcome-bearing measurement (DESIGN only)

---

## 1. Strategic Question (Director binding)

> Do matched WebArena-Verified families at 0%,25%,50%,75%,100% novelty (train on resource A, test on never-observed B with 36 families >=3, duplication 0.9479) show later-agent cost tracking residual novelty rather than full length when SPIDER parameterized inheritance is implemented as a real resolve/bind pipeline (required_slots, freshness gating 0.25, confidence<0.80 UNKNOWN abstention, verification/repair) measured as tokens+browser+retrieval+verification+repair amortized over frequency vs COLD vs instructions vs retrievable RAG vs TERX 0-token replay that hits at 0% with block-permutation p-values?

DESIGN converts this into the smallest rigorous falsifiable experiment below. We do NOT repeat the parent's synthetic wiring that was MEASUREMENT_INVALID (bijective cost formula, starved baselines, degenerate p). We preserve its continuity evidence (Section 2) but the Director's REOPEN + SUPERSEDE is binding: the central hypothesis remains pay-cost-of-novelty-not-full-length, but the substrate must be repaired (RF1-RF9) to make falsifiers reachable and economics honest.

Related Director priors (request.json director_mandate.agent_priors_used):
- Path dependence / reconstruction vs verbatim replay prior (MemHarness) — verbatim replay can be harmful without adaptation; SPIDER must demonstrate reconstruction benefit with guards.
- Tunneling indicator >10 consecutive exps with degenerate controls signals diminishing marginal information — product must not tunnel on same mock with formulaic cost.
- LLM agents benefit from memory only with applicability guards + verification/repair; false_accept, UNKNOWN abstention and repair cost amortized dominate economics (not token savings alone; SPIDER has shown only 5.42% analytical savings).
- Effective dynamics identifiability requires history conditioning; without it PMI/TV collapses to destination predictability or tautological mapping — explains leakage 78-92% and guides design to not conflate action→observation with dynamics; our product experiment measures cost conditional on verification, not PMI.

---

## 2. Inherited State (from parent handoff EXP-PRODUCT-35725756862, superseded but preserved)

### 2.1 Established (must not be re-assumed beyond ceiling, but informs validity)

- Frozen inputs of parent authentic and unmodified (request eef2aea33..., spec b7060720..., prereg 145fde67..., freeze 07ecf939... verified vs git commit bba7197e; provenance hash 24c9a715.. was recording error, not tampering). New experiment's freeze will be independent.
- In deterministic simulation where per-task SPIDER cost was defined as 250+500*int(10n) tokens with success=1, metrics deterministically reproduced formula: 100 SPIDER rows tokens {250,1250,2750,3750,5250} 20x each, Spearman rho=1.0, slope 5000, R2 0.995, delta 0.995 (harness artifact, not SPIDER measurement). This establishes only that the harness can generate a deterministic mock, not that novelty tracking exists.
- Synthetic catalog mock with L=10 fixed workflow (search->filter->open->select->add->checkout->verify, 12 stores sharing platform) and controlled novelty bins (novel_counts 0,2,5,7,10) can be generated and frozen proxy applied deterministically — but this is artifact generation, not mechanism measurement.
- Substrate can measure 0-token replay in isolation: hand-injected PC1 exact-repeat row achieves B-REPLAY-TERX 50 tokens (0 LLM +50 verification) +1 browser call ~150ms and success 1, but only outside compared set. PC2 reused 1.0 was forced in code (line328), not measured — demonstrates 0-token replay capability exists but was not exercised in honest comparison.
- Prior C-FRESHNESS pipeline existence (kernel freshness_check behavioral_score 0.8 on 401/403 vs 0.0 on 200 at threshold 0.25, TP1.0 FP0.0 at reduced N on localhost Flask) and prior orthogonality confirmations at delta0.15 from three stochastic PASS (EXP-GRAPH-35353011131 r0.046, EXP-GRAPH-35389145821 r0.002, EXP-PRODUCT-35445596342 r-0.026, n=480 each, audit PASS) remain established but NOT extended by parent wiring; kernel remains literal-only for distill, parameterized logic still harness-only. New experiment stays harness-level and does not claim kernel integration.
- Prior C-RESIDUAL-NOVELTY evidence ceiling remains: EXP-INTEL-35651934683 doc survey only (corrected WebArena shopping M1 0.311 from empirical 4.42 not 0.818 hardcoded 10, M2 heuristic, M3 false for WebArena true for Mind2Web with instance-level but not mechanism-overlap guarantee) and EXP-FRONTIER-35651943981 bundled FALSIFIED-IN-SETTING with spec contradiction (SURVIVES requires adv0>0.20 and <=0.15 impossible) and length artifact; no cost-vs-novelty measurement established. C-RESIDUAL-NOVELTY remains HYPOTHESIS (codex/claim_state.json).

### 2.2 Rejected (must not be assumed)

- Bounded rejection: claim that EXP-PRODUCT-35725756862 demonstrated SURVIVES_CURRENT_TEST for C-RESIDUAL-NOVELTY at synthetic/WebArena-inspired mock ceiling — rejected as MEASUREMENT_INVALID; cost proportionality (rho1.0, R2 delta 0.995) and beats RAG/REPLAY/INSTR ratios (0.06/0.19 vs 0.80, 0.07/0.28 vs 0.85, <5600 at >=25%) are arithmetic consequences of chosen formulas and starved baselines, not measurements (VF1,VF6-VF8, BF3-BF4).
- Bounded rejection: interpretation that controls NC1 (shuffled |rho|<0.25) and NC2 (random false_accept>=0.30) validated that novelty tracking depends on correct parameterization/ranking — rejected; both returned flat tokens by construction (VF7, BF5) and false_accept hash-assigned (0.38 from h<45) not verification-derived, so they tested nothing about mapping effect.
- Bounded rejection: interpretation that SPIDER within 2x of REPLAY at 0% (ratio 0.192) or that C2/C5 beating REPLAY at >=25% demonstrates pay-cost-of-novelty superiority — rejected; REPLAY hit_rate 0/100 in compared set (including n=0.0) vs frozen expected 1.0, so comparison was SPIDER formula vs REPLAY miss-fallback 5500 tok; honest accounting with REPLAY-as-designed hit (50 tok) yields ratio ~5.0 opposite direction (VF6, BF4, RF3).
- No broader rejection: residual-novelty economics globally, parameterization generalizability, or caching-vs-generalization tension are NOT closed — environment rendered falsifiers unreachable (VF10); C-RESIDUAL-NOVELTY remains HYPOTHESIS, not REJECTED. C-PRODUCT-ECON logistic extrapolation remains REJECTED (6-model vacuous step k10.75 R2=1.0 identical to null) — do not assume token economics viable without direct measurement.

### 2.3 Unknown (this experiment is designed to answer one of them; others remain open)

- Whether later-agent cost is proportional to residual novelty fraction vs full length under a real (executed) parameterized inheritance mechanism with genuine costs (LLM tokens, browser calls, retrieval+verification+repair) — untested because binding/gating/abstention/verification/repair were never executed (RF1, unresolved2 in handoff). **This experiment's primary unknown.**
- Whether parameter-slot binding of never-observed B values survives verification (generalization to unseen identifiers, the central test) — untested; success/false_accept constant by assignment (VF3, unresolved2).
- Whether freshness gating (behavioral_score 0.25) and confidence gating (<0.80 -> UNKNOWN) prevent contamination at 100% novelty and what amortized cost via UNKNOWN fallback truly is — untested; M-UNKNOWN 0.0 at all bins including 1.0 (VF4, unresolved3).
- Whether SPIDER advantage persists under fair main-set comparison (REPLAY hitting at n=0 as frozen spec expects, RAG with retrievable trajectories and retrieval-derived success) and honest cost accounting — magnitude unresolved; audit predicted C2 likely fails under honest replay hit (~5.0 vs 2.0 threshold) but not measured (unresolved3).
- Whether novelty tracking holds with real LLM token/latency economics vs frozen proxy (500 tok/step), and whether amortization over f=1,10,100 rescues retrieval cost at commercial frequencies — proxy sensitivity disclosed but untested with real LLM (validity threat).
- Whether effect persists when full task length co-varies with novelty (L=10 constant was artificial isolation guaranteeing R2_length 0.0), when catalog DOM complexity/auth drift are stressed, and across >1 WebArena families — all disclosed as follow-up.
- Whether harness-level distill_parameterized slot induction (2 slots sku/store_id) actually induces from 5 synthetic demos — bypassed by hard-coded registry and kernel.py still literal-only; prior multi-param POCs remain harness-only.

### 2.4 Do-not-assume (dangerous over-generalizations, per handoff carry_forward.do_not_assume)

- Do not assume C-RESIDUAL-NOVELTY is supported, EXPERIMENTAL, or that SURVIVES was achieved — audit MEASUREMENT_INVALID, producer_claim_supported false; no promotion authorized.
- Do not assume rho=1.0 p0.0 CI[1,1] / R2=0.995 / slope 5000 demonstrate novelty-proportional work compression — they are identities of tokens =250+500*int(10n) defined from novelty count (VF1); exact two-sided block-permutation p=0.0167 fails frozen C3 p<0.01 (VF5).
- Do not assume SPIDER beats strong baselines (RAG, REPLAY-TERX, INSTRUCTIONS) at low novelty — REPLAY was starved (0/100 hits incl n=0) and RAG starved (1/100, hash success) (VF6-VF7, BF3-BF4); ratios are handicaps not measured advantages.
- Do not assume success 1.0 false_accept 0.0 UNKNOWN 0.0 demonstrate correctness/abstention at 100% novelty — all constants assigned in code (VF3-VF4); binding error rate >0.20 trigger and MIXED flat-cost outcome were structurally unreachable (VF10).
- Do not assume bootstrap CI [1,1] or Wilson low 0.8389 indicate precision — both are around assigned constants with degenerate formula variance.
- Do not assume NC1/NC2 controls proved mapping/ranking matters — both flat-cost by construction (VF7).
- Do not assume NC1 success 0.35 as stated — actual 0.45 (45/100) in raw CSV matching code h<35 rule; do not assume provenance freeze hash 24c9a715.. is correct — actual is 07ecf939.. verified in git (VF9, RF8).
- Do not assume amortized ratios (f1 0.208 SPIDER/COLD, f1 0.192 SPIDER/REPLAY, f10 0.062 vs RAG) use consistent units — producer added DISTILL to every baseline and mismatched bootstrap CI units (VF8, BF6, RF6); B-INSTRUCTIONS f10 amortization not implemented.
- Do not assume synthetic L=10 catalog mock, token proxy, single-family, harness-level parameterization generalize to WebArena-Verified DOM, real LLM, cross-site transfer, or production hosting — ceiling explicitly bounded to synthetic mock; Intel sample-level mechanism overlap and Runtime distributed replication remain prerequisites for Docker full-DOM scale-up per Director dependencies intel/graph/runtime.
- Do not assume prior inflated M1=0.818 — corrected 0.311 is honest bound; do not assume WebArena has official instance splits (M3 false); do not import frontier TV/KDE rho=1.0 translation-only signal as Web evidence.
- Do not assume C-FRESHNESS validated/product-core — remains EXPERIMENTAL at localhost mock ceiling only.

---

## 3. Hypothesis

**H1 (primary, C-RESIDUAL-NOVELTY):** Later-agent cost under SPIDER parameterized inheritance (freshness gating + UNKNOWN abstention) is proportional to residual novelty fraction, not full task length, when cost is MEASURED from executed pipeline branches (not defined from novelty label).

Formally: `cost_SPIDER(n) = C_fixed + C_novel * n` where `n ∈ {0.0,0.25,0.50,0.75,1.0}` is the fraction of parameterizable identifier slots whose values were never observed during training on resource A (test on unseen B), `C_fixed` = retrieval (200 tok +150ms) + verification (50 tok +120ms), `C_novel` << `C_cold` (500 tok +2 calls per novel/failed-verification step). At `n=0.0` SPIDER cost is ≥60% cheaper than B-COLD (full-length) and within 2× of B-REPLAY-TERX (0-token replay cost ~50 tok verification only) with high reuse fraction ≥0.90. At `n=1.0` SPIDER cost via UNKNOWN fallback is ≤1.10× B-COLD (no worse than cold). Spearman `rho(cost_SPIDER, n) ≥0.60` (two-sided block-permutation p<0.01, bootstrap 95% CI lower >0.35, slope >0 p<0.01) and `R2_novelty - R2_full_length ≥0.15` (with `R2_novelty ≥0.30` given `R2_length ≈0.00` at constant L=10).

**H2 (strong-baseline superiority):** SPIDER amortized cost per success beats B-RAG by ≥20% at `n=0.0` and `n=0.25` and beats B-INSTRUCTIONS by ≥15% at same bins (both at f=10 honest amortization), and beats B-REPLAY-TERX at any `n ≥0.25` (where exact replay misses) at f=10. This demonstrates parameterized inheritance adds commercial value beyond retrieval and caching, with honest accounting (distill only for SPIDER, instruction tokens correctly amortized, block-permutation p-values, and baselines that actually hit where designed).

**Null (H0):** Cost is flat vs novelty (`rho≈0`, `R2_novelty ≈0`) or SPIDER not cheaper than strong baselines at low novelty, indicating pay-full-task-length or no advantage over retrievable RAG/replay — residual-novelty economics do not exist in this setting, or are offset by retrieval/verification/repair overhead (captured via MIXED outcome if C1 passes but C3/C4 fail). MEASUREMENT_INVALID is substrate failure (mechanism not executed or baselines still starved), not H0.

---

## 4. Design Overview

### 4.1 Task families (matched, constant full length, novelty-controlled, exact-repeat at 0%)

- **Source:** WebArena-Verified shopping task family as template (36 families >=3, duplication 0.9479 per Director portfolio assessment). If WebArena JSON fixtures are accessible locally (cached repo or `/tmp/webarena`), import shopping task intents + accessibility-tree fragments directly as in EXP-INTEL-35651934683; otherwise use synthetic Flask catalog mock replicating WebArena shopping structure: 12 store instances sharing platform (per corrected M1=0.311 but M1=1.0 for store sharing per EXP-INTEL-35651934683), 996-task structure, template-like parameterization (heuristic M2≈0.8). The chosen source is logged in `provenance.json`; either satisfies the Director's strategic question while avoiding Docker-hosting prerequisite flagged as dependency. Ceiling disclosed as synthetic/WebArena-inspired mock if mock is used.
- **Structure:** Each task is a fixed-length `L=10` step workflow: `search(query) → filter(category) → open(product) → select(variant) → add_to_cart → checkout → verify`. Only identifier slots vary: `${sku}`, `${store_id}`, `${category}`, `${variant}`. Full length is constant by construction; only residual novelty varies. This isolates the novelty effect from length (disclosed as artificial isolation; follow-up must co-vary length).
- **Training set (resource A):** 5 demonstrations per family on A identifiers (e.g., `A_SKU_001..050`, `A_STORE_01..06`) stored as observations. `distill_parameterized` with `_extract_varying_values` (field-path-relevant, structure-similarity ≥0.75, validated in EXP-PRODUCT-33741671686 but still harness-only) induces one parameterized mechanism per family with slots `${sku}`, `${store_id}` (and possibly `${variant}`) via ACTUAL code path, not hard-coded registry. Registry confidence 0.90. All training identifiers are disjoint from test B identifiers except as controlled by novelty fraction. Registry write/read via actual `MechanismRegistry` is exercised and logged.
- **Test set (resource B, controlled novelty, exact-repeat fix RF3/RF4):** 5 bins ×20 tasks =100 SPIDER test tasks:
  - `n=0.00`: 100% identifiers from A set AND test sequence exactly equals a training trajectory (exact repeat, not just identifier pool overlap). This makes B-REPLAY-TERX hit_rate=1.0 reachable inside the compared set (resolving frozen contradiction: spec expected hit 1.0 at 0%, prereg 4.1 said not exact replay — we choose exact-repeat semantics and freeze it here). Both B-RAG (Jaccard 1.0) and B-REPLAY-TERX (exact string equality) MUST hit at 0% by construction; we verify hit_rate in main set.
  - `n=0.25`: 25% slots are unseen B values, 75% are A values, with overlap sampling ensuring expected Jaccard ~0.75 for RAG (not 0.2 as in parent random disjoint sampling that made RAG unreachable).
  - `n=0.50`: 50% unseen B
  - `n=0.75`: 75% unseen B
  - `n=1.00`: 100% unseen B (fully novel resource B, never-observed)
  - Assignment within bins is deterministic and stratified by position in workflow to avoid ordering confounds. Deterministic seeds (PYTHONHASHSEED=0, random.seed 42).
- **Length-proportional fail-able control:** One additional baseline B-LENGTH-PROPORTIONAL (see 4.3) is run on same bins but with cost proportional to length (flat vs novelty) to demonstrate MIXED/falsifier is reachable.

### 4.2 SPIDER system under test (real pipeline, RF1/RF2/RF7)

- **Harness-level** (not yet kernel-integrated per audit: kernel.py `distill` is literal-only, parameterized logic lives in harness `run_experiment.py` — same as parent but now actually executed). Registry holds the parameterized mechanism. At test time for each task:
  1. `resolve(intent, context, params)` with test `params` (contains B identifiers for novel slots) via actual `SpiderKernel.resolve` consulting `MechanismRegistry`, checking `required_slots = set(parameter_slots) | template_slots`, not a stub.
  2. Freshness gating: probe `mechanism.freshness.probe_url` if present (reuse Flask JWT mock if used, HS256, same behavioral_score 0.8 on 401/403 vs 0.0 on 200 threshold 0.25) — but catalog drift is not the focus; freshness is exercised as gating branch and can trigger UNKNOWN. If behavioral_score ≥0.25 → return `UNKNOWN` (abstain) rather than false accept. This branch is actually evaluated per task (not skipped).
  3. Confidence gating: if `best.confidence <0.80` → `UNKNOWN` (actual check).
  4. If `UNKNOWN` → fallback to B-COLD simulated LLM cost for remaining novel steps (honest abstention, counted in cost, success via fallback verification, not constant).
  5. If `EXECUTABLE` → `bound_action = _bind(action_template, params)` via actual `_bind` and verification step checks postconditions against simulated observed_state; on verification failure charge repair cost (1 LLM step 500 tok+2 calls) and count false_accept if binding was wrong. No forced constants; success/false_accept/unknown/reused_steps are verification-derived with genuine variability, so rho can be <1 and C3/MIXED are falsifiable (RF1,RF2,RF7,RF9).
- **Cost model (frozen proxy, no LLM keys, but measured):** Retrieval 200 tok +150ms, verification 50 tok +120ms (1 browser call), reused verified step 0 tok +0 calls, novel/failed-verification step 500 tok +2 browser calls (120ms each), repair 500 tok +2 calls. These constants are frozen before execution; sensitivity analysis varies tokens/step ±50% and browser latency ±50% in report appendix. Crucially, cost is SUM of executed branches per task, not `250+500*int(10n)` formula — novelty influences cost only via pipeline decisions (RF2).

### 4.3 Baselines (identical 100-task set, identical proxy, honest accounting RF6, retrievable RF4, hit inside set RF3)

All baselines run on the same 100 tasks with same proxy and same verification fallback logic, via same harness:

- **B-COLD:** No memory. Every step is novel: cost = 10×500 tok +20 browser calls. Retrieval cost 0. Success via verification, not constant. Distill NOT added.
- **B-INSTRUCTIONS:** Instructions tokens correctly amortized (200/f) + full exploration of identifier steps (still 10 novel steps, but instruction saves one reasoning step: 9×500 tok at f=1; at f=10 honest is 20+4500=4520, not 4800 as parent misreported). Tests instructions alone vs SPIDER.
- **B-RAG:** Jaccard retrieval over prior A trajectories (TAU=0.30). Now RETRIEVABLE by construction: at n=0.0 expected hit 1.0 (exact set match), at n=0.25 expected ~0.75 overlap → hits proportional, not 1/100. If retrieved trajectory's identifier set matches test identifiers at verification (actual bind check), reuse matching steps at 0 cost; else fallback to B-COLD for mismatched steps. Retrieval cost 200 tok +150ms per task. Success derived from verification after fallback, not hash bands (RF4 fix).
- **B-REPLAY-TERX:** Exact string equality on `action_template` (no parameterization). Hit iff test identifier sequence exactly equals a training trajectory. Hit cost 0 tok +50 tok verification +1 browser call; miss cost = B-COLD (5000+50). Because n=0.0 tasks are exact repeats, hit_rate=1.0 at 0% inside compared set is enforced and measured (RF3 fix). Hit_rate at 100% =0.0, intermediate bins proportional to exact overlap (n=0.25 low hit, etc.). No distill added.
- **B-LENGTH-PROPORTIONAL:** Fail-able control (RF9): cost = task length × unit cost regardless of novelty (flat vs novelty). Designed to fail C3/C4 (rho≈0, R2≈0), proving the environment can express not only SURVIVES but also MIXED/FALSIFIED. If this control spuriously shows |rho|≥0.35, novelty label is confounded.

### 4.4 Controls (real semantics, RF7, plus fail-able demonstration RF9)

- **PC1 (PC-PARAM-AND-REPLAY):** Exact-repeat TERX at n=0.0 must be 0 LLM tokens +50 tok verification +1 browser call and 100% success with hit_rate=1.0 measured inside main set (not only hand-injected row). SPIDER at n=0.0 on same A set must be EXECUTABLE via actual pipeline with reused_actions ≥0.90. Failure → MEASUREMENT_INVALID.
- **NC1 (shuffled mapping):** Randomly permute learned slot→identifier mapping (e.g., `${sku}`↔`${store_id}`) before SPIDER resolve on same 100 tasks via actual registry/bind/verify pipeline (not flat 5200 formula). Each task incurs real retrieval+verify+fallback costs based on verification outcomes (mismatched binds fail verification → repair/fallback cost, introducing variability). Expect Spearman |rho|<0.25 p≥0.05 (block-permutation) and success ≤ B-COLD.
- **NC2 (random retrieval):** SPIDER retrieval returns random registry entry instead of ranked match, UNKNOWN disabled, via actual ranking path. Expect false_accept ≥0.30 (verification-derived) and flat cost vs novelty. Demonstrates ranking/gating matters; not hash-assigned flat cost.
- **B-LENGTH-PROPORTIONAL as additional falsifiability witness:** Expected to fail C3 (rho 0) and C4 (R2 0), demonstrating MIXED (C1 passes but C3/C4 fail) is reachable, unlike parent where FALSIFIED/MIXED were structurally unreachable (VF10).

### 4.5 Sample size and power (block-aware)

- `n_SPIDER =100` paired cost-novelty observations (20 per bin) gives >0.90 power to detect Spearman rho≥0.60 at α=0.01 (requires n≥44) under sampling variability — but now variability is genuine (pipeline decisions) not 20-fold ties of 5 values, so power claim is honest. Five bins of 20 give Wilson CI width ~±0.18 at 0.85 success per bin; aggregated 100 gives width ~±0.07. Baselines each also n=100.
- Primary test uses exact block-permutation p (permute bin labels 5! =120 permutations; two-sided p=2/120=0.0167 for perfect monotone, one-sided 1/120=0.0083). This is the decision threshold for C3 (p<0.01 two-sided); perfect monotone alone yields 0.0167 which FAILS C3 two-sided, correctly requiring either stronger evidence or one-sided justification — disclosed. Normal-approximation p reported as secondary. Bootstrap 5000 resamples stratified by bin for 95% CI on cost ratios and rho with degenerate handling (if variance 0, CI flagged as degenerate, not claimed as precision).
- Two-sided tests throughout; block structure respected.

---

## 5. Metrics (stable IDs for result.json, auditable via raw CSV)

| ID | Definition | Unit |
|----|------------|------|
| `M-SUCCESS-SPIDER` | Success rate per novelty bin and overall for SPIDER (verified postconditions, not assigned) | fraction |
| `M-SUCCESS-COLD`, `M-SUCCESS-RAG`, `M-SUCCESS-REPLAY`, `M-SUCCESS-INSTR`, `M-SUCCESS-LENGTH` | Success rate per baseline (verification-derived) | fraction |
| `M-FALSE-ACCEPT-SPIDER` | False accept rate: EXECUTABLE returned with wrong binding that fails verification / would cause wrong side effect | fraction |
| `M-UNKNOWN-RATE-SPIDER` | Abstention rate (UNKNOWN returned) per bin (genuine UNKNOWN branch, not constant) | fraction |
| `M-COST-TOKENS-SPIDER` | Sum proxy tokens per task (retrieval+verify+exec+repair) MEASURED from executed branches | tokens |
| `M-COST-BROWSER-SPIDER` | Browser calls per task (measured) | count |
| `M-COST-LATENCY-SPIDER` | Simulated latency per task (browser_calls*120ms + retrieval*150ms + token proxy at 2ms/token) | ms |
| `M-COST-AMORTIZED-SPIDER-f1`, `f10`, `f100` | Amortized cost per success at repeat frequency f: (total_cost + distill_cost/f)/success_rate where distill_cost 1000 added ONLY to SPIDER | tokens |
| `M-COST-*_COLD/RAG/REPLAY/INSTR/LENGTH` | Same cost metrics for each baseline (distill NOT added; INSTR amortized as 200/f) | tokens / ms |
| `M-COST-RATIO-SPIDER-COLD-0pct` | Amortized SPIDER / COLD at n=0.0 (honest units, matching CI) | ratio |
| `M-COST-RATIO-SPIDER-REPLAY-0pct` | Amortized SPIDER / REPLAY at n=0.0 (REPLAY hits at 1.0 inside set) | ratio |
| `M-COST-RATIO-SPIDER-COLD-100pct` | Amortized SPIDER / COLD at n=1.0 (UNKNOWN fallback) | ratio |
| `M-REUSED-ACTIONS-FRACTION-SPIDER` | Fraction of steps reused without LLM at n=0.0 (measured, not forced) | fraction |
| `M-SPEARMAN-RHO` | Spearman rho between M-COST-TOKENS-SPIDER and novelty_fraction (n=100, block-permutation p primary) | rho |
| `M-SPEARMAN-RHO-BLOCK-P` | Exact block-permutation two-sided p for M-SPEARMAN-RHO (primary decision) | p |
| `M-SPEARMAN-RHO-NORMAL-P` | Normal-approximation p (secondary, for comparison to parent) | p |
| `M-SLOPE-NOVELTY` | Linear regression slope cost_SPIDER ~ novelty_fraction | tokens per 100% |
| `M-R2-NOVELTY`, `M-R2-LENGTH` | R2 from cost~novelty and cost~full_length regressions (length constant 10) | R2 |
| `M-R2-DELTA` | R2_novelty - R2_length | delta |
| `M-CORRELATION-NC-SHUFFLE` | Spearman rho for NC1 shuffled control (block-permutation) | rho |
| `M-FALSE-ACCEPT-NC2` | False accept for NC2 random retrieval (verification-derived) | fraction |
| `M-HIT-RATE-REPLAY-0pct`, `M-HIT-RATE-RAG-0pct` | Measured hit rates in main set at n=0.0 | fraction |
| `M-BOOTSTRAP-CI-RHO`, `M-BOOTSTRAP-CI-RATIO-COLD-0` | Bootstrap 95% CIs on same units as decision metrics, with degenerate flag | interval |

All metrics computed from raw per-task CSV `artifacts/raw_per_task.csv` (columns: task_id, novelty_fraction, system, success, false_accept, unknown, tokens, browser_calls, latency_ms, reused_steps, hit, verification_passed, repair_triggered). All hashes logged.

---

## 6. Decision Rule (frozen, block-permutation primary)

**SURVIVES_CURRENT_TEST** requires **ALL** of (C1)–(C6) measured via actual pipeline (not formula):

- **C1 (correctness + abstention, verification-derived):** SPIDER `M-SUCCESS-SPIDER` at `n=0.0` ≥0.85 (Wilson 95% CI lower ≥0.72) and mean success across `n∈{0,0.25,0.5,0.75,1.0}` ≥0.80, with `M-FALSE-ACCEPT-SPIDER` ≤0.10 and binding error rate ≤0.20 across all bins (all via verification outcomes, not constants) and `M-UNKNOWN-RATE-SPIDER` =0.0 at 0% and ≥0.0 at 100% via genuine UNKNOWN branch (i.e., UNKNOWN was exercised, not constant 0.0).

- **C2 (work compression vs cold and vs replay, honest amortization):** At `n=0.0`, `M-COST-RATIO-SPIDER-COLD-0pct` (amortized f=1, distill only SPIDER, matching CI) ≤0.35 (≥65% cheaper than full-length COLD). At `n=0.0`, `M-COST-RATIO-SPIDER-REPLAY-0pct` (f=1, REPLAY hit at 1.0 inside set) ≤2.0 (SPIDER within 2× of 0-token replay; beating replay not required at exact repeat). At `n=1.0`, `M-COST-AMORTIZED-SPIDER-f1` / `M-COST-AMORTIZED-COLD-f1` ≤1.10 (not more expensive than cold when fully novel, via UNKNOWN fallback). All CIs on same units as ratios.

- **C3 (novelty tracking, block-permutation):** `M-SPEARMAN-RHO` ≥0.60 with two-sided block-permutation `M-SPEARMAN-RHO-BLOCK-P` <0.01 and bootstrap 95% CI lower >0.35, and `M-SLOPE-NOVELTY` >0 with p<0.01 (block-permutation or regression p). Note: perfect monotone 5-bin pattern yields exact two-sided p=0.0167 which FAILS this threshold — so C3 requires either genuine variability that strengthens evidence or acknowledgment that perfect monotone alone is insufficient at two-sided 0.01 (one-sided 0.0083 would pass if pre-registered one-sided, but we freeze two-sided).

- **C4 (novelty explains cost, not length):** `M-R2-DELTA` ≥0.15 and `M-R2-NOVELTY` ≥0.30 given `M-R2-LENGTH` ≈0.00 (length constant L=10 by design; `M-R2-LENGTH` expected <0.02 and its bootstrap CI upper <0.15 is reported). If task length truly constant, pass requires `M-R2-NOVELTY` ≥0.30.

- **C5 (beating strong memory baselines, honest):** At amortized `f=10` (distill only SPIDER, INSTR 200/f), SPIDER cost per success beats B-RAG: `M-COST-AMORTIZED-SPIDER / M-COST-AMORTIZED-RAG` ≤0.80 at both `n=0.0` and `n=0.25` (with retrieval-derived success, RAG hits at 0% by construction); and beats B-INSTRUCTIONS: ≤0.85 at same bins. Additionally SPIDER beats B-REPLAY-TERX at every `n≥0.25` (`cost_SPIDER < cost_REPLAY` at 0.25,0.50,0.75,1.00 at f=10, where REPLAY miss cost dominates and hit_rate measured).

- **C6 (controls, real semantics):** PC1 `M-COST-TOKENS-REPLAY` at `n=0.0` =50 LLM tokens (0 LLM +50 verification) with `M-HIT-RATE-REPLAY-0pct` =1.0 in main set and PC2 `M-REUSED-ACTIONS-FRACTION-SPIDER` at `n=0.0` ≥0.90 via measured pipeline pass; NC1 `M-CORRELATION-NC-SHUFFLE` |rho|<0.25 p≥0.05 (block-permutation) and success ≤ B-COLD; NC2 random-retrieval `M-FALSE-ACCEPT-NC2` ≥0.30 (verification-derived) or |rho|<0.25. Additionally B-LENGTH-PROPORTIONAL must show |rho|<0.25 and `M-R2-NOVELTY` <0.15 (demonstrating fail-able control, RF9).

**FALSIFIED** if any C1–C6 fails (excluding PC/NC substrate failures which are MEASUREMENT_INVALID).

**MIXED** if C1 passes but C3 or C4 fails: mechanisms are correct and low false-accept (so parameterization works) but cost is flat vs novelty (constant overhead dominates), indicating reuse without residual-novelty proportionality. This outcome must be demonstratively reachable via B-LENGTH-PROPORTIONAL control (which is expected to be MIXED by construction), so the environment is not biased to SURVIVES only.

**MEASUREMENT_INVALID** if: (i) PC1 or PC2 fail due to harness binding/execution errors (success <0.50 at `n=0.0` for all systems, or binding error rate >0.20, or hit_rate at 0% <0.90 for REPLAY/RAG where hits are by construction), (ii) NC1 spuriously shows |rho|≥0.35 p<0.05 indicating novelty label confounded with task difficulty, or (iii) infrastructure failure (registry write/read, mock unreachable when used) or block-permutation null variance degenerate with no behavioral variability to permit inference (i.e., cost variance 0). These are recorded as `status=MEASUREMENT_INVALID`, not scientific falsification. The producer must report degenerate bootstrap handling (CI [value,value] flagged).

All recomputations use frozen `result.json` metric IDs and raw CSV; block-permutation p is primary audit metric.

---

## 7. Validity Threats and Mitigations (including RF1-RF9 repairs)

1. **Bijective cost formula (VF1, RF1/RF2) →** Fixed: cost is sum of executed branches (retrieval+verify+exec+repair) via actual resolve/bind/verify, not `250+500*int(10n)` formula. Success/false_accept/unknown are verification-derived, not constants. Spearman rho can be <1 and degenerate CI is flagged; block-permutation p is primary.
2. **Mechanism not executed (VF2, RF1) →** Fixed: registry is actual `MechanismRegistry` write/read, `required_slots` check, `_bind`, freshness probe (0.25), confidence<0.80 UNKNOWN branch actually evaluated per task; UNKNOWN fallback cost honestly counted. Registry hash and per-task branch trace logged.
3. **Success/false_accept constants (VF3/VF4) →** Fixed: verification postconditions with possible failures and repairs; false_accept and UNKNOWN rates are measured outcomes, with genuine variability.
4. **Frozen baseline semantics contradiction exploited (VF6, RF3) →** Fixed: choose exact-repeat semantics for n=0.0 (test sequence == training trajectory) and freeze it here; B-REPLAY-TERX hit_rate=1.0 at 0% inside compared set is required and measured; B-RAG also hits at 0% by construction (overlap 1.0). The alternative semantics (n=0 not exact repeat) is explicitly rejected and documented.
5. **RAG starved (VF7, BF3, RF4) →** Fixed: sampling ensures retrievability at low novelty (overlap proportional to novelty, TAU 0.30 reachable); success is retrieval/verification-derived, not sha256 hash bands; hit_rate reported and must be >0 at 0%.
6. **Statistics on tied constructed data (VF5, RF5) →** Fixed: block-permutation p (exact 2/120) is primary, normal approximation secondary; data has genuine variability via pipeline decisions, not 20-fold ties of 5 values; bootstrap stratified by bin with degenerate handling.
7. **Accounting artifacts (VF8, BF6, RF6) →** Fixed: `amortized_cost()` adds DISTILL_TOKENS/f only to SPIDER, not baselines; B-INSTRUCTIONS correctly amortized as 200/f; bootstrap CIs computed on same units as decision ratios (amortized ratios, not raw-token ratios).
8. **Controls flat-cost guarantees (VF7, BF5, RF7) →** Fixed: NC1/NC2 go through actual binding/ranking/verification, incurring real costs based on verification outcomes (mismatched binds fail → repair/fallback), so rho=0 is not guaranteed; PC2 reused fraction measured, not forced 1.0.
9. **Environment cannot express falsifier/MIXED (VF10, RF9) →** Fixed: add B-LENGTH-PROPORTIONAL fail-able control that should fail C3/C4 (rho≈0, R2≈0) and demonstrate MIXED is reachable; binding error rate >0.20 trigger is reachable if pipeline is broken.
10. **Proxy vs real LLM economics:** Token/browser proxy is not real LLM latency/tokens. Mitigation: proxy values frozen and disclosed; sensitivity analysis varies tokens/step ±50% and browser latency ±50%; report whether SURVIVES is robust to proxy choice. No real LLM keys needed for proxy isolation, but scale-up to real LLM is disclosed as not claimed.
11. **Synthetic vs WebArena-Verified DOM complexity:** Mock catalog or cached JSON lacks real DOM accessibility-tree complexity (800-element pages, truncation risk, duplication 0.9479 is design parameter if mock used). Mitigation: disclose ceiling as synthetic/WebArena-inspired mock at single-family bounded evidence; do not claim cross-site transfer or production hosting. Intel sample-level mechanism overlap verification and Runtime distributed replication remain prerequisites for scale-up (Director dependencies), but not gating for this proxy-isolation experiment.
12. **Parameterization ceiling:** Harness-level `_extract_varying_values` is synthetic POC validated only on single-char/path+body tests; may not generalize to richer WebArena form fields. Mitigation: limit claim to slots `${sku}`, `${store_id}`, `${variant}` with disclosed heuristic; report slot induction success rate (slots induced / slots expected) via actual induction, not hard-coded.
13. **Amortization assumption:** Retrieval/distill cost amortized over f=1,10,100 is analytical, not measured repeated use. Mitigation: report all three f values; require f=10 advantage for C5; do not claim commercial viability at f=1 alone.
14. **Length constant is artificial:** Fixing L=10 removes natural length variation, guaranteeing R2_length≈0. This is intentional isolation, but limits generalization to tasks where length and novelty co-vary. Mitigation: report that C4 is a best-case isolation test; follow-up must co-vary length and novelty (B-LENGTH-PROPORTIONAL begins to probe this).
15. **Freshness gating not stressed:** Catalog mock has no real auth/session drift beyond parent Flask JWT probe. Mitigation: freshness gating exercised via probe but not the primary metric; its false_accept contribution is reported separately with genuine UNKNOWN rate.

---

## 8. Execution Plan (no outcome data inspected)

1. Freeze proxy constants, seeds, SKU sets, decision thresholds (this file + `spec.json` → `freeze.json` via deterministic freezer; verify hashes).
2. Attempt to load WebArena-Verified shopping fixtures from `/tmp/webarena` or repo cache; else generate synthetic catalog mock with 12 stores, L=10 workflow, 5×20 test tasks at controlled novelty fractions with exact-repeat at 0% and overlap-proportional RAG sampling; write fixtures to `fixtures/tasks.json` with manifest and hashes.
3. Build harness: actual `distill_parameterized` from 5 A observations → registry via `MechanismRegistry` (not hard-coded constant); SPIDER resolve with actual required_slots/freshness/confidence/UNKNOWN/verify/repair branches; baseline implementations (COLD, INSTRUCTIONS, RAG with TAU 0.30 and verification-derived success, REPLAY with exact equality and hit inside set, LENGTH-PROPORTIONAL) with identical proxy and honest amortization; controls (NC1 shuffled via actual permuted bind, NC2 random retrieval via actual ranking).
4. Execute ~800 trials deterministically (`PYTHONHASHSEED=0`, `random.seed 42`), writing `artifacts/raw_per_task.csv` (with hit, verification_passed, repair_triggered, reused_steps), `artifacts/registry.json`, `artifacts/cost_config.json`, `artifacts/branch_traces.json`.
5. Compute metrics per Section 5, block-permutation p (exact 120 permutations stratified), linear regressions, cost ratios at f=1,10,100 with honest accounting, bootstrap 5000 stratified with degenerate handling; write `result.json` with required top-level shape (`schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved`).
6. No LLM keys, no Docker, no browser automation required. Deterministic. Report sensitivity ±50% in `report.md` appendix.

---

## 9. Product Consequences

- **If SURVIVES:** C-RESIDUAL-NOVELTY advances HYPOTHESIS→EXPERIMENTAL at bounded synthetic/WebArena-inspired mock ceiling (L=10 fixed, token proxy, n=100, single-family, harness-level distill, 36-family template). Provides first direct evidence that cost tracks residual novelty with genuine variability and beats retrievable RAG and 0-token REPLAY at >0% (honest amortization, block-permutation p<0.01, reachable falsifiers), unblocking C-PRODUCT-ECON scale-up to real LLM measurement and Docker full-DOM hosting (Intel sample-level overlap + Runtime distributed replication become next prerequisites). No PRODUCT_CORE promotion; replication with real LLM + production WebArena hosting required next.
- **If FALSIFIED / MIXED:** C-RESIDUAL-NOVELTY stays HYPOTHESIS (bounded REJECTED for proxy setting only). If flat cost (MIXED), investigate constant overhead (retrieval/verification/repair dominated). If not beating retrievable RAG/REPLAY where baselines actually hit, parameterized inheritance adds no economics beyond retrieval/caching — caching-vs-generalization tension upheld (TERX dominance at 0% acknowledged, but SPIDER fails to beat at >0), redirect Product lane to C-FRESHNESS, C-DELTA-REPAIR (runtime nginx HIT/SWR/SIE substrate) or C-SEMANTIC-RESOLVE. Prevents premature C-PRODUCT-ECON scale-up.
- **If MEASUREMENT_INVALID:** Fix harness/binding substrate (RF1-RF9) before re-testing economics; do not advance claim.

---

## 10. Related Claims and Lanes

- **C-PARAM-INHERIT:** prior narrow single-char POC (EXPERIMENTAL) and harness-level multi-param POC — this experiment tests its economic *consequence* with real pipeline, not just slot induction.
- **C-PRODUCT-ECON:** closed logistic REJECTED (R2=1.0 vacuous step, COLD 7.5x cheaper) — this experiment provides the missing direct cost-vs-novelty measurement that could justify reopening, but does not itself claim commercial viability at scale.
- **C-FRESHNESS / C-DELTA-REPAIR:** Orthogonal claims; product must not import freshness orthogonality r=-0.53 as validation — remains EXPERIMENTAL at localhost mock. Delta-repair remains 0 exps; runtime nginx substrate (960/960 HIT) is next dependency per Director comparative reasoning.
- **Dependencies:** Intel sample-level mechanism overlap verification, Graph parameterized reuse beyond single-char, Runtime header isolation / distributed replication — not prerequisites for this proxy-based isolation test, but prerequisites for follow-up scale-up to Docker full-DOM (Director dependencies intel, graph, runtime). All are logged.
- **Fresh-context transmission:** All identities (`experiment_id`, `claim_ids`, metric IDs `M-*`, control IDs `PC*`/`NC*`/`B-*`) are stable for EXECUTE→AUDIT→DIRECTOR. `request.json:request_hash 937669c2cc...` and `freeze.json` hashes are immutable; provenance must match actual artifact hashes (fixing parent hash mismatch 24c9.. vs 07ecf9..).

---

## 11. Preregistration Integrity

No outcome-bearing measurement has been run. `spec.json` and this `prereg.md` are the frozen preregistration. Any change after `freeze.json` is exploratory. A new confirmatory claim requires a new experiment ID and untouched evidence. This design directly repairs the 9 substrate failures (RF1-RF9) identified in EXP-PRODUCT-35725756862 audit (bijective cost, unexecuted mechanism, starved baselines, degenerate p, inconsistent accounting, flat controls, unreachable falsifiers) and implements the Director-mandated block-permutation, honest amortized accounting, and retrievable strong baselines that hit at 0% — the first valid test of commercial viability's core promise.

