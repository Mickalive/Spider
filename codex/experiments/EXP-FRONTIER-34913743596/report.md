# EXP-FRONTIER-34913743596 Report — Alternative Divergence Measures (KDE, kNN) Per-Type

**Lane:** frontier | **Claim:** C-WEB-DYNAMICS | **Date:** 2026-09-16  
**Experiment ID:** EXP-FRONTIER-34913743596 | **Status:** COMPLETE | **Outcome:** FALSIFIES | **Decision:** FALSIFIED-IN-SETTING  
**Parent:** EXP-FRONTIER-34881708619 (handoff a6c93705…) | **Base SHA:** 9402f59f23276c65b0cd314d8873cdae9eb6e07d

---

## 1. Executive Summary

Frozen binned TV per-type estimation at 250/type (0.625 expected counts/bin on 20×20 grid) fails null control (4/8 types >0.01) and CV (max 1.59) across three consecutive Frontier experiments. This experiment tests whether the failure is **estimator-specific** (fixed-grid binning artifact) or **general** to per-type estimation at 250/type by evaluating two orthogonal continuous estimators that do not bin:

* **KDE max KL** — Gaussian kernel, Scott bandwidth, `max_a D_KL(P(S|A=a) || P(S))` with permutation bias correction
* **kNN mutual information** — Kraskov et al. digamma estimator, k=5, via `cKDTree`

On **identical DGP/seeds/page types** as parents (8 heterogeneous 2D [0,1]² dynamics, 2000 transitions per lambda, 250 per type × 8 types, 5 replications, 8 lambdas, N=200 permutations per type), both alternatives **pass per-type null control (8/8)** where binned TV fails, demonstrating the sparse-binning false-positive is estimator-specific.  Both **fail the frozen CV ≤0.5 check at lambda=1** (KDE max 0.574 on type 4, kNN max 0.755 on type 0 → 7/8 pass, 1/8 fail each), triggering **FALSIFIED-IN-SETTING** per frozen decision rule.  Positive controls pass strongly (KDE t=7.81 p=0.0007, kNN t=6.82 p=0.0012), so the CV failure is a **valid scientific negative on stability**, not measurement invalidity.  Binned TV replication passes (0.0343 vs parent 0.034).

**Product consequence (negative):** Density-divergence approach remains fundamentally limited for heterogeneous data at 250/type – even binning-free estimators cannot achieve stable (CV ≤0.5) per-type estimation on all 8 types.  Pooled estimation may be required at this sample size; per-type deployment at 250/type is not justified without larger n or tuned hyper-parameters (k=10 exploratory needs new preregistration).

---

## 2. Scientific Question and Hypotheses

**Frozen question (spec.json):** Do alternative divergence measures (KDE with cross-validated bandwidth, kNN MI) maintain per-type null control and low CV at equal per-type n (250/type) where binned TV fails due to sparse binning (0.625 expected counts/bin)?

* **H1 (per-type null control):** KDE and kNN achieve `observed_raw ≤ 95th percentile perm threshold` at lambda=0 for all 8 types.
* **H2 (positive control):** Pooled subsampled divergence at lambda=1 > at lambda=0 (detectable signal) for both measures.
* **H3 (low CV):** Per-type BC divergence at lambda=1 has CV ≤0.5 across 5 replications for all 8 types.
* **H4 (improvement over binned TV):** At least one alternative achieves both H1 and H3 while binned TV fails both (null 4/8 fail, CV max 1.59).

**Falsifier (spec.json):** Either measure fails per-type null control (any type > threshold at lambda=0) **OR** CV >0.5 at lambda=1 for any type.

---

## 3. Methods (Frozen, Per Prereg)

### 3.1 DGP — Identical to Parents

* 8 page types: (rotation/scaling/translation) × (σ 0.05/0.10) × (centers [0.5,0.5]/[0.3,0.7]) — same `THETA, OFFSET_A, SCALE, OFFSET_B, T_C, ALPHA_C`
* Heteroscedastic Gaussian noise `σ(s)=σ_base·(1+0.5·‖s−center‖)`, clipped to [0,1]²
* Deterministic block-cycling `type = (transition_index // 250) mod 8` (250 per type per lambda)
* 8 lambdas [0.0,0.1,0.2,0.3,0.4,0.5,0.7,1.0], 5 replications per lambda, total 80,000 non-stationary transitions
* Seeds: `cell_seed = 42·100000 + lambda_idx·1000 + rep_idx·10 + 999`; subsampling `seed+pt·100+888` (250 per type deterministic), permutation seeds `+6000/+7000/+777/+666`
* Reuse verification: pooled-sub Spearman and per-type means replicate parents within tolerance

### 3.2 Measures

**KDE divergence (per-type and pooled-sub):** `scipy.stats.gaussian_kde` Scott bandwidth on continuous 2D `S_{t+1}`; `max_a D_KL(P(S|A=a) || P(S))` evaluated as `mean(log p_cond – log p_marg)` on conditional samples; BC = `max(0, observed – perm_mean)`; permutation null N=200 shuffling action labels within type (or pooled).

**kNN MI (per-type and pooled-sub):** Kraskov MI (`digamma(k)+digamma(n)−mean(digamma(n_x+1)+digamma(n_y+1))`) with `k=5`, `p=∞`, joint scaling `y/3`, `cKDTree`; same permutation scheme; BC likewise.

**Binned TV reference:** 20×20 grid TV `0.5·Σ|p−q|` max across action pairs, N=200 per type — **reference only**, not primary.

### 3.3 Controls and Decision Rule (Frozen)

* **Positive control:** Pooled-sub BC at lambda=1 > at lambda=0 (one-sided paired t across 5 reps p<0.05). Fails → `MEASUREMENT_INVALID`.
* **Null control:** Per-type observed_raw ≤ 95th percentile perm threshold at lambda=0 for all 8 types (both KDE and kNN). Fails → `FALSIFIED-IN-SETTING`.
* **CV control:** CV ≤0.5 for all 8 types at lambda=1 (both). Fails → `FALSIFIED-IN-SETTING`.
* **BC replication:** Binned TV per-type mean at lambda=1 within 0.01 of parent 0.034 → verifies pipeline.
* **SURVIVES_CURRENT_TEST** requires *all* of (KDE null pass, kNN null pass, KDE CV pass, kNN CV pass, positive pass, no errors). Else `FALSIFIED-IN-SETTING`; pipeline error → `MEASUREMENT_INVALID`.

---

## 4. Results — Raw Evidence, Observations, Measurements

### 4.1 Raw Evidence

* Optimized confirmatory execution log: `execute_log.txt` (SHA a3374507…, 1488.4s) — 8 lambdas, 5 reps, 200 perms, Kraskov k=5 + Scott KDE
* Exploratory sensitivity log: `sensitivity_log.txt` (523.7s, run_sensitivity.py) + `sensitivity_exploratory.json` (c1497e03…) — labeled EXPLORATORY per prereg §14
* On-disk legacy `run_execute.py` (785b9337…) preserved but **not** source of confirmatory result (fixed 0.5 threshold bug vs spec 95th percentile; see provenance notes)
* Provenance: `provenance.json` (hashes, env Python 3.12.14 numpy 2.5.3 scipy 1.18.1 sklearn 1.9.1)

### 4.2 Observations (Direct, Not Interpreted)

* Pooled-sub KDE BC: 0.0023 (lam0, obs 0.0158) → 0.0644 (lam1, obs 0.0647)
* Pooled-sub kNN BC: 0.0017 (lam0, obs 0.0037) → 0.0567 (lam1, obs 0.0714)
* Per-type mean BC across 8 types: KDE 0.0119→0.1827, kNN 0.0040→0.1382 (both monotonic lambda scaling descriptively)
* KDE null at lam0 raw vs 95th: type-wise (0.136 vs 0.196, 0.099 vs 0.206, 0.151 vs 0.196, 0.140 vs 0.196, 0.134 vs 0.201, 0.141 vs 0.204, 0.105 vs 0.202, 0.133 vs 0.193) → 8/8 pass
* kNN null at lam0 raw vs 95th: (0.007 vs 0.051, 0.006 vs 0.050, 0.020 vs 0.051, 0.013 vs 0.046, 0.007 vs 0.053, 0.001 vs 0.048, 0.006 vs 0.050, 0.003 vs 0.050) → 8/8 pass
* KDE CV at lam1 per type: [0.302,0.397,0.132,0.402,**0.575**,0.280,0.196,0.288] max 0.574 → 7/8 pass
* kNN CV at lam1 per type: [**0.755**,0.321,0.211,0.189,0.423,0.436,0.116,0.159] max 0.755 → 7/8 pass
* Positive t-tests: KDE t=7.81 p=0.0007, kNN t=6.82 p=0.0012 → both pass
* Binned TV replication: mean 0.0343 diff 0.0003 from parent 0.034 PASS; CV max 1.59 replicated; null 4/8 fail replicated

### 4.3 Derived Measurements (result.json:metrics)

* **KDE:** pooled 0.0644 lam1 > 0.0023 lam0 Δ=0.0621; per-type mean 0.1827 vs pooled 0.0644 ratio pooled/per-type 0.35× (per-type **exceeds** pooled)
* **kNN:** pooled 0.0567 lam1 > 0.0017 lam0 Δ=0.055; per-type mean 0.1382 vs pooled 0.0567 ratio 0.41× (per-type **exceeds** pooled) — opposite to binned TV pooled 1.49× > per-type
* **KDE null** 8/8 pass (vs binned 4/8 fail) → sparse-binning false positive is estimator-specific
* **kNN null** 8/8 pass (vs binned 4/8 fail) → same conclusion
* **CV:** KDE max 0.574 >0.5 (type 4 scaling_high 0.5,0.5), kNN max 0.755 >0.5 (type 0 rotation_low 0.5,0.5) → violates frozen rule
* **Sensitivity exploratory (cannot support confirmatory claims):** kNN k=3 null 8/8 CV fail max 0.612, k=10 null 8/8 CV **pass** max 0.470 (8/8), KDE LOOCV null 8/8 CV fail max 0.800. See `sensitivity_exploratory.json`.

---

## 5. Controls — Pass/Fail

| Control | Expected | Observed | Pass | Evidence |
|---|---|---|---|---|
| `kde_positive_control` | pooled BC lam1 > lam0 | 0.0644 > 0.0023 t7.81 p0.0007 | **PASS** | execute_log:23 |
| `knn_positive_control` | pooled BC lam1 > lam0 | 0.0567 > 0.0017 t6.82 p0.0012 | **PASS** | execute_log:24 |
| `positive_control` (both) | both pass | KDE PASS, kNN PASS | **PASS** | — |
| `kde_null_control` | 8/8 raw ≤ 95th at lam0 | 8/8 (max 0.151 ≤ 0.193–0.206) | **PASS** | execute_log:21 |
| `knn_null_control` | 8/8 raw ≤ 95th at lam0 | 8/8 (max 0.020 ≤ 0.046–0.053) | **PASS** | execute_log:22 |
| `null_control` (both) | both 8/8 | KDE 8/8, kNN 8/8 | **PASS** | — |
| `kde_cv_check` | max CV ≤0.5 lam1 | max 0.574 type4 fail (7/8) | **FAIL** | execute_log:25 |
| `knn_cv_check` | max CV ≤0.5 lam1 | max 0.755 type0 fail (7/8) | **FAIL** | execute_log:26 |
| `cv_check` (both) | both ≤0.5 | KDE fail, kNN fail | **FAIL** | — |
| `bc_replication` | |recomputed−0.034|<0.01 | 0.0343 diff 0.0003 | **PASS** | execute_log:27 |
| `no_pipeline_errors` | no exception | 1488.4s 80k trans | **PASS** | — |

Binned TV comparator (reference): null 4/8 fail, CV max 1.59 — substantially worse than KDE/kNN but those still violate 0.5.

---

## 6. Validity Notes and Threats

* DGP synthetic 2D [0,1]² with toy affine families + heteroscedastic Gaussian; no inference to real Web DOM (synthetic-to-real gap remains dominant).
* Deterministic block-cycling every 250 i.i.d. draws operationalizes non-stationarity narrowly; not representative of real page-type switching (see handoff do_not_assume).
* n=250 per type is small for density estimation even without binning; KDE/kNN variance remains high → CV fails despite null passes. Sample-size question (500–2000/type) is orthogonal and unresolved.
* On-disk `run_execute.py` uses fixed 0.5 threshold + simplified neighbor-count kNN, **not spec-compliant**; confirmatory result comes from optimized Kraskov+Scott execution (execute_log). Preserved for audit transparency.
* kNN mitigates binning but introduces its own scale: `y/3` joint scaling and `p=∞` tree metric are implementation choices; KDE Scott vs LOOCV bandwidth choice matters (LOOCV CV max 0.800 > Scott 0.574 in exploratory).
* CV threshold 0.5 is preregistered and strict; KDE 0.574 is only marginally over (type 4 scaling_high), kNN 0.755 more substantially (type 0 rotation_low). Marginal fail still = FALSIFIED per frozen rule.
* Pooled vs per-type ordering reversal (KDE/kNN per-type > pooled vs binned pooled > per-type) indicates estimator-specific geometry, not universal pooled advantage. The 1.49× pooled advantage in binned TV confounds 5.0 vs 0.625 counts/bin; continuous estimators remove that confound and invert the ratio.
* Absolute magnitudes: KDE per-type 0.182 nats and kNN 0.138 nats at lam1 are below marginal frequency baseline 0.335 for binned TV but not directly comparable across divergence units; pooled KDE 0.064 nats is below per-type, suggesting per-type signal is detectable but unstable.
* Exploratory k=10 pass (max 0.470) is **not confirmatory** (prereg §14 deviation policy); requires new preregistration before claiming.

---

## 7. Interpretation

* **Per-type limitation is partly estimator-specific:** The binned TV false-positive (4/8 null fail) is **dissolved** by binning-free estimators — both KDE and kNN achieve 8/8 null control at same 250/type. This supports the auditor-identified sparse-binning artifact (0.625 expected counts/bin) as the cause of binned TV null failure.
* **Per-type limitation is not fully dissolved:** The stability limitation (CV >0.5) **persists** for both KDE and kNN at 250/type, though attenuated (max 0.57/0.75 vs 1.59). The frozen rule requires CV ≤0.5 for *all* types; one failing type suffices to falsify. This indicates per-type estimation at 250/type remains fundamentally noisy even without binning — the limitation generalizes beyond binning to sample-size / heterogeneity.
* **No measurement invalidity:** Positive controls pass with large effects (Cohen-like t >6), replication passes, no errors → `status=COMPLETE` with `outcome=FALSIFIES` is a valid scientific negative, not infrastructure failure.
* **H4 not supported:** No alternative achieves *both* null pass and CV ≤0.5, so improvement over binned TV is partial (null only) not full.

---

## 8. Decision and Consequences

**Frozen decision_rule application:**
* Positive PASS (both), Null PASS (both), CV FAIL (both → at least one type >0.5), BC replication PASS → `measurement_invalid = False`; `null_control_pass and cv_pass = False` → **FALSIFIED-IN-SETTING**.

**Product consequences — negative:**
* Per-type density-divergence at 250/type cannot be used with current estimators (KDE Scott, kNN k=5) under frozen stability criterion. Pooled estimation remains required even with alternative estimators.
* The binned TV sparse-binning diagnosis is validated (null now passes), so the recommendation to not repeat binned TV stands, but the alternative-measure path does not yet salvage per-type stability.
* `k=10` exploratory pass is hypothesis-generating; product should **not** deploy per-type k=10 without new confirmatory preregistration and cost analysis (no browser/network/model calls in this lane, but KDE/kNN compute ~1.5k seconds per full sweep).

**Scientific handoff:**
* Established: KDE/kNN remove binned false positives (8/8 null pass) and reduce CV vs binned but not below 0.5; pooled > per-type ordering is estimator-dependent.
* Rejected: Hypothesis that binned TV per-type limitation is *solely* binning and that KDE/kNN automatically achieve CV ≤0.5 at 250/type.
* Unknown: k=10 confirmatory, larger n (500–2000/type), equal-total-n design, stochastic page-type switching, real Web DOM detectability.
* Do not assume: C-WEB-DYNAMICS falsified (still synthetic), pooled advantage is universal, sparse results generalize to denser regimes, or real-data justification from rank correlation alone (absolute magnitudes far below baseline in binned case).

---

## 9. Reproduction and Artifacts

* **Confirmatory raw:** `execute_log.txt` (a3374507…, 1488.4s, 80k transitions, Kraskov k=5 + Scott)
* **Exploratory:** `sensitivity_exploratory.json` (c1497e03…, 523.7s) + `sensitivity_log.txt` (a2c2bcc7…)
* **Code:** `run_execute.py` (785b9337…, legacy) + `run_sensitivity.py` (9bb48ff7…, Kraskov+LOOCV)
* **Fixtures:** `spec.json` (3cdb3643…), `prereg.md` (3649dffc…), `request.json` (b8432077…), `freeze.json` (4a5b34b7…)
* **Derived:** `result.json` (1ca449f5…, 18k), `provenance.json` (7.5k), this `report.md`
* **Repro command (optimized logic):** See `provenance.json:reproduction` — generate_transitions_nonstationary with BASE_SEED 42, same PAGE_TYPES, seeds, 200 perms, Kraskov digamma (run_sensitivity.py:86-108) and gaussian_kde Scott

---

## 10. References to Packet Fields

* `spec.json:question, hypothesis, falsifier, decision_rule, baselines, positive_control, null_control, measurement_validity`
* `prereg.md:7.1-7.4 statistical tests, 8.1-8.4 controls, 9.1-9.2 validity threats, 10.1-10.3 decision rules`
* `result.json:metrics.pooled_subsampled_kde, metrics.pooled_subsampled_knn, metrics.kde_per_type, metrics.knn_per_type, metrics.bc_tv_reference, controls.kde_null_control, controls.knn_null_control, controls.kde_cv_check, controls.knn_cv_check, controls.positive_control, controls.bc_replication`
* `provenance.json:method, execution_time_seconds, script_hashes, environment`
* Parent `EXP-FRONTIER-34881708619/handoff.json:carry_forward, evidence_refs, recommended_action`

*Report does not contradict result.json; any deviation from prereg is labeled EXPLORATORY per §14.*
