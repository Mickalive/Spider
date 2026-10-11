# Preregistration: EXP-GRAPH-38116418896

## 1. Experiment Identity

- **experiment_id**: EXP-GRAPH-38116418896
- **lane**: graph
- **claim_ids**: ["C-SEMANTIC-RESOLVE"]
- **design_contract_version**: 2
- **director_mandate**: CONTINUE on C-SEMANTIC-RESOLVE with cognitive_reset=true, parent_handoff_disposition=SUPERSEDE
- **target_claim**: C-SEMANTIC-RESOLVE (current effective status: HYPOTHESIS per codex/claim_state.json)

## 2. Scientific Question

Does max-cosine-similarity selection over sentence-transformer embeddings (all-MiniLM-L6-v2) with a fitted logistic regression calibration gate achieve mechanism-identity binding accuracy strictly above a token-overlap null on **independently authored goals**, with calibrated abstention meeting:
- UNKNOWN precision ≥ 0.85 (Wilson lower bound)
- Pooled false-accept rate ≤ 0.10 (Wilson upper bound)
- Global ECE ≤ 0.15 (bootstrap 95% upper bound ≤ 0.18)

...or was the prior bounded advantage (45/52 vs 33/52, paired family-blocked difference 0.2308, 95% CI [0.1136, 0.3509]) an artifact of joint authorship (intents and goal templates authored in the same execute-time file by the same agent)?

## 3. Hypothesis

**H1 (Primary)**: Candidate resolver (all-MiniLM-L6-v2 embeddings + fitted logistic regression gate) achieves mechanism-identity accuracy on applicable goals > B-LEXICAL-OVERLAP, with paired family-blocked bootstrap one-sided 95% lower bound > 0.

**H2 (Calibration)**: Candidate achieves UNKNOWN precision ≥ 0.85, pooled false-accept ≤ 0.10, global ECE bootstrap 95% upper ≤ 0.18.

**H3 (Controls)**: All controls pass: PC-VERBATIM-INTENT (1.0 on verbatim), NC-NO-APPLICABLE (1.0 abstention on no-applicable), B-INTERNAL-ID-ORACLE (1.0 on applicable), B-RANDOM-ROLE (candidate > chance).

**H4 (Reference)**: A-REFERENCE-DISTINCT-EMBEDDING (all-mpnet-base-v2 + independent gate) provides architecturally distinct comparison; its performance relative to candidate informs whether embedding model choice drives the effect.

## 4. Falsifier

The hypothesis is falsified if **any** of the following occurs (all measured on the frozen test split after calibration):

1. Candidate mechanism-identity accuracy on applicable goals does not exceed B-LEXICAL-OVERLAP by a paired family-blocked bootstrap one-sided 95% lower bound > 0.
2. Candidate pooled false-accept rate > 0.10 (Wilson upper bound).
3. Candidate UNKNOWN precision < 0.85 (Wilson lower bound).
4. Candidate global ECE bootstrap 95% upper bound > 0.18.
5. Candidate fails to exceed B-RANDOM-ROLE on applicable goals.
6. PC-VERBATIM-INTENT fails (accuracy < 1.0 on verbatim goals, denominator > 0).
7. B-INTERNAL-ID-ORACLE < 1.0 on applicable goals (denominator > 0).
8. Contamination screen detects max token Jaccard ≥ 0.3 between any goal and any non-target-family intent.
9. A-REFERENCE-DISTINCT-EMBEDDING achieves equal or higher primary metric than candidate on applicable goals.

## 5. Substrate and Fixture

### 5.1 HTTP Application (stdlib-only)
- **File**: `artifacts/http_server.py`
- **Endpoints**: 20 (5 resource families × 4 CRUD verbs)
- **Families**: users, posts, comments, albums, photos
- **Verbs**: create (POST), read (GET), update (PUT), delete (DELETE)
- **State**: In-memory JSON store, reset to identical hash before every arm request
- **Port**: 8765 (localhost)
- **No external dependencies**: Pure Python stdlib (`http.server`, `json`, `uuid`, `urllib.parse`)

### 5.2 Mechanism Registry (Fixture)
- **File**: `artifacts/fixture_def.py` → produces `fixture.json`
- **20 mechanisms**: One per (family, verb) combination
- **Each mechanism contains**:
  - `mechanism_id`: e.g., "mech_users_create"
  - `intent`: Natural language description, e.g., "Create a new user account with the provided details"
  - `parameter_slots`: Non-empty list of required parameters (e.g., ["name", "email"])
  - `action_template`: HTTP request template with slot placeholders
  - `postconditions`: Expected response status and body structure
  - `confidence`: 0.9 (above min_confidence=0.8 threshold)
  - `applicability_guards`: Conditions for when mechanism applies
- **Verification (V10)**: All 20 mechanisms have distinct intents, non-empty parameter_slots, executable templates; verified before evaluation.

### 5.3 Goal Set
- **File**: `artifacts/goal_generator.py` → produces `goals.json` + `authoring_provenance.json`
- **80 goals total**: 16 per family (5 families × 16), all goals assigned to a family for family-blocked bootstrap
- **Per family (16 goals total)**: ~10-11 applicable, ~5-6 no-applicable (exact counts vary by family, summing to 52 applicable / 28 no-applicable overall)
- **Applicable goals (52 total, distributed across families)**:
  - 12 verbatim: Exact string match to mechanism intent (~2-3 per family)
  - 20 paraphrased: Semantic paraphrase, same target mechanism (~4 per family)
  - 10 underspecified: Missing parameter information, should abstain or defer (~2 per family)
  - 10 composite: Require multi-step or combined mechanisms (~2 per family)
- **No-applicable goals (28 total, distributed across families)**:
  - 8 no_applicable: Goals with no matching mechanism in registry
  - 20 OOD (out-of-distribution): Goals from unrelated domains (e.g., "translate this text", "calculate fibonacci")
- **All 80 goals** have a `family` field for bootstrap blocking and a `category` field (verbatim/paraphrased/underspecified/composite/no_applicable/OOD).

### 5.4 Independent Goal Authoring (V2)
**Critical design requirement**: The goal generator process **never receives mechanism intent strings**.
- Goal generator knows only: HTTP endpoint structure (verb, path, parameters), resource family names, and parameter schemas.
- Goal generator does **not** receive: mechanism `intent` strings, `applicability_guards`, or any semantic descriptions from distillation.
- **Provenance record** (`authoring_provenance.json`) frozen **before any resolver arm runs**, containing:
  - `goal_generator_code_sha256`: Hash of `goal_generator.py` at generation time
  - `timestamp_utc`: ISO 8601 timestamp
  - `goals_json_sha256`: Hash of generated `goals.json`
  - `fixture_json_sha256`: Hash of `fixture.json` (for identity continuity)
  - `generation_metadata`: {"families": 5, "goals_per_family": 16, "split_strategy": "family_blocked"}

### 5.5 Contamination Screen (V3)
**Before any arm runs**, compute for every goal:
- Token Jaccard similarity against **ALL 20 registry intents** (not just target family)
- Record max_overlap_all_intents, max_overlap_target_family, max_overlap_non_target_families
- **Pass criterion**: max_overlap_non_target_families < 0.3 for all 80 goals
- Output logged to `raw_evidence/contamination_screen.jsonl` with per-goal records

### 5.6 Splits (Family-Blocked)
- **Calibration split** (used for gate fitting + dynamic range verification): 42 goals (stratified by family, 8-9 per family)
- **Validation split** (used for gate threshold selection + non-inert check): 10 goals (2 per family)
- **Test split** (used for final evaluation): 28 goals (remainder, ~5-6 per family)
- **All splits logged** in `derived_evidence/split_manifest.json` before any arm runs on test split.

## 6. Arms (Resolvers)

### 6.1 A-CANDIDATE (Treatment)
- **File**: `artifacts/candidate_resolver.py`
- **Embedding model**: `sentence-transformers/all-MiniLM-L6-v2` (cached locally, no external API)
- **Similarity**: Cosine similarity between goal embedding and each mechanism intent embedding
- **Selection**: argmax over cosine similarities
- **Calibration gate**: Logistic regression (sklearn, penalty=None, solver=lbfgs, max_iter=5000) fitted on **calibration split** (held-out), predicting `is_correct` from `cosine_similarity`
- **Threshold**: Selected on **validation split** to achieve target coverage; applied to test split
- **Abstention**: When fitted `p_applicable < threshold` → abstain (scored as own class DEFER)
- **Parameter binding**: Fill template slots from goal parameters; abstain if slots unfilled (unfilled_parameter_slots)

### 6.2 A-REFERENCE-DISTINCT-EMBEDDING (Reference Comparison)
- **File**: `artifacts/reference_resolver.py`
- **Embedding model**: `sentence-transformers/all-mpnet-base-v2` (**different model**, provably architecturally distinct)
- **Similarity**: Cosine similarity
- **Calibration gate**: Independent logistic regression fitted on **same calibration split** (separate fit)
- **Threshold**: Selected on **same validation split** (independent selection)
- **Abstention**: Same logic as candidate
- **Declared non-empty leg (V11)**: Must achieve `executable_count == n_applicable` on test split at its operating threshold. Verified before candidate runs on test.

### 6.3 B-LEXICAL-OVERLAP (Strong Null)
- **File**: `artifacts/null_resolvers.py` (class `LexicalOverlapResolver`)
- **Similarity**: Token Jaccard between goal text and mechanism intent strings
- **Selection**: argmax over Jaccard scores
- **Abstention**: Never abstains (always returns EXECUTABLE)
- **No calibration**: Raw similarity scores

### 6.4 B-RANDOM-ROLE (Null Control)
- **File**: `artifacts/null_resolvers.py` (class `RandomRoleResolver`)
- **Role inference**: Keyword matching on goal text → family (users/posts/comments/albums/photos)
- **Selection**: Uniform random among mechanisms in inferred family
- **Abstention**: Abstains if no keyword matches any family

### 6.5 B-INTERNAL-ID-ORACLE (Oracle Ceiling)
- **File**: `artifacts/null_resolvers.py` (class `InternalIdOracleResolver`)
- **Selection**: Exact `mechanism_id` match to goal's `target_mechanism_id`
- **Abstention**: Abstains on no-applicable goals (no target mechanism)

### 6.6 PC-VERBATIM-INTENT (Positive Control)
- **Not a separate arm**: Evaluated as **A-CANDIDATE on verbatim goals only** (12 goals per family-blocked test split)
- **Expected**: 1.0 accuracy, 0.0 false-accept, 1.0 UNKNOWN precision, ECE=0.0
- **Failure → MEASUREMENT_INVALID**

## 7. Measurement Validity Gates (V1–V13)

| Gate | Description | Pass Criterion | Failure Consequence |
|------|-------------|----------------|---------------------|
| V1 | Construct validity: primary metric = mechanism-identity binding | Primary metric defined as `selected_mechanism_id == target_mechanism_id` on applicable goals | MEASUREMENT_INVALID |
| V2 | Independent goal authoring | `authoring_provenance.json` exists with code hash + timestamp frozen before arms run; max goal-vs-intent Jaccard < 0.3 | MEASUREMENT_INVALID |
| V3 | Contamination screen | max_overlap_non_target_families < 0.3 for all 80 goals | MEASUREMENT_INVALID |
| V4 | Paired design + family-blocked bootstrap | All arms run per task in randomized order; bootstrap blocks = 5 families | MEASUREMENT_INVALID |
| V5 | Per-task state reset | Single identical state hash across all 80 tasks × 6 arms | MEASUREMENT_INVALID |
| V6 | Calibration gate non-inert | Gate fires on > 0 applicable validation goals (fitted p < threshold for ≥1) | MEASUREMENT_INVALID |
| V7 | Closed top-bin ECE | 10 equal-mass bins, top bin [0.9, 1.0] inclusive, 0 rows dropped | MEASUREMENT_INVALID |
| V8 | UNKNOWN precision defined | TP_abstain = no-mechanism AND abstain; FP_abstain = mechanism AND abstain | MEASUREMENT_INVALID |
| V9 | Code hashed into freeze | All files in `freeze_artifacts` hashed into `freeze.json.artifact_hashes`; verified at execution start | MEASUREMENT_INVALID |
| V10 | Fixture discrimination | 20 mechanisms, all distinct intents, non-empty slots, executable templates | MEASUREMENT_INVALID |
| V11 | Degeneracy screen | B-LEXICAL-OVERLAP applicable_accuracy < 0.90; A-REFERENCE-DISTINCT-EMBEDDING executable_count == n_applicable | MEASUREMENT_INVALID |
| V12 | Authoring provenance | `authoring_provenance.json` immutable, recorded before any arm runs | MEASUREMENT_INVALID |
| V13 | Dynamic range controls | Control arms collectively span non-degenerate range on calibration split (min_across_arms < max_across_arms on primary metric) | MEASUREMENT_INVALID |

**Gate evaluation order**: V1–V13 (all must PASS) → V11 → PC-VERBATIM-INTENT → B-INTERNAL-ID-ORACLE → NC-NO-APPLICABLE → V13 → V6 → Primary → Secondary

Any failure in V1–V13, V11, PC-VERBATIM-INTENT, B-INTERNAL-ID-ORACLE, NC-NO-APPLICABLE, V13, or V6 → **MEASUREMENT_INVALID** (short-circuit).

## 8. Primary Metric

- **Name**: `mechanism_identity_accuracy`
- **Definition**: Proportion of applicable goals (n=52 on full set, n_test on test split) where `selected_mechanism_id == target_mechanism_id`
- **Abstention scoring**: An abstention (DEFER) on an applicable goal counts as **incorrect** (per prereg 6.1 convention)
- **Denominator**: Number of applicable goals in the evaluation split
- **Inference**: Paired family-blocked bootstrap (5 blocks = 5 families), 10,000 resamples, one-sided 95% lower bound
- **Comparison**: Candidate vs B-LEXICAL-OVERLAP (primary), Candidate vs B-RANDOM-ROLE (secondary)

## 9. Secondary Metrics (All Must Pass for COMPLETE_SUPPORTS)

| Metric | Threshold | Method |
|--------|-----------|--------|
| Pooled false-accept rate | ≤ 0.10 (Wilson 95% upper) | `false_accept / (executable_correct + executable_incorrect)` on applicable goals where arm returned EXECUTABLE |
| UNKNOWN precision | ≥ 0.85 (Wilson 95% lower) | `TP_abstain / (TP_abstain + FP_abstain)` where TP=no-mechanism+abstain, FP=mechanism+abstain |
| Global ECE | ≤ 0.15 (bootstrap 95% upper ≤ 0.18) | 10 equal-mass bins, top bin [0.9,1.0], bootstrap 10,000 resamples |
| Candidate > B-RANDOM-ROLE | One-sided p < 0.05 | Paired family-blocked bootstrap on applicable goals |

## 10. Decision Rule (Formal)

```
IF any(V1..V13) == FAIL:                          status = MEASUREMENT_INVALID, outcome = INCONCLUSIVE
ELSE IF V11 == FAIL:                              status = MEASUREMENT_INVALID, outcome = INCONCLUSIVE
ELSE IF PC-VERBATIM-INTENT.accuracy < 1.0:        status = MEASUREMENT_INVALID, outcome = INCONCLUSIVE
ELSE IF B-INTERNAL-ID-ORACLE.accuracy < 1.0:      status = MEASUREMENT_INVALID, outcome = INCONCLUSIVE
ELSE IF NC-NO-APPLICABLE.abstention_rate < 1.0:   status = MEASUREMENT_INVALID, outcome = INCONCLUSIVE
ELSE IF V13 == FAIL:                              status = MEASUREMENT_INVALID, outcome = INCONCLUSIVE
ELSE IF V6 == FAIL:                               status = MEASUREMENT_INVALID, outcome = INCONCLUSIVE
ELSE IF primary_gate.lower_bound_95 <= 0:         status = COMPLETE, outcome = FALSIFIES
ELSE IF any(secondary_gate) == FAIL:              status = COMPLETE, outcome = MIXED
ELSE:                                             status = COMPLETE, outcome = SUPPORTS
```

**Logic**: Validity/control gates are gating (any failure → MEASUREMENT_INVALID). Primary gate determines FALSIFIES vs (SUPPORTS/MIXED). Secondary gates only distinguish SUPPORTS from MIXED when primary passes.

## 11. Product Consequences

### Positive (COMPLETE + SUPPORTS)
- C-SEMANTIC-RESOLVE advances from **HYPOTHESIS → EXPERIMENTAL**
- Evidence that embedding-similarity semantic resolution works on independently authored goals with calibrated abstention
- Product capability "semantic resolution" (goals → mechanisms without internal IDs) gains experimental support
- Enables downstream work on C-PARAM-INHERIT (parameterized mechanisms) and C-LLM-INHERIT (external agent benefit)
- Product may integrate calibrated embedding resolver behind semantic resolution interface

### Negative (COMPLETE + FALSIFIES or MIXED)
- C-SEMANTIC-RESOLVE remains **HYPOTHESIS** or bounded to **REJECTED** for embedding-similarity approach
- Prior 45/52 vs 33/52 advantage confirmed as joint-authorship artifact
- Product must **not** ship embedding-based semantic resolution
- Alternative approaches required: cross-encoder reranking, LLM-based resolution, structured retrieval, hybrid methods
- Next Graph experiment must pivot to alternative resolution mechanism

## 12. Estimated Cost

- Model calls: 0 (local sentence-transformers only)
- Browser interactions: 0
- HTTP requests: 480 (80 tasks × 6 arms)
- CPU seconds: ~120
- Wall-clock seconds: ~180
- External API calls: 0

## 13. Expected Information Gain

**High**. This is a decisive retest of the only positive signal for C-SEMANTIC-RESOLVE with the confound removed. A clean positive upgrades the claim to EXPERIMENTAL with calibrated evidence. A clean negative retires the only positive signal and forces a pivot to alternative resolution mechanisms. Either outcome changes the product decision on semantic resolution.

## 14. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Embedding model quality drives effect, not method | A-REFERENCE-DISTINCT-EMBEDDING uses different model (mpnet) as independent check |
| Calibration gate overfits calibration split | Gate fitted on calibration, threshold selected on validation, evaluated on test; independent_refit_spread > 1.0 required |
| Family-blocked bootstrap underestimates variance | 5 blocks is minimum; 10,000 resamples; report CI width |
| Token Jaccard null is weak | Structural ceiling 0.65 on all-80; applicable-only shows 0.6923 in prior run; headroom to 1.0 |
| OOD goals not representative | 20 OOD goals from diverse unrelated domains; UNKNOWN precision explicitly defined |
| Single embedding model (no ensemble) | Acknowledged as limitation; mpnet reference provides cross-model check |
| stdlib HTTP not representative of real Web | This is a mechanism test, not end-to-end economics; C-PRODUCT-ECON tested separately |
| Abstention scoring convention | Explicitly preregistered: abstention on applicable = incorrect for primary metric |

## 15. Artifact Hashes (for freeze_artifacts_bound)

All files listed in `spec.json.freeze_artifacts` will be hashed by the deterministic freezer into `freeze.json.artifact_hashes`. At execution start, `provenance.json.frozen_input_verification` will verify all hashes match.

## 16. Differences from Prior R2 Attempts (EXP-GRAPH-36272373909, 36279237023, 36287167610)

| Defect in Prior Runs | Fixed in This Design |
|---------------------|---------------------|
| V9: Code not hashed into freeze (control-plane defect) | `freeze_artifacts` lists all 10 mutable code files; freezer hashes them |
| Reference arm identical to candidate (argmax-w*cos+b) | A-REFERENCE-DISTINCT-EMBEDDING uses **all-mpnet-base-v2** (different model) + independent gate fit |
| Joint authorship confound (intents + goals in same file) | Independent goal authoring (V2) + contamination screen against ALL intents (V3) + authoring provenance (V12) |
| Calibration gate inert (threshold 0.02, fired 0/52) | V6 requires gate fires on >0 applicable validation goals; threshold selected on validation split |
| NC-NO-APPLICABLE abstentions from parameter binding, not gate | Gate must fire on no-applicable; parameter binding abstentions tracked separately |
| False-accept metric ambiguity (4 readings) | Single pooled false-accept definition preregistered; Wilson CI used |
| No dynamic range verification for controls | V13: control arms collectively verified on calibration split to span non-degenerate range (min_across_arms < max_across_arms) |

## 17. Legacy Comparison (per POLICY.md §46)

**LEGACY: DISTINCT_EXTENSION** — The pre-2.0 paraphrase-resolution threads (graph/paraphrase_prompt_confirm_cycle4.md artifact 144, paraphrase_prompt_cycle3.md artifact 145, fused confirm 146; product summary artifact 4.697 sha 017a80aeb9a6759c8f6913a37031ff1616ec1bda: G-H2 3/3 unseen compositions vs 0/3 weak baselines with keyword/oracle dependence, scripted V31 paraphrase retrieval 2/8 to 6/8) are the closest precedents. The legacy guard P2-BLIND-COMPOSITION explicitly forbids repeating weak-baseline/keyword-dependent designs. This allocation is a materially distinct extension because it adds: independent goal authoring (separate stage, separate artifact), provably distinct reference arm, fail-able positive/null controls, and contamination screen against EVERY intent. Not a rerun: the three R2 attempts were all MEASUREMENT_INVALID on the control-plane V9 defect and tautological controls, never on the science; this test changes the object (remove the confound) rather than re-freezing the same design.

## 18. Open Questions (Unresolved)

- Whether a better-calibrated candidate resolver (different threshold, better calibration head, more training data) could satisfy the primary gate if this one fails
- Whether the decision rule's requirement for candidate to beat lexical null while maintaining calibration is appropriate
- Whether the OOD goal set (20 goals) is sufficient for reliable UNKNOWN precision estimation
- Whether the candidate's false-accept rate (if high) stems from semantic similarity false positives or HTTP execution failures
- Whether a different embedding model or fine-tuning would improve calibration
- Whether the contamination screen threshold (0.3) is appropriate for this vocabulary
- Whether family-blocked bootstrap with 5 families provides adequate coverage for CI estimation

---

**Preregistration frozen before any outcome data inspection.** All measurement validity gates, controls, metrics, and decision rules are declared above. No confirmatory analysis will be added after seeing test-split results.