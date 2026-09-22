# EXP-GRAPH-35752541832 Report: C-DELTA-REPAIR Localized Repair — BLOCKED

**Experiment ID:** EXP-GRAPH-35752541832
**Lane:** graph
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally
**Status:** BLOCKED (infrastructure failure)
**Outcome:** NOT_APPLICABLE
**Freeze:** 2026-09-22T16:15:49.281519+00:00 (spec.json, prereg.md, freeze.json immutable)

---

## 1. Summary

This experiment was designed to execute the first real-substrate measurement of C-DELTA-REPAIR: testing whether a controlled single-resource local perturbation (DOM attribute/text change, endpoint param/header change, Cache-Control/ETag mutation) admits localized repair with bounded cost (<50% tokens and <40% browser vs cold re-exploration), verification AUROC≥0.75 and precision≥0.80, contamination <0.10, and amortized cost < cold at 10 reuses — **measured with a real LLM agent, real Playwright execution, and real verify() on actual DOM/response state** on a real nginx HIT/SWR/SIE/304 + Flask HS256 localhost substrate.

The experiment is **BLOCKED** due to missing LLM API infrastructure. No OpenAI API key (or equivalent) is available in the execution environment, making it impossible to satisfy the frozen measurement validity requirements mandating real LLM token counting and model calls.

---

## 2. Infrastructure Status

| Component | Status | Notes |
|-----------|--------|-------|
| nginx 1.24.0 | ✅ Available | `/usr/sbin/nginx` present |
| Playwright Chromium | ✅ Installed | `playwright install chromium` completed |
| Python packages | ✅ Available | `openai`, `playwright`, `flask`, `pyjwt`, `sklearn` installable |
| Flask + PyJWT HS256 backend | ❌ Not deployed | Requires testbed server implementation |
| nginx reverse proxy with proxy_cache | ❌ Not configured | Requires nginx.conf with HIT/SWR/SIE/304 cache stages |
| **LLM API key (OpenAI or equivalent)** | ❌ **MISSING — HARD BLOCKER** | Required for real token counting per `measurement_validity #4` |
| Real verify() on DOM/response | ❌ Not implemented | Requires Playwright + LLM pipeline |

---

## 3. Frozen Requirements Not Satisfied

The frozen `spec.json` and `prereg.md` mandate the following **real** (not simulated) measurements:

### Measurement Validity Requirements (spec.json § measurement_validity)
1. **Substrate provenance**: Real nginx 1.2x reverse-proxy with HIT/SWR/SIE/304 caching, Flask 3.1.3 + PyJWT HS256, oracle-free decompression — NOT SIMULATED
2. **Perturbation isolation**: Real DOM/response mutations on single resource, observed via Playwright accessibility tree and real HTTP fetches
3. **Registry snapshot isolation**: Deep clone, contamination measured via real verify() on N≥24 unrelated mechanisms
4. **Cost measurement transparency**: `tokens = sum(prompt_tokens + completion_tokens) from real LLM API responses (record model id, temperature, max_tokens, provider, per-call token counts)` — **REQUIRES API KEY**
5. **Verification validity**: Real verify() checking postconditions on actual DOM/response state, false accepts measured by independent oracle script
6. **Adequacy**: ≥48 perturbation instances (3 families × 2 variants × 8 seeds), family-stratified TRAIN/TEST split
7. **Determinism**: Fixed seeds via hashlib.sha256, real nginx/Playwright/LLM versions recorded
8. **Representation fidelity**: Full DOM snapshot + accessibility tree + response headers + decompressed body bytes + cache status header — NO HASH-ONLY SURROGATE

### Decision Rule Gates (spec.json § decision_rule)
- **C1**: PC1 success=1.0 and PC2 repair success ≥0.90 **on real pipeline**
- **C2**: NC1 patch cost 0, NC2 contamination=0, random-patch false-accept ≤5% with AUROC 0.4-0.6 **on real pipeline**
- **C3**: B-RUNTIME-BYTE-IDENTITY pre-perturbation byte identity ≥0.99 **on real nginx**
- **C4-C8**: Primary gates on **frozen pre-registered TEST data only** with real measurements

**Without a real LLM API, gates C1, C2, C4, C5, C7, C8 cannot be measured.** Gate C3 requires the nginx+Flask testbed which also cannot be fully exercised without the repair pipeline.

---

## 4. Relationship to Prior Work

This experiment is the **real-substrate remeasurement** of EXP-GRAPH-35741890679, which was a deterministic simulation (audit: `SIMULATION_NOT_MEASUREMENT`, `VERIFICATION_AUROC_ARTIFACTUALLY_PERFECT`, `CONTAMINATION_HARDCODED_NOT_MEASURED`, `AMORTIZATION_MATHEMATICAL_CONSEQUENCE`, `SUBSTRATE_SIMULATION_NOT_REAL_NGINX`).

The parent experiment's audit required fixes:
1. Replace simulated heuristic repair with actual LLM agent (real model calls, real token counting)
2. Execute actual browser interactions via Playwright
3. Implement real verification function on actual DOM/response state
4. Measure contamination from actual system behavior
5. Run on real nginx 1.2x with production gzip/chunked encoding
6. Increase per-family TEST sample size
7. Decouple verification threshold calibration from deterministic instance_id-based score generation

**None of these fixes can be implemented without an LLM API key.**

---

## 5. Validity Notes

- This is an **infrastructure failure**, not a scientific negative result.
- Per `EXPERIMENT_PACKET.md` §9: "Operational failure is not scientific falsification. A later retry must resume from the last valid checkpoint and must not rewrite frozen scientific inputs."
- Per `AGENTS.md`: "If a required substrate, model, dataset or tool is unavailable, write the exact failure and the smallest next action that could unblock it."
- The frozen `spec.json`, `prereg.md`, and `freeze.json` remain immutable and valid for retry.
- The claim C-DELTA-REPAIR remains `HYPOTHESIS` (per codex/claim_state.json) — untested on real substrate.

---

## 6. Smallest Next Action to Unblock

**Provide an LLM API key (OpenAI or equivalent) in the execution environment.**

With an API key, the remaining work would be:
1. Deploy nginx reverse proxy with `proxy_cache` configured for HIT/SWR/SIE/304 stages (using the validated configuration from EXP-RUNTIME-35611612543)
2. Deploy Flask 3.1.3 + PyJWT HS256 backend with perturbation endpoints
3. Implement the repair agent with real LLM calls, Playwright execution, and real verify()
4. Execute the 48-instance experiment per frozen design

---

## 7. Consequences

- **No scientific conclusion** about C-DELTA-REPAIR can be drawn from this run.
- The experiment packet correctly records `status=BLOCKED` and `outcome=NOT_APPLICABLE`.
- A retry with the same frozen design is required once infrastructure is available.
- This does not change the claim state (C-DELTA-REPAIR remains `HYPOTHESIS`).
- No promotion, rejection, or handoff decision is warranted.