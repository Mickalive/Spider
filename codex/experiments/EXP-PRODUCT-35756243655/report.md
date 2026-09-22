# EXP-PRODUCT-35756243655 — Execution Report

## Status: MEASUREMENT_INVALID

**Experiment**: EXP-PRODUCT-35756243655  
**Lane**: product  
**Claim**: C-PARAM-INHERIT  
**Director mandate**: REOPEN C-PARAM-INHERIT  
**Date**: 2026-09-22  

---

## 1. Executive Summary

This experiment was designed to test whether a committed kernel-integrated `distill_parameterized()` (fixing `_common_prefix_and_suffix` double-prefix handling) enables a real LLM agent on WebArena-Verified v2 family hold-out to achieve EXECUTABLE >=0.75 and binding correctness >=0.90 with zero unsubstituted templates, beating B-COLD/B-RAG/B-REPLAY/B-INSTR by >=0.12 success margin with honest amortized economics.

**The experiment could not be executed.** Three critical substrates were unavailable:

1. **Kernel fix not committed**: `src/spider/kernel.py` (sha256 `46929b3a...`) contains only the base `SpiderKernel` class with `distill()`, `resolve()`, `verify()`, `invalidate()`. It does NOT contain `distill_parameterized()`, `_common_prefix_and_suffix()`, `_extract_varying_values()`, or `_field_path_to_slot_name()` as required by spec.json and prereg.md §3.

2. **LLM API unavailable**: No `OPENAI_API_KEY` in the environment. The `openai` Python package (3.17.0) is installed but cannot make API calls. Previous execution attempts (4 retries, exit_code 124) all timed out.

3. **Nginx HIT-cache substrate unavailable**: nginx is installed but inactive. No DOM/response provenance for `_matches` postcondition verification.

Per the frozen spec's MEASUREMENT_INVALID criteria, this is **not a scientific falsification**. The C-PARAM-INHERIT question remains open.

---

## 2. Raw Evidence (separate from interpretation)

### 2.1 Kernel code state
- `src/spider/kernel.py` (132 lines): Contains `SpiderKernel` class with `observe()`, `distill()`, `resolve()`, `verify()`, `invalidate()` methods only.
- `_bind()` and `_template_slots()` and `_matches()` helper functions exist but are the base implementations, not the corrected parameterized versions.
- No `distill_parameterized()`, `_common_prefix_and_suffix()`, `_extract_varying_values()`, `_field_path_to_slot_name()` anywhere in `src/spider/`.

### 2.2 LLM API status
- Environment: no `OPENAI_API_KEY`, no alternative LLM credentials
- `openai` package 3.17.0 installed
- 4 previous execution attempts timed out (exit_code 124) on model `opencode/big-pickle`
- Per spec measurement_validity #1: "LLM_API_available logged; >50% failures → MEASUREMENT_INVALID"

### 2.3 WebArena data
- `/tmp/opencode/webarena-verified.json`: 812 tasks, 190 templates, 12 site families
- This is **raw data**, not the Intel-validated v2 family-stratified version:
  - Missing measured duplication 0.9479 (hardcoded or unmeasured)
  - Missing AX 0.9 longest-prefix mapping proof on 20 CDP trees
  - Missing explicit family A/B disjoint pools with verified zero value overlap
  - Missing the 49-template structure with per-family parameterization

### 2.4 Nginx status
- `/usr/sbin/nginx` exists but systemctl status: **inactive (dead)**
- No HIT/SWR/SIE/304 discrimination possible
- No provenance layer for `_matches` postcondition verification

### 2.5 Previous execution history
- `model_execute.json`: 4 retry attempts, all exit_code 124 (timeout), category "transient"
- `execution_checkpoint.json`: Pre-execute sha `325f6c14cd976e0512c9d30e2dd186201fc8155e`, recorded at 2026-09-22T16:50:47

---

## 3. Derived Measurements

No outcome-bearing measurements were performed. All metrics are infrastructure diagnostics:

| Metric | Value | Meaning |
|--------|-------|---------|
| M-LLM-AVAILABLE | false | No API credentials |
| M-KERNEL-FIX-COMMITTED | false | distill_parameterized absent |
| M-WEBARENA-LOADED | partial | Raw data only, not validated v2 |
| M-NGINX-HIT-CACHE-AVAILABLE | false | nginx inactive |
| M-PLAYWRIGHT-BROWSERS-AVAILABLE | false | No browsers configured |
| M-PREVIOUS-EXECUTION-ATTEMPTS | 4 | All timed out |

---

## 4. Interpretation

Per the frozen spec and AGENTS.md failure discipline:

- **Infrastructure failure ≠ scientific falsification**. The experiment status is MEASUREMENT_INVALID, not FALSIFIED.
- The C-PARAM-INHERIT claim remains EXPERIMENTAL at its prior synthetic ceiling (EXP-PRODUCT-33528829801 single-param POC 5.42%, EXP-PRODUCT-33741671686 harness-only 21/21).
- The double-prefix bug in `_common_prefix_and_suffix` identified in parent handoff (EXP-PRODUCT-35752564139) remains unaddressed in the committed kernel.
- Per spec falsifier: "kernel fix not committed to src/spider/kernel.py → MEASUREMENT_INVALID (not falsification)".

### What this does NOT tell us:
- Whether parameterized inheritance works on real LLM+Playwright
- Whether the corrected kernel fix would achieve EXECUTABLE >=0.75
- Whether SPIDER beats COLD/RAG/REPLAY on held-out B
- Whether amortized economics achieve >=25% saving vs COLD

### What this DOES tell us:
- The substrate repair required by the Director's REOPEN mandate has not been completed
- The kernel fix must be committed before any valid execution
- LLM API access is a prerequisite for product-level evidence

---

## 5. Validity Threats

| # | Threat | Status |
|---|--------|--------|
| 1 | Kernel fix not committed | **TRIGGERED** — MEASUREMENT_INVALID criterion 1 |
| 2 | LLM API unavailable | **TRIGGERED** — MEASUREMENT_INVALID criterion 2 |
| 3 | WebArena validated v2 not loaded | **TRIGGERED** — MEASUREMENT_INVALID criterion 3 |
| 4 | Nginx provenance unavailable | **TRIGGERED** — Verification substrate missing |
| 5 | Previous timeout failures | **TRIGGERED** — 4 retries, transient category |
| 6 | Playwright browsers unconfigured | **TRIGGERED** — Browser execution impossible |

---

## 6. Smallest Next Action

To unblock this experiment:

1. **Obtain LLM API credentials** (OPENAI_API_KEY or equivalent for gpt-4o-mini-2024-07-18) — highest priority, enables all agent execution
2. **Commit `distill_parameterized()` with `_common_prefix_and_suffix`, `_extract_varying_values`, `_field_path_to_slot_name` to `src/spider/kernel.py`** — audit import+hash verification required
3. **Start nginx for HIT-cache provenance** — enables `_matches` verification on actual DOM/response
4. **Configure Playwright browsers** — enables browser execution
5. **Validate Intel WebArena-Verified v2 family-stratified data** with measured duplication 0.9479 and AX 0.9 mapping

Without (1) and (2), the experiment cannot produce valid scientific evidence regardless of other repairs.

---

## 7. Consequences

### If substrates become available and experiment re-executes:
- **SURVIVES**: C-PARAM-INHERIT advances EXPERIMENTAL → VALIDATED; unblocks C-LLM-INHERIT and C-PRODUCT-ECON
- **FALSIFIED/MIXED**: C-PARAM-INHERIT remains EXPERIMENTAL at narrow synthetic ceiling; Product redirects to C-FRESHNESS/C-DELTA-REPAIR/C-SEMANTIC-RESOLVE
- **MEASUREMENT_INVALID again**: Priority is fixing the specific substrate that failed

### Current state:
- C-PARAM-INHERIT remains EXPERIMENTAL (unchanged)
- No product promotion authorized
- No further claim updates until substrate repaired and valid measurement obtained
- Parent handoff carry_forward distinctions preserved (established/rejected/unknown/do_not_assume)

---

## 8. References

- `research/experiments/EXP-PRODUCT-35756243655/freeze.json` — frozen hashes
- `research/experiments/EXP-PRODUCT-35756243655/request.json` — Director mandate REOPEN C-PARAM-INHERIT
- `research/experiments/EXP-PRODUCT-35756243655/spec.json` — frozen experiment design
- `research/experiments/EXP-PRODUCT-35756243655/prereg.md` — frozen preregistration
- `research/experiments/EXP-PRODUCT-35752564139/handoff.json` — parent handoff (MEASUREMENT_INVALID)
- `src/spider/kernel.py` — base kernel (sha256 `46929b3a...`), fix not committed
- `/tmp/opencode/webarena-verified.json` — raw WebArena data (812 tasks, not validated v2)
- `codex/index.json` — prior experiment evidence (EXP-PRODUCT-33528829801, EXP-PRODUCT-33741671686, etc.)
- `codex/claim_state.json` — C-PARAM-INHERIT claim state history
- AGENTS.md §Failure discipline: "infrastructure failure is not a scientific negative"
- EXPERIMENT_PACKET.md §9: "Failure transmission" — MEASUREMENT_INVALID not falsification
