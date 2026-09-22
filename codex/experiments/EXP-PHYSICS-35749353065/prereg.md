# EXP-PHYSICS-35749353065 Preregistration — Physics Orthogonal Factorization

**Status: DESIGN — FROZEN BEFORE OUTCOME (2026-09-22). No outcome-bearing measurements have been inspected.**

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35749353065
- **Lane**: physics
- **Claim**: C-WEB-DYNAMICS — Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity
- **Directive**: Global Research Director PIVOT on C-WEB-DYNAMICS (request.json director_mandate, cycle 35748646600) — orthogonal falsifiable program not based on TV/KDE/binned PMI density divergence; specifically effect factorization with session/state-correlated non-determinism (DOM_before correlates with latent state), or barrier/committor, or timescale separation, tested on Intel-supplied production SPAs with leakage-free actions and history-conditioned PMI/CMI.
- **Parent handoff**: research/experiments/EXP-PHYSICS-35741898214/handoff.json — disposition **SUPERSEDE** per director_mandate (parent_handoff_disposition SUPERSDE, cognitive_reset true). Parent proposed recovering Mind2Web/WebArena website-holdout corpus for C-CROSSSITE TF-IDF test; that agenda is **not** pursued here. Preserved distinctions: TF-IDF pipeline operational but splits unavailable (MEASUREMENT_INVALID) is continuity evidence only, not the research objective for this experiment.
- **Dependencies** (binding): (a) Intel production SPA manifest with title variation and non-leakage density (NL≥50, H(S_next|URL,H_K=3)>0.2 bits, leakage<40%); (b) runtime writable/intervention-valid substrate for factorization (auth/session controls) — used as synthetic positive/negative controls, not required for production SPA observational test.
- **Pre-2.0 baseline**: 58 C-WEB-DYNAMICS experiments synthetic-only, one SURVIVES_CURRENT_TEST (2D continuous), complementary blind spots (kNN fails scaling rho=-0.12, KDE fails rotation rho=0.286), per-type CV fails at n=250/type, pooled non-stationary 95% attenuation, PMI on locally-hosted deterministic/independent-noise SPAs redundant at K=3 (0.0 bits) and independent-noise model bakes in null (EXP-PHYSICS-34764605162 audit V1). Tunnel flag true — further TV/KDE/binned tuning has near-zero marginal.

## 2. Scientific Question

Do interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity via an **orthogonal falsifiable program** beyond TV/KDE/binned density divergence — specifically **effect factorization with session/state-correlated non-determinism** where `DOM_before` correlates with a latent environment state `L` that determines the stochastic branch `P(S_next | S_current, A, L)`, such that `I(S_next ; DOM_before | URL_before, H_K=3, Action) >0` on production SPAs?

Equivalently: does the Web environment factorize into a latent regime `L` (session, auth tier, cart/user-dependent content, external data) that is **revealed in DOM_before** (title, visible text, a11y tree) and predicts `S_next` beyond what action-history `H_K=3` and `URL_before` already predict?

Alternatives that this program **does not** test (reserved for next orthogonal pivot if this falsifies): dynamical barrier/committor identifiability from branched evidence (≥10 revisits to same (URL,DOM) with divergent futures, committor variance), and characteristic timescale separation (autocorrelation, dwell-time spectra). This experiment tests factorization; a negative result pivots to those.

## 3. Motivation & Why This Is the Smallest High-Information Test

### 3.1 Tunnel diagnosis

- Frontier TV/KDE/binned PMI sequence: kNN TV fails scaling (rho=-0.12), KDE fails rotation (rho=0.286), PCA 2D/3D falsified, pooled non-stationary loses 95% magnitude, per-type bias-correction at 250/type fails CV for both estimators — complementary blind spots, no single density estimator works uniformly. No real Web data involved (all synthetic 2D [0,1]^2 or 10D mixture).
- Physics PMI sequence: deterministic SPAs → PMI 0.0 bits at K=3 (memory suffices); independent-noise SPAs → PMI 0.004–0.025 bits p=1.0 (V1: independent per-step draw bakes in null, audit correctly bounds falsification to that noise model). Open per audit: **correlated non-determinism where DOM_before and latent state are correlated** — never tested. Production SPA attempts failed on degenerate testbeds (TodoMVC constant title, unique_titles=1; server-rendered MPAs H=0, singleton SA rate 92-98% leakage, NL 2–8 vs required 50).
- Product consequence: if factorization exists, it yields a mechanical prior (DOM_before freshness/latent-state detector) that reduces exploration beyond retrieval; if it does not, physics should abandon DOMBefore latent-state detectors and Graph/Product should not pay that cost.

### 3.2 Why factorization is orthogonal

TV/KDE/binned divergence tests pooled `P(S'|S,A)` vs `P(S'|S)` aggregated over sites. Factorization tests **within-strata** `I(S_next ; DOM_before | URL, H_K, Action)` where strata already condition on history. It requires `H(S_next|URL,H_K=3)>0.2 bits` (branching) and tests whether DOM_before resolves the branch (latent state), not whether transitions differ from shuffle globally. Estimator is history-conditioned CMI with trajectory-grouped permutation, not pooled TV — different identifiability argument (requires branched evidence, not density fit).

### 3.3 Why production SPAs with title variation

TodoMVC hash-SPAs have 1 unique title (entropy 0) and after leakage-free filtering have no DOM-before variation correlated with branch; server-rendered MPAs have URL-level leakage 78–92% and H=0 at K=3 (deterministic link graph). Both are **incapable** of expressing the effect by construction. Testing factorization on them is a tautological negative (like testing PMI at K=3 on 5-state linear FSM where H=0). Director mandate correctly requires Intel-supplied production SPAs (BrowserGym/AgentLab 1280x720 capture) with title variation (≥2 titles) and verified non-leakage density (NL≥50, leakage<40%, H>0.2). This is the minimal substrate where the hypothesis is expressible.

## 4. Hypotheses

### H_primary (correlated factorization)

On Intel production SPAs satisfying Gate 0, bias-corrected history-conditioned CMI `I(S_next ; DOM_before | URL_before, H_K=3, Action_leakageFree) ≥0.10 bits` with Bonferroni-corrected grouped permutation p<0.005 on ≥2/3 qualifying SPAs for at least one DOM representation (R1 visible_text_hash or R2 a11y_tree_hash). Mechanism: `DOM_before` proxies latent regime `L` that is not resolved by `(URL, H_K=3)` alone.

### H_positive_control

Synthetic correlated SPA (branching FSM, L persists 3 steps, DOM_before = hash(L) + step, H=1.0 bit) shows BC PMI ≥0.5 bits, p<0.001, Cohen d>2.0, and accuracy gain Δ = acc(history+DOM) − acc(history)>0.10 with p<0.01. Pipeline blind if this fails.

### H_null (independent-noise)

Independent-noise synthetic SPA (same FSM, DOM variant i.i.d. per step independent of L) shows BC PMI ≤0.05 bits, p>0.10, replicating parent EXP-PHYSICS-34764605162 (0.004–0.025 bits, p=1.0). Demonstrates factorization is distinct from independent noise.

### H_shuffled_null

Within-strata shuffled DOM_before on each production SPA: |mean_null|<3*std_null and p>0.10. Valid null centering (not Gaussian jitter).

### H_accuracy_factorization

On qualifying SPAs where H_primary holds, history+DOM Markov predictor exceeds history-only Markov by Δ accuracy >0.03 (grouped permutation p<0.05). Demonstrates factorization has predictive bite beyond bits.

### H_leakage_diagnostic

`PMI_leaky` (action_with_href) − `PMI_leakageFree` >0 quantifies target leakage inflation; valid inference uses only leakageFree (leakageFree should be < leaky but still >0 if factorization holds).

## 5. Data Generation & Reuse

### 5.1 Gate 0 — Substrate qualification (must pass before primary test)

- **Source**: Intel lane must deliver manifest `intel_spa_manifest.json` with provenance (dataset revision hash, capture date, BrowserGym/AgentLab version, 1280x720 viewport). Each entry records `site_id, raw_transitions_path, n_raw, n_NL, leakage_rate, unique_titles, title_entropy, H_Snext_given_URL_HK3, singleton_SA_rate`.
- **Qualification per SPA** (computed after leakage-free filtering defined in §6):
  - `unique_titles ≥2` (title entropy >0 bits)
  - `H(S_next | URL_before, H_K=3) >0.2 bits` (plug-in entropy on NL transitions with ≥5 per stratum; if <5 per stratum for all strata → H undefined → SPA disqualified)
  - `leakage_rate_validOnly <40%` (where leakage = normalized target_href == normalized state_after_url; validOnly = among transitions where action has href)
  - `NL ≥50` (non-leakage transitions after filtering)
  - `NL unique (URL, H_K, Action) strata ≥10` and singleton rate <50%
- **Decision**: If 0 SPAs qualify → record MEASUREMENT_INVALID (substrate_unavailable), publish Gate 0 table, do not test H_primary; handoff requests Intel to supply title-varying branching SPAs (e.g., shopping/account/personalized content sites, not degenerate TodoMVC). If ≥1 SPA qualifies, proceed with qualifying set (max 3 for cost; if >3, take top-3 by H×NL).
- **Reuse**: Prefer reuse of existing Intel BrowserGym trajectories (if manifest overlaps prior EXP-INTEL-35697055679 artifacts, reuse with hash verification). New collection via Playwright if needed: 50 trajectories/SPA, 10 steps/trajectory, jitter 50–150 ms uniform, auth/session controls via runtime Flask JWT middleware for synthetic controls only.

### 5.2 Synthetic controls (local, deterministic seeds)

- **Positive control SPA** (correlated): 3-state branching FSM, state = (step_mod_3, L) where L∈{A,B} persists 3 steps with P(L flips)=0.3, URL = hash(step_mod_3), DOM_before = SHA256(L || step_mod_3), S_next = (step+1 mod 3, L_next) branched by L. Leakage 0%, H=1.0 bit, NL=200, seed 42.
- **Negative control SPA** (independent-noise): same FSM, L independent of DOM; DOM variant = SHA256(random_draw per step, seed 42, independent of L). Expected PMI~0.
- Both use same pipeline (hashing, strata, permutation) as production.

### 5.3 Sample size & power

- Per qualifying production SPA: target 150 NL (3×50 gate) gives ~10–15 strata ×10–15 per stratum — sufficient for 0.10 bits detection (parent needed 0.05). Minimum 50 is gate, 150 is target; power reported via bootstrap CI width.
- Per synthetic control: 200 NL fixed.

## 6. State, Action, History, DOM Representation (operational definitions)

### 6.1 State `S_next`

Primary: `S_next_primary = SHA256( normalize(URL_after) || '|' || normalize(title_after) )` where `normalize(URL)` = lowercase, strip session tokens/query `?session=`/`?token=`, preserve SPA hash fragment `#/` (do not strip), strip trailing slash; `normalize(title)` = trimmed, lowercased, truncated 200 chars. Exploratory variants: `S_URLonly` and `S_URL_DOMhash` reported but not primary.

### 6.2 Action `A_leakageFree`

`A = (primitive, target_sig)` where `primitive ∈ {click, fill, navigate, select, submit, hover}` and `target_sig = role + name + testId + aria-label` (never href/URL). Link `target_href` equality never enters A. Diagnostic `A_leaky = A + href` computed only for B-SITE-LEAKAGE gap.

### 6.3 History `H_K=3`

`H_K = (A_{t-2}, A_{t-1}, A_t, S_{t-2}, S_{t-1}, S_t)` truncated to last 3 steps; strata key = `(URL_before_normalized, H_K_actions)` where `URL_before_normalized` is same normalization as above but URL_only (without title) to avoid state leakage into condition. Rare strata <5 excluded from PMI point estimate but counted.

### 6.4 DOM_before representations

Tested independently (not ensembled):
- **R1 visible_text_hash**: SHA256( visibleText[:5000] ), visibleText from BrowserGym DOM snapshot (innerText, 0–5000 chars).
- **R2 a11y_tree_hash**: SHA256( serialized AX tree (role/name/value) up to 5k chars).
- **R3 title_before**: exact string equality on `title_before` (discretized by identity).
- **R4 combined_hash**: SHA256(R1 || R2).
Numeric structural features (element_count etc.) exploratory only — previously degenerate.

All raw observables preserved (dom_bytes, a11y_bytes, title string) with documented truncation.

## 7. Measures

### 7.1 Primary: history-conditioned bias-corrected CMI

For each (SPA, representation R):

```
I(S_next ; R | C)  where C = (URL_before, H_K=3, Action)
BC_PMI = PMI_observed(CMI) - mean(PMI_permuted)
PMI_observed = Σ_{c} (n_c/N) * Σ_{s,r} p(s,r|c) log2[ p(s,r|c) / (p(s|c)p(r|c)) ]
```

Plug-in with Laplace alpha=1.0, Miller-Madow bias correction on each stratum entropy, then weighted by stratum size. Sensitivity: report nosmooth (alpha=0) and alpha=1.0.

### 7.2 Accuracy factorization delta

Split trajectories 70/30 by `trajectory_id` (grouped):
- `acc_history = accuracy( majority S_next | C )` on test
- `acc_history_DOM = accuracy( majority S_next | C,R )` on test
- `Δ = acc_history_DOM - acc_history`

### 7.3 Auxiliary

- `H(S_next|C)` entropy (ceiling), strata count, singleton rate, NL, leakage_rate, unique_titles, title_entropy, null_std, Cohen d = (BC_PMI)/std_null, 95% grouped permutation CI, Jaccard DOM similarity baseline accuracy.

## 8. Null Models & Baselines (strong)

1. **B-HISTORY-MARKOV**: `P(S_next|C)` majority vote — the beyond-memory null.
2. **B-ACTION-FREQ-SHUFFLE**: within-strata shuffle of R and of S_next.
3. **B-DOM-SIMILARITY**: kNN over DOM TF-IDF cosine (k=5) predicting S_next via similarity, without history conditioning — ordinary similarity null.
4. **B-TRAJECTORY-MEMORY**: exact `(C)->S_next` memorization from train (replay baseline).
5. **B-SITE-LEAKAGE-DIAGNOSTIC**: PMI_leaky vs PMI_leakageFree gap.
6. **B-INDEPENDENT-NOISE-SYNTHETIC**: independent-noise SPA expected 0 bits.
7. **B-RANDOM-DOM**: SHA256(random_counter) independent of S/A/C.

All baselines use same strata, same permutation grouping, same seeds.

## 9. Statistical Tests & Uncertainty

- **Permutation**: 1000 within-strata cross-trajectory shuffles of R labels within each C stratum, preserving stratum sizes, grouped by trajectory_id (shuffle R across trajectories but within same C stratum), seed 42, deterministic. Null distribution = BC_PMI_permuted.
- **p-value**: `p = (1 + #{perm ≥ observed})/1001`, one-sided (PMI>0). Bonferroni over `n_qualifying_SPAs × n_representations` (max 3×4=12 → alpha 0.05/12=0.00417, rounded to 0.005). Report raw and corrected.
- **Effect size**: Cohen d = BC_PMI / std_null; BC_PMI 95% CI via permutation percentiles.
- **Accuracy p**: grouped permutation of R labels (1000) for Δ>0, one-sided.
- **Resampling unit**: trajectory_id — never treat correlated transitions within trajectory as independent. No Gaussian jitter bootstrap.
- **Seed determinism**: Python `PYTHONHASHSEED=0`, `numpy.random.seed(42)`, `sklearn` random_state 42, `hash()` not used.

## 10. Controls

### Positive control

Synthetic correlated SPA: must achieve BC PMI ≥0.5 bits, p<0.001, d>2.0, Δ≥0.10. Failure → MEASUREMENT_INVALID (pipeline cannot detect factorization when it exists).

### Null controls

1. **Shuffled-DOM within C strata** on each production SPA: |mean_null|<3*std_null and p>0.10. Valid centering requires std_null>0.01.
2. **Independent-noise synthetic SPA**: BC PMI ≤0.05 bits, p>0.10. Replicates parent.

If null std==0 (singleton strata >50% making permutation degenerate) → MEASUREMENT_INVALID, not falsification.

### Data-quality controls

- ≥50 NL per SPA, H>0.2, leakage<40%, titles≥2.
- Singleton (C,A) rate <50% (otherwise estimator degenerate).
- Raw observable preservation check: dom_bytes≥2000 and a11y non-empty on ≥90% transitions.

## 11. Validity Threats & Mitigations

| Threat | Mitigation |
|---|---|
| **Target leakage** (href==URL) | Leakage-free A excludes href; report leaky diagnostic gap; filter leakage transitions from primary. |
| **Split leakage** | All discretization/vocab fit on TRAIN trajectories only; stratified 70/30 by trajectory_id; site identity never a feature. |
| **Sampling/policy confounding** | Crawler policy documented (depth, jitter, action distribution); separate policy regularity from environment dynamics; report action distribution per SPA. |
| **Uncertainty mis-specification** | Grouped permutation by trajectory_id; no Gaussian jitter; report null_std and singleton rate. |
| **Representation loss** | Preserve raw DOM/a11y/title; test 4 legitimate representations; require survival on at least one. |
| **Synthetic-to-real gap** | Production SPAs only for primary; synthetic only for controls; explicitly bound claim to qualifying production SPA regime (shopping/account/personalized). |
| **H=0 determinism ceiling** | Gate 0 requires H>0.2 bits; deterministic SPAs excluded from primary (would force PMI=0). |
| **Title degeneracy** | Gate 0 requires ≥2 titles; TodoMVC-like hash-SPAs with 1 title auto-disqualified → MEASUREMENT_INVALID, not negative. |
| **Hash collision/tautology** | R is DOM_before, S_next is URL+title after action — distinct time steps; report MI(R; A) to test action→DOM tautology; require MI(R;S_next|C) not explained by MI(R;A). |

## 12. Decision Rules (frozen)

### Gate 0 — Substrate

- If 0 SPAs qualify → **MEASUREMENT_INVALID** (substrate_unavailable). No claim update for C-WEB-DYNAMICS. Report Gate 0 table, unresolved substrate. Handoff requests Intel BrowserGym title-varying branching SPAs.

### Pipeline gates

- If positive control fails (BC PMI<0.5 or p≥0.001) → **MEASUREMENT_INVALID** (pipeline blind).
- If null controls degenerate (std_null==0 or |mean_null|≥3*std) → **MEASUREMENT_INVALID**.

### Primary decision (only if gates pass)

Let `Q = #qualifying SPAs`, `sig(SPA)=1` if any representation achieves **BC PMI≥0.10 bits AND Bonferroni p<0.005 AND Δ>0.03 with p<0.05**.

- If `Q≥3` and `Σ sig ≥2` → **SURVIVES_CURRENT_TEST** — correlated factorization demonstrates beyond-memory dynamics on production SPAs in this regime.
- If `Q∈{1,2}` and `Σ sig ≥1` and all sig SPAs meet both PMI and Δ thresholds → **SURVIVES_CURRENT_TEST** (bounded to Q SPAs, not general Web).
- If `Σ sig ==0` (no SPA meets PMI and Δ) → **FALSIFIED-IN-SETTING** — no DOM-before latent-state factorization beyond memory on these SPAs/representations. Bounded to tested SPA types and R1–R4; does not close barrier/timescale programs.
- If `0< Σ sig < threshold` → **MIXED/INCONCLUSIVE** — partial evidence, report per-SPA table, do not update claim beyond hypothesis; recommend larger N or alternative representations.

### Sensitivity & exploratory (not gating)

- Report leakage diagnostic Δ_leak = PMI_leaky − PMI_leakageFree.
- Report B-DOM-SIMILARITY gap vs CMI.
- Report branched revisits rate (for next barrier/committor feasibility) and dwell-time distribution (for timescale feasibility) — informs orthogonal pivot without claiming.

## 13. Consequences

### If SURVIVES

- C-WEB-DYNAMICS ceiling expands to: history-conditioned DOM_before factorization on title-varying production SPAs with H>0.2 (shopping/account/personalized). First real-SPA beyond-memory dynamics beyond synthetic 2D.
- Product: distill DOM_before latent-state detectors as applicability guards for parameterized mechanisms and freshness sentinels (DOM_before change signals regime shift). Prioritize Intel BrowserGym collection on title-varying branching sites for Graph/Product. Next: scope which DOM signals generalize and measure delta-repair cost when latent state drifts.
- Physics next: test factorization invariance across site types and cross-site holdout.

### If FALSIFIED

- C-WEB-DYNAMICS remains HYPOTHESIS but factorization program is closed for R1–R4 on tested SPA regime; independent-noise and correlated models both predict PMI~0 on these production SPAs (or insufficient branching).
- Product: do not invest in DOM_before latent-state detectors as mechanical prior; Graph/Product rely on trajectory memory/retrieval without physics prior.
- Physics next (per director_mandate): pivot to barrier/committor (estimate committor from ≥10 revisits to same (URL,DOM) state, test bimodality/barrier) or timescale separation (autocorrelation, dwell-time heavy tail) on same substrate — orthogonal programs not based on pooled density divergence.

### If MEASUREMENT_INVALID

- No claim update. Report exact gate failed, handoff with per-SPA table, request Intel manifest fix or runtime substrate fix. Retry is not a scientific negative.

## 14. Analysis Plan (deterministic order)

1. Verify manifest hashes, load raw transitions, compute Gate 0 table (leakage_rate, unique_titles, H, NL, singleton rate) — halt if Q==0.
2. Build synthetic correlated and independent-noise control datasets (seed 42).
3. For each (SPA/control, representation R1–R4): build strata C=(URL,H_K=3,A), compute PMI_observed (Laplace + Miller-Madow), run 1000 grouped within-strata permutations → BC PMI, std_null, p, d, CI.
4. Compute accuracy split 70/30 grouped by trajectory: acc_history, acc_history_DOM, Δ, permutation p for Δ.
5. Compute baselines B-SIMILARITY, B-TRAJECTORY-MEMORY, B-RANDOM-DOM, B-LEAKAGE diagnostic.
6. Apply frozen decision rule, publish per-SPA × representation table, Gate 0 table, control tables, and handoff with barrier/timescale feasibility metrics.
7. Commit all artifacts with sha256 in provenance.json; no outcome peeking before freeze hash.

## 15. Freeze Statement

This preregistration is frozen **before** any outcome data on qualifying production SPAs is inspected. Positive/negative controls are defined by synthetic construction, not by peeking at production data. Any deviation is labeled **EXPLORATORY** and cannot support confirmatory SURVIVES/FALSIFIED claims. A new confirmatory claim requires a new preregistration. Estimated cost <4h wall-clock, no LLM calls.

## 16. References to Prior Evidence

- EXP-PHYSICS-34764605162 (FALSIFIED-IN-SETTING, audit V1): independent-noise bakes in null, correlated state open.
- EXP-PHYSICS-35209110569/35262258744: TodoMVC title degeneracy (1 title) and H=0 ceiling.
- EXP-PHYSICS-34038570933/34071626363/34149195420: leakage 92-98% via target_href, PMI drops 1.073→0.0 when filtered.
- Frontier TV/KDE: complementary blind spots, 95% attenuation non-stationary, per-type CV fails at 250/type — justifies orthogonal pivot.

