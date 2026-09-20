# EXP-INTEL-35476271877 — Preregistration

## Status: DESIGN COMPLETE — PENDING FREEZE

## Context

Two consecutive BLOCKED runs (EXP-INTEL-35462974425, EXP-INTEL-35470447439) failed because Docker image am1n3e/webarena-verified-shopping:latest is unavailable, preventing full-DOM data re-collection. The parent handoff identifies full-DOM testing as the highest-information question for the MIXED program, but Docker is the sole blocking action.

Rather than retry Docker (risking a third BLOCKED run), this experiment extracts maximum information from existing data by diagnosing the ROOT CAUSE of the ranking instability.

## Key inherited finding

The parent experiment (EXP-INTEL-35445596324) revealed a paradoxical dissociation:

| Recipe type | Discrimination (eta2) | Ranking agreement |
|---|---|---|
| Canonical (shared subset) | 0.9205 (HIGH) | 55.95% (LOW) |
| Per-task (independent subset) | 0.3664 (LOW) | 78.65% (MODERATE) |
| Non-recipe (full pipeline) | 0.9958 (NEAR-PERFECT) | 100% (PERFECT) |

This dissociation is unexplained. Understanding it is prerequisite to predicting whether full DOM would help.

## Analytical approach

### 1. Per-iteration density decomposition

For each of the 1000 canonical recipe iterations at effective_n ∈ {5, 10, 15, 20}:

- Compute per-task density: d_task = sum(feature_value for matching elements) / elements_with_bbox
- Compute type means: mu_listing = mean(d_listing_tasks), mu_detail = mean(d_detail_tasks)
- Compute margin: M = mu_listing - mu_detail
- Compute within-type SE: SE_listing = std(d_listing_tasks) / sqrt(3), SE_detail = std(d_detail_tasks) / sqrt(3)
- Compute SNR: SNR = M / sqrt(SE_listing^2 + SE_detail^2)
- Record whether ranking is preserved: mu_listing > mu_detail

### 2. SNR model

Model ranking agreement as a function of SNR:

P(agree) = Phi(SNR) where Phi is the standard normal CDF

This model assumes the ranking flip is caused by Gaussian noise in the type means exceeding the margin.

Fit the model to n=5/10/15/20 data points. Validate by comparing predicted vs observed agreement.

### 3. Extrapolation

Fit margin(n) and SE(n) as functions of effective_n using the 4 data points (n=5/10/15/20).

Extrapolate to n=50 (midpoint of full-DOM range) and n=82 (maximum full-DOM).

Report prediction intervals accounting for extrapolation uncertainty.

### 4. Mechanism identification

Decompose the instability into:
- **Margin deficit**: Is M small relative to SE at n=20?
- **Task variance**: Is within-type task variance high (CV > 0.1)?
- **Correlation structure**: Is recipe noise correlated across tasks of the same type (rho > 0.3)?

### 5. Hybrid recipe test (exploratory)

For α ∈ {0, 0.2, 0.4, 0.6, 0.8, 1.0}, compute:

hybrid_density = α × canonical_density + (1-α) × per_task_density

Measure eta2 and ranking agreement for each α. Identify whether a sweet spot exists (eta2 ≥ 0.80 AND agreement ≥ 80%).

This is exploratory per §14 — results are hypothesis-generating only.

## Analysis plan

### Phase A: Data preparation

1. Load raw data from EXP-INTEL-34782350557 (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050)
2. Load analysis framework from EXP-INTEL-35445596324 (analyze.py sha256: 5acc37315ef28a5dd21420701c6826c4fc8f242fadbd7ccd4481ea83e123b724)
3. Select 7 tasks (3 listing, 3 detail, 1 cart deduplicated)
4. Verify within-type template invariance persists

### Phase B: Per-iteration density computation

For each effective_n ∈ {5, 10, 15, 20}:
1. Subsample first-n elements from each task's locatable_sample
2. Compute per-element features (tag_entropy, form_fraction, total_area)
3. For canonical recipe (shared role subset p=0.5):
   - Run 10 seeds × 1000 iterations
   - For each iteration: select roles, compute density per task, record density and ranking
4. For per-task recipe (independent role subset p=0.5 per task):
   - Run 10 seeds × 1000 iterations
   - For each iteration: select roles independently per task, compute density per task, record density and ranking

### Phase C: SNR decomposition

For each effective_n:
1. Compute per-iteration margin: M_i = mu_listing_i - mu_detail_i
2. Compute per-iteration SE: SE_i = sqrt(SE_listing_i^2 + SE_detail_i^2)
3. Compute per-iteration SNR: SNR_i = M_i / SE_i
4. Compute agreement: fraction of iterations where M_i > 0
5. Fit SNR model: agreement ≈ Phi(mean(SNR))
6. Report residual: |predicted - observed|

### Phase D: Extrapolation

1. Fit margin(n) = a * n^b (power law) to 4 data points
2. Fit SE(n) = c * n^d (power law) to 4 data points
3. Extrapolate to n=50 and n=82
4. Compute predicted agreement at n=50 and n=82
5. Report 90% prediction intervals

### Phase E: Mechanism identification

1. Compute margin/SE ratio at n=20
2. Compute within-type CV of density at n=20
3. Compute correlation of recipe noise across listing tasks and across detail tasks
4. Classify primary mechanism: margin deficit, task variance, or correlation

### Phase F: Hybrid recipe (exploratory)

For each α ∈ {0, 0.2, 0.4, 0.6, 0.8, 1.0}:
1. Compute hybrid density = α × canonical + (1-α) × per_task
2. Compute eta2 of hybrid density
3. Compute ranking agreement of hybrid density
4. Report eta2 vs agreement tradeoff curve

## Frozen inputs

- Raw data: EXP-INTEL-34782350557 raw_evidence (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050)
- Analysis framework: EXP-INTEL-35445596324 analyze.py (sha256: 5acc37315ef28a5dd21420701c6826c4fc8f242fadbd7ccd4481ea83e123b724)
- Parent results: EXP-INTEL-35445596324 result.json (metrics M4, M5, M6, M7, M8)
- Definitions: DEF-FULL-MAP (a→link, input→textbox), DEF-FORM-ONLY (form roles only)
- Effective_n values: {5, 10, 15, 20}
- Recipe parameters: 10 seeds × 1000 iterations, role subset p=0.5
- Tasks: 3 listing + 3 detail + 1 cart (deduplicated), truncated-first-20 locatable_sample

## Decision criteria

C1_SNR_MODEL_VALID:
- Predicted agreement at n=15 within 10pp of 49.98%
- Predicted agreement at n=20 within 10pp of 55.95%
- Both must pass for C1 to pass

C2_MECHANISM_IDENTIFIED:
- At least one mechanism classified with quantitative support:
  - Margin deficit: margin/SE < 3 at n=20
  - Task variance: CV > 0.1 at n=20
  - Correlation: rho > 0.3 across tasks of same type

C3_EXTRAPOLATION_FALSIFIES_FULL_DOM:
- Extrapolated agreement at n=50 < 80%
- If extrapolated agreement >= 80%, C3 FAILS (supports full-DOM testing)

## Verdict rules

- NOT C1 → MEASUREMENT_INVALID
- C1 AND NOT C2 → MIXED (model valid, mechanism unclear)
- C1 AND C2 AND C3 → FALSIFIES-FULL-DOM (plateau structural, recipe density limited)
- C1 AND C2 AND NOT C3 → SUPPORTS-FULL-DOM (plateau may break at full DOM, Docker warranted)

## Product consequences

**If C3 (FALSIFIES-FULL-DOM)**:
- Recipe density structurally limited to ~56% agreement at any element count
- Product lane adopts non-recipe density immediately (100% ranking agreement, eta2=0.999)
- Docker re-collection NOT justified for ranking stability question
- The MIXED program bottleneck is resolved negatively: recipe density is not viable

**If NOT C3 (SUPPORTS-FULL-DOM)**:
- Plateau at 56% is artifact of narrow truncated-first-20 range
- Full DOM (n=21-82) predicted to cross 80% threshold
- Docker re-collection IS justified
- Product lane waits for full-DOM results before closing recipe density path

## Representation loss and validity threats

1. **First-n subsampling**: Effective_n subsampling uses first-n elements (DOM-ordered), not random subsets. The monotonic improvement (Spearman=1.0) suggests this captures meaningful structure, but first-n may over-represent top-of-page elements that are more uniform across page types.

2. **Small type sample**: Only 3 tasks per type (listing, detail). Within-type statistics are estimated from n=3, which is very noisy. The SNR model's prediction uncertainty is dominated by this small sample.

3. **Template invariance**: Tasks of the same type share identical element features in the truncated-first-20 sample. This means within-type variance in density is driven entirely by recipe sampling, not by genuine task differences. At full DOM, template invariance may break, changing the variance structure.

4. **Single site**: All data is from one Magento Docker site. Cross-site generalization not tested.

5. **Extrapolation risk**: Power-law extrapolation from 4 data points (n=5/10/15/20) to n=50-82 is inherently uncertain. Prediction intervals will be wide.

6. **Cart degeneracy**: Cart n=1 makes within-type variance degenerate. Analysis focuses on listing vs detail only.

## Frozen at

DESIGN COMPLETE — pending FREEZE by deterministic freezer.
