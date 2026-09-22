# EXP-PHYSICS-35756224948 Preregistration — Physics Orthogonal Factorization (REOPEN with Corrected Pipeline)

**Status: DESIGN — FROZEN BEFORE OUTCOME (2026-09-22). No outcome-bearing measurements on qualifying production SPAs have been inspected.**

## 1. Experiment Identity

- **Experiment ID**: EXP-PHYSICS-35756224948
- **Lane**: physics
- **Claim**: C-WEB-DYNAMICS — Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity (status HYPOTHESIS per codex/claim_state.json, 59 synthetic-dominated events)
- **Directive**: Global Research Director REOPEN on C-WEB-DYNAMICS (request.json director_mandate cycle 35755646729, allocation REOPEN cognitive_reset true). Binding strategic question verbatim in request.json director_mandate.question. Parent handoff disposition USE per request, comparative reasoning: continuing synthetic TV/KDE/kNN/CV tuning is tunneling with near-zero marginal; REOPEN on Gate0 production SPAs directly tests predictive structure beyond memory; if Gate0 not met return MEASUREMENT_INVALID not false negative.
- **Parent handoff**: research/experiments/EXP-PHYSICS-35749353065/handoff.json (sha256 516ef1ca6100f77abeeb5e0ff16cdf9ce92a6b9524e56bd2911f1036a38dc6cc) — established/rejected/unknown/do_not_assume distinctions preserved below (§2). Parent was MEASUREMENT_INVALID substrate_unavailable, not falsification.
- **Dependencies (binding)**: (a) intel: production SPA manifest intel_spa_manifest.json satisfying Gate0 (>=2 titles, H>0.2, leakage<40%, NL>=50, strata>=10, singleton<50%) from BrowserGym/AgentLab 1280x720 with provenance (dataset revision hash, capture date, version, viewport); (b) runtime: BrowserGym/AgentLab 1280x720 AX tree provenance (Accessibility.getFullAXTree) and leakage-free action definition; (c) corrected trajectory-grouped permutation and restored positive-control FSM must be re-frozen before retry.
- **Pre-2.0 / pre-2.0+ codex baseline**: WP-002B true next-state rule minus shuffle +0.0532 (no holdout), historical WP-003 MEASUREMENT_INVALID (prev_action_label leakage, Gaussian jitter CI, hash(site) seed), synthetic TV/KDE/binned tunnel with complementary blind spots and 95% pooled attenuation, independent-noise falsification at 0.004–0.025 bits (EXP-PHYSICS-34764605162) bounded to that noise model, TodoMVC title degeneracy (unique_titles=1) and MPA leakage 78–98% disqualify those testbeds.

## 2. Inherited Scientific State (from parent handoff — continuity evidence only)

Per AGENTS.md and EXPERIMENT_PACKET.md, parent handoff is continuity evidence and MUST NOT silently override the REOPEN Director decision. Its `next_question` is identical to the Director's binding question, so no conflict.

### Established (justified at stated ceiling)
- Gate0 correctly classified as MEASUREMENT_INVALID substrate_unavailable in parent (0/5 candidates, no manifest, no research/intel/, no BrowserGym artifacts) — per audit FINDING-1.
- C-WEB-DYNAMICS was NOT tested on production SPAs and remains HYPOTHESIS; NOT falsified by parent.
- Synthetic pipeline qualitative discrimination reproduced byte-identically (raw_cmi_results.json): positive correlated BC 0.8539 item-level (audit grouped 0.8392) with delta accuracy 0.4667; independent-noise R2 non-degenerate BC 0.0036 p=0.458 matches parent ~0-bit null — but 'exactly per frozen design' not justified due to deviations below.
- Leakage diagnostic 0% in synthetics is construction artifact; absolute PMI 0.977/1.0 are plug-in bias artifacts.

### Rejected (bounded)
- Independent per-step DOM observation noise (i.i.d. per-step variant independent of latent L) yields ~0 bits on hash-based DOM — bounded to that noise model and 5-state linear Express SPAs.
- NOT rejected: correlated non-determinism where DOM_before proxies persistent latent regime; barrier/committor; timescale separation.

### Unknown (open for this experiment)
- Whether Intel can supply manifest satisfying Gate0 with 1280x720 provenance.
- What BC PMI, Bonferroni p, Cohen d, CI, delta accuracy would be observed on qualifying production SPAs for R1/R2/R3/R4 with leakage-free action and trajectory-grouped CMI.
- Whether frozen trajectory-grouped permutation null is well-centered on hash-DOM production strata (audit grouped perm_mean up to 0.4614 bits).
- Whether frozen positive-control construction P=0.3 DOM=SHA256(L||step_mod) achieves BC>=0.5 bits (executor substituted P=0.0 to guarantee threshold).
- Whether B-DOM-SIMILARITY diverges from history-conditioned CMI on production data (not executed in parent).
- Feasibility of barrier/committor (>=10 revisits) or timescale separation on same substrate.

### Do Not Assume
- Do not assume C-WEB-DYNAMICS falsified or supported — no production factorization measurement exists.
- Do not assume pipeline validated exactly per frozen design — deviations: item-level shuffle never using trajectory_id, outcome-modified positive control (P=0.0, DOM=SHA256(L) not SHA256(L||step_mod)), unreachable Bonferroni p<0.001 at N=1000, result.json/report.md contradict raw artifact (0.5/0.9667 vs 0.5333/1.0, CI 0.094/0.153 vs -0.0229/0.0347), null R1/R4/corr degenerate, representation diversity nominal (all encode same L bit), synthetic absolute PMI biased, pooled TV/KDE not only method, synthetic-to-real gap.

This design corrects all six required_fixes from parent audit.

## 3. Scientific Question (binding)

On Intel-supplied production SPAs satisfying Gate 0 (>=2 titles, H(S_next|URL,H_K=3)>0.2 bits, leakage<40%, NL>=50, strata>=10, singleton<50%) with BrowserGym/AgentLab 1280x720 provenance, does history-conditioned CMI I(S_next;DOM_before|URL,H_K=3,Action_leakageFree) with frozen trajectory-grouped permutation (resampling unit trajectory_id, 1000 perms) and restored positive control (P(L flips)=0.3, DOM=SHA256(L||step_mod)) achieve BC PMI>=0.10 bits, Bonferroni p<0.005 and Delta accuracy>0.03 on >=1/2 SPAs (or >=2/3 if Q=3) for R1 or R2, and if falsified does barrier/committor (>=10 revisits to same URL,DOM with divergent futures) or timescale separation reveal beyond-memory dynamics with B-DOM-SIMILARITY executed as frozen?

Equivalent factorization framing: does DOM_before correlate with latent environment state L that determines stochastic branch P(S_next | S_current, A, L), such that I(S_next ; DOM_before | URL, H_K=3, Action) >0 beyond memory/similarity?

Alternatives reserved for orthogonal pivot if this falsifies: barrier/committor identifiability and timescale separation — both tested exploratory on same substrate without density divergence.

## 4. Motivation & Why This Is the Smallest High-Information Test

### 4.1 Tunnel diagnosis (why not another synthetic sweep)
- Frontier: kNN TV fails scaling rho=-0.12, KDE fails rotation rho=0.286, PCA 2D/3D falsified, pooled non-stationary loses 95% magnitude, per-type CV fails at 250/type for both estimators, bias-corrected TV still fails scaling — no single density estimator uniform; all synthetic 2D/10D.
- Physics: deterministic SPAs PMI 0.0 at K=3 (memory suffices), independent-noise SPAs 0.004–0.025 bits (V1 bakes in null), TodoMVC title degeneracy 0 titles, MPAs H=0 at K=3 and 78–98% leakage with NL 2–8 vs required 50 — incapable testbeds tautologically force PMI=0. Open per audit: correlated non-determinism where DOM_before and latent state correlated — never tested on production.
- Product leak: if factorization exists, DOM_before freshness/latent detector reduces exploration beyond retrieval; if not, physics must abandon that detector.

### 4.2 Why factorization is orthogonal to prior tunnel
TV/KDE/binned tests pooled P(S'|S,A) vs P(S'|S) aggregated. Factorization tests within-strata I(S_next ; DOM_before | URL, H_K, Action) where strata already condition on history. Requires H>0.2 branching and tests whether DOM_before resolves the branch (latent state), not global density shift. Estimator is history-conditioned CMI with trajectory-grouped permutation, not pooled TV — different identifiability (requires branched revisits, not density fit). Director mandate explicitly distinguishes these and prioritizes factorization.

### 4.3 Why production SPAs with title variation and Gate0
TodoMVC hash-SPAs and server-rendered MPAs cannot express effect by construction (entropy 0, no DOM-before variation correlated with branch). Director mandate requires Intel production SPAs with title variation (>=2 titles) and verified non-leakage density (NL>=50, H>0.2, leakage<40%). This is minimal substrate where hypothesis is expressible; without it, test is measurement-invalid by design, not negative evidence.

## 5. Hypotheses (frozen, exhaustive)

### H_primary (correlated factorization)
On Intel production SPAs satisfying Gate0, bias-corrected history-conditioned CMI BC_PMI >=0.10 bits with Bonferroni-corrected grouped permutation p<0.005 (over Q*2 tests) and delta accuracy >0.03 (grouped p<0.05) on >=2/3 SPAs when Q=3 or >=1/2 when Q in {1,2} for R1 visible_text_hash or R2 a11y_tree_hash. Mechanism: DOM_before proxies latent regime L not resolved by (URL,H_K=3).

### H_positive_control
Synthetic correlated SPA (branching FSM, L persists 3 steps P=0.3, DOM=SHA256(L||step_mod), H=1.0, leakage 0%, NL=200) shows BC_PMI >=0.50 bits, raw p<0.005, Cohen d>2.0, delta >=0.10 with p<0.01. Pipeline blind if fails.

### H_null_independent
Independent-noise synthetic SPA (same FSM, DOM variant i.i.d. per step independent of L) shows BC_PMI <=0.05 bits, p>0.10, replicating parent non-degenerate R2 0.0036 bits p=0.458. Demonstrates factorization distinct from independent noise.

### H_null_shuffled
Within-strata shuffled DOM_before on each production SPA: |null_mean|<3*null_std and p>0.10 with null_std>0.01 (valid centering).

### H_delta
On qualifying SPAs where H_primary holds, history+DOM Markov exceeds history-only Markov by delta>0.03 with grouped p<0.05 — predictive bite beyond bits.

### H_leakage_diagnostic
PMI_leaky (action_with_href) - PMI_leakageFree >0 quantifies inflation; valid inference uses leakageFree alone.

## 6. Data Generation & Reuse

### 6.1 Gate0 — Substrate qualification (must pass before primary test)
- **Source**: Intel lane manifest intel_spa_manifest.json with provenance (dataset revision hash, capture date, BrowserGym/AgentLab version, 1280x720 viewport). Each entry: site_id, raw_transitions_path, n_raw, n_NL, leakage_validOnly, unique_titles, title_entropy, H_Snext_given_URL_HK3, strata_count, singleton_SA_rate, viewport, provenance hash.
- **Qualification per SPA** (computed after leakage-free filtering §7):
  - unique_titles >=2 (title_entropy>0)
  - H(S_next|URL,H_K=3)>0.2 bits (plug-in entropy on NL transitions with >=5 per stratum; else H undefined => disqualified)
  - leakage_validOnly <40% among href-bearing actions
  - NL >=50
  - strata_count >=10 and singleton_SA_rate <50%
- **Decision**: 0 qualify => MEASUREMENT_INVALID substrate_unavailable, publish gate0_table.json, do not test H_primary; handoff requests Intel branching title-varying SPAs (shopping/account/personalized, not degenerate TodoMVC). If >=1 qualify, proceed with qualifying set (max 3 for cost; if >3 take top-3 by H*NL).
- **Reuse**: verify manifest hash, load raw transitions, do not self-collect production sites as substitute without re-freeze. Existing Intel trajectories reused with hash verification.

### 6.2 Synthetic controls (local, deterministic seeds PYTHONHASHSEED=0 numpy 42)
- **Positive correlated**: 3-state branching FSM, state=(step_mod_3, L) L in {A,B} persists 3 steps P(flip)=0.30 exactly per frozen spec, URL=hash(step_mod_3), DOM_before=SHA256(L || step_mod_3), S_next branched by L, H=1.0 bit, leakage 0%, NL=200.
- **Negative independent-noise**: same FSM, L independent of DOM; DOM variant=SHA256(random_draw per step, seed 42, independent of L). Expected PMI~0.
- Both use identical pipeline (hashing, strata, grouped permutation) as production.

### 6.3 Sample size & power
- Per qualifying production SPA: gate 50 minimum, target 150 NL gives ~10–15 strata x10–15 per stratum for 0.10 bits detection. Power reported via bootstrap CI width and H ceiling.
- Per synthetic control: 200 NL fixed.

## 7. State, Action, History, DOM Operational Definitions

### 7.1 State S_next
Primary S_next_primary = SHA256(normalize(URL_after) || '|' || normalize(title_after)) where normalize(URL)=lowercase, strip query ?session=/?token=, preserve SPA hash fragment #/, strip trailing slash; normalize(title)=trimmed lowercased truncated 200 chars. Exploratory: S_URLonly, S_URL_DOMhash. Title variation is Gate0 discriminator; S_next distinct timestep from DOM_before.

### 7.2 Action A_leakageFree
A=(primitive, target_sig) primitive in {click, fill, navigate, select, submit, hover}, target_sig=role+name+testId+aria-label (never href/URL/src). Link target_href never enters A. Diagnostic A_leaky=A+href for leakage gap only. Report link share vs non-link.

### 7.3 History H_K=3
H_K=(A_{t-2},A_{t-1},A_t, S_{t-2},S_{t-1},S_t) last 3 steps; strata key C=(URL_before_normalized, H_K_actions) where URL_before_normalized is URL_only without title to avoid state leakage into condition. Rare strata <5 excluded from PMI point estimate but counted in singleton_rate.

### 7.4 DOM_before representations (tested independently)
- R1 visible_text_hash: SHA256(visibleText[0:5000] innerText from BrowserGym DOM snapshot)
- R2 a11y_tree_hash: SHA256(serialized AX tree role/name/value up to 5k chars via Accessibility.getFullAXTree)
- R3 title_before: exact string equality on title_before (exploratory)
- R4 combined_hash: SHA256(R1 || R2) (exploratory)
Numeric structural features exploratory only. Raw observables preserved (dom_bytes>=2000, a11y non-empty on >=90% transitions) with truncation documented.

## 8. Measures

### 8.1 Primary: history-conditioned bias-corrected CMI
For each (SPA, R in {R1,R2}):
```
I(S_next ; R | C)  C=(URL_before, H_K=3, Action)
BC_PMI = observed PMI(CMI) - mean(permuted PMI)
observed = sum_c (n_c/N) * sum_{s,r} p(s,r|c) log2[p(s,r|c)/(p(s|c)p(r|c))]
```
Plug-in Laplace alpha=1.0 plus Miller-Madow bias correction per stratum, weighted by stratum size. Sensitivity: nosmooth alpha=0 reported.

### 8.2 Accuracy factorization delta
Split trajectories 70/30 by trajectory_id (grouped, stratified):
- acc_history = accuracy(majority S_next | C) on test
- acc_history_DOM = accuracy(majority S_next | C,R) on test
- delta = acc_history_DOM - acc_history, grouped permutation p for delta

### 8.3 Auxiliary (per SPA per R)
H(S_next|C) entropy ceiling, strata_count, singleton_rate, NL, leakage_validOnly, unique_titles, title_entropy, link_share, null_mean, null_std, Cohen d=BC/null_std, 95% grouped permutation CI via percentiles, B-DOM-SIMILARITY accuracy gap, action distribution.

## 9. Null Models & Baselines (strong, all executed as frozen)

1. **B-HISTORY-MARKOV**: P(S_next|C) majority vote — beyond-memory null, primary comparator.
2. **B-ACTION-FREQ-SHUFFLE**: within-strata shuffle of R labels AND separate within-strata shuffle of S_next labels; frequency-only P(S_next) accuracy =1/|S_next| reported; same strata/grouped seeds.
3. **B-DOM-SIMILARITY** (mandatory per director): kNN TF-IDF cosine / Jaccard over DOM visible_text and a11y text, k=5 predicting S_next via similarity without history conditioning; MUST be executed and gap vs history-conditioned CMI reported; history-conditioned CMI must beat similarity to claim beyond-memory.
4. **B-TRAJECTORY-MEMORY**: exact (C)->S_next memorization from train; computed separately, not asserted.
5. **B-SITE-LEAKAGE-DIAGNOSTIC**: PMI_leaky vs PMI_leakageFree gap (calibrated BC); same estimator, not uncorrected plug-in.
6. **B-INDEPENDENT-NOISE-SYNTHETIC**: independent-noise SPA expected ~0 bits on same grouped pipeline.
7. **B-RANDOM-DOM**: SHA256(random_counter) independent of state/action/stratum.

All baselines share identical strata, grouped permutation grouping, and seeds.

## 10. Statistical Tests & Uncertainty (frozen, corrected per audit)

- **Permutation**: 1000 within-strata cross-trajectory shuffles of R labels within each C stratum, preserving stratum sizes and within-trajectory DOM sequences, grouped by trajectory_id (shuffle R across trajectories but within same C stratum), seed 42 deterministic. Null = BC_PMI_permuted distribution. Resampling unit = trajectory_id; correlated transitions within trajectory not independent; no Gaussian jitter.
- **p-value**: p_raw = (1 + #{perm >= observed})/1001 one-sided (PMI>0). Bonferroni primary: p_bonf = min(1, p_raw * Q * 2) over Q SPAs *2 primary representations; alpha 0.05/6=0.0083 rounded to frozen 0.005 for conservatism. Report raw and Bonferroni. Positive control: raw p<0.005 single test (reachable at N=1000 floor 0.001; fixes FINDING-4 unreachable p<0.001).
- **Effect size**: Cohen d = BC_PMI / null_std (null_std>0.01 required); BC 95% CI via grouped permutation percentiles (2.5th/97.5th), NOT Gaussian mean±2*std.
- **Accuracy p_delta**: grouped permutation of R labels within strata (1000) for delta>0 one-sided.
- **Seed determinism**: PYTHONHASHSEED=0, numpy seed 42, sklearn random_state 42; hash() not used.

## 11. Controls (frozen, addressing all parent findings)

### Positive control
Synthetic correlated SPA must achieve BC>=0.5 bits, raw p<0.005, d>2.0, delta>=0.10 p<0.01. Construction exactly P=0.30 and DOM=SHA256(L||step_mod_3); any change is protocol violation labeled EXPLORATORY. Failure => MEASUREMENT_INVALID.

### Null controls
1. Shuffled-DOM within C strata on each production SPA: |null_mean|<3*null_std, p>0.10, null_std>0.01. Degenerate (null_std==0 or singleton>50%) => MEASUREMENT_INVALID not PASS.
2. Independent-noise synthetic: BC<=0.05 bits, p>0.10, null_std>0.01. R3 constant DOM triggers MEASUREMENT_INVALID for that representation.

### Data-quality controls
NL>=50 per SPA, strata>=10, singleton<50%, H>0.2, leakage<40%, titles>=2, dom_bytes>=2000 and a11y non-empty >=90%.

## 12. Validity Threats & Mitigations

| Threat | Mitigation |
|---|---|
| Target leakage href==URL | Leakage-free A excludes href; filter leakage transitions; report diagnostic gap; same estimator for both. |
| Split leakage | Discretization/TF-IDF fit on TRAIN only; 70/30 by trajectory_id; site identity never feature. |
| Sampling/policy confounding | Document crawler policy, action distribution per SPA, separate policy regularity; determinism via seeds. |
| Uncertainty mis-specification | Grouped permutation by trajectory_id (fixes FINDING-2); no Gaussian jitter; report null_std and singleton_rate; degeneracy=>MEASUREMENT_INVALID. |
| Representation loss | Preserve raw DOM/a11y/title; test R1,R2 primary plus R3,R4 exploratory; require R1 or R2; document hash truncation. |
| Synthetic-to-real gap | Production SPAs only for primary; synthetic only controls; bound claim to qualifying production regime. |
| H=0 determinism ceiling | Gate0 H>0.2 excludes deterministic SPAs (would force PMI=0). |
| Title degeneracy | Gate0 >=2 titles; TodoMVC auto-disqualified => MEASUREMENT_INVALID. |
| Hash collision/tautology | R is DOM_before distinct timestep from S_next; report MI(R;A) to test action->DOM tautology; require MI(R;S_next|C) not explained by MI(R;A); probe same estimator. |
| Unreachable Bonferroni | N=1000 raw p<0.005 reachable (fixes FINDING-4); report both raw and Bonferroni. |
| Result/report drift | All metrics recomputed from raw_cmi_results.json; freeze hashes verified before execution (fixes FINDING-6). |
| Missing baselines | B-DOM-SIMILARITY/B-ACTION-FREQ-SHUFFLE/B-TRAJECTORY-MEMORY all executed as frozen with same grouping (fixes audit baseline findings). |

## 13. Decision Rules (frozen, pre-outcome)

### Gate0 — Substrate
- 0 qualifying SPAs => MEASUREMENT_INVALID substrate_unavailable. No C-WEB-DYNAMICS update. Publish gate0_table.json. Handoff requests Intel manifest. This is not falsification.

### Pipeline gates
- Positive control BC<0.5 or raw p>=0.005 or d<=2.0 or delta<0.10 => MEASUREMENT_INVALID pipeline_blind.
- Null controls degenerate (null_std==0 or |null_mean|>=3*null_std or singleton>50%) => MEASUREMENT_INVALID for that representation.

### Primary decision (only if gates pass)
Let Q=#qualifying, sig(SPA)=1 if EXISTS R in {R1,R2} with BC>=0.10 AND p_bonf<0.005 AND delta>0.03 p_delta<0.05 AND null_std>0.01.
- Q>=3 and sum sig >=2 => SURVIVES_CURRENT_TEST — correlated factorization beyond memory on production SPAs in this regime (bounded to tested types and R1/R2).
- Q in {1,2} and sum sig >=1 => SURVIVES_CURRENT_TEST (bounded to Q SPAs).
- sum sig ==0 => FALSIFIED-IN-SETTING — no DOM-before latent-state factorization beyond memory via R1/R2 hash representations on these SPAs (bounded; does not close barrier/timescale).
- 0< sum sig <threshold => MIXED/INCONCLUSIVE — partial, report per-SPA table, do not update claim beyond HYPOTHESIS.

### Exploratory contingency (only if primary FALSIFIED and pipeline gates passed)
- Evaluate barrier/committor: count revisits to same (URL,DOM) with divergent futures; if branched_revisit_count>=10 estimate committor variance; exploratory SURVIVES only if variance>0.10 with grouped p<0.05 and bimodal. Report branched_revisit_count, divergent_future_rate, committor variance regardless.
- Evaluate timescale separation: dwell-time distribution, autocorrelation; report histogram and separation metric regardless.
- B-DOM-SIMILARITY gap vs CMI reported in all cases. These do NOT alter primary FALSIFIED verdict; they inform orthogonal pivot.

### Sensitivity (not gating)
- Leakage diagnostic delta_leak, B-DOM-SIMILARITY gap, nosmooth alpha=0 sensitivity, branched revisit and dwell-time feasibility.

## 14. Consequences

### If SURVIVES
- C-WEB-DYNAMICS ceiling expands to: history-conditioned DOM_before factorization on title-varying production SPAs with H>0.2 (shopping/account/personalized) via R1 or R2. First real-SPA beyond-memory dynamics beyond synthetic 2D.
- Product: distill DOM_before latent-state detectors as applicability guards for parameterized mechanisms and freshness sentinels (DOM_before regime shift triggers re-validation). Prioritize Intel BrowserGym collection on branching sites for Graph/Product. Next: scope which DOM signals generalize, cross-site holdout, delta-repair cost when latent state drifts.
- Physics next: test invariance across site types and cross-site holdout.

### If FALSIFIED
- C-WEB-DYNAMICS remains HYPOTHESIS but hash-DOM factorization program closed for R1/R2 on tested regime; independent-noise and correlated-proxy via hash DOM both ~0 on these SPAs.
- Product: do not invest in DOM_before hash detectors; Graph/Product rely on trajectory memory/retrieval without physics prior.
- Physics next per director_mandate: pivot to barrier/committor (>=10 revisits, committor variance) or timescale separation (autocorrelation/dwell-time heavy tail) on same substrate — orthogonal, not density divergence.

### If MEASUREMENT_INVALID
- No claim update. Report exact gate failed, per-SPA table, unresolved substrate. Retry not a scientific negative. Preserve epistemic discipline (refuse false negative from degenerate TodoMVC/MPA testbeds).

## 15. Analysis Plan (deterministic order, no outcome peeking before freeze)

1. Verify manifest hashes, load raw transitions, compute Gate0 table (leakage_validOnly, unique_titles, title_entropy, H, NL, strata_count, singleton_rate) — halt if Q==0 with MEASUREMENT_INVALID.
2. Build synthetic correlated (P=0.30) and independent-noise control datasets (seed 42, exactly SHA256(L||step_mod)).
3. For each (SPA/control, R in {R1,R2,R3,R4}): build strata C=(URL,H_K=3,A_leakageFree), compute observed PMI (Laplace alpha=1.0 + Miller-Madow), run 1000 grouped within-strata cross-trajectory permutations => BC_PMI, null_mean/std, p_raw/p_bonf, d, CI percentiles; compute delta accuracy 70/30 grouped split, permute p_delta.
4. Compute B-HISTORY-MARKOV, B-DOM-SIMILARITY (TF-IDF cosine k=5), B-TRAJECTORY-MEMORY, B-ACTION-FREQ-SHUFFLE, B-SITE-LEAKAGE-DIAGNOSTIC, B-RANDOM-DOM on same strata/grouping.
5. For exploratory contingency, compute branched_revisit_count, divergent futures, dwell-time, autocorrelation on same substrate.
6. Apply frozen decision rule, publish per-SPA x representation table, Gate0 table, control tables, provenance with sha256; no metric built from report before freeze hash.

## 16. Freeze Statement

This preregistration is frozen before any outcome data on qualifying production SPAs is inspected. Synthetic controls are defined by construction (not by peeking at production data). Trajectory-grouped permutation, restored positive-control construction (P=0.30, DOM=SHA256(L||step_mod)), reachable Bonferroni thresholds, and mandatory B-DOM-SIMILARITY/B-ACTION-FREQ-SHUFFLE/B-TRAJECTORY-MEMORY execution correct all six parent audit required_fixes before any new outcome is observed. Any deviation after freeze is labeled EXPLORATORY and cannot support confirmatory SURVIVES/FALSIFIED. A new confirmatory claim requires a new preregistration. Estimated cost <4h wall-clock, no LLM calls.

## 17. References to Prior Evidence

- Parent EXP-PHYSICS-35749353065 (MEASUREMENT_INVALID, REVISE) — audit findings 1–9 and required_fixes 1–6 corrected here.
- EXP-PHYSICS-34764605162 audit V1_independent_noise_bakes_in_null — bounded falsification, correlated open.
- EXP-PHYSICS-35209110569/35262258744 — TodoMVC title degeneracy.
- EXP-PHYSICS-34038570933/34071626363/34149195420 — leakage 92–98% via target_href, PMI 1.073->0.0 when filtered.
- Frontier TV/KDE/binned — complementary blind spots, 95% non-stationary attenuation, per-type CV fails.
- Codex index 234 experiments, C-WEB-DYNAMICS 58 synthetic-only events, portfolio_assessment tunnel flag true.
- SPIDER_MASTER_PROMPT §15–22 (physics validity gates, strong nulls), SPIDER_ARCHITECTURE_RESEARCH2 §4–6 (packet, Codex), AGENTS.md transmission discipline.
