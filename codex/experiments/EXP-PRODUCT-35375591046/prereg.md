# EXP-PRODUCT-35375591046 Preregistration

## Experiment Identity

- **Experiment ID:** EXP-PRODUCT-35375591046
- **Lane:** product
- **Claim IDs:** C-PRODUCT-ECON
- **Parent:** EXP-PRODUCT-35353007958 (handoff sha256: 0fb45f53ab9fe04b8c3bdfb5e89d5e95e0cf7dc3ad67ac073f159e8c0258a9a0)

## Motivation

The parent experiment (EXP-PRODUCT-35353007958) was MEASUREMENT_INVALID due to missing LLM API keys. No evidence was produced. The parent's analytical ceiling (5.42% token savings on synthetic 32-task corpus) remains the most recent valid measurement with validity gaps (C1 assumed, completion estimated, browser omitted, COLD 8x cheaper unmeasured).

The three-way decision from the parent handoff (A: re-run with API keys, B: real corpus, C: close token-based economics) remains the required product lane decision. The smallest unblocking action is providing API access; alternatively, the COLD baseline economics and thin margin may justify closing this line of inquiry.

This experiment pursues option C indirectly: measure the COLD baseline success rate and token cost to determine whether token-based inheritance is necessary at all. If COLD is viable, the 5.42% savings are irrelevant. If COLD is not viable, the parent's frozen design (option A) remains relevant.

## Research Question

What is the success rate and token cost of the COLD baseline (no registry) on the synthetic 32-task corpus using a real LLM, and does this viability close the token-based inheritance economics line?

## Hypothesis

The COLD baseline (no registry) achieves >= 90% success rate with average token cost <= 100 tokens/task on the synthetic 32-task corpus, making token-based parameterized inheritance unnecessary because the cheapest baseline is already viable.

## Falsifier

COLD success rate < 90% OR average token cost > 150 tokens/task, indicating that COLD is not viable and registry-based inheritance may still be needed.

## Test Corpus

Identical to parent EXP-PRODUCT-35330741529: 32 tasks across 6 domains (blog, admin, shop, pm, auth, search) with known expected outcomes.

## Baselines

### B-COLD-EXECUTED
No registry. Real LLM generates the correct URL from the task goal without any mechanism guidance via API call.

### B-LITERAL-EXECUTED
Full literal registry (32 concrete-URL mechanisms). Real LLM selects from all 32 mechanisms via API call; executes the matched mechanism directly. Reference baseline for token cost comparison; not primary target.

### B-PARAMETERIZED-EXECUTED
Deduplicated parameterized registry (25 mechanisms with `${slot}` templates). Real LLM selects from 25 mechanisms via API call and resolves the matched template via a second API call. Reference baseline for token cost comparison; not primary target.

## Controls

### Positive Control: POS-CONTROL-COLD-SIMPLE
The 5 blog-read-post tasks (simple GET /posts/{id}) must be solvable by COLD with correct URL generation.

**Expected:** All 5 tasks produce correct URLs under COLD; success rate 100% on these simple tasks.

### Null Control: NULL-COLD-COMPLEX
Tasks with complex parameters (admin, auth, search) may have lower COLD success rate, indicating registry value.

**Expected:** COLD success rate on complex tasks may be lower than on simple tasks; not required to pass.

## Measurement Protocol

### Execution Steps

**For each task in COLD condition:**

1. **COLD step:**
   - System prompt: empty or minimal instruction
   - User prompt: task description
   - Model outputs: URL generated from scratch
   - Measure: prompt tokens, completion tokens

### Token Measurement
- All token counts measured via `tiktoken` (cl100k_base) on actual prompt+completion text, not estimated

### Success Criteria
- **Task success:** resolved URL matches expected URL exactly

### API Configuration
- Model: specified in provenance.json (e.g., gpt-4o-mini or available model)
- Temperature: 0.0 (deterministic)
- Max tokens: 50 (sufficient for URL generation)
- Timeout: 30 seconds per call
- Retry: up to 2 retries on API errors (429, 500, 503)

## Frozen Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- (C1) COLD success rate >= 90% across all 32 tasks
- (C2) average COLD token cost (prompt+completion) <= 100 tokens/task
- (C3) positive control passes (5 blog-read-post tasks succeed)

**FALSIFIED** if any condition fails.

**MEASUREMENT_INVALID** if API failures prevent completion of >=5 tasks.

## Product Consequences

### If SURVIVES_CURRENT_TEST
- COLD achieves >=90% success with <=100 tokens/task
- Token-based inheritance economics are closed: the cheapest baseline is viable
- Parameterized inheritance adds net token overhead without必要 benefit
- Product lane pivots to alternative mechanisms (registry compression, retrieval efficiency, orthogonal capabilities)
- C-PRODUCT-ECON advances toward REJECTED for token-based savings

### If FALSIFIED
- COLD fails (<90% success or >150 tokens/task)
- Registry-based inheritance may still be needed
- The parent's 5.42% analytical savings remain potentially relevant
- Product lane should pursue option A (re-run with API keys) or option B (real SPIDER corpus)
- C-PRODUCT-ECON remains HYPOTHESIS

## Estimated Cost

- 32 tasks × 1 condition × 1 LLM call each = 32 API invocations
- ~500 tokens/call average ≈ 16K total tokens
- No browser/network execution needed
- Estimated wall time: <5 minutes

## Scope Limitations

This experiment does NOT test:
- Browser execution cost or verification cost (assumed equal across conditions)
- Real SPIDER registry/task corpus (synthetic corpus only)
- Parameterized or literal registry conditions (reference baselines only)
- Non-deterministic LLM behavior (temperature 0.0)
- Cross-site generalization
- Staleness or freshness effects

These omissions are acceptable because the experiment's goal is to determine whether COLD baseline viability closes the token-based inheritance line, not to establish end-to-end product economics.