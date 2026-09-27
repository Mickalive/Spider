# Preregistration: EXP-GRAPH-36272373909

**Lane**: graph  
**Claim**: C-SEMANTIC-RESOLVE  
**Experiment ID**: EXP-GRAPH-36272373909  
**Director Mandate**: CONTINUE on C-SEMANTIC-RESOLVE, SUPERSEDE parent handoff (EXP-GRAPH-36132150213)  
**Frozen at**: Design stage — before any outcome-bearing measurement

---

## 1. Strategic Question (from Director Mandate)

On a stdlib-only real locally-served multi-endpoint HTTP application with genuinely distinct resource instances and goal wordings produced by a generator independent of the intent strings used at distillation, with that independence disclosed and provenance-traceable, and using a paired within-task design in which every candidate resolver and the incumbent shipped `spider.kernel.SpiderKernel` observe the identical starting state and the identical frozen mechanism fixture:

1. **(a) Incumbent reference curve**: What is the incumbent's reference resolution curve, measured rather than assumed — recording `shipped_has_distill_parameterized`, the shipped distill confidence against `min_confidence`, resolve status for exact and for paraphrased intent, and the number of EXECUTABLE resolutions attainable from the committed kernel alone, probed at the executing commit?

2. **(b) Candidate vs. incumbent + nulls**: Does any candidate goal-to-mechanism resolver convert unseen natural-language goals into correct applicable-mechanism bindings at a rate beating the incumbent and three strong nulls — random-role, lexical-overlap-only and internal-id-lookup — with family-blocked, trajectory-grouped uncertainty and non-degenerate interval width?

3. **(c) Applicability gate calibration**: Does its applicability gate abstain with pooled false-accept at most 0.10, UNKNOWN precision at least 0.85 and global and per-class ECE at most 0.15 with bootstrap upper at most 0.18, at a confidence threshold frozen before any arm runs?

---

## 2. Hypothesis

A candidate resolver that performs semantic goal-to-mechanism resolution (beyond exact intent string matching) can achieve higher abstention-adjusted accuracy than the incumbent SpiderKernel and three strong null baselines on unseen natural-language goals, while maintaining calibrated abstention (false-accept ≤ 0.10, UNKNOWN precision ≥ 0.85, ECE ≤ 0.15). The incumbent SpiderKernel, which only supports exact intent matching and has no parameterized induction (distill confidence=0.5 < min_confidence=0.8), will resolve 0 EXECUTABLE for paraphrased goals and serve as a well-characterized reference floor.

---

## 3. Pre-declared Falsifier

**If no candidate resolver beats the incumbent's abstention-adjusted accuracy at bounded false-accept (≤ 0.10), C-SEMANTIC-RESOLVE's mechanism-level premise is FALSIFIED-IN-SETTING and semantic resolution is abandoned as an architectural component in favour of explicit goal annotation or full re-exploration.**

This is a hard gate. No weakening of thresholds, no substitution of metrics, no "partial credit" for beating only some nulls.

---

## 4. Experimental Substrate

### 4.1 HTTP Application (V1)
- **Implementation**: Python stdlib `http.server` with custom `BaseHTTPRequestHandler`
- **Endpoints**: 5 distinct resource types × 4 CRUD operations = 20 endpoints
  - `/users` (GET, POST, PUT, DELETE)
  - `/posts` (GET, POST, PUT, DELETE)
  - `/comments` (GET, POST, PUT, DELETE)
  - `/albums` (GET, POST, PUT, DELETE)
  - `/photos` (GET, POST, PUT, DELETE)
- **State**: Each resource type has independent in-memory state (dict keyed by ID)
- **Authentication**: Bearer token required (validated via simple secret)
- **Response format**: JSON with consistent schema per resource type
- **No external dependencies**: Pure stdlib, no Flask, no Django, no database

### 4.2 Mechanism Fixture (V8)
- **Distillation pass**: Single fixed seed, run once before any resolver measurement
- **Distillation intents**: 5 verbatim intent strings (one per resource type), e.g.:
  - "create a new user"
  - "retrieve a post by id"
  - "update a comment"
  - "delete an album"
  - "list photos"
- **Mechanisms produced**: 5 literal mechanisms (one per intent) via `SpiderKernel.distill()`
- **Mechanism properties**:
  - `intent`: exact distillation intent string
  - `preconditions`: auth token present, required fields present
  - `action_template`: HTTP method, URL template, body template
  - `postconditions`: expected status code, response schema
  - `confidence`: 0.5 (hardcoded in current kernel)
  - `parameter_slots`: [] (no parameterization in current kernel)
  - `applicability_guards`: {} (empty in current kernel)
- **Registry**: Frozen after distillation; identical for all arms

### 4.3 Goal Generator (V2, V10)
- **Implementation**: Separate Python module with templated goal generation
- **Independence**: Generator templates never reference distillation intent strings
- **Vocabulary disjointness**: Measured via token overlap (target < 0.3 Jaccard)
- **Goal types per resource family** (4 per family × 5 families = 20 goals):
  - Paraphrased CRUD (e.g., "add a user" vs "create a new user")
  - Composite/implicit (e.g., "make a post and then comment on it")
  - Underspecified (e.g., "get the latest post")
  - Out-of-distribution (e.g., "archive a user" — no mechanism exists)
- **Provenance trace**: Generator prompt, seed, full output logged to `raw_evidence/goal_generation.json` before any resolver runs

---

## 5. Arms (Resolvers Under Test)

| Arm ID | Name | Description | Access |
|--------|------|-------------|--------|
| `A-INCUMBENT` | Incumbent SpiderKernel | Shipped `spider.kernel.SpiderKernel` with `min_confidence=0.8` | Full registry (intent, preconditions, action_template, postconditions, confidence, parameter_slots, applicability_guards) |
| `A-CANDIDATE` | Candidate Resolver | New semantic resolver (design detailed in Section 6) | Same as incumbent — **no mechanism_id, no fragment_id** |
| `B-RANDOM-ROLE` | Random Role Null | Uniform random mechanism selection | Same registry access |
| `B-LEXICAL-OVERLAP` | Lexical Overlap Null | Max token/Jaccard overlap between goal and mechanism intent | Same registry access |
| `B-INTERNAL-ID-LOOKUP` | Internal ID Lookup Null | Oracle: given goal, returns mechanism with matching internal ID (cheating) | **Full registry + internal IDs** — upper bound only |

**Paired within-task design (V3)**: Each task (goal + context) is presented to all 5 arms in randomized order. Arms share identical starting state and frozen registry.

---

## 6. Candidate Resolver Design

The candidate resolver implements **semantic goal-to-mechanism resolution** via:

1. **Embedding-based similarity**: Sentence-transformer (all-MiniLM-L6-v2, cached locally) encodes goal and mechanism intents; cosine similarity used for retrieval.
2. **Precondition checking**: Filters mechanisms whose preconditions match current context (auth, required fields).
3. **Applicability guard**: Learned calibration head (logistic regression on similarity + precondition features) outputs P(applicable). Threshold frozen at 0.5 before any run.
4. **Parameter binding**: For parameterized mechanisms (if any exist), extracts slot values from goal using NER/regex; for literal mechanisms, binds empty params.
5. **Abstention**: Returns UNKNOWN if max P(applicable) < threshold or no precondition match.

**Critical constraint (V9)**: The candidate resolver receives only the public mechanism interface (intent, preconditions, action_template, postconditions, confidence, parameter_slots, applicability_guards). It never sees `mechanism_id`, `fragment_id`, or internal indices.

---

## 7. Measurement Protocol

### 7.1 Tasks
- **20 goals** × **5 resource families** = 100 task instances (each goal instantiated with different resource IDs)
- **Split**: 16 paraphrased/composite/underspecified (in-distribution but unseen wording), 4 out-of-distribution (no applicable mechanism)
- **Context**: Each task provides a valid auth token and resource-specific context (e.g., target ID for retrieval)

### 7.2 Per-Task Measurement
For each arm on each task, record:
- `resolution_status`: EXECUTABLE | EXPLORE | UNKNOWN
- `bound_action`: dict (if EXECUTABLE)
- `confidence`: float
- `mechanism_id`: str (if EXECUTABLE/EXPLORE)
- `correct`: bool (EXECUTABLE + bound_action produces expected postconditions when executed on HTTP server)
- `false_accept`: bool (EXECUTABLE but bound_action fails verification)
- `abstained`: bool (UNKNOWN or EXPLORE)

### 7.3 Primary Metrics (computed per arm, pooled across families)
- **Abstention-adjusted accuracy** = EXECUTABLE_correct / (EXECUTABLE_correct + EXECUTABLE_incorrect + UNKNOWN)
- **False-accept rate** = EXECUTABLE_incorrect / (EXECUTABLE_correct + EXECUTABLE_incorrect)
- **UNKNOWN precision** = TRUE_UNKNOWN / (TRUE_UNKNOWN + FALSE_UNKNOWN) where TRUE_UNKNOWN = correctly abstained on OOD, FALSE_UNKNOWN = incorrectly abstained on in-distribution
- **ECE (Expected Calibration Error)**: 5-bin ECE on P(applicable) vs. empirical correctness, with bootstrap 97.5% upper bound
- **Per-class ECE**: Same for EXECUTABLE class and UNKNOWN class separately

### 7.4 Uncertainty Quantification (V4, V5, V6)
- **Family-blocked bootstrap**: 10,000 resamples at resource-family level (5 families)
- **Trajectory-grouped**: If multi-step tasks used, resample at trajectory level
- **Non-degenerate CI**: Wilson 95% CI width < 0.30 for primary rates; bootstrap CI upper for ECE < 0.18

---

## 8. Controls

### 8.1 Positive Control: PC-EXACT-MATCH
- **Condition**: Goals that exactly match a mechanism's intent string (verbatim)
- **Expected**: Incumbent achieves EXECUTABLE rate ≥ 0.95
- **Purpose**: Verifies fixture, registry, HTTP server, and measurement pipeline work
- **Failure → MEASUREMENT_INVALID**

### 8.2 Null Control: NC-NO-APPLICABLE
- **Condition**: 4 out-of-distribution goals per family (20 total) with no applicable mechanism
- **Expected**: All arms return UNKNOWN; UNKNOWN precision ≥ 0.85, false-accept = 0.0
- **Purpose**: Verifies abstention calibration on genuinely inapplicable goals
- **Failure → MEASUREMENT_INVALID**

---

## 9. Decision Rule

### Primary Gate (ALL must pass)
1. Candidate abstention-adjusted accuracy Wilson 95% lower bound > Incumbent Wilson 95% upper bound
2. Candidate false-accept Wilson 95% upper bound ≤ 0.10
3. Candidate UNKNOWN precision Wilson 95% lower bound ≥ 0.85
4. Candidate global ECE bootstrap 97.5% upper bound ≤ 0.18
5. Candidate per-class ECE (EXECUTABLE, UNKNOWN) bootstrap 97.5% upper bound ≤ 0.18

### Secondary Gates (ALL must pass)
6. Candidate beats B-RANDOM-ROLE on EXECUTABLE_correct rate (family-blocked bootstrap p < 0.01)
7. Candidate beats B-LEXICAL-OVERLAP on EXECUTABLE_correct rate (family-blocked bootstrap p < 0.01)
8. Candidate does not use internal IDs (verified by code inspection + V9)
9. PC-EXACT-MATCH passes
10. NC-NO-APPLICABLE passes

### Outcome Mapping
| Condition | Outcome |
|-----------|---------|
| All primary + secondary pass | **SURVIVES** |
| Primary gate fails (no candidate beats incumbent at bounded FA/calibration) | **FALSIFIES** (triggers pre-declared falsifier) |
| Primary passes but calibration gates fail, or beats some nulls not all | **MIXED** |
| Any V1-V11 violated, PC/NC fail, CI degenerate | **MEASUREMENT_INVALID** |

---

## 10. Preconditions as Observations (Hard Requirement)

Every precondition is recorded as an **OBSERVATION** with explicit `smallest_next_action` — **never as a blocking falsifier**.

| Precondition | Observation Key | Smallest Next Action if False |
|--------------|-----------------|-------------------------------|
| `distill_parameterized` exists in committed kernel at executing commit | `OBS-HAS-DISTILL-PARAMETERIZED` | Record `false`; proceed with incumbent-only measurement. Candidate resolver supplies own parameterized mechanisms. |
| Registry non-empty after distillation pass | `OBS-REGISTRY-NON-EMPTY` | Record `0`; debug distillation fixture; abort if unfixable in 10 min. |
| HTTP server responsive on all 20 endpoints | `OBS-HTTP-RESPONSIVE` | Record failure; restart server; abort if unrecoverable in 5 min. |
| Goal generator vocabulary disjoint from distillation intents (token Jaccard < 0.3) | `OBS-GOAL-GEN-INDEPENDENCE` | Record overlap ratio; if > 0.3, regenerate with new seed; abort if persistent. |

These observations are written to `raw_evidence/preconditions.json` **before any resolver arm runs**.

---

## 11. Validity Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| Candidate resolver accidentally accesses internal IDs | Code review + V9 enforcement (registry view strips IDs); auditor verifies |
| Goal generator leaks distillation vocabulary | Separate module, separate prompt, provenance logged before resolver runs (V2, V10) |
| HTTP server state leakage between tasks | Fresh in-memory state per task; server restarted between families |
| Family-blocked bootstrap too few families (5) | Minimum 5 families; if CI degenerate, report as MEASUREMENT_INVALID (V6) |
| Candidate resolver overfits to fixture | Held-out goals (composite/underspecified) not seen during resolver development |
| Incumbent confidence=0.5 < min_confidence=0.8 means 0 EXECUTABLE ever | This is the **measured reference floor**, not a bug — recorded as OBS-INCUMBENT-FLOOR |

---

## 12. Artifacts to Produce

| Path | Role |
|------|------|
| `raw_evidence/preconditions.json` | Raw observations (preconditions) |
| `raw_evidence/goal_generation.json` | Provenance: generator prompt, seed, all goals |
| `raw_evidence/fixture.json` | Frozen mechanism registry, distillation intents, HTTP endpoint specs |
| `raw_evidence/task_results.jsonl` | Per-task, per-arm raw outcomes |
| `derived_evidence/metrics.json` | Aggregated metrics with CIs |
| `artifacts/candidate_resolver.py` | Candidate resolver implementation (frozen at run start) |
| `artifacts/goal_generator.py` | Goal generator (frozen) |
| `artifacts/http_server.py` | HTTP application (frozen) |

---

## 13. No-Go Rules (from EXPERIMENT_PACKET.md §15 analog)

1. **No weakening thresholds** after seeing data (false-accept 0.10, UNKNOWN precision 0.85, ECE 0.15 are frozen)
2. **No substituting metrics** (abstention-adjusted accuracy is primary; not raw accuracy, not F1)
3. **No dropping null controls** (all three nulls must be beaten)
4. **No internal ID access** for candidate (V9 enforced by code + audit)
5. **No post-hoc family regrouping** (families fixed by resource type)
6. **No CI inflation** (degenerate CI → MEASUREMENT_INVALID, not "inconclusive")
7. **No precondition as falsifier** (all preconditions → observations with next actions)

---

## 14. Consequences

### If SURVIVES:
- Candidate resolver with calibrated abstention becomes promotable component
- Graph lane delivers semantic resolution module to Product lane
- Unblocks C-LLM-INHERIT, C-CROSSSITE, C-PRODUCT-ECON design
- Next experiment: live-browser replication + LLM agent integration

### If FALSIFIES (pre-declared falsifier triggered):
- C-SEMANTIC-RESOLVE mechanism-level premise FALSIFIED-IN-SETTING
- Semantic resolution abandoned as architectural component
- Product must rely on explicit goal annotation or full re-exploration
- Graph lane pivots to goal annotation interfaces and exploration economics
- **No further Graph cycles on semantic resolution without new Director mandate**

### If MIXED:
- Director adjudicates bounded ceiling; likely PARK semantic resolution, pursue goal annotation
- Specific failure mode (calibration vs. accuracy vs. nulls) recorded in handoff

### If MEASUREMENT_INVALID:
- Validity threat identified; smallest next action recorded in handoff
- Experiment may be re-frozen with fixed threat (new experiment ID)
- Does not update claim status

---

## 15. Independence & Provenance

- **No external API calls**: Sentence-transformer model cached locally (downloaded once, hashed)
- **No browser required**: Pure HTTP + stdlib
- **No GPU required**: CPU-only inference
- **Deterministic seeds**: All randomness seeded (numpy, python random, torch) and logged
- **Frozen code**: Candidate resolver, goal generator, HTTP server hashed at freeze time
- **Audit-ready**: All raw evidence preserved; metrics recomputable from task_results.jsonl

---

## 16. Dependencies (from Director Mandate)

1. **Runtime**: Capability ledger's product-code capability entry → Graph declares at prereg whether parameterized induction arm exists (recorded as OBS-HAS-DISTILL-PARAMETERIZED)
2. **Product**: Committed parameterized induction path → usable only as declared comparison arm, never as blocking precondition; if absent, incumbent reference curve is still the measurement
3. **Pre-freeze failure**: EXP-GRAPH-36249048451 failed at DESIGN with no scientific content — superseded, not inherited

---

**End of Preregistration**  
This document is frozen at design stage. No outcome data has been observed. Any modification after freeze invalidates the experiment.