# EXP-INTEL-35860344410 Report — Intel PIVOT to C-CROSSSITE (EXECUTE)

**Lane:** intel  
**Claim:** C-CROSSSITE (HYPOTHESIS)  
**Outcome:** MIXED — substrate live, but product page scarcity + degenerate metrics  
**Status:** COMPLETE  
**Date:** 2026-09-23  

---

## Executive Summary

This experiment executed the Director-mandated PIVOT from the 8-repair mega-question to three minimal unblocking measurements. The substrate is **confirmed LIVE** — Docker, Playwright, CDP AX tree capture, and mutation via page.evaluate all function correctly. However, all three hypotheses (H1/H2/H3/H4) are classified **MEASUREMENT_INVALID or FALSIFIED-IN-SETTING** due to substrate-level issues, not infrastructure failure.

**Key finding:** Full DOM SHA256 is fundamentally unsuitable as a Stagehand cache key on dynamic web pages because each page load generates a different hash even for identical URLs. This is a substrate-level discovery that blocks the entire Stagehand replication branch.

---

## 1. Substrate Liveness (PC1 — PASS)

Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` reached on 1st retry at `http://localhost:7770`. Playwright 1.63.0 functional. CDP `Accessibility.getFullAXTree` yielded 20/20 valid captures:
- Node counts: 668–1426 (all ≥600 threshold)
- DOM bytes: 196,958–251,734 (all ≥2000 threshold)
- Viewport: 1280×720
- Seed: 35725763380 (deterministic)

**PC1 PASSES.** The substrate is live and producing valid AX trees.

---

## 2. H1_AX_FULLTREE — FALSIFIED-IN-SETTING / MEASUREMENT_INVALID

### Method
Full-tree semantic/multi-anchor traversal (no `[:20]` truncation) via CDP `Accessibility.getFullAXTree`, anchored on heading/price/add-to-cart/main/contentinfo boundaries, with longest-prefix consistency per family.

### Results
- **20 captures** from **10 families** (all valid: 600–2000 nodes, ≥2000 bytes)
- **Only 4/20 captures (2/10 families)** navigate to task-specific product pages (families 136, 145)
- **16/20 captures (8/10 families)** navigate to identical "One Stop Market" homepage (1426 nodes, 251KB)

| Family | Consistency | Page Type |
|--------|------------|-----------|
| 101 | 1.0000 | Homepage |
| 136 | 0.0000 | Product |
| 137 | 1.0000 | Homepage |
| 138 | 1.0000 | Homepage |
| 139 | 1.0000 | Homepage |
| 145 | 0.0000 | Product |
| 147 | 1.0000 | Homepage |
| 153 | 1.0000 | Homepage |
| 154 | 1.0000 | Homepage |
| 155 | 1.0000 | Homepage |

### Metrics
- **Mean consistency:** 0.8000
- **Bootstrap 95% CI:** [0.5000, 1.0000] — lower bound NOT > 0.5 (equals exactly)
- **Trajectory-grouped shuffle p:** 1.0 (degenerate — shuffling binary 0/1 scores produces identical mean)
- **Per-family variance:** 0.16 (non-zero but driven by binary pattern)
- **Delta vs truncated [:20]:** 0.0 (full-tree identical to truncated for short homepage patterns)

### Decision Rule Evaluation
- Mean ≥ 0.6: ✓ (0.8)
- CI lower > 0.5: ✗ (equals 0.5, not strictly greater)
- Shuffle p < 0.05: ✗ (p = 1.0)
- Delta vs 0.2857 ≥ 0.20: ✗ (delta vs truncated = 0.0)
- Full-tree vs truncated delta ≥ 0.10: ✗ (delta = 0.0)
- PC1 ≥ 15/20: ✓ (20/20)
- Variance > 0: ✓ (0.16)
- **Product families < 5:** ✗ (only 2 of 10)

**H1 = MEASUREMENT_INVALID** (product page scarcity: 2/10 < 5 required).  
**H1 also shows FALSIFIED characteristics** for general AX consistency (p=1.0, delta=0.0, CI lower=0.5).

### Root Cause
The `[:20]` truncation bug does not affect homepage pages because their patterns are already shorter than 20 tokens. Full-tree traversal provides no improvement over truncation for short patterns. The binary 0/1 scoring (1.0 for identical homepage, 0.0 for different products) creates a degenerate shuffle distribution.

---

## 3. H2_STAGEHAND_RECOMPUTED — MEASUREMENT_INVALID

### Critical Finding: Full DOM SHA256 Instability

**Each page load generates a different DOM SHA256 even for identical URLs.** For example, family 101's two captures of the same "One Stop Market" homepage produce different hashes:
- Capture 1: `9fb422deea4d9b26...`
- Capture 2: `a5a64375c87645e0...`

This means **SHA256 of full DOM cannot serve as a cache key** because dynamic content (CSRF tokens, session IDs, timestamps) changes between page loads. Stagehand's `HIT after N=2 identical results` can never be achieved on dynamic pages unless the cache key uses normalized/static content.

### Stagehand Replication Results
- **HIT rate:** 0.0/10 (all families have different DOM hashes on each load)
- **MISS rate:** 1.0/10
- **Mutation capability:** ✓ (page.evaluate changes hash)
- **Hash changed on mutation:** ✓ (before_hash ≠ after_hash)
- **Selector derivation:** ✓ (1426 AX nodes, role+name+CSS path)
- **No synthetic fallback used**
- **Per-project isolation:** ✓ (key includes project_id)

### What Could NOT Be Measured
- Stagehand server HIT/MISS/false_accept rates (requires actual Stagehand server)
- Cold vs cached latency/tokens (requires Stagehand server)
- Speedup ~2x/~30% (requires Stagehand server)
- 30+ families drift test (requires Stagehand server)

**H2 = MEASUREMENT_INVALID** (cannot test Stagehand HIT without server; full DOM SHA256 unsuitable for caching on dynamic pages).

---

## 4. H3_WEBGYM_DIVERSE — MEASUREMENT_INVALID

### Results
- WebGym v1.0.6 installed
- 50 non-standard hosts found via WebArena task overlap
- **Cannot confirm** 50 distinct eTLD+1 sites as WebGym corpus
- **Cannot compute** duplication 95%CI or threshold sweep 0.818-0.9479
- **Cannot confirm** site diversity entropy

**H3 = MEASUREMENT_INVALID** (WebGym census incomplete; requires WebGym-specific corpus enumeration beyond WebArena overlap).

---

## 5. H4_GATE0_RELAXED — MEASUREMENT_INVALID

### Results
- **9 transitions** collected (vs ≥50 required per family)
- **All** `action.target_href == state_after.url` (leakage_validOnly = 1.0)
- **9 unique titles** (all URL-level)
- **Relaxed Gate0** H>0.1 NL≥20 NOT achieved
- **Strict Gate0** not attempted (insufficient transitions)

The shopping site is link-dominated; navigations return to the same page or same-origin listings. Structural `action.target_href == state_after.url` leakage removes most transitions by design.

**H4 = MEASUREMENT_INVALID** (insufficient transition density; 9 < 50 per family).

---

## 6. Baselines Summary

| Baseline | Expected | Observed | Status |
|----------|----------|----------|--------|
| B-STAGEHAND-VERB | HIT≥0.8, MISS≥0.8, FA<0.05, ~2x/~30% | HIT=0.0, DOM hash unstable | MEASUREMENT_INVALID |
| B-RANDOM-AX-SHUFFLE | True > shuffle+0.20, p<0.05 | Shuffle mean=0.8, p=1.0 | FAIL |
| B-TRUNCATED-20 | Full-tree > truncated by ≥0.10 | Delta=0.0 | FAIL |
| B-WEBGYM-HARDCODED-09479 | WebGym CI distinct from 0.9479 | Census incomplete | MEASUREMENT_INVALID |
| B-COLD-LLM | Cold latency/tokens upper bound | Not measured | NOT_MEASURED |
| B-CONSTANT-NULL-05654 | REJECTED vacuous | Disclosed only | N/A |

---

## 7. What Worked vs What Failed

### Working (infrastructure level)
- ✅ Docker substrate reachable, stable
- ✅ Playwright 1.63.0 + CDP AX tree capture functional
- ✅ Full-tree semantic/multi-anchor grammar implemented (no `[:20]` truncation)
- ✅ page.evaluate mutation + SHA256 recomputation after mutation verified
- ✅ Selector derivation from AX tree (role+name+CSS path)
- ✅ Frozen seed 35725763380 deterministic throughout
- ✅ Per-project isolation structurally enforced
- ✅ Cross-project leakage prevention verified

### Failed (scientific level)
- ❌ Product page scarcity (2/10 < 5 required)
- ❌ Shuffle degeneracy (p=1.0 due to binary 0/1 scores)
- ❌ Full-tree vs truncated delta=0.0 (short homepage patterns)
- ❌ Full DOM SHA256 unstable between page loads (dynamic content)
- ❌ Stagehand HIT rate=0.0 (cannot achieve identical hash on re-access)
- ❌ WebGym diverse census incomplete
- ❌ Gate0 transitions insufficient (9 < 50)

---

## 8. Implications for Product

### Positive findings (if any)
- Substrate is LIVE and producing valid AX trees at 1280×720
- Full-tree traversal without truncation is correctly implemented
- page.evaluate mutation + SHA256 recomputation after mutation works
- Selector derivation from AX+DOM is feasible
- Cross-project isolation is structurally sound

### Negative findings (block product decisions)
- **Full DOM SHA256 cannot serve as cache key** on dynamic pages — this blocks the entire Stagehand competitive floor claim
- **Product page scarcity persists** — the shopping_admin 184-task/42-family expansion is still needed
- **AX_consistency metric is degenerate** on shopping sites — binary 0/1 scoring prevents meaningful statistical testing
- **Gate0 multi-step trajectories** are unreachable via simple navigation on shopping sites
- **WebGym diverse census** requires WebGym-specific tooling, not WebArena overlap

### Required next steps
1. **Normalize DOM content** for Stagehand cache key (extract static product attributes, exclude dynamic tokens)
2. **Expand to shopping_admin 184-task/42-family** corpus to achieve ≥5 product-page families
3. **Implement BrowserGym loopback** or hierarchical/WebAPI retrieval for Gate0
4. **Use WebGym-specific corpus** for diverse eTLD+1 census
5. **Consider AX-level consistency** (semantic similarity) instead of token-level LCP

---

## 9. Artifacts

All artifacts preserved with SHA256 hashes:

| Artifact | Path | Role |
|----------|------|------|
| AX Captures | `artifacts/raw/ax_captures.json` | raw |
| AX Consistency | `artifacts/derived/ax_consistency_fulltree.json` | derived |
| Stagehand Replication | `artifacts/derived/stagehand_replication_recomputed.json` | derived |
| WebGym Census | `artifacts/derived/webgym_census.json` | derived |
| Gate0 Table | `artifacts/derived/gate0_relaxed_table.json` | derived |
| Provenance | `artifacts/derived/provenance.json` | derived |

---

## 10. Cost

No LLM inference used. Wall-clock: ~8 minutes (Docker already running). All measurements are browser-based CDP AX extraction + Playwright navigation. Total artifacts: <15MB.

---

## 11. Pre-registration Compliance

All frozen design elements followed:
- ✅ Frozen seed 35725763380 used deterministically
- ✅ Full-tree semantic/multi-anchor grammar implemented (no `[:20]` truncation)
- ✅ Placeholder expansion verified (`__SHOPPING__` → `http://localhost:7770/`)
- ✅ Pins: BrowserGym 0.14.3, AgentLab 0.4.2, Playwright 1.63.0
- ✅ Viewport 1280×720 CDP
- ✅ Docker digest `3e8cb9b945` recorded
- ✅ 2000 bootstrap, 1000 shuffle, 1000 Stagehand random nulls
- ✅ 2000 family-level bootstrap for CIs
- ✅ All artifact paths SHA256 hashed
- ❌ Shopping_admin 42-family expansion not implemented (product page scarcity)
- ❌ Stagehand server not deployed (HIT/MISS not measurable)
- ❌ WebGym corpus not fully enumerated (diverse census incomplete)
- ❌ Multi-step trajectories not achieved (9 < 50)
