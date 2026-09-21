# Preregistration: EXP-INTEL-35572177756

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35572177756
- **Lane**: intel
- **Claim IDs**: C-MEAS-VALID
- **Parent**: EXP-INTEL-35551517470 (handoff sha256: ce6224a979be8a76f57b2d20931c09611135007c533b518c258648f929bf2d27)
- **Date**: 2026-09-21

## Inherited State (from parent handoff)

### Established
- Sample-size effect on ranking agreement is REAL and MONOTONIC: canonical recipe agreement improves from 0% at n=5/10 to 50% at n=15 to 56.5% at n=20 (Spearman=1.0)
- Ranking agreement PLATEAUS below 80% at maximum available sample size: canonical 56.5% at n=20, per-task 78.0% at n=20
- Under template invariance, ranking agreement equals proportion(margin_i>0) exactly: this is a structural identity, not a predictive model
- Step-function structure of proportion(margin>0): (0, 0, 0.50, 0.57) at n=5/10/15/20 with 7.6x growth deceleration
- margin_std (~1e-4 to 6e-4) is the empirically correct noise scale for ranking flips
- Template invariance persists on truncated-first-20 subsample
- OECD/COINr pipeline preserves between-type discrimination (max eta2 0.999645 at n=20)
- Per-task recipe achieves 78.65% ranking agreement at n=20 vs canonical 55.95%

### Rejected
- ALL six model-based extrapolation approaches (Phi(mean/SNR_i), Phi(mean/std), Phi(median/std), sign-fraction power law, empirical CDF linear extrapolation, bounded saturating functions) — REJECTED: none produced validated extrapolation
- Ranking instability is PURELY a sample-size artifact within truncated-first-20 range — REJECTED: plateaus at 56% at n=20
- OECD/COINr pipeline structure itself destroys between-type variance — REJECTED
- Recipe-based density is safe for Product Core promotion — REJECTED

### Unknown
- Does ranking stabilize at full DOM (n=21-82)?
- Whether Docker image am1n3e/webarena-verified-shopping:latest becomes available
- Does per-task recipe achieve >= 80% at full DOM?
- Cross-site generalization of the sample-size effect
- Whether bootstrap CIs or permutation tests could provide bounded uncertainty

### Do Not Assume
- That the logistic F50=0.5654 prediction is evidence for structural plateau — it is informationally identical to constant null
- That R2=1.0 for logistic/Hill indicates validated predictive model — reflects structural interpolation
- That the frozen C1/C2/C3 PASS constitutes scientifically meaningful result — gates mis-calibrated for N=4 k=3
- That n=20 result generalizes to full DOM n=21-82
- That the SURVIVES verdict per frozen gates is scientifically meaningful

## Question

Can the Docker image am1n3e/webarena-verified-shopping:latest be made available to re-collect full-DOM locatable_sample for the 7 existing Magento tasks, enabling the frozen ranking-agreement analysis to be completed — and if so, does canonical recipe ranking agreement cross the 80% threshold at full DOM?

## Hypothesis

The ranking instability at truncated-first-20 (canonical recipe agreement 55.95%) is a truncation artifact. Full DOM samples contain richer element diversity with more discriminative elements per definition, enabling canonical recipe sampling to capture a more representative subset.

Specifically:
- H1: Canonical recipe ranking agreement for tag_entropy x DEF-FULL-MAP >= 80% on full DOM (n=21-82 per task)
- H2: Full-DOM agreement exceeds truncated-first-20 agreement (55.95%) by >= 10 percentage points
- H3: Per-task recipe ranking agreement >= 85% at full DOM

## Falsifier

The hypothesis is falsified if ANY of:
- F1: Canonical recipe agreement on full DOM < 75%
- F2: Full-DOM agreement does NOT exceed truncated-first-20 by >= 5pp
- F3: Per-task recipe agreement on full DOM < 75%
- F4: Pipeline eta2 on full DOM drops below 0.90

## Baselines

| ID | Description | Source |
|----|-------------|--------|
| B1 | Canonical recipe agreement at truncated-first-20: 55.95% | EXP-INTEL-35476271877 snr data |
| B2 | Per-task recipe agreement at truncated-first-20: 78.65% | EXP-INTEL-35445596324 M5 |
| B3 | Non-recipe ranking agreement: 100% (listing > detail preserved) | EXP-INTEL-35462974425 analysis |
| B4 | Pipeline eta2 at truncated-first-20: 0.9996 | EXP-INTEL-35445596324 M3 |

## Controls

### Positive Control: PC1_RAW_FEATURE_REPRODUCES_FULL_DOM
- Direct features (tag_entropy, form_fraction, total_area) achieve eta2 >= 0.99 on page_type with full DOM locatable_sample
- Confirms raw features retain perfect discrimination with larger element set

### Null Control: NC1_HIERARCHY_NORMALIZED_FULL_DOM
- Normalized hierarchy density: eta2 < 0.01 on page_type with full DOM
- Reproduces y-proxy degeneracy anchor

## Experimental Protocol

### Phase 1: Docker Availability Check
1. Attempt `docker pull am1n3e/webarena-verified-shopping:latest`
2. Record: pull success/failure, image size, digest, exact error message
3. If pull succeeds, start container: `docker run -d -p 8080:80 am1n3e/webarena-verified-shopping:latest`
4. Health check: HTTP GET localhost:8080, record status code and response time
5. If container starts, wait 30s for Magento initialization, re-check health

### Phase 2: Full-DOM Data Collection (if Docker available)
1. Use the exp347 collection script or equivalent Playwright automation
2. For each of the 7 tasks (3 listing, 3 detail, 1 cart):
   - Navigate to the task URL
   - Wait for full page load
   - Extract ALL elements with bbox into locatable_sample (NOT truncated-first-20)
   - Verify locatable_sample length matches locatable_elements metadata
   - Record: task_id, url, page_type, locatable_sample (full), locatable_elements, elements_with_bbox
3. Save full-DOM data as JSON with same structure as exp347_raw_results.json

### Phase 3: Analysis (if full-DOM data collected)
1. Run frozen analyze.py (EXP-INTEL-35462974425/analyze.py) on full-DOM data
2. Evaluate frozen decision_rule C1-C7 from EXP-INTEL-35462974425/spec.json
3. Report: M1 (full-DOM canonical agreement), M2 (full-DOM per-task agreement), M3 (delta vs truncated), M4 (bootstrap CI), M5 (pipeline eta2)

### Phase 4: Fallback Bootstrap Analysis (if Docker unavailable)
Using per-iteration margin data from EXP-INTEL-35476271877/snr_per_iteration_tag_entropy.json.gz:

1. **Sign test**: One-sample test of H0: p(positive margin) = 0.5 at n=15 and n=20
   - At n=20: observed proportion = 0.5654, n = 10000 iterations
   - Compute exact binomial p-value for two-sided test

2. **Bootstrap CI for proportion**: B=10000 bootstrap resamples of iterations
   - Compute 95% and 99% CI for p(positive margin) at each n
   - Check whether 80% is within the 99% CI upper bound at n=20

3. **Extrapolation analysis**:
   - Fit logistic function p(n) = L / (1 + exp(-k*(n-n0))) on 4 observed proportions: (5,0), (10,0), (15,0.4996), (20,0.5654)
   - Compute predicted agreement at n=50 and n=82
   - Bootstrap uncertainty: resample from per-iteration data, refit logistic, compute prediction intervals
   - Report: predicted agreement at n=50 and n=82 with 95% PI

4. **Decision criteria for Docker-unavailable path**:
   - C8: Bootstrap 99% CI upper bound for p(positive margin) at n=20 < 0.80
   - C9: Logistic extrapolation predicted agreement at n=82 < 80% with 95% PI upper bound < 85%
   - If both C8 and C9: FALSIFIES (ranking agreement does not cross 80% at full DOM)
   - If either fails: MIXED (extrapolation uncertain, Docker required)

## Metric Definitions

| Metric | Definition | Unit |
|--------|-----------|------|
| M1_full_dom_canonical_agreement | Canonical recipe ranking agreement for tag_entropy x DEF-FULL-MAP on full DOM | proportion (0-1) |
| M2_full_dom_pertask_agreement | Per-task recipe ranking agreement for tag_entropy x DEF-FULL-MAP on full DOM | proportion (0-1) |
| M3_full_dom_delta_vs_truncated | M1 - 0.5595 (truncated-first-20 agreement) | percentage points |
| M4_full_dom_bootstrap_ci | Bootstrap 95% CI for M1 | [lower, upper] |
| M5_full_dom_pipeline_eta2 | Pipeline eta2 for tag_entropy x DEF-FULL-MAP on full DOM | proportion (0-1) |
| M6_sign_test_pvalue_n20 | Two-sided binomial p-value for H0: p(positive margin) = 0.5 at n=20 | p-value |
| M7_bootstrap_ci_proportion_n20 | Bootstrap 95% CI for p(positive margin) at n=20 | [lower, upper] |
| M8_logistic_extrapolation_n82 | Logistic-predicted agreement at n=82 | proportion (0-1) |
| M9_logistic_pi_upper_n82 | Upper 95% prediction interval for logistic extrapolation at n=82 | proportion (0-1) |

## Decision Rule

Conjunctive:

- If Docker available AND full-DOM data collected: follow frozen EXP-INTEL-35462974425 verdict rules
- If Docker unavailable: apply bootstrap/extrapolation decision criteria (C8, C9)
- Document exact Docker availability status regardless of outcome

## Product Consequences

**Positive (Docker available, C5 AND C6 PASS)**: Recipe density viable for MIXED handling. Product lane can use tag_entropy-weighted density with canonical recipe.

**Positive (Docker unavailable, C8 AND C9 PASS)**: Recipe density path falsified by extrapolation. Product lane closes recipe density permanently, uses non-recipe density only.

**Negative (Docker available, C5 FAILS)**: Recipe density structurally unstable. Product lane uses non-recipe density only.

**Negative (Docker unavailable, C8 FAILS)**: Extrapolation question genuinely open. Docker measurement required to resolve. Blocking dependency carried forward.

## Validity Threats

1. **Docker image unavailability**: The image may not be pullable from Docker Hub. This is an infrastructure failure, not a scientific negative. The fallback bootstrap analysis provides partial information but cannot fully resolve the empirical question.

2. **Docker container startup failure**: Even if pulled, the Magento container may fail to start or initialize. Record exact error and classify as infra-blocked.

3. **Full-DOM collection failure**: Browser automation may fail to collect full locatable_sample. The collection script may need modification to capture all elements with bbox.

4. **Truncation in existing data**: The existing exp347 data has locatable_sample truncated to first-20. This was confirmed in EXP-INTEL-35462974425. Full-DOM re-collection is the only path to new data.

5. **Bootstrap CI width**: With 10000 iterations, the bootstrap CI at n=20 is tight ([55.6%, 57.5%]). However, extrapolation to n=50/82 introduces model-dependent uncertainty that bootstrap cannot fully capture.

6. **Logistic extrapolation model dependence**: The logistic fit on 4 points (2 at zero) is model-dependent. Different functional forms (power law, Hill, Richards) may give different extrapolations. The parent found all model-based approaches failed. The bootstrap analysis should report sensitivity to functional form.

7. **Single Magento site**: Results are bounded to one site with specific template structure. Cross-site generalization is unknown.

8. **7 tasks, 3 page types**: Small sample limits generalization. Cart n=1 has degenerate within-type variance.

## Stable Identities

- experiment_id: EXP-INTEL-35572177756
- lane: intel
- claim_ids: ["C-MEAS-VALID"]
- parent_experiment_id: EXP-INTEL-35551517470
- parent_handoff_sha256: ce6224a979be8a76f57b2d20931c09611135007c533b518c258648f929bf2d27
- baseline B1 source: EXP-INTEL-35476271877/snr_per_iteration_tag_entropy.json.gz (sha256: ce3dda6e021137ef0c911c19d8897c24f26342e8bd6da77242e1a026e08c1b7a)
- raw data source: EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json (sha256: da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050)
- frozen analysis script: EXP-INTEL-35462974425/analyze.py (sha256: 79721d4668c679d4fb2695b092b848a2c1d8b3bcbdf262f81a5641c6ddc1b459)
- Docker image: am1n3e/webarena-verified-shopping:latest
