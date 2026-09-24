# EXP-RUNTIME-36047340781 — H1-SINGLE-NODE-NATURAL-HEADER-REAL-CACHE

**Status:** COMPLETE
**Outcome:** FALSIFIES
**Lane:** runtime
**Claim:** C-MEAS-VALID

## Controls

| V-NGINX-CONFIG-OK | PASS | nginx: the configuration file /tmp/spider-runtime/36044045537/nginx.conf syntax is ok
nginx: configuration file /tmp/spider-runtime/36044045537/nginx.conf test is successful | nginx -t exclusive -c rc=0 no warning no duplicate hash |
| V-SINGLE-HASH | PASS | count=1 | exactly one 'hash $request_uri consistent;' |
| V-CACHE-ENABLED | PASS | proxy_cache_path+proxy_cache+proxy_cache_valid+proxy_temp_path+bypass present | proxy_cache spider_cache active directives |
| NC-CACHE-DISABLED-REJECTED | PASS | provenance proxy_cache_enabled=true | cache ENABLED; disabled would be MEASUREMENT_INVALID |
| NC-SYNTHETIC-MUTATION-ABSENCE | PASS | header-varying probes = real HTTP pairs valid vs expired same body_variant (body bytes asserted identical) | no synthetic header dict mutation; natural valid-vs-expired probes |
| NC-EXCLUSIVE-NGINX | PASS | sudo nginx -c /tmp/spider-runtime/36044045537/nginx.conf; cache ls logged | exclusive nginx -c only; cache enabled perms valid |
| V-FLASK-LISTENING | PASS | socket connect ok | Flask verified listening 127.0.0.1:19860 socket retry 30s |
| V-HEALTH-GATE | PASS | 1 attempts, missing_on_200=0 | 0 missing X-Worker-Pid on 200s |
| V-NGINX-NO-PERMISSION-DENIED | PASS | nginx_error.log clean | 0 Permission denied (proxy_temp_path fix) |
| C1-FRESHNESS-NON304 | PASS | n_non304=850 per_ep={'/api/profile': 430, '/api/data_list': 420} hs_rate=1.0 batch=25 missing=0 | n_non304>=800 stratified 400/endpoint hs>=0.90 batch>=10 0 missing |
| C2-ORTHOGONALITY | FAIL | r_sched=0.0353 V=0.1155 mean_j=0.3845 var_j=0.027922 std_j=0.1671 drift_mean=0.2857 no_drift_mean=0.6667 nullFP=1.0000 n=540 | |r_sched|<0.30 V<0.30 variance>0 std>0 mean<1.0 nullFP<=0.05 de-confounded |
| C3-HONEST-COST | PASS | |rho_shuffled|=0.0351 p=0.4730 rho_obs=0.0313 std=3.1814 width=0.1028 eff=6 nullFP=0.0000 | |rho_shuffled|<0.20 p>=0.20 within-f std>0 width>0 effective>1 nullFP<=0.05 integer sums |
| C4-FULL-VECTOR | FAIL | full=1.0000 body=0.3810 status=0.0000 bodyVar=1.0000 hdrVar=1.0000 bodyHdr=0.0000 statusHdr=0.0000 width=0.0000 eff=341 diff_lo=0.5524 null=1.0000 nginx=1.0000 | full>0.5 full>max(body,status)+0.05 width>0 eff>1 diff_lo>0 nullFP<=0.05 via NATURAL headers |
| C5-LOOPBACK-HIT-CACHE | FAIL | header=1.0000 body=1.0000 nullFP=1.0000 HIT=330/330 x_cache_all_HIT=True cache_files=0 | 2x header drift 1.0 body drift 1.0 nullFP<=0.05 HIT 330/330 via REAL nginx cache greedy byte-identical |
| PC-304-REAL | PASS | n_non304=850 hs=1.0 missing=0 | n_non304>=800 hs>=0.90 0 missing shared WAL |
| PC-HEADER-NATURAL-VAR | FAIL | var_j=0.027922 std_j=0.1671 mean_j=0.3845 drift_mean=0.2857 no_drift_mean=0.6667 | headers depend on auth state; Jaccard variance>0 std>0 mean<1.0 drift<1.0 |
| PC-HONEST-COST-SANITY | PASS | |rho|=0.0351 p=0.4730 | |rho_shuffled|<0.20 p>=0.20 integer sums block perm B=1000 |
| PC-FULL-VECTOR-NATURAL | FAIL | full=1.0000 hdrVar=1.0000 width=0.0000 | full>0.5 non-degenerate via natural headers |
| PC-HIT-NGINX-CACHE | FAIL | HIT=330/330 warm=HIT cache_files=0 | HIT 330/330 via real nginx proxy_cache greedy MAX_DEPTH5 byte-identical |
| PC-LOOPBACK-2X-STICKY | FAIL | header=1.0000 body=1.0000 | drift 1.0 nullFP<=0.05 |
| B-FULL-VECTOR | FAIL | full=1.0000 lo=1.0000 hi=1.0000 | full>0.5 full>max+0.05 non-degenerate |
| B-BODY-ONLY | PASS | body_only=0.3810 bodyVar=1.0000 hdrVar=0.0000 | 1.0 body-varying 0.0 body-identical header-only |
| B-STATUS-ONLY | PASS | status_only=0.0000 statusHdr=0.0000 | 0.0 (200-vs-200 body-only and natural header-only) |
| B-HEADER-ONLY-JACCARD | FAIL | r_sched=0.0353 V=0.1155 mean_j=0.3845 var_j=0.027922 | |r_sched|<0.30 V<0.30 variance>0 mean<1.0 |
| B-HEADER-HASH-REJECTED | PASS | filtered headers minus body-derived only; set-cookie/vary/cache-control preserved | hash surrogate never used; MINUS filter preserves Cache-Control/Set-Cookie/Vary |
| B-COST-SHUFFLED | PASS | |rho_shuffled|=0.0351 p=0.4730 n_traj=500 | |rho|<0.20 p>=0.20 block-permuted trajectory_id B=1000 integer sums |
| B-HEADERS-NO-BODYDERIVED | PASS | bodyVar bodyOnly=1.0000 hdrVar bodyOnly=0.0000 hdrVar full=1.0000 | 0.0 body-only on AvsC same-auth; >0.5 natural header-only AvsE same body |
| NC-ORTHOGONALITY-NOISE | FAIL | no_drift_mean=0.6667 nullFP=1.0000 | noise-only same-state Jaccard mean 1.0 FP<=0.05 |
| NC-COST-SHUFFLED | PASS | |rho|=0.0351 p=0.4730 | |rho_shuffled|<0.20 p>=0.20 |
| NC-BROWSER-SAME-STATE-ANALOG | FAIL | null_full=1.0000 | same-state null full 0.0 CI contains 0 |
| NC-LOOPBACK-NULL | FAIL | loopback_nullFP=1.0000 | same-state 2x loopback 0.0 drift FP<=0.05 |
| NC-HIT-NULL | PASS | HIT=330/330 all byte-identical after greedy | cache body identical to origin (greedy compare) |
| NC-FACTORY-REGRESSION | PASS | wsgi.py inserts sys.path Path(__file__).parent then imports create_app | factory create_app + wsgi sys.path parent; dir before DB |
| V-RECOMPUTE-MISMATCHES | PASS | mismatches=0 | 0 mismatches recompute vs recorded |

## Metrics

- **freshness_n_total**: 993
- **freshness_n_non304**: 850
- **freshness_n_304**: 143
- **freshness_n_missing_worker**: 0
- **freshness_hs256_valid_success_rate**: 1.0
- **freshness_batch_distinct_ts**: 25
- **freshness_per_ep_non304**: {'/api/profile': 430, '/api/data_list': 420}
- **freshness_per_ep_304**: {'/api/profile': 67, '/api/data_list': 76}
- **freshness_scheduling_confound_r**: 0.0353
- **freshness_scheduling_r_raw**: 0.0353
- **freshness_scheduling_p**: 0.413426
- **freshness_scheduling_ci_lo**: -0.0493
- **freshness_scheduling_ci_hi**: 0.1193
- **freshness_cramers_v**: 0.1155
- **freshness_header_only_jaccard_mean**: 0.3845
- **freshness_header_only_variance**: 0.027922
- **freshness_header_only_std**: 0.1671
- **freshness_header_only_jaccard_drift_mean**: 0.2857
- **freshness_header_only_jaccard_no_drift_mean**: 0.6667
- **freshness_header_only_jaccard_r_vs_drift_info**: -1.0
- **freshness_header_only_pairs_n**: 540
- **freshness_header_only_null_FP**: 1.0
- **freshness_scheduling_confound_r_freshness**: 0.0229
- **honest_cost_rho_shuffled**: 0.0351
- **honest_cost_p**: 0.473
- **honest_cost_rho_obs**: 0.0313
- **honest_cost_rho_obs_raw**: -0.0313
- **honest_cost_within_f_std**: 3.1814
- **honest_cost_ci_width**: 0.1028
- **honest_cost_effective_distinct_n**: 6
- **honest_cost_n_trajectories**: 500
- **honest_cost_null_FP**: 0.0
- **full_vector_discrimination_full**: 1.0
- **full_vector_discrimination_body_only**: 0.381
- **full_vector_discrimination_status_only**: 0.0
- **full_vector_discrimination_body_varying**: 1.0
- **full_vector_discrimination_header_varying**: 1.0
- **full_vector_discrimination_null**: 1.0
- **full_vector_discrimination_nginx**: 1.0
- **full_vector_body_body_varying**: 1.0
- **full_vector_body_header_varying**: 0.0
- **full_vector_status_header_varying**: 0.0
- **full_vector_ci_lo**: 1.0
- **full_vector_ci_hi**: 1.0
- **full_vector_ci_width**: 0.0
- **full_vector_effective_distinct_n**: 341
- **full_vector_diff_lo**: 0.5524
- **full_vector_n_pairs**: 210
- **hit_byte_identical**: 330
- **hit_total**: 330
- **hit_rate**: 1.0
- **hit_warm_cache_status**: HIT
- **hit_warm_ok**: False
- **hit_all_via_cache_HIT**: True
- **hit_nginx_cache_files**: 0
- **loopback_header_drift**: 1.0
- **loopback_body_drift**: 1.0
- **loopback_null_FP**: 1.0
- **loopback_full_vector_header_varying**: 1.0
- **loopback_drift_jaccard_mean**: 0.2857
- **recompute_mismatches**: 0

## Validity Notes

- sudo available: nginx master started as root with user www-data workers; cache/temp dirs chowned www-data (frozen spec www-data perms).
- FALSIFIED-IN-SETTING conditions failed: ['C2', 'C4'] with validity passing

## Unresolved
