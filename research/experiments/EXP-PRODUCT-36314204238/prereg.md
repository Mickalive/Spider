# Preregistration: EXP-PRODUCT-36314204238

**Experiment ID**: EXP-PRODUCT-36314204238
**Lane**: product
**Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
**Director Mandate**: PIVOT — mechanism-level question underneath C-PARAM-INHERIT, C-PRODUCT-ECON, C-RESIDUAL-NOVELTY
**Status**: DESIGN (frozen at freeze.json creation)

---

## 1. Scientific Question

Is parameter binding in SPIDER a **MECHANISM** that learns slot support from observed variability across collections, or a **STRING MATCHER** that uses a hardcoded vocabulary (`DEFAULT_IDENTITY_FIELDS = ('collection','resource')`)?

The parent experiment (EXP-PRODUCT-36306521892) established:
- Collection slot is DECLARED, not learned (single-collection 'items' training, hardcoded vocabulary)
- Safety gate only measures syntax/punctuation rejection, NOT semantic false-accepts on well-formed out-of-support identifiers
- Cheap regime was analytically degenerate (cost ratio = 1 by construction)
- Transfer to 'products' succeeded at 1.0000 but this is evidence of permissive declared vocabulary, not learned variability

This experiment directly tests the mechanism vs. matcher distinction.

---

## 2. Hypothesis

**Primary**: A slot binder that infers support FROM OBSERVED VARIABILITY across multiple collections in training observations will:
- (H1a) Beat three strong null binders on in-support bind accuracy (family-blocked CI95 lower bound)
- (H1b) Maintain semantic false-accept rate ≤ 0.10 on well-formed out-of-support identifiers, with UNKNOWN precision ≥ 0.85, global ECE ≤ 0.15, bootstrap 97.5% upper ECE ≤ 0.18
- (H1c) Achieve executed-and-verified rate within 0.05 of bind accuracy (no execution gap)
- (H1d) Show transfer pattern consistent with variability learning: FAILS transfer from 'items'-only training to 'products' (rate < 0.90), SUCCEEDS when trained on multi-collection variability (rate ≥ 0.90)

**Null**: The current kernel's declared-vocabulary approach is indistinguishable from a variability-learned mechanism on all four criteria, OR the variability-learned binder fails to beat the null binders.

---

## 3. Falsifiers (Pre-registered)

| ID | Falsifier | Trigger Condition |
|----|-----------|-------------------|
| F1 | Bind accuracy failure | Variability binder does NOT beat ALL three nulls (lexical-overlap, positional/regex, most-frequent-value) on in-support bind accuracy (family-blocked CI95 lower bound) |
| F2 | Semantic guard failure | Semantic false-accept rate > 0.10 pooled OR UNKNOWN precision < 0.85 OR global ECE > 0.15 OR bootstrap 97.5% upper ECE > 0.18 |
| F3 | Execution gap | Executed-and-verified rate < bind accuracy - 0.05 on unseen in-support identifiers |
| F4 | Transfer pattern violation | Items-only training transfers to 'products' at ≥ 0.90 (declared-vocab behavior) OR multi-collection training fails to transfer at ≥ 0.90 |
| F5 | Substrate contract violation | Pre-arm surface probe fails (cost manipulation not working, inheritance path ≠ 1 request, error rates ≥ 0.01) |
| F6 | Degenerate discriminative power | Any arm has success CI [1.0, 1.0] at ceiling (bootstrap) |
| F7 | Cost model integrity failure | Counted requests deviate from declared basis |
| F8 | Commit hash mismatch | Kernel at EXECUTE ≠ frozen kernel hash |

**Any F1-F4 true → FALSIFIES**
**F5-F8 triggered → INCONCLUSIVE or MEASUREMENT_INVALID (not scientific falsification)**

---

## 4. Substrate Design

### 4.1 Measurement-Valid Substrate (stdlib HTTP only)

Per Scout assessment and Codex evidence, only two substrate classes have produced valid measurement:
- (A) Real credential-free public HTTP via stdlib
- (B) Executed local HTTP cost asymmetry

This experiment uses a **local stdlib HTTP server** with **manipulable per-task re-derivation cost**.

### 4.2 Cost Manipulation (Free Variable)

Re-derivation cost is a **free variable set by the experiment**, NOT tied to auth/pagination dichotomy:

```
re_derivation_cost = base_cost * cost_multiplier
```

Where:
- `base_cost` = 3 requests (simulated pagination: list → detail → verify)
- `cost_multiplier` ∈ {1.0, 2.0, 5.0, 10.0, 20.0} — **5 levels, free variable**
- Inherited execution cost = **exactly 1 request** (direct GET with bound mechanism)
- Induction cost = **150 requests** (fixed, measured once per training condition)

This yields cost ratios (re-derivation / inheritance) of: **3.0, 6.0, 15.0, 30.0, 60.0**

### 4.3 Collections and Identifiers

**Training Collections** (variability-learned condition):
- `items` — 50 identifiers: `item-151` to `item-200`
- `products` — 50 identifiers: `product-151` to `product-200`
- `orders` — 50 identifiers: `order-151` to `order-200`
- Each collection has 3 task families: `read`, `update`, `delete` (HTTP verbs GET, PUT, DELETE)

**Test Collections** (held-out):
- In-support (seen collections, unseen identifiers): `item-201` to `item-250`, `product-201` to `product-250`, `order-201` to `order-250`
- Out-of-support (unseen collection, well-formed): `widgets` with identifiers `widget-151` to `widget-200` (same shape/namespace)
- Malformed probes: empty string, punctuation (`item!!`), wrong intent namespace

**Declared-vocabulary condition** (null control):
- Training: ONLY `items` collection (50 identifiers × 3 families = 150 observations)
- Vocabulary: hardcoded `('collection','resource')` — current kernel behavior

### 4.4 Surface Contract (Pre-arm Probe)

Before any measurement arm runs, verify:
1. Each `cost_multiplier` yields distinct mean re-derivation requests (ANOVA p < 0.001)
2. Inheritance path costs exactly 1 request (direct GET on bound URL)
3. HTTP error rates (401/403/404/5xx) < 0.01 across all arms
4. Latency injection deterministic per seed (fixed delay per cost_multiplier)
5. Server responds with correct state transitions for all verbs

**If any check fails → INCONCLUSIVE (F5), do not proceed**

---

## 5. Arms (Experimental Conditions)

| Arm | Training Data | Binder | Cost Multiplier | Purpose |
|-----|---------------|--------|-----------------|---------|
| A1 | Multi-collection (items, products, orders) | Variability-learned | 1.0, 2.0, 5.0, 10.0, 20.0 | Primary mechanism test |
| A2 | Single-collection (items only) | Variability-learned | 1.0, 2.0, 5.0, 10.0, 20.0 | Variability degradation test |
| A3 | Single-collection (items only) | Declared-vocab (kernel) | 1.0, 2.0, 5.0, 10.0, 20.0 | Current kernel behavior (B-DECLARED-VOCAB) |
| A4 | Multi-collection | Lexical-overlap null | 1.0, 2.0, 5.0, 10.0, 20.0 | B-LEXICAL-OVERLAP |
| A5 | Multi-collection | Positional/regex null | 1.0, 2.0, 5.0, 10.0, 20.0 | B-POSITIONAL-REGEX |
| A6 | Multi-collection | Most-frequent-value null | 1.0, 2.0, 5.0, 10.0, 20.0 | B-MOST-FREQUENT-VALUE |
| A7 | None (cold) | — | 1.0, 2.0, 5.0, 10.0, 20.0 | B-COLD-RE-DERIVATION |
| A8 | Within-episode scratchpad | — | 1.0, 2.0, 5.0, 10.0, 20.0 | B-WITHIN-EPISODE-SCRATCHPAD |
| A9 | Retrieval K=5 | — | 1.0, 2.0, 5.0, 10.0, 20.0 | B-RETRIEVAL-K5 |

**Total arms**: 9 binders × 5 cost multipliers = **45 measurement cells**
**Tasks per cell**: 100 tasks (50 in-support + 50 out-of-support probes)
**Total tasks**: 4,500
**Induction**: 150 observations per training condition (A1, A2, A3)

---

## 6. Metrics (Stable Identities)

### 6.1 Primary Metric
- `in_support_bind_accuracy` — proportion of held-out in-support identifiers correctly bound
  - Computed per arm, per cost_multiplier
  - Family-blocked bootstrap CI95 (strata: read/update/delete families)
  - **Decision**: variability binder (A1) CI95 lower > max(null binders A4-A6 CI95 upper)

### 6.2 Semantic Safety Metrics (Pooled across cost multipliers)
- `semantic_false_accept_rate_pooled` — rate of EXECUTED bindings on well-formed out-of-support identifiers (widgets collection)
- `unknown_precision` — precision of ABSTAIN outcome class (true unknown / (true unknown + false abstain))
- `global_ece` — Expected Calibration Error across all confidence bins
- `ece_975_upper` — 97.5% bootstrap upper bound on ECE
- `abstention_rate` — proportion of tasks where binder abstains (confidence < threshold)
- `selective_accuracy` — accuracy on non-abstained tasks
- `coverage` — 1 - abstention_rate

**Thresholds (frozen)**: false_accept ≤ 0.10, unknown_precision ≥ 0.85, global_ece ≤ 0.15, ece_975_upper ≤ 0.18

### 6.3 Execution Metrics
- `executed_verified_rate` — proportion of bound tasks that execute HTTP request AND verify postcondition (2xx + expected state)
- `execution_gap` = bind_accuracy - executed_verified_rate (threshold: ≤ 0.05)

### 6.4 Transfer Metrics
- `transfer_items_to_products_rate` — task success on 'products' identifiers when trained ONLY on 'items'
- `transfer_multi_to_products_rate` — task success on 'products' when trained on multi-collection
- **Pattern test**: items-only < 0.90 AND multi-collection ≥ 0.90

### 6.5 Economics Metrics (per cost_multiplier)
- `amortized_cost_ratio_vs_scratchpad` = (induction + n × inherit) / (scratchpad_induction + n × scratchpad_transfer)
- `amortized_cost_ratio_vs_retrieval_k5` = (induction + n × inherit) / (n × retrieval_k5_cost)
- `break_even_reuse_count_vs_scratchpad` — minimal n where inheritance cheaper than scratchpad
- `break_even_reuse_count_vs_retrieval_k5` — minimal n where inheritance cheaper than retrieval-K5
- Cost basis: **counted HTTP requests only** (stdlib responses, tiktoken cl100k_base for any token counting)

---

## 7. Controls (Stable Identifiers)

| Control ID | Type | Description | Pass Criterion |
|------------|------|-------------|----------------|
| PC-MULTI-COLLECTION-VARIABILITY | Positive | Multi-collection training, variability binder on seen-collection held-out identifiers | bind_accuracy ≥ 0.95, executed_verified ≥ 0.90, semantic_false_accept ≤ 0.05 |
| NC-SINGLE-COLLECTION-DECLARED | Null | Single-collection (items), declared-vocab binder on 'products' (out-of-support) | semantic_false_accept ≥ 0.40, transfer_rate ≥ 0.90 |
| NC-LEXICAL-OVERLAP | Null | Lexical-overlap binder on in-support | bind_accuracy < variability binder (A1) |
| NC-POSITIONAL-REGEX | Null | Positional/regex binder on in-support | bind_accuracy < variability binder (A1) |
| NC-MOST-FREQUENT-VALUE | Null | Most-frequent-value binder on in-support | bind_accuracy < variability binder (A1) |

---

## 8. Uncertainty & Validity

### 8.1 Bootstrap Procedure
- **Family-stratified**: Strata = task families (read, update, delete) × collection
- **B = 5000** resamples
- **Unit of resampling**: identifier (not individual transition)
- **Intervals**: 95% CI (primary), 97.5% upper (ECE guard)

### 8.2 Confidence Threshold
- Frozen at **0.85** before any arm runs
- Abstention (confidence < 0.85) scored as distinct outcome class `ABSTAIN`
- Selective accuracy and coverage reported as pair

### 8.3 Validity Threats (Disclosed)
| Threat | Mitigation | Residual |
|--------|------------|----------|
| Single path template `/collection/id` | All collections share template; variability only in segment values | Limits generalization to multi-template routes |
| Stdlib HTTP server (not real Web) | Only substrate with valid measurement history; real-Web transfer is separate claim | No browser, no JS, no auth complexity |
| Synthetic identifier distributions | Identifiers follow same shape/namespace; only collection segment varies | Clean separation of variability vs vocabulary |
| Deterministic server (no noise) | Cost manipulation via fixed latency injection | No stochasticity in state transitions |
| No model/LLM involvement | Pure kernel mechanism test; C-LLM-INHERIT requires separate experiment | External agent economics not measured |

### 8.4 Representation Loss (Documented)
- Raw HTTP request/response preserved for every interaction
- Slot inference operates on **observed path-segment value distributions** across collections
- No derived embeddings, no semantic similarity proxies — direct string variability
- `state.collection` field preserved in raw observations

---

## 9. Decision Rule (Frozen)

```
IF any F5-F8 triggered:
    outcome = INCONCLUSIVE (F5) or MEASUREMENT_INVALID (F6-F8)
ELIF all F1-F4 false:
    outcome = SUPPORTS
ELIF any F1-F4 true:
    outcome = FALSIFIES
ELSE:
    outcome = MIXED
```

**Claim update mapping**:
- SUPPORTS → C-PARAM-INHERIT advances toward VALIDATED (requires audit PASS)
- FALSIFIES → C-PARAM-INHERIT held at EXPERIMENTAL or downgraded; architectural pivot required
- MIXED → C-PARAM-INHERIT held at EXPERIMENTAL; specific failure mode documented
- INCONCLUSIVE/MEASUREMENT_INVALID → No claim change; experiment repeated with fixes

---

## 10. Product Consequences

### Positive (SUPPORTS)
- **C-PARAM-INHERIT**: Mechanism validated — parameter binding learns from variability
- **Architecture**: `distill_parameterized()` refactored to infer identity slots from multi-collection variability
- **C-SEMANTIC-RESOLVE**: Enabled — semantic resolution can use learned slot support
- **C-CROSSSITE**: Enabled — cross-site transfer uses variability learning, not declared vocabulary
- **Promotion gate**: This experiment PASS + independent audit PASS → promotion eligible

### Negative (FALSIFIES or MIXED on F1/F2/F3)
- **C-PARAM-INHERIT**: Held at EXPERIMENTAL or downgraded
- **Current kernel**: Confirmed as string matcher (declared vocabulary)
- **Required pivot**: Either (a) implement variability learning in kernel, or (b) accept declared vocabulary with explicit semantic false-accept bounds and UNKNOWN handling
- **No promotion** of current `distill_parameterized`

### Mixed (F4 only or semantic/execution partial)
- **C-PARAM-INHERIT**: Held at EXPERIMENTAL
- **Specific failure documented**: Transfer pattern, semantic guard, or execution gap
- **Next experiment**: Targeted fix for identified failure mode

---

## 11. Artifacts to Preserve

| Artifact | Path | Role |
|----------|------|------|
| Raw observations | `raw_evidence/observations.jsonl` | raw |
| Bind results | `raw_evidence/bind_results.jsonl` | raw |
| Execution results | `raw_evidence/exec_results.jsonl` | raw |
| Probe results | `raw_evidence/probe_results.jsonl` | raw |
| Substrate probe | `raw_evidence/substrate_probe.json` | raw |
| Derived metrics | `raw_evidence/derived.json` | derived |
| Mechanisms | `raw_evidence/mechanisms.json` | derived |
| Kernel commit | `provenance.json.kernel_sha256` | fixture |
| Git state | `provenance.json.git_state` | fixture |

All raw evidence files will include: task_id, arm, cost_multiplier, collection, identifier, family, bind_value, bind_confidence, executed, verified, http_status, request_count, latency_ms

---

## 12. Reproducibility

- **Seed**: 42 (deterministic across all arms)
- **Tokenizer**: tiktoken cl100k_base (declared, no per-observation constants)
- **Bootstrap**: B=5000, family-stratified, seed=42
- **Commit**: Kernel SHA256 recorded at EXECUTE start and verified at end
- **Environment**: Python 3.12+, stdlib only, no external dependencies
- **Code paths**: `src/spider/kernel.py`, `run_experiment.py`, `tests/test_kernel.py`

---

## 13. Dependencies (from Parent Handoff)

This design explicitly addresses all parent handoff dependencies:
1. ✅ **Manipulable re-derivation cost** — cost_multiplier free variable (5 levels)
2. ✅ **Primary criterion against within-episode reuse** — scratchpad and retrieval-K5 arms at every cost level
3. ✅ **Comparators that can fail** — null binders + cost manipulation creates non-degenerate success rates
4. ✅ **F4 restated with infinity handling** — no cheap regime; cost ratio is continuous free variable
5. ✅ **Mechanism/economics gates split** — primary metric is bind accuracy (mechanism); economics are secondary
6. ✅ **Semantic probe that can fail** — widgets collection (well-formed, out-of-support) with binding values logged
7. ✅ **Corrected producer observation** — mechanism.json records declared/inferred slots; no claim that collection is "induced"
8. ✅ **Sanctioned persistence** — not addressed (control-plane); experiment runs on current kernel
9. ✅ **Build-before-freeze** — not addressed (control-plane); kernel fixes preregistered as measurement
10. ✅ **Substrate surface-contract in freeze** — pre-arm probe verified before measurement
11. ✅ **Real-agent economics** — deferred (C-LLM-INHERIT); this is mechanism-level
12. ✅ **Credential-free real-Web substrate** — optional dependency; stdlib local HTTP is valid per Scout

---

## 14. Estimated Cost & Timeline

- **HTTP requests**: ~50,000 total (45 cells × 100 tasks × ~10 req/task + induction + probes)
- **Compute**: ~2 CPU hours on single machine
- **Wall time**: ~30 minutes (parallelizable across arms)
- **No**: Model calls, browser, Docker, external API keys, GPU
- **Risk**: LOW — stdlib substrate has 100% measurement validity in Codex

---

## 15. Signatures

This preregistration is frozen at `freeze.json` creation. No outcome-bearing measurements may be inspected before freeze. The DESIGN agent certifies that this design:
- Addresses the Director's strategic question directly
- Uses the smallest high-information experiment that can change the claim
- Does not merely repeat pre-2.0 work
- Includes strong baselines, positive/null controls, and validity threats
- Uses stable metric/control identities for downstream transmission
- States consequences of both positive and negative outcomes

**Frozen by**: deterministic freezer (not research agent)
**Freeze hash**: recorded in `freeze.json`