# EXP-PRODUCT-33528829801 — Preregistration

## Status

DESIGN ONLY. Not yet frozen.

## Experiment Identity

- **Experiment ID:** EXP-PRODUCT-33528829801
- **Lane:** Product
- **Claim:** C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers"
- **Request trigger:** pulse (first Product lane experiment)

## Scientific Question

Does parameterized mechanism inheritance reduce later-agent cost for unseen resource identifiers compared to literal mechanism replay and cold exploration?

## Hypothesis

A mechanism distilled with parameter induction from successful observations on resources A, B, C will resolve correctly for unseen resource D, with bound action correctly substituting the new identifier. The cost of parameterized resolution is O(k) where k is the number of parameters, compared to O(n) for full task replay where n is the task length.

## Background and Motivation

The SpiderKernel currently has a gap between what `resolve()` can handle (parameterized mechanisms with `${param}` slots) and what `distill()` produces (literal mechanisms with no parameter induction). This gap means the product's core value proposition — that knowledge learned on one resource can be reused on unseen resources — is untested.

C-PARAM-INHERIT is the foundational product claim. If parameterized inheritance fails, the product architecture needs revision before further investment.

## Experimental Design

### What we test

1. **Parameter induction during distillation:** Add a simple heuristic to `distill()` that identifies varying parts across multiple observations of the same intent and marks them as parameter slots.

2. **Parameterized resolution on unseen identifiers:** Test whether a mechanism distilled from observations on resources A, B, C resolves correctly for unseen resource D.

3. **Cost comparison:** Compare the number of operations required for:
   - Cold exploration (no memory)
   - Literal mechanism replay
   - Parameterized mechanism resolution

### Materials

- Synthetic observations with structured state, action, and next_state
- Varying resource identifiers (e.g., `/api/items/1`, `/api/items/2`, `/api/items/3`)
- Same intent, preconditions, and applicability guards across all observations

### Procedure

1. Create 3 synthetic observations of successful "delete-item" actions on resources A, B, C
2. Distill each into a literal mechanism (current behavior)
3. Apply parameter induction: compare action templates across mechanisms, identify the varying substring as a parameter
4. Create a unified parameterized mechanism with `${resource_id}` slot
5. Test resolution on unseen resource D (resource_id=99)
6. Record: resolution status, bound_action, number of operations
7. Repeat for 10 different unseen identifiers

### Baselines

- **B1 (Cold):** No memory. Simulate full task cost = number of steps in original observation.
- **B2 (Literal):** Use literal mechanism from distill. Test resolution on unseen identifier.
- **B3 (Retrieval):** Find nearest observation by state similarity (simple feature matching), attempt replay.

### Controls

- **Positive control:** Resolve parameterized mechanism with a seen identifier (A, B, or C). Should succeed.
- **Null control:** Resolve parameterized mechanism with mismatched preconditions. Should return UNKNOWN.

## Falsification Criteria

C-PARAM-INHERIT is **falsified** at this level if ANY of:

1. Parameterized mechanism fails to resolve for >= 2 of 10 unseen identifiers despite matching preconditions
2. Bound action contains the old identifier (e.g., still shows `/api/items/A` instead of `/api/items/99`)
3. Parameter induction false negative rate > 0.2 (misses > 20% of true parameter slots)

C-PARAM-INHERIT **survives** this test if ALL of:

1. Parameterized mechanisms resolve correctly for >= 90% of unseen identifiers
2. Bound actions correctly substitute the new identifier in all successful resolutions
3. Literal mechanisms resolve for 0% of unseen identifiers (confirming they can't handle novelty)
4. Parameter induction false negative rate <= 0.2

## Decision Rule

- **Survives:** Proceed to end-to-end agent evaluation with real LLM. Increase confidence in parameterized inheritance.
- **Falsified:** Re-evaluate product architecture. Consider: (a) different parameter induction approach, (b) LLM-based parameterization, (c) alternative mechanism abstraction.
- **Inconclusive:** If measurement infrastructure fails (not the same as negative result), write exact failure and smallest next action.

## Product Consequences

- **Positive outcome:** Parameterized inheritance is viable. Invest in richer parameter induction, cross-intent parameterization, and end-to-end agent evaluation. Promotion readiness increases.
- **Negative outcome:** Parameterized inheritance fails at the simplest synthetic level. Do not promote to Product Core. Redirect resources to alternative mechanisms (semantic resolution, LLM-based inheritance, or revised mechanism abstraction).

## Validity Threats

1. **Parameter induction simplicity:** The heuristic may be too simple to generalize. This is acceptable for a POC; a negative result means even simple cases fail, which is informative.
2. **Synthetic data:** Real web observations have more noise. A positive result on synthetic data is necessary but not sufficient for real-world viability.
3. **Small sample:** 10 unseen identifiers is small. A clear positive or negative result is still informative; ambiguous results (e.g., 7/10) require replication.

## What This Experiment Does NOT Test

- Real browser observation and distillation
- LLM-based parameter induction
- Cross-intent mechanism transfer
- End-to-end agent cost with real model calls
- Freshness, staleness, or drift detection
- Delta repair mechanisms

These are deferred to subsequent experiments based on the outcome of this foundational test.

## Raw Observations to Preserve

- All mechanism contents (JSON) before and after parameter induction
- Resolution results for each unseen identifier (status, bound_action, operations count)
- Parameter induction decisions (which parts were identified as parameters)
- Baseline cost measurements (operations count for each baseline)

## Timeline

- DESIGN: complete (this document)
- FREEZE: pending (deterministic hash of spec + prereg)
- EXECUTE: pending (code changes in src/spider/, tests in tests/)
- AUDIT: pending
- VERDICT: pending
