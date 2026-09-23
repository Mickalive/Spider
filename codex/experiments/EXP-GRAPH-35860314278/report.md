# EXP-GRAPH-35860314278 Report: C-DELTA-REPAIR Localized Repair — BLOCKED

**Lane:** graph | **Claim:** C-DELTA-REPAIR | **Status:** BLOCKED | **Outcome:** NOT_APPLICABLE

---

## 1. Summary

This experiment was designed to execute the **first real-substrate measurement** of C-DELTA-REPAIR: testing whether a controlled single-resource local perturbation (DOM attribute/text change, endpoint param/header change, Cache-Control/ETag mutation) admits localized repair with bounded cost (<50% tokens and <40% browser vs cold re-exploration), verification AUROC≥0.75 and precision≥0.80, contamination <0.10, and amortized cost < cold at 10 reuses — **measured with a real LLM agent, real Playwright execution, and real verify() on actual DOM/response state** on a real nginx HIT/SWR/SIE/304 + Flask HS256 localhost substrate.

**Result: BLOCKED — an infrastructure failure prevents any outcome-bearing measurement.** This is **not a scientific negative result** and is not falsification of C-DELTA-REPAIR. The frozen design requires a real LLM agent (`gpt-4o-mini-2024-07-18` with real token billing), real Playwright execution, and real `verify()` on actual nginx+Flask state. None of these were available in the execution environment.

---

## 2. Infrastructure Failure Details

| Component | Required | Available | Status |
|-----------|----------|-----------|--------|
| OPENAI_API_KEY | Yes (gpt-4o-mini-2024-07-18) | No | ❌ MISSING |
| openai Python package | ≥1.0.0 | No (only pip installed) | ❌ MISSING |
| playwright Python package | ≥1.40.0 | No | ❌ MISSING |
| playwright chromium browser | Yes | No | ❌ MISSING |
| nginx binary | 1.2x | Yes (1.24.0) | ✅ PRESENT |
| nginx proxy_cache HIT/SWR/SIE/304 | Configured | No (not in nginx.conf) | ❌ MISSING |
| Flask HS256 testbed backend | Deployed on localhost | No | ❌ MISSING |
| Real repair agent | execute_delta_repair_real.py | Not implemented | ❌ MISSING |
| SpiderKernel importable | With dependencies | No (missing deps) | ❌ MISSING |

**Zero LLM calls, zero Playwright traces, zero verify() signals obtained.**

---

## 3. Frozen Design Preserved

Per `research/EXPERIMENT_PACKET.md` transmission invariants, the frozen design is immutable and preserved:

- **request.json** — Director mandate: PIVOT to C-DELTA-REPAIR, SUPERSEDE parent handoff, strategic question binding
- **spec.json** — 36 perturbation instances (3 families × 2 variants × 6 seeds), 5 baselines (B-COLD, B-RAG, B-REPLAY, B-ORACLE, B-BYTE-IDENTITY), positive/null controls, 8 measurement validity gates, frozen decision rule C1-C8
- **prereg.md** — Full preregistration with TRAIN/TEST split, trajectory-grouped bootstrap CIs, Wilson CIs, per-family thresholds
- **freeze.json** — Deterministic hashes proving pre-outcome freeze

**No simulation fallback executed.** Prior simulation-only experiment (EXP-GRAPH-35741890679) was correctly audited as SIMULATION_NOT_MEASUREMENT; this run correctly resists simulation per prereg §8/§13 and spec measurement_validity #4/#8.

---

## 4. Gates Unevaluable (C1–C8)

All frozen gates require real-substrate measurements:

| Gate | Requirement | Status |
|------|-------------|--------|
| **C1** | PC1 3/3 success, PC2 ≥90% (Wilson lower ≥70%) cost ratio <0.50 on real gpt-4o-mini | NOT_MEASURED |
| **C2** | NC1 cost=0, NC2 contamination=0, random-patch FA≤5% AUROC 0.45-0.55 trajectory-grouped | NOT_MEASURED |
| **C3** | B-BYTE-IDENTITY ≥0.99 via oracle-free gzip.decompress on real nginx | NOT_MEASURED |
| **C4** | Repair success ≥80% pooled AND ≥70% per-family on TEST (Wilson CIs) | NOT_MEASURED |
| **C5** | Token ratio <0.50, browser ratio <0.40, verif steps ≤2 on TEST (bootstrap upper bounds) | NOT_MEASURED |
| **C6** | Contamination <0.10 (Wilson upper <0.15) N≥24 unrelated | NOT_MEASURED |
| **C7** | Verification AUROC ≥0.75, precision ≥0.80 at TRAIN-calibrated threshold | NOT_MEASURED |
| **C8** | Amortized (repair+verify+10×retrieval)/10 < B-COLD on TEST (bootstrap upper <1.0) | NOT_MEASURED |

---

## 5. Claim Ceiling Unchanged

**C-DELTA-REPAIR remains `HYPOTHESIS` on real nginx HIT-cache localhost substrate with real LLM+Playwright+verify().**

The maximum justified ceiling remains exactly the **bounded simulation ceiling** from parent EXP-GRAPH-35741890679 (audit REVISE, SIMULATION_NOT_MEASUREMENT):
- Deterministic heuristic on 36 instances (3×2×6) showed:
  - Pooled repair success 0.833 CI [0.681, 0.921], TEST 0.944 CI [0.742, 0.990]
  - Token ratio 0.613 CI [0.569, 0.661] **failing <0.50**
  - Browser ratio 0.431 CI [0.396, 0.469] **failing <0.40**
  - Verification AUROC 1.0 **artefactual** (perfect separation by instance_id construction)
  - Contamination 0.0046 **hardcoded** to 2 events
  - Amortized 4744 vs cold 2226 → **2.1× failing**
- Audit explicitly limited that ceiling to **simulation parameters only** — no inference to real LLM economics.

**Do NOT assume:**
- That BLOCKED infrastructure failure constitutes scientific falsification — per EXPERIMENT_PACKET.md §9 operational failure is not falsification
- That C5/C8 failure in simulation falsifies C-DELTA-REPAIR generally — it falsifies only the cheapest single-resource simulation parameterization; real LLM with real DOM/a11y tree observation and real verify() may achieve thresholds
- That C-DELTA-REPAIR holds because C-FRESHNESS orthogonality holds (r~0.002-0.046) — orthogonal claims per prereg do_not_assume
- That synthetic 960/960 byte identity via gzip.decompress on strings validates runtime HIT-cache substrate for C-DELTA-REPAIR — synthetic gzip vs production nginx/CDN with Content-Encoding/chunked/Vary are distinct

---

## 6. Next Steps (Smallest Unblocking Actions)

Per AGENTS.md failure discipline: write the exact failure and the smallest next action that could unblock it.

1. **Provision OPENAI_API_KEY** in execution environment
2. **Install packages**: `pip install openai>=1.0.0 playwright>=1.40.0`
3. **Install browser**: `playwright install chromium`
4. **Deploy nginx reverse-proxy** with proxy_cache HIT/SWR/SIE/304 configuration (Cache-Control max-age, stale-while-revalidate, stale-if-error)
5. **Deploy Flask 3.1.3 + PyJWT 2.13.0 HS256 testbed backend** with endpoints for DOM/endpoint/cache perturbation families
6. **Implement execute_delta_repair_real.py** with:
   - Real LLM agent loop (gpt-4o-mini-2024-07-18, temp 0.0, seed 42, max 15 steps, 4096 tokens)
   - Real Playwright traces (goto, click, fill, evaluate, fetch)
   - Real verify() on actual DOM/response state via SpiderKernel
   - Trajectory-grouped bootstrap (5000 resamples, seed 42)
   - TRAIN24/TEST24 stratified split with manifest holdout
7. **Record provenance hashes**: nginx.conf, Flask testbed_server.py commit, decompression code, all versions
8. **Execute 48 instances** (3×2×8) per frozen spec and compute C1-C8 on TEST

When substrate is available: **resume from frozen design unchanged** (spec/prereg/freeze immutable per provenance retry_instructions do_not_modify). If C1-C3 PASS and C4-C8 all PASS on TEST → advance C-DELTA-REPAIR HYPOTHESIS→EXPERIMENTAL (VALIDATED candidate, localhost single-resource only, not Product Core). If any C4-C8 fails while C1-C3 PASS → mark bounded FALSIFIED-IN-SETTING for single-resource radius and pivot per product_consequence_negative.

---

## 7. Transmission Invariants Preserved

This BLOCKED packet carries stable identities for downstream AUDIT/DIRECTOR:

- `experiment_id`: EXP-GRAPH-35860314278
- `lane`: graph
- `claim_ids`: ["C-DELTA-REPAIR"]
- Frozen control identifiers (B-COLD, B-RAG, B-REPLAY, B-ORACLE, B-BYTE-IDENTITY, PC-LOCALIZED-REPAIR-SUCCEEDS, NC-ZERO-AND-DISTANT, C1-C8)
- Exact evidence paths in `artifacts` (raw_evidence/infrastructure_check.json, raw_evidence/infrastructure_failure.json)
- `status=BLOCKED` `outcome=NOT_APPLICABLE` — infrastructure failure correctly classified, not scientific negative
- `metrics={}` `controls={...observed=null, pass=null, evidence="NOT_MEASURED"}` — absent data not encoded as falsification

Downstream agents must read `research/EXPERIMENT_PACKET.md` transmission invariants: absent mandatory keys would be invalid packet; `null`/`{}`/`[]` used per contract with explanation in `validity_notes` and `unresolved`.

---

## 8. Director Mandate Honored

The Global Research Director (cycle 35859819467) performed a **PIVOT** with comparative reasoning explicitly in request.json:
- vs CONTINUE single-family WebArena pilot: repeats same pilot without substrate fix, requires distributed shared-store still missing, low marginal gain
- vs C-FRESHNESS file-census sweep: re-tests scalar orthogonality already falsified at FP=1.0
- vs C-DELTA-REPAIR localized repair: discriminating positive vs null with already-available nginx HIT substrate, trajectory-grouped CIs, honest token/browser cost — **highest marginal value**

This experiment correctly implemented the PIVOT design. The infrastructure failure is not a design flaw — it is the environment not meeting the frozen substrate requirements. The mandate's rationale remains valid; the measurement awaits substrate provisioning.