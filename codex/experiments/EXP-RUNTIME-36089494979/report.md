# EXP-RUNTIME-36089494979 — H1-STABLE-HEADER-SINGLE-NODE-SCOPED

**Status:** COMPLETE
**Outcome:** SUPPORTS
**Lane:** runtime
**Claim:** C-MEAS-VALID

## Controls

| V-SCOPED-UUID-CHECK | PASS | naive_uuid_count=96 scoped_uuid_count=0 scoped_block_lines=154 ast_uuid_refs=[] import_uuid_absent=True hmac_present=True | scoped uuid count in executable create_app block ==0; import uuid absent; hmac.new present |
| V-NGINX-CONFIG-OK | PASS | nginx: the configuration file /tmp/spider-runtime/36044045537/nginx.conf syntax is ok
nginx: configuration file /tmp/spider-runtime/36044045537/nginx.conf test is successful | nginx -t exclusive -c rc=0 no warning no duplicate hash |
| V-SINGLE-HASH | PASS | count=1 | exactly one 'hash $request_uri consistent;' |
| V-CACHE-ENABLED | PASS | proxy_cache_path+proxy_cache+proxy_cache_valid+proxy_temp_path+bypass present | proxy_cache spider_cache active |
| NC-CACHE-DISABLED-REJECTED | PASS | provenance proxy_cache_enabled=true | cache ENABLED; disabled would be MEASUREMENT_INVALID |
| NC-SYNTHETIC-MUTATION-ABSENCE | PASS | Set-Cookie = HMAC(TESTBED_SECRET, auth_state)[:16]; no uuid.uuid4() in code | no uuid4 per-response nonce; grep uuid absent |
| NC-EXCLUSIVE-NGINX | PASS | sudo nginx -c /tmp/spider-runtime/36044045537/nginx.conf; cache ls logged | exclusive nginx -c only; cache enabled perms valid |
| V-FLASK-LISTENING | PASS | socket connect ok | Flask verified listening 127.0.0.1:19860 socket retry 30s |
| V-HEALTH-GATE | PASS | 1 attempts, missing_on_200=0 | 0 missing X-Worker-Pid on 200s |
| V-NGINX-NO-PERMISSION-DENIED | PASS | nginx_error.log clean | 0 Permission denied |
| B-HEADER-NAME-ONLY | PASS | name_mean=0.8519 name_var=0.007696 name_std=0.0877 name_drift_mean=0.8000 name_no_drift_mean=1.0000 nullFP=0.0000 | nullFP<=0.05 variance>0 diagnostic; drift separation may be lower than value-stable Jaccard; not primary falsifier |
| V-SAME-STATE-J | PASS | same_state_J=1.0000 | same-state Jaccard J==1.0 (stable headers identical) |
| C1-FRESHNESS-NON304 | PASS | n_non304=850 per_ep={'/api/profile': 430, '/api/data_list': 420} hs_rate=1.0 batch=25 missing=0 | n_non304>=800 stratified 400/endpoint hs>=0.90 batch>=10 0 missing |
| C2-ORTHOGONALITY | PASS | r_sched=0.0353 V=0.1155 mean_j=0.4709 var_j=0.098163 std_j=0.3133 drift_mean=0.2857 no_drift_mean=1.0000 nullFP=0.0000 same_state_J=1.0000 n=540 | |r_sched|<0.30 V<0.30 variance>0 std>0 mean<1.0 nullFP<=0.05 de-confounded same-state J==1.0 |
| C3-HONEST-COST | PASS | |rho_shuffled|=0.0351 p=0.4730 rho_obs=0.0313 std=3.1814 width=0.1028 eff=6 nullFP=0.0000 | |rho_shuffled|<0.20 p>=0.20 within-f std>0 width>0 effective>1 nullFP<=0.05 integer sums |
| C4-FULL-VECTOR | PASS | full=0.7619 body=0.3810 status=0.0000 bodyVar=1.0000 hdrVar=1.0000 bodyHdr=0.0000 statusHdr=0.0000 width=0.1143 eff=4 diff_lo=0.3190 null=0.0000 nginx=1.0000 | full>0.5 full>max(body,status)+0.05 width>0 eff>1 diff_lo>0 nullFP<=0.05 via STABLE headers |
| C5-LOOPBACK-HIT-CACHE | PASS | header=1.0000 body=1.0000 nullFP=0.0000 HIT=330/330 x_cache_all_HIT=True cache_files=1 | 2x header drift 1.0 body drift 1.0 nullFP<=0.05 HIT 330/330 via REAL nginx cache greedy byte-identical |
| PC-304-REAL-STABLE | PASS | n_non304=850 hs=1.0 missing=0 | n_non304>=800 hs>=0.90 0 missing shared WAL stable Set-Cookie |
| PC-HEADER-STABLE-VAR | PASS | var_j=0.098163 std_j=0.3133 mean_j=0.4709 same_state_J=1.0000 | headers depend on auth state via stable HMAC; Jaccard variance>0 std>0 mean<1.0 same-state J==1.0 |
| PC-HONEST-COST-SANITY | PASS | |rho|=0.0351 p=0.4730 | |rho_shuffled|<0.20 p>=0.20 integer sums block perm B=1000 |
| PC-FULL-VECTOR-STABLE | PASS | full=0.7619 hdrVar=1.0000 width=0.1143 | full>0.5 non-degenerate via stable headers |
| PC-LOOPBACK-2X-STICKY-STABLE | PASS | header=1.0000 body=1.0000 | drift 1.0 nullFP<=0.05 with stable headers |
| PC-HIT-NGINX-CACHE | PASS | HIT=330/330 warm=EXPIRED warm_ok=False cache_files=1 | HIT 330/330 via real nginx proxy_cache greedy MAX_DEPTH5 byte-identical |
| B-FULL-VECTOR | PASS | full=0.7619 lo=0.7048 hi=0.8190 | full>0.5 full>max+0.05 non-degenerate |
| B-BODY-ONLY | PASS | body_only=0.3810 bodyVar=1.0000 hdrVar=0.0000 | 1.0 body-varying 0.0 body-identical stable-header-varying |
| B-STATUS-ONLY | PASS | status_only=0.0000 statusHdr=0.0000 | 0.0 (200-vs-200 body-only and stable-header-only) |
| B-HEADER-ONLY-JACCARD-STABLE | PASS | r_sched=0.0353 V=0.1155 mean_j=0.4709 var_j=0.098163 same_state_J=1.0000 | |r_sched|<0.30 V<0.30 variance>0 mean<1.0 same-state J==1.0 |
| B-HEADER-HASH-REJECTED | PASS | filtered headers minus body-derived only; stable Set-Cookie via HMAC | hash surrogate never used; MINUS filter preserves Cache-Control/Set-Cookie/Vary |
| B-COST-SHUFFLED | PASS | |rho|=0.0351 p=0.4730 | |rho_shuffled|<0.20 p>=0.20 |
| B-HEADERS-NO-BODYDERIVED-STABLE | PASS | bodyVar bodyOnly=1.0000 hdrVar bodyOnly=0.0000 hdrVar full=1.0000 | 0.0 body-only same-auth; >0.5 stable-header-only valid vs expired same body |
| NC-ORTHOGONALITY-NOISE-STABLE | PASS | no_drift_mean=1.0000 same_state_J=1.0000 nullFP=0.0000 | noise-only same-state Jaccard mean 1.0 FP<=0.05 |
| NC-COST-SHUFFLED | PASS | |rho|=0.0351 p=0.4730 | |rho_shuffled|<0.20 p>=0.20 |
| NC-BROWSER-SAME-STATE-ANALOG-STABLE | PASS | null_full=0.0000 | same-state null full 0.0 CI contains 0 |
| NC-LOOPBACK-NULL-STABLE | PASS | loopback_nullFP=0.0000 | same-state 2x loopback 0.0 drift FP<=0.05 |
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
- **freshness_header_only_jaccard_mean**: 0.4709
- **freshness_header_only_variance**: 0.098163
- **freshness_header_only_std**: 0.3133
- **freshness_header_only_jaccard_drift_mean**: 0.2857
- **freshness_header_only_jaccard_no_drift_mean**: 1.0
- **freshness_header_only_jaccard_r_vs_drift_info**: -1.0
- **freshness_header_only_pairs_n**: 540
- **freshness_header_only_null_FP**: 0.0
- **freshness_same_state_j**: 1.0
- **header_name_only_jaccard_mean**: 0.8519
- **header_name_only_variance**: 0.007696
- **header_name_only_std**: 0.0877
- **header_name_only_drift_mean**: 0.8
- **header_name_only_no_drift_mean**: 1.0
- **header_name_only_null_FP**: 0.0
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
- **full_vector_discrimination_full**: 0.7619
- **full_vector_discrimination_body_only**: 0.381
- **full_vector_discrimination_status_only**: 0.0
- **full_vector_discrimination_body_varying**: 1.0
- **full_vector_discrimination_header_varying**: 1.0
- **full_vector_discrimination_null**: 0.0
- **full_vector_discrimination_nginx**: 1.0
- **full_vector_body_body_varying**: 1.0
- **full_vector_body_header_varying**: 0.0
- **full_vector_status_header_varying**: 0.0
- **full_vector_body_varying_ci_lo**: 1.0
- **full_vector_body_varying_ci_hi**: 1.0
- **full_vector_body_varying_ci_width**: 0.0
- **full_vector_body_varying_effective_distinct_n**: 2
- **full_vector_header_varying_ci_lo**: 1.0
- **full_vector_header_varying_ci_hi**: 1.0
- **full_vector_header_varying_ci_width**: 0.0
- **full_vector_header_varying_effective_distinct_n**: 2
- **full_vector_ci_lo**: 0.7048
- **full_vector_ci_hi**: 0.819
- **full_vector_ci_width**: 0.1143
- **full_vector_effective_distinct_n**: 4
- **full_vector_diff_lo**: 0.319
- **full_vector_n_pairs**: 210
- **hit_byte_identical**: 330
- **hit_total**: 330
- **hit_rate**: 1.0
- **hit_warm_cache_status**: EXPIRED
- **hit_warm_ok**: False
- **hit_all_via_cache_HIT**: True
- **hit_nginx_cache_files**: 1
- **hit_nginx_cache_entries**: ['/tmp/spider-runtime/36044045537/cache/2/05/febd9bd9f76478774376fc8d7baa5052']
- **loopback_header_drift**: 1.0
- **loopback_body_drift**: 1.0
- **loopback_null_FP**: 0.0
- **loopback_full_vector_header_varying**: 1.0
- **loopback_drift_jaccard_mean**: 0.2857
- **recompute_mismatches**: 0

## Validity Notes

- sudo available: nginx master started as root with user www-data workers; cache/temp dirs chowned www-data.
- STABLE_HEADER_GENERATION_VERIFIED: Set-Cookie = HMAC-SHA256(TESTBED_SECRET, auth_state)[:16]; scoped uuid-absence grep verified (executable create_app block uuid count 0, import uuid absent, docstring 7 historical matches excluded); same valid auth state always produces identical Set-Cookie token.
- HEADER-SIGNAL-DIRECTION: header-only Jaccard separates drift from no-drift in-sample (drift_mean vs no_drift_mean, r(J,drift_label) negative) proving headers respond to auth state; the question is whether stable representation achieves nullFP<=0.05.
- Same-state Jaccard J==1.0 check: same-auth same body_variant pairs produce J=1.0000 (target exactly 1.0) — stable Set-Cookie ensures identical headers for same auth state.
- B-HEADER-NAME-ONLY diagnostic: name-only Jaccard mean=0.8519 var=0.007696 drift_mean=0.8000 no_drift_mean=1.0000 nullFP=0.0000 (diagnostic not primary gating).
- All primary C1-C4 plus gating C5 (loopback 2x drift 1.0 + HIT 330/330 via REAL nginx cache) pass — STABLE-HEADER single-node honesty gate restored!

## Interpretation

Stable-header representation: uuid4 per-response nonce replaced with deterministic HMAC-SHA256(TESTBED_SECRET, auth_state)[:16] token. Same auth state produces identical Set-Cookie, ensuring same-state Jaccard == 1.0. Header-only Jaccard and full-vector fingerprints computed on stable headers MINUS {Content-Length,ETag,W-ETag,Range} lowercased sorted keys preserving natural Cache-Control/Vary/stable Set-Cookie token.

## Unresolved
