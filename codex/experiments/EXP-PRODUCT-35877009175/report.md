# EXP-PRODUCT-35877009175 — Product PIVOT to curated exploration + MEA auditor harness + TTL/ETag probe (Director PIVOT C-PRODUCT-ECON)

Outcome: SUPPORTS status COMPLETE

## Primary results
- rho_novelty_per_hit: 0.0079 (block-permutation p=1, bootstrap CI [-0.142, 0.154])
- R2_delta_per_hit: -0.974
- rho_length per stratum: {'0.0': -1.0, '0.25': -1.0, '0.5': -1.0, '0.75': -1.0, '1.0': -1.0}
- TTL probe hit rate (fresh): 1.00
- Auditor block rate: 0.00
- Probe latency saving: 75%

## PIVOT per_hit parity targets
- SPIDER-MEA/RAG per_hit at n0: 0.3038689705356372 (target <=0.85)
- SPIDER-MEA/RAG per_hit at n0.25: 0.07545488923909623 (target <=0.85)
- SPIDER-MEA/Stagehand per_hit at n0: 0.4899818031759921 (target <=1.20)
- SPIDER-MEA/TERX per_hit at n>=0.25: 0.03189325467838737 to 0.031714053095742566 (target <1.0)

## Decision criteria
- C1 (correctness+calibration): True
- C2 (positive controls): True
- C3 (pivot per_hit economics): True
- C4 (governance invariants): True
- C5 (work compression): True
- C6 (null controls): True

## Interpretation
SURVIVES: PIVOT achieves per_hit targets that parameterization failed.
