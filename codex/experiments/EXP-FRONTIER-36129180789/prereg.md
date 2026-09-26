# EXP-FRONTIER-36129180789 Preregistration
## Frontier Lane — C-RESIDUAL-NOVELTY (Pay Novelty, Not Length)
## Global Director Mandate: PIVOT with cognitive_reset=true, SUPERSEDE parent

---

### 1. Executive Summary

This experiment tests SPIDER's **central premise** against the **strongest available null**: a no-memory deterministic executor compiled from the current observation alone.

**Director Mandate (binding):**
> "The decisive question SPIDER has never asked is whether inheritance is needed at all. Every prior design compared inheritance against cold, instructions and retrieval, but never against a deterministic executor that has no memory and derives its plan from the current observation... If that no-memory executor matches inherited execution at matched correctness and equal cost, then C-RESIDUAL-NOVELTY, C-PRODUCT-ECON and the compilation priors are jointly moot and the architecture must change. That is a null against SPIDER's own premise, which is the highest-upside falsification available and exactly Frontier's charter. It is also reachable: it needs a real service and two executors, not a public-Web corpus and not a policy model."

**Parent Handoff Disposition:** SUPERSEDE. The prior WebChoreArena heterogeneous shootout (EXP-FRONTIER-36103384192) was MEASUREMENT_INVALID due to substrate unavailability (BrowserGym, Runtime WAL, Intel manifest, Graph freshness all unavailable). The synthetic 36-family Jaccard 0.0 gate was validly FALSIFIED (rho=0.4837 CI[0.410,0.552] < 0.60, ECE=0.216 > 0.15, RAG dominance false) but is **bounded to synthetic disjoint alphabets only** — explicitly forbidden as substitute for live heterogeneous evidence.

---

### 2. Scientific Question

> Does inherited execution actually pay for itself against a no-memory deterministic executor, when both are held to identical verification and identical honest non-token work accounting?

**Operationalized:** On matched task families with controlled novelty fractions, using a paired within-task design (identical starting state for both executors), does the inherited-mechanism executor reduce observation + network request + verification work relative to the no-memory executor by an amount that tracks **residual novelty** (ρ ≥ 0.60, bootstrap lower > 0.40, p < 0.05) rather than **full task length** (|ρ| < 0.20 pooled, |ρ| < 0.20 per stratum with upper < 0.30), with an inheritance-ablation arm (emptied registry) as the mandatory null?

---

### 3. Hypothesis

**H1 (Primary):** Inherited execution with SPIDER's populated registry reduces honest per-trajectory work (resolve + bind + verify + freshness + network + browser steps) compared to a no-memory deterministic executor, and this reduction correlates with residual novelty fraction (ρ_novelty ≥ 0.60) rather than full task length (|ρ_length| < 0.20).

**H0 (Falsifier):** The no-memory deterministic executor achieves matched or better correctness at equal or lower amortized honest cost. If H0 holds, SPIDER's central premise is FALSIFIED-IN-SETTING and the architecture must change.

---

### 4. Experimental Design

#### 4.1 Substrate Requirements (Hard Gates)

Per Director mandate dependencies, this experiment **requires**:
1. **Real HTTP service** (local Flask/FastAPI test server) — *reachable without BrowserGym*
2. **Runtime capability ledger** certifying distributed-substrate bring-up contract
3. **Graph C-FRESHNESS false-accept gate** (TN ≥ 0.85, ≥30 stale probes) for inherited arm's abstention measurement

**If ANY substrate is unavailable → live_available = false → MEASUREMENT_INVALID diagnostic. STOP. Do not substitute synthetic fixtures, jittered counters, or n×3200/f×6.0 proxies. Record finding and halt.**

#### 4.2 Task Families & Novelty Control

- **Matched task families**: ≥10 families, pairwise Jaccard < 0.30, mean < 0.15
- **Controlled novelty fractions**: 0%, 25%, 50%, 75%, 100% (5 strata)
  - Novelty fraction = 1 - max_Jaccard(derived_context, nearest_training_template)
  - Measured on observable state only (url_path, headers_observed, body_observed, url_query)
- **Per-family**: N ≥ 30 tasks, N ≥ 3 per stratum
- **Coverage**: ≥8/10 families represented, pooled ≥40 tasks
- **Holdout**: Whole-trajectory, disjoint families (no family in both train and test)
- **Length variation**: Tasks with 1-10 steps, tertiles for S3 per-stratum check

#### 4.3 Three Arms (Paired Within-Task Design)

| Arm | Registry | Executor Logic | Purpose |
|-----|----------|----------------|---------|
| **A-Inherited** | Populated MechanismRegistry (validated mechanisms from training) | SpiderKernel.resolve() → binds parameters → executes | Treatment: tests if inheritance pays off |
| **B-NoMemory** | **EMPTY** (no mechanisms) | Compiles HTTP request directly from derived_context: uses url, method, headers_observed, body_observed, url_query to construct request. No memory, no reuse. | **Primary Control**: strongest null against inheritance |
| **C-Ablation** | **EMPTY** (identical to B-NoMemory registry) | SpiderKernel.resolve() with empty registry → always returns UNKNOWN | **Mandatory Null Control**: must return 100% UNKNOWN. If any EXECUTABLE → leakage bug. Honest cost = cold upper bound. |

**Critical**: All three arms face **identical derived_context** (same observation) for each task. This is the paired within-task design.

#### 4.4 Honest Cost Measurement (Per-Trajectory Hard-Reset Counters)

For each trajectory, integer counters reset to zero at task start:

| Counter | Description | Applies To |
|---------|-------------|------------|
| `resolve_ops` | Registry/resolution lookups | A, C |
| `bind_ops` | Parameter binding operations | A, C |
| `verify_ops` | Postcondition verification checks | A, B, C |
| `freshness_checks` | Freshness watermark/TTL validation | A, C |
| `network_requests` | Actual HTTP requests sent | A, B, C |
| `browser_steps` | Browser interaction steps (0 if HTTP-only) | A, B, C |

**Total honest cost** = sum of all counters (NO jitter, NO f×6.0, NO token surrogate).

**Token dimension**: No policy model credential available → declared **NOT_APPLICABLE** → reported as **UNKNOWN** in metrics. Never surrogate-filled.

**Browser quantities**: Only reported if Runtime capability ledger certifies launchable browser. Otherwise omitted with explicit note.

**TAU0.30 topology gate**: Only tasks with Jaccard < 0.30 to nearest training template contribute to primary metrics.

**Freshness gate**: Graph C-FRESHNESS TN ≥ 0.85 with ≥30 stale probes required for UNKNOWN precision/ECE metrics.

#### 4.5 Correctness & Verification

- **EXECUTABLE + correct bound_action** → `is_correct = true`
- **EXECUTABLE + wrong bound_action** → `is_false_accept = true`
- **UNKNOWN** (correct abstention) → `is_unknown = true`
- **Verification**: Actual HTTP response matched against mechanism postconditions (Arm A, C) or expected response schema (Arm B)

#### 4.6 Alias Resolution & Routing (If Applicable)

If task families require alias normalization:
- Alias catalog built from TRAIN only (Jaccard ≥ 0.60, min pairwise ≥ 0.60)
- Canonical key = most frequent in train
- **Correct-family gating**: Exact key-set equality after alias resolution
- **Routing normalization**: Version collapse (/api/vN/ → /api/), case normalization
- **TRAIN-only vocab isolation**: 0 leakage from test to train

---

### 5. Controls (Stable Identifiers for Downstream Transmission)

#### Positive Controls (must ALL pass for validity)

| ID | Description | Threshold |
|----|-------------|-----------|
| **PC-EXACT-MATCH** | On exact-match tasks (literal mechanism in registry), both A and B achieve EXECUTABLE with correct bound_action. A cost ≤ B cost. | correct_rate ≥ 0.90, false_accept ≤ 0.10, cost_A ≤ cost_B |

#### Null Controls (must ALL pass for validity)

| ID | Description | Threshold |
|----|-------------|-----------|
| **NC-INHERITANCE-ABLATION** | Arm C (SpiderKernel + empty registry) returns UNKNOWN for ALL tasks. Zero EXECUTABLE. | unknown_rate = 1.0, false_accept = 0.0, cost_C = cold_upper_bound |
| **NC-ORACLE-LEAK** | Static audit: derived_context contains ZERO forbidden keys (residual_novelty_fraction, target_resource_id, length_label, expected_key_set). Read count of test-B resources = 0. | 0 forbidden keys, 0 test-B reads |
| **NC-BIJECTIVE-COST** | Honest cost not bijective with n×3200 or f×6.0 or TAU candidate-count proxy. | gap > 0.35, \|ρ_proxy\| < 0.60 (gated) |
| **NC-SHUFFLED-NULL** | Global trajectory-grouped stratified permutation (5000 perms): \|ρ_shuffled\| < 0.20, centered \|mean\| < 0.05, std < 0.15. | All three conditions |
| **NC-GUARD-SPECIFICITY** | Shuffled guard + freshness ablation (N ≥ 12): precision drop ≥ 30% vs real guards. | drop ≥ 0.30, discriminating not tautological |

---

### 6. Primary Metrics & Decision Rule (Frozen Before Execution)

#### S1: Residual Novelty Correlation
- **Metric**: Spearman ρ between (cost_B - cost_A) and residual_novelty_fraction
- **Threshold**: ρ ≥ 0.60, bootstrap lower CI > 0.40 (5000 family-stratified), permutation p < 0.05 (5000 family-block)
- **Gate**: TAU0.30 + freshness TN ≥ 0.85 gated

#### S2: Length Decoupling (Pooled)
- **Metric**: Spearman \|ρ\| between (cost_B - cost_A) and full task length (steps)
- **Threshold**: \|ρ\| < 0.20, upper CI < 0.25, permutation p ≥ 0.05

#### S3: Length Decoupling (Per-Stratum)
- **Metric**: Per-novelty-stratum (0/25/50/75/100%) AND per-length-tertile \|ρ\|
- **Threshold**: \|ρ\| < 0.20, upper CI < 0.30 for EVERY stratum
- **Requirement**: N ≥ 30 per family, N ≥ 3 per stratum

#### S4: Calibration
- **Metrics**: UNKNOWN precision ≥ 0.85, false_accept ≤ 0.10, ECE ≤ 0.15 (upper ≤ 0.18)
- **Conditions**: Freshness TN ≥ 0.85, ≥30 stale probes, softmax temp 0.15 + deterministic jitter 0.02, imperfect accuracy 0.35-0.78

#### S5: Pareto Dominance
- **Metric**: M_total_SPIDER(f=10) ≤ 0.75 × M_total_COLD (saving ≥ 25%, lower > 15%, p < 0.05)
- **Strict dominance** vs cold AND vs flat RAG k5 at f=10 and f=100
- **Robustness**: ±50% build cost sensitivity
- **External reference**: Agentic Compilation DSM / Agent JIT blind reproductions (if available)

#### S6: Honest Gap
- **Metric**: ρ_novelty - \|ρ_shuffled\| > 0.35, \|ρ_proxy\| < 0.60, global \|ρ_shuffled\| < 0.20 (p ≥ 0.20), centered \|mean\| < 0.05, std < 0.15, within-family std > 0, zero_cells = 0
- **Permutations**: 5000 global + 5000 block, TAU+freshness-gated

#### FALSIFIED-IN-SETTING TRIGGER (Pre-declared)
> **If no-memory executor (B) matches or beats inherited executor (A) at matched correctness (correct_rate_B ≥ correct_rate_A - 0.05) AND equal or lower amortized honest cost (cost_B ≤ cost_A × 1.05) → FALSIFIED-IN-SETTING. Architecture must change.**

#### Overall Verdict
- **SURVIVES_CURRENT_TEST**: S1-S6 ALL pass AND FALSIFIED_IN_SETTING_TRIGGER = FALSE
- **FALSIFIED-IN-SETTING**: FALSIFIED_IN_SETTING_TRIGGER = TRUE (regardless of S1-S6)
- **MEASUREMENT_INVALID**: live_available = false OR any PC/NC fails OR substrate cannot support paired executors with discriminating verification

---

### 7. Validity Threats & Representation Loss (Pre-Declared)

1. **Substrate availability**: Real HTTP service, Runtime ledger, Graph freshness are hard gates. If unavailable → MEASUREMENT_INVALID (not scientific negative).
2. **No BrowserGym**: Experiment designed for HTTP service only. Browser quantities omitted with explicit UNKNOWN.
3. **No policy model**: Token costs = NOT_APPLICABLE → UNKNOWN. No LLM calls in this experiment.
4. **Synthetic task generation risk**: Tasks must be derived from real HTTP service behavior, not hand-crafted fixtures. If only synthetic tasks available → MEASUREMENT_INVALID.
5. **Alias/routing scope**: If task families don't naturally exhibit alias/routing variation, those controls are N/A (not failed).
6. **Sample size**: Minimum thresholds (N ≥ 30/family, N ≥ 3/stratum, pooled ≥ 40) are validity gates. If unmet → MEASUREMENT_INVALID.
7. **Freshness gate dependency**: Graph C-FRESHNESS must be independently validated. If not → S4/S6 cannot be evaluated → MEASUREMENT_INVALID.

---

### 8. Product Consequences

| Outcome | Consequence |
|---------|-------------|
| **SURVIVES_CURRENT_TEST** | C-RESIDUAL-NOVELTY → EXPERIMENTAL. Core premise survives strongest null. Enables product promotion of residual-novelty economics. Justifies continued investment in registry, parameterization, semantic resolution. |
| **FALSIFIED-IN-SETTING** | C-RESIDUAL-NOVELTY → FALSIFIED-IN-SETTING. Core premise fails. C-PRODUCT-ECON and compilation priors jointly moot. Architecture MUST change. Frontier PARKs C-RESIDUAL-NOVELTY, pivots to orthogonal basins (per-value alias via Runtime diverse substrate or production SPA measurement). |
| **MEASUREMENT_INVALID** | No scientific update. Substrate unblockers needed: Runtime ledger, Graph freshness, real HTTP service with sufficient task families. Experiment records finding and stops. |

---

### 9. Dependencies (Per Director Mandate)

1. **Runtime capability ledger** + distributed-substrate bring-up contract
2. **Graph C-FRESHNESS false-accept gate** (TN ≥ 0.85, ≥30 stale probes) for inherited arm's abstention measurement
3. **No policy-model credential** → token cost NOT_APPLICABLE → reported UNKNOWN

---

### 10. Forbidden Substitutions (Explicit)

- ❌ Synthetic 36-family Jaccard 0.0 disjoint-alphabet fixture (EXP-FRONTIER-36042599040)
- ❌ Jittered counters or any f×6.0 / n×3200 proxy
- ❌ Token cost surrogates (must be UNKNOWN)
- ❌ Browser quantities without Runtime capability ledger certification
- ❌ Any substitution when substrate unavailable → **record finding and STOP**

---

### 11. Analysis Plan (Pre-Registered)

1. **Freeze verification**: Hash check on request.json, spec.json, prereg.md before any outcome inspection
2. **Substrate diagnostic**: Run availability checks, emit substrate_diagnostic.json
3. **If live_available = false**: Emit MEASUREMENT_INVALID result.json, report.md, provenance.json. STOP.
4. **If live_available = true**:
   - Build task families from real HTTP service
   - Populate registry from training trajectories
   - Run paired executors (A, B, C) on each test task
   - Collect raw evidence (per-trajectory counters, outcomes, bound_actions)
   - Compute metrics S1-S6 with declared bootstrap/permutation procedures
   - Evaluate PC/NC thresholds
   - Apply frozen decision rule
   - Emit result.json, report.md, provenance.json, artifacts

---

### 12. Artifacts to Produce

| Artifact | Role | Description |
|----------|------|-------------|
| `result.json` | producer handoff | Schema v1: status, outcome, metrics, controls, artifacts, observations, validity_notes, unresolved |
| `report.md` | interpretation | Bounded by measurements, references exact packet fields |
| `provenance.json` | reproducibility | Git commit, seeds, environment, code paths, artifact hashes |
| `artifacts/substrate_diagnostic.json` | raw | Complete substrate availability check |
| `artifacts/raw_evidence.jsonl` | raw | Per-trajectory: task_id, arm, counters, outcome, bound_action, novelty_fraction, length |
| `artifacts/registry_train.jsonl` | fixture | Training mechanisms used for Arm A |
| `artifacts/task_families.json` | derived | Family assignments, novelty fractions, Jaccard stats |

---

### 13. Carry-Forward from Parent Handoff (Preserved Distinctions)

**ESTABLISHED (carried forward):**
- Synthetic 36-family TAU0.30 Jaccard 0.0 non-Pareto: ρ=0.4837 CI[0.410,0.552] ECE=0.216 RAG dominance false (all 11 PCs/NCs PASS) — bounded to synthetic, NOT live heterogeneous
- Alias catalog+routing ceiling: 21/40=0.525 pooled Wilson [0.352,0.648], 0/10 mixed routing gain 0.0
- Substrate diagnostic MEASUREMENT_INVALID with audit PASS — provides zero evidence for/against live heterogeneous gate

**REJECTED (carried forward):**
- WebChoreArena heterogeneous residual-novelty economics itself is NOT rejected (MEASUREMENT_INVALID = zero evidence)
- Deterministic compilation bypass on live heterogeneous gate NOT rejected (4 prior MEASUREMENT_INVALID, all substrate-gated)

**UNKNOWN (carried forward):**
- S1-S6 survival criteria on live heterogeneous gate — all unevaluated
- Whether larger Intel manifest (WebGym 292k, WebArena-Verified Hard expanded) would reveal different economics
- Whether Runtime single-worker sticky WAL + Graph freshness can be validated on cross-site sessions

**DO_NOT_ASSUME (carried forward, CRITICAL):**
- ❌ C-RESIDUAL-NOVELTY is falsified/validated on live heterogeneous gate — prior synthetic FALSIFIED is BOUNDED to TAU0.30 Jaccard 0.0
- ❌ Agent priors (Agentic Compilation DSM $0.002-0.092, Agent JIT 10.4x, hierarchical Intent→Stage→Action, path dependence, human 50.2% vs GPT-5 48.3%) are SPIDER evidence — they are labeled general priors, cannot satisfy S1-S6 thresholds
- ❌ Chromium presence or PyPI reachable implies BrowserGym available — importlib find_spec is the ground truth
- ❌ Cross-family key adoption valid without exact key-set equality, TRAIN-only vocab isolation, whole-trajectory holdout
- ❌ Statistical thresholds hold without 5000 global + 5000 block perms, freshness TN≥0.85, coverage ≥8/10

---

### 14. Signatures

**Frozen by:** deterministic freezer (not research agent)  
**Hashes recorded in:** freeze.json  
**Downstream stages:** EXECUTE → AUDIT → DIRECTOR → CODEX  

**This preregistration is immutable after freeze. No outcome-bearing measurements may be inspected during DESIGN. Any analysis change after seeing results is exploratory and requires new preregistration with untouched evidence.**