# EXP-PHYSICS-35741898214 — Preregistration

## Status
DESIGN ONLY. Not yet frozen. No outcome-bearing measurements have been inspected.

## Experiment Identity
- **Experiment ID:** EXP-PHYSICS-35741898214
- **Lane:** physics
- **Claim:** C-CROSSSITE (Reusable mechanisms transfer across website holdout)
- **Director Mandate:** PIVOT (SUPERSEDE) — `allocation.action=PIVOT`, `claim_id=C-CROSSSITE`, `parent_handoff_disposition=SUPERSEDE`, `cognitive_reset=true`
- **Parent Handoff:** EXP-PHYSICS-35697037202 (MIXED, lag-1 autocorrelation on TodoMVC hash-SPA, 5-state deterministic FSM, audit notes encoding sensitivity, sample collapse, Markov-1 sufficiency) — superseded, not continued. Its `next_question` (real user sessions on TodoMVC) is advisory only and is NOT pursued. Established/rejected/unknown/do_not_assume distinctions from parent are preserved below but do not drive design.
- **Dependencies:** intel (dataset censuses prerequisite)
- **Registry:** claims/registry.json sha256 3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b, base_sha e606e040dfa1154aa4bae2ae4b456f81fd16781c

## Strategic Context

### Why this pivot
Physics has 42 consecutive C-WEB-DYNAMICS experiments (58 total, 40+ FALSIFIED-IN-SETTING + ~15 MEASUREMENT_INVALID). The first Bayesian Dirichlet-Multinomial estimator to pass C1+C3 shows absolute BF negative (-10 to -15 nats M0 favored) on real TodoMVC hash-SPA despite relative BF 168-643 nats vs K12 null (p0.0005). kNN/KDE TV detects only translation-like dynamics (rho 1.0 d9.1) with scaling rho -0.12 and rotation blind spots even after bias correction. PMI leakage 78-92% (href==url) and self-loops 17-49% confounded prior signals. The Director judged marginal information from another PMI/TV K-tuning as near zero and chose an orthogonal high-leverage test: true website-holdout transfer directly exercises C-CROSSSITE `next_gate` (true website holdout without site identity leakage) with strong falsifiability and product unblocking value.

Portfolio assessment notes 224 canonical exps are tunnel-trapped (Graph 30/C-FRESHNESS, Runtime 40/C-MEAS-VALID, Physics 42/C-WEB-DYNAMICS), with C-CROSSSITE/C-LLM-INHERIT at census-only (WebArena 192 tasks duplication 0.9479 param 0.8958 but AX_consistency null) and Mind2Web 33-heuristic non-compliant.

### Inherited state handling (SUPERSEDE)
- **Preserved established:** TodoMVC lag-1 ACF 0.418-0.454 explained by Markov-1 (parent); WebArena-Verified v2 single-store vacuity (EXP-INTEL-35697055679/35725763380: exactly one Magento One Stop Market, 192 tasks, 49 templates, 36 families >=3, cross-store overlap is vacuous null not 0.0); Mind2Web censuses not measured to spec (33 heuristic vs required TF-IDF, synthetic shuffle vs official splits).
- **Preserved rejected:** Cross-store holdout on WebArena-Verified v2 as dataset property (falsified); coarse 33-mechanism heuristic as compliant measure; synthetic 60/40 website shuffle as official split.
- **Preserved unknown:** Whether TF-IDF->k-means text mechanisms transfer across true holdout; whether AX element-pattern consistency (>=0.6) holds.
- **Do not assume:** That lag-1 ACF represents Web dynamics; that family-level holdout equals cross-store holdout; that documentation M1=1.0 (12 stores) applies to v2.
- **Disposition:** The parent's timescale question is explicitly NOT pursued. This design tests a new claim (C-CROSSSITE) per binding `director_mandate`.

## Research Question

> Does a true website-holdout test — WebArena-Verified v2 family-level holdout and Mind2Web official train/test_website/test_domain splits with spec-compliant TF-IDF→k-means (k=min(50, unique_tasks/20) fitted train-only), 1000 website-label shuffles, and k/2 / 2k sensitivity — show same-mechanism parameterized overlap exceeding the shuffled null by ≥0.10 without site-identity leakage, using only task + action target text?

## Claims and Next-Gate Mapping
- **C-CROSSSITE:** HYPOTHESIS → next_gate = "true website holdout without site identity leakage". This experiment is the gate. C-WEB-DYNAMICS deliberately PARKED (not tested here). A positive result advances C-CROSSSITE to EXPERIMENTAL (bounded); a negative bounds the text-proxy mechanism on these datasets/k.

## Hypotheses

### H1 (Primary, two datasets)
Same-mechanism parameterized overlap exceeds the shuffled null by ≥0.10.

**Operational definitions:**

- **Mechanism:** k-means cluster ID on TF-IDF vectors of *clean* task+action text. Text = lowercase concatenation of task goal/intent utterance + action target element text (WebArena: `intent` + `instantiation_dict` values concatenated + task utterance; Mind2Web: `confirmed_task`/intent + `action.target_element_text`/`action.target_name`+ target role). Preprocessing: URL/domain/shop-name regex `https?://\S+|www\.\S+|[\w-]+\.(com|org|net|io)` removed, site/store names (magento/one stop market, 137 Mind2Web website names) removed via stoplist built from website/domain metadata, lowercased, English stopwords removed via TfidfVectorizer, ngram_range (1,2).

- **Vectorizer:** `sklearn.feature_extraction.text.TfidfVectorizer(max_features=5000, min_df=2, max_df=0.9, ngram_range=(1,2), stop_words='english')` fitted **TRAIN ONLY**.

- **Clustering:** `sklearn.cluster.KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)` fitted on train TF-IDF matrix. `k = min(50, floor(n_unique_train_task_goals / 20))`. `n_unique_train_task_goals` = number of unique lowercased task-goal strings in train. Sensitivity at `k/2` (floor, min 2) and `2k` (min 100 cap).

- **Overlap metric:** For each held-out set T (WebArena held-out families; Mind2Web test_website and test_domain), assign clusters via `vectorizer.transform` → `kmeans.predict`. Let `C_train` = set of cluster IDs present in train, `C_test` = set present in test. `overlap_observed = |C_train ∩ C_test| / |C_test|`. Also report instance-level `overlap_instance = n_test_assigned_to_train_clusters / n_test`.

- **Null:** 1000 website/family label shuffles preserving per-entity task counts. For Mind2Web shuffle website labels among tasks (keeping each website's n_tasks); for WebArena shuffle family labels among tasks. For each shuffle b, redo TM split by shuffled labels (shuffled holdout defined analogously), refit TF-IDF+kmeans on shuffled-train only, compute `overlap_null[b]`. Then `delta = overlap_observed - mean(overlap_null)`, `p = (1 + #{null>=observed})/1001`, `p95 = 95th percentile of null`.

H1 passes iff delta ≥0.10 and observed > p95 (p<0.05) on every primary holdout.

### H2 (Sensitivity)
Result is not fragile to k. Delta ≥0.10 direction preserved at k/2 and 2k on all three holds (sign preserved, no sign flip).

## Datasets and Splits

### A. WebArena-Verified v2
- Source: `web-arena/web-arena-verified` or local census `EXP-INTEL-35725763380` artifacts (192 shopping tasks, 49 intent_templates, 36 families with ≥3 tasks). Verified single shopping store.
- **True holdout:** family-level holdout (within-store family generalization) — hold out 20% of families (7 families) in 5 random folds (seed 42). Family = intent_template group (e.g., shopping `add_to_cart`, `search_product`, `checkout`). This is NOT cross-store; cross-store is vacuous (document as established). Report mean±std over 5 folds.
- Holdout families ensure instantiation_dict variation is preserved (parameterized variation within family).

### B. Mind2Web
- Source: HuggingFace `osunlp/Mind2Web` (official splits: `train`, `test_website`, `test_domain`; optionally `test_task`). Use exact official splits referenced by dataset_revision hash (record `dataset_revision` and `train/test_website/test_domain` n_tasks/n_websites). If HF revision lacks 3-way splits or reports 73/3 instead of spec 137/31, declare MEASUREMENT_INVALID with revision hash rather than fabricating splits.
- Holdouts: `train` vs `test_website` (C1), `train` vs `test_domain` (C2). `test_task` reported exploratorily only.

### Text hygiene
- Only clean text used for primary. Leakage diagnostic `B-SITE-LEAKAGE` adds URLs/domains back and shows inflation >0.05 if leakage matters.
- Verify top 100 TF-IDF features contain no domain/url token after cleaning; save vocab list.

## Baselines and Controls

| ID | Type | Purpose | Expected |
|---|---|---|---|
| B-SHUFFLE-WEBSITE | Null (primary) | Chance overlap due to cluster cardinality | null mean 0.3-0.7; observed must beat p95 by ≥0.10 |
| B-SITE-LEAKAGE | Diagnostic | Site-identity mediation | leakage > clean by >0.05; clean still > null |
| B-RANDOM-SPLIT | Reference | Upper bound without holdout | random 80/20 overlap 0.75-0.90 |
| B-LEXICAL-OVERLAP | Reference | Token Jaccard without clustering | ~0.6-0.8 |
| POS-WITHIN-SAME-WEBSITE | Positive control | Pipeline detects known sharing | overlap ≥0.50 delta ≥0.20 p<0.01 |
| NULL-INDEPENDENT-DOMAINS | Null control | Collapse check | delta ≤0.05 p>0.10 |

Controls must be computed with same code path (train-only fit) as primary.

## Measurement Validity and Physics Gates

1. **Target integrity:** No predictor contains site/store label deterministically; task+action text only.
2. **Split integrity:** All preprocessing fit TRAIN ONLY; verified by code audit (transform vs fit_transform).
3. **Sampling integrity:** Deterministic seeds; policy explicit (family label permutation, website label permutation).
4. **Uncertainty integrity:** Resampling unit = website/family, not individual task; correlated transitions within website not treated as independent.
5. **Representation integrity:** Raw task text preserved; TF-IDF losses documented; overlap defined on cluster sets (operational mathematical object with falsifier delta<0.10).
6. **Identifiability:** k-means is identifiable up to permutation; overlap metric is permutation-invariant (set intersection).
7. **Data sufficiency:** WebArena 192 tasks (36 families), Mind2Web ~1000 tasks; if any held-out set has <20 tasks, report INCONCLUSIVE for that set, not falsified.

## Decision Rule (pre-frozen, exact)

Let `delta_k = overlap_observed_k - mean(null_k)` at each primary k.

- **Conditions:**
  - C1: Mind2Web test_website delta_k ≥0.10 and observed_k > p95_k (p<0.05)
  - C2: Mind2Web test_domain delta_k ≥0.10 and p<0.05
  - C3: WebArena family holdout mean delta_k ≥0.10 and p<0.05 (mean over 5 folds; per-fold p computed vs 1000 family-shuffled nulls; aggregate p via mean delta vs pooled null)
  - PC: Positive control overlap ≥0.50 and delta ≥0.20 p<0.01
  - NC: Null control delta ≤0.05 p>0.10
  - SENS: At k/2 and 2k, deltas on C1,C2,C3 remain ≥0.10 in same direction (no sign flip)

- **Verdict mapping:**
  - `SURVIVES_CURRENT_TEST` iff C1 ∧ C2 ∧ C3 ∧ PC ∧ NC ∧ SENS. Claim ceiling: TF-IDF→k-means text mechanisms transfer across true website/family holdout beyond chance by ≥0.10 without leakage on these datasets.
  - `FALSIFIED-IN-SETTING` iff any C1/C2/C3 fails delta<0.10 or p≥0.05 while PC passes and NC passes (valid negative). Bounded to this k/text-proxy on these datasets; not proof transfer impossible.
  - `MIXED` iff WebArena C3 passes but Mind2Web C2 (domain) fails while C1 passes — stricter domain shift boundary.
  - `MEASUREMENT_INVALID` iff split leakage (fit on test), WebArena cross-store misuse, official Mind2Web splits unavailable, or cluster collapse (>40% tasks in one cluster).

Report: overlap_observed, overlap_null_mean, null_std, p95, delta, p, |C_train|, |C_test|, |C_overlap|, cluster histogram, and per-k table for k/2, k, 2k.

## Product / Claim Consequences

- **Positive (SURVIVES):** C-CROSSSITE moves HYPOTHESIS → EXPERIMENTAL (bounded to TF-IDF text proxy). Unblocks Graph/Product to design within-store family holdout (WebArena, 36 families 2-train/1-test) and cross-website (Mind2Web) parameterized inheritance experiments. Next mandatory step: element-pattern AX consistency (≥0.6, 15 tasks 2-per-family live CDP at 1280x720, per EXP-INTEL-35725763380) and then LLM-agent benefit vs cold/retrieval/SPIDER.
- **Negative (FALSIFIED/MIXED):** C-CROSSSITE stays HYPOTHESIS with ceiling: bag-of-words text clusters alone do not transfer across true holdouts by ≥0.10. Does NOT close domain — directs Frontier/Graph to test richer mechanisms (DOM/AX patterns, learned embeddings, state-conditioned actions) before product routing. Product stays bounded to 2-site corpus or within-store reuse only.

## Estimated Cost and Information Gain

- **Cost:** Low — offline compute only. 1-2h CPU, <2GB RAM, ~6000 k-means fits (1000 shuffles × 3 ks × 2 datasets + controls). No Docker/Playwright/LLM. Network: HF downloads.
- **Information gain:** High — first spec-compliant measurement correcting three prior REVISE causes (heuristic → TF-IDF train-only, synthetic split → official, split_point label shuffle → count-preserving website permutation). First discriminating test of C-CROSSSITE next_gate; changes routing regardless of sign.

## Analysis Plan (frozen steps)

1. Fetch WebArena-Verified v2 census/tasks (or reuse EXP-INTEL-35725763380 artifacts) and Mind2Web official HF splits; record hashes/revisions; verify single-store vacuity for WebArena and website counts for Mind2Web.
2. Build clean text (task+action only) per dataset; verify leakage removal via vocab audit.
3. Compute k per dataset (min(50, unique_train/20)) and k/2, 2k.
4. For each k: fit TF-IDF train-only → kmeans train-only → assign test → compute overlap_observed, instance overlap, lexical Jaccard.
5. For each shuffle b=0..999: permute website/family labels preserving counts, repeat fit+assignment+overlap → build null.
6. Compute delta, p, p95; repeat for leakage, random-split, lexical baselines; run positive/negative controls.
7. Tabulate C1/C2/C3/PC/NC/SENS and apply decision rule without post hoc threshold changes.

## Validity Threats and Mitigations

- TF-IDF captures lexical not structural mechanisms → bounded to text-proxy; do not claim element-pattern transfer.
- k selection influences cardinality → sensitivity at k/2 and 2k required; cluster collapse check.
- WebArena family definition is template-based not site-based → explicitly bounded as within-store family generalization, not cross-site.
- Mind2Web website/domain metadata may be noisy → report dataset_revision and website count; if counts diverge from spec 137/31, report as MEASUREMENT_INVALID for that axis.
- Shuffled null may be high if k small → delta threshold already accounts for marginal; report null mean.

## Preregistration Freeze
Hypothesis, state (clean text) representation, action (cluster) representation, target (overlap), sampling policy, holdout unit (website/family), nulls/baselines, primary metric (delta ≥0.10), direction (observed > null), uncertainty (1000 permutation), adequacy (≥20 test tasks), and falsification rule are frozen above before outcome inspection. Any analysis change after seeing outcomes is exploratory and requires a new preregistration.

