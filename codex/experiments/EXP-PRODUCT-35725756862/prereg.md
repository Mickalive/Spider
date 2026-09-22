# EXP-PRODUCT-35725756862 — Preregistration

**Experiment:** C-RESIDUAL-NOVELTY residual-novelty economics
**Lane:** product
**Claim:** C-RESIDUAL-NOVELTY (HYPOTHESIS → EXPERIMENTAL if SURVIVES)
**Created:** 2026-09-22
**Director Mandate:** REOPEN C-RESIDUAL-NOVELTY, action REOPEN, parent_handoff_disposition SUPERSEDE (EXP-PRODUCT-35697049382 handoff is continuity evidence only, not research direction)
**Frozen:** BEFORE any outcome-bearing measurement (DESIGN only)

---

## 1. Strategic Question (Director binding)

> Do matched WebArena-Verified task families with controlled novelty fraction (0%, 25%, 50%, 75%, 100% unseen identifiers, training on resource A testing on never-observed B) show later-agent cost (tokens, browser calls, latency, retrieval+verification+repair amortized over frequency) tracking residual novelty rather than full task length when SPIDER parameterized inheritance (with freshness gating and UNKNOWN abstention) is compared vs COLD vs instructions vs retrieval/RAG vs TERX/BrowserBash 0-token replay + LLM fallback strong baselines?

DESIGN converts this into the smallest rigorous falsifiable experiment below. We do NOT repeat the parent's C-FRESHNESS kernel freshness_check orthogonality question (REVISE at pooled r=-0.53, missing baselines) — that thread is superseded per Director mandate. We preserve its distinctions as inherited state (Section 2) but do not re-test it.

---

## 2. Inherited State (from parent handoff EXP-PRODUCT-35697049382)

### 2.1 Established (must not be re-assumed beyond ceiling, but informs validity)

- Kernel `freshness_check` subprocess is wired into `src/spider/kernel.py` using real HTTP GET to `mechanism.freshness.probe_url` with Bearer token: behavioral_score 0.8 on 401/403 vs 0.0 on 200 at threshold 0.25 on localhost Flask 3.1.3 + PyJWT 2.14.0 + SQLite WAL mock (TP 1.0 on 45 drift samples, FP 0.0 on 60 noise samples, median latency 0.985ms). This is pipeline-existence evidence, not orthogonality evidence.
- Prior C-FRESHNESS orthogonality at delta=0.15 remains established ONLY from three stochastic mock PASS experiments: EXP-GRAPH-35353011131 (r=0.046 CI upper 0.135), EXP-GRAPH-35389145821 (r=0.002 CI upper 0.092), EXP-PRODUCT-35445596342 (r=-0.026 CI upper 0.064), each n=480. The kernel wiring experiment does NOT extend this ceiling.
- C-MEAS-VALID narrowly valid on localhost Flask/JWT (discrimination 0.833-1.0, null FP 0.0%, but full==body==status vacuous, deterministic CI degenerate). Distributed local correlation passing (stratified r≈-0.03 TOST p~2e-08) but distributed replication FALSIFIES on infrastructure C1 TN=0.667 per-node SQLite without replication.
- C-RESIDUAL-NOVELTY prior evidence is ONE doc survey EXP-INTEL-35651934683: M1 inflated 0.818→0.311 after correction (hardcoded instance_count=10 vs empirical 4.42), heuristic M2 estimates, tautological PC/NC, no dataset inspection, no cost measurement. Claim remains HYPOTHESIS. M3 novelty splits: Mind2Web has official instance splits but mechanism overlap across train/test not verified (audit VF6); WebArena has no official instance splits (M3 false, manual splits required). No experiment has measured cost vs novelty fraction.

### 2.2 Rejected (must not be assumed)

- Orthogonality at delta=0.15 in kernel wiring (pooled r=-0.53 CI [-0.61,-0.47], two-sided Fisher CI outside [-0.15,0.15], 28% shared variance) — rejected, anti-correlated not orthogonal. One-sided TOST alone is insufficient; variance gate C3 over combined A+B+C is artifact (0/3 on Phase-B-only would fail). Parallel-channel justification for kernel productization vs single-channel not established (baselines B-BEHAVIORAL-ONLY / B-STRUCTURAL-ONLY not executed).
- C-PRODUCT-ECON logistic extrapolation closed as REJECTED (L=0.5654 vacuous, 4 pts/3 params overfit, 5.42% thin margin, COLD 7.5x cheaper) — do not assume token economics viable without new direct measurement.
- WebArena-Verified v2 single-store MIXED result does not establish that SPIDER beats replay economics; TERX 0-token exact replay dominates at 0% novelty by construction.

### 2.3 Unknown (this experiment answers one of them)

- Whether later-agent cost tracks residual novelty vs full length and beats strong baselines amortized — this is the unknown under test. Also unknown: whether parameter-slot induction generalizes beyond single-char synthetic POC, whether staleness gating + UNKNOWN prevents contamination at 100% novelty, whether amortization over frequency rescues retrieval cost.

### 2.4 Do-not-assume (dangerous over-generalizations)

- Do not assume C-FRESHNESS validated/product-core — remains EXPERIMENTAL at localhost mock ceiling only.
- Do not assume ~1ms latency or TP 1.0/FP 0.0 generalize to production (localhost, deterministic mock, reduced N).
- Do not assume Mind2Web M1=0.818 — corrected 0.311 is the honest bound; do not assume WebArena M3 true (it is false without manual split).
- Do not assume TERX 90ms 0-token economics imply SPIDER has no value — the tension is exactly what the amortized novelty-fraction comparison must resolve.
- Do not import frontier TV/KDE rho=1.0 translation-only signal as evidence for Web dynamics or residual novelty — synthetic 2D [0,1]^2 only.

---

## 3. Hypothesis

**H1 (primary):** Later-agent cost under SPIDER parameterized inheritance (freshness gating + UNKNOWN abstention) is proportional to residual novelty fraction, not full task length.

Formally: `cost_SPIDER(n) = C_fixed + C_novel * n` where `n ∈ {0.0,0.25,0.50,0.75,1.0}` is the fraction of parameterizable identifier slots whose values were never observed during training on resource A (test on unseen B), `C_fixed` = retrieval (200 tok +150ms) + verification (50 tok +120ms), `C_novel` << `C_cold` (500 tok +2 calls per novel step). At `n=0.0` SPIDER cost is ≥60% cheaper than B-COLD (full-length) and within 2× of B-REPLAY-TERX (0-token replay cost ~90ms); at `n=1.0` SPIDER cost via UNKNOWN fallback is ≤1.10× B-COLD (no worse than cold). Spearman `rho(cost_SPIDER, n) ≥0.60` (p<0.01) and `R2_novelty - R2_full_length ≥0.15`.

**H2 (strong-baseline superiority):** SPIDER amortized cost per success beats B-RAG by ≥20% at `n=0.0` and `n=0.25` and beats B-INSTRUCTIONS by ≥15% at same bins, and beats B-REPLAY-TERX at any `n ≥0.25` (where exact replay misses). This demonstrates parameterized inheritance adds commercial value beyond retrieval and caching.

**Null (H0):** Cost is flat vs novelty (`rho≈0`) or SPIDER not cheaper than strong baselines at low novelty, indicating pay-full-task-length or no advantage over RAG/replay — the residual-novelty economics do not exist in this setting.

---

## 4. Design Overview

### 4.1 Task families (matched, constant full length)

- **Source:** WebArena-Verified shopping task family as template. If WebArena JSON fixtures are accessible locally (cached repo or `/tmp/webarena`), import shopping task intents + accessibility-tree fragments directly; otherwise use synthetic Flask catalog mock replicating WebArena shopping structure: 12 store instances sharing platform (per EXP-INTEL-35651934683 M1=1.0), 996-task structure, template-like parameterization (heuristic M2≈0.8). The chosen source is logged in `provenance.json`; either satisfies the Director's strategic question while avoiding Docker-hosting prerequisite flagged as dependency.
- **Structure:** Each task is a fixed-length `L=10` step workflow: `search(query) → filter(category) → open(product) → select(variant) → add_to_cart → checkout → verify`. Only identifier slots vary: `${sku}`, `${store_id}`, `${category}`, `${variant}`. Full length is constant by construction; only residual novelty varies. This isolates the novelty effect from length.
- **Training set (resource A):** 5 demonstrations per family on A identifiers (e.g., `A_SKU_001..050`, `A_STORE_01..06`) stored as observations. `distill_parameterized` induces one parameterized mechanism per family with slots `${sku}`, `${store_id}` (and possibly `${variant}`) via `_extract_varying_values` logic (field-path-relevant, structure-similarity ≥0.75, validated in EXP-PRODUCT-33741671686). Registry confidence 0.90. All training identifiers are disjoint from test B identifiers.
- **Test set (resource B, controlled novelty):** 5 bins ×20 tasks =100 SPIDER test tasks:
  - `n=0.00`: 100% identifiers from A set (exact repeat, but not exact trajectory replay because parameter binding still exercised)
  - `n=0.25`: 25% slots are unseen B values, 75% are A values
  - `n=0.50`: 50% unseen B
  - `n=0.75`: 75% unseen B
  - `n=1.00`: 100% unseen B (fully novel resource B, never-observed)
  - Assignment within bins is deterministic and stratified by position in workflow to avoid ordering confounds.

### 4.2 SPIDER system under test

- **Harness-level** (not yet kernel-integrated per audit: kernel.py `distill` is literal-only, parameterized logic lives in harness `run_experiment.py` per EXP-PRODUCT-33974562602). Registry holds the parameterized mechanism. At test time:
  1. `resolve(intent, context, params)` with test `params` (contains B identifiers for novel slots)
  2. Freshness gating: probe `mechanism.freshness.probe_url` if present (reuse Flask JWT mock from parent, HS256, same behavioral_score 0.8/0.0 threshold 0.25) — but catalog drift is not the focus; freshness is exercised as gating signal. If behavioral_score ≥0.25 → return `UNKNOWN` (abstain) rather than false accept.
  3. Confidence gating: if `best.confidence <0.80` → `UNKNOWN`
  4. If `UNKNOWN` → fallback to B-COLD simulated LLM cost for remaining novel steps (honest abstention, not contamination). If `EXECUTABLE` → `bound_action = _bind(action_template, params)` and verification step checks postconditions; on verification failure charge repair cost (1 LLM step).
- **Cost model (frozen proxy, no LLM keys):** Retrieval 200 tok +150ms, verification 50 tok +120ms (1 browser call), reused verified step 0 tok +0 calls, novel step 500 tok +2 browser calls (120ms each), repair 500 tok +2 calls. These constants are frozen before execution; sensitivity analysis varies tokens/step ±50% in report appendix. This proxies the Director-allowed simulated LLM / token-count proxy.

### 4.3 Baselines (identical 100-task set, identical proxy)

All baselines run on the same 100 tasks with same proxy:

- **B-COLD:** No memory. Every step is novel: cost = 10×500 tok +20 browser calls. Retrieval cost 0.
- **B-INSTRUCTIONS:** Instructions tokens amortized (200 tok once) + full exploration of identifier steps (still 10 novel steps, but instruction saves one reasoning step: 9×500 tok).
- **B-RAG:** Jaccard retrieval over prior A trajectories (TAU=0.30). If retrieved trajectory's identifier set matches test identifiers at ≥75% token overlap, replay matching steps at 0 cost; else fallback to B-COLD for mismatched steps. Retrieval cost 200 tok +150ms per task.
- **B-REPLAY-TERX:** Exact string equality on `action_template` (no parameterization). Hit iff test identifier sequence exactly equals a training trajectory. Hit cost 0 tok +90ms (verification call); miss cost = B-COLD. Hit rate = 100% at n=0.0, 0% at n=1.0, intermediate bins proportional to exact overlap.

### 4.4 Controls

- **PC1 (PC-PARAM-AND-REPLAY):** Exact-repeat TERX at n=0.0 must be 0 LLM tokens +~90ms and 100% success; SPIDER at n=0.0 on same A set must be EXECUTABLE with reused_actions ≥0.90. Failure → MEASUREMENT_INVALID.
- **NC1 (shuffled mapping):** Randomly permute learned slot→identifier mapping (e.g., `${sku}`↔`${store_id}`) before SPIDER resolve on same 100 tasks. Expect Spearman |rho|<0.25 p≥0.05 and success ≤ B-COLD.
- **NC2 (random retrieval):** SPIDER retrieval returns random registry entry instead of ranked match, UNKNOWN disabled. Expect false_accept ≥0.30 and flat cost vs novelty, proving ranking matters.

### 4.5 Sample size and power

- `n_SPIDER =100` paired cost-novelty observations gives >0.90 power to detect Spearman rho≥0.60 at α=0.01 (requires n≥44). Five bins of 20 give Wilson CI width ~±0.18 at 0.85 success per bin; aggregated 100 gives width ~±0.07. Baselines each also n=100.
- Bootstrap 5000 resamples stratified by novelty bin for 95% CI on cost ratios and rho. Two-sided tests throughout.

---

## 5. Metrics (stable IDs for result.json)

| ID | Definition | Unit |
|----|------------|------|
| `M-SUCCESS-SPIDER` | Success rate per novelty bin and overall for SPIDER (verified postconditions) | fraction |
| `M-SUCCESS-COLD`, `M-SUCCESS-RAG`, `M-SUCCESS-REPLAY`, `M-SUCCESS-INSTR` | Success rate per baseline | fraction |
| `M-FALSE-ACCEPT-SPIDER` | False accept rate: EXECUTABLE returned with wrong binding that fails verification / would cause wrong side effect | fraction |
| `M-UNKNOWN-RATE-SPIDER` | Abstention rate (UNKNOWN returned) per bin | fraction |
| `M-COST-TOKENS-SPIDER` | Sum proxy tokens per task (retrieval+verify+exec+repair) | tokens |
| `M-COST-BROWSER-SPIDER` | Browser calls per task | count |
| `M-COST-LATENCY-SPIDER` | Simulated latency per task (browser_calls*120ms + retrieval*150ms + token proxy at 2ms/token) | ms |
| `M-COST-AMORTIZED-SPIDER-f1`, `f10`, `f100` | Amortized cost per success at repeat frequency f=1,10,100: total amortized = (retrieval+distill amortized over f) + per-task exec, divided by success_rate | tokens / ms |
| `M-COST-*_COLD/RAG/REPLAY/INSTR` | Same cost metrics for each baseline | tokens / ms |
| `M-COST-RATIO-SPIDER-COLD-0pct` | Amortized SPIDER / COLD at n=0.0 | ratio |
| `M-COST-RATIO-SPIDER-REPLAY-0pct` | Amortized SPIDER / REPLAY at n=0.0 | ratio |
| `M-REUSED-ACTIONS-FRACTION-SPIDER` | Fraction of steps reused without LLM at n=0.0 | fraction |
| `M-SPEARMAN-RHO` | Spearman rho between M-COST-TOKENS-SPIDER and novelty_fraction | rho |
| `M-SLOPE-NOVELTY` | Linear regression slope cost_SPIDER ~ novelty_fraction | tokens per 100% |
| `M-R2-NOVELTY`, `M-R2-LENGTH` | R2 from cost~novelty and cost~full_length regressions | R2 |
| `M-R2-DELTA` | R2_novelty - R2_length | delta |
| `M-CORRELATION-NC-SHUFFLE` | Spearman rho for NC1 shuffled control | rho |

All metrics computed from raw per-task CSV `artifacts/raw_per_task.csv` (columns: task_id, novelty_fraction, system, success, false_accept, tokens, browser_calls, latency_ms, reused_steps, unknown).

---

## 6. Decision Rule (frozen)

**SURVIVES_CURRENT_TEST** requires **ALL** of (C1)–(C6):

- **C1 (correctness + abstention):** SPIDER `M-SUCCESS-SPIDER` at `n=0.0` ≥0.85 (Wilson 95% CI lower ≥0.72) and mean success across `n∈{0,0.25,0.5,0.75,1.0}` ≥0.80, with `M-FALSE-ACCEPT-SPIDER` ≤0.10 overall (freshness+confidence gating prevents contamination).

- **C2 (work compression vs cold and vs replay):** At `n=0.0`, `M-COST-RATIO-SPIDER-COLD-0pct` (amortized f=1) ≤0.35 (≥65% cheaper than full-length COLD). At `n=0.0`, `M-COST-RATIO-SPIDER-REPLAY-0pct` ≤2.0 (SPIDER within 2× of 0-token replay; beating replay not required at exact repeat). At `n=1.0`, `M-COST-AMORTIZED-SPIDER-f1` / `M-COST-AMORTIZED-COLD-f1` ≤1.10 (not more expensive than cold when fully novel, via UNKNOWN fallback).

- **C3 (novelty tracking):** `M-SPEARMAN-RHO` ≥0.60 with two-sided p<0.01 and bootstrap 95% CI lower >0.35, and `M-SLOPE-NOVELTY` >0 with p<0.01.

- **C4 (novelty explains cost, not length):** `M-R2-DELTA` ≥0.15, or equivalently `M-R2-NOVELTY` ≥0.30 given `M-R2-LENGTH` ≈0.00 (length constant L=10 by design; `M-R2-LENGTH` expected <0.02 and its CI upper <0.15 is reported).

- **C5 (beating strong memory baselines):** At amortized `f=10`, SPIDER cost per success beats B-RAG: `M-COST-AMORTIZED-SPIDER / M-COST-AMORTIZED-RAG` ≤0.80 at both `n=0.0` and `n=0.25`; and beats B-INSTRUCTIONS: ≤0.85 at same bins. Additionally SPIDER beats B-REPLAY-TERX at every `n≥0.25` (`cost_SPIDER < cost_REPLAY` at 0.25,0.50,0.75,1.00 at f=10).

- **C6 (controls):** PC1 `M-COST-TOKENS-REPLAY` at `n=0.0` =0 LLM tokens (verification calls only) and PC2 `M-REUSED-ACTIONS-FRACTION-SPIDER` at `n=0.0` ≥0.90 pass; NC1 `M-CORRELATION-NC-SHUFFLE` |rho|<0.25 p≥0.05 and NC2 random-retrieval false_accept ≥0.30 (or |rho|<0.25).

**FALSIFIED** if any C1–C6 fails (excluding substrate failures below).

**MIXED** if C1 passes but C3 or C4 fails: mechanisms are correct and low false-accept (so parameterization works) but cost is flat vs novelty (constant overhead dominates), indicating reuse without residual-novelty proportionality.

**MEASUREMENT_INVALID** if: (i) PC1 or PC2 fail due to harness binding/execution errors (success <0.50 at `n=0.0` for all systems, or binding error rate >0.20), (ii) NC1 spuriously shows |rho|≥0.35 p<0.05 indicating novelty label confounded with task difficulty, or (iii) infrastructure failure (registry write/read, Flask mock unreachable when used). These are recorded as `status=MEASUREMENT_INVALID`, not scientific falsification.

All recomputations use frozen `result.json` metric IDs and raw CSV.

---

## 7. Validity Threats and Mitigations

1. **Proxy vs real LLM economics:** Token/browser proxy is not real LLM latency/tokens. Mitigation: proxy values frozen and disclosed; sensitivity analysis varies tokens/step ±50% and browser latency ±50%; report whether SURVIVES is robust to proxy choice. This bypasses the LLM-key MEASUREMENT_INVALID that blocked two prior Product experiments per Director comparative reasoning.
2. **Synthetic vs WebArena-Verified DOM complexity:** Mock catalog or cached JSON lacks real DOM accessibility-tree complexity (800-element pages, truncation risk). Mitigation: disclose ceiling as synthetic/WebArena-inspired mock; do not claim cross-site transfer beyond this mock. Intel sample-level mechanism overlap verification and Runtime distributed replication remain prerequisites for scale-up (Director dependencies).
3. **Parameterization ceiling:** Harness-level `_extract_varying_values` is synthetic POC validated only on single-char/path+body tests; may not generalize to richer WebArena form fields. Mitigation: limit claim to slots `${sku}`, `${store_id}`, `${variant}` with disclosed heuristic; report slot induction success rate (slots induced / slots expected).
4. **Amortization assumption:** Retrieval/distill cost amortized over f=1,10,100 is analytical, not measured repeated use. Mitigation: report all three f values; do not claim commercial viability at f=1 alone; require f=10 advantage for C5.
5. **Length constant is artificial:** Fixing L=10 removes natural length variation, guaranteeing R2_length≈0. This is intentional isolation, but limits generalization to tasks where length and novelty co-vary. Mitigation: report that C4 is a best-case isolation test; follow-up experiment must co-vary length and novelty.
6. **Freshness gating not stressed:** Catalog mock has no real auth/session drift beyond parent Flask JWT probe. Mitigation: freshness gating exercised via probe but not the primary metric; its false_accept contribution is reported separately.
7. **Single family bias:** One catalog family may not represent WebArena diversity (one store platform). Mitigation: disclose as single-family bounded evidence; two-family replication is follow-up work.

---

## 8. Execution Plan (no outcome data inspected)

1. Freeze proxy constants, seeds, SKU sets, decision thresholds (this file + `spec.json` → `freeze.json`).
2. Generate training A set (50 SKUs, 6 stores) and 5×20 test B tasks at controlled novelty fractions; write fixtures to `fixtures/tasks.json`.
3. Build harness: `distill_parameterized` from A observations → registry; SPIDER resolve with gating; baseline implementations (COLD, INSTRUCTIONS, RAG, REPLAY) with identical proxy.
4. Execute 700 trials, write `artifacts/raw_per_task.csv`, `artifacts/registry.json`, `artifacts/cost_config.json`.
5. Compute metrics, bootstrap CIs, regressions, cost ratios per Section 5–6; write `result.json` with required top-level shape (`schema_version`, `experiment_id`, `lane`, `status`, `outcome`, `metrics`, `controls`, `artifacts`, `observations`, `validity_notes`, `unresolved`).
6. No LLM keys, no Docker, no browser automation required. Deterministic (`PYTHONHASHSEED=0`, `random.seed(42)`).

---

## 9. Product Consequences

- **If SURVIVES:** C-RESIDUAL-NOVELTY advances HYPOTHESIS→EXPERIMENTAL at bounded synthetic/WebArena-inspired mock ceiling (L=10 fixed, token proxy, n=100). Provides first direct evidence that cost tracks residual novelty and beats strong baselines amortized, unblocking C-PRODUCT-ECON scale-up to real LLM measurement and Docker full-DOM hosting. No PRODUCT_CORE promotion; replication with real LLM + production hosting required next.
- **If FALSIFIED / MIXED:** C-RESIDUAL-NOVELTY stays HYPOTHESIS (bounded REJECTED for proxy setting only). If flat cost (MIXED), investigate constant overhead. If not beating RAG/REPLAY, parameterized inheritance adds no economics beyond retrieval/caching — caching-vs-generalization prior upheld, redirect Product lane to C-FRESHNESS, C-DELTA-REPAIR, or C-SEMANTIC-RESOLVE. Prevents premature C-PRODUCT-ECON scale-up.
- **If MEASUREMENT_INVALID:** Fix harness/binding substrate (prior FALSIFIED filters) before re-testing economics.

---

## 10. Related Claims and Lanes

- **C-PARAM-INHERIT:** prior narrow single-char POC (EXPERIMENTAL) — this experiment tests its economic *consequence*.
- **C-PRODUCT-ECON:** closed logistic REJECTED — this experiment provides the missing direct cost-vs-novelty measurement that could justify reopening.
- **Dependencies:** Intel sample-level mechanism overlap verification, Graph parameterized reuse beyond single-char, Runtime header isolation / distributed replication — not prerequisites for this proxy-based isolation test, but prerequisites for follow-up scale-up (Director dependencies intel, graph, runtime).
- **Fresh-context transmission:** All identities (`experiment_id`, `claim_ids`, metric IDs `M-*`, control IDs `PC*`/`NC*`/`B-*`) are stable for EXECUTE→AUDIT→DIRECTOR.

---

## 11. Preregistration Integrity

No outcome-bearing measurement has been run. `spec.json` and this `prereg.md` are the frozen preregistration. Any change after `freeze.json` is exploratory. A new confirmatory claim requires a new experiment ID and untouched evidence. This design does not merely repeat the inflated M1=0.818 doc survey; it measures amortized end-to-end cost vs novelty fraction against the TERX 0-token replay + LLM fallback strong baselines that the Director flagged as mandatory.
