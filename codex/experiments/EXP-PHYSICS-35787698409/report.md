# EXP-PHYSICS-35787698409 — RECALIBRATED Correlated-State CMI Measurement

**Lane:** physics · **Status:** MEASUREMENT_INVALID · **Outcome:** NOT_APPLICABLE
**Frozen inputs (all verified against freeze.json `bd75109e...`):** request `eeaa8b63...`, spec `8dd815d0...`, prereg `4663c261...`. Git HEAD `db7e59ee`.

## 1. Purpose and design

Second attempt at the dominant-measurement claim for `C-WEB-DYNAMICS`: a locally-hosted 6-state SPA with a per-trajectory correlated latent L (site-internal regime) produces DOM states (36 variants: 2 L × 6 variants/state) that carry predictive information about the next visited state S_next *beyond* the full browsing context (URL, last-3 leakage-free actions, current action). The Bayesian Dirichlet-Multinomial CMI estimator (K = number of DOM hash categories) is applied with trajectory-grouped permutation nulls.

This experiment is the **mandated recalibration** of parent EXP-PHYSICS-35782523165 (also MEASUREMENT_INVALID): the parent audit predicted K=24 would clear both null-centering thresholds ("mean 0.074 std 0.0104"). Recalibration applied exactly as frozen: **K = 24, alpha = 1/K**, independent-noise variants **3 → 6 per state**, i.i.d. null unchanged, N = 1999 (50 trajectories × 40 steps), 1000 grouped permutations, seed 42, `p_bonf` with n_tests = 8, alpha = 0.01.

Frozen gated decision rule (evaluated strictly in order): G1 positive control `BC>=0.30, p_raw<0.01, null_std>0.01, |null_mean|<0.1` on R1 or R2 → fail ⇒ MEASUREMENT_INVALID; G2 independent confound; G3 iid miscentering; G4 primary-null degeneracy on both R1/R2 (null_std≤0.01 or |null_mean|≥0.1) → fail ⇒ MEASUREMENT_INVALID; otherwise any `sig(R)` ⇒ SURVIVES_CURRENT_TEST (SUPPORTS) / no `sig(R)` ⇒ FALSIFIED-IN-SETTING (FALSIFIES).

## 2. Raw evidence and replication

Generated from the same frozen construction as the parent (locally-hosted Express SPAs, PYTHONHASHSEED=0, numpy seed 42, `trajectory_id` = 50 integer labels 0–49 from default_rng(777), L per trajectory from `default_rng(seed+99)`, correlated transitions `default_rng(seed+666)`, iid `default_rng(seed+777)`, independent `default_rng(seed+999)`):

- `raw_transitions_correlated.json` sha256 `2ffc9e95...` — **byte-identical to parent** (replication confirmed).
- `raw_transitions_iid.json` sha256 `ab685d9d...` — **byte-identical to parent**.
- `raw_transitions_independent.json` sha256 `7215be08...` — differs from parent **by design** (RECALIBRATED 6 variants/state, parent `4ee10d70...` 3 variants).

## 3. Results

### 3.1 Recalibration outcome (headline)

K=12→24 fixed the null **mean** (0.1297 → 0.0748, now < 0.1) but **not** the null **std** (0.0097, still ≤ 0.01). The permutation std is a variance property of the grouped-permutation estimator at N=1999 / 24 strata — it scales *down* with N, so more data alone cannot clear the frozen `null_std>0.01` threshold. Every other measurement is far from borderline.

### 3.2 Decision gates (frozen order) → MEASUREMENT_INVALID

| Gate | Criterion | R1 | R2 | Verdict |
|---|---|---|---|---|
| G1 positive control | BC≥0.30, p_raw<0.01, null_std>0.01, \|null_mean\|<0.1 | BC 0.7066, p 0.0010, std 0.0097, mean 0.0748 | identical | **FAIL** (std shortfall 0.0003 bits) |
| G2 independent confound | NOT(BC≥0.05 & p<0.10) | BC −0.0006, p 0.5295 | identical | pass |
| G3 iid miscentering | NOT(BC>0.03 & p<0.10) | BC 0.0016, p 0.3926 | identical | pass |
| G4 primary-null degenerate | NOT(degenerate on both) | std 0.0097≤0.01 → degenerate | identical | **FAIL** |

Frozen consequence: **status = MEASUREMENT_INVALID, outcome = NOT_APPLICABLE, verdict = MEASUREMENT_INVALID** (`pipeline_blind_or_miscalibrated` category, though reason recorded for this run is the borderline null std, not blindness). The primary claim is **not adjudicated**; this is a measurement-validity verdict, **not** a falsification.

### 3.3 Measurements (derived, from `raw_results.json`)

- **Primary correlated (K=24):** observed CMI 0.7815 bits, perm null mean 0.0748, std 0.0097, **BC 0.7066**, p_raw 0.001 (floor), p_bonf 0.0080, Cohen d 73.05, null 95% CI [0.057, 0.094]. Identical on R1/R2/R3 (all encode L); R4 numeric-structural null (BC −0.0040, p 0.736).
- **Independent-noise control (6 variants):** BC −0.0006, p 0.529 — replicates prior falsifications (parent −0.0051; EXP-PHYSICS-34764605162 0.004 bits); no confound.
- **IID null:** BC 0.0016, p 0.393 — centered; correlated signal is not estimator bias.
- **Baselines:** B-DOM-SIMILARITY 0.0 (acc 0.108), B-MARKOV-1 0.0, B-MARKOV-K3 0.0 → gap 0.7066, would satisfy `sig(R)` if gates passed.
- **Diagnostics (non-gating):** B-SITE-LEAKAGE leaky BC 0.0363 vs free 0.7066 → signal lives in leakage-free DOM content, not href; B-TRAJECTORY-MEMORY test exact-acc 0.152 vs chance 0.167 → no memorization artifact; S_URLonly BC 0.079 → no URL-leakage artifact.
- **Data quality:** H(S|C) 3.334 > 0.3; strata 24 (ge3 24, singleton 0); |R|/N 0.018; MI(DOM;Action) 0.0. All pass.

## 4. Interpretation

A single, razor-thin quantity — grouped-permutation null std 0.0097 vs frozen threshold 0.01 (shortfall 0.0003 bits, ~3% of the std; observed BC is ~70 stds above the null) — drives the MEASUREMENT_INVALID verdict, same as the parent but now on the *std* arm only. The recalibration resolved the centering concern completely; it did not and (by construction) cannot raise permutation spread.

Per failure discipline, the frozen rule stands as recorded: this is a negative *measurement-validity* result, not a weakening of the claim. The claim direction (correlated DOM carries state-predictive information beyond context) continues to receive strong, internally consistent support in every gate that does not touch the std threshold (BC 0.71, p_bonf 0.008, d 73, gap 0.71, nulls centered on both controls, leak and memorization diagnostics clean).

## 5. Consequences

- **Positive outcome would have required** G1+G4 pass ⇒ SURVIVES_CURRENT_TEST supporting C-WEB-DYNAMICS with BC 0.707; instead the frozen rule yields MEASUREMENT_INVALID (validity unknown, claim not adjudicated).
- **Next-step options** (for Global Research Director / lane Director only; lane does not self-dispatch):
  1. New prereg adjusting the degeneracy definition (e.g., a theoretically motivated null_std floor or a distributional degeneracy check) — the current borderline is 0.0003 bits, and BC separation is ~70 stds;
  2. Same-threshold replication at a different substrate (larger real-ish DOM corpus) where permutation variance may differ;
  3. Treat the tight-null regime as diagnosed and proceed to a production-substrate (BrowserGym-class) probe;
  4. Park C-WEB-DYNAMICS measurement and reopen the earlier statistical machinery (estimator/permutation design) as its own thread.

## 6. Deliverables

`result.json` (packet shape), `report.md`, `provenance.json`; raw evidence, code and hashes listed in `provenance.json`; artifacts preserved unmodified.