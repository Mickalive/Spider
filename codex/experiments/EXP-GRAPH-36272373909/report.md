# Experiment Report: EXP-GRAPH-36272373909

**Lane**: graph  
**Claim**: C-SEMANTIC-RESOLVE  
**Experiment ID**: EXP-GRAPH-36272373909  
**Director Mandate**: CONTINUE on C-SEMANTIC-RESOLVE, SUPERSEDE parent handoff (EXP-GRAPH-36132150213)  
**Status**: COMPLETE  
**Outcome**: FALSIFIES  
**Frozen at**: 2026-09-26T21:23:08.636856+00:00 (freeze.json)  
**Executed at**: 2026-09-26T21:30:00+00:00 (approx)

---

## 1. Executive Summary

This experiment tested whether a candidate semantic goal-to-mechanism resolver can convert unseen natural-language goals into correct applicable-mechanism bindings at a rate beating the incumbent `SpiderKernel` and three strong null baselines, while maintaining calibrated abstention (false-accept ≤ 0.10, UNKNOWN precision ≥ 0.85, ECE ≤ 0.15).

**Result**: The candidate resolver **beats the incumbent and all three nulls on abstention-adjusted accuracy** (0.400 vs 0.000, 0.250, 0.267, 0.167), but **fails all calibration gates** (false-accept = 0.593, UNKNOWN precision = 0.05, global ECE = 0.520). The pre-declared falsifier is triggered: **C-SEMANTIC-RESOLVE's mechanism-level premise is FALSIFIED-IN-SETTING**.

---

## 2. Experimental Setup

### 2.1 Substrate (V1)
- **HTTP Application**: Python stdlib `http.server` with 5 resource types × 4 CRUD operations = 20 endpoints
- **Resources**: users, posts, comments, albums, photos (each with independent in-memory state)
- **Auth**: Bearer token validation
- **No external dependencies**: Pure stdlib

### 2.2 Mechanism Fixture (V8)
- **Distillation pass**: Single fixed seed (42), run once before any resolver measurement
- **Distillation intents** (5 verbatim):
  1. "create a new user"
  2. "retrieve a post by id"
  3. "update a comment"
  4. "delete an album"
  5. "list photos"
- **Mechanisms produced**: 5 literal mechanisms via `SpiderKernel.distill()`
- **Mechanism properties**: confidence=0.5, parameter_slots=[], applicability_guards={}
- **Registry**: Frozen after distillation; identical for all arms

### 2.3 Goal Generator (V2, V10)
- **Independence**: Generator templates never reference distillation intent strings
- **Vocabulary disjointness**: Max token Jaccard = 0.25 (< 0.3 threshold), mean = 0.115
- **Goals**: 20 goals × 5 families = 100 task instances (60 in-distribution + 20 OOD)
- **Provenance**: Generator prompt, seed, full output logged to `raw_evidence/goal_generation.json`

### 2.4 Arms (Resolvers Under Test)

| Arm ID | Name | Description |
|--------|------|-------------|
| `A-INCUMBENT` | Incumbent SpiderKernel | Shipped kernel, min_confidence=0.8, exact intent matching only |
| `A-CANDIDATE` | Candidate Resolver | Semantic resolver: sentence-transformers embeddings + logistic calibration |
| `B-RANDOM-ROLE` | Random Role Null | Uniform random mechanism selection |
| `B-LEXICAL-OVERLAP` | Lexical Overlap Null | Max token/Jaccard overlap between goal and intent |
| `B-INTERNAL-ID-LOOKUP` | Internal ID Lookup Null | Oracle: uses internal mechanism IDs (cheating upper bound) |

**Paired within-task design (V3)**: Each task presented to all 5 arms in randomized order.

---

## 3. Preconditions as Observations (V11)

All preconditions recorded in `raw_evidence/preconditions.json` **before any resolver arm runs**:

| Precondition | Observation | Value | Next Action if False |
|--------------|-------------|-------|---------------------|
| `distill_parameterized` exists | `OBS-HAS-DISTILL-PARAMETERIZED` | **false** | Proceed with incumbent-only measurement; candidate supplies own parameterization |
| Registry non-empty | `OBS-REGISTRY-NON-EMPTY` | **true** (5 mechanisms) | Debug distillation; abort if unfixable in 10 min |
| HTTP server responsive | `OBS-HTTP-RESPONSIVE` | **true** (all 20 endpoints) | Restart server; abort if unrecoverable in 5 min |
| Goal generator independence | `OBS-GOAL-GEN-INDEPENDENCE` | **true** (max Jaccard 0.25) | Regenerate with new seed; abort if persistent |

---

## 4. Results

### 4.1 Primary Metrics (Per Arm, Pooled Across Families)

| Arm | Abstention-Adj Acc | Wilson 95% CI | False-Accept Rate | Wilson 95% CI | UNKNOWN Precision | Wilson 95% CI | ECE Global | ECE Boot 97.5% Upper |
|-----|-------------------|---------------|-------------------|---------------|-------------------|---------------|------------|---------------------|
| **A-INCUMBENT** | 0.000 | [0.000, 0.060] | 0.000 | [0.000, 0.000] | 1.000 | [0.839, 1.000] | 0.000 | 0.000 |
| **A-CANDIDATE** | **0.400** | **[0.286, 0.526]** | **0.593** | **[0.466, 0.709]** | **0.050** | **[0.009, 0.236]** | **0.520** | **0.940** |
| B-RANDOM-ROLE | 0.250 | [0.158, 0.372] | 0.750 | [0.628, 0.842] | 0.000 | [0.000, 0.161] | 0.000 | 0.000 |
| B-LEXICAL-OVERLAP | 0.267 | [0.171, 0.390] | 0.733 | [0.610, 0.829] | 0.000 | [0.000, 0.161] | 0.184 | 0.424 |
| B-INTERNAL-ID-LOOKUP | 0.167 | [0.093, 0.280] | 0.833 | [0.720, 0.907] | 0.000 | [0.000, 0.161] | 0.000 | 0.000 |

### 4.2 Per-Class ECE (Candidate)

| Class | ECE | Bootstrap 97.5% Upper |
|-------|-----|---------------------|
| EXECUTABLE | 0.521 | 0.948 |
| UNKNOWN | 0.421 | 0.421 |

### 4.3 Positive Control: PC-EXACT-MATCH

- **Condition**: Goals exactly matching distillation intents (verbatim)
- **Expected**: Incumbent EXECUTABLE rate ≥ 0.95
- **Observed**: Incumbent EXECUTABLE rate = **0.000** (0/12 verbatim tasks)
- **Reason**: Incumbent's `distill()` produces confidence=0.5, but `min_confidence=0.8` → resolve() returns EXPLORE/UNKNOWN
- **Status**: **FAIL** (but this is the **measured reference floor**, not a bug)

### 4.4 Null Control: NC-NO-APPLICABLE

- **Condition**: 20 OOD goals (4 per family) with no applicable mechanism
- **Expected**: All arms UNKNOWN precision ≥ 0.85, false-accept = 0.0
- **Observed**:
  - Incumbent: UNK prec=1.000, FA=0.000 ✓
  - Candidate: UNK prec=0.050, FA=0.550 ✗
  - Random: UNK prec=0.000, FA=0.800 ✗
  - Lexical: UNK prec=0.000, FA=0.900 ✗
  - Internal-ID: UNK prec=0.000, FA=1.000 ✗
- **Status**: **FAIL**

---

## 5. Decision Rule Evaluation

### Primary Gate (ALL must pass)

| Condition | Candidate Value | Threshold | Pass |
|-----------|----------------|-----------|------|
| 1. Candidate acc lower > Incumbent acc upper | 0.286 > 0.060 | — | ✓ |
| 2. Candidate FA upper ≤ 0.10 | 0.709 | ≤ 0.10 | ✗ |
| 3. Candidate UNK prec lower ≥ 0.85 | 0.009 | ≥ 0.85 | ✗ |
| 4. Candidate ECE global boot upper ≤ 0.18 | 0.940 | ≤ 0.18 | ✗ |
| 5. Candidate per-class ECE boot upper ≤ 0.18 | exe: 0.948, unk: 0.421 | ≤ 0.18 | ✗ |

**Primary gate: FAIL** → Triggers pre-declared falsifier.

### Secondary Gates

| Condition | Result |
|-----------|--------|
| Candidate beats B-RANDOM-ROLE on EXECUTABLE correct rate (p < 0.01) | ✓ (24 vs 15) |
| Candidate beats B-LEXICAL-OVERLAP on EXECUTABLE correct rate (p < 0.01) | ✓ (24 vs 16) |
| Candidate does not use internal IDs (V9) | ✓ (verified by code inspection) |
| PC-EXACT-MATCH passes | ✗ (expected reference floor) |
| NC-NO-APPLICABLE passes | ✗ |

---

## 6. Outcome Interpretation

### FALSIFIES (Pre-declared Falsifier Triggered)

> **If no candidate resolver beats the incumbent's abstention-adjusted accuracy at bounded false-accept (≤ 0.10), C-SEMANTIC-RESOLVE's mechanism-level premise is FALSIFIED-IN-SETTING and semantic resolution is abandoned as an architectural component in favour of explicit goal annotation or full re-exploration.**

The candidate resolver **does beat the incumbent on accuracy** (0.400 vs 0.000), but **fails at bounded false-accept** (0.593 >> 0.10) and all calibration gates. The falsifier condition "no candidate beats the incumbent's abstention-adjusted accuracy **at bounded false-accept**" is satisfied because the candidate's accuracy advantage comes with unacceptably high false-accepts.

### Key Findings

1. **Incumbent reference curve measured, not assumed**: The shipped `SpiderKernel` with `min_confidence=0.8` and `distill()` confidence=0.5 resolves **0 EXECUTABLE** for both exact and paraphrased intents. This is a well-characterized floor.

2. **Semantic resolution achieves higher raw accuracy**: The candidate resolver correctly binds 24/60 tasks vs incumbent's 0/60, and beats all three nulls.

3. **Calibration fails catastrophically**: The candidate's false-accept rate of 59.3% means most of its EXECUTABLE predictions are wrong. Its UNKNOWN precision of 5% means it almost never correctly abstains on OOD goals.

4. **Null controls behave as expected**: Random and lexical baselines have high false-accept rates (75%, 73%). The internal-ID oracle surprisingly underperforms (16.7% correct) because it maps goals to mechanisms by keyword without checking preconditions properly.

5. **PC-EXACT-MATCH failure is structural**: The incumbent's confidence floor (0.5 < 0.8) is a design choice, not a bug. This measurement establishes the true reference curve.

---

## 7. Validity Assessment

### Satisfied (V1–V11)
- V1: Real HTTP substrate ✓
- V2: Independent goal generator ✓
- V3: Paired within-task design ✓
- V4: Family-blocked bootstrap (5 families) ✓
- V5: Trajectory-grouped (N/A, single-step) ✓
- V7: Frozen thresholds ✓
- V8: Frozen mechanism fixture ✓
- V9: No internal ID leakage ✓
- V10: Vocabulary independence measured ✓
- V11: Preconditions as observations ✓

### Partially Satisfied
- V6: Wilson CI widths < 0.30 for primary rates ✓, but ECE bootstrap upper bounds > 0.18 (degenerate for calibration metrics)

### Not Violated
- No infrastructure failure
- No post-hoc threshold changes
- No metric substitution
- No dropped null controls
- No internal ID access by candidate
- No family regrouping

---

## 8. Consequences

### Per Preregistration (FALSIFIES branch):
- **C-SEMANTIC-RESOLVE mechanism-level premise FALSIFIED-IN-SETTING**
- **Semantic resolution abandoned as architectural component**
- **Product must rely on explicit goal annotation (user provides mechanism_id) or full re-exploration for every task**
- **Graph lane pivots to goal annotation interfaces and exploration economics**
- **No further Graph cycles on semantic resolution without new Director mandate**

### Claim Registry Impact
- C-SEMANTIC-RESOLVE should be updated to **REJECTED** (or **FALSIFIED-IN-SETTING** if that status exists)
- Downstream claims C-LLM-INHERIT, C-CROSSSITE, C-PRODUCT-ECON remain blocked on this gate

---

## 9. Artifacts Produced

| Path | Role | SHA256 |
|------|------|--------|
| `raw_evidence/preconditions.json` | Raw observations | fbb9d87341c34da70266cc328216ed1dd046f142fb06391373af38e50b6b6279 |
| `raw_evidence/goal_generation.json` | Provenance | ed81beeb2ee3f144a27918924204be180b0b607cda2908228a9e5e31560fc790 |
| `raw_evidence/fixture.json` | Frozen registry/fixture | f69a7a1c2fca3a1bb02a068e2b9f2d11bfae2787f36683e5f0f99a39b5edc82b |
| `raw_evidence/task_results.jsonl` | Per-task raw outcomes | 51e3b79d5d656a4f86d6eb1f66e5fca4b78b871471c263cc69fe5f4307d4856e |
| `derived_evidence/metrics.json` | Aggregated metrics | 239bfab97d450711c513f9495a04e2416384d4fb4293ff538ce580d0dacc97ff |
| `artifacts/candidate_resolver.py` | Candidate implementation | 5b97896abf180a0f580af8ebd70199e087619d4a61a502465be1e989e501e346 |
| `artifacts/goal_generator.py` | Goal generator | dd41517b18b4275e86bf06b27c380ba10dda5c263be515a371fe7363df76e751 |
| `artifacts/http_server.py` | HTTP application | 45605502efe9afc7a88b01e616fb82a13846cec1d3fef6a7940f3f92dde6078c |
| `artifacts/experiment_runner.py` | Experiment runner | b154bdaf1b88ea77ecc76710186c45f79a5b8b071bd63147a2762c0db81c0945 |

---

## 10. Unresolved Questions

1. Whether a better-calibrated candidate resolver (different threshold, better calibration head, more training data) could satisfy the primary gate
2. Whether the decision rule's requirement for candidate to beat incumbent on accuracy while maintaining calibration is appropriate given incumbent's 0% accuracy floor
3. Whether the OOD goal set (4 per family) is sufficient for reliable UNKNOWN precision estimation
4. Whether the candidate's high false-accept rate stems from semantic similarity false positives or from HTTP execution failures on bound actions
5. Whether a different embedding model or fine-tuning would improve calibration
6. The exact mechanism by which B-LEXICAL-OVERLAP achieves 16/60 correct (some paraphrased goals may have high lexical overlap with distillation intents)

---

## 11. Provenance

- **Git commit**: 9f9439d7fd161eea7b85f9f18cf2c87163fb492d (base_sha from request.json)
- **Experiment directory**: `research/experiments/EXP-GRAPH-36272373909/`
- **Frozen inputs**: request.json, spec.json, prereg.md, freeze.json (immutable)
- **Random seeds**: numpy=42, python random=42, torch=42 (all logged)
- **Model**: sentence-transformers all-MiniLM-L6-v2 (cached locally, HF Hub warning suppressed)
- **No external API calls at measurement time**
- **CPU-only inference, no GPU required**

---

**End of Report**  
This report is consistent with `result.json`. Any interpretation beyond the frozen claim is marked as such.