# EXP-PRODUCT-36306521892 Preregistration

**Experiment ID:** EXP-PRODUCT-36306521892
**Lane:** product
**Claim IDs:** C-PRODUCT-ECON, C-PARAM-INHERIT
**Director Mandate:** PIVOT with cognitive_reset to C-PRODUCT-ECON
**Base SHA:** 4682030b49d96a0dc1c4a7522ed767ac0efcc3d6
**Created:** 2026-09-27T08:32:55.939413+00:00

---

## 1. Strategic Question (from Director Mandate)

What is the break-even reuse count f* at which persistent inheritance actually costs less than re-deriving the same operational knowledge, measured end-to-end in two regimes:

1. **Costly-re-derivation regime**: multi-step auth, pagination traversal, schema discovery — cold episode provably costs >1 request/task
2. **Cheap-re-derivation regime**: credential-free read-only class SPIDER actually reached — cold episode costs 1 request/task

Does f* differ between regimes by enough to justify a per-object persistence policy instead of unconditional persistence?

---

## 2. Hypothesis

A mechanism induced from observations of resource A (`items` collection) in the cheap regime, with parameter slots induced by `distill_parameterized()` reaching confidence ≥ `min_confidence` (0.8) through the **committed kernel at HEAD**, will transfer to never-observed resource B (`products` collection) with disjoint identifier namespace.

- In the **costly regime**, the amortized cost ratio `(induction_cost + n × transfer_cost) / (n × B-COLD-COSTLY)` will fall ≤ 0.85 at some reuse count `f*_costly`.
- In the **cheap regime**, the same ratio against `B-COLD-CHEAP` will fall ≤ 0.85 at `f*_cheap`.
- The ratio `f*_costly / f*_cheap` will exceed 2.0, demonstrating that persistence policy should be regime-dependent.
- **Mandatory safety**: `abstention_precision ≥ 0.95` on negative probes and `false_accept_rate ≤ 0.10` on out-of-support bindings in BOTH regimes.
- **Task success** ≥ 0.95 for INHERITANCE arm in BOTH regimes.

---

## 3. Falsifiers (Pre-registered)

The hypothesis is **falsified** if ANY of the following hold:

| ID | Condition | Rationale |
|----|-----------|-----------|
| F1 | INHERITANCE arm task success < 0.95 in either regime | Transfer fails |
| F2 | `abstention_precision < 0.95` OR `false_accept_rate > 0.10` in either regime | Safety gate failed — architectural liability |
| F3 | `amortized_cost_ratio(INHERITANCE vs B-COLD) > 0.85` at maximum executed reuse count in either regime | Economics fail |
| F4 | `f*_costly / f*_cheap ≤ 2.0` | No meaningful regime difference — unconditional persistence not justified |
| F5 | Kernel `distill()` path does not reach `EXECUTABLE` for any induced mechanism | Durability precondition fails — cannot test economics without working induction |
| F6 | `B-COLD-COSTLY` mean requests/task ≤ 1.0 | Costly regime not actually costly |
| F7 | `B-COLD-CHEAP` mean requests/task > 1.5 | Cheap regime not actually cheap |
| F8 | Any cost component uses imported per-observation constants, jitter, or f-scaled substitution instead of substrate's own responses under the declared tokenizer | Cost accounting invalid |

---

## 4. Substrate Design (Dual-Regime)

A single in-process HTTP substrate (`substrate.py`) with **two operating modes**, serving the same resource structure:

### Resource Structure
- **Resource A (training):** `/items/{id}` — 200 identifiers `item-1` .. `item-200`
- **Resource B (transfer):** `/products/{id}` — 126 identifiers `SKU-A`..`SKU-Z`, `PROD-100`..`PROD-199`
- **Namespaces disjoint by construction** — zero string overlap

### Costly Regime (Mode: `costly`)
| Feature | Behavior |
|---------|----------|
| Auth | POST `/auth/login` → Bearer token; token expires after 100 requests (monotone counter); no issuance endpoint (401) |
| Schema discovery | GET `/schema` → returns verb/method/body templates |
| Pagination | GET `/items?page=N&page_size=10` → must iterate to find item |
| Item access | GET/PUT/DELETE `/items/{id}` requires valid token |
| Session-scoped responses | Same entity returns different `session`/`visible_to` per token |
| ETag/304 | Supported for conditional GET |

### Cheap Regime (Mode: `cheap`)
| Feature | Behavior |
|---------|----------|
| Auth | None — all endpoints public |
| Schema | Known a priori — no discovery needed |
| Pagination | None — direct access |
| Item access | GET `/products/{id}` returns item directly (1 request) |
| Session-scoped responses | Disabled — same response for all |
| ETag/304 | Not applicable |

**Mode switching:** Substrate instantiated with `mode="costly"` or `mode="cheap"`. Arms run against one mode at a time. Substrate `reset()` between arms.

### Surface Contract Verification (Pre-arm Probe)
Before any arm runs, a probe verifies:
- Costly mode: `/auth/login` returns token, `/schema` returns verbs, `/items?page=1` paginates, token expires at 100
- Cheap mode: `GET /products/SKU-A` returns 200 with item, no auth header required, no pagination

If probe fails → **MEASUREMENT_INVALID** (substrate contract not met).

---

## 5. Arms (Treatments & Baselines)

### 5.1 Inheritance Arm (Primary Treatment)
- **Name:** `INHERITANCE`
- **Induction:** 50 observations from resource A (`items`) across 3 families (read/update/delete) in **cheap regime** (accessible). 50 distinct identifiers × 3 families = 150 observations.
- **Induction method:** `kernel.distill_parameterized(training, mechanism_prefix="inherit")` — **must** produce mechanisms with `confidence ≥ 0.8` and `parameter_slots` induced (not hand-declared).
- **Transfer:** Mechanisms registered, then resolved on resource B (`products`) in **BOTH regimes** using intent namespace mapping (`read-item` → `read-product`, etc.).
- **Execution:** Resolved `bound_action` executed verbatim (verb from mechanism, not task family). Verified against `task_success` (verb AND status AND returned entity).
- **Cost accounting:** Induction cost = actual HTTP requests during observation collection. Transfer cost = actual HTTP requests per task.

### 5.2 Baselines (Per Regime)

| Arm ID | Description | Cost Basis |
|--------|-------------|------------|
| `B-COLD-COSTLY` | Per-task cold discovery: auth → schema → paginate → target verb | Counted HTTP requests |
| `B-COLD-CHEAP` | Per-task cold discovery: direct GET `/products/{id}` | Counted HTTP requests (expected 1) |
| `B-SCRATCHPAD-COSTLY` | Within-episode: task 1 pays cold cost, tasks 2..n reuse discovered schema/auth/paths (no registry) | Cold cost + (n-1)×1 |
| `B-SCRATCHPAD-CHEAP` | Within-episode: all tasks 1 request (no savings possible) | 1 request/task |
| `B-NO-MEMORY-COSTLY` | Deterministic executor: hard-coded auth+pagination per task, no registry | Full cold cost/task |
| `B-NO-MEMORY-CHEAP` | Deterministic executor: direct GET per task, no registry | 1 request/task |
| `B-INSTRUCTIONS-COSTLY` | Pre-provided instructions for auth/schema/pagination; agent executes per task | Instructions overhead + execution |
| `B-INSTRUCTIONS-CHEAP` | Pre-provided direct GET template; agent executes | 1 request + overhead |
| `B-RETRIEVAL-K5-COSTLY` | Retrieval K=5 over prior trajectories (deterministic hash-n-gram embedding); execute top match | Retrieval + execution |
| `B-RETRIEVAL-K5-CHEAP` | Retrieval K=5; execute top match | Retrieval + 1 request |

### 5.3 Controls

| Control | Description | Success Criterion |
|---------|-------------|-------------------|
| `PC-SAME-RESOURCE` | Induced mechanisms tested on held-out resource A identifiers (cheap regime) | Task success ≥ 0.95, resolution `EXECUTABLE` via `distill_parameterized` |
| `NC-SHUFFLED-INTENT` | Training labels shuffled, then `distill_parameterized` induced | Abstains (`EXPLORE`/`UNKNOWN`) on all probes; induced confidence < 0.8 |
| `NC-FALSE-ACCEPT` | Probes: out-of-support bindings (`SKU-X!!unsupported!!`), empty-string bindings, invalid intents | `false_accept_rate ≤ 0.10`, `abstention_precision ≥ 0.95` |

---

## 6. Measurement & Cost Accounting

### Cost Basis (Single, Declared)
- **Tokenizer:** `tiktoken` encoding `cl100k_base` (or `word_count` if tiktoken unavailable — declared at runtime)
- **Request counting:** Every HTTP call issued by client counted via `Client.mark()` (includes re-auth charges per Amendment A1 from parent experiment)
- **Induction cost:** Sum of requests during `collect_observations()` — **counted, not estimated**
- **Response bodies:** Tokenized for any per-token cost accounting (though primary metric is request count)
- **No imported constants:** No per-observation cost constants from other packets. No jitter. No f-multiplied proxies.

### Unmeasurable Costs → Reported as UNKNOWN
| Cost Component | Status | Reason |
|----------------|--------|--------|
| Model calls / tokens | UNKNOWN | No `OPENAI_API_KEY` in environment; no LLM API available |
| Browser interactions / latency | UNKNOWN | Stdlib HTTP substrate only; no browser/Playwright |
| Verification / repair | UNKNOWN | No external auditor model; `verify()` only checks postconditions |
| Staleness / maintenance | UNKNOWN | Single-shot experiment; no longitudinal drift measurement |
| Retrieval embedding compute | UNKNOWN | Deterministic hash-n-gram embedding used; no model tokens |

---

## 7. Experimental Protocol

### 7.1 Kernel Preparation (Durability Precondition)
**BEFORE freeze / at EXECUTE start:**
1. Implement `distill_parameterized()` in `src/spider/kernel.py` (parameter induction with confidence calibration)
2. Commit to product branch with nonempty diff vs `base_sha`
3. Verify `git diff --stat base_sha..HEAD -- src tests` shows changes
4. Verify `tests/test_kernel.py` exercises `distill_parameterized()` → `EXECUTABLE` resolution (not hand-built `Mechanism` at confidence 0.95)
5. Run tests: `python -m pytest tests/test_kernel.py -v` → all pass
6. Record kernel SHA256 at HEAD for provenance

**If F5 triggers (kernel cannot reach EXECUTABLE from distill):** Experiment status = `INCONCLUSIVE` / `NOT_APPLICABLE`. No economics measurement possible.

### 7.2 Arm Execution Order (Per Regime)
For **each regime** (costly, cheap):
1. Probe substrate surface contract
2. `fresh(sub)` — reset substrate state, reseed both collections
3. `collect_observations()` in cheap regime (shared induction data)
4. Induce mechanisms via `distill_parameterized()` (shared across regimes)
5. Run arms in order (reset between each):
   - `B-COLD`
   - `B-SCRATCHPAD`
   - `B-NO-MEMORY`
   - `B-INSTRUCTIONS`
   - `B-RETRIEVAL-K5`
   - `INHERITANCE` (with mechanisms registered)
   - `PC-SAME-RESOURCE` (cheap regime only, on resource A held-out)
6. Run probes (`NC-SHUFFLED-INTENT`, `NC-FALSE-ACCEPT`) with appropriate registry

### 7.3 Negative Probes (Safety Measurement)
- 60 probes per control arm
- Kinds: `out_of_support_binding` (20), `invalid_intent` (20), `empty_string_binding` (20)
- `abstention_precision = 1 - (executed_probes / total_probes)` on `invalid_intent` probes
- `false_accept_rate = executed_probes / total_probes` on `out_of_support_binding` + `empty_string_binding`

---

## 8. Metrics & Derived Measurements

### Primary Metrics (Per Regime)
| Metric | Definition |
|--------|------------|
| `task_success_rate[arm]` | Fraction of tasks with verb AND status AND returned entity correct |
| `mean_requests_per_task[arm]` | Bootstrap mean (B=5000, family-stratified) |
| `amortized_cost_ratio[arm]` | `(induction_cost + n_transfer × transfer_cost) / (n_transfer × B-COLD_cost)` |
| `break_even_reuse_count f*` | Minimum n where `amortized_cost_ratio ≤ 1.0` (solved directly: `ceil(induction_cost / (B-COLD_cost - transfer_cost))`) |
| `abstention_precision[control]` | `1 - false_positive_rate` on `invalid_intent` probes |
| `false_accept_rate[control]` | `executed / total` on `out_of_support` + `empty_string` probes |

### Derived Measurements
- `f*_costly`, `f*_cheap` — break-even reuse counts
- `f*_ratio = f*_costly / f*_cheap` — regime difference factor
- `induction_cost_total` — counted HTTP requests during observation collection
- `reauths_total` — Amendment A1 re-authentication charges
- Per-family breakdowns (read/update/delete) for all metrics

---

## 9. Decision Rule (Frozen)

| Outcome | Condition |
|---------|-----------|
| **SUPPORTS** | ALL: (1) INHERITANCE task success ≥ 0.95 both regimes; (2) safety gate passes both regimes (`abstention_precision ≥ 0.95`, `false_accept_rate ≤ 0.10`); (3) `amortized_cost_ratio ≤ 0.85` at some executed n both regimes; (4) `f*_ratio > 2.0`; (5) `PC-SAME-RESOURCE` success ≥ 0.95 via `distill_parameterized`; (6) durability precondition met |
| **FALSIFIES** | Any falsifier F1–F8 triggers |
| **MIXED** | Some regimes pass primary criteria but not both; OR safety passes but economics fails one regime; OR `f*_ratio` inconclusive (e.g., one regime has no break-even) |
| **INCONCLUSIVE** | Measurement validity failure: substrate contract not met, <50 IDs/family/regime, bootstrap degenerate, kernel not committed |
| **NOT_APPLICABLE** | Durability precondition F5 fails — kernel `distill()` cannot reach `EXECUTABLE` |

**Safety gate is mandatory and non-tradeable:** A mechanism that removes work while silently replaying wrong actions is an architectural liability and cannot pass on cost alone.

---

## 10. Validity Threats & Disclosures

| Threat | Mitigation / Disclosure |
|--------|-------------------------|
| Substrate is self-authored stdlib HTTP server, not real Web | Acknowledged — measures *relative* economics on controlled substrate; real Web validation requires separate experiment |
| No LLM agent / model tokens | Reported as UNKNOWN; deterministic executor arms approximate `B-NO-MEMORY` baseline from mandate |
| Single tokenizer (cl100k_base) | Declared upfront; if unavailable, fallback to word count declared in `provenance.json` |
| Induction in cheap regime only | Mandate specifies "observations of resource A" — cheap regime is what SPIDER reaches; costly induction would be circular |
| Deterministic substrate (no noise) | Bootstrap captures sampling variance; no injected noise per mandate |
| `promote_to_product = false` → changes reverted | Mandated by Director; durability is precondition, not deliverable |
| Family diversity limited to verb + intent namespace | Resource shape identical across families (`/{collection}/{id}`); shape transfer tested via collection slot induction |

---

## 11. Artifacts to Produce (Raw Evidence)

| Path | Content |
|------|---------|
| `raw_evidence/observations.jsonl` | 150 training observations (intent, state, action, next_state, success) |
| `raw_evidence/task_results.jsonl` | Per-task rows for all arms × both regimes |
| `raw_evidence/probe_results.jsonl` | Per-probe rows for all controls |
| `raw_evidence/mechanisms.json` | Induced mechanisms (JSON with slots, confidence, templates) |
| `raw_evidence/derived.json` | All bootstrapped metrics, break-even counts, ratios, probe rates |
| `raw_evidence/substrate_probe.json` | Surface contract verification results per regime |

---

## 12. Dependencies (from Director Mandate)

1. **Durability precondition:** Kernel parameter-induction code committed at HEAD, hash-verified, tests reach `EXECUTABLE` via `distill()`.
2. **Frontier's C-CROSSSITE surface measurement:** Valuable input for cheap regime but NOT blocking — regime constructed directly here.
3. **Runtime's certified substrate:** May be used but NOT blocking — stdlib substrate constructed directly.
4. **Cost accounting:** Every unmeasurable cost component → UNKNOWN with reason. No proxies.
5. **Abstention/false-accept arm:** Mandatory, scored as own outcome class.
6. **Control-plane condition:** No frozen gate may require code digest/attestation; kernel durability attested by recorded commit SHA256 and nonempty diff at EXECUTE.

---

## 13. Prior Evidence Carried Forward (from Parent Handoff)

### Established (Preserved)
- Single-collection training pins collection segment → no transfer (Treatment 0.0000)
- Same pipeline transfers at 1.0000 when collection slot **declared** (diagnostic arm)
- First executed B-COLD: 4.08 requests/task, 1746 total requests, 14 re-auths
- Identity-slot mechanism amortized ratio 0.545 vs B-COLD (break-even at 50)
- `min_confidence` gate load-bearing: NC-SHUFFLED-INTENT abstained 126/126 at zero requests; forced → 84/126 wrong verb, 0.333 success
- Positive control works through shipped-kernel path (PC-SAME-RESOURCE 1.0000 via `distill_parameterized`)
- Substrate authentic but misdescribed (digest matches, endpoints differ)
- Control-plane defect: freeze gate cannot bind code (3 hashes only); design grants code only at execute

### Rejected (Bounded to Prior Run)
- Treatment 0.0000 ≠ prefix-preservation wrong or inheritance non-viable
- F2, F6, F9 as instruments (unsatisfiable/identity/penalizes abstention)
- B-LITERAL-REPLAY / B-RETRIEVAL-K5 as economic comparators (0 success)
- Null arm abstention_precision 1.0000 ≠ kernel safe (guards intent, not slots)
- F12 sample-size failure ≠ evidence about inheritance

### Unknown (Carried Forward)
- Durability of corrected kernel (reverted by `revert_product_reject.py`)
- Whether variability can be **learned** (not declared) from two resources
- Generalization beyond self-authored substrate
- Sound baseline with non-zero success
- Parent packet artifact discrepancy (transfer 1.0 at kernel with prefix-free template)
- Slot-value guard (false_accept_rate 0.5 on treatment arms)
- C-PRODUCT-ECON end-to-end gate reachability

### Do Not Assume (Explicit Non-Conclusions)
- C-PARAM-INHERIT NOT falsified NOR validated (held EXPERIMENTAL)
- Capability NOT durable (committed then reverted — 15th cycle)
- 0.5447 NOT a product-economics result (self-authored substrate, HTTP requests only)
- B-LITERAL-REPLAY HTTP-OK 1.0000 ≠ partial success (wrong entity, 0 task success)
- Null arm abstention_precision 1.0000 ≠ kernel safe/calibrated
- F2/F6/F9 NOT falsifier evidence
- Substrate digest ≠ design validation
- n=42/family NOT powered estimate
- Next experiment NOT authorized (Global Director decides)

---

## 14. Execution Checklist (for EXECUTE Agent)

- [ ] Implement `distill_parameterized()` in `src/spider/kernel.py`
- [ ] Commit kernel + tests to product branch; verify nonempty diff vs base_sha
- [ ] Run `pytest tests/test_kernel.py -v` → all pass (distill → EXECUTABLE)
- [ ] Record kernel SHA256 at HEAD
- [ ] Implement dual-regime `substrate.py`
- [ ] Run substrate surface probe for both regimes → verify contract
- [ ] Execute all arms in both regimes with `fresh()` between
- [ ] Collect raw evidence (JSONL + JSON)
- [ ] Compute derived metrics with family-stratified B=5000 bootstrap
- [ ] Write `result.json`, `report.md`, `provenance.json`
- [ ] Verify all falsifiers evaluated, decision rule applied
- [ ] Report UNKNOWN costs with reasons

---

## 15. Consequences of Outcomes

| Outcome | Claim Updates | Product Action |
|---------|---------------|----------------|
| **SUPPORTS** | C-PRODUCT-ECON → EXPERIMENTAL (measured f* in two regimes)<br>C-PARAM-INHERIT → EXPERIMENTAL (transfer confirmed) | Implement per-object persistence policy (persist when regime f* reachable). Next: test on real Web substrate. |
| **FALSIFIES** | C-PRODUCT-ECON → REJECTED (if economics fail both regimes)<br>C-PARAM-INHERIT → REJECTED (if F1/F5) OR HYPOTHESIS (if safety fails) | If safety fails: kernel unsafe — add slot-value guards. If economics fail: pivot to re-derivation + caching architecture. |
| **MIXED** | C-PRODUCT-ECON → EXPERIMENTAL (bounded)<br>C-PARAM-INHERIT → EXPERIMENTAL | Investigate regime where economics failed. Next: improve induction or substrate fidelity. |
| **INCONCLUSIVE / NOT_APPLICABLE** | C-PRODUCT-ECON → HYPOTHESIS<br>C-PARAM-INHERIT → EXPERIMENTAL (if kernel works) OR HYPOTHESIS (if F5) | Fix kernel induction (F5) or substrate contract. Re-run with valid measurement. |

---

**End of Preregistration.** This document is frozen at DESIGN. EXECUTE must follow exactly. No outcome-bearing measurements during DESIGN.