# Preregistration: EXP-PRODUCT-37982016598

**Lane**: product
**Claim**: C-RESIDUAL-NOVELTY
**Experiment ID**: EXP-PRODUCT-37982016598
**Director Mandate**: PIVOT from C-PARAM-INHERIT to C-RESIDUAL-NOVELTY
**Parent Handoff**: EXP-PRODUCT-37973256064 (audit PASS, parameterized path LIVE on real credential-free substrate, ZERO dynamic range)

---

## 1. Scientific Question

On the real credential-free localhost HTTP substrate where the shipped kernel's parameterized `distill_parameterized -> resolve -> execute` path is live and causally attributable (established in EXP-PRODUCT-37973256064, audit PASS), over **matched task families with a controlled residual-novelty fraction and a PRE-FREEZE CERTIFIED dynamic range** (cold re-derivation and retrieval-shaped comparator success_rate < 0.95), does **cost per SUCCESSFUL task** — including verification and repair, in honest `http_requests`/`verification_calls`/`repair_attempts`/`latency_ms` — **track residual novelty rather than full task length**, against:

- **B-COLD-RE-DERIVE**: cold re-derivation (direct URL construction from task spec)
- **B-RETRIEVAL-SHAPED**: retrieval-shaped comparator (embedding retrieval + template bind)
- **B-EMPTIED-REGISTRY**: inheritance-ablation null (emptied registry forcing cold fallback)

---

## 2. Hypothesis (Frozen)

**H1 (Primary)**: Cost per successful task for the SPIDER parameterized inheritance arm (**T-SPIDER-PARAM**) increases **sub-linearly** with residual novelty fraction, while **B-COLD-RE-DERIVE** and **B-RETRIEVAL-SHAPED** increase **super-linearly or linearly**, such that the **cost advantage of SPIDER over both comparators grows with residual novelty**.

**H2 (Null)**: The emptied-registry arm (**B-EMPTIED-REGISTRY**) produces cost_per_success statistically indistinguishable from **B-COLD-RE-DERIVE** at all novelty levels, confirming that any SPIDER advantage requires registry content.

**H3 (Substrate)**: At zero novelty (training identifiers), all arms achieve success_rate = 1.0 and T-SPIDER-PARAM cost_per_success ≤ B-COLD-RE-DERIVE (registry lookup overhead only).

---

## 3. Falsifier (Frozen, Both Directions)

The experiment yields **FALSIFIES-IN-SETTING** if **ANY** of the following hold:

1. **Dynamic range certification fails**: B-COLD-RE-DERIVE success_rate ≥ 0.95 OR B-RETRIEVAL-SHAPED success_rate ≥ 0.95 on ALL task families at novelty ≥ 0.5. (No headroom → MEASUREMENT_INVALID)

2. **Matched correctness fails**: Any arm achieves success_rate < 0.80 on more than 1 of 4 novelty levels. (Cannot compare cost at unequal correctness)

3. **Cost advantage does not grow with novelty**: Spearman ρ (cost_advantage_vs_cold vs novelty) ≤ 0.5 with permutation p ≥ 0.05, **OR** Spearman ρ (cost_advantage_vs_retrieval vs novelty) ≤ 0.5 with permutation p ≥ 0.05.

4. **No advantage at highest novelty**: At the highest novelty level tested (novelty ≥ 0.7), T-SPIDER-PARAM cost_per_success is **NOT** lower than BOTH B-COLD-RE-DERIVE AND B-RETRIEVAL-SHAPED (paired permutation p ≥ 0.05 for either comparison).

**If all primary conditions pass → SUPPORTS.**

**If any primary condition fails → FALSIFIES (valid scientific negative, not infrastructure failure).**

---

## 4. Experimental Design

### 4.1 Substrate (Credential-Free, Identical to EXP-PRODUCT-37973256064)

- **Server**: localhost stdlib `http.server` (harness/substrate.py)
- **Resource types**: `items`, `users`, `orders`, `products` (4 types)
- **Identifiers per type**: 20 (001-020)
- **HTTP semantics**: GET/PUT/POST/DELETE with deterministic headers, realistic response bodies
- **No model calls**: `model_calls=0`, `model_tokens=0` for all arms by construction

### 4.2 Task Families & Novelty Control

| Family | Resource Type | Training IDs | Novelty Levels (held-out IDs) |
|--------|---------------|--------------|-------------------------------|
| F1 | items | 001-005 | L0: 001-005 (novelty=0.0), L1: 006-010 (0.25), L2: 011-015 (0.50), L3: 016-020 (0.75) |
| F2 | users | 001-005 | Same structure |
| F3 | orders | 001-005 | Same structure |
| F4 | products | 001-005 | Same structure |

**Novelty fraction definition**: Proportion of task steps/parameters NOT covered by mechanisms in registry.
- L0 (0.0): Exact training identifiers — full registry coverage
- L1 (0.25): Adjacent identifiers — parameter slot varies, path template matches
- L2 (0.50): Mid-range identifiers — parameter slot + minor path variation
- L3 (0.75): Far identifiers — parameter slot + significant path/body variation

**Tasks per family per level**: 5 (20 tasks per family, 80 total)
**Total task executions**: 80 tasks × 4 arms = 320 executions

### 4.3 Arms (Mechanism Architecture Separation)

| Arm | Mechanism | Registry Access | Parameter Binding |
|-----|-----------|-----------------|-------------------|
| **T-SPIDER-PARAM** | `kernel.distill_parameterized` → `resolve` → `execute` | Full registry (induced mechanisms from training) | Parameter slots from induction |
| **B-COLD-RE-DERIVE** | Direct URL construction from task spec | **None** | None (fully specified) |
| **B-RETRIEVAL-SHAPED** | Embedding retrieval (cosine) → template bind → execute | Full registry (mechanisms as templates) | Retrieved template slots |
| **B-EMPTIED-REGISTRY** | T-SPIDER-PARAM code path with **registry cleared** | **Empty** | Falls back to cold (no match) |
| **PC-EXACT-REPLAY** | T-SPIDER-PARAM on training IDs | Full registry | Exact training match |

### 4.4 Accounting Surface (Per-Task, Honest)

Every arm emits identical counters to `raw_evidence/accounting_counters.jsonl`:
- `http_requests` (integer)
- `verification_calls` (integer)
- `repair_attempts` (integer)
- `latency_ms` (integer, wall-clock)
- `success` (boolean)
- `bound_action_correct` (boolean, for executed tasks)

**No injected counter events.** Counters fire on real execution only.

### 4.5 Verification (Deterministic, Mechanical, No LLM)

Each task spec includes a **mechanical verify function**: `verify(task_id, trajectory) -> bool`
- Checks: HTTP status, response body schema, expected fields, idempotency where applicable
- No LLM judge, no semantic evaluation, fully deterministic
- Same verify function used for all arms

### 4.6 Known Negatives (Refusal Test)

5 declared negative task specs per family (20 total):
1. Out-of-support identifier (e.g., `item-999`)
2. Missing required parameter
3. Wrong intent (task spec maps to no mechanism)
4. Unseen resource type (e.g., `invoices`)
5. Malformed request body

**All arms must refuse** with `bound_action=null` and non-empty `reason`. Refusal rate must = 1.0.

---

## 5. Dynamic Range Certificate (PRE-FREEZE, MANDATORY)

**Before `freeze.json` is written**, the harness MUST execute a **dynamic range certification run**:

1. Run B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED on all 80 tasks
2. Compute success_rate per arm per family at novelty ≥ 0.5 (levels L2, L3)
3. **Certificate passes** iff: ∃ at least one family where **BOTH** cold_success < 0.95 **AND** retrieval_success < 0.95 at novelty ≥ 0.5
4. Certificate result recorded in `spec.json.dynamic_range_certified` (true/false) and `spec.json.dynamic_range_certificate` object
5. **If certificate fails → experiment is MEASUREMENT_INVALID, must not freeze, must redesign task bank**

This certificate is **not optional**. It is a frozen gate. The Director's mandate requires it.

---

## 6. Decision Rule (Frozen, Exact)

### Primary Gate (all must pass for SUPPORTS)

| Condition | Test | Threshold |
|-----------|------|-----------|
| C1 | Dynamic range certified | `spec.json.dynamic_range_certified == true` |
| C2 | Matched correctness | All 4 arms: success_rate ≥ 0.80 on ≥ 3/4 novelty levels |
| C3 | Cost advantage vs cold grows with novelty | Spearman ρ > 0.5, permutation p < 0.05 (10,000 perms) |
| C4 | Cost advantage vs retrieval grows with novelty | Spearman ρ > 0.5, permutation p < 0.05 (10,000 perms) |
| C5 | Advantage at highest novelty | T-SPIDER-PARAM cost_per_success < B-COLD-RE-DERIVE (p<0.05) **AND** < B-RETRIEVAL-SHAPED (p<0.05) at novelty ≥ 0.7 |

### Secondary Gate (must pass for clean interpretation)

| Condition | Test | Threshold |
|-----------|------|-----------|
| S1 | Null matches cold | B-EMPTIED-REGISTRY ≈ B-COLD-RE-DERIVE cost_per_success at all levels (paired perm p > 0.05) |
| S2 | Positive control | PC-EXACT-REPLAY success_rate = 1.0 for all arms |
| S3 | Known negatives | Refusal rate = 1.0 for all arms, non-empty reasons |
| S4 | Support boundary | Refusal pattern on 006-020 characterized (contiguous sequence generalization) |

---

## 7. Metrics (Stable Identities for Downstream)

| Metric ID | Definition | Unit |
|-----------|------------|------|
| `cost_per_success` | Mean(http_requests + verification_calls + repair_attempts) / success_count | composite cost units |
| `cost_advantage_vs_cold` | B-COLD-RE-DERIVE.cost_per_success - T-SPIDER-PARAM.cost_per_success | composite cost units |
| `cost_advantage_vs_retrieval` | B-RETRIEVAL-SHAPED.cost_per_success - T-SPIDER-PARAM.cost_per_success | composite cost units |
| `success_rate` | successful_executions / total_attempts | [0,1] |
| `spearman_rho_cold` | ρ(cost_advantage_vs_cold, novelty_fraction) | [-1,1] |
| `spearman_rho_retrieval` | ρ(cost_advantage_vs_retrieval, novelty_fraction) | [-1,1] |
| `perm_p_cold` | Permutation p-value for spearman_rho_cold | [0,1] |
| `perm_p_retrieval` | Permutation p-value for spearman_rho_retrieval | [0,1] |
| `refusal_rate` | known_negative_refusals / known_negative_attempts | [0,1] |

All metrics computed per-arm, per-novelty-level, per-family, then aggregated.

---

## 8. Validity Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| Ceiling effects (predecessor's failure) | PRE-FREEZE dynamic range certificate (C1); task bank designed for headroom |
| Retrieval comparator too weak | B-RETRIEVAL-SHAPED uses same registry as T-SPIDER-PARAM; embedding retrieval is strong baseline |
| Registry induction variance | Training identifiers fixed (001-005); induction deterministic given training set |
| Support boundary confound | Explicit characterization (S4); held-out IDs systematically spaced |
| Accounting dishonesty | Identical counter surface for all arms; raw_evidence preserved; audit recomputes |
| Substrate drift | Same harness/substrate.py as EXP-PRODUCT-37973256064; server_log.jsonl preserved |
| Multiple comparisons | Primary gate is conjunctive (all 5 conditions); permutation tests control Type I |

---

## 9. Product Consequences (Frozen)

### If SUPPORTS:
- C-RESIDUAL-NOVELTY advances to **EXPERIMENTAL** with measured cost/novelty curve
- Dynamic-range task bank + accounting surface become **product infrastructure** for C-LLM-INHERIT benchmark
- Kernel parameterized path (src/spider/kernel.py) validated as **treatment carrier** for four-arm benchmark when credential provisions

### If FALSIFIES:
- "Pay for novelty, not whole task" premise **rejected for this architecture on this substrate**
- Product must **change architecture** (different parameterization, retrieval, cost model) rather than continue incremental fixes
- C-RESIDUAL-NOVELTY set to **REJECTED**
- Dynamic-range task bank **retained** for future architectures

### If MEASUREMENT_INVALID:
- Dynamic range certificate failed or infrastructure failure
- No claim update; task bank redesigned and re-frozen

---

## 10. Inheritance from Parent Handoff (EXP-PRODUCT-37973256064)

| Category | Items Preserved |
|----------|-----------------|
| **Established** | Parameterized path LIVE on real substrate; substrate validity; causal attribution; honest accounting; known-negative refusal; treatment 0.80 bounded by support regex |
| **Rejected** | Hypothesis that treatment advantage >0.15 on zero-headroom task family (structurally unreachable) |
| **Unknown** | Whether treatment beats cold/retrieval on headroom task bank; support generalization; real LLM benefit (C-LLM-INHERIT); model credential provisioning; repair/amortized behavior |
| **Do Not Assume** | FALSIFIES ≠ evidence against parameterized inheritance; 0.80 ≠ architecture ceiling; cold/retrieval 1.0 ≠ retrieval substitutes for inheritance; no C-LLM-INHERIT evidence; no promotion |

---

## 11. Artifacts to Preserve (Stable Paths)

- `raw_evidence/task_trajectories.jsonl` — per-task execution records
- `raw_evidence/accounting_counters.jsonl` — per-task honest counters
- `raw_evidence/induced_mechanisms.json` — induced mechanisms from training
- `raw_evidence/known_negatives.jsonl` — refusal records
- `raw_evidence/server_log.jsonl` — HTTP cycles
- `derived/arm_metrics.json` — aggregated per-arm metrics
- `derived/decision_rule_eval.json` — frozen decision rule evaluation
- `derived/dynamic_range_cert.json` — certification record (PRE-FREEZE)

---

## 12. Pre-freeze Checklist (Harness Must Verify)

- [ ] Dynamic range certificate computed and `spec.json.dynamic_range_certified = true`
- [ ] All 4 arms executable on all 80 tasks (no import errors, no crashes)
- [ ] Mechanical verify() deterministic and identical for all arms
- [ ] Accounting counters fire identically across arms
- [ ] Known negatives refused by all arms
- [ ] PC-EXACT-REPLAY success_rate = 1.0 on training IDs
- [ ] `freeze.json` hashes match request.json, spec.json, prereg.md

---

**This preregistration is frozen upon `freeze.json` creation. No outcome data may be inspected before freeze. The dynamic range certificate is a hard gate: if `dynamic_range_certified != true` at freeze time, the experiment is MEASUREMENT_INVALID and must not proceed to EXECUTE.**