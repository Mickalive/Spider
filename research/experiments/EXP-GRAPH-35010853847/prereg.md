# EXP-GRAPH-35010853847 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-35010853847
- **Lane**: Graph
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Date**: 2026-09-15
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-GRAPH-34788722106 (adaptive Jaccard threshold falsified under structural noise)

## 2. Scientific Question

Can semantic embedding similarity distinguish true schema drift from structural noise with TP>=0.8 and FP<=0.15, replacing Jaccard (field_path,type) as a staleness signal?

## 3. Motivation

### 3.1 Inherited State (from EXP-GRAPH-34788722106 handoff)

**Established:**
- Adaptive Jaccard threshold T(n)=1-0.8/(n+1) achieves TP=360/360=1.0 for single-field drift at n=10,20,30,50
- Null-control FP=0/120=0.0 on identical fresh copies
- Structural-noise FP=360/360=1.0 for optional_field_churn, null_valued_fields, nested_object_variation at all sizes
- Jaccard (field_path,type) is structure-only: it detects single-field drift perfectly but cannot distinguish true drift from structural noise

**Rejected:**
- Adaptive Jaccard threshold T(n)=1-0.8/(n+1) viable under structural noise (FP=1.0 > 0.15)
- Detection margin metric discriminates true drift from structural noise (non-discriminating)

**Unknown:**
- Whether alternative staleness signals (session token validation, semantic embedding similarity, response-time profiling) can discriminate true drift from structural noise
- Whether combining Jaccard with orthogonal staleness signals can rescue freshness detection

**Do Not Assume:**
- C-FRESHNESS is closed or globally rejected (bounded falsification only)
- Any single staleness signal can detect drift under structural noise
- Synthetic noise patterns are representative of real-world API variation

### 3.2 Why Semantic Embeddings

Jaccard (field_path,type) fails because it operates at the structural level: both true drift (adding a genuinely new field) and structural noise (churning optional fields, nulling fields, nesting objects) modify the (field_path,type) set, producing similar Jaccard values below the threshold.

Semantic embeddings operate at the meaning level: they represent the conceptual content of field names and types. True drift introduces new concepts (e.g., adding 'user_email' adds an email concept); structural noise repackages existing concepts (e.g., removing and re-adding the same field, setting a field to null, nesting an existing field). If embeddings capture this distinction, semantic similarity can separate true drift from structural noise where Jaccard cannot.

### 3.3 Prior Art

- SPIDER runtime lane (EXP-RUNTIME-33902315583, EXP-RUNTIME-34054515149) demonstrated that full HTTP response vectors (body + headers) can discriminate auth states, but this is response-level not schema-level
- No prior SPIDER experiment has tested semantic embeddings for schema staleness detection
- The parent experiment's unresolved[3] explicitly flagged "combining Jaccard with orthogonal staleness signals (session token validation, semantic embedding similarity, response-time profiling)" as the next frontier

## 4. Hypotheses

### H1: Semantic Discrimination
Semantic embedding similarity achieves TP>=0.8 on true drift and FP<=0.15 on structural noise across all tested schema sizes (10, 20, 30, 50 fields).

### H2: Semantic Separation
Semantic similarity distributions for true drift and structural noise are significantly separable (Mann-Whitney U p<0.05, Bonferroni corrected for 4 schema sizes).

### H3: Positive Control
Add-field drift produces lower semantic similarity than baseline at all schema sizes (embedding detects novel concept).

### H4: Null Control
Fresh copies produce semantic similarity = 1.0 (or near 1.0 above threshold), yielding FP = 0.

### H5: Semantic vs Structural
Semantic similarity achieves strictly better discrimination than Jaccard (field_path,type) on structural noise (lower FP at equivalent TP).

## 5. Data and Representations

### 5.1 Schema Source

Reuse mock schemas from parent EXP-GRAPH-34788722106 (raw_evidence/mock_schemas.json). This ensures:
- Direct comparability with parent Jaccard measurements
- Same field counts (10, 20, 30, 50)
- Same random field names and types
- Same structural noise patterns at same magnitudes

### 5.2 Schema Text Representation

Each field in a schema is converted to a text string:

```
field_text = f"{field_name}:{field_type}"
```

For nested objects, the field path is used:

```
field_text = f"{field_path}:{field_type}"
```

Example: A schema with fields `id:int, name:string, email:string` produces:

```
["id:int", "name:string", "email:string"]
```

### 5.3 Embedding Generation

**Primary**: sentence-transformers all-MiniLM-L6-v2 (384-dimensional embeddings)
- Encode each field_text independently
- Schema embedding = mean-pooled field embeddings (element-wise average)
- This produces one 384-dim vector per schema

**Fallback**: If sentence-transformers is unavailable, use TF-IDF cosine similarity:
- Corpus = all field_text strings across all schemas in the experiment
- Schema embedding = mean TF-IDF vector across field_texts
- This is a lighter but less semantically rich alternative

### 5.4 Semantic Similarity

```python
semantic_similarity = cosine_similarity(schema_a_embedding, schema_b_embedding)
```

Range: [0, 1] where 1 = identical meaning, 0 = no overlap.

### 5.5 Schema Pairs

For each schema size n and each pattern:
- **Fresh**: baseline vs fresh copy (identical fields, value changes only)
- **True drift** (3 patterns):
  - add_field: baseline vs baseline + 1 new field with novel concept name
  - remove_field: baseline vs baseline - 1 field
  - change_type: baseline vs baseline with 1 field's type changed
- **Structural noise** (3 patterns):
  - optional_field_churn: baseline vs baseline with ~10% fields randomly added/removed
  - null_valued_fields: baseline vs baseline with random fields set to null type
  - nested_object_variation: baseline vs baseline with 1 field converted to nested object

Sample size: 30 pairs per pattern per schema size (matching parent).

## 6. Threshold Optimization

### 6.1 Calibration Set

For each schema size, pool all true drift and structural noise semantic similarity scores. Split 80/20 into calibration and test sets (stratified by pattern type). The calibration set is used to find the optimal threshold; the test set is used for final evaluation.

### 6.2 Threshold Selection

On the calibration set, find the threshold that maximizes the F1 score for discriminating true drift (positive class) from structural noise (negative class). Record the threshold and the corresponding TP/FP on the calibration set.

### 6.3 Final Evaluation

Apply the calibrated threshold to the held-out test set. Report TP, FP, Wilson CIs, and Mann-Whitney U on the test set. This is the confirmatory evaluation.

### 6.4 Fallback: No Calibration

If the calibration/test split produces too few samples for stable threshold estimation (<10 per class in test), use the entire pool with LOO-CV threshold estimation (for each sample, optimize threshold on all other samples, evaluate on held-out sample).

## 7. Baselines

### 7.1 Jaccard (field_path,type) with Adaptive Threshold
- T(n) = 1 - 0.8/(n+1)
- Re-measured on the same schema pairs for direct comparison
- Expected: TP=1.0, FP=1.0 on structural noise (replicates parent)

### 7.2 Jaccard with Fixed Threshold 0.85
- Re-measured on the same schema pairs
- Expected: TP degrades at n>=10 per prior experiments

### 7.3 Random Classifier
- 50% detection, 50% false positive
- Trivially fails both TP>=0.8 and FP<=0.15

### 7.4 Ensemble (alpha * Jaccard + (1-alpha) * Semantic)
- Alpha optimized via 10-fold cross-validation on the pooled true_drift vs noise data
- Tests whether combining structural and semantic signals improves discrimination

## 8. Controls

### 8.1 Positive Control (add_field)
- Semantic similarity for add_field must be < baseline semantic similarity at all sizes
- Verifies: embedding detects novel concept in added field name

### 8.2 Null Control (fresh)
- Semantic similarity for fresh copies must be >= threshold, yielding FP = 0
- Verifies: pipeline does not false-alarm on stable endpoints

### 8.3 Separation Control
- Mann-Whitney U test p < 0.05 (Bonferroni corrected) at each schema size
- Verifies: true drift and structural noise are statistically separable in semantic space

### 8.4 Jaccard Replication Control
- Jaccard achieves TP=1.0 on true drift and FP=1.0 on structural noise
- Verifies: parent results replicate on the reused schemas

## 9. Statistical Tests

### 9.1 Primary: TP and FP with Wilson CIs
- Wilson 95% CI for TP (true drift patterns) and FP (structural noise patterns) at each schema size
- TP lower bound >= 0.8 and FP upper bound <= 0.15 required for SURVIVES_CURRENT_TEST

### 9.2 Separation: Mann-Whitney U
- One-sided test: semantic similarity for true drift < semantic similarity for structural noise
- Bonferroni correction for 4 schema sizes (alpha = 0.05/4 = 0.0125)

### 9.3 Effect Size: Cohen's d
- For semantic similarity difference between true drift and structural noise at each size
- Reports practical significance alongside statistical significance

### 9.4 Comparison: Paired Bootstrap
- Compare semantic FP vs Jaccard FP at each schema size using paired bootstrap (1000 resamples)
- Tests whether semantic achieves strictly lower FP than Jaccard

## 10. Validity Threats

### 10.1 Embedding Quality
all-MiniLM-L6-v2 is a general-purpose sentence embedding model. It may not capture domain-specific semantic relationships between field names (e.g., 'user_email' and 'contact_email' may be semantically similar even though they represent different fields). Mitigation: report per-pattern analysis to identify which noise patterns are most/least separable.

### 10.2 Synthetic-to-Real Gap
Mock schemas have random field names (e.g., 'field_0', 'field_1') that may not reflect real API naming conventions. Real APIs use meaningful names (e.g., 'userId', 'createdAt') where semantic similarity may behave differently. Mitigation: add a supplementary test with 5 hand-crafted realistic schemas (e.g., GitHub API, Stripe API, Twitter API subsets) to bound the synthetic-to-real gap.

### 10.3 Threshold Overfitting
Optimizing threshold on the calibration set may overfit to the specific noise patterns tested. Mitigation: held-out test set evaluation; LOO-CV fallback; reporting both calibration and test performance.

### 10.4 Schema Size Confound
Semantic similarity may vary with schema size independently of drift/noise type (longer field lists may produce different mean-pooling behavior). Mitigation: evaluate at each schema size independently; do not pool across sizes for the primary analysis.

### 10.5 Parent Schema Reuse
Reusing parent schemas ensures comparability but means the same random field names are used. If the parent's random names happen to be semantically distinctive, this could inflate semantic discriminability. Mitigation: supplementary test with realistic schemas; report per-pattern analysis.

## 11. Decision Rules

### 11.1 SURVIVES_CURRENT_TEST
If ALL of:
1. Semantic TP lower bound >= 0.8 at all 4 schema sizes
2. Semantic FP upper bound <= 0.15 at all 4 schema sizes
3. Mann-Whitney U p < 0.0125 (Bonferroni corrected) at all 4 sizes
4. Positive control passes (add-field semantic < baseline)
5. Null control passes (fresh FP = 0)
6. No pipeline errors

### 11.2 MIXED
If semantic achieves TP>=0.8 and FP<=0.15 but ensemble achieves strictly better separation (higher Mann-Whitney U statistic or lower p-value at >=3/4 sizes).

### 11.3 FALSIFIED-IN-SETTING
If ANY of:
1. Semantic TP lower bound < 0.8 at any size
2. Semantic FP upper bound > 0.15 at any size
3. Mann-Whitney U p > 0.0125 at any size after correction
4. Positive or null control fails
5. Jaccard replication fails (TP < 1.0 on true drift or FP < 0.8 on noise, suggesting schema generation issue)

### 11.4 MEASUREMENT_INVALID
If:
1. sentence-transformers and TF-IDF both fail
2. Sample sizes insufficient (<10 per class in test set)
3. Pipeline errors prevent computation
4. Parent schemas cannot be loaded

## 12. Expected Outcomes

### 12.1 Positive Result (SURVIVES_CURRENT_TEST)
- Semantic embedding similarity is a viable staleness signal for SPIDER
- Can replace or augment Jaccard for freshness detection
- Product lane can integrate semantic freshness scoring
- C-FRESHNESS moves from HYPOTHESIS toward EXPERIMENTAL/VALIDATED
- Next step: test on real API schemas; measure computational cost for product integration

### 12.2 Mixed Result (MIXED)
- Semantic alone works but ensemble is better
- Product should use ensemble approach (Jaccard + semantic)
- Indicates that structural and semantic signals are complementary
- Next step: optimize ensemble weights; test on real APIs

### 12.3 Negative Result (FALSIFIED-IN-SETTING)
- Semantic embeddings cannot distinguish drift from noise at the tested magnitudes
- Product must pursue response-time profiling, session token validation, or multi-signal ensembles
- Does NOT close C-FRESHNESS — only this specific signal
- Next step: test response-time profiling (highest-cost but potentially most discriminating signal)

### 12.4 Invalid Result (MEASUREMENT_INVALID)
- Pipeline infrastructure issue, not scientific evidence
- Debug and retry

## 13. Analysis Plan

1. **Schema Loading**: Load mock_schemas.json from parent experiment
2. **Embedding Generation**: Generate schema embeddings via sentence-transformers or TF-IDF fallback
3. **Similarity Computation**: Compute semantic similarity for all schema pairs
4. **Jaccard Replication**: Compute Jaccard for all schema pairs (verify parent results)
5. **Threshold Optimization**: Find optimal threshold on calibration set per schema size
6. **Final Evaluation**: Apply threshold to test set, compute TP/FP/Wilson CIs
7. **Statistical Tests**: Mann-Whitney U, Cohen's d, paired bootstrap
8. **Ensemble**: Optimize alpha for Jaccard+semantic combination
9. **Supplementary**: Realistic schema test (5 hand-crafted API schemas)
10. **Reporting**: All outcomes reported with equal prominence

## 14. Inherited Decision Constraints

From parent handoff EXP-GRAPH-34788722106:
- The adaptive Jaccard threshold direction is falsified under structural noise
- The recommended next action is to test orthogonal staleness signals
- This experiment directly follows that recommendation
- Established parent results (Jaccard TP=1.0 on true drift, FP=1.0 on noise) are treated as inherited facts, not re-hypothesized

From claim registry:
- C-FRESHNESS status is HYPOTHESIS
- Next gate: "session/token/DOM/endpoint/permission drift with false-accept measurement"
- This experiment addresses the semantic component of that gate

## 15. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

Deviations that require disclosure:
- If sentence-transformers is unavailable and TF-IDF fallback is used, this must be disclosed as a representation change
- If parent schemas cannot be loaded and new schemas are generated, this breaks comparability and must be disclosed
- If the calibration/test split produces too few samples and LOO-CV is used, this must be disclosed as an analysis change

## 16. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
