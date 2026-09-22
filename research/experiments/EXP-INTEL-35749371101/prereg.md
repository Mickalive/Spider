# EXP-INTEL-35749371101 Preregistration — Intel REOPEN Spec-Compliant Remeasurement for C-CROSSSITE / C-PARAM-INHERIT

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35749371101
- **Lane**: intel
- **Claims**: C-CROSSSITE (primary allocation, REOPEN), C-PARAM-INHERIT (secondary substrate for within-store parameterized transfer)
- **Parent Handoff**: `research/experiments/EXP-INTEL-35741921602/handoff.json`, sha256 `7574ec3943b064ff8d916c95ec39041d3a731d87de90d9c74ec07bb0617a29dd`, verdict `REVISE` (audit REVISE, 5 required_fixes)
- **Director Mandate**: REOPEN C-CROSSSITE, `request.json` cycle 35748646600, allocation action REOPEN, target claim C-CROSSSITE, parent_handoff_disposition USE, binding strategic question verbatim in spec.json:question
- **Date**: 2026-09-22
- **Status**: DESIGN — NOT YET FROZEN (freeze.json will hash spec.json + prereg.md before EXECUTE)

This is a NEW governed experiment. Per AGENTS.md precedence, the Director's strategic question is binding research direction; the inherited parent_handoff is continuity evidence only and must not silently override the REOPEN decision. This design preserves the parent handoff's four-way distinction while converting the Director question into the smallest rigorous falsifiable experiment.

## 2. Scientific Question (Binding Director Question, Refined)

> After fixing AX measurement validity - longest-prefix element-pattern mapping without fallback, task-specific navigation to category/product/cart start_url (not ?task= homepage) for >=20 live CDP Accessibility.getFullAXTree trees at 1280x720 across >=10 families 2-per-family (seed 35725763380), and pinning Mind2Web HuggingFace revision to expose official train/test_website/test_domain splits (resolving 73/3 vs 137/31 divergence, recording revision hash) for spec-compliant TF-IDF->k-means k=min(50,unique_train_tasks/20) fitted train-only with 1000 website-label shuffles, 2000 bootstraps and k/2,2k sensitivity - does AX_consistency >=0.6 demonstrate identifiable same-mechanism parameterized transfer within WebArena-Verified v2 and does Mind2Web cross-website overlap exceed shuffled null by >=0.10 sufficient to unblock product within-store family holdout vs cold/retrieval/SPIDER with 0-token replay?

**Refinement into smallest high-information experiment**: Recompute WebArena-Verified v2 census for pin integrity (192/49), live-extract >=20 AX trees with task-specific navigation and corrected longest-prefix mapping to compute AX_consistency with bootstrap CI, and remeasure Mind2Web overlap on pinned official splits with frozen TF-IDF/k-means train-only, website-label shuffle, bootstraps, and sensitivity. No LLM agents executed; substrate viability only. Result decides whether Product within-store family holdout (train N per family test held-out same family) is identifiable same-mechanism and whether Mind2Web website-holdout is demonstrably same-mechanism beyond null.

## 3. Motivation and Inherited State

### 3.1 Why This Is Highest Marginal Information

Per Global Research Director portfolio assessment (request.json portfolio_assessment): SPIDER at 229 canonical experiments has no claim VALIDATED/PRODUCT_CORE/SHIPPED, one REJECTED (C-PRODUCT-ECON logistic), two narrow EXPERIMENTAL ceilings (C-MEAS-VALID header-only, C-FRESHNESS LOCAL orthogonality). Four lanes IDLE, product FROZEN on degenerate residual, frontier synthetic. C-PARAM-INHERIT starved 0/60 recent (37 total, last 0/32 infra fail, ceiling only 5.42% synthetic token saving), C-RESIDUAL-NOVELTY 3 degenerate, C-LLM-INHERIT no same-model cold vs retrieval vs SPIDER comparison, C-CROSSSITE 5 recent all MEASUREMENT_INVALID, C-DELTA-REPAIR newly unblocked but no repair cost bounds. Graph tunneled 14/15 on C-FRESHNESS LOCAL with audit-confirmed confounds; physics/frontier tunneled 58 synthetic density-divergence experiments with complementary blind spots and 95% attenuation non-stationary. 

Scout brief organized evidence but was challenged on authority; Director imposed global comparison (marginal info vs opportunity cost) and parked further LOCAL tuning, forced physics out of TV/KDE basin, and directed Intel to deep verification of AX/Mind2Web splits rather than broad competitor teardown. Census alone (192/49 duplication 0.9479) insufficient to design true website holdout without site-identity leakage (next_gate requires true website holdout). Fixes are narrow, pre-registered, and directly unblock graph/product C-PARAM-INHERIT and C-CROSSSITE evaluations on BrowserGym/AgentLab 1280x720 substrate. Expected information gain is HIGH and portfolio-level decision-changing; cost is LOW (<2.5h, no LLM).

Prior Intel REVISE (EXP-INTEL-35741921602) replicated census exactly (192/49, duplication 0.9479 exact 0.0781 param 0.8958, 36 families >=3, PC1 PASS 1426 nodes) but AX_consistency 0.2857 (2/7) ruled MEASUREMENT_INVALID per audit (7<10 families, pattern_map ordering bug causing 5/7 false negatives via 'Add' prefix fallthrough, and ?task= homepage-only extraction yielding identical role sets). Mind2Web axis correctly MEASUREMENT_INVALID per Gate0 (single train 73/3/1009 vs spec 137/31, revision unknown, diagnostic overlap excess -0.184 not usable). Without corrected mapping + task-specific navigation and pinned HF revision with proper shuffle, Product holdout would mix incomparable mechanisms. Fixes are low cost and decision-changing: valid AX >=0.6 unlocks within-store holdout, valid Mind2Web excess >=0.10 unlocks website-holdout.

### 3.2 Parent Handoff Continuity — Preserved Four-Way Distinction

Parent EXP-INTEL-35741921602 handoff USE disposition preserved exactly; Director REOPEN supersedes `next_question` routing but inherits scientific state:

**Established** (must not be re-tested as hypothesis; recomputed for integrity only):
- WebArena-Verified v2 single Magento One Stop Market store pinned to d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (812 total, 192 shopping, 49 intent_templates, site_tuples 187 ('shopping',)+5 ('shopping','reddit'), verified_sha true) — census recomputed exactly: duplication 182/192=0.9479 95% CI [0.9167,0.9792], exact-copy 15/192=0.0781 CI [0.0417,0.1198] => 91.8% parameterized variants (167/182), param_task 172/192=0.8958 CI [0.8490,0.9375], param_template 41/49=0.8367, families_ge3=36 ge4=34 ge5=33; thresholds >=0.5 reuse, >=0.3 param, <0.2 copy, >=5 families>=3 and >=3 families>=4 all PASS (result.json:metrics.webarena_census, audit recomputed match). This is the narrow ceiling carried forward.
- Live CDP infrastructure verified at spec viewport: Playwright 1.63.0 installed and functional, Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb running at http://localhost:7770, 15 live Accessibility.getFullAXTree extractions at 1280x720 initial viewport no scroll (provenance.json docker_available true, 1426 nodes) — PC1 PASS 1426 nodes strongly confirmed (combobox 'Search' + button 'Search' + input#search placeholder in all 15 trees, audit validity_findings PC1 PASS).
- Mind2Web HuggingFace divergence correctly diagnosed per Gate0: osunlp/Mind2Web in this environment exposes only single train split (73 websites/3 domains/1009 tasks) vs spec 137/31, revision unknown — axis correctly reported MEASUREMENT_INVALID/BLOCKED not FALSIFIED (audit validity_findings[2] severity none).
- Controls correctly handled: PC1 PASS, PC2 CANNOT_VERIFY (needs official splits not fabricated), NC3 PASS (0.0781<0.2), B1 REJECTED (single store vs 12-store M1=1.0), B2 gap quantified, B3 2-site bound trivially exceeded, B4 website-label permutation correctly implemented (1000 perms seed 35725763380) yielding diagnostic mean 0.998, B5 disclosure only.

**Rejected** (must not be revived without new evidence):
- WebArena-Verified v2 provides 12 shopping store instances sharing mechanisms (M1=1.0) enabling train-on-N-stores/test-on-held-out-stores cross-site design — rejected bounded to v2 single store (audit baseline B1).
- High duplication 0.9479 implies verbatim copying diluting inheritance — rejected; decomposition shows exact-copy 0.0781, 91.8% parameterized variation, NC3 PASS.
- Producer interpretation that AX_consistency=0.2857 (2/7 <0.6) is valid FALSIFIED-IN-SETTING for within-store identifiability — rejected per audit REVISE: measurement invalid due to 7<10 families, pattern_map ordering bug (Add* families all expecting 'Add to Wish List' via prefix 'Add' fallthrough), and homepage-only navigation (?task=) yielding identical role sets testing homepage coverage not within-family stability; corrected longest-prefix 6/7 shows metric not discriminating.
- Claim that Mind2Web diagnostic overlap 0.8139 vs shuffle null 0.998 excess -0.184 demonstrates lack of sharing or that k=50 failure is website-specific — rejected; null inflated due to coarse clustering not website sharing, diagnostic correctly labeled not used for decision.
- Any claim that within-store holdout is identifiable same-mechanism parameterized transfer at element-pattern level or Mind2Web website-holdout is demonstrably same-mechanism at this granularity — rejected as not established; ceiling remains census-level reuse only.

**Unknown** (this experiment directly targets):
- Whether corrected longest-prefix mapping without fallthrough, task-specific navigation to category/product/cart start_url for >=20 trees across >=10 families 2-per-family at 1280x720 yields AX_consistency >=0.6 — requires code fix in measure.py and re-extraction with task-specific URLs (audit required_fixes 1-2, director mandate).
- Whether AX_consistency threshold sensitivity holds when below-fold/post-interaction states included vs initial viewport only — explicitly excluded per spec 1280x720 no scroll; representation loss disclosed.
- Whether Mind2Web pinned HF revision exposing official train/test_task/test_website/test_domain (137/31) exists, revision hash, task counts, and spec-compliant TF-IDF/k-means train-only overlap fraction, website-label shuffle excess (>=0.10), bootstrap CIs and k/2,2k sensitivity show — currently BLOCKED on revision unknown.
- Whether within-store template-count level holdout (36 families) differs from element-pattern level — count-level PASS but pattern-level UNMEASURED; future Product must test both vs cold/retrieval/SPIDER with 0-token replay.
- Whether alternative AX features (HTML tag/attribute, computed style) yield higher consistency — not tested.
- Bootstrap CI and power for AX_consistency with n=7 — no CI computed; requires >=10 families for margin check.

**Do_not_assume** (explicitly guarded):
- That AX_consistency=0.2857 is validated falsification justifying Product within-store holdout is NOT identifiable — do not treat buggy homepage-only metric as genuine negative; correct ceiling is MEASUREMENT_INVALID pending fix.
- That high census (0.9479, 0.8958, 36 families, PC1 PASS 1426 nodes) guarantees element-pattern identifiability or justifies LLM ranking — frozen Clause1 requires AX >=0.6 live verification.
- That 15 AX trees with distinct hashes but identical 1426 nodes and role sets prove parameterized variants are stable — they prove ?task= yields homepage, not product-page mechanisms; task-specific navigation required.
- That Mind2Web diagnostic overlap 0.8139 or shuffle null 0.998 falsifies C-CROSSSITE or that 73/3 single split approximates 137/31 — diagnostic on 50/50 split from single train, coarse k=50, not used for decision; true spec-compliant overlap remains UNKNOWN.
- That coarse 33-mechanism heuristic or label-shuffle null approximates frozen TF-IDF/k-means website-label permutation — audit REVISE rejects substitution.
- That substrate experiment demonstrated or refuted LLM benefit, 0-token advantage, or repair cost — no LLM agents, no cold vs retrieval vs SPIDER comparison executed.

### 3.3 What This Experiment Is and Is Not

**Is**: A spec-compliant repair that (1) re-extracts >=20 live CDP Accessibility.getFullAXTree trees at 1280x720 initial viewport with task-specific navigation to category/product/cart start_url across >=10 families 2-per-family (seed 35725763380) using corrected longest-prefix element-pattern mapping without fallback and computes AX_consistency >=0.6 with bootstrap CI, and (2) remeasures Mind2Web cross-website overlap on pinned official splits with frozen TF-IDF->k-means k=min(50,unique_train_tasks/20) fitted train-only via website-label shuffle (1000 perms), 2000 bootstraps, and k/2,2k sensitivity, recording HF revision hash. It recomputes WebArena census for integrity and evaluates frozen decision_rule strictly. Smallest high-information experiment that can change Product unblock decision.

**Is not**: An LLM agent inheritance test (no cold vs retrieval vs SPIDER execution), not a browser end-to-end cart/checkout flow beyond initial viewport, not a re-tuning of viewport heuristics, not a repetition of 12-store cross-site question on v2 (already falsified), not a synthetic DGP, not a documentation survey. It does not claim freshness, delta-repair, or product economics beyond substrate viability.

## 4. Hypotheses (Falsifiable, Directional, Preregistered)

### H1_WEB_PARAM_IDENTIFIABILITY — Within-store family holdout is identifiable same-mechanism

Operational: intent_template defines mechanism. Same-mechanism parameterized transfer is identifiable iff quantitative thresholds hold (family_reuse >=0.5, param_task >=0.3, exact_copy <0.2, families_ge3 >=5, families_ge4 >=3) AND element-pattern identifiability holds (AX_consistency >=0.6 on live CDP trees with corrected mapping and task-specific navigation). Expected: quantitative thresholds will replicate parent (0.9479, 0.8958, 0.0781, 36/34 families) — likely PASS — but AX_consistency is uncertain and is the falsifier; previous 15 trees 1-per-homepage could not test it.

### H2_AX_PATTERN_STABILITY — Same template -> same element pattern

AX_consistency = fraction of sampled families where both tasks' AX trees contain template-required element pattern at initial viewport via longest-prefix mapping without fallback. Mapping table frozen in code: distinct prefixes, no generic 'Add' fallthrough, validated against product-page vs homepage (Add to Wish List absent homepage present product page, Add to Cart present both). Threshold >=0.6. Expected direction uncertain — homepage PC1 suggests search pattern present, but within-family consistency across parameterized variants (e.g., 'Search for {{product}}' with different products all landing on search results vs homepage) must be measured with task-specific navigation.

### H3_MIND2WEB_OVERLAP — Cross-website splits share mechanisms under fine-grained clustering

Mechanism = TF-IDF->k-means cluster label fitted train-only (k = min(50, unique_train_tasks/20)). Overlap = |M_test_website ∩ M_train|/|M_test_website| >=0.15 and exceeds website-label shuffle null mean by >=0.10 and exceeds p95. Expected direction uncertain — coarse 33-mechanism gave excess 0.0466 <0.10 INCONCLUSIVE and diagnostic 0.814 vs null 0.998 excess -0.184; fine-grained TF-IDF/k-means may lower both true and null but excess threshold tests genuine sharing. k/2 and 2k sensitivity discloses granularity dependence. Parmeterization prevalence >=0.15.

### H4_HEURISTIC_DISCLOSURE — Parameterization vs copy decomposition

Measured WebArena duplication 0.9479 will again decompose to exact-copy <0.2 (parameterized reuse 91.8%), disclosing heuristic M2 inflation. Mind2Web fine-grained param prevalence reported with gap to heuristic 0.65 and duplication fraction with sensitivity.

## 5. Methods (Frozen Before Outcome Inspection)

### 5.1 Datasets and Pinning

- **WebArena-Verified v2**: `research/experiments/EXP-INTEL-35725763380/artifacts/raw/webarena-verified.json` from ServiceNow/WebArena-Verified commit `ef74e1bfd0d83d4bab1c55b2d1b4c2aeaac8e0d0`, sha256 `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` (812 tasks). Verify 192 shopping tasks / 49 templates; also verify `test.raw.json` and `webarena-verified-hard.json` for consistency. Any sha divergence reported, not silently substituted.
- **Mind2Web**: HuggingFace `osunlp/Mind2Web` (canonical NeurIPS 2023) via `datasets` library. MUST record HF revision hash (git commit), download date, per-split census train/test_task/test_website/test_domain task/website/domain counts. Attempt `load_dataset('osunlp/Mind2Web', revision=<pinned>)` exposing official splits. If HF exposes only single split train (as parent 1009/73/3), document divergence to spec 137/31, record revision, and report Mind2Web axis as MEASUREMENT_INVALID/INCONCLUSIVE — do NOT synthesize splits. 3 retries with backoff; durable error on failure.
- **Browser substrate**: BrowserGym/AgentLab standard 1280x720 observation/action capture with live CDP Accessibility.getFullAXTree (director prior 3), not bespoke CDP plumbing beyond spec.

### 5.2 Mechanism Definitions (Frozen Before Measurement)

- **WebArena mechanism**: `intent_template` string verbatim (e.g., `Search for {{product}}`). Parameterization = `instantiation_dict` non-empty task-level or template has ≥2 distinct instantiations across tasks template-level. Exact-copy = identical (template AND instantiation_dict) appearing ≥2.
- **Mind2Web mechanism**: Normalized operation-template cluster = TF-IDF on concatenated `(task instruction + action target text + candidate element text)` -> k-means. Frozen: TF-IDF max_features 5000, ngram_range (1,2), lowercase, stop_words english, min_df 2; k = min(50, n_unique_train_tasks/20) where n_unique_train_tasks = distinct task strings in train; k-means n_init 10, random_state 35725763380, fitted on train only, then applied to test splits via same vectorizer/centroids (predict). No test leakage. Fallback if unstable (n_samples < k or empty clusters or silhouette <0.05): exact `(action_type, verb_lemma)` bigram with disclosure, still report k/2,2k sensitivity. Sensitivity: report overlap for k, k/2, 2k.

Definitions frozen in `research/intel/exp_35749371101_measure.py` (new file, sha recorded in provenance.json) before any metric computed; file hash frozen at freeze.json time.

### 5.3 WebArena Census and Hold-out Enumeration (Integrity Check)

1. Parse webarena-verified.json, filter site tuple containing shopping, count tasks, distinct intent_templates, per-template task counts.
2. Compute: duplication = tasks whose template appears >=2 / total; exact_copy = tasks with identical (template, instantiation_dict) appearing >=2 / total; param fractions task/template; family sizes histogram; families_ge3, ge4, ge5; usable hold-out families list.
3. Bootstrap 95% CIs (2000 reps, seed 35725763380) for duplication, exact-copy, param, family-reuse.

### 5.4 Accessibility-Tree Live Verification — The Critical Fix

- **Sampling**: Stratified >=20 tasks across >=10 families, exactly 2 tasks per family where family size >=2, using frozen seed 35725763380. Prefer families with >=3 tasks (hold-out realism) and cover diverse mechanisms (search, add-to-cart, wish-list, reviews, search+filter, cart, address). Sampling code frozen before extraction; list of task_ids pre-registered in derived artifact with sampling seed.
- **Task-specific navigation**: For each sampled task, resolve start_url from dataset fields: use `start_url` if present, else construct via `category`/`product_id`/`product` instantiation mapped to Magento One Stop Market routes (`/catalog/category/view`, `/catalog/product/view/id/` etc.), not `?task=` homepage. Verify navigation mapping discloses field used per task; record requested URL vs final URL. Previous `?task={id}` yields homepage for all shopping tasks — this fix navigates to task-relevant page (category listing, product detail, shopping cart `/checkout/cart/`).
- **Longest-prefix mapping without fallback**: Element-pattern mapping table uses longest matching intent_template prefix among entries, no generic fallthrough. Example frozen entries: `Search for {{product}}` -> combobox 'Search' + button 'Search'; `Add {{product}} to cart` -> button 'Add to Cart'; `Add {{product}} to my wish list.` (exact with period) -> link/button 'Add to Wish List' and `Add a {{product}} to my wish list.` -> same but distinct entry no sharing prefix 'Add'; `Add the product` variants each distinct; `Get name(s) of reviewer` -> region 'Reviews'; etc. Table validated against known product-page AX where Add to Wish List exists vs homepage where absent; unit test asserts no prefix 'Add' alone matches.
- **Live extraction**: Run `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` at `http://localhost:7770` (Docker). For each sampled task's task-specific start URL, use Playwright CDP `Accessibility.getFullAXTree` at **1280x720 initial viewport, no scroll, no cart/checkout execution**. Save raw AX JSON with sha256, node count, viewport metadata, task_id, intent_template, start_url, extraction timestamp. Requires `npx playwright install chromium` (record playwright_installed true, docker_available true, image digest). Below-fold/post-checkout not measured — disclosed as scope bound.
- **AX consistency**: For each sampled family with 2 tasks, check whether both AX trees contain template-required element pattern per frozen mapping. Consistency = families passing / families sampled. Manual inspection of 3 families for sanity. Threshold >=0.6. Bootstrap CI 2000 reps for AX_consistency.
- **Failure handling**: If Docker pull fails or Playwright not installable after 3 retries, record durable error, set ax_consistency = null, provenance playwright_installed false, evaluate Clause1 as FALSIFIED-IN-SETTING per frozen rule — do not treat as PASS. If task-specific URL field missing for a template, disclose and use homepage with annotation but that family counts toward null measurement validity.

### 5.5 Mind2Web Cross-Website Overlap — Spec-Compliant Remeasurement

1. Load Mind2Web HF pinned revision, enumerate official splits, verify task counts per split and website/domain counts. Record revision hash/date. If only single split available, document divergence and halt Mind2Web axis as MEASUREMENT_INVALID (do not fabricate).
2. Extract mechanism label per task via frozen TF-IDF/k-means (train-only fit). For each task, mechanism set = 1 label per task (cluster of first action's TF-IDF vector; multi-step majority label exploratory diagnostic but primary is first-action to avoid multi-label ambiguity — preregistered).
3. Compute: overlap_website = |M_test_website ∩ M_train|/|M_test_website|; similarly test_domain and test_task (diagnostic). Also duplication and parameterization_prevalence per split.
4. **Website-label shuffle null**: Permute website assignment labels across train+test_website task pool 1000 times (seed 35725763380): shuffle website label array, reassign tasks to train/test_website preserving per-split task counts, recompute overlap each perm. Record mean/std/p95, excess = true - mean. True must exceed mean by >=0.10 and exceed p95. This permutes website identity, not mechanism labels, keeps split sizes fixed (no random split_point).
5. **Uncertainty**: Bootstrap 95% CIs for overlap and param prevalence (2000 reps, same seed). **Sensitivity**: recompute overlap for k/2 and 2k (same TF-IDF, different k) and report table; primary decision uses k, sensitivity is disclosure.
6. Record TF-IDF vocab hash, k-means centroids hash, cluster counts per split.

### 5.6 Controls (Stable Identifiers)

- **PC1_WEB_SEARCH** (live): task-specific + homepage AX must contain combobox 'Search' + button 'Search' and DOM input#search placeholder 'Search entire store here...' form /catalogsearch/result/. Must PASS on re-extracted live trees; failure = measurement error.
- **PC2_MIND2WEB_RECURRENCE**: >=1 TF-IDF/k-means cluster appears in >=10 tasks across >=3 websites in train. Proves recurrence detectable under fine-grained clustering.
- **NC1_WIKIPEDIA_NULL**: guarded Wikipedia Docker check — if absent, report NOT EXERCISED (null not 0).
- **NC2_MIND2WEB_SHUFFLE_NULL**: website-label shuffle null per 5.5(4) — true overlap must exceed mean by >=0.10 and p95.
- **NC3_WEB_EXACT_COPY_NULL**: WebArena exact-copy <0.2 distinguishes parameterized reuse from verbatim copy.
- Baselines B1-B5 stable for audit recomputation: B1_DOC_M1_12STORES, B2_DOC_M2_HEURISTIC, B3_SPIDER_2SITE, B4_SHUFFLE_NULL, B5_RETRIEVAL_REPLAY_STRONG (disclosure-only).
- All controls use frozen seed 35725763380.

### 5.7 Artifacts

- `artifacts/raw/webarena-verified.json` (sha d6527566... hash verification)
- `artifacts/raw/mind2web_split_census.json` (HF revision hash, per-split counts, website/domain counts)
- `artifacts/raw/axtree_web_sample_task_specific_*.json` (>=20 live AX trees task-specific navigation at 1280x720, each sha256, viewport, start_url metadata) — live-extracted, not reused
- `artifacts/derived/measurements.json` (all metrics: webarena census, family histogram, AX_consistency table per family, Mind2Web overlap per k, bootstrap CIs, shuffle null distribution, TF-IDF/k-means hashes)
- `artifacts/derived/bootstrap_ci.json` (2000 reps, seed, CIs for duplication/exact_copy/param/AX/overlap)
- `artifacts/derived/shuffle_null.json` (1000 perms, mean/std/p95, per-perm overlaps, seed)
- `artifacts/derived/tfidf_kmeans_meta.json` (vectorizer params, k, k/2, 2k, vocab hash, centroids hash, cluster counts)
- `research/intel/exp_35749371101_measure.py` (frozen measurement script, sha in provenance.json)
- `provenance.json` (commits, HF revision, Docker digest, playwright_installed, docker_available, seeds, artifact hashes)

## 6. Decision Rule (Frozen, Ordered)

**Gate0 — Infrastructure**: if WebArena JSON sha mismatch irreconcilable OR Mind2Web HF unavailable after 3 retries OR Mind2Web pinned revision does not expose official train/test_task/test_website/test_domain splits (e.g., single train 73/3 vs spec 137/31 revision unknown) -> that axis status = MEASUREMENT_INVALID or BLOCKED (outcome NOT_APPLICABLE), verdict deferred. Not scientific falsification.

**Clause1 — WebArena within-store axis**: if family_reuse <0.5 OR param_task <0.3 OR exact_copy >=0.2 OR families_ge3 <5 OR families_ge4 <3 OR AX_consistency <0.6 OR AX_consistency is null/unmeasurable (<20 trees or <10 families 2-per-family or Playwright/CDP extraction fails or homepage-only navigation) OR PC1 fails -> FALSIFIED-IN-SETTING for within-store holdout viability. AX null = FALSIFIED-IN-SETTING, not PARTIAL.

**Clause2 — Mind2Web cross-website axis**: if spec-compliant TF-IDF/k-means on official splits executed and (overlap <0.15 OR excess <0.10 OR overlap <= shuffle_p95 OR param_prevalence <0.15 OR PC2 fails) -> FALSIFIED-IN-SETTING for same-mechanism cross-website transfer. If spec-compliant mechanism/splits/null were not executed (coarse heuristic, synthetic partition, label-shuffle null) -> INCONCLUSIVE/MEASUREMENT_INVALID per audit (not falsified).

**Clause3 — SURVIVES**: if Gate0 passes AND Clauses 1 and 2 both pass AND NC2/NC3 behave (shuffled low, exact-copy <0.2) AND bootstrap CIs exclude thresholds by >=0.05 margin -> SURVIVES_CURRENT_TEST. Ceiling: within-store family holdout is viable identifiable same-mechanism substrate; Mind2Web provides measurable cross-website overlap for future website-holdout.

**Clause4 — MIXED**: one axis passes, other is FALSIFIED-IN-SETTING -> MIXED with per-axis bounded ceiling (declare which transfer axis is viable; do not overclaim cross-site if only within-store survives).

**Clause5 — Duplication handling**: high duplication 0.9479 is NOT a trigger for MIXED when exact-copy <0.2; parent MIXED duplication clause superseded. Report duplication decomposition explicitly.

Thresholds frozen; no post hoc relaxation. All comparisons use two-sided bootstrap 95% CIs where relevant but decision thresholds are point-estimate based with CI margin check (threshold +0.05 inside CI lower bound for SURVIVES). Two-sided shuffle test at alpha 0.05 via p95 exceedance.

## 7. Baselines and Controls Summary

Stable IDs for downstream transmission: B1_DOC_M1_12STORES, B2_DOC_M2_HEURISTIC, B3_SPIDER_2SITE, B4_SHUFFLE_NULL, B5_RETRIEVAL_REPLAY_STRONG, PC1_WEB_SEARCH, PC2_MIND2WEB_RECURRENCE, NC1_WIKIPEDIA_NULL, NC2_MIND2WEB_SHUFFLE_NULL, NC3_WEB_EXACT_COPY_NULL. Expected behaviors in spec.json. B3 is lower bound disclosure; B5 is disclosure-only framing for future Product within-store holdout (cold vs retrieval vs SPIDER vs SPIDER+0-token replay). Strong baselines: literal 0-token replay fails on perturbation (Director prior 1), so parameterized reuse requires applicability guards (false_accept/UNKNOWN ECE) not success alone — this Intel substrate does not yet measure retrieval benefit but disclosure prevents conflation.

## 8. Validity Threats and Mitigations

**Representation loss**: intent_template may be coarser than true mechanism (search vs filtered search merged). Mitigated by live AX consistency at element-pattern level (role/name) with longest-prefix mapping and by disclosing template granularity; Mind2Web TF-IDF/k-means may merge distinct mechanisms or split same mechanism — disclosed via cluster counts, k/2 and 2k sensitivity, and fallback bigram disclosure. No post hoc redefinition.

**Sampling**: >=20 WebArena AX trees across >=10 families cannot cover 49 families exhaustively; stratified 2-per-family with frozen seed and explicit below-fold exclusion limits claims to initial viewport task-specific pages only. Stratified preferring families >=3 ensures holdout realism vs homepage-only prior. Task-specific URL field mapping completeness disclosed. Mind2Web HF version drift — pinned revision and hash with divergence disclosure.

**Leakage**: Mind2Web website identity must not leak into mechanism clustering; clustering fitted train only (vectorizer + k-means), test labels via predict only; shuffle null permutes website labels not mechanism labels preserving split sizes and keeping k-means fixed (website-label shuffle per audit). WebArena template holdout is instance-level within single store; no site identity to leak. Longest-prefix mapping without fallback prevents generic 'Add' leakage causing Add-to-Wish-List fallthrough.

**Infrastructure**: Docker optional but required for AX live path; Playwright install required; HF auth/rate limit — 3 retries with backoff, durable error, and MEASUREMENT_INVALID vs FALSIFIED distinction preserved per Gate0. Director prior 5 (LLM/budget preflight) not applicable here (no LLM); offline replay substrate ensures no infra failure masks science.

**Coarse clustering artifact**: Previous coarse mechanisms (33) inflated true and null together (0.814 vs 0.998) — fine-grained TF-IDF/k-means k=min(50,unique/20) with website-label shuffle is the falsifier; k/2,2k sensitivity reveals if excess is granularity-dependent. True overlap must exceed p95 not just mean.

**Overclaim**: This experiment does NOT demonstrate LLM benefit, freshness guards with false_accept/UNKNOWN ECE, or delta-repair amortization — product consequences are conditional on substrate passing; report.md must keep RAW EVIDENCE (counts, node counts, revision hashes, start_urls) distinct from DERIVED MEASUREMENT (fractions, CIs, excess, AX table) from INTERPRETATION (viability, unblock).

**Browser context salience / stale snippets** (Director prior 3): Acknowledged — future Product holdout using BrowserGym/AgentLab 1280x720 fresh grounding will mitigate path dependence; this Intel measurement uses fresh per-task grounding with no accumulated trajectory.

## 9. Product Consequence (from spec.json)

**Positive SURVIVES (both)**: Product/Graph UNBLOCKED to design within-store template-family holdout for C-PARAM-INHERIT/C-LLM-INHERIT on WebArena-Verified v2 (36 families >=3 enabling 2-train/1-test with AX>=0.6) AND Mind2Web website-holdout for C-CROSSSITE (overlap >=0.15 excess >=0.10). Next Product trains on N per family/website test held-out same family/cluster vs cold/retrieval/SPIDER with strong 0-token replay baseline (90ms TERX/HyperAgent 23k->0 framing). Mind2Web overlap green-lights parallel website-holdout.

**Positive MIXED WebArena-only**: proceed ONLY within-store holdout; do not claim cross-site generalization; Mind2Web remains diagnostic. MIXED opposite: within-store not identifiable; Product stays bounded to 2-site or Mind2Web-only.

**Negative WebArena FALSIFIED** (AX <0.6 or null): within-store family holdout NOT identifiable at element-pattern level despite census; Product stays bounded to 2-site or custom benchmark; do not proceed to LLM-costly ranking. **Negative Mind2Web FALSIFIED** (spec-compliant overlap <0.15 or excess <0.10): cross-website not demonstrably same-mechanism beyond null; website-holdout limited to within-store families or custom.

**MEASUREMENT_INVALID/BLOCKED**: no falsification; next action infra repair (pin HF revision with official splits, reinstall Playwright, re-pull container) and re-run; do not treat as negative. In all negative/inconclusive ceiling remains census only (192/49 duplication 0.9479 exact 0.0781 param 0.8958 families 36/34/33) with no LLM benefit demonstrated.

## 10. Analysis Plan (Preregistered)

- Compute all metrics deterministically with seed 35725763380.
- Bootstrap 95% CIs (2000 reps) for WebArena duplication/exact-copy/param/family-reuse, AX_consistency, Mind2Web overlap/param per split.
- Website-label shuffle null 1000 perms for Mind2Web overlap (mean/std/p95, excess true-mean and comparison to p95).
- Sensitivity: recompute Mind2Web overlap for k/2 and 2k (same TF-IDF, different k) reporting table; primary decision uses k.
- Report per-family size histogram, list of hold-out-viable families, AX consistency table (family, intent_template, task_ids, element pattern present per task, pass/fail, start_url), Mind2Web per-split overlap table for k/k/2/2k, and comparison to documentation heuristics (B1/B2) with gap quantified.
- Preserve raw and derived artifacts with sha256 for audit recomputation; record TF-IDF vocab hash and k-means centroids hash.
- Report.md will not exceed frozen claim ceiling and will keep RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT -> INTERPRETATION distinct, with strict ordered decision_rule evaluation.

## 11. Estimated Cost and Information Gain

- **Cost**: LOW — <2.5h compute, <4GB /tmp, no LLM API, stdlib+datasets+scikit-learn+optional Playwright/Docker (spec estimate). Offline replayable; director prior 5 fulfilled (no LLM waste).
- **Information gain**: HIGH — resolves 5 blocking audit findings gating all cross-site and LLM-inherit tests; portfolio-level decision-changing for C-CROSSSITE/C-PARAM-INHERIT/C-LLM-INHERIT; unlocks or redirects highest-leverage product promise before costly ranking; directly tests BrowserGym/AgentLab 1280x720 substrate and pinned HF revision dependencies highlighted by Director.

## 12. Time and Resource Estimate

- Dataset pinning and census recomputation: 0.5h
- Sampling + task-specific navigation logic + longest-prefix mapping unit tests: 0.5h
- Live AX extraction (>=20 trees at 1280x720 with task-specific URLs): 0.5-1h (including Docker pull + Playwright install)
- Mind2Web download / TF-IDF train-only fit / k-means / overlap / shuffle 1000 perms / bootstrap 2000 reps / k/2,2k sensitivity: 1h
- Reporting and provenance with hash verification: 0.5h
- Total: ~2.5-3h

## 13. Falsification and Audit Preparation

All code paths for decision_rule clauses are unit-tested with synthetic fixtures (mock 1-store census at/below thresholds, mock AX_consistency 0.5 vs 0.7 with longest-prefix vs fallback comparison, mock task-specific vs homepage navigation, mock Mind2Web overlap at/below 0.15 and excess at/below 0.10) before execution. Audit recomputation enabled by freezing seed 35725763380, pinning HF revision, preserving raw JSONs and AX trees with sha256/start_url, and hashing TF-IDF/k-means artifacts (vocab hash, centroids hash) plus vectorizer params in meta json. Failure modes (Playwright missing, HF single-split, coarse fallback) are not relabeled as negatives but as MEASUREMENT_INVALID/INCONCLUSIVE per Gate0/Clause2 with durable error and revision disclosure. Any analysis deviating from this plan after seeing results will be labeled exploratory and requires new preregistration for confirmatory claims. Model priors used in Director rationale (replay vs similarity, verification abstention ECE, path dependence, compilation brittleness, provider budgets) are acknowledged but not tested in this substrate; they motivate Product design conditional on substrate pass.

---
*Preregistration frozen before outcome inspection. Any analysis deviating from this plan after seeing results will be labeled exploratory and requires a new preregistration for confirmatory claims. Design respects Director REOPEN mandate for C-CROSSSITE, preserves parent handoff established/rejected/unknown/do_not_assume distinctions, implements 5 audit-required fixes plus director-specified 1000 shuffles/2000 bootstraps/k/2,2k sensitivity, and is the smallest rigorous experiment that can change a claim/product decision without repeating pre-2.0 work or inspecting outcomes during DESIGN.*
