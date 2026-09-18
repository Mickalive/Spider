# EXP-PRODUCT-35353007958 Preregistration

## Experiment Identity

- **Experiment ID:** EXP-PRODUCT-35353007958
- **Lane:** product
- **Claim IDs:** C-PRODUCT-ECON, C-PARAM-INHERIT
- **Parent:** EXP-PRODUCT-35330741529 (handoff sha256: 3876ceb91a77e10e2be1468b9d621f77e1a4eac941de86004794d75b6325015d)

## Motivation

The parent experiment (EXP-PRODUCT-35330741529) measured analytical token costs for parameterized mechanism deduplication and found 5.42% net workflow savings (1067 tokens) on a synthetic 32-task corpus. However, the frozen gate failed because:

1. **C1 (100% success) was assumed analytically, not measured** — no LLM selection or resolution calls were executed; the experiment used deterministic template filling
2. **Completion tokens were hard-coded estimates** (2 for selection, 15 for resolution, 20 for cold) — not measured from real model outputs; with 5.42% margin, modest variation in completion length could reverse C3
3. **Browser/verification costs were omitted** — assumed constant without evidence
4. **COLD baseline was 8x cheaper** (77 tokens/task) but success rate unmeasured

The parent audit (V1_C1_SUCCESS_UNMEASURED, V2_COMPLETION_TOKENS_ESTIMATED) and the parent handoff both identify the same next question: should the product lane (A) measure end-to-end workflow cost with real LLM calls on the existing synthetic corpus?

This experiment pursues option A: execute real LLM API calls for selection and resolution steps, measuring actual prompt and completion tokens, and verifying task success rates.

## Research Question

Does parameterized mechanism deduplication reduce total workflow cost per successful task when selection and resolution are executed with real LLM API calls, resolving the parent's C1_success and completion_token measurement gaps?

## Hypothesis

The deduplicated parameterized registry (25 mechanisms) reduces total workflow cost versus the full literal registry (32 mechanisms) under real LLM execution because:
1. Fewer mechanisms to evaluate during selection reduces prompt tokens
2. Real LLM completion tokens for mechanism selection are small (~2 tokens) and do not reverse the 5.42% analytical savings
3. Real LLM resolution of parameterized templates succeeds with low overhead

The parent's analytical estimate of 5.42% net savings survives real execution.

## Falsifier

Total workflow cost for parameterized condition exceeds literal condition under real LLM execution, OR LLM selection accuracy drops below 100% for either condition, OR real completion tokens for parameterized resolution exceed 15 tokens/task average by enough to reverse the 5.42% margin, OR any task fails end-to-end under either condition.

## Test Corpus

Identical to parent EXP-PRODUCT-35330741529: 32 tasks across 6 domains (blog, admin, shop, pm, auth, search) with known expected outcomes.

## Baselines

### B-LITERAL-EXECUTED
Full literal registry (32 concrete-URL mechanisms). Real LLM selects from all 32 mechanisms via API call.

### B-PARAMETERIZED-EXECUTED  
Deduplicated parameterized registry (25 mechanisms with `${slot}` templates). Real LLM selects from 25 mechanisms via API call and resolves the matched template via a second API call.

### B-COLD-EXECUTED
No registry. Real LLM generates the correct URL from the task goal without any mechanism guidance via API call.

## Controls

### Positive Control: POS-CONTROL-SHARED-PATTERN-EXECUTED
The 5 blog-read-post tasks (GET /posts/{id} with ids 101, 202, 303, 404, 505) must select the same parameterized mechanism under real LLM selection, and resolution must produce correct bound URLs.

**Expected:** All 5 tasks select `GET:https://blog.example.com/posts/${id_0}` in the parameterized condition; resolution calls produce correct bound URLs.

### Null Control: NULL-UNIQUE-PATTERN-EXECUTED
Tasks with unique patterns (search) should show parameterized total cost within 30% of literal total cost under real LLM execution.

**Expected:** For unique-pattern tasks, parameterized total workflow cost <= 1.3 × literal total workflow cost.

## Measurement Protocol

### Execution Steps

**For each task in each condition:**

1. **Selection step:**
   - System prompt: registry description (numbered list of `[METHOD] URL` patterns)
   - User prompt: task description
   - Model outputs: mechanism key (e.g., "1" for first mechanism)
   - Measure: prompt tokens, completion tokens

2. **Resolution step (parameterized only):**
   - System prompt: selected template with `${slot}` visible
   - User prompt: task description + concrete values for slot filling
   - Model outputs: resolved URL with slot filled
   - Measure: prompt tokens, completion tokens

3. **COLD step:**
   - System prompt: empty or minimal instruction
   - User prompt: task description
   - Model outputs: URL generated from scratch
   - Measure: prompt tokens, completion tokens

### Token Measurement
- All token counts measured via `tiktoken` (cl100k_base) on actual prompt+completion text
- No estimation or hard-coding of completion tokens

### Success Criteria
- **Selection success:** model outputs correct mechanism key (integer matching expected mechanism)
- **Resolution success:** resolved URL matches expected URL exactly
- **Task success:** both selection AND resolution succeed

### API Configuration
- Model: specified in provenance.json (e.g., gpt-4o-mini or available model)
- Temperature: 0.0 (deterministic)
- Max tokens: 50 (sufficient for mechanism key or URL)
- Timeout: 30 seconds per call
- Retry: up to 2 retries on API errors (429, 500, 503)

## Frozen Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- (C1) Both LITERAL and PARAMETERIZED conditions achieve 100% selection accuracy (correct mechanism key selected for all 32 tasks)
- (C2) Parameterized selection prompt tokens <= literal selection prompt tokens
- (C3) Total workflow cost (selection_prompt + selection_completion + resolution_prompt + resolution_completion) for parameterized <= total workflow cost for literal
- (C4) Positive control passes (5 blog-read-post tasks select same mechanism with correct bound URLs)

**FALSIFIED** if any condition fails.

**MEASUREMENT_INVALID** if API failures prevent completion of >=5 tasks in either condition.

## Product Consequences

### If SURVIVES_CURRENT_TEST
- The 5.42% analytical savings is validated under real LLM execution
- C-PRODUCT-ECON advances toward VALIDATED
- Proceed to option B (real SPIDER corpus testing) or larger registry economics

### If FALSIFIED
- The 5.42% analytical savings do not translate to real workflow economics
- C-PRODUCT-ECON status may advance to REJECTED
- Product lane pivots to alternative mechanisms (registry compression, retrieval efficiency, orthogonal capabilities)

## Estimated Cost

- 32 tasks × 3 conditions × (1-2 LLM calls each) ≈ 128-192 API invocations
- ~500 tokens/call average ≈ 64K-96K total tokens
- No browser/network execution needed
- Estimated wall time: <10 minutes

## Scope Limitations

This experiment does NOT test:
- Browser execution cost or verification cost (assumed equal across conditions)
- Real SPIDER registry/task corpus (synthetic corpus only)
- Registry sizes >32 mechanisms
- Non-deterministic LLM behavior (temperature 0.0)
- Cross-site generalization
- Staleness or freshness effects

These omissions are acceptable because the experiment's goal is to resolve the parent's specific validity gaps (C1_success, completion tokens), not to establish end-to-end product economics.
