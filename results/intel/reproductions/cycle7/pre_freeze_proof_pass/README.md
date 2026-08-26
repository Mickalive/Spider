# NON-EVIDENCE — PRE-FREEZE PROOF-PASS ARTIFACTS (cycle 7)

Everything in this directory is marked NON-EVIDENCE per the mission
stop-condition (b): the mechanical instrumentation proof-pass executed
BEFORE the cycle-7 preregistration freeze. None of these files is
confirmatory data; the frozen evaluator reads only the post-freeze evidence
under `results/intel/reproductions/cycle7/`.

- `proof_pass_report.json` — final clean proof-pass report (all eight gates
  PASS). Probe volume inside. Two earlier proof-pass executions surfaced
  three instrument findings; all were repaired BEFORE the second (clean)
  pass and BEFORE the freeze, and are disclosed in prereg section 11:
    1. P-ECHO widening: browser client-hint/trace fields (Sec-Ch-Ua*,
       X-Amzn-Trace-Id) absent from any fixed header list produced
       missing-key deviations on httpbin FORM smoke -> policy amended to
       strip ALL keys under a detected echo-envelope headers object.
    2. Proof-pass smoke harness bug: it passed empty params to a task whose
       route has query slots (PARAM_UNRESOLVED artifact); smoke now drives
       each task's real call_sequence.
    3. Fingerprint canonicalization: httpbin /get embeds a per-request
       X-Amzn-Trace-Id, so its raw-body hash changes on every fetch ->
       httpbin excluded from fingerprint change detection (volatile by
       design), recorded for provenance only.
- `reachability_c7.json` — start-of-session reachability x3 + verbatim
  robots.txt quotes + restful-booker cooldown check (HTTP 418 on
  POST /booking persists after >1h natural cooldown) + clock-skew
  bookkeeping vs two independent server Date headers.
- `env_playwright_install.log` — environment setup record.

— INTEL_REPRODUCER, cycle 7, 2026-08-25
