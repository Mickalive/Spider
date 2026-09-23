# EXP-PRODUCT-35860337280 — Product honest residual-novelty economics (Director PIVOT C-RESIDUAL-NOVELTY)

Outcome: FALSIFIES status COMPLETE

## Primary results
- rho_novelty_per_hit: 0.8200 (block-permutation p=0.0002, bootstrap CI [0.750, 0.877])
- R2_delta_per_hit: 0.752
- rho_length per stratum: {'0.0': 0.0, '0.25': -0.0015, '0.5': 0.0, '0.75': 0.0, '1.0': 0.0}

## Decision criteria
- C1 (correctness+calibration): True
- C2 (positive controls): True
- C3 (novelty tracking rho>=0.60): True
- C4 (residual R2_delta>=0.50, |rho_length|<0.20): True
- C5 (honest economics per_hit<=0.85x RAG, saving>=25%): False
- C6 (null controls): True

## Interpretation
C1-C4 PASS: honest branch-derived cost framework with genuine kernel resolve/_bind/verify works. Per-hit isolation confirms rho>=0.60 R2_delta>=0.50 and |rho_length|<0.20 — residual novelty tracks cost, not task length.
C5 FAILS: SPIDER/RAG per_hit is 1.0 at n0 (>0.85 threshold) and 1.573 at n0.25 (>0.85). SPIDER/TERX per_hit is 1.0 at n>=0.5. Stagehand/TERX at n0 are exactly at parity (1.0) but SPIDER more expensive at partial novelty. Honest saving >=25% vs COLD at n0 holds (0.162 ratio) but per_hit baseline advantage fails.
Conclusion: parameterization as ported does NOT yield per_hit advantage over retrievable RAG under QCR with honest 50-tok hits. Per-hit isolation confirms genuine tracking (rho, R2_delta) but economics fail. FALSIFIED per Director mandate — definitively closes work-compression claim for this kernel/cost model/QCR census.
