# EXP-PHYSICS-35290611436 — Report

## Experiment

History-conditioned URL PMI on TodoMVC hash-SPAs: testing beyond-Markov structure

## Status

**COMPLETE** — FALSIFIED-IN-SETTING

## Summary

The parent experiment (EXP-PHYSICS-35262258744) demonstrated URL-level PMI of 0.188-0.209 bits on 5 TodoMVC hash-SPA variants, but could not determine whether this signal contained beyond-Markov structure or was entirely explained by deterministic (url, action) -> next_url transitions. This experiment resolves that question definitively: **the signal is entirely Markov**. Conditional PMI at K=3 is exactly 0.0 bits on all 5 variants, meaning the 3-step action history fully determines the next URL on these minimal deterministic SPAs.

## Key Results

### Primary Test: Conditional PMI at K=3

| Variant | PMI (bits) | Perm p | Effect d | Accuracy | Strata Used |
|---------|-----------|--------|----------|----------|-------------|
| vanillajs | 0.000 | 1.000 | -0.142 | 100.0% | 10/23 |
| react | 0.000 | 1.000 | -0.142 | 100.0% | 10/23 |
| vue | 0.000 | 1.000 | -0.176 | 95.4% | 7/24 |
| angular | 0.000 | 1.000 | -0.134 | 100.0% | 10/23 |
| svelte | 0.000 | 1.000 | -0.142 | 100.0% | 10/23 |

**0/5 variants achieve conditional PMI > 0.05 bits** — decisively fails the primary test threshold.

### Baseline: Unconditional PMI at K=0

| Variant | PMI (bits) | Perm p | Effect d |
|---------|-----------|--------|----------|
| vanillajs | 0.187 | 0.001 | 6.51 |
| react | 0.187 | 0.001 | 6.51 |
| vue | 0.204 | 0.001 | 7.14 |
| angular | 0.187 | 0.001 | 8.69 |
| svelte | 0.187 | 0.001 | 6.51 |

Parent signal reproduced exactly: 5/5 variants > 0.05 bits with p < 0.01.

### Intermediate: Conditional PMI at K=1

| Variant | PMI (bits) | Perm p | Effect d |
|---------|-----------|--------|----------|
| vanillajs | 0.074 | 0.327 | 0.40 |
| react | 0.074 | 0.327 | 0.40 |
| vue | 0.081 | 0.283 | 0.55 |
| angular | 0.074 | 0.111 | 1.24 |
| svelte | 0.074 | 0.327 | 0.40 |

K=1 PMI is positive but not significant after Bonferroni correction (all p > 0.01).

### Controls

| Control | Expected | Observed | Passes |
|---------|----------|----------|--------|
| Positive control (synthetic SPA) | PMI >= 1.0, p < 0.001 | PMI = 1.496, p = 0.001 | Yes |
| Null control (shuffled actions) | Mean PMI ~ 0.0 | -0.012 (K=3) | Yes |
| Null control (normalized URL) | PMI = 0.0 | 0.0 | Yes |

## Interpretation

### The Markov Ceiling

The K=0 to K=3 PMI trajectory (0.187 -> 0.074 -> 0.0 bits) reveals the information structure:

1. **K=0**: I(url_after; action | url_before) = 0.187 bits — the action provides 0.187 bits of information about the next URL given only the current URL. This is the unconditional Markov predictability.

2. **K=1**: I(url_after; action | url_before, H_1) = 0.074 bits — adding 1 previous action reduces PMI by 60%. The previous action disambiguates some state uncertainty.

3. **K=3**: I(url_after; action | url_before, H_3) = 0.0 bits — adding 3 previous actions completely eliminates PMI. The 3-step history fully determines the FSM state, making the current action redundant.

This is exactly the Markov-only prediction: on a deterministic FSM with 3-4 states and 3 actions, K=3 history uniquely identifies the current state, so (url_before, H_K=3) fully determines url_after regardless of the current action.

### Why K=3 is Sufficient

TodoMVC hash-SPAs are minimal deterministic FSMs:
- 3-4 hash states (#/, #/active, #/completed, sometimes trailing slash)
- 3 action primitives (form_submit, button_click, js_navigate)
- Deterministic transitions: each (state, action) maps to exactly one next state

With 3 actions and 3-4 states, the FSM's transition graph has in-degree at most 3. After K=3 actions, the path through the FSM is fully determined (given the starting URL), so the current action provides no additional information about the next URL.

### Implications for C-WEB-DYNAMICS

The parent's 0.188-0.209 bit PMI signal is entirely explained by deterministic Markov predictability. There is **no beyond-Markov component** on these testbeds. This means:

1. URL-level PMI on TodoMVC hash-SPAs demonstrates **state-conditioned predictability**, not **predictive dynamical structure beyond memory**.
2. The signal is a consequence of deterministic (url, action) -> next_url transitions, not of any deeper dynamical structure.
3. C-WEB-DYNAMICS ("Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity") is **not supported** on TodoMVC hash-SPAs.

### Scope of Falsification

The falsification is bounded to:
- TodoMVC hash-SPA testbeds (3-4 states, deterministic transitions)
- URL-level state representation with fragment preservation
- Action-history conditioning with K <= 3
- Non-leakage transitions only (action_primitive != 'link_click')

**Not falsified:**
- Beyond-Markov dynamics on production SPAs with larger state spaces (>4 states)
- Beyond-Markov dynamics on stochastic SPAs where H_K=3 does NOT determine the next state
- Richer state representations (DOM, accessibility tree) that might reveal structure invisible at URL level
- History-based routing SPAs where URL alone is ambiguous

## Decision Rule Evaluation

| Check | Condition | Result |
|-------|-----------|--------|
| C1 | >= 3/5 variants: K=3 PMI > 0.05 AND p < 0.01 | **FAIL** (0/5) |
| C2 | Positive control PMI >= 1.0 bits | PASS (1.496) |
| C3 | >= 50 NL transitions per variant | PASS (5/5) |
| C4 | K=0 PMI > 0.05 on >= 3/5 variants | PASS (5/5) |

**Verdict: FALSIFIED-IN-SETTING** — C1 fails. The frozen decision rule triggers falsification when fewer than 3/5 variants achieve conditional PMI at K=3 > 0.05 bits.

## Product Consequence

SPIDER should not rely on URL-level PMI alone for SPA state tracking on minimal deterministic SPAs. The 0.188-0.209 bit signal reflects Markov predictability, not beyond-memory dynamics. Richer representations (DOM, accessibility tree, visual layout) or explicit FSM modeling may be needed for SPA state tracking beyond what URL fragments provide.
