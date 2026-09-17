# EXP-PRODUCT-35185290656: Fix3 Redesign for Query-Parameterized URLs

## Executive Summary

**Verdict: SURVIVES_CURRENT_TEST** — All 7 frozen decision-rule conditions pass.

The redesigned `_is_protocol_only_prefix` (Fix3) correctly rejects bare authority prefixes while accepting query-parameterized URLs. This resolves the parent experiment's blocker (V2_FIX3_OVERBROAD_BLOCKS_VALID_QUERY_PARAM) where the old Fix3 incorrectly rejected valid `host?query` patterns.

## Key Results

| Condition | Description | Result |
|-----------|-------------|--------|
| C1 | Fix3 rejects bare authority `https://api.example.com` | PASS (True) |
| C2 | Fix3 accepts query-param `https://api.example.com?key=` | PASS (False) |
| C3 | Fix3 accepts path-slash `https://jsonplaceholder.typicode.com/` | PASS (False) |
| C4 | Old Fix3 incorrectly rejects query-param (demonstrates bug) | PASS (True) |
| C5 | Kernel regression tests 3/3 | PASS |
| C6 | HTTP binding accuracy on query-param endpoint | PASS (3/3, 1.0) |
| C7 | distill_parameterized produces correct Mechanism | PASS |

## Fix3 Redesign

**Old logic (overbroad):**
```python
if "/" not in rest:
    return True
```

**New logic (redesigned):**
```python
if "?" not in rest and "/" not in rest and "#" not in rest:
    return True
```

The key change: only reject prefixes that have NO path delimiter (`/`), NO query marker (`?`), and NO fragment marker (`#`) after the authority. This correctly distinguishes:
- `https://api.example.com` → REJECT (bare authority, no path/query/fragment)
- `https://api.example.com?key=` → ACCEPT (has `?`, valid parameterization)
- `https://jsonplaceholder.typicode.com/` → ACCEPT (has `/`, valid path)

## URL Test Corpus (12 patterns, 4 categories)

All 12 patterns pass:
- **Protocol-only (3/3):** `https://api.example.com`, `http://localhost:8080`, `https://a.com` → all REJECT
- **Query-parameterized (3/3):** `https://api.example.com?key=`, `https://example.com?x=`, `https://api.example.com?foo=bar&baz=` → all ACCEPT
- **Path-slash (3/3):** `https://jsonplaceholder.typicode.com/`, `https://jsonplaceholder.typicode.com/posts/`, `https://api.example.com/v1/` → all ACCEPT
- **Mixed/edge (3/3):** `https://api.example.com/path?query=`, `https://example.com#frag`, `https://api.example.com:8080/` → all ACCEPT

## HTTP Binding (C6)

Query-parameterized mechanism distilled from `comments?postId=1/2/3` training observations:
- Template: `https://jsonplaceholder.typicode.com/comments?postId=${url}`
- Slot: `url`
- HTTP binding: 3/3 correct (postIds 5, 6, 7 → status 200, valid JSON body)

## Distill Parameterized (C7)

Mechanism resolves EXECUTABLE with correct bound_action:
- Input: `params = {"url": "5"}`
- Bound URL: `https://jsonplaceholder.typicode.com/comments?postId=5`
- Template correct: True
- Resolves: EXECUTABLE

## Controls

| Control | Type | Expected | Observed | Pass |
|---------|------|----------|----------|------|
| P1_QUERY_PARAM_ACCEPTED | Positive | Fix3 returns False for query-param prefix | False | Yes |
| N1_PROTOCOL_ONLY_REJECTED | Null | Fix3 returns True for bare authority | True | Yes |
| B_OLD_FIX3_OVERBROAD | Baseline | Old Fix3 returns True (demonstrates bug) | True | Yes |
| B_LITERAL_HTTP_REGRESSION | Baseline | 3/3 kernel tests pass | 3/3 pass | Yes |

## Discriminating Test

C7 demonstrates Fix3 independently necessary over Fix2:
- Fix2 (`_validate_prefix_boundary`) passes `https://api.example.com?key=` because prefix ends with `=` (structural delimiter)
- Old Fix3 incorrectly REJECTS this prefix because `?` not in rest check was missing
- Redesigned Fix3 correctly ACCEPTS this prefix because `?` in rest is detected

Fix3 provides non-redundant defense-in-depth: Fix2 handles boundary validation, Fix3 handles protocol-only detection.

## Product Consequence

**Positive outcome:** C-PARAM-INHERIT claim ceiling expands to include host?query parameterization patterns. Fix3 is demonstrated as non-redundant defense-in-depth for bare authority patterns. Claim ceiling: 'path-slash and query-parameterized GET'.

**No product promotion:** C-PARAM-INHERIT remains EXPERIMENTAL. Claim ceiling is synthetic single-slot GET on jsonplaceholder only.

## Scope Limitations

- GET-only endpoints (PUT/POST not tested)
- Single-slot parameterization only
- Synthetic training data from jsonplaceholder.typicode.com
- No browser automation, no model calls, no LLM distillation
- Token cost not re-measured (carried from parent: 68 vs 96 tokens)
