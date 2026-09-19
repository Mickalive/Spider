# EXP-INTEL-35470447439 — Preregistration

## 1. Title

Full DOM re-collection to unblock recipe ranking stability experiment: testing whether truncation artifact explains the 55.95% canonical agreement at truncated-first-20.

## 2. Background and motivation

The parent experiment (EXP-INTEL-35445596324) found that canonical recipe sampling achieves only 55.95% ranking agreement at n=20 (truncated-first-20 locatable_sample), well below the 80% stability threshold. The BLOCKED follow-up (EXP-INTEL-35462974425) confirmed this is because ALL 7 tasks had locatable_sample truncated to exactly 20 elements at collection time in EXP-INTEL-34782350557 (the `if (locatableSample.length < 20)` cap in measure_fullpage_yield.py line 89).

The `locatable_elements` metadata correctly reports 82/32/21 elements for listing/detail/cart tasks, but the `locatable_sample` array was capped at 20. This means the existing data cannot test whether ranking stabilizes at larger n.

The hypothesis is that full DOM samples (n=21-82) contain richer element diversity per definition, enabling canonical recipe sampling to capture a more representative subset and stabilize rankings above 80%.

## 3. Inherited state (from parent handoff)

### Established
- Sample-size effect on ranking agreement is real and monotonic: 0% at n=5/10 → 50% at n=15 → 56% at n=20 (Spearman=1.0)
- Ranking agreement plateaus below 80% at maximum available sample size
- Non-recipe pipeline ranking agreement requires ≥15 elements to preserve listing > detail
- OECD/COINr pipeline preserves between-type discrimination (max eta2 0.999645)
- Per-task recipe achieves 78.65% at n=20 — tantalizingly close to 80%
- Raw features retain perfect task-type discrimination (eta2=1.0)
- Data truncation root cause confirmed: locatable_sample truncated to first-20 at collection time

### Rejected
- Hypothesis that ranking instability is purely a sample-size artifact within truncated-first-20 range — REJECTED (plateaus at 56% at n=20)
- OECD/COINr pipeline structure itself destroys between-type variance — REJECTED

### Unknown (untested)
- Does ranking stabilize at full DOM (n=21-82)?
- Does per-task recipe achieve ≥80% at full DOM?
- Cross-site generalization of the sample-size effect

### Do not assume
- That n=20 result generalizes to full DOM n=21-82
- That recipe-based density is safe for Product Core promotion
- That this BLOCKED experiment provides evidence for or against the full-DOM hypothesis (it provides NONE)

## 4. Hypothesis

The ranking instability (55.95% canonical agreement at truncated-first-20) is a truncation artifact. Full DOM samples with richer element diversity will achieve ≥80% canonical recipe ranking agreement for tag_entropy × DEF-FULL-MAP.

## 5. Falsifier

The hypothesis is falsified if ANY of:
- (F1) Canonical recipe agreement on full DOM <75% — structural instability regardless of element count
- (F2) Full-DOM does NOT exceed truncated-first-20 (55.95%) by ≥10pp — additional elements don't help
- (F3) Per-task recipe agreement on full DOM <75% — independent sampling can't stabilize with richer diversity
- (F4) Pipeline eta2 on full DOM <0.90 — full-DOM elements introduce noise degrading discrimination

## 6. Experimental design

### Phase A: Collection (new work)

Write a modified collection script (`collect_full_dom.py`) that:
1. Removes the `< 20` cap from the original MEASURE_JS (EXP-INTEL-34718481334/measure_fullpage_yield.py line 89)
2. Collects ALL elements with bbox into `locatable_sample`
3. Runs against the Magento Docker container (am1n3e/webarena-verified-shopping:latest)
4. Collects the same 7 tasks (3 listing, 3 detail, 1 cart)
5. Produces output in the same JSON format as EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json

Validation before full execution:
1. Verify Docker container is accessible
2. Collect data for 1 task first and verify locatable_sample length >20
3. Only then collect all 7 tasks

### Phase B: Analysis (reuse frozen code)

Run the frozen `analyze.py` from EXP-INTEL-35462974425 on the newly collected full-DOM data. The frozen decision_rule C3 gate will automatically pass if ≥5 tasks have locatable_sample >20, enabling evaluation of C1-C7.

## 7. State representation

- **Elements**: All DOM elements with non-zero bounding box (tag, role, ariaLabel, inForm, x, y, w, h)
- **Features**: tag_entropy (Shannon entropy of tag distribution), form_fraction (1.0 if inForm), total_area (w × h)
- **Definitions**: DEF-FULL-MAP (a→link, input→textbox, 13 interactive roles), DEF-FORM-ONLY (10 interactive roles, no role mapping)
- **Density**: sum(feature_value for matching elements) / elements_with_bbox
- **Ranking**: listing vs detail page_type comparison via eta2

## 8. Sampling policy

- **Recipe sampling**: canonical recipe (shared subset p=0.5) and per-task recipe (independent p=0.5 per task)
- **Iterations**: 10 seeds × 1000 iterations per recipe type
- **Bootstrap**: 1000 resamples of tasks within page_type

## 9. Unit of analysis

Task-level feature-weighted density values, compared across page_type (listing vs detail).

## 10. Baselines

- B1: Truncated-first-20 canonical agreement 55.95%
- B2: Truncated-first-20 per-task agreement 78.65%
- B3: Non-recipe pipeline 100% ranking preservation at n≥15
- B4: Pipeline eta2 0.999645 at n=20
- B5: BLOCKED experiment C3 gate (0/7 tasks >20 elements)

## 11. Positive control

PC1: Raw features reproduce full-DOM discrimination (eta2 >= 0.99 for all three features on page_type)

## 12. Null control

NC1: Normalized hierarchy density produces eta2 < 0.01 on page_type (y-proxy degeneracy anchor)

## 13. Primary metrics

- M1: Canonical recipe ranking agreement for tag_entropy × DEF-FULL-MAP on full DOM
- M2: Per-task recipe ranking agreement for tag_entropy × DEF-FULL-MAP on full DOM
- M3: Delta vs truncated-first-20 (full_DOM_agree - 0.5595)
- M4: Bootstrap CI (mean ± std) for canonical agreement
- M5: Pipeline eta2 on full DOM
- M6: Canonical recipe eta2 on full DOM
- M7: Per-task recipe eta2 on full DOM

## 14. Decision rule (conjunctive, as frozen in spec.json)

See spec.json for the complete decision_rule with C1-C7 conditions and verdict rules.

## 15. Expected outcomes and consequences

**If SURVIVES (C5 AND C6 PASS):**
- Ranking instability was a truncation artifact
- MIXED program unblocked
- Product lane can use recipe density with the existing framework
- The 31x recipe material gap becomes actionable

**If FALSIFIES (C5 FAILS, <65.95%):**
- Ranking instability is structural regardless of element count
- Product lane must use non-recipe density only
- Recipe density design path permanently closed for this framework

**If MIXED (C5 passes but C6 fails, 65.95%-80%):**
- Truncation contributes but is not sole cause
- Partial improvement; further investigation needed

## 16. Threats to validity

1. **Single site**: Only Magento Docker container tested. Cross-site generalization unknown.
2. **7 tasks**: Small sample limits bootstrap power. Within-type variance for cart (n=1) is degenerate.
3. **Template invariance**: Within-type identical structure may inflate eta2 artificially (inherited from prior experiments).
4. **Collection script differences**: Modified MEASURE_JS may have subtle behavioral differences from original. Mitigated by same Docker image, viewport, and task definitions.
5. **DOM-sequential subsampling**: First-n elements by DOM position may not represent random subsets (inherited limitation from parent).

## 17. Analysis code

Frozen `analyze.py` from EXP-INTEL-35462974425 (sha256: 79721d4668c679d4fb2695b092b848a2c1d8b3bcbdf262f81a5641c6ddc1b459). Reused unchanged.
