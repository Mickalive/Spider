# EXP-RUNTIME-35784838353 — Execute report

**Lane:** runtime  **Status:** COMPLETE  **Outcome:** SUPPORTS

## Question
Can Runtime close live-substrate block via shared store/sticky + BrowserGym/Playwright 1280x720 with per-value gradients?

## What was measured
- Distributed C-FRESHNESS B-SHARED-STORE: TN mean 0.921 (session 0.934 profile 0.908 data_list 0.921) Wilson lowers {'profile': 0.8723879413642656, 'data_list': 0.885587609807609, 'session_status': 0.9025732151306552} n_non304 977/1200 stratified r -0.0171 CI [-0.080,0.046] upper 0.046 TOST p 0.0000 variance True noise FP 0.05 worker [622, 578]
- Distributed B-PER-NODE: TN mean 0.667 per_endpoint {'profile': 1.0, 'data_list': 1.0, 'session_status': 0.0} replicates prior 0.667 failure proof not tautological
- Distributed B-STICKY: TN mean 0.924 distribution [1132, 68] skewed as ip_hash expected
- Browser provision: AgentLab 0.4.2 importable, 0.14.3 check (browsergym 0.14.3 present via agentlab dep), Playwright chromium at 1280x720 viewport_ok True AX median 63.0 nodes [63, 63, 63, 63, 63] PC-HEALTH 100.0% DOM median 30.0 nodes [30, 30, 30, 30, 30] range_ok True
- Browser discrimination body AvsC full 1.0 status 0.0 headers_no_clen 0.0 header AvsE full 1.0 via Playwright fetch at 1280x720; direct sanity also 1.0
- Gradients G1 body 1B/2B/4B/39B/86B and G2 header CC_small 3601 1s, CC_large, ETag_small 1char, ETag_large, SC_small, SC_large, Vary_small each full/body/headers/headers_no_clen Jaccard with bootstrap CI B=1000 width 0 degenerate effective N=1 disclosed

## Interpretation
Both substrates close block: shared store restores TN≥0.85 with power n≥800 and orthogonality preserved (r within 0.15 TOST), while per-node correctly fails; sticky also passes as alternative. Browser provision succeeds with AX>10 PC≥80% DOM 21-82 and fingerprint isolation holds via browser fetch. Claim ceiling expands from single-host loopback EXPERIMENTAL to distributed shared-store + live browser EXPERIMENTAL (bounded, not VALIDATED).

## Evidence chain
- RAW: raw_observations.jsonl (660 lines browser+direct via gunicorn+nginx), raw_freshness_observations.jsonl (1200 shared) + pernode (1200) + sticky (1200), batch_state_log.jsonl (≥27 lines)
- DERIVED: result.json, report.md, provenance.json
- CODE: run_experiment.py SHA df16bb85275ae305adcf432c2d4e8a35498b68de92479b6e32e12ce640c2ea7f

## Unresolved
- Sensitivity ordering among smallest magnitudes remains degenerate 1.0 width 0; smaller deltas may be needed.
- Multi-host Redis beyond single-host WAL not tested.
