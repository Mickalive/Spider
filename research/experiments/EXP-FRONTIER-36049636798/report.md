# EXP-FRONTIER-36049636798 EXECUTE Report

**Lane:** frontier  
**Claim:** C-RESIDUAL-NOVELTY (deterministic compilation bypass PIVOT)  
**Status:** MEASUREMENT_INVALID  
**Outcome:** NOT_APPLICABLE (infrastructure failure, not scientific falsification)  
**Elapsed:** 0.001s  
**Timestamp:** 2026-09-24T19:49:20.342257Z

## Frozen Design Summary

This experiment was a Director-mandated PIVOT SUPERSEDE with cognitive_reset=true (cycle 36049089810) from the 17-deep alias-catalog/routing/WebMCP tunnel (bounded at pooled 21/40=0.525 Wilson [0.352,0.648], 0/10 mixed triple-channel, routing gain 0.0 p=1.0) and valid non-Pareto falsification of residual-novelty economics under honest per-trajectory hard-reset sum counters on 36-family orthogonal Jaccard<0.30 fixture (EXP-FRONTIER-36042599040 PASS, all 11 PCs/NCs PASS).

The frozen hypothesis (H1): On heterogeneous mixed triple-channel tasks (WebArena-Verified v2 192/36 or WebGym 292k dedup manifest >=10 families pairwise bigram Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 at 1280x720 CDP AX>10), deterministic compilation bypass — first-run BrowserGym 1280x720 CDP trajectory capture -> TreeWalker 99% compression + stable locator ranking + deterministic JSON/Python DAG with speculative guards + bailout fallback to LLM — will achieve honest end-to-end economics Pareto dominance versus both cold LLM browsing and alias catalog+routing+hierarchical xMemory / flat TF-IDF RAG k5.

## Substrate Diagnostic Results

| Substrate Component | Required | Available | Details |
|---|---|---|---|
| BrowserGym (browsergym-core) | Yes | **NO** | ModuleNotFoundError |
| Playwright (CDP support) | Yes | **NO** | ModuleNotFoundError |
| WebGym 292k data | Yes | **NO** | Directory not found |
| Intel diverse_site_manifest.json | Yes (>=10 families Jaccard<0.30) | **NO** | File not found, 0 families |
| Runtime WAL (/tmp/spider-runtime/shared.db) | Yes (n_non304>=800 stratified) | **NO** | File not found |
| Heterogeneity adequacy (frozen) | >=10 families, Jaccard mean<0.15, max<0.30 | **FAIL** | 0 families |
| Coverage adequacy (frozen) | Pooled>=40, Mixed>=10 | **FAIL** | 0 tasks |

## Controls Evaluation

### Positive Controls (ALL must PASS for SURVIVES_CURRENT_TEST)

| Control | Status | Reason |
|---|---|---|
| PC-COMPILATION-PIPELINE | NOT_RUN | BrowserGym/CDP missing |
| PC-HONEST-COST-SANITY | NOT_RUN | No trajectories captured |
| PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST | **FAIL** | Manifest families=0 <10 |
| PC-TRAIN-TEST-DISJOINT | NOT_RUN | No train/test split without manifest |
| PC-CALIBRATION-DERIVED | NOT_RUN | No live data |
| PC-BROWSERGYM-SUBSTRATE | **FAIL** | browsergym_available=false, playwright_available=false |

### Null Controls (ALL must PASS for SURVIVES_CURRENT_TEST)

| Control | Status | Reason |
|---|---|---|
| NC-EMPTY-COMPILE | NOT_RUN | No compilation pipeline |
| NC-NO-APPLICABLE-MIXED | NOT_RUN | No mixed triple-channel tasks |
| NC-ORACLE-LEAK | NOT_RUN | No live data to audit |
| NC-BIJECTIVE-COST | NOT_RUN | No honest counters executed |
| NC-SHUFFLED-NULL | NOT_RUN | No trajectories for permutation |
| NC-GUARD-SPECIFICITY | NOT_RUN | No guard pipeline |

**PC All Pass:** False  
**NC All Pass:** False

## Survival Criteria (Frozen Decision Rule)

| Criterion | Required | Result |
|---|---|---|
| All PCs PASS | Yes | **FAIL** |
| All NCs PASS | Yes | **FAIL** |
| S1 Pareto: saving>=25% vs cold, dominance vs RAG/alias at f10/f100 | Yes | NOT_EVALUATED |
| S2 Mixed: >=4/10 mixed, pooled>=0.60, gap>=0.07 vs alias | Yes | NOT_EVALUATED |
| S3 Latency: hot-path <200ms mean, <100ms median, 0 tokens | Yes | NOT_EVALUATED |
| S4 Calibration: UNKNOWN>=0.85, false<=0.10, ECE<=0.15, |rho_shuffled|<0.20 | Yes | NOT_EVALUATED |

## Verdict

**MEASUREMENT_INVALID** — The frozen experiment cannot be executed because the required measurement substrate is entirely absent. This is an infrastructure failure, NOT a scientific falsification of the compilation bypass hypothesis or C-RESIDUAL-NOVELTY.

Per the frozen `measurement_validity[0]` and `decision_rule`:
> "If BrowserGym/CDP or Intel diverse manifest unavailable or n_non304 stratified insufficient, declare live_available=false and MEASUREMENT_INVALID diagnostic (0.035s-style) without falsifying claim — do not substitute synthetic disjoint alphabets as live evidence."

> "MEASUREMENT_INVALID if any PC/NC fails or manifest <10 families or pooled<40 or mixed<10 or n_non304 insufficient or BrowserGym/CDP missing or guard pipeline fidelity <90% or locator top-1 <95% — no inference to product; requires substrate repair..."

## Prior Valid Evidence Preserved (Per Parent Handoff carry_forward.established)

1. **Alias-catalog/routing/WebMCP tunnel bounded**: 21/40=0.525 pooled, 0/10 mixed triple-channel, routing gain 0.0 p=1.0 on synthetic diverse substrate
2. **Honest residual-novelty non-Pareto validly FALSIFIED**: EXP-FRONTIER-36042599040 PASS, all 11 PCs/NCs PASS, rho=0.4837<0.60, ECE=0.216>0.15, RAG dominance false at f10/f100
3. **Physics Dirichlet-Multinomial companion**: BC~0 rel_sep<200 with trajectory-grouped exact Gamma-ratio |perm-analytic|<0.03 at N=1000-1999 on real BrowserGym 1280x720

## Required Fixes for Live Test

1. **Intel**: Produce diverse-site manifest deterministic seed 42 on WebGym 292k >=50 eTLD+1 or WebArena-Verified v2 192/36 with >=10 families pairwise Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2, AX>10 mean>15 std>5, raw N>=500 (>=50/family)
2. **Runtime**: Deploy single-worker sticky Flask HS256+nginx substrate with /tmp/spider-runtime/shared.db WAL, sticky cookie, If-None-Match/ETag TTL 60s conditional probes, n_non304>=800 stratified >=80/family, honest per-trajectory hard-reset sum counters, trajectory-grouped |rho_shuffled|<0.20
3. **Frontier/Graph**: Install playwright browsergym-core agentlab with display support for 1280x720 CDP AX>10 trajectory capture

## Do Not Assume (Per Parent Handoff carry_forward.do_not_assume)

- This MEASUREMENT_INVALID does not falsify or validate C-WEB-DYNAMICS or C-RESIDUAL-NOVELTY
- Alias-catalog 21/40=0.525 or residual-novelty non-Pareto on synthetic TAU0.30 gate does not imply live BrowserGym will also be non-Pareto
- Jaccard 0.0 disjoint alphabets does not generalize to natural Web overlap 0.30-0.60
- Prior synthetic cost formulas (n*3200, f*6.0) are not evidence for live LLM Pareto
- Distributed n>=800, 1280x720 CDP AX>10 heterogeneity, or health-gated n_non304>=800 have NOT been tested
- Agent priors from director_mandate are general priors, not SPIDER evidence

## Next Action

Repair substrate per dependencies, then re-execute same frozen gate. Do NOT run 18th alias/routing permutation (VOI~0 per Director comparative_reasoning). Continue=false awaiting Global Research Director pulse.

---
*Report generated from frozen EXECUTE stage. Raw evidence preserved in artifacts/substrate_diagnostic.json*
