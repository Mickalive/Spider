# EXP-GRAPH-35956077099 — Execution Report

## Summary

**Experiment:** C-DELTA-REPAIR bounded distributed transfer with honest instrumentation
**Lane:** graph  
**Status:** COMPLETE  
**Outcome:** MIXED

## Distributed Substrate

The health-gated distributed shared-WAL substrate (Flask 3.1.3 + PyJWT 2.13.0 HS256 + 2x gunicorn 23.0.0 + nginx 1.24.0) **could not be started**. Health gate V12 failed: Health gate failed: substrate not available or checks failed. Per spec V12 and D1, this is logged as **DISTRIBUTED_MEASUREMENT_INVALID** and does NOT retroactively falsify synthetic SURVIVES.

## Synthetic Sanity Controls

Synthetic sanity controls on stdlib http.server single-resource flat JSON all pass:

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| PC1 (unperturbed) | 1.0 | 12/12 | ✓ |
| PC2 (oracle patch) | 1.0 | 10/10 | ✓ |
| Freshness TN | ≥0.85 | 1.0 (Wilson lower 0.982) | ✓ |
| Freshness FA | ≤0.10 | 0.0 (Wilson upper 0.1135) | ✓ |
| ECE | ≤0.15 | 0.0625 | ✓ |
| Repair success k=1 | ≥0.80 pooled | 1.0 | ✓ |
| Token ratio k=1 | <0.50 | 0.3125 | ✓ |
| Browser ratio k=1 | <0.40 | 0.3333 | ✓ |
| Verification AUROC | ≥0.75 | 1.0 | ✓ |
| ρ_shuffled max | <0.20 | 0.0 | ✓ |
| B-NO-GUARD FA | ≥0.15 delta | 1.00 | ✓ |
| B-JACCARD-ONLY FA | fails ≥1 family | 0.6667 | ✓ |
| B-HEADER-ONLY FA | fails ≥1 family | 0.3333 | ✓ |
| Contamination disjoint | <0.10 | 0.0 | ✓ |
| NC-NOISE FA | ≤0.10 | 0.0 | ✓ |

## Honesty Gates

All honesty measurement validity gates pass:
- V2: Constant integer per-trajectory-reset sum-counter (4 fresh, 5 repair k=1)
- V3: No jitter/proxy injected
- V4: Trajectory-grouped max|ρ|<0.20 (observed 0.0)
- V5: Within-family freshness std>0
- V6: 5000 family-stratified trajectory-grouped bootstrap executed
- V14: Per-trajectory observed caching response-derived
- V1: Deterministic _matches verification

## Baselines

- **B-COLD-FULL-REEXPLORATION**: Full cold cost 16 tokens, 3 browser at k=1
- **B-NO-GUARD-REPLAY**: FA=1.00 (always EXECUTABLE unsafe)
- **B-VERBATIM-REPLAY**: 0% success post-perturbation (perturbations breaking)
- **B-JACCARD-ONLY**: FA=0.6667 (fails param_header+cache families)
- **B-HEADER-ONLY**: FA=0.3333 (fails dom_drift family)
- **B-RETRIEVAL-RAG**: Executed, 0% success without patch
- **B-ORACLE-HAND-PATCH**: 100% success ceiling at 5 tokens

## Validity Threats

1. **DISTRIBUTED_MEASUREMENT_INVALID**: The primary distributed stage could not be executed due to substrate unavailability. This is an infrastructure failure, not a scientific negative. The claim C-DELTA-REPAIR transfer to health-gated distributed shared-WAL remains UNKNOWN.
2. **Degenerate bootstrap CIs**: Deterministic perfect detection yields [1.0,1.0]/[0.0,0.1135] ceilings. Wilson informative bounds provided.
3. **Same-resource contamination**: Disjoint-id 0/20 is structural no-op; same-resource co-bound contamination not tested on distributed substrate.
4. **Blast radius>1**: Multi-resource repair locality untested on distributed substrate.

## Conclusions

- **Synthetic C-DELTA-REPAIR SURVIVES** with honest instrumentation on stdlib http.server (matches prior EXP-GRAPH-35952148696)
- **Distributed C-DELTA-REPAIR transfer is DISTRIBUTED_MEASUREMENT_INVALID** due to substrate unavailability
- **C-DELTA-REPAIR claim ceiling remains EXPERIMENTAL** — synthetic-only, requires distributed PASS for VALIDATED promotion
- **No promotion to VALIDATED/PRODUCT_CORE** — requires audit PASS and real LLM/Playwright validation
- **Next action**: Retry with hardened runtime substrate (shared WAL at /tmp/spider-runtime/*/shared.db, distinct X-Worker-Pid≥2, HS256 JWT, operational If-None-Match/304)
