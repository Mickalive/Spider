# EXP-INTEL-35651934683: Benchmark Structure Analysis for C-LLM-INHERIT

## Executive Summary

**Decision: SURVIVES_CURRENT_TEST** — At least one benchmark meets all three structural requirements for SPIDER's mechanism inheritance claims.

The frozen decision rule triggers SURVIVES_CURRENT_TEST:
- **M1 (Cross-Site Structure) ≥ 0.5**: PASS — WebArena shopping M1=1.0 (12 store instances), Mind2Web cross-website M1=0.82 (10 websites/domain)
- **M2 (Parameterization) ≥ 0.5**: PASS — WebArena shopping M2=0.8 (explicit templates), Mind2Web M2=0.65 (operation fields)
- **M3 (Novelty Fraction Measurable)**: PASS — Mind2Web provides official 3-way instance-level splits

**Top recommendation**: WebArena shopping + Mind2Web cross-website split together provide complementary strengths for C-LLM-INHERIT testing.

## Question

Which publicly available web-agent benchmark task families have structures that test SPIDER's inheritance claims: cross-site transfer potential (C-CROSSSITE), parameterized reuse potential (C-LLM-INHERIT), and controlled novelty fractions (C-RESIDUAL-NOVELTY)?

## Findings

### 1. WebArena Shopping (Primary: Cross-Site + Parameterization)

**M1=1.0, M2=0.8, M3=false, M4=0.0**

WebArena shopping is the strongest benchmark for cross-site structure and parameterized reuse:

- **12 store instances** share common action patterns: search, add-to-cart, checkout, filter
- **Explicit intent_template + instantiation_dict**: task definitions include parameterizable templates (e.g., `"tell me all subreddits starting with character '{{character}}'"` with `{"character": "a"}`)
- **996 tasks** across 12 instances provide high-density cross-site pairs
- **No official instance-level splits** (M3=false), but splits could be defined manually by store instance

This is the positive control: if WebArena shopping fails to show cross-site structure, no benchmark will.

### 2. Mind2Web Cross-Website (Primary: Novelty Fraction)

**M1=0.82, M2=0.65, M3=true, M4=0.53**

Mind2Web provides the best novelty fraction measurement:

- **137 real-world websites across 31 domains** with crowdsourced multi-step tasks
- **Official 3-way split**: train/test_task/test_website/test_domain by instance
  - test_website: 177 tasks on websites NOT seen during training (same domains)
  - test_domain: 912 tasks on entire domains NOT seen during training
- **Operations (CLICK/TYPE/SELECT)** have variable fields (element_id, input_value, select_value)
- **Cross-website pairs**: tasks on different websites in same domain share action patterns (e.g., "find flights" on kayak.com vs expedia.com)

This is the only benchmark with pre-defined instance-level splits enabling controlled novelty fraction measurement.

### 3. VisualWebArena (Secondary: Visual + Cross-Site)

**M1=1.0, M2=0.3, M3=false, M4=0.0**

VisualWebArena shares WebArena shopping instances but adds visual grounding:

- **521 shopping tasks** across 12 store instances (same as WebArena)
- **Visual requirement**: tasks require image understanding (SoM annotations, screenshots)
- **Lower M2 (0.3)**: visual tasks are less amenable to text-template parameterization
- Useful for testing whether mechanism transfer works with visual observations

### 4. AgentBench Web Component (Not Primary)

AgentBench's web browsing component is a Mind2Web subset; no independent benchmark structure. Not recommended as a primary benchmark for C-LLM-INHERIT.

### 5. External Systems Analysis

**HMT (Hierarchical Memory Tree)**: Most directly relevant to SPIDER's inheritance claims. Tests stage-level pre/post-condition matching on WebArena+Mind2Web. Achieves 38.7% task SR on WebArena, 39.7% step SR on Mind2Web cross-website. Its benchmark structure choices directly inform C-LLM-INHERIT experiment design.

**WebCoach**: Trajectory-level FAISS memory on WebVoyager. Tests memory reuse but NOT mechanism-level parameterized inheritance. 47%→61% improvement with 38B model.

**AgentRR**: Deterministic record-and-replay debugging. NOT relevant to mechanism inheritance. Exact replay, not transfer.

## Recommended Benchmark Structure for C-LLM-INHERIT

### Tier 1: Primary (use for experiment design)

| Benchmark | Task Family | M1 | M2 | M3 | Use Case |
|-----------|-------------|-----|-----|-----|----------|
| WebArena | Shopping (996 tasks, 12 stores) | 1.0 | 0.8 | false | Cross-site pairs + parameterized templates |
| Mind2Web | Cross-Website (177 tasks, 137 sites) | 0.82 | 0.65 | true | Novelty fraction measurement |

### Tier 2: Secondary (supplementary testing)

| Benchmark | Task Family | M1 | M2 | M3 | Use Case |
|-----------|-------------|-----|-----|-----|----------|
| VisualWebArena | Shopping (521 tasks, 12 stores) | 1.0 | 0.3 | false | Visual grounding + cross-site |
| WebArena | GitLab (196 tasks) | 0.0 | 0.5 | false | Multi-step complex tasks |

### Tier 3: Not recommended for C-LLM-INHERIT

| Benchmark | Reason |
|-----------|--------|
| AgentBench | Web component is Mind2Web subset; no independent structure |
| WebArena Wikipedia | Null control only (7 tasks, single site) |
| WebCoach/WebVoyager | Live web, no controlled splits |

## Positive Control

**PC1: WebArena Shopping** — PASS
- M1=1.0 (12 store instances with shared action patterns)
- M2=0.8 (explicit intent_template + instantiation_dict)
- If this failed, no benchmark would show cross-site structure

## Null Control

**NC1: WebArena Wikipedia** — PASS
- M1=0.0 (single instance, 7 tasks)
- M2=0.1 (no templates, no multi-step operations)
- Correctly identifies absence of cross-site and parameterization structure

## Product Consequences

### If Positive (DECISION = SURVIVES_CURRENT_TEST)

Intel provides Product lane with:
1. **Ranked benchmark task families** scored on cross-site structure, parameterization potential, and novelty fraction measurability
2. **Concrete C-LLM-INHERIT experiment design path**:
   - Train on WebArena shopping tasks across N store instances
   - Test on held-out store instances (cross-site transfer)
   - Use Mind2Web cross-website split for controlled novelty fraction measurement
3. **Transformation cost estimate**: WebArena adapter = 224 LOC (from EXP-INTEL-33925056324); Mind2Web provides raw HTML directly (0 LOC adapter)
4. **HMT alignment**: HMT's stage-level pre/post-condition matching on same benchmarks validates the structural approach

### If Negative (DECISION = FALSIFIED-IN-SETTING)

2-site corpus remains the practical bound for C-LLM-INHERIT, C-CROSSSITE, and C-RESIDUAL-NOVELTY. All mechanism claims remain untestable on diverse task structures.

## Scope

This is an Intel structural analysis experiment. It does NOT:
- Deploy Docker containers or run browser automation
- Execute LLM API calls
- Test SPIDER's kernel or fragment extraction
- Make claims about SPIDER's actual performance on benchmarks

It produces a ranked assessment of benchmark suitability that informs downstream experiment design.
