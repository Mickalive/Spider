# EXP-PHYSICS-37992957068 — EXECUTE report

Lane: **physics**. Target claim: **C-WEB-DYNAMICS**. Director mandate: PIVOT (barrier dynamics).

**status = `COMPLETE`  |  outcome = `INCONCLUSIVE`** (frozen branch: `INCONCLUSIVE`)

## 1. What was run

Frozen 57-endpoint credential-free universe x 12 fresh-cookie-jar sessions x up to J_max=5 GETs (3420 planned); 1254 requests issued over 336.2s with the four frozen arms (A_RETRY, A_RETRY_SPACED, A_FRESH, A_ADAPT). Class histogram: `{'BLOCK_403_CHALLENGE': 240, 'OTHER_NONBARRIER': 435, 'CLEAN': 501, 'TRANSPORT_ERROR': 52, 'RATE_LIMIT_429': 26}`. This is a credential-free GET-only instrument (no browser/JS/auth/model calls).

## 2. Measurement validity

- Headline: **COMPLETE**.
- Live oracles all classified as expected: True.
- A_ADAPT treatment liveness (non-network trace): all_classes_defined=True, terminates_within_J_max=True.
- Classifier reproducible from stored fields: 0 mismatches / 1254.
- Stratum floors: barrier-exposed endpoints = 11 (>=3); scheduler barrier events = 318 (>=30).

## 3. Controls

- **PC_SYNTHETIC_DYNAMICS** (positive control: offline planted schedule-dependent hazard): expected power (fraction of R=200 reps with SKILL_LL CI lower > 0) >= 0.80; observed=0.98; pass=True.
- **NC_SYNTHETIC_MEMORYLESS** (negative control: offline i.i.d. endpoint-constant barriers): expected false-positive rate (CI lower > 0 fraction) <= 0.05; observed=0.01; pass=True.
- **PC_BARRIER_ORACLE** (live positive control on deterministic barrier oracles): expected status/403 -> barrier-family; status/429 -> RATE_LIMIT_429; unresolvable host -> TRANSPORT_ERROR; observed=True; pass=True.
- **NC_CLEAN_ORACLE** (live negative control on clean endpoints): expected status/200 and uuid -> CLEAN; observed=True; pass=True.

## 4. Primary metrics

- **SKILL_LL** = 0.0051411334373070855 nats/request (CI95 [-0.00933845159088395, 0.019388300216115453]); threshold delta_SKILL = 0.05 with CI lower > 0 for PRED_PASS.
- M_HISTORY_NOID ablation SKILL_LL = -0.16769865144813678 (CI95 [-0.20766734593518785, -0.12518679747297579]).
- SKILL_BA = 0.004273504273504258.
- ONSET_SKILL_LL = null (n=0; no ONSET events in this window); RECOVERY_SKILL_LL = -0.15683934234527497 (n=13).
- SEPARABILITY_SKILL_LL (barrier vs ordinary unavailability) = 0.020645683265606084 (n=753).

## 5. Scheduler economy (barrier-exposed stratum)

- d_Req = -2.4848484848484853 requests/episode (clustered CI [-3.3900752464971458, -1.6916514227642279]); d_Succ = 0.0.
- A_ADAPT mean requests 1.2727272727272727 vs A_RETRY 3.757575757575758; no-barrier success baseline 0.25.

## 6. Frozen branch decision

- PRED disposition: PRED_AMBIG; SCHED disposition: SCHED_ECON_PASS.
- **Branch = INCONCLUSIVE** => outcome **INCONCLUSIVE** (status COMPLETE).

## 7. Validity threats

- **V1_ENDPOINT_CONSTANT_DOMINANCE**: The frozen pool is dominated by endpoint-constant behaviour (e.g. Cloudflare 403-challenge endpoints and one unresolvable transport endpoint). This is a genuine scientific S0 risk and is captured by the identity/persistence nulls; it is not a measurement failure.
- **V2_RUN_DEFINED_STRATUM**: The scheduler stratum is defined by barrier events observed in this run (pre-registered conditional subgroup). The fixed pre-freeze candidate set is separately reported in spec.scheduler_strata; all inference is additionally reported relative to it.
- **V3_SEQUENTIAL_POLICY**: For retry arms later requests occur only after non-CLEAN responses, so the request population is policy-dependent. Cross-validation respects time order and uses only past features; all nulls see the same rows.
- **V4_SINGLE_WINDOW_AND_CLIENT**: One stdlib-HTTP client, one collection window, one frozen 57-endpoint universe. Rates and classes describe this pool and window only, not the Web.
- **V5_REPRESENTATION_LOSS**: Credential-free GET only: no JavaScript, DOM, SPA, GraphQL, WebSocket, browser TLS fingerprint or authenticated state. Barrier mechanisms that depend on those observables are invisible to this instrument.
- **V6_ONSET_UNOBSERVED_IN_WINDOW**: No ONSET events (prev CLEAN -> barrier) occurred in this window (ONSET_n=0), so ONSET_SKILL_LL is null. This is a property of the window, not a measurement failure; the frozen primary PRED_PASS/PRED_FAIL branch depends only on the pooled next-request task which had 1254 held-out rows.
- **V7_IMPLEMENTATION_DEBUGGING_BEFORE_OUTCOMES**: The analysis code is authored at EXECUTE as a literal realisation of the frozen literals. Three pure implementation defects (a Python-list index in the transition sub-routine, a keyword-argument name mismatch, and a missing numpy import) were fixed during a pre-outcome smoke run of the sub-steps. No frozen literal, threshold, model feature set, seed or branch rule was altered or retuned after observing any outcome.
- **V8_CENSUS_ARTIFACT_NOT_IN_REPO**: The pre-freeze reachability census /tmp/opencode/phys379/census.json cited by spec.json for the attainability certificate is not present in this environment (it lived in an external temp dir). Its hash is recorded as null in provenance; its cited facts remain design-time disclosures, and the run's own attainability floors are verified directly from observed data.

## 8. Unresolved

- **U1_GENERALIZATION_WINDOW**: Do the observed barrier classes and (absent) onset dynamics persist across collection windows and source IPs? A second window would distinguish stable structure from a point-in-time artifact.
- **U2_ONSET_MECHANISM**: ONSET events were not observed on this pool/window. Which endpoints (if any) exhibit a clean-to-barrier transition under a longer, higher-rate or different-spacing probe, and is it schedule-driven?
- **U3_CONSTRUCT_BOUNDARY**: What is the real-Web barrier dynamics on JavaScript-rendered, authenticated or SPA substrates that this credential-free GET instrument cannot observe?
- **U4_MIXED_PRODUCT_POLICY**: If the branch is INCONCLUSIVE/MIXED, what is the minimal additional design (larger barrier-exposed pool, forced onset via spacing) that would make PRED_PASS/PRED_FAIL decidable?

## 9. Product interpretation (bounded)

Mixed/inconclusive: the two frozen sub-branches disagree or are ambiguous; no single product policy is licensed by this packet. On the predictive side SKILL_LL = 0.0051411334373070855 nats with CI95 [-0.00933845159088395, 0.019388300216115453] (delta_SKILL = 0.05) and the endpoint-identity ablation M_HISTORY_NOID = -0.16769865144813678 is strongly negative, so no online history-based barrier model is licensed on this evidence. On the scheduler side d_Req = -2.4848484848484853 requests/episode with clustered CI [-3.3900752464971458, -1.6916514227642279] at d_Succ = 0.0 (SCHED_ECON_PASS), but on this pool that economy is largely a mechanical consequence of the frozen arm definitions on endpoint-constant barriers rather than demonstrated predictive barrier dynamics. Claim status unchanged; no promotion.

