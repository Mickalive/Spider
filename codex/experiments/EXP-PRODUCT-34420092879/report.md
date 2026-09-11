# EXP-PRODUCT-34420092879 Report

## Experiment Summary

**Experiment ID**: EXP-PRODUCT-34420092879
**Lane**: Product
**Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
**Status**: COMPLETE
**Outcome**: SUPPORTS

## Scientific Question

Can C2 be resolved without regressions by implementing bind-time slot-level prefix extraction in `_bind()`, such that all 10 conditions pass and the product API supports both short and full value calling conventions?

## Answer

**Yes.** All 10 conditions pass with binding_accuracy=1.0. Both short and full value calling conventions work with the same mechanism. The C2 blocker is resolved without regressions.

## Key Results

| Condition | Slot Count | Binding Accuracy | Status |
|-----------|-----------|-----------------|--------|
| B1 (single-path) | 1 | 1.0 | PASS |
| B2 (path-and-body) | 2 | 1.0 | PASS |
| B3 (path-body-headers) | 3 | 1.0 | PASS |
| B4 (non-identifier-values) | 1 | 1.0 | PASS |
| B5 (shared-slot-name) | 1 | 1.0 | PASS |
| C1 (prefix+suffix URL) | 1 | 1.0 | PASS |
| C2 (full-value IDs) | 1 | 1.0 | PASS |
| D1 (noisy POST) | 3 | 1.0 | PASS |
| D2 (noisy GET) | 1 | 1.0 | PASS |
| D3 (varying preconditions) | 1 | 1.0 | PASS |
| E1 (null: pattern absence) | 0 | — | PASS |
| E2 (null: single obs) | 0 | — | PASS |
| B_LITERAL (baseline) | — | — | PASS (fail_rate=1.0) |

**Overall binding accuracy**: 27/27 = 1.0

## Mechanism

### Bind-Time Slot-Level Prefix Extraction

The implementation adds three components:

1. **`slot_prefixes` field on `Mechanism`**: Stores the slot-level prefix for each parameter slot (e.g., `{'url': 'user-', 'callback_url': 'site-'}`).

2. **`distill_parameterized()` method**: Detects slot-level prefixes from training value distribution. Template retains the FULL prefix (no distill-time stripping). Slot prefixes are stored as metadata.

3. **Modified `_bind()` with prefix parameter**: At bind-time, checks if the parameter value starts with the stored prefix. If yes, strips prefix before substitution (avoids double-prefix). If no, substitutes directly (template prefix is applied).

### How It Handles Mixed Conventions

**Short value** `d` into template `https://site-${callback_url}.com/hook` with prefix `site-`:
- `d` does not start with `site-` → substitute directly → `https://site-d.com/hook` ✓

**Full value** `site-d` into same template:
- `site-d` starts with `site-` → strip prefix → `d` → substitute → `https://site-d.com/hook` ✓

This resolves the VALUE CONTRACT problem from parent EXP-PRODUCT-34282620394, where distill-time stripping mandated full-value-only convention and broke 4/9 conditions.

## Comparison with Prior Experiments

| Experiment | Strategy | C2 | Regressions | Verdict |
|-----------|----------|-----|------------|---------|
| EXP-PRODUCT-34015741916 | No parameterization | FAIL | — | PARTIAL |
| EXP-PRODUCT-34195008089 | `_bind()` prefix-strip (full template prefix) | FAIL | — | FALSIFIED |
| EXP-PRODUCT-34282620394 | Distill-time stripping | PASS | 4/9 FAIL | FALSIFIED |
| **EXP-PRODUCT-34420092879** | **Bind-time slot-level prefix extraction** | **PASS** | **0/9 FAIL** | **SUPPORTS** |

## Implementation Changes

- **`src/spider/models.py`**: Added `slot_prefixes: dict[str, str]` field to `Mechanism` dataclass.
- **`src/spider/kernel.py`**: Added `distill_parameterized()` method, modified `_bind()` to accept optional `prefixes` parameter, updated `resolve()` to pass `slot_prefixes` to `_bind()`, added helper functions for parameter induction.

## Validity Threats

1. **Synthetic-to-real gap**: All conditions use deterministic synthetic data. Real-browser behavior not tested.
2. **Prefix extraction robustness**: Edge cases (no common prefix, multiple candidate prefixes) not tested beyond the 10 conditions.
3. **No model/network/browser**: Pure offline computation. Product economics measurement is a separate experiment.

## Product Consequences

- **If SUPPORTS** (this experiment): C2 resolved. C-PARAM-INHERIT advances. Kernel integration moves from PARTIAL toward complete. Product API can support mixed calling conventions. Unblocks end-to-end product economics measurement.
- **If FALSIFIED** (not this experiment): VALUE CONTRACT problem persists. Product API would need to mandate full-value-only convention or explore hybrid approach.
