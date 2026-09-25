# EXP-GRAPH-36106653880 — Execution Report

## Summary

**Experiment:** C-DELTA-REPAIR bounded distributed transfer test
**Lane:** graph
**Status:** COMPLETE
**Outcome:** MIXED

## Distributed Substrate

Health gate FAILED: Distributed substrate did not become ready (workers/nginx startup failed)

## Decision Rules

| Rule | Metric | Threshold | Observed | Pass |
|------|--------|-----------|----------|------|
| D1 | TN (Wilson lower) | >=0.85 | 0.0000 | False |
| D2 | FA (Wilson upper) | <=0.10 | 0.0000 | True |
| D3 | Repair (Wilson lower) | >=0.70 | 0.0000 | False |
| D4 | Per-family repair | >=0.70 | {} | False |
| D5 | Contamination (Wilson upper) | <0.10 | 0.1611 | False |
| D6 | AUROC/Precision | >=0.75/>=0.80 | 0.5000/0.0000 | False |
| D7 | Amortized cost | <cold | tokens=15.0<16, browser=1<3 | True |

**All rules PASS:** False

## Baselines

- **B-COLD**: Full cold re-exploration at 16 tokens, 3 browser
- **B-NO-GUARD**: Always EXECUTABLE (FA=1.0) — bounded rejection
- **B-VERBATIM**: Literal replay (repair=0 on drift)
- **B-RETRIEVAL**: Retrieval/RAG without patch

## Honesty Gates

- Per-trajectory-reset integer sum-counter (no jitter/parity/bijective)
- 1000 trajectory-grouped permutations (max|rho|<0.20)
- 5000 family-stratified trajectory-grouped bootstraps
- Registry-clone re-verification (disjoint-id contamination)

## Validity Notes

- DISTRIBUTED_MEASUREMENT_INVALID per V12: distributed substrate unavailable. Per spec, this does NOT retroactively falsify single-node SURVIVES.
- Single-node SURVIVES at EXP-GRAPH-36018188168 remains the prior established result.
- The distributed transfer test could not be executed due to infrastructure failure.

## Conclusions

- **Claim C-DELTA-REPAIR**: MIXED on distributed substrate
- **Claim ceiling**: No scientific conclusion (measurement invalid)
- **Product consequence**: No promotion authorized
