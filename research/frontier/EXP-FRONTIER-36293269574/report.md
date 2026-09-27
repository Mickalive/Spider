# EXP-FRONTIER-36293269574 Report

**Lane**: frontier
**Claim**: C-CROSSSITE
**Date**: 2026-09-27T04:34:21.290035+00:00
**Git SHA**: 68173dc18b43860977483bc112491be55142e3f2

## Summary

**Outcome**: MIXED

This experiment measured cross-site transfer on real credential-free public websites with a true holdout (TRAIN sites for distillation, TEST sites never observed during distillation).

## Key Findings

### 1. Architectural Precondition: Stable Identifier Prevalence

| Metric | Value |
|--------|-------|
| Stable identifier prevalence | 0.060 (3/50 action-gating spans) |
| Session-scoped prevalence | 0.000 (0/50) |
| F1 threshold (<= 0.10) | FAILS |

**Per-site breakdown:**
- **https://api.ipify.org**: stable=0, session=0, absent=0, prevalence=0.000
- **https://dog.ceo**: stable=0, session=0, absent=0, prevalence=0.000
- **https://catfact.ninja**: stable=1, session=0, absent=0, prevalence=0.100
- **https://api.chucknorris.io**: stable=1, session=0, absent=0, prevalence=0.100
- **https://zenquotes.io**: stable=1, session=0, absent=3, prevalence=0.100


### 2. Arm Performance

| Arm | Correctness | Abstention | False Replay | Amortized Cost/ep |
|-----|-------------|------------|--------------|-------------------|
| INHERITED_PARAMETERIZED | 0.0000 | 0.0000 | 0.0000 | 0.00 |
| NULL_STATE_KEYED | 1.0000 | 0.0000 | 0.0000 | 241.88 |
| COLD_REEXPLORATION | 1.0000 | 0.0000 | 0.0000 | 240.00 |
| NO_MEMORY_DETERMINISTIC | 1.0000 | 0.0000 | 0.0000 | 240.00 |
| WITHIN_EPISODE_SCRATCHPAD | 1.0000 | 0.0000 | 0.0000 | 240.00 |
| ORACLE_PERFECT_TRANSFER | 1.0000 | 0.0000 | 0.0000 | 252.00 |


### 3. Falsification Conditions

| Condition | Threshold | Observed | Result |
|-----------|-----------|----------|--------|
| F1: Stable prevalence | > 0.10 | 0.060 | FAIL |
| F2: INH correctness > COLD + 0.05 | > 1.050 | 0.000 | FAIL |
| F3: INH abstention < 0.50 | < 0.50 | 0.000 | PASS |
| F4: INH cost < COLD | < 240.00 | 0.0 | PASS |
| F5: INH cost < NOMEM | < 240.00 | 0.0 | PASS |
| F6: NULL false replay >= 0.05 | >= 0.05 | 0.000 | FAIL |
| F7: Mechanism available | Yes | No | FAIL |

### 4. Outcome Interpretation

**MIXED**



## Validity Notes

- INHERITED_PARAMETERIZED arm unavailable - src/spider/kernel.py lacks distill_parameterized method; distill() hardcodes confidence=0.5 < min_confidence=0.8
- TEST sites are read-only public APIs (no CREATE/UPDATE/DELETE support); task family adapted to available operations
- Minimal structural observation tokens vary by site (35-200 tokens) vs 763-token baseline from EXP-INTEL-36287179392 (HTML pages)
- Identifier detection uses heuristic patterns; may miss site-specific identifier schemas
- NULL_STATE_KEYED false replay measurement limited by read-only API nature (fewer gating objects)
- No site identity leakage prevention verified by audit (mechanisms are stateless functions)
- Cost ledger uses token + request + verification + repair units; no model API calls


## Unresolved Questions

- Whether parameterized mechanism would transfer if available
- Whether stable identifier prevalence > 0.10 holds on broader Web sample
- Whether NULL_STATE_KEYED false replay rate would be >= 0.05 on read-write sites with CSRF/session identifiers
- Exact token cost mapping to real model API pricing
