# EXP-PRODUCT-35958402290 — Execute Report (Product REOPEN C-PRODUCT-ECON)

**Status:** MEASUREMENT_INVALID — **Outcome:** INCONCLUSIVE (infrastructure failure, not scientific falsification).

## 1. What was attempted (frozen checklist order)

1. **Pins:** gunicorn 23.0.0 / PyJWT 2.14.0 comply exactly (PASS); Flask 3.1.3; scientific stack installed but unused.
2. **Kernel MV2 sub-gate:** Patched `src/spider/kernel.py` line12 to dot-regex (product-scope edit), sha `d926279d` matching parent established patch. 5/5 dot-nested spot checks EXECUTABLE at confidence 0.85; `tests/test_kernel.py` 3/3 PASS. Sub-gate PASS in working tree only (HEAD still pre-patch).
3. **Single-node substrate:** `/tmp/spider-runtime/shared.db` absent; nginx 1.24.0 binary present but no `$request_uri` sticky running; If-None-Match/ETag loop not exercised; `n_non304=0 < 800`. PC5 FAIL.
4. **BrowserGym + real tokens:** `docker pull ghcr.io/servicenow/browsergym:0.14.3` denied; browsergym pip not importable; `OPENAI_API_KEY` absent. `rho_proxy_real` unmeasurable. MV5 FAIL.
5. **Fixtures:** `pip install webarena` has no matching distribution (Hard258 not staged); `sgdr_index` absent repo-wide; qcr/dsm/cost verified only as cross-experiment references. MV1/MV6/MV7 staging FAIL.
6. **Economics/statistics:** Not run — frozen rule bans file-proxy fallback for SURVIVES, so no proxy Pareto/rho/calibration numbers are reported. All primary metrics null (not zero).

## 2. Decision-rule evaluation

- **Clause (1) MEASUREMENT_INVALID triggers:** PC5 fail; Docker+gpt-4o-mini unavailable; fixtures missing; `n_non304<800`; census not heterogeneous-staged. Any single trigger suffices; five fired.
- **Clause (2)/(3):** Not reached — controls are UNKNOWN (nulls not executed, non-degenerate by vacuity, not by PASS), so neither FALSIFIED nor SURVIVES is licensed.
- **SUPERSEDE clause:** Not testable; per_hit and M_total both unmeasured on honest substrate.

## 3. Interpretation (distinct from observation)

No claim update for C-PRODUCT-ECON is justified: the honest-substrate Pareto question remains UNKNOWN, and the bounded file-proxy rejection (per_hit ~1.0 artifact, rho 0.472) is neither reopened nor extended. The kernel dot-regex fix replicates for the third time as a working-tree-only patch — durability (commit) is the recurring blocker, and AUDIT should treat HEAD as still pre-patch.

## 4. Smallest next actions (ordered)

1. Provision `/tmp/spider-runtime/shared.db` WAL single-worker gunicorn 23.0.0 + nginx `$request_uri` sticky + PyJWT HS256 with real If-None-Match/304 loop; log `n_non304>=800` stratified + TN>=0.85 (runtime lane dependency).
2. Authorize GHCR pull for BrowserGym 0.14.3 and provision `OPENAI_API_KEY` for gpt-4o-mini 15-step (rho_proxy_real gate).
3. Commit the kernel dot-regex patch durably (currently working-tree only across parent + this run).
4. Stage Hard258 (or disclosed 192/36) + qcr TAU0.30 + dsm 714/2147 + sgdr 36 TRAIN-only with hashes; then re-execute this identical frozen design.
