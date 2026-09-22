# EXP-INTEL-35697055679 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35697055679
- **Lane**: Intel
- **Claims**: C-LLM-INHERIT, C-CROSSSITE
- **Parent Handoff**: EXP-INTEL-35651934683 (verdict: SURVIVES_CURRENT_TEST, audit: bounded)
- **Director Mandate**: PIVOT to C-LLM-INHERIT with cognitive reset
- **Date**: 2026-09-22
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can actual mechanism sharing be verified on WebArena Docker datasets by extracting accessibility trees from 2-3 shopping stores and measuring mechanism overlap fraction, parameterization prevalence, and duplication fraction?

## 3. Motivation

### 3.1 The Blocking Problem

The prior structural survey (EXP-INTEL-35651934683) identified WebArena shopping as the strongest candidate for C-LLM-INHERIT experiment design (M1=1.0 cross-site structure, M2=0.8 heuristic parameterization). However, audit finding VF5 states: "Cross-site mechanism sharing is assumed from documentation, not verified on task samples." This assumption blocks C-LLM-INHERIT experiment design because:

1. WebArena 996 shopping tasks across 12 stores may have per-instance duplication (996 vs 812 task count discrepancy)
2. Documentation-level intent templates may not map to actual interactive elements in accessibility trees
3. Parameterization prevalence is heuristic (M2=0.8), not measured from task definitions

### 3.2 Why This Experiment Is Highest-Information

The Director mandate identifies this as the most impactful Intel work: "resolving VF5 and unblocking C-LLM-INHERIT experiment design." A positive outcome directly enables the highest-leverage untested product promise (C-LLM-INHERIT). A negative outcome redirects product lane away from WebArena cross-site inheritance.

### 3.3 What This Experiment Is Not

This is NOT an end-to-end LLM inheritance test. It verifies the prerequisite: do mechanisms actually share across stores? The experiment does not test whether an LLM agent benefits from inheritance.

## 4. Hypotheses

### H1: Mechanism Overlap
Mechanism overlap fraction across 2-3 stores will be ≥0.5. A mechanism is defined as an intent template (e.g., "search for product X", "add item to cart", "checkout") that appears in at least 2 stores.

### H2: Duplication Fraction
Duplication fraction across stores will be <0.8. Duplication is defined as tasks with identical intent templates across stores (same abstract task, different store instance).

### H3: Parameterization Prevalence
Parameterization prevalence will be ≥0.1. Parameterization is defined as intent templates with variable fields (e.g., product name, search query) that could become parameter slots.

### H4: Documentation-Execution Mapping
Documented intent templates map to actual interactive elements in accessibility trees (positive control: search mechanism appears in all stores).

## 5. Methods

### 5.1 Infrastructure
- Deploy WebArena Docker image `am1n3e/webarena-verified-shopping:latest` for 2-3 stores (randomly selected from the 12 store instances)
- Validate Playwright + Chromium functional for accessibility tree extraction
- Record Docker image digest before measurement

### 5.2 Task Selection
- Parse task definitions from WebArena-Verified dataset (JSON files)
- For each store, sample 10 tasks using frozen random seed (seed=35697055679), stratified by intent template type
- Record task IDs and intent templates

### 5.3 Accessibility Tree Extraction
- For each task, extract accessibility tree at initial viewport using Playwright
- Save raw accessibility tree with sha256 hash
- Extract interactive elements (input, button, select, etc.) and their properties

### 5.4 Mechanism Analysis
- Map each task to an intent template (manual verification of 5 tasks for mapping validity)
- Compute mechanism overlap fraction: fraction of intent templates appearing in ≥2 stores
- Compute duplication fraction: fraction of tasks with identical intent templates across stores
- Compute parameterization prevalence: fraction of intent templates with variable fields

### 5.5 Controls
- **Positive control**: Search mechanism (input + button) appears in all stores
- **Null control**: If Wikipedia store Docker available, verify it does not contain shopping mechanisms
- **Baseline comparison**: Compare with documentation-based M1=1.0, M2=0.8

## 6. Decision Rule

**SURVIVES_CURRENT_TEST** if ALL:
1. Mechanism overlap fraction ≥0.5
2. Duplication fraction <0.8
3. Parameterization prevalence ≥0.1
4. Positive control passes (search in all stores)
5. Infrastructure blocks ≤1 store (if 2 stores succeed, proceed)

**FALSIFIED-IN-SETTING** if:
- Mechanism overlap fraction <0.5 (mechanisms not shared)

**MIXED** if:
- Duplication fraction ≥0.8 (tasks duplicated, inheritance less meaningful)

**BLOCKED** if:
- Infrastructure blocks ≥2 stores (Docker deployment fails)

**MEASUREMENT_INVALID** if:
- Intent templates do not map to accessibility tree elements (documentation vs execution mismatch)

## 7. Validity Threats

### 7.1 Representation Loss
- Accessibility tree truncation (max_obs_length) may hide elements
- Viewport-only extraction may miss off-screen mechanisms
- ARIA role vs HTML tag mapping may affect mechanism identification

### 7.2 Sampling Bias
- 10 tasks per store may not represent full task diversity
- Random seed may produce unrepresentative sample
- Intent template mapping may be ambiguous

### 7.3 Infrastructure Risks
- Docker images may require authentication (blocked in prior experiments)
- Playwright may fail on certain page types
- Task definition JSON format may vary across stores

### 7.4 Mechanism Definition Ambiguity
- Intent template granularity affects overlap calculation
- Parameter slot identification is non-trivial
- Duplication definition (identical intent template) may be too strict or too loose

## 8. Expected Outcomes

### Positive Outcome (SURVIVES)
- Mechanism sharing verified → C-LLM-INHERIT experiment design can proceed
- Product lane can design train-on-N-stores, test-on-held-out-stores experiment
- Duplication fraction informs task uniqueness for novelty fraction measurement

### Negative Outcome (FALSIFIED)
- Mechanisms not shared → C-LLM-INHERIT cannot use WebArena cross-site inheritance
- Product lane must use single store with parameter variation or stay bounded to 2-site corpus
- Documentation-level M1=1.0 shown to be misleading

### Mixed Outcome (DUPlication high)
- Tasks duplicated across stores → inheritance less meaningful
- Need to assess whether duplication dilutes cross-site transfer benefit

## 9. Analysis Plan

- Compute metrics with 95% bootstrap confidence intervals
- Report per-store and aggregate mechanism overlap
- Manual verification of intent template mapping for 5 tasks per store
- Compare with documentation-based estimates (M1, M2)
- Preserve raw accessibility trees and task definitions for audit

## 10. Time and Resource Estimate

- Docker deployment and validation: 1 hour
- Accessibility tree extraction (30 tasks): 2 hours
- Mechanism analysis and manual verification: 1 hour
- Total compute: ~4 hours
- Manual effort: ~1 hour for intent template mapping verification