# EXP-GRAPH-35764315683 Report: C-DELTA-REPAIR Localized Repair — INFRASTRUCTURE BLOCKER

## Status
**MEASUREMENT_INVALID** — Infrastructure failure, not scientific falsification.

## Infrastructure Blocker
**Missing OPENAI_API_KEY** — The frozen design (spec.json, prereg.md, freeze.json) requires real gpt-4o-mini LLM agent with real token billing, real Playwright browser execution, and real verify() on actual DOM/response state. Without the API key, the following gates cannot be measured:

- **C1 (Positive Controls):** PC1 unperturbed 100% and PC2 oracle patch ≥90% success on REAL gpt-4o-mini pipeline
- **C2 (Null Controls):** NC1 zero-perturbation cost=0 contamination=0, NC2 distant perturbation, random-patch block-permutation false-accept ≤5% AUROC 0.4-0.6 on REAL verify()
- **C3 (Byte Identity):** ≥0.99 SHA256(decompressed_body) identity HIT/SWR/SIE/304 on REAL nginx with oracle-free gzip.decompress (substrate not deployed)
- **C4-C8 (Primary Gates):** All require real cost measurements (tokens from OpenAI API, browser interactions from Playwright traces, verification steps, amortized economics at n=10 reuses)

## Available Infrastructure
- nginx 1.24.0 binary: ✅ Available
- Python 3.12.14: ✅ Available  
- openai SDK 3.18.0: ✅ Installed
- playwright SDK 1.63.0 (Chromium): ✅ Installed
- flask 3.1.3: ✅ Installed
- pyjwt 2.14.0: ✅ Installed
- gzip stdlib oracle-free decompression: ✅ Available

## Missing Infrastructure (Required for Real Measurement)
- OPENAI_API_KEY environment variable: ❌ **ABSENT** (hard blocker)
- nginx proxy_cache configured for HIT/SWR/SIE/304 stages: ❌ Not deployed
- Flask 3.1.3 + PyJWT HS256 + SQLite backend: ❌ Not deployed
- Real repair agent pipeline (execute_delta_repair_real.py): ❌ Not implemented
- Real verify() on actual DOM/response state with independent oracle: ❌ Not implemented
- Playwright trace logging for browser interaction counting: ❌ Not implemented

## Experimental Design (Frozen, Ready for Execution When Unblocked)
- **48 perturbation instances**: 3 families (F-DOM, F-ENDPOINT, F-CACHE) × 2 variants × 8 seeds
- **TRAIN/TEST split**: 24/24 stratified (seeds 0-3 TRAIN, 4-7 TEST per variant)
- **Unrelated mechanisms**: N≥24 for contamination measurement
- **Perturbation isolation**: Single resource per instance, blast_radius=1, registry clone isolation
- **Threshold calibration**: Verification operating threshold fit on TRAIN only, evaluated on TEST
- **Trajectory-grouped statistics**: Wilson CIs for rates, instance-block bootstrap (2000) for cost ratios, block-permutation for nulls
- **Non-vacuous substrate**: Full>body>status discrimination when headers/body vary independently

## Decision Rule (Frozen)
Per spec decision_rule and prereg §8:
- C1-C3 PASS required for measurement validity (else MEASUREMENT_INVALID)
- C4-C8 ALL PASS on TEST required for CONFIRMED
- Any C4-C8 FAIL while C1-C3 PASS → FALSIFIED-IN-SETTING (valid negative)
- Family-heterogeneous (≥1 family passes, another fails) → MIXED

## Smallest Unblock Action
```bash
export OPENAI_API_KEY="sk-..."  # Valid OpenAI key for gpt-4o-mini
# Then deploy nginx proxy_cache + Flask backend
# Then implement execute_delta_repair_real.py with real OpenAI + Playwright
# Then re-run EXECUTE from frozen design (spec/prereg/freeze immutable)
```

## Validity Notes
- This is an **infrastructure failure**, not a scientific result. Per EXPERIMENT_PACKET.md §9: "Operational failure is not scientific falsification."
- The parent experiment EXP-GRAPH-35761721514 had identical blocker (BLOCKED, MISSING_LLM_API_KEY).
- Simulation experiment EXP-GRAPH-35741890679 produced MEASUREMENT_INVALID (simulation-only, token ratio 0.613 falsified as parameter artifact).
- C-DELTA-REPAIR remains HYPOTHESIS/BLOCKED with zero valid real measurements across 239 canonical experiments.
- No claim ceiling change justified — zero evidence for or against localized repair on real substrate.

## Artifacts
- Frozen inputs: request.json, spec.json, prereg.md, freeze.json (hashes in provenance.json)
- Generated instances manifest: 48 perturbation instances with deterministic seeds
- No raw evidence collected (measurement not executed)
