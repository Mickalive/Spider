# EXP-PRODUCT-35130681515 preregistration

## 1. Experiment identity

- **Experiment ID:** EXP-PRODUCT-35130681515
- **Lane:** product
- **Claim IDs:** C-PARAM-INHERIT, C-PRODUCT-ECON
- **Parent:** EXP-PRODUCT-35124662913 (verdict: SURVIVES_CURRENT_TEST, claim ceiling: committed-code synthetic single-slot with prefix metadata, Fix1/Fix2 necessity quantified)
- **Mode:** Gap resolution — implement Fix3 for protocol-only gap, validate on parent conditions, measure prevalence on realistic URL corpus

## 2. Question

Can a minimum prefix length threshold (Fix3) resolve the Fix2 protocol-only gap while preserving all 8 parent decision-rule conditions, and what is the prevalence of protocol-only over-parameterization patterns in a realistic synthetic URL corpus?

## 3. Hypothesis

Adding Fix3 (minimum prefix length threshold of 12 characters after scheme+authority delimiter) to `distill_parameterized()` rejects protocol-only prefixes like `'https://'` (8 chars) and `'http://'` (7 chars) while preserving `binding_accuracy=1.0` on all 5 parent established conditions (P1/G1/G2/G3/G5) and `slot_count=0` on null controls (N1_ORIGINAL/N1_CORRECTED).

The realistic URL corpus reveals that protocol-only over-parameterization affects a measurable fraction of real API URL patterns, quantifying the cost impact before C-PRODUCT-ECON measurement.

## 4. Falsifier

Any of:

1. Fix3 causes any parent established condition (P1/G1/G2/G3/G5) to drop below `binding_accuracy=1.0`
2. Fix3 fails to reject protocol-only URLs (`slot_count > 0` for PROTOCOL_ONLY condition)
3. Fix3 incorrectly rejects legitimate path-prefix patterns (e.g., `https://api.example.com/users/` with prefix length > 12)
4. The realistic corpus reveals that protocol-only patterns are the dominant URL class, implying the parameterized kernel is fundamentally misdesigned for real traffic

## 5. Conditions

### 5.1 Parent established conditions (regression checks, identical to EXP-PRODUCT-35124662913)

| ID | Training URLs | Unseen URLs | Expected slot_count | Expected binding_accuracy |
|----|---------------|-------------|---------------------|--------------------------|
| P1_PATH_PREFIX | `https://api.example.com/users/{A,B,C}` | `{D,E,F}` | 1 | 1.0 |
| G1_QUERY_STRING_SIMPLE | `https://api.example.com/search?q={alpha,beta,delta}` | `{gamma,epsilon,zeta}` | 1 | 1.0 |
| G2_QUERY_STRING_MULTIPARAM | `https://api.example.com/items?category=books&page={1,2,3}` | `{4,5,6}` | 1 | 1.0 |
| G3_DEEP_PATH | `https://api.example.com/orgs/acme/repos/main/issues/{1,2,3}` | `{4,5,6}` | 1 | 1.0 |
| G5_PATH_QUERY_HYBRID | `https://api.example.com/users/{A,B,C}/items?page=1` | `{D,E,F}` | 1 | 1.0 |

### 5.2 Null controls (inherited + Fix3 target)

| ID | Training URLs | Expected slot_count | Rationale |
|----|---------------|--------------------|----|
| N1_ORIGINAL | `https://api.example.com/a`, `https://api.other.com/b`, `https://api.third.com/c` | 0 | Cross-host: Fix2 rejects prefix ending at `.` |
| N1_CORRECTED | `http://a.com/x`, `ftp://b.org/y`, `custom://c.net/z` | 0 | Truly disjoint: empty-prefix guard rejects |
| PROTOCOL_ONLY | `https://a.com/x`, `https://b.com/y`, `https://c.com/z` | 0 | **Fix3 primary target:** minimum prefix length rejects `https://` (8 chars < 12 threshold) |

### 5.3 Baselines

| ID | Training data | Expected behavior | Purpose |
|----|---------------|-------------------|---------|
| B_UNFIXED_PROTOCOL_ONLY | PROTOCOL_ONLY training data | `slot_count=1` (over-parameterized `https://${url}` without Fix3) | Quantify Fix3 necessity |
| B_UNFIXED_G1 | G1 training data | `binding_accuracy=0.0` (suffix corruption without Fix1) | Inherited from parent, confirm Fix1 necessity |
| B_LITERAL | Any 3 URLs | `confidence=0.5 < min_confidence=0.8`, `fail_rate=1.0` | Confirm parameterized induction necessary |
| B_REALISTIC_PROTOCOL_ONLY | Realistic protocol-only patterns (see 5.5) | `slot_count=0` | Quantify Fix3 effectiveness on realistic data |

### 5.4 Positive control

| ID | Training URLs | Unseen URLs | Expected slot_count | Expected binding_accuracy |
|----|---------------|-------------|---------------------|--------------------------|
| P1_PATH_PREFIX | `https://api.example.com/users/{A,B,C}` | `{D,E,F}` | 1 | 1.0 |

### 5.5 Realistic URL corpus (new for this experiment)

Purpose: Measure prevalence of protocol-only over-parameterization in URL patterns approximating real API traffic.

| ID | Training URLs (3 each) | Unseen URLs (3 each) | Expected slot_count | Expected binding_accuracy | Pattern class |
|----|------------------------|----------------------|---------------------|--------------------------|---------------|
| R1_REST_API | `https://api.example.com/v1/users/{1,2,3}` | `{4,5,6}` | 1 | 1.0 | REST API path-versioned |
| R2_QUERY_HEAVY | `https://search.example.com/results?q={cat,dog,bird}&page={1,2,3}&limit=10` | `{fish,snake,lizard}&page={4,5,6}` | 1 | 1.0 | Search with multiple query params |
| R3_PROTOCOL_ONLY_DEEP | `https://cdn.example.com/images/{logo,banner,icon}.png` | `{hero,thumb,wide}.png` | 1 | 1.0 | CDN with protocol + domain + path |
| R4_CROSS_PROTOCOL | `https://api.example.com/{v1,v2,v3}/data` | `{v4,v5,v6}` | 1 | 1.0 | Version-path parameterization |
| R5_MINIMAL_PREFIX | `https://example.com/{a,b,c}` | `{d,e,f}` | 1 | 1.0 | Short but valid path prefix |
| R6_PROTOCOL_ONLY_SHALLOW | `https://a.com/{x,y,z}` | `{p,q,r}` | 0 | N/A | Protocol + single-char domain (Fix3 target) |

## 6. Decision rule

If ALL of:

1. Fix3 does not introduce import/syntax errors
2. P1: `slot_count=1 AND binding_accuracy=1.0`
3. G1: `slot_count=1 AND binding_accuracy=1.0`
4. G2: `slot_count=1 AND binding_accuracy=1.0`
5. G3: `slot_count=1 AND binding_accuracy=1.0`
6. G5: `slot_count=1 AND binding_accuracy=1.0`
7. N1_ORIGINAL: `slot_count=0`
8. N1_CORRECTED: `slot_count=0`
9. PROTOCOL_ONLY: `slot_count=0` (Fix3 primary target)
10. B_LITERAL: `fail_rate=1.0`

**Verdict = SURVIVES_CURRENT_TEST**

If any condition (2-9) fails: **Verdict = FALSIFIED-IN-SETTING**

B_UNFIXED_PROTOCOL_ONLY, B_UNFIXED_G1, B_REALISTIC_PROTOCOL_ONLY, and the realistic corpus (R1-R6) are reported for prevalence quantification and gap bounding but do not gate the decision rule.

## 7. Algorithm

Fix3 is implemented as a minimum prefix length threshold in `distill_parameterized()`:

```python
def _is_protocol_only_prefix(prefix: str) -> bool:
    """Reject common prefixes that are only scheme+authority without meaningful path content."""
    if not prefix:
        return False
    parts = prefix.split("://", 1)
    if len(parts) != 2:
        return False
    scheme, rest = parts
    # If rest is empty or only contains host (no path segment), it's protocol-only
    if not rest or "/" not in rest:
        return True
    # If the path part after authority is very short, it's likely protocol-only
    authority_end = rest.find("/")
    if authority_end >= 0:
        path_part = rest[authority_end + 1:]
        if len(path_part) < 3:  # e.g., "https://a.com/x" -> path "x" (1 char)
            return True
    return False
```

Fix3 adds a guard at the beginning of `distill_parameterized()` after common prefix computation:

```python
# Fix3: Reject protocol-only prefixes
if _is_protocol_only_prefix(common_prefix):
    return DistillationResult(
        distill_success=False,
        slot_count=0,
        action_template=base_url,
        slot_prefixes={},
        metadata={"rejection_reason": "protocol_only_prefix"}
    )
```

Fix3 is additive: it does not modify Fix1 (suffix guard), Fix2 (delimiter-bound prefix validation), or slot_prefixes extraction behavior. It only adds a pre-check that rejects protocol-only prefixes before Fix1/Fix2 are applied.

## 8. Fix3 threshold justification

The 12-character threshold is chosen because:

- `https://` = 8 characters (scheme + authority delimiter)
- `http://` = 7 characters
- `https://a.com/` = 14 characters (scheme + minimal authority + path delimiter)
- `https://example.com/` = 20 characters

A threshold of 12 characters rejects pure protocol prefixes (`https://`, `http://`) while allowing minimal but meaningful path prefixes (`https://a.com/x` = 14 chars). The `_is_protocol_only_prefix` function provides more structural validation than a raw length check: it verifies that the prefix contains a meaningful path segment beyond the authority.

## 9. Controls and stability

- Fresh Python import per condition (no cross-contamination)
- Training values identical to parent where applicable (P1/G1/G2/G3/G5/N1_ORIGINAL/N1_CORRECTED)
- Training/unseen values disjoint (no leakage)
- n=3 training + 3 unseen per condition (72 binding tests total across 18 conditions)
- Zero model/network/browser calls (deterministic synthetic)
- Deterministic: same inputs produce same outputs
- Fix3 is additive: does not modify existing Fix1/Fix2/slot_prefixes logic

## 10. Product consequences

**Positive:** C-PARAM-INHERIT protocol-only gap resolved. Claim ceiling advances to include Fix3. Path for C-PRODUCT-ECON measurement opens: the protocol-only over-parameterization concern is addressed. Product lane can proceed to real-browser cost measurement.

**Negative:** If Fix3 breaks legitimate binding or the realistic corpus reveals fundamental design issues, C-PARAM-INHERIT remains EXPERIMENTAL with unresolved protocol-only gap. Product lane cannot proceed to C-PRODUCT-ECON until the gap is resolved by a different mechanism.

## 11. What this does NOT establish

- Real-browser external validity (all synthetic, zero model/browser/network calls)
- C-PRODUCT-ECON cost savings (requires real-browser testing)
- Multi-slot induction (G4 architectural bound persists)
- Real-world URL pattern prevalence (realistic corpus is synthetic approximation)
- Cross-site transfer (C-CROSSSITE not tested)
- Fix3 correctness for all possible URL patterns (threshold is empirically chosen)
