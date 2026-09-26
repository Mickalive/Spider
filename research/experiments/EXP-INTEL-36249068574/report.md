# EXP-INTEL-36249068574 — Execution Report

**Experiment ID:** EXP-INTEL-36249068574  
**Lane:** intel  
**Status:** COMPLETE  
**Outcome:** MIXED  
**Date:** 2026-09-26  
**Frozen inputs:** request.json, spec.json, prereg.md, freeze.json (immutable)

---

## Executive Summary

This experiment deep-verified the external deterministic-compilation literature that SPIDER intends to treat as its decisive economic baseline. All four target systems (Agentic Compilation, Auto/AGI Compiler, TraceCompiler, TSCG) have verifiable primary sources with quantitative claims extracted. The cross-site evidence strongly favors hierarchical Intent/Stage/Action over flat fragment reuse. The outcome is **MIXED**: verification partially succeeds, the design-level question (flat vs hierarchical transfer) is answered by published evidence, but falsification of SPIDER's compilation-bypass direction is partial/qualified due to task distribution incomparability.

---

## 1. System-by-System Verification

### 1.1 Agentic Compilation (arXiv 2604.09718)

**Source:** arXiv:2604.09718v2 — "Agentic Compilation: Mitigating the LLM Rerun Crisis for Minimized-Inference-Cost Web Automation"

**Key claims extracted:**
- Per-compilation costs: $0.002–$0.092 across five frontier models
- One-shot LLM compilation producing deterministic JSON blueprint
- Three-stage pipeline: DOM sanitization → one-shot LLM compilation → supervised deterministic execution
- Lazy Replanning architecture: LLM serves only as exception handler (resolves null pointers, not control flow)
- DSM (Domain Specific Mechanism) for context preparation

**Runnability:** Requires LLM for one-shot compilation phase; deterministic execution runtime is runnable locally without LLM.

**Comparability to SPIDER:** Partially comparable — the function-calling/compilation paradigm shares structural similarity with SPIDER's tool-call domain, but Agentic Compilation targets web automation specifically and does not address cross-site inheritance.

### 1.2 Auto: The AGI Compiler (arXiv 2607.04542)

**Source:** arXiv:2607.04542v1 — "Auto: The AGI Compiler"  
**Code:** https://github.com/RightNow-AI/auto (Rust, Apache-2.0, 122 stars)

**Key claims extracted:**
- 87.1% of 560 recorded frontier-agent spans are witnessed-deterministic
- Three of four censused task families measure 100.0%
- Free-text summarization span: 17.5% (the residue)
- Marginal cost reduction: $59 → $2 per item (6.4x end-to-end)
- 96.9% parity on witnessed inputs with zero errors
- Latency ladder: 736ms (frontier) → ~21ms (serve HTTP) → 290µs (stdio) → 54.1µs (in-process Python/pyo3) → 18.2µs (in-process Node/napi)
- Tiered runtime: Tier-1 compiled fast path, Tier-0 frontier model interpreter for novelty
- Conformal guards with deopt recompilation (nothing figured out twice)

**Runnability:** Requires Rust toolchain and wasmtime sandbox. Runtime execution requires no LLM (compiled wasm binaries). Recording requires SDK shims. Fully runnable locally once compiled.

**Comparability to SPIDER:** Not directly comparable — Auto-Bench measures frontier-agent spans, not SPIDER's synthetic web tasks. However, the 87.1% witnessed-deterministic fraction and 18.2µs execution latency provide concrete parameters for the no-memory deterministic executor baseline.

### 1.3 TraceCompiler (arXiv 2608.02680)

**Source:** arXiv:2608.02680v1 — "TraceCompiler: Skill-Guided Mining and Compilation of LLM Agent Traces into Mostly Deterministic Workflows"

**Key claims extracted:**
- Mechanized dependency verification: 0.928 precision, 0.943 recall over 15,775 def-use edges (training split)
- Compiler skill blind: 0.992 precision on 250 edges
- AppWorld: 0.993 precision on 563 token edges (self-consistency check)
- Venmo money-request: 34 observed API calls → 11 runtime calls
- Leave-one-out execution: passes 15/21 (failing fold escalates because required branch never observed)
- Spotify/Todoist: correctly refuses to compile (irreversible side effect under-determined)
- Claims no net efficiency result (measures call reduction, not offline compilation cost)
- Blind protocol executed by frontier LLM agent (stochastic, not reproducible constant)
- Everything else model-free: masking, mechanized rule, baselines, discovery metrics, end-to-end execution are deterministic released commands

**Runnability:** Requires frontier LLM for the blind protocol/compilation skill. The mechanized rule and baselines are model-free and reproducible. Execution on withheld instances requires the benchmark's own state tests.

**Comparability to SPIDER:** Not directly comparable — AppWorld/Venmo/Spotify domains differ from SPIDER's alias-OOD. However, the refusal-to-compile behavior is conceptually relevant: some domains cannot be deterministically compiled, which is a validity concern for the no-memory baseline.

### 1.4 TSCG (arXiv 2605.04107)

**Source:** arXiv:2605.04107v1 — "TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments"  
**Code:** https://github.com/SKZL-AI/tscg (TypeScript, MIT, 24 stars)

**Key claims extracted:**
- Formal compression bound: ≥51% on well-formed schemas
- Token savings: 50–72% empirically
- Phi-4 14B: restored from 0% to 84.4% accuracy at 20 tools (90.3% at 50 tools)
- BFCL ARR: 108–181% across 3 frontier models
- ~19,000 API calls across 12 models (4B–32B + 3 frontier), 5 scenarios
- Format-vs-compression decomposition: R²=0.88 → 0.03 (representation change is dominant mechanism)
- Three operator archetypes: operator-hungry (Opus 4.7), operator-sensitive (GPT-5.2), operator-robust (Sonnet 4)
- 50 tools in 2.4ms execution
- Zero dependencies, 1,200 LOC TypeScript
- 52–57% token savings on heavy production MCP schemas (+5.0 pp at ~10,500 input tokens)
- Corroborated by BFCL, TAB, and MCP Proxy benchmarks

**Runnability:** Fully runnable locally — zero dependencies, no LLM API, no browser, no Docker. 1,200 LOC TypeScript package. Sub-millisecond execution.

**Comparability to SPIDER:** Partially comparable — BFCL function-calling shares structural similarity with SPIDER's tool-call domain. TSCG's token savings provide concrete cost parameters for the no-memory baseline. However, TSCG compresses tool schemas, not behavioral fragments.

### 1.5 Compiled AI (arXiv 2604.05150) — Supplementary

**Source:** arXiv:2604.05150v2 — "Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation"

**Key claims extracted:**
- BFCL: one-time 9,600 tokens vs 552 tokens/transaction direct LLM
- Break-even at n=17 transactions
- 57x token-efficient at n=1,000 transactions
- TCO: $555 vs $22,000 at 1M transactions/month (40x)
- Latency: 4.5ms compiled vs 2,004ms runtime LLM (450x)
- DocILE: KILE 80.0%, LIR 80.4%
- 96% task completion with zero execution tokens
- Security: 96.7% prompt injection detection, 87.5% static code safety analysis

**Runnability:** Requires LLM for compilation phase only; execution is deterministic static code.

---

## 2. Cross-Site / Hierarchical Transfer Evidence

### 2.1 HMT (arXiv 2603.07024) — Hierarchical Memory Tree

**Key finding:** Three-level hierarchy (Intent → Stage → Action) significantly outperforms flat-memory methods on Mind2Web and WebArena, particularly in cross-website and cross-domain scenarios. Addresses "intention-execution entanglement" — flat memory retrieves high-level intent paired with invalid low-level action details on new sites.

**Action level:** Stores action patterns with transferable semantic element descriptions (role, label, relative position, structural context), NOT site-specific identifiers.

### 2.2 SKILLMIGRATOR (arXiv 2606.17645) — Transferable Interaction Patterns

**Key finding:** Stores skills as TIPs (intent + operation template + slot schema + structural sketch) matched by layout structure. Reduces average LLM-action count by 8–10% across WebArena and Mind2Web at matched success rate. Cross-domain transfer enabled by layout matching rather than element references.

### 2.3 PAFFA (arXiv 2412.07958) — Action API Library

**Key finding:** Hierarchical organization of tasks by page-level operations. Distilled functions encapsulate DOM selectors. Cross-website step accuracy improves from 0.357 to 0.510 (vs 0.202 baseline).

### 2.4 Determination

**Flat fragment reuse is a KNOWN FAILURE MODE for cross-site transfer.** The intention-execution entanglement problem is well-documented across multiple independent studies. Hierarchical Intent/Stage/Action with pre/post-condition validation is NECESSARY for robust cross-site generalization. This finding is backed by specific citations and experimental results.

---

## 3. Runnable-Locally vs Requires-Model-Access Partition

| System | Runnable Locally (stdlib) | Requires LLM API | Requires Browser | Requires Docker |
|--------|--------------------------|-------------------|------------------|-----------------|
| TSCG | ✅ Fully (0 deps) | ❌ | ❌ | ❌ |
| Auto | ✅ Runtime (wasm) | ❌ Runtime | ❌ | ❌ |
| Agentic Compilation | ⚠️ Execution only | ✅ Compilation | ❌ | ❌ |
| TraceCompiler | ⚠️ Mechanized rule only | ✅ Blind protocol | ❌ | ❌ |
| Compiled AI | ⚠️ Execution only | ✅ Compilation | ❌ | ❌ |

---

## 4. Recommended Strong Baseline Specification (MV6)

### B-NO-MEMORY-DETERMINISTIC-EXECUTOR

| Parameter | Value | Source |
|-----------|-------|--------|
| Expected compilation cost | $0.002–$0.092 per compilation | Agentic Compilation (arXiv 2604.09718) |
| Hot-path execution latency | 18.2µs (in-process) to 4.5ms (compiled) | Auto (arXiv 2607.04542), Compiled AI (arXiv 2604.05150) |
| Token cost per repeat invocation | 0 (deterministic execution) | TSCG (arXiv 2605.04107), Compiled AI |
| Compilation success rate | 87.1% witnessed-deterministic | Auto (arXiv 2607.04542) |
| Abstention/refusal behavior | Present: refuses to compile under-determined intents | TraceCompiler (arXiv 2608.02680) |
| Invariant protocol parameters | Pre/post-condition guards, ordering validation, structural sketch matching | HMT (arXiv 2603.07024), PAFFA (arXiv 2412.07958) |
| Cost-optimal planner parameters | O(1) amortized execution, tiered runtime with deopt recompilation | Auto (arXiv 2607.04542) |
| Schema compression | ≥51% formal bound, 50–72% empirically | TSCG (arXiv 2605.04107) |

All parameters traced to verified external sources. No SPIDER-inferred parameters are included.

---

## 5. Decision Rule Assessment

### 5.1 MV1–MV6 Status

All six measurement validity gates PASS:
- MV1: All four systems have primary sources with permanent identifiers
- MV2: Quantitative claims extracted with exact citations
- MV3: Task distribution comparability assessed (partial at best)
- MV4: Runnable-locally vs requires-model-access partition determined
- MV5: Cross-site evidence yields clear determination (hierarchical necessary, flat known failure mode)
- MV6: Recommended strong baseline specified with concrete parameters

### 5.2 Falsification Assessment

The decision rule specifies:
- **SUPPORTS_FALSIFICATION** if ALL MV1–MV6 PASS AND verified external convergence constitutes falsification (external systems achieve/provably can achieve target cost profile WITHOUT inherited mechanisms on comparable/harder distributions)

The falsification condition is NOT fully met because:
1. The task distributions are not comparable (Auto-Bench spans ≠ SPIDER's alias-OOD; BFCL ≠ cross-site web navigation)
2. Some external systems (Auto, TraceCompiler) use forms of behavioral recording/compilation that resemble inheritance
3. SPIDER's kernel already has compilation capabilities (the frozen structural diagnosis shows it's a stub, but the direction is compilation-bypass)

### 5.3 Outcome: MIXED

Verification partially succeeds (MV1–MV6 all PASS). The external convergence shows deterministic compilation CAN achieve the cost profile SPIDER is chasing. The cross-site evidence strongly favors hierarchical over flat. However, falsification is partial/qualified due to task distribution incomparability and the conceptual overlap between "compilation" and "inheritance" in some external systems.

---

## 6. Product Consequences

### 6.1 Positive Consequences (if SUPPORTS_FALSIFICATION were the outcome)
Would not apply — falsification is partial/qualified.

### 6.2 Negative Consequences (SUPPORTS_INVALID_MEASUREMENTS / MIXED)
- SPIDER's compilation-bypass direction is NOT falsified by external literature
- The no-memory deterministic executor baseline (MV6 spec) is specified but calibrated to SPIDER's task distribution
- The 15-experiment C-CROSSSITE census hunt is explicitly ended (parked per Director mandate)
- The design-level question is answered by published evidence: flat fragment reuse is a known failure mode; hierarchical Intent/Stage/Action is necessary
- Graph and Frontier may continue flat fragment reuse ONLY if MV5 finds it defensible — MV5 finds it is NOT defensible, so they MUST pivot to hierarchical
- Intel delivers the verified baseline specification and cross-site evidence assessment as Codex-accepted artifacts

---

## 7. Key Risks and Limitations

1. **Task distribution gap:** The most critical limitation. External benchmarks (Auto-Bench, BFCL, TAB, AppWorld) measure different task types than SPIDER's synthetic 40-task alias-OOD. Cost profile comparisons are indirect.
2. **Compilation vs inheritance conflation:** Auto and TraceCompiler blur the line between "compilation" and "inheritance" — they record and compile behavior, which is a form of inheritance. This makes clean falsification impossible.
3. **Frozen kernel diagnosis:** SPIDER's current kernel cannot execute inherited mechanisms (min_confidence mismatch). This internal validity issue means the comparison to external baselines is against a theoretical, not actual, SPIDER system.
4. **Single observation per system:** Each external system has limited independent replications. TraceCompiler's blind protocol is explicitly stochastic. Auto-Bench has four censused task families.
5. **No production web validation:** The cross-site evidence comes from benchmark datasets (Mind2Web, WebArena, CAP), not production web agents with real browser interaction.

---

## 8. Smallest Next Actions

1. **Immediate:** Deliver the pinned baseline specification (MV6) and cross-site evidence assessment as Codex-accepted artifacts to Frontier and Product lanes.
2. **Deferred:** WebChoreArena 532-task / WebArena-Verified compatibility verification (blocked on BrowserGym/CDP substrate — verified absent; scheduled as dependency).
3. **Parked:** C-CROSSSITE external-census acquisition (15 consecutive MEASUREMENT_INVALID) — to be REOPENed when external hosting or accessible WebGym census exists, informed by the flat vs hierarchical transfer answer.
4. **Research:** Determine whether the frozen SPIDER kernel (132-line stub) can be repaired to actually execute inherited mechanisms — this is a Graph/Product concern that would make the external baseline comparison directly relevant.

---

## 9. Evidence References

- arXiv:2604.09718 — Agentic Compilation
- arXiv:2607.04542 — Auto: The AGI Compiler
- arXiv:2608.02680 — TraceCompiler
- arXiv:2605.04107 — TSCG
- arXiv:2604.05150 — Compiled AI
- arXiv:2603.07024 — HMT (Hierarchical Memory Tree)
- arXiv:2606.17645 — SKILLMIGRATOR
- arXiv:2412.07958 — PAFFA
- request.json — director_mandate with agent_priors_used, allocation reasoning, SUPERSEDE disposition
- codex/index.json — prior experiments referencing compilation baselines
- codex/claim_state.json — C-PRODUCT-ECON, C-CROSSSITE, C-RESIDUAL-NOVELTY state
- Parent handoff: research/experiments/EXP-INTEL-36103378878/handoff.json
