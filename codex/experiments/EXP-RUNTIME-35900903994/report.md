# EXP-RUNTIME-35900903994 — Execution Report

**Status:** COMPLETE
**Outcome:** MIXED
**Lane:** runtime
**Seed:** 44 | **N distributed/arm:** 1200 | **N browser/state:** 20

## Summary

This frozen run retests `C-FRESHNESS` and `C-MEAS-VALID` under the four parent-audit fixes:
status-free `hash(body)` structural, de-confounded scheduling, nginx health gate, and
URL-bound sticky sessions without dual-DB session mirroring during the arm.

- **Distributed branch:** C1/C2/C4 pass (shared TN mean 0.9745370370370371,
  n_non304 1073, noise FP 0.0);
  **C3 fails** (stratified r=0.7213198002332586, CI upper
  0.748914490044496 ≥ 0.15, TOST p_upper
  1.0 ≥ 0.05) with all validity gates green.
  Per frozen decision_rule: orthogonality **FALSIFIED-IN-SETTING** bounded to C3,
  not rescued by FIX-1/FIX-2.
- **Browser branch:** C5/C6a/C6b/C6c all pass at N=20 (body AvsC
  1.0, header AvsE
  1.0, null body
  0.0, AX median
  54.0, PC-HEALTH 100.0%).
- **Valid gates:** V-HEALTH-GATE (missing=0,
  status_none=0), V-STATUS-FREE-STRUCTURAL
  (prefix_present=False),
  V-SCHEDULING-INDEPENDENCE (confound r=0.06664837419350436).
- **Baselines:** B-SHARED-STORE pass; B-PER-NODE pass (TN
  0.6666666666666666 < 0.85);
  B-STICKY-URL **fail** (TN 1.0 but overall skew
  0.6666666666666666 ≤ 0.90; min per-URI affinity
  1.0).

**Packet outcome MIXED:** browser branch supports measurement validity in this fixture;
distributed detection/power/noise close, orthogonality does not.

## Metrics (selected)

| Metric | Value | Frozen expectation |
|--------|-------|--------------------|
| freshness_c1_tn_mean | 0.9745370370370371 | >=0.85 |
| freshness_c1_tn_session_status | 0.9236111111111112 | >=0.85 |
| freshness_c1_tn_session_status_wilson_lo | 0.8683944027724343 | >0.75 |
| freshness_c1_tn_per_node_mean | 0.6666666666666666 | ~0.667 <0.85 |
| freshness_c1_tn_sticky_url_mean | 1.0 | >=0.85 |
| freshness_c1_tn_sticky_url_skew | 0.6666666666666666 | >0.90 |
| freshness_c1_tn_sticky_url_min_uri_affinity | 1.0 | >0.90 |
| freshness_n_non304 | 1073 | >=800 |
| freshness_n_304 | 127 | real exclusion |
| freshness_n_missing_worker | 0 | 0 |
| freshness_n_status_none | 0 | 0 |
| freshness_stratified_r | 0.7213198002332586 | CI upper <0.15 |
| freshness_stratified_r_ci_lo | 0.6912278362739166 | >-0.15 |
| freshness_stratified_r_ci_upper | 0.748914490044496 | <0.15 |
| freshness_tost_p_upper | 1.0 | <0.05 |
| freshness_tost_pass | False | true |
| freshness_pooled_r | 0.597990022849456 | abs<0.15 |
| freshness_fp_noise | 0.0 | <=0.15 |
| freshness_c2_variance_pass | True | 8/8 |
| freshness_hs256_valid_success_rate | 0.9838235294117647 | >=0.90 |
| freshness_structural_status_prefix_present | False | false |
| freshness_scheduling_confound_r | 0.06664837419350436 | abs<0.30 |
| freshness_batch_state_log_len | 31 | >=27 |
| freshness_batch_state_log_distinct_ts | 93 | >=27 |
| freshness_worker_distribution_shared | {'66038': 581, '66039': 619} | >=10 each |
| bg_ax_nodes_median | 54.0 | >10 |
| bg_pc_health_pct | 100.0 | >=80 |
| bg_dom_nodes_median | 26.0 | 21-82 |
| browser_body_AvsC_full | 1.0 | >0.5 |
| browser_body_AvsC_status | 0.0 | 0.0 |
| browser_header_AvsE_full | 1.0 | >0.5 |
| browser_header_AvsE_headers_only | 1.0 | 1.0 |
| browser_null_body_full | 0.0 | <=0.05 |
| browser_gradient_* (all) | n=20, discrimination 1.0, ci [1,1] degenerate | ordered if width>0 |

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
| B-SHARED-STORE | True |
| B-PER-NODE | True |
| B-STICKY-URL | False |
| V-HEALTH-GATE | True |
| V-SCHEDULING-INDEPENDENCE | True |
| V-STATUS-FREE-STRUCTURAL | True |

## Interpretation (not raw observation)

1. **C3 orthogonality FALSIFIED-IN-SETTING under FIX-1+FIX-2.** With status-free
   structural and scheduling_confound_r=0.06664837419350436,
   stratified r remains 0.7213198002332586 (CI
   [0.6912278362739166, 0.748914490044496]).
   The parent hypothesized status prefix and scheduling confound as causes; both are
   removed and C3 still fails. Residual coupling is consistent with auth-dependent
   body content (error JSON vs success JSON) shared by `hash(body)` and
   behavioral_composite — a construction caveat, not a validity-triggering failure.
2. **Shared store restores freshness detection (C1/C2/C4)** vs per-node failure
   (TN 0.6666666666666666, session_status
   0.0), with real 304 exclusion and
   health gate — supports bounded C-FRESHNESS detection claim, not full SUPPORTS
   (C3 required).
3. **Sticky URL affinity routes consistently (min per-URI affinity
   1.0) but fails prereg overall
   skew >0.90** with 3 URIs (800/400). Pre-seeded dual-DB sessions make sticky TN
   1.0 non-diagnostic for post-hoc affinity-alone
   proof (see validity_notes).
4. **Browser C-MEAS-VALID holds at N=20** for body/header discrimination and nulls;
   gradients stay at ceiling (width 0) so magnitude ordering remains unknown but
   correctly powered (G2).

## Decision consequence

- Positive for bounded shared-store freshness detection + browser measurement validity.
- Negative for distributed orthogonality (`C3-FRESHNESS` fail with green validity) →
  full frozen SUPPORTS not reachable; packet **MIXED**.
- Next Director action should target residual structural-behavioral coupling (body-content
  confound or body-agnostic structural features), not re-run FIX-1/FIX-2 as if still open.

## Validity notes

- Sticky-URL sessions were seeded into both worker DBs at setup only; control-plane session writes were NOT mirrored during the arm (replicate_session_to_workers=False). Sticky TN therefore does not isolate post-hoc affinity for sessions created after routing; per-URI affinity and body/header config mirroring are the structural observations. Disclose before using sticky TN as affinity-alone proof.
- E4_STICKY_URL dual criterion: tn_mean=1.0 (>=0.85) and min per-URI affinity=1.0 but overall worker skew=0.6666666666666666 fails prereg >0.90 with only 3 distinct URIs under consistent hashing (observed 800/400 = 2/3 max unless all URIs collide). B-STICKY-URL pass=False reflects full dual criterion; exploratory, not gating.
- Browser gradients remain degenerate ci_95=[1.0,1.0] width=0 effective_distinct_n=1 at N=20 for all body/header magnitudes: responses are deterministic per state (set size 1). Per frozen prereg G2, ordering remains unknown but correctly powered; this is not underpowering (n_a=n_b=20) but ceiling/determinism of the fixture.
- C3 orthogonality validity gates pass (status-free structural, scheduling_confound_r = 0.06664837419350436 < 0.30, 0 missing worker/status None). Residual measurement caveat: error bodies (401/403 JSON) differ from success bodies, so hash(body) still co-varies with auth outcome even without status prefix — a shared substrate between structural and behavioral composite. Interpretation of r is bounded to this fixture construction; see report INTERPRETATION section.
- Prereg §5.4 estimated ~520 raw_observations lines; N=20 mandate per browser state is binding and actual raw_observations count is 1520. Power follows N=20, not the earlier line-count estimate.
- JWT HS256 secret is 25 bytes (PyJWT InsecureKeyLengthWarning: below 32-byte minimum for SHA256). Functional validation still achieved hs256_valid_success_rate=0.9838235294117647 (>=0.90). Disclosed as environment/credential length caveat, not measurement failure.
- Shared SQLite path /tmp/spider-runtime-35860330078/shared.db reuses parent frozen SHARED_DB constant as specified in this experiment freeze; DB cleaned before run. This is intentional path identity, not cross-experiment data carryover.
- frozen_b_flask_only_r (prereg §5.2) not computed: this run has no Flask-only baseline arm (all distributed arms are gunicorn+nginx real HTTP). Metric left absent rather than fabricating a value; alias not applicable to this design.

## Unresolved

- Does C3 orthogonality fail solely because auth-dependent error vs success body content couples hash(body) to behavioral_composite, or is there deeper structural-behavioral coupling on this substrate? Requires a fixture with status-matched bodies across auth states while varying only non-body signals, or structural features orthogonal to body content.
- Does sticky URL affinity alone suffice for freshness when sessions are created AFTER routing (not pre-seeded in both workers)? Requires sticky arm with initial session only on the hash-assigned worker and no dual-DB seed.
- Is overall sticky worker skew >0.90 achievable with only 3 endpoints under consistent hashing, or does E4 need more distinct URIs (or a single hot URI) to meet the prereg skew threshold?
- Can gradient ordering be measured at N=20 on a non-deterministic or partially overlapping fixture where effective_distinct_n > 1 and CI width > 0?
- What is freshness_b_flask_only_r under a Flask-only arm (if a future run adds that baseline)?
- Does C3 status-free r remain outside 0.15 if structural uses a status-free, body-agnostic feature set (e.g., header Jaccard excluding auth-derived headers only)?
