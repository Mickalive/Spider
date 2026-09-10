# EXP-PRODUCT-34485517221 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34485517221
- **Lane**: Product
- **Claims**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Date**: 2026-09-10
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Does the leaf-path URL-as-string prefix extraction heuristic (rfind('/') based) generalize to structurally different URL patterns — query-string parameters, multi-segment path variation, and URLs with no common prefix — or does it fail on patterns that are common in real-world API designs?

## 3. Motivation

### Inherited state from EXP-PRODUCT-34420092879

The parent experiment resolved the C2 double-prefix bug at the kernel level (bind-time slot-level prefix extraction, binding_accuracy=1.0 across 10 conditions, 34/34 bindings correct). However, the audit flagged a medium-severity finding:

**V3_REPRESENTATION_LOSS**: The kernel's leaf-path model treats the full URL as a single leaf. Slot extraction uses `rfind('/')` to split URL prefix from slot prefix. This works for tested patterns (`https://site-a.com/hook` → `site-`, `https://api.example.com/users/user-1` → `user-`) but would not generalize to query-string decomposition or multi-segment variation.

Specifically, D2 template `https://api.example.com/search?q=${url}` with `slot_prefixes={'url': 'search?q='}` was identified as an artifact of the rfind('/') heuristic, not general query-string decomposition. The prefix `search?q=` was captured because rfind('/') on the URL returns the position of the last `/` before `?q=`, which happens to produce the correct prefix for short values but is structurally incorrect.

The parent handoff explicitly lists as unknown:
- "Whether leaf-path URL-as-string heuristic generalizes to query-string decomposition or multi-segment variation"
- "Prefix extraction robustness beyond tested consistent-prefix distributions"

### Why this matters

If the heuristic fails on common real-world URL patterns (query strings, multi-segment REST paths, URLs with no common prefix), then:
1. The parameterized kernel cannot handle a significant fraction of real API URLs
2. C-PRODUCT-ECON economics measurement would be measuring a broken mechanism
3. The kernel needs a more robust prefix extraction approach before product deployment

If the heuristic succeeds, then:
1. V3_REPRESENTATION_LOSS is resolved
2. C-PRODUCT-ECON measurement can proceed with confidence
3. The leaf-path URL-as-string model is validated for common API URL patterns

### Why now

This is the smallest high-information experiment between the established kernel correctness (EXP-PRODUCT-34420092879) and the target product economics measurement (C-PRODUCT-ECON). It resolves a specific audit finding before committing to the higher-cost economics measurement.

## 4. Hypotheses

### H1: Query-String Generalization
The heuristic correctly extracts slot_prefixes for query-string URL patterns where the varying parameter appears after `?` or `&`.

### H2: Multi-Segment Generalization
The heuristic correctly identifies multiple distinct varying segments in multi-segment path URLs.

### H3: No-Common-Prefix Null
The heuristic produces slot_count=0 when observations share no common URL prefix.

### H4: Path-Query Hybrid
The heuristic handles URLs with both path segments and query parameters, extracting the correct prefix for the varying segment.

### H5: Deep Path Prefix
The heuristic handles URLs with multiple path segments before the varying slot.

## 5. Test Conditions

### P1_PATH_PREFIX (Positive Control)
- **Training**: 3 observations of `https://api.example.com/users/{A,B,C}`
  - `https://api.example.com/users/A`
  - `https://api.example.com/users/B`
  - `https://api.example.com/users/C`
- **Unseen values**: `D`, `E`, `F`
- **Expected slot_count**: 1
- **Expected slot_prefixes**: `{'user': 'users/'}`
- **Expected binding**: `https://api.example.com/users/D` etc.
- **Rationale**: Replicates the established pattern from parent experiments. Verifies pipeline works.

### G1_QUERY_STRING_SIMPLE
- **Training**: 3 observations of `https://api.example.com/search?q={alpha,beta,gamma}`
  - `https://api.example.com/search?q=alpha`
  - `https://api.example.com/search?q=beta`
  - `https://api.example.com/search?q=gamma`
- **Unseen values**: `delta`, `epsilon`, `zeta`
- **Expected slot_count**: 1
- **Expected slot_prefixes**: `{'query': 'search?q='}`
- **Expected binding**: `https://api.example.com/search?q=delta` etc.
- **Rationale**: Tests whether rfind('/') correctly captures `search?q=` as prefix. The rfind('/') on `search?q=alpha` finds `/` at position 27 (after `.com`), giving prefix `https://api.example.com/search?q=`. For `search?q=beta` same prefix. Common prefix is `https://api.example.com/search?q=`. This should work because the varying part (`alpha`/`beta`/`gamma`) starts at the same position.
- **Validity note**: This is the specific pattern flagged in V3_REPRESENTATION_LOSS as "structurally incorrect but happens to bind correctly for short values." We test whether it actually works for unseen values.

### G2_QUERY_STRING_MULTIPARAM
- **Training**: 3 observations with 2 query parameters, one varying:
  - `https://api.example.com/items?category=books&page=1`
  - `https://api.example.com/items?category=books&page=2`
  - `https://api.example.com/items?category=books&page=3`
- **Unseen values for page**: `4`, `5`, `6`
- **Expected slot_count**: 1 (only page varies)
- **Expected slot_prefixes**: `{'page': 'items?category=books&page='}`
- **Expected binding**: `https://api.example.com/items?category=books&page=4` etc.
- **Rationale**: Tests whether the heuristic correctly identifies that only `page` varies while `category=books` is constant. The common prefix across observations is `https://api.example.com/items?category=books&page=`.

### G3_DEEP_PATH
- **Training**: 3 observations with deep path:
  - `https://api.example.com/orgs/acme/repos/main/issues/1`
  - `https://api.example.com/orgs/acme/repos/main/issues/2`
  - `https://api.example.com/orgs/acme/repos/main/issues/3`
- **Unseen values**: `4`, `5`, `6`
- **Expected slot_count**: 1
- **Expected slot_prefixes**: `{'issue_id': 'repos/main/issues/'}`
- **Expected binding**: `https://api.example.com/orgs/acme/repos/main/issues/4` etc.
- **Rationale**: Tests whether the heuristic handles deep path structures. The rfind('/') on `.../issues/1` finds `/` before `1`, giving prefix `.../issues/`. Common prefix across observations is `https://api.example.com/orgs/acme/repos/main/issues/`.

### G4_MULTI_SLOT
- **Training**: 3 observations with 2 varying segments:
  - `https://api.example.com/users/alice/orders/100`
  - `https://api.example.com/users/bob/orders/200`
  - `https://api.example.com/users/charlie/orders/300`
- **Unseen values**: user=`dave` order=`400`, user=`eve` order=`500`, user=`frank` order=`600`
- **Expected slot_count**: 2
- **Expected binding**: `https://api.example.com/users/dave/orders/400` etc.
- **Rationale**: Tests whether the heuristic can identify 2 distinct varying segments. This is a harder case: the common prefix varies across observation pairs. The parameterized kernel must identify that both `users/` and `orders/` contain varying slots.
- **Note**: This condition may fail because the rfind('/') heuristic treats the URL as a single leaf and may only extract one prefix. If it fails, this identifies a real limitation of the leaf-path model.

### G5_PATH_QUERY_HYBRID
- **Training**: 3 observations with path segment and query parameter:
  - `https://api.example.com/users/alice/items?page=1`
  - `https://api.example.com/users/bob/items?page=1`
  - `https://api.example.com/users/charlie/items?page=1`
- **Unseen values**: user=`dave`, user=`eve`, user=`frank`
- **Expected slot_count**: 1 (only user varies; page=1 is constant)
- **Expected slot_prefixes**: `{'user': 'users/'}`
- **Expected binding**: `https://api.example.com/users/dave/items?page=1` etc.
- **Rationale**: Tests whether the heuristic correctly identifies the varying path segment while treating the constant query parameter as part of the prefix.

### N1_NO_COMMON_PREFIX (Null Control)
- **Training**: 3 observations with completely different URLs:
  - `https://api.example.com/a`
  - `https://api.other.com/b`
  - `https://api.third.com/c`
- **Unseen values**: `x`, `y`, `z`
- **Expected slot_count**: 0
- **Rationale**: No common structure should induce no parameterization.

## 6. Measures

### 6.1 Primary Metric
- **condition_pass_rate**: Fraction of 7 conditions (P1 + G1-G5 + N1) where both slot_count matches expected AND binding_accuracy=1.0 for all unseen values

### 6.2 Per-Condition Metrics
- **slot_count**: Number of parameter slots induced
- **slot_prefixes**: Extracted prefix per slot
- **binding_accuracy**: Fraction of unseen values that bind correctly (strict JSON equality)
- **induced_template**: The action_template with slot placeholders

### 6.3 Aggregate Metrics
- **overall_binding_accuracy**: Mean binding_accuracy across all conditions with unseen values
- **structural_generalization_rate**: Fraction of G1-G5 conditions that pass (excludes positive control and null)

## 7. Controls

### 7.1 Positive Control (P1_PATH_PREFIX)
- Expected: slot_count=1, binding_accuracy=1.0
- Purpose: Verify pipeline works on established pattern

### 7.2 Null Control (N1_NO_COMMON_PREFIX)
- Expected: slot_count=0
- Purpose: Verify no parameterization hallucinated when no structure exists

### 7.3 Regression Baseline (B_LITERAL)
- Literal mechanism reuse (confidence 0.5 < min_confidence 0.8)
- Expected: fail_rate=1.0 (all resolutions return UNKNOWN/EXPLORE)
- Purpose: Confirm parameterized induction is necessary

## 8. Validity Threats

### 8.1 rfind('/') Specificity
The test conditions are designed to specifically probe the rfind('/') heuristic. If the heuristic is replaced with a different prefix extraction method, these conditions may have different outcomes. This is by design — we are testing the current implementation, not a hypothetical better one.

### 8.2 Synthetic URL Patterns
All URLs are synthetic and deterministic. Real-world URLs may have additional complexity (URL encoding, fragments, port numbers, authentication in URL). This experiment tests structural generalization within the URL-as-string model, not full URL parsing.

### 8.3 Training Data Size
3 training observations per condition matches the parent experiment protocol. With only 3 observations, the common prefix computation is exact (minimum of 3 strings). Larger training sets might reveal different prefix extraction behavior.

### 8.4 Multi-Slot Detection (G4)
The G4 condition tests 2 varying segments. The current kernel may not support multi-slot detection via rfind('/') because it treats the URL as a single leaf. If G4 fails, this is an expected limitation of the leaf-path model, not a measurement error.

### 8.5 Expected Failure Modes
- G1 (query string): Should work if rfind('/') correctly captures the prefix before the varying parameter
- G2 (multi-param query): Should work if constant parameters are part of the common prefix
- G4 (multi-slot): Likely to fail — the leaf-path model may only detect 1 slot
- G5 (path-query hybrid): Should work if the varying path segment is correctly identified

## 9. Analysis Plan

1. Execute each condition independently with fresh temporary registry
2. Record slot_count, slot_prefixes, binding_accuracy per condition
3. Apply decision rule: ≥6/7 pass → SURVIVES_CURRENT_TEST; 4-5 pass → MIXED; ≤3 pass → FALSIFIED-IN-SETTING
4. Report per-condition results with slot_prefixes and binding details
5. Identify which URL classes pass and which fail
6. If MIXED or FALSIFIED, classify failures by URL structure type

## 10. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 11. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
