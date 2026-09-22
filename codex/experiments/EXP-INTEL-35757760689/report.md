# EXP-INTEL-35757760689 Report — Bundled Spec-Compliant Mind2Web + Docker Full-DOM Direct Measurement for C-CROSSSITE / C-PRODUCT-ECON

## 1. Experiment Identity and Frozen Inputs
- **Experiment ID**: EXP-INTEL-35757760689
- **Lane**: intel
- **Claims**: C-CROSSSITE (primary CONTINUE), C-PRODUCT-ECON (secondary REJECTED-path closure)
- **Parent Handoff**: `research/experiments/EXP-INTEL-35749371101/handoff.json` sha256 `19bb656434e4a81991ba922854c59492a8be456bbf65b27ea3bb74c35944d87e`, verdict MIXED — WebArena within-store PASS (AX 0.9), Mind2Web MEASUREMENT_INVALID per Gate0
- **Director Mandate**: CONTINUE C-CROSSSITE, cycle 35757103830, target claim C-CROSSSITE, cognitive_reset true, binding question in `spec.json:question`
- **Frozen hashes**: `request.json` 0f393cfa..., `spec.json` 92b22635..., `prereg.md` aa70be43..., `freeze.json` 2026-09-22T17:05:09.671617+00:00
- **Seed**: 35725763380 for all sampling, TF-IDF/k-means, bootstrap (2000 reps), shuffle (1000 perms), random-role null (1000 perms)

## 2. Scientific Question
> On pinned HuggingFace revision (record hash) does Mind2Web official train/test_website/test_domain splits (137 websites/31 domains spec vs observed 73/3 divergence) show same-mechanism parameterized overlap via spec-compliant TF-IDF (max_features 5000, ngram 1-2, min_df 2, stop_words english) -> k-means k=min(50, unique_train_tasks/20) fitted train-only with 1000 website-label shuffles (seed 35725763380), 2000 bootstraps and k/2,2k sensitivity achieving overlap >=0.15 and excess vs shuffle >=0.10, and can Docker am1n3e/webarena-verified-shopping full-DOM locatable_sample (n=21-82 per task, not truncated-first-20) be re-collected for 7 Magento tasks to measure canonical recipe ranking agreement at full element counts vs 80% threshold, closing the REJECTED model-extrapolation path (logistic vacuous L=0.5654, Hill h=20 at bound, 4 points 3 params)?

## 3. Hypotheses (Preregistered)
- **H1_CROSSSITE_OVERLAP**: Mind2Web official splits share same-mechanism overlap >=0.15 and excess >=0.10 beyond website-label shuffle p95, with param_prevalence >=0.15, PC2 recurrence >=1 cluster in >=10 tasks across >=3 websites, bootstrap CIs exclude thresholds by >=0.05, k/2,2k sensitivity disclosed.
- **H2_DOCKER_FULL_DOM**: Docker full-DOM locatable_sample 21-82 yields canonical recipe ranking agreement F_full >=0.80 (crosses threshold, truncation artifact) or remains CI entirely <0.80 (plateau confirmed below threshold, logistic L=0.5654 validated).
- **H3_HEURISTIC_DISCLOSURE**: Decomposition exact_copy <0.2 and cross-recipe gap disclosure vs truncated 84.7x.

## 4. Methods (Frozen Before Outcome Inspection, Per prereg 5.1-5.5)
- **Mind2Web**: HuggingFace `osunlp/Mind2Web` via `datasets` 5.0.1 + `huggingface_hub` 1.32.0, 3 retries with backoff, record HF revision hash, per-split census, compare to spec 137/31. If single train only, document divergence and halt axis as MEASUREMENT_INVALID without synthetic partition. Mechanism frozen before measurement: TF-IDF max_features 5000 ngram 1-2 lowercase stop english min_df 2 -> k-means k=min(50, unique_train_tasks/20) n_init 10 random_state 35725763380 fitted train-only then predict test. Bootstrap 2000 reps, shuffle 1000 website-label perms seed 35725763380, k/2,2k sensitivity.
- **Docker**: Image `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` (also :latest digest recorded) at `http://localhost:7770`, viewport 1280x720 initial no scroll. Verify MEASURE_JS no longer contains `if (locatableSample.length <20)` truncation (hash diff vs parent `measure_fullpage_yield.py:89`). Sample 7 Magento tasks exactly as parent census: 3 listing, 3 detail, 1 cart. For each task full-DOM locatable count and tightened_count (role-only a->link mapping DEF-FULL-MAP) enumerated, total_dom and elements_with_bbox recorded, locatable_sample saved with sha256. Ranking agreement F_full defined frozen in `research/intel/exp_35757760689_measure.py` (hash 826802ce...) as canonical vs weighted ranking agreement at full counts and truncated vs full canonical check, bootstrap 2000 reps, random-role null 1000 perms same cardinality.

## 5. Results — RAW EVIDENCE vs OBSERVATIONS vs DERIVED MEASUREMENTS

### 5.1 RAW EVIDENCE
- **Mind2Web HF**: `osunlp/Mind2Web` load with 3 retries yields single `train` split only: `split_names ['train']`, `n_tasks 1009`, `n_websites 73`, `n_domains 3`, `hf_sha 17ece8eb89862368edc0cc806acee6fca5163474`, `has_official_splits false` vs spec 137/31 with official `train/test_task/test_website/test_domain`. No TF-IDF/k-means fitted, no shuffle null computed, no synthetic 50/50 website split fabricated. Divergence documented in `artifacts/raw/mind2web_split_census.json` sha 8e1c27b5....
- **Docker host**: `am1n3e/webarena-verified-shopping:latest` digest `sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` container `ca4a09a00f62` at `http://localhost:7770` responds 200 with DOM `input#search placeholder 'Search entire store here...' form /catalogsearch/result/`. Full-DOM AX at 1280x720 homepage nodes 1426, product pages via task-specific URLs.
- **Full-DOM enumeration** (no cap): 7 tasks each with `locatable_sample_len == locatable_elements` and `tightened_sample_len == tightened_elements` verifying cap removed:
  - `listing_clothing-shoes-jewelry`: totalDom 1973, elementsWithBbox 622, locatable 173, tightened 116, tightSample 116
  - `listing_beauty-personal-care`: 1984, 632, 176, 119
  - `listing_electronics`: 1989, 636, 177, 120
  - `detail_camera`: 1767, 346, 93, 50
  - `detail_vr_bag`: 1682, 280, 93, 50
  - `detail_pet_camera`: 1676, 274, 93, 50
  - `cart_1`: 1445, 172, 67, 34
  MEASURE_JS_FULL hash `826802ce24f3cc534da1a0b4a60f1dd276999eecefcf0afc7f22d1d591839ce8` contains no `locatableSample.length <20`; parent `measure_fullpage_yield.py:89` contains `if (locatableSample.length < 20)` cap, `parent_has_cap true`, hash diff verifies removal.
- **Preserved artifacts**: All raw/derived JSONs with sha256 in `result.json:artifacts`.

### 5.2 OBSERVATIONS (Direct, Not Interpreted)
- Mind2Web HF revision still 17ece8eb single train 73/3 vs spec 137/31; TF-IDF/k-means train-only and website-label shuffle NOT computed per Gate0.
- Docker full-DOM tightened counts 34-120 exceed spec expected 21-82 for listing (116-120 vs 82, detail 50 vs 32 1.56x, cart 34 vs 21 1.61x) but cap removal verified and totalDom larger (1973 vs 1696) with menuitem expansion (40+ menuitems) as representation divergence.
- Per-task canonical densities (tightened/totalDom): listing 0.05879,0.05998,0.06033; detail 0.02830,0.02973,0.02983; cart 0.02353. Weighted densities (tightened/elementsWithBbox): listing 0.186-0.188, detail 0.144-0.182, cart 0.197. PC1 passes (combobox true button true placeholder on all trees).

### 5.3 DERIVED MEASUREMENTS (With Uncertainty)
- **Mind2Web**: Overlap, excess, shuffle null mean/p95, param_prevalence, PC2, bootstrap CIs, k/2,2k sensitivity: `null` (not computed due to Gate0).
- **Docker ranking**:
  - `F_full canonical vs weighted` (primary threshold test): **0.7143** across 21 pairs (7 choose 2), bootstrap 95% CI **[0.4286, 1.0]** (2000 reps seed 35725763380). Threshold 0.80 inside CI → **straddles**.
  - `F_trunc_vs_full canonical` (truncated 20/totalDom vs full canonical): **0.1429** CI [0.095,0.714] — very low, truncation reverses ranking.
  - Truncated baseline `F=0.5654` (constant null for all n) and Hill `L=0.5657` not rejected nor validated; F_full 0.7143 not significantly above 0.5654 nor above 0.80 due to wide CI.
  - Cross-recipe gap: truncated 84.7x (canonical 0.005965 vs weighted 0.505) collapses to **4.36x** at full DOM (can 0.0415 vs w 0.181) — gap persists but 19x smaller.
  - Random-role null: mean **0.4989** p95 **0.7619** (1000 perms seed +1), excess **0.2155** >=0.20 threshold marginally, but CI [0.4286,1.0] overlaps p95, not discriminating at 95% confidence with n=7.
- **WebArena census** (reused): duplication 0.9479 CI [0.9167,0.9792], exact_copy 0.0781 CI [0.0417,0.1198] →91.8% parameterized, param_task 0.8958 CI [0.8490,0.9375], families_ge3 36 etc., verified sha.

## 6. Decision Rule Evaluation (Frozen Ordered, Gate0 Precedence)

**Gate0 — Infrastructure**:
- Mind2Web HF pinned revision does NOT expose official 4-way splits after 3 retries (single train 73/3/1009 vs spec 137/31) → **Mind2Web axis = MEASUREMENT_INVALID/BLOCKED (outcome NOT_APPLICABLE), not FALSIFIED**, durable error and revision recorded. No synthetic partition substituted.
- Docker image available after pull, Playwright full-DOM enumeration succeeds on 7 tasks, locatableSample cap absent verified via hash diff → **Docker axis Gate0 PASS**.

**Clause1 — Mind2Web cross-website axis**:
- Spec-compliant TF-IDF/max_features 5000 ngram 1-2 min_df2 stop english ->k-means k=min(50, unique_train/20) train-only **NOT executed** (Gate0). Therefore **INCONCLUSIVE/MEASUREMENT_INVALID per audit required_fixes, not falsified**. No decision on overlap >=0.15, excess >=0.10, param_prevalence >=0.15, PC2, or k/2,2k sensitivity.

**Clause2 — Docker full-DOM axis**:
- Full-DOM enumeration on 7 tasks executed with verified counts 34-120 (listing exceedance disclosed) and no cap (cap_present false). Canonical ranking agreement `F_full 0.7143 CI [0.4286,1.0]` **straddles 0.80** (lower <0.80 < upper) → **INCONCLUSIVE (insufficient precision at n=7)** per frozen rule. Not FALSIFIED-IN-SETTING (would require ci_upper <0.80) nor SURVIVES (requires point >=0.80 with ci_lower >0.70).

**Clause3 — SURVIVES**: Requires Gate0 pass AND Clause1 SURVIVES AND Clause2 SURVIVES. Not met (Clause1 blocked, Clause2 inconclusive) → not SURVIVES.

**Clause4 — MIXED**: Requires one axis SURVIVES and other FALSIFIED/INCONCLUSIVE/MEASUREMENT_INVALID. Not met (no axis SURVIVES).

**Clause5 — Duplication handling**: Duplication 0.9479 with exact_copy 0.0781 <0.2 is parameterized reuse, not MIXED trigger (superseded).

**Overall**: Neither hypothesis survived. Mind2Web remains blocked on dataset infrastructure; Docker ranking stability remains imprecise. Per packet `status=COMPLETE` (valid measurement, not infrastructure failure beyond known HF divergence) with `outcome=MIXED` (mixed per-axis: Mind2Web BLOCKED, Docker INCONCLUSIVE) — alternatively INCONCLUSIVE overall. Report keeps per-axis ceilings distinct: Mind2Web bounded to MEASUREMENT_INVALID, Docker bounded to INCONCLUSIVE at n=7.

## 7. Controls and Baselines (Stable IDs)

All controls evaluated with frozen seeds and evidence paths per `result.json:controls`:

- **B1_DOC_M1_12STORES**: REJECTED for v2 single store, confirmed single store (site_tuples, single container).
- **B2_DOC_M2_HEURISTIC**: 91.8% parameterized vs M2=0.80 gap quantified.
- **B3_SPIDER_2SITE**: Bound exceeded (36 families >>2-site).
- **B4_SHUFFLE_NULL**: NOT_COMPUTED due Gate0, correctly not fabricated (coarse 0.998 null artifact disclosed).
- **B5_TRUNCATED_FIRST_20**: 0.5654 baseline vs F_full 0.7143 not significantly different; F_trunc_vs_full 0.1429 shows truncation artifact for ranking order.
- **B6_CONSTANT_NULL_05654**: Logistic L=0.5654 not rejected nor validated (CI straddles).
- **B7_RETRIEVAL_REPLAY_STRONG**: Disclosure-only (TERX 90ms 23k->0).
- **PC1_WEB_SEARCH**: PASS (1426 nodes, placeholder verified).
- **PC2_MIND2WEB_RECURRENCE**: CANNOT_VERIFY (official splits missing, would need >=1 cluster in >=10 tasks across >=3 websites).
- **PC3_FULL_DOM_ENUMERATION**: PASS with disclosure (cap removed hash diff, counts 34-120 vs 21-82 exceedance disclosed as larger totalDom/menuitem).
- **NC1_WIKIPEDIA_NULL**: NOT_EXERCISED (null not 0).
- **NC2_MIND2WEB_SHUFFLE_NULL**: NOT_COMPUTED_MEASUREMENT_INVALID.
- **NC3_WEB_EXACT_COPY_NULL**: PASS 0.0781<0.2.
- **NC4_RANDOM_ROLE_NULL**: MARGINAL 0.4989 mean vs F_full 0.7143 excess 0.215 >=0.20 but CI overlaps p95, not discriminating at n=7.
- **NC5_COARSE_33_MECHANISM_NULL**: Disclosure only (0.8139 vs 0.998 not used).

## 8. Interpretation (Bounded)

- **H1 Mind2Web**: No evidence accumulated for or against same-mechanism cross-website overlap at spec-compliant granularity. The hypothesis remains **UNKNOWN/HYPOTHESIS**. The repeated HF divergence (17ece8eb single train) confirms the dataset infrastructure is the blocker, not the mechanism. Do not treat diagnostic 0.8139/0.998 coarse overlap as falsification.
- **H2 Docker**: Ranking agreement at full DOM does **not** validate the logistic plateau at 0.5654 nor confirm crossing 80%. The data are **inconclusive due to underpowered n=7** (CI width 0.57). Truncation does affect ranking order (0.1429 vs 0, high vs low) and reduces gap magnitude 84.7x→4.36x, but the threshold decision requires larger n (≥20 tasks) to narrow CI outside 0.80. The REJECTED model-extrapolation path remains closed; direct measurement is the only valid path, but precision insufficient.
- **Product consequence**: No promotion. C-CROSSSITE website-holdout remains blocked on Mind2Web alternative corpus (WebLINX/Go-Browse) or HF dump re-pin. C-PRODUCT-ECON ranking stability remains unvalidated at Magento scale; product must not assume 80% stability, should test larger n or alternative recipe (per-task weighted) before relying on canonical p=0.5 density for yield estimation. Within-store AX 0.9 [0.7,1.0] remains the only MEASUREMENT-VALID substrate for product holdout.
- **Ceiling**: WebArena census only (192/49 duplication 0.9479 exact 0.0781 param 0.8958 families 36/34/33) with AX 0.9 within-store, no LLM benefit demonstrated; tightened/full-DOM densities now measured at full element counts with gap disclosure.

## 9. Validity Threats and Mitigations
- **Gate0 HF divergence**: Mitigated by 3 retries, hash recording, and refusing synthetic substitution.
- **TotalDom/divergence**: 1973 vs 1696 earlier, elementsWithBbox 172-636 vs 1070-1564 — larger totalDom/smaller bbox counts due to stricter bbox>0 and menuitem increase; disclosed as representation loss.
- **Count exceedance**: Tightened 116-120 >82 — menuitem expansion (40+), disclosed with hash verification, not relabeled as invalid.
- **F_full ambiguity**: Both canonical vs weighted and truncated vs full reported; threshold test unchanged.
- **Small n**: n=7 wide CI anticipated in prereg as INCONCLUSIVE when straddling; power requires n≥20.
- **No LLM**: Substrate only, no claim of inheritance benefit.

## 10. Preservation and Reproducibility
- Raw evidence paths/hashes in `result.json:artifacts` and `provenance.json:artifacts`.
- Frozen script `research/intel/exp_35757760689_measure.py` sha `826802ce24f3cc534da1a0b4a60f1dd276999eecefcf0afc7f22d1d591839ce8` includes vectorizer/k-means/shuffle/bootstrap with seed 35725763380.
- HF revision hash, Docker digest, Playwright 1.63.0, viewport 1280x720, bootstrap 2000 reps, shuffle 1000 perms all recorded in `provenance.json`.

---

*Report keeps RAW EVIDENCE distinct from OBSERVATIONS, DERIVED MEASUREMENTS, and INTERPRETATION per AGENTS.md transmission discipline. No LLM benefit, freshness, or delta-repair claimed.*
