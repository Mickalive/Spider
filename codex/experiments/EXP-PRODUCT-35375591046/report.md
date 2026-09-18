# EXP-PRODUCT-35375591046 — Report

## Experiment Identity

- **Experiment ID:** EXP-PRODUCT-35375591046
- **Lane:** product
- **Claim IDs:** C-PRODUCT-ECON
- **Parent:** EXP-PRODUCT-35353007958 (handoff sha256: 0fb45f53ab9fe04b8c3bdfb5e89d5e95e0cf7dc3ad67ac073f159e8c0258a9a0)
- **Frozen at:** 2026-09-18T17:41:20.803580+00:00
- **GitHub Run ID:** 35375591046

## Status

**MEASUREMENT_INVALID — Infrastructure failure: no LLM API keys available.** 0/32 tasks executed. No scientific evidence was produced or falsified.

## Summary

This experiment was designed to measure the COLD baseline (no registry) success rate and token cost on the synthetic 32-task corpus using real LLM API calls, to determine whether token-based parameterized inheritance economics are closed. The frozen design required 32 independent LLM API calls (one per task). However, **no LLM API keys are available in the execution environment** — this is the same infrastructure failure that invalidated the parent experiment (EXP-PRODUCT-35353007958).

Per the packet contract (research/EXPERIMENT_PACKET.md section 9), infrastructure failure is not a scientific negative. No evidence was produced or falsified. The parent's analytical ceiling remains the most recent valid measurement.

## What Was Measured

Nothing. Zero LLM API calls were made. The frozen decision_rule C1-C4 could not be evaluated because the prerequisite substrate (LLM API access) was unavailable.

## Parent Analytical Ceiling (Carried Forward)

The parent experiment EXP-PRODUCT-35330741529 established the following analytical measurements (via tiktoken counting, NOT real LLM execution):

| Metric | Value |
|--------|-------|
| COLD total model cost | 2,475 tokens |
| COLD per-task avg cost | 77.34 tokens/task |
| Literal per-task avg cost | 615.34 tokens/task |
| Parameterized per-task avg cost | 582.0 tokens/task |
| Workflow savings (param vs literal) | 1,067 tokens (5.42%) |
| COLD vs literal cost ratio | ~8x cheaper |
| COLD success rate | **Assumed 100% (not measured)** |
| COLD completion tokens | **Estimated 20/task (not measured)** |

## Key Gaps

1. **COLD success rate is entirely unmeasured.** The parent assumed 100% success, but this was never tested with a real LLM. The COLD baseline requires the model to generate correct URLs from scratch — this could fail at any rate.

2. **Completion tokens are estimated, not measured.** The parent used 20 tokens/task estimate for COLD URL generation. Real LLM outputs may differ significantly.

3. **Browser/verification costs omitted.** All conditions execute identical actions, so these costs are assumed to cancel, but this assumption was never validated.

4. **The 5.42% margin is thin.** If real LLM completion tokens exceed estimates, the margin could reverse, making parameterized deduplication less attractive than COLD.

## Validity Assessment

- **Status:** MEASUREMENT_INVALID (infrastructure failure)
- **Outcome:** NOT_APPLICABLE (no measurement possible)
- **Scientific impact:** None — no evidence was produced or falsified
- **Parent carry-forward:** Unchanged — the three-way decision (A/B/C) remains unresolved

## Validity Notes

- This is the second consecutive PRODUCT lane experiment to fail with the same infrastructure cause (missing LLM API keys).
- The frozen decision_rule states: "MEASUREMENT_INVALID if API failures prevent completion of >=5 tasks." Zero tasks were executed.
- The analytical tiktoken measurement (EXP-PRODUCT-35330741529) is preserved as the most recent valid measurement, but it has known validity gaps (C1 assumed, completion estimated, browser omitted).
- No code modifications were made to any registry-authorized code root (src, tests, sdk, pyproject.toml).

## Unresolved Questions

1. Can COLD achieve >= 90% success rate with real LLM calls?
2. What is the actual COLD token cost from real model output?
3. Does the 5.42% savings survive real LLM execution?
4. Should the product lane retry with API keys (option A), test with real corpus (option B), or close token-based economics (option C)?

## Evidence References

- request.json: explicit statement of infrastructure failure
- spec.json: frozen design requiring real LLM API calls
- prereg.md: measurement protocol and decision rule
- parent handoff (EXP-PRODUCT-35353007958/handoff.json): three-way decision and carry_forward
- parent result (EXP-PRODUCT-35330741529/result.json): analytical ceiling with 77 tokens/task COLD
- codex/claim_state.json: C-PRODUCT-ECON remains HYPOTHESIS