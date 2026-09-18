# Preregistration: EXP-PRODUCT-35290617719

## Experiment Overview

**Lane:** Product  
**Experiment ID:** EXP-PRODUCT-35290617719  
**Date:** 2026-09-18  
**Parent Handoff:** EXP-PRODUCT-35262262156  

## Question

Does parameterized mechanism representation reduce total unique mechanism count and token cost across the existing SPIDER task corpus, providing evidence that deduplication savings could offset per-mechanism token penalty in real agent workflows?

## Background

Two prior experiments (EXP-PRODUCT-35209109455, EXP-PRODUCT-35262262156) established that per-mechanism token savings do NOT exist as a general claim:
- Short-value patterns (1-3 chars): mean -6.4% penalty
- Long-value patterns: bimodal (UUID +44%, bearer +57% vs deep-path -12%, multi-param -10%), 2/5 positive

The only remaining economic argument for parameterized inheritance is **amortized deduplication**: if multiple tasks share the same action pattern, one parameterized mechanism replaces many literal variants, reducing storage, retrieval, and transmission costs.

This experiment measures the deduplication potential analytically before committing to expensive end-to-end infrastructure.

## Method

### Data Sources
1. **SPIDER Registry:** All existing mechanism definitions in `src/spider/registry/`
2. **Task Corpus:** All task definitions in `tasks/` directory
3. **Token Counter:** tiktoken cl100k_base (consistent with parent experiments)

### Procedure

#### Step 1: Enumerate Literal Mechanisms
For each task in the corpus:
- Extract all concrete URLs (after parameter substitution)
- Each unique URL becomes one literal mechanism
- Count: N_literal_mechanisms
- Token cost: sum of tokens for each literal mechanism definition

#### Step 2: Enumerate Parameterized Mechanisms
For each task in the corpus:
- Extract action patterns (method + URL template with parameter slots)
- Each unique pattern becomes one parameterized mechanism
- Count: N_parameterized_mechanisms
- Token cost: sum of tokens for each parameterized mechanism definition (including `${slot}` syntax)

#### Step 3: Compute Deduplication Metrics
- **Deduplication Ratio:** parameterized_total_tokens / literal_total_tokens
- **Net Token Savings:** literal_total_tokens - parameterized_total_tokens
- **Mechanism Count Reduction:** (literal_count - parameterized_count) / literal_count

#### Step 4: Controls
- **Positive Control:** Tasks sharing same action pattern (e.g., GET /posts/{id} for IDs 1-100) should collapse to 1 parameterized mechanism
- **Null Control:** Tasks with completely distinct patterns should show ratio ~1.0

### Decision Rule

**SURVIVES_CURRENT_TEST** requires ALL of:
- C1: parameterized_mechanism_count < literal_mechanism_count
- C2: deduplication_ratio < 1.0 (parameterized cheaper than literal)
- C3: net_token_savings > 0
- C4: positive_control passes (shared patterns collapse)
- C5: null_control passes (no-sharing patterns show ratio ~1.0)

**FALSIFIED-IN-SETTING** if any condition fails.

### Measurement Validity

1. Mechanism definitions from existing registry/task corpus only (not synthetic)
2. Token counting uses tiktoken cl100k_base
3. GET and non-GET methods counted separately (avoid method-conflation bias from EXP-PRODUCT-35132898840)
4. No browser/model/network calls — purely analytical

### Expected Outcomes

**Positive (deduplication viable):**
- Deduplication ratio < 1.0 with positive net savings
- → Proceed to end-to-end C-PRODUCT-ECON measurement

**Negative (deduplication not viable):**
- Deduplication ratio >= 1.0 or net savings <= 0
- → Close token-based inheritance, pursue alternative product economics

### Validity Threats

1. **Task corpus representativeness:** Current tasks may not reflect real agent workflows
2. **Mechanism reuse assumption:** Real agents may not share patterns as much as static corpus suggests
3. **Token overhead estimation:** Parameterized mechanism tokens include `${slot}` syntax which may not accurately represent real storage/retrieval costs
4. **Method conflations:** Separate GET/non-GET counting to avoid EXP-PRODUCT-35132898840 bias

### Scope Limitations

This experiment measures **static deduplication potential**, not:
- End-to-end amortized cost with real agent execution
- Retrieval efficiency gains from fewer mechanisms
- Transmission cost savings
- Storage cost savings in production registry

A positive result justifies building end-to-end measurement infrastructure. A negative result closes the token-based inheritance economic argument.
