# EXECUTE report — EXP-PRODUCT-37982016598

**Lane:** product
**Claim:** C-RESIDUAL-NOVELTY (C-RESIDUAL-NOVELTY)
**Status:** `MEASUREMENT_INVALID`
**Outcome:** `NOT_APPLICABLE`
**Canonical packet:** `result.json`, `provenance.json`, `derived/`, `raw_evidence/`

---

## 1. What was run

EXECUTE ran the frozen design exactly as frozen, using the frozen harness inputs
`request.json`, `spec.json`, `prereg.md`, `freeze.json`. The runner
`harness/run_experiment.py` executed the five frozen arms
(`T-SPIDER-PARAM`, `B-COLD-RE-DERIVE`, `B-RETRIEVAL-SHAPED`,
`B-EMPTIED-REGISTRY`, `PC-EXACT-REPLAY`) over the 4 resource families × 4 novelty
levels × 5 tasks = 80 tasks against a real localhost stdlib `http.server`
substrate (`harness/substrate.py`), with 20 declared known-negative task specs,
deterministic mechanical verification and honest per-task counters
(`http_requests`, `verification_calls`, `repair_attempts`, `latency_ms`).
`model_calls=0` and `model_tokens=0` by construction; 316 HTTP request cycles
were served.

The run is preserved as raw evidence and derived measurements. **It is not a
valid hypothesis test**, because the frozen primary gate C1 had already failed
at freeze time (see §2).

## 2. Why the measurement is invalid (frozen gate, not outcome-driven)

The frozen `spec.json` contains `"dynamic_range_certified": false` and a
`dynamic_range_certificate` whose fields are all null. The frozen `prereg.md`
is explicit (sections 5 and 12, and the closing line):

> The dynamic range certificate is a hard gate: if `dynamic_range_certified !=
> true` at freeze time, the experiment is `MEASUREMENT_INVALID` and must not
> proceed to EXECUTE.

and frozen `spec.measurement_validity.dynamic_range_certificate`:

> If certification fails, experiment is `MEASUREMENT_INVALID` and must not freeze.

Frozen `spec.falsifier` clause 3 likewise maps a certification failure
(cold or retrieval success_rate ≥ 0.95 on the relevant levels) to
`MEASUREMENT_INVALID`. The frozen primary `decision_rule.primary.C1` binds the
treatment to `spec.json.dynamic_range_certified == true`.

Therefore `status=MEASUREMENT_INVALID` is forced by the frozen contract before
any outcome is read, and `outcome=NOT_APPLICABLE` is the honest value: no
SUPPORTS/FALSIFIES conclusion about C-RESIDUAL-NOVELTY is available from this
transaction.

## 3. Diagnostic confirmation of the certificate failure

The diagnostic re-computation reproduced the certificate failure, exactly as the
predecessor `EXP-PRODUCT-37973256064` observed:

| Arm | success_rate | novelty 0.0 | 0.25 | 0.5 | 0.75 | cost_per_success |
|-----|--------------|-------------|------|-----|------|------------------|
| T-SPIDER-PARAM | 0.45 | 1.0 | 0.8 | 0.0 | 0.0 | 2.0 (null at L2/L3) |
| B-COLD-RE-DERIVE | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 2.0 |
| B-RETRIEVAL-SHAPED | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 2.0 |
| B-EMPTIED-REGISTRY | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 2.0 |
| PC-EXACT-REPLAY | 1.0 | 1.0 | — | — | — | 2.0 |

`cost_per_success` is the frozen composite
`(http_requests + verification_calls + repair_attempts) / success_count`.
Because every comparator task is a one-request GET that verifies on the first
try, every arm costs 2.0 composite units per success, and the treatment is
undefined (null) where it has zero successes. Observed certificate:
`cold_max_success_rate=1.0`, `retrieval_max_success_rate=1.0`,
`certified=false`. C1 fails; consequently C2–C5 were not evaluable (see
`derived/decision_rule_eval.json`, `primary_pass=false`).

## 4. Treatment support boundary (S4)

Induced mechanisms (`raw_evidence/induced_mechanisms.json`) carry support
regexes of the form `^<type>\-00[0-9]{1}$` for `item`, `user`, `order`,
`product`. That pattern accepts identifiers `001`–`009` only. Hence the treatment
resolves the training block `001-005` (novelty 0.0) and the first held-out block
`006-009` (novelty 0.25, 0.8 success), and refuses `011-020` (novelty 0.5 and
0.75, 0.0 success). This is a **support-boundary observation**, not evidence
about cost economics, and it is the mechanism behind the treatment's 0.45.

## 5. Shipped-path liveness threat (do not assume transfer)

The frozen design names the shipped parameterized
`distill_parameterized -> resolve -> execute` path as the treatment carrier.
The current shipped `src/spider/kernel.py` is git blob `cfec9866`, which lacks
`distill_parameterized`, `TrajectoryCounters`, `_support_accepts` and `rebind`
(`raw_evidence/shipped_kernel_probe.json`, `api_complete=false`). The audited
carrier is blob `b15ed848` (sha256 `718efa6a…`), which merge commit `5601ede3`
regressed away. The diagnostic therefore ran against a vendored copy of the
audited blob (`harness/audited_spider/`), not the shipped path. This run does
**not** certify the shipped carrier.

## 6. Interpretation (bounded)

- The frozen measurement transaction is invalid: the task bank has no dynamic
  range because cold and retrieval comparators solve the deterministic localhost
  substrate at ceiling, the same zero-headroom failure mode recorded in the
  parent experiment.
- The descriptive arm numbers are consistent with that reading: there is no
  cost-per-success headroom to compare, and the composite metric is saturated at
  2.0 for all arms.
- The treatment's collapse at novelty ≥ 0.5 is attributable to its induced
  support regex, not to a measured economic disadvantage.
- Per frozen prereg §9, a `MEASUREMENT_INVALID` outcome carries **no claim
  update**; the task bank must be redesigned and re-frozen. No claim was
  promoted.

## 7. Consequences

Neither the positive nor the negative product consequence frozen in `spec.json`
is triggered, because no primary condition was testable. C-RESIDUAL-NOVELTY
remains at its pre-existing registry status. The retained assets are the
descriptive cost/novelty task bank scaffold and the accounting surface, plus the
support-boundary and shipped-regression observations, all carried in
`result.json.unresolved` for DIRECTOR/AUDIT.

## 8. Reproduction

```
python3 research/experiments/EXP-PRODUCT-37982016598/harness/run_experiment.py
```

Artifacts and exact paths/hashes are enumerated in `result.json.artifacts`.
