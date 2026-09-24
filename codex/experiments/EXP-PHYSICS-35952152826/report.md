# EXP-PHYSICS-35952152826 Report — C-WEB-DYNAMICS exact DM K12 on real BrowserGym banks at 1280x720

**Status: BLOCKED Outcome: NOT_APPLICABLE**

## Summary
Frozen spec requires real BrowserGym WebShop/TodoMVC trajectory banks at locked 1280x720 via CDP Accessibility.getFullAXTree + DOM.getDocument + DOM.getBoxModel + CSS.getComputedStyleForNode with genuine overlapping DOM (visual bbox 10 bins + 8 computed styles + AX serialized 5k TRAIN-only k-means 20, not SHA256-truncated, TRAIN-only Dirichlet counts 70/30 by trajectory_id, exact gammaln/polygamma Dirichlet-Multinomial K12 with trajectory-grouped 1999 perms seed42).

BrowserGym substrate attempt: pip install browsergym-core==0.14.3 + agentlab==0.4.2 + playwright==1.63.0 pinned as per director mandate. Dry-run fails: browsergym-core 0.14.3 depends on playwright==1.44 vs required 1.63 -> ResolutionImpossible (conflict). Manifest missing verified at research/intel/manifest.json and codex/browsergym_manifest.json. Viewport 1280x720 verified on locally-hosted overlapping proxy (36 prototypes dom_min 443 a11y_min 64 hist_color 0.667 >0.3) but real BrowserGym WebShop categories/search/cart heterogeneity at N=1000-1999 unavailable => G5 substrate BLOCKED.

Synthetic positive control (offline) demonstrates exact pipeline is measurement-valid: 12-state hash-routed 50x100 N=5000 seed42, 4 candidates per (s,a) 50% hash +50% uniform, K12 alpha 1/K via exact gammaln/polygamma, 1999 trajectory-grouped perms. Proxy WebShop/TodoMVC 50x38 each computed for evidence but NOT used to claim BrowserGym beyond-memory.

## Gate Table
- G0 synthetic positive BF rel_sep>=200 p<0.01 |analytic|<0.1 cons<0.03: True synth BF 654.8 median -456.4 rel_sep 1111.2 p 0.0040 analytic -0.091 cons 0.000 std 12.055
- G1 independent BC~0: True
- G2 IID BC~0: True
- G3 degenerate H>0.05 N>=100 >=5 strata |R|/N 0.01-0.30 |A|>1 MI<0.10: True 
- G4 consistency |perm-analytic|<0.03: True
- G5 substrate genuine 1280x720 BrowserGym WebShop/TodoMVC overlapping: False => BLOCKED (not MEASUREMENT_INVALID proxy substitution)
- G6 TRAIN leakage: True

G5 fails due to infrastructure dependency conflict + missing manifest, not heuristic or baseline artifact. Per spec, this emits BLOCKED retryable, not falsification. Proxy substitution forbidden per audit VF-SUBSTRATE-SUBSTITUTION and not used to claim.

## Per-R Synthetic K12 (exact, offline)
- R_visual: BF 654.8 perm_median -456.4 rel_sep 1111.2 bc 1110.597 p_bonf 0.0040 analytic -0.091 cons 0.000 std 12.055
- R_computed_style: BF 654.8 perm_median -456.4 rel_sep 1111.2 bc 1110.597 p_bonf 0.0040 analytic -0.091 cons 0.000 std 12.055
- R_AX: BF 937.4 perm_median -158.0 rel_sep 1095.4 bc 1094.888 p_bonf 0.0040 analytic -0.032 cons 0.000 std 12.055
- R_event: BF 0.0 perm_median 0.0 rel_sep 0.0 bc 0.000 p_bonf 1.0000 analytic 0.000 cons 0.000 std 12.055

## Proxy Per-R (not BrowserGym, for pipeline evidence only)
- WebShop proxy R_visual: BF -135.4 rel_sep 317.1 bc 226.361 p 0.0040 cons 0.048
- WebShop proxy R_computed_style: BF -135.4 rel_sep 317.1 bc 226.361 p 0.0040 cons 0.048
- WebShop proxy R_AX: BF -135.4 rel_sep 317.1 bc 226.361 p 0.0040 cons 0.048
- WebShop proxy R_event: BF 0.0 rel_sep 0.0 bc 0.000 p 1.0000 cons 0.000

## Decision
BLOCKED: Real BrowserGym banks at 1280x720 N=1000-1999 unavailable after pip dry-run attempt (playwright 1.63 vs 1.44 conflict) + manifest missing. Primary question On real BrowserGym WebShop/TodoMVC ... does observed log BF exceed null by >=200 nats remains UNMEASURED. No beyond-memory claim update. Physics remains PARKED pending substrate.

Synthetic positive shows exact DM pipeline passes G0 with valid centering |analytic|<0.1 cons<0.03 calibrated std valid, so measurement is valid when substrate available. Locally-hosted proxy demonstrates overlapping genuine rendering at 1280x720 but bounded to 6-state SPA not production heterogeneity.

## Validity Notes
- Exact gammaln/polygamma used, no heuristic constants 0.015/0.035/0.005/0.35/0.008/0.022/*10 present (grep verifiable)
- Representation loss: bbox 10 bins, style 8 values, AX 5k preserved, k-means 20 TRAIN-only not exercised due to BLOCKED
- Overlapping spectra hist >0.3 verified
- Independent regime-independent not S_current%2
- No BrowserGym reuse; primary locally-hosted proxy bounded

## Artifacts
- raw_prototypes.json, raw_transitions_*.json, raw_results.json, overlap_verification.json, pip_attempt.log
- Code: execute_35952152826.py uses scipy.special.gammaln/polygamma exactly
