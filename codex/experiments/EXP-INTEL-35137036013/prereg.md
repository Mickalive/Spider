# EXP-INTEL-35137036013 — Preregistration

## Status

DESIGN ONLY — awaiting freeze. EXECUTE must not inspect outcomes before freeze.

## Experiment Identity

- **Experiment ID**: EXP-INTEL-35137036013
- **Lane**: intel
- **Parent**: EXP-INTEL-35131994346 (PROVENANCE_PARTIAL)
- **Parent chain**: EXP-INTEL-34782350557 → EXP-INTEL-35112013458 (FALSIFIED) → EXP-INTEL-35124660457 (MEASUREMENT_INVALID) → EXP-INTEL-35131994346 (PROVENANCE_PARTIAL) → **this experiment**
- **Claim IDs**: C-MEAS-VALID
- **Created**: 2026-09-16

## Scientific Question

After the runtime lane removes the first-20 `locatableSample` cap, does full DOM enumeration confirm that the `a→link`-inclusive page-type ordering changes between truncated and full-DOM, and does the null-model pairwise agreement exceed chance on full-DOM data?

## Background and Motivation

### The FALSIFIED verdict chain

1. **EXP-INTEL-34782350557** collected raw DOM measurements from 7 distinct tasks (8 measurements, cart_1 duplicated) on a single Magento site, with first-20 document-order `locatableSample` truncation.

2. **EXP-INTEL-35112013458** tested whether the observed pairwise ordering agreement (0.3) across 5 role-based definitions exceeds chance. **FALSIFIED**: random ROLE_MAP null mean = 0.5275 > observed 0.3, and button-only/form-only definitions reproduce the DEF-FORM-ONLY ordering (violating multi-role invariance).

3. **EXP-INTEL-35124660457** expanded the analysis to 3 definitions (DEF-FULL-MAP, DEF-FORM-ONLY, ISOLATED-A-LINK) with per-definition role filtering. **MEASUREMENT_INVALID**: committed `analyze.py` uses all-role density (producing FALSIFIED) while stored `analysis_results.json` uses per-definition filtering (producing SURVIVES). Provenance mismatch prevents reproducibility. Additionally, the estimator inflates bias 4-7x by conflating total DOM counts with locatable counts.

4. **EXP-INTEL-35131994346** reconstructed the analysis from raw evidence. **PROVENANCE_PARTIAL**: 2/3 definitions (DEF-FULL-MAP, DEF-FORM-ONLY) reconstruct exactly within ±0.001 density tolerance. ISOLATED-A-LINK in stored results is a copy-paste bug (byte-identical to DEF-FULL-MAP). The canonical analysis script remains uncommitted.

### Blocking dependencies

Two blocking dependencies prevent this experiment from executing:

1. **Substrate fix (RUNTIME BLOCKING)**: The runtime lane must remove the first-20 `locatableSample` cap to provide full DOM enumeration. Without this, the locatable elements are capped at 20 per page, discarding 62-95% of interactive elements and introducing document-order selection bias that changes page-type-dependent density ordering.

2. **Canonical script (CODE BLOCKING)**: The analysis script implementing 3-definition per-role filtering with cart_1 deduplication and float scaling must be committed. The committed `analyze.py` uses all-role density (a different algorithm) and produces a different verdict.

### Why this experiment matters

The FALSIFIED verdict from EXP-INTEL-35112013458 is the primary evidence against the density-based ordering metric (C-MEAS-VALID). If truncation artifacts drove the FALSIFIED result, the metric may be valid under full enumeration. If the FALSIFIED result persists under full enumeration, the metric family is genuinely invalid and product must adopt alternative metrics.

This is the **decisive test** that resolves the entire chain.

## Hypothesis

**H1**: Full DOM enumeration produces a different page-type ordering than truncated-first-20 for at least one definition (DEF-FULL-MAP or DEF-FORM-ONLY).

**H2**: On full-DOM data, the null-model pairwise agreement mean is at or above the observed pairwise agreement (i.e., observed does not exceed chance), confirming the metric's null-model test is valid.

**Combined**: H1 AND H2 together mean truncation drove the FALSIFIED verdict and the metric survives under full enumeration.

## Falsification Conditions

**F1**: Full DOM ordering is identical to truncated ordering for ALL definitions.

**F2**: Null-model pairwise agreement on full-DOM data remains below chance (null mean > observed), as on truncated data.

**F3**: If F1 AND F2 both hold, truncation did not drive the FALSIFIED verdict; the metric fails on full DOM.

## State Representations

### Definitions (carried from parent chain)

| Definition | Roles included | Scientific purpose |
|---|---|---|
| DEF-FULL-MAP | a + button + input + combobox | Full interactive element map |
| DEF-FORM-ONLY | button + combobox | Form-interaction subset |
| ISOLATED-A-LINK | a only | Isolated link-role test |

### Density computation

- **Truncated density**: `count(locatable elements matching definition in first-20 document order) / total_locatable_elements_in_page`
- **Full-DOM density**: `count(locatable elements matching definition in full DOM) / total_locatable_elements_in_page`
- **Estimator note**: Parent audit V1 documents that total DOM tag counts (linksCount 393-397) inflated bias 4-7x vs proper locatable counts (~19 links). This experiment uses per-definition role-filtered counts. The substrate fix provides true locatable element counts.

### Page types

- product_listing (n=3 tasks)
- detail (n=3 tasks)
- cart (n=1 distinct task after deduplication)

## Analysis Plan

### Step 1: Verify substrate fix

Confirm that the `locatableSample` cap has been removed:
- `locatable_elements` count must exceed 20 for at least one task
- DOM stats must show full element enumeration
- If cap is still present: MEASUREMENT_INVALID

### Step 2: Run canonical script on full-DOM data

Execute the committed canonical analysis script on the full-DOM data with:
- 3-definition per-role filtering (DEF-FULL-MAP: a+button+input+combobox; DEF-FORM-ONLY: button+combobox; ISOLATED-A-LINK: a only)
- cart_1 deduplication (8→7 tasks)
- Float scaling (not integer truncation)

Record per-definition:
- Truncated ordering (first-20 document order)
- Full-DOM ordering
- Ordering changed (C1): boolean per definition
- Per-task density values

### Step 3: Run null model on full-DOM data

For each definition where C1=true:
- Generate 1000 random ROLE_MAP assignments (seed=42)
- Compute pairwise agreement for each random assignment
- Record null distribution mean, p5, p95
- Compare observed pairwise agreement to null distribution

### Step 4: Evaluate decision rule

Apply the conjunctive decision rule from spec.json:
- C1_ORDERING_CHANGED: at least one definition shows ordering change
- C2_NULL_EXCEEDS_OBSERVED: for definitions with C1=true, null mean ≥ observed

## Baselines

| ID | Description | Expected behavior |
|---|---|---|
| B1_TRUCATED_REGRESSION | Canonical script on truncated-first-20 data | Reproduce known truncated ordering and null result (null 0.5275 > observed 0.3) |
| B2_COMMITTED_SCRIPT_BASELINE | Committed analyze.py (all-role density) on full-DOM data | Document algorithmic difference under full enumeration |
| B3_STORED_RESULTS_COMPARISON | Load stored analysis_results.json | Confirm reference values for truncated-sample comparison |

## Controls

| ID | Type | Expected | Falsification |
|---|---|---|---|
| positive_control | Script regression | Canonical script on truncated data reproduces known ordering and null result | Script is misimplemented |
| null_control | Null model | Random ROLE_MAP on full-DOM data produces null mean ≥ observed for definitions where ordering changes | Null model is broken or data is contaminated |

## Stable Metric Identifiers (for EXECUTE/AUDIT)

| Metric ID | Description | Type |
|---|---|---|
| M1_C1_ORDERING_CHANGED | Per-definition boolean: does full-DOM ordering differ from truncated? | Derived, per-definition |
| M2_C2_NULL_EXCEEDS_OBSERVED | Per-definition: null mean pairwise agreement ≥ observed on full DOM? | Derived, per-definition |
| M3_OBSERVED_PAIRWISE_AGREEMENT | Pairwise agreement of 5-definition orderings on full-DOM data | Derived, pooled |
| M4_NULL_MEAN_PAIRWISE_AGREEMENT | Mean pairwise agreement under random ROLE_MAP (1000 iter, seed=42) on full-DOM | Derived, per-definition |
| M5_DENSITY_DIFF_TRUNCATED_VS_FULL | Per-task density difference (full - truncated) per definition | Derived, per-task |
| M6_PER_DEFINITION_ORDERING | Truncated and full orderings per definition | Derived, per-definition |

## Stable Control Identifiers (for EXECUTE/AUDIT)

| Control ID | Description |
|---|---|
| B1_TRUCATED_REGRESSION | Canonical script reproduces truncated-sample ordering and null result |
| B2_COMMITTED_SCRIPT_BASELINE | Committed script behavior under full enumeration |
| B3_STORED_RESULTS_COMPARISON | Stored results reference values |
| C_POSITIVE_SCRIPT_REGRESSION | Positive control: script produces known output on truncated data |
| C_NULL_MODEL_RANDOM_ROLE_MAP | Null control: random roles on full-DOM data |

## Decision Rule (frozen)

```
if NOT measurement_validity_pass:
    verdict = MEASUREMENT_INVALID
elif C1_ORDERING_CHANGED AND C2_NULL_EXCEEDS_OBSERVED:
    verdict = SURVIVES_CURRENT_TEST
elif C1_ORDERING_CHANGED AND NOT C2_NULL_EXCEEDS_OBSERVED:
    verdict = MIXED
elif NOT C1_ORDERING_CHANGED AND NOT C2_NULL_EXCEEDS_OBSERVED:
    verdict = FALSIFIED
elif NOT C1_ORDERING_CHANGED AND C2_NULL_EXCEEDS_OBSERVED:
    verdict = INCONCLUSIVE
```

## Product Consequences

- **SURVIVES**: FALSIFIED verdict confirmed as truncation artifact. Density metric valid under full DOM. C-MEAS-VALID advances. Product may adopt DEF-FULL-MAP as canonical metric (bounded to single Magento site).
- **FALSIFIED**: Metric fails on full DOM. C-MEAS-VALID BLOCKED for density family. Product must explore alternative metrics.
- **MIXED**: Ordering changes but null still exceeds observed. Metric partially survives. Further investigation needed.
- **INCONCLUSIVE**: Cannot distinguish signal from noise. Metric status unchanged.

## Validity Threats

1. **Single site**: Bounded to 1 Magento site, 7 distinct tasks. No cross-site generalization.
2. **Small N**: n=3 per page type (product_listing, detail), n=1 distinct cart. No within-type CI possible.
3. **Estimator accuracy**: Even with per-definition role filtering, the density estimator's accuracy depends on the substrate fix providing true locatable element counts.
4. **ISOLATED-A-LINK interpretation**: If a elements dominate the locatable pool, ISOLATED-A-LINK ordering may be tautologically identical to DEF-FULL-MAP.
5. **Null model sensitivity**: 1000 iterations with seed=42 provides limited resolution for rare events. Results should be treated as directional.

## Expected Information Gain

**High**: This is the decisive test for the density-based ordering metric family. A clear SURVIVES or FALSIFIED result directly changes the C-MEAS-VALID claim status and product decision. The experiment resolves a chain of 4 prior experiments spanning the full validity investigation.

## Dependencies

| Type | Description | Blocking |
|---|---|---|
| substrate | Runtime lane removes first-20 locatableSample cap | YES |
| code | Canonical analysis script committed with 3-definition filtering, dedup, float scaling | YES |
| data | Additional sites with non-zero menuitem/tab counts | NO |
| data | More distinct cart pages (current n=1) | NO |
