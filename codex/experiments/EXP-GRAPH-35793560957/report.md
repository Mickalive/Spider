# EXP-GRAPH-35793560957 Report — Single-Family Pilot (C-PARAM-INHERIT)

**Lane:** graph · **Claim:** C-PARAM-INHERIT · **Status:** MEASUREMENT_INVALID · **Date:** 2026-09-22

## Executive Summary

This experiment attempted to execute the frozen single-family WebArena-Verified v2 pilot per Director mandate CONTINUE on C-PARAM-INHERIT. The kernel fixes (single-prefix `_common_prefix_and_suffix`, field-path relevance filter `url/body.*/headers.*`, Jaccard `>=0.75` constant-anchor, distinct slot naming per field-path, confidence `0.90`) were implemented in `src/spider/kernel.py` and verified by code inspection and unit tests (13/13 tests PASS including B1/B4/D1/E1/B2/B3/B5/C2).

However, **measurement validity was not achieved** due to missing infrastructure:
- **OPENAI_API_KEY not present** - real LLM execution impossible
- **Synthetic WebArena census used** - not real Docker data (ceiling downgraded per prereg)

Per `EXPERIMENT_PACKET.md` §9 and frozen `decision_rule`, infrastructure failure yields `MEASUREMENT_INVALID` not falsification. C-PARAM-INHERIT remains `EXPERIMENTAL` at synthetic-only ceiling.

## Kernel Fixes Verification

| Function | Present | Verified by Tests |
|----------|---------|-------------------|
| `distill_parameterized` | ✅ | B1, B4 |
| `_common_prefix_and_suffix` (single-prefix) | ✅ | C2 |
| `_extract_varying_values` (field-path filter) | ✅ | D1 |
| `_structure_similarity` (Jaccard >=0.75) | ✅ | E1 |
| `_is_allowed_path` (url/body.*/headers.*) | ✅ | D1 |
| `_field_path_to_slot_name` (distinct slots) | ✅ | B4, distinct_slot test |
| `_sanitize_slot` | ✅ | B4, distinct_slot test |

**Kernel SHA256:** `04438d0ecd91113e4367a5d6de0e7b357f141ea67495778f44668da17f3853f6`

**Unit Tests:** 16/16 PASS (3 existing + 13 new)

## WebArena Census

- **Source:** Synthetic generation matching target statistics (fallback per prereg)
- **Path:** `/home/runner/work/Spider/Spider/data/webarena_verified_v2.json`
- **SHA256:** `f55c34141105a77b14db2420e43f48234b4391a27196daabc69bbeb32974f9c6`
- **Tasks:** 275
- **Templates:** 50
- **Duplication:** 0.8182 (target 0.9479)
- **Exact Copy:** 0.0291 (target 0.0781)
- **Param Task:** 0.8982 (target 0.8958)
- **Param Template:** 1.0000 (target 0.8367)
- **Families ≥3:** 44 (target 36)
- **Families ≥4:** 44 (target 34)
- **Families ≥5:** 44 (target 33)

> **Validity Note:** Synthetic census does not meet prereg target statistics exactly. Per prereg: "fallback synthetic mock requires ceiling downgrade and then MEASUREMENT_INVALID for WebArena claim."

## Pilot Family Selection

- **Family:** `add_to_cart` (`Add {sku} to cart`)
- **Pool A (train):** 7 tasks (SKU-A001 to SKU-A007)
- **Pool B (test):** 7 tasks (SKU-B001 to SKU-B007)
- **Exemplars for training:** 5 (3-5 per spec)
- **Zero Overlap Verified:** True

Pool A values: `['SKU-A001', 'SKU-A002', 'SKU-A003', 'SKU-A004', 'SKU-A005', 'SKU-A006', 'SKU-A007']`
Pool B values: `['SKU-B001', 'SKU-B002', 'SKU-B003', 'SKU-B004', 'SKU-B005', 'SKU-B006', 'SKU-B007']`

## Infrastructure Status

| Component | Status | Details |
|-----------|--------|---------|
| OPENAI_API_KEY | ❌ Missing | `api_key_present: false` |
| Playwright Chromium | ✅ Available | Version: installed |
| Docker | ✅ Available | WebArena container: False |
| Kernel Tests | ✅ PASS | 16/16 tests |
| Kernel Fixes | ✅ Verified | All 7 required functions present |

## Measurement Validity Assessment

**Result: MEASUREMENT_INVALID**

Per frozen `spec.json` `measurement_validity` clause 1, 2, 4, 7 and `decision_rule` adequacy rule:
- ✅ Kernel fixes ported to `src/spider/kernel.py` and verified (code inspection + unit tests)
- ✅ Synthetic census loaded with pilot family ≥10 tasks, zero-overlap proven
- ❌ **Real LLM execution not possible** (OPENAI_API_KEY absent, >50% trials would fail)
- ❌ **Real WebArena data not used** (synthetic fallback, ceiling downgraded)
- ❌ **Positive/negative controls not exercised** (require real LLM+Playwright)

Per `EXPERIMENT_PACKET.md` §9: "Infrastructure or substrate failure must never be encoded as scientific falsification."

## Metrics (All NULL - Not Measured)

| Metric | Value | Wilson 95% CI | Status |
|--------|-------|---------------|--------|
| M-EXECUTABLE-SPIDER | null | — | NOT_MEASURED |
| M-BINDING-CORRECT | null | — | NOT_MEASURED |
| M-UNSUBSTITUTED-TEMPLATES | null | — | NOT_MEASURED |
| M-SUCCESS-SPIDER | null | — | NOT_MEASURED |
| M-SUCCESS-COLD | null | — | NOT_MEASURED |
| M-SUCCESS-RAG | null | — | NOT_MEASURED |
| M-SUCCESS-REPLAY | null | — | NOT_MEASURED |
| M-SUCCESS-INSTR | null | — | NOT_MEASURED |
| M-SUCCESS-LITERAL | null | — | NOT_MEASURED |
| M-FALSE-ACCEPT-SPIDER | null | — | NOT_MEASURED |
| M-UNKNOWN-RATE | null | — | NOT_MEASURED |
| M-ECE | null | — | NOT_MEASURED |
| M-AMORTIZED-SAVING-vs-COLD | null | — | NOT_MEASURED |
| M-COST-RATIO-RAG | null | — | NOT_MEASURED |

## Controls (All NOT_MEASURED)

| Control | Expected | Observed | Status |
|---------|----------|----------|--------|
| PC-PARAM-REGRESSION-AND-LITERAL-HIT (PC1/PC2) | PASS | NOT_MEASURED | Infrastructure |
| NC-SHUFFLED-AND-RANDOM (NC1/NC2) | Null pattern | NOT_MEASURED | Infrastructure |
| B-COLD | Baseline | NOT_MEASURED | Infrastructure |
| B-RAG | Baseline | NOT_MEASURED | Infrastructure |
| B-REPLAY-TERX | Baseline | NOT_MEASURED | Infrastructure |
| B-INSTR | Baseline | NOT_MEASURED | Infrastructure |
| B-LITERAL | Leakage check | NOT_MEASURED | Infrastructure |

## Validity Threats

1. **Synthetic Census Ceiling**: Synthetic data does not replicate real WebArena distribution exactly. Duplication 0.8182 vs target 0.9479, exact_copy 0.0291 vs 0.0781. Per prereg, this requires ceiling downgrade to MEASUREMENT_INVALID for WebArena claim.

2. **No Real LLM Execution**: All primary metrics require real `gpt-4o-mini-2024-07-18` (or equivalent) with Playwright. Without API key, no outcome-bearing measurement obtained.

3. **Kernel Not Exercised End-to-End**: While unit tests pass, the `distill_parameterized` → registry → `resolve` → `_bind` → Playwright → `_matches` pipeline was not exercised on real held-out B tasks.

4. **Controls Not Executed**: PC1, PC2, NC1, NC2, and all baselines require real execution substrate.

## Unresolved Questions

1. Does genuinely fixed `distill_parameterized` enable real-LLM A→B transfer on WebArena-Verified v2 single-family hold-out?
2. Does SPIDER achieve EXECUTABLE ≥0.75, binding ≥0.90, margin ≥0.12 vs baselines on real substrate?
3. Do safety/calibration gates hold (false_accept ≤0.10, UNKNOWN ∈ [0,0.15], ECE ≤0.15)?
4. Do honest amortized economics show ≥25% saving vs COLD at f=10?

## Next Steps (per handoff.do_not_assume and Director portfolio)

1. **Provision OPENAI_API_KEY** for `gpt-4o-mini-2024-07-18` (or approved haiku/flash equivalent)
2. **Pull WebArena Docker** `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` and extract real census
3. **Re-execute frozen spec** with real LLM+Playwright on identical held-out B set
4. **If substrate remains unavailable**, Global Research Director to pivot Graph to orthogonal question per `research/portfolio/POLICY.md`

---

*This report preserves RAW EVIDENCE (kernel code, test results, census statistics) distinct from OBSERVATION (infrastructure status) and INTERPRETATION (MEASUREMENT_INVALID classification). No material fact exists only in this narrative; canonical JSON is `result.json`.*
