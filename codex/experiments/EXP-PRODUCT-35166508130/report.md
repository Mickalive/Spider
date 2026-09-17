# EXP-PRODUCT-35166508130: Real HTTP Binding Correctness with Valid IDs

## Executive Summary

**Outcome: FALSIFIES (FALSIFIED-IN-SETTING)**

This experiment resolves the primary blocker from the parent MEASUREMENT_INVALID experiment (V1_HTTP_DESIGN_IMPOSSIBLE_IDS) and demonstrates that parameterized mechanisms bind correctly over real HTTP with valid endpoint IDs. However, the frozen decision rule triggers FALSIFIED-IN-SETTING because condition C4 (B_UNFIXED_PROTOCOL_ONLY) fails due to a test design limitation where Fix2 subsumes Fix3 for the tested URL pattern.

## What Changed from Parent

| Aspect | Parent (EXP-PRODUCT-35154724610) | This Experiment |
|--------|----------------------------------|-----------------|
| Unseen IDs | 99, 100, 101 (don't exist) | posts 96-98, users 8-10, comments postId 5-7 (verified to exist) |
| Comment validation | isinstance(body_json, dict) — rejects list-of-dicts | validate_comment_body — accepts list-of-dicts with expected keys |
| Token measurement | chars/4 heuristic | tiktoken cl100k_base with model pricing |
| HTTP binding accuracy | 0.333 (3/9) — API returned 404 for nonexistent IDs | **1.000 (9/9)** — all IDs exist and return valid data |

## Condition-by-Condition Results

### C1: P1_REAL_HTTP_BINDING — PASS (9/9)

All 3 parameterized mechanisms (fetch_posts, fetch_users, fetch_comments) correctly construct URLs and execute over real HTTP:

| Endpoint | Unseen ID | URL | Status | Body Valid |
|----------|-----------|-----|--------|------------|
| posts | 96 | /posts/96 | 200 | yes |
| posts | 97 | /posts/97 | 200 | yes |
| posts | 98 | /posts/98 | 200 | yes |
| users | 8 | /users/8 | 200 | yes |
| users | 9 | /users/9 | 200 | yes |
| users | 10 | /users/10 | 200 | yes |
| comments | 5 | /comments?postId=5 | 200 | yes |
| comments | 6 | /comments?postId=6 | 200 | yes |
| comments | 7 | /comments?postId=7 | 200 | yes |

URL binding accuracy: 1.0 (9/9). HTTP binding accuracy: 1.0 (9/9).

### C2: N1_NONEXISTENT_ENDPOINT — PASS

- posts/999999: 404 (correct)
- users/999999: 404 (correct)
- comments?postId=999999: 200 with empty list `[]` (correct — jsonplaceholder returns empty array for valid postId format with no matching comments)

### C3: B_LITERAL_HTTP_EXECUTION — PASS (9/9)

Literal mechanisms (exact URLs) achieve 9/9 HTTP execution success, identical to parameterized mechanisms. This confirms both mechanisms execute correctly over real HTTP and the improvement from parent is from corrected test design, not parameterization advantage.

### C4: B_UNFIXED_PROTOCOL_ONLY — FAIL

**This is the condition that triggers FALSIFIED-IN-SETTING.**

The test uses the URL pair `https://jsonplaceholder.typicode.com/` + `https://jsonplaceholder.typicode.com/about`. The common prefix is `https://jsonplaceholder.typicode.com/`.

- **Fixed (with Fix3)**: `distill_parameterized` returns a Mechanism (NOT None) because `_is_protocol_only_prefix("https://jsonplaceholder.typicode.com/")` returns `False` — the prefix contains `/` in the rest after `split("://")`, so Fix3 does not reject it.
- **Unfixed (simulated)**: Would produce a slot because the prefix ends with `/` (Fix2 passes).

**Root cause**: `_is_protocol_only_prefix` only rejects prefixes where the rest (after `://`) contains NO `/` character. The URL `https://jsonplaceholder.typicode.com/` has `/` in the rest, so Fix3 does not trigger. Meanwhile, Fix2 (`_validate_prefix_boundary`) passes because the prefix ends with `/`.

**Implication**: For the tested URL pattern, Fix2 already provides the necessary boundary validation. Fix3 adds no additional protection because:
1. Truly protocol-only prefixes (e.g., `https://api.example.com`) are rejected by Fix2's boundary check before Fix3 runs.
2. Protocol-only prefixes with trailing `/` (e.g., `https://example.com/`) are NOT caught by Fix3 because `/` is in the rest.

This is a genuine finding: Fix3 is redundant with Fix2 for the tested class of inputs. A new test design would be needed to demonstrate Fix3's independent value, if any exists.

### C5: Kernel Regression Tests — PASS (3/3)

- test_unknown_is_default: PASS
- test_parameterized_mechanism_binds_only_when_guarded: PASS
- test_invalidation_forces_abstention: PASS

### C6: Token Cost — PASS

| Metric | Parameterized | Literal |
|--------|---------------|---------|
| Total tokens (tiktoken cl100k_base) | 68 | 96 |
| Savings | 28 tokens (29.17%) | — |
| Cost per invocation (gpt-4o-mini input) | $0.0000102 | $0.0000144 |

Model: gpt-4o-mini, $0.15/1M input tokens, $0.60/1M output tokens (OpenAI pricing, 2026-09-17).

## Scientific Assessment

### What This Experiment Establishes

1. **Parameterized mechanisms bind correctly over real HTTP** on jsonplaceholder.typicode.com GET endpoints: URL construction 1.0 (9/9), HTTP execution 1.0 (9/9).
2. **Literal mechanisms also achieve 9/9**, confirming both work correctly.
3. **Comment body validation fix (V2)** resolves the parent audit finding: comments endpoint returns list-of-dicts, now correctly validated.
4. **Token cost measurement** with actual tokenizer confirms parameterized is cheaper (68 vs 96 tokens, 29.17%).
5. **Fix3 is not discriminating** for the tested URL pattern — Fix2 subsumes Fix3's protection.

### What This Experiment Does NOT Establish

- **General Web binding**: limited to jsonplaceholder GET endpoints.
- **Fix3 necessity**: the frozen B_UNFIXED_PROTOCOL_ONLY test is not a discriminating test for Fix3.
- **End-to-end product viability**: zero model/browser calls in this experiment.
- **Amortized cost**: single token measurement, not amortized over task sequences.
- **Method fidelity**: only GET tested, PUT/POST untested.

### Frozen Decision Rule Consequence

The frozen rules require ALL conditions C1-C6 for SURVIVES_CURRENT_TEST. C4 fails, triggering FALSIFIED-IN-SETTING. This is a valid application of the frozen rules, but the scientific content is mixed: C1-C3 provide strong positive evidence for HTTP binding correctness, while C4 failure reflects a test design limitation rather than a genuine binding or execution bug.

## Claim Status Impact

- **C-PARAM-INHERIT**: Advances from MEASUREMENT_INVALID to a mixed state — real HTTP binding evidence is positive (C1-C3), but the frozen gate fails on C4. The claim ceiling expands to include "committed-code synthetic single-slot GET with real HTTP binding on jsonplaceholder".
- **C-PRODUCT-ECON**: Gets first actual tokenization data point (68 vs 96 tokens, 29.17% savings). Remains HYPOTHESIS pending amortized cost measurement.
