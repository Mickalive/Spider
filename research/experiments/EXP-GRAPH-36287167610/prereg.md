# Preregistration: EXP-GRAPH-36287167610

**Lane:** graph
**Claim:** C-SEMANTIC-RESOLVE
**Experiment ID:** EXP-GRAPH-36287167610
**Date:** 2026-09-27
**Status:** PREREGISTERED (pre-freeze)

---

## 1. Strategic Context

This experiment is mandated by the Global Research Director (director_mandate.action=CONTINUE, claim_id=C-SEMANTIC-RESOLVE, cognitive_reset=true). It addresses the three critical defects that caused EXP-GRAPH-36279237023 to be MEASUREMENT_INVALID and scientifically inconclusive:

1. **Inert gate**: The fitted applicability gate was trained only on positive-class (applicable) goals, so its p_applicable range [0.6785, 0.9468] never fell below the 0.02 threshold → fired on 0 of 52 applicable goals. All 28 abstentions came from an uncalibrated slot filler. The gate passed its own fittedness test while making zero decisions.

2. **Ambiguous false-accept denominator**: The coded false_accept_rate used reading R4 (all-80 wrong executions over 52 applicable) for the candidate and reading R2 (all-80 over all-80) for every other arm, making cross-arm comparison invalid and the single gate whose verdict was interpretation-dependent.

3. **Safety blind spot**: On 20 no-applicable goals, the candidate executed 11 wrong mechanisms at mean p=0.7787, invisible to every frozen gate because the gate was fitted only on applicable goals and the primary metric used applicable-only denominator.

The parent handoff established that the selection signal is real and separable (embedding route 19/20 vs lexical 15/20 on paraphrase; uncalibrated argmax 45/52; oracle 52/52), but the abstention policy destroyed it. This design implements the exact repairs mandated:

- Applicability gate fitted on **BOTH** positive (applicable) AND negative (no-applicable) classes
- **Single unambiguous pooled false-accept**: wrong EXECUTABLE on ALL goals / total EXECUTABLE
- **Abstention as first-class outcome class** with coverage/selective-risk pair on applicable goals
- Parameter-omitting goals as **declared deferral class** (not errors)
- Lexical-overlap null headroom screen on **applicable goals only**
- Substitute reference arm (B-EMBEDDING-ARGMAX) **declared non-empty by construction**
- Explicit **train/validation/test splits** logged before fitting
- **Code binding via prereg.md-declared SHA256** of pre-existing harness module (freezer hashes prereg.md)
- **Instrument dynamic range precondition**: gate must fire on ≥10% of each class

---

## 2. Hypothesis and Falsifier

**Hypothesis (H1):** An applicability gate fitted on a labelled positive class (applicable goals) AND a negative class (no-applicable goals) will produce non-inert abstention decisions on no-applicable goals, achieve pooled false-accept rate ≤ 0.10 counting wrong EXECUTABLE decisions on ALL goals, and maintain selection accuracy at or above the uncalibrated embedding-argmax reference on the goals it chooses to answer (coverage/selective-risk pair), thereby demonstrating that goals can be routed to applicable mechanisms without internal IDs and with calibrated safety.

**Falsifier (F1):** The fitted resolver fails to exceed the lexical-overlap null on mechanism-identity binding accuracy with paired family-blocked uncertainty on applicable goals, OR the pooled false-accept rate (wrong EXECUTABLE on ALL goals including no-applicable) exceeds 0.10, OR the coverage/selective-risk pair falls below the embedding-argmax reference on answered applicable goals, OR the calibration gate is inert (fires on 0 of applicable goals at its selected threshold), OR UNKNOWN precision falls below 0.85, OR global ECE exceeds 0.15 (bootstrap upper > 0.18), OR per-class ECE exceeds 0.15 (bootstrap upper > 0.18), OR the calibration is not fitted (parameters fixed algebraic transform).

---

## 3. Fixture Specification

### 3.1 HTTP Application (stdlib-only)

- **Server:** Python `http.server` with custom request handler (no external frameworks)
- **Endpoints:** 20 REST endpoints across 5 resource families × 4 verbs (CREATE/READ/UPDATE/DELETE)
- **Resource Families:** `users`, `posts`, `comments`, `albums`, `photos`
- **State:** In-memory dictionaries per resource family, fully reset per task
- **Persistence:** None (ephemeral per-task state)
- **Port:** Dynamically allocated (logged)
- **Concurrency:** Single-threaded, sequential request handling

### 3.2 Mechanism Registry

- **Total mechanisms:** 20 (4 per resource family: CREATE, READ, UPDATE, DELETE)
- **Parameter slots:** Every mechanism has non-empty `parameter_slots` list (e.g., `["user_id"]`, `["post_id", "title", "body"]`)
- **Action templates:** All templates executable with bound parameters. **Zero** unbindable `${...}` placeholders.
- **Intent strings:** Natural-language descriptions used for distillation (e.g., "create a new user", "retrieve a post by id", "update a comment", "delete an album")
- **Mechanism IDs:** Stable identifiers `mech_{family}_{verb}` (e.g., `mech_users_create`)
- **Roles:** Each mechanism tagged with role ∈ {create, read, update, delete}

### 3.3 Goal Set (frozen before freeze, machine-derived counts)

Goals are generated by a deterministic, seeded goal generator. The complete goal list with target mechanism_ids and category labels is hashed into `freeze.json` via prereg.md declaration.

| Category | Count | Description | Applicable? |
|----------|-------|-------------|-------------|
| verbatim | 12 | Exact copies of distillation intents (subset, for PC) | Yes |
| paraphrased | 20 | Natural-language paraphrases, unseen wording | Yes |
| underspecified | 10 | Goals missing required parameters (deferral class) | Yes* |
| composite | 10 | Goals combining multiple operations | Yes |
| no_applicable | 20 | Goals targeting operations/families not in registry | **No** |
| ood_paraphrase | 8 | Paraphrases of non-registry operations | **No** |

**Total goals:** 80
**Applicable goals (machine-derived):** 52 (12 verbatim + 20 paraphrased + 10 underspecified + 10 composite)
**No-applicable goals (machine-derived):** 28 (20 no_applicable + 8 ood_paraphrase)

*The 10 underspecified goals ARE applicable (a mechanism exists) but omit required parameters. They are analysed as a declared **deferral class** — abstention on these is scored as DEFER, not error, and they are excluded from the primary mechanism-identity accuracy denominator but included in coverage/selective-risk analysis as a separate stratum.

The goal generator uses disjoint templates from the distillation intents. Overlap statistic (max token Jaccard per-goal vs own family target) < 0.3 verified and logged as OBS-GOAL-GEN-INDEPENDENCE.

### 3.4 Embedding Model

- **Model:** `sentence-transformers/all-MiniLM-L6-v2` (cached locally)
- **Revision:** Pinned to specific commit hash (recorded in freeze.json via prereg.md declaration)
- **Use:** Cosine similarity between goal embedding and mechanism intent embeddings

### 3.5 Train/Validation/Test Splits (explicit, frozen)

Applicable goals (52) split by resource family (stratified):
- **Train:** 32 goals (60%) — used for fitting logistic regression
- **Validation:** 10 goals (20%) — used for threshold selection (optimize F1 on applicable goals)
- **Test:** 10 goals (20%) — held out for final reporting only

No-applicable goals (28) split:
- **Train:** 17 goals (60%) — used as negative class for fitting
- **Validation:** 5 goals (20%) — used for threshold selection
- **Test:** 6 goals (20%) — held out

Splits use fixed seeds (goal_split=990017) and are logged before any fitting. No data leakage across splits.

---

## 4. Arms

### 4.1 A-CANDIDATE (Dual-Class Fitted Applicability Gate Resolver)

**Architecture:**
1. **Scoring:** Cosine similarity between goal embedding and each mechanism's intent embedding → `cos_sim ∈ [-1, 1]`
2. **Applicability Gate:** Fitted logistic regression `p_applicable = 1 / (1 + exp(-(w * cos_sim + b)))`
   - Training data: Train split of applicable goals (label=1) + Train split of no-applicable goals (label=0)
   - Features: max cos_sim per goal
   - Parameters `w`, `b` learned via maximum likelihood on combined train set
   - **Not** a fixed algebraic transform — verified by parameter variation across seeds
   - Fitted parameters logged and **declared in prereg.md with SHA256**
3. **Decision Rule:**
   - If `max(p_applicable) < threshold` → ABSTAIN (outcome class: UNKNOWN)
   - Else → select mechanism with highest `p_applicable` → EXECUTABLE
   - Threshold chosen on validation split to optimize F1 (applicable vs no-applicable classification)
   - Threshold logged and frozen
4. **Parameter Binding:** Selected mechanism's `parameter_slots` bound from goal via slot-filling heuristic (keyword/entity extraction). All slots filled → EXECUTABLE. Any unfilled → DEFER (outcome class: DEFER, distinct from UNKNOWN).
5. **Output per goal:** `mechanism_id`, `resolution_status` (EXECUTABLE/ABSTAIN/DEFER/EXPLORE), `p_applicable`, `bound_parameters`, `confidence`, `outcome_class` (EXECUTABLE/UNKNOWN/DEFER)

**Key design:** The gate sees BOTH classes during fitting. The threshold is selected to balance precision/recall on the validation split. The instrument dynamic range check (V13) verifies the gate actually fires on both classes before main evaluation.

### 4.2 B-LEXICAL-OVERLAP (Null Baseline)

- **Algorithm:** Max token Jaccard similarity between goal tokens and mechanism intent tokens
- **Selection:** Mechanism with highest Jaccard; ties broken by mechanism_id lexical order
- **Abstention:** Never abstains (always produces EXECUTABLE)
- **Output:** `mechanism_id`, `resolution_status=EXECUTABLE`, `outcome_class=EXECUTABLE`

### 4.3 B-RANDOM-ROLE (Null Baseline)

- **Algorithm:** Infer role (CREATE/READ/UPDATE/DELETE) from goal keywords; select uniformly from mechanisms with matching role
- **Abstention:** Never abstains
- **Output:** `mechanism_id`, `resolution_status=EXECUTABLE`, `outcome_class=EXECUTABLE`

### 4.4 B-EMBEDDING-ARGMAX (Substitute Reference Arm — Declared Non-Empty)

- **Algorithm:** Select mechanism with highest cosine similarity (raw embedding argmax)
- **Abstention:** Never abstains → **always EXECUTABLE by construction**
- **Declared non-empty:** This arm produces EXECUTABLE on 100% of applicable goals by design (max cos_sim always exists). Serves as the reference for coverage/selective-risk comparison.
- **Output:** `mechanism_id`, `resolution_status=EXECUTABLE`, `outcome_class=EXECUTABLE`

### 4.5 B-INTERNAL-ID-ORACLE (Oracle / Difficulty Ceiling)

- **Input:** Receives true `mechanism_id` for each goal
- **Behavior:** Returns the exact target mechanism
- **Expected accuracy:** 1.0 on applicable goals by construction
- **Declared ceiling:** If < 1.0 on applicable goals → fixture defective → MEASUREMENT_INVALID

### 4.6 PC-VERBATIM-INTENT (Positive Control)

- **Goals:** The 12 verbatim goals (exact distillation intents)
- **Expected:** Mechanism-identity accuracy = 1.0, false_accept = 0.0, UNKNOWN precision = 1.0, ECE = 0.0
- **Denominator:** Must be > 0 (explicitly 12); logged and reported
- **Failure → MEASUREMENT_INVALID**

### 4.7 NC-NO-APPLICABLE (Null Control)

- **Goals:** The 28 no-applicable goals (20 no_applicable + 8 ood_paraphrase)
- **Expected:** Abstention rate = 1.0 on no-applicable goals, UNKNOWN precision = 1.0 (vacuous), false_accept = 0.0
- **Denominator:** Must be > 0 (explicitly 28); logged and reported
- **Failure → MEASUREMENT_INVALID**

---

## 5. Execution Protocol

### 5.1 Task Structure

Each task = one goal. All 7 arms execute on each goal in randomized order (minimum 43 distinct orderings across 80 tasks, target 78+).

### 5.2 Per-Task State Reset (V7)

Before each task:
1. Server state dictionaries cleared and re-initialized
2. State hash = SHA256(JSON serialization of all server state) computed and logged
3. All arms execute against this identical starting state

### 5.3 Degeneracy Screen (V8) — Runs BEFORE Any Candidate Arm

Before A-CANDIDATE runs on any goal:
1. Run B-LEXICAL-OVERLAP on all 52 applicable goals → compute mechanism-identity accuracy
2. Run B-EMBEDDING-ARGMAX on all 52 applicable goals → count EXECUTABLE decisions
3. **Screen PASS conditions (both required):**
   - (a) B-LEXICAL-OVERLAP accuracy on applicable goals < 0.90 (headroom threshold)
   - (b) B-EMBEDDING-ARGMAX EXECUTABLE count on applicable goals > 0
4. If either FAILS → experiment halts, status = MEASUREMENT_INVALID, logged with full screen output

### 5.4 Calibration Fitting (V4)

Before main evaluation:
1. Combine train splits: 32 applicable (label=1) + 17 no-applicable (label=0) = 49 training goals
2. Fit logistic regression: `p_applicable ~ max_cos_sim` with labels
3. Select threshold on validation split (10 applicable + 5 no-applicable) to optimize F1
4. Log fitted `w`, `b`, threshold, validation metrics (accuracy, precision, recall, F1 per class)
5. **Instrument Dynamic Range Check (V13):** Apply fitted gate to validation split. Verify:
   - Gate abstains on ≥10% of applicable validation goals
   - Gate abstains on ≥10% of no-applicable validation goals
   - If either fails → MEASUREMENT_INVALID (gate is inert on that class)
6. Freeze parameters (declared in prereg.md with SHA256)

### 5.5 Code Binding (V9)

The following modules exist under `research/harness/` (allowed code root for graph lane) **before freeze**:
- `harness/candidate_resolver.py`
- `harness/goal_generator.py`
- `harness/http_server.py`
- `harness/experiment_runner.py`

Their SHA256 digests are **declared in this prereg.md** (Section 9). The freezer hashes `prereg.md`, binding code transitively. EXECUTE recomputes digests at runtime and fails measurement validity on any mismatch.

---

## 6. Metrics (Stable Identities)

### 6.1 Primary Metric

- **mechanism_identity_accuracy_applicable:** Fraction of **applicable** goals where `selected_mechanism_id == target_mechanism_id`
- **Unit:** Proportion [0,1]
- **Comparison:** Paired family-blocked bootstrap (10,000 resamples) against B-LEXICAL-OVERLAP and B-RANDOM-ROLE
- **Blocking unit:** Resource family (goals sharing a family resampled together)

### 6.2 Secondary Metrics

| Metric ID | Definition | Threshold |
|-----------|------------|-----------|
| `pooled_false_accept_rate` | Wrong EXECUTABLE decisions / total EXECUTABLE decisions, pooled across **ALL 80 goals** (applicable + no-applicable). Numerator: EXECUTABLE where `selected != target` (for no-applicable, any EXECUTABLE is wrong). Denominator: total EXECUTABLE count. | ≤ 0.10 |
| `coverage` | Fraction of **applicable** goals where A-CANDIDATE produces EXECUTABLE decision | ≥ 0.50 |
| `selective_risk` | Error rate on applicable goals where A-CANDIDATE produces EXECUTABLE | ≤ (embedding_argmax selective risk on its answered applicable) + 0.05 |
| `unknown_precision` | TP_abstain / (TP_abstain + FP_abstain) where TP_abstain = no-mechanism-applies AND abstain (UNKNOWN), FP_abstain = mechanism-applies AND abstain (UNKNOWN) | ≥ 0.85 |
| `ece_global` | Expected Calibration Error, 10 equal-mass bins, **closed top bin [0.9, 1.0]**, no rows dropped | ≤ 0.15 (bootstrap upper ≤ 0.18) |
| `ece_per_class_max` | Max ECE across resolution status classes (EXECUTABLE, UNKNOWN), same estimator | ≤ 0.15 (bootstrap upper ≤ 0.18) |
| `calibration_is_fitted` | Boolean: calibration parameters learned on held-out validation with both classes | = true |
| `degeneracy_screen_pass` | Boolean: both screen conditions PASS | = true |
| `pc_verbatim_accuracy` | Mechanism-identity accuracy on verbatim goals | = 1.0 (denom > 0) |
| `oracle_accuracy` | Mechanism-identity accuracy of B-INTERNAL-ID-ORACLE on applicable | = 1.0 |
| `nc_abstention_rate` | Abstention rate on no-applicable goals | = 1.0 (denom > 0) |
| `gate_fires_on_both_classes` | Fitted gate abstains on ≥10% of applicable AND ≥10% of no-applicable (validation split) | both ≥ 0.10 |

### 6.3 Deferral Class Analysis (Underspecified Goals)

The 10 underspecified goals are reported as a separate **deferral stratum**:
- DEFER rate on underspecified goals
- Mechanism-identity accuracy on underspecified goals that are EXECUTABLE
- Not included in primary accuracy denominator (52 applicable = 12 verbatim + 20 paraphrased + 10 composite)
- Not counted as errors in any gate

---

## 7. Decision Rule (Frozen)

### 7.1 Gate Evaluation Order

1. **Measurement Validity (V1-V13):** Any FAIL → MEASUREMENT_INVALID
2. **Degeneracy Screen (V8):** FAIL → MEASUREMENT_INVALID
3. **Positive Control (PC-VERBATIM-INTENT):** FAIL or denom=0 → MEASUREMENT_INVALID
4. **Oracle Ceiling (B-INTERNAL-ID-ORACLE):** accuracy < 1.0 on applicable → MEASUREMENT_INVALID
5. **Null Control (NC-NO-APPLICABLE):** FAIL or denom=0 → MEASUREMENT_INVALID
6. **Calibration Fitted Check (V4):** FAIL → MEASUREMENT_INVALID
7. **Instrument Dynamic Range (V13):** FAIL → MEASUREMENT_INVALID
8. **Primary Gate:** A-CANDIDATE mechanism_identity_accuracy_applicable > B-LEXICAL-OVERLAP AND > B-RANDOM-ROLE (paired family-blocked bootstrap, α=0.05, one-sided)
9. **Secondary Gates:** All must PASS (pooled_false_accept, coverage_selective_risk, unknown_precision, ece_global, ece_per_class_max)

### 7.2 Outcomes

| Outcome | Conditions |
|---------|------------|
| **SUPPORTS** | All gates 1-9 PASS |
| **FALSIFIES** | Primary gate (8) FAILS OR any secondary gate (9) FAILS |
| **MEASUREMENT_INVALID** | Any gate 1-7 FAILS |

**Note:** A valid FALSIFIES (status=COMPLETE, outcome=FALSIFIES) is a scientific result that bounds the dual-class resolver architecture. MEASUREMENT_INVALID means the experiment failed to validly test the hypothesis.

---

## 8. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Construct validity: metric doesn't measure resolution | V1: Primary = mechanism-identity binding on applicable. Pooled false-accept on ALL goals. Coverage/selective-risk on answered applicable. |
| Gate inert on negative class | V4+V13: Dual-class fitting + instrument dynamic range check before main evaluation |
| False-accept denominator ambiguity | Single unambiguous definition: wrong EXECUTABLE on ALL goals / total EXECUTABLE |
| Positive control unmeasured | V2: PC-VERBATIM-INTENT runs on all 12 verbatim; denominator logged |
| Oracle not a true ceiling | V3: Oracle receives mechanism_id; must achieve 1.0 on applicable |
| Calibration algebraic, not fitted | V4: Logistic regression on held-out validation with both classes; parameters vary across seeds |
| ECE half-open bin defect | V5: Closed top bin [0.9, 1.0] inclusive; 10 equal-mass bins |
| UNKNOWN precision misdefined | V6: Explicit TP/FP definition; NOT OOD abstention rate |
| Shared server state confound | V7: Per-task reset + state hash logged |
| Fixture non-discriminating | V8: Degeneracy screen on applicable goals only; reference arm declared non-empty |
| Code not bound to freeze | V9: SHA256 of pre-existing harness modules declared in prereg.md (freezer hashes prereg.md) |
| Uncertainty ignores family clustering | V10: Paired bootstrap with family as blocking unit |
| Fixture too easy (1 mech/family) | V11: 4 mechanisms/family, all verbs, all slots bound, zero unbindable placeholders |
| Embedding model drift | Model revision hash pinned and declared in prereg.md |
| Goal independence from intents | Disjoint templates; overlap < 0.3 verified (OBS-GOAL-GEN-INDEPENDENCE) |
| Data leakage across splits | V12: Splits fixed by seed, logged before fitting, no cross-contamination |
| Deferral class confused with errors | Underspecified goals explicitly stratified, scored as DEFER, excluded from primary denominator |

---

## 9. Artifacts to Preserve (Declared in prereg.md for Freeze Binding)

The following modules exist under `research/harness/` **before freeze**. Their SHA256 digests are declared here and bound transitively via `freeze.json` hashing `prereg.md`:

| Module | Declared SHA256 (to be filled at freeze time) |
|--------|-----------------------------------------------|
| `harness/candidate_resolver.py` | `[FILLED_AT_FREEZE]` |
| `harness/goal_generator.py` | `[FILLED_AT_FREEZE]` |
| `harness/http_server.py` | `[FILLED_AT_FREEZE]` |
| `harness/experiment_runner.py` | `[FILLED_AT_FREEZE]` |

The following data artifacts are generated and hashed into `freeze.json` via prereg.md declaration:
- `fixture.json` — Complete mechanism registry (20 mechanisms, intents, parameter_slots, action_templates, roles)
- `goals.json` — Frozen goal list (80 goals with target mechanism_ids, categories, applicable/no-applicable labels)

EXECUTE recomputes all SHA256 values and fails measurement validity on any mismatch.

---

## 10. Preconditions (Recorded as Observations, Not Blocking)

Per AGENTS.md and parent handoff, the following are recorded as observations (OBS-*) before arm execution:

- OBS-GOAL-GEN-INDEPENDENCE: Max token Jaccard per-goal vs own family target < 0.3
- OBS-FIXTURE-DISCRIMINATION: Registry has >1 mech/family, all slots bound, all templates executable
- OBS-CALIBRATION-FITTED: Calibration parameters learned on dual-class train split, not fixed
- OBS-CODE-BOUND: All outcome-bearing code SHA256 declared in prereg.md
- OBS-SPLITS-EXPLICIT: Train/validation/test splits logged with counts per class before fitting
- OBS-DYNAMIC-RANGE: Fitted gate fires on ≥10% of each class on validation split

If any OBS fails, it is logged but does not trigger MEASUREMENT_INVALID (the measurement validity conditions V1-V13 are the gates).

---

## 11. Smallest Next Actions if MEASUREMENT_INVALID

| Failure Mode | Smallest Next Action |
|--------------|---------------------|
| Degeneracy screen FAILS (lexical ≥ 0.90 on applicable) | Increase fixture difficulty: more mechanisms/family, harder paraphrases, different embedding |
| Degeneracy screen FAILS (reference arm empty) | B-EMBEDDING-ARGMAX is non-empty by construction; failure indicates code defect → fix harness |
| Oracle accuracy < 1.0 | Fix fixture: ensure mechanism_id mapping correct and complete |
| Calibration not fitted | Implement logistic regression; verify parameters change across seeds |
| Instrument dynamic range FAILS (gate inert) | Redesign gate: different features (e.g., cos_sim + entropy), different model class, more negative samples |
| Code hash mismatch | Ensure harness modules are stable before freeze; no edits after prereg.md declares digests |
| Per-task state hash missing | Add state serialization and hashing to http_server.py reset method |
| UNKNOWN precision < 0.85 | Strengthen negative class representation; add more no-applicable goal diversity |

---

## 12. No-Go Rules (Do Not Weaken After Seeing Outcomes)

- Do not change primary metric from mechanism-identity binding on applicable goals
- Do not substitute pooled false-accept with applicable-only false-accept
- Do not substitute UNKNOWN precision with OOD abstention rate
- Do not use half-open ECE bins
- Do not weaken headroom threshold from 0.90 on applicable goals
- Do not remove family blocking from bootstrap
- Do not drop PC-VERBATIM-INTENT or NC-NO-APPLICABLE denominators
- Do not accept algebraic calibration as "fitted"
- Do not run candidate arms if degeneracy screen fails
- Do not edit frozen files after freeze.json exists
- Do not change coverage minimum from 0.50
- Do not change selective risk margin from +0.05 vs embedding-argmax reference
- Do not merge DEFER class into error or abstention classes
- Do not move no-applicable goals into applicable denominator

---

## 13. Provenance Requirements

- Git commit hash of all code at freeze time
- Python version, sentence-transformers version, torch version
- Model revision hash (all-MiniLM-L6-v2)
- Random seeds for: goal generation (36287167610), arm ordering (20260927), split (990017), bootstrap (36287167610)
- SHA256 of all modules declared in Section 9
- SHA256 of fixture.json and goals.json

---

## 14. Freeze Checklist (Before freeze.json Created)

- [ ] spec.json matches this prereg.md exactly
- [ ] All harness modules exist under research/harness/ and are stable
- [ ] SHA256 of all harness modules computed and declared in Section 9
- [ ] Goal set frozen (goals.json) with target mechanism_ids, categories, applicable labels
- [ ] Fixture frozen (fixture.json) with 20 mechanisms, all slots bound, all templates executable
- [ ] Degeneracy screen code implemented and tested in isolation (applicable-only headroom)
- [ ] Calibration fitting code implemented and tested in isolation (dual-class, threshold selection)
- [ ] ECE estimator uses closed top bin (verified by unit test)
- [ ] UNKNOWN precision uses TP/FP definition (verified by unit test)
- [ ] Per-task state reset + hash logging implemented
- [ ] Instrument dynamic range check implemented (V13)
- [ ] Pooled false-accept computation implemented (ALL goals denominator)
- [ ] Coverage/selective-risk computation implemented (applicable answered only)
- [ ] Deferral class (underspecified) handled as separate stratum
- [ ] No outcome data has been inspected

---

## 15. Declaration

This preregistration is complete and frozen prior to any outcome-bearing execution. All design choices, thresholds, and decision rules are declared above. No modifications will be made after freeze.json is created.

**Frozen by:** [Deterministic freezer at freeze time]
**Freeze timestamp:** [To be recorded in freeze.json]