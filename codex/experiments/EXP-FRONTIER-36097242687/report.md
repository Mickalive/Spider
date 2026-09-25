# EXP-FRONTIER-36097242687 — Report: WebChoreArena Heterogeneous Residual-Novelty Verification Economics (PIVOT SUPERSEDE)

**Status:** MEASUREMENT_INVALID (substrate insufficient)  
**Outcome:** NOT_APPLICABLE  
**Lane:** frontier  
**Claim:** C-RESIDUAL-NOVELTY (HYPOTHESIS)

## Substrate Diagnostic

| Component | Status |
|-----------|--------|
| browsergym | False |
| browsergym.core | False |
| playwright | False |
| agentlab | False |
| chromium present | True |
| PyPI reachable | True |
| Intel diverse manifest | False (families: 0) |
| Runtime WAL | False |
| X-Worker-Pid | None |
| n_non304 | None |
| Substrate adequate | False |
| Heterogeneity adequate | False |
| Coverage adequate | False |

## Summary

The frozen experiment requires a live heterogeneous substrate:
- **WebChoreArena 532** tedious/memory tasks + **WebArena-Verified Hard 192/36** combined manifest ≥10 families pairwise canonical bigram Jaccard <0.30 mean <0.15
- **BrowserGym 0.14.3** 1280x720 CDP with AX>10 mean>15 std>5 DOM≥2000
- **Runtime** health-gated single-worker sticky HS256+nginx WAL with n_non304≥360 single-node (else ≥800 distributed), X-Worker-Pid≥10, If-None-Match/304 handling, proxy_cache HIT
- **Graph** freshness gate TN≥0.85 with ≥30 stale probes

**None of these dependencies are satisfied.** The environment lacks:
1. BrowserGym stack (browsergym-core 0.14.3, playwright 1.63.0, agentlab 0.4.2)
2. Intel diverse-site manifest (WebChoreArena 532 / WebArena-Verified Hard 192/36)
3. Runtime WAL at /tmp/spider-runtime/shared.db with health-gated metrics
4. Graph freshness gate validation

Per the frozen `measurement_validity[0]` and `decision_rule`, this triggers `MEASUREMENT_INVALID` with `live_available=false` — a diagnostic, not a scientific falsification. No outcome-bearing measurements were run. All positive and null controls are `NOT_RUN`.

## Prior Evidence Preserved

- **EXP-FRONTIER-36042599040** (synthetic TAU0.30): Valid `FALSIFIED-IN-SETTING`, rho_novelty=0.4837 CI[0.4102,0.5523] <0.60, ECE=0.216 >0.15, RAG dominance false at f10/f100, all 11 PCs/NCs PASS. Bounded to synthetic Jaccard 0.0 disjoint-alphabet gate.
- **EXP-FRONTIER-36052053591** lineage: Alias catalog+routing+hierarchical xMemory bounded at 21/40=0.525 pooled Wilson [0.352,0.648], 0/10 mixed routing gain 0.0 p=1.0. Retrieval-diversity ceiling preserved.
- **EXP-FRONTIER-36095585747**: Prior diagnostic `MEASUREMENT_INVALID` substrate absent (0.124s), compilation bypass with invariant protocol remains UNTESTED on live heterogeneous gate.

## Director Mandate Context

This experiment was a Director-mandated **PIVOT** (`cognitive_reset=true`, `SUPERSEDE` parent handoff) after:
1. Valid synthetic non-Pareto falsification (36042599040)
2. 4 consecutive `MEASUREMENT_INVALID` deterministic compilation attempts bounded at 21/40=0.525

The PIVOT targeted WebChoreArena heterogeneous tasks where compressible cross-site/memory structure exists (human 50.2% vs GPT-5 48.3% unsaturated), but the substrate is not yet available.

## Required Fixes (from validity_notes)

1. Intel lane must produce `research/intel/diverse_site_manifest.json` or `data/webgym_292k` / `data/webarena_verified_hard` with ≥10 families Jaccard<0.30
2. Runtime lane must deploy health-gated single-worker sticky Flask HS256+nginx WAL at `/tmp/spider-runtime/shared.db` with n_non304≥360, X-Worker-Pid≥10
3. BrowserGym 0.14.3 + playwright 1.63.0 + agentlab 0.4.2 must be installable (chromium present, PyPI reachable)
4. Graph freshness gate TN≥0.85 must be validated on WebChoreArena cross-site sessions

Upon substrate PASS (all 8 PCs including PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST, PC-BROWSERGYM-SUBSTRATE, PC-WEBMCP-REGISTRY≥95%, PC-FRESHNESS-GATED-BAILOUT TN≥0.85 and all 8 NCs PASS), the identical frozen shootout should be re-executed testing S1-S6.

