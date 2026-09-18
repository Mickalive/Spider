# EXP-PRODUCT-35262262156 preregistration

## Experiment identity

- **experiment_id**: EXP-PRODUCT-35262262156
- **lane**: product
- **claim_ids**: C-PARAM-INHERIT, C-PRODUCT-ECON
- **parent**: EXP-PRODUCT-35209109455 (handoff sha256: 97a75186e42637b17f90dd00d76125f3f1ef0f2852c68b9861e99298be69d1b0)

## Question

Does parameterized mechanism representation reduce token cost when concrete values are long strings (UUIDs, slugs, full API paths, bearer tokens) rather than short numeric IDs?

## Hypothesis

Parameterized mechanisms with ${var} template slots use fewer tiktoken tokens than literal mechanisms when concrete values exceed ~8 characters. The structural property is: template overhead per slot (varname.length + 3 chars) is fixed, so when the concrete value is long, the total parameterized URL is shorter than the literal URL with the full value inlined.

## Falsifier

Parameterized uses more or equal tokens for the majority of long-value patterns, OR mean savings are negative, OR savings do not increase with value length.

## Test patterns

### Target long-value patterns (5 patterns)

| Pattern | Value type | Concrete value | Value length | Template slot |
|---------|-----------|----------------|-------------|---------------|
| P1_UUID | UUID | `550e8400-e29b-41d4-a716-446655440000` | 36 chars | `${userId}` |
| P2_SLUG | Slug | `user-profile-settings-page` | 28 chars | `${pageSlug}` |
| P3_DEEPPATH | Deep API path | `v2/api/organizations/12345/projects/67890` | 42 chars | `${orgId}`, `${projectId}` |
| P4_BEARER | Bearer token | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkw` | 64 chars | `${token}` |
| P5_MULTIPARAM | Multi-param | `category=electronics&minPrice=100&maxPrice=500` | 46 chars | `${category}`, `${minPrice}`, `${maxPrice}` |

### Positive control (1 pattern)

| Pattern | Value type | Concrete value | Value length | Expected |
|---------|-----------|----------------|-------------|----------|
| PC_SHORT | Short numeric | `42` | 2 chars | Parameterized uses MORE tokens (replicates parent) |

### Null control (1 pattern)

| Pattern | Value type | Concrete value | Value length | Expected |
|---------|-----------|----------------|-------------|----------|
| NC_MID | Mid alphanumeric | `abc123` | 6 chars | Direction uncertain (breakeven region) |

### Total: 7 patterns, 21 observations

## Training data construction

For each pattern, 3 training observations with varying concrete values (different IDs, different slugs) to enable parameter induction verification. Training observations use the same `action_template` JSON structure as the parent experiment.

### P1_UUID training values
- `550e8400-e29b-41d4-a716-446655440000`
- `6ba7b810-9dad-11d1-80b4-00c04fd430c8`
- `f47ac10b-58cc-4372-a567-0e02b2c3d479`

### P2_SLUG training values
- `user-profile-settings-page`
- `admin-dashboard-analytics-view`
- `blog-post-comments-section`

### P3_DEEPPATH training values (2 slots: orgId, projectId)
- `v2/api/organizations/100/projects/200`
- `v2/api/organizations/300/projects/400`
- `v2/api/organizations/500/projects/600`

### P4_BEARER training values
- `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkw`
- `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2FwaS5leGFtcGxlLmNvbSIsInN1YiI6InVzZXIxMjM0NTY3ODkwIn0`
- `BKy8jB3XQa9kL7v2mN4pR6wT8yZ1cE5gF0hI2oS4uA7dG9qW3xJ8nK5mP1rV6bQ`

### P5_MULTIPARAM training values (3 slots: category, minPrice, maxPrice)
- `category=electronics&minPrice=100&maxPrice=500`
- `category=clothing&minPrice=25&maxPrice=200`
- `category=books&minPrice=10&maxPrice=100`

### PC_SHORT training values
- `42`
- `7`
- `100`

### NC_MID training values
- `abc123`
- `xyz789`
- `mno456`

## Decision rule

| Condition | Description | Threshold |
|-----------|-------------|-----------|
| C1 | resolve() EXECUTABLE for all 5 long-value params | 5/5 |
| C2 | resolve() UNKNOWN for all 5 missing params | 5/5 |
| C3 | _bind() correct for all 5 long-value patterns | 5/5 |
| C4 | Parameterized fewer tokens for >= 3/5 long-value | >=3/5 |
| C5 | Mean savings across 5 long-value >= 10% | >=10% |
| C6 | Savings increase with value length (r >= 0.7) | r >= 0.7 |
| C7 | Kernel regression 3/3 intact | 3/3 |
| C8 | Positive control: short-value penalty replicates | parameterized > literal |
| ALL | All C1-C8 must pass | — |

### Consequences
- ALL pass → SURVIVES_CURRENT_TEST
- Any fail → FALSIFIED-IN-SETTING

## Scope limitations

- tiktoken cl100k_base only — different LLM tokenizers may differ
- action_template JSON serialization (method + url fields), not full Mechanism object
- Synthetic training data, not real browser sessions
- No network access, no browser, no model calls
- GET-only patterns (no PUT/POST/DELETE)
- All patterns use confidence=0.9, above min_confidence=0.8
- Single test environment (Python 3.12, tiktoken 0.14.0)
- Bearer token is a real JWT-format string (header.payload.signature) — may not represent all token types
- Deep API path uses numeric IDs that could themselves be parameterized — tests the specific case of long path segments
