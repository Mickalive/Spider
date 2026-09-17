# Preregistration: EXP-PRODUCT-35166508130

## Background

The parent experiment (EXP-PRODUCT-35154724610) was MEASUREMENT_INVALID due to a frozen test design flaw: unseen IDs 99, 100, 101 do not exist on jsonplaceholder.typicode.com (posts 1-100, users 1-10). URL binding accuracy was 1.0 (9/9) proving correct URL construction, but HTTP binding accuracy was 0.333 (3/9) because the API returned 404 for non-existent resources. The literal baseline showed identical 3/9 failure, confirming the issue was API data limits not parameterization.

This experiment fixes the test design flaw by using endpoint-appropriate unseen IDs that actually exist on jsonplaceholder.typicode.com.

## Research Question

Can parameterized mechanisms bind correctly over real HTTP when using endpoint-appropriate unseen IDs that exist on jsonplaceholder.typicode.com?

## Hypothesis

With valid unseen IDs (posts 96-98, users 8-10, comments postId 5-7), distill_parameterized with Fix1+Fix2+Fix3 will achieve 9/9 HTTP binding correctness. The literal baseline will also achieve 9/9, confirming both mechanisms execute correctly over real HTTP.

## Method

### Code Restoration

Restore `distill_parameterized()` and supporting functions (`_find_common_prefix_suffix`, `_validate_prefix_boundary`, `_is_protocol_only_prefix`, `_collect_leaf_paths`, `_get_value_at_path`, `_set_template_value`, `_field_path_to_slot_name`, `_is_metadata_path`, `_METADATA_PATHS`) from parent execute commit `a49d839e` into `src/spider/kernel.py`. Verify kernel regression tests pass (3/3) before HTTP testing.

### Training Data

Use same P1_API_ENDPOINTS training observations as parent:
- fetch_posts: 5 observations with GET+PUT shared (method excluded via `_METADATA_PATHS`)
- fetch_users: 3 observations
- fetch_comments: 3 observations

### Unseen IDs (Validated to Exist)

| Endpoint | Unseen IDs | Verification |
|----------|-----------|--------------|
| posts | 96, 97, 98 | jsonplaceholder has posts 1-100 |
| users | 8, 9, 10 | jsonplaceholder has users 1-10 |
| comments postId | 5, 6, 7 | jsonplaceholder returns data for postId 1-100 |

### Test Conditions

1. **P1_REAL_HTTP_BINDING** (positive control): Distill parameterized mechanisms from training data, resolve with unseen IDs, execute over HTTP, verify status=200 and valid JSON body.

2. **B_LITERAL_HTTP_EXECUTION** (baseline): Create literal mechanisms from same training data, execute with same unseen IDs over HTTP, verify status=200 and valid JSON body.

3. **N1_NONEXISTENT_ENDPOINT** (null control): Request resource ID 999999 on each endpoint. Expected: 404 or empty array without crashes.

4. **B_UNFIXED_PROTOCOL_ONLY** (baseline): Apply unfixed heuristic (without Fix3) to protocol-only URL `https://jsonplaceholder.typicode.com/`. Expected: unfixed produces slot_count > 0 while fixed produces 0. Uses URL pair where Fix2 passes but Fix3 should reject.

5. **Kernel regression**: Run existing kernel tests (3/3 expected pass).

6. **Token cost**: Measure token count for parameterized vs literal templates using tiktoken cl100k_base. Document model pricing.

### Comment Body Validation Fix

Fix V2_COMMENT_BODY_VALIDATION_BUG from parent audit: validation must accept list-of-dicts with keys `postId, id, name, email, body` for comments endpoint. Non-empty comment lists marked valid, empty lists marked valid.

## Decision Rule

All conditions C1-C6 must pass for SURVIVES_CURRENT_TEST:

- **C1**: URL binding accuracy >= 1.0 (9/9 correct URL construction)
- **C2**: HTTP binding accuracy >= 1.0 (9/9 correct HTTP executions)
- **C3**: B_LITERAL HTTP accuracy >= 1.0 (9/9 literal mechanisms execute correctly)
- **C4**: B_UNFIXED confirms Fix3 necessity (unfixed slot_count > 0, fixed slot_count = 0)
- **C5**: Kernel regression tests pass (3/3)
- **C6**: Token cost measured with actual tokenizer; parameterized <= literal

Any failure triggers FALSIFIED-IN-SETTING.

## Validity Conditions

1. distill_parameterized + Fix1+Fix2+Fix3 restored from parent execute commit
2. Unseen IDs verified to exist before HTTP testing
3. Comment body validation accepts list-of-dicts
4. Token cost measured with tiktoken, not chars/4 heuristic
5. HTTP execution uses urllib.request with 10s timeout
6. GET-only endpoints (PUT/POST not tested)
7. Network access to jsonplaceholder.typicode.com required

## Scope Limitations

- Single API (jsonplaceholder.typicode.com), not general Web
- GET-only endpoints (method conflation not tested)
- Single-slot parameterization only (G4 multi-char suffix architectural bound persists)
- Synthetic training data (no LLM distillation, no browser automation)
- No end-to-end amortized cost measurement (C-PRODUCT-ECON remains HYPOTHESIS)
- No real browser traffic prevalence measurement
- resolve() lacks parameter-slot-count tie-break (unsafe for mixed literal+parameterized registries at equal confidence)

## Do Not Assume

- C-PARAM-INHERIT is VALIDATED or PRODUCT_CORE: it remains EXPERIMENTAL regardless of outcome
- HTTP 9/9 success proves general parameterized binding: limited to jsonplaceholder GET endpoints
- Token cost savings reflect real economics: tiktoken measurement is one data point, not amortized cost
- Fix3 necessity is fully quantified: B_UNFIXED tests one protocol-only URL pair
- Method fidelity is established: only GET tested, PUT/POST untested
- End-to-end product viability is demonstrated: zero model/browser calls in this experiment
