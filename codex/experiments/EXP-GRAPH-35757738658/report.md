# EXP-GRAPH-35757738658 Report: C-DELTA-REPAIR Localized Repair — BLOCKED

**Experiment ID:** EXP-GRAPH-35757738658  
**Lane:** graph  
**Claim:** C-DELTA-REPAIR — Local Web changes can be repaired locally  
**Status:** BLOCKED (infrastructure failure)  
**Outcome:** NOT_APPLICABLE  
**Frozen at:** 2026-09-22T17:03:45.607322+00:00 (freeze.json)  
**Director mandate:** PIVOT, cognitive_reset=true, target claim C-DELTA-REPAIR  

---

## 1. Executive Summary

This experiment was designed to execute the first real-substrate measurement of C-DELTA-REPAIR: testing whether a controlled single-resource local perturbation (DOM attribute/text change, endpoint param/header change, Cache-Control/ETag mutation) admits localized repair with bounded cost when measured with a **real LLM agent (gpt-4o-mini)**, **real Playwright execution**, and **real verify()** on actual DOM/response state on a real nginx HIT/SWR/SIE/304 + Flask HS256 localhost substrate.

**The experiment is BLOCKED** because no LLM API key is available in the execution environment. The frozen specification (measurement_validity #4, #8) mandates real LLM API calls with token counting (model id gpt-4o-mini, temperature 0.0, max_tokens, provider, per-call token counts, 15-step budget). This infrastructure requirement cannot be satisfied without an API key.

Per EXPERIMENT_PACKET.md §9 and AGENTS.md Failure discipline: this is an **operational failure, not a scientific falsification**. No scientific conclusion about C-DELTA-REPAIR can be drawn from this run. The claim C-DELTA-REPAIR remains `HYPOTHESIS` — untested on real substrate.

---

## 2. Infrastructure Status

| Component | Status | Details |
|-----------|--------|---------|
| **nginx** | ✅ Available | nginx/1.24.0 (Ubuntu) installed |
| **Playwright** | ✅ Available | 1.63.0, Chromium headless-shell installed |
| **Python** | ✅ Available | 3.12.14 |
| **Flask / PyJWT** | ⚠️ Installable | Not deployed; pip installable |
| **OpenAI API Key** | ❌ **MISSING** | `OPENAI_API_KEY` not set in environment — **HARD BLOCKER** |
| **openai Python SDK** | ✅ Available | 3.17.0 installed |

The missing LLM API key blocks all measurements requiring real model calls:
- B-COLD-FULL-REEXPLORATION (full task cost)
- B-RETRIEVAL-RAG (embedding + retrieval)
- PC-LOCALIZED-REPAIR-SUCCEEDS (PC2 oracle patch on real pipeline)
- NC-ZERO-AND-DISTANT-PERTURBATION (real pipeline calibration)
- C4 repair success rate
- C5 real token/browser cost ratios with trajectory-grouped bootstrap CIs
- C6 real contamination measurement
- C7 real verification AUROC/precision with TRAIN-calibrated threshold
- C8 real amortized cost economics

---

## 3. Relationship to Prior Work

| Experiment | Status | Key Finding |
|------------|--------|-------------|
| EXP-GRAPH-35741890679 | COMPLETE, FALSIFIES (simulation) | Deterministic heuristic simulation: token ratio 0.613 > 0.50, amortized 2.1× cold. Audit: SIMULATION_NOT_MEASUREMENT — ceiling bounded to simulation parameters only. |
| EXP-GRAPH-35752541832 | BLOCKED | Same frozen design as this experiment. Zero real measurements due to missing LLM API key. Correctly resisted simulation fallback. |
| EXP-RUNTIME-35611612543 | COMPLETE | Runtime verified byte-preserving nginx HIT/SWR/SIE/304 substrate: 960/960 byte-identical via oracle-free gzip.decompress. Dependency satisfied. |
| EXP-RUNTIME-35741906498 | COMPLETE | Header-only drift discrimination on localhost Flask+JWT: non-vacuous C4 (full > body/status). Unblocked C-FRESHNESS/C-DELTA-REPAIR for localhost testing. |

**Director mandate rationale (cycle 35757103830):** Global Research Director performed PIVOT with cognitive_reset=true. Graph had tunneled 13/17 recent on C-FRESHNESS (r~0.002–0.041, CI upper <0.15) with diminishing returns; distributed failure is infra session non-replication (TN 0.667), not science. C-DELTA-REPAIR has 0/235 valid real measurements yet runtime just delivered verified HIT substrate enabling this gate. This directly tests SPIDER's core compression promise "pay residual novelty not whole task" with end-to-end LLM+Playwright economics.

---

## 4. Frozen Design Compliance

The frozen design (spec.json, prereg.md, freeze.json) is **immutable and hash-verified**:

- `request.json` sha256: `f8f5e93e67c4b9ef3d764198c69d8ae4a9989c4c9dd6fdba852f0ca4606bc9d8`
- `spec.json` sha256: `2657ca935665f17867759544bcbef08386116872247caec0b2a95707ef446304`
- `prereg.md` sha256: `330247b2acb7abcba979ec9d21a10571472d2ec09bb8c06749e64b99d9c033f0`
- `freeze.json` records these hashes at `frozen_at: 2026-09-22T17:03:45.607322+00:00`

No post-freeze mutation occurred. The experiment correctly resisted any simulation fallback (hardcoded COLD_TOKENS_BASE 2250, retrieval 320, verify 180, heuristic 1364, AUROC 1.0 perfect-separation removed per spec).

---

## 5. Gates Status (Frozen Decision Rule)

| Gate | Description | Status | Evidence |
|------|-------------|--------|----------|
| **C1** | PC1 1.0 & PC2 ≥0.90 on real pipeline | NOT_MEASURED | Requires real LLM + Playwright |
| **C2** | NC1 cost0, NC2 cont0, rand FA≤5% AUROC 0.4–0.6 | NOT_MEASURED | Requires real pipeline + block-permutation |
| **C3** | Byte identity ≥0.99 on real nginx | NOT_MEASURED | Requires nginx+Flask deployment |
| **C4** | Repair success ≥0.80 pooled, ≥0.70/family TEST | NOT_MEASURED | Requires real LLM repair |
| **C5** | Token ratio <0.50, browser ratio <0.40, verif≤2 TEST | NOT_MEASURED | Requires real token/browser costs |
| **C6** | Contamination <0.10 TEST | NOT_MEASURED | Requires real registry + verify() |
| **C7** | AUROC ≥0.75, precision ≥0.80 TEST | NOT_MEASURED | Requires real verify() + TRAIN threshold |
| **C8** | Amortized (repair+verif+10×retrieval) < cold TEST | NOT_MEASURED | Requires real retrieval/repair costs |

**Decision rule:** If C1–C3 fail → MEASUREMENT_INVALID. If C1–C3 PASS and any C4–C8 fails → FALSIFIES-IN-SETTING. If C1–C8 all PASS → CONFIRMED. If family-heterogeneous → MIXED. **Cannot be evaluated without real measurements.**

---

## 6. Smallest Next Action to Unblock

1. **Provide `OPENAI_API_KEY`** environment variable for gpt-4o-mini access
2. **Deploy nginx reverse proxy** with `proxy_cache` configured for HIT/SWR/SIE/304 stages matching EXP-RUNTIME-35611612543 substrate
3. **Deploy Flask 3.1.3 + PyJWT HS256 + SQLite** backend with perturbation endpoints
4. **Implement `execute_delta_repair_real.py`** with:
   - Real LLM calls (record model id, temperature, max_tokens, provider, per-call tokens)
   - Real Playwright execution (goto/click/fill/evaluate/fetch with trace logs)
   - Real `verify()` on actual DOM/response (Playwright evaluate for selectors, fetch for headers/body)
   - Independent oracle script for false-accept detection (ground-truth from perturbation manifest)
5. **Run 48 instances** (3 families × 2 variants × 8 seeds) with TRAIN24/TEST24 stratified split
6. **Compute metrics** and apply frozen C1–C8 on TEST data with trajectory-grouped uncertainty

Resume from frozen design unchanged (spec/prereg/freeze immutable per provenance `retry_instructions.do_not_modify`).

---

## 7. Validity Notes

- **INFRASTRUCTURE_FAILURE**: No LLM API key. Frozen spec mandates real token counting from API responses.
- **No simulation fallback**: Hardcoded parameters (COLD_TOKENS_BASE 2250, retrieval 320, etc.) were removed per spec; this run correctly produces zero measurements rather than synthetic ones.
- **Frozen integrity preserved**: All input hashes match freeze.json. No threshold weakening, no post-freeze mutation.
- **Claim ceiling unchanged**: Maximum justified ceiling remains the bounded simulation ceiling from EXP-GRAPH-35741890679 (audit REVISE, SIMULATION_NOT_MEASUREMENT). C-DELTA-REPAIR remains HYPOTHESIS on real substrate.
- **Per EXPERIMENT_PACKET.md §9**: Operational failure ≠ scientific falsification. Later retry must resume from last valid checkpoint without rewriting frozen inputs.

---

## 8. Unresolved Questions (Carried Forward)

1. Whether a real LLM agent achieves repair token cost <50% cold and browser <40% cold on F-DOM/F-ENDPOINT/F-CACHE single-resource perturbations with real token billing and Playwright execution (C5 gate)
2. Whether real verification on actual DOM/response discriminates correct vs incorrect patch with AUROC≥0.75 and precision≥0.80 at TRAIN-calibrated threshold without perfect-separation artefact (C7 gate)
3. Whether contamination remains <0.10 and random-patch false_accept <5% when measured on real registry with N≥24 unrelated mechanisms via real verify() and block-permutation (C6/C2 gates)
4. Whether amortized cost at 10 reuses (repair+verification+10×retrieval) < B-COLD cost holds with real retrieval costs and trajectory-grouped CIs (C8 gate)
5. Whether nginx HIT/SWR/SIE/304 byte identity ≥0.99 holds on real nginx 1.2x with production gzip/chunked/Vary via oracle-free greedy decode (C3 gate)
6. Whether per-family cost heterogeneity exists at adequate TEST n=8 per family and whether 2-3 resource radius, cross-page, distributed Redis, or production CDN change repair economics
7. Whether residual-novelty amortization and verification generalize to production DOM where controller/oracle disagree on functional correctness

These unknowns are preserved exactly from the parent handoff (EXP-GRAPH-35752541832) and the frozen preregistration.

---

## 9. Artifacts

No durable artifacts produced beyond this canonical packet (result.json, report.md, provenance.json). Raw evidence directory exists but contains no measurements due to infrastructure blocker.

---

*This report is the human-readable explanation of the canonical result.json. The JSON packet is the authoritative handoff for downstream agents.*
