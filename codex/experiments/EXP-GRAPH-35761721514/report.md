# EXP-GRAPH-35761721514 — C-DELTA-REPAIR Localized Repair (REOPEN)

**Lane:** graph | **Claim:** C-DELTA-REPAIR | **Status:** BLOCKED | **Outcome:** NOT_APPLICABLE  
**Experiment ID:** EXP-GRAPH-35761721514 | **GitHub Run:** 35761721514 | **Commit:** 3835093717705577f43a7a7a5ee1531f014017a7

## Summary

This experiment is **BLOCKED** — an infrastructure failure prevents any outcome-bearing measurement. This is **not a scientific negative result** and is not falsification of C-DELTA-REPAIR. The frozen design (REOPEN after runtime's verified byte-preserving nginx HIT-cache substrate) requires a real LLM agent (`gpt-4o-mini` with real token billing), real Playwright execution, and real `verify()` on actual DOM/response state. No LLM API key was available in the execution environment, and the `openai` and `playwright` SDKs are not installed. Correctly resisted simulation fallback with hardcoded costs (per prereg §8/§13, spec measurement_validity #4/#8).

No new scientific evidence was added. C-DELTA-REPAIR remains HYPOTHESIS on the real nginx HIT-cache localhost substrate, bounded above only by the prior simulation ceiling (EXP-GRAPH-35741890679, 36 instances, token ratio 0.613 CI [0.569,0.661] failing <0.50, amortized 2.1× cold, audit SIMULATION_NOT_MEASUREMENT).

## Question (frozen)

After runtime's verified byte-preserving nginx HIT-cache substrate (960/960 byte-identical across HIT/SWR/SIE/304 with oracle-free greedy decode EXP-RUNTIME-35611612543), does a controlled single-resource local perturbation (DOM attribute/text change, endpoint param/header change, Cache-Control/ETag mutation — one resource only) require only localized repair when measured with a real LLM agent (`gpt-4o-mini` same model/tools/budget 15 steps Playwright) and real `verify()` on actual DOM/response state: repair tokens <50% and browser interactions <40% vs cold re-exploration, verification AUROC≥0.75 and precision≥0.80, contamination<0.10, and amortized cost < cold at 10 reuses (retrieval+verification+repair amortized) vs COLD and retrieval baselines with trajectory-grouped CIs?

## Hypothesis (frozen)

C-DELTA-REPAIR (real-substrate remeasurement, REOPEN): a single-resource local perturbation is repairable by a localized patch (re-target selector, rebind param slot, update header expectation, refresh cache key) without full-task re-exploration when measured with real LLM `gpt-4o-mini` and real Playwright with real `verify()` on actual nginx+Flask state. Operational predictions on held-out TEST (24 TRAIN / 24 TEST from 48 instances: 3 families F-DOM/F-ENDPOINT/F-CACHE ×2 variants ×8 seeds): (1) success ≥80% pooled and ≥70% per-family; (2) mean repair tokens <0.50× cold and browser <0.40× cold and verification steps ≤2; (3) AUROC ≥0.75 and precision ≥0.80; (4) contamination <0.10 and random-patch false-accept <5%; (5) amortized cost at n=10 < cold.

## Method (frozen, not executed)

- **Families:** F-DOM (D1 attribute `#submit-123→#submit-124`, D2 text `Submit→Send`), F-ENDPOINT (E1 param `?id=→?item=`, E2 header `X-Request-Id→X-Req-Id`), F-CACHE (C1 `max-age 60→3600`, C2 ETag mutation)
- **Instances:** 48 total (3×2×8 seeds), family-stratified TRAIN24/TEST24 (TRAIN seeds 0–3, TEST 4–7 per variant), N≥24 unrelated mechanisms for contamination
- **Substrate:** nginx 1.2x reverse-proxy with HIT/SWR/SIE/304 caching (Cache-Control max-age, stale-while-revalidate, stale-if-error), Flask 3.1.3 + PyJWT HS256 + SQLite, Content-Encoding gzip where applicable, oracle-free `gzip.decompress` without oracle lookup
- **Costs:** real `openai` API usage `prompt_tokens + completion_tokens` per call (record model id `gpt-4o-mini`, temperature 0.0, max_tokens, 15-step budget) and Playwright action counts (goto/click/fill/evaluate/fetch) with trace logs
- **Verification:** `verify(mechanism_id, observed_state)` on actual DOM/response via Playwright evaluate + response header/body match; threshold fit on TRAIN only, evaluated on TEST; false accepts checked by independent oracle from manifest (held out from agent)
- **Baselines:** B-COLD (full re-exploration), B-VERBATIM (0-token replay, must fail <10%), B-RETRIEVAL-RAG (20–40% expected, block-permutation null), B-ORACLE (1 probe +1 verify ceiling), B-RUNTIME-BYTE-IDENTITY (≥0.99 byte identity pre-perturbation, non-vacuous full>body and full>status per agent prior #5), PC-LOCALIZED (PC1 1.0, PC2 ≥0.90), NC-ZERO-AND-DISTANT (NC1 cost 0, NC2 cont 0, random AUROC 0.4–0.6 FA ≤5%)
- **Statistics:** Wilson 95% CI by instance for rates, instance-block bootstrap 2000 resamples for cost ratios, block-permutation for retrieval/verification nulls, trajectory-grouped by instance/trajectory block (not transition), resampling unit = instance block

## Infrastructure Status (RAW EVIDENCE)

- `OPENAI_API_KEY`: **absent** (checked `env | grep OPENAI`, not set; no Anthropic/Mimo key either)
- `openai` SDK: **not installed** (`pip show openai` → not found)
- `playwright` SDK: **not installed** (`pip show playwright` → not found)
- `nginx`: **1.24.0 (Ubuntu)** binary present (`nginx -v` → 1.24.0) but `proxy_cache` HIT/SWR/SIE/304 not configured
- `Python`: **3.12.14**
- `gzip` stdlib sanity: `gzip.decompress(gzip.compress(b"test"))==b"test"` → **True** (oracle-free path exists but not on real nginx responses)
- `Flask`/`PyJWT`: not installed, installable via pip, not deployed
- Frozen hash verification: `request.json 77f7db7a`, `spec.json 01c99c55`, `prereg.md 59522090`, `freeze.json 04c744e8` — all match `freeze.json` hashes, no post-freeze mutation
- Git commit: `3835093717705577f43a7a7a5ee1531f014017a7`, branch `main`

## Results (NONE MEASURED)

All gates **NOT_MEASURED**:

| Gate | Threshold | Observed | Pass |
|------|-----------|----------|------|
| C1 PC | PC1 1.0 and PC2 ≥0.90, B-RUNTIME non-vacuous full>body | null | null |
| C2 NC | NC1 cost 0, NC2 cont 0, random FA ≤5% AUROC 0.4–0.6 | null | null |
| C3 BYTE | byte identity ≥0.99 pre-perturbation (oracle-free) | null | null |
| C4 SUCCESS | repair success ≥0.80 pooled and ≥0.70 per-family on TEST | null | null |
| C5 COST | tokens <0.50× cold, browser <0.40× cold, verif ≤2 on TEST | null | null |
| C6 CONTAM | contamination <0.10 | null | null |
| C7 VERIF | AUROC ≥0.75 and precision ≥0.80 at TRAIN threshold on TEST | null | null |
| C8 AMORT | amortized (repair+verif+10×retrieval) < cold at n=10 | null | null |

No baseline was executed:
- B-COLD: NOT_MEASURED (requires LLM)
- B-VERBATIM: NOT_MEASURED (requires Playwright on perturbed substrate)
- B-RETRIEVAL-RAG: NOT_MEASURED (requires embedding API + LLM)
- B-ORACLE: NOT_MEASURED (requires Playwright)
- B-RUNTIME-BYTE-IDENTITY: NOT_MEASURED (requires nginx+Flask deployment; synthetic gzip sanity True is not real nginx measurement)

## Observations vs Measurements vs Interpretation

- **RAW EVIDENCE:** `env` shows no `OPENAI_API_KEY`, `nginx -v` 1.24.0, `python3 --version` 3.12.14, `pip show openai/playwright` not found, `sha256sum` of frozen files matches freeze.json, `gzip.decompress` sanity True, `git rev-parse HEAD` 3835093.
- **OBSERVATION:** Execution environment lacks the LLM substrate required by measurement_validity #4/#8. No perturbation instance was generated or executed; no LLM call, browser trace, or verify() signal exists.
- **DERIVED MEASUREMENT:** None — `result.json` metrics `{}` correctly reflects no measurement rather than a zero/false-negative result.
- **INTERPRETATION:** This BLOCKED status must not be read as FALSIFIES or MEASUREMENT_INVALID on C-DELTA-REPAIR. It is parity with parent EXP-GRAPH-35757738658 (also BLOCKED MISSING_LLM_API_KEY, audit V_BLOCKED_CORRECTLY_CLASSIFIED). No claim ceiling change is justified.

## Validity Notes

1. **MISSING_LLM_API_KEY:** Hard blocker per spec measurement_validity #4 — tokens must be `sum(prompt_tokens + completion_tokens)` from real API usage with recorded model id/temperature/max_tokens/provider/per-call tokens/15-step enforcement. Absent.
2. **SDKs not installed:** `openai` and `playwright` not found in `pip list` (Python 3.12.14). Installation step `pip install openai playwright && playwright install chromium` required before retry.
3. **nginx proxy_cache not configured:** Binary present (1.24.0) with correct build flags (`--with-http_gzip_static_module`, `--with-http_gunzip_module` etc.) but no `proxy_cache` config for HIT/SWR/SIE/304, no Flask backend deployed. B-RUNTIME-BYTE-IDENTITY therefore unmeasured on real nginx.
4. **Resisted simulation:** Per prereg §8/§13 and spec, hardcoded constants (`COLD_TOKENS_BASE 2250`, `retrieval 320`, `verify 180`, heuristic 1364) remain forbidden. No simulation fallback executed; this preserves the distinction between this BLOCKED run and the prior simulation run EXP-GRAPH-35741890679 (which measured token ratio 0.613 and was correctly flagged SIMULATION_NOT_MEASUREMENT).
5. **Frozen integrity:** Hashes verified; no post-freeze mutation. `report.md` interpretation does not contradict `result.json` (both BLOCKED/NOT_APPLICABLE).
6. **Claim ceiling unchanged:** Remains bounded by EXP-GRAPH-35741890679 simulation (REVISE, token 0.613 failing <0.50, browser 0.431 failing <0.40, amortized 2.1×, contamination 0.0046, AUROC 1.0 artefactual perfect separation) with ceiling explicitly limited to simulation parameters only per audit.

## Unresolved (carry-forward)

All 7 unknowns from handoff remain open:
1. Real LLM repair cost (<50% tokens, <40% browser) on F-DOM/F-ENDPOINT/F-CACHE
2. Real verification discrimination (AUROC≥0.75, precision≥0.80) trajectory-grouped
3. Contamination <0.10 and random-patch FA<5% on real registry N≥24 block-permutation
4. Amortized cost at 10 reuses < cold with real retrieval costs trajectory-grouped
5. nginx HIT/SWR/SIE/304 byte identity ≥0.99 on real nginx with non-vacuous full>body>status
6. Per-family heterogeneity at TEST n=8 (Wilson half-width ±0.26 exploratory) and upgrade to 72 instances
7. B-VERBATIM (~0% expected) and B-RETRIEVAL (20–40%) replication with block-permutation sanity

Plus smallest next action: provide `OPENAI_API_KEY`, install SDKs, deploy substrate, implement `execute_delta_repair_real.py`, run 48 instances with manifest holdout and TRAIN/TEST split, compute trajectory-grouped metrics and apply C1–C8 exactly on TEST.

## Product Consequence

**None yet** — cannot advance C-DELTA-REPAIR HYPOTHESIS→EXPERIMENTAL nor mark FALSIFIED-IN-SETTING until a valid measurement exists. If future C1–C3 PASS and C4–C8 all PASS on real gpt-4o-mini + Playwright + verify with trajectory-grouped CIs and non-vacuous substrate, then advances to EXPERIMENTAL (VALIDATED candidate, localhost single-resource only, not Product Core). If any C4–C8 fails while C1–C3 PASS, then locality fails even at smallest radius → product must default to full re-exploration, budget repair≈cold, favor UNKNOWN/abstain when verification not discriminating, and pivot Graph to C-RESIDUAL-NOVELTY or C-SEMANTIC-RESOLVE per Director comparative reasoning.

## Evidence Preservation

- Raw evidence is environment checks and hash verification, not simulation synthesis — preserved as observations in `result.json` (not hashed as derived measurements).
- No `raw_evidence/experiment_data.json` generated because no perturbation instance was executed (artifacts `[]` is valid with explanation in `validity_notes`).
- Downstream agents must read `research/EXPERIMENT_PACKET.md` transmission invariants: this BLOCKED packet carries `experiment_id`, `lane`, frozen claim ids (`C-DELTA-REPAIR`), control identifiers, and evidence paths exactly for audit reuse.

---
*Generated by EXECUTE lane graph, model muse-spark-1.2-contributor-free, frozen design immutable.*
