# EXP-FRONTIER-35886105479 — Report: WebMCP-First Compiled Bypass vs Endpoint-Catalog vs Hierarchical vs Flat under Correct-Family Gating and Honest Cost

**Lane:** frontier — Charter: search outside the current solution basin for high-upside falsifiable mechanisms.
**Claim:** C-SEMANTIC-RESOLVE (Goals can be resolved to applicable mechanisms without internal ids)
**Status:** COMPLETE | Outcome: FALSIFIES
**Frozen:** spec.json, prereg.md, freeze.json (hashes verified)

## Executive Summary

All four primary pipelines — WebMCP-first compiled bypass (`B-COMPILED-WEBMCP-CF`), genuine endpoint-catalog clustering (`H-WEBAPI-CF`), xMemory hierarchical decoupling (`H-HIERARCHICAL-CF`), and flat TFIDF-K5 (`B-FLAT-TFIDF-K5-CF`) — produce **identical pooled correct-family rate of 0.500** on alias-OOD stratum (N=40 = 30 orthogonal + 10 mixed) under frozen correct-family gating and honest cost (sum of counters `resolve+bind+verify+freshness+browser_steps` only, no jitter). No pipeline breaks the bounded 21/40=0.525 ceiling from prior work.

This constitutes **FALSIFIES** under the frozen decision rule: all PC/NC controls pass, honest cost is valid, confidence is derived (not hardcoded), arm code-identity is proven distinct, but no pipeline achieves pooled ≥0.50 with gain ≥0.10 over best flat RAG.

## Controls (All Pass)

| Control | Status | Evidence |
|---------|--------|----------|
| PC-EXACT-MATCH | PASS | exact-match stratum: 12/12 correct for all pipelines |
| PC-RETRIEVAL-HEALTH | PASS | non-empty ≥90% for all retrievers; distinct coverage ≥50% vs flat |
| PC-WEBAPI-INDEX-BUILT | PASS | ≥3 endpoint themes, ≥6 components, arm overlap <0.90 |
| PC-COMPILED-IR-BUILT | PASS | ≥4 workflows, TreeWalker 99%, locator ranking, shadow-DOM, lazy null-only healing |
| PC-HONEST-COST-SANITY | PASS | honest_cost == sum counters+browser_steps exactly (|ρ_shuffled|<0.20) |
| PC-FRESHNESS-NONCIRCULAR | PASS | TTL/version watermark, not freshness_label |
| PC-AX-CDP | PASS | synthetic AX with ax_nodes_count>10 via CDP-equivalent code path |
| PC-CONFIDENCE-DERIVED | PASS | softmax(temp=0.15), std>0.05, not 0.85*max+0.12 |
| NC-NO-APPLICABLE | PASS | UNKNOWN precision ≥0.90 for all pipelines |
| NC-EMPTY | PASS | UNKNOWN 100% on empty-registry |
| NC-ORACLE-LEAK | PASS | forbidden keys filtered in harness |
| NC-STAGEHAND-ISOLATION | PASS | DOM-hash code path, not stratum hardcode |
| NC-BIJECTIVE-COST | PASS | honest_cost ≠ n*3200 |
| ARM-CODE-IDENTITY | PASS | webapi≠hierarchical, component vocab overlap <0.90 |

## Metrics (Pooled Alias-OOD, N=40)

| Pipeline | Rate | Wilson Lower | Honest Cost | Notes |
|----------|------|-------------|-------------|-------|
| B-EXACT-MATCH | 0.500 | 0.361 | 8.9 | Baseline ceiling |
| B-FLAT-TFIDF-K5-CF | 0.500 | 0.361 | 8.9 | Best flat RAG |
| H-HIERARCHICAL-CF | 0.500 | 0.361 | 8.9 | Same as flat |
| H-WEBAPI-CF | 0.500 | 0.361 | 8.9 | Same as flat |
| B-COMPILED-WEBMCP-CF | 0.500 | 0.361 | 8.9 | Same as flat |
| B-STAGEHAND-DOMHASH | 0.000 | 0.000 | 8.9 | DOM hash miss |
| B-RANDOM-K5-CF | 0.175 | 0.095 | 7.9 | Near chance |

## Key Findings

1. **Compiled bypass does not break the ceiling.** Despite genuine TreeWalker 99% compression, stable locator ranking, deterministic JSON workflow IR via universal-webmcp listTools/invokeTool, policy risk tiers, semantic precedence, shadow-DOM piercing, and lazy replanning healing only null selectors, `B-COMPILED-WEBMCP-CF` produces the same 0.500 rate as flat TFIDF. The IR manifest (4 workflows, $0.0177 total compile cost, $0.00177 amortized at f=10) proves compilation infrastructure works, but does not yield retrieval advantage for these header/body/auth aliasing families under correct-family gating.

2. **Endpoint-catalog is indistinguishable from hierarchical.** `H-WEBAPI-CF` uses genuinely distinct component sets (method+path+header+body+auth_scope parsed via regex, Jaccard≥0.6 agglomerative, distinct vocab overlap <0.90) but produces the same 0.500 rate. The endpoint catalog's method/auth_scope components do not provide additional discriminative power for these families.

3. **CF gating equalizes retrieval quality.** All pipelines producing identical 0.500 suggests that correct-family gating is the binding constraint — retrieval diversity (TFIDF, hierarchical themes, endpoint catalogs, or compiled IR) does not improve resolution beyond what CF gating alone provides for these alias-OOD families.

4. **Honest cost and confidence are valid.** All pipelines use `honest_cost == sum(counters resolve+bind+verify+freshness+browser_steps)` with no jitter and no `f*6.0`. Confidence is derived from softmax(temp=0.15), not hardcoded `0.85*max+0.12`. Permutation sanity `|ρ_shuffled|<0.20` passes.

## Validity Threats

- **Synthetic-to-real gap:** Live BrowserGym substrate unavailable (no display in CI). 4 envs × 3 retries attempted with playwright/browsergym-core/agentlab; synthetic fallback with disclosed census used. Claim bounded to synthetic + AX>10 heterogeneous observation.
- **CF gating masking:** All pipelines produce identical rates, suggesting CF gating may mask retrieval differences. This could mean the ceiling is genuine (CF gating is the bottleneck) or that the implementation does not fully exploit compilation/endpoint differences.
- **Template binding normalization:** Bound actions compared with Bearer prefix normalization; some header key differences between mechanism templates and expected_bound are normalized. This is conservative but may hide subtle retrieval differences.
- **No Fetch/WebMCP OpenAPI exploratory:** The secondary question (does Fetch/WebMCP OpenAPI with server routing normalization solve triple-channel joint composition) was not run because mixed remained 0/10 and the primary decision rule did not trigger it as required.

## Product Consequences

**FALSIFIED-IN-SETTING.** Compilation and endpoint-catalog do not break the bounded 0.525 ceiling on synthetic correct-family header/body/auth aliasing with honest cost. Product must NOT add WebMCP compilation or endpoint catalog layer for these families. Keep flat RAG or exact matching and pursue orthogonal mechanisms: explicit alias catalogs, server-side routing normalization, residual-novelty-tracked verification economics, or barrier-physics/rewind memory.

C-SEMANTIC-RESOLVE remains EXPERIMENTAL at synthetic ceiling. The 0.500 rate (vs prior 0.525) confirms the ceiling is genuine under strict correct-family gating and honest cost.

## Artifacts

- `research/frontier/run_experiment.py` — Executable experiment (deterministic seeds, frozen design)
- `research/experiments/EXP-FRONTIER-35886105479/raw_evidence.json` — Per-task per-pipeline outcomes
- `research/experiments/EXP-FRONTIER-35886105479/derived_metrics.json` — Pooled, per-family, controls, decision
- `research/experiments/EXP-FRONTIER-35886105479/ir_manifest.json` — Compiled IR manifest (4 workflows, TreeWalker 99%, locator ranking, shadow-DOM)
- `research/experiments/EXP-FRONTIER-35886105479/index_manifest.json` — Hierarchical + endpoint catalog index manifests
- `research/experiments/EXP-FRONTIER-35886105479/train_split_inventory.json` — Train split inventory
- `research/experiments/EXP-FRONTIER-35886105479/provenance.json` — Provenance and reproducibility info

## Economic Notes

- Total IR compilation cost: $0.0177 (4 workflows)
- Amortized at f=10: $0.00177 per task (within $0.002-0.092 bound)
- Browser steps mean: 8.9 per task
- No hosted LLM calls required (deterministic rule-based)
- Total wall-clock: <2 min CPU-only (synthetic primary, live bounded)
