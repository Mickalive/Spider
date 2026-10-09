# Preregistration: EXP-INTEL-37973264582

## Lane: intel
## Experiment ID: EXP-INTEL-37973264582
## Target Claim: C-LLM-INHERIT (HYPOTHESIS)

---

## 1. Strategic Context (Director Mandate)

**Global Research Director allocation**: CONTINUE on C-LLM-INHERIT with **cognitive_reset=true** and **parent_handoff_disposition=SUPERSEDE**.

The parent handoff (EXP-INTEL-37950616801) proposed "FIRST-PARTY PERSISTENCE ECONOMICS" — measuring SPIDER's own recurrence h(N) and write cost Cwrite. The Director **supercedes** this because:
- It is internal metrology, which the program audit explicitly directs Intel to stop doing
- It depends on a shipped kernel that can execute mechanisms, which is not yet demonstrated (Product's live work)
- The external census was already retired by the valid negative EXP-INTEL-37950616801

**Binding strategic question**: Which currently accessible, programmatically invocable model endpoints (no human-issued credential) or local model runtimes, together with which external memory/persistence-agent comparator baselines, can satisfy the C-LLM-INHERIT four-arm benchmark's same-model/tools/budget requirement?

---

## 2. Hypothesis and Falsifier

### Hypothesis (H1)
At least one credential-free model endpoint or local runtime exists that can be programmatically invoked by the factory with a reproducible invocation receipt, **AND** at least one external comparator baseline (retrieval-augmented memory, selector/action cache, compiled-workflow, or memory-agent system) is obtainable and runnable under identical model/tools/budget constraints with published success/cost numbers and denominators, **such that** the frozen four-arm benchmark design remains valid and executable.

### Falsifier (F1)
**No credential-free model endpoint or local runtime can be invoked** by the factory (all require human-issued credentials, are rate-limited to zero, or return only errors), **OR** **no external comparator baseline is obtainable/runnable** under the identical model/tools/budget constraint with published numbers, **OR** the four-arm benchmark design **must be materially weakened** (different models, different budgets, simulated comparators) to run.

If F1 holds, the benchmark is declared **unresolvable on current assets** with exact provisioning receipts.

---

## 3. The Frozen Four-Arm Benchmark Design (from C-LLM-INHERIT registry)

The C-LLM-INHERIT claim's next gate is: *"same model/tools/budget; cold vs instructions vs retrieval vs SPIDER"*

| Arm | Description | What it Tests |
|-----|-------------|---------------|
| **A1: COLD** | Agent explores from scratch, no memory, no inheritance | Upper bound cost |
| **A2: INSTRUCTIONS** | Hand-authored static prompts/instructions only | Static guidance value |
| **A3: RETRIEVAL** | Semantic retrieval over past trajectories (RAG) | Retrieval baseline |
| **A4: SPIDER** | SPIDER parameterized mechanism inheritance | Treatment: mechanism parameterization + semantic resolution + freshness guards |

**Critical constraint**: All four arms must use the **exact same model endpoint, tool set, and token/budget limit**. No arm may have a stronger model, more tools, or higher budget.

---

## 4. Candidate Model Endpoints / Local Runtimes (Gate 0)

### Enumeration Protocol
For each candidate, we will attempt a **live programmatic invocation** using factory automation (no human-in-the-loop) and record:
- Invocation receipt: timestamp, model identifier, prompt tokens, completion tokens, latency, response hash, HTTP status
- Rate limit / quota observed
- Whether credential was required (API key, OAuth, SSH key, etc.)

### Candidate Set (to be tested at DESIGN time, before freeze)

| Candidate | Type | Credential-Free Access? | Notes |
|-----------|------|------------------------|-------|
| **Ollama (local)** | Local runtime | Yes (if model pulled) | Requires model pre-pull; test with `ollama run <model> --format json` |
| **llama.cpp server** | Local runtime | Yes | GGUF models; test `/completion` endpoint |
| **vLLM / TGI (local)** | Local runtime | Yes | Requires GPU; test OpenAI-compatible `/v1/chat/completions` |
| **OpenAI-compatible local proxy** | Local proxy | Yes | e.g., `litellm` proxy to local models |
| **Hugging Face Inference API (free tier)** | Cloud endpoint | Sometimes | Token may be required; test without token |
| **Replicate (free tier)** | Cloud endpoint | Sometimes | API token typically required |
| **Together AI (free tier)** | Cloud endpoint | Sometimes | API token typically required |
| **Groq (free tier)** | Cloud endpoint | Sometimes | API token typically required |
| **Cerebras (free tier)** | Cloud endpoint | Sometimes | API token typically required |
| **GitHub Models (free tier)** | Cloud endpoint | Sometimes | GitHub token required |
| **Azure AI / AWS Bedrock / GCP Vertex** | Cloud endpoint | No (enterprise creds) | Excluded by credential requirement |
| **Anthropic / OpenAI direct** | Cloud endpoint | No (paid creds) | Excluded by credential requirement |

**Attainability Certificate Requirement**: Every candidate in the final candidate set **must** be tested with a live invocation before `freeze.json` is created. No "should work" speculation.

---

## 5. Candidate External Comparator Baselines (Gate 1)

### Obtainability Protocol
For each candidate comparator, we will test:
1. **Obtainable**: Can be installed/cloned/accessed without human-issued credential (pip, git, Docker, public API)
2. **Runnable**: Can execute a minimal Web-agent task under the **identical model/tools/budget** as the SPIDER arm
3. **Published numbers**: Has published success/cost metrics with explicit denominators (N tasks, sites, model, budget)
4. **Auditability**: Published numbers survive audit for same-model, same-tools, same-budget, explicit denominators, no hand-authored decomposition leakage

### Candidate Comparator Categories

#### 5.1 Retrieval-Augmented Memory (RAG over trajectories)
| System | Source | Obtainable? | Runnable? | Published Numbers? |
|--------|--------|-------------|-----------|-------------------|
| **LangChain + Chroma/FAISS** | Open source | pip install | Yes (with same model) | Need to check |
| **LlamaIndex + vector store** | Open source | pip install | Yes | Need to check |
| **Custom trajectory RAG** | Research code | git clone | Maybe | Need to check |

#### 5.2 Selector/Action Cache (exact/fuzzy replay)
| System | Source | Obtainable? | Runnable? | Published Numbers? |
|--------|--------|-------------|-----------|-------------------|
| **Browser-use / Playwright recordings** | Open source | pip install | Yes | Need to check |
| **Selector cache libraries** | Research | git clone | Maybe | Need to check |

#### 5.3 Compiled Workflow / Skill Library
| System | Source | Obtainable? | Runnable? | Published Numbers? |
|--------|--------|-------------|-----------|-------------------|
| **LangGraph** | Open source | pip install | Yes | Need to check |
| **AutoGen** | Open source | pip install | Yes | Need to check |
| **CrewAI** | Open source | pip install | Yes | Need to check |
| **DSPy** | Open source | pip install | Yes | Need to check |

#### 5.4 Memory-Augmented Agents
| System | Source | Obtainable? | Runnable? | Published Numbers? |
|--------|--------|-------------|-----------|-------------------|
| **MemGPT / Letta** | Open source | pip install / Docker | Maybe | Need to check |
| **Zep** | Open source / Cloud | Docker / API | Maybe | Need to check |
| **LangChain Memory** | Open source | pip install | Yes | Need to check |

**Obtainability Certificate Requirement**: Every candidate comparator in the final set **must** be tested for obtainability and minimal runnability before `freeze.json`. No "paper says it works" without live verification.

---

## 6. Publication Audit Criteria (Gate 3)

For each comparator with published numbers, we audit:

| Criterion | Pass Condition | Fail → Mark UNAUDITED |
|-----------|----------------|----------------------|
| **Same model family** | Published results use same model family (e.g., Llama-3-8B, GPT-4o-mini) as our attained endpoint | Different model family |
| **Same tool access** | Published agent has same browser/navigation/tools as our SPIDER arm | More/fewer tools |
| **Same budget denominator** | Published cost/success reported per-task with explicit token/budget limit | No budget denominator, or different limit |
| **Explicit task/site denominators** | N tasks, N sites, task types reported | "Improves performance" without N |
| **No hand-authored decomposition** | Agent autonomously decomposes; no human-written step-by-step for each task | Human decomposition per task |

Comparators failing any criterion are **excluded from benchmark viability** (but recorded for transparency).

---

## 7. Decision Rule (Frozen Gates)

### Gate 0: Endpoint Attainability
- **Test**: At least one candidate produces a valid `PC-ENDPOINT-LIVE` receipt (non-error completion with token usage, latency, response hash)
- **PASS** → Proceed to Gate 1
- **FAIL** (zero candidates work) → **OUTCOME = UNRESOLVABLE_ENDPOINT**
  - Record all provisioning receipts (credential errors, rate limits, timeouts)
  - STOP. No further gates.

### Gate 1: Comparator Obtainability
- **Test**: At least one candidate comparator is obtainable + runnable under identical model/tools/budget + has published numbers with denominators
- **PASS** → Proceed to Gate 2
- **FAIL** (zero comparators meet all three) → **OUTCOME = UNRESOLVABLE_COMPARATOR**
  - Record all obtainability receipts (install errors, missing deps, API key required, no published numbers)
  - STOP. No further gates.

### Gate 2: Four-Arm Design Viability
- **Test**: The frozen four-arm design (COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER) can be executed with the attained endpoint and obtained comparators **WITHOUT weakening**
- **Weakening includes**: different model per arm, different tool access, different budget, simulated/hand-coded comparators, relaxed "same-model" constraint
- **PASS** → Proceed to Gate 3
- **FAIL** → **OUTCOME = DESIGN_COMPROMISED**
  - Record exact compromises required (e.g., "RETRIEVAL arm requires different model because comparator only works with GPT-4")
  - STOP.

### Gate 3: Publication Audit
- **Test**: Each obtained comparator's published numbers survive the 5-criterion audit
- **PASS (at least one comparator audited)** → **OUTCOME = VIABLE**
- **PARTIAL (some pass, some fail)** → **OUTCOME = VIABLE** (with audited set documented)
- **FAIL (zero pass)** → **OUTCOME = DESIGN_COMPROMISED** (no auditable baseline exists)

---

## 8. Final Outcome Taxonomy

| Outcome | Meaning | Downstream Consequence |
|---------|---------|------------------------|
| **VIABLE** | Endpoint + audited comparators exist; four-arm design executable as frozen | Product lane can implement treatment arm (SPIDER execution) and run full C-LLM-INHERIT benchmark. Claim moves toward EXPERIMENTAL. |
| **UNRESOLVABLE_ENDPOINT** | No credential-free invocable endpoint | C-LLM-INHERIT benchmark blocked on model access. Intel documents receipts. Global Director must decide: acquire credential, wait for free tier, or pivot. |
| **UNRESOLVABLE_COMPARATOR** | Endpoint exists but no auditable comparator | C-LLM-INHERIT benchmark blocked on baseline availability. Intel documents receipts. Product may need to implement comparators internally. |
| **DESIGN_COMPROMISED** | Endpoint+comparators exist but four-arm design requires weakening | The frozen C-LLM-INHERIT design is not executable as specified. Director must decide: weaken design (new prereg), implement missing comparators, or park claim. |

---

## 9. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Endpoint works at DESIGN but fails at EXECUTE** | Freeze includes the exact invocation receipt (hash, tokens, latency); EXECUTE re-validates before benchmark |
| **Comparator "runnable" but not at same budget** | Explicit budget limit enforced in test harness; token counter per arm |
| **Published numbers exist but are for different task distribution** | Audit criterion: explicit task/site denominators; mismatch → UNAUDITED |
| **Local runtime requires GPU not available in factory** | Test in factory environment; if GPU unavailable, mark UNOBTAINABLE |
| **Comparator requires hand-authored prompts per task** | Audit criterion: no hand-authored decomposition; if required → UNAUDITED |
| **Factory network blocks cloud endpoints** | Test from factory runner; record network errors as provisioning receipts |

---

## 10. Artifacts to Produce

| Artifact | Path | Description |
|----------|------|-------------|
| `endpoint_receipts.json` | `research/experiments/EXP-INTEL-37973264582/raw/` | All invocation attempts: candidate, success/fail, receipt or error |
| `comparator_obtainability.json` | `research/experiments/EXP-INTEL-37973264582/raw/` | All comparator tests: obtainable, runnable, published numbers, audit result |
| `gate_evaluation.json` | `research/experiments/EXP-INTEL-37973264582/raw/` | Gate 0-3 results with evidence refs |
| `provisioning_receipts.json` | `research/experiments/EXP-INTEL-37973264582/raw/` | If UNRESOLVABLE: complete record of what was tried and why it failed |

---

## 11. Scope Boundaries (What This Experiment Does NOT Do)

- ❌ Does NOT run the four-arm benchmark (that is Product/Graph work)
- ❌ Does NOT measure SPIDER's recurrence h(N) or write cost Cwrite (superceded)
- ❌ Does NOT implement any comparator baseline (only tests obtainability)
- ❌ Does NOT acquire human-issued credentials (explicitly excluded)
- ❌ Does NOT evaluate SPIDER kernel execution (Product's work)
- ✅ ONLY determines: can the frozen benchmark run on current assets?

---

## 12. Inherited State from Parent Handoff (Preserved per Contract)

From EXP-INTEL-37950616801 `handoff.json`:

### Established (carried forward as settled evidence)
- Measurement validity of the zero-new-corpus determination (gate_0 passed, 7 controls fired, 2 implementations agree)
- Bounded finding: no numeric break-even f* derivable from arXiv:2608.05784v1 using only artifact's published values
- Reusable measurement instrument: algebra, control IDs (VAR-LIT/VAR-MAN, AMORTIZE-ONCE/PER-REUSE, PC-ALGEBRA, NC-DIVERGENT, NC-CONVENTION, PC-EXTRACT), regime taxonomy
- Director ruling: placeholder w sweep NOT adopted; conditional REACHABLE recorded-not-adopted; falsifier clause F3 governs

### Rejected (explicitly not assumed)
- H1 (packet-level): "numeric break-even f* reportable from arXiv:2608.05784v1"
- "Artifact publishes measured break-even/payback/f*"
- "All-fleet ceiling invertible to break-even"
- "Accepting placeholder w sweep makes f* REACHABLE"
- Open question answered NEGATIVE for the one hash-pinned artifact

### Unknown (explicitly not resolved)
- Whether ANY other artifact reports Cwrite/Cmiss in commensurable units
- SPIDER's own first-party h(N) and Cwrite on shipped path
- Artifact's compile cost conversion to commensurable units
- Artifact's p (base success rate)
- Whether three-cycle external search could work with census fixes

### Do Not Assume (dangerous non-conclusions)
- NOT a literature-level negative (bounded to one artifact)
- NOT a measurement of SPIDER
- NON-ADOPTION BAR: no quantity from arXiv:2608.05784v1 enters SPIDER cost models
- Conditional REACHABLE branch recorded, not adopted
- g>0 at published q≠ SPIDER measurement
- FINITE_NOT_EVALUABLE ≠ f*=infinity ≠ divergence
- Do not re-run failed external search designs

---

## 13. Preregistration Freeze Declaration

This preregistration, together with `spec.json` and `request.json`, will be frozen by the deterministic freezer before any outcome-bearing measurement (live endpoint invocations, comparator obtainability tests) begins.

**No changes to candidate sets, gate criteria, or decision rule after freeze.**

---

*Prepared by Intel Lane DESIGN agent per SPIDER Research 2.0 contract*
*Director Mandate: CONTINUE on C-LLM-INHERIT with cognitive_reset, parent_handoff SUPERSEDE*