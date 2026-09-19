# EXP-PRODUCT-35409929216 preregistration

## Title

Sensitivity analysis of the 5.42% token savings margin to completion token estimation error

## Authors

Product lane autonomous agent

## Date

2026-09-19

## Status

DESIGN ONLY — not yet frozen

## 1. Background

Three consecutive PRODUCT lane experiments have not produced end-to-end measurement with real LLM execution:
1. EXP-PRODUCT-35330741529: FALSIFIED-IN-SETTING (measurement validity violated, synthetic corpus)
2. EXP-PRODUCT-35353007958: MEASUREMENT_INVALID (no LLM API keys)
3. EXP-PRODUCT-35389141536: SURVIVES_CURRENT_TEST with tautological C3/C4 (browser costs identical by construction)

The parent handoff identifies three options:
- (A) Provision LLM API credentials and execute frozen COLD baseline
- (B) Close C-PRODUCT-ECON as unmeasurable given persistent infrastructure blockers
- (C) Pivot to measuring end-to-end agent economics on real SPIDER registry

The parent handoff also identifies a critical concern: "5.42% token savings margin is thin and sensitive to ~1 token/task estimate error."

## 2. Question

Is the 5.42% token savings margin (1067 tokens) from parameterized deduplication robust to realistic completion token estimation error, or is it fragile and likely an artifact of the assumed 2/15/20 completion token distribution?

## 3. Hypothesis

The 5.42% margin is fragile: systematic completion token estimation error of less than 1 token/task (32 tasks × 1 token = 32 tokens) erases the margin (1067 tokens).

Sub-hypotheses:
- H1: The break-even systematic bias in completion tokens is < 2 tokens/task
- H2: The margin is dominated by the selection prompt savings (112 tokens, 14.16%) not the completion savings
- H3: Under realistic completion token variation (±50% of estimates), the margin survives in < 30% of bootstrap samples

## 4. Falsifier

FALSIFIED if:
- F1: Break-even systematic bias ≥ 3 tokens/task (> 32 tasks × 3 = 96 tokens, still < 10% of margin), indicating the margin is robust to realistic estimation error
- F2: Under ±50% completion token variation, the margin survives in > 70% of bootstrap samples

MIXED if: break-even 1-3 tokens/task AND survival rate 30-70%

## 5. Analysis plan

### 5.1 Data source

Carry forward token costs from EXP-PRODUCT-35330741529:
- LITERAL total: 19691 tokens (791 selection + 18900 completion)
- PARAMETERIZED total: 18624 tokens (679 selection + 17945 completion)
- COLD total: 2475 tokens (77 per task × 32)
- Selection prompt savings: 112 tokens (14.16%)
- Completion savings: 955 tokens (5.05%)
- Total savings: 1067 tokens (5.42%)

Task composition (32 tasks):
- 5 blog-read-post: completion = 2 tokens each
- 15 shop/admin/pm tasks: completion = 15 tokens each
- 12 other tasks: completion = 20 tokens each

### 5.2 Break-even analysis

Compute the systematic bias (delta per task) needed to erase the 1067-token margin:
- If all tasks have delta completion tokens, total change = 32 × delta
- Break-even: delta = 1067 / 32 = 33.3 tokens/task

This is the maximum systematic bias that preserves the margin. However, the margin is not uniform across task types:
- Selection prompt savings: 112 tokens (fixed, not affected by completion estimates)
- Completion savings: 955 tokens (directly affected by completion estimates)

The true break-even for completion savings only is:
- Break-even delta = 955 / 32 = 29.8 tokens/task

But this is the bias relative to the *current* estimates. The current estimates are 2/15/20. A systematic bias of +1 token/task means the true values are 3/16/21.

### 5.3 Bootstrap analysis

For each of 1000 bootstrap samples:
1. For each task type, sample completion tokens from Normal(estimate, 0.5 × estimate)
2. Recompute LITERAL and PARAMETERIZED total costs
3. Check if PARAMETERIZED < LITERAL (margin survives)
4. Compute survival rate = fraction of samples where margin survives

### 5.4 Sensitivity to COLD baseline

Vary COLD cost from 2475 to 5000 tokens (±100%) and recompute the COLD-to-PARAMETERIZED ratio. The COLD baseline is 8× cheaper; does this ratio survive?

## 6. Controls

- **Positive control**: Selection prompt savings remain 112 tokens regardless of completion variation (they don't depend on completion tokens)
- **Null control**: With zero completion tokens, savings = 112 tokens (selection prompt only)

## 7. Expected outcomes

| Scenario | Break-even | Survival | Interpretation |
|----------|-----------|----------|----------------|
| FRAGILE | < 1 token/task | < 30% | Close C-PRODUCT-ECON, redirect to non-token mechanisms |
| MIXED | 1-3 tokens/task | 30-70% | Need real LLM measurement to resolve |
| ROBUST | ≥ 3 tokens/task | > 70% | Continue toward real LLM measurement (option A) |

## 8. Decision consequences

- **Positive outcome (ROBUST)**: The margin is robust to estimation error. Proceed with option A from parent handoff: provision LLM API credentials and execute frozen COLD baseline. This validates the token-based economics line.
- **Negative outcome (FRAGILE)**: The margin is fragile. Close C-PRODUCT-ECON and redirect product lane to non-token mechanisms (registry compression, retrieval efficiency, correctness improvements). This resolves the three-way decision in favor of option B.
- **Mixed outcome**: The margin's robustness is uncertain. This does not resolve the three-way decision but provides stronger evidence for the directorial decision.

## 9. Limitations

- This is a sensitivity analysis, not a real LLM measurement. It measures robustness to *estimation error*, not actual LLM costs.
- The analysis assumes the current task composition (32 tasks, 5/15/12 type distribution) is representative.
- The bootstrap analysis assumes completion token variation is normally distributed with CV=0.5; real variation may be heavier-tailed.
- The analysis does not measure COLD success rate (assumed 100%), which could change the economics if real success rate is lower.

## 10. Data availability

- Token costs: EXP-PRODUCT-35330741529/raw_evidence.json
- Task composition: EXP-PRODUCT-35330741529/run_experiment.py
- Parent handoff: EXP-PRODUCT-35389141536/handoff.json
- Claim registry: research/claims/registry.json (C-PRODUCT-ECON)
