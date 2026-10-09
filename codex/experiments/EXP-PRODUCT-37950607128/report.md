# EXP-PRODUCT-37950607128 — Shipped-kernel arm-differentiation certificate

- **Lane:** product
- **Claim under test:** `C-LLM-INHERIT` (NOT promoted by this packet)
- **Status:** `COMPLETE`
- **Outcome:** `SUPPORTS` (certificate established)
- **Run id:** 37950607128
- **HEAD:** `98bd80b943778b3895c7a3805dc5bccab7715d01` (branch `lab2/product`)

## 1. Question

Does the shipped kernel in `src/spider` execute an inherited parameterized
mechanism at a non-zero rate, demonstrated by a **pre-execution
arm-differentiation certificate** that is *shown to fire* on a synthetic,
credential-free fixture before any expensive arm runs? Specifically:

1. a known-positive round trip (induction -> parameterized distillation ->
   resolve to `EXECUTABLE` with a correctly bound non-null action -> execute ->
   verify);
2. a known-negative round trip (missing-parameter / out-of-support /
   wrong-intent refused with a reason and null action);
3. a treatment-contrast check in which a retrieval-shaped **zero-contrast**
   variant is detected as the null it is;
4. accounting fidelity where the inherited-path counters
   (`retrieval_calls`, `verification_calls`, `repair_attempts`) increment on a
   real mechanism execution, not only a scripted trajectory.

This is the credential-free half of the frozen design. The experiment is
deliberately **not** the four-arm benchmark; it certifies the instrument.

## 2. Method

The frozen `spec.json` / `prereg.md` define the synthetic bank
**SYNTH-INDUCTION-BANK-v1** (6 families) and the certificate checks. EXECUTE:

- reconstructed the bank deterministically (`harness/fixture.py`) and recorded
  its sha256;
- implemented the in-scope, preregistered kernel repair in `src/spider/kernel.py`:
  `distill_parameterized()` plus a parameterized confidence policy (0.9) that
  clears the unchanged `resolve()` threshold (0.8), parameter-support
  descriptors, refusals, and `TrajectoryCounters`;
- left the pre-existing literal `distill()` at confidence 0.5 so the
  pre-repair baseline `B-LITERAL-KERNEL` remains reproducible;
- ran the certificate (`harness/run_certificate.py`) and added 6 contract tests
  to `tests/test_kernel.py`.

The fixture bank is text-frozen in `prereg.md`/`spec.json`, which
`freeze.json` hashes; this, plus the recorded fixture sha256 and the pre/post
kernel git blob identities, is the **documented preregistered substitute** for
a direct code-hash freeze.

## 3. Results

| Check | Result | Key numbers |
|---|---|---|
| `AD-POSITIVE-ROUNDTRIP` | PASS | 6/6 held-out cases `EXECUTABLE`, 6/6 correctly bound, 6/6 verify True; `in_support_executable_rate = 1.0` |
| `AD-NEGATIVE-ROUNDTRIP` | PASS | 24/24 refused; out-of-support 1.0, missing-param 1.0, wrong-intent 1.0; all `bound_action=null`, non-empty reason |
| `AD-TREATMENT-CONTRAST` | PASS | 6/6 treatment != comparator; forced variant contrast 0.0 detected (`degenerate_variant_detected=true`) |
| `PC-ACCOUNTING-FIDELITY` | PASS | seeded trajectory `max_relative_error=0.0`; inherited-path increments `retrieval_calls=3`, `verification_calls=2`, `repair_attempts=1` exactly as declared |
| `AD-IDENTITY-BINDING` | PASS | fixture sha256 recorded; pre-repair blob `cfec9866…`, post-repair blob `b15ed848…` (differ, consistent) |
| `B-LITERAL-KERNEL` | PASS | 0/6 `EXECUTABLE` on held-out in-support set (pre-repair literal mode) |
| `B-RETRIEVAL-SHAPED` (non-gating) | recorded | comparator action differs from treatment on all 6 families |
| `NC-ZERO-CONTRAST-TREATMENT` | detected | variant contrast 0.0, reported as certificate failure |

`certificate_overall = PASS`. No pathological count occurred: the EXECUTABLE
rate on declared negatives is 0 and `refusal_rate = 1.0`.

Unit tests: `Ran 9 tests … OK` (3 pre-existing + 6 new contract tests).

## 4. Interpretation

The frozen decision rule maps **all checks PASS** to
`SUPPORTS (CERTIFICATE_ESTABLISHED)`. The shipped kernel, after the in-scope
repair, demonstrates:

- **liveness** — it executes an inherited parameterized mechanism for unseen
  in-support identifiers;
- **selectivity** — it is not an always-`EXECUTABLE` function; out-of-support,
  missing-parameter and wrong-intent bindings are refused;
- **arm-differentiation** — a bound mechanism action can differ from a
  retrieval-shaped comparator, and the certificate is shown to fire on the
  degenerate retrieval-in-disguise treatment;
- **accounting** — inherited-path counters increment on a real mechanism
  execution;
- **attribution** — the pre-repair literal path yields zero `EXECUTABLE`, so
  the observed liveness is attributable to the in-scope repair.

## 5. Claim ceiling (binding)

This packet measures **only** the certificate and kernel
liveness/selectivity/accounting. It does **not** run the cold / instructions /
retrieval / SPIDER arms and therefore provides **zero evidence for or against
C-LLM-INHERIT**. `C-LLM-INHERIT` remains `HYPOTHESIS` and must not be promoted,
cited, or treated as product evidence on the basis of this packet.

The product-positive consequence is narrow: the first admissible four-arm
benchmark is now executable and non-degenerate **pending a model credential**.

## 6. Threats to validity

- **Self-fulfilling certificate:** EXECUTE authored both the repair and the
  harness. Mitigations actually exercised are the negative round trip (24/24),
  unseen held-out identifiers, the forced degenerate variant, the text-frozen
  fixture, the absence of pathological counts, and the causal
  `B-LITERAL-KERNEL` baseline. AUDIT should rebuild the fixture independently
  and re-run against the recorded kernel commit.
- **Support-inference narrowness:** support descriptors are inferred from the
  finite induction values (e.g. F1 infers `^itm\-000[0-9]{1}$`); sufficient for
  the frozen checks but a bounded-fixture artefact, not general grammar
  induction.
- **Noise handling:** noise fields (`trace_id`, `seq`, `ts`, `nonce`) did not
  become slots — declared vs inferred slot counts match for every family,
  including `F6-NOISE-STRESS` (1/1).
- **Credential-free by construction:** model/browser/http counters are 0; model
  counters were exercised only on an explicitly *injected* event.

## 7. Reproduction

```bash
cd /home/runner/work/Spider/Spider
PYTHONPATH=src python3 research/experiments/EXP-PRODUCT-37950607128/harness/run_certificate.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Raw evidence: `raw_certificate/arm_differentiation_certificate.json`,
`raw_certificate/accounting_fidelity_trace.json`,
`raw_fixture/synth_induction_bank.json`. Hashes and environment are in
`provenance.json`. Certificate semantics and mandatory-field values are in
`result.json`.
