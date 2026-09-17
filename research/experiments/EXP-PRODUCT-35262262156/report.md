# EXP-PRODUCT-35262262156 Report

## Experiment Summary

**Question:** Does parameterized mechanism representation reduce token cost when concrete values are long strings (UUIDs, slugs, full API paths, bearer tokens) rather than short numeric IDs?

**Outcome:** FALSIFIED. The hypothesis that parameterized mechanisms save tokens for long-value patterns is not supported as a general claim. Only 2/5 long-value patterns show positive savings; 2/5 show negative savings and 1/5 is neutral. The frozen decision rule requires ALL conditions C1-C8; conditions C4 (>=3/5 patterns with positive savings) and C6 (savings correlate with value length, r>=0.7) fail.

## Decision Rule Results

| Condition | Description | Result | Detail |
|-----------|-------------|--------|--------|
| C1 | resolve() EXECUTABLE for all 5 long-value | PASS | 5/5 |
| C2 | resolve() UNKNOWN for all 5 missing params | PASS | 5/5 |
| C3 | _bind() correct for all 5 | PASS | 5/5 |
| C4 | Parameterized fewer tokens >= 3/5 | **FAIL** | 2/5 |
| C5 | Mean savings >= 10% | PASS | 15.99% |
| C6 | Savings correlate with value length (r>=0.7) | **FAIL** | r=0.3909 |
| C7 | Kernel regression 3/3 | PASS | 3/3 |
| C8 | Positive control: short-value penalty | PASS | -5.26% |

## Token Cost Results

### Long-value patterns

| Pattern | Value | Value Length | Literal Tokens | Param Tokens | Savings |
|---------|-------|-------------|----------------|--------------|---------|
| P1_UUID | `550e8400-e29b-41d4-a716-446655440000` | 36 | 36 | 20 | **+44.44%** |
| P2_SLUG | `user-profile-settings-page` | 28 | 21 | 21 | 0.0% |
| P3_DEEPPATH | `v2/api/organizations/12345/projects/67890` | 42 | 26 | 29 | **-11.54%** |
| P4_BEARER | `eyJhbG...` (JWT) | 64 | 67 | 29 | **+56.72%** |
| P5_MULTIPARAM | `category=electronics&minPrice=100&maxPrice=500` | 46 | 31 | 34 | **-9.68%** |

### Controls

| Pattern | Value | Value Length | Literal Tokens | Param Tokens | Savings |
|---------|-------|-------------|----------------|--------------|---------|
| PC_SHORT | `42` | 2 | 19 | 20 | -5.26% (replicates parent) |
| NC_MID | `abc123` | 6 | 21 | 21 | 0.0% (breakeven) |

## Analysis

### Why C4 fails (2/5 < 3/5 threshold)

The two patterns showing **positive** savings share a key property: they use a **single parameter slot** replacing a **very long concrete value** (UUID 36 chars, bearer 64 chars). The template syntax `${userId}` or `${token}` is substantially shorter than the inlined value.

The two patterns showing **negative** savings have a different structure: they use **multiple parameter slots** where the template overhead per slot is not offset by the value removal. P3_DEEPPATH has 2 slots (`${orgId}`, `${projectId}`) where the concrete values being replaced are only 3-5 digit numbers. P5_MULTIPARAM has 3 slots (`${category}`, `${minPrice}`, `${maxPrice}`) with mixed short/medium values.

P2_SLUG sits at the breakeven: the slug value (28 chars) and template `${pageSlug}` (12 chars) are close enough that tiktoken tokenization yields equal token counts.

### Why C6 fails (r=0.3909)

Savings do not increase monotonically with value length. The ordering by value length is:

P1_UUID (36) > P2_SLUG (28) > P4_BEARER (64) > P3_DEEPPATH (42) > P5_MULTIPARAM (46)

But savings ordering is:

P4_BEARER (56.72%) > P1_UUID (44.44%) > P2_SLUG (0%) > P5_MULTIPARAM (-9.68%) > P3_DEEPPATH (-11.54%)

P5_MULTIPARAM has the second-longest value (46 chars) but negative savings because it has 3 parameter slots. P4_BEARER has the longest value (64 chars) and highest savings because it has 1 slot. The correlation is weak because **slot count** confounds the value-length relationship.

### Structural insight

The breakeven is not a simple value-length threshold. It depends on:

1. **Number of parameter slots**: More slots = more template overhead per slot
2. **Slot name length**: `${category}` (12 chars) vs `${id}` (5 chars) 
3. **Value length per slot**: Each slot's concrete value must be long enough to offset its template overhead
4. **URL structure**: Fixed characters (URL path, query separators) are present in both representations

For a single-slot pattern, the breakeven occurs when the concrete value length exceeds the template overhead by enough to overcome the fixed URL structure. For multi-slot patterns, the per-slot overhead accumulates and can dominate even with long total value strings.

## Scope Limitations

- tiktoken cl100k_base only; different LLM tokenizers may differ
- action_template JSON serialization (method + url fields), not full Mechanism object
- Synthetic training data, not real browser sessions
- No network access, no browser, no model calls
- GET-only patterns (no PUT/POST/DELETE)
- All patterns use confidence=0.9, above min_confidence=0.8
- Single test environment (Python 3.12, tiktoken 0.14.0)
- Bearer token is a real JWT-format string
- Deep API path uses numeric IDs that could themselves be parameterized
