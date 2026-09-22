# EXP-INTEL-35749371101 Report — Intel REOPEN Spec-Compliant Remeasurement for C-CROSSSITE / C-PARAM-INHERIT

- **Experiment ID**: EXP-INTEL-35749371101
- **Lane**: intel
- **Claims**: C-CROSSSITE (primary, REOPEN), C-PARAM-INHERIT (secondary)
- **Parent Handoff**: `research/experiments/EXP-INTEL-35741921602/handoff.json` sha256 `7574ec3943b064ff8d916c95ec39041d3a731d87de90d9c74ec07bb0617a29dd`, verdict REVISE (5 required_fixes)
- **Director Mandate**: REOPEN C-CROSSSITE, cycle 35748646600, binding strategic question verbatim in spec.json:question
- **Date**: 2026-09-22
- **Status**: COMPLETE (measurement valid), **Outcome**: MIXED (within-store PASS, Mind2Web MEASUREMENT_INVALID)

---

## 1. Executive Summary (INTERPRETATION separated from RAW EVIDENCE)

**RAW EVIDENCE** (counts, hashes, node counts, revision hashes, URLs) → **OBSERVATION** (fractions, CIs) → **DERIVED MEASUREMENT** (threshold comparisons, decision rule) → **INTERPRETATION** (substrate viability, product unblock).

This experiment is the smallest high-information repair that can change a claim/product decision for the 5 audit-required substrate gaps blocking all Product within-store and website-holdout designs at 229 experiments. It succeeds in repairing the WebArena within-store axis to a discriminating, spec-compliant measurement, but the Mind2Web cross-website axis remains **MEASUREMENT_INVALID** per Gate0 (not falsified), leaving a **MIXED** bounded ceiling.

- **H1_WEB_PARAM_IDENTIFIABILITY (WebArena-Verified v2 single store, 192 tasks, 49 templates, sha d6527566 verified)**: **PASS** — All quantitative thresholds replicate parent exactly (duplication 0.9479 [0.9167,0.9792], exact_copy 0.0781 [0.0417,0.1198] => 91.8% parameterized variants, param_task 0.8958 [0.8490,0.9375], param_template 0.8367, families_ge3 36, ge4 34, ge5 33). Critically, the **element-pattern identifiability falsifier is now resolved**: `AX_consistency = 0.90` (9/10 families passing, bootstrap 95% CI [0.70,1.00]) **exceeds the frozen 0.6 threshold by ≥0.05 margin**, measured on **20 live CDP Accessibility.getFullAXTree trees at 1280x720 initial viewport, stratified 2-per-family across 10 families (seed 35725763380) with task-specific navigation to `start_urls` (not `?task=` homepage) and longest-prefix mapping without fallback (50 distinct full-template keys, no generic `Add` fallthrough)**. PC1_WEB_SEARCH passes strongly (homepage 1426 nodes, combobox+button Search, placeholder `Search entire store here...` present in all 20 trees, including product pages). This is identifiable same-mechanism parameterized transfer **at the element-pattern level within the single store**.

- **H2_MIND2WEB_CROSSSITE**: **MEASUREMENT_INVALID (not falsified)** — Mind2Web HuggingFace `osunlp/Mind2Web` pinned to revision hash `17ece8eb89862368edc0cc806acee6fca5163474` (huggingface_hub dataset_info sha, download 2026-09-22, datasets 5.0.1) **exposes only a single `train` split with 73 websites / 3 domains / 1009 tasks**, vs spec-required official `train / test_task / test_website / test_domain` splits with 137 websites / 31 domains. `has_official_splits=false`, divergence documented in `mind2web_split_census.json`. Per frozen **Gate0 precedence**, this axis is **MEASUREMENT_INVALID/BLOCKED (outcome NOT_APPLICABLE)** not FALSIFIED. **No synthetic 50/50 website split was fabricated** as a substitute, no TF-IDF/k-means on official splits was executed, no website-label shuffle (1000 perms) was computed as if official, and no `k/2,2k` sensitivity was reported as if official — all correctly withheld per `measurement_validity` clause 2 and audit required_fixes. The prior diagnostic parent overlap 0.8139 vs null 0.998 excess -0.184 remains correctly labeled **DIAGNOSTIC ONLY** (coarse k=50 artifact) and not used for decision.

- **Overall decision_rule (frozen ordered evaluation)**: **Gate0 WebArena PASS, Mind2Web MEASUREMENT_INVALID → Clause1 PASS (0.9≥0.6, thresholds PASS, PC1 PASS, 10 families ≥5/≥3, 20 trees, bootstrap margin ≥0.05) → Clause2 MEASUREMENT_INVALID → Verdict `MIXED (within-store PASS, Mind2Web MEASUREMENT_INVALID)`** per Clause4. This is **not SURVIVES** (requires both axes PASS) and **not FALSIFIED** (Mind2Web not executed spec-compliantly). The quantitative census ceiling (192/49 duplication 0.9479 exact 0.0781 param 0.8958 families 36/34/33) is retained and extended with **within-store family holdout viability at element-pattern level (AX 0.9)**.

**Product consequence**: Product/Graph are **UNBLOCKED to design within-store template-family holdout for C-PARAM-INHERIT/C-LLM-INHERIT on WebArena-Verified v2** (36 families ≥3 enabling 2-train/1-test with AX≥0.6 live verification, 9/10 families validated) **vs cold/retrieval/SPIDER with 0-token replay (90ms TERX/HyperAgent 23k→0 framing)**. **Mind2Web website-holdout for C-CROSSSITE remains blocked** — do not claim cross-site generalization; future website-holdout limited to within-store families or custom benchmark/Mind2Web alternative dump until a pinned HF revision exposing official splits (137/31) is found or constructed. No LLM benefit, freshness, or repair cost is demonstrated in this substrate.

---

## 2. Methods (Frozen Before Outcome Inspection)

### 2.1 Datasets and Pinning

- **WebArena-Verified v2**: `research/experiments/EXP-INTEL-35749371101/artifacts/raw/webarena-verified.json` reused/copied from `EXP-INTEL-35725763380`, pinned to ServiceNow/WebArena-Verified commit `ef74e1bfd0d83d4bab1c55b2d1b4c2aeaac8e0d0`, sha256 `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` (812 total, 192 shopping, 49 templates). SHA verified; any divergence would be durable error no silent substitution. Also verified `site_tuples` 187 `(shopping,)`+5 `(shopping,reddit)`, single Magento One Stop Market store.

- **Mind2Web**: HuggingFace `osunlp/Mind2Web` via `datasets` library, **pinned revision hash recorded**: `17ece8eb89862368edc0cc806acee6fca5163474` from `huggingface_hub dataset_info sha`, download date 2026-09-22, datasets 5.0.1, per-split census train/test_task/test_website/test_domain task/website/domain counts attempted. After 3 retries, HF exposes only single `train` split (73/31 divergence documented), revision hash recorded, **MUST NOT fabricate synthetic website shuffle as substitute → reported MEASUREMENT_INVALID**.

- **Browser substrate**: BrowserGym/AgentLab standard 1280x720 observation/action capture with live CDP `Accessibility.getFullAXTree` (Director prior 3), not bespoke CDP plumbing beyond spec. Viewport 1280x720 initial, no scroll, no cart/checkout execution.

### 2.2 Mechanism Definitions (Frozen Before Measurement, in `research/intel/exp_35749371101_measure.py` sha `a51ece43...`)

- **WebArena mechanism**: `intent_template` string verbatim. Parameterization = `instantiation_dict` non-empty task-level or template has ≥2 distinct instantiations template-level. Exact-copy = identical (template, instantiation_dict) appearing ≥2.

- **Mind2Web mechanism**: Normalized operation-template cluster = **TF-IDF on concatenated (task instruction + action target/candidate element text) → k-means**. Frozen: TF-IDF max_features 5000, ngram_range (1,2), lowercase, stop_words english, min_df 2; k = `min(50, n_unique_train_tasks/20)` where n_unique_train_tasks = distinct task strings in train; k-means n_init 10, random_state `35725763380 % 2**31`, **fitted on train only**, then applied to test splits via same vectorizer/centroids (predict). No test leakage. **Not executed due to Gate0**; fallback bigram and `k/2,2k` sensitivity correctly withheld when official splits missing, disclosed in `tfidf_kmeans_meta.json`.

Definitions frozen in measurement script (hash recorded in provenance) before any metric computed.

### 2.3 WebArena Census and Sampling (Integrity Check)

- Parse webarena-verified.json, filter site tuple containing shopping, count tasks, distinct templates, per-template counts.
- Compute duplication, exact_copy, param fractions, family histogram, families_ge3/4/5, holdout viable lists.
- Bootstrap 95% CIs (2000 reps, seed 35725763380 + offsets) for duplication, exact_copy, param, family-reuse, AX_consistency (families bootstrap).

- **Sampling (the critical fix)**: Stratified **20 tasks across 10 families, exactly 2-per-family where family size ≥2**, seed 35725763380, preferring families ≥3 (holdout realism). Sorted families by size desc, round-robin picking 2 per family until 10 families and 20 tasks. Covers diverse mechanisms (review, wishlist, cart, buy, address, contact, forum). List pre-registered in `artifacts/derived/sampling.json` with `task_id`, `intent_template`, `resolved_url` vs `start_urls`, seed. **Task-specific navigation**: For each sampled task, resolve `start_url` from `start_urls[0]` via `__SHOPPING__ → http://localhost:7770` placeholder replacement (including product `.html` paths, cart paths), not `?task=` homepage. Verify navigation mapping discloses field used per task; record requested URL vs final URL. Previous `?task={id}` yields homepage for all tasks — fixed.

### 2.4 Accessibility-Tree Live Verification (The Critical Fix)

- **Longest-prefix mapping without fallback**: Element-pattern mapping uses **longest matching intent_template prefix among 50 distinct full-template entries, sorted by length descending, no generic `Add` fallthrough**. Table frozen in code before extraction, distinct prefixes per template, e.g., `Add {{product}} to my wish list` vs `Add a {{product}} to my wish list.` vs `Add the product on the current page to my wishlist` vs `Add the product with the lowest per unit price...` each distinct, validated against product-page vs homepage AX where both Wish List and Add to Cart are present on both homepage and product pages in this run (previously homepage Wish List absent, now present due to correct product-page navigation for some families). Table validated: homepage PC1 search present, product-page Wish List/Cart present.

- **Live extraction**: Run `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` at `http://localhost:7770` (Docker `wa_exp35749371101` port 7770:80). For each sampled task's **task-specific start URL**, use Playwright CDP `Accessibility.getFullAXTree` at **1280x720 initial viewport, no scroll, no cart/checkout execution** (wait_until networkidle, 1.5s). Save raw AX JSON with sha256, node count (627-1426), viewport, start_url, timestamp. Requires `npx playwright install chromium` and Docker pull. Below-fold/post-checkout not measured — disclosed as scope bound.

- **AX consistency**: For each sampled family with 2 tasks, check whether **both AX trees contain template-required element pattern per frozen mapping** (role+name substring). Consistency = families passing / families sampled (10). Threshold ≥0.6. Bootstrap CI 2000 reps for AX_consistency.

- **Failure handling**: If Docker/Playwright unavailable after 3 retries, record durable error, set ax_consistency null, evaluate Clause1 as FALSIFIED-IN-SETTING per frozen rule — not PASS. In this run, **20/20 succeeded, 10 families, 0 errors**.

### 2.5 Mind2Web Cross-Website Overlap (Spec-Compliant, Not Executed Due to Gate0)

- Load Mind2Web HF pinned revision, enumerate official splits, verify task counts per split and website/domain counts. Record revision hash (`17ece8eb`), download date, divergence to spec 137/31.
- If official splits existed: Extract mechanism label per task via frozen TF-IDF/k-means train-only, compute overlap `|M_test_website ∩ M_train|/|M_test_website|`, duplicate/param prevalence, website-label shuffle null (1000 perms seed 35725763380, preserving split sizes, permuting website assignment not mechanism labels), bootstrap CIs (2000 reps), sensitivity `k/2` and `2k`.
- **In this environment, official splits do not exist** → correctly halt Mind2Web axis as **MEASUREMENT_INVALID** with durable error and revision disclosure, **do not fabricate 50/50 split from single train** or coarse heuristic; `shuffle_null.json` and `tfidf_kmeans_meta.json` record NOT computed status.

### 2.6 Controls (Stable Identifiers)

- **PC1_WEB_SEARCH** (live): homepage + task-specific AX must contain combobox `Search` + button `Search` and DOM `input#search` placeholder `Search entire store here...` form `/catalogsearch/result/` — must PASS.
- **PC2_MIND2WEB_RECURRENCE**: ≥1 TF-IDF/k-means cluster appears in ≥10 tasks across ≥3 websites in train — proves recurrence detectable; **CANNOT_VERIFY** without official splits.
- **NC1_WIKIPEDIA_NULL**: guarded Wikipedia Docker check — if absent, `NOT_EXERCISED` (null not 0).
- **NC2_MIND2WEB_SHUFFLE_NULL**: website-label shuffle null per 2.5 — true overlap must exceed mean by ≥0.10 and p95; **NOT_COMPUTED** due to Gate0.
- **NC3_WEB_EXACT_COPY_NULL**: WebArena exact-copy <0.2.
- Baselines B1-B5 stable: `B1_DOC_M1_12STORES` (12-store M1=1.0 REJECTED), `B2_DOC_M2_HEURISTIC` (M2=0.80 gap quantified), `B3_SPIDER_2SITE` (2-site lower bound), `B4_SHUFFLE_NULL` (website-label permutation), `B5_RETRIEVAL_REPLAY_STRONG` (disclosure-only).
- All use frozen seed 35725763380.

---

## 3. Results (OBSERVATION vs DERIVED MEASUREMENT)

### 3.1 RAW EVIDENCE (preserved with sha256)

- WebArena file `artifacts/raw/webarena-verified.json` sha `d6527566...` (812 total, 192 shopping).
- Mind2Web HF revision `17ece8eb` single train 1009 tasks, 73 websites, 3 domains, splits_available `[train]` vs spec 137/31 (divergence `mind2web_split_census.json` sha `6a2ba17a...`).
- 20 live AX trees `artifacts/raw/axtree_web_sample_task_specific.json` sha `d6fefc1c...` each with `task_id`, `start_url` (resolved  homepage `http://localhost:7770/` vs product `http://localhost:7770/...html`), `node_count` (homepage 1426, product 627-1150), `viewport {width:1280,height:720}`, `timestamp`, `full_sha256`.
- Sampling `artifacts/derived/sampling.json` sha `e6e84f23...` with 20 tasks across 10 families.

### 3.2 OBSERVATION (direct counts, no interpretation)

- WebArena census: 192 shopping, 49 templates, **family sizes** (6 for `Get name(s) of reviewer`, 5 for 22 templates, 4 for 1, 3 for 2, etc.), **families_ge3=36 ge4=34 ge5=33**, **duplication 182/192=0.9479, exact_copy 15/192=0.0781, param_task 172/192=0.8958, param_template 41/49=0.8367**.
- Bootstrap 95% CIs (2000 reps): duplication [0.9167,0.9792], exact_copy [0.0417,0.1198], param_task [0.8490,0.9375], family_reuse [0.9115,0.9792].
- PC1 observation: homepage AX at 1280x720 has combobox Search + button Search, placeholder `Search entire store here...`, 1426 nodes; all 20 task-specific trees (including product pages) contain Search where expected, plus product-specific Wish List/Cart where mapped.
- AX raw per-family checks (10 families, 2 tasks each): 9 families both tasks pattern_match true, 1 family (`Change the delivery address` expecting `Save`) both false on homepage initial viewport.
- Mind2Web raw: HF train 1009 tasks, 73 websites (top `united 24`, `budget 24`), 3 domains (Travel 467, Shopping 281, Entertainment 261), no test_website/test_domain splits.
- Mapping validation: product-page vs homepage AX — Wish List homepage true vs product true (previously false/true), Cart homepage true vs product true.

### 3.3 DERIVED MEASUREMENT (fractions, CIs, thresholds)

- **WebArena thresholds** (frozen): family_reuse 0.9479≥0.5 PASS, param_task 0.8958≥0.3 PASS, exact_copy 0.0781<0.2 PASS, families_ge3 36≥5 PASS, families_ge4 34≥3 PASS.
- **AX_consistency** = 9/10 = **0.90**, threshold 0.6, **PASS**; bootstrap CI [0.70,1.00] **excludes threshold by 0.10 margin (≥0.05 required for SURVIVES)**; std 0.098. `tasks_live_extracted`=20, `families_checked`=10 satisfy spec ≥20/≥10. **Mapping**: 50 entries, longest-prefix without fallback, no generic Add.
- **Mind2Web**: `overlap` null (not computed), `excess` null, `shuffle_p95` null, `param_prevalence` null, `PC2` CANNOT_VERIFY — **MEASUREMENT_INVALID per Gate0**, not compared to 0.15/0.10 thresholds. TF-IDF/k-means `k` would have been `min(50,1009/20)=50` but not fitted due to Gate0; `k/2=25, 2k=100` sensitivity not executed; vocab/centroids hash null.
- **Controls**: PC1 PASS, PC2 CANNOT_VERIFY, NC1 NOT_EXERCISED, NC2 NOT_COMPUTED_MEASUREMENT_INVALID, NC3 PASS (0.0781<0.2), B1 CONFIRMED_SINGLE_STORE REJECTED, B2 gap 91.8% parametrized vs 0.80 heuristic, B3 bound exceeded (36>>2), B4 NOT_COMPUTED (audit-required website-label shuffle not fabricated), B5 disclosure.

### 3.4 INTERPRETATION (respecting frozen decision_rule, no overclaim)

- **Gate0**: WebArena PASS (SHA verified), Mind2Web MEASUREMENT_INVALID (revision 17ece8eb single train vs 137/31).
- **Clause1 WebArena within-store**: PASS (all thresholds + AX 0.9 + PC1 + 20/10 sampling) → **FALSIFIED-IN-SETTING for identifiable same-mechanism parameterized transfer is REJECTED; instead SURVIVES for within-store**.
- **Clause2 Mind2Web cross-website**: MEASUREMENT_INVALID → **not FALSIFIED-IN-SETTING**; requires re-run with pinned HF revision exposing official splits (or alternative dump) before claiming `overlap≥0.15` or `excess≥0.10`.
- **Clause3 SURVIVES** requires both axes PASS + CIs exclude thresholds by ≥0.05 + NC2/NC3 behave → **fails** (Clause2 not PASS).
- **Clause4 MIXED** (one PASS, other MEASUREMENT_INVALID) → **MIXED (within-store PASS, Mind2Web MEASUREMENT_INVALID) with per-axis bounded ceiling**.
- **Clause5** duplication 0.9479 with exact_copy<0.2 not MIXED trigger — superseded.

The **only surviving transfer substrate is within-store template-family holdout on WebArena-Verified v2 single store at element-pattern level**, demonstrated beyond template-count level (36 families) to live AX stability.

---

## 4. Controls and Baselines Detail

| ID | Expected | Observed | Pass | Evidence |
|---|---|---|---|---|
| **PC1_WEB_SEARCH** | homepage + re-extracted trees contain combobox Search + button Search, input#search placeholder, form /catalogsearch/result/ | PASS — 1426 nodes homepage, all 20 task-specific trees contain Search where expected, placeholder verified | **PASS** | `axtree_web_sample_task_specific.json` (20 trees) |
| **PC2_MIND2WEB_RECURRENCE** | ≥1 cluster in ≥10 tasks across ≥3 websites in official train | CANNOT_VERIFY — single train 73/3 insufficient to test official train recurrence | **CANNOT_VERIFY** | `mind2web_split_census.json` has_official_splits false |
| **NC1_WIKIPEDIA_NULL** | 0 shopping overlap (guarded) | NOT_EXERCISED — no Wikipedia container | null | correctly null not 0 |
| **NC2_MIND2WEB_SHUFFLE_NULL** | true exceeds shuffle mean by ≥0.10 and p95 (1000 perms seed 35725763380) | NOT_COMPUTED_MEASUREMENT_INVALID — 1000 website-label shuffles not computed due to missing official splits | null | `shuffle_null.json` explains Gate0, no synthetic 50/50 substituted |
| **NC3_WEB_EXACT_COPY_NULL** | exact_copy <0.2 | PASS 0.0781 [0.0417,0.1198] | **PASS** | census |
| **B1_DOC_M1_12STORES** | 12-store M1=1.0 REJECTED for v2 single store | CONFIRMED single store 187/5 site_tuples, single Docker | **REJECTED** | dataset + Docker |
| **B2_DOC_M2_HEURISTIC** | M2=0.80 inflation gap disclosure | param 0.8958/0.8367 exceeds heuristic, 91.8% parameterized | **Quantified** | census |
| **B3_SPIDER_2SITE** | lower bound 2-site corpus | 36 families >>2, 73 websites >>2 but split missing | **Exceeded** | census |
| **B4_SHUFFLE_NULL** | website-label permutation 1000 perms | NOT_COMPUTED_MEASUREMENT_INVALID | null | `shuffle_null.json` audit-required B4 correctly not fabricated; prior random split_point 0.6942 rejected |
| **B5_RETRIEVAL_REPLAY_STRONG** | disclosure-only 0-token replay 90ms 23k→0 | Not executed, future Product within-store holdout conditional | **Disclosure** | not claim LLM benefit |

All controls use frozen seed 35725763380.

---

## 5. Validity Threats and Mitigations

- **Representation loss**: `intent_template` may be coarser than true mechanism (search vs filtered search merged). Mitigated by live AX consistency at role/name level with longest-prefix mapping and disclosing template granularity; Mind2Web TF-IDF/k-means would have disclosed cluster counts and `k/2,2k` sensitivity if executed. No post hoc redefinition.
- **Sampling**: 20 trees across 10 families cannot cover 49 families exhaustively; stratified 2-per-family with frozen seed and below-fold exclusion limits claims to initial viewport task-specific pages only. Preferring families ≥3 ensures holdout realism vs homepage-only parent (15 trees, 7 families). Task-specific URL field completeness disclosed in `sampling.json` (16 homepage, 4 product .html).
- **Leakage**: Mind2Web website identity would have been kept train-only (vectorizer+k-means fitted train only, test via predict); shuffle null permutes website labels not mechanism labels preserving split sizes and fixed k-means. WebArena within-store is instance-level single store, no site leakage. Longest-prefix without fallback prevents generic `Add` leakage.
- **Infrastructure**: Docker/Playwright/HF rate limit — 3 retries, durable error, MEASUREMENT_INVALID vs FALSIFIED distinction preserved per Gate0. Director prior 5 (LLM/budget preflight) not applicable (no LLM).
- **Coarse clustering artifact**: Previous coarse mechanisms (33) inflated true and null together (0.814 vs 0.998); fine-grained TF-IDF/k-means `k=min(50,unique/20)` with website-label shuffle is the falsifier, but not executed due to Gate0 — correctly not claimed.
- **Overclaim**: Does NOT demonstrate LLM benefit, freshness guards, or delta-repair — product consequences conditional on substrate passing; kept RAW→OBSERVATION→DERIVED→INTERPRETATION distinct.
- **Browser context salience**: Acknowledged — future Product holdout using BrowserGym/AgentLab 1280x720 fresh grounding will mitigate path dependence; this Intel uses fresh per-task grounding with no accumulated trajectory.

---

## 6. Decision Rule (Frozen Ordered Evaluation)

**Gate0 Infrastructure**: WebArena JSON sha `d6527566...` matches pinned commit → PASS; Mind2Web HF revision `17ece8eb` single train 73/3 vs spec 137/31 → **that axis MEASUREMENT_INVALID/BLOCKED (NOT_APPLICABLE) not FALSIFIED**.

**Clause1 WebArena within-store**: family_reuse 0.9479≥0.5, param_task 0.8958≥0.3, exact_copy 0.0781<0.2, families_ge3 36≥5, ge4 34≥3, **AX_consistency 0.9≥0.6 (10 families, 20 trees, bootstrap margin 0.10)**, PC1 PASS → **PASS**; if AX null/<0.6/unmeasurable (<20 trees or <10 families or CDP fails or homepage-only navigation) → FALSIFIED-IN-SETTING, but **not triggered**.

**Clause2 Mind2Web**: spec-compliant TF-IDF/k-means on official splits **NOT executed** (Gate0) → **INCONCLUSIVE/MEASUREMENT_INVALID per audit required_fixes not falsified**; if executed and overlap<0.15 or excess<0.10 or overlap≤p95 or param<0.15 or PC2 fails → FALSIFIED-IN-SETTING.

**Clause3 SURVIVES**: requires Gate0 PASS AND Clauses 1+2 both PASS AND NC2/NC3 behave AND bootstrap CIs exclude thresholds by ≥0.05 → **fails** (Clause2 not PASS).

**Clause4 MIXED**: one PASS, other MEASUREMENT_INVALID → **MIXED with per-axis bounded ceiling** (within-store PASS, cross-website MEASUREMENT_INVALID).

**Clause5**: high duplication 0.9479 with exact_copy<0.2 **not** MIXED trigger — superseded.

Thresholds frozen; no post hoc relaxation.

---

## 7. Artifacts (stable paths, sha256 where practical)

| Path | SHA256 | Role | Note |
|---|---|---|---|
| `artifacts/raw/webarena-verified.json` | `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` | raw | Pinned commit ef74e1bfd..., 812/192/49 verified |
| `artifacts/raw/mind2web_split_census.json` | `6a2ba17ad...` | raw | HF revision 17ece8eb, single train 73/3/1009 divergence |
| `artifacts/raw/axtree_web_sample_task_specific.json` | `d6fefc1c...` | raw | 20 live CDP trees 627-1426 nodes, 1280x720, task-specific start_url |
| `artifacts/derived/measurements.json` | `85abe93f...` | derived | All metrics, bootstrap CIs, AX 0.9, decision MIXED |
| `artifacts/derived/bootstrap_ci.json` | `d8745ef5...` | derived | 2000 reps seed 35725763380, duplication/exact_copy/param/AX [0.7,1.0] |
| `artifacts/derived/shuffle_null.json` | `2a3afc77...` | derived | NOT computed - MEASUREMENT_INVALID, Gate0, no synthetic |
| `artifacts/derived/tfidf_kmeans_meta.json` | `ecde350d...` | derived | Frozen TF-IDF/k-means params, vocab/centroids null, k/2,2k not executed |
| `artifacts/derived/sampling.json` | `e6e84f23...` | derived | 20 tasks 10 families 2-per-family seed, resolved_url vs start_urls |
| `artifacts/derived/mind2web_split_census.json` | `6a2ba17a...` | derived | Same as raw |
| `research/intel/exp_35749371101_measure.py` | `a51ece43...` | code | Frozen measurement script, longest-prefix without fallback |

`provenance.json` records GitHub run 35749371101, base_sha `3c8ce37f...`, freeze hashes, Docker digest, Playwright 1.63.0, seeds, commands, environment.

---

## 8. Product Consequence

**MIXED WebArena PASS + Mind2Web MEASUREMENT_INVALID**: Product/Graph are **UNBLOCKED ONLY for within-store family holdout** on WebArena-Verified v2 (36 families ≥3, AX 0.9). Do **not claim cross-site generalization**; Mind2Web website-holdout remains diagnostic.

- **Next Product (within-store)**: Train N per family (2-train/1-test) on WebArena-Verified v2 single store, test held-out same family parameterized variant vs cold/retrieval/SPIDER with strong 0-token replay baseline (90ms TERX/HyperAgent 23k→0 framing per B5), measuring correct_resolution vs false_accept vs UNKNOWN ECE, not success alone, with BrowserGym/AgentLab 1280x720 fresh grounding. Seed 35725763380. Record TF-IDF/k-means artifacts for reuse if Mind2Web later unblocked.

- **Negative Mind2Web**: Cross-website not demonstrably same-mechanism beyond website-label null at this granularity (unknown due to split divergence); website-holdout limited to within-store families or custom benchmark/Mind2Web alternative until HF revision with 137/31 is pinned.

- **MEASUREMENT_INVALID/BLOCKED**: No falsification; next action infra repair is **find/pin Mind2Web HF revision or alternative dump exposing official train/test_task/test_website/test_domain (137/31), record revision hash, re-run TF-IDF/k-means train-only with 1000 shuffles, 2000 bootstraps, k/2,2k sensitivity**; do not treat as negative. WebArena axis remains valid regardless.

In all cases, ceiling remains **quantitative census (192/49 duplication 0.9479 exact 0.0781 param 0.8958 families 36/34/33) plus within-store element-pattern AX 0.9 [0.7,1.0]** with no LLM benefit demonstrated.

---

## 9. Related Codex and Handoff

- This experiment **replicates exactly** the WebArena census from parent `EXP-INTEL-35741921602` (192/49 duplication 0.9479 exact 0.0781 param 0.8958 families 36/34/33) and **extends it with the 5 audit-required repairs**: (1) longest-prefix mapping without `Add` fallthrough (50 distinct keys, sorted descending, validated product vs homepage), (2) task-specific navigation via `start_urls` (`__SHOPPING__`→`http://localhost:7770`, .html product paths) not `?task=` homepage, (3) ≥20 trees across ≥10 families 2-per-family seed 35725763380 (20/10 vs prior 15/7 and 8 families), (4) pinned HF revision hash `17ece8eb` with official split attempt and Gate0 MEASUREMENT_INVALID reporting (no synthetic substitution), (5) 2000 bootstraps + 1000 shuffles frozen, disclosed as not computed when Gate0 triggers, with per-artifact sha256.

- Parent `handoff.json` REVISE ceiling was **census-only quantitative** (AX 0.2857 MEASUREMENT_INVALID, Mind2Web single train 73/3). This experiment **raises the within-store ceiling to pattern-level (AX 0.9)** while correctly keeping Mind2Web as MEASUREMENT_INVALID.

- Codex `C-LLM-INHERIT` remains EXPERIMENTAL, `C-CROSSSITE` HYPOTHESIS per `codex/claim_state.json` — this MIXED result does not yet promote either to VALIDATED; within-store is viable substrate for future LLM-inherit test.

---

*Report keeps RAW EVIDENCE (counts, node counts, revision hashes, start_urls) distinct from OBSERVATION (fractions [0.9]) from DERIVED MEASUREMENT (threshold ≥0.6, bootstrap margin) from INTERPRETATION (viability, MIXED unblock). No material fact exists only in this narrative; canonical JSON is the machine handoff.*
