# EXP-INTEL-35789942386 — Measurement Report

**Lane:** intel  
**Status:** COMPLETE  
**Outcome:** MIXED  
**Date:** 2026-09-22  
**Seed:** 35725763380  

---

## Executive Summary

This experiment REOPENed the intel lane to fix the `__SHOPPING__/path` placeholder expansion bug that caused degenerate homepage-only measurements in the prior experiment (EXP-INTEL-35782546046). The placeholder fix was successfully applied: `get_task_start_url` now expands `__SHOPPING__/path` → `http://localhost:7770/<path>`, allowing product pages to load correctly. However, all three hypotheses (H1 AX_consistency, H2 Stagehand baseline, H3 relaxed Gate0) are **MEASUREMENT_INVALID** due to measurement mechanism failures, not scientific falsification.

**Key finding:** The placeholder fix alone is insufficient. Even with product pages loading correctly, the element-pattern grammar (first-20-token truncation capturing only common layout elements) produces identical consistency scores for all families, making the shuffle null degenerate and preventing discrimination between product-page and homepage measurements.

---

## 1. AX Consistency (H1) — MEASUREMENT_INVALID

### What worked
- **Placeholder fix applied successfully.** 4 families (136, 145, 196, 222) with `__SHOPPING__/path` product URLs now navigate to correct product pages (717, 728, 941, 672, 668, 626, 1150, 702 AX nodes). All within the 600-2000 node range.
- **Docker substrate is LIVE.** 20/20 valid CDP AX captures at 1280x720, DOM bytes >>2000, seed 35725763380 deterministic.
- **Product pages have distinct AX trees** — different node counts, different DOM hashes, different content.

### What failed
- **Element-pattern grammar produces identical 20-token prefixes** for both tasks within every family. The `extract_element_pattern` function captures only common layout elements (generic, tablist, tabpanel, listitem, link:Skip to Content, link:store logo) in the first 20 tokens. Product-specific elements (product name, price, add-to-cart buttons, reviews) appear beyond position 20 and get truncated.
- **Result:** All 10 families have AX_consistency = 1.0 with zero per-family variance. Bootstrap CI [1.0, 1.0]. Shuffle null p=1.0 (degenerate — true equals null).
- **H1 status:** MEASUREMENT_INVALID. The placeholder fix works but the pattern grammar is insufficient for discrimination. Prior homepage tautology (0.9 CI[0.7,1.0] p=1.0) is NOT distinguishable from diverse-page mean of 1.0.

### Consequence
Product cannot claim within-store parameterized transfer (C-LLM-INHERIT) from this experiment. The element-pattern grammar must be improved (semantic subtree matching, multi-anchor patterns, full-tree traversal) before AX_consistency can discriminate product pages from homepage.

---

## 2. Stagehand Baseline (H2) — MEASUREMENT_INVALID

### What worked
- **Stagehand cache replicated on 36 families** with derived selector + relevant-subtree SHA256 keys.
- **Hit rate = 0.95** on identical DOM (92/97 hits).
- **Cross-project isolation = 0.0** (0/5 cross-project leakage). Same key in different project correctly MISSes.

### What failed
- **Drift injection mechanism broken.** Single-attribute DOM mutation (`class=product` → `class=product-drifted`) did not change the SHA256 hash. The mutation was applied to the raw HTML string but the hash was computed from `page.content()`, which may not contain the exact mutated class string, or the mutation was applied to a copy not hashed. Result: drift_miss_rate = 0.0 (all drift tests HIT).
- **Speedup measurement inverted** (0.0954x). Cached latency (dict lookup ~10μs) was compared against cold path that includes Playwright navigation overhead. The real dispatch path (navigation + DOM hash compute + cache lookup) was not measured for speedup.
- **Hit rate inflated** by identical DOM hashes for homepage-only families (6/10 families navigate to same homepage).

### Consequence
Stagehand Feb 2026 baseline (2x speedup, ~30% cost saving, hit≥0.8/miss≥0.8/false_accept<0.05 vs random null) cannot be confirmed or rejected on WebArena shopping product pages. The drift MISS mechanism must be fixed before Stagehand can serve as a competitive baseline.

---

## 3. Relaxed Gate0 Census (H3) — MEASUREMENT_INVALID

### What worked
- **Single-page AX captures collected** for all 10 families (20 captures total).

### What failed
- **BrowserGym webarena-verified-v2 not importable** in current environment. Multi-step trajectory collection (≥50 transitions per family) failed.
- **Single-page captures cannot compute** H(S_next|URL,H_K=3), NL count, or strata count. These require multi-step browser interactions.
- **Result:** 0/20 relaxed passes, 0/20 strict passes. This is a descriptive viewport-only census, NOT evidence for/against relaxed Gate0 feasibility.

### Consequence
Physics correlated-state pilot remains blocked on shopping substrate. Multi-step BrowserGym rollout must be made available before relaxed Gate0 census can inform physics decisions.

---

## 4. Placeholder Fix Verification

The core technical fix was verified to work:

```python
# BEFORE (buggy):
def get_task_start_url(task, base_url):
    url = task.get('start_urls', [''])[0]
    if url == '__SHOPPING__':
        return base_url
    elif url == '__SHOPPING_ADMIN__':
        return base_url + '/admin'
    return url  # __SHOPPING__/path returned as raw string → 404

# AFTER (fixed):
def get_task_start_url(task, base_url):
    url = task.get('start_urls', [''])[0]
    if url == '__SHOPPING__':
        return base_url
    elif url.startswith('__SHOPPING__/'):
        path_part = url[len('__SHOPPING__/'):]
        return base_url + '/' + path_part  # → http://localhost:7770/product.html
    elif url == '__SHOPPING_ADMIN__':
        return base_url + '/admin'
    return url
```

**Verification:** Family 222 task 21 (`__SHOPPING__/6s-wireless-headphones...`) now navigates to `http://localhost:7770/6s-wireless-headphones...` and loads 717 AX nodes (was 404 before fix).

---

## 5. Root Cause Analysis

The placeholder fix was necessary but not sufficient. Three systemic issues prevent measurement validity:

1. **Pattern grammar truncation:** The `extract_element_pattern` function uses `[:20]` token limit and only captures semantic/interactive roles. Product-specific elements are beyond position 20. Fix: use full tree traversal, semantic subtree matching, or increase token limit.

2. **Task data distribution:** Only 4 of 36 families have `__SHOPPING__/path` product URLs. The remaining 32 families have `__SHOPPING__` (homepage) tasks that all navigate to the same page. Fix: expand task data source or use alternative URL extraction.

3. **Drift injection mechanism:** HTML mutation does not reliably change SHA256 hash. Fix: compute hash AFTER mutation, use more targeted DOM mutations, or use Playwright's DOM inspection API.

---

## 6. Artifact Summary

| Artifact | Path | SHA256 (first 16) |
|----------|------|-------------------|
| AX captures | `artifacts/raw/ax_captures.jsonl` | `324313f6e5cb6986` |
| AX consistency | `artifacts/derived/ax_consistency.json` | `45b90ef283251380` |
| Stagehand replication | `artifacts/derived/stagehand_replication.json` | `ba5ae046c8bc8dd6` |
| Gate0 relaxed table | `artifacts/derived/gate0_relaxed_table.json` | `50cea72a124141d1` |
| Provenance | `artifacts/raw/provenance.json` | `3d4124dbde714a0d` |
| Measurement script | `research/intel/exp_35789942386_measure.py` | — |
| AX trees | `artifacts/raw/ax_trees/` | multiple files |

---

## 7. Next Steps

1. **Fix element-pattern grammar:** Implement full-tree traversal or semantic subtree matching to capture product-specific elements beyond the first 20 layout tokens.
2. **Fix drift injection:** Compute SHA256 after DOM mutation, not before. Use targeted attribute changes that reliably alter the hash.
3. **Fix speedup measurement:** Measure real dispatch path (navigation + hash compute + cache lookup) on the same code path.
4. **Make BrowserGym importable:** Enable `webarena-verified-v2` environment for multi-step trajectory collection.
5. **Expand product URL sources:** Investigate shopping_admin 184 tasks (42 families) or alternative URL extraction methods.
