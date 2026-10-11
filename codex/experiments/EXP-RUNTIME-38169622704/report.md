# EXP-RUNTIME-38169622704 — SBA-CREDENTIAL-FREE-V2 substrate-validity certificate

status=COMPLETE outcome=SUPPORTS
lane=runtime claim_scope=C-MEAS-VALID (substrate validity only; no claim-status promotion)

## Question

Can a credential-free, stdlib-only synthetic HTTP task bank be made to *certify*
its own dynamic range — i.e. produce a frozen, reproducible certificate in which the
amortized treatment is exactly live (1.0) while strong memoryless comparators are
capped at the closed-form (K-1)/K — so that the flagship four-arm
`C-LLM-INHERIT` benchmark is unblocked with a calibrated B2 substrate?

This packet tests only the substrate-validity prerequisite. It does not run the
flagship benchmark and does not promote any mechanism.

## Frozen design (immutable)

- request.json   = aa62a6d3464444044eab5a1cf6cd2363d8d3fc1221858756b6c6509cf76750d6
- spec.json      = bc80c7c06fee33b9284ecb1cf94adf84b765a85668e40ca47ae01e99f264eb52
- prereg.md      = 3d706af3a54d1763af721215421adf3ad96a6f6a4b0629331392f3847c4aed46
- freeze.json    = cfbece9651388e12b623ebcc953b948f5c1b490d1ccaebff8a274852b9046fed
- design_review.json = 184857b7276d5d58ae9c835da9009392a6b4e3e343569d6b0cbb2ae0e33c05dd (PASS)
- harness run_experiment.py = 28704cf16399e7117096dfb300ab230674a2cebd122d68a1620499f7c5d664da
  (byte-identical to spec.design_satisfiability_probe.source_sha256 and the prereg
  BEGIN/END SBA-HARNESS block)

`freeze.artifact_hashes` is empty as declared; the single mutable interpretation
dependency is the EXECUTE copy of the harness, pinned by its sha256 and by the V1
code-fidelity manifest (`result.metrics.code_fidelity_manifest_v1`).

## Execution

`python3 run_experiment.py --mode scored --out artifacts/run_scored.json`
→ exit 0, empty stdout/stderr, wall clock 11m24s, Python 3.12.15.
The scored path runs the matrix twice (2 families × 4 novelty bands × 4 arms × 20
sessions = 640 sessions per pass) plus the control suite. Two independent passes
produced byte-identical cells (`determinism_ok=true`).

Non-outcome-bearing diagnostics re-run at EXECUTE:
`--mode probe` → artifacts/probe_mode.json (sha256 023cc3e2…, byte-identical to the
DESIGN-time `spec.design_satisfiability_probe.output_sha256`);
`--mode selftest` → artifacts/selftest_stdout.json (sha256 7456fc3b…, equal to
`spec.execute_evaluator_selftest_sha256`).

## Measurements (RAW EVIDENCE → DERIVED)

All V1–V8 gates true. Both families certified. Decision = SUPPORTS.

| family | K | closed form (K-1)/K | COLD obs | RETRIEVAL obs | T obs | PC obs | margin vs COLD | margin vs RETRIEVAL | distinct counter dims (T|COLD / T|RETR) |
|---|---|---|---|---|
| F1-RECORDS | 8 | 0.875 | 0.875 (140/160) | 0.875 (140/160) | 1.0 (160/160) | 1.0 | +0.125 | +0.125 | 2 / 3 |
| F2-WIDGETS | 10 | 0.900 | 0.900 (180/200) | 0.900 (180/200) | 1.0 (200/200) | 1.0 | +0.100 | +0.100 | 2 / 3 |

- Novelty bands 0.0 and 0.25: every arm 1.0 (ceiling band; certificate not evaluated).
- Novelty bands 0.50 and 0.75: comparators capped at (K-1)/K; T and PC live at 1.0.
- `matched_correctness == success_rate` in all 32 cells (exact-match scoring, V7).
- Counter profiles per session match the frozen predictions: T http 17/21,
  COLD 24/30, RETRIEVAL 24/30 + retrieval 8/10; comparators carry repair_calls=1 on
  the chain task at novelty ≥ 0.50.

Controls (stable identifiers; see `result.json.controls`):
`PC-EXACT-REPLAY` (positive) 1.0 everywhere; `NC-MECHANISM-OFF` exposing the binding
raises COLD to 1.0 and destroys the certificate; `NC-CEILING-BAND` holds;
`NC-EMPTIED-CONTEXT` tracks (K-1)/K; `NC-NO-LEAK` clean on all protocol invariants;
`NC-RETAIN-RECEIPT` 1.0 @0.50 → 0.875 @0.75; `NC-NO-DISCOVERY-DIRECT` 1.0 @0.0 →
0.0 @0.50; `NC-BINDING-UNIQUENESS` 0 collisions over 160 sampled 48-bit bindings;
`NC-MEMORYFUL` disclosed boundary (not a certificate input).

## Interpretation

The frozen certificate is satisfiable, reproducible and counter-identifiable: the
amortized treatment is live at every band while two distinct memoryless comparator
classes are capped at the predicted closed form, and they are distinguishable from
the treatment along 2–3 counter dimensions. The measured numbers equal the
arithmetic predicted in DESIGN; the EXECUTE probe and selftest reproduce the DESIGN
hashes byte-for-byte. This is a bounded substrate-validity result for
`C-MEAS-VALID`; it discharges the B2 dynamic-range prerequisite if the Director
accepts it.

## Validity threats

- The substrate is synthetic, credential-free, stdlib-only and generated from frozen
  literals; the dynamic range is an engineered `(K-1)/K` construction property and
  is **not** evidence about baseline strength on natural Web tasks.
- `NC-MEMORYFUL` is a disclosed boundary: a within-session-memoryful cold agent
  reaches 1.0 by retaining the precursor receipt. The certificate bounds the
  amortization rate, not agent capability.
- Scope is one construction class and two families (K=8, K=10); the K∈[6,12] sweep
  is arithmetically in band but only K=8 and K=10 were measured in the scored matrix.
- No claim status changes. The flagship four-arm `C-LLM-INHERIT` benchmark was not
  run; this is the prerequisite, not the test itself.

## Failures / anomalies

None. No infrastructure failure, no measurement-invalid condition, no gate failure.
