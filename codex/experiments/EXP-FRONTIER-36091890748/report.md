# EXP-FRONTIER-36091890748 Report — Frontier REOPEN: Deterministic Compilation Bypass Shootout for C-RESIDUAL-NOVELTY (Heterogeneous Live Gate)

**Lane:** frontier | **Claim:** C-RESIDUAL-NOVELTY | **Status:** MEASUREMENT_INVALID | **Outcome:** NOT_APPLICABLE

---

## Executive Summary

This experiment was a **Director-mandated REOPEN with `cognitive_reset=true`** (cycle 36091430101) to test the deterministic compilation bypass with invariant-enforcing protocol + cost-optimal planner against the 17-deep alias-catalog/routing/WebMCP tunnel (bounded at 21/40=0.525 pooled, 0/10 mixed, routing gain 0.0 p=1.0) and the validly falsified honest residual-novelty non-Pareto on synthetic TAU0.30 orthogonal gate (EXP-FRONTIER-36042599040: rho 0.4837 <0.60, ECE 0.216 >0.15, RAG dominance false, all 11 PCs/NCs PASS).

**The experiment is MEASUREMENT_INVALID due to substrate unavailability.** No live data was captured. All frozen positive controls (7) are NOT_RUN or FAIL; all null controls (8) are NOT_RUN; all baselines (6) are NOT_RUN. This is an infrastructure failure, **not a scientific falsification** of C-RESIDUAL-NOVELTY. The frozen spec explicitly mandates this diagnostic path: *"If BrowserGym/CDP or Intel diverse manifest unavailable or n_non304 stratified insufficient, declare live_available=false and MEASUREMENT_INVALID diagnostic without falsifying claim — do not substitute synthetic disjoint alphabets (36-family TAU0.30 fixture) as live evidence."*

The compilation/WebMCP shootout remains **UNTESTED on the live heterogeneous mixed triple-channel gate**. Prior valid bounded negatives on synthetic gates are preserved and not superseded.

---

## Frozen Design (Immutable)

### Primary Question
On heterogeneous WebArena-Verified Hard/WebGym triple-channel tasks (≥10 families Jaccard<0.30 product-subtree anchored 1280x720 CDP AX>10 mean>15 std>5 DOM≥2000, ≥40 pooled ≥10 mixed trajectory-grouped holdout) with honest per-trajectory hard-reset sum counters (resolve+bind+verify+freshness+browser_steps |rho_shuffled|<0.20 trajectory-grouped 5000 family-stratified bootstrap + 5000 block-permutation + 5000 global permutation), does **deterministic compilation bypass with invariant-enforcing protocol + cost-optimal planner** (TreeWalker 99% + stable locator ranking + deterministic JSON/Python DAG with pre/postcondition contracts + cost-optimal k-candidate planner penalizing LLM calls in loops + speculative guards & bailout fallback, <0.1ms hot path 0.09s vs 3-17s 0 tokens amortized $0.002-0.092) vs alias catalog+routing+hierarchical xMemory vs flat TFIDF-K5 vs WebMCP tool bypass achieve **honest M_total_f10/f100 Pareto dominance** (saving≥25% vs cold lower>15% p<0.05 strict dominance vs TFIDF and vs alias 0.525 portfolio at f10 and f100 robust to ±50% build, hot mean<200ms median<100ms 0 tokens, resolve+bind reduction≥40%, mixed 0/10→≥4/10 pooled≥0.60 Wilson lower≥0.45 gap≥0.07 vs alias, calibrated UNKNOWN precision≥0.85 false_accept≤0.10 ECE≤0.15 upper≤0.18)?

### Hypothesis (H1)
Deterministic compilation bypass with invariant-enforcing protocol + cost-optimal planner achieves honest Pareto dominance on heterogeneous mixed triple-channel tasks, breaking the alias 0.525 ceiling and the synthetic non-Pareto barrier.

### Falsifier (H0 - Bounded)
Even with invariant-enforcing compilation + cost-optimal planner and WebMCP tool bypass, economics remains non-Pareto or ceiling not broken (<4/10 mixed or pooled<0.60 or calibration fails or not Pareto vs alias/RAG/WebMCP at f10/f100) — bounded falsification for C-RESIDUAL-NOVELTY on this live gate.

### Decision Rule (Frozen)
**SURVIVES_CURRENT_TEST** iff ALL PCs PASS AND ALL NCs PASS AND:
- S1: M_total_COMPILE(f=10) ≤0.75×M_total_COLD (saving≥25% bootstrap lower>15% p<0.05) AND < M_total_ALIAS and < M_total_RAGk5 and < M_total_WEBMCP (CI lower>0) at f=10 AND same at f=100 with ±50% build sensitivity not inverting
- S2: compilation mixed ≥4/10 and pooled_coverage≥0.60 Wilson lower≥0.45 and gap vs alias 0.525 ≥0.07 p<0.05 and gap vs WebMCP ≥0.07
- S3: hot-path guard-pass mean<200ms median<100ms 0 tokens vs alias/RAG/WebMCP/cold median≥3000ms p<0.01, resolve+bind reduction≥40% vs alias, invariant contracts enforce ordering
- S4: UNKNOWN precision≥0.85 false_accept≤0.10 ECE≤0.15 upper≤0.18 and global |rho_shuffled|<0.20 p≥0.20 centered |mean|<0.05 std<0.15 gap rho - |rho_shuffled|>0.35, freshness TN≥0.85

**FALSIFIED-IN-SETTING** if PCs/NCs PASS but any S1-S4 fails.
**MEASUREMENT_INVALID** if any PC/NC fails OR substrate inadequate (manifest<10, pooled<40, mixed<10, n_non304 insufficient, BrowserGym/CDP missing, DOM<2000, AX≤10, within-family std=0, leakage 92-98%, |R|=1 degenerate).

---

## Substrate Diagnostics (Raw Evidence)

| Component | Status | Detail |
|-----------|--------|--------|
| **browsergym** | ❌ NOT INSTALLED | `importlib.util.find_spec("browsergym")` = False |
| **browsergym.core** | ❌ NOT INSTALLED | `importlib.util.find_spec("browsergym.core")` = False |
| **playwright** | ❌ NOT INSTALLED | `importlib.util.find_spec("playwright")` = False |
| **agentlab** | ❌ NOT INSTALLED | `importlib.util.find_spec("agentlab")` = False |
| **System chromium** | ✅ PRESENT | `chromium`, `chromium-browser`, `google-chrome` binaries found |
| **PyPI reachable** | ✅ YES | browsergym-core 0.14.3, playwright 1.63.0 installable in principle |
| **Intel diverse-site manifest** | ❌ ABSENT | No `research/intel/diverse_site_manifest.json`, no `data/webgym_292k`, no `data/webarena_verified`, no `data/webarena_verified_hard` |
| **Manifest families** | 0 | <10 required |
| **Jaccard mean/max** | null | Heterogeneity not measurable |
| **Runtime WAL** | ❌ ABSENT | `/tmp/spider-runtime/shared.db` does not exist |
| **X-Worker-Pid / n_non304** | N/A | No Runtime substrate to measure |
| **Pooled tasks** | 0 | <40 required |
| **Mixed triple-channel tasks** | 0 | <10 required |

**Frozen input integrity:** ✅ VERIFIED — request.json, spec.json, prereg.md hashes match freeze.json exactly. Parent handoff EXP-FRONTIER-36089506922 hash verified.

---

## Control Statuses (Frozen Identifiers Preserved)

### Positive Controls (7)

| Control ID | Status | Reason |
|------------|--------|--------|
| PC-COMPILATION-PIPELINE | NOT_RUN | No DOM/capture without BrowserGym + manifest |
| PC-HONEST-COST-SANITY | NOT_RUN | No trajectories captured |
| PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST | **FAIL** | manifest_families=0 <10, Jaccard null |
| PC-TRAIN-TEST-DISJOINT | NOT_RUN | No manifest/trajectories |
| PC-CALIBRATION-DERIVED | NOT_RUN | No live data |
| PC-BROWSERGYM-SUBSTRATE | **FAIL** | browsergym/playwright/agentlab absent, Runtime WAL absent, manifest absent |
| PC-WEBMCP-REGISTRY | NOT_RUN | Depends on BrowserGym/CDP + manifest |
| PC-FRESHNESS-GATED-BAILOUT | NOT_RUN | No trajectories captured |

**pc_all_pass: false** (2 FAIL, 5 NOT_RUN)

### Null Controls (8)

All 8 null controls: **NOT_RUN** — substrate dependent (no live data, no pipelines executed).

**nc_all_pass: false**

### Baselines (6)

All 6 baselines: **NOT_RUN** — substrate missing (no manifest, no BrowserGym, no Runtime WAL).

---

## Artifacts Produced

| Artifact | Path | SHA256 | Role |
|----------|------|--------|------|
| substrate_diagnostic.json | `artifacts/substrate_diagnostic.json` | `782ac225fd64abdefdb297937b7f5dfa2e3ac57e5718ff77afc721ee158b9a60` | raw |
| compilation_pipeline_check.json | `artifacts/compilation_pipeline_check.json` | `1000988012728cf42218dc8f318a70962684722356d9ea8749e704aa9966df0b` | raw |
| per_trajectory_traces.json | `artifacts/per_trajectory_traces.json` | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` | raw |
| honest_cost_audit.json | `artifacts/honest_cost_audit.json` | `ae9c50976326c6c805cde81b09f7ce64057756983425731dc0d5f3997c421cb8` | raw |

All artifacts are raw diagnostic evidence; no derived measurements or interpretations were generated because no live data exists.

---

## Prior Valid Bounded Negatives Preserved (Not Superseded)

1. **EXP-FRONTIER-36042599040** (audit PASS, all 11 PCs/NCs PASS): Honest residual-novelty economics **FALSIFIED-IN-SETTING** on synthetic 36-family TAU0.30 gate — rho 0.4837 CI[0.4102,0.5523] <0.60, ECE 0.216 >0.15, RAG dominance false at f10/f100. This remains a valid bounded negative on the synthetic orthogonal Jaccard 0.0 gate.

2. **EXP-FRONTIER-36052053591** (parent of parent, MEASUREMENT_INVALID, audit PASS): Alias ceiling **21/40=0.525** pooled Wilson [0.352,0.648] with routing gain 0.0 p=1.0, 0/10 mixed triple-channel. Compilation/WebMCP shootout untested.

3. **EXP-FRONTIER-36089506922** (immediate parent, MEASUREMENT_INVALID, audit PASS): Substrate diagnostic only. Compilation/WebMCP shootout remains untested on live heterogeneous gate.

---

## Validity Notes

1. **MEASUREMENT_INVALID is an infrastructure failure, not scientific falsification.** The frozen decision_rule explicitly gates SURVIVES/FALSIFIES on ALL PCs/NCs PASS + substrate adequacy. Substrate inadequacy triggers MEASUREMENT_INVALID per validity gate.

2. **No outcome-bearing measurements were run.** All controls/baselines correctly recorded as NOT_RUN or FAIL with explicit reasons. No data was invented.

3. **Synthetic TAU0.30 fixtures are explicitly forbidden as live evidence** per `spec.json measurement_validity[0]` and `prereg.md section 15`. Their presence is disclosed but they were never used.

4. **Agent priors from `director_mandate.agent_priors_used` are labeled general priors, not SPIDER evidence.** They cannot satisfy S1-S4 per the frozen contract.

5. **No representation loss for live data** (none captured). Synthetic TAU0.30 representation loss (disjoint alphabets, Jaccard 0.0 not natural 0.30-0.60 overlap) is disclosed in parent handoff `do_not_assume`.

6. **The compilation bypass shootout remains UNTESTED on the live heterogeneous gate.** This was the minimal orthogonal high-upside test outside the 17-deep alias tunnel, per Director rationale.

---

## Unresolved Questions (Carried Forward)

All questions from the frozen `prereg.md` and parent handoff `carry_forward.unknown` remain unresolved:

- Whether deterministic compilation bypass achieves honest M_total_f10/f100 Pareto dominance on live heterogeneous mixed triple-channel tasks
- Whether compilation breaks alias 0.525 ceiling via mixed triple-channel ≥4/10 success with pooled ≥0.60
- Whether hot-path guard-pass 0 tokens <200ms mean <100ms median Pareto holds
- Whether calibration achieves UNKNOWN≥0.85 false≤0.10 ECE≤0.15 with |rho_shuffled|<0.20
- Whether WebMCP tool bypass achieves competitive Pareto vs compilation
- Whether per-type CV stability, null centering, guard precision hold at ≥10-family live scale
- Whether larger Intel manifest or richer representations would change economics
- Whether Runtime health-gated n_non304≥360/800 can pass before distributed f=100 authorization

---

## Required Fixes for Valid Re-Execution

Per frozen `spec.json measurement_validity` and `prereg.md section 15`, the following substrate repairs are required before any valid test of S1-S4 can occur:

1. **Intel diverse-site manifest**: ≥10 families pairwise bigram Jaccard<0.30 mean<0.15 product-subtree anchored depth≥2 at 1280x720 CDP AX>10 mean>15 std>5 DOM≥2000, raw N≥500 ≥50/family, TRAIN-only vocab isolation 0 leakage, trajectory-grouped holdout (WebGym 292k dedup ≥50 eTLD+1 or WebArena-Verified Hard 192/36; reuse Hard258 where available).

2. **Runtime health-gated substrate**: Single-worker sticky Flask HS256+nginx WAL at `/tmp/spider-runtime/shared.db` with sticky cookie, If-None-Match/ETag TTL 60s conditional probes, n_non304≥360 single-node else ≥800 distributed stratified ≥80/family, X-Worker-Pid≥10, honest per-trajectory hard-reset sum counters.

3. **BrowserGym/CDP substrate**: browsergym-core 0.14.3 / playwright 1.63.0 / agentlab 0.4.2 pins; system chromium present; TreeWalker 99% fidelity, locator top-1 ≥95%, guard <5ms, WebMCP OpenAPI fetch ≥95%.

---

## Conclusion

**This experiment honestly reports MEASUREMENT_INVALID due to missing substrate.** It does not falsify C-RESIDUAL-NOVELTY. The Director-mandated REOPEN with `cognitive_reset=true` to test deterministic compilation bypass with invariant-enforcing protocol + cost-optimal planner on the heterogeneous live gate **remains unexecuted** pending substrate repair (Intel manifest, Runtime WAL, BrowserGym/CDP stack). The prior valid bounded negatives on synthetic gates (EXP-FRONTIER-36042599040, EXP-FRONTIER-36052053591) are preserved per the handoff contract.

The next valid execution requires the substrate repairs listed above. Until then, the compilation/WebMCP shootout remains UNTESTED on the live heterogeneous mixed triple-channel gate, and C-RESIDUAL-NOVELTY remains HYPOTHESIS per codex/claim_state.json.