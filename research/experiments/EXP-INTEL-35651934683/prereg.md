# EXP-INTEL-35651934683 preregistration

## Experiment Identity
- **Experiment ID**: EXP-INTEL-35651934683
- **Lane**: intel
- **Claims**: C-LLM-INHERIT, C-CROSSSITE, C-RESIDUAL-NOVELTY
- **Director Mandate**: PIVOT to C-LLM-INHERIT with cognitive reset

## Background and Rationale

The Director's portfolio assessment identifies SPIDER as being in a local-attractor phase: all six lanes carry tunnel_flag=true, six of ten claims have zero recent experiments, and the two most active claims (C-FRESHNESS, C-MEAS-VALID) are deep in measurement-validity refinement loops. The program has never tested its core product promise with real LLM API calls (C-LLM-INHERIT, C-PARAM-INHERIT blocked by infrastructure). The external landscape has shifted: TERX, HyperAgent, BrowserBash have commoditized exact-workflow replay. SPIDER's differentiation must be mechanism-level inheritance with formal freshness/drift guarantees.

The Director mandates a PIVOT from the closed truncation-artifact line (FALSIFIED in EXP-INTEL-35572177756) to benchmark structure analysis for C-LLM-INHERIT. The inherited parent_handoff's recommendation to investigate ranking degradation mechanisms is SUPERSEDED by this mandate.

## Question

Which publicly available web-agent benchmark task families have structures that test SPIDER's inheritance claims: cross-site transfer potential (C-CROSSSITE), parameterized reuse potential (C-LLM-INHERIT), and controlled novelty fractions (C-RESIDUAL-NOVELTY)?

## Hypothesis

At least one benchmark (WebArena, VisualWebArena, Mind2Web, or AgentBench) contains task families that are:
- (a) structurally runnable for SPIDER-style mechanism inheritance (not merely record-and-replay)
- (b) provide cross-site pairs sharing an action pattern across different site instances
- (c) allow controlled novelty fraction splits where training on a subset of task instances predicts performance on the remainder

Specific sub-hypotheses:
- **H1**: WebArena shopping/gitlab task families contain cross-site parameterized pairs (same mechanism, different store/project)
- **H2**: Mind2Web multi-step stateful tasks contain reusable action templates with parameterizable fields (form_submit, search, navigate patterns)
- **H3**: At least one benchmark supports train/test splits by task instance (not by site) enabling controlled novelty fraction measurement

## Falsifier

If:
- **F1**: NO benchmark among WebArena, VisualWebArena, Mind2Web, AgentBench contains task families where the same action mechanism operates across different site instances (cross-site pairs = 0)
- **F2**: All task families are single-step atomic actions with no reusable multi-step pattern (parameterized templates = 0)
- **F3**: All benchmarks use site-level train/test splits (not instance-level) making controlled novelty fractions impossible to measure

then the 2-site corpus remains the practical bound for C-LLM-INHERIT/C-CROSSSITE/C-RESIDUAL-NOVELTY and Intel should recommend alternative low-transformation-cost benchmark sources.

## Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B1-SPIDER-2SITE | Current SPIDER 2-site corpus (quotes + books) | Limited cross-site diversity (2 sites, 1-2 mechanisms each) |
| B2-TERX-HYPERAGENT | External record-and-replay systems (TERX, HyperAgent, BrowserBash) | Single-site, single-trajectory, no mechanism-sharing |
| B3-HMT-WEBCOACH-AGENTRR | Scout-identified systems relevant to SPIDER's inheritance claims | Test mechanism-level inheritance, benchmark structures inform C-LLM-INHERIT design |

## Controls

### Positive Control
WebArena shopping site type (996 tasks across 12 store instances): shopping tasks share common action patterns (search, add-to-cart, checkout) across different store instances, providing natural cross-site parameterized pairs. If this fails to show cross-site structure, no benchmark will.

### Null Control
WebArena wikipedia site type (single site, 7 tasks): Wikipedia tasks are site-specific Q&A with no cross-site mechanism sharing. Expected: 0 cross-site pairs, 0 parameterized templates.

## Scoring Metrics

For each benchmark × task family combination, compute:

### M1: Cross-Site Structure Score (0.0–1.0)
- Count of site instances sharing a common action mechanism
- Normalized by: (count - 1) / (max_expected_instances - 1)
- Threshold: >=0.5 indicates cross-site pairs exist

### M2: Parameterization Score (0.0–1.0)
- Fraction of task instances with at least one variable field (URL parameter, form input, search query) while the action pattern remains constant
- Threshold: >=0.5 indicates parameterized templates exist

### M3: Novelty Fraction Measurability (boolean)
- Can train/test splits be defined by task instance (not by site)?
- Requires: same mechanism appears in both train and test sets on different instances

### M4: Mechanism Reusability Index (0.0–1.0)
- Product of M1 × M2 × M3 (composite score)
- Higher = more suitable for SPIDER's mechanism inheritance testing

## Benchmarks to Survey

### Tier 1: Primary (publicly available, multi-site, structured tasks)
1. **WebArena** (812 tasks, 6 site types, Docker-based)
   - Shopping (996 tasks, 12 store instances)
   - GitLab (196 tasks)
   - Shopping Admin (182 tasks)
   - Reddit (114 tasks)
   - Map (112 tasks)
   - Wikipedia (7 tasks)

2. **VisualWebArena** (910 tasks, 3 visual grounding sites)
   - Shopping (521 tasks)
   - Reddit (298 tasks)
   - Classifieds (91 tasks)

3. **Mind2Web** (2350 tasks, 137 websites, crowd-sourced)
   - Cross-task generalization subset (90 tasks, 30 websites)
   - Cross-website generalization subset (90 tasks, 30 websites)
   - Cross-domain generalization subset (90 tasks, 30 websites)

### Tier 2: Secondary (may require special access or have limited structure)
4. **AgentBench** (842 tasks, 4 environments)
   - Web browsing tasks
   - Database tasks
   - Game tasks
   - OS tasks

### Tier 3: External Systems (published papers/repos, not full benchmarks)
5. **HMT** (Hierarchical Multi-step Task) — stage-level pre/post-condition matching
6. **WebCoach** — trajectory summarization + FAISS memory
7. **AgentRR** — record-and-replay with check functions

## Measurement Validity

1. Task definitions must be publicly accessible without Docker deployment or proprietary API access
2. Cross-site pairs must share an action mechanism (same abstract action pattern, different site instance) — not merely share a task category label
3. Parameterized templates must have at least one variable field while the action pattern remains constant
4. Novelty fraction splits must be definable by task instance (not by site)
5. Analysis must distinguish inherent structure vs imposed structure (e.g., WebArena's 12 stores are intentionally different stores sharing a platform)
6. External system analysis uses published papers/repos only

## Decision Rule

- **SURVIVES_CURRENT_TEST**: >=1 benchmark has cross-site score >=0.5 AND >=1 benchmark has parameterization score >=0.5 AND >=1 benchmark supports instance-level splits
- **MIXED**: (1) or (2) fails but (3) passes
- **FALSIFIED-IN-SETTING**: All three conditions fail
- **BLOCKED**: Infrastructure blocks access to >=2 benchmarks (with proof)

## Product Consequences

### Positive
Intel provides Product lane with ranked benchmark task families scored on cross-site structure, parameterization potential, and novelty fraction measurability. Product lane designs C-LLM-INHERIT experiments on highest-scoring families. Graph lane designs C-CROSSSITE experiments using identified cross-site pairs.

### Negative
2-site corpus remains practical bound. All mechanism claims remain untestable on diverse task structures. External commoditization continues without SPIDER differentiation.

## Scope

This is an Intel structural analysis experiment. It does NOT:
- Deploy Docker containers or run browser automation
- Execute LLM API calls
- Test SPIDER's kernel or fragment extraction
- Make claims about SPIDER's actual performance on benchmarks

It produces a ranked assessment of benchmark suitability that informs downstream experiment design.
