# EXP-INTEL-35741921602 Preregistration — Intel 7-Fix Spec-Compliant Remeasurement for C-LLM-INHERIT / C-CROSSSITE

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35741921602
- **Lane**: intel
- **Claims**: C-LLM-INHERIT (primary, allocation claim_id), C-CROSSSITE (secondary diagnostic for website-holdout feasibility)
- **Parent Handoff**: `research/experiments/EXP-INTEL-35725763380/handoff.json`, sha256 `1ff31f803ffec5c110dff97720771c995f1f451a9d340d55de530b20b2d367d0`, verdict `REVISE` (audit REVISE, 7 required_fixes)
- **Director Mandate**: CONTINUE to C-LLM-INHERIT, `request.json` cycle 35741318902, allocation action CONTINUE, target claim C-LLM-INHERIT, parent_handoff_disposition USE, question verbatim in spec.json
- **Date**: 2026-09-22
- **Status**: DESIGN — NOT YET FROZEN (freeze.json will hash spec.json + prereg.md before EXECUTE)

This experiment executes exactly the 7 audit-required fixes from EXP-INTEL-35725763380 audit REVISE and Director strategic question, without inspecting outcome measurements during DESIGN.

## 2. Scientific Question (Binding Director Question, Refined)

> After executing the 7 audit-required fixes — live CDP Accessibility.getFullAXTree at 1280x720 initial viewport 2-per-family for >=15 tasks across >=10 families to measure AX_consistency >=0.6, and spec-compliant Mind2Web TF-IDF->k-means k=min(50,unique_tasks/20) fitted train-only on official train/test_website/test_domain splits (pinned HF revision) with 1000 website-label shuffles seed 35725763380, 2000 bootstraps, k/2 and 2k sensitivity — does WebArena-Verified v2 within-store family hold-out provide identifiable same-mechanism parameterized transfer and does Mind2Web show cross-website overlap exceeding shuffled null by >=0.10 sufficient to unblock website-holdout Product experiment vs cold/retrieval/SPIDER with 0-token replay baseline?

Refinement: DESIGN converts this strategic question into the smallest rigorous falsifiable measurement that can change a claim/product decision: recompute WebArena census for integrity, live-extract >=15 AX trees 2-per-family to compute AX_consistency, and remeasure Mind2Web overlap with frozen TF-IDF/k-means train-only on pinned official splits with proper website-label shuffle, bootstrap CIs and sensitivity. No LLM agents are executed; substrate viability only.

## 3. Motivation and Inherited State

### 3.1 Why This Is Highest Marginal Information

Per Global Research Director portfolio assessment (request.json portfolio_assessment): SPIDER at 224 canonical exps is tunnel-trapped — Graph 30-streak and Runtime 40-streak on C-FRESHNESS/C-MEAS-VALID localhost mocks (r~0.002-0.046, degenerate fingerprint), Physics 42-streak and Frontier 9/10 on C-WEB-DYNAMICS synthetic 2D TV/KDE where only translation detectable (rho 1.0 d9.1, scaling -0.12), C-PRODUCT-ECON REJECTED (6-model logistic vacuous step k=10.75 R2=1.0 identical to null 0.5654), C-RESIDUAL-NOVELTY 0/3 valid, C-DELTA-REPAIR 0 exps, C-SEMANTIC-RESOLVE MIXED, C-CROSSSITE/C-LLM-INHERIT census-only (192 tasks duplication 0.9479 param 0.8958 but AX_consistency null and Mind2Web 33-heuristic non-compliant). Scout brief + Director allocation: highest marginal information is (1) delta-repair via runtime HIT/SWR/SIE substrate, (2) residual-novelty real cost, (3) Intel 7-fix spec-compliant remeasurement to unblock holdout tests, (4) frontier reconstruction vs verbatim replay — not another freshness/PMI replication. This Intel experiment is the blocking dependency for graph/physics/product cross-site and LLM-inherit tests; infrastructure is ready (Playwright/Docker), so marginal info is highest and cost is LOW (no LLM calls).

The 7 fixes are cheaper than an LLM ranking and must be resolved before committing LLM API costs. High duplication 0.9479 does not imply verbatim copying (exact-copy 0.0781) — this experiment discloses that decomposition and adds element-pattern identifiability.

### 3.2 Parent Handoff Continuity — Preserved Four-Way Distinction (request.json inherited_last_verdict)

Parent EXP-INTEL-35725763380 verdict REVISE; handoff USE disposition. We preserve carry_forward exactly and do not silently override Director CONTINUE:

**Established** (must not be re-tested as hypothesis; recomputed for integrity only):
- WebArena-Verified v2 shopping is exactly ONE Magento One Stop Market store (single container am1n3e/webarena-verified-shopping@sha256:3e8cb9b945..., 192 tasks over 49 intent_templates, site_tuples 187 ('shopping',)+5 ('shopping','reddit'), zero shopping_0..11, sha256 d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30) — census 192/49 and bootstrap CIs verified [0.9167,0.9792] exactly (audit recomputed_metrics). This is the narrow ceiling carried forward.
- Within-store quantitative family reuse: duplication 0.9479 (182/192 share template), exact-copy 0.0781 (15/192 identical template AND instantiation_dict, CI [0.0417,0.1198]), so 91.8% of reuse-family tasks are parameterized variants; parameterization prevalence 0.8958 task (172/192, CI [0.8490,0.9375]) and 0.8367 template (41/49) exceeding frozen thresholds (>=0.5, >=0.3, <0.2) and heuristic M2=0.8.
- Hold-out enumeration: 36 families >=3, 34 >=4, 33 >=5 — frozen thresholds families>=3 >=5 and >=4 >=3 met quantitatively, enabling 2-train/1-test hold-out axis on single-store v2 at template-count level.
- Positive controls: PC1_WEB_SEARCH PASS via REUSED parent (homepage AX 1426 nodes task 514 contains combobox 'Search' + button 'Search', input#search placeholder 'Search entire store here...' form /catalogsearch/result/, add-to-cart 87 / wish-list 84 / compare 84 across 10 sampled pages) and PC2_MIND2WEB_RECURRENCE PASS (max cluster 151 >=10 tasks >=3 websites), NC3_WEB_EXACT_COPY_NULL PASS (0.0781 <0.2).
- Documentation M1=1.0 12-store claim remains falsified for v2 (B1 strong falsification) and is a WebArena v1 property; cross-store overlap remains vacuous null not 0.0; duplication high does not imply verbatim copy.

**Rejected** (must not be revived without new evidence):
- WebArena-Verified v2 provides 12 shopping store instances sharing mechanisms (M1=1.0) and enables train-on-N-stores/test-on-held-out-stores design — rejected bounded to v2 dataset.
- High duplication 0.9479 implies verbatim copying — rejected; decomposition shows 91.8% parameterized variation.
- Producer PARTIAL PASS treating AX null as not falsifying — rejected per frozen decision_rule clause 1; missing AX_consistency triggers FALSIFIED-IN-SETTING, infrastructure availability does not convert null to PASS.
- Claim that Mind2Web coarse excess 0.0466 <0.10 demonstrates lack of cross-website sharing — rejected as inference; null was mis-specified and mechanism coarse, so failure is INCONCLUSIVE not falsified.

**Unknown** (this experiment directly targets):
- Whether same intent_template maps to same AX element pattern across tasks of same family (AX_consistency >=0.6) — requires live CDP 2-per-family re-extraction (audit critical, unresolved[0]).
- Whether Mind2Web official splits with frozen TF-IDF/k-means provide measurable overlap exceeding shuffled null by >=0.10 with pinned revision (spec 137/31 vs observed 73/3 divergence, spec-compliant overlap/shuffle null = null, audit unresolved[1][3]).
- Below-fold/post-interaction mechanism coverage (bounded out, initial viewport only).
- Whether within-store hold-out yields LLM benefit vs cold/retrieval/SPIDER with 0-token replay — out of scope, C-LLM-INHERIT remains EXPERIMENTAL pending Product.
- Whether authenticated ghcr.io multi-store images would show cross-store sharing — blocked on auth.
- True Mind2Web parameterization gap to heuristic M2=0.65 under fine-grained clustering.

**Do_not_assume** (explicitly guarded):
- AX_consistency=null does not demonstrate identifiability or justify Product hold-out beyond census — frozen clause 1 remains FALSIFIED-IN-SETTING until live 2-per-family verification.
- Mind2Web excess 0.0466 on coarse heuristic synthetic partition does not falsify C-CROSSSITE — measurement used 33 mechanisms and synthetic 60/40 shuffle vs official splits, high null reflects label frequency not website identity.
- Duplication 0.9479 or param 0.8958 or PC1/PC2 PASS does not demonstrate LLM benefit, retrieval advantage, or checkout execution — no agents executed here.
- 73/3 Mind2Web census is not 137/31 spec; 60/40 synthetic partition does not approximate official splits; coarse shuffled null mean 0.6942 is not frozen B4 website-label shuffle null.

### 3.3 What This Experiment Is and Is Not

**Is**: A 7-fix repair that (1) live-extracts CDP Accessibility.getFullAXTree at 1280x720 initial viewport for >=15 tasks 2-per-family across >=10 families to compute AX_consistency >=0.6, and (2) remeasures Mind2Web cross-website overlap with frozen TF-IDF->k-means k=min(50,unique_tasks/20) fitted train-only on pinned official train/test_website/test_domain splits with 1000 website-label shuffles seed 35725763380, 2000 bootstraps, k/2 and 2k sensitivity. It recomputes WebArena census for integrity and evaluates frozen decision_rule strictly. It is the smallest high-information experiment that can change the Product unblock decision.

**Is not**: An LLM agent inheritance test (no cold vs retrieval vs SPIDER execution), not a browser end-to-end cart/checkout flow, not a re-tuning of viewport heuristics, not a repetition of 12-store cross-site question on v2 (already impossible), not a synthetic DGP, not a documentation survey. It does not claim freshness, delta-repair, or product economics beyond substrate viability.

## 4. Hypotheses (Falsifiable, Directional)

### H1_WEB_HOLDOUT — Within-store family hold-out is identifiable same-mechanism

Operational: intent_template defines mechanism. Same-mechanism parameterized transfer is identifiable iff quantitative thresholds hold (family_reuse >=0.5, param_task >=0.3, exact_copy <0.2, families_ge3 >=5, families_ge4 >=3) AND element-pattern identifiability holds (AX_consistency >=0.6 on live CDP trees). Expected: quantitative thresholds will replicate parent (0.9479, 0.8958, 0.0781, 36/34 families) — likely PASS — but AX_consistency is uncertain and is the falsifier; previous 10 REUSED trees 1-per-family could not test it, so this measurement decides viability beyond census.

### H2_WEB_AX_CONSISTENCY — Same template -> same element pattern

AX_consistency = fraction of sampled families where both tasks' AX trees contain the template-required element pattern at initial viewport. Pre-registered mapping table (search->combobox+button, add-to-cart->button 'Add to Cart', wish-list->link 'Add to Wish List', reviews->region 'Reviews', search+filter->combobox+filter controls, etc., frozen in code). Threshold >=0.6. Expected direction uncertain — homepage PC1 suggests search pattern present, but within-family consistency across parameterized variants (e.g., 'Search for {{product}}' with different products) must be measured live.

### H3_MIND2WEB_OVERLAP — Cross-website splits share mechanisms under fine-grained clustering

Mechanism = TF-IDF->k-means cluster label fitted train-only (k as above). Overlap = |M_test_website ∩ M_train| / |M_test_website| >=0.15 and exceeds website-label shuffle null mean by >=0.10 and exceeds p95. Expected direction uncertain — heuristic M2 inflated and coarse 33-mechanism clustering gave 0.7407 vs null 0.6942 excess 0.0466 (INCONCLUSIVE); fine-grained TF-IDF/k-means may lower both true and null, but excess threshold tests genuine website sharing. k/2 and 2k sensitivity will disclose granularity dependence. Parameterization prevalence (TYPE/SELECT with variable value) >=0.15.

### H4_HEURISTIC_DISCLOSURE — Parameterization vs copy decomposition

Measured WebArena duplication 0.9479 will again decompose to exact-copy <0.2 (parameterized reuse 91.8%), disclosing heuristic M2 inflation. Mind2Web fine-grained param prevalence will be reported with gap to heuristic 0.65 and duplication fraction with clustering sensitivity.

## 5. Methods

### 5.1 Datasets and Pinning

- **WebArena-Verified v2**: `research/experiments/EXP-INTEL-35725763380/artifacts/raw/webarena-verified.json` from ServiceNow/WebArena-Verified commit `ef74e1bfd0d83d4bab1c55b2d1b4c2aeaac8e0d0`, sha256 `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` (812 tasks). Verify 192 shopping tasks / 49 templates; also verify `test.raw.json` (812/192) and `webarena-verified-hard.json` (258/61) for consistency. Any sha divergence is reported, not silently substituted.
- **Mind2Web**: HuggingFace `osunlp/Mind2Web` (canonical NeurIPS 2023) via `datasets` library. MUST record HF revision hash (`dataset_info` or git log), download date, and per-split census train/test_task/test_website/test_domain. Attempt `load_dataset('osunlp/Mind2Web', revision=<pinned>)` and `load_dataset('osunlp/Mind2Web', data_files=...)` or official `data/*.json` splits. If HF exposes only single split `train` (as parent 1009 tasks 73 websites 3 domains), document divergence to spec 137/31, record revision, and report Mind2Web axis as MEASUREMENT_INVALID/INCONCLUSIVE — do NOT synthesize splits. 3 retries with exponential backoff; durable error on failure.

If Mind2Web HF unreachable after 3 retries, record BLOCKED with HTTP status/timestamp and do not fall back to documentation.

### 5.2 Mechanism Definitions (Frozen Before Measurement)

- **WebArena mechanism**: `intent_template` string verbatim (e.g., `Search for {{product}}`). Parameterization = `instantiation_dict` non-empty (task-level) or template has ≥2 distinct instantiations across tasks (template-level). Exact-copy = identical (template AND instantiation_dict) appearing ≥2.
- **Mind2Web mechanism**: Normalized operation-template cluster = TF-IDF on concatenated `(task instruction + action target text + candidate element text)` -> k-means. Frozen: TF-IDF max_features 5000, ngram_range (1,2), lowercase true, stop_words english, min_df 2; k = min(50, n_unique_train_tasks / 20) where n_unique_train_tasks = distinct task strings in train; k-means n_init 10, random_state 35725763380, fitted on train only, then applied to test splits via same vectorizer/centroids (predict). No test leakage. Fallback if unstable (n_samples < k or empty clusters or silhouette <0.05): exact `(action_type, verb_lemma)` bigram with disclosure, still report k/2 and 2k sensitivity as exploratory. Cluster count sensitivity: report overlap for k, k/2, 2k.

Definitions frozen in `research/intel/exp_35741921602_measure.py` before any metric is computed; file sha recorded in provenance.json.

### 5.3 WebArena Census and Hold-out Enumeration (Integrity Check)

1. Parse webarena-verified.json, filter site tuple containing shopping, count tasks, distinct intent_templates, per-template task counts.
2. Compute: duplication_fraction = tasks whose template appears >=2 / total; exact_copy_fraction = tasks with identical (template, instantiation_dict) appearing >=2 / total; param fractions task/template; family sizes histogram; families_ge3, ge4, ge5; usable hold-out families list.
3. Bootstrap 95% CIs (2000 reps, seed 35725763380) for duplication, exact-copy, param, family-reuse.

### 5.4 Accessibility-Tree Live Verification — The Critical Fix (Audit 1,7)

- **Sampling**: Stratified 15-20 tasks across >=10 families, exactly 2 tasks per family where family size >=2, using frozen seed 35725763380. Prefer families with >=3 tasks (hold-out realism) and cover diverse mechanisms (search, add-to-cart, wish-list, reviews, cart). Sampling code frozen before extraction; list of task_ids pre-registered in derived artifact.
- **Live extraction**: Run `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` at `http://localhost:7770` (Docker). For each sampled task's start URL, use Playwright CDP `Accessibility.getFullAXTree` at **1280x720 initial viewport, no scroll, no cart/checkout execution**. Save raw AX JSON with sha256, node count, viewport metadata, task_id, intent_template, extraction timestamp. Requires `npx playwright install chromium` (record playwright_installed true, docker_available true, image digest).
- **AX consistency**: For each sampled family with 2 tasks, check whether both AX trees contain the template-required element pattern per pre-registered mapping table (frozen dict: e.g., `Search for*` -> combobox 'Search' + button 'Search'; `Add {{product}} to cart` -> button role 'Add to Cart'; `Add {{product}} to wish list` -> link 'Add to Wish List'; `Review *` -> region 'Reviews'; etc.). Consistency = families passing / families sampled. Manual inspection of 3 families for sanity. Threshold >=0.6.
- **Failure handling**: If Docker pull fails or Playwright not installable after 3 retries, record durable error, set ax_consistency = null, provenance playwright_installed false, and evaluate Clause 1 as FALSIFIED-IN-SETTING per frozen rule — do not treat as PASS. Below-fold/post-interaction explicitly excluded and disclosed.

### 5.5 Mind2Web Cross-Website Overlap — Spec-Compliant Remeasurement (Audit 2-6)

1. Load Mind2Web HF pinned revision, enumerate official splits, verify task counts per split and website/domain counts. Record revision hash/date. If only single split available, document divergence and halt Mind2Web axis as MEASUREMENT_INVALID (do not fabricate).
2. Extract mechanism label per task via frozen TF-IDF/k-means (train-only fit). For each task, derive mechanism set (1 label per task = cluster of first action's TF-IDF vector; for multi-step tasks, majority label across actions is exploratory diagnostic but primary is first-action to avoid multi-label ambiguity — pre-registered).
3. Compute: overlap_website = |M_test_website ∩ M_train| / |M_test_website|; similarly test_domain and test_task (diagnostic). Also duplication_fraction (tasks sharing same cluster / total) and parameterization_prevalence (tasks with TYPE/SELECT containing variable value / total) per split.
4. **Website-label shuffle null (audit fix 4)**: Permute website assignment labels across train+test_website task pool 1000 times (seed 35725763380): shuffle website label array, reassign tasks to train/test_website preserving per-split task counts, recompute overlap each perm. Record mean/std/p95. True overlap must exceed mean by >=0.10 and exceed p95. This permutes website identity, not mechanism labels, and keeps split sizes fixed (no random split_point).
5. **Uncertainty**: Bootstrap 95% CIs for overlap and param prevalence (2000 reps, same seed). **Sensitivity**: recompute overlap for k/2 and 2k (same TF-IDF, different k) and report table; primary decision uses k, sensitivity is disclosure.
6. Record TF-IDF vocab hash, k-means centroids hash, cluster count per split.

### 5.6 Controls

- **PC1_WEB_SEARCH** (live): homepage AX at 1280x720 must contain combobox 'Search' + button 'Search' and DOM input#search placeholder 'Search entire store here...' form /catalogsearch/result/. Must PASS on re-extracted live tree; node count ~1150-1426. Failure = measurement error.
- **PC2_MIND2WEB_RECURRENCE**: >=1 TF-IDF/k-means cluster appears in >=10 tasks across >=3 websites in train. Proves recurrence detectable under fine-grained clustering.
- **NC1_WIKIPEDIA_NULL**: guarded Wikipedia Docker check — if container absent, report NOT EXERCISED (null, not 0).
- **NC2_MIND2WEB_SHUFFLE_NULL**: website-label shuffle null per 5.5(4) — true overlap must exceed mean by >=0.10 and p95.
- **NC3_WEB_EXACT_COPY_NULL**: WebArena exact-copy <0.2 distinguishes parameterized reuse from verbatim copy.
- All controls use frozen seed 35725763380 and stable IDs B1-B5/PC1/PC2/NC1-NC3 for audit recomputation.

### 5.7 Artifacts

- `artifacts/raw/webarena-verified.json` (sha d6527566..., hash verification)
- `artifacts/raw/mind2web_split_census.json` (HF revision hash, per-split counts, website/domain counts)
- `artifacts/raw/axtree_web_sample_*.json` (15+ live AX trees at 1280x720, each sha256, viewport metadata) — live-extracted, not REUSED
- `artifacts/derived/measurements.json` (all metrics: webarena census, family histogram, AX_consistency table, Mind2Web overlap per k, bootstrap CIs, shuffle null distribution, TF-IDF/k-means hashes)
- `artifacts/derived/bootstrap_ci.json` (2000 reps, seed, CIs)
- `artifacts/derived/shuffle_null.json` (1000 perms, mean/std/p95, per-perm overlaps)
- `artifacts/derived/tfidf_kmeans_meta.json` (vectorizer params, k, k/2, 2k, vocab hash, centroids hash, cluster counts)
- `research/intel/exp_35741921602_measure.py` (frozen measurement script, sha in provenance.json)
- `provenance.json` (commits, HF revision, Docker digest, playwright_installed, docker_available, seeds, artifact hashes)

## 6. Decision Rule (Frozen, Ordered)

**Gate 0 — Infrastructure**: if WebArena JSON sha mismatch irreconcilable OR Mind2Web HF unavailable after 3 retries OR Mind2Web pinned revision does not expose official train/test_task/test_website/test_domain splits (e.g., 73/3 single-split with revision unknown) -> that axis status = MEASUREMENT_INVALID or BLOCKED (outcome NOT_APPLICABLE), verdict deferred. Not scientific falsification.

**Clause 1 — WebArena within-store axis**: if family_reuse <0.5 OR param_task <0.3 OR exact_copy >=0.2 OR families_ge3 <5 OR families_ge4 <3 OR AX_consistency <0.6 OR AX_consistency is null/unmeasurable OR PC1 fails -> FALSIFIED-IN-SETTING for within-store hold-out viability. AX null = FALSIFIED-IN-SETTING, not PARTIAL (audit fix 7).

**Clause 2 — Mind2Web cross-website axis**: if spec-compliant TF-IDF/k-means on official splits was executed and overlap <0.15 OR (overlap - shuffle_mean) <0.10 OR overlap <= shuffle_p95 OR param_prevalence <0.15 OR PC2 fails -> FALSIFIED-IN-SETTING for same-mechanism cross-website transfer. If spec-compliant mechanism/splits/null were not executed (coarse heuristic, synthetic partition, label-shuffle null) -> INCONCLUSIVE/MEASUREMENT_INVALID per audit fixes 2-4, not falsified.

**Clause 3 — SURVIVES**: if Gate 0 passes AND Clauses 1 and 2 both pass AND NC2/NC3 behave (shuffled low, exact-copy <0.2) AND bootstrap CIs exclude thresholds by >=0.05 margin -> SURVIVES_CURRENT_TEST. Ceiling: within-store family hold-out is viable identifiable same-mechanism substrate; Mind2Web provides measurable cross-website overlap for future website-holdout.

**Clause 4 — MIXED**: one axis passes, the other is FALSIFIED-IN-SETTING -> MIXED with per-axis bounded ceiling (declare which transfer axis is viable; do not overclaim cross-site if only within-store survives).

**Clause 5 — Duplication handling**: high duplication 0.9479 is NOT a trigger for MIXED when exact-copy <0.2; parent MIXED duplication clause is superseded. Report duplication decomposition explicitly.

Thresholds frozen; no post hoc relaxation. All comparisons use two-sided bootstrap CIs where relevant but decision thresholds are point-estimate based with CI margin check.

## 7. Baselines and Controls Summary

Stable IDs for downstream transmission: B1_DOC_M1_12STORES, B2_DOC_M2_HEURISTIC, B3_SPIDER_2SITE, B4_SHUFFLE_NULL, B5_RETRIEVAL_REPLAY_STRONG, PC1_WEB_SEARCH, PC2_MIND2WEB_RECURRENCE, NC1_WIKIPEDIA_NULL, NC2_MIND2WEB_SHUFFLE_NULL, NC3_WEB_EXACT_COPY_NULL. Expected behaviors in spec.json. This experiment does not re-measure B3 quantitatively but retains it as lower bound; B5 is disclosure-only for product framing.

## 8. Validity Threats and Mitigations

**Representation loss**: intent_template may be coarser than true mechanism (search vs filtered search merged). Mitigated by live AX consistency check at element-pattern level (role/name) and by disclosing template granularity; Mind2Web TF-IDF/k-means may merge distinct mechanisms or split same mechanism — disclosed via cluster counts, k/2 and 2k sensitivity, and fallback bigram disclosure. No post hoc redefinition.

**Sampling**: 15-20 WebArena AX trees cannot cover 49 families exhaustively; stratified 2-per-family across >=10 families with frozen seed and explicit below-fold exclusion limits claims to initial viewport only. Mind2Web HF version drift — pinned revision and hash with divergence disclosure.

**Leakage**: Mind2Web website identity must not leak into mechanism clustering; clustering fitted on train only (vectorizer + k-means), test labels via predict only. WebArena template hold-out is instance-level within single store; no site identity to leak.

**Infrastructure**: Docker optional but required for AX live path; Playwright install required; HF auth/rate limit — 3 retries with backoff, durable error, and MEASUREMENT_INVALID vs FALSIFIED distinction.

**Coarse clustering artifact**: Previous 33-mechanism heuristic inflated both true (0.7407) and null (0.6942) — fine-grained TF-IDF/k-means with website-label shuffle is the falsifier; k/2,2k sensitivity will reveal if excess is granularity-dependent.

**Overclaim**: This experiment does NOT demonstrate LLM benefit, freshness, or repair. C-LLM-INHERIT remains EXPERIMENTAL pending future Product within-store hold-out (cold vs retrieval vs SPIDER with 0-token replay). Validity notes will carry this ceiling; report.md must distinguish RAW EVIDENCE (counts, node counts, revision hashes) from DERIVED MEASUREMENT (fractions, CIs, excess) from INTERPRETATION (viability).

## 9. Product Consequence

See spec.json product_consequence_positive / product_consequence_negative. Positive (both axes PASS) unlocks Product/Graph within-store hold-out and Mind2Web website-holdout designs vs cold/retrieval/SPIDER with strong replay baseline. WebArena-only PASS unlocks within-store hold-out only; Mind2Web-only PASS unlocks website-holdout only. Negative/both FAIL keeps Product bounded to 2-site corpus or custom benchmark and prevents LLM-costly ranking on vacuous substrate. MEASUREMENT_INVALID requires infra repair, not negative inference.

## 10. Analysis Plan

- Compute all metrics deterministically with seed 35725763380.
- Bootstrap 95% CIs (2000 reps) for WebArena duplication/exact-copy/param/family-reuse and Mind2Web overlap/param per split.
- Website-label shuffle null 1000 perms for Mind2Web overlap (mean/std/p95, excess).
- Report per-family size histogram, list of hold-out-viable families, AX consistency table (family, intent_template, task_ids, element pattern present per task, pass/fail), Mind2Web per-split overlap table for k, k/2, 2k, and comparison to documentation heuristics (B1/B2) with gap quantified.
- Preserve raw and derived artifacts with sha256 for audit recomputation.
- Report.md will not exceed frozen claim ceiling and will keep RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT -> INTERPRETATION distinct, with strict decision_rule evaluation in order.

## 11. Estimated Cost and Information Gain

- **Cost**: LOW — <2h compute, <4GB /tmp, no LLM API, stdlib+datasets+scikit-learn+optional Playwright/Docker (see spec).
- **Information gain**: HIGH — resolves 7 blocking audit findings that gate all cross-site and LLM-inherit tests; portfolio-level decision-changing for C-LLM-INHERIT/C-CROSSSITE; unlocks or redirects highest-leverage product promise before costly ranking.

## 12. Time and Resource Estimate

- Dataset pinning and census: 0.5h
- Sampling + live AX extraction (15+ trees at 1280x720): 0.5-1h (including Docker pull + Playwright install)
- Mind2Web download / TF-IDF fit train-only / k-means / overlap / shuffle (1000 perms) / bootstrap (2000 reps) / k/2,2k sensitivity: 1h
- Reporting and provenance: 0.5h
- Total: ~2-3h

## 13. Falsification and Audit Preparation

All code paths for decision_rule clauses are unit-tested with synthetic fixtures (mock 1-store census at/below thresholds, mock AX_consistency 0.5 vs 0.7, mock overlap at/below 0.15 and excess at/below 0.10) before execution. Audit recomputation enabled by freezing seeds, pinning HF revision, preserving raw JSONs and AX trees with sha256, and hashing TF-IDF/k-means artifacts. Failure modes (Playwright missing, HF single-split, coarse fallback) are not re-labeled as negatives but as MEASUREMENT_INVALID/INCONCLUSIVE per Gate 0 / Clause 2. Any analysis deviating from this plan after seeing results will be labeled exploratory and requires a new preregistration for confirmatory claims.

---
*Preregistration frozen before outcome inspection. Any analysis deviating from this plan after seeing results will be labeled exploratory and requires a new preregistration for confirmatory claims. Design respects 7 audit-required fixes and Director CONTINUE mandate; parent handoff established/rejected/unknown/do_not_assume distinctions preserved.*

