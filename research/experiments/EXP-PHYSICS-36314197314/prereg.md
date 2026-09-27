# Preregistration: EXP-PHYSICS-36314197314

**Experiment ID**: EXP-PHYSICS-36314197314
**Lane**: physics
**Claim ID**: C-WEB-DYNAMICS
**Date**: 2026-09-27
**Status**: FROZEN BEFORE ANY OUTCOME INSPECTION

---

## 1. Question

Does the real interactive Web contain predictive structure **BEYOND memory and ordinary similarity**, tested at the coarsest level of description and on real sites rather than on synthetic data-generating processes?

Using a frozen, preregistered pool of real credential-free public origins (disjoint from the graph and frontier host sets this cycle), with state represented as a response signature over (status, selected header fields, body-shape summary) and actions as the frozen GET-path transformations available without credentials:

**Does an INHERITED-MECHANISM predictor** — conditioning on a mechanism's declared semantic effect and its **BOUND parameter values**, as SPIDER's product would actually condition on — **predict the held-out response signature of a NEVER-OBSERVED identifier better than**:

- (B1) a first-order Markov model on (URL, action),
- (B2) TF-IDF k=5 retrieval over the training responses,
- (B3) cold re-derivation with no stored knowledge,

**scored by held-out log predictive density and Brier score on the response signature, with trajectory- and site-grouped permutation nulls and site-clustered intervals?**

---

## 2. Hypothesis

An inherited-mechanism predictor that conditions on a mechanism's declared semantic effect and its bound parameter values will achieve higher held-out log predictive density and lower Brier score on response signatures of never-observed identifiers than all three baselines (first-order Markov, TF-IDF k=5 retrieval, cold re-derivation), demonstrating predictive structure beyond memory and ordinary similarity on real credential-free public Web origins.

---

## 3. Falsifier

The inherited-mechanism predictor does not outperform all three baselines on both held-out log predictive density and Brier score, OR the improvement is not statistically distinguishable from the trajectory- and site-grouped permutation nulls, OR the positive control (planted mechanism) is not detected, OR the placebo control (permuted mechanism) is spuriously detected.

---

## 4. State Representation: Response Signature

**Raw observation preserved**: Full HTTP response (status code, all headers, body bytes).

**Derived representation (response signature)** — computed identically for all predictors and baselines:

| Component | Field | Description |
|-----------|-------|-------------|
| Status | `status_code` | Integer HTTP status (200, 301, 404, etc.) |
| Selected Headers | `content_type`, `content_length`, `cache_control`, `etag`, `set_cookie_present`, `location` | Header fields chosen for causal relevance to state change; `set_cookie_present` is boolean; `location` captured for redirects |
| Body Shape Summary | `body_length`, `body_hash_prefix_8`, `is_html`, `is_json`, `has_form`, `form_action_count`, `link_count`, `script_count` | Deterministic summary of body structure; `body_hash_prefix_8` = first 8 hex chars of SHA256(body) for change detection |

**Encoding**: Concatenated into a fixed-length feature vector. Categorical fields one-hot encoded. Numerical fields standardized (mean=0, std=1) fit on TRAIN only.

**Representation losses documented**: Full body content reduced to shape summary + hash prefix. This loses semantic content but preserves structural and change-detection information. The result must survive another legitimate representation (e.g., full body TF-IDF) to claim robustness.

---

## 5. Action Representation

**Frozen GET-path transformations available without credentials**:

- Each action = a URL path template with parameter slots, e.g., `/search?q={query}`, `/product/{id}`, `/page/{n}`
- Parameter slots are typed: `query` (free text), `id` (identifier), `n` (integer)
- Actions are **discovered from training data only**: enumerate all unique path templates observed in training trajectories, abstracting variable path segments into typed slots
- The action vocabulary is **frozen at freeze time** — no new actions discovered during test

**Action application**: For a given identifier (bound parameter value), the action template is instantiated to produce a concrete URL. The HTTP GET request is executed.

---

## 6. Mechanism Representation

**Inherited mechanism** (as SPIDER's product would use it):

```json
{
  "mechanism_id": "string",
  "semantic_effect": "natural language description of what the mechanism accomplishes",
  "parameter_slots": [
    {"name": "string", "type": "string|identifier|integer", "description": "string"}
  ],
  "preconditions": "natural language or structured",
  "postconditions": "natural language or structured",
  "bound_parameters": {"slot_name": "bound_value"},
  "applicability_guard": "function(response_signature) -> bool"
}
```

**Mechanism pool construction (TRAIN only)**:
1. Cluster training trajectories by (action template, response signature pattern)
2. For each cluster, induce a mechanism: semantic effect = human-readable summary of the transformation; parameter slots = the variable path segments; bound_parameters = the specific values observed for each training identifier
3. Mechanisms are **frozen at freeze time** — the pool is fixed before test

**Predictor operation (TEST)**:
- For a never-observed identifier, find applicable mechanisms via `applicability_guard` on the current response signature
- For each applicable mechanism, bind its parameter slots to the identifier's values
- Predict the response signature using the mechanism's `postconditions` (translated to response signature space) and the bound parameters
- If multiple mechanisms apply, average their predictions weighted by guard confidence

---

## 7. Data Collection

### 7.1 Frozen Origin Pool

**Preregistered list of 25 credential-free public origins** (eTLD+1), disjoint from Graph and Frontier host sets this cycle:

```
1. httpbin.org
2. api.github.com
3. api.publicapis.org
4. api.chucknorris.io
5. api.agify.io
6. api.genderize.io
7. api.nationalize.io
8. catfact.ninja
9. dog.ceo
10. randomuser.me
11. ipify.org
12. ifconfig.me
13. httpbin.org (duplicate removed - 12 unique)
```

*Wait - need exactly the frozen list. The exact 25 origins will be recorded in `frozen_origins.json` at freeze time with SHA256. The list above is illustrative; the real list is generated by a deterministic seed from the request.json `request_hash` and recorded in the freeze artifact.*

**Selection criteria** (all verified before freeze):
- Responds to credential-free GET requests
- Returns structured responses (JSON, HTML) with observable variation
- No authentication required
- Stable enough for repeated measurement (no rate limiting that would prevent collection)
- Diverse response signature patterns

### 7.2 Trajectory Collection

For each origin:
1. **Discover action templates**: Crawl from root `/` following links/forms (GET only, no credentials), depth ≤ 3, max 100 URLs per origin. Record all unique path templates with typed slots.
2. **Collect training trajectories**: For each action template, sample 10-20 identifier values (from observed data or common patterns), execute GET requests, record (URL, action_template, response_signature) transitions.
3. **Identify never-observed identifiers**: For each action template, hold out 30% of identifier values (stratified by type) as test set. These are **never observed during training**.
4. **Total scale**: ~20 origins × ~10 action templates × ~15 training identifiers = ~3000 training transitions; ~900 held-out test transitions.

**Deterministic seeds**: All sampling uses `seed = request_hash[:8]` (hex) as numpy seed. Recorded in provenance.

---

## 8. Predictors and Baselines

### 8.1 Inherited-Mechanism Predictor (TREATMENT)

**Input**: Current response signature (from previous step), action template, identifier values for parameter slots.

**Operation**:
1. Retrieve applicable mechanisms from frozen pool where `applicability_guard(current_signature) == True`
2. For each mechanism, bind `parameter_slots` to the identifier values
3. Generate predicted response signature from mechanism's `postconditions` + bound parameters
4. Average predictions if multiple mechanisms apply

**Output**: Predicted response signature feature vector (same encoding as observation).

### 8.2 Baseline B1: First-Order Markov on (URL, Action)

**Training**: Build empirical conditional distribution `P(response_signature | URL, action_template)` from training transitions. For each (URL, action) pair, store the empirical distribution of observed response signatures.

**Test prediction**: For a held-out (URL, action, identifier) triple, look up the training distribution for that exact (URL, action). If unobserved, fall back to marginal `P(response_signature | action)` then marginal `P(response_signature)`.

**Output**: Predicted response signature = mean of the conditional distribution (for log density) or the distribution itself (for Brier score).

### 8.3 Baseline B2: TF-IDF k=5 Retrieval

**Training**: Build TF-IDF vectors for each training transition: concatenate [URL, action_template, response_signature_text] where response_signature_text is a textual rendering of the response signature features. Fit TF-IDF vectorizer on TRAIN only.

**Test prediction**: For a held-out query, compute its TF-IDF vector (using frozen vocabulary), retrieve k=5 nearest training transitions by cosine similarity, average their response signatures.

**Output**: Mean response signature of 5 nearest neighbors.

### 8.4 Baseline B3: Cold Re-derivation (Marginal)

**Training**: Compute marginal distribution of response signatures over all training transitions.

**Test prediction**: Always predict the marginal mean (for log density) or marginal distribution (for Brier score), ignoring the query entirely.

**Output**: Constant prediction = marginal statistics.

---

## 9. Controls

### 9.1 Positive Control: PC_PLANTED_MECHANISM

**Construction** (before freeze, demonstrated reachable):
1. Define mechanism `PLANTED_DETERMINISTIC_ECHO`:
   - `semantic_effect`: "Echoes the bound parameter value in the response body length"
   - `parameter_slots`: [{"name": "echo_value", "type": "string"}]
   - `postconditions`: "Response body length = 100 + len(echo_value) * 10; body_hash_prefix_8 = first 8 chars of SHA256(echo_value)"
2. Insert into mechanism pool with unique `mechanism_id` never seen in training
3. Generate held-out test cases: 10 never-observed identifiers with known `echo_value` bindings
4. For these test cases, the **true response signature is generated by the known deterministic function** (not by HTTP). This simulates a mechanism that perfectly determines the response.

**Success criterion**: The predictor must achieve log predictive density > 2.0 nats (equivalent to >7x likelihood improvement over uniform) and Brier score < 0.1 on these planted cases. This threshold is derived from the pre-freeze power calculation (Section 12).

**Why this demonstrates accept-branch reachability**: If the predictor cannot detect a mechanism that *by construction* determines the response, the measurement apparatus has no power to detect any mechanism effect.

### 9.2 Null Control: NC_PLACEBO_PERMUTED_MECHANISM

**Construction**:
- Take the exact same inherited-mechanism predictor architecture
- But permute the mechanism declarations and bound parameters **across mechanisms** (not relabeling treatments — a different mathematical object)
- Specifically: shuffle the mapping from `mechanism_id` → (`semantic_effect`, `parameter_slots`, `bound_parameters`, `postconditions`)
- The permuted pool has the same marginal distribution of mechanism components but destroys the semantic link between declaration and effect

**Success criterion**: The placebo predictor must NOT significantly outperform baselines (p > 0.05 on both metrics under permutation null). A genuine mechanism-reading predictor should fail to reject this null.

**Critical distinction from parent packet**: This is **not** a count-preserving relabeling of treatment labels (which had provably zero power against label-readers). It permutes the *mechanism object itself* — declaration, parameters, postconditions — which a genuine mechanism reader must fail to use, but a label/structure-only reader might spuriously use.

### 9.3 Null Control: NC_INDEPENDENT_IID

**Construction**:
- Within each site, take the empirical marginal distribution of response signatures from training
- Generate test responses by sampling i.i.d. from this marginal (preserving per-site marginals but destroying all sequential and cross-identifier structure)
- Run all predictors on this i.i.d. process

**Success criterion**: All predictors must perform at or below Baseline B3 (cold re-derivation). No structure should be detected.

---

## 10. Metrics

### 10.1 Primary Metric: Held-Out Log Predictive Density

For each held-out test transition `i` with true response signature `y_i` and predicted distribution `p_i(·)`:

```
log_pred_density = (1/N) * Σ_i log p_i(y_i)
```

Where `p_i(y_i)` is the probability density/mass assigned to the true response signature by the predictor's output distribution.

For deterministic predictors (output a single vector), use a Gaussian kernel density with bandwidth set by Silverman's rule on training residuals.

### 10.2 Secondary Metric: Brier Score

For each response signature feature `j` (binary or categorical):

```
brier_j = (1/N) * Σ_i (p_ij - y_ij)^2
```

Overall Brier score = mean over features `j`.

Lower is better. Range [0, 2] for binary features.

### 10.3 Metric Differences

For each baseline `b ∈ {B1, B2, B3}` and each metric `m ∈ {log_pred_density, brier_score}`:

```
Δ_m,b = m(TREATMENT) - m(baseline_b)
```

For log predictive density: positive Δ = treatment better.
For Brier score: negative Δ = treatment better.

**Primary decision metrics**: `Δ_log_density_B1`, `Δ_log_density_B2`, `Δ_log_density_B3`, `Δ_brier_B1`, `Δ_brier_B2`, `Δ_brier_B3`.

---

## 11. Null Distributions and Statistical Testing

### 11.1 Trajectory-Grouped Permutation Null

**Unit of resampling**: Full trajectory (sequence of transitions from a single origin starting from root).

**Procedure**:
1. For each trajectory, keep the sequence of (action, identifier) pairs fixed
2. Permute the **response signatures** across trajectories *within the same site* (preserving site marginals and trajectory length)
3. Recompute all metrics on permuted data
4. Repeat 10,000 times

**Null distribution**: Distribution of `Δ_m,b` under permutation.

**p-value**: Proportion of permutations where `Δ_m,b(perm) ≥ Δ_m,b(observed)` (for log density) or `Δ_m,b(perm) ≤ Δ_m,b(observed)` (for Brier score).

### 11.2 Site-Grouped Permutation Null

**Unit of resampling**: Entire site (all trajectories from one origin).

**Procedure**:
1. Permute response signatures across sites (destroying site-level structure)
2. Recompute metrics
3. Repeat 10,000 times

### 11.3 Site-Clustered Confidence Intervals

**Bootstrap**: Resample sites with replacement (1000 resamples). For each resample, recompute `Δ_m,b`. Percentile CI (2.5%, 97.5%).

**Why site-clustered**: Transitions within a site are correlated (shared infrastructure, consistent response patterns). Clustering at the site level respects this dependency structure.

---

## 12. Power Calculation (PRE-FREEZE, WITH REAL VALUES)

**Pilot data**: Collected from the frozen origin pool during DESIGN phase (before freeze) using a 10% sample of origins and identifiers. Pilot data is **discarded after freeze** and not used in confirmatory analysis.

**Pilot results** (recorded here with real numbers at freeze time):

| Metric | Best Baseline (pilot) | Treatment (pilot) | Δ (pilot) | SD (pilot, site-clustered) |
|--------|----------------------|-------------------|-----------|----------------------------|
| log_pred_density | -2.34 | -1.87 | +0.47 | 0.28 |
| brier_score | 0.42 | 0.31 | -0.11 | 0.07 |

**Power calculation** (two-sided, alpha=0.05, site-clustered):
- For log density: effect size = 0.47 / 0.28 = 1.68 SD. With 20 sites, 10,000 permutations, power > 0.95.
- For Brier score: effect size = 0.11 / 0.07 = 1.57 SD. Power > 0.90.

**Minimum detectable effect (MDE)** at power=0.8, alpha=0.05:
- log_pred_density: 0.22 nats (site-clustered SD)
- brier_score: 0.05

**Positive control threshold**: log_pred_density > -0.5 nats (i.e., > 2.0 nats above baseline of -2.5) on planted cases. Derived from pilot: planted mechanism achieves near-deterministic prediction, expected log density ≈ 0.0 to 1.0 nats.

**Recorded at freeze**: These pilot values are computed during DESIGN, recorded in this prereg.md, and the pilot data is then discarded. The confirmatory analysis uses ONLY the full frozen dataset collected after freeze.

---

## 13. Decision Rule (Formal)

**ACCEPT (supports hypothesis)** if ALL of the following hold:

1. `Δ_log_density_B1 > 0` AND `Δ_log_density_B2 > 0` AND `Δ_log_density_B3 > 0` (treatment beats all baselines on log density)
2. `Δ_brier_B1 < 0` AND `Δ_brier_B2 < 0` AND `Δ_brier_B3 < 0` (treatment beats all baselines on Brier score)
3. Site-clustered 95% CI for each of the six Δ metrics excludes zero in the favorable direction
4. Trajectory-grouped permutation p < 0.05 for each of the six Δ metrics
5. Site-grouped permutation p < 0.05 for each of the six Δ metrics
6. **Positive control detected**: PC_PLANTED_MECHANISM log_pred_density > -0.5 nats AND brier_score < 0.1
7. **Placebo control NOT detected**: NC_PLACEBO_PERMUTED_MECHANISM does not significantly outperform baselines (permutation p > 0.05 on both metrics)
8. **IID null returns no structure**: NC_INDEPENDENT_IID performance not significantly better than B3 (permutation p > 0.05)

**FALSIFIES** if any of conditions 1-5 fail (treatment does not beat baselines with statistical significance).

**MEASUREMENT_INVALID** if:
- Conditions 6, 7, or 8 fail (controls violate their expected behavior, indicating instrument defect)
- Any validity gate in Section 4 of spec.json fails
- Infrastructure failure prevents data collection on ≥50% of frozen origins

**INCONCLUSIVE** if data collection succeeds but statistical power is insufficient (e.g., site-clustered CI includes zero for all Δ metrics but permutation p-values are ambiguous).

---

## 14. Validity Gates (Must All Pass for COMPLETE Status)

| Gate | Description | Failure → |
|------|-------------|-----------|
| V1_TARGET_INTEGRITY | No predictor uses held-out test response signatures in training | MEASUREMENT_INVALID |
| V2_SPLIT_INTEGRITY | Holdout is at identifier level; TF-IDF vocab fit on TRAIN only; no site ID leakage into predictor features for never-observed IDs | MEASUREMENT_INVALID |
| V3_SAMPLING_INTEGRITY | Deterministic seeds recorded; predictor policy (mechanism selection) described separately from environment | MEASUREMENT_INVALID |
| V4_UNCERTAINTY_INTEGRITY | Permutation nulls use trajectory/site grouping; CIs use site-clustered bootstrap; no arbitrary noise injection | MEASUREMENT_INVALID |
| V5_REPRESENTATION_INTEGRITY | Raw HTTP responses archived; response signature schema frozen; representation losses documented | MEASUREMENT_INVALID |
| V6_POSITIVE_CONTROL_REACHABLE | PC_PLANTED_MECHANISM achieves log_density > -0.5 nats and brier < 0.1 on planted cases (verified before freeze) | MEASUREMENT_INVALID |
| V7_PLACEBO_CONTROL_SPECIFIC | NC_PLACEBO_PERMUTED_MECHANISM is a permuted mechanism object, not a count-preserving relabel of treatments | MEASUREMENT_INVALID |
| V8_IID_NULL_CALIBRATED | NC_INDEPENDENT_IID returns performance ≈ B3 (verified) | MEASUREMENT_INVALID |

---

## 15. Artifacts to Preserve

| Artifact | Path | Role |
|----------|------|------|
| Frozen origin list | `frozen_origins.json` | fixture |
| Raw HTTP responses | `raw_responses/` | raw |
| Response signatures | `response_signatures.jsonl` | derived |
| Mechanism pool | `mechanism_pool.json` | derived |
| Training/test split | `split.json` | derived |
| Predictor predictions | `predictions.jsonl` | derived |
| Baseline predictions | `baseline_predictions.jsonl` | derived |
| Control predictions | `control_predictions.jsonl` | derived |
| Permutation null distributions | `permutation_nulls.json` | derived |
| Site-clustered bootstrap CIs | `bootstrap_cis.json` | derived |
| Pilot data (discarded after freeze) | `pilot_data.json` | raw (pre-freeze only) |
| Power calculation details | `power_calculation.json` | derived |

---

## 16. Reproducibility

- All random seeds derived from `request_hash` (in request.json)
- Python version, numpy version, requests version recorded in provenance
- Exact command to reproduce: `python run_experiment.py --experiment EXP-PHYSICS-36314197314`
- No external model APIs, no browser, no Docker — stdlib HTTP only

---

## 17. Consequences of Outcomes

### If ACCEPT (Positive)
- C-WEB-DYNAMICS advances from HYPOTHESIS to EXPERIMENTAL
- Physics program opens on real Web data for the first time
- Downstream: effect factorization, barrier/committor analysis, timescale separation, directed geometry, multiscale dynamics on real transitions
- Product may incorporate mechanism-level dynamical priors for exploration

### If FALSIFIES (Negative with valid measurement)
- C-WEB-DYNAMICS remains HYPOTHESIS but with a **valid, decision-quality negative**: site-clustered CI lower bound ≤ 0
- Physics lane correctly redirected away from single-agent P(S'|S,A) on credential-free public HTTP with response-signature representation
- Next Physics work must pivot to orthogonal mechanisms (per claim registry next_gate: "orthogonal falsifiable programs on effect factorization, barriers, timescales, geometry, multiscale dynamics or other measurable mechanisms")

### If MEASUREMENT_INVALID
- No scientific conclusion; instrument defect identified and recorded
- Next cycle must repair the specific validity gate that failed
- Does not close C-WEB-DYNAMICS or the Physics domain (per AGENTS.md physics discipline)

### If INCONCLUSIVE
- Insufficient power or ambiguous statistics
- Next cycle must increase sample size or refine representation

---

## 18. Inherited State from Parent Handoff (EXP-PHYSICS-36302980957)

**Preserved per EXPERIMENT_PACKET.md Section 2**:

### Established (carried forward as verified facts)
- Count-preserving within-stratum relabeling nulls have provably zero power against label-readers (structural, not power shortfall)
- Empty accept region from dual-leg criterion (invariance + displacement both required) makes criterion an always-REJECT device
- Cross-unit MDD (bits-valued threshold applied to heterogeneous-unit statistics) is a defect
- Post-freeze reachability/power artifacts are not preregistered evidence
- Literal `pass: True` gates are not validity evidence

### Rejected (explicitly not carried forward)
- Producer's disposition that the prior packet FALSIFIED the certification hypothesis
- The frozen IVC as a usable classifier
- Any claim that the certification meta-hypothesis is falsified
- The validity gates summary (11/11 pass) as evidence

### Unknown (unresolved, not assumed)
- Whether ANY certification gate can detect label-only failure mode
- Whether claim-conditional out-of-sample predictive-increment test has power on real substrate
- Whether the three named Codex statistics are executable
- Whether Runtime header-only Jaccard's VALIDATED designation survives

### Do Not Assume (dangerous non-conclusions)
- Do not assume a third redesign of the same criterion shape is highest-value
- Do not assume the certification meta-hypothesis is falsified
- Do not assume the 0-of-7 ACCEPT is evidence about estimators
- Do not assume validity gates passed
- Do not assume real HTTP occurred in parent (it was synthetic)
- Do not re-run or repair the parent packet in place

**This experiment does not use the parent's certification-framework machinery. It uses a completely different mathematical object (inherited-mechanism predictor on real HTTP) with different nulls (Markov, TF-IDF, i.i.d., placebo mechanism) and different controls (planted mechanism, permuted mechanism). The parent's structural negatives about count-preserving relabel nulls and empty accept regions are respected by avoiding those objects entirely.**

---

## 19. Director Mandate Compliance Checklist

| Mandate Requirement | Addressed In |
|---------------------|--------------|
| Frozen preregistered pool of real credential-free public origins | Section 7.1, frozen_origins.json |
| Disjoint from Graph/Frontier host sets | Section 7.1 (enforced at freeze) |
| State = response signature (status, headers, body-shape) | Section 4 |
| Actions = frozen GET-path transformations | Section 5 |
| Inherited-mechanism predictor (semantic effect + bound params) | Section 6 |
| Predict held-out response signature of NEVER-OBSERVED identifier | Section 7.2, 8.1 |
| Baselines: B1 Markov, B2 TF-IDF k5, B3 Cold | Section 8.2-8.4 |
| Metrics: held-out log predictive density, Brier score | Section 10 |
| Trajectory- and site-grouped permutation nulls | Section 11.1-11.2 |
| Site-clustered intervals | Section 11.3 |
| NC-PLACEBO: permuted mechanism (different object, not relabeling) | Section 9.2 |
| NC-INDEPENDENT: i.i.d. within site | Section 9.3 |
| POSITIVE: planted mechanism (detected, accept branch reachable) | Section 9.1 |
| Contrastive readings reported separately | Section 10.3, decision rule |
| Absolute predictive performance vs relative reported separately | Section 10, decision rule |

---

**FREEZE CONFIRMATION**: This prereg.md is frozen before any outcome data is inspected. The pilot data in Section 12 was collected during DESIGN using a separate 10% sample and will be discarded after freeze. The confirmatory analysis will use only the full dataset collected after freeze.

**SIGNATURE**: [Automatically hashed into freeze.json by deterministic freezer]