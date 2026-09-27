# Experiment Report: EXP-GRAPH-36287167610

**Lane:** graph
**Claim:** C-SEMANTIC-RESOLVE
**Experiment ID:** EXP-GRAPH-36287167610
**Date:** 2026-09-27
**Status:** MEASUREMENT_INVALID
**Outcome:** INCONCLUSIVE

---

## 1. Executive Summary

This experiment tested whether a dual-class fitted applicability gate (trained on both applicable and no-applicable goals) can achieve calibrated routing with bounded false-accept rates. The experiment **FAILED measurement validity** due to **V13 Instrument Dynamic Range** failure: the fitted gate fired on 0% of applicable validation goals (below the required 10% threshold), making it inert on the positive class.

**Key Finding:** The dual-class logistic gate with F1-optimal threshold selection produces a threshold that is too high for applicable goals, resulting in zero abstentions on applicable goals while achieving 60% abstention on no-applicable goals. This replicates the core pathology of the previous experiment (EXP-GRAPH-36279237023) where the gate was fitted only on positive-class data — here, even with negative-class data, the threshold selection rule (maximize F1) still yields an inert gate on applicable goals.

---

## 2. Measurement Validity Assessment (V1-V13)

| Gate | Description | Status | Details |
|------|-------------|--------|---------|
| V1 | Construct Validity | PASS | Primary metric = mechanism-identity binding on applicable; pooled false-accept on ALL goals; coverage/selective-risk on answered applicable |
| V2 | Positive Control Executed | PASS | PC-VERBATIM-INTENT: 12/12 verbatim goals, accuracy=1.0 |
| V3 | Oracle Ceiling | PASS | B-INTERNAL-ID-ORACLE: 52/52 applicable, accuracy=1.0 |
| V4 | Calibration Fitted | PASS | LogisticRegression fitted on dual-class train data (w=2.689, b=-1.317); not fixed algebraic transform |
| V5 | Closed Top Bin ECE | PASS | ECE estimator uses closed top bin [0.9, 1.0] inclusive, 10 equal-mass bins |
| V6 | UNKNOWN Precision Defined | PASS | Explicit TP/FP definition: TP=no-mechanism AND abstain, FP=mechanism AND abstain |
| V7 | Per-Task State Reset | PASS | All 80 tasks began from identical state hash (ef0cafcd...) |
| V8 | Degeneracy Screen | PASS | Lexical applicable-only accuracy=0.6346 < 0.90; Embedding argmax executable=52/52 |
| V9 | Code Bound via Prereg | PASS | All 4 harness modules SHA256 recorded; freezer hashes prereg.md transitively |
| V10 | Family-Blocked Uncertainty | PASS | Paired bootstrap with family (5 families) as blocking unit, 10,000 resamples |
| V11 | Fixture Discrimination | PASS | 4 mechanisms/family across 5 families × 4 verbs; all slots bound; zero unbindable placeholders |
| V12 | Explicit Splits | PASS | Train/val/test splits logged with counts per class before fitting (train: 29 app + 16 na, val: 9 app + 5 na, test: 14 app + 7 na) |
| **V13** | **Instrument Dynamic Range** | **FAIL** | **Gate fires on 0.0% of applicable and 60.0% of no-applicable validation goals** |

**Overall Measurement Validity: FAIL** (V13 failure → MEASUREMENT_INVALID)

---

## 3. Primary and Secondary Gate Results

### 3.1 Primary Metric: Mechanism-Identity Accuracy on Test Applicable (14 goals)

| Arm | Accuracy | Count |
|-----|----------|-------|
| A-CANDIDATE | 0.9286 | 13/14 |
| B-LEXICAL-OVERLAP | 0.5714 | 8/14 |
| B-RANDOM-ROLE | 0.0714 | 1/14 |
| B-EMBEDDING-ARGMAX | 0.9286 | 13/14 |
| B-INTERNAL-ID-ORACLE | 1.0000 | 14/14 |

**Paired Bootstrap (Candidate vs Lexical, family-blocked, 10k resamples):**
- Observed difference: +0.3571
- 95% CI: [0.0833, 0.6923]
- **Primary gate PASS** (CI lower > 0)

**Paired Bootstrap (Candidate vs Random):**
- Observed difference: +0.8571
- 95% CI: [0.6667, 1.0000]
- **Primary gate PASS**

### 3.2 Secondary Gates

| Gate | Metric | Threshold | Observed | Status |
|------|--------|-----------|----------|--------|
| Pooled False Accept | Wrong EXECUTABLE / Total EXECUTABLE (ALL 80 goals) | ≤ 0.10 | 0.3871 (12/31) | **FAIL** |
| Coverage | Fraction applicable with EXECUTABLE | ≥ 0.50 | 0.4423 | **FAIL** |
| Selective Risk | Error rate on answered applicable | ≤ ref + 0.05 | 0.1739 vs 0.1846 | PASS |
| UNKNOWN Precision | TP_abstain / (TP_abstain + FP_abstain) | ≥ 0.85 | 1.0000 | PASS |
| ECE Global | 10-bin closed top bin | ≤ 0.15 | 0.2583 | **FAIL** |
| ECE Per-class Max | Max across classes | ≤ 0.15 | 0.3975 | **FAIL** |

---

## 4. Key Observations

### 4.1 Selection Signal is Real and Strong
- Candidate beats lexical null on test applicable: **0.9286 vs 0.5714** (paired bootstrap CI excludes 0)
- On paraphrase goals (20 unseen wording): Candidate **18/20**, Lexical **11/20**, Embedding **18/20**
- Candidate ties embedding argmax on applicable goals (both 13/14 on test, 45/52 on all applicable)
- Oracle achieves 52/52 — ceiling is reachable

### 4.2 Gate Inertness on Applicable Goals (V13 Failure)
- Fitted threshold: **0.47** (selected to maximize F1 on validation)
- Applicable validation goals (9): **0/9** abstained (p_applicable range all > 0.47)
- No-applicable validation goals (5): **3/5** abstained (60%)
- On all 52 applicable goals: **0/52** gate-fired abstentions
- All 28 candidate abstentions on applicable goals came from **unfilled parameter slots (DEFER)**, not the calibrated gate

### 4.3 Safety Blind Spot on No-Applicable Goals
- Candidate executed **8/28** no-applicable goals (mean p_applicable = 0.5760)
- These wrong executions had p_applicable between 0.49–0.70
- Pooled false-accept rate: **0.3871** (threshold 0.10)
- UNKNOWN precision: **1.0** (14 TP_abstain, 0 FP_abstain) — but this only captures abstentions, not wrong executions

### 4.4 Coverage/Selective-Risk Tradeoff
- Coverage: **0.4423** (below 0.50 threshold)
- Selective risk: **0.1739** (within 0.05 of embedding argmax's 0.1346)
- The low coverage is driven by DEFER (unfilled parameters) on underspecified goals, not gate abstentions

### 4.5 Calibration Quality
- ECE Global: **0.2583** (threshold 0.15) — poorly calibrated
- ECE Per-class max: **0.3975** (UNKNOWN class) — threshold 0.15
- The gate produces overconfident p_applicable values on applicable goals (all > 0.9), but these are never acted on since gate doesn't fire

---

## 5. Interpretation

### 5.1 What This Experiment Establishes

1. **The selection signal is real:** The embedding route materially exceeds the lexical null on unseen paraphrases (18/20 vs 11/20) and ties the uncalibrated embedding argmax on applicable goals. The oracle at 52/52 proves the ceiling is reachable.

2. **The dual-class gate with F1-optimal threshold is inert on applicable goals:** Even with negative-class training data, maximizing F1 selects a threshold that abstains on 0% of applicable goals. The p_applicable distribution for applicable goals is concentrated near 1.0, while no-applicable goals have lower but overlapping scores.

3. **The threshold selection criterion is the problem:** Optimizing F1 on a validation set with class imbalance (9 applicable vs 5 no-applicable) favors a high threshold that maximizes precision on the positive class at the cost of zero recall on abstention decisions for that class.

4. **The null control fails:** NC-NO-APPLICABLE abstention rate = 0.50 (expected 1.0). The candidate does not abstain on all no-applicable goals.

5. **Pooled false-accept is high:** 0.3871 vs 0.10 threshold. The gate does not prevent confident wrong executions on no-applicable goals.

### 5.2 What This Experiment Does NOT Establish

- This does **not** falsify C-SEMANTIC-RESOLVE as a claim. The measurement validity failure (V13) means the experiment could not validly test the hypothesis.
- The dual-class gate architecture with *this threshold selection rule* fails the dynamic range check. A different threshold selection rule (e.g., constrained to ensure minimum abstention on both classes) might pass.
- The calibration quality (ECE) is poor, but this is partly because the gate never fires on applicable goals — the calibration metrics reflect the DEFER/EXECUTABLE behavior, not gate behavior.

### 5.3 Comparison to Previous Experiment (EXP-GRAPH-36279237023)

| Aspect | Previous (Positive-only gate) | Current (Dual-class gate) |
|--------|-------------------------------|---------------------------|
| Gate firing on applicable | 0/52 (0%) | 0/52 (0%) |
| Gate firing on no-applicable | 0/20 (0%) | ~60% on validation, ~32% on test |
| Pooled false-accept | Ambiguous denominator | 0.3871 (unambiguous, but high) |
| Calibration fitted | Yes (but positive-only) | Yes (dual-class) |
| V13 dynamic range | Not checked | **FAIL** (0% applicable) |

The dual-class gate **improves** on the previous experiment by abstaining on some no-applicable goals, but **regresses** on the dynamic range check which now explicitly fails.

---

## 6. Validity Threats and Limitations

1. **Single fixture, single embedding model:** Results may not generalize to other mechanism registries, paraphrase distributions, or embedding models.

2. **Small validation set:** Only 9 applicable + 5 no-applicable validation goals. Threshold selection is noisy.

3. **F1 optimization vs dynamic range tension:** The preregistered threshold selection (maximize F1) conflicts with the dynamic range requirement (minimum 10% abstention on each class). This is a design tension, not a bug.

4. **DEFER class conflation:** Underspecified goals (missing parameters) are scored as DEFER, not gate abstentions. This reduces coverage but is by design.

5. **No held-out test for calibration:** Calibration metrics computed on all goals including train/validation.

6. **Bootstrap only captures family resampling variability:** Does not propagate goal-sampling or seed variability.

---

## 7. Conclusion

**Status: MEASUREMENT_INVALID** — The experiment failed the preregistered Instrument Dynamic Range check (V13). The fitted dual-class applicability gate is inert on applicable goals (0% abstention rate) because the F1-optimal threshold is too high. This prevents valid assessment of the hypothesis.

**Scientific Value:** Despite measurement invalidity, the raw measurements reveal:
- The goal-to-mechanism selection signal is real and exceeds lexical overlap on unseen paraphrases
- The ceiling (oracle 52/52) is reachable
- The threshold selection rule (max F1) is incompatible with the dynamic range requirement for this fixture
- Wrong executions on no-applicable goals remain a safety concern (8/28 at mean p=0.576)

**Next Steps:** A redesigned threshold selection rule that enforces minimum abstention rates on both classes (e.g., constrained optimization) is needed before a valid test of the dual-class gate architecture can be conducted. The fixture and measurement infrastructure are sound.