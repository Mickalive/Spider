# EXP-PRODUCT-35209109455 — Report

## Experiment

Multi-pattern token economics of parameterized vs literal mechanism representation, with resolve/bind pipeline validation.

## Verdict: FALSIFIED-IN-SETTING

The frozen decision rule requires ALL of C1–C7 to pass for SURVIVES_CURRENT_TEST. Three conditions fail:

- **C4 FAIL** (0/5): Parameterized mechanisms use MORE tokens than literal mechanisms for all 5 patterns, not fewer
- **C5 FAIL**: Mean token savings is -6.4% (negative), far below the 15% threshold
- **C6 FAIL**: Token savings DECREASE with parameter count (3-param -9.68% worse than 1-param -4.81%)

The resolve/bind pipeline (C1–C3) and kernel regression (C7) pass perfectly.

## Token Measurements

| Pattern | Params | Literal | Param | Savings | Direction |
|---------|--------|---------|-------|---------|-----------|
| 1. Path param | 1 | 19 | 20 | -5.26% | param worse |
| 2. Query param | 1 | 23 | 24 | -4.35% | param worse |
| 3. Two query | 2 | 25 | 26 | -4.0% | param worse |
| 4. Path+query | 2 | 23 | 25 | -8.70% | param worse |
| 5. Three query | 3 | 31 | 34 | -9.68% | param worse |

**Mean savings: -6.4%** (parameterized uses 6.4% MORE tokens on average)

## Root Cause

The `${varname}` template syntax adds fixed overhead per slot: `$` + `{` + varname + `}` = varname.length + 4 characters. For the tested URL patterns, the concrete values are short (1–3 digit numbers), so the template variable names (id, userId, limit, page, category, minPrice, maxPrice) are longer than the values they replace.

Example for pattern_5:
- Literal: `"category=books&minPrice=10&maxPrice=50"` → 38 chars
- Parameterized: `"category=${category}&minPrice=${minPrice}&maxPrice=${maxPrice}"` → 56 chars (18 chars overhead for 3 slots)

This is a structural property of the template representation: **savings require concrete values longer than the template variable name + syntax overhead**.

## Resolve/Bind Pipeline

All 5 patterns pass the resolve/bind pipeline:

| Pattern | resolve(exec) | resolve(miss) | bind correct |
|---------|---------------|---------------|--------------|
| 1. Path param | EXECUTABLE | UNKNOWN | ✓ |
| 2. Query param | EXECUTABLE | UNKNOWN | ✓ |
| 3. Two query | EXECUTABLE | UNKNOWN | ✓ |
| 4. Path+query | EXECUTABLE | UNKNOWN | ✓ |
| 5. Three query | EXECUTABLE | UNKNOWN | ✓ |

The kernel correctly:
- Resolves parameterized mechanisms when all required slots are provided
- Returns UNKNOWN when slots are missing
- Binds template variables to concrete values via `_bind()`

## Kernel Regression

3/3 existing tests pass. No regression.

## Implications for Claims

### C-PARAM-INHERIT (EXPERIMENTAL)

The resolve/bind pipeline works correctly for manually-registered parameterized mechanisms with 1–3 parameter slots. However, the token economics hypothesis is falsified for short-value URL patterns. The claim ceiling is narrowed:

- **Supported**: resolve() and _bind() correctly handle parameterized mechanisms with 1–3 slots
- **Falsified**: parameterized representation does not reduce token cost for URL patterns with short numeric values
- **Open**: token savings may exist for patterns with long concrete values (UUIDs, slugs, full paths)

### C-PRODUCT-ECON (HYPOTHESIS)

Negative evidence on token component: parameterized representation adds per-mechanism token cost rather than reducing it for typical URL patterns. End-to-end amortized cost remains unmeasured. Product lane may need to reconsider whether token savings are a viable economic argument for parameterized inheritance.

## Comparison with Parent

The parent experiment (EXP-PRODUCT-35185290656) reported 68 tokens parameterized vs 96 tokens literal (29.17% savings) for a single `comments?postId=${url}` pattern. This experiment finds the opposite: all 5 patterns show negative savings.

Possible explanations:
1. Parent may have measured a different action_template structure (e.g., without full URL domain)
2. Parent may have used a different encoding or JSON serialization
3. The single data point was not generalizable

The parent's 29.17% savings figure should not be cited as established; this experiment's multi-pattern measurement provides stronger evidence that the savings do not generalize.

## Product Consequence

**Negative outcome authorized by frozen decision rule**: The product lane should not use token savings as a selling point for parameterized inheritance when concrete values are short. Alternative economic arguments (amortization across tasks, mechanism deduplication, retrieval efficiency) remain open but unmeasured.
