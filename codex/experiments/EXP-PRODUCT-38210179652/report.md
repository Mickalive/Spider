# EXP-PRODUCT-38210179652 — EXECUTE report

Lane: **product** · design_contract_version: **2** · parent: EXP-PRODUCT-38205292822
Target claim: **C-PARAM-INHERIT** (retained at EXPERIMENTAL in every branch).
This packet is **MEASUREMENT-ONLY**: it invokes the shipped carrier
`src/spider/kernel.py` unchanged and writes no product code.

## 0. Provenance and integrity

- Frozen inputs match `freeze.json.hashes`: `request.json`, `spec.json`,
  `prereg.md`, `design_review.json`.
- All six `freeze_artifacts` re-hash identically after the run; the shipped
  carrier is untouched (`src/spider/kernel.py` sha256 `3a6caf97…`).
- The FROZEN RUNNER was extracted verbatim from `prereg.md`; its raw-byte
  sha256 is `99d4edf542b3aad2acce14ce702f8e3caf5478922eae720de5f33b63cc2ab820`,
  exactly the declared value in prereg.md section 1.
- `V8_FREEZE_BINDING` PASS in **BOUND** mode inside the runner
  (`runner_block`, `prereg_sha`, and all six artifact checks true).
- Raw evidence (stdout/stderr, runner source) is stored separately under
  `raw_evidence/`; measurements are in `result.json.metrics`; interpretation is
  confined to this section and `result.json` narrative fields.

## 1. What was run

Deterministic, stdlib-only, credential-free. Eight expansion families whose
origins lie outside the frozen seven-family audited bank were declared before
scoring. An audited-origin allowlist `O1,O2,O3,O4` gates adoption; the shipped
`SpiderKernel.ingest_declaration` + `certify_declaration` path is invoked with a
negative bank grown by real loopback HTTP probing (seed `38210179`, alphabet
`0123456789abcdef`, budget 256/family). Two in-process runs are compared for
determinism; the whole process was executed a second time as an additional
cross-process check.

## 2. Raw observations (direct)

- `V8_FREEZE_BINDING` PASS (BOUND); all five frozen gates PASS
  (`validity_gate`, `sensitivity_gate`, `provenance_gate`, `growth_gate`,
  `boundary_gate`).
- Induction identity: `M-MECHANISM-COUNT=8`, `M-SINGLE-SLOT=true`,
  `M-CONFIDENCE-0.9=true`, `M-SUPPORT-IDENTITY=true`.
- Treatment, within-envelope (`H1–H6,H8`): `M-T-FALSE-ACCEPT-COUNT=0`,
  `M-T-HTTP-ON-OUT-COUNT=0`, `M-T-REFUSAL-SEMANTICS-VIOLATIONS=0`,
  `M-T-COVERAGE=1.0` (30/30) vs `M-B-SHIPPED-COVERAGE=0.4667` (14/30),
  `M-T-COVERAGE-DELTA-VS-SHIPPED=+0.5333`; anchor `0.6750` cleared.
- Arms on the same bank: `C-FROZEN-CERT` FA=9 at coverage 1.0; `A-RAW-DECL`
  FA=9; `A-PROV-NO-GROW` FA=6 (H5,H6); `A-GROW-NO-PROV` FA=3 (H8);
  `A-PROV-STRICT` FA=0 at coverage 0.4667; `B-ORACLE` coverage 1.0 FA=0.
- Certification: H1–H4 CERTIFIED; H5,H6 REFUSED by growth; H7 CERTIFIED;
  H8 refused by the origin gate (`provenance_gate=REFUSED_ORIGIN`) even though
  the certificate would admit it.
- Boundary family H7: `M-T-BOUNDARY-FALSE-ACCEPT-COUNT=3`; `BP-HIDDEN-FAILS`
  fires and `PC-GROW-MISSES-HIDDEN` passes.
- Drift probe: `M-R-DRIFT-STALE-FA=16`, `M-R-DRIFT-REMINE-FA=0`.
- Cost: `M-T-PROBE-CANDIDATES=1792`, `M-T-ORACLE-CALLS=168` growth calls,
  `M-EVAL-ORACLE-CALLS=266`, `M-T-GROW-LATENCY-MS=134.26`.
- All 12 controls PASS (`result.json.controls`); determinism repeat identical;
  regression `tests_run=3, failures=0, errors=0`.

## 3. Derived measurement and frozen decision

Applying the frozen decision rule to `result.json.metrics`:

- Safety: `M-T-FALSE-ACCEPT-COUNT=0`, `M-T-HTTP-ON-OUT-COUNT=0`,
  `M-T-REFUSAL-SEMANTICS-VIOLATIONS=0`.
- Expansion: `M-T-COVERAGE=1.0 > M-B-SHIPPED-COVERAGE=0.4667` **and**
  `>= 0.6750`.

→ `status=COMPLETE`, `outcome=SUPPORTS`,
`decision=PROVENANCE_CERT_SAFE_AND_EXPANSIVE` (`result.json`).
`FALSIFIES` is demonstrably live on the same bank (`C-FROZEN-CERT`/`A-RAW-DECL`
FA=9) and `MIXED` is realized by `A-PROV-STRICT` (coverage 0.4667, FA=0).

## 4. Interpretation (bounded)

Within this synthetic expansion bank, provenance-controlled certification —
an audited-origin allowlist plus execution-grounded negative-bank growth over
the shipped certificate — safely widens the ingested declaration class beyond
the frozen audited boundary: it raises safe coverage from the shipped
conservative 0.4667 to 1.0 while holding zero false accepts, zero out-of-grammar
HTTP executions and zero refusal-semantics violations, and it strictly dominates
the frozen-certificate incumbent (FA 0 vs 9 at equal coverage). Both mechanism
components are individually necessary on this bank: provenance alone misses the
probeable evaders (`A-PROV-NO-GROW` FA=6) and growth alone misses the
non-allowlisted hidden evader (`A-GROW-NO-PROV` FA=3).

The result is explicitly **conditional**. The hidden boundary family H7 is
allowlisted and certificate-admitted; its over-accept lies outside the probe
alphabet and therefore survives growth, producing the recorded
`M-T-BOUNDARY-FALSE-ACCEPT-COUNT=3`. The guarantee is therefore conditional on
the allowlist AND on the probing procedure's reachable token space covering the
declaration's over-accepts. The drift probe further shows that a certificate
mined before a true-grammar change false-accepts (stale FA=16) until it is
re-mined against the drifted oracle (FA=0), so re-certification is a maintenance
requirement.

This is a bounded measurement on a synthetic eight-family construction; it is
NOT an end-to-end external-agent measurement, NOT a general soundness proof and
NOT a product-economics measurement. Per the frozen
`spec.json#decision_rule.claim_status_semantics`, **C-PARAM-INHERIT is RETAINED
at EXPERIMENTAL in every branch**, no code is promoted, and any product decision
about the breadth of the trust boundary is a downstream DIRECTOR decision.

## 5. Validity threats

- `V10`: results bound THIS bank, THIS fixed seeded probe space and THIS carrier.
- Zero false accepts is **within-envelope** by frozen construction
  (`WITHIN_ENVELOPE` excludes H7); H7's FA=3 is the recorded boundary, not a
  treatment safety violation.
- Cost is loopback HTTP/latency only; real provenance/allowlist administration
  and negative-bank acquisition economics are not measured.
- The drift probe is decoupled and non-gating.
- Any identity/prerequisite/freeze/regression/gate failure would be
  BLOCKED/MEASUREMENT_INVALID, never FALSIFIES; none occurred.

## 6. Artifacts

- `result.json` — producer handoff (metrics, controls, artifact hashes).
- `provenance.json` — commands, commits, environment, re-hashed dependencies.
- `raw_evidence/run_prov_grow.py` — FROZEN RUNNER, sha256 `99d4edf5…`.
- `raw_evidence/raw_run_output.json`, `raw_run_stderr.txt` — primary run.
- `raw_evidence/raw_run_output_run2.json`, `raw_run_stderr_run2.txt` — second
  full process run for cross-process determinism.
