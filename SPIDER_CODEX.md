# SPIDER CODEX — Research 2.0

Pre-2.0 canonical memory remains frozen at `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md`.

Canonical Research 2.0 evidence lives in `codex/experiments/<experiment_id>/`.
Use `codex/index.json` and `codex/claim_state.json` to locate relevant packets; do not load all experiment bodies by default.
Validated experiments: **101**. Coverage gaps: **0**. Quarantined packets: **0**.

## Experiment index

| Experiment | Lane | Audit | Verdict | Claims | Source commit |
|---|---|---|---|---|---|
| EXP-PRODUCT-33528829801 | product | PASS | SURVIVES — C-PARAM-INHERIT survives at synthetic in-kernel POC level: distill_parameterized() with _extract_varying_values() correctly induces one parameter slot for isomorphic action paths and resolves to EXECUTABLE with correct bound_action for all 10 unseen single-char identifiers. All four frozen decision-rule conditions satisfied. Audit PASS confirms recomputed metrics match producer. However, the claim ceiling is narrow: single-parameter, single-field, common-prefix heuristic, deterministic synthetic data, hardcoded confidence, simulated baselines. No broader product promotion is authorized by this evidence. | C-PARAM-INHERIT | `fb05ae4d41a0` |
| EXP-FRONTIER-33528827909 | frontier | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `9cf80f63bd0f` |
| EXP-PHYSICS-33528829431 | physics | REVISE | REVISE | C-MEAS-VALID, C-WEB-DYNAMICS | `0cef5908fade` |
| EXP-RUNTIME-33528830833 | runtime | REVISE | NARROW_SUCCESS | C-MEAS-VALID | `f6949358832f` |
| EXP-INTEL-33528832113 | intel | REVISE | SUPPORTS | C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON | `14d124a7e652` |
| EXP-GRAPH-33528827169 | graph | FAIL | PARAM-INHERIT-SUBSTRATE-BROKEN | C-PARAM-INHERIT | `c72fbcd7da6a` |
| EXP-GRAPH-33718012817 | graph | REVISE | COMPETITION-UNSAFE | C-PARAM-INHERIT | `bd318921b4ff` |
| EXP-PRODUCT-33741671686 | product | PASS | MULTI-PARAM-SURVIVES — the frozen decision rule passes all 7 checks: C1 regression (slot≥1, resolution=1.0, binding=1.0), C2 multi-param (slot=2, distinct, resolution=1.0, binding=1.0), C3 three-param (slot=3, distinct, resolution=1.0, binding=1.0), C4 non-identifier (slot=1, resolution=1.0, binding=1.0), C5 no-collision (slot=2, distinct, resolution=1.0, binding=1.0), null_control passed, no crashes. Producer metrics verified: 21/21 EXECUTABLE, 21/21 binding correct, 0/21 unsubstituted templates. Audit PASS confirms all recomputed metrics match producer. However, the claim ceiling remains narrow: synthetic POC implemented only in run_experiment.py (not in kernel.py), single-intent deterministic observations, trivial full-replacement parameterization for body fields, tautological confidence gate (0.8 == min_confidence 0.8), null control passes via intent mismatch not pattern absence, fragile positional slot-to-param mapping in harness. Do NOT promote to Product Core. | C-PARAM-INHERIT | `b99b379f508a` |
| EXP-FRONTIER-33767130362 | frontier | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `f48d8baf8331` |
| EXP-RUNTIME-33767375933 | runtime | REVISE | NARROW_SUCCESS | C-MEAS-VALID | `a6698de64a40` |
| EXP-PHYSICS-33788037373 | physics | FAIL | MEASUREMENT_INVALID | C-MEAS-VALID, C-WEB-DYNAMICS | `0d00d3abac08` |
| EXP-RUNTIME-33805283356 | runtime | REVISE | NARROW_SUCCESS | C-MEAS-VALID | `f48f1ad99f34` |
| EXP-GRAPH-33816735314 | graph | PASS | COMPETITION-SAFE | C-PARAM-INHERIT | `db32eb7948b0` |
| EXP-INTEL-33842055594 | intel | REVISE | PARTIALLY_COMPATIBLE | C-CROSSSITE, C-LLM-INHERIT | `957181df06b1` |
| EXP-FRONTIER-33863640568 | frontier | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `dca0b76bab7b` |
| EXP-RUNTIME-33902315583 | runtime | PASS | C-MEAS-VALID survives narrowly on real Flask/JWT middleware within tested scope. Full-vector discrimination 0.833 > 0.5, null FP 0.0% < 5%, valid vs expired discriminable Jaccard 0.3505 < 0.5. All three decision criteria pass. Full vector equals B-BODY-ONLY (0.833 = 0.833) — standard headers add no independent discriminating information; body is the dominant signal. Parent gaps V1-REAL-MIDDLEWARE-GAP and V2-SYNTHETIC-HEADER-TAUTOLOGY closed. Claim ceiling bounded to Flask 3.1.3 + PyJWT 2.13.0 HS256, localhost, 4 states, no synthetic headers, standard headers only, jitter 50-150ms, N=40. | C-MEAS-VALID | `24969f18d2ae` |
| EXP-INTEL-33925056324 | intel | REVISE | SUPPORTS | C-CROSSSITE, C-LLM-INHERIT | `8a494724d6cc` |
| EXP-FRONTIER-33932275169 | frontier | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `d4353fcba3d3` |
| EXP-INTEL-33945226776 | intel | REVISE | MIXED | C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON | `8f2ef00975df` |
| EXP-GRAPH-33955869291 | graph | REVISE | SCOPE-LIMITED | C-PARAM-INHERIT | `6c7df8c31f4a` |
| EXP-PHYSICS-33965269281 | physics | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-MEAS-VALID, C-WEB-DYNAMICS | `c1a660af6363` |
| EXP-PRODUCT-33974562602 | product | PASS | KERNEL-INTEGRATION-FALSIFIED | C-PARAM-INHERIT | `bcbc236d4ad4` |
| EXP-PRODUCT-33993747223 | product | PASS | FIXES-FALSIFIED | C-PARAM-INHERIT | `44d59cfed64d` |
| EXP-GRAPH-33998605047 | graph | REVISE | PARTIAL_VALIDATION | C-PARAM-INHERIT | `a208512f8901` |
| EXP-PRODUCT-34003641840 | product | REVISE | FIXES-FALSIFIED | C-PARAM-INHERIT | `740204b76ecc` |
| EXP-RUNTIME-34015740602 | runtime | REVISE | CONSTRAINED — C-MEAS-VALID survives narrowly. All three mandatory decision criteria pass (full-vector discrimination 1.0 > 0.5, null FP 0.0% < 5%, valid vs expired Jaccard 0.328 < 0.5). However, the producer's claim ceiling is overgeneralized: claim extends only to Flask 3.1.3 + PyJWT 2.13.0 HS256 on localhost 127.0.0.1:18928 with 4 states returning distinct bodies, headers filtered (Date/Server/X-Request-Id excluded), Cache-Control no-store/no-cache, ETag W/body_sha, Set-Cookie session only for valid_token, jitter 50-150ms uniform, N=40 seed 44, Python 3.12.14. The exploratory H4 test (full vector > B-BODY-ONLY) is INCONCLUSIVE due to ceiling effect: with all 4 bodies distinct, discrimination is at 1.0 and headers cannot improve beyond perfect. Full vector = B-BODY-ONLY (1.0 = 1.0) reflects body dominance under distinct-body design, not proof headers are non-discriminative. The bootstrap CI [1.0, 1.0] is degenerate at ceiling (uninformative, not high-precision). ETag and Content-Length are body-correlated by construction. Only Cache-Control and Set-Cookie are state-varying independent headers; each achieves 0.5 discrimination alone but is redundant when bodies already separate. | C-MEAS-VALID | `abca81f5a5ca` |
| EXP-PRODUCT-34015741916 | product | FAIL | KERNEL-INTEGRATION-PARTIAL | C-PARAM-INHERIT | `74256fb86a51` |
| EXP-FRONTIER-34029326102 | frontier | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `22ccea04903a` |
| EXP-PHYSICS-34038570933 | physics | FAIL | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `1504ba88ec66` |
| EXP-INTEL-34047713704 | intel | BLOCKED | BLOCKED | C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON | `c621fb1ed4a3` |
| EXP-RUNTIME-34054515149 | runtime | PASS | SURVIVES_CURRENT_TEST — C-MEAS-VALID survives narrowly. All four frozen decision criteria pass: full_vector_discrimination 1.0 > B-BODY-ONLY 0.833 (incremental header value 0.167), full_vector_discrimination 1.0 > 0.5, null FP 0.0% < 5%, Cache-Control-only discrimination 0.833 > 0. The parent H4 ceiling confound (V3-DISTINCT-BODY-CEILING-CONFOUND) is resolved: when expired_token and invalid_token share identical bodies, Cache-Control no-store vs no-cache provides the discriminating signal that body-only cannot capture, lifting full vector from 0.833 to 1.0. Audit V4 (ENGINEERED-HEADER-TAUTOLOGY-CONSTRAINT, medium severity) constrains the claim ceiling: incremental header value is by construction (application-set Cache-Control/Set-Cookie per auth state in Flask middleware), not discovery of natural production header variance. Claim extends only to Flask 3.1.3 + PyJWT 2.13.0 HS256 on localhost 127.0.0.1:18929, 4 states (no_auth 401 login_required body ae00c5, valid_token 200 alice_profile body 65d603 with Set-Cookie session, expired_token 401 auth_failed body a138b3 Cache-Control no-store, invalid_token 401 auth_failed body a138b3 identical to expired Cache-Control no-cache), headers after Date/Server/X-Request-Id exclusion, deterministic SHA-256(repr((status, tuple(sorted(filtered_headers.items())), body_sha256, ''))) on Python 3.12.14, N=40 (4x10 seed 44) server jitter 50-150ms uniform client 0-200ms. Does NOT extend to production OAuth/OIDC (Auth0/Okta/Keycloak), CDN/caching, load-balancer, rate-limit, compression, jitter >150ms, or natural (non-application-set) header variance. Product architecture recommendation to use full vector is supported only within this synthetic Flask localhost pattern where headers are application-set per state. | C-MEAS-VALID | `2ab22ff1c2fe` |
| EXP-FRONTIER-34061241004 | frontier | REVISE | SURVIVES_CURRENT_TEST | C-WEB-DYNAMICS | `8ae9ddc8f202` |
| EXP-FRONTIER-34065969836 | frontier | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `be11b0bfedbf` |
| EXP-PHYSICS-34071626363 | physics | PASS | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `a4c9a3e22d34` |
| EXP-FRONTIER-34121473072 | frontier | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `111951aeb5f0` |
| EXP-PHYSICS-34149195420 | physics | REVISE | SURVIVES_CURRENT_TEST | C-WEB-DYNAMICS | `fcec93130c8d` |
| EXP-GRAPH-34170139507 | graph | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-PARAM-INHERIT | `b727aee7b058` |
| EXP-GRAPH-34176416673 | graph | PASS | BLOCKED | C-PARAM-INHERIT | `ca57376ba74b` |
| EXP-PRODUCT-34195008089 | product | PASS | C2-FIX-FALSIFIED | C-PARAM-INHERIT | `b6a0886e3675` |
| EXP-GRAPH-34222171093 | graph | PASS | BLOCKED | C-PARAM-INHERIT | `00bf4dd51b80` |
| EXP-GRAPH-34244445713 | graph | PASS | BLOCKED | C-PARAM-INHERIT | `df9af4b6b730` |
| EXP-PHYSICS-34266105229 | physics | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `a23db9347a32` |
| EXP-PRODUCT-34282620394 | product | FAIL | C2-FIX-FALSIFIED | C-PARAM-INHERIT | `d04d236205ae` |
| EXP-GRAPH-34291967676 | graph | PASS | BLOCKED | C-PARAM-INHERIT | `968991590c03` |
| EXP-RUNTIME-34300004597 | runtime | REVISE | SURVIVES_CURRENT_TEST — C-MEAS-VALID survives with severely narrowed ceiling. All four frozen decision criteria pass: full_vector_discrimination 0.833 > B-BODY-ONLY 0.5 (incremental header value 0.333), full_vector_discrimination 0.833 > 0.5, null FP 0.0% < 5%, Cache-Control-only discrimination 0.5 > 0. However, the audit corrects the producer's mechanistic interpretation: (1) Cache-Control variation is valid_token no-cache vs absent on ALL errors — it does NOT vary by error type (no-store vs no-cache as hypothesized), confirming V4 ENGINEERED-HEADER-TAUTOLOGY for the critical expired/invalid pair; (2) the true discriminating header is WWW-Authenticate (discrimination 0.833 == full vector), not Cache-Control; (3) Set-Cookie adds zero (absent on all Keycloak /userinfo responses); (4) expired_token and invalid_token remain indistinguishable (identical bodies, headers, fingerprint, Jaccard 1.0); (5) body baseline weakened (B-BODY-ONLY 0.5 vs parent 0.833) inflates apparent incremental value; (6) expired token is not truly Keycloak-issued (V6 state construction leakage). Claim ceiling bounded to Keycloak 25.0 start-dev localhost:18080 /userinfo, 3 distinct fingerprints (not 4), full vector via WWW-Authenticate not Cache-Control error-type variation. Does NOT extend to production OAuth/OIDC, CDN/load-balancer, /token endpoint, or cross-Python-version reproducibility. | C-MEAS-VALID | `2a6b3b8a0f5f` |
| EXP-GRAPH-34320613096 | graph | PASS | BLOCKED | C-PARAM-INHERIT | `d742b1d9d82f` |
| EXP-PHYSICS-34348438464 | physics | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `e45dabebba74` |
| EXP-INTEL-34377576886 | intel | REVISE | REVISE | C-CROSSSITE, C-LLM-INHERIT, C-PRODUCT-ECON | `3b2e25ab8793` |
| EXP-GRAPH-34395286092 | graph | PASS | BLOCKED_CLOSE_AND_PIVOT | C-PARAM-INHERIT | `34848357b257` |
| EXP-GRAPH-34409639346 | graph | PASS | SUPPORTED | C-SEMANTIC-RESOLVE | `6c64f4717052` |
| EXP-PRODUCT-34420092879 | product | REVISE | SURVIVES_CURRENT_TEST | C-PARAM-INHERIT | `21e440173068` |
| EXP-RUNTIME-34439061845 | runtime | PASS | FALSIFIED-IN-SETTING — WWW-Authenticate header discrimination does NOT transfer across Keycloak endpoints. Frozen decision rule fails on both primary conditions: (1) WWW-Auth-only discrimination > 0 on >= 2/3 additional endpoints: 0/3 positive (/token password 0.0, /token client_credentials 0.0, /introspect 0.0); (2) full-vector discrimination > 0.5 on >= 2/3 additional endpoints: 0/3 positive (/token password 0.0, /token client_credentials 0.0, /introspect 0.5 not > 0.5). Positive control PASS (/userinfo WWW-Auth 0.833 == full vector, replicates parent EXP-RUNTIME-34300004597). Null FP PASS on 3/4 endpoints (100% on /token password is structural: fresh JWT per request, not measurement instability). Audit PASS, all metrics recomputed match producer. WWW-Authenticate header is absent from all /token and /introspect responses across all 120 reps of additional endpoints — this is expected OAuth behavior (credentials in form body, not Authorization header), not a measurement gap. The discrimination pattern is /userinfo-specific resource-server behavior, not Keycloak-level. /token endpoints ignore Authorization header entirely. /introspect achieves body-only discrimination 0.5 via active:true/false field. client_credentials test is degenerate (serviceAccountsEnabled false on spider-client, all 401 unauthorized_client); claim ceiling excludes this endpoint as informative transfer test. | C-MEAS-VALID | `32eced076e48` |
| EXP-PRODUCT-34485517221 | product | REVISE | FALSIFIED-IN-SETTING | C-PARAM-INHERIT | `f3fee46cab94` |
| EXP-RUNTIME-34509593940 | runtime | PASS | SURVIVES_CURRENT_TEST | C-MEAS-VALID | `6db3260c944a` |
| EXP-PHYSICS-34524411213 | physics | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `ad803c5168c0` |
| EXP-FRONTIER-34538185726 | frontier | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `ca9884ed23d6` |
| EXP-INTEL-34546944360 | intel | REVISE | MIXED | C-CROSSSITE, C-LLM-INHERIT | `e79ae260a5b5` |
| EXP-GRAPH-34586318405 | graph | REVISE | MIXED — H1 supported: kernel is deterministic exact-intent matcher (L97) with no URL template analysis, confirmed for complex aliasing types (query-param, path-rewriting, server-side routing) at equal confidence 0.9, n=6 aliased-first conditions (0/6 correct, binomial p=0.016). H2 falsified-in-setting: HTTP status-code grounding provides zero autonomous signal on jsonplaceholder.typicode.com (0/12 status differences across 12 aliased conditions; substrate returns 200 for malformed templates like /posts?id=1/comments). Body-based grounding is an exploratory non-autonomous finding (4/4 body differences in asymmetric scenarios B and C, but requires external oracle to determine correctness, produces false positives for equivalent templates in A and F). Experiment does not meet SURVIVES_CURRENT_TEST per frozen decision rule condition (4): for asymmetric scenarios B and C, HTTP execution per frozen status-code definition correctly identifies valid template in 0/4 cases, not 100%. | C-SEMANTIC-RESOLVE | `0fc2196920ae` |
| EXP-INTEL-34607693437 | intel | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-CROSSSITE, C-LLM-INHERIT | `0fa3c79845ae` |
| EXP-PHYSICS-34629310987 | physics | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `1eae61c57d53` |
| EXP-PRODUCT-34642376433 | product | REVISE | FALSIFIED-IN-SETTING | C-PARAM-INHERIT | `44f665985435` |
| EXP-RUNTIME-34654566605 | runtime | REVISE | SURVIVES_CURRENT_TEST | C-MEAS-VALID | `9f154d278099` |
| EXP-PRODUCT-34662221249 | product | REVISE | SURVIVES_CURRENT_TEST | C-PARAM-INHERIT | `60981e36e570` |
| EXP-PHYSICS-34674671762 | physics | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `df5a7fd2f905` |
| EXP-PRODUCT-34685457833 | product | PASS | SURVIVES_CURRENT_TEST | C-PARAM-INHERIT | `359a1644d1ba` |
| EXP-PHYSICS-34695057869 | physics | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `4ce4954fbfec` |
| EXP-PRODUCT-34704657427 | product | REVISE | REVISE | C-PARAM-INHERIT | `569a1573e40b` |
| EXP-GRAPH-34711403174 | graph | REVISE | SURVIVES_CURRENT_TEST | C-FRESHNESS | `d72132df7f23` |
| EXP-INTEL-34718481334 | intel | REVISE | MEASUREMENT_INVALID | C-CROSSSITE, C-LLM-INHERIT | `bfbe74400ae9` |
| EXP-PHYSICS-34719136202 | physics | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `6fc96c940178` |
| EXP-PHYSICS-34724244876 | physics | FAIL | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `8ae879a69fd5` |
| EXP-FRONTIER-34729238832 | frontier | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `636109afec36` |
| EXP-RUNTIME-34741873198 | runtime | REVISE | SURVIVES_CURRENT_TEST | C-MEAS-VALID | `7c633b0a2a5c` |
| EXP-GRAPH-34755316488 | graph | FAIL | FALSIFIED-IN-SETTING | C-FRESHNESS | `5a2e3b5ab3b6` |
| EXP-PHYSICS-34764605162 | physics | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `b8b379afd65b` |
| EXP-FRONTIER-34773875458 | frontier | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `858edf9f6a14` |
| EXP-INTEL-34782350557 | intel | REVISE | INCONCLUSIVE | C-MEAS-VALID, C-CROSSSITE, C-LLM-INHERIT | `1addb517158e` |
| EXP-GRAPH-34788722106 | graph | PASS | FALSIFIED-IN-SETTING | C-FRESHNESS | `78a2a667be8f` |
| EXP-FRONTIER-34794649996 | frontier | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `2916a7c97b2c` |
| EXP-PHYSICS-34846934524 | physics | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `d2eff3812d50` |
| EXP-FRONTIER-34881708619 | frontier | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `57ca23d0c9a4` |
| EXP-RUNTIME-34902094115 | runtime | PASS | SURVIVES_CURRENT_TEST | C-MEAS-VALID | `651877a2e9e9` |
| EXP-PHYSICS-34932344937 | physics | REVISE | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `894ea2ef394f` |
| EXP-INTEL-34956989900 | intel | PASS | FALSIFIED-IN-SETTING | C-MEAS-VALID, C-CROSSSITE, C-LLM-INHERIT | `ac10541a53a9` |
| EXP-RUNTIME-34986155186 | runtime | PASS | MIXED | C-MEAS-VALID | `5c54f99d8325` |
| EXP-GRAPH-35010853847 | graph | PASS | FALSIFIED-IN-SETTING | C-FRESHNESS | `39381a4eda53` |
| EXP-PHYSICS-35040401992 | physics | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `77d4d2323629` |
| EXP-RUNTIME-35058619700 | runtime | REVISE | MIXED | C-MEAS-VALID | `9875ae7717e8` |
| EXP-INTEL-35083033552 | intel | REVISE | SURVIVES_CURRENT_TEST | C-MEAS-VALID | `f0eb80b6f16f` |
| EXP-GRAPH-35083040517 | graph | PASS | FALSIFIED-IN-SETTING | C-FRESHNESS | `8310a3a35cd4` |
| EXP-INTEL-35112013458 | intel | PASS | FALSIFIED-IN-SETTING | C-MEAS-VALID | `d5a6add38ab8` |
| EXP-INTEL-35124660457 | intel | REVISE | MEASUREMENT_INVALID | C-MEAS-VALID | `211227fc1809` |
| EXP-PRODUCT-35124662913 | product | PASS | SURVIVES_CURRENT_TEST | C-PARAM-INHERIT | `75062582173d` |
| EXP-RUNTIME-35130682006 | runtime | REVISE | SURVIVES_CURRENT_TEST — all 4 frozen decision-rule conditions pass. Decompression-normalization (SHA256 on decompressed body + status via brotli.decompress after Content-Encoding:br removal) preserves body-only discrimination at structural ceiling 0.5 on /userinfo and 0.8333 on /introspect under synthetic brotli quality selection from {4,5,6,7,8} via local Python proxy (N=20 per state, seed 44, 1KB compressible JSON). Algorithm-equivalence with gzip holds (diff=0.0). However, audit REVISE narrows claim ceiling: effective brotli diversity is 2 variants (q4 distinct vs q5-8 identical for all tested body types), not 5 distinct; the 5-level range is not a materially stronger stress test than binary {4,8} for these payload sizes. H3 (compressed <0.35) is falsified on /userinfo (0.4329 > 0.35). Producer's SUPPORTS outcome is accepted with narrowed ceiling per audit required_fixes. | C-MEAS-VALID | `2918969df710` |
| EXP-PRODUCT-35130681515 | product | PASS | SURVIVES_CURRENT_TEST | C-PARAM-INHERIT, C-PRODUCT-ECON | `0efda56bec08` |
| EXP-PHYSICS-35130680344 | physics | MEASUREMENT_INVALID | MEASUREMENT_INVALID | C-WEB-DYNAMICS | `d35778c4f190` |
| EXP-GRAPH-35130682058 | graph | REVISE | FALSIFIED-IN-SETTING | C-FRESHNESS | `a605af55689d` |
| EXP-INTEL-35131994346 | intel | REVISE | PROVENANCE_PARTIAL | C-CROSSSITE, C-LLM-INHERIT | `57efaab4f562` |
| EXP-PRODUCT-35132898840 | product | REVISE | REVISE — frozen decision rule passes arithmetically on all 5 conditions (Fix1+Fix2+Fix3 importable, binding_accuracy=1.0 on 3 parameterized endpoints, mechanism count 3 vs 5 = 40% reduction, protocol-only prevalence 19.23% on curated corpus, zero task failures). However, the audit identifies high-severity measurement validity gaps that prevent producer claims from being fully supported: (1) protocol-only prevalence measured on curated 52-URL hardcoded list (V1_PROTOCOL_CORPUS_NOT_LIVE) not actual live browser traffic as required by spec measurement_validity[3]; (2) binding accuracy validated by exact URL string matching (V2_BINDING_NOT_HTTP) not real HTTP execution against jsonplaceholder.typicode.com as required by spec measurement_validity[2]; (3) mechanism count reduction conflates GET/PUT methods (V3_MECHANISM_COUNT_METHOD_CONFLATION) — method-aware counting yields 5 vs 4 = 20% at threshold; (4) token cost baseline uses arbitrary arithmetic without pricing documentation (V4_TOKEN_COST_ARBITRARY); (5) B_UNFIXED_PROTOCOL_ONLY baseline omitted (V7_B_UNFIXED_MISSING). The claim ceiling is bounded to: committed-code synthetic single-slot with metadata-only slot_prefixes on src/spider/kernel.py, string-match binding accuracy 1.0 on 3 parameterized endpoints, method-excluded mechanism reduction 40% (method-aware 20% at boundary), curated 52-URL protocol-only prevalence 19.23% (20.41% deduped). Real HTTP binding correctness, live traffic prevalence, literal vs parameterized real cost per successful task (C-PRODUCT-ECON), and model-token economics are NOT established. No product promotion. | C-PARAM-INHERIT, C-PRODUCT-ECON | `6e4206dcccf7` |
| EXP-PHYSICS-35137030850 | physics | REVISE | FALSIFIED-IN-SETTING | C-WEB-DYNAMICS | `c87d8226bdc3` |
| EXP-RUNTIME-35137033384 | runtime | PASS | SURVIVES_CURRENT_TEST — all 4 frozen decision-rule conditions pass. Decompression-normalization (SHA256 on decompressed body + status) preserves body-only discrimination at structural ceiling 0.5 on /userinfo and 0.8333 on /introspect under localhost CDN-noise proxy simulating 6 categories (brotli quality variation, chunked transfer-encoding, CDN headers, Accept-Encoding negotiation, response caching, Content-Length variation). Algorithm-equivalence with gzip holds (|diff| = 0.0 < 0.1). Compressed-byte-only hashing degrades to 0.2789 on /userinfo (< 0.35), confirming H3. Claim ceiling advances from 'synthetic proxy only' to 'synthetic proxy + CDN simulator with realistic non-determinism'. Audit PASS confirms all recomputed metrics match producer (max_abs_diff 0.0). Bounded to: localhost synthetic proxy, 1KB compressible JSON, effective brotli diversity 2 variants (q4 distinct vs q5-8 identical), mock OAuth2 4 states with 3-way error collapse (ceiling 0.5 on /userinfo), seed 44, N=20 per state, chunked decoded by HTTP client before decompression. Do NOT promote to Product Core — real-CDN infrastructure validation remains the critical untested blocker. | C-MEAS-VALID | `3b672238c289` |

## Latest recorded claim events

These are chronological latest events, not an automatic truth ranking.

| Claim | Status | Experiment | Lane |
|---|---|---|---|
| C-CROSSSITE | HYPOTHESIS | EXP-INTEL-35131994346 | intel |
| C-FRESHNESS | HYPOTHESIS | EXP-GRAPH-35130682058 | graph |
| C-LLM-INHERIT | HYPOTHESIS | EXP-INTEL-35131994346 | intel |
| C-MEAS-VALID | EXPERIMENTAL | EXP-RUNTIME-35137033384 | runtime |
| C-PARAM-INHERIT | EXPERIMENTAL | EXP-PRODUCT-35132898840 | product |
| C-PRODUCT-ECON | HYPOTHESIS | EXP-PRODUCT-35132898840 | product |
| C-SEMANTIC-RESOLVE | EXPERIMENTAL | EXP-GRAPH-34586318405 | graph |
| C-WEB-DYNAMICS | HYPOTHESIS | EXP-PHYSICS-35137030850 | physics |
