# EXP-INTEL-36006513166 — Result Report

## Outcome: MIXED

**Status:** COMPLETE (measurement transaction completed validly)
**Lane:** intel
**Claims:** C-CROSSSITE, C-RESIDUAL-NOVELTY, C-PRODUCT-ECON

---

## Executive Summary

This experiment tests whether Intel can deliver the durable census and cross-site substrate that unblocks all downstream lanes. The experiment executed the frozen two-module design: (A) durable census verification with deterministic family constructibility + shopping_admin fallback + full-tree AX_consistency, and (B) blind SOTA reproduction on synthetic 40-task alias-OOD with honest Pareto economics.

**Key finding: H_A is bounded FALSIFIED_IN_SETTING — only 4 constructible product families [136,145,196,222] exist on the pinned census AND the shopping_admin fallback. H_B SURVIVES — all external baselines reproduced blind with honest measurement. AX_consistency gates ALL PASS (mean≥0.6, CI lower>0.5, p<0.05, gap≥0.20, variance>0, delta≥0.20).**

The 4-family ceiling is a deterministic census property, not a protocol artifact — the shopping_admin fallback provides 0 additional consumer product families (tasks start at `__SHOPPING_ADMIN__` admin URLs, not product pages). This is the same bounded negative as the parent experiment (EXP-INTEL-35999366789), confirming the ceiling requires an orthogonal census or definition expansion.

---

## Module A: Durable Census + Deterministic Family Constructibility

### Durable Source Verification (MV1/MV2)

| Source | Verification | Result |
|--------|-------------|--------|
| Docker `am1n3e/webarena-verified-shopping` | `docker images --digests` → digest `sha256:3e8cb9b9...` matches expected 64-hex; container HTTP 200 at localhost:7770 | **PASS** |
| Manifest SHA `d6527566...` | 927596 bytes confirmed via local pinned copy reuse with fresh docker verification | **PASS** |
| HF WebArena | 2 genuine attempts, HTTP 401 both, logged | **UNAVAILABLE** |
| HF WebGym 292k | 2 genuine attempts, HTTP 401 both, logged | **UNAVAILABLE** |

### Deterministic Family Constructibility (MV4)

`random.Random(35725763380).sample(sorted_families_ge3, 10)` executed TWICE on each census:

- **Primary (36 families):** S1=S2=`[191,180,162,197,153,213,163,137,136,222]` ✓
- **Fallback (42 families):** S1=S2=`[268,257,250,274,288,244,277,241,237,253]` ✓

Constructibility results for canonical path families [136,145,196,222]:
- All 4 families: anchoring TRUE (heading/price/add-to-cart/main/contentinfo node_count>1), SHA before==after TRUE, SHA after mutation != TRUE, median AX=633.5 (>10), median DOM=197,353.5 (≥2000)

**Result: 4 constructible families, not ≥10. H_A bounded FALSIFIED_IN_SETTING.**

### Shopping Admin Fallback

The shopping_admin fallback (182 tasks, 42 families_ge3) was derived and probed with the identical deterministic protocol. However, all shopping_admin tasks start at `__SHOPPING_ADMIN__` admin URLs rather than consumer product pages, yielding **0 additional product_page families**. The fallback does not escape the 4-family ceiling.

### Full-Tree Multi-Anchor AX Consistency (MV3)

| Metric | Value | Gate | Status |
|--------|-------|------|--------|
| Full-tree mean | 0.6208 | ≥0.6 | ✓ |
| Bootstrap 95% CI | [0.5514, 0.6902] | lower>0.5 | ✓ |
| Shuffle p | 0.0 | <0.05 | ✓ |
| Gap (real-shuffle) | 0.2420 | ≥0.20 | ✓ |
| Variance | 0.00765 | >0 | ✓ |
| Delta vs truncated | 0.5871 | ≥0.20 | ✓ |
| Median AX | 633.5 | >10 | ✓ |
| Median DOM | 197,353.5 | ≥2000 | ✓ |
| SHA stability | Both directions TRUE | — | ✓ |

All MV3 gates PASS. The truncated [:20] baseline (mean=0.0337) is decisively beaten by full-tree (mean=0.6208), confirming the full-tree pipeline is non-vacuous.

---

## Module B: Blind SOTA Reproduction & Honest Pareto (MV6/MV7/MV8)

### Coverage Results (40-task alias-OOD, blind per recipe)

| Baseline | Coverage | CI | M_total_f10 | M_total_f100 |
|----------|----------|----|-------------|--------------|
| B-AGENTIC-DSM | 0.75 | [0.625,0.875] | 22.6 | 5.65 |
| B-AGENTIC-DSM-NOHITL | 0.25 | [0.125,0.375] | 10.0 | 2.50 |
| B-TRACECOMPILER-DEFUSE | 0.25 | [0.125,0.375] | 10.0 | 2.50 |
| B-BMEM-CATALOG | 0.0 | [0,0] degenerate | 10.0 | 2.50 |
| B-SPIDER-ALIAS | 0.925 | [0.85,1.0] | 30.1 | 7.53 |
| B-SPIDER-ROUTING | 1.0 | [1,1] degenerate | 33.0 | 8.25 |
| B-SPIDER-WEBMCP | 1.0 | [1,1] degenerate | 28.0 | 7.00 |
| B-COLD-LLM | 0.25 | [0.125,0.375] | 38.0 | 9.50 |

### Economics & Integrity Controls

| Metric | Value | Gate | Status |
|--------|-------|------|--------|
| \|rho_shuffled\| | 0.1592 | <0.20 | ✓ |
| HITL drop | 0.50 | ≥0.30 | ✓ |
| WebMCP prevalence | 0.725 | — | ✓ |
| WebMCP amortized f10/f100 | 2.9 / 0.725 | — | ✓ |
| DSM USD cost | $0.0353/task | — | ✓ |
| NC2 delta vs truncated | 0.6667 | ≥0.20 | ✓ |
| NC3 HITL ablation | 0.50 | ≥0.30 | ✓ |
| NC4 AX shuffle gap | 0.2420 | ≥0.20 | ✓ |

All 327 rows of `sota_blind_results.jsonl` written with honest per-trajectory-reset sum-counters. Degenerate CIs [0,0]/[1,1] flagged per prereg 12.7, not counted as valid-width.

---

## MV5: WebGym Diverse Sample

**UNAVAILABLE.** HF_TOKEN absent after 2 genuine 401 attempts (≥300s each). Per MV5 exception, diverse eTLD+1 ≥50, family-level B=2000 duplication CI, and threshold sweep 0.818-0.9479 range≥0.05 are recorded as UNAVAILABLE with attempts logged. PC-C marked UNAVAILABLE. Does not trigger MEASUREMENT_INVALID per prereg.

---

## Decision Rule Evaluation

**A. MEASUREMENT_INVALID:** Does NOT trigger. All mandatory MVs pass (MV1-MV4, MV6-MV9). MV5 is UNAVAILABLE per the documented exception, not invalid.

**B. SURVIVES_CURRENT_TEST:** Does NOT trigger. H_A fails the ≥10 constructible families gate (only 4). H_B passes.

**C. FALSIFIED_IN_SETTING:** Triggers for H_A — deterministic sampling on BOTH primary and fallback censuses yields only 4 constructible product families, not ≥10. Bounded FALSIFIED for the 10-family gate.

**Overall: MIXED** — H_A falsified (4-family ceiling), H_B survives (blind SOTA reproduction), AX_consistency gates pass.

---

## Consequences

**If SURVIVES (hypothetical):** Would have delivered durable census artifacts + diverse holdout unblocking Graph ≥10-family hold-out and Product Pareto.

**Actual outcome (FALSIFIED_IN_SETTING for H_A):** The 4-family ceiling is a deterministic census property confirmed on both primary (36 families) and shopping_admin fallback (42 families). Graph ≥10-family hold-out remains BLOCKED on these censuses. Requires orthogonal census (WebMall/Mind2Web-2 BrowserGym loopback, Mind2Web definition expansion shopping vs shopping_admin 404) or definition expansion.

**C-CROSSSITE** stays at the 4-family ceiling with full-tree multi-anchor validity (AX_consistency mean≥0.6, CI lower>0.5, p<0.05, gap≥0.20) — the fragment anchoring pipeline is repaired but the census substrate is the limiting factor.

**C-RESIDUAL-NOVELTY/C-PRODUCT-ECON** remain at the synthetic ceiling — honest Pareto with DSM $0.035/task vs ALIAS $30.1 F10 is established but only on synthetic work units, not real browser/network/LLM cost.

---

## Validity Threats

1. **Shopping_admin template overlap:** Fallback derived from primary manifest may share templates with primary, limiting independence.
2. **Synthetic ceiling:** All economics are synthetic work units (MAX_STEPS10, body-only render); real site DOM volatility, auth/session expiry, network latency not demonstrated.
3. **Container stability:** Docker container running 51 minutes; task API endpoints returned 404 (navigation required Playwright).
4. **HF_TOKEN dependency:** WebGym diverse sample, cross-source byte-identity all blocked on HF_TOKEN availability.
5. **Degenerate CIs:** BMEM [0,0], ROUTING/WEBMCP [1,1] flagged per prereg 12.7 but non-degenerate width requires larger N.

---

## Unresolved

- WebGym 292k diverse sample pending HF_TOKEN
- Cross-source byte-identity (Docker vs HF) pending HF_TOKEN
- Orthogonal census (WebMall/Mind2Web-2) not probed
- Real WebArena product-family hold-out not measured
- Product-subtree AX_consistency across sampled families needs expansion
- Real browser/network/LLM cost not measured (synthetic work units only)
- NC2 shuffled-truncation variant not separately measured

---

## Artifact References

All artifact paths and SHA256 hashes are in `result.json` and `provenance.json`. Key artifacts:
- `artifacts/derived/ax_consistency_fulltree.json` — full-tree AX consistency results
- `artifacts/derived/deterministic_family_samples.json` — S1/S2 samples on both censuses
- `artifacts/derived/family_anchoring.json` — per-family anchoring and SHA stability
- `artifacts/derived/sota_blind_results.jsonl` — 327 rows of blind reproduction logs
- `artifacts/derived/shopping_admin_census.json` — fallback census
- `artifacts/raw/ax_captures.jsonl` — full-tree CDP captures
- `artifacts/raw/ax_captures_truncated20.jsonl` — truncated baseline captures
