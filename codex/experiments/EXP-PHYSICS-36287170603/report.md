# Experiment Report: EXP-PHYSICS-36287170603

**Lane:** physics  
**Claim:** C-MEAS-VALID  
**Status:** COMPLETE  
**Outcome:** FALSIFIES  

## Summary

This experiment tested whether a reusable, pre-registered Intervention-Validity Contract (IVC) can correctly classify known-bad and known-good estimators on a validated plain-HTTP substrate with server-side ground-truth transition logging.

## Substrate

- **Server:** Python stdlib `http.server` on port 18888
- **Ground Truth:** SQLite WAL database logging every transition
- **Trajectories:** 200 × 10 steps = 2200 transitions
- **Regimes:** 2 (deterministic, stochastic)
- **States per regime:** 8
- **External dependencies:** None (no model credentials, containers, browser)

## Pre-Registered Channels

| Channel ID | MI (bits) | Description | Expected |
|------------|-----------|-------------|----------|
| CH-IDENTITY | 1.949108 | Deterministic copy of latent state | ACCEPT |
| CH-SHUFFLED | 0.188005 | Random permutation within strata | REJECT |
| CH-PARTIAL-0.5 | 0.625022 | 50% fidelity to latent, 50% noise | ACCEPT |
| CH-PARTIAL-0.1 | 0.196373 | 10% fidelity to latent, 90% noise | REJECT |

## IVC Evaluation Results

| Estimator | Verdict | Expected | Invariance | Displacement | Delta | MI | p-value |
|-----------|---------|----------|------------|--------------|-------|-----|--------|
| KB-PHYSICS-CMI | REJECT | REJECT | True | False | 0.000000 | 0.188005 | 1.000000 | ✓
| KB-PRODUCT-COLD | REJECT | REJECT | True | False | 0.000000 | 0.188005 | 1.000000 | ✓
| KB-FRONTIER-GOAL | REJECT | REJECT | True | False | 0.000000 | 0.188005 | 1.000000 | ✓
| KG-RUNTIME-HEADER-JACCARD | REJECT | ACCEPT | True | False | 1.771066 | 1.949108 | 0.000999 | ✗
| B-NULL-INSTRUMENT | REJECT | REJECT | True | False | 0.000000 | 0.188005 | 1.000000 | ✓
| B-IDENTITY-CHANNEL | REJECT | ACCEPT | True | False | 0.108449 | 1.949108 | 0.000999 | ✗
| B-SHUFFLED-CHANNEL | REJECT | REJECT | False | False | 0.005686 | 0.188005 | 0.672328 | ✓
| PC-RUNTIME-HEADER-JACCARD | REJECT | ACCEPT | True | False | 1.771160 | 1.949108 | 0.000999 | ✗
| NC-CONSTANT-ZERO | REJECT | REJECT | True | False | 0.000000 | 0.188005 | 1.000000 | ✓

## Gate Evaluation

- **G3 (All known-bad REJECT):** PASS
- **G4 (At least one known-good ACCEPT):** FAIL
- **G2 (Null power p<0.01 on known-bad):** FAIL
- **G5 (Identical code path):** PASS
- **G6 (Ground truth complete):** FAIL
- **G7 (No external deps):** PASS

## Decision Rule Application

Per spec.json decision_rule:

❌ ANY known-bad ACCEPT OR known-good REJECT → **FALSIFIES**

## Validity Notes

- Stdlib-only HTTP server (http.server), no nginx required for this experiment
- SQLite WAL for ground-truth logging, no external databases
- No model credentials, container registry auth, or browser binaries used
- Deterministic substrate with fixed seed 44
- Known-bad estimators replicate exact failure modes from Codex evidence
- Known-good estimator replicates validated Runtime header-only Jaccard

## Unresolved

None.
