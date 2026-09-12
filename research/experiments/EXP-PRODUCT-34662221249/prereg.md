# EXP-PRODUCT-34662221249 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-PRODUCT-34662221249
- **Lane**: Product
- **Claim**: C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers)
- **Parent**: EXP-PRODUCT-34642376433 (standalone fixes validated, V3 substrate gap)
- **Date**: 2026-09-12
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can the suffix guard (Fix1) and delimiter-bound prefix validation (Fix2, last-char variant) be applied to actual src/spider/kernel.py distill_parameterized and _bind, producing correct binding outcomes for all established conditions with no regressions, and correctly rejecting parameterization on the N1_ORIGINAL null control?

## 3. Motivation

EXP-PRODUCT-34642376433 validated two bounded fixes in standalone reimplementation:
- Fix1 (suffix guard): restores G1 binding by rejecting single-char suffixes not preceded by structural delimiters
- Fix2 (delimiter-bound prefix validation): prevents N1_ORIGINAL over-parameterization by requiring prefix to end at a structural delimiter

All 5 established conditions (P1, G2, G3, G5) maintained binding_accuracy=1.0 with no regressions.

However, audit V3 identified the critical gap: fixes were tested in standalone reimplementation, not actual src/spider/kernel.py. The kernel.py at HEAD has literal-only distill (no parameterization) and _bind without prefix stripping. The standalone reimplementation's _bind ignores the slot_prefixes dict that kernel.py would use for VALUE CONTRACT stripping.

The parent handoff explicitly requires validation against actual kernel.py before C-PRODUCT-ECON can proceed.

## 4. Hypotheses

### H1: Kernel Integration
Fix1 and Fix2 patches applied to actual kernel.py produce the same binding outcomes as the standalone reimplementation for all 5 established conditions (P1, G1, G2, G3, G5): slot_count=1, binding_accuracy=1.0.

### H2: Fix1 in Kernel
G1 binding_accuracy=1.0 after Fix1 patch in kernel.py (suffix guard removes 'a' suffix from template search?q=${url}a).

### H3: Fix2 in Kernel
N1_ORIGINAL slot_count=0 after Fix2 patch in kernel.py (delimiter guard rejects prefix 'https://api' ending at '.').

### H4: No Regressions
P1, G2, G3, G5 remain at binding_accuracy=1.0 after patches (no regressions on established conditions).

### H5: Baseline Preservation
B_LITERAL fail_rate=1.0 (literal baseline unaffected by parameterization patches).

## 5. Code Changes to kernel.py

### 5.1 _find_common_prefix_suffix (with Fix1)

```python
def _find_common_prefix_suffix(values: list[str]) -> tuple[str, str]:
    if not values:
        return "", ""
    # Common prefix
    prefix = values[0]
    for v in values[1:]:
        while not v.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                break
    # Common suffix (raw)
    suffix = values[0]
    for v in values[1:]:
        while not v.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                break
    # FIX 1: Suffix Guard — reject single-char suffixes not preceded by structural delimiters
    if suffix and len(suffix) <= 1:
        pos = len(values[0]) - len(suffix) - 1
        if pos < 0 or values[0][pos] not in ('?', '=', '&'):
            suffix = ''
    return prefix, suffix
```

### 5.2 _validate_prefix_boundary (with Fix2)

```python
def _validate_prefix_boundary(full_prefix: str) -> bool:
    """Require prefix to end at structural delimiter: / ? = & or EOS."""
    if not full_prefix:
        return True
    last_char = full_prefix[-1]
    return last_char in ('/', '?', '=', '&')
```

Note: Uses last_char of prefix (not next_char after prefix). This is the correct logic validated in EXP-PRODUCT-34642376433 — next_char logic would false-reject P1/G1.

### 5.3 distill_parameterized

```python
def distill_parameterized(self, observations: list[Observation]) -> Mechanism | None:
    # Leaf-path extraction from observations
    # Path-value analysis across successful observations
    # Fix1: _find_common_prefix_suffix for suffix rejection
    # Fix2: _validate_prefix_boundary for prefix rejection
    # Template construction with ${slot} placeholders
    # slot_prefixes metadata extraction via rfind('/')
    # Returns Mechanism with parameter_slots and slot_prefixes
```

### 5.4 models.py — Mechanism.slot_prefixes

Add to Mechanism dataclass:
```python
slot_prefixes: dict[str, str] = field(default_factory=dict)
```

### 5.5 _bind — No Changes

`_bind` remains template-substitution-only. slot_prefixes is metadata, not used in substitution. All 5 established conditions produce templates with full prefix already embedded (e.g., `https://api.example.com/users/${url}`).

## 6. Test Conditions

### 6.1 Established Conditions (should pass with fixes)

| ID | Type | Training URLs | Unseen | Expected slot_count | Expected binding |
|----|------|--------------|--------|--------------------|--------------------|
| P1 | path-prefix | https://api.example.com/users/{A,B,C} | D,E,F | 1 | 1.0 |
| G1 | query-string | https://api.example.com/search?q={alpha,beta,delta} | gamma,epsilon,zeta | 1 | 1.0 |
| G2 | multi-param | https://api.example.com/items?category=books&page={1,2,3} | 4,5,6 | 1 | 1.0 |
| G3 | deep-path | https://api.example.com/orgs/acme/repos/main/issues/{1,2,3} | 4,5,6 | 1 | 1.0 |
| G5 | path+query | https://api.example.com/users/{alice,bob,charlie}/items?page=1 | dave,eve,frank | 1 | 1.0 |

### 6.2 Null Control

| ID | Type | Training URLs | Unseen | Expected slot_count |
|----|------|--------------|--------|--------------------|
| N1_ORIGINAL | fix2_target | https://api.{example,other,third}.com/{a,b,c} | x,y,z | 0 |

### 6.3 Baselines

| ID | Type | Expected |
|----|------|----------|
| B_LITERAL | baseline | fail_rate=1.0 (confidence 0.5 < 0.8) |
| B_UNFIXED | paired_comparison | ~4/7 pass (G1/N1 fail without fixes) |

### 6.4 Architectural Bound (reported separately)

| ID | Type | Expected slot_count | Expected binding | Note |
|----|------|--------------------|--------------------|------|
| G4 | architectural | 1 | 0.0 | Multi-char suffix '00' not caught by Fix1; single-slot leaf-path bound |

## 7. Controls

### 7.1 Positive Control (P1)
- Verifies: pipeline works after patches to kernel.py
- Expected: slot_count=1, binding_accuracy=1.0

### 7.2 Null Control (N1_ORIGINAL)
- Verifies: Fix2 rejects non-delimiter-bound prefixes
- Expected: slot_count=0

### 7.3 Baseline Control (B_LITERAL)
- Verifies: parameterized induction is necessary
- Expected: fail_rate=1.0

### 7.4 Paired Comparison (B_UNFIXED)
- Verifies: fixes improve over unfixed heuristic
- Expected: B_UNFIXED ~4/7 pass vs fixed ~8/8 pass

## 8. Decision Rules

### 8.1 SURVIVES_CURRENT_TEST
If ALL of:
1. P1 slot_count=1 AND binding_accuracy=1.0
2. G1 slot_count=1 AND binding_accuracy=1.0
3. G2 slot_count=1 AND binding_accuracy=1.0
4. G3 slot_count=1 AND binding_accuracy=1.0
5. G5 slot_count=1 AND binding_accuracy=1.0
6. N1_ORIGINAL slot_count=0
7. B_LITERAL fail_rate=1.0
8. No import/syntax errors in patched kernel.py

### 8.2 MIXED
If Fix1 or Fix2 works partially (at least one of G1 or N1_ORIGINAL passes) but no regressions on P1/G2/G3/G5.

### 8.3 FALSIFIED-IN-SETTING
If any established condition (P1/G2/G3/G5) drops below binding_accuracy=1.0 (regression), OR both G1 and N1_ORIGINAL fail.

### 8.4 MEASUREMENT_INVALID
If patches cause import/syntax errors preventing kernel.py from loading.

## 9. Validity Threats

### 9.1 Kernel.py at HEAD is Literal-Only
Current kernel.py distill() produces literal mechanisms with confidence 0.5. Adding distill_parameterized is a non-trivial code change. If the addition introduces bugs, the failure is infrastructure, not scientific falsification.

### 9.2 Monkey-Patching vs Direct Modification
The test script patches kernel.py functions rather than committing changes. This validates logical correctness but not production integration. Committing patches to kernel.py is a separate decision.

### 9.3 Synthetic Data
All conditions use n=3 deterministic synthetic URLs, no model/network/browser calls. Generalization beyond tested URL classes unproven. This is the same scope as parent experiments.

### 9.4 slot_prefixes Metadata vs Binding
slot_prefixes is metadata only — binding works via template substitution. The empty slot_prefixes for P1/G3/G5 (rfind('/') returns empty when varying part starts after last '/') is a representation loss but not a binding failure. This is the same behavior as parent.

### 9.5 Fix1 Single-Char Bound
Fix1 guards len(suffix)<=1 only. G4 suffix '00' (2-char) not caught. Claim bounded to single-char coincidental overlap.

### 9.6 Fix2 No Minimum Prefix Length
Fix2 does not enforce minimum prefix length. Protocol-only prefixes like 'http' (4 chars) that don't end at delimiter are correctly rejected. Prefixes like 'http://' (7 chars) ending at '/' are accepted — this may allow over-parameterization of protocol-only patterns. Documented as unresolved; not blocking for this experiment.

## 10. Expected Outcomes

### 10.1 SURVIVES_CURRENT_TEST
- Fixes validated against actual kernel.py
- C-PARAM-INHERIT claim ceiling advances to 'kernel-validated synthetic'
- C-PRODUCT-ECON unblocked for next measurement
- Clears V3 audit gap from EXP-PRODUCT-34642376433

### 10.2 MIXED
- Fixes partially work in kernel.py
- Need to diagnose kernel-specific divergence for failing conditions
- C-PARAM-INHERIT remains EXPERIMENTAL

### 10.3 FALSIFIED-IN-SETTING
- Fixes fail in kernel.py despite passing in standalone
- Kernel code paths diverge materially from reimplementation
- Need deep diagnosis of kernel.py binding behavior

### 10.4 MEASUREMENT_INVALID
- Patches cause kernel.py errors
- Infrastructure issue, not scientific finding

## 11. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 12. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
