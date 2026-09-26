# EXP-INTEL-36272389571 — Execution Report

**Experiment ID:** EXP-INTEL-36272389571  
**Lane:** intel  
**Status:** COMPLETE  
**Outcome:** MIXED  
**Date:** 2026-09-26  
**Frozen inputs:** request.json, spec.json, prereg.md, freeze.json (immutable)

---

## Executive Summary

This experiment performed bounded, source-verified extraction of two decision-relevant facts from five deterministic-compilation systems per the Director mandate: (1) **ADDRESSING** — what binds a new task to a compiled artifact and the published error rate of that binding step; (2) **REGIME BOUNDARIES** — exact reported conditions for compiled-executor win/loss. The outcome is **MIXED**: C1 (open natural-language binding with published error rate) is satisfied by AgentJIT (Agentic Compilation), but C4 (runnability without LLM key/browser/docker) fails for 3 of 5 systems. All MV1-MV6 validity gates PASS. Positive and null controls PASS.

**Decision Rule Assessment:**
- C1_ADDRESSING_OPEN_NL: **SATISFIED** (AgentJIT achieves open NL binding, 80-94% compilation success)
- C2_REGIME_BOUNDARIES_EXTRACTABLE: **SATISFIED** (3+ systems: AgentJIT, TraceCompiler/Auto, Compiled AI)
- C3_COMPARABILITY_ASSESSED: **SATISFIED** (all 5 systems explicitly assessed vs SPIDER alias-OOD)
- C4_RUNNABILITY_VERIFIED: **NOT SATISFIED** (only 2/5 systems runnable without LLM key)
- C5_CONFLATION_FLAGGED: **SATISFIED** (all conflations explicitly identified)

Per frozen decision rule: C1 satisfied but C4 fails → **MIXED** outcome.

---

## 1. System-by-System Extraction Results

### 1.1 AgentJIT (arXiv:2604.09718 — "Agentic Compilation")

| Field | Finding |
|-------|---------|
| **ADDRESSING — Binding Mechanism** | One-shot LLM compilation from user intent (natural language) + DOM Sanitization Module (DSM) output → deterministic JSON workflow blueprint. Semantic selector hierarchy (ARIA roles, data-* attributes) over fragile positional paths. |
| **ADDRESSING — Error Rate** | Zero-shot compilation success: 80-94% across three modalities (Table 2: T1 Extraction 92%, T2 Form Filling 80%, T3 Fingerprinting 94%). HITL patching elevates to near-100% execution reliability. |
| **ADDRESSING — Abstention/Refusal** | "Ultra-low-cost models—specifically Gemini 2.5 Flash and Claude 3.5 Haiku—exhibited elevated failure rates... attributable to insufficient reasoning depth... excluded from Table 1 on the basis of systematic compilation failure rather than cost alone" (Section 4.2). |
| **ADDRESSING — Human Intervention** | HITL verification gate: operators "manually patch isolated failures—such as correcting a single misaligned semantic selector—in seconds" (Section 4.3). |
| **REGIME BOUNDARIES — Reuse Count** | Evaluated at M=500 executions of 5-step workflow (N=5). Architecture achieves O(M×N) → amortized O(1) inference scaling. |
| **REGIME BOUNDARIES — Witnessed-Determinism** | Not explicitly reported as fraction; deterministic execution assumed after compilation. |
| **REGIME BOUNDARIES — Novelty Rate** | Lazy replanning triggers on UI changes (structural mutations, A/B tests, framework updates) occurring "on macro-timescales, typically bi-annually or annually" (Section 5.2). |
| **REGIME BOUNDARIES — Task Length** | 5-step workflow (5 actions per profile) in evaluation. |
| **REGIME BOUNDARIES — Build Cost** | Per-compilation cost $0.002–$0.092 across five frontier models (Table 1). |
| **REGIME BOUNDARIES — Amortization** | Total inference cost $0.002–$0.10 for 500 executions vs $150 (unoptimized) / $15 (90% caching) for continuous agents. |
| **REGIME BOUNDARIES — Staleness/Maintenance** | Structural UI mutations bi-annually/annually. Lazy replanning handles selector healing. No explicit maintenance cost reported. |
| **Runnable Locally** | Requires LLM for compilation phase; execution runtime local (Playwright/Selenium). **NOT runnable without LLM key.** |
| **Task Distribution Comparability** | **INCOMPARABLE**: Live web automation (extraction/form-filling/fingerprinting on real sites) vs SPIDER's locally-served multi-endpoint HTTP with parameterized identifiers. Different: browser-required vs no-browser; DOM-based vs API-based; general web vs synthetic routing. |
| **Compilation-vs-Inheritance Conflation** | **CLEAN** — Pure compilation-bypass: one-shot LLM → JSON blueprint → zero-LLM execution. Lazy replanning is exception handling, not inheritance. |

**Key Quotes:**
- "Zero-shot compilation success rates of 80–94%" (Abstract)
- "Per-compilation costs between $0.002 and $0.092 across five frontier models" (Abstract)
- "HITL patching... elevate execution reliability to near-100%" (Abstract)
- "Cost reduction from O(M×N) to amortized O(1) inference scaling" (Abstract)

---

### 1.2 TraceCompiler per spec name = Auto (arXiv:2607.04542 — "Auto: The AGI Compiler")

| Field | Finding |
|-------|---------|
| **ADDRESSING — Binding Mechanism** | Records live agent behavior via SDK shims → determinism census (witnessed-deterministic fraction per span) → enumerative synthesis + LLM-guided CEGIS for deterministic parts → distillation for residue → differential replay verification → signed WebAssembly "cognition binaries" with manifests. |
| **ADDRESSING — Error Rate** | Determinism census: 87.1% of 560 spans witnessed-deterministic (Table 1). F1/F3/F4 = 100%; F2 = 77.5% (priority 92.5%, summarize 17.5%); F5 = 17.5%. F3 extraction: refused at all three rungs. F5 summarize: FAIL 17/40 = 42.5% << 800‰ threshold. |
| **ADDRESSING — Abstention/Refusal** | Conformal guards with abstention; "a failing contract never emits" (Section 4). Gate-refused recompilation under unfaithful deopt reference (Table 3, Leg B: 3 gate-refused). |
| **ADDRESSING — Human Intervention** | LLM judge for generative spans (spend-capped, ledgered). "Judged example with no judge supplied is Inconclusive, never silently exact" (Section 4). |
| **REGIME BOUNDARIES — Reuse Count** | Ratchet recompiles after K=8 new distinct inputs ingested (Algorithm 1). Three artifact generations over 300-item stream. |
| **REGIME BOUNDARIES — Witnessed-Determinism** | 87.1% pooled (560 spans); F1/F3/F4 = 100%; F2 = 77.5%; F5 = 17.5% (Table 1). |
| **REGIME BOUNDARIES — Novelty Rate** | Three scheduled distribution shifts in 300-item stream (shift 1: +security, shift 2: +onboarding, shift 3: +fraud phrasing). 56 distinct ticket texts across 300 positions. |
| **REGIME BOUNDARIES — Task Length** | Varies: F1 single call, F2 3-call pipeline, F3 field extraction, F4 policy routing, F5 summarization. |
| **REGIME BOUNDARIES — Build Cost** | "Total benchmark spend on the compiler side: $0.0621 against a pre-registered $5 cap" (Section 5 Setup). |
| **REGIME BOUNDARIES — Amortization** | Marginal cost 59→2 μ$/item (6.4x end-to-end) at 96.9% parity. Steady state 2.3 μ$/item vs 59 μ$/item control. Stream total 2,775 μ$ vs 17,692 μ$ control. |
| **REGIME BOUNDARIES — Staleness/Maintenance** | "Calibration and reference fidelity, not model capability, decide whether cheap stays correct" (Abstract). Loose guard (α=0.1) → 48.9% silent wrongness (133/272). Unfaithful deopt reference stalls ratchet. "Semantic embedding guards are the recorded upgrade" (Section 5.4). |
| **Runnable Locally** | Runtime execution requires no LLM (compiled wasm). Recording requires SDK shims + frontier model. Requires Rust toolchain + wasmtime. **NOT runnable without LLM key for recording.** |
| **Task Distribution Comparability** | **INCOMPARABLE**: Auto-Bench measures frontier-agent spans (ticket triage, inbox pipeline, etc.) vs SPIDER's synthetic 40-task alias-OOD (parameterized HTTP routing). Different: agent behavior compilation vs web navigation; recorded spans vs synthetic tasks. |
| **Compilation-vs-Inheritance Conflation** | **CONFLATION FLAGGED** — Records live agent behavior (inheritance/behavioral recording) then compiles. Ratchet continuously recompiles from new deopt traces. "Auto compiles *out of* interpretation into programs that no longer call a model" but recording phase IS inheritance. |

**Key Quotes:**
- "87.1% of 560 recorded frontier-agent spans are witnessed-deterministic (three of the four censused task families measure 100.0%)" (Abstract)
- "Marginal cost from 59 to 2 micro-dollars per item (6.4× end-to-end) at 96.9% parity on witnessed inputs with zero errors" (Abstract)
- "A loose guard silently mislabels 48.9% of compiled answers, and an unfaithful deopt reference causes the verification gate to refuse recompilation" (Abstract)
- "Calibration and reference fidelity, not model capability, decide whether cheap stays correct" (Abstract)

---

### 1.3 COVENANT per spec name = TraceCompiler (arXiv:2608.02680 — "TraceCompiler")

| Field | Finding |
|-------|---------|
| **ADDRESSING — Binding Mechanism** | Mines clusters of noisy agent traces → behavioral denoising → argument-level dependency verification (admits edge only when consumer argument contains value attributable uniquely to earlier producer) → provenance classification (constant, user_input, copy_edge, transform_edge, llm_or_dynamic) → executable workflows with typed nodes (START/END, TOOL, TRANSFORM, DECISION, LLM, HUMAN). |
| **ADDRESSING — Error Rate** | Mechanized rule: 0.928 precision, 0.943 recall over 15,775 def-use edges (training split). Compiler skill blind: 0.992 on 250 edges. AppWorld: 0.993 precision on 563 token edges. Venmo leave-one-out: passes 15/21 (failing fold escalates — required branch never observed). Spotify/Todoist: **CORRECTLY REFUSES TO COMPILE** (irreversible side effect under-determined). |
| **ADDRESSING — Abstention/Refusal** | Explicit refusal to compile when irreversible side effect under-determined (Spotify/Todoist). "Suspected" edges downgraded when exclusion fails — impose no ordering constraint. HUMAN node type specified but never emitted in case studies. |
| **ADDRESSING — Human Intervention** | Compiler skill is "a versioned instruction package a capable LLM agent loads and follows" — requires frontier LLM. "An LLM-driven compiler is not deterministic across runs or versions, so those results are one observation of a stochastic procedure, not reproducible constants" (Section 5). |
| **REGIME BOUNDARIES — Reuse Count** | Intent clusters require support floor of 5 traces. Median removable fraction 51.4% (IQR 41.9–74.1%) across 56 scenarios (14,128 calls). |
| **REGIME BOUNDARIES — Witnessed-Determinism** | Not directly measured as fraction. Venmo: tool calls 34→11, residual LLM node count = 1 (recipient-resolution branch). With deterministic rules substituted: 0 model invocations at runtime. |
| **REGIME BOUNDARIES — Novelty Rate** | Leave-one-out shows generalization fails when required branch never observed (1/7 for Venmo instance 2). "Structure from two executions suffices when those two exhibited the needed path and not otherwise." |
| **REGIME BOUNDARIES — Task Length** | Venmo: 34→11 calls (3, 3, 5 per instance). Spotify/Todoist: 106→59 logical activities (no executable count due to refusal). |
| **REGIME BOUNDARIES — Build Cost** | **"We measure call reduction but not offline compilation cost, so we claim no net efficiency result"** (Abstract). **NOT REPORTED.** |
| **REGIME BOUNDARIES — Amortization** | Not quantified (explicitly not claimed). |
| **REGIME BOUNDARIES — Staleness/Maintenance** | Not reported. "No compile/decline rate is reported over the 56 scenarios, and that rate... is the adoption-relevant number" (Section 6.3). |
| **Runnable Locally** | Requires frontier LLM for blind protocol/compilation skill. Mechanized rule/baselines model-free. Execution requires AppWorld simulator. **NOT runnable without LLM key.** |
| **Task Distribution Comparability** | **INCOMPARABLE**: AppWorld (9 apps, 457 APIs, 56 scenarios) and T1 (template travel dialogues) vs SPIDER's locally-served HTTP with parameterized identifiers. Different: API call traces vs HTTP routing; requires AppWorld simulator; multi-app coordination vs single-app routing. |
| **Compilation-vs-Inheritance Conflation** | **CONFLATION FLAGGED** — Mines from agent traces (behavioral recording): "Tool-using language-model agents repeatedly rediscover procedures they have already executed, producing traces that mix reusable structure with retries, exploration, accidental ordering, and repeated lookups" (Abstract). Compilation INPUT is inherited/recorded behavior. |

**Key Quotes:**
- "Mechanized form of the rule recovers producer–consumer dependencies at 0.928 precision and 0.943 recall over 15,775 def–use edges" (Abstract)
- "Venmo money-request intent reduces 34 observed API calls to 11 runtime calls and... passes 15 of 21, the failing fold escalating rather than acting because its required branch was never observed" (Abstract)
- "Spotify/Todoist intent the compiler correctly refuses to compile, because an irreversible side effect is under-determined" (Abstract)
- "We measure call reduction but not offline compilation cost, so we claim no net efficiency result" (Abstract)

---

### 1.4 Auto/AGI Compiler per spec = TSCG (arXiv:2605.04107) + Compiled AI (arXiv:2604.05150)

#### Part A: TSCG (arXiv:2605.04107 — "TSCG: Deterministic Tool-Schema Compilation")

| Field | Finding |
|-------|---------|
| **ADDRESSING — Binding Mechanism** | **Schema compilation, not task binding.** Deterministic tool-schema compiler converting JSON schemas → token-efficient structured text via 8 operators (TAS, CFL, CFO, SDM, DRO, CCP, CAS, SAD-F). Binds tool schemas to compressed representations at API boundary. |
| **ADDRESSING — Error Rate** | Not applicable as task-binding error rate. Accuracy: Phi-4 14B restored from 0% to 84.4% at 20 tools (90.3% at 50 tools). BFCL ARR 108–181% across 3 models. Format-vs-compression R²=0.88→0.03. |
| **ADDRESSING — Abstention/Refusal** | No abstention mechanism reported. Conservative vs balanced profiles recommended per model class (Table 6). |
| **REGIME BOUNDARIES — Build Cost** | Sub-millisecond execution, 1,200 LOC TypeScript, zero dependencies. "TSCG executes in <1 ms... LLMLingua-2 requires 42.5 s... ~40,000× slower" (Section 3.5). |
| **REGIME BOUNDARIES — Amortization** | Token savings 50–72% (52–57% on heavy production MCP schemas). Formal compression bound ≥51% on well-formed schemas (Theorem 3.1). |
| **REGIME BOUNDARIES — Staleness/Maintenance** | Not reported. "Toward a Community Schema Registry" discusses maintenance (Section 7.4) but no costs quantified. |
| **Runnable Locally** | **YES** — "1,200-line zero-dependency TypeScript package. Sub-millisecond execution. No model access, fine-tuning, or runtime search required" (Abstract). Fully runnable: no LLM key, no browser, no Docker. |
| **Compilation-vs-Inheritance Conflation** | **CLEAN** — Pure deterministic compilation of schemas. "TSCG is a *compiler*, not a search-based optimizer... same input always produces the same output. No model access is required" (Section 3.5). |

#### Part B: Compiled AI (arXiv:2604.05150)

| Field | Finding |
|-------|---------|
| **ADDRESSING — Binding Mechanism** | YAML workflow spec → Orchestrator selects templates/modules/prompt blocks → LLM generates business logic once → 4-stage validation (Security, Syntax, Execution, Accuracy) → validated Temporal activity deployed. |
| **ADDRESSING — Error Rate** | BFCL: 96% task completion (384/400); all 16 failures compilation-time (detectable pre-deployment). "Successfully compiled BFCL workflows execute with 100% reliability." DocILE Code Factory: KILE 80.0% (matching Direct LLM), LIR 80.4% (highest). |
| **ADDRESSING — Abstention/Refusal** | Validation pipeline catches failures; regeneration on failure. Security: prompt injection validator 95.8% recall, 100% precision; code safety gate 75% recall, 100% precision. |
| **REGIME BOUNDARIES — Reuse Count** | Break-even at n*≈17 transactions (BFCL). |
| **REGIME BOUNDARIES — Witnessed-Determinism** | Control-plane: 100% reproducibility, zero output entropy (H=0) over N=1,000 identical inputs. Runtime inference: 95% reproducibility. |
| **REGIME BOUNDARIES — Build Cost** | One-time 9,600-token generation cost. First compile: 57s (DocILE). |
| **REGIME BOUNDARIES — Amortization** | At 1K transactions: 57× token reduction vs Direct LLM, 84× vs AutoGen. At 1M transactions/month: TCO $555 vs $22,000 (40×). Latency: 4.5ms vs 2,004ms (450×). |
| **REGIME BOUNDARIES — Staleness/Maintenance** | "Bounded tool call drift... semantic drift in extracted values requires production monitoring... evaluation does not characterize this drift over long deployment horizons" (Limitations). Model updates may require re-validation. |
| **Runnable Locally** | Requires LLM for compilation; execution on Temporal. **NOT runnable without LLM key + Temporal.** |
| **Compilation-vs-Inheritance Conflation** | **MOSTLY CLEAN** — One-time generation from spec → deterministic execution. Code Factory uses bounded LLM tool calls at runtime for semantic subtasks, but orchestration compiled. No behavioral recording from prior executions. |

**Key Quotes (TSCG):**
- "Formal compression bound (≥51% on well-formed schemas)" (Theorem 3.1)
- "50–72% token savings" (Abstract)
- "BFCL ARR 108–181% across three models" (Abstract)
- "1,200-line zero-dependency TypeScript package... sub-millisecond" (Abstract)

**Key Quotes (Compiled AI):**
- "Break-even with runtime inference at approximately 17 transactions and reducing token consumption by 57× at 1,000 transactions" (Abstract)
- "450× latency reduction (4.5ms vs 2,004ms)" (Abstract)
- "TCO $555 vs $22,000 at 1M transactions/month (40×)" (Table 2)
- "96% task completion with zero runtime tokens" (Abstract)

---

### 1.5 TSCG (from prior packet EXP-INTEL-36249068574)

| Field | Finding |
|-------|---------|
| **Source** | Prior packet result.json metrics and report.md |
| **Formal Compression Bound** | ≥51% (tscg_formal_compression_bound: 0.51) |
| **Token Savings** | 50–72% (tscg_token_savings_min: 0.50, tscg_token_savings_max: 0.72) |
| **BFCL ARR** | 108–181% across 3 models (tscg_bfcl_arr_min: 1.08, tscg_bfcl_arr_max: 1.81) |
| **Models Tested** | 12 (tscg_models_tested: 12) |
| **API Calls** | ~19,000 (tscg_api_calls: 19000) |
| **Phi-4 14B Restoration** | 0% → 84.4% at 20 tools (90.3% at 50 tools) |
| **Runnable Locally** | **YES** — "Fully runnable locally — zero dependencies, no LLM API, no browser, no Docker. 1,200 LOC TypeScript package. Sub-millisecond execution." (Prior report.md) |
| **Compilation-vs-Inheritance** | **CLEAN** — Pure schema compilation, no behavioral recording. |

---

## 2. Control Results

### 2.1 Positive Control: PC-MV6-REPRODUCIBILITY — **PASS**

All MV6 no-memory deterministic executor parameters reproduced from primary sources with exact numerical agreement:

| Parameter | Prior Packet | This Extraction | Source |
|-----------|-------------|-----------------|--------|
| Compilation cost range | $0.002–$0.092 | $0.002–$0.092 | AgentJIT Table 1 |
| Hot-path latency | 18.2µs–4.5ms | 18.2µs (Node in-process) – 4.5ms (Compiled AI) | Auto Table 3, Compiled AI Table 1 |
| Token cost per repeat | 0 | 0 (TSCG, Compiled AI) | TSCG Abstract, Compiled AI Table 1 |
| Witnessed-determinism | 87.1% | 87.1% (560 spans) | Auto Table 1 |
| Abstention/refusal | Present | Auto gate-refused recompilation; COVENANT refuses under-determined; Compiled AI validation | Auto Table 3, TraceCompiler Section 6.1, Compiled AI Section 3 |

### 2.2 Null Control: NC-FABRICATED-BINDING-CLAIMS — **PASS**

Zero occurrences of all three fabricated claims across all five papers:
1. "zero-shot open-vocabulary goal resolution with <5% error rate" — **NOT FOUND**
2. "automatic cross-site transfer without any site-specific configuration" — **NOT FOUND**
3. "forgetting/staleness maintenance cost <1% of build cost" — **NOT FOUND**

---

## 3. Measurement Validity Gates (MV1–MV6)

| Gate | Requirement | Status | Evidence |
|------|-------------|--------|----------|
| **MV1** | Verbatim quote with page/section/figure/table from primary source | **PASS** | All extractions include exact quotes with section/table references (e.g., AgentJIT Table 1, Auto Table 1, TraceCompiler Abstract, TSCG Theorem 3.1, Compiled AI Table 1) |
| **MV2** | Runnable-locally verified by checking repo availability, dependencies, execution requirements | **PASS** | GitHub repos verified: RightNow-AI/auto (Rust, Apache-2.0), SKZL-AI/tscg (TypeScript, MIT), XY.AI Labs (Compiled AI). TSCG confirmed zero deps. |
| **MV3** | Task distribution comparability explicitly assessed vs SPIDER alias-OOD | **PASS** | All 5 systems assessed: all INCOMPARABLE on key dimensions (live web vs local HTTP, browser vs no-browser, DOM vs API, agent-behavior vs parameterized-routing) |
| **MV4** | Compilation-vs-inheritance distinction maintained; conflations flagged | **PASS** | AgentJIT: CLEAN; TraceCompiler/Auto: CONFLATION FLAGGED; COVENANT/TraceCompiler: CONFLATION FLAGGED; TSCG: CLEAN; Compiled AI: MOSTLY CLEAN; TSCG prior: CLEAN |
| **MV5** | Regime boundaries require explicit numerical thresholds | **PASS** | 3 systems with numerical thresholds; COVENANT explicitly states "claim no net efficiency result"; TSCG not applicable regime |
| **MV6** | Staleness/forgetting/maintenance explicitly reported or "not reported" | **PASS** | AgentJIT: bi-annual UI changes; Auto: 48.9% silent wrongness, calibration exposure; COVENANT: not reported; TSCG: not reported; Compiled AI: semantic drift monitoring needed |

**All MV1–MV6 PASS.** No MEASUREMENT_INVALID.

---

## 4. Decision Rule Outcome

| Condition | Status | Rationale |
|-----------|--------|-----------|
| **C1_ADDRESSING_OPEN_NL** | ✅ SATISFIED | AgentJIT achieves open NL goal resolution with published error rate (80–94% compilation success, 6–20% failure + HITL) |
| **C2_REGIME_BOUNDARIES_EXTRACTABLE** | ✅ SATISFIED | ≥3 systems (AgentJIT, TraceCompiler/Auto, Compiled AI) yield numerical thresholds with source quotes |
| **C3_COMPARABILITY_ASSESSED** | ✅ SATISFIED | All 5 systems explicitly assessed vs SPIDER alias-OOD |
| **C4_RUNNABILITY_VERIFIED** | ❌ NOT SATISFIED | Only 2/5 systems runnable without LLM key/browser/docker (TSCG paper, TSCG prior) |
| **C5_CONFLATION_FLAGGED** | ✅ SATISFIED | All conflations explicitly identified and categorized |

**Frozen Decision Rule Mapping:**
- SUPPORTS: C1∧C2∧C3∧C4∧C5 → **NO** (C4 fails)
- FALSIFIES: ¬C1 ∧ (¬C2 for ≥4/5) → **NO** (C1 satisfied, C2 satisfied)
- MIXED: (¬C1 ∧ partial C2–C5) ∨ (C1 ∧ ¬(C2∧C3∧C4∧C5)) → **YES** (C1 satisfied but C4 fails)
- MEASUREMENT_INVALID: Any MV1–MV6 fails → **NO** (all PASS)

**OUTCOME: MIXED**

---

## 5. Product Consequences

### Per MIXED Outcome (C1 satisfied but C4 fails):

**Addressing occupied but regime boundaries partially unavailable:**
- AgentJIT demonstrates open natural-language goal-to-artifact binding **with published error rate** (80–94% compilation success). This suggests SPIDER's differentiated component (semantic resolution without internal IDs) **may be partially occupied externally**.
- However, AgentJIT requires HITL patching for near-100% reliability and requires LLM for compilation. The "binding error rate" includes human-in-the-loop intervention.
- Regime boundaries extracted for 3 systems (AgentJIT, Auto, Compiled AI) but **COVENANT explicitly lacks build-cost/amortization data** and TSCG operates on different regime (schema compilation).
- **Only 2 of 5 systems are runnable without external dependencies** (TSCG variants), limiting direct verification.

**Implications for SPIDER lanes:**
- **Graph/Product**: C-SEMANTIC-RESOLVE remains load-bearing for *fully autonomous* open NL binding (AgentJIT requires HITL; others require behavioral recording or structured specs). The published error rate (6–20% + HITL) is a benchmark SPIDER must beat *without* human intervention.
- **Product**: Break-even measurements should target the regime where compilation wins per extracted boundaries: reuse count ≥17 (Compiled AI), witnessed-determinism ≥87% (Auto), task length 5+ steps (AgentJIT). But must test on SPIDER's alias-OOD, not external benchmarks.
- **Frontier**: Headroom decomposition should target regimes where witnessed-determinism >87% and reuse count >17, but must account for SPIDER's task distribution incomparability.
- **Intel**: Verification complete for this cycle. The architectural decision is informed but not settled: external open NL binding exists but with human intervention and incomparable task distributions.

---

## 6. Key Validity Threats

1. **Spec mapping inconsistencies**: System names in spec don't match paper titles (e.g., "TraceCompiler" → Auto paper; "COVENANT" → TraceCompiler paper; "Auto/AGI Compiler" → TSCG+Compiled AI). Analysis follows frozen spec exactly.

2. **TSCG appears twice**: Once as Auto/AGI Compiler source (arXiv:2605.04107), once as TSCG from prior packet. Same paper, treated as separate per spec.

3. **COVENANT explicitly lacks regime boundaries**: "We measure call reduction but not offline compilation cost, so we claim no net efficiency result" — build cost and amortization genuinely absent.

4. **AgentJIT error rate includes HITL**: 80–94% zero-shot; near-100% with human patching. The "published binding error rate" conflates compilation failure and human intervention.

5. **Runnability assessed from claims/repos, not execution**: GitHub repo inspection only (RightNow-AI/auto, SKZL-AI/tscg). Auto requires Rust/wasmtime; Compiled AI requires Temporal.

6. **All comparability assessments are INCOMPARABLE**: No external system evaluates on locally-served multi-endpoint HTTP with parameterized identifiers. SPIDER's task distribution is unique.

7. **Representation loss**: HTML versions may omit some PDF tables/figures. Extractions prioritized HTML-accessible content.

---

## 7. Unresolved Questions

1. Does AgentJIT's 6–20% failure rate (with HITL to near-100%) meet the Director's implicit threshold for "published binding error rate" making C-SEMANTIC-RESOLVE not load-bearing?

2. Is TraceCompiler (Auto) ratchet's 48.9% silent wrongness under loose calibration a fundamental bound or fixable? Agent-faithful configuration closes loop but requires faithful deopt reference.

3. What is COVENANT's (TraceCompiler) compile/decline rate over 56 AppWorld scenarios (the "adoption-relevant number" per paper)?

4. Does Compiled AI's semantic drift in bounded tool calls materially affect regime boundaries for mixed-content workflows over long horizons?

5. Does TSCG's 50–72% schema token savings translate to SPIDER's parameterized HTTP routing context?

6. What is the exact mapping between Auto's "witnessed-deterministic fraction" and SPIDER's "residual novelty rate"?

7. Does any external system achieve **fully autonomous** open NL binding (zero human intervention, zero behavioral recording)?

---

## 8. Evidence References

**Primary Sources (5 papers):**
- arXiv:2604.09718v2 — Agentic Compilation (AgentJIT per spec)
- arXiv:2607.04542v1 — Auto: The AGI Compiler (TraceCompiler per spec)
- arXiv:2608.02680v1 — TraceCompiler (COVENANT per spec)
- arXiv:2605.04107v1 — TSCG (Auto/AGI Compiler per spec, part A)
- arXiv:2604.05150v2 — Compiled AI (Auto/AGI Compiler per spec, part B)

**Prior Packet:**
- EXP-INTEL-36249068574 — result.json, report.md, handoff.json (TSCG metrics, MV6 baseline, cross-site evidence)

**Code Repositories Verified:**
- https://github.com/RightNow-AI/auto (Auto, Rust, Apache-2.0)
- https://github.com/SKZL-AI/tscg (TSCG, TypeScript, MIT)

**Frozen Inputs:**
- research/experiments/EXP-INTEL-36272389571/request.json
- research/experiments/EXP-INTEL-36272389571/spec.json
- research/experiments/EXP-INTEL-36272389571/prereg.md
- research/experiments/EXP-INTEL-36272389571/freeze.json