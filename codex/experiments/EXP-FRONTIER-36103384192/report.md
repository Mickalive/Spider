# EXP-FRONTIER-36103384192 Report — Heterogeneous Residual-Novelty Verification Economics

**Lane:** frontier — C-RESIDUAL-NOVELTY (pay-novelty-not-length)
**Status:** MEASUREMENT_INVALID
**Outcome:** NOT_APPLICABLE
**Freeze:** 2026-09-25T06:38:04.292858+00:00

## Executive Summary

This experiment tests whether SPIDER residual-novelty verification economics with honest per-trajectory hard-reset integer sum counters (TAU0.30 topology-gated + freshness TN>=0.85) demonstrates pay-novelty-not-length on heterogeneous shared-manifest WebChoreArena 532 + WebArena-Verified 812/Hard258/192/36 L=8-14 orthogonal holdout.

**Result: MEASUREMENT_INVALID (validity gate, not scientific falsification)**

All required live substrates are unavailable:
- BrowserGym 1280x720 CDP stack (browsergym-core 0.14.3, playwright 1.63.0, agentlab 0.4.2) — Python packages not installed
- Runtime HS256 sticky WAL at `/tmp/spider-runtime/shared.db` — not deployed
- Intel diverse site manifest at `research/intel/diverse_site_manifest.json` — not found
- Graph freshness gate TN>=0.85 — not validated
- External Pareto references (Agentic Compilation DSM / Agent JIT blind reproductions) — not available

Per frozen `spec.json` measurement_validity[0] and `prereg.md` section 12/13: **If Intel shared manifest unavailable or BrowserGym CDP or Runtime WAL insufficient (n_non304<360 single-node) declare live_available=false and MEASUREMENT_INVALID diagnostic without falsifying claim — do not substitute synthetic disjoint alphabets (36-family TAU0.30 Jaccard 0.0 gate) as heterogeneous evidence.**

## Substrate Diagnostic

| Substrate | Required | Available | Details |
|-----------|----------|-----------|---------|
| BrowserGym 1280x720 CDP | browsergym-core 0.14.3 + playwright 1.63.0 + agentlab 0.4.2 + chromium | **NO** | Python packages not installed (chromium binary present) |
| Runtime HS256 Sticky WAL | n_non304>=360 single-node, X-Worker-Pid>=10, If-None-Match/304 proxy_cache HIT | **NO** | `/tmp/spider-runtime/shared.db` not found |
| Intel Diverse Manifest | >=10 families Jaccard<0.30 mean<0.15 AX>10 DOM>=2000 pooled>=40 mixed>=10 | **NO** | `research/intel/diverse_site_manifest.json` not found |
| Graph Freshness Gate | TN>=0.85, >=30 stale probes | **NO** | `research/graph/state.json` not found |
| Agentic Compilation DSM Repro | Blind reproduction for Pareto baseline | **NO** | `research/intel/agentic_compilation_repro.json` not found |
| Agent JIT Repro | Blind reproduction for Pareto baseline | **NO** | `research/intel/agent_jit_repro.json` not found |

**Overall:** `live_available=false`, `substrate_adequate=false`, `heterogeneity_adequate=false`, `coverage_adequate=false`

## Controls Status

All positive controls (PC) and null controls (NC) requiring live execution are **NOT_RUN**:

| Control | Status | Reason |
|---------|--------|--------|
| PC-HONEST-COST-SANITY | FAIL (NOT_RUN) | Requires live per-trajectory hard-reset integer counters with TAU+freshness mask |
| PC-WEBCHORE-MANIFEST-ORTHOGONAL | FAIL (NOT_RUN) | Requires Intel manifest with >=10 families Jaccard<0.30 |
| PC-TRAIN-TEST-DISJOINT | FAIL (NOT_RUN) | Requires Intel manifest trajectory-grouped holdout |
| PC-CALIBRATION-DERIVED | FAIL (NOT_RUN) | Requires live execution with TAU+freshness gating |
| PC-NOVELTY-MONOTONICITY | FAIL (NOT_RUN) | Requires live execution with controlled novelty strata |
| PC-BUILD-COST-ISOLATED | PASS (definition only) | Build cost definition frozen in spec; actual ops unverifiable |
| PC-BROWSERGYM-SUBSTRATE | FAIL | BrowserGym stack not available |
| PC-FRESHNESS-GATED-BAILOUT | FAIL | Graph freshness gate not validated |
| NC-EMPTY-REGISTRY | FAIL (NOT_RUN) | Requires live execution |
| NC-NO-APPLICABLE | FAIL (NOT_RUN) | Requires live execution |
| NC-ORACLE-LEAK | FAIL (NOT_RUN) | Requires live harness inspection |
| NC-BIJECTIVE-COST | FAIL (NOT_RUN) | Requires live honest cost measurements |
| NC-SHUFFLED-NULL | FAIL (NOT_RUN) | Requires live execution + 5000 permutations |
| NC-GUARD-SPECIFICITY | FAIL (NOT_RUN) | Requires live guard ablation |

**Per frozen decision rule: MEASUREMENT_INVALID if any PC or NC fails.** This is a validity gate, not a scientific negative result.

## Scientific Context (from Director Mandate)

- **Prior synthetic falsification:** EXP-FRONTIER-36042599040 validly FALSIFIED synthetic alias economics on 36-family TAU0.30 Jaccard 0.0 gate (rho=0.4837 CI[0.410,0.552] <0.60, ECE=0.216>0.15, RAG dominance false) with all 11 PCs/NCs PASS
- **Alias ceiling bounded:** 17-deep retrieval-diversity tunnel at 21/40=0.525 pooled Wilson [0.352,0.648] with 0/10 mixed routing gain 0.0 (EXP-FRONTIER-36052053591 lineage)
- **4 deterministic compilation bypasses:** All MEASUREMENT_INVALID bounded at same 0.525 ceiling with 0/10 mixed
- **Director CONTINUE with cognitive_reset=true:** PIVOT to WebChoreArena heterogeneous basin where compressible structure actually exists (human 50.2% vs GPT-5 48.3% unsaturated, WebArena saturates)
- **Comparative reasoning:** 18th alias permutation VOI~0; C-SEMANTIC-RESOLVE blocked pending Intel hierarchical census; C-WEB-DYNAMICS PARKED pending diverse manifest. This is the only unblocked high-upside orthogonal mechanism.

## Validity Threats & Representation Loss

1. **No live heterogeneous evidence:** This experiment provides zero evidence for or against C-RESIDUAL-NOVELTY on the target distribution. The prior synthetic FALSIFIED-IN-SETTING (rho 0.4837) is bounded to TAU0.30 disjoint Jaccard 0.0, not live Jaccard 0.30-0.60.

2. **Substrate dependencies are hard gates:** The Director mandate explicitly lists Intel shared manifest, Runtime health-gated WAL, BrowserGym CDP, and Graph freshness as dependencies. None are satisfied.

3. **Synthetic substitution forbidden:** Per frozen spec BINDING-RULE and prereg, the synthetic 36-family Jaccard 0.0 fixture must NOT be substituted as heterogeneous evidence.

4. **Agent priors are not SPIDER evidence:** Director mandate agent priors (Agentic Compilation DSM $0.002-0.092, Agent JIT 10.4x, hierarchical decomposition, path dependence) are labeled priors distinguished in validity_notes/do_not_assume; they cannot satisfy S1-S6.

## Unresolved Questions (Carried Forward)

All primary survival criteria S1-S6 remain unevaluated:
- S1: rho_novelty >=0.60 lower>0.40 p<0.05 (TAU+freshness-gated)
- S2: pooled |rho_length|<0.20 upper<0.25 p>=0.05 (decoupling)
- S3: per-stratum |rho_length|<0.20 upper<0.30 for all 5 novelty strata + length tertiles
- S4: calibration UNKNOWN precision>=0.85 false_accept<=0.10 ECE<=0.15 upper<=0.18
- S5: Pareto saving>=25% vs cold, strict dominance vs RAG k5 at f10/f100, external DSM/JIT reference
- S6: honest gap >0.35, |rho_proxy|<0.60, |rho_shuffled|<0.20 centered

Infrastructure unblockers needed:
- Intel diverse-site manifest delivery (WebGym 292k 50 eTLD+1 or WebArena-Verified Hard expanded)
- Runtime health-gated single-worker sticky Flask HS256+nginx WAL deployment
- BrowserGym 1280x720 CDP stack installation
- Graph freshness gate validation

## Artifacts

- `artifacts/substrate_diagnostic.json` — Complete substrate availability diagnostic with SHA256

## Next Steps

Per handoff recommendation from parent EXP-FRONTIER-36100559236: **BLOCK frontier EXECUTE until Global Research Director scheduled pulse after all substrates PASS.** Do not retry with synthetic fixture. Upon substrate PASS, re-execute identical frozen shootout with honest per-trajectory hard-reset sum counters and 5000 family-stratified bootstrap + 5000 block-permutation + 5000 global permutation.
