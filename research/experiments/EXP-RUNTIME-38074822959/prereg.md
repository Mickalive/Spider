# Preregistration: EXP-RUNTIME-38074822959

**Lane:** runtime | **Design Contract:** v2 | **Target Claim:** C-MEAS-VALID (shared), C-RESIDUAL-NOVELTY
**Director Mandate:** CONTINUE with SUPERSEDE disposition on parent oracle-repair handoff
**Strategic Question:** Can a parameterized asymmetric-discovery task bank be certified arithmetically BEFORE freeze — with cold and retrieval-shaped baselines demonstrably below ceiling at high residual novelty (≥0.7), a real treatment/comparator behavioural distinction, honest per-condition counters, and a preregistered contamination/dynamic-range certificate — delivered as a reusable substrate that unblocks blocker B2 for the flagship inheritance benchmark?

---

## 1. Background and Motivation

The Global Research Director has identified three readiness conditions (B1, B2, B3) gating the flagship inheritance benchmark (C-LLM-INHERIT, C-RESIDUAL-NOVELTY, C-PRODUCT-ECON). **B2 is the Runtime lane's responsibility**: a task bank with non-ceiling cold/retrieval dynamic range and a real treatment/comparator contrast.

The previous Runtime experiments (EXP-RUNTIME-37973247935, EXP-RUNTIME-36293257855) focused on the composite oracle's out-of-surface transfer detection. That thread is MEASUREMENT_INVALID due to:
- Detector compromise: hop-by-hop `Connection` header excluded from volatile-header set (260/260 false positives)
- Capture-stability gate mis-specified (checked `all_identical` vs prereg's `byte-identical` = WAL vector)
- M-REVERT-LOGICAL implemented as byte-restore, not logical restore

The Director's cognitive reset: **do not repair the oracle again**. The mandate supersedes the parent handoff with SUPERSEDE disposition. This experiment addresses B2 directly: **certify a task bank substrate with arithmetic proof of non-ceiling dynamic range before any outcome measurement**.

---

## 2. Hypothesis

A task bank constructed from parameterized web interaction sequences with controlled residual novelty (≥0.7) will yield:
- **Cold baseline** success ≤0.60 (upper 95% Wilson bound <0.85)
- **Retrieval baseline** success ≤0.75 (upper 95% Wilson bound <0.85)
- **SPIDER-inheritance treatment** shows Δsuccess ≥0.20 over retrieval with lower Wilson bound >0.10, and cost_ratio ≤0.70
- All with honest counters: `http_requests`, `retrieval_calls`, `verification_calls`, `repair_attempts`

The **dynamic range certificate** (ceiling gap ≥0.25 for cold, ≥0.15 for retrieval) is **arithmetically verifiable from frozen task bank parameters alone** before freeze.

---

## 3. Falsifier

The design is falsified at the arithmetic certificate stage (pre-freeze) if **any** of:
1. Certified cold upper Wilson bound ≥0.85
2. Certified retrieval upper Wilson bound ≥0.85
3. Certified residual novelty <0.70
4. Maximum theoretical Δsuccess (treatment vs retrieval) <0.15 under parameterized novelty model
5. Honest counter instrumentation cannot be implemented without synthetic fallback

If falsified, the task bank cannot serve as a non-degenerate B2 substrate. The experiment cannot freeze. The Runtime lane must report the certificate failure and await Director redirection.

---

## 4. Task Bank Construction (Parameterized Asymmetric Discovery)

### 4.1 Task Representation
Each task is a **directed acyclic graph (DAG)** of web interaction steps:
- Nodes: `Action` objects (HTTP method, URL template, parameter schema, expected response pattern)
- Edges: `Transition` objects (preconditions, postconditions, side effects)
- Parameters: `TaskParameters` (structural: graph topology, parameter domains; semantic: entity types, relationship patterns)

### 4.2 Asymmetric Discovery Property
A task has **asymmetric discovery** iff:
- **Discovery cost** (cold): Number of valid action sequences to reach goal from initial state ≥ 10
- **Inheritance cost** (warm): With correct parameterized mechanism, cost ≤ 3 steps
- **Residual novelty**: Structural Hamming distance to nearest known fragment / task diameter ≥ 0.7

### 4.3 Parameterization for Novelty Control
The task bank generator (`task_bank.py`) produces tasks by sampling from a **parameterized grammar**:
```
TaskGrammar := Sequence(Step+) | Branch(Step, Step+) | Loop(Step, IntRange)
Step := Navigate(URLTemplate) | Click(SelectorTemplate) | FormFill(FieldMap) | Assert(ResponsePattern)
URLTemplate := "/api/{entity}/{action}?{params}"
SelectorTemplate := "[data-testid='{component}-{action}']"
FieldMap := {field: ValueGenerator}
ValueGenerator := Constant | Enum(domain) | Faker(provider)
```

**Novelty dimensions** (each independently controllable):
1. **Structural novelty**: Unseen graph topology (new branching/loop patterns)
2. **Parametric novelty**: Unseen entity/parameter combinations
3. **Semantic novelty**: Unseen entity types and relationship patterns
4. **Compositional novelty**: Known fragments in new sequences

The **residual novelty score** for a task is the maximum over dimensions, normalized to [0,1].

### 4.4 Bank Split (Contamination Control)
- **Certification set** (N=50 tasks): Frozen at DESIGN, used **only** for arithmetic certificate. Never measured at EXECUTE.
- **Evaluation set** (N=100 tasks): Disjoint from certification set. Used for outcome measurement at EXECUTE.
- **Retrieval index**: Built **only** from certification set trajectories (simulated cold runs). Evaluation set tasks never enter the retrieval index.

---

## 5. Experimental Conditions (Arms)

| Arm | ID | Inheritance Level | Retrieval | SPIDER Mechanisms | Expected Success |
|-----|-----|-------------------|-----------|-------------------|------------------|
| Cold | COLD | None | No | No | ≤0.60 |
| Retrieval | RETRIEVAL_ONLY | Retrieved fragments (top-k semantic similarity) | Yes | No | ≤0.75 |
| Treatment | SPIDER_INHERIT | Full SPIDER: parameterized mechanisms + verification + repair | Yes | Yes | ≥0.85 |
| Positive Control | PC-KNOWN_ROUTE_REPLAY | Exact replay (novelty=0) | N/A | N/A | 1.0 |
| Null Control | NC-SHUFFLED_NOVELTY | Shuffled parameters (destroyed semantics) | Yes | No | ≤ Cold |

### 5.1 Per-Arm Sample Sizes
- COLD: n=40 evaluation tasks
- RETRIEVAL_ONLY: n=40 evaluation tasks (same tasks as COLD, different condition)
- SPIDER_INHERIT: n=40 evaluation tasks (same tasks)
- PC-KNOWN_ROUTE_REPLAY: n=10 certification tasks (novelty=0)
- NC-SHUFFLED_NOVELTY: n=20 evaluation tasks (shuffled version of evaluation tasks)

Total evaluation episodes: 140 (40 × 3 + 10 + 20). All arms use the **same evaluation task set** (except PC/NC) for matched comparison.

---

## 6. Honest Counter Instrumentation

**No synthetic fallback.** Every counter is an explicit API call in the execution harness:

| Counter | Instrumentation Point | Definition |
|---------|----------------------|------------|
| `http_requests` | Instrumented HTTP transport (wrapper around `httpx`/`requests`) | Count of outbound HTTP requests issued by the agent |
| `retrieval_calls` | `Registry.lookup(query, k)` | Count of semantic retrieval calls to the fragment store |
| `verification_calls` | `Verifier.verify(action, expected, actual)` | Count of explicit outcome verification calls |
| `repair_attempts` | `Repairer.attempt(failure_context)` | Count of localized delta repair invocations |

**Measurement failure mode:** If any counter returns `None` or raises `NotImplementedError`, the episode is marked `counter_failure=true` and recorded in `validity_notes`. The decision rule requires **zero counter failures** for SUPPORTS.

---

## 7. Arithmetic Certificate (Pre-Freeze, Deterministic)

The certificate is a **pure function** of:
- Frozen task bank JSON (certification set, 50 tasks)
- Frozen decision thresholds (Wilson z=1.96, point_min=0.90, wilson_lo_min=0.80)
- Frozen baseline models (cold: uniform random walk; retrieval: nearest-neighbor fragment reuse)

### 7.1 Certificate Computation
```python
def compute_certificate(task_bank: TaskBank, thresholds: Thresholds) -> Certificate:
    # 1. Residual novelty: exact from task bank parameters
    novelty_scores = [t.residual_novelty for t in task_bank.certification_set]
    certified_novelty = min(novelty_scores)  # conservative
    
    # 2. Cold baseline ceiling: theoretical max success for uniform random walk
    #    on task DAGs with given branching factors and depths
    cold_max_p = max_theoretical_cold_success(task_bank.certification_set)
    cold_upper_wilson = wilson_upper(cold_max_p * 40, 40, thresholds.wilson_z)
    
    # 3. Retrieval baseline ceiling: theoretical max for nearest-neighbor fragment reuse
    #    given fragment coverage and parametric overlap
    retrieval_max_p = max_theoretical_retrieval_success(task_bank.certification_set)
    retrieval_upper_wilson = wilson_upper(retrieval_max_p * 40, 40, thresholds.wilson_z)
    
    # 4. Max theoretical treatment advantage
    max_delta = max_theoretical_delta(task_bank.certification_set)
    
    # 5. Counter instrumentation completeness
    counters_complete = all(has_implementation(c) for c in COUNTER_APIS)
    
    return Certificate(
        certified_novelty=certified_novelty,
        cold_upper_wilson=cold_upper_wilson,
        retrieval_upper_wilson=retrieval_upper_wilson,
        max_theoretical_delta=max_delta,
        counters_complete=counters_complete,
        pass_all=(
            certified_novelty >= 0.70 and
            cold_upper_wilson < 0.85 and
            retrieval_upper_wilson < 0.85 and
            max_delta >= 0.20 and
            counters_complete
        )
    )
```

### 7.2 Certificate PASS Criteria (All Required)
| Check | Threshold | Rationale |
|-------|-----------|-----------|
| `certified_novelty` | ≥ 0.70 | High residual novelty per mandate |
| `cold_upper_wilson` | < 0.85 | Non-ceiling: room for treatment improvement |
| `retrieval_upper_wilson` | < 0.85 | Non-ceiling: retrieval alone insufficient |
| `max_theoretical_delta` | ≥ 0.20 | Real treatment/comparator distinction possible |
| `counters_complete` | = true | Honest counters, no synthetic fallback |

**The certificate is computed at DESIGN time and included in `spec.json.freeze_eligibility`. If any check fails, the experiment cannot freeze.**

---

## 8. Outcome Measurement (Post-Freeze, EXECUTE)

### 8.1 Primary Metrics (per arm)
| Metric | Estimand | Success Criterion |
|--------|----------|-------------------|
| `success_rate` | Task completion | COLD ≤0.65 (upper Wilson <0.80), RETRIEVAL ≤0.80 (upper Wilson <0.90), SPIDER ≥0.85 |
| `cost_ratio` | SPIDER cost / COLD cost | ≤0.70 (SPIDER cheaper than cold) |
| `Δsuccess` | SPIDER - RETRIEVAL | ≥0.20 (lower Wilson >0.10) |
| `counters_clean` | Fraction of episodes with zero counter failures | =1.0 |

### 8.2 Decision Rule (Outcome)
| Outcome | Conditions |
|---------|------------|
| **SUPPORTS** | All primary metrics meet criteria + independent recomputation `zero_mismatches=true` |
| **FALSIFIES** | Any primary metric fails its criterion |
| **MIXED** | Certificate PASSED but outcome INCONCLUSIVE (e.g., Δsuccess=0.18 with CI crossing 0.10) |
| **MEASUREMENT_INVALID** | Counter failures >0, or infrastructure failure, or recomputation mismatch |

### 8.3 No Claim Promotion on Certificate Alone
Per Director mandate: **C-MEAS-VALID and C-RESIDUAL-NOVELTY status unchanged until outcome measurement completes with valid SUPPORTS.** The arithmetic certificate only gates freeze eligibility and B2 unblocking for downstream preregistration.

---

## 9. Positive and Null Controls

### 9.1 Positive Control: PC-KNOWN_ROUTE_REPLAY
- **Task**: Exact replay of a known successful trajectory (novelty=0)
- **Expected**: success_rate=1.0, cost_ratio=1.0, all counters match first-agent cost
- **Failure mode**: If <1.0, the substrate has execution/replay defects — recorded in `validity_notes`, triggers MEASUREMENT_INVALID

### 9.2 Null Control: NC-SHUFFLED_NOVELTY
- **Task**: Evaluation tasks with parameters shuffled (semantic coherence destroyed, surface statistics preserved)
- **Expected**: success_rate ≤ COLD baseline, no SPIDER advantage
- **Failure mode**: If SPIDER shows advantage on shuffled tasks, the effect is driven by surface statistics, not semantic inheritance — recorded in `validity_notes`

---

## 10. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Retrieval contamination** | Retrieval index built ONLY from certification set; evaluation set never indexed |
| **Parameter leakage** | Certification/evaluation split by task ID hash; disjoint parameter domains enforced |
| **Counter synthetic fallback** | Abstract counter interfaces; missing implementation = measurement failure (not zero) |
| **Ceiling effects** | Arithmetic certificate guarantees upper Wilson bounds <0.85 pre-freeze |
| **Treatment non-liveness** | Adapter interface specified at DESIGN; stub validates structural executability |
| **Authorship confusion** | Task bank (runtime) separate from SPIDER mechanism (graph/product); adapter boundary frozen |

---

## 11. Reusable Substrate Deliverables

If certificate PASSES and outcome SUPPORTS, the following become **reusable runtime substrate** for B2 unblocking:
1. `task_bank.py` — Parameterized task generator with novelty certification
2. `task_harness.py` — Instrumented execution engine with counter hooks
3. `task_adapter.py` — SPIDER inheritance adapter interface (Graph/Product implement)
4. `counters.py` — Honest counter API definitions and concrete implementations
5. `certification.py` — Arithmetic certificate computation (deterministic, pure)

These are listed in `spec.json.freeze_artifacts` and will be hashed into `freeze.json`.

---

## 12. Dependencies on Other Lanes

- **Graph/Product lanes**: Provide `TaskInheritanceAdapter` implementation at EXECUTE. The interface is frozen in this design.
- **Intel lane**: No dependency (local task bank, no external datasets).
- **Physics/Frontier**: No dependency.

---

## 13. Consequences

### Positive (Certificate PASS + Outcome SUPPORTS)
- B2 blocker **resolved**. Flagship inheritance benchmark can be preregistered.
- Task bank substrate **promoted** to reusable runtime capability.
- Graph/Product lanes proceed with C-LLM-INHERIT/C-RESIDUAL-NOVELTY/C-PRODUCT-ECON preregistration using this substrate.

### Negative (Certificate FAIL or Outcome FALSIFIES/MEASUREMENT_INVALID)
- B2 blocker **persists**. No certified non-ceiling task bank exists.
- Runtime lane reports certificate failure with exact failing check.
- Global Director must PARK/PIVOT Runtime or weaken B2 dependency.
- Graph/Product lanes must either accept UNKNOWN on inheritance economics or propose alternative B2 resolution.

---

## 14. Computational Budget

- **Task bank generation**: ~100 tasks × 10 variants = 1000 DAGs (offline, <5 min)
- **Certificate computation**: Deterministic, <1 sec
- **EXECUTE**: 140 episodes × ~30 steps = ~4200 instrumented steps
- **Model calls**: ~1200 (estimated 8-10 per episode for SPIDER arm)
- **Browser sessions**: 180 (includes warmup/calibration)
- **Wall time**: ~4 hours on allocated infrastructure

---

## 15. Pre-Freeze Satisfiability Probes (Design Contract v2)

**Cheap non-outcome-bearing probes executed at DESIGN to verify certificate computability:**

1. **Task bank generator instantiation**: Import `task_bank.py`, generate 5 tasks, verify novelty scores computable.
2. **Certificate computation**: Run `certification.compute_certificate()` on generated tasks, verify all five checks return boolean.
3. **Counter interface validation**: Import `counters.py`, verify all four counter APIs have concrete implementations (no `NotImplementedError`).
4. **Adapter interface validation**: Import `task_adapter.py`, verify `TaskInheritanceAdapter` is an abstract base class with required methods.
5. **Harness smoke test**: Run `task_harness.py` on 1 COLD episode, verify counters increment and episode completes.

**All probes must pass before freeze.** Probe results are recorded in `validity_notes` of `spec.json` but are NOT outcome measurements.

---

## 16. Comparison with Pre-2.0 Precedents

| Pre-2.0 Artifact | Relation | Difference |
|------------------|----------|------------|
| P2-REPLAY-COST (sha 9687ff787f2d74460bb7006826008852f5b4416b) | **Guard** | Withdrew 8.5x speed claim; mandated matched tasks + fully loaded counterfactual costs. This design obeys: matched evaluation tasks across arms, honest counters including retrieval/verification/repair. |
| P2-BLIND-COMPOSITION (sha 017a80aeb9a6759c8f6913a37031ff1616ec1bda) | **Guard** | G-H2 used keywords/oracle/weak baselines. This design: no keywords, no oracle, strong baselines (cold + retrieval), explicit null control. |
| P2-MIND2WEB (Mind2Web V0.50) | **Guard** | 3.4% exact match, 26.7% retrieval. This design: parameterized novelty control, residual novelty ≥0.7 certified, not assumed. |
| P2-AUTOMATION (archived Codex §2) | **Guard** | Immutable request, hash-pinned inheritance, separation of workflow completion and scientific validity. This design: design_contract v2, freeze_eligibility, freeze_artifacts_bound. |
| EXP-RUNTIME-37973247935 (parent) | **Superseded** | Oracle repair thread (MEASUREMENT_INVALID). This design: SUPERSEDE disposition, addresses B2 directly, no oracle repair. |

**LEGACY: DISTINCT_EXTENSION** — No pre-2.0 or Research 2.0 artifact delivers a task bank with certified non-ceiling dynamic range, honest counters, and a pre-freeze arithmetic certificate. The mandate adds the certificate requirement that prior attempts lacked.

---

## 17. Freeze Eligibility Declaration (Design Contract v2)

All six checks **PASS** with justification:

1. **decision_rule_reachability**: PASS — Arithmetic certificate is a pure deterministic function of frozen parameters.
2. **measurement_prerequisites**: PASS — All components specified for construction; no unavailable external dependencies.
3. **baseline_identifiability**: PASS — Cold/retrieval ceilings computable from task DAG parameters; Wilson bounds deterministic.
4. **control_sensitivity**: PASS — PC (replay=1.0) and NC (shuffled≤cold) are discriminating and executable.
5. **treatment_liveness**: PASS — Adapter interface frozen; stub validates structural executability at DESIGN.
6. **freeze_artifacts_bound**: PASS — All 10 mutable local files listed in `spec.json.freeze_artifacts`.

---

## 18. Signature

This preregistration is frozen at DESIGN. No outcome data has been inspected. The arithmetic certificate is computed from the frozen task bank parameters and included in `spec.json`. The experiment proceeds to FREEZE only if all six `freeze_eligibility` checks are PASS.

**Design Agent:** SPIDER Research 2.0 Runtime Lane
**Date:** 2026-10-10
**Request Hash:** 3acd38937a2bfca465d07bdec1f1b171fcb74c940475908ebfdc075962e34900