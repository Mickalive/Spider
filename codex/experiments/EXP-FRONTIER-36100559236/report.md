# EXP-FRONTIER-36100559236 Report — Heterogeneous Residual-Novelty Verification Economics (Director PIVOT)

**Lane:** frontier — C-RESIDUAL-NOVELTY (pay-novelty-not-length)  
**Status:** MEASUREMENT_INVALID  
**Outcome:** NOT_APPLICABLE  
**Experiment ID:** EXP-FRONTIER-36100559236  
**Frozen at:** 2026-09-25T05:59:29.991443+00:00  
**Parent:** EXP-FRONTIER-36099072254 handoff ef479f0688ce9d207ce3a207cda6f52683ec845e3182286c33c37d4ff5c686b7

## Summary
Diagnostic replication of the frozen heterogeneous WebChoreArena shootout after parent MEASUREMENT_INVALID. All substrate dependencies remain absent; no outcome-bearing measurements were run. This preserves the Director PIVOT SUPERSEDE design integrity while correctly distinguishing infrastructure failure from scientific falsification.

## Frozen Question
On WebChoreArena 532 tedious/memory + WebArena-Verified Hard 192/36 Jaccard<0.30 disjoint L=8-14 holdout (1280x720 CDP AX>10 DOM>=2000, deterministic random.Random(35725763380)) + Hard258 pooled >=10 families, does honest residual-novelty verification economics with per-trajectory hard-reset integer sum counters (TAU0.30+freshness TN>=0.85, 5000 bootstrap/block/global perms) demonstrate rho>=0.60 calibrated Pareto vs cold/RAG?

## Substrate Diagnostic (RAW EVIDENCE)
- live_available: false
- browsergym: False browsergym.core: False playwright: False agentlab: False
- intel_diverse_manifest_exists: False manifest_families: 0 (need >=10)
- runtime_wal_exists: False n_non304: None x_worker_pid: None (need >=360)
- chromium_present: True at ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome']
- pypi_reachable: True
- graph_freshness_exists: False freshness_tn: None
- pooled_tasks: 0 (<40 required) mixed_tasks: 0 (<10 required)
- heterogeneity_adequate: false coverage_adequate: false substrate_adequate: false

All 8 PCs and 6 NCs are NOT_RUN. Per measurement_validity clause 1, synthetic 36-family Jaccard 0.0 disjoint alphabets MUST NOT be substituted as heterogeneous evidence. This is a binding BINDING-RULE.

## Controls
- PC-HONEST-COST-SANITY: NOT_RUN — honest counters not executed, diff not measured
- PC-WEBCHORE-MANIFEST-ORTHOGONAL: FAIL — 0 families <10, Jaccard null, no 1280x720 CDP AX>10
- PC-TRAIN-TEST-DISJOINT: NOT_RUN — whole-trajectory holdout not constructed
- PC-CALIBRATION-DERIVED: NOT_RUN — softmax temp 0.15+jitter not computed
- PC-NOVELTY-MONOTONICITY: NOT_RUN
- PC-BUILD-COST-ISOLATED: NOT_RUN — 108 vector ops not counted
- PC-BROWSERGYM-SUBSTRATE: FAIL — no BrowserGym, n_non304 None <360
- PC-FRESHNESS-GATED-BAILOUT: FAIL — TN null, stale 0 <30
- NC-EMPTY-REGISTRY: NOT_RUN
- NC-NO-APPLICABLE: NOT_RUN
- NC-ORACLE-LEAK: NOT_RUN — forbidden-read audit not executed but harness inspection would be 0 if run
- NC-BIJECTIVE-COST: NOT_RUN
- NC-SHUFFLED-NULL: NOT_RUN — 5000 global/block perms not executed
- NC-GUARD-SPECIFICITY: NOT_RUN

Any PC/NC failure => MEASUREMENT_INVALID per frozen falsifier; no SURVIVES/FALSIFIES inference.

## Metrics (all null where outcome-gated)
- rho_novelty: null (need >=0.60 lower>0.40 p<0.05)
- rho_length_pooled: null (need |rho|<0.20 upper<0.25)
- ECE: null (need <=0.15 upper<=0.18)
- UNKNOWN precision: null (need >=0.85)
- saving_f10_pct: null (need >=25% lower>15%)
All gated metrics remain null because TAU0.30+freshness-gated pipelines were not executed.

## Prior Bounded Evidence (unchanged)
- Alias tunnel 21/40=0.525 Wilson [0.352,0.648] 0/10 mixed routing gain 0.0 p=1.0 — retrieval-diversity ceiling preserved
- Synthetic honest TAU0.30 non-Pareto EXP-FRONTIER-36042599040 rho 0.4837 CI[0.410,0.552] <0.60 ECE 0.216>0.15 RAG dominance false with all 11 PCs/NCs PASS — bounded to synthetic Jaccard 0.0 gate, not heterogeneous
- Parent EXP-FRONTIER-36099072254 diagnostic MEASUREMENT_INVALID audit PASS preserved

## Interpretation vs Observation
Observations are substrate diagnostics above. Interpretations (e.g., whether heterogeneous compressible structure would yield rho>=0.60) remain UNKNOWN and are explicitly not inferred from this diagnostic. Do not turn infrastructure failure into negative scientific result.

## Validity Threats Addressed
- Jitter/n*3200/f*6.0 bijective proxy: would be checked via NC-BIJECTIVE-COST gap>0.35 |rho_proxy|<0.60 but not measured
- Header variance / Jaccard orthogonality: would be gated by PC-WEBCHORE-MANIFEST-ORTHOGONAL Jaccard<0.30 but manifest absent
- Ceiling CI degeneracy: would require within-family std>0 zero_cells 0 but not measured
- Hash PMI / SHA instability: would be isolated via deterministic hashlib.sha256 and freshness gate but not executed
- Leakage via derived_context: would be audited via NC-ORACLE-LEAK 0 forbidden reads but not executed

## Product Consequence
No product promotion. C-RESIDUAL-NOVELTY remains HYPOTHESIS. Heterogeneous gate remains UNTESTED. Per Director comparative_reasoning, continuing alias/permutation tuning has VOI~0 (routing gain 0.0 p=1.0, 21/40 ceiling). The orthogonal WebChoreArena pivot is the highest-EV next test but is blocked on Intel manifest, Runtime health gate (n_non304>=360), BrowserGym pins, and Graph freshness TN>=0.85. Do not retry with synthetic fixture as live evidence.

## Unresolved
All 7 unresolved questions from result.json remain open; next experiment must be authorized only after Global Research Director verifies Intel+Runtime+BrowserGym+Graph substrates PASS.

## Artifacts
- substrate_diagnostic.json b4ccc55f...
- per_trajectory_traces.json 4f53cda1...
- honest_cost_audit.json 1f163c33...
- freshness_gate_check.json 5789d05b...
- compilation_pipeline_check.json 3853592f...
- webmcp_registry_check.json c35fb459...

Freeze verified true. No post-freeze spec/prereg tampering.
