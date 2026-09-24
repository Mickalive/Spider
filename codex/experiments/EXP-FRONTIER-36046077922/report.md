# EXP-FRONTIER-36046077922 — Execution Report

**Lane:** frontier  
**Claim:** C-WEB-DYNAMICS (Interactive Web transformations contain predictive dynamical structure beyond memory and ordinary similarity)  
**Status:** MEASUREMENT_INVALID  
**Outcome:** NOT_APPLICABLE  
**Executed:** 2026-09-24T19:19:59.082368Z  
**Duration:** 0.0s  

## Summary

This experiment was designed to test **C-WEB-DYNAMICS** via barrier-physics rewind on live BrowserGym 1280x720 CDP AX>10 heterogeneous sites with Intel diverse-site manifest and Runtime health-gated substrate, using history-conditioned bias-corrected PMI with trajectory-grouped permutation (BC PMI > 0.05 bits, Bonferroni p < 0.01, gap ≥ 0.05 over TF-IDF k5, rel_sep ≥ 200).

**Result: MEASUREMENT_INVALID** — Required infrastructure dependencies are not available. This is an infrastructure failure, not a scientific falsification.

## Dependency Verification

| Dependency | Required | Available | Details |
|------------|----------|-----------|---------|
| BrowserGym 1280x720 CDP AX>10 | Live heterogeneous collection | False | BrowserGym import failed: ModuleNotFoundError: No module named 'browsergym' |
| BrowserGym CDP launch | 1280x720 viewport, AX>10 nodes | False | BrowserGym import failed: ModuleNotFoundError: No module named 'browsergym' |
| Intel diverse-site manifest | ≥10 families, Jaccard<0.30, product-subtree anchored | False | families=0, jaccard_max=1.0000, product_subtree=False |
| Runtime health-gated substrate | Flask HS256+nginx, sticky, WAL, n_non304≥800, honest counters | False | No Runtime substrate found at expected paths |
| Physics PARK | No concurrent Dirichlet-Multinomial | True | Per director_mandate |

## Validity Notes

- BrowserGym not available: BrowserGym import failed: ModuleNotFoundError: No module named 'browsergym'
- Intel diverse-site manifest unavailable: No Intel diverse-site manifest found at expected paths
- Runtime health-gated substrate unavailable: No Runtime substrate found at expected paths

## Unresolved (Smallest Next Actions)

- Install playwright, browsergym-core, agentlab for live 1280x720 CDP AX>10 collection
- Produce Intel manifest with ≥10 families Jaccard<0.30 product-subtree anchored at 1280x720 from WebGym 292k or WebArena-Verified v2 192/36
- Deploy Runtime single-worker sticky Flask HS256+nginx with honest per-trajectory counters, If-None-Match/ETag TTL 60s, n_non304≥800 stratified, trajectory-grouped |rho_shuffled|<0.20

## Controls Status

All positive and null controls are **not run** due to missing dependencies. Per frozen `measurement_validity` and `decision_rule`, any PC/NC failure (including unmet dependencies) triggers **MEASUREMENT_INVALID** — no SURVIVES/FALSIFIED inference is permitted.

| Control ID | Expected | Observed | Pass |
|------------|----------|----------|------|
| PC-SYNTHETIC-PIPELINE | BC>1.0 p<0.01 | not_run | N/A |
| PC-BROWSERGYM-HETEROGENEITY | ≥10 families Jaccard<0.30 AX>10 | not_run | N/A |
| PC-CEILING-NONDEGENERATE | H≥0.4 (K=1), H≥0.2 (K=3) | not_run | N/A |
| PC-RUNTIME-HEALTH | n_non304≥800 stratified, |rho_shuffled|<0.20 | not_run | N/A |
| NC-TRAJECTORY-GROUPED-CENTERED | |BC_shuffled|<0.05, p≥0.20 | not_run | N/A |
| NC-LEAKAGE-FILTERED | shuffled |BC|<0.05, p≥0.20 | not_run | N/A |
| NC-TRAIN-VOCAB-ISOLATED | 0 leakage | not_run | N/A |
| NC-SITE-HOLDOUT | LOFO within 50%, site_id PMI≈0 | not_run | N/A |

## Metrics

```json
{
  "live_available": false,
  "browsergym_available": false,
  "browsergym_cdp_available": false,
  "intel_families": 0,
  "intel_jaccard_max": 1.0,
  "intel_product_subtree": false,
  "runtime_available": false,
  "physics_parked": true
}
```

## Artifacts

No measurement artifacts produced (dependencies unavailable).

## Conclusion

The experiment cannot execute its frozen design because the required measurement substrate is not available:

1. **BrowserGym/playwright** not installed → cannot collect live 1280x720 CDP AX>10 trajectories
2. **Intel diverse-site manifest** not produced → no ≥10 families with Jaccard<0.30 product-subtree anchoring
3. **Runtime health-gated substrate** not deployed → no honest per-trajectory counters, no n_non304≥800 stratified conditional probes

Per `SPIDER_MASTER_PROMPT.md` Physics validity gate and `research/EXPERIMENT_PACKET.md`: **MEASUREMENT_INVALID takes precedence over SURVIVES/FALSIFIED**. No substantive claim follows from invalid measurement.

The frozen `prereg.md §7` decision rule explicitly states: `MEASUREMENT_INVALID if any PC/NC fails (including unmet dependencies runtime/intel, NL<100, strata<5, H<0.2 ceiling, vocab leakage >0, not trajectory-grouped, Jaccard≥0.30, resolution ≠1280x720, AX≤10) → no SURVIVES/FALSIFIED inference; report exact failure in validity_notes/unresolved and smallest next action.`

This MEASUREMENT_INVALID result **does not falsify C-WEB-DYNAMICS**. The claim remains HYPOTHESIS per codex/claim_state.json. The orthogonal barrier-physics rewind test remains pending the single-node honesty gate (Runtime n_non304≥800 stratified + Intel Jaccard<0.30 manifest) as mandated by the Global Research Director.

## Next Steps (per unresolved)

1. Install playwright, browsergym-core, agentlab with display support for live BrowserGym 1280x720 CDP
2. Generate Intel diverse-site manifest from WebGym 292k (≥50 eTLD+1) or WebArena-Verified v2 192/36 with deterministic sampling seed 42, Jaccard<0.30 verification, product-subtree anchoring
3. Deploy Runtime single-worker sticky Flask HS256+nginx with /tmp/spider-runtime/shared.db WAL, honest per-trajectory hard-reset counters (resolve+bind+verify+freshness+browser_steps), If-None-Match/ETag TTL 60s conditional probes, trajectory-grouped |rho_shuffled|<0.20 validation, n_non304≥800 stratified

Only after all dependencies are verified can the live barrier-physics rewind test execute and produce a valid SURVIVES_CURRENT_TEST or FALSIFIED-IN-SETTING outcome.
