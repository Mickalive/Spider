# EXP-RUNTIME-35908617140 — Execution Report

**Status:** MEASUREMENT_INVALID
**Outcome:** INCONCLUSIVE
**Lane:** runtime
**Claims:** C-MEAS-VALID, C-FRESHNESS

## Distributed C-FRESHNESS (B-SHARED-STORE primary)

| Metric | Value | Target |
|--------|-------|--------|
| freshness_c1_tn_mean | 0.9760 | >=0.85 |
| freshness_c1_tn_wilson_lo | 0.9572 | >0.75 |
| freshness_c1_tn_session_status | 0.9281 | >=0.85 |
| freshness_c1_tn_profile | 1.0000 | Wilson lo>0.75 |
| freshness_c1_tn_data_list | 1.0000 | Wilson lo>0.75 |
| freshness_n_non304 | 1070 | >=800 |
| freshness_n_304 (real) | 130 | >0 |
| freshness_stratified_r | 0.3052 | abs<0.15 |
| freshness_stratified_r_ci_upper | 0.3587 | <0.15 |
| freshness_tost_p_upper | 1.0000 | <0.05 |
| freshness_fp_noise | 0.0000 | <=0.15 |
| freshness_c2_variance | 8/8 | 8/8 |
| freshness_hs256_valid_success_rate | 0.9853 | >=0.90 |
| freshness_worker_distribution | {'46687': 603, '46688': 597} | >=10 each |
| batch_state_log lines | 31 | >=27 |

### B-PER-NODE baseline (expected TN~0.667)

| Metric | Value |
|--------|-------|
| tn_mean | 0.6667 |
| tn_session_status | 0.0000 |
| tn_profile | 1.0000 |
| tn_data_list | 1.0000 |

### B-STICKY-URL (exploratory E4: hash $request_uri consistent, no session mirroring)

| Metric | Value | Target |
|--------|-------|--------|
| tn_mean | null | >=0.85 |
| workers | {'46947': 720, '46948': 480} | skewed by URI |
| per_uri_affinity | {'/api/session/status?u=3': 1.0, '/api/profile?u=2': 1.0, '/api/profile?u=1': 1.0, '/api/profile?u=3': 1.0, '/api/session/status?u=2': 1.0, '/api/data_list?u=3': 1.0, '/api/session/status?u=1': 1.0, '/api/data_list?u=1': 1.0, '/api/data_list?u=2': 1.0, '/api/profile?u=4': 1.0} | >0.90 each |
| overall_skew | 0.6000 | reported |

### Validity gates (frozen fixes)

| Gate | Pass |
|------|------|
| V-HEALTH-GATE (0 missing worker/status None) | True |
| V-STATUS-FREE-STRUCTURAL (no status prefix) | False |
| V-SCHEDULING-INDEPENDENCE (|r|<0.30) | True |
| freshness_scheduling_confound_r | 0.0661 |
| freshness_structural_status_prefix_present | True |

## Browser C-MEAS-VALID (Playwright 1280x720)

| Metric | Value | Target |
|--------|-------|--------|
| bg_provision_ok | None | true |
| bg_agentlab_version | None | 0.4.2 |
| bg_playwright_viewport | None | 1280x720 |
| bg_ax_nodes_median | None | >10 |
| bg_pc_health_pct | null | >=80 |
| bg_dom_nodes_median | None | 21-82 |
| bg_dom_nodes_range_ok | None | true |
| browser_body_AvsC_full | null | >0.5 |
| browser_body_AvsC_status | null | 0.0 |
| browser_body_AvsC_headers_no_clen | null | 0.0 |
| browser_header_AvsE_full | null | >0.5 |
| browser_header_AvsE_headers | null | 1.0 |
| browser_header_AvsE_body | null | 0.0 |
| browser_null_body_full | null | <=0.05 |

## Controls

| Control | Pass |
|---------|------|
| C1-FRESHNESS | True |
| C2-FRESHNESS | True |
| C3-FRESHNESS | False |
| C4-FRESHNESS | True |
| C5-BROWSER | None |
| C6a-BODY-DISCRIM | None |
| C6b-HEADER-DISCRIM | None |
| C6c-BROWSER-NULL | None |
| B-PER-NODE | True |
| B-SHARED-STORE | True |
| B-STICKY-URL | False |
| V-HEALTH-GATE | True |
| V-STATUS-FREE-STRUCTURAL | False |
| V-SCHEDULING-INDEPENDENCE | True |

## Validity notes

- Unexpected browser failure: Traceback (most recent call last):
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-RUNTIME-35908617140/run_experiment.py", line 2494, in main
    browser_obs, ax_pages, provision = run_browser_harness(
                                       ^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-RUNTIME-35908617140/run_experiment.py", line 1590, in run_browser_harness
    from playwright.sync_api import sync_playwright
ModuleNotFoundError: No module named 'playwright'

- Measurement invalidity triggers: STATUS_PREFIX_STILL_PRESENT
- Infrastructure errors: BROWSER_UNEXPECTED: No module named 'playwright'

## Unresolved

- None
