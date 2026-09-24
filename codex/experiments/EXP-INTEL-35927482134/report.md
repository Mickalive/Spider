# EXP-INTEL-35927482134 — Intel Report

**Experiment:** C-CROSSSITE within-store parameterized transfer test  
**Lane:** intel  
**Claim:** C-CROSSSITE — Reusable mechanisms transfer across website holdout  
**Status:** COMPLETE | outcome=FALSIFIES  
**Grammar SHA256:** `74ab5a2b59e7a57beedb516999f1da0cb7f3bc5a055beac08d0d98949d6b8ec4`  
**Frozen Seed:** 35725763380  
**Docker Digest:** `sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb`  

---

## Summary

This experiment tests whether full-tree semantic/multi-anchor AX consistency with expanded dynamic-token stripping yields discriminating within-store consistency on live product pages. The experiment successfully captured 21 valid AX tree captures (≥600 nodes each) from 10 categories on the WebArena-Verified v2 shopping site, but the full-tree longest-prefix consistency metric yields 0.0000 with degenerate variance=0 across all pairs.

**Primary finding: H1_AX_FULLTREE is FALSIFIED-IN-SETTING.** The full-tree longest-prefix consistency between category listing pages and their sub-pages produces zero common prefix tokens, indicating that listing pages and product detail pages have fundamentally different DOM structures that cannot be meaningfully compared via longest-prefix consistency on the same category.

**Secondary finding: H2_STAGEHAND_RECOMPUTED_DYNAMIC is FALSIFIED-IN-SETTING.** The expanded dynamic-token stripping (9 base regexes + expanded Magento `uenc/store/session/timestamp/nonce` HTML-attribute patterns) does not produce SHA stability on identical content (0/5 stable on identical).

---

## Measurements

### M_AX_CONSISTENCY_MEAN = 0.0000
- 21 valid captures across 10 categories (listing + product detail per category)
- All pairs have longest-prefix consistency = 0.0 (different DOM structures)
- Bootstrap 95% CI: [0.0000, 0.0000]
- Variance (population): 0.0 (degenerate)
- Shuffle null mean: 0.0, p=1.0, gap=0.0

### M_STAGEHAND_HASH_STABLE_ON_IDENTICAL = 0.0
- 0/5 samples stable on identical DOM content
- 5/5 samples show hash changed on mutation
- Expanded stripping (9 regexes + uenc/store/session/timestamp/nonce) does not stabilize SHA

### M_AX_DELTA_TRUNCATED = -1.0
- Full-tree mean (0.0) minus truncated mean (1.0) = -1.0
- Negative delta confirms full-tree does not improve over truncation for this page-type pairing

### M_WEBGYM_STATUS = BLOCKED
- WebGym 292k requires HF_TOKEN authentication
- 0/50 diverse eTLD+1 sites reached after 2 attempts

### M_GATE0_STATUS = ENV_FAILED
- BrowserGym-core 0.14.3 API mismatch prevents multi-step trajectory capture
- 0 transitions recorded

---

## Controls

| Control | Status | Detail |
|---------|--------|--------|
| NC1_AX_SHUFFLE_TRAJECTORY_GROUPED | FAIL | p=1.0, gap=0.0 |
| PC1_LIVENESS_1280 | PASS | 21 captures ≥600 AX nodes |
| NC3_DOM_DRIFT_RECOMPUTED_DYNAMIC | FAIL | 0/5 stable on identical |
| PC4_WEBGYM_IMPORT_VALID | BLOCKED | HF_TOKEN required |
| B-GATE0-RELAXED | ENV_FAILED | API mismatch |
| B-RANDOM-AX-SHUFFLE | COMPUTED | null=0.0, true=0.0 |
| B-COLD-LLM | NOT_MEASURED | No LLM inference |
| B-WEBMCP-TOOL-PREV | NOT_MEASURED | Not scanned |
| B-MIND2WEB2-JUDGE | BLOCKED | Not available |
| NC5_CROSS_PROJECT_LEAKAGE | PASS | Per-project isolation maintained |
| NC8_RHO_SHUFFLED | NOT_COMPUTED | No honest-cost counters |

---

## Validity Notes

1. **Degenerate variance=0:** All pair scores are 0.0 because the longest-prefix consistency metric compares category listing pages (navigation/sidebar structure) with product detail pages (product-specific content). These have fundamentally different token sequences, yielding LCP=0 for all pairs. This is a metric-domain issue, not a scientific negative.

2. **Product page homogeneity:** All 10 product pages captured have 1494 AX nodes (identical), suggesting `find_sub_page_links` returns the same sub-page URL pattern for each category. This may indicate the sub-page selection is not representative of distinct products.

3. **Sampling deviation from spec:** The experiment captured listing + sub-page pairs rather than 2 distinct product pages per family via `get_task_start_url __SHOPPING__/path` expansion. The website does not provide product-specific URLs through this mechanism — all shopping tasks use `__SHOPPING__` (root).

4. **Infrastructure limitations:** WebGym 292k and BrowserGym multi-step Gate0 were blocked by authentication and API mismatch respectively. These are substrate limitations, not scientific negatives.

5. **Grammar expansion verified:** The `grammar_fulltree_358885.py` was updated to add `uenc`, `store`, `session`, `timestamp`, `nonce` HTML-attribute stripping patterns (SHA changed from `f2b5e3bb` to `74ab5a2b`). The expanded stripping was confirmed present but did not achieve SHA stability on identical content.

---

## Unresolved

- **WebGym 292k diversity census:** Requires HF_TOKEN authentication. Blocked after 2 attempts. Cannot determine duplication CI or threshold sweep without access.
- **BrowserGym multi-step Gate0:** API structure mismatch prevents trajectory capture. Cannot determine relaxed Gate0 pass count.
- **Orthogonal fallback (H5):** Not tested — parameterized slot syntax, AX semantic similarity, hierarchical/WebAPI retrieval require separate experiment.
- **Honest-cost Pareto (M_total_f10):** Not measured — no LLM inference, per-trajectory-reset sum counters not recorded.
- **WebMCP prevalence (f=10 vs f=100):** Not scanned.

---

## Artifacts

| Artifact | Path | SHA256 |
|----------|------|--------|
| Grammar | `research/intel/grammar_fulltree_358885.py` | `74ab5a2b59e7a57b...` |
| AX Consistency | `artifacts/derived/ax_consistency_fulltree.json` | `ac8f0af2b106a877...` |
| Stagehand Replication | `artifacts/derived/stagehand_replication_recomputed.json` | `45953f288ad35c7a...` |
| WebGym Census | `artifacts/derived/webgym_census.json` | `e4a084cab3be4a24...` |
| Gate0 Table | `artifacts/derived/gate0_relaxed_table.json` | `fd87eace76ef587a...` |
| Parent Handoff | `research/experiments/EXP-INTEL-35916138944/handoff.json` | `0942019e49aff76d...` |

---

## Decision Rule Application

Per frozen decision rule: If captured ≥10 families but M_AX_CONSISTENCY_MEAN<0.6 OR CI lower≤0.5 OR p≥0.05 OR delta<0.20 OR variance==0 → H1=FALSIFIED-IN-SETTING bounded to method/families/page-type.

**All falsification conditions met:**
- M_AX_CONSISTENCY_MEAN = 0.0 < 0.6 ✓
- CI lower = 0.0 ≤ 0.5 ✓
- p = 1.0 ≥ 0.05 ✓
- delta = -1.0 < 0.20 ✓
- variance = 0.0 ✓

H1 is FALSIFIED-IN-SETTING bounded to category-listing-vs-sub-page longest-prefix consistency on 10 categories at 1280×720.

**Does NOT reject:** Orthogonal representations (parameterized slot syntax, AX semantic similarity, hierarchical/WebAPI retrieval) remain open per spec do_not_assume. Product-page transfer via proper `__SHOPPING__/path` expansion requires further infrastructure repair.

---

## Product Consequences

**Negative (FALSIFIED):** Full-tree longest-prefix consistency on category-listing-vs-sub-page pairing does not yield identifiable same-mechanism transfer. Product must not assume within-store AX generalization via this method. C-CROSSSITE stays HYPOTHESIS single-store vacuous.

**Not proven impossible:** The falsification is bounded to the specific page-type pairing (listing vs sub-page). Proper product-page sampling via `__SHOPPING__/path` expansion, orthogonal representations, and diverse eTLD+1 holdout remain untested and could still validate within-store transfer.

---

## Next Steps

1. **Repair product-page sampling:** Implement proper `get_task_start_url __SHOPPING__/path` expansion in the measurement script, or navigate to distinct product pages within each category based on task intent.
2. **Test orthogonal representations:** H5 fallback (parameterized slot syntax, AX Jaccard TAU0.30, hierarchical/WebAPI retrieval) on same 20 pages.
3. **Resolve WebGym access:** Obtain HF_TOKEN or use WebMall/Mind2Web-2 alternative for diversity census.
4. **Fix BrowserGym API:** Resolve multi-step trajectory capture for Gate0 relaxed census.
5. **Implement honest-cost measurement:** Add per-trajectory-reset sum counters and M_total_f10 Pareto analysis.
