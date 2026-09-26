# EXP-GRAPH-36018188168 — EXECUTE report (single-node honest re-execution)

**Decision:** SURVIVES_CURRENT_TEST — ALL D1-D13 hold
**status=COMPLETE outcome=SUPPORTS**

## 1. Raw evidence
- Per-request V13 logs: `raw_evidence/raw_evidence_single.jsonl`, `raw_evidence/raw_evidence_synthetic.jsonl` (every request logged before metrics).
- Health gate: worker_pids=[38534, 38535], wal=True, jwt=True, 304=True, sticky=True, rw=True.
- Evaluated pool: single-node n_non304=500 (fresh 300, stale 50, noise 150); synthetic n_non304=360.

## 2. Observations (measured)
- Freshness single-node: TN 1.0000 (wilson lower 0.9874), FA 0.0000, UNKNOWN 0.1429, ECE g/f/s 0.0643/0.0500/0.1500.
- Repair k=1: pooled 1.0000 (wilson lower 0.8865, n=30), tokens 5.00 vs 16, browser 1.00 vs 3, per family {'dom_drift': 1.0, 'param_header_mutation': 1.0, 'cache_expiry': 1.0}.
- Repair k=2: pooled 1.0000 (wilson lower 0.7225, n=10), tokens 10.00 vs 32, browser 2.00 vs 6, per family {'dom_drift': 1.0, 'param_header_mutation': 1.0, 'cache_expiry': 1.0}.
- Repair k=3: pooled 1.0000 (wilson lower 0.7225, n=10), tokens 15.00 vs 48, browser 3.00 vs 9, per family {'dom_drift': 1.0, 'param_header_mutation': 1.0, 'cache_expiry': 1.0}.
- Contamination: k1: disjoint 0.0000, same 0.0000; k2: disjoint 0.0000, same 0.0000; k3: disjoint 0.0000, same 0.0000.
- Verification TEST per k: k1: AUROC 1.0000 prec 1.0000 perm_null 0.4988; k2: AUROC 1.0000 prec 1.0000 perm_null 0.4933; k3: AUROC 1.0000 prec 1.0000 perm_null 0.4933.
- Honesty: max|rho| 0.0000, cost std 0.0000, min within-family fresh std 0.5000.

## 3. Derived measurements -> interpretation
- All gates: {'D1': True, 'D2': True, 'D3': True, 'D4': True, 'D5': True, 'D6': True, 'D7': True, 'D8': True, 'D9': True, 'D10': True, 'D11': True, 'D12': True, 'D13': True}.
- Synthetic sanity: PC1 1.000, PC2 {'dom_drift': 1.0, 'param_header_mutation': 1.0, 'cache_expiry': 1.0}, TN 1.0000, FA 0.0000, UNKNOWN 0.1429, ECE 0.0643; gates pass = {'pc1_1.0': True, 'pc2_0.90_per_family': True, 'freshness_parity': True}.
- Frozen consequence: ALL D1-D13 hold.

## 4. Validity notes
- Deterministic site: measured repair is definitionally identical to B-ORACLE re-observe (ratio 1.0x synthetic / 1.0x single-node); disclosed as ceiling.
- Verify steps D8 gate uses per-probe verify steps (==1 per probe, <=2 per frozen satisfiability proof); total verify steps per repair = k are also reported (M-REPAIR-VERIFY-STEPS-MEAN-Kk).
- N per family at K2/K3 is the frozen 10 total per k (dom 4 / param 3 / cache 3); per-family Wilson lower>0.39 threshold applies at blast radius=1 (10 per family) per frozen D6 text.
- Bootstrap n_iter=5000 trajectory-grouped executed; degenerate flag = [True, True, True] (deterministic zero-variance ceiling, Wilson informative).
- Drift instances run per-id request sequences (1..10 restarting at 1) because the app drifts at X-Request-Num>=6; per-trajectory observed caching is per (trajectory_id, rid).
- n_non304 counts non-304 responses in the evaluated pool (fresh requests + stale instances + noise requests); construction/probe/control requests are additional executed requests not in the evaluated pool.
- Synthetic stage uses stdlib http.server (family via X-Drift-Family header) — regression check only; primary gates are single-node.

## 5. Unresolved
- Distributed n>=800 shared-WAL validation remains UNKNOWN (deferred until this single-node gate passes per spec product_consequence).
- Real LLM token billing and Playwright execution untested (Product lane).
- f=100 amortization untested; only f=10 frozen gate measured.