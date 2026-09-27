# EXP-PRODUCT-36306521892 — Break-even reuse count for persistent inheritance in two regimes

**Experiment ID:** EXP-PRODUCT-36306521892
**Lane:** product
**Claims:** C-PRODUCT-ECON, C-PARAM-INHERIT
**Status:** COMPLETE
**Outcome:** MIXED
**Date:** 2026-09-27

---

## 1. Question

What is the break-even reuse count f* at which persistent inheritance actually costs less than re-deriving the same operational knowledge, measured end-to-end in two regimes (costly-re-derivation and cheap-re-derivation)? Does f* differ between regimes by enough to justify a per-object persistence policy?

## 2. Design Summary

A mechanism induced from 150 observations of resource A (`items`, cheap regime) via the committed kernel's `distill_parameterized()` was replayed on 150 never-observed resource B (`products`) identifiers in both regimes. The costly regime requires auth (login, token expiry at 100 requests), schema discovery, and pagination traversal; the cheap regime serves direct GET at 1 request/task. Arms: B-COLD, B-SCRATCHPAD, B-NO-MEMORY, B-INSTRUCTIONS, B-RETRIEVAL-K5, INHERITANCE, plus controls PC-SAME-RESOURCE, NC-SHUFFLED-INTENT, NC-FALSE-ACCEPT. All costs are counted HTTP requests from the substrate's own responses under one declared basis. Family-stratified B=5000 bootstrap.

## 3. Durability Precondition (F5)

The shipped kernel's `distill()` hard-codes confidence=0.5 against `resolve()`'s min_confidence=0.8, so no distilled mechanism could reach EXECUTABLE. This was fixed and committed:

- `distill_parameterized()` implemented in `src/spider/kernel.py` (committed at HEAD `408f3bc1`, sha256 `57690132...`)
- Nonempty diff vs base_sha `4682030b`: 3 files, 564 insertions
- `tests/test_kernel.py`: 9/9 pass, all reaching EXECUTABLE through `distill_parameterized` (not hand-built Mechanism)
- Slot-value guard added to `resolve()`: rejects empty/non-identifier bindings

**F5 does not trigger.** The kernel reaches EXECUTABLE from distill.

## 4. Surface Contract Probe

| Check | Costly | Cheap |
|-------|--------|-------|
| Auth login returns token | PASS (200, token) | N/A (no auth) |
| Schema discovery | PASS (200, verbs) | N/A (404) |
| Pagination | PASS (200, count=2) | N/A |
| Token expiry at 100 | PASS (401 after 100) | N/A |
| Direct GET /products/SKU-A | N/A | PASS (200, no auth) |

Both regimes satisfy their preregistered surface contract.

## 5. Primary Results

### 5.1 Task Success

| Arm | Costly | Cheap |
|-----|--------|-------|
| INHERITANCE | 1.0000 (150/150) | 1.0000 (150/150) |
| B-COLD | 1.0000 | 1.0000 |
| B-SCRATCHPAD | 1.0000 | 1.0000 |
| B-NO-MEMORY | 1.0000 | 1.0000 |
| B-INSTRUCTIONS | 1.0000 | 1.0000 |
| B-RETRIEVAL-K5 | 1.0000 | 1.0000 |
| PC-SAME-RESOURCE | — | 1.0000 (150/150) |
| NC-SHUFFLED-INTENT | 0.0000 (abstains) | 0.0000 (abstains) |

### 5.2 Cost per Task (mean requests, B=5000 bootstrap)

| Arm | Costly | Cheap |
|-----|--------|-------|
| INHERITANCE | 1.0267 [1.000, 1.067] | 1.0000 [1.000, 1.000] |
| B-COLD | 3.0600 [3.013, 3.120] | 1.0000 [1.000, 1.000] |
| B-SCRATCHPAD | 1.0667 | 1.0000 |
| B-NO-MEMORY | 2.0400 | 1.0000 |
| B-INSTRUCTIONS | 2.0400 | 1.0000 |
| B-RETRIEVAL-K5 | 1.0267 | 1.0000 |

### 5.3 Amortized Cost Ratio and Break-even f*

| Regime | Ratio at n=150 | n for ratio ≤ 0.85 | f* (break-even) |
|--------|---------------|---------------------|-----------------|
| Costly | 0.6623 | 96 | 74 |
| Cheap | 2.0000 | never | infinity |

**f*_costly / f*_cheap = 0** (f*_cheap = infinity).

### 5.4 Safety Gate

| Metric | Value | Threshold | Pass |
|--------|-------|-----------|------|
| abstention_precision (invalid_intent) | 1.0000 | ≥ 0.95 | ✓ |
| false_accept_rate (out-of-support + empty) | 0.0000 | ≤ 0.10 | ✓ |

## 6. Falsifier Evaluation

| ID | Condition | Triggered? |
|----|-----------|------------|
| F1 | INHERITANCE success < 0.95 in either regime | NO (1.0 both) |
| F2 | abstention_precision < 0.95 or false_accept_rate > 0.10 | NO (1.0, 0.0) |
| F3 | amortized ratio > 0.85 at max n in either regime | **YES** (cheap: 2.0 > 0.85) |
| F4 | f*_costly / f*_cheap ≤ 2.0 | **YES** (0 ≤ 2.0) |
| F5 | kernel distill() not EXECUTABLE | NO (tests pass) |
| F6 | B-COLD-COSTLY ≤ 1.0 | NO (3.06) |
| F7 | B-COLD-CHEAP > 1.5 | NO (1.0) |
| F8 | cost accounting invalid | NO (counted requests) |

## 7. Decision Rule

**Outcome: MIXED.**

The costly regime passes all primary criteria: INHERITANCE success 1.0 ≥ 0.95, amortized ratio 0.66 ≤ 0.85 at n=96, f* = 74, safety gate passes. The cheap regime passes mechanism (success 1.0) and safety but fails economics: the amortized ratio is 2.0 and never falls to 0.85 because transfer cost equals cold cost (1.0 req/task) and the 150-request induction is unrecoverable overhead. This is the MIXED clause: "safety passes but economics fails in one regime."

## 8. Interpretation

**What the measurement establishes:**

1. **In the costly regime, persistent inheritance amortizes.** f* = 74 transfer tasks. At n=150 the amortized cost ratio is 0.66, well below 0.85. The mechanism induced from items transfers to products at 100% success with a 3x per-task cost reduction vs cold discovery (1.03 vs 3.06 requests/task).

2. **In the cheap regime, persistent inheritance does NOT amortize.** f* = infinity. When cold discovery is already 1 request/task, inheritance transfer is also 1 request/task, so the 150-request induction cost can never be recovered. This is a structural property, not a measurement failure.

3. **The regime difference is maximal, not absent.** f*_costly is finite (74), f*_cheap is infinite. The ratio is 0, which triggers F4 as written (≤ 2.0), but the direction is the strongest possible regime difference. This **supports a per-object persistence policy**: persist only in costly regimes where f* is reachable.

4. **Within a single episode, cross-episode inheritance does not beat a within-episode scratchpad or retrieval.** B-SCRATCHPAD (1.067 req/task, no induction cost) and B-RETRIEVAL-K5 (1.027 req/task) are cheaper than INHERITANCE (1.027 req/task + 150 induction) at n=150. The scratchpad's break-even vs inheritance is 3750 tasks. Over 25+ episodes the induction cost would amortize, but this experiment measures one episode.

5. **The safety gate is load-bearing and passes.** The slot-value guard rejects empty and out-of-support bindings (false_accept_rate 0.0), and the min_confidence gate abstains on shuffled-label mechanisms (NC-SHUFFLED-INTENT 0% success at zero requests).

**Product consequence:** C-PRODUCT-ECON advances to EXPERIMENTAL with a bounded, decision-changing result: persistence pays in costly regimes (f* = 74) but not in cheap regimes (f* = infinity). The honest architecture is re-derivation plus caching with a per-object persistence policy (persist only when the regime indicates f* is reachable), not unconditional persistence. C-PARAM-INHERIT is reinforced at EXPERIMENTAL: the committed kernel's distill_parameterized induces transferable mechanisms (collection + id slots) that reach EXECUTABLE and transfer at 100% success with a working safety gate.

## 9. Validity Threats

- Self-authored stdlib substrate, not the real Web. Ratios are relative economics.
- No LLM agent. The INHERITANCE arm is a deterministic executor. Model tokens, browser, latency, verification, and staleness costs are UNKNOWN.
- Bootstrap CIs on success rates are degenerate at [1.0, 1.0] (ceiling effect).
- The slot-value guard is syntactic, not semantic. It cannot distinguish a valid transfer from a well-formed out-of-support binding.
- F4 is mis-calibrated for the infinity case (see result.json validity_notes).

## 10. Artifacts

| Path | Role |
|------|------|
| `raw_evidence/observations.jsonl` | 150 training observations |
| `raw_evidence/task_results.jsonl` | 2250 per-task rows (15 arms × 150 tasks) |
| `raw_evidence/probe_results.jsonl` | 60 negative probes |
| `raw_evidence/mechanisms.json` | Induced mechanisms (inheritance + null) |
| `raw_evidence/substrate_probe.json` | Surface contract verification |
| `raw_evidence/derived.json` | All bootstrapped metrics, falsifier evaluation |
| `run_experiment.py` | Experiment runner |
| `build_result.py` | Derived metrics builder |
| `substrate.py` | Dual-regime substrate |
| `src/spider/kernel.py` | Committed kernel (sha256 57690132...) |
| `tests/test_kernel.py` | 9 tests reaching EXECUTABLE via distill_parameterized |
