# Preregistration: EXP-INTEL-36272389571

## 1. Experiment Identity
- **Experiment ID**: EXP-INTEL-36272389571
- **Lane**: intel
- **Claim IDs**: C-PRODUCT-ECON, C-SEMANTIC-RESOLVE, C-CROSSSITE
- **Request Hash**: 9d7c48c6bcdc9436bff68e8bad412989cc628a5c381219b35bc3534d3c077dd1
- **Director Mandate**: CONTINUE on C-PRODUCT-ECON with SUPERSEDE of parent handoff
- **Cycle ID**: 36271679786

## 2. Strategic Question (from Director Mandate)

Resolve the conflation between **compilation** and **inheritance** in external deterministic-compilation systems by bounded, source-verified extraction of two decision-relevant facts:

### ADDRESSING
In each verified system (AgentJIT, TraceCompiler, COVENANT, Auto/AGI Compiler, TSCG):
- What exactly binds a new task to a compiled artifact: stable internal artifact id, selector/DOM inventory, typed tool schema, recorded trace signature, or **open natural-language goal resolution**?
- What published evidence bears on the **error rate** of that binding step, including abstention, refusal, or human-intervention numbers?
- *Critical*: Goal-to-mechanism resolution without internal ids is SPIDER's only component those systems do not obviously already possess.

### REGIME BOUNDARIES
For each system, the **exact reported conditions** under which a compiled/deterministic executor wins or loses:
- Reuse count threshold
- Witnessed-determinism fraction
- Novelty / residual-novelty rate
- Task length
- Build-cost and amortization accounting convention
- Any reported forgetting, staleness, or maintenance cost

**For every fact extracted:**
- Exact quoted number with source (page/section/figure/table)
- Whether artifact is obtainable and runnable with **no LLM key, no browser, no docker**
- Whether reported task distribution is comparable to **locally-served multi-endpoint HTTP application with parameterized identifiers** (SPIDER's synthetic 40-task alias-OOD)
- Explicit statement of what remains incomparable

## 3. Hypothesis

**H1 (Addressing)**: At least one of the five verified systems achieves goal-to-artifact binding via **open natural-language resolution** (not internal id, selector inventory, typed schema, or trace signature) with a **published binding error rate** (including abstention/refusal/human-intervention numbers).

**H2 (Regime Boundaries)**: For at least three of the five systems, the exact reported conditions for compiled-executor win/loss are extractable as **numerical thresholds** with explicit source quotes, enabling Product's break-even measurement and Frontier's headroom decomposition to target the regime where the answer is not already published.

## 4. Falsifier

**F1**: No verified system achieves open natural-language goal resolution with a published binding error rate (the binding step requires internal ids, selector inventories, typed schemas, or trace signatures in all five systems).

**F2**: The reported regime boundaries for compiled-executor wins are absent, incomparable to SPIDER's alias-OOD distribution, or conflated with compilation-vs-inheritance such that no clean break-even condition can be extracted for Product's economics and Frontier's headroom decomposition.

## 5. Target Systems (5 total, per Director Mandate)

| System | Primary Source(s) | Prior Intel Status |
|--------|-------------------|-------------------|
| **AgentJIT** | arXiv:2604.09718 | MV1-MV6 PASS (as "Agentic Compilation") |
| **TraceCompiler** | arXiv:2607.04542 | MV1-MV6 PASS |
| **COVENANT** | arXiv:2608.02680 | Not in prior MV1-MV6; new target per mandate |
| **Auto/AGI Compiler** | arXiv:2605.04107, arXiv:2604.05150 | MV1-MV6 PASS |
| **TSCG** | (from prior packet, fully local) | MV1-MV6 PASS; runnable locally with zero deps |

*Note: The prior packet covered four systems under MV1-MV6 (Agentic Compilation, Auto/AGI Compiler, TraceCompiler, TSCG). This packet adds COVENANT as the fifth system and re-extracts all five with the specific ADDRESSING and REGIME BOUNDARIES focus.*

## 6. Baselines (Frozen from Request)

### B-MV6-NO-MEMORY-EXECUTOR (Primary Baseline)
- **Source**: EXP-INTEL-36249068574 report.md Table 4
- **Parameters**: Compilation cost $0.002–$0.092; hot-path latency 18.2µs–4.5ms; token cost 0 on repeats; 87.1% witnessed-deterministic; abstention/refusal present
- **Role**: Strong baseline for Product/Frontier once kernel executable

### B-PRIOR-INTEL-EXTRACTIONS (Continuity Baseline)
- **Source**: EXP-INTEL-36249068574 result.json metrics MV1-MV6
- **Role**: Verify extraction reproducibility; detect drift

### B-CROSSSITE-HIERARCHICAL (Architectural Baseline)
- **Source**: EXP-INTEL-36249068574 established (arXiv:2603.07024, arXiv:2606.17645, arXiv:2412.07958)
- **Finding**: Hierarchical Intent/Stage/Action significantly outperforms flat fragment reuse on Mind2Web/WebArena/CAP
- **Role**: If inheritance continues, Graph/Frontier should pivot to hierarchical

## 7. Controls

### Positive Control: PC-MV6-REPRODUCIBILITY
- **Action**: Re-extract MV6 no-memory deterministic executor parameters from the same primary sources used in EXP-INTEL-36249068574
- **Expected**: All MV6 parameters match prior extraction within stated precision
- **Purpose**: Verify extraction procedure reliability; detect source drift

### Null Control: NC-FABRICATED-BINDING-CLAIMS
- **Action**: Search the five target papers for three fabricated claims that should not appear:
  1. "zero-shot open-vocabulary goal resolution with <5% error rate"
  2. "automatic cross-site transfer without any site-specific configuration"
  3. "forgetting/staleness maintenance cost <1% of build cost"
- **Expected**: Zero occurrences of these exact fabricated claims
- **Purpose**: Verify extraction procedure does not hallucinate positive findings

## 8. Measurement Validity Gates (MV1–MV6)

Every extracted fact must satisfy all six gates:

| Gate | Requirement | Failure Consequence |
|------|-------------|---------------------|
| **MV1** | Verbatim quote with page/section/figure/table from primary source (paper, tech report, official docs) — no secondary summaries | MEASUREMENT_INVALID |
| **MV2** | Runnable-locally verified by checking repo availability, dependency list, execution requirements — not inferred from paper claims | MEASUREMENT_INVALID |
| **MV3** | Task distribution comparability explicitly assessed against SPIDER's synthetic 40-task alias-OOD (locally-served multi-endpoint HTTP with parameterized identifiers) — state matching and non-matching dimensions | MEASUREMENT_INVALID |
| **MV4** | Compilation-vs-inheritance distinction maintained: recording/compilation using behavioral traces or LLM generation is NOT "compilation-bypass" — flag every conflation | MEASUREMENT_INVALID |
| **MV5** | Regime boundaries require explicit numerical thresholds (reuse count, novelty rate, task length, build cost) — qualitative statements insufficient | MEASUREMENT_INVALID |
| **MV6** | Staleness/forgetting/maintenance costs explicitly reported in source — absence recorded as "not reported" not "zero" | MEASUREMENT_INVALID |

## 9. Decision Rule (Frozen from Director Mandate)

| Outcome | Conditions |
|---------|------------|
| **SUPPORTS** | C1 AND C2 AND C3 AND C4 AND C5 all satisfied |
| **FALSIFIES** | C1 fails AND C2 fails for ≥4/5 systems |
| **MIXED** | C1 fails but C2–C5 partially satisfied; OR C1 satisfied but C2–C5 fail |
| **MEASUREMENT_INVALID** | Any MV1–MV6 gate fails |

Where:
- **C1_ADDRESSING_OPEN_NL**: ≥1 system achieves open NL binding with published error rate
- **C2_REGIME_BOUNDARIES_EXTRACTABLE**: ≥3 systems yield numerical regime boundaries with source quotes
- **C3_COMPARABILITY_ASSESSED**: Every regime boundary has explicit comparability statement to SPIDER's alias-OOD
- **C4_RUNNABILITY_VERIFIED**: Every system has verified runnability (no LLM key, browser, docker)
- **C5_CONFLATION_FLAGGED**: Every compilation-vs-inheritance conflation explicitly flagged

## 10. Product Consequences

### If SUPPORTS (C1 true)
- C-SEMANTIC-RESOLVE is **NOT** the load-bearing investment
- External systems already occupy SPIDER's differentiated component (open NL goal→artifact binding)
- Graph and Product should **converge toward compilation-based architectures**
- Product's break-even and Frontier's headroom target the regime where compilation wins (per extracted boundaries)
- Intel verification complete for this cycle

### If FALSIFIES (C1 false AND C2 largely unavailable)
- C-SEMANTIC-RESOLVE **IS** the load-bearing investment
- No external system achieves open NL binding with published error rate
- Binding requires internal ids/selectors/schemas/traces with published error rates SPIDER must beat
- Product's economics and Frontier's headroom must test SPIDER's inheritance against **MV6 no-memory executor** on SPIDER's alias-OOD
- Graph must invest in semantic resolution with abstention calibration
- Architectural decision made: inheritance path is differentiated

### If MIXED
- Partial regime boundaries extracted but addressing gap remains (C1 false, C2–C5 partial) → Product/Frontier get partial aiming data; Graph/Product still need semantic resolution investment
- Addressing occupied but regime boundaries unavailable (C1 true, C2–C5 fail) → Convergence indicated but targeting unresolved; Intel may need follow-up

## 11. Scope and Exclusions

### In Scope
- 5 target systems × 2 fact categories (ADDRESSING + REGIME BOUNDARIES) = 10 primary extraction targets
- Source verification for runnability (repo check, dependency audit)
- Comparability assessment against SPIDER's synthetic 40-task alias-OOD
- Compilation-vs-inheritance conflation flagging

### Out of Scope
- Reproducing any system end-to-end (requires absent browsergym image / LLM key)
- WebArena / WebChoreArena evaluation (blocked on absent substrate)
- xMemory on LongMemEval-V2 (requires model access)
- C-CROSSSITE external census acquisition (parked per Director mandate — 15 consecutive MEASUREMENT_INVALID, requires external hosting)
- Kernel repair (Product/Graph responsibility, superseded per Director mandate)

## 12. Evidence Preservation

All extractions recorded as:
```json
{
  "system": "AgentJIT|TraceCompiler|COVENANT|Auto/AGI Compiler|TSCG",
  "fact_category": "ADDRESSING|REGIME_BOUNDARIES",
  "fact": "exact description",
  "verbatim_quote": "exact text from source",
  "source_location": "paper:section:figure:table or doc:url",
  "extracted_value": "numerical value or categorical",
  "runnable_locally": true|false,
  "runnability_evidence": "repo URL, dependency list, execution command",
  "task_distribution_comparability": "matches on X, differs on Y, incomparable on Z",
  "compilation_vs_inheritance_conflation": "flagged|not_applicable|clean",
  "staleness_maintenance_reported": "value|not_reported"
}
```

## 13. Estimated Cost
- **Human hours**: 8 (source reading, extraction, verification, comparability assessment)
- **Compute**: Negligible (no code execution, only source retrieval)
- **External dependencies**: arXiv access for 5 papers + official documentation/repositories for runnability verification

## 14. Expected Information Gain
**High** — This is the minimal high-information experiment that resolves the single highest-leverage external fact (addressing mechanism + error rate) redirecting Graph and Product budgets, while extracting regime boundaries that aim Product/Frontier measurements at the unresolved regime. The Director identified this as "the highest-leverage verification available" that "breaks a fifteen-experiment tunnel."

## 15. Predecessor State (Inherited from Parent Handoff)

### Established (Carry Forward)
- MV1-MV6 PASS for 4 systems with verifiable sources and quantitative claims
- MV6 no-memory deterministic executor baseline specified with concrete parameters (Table 4)
- Cross-site evidence: hierarchical > flat on Mind2Web/WebArena/CAP (3 papers)
- Runnable-locally partition determined (TSCG fully local; Auto runtime local; others require LLM for compilation only)
- C-CROSSSITE acquisition thread parked (15 consecutive MEASUREMENT_INVALID)

### Rejected
- Flat fragment reuse as defensible level for cross-site transfer on benchmark distributions
- Global "flat fragment reuse is known failure mode" beyond screened benchmarks

### Unknown
- Task distribution comparability between external benchmarks and SPIDER's alias-OOD (MV3 PARTIAL)
- Whether external compilation systems constitute "without inherited mechanisms" (conflation)
- Whether SPIDER kernel can execute inherited mechanisms
- Cross-site evidence validity on production web agents with real browser
- Exact Auto per-compilation overhead in production
- Generalizability of TraceCompiler refusal behavior
- Precision of MV6 parameters to SPIDER's task distribution

### Do Not Assume
- Task distributions are comparable
- External convergence falsifies SPIDER's direction
- SPIDER kernel is executable (min_confidence mismatch: distill returns 0.5, min 0.8)
- "Compilation" = "bypass" (distinguish recording/compilation from pure bypass)
- Cross-site finding generalizes beyond benchmark datasets
- Single-point estimates are bounds with uncertainty
- Retry C-CROSSSITE census without external hosting/WebGym census

## 16. Dependencies (from Director Mandate)

- **Graph**: Published binding-error rate sets threshold C-SEMANTIC-RESOLVE must beat
- **Frontier**: Regime boundaries determine novelty rate and reuse count for headroom decomposition
- **Product**: If compilation externally dominates in Product's cost regime, promotion case for inheritance layer weakens
- **Deferred** (not scheduled): AgentJIT/TraceCompiler/COVENANT on WebArena/WebChoreArena, xMemory on LongMemEval-V2 — blocked on browsergym image and model access
- **Parked**: C-CROSSSITE external census acquisition

---

*This preregistration is frozen upon creation. No outcome-bearing measurements may be taken during DESIGN. The frozen spec.json and this prereg.md constitute the immutable design for EXECUTE.*