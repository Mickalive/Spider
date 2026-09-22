# EXP-RUNTIME-35774047385 — Execute report

**Lane:** runtime  **Status:** MEASUREMENT_INVALID  **Outcome:** NOT_APPLICABLE

## Claim under test
C-MEAS-VALID: does the HTTP fingerprint substrate `SHA256(status || body_bytes || sorted_filtered_headers)` retain its deterministic same-status body-only / header-only discrimination, null stability and writable permission/session behavior when moved from single-host gunicorn+nginx loopback to a PAID-CDN edge and a BrowserGym/AgentLab observation layer (global-director CONTINUE)?

## What was measured
- Sanity topology L (Werkzeug threaded): replication gate — `{'l_body_AvsC_full': 1.0, 'l_body_AvsC_status': 0.0, 'l_hdr_AvsE_full': 1.0, 'l_hdr_AvsE_body': 0.0, 'sanity_started_at': '2026-09-22T20:18:43.512796+00:00', 'sanity_finished_at': '2026-09-22T20:18:53.804342+00:00', 'n_per_state': 20, 'topology': 'L (Werkzeug dev server, threaded)'}`
- Diagnostic battery on available origin (gunicorn 2x sync + nginx loopback, N=20/batch, concurrency 4): raw line count 780 (sanity 100 + diagnostic 680); identity checks critical_all_pass=True.
- CDN probe: CDN_UNAVAILABLE — see cdn_probe.json.
- BrowserGym probe: NOT_TESTED — see bg_probe.json.

## Interpretation
Per the frozen decision rule, the paid-CDN claim is MEASUREMENT_INVALID (category CDN_UNAVAILABLE): No CF_API_TOKEN / FASTLY_API_KEY / SPIDER_CDN_DOMAIN in runner env or workflow secret block; paid CDN edge not provisionable from this runner.. This is NOT falsification — loopback diagnostic success cannot be read as CDN evidence, and the CDN conditions C1_CDN..C10_CDN are recorded NOT_MEASURED.

The loopback diagnostic battery (C1_LB..C10_LB, G1, G2, E1–E3) measured pipeline integrity, per-value magnitude gradients and origin readiness on the P_CDN origin; failing diagnostic conditions: [].

## Evidence chain
- RAW: raw_observations.jsonl (sanity L prefix + diagnostic battery), batch_state_log.jsonl (whole-run server-state log incl. sanity prefix), sanity_l_raw_observations.jsonl, cdn_probe.json, bg_probe.json
- DERIVED: experiment_result.json, sanity_l_result.json, result.json
- CODE: run_experiment.py (sha in provenance.json)

## Unresolved
- Paid CDN edge (Cloudflare/Fastly HIT/STALE/SWR/SIE/304, Vary/ETag, brotli/chunked) measurement pending: requires CF_API_TOKEN or FASTLY_API_KEY plus SPIDER_CDN_DOMAIN mapped into the runner; smallest unblocking action: add the CDN secrets to the lane workflow env and rerun this frozen experiment as-is.
- BrowserGym/AgentLab 1280x720 DOM/AX capture: E4_BG NOT_TESTED IMAGE_UNAVAILABLE; smallest unblocking action: runner with Docker registry access to pull am1n3e/webarena-verified-shopping or agentlab image, then rerun.
