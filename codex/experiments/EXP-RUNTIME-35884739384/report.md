# EXP-RUNTIME-35884739384 — Execution Report

**Status:** COMPLETE
**Outcome:** MIXED
**Lane:** runtime
**Claims:** C-MEAS-VALID, C-FRESHNESS

## Distributed C-FRESHNESS (B-SHARED-STORE primary)

| Metric | Value | Target |
|--------|-------|--------|
| freshness_c1_tn_mean | 0.9860 | >=0.85 |
| freshness_c1_tn_wilson_lo | 0.9695 | >0.75 |
| freshness_c1_tn_session_status | 0.9580 | >=0.85 |
| freshness_c1_tn_profile | 1.0000 | Wilson lo>0.75 |
| freshness_c1_tn_data_list | 1.0000 | Wilson lo>0.75 |
| freshness_n_non304 | 1052 | >=800 |
| freshness_n_304 (real) | 131 | >0 |
| freshness_stratified_r | -0.3579 | abs<0.15 |
| freshness_stratified_r_ci_upper | -0.3039 | <0.15 |
| freshness_tost_p_upper | 0.0000 | <0.05 |
| freshness_fp_noise | 0.0000 | <=0.15 |
| freshness_c2_variance | 8/8 | 8/8 |
| freshness_hs256_valid_success_rate | 0.9911 | >=0.90 |
| freshness_worker_distribution | {'65443': 588, '65439': 595} | >=10 each |
| batch_state_log lines | 31 | >=27 |

### B-PER-NODE baseline (expected TN~0.667)

| Metric | Value |
|--------|-------|
| tn_mean | 0.6667 |
| tn_session_status | 0.0000 |
| tn_profile | 1.0000 |
| tn_data_list | 1.0000 |

### B-STICKY (exploratory)

| Metric | Value |
|--------|-------|
| tn_mean | 0.9603 |
| workers | {'65764': 1200} |

## Browser C-MEAS-VALID (Playwright 1280x720)

| Metric | Value | Target |
|--------|-------|--------|
| bg_provision_ok | True | true |
| bg_agentlab_version | 0.4.2 | 0.4.2 |
| bg_playwright_viewport | {'width': 1280, 'height': 720} | 1280x720 |
| bg_ax_nodes_median | 54.0 | >10 |
| bg_pc_health_pct | 100.0 | >=80 |
| bg_dom_nodes_median | 26.0 | 21-82 |
| bg_dom_nodes_range_ok | True | true |
| browser_body_AvsC_full | 1.0000 | >0.5 |
| browser_body_AvsC_status | 0.0000 | 0.0 |
| browser_body_AvsC_headers_no_clen | 0.0000 | 0.0 |
| browser_header_AvsE_full | 1.0000 | >0.5 |
| browser_header_AvsE_headers | 1.0000 | 1.0 |
| browser_header_AvsE_body | 0.0000 | 0.0 |
| browser_null_body_full | 0.0000 | <=0.05 |

## Controls

| Control | Pass |
|---------|------|
| C1-FRESHNESS | True |
| C2-FRESHNESS | True |
| C3-FRESHNESS | False |
| C4-FRESHNESS | True |
| C5-BROWSER | True |
| C6a-BODY-DISCRIM | True |
| C6b-HEADER-DISCRIM | True |
| C6c-BROWSER-NULL | True |
| B-PER-NODE | True |
| B-SHARED-STORE | True |
| B-STICKY | True |

## Validity notes

- None

## Unresolved

- None
