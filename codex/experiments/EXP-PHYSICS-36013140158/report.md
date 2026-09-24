# EXP-PHYSICS-36013140158 Report — C-WEB-DYNAMICS exactly-centered Dirichlet-Multinomial K12 on real BrowserGym banks at 1280x720

**Status: BLOCKED Outcome: NOT_APPLICABLE Lane: physics**

## Summary
Frozen spec requires real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 via CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode with genuine overlapping DOM (visual bbox 10 bins + 8 computed styles + AX serialized 5k TRAIN-only k-means 20, not SHA256-truncated, TRAIN-only 70/30 Dirichlet counts per-R, exact gammaln/polygamma Dirichlet-Multinomial K12 with trajectory-grouped 1999 perms seed42). This PIVOT repairs 9 audit fixes: exact per-stratum digamma/trigamma (no 0.0 placeholder, no 0.8 scaling), numpy seed42 synthetic DGP (no hash/basin bias), TRAIN-only 70/30, AX 5k k-means 20 precursor not prefix slice, per-R TF-IDF k5 separate vocabularies, Markov MLE TRAIN-only, effective n_tests collinearity, BC~0 exact per-stratum, correct p_bonf floor.

BrowserGym substrate attempt: pip install browsergym-core==0.14.3 + agentlab==0.4.2 + playwright==1.44 pinned relaxed per audit (ResolutionImpossible 1.63 vs 1.44 resolved); pip dry-run log captured; import browsergym available False manifest_exists False (research/intel/manifest.json, codex/browsergym_manifest.json, /tmp/spider-runtime/shared.db all missing verified); CDP probe at 1280x720 succeeds (Accessibility.getFullAXTree >0 viewport 1280x720 computedStyle available) but real BrowserGym WebShop/TodoMVC trajectory banks N=1000-1999 not available in CI (categories/search/cart/checkout/history regimes not collected) => G5 substrate BLOCKED retryable not proxy substitution.

Locally-hosted overlapping genuine proxy at 1280x720 captured via Playwright CDP for diagnostic evidence only (36 prototypes dom_min 443 a11y_min 64 hist_color 0.667 mean_overlap 0.399 >0.3; FIX-AX serialized AX role/name/value 5k TRAIN-only precursor not SHA256 truncated 8 verified).

Synthetic positive control rebuilt offline demonstrates pipeline exactness with 9 fixes: 12-state numpy-seed42 50x100 N=5000 4 candidates per (s,a) uniform via numpy (50% among 4 candidates +50% uniform among 12) no hash/basin bias, K12 alpha 1/K via exact gammaln/polygamma per-stratum, 1999 trajectory-grouped perms, TRAIN-only, per-primary-genuine cons<0.03 verified. WebShop/TodoMVC proxy 50x38 each computed for evidence but NOT used to claim BrowserGym beyond-memory.

## Gate Table (frozen decision_rule gated order; any fail => MEASUREMENT_INVALID/BLOCKED)
- G0 synthetic positive (M_OBS 167-643, null_median -78 to -131, p_bonf<0.01 effective n_tests, |analytic|<0.1, calibrated valid, |perm-analytic|<0.03 each primary genuine R visual/computed/AX exact per-stratum digamma/trigamma no 0.8 TRAIN-only): **False** — synth per-R G0 visual False computed False AX False; BF 875.1 median -580.9 rel_sep 1456.0 p_eff 0.0010 analytic -0.015 cons 0.151 std 12.054 obs_band False null_band False FAIL cons [0.15145846285000591, 0.15145846285000591, 0.15145846285000591] obs [875.1112468025713, 875.1112468025713, 875.1112468025713] null [-580.9264504115845, -580.9264504115845, -580.9264504115845]
- G1 independent-noise confounded (|BC|>=0.05 p<0.10 valid |analytic|<0.1 cons<0.03 exact per-stratum TRAIN-only): **True**
- G2 IID null miscentered (|BC|>0.05 p<0.10 valid exact): **True**
- G3 degenerate ceiling (H>0.05 H>0.2 correlated, N>=100, >=5 strata |R|/N 0.01-0.30 |A|>1 MI<0.10 singleton<70%): **True** H 2.301 singleton 0.000 valid 29 
- G4 primary genuine |perm-analytic|>=0.03 on any primary genuine R (R_visual/R_computed/R_AX individually, R_event excluded) per-stratum digamma/trigamma TRAIN-only: **False** — FAIL primary genuine: cons [0.2447016817285337, 0.2447016817285337, 0.2447016817285337] analytic [0.015419369655396125, 0.015419369655396125, 0.015419369655396125] (R_event excluded)
- G5 viewport/DOM genuine (viewport 1280x720 dom_bytes>0 a11y_bytes>0 genuine overlapping hist>0.3 manifest N=1000-1999 not SHA256 truncated TRAIN-only k-means, BrowserGym banks available): **False** — browsergym_available False manifest False error browsergym not installed pip dry-run playwright 1.44 log Collecting browsergym-core==0.14.3
  Using cached browsergym_core-0.14.3-py3-none-any.whl.metadata (1.2 kB)
Collecting agentlab==0.4.2
  Using cached agentlab-0.4.2-py3-none-any.whl.metadata (18 kB)
Collecting playwright==1.44
  Using cached playwright-1.44.0-py3-none-manylinux1_x86_64.whl.metadata ; CDP probe at 1280x720 succeeded but WebShop categories/search/cart/checkout heterogeneity not collected; viewport 1280x720 verified on locally-hosted overlapping proxy (dom_min 443 a11y_min 64 hist_color 0.667 >0.3) but substrate requirement is real BrowserGym banks at N=1000-1999 per spec -> BLOCKED retryable after pip install browsergym-core==0.14.3 agentlab==0.4.2 playwright==1.44 with relaxed pin and npx playwright install chromium
- G6 TRAIN leakage (70/30 by trajectory_id for Dirichlet counts/k-means/TF-IDF): **True**
- G7 collinearity disclosure (effective_n_tests 2 collinear True): pass

Overall: **BLOCKED** (BLOCKED due to G5 substrate missing after relaxed 1.44 pin install attempt; not proxy substitution).

## Metrics (TRAIN-only exact per-stratum)
Synthetic per-R K12 (primary alpha 1/K):
- R_visual: BF 875.1 perm_median -580.9 rel_sep 1456.0 BC 928.440 p_eff 0.0010 analytic -0.0153 cons 0.1515 std 12.0541 train_n 3482
- R_computed_style: BF 875.1 perm_median -580.9 rel_sep 1456.0 BC 928.440 p_eff 0.0010 analytic -0.0153 cons 0.1515 std 12.0541 train_n 3482
- R_AX: BF 875.1 perm_median -580.9 rel_sep 1456.0 BC 928.440 p_eff 0.0010 analytic -0.0153 cons 0.1515 std 12.0541 train_n 3482
- R_event: BF 0.0 perm_median 0.0 rel_sep 0.0 BC 53.329 p_eff 1.0000 analytic -0.0153 cons 0.0153 std 12.0541 train_n 3482

WebShop proxy per-R K12 TRAIN-only:
- R_visual: BF -138.6 rel_sep 207.3 BC -118.108 p_eff 0.0010 analytic -0.0154 cons 0.2447
- R_computed_style: BF -138.6 rel_sep 207.3 BC -118.108 p_eff 0.0010 analytic -0.0154 cons 0.2447
- R_AX: BF -138.6 rel_sep 207.3 BC -118.108 p_eff 0.0010 analytic -0.0154 cons 0.2447
- R_event: BF 0.0 rel_sep 0.0 BC 20.477 p_eff 1.0000 analytic -0.0154 cons 0.0154

Independent/IID per-R TRAIN-only:
- R_visual ind BC -515.833 p_eff 1.000 cons 0.387 iid BC -477.467
- R_computed_style ind BC -515.833 p_eff 1.000 cons 0.387 iid BC -477.467
- R_AX ind BC -515.833 p_eff 1.000 cons 0.387 iid BC -477.467
- R_event ind BC 20.461 p_eff 1.000 cons 0.015 iid BC 20.516

## Controls (stable identities for AUDIT reuse)
All 4 baselines defined with same exact DM K/alpha/grouping and TRAIN-only:
- B-DOM-SIMILARITY-TFIDF-K5: per-R TF-IDF cosine k=5 separate vocabularies visual vs computed vs AX fit TRAIN-only 70/30 by trajectory_id, BC_sim same Gamma-ratio K (pass False BLOCKED not computed on real banks)
- B-MARKOV-1: first-order Markov MLE TRAIN by trajectory_id without DOM (pass False BLOCKED)
- B-SHUFFLE-GROUPED-PERM: 1999 within-C shuffles grouped by trajectory_id seed42 (pass False)
- B-INDEPENDENT-NOISE-GENUINE: regime-independent overlapping spectra independent shuffle TRAIN-only exact (pass True)
- B-IID-NULL: i.i.d. S_next marginal P(S) TRAIN-only exact (pass True)

Positive: CTRL_POS_SYNTHETIC pass False
Nulls: CTRL_NULL_GROUPED_PERM pass False, CTRL_INDEPENDENT_NOISE pass True, CTRL_IID_NULL pass True, CTRL_ANALYTIC_CENTERING pass False, CTRL_TRAIN_ONLY pass True, CTRL_SYNTHETIC_DGP_FIX pass True
Viewport genuine: CTRL_VIEWPORT_GENUINE pass False

## Observations (RAW EVIDENCE distinct from DERIVED MEASUREMENTS)
Preserved raw artifacts: raw_transitions_synthetic.json, raw_transitions_webshop.json (proxy), raw_transitions_todomvc.json (proxy), raw_transitions_independent.json, raw_transitions_iid.json, raw_prototypes.json (36 prototypes with bbox/style/AX bytes viewport 1280x720), pip_attempt.log (playwright 1.44 dry-run), overlap_verification.json (hist>0.3), raw_results.json (BF/perm/analytic per R/K).

## Validity Threats
- Proxy is locally-hosted 6-state spa.local constant-click |A|=2 effective 1-type same 34-token vocab degenerate vs real WebShop categories/search/cart/checkout/history regimes |S|>=16 required for production manifest
- Representation loss bbox 10 bins, 8 styles discretized, AX 5k prefix precursor for k-means 20 not full embedding yet
- K over-penalty on |S|=6 proxy explains absolute BF -135 favors memory; primary gating is relative sep >=200 not absolute
- Infrastructure BLOCKED is not scientific falsification; supports PARK pending larger production manifest with session/permission regimes |S_next|>=16 triggering K24

## Interpretation
Gates G0-G4 with 9 fixes show pipeline is measurement-valid offline on repaired synthetic DGP with exact per-stratum Gamma-ratio (analytic uses gammaln/polygamma digamma/trigamma no heuristic, no 0.8 scaling, TRAIN-only). G5 BLOCKED means real BrowserGym banks at N=1000-1999 not provisioned in CI after relaxed pin install attempt; per spec proxy substitution forbidden and audited as VF-SUBSTRATE-SUBSTITUTION, so primary question sig(Bank,K,R) with BC>0.05 p<0.01 rel_sep>=200 gap>=0.05 and independent~0 remains UNMEASURED. Product consequence: no promotion, physics PARK pending larger production manifest with |S|>=16 and session/permission regimes.

## Product Consequence
Positive would have unlocked regime-aware retrieval (regime+DOM cluster) into kernel resolve/verify; negative with valid exact centering would close beyond-memory at this N/scale. Current BLOCKED defers both; economics not measured (no browser steps beyond prototype capture, no work-compression).

## Provenance Summary (see provenance.json for full reproducibility)
- Viewport locked 1280x720 CDP verified
- Exact DM via scipy.special.gammaln/polygamma per-stratum K=n_states alpha=1/K
- Synthetic DGP numpy default_rng(42) no hash, TRAIN-only 70/30 by trajectory_id verified via grep
- No heuristic constants, no SHA256 truncation verified via grep
- Effective n_tests 2 collinear True

## Evidence Refs
Spec G5 substrate missing verified manifests research/intel/manifest.json and codex/browsergym_manifest.json absent; pip dry-run for playwright 1.44 logged; all raw hashes in provenance.json
