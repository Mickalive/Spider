# EXP-RUNTIME-36044045537 — Minimal Single-Node Honesty Gate REOPEN

**Status:** COMPLETE
**Outcome:** SUPPORTS
**Lane:** runtime
**Claim:** C-MEAS-VALID

## Controls

| V-NGINX-CONFIG-OK | PASS | 2026/09/24 19:02:33 [warn] 56578#56578: load balancing method redefined in /tmp/spider-runtime/36044045537/nginx.conf:10
nginx: the configuration file /tmp/spider-runtime/36044045537/nginx.conf syntax | nginx -t syntax ok exclusive -c |
| V-FLASK-LISTENING | PASS | socket connect ok | Flask verified listening 127.0.0.1:19860 |
| V-EXCLUSIVE-NGINX-C | PASS | ps aux shows experiment nginx -c | nginx -c /tmp/spider-runtime/36044045537/nginx.conf exclusively loaded |
| V-NGINX-CACHE-PERMS | PASS | No Permission denied in nginx_error.log | No Permission denied |
| V-HEALTH-GATE | PASS | 1 attempts, last status {'attempt': 0, 'status': 200, 'worker': '56580, 56580'} | 0 missing X-Worker-Pid |
| C1-FRESHNESS-NON304 | PASS | n_non304=850 per_ep={'/api/profile': 422, '/api/data_list': 428} hs_rate=1.0 batch=26 missing=0 | n_non304>=800 stratified 400/endpoint hs>=0.90 batch>=10 0 missing |
| C2-ORTHOGONALITY | PASS | r=0.0000 abs=0.0000 V=0.0531 mean_j=1.0000 n=400 | |r|<0.30 V<0.30 de-confounded |
| C3-HONEST-COST | PASS | |rho_shuffled|=0.0397 p=0.3740 rho_obs=0.0442 std=4.4680 width=0.1163 eff=6 nullFP=0.0000 | |rho_shuffled|<0.20 p>=0.20 within-f std>0 width>0 effective>1 nullFP<=0.05 |
| C4-FULL-VECTOR | PASS | full=0.7619 body=0.3810 status=0.0000 bodyVar=1.0000 hdrVar=1.0000 width=0.1143 eff=4 diff_lo=0.3143 null=0.0000 nginx=1.0000 | full>0.5 full>max(body,status)+0.05 width>0 eff>1 diff_lo>0 nullFP<=0.05 |
| C5-LOOPBACK-SECONDARY | FAIL | header=0.9583 body=1.0000 nullFP=0.0000 HIT=330/330 | 2x header~1.0 body~1.0 nullFP<=0.05 HIT330 greedy executed |
| B-FULL-VECTOR | PASS | full=0.7619 lo=0.7048 hi=0.8190 | full>0.5 full>max+0.05 non-degenerate |
| B-BODY-ONLY | PASS | body_only=0.3810 bodyVar_bodyOnly=1.0000 hdrVar_bodyOnly=0.0000 | 1.0 body-varying 0.0 header-varying |
| B-STATUS-ONLY | PASS | status_only=0.0000 | 0.0 |
| B-HEADER-ONLY-JACCARD | PASS | r=0.0000 V=0.0531 | |r|<0.30 V<0.30 |
| B-HEADER-HASH-REJECTED | PASS | filtered MINUS body-derived preserves Cache-Control/Set-Cookie/Vary; hash surrogate not used | surrogate would fail |r|>>0.30 if used |
| B-COST-SHUFFLED | PASS | |rho_shuffled|=0.0397 p=0.3740 n_traj=401 | |rho|<0.20 p>=0.20 block-permuted trajectory_id B=1000 integer sums |
| B-HEADERS-NO-BODYDERIVED | PASS | bodyVar=1.0000 hdrVar=1.0000 via filtered headers | 0.0 body-only 1.0 header-only isolated |
| PC-304-REAL | PASS | n_non304=850 hs=1.0 missing=0 | n_non304>=800 hs>=0.90 0 missing |
| PC-HEADER-ONLY | PASS | r=0.0000 V=0.0531 | |r|<0.30 V<0.30 |
| PC-HONEST-COST-SANITY | PASS | |rho|=0.0397 p=0.3740 | |rho_shuffled|<0.20 p>=0.20 integer sums block perm |
| PC-FULL-VECTOR | PASS | full=0.7619 width=0.1143 | full>0.5 non-degenerate |
| PC-LOOPBACK-2X | FAIL | header=0.9583 body=1.0000 | drift~1.0 nullFP<=0.05 |
| NC-ORTHOGONALITY-NOISE | PASS | no_drift_jaccard_mean=1.0000 | noise-only FP<=0.15 |
| NC-COST-SHUFFLED | PASS | |rho|=0.0397 p=0.3740 | |rho_shuffled|<0.20 p>=0.20 |
| NC-EXCLUSIVE-NGINX | PASS | exclusive=True cache_perms=True | exclusive nginx -c no Permission denied |

## Metrics

- **freshness_n_total**: 1008
- **freshness_n_non304**: 850
- **freshness_n_304**: 158
- **freshness_n_missing_worker**: 0
- **freshness_hs256_valid_success_rate**: 1.0
- **freshness_batch_distinct_ts**: 26
- **freshness_per_ep_non304**: {'/api/profile': 422, '/api/data_list': 428}
- **freshness_per_ep_304**: {'/api/profile': 82, '/api/data_list': 76}
- **freshness_scheduling_confound_r**: 0.0
- **freshness_scheduling_r_raw**: 0.0
- **freshness_scheduling_p**: 1.0
- **freshness_cramers_v**: 0.0531
- **freshness_header_only_jaccard_mean**: 1.0
- **freshness_header_only_jaccard_ci_lo**: -0.0981
- **freshness_header_only_jaccard_ci_hi**: 0.0981
- **freshness_header_only_variance**: 0.0
- **freshness_header_only_preserves_cache_control**: True
- **freshness_scheduling_confound_r_freshness**: 0.0154
- **honest_cost_rho_shuffled**: 0.0397
- **honest_cost_p**: 0.374
- **honest_cost_rho_obs**: 0.0442
- **honest_cost_rho_obs_raw**: -0.0442
- **honest_cost_within_f_std**: 4.468
- **honest_cost_ci_width**: 0.1163
- **honest_cost_effective_distinct_n**: 6
- **honest_cost_n_trajectories**: 401
- **honest_cost_null_FP**: 0.0
- **full_vector_discrimination_full**: 0.7619
- **full_vector_discrimination_body_only**: 0.381
- **full_vector_discrimination_status_only**: 0.0
- **full_vector_discrimination_body_varying**: 1.0
- **full_vector_discrimination_header_varying**: 1.0
- **full_vector_discrimination_null**: 0.0
- **full_vector_discrimination_nginx**: 1.0
- **full_vector_ci_lo**: 0.7048
- **full_vector_ci_hi**: 0.819
- **full_vector_ci_width**: 0.1143
- **full_vector_effective_distinct_n**: 4
- **full_vector_diff_lo**: 0.3143
- **hit_byte_identical**: 330
- **hit_total**: 330
- **hit_rate**: 1.0
- **loopback_header_drift**: 0.9583
- **loopback_body_drift**: 1.0
- **loopback_null_FP**: 0.0

## Validity Notes

- C5 secondary loopback/HIT limitation disclosed but does not downgrade primary SUPPORTS per spec (C1-C4 pass)

## Unresolved
