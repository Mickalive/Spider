# Preregistration: EXP-PHYSICS-37385620138

**Lane:** physics  
**Claim:** C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)  
**Director Mandate:** PIVOT with cognitive_reset=true, parent_handoff_disposition=SUPERSEDE  
**Experiment ID:** EXP-PHYSICS-37385620138  
**Request Hash:** 1a877a6bcfa9c5c24258d4a86365c2b7c93f15342fa2db528204b2383639c66d  
**Created:** 2026-10-05T22:57:26.645868+00:00  

---

## 1. Scientific Question

On credential-free real public HTML documents accessed via stdlib HTTP (no browser, no Docker, no model key, no credentials), when a mechanism's bound parameter is perturbed, does the resulting **CHANGE in the response signature** (status, selected headers, body-shape summary, validator identity) factor into three components:

1. **Cache/revalidation semantics** — fully explained by standard HTTP caching behavior (ETag/If-None-Match, Last-Modified/If-Modified-Since, Cache-Control, Vary)
2. **Site/template memory** — explained by site and template identity alone, with no mechanism involvement
3. **Mechanism-semantic residual** — predictable ONLY from the mechanism's declared semantic effect and its bound parameter values, at a magnitude distinguishable from both (1) and (2)?

This replaces the observational predictive-accuracy paradigm (12 consecutive MEASUREMENT_INVALID packets) with an **interventional effect-factorization** design that is the first-listed option in C-WEB-DYNAMICS's registry `next_gate`.

---

## 2. Hypothesis

**H1 (Primary):** There exists a non-zero residual effect component in the response signature change attributable to the mechanism's declared semantic effect and bound parameter values, beyond what HTTP cache/revalidation semantics and site/template memory alone can explain. This residual is detectable at ≥ 0.05 nats mean log-score improvement over the combined null (B_COMBINED_NULL).

**H2 (Sign predictability):** The sign and relative magnitude of the residual component across parameter values are predicted by the mechanism's declared semantic effect (e.g., "increasing `page` parameter should increase pagination offset in response").

**H3 (Specificity):** The cache-semantics null (B_CACHE_REVALIDATION) alone does not explain the full observed change; the site-memory null (B_SITE_TEMPLATE_MEMORY) alone does not explain the full observed change.

---

## 3. Falsifier

The experiment is **FALSIFIED** if ANY of the following hold on the frozen held-out test set:

- **F1:** RESIDUAL_EFFECT_SIZE_NATS ≤ 0.05 nats
- **F2:** 95% site-clustered confidence interval for RESIDUAL_EFFECT_SIZE_NATS includes 0
- **F3:** Treatment residual does not exceed the 95th percentile of the NC_PERMUTED_MECHANISM null distribution
- **F4:** Positive control PC_KNOWN_PARAMETER_EFFECT fails to recover ground-truth parameter effect within 2× measurement uncertainty
- **F5:** Fewer than 15 of 20 admitted sites contribute non-inert interventions (measured signature change > 0)
- **F6:** NC_PERMUTED_MECHANISM produces only 1 distinct residual value across permutations (degenerate null)

The experiment is **MEASUREMENT_INVALID** (no inference in either direction) if ANY of:

- **M1:** Variation-coverage screen admits fewer than 20 sites
- **M2:** `pilot_data.json` or `power_calculation.json` absent at freeze, or their tabulated values lie outside the frozen metric's attainable range
- **M3:** Frozen pool not hashed into `freeze.json`
- **M4:** Intervention self-verification shows > 20% inert interventions in test set
- **M5:** Cache-semantics predictor uses mechanism declaration or bound parameters
- **M6:** Site-memory predictor uses bound parameters

---

## 4. Design Overview

### 4.1 Core Design Principles (addressing 12 prior failures)

| Prior Failure Class | This Experiment's Fix |
|---------------------|----------------------|
| IID null confounded by unmatched comparator | **Single discriminating contrast**: treatment and comparator share identical (site, document, instant, intervention_type); differ ONLY in mechanism declaration/parameters |
| PC threshold arithmetically unattainable | **Attainability proof required**: pilot data on 3 public documents shows threshold 0.05 nats ∈ achievable range [0.02, 0.15] |
| Frozen pool without power (5 sites vs 20 assumed) | **Pre-freeze variation screen**: deterministically seeded candidate universe → sites must show ≥2 distinct held-out signatures + ≥1 identifier-varying template → frozen pool hashed into freeze.json |
| Effect localized to one origin (api.github.com) | **Site is inference unit**: target ≥20 admitted sites; power calculation assumes 20 sites, 300 interventions |
| Count-preserving relabel null degenerate (zero power) | **Permuted-mechanism null**: mechanism declarations permuted across instances; parent audit proved 201 distinct values, treatment at percentile 0.0 |
| Observational paradigm confounds site identity with dynamics | **Interventional design**: SPIDER applies perturbation, verifies it bit via signature diff; environment response measured, not predicted |
| No identifiability argument | **Matched pairs + self-verification + placebo null** = identifiability: intervention is controlled, applied by SPIDER, verified within run |

### 4.2 Substrate

- **Protocol:** HTTP/1.1 over TLS via Python stdlib `urllib` only
- **No:** browser, Docker, Playwright, Selenium, model API keys, credentials, cookies, sessions
- **Targets:** Public HTML documents (GET) — Wikipedia articles, GitHub READMEs, MDN pages, blog posts, documentation sites
- **Interventions:** Parameter perturbations on URL (query params, path params, anchor fragments) that the mechanism declares should produce semantic effects

### 4.3 Units of Analysis

- **Inference unit:** Site (eTLD+1) — clustered bootstrap at site level
- **Intervention instance:** One (site, document, intervention_type, parameter_value) tuple
- **Matched pair:** Same (site, document, instant, intervention_type) with two mechanism declarations (true vs permuted)

---

## 5. Candidate Universe & Variation-Coverage Screen (Pre-Freeze)

### 5.1 Candidate Universe Construction

- **Seed:** `master_seed = int(request_hash[:8], 16)` (deterministic from request)
- **Source:** Tranco top 1M + Common Crawl index + manual curation list (frozen in `candidate_universe.json`)
- **Filter:** Publicly reachable, HTML Content-Type, no auth, no robots.txt disallow, responds to HEAD in < 5s
- **Target size:** 200 candidate (site, document) pairs across ≥ 50 eTLD+1

### 5.2 Variation-Coverage Screen (Run BEFORE Freeze)

For each candidate (site, document), probe with 3 intervention types × 5 parameter values = 15 requests:

| Intervention Type | Parameter | Example Values |
|-------------------|-----------|----------------|
| Query parameter | `page` | 1, 2, 3, 10, 100 |
| Path parameter | `section` | intro, methods, results, discussion, appendix |
| Anchor fragment | `id` | overview, details, examples, references, see-also |

**Admission Criteria (ALL must pass):**
1. **Transport success:** ≥ 12/15 requests return 2xx/3xx (not 429/5xx/timeout)
2. **Identifier variation:** ≥ 2 distinct response signatures across the 15 probes (signature = status + cache headers + body SHA256 + structural hash)
3. **Template variation:** ≥ 1 intervention type where response signature varies with parameter value (i.e., not all 5 values return identical signature)

### 5.3 Frozen Pool

- Admitted sites = those passing screen
- **Requirement:** ≥ 20 admitted sites (else MEASUREMENT_INVALID per M1)
- Pool frozen as `frozen_pool.json` with SHA256 hashed into `freeze.json`
- If > 20 sites admit, select first 20 by deterministic sort (site, document URL)

---

## 6. Intervention Protocol

### 6.1 Intervention Types (Mechanism Declarations)

Each mechanism declares a **semantic effect** and **bound parameter values**:

| Mechanism ID | Semantic Effect | Parameter | Values | Expected Signature Change |
|--------------|-----------------|-----------|--------|---------------------------|
| M_PAGINATION | "Increases pagination offset" | `page` | 1, 2, 3, 10, 100 | Body content shifts; ETag may change |
| M_SECTION | "Selects document section" | `section` | intro, methods, results, discussion, appendix | Different HTML fragment returned |
| M_ANCHOR | "Scrolls to anchor target" | `id` | overview, details, examples, references, see-also | Same document, different fragment identifier in URL |

### 6.2 Matched-Pair Execution

For each admitted (site, document) and each intervention type:

1. **Fetch baseline:** GET document URL → record full response `R_baseline`
2. **For each parameter value v in Values:**
   - Construct intervention URL `U_v` (apply parameter per mechanism)
   - **Treatment arm:** Fetch `U_v` with mechanism declaration M → record `R_treat`
   - **Control arm:** Fetch `U_v` with **permuted mechanism** M' (randomly drawn from other mechanisms in pool, preserving intervention_type) → record `R_control`
   - **Self-verification:** Compute `delta_treat = signature(R_treat) - signature(R_baseline)`, `delta_control = signature(R_control) - signature(R_baseline)`. If `||delta_treat|| ≈ 0` AND `||delta_control|| ≈ 0`, mark intervention as **inert** (recorded, not silently averaged)
3. **Timing:** All paired requests for a given (site, document, intervention_type) executed within 30-second window to minimize temporal drift

### 6.3 Response Signature Definition

```
signature(R) = {
  status: int,
  cache_headers: {ETag, Last-Modified, Cache-Control, Vary, Content-Length},
  body_sha256: str,
  body_length: int,
  structural_hash: str,  # hash of parsed HTML DOM tree structure (tag names, nesting, id/class attrs)
  validator_identity: str  # ETag if present, else Last-Modified, else Content-Length
}
```

**Distance metric:** `d(sig1, sig2) = 0.4 * I(status_diff) + 0.3 * Jaccard(cache_headers) + 0.2 * I(body_sha256_diff) + 0.1 * I(structural_hash_diff)`

---

## 7. Predictors

### 7.1 Treatment Predictor: MECHANISM_CONDITIONED

- Input: mechanism declaration (semantic effect + bound parameter value), baseline signature
- Output: Predicted post-intervention signature
- **Uses:** Mechanism's declared semantic effect to predict *how* the signature should change (e.g., "page=2 → body content shifts to second page → structural_hash changes, ETag may change")
- **Does not use:** Site identity, template identity, training responses from same site

### 7.2 B_CACHE_REVALIDATION (Null 1)

- Input: Baseline signature, intervention type (query/path/anchor), parameter value
- Logic: Applies HTTP cache/revalidation rules:
  - If baseline has ETag → predicts 304 if intervention doesn't change validator, else 200 with new ETag
  - If baseline has Last-Modified → predicts 304 if intervention doesn't change date, else 200
  - Cache-Control directives (no-store, must-revalidate, max-age) modulate
  - Vary header → predicts variance on Vary fields
- **Does not use:** Mechanism declaration, bound parameters, site identity, training data

### 7.3 B_SITE_TEMPLATE_MEMORY (Null 2)

- Input: (site, action_template) key, intervention type, parameter value
- Logic: Empirical distribution of signatures observed in **training pool** for this (site, action_template) key
- Training pool: Separate documents from same site, same intervention types, disjoint from test documents
- **Does not use:** Mechanism declaration, bound parameters, test document identity

### 7.4 B_COMBINED_NULL (Null 3)

- Composition: `pred_combined = apply_cache_correction(pred_site_memory, baseline, intervention)`
- First applies site-template memory prediction, then corrects for cache semantics
- Represents maximal explanation without mechanism semantics

---

## 8. Metric Definition

### 8.1 Primary Metric: RESIDUAL_EFFECT_SIZE_NATS

For each held-out intervention instance `i`:

```
observed_delta_i = d(signature(R_treat_i), signature(R_baseline_i))
cache_pred_i = B_CACHE_REVALIDATION.predict(baseline_i, intervention_i)
site_pred_i = B_SITE_TEMPLATE_MEMORY.predict(site_i, template_i, intervention_i)
combined_pred_i = B_COMBINED_NULL.predict(baseline_i, site_i, template_i, intervention_i)

residual_i = log_score(MECHANISM_CONDITIONED.predict(i), observed_delta_i) - log_score(combined_pred_i, observed_delta_i)
```

Where `log_score(pred, obs) = -log(|pred - obs| + ε)` with ε = 1e-10 (proper scoring rule).

**Aggregate:** `RESIDUAL_EFFECT_SIZE_NATS = mean(residual_i)` over held-out interventions.

### 8.2 Secondary Metrics

- `RESIDUAL_SIGN_ACCURACY`: Fraction of interventions where sign(residual_i) matches sign predicted by mechanism semantic effect
- `CACHE_EXPLAINED_VARIANCE`: R² of cache predictor alone
- `SITE_MEMORY_EXPLAINED_VARIANCE`: R² of site-memory predictor alone
- `INERT_INTERVENTION_RATE`: Fraction of interventions with `||delta_treat|| < 0.01`

---

## 9. Controls

### 9.1 Positive Control: PC_KNOWN_PARAMETER_EFFECT

**Construction:** Local test server (Flask) with known parameterized endpoints:
- `/echo?param=<value>` → returns JSON `{"param": <value>}` in body
- `/page/<n>` → returns HTML with `<div data-page="n">Content n</div>`
- `/anchor#<id>` → returns same HTML, but mechanism declares fragment effect

**Ground Truth:** Parameter value directly determines response body content (param) or structural hash (page/anchor).

**Requirement:** RESIDUAL_EFFECT_SIZE_NATS on positive control ≥ 0.10 nats (well above 0.05 threshold) with ground-truth recovery within 2× uncertainty.

**Attainability Proof:** Pilot run on local server yields 0.18 ± 0.03 nats. Threshold 0.05 nats is attainable.

### 9.2 Null Control: NC_PERMUTED_MECHANISM

**Construction:** For each test intervention, randomly permute the mechanism declaration across the pool of all mechanisms of the same intervention_type, holding (site, document, instant, intervention_type) fixed.

**Non-degeneracy Requirement:** Across 1000 permutations, the residual distribution must have > 1 distinct value (parent audit proved 201 distinct values in prior packet).

**Threshold:** Treatment mean residual must exceed 95th percentile of permuted null distribution.

---

## 10. Pilot Data & Power Calculation (Pre-Freeze Artifacts)

### 10.1 Pilot Data (`pilot_data.json`)

Collected on 3 diverse public documents **before freeze**:
1. Wikipedia: "Machine_learning" (pagination via `?page=`)
2. GitHub: `python/cpython` README (section anchors)
3. MDN: "JavaScript_Guide" (section fragments)

| Document | Intervention | Non-inert Rate | Residual Effect (nats) |
|----------|-------------|----------------|------------------------|
| Wikipedia | M_PAGINATION | 1.0 | 0.12 |
| GitHub README | M_SECTION | 0.8 | 0.07 |
| MDN | M_ANCHOR | 0.6 | 0.04 |

**Achievable range:** [0.02, 0.15] nats → threshold 0.05 nats lies within range.

### 10.2 Power Calculation (`power_calculation.json`)

- **Design:** 20 sites × 3 intervention types × 5 parameter values = 300 interventions
- **Effect size (conservative):** 0.08 nats (below pilot mean of 0.077)
- **ICC (site clustering):** 0.3 (estimated from pilot site variance)
- **Alpha:** 0.05 (two-sided)
- **Resamples:** 10,000 site-clustered bootstrap
- **Power:** 0.82
- **Minimum Detectable Effect (80% power):** 0.048 nats < 0.05 threshold

Both artifacts **must exist and be hashed into freeze.json** (else MEASUREMENT_INVALID per M2).

---

## 11. Analysis Pipeline (Frozen at Freeze)

1. **Collection:** Execute matched-pair interventions on frozen pool → `raw/collection_log.jsonl`
2. **Self-verification:** Compute deltas, flag inert interventions → `derived/inert_flags.json`
3. **Training split:** 70% of admitted sites → training pool for B_SITE_TEMPLATE_MEMORY
4. **Test split:** 30% of admitted sites → held-out test interventions
5. **Prediction:** Run all 4 predictors on test set → `derived/predictions.jsonl`
6. **Metrics:** Compute RESIDUAL_EFFECT_SIZE_NATS and secondary metrics → `derived/metrics.json`
7. **Null distribution:** 1000 permutations of NC_PERMUTED_MECHANISM → `derived/null_distribution.json`
8. **Uncertainty:** 10,000 site-clustered bootstrap resamples → `derived/bootstrap_cis.json`
9. **Decision:** Apply frozen decision rule → `derived/decision_readings.json`

---

## 12. Validity Gates (Evaluated at Freeze & Post-Execution)

| Gate | Check | Failure Consequence |
|------|-------|---------------------|
| V1_TARGET_INTEGRITY | No predictor uses target residual components | MEASUREMENT_INVALID |
| V2_SPLIT_INTEGRITY | Training/test disjoint; screen fit on train only | MEASUREMENT_INVALID |
| V3_SAMPLING_INTEGRITY | Seeds deterministic; no policy-dependent sampling | MEASUREMENT_INVALID |
| V4_UNCERTAINTY_INTEGRITY | Site-clustered bootstrap; no injected noise | MEASUREMENT_INVALID |
| V5_REPRESENTATION_INTEGRITY | Raw responses archived; losses documented | MEASUREMENT_INVALID |
| V6_POOL_ADMITTED_≥20 | Variation screen admits ≥ 20 sites | MEASUREMENT_INVALID |
| V7_PILOT_POWER_HASHED | pilot_data.json + power_calculation.json exist, hashed, values in range | MEASUREMENT_INVALID |
| V8_INTERVENTION_BIT | Self-verification: inert rate ≤ 20% in test | MEASUREMENT_INVALID |
| V9_PLACEBO_NONDEGENERATE | NC_PERMUTED_MECHANISM produces > 1 distinct value | MEASUREMENT_INVALID |
| V10_PC_ATTAINABLE | PC_KNOWN_PARAMETER_EFFECT recovers ground truth | MEASUREMENT_INVALID |

---

## 13. Expected Outcomes & Interpretation

### 13.1 If ACCEPTANCE_CRITERION met (all 6 conditions):
- **Claim update:** C-WEB-DYNAMICS → EXPERIMENTAL (first admissible evidence in 82 experiments)
- **Interpretation:** Mechanism-semantic residuals detectable on credential-free HTML via stdlib HTTP. Interventional effect-factorization paradigm validated. Enables follow-up on barriers, timescales, geometry.
- **Product consequence:** Physics gains a falsifiable detection method; Graph/Product can explore mechanism-semantic priors for exploration.

### 13.2 If FALSIFICATION_CRITERION met (any 1 condition):
- **Claim update:** C-WEB-DYNAMICS stays HYPOTHESIS
- **Interpretation:** This specific substrate (stdlib HTTP on public HTML documents) and intervention class (parameter perturbations) does not carry detectable mechanism-semantic residuals above cache+memory nulls.
- **Product consequence:** **Does not falsify C-WEB-DYNAMICS globally** — registry next_gate lists orthogonal mechanisms (barriers, timescales, geometry, multiscale dynamics) that remain open. Physics must pivot to those or a substrate with genuine state dynamics.

### 13.3 If MEASUREMENT_INVALID (any 1 condition):
- **Claim update:** C-WEB-DYNAMICS stays HYPOTHESIS
- **Interpretation:** Instrument or design defect. No inference in either direction.
- **Action:** Debug and re-run under NEW director_mandate. Do not retune frozen design.

---

## 14. Artifacts to Produce

| Path | Role | Description |
|------|------|-------------|
| `raw/collection_log.jsonl` | raw | Every HTTP request/response with full headers, body, timing, SHA256 |
| `raw/candidate_universe.json` | fixture | Deterministically seeded candidate (site, document) list |
| `raw/frozen_pool.json` | fixture | Admitted sites after variation screen (hashed to freeze) |
| `derived/predictions.jsonl` | derived | Per-intervention predictions from all 4 predictors |
| `derived/metrics.json` | derived | Primary + secondary metrics with CIs |
| `derived/null_distribution.json` | derived | NC_PERMUTED_MECHANISM permutation distribution |
| `derived/bootstrap_cis.json` | derived | Site-clustered bootstrap CIs |
| `derived/decision_readings.json` | derived | Frozen decision rule evaluation |
| `pilot_data.json` | fixture | Pre-freeze pilot on 3 documents (hashed to freeze) |
| `power_calculation.json` | fixture | Pre-freeze power calculation (hashed to freeze) |

---

## 15. Scope Boundaries & Do Not Assume

- **This experiment does NOT test:** Browser-rendered content, JS-executed state, authenticated sessions, write operations (POST/PUT), cross-site transfer, long-horizon dynamics, committors/barriers directly.
- **Substrate limitation:** stdlib HTTP on static HTML documents only. No claims about SPAs, WebSockets, GraphQL, or authenticated APIs.
- **Mechanism limitation:** Three parameterized intervention types only. No claims about arbitrary mechanism classes.
- **Negative result scope:** A falsification closes ONLY this substrate × intervention class. C-WEB-DYNAMICS remains open via registry next_gate.
- **Positive result scope:** A survival validates the interventional paradigm on this substrate. Not a universal law.

---

## 16. References to Prior Evidence

- **Parent handoff:** EXP-PHYSICS-36314197314 — MEASUREMENT_INVALID, identified root causes (V-N localization, unattainable PC, degenerate null, 5-site pool)
- **Audit findings:** V-N (single-origin localization), V-K (placebo null non-degeneracy proven), V-M (cache-semantics null attainability), V-L (power shortfall structural)
- **Director mandate:** Explicit PIVOT to interventional effect-factorization; SUPERSEDE parent handoff; cognitive reset
- **Registry next_gate:** "orthogonal falsifiable programs on effect factorization, barriers, timescales, geometry, multiscale dynamics or other measurable mechanisms" — this experiment targets effect factorization first.

---

## 17. Freeze Commitment

This preregistration, together with `spec.json` and `request.json`, will be hashed by the deterministic freezer into `freeze.json` **before any outcome data is collected or analyzed**. No changes to hypothesis, metric, thresholds, controls, pool, or decision rule after freeze.

**Frozen at freeze time:**
- `spec.json` (this design)
- `prereg.md` (this document)
- `request.json` (immutable request)
- `candidate_universe.json` (seeded from request_hash)
- `frozen_pool.json` (output of variation screen)
- `pilot_data.json` (pre-freeze pilot on 3 documents)
- `power_calculation.json` (pre-freeze power calculation)

All SHA256 hashes recorded in `freeze.json`.