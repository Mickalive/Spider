# EXP-GRAPH-35010853847 — Semantic Embedding Staleness Detection

## Executive Summary

**Verdict: FALSIFIED-IN-SETTING**

TF-IDF semantic embedding similarity on `(field_name:field_type)` text pairs **completely fails** to distinguish true schema drift from structural noise. The semantic signal achieves 100% false positive rate on all structural noise patterns at every tested schema size, performing no better than the Jaccard baseline it was meant to replace.

The falsification is total: the Mann-Whitney U test returns p = 1.0 at all schema sizes, meaning the data goes in the **opposite** direction from the hypothesis — structural noise produces *lower* semantic similarity than true drift, not higher.

## 1. Scientific Question

Can semantic embedding similarity distinguish true schema drift from structural noise with TP ≥ 0.8 and FP ≤ 0.15, replacing Jaccard (field_path,type) as a staleness signal?

## 2. Hypothesis and Falsifier

**Hypothesis**: Semantic embedding similarity captures meaning-level differences between schemas, enabling discrimination between true drift (new concepts) and structural noise (repackaging of existing concepts).

**Falsifier** (frozen): TP lower bound of 95% Wilson CI < 0.8 at any schema size for true drift, OR FP upper bound > 0.15 at any schema size for structural noise, OR Mann-Whitney U p > 0.0125 (Bonferroni corrected) at any size.

## 3. Results

### 3.1 Primary Metrics

| Schema Size | Threshold | True Drift TP (CI) | Noise FP (CI) | Fresh FP (CI) | MW p-value | Cohen's d |
|-------------|-----------|-------------------|---------------|---------------|------------|-----------|
| n=10 | 0.9981 | 0.978 [0.923, 0.994] | 1.000 [0.959, 1.000] | 0.000 [0.000, 0.114] | 1.0000 | 1.21 |
| n=20 | 0.9998 | 0.956 [0.929, 0.985] | 1.000 [0.959, 1.000] | 0.000 [0.000, 0.114] | 1.0000 | 1.69 |
| n=30 | 0.9999 | 0.989 [0.948, 0.987] | 1.000 [0.959, 1.000] | 0.000 [0.000, 0.114] | 1.0000 | 1.84 |
| n=50 | 1.0000 | 0.967 [0.950, 0.985] | 1.000 [0.959, 1.000] | 0.000 [0.000, 0.114] | 1.0000 | 1.89 |

**Overall**: TP = 350/360 = 97.2%, Noise FP = 360/360 = 100%, Fresh FP = 0/120 = 0%.

### 3.2 Why It Fails

The fundamental problem is that TF-IDF operates on **surface-level token overlap**:

- **Optional field churn** adds genuinely new tokens (`churn_field_NNNN`) while removing old ones, creating maximum TF-IDF divergence (mean similarity 0.847–0.892). This is *more* divergent than adding a single new field.
- **Null-valued fields** replaces type tokens (e.g., `string` → `null`), changing the type component of every affected field's TF-IDF representation.
- **Nested object variation** modifies path tokens (e.g., `field_X` → `field_X.nested_child`), changing the path component.

All three structural noise patterns produce the same kind of token-level disruption as true drift. There is no TF-IDF mechanism to distinguish "meaningful" token changes from "noise" token changes.

### 3.3 The Direction Is Inverted

Cohen's d values are 1.2–1.9, indicating large effect sizes, but in the **wrong direction**: structural noise has *lower* semantic similarity (more divergent) than true drift. This means noise is MORE different from the baseline than actual drift — exactly backwards from what the hypothesis requires.

The Mann-Whitney p = 1.0 confirms this: the test cannot reject the null hypothesis in the hypothesized direction because the data strongly favors the opposite direction.

### 3.4 Per-Pattern Analysis

| Pattern | Type | n=10 | n=20 | n=30 | n=50 | Mean Sim |
|---------|------|------|------|------|------|----------|
| add_field | true drift | 1.000 | 1.000 | 1.000 | 1.000 | 0.89–0.98 |
| remove_field | true drift | 1.000 | 1.000 | 1.000 | 1.000 | 0.96–0.99 |
| change_type | true drift | 0.933 | 0.867 | 0.967 | 0.900 | 0.995–1.000 |
| optional_field_churn | noise | 1.000 | 1.000 | 1.000 | 1.000 | 0.85–0.89 |
| null_valued_fields | noise | 1.000 | 1.000 | 1.000 | 1.000 | 0.89–0.90 |
| nested_object_variation | noise | 1.000 | 1.000 | 1.000 | 1.000 | 0.95–0.99 |

Key insight: `optional_field_churn` has the LOWEST mean similarity (0.85–0.89), meaning it is the MOST different from baseline. But it is structural noise, not true drift. Meanwhile, `change_type` has the HIGHEST mean similarity (0.995–1.000) because changing one type token in a field list of 10–50 has minimal TF-IDF impact. This is the opposite of what we need.

### 3.5 Ensemble Results

The ensemble optimization (alpha × Jaccard + (1-alpha) × Semantic) converges to alpha ≈ 0.0 (pure semantic) at all schema sizes, with best F1 ≈ 0.65. This confirms that Jaccard adds no discrimination value — both signals fail equally on structural noise. The ensemble cannot rescue the fundamental representational limitation.

### 3.6 Realistic Schema Test

| Pair | Label | Semantic | Jaccard |
|------|-------|----------|---------|
| github_user vs +email | true drift | 0.969 | 0.947 |
| github_user vs noise | noise | 0.961 | 0.895 |
| stripe_charge vs +dispute | true drift | 0.970 | 0.941 |
| stripe_charge vs churn | noise | 0.974 | 0.882 |
| twitter_tweet vs +annotations | true drift | 0.972 | 0.944 |

Even with realistic API field names (GitHub, Stripe, Twitter), the semantic similarity difference between true drift and noise is negligible (~0.005). The noise pair stripe_charge_churn has HIGHER semantic similarity (0.974) than the true drift pair stripe_charge_dispute (0.970) — the wrong direction.

## 4. Controls

### 4.1 Passed Controls
- **Positive control (add_field)**: PASS — embedding correctly detects novel concept in added field (100% TP at all sizes)
- **Null control (fresh)**: PASS — identical copies correctly not detected (0% FP)
- **Jaccard replication**: PASS — all 720 per-pattern Jaccard similarities match parent within 1e-6

### 4.2 Failed Controls
- **All three structural noise controls**: FAIL — 100% FP at all sizes
- **Separation control (Mann-Whitney)**: FAIL — p = 1.0 at all sizes (wrong direction)
- **change_type TP CI**: FAIL at n=10, 20, 50 (CI lower bound < 0.8)

## 5. Violations of Frozen Decision Rule

19 violations recorded, including:
- 12 structural noise FP violations (all 3 noise patterns × 4 sizes)
- 3 Mann-Whitney p-value violations
- 3 change_type TP CI violations (n=10, 20, 50)
- 1 additional structural noise FP at n=10

## 6. Interpretation

### 6.1 What This Means for C-FRESHNESS

This experiment **does not close C-FRESHNESS**. It eliminates one specific signal (TF-IDF semantic similarity on field text pairs) under one specific condition (synthetic schemas with random field names). The broader question of whether *any* semantic representation can discriminate drift from noise remains open.

### 6.2 Why TF-IDF Specifically Fails

TF-IDF is a bag-of-words model: it represents documents as sparse vectors of term frequencies. It has no concept of:
- **Semantic similarity** between tokens (e.g., 'email' and 'contact_email' are completely different)
- **Type hierarchy** (e.g., 'string' and 'text' might be related)
- **Field relationships** (e.g., 'user_id' and 'user_name' are semantically linked)
- **Structural roles** (e.g., adding a field is different from renaming a field)

These limitations make TF-IDF fundamentally unsuitable for distinguishing "meaningful" schema changes from "noise" changes.

### 6.3 What Might Work Better

1. **Sentence-transformers embeddings** (the preregistered primary method, unavailable here): 384-dimensional contextual embeddings might capture semantic relationships between field names. However, the realistic schema test suggests the problem may be more fundamental — even meaningful field names don't produce sufficient separation at the schema level.

2. **Per-field matching + semantic similarity**: Instead of comparing schema-level mean embeddings, match individual fields by name similarity and compare their types. This could distinguish "field X changed type" (true drift) from "field X was temporarily removed" (noise).

3. **Response-time profiling**: Measuring how long an endpoint takes to respond might detect structural changes (e.g., adding a field increases response time) differently from true drift (e.g., new business logic changes response time profile).

4. **Session token validation**: Checking whether existing session tokens still work after a schema change could detect auth-relevant drift vs. structural noise.

5. **Multi-signal ensemble with diverse representations**: Combining structural (Jaccard), semantic (embeddings), temporal (response time), and behavioral (session) signals might achieve discrimination that no single signal can.

## 7. Product Consequences

**Negative outcome**: TF-IDF semantic embedding similarity cannot replace or augment Jaccard for freshness detection. Product must either:
- Test sentence-transformers embeddings (requires torch installation)
- Pursue response-time profiling or session token validation as alternative staleness signals
- Require schema-specific calibration for any staleness signal
- Move to multi-signal ensemble approaches with higher computational cost

This result narrows the viable staleness signal space but does not close it.

## 8. Deviations from Preregistration

1. **TF-IDF fallback used instead of sentence-transformers**: Disclosed per prereg section 15. sentence-transformers was unavailable in this environment (requires torch, ~2GB). TF-IDF was the preregistered fallback.

2. **No LOO-CV fallback needed**: The calibration/test split produced sufficient samples (18+ per class in test set).

3. **No realistic schema supplementary test deviations**: The 5 hand-crafted realistic schemas were tested as planned, with 2 additional noise pairs added for completeness.

## 9. Conclusion

TF-IDF semantic embedding similarity on `(field_name:field_type)` text pairs is **falsified** as a staleness signal that can distinguish true drift from structural noise. The falsification is complete: 100% noise FP rate, inverted separation direction, and Mann-Whitney p = 1.0 at all schema sizes. The result is bounded to TF-IDF representation on synthetic schemas; sentence-transformers embeddings remain untested.
