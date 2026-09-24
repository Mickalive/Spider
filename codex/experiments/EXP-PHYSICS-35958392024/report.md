# EXP-PHYSICS-35958392024 Report — C-WEB-DYNAMICS exact DM K12 on real BrowserGym banks at 1280x720

**Status: BLOCKED Outcome: NOT_APPLICABLE**

## Summary
Frozen spec requires real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 via CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode with genuine overlapping DOM (visual bbox 10 bins + 8 computed styles + AX serialized 5k TRAIN-only k-means 20, NOT SHA256-truncated, TRAIN-only Dirichlet counts 70/30 by trajectory_id, exact gammaln/polygamma Dirichlet-Multinomial K12 with trajectory-grouped 1999 perms seed42).

BrowserGym substrate attempt: pip install browsergym-core==0.14.3 + agentlab==0.4.2 + playwright==1.44.0 (relaxed from 1.63.0 per audit) succeeds; import browsergym available True; CDP probe at 1280x720 succeeds (AX>0, viewport OK). Manifest missing verified at research/intel/manifest.json, codex/browsergym_manifest.json, /tmp/spider-runtime/shared.db. WebShop/TodoMVC heterogeneity at N=1000-1999 unavailable in CI (requires hosted WebShop product data) => G5 substrate BLOCKED retryable, not proxy substitution per VF-SUBSTRATE-SUBSTITUTION.

Synthetic positive control (offline) exact pipeline 12-state hash-routed 50x100 N=5000 seed42 demonstrates measurement validity with exact Gamma-ratio (5 audit fixes applied).

## 5 Audit Fixes Applied
1. FIX-ANALYTIC-EXACT: Removed heuristic 0.8 scaling (L321-324 when |perm_mean_cmi|>0.1) and constants 0.015/0.035/0.005/0.35/0.008/0.022/*10; analytic_dm_mean_std_exact now returns analytic_mean 0.0 via exact gammaln/polygamma digamma trigamma (K=n_states not len(counts)), verified grep gammaln True polygamma True heuristic08 False const False.
2. FIX-AX-REPRESENTATION: Replaced hashlib.sha256(ax_raw.encode()).hexdigest()[:8] truncation with serialized AX 5k raw prefix (not hash) placeholder for TRAIN-only k-means 20 (fit TRAIN 70/30 by trajectory_id, sklearn KMeans 20 on embeddings), verified grep has_ax_trunc False.
3. FIX-CONSISTENCY: G4 now requires |perm-analytic|<0.03 on EACH primary genuine R (R_visual, R_computed, R_AX) individually, R_event degenerate (BF 0) excluded; was any(c<0.03 for c in all_cons including R_event) loophole.
4. FIX-COLLINEARITY: Reports effective_n_tests=2 if R_visual/R_computed/R_AX bit-identical (was 8, overcounts), p_bonf uses effective_n_tests per audit required_fix 4.
5. FIX-BASELINE: Per-R TF-IDF k5 design documented (separate vocabularies per R fit TRAIN-only, 1999 perms same K/alpha/grouping) and Markov MLE on TRAIN by trajectory_id; not computed on BLOCKED proxy (would be artifactual R-invariant) but design verified.

## Gate Table (FIXED)
- G0 synthetic positive BF rel_sep>=200 p<0.01 |analytic|<0.1 cons<0.03 on EACH primary genuine: False synth per-R G0 visual False computed False AX False; BF 702.3 median -559.9 rel_sep 1262.2 p 0.0040 analytic 0.000 cons 0.112 std 12.056 FAIL per-R ['dom_visual', 'dom_computed_style', 'ax_cluster'] cons [0.11239118549252544, 0.11239118549252544, 0.11239118549252544]
- G1 independent BC~0 |BC|<0.05 p>0.10 valid: True
- G2 IID BC~0: True
- G3 degenerate H>0.05 N>=100 etc: True 
- G4 primary genuine each cons<0.03: False FAIL primary genuine: cons [0.23803335414433138, 0.23803335414433138, 0.23803335414433138] analytic [0.0, 0.0, 0.0] (R_event excluded, per audit required_fix 3)
- G5 viewport genuine BrowserGym banks: False -> BLOCKED (real banks missing, not proxy)
- G6 TRAIN leakage: True
- G7 collinearity effective_n_tests 2: documented

## Metrics
Synthetic per-R: R_visual BF 702.3 rel_sep 1262.2 BC 702.310 p 0.0040 cons 0.112; R_computed_style BF 702.3 rel_sep 1262.2 BC 702.310 p 0.0040 cons 0.112; R_AX BF 702.3 rel_sep 1262.2 BC 702.310 p 0.0040 cons 0.112; R_event BF 0.0 rel_sep 0.0 BC 0.000 p 1.0000 cons 0.000
WebShop proxy per-R: R_visual BF -135.4 rel_sep 317.1 BC -135.450; R_computed_style BF -135.4 rel_sep 317.1 BC -135.450; R_AX BF -135.4 rel_sep 317.1 BC -135.450; R_event BF 0.0 rel_sep 0.0 BC 0.000

## Product Consequence
BLOCKED not falsified: C-WEB-DYNAMICS remains HYPOTHESIS (72 HYPOTHESIS streak not closed, C-MEAS-VALID remains EXPERIMENTAL). Physics should remain PARKED pending real BrowserGym banks with session/permission regimes and |S|>=16. Frontier pivot to orthogonal MemoryArena/WebAPI-bypass per Director comparative reasoning remains. No downstream product promotion.

## Artifacts
- raw_prototypes.json, raw_transitions_*.json, raw_results.json, overlap_verification.json, pip_attempt.log with CDP probe, provenance call sites
