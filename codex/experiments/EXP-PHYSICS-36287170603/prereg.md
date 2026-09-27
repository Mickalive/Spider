# Preregistration: EXP-PHYSICS-36287170603

## Intervention-Validity Contract (IVC) for Estimator Certification

**Experiment ID:** EXP-PHYSICS-36287170603
**Lane:** physics
**Claim:** C-MEAS-VALID (Measurement substrate is intervention-valid)
**Status:** PREREGISTERED — frozen before any outcome inspection

---

## 1. Scientific Question and Hypothesis

**Question:** Can a reusable, pre-registered intervention-validity contract — a validity test whose null calibration has demonstrated power against the specific failure it must detect, and which is itself validated as a classifier over a preregistered battery of known-good and known-bad statistics including at least the three SPIDER estimators the Codex records as non-discriminating — correctly reject every known-bad case and accept every known-good case, with each case run through the identical code path on real locally-served multi-page HTTP data carrying a server-side ground-truth transition log?

**Hypothesis:** A metamorphic intervention-validity contract (representation-sensitivity test + channel-displacement test) executed on a validated plain-HTTP substrate with server-side ground truth will correctly classify the three documented non-discriminating estimators as INVALID (reject) and at least one validated discrimination estimator as VALID (accept), thereby providing a reusable instrument-certification gate that converts instrument-blindness from a post-hoc discovery into a pre-registered detectable event.

**Falsifier:** The contract fails to reject any of the three known-bad estimators, OR incorrectly rejects a known-good estimator, OR the null calibration of the contract itself lacks demonstrated power (minimum attainable permutation p >= 0.01 on any known-bad case), OR the contract cannot be executed on the identical code path for all test cases, OR the substrate fails to provide server-side ground-truth transition logs for verification.

---

## 2. Director Mandate Context

This experiment is governed by a **Global Research Director mandate** (request.json `director_mandate`):
- **Action:** PIVOT with `cognitive_reset: true`
- **Target Claim:** C-MEAS-VALID (NOT C-WEB-DYNAMICS)
- **Parent Handoff Disposition:** SUPERSEDE — the parent handoff's continuity state is explicitly overridden; DESIGN must follow the mandate's strategic question, not drift back to the parent's C-WEB-DYNAMICS calibration question.
- **Allocation Dependencies:**
  - Runtime owns substrate-side controls (writable/auth/session/drift on validated distributed HTTP substrate)
  - Physics owns estimator-side validity
  - Codex: must use exact statistics recorded in Codex, not re-implementations
  - No external dependencies: executable on stdlib-served multi-page HTTP with server-side ground-truth transition log, no model credential, container registry auth, or browser binary

---

## 3. Substrate Specification (Browser-Free, Stdlib-Only)

### 3.1 HTTP Server
- **Implementation:** Python `http.server` + `nginx` reverse proxy (validated in EXP-RUNTIME-36100549580)
- **Configuration:** Single-node, sticky routing via `hash $request_uri`, shared SQLite WAL at `/tmp/single.db`
- **Endpoints:** Multi-page transitions with stateful auth (HMAC-SHA256 per auth_state)
- **Headers:** Deterministic header generation (filtered MINUS {content-length, etag, w-etag, range})
- **Compression:** Greedy brotli→gzip decompression, MAX_DEPTH5, oracle-free byte-identical HIT verification
- **Ground Truth:** Server-side transition log recording (state, action, next_state, regime, timestamp) for every request

### 3.2 Ground-Truth Transition Log
- **Schema:** `(trajectory_id, step, state_before, action, state_after, regime, url_before, url_after, timestamp)`
- **Completeness:** 100% of transitions logged server-side before response
- **Alignment:** Client-observed transitions must match server log 1:1 (verified post-hoc)
- **Regimes:** At least 2 distinct dynamical regimes (e.g., "deterministic" vs "stochastic" transition kernels)

### 3.3 No External Dependencies
- No model API credentials (OpenAI, Anthropic, etc.)
- No container registry authentication (GHCR, Docker Hub, etc.)
- No browser binaries (Playwright, Chrome, Firefox, etc.)
- Stdlib + nginx + SQLite only

---

## 4. The Intervention-Validity Contract (IVC)

The IVC is a **single deterministic Python class** `InterventionValidityContract` with one public method `evaluate(estimator, data, ground_truth) -> ContractResult`.

### 4.1 Contract Structure

```python
class ContractResult:
    verdict: Literal["ACCEPT", "REJECT", "INDETERMINATE"]
    invariance_passed: bool
    displacement_passed: bool
    min_permutation_p: float
    delta_statistic: float
    channel_MI: float
    code_path_hash: str  # SHA256 of the contract's evaluate() bytecode
```

### 4.2 Test 1: Metamorphic Invariance (IVC-METAMORPHIC-INVARIANCE)

**Principle:** A valid estimator's output must be invariant to within-stratum permutation of the treatment variable. If permuting the treatment within each stratum changes the statistic, the estimator is reading the treatment label rather than its information content.

**Procedure:**
1. For each stratum `s` (defined by ground-truth state/context), collect all transitions in that stratum
2. Compute `statistic_original = estimator(data)`
3. For each stratum, permute the treatment variable (R channel) within that stratum
4. Compute `statistic_permuted = estimator(permuted_data)`
5. Check **bitwise equality**: `statistic_original == statistic_permuted` for all outputs

**Criterion:** `invariance_passed = True` iff bitwise equality holds for all strata.

**Note:** This test must PASS for all valid estimators (known-good and known-bad alike). A known-bad estimator that is structurally R-invariant (like Physics CMI) will pass this test — which is correct behavior. The invariance test alone cannot distinguish them; it establishes the baseline invariance property.

### 4.3 Test 2: Channel Displacement (IVC-CHANNEL-DISPLACEMENT)

**Principle:** A valid estimator must respond to a treatment channel whose mutual information (MI) with the target is known and pre-registered. Re-drawing the treatment through such a channel must move the statistic by at least the channel's marginal-conditional information.

**Procedure:**
1. **Pre-register channel MI:** For each test channel `c`, compute `MI_c = I(R_c; target | context)` from ground truth BEFORE freezing the contract. Record in `preregistered_channels.json`.
2. For each channel `c`:
   a. Replace the treatment variable in data with channel `c`'s values
   b. Compute `statistic_c = estimator(data_with_channel_c)`
   c. Compute `delta = |statistic_c - statistic_baseline|` where baseline is the null channel (shuffled)
   d. Run permutation test: permute channel `c` within strata `n_perms=1000` times, compute `p = (1 + n_exceed) / (n_perms + 1)`
3. **Criterion:** `displacement_passed = True` iff `delta >= MI_c AND p < 0.01` for the channel.

**Pre-Registered Channels (measured from ground truth before freeze):**

| Channel ID | Description | Pre-Registered MI (bits) | Expected Verdict |
|------------|-------------|--------------------------|------------------|
| `CH-IDENTITY` | Deterministic copy of latent state | H(latent) = log2(n_states) | ACCEPT (known-good) |
| `CH-SHUFFLED` | Random permutation within strata | 0.0 | REJECT (null) |
| `CH-PARTIAL-0.5` | 50% fidelity to latent, 50% noise | 0.5 * H(latent) | ACCEPT (known-good) |
| `CH-PARTIAL-0.1` | 10% fidelity to latent, 90% noise | 0.1 * H(latent) | REJECT (known-bad threshold) |

**Critical Requirement:** The minimum attainable permutation p across ALL channels on a known-bad estimator MUST be < 0.01. If the contract's null is degenerate (p=1.0 floor), the contract itself is MEASUREMENT_INVALID.

### 4.4 Test 3: Identical Code Path (IVC-IDENTICAL-CODE-PATH)

**Principle:** All estimator evaluations must pass through the exact same `evaluate()` method. No special-casing, no estimator-specific branches.

**Verification:** Record SHA256 of `InterventionValidityContract.evaluate.__code__.co_code` at runtime. All 9 test cases must show identical hash.

### 4.5 Test 4: Server Ground Truth (IVC-SERVER-GROUND-TRUTH)

**Principle:** The contract's MI computations and permutation tests must use server-side ground truth, not client-observed proxies.

**Verification:** Post-execution audit comparing contract-internal MI values against independent ground-truth recomputation.

---

## 5. Test Battery: Known-Bad Estimators (Must REJECT)

### 5.1 KB-PHYSICS-CMI — Physics Conditional-Entropy Statistic
- **Source:** EXP-PHYSICS-36279239922 / `execute_calibration_v3.py`
- **Failure Mode:** `K_per_stratum` keyed by C stratum alone (lines 351-355), while R-conditioned term keyed by (C,R) (line 268) and skipped by line-207 guard. Result: 0 of 468 (C,R) cells resolve, `H(S_next|C,R) ≡ 0.0`, `p_raw` floored at 1.0 for ANY dataset.
- **Codex Reference:** `research/experiments/EXP-PHYSICS-36279239922/execute_calibration_v3.py` (sha256: `19e44d27bc6b089a3a5297396c1bb97887cf6f65c74cf211a4555ab6570bc0e4`)
- **Implementation:** Use the EXACT code from the Codex artifact. Do not re-implement.
- **Expected Contract Verdict:** REJECT (fails channel displacement: delta=0, p=1.0)

### 5.2 KB-PRODUCT-COLD — Product Fixed-Request Cold Comparator
- **Source:** EXP-PRODUCT-36272385776 and related Product experiments
- **Failure Mode:** Cold baseline operates at per-task optimum (1.0 HTTP request/task for crud-read/query), leaving zero dynamic range for amortization. The economic comparator cannot distinguish SPIDER from cold because both achieve identical per-task cost on this substrate.
- **Codex Reference:** `EXP-PRODUCT-36272385776` verdict.json — "cold baseline already operates at the per-task optimum... leaving no per-task saving to amortize the 100-request induction bill"
- **Implementation:** The comparator that computes `amortized_cost_ratio = treatment_cost / cold_cost` where `cold_cost ≡ 1.0` per task by substrate construction.
- **Expected Contract Verdict:** REJECT (zero dynamic range: delta=0 for all channels, p=1.0)

### 5.3 KB-FRONTIER-GOAL — Frontier Goal-State-Success Endpoint
- **Source:** EXP-FRONTIER-36272394045
- **Failure Mode:** Goal-state success = 1.000 for all 7 arms including one wrong on 43.3% of spans. The endpoint metric is blind to missing binding key (capability handle).
- **Codex Reference:** `EXP-FRONTIER-36272394045` result.json controls.CTRL-CORRECTNESS-INVARIANCE — "goal-state success is 1.0 for arms whose span-level action correctness is as low as 0.5667"
- **Implementation:** The metric `goal_state_success = all(steps.expected_code AND final_store_empty)` which ignores action-level correctness.
- **Expected Contract Verdict:** REJECT (insensitive to treatment: delta=0, p=1.0)

---

## 6. Test Battery: Known-Good Estimators (Must ACCEPT)

### 6.1 KG-RUNTIME-HEADER-JACCARD — Runtime Header-Only Jaccard Discrimination
- **Source:** EXP-RUNTIME-36100549580 (VALIDATED)
- **Success Mode:** Header-only Jaccard mean=0.4643, variance=0.0958, std=0.3095, null FP=0.0, same-state J=1.0, scheduling de-confounded (r=0.0087, V=0.0379). Full-vector discrimination 0.7619 > max(body=0.381, status=0.0) + 0.05.
- **Codex Reference:** `EXP-RUNTIME-36100549580` verdict.json claim_updates C-MEAS-VALID VALIDATED
- **Implementation:** The exact discrimination estimator from the validated Runtime substrate: Jaccard similarity on filtered headers (MINUS body-derived) between same-state vs different-state transition pairs.
- **Expected Contract Verdict:** ACCEPT (responds to CH-IDENTITY and CH-PARTIAL-0.5 with delta >= MI, p < 0.01)

---

## 7. Baselines and Controls

| ID | Description | Expected Contract Verdict | Purpose |
|----|-------------|---------------------------|---------|
| B-NULL-INSTRUMENT | Constant statistic (returns 0.0 always) | REJECT | Verify contract detects zero dynamic range |
| B-IDENTITY-CHANNEL | Treatment = latent state copy (MI = H(latent)) | ACCEPT | Verify contract accepts maximum signal |
| B-SHUFFLED-CHANNEL | Treatment = random within-stratum permutation (MI = 0) | REJECT | Verify contract rejects null channel |
| PC-RUNTIME-HEADER-JACCARD | Runtime header Jaccard (validated) | ACCEPT | Positive control: known-good estimator |
| NC-CONSTANT-ZERO | Degenerate constant-zero statistic | REJECT | Null control: contract's own null must reject this |

---

## 8. Measurement Validity Gates (Pre-Registered)

| Gate | Criterion | Failure → |
|------|-----------|-----------|
| G1-INVARIANCE | All estimators pass bitwise invariance test | MEASUREMENT_INVALID (contract defect) |
| G2-DISPLACEMENT-POWER | min_permutation_p < 0.01 on ALL known-bad estimators | MEASUREMENT_INVALID (contract's null lacks power) |
| G3-KNOWN-BAD-REJECT | All 3 known-bad → REJECT | FALSIFIES (contract fails primary purpose) |
| G4-KNOWN-GOOD-ACCEPT | At least 1 known-good → ACCEPT | FALSIFIES (contract has false positive) |
| G5-IDENTICAL-PATH | All 9 cases share identical code_path_hash | MEASUREMENT_INVALID (infrastructure failure) |
| G6-GROUND-TRUTH | Server log completeness = 100%, alignment verified | MEASUREMENT_INVALID (substrate failure) |
| G7-NO-EXTERNAL-DEPS | No credentials, containers, browser used | MEASUREMENT_INVALID (violation of mandate) |

**Gate Evaluation Order:** G5, G6, G7 (infrastructure) → G1, G2 (contract validity) → G3, G4 (scientific outcome)

---

## 9. Data Collection and Sample Sizes

- **Trajectories:** 200 trajectories × 10 steps = 2,000 transitions per regime
- **Regimes:** 2 (deterministic kernel, stochastic kernel with 0.3 noise)
- **States per regime:** 8 distinct states
- **Actions:** 4 actions per state
- **Total transitions:** 4,000 (sufficient for MI estimation and permutation tests)
- **Permutations per channel:** 1,000 (gives p-resolution of 0.001)
- **Random Seeds:** Fixed seed `44` for all stochastic components (matching EXP-RUNTIME-36100549580)

---

## 10. Threats to Validity and Mitigations

| Threat | Mitigation |
|--------|------------|
| Contract implementation bug | Unit tests for IVC on synthetic data with known outcomes; code_path_hash verification |
| Ground-truth log mismatch | Post-execution audit: independent recomputation of MI from server logs vs contract-internal |
| Estimator version drift | Use EXACT Codex artifact hashes for all 3 known-bad estimators; pin Runtime estimator to EXP-RUNTIME-36100549580 commit |
| Channel MI miscalibration | Pre-register all channel MI values in `preregistered_channels.json` BEFORE freeze; verify against ground truth |
| Permutation test degeneracy | Pre-compute minimum attainable p for each known-bad estimator; if any ≥ 0.01, contract is MEASUREMENT_INVALID by design |
| Substrate non-determinism | Deterministic server (single-threaded http.server), fixed seeds, no concurrency |

---

## 11. Representation Integrity

- **Raw Observations Preserved:** Full HTTP request/response pairs logged (method, path, headers, body, status)
- **Derived Variables:** State representation = `(url, filtered_headers_sha256)`; Action = `(method, path_template, param_values)`; Next-state = same as state
- **Losses Documented:** Body content not used in state representation (by design, matching Runtime validated substrate); dynamic form values not captured (no forms in this substrate)
- **Alternative Representation Survival:** Contract must also pass if state representation uses full headers (no filtering) — tested as robustness check in `validity_notes`, not a primary gate.

---

## 12. Pre-Registered Analysis Plan

No post-hoc analysis. The decision rule in `spec.json` is the complete analysis plan.

**Outputs (written by EXECUTE):**
- `result.json` — structured metrics per `EXPERIMENT_PACKET.md` schema
- `contract_results.json` — per-estimator ContractResult objects
- `preregistered_channels.json` — channel MI values measured pre-freeze
- `ground_truth_log.jsonl` — server-side transition log
- `code_path_hash.txt` — SHA256 of contract evaluate() bytecode
- `report.md` — interpretation bounded by measurements
- `provenance.json` — commits, environment, seeds, artifact hashes

---

## 13. No-Drift Clause

After `freeze.json` is created:
- No changes to `spec.json`, `prereg.md`, or `request.json`
- No changes to the IVC implementation (`intervention_validity_contract.py`)
- No changes to the substrate server code
- No changes to the estimator implementations (use Codex artifact hashes)
- Any post-freeze deviation → MEASUREMENT_INVALID

---

## 14. Artifact Identifiers for Downstream Transmission

All metrics and controls use stable identifiers from `spec.json`:

**Metrics (in result.json.metrics):**
- `IVC_CONTRACT_VERDICT_[ESTIMATOR_ID]` — ACCEPT/REJECT/INDETERMINATE
- `IVC_INVARIANCE_PASSED_[ESTIMATOR_ID]` — bool
- `IVC_DISPLACEMENT_PASSED_[ESTIMATOR_ID]` — bool
- `IVC_MIN_PERMUTATION_P_[ESTIMATOR_ID]` — float
- `IVC_DELTA_STATISTIC_[ESTIMATOR_ID]` — float
- `IVC_CHANNEL_MI_[CHANNEL_ID]` — float (pre-registered)
- `IVC_CODE_PATH_HASH` — string (identical for all)

**Controls (in result.json.controls):**
- `B-NULL-INSTRUMENT`, `B-IDENTITY-CHANNEL`, `B-SHUFFLED-CHANNEL`
- `PC-RUNTIME-HEADER-JACCARD`, `NC-CONSTANT-ZERO`
- `KB-PHYSICS-CMI`, `KB-PRODUCT-COLD`, `KB-FRONTIER-GOAL`
- `KG-RUNTIME-HEADER-JACCARD`

**Artifacts (in result.json.artifacts):**
- `intervention_validity_contract.py` (role: code)
- `preregistered_channels.json` (role: fixture)
- `ground_truth_log.jsonl` (role: raw)
- `contract_results.json` (role: derived)
- `code_path_hash.txt` (role: derived)

---

## 15. Consequences Summary

| Outcome | C-MEAS-VALID Status | Product Action | Next Step |
|---------|---------------------|----------------|-----------|
| SUPPORTS | → EXPERIMENTAL (with concrete IVC artifact) | Publish IVC as reusable gate; all lanes must certify estimators | Global Director allocates IVC integration across lanes |
| FALSIFIES | → MEASUREMENT_INVALID (no reusable certification path) | Continue bespoke per-lane gates; gate proliferation continues | Global Director re-evaluates C-MEAS-VALID strategy |
| MEASUREMENT_INVALID | → MEASUREMENT_INVALID (infrastructure/contract defect) | Fix contract/substrate; re-run with new mandate | PIVOT or PARK per Global Director |
| INCONCLUSIVE | → EXPERIMENTAL (ambiguous) | Investigate ambiguity; likely redesign contract | Global Director decides |

---

**Frozen by:** DESIGN agent
**Freeze Hash:** (to be computed by deterministic freezer)
**Date:** 2026-09-27