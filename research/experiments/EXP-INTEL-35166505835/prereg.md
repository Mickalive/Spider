# EXP-INTEL-35166505835 preregistration

**Experiment ID**: EXP-INTEL-35166505835
**Lane**: intel
**Claim IDs**: C-MEAS-VALID
**Created**: 2026-09-17T00:25:49Z

---

## Inherited Context

- **Parent Handoff**: EXP-INTEL-35137036013 (sha256: 189301c4cad2bbb6a9d1b1ce93a3ef5a438aad9bc24d53df369d1e6de2463ed3)
- **Inherited Last Verdict**: MEASUREMENT_INVALID
- **Inherited Next Question**: After the runtime lane removes the first-20 locatableSample cap and a canonical analysis script (3-definition per-role filtering, cart_1 dedup, float scaling) is committed, does full DOM enumeration confirm that the a→link-inclusive page-type ordering changes between truncated and full-DOM, and does the null-model pairwise agreement exceed chance on full-DOM data?

### Parent carry_forward

**Established**:
- ISOLATED-A-LINK stored results invalid (byte-identical to DEF-FULL-MAP)
- Directional finding: first-20 truncation introduces page-type-dependent ordering change
- Committed analyze.py uses different algorithm than 3-definition per-role filtering
- Cart_1 deduplication required (8→7 tasks)
- ISOLATED-A-LINK corrected a-only ordering_changed=False

**Rejected**:
- Stored ISOLATED-A-LINK results valid
- Committed analyze.py is canonical 3-definition analysis

**Unknown**:
- Full DOM enumeration effect on density magnitudes and ordering
- Whether canonical 3-definition script should be committed or analyze.py accepted
- C2 direction (null>observed vs null>=observed)
- Statistical significance of product_listing vs detail ordering swap
- Null-model pairwise agreement on true full-DOM data

**Do Not Assume**:
- Proxy tag-count estimator provides valid full-DOM density values
- FALSIFIED verdict from EXP-INTEL-35112013458 is explained by truncation
- Proxy C1/C2 values are evidence for full DOM signal
- C2 direction is unambiguous
- Ordering differences are statistically significant
- Results generalize to other sites
- Random baseline advantage is scientifically meaningful
- ISOLATED-A-LINK corrected ordering applies to other definitions

---

## 1. Research Question

Can the intel lane, within its own scope, resolve the two non-substrate blocking dependencies (C2 semantic contradiction in spec.json and canonical-script absence) that prevent re-running the full-DOM density metric measurement, and does a formal dependency audit confirm the substrate (locatableSample cap) remains the sole remaining runtime-lane blocker?

## 2. Hypothesis

The C2 semantic contradiction can be resolved to a single coherent direction by analyzing the statistical intent of the original FALSIFIED verdict from EXP-INTEL-35112013458, and a concrete canonical-script specification can be produced that unblocks measurement reproducibility. The locatableSample cap in MEASURE_JS remains the sole remaining runtime-lane blocker.

## 3. Falsifier

If the C2 contradiction cannot be resolved without introducing a new scientific assumption, or the canonical-script specification is inconsistent with the 3-definition per-role filtering algorithm, or the locatableSample cap has been removed, then the design work is invalid or superseded.

## 4. Baselines

### B1_SPEC_COHERENCE
Read frozen spec.json from EXP-INTEL-35137036013. Extract C2 falsifier and decision_rule clauses. Document exact contradiction. Verify still present at HEAD.

### B2_CANONICAL_SCRIPT_ABSENCE
Search repository for committed canonical analysis script implementing 3-definition per-role filtering with cart_1 dedup and float scaling. Expected: no such script exists.

### B3_MEASURE_JS_CAP
Search MEASURE_JS in measure_fullpage_yield.py for locatableSample cap. Expected: `if (locatableSample.length < 20)` still present at line 89.

## 5. Positive Control

Frozen spec.json from EXP-INTEL-35137036013 contains both contradictory C2 clauses. Canonical script search returns zero matches. MEASURE_JS cap search returns a match.

## 6. Null Control

If C2 contradiction already resolved in a newer spec.json, the resolution work is unnecessary and the experiment is superseded.

## 7. Measurement Validity

- This is a dependency audit and design-resolution exercise, not an outcome-bearing measurement
- No browser interaction, data collection, or model calls required
- All evidence from committed artifacts (spec.json, code files, MEASURE_JS)
- C2 resolution grounded in original experiment's statistical intent

## 8. C2 Resolution Analysis

### The Contradiction

The spec.json from EXP-INTEL-35137036013 contains:

**Falsifier (spec.json line 7)**:
> "If (F2) null-model pairwise agreement on full-DOM data remains below chance (null mean > observed, as on truncated data), THEN truncation did not drive the FALSIFIED verdict and the metric itself fails the null-model test under full enumeration."

**Null Control (spec.json line 14)**:
> "If the null distribution mean pairwise agreement on full-DOM data is at or above the observed pairwise agreement, the null hypothesis (ordering is at chance) is not rejected and the FALSIFIED verdict stands."

**Decision Rule (spec.json line 22)**:
> "C2_NULL_EXCEEDS_OBSERVED: For at least one definition where C1 is true, the null-model pairwise agreement mean on full-DOM data is ≥ the observed pairwise agreement on full-DOM data (i.e., the observed ordering does not exceed chance)."

The contradiction:
- Falsifier: null > observed → FALSIFIED
- Decision Rule: null ≥ observed → SURVIVES (C2=true)

These are logically incompatible when null = observed.

### Resolution Approach

The original FALSIFIED verdict from EXP-INTEL-35112013458 was based on null mean (0.5275) > observed (0.3). The intent was: "does the observed ordering exceed what we'd expect by chance?" If null ≥ observed, the answer is NO — the observed ordering does not exceed chance.

The resolution should be:
- **C2 = true** means: null mean ≥ observed → observed does NOT exceed chance → metric FAILS null test
- **C2 = false** means: null mean < observed → observed EXCEEDS chance → metric SURVIVES null test

This aligns the falsifier and decision_rule: both say "null ≥ observed is bad for the metric."

## 9. Canonical Script Specification

The canonical analysis script must implement:

1. **3-Definition Per-Role Filtering**:
   - DEF-FULL-MAP: a + button + input + combobox
   - DEF-FORM-ONLY: button + combobox
   - ISOLATED-A-LINK: a only

2. **Cart_1 Deduplication**: Remove duplicate cart_1 entry (8→7 unique tasks)

3. **Float Scaling**: Use float counts, not integer truncation

4. **Density Calculation**: For each definition, per task:
   - Count elements matching the definition's roles
   - Divide by total DOM elements (or locatable elements, depending on substrate)

5. **Page-Type Ordering**: Sort page types by mean density across tasks of that type

6. **Null Model**:
   - Random ROLE_MAP assignment (1000 iterations, seed=42)
   - For each iteration: compute density with shuffled role assignments
   - Compute pairwise agreement among null orderings
   - Compare null mean to observed pairwise agreement

7. **C1 Evaluation**: ordering_changed = (truncated_ordering != full_ordering)

8. **C2 Evaluation** (using resolved direction):
   - C2 = true if null_mean ≥ observed (metric fails null test)
   - C2 = false if null_mean < observed (metric survives null test)

## 10. Decision Rule

C1_C2_RESOLVED: C2 contradiction resolved to single coherent direction consistent with original FALSIFIED intent.

C2_CANONICAL_SPEC_PRODUCED: Concrete canonical-script specification produced with all 8 components above.

C3_SUBSTRATE_BLOCKER_CONFIRMED: locatableSample cap still present in MEASURE_JS.

- C1=true AND C2=true AND C3=true → BLOCKING_REDUCED
- C1=true AND C2=true AND C3=false → SUPERSEDED
- C1=false OR C2=false → DESIGN_FAILED

## 11. Product Consequences

**Positive (BLOCKING_REDUCED)**: Two of three blockers resolved. Next re-run has only one remaining blocker (runtime substrate fix). Reproducible canonical-script specification available for any lane to commit.

**Negative (DESIGN_FAILED)**: C2 contradiction or canonical-spec inconsistency cannot be resolved. Full-DOM density metric chain blocked at deeper level than recognized.

## 12. Estimated Cost

Minimal: offline code/spec reading and analysis. No browser, no data collection, no model calls. Near-zero compute.

## 13. Expected Information Gain

Medium-high: resolves blocking design ambiguity persisted across 4 experiments (EXP-INTEL-35112013458 → 35124660457 → 35131994346 → 35137036013). Clear resolution either unblocks next measurement or reveals deeper statistical framework problem.
