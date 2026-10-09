# Preregistration: EXP-PRODUCT-37385633334

**Experiment ID**: EXP-PRODUCT-37385633334
**Lane**: product
**Claim**: C-LLM-INHERIT
**Director Mandate**: PIVOT (supercedes parent handoff EXP-PRODUCT-36314204238)
**Created**: 2026-10-05

---

## 1. Strategic Question (Binding from Director Mandate)

> Does a real external agent with a real LLM benefit from SPIDER's inherited mechanisms beyond strong memory and instruction baselines, at equal model, tools and budget?

This is the program's actual product thesis. It has 24 prior experiments and **zero admissible evidence**. Both owner lanes (graph, product) have it on their neglected list. No other lane can own it: it requires external-agent behaviour and end-to-end economics, which is Product's charter.

---

## 2. Readiness Certificate (Gate 0 — Mandatory, Pre-Execution)

The experiment **terminates at MEASUREMENT_INVALID** if any element is absent. No arm executes until all three checks pass.

### 2.1 Model Endpoint Reachable
- **Check**: HTTP POST to configured model endpoint returns 200 with valid completion within 30s
- **Model**: gpt-4o-mini (or equivalent available endpoint), temperature=0, max_tokens=4096
- **Seed**: 42 (fixed for all arms)
- **Failure**: No model key, endpoint unreachable, timeout, or invalid response → MEASUREMENT_INVALID

### 2.2 Task Set: ≥30 Credential-Free Real-Web Tasks with Mechanical Verification
- **Source**: Public, credential-free websites (HTTPBin, Wikipedia API, GitHub API, example.com, jsonplaceholder, reqres.in, etc.)
- **Minimum**: 30 distinct tasks across ≥5 domains
- **Verification**: Each task has a **mechanical postcondition** — a deterministic Python function `verify(task_id, trajectory) -> bool` that checks:
  - HTTP status code
  - Response body JSON schema / exact field values
  - DOM selector presence / text content (for browser tasks)
  - No LLM judge, no human evaluation, no self-report
- **Task Categories** (examples, final list frozen in spec):
  - API GET with expected JSON response (10 tasks)
  - API POST with expected creation response (5 tasks)
  - HTML page navigation + DOM assertion (8 tasks)
  - Multi-step form interaction + result verification (7 tasks)
- **Credential-Free**: No authentication, no API keys, no login required
- **Failure**: <30 tasks defined, any task lacks mechanical verifier, any task requires credentials → MEASUREMENT_INVALID

### 2.3 Accounting-Fidelity Control (PC-ACCOUNTING-FIDELITY)
- **Seeded Control Trajectory**: A deterministic 5-step browser+HTTP trajectory on httpbin.org with known ground truth counts
- **Counters Verified** (per trajectory):
  - `model_calls` (exact integer)
  - `model_tokens` (prompt + completion, exact)
  - `browser_actions` (click, type, navigate, exact)
  - `http_requests` (exact)
  - `retrieval_calls` (exact)
  - `verification_calls` (exact)
  - `repair_attempts` (exact)
  - `latency_ms` (wall clock)
- **Pass Criterion**: `max_relative_error <= 0.01` on all counter types vs ground truth
- **Failure**: Any counter exceeds 1% error → MEASUREMENT_INVALID (instrument not trustworthy)

---

## 3. Arms (Executed ONLY After Readiness Certificate Passes)

All arms share **identical** runtime configuration:
- Model: gpt-4o-mini, temperature=0, seed=42, max_tokens=4096, max_steps=15
- Tools: Playwright (Chromium), HTTP client (httpx), SPIDER kernel (SPIDER arm only)
- Budget: 15 steps max per task, 4096 tokens max per step
- Task Order: Randomized per arm (seed=42), same order across arms for fair comparison

### 3.1 B-COLD (Cold Re-derivation) — Negative Control
- **Knowledge**: Empty. No observation bank, no mechanisms, no instructions beyond task goal.
- **Agent Prompt**: "You are a web agent. Complete the task: {goal}. You have access to browser and HTTP tools."
- **Inheritance**: None. Every action derived from scratch.

### 3.2 B-INSTRUCTIONS (Instructions-Only) — Baseline
- **Knowledge**: Natural-language task instructions only (1-2 sentences per task describing the procedure).
- **Retrieval**: None. No access to observation bank.
- **Inheritance**: None. No mechanism registry, no bind/execute.
- **Agent Prompt**: "You are a web agent. Complete the task: {goal}. Procedure: {instructions}. You have access to browser and HTTP tools."

### 3.3 B-RETRIEVAL (Retrieval Baseline, K=5) — Strong Baseline
- **Knowledge**: SPIDER observation bank (all prior trajectories from this experiment's induction phase).
- **Retrieval**: TF-IDF Jaccard similarity (TAU=0.30), top-5 trajectories returned.
- **Retrieval Quality Reported**: precision@5, recall@5, mean similarity score per task.
- **Inheritance**: None. Retrieved trajectories shown as examples; no mechanism bind/execute.
- **Agent Prompt**: "You are a web agent. Complete the task: {goal}. Here are 5 similar past trajectories: {retrieved}. You have access to browser and HTTP tools."

### 3.4 A-SPIDER (SPIDER Arm) — Treatment
- **Knowledge**: SPIDER observation bank + mechanism registry (as currently implemented in `src/spider/kernel.py`).
- **Retrieval**: Same as B-RETRIEVAL (TF-IDF Jaccard K=5, TAU=0.30) for fair budget matching.
- **Inheritance**: Full SPIDER pipeline:
  1. `resolve(goal, context)` → candidate mechanisms
  2. `bind(mechanism, goal, context)` → bound_action (with parameter slots)
  3. `execute(bound_action)` → observation
  4. `verify(observation, postcondition)` → success/failure
  5. `repair(failure, mechanism)` → retry (if implemented)
- **Absent Primitives (Declared Before Freeze)**:
  - ❌ NO freshness guard (C-FRESHNESS) — mechanisms never checked for staleness
  - ❌ NO delta repair (C-DELTA-REPAIR) — local Web changes not repaired locally
  - ❌ NO cross-site transfer (C-CROSSSITE) — mechanisms not validated across sites
- **Agent Prompt**: "You are a web agent with SPIDER inheritance. Complete the task: {goal}. SPIDER provides: {bound_mechanism if resolved}. You have access to browser and HTTP tools."

---

## 4. Induction Phase (Pre-Arm)

Before arms execute, SPIDER builds its observation bank and mechanism registry:
- **Induction Tasks**: 50 tasks (distinct from the 30+ test tasks) run with B-COLD to populate observation bank
- **Mechanism Distillation**: `distill_parameterized()` run on induction observations to produce mechanism registry
- **Registry State**: Frozen before test arms begin. Same registry used for all test tasks.

---

## 5. Metrics (Stable Identities for Downstream Transmission)

### 5.1 Primary Metric
- **cost_per_verified_success_M_total_f10**
  - `M_total_f10 = model_tokens + 10 * (browser_actions + http_requests + retrieval_calls + verification_calls + repair_attempts)`
  - Amortized over f=10 reuses: `cost_per_success = (induction_cost / f + sum(M_total_f10 per task)) / verified_successes`
  - Reported per arm with family-stratified bootstrap 95% CI (5000 resamples, trajectory_id unit)

### 5.2 Accuracy Metrics (Reported ALONGSIDE Cost, Never Traded)
- **task_success_rate**: verified_successes / total_tasks
- **false_accept_rate**: false_accepts / (verified_successes + false_accepts)
- **abstention_rate**: abstentions / total_tasks
- **ECE (Expected Calibration Error)**: on bind confidence vs execution success

### 5.3 Per-Trajectory Honest Counters (Raw Evidence)
- `model_calls`, `model_tokens`, `browser_actions`, `http_requests`, `retrieval_calls`, `verification_calls`, `repair_attempts`, `latency_ms`
- Recorded per trajectory, per arm, per task

### 5.4 Retrieval Quality (B-RETRIEVAL and A-SPIDER)
- `retrieval_precision_at_5`, `retrieval_recall_at_5`, `retrieval_mean_similarity`

---

## 6. Falsifier (Frozen Before Execution)

**The SPIDER arm (A-SPIDER) must beat the retrieval baseline (B-RETRIEVAL) on BOTH:**
1. `cost_per_verified_success_M_total_f10` strictly lower (bootstrap CI upper < B-RETRIEVAL CI lower)
2. `task_success_rate` within 2% (SPIDER >= B-RETRIEVAL - 0.02)

**AND satisfy safety gates:**
3. `false_accept_rate <= 0.10`
4. `abstention_rate in [0.00, 0.15]` with `ECE <= 0.15`

If readiness certificate fails → `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`.

---

## 7. Controls (Stable Identities)

| Control ID | Type | Expected Behavior | Pass Criterion |
|------------|------|-------------------|----------------|
| PC-ACCOUNTING-FIDELITY | Positive | All counters within 1% of ground truth on seeded trajectory | max_relative_error <= 0.01 |
| NC-SHUFFLED-RETRIEVAL | Null | Cost >= B-COLD, Accuracy <= B-COLD | cost_ratio_vs_cold >= 1.0 AND accuracy_ratio_vs_cold <= 1.0 |

---

## 8. Validity Threats (Disclosed Before Freeze)

1. **Synthetic-to-Real Gap**: Task set uses public APIs and simple sites, not complex production SPAs. Generalization to complex sites untested.
2. **Absent Primitives**: No freshness guard, no delta repair. A null result is a lower bound, not a refutation of the full product thesis.
3. **Model Dependency**: Results specific to gpt-4o-mini (or configured model) at temperature=0. Other models may differ.
4. **Induction Bias**: Mechanism registry built from B-COLD induction only. Different induction policies could yield different mechanisms.
5. **Retrieval Budget Matching**: B-RETRIEVAL and A-SPIDER use same retrieval budget (K=5), but A-SPIDER also has mechanism execution cost. This is intentional — the test is whether the *additional* inheritance mechanism pays for itself.
6. **Task Selection**: 30+ tasks chosen for mechanical verifiability, not representativeness of all Web tasks.
7. **Single-Run**: No replication across model seeds or task subsets in this experiment. Generalization requires follow-up.

---

## 9. Product Consequences (Frozen)

### Positive (SUPPORTS)
- C-LLM-INHERIT advances toward EXPERIMENTAL/VALIDATED
- First admissible evidence for SPIDER's product thesis
- Product thesis gains empirical footing
- Next gates: C-CROSSSITE (cross-site transfer), C-FRESHNESS (staleness detection), C-DELTA-REPAIR (local repair)

### Negative (FALSIFIES)
- C-LLM-INHERIT remains HYPOTHESIS
- Current architecture's central claim falsified under rigorous test
- Product lane must either strengthen primitives or pivot architecture
- No promotion possible without SUPPORTS on this claim

### Measurement Invalid (Readiness Certificate Failure)
- Missing substrate honestly identified (model, tasks, or counters)
- Cheap early abort prevents expensive invalid packet
- Even a failed SPIDER arm would yield first valid execution of B-RETRIEVAL and B-INSTRUCTIONS against a real agent — itself an unheld external comparator

---

## 10. Reproducibility Commitments

- All code paths: `src/spider/kernel.py`, `src/spider/variability.py` (if present), experiment runner
- Frozen model config: endpoint, temperature=0, seed=42, max_tokens=4096
- Frozen task list with mechanical verifiers (committed before freeze)
- Frozen induction task list (50 tasks, distinct from test)
- Family-stratified bootstrap: 5000 resamples, trajectory_id unit, seed=42
- Block permutation: 5000 permutations, trajectory_id blocks, seed=42
- All raw evidence preserved: per-trajectory counters, bind/execute/verify logs, mechanical verification results

---

## 11. Deviations from Parent Handoff (Explicit per SUPERSEDE)

The Director mandate **SUPERSEDES** the parent handoff (EXP-PRODUCT-36314204238). Key differences:
- **Claim**: C-LLM-INHERIT (not C-PARAM-INHERIT or C-PRODUCT-ECON)
- **Agent**: Real LLM (not scripted heuristic)
- **Tasks**: Real credential-free Web (not synthetic stdlib server)
- **Verification**: Mechanical (not self-reported)
- **Baselines**: Strong (cold, instructions, retrieval) executed FIRST
- **Readiness Certificate**: Mandatory gate before any arm
- **Cost Model**: M_total_f10 with honest per-trajectory counters
- **Absent Primitives**: Declared before freeze (freshness, repair)

The parent handoff's identifier-level support model question is **Graph's mechanism micro-research**, assigned to Graph lane. This experiment tests the **product thesis end-to-end**.

---

## 12. Mandatory Non-Experiment Obligation (Hygiene)

Per Automation Invariant 13 and Director mandate: **Revert the committed four-file 1466-line kernel delta** (src/spider/variability.py, tests/test_variability.py, src/spider/kernel.py, src/spider/models.py) from the Product branch while retaining evidence packets. This is recorded as done in the experiment provenance, not as an experimental outcome.

---

*This preregistration is frozen upon creation of freeze.json. No outcome-bearing measurements may be inspected during DESIGN. The readiness certificate gate ensures MEASUREMENT_INVALID is an honest substrate diagnosis, not a scientific conclusion.*