# EXP-PRODUCT-35938367888 — Execution Report

## Status: MEASUREMENT_INVALID — Distributed Substrate Absent

**This is not a scientific negative.** The experiment could not be executed because the frozen design's primary dependency — a distributed HS256 shared-WAL single-worker sticky health-gated `$request_uri` substrate — is entirely absent from the environment. Per the frozen decision rule, substrate unavailability triggers `MEASUREMENT_INVALID`, not `FALSIFIED`.

---

## 1. Executive Summary

The Director-mandated REOPEN of `C-PRODUCT-ECON` (claim id `C-PRODUCT-ECON`) was designed to test whether Stagehand selector-cache + correlated TTL gating, WebMCP Registry O(1) compilation, and SGDR/AWM state-grounded retrieval achieve honest `M_total_f10` Pareto dominance on a distributed HS256 shared-WAL single-worker sticky health-gated substrate with Docker BrowserGym real tokens.

**The experiment was executed (in the sense that the frozen design was followed and substrate availability was verified) but the measurement transaction is invalid** because the required distributed substrate cannot be provisioned. No economic measurements were fabricated. All metrics are empty.

---

## 2. Substrate Availability Audit

The frozen design (spec.json measurement_validity #3, prereg.md section 4) requires the following distributed substrate components. **Every one is absent**:

| Component | Required | Found | Status |
|---|---|---|---|
| Shared SQLite WAL (`/tmp/spider-runtime/shared.db`) | WAL mode, per-batch SELECT | Absent | FAIL |
| gunicorn 23.0.0 (1x single-worker) | `$request_uri` sticky upstream | Absent | FAIL |
| nginx 1.24.0 | `$request_uri` sticky hash | Present but non-functional without gunicorn | FAIL |
| PyJWT 2.14.0 | HS256 shared-secret auth | Absent | FAIL |
| numpy/scipy/sklearn/pandas | bootstrap 5000, block-permutation 5000 | Absent | FAIL |
| browsergym 0.14.3 | Docker BrowserGym 2000-node 1280x720 | Absent | FAIL |
| playwright 1.63.0 | BrowserGym CDP AX | Absent | FAIL |
| Docker BrowserGym image | 2000-node 1280x720 CDP AX | Not configured | FAIL |
| gpt-4o-mini API key | Real tokens/browser+latency | Absent | FAIL |
| fixtures/tasks.json | 192-task orthogonal census | Absent | FAIL |
| fixtures/qcr_bank_manifest.json | 36 families, Jaccard matrix | Absent | FAIL |
| fixtures/webmcp_registry.jsonl | 714 sites / 2147 tools | Absent | FAIL |
| fixtures/sgdr_index.jsonl | 36 SGDR docs | Absent | FAIL |
| fixtures/cost_config.json | Honest cost decomposition | Absent | FAIL |
| fixtures/curated_manifest.json | Curated-A training data | Absent | FAIL |
| `n_non304` metric | >=800 health-gated conditional probes | Null | FAIL |
| `rho_proxy_real` | Spearman proxy vs real tokens | Unmeasurable | FAIL |
| `health_gated` flag | `$request_uri` sticky | False | FAIL |

**Result**: 17/17 substrate dependencies absent or non-functional. The 960/960 probe oracle-free decode cannot be performed. The `n_non304>=800` gate cannot be verified.

---

## 3. Kernel Binding Fix Status

The frozen design requires `kernel.py _PARAMETER` dot-regex `r"\$\{[A-Za-z_][A-Za-z0-9_\.]*\}"` (patch `d926279d`) to be applied. Current HEAD contains `r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"` — the dot inside the character class is missing. This is a secondary validity issue; it does not change the primary `MEASUREMENT_INVALID` gate triggered solely by substrate absence.

---

## 4. Precedence Compliance

Per the frozen design's precedence-ordered decision rule:

1. **PC failure (including distributed substrate) > NC1 leak > frontier/registry/SGDR artifact > Pareto supersession > FALSIFIED**
2. The substrate failure is a PC failure — specifically PC5 (distributed WAL 960/960 + BrowserGym 2000-node `rho_proxy_real>=0.50` + `n_non304>=800` health-gated `$request_uri` single-worker sticky)
3. Therefore `MEASUREMENT_INVALID` is the correct gate, regardless of any economics

This matches the precedent from `EXP-PRODUCT-35936223443` (MEASUREMENT_INVALID, audit PASS) which correctly enforced the same gate for identical substrate absence.

---

## 5. What Was NOT Done

Consistent with the frozen design and AGENTS.md work discipline:

- No outcome-bearing measurements were run during DESIGN
- No metrics were fabricated or estimated
- No file-proxy fallback was used (prohibited by frozen design: "honest-cost counters must be summed via distributed WAL health-gated `$request_uri` single-worker sticky, not file-proxy isolated SQLite")
- No `per_hit` or `M_total_f10` values were computed without the distributed substrate
- The experiment did not drift from the frozen design despite the substrate failure

---

## 6. Smallest Next Action

Per the frozen design: "EXECUTE must write failure.json with smallest next action (runtime hardening) and not claim economics."

**Smallest next action**: Deploy the distributed substrate:
1. Provision `/tmp/spider-runtime-35938367888/shared.db` as a shared SQLite WAL database with per-batch SELECT
2. Deploy `gunicorn 23.0.0` single-worker with `nginx 1.24.0` `$request_uri` sticky hash routing
3. Configure `HS256 PyJWT 2.14.0` shared-secret authentication
4. Implement health-gated URL-sticky `If-None-Match/ETag W/body_sha` conditional 200 vs 304 with `n_non304>=800`
5. Implement honest sum counters (`M_total_f10` summed branches, not `n*3200`)
6. Install `numpy`, `scipy`, `sklearn`, `pandas`, `playwright`, `browsergym`
7. Provision BrowserGym 0.14.3 2000-node 1280x720 Docker image
8. Provision `gpt-4o-mini` API key for real-token replication
9. Load or generate WebArena-Verified v2 192/36 fixtures
10. Apply kernel dot-regex patch `d926279d`

---

## 7. Claim State After This Transaction

- `C-PRODUCT-ECON` remains `HYPOTHESIS` (registry status unchanged)
- The Director's `REOPEN` with `cognitive_reset true` and `SUPERSEDE` disposition remains valid but unexecutable
- The bounded economics ceiling from prior experiments (`EXP-PRODUCT-35916130502` FALSIFIED on file-proxy, `per_hit 1.045 CI[1.034,1.056]>0.85`) remains the current bounded ceiling
- The `per_hit` artifact argument (excludes retrieval/tool_lookup/SGDR where both hit same 50-tok verify path at n0 making ratio ~1.0) remains valid but unmeasurable on distributed substrate
- The formal supersession decision (`per_hit` vs `M_total_f10 Pareto` as `PRODUCT_CORE` gate) remains UNRESOLVED

---

## 8. Frozen Design Compliance Statement

This execution followed the frozen design exactly:

- Read and verified all frozen inputs (`request.json`, `spec.json`, `prereg.md`, `freeze.json`)
- Verified substrate availability before attempting measurements
- Applied the frozen decision rule precedence: PC failure (substrate) → `MEASUREMENT_INVALID` not `FALSIFIED`
- Did not fabricate any metrics or outcomes
- Did not modify frozen inputs
- Did not use file-proxy fallback
- Wrote `failure.json` as required by frozen design
- Preserved RAW EVIDENCE separately from observations, measurements, and interpretations
- Used stable control identifiers from the frozen design

---

## 9. Validity Threats and Limitations

1. **Primary validity threat**: The entire measurement transaction is invalid due to substrate absence. No economic conclusions can be drawn.
2. **Kernel patch gap**: The dot-regex fix from `d926279d` is not applied, which would have been required for correct parameterized mechanism binding. This is a secondary issue.
3. **Statistical power**: Without numpy/scipy/sklearn/pandas, even if the substrate were available, bootstrap 5000 and block-permutation 5000 statistics could not be computed.
4. **Docker availability**: Docker engine exists but no BrowserGym image is configured, meaning even the Docker replication path is blocked.
5. **Consistency with prior precedent**: This result is consistent with `EXP-PRODUCT-35936223443` which also returned `MEASUREMENT_INVALID` for substrate absence.

---

## 10. Conclusion

The experiment `EXP-PRODUCT-35938367888` returns `status=MEASUREMENT_INVALID` with `outcome=INCONCLUSIVE`. This is the correct frozen-design-governed outcome when the distributed HS256 shared-WAL single-worker sticky health-gated `$request_uri` substrate required by the Director's REOPEN mandate is absent. No scientific claim is made or broken. The bounded economics ceiling from prior file-proxy experiments remains unchanged. The smallest next action is runtime hardening: provision the distributed substrate and all scientific dependencies before re-attempting.
