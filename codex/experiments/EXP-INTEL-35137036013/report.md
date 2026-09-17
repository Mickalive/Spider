# EXP-INTEL-35137036013 — Execution Report

**Lane:** intel  
**Experiment ID:** EXP-INTEL-35137036013  
**Claim IDs:** C-MEAS-VALID  
**Status:** MEASUREMENT_INVALID  
**Outcome:** NOT_APPLICABLE  
**Parent:** EXP-INTEL-35131994346 (PROVENANCE_PARTIAL)  
**Chain:** 34782350557 → 35112013458 (FALSIFIED) → 35124660457 (MEASUREMENT_INVALID) → 35131994346 (PROVENANCE_PARTIAL) → **this experiment**  
**Execution:** 2026-09-16T19:04:08Z, github_run_id 35137036013, base_sha 0a99476d

---

## 1. Scientific Question (frozen)

> After the runtime lane removes the first-20 `locatableSample` cap, does full DOM enumeration confirm that the `a→link`-inclusive page-type ordering changes between truncated and full-DOM, and does the null-model pairwise agreement exceed chance on full-DOM data?

## 2. Hypothesis (frozen)

**H1:** Full DOM enumeration produces a different page-type ordering than truncated-first-20 for at least one definition (DEF-FULL-MAP or DEF-FORM-ONLY).

**H2:** On full-DOM data, null-model pairwise agreement mean is at or above observed pairwise agreement (null ≥ observed), confirming the FALSIFIED result was a truncation artifact.

Combined H1 AND H2 → SURVIVES_CURRENT_TEST (truncation drove the FALSIFIED verdict).

## 3. Falsifier (frozen)

If full DOM ordering is identical to truncated for ALL definitions (F1) AND null mean remains > observed as on truncated data (F2) AND canonical script with per-definition filtering reproduces verdict inconsistent with decision rule (F3), then truncation did not drive the FALSIFIED verdict and metric fails under full enumeration. Measurement validity conditions failing → MEASUREMENT_INVALID.

## 4. Method

### 4.1 Frozen inputs (immutable)

- `request.json` sha256 `643b91daec4b9882f577ba4f922d043f4fdf33b8f7d7cfe03c0fa9b57e479a43`
- `spec.json` sha256 `712f4a72b868aaebc1db4e7698d88dcdad4c0d1f4ee490e4a7f412fc23331d51`
- `prereg.md` sha256 `5e26bbb85fd397d4ccbca00168440f2927ed3f13bfec0ec0ca6d8a46da015b6d`
- `freeze.json` sha256 `4968635244466ea7283265844f5055041384c560577e30ada9b70c5f5aa48fa4`
- Raw evidence: `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json` sha256 `da30bd059adb555409784a2fd41402d53b64a25c89aa710b77e686a94a155050` (10 measurements, 8 valid, 7 unique after cart_1 dedup)
- MEASURE_JS: `research/experiments/EXP-INTEL-34718481334/measure_fullpage_yield.py` sha256 `085b58c93be51bc76dc4ad712436500100c077594bd73c1cc1e552b6f68f49a3`

No outcome-bearing measurement was inspected during DESIGN.

### 4.2 Substrate verification (validity gate)

Checked `MEASURE_JS` for cap string. Result: `if (locatableSample.length < 20)` present at line 89 → cap **still present**. Verified `locatable_sample` lengths: all 8 valid measurements have `sample_len=20` while `locatable_elements=82` (listing, n=3), `32` (detail, n=3), `21` (cart, n=1 + duplicate). All tasks with `locatable_elements>20` are capped at 20, discarding 62–95% of interactive elements. Tasks with locatable>20: 8/8. This reproduces audit V1 truncation representation loss.

Checked canonical script: no committed file at `research/intel/canonical_35137036013.py` or `research/experiments/EXP-INTEL-35137036013/canonical_analysis.py`. Blocking code dependency **not implemented** (audit V2_provenance_not_reproducible remains open).

Both frozen `measurement_validity` conditions fail → decision rule mandates MEASUREMENT_INVALID.

### 4.3 Baselines (frozen)

- **B1_TRUCATED_REGRESSION:** Run canonical 3-definition per-role filtering (DEF-FULL-MAP: a+button+input+combobox, DEF-FORM-ONLY: button+combobox, ISOLATED-A-LINK: a only, cart_1 dedup, float scaling) on truncated-first-20 data. Expected to reproduce stored analysis_results.json within ±0.001 density, ordering cart>product_listing>detail truncated vs cart>detail>product_listing full (DEF-FULL-MAP) and product_listing>cart>detail vs product_listing>detail>cart (DEF-FORM-ONLY), and parent null 0.5275 > observed 0.3.
- **B2_COMMITTED_SCRIPT_BASELINE:** Run committed `analyze.py` (all-role density a+button+form+input+combobox+div+label+span, 8 tasks incl. duplicate) on same data (proxy for full-DOM due to no true full enumeration). Documents algorithmic difference.
- **B3_STORED_RESULTS_COMPARISON:** Load `analysis_results.json` from EXP-INTEL-35124660457 (sha256 b2aaafdeeacbc9b39ffba40e4df058099b71b643fb2a2ce79d4b8c08f111d546) for truncated-sample reference values, excluding invalid ISOLATED-A-LINK.

### 4.4 Controls (frozen stable IDs)

- **C_POSITIVE_SCRIPT_REGRESSION:** Canonical script on truncated data reproduces known ordering change (C1=true) and null result.
- **C_NULL_MODEL_RANDOM_ROLE_MAP:** 1000 random ROLE_MAP assignments (seed=42, 8 roles a/button/combobox/div/form/input/label/span, p=0.5) on per-definition full-DOM proxy density estimates (tag-count estimator). Null mean vs observed determines C2.

### 4.5 Derived computation (proxy only)

Because true full DOM enumeration is unavailable, a **proxy estimator** was computed for illustrative comparison: `full_count_estimate` = DOM tag counts for a/button/form/input (`linksCount` 393–397, `buttonsCount` 15/4, etc.) plus scaled sample counts for combobox/div/label/span (scale = locatable_elements/20). Density = count / elements_with_bbox. This is the same estimator used in EXP-INTEL-35124660457 and inherits its 4–7x inflation bias; point estimates are not valid locatable densities and are flagged as such.

Null model: for each random ROLE_MAP, compute full-proxy density per task, then per-type mean and ordering; compute pairwise agreement among 1000 random orderings (agreeing pairs / total pairs). Observed pairwise agreement = agreement among 3 definition orderings (proxy 0.333 for full, 0.0 for truncated, parent 5-def observed 0.3).

All code: `/tmp/opencode/exp35137036013_execute.py` → artifacts `full_dom_proxy_analysis.json` (sha256 5b3c03b4...), `substrate_verification.json` (sha256 bce78e0c...).

No Docker, browser, model calls; offline numpy computation only.

---

## 5. Raw Evidence (distinct from observations)

- **Raw:** `exp347_raw_results.json` — 8 valid measurements (2 checkout_1 errors excluded), frozen_seed 99, docker image am1n3e/webarena-verified-shopping:latest, timestamp 2026-09-12. Each measurement contains `locatable_sample` array length 20 (capped) and `dom_stats` tag counts.
- **Raw:** `measure_fullpage_yield.py` — MEASURE_JS string with `if (locatableSample.length < 20)` truncation (line 89), evidence path for cap.
- **Derived:** `full_dom_proxy_analysis.json` — per-definition per-task truncated/full densities, orderings, null model distributions, decision proxy values.
- **Derived:** `substrate_verification.json` — cap string found = true, per-task sample_len vs locatable_elements table, raw sha256, canonical missing evidence.

Evidence paths and hashes in `result.json:artifacts` and `provenance.json`.

---

## 6. Observations (direct, not interpretations)

1. Substrate fix NOT applied: MEASURE_JS still contains `locatableSample.length < 20` (true) and all 8 tasks with locatable_elements>20 are capped at 20 samples (sample_len 20 vs locatable 82/32/21). This matches audit V1 representation loss.
2. Canonical analysis script NOT committed: no file at expected locations; proxy reconstruction via per-definition role filtering used instead. The committed `analyze.py` (sha256 c2a085bb) uses all-role density and does not deduplicate cart_1.
3. Truncated vs full proxy ordering (estimator, inflates 4–7x): DEF-FULL-MAP `['cart','product_listing','detail']` → `['cart','detail','product_listing']` changed=True; DEF-FORM-ONLY `['product_listing','cart','detail']` → `['product_listing','detail','cart']` changed=True; ISOLATED-A-LINK corrected `['cart','detail','product_listing']` → `['cart','detail','product_listing']` changed=False (correct a-only count ~2 vs stored 8). This reproduces B1 expected orderings exactly.
4. ISOLATED-A-LINK stored bug confirmed: stored truncated_count=8 for listings vs correct a-only 2; byte-identical to DEF-FULL-MAP across all 7 tasks (identical_to_fullmap=True).
5. B1 regression PASS: 2/2 valid definitions reconstruct exactly within tolerance, matching stored results for truncated and full orderings (per audit V2_recomputed_metrics).
6. B2 committed-script baseline: all-role density ordering `['cart','detail','product_listing']` → `['product_listing','detail','cart']` changed=True, opposite direction to per-definition results, documenting algorithmic difference (all-role inflates denominator).
7. Observed pairwise agreement proxy: truncated 3-defs 0.0, full proxy 0.333 (parent 5-def observed 0.3). With 3 definitions, agreement is coarse (0, 0.333, 0.666, 1.0).
8. Null model on full-DOM proxy (1000 iter, seed=42, 8 roles p=0.5): DEF-FULL-MAP null_mean 0.400 top `['product_listing','detail','cart']` 48.1% distinct 6; DEF-FORM-ONLY 0.404 same top 48.2%; ISOLATED 0.421 top 50.9%. These are not directly comparable to parent null_mean 0.5275 (5 defs, different role pool) but same order of magnitude.
9. Deduplication: 8 valid measurements contain duplicate cart_1 (same task_id, 2 entries), deduplicated to 7 unique tasks (removed 1 duplicate) per spec `measurement_validity` #2.
10. Measurement validity FAIL: both blocking conditions fail (cap present AND canonical script missing), so frozen decision rule mandates MEASUREMENT_INVALID irrespective of proxy C1/C2 values (proxy C1=True, proxy C2=True).

See `result.json:metrics` for numeric details.

---

## 7. Derived Measurements (metrics, controls)

### Metrics (stable IDs)

| Metric ID | Value | Notes |
|---|---|---|
| **M6_PER_DEFINITION_ORDERING** | DEF-FULL-MAP trunc `cart>product_listing>detail` full `cart>detail>product_listing`; DEF-FORM-ONLY trunc `product_listing>cart>detail` full `product_listing>detail>cart`; ISOLATED trunc `cart>detail>product_listing` full `cart>detail>product_listing` | per spec |
| **M1_C1_ORDERING_CHANGED** | DEF-FULL-MAP true, DEF-FORM-ONLY true, ISOLATED false | at least one true for DEF-FULL-MAP/DEF-FORM-ONLY → C1=true |
| **M3_OBSERVED_PAIRWISE_AGREEMENT** | trunc_proxy 0.0, full_proxy 0.333, parent 0.3 (5-def), parent null 0.5275 | proxy not true full DOM |
| **M4_NULL_MEAN_PAIRWISE_AGREEMENT** | DEF-FULL-MAP 0.400, DEF-FORM-ONLY 0.404, ISOLATED 0.421 | proxy, 1000 iter seed 42 |
| **M2_C2_NULL_EXCEEDS_OBSERVED** | DEF-FULL-MAP true (0.400 ≥ 0.333), DEF-FORM-ONLY true (0.404 ≥ 0.333), ISOLATED null (C1 false) | proxy C2 true |
| **M5_DENSITY_DIFF_TRUNCATED_VS_FULL** | DEF-FULL-MAP mean 0.292, DEF-FORM-ONLY 0.0049, ISOLATED 0.269 | proxy, inflated |
| **SUBSTRATE_VERIFICATION** | cap_present true, canonical_exists false, tasks 8→7 unique | blocking |
| **B1_TRUNCATED_REGRESSION** | all 4 ordering checks true | PASS |
| **B2_COMMITTED_SCRIPT_BASELINE** | all-role trunc `cart>detail>product_listing` full `product_listing>detail>cart` | documents difference |
| **B3_STORED_RESULTS_COMPARISON** | identical_to_fullmap true, computed vs stored counts 2 vs 8 | PARTIAL (bug) |

### Controls

| Control ID | Expected | Observed | Pass | Evidence |
|---|---|---|---|---|
| **B1_TRUCATED_REGRESSION** | ordering reproduction | DEF-FULL-MAP + DEF-FORM-ONLY match true | true | full_dom_proxy_analysis.json |
| **B2_COMMITTED_SCRIPT_BASELINE** | all-role inflates | all-role ordering change true, opposite direction | true | same |
| **B3_STORED_RESULTS_COMPARISON** | stored ordering + bug | stored DEF-FULL-MAP match, ISOLATED identical true, computed vs stored mismatch for ISOLATED | PARTIAL | analysis_results.json |
| **C_POSITIVE_SCRIPT_REGRESSION** | C1 true, null 0.5275>0.3 | C1 true for both, proxy null 0.400 | true | derived |
| **C_NULL_MODEL_RANDOM_ROLE_MAP** | null ≥ observed → FALSIFIED stands | proxy null 0.400–0.421 ≥ observed 0.333 → true per def | UNKNOWN (proxy) | derived |

All metrics/controls preserve frozen identifiers; recomputed values available in `full_dom_proxy_analysis.json`.

---

## 8. Interpretation (decision rule)

Frozen rule:

```
if NOT measurement_validity_pass: MEASUREMENT_INVALID
elif C1 AND C2: SURVIVES_CURRENT_TEST
elif C1 AND NOT C2: MIXED
elif NOT C1 AND NOT C2: FALSIFIED
elif NOT C1 AND C2: INCONCLUSIVE
```

Measurement validity **fails** on two independent blocking dependencies:

1. Substrate: `locatableSample` cap not removed (evidence: MEASURE_JS line 89, all samples 20 vs locatable 82/32/21).
2. Code: canonical 3-def script not committed (no file at HEAD; audit V2 remains open).

Therefore **VERDICT = MEASUREMENT_INVALID** per spec. This overrides proxy C1/C2 values.

For directional context only (not citable as evidence for full DOM):

- Proxy C1 = true (ordering changes for DEF-FULL-MAP and DEF-FORM-ONLY, matching stored results and parent reconstruction). This reproduces the directional finding that first-20 truncation introduces page-type-dependent bias, robust across estimators.
- Proxy C2 = true (null_mean 0.400–0.404 ≥ observed 0.333) would, if valid, map to SURVIVES_CURRENT_TEST (truncation drove FALSIFIED). However this is **estimator-inflated and not a valid full-DOM test**; it cannot be used to claim C-MEAS-VALID survives.

**Infrastructure failure is not a scientific negative.** The FALSIFIED verdict from EXP-INTEL-35112013458 is neither confirmed nor overturned by this experiment; it remains the last valid measurement on truncated data.

---

## 9. Product Consequence

- **If SURVIVES (had measurement been valid):** FALSIFIED verdict confirmed as truncation artifact; density metric valid under full enumeration; product may adopt DEF-FULL-MAP as canonical yield metric bounded to single Magento site; C-MEAS-VALID advances toward PRODUCT_CORE.

- **Actual (MEASUREMENT_INVALID):** No change to claim status. **C-MEAS-VALID remains BLOCKED** for density family pending substrate and code fixes. Product lane must NOT adopt density-based ordering metric on truncated sample (FALSIFIED remains) and must not adopt proxy full-DOM estimate (inflated). The required_fix path is unchanged from handoff: route to runtime lane for cap removal and commit canonical script before re-testing.

Economics: pure offline re-analysis (numpy 1000 iter), no browser/network/model calls. Amortized cost low; no new data collection.

---

## 10. Validity Notes

1. Substrate representation loss: true full DOM unavailable; proxy overcounts 4–7x, full densities 0.29 vs locatable-scaled ~0.02–0.06; ordering direction robust but point estimates invalid.
2. Code provenance gap: proxy reconstruction not audited canonical artifact; until committed, measurement non-reproducible from HEAD.
3. Estimator loss as above.
4. ISOLATED-A-LINK bug preserved in analysis; corrected value fails C1 (ordering unchanged) but decision rule primary scopes DEF-FULL-MAP/DEF-FORM-ONLY.
5. Small N single-site bound (n=3,3,1 distinct cart), no CI, no cross-site generalization.
6. Null model coarse with 3 definitions; 1000 iter seed 42 conservative but not calibrated to real definition subspace.
7. No browser execution; frozen evidence only.
8. Frozen inputs verified immutable.

---

## 11. Unresolved

- Whether true full DOM enumeration (after cap removal) changes ordering beyond tag-count estimator.
- Whether canonical script should be committed at `research/intel/canonical_35137036013.py` or committed `analyze.py` accepted as canonical.
- Whether corrected ISOLATED-A-LINK alters C3 conclusions (pooled vs per-def).
- Whether product_listing vs detail swap is significant (needs bootstrap on full counts, n=3 per type).
- Whether menuitem/tab additive when present (0 counts here).
- Whether null-model pairwise agreement exceeds chance on true full-DOM data (requires full enumeration).

---

## 12. Evidence Refs

- `research/experiments/EXP-INTEL-35137036013/result.json` (this packet, sha pending)
- `research/experiments/EXP-INTEL-35137036013/provenance.json`
- `research/experiments/EXP-INTEL-35137036013/full_dom_proxy_analysis.json` sha256 5b3c03b4...
- `research/experiments/EXP-INTEL-35137036013/substrate_verification.json` sha256 bce78e0c...
- `research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json` sha256 da30bd05...
- `research/experiments/EXP-INTEL-35124660457/analysis_results.json` sha256 b2aaafde...
- `research/experiments/EXP-INTEL-35124660457/analyze.py` sha256 c2a085bb...
- `research/experiments/EXP-INTEL-35131994346/reconstruct.py` sha256 b4356768...
- `research/experiments/EXP-INTEL-34718481334/measure_fullpage_yield.py` sha256 085b58c9... (cap evidence line 89)
- Parent handoff: `research/experiments/EXP-INTEL-35131994346/handoff.json` sha256 fde5ee21...

All artifacts preserve stable IDs frozen in spec/prereg (M1–M6, B1–B3, C_POSITIVE, C_NULL).

---

## 13. Reproduction

```bash
python3 /tmp/opencode/exp35137036013_execute.py
# reads raw evidence, writes full_dom_proxy_analysis.json, substrate_verification.json, result.json, provenance.json
```

Environment: linux, python 3.12.14, numpy 2.5.3, working dir /home/runner/work/Spider/Spider.
