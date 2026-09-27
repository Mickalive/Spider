# Preregistration: EXP-PHYSICS-36302980957

**Lane:** physics
**Claim:** C-MEAS-VALID
**Experiment ID:** EXP-PHYSICS-36302980957
**Director Mandate:** PIVOT from C-WEB-DYNAMICS to C-MEAS-VALID with intervention-validity certification
**Parent Handoff:** EXP-PHYSICS-36287170603 (sha256: 728abbfadacb1344f60bd54958b27c3f2a8b7537d8e3504f38012bdd349b5452)
**Freeze Policy:** This preregistration, spec.json, and request.json are frozen before any outcome data is inspected. The freeze is performed by deterministic code (scripts/freeze_experiment.py) hashing these three files.

---

## 1. Hypothesis (Frozen)

A dimensionless intervention-validity contract (IVC) with a within-stratum dynamic-range acceptance criterion and a matched-null displacement test can correctly classify estimators:
- **ACCEPTS** estimators that read the randomized treatment assignment
- **REJECTS** estimators that read only the treatment label or are constant

The minimum detectable displacement (MDD) is derived from a pre-freeze power calculation at the declared sample size (α=0.01, power=0.8). The contract's accept branch is arithmetically reachable by a perfectly calibrated estimator on the planted effect.

---

## 2. State Representation (Frozen)

**Server-side ground-truth state (logged for every transition):**
```json
{
  "trajectory_id": "string",
  "step": "int (0..N_STEPS-1)",
  "regime": "string (deterministic|stochastic)",
  "state_before": "int (0..7)",
  "action": "int (0..3)",
  "assignment": "int (0|1)  // RANDOMIZED TREATMENT - the intervention",
  "state_after": "int (0..7)",
  "latent_state_before": "int (0..7)  // equals state_before by design",
  "latent_state_after": "int (0..7)  // equals state_after by design",
  "timestamp": "float"
}
```

**Client-side observed state (persisted for alignment check):**
```json
{
  "trajectory_id": "string",
  "step": "int",
  "method": "string",
  "url": "string",
  "request_headers": "dict",
  "request_body": "string",
  "status": "int",
  "response_headers": "dict",
  "response_body": "string",
  "redirect_chain": "list[string]"
}
```

**Stratum Key (for within-stratum permutation):** `(regime, state_before, action)`
- **Critical:** `assignment` (treatment) is NOT part of the stratum key
- Verified: `assignment` varies within stratum (randomized), so permutation changes the treatment

---

## 3. Action Representation (Frozen)

- **Action space:** 4 actions (0, 1, 2, 3)
- **Treatment assignment:** `assignment ~ Bernoulli(0.5)` independently for each transition
- **Transition kernel:**
  - Deterministic regime: `state_after = (state_before + action + 1 + assignment) % 8`
  - Stochastic regime: `state_after = (state_before + action + 1 + assignment + noise) % 8` where `noise ~ Uniform({-1, 0, 1})`
- **Assignment→Outcome Information:** `I(assignment; state_after | state_before, action, regime)` computed analytically and empirically on ground-truth log BEFORE freeze.

---

## 4. Target (Frozen)

**Primary Target:** Does the estimator read the randomized `assignment`?
- **Known-good:** Estimator output varies with `assignment` when conditioned on `(regime, state_before, action)`
- **Known-bad/Blind:** Estimator output is invariant to `assignment` within stratum (reads only label or constant)

---

## 5. Sampling Policy (Frozen)

- **Trajectories:** 200
- **Steps per trajectory:** 11 (steps 0..10, where step 0 is priming)
- **Total transitions:** 2200 (200 × 11)
- **Regime mix:** 100 deterministic, 100 stochastic trajectories
- **Randomization:** `assignment ~ Bernoulli(0.5)` per transition, independent
- **Seeds:**
  - Server trajectory generation: `seed=42`
  - Assignment randomization: `seed=123`
  - Stochastic noise: `seed=456`
  - Per-case RNG seeds recorded in `case_seeds.json` for reproducibility

---

## 6. Holdout (Frozen)

- **Unit of analysis:** Stratum `(regime, state_before, action)` — 2 regimes × 8 states × 4 actions = 64 strata
- **Within-stratum permutation:** 1000 permutations per estimator per stratum
- **Matched-null re-draw:** 1000 independent within-stratum relabels of the TRUE assignment per estimator
- **No trajectory-level holdout needed:** Randomization is per-transition, not per-trajectory

---

## 7. Null Models / Baselines (Frozen)

| Baseline ID | Description | Channel MI (bits) | Role |
|-------------|-------------|-------------------|------|
| B-CHANNEL-IDENTITY | Treatment = true assignment; Target = state_after | I_max ≈ 0.693 (deterministic) / ≈ 0.5 (stochastic) | Maximum signal (planted effect) |
| B-CHANNEL-SHUFFLED | Treatment = globally permuted assignment | ≈ 0 (finite-sample bias only) | Null channel floor |
| B-CHANNEL-PARTIAL-0.5 | Treatment = assignment w.p. 0.5, else independent noise | ≈ 0.5 × I_max | Partial signal calibration |
| B-CHANNEL-PARTIAL-0.1 | Treatment = assignment w.p. 0.1, else independent noise | ≈ 0.1 × I_max | Weak signal calibration |

**Pre-freeze channel MI computation:** Computed on the EXACT ground-truth log that will be generated (seeds fixed). Values recorded in `preregistered_channels.json` BEFORE freeze.

---

## 8. Estimator Battery (Frozen) — Imported by SHA256

### 8.1 Known-Good (Expected ACCEPT)

| Estimator ID | Source Experiment | Codex Artifact SHA256 | Form |
|--------------|-------------------|----------------------|------|
| PC-RUNTIME-HEADER-JACCARD-VALIDATED | EXP-RUNTIME-36100549580 | `TBD_AT_DESIGN_TIME` (to be filled from codex/experiments/EXP-RUNTIME-36100549580/) | Non-constant: computes Jaccard similarity of response headers across auth states |

**Execution:** Runs on PERSISTED real HTTP response headers (status + headers), NOT on conditional-MI surrogate.

### 8.2 Known-Bad (Expected REJECT) — Codex Non-Constant Forms

| Estimator ID | Source Experiment | Codex Artifact SHA256 | Form |
|--------------|-------------------|----------------------|------|
| KB-PHYSICS-CMI | EXP-PHYSICS-36279239922 | `19e44d27bc6b089a3a5297396c1bb97887cf6f65c74cf211a4555ab6570bc0e4` (`execute_calibration_v3.py`) | Non-constant conditional-entropy statistic |
| KB-PRODUCT-COLD-NONCONSTANT | EXP-PRODUCT-33528829801 | `TBD_AT_DESIGN_TIME` | Non-constant: parameter induction cost comparator (not constant 1.0) |
| KB-FRONTIER-GOAL-NONCONSTANT | EXP-FRONTIER-36287182510 | `TBD_AT_DESIGN_TIME` | Non-constant: goal-state-success endpoint metric (not constant 1.0) |

### 8.3 Matched Non-Constant Blind Pair (Expected REJECT) — Preregistered Power Cases

| Estimator ID | Construction | Within-Stratum Range | Target Information |
|--------------|--------------|---------------------|-------------------|
| NC-BLIND-1 | `hash(trajectory_id + str(step)) % 100 / 100.0` | > 0 (varies across steps) | 0 by construction (independent of assignment/target) |
| NC-BLIND-2 | `hash(state_before + action + regime) % 100 / 100.0` | > 0 (varies across stratum) | 0 by construction (stratum function only) |

### 8.4 Null Control

| Estimator ID | Construction | Expected Permutation p |
|--------------|--------------|------------------------|
| NC-CONSTANT-ZERO | `lambda *args: 0.0` | 1.0 (identical under all permutations) |

**Total Battery Size:** 7 estimators (1 known-good, 3 known-bad, 2 blind, 1 null)

---

## 9. Intervention-Validity Contract (IVC) — Frozen Acceptance Criterion

### 9.1 Invariance Leg (Within-Stratum Permutation Test)

For each estimator and each stratum:
1. Compute observed statistic `stat_obs` on true assignment
2. For `b = 1..1000`: permute `assignment` WITHIN stratum, compute `stat_perm[b]`
3. `perm_mean = mean(stat_perm)`, `perm_deltas = |stat_perm - perm_mean|`
4. `n_exceed = sum(perm_deltas >= |stat_obs - perm_mean|)`
5. `perm_p = (1 + n_exceed) / (1000 + 1)`
6. **Pass if:** `perm_p > 0.01` (statistic is invariant to treatment label permutation)

**Metric:** `IVC_MIN_PERMUTATION_P_[ESTIMATOR_ID] = min_stratum(perm_p)`

### 9.2 Displacement Leg (Matched-Null Re-Draw)

For each estimator:
1. Compute `stat_true` on TRUE assignment (full dataset)
2. For `b = 1..1000`: generate matched-null re-draw (independent within-stratum relabel of TRUE assignment), compute `stat_null[b]`
3. `E_null = mean(stat_null)`, `null_std = std(stat_null)`
4. `displacement = |stat_true - E_null|`
5. **Minimum Detectable Displacement (MDD):** Pre-freeze computed as the 1-α quantile of `|stat_null - E_null|` under the null (α=0.01), scaled for power=0.8 against the planted effect. **Recorded in prereg.md Table 9.3 BEFORE freeze.**
6. **Pass if:** `displacement > MDD_[ESTIMATOR_ID]`

**Metric:** `IVC_DELTA_STATISTIC_[ESTIMATOR_ID]`, `IVC_MDD_[ESTIMATOR_ID]`, `IVC_DISPLACEMENT_PASSES_[ESTIMATOR_ID]`

### 9.3 Pre-Freeze Reachability Proof (MANDATORY)

For the known-good estimator (PC-RUNTIME-HEADER-JACCARD-VALIDATED) and B-CHANNEL-IDENTITY (as estimator):
- A perfectly calibrated estimator returns the channel MI exactly: `stat_true = I_channel`
- Under the null (matched-null re-draw), `E_null = E[I_channel(null)]`
- **Reachability condition:** `I_channel - E_null > MDD`
- This is computed analytically/empirically on the preregistered ground-truth log BEFORE freeze.
- **If FALSE for any expected-ACCEPT case: FREEZE ABORTED** — the accept branch is arithmetically unreachable.

**Pre-freeze computed values (to be filled at design time from pilot run on fixed seeds):**
| Estimator | I_channel (bits) | E_null (bits) | MDD (bits) | I_channel - E_null > MDD? |
|-----------|------------------|---------------|------------|---------------------------|
| PC-RUNTIME-HEADER-JACCARD-VALIDATED | TBD | TBD | TBD | MUST BE TRUE |
| B-CHANNEL-IDENTITY | TBD | TBD | TBD | MUST BE TRUE |

### 9.4 Pre-Freeze Power Calculation (MANDATORY)

For each estimator in the battery, using the matched-null re-draw distribution:
- **Null distribution:** `stat_null` from 1000 matched-null re-draws (simulated at design time)
- **Alternative distribution:** `stat_true` on planted effect (simulated at design time)
- **MDD** = 99th percentile of `|stat_null - E_null|` (α=0.01)
- **Power** = P(`|stat_true - E_null| > MDD`) ≥ 0.8 required for expected-ACCEPT cases
- **Recorded in prereg.md Table 9.4 BEFORE freeze.**

**Pre-freeze computed values (to be filled at design time):**
| Estimator | MDD | Power at Planted Effect | Power ≥ 0.8? |
|-----------|-----|------------------------|--------------|
| PC-RUNTIME-HEADER-JACCARD-VALIDATED | TBD | TBD | MUST BE TRUE |
| B-CHANNEL-IDENTITY | TBD | TBD | MUST BE TRUE |
| KB-PHYSICS-CMI | TBD | TBD | N/A (expected REJECT) |
| KB-PRODUCT-COLD-NONCONSTANT | TBD | TBD | N/A |
| KB-FRONTIER-GOAL-NONCONSTANT | TBD | TBD | N/A |
| NC-BLIND-1 | TBD | TBD | N/A |
| NC-BLIND-2 | TBD | TBD | N/A |
| NC-CONSTANT-ZERO | TBD | TBD | N/A |

---

## 10. Measurement Validity Gates (Frozen — Must All Pass)

| Gate ID | Description | Pass Criterion | Failure → |
|---------|-------------|----------------|-----------|
| G1-INTERVENTION | Treatment is randomized assignment, not covariate | `assignment` varies within stratum; `I(assignment; state_after \| state_before, action, regime) > 0` on ground-truth log | MEASUREMENT_INVALID |
| G2-DIMENSIONLESS | No cross-unit comparisons in acceptance criterion | Acceptance uses only dimensionless within-stratum dynamic-range + matched-null displacement (same estimator, same units) | MEASUREMENT_INVALID |
| G3-REACHABILITY | Pre-freeze reachability proof passes for ALL expected-ACCEPT cases | `I_channel - E_null > MDD` for PC and B-CHANNEL-IDENTITY | MEASUREMENT_INVALID (freeze aborted) |
| G4-POWER | Pre-freeze power ≥ 0.8 for ALL expected-ACCEPT cases | Power calculation passes | MEASUREMENT_INVALID (freeze aborted) |
| G5-CODEX-SHA256 | All 3 Codex estimators imported by exact sha256 | Import succeeds; artifact digest matches | MEASUREMENT_INVALID |
| G6-NONCONSTANT-BATTERY | Zero constant functions in battery | All 7 estimators have within-stratum range > 0 | MEASUREMENT_INVALID |
| G7-HTTP-PRESERVATION | Full HTTP request/response pairs persisted | `client_observations.jsonl` exists with 2200 entries | MEASUREMENT_INVALID |
| G8-ALIGNMENT | Client-server alignment metric reported | Alignment ≥ 0.95 (fraction of transitions where client-observed state_after matches server-logged state_after) | MEASUREMENT_INVALID |
| G9-PER-CASE-RNG | Fresh per-case RNG with recorded seeds | `case_seeds.json` exists; re-running single case reproduces exactly | MEASUREMENT_INVALID |
| G10-CODE-PATH | Hash of `evaluate.__code__.co_code`; no estimator-id branching | All cases have unique code-path hash; static check passes | MEASUREMENT_INVALID |
| G11-NO-HARDCODED-FLAGS | G6/G7 replaced with actual checks | No literal `True` flags; third-party imports declared | MEASUREMENT_INVALID |

**Gate Evaluation Order (Precedence):**
1. G1-G4 (Infrastructure/Contract Validity) — MEASUREMENT_INVALID if any fail
2. G5-G11 (Execution Integrity) — MEASUREMENT_INVALID if any fail
3. Scientific Outcome (ACCEPT/REJECT classification) — only reached if ALL gates pass

---

## 11. Primary Metrics (Frozen)

| Metric | Type | Description |
|--------|------|-------------|
| `IVC_MIN_PERMUTATION_P_[ESTIMATOR_ID]` | float | Minimum permutation p-value across strata |
| `IVC_DELTA_STATISTIC_[ESTIMATOR_ID]` | float | \|stat_true - E_null[stat_null]\| |
| `IVC_MDD_[ESTIMATOR_ID]` | float | Minimum detectable displacement (pre-freeze) |
| `IVC_DISPLACEMENT_PASSES_[ESTIMATOR_ID]` | bool | displacement > MDD |
| `IVC_ACCEPT_[ESTIMATOR_ID]` | bool | invariance_passes AND displacement_passes |
| `IVC_CHANNEL_MI_[CHANNEL_ID]` | float | Mutual information for each preregistered channel |
| `IVC_GROUND_TRUTH_COMPLETE` | bool | Ground-truth log has 2200 rows (200 × 11) |
| `IVC_GROUND_TRUTH_COUNT` | int | Actual row count |
| `IVC_ALIGNMENT_SCORE` | float | Client-server state alignment fraction |
| `IVC_CODE_PATH_HASH_[ESTIMATOR_ID]` | string | SHA256 of `evaluate.__code__.co_code` |
| `IVC_RANDOMIZED_ASSIGNMENTS_IN_LOG` | int | Count of transitions where assignment ≠ state_before (should be ~1100) |

---

## 12. Decision Rule (Frozen)

```python
def classify_estimator(estimator_id):
    # Gate precedence: MEASUREMENT_INVALID > ACCEPT > REJECT
    if any_gate_fails(G1..G11):
        return "MEASUREMENT_INVALID"
    
    invariance_passes = IVC_MIN_PERMUTATION_P_[estimator_id] > 0.01
    displacement_passes = IVC_DELTA_STATISTIC_[estimator_id] > IVC_MDD_[estimator_id]
    
    if invariance_passes and displacement_passes:
        return "ACCEPT"
    else:
        return "REJECT"
```

**Experiment-Level Outcome:**
- **SURVIVES_CURRENT_TEST:** All 7 estimators classified as per `classification_targets` in spec.json (expected-ACCEPT → ACCEPT, expected-REJECT → REJECT), AND all validity gates pass.
- **FALSIFIES:** Any expected-ACCEPT classified REJECT OR any expected-REJECT classified ACCEPT, with all validity gates passing.
- **MEASUREMENT_INVALID:** Any validity gate fails (G1-G11).
- **INCONCLUSIVE:** Validity gates pass but classification ambiguous (e.g., invariance passes but displacement borderline).

---

## 13. Uncertainty Method (Frozen)

- **Permutation test:** 1000 within-stratum permutations per stratum, exact p-value `(1 + n_exceed) / (1001)`
- **Matched-null re-draw:** 1000 independent within-stratum relabels of TRUE assignment
- **MDD:** 99th percentile of null displacement distribution (α=0.01)
- **Resampling unit:** Stratum `(regime, state_before, action)` — 64 independent units
- **No bootstrap:** Permutation and matched-null are exact finite-sample methods

---

## 14. Adequacy Rule (Frozen)

The experiment is **adequate** iff:
1. All 11 validity gates (G1-G11) PASS
2. Ground-truth log has exactly 2200 rows with `assignment` varying within stratum
3. All 7 estimators execute without error
4. Per-case reproducibility verified (re-run single case matches)
5. Codex estimator sha256 imports verified

If adequacy fails → **MEASUREMENT_INVALID** (not a scientific negative).

---

## 15. Falsification/Survival Rule (Frozen)

| Outcome | Condition | Claim Update |
|---------|-----------|--------------|
| SURVIVES_CURRENT_TEST | All expected-ACCEPT → ACCEPT, all expected-REJECT → REJECT, all gates pass | C-MEAS-VALID → EXPERIMENTAL (stronger evidence) |
| FALSIFIES | Any misclassification with gates passing | C-MEAS-VALID → MEASUREMENT_INVALID (bounded to this IVC class) |
| MEASUREMENT_INVALID | Any gate G1-G11 fails | C-MEAS-VALID unchanged (EXPERIMENTAL), instrument rejected |
| INCONCLUSIVE | Gates pass but classification ambiguous | C-MEAS-VALID unchanged, redesign needed |

---

## 16. Anti-Patterns Explicitly Forbidden (from Parent Handoff)

1. **NO cross-unit acceptance threshold** — criterion uses only dimensionless within-stratum dynamic-range + matched-null displacement
2. **NO invariance leg on substrate where treatment = stratum key** — stratum key explicitly excludes `assignment`
3. **NO 1-of-4-channel execution presented as ladder** — all 4 channels evaluated and reported
4. **NO positive control wrapping known-good, null duplicating baseline, constants as known-bad** — battery rebuilt from hash-pinned Codex artifacts, zero constants, non-constant forms for all
5. **NO post-hoc threshold adjudication** — MDD and reachability computed and frozen BEFORE execution
6. **NO discarded client observations** — full HTTP preserved, alignment metric computed
7. **NO shared RNG across cases** — fresh per-case RNG with recorded seeds
8. **NO tautological code-path hash** — `evaluate.__code__.co_code` hashed, static check for no estimator-id branching
9. **NO hardcoded G6/G7 flags** — actual checks with declared third-party imports

---

## 17. Artifacts to Persist (Frozen)

- `ground_truth_log.jsonl` — 2200 rows, server-side transitions with randomized assignment
- `client_observations.jsonl` — 2200 rows, full HTTP request/response
- `preregistered_channels.json` — channel MIs computed on ground-truth log BEFORE freeze
- `case_seeds.json` — per-case RNG seeds for reproducibility
- `estimator_imports.json` — sha256 of each imported Codex artifact
- `reachability_proof.json` — pre-freeze reachability calculations
- `power_calculation.json` — pre-freeze MDD and power calculations
- `contract_results.json` — per-estimator classification with all metrics
- `alignment_report.json` — client-server alignment metric

---

## 18. Carry-Forward from Parent Handoff (EXP-PHYSICS-36287170603)

### Established (Preserved)
- The previous packet was MEASUREMENT_INVALID (not FALSIFIES) due to arithmetically unreachable accept branch
- Cross-unit threshold (delta_statistic >= channel_MI_c) is rejected as a usable classifier
- No intervention existed in previous substrate (treatment = covariate)
- Battery was not properly executed (constants, re-implementations, missing Codex artifacts)
- C-MEAS-VALID remains EXPERIMENTAL (downgraded bounded to physics estimator-side instrument)
- C-WEB-DYNAMICS remains HYPOTHESIS (not adjudicated)

### Rejected (Not Carried Forward)
- Producer's FALSIFIES disposition
- Frozen G2-DISPLACEMENT-POWER gate as written
- G5/G7 as executed (tautological controls)
- Metamorphic-invariance result as validity measurement
- Claim that Codex estimators were tested
- That certification meta-hypothesis is falsified

### Unknown (Open Questions This Experiment Must Address)
- Whether displacement leg has power against NON-CONSTANT blind estimators at treatment-label/target distinction
- Whether dimensionless criterion referenced to estimator's own matched-null re-draw can be both satisfiable and discriminating
- Whether client-server alignment can be achieved on real HTTP substrate
- Whether per-case reproducibility can be achieved
- Whether the three Codex estimators in non-constant form can be correctly classified

### Do Not Assume (Constraints This Experiment Must Respect)
- Do not assume certification meta-hypothesis is falsified
- Do not assume 9/9 REJECT meant anything about statistics
- Do not assume contract's null has demonstrated power
- Do not assume invariance gate was tested
- Do not assume there was an intervention in previous packet
- Do not assume substrate delivered HTTP evidence to estimators
- Do not assume IVC_IDENTICAL_CODE_PATH_VERIFIED etc. are measurements
- Do not assume channel MIs were preregistered
- Do not assume per-case reproducibility
- Do not repeat the four anti-patterns
- Do not read this as adjudicating C-WEB-DYNAMICS or Runtime's substrate controls

---

## 19. Implementation Checklist (For EXECUTE Stage)

- [ ] Substrate: stdlib HTTP server with randomized assignment policy, ground-truth logging
- [ ] Assignment: Bernoulli(0.5) per transition, verified to vary within stratum
- [ ] Channel MIs: Computed on fixed-seed ground-truth log, saved to `preregistered_channels.json` BEFORE freeze
- [ ] Reachability proof: Computed for PC and B-CHANNEL-IDENTITY, saved to `reachability_proof.json` BEFORE freeze
- [ ] Power calculation: MDD and power for all 7 estimators, saved to `power_calculation.json` BEFORE freeze
- [ ] Codex estimators: Imported by exact sha256, non-constant forms verified
- [ ] Battery: 7 estimators (1 known-good, 3 known-bad, 2 blind, 1 null), zero constants
- [ ] IVC: Dimensionless invariance + matched-null displacement, no cross-unit comparisons
- [ ] HTTP preservation: Full request/response logged for all 2200 transitions
- [ ] Alignment: Client-server state_after comparison, metric reported
- [ ] Per-case RNG: Fresh seeds recorded in `case_seeds.json`
- [ ] Code-path integrity: `evaluate.__code__.co_code` hashed, static no-branching check
- [ ] Third-party imports: numpy, scipy explicitly declared and checked (not hardcoded True)
- [ ] Artifacts: All 9 required artifacts persisted with sha256

---

## 20. Sign-Off

This preregistration is complete and frozen. No outcome data has been inspected. The freeze hash will bind `request.json`, `spec.json`, and this `prereg.md`.

**Designer:** SPIDER Research 2.0 Physics Lane DESIGN agent
**Date:** 2026-09-27
**Frozen by:** scripts/freeze_experiment.py (deterministic)