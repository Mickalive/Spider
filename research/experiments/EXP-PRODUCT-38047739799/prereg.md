# EXP-PRODUCT-38047739799 preregistration

Lane: product. Claim: C-PARAM-INHERIT. Design contract: v2 (frozen 2026-10-10).

## 1. Direction and mandate

This experiment executes the Global Research Director mandate for cycle 38047320124:
CONTINUE, claim `C-PARAM-INHERIT`, cognitive reset, parent handoff
`EXP-PRODUCT-37989728440` disposition SUPERSEDE. The mandate question is whether the
audited parameterized-inheritance capability can be made DURABLE and PROMOTABLE in the
shipping kernel path (`src/spider`) so that it lands in `main` through the pinned Product
promotion path without manually copying experiment code. This is open blocker B1 and
readiness condition (1) of `PROGRAM_AUDIT_2026-10-10.md`.

## 2. Treatment and comparators

Treatment (EXECUTE):
- Replace `src/spider/kernel.py` byte-identically with the frozen audited carrier
  `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`
  (sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`, git blob
  `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`).
- Do NOT modify `src/spider/models.py` (sha256 `338aaf4d...`) or `src/spider/registry.py`
  (sha256 `51fb440d...`); the carrier is a drop-in on their shipped bytes.
- Byte-copy the frozen instrument files into this experiment's harness:
  `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py`
  (sha256 `b0ffcbba...`) and
  `research/experiments/EXP-PRODUCT-37950607128/harness/run_certificate.py`
  (sha256 `59895ddd...`). Run the copied runner so raw evidence lands in this
  experiment's `raw_fixture/` and `raw_certificate/` directories.
- Add `tests/test_ship_kernel.py` asserting the parameterized round trip, the three
  refusal categories, and inherited-path counter increments.

Comparators / controls:
- `B-SHIPPED-PRE-INSTALL`: the unmodified shipped kernel (blob `cfec9866...`), which lacks
  `distill_parameterized`, `TrajectoryCounters` and `_support_accepts`.
- `B-LITERAL-KERNEL`: post-install literal `distill()` path on the same bank; must be 0.
- `B-RETRIEVAL-SHAPED`: exact-retrieval comparator; non-gating.
- `AD-POSITIVE-ROUNDTRIP` (positive control) and `NC-ZERO-CONTRAST-TREATMENT`
  (degenerate null) as defined in `spec.json`.

## 3. Frozen instrument

`ARM-DIFFERENTIATION-CERTIFICATE-v1` on task bank `SYNTH-INDUCTION-BANK-v1`
(seed 37950607128), deterministic and credential-free (standard library only). It emits
raw `raw_fixture/synth_induction_bank.json`,
`raw_certificate/arm_differentiation_certificate.json` and
`raw_certificate/accounting_fidelity_trace.json`. The instrument embeds its origin
experiment id `EXP-PRODUCT-37950607128`; that raw field is preserved verbatim and the
packet's own `experiment_id` is authoritative.

## 4. Frozen decision rule

Seven gates, evaluated in the precedence order defined in `spec.json.decision_rule`:

- C1 `AD-IDENTITY-BINDING` (gate MEASUREMENT_INVALID): installed kernel sha256 == carrier
  sha256 AND git blob == carrier blob AND all `freeze_artifacts` hashes match.
- C2 `AD-POSITIVE-ROUNDTRIP` (gate FALSIFIES): 6/6 known-positive families resolve
  EXECUTABLE, correctly bound, execute 200, verify true.
- C3 `AD-NEGATIVE-ROUNDTRIP` (gate FALSIFIES): 24/24 known-negatives refuse with a
  non-empty reason and null action (missing_param, out_of_support, wrong_intent).
- C4 `AD-TREATMENT-CONTRAST` (gate MEASUREMENT_INVALID): real contrast 1.0 AND degenerate
  variant detected.
- C5 `PC-ACCOUNTING-FIDELITY` (gate MEASUREMENT_INVALID): max relative error <= 0.01 AND
  inherited-path increments == {retrieval_calls: 3, verification_calls: 2,
  repair_attempts: 1}.
- C6 `B-LITERAL-KERNEL` (gate MEASUREMENT_INVALID): held-out executable count == 0.
- C7 `PROMOTABILITY-REGRESSION` (gate FALSIFIES): `compileall -q src`,
  `unittest discover -s tests` and `scripts/validate_repo.py` all exit 0.

Outcome: SUPPORTS iff C1..C7 pass. FALSIFIES iff C1 passes and C2/C3/C7 fails.
MEASUREMENT_INVALID if C1 fails or (C1/C2/C3/C7 pass and C4/C5/C6 fails). BLOCKED if a
frozen prerequisite is missing or installation is out of scope. Raw evidence, observations,
derived metrics and interpretation must be reported separately in `result.json`.

## 5. Design-time satisfiability probes

These are bounded, non-outcome-bearing probes run during DESIGN to disprove the design's
own satisfiability. They use a throwaway sandbox (`/tmp`), never the experiment directory.

- Probe P1 (SUPPORTS reachability): built a sandbox `src/spider` from the shipped
  `__init__.py`/`models.py`/`registry.py` plus the frozen carrier `kernel.py`, copied the
  frozen `fixture.py` and `run_certificate.py`, and ran the runner. Result:
  `certificate_overall=PASS`, `outcome=SUPPORTS`, positive 6/6, negative 24/24,
  `treatment_contrast_rate=1.0`, `degenerate_variant_detected=true`,
  `counter_max_relative_error=0.0`, inherited increments `{retrieval_calls: 3,
  verification_calls: 2, repair_attempts: 1}`, literal `held_out_executable_count=0`,
  identity `pass=true`.
- Probe P2 (FALSIFIES reachability / treatment liveness): inspected the shipped
  `src/spider/kernel.py`; `distill_parameterized`, `TrajectoryCounters` and
  `_support_accepts` are all absent, so the certificate's import/positive arm is
  unreachable pre-install. The treatment is therefore live and different.
- Probe P3 (regression / backward compatibility): with the carrier installed, the existing
  `tests/test_kernel.py` still passes 3/3.

No confirmatory or outcome-bearing measurement was performed during DESIGN. Frozen
interpretation dependencies are hashed in `freeze.json.artifact_hashes`; `src/spider/kernel.py`
is intentionally not frozen because it is the treatment subject and is pinned by C1 instead.

## 6. Consequences

Positive: the audited carrier is durable and promotable; `product-promote.yml` extracts
exactly the `src`/`tests` delta and applies it to `main`; readiness condition (1) is met.
Negative (FALSIFIES): the carrier does not survive the shipping position;
`C-PARAM-INHERIT` is not advanced and `scripts/revert_product_reject.py` reverts the code
roots with no residue; the next action is to re-audit or re-derive the carrier.
MEASUREMENT_INVALID: no claim movement; repair the named gate and re-run.
