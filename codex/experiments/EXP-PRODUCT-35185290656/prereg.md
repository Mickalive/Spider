# EXP-PRODUCT-35185290656 preregistration

## Status

DESIGN ONLY — not yet frozen.

## Experiment Identity

- **experiment_id**: EXP-PRODUCT-35185290656
- **lane**: product
- **claim_ids**: C-PARAM-INHERIT
- **parent**: EXP-PRODUCT-35166508130 (FALSIFIED-IN-SETTING)

## Question

Can Fix3 (_is_protocol_only_prefix) be redesigned to reject only truly protocol-only prefixes (bare scheme+authority with no path, query, or fragment) without blocking valid host?query parameterization, and does a discriminating test corpus demonstrate its independent necessity over Fix2?

## Background

The parent experiment (EXP-PRODUCT-35166508130) established:
- Real HTTP binding correctness 9/9 for parameterized mechanisms on jsonplaceholder GET endpoints
- C4 (B_UNFIXED_PROTOCOL_ONLY) failed because Fix3 is redundant with Fix2 for the tested URL pair
- Fix3 is overbroad: it blocks valid host?query parameterization (audit V2)

The parent audit (V2_FIX3_OVERBROAD_BLOCKS_VALID_QUERY_PARAM) identified:
- Current Fix3 logic: `if '/' not in rest: return True`
- This incorrectly rejects `https://api.example.com?key=abc` because rest `api.example.com?key=abc` has no `/`
- Fix3 should only reject bare authority prefixes with NO path, query, or fragment

## Hypothesis

A redesigned Fix3 that checks for `?` or `/` or `#` in the rest after `://` will:
1. Correctly reject bare authority prefixes (protocol-only)
2. Correctly accept query-parameterized prefixes (valid parameterization)
3. Not break existing kernel tests or HTTP binding
4. Be independently necessary for patterns where Fix2 passes but Fix3 should reject

## Redesigned Fix3 Specification

```python
def _is_protocol_only_prefix(prefix: str) -> bool:
    """Reject common prefixes that are only scheme+authority without meaningful path/query content.
    
    A prefix is 'protocol-only' if it contains only the scheme and authority
    (e.g., 'https://', 'http://', 'https://a.com') with no path segment,
    query string, or fragment after the host.
    Prefixes containing '?', '/', or '#' after the authority are NOT protocol-only.
    """
    if not prefix:
        return False
    parts = prefix.split("://", 1)
    if len(parts) != 2:
        return False
    scheme, rest = parts
    if not rest:
        return True
    # Protocol-only: only authority, no path/query/fragment
    if '?' not in rest and '/' not in rest and '#' not in rest:
        return True
    return False
```

Key change: old logic was `if '/' not in rest: return True` (rejects everything without `/`).
New logic: `if '?' not in rest and '/' not in rest and '#' not in rest: return True` (only rejects bare authority).

## URL Test Corpus

### Category 1: Protocol-only (Fix3 should REJECT)

| # | Prefix | Expected Fix3 | Expected Fix2 | Notes |
|---|--------|---------------|---------------|-------|
| 1 | `https://api.example.com` | True | varies | Bare authority, no path/query |
| 2 | `http://localhost:8080` | True | varies | Localhost bare authority |
| 3 | `https://a.com` | True | varies | Minimal bare authority |

### Category 2: Query-parameterized (Fix3 should ACCEPT)

| # | Prefix | Expected Fix3 | Expected Fix2 | Notes |
|---|--------|---------------|---------------|-------|
| 4 | `https://api.example.com?key=` | False | True | Query param prefix |
| 5 | `https://example.com?x=` | False | True | Different host |
| 6 | `https://api.example.com?foo=bar&baz=` | False | True | Multi-query prefix |

### Category 3: Path-slash (Fix3 should ACCEPT, same as current)

| # | Prefix | Expected Fix3 | Expected Fix2 | Notes |
|---|--------|---------------|---------------|-------|
| 7 | `https://jsonplaceholder.typicode.com/` | False | True | Parent test pattern |
| 8 | `https://jsonplaceholder.typicode.com/posts/` | False | True | Deeper path |
| 9 | `https://api.example.com/v1/` | False | True | Versioned path |

### Category 4: Mixed/Edge (Fix3 should ACCEPT)

| # | Prefix | Expected Fix3 | Expected Fix2 | Notes |
|---|--------|---------------|---------------|-------|
| 10 | `https://api.example.com/path?query=` | False | True | Path + query |
| 11 | `https://example.com#frag` | False | True | Fragment (unusual) |
| 12 | `https://api.example.com:8080/` | False | True | Port + path |

## Baselines

### B_OLD_FIX3_OVERBROAD

Test current (pre-redesign) Fix3 against query-parameterized prefix `https://api.example.com?key=`:
- Expected: old Fix3 returns True (blocks valid parameterization)
- Purpose: demonstrates the bug being fixed

### B_LITERAL_HTTP_REGRESSION

Literal mechanisms with same training data and valid IDs:
- Expected: 9/9 HTTP execution success
- Purpose: regression baseline confirming Fix3 redesign doesn't break existing capability

## Controls

### P1_QUERY_PARAM_ACCEPTED (Positive Control)

Redesigned Fix3 applied to query-parameterized prefix `https://api.example.com?key=`:
- Expected: returns False (does NOT reject)
- This is the primary fix validation

### N1_PROTOCOL_ONLY_REJECTED (Null Control)

Redesigned Fix3 applied to bare authority prefix `https://api.example.com`:
- Expected: returns True (rejects)
- Confirms Fix3 still catches truly protocol-only patterns

## Measurement Validity

1. Fix3 redesign is a single function body change to `_is_protocol_only_prefix` in `src/spider/kernel.py`
2. No other function signatures changed
3. Existing kernel regression tests run before and after change
4. HTTP binding test re-run with query-parameterized endpoint
5. All measurements use committed code
6. GET-only endpoints tested
7. Network access to jsonplaceholder.typicode.com required

## Decision Rule

- **C1**: Fix3 redesigned rejects bare authority prefix `https://api.example.com` (returns True)
- **C2**: Fix3 redesigned accepts query-parameterized prefix `https://api.example.com?key=` (returns False)
- **C3**: Fix3 redesigned accepts path-slash prefix `https://jsonplaceholder.typicode.com/` (returns False)
- **C4**: Old Fix3 incorrectly rejects query-parameterized prefix `https://api.example.com?key=` (returns True)
- **C5**: Kernel regression tests pass (3/3) after Fix3 redesign
- **C6**: HTTP binding accuracy >= 1.0 on query-parameterized endpoint (comments?postId=${url} with valid unseen IDs postId 5-7)
- **C7**: distill_parameterized with Fix3 redesign produces correct Mechanism for query-parameterized observations (slot ['url'], template 'comments?postId=${url}')

**ALL conditions C1-C7 must pass for SURVIVES_CURRENT_TEST; any failure triggers FALSIFIED-IN-SETTING.**

## Product Consequence

### If SURVIVES_CURRENT_TEST

- C-PARAM-INHERIT expands to include host?query parameterization patterns
- Fix3 demonstrated as non-redundant defense-in-depth for bare authority patterns
- Claim ceiling: 'path-slash and query-parameterized GET' (previously 'path-slash GET only')
- No product promotion yet (still EXPERIMENTAL, not VALIDATED/PRODUCT_CORE)

### If FALSIFIED-IN-SETTING

- C-PARAM-INHERIT remains limited to path-slash URL patterns
- Fix3 either overbroad (blocks valid queries) or redundant (Fix2 handles all cases)
- Consider removing Fix3 entirely if redundancy confirmed
- No product promotion

## Scope Limitations

- GET-only endpoints (PUT/POST not tested)
- Single-slot parameterization only
- Synthetic training data from jsonplaceholder.typicode.com
- Fix3 redesign is a minimal code change; broader parameterization quality not tested
- Token economics not re-measured (carried from parent: 68 vs 96 tokens, 29.17% structural savings)
- No browser automation, no model calls
- No LLM distillation tested
- No multi-slot, noisy browser, cross-site generalization

## Inherited State from Parent

### Established
- Real HTTP binding correctness 9/9 for parameterized mechanisms on jsonplaceholder GET endpoints
- Token cost measurement: parameterized 68 tokens, literal 96 tokens (29.17% savings)
- Kernel regression tests pass (3/3)
- N1 null control passes
- distill_parameterized with Fix1+Fix2+Fix3 induces 3 GET-only mechanisms

### Rejected
- C4 B_UNFIXED_PROTOCOL_ONLY test design is non-discriminating for the frozen URL pair
- Fix3 necessity not demonstrated by the frozen test

### Unknown
- Fix3 independent necessity on discriminating data where Fix2 passes but Fix3 should reject
- PUT/POST method fidelity over real HTTP
- End-to-end amortized cost per successful real-browser task

### Do Not Assume
- C-PARAM-INHERIT is VALIDATED or PRODUCT_CORE (remains EXPERIMENTAL)
- Fix3 is necessary for all URL patterns
- Token cost savings reflect real economics
- HTTP binding generalizes beyond jsonplaceholder GET
