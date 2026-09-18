# EXP-PRODUCT-35330741529 — Preregistration

## Experiment Identity

- **Experiment ID**: EXP-PRODUCT-35330741529
- **Lane**: product
- **Claim IDs**: C-PRODUCT-ECON, C-PARAM-INHERIT
- **Parent**: EXP-PRODUCT-35290617719 (deduplication arithmetic validated, frozen gate failed on C5 null control and C1 measurement validity)
- **Parent Handoff sha256**: fd386e76a3187d812f19dda54a4f4a7b4ebfb3a422ac2f925ebefb0a60e49a83

## 1. Research Question

Does parameterized mechanism deduplication reduce total end-to-end workflow cost per successful task compared to literal mechanism replay, when model selection, mechanism resolution, browser execution, and verification costs are all measured on a fixed task corpus?

## 2. Hypothesis

The deduplicated parameterized registry (25 mechanisms) reduces total workflow cost versus the full literal registry (32 mechanisms) because:

1. **Fewer mechanisms to evaluate**: Model selection cost scales with registry size; 25 vs 32 mechanisms means fewer tokens for evaluation.
2. **Shared pattern storage**: Storing a pattern once instead of N times reduces total registry tokens (parent measured 14.16% storage savings).
3. **Constant execution cost**: Both conditions execute the same actions (same URLs, same browser interactions, same verification), so execution cost cancels in the comparison.

The net workflow savings should exceed the parent's 14.16% storage savings because selection cost scales with registry size while execution cost is constant.

## 3. Falsifier

Total workflow cost for parameterized condition is higher than literal condition when all costs (selection + resolution + execution + verification) are summed, OR the parameterized condition achieves lower success rate due to binding/resolution failures, OR selection tokens for parameterized are higher than literal despite smaller registry.

## 4. Data Sources

### 4.1 Task Corpus

Reuse the synthetic 32-task corpus from parent EXP-PRODUCT-35290617719 (run_experiment.py TASK_CORPUS). This corpus is kept as a controlled testbed — the parent's measurement validity violation (synthetic vs registry) is acknowledged but accepted for this economic measurement. The question is not "does deduplication work on real registry" (that requires Option A) but "does storage-level savings translate to workflow savings" (testable on any corpus).

### 4.2 Mechanism Registries

- **Literal Registry**: 32 concrete-URL mechanisms from parent raw_evidence.json literal_mechanisms dict.
- **Parameterized Registry**: 25 parameterized mechanisms from parent raw_evidence.json parameterized_mechanisms dict (with ${slot} templates).
- **Cold Registry**: Empty — no mechanisms provided.

### 4.3 Model

Use the same model for all conditions. Temperature 0.0 for deterministic selection. Record exact model ID in provenance.json.

## 5. Method

### 5.1 Workflow Measurement Protocol

For each task in the corpus, under each condition (LITERAL, PARAMETERIZED, COLD):

**Step 1 — Selection**: Provide the model with the task goal and the full registry. Measure model tokens consumed for:
- Prompt tokens (task goal + registry description + instructions)
- Completion tokens (model's mechanism selection response)

**Step 2 — Resolution** (PARAMETERIZED only): Provide the model with the selected parameterized template and the task context. Measure model tokens for the resolution response (filling ${slot} with concrete value).

**Step 3 — Execution** (optional, not required for discriminating measurement): Execute the resolved URL via Playwright and measure browser interactions. Can be skipped if selection+resolution cost difference is already decisive.

**Step 4 — Verification** (optional): Verify final state matches expected outcome. Can be skipped if selection+resolution cost difference is already decisive.

### 5.2 Cost Aggregation

For each condition, compute:

```
total_workflow_cost = selection_prompt_tokens + selection_completion_tokens 
                    + resolution_tokens  # 0 for LITERAL and COLD
                    + browser_interactions  # constant across LITERAL and PARAMETERIZED
                    + verification_calls    # constant across LITERAL and PARAMETERIZED
```

For the discriminating measurement, focus on:

```
model_cost = selection_prompt_tokens + selection_completion_tokens + resolution_tokens
```

This isolates the deduplication-relevant cost. Browser and verification costs are constant across conditions and cancel in the comparison.

### 5.3 Per-Task Analysis

For each task, record:
- Registry size (mechanisms to evaluate)
- Selection tokens
- Resolution tokens (0 for LITERAL)
- Total model tokens
- Success (yes/no)
- Sharing category (shared pattern / unique pattern)

## 6. Controls

### 6.1 Positive Control (POS-CONTROL-SHARED-PATTERN-COLLAPSE)

The 5 blog-read-post tasks share GET /posts/{id}. In PARAMETERIZED condition:
- All 5 tasks must select the same mechanism key
- Resolution must fill ${id_0} with the correct concrete ID for each task
- Resolved URL must match the literal URL

### 6.2 Null Control (NULL-UNIQUE-PATTERN-OVERHEAD)

Tasks with unique patterns (no sharing) should show:
- Parameterized selection cost <= literal selection cost (fewer mechanisms)
- Parameterized total cost within 50% of literal total cost (resolution overhead partially offset by smaller registry)
- If parameterized cost exceeds literal by >50% for unique patterns, the overhead is not justified

### 6.3 Regression Control

Existing kernel tests (tests/test_kernel.py) must still pass after any code changes.

## 7. Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:

- **C1**: Both LITERAL and PARAMETERIZED conditions achieve 100% success rate
- **C2**: Parameterized selection tokens <= literal selection tokens
- **C3**: Total workflow cost (model_cost) for parameterized <= total workflow cost for literal
- **C4**: Positive control passes (shared patterns resolve correctly)
- **C5**: Null control passes (unique-pattern overhead <= 50%)

**FALSIFIED** if any condition fails.

**MEASUREMENT_INVALID** if infrastructure failure prevents completion of either condition.

## 8. Scope Limitations

1. **Synthetic corpus**: Task definitions and mechanism registry are synthetic/representative, not derived from real SPIDER agent execution. External validity to real workflows is not claimed.
2. **Heuristic induction**: Parameterized mechanisms use parent's heuristic regex induction, not kernel distill_parameterized(). Results reflect deduplication concept, not shipped product mechanism.
3. **Model-specific**: Results are specific to the chosen model. Different models may have different selection/resolution costs.
4. **No browser execution** (if skipped): If selection+resolution cost is the only measured cost, browser and verification costs are assumed equal across conditions. This is valid only if both conditions execute identical actions.
5. **No retrieval cost**: The experiment measures mechanism selection cost, not retrieval-from-database cost. In production, retrieval cost may differ.
6. **Storage-level deduplication**: The parent's 14.16% storage savings is the mechanism being tested. The experiment does not test alternative deduplication strategies.

## 9. Expected Outcomes

- **If C3 passes (parameterized <= literal total cost)**: Storage-level savings translate to workflow savings. The product lane should proceed to C-PRODUCT-ECON validation with real SPIDER registry.
- **If C3 fails (parameterized > literal total cost)**: Storage-level savings do NOT translate to workflow savings. The resolution overhead and per-task penalty outweigh the smaller registry. Close token-based inheritance economics.
- **If C2 fails (param selection > literal selection)**: The smaller registry does NOT reduce selection tokens. This would be surprising and suggest selection cost is not proportional to registry size.
- **If C1 fails (different success rates)**: The parameterized mechanism introduces binding/resolution failures. This would falsify the practical utility of parameterized inheritance.

## 10. Consequences

**Positive outcome** (SURVIVES_CURRENT_TEST):
- C-PRODUCT-ECON advances from HYPOTHESIS toward EXPERIMENTAL
- Product lane proceeds to real-corpus validation (Option A from parent handoff)
- Deduplication is validated as a workflow-level mechanism, not just storage-level

**Negative outcome** (FALSIFIED):
- C-PRODUCT-ECON may be REJECTED if resolution overhead consistently exceeds savings
- Product lane closes token-based economics and pivots to alternative mechanisms
- C-PARAM-INHERIT remains EXPERIMENTAL (resolution correctness is separate from economic viability)
