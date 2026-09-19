# Preregistration: EXP-INTEL-35422991016

## Experiment Identity

- **experiment_id**: EXP-INTEL-35422991016
- **lane**: intel
- **claim_ids**: C-MEAS-VALID
- **parent**: EXP-INTEL-35409927864

## Question

Can a density metric based on sample-derived features (tag entropy, form fraction, total_area) -- which achieve eta2=1.0 on page_type -- be designed to produce non-zero task-type discrimination within the OECD/COINr framework, or does the hierarchy-weighted density formula's collapse generalize to all density metrics on this truncated-first-20 sample?

## Background and Motivation

The parent experiment (EXP-INTEL-35409927864) decisively falsified the template-composition explanation for zero density eta2. The locatable_sample DOES have task-type discrimination (eta2=1.0 on tag_entropy, form_fraction, total_area), but the hierarchy-weighted density formula produced eta2=0.0. This dissociation means the density formula -- not the sample -- is the bottleneck.

The parent handoff asks: can a density metric based on the sample's discriminative features be designed to produce non-zero task-type discrimination within OECD/COINr? This experiment directly tests that question.

**Inherited established facts (from parent carry_forward.established):**
- Sample has task-type discrimination eta2=1.0 on tag_entropy/form_fraction/total_area (EXP-INTEL-35409927864 M2)
- Structural fields (tag, role, inForm, x, w, h) are 100% identical within each page type (EXP-INTEL-35409927864 M1)
- Recipe choice is MATERIAL: 31x canonical/weighted density gap (EXP-INTEL-35264637598)
- Linear combinations CANNOT break OECD/COINr dominance degeneracy (EXP-INTEL-35353016702)
- Within each recipe, definitions are highly correlated (Spearman r > 0.98) (EXP-INTEL-3330747199)
- Heuristic hierarchy-weighted density is a perfect monotonic reparameterization of weighted (Spearman rho=1.0 at alpha=0.3) with zero task-type structure (EXP-INTEL-35401997918)

**Inherited unknowns (from parent carry_forward.unknown):**
- Can a density metric based on tag entropy, form fraction, total_area be designed to produce non-zero task-type discrimination within OECD/COINr?
- Does the hierarchy-weighted density formula's collapse generalize to ALL density metrics?
- Is MIXED outcome resolvable at all within OECD/COINr with any density-based recipe?

**Inherited do_not_assume (from parent carry_forward.do_not_assume):**
- OECD/COINr framework has been validated for SPIDER -- it has not
- 31x canonical/weighted ratio is validated on full DOM -- only tested on truncated-first-20 sample
- Density metric is entirely useless -- recipe choice is MATERIAL (31x gap)
- True DOM depth failure is implied by heuristic depth failure -- negative result bounded to inForm-based heuristic

## Hypothesis

The hierarchy-weighted density formula's eta2=0.0 is caused by the specific exp(-alpha*depth) with binary inForm depth mapping collapsing between-type variance, not by a fundamental limitation of the sample or the OECD/COINr framework. A density metric constructed from the sample's discriminative features (tag entropy, form fraction, total_area -- all achieving eta2=1.0 on page_type) should produce non-zero task-type discrimination when passed through OECD/COINr density computation.

## Falsifier

The hypothesis is falsified if ANY of:
- F1: ALL tested density metrics based on entropy/form_frac/total_area produce eta2=0.0 on page_type within OECD/COINr (the collapse is formula-independent)
- F2: The OECD/COINr density pipeline maps different input feature vectors to identical density values for all tasks of the same page type regardless of the input metric chosen (the framework itself collapses between-type variance)
- F3: At least one alternative density metric achieves eta2 > 0.0 but within-type variance exceeds between-type variance (density values are noisy not discriminating)

## Data Source

All data comes from existing raw evidence:
- **Source**: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json`
- **SHA256**: `da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050`
- **Scope**: 7 tasks (3 product_listing, 3 detail, 1 cart deduplicated from 8 success measurements), 1 Magento site, 3 definitions, truncated-first-20 locatable_sample
- **No new data collection required**

## Alternative Density Metrics to Test

The following density metrics will be constructed from the sample's discriminative features and tested within the OECD/COINr framework:

1. **Tag entropy density**: Direct use of tag_entropy (listing 2.646 vs detail 2.484 vs cart 2.602)
2. **Form fraction density**: Direct use of form_fraction (listing 0.85 vs detail 0.95 vs cart 0.95)
3. **Total area density**: Direct use of total_area (listing 341k vs detail 589k vs cart 428k)
4. **Combined entropy+area**: Normalized combination of tag_entropy and total_area
5. **Normalized entropy**: tag_entropy / log2(unique_tags) (entropy relative to maximum possible entropy given the tag vocabulary)

Each metric will be used as the input to the OECD/COINr density computation pipeline, replacing the hierarchy-weighted density formula.

## Decision Rule

Conjunctive:

**C1_HIERARCHY_REPRODUCES**: The hierarchy-weighted density formula produces eta2 < 0.01 on page_type when run on the truncated-first-20 sample.
- PASS if eta2 < 0.01; FAIL if eta2 >= 0.01.

**C2_ALTERNATIVE_ETA2_NONZERO**: At least one alternative density metric (constructed from tag entropy, form fraction, or total_area) achieves eta2 >= 0.05 on page_type within the OECD/COINr density pipeline.
- PASS if max(eta2) >= 0.05; FAIL if all eta2 < 0.05.

**C3_DENSITY_VALUES_DISCRIMINATE**: For the best alternative metric, the between-type variance exceeds within-type variance (eta2 > 0.0) AND the density values for listing and detail tasks are distinct (absolute difference > 1% of range).
- PASS if both conditions hold; FAIL otherwise.

**C4_WITHIN_TYPE_STABILITY**: For the best alternative metric, within-type standard deviation of density values is less than 50% of between-type range.
- PASS if std_within / range_between < 0.5; FAIL otherwise.

**VERDICT RULES:**
- If NOT C1: MEASUREMENT_INVALID -- hierarchy reproduction fails, cannot anchor comparison.
- If C1 AND NOT C2: FALSIFIES -- all alternative density metrics also produce eta2=0.0. The collapse is formula-independent; the OECD/COINr framework itself cannot exploit the sample's discriminative features. Abandon density-based MIXED handling for this sample.
- If C1 AND C2 AND NOT C3: MIXED -- some alternative metric achieves non-zero eta2 but density values do not reliably discriminate. Metric design partially helps but is insufficient.
- If C1 AND C2 AND C3 AND NOT C4: MIXED -- density values discriminate on average but within-type noise is high. Limited practical utility.
- If C1 AND C2 AND C3 AND C4: SURVIVES -- a density metric based on discriminative sample features achieves task-type discrimination within OECD/COINr. The hierarchy formula was the bottleneck. Product can pursue density-based MIXED resolution.

## Positive Control

**PC1_SAMPLE_ETA2_NONZERO**: The sample's raw features (tag entropy, form fraction, total_area) achieve eta2 > 0.0 on page_type when computed directly (not through density formula). This confirms the sample contains task-type-discriminative information.
- Expected: eta2 >= 0.10 for at least one of tag_entropy, form_fraction, or total_area on page_type

## Null Control

**NC1_HIERARCHY_REPRODUCTION**: Reproduce the parent's hierarchy-weighted density computation on the same truncated-first-20 sample to confirm eta2=0.0 is reproducible and not an implementation artifact.
- Expected: Hierarchy-weighted density eta2 < 0.01, reproducing EXP-INTEL-35401997918 M7

## Product Consequence

**If positive (C4 PASS)**: Resolves the MIXED program bottleneck. Density-based task-type discrimination is achievable with the right metric. Product lane can pursue density-based MIXED handling using entropy/form_frac/total_area-derived density instead of hierarchy-weighted density.

**If negative (C2 FAIL)**: The OECD/COINr framework itself is the bottleneck, not the specific formula. Density-based MIXED handling should be abandoned for this sample/site, and the lane should pivot to cross-site testing or non-density-based approaches.

## Estimated Cost

VERY LOW -- offline computation on existing reconstructed data. No browser/network work. Compute density from 3 features x 7 tasks x 20 elements = 420 feature values. Test ~5 alternative density metrics. Estimated < 2000 LLM tokens.

## Scope Limitations

- 7 tasks (3 listing, 3 detail, 1 cart), 1 Magento site, 3 definitions, truncated-first-20 locatable_sample
- Cart n=1 within-type variance is degenerate; comparison focuses on listing vs detail
- Cross-site generalization not tested
- Full DOM density values not in scope
- Per-task sampling not required (parent established sample has eta2=1.0 on basic features)
