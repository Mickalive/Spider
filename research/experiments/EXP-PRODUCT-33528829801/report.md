# EXP-PRODUCT-33528829801 — Execution Report

## Claim Under Test

**C-PARAM-INHERIT:** "Mechanisms parameterize to unseen identifiers"

## Outcome: SUPPORTS

The claim **survives** all four falsification criteria defined in the frozen preregistration. Parameterized mechanism inheritance works correctly at the synthetic unit-test level.

---

## Summary of Results

| Criterion | Threshold | Observed | Pass? |
|---|---|---|---|
| Unseen resolution rate | >= 90% | 100% (10/10) | Yes |
| Binding accuracy | 100% | 100% (10/10) | Yes |
| Literal mechanism failure rate | 100% fail | 100% (10/10) | Yes |
| Parameter induction FN rate | <= 0.2 | 0.0 (1/1 detected) | Yes |

Both controls passed:
- **Positive control:** Parameterized mechanism resolves for seen identifier A with correct bound_action
- **Null control:** Parameterized mechanism abstains (UNKNOWN) when preconditions mismatch

---

## What Happened

### 1. Parameter Induction

Three synthetic "delete-item" observations were created for resources A, B, C. Each had identical preconditions (`authenticated: true, role: owner`), identical postconditions (`exists: false`), and actions differing only in the resource identifier:

```
A: {"method": "DELETE", "path": "/api/items/A"}
B: {"method": "DELETE", "path": "/api/items/B"}
C: {"method": "DELETE", "path": "/api/items/C"}
```

`distill_parameterized()` compared the action templates across all three observations, identified the path field as varying, extracted the common prefix (`/api/items/`) and suffix (empty), and produced:

```json
{
  "method": "DELETE",
  "path": "/api/items/${id}"
}
```

The parameter slot `["id"]` was correctly identified. False negative rate: 0.0.

### 2. Resolution on Unseen Identifiers

The parameterized mechanism was registered and tested against 10 unseen resource identifiers (D through M). For each, `resolve()` was called with `params={"id": <resource>}`. All 10 resolved with:

- Status: `EXECUTABLE`
- Bound action: `{"method": "DELETE", "path": "/api/items/<resource>"}`
- Confidence: 0.9 (above the 0.8 execution threshold)

Resolution cost: ~76 microseconds per call (amortized), compared to 4 simulated operations for cold exploration.

### 3. Baselines

| Baseline | Behavior | Failure Mode |
|---|---|---|
| B1 (Cold) | 4 operations per resource, always succeeds | No memory reuse |
| B2 (Literal) | Returns EXPLORE (confidence 0.5 < 0.8) for all 10 unseen | Cannot bind new identifiers; literal path is fixed |
| B3 (Retrieval) | Matches training resource A, replays literal content | Same failure as B2 |

All three baselines confirm that without parameterized inheritance, unseen resources require full re-exploration.

### 4. Cost Economics

| Approach | Operations per unseen resource | Success |
|---|---|---|
| Cold (B1) | 4 | Yes (eventually) |
| Literal (B2) | 1 (but fails) | No |
| Retrieval (B3) | 2 (but fails) | No |
| **Parameterized** | **1** | **Yes** |

Parameterized resolution achieves a 4x cost reduction vs. cold exploration while maintaining correctness.

---

## What This Experiment Does NOT Test

Per the frozen preregistration, the following are explicitly out of scope:

- Real browser observation and distillation
- LLM-based parameter induction
- Cross-intent mechanism transfer
- End-to-end agent cost with real model calls
- Freshness, staleness, or drift detection
- Delta repair mechanisms
- Multi-parameter mechanisms
- Non-identifier parameter values

A positive result on synthetic data is necessary but not sufficient for real-world viability.

---

## Validity Threats

1. **Synthetic data:** All observations are deterministic and perfectly structured. Real web observations have noise, varying schemas, and multi-step actions. The parameter induction heuristic may fail on noisier inputs.

2. **Simple parameter pattern:** The only varying field is a single resource identifier in a URL path. Multi-parameter mechanisms (e.g., `{resource}/${id}` or `{name: ${title}}`) are untested.

3. **Small sample:** 10 unseen identifiers is sufficient for a clear binary result but not for estimating confidence intervals on the resolution rate.

4. **No adversarial cases:** The experiment does not test edge cases like empty identifiers, special characters, very long identifiers, or identifiers that partially match the prefix/suffix pattern.

---

## Product Consequence

Per the frozen spec:

> **Positive outcome:** Parameterized inheritance is viable at the kernel level. Invest in richer parameter induction, parameterized distillation research, and end-to-end agent evaluation. Promotion readiness increases.

**Recommendation:** C-PARAM-INHERIT survives this gate. Proceed to:
1. End-to-end agent evaluation with real LLM (test cross-resource reuse in a realistic agent loop)
2. Multi-parameter induction testing
3. Real-browser observation distillation
4. Stress testing with noisy/adversarial observation patterns
