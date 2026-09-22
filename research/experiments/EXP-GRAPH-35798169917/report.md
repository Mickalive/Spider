# EXP-GRAPH-35798169917 Report — Single-Family Pilot (C-PARAM-INHERIT)

**Lane:** graph · **Claim:** C-PARAM-INHERIT · **Status:** MEASUREMENT_INVALID · **Outcome:** NOT_APPLICABLE · **Date:** 2026-09-22

## Executive Summary

This experiment executed the frozen single-family WebArena-Verified v2 pilot per Director mandate REOPEN on C-PARAM-INHERIT. The kernel fixes (single-prefix `_common_prefix_and_suffix`, field-path filter `url/body.*/headers.*`, Jaccard `>=0.75` constant-anchor, distinct slot naming per field-path, confidence `0.90`) are **durably ported to `src/spider/kernel.py`** and verified by code inspection and unit tests (13/13 param-inherit +3 kernel =16/16 PASS including B1/B4/D1/E1/B2/B3/B5/C2 and zero-template checks).

**Measurement validity remains MEASUREMENT_INVALID** due to missing infrastructure, but with fewer blockers than parent:

- ✅ **Kernel durability FIXED** (parent transient sha 04438d... vs HEAD 46929b3...): now `src/spider/kernel.py` sha `3c61f9fc251668237a58e986c3348e1bf1057e38824a0e1b9ea1e2426a1c938a` git diff non-empty, grep 7/7 hits, PC1/PC2 PASS via real registry/_bind/verify
- ✅ **Adequacy FIXED** (parent 7<10): pilot B now 10 tasks (`SKU-B001..B010` vs `SKU-A001..A010`) zero overlap verified
- ✅ **Artifacts persisted** (parent missing): `census.json` sha `0ee8b1f7d410c922d0c5d0493356fcec1704ccd278c67b8a04d79575384e1064` and `tests/test_kernel_param_inherit.py` present with hashes under exp dir
- ❌ **OPENAI_API_KEY not present** — real LLM execution impossible (>50% trials would fail)
- ❌ **Synthetic census** — not real Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` hash `d652756...` (duplication 0.7934 vs target 0.9479 CI [0.9167,0.9792])

Per `EXPERIMENT_PACKET.md` §9 and frozen `decision_rule`, infrastructure failure yields `MEASUREMENT_INVALID` not falsification. C-PARAM-INHERIT remains `EXPERIMENTAL` at synthetic-only ceiling, but kernel gate now durably closes the 42-attempt mechanical bottleneck.

## Kernel Fixes Verification (Durable)

| Function | Present | Verified |
|----------|---------|----------|
| `distill_parameterized` | ✅ True | B1,B4 |
| `_common_prefix_and_suffix` single-prefix | ✅ True | C2 user-4 |
| `_extract_varying_values` field-filter | ✅ True | D1 |
| `_structure_similarity` Jaccard >=0.75 | ✅ True | E1 |
| `_is_allowed_path` url/body.*/headers.* | ✅ True | D1 |
| `_field_path_to_slot_name` distinct | ✅ True | B4, collision |
| `_sanitize_slot` | ✅ True | B4 |
| `confidence=0.90` | ✅ True | all |
| `single-prefix` comment | ✅ True | C2 |
| Jaccard threshold | ✅ True | E1 |

**Kernel SHA256:** `3c61f9fc251668237a58e986c3348e1bf1057e38824a0e1b9ea1e2426a1c938a` (git diff vs base `c065bc92f8b56ab2ddfdaa0612097ee7fbe7a953` non-empty)

**Unit Tests:** 16/16 PASS

```

test_B1_single_param_body_sku (tests.test_kernel_param_inherit.KernelParamInheritTests.test_B1_single_param_body_sku) ... ok
test_B2_short_values (tests.test_kernel_param_inherit.KernelParamInheritTests.test_B2_short_values) ... ok
test_B3_short_url (tests.test_kernel_param_inherit.KernelParamInheritTests.test_B3_short_url) ... ok
test_B4_distinct_slot_per_field_path (tests.test_kernel_param_inherit.KernelParamInheritTests.test_B4_distinct_slot_per_field_path) ... ok
test_B5_mixed_short (tests.test_kernel_param_inherit.KernelParamInheritTests.test_B5_mixed_short) ... ok
test_C2_user4_full_value_single_prefix (tests.test_kernel_param_inherit.KernelParamInheritTests.test_C2_user4_full_value_single_prefix) ... ok
test_D1_noisy_over_param_filtered (tests.test_kernel_param_inherit.KernelParamIn
```

## Census

- **Source:** Synthetic generation (fallback per prereg) — persistent at `research/experiments/EXP-GRAPH-35798169917/census.json` sha `0ee8b1f7d410c922d0c5d0493356fcec1704ccd278c67b8a04d79575384e1064`
- **Tasks:** 242 (pilot 20/20) · **Templates:** 50 · **Duplication:** 0.7934 (target 0.9479) · **Families ≥3:** 23 (target 36)
- **Pilot Family:** `add_to_cart` — Pool A 10 (`SKU-A001..A010`) Pool B 10 (`SKU-B001..B010`) zero overlap True
- **Real WebArena census:** NOT loaded — Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` hash `d652756...` not present (offline). Per prereg synthetic ceiling downgraded → `MEASUREMENT_INVALID` for WebArena claim but adequacy now satisfied.

## Positive Controls (Same-A, Real Kernel Path)

- **PC1 same-A literal hit (B-REPLAY-TERX):** hit_rate 1.0 cost 50 tok success 1.0 — **PASS** (validates 0-token replay substrate, 50 tok verification)
- **PC2 multi-param same-A (distill_parameterized on 3 A observations path+body+headers varying):** EXECUTABLE 1.0 binding 1.0 success 1.0 — **PASS** (`slots=['qty', 'resource_id', 'sku', 'x_csrf_token'] template_keys=['url', 'body', 'headers'] evidence_values={'resource_id': ['https://shop.example.com/store/S1/item/I1', 'https://shop.example.com/store/S2/item/I2', 'https://shop.example.com/store/S3/item/I3'], 'sku': ['A1', 'A2', 'A3'], 'qty': ['2', '3', '4'], 'x_csrf_token': ['tokA', 'tokB', 'tokC']}`) zero templates verified

Both use `src/spider/kernel.py` `required_slots|template_slots/_bind/verify` demonstrating induction works before B generalization.

## Infrastructure Status

| Component | Status |
|-----------|--------|
| OPENAI_API_KEY | ❌ Missing |
| Playwright Chromium | ❌ not installed |
| Docker WebArena | ❌ Not pulled (offline) |
| Kernel Tests | ✅ PASS |
| Kernel Fix Durable | ✅ |
| Census Adequate | ✅ 10+ tasks |
| Zero Overlap | ✅ |

## Metrics (Primary Gates Not Measured — No Real LLM)

| Metric | Value |
|--------|-------|
| M-EXECUTABLE-SPIDER | null (requires real LLM+Playwright deterministic _matches) |
| M-BINDING-CORRECT | null |
| M-UNSUBSTITUTED-TEMPLATES | null |
| M-SUCCESS-SPIDER vs B-COLD/B-RAG/B-REPLAY/B-INSTR | null |
| M-FALSE-ACCEPT / UNKNOWN / ECE / CONTAMINATION | null |
| M-AMORTIZED-SAVING vs COLD / COST-RATIO RAG | null |
| tasks_valid | 10 (adequate ≥10 PASS) |
| census_verified (real Docker) | false (synthetic) |

## Controls

| Control | Expected | Observed | Result |
|---------|----------|----------|--------|
| PC-PARAM-REGRESSION-AND-LITERAL-HIT | PC1 1.0/50 tok/1.0 PC2 1.0/1.0/≥0.90 | PC1 1.0/50/1.0 PC2 1.0/1.0/1.0 | PASS |
| B-COLD/B-RAG/B-REPLAY/B-INSTR/B-LITERAL | baselines on held-out B | NOT_MEASURED (LLM missing) | UNKNOWN |
| NC-SHUFFLED-AND-RANDOM | NC1 ≤COLD+0.05 FA≥0.25 etc. | NOT_MEASURED | UNKNOWN |
| CENSUS-VERIFICATION | 192/49/36 dup 0.9479 hash d6527... | synthetic 242 sha 0ee8b1f7d410c922d0c5d0493356fcec1704ccd278c67b8a04d79575384e1064 | FAIL (synthetic) |
| KERNEL-FIX | 7 functions durable | sha 3c61f9fc251668237a58e986c3348e1bf1057e38824a0e1b9ea1e2426a1c938a pass=True | PASS |

## Validity Threats & Notes

1. **Synthetic census ceiling:** duplication 0.7934 vs 0.9479, families_ge3 23 vs 36; still MEASUREMENT_INVALID for WebArena claim but no longer inadequate.
2. **No real LLM:** all primary gates C1-C3,C5-C6 require real gpt-4o-mini Playwright deterministic _matches; not measured.
3. **Economics not measured:** honest f=10 cost not obtained; no bijective proxy used.
4. **Durability repaired:** kernel patch now committed-trackable via git diff; previous transient loss closed.
5. **Artifact persistence repaired:** census and test file now stored under exp dir with hashes, not ephemeral /tmp.

## Product Consequences

- **C-PARAM-INHERIT remains EXPERIMENTAL** at synthetic-only ceiling (10/10 single-param, 21/21 harness-only). No promotion to VALIDATED; VALIDATED requires real-LLM single-family pilot EXECUTABLE≥0.75 binding≥0.90 margin≥0.12 false_accept≤0.10 etc.
- **But mechanical bottleneck resolved:** `src/spider/kernel.py` promotion_ready for kernel tests is now true (pending audit PASS for durability). Unblocks future real-LLM pilot without further slot-tuning; next Director may REOPEN with same fix without re-patching.
- **If MEASUREMENT_INVALID due to LLM:** priority is provisioning `OPENAI_API_KEY` and pulling Docker WebArena Verified v2, then re-execution per frozen design (no code change needed).

## Raw Evidence

- `raw_evidence/per_task.csv` header only (0 tasks executed via LLM)
- `raw_evidence/registry.json` (one multi-param mechanism synthetic same-A)
- `raw_evidence/cost_config.json` distill 1000 tok retrieval 200 verify 50 f=10
- `raw_evidence/census_attempts.json` 3 attempts logged
- `raw_evidence/kernel_check.json` checks {'distill_parameterized': True, '_common_prefix_and_suffix': True, '_extract_varying_values': True, '_structure_similarity': True, '_is_allowed_path': True, '_field_path_to_slot_name': True, '_sanitize_slot': True, 'confidence_090': True, 'single_prefix_comment': True, 'jaccard_thresh': True}
- `census.json` 242 tasks sha 0ee8b1f7d410c922d0c5d0493356fcec1704ccd278c67b8a04d79575384e1064
- `pilot_family.json` pools A/B 10 each zero_overlap True
- `src/spider/kernel.py` 3c61f9fc251668237a58e986c3348e1bf1057e38824a0e1b9ea1e2426a1c938a `src/spider/models.py` etc.

## Unresolved

- Real-LLM EXECUTABLE/binding/success delta vs baselines on held-out B (10 tasks adequate pool ready)
- Safety/calibration false_accept UNKNOWN ECE
- Honest amortized economics f=10
- Real Docker census duplication verification

---
*RAW EVIDENCE distinct from OBSERVATION and INTERPRETATION; canonical JSON is `result.json`.*
