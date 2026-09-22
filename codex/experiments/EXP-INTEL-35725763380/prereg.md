# EXP-INTEL-35725763380 Preregistration — Intel Dataset Verification for C-LLM-INHERIT

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-35725763380
- **Lane**: Intel
- **Claims**: C-LLM-INHERIT (primary), C-CROSSSITE (secondary diagnostic for website-holdout feasibility)
- **Parent Handoff**: EXP-INTEL-35697055679 (verdict: MIXED, audit: PASS) — path `research/experiments/EXP-INTEL-35697055679/handoff.json`, sha256 `fc4bab31654c5ee192a49dac9ca00ea2311a5bc58a1789232e75954399d2b9c8`
- **Director Mandate**: PIVOT to C-LLM-INHERIT with cognitive reset, SUPERSEDE parent handoff — `research/experiments/EXP-INTEL-35725763380/request.json` (cycle 35725295819, allocation action PIVOT, target claim C-LLM-INHERIT, parent_handoff_disposition SUPERSEDE)
- **Date**: 2026-09-22
- **Status**: DESIGN — NOT YET FROZEN

## 2. Scientific Question

Can within-store template-family hold-out (train on N tasks of a family, test on held-out tasks of same family) on WebArena-Verified v2 single shopping store provide identifiable same-mechanism parameterized transfer for C-LLM-INHERIT, and does Mind2Web cross-website splits show measurable same-mechanism overlap when inspected at task-sample accessibility-tree level — quantifying duplication fraction, parameterization prevalence and cross-task mechanism overlap to resolve documentation-assumed VF5 and design true website-holdout?

This is the binding Director strategic question. DESIGN refines it into the smallest rigorous falsifiable measurement that can change a claim/product decision without re-running a synthetic DGP or merely repeating documentation surveys.

## 3. Motivation and Inherited State

### 3.1 Why This Is Highest Information

Per Global Research Director portfolio assessment (request.json: portfolio_assessment): at 221 canonical experiments SPIDER is narrowly measurement-valid on localhost Flask/JWT but FALSIFIES on infrastructure, four lanes tunnelled on synthetic DGP loops, and central promise — later-agent cost ~ residual novelty vs full task beating cold/retrieval and TERX 0-token replay — remains untested. C-DELTA-REPAIR has 0 experiments, C-RESIDUAL-NOVELTY only doc survey, C-PARAM-INHERIT narrow POC, C-LLM-INHERIT and C-CROSSSITE blocked on unverified dataset assumptions. Highest marginal information is breadth to starved claims with strong replay baseline, not 31st orthogonality test. This experiment is sequenced before any LLM-costly ranking (n=50/82) or distributed session scale-up: mechanism overlap must be verified at sample level first, otherwise ranking mixes incomparable mechanisms.

### 3.2 Parent Handoff Continuity (Preserved Distinctions)

The parent handoff EXP-INTEL-35697055679 is continuity evidence only per SUPERSEDE and must not silently override the Director decision. We preserve its four-way carry_forward exactly:

**Established** (must not be re-assumed or re-tested as hypothesis):
- WebArena-Verified v2 shopping is exactly ONE Magento One Stop Market store (single container, 192 tasks over 49 intent_templates, zero shopping_0..11 identifiers) — census M6=1, site tuples 187 shopping +5 shopping+reddit.
- Cross-store overlap metric is vacuous null, not 0.0; literal 0.0 is absent-measurement artifact.
- Documentation-level M1=1.0 (12 stores) is falsified as a dataset property for v2; it is a WebArena v1 property.
- Within-store reuse is high: duplication 0.9479 (182/192 share template, CI [0.9167,0.9792]) but exact-copy 0.0781 (15/192 identical template AND instantiation_dict), so 91.8% of reuse is parameterized variation.
- Parameterization prevalence 0.8958 task (172/192) / 0.8367 template (41/49).
- Template reuse proxy 39/49 templates appear >=2 tasks.
- Positive control PASS: homepage AX 1426 nodes contains Search combobox+button, add-to-cart 87 / wish-list 84 / compare 84.
- Intent-to-element 5/5 PASS, live extraction 10/10 at 1280x720 via CDP.

**Rejected** (must not be revived without new evidence):
- v2 provides 12 shopping store instances; cross-store overlap <0.5 as store-specificity inference; duplication = verbatim copy; train-on-N-stores hold-out on v2 is buildable — all REJECTED bounded to v2.

**Unknown** (this experiment directly targets):
- Whether template-family hold-out within single store is identifiable same-mechanism transfer (was unresolved[0]).
- Whether Mind2Web cross-website splits provide true same-mechanism overlap (audit VF6, unresolved[2]).
- Below-fold/post-interaction coverage (unresolved[3], bounded out here).

**Do_not_assume** (explicitly guarded):
- Vacuous null ≠ falsified C-CROSSSITE; high duplication ≠ verbatim copies; 0.8958 prevalence ≠ LLM inheritance benefit; homepage elements ≠ full checkout execution; within-store families ≠ cross-site.

### 3.3 What This Experiment Is and Is Not

This IS: a sample-level dataset census + accessibility-tree verification that enumerates template-family hold-out viability on the single shopping store and measures Mind2Web cross-website overlap at operation-template level with shuffled null. It quantifies duplication fraction, parameterization prevalence, and cross-task mechanism overlap — the exact VF5/VF6 gaps flagged by audits.

This IS NOT: an LLM agent inheritance test (no cold vs retrieval vs SPIDER execution), not a browser end-to-end execution of cart/checkout flows, not a re-tuning of viewport heuristics, and not a repetition of the 12-store cross-site question on v2 (already shown impossible). It also does not claim freshness, delta-repair, or product economics beyond substrate viability disclosure.

## 4. Hypotheses

### H1_WEB_HOLDOUT — Within-store family hold-out is identifiable

Operational: On WebArena-Verified v2 single store, intent_template defines mechanism. Same-mechanism parameterized transfer is identifiable if: family-reuse comparable to parent (≥0.5 of templates appear ≥2 times), task-level parameterization ≥0.3 (non-empty instantiation_dict), exact-copy <0.2, and at least 5 families have ≥3 tasks (enabling 2-train/1-test) with 3 families having ≥4 tasks.

Expected direction: PASS — parent already shows 0.7959 family reuse, 0.8958 parameterization, 0.0781 exact-copy, so viability is likely but must be enumerated per-family size distribution and AX-verified.

### H2_WEB_AX_CONSISTENCY — Same template → same mechanism elements

Sampled AX trees for tasks sharing same intent_template must map to same element pattern (e.g., search → combobox+button, add-to-cart → button with specific role/name, reviews → review-list region). AX consistency = fraction of sampled families where both tasks of same family contain the template-required element pattern at initial viewport. Threshold ≥0.6.

### H3_MIND2WEB_OVERLAP — Cross-website splits share mechanisms

Mind2Web operation templates (normalized clusters) that appear in test_website also appear in train at fraction ≥0.15 and exceed shuffled-website null by ≥0.10. This demonstrates that cross-website hold-out is not merely testing unseen layouts but testing same abstract mechanism on new sites.

Expected direction: uncertain — documentation M1 inflated 0.8182 vs corrected 0.311 suggests true overlap may be low; measurement resolves.

### H4_HEURISTIC_DISCLOSURE — Parameterization and duplication are heurstic-inflated

Measured Mind2Web parameterization prevalence (fraction of tasks with variable TYPE/SELECT slots) will be materially lower than heuristic M2=0.65, and WebArena duplication 0.9479 will be shown to be parameterized (exact-copy <0.2), disclosing that documentation-level scores overstate copy risk.

## 5. Methods

### 5.1 Datasets and Pinning

- **WebArena-Verified v2**: `assets/dataset/webarena-verified.json` from ServiceNow/WebArena-Verified commit `ef74e1bfd0d83d4bab1c55b2d1b4c2aeaac8e0d0`, local sha256 `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` (812 tasks). Also verify `test.raw.json` (812/192) and `webarna-verfied-hard.json` (258/61) censuses for consistency. Any sha divergence is reported and does not silently substitute another file.
- **Mind2Web**: HuggingFace `osborne-nlp/Mind2Web` or `OSU-NLP/Mind2Web` (canonical NeurIPS 2023, 137 websites, 31 domains, ~2350 tasks) via `datasets` library. Record dataset revision hash, download date, and split file census. Splits: `train`, `test_task`, `test_website`, `test_domain` per official `data/*.json`.

If Mind2Web HF is unreachable after 3 retries with backoff, record BLOCKED with durable error (HTTP status, timestamp) and do not fall back to documentation.

### 5.2 Mechanism Definitions (Frozen Before Measurement)

- **WebArena mechanism**: `intent_template` string as stored in dataset (e.g., `Search for {{product}}`). Parameterization = `instantiation_dict` non-empty (task-level) or template has ≥2 distinct instantiations across tasks (template-level).
- **Mind2Web mechanism**: normalized operation-template cluster = `(action_type, target_semantic_role, intent_verb_lemma)` where action_type ∈ {CLICK, TYPE, SELECT, HOVER, PRESS}, target_semantic_role derived from `target` HTML snippet (tag + aria role) and candidate element description, intent_verb lemma from `task` instruction (search, book, compare, filter...). Clustering is deterministic: TF-IDF on (task + action target text) → k-means with k chosen by frozen seed heuristic (k = min(50, unique_tasks/20)) fitted on train split only, then applied to test splits. No test leakage. Fallback if clustering unstable: exact `(action_type, verb_lemma)` bigram.

These definitions are code-frozen in `research/intel/exp_35725763380_measure.py` before any metric is computed.

### 5.3 WebArena Census and Hold-out Enumeration

1. Parse `webarena-verified.json`, filter site tuple containing shopping, count tasks, distinct intent_templates, per-template task counts.
2. Compute: duplication_fraction = tasks whose template appears ≥2 / total; exact_copy_fraction = tasks with identical (template AND instantiation_dict) appearing ≥2 / total; parameterization fractions task/template; family sizes histogram; families_with_≥3, ≥4, ≥5 tasks; usable hold-out families list.
3. Bootstrap 95% CIs (2000 reps, seed 35725763380) for duplication, exact-copy, parameterization, and family-reuse fractions.

### 5.4 Accessibility-Tree Sample Verification (WebArena)

- Sample: stratified 15 tasks across ≥10 families, aiming for 2 tasks per family where size ≥2. Use frozen seed 35725763380, preferring families with ≥3 tasks to test hold-out realism. If Docker unavailable, reuse parent 10 AX trees (`research/experiments/EXP-INTEL-35697055679/artifacts/raw/axtree_*.json`) with explicit provenance label REUSED, not re-extracted.
- If Docker available: run `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` at `http://localhost:7770`, extract CDP `Accessibility.getFullAXTree` at 1280x720 initial viewport (no scroll) for each sampled task's start URL. Save with sha256.
- AX consistency: for each sampled family, check whether both tasks' AX trees contain the template-required element pattern (pre-registered mapping table: search→combobox+button, add-to-cart→button role `Add to cart`, wish-list→link `Add to Wish List`, reviews→region `Reviews`, etc.). Consistency = families passing / families sampled. Manual inspection of 3 families for sanity.

### 5.5 Mind2Web Cross-Website Overlap Measurement

1. Load Mind2Web HF dataset, enumerate splits, verify task counts per split.
2. Extract mechanism label per task via frozen clustering (trained on train only). For each task, derive its mechanism set (1 label per task for single-step; or majority label for multi-step — pre-registered as first-action mechanism to avoid multi-label ambiguity).
3. Compute: overlap_fraction = |M_test_website ∩ M_train| / |M_test_website|; similarly for test_domain and test_task (diagnostic). Also compute duplication_fraction (tasks sharing same mechanism label / total) and parameterization_prevalence (tasks with TYPE or SELECT operation containing variable value / total) per split.
4. Shuffled null: permute website labels across train+test_website 1000 times (seed 35725763380), recompute overlap each perm, record mean/std and 95th percentile. True overlap must exceed 95th percentile and exceed mean by ≥0.10.
5. Bootstrap CIs for overlap and parameterization.

### 5.6 Controls

- **PC1_WEB_SEARCH**: must find Search combobox+button on homepage AX (node count ~1150-1426, matches parent task 514). Failure → measurement error.
- **PC2_MIND2WEB_RECURRENCE**: at least one operation-template cluster appears in ≥10 tasks across ≥3 websites in train (proves recurrence detectable).
- **NC1_WIKIPEDIA_NULL**: guarded Wikipedia Docker check — if container absent, report NOT EXERCISED (null, not 0).
- **NC2_SHUFFLE_NULL**: shuffled overlap per §5.5(4).
- **NC3_EXACT_COPY**: WebArena exact-copy <0.2 distinguishes parameterized reuse from copies.

### 5.7 Artifacts

- `artifacts/raw/webarena-verified.json` (sha `d6527566...`, reused with hash verification)
- `artifacts/raw/mind2web_split_census.json` (HF revision, counts, hashes)
- `artifacts/raw/axtree_web_sample_*.json` (15 trees, or REUSED label)
- `artifacts/derived/measurements.json` (all metrics, per-family sizes, per-split overlap, bootstrap CIs, shuffle distribution)
- `artifacts/derived/bootstrap_ci.json` and `artifacts/derived/shuffle_null.json`
- `research/intel/exp_35725763380_measure.py` (frozen measurement script, sha recorded in provenance.json)

## 6. Decision Rule (Frozen)

Ordered evaluation; first failing infrastructure gate takes precedence over scientific falsification.

**Gate 0 — Infrastructure**: if WebArena JSON sha unavailable/mismatch irreconcilable or Mind2Web HF unavailable after 3 retries → `status=MEASUREMENT_INVALID` or `BLOCKED` (per failure taxonomy), `outcome=NOT_APPLICABLE`, verdict deferred. Not a scientific falsification.

**Clause 1 — WebArena within-store axis**: family_reuse <0.5 OR parameterization_task <0.3 OR exact_copy ≥0.2 OR families_≥3 <5 OR families_≥4 <3 OR AX_consistency <0.6 OR PC1 fails → FALSIFIED-IN-SETTING for within-store hold-out viability.

**Clause 2 — Mind2Web cross-website axis**: overlap <0.15 OR (overlap - shuffled_mean) <0.10 OR parameterization_prevalence <0.15 OR PC2 fails → FALSIFIED-IN-SETTING for same-mechanism cross-website transfer.

**Clause 3 — SURVIVES**: if Gate 0 passes AND Clauses 1 and 2 both pass AND NC2/NC3 behave (shuffled overlap low, exact-copy low) AND bootstrap CIs exclude thresholds by ≥0.05 → `SURVIVES_CURRENT_TEST`. Ceiling: within-store family hold-out is viable identifiable same-mechanism substrate; Mind2Web provides measurable cross-website overlap for future website-holdout.

**Clause 4 — MIXED**: one axis passes, the other is FALSIFIED → `MIXED` with per-axis bounded ceiling (declare which transfer axis is viable; do not overclaim cross-site if only within-store survives).

**Clause 5 — Duplication handling**: high duplication 0.9479 is NOT a trigger for MIXED when exact-copy <0.2; parent MIXED duplication clause is superseded. Report duplication decomposition explicitly.

Thresholds are frozen; no post hoc relaxation.

## 7. Baselines and Controls Summary

See spec.json `baselines` B1-B5, `positive_control`, `null_control`. Stable IDs: B1_DOC_M1_12STORES, B2_DOC_M2_HEURISTIC, B3_SPIDER_2SITE, B4_SHUFFLE_NULL, B5_RETRIEVAL_REPLAY_STRONG, PC1_WEB_SEARCH, PC2_MIND2WEB_RECURRENCE, NC1_WIKIPEDIA_NULL, NC2_MIND2WEB_SHUFFLE_NULL, NC3_WEB_EXACT_COPY_NULL.

## 8. Validity Threats and Mitigations

**Representation loss**: intent_template may be coarser than true mechanism (e.g., search vs filtered search merged). Mitigated by AX consistency check at element-pattern level and by disclosing template granularity. Mind2Web clustering may merge distinct mechanisms or split same mechanism — disclosed via cluster count sensitivity (report k/2 and 2k as exploratory).

**Sampling**: 15 WebArena AX trees cannot cover 49 families exhaustively; stratified sampling with frozen seed and explicit below-fold exclusion limits claims to initial viewport. Mind2Web HF version drift — pinned revision and hash.

**Leakage**: Mind2Web website identity must not leak into mechanism clustering; clustering fit on train only. WebArena template hold-out split is instance-level, not site-level; no site identity to leak (single store).

**Infrastructure**: Docker optional; HF auth/rate limit — 3 retries, durable error. No LLM cost.

**Overclaim**: This experiment does NOT demonstrate LLM benefit, freshness, or repair. C-LLM-INHERIT remains EXPERIMENTAL pending future Product experiment (cold vs retrieval vs SPIDER on this substrate). Validity_notes will carry this ceiling.

## 9. Product Consequence

See spec.json `product_consequence_positive` / `product_consequence_negative`. Positive unlocks Product/Graph designs for within-store hold-out and Mind2Web website-holdout; negative bounds to surviving axis or to 2-site corpus.

## 10. Analysis Plan

- Compute all metrics deterministically with seed 35725763380.
- Bootstrap 95% CIs (2000 reps) for WebArena duplication/exact-copy/param/family-reuse and Mind2Web overlap/param.
- Shuffle null 1000 perms for Mind2Web overlap.
- Report per-family size histogram, list of hold-out-viable families, AX consistency table, Mind2Web per-split overlap table, and comparison to documentation heuristics (B1/B2) with gap quantified.
- Preserve raw and derived artifacts with sha256 for audit recomputation.
- Report.md will not exceed frozen claim ceiling and will distinguish RAW EVIDENCE (JSON counts, AX node counts) from DERIVED MEASUREMENT (fractions, CIs) from INTERPRETATION (viability).

## 11. Estimated Cost and Information Gain

- **Cost**: LOW — <2h compute, <3GB /tmp, no LLM API, stdlib+datasets+optional playwright.
- **Information gain**: HIGH — resolves VF5/VF6 at sample level, prerequisite for any valid residual-novelty or LLM-inheritance measurement, portfolio-level before costly ranking.

## 12. Time and Resource Estimate

- Dataset pinning and census: 0.5h
- Sampling, optional AX extraction (15 trees): 0.5-1h
- Mind2Web download/cluster/overlap/shuffle: 1h
- Bootstrap and reporting: 0.5h
- Total: ~2-3h

## 13. Falsification and Audit Preparation

All code paths for decision_rule clauses are unit-tested with synthetic fixtures (mock 1-store and mock overlap at/below threshold) before execution. Audit recomputation is enabled by freezing seeds, pinning revisions, and preserving raw JSONs. Failure modes are not re-labeled as negatives.

---
*Preregistration frozen before outcome inspection. Any analysis deviating from this plan after seeing results will be labeled exploratory and requires a new preregistration for confirmatory claims.*
