# EXP-PRODUCT-37999047472 preregistration

- `experiment_id`: `EXP-PRODUCT-37999047472`
- `lane`: product
- `design_contract_version`: 2
- `claim_ids`: `["C-PARAM-INHERIT"]`
- `request.base_sha`: `e35fccd0e620d4f564050a90c632ce6a6f89d037`
- Director mandate: `REOPEN` of `C-PARAM-INHERIT` in the `product` lane, cycle `37998281030`, with `parent_handoff_disposition = SUPERSEDE`.

DESIGN emits `spec.json` and this preregistration only. No confirmatory/outcome-bearing measurement of the frozen design is executed at DESIGN. The one execution at DESIGN is the mandatory v2 **pre-freeze treatment-liveness satisfiability probe** described in section 7; it is a gate, not a scientific result.

---

## 1. Objective and the decision this experiment changes

The Global Research Director's mandate asks a single question: can the already-audited parameterized-inheritance capability be made **DURABLE and PROMOTABLE in the shipping kernel path** (`src/spider`), gated by a pre-freeze arm-differentiation certificate, unit tests, an accounting check, and a kernel identity bound at freeze, so the carrier actually **lands in main through the pinned Product promotion path without manually copying experiment code**?

The decision this changes is a product/shipping decision that has repeatedly blocked the program:

1. `research/claims/registry.json`/Codex place `C-PARAM-INHERIT` at EXPERIMENTAL: the mechanism has been shown live and causally attributable, with audit PASS, on a real credential-free substrate (`EXP-PRODUCT-37973256064`) and certified on the frozen synthetic bank (`EXP-PRODUCT-37950607128`).
2. Yet **no** packet has `promote_to_product = true`, and the shipped `src/spider/kernel.py` still exposes only literal `distill()` at confidence 0.5 with **no** `distill_parameterized()`. The audited carrier has never been installed at the shipping position.
3. Therefore every downstream benchmark that needs a shipped treatment (the four-arm `C-LLM-INHERIT` benchmark; first-party `C-PRODUCT-ECON` economics) is blocked on **readiness condition (1): a shipped carrier**.

This experiment installs the audited carrier at the shipping position and certifies, on the **installed shipped package**, that the inherited parameterized round trip fires and that negatives are refused, with honest accounting and a bound identity. On success the `src/`+`tests/` delta is promotable by `.github/workflows/product-promote.yml` — the pinned promotion path — with no manual copying of experiment code into main.

**"Without manually copying experiment code" interpretation (recorded so it is not ambiguous).** EXECUTE, acting inside the Product lane's granted `src`/`tests` scope, writes the audited carrier bytes to `src/spider/kernel.py`. That is the *experiment* installing its audited treatment; it is not a human hand-editing `main`. The phrase targets the **landing mechanism**: the delta reaches `main` only via `product-promote.yml`, which applies the audited code-root delta and re-runs `compileall`, `validate_repo.py` and the canonical unit-test discovery before committing. No manual main-branch copy is part of this design.

## 2. Inheritance from `request.json.parent_handoff` (preserved four-way distinction)

The exact parent is `research/experiments/EXP-PRODUCT-37989728440/handoff.json` (`sha256 911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9`). Per the mandate, `parent_handoff_disposition = SUPERSEDE`: the parent's `next_question` (run the four-arm `C-LLM-INHERIT` benchmark now) is **not** this experiment's objective; the Director's target claim and question in `request.json.director_mandate` are binding. The parent's `carry_forward` is preserved as inherited scientific state, not as an agenda:

- **established (inherited, relied on):** the treatment carrier is vendored byte-identically to git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` (`sha256 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`); the shipped `src/spider/kernel.py` is unchanged blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` (`sha256 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`); the kernel's parameterized path is causally necessary on the deterministic bank (`B-LITERAL-KERNEL` 0.0 vs exact replay 1.0); `C-PARAM-INHERIT` is at EXPERIMENTAL.
- **rejected (inherited, bounded; not reopened here):** the mandatory-discovery deterministic credential-free REST substrate cannot produce a certified dynamic range (three consecutive failures: `EXP-PRODUCT-37973256064`, `EXP-PRODUCT-37982016598`, `EXP-PRODUCT-37989728440`); the latency-inclusive `cost_per_success` is a non-discriminating instrument on that substrate; the claim that the pre-2.0 freeze step enforced a certificate is rejected.
- **unknown (inherited, untouched):** whether any credential-free deterministic substrate can exhibit dynamic range; whether asymmetric/amortized discovery would let the treatment save work; whether the external model endpoint will be provisioned; whether support-predicate application to free-form payloads is a defect.
- **do_not_assume (inherited, honored):** do not assume `src/spider/kernel.py` contains the parameterized path (it does not — the literal-only `cfec9866` baseline is explicit in `spec.json.baselines.B-SHIPPED-PRE-INSTALL`); do not treat the deterministic substrate's 1.0 correctness ceiling as evidence about inheritance value; do not treat the parent packet's 40/40 or its noise-driven C3/C4 as work compression; do not promote the parent packet's scaffolding.

**Scope discipline honored:** the parent's `do_not_assume` says "do not re-run this certificate or its two predecessors" — that prohibition is on the **mandatory-discovery deterministic REST certificate** (`B-COLD-RE-DERIVE` vs `B-RETRIEVAL-SHAPED` on the localhost REST bank). This experiment does **not** re-run it. It runs the structurally different **arm-differentiation certificate** (positive parameterized round trip vs known-negative refusal) from `EXP-PRODUCT-37950607128`, now targeted at the **installed shipping package** — which is precisely what the Director mandate requires.

## 3. Treatment, identity rule, and the exact install

**Treatment (T-SHIPPED-PARAM).** The shipping package `spider` with `src/spider/kernel.py` replaced **byte-for-byte** by the audited carrier `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`. No reformatting, no re-implementation, no semantic edits. The carrier's `models.py` and `registry.py` are **already byte-identical** to the shipped `src/spider/models.py` and `src/spider/registry.py` (both `338aaf4d…` and `51fb440d…` respectively), so the only production module that changes is the kernel.

**Identity rule (gate; decision_rule C1).** After install:

```
sha256(src/spider/kernel.py) == 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72
git hash-object(src/spider/kernel.py) == b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796
```

The kernel identity is therefore **bound at freeze** through the frozen carrier artifact (section 6): the freezer hashes the carrier source into `freeze.json.artifact_hashes`, and the installed kernel is required to equal that hash. `src/spider/kernel.py` is deliberately **not** itself a freeze artifact (EXECUTE must change it); its pre-install baseline is recorded for reversion.

**Shipped public surface unchanged.** `src/spider/__init__.py` is bound and must remain byte-identical (`3d173722…`). `TrajectoryCounters` remains importable from `spider.kernel` (as the audited packets used it); adding a package-level re-export is explicitly **out of scope** and non-gating, so the shipped public surface does not drift as part of this experiment.

**Baseline (B-SHIPPED-PRE-INSTALL).** The pre-install kernel (`cfec9866…`/`46929b3a…`) has no `distill_parameterized` and cannot execute the inherited parameterized round trip. The proof that the shipped kernel currently lacks the path is part of the record: `hasattr(SpiderKernel, "distill_parameterized") == False` on the unmodified tree.

## 4. Fixture

Reconstructed by the frozen executable `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py` (`sha256 b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf`): **SYNTH-INDUCTION-BANK-v1**, `SEED = 37950607128`, six families (`F1-PATH-ID`, `F2-QUERY-ID`, `F3-BODY-FIELD`, `F4-HEADER-FIELD`, `F5-TWO-SLOT`, `F6-NOISE-STRESS`), four induction observations per family, one held-out parameter set per family, four varying noise fields, and a deterministic credential-free `fixture_execute`. EXECUTE copies `fixture.py` into its own harness directory byte-identically and records the serialized-bank sha256.

## 5. Certificate checks (frozen identities and thresholds)

The certificate is `ARM-DIFFERENTIATION-CERTIFICATE-v2`. Identifiers are reused from the audited `EXP-PRODUCT-37950607128` certificate so AUDIT and DIRECTOR can refer to the same objects; the object certified here is the **installed shipping package**, extended with identity and regression checks.

| check id | type | frozen pass condition |
|---|---|---|
| `AD-POSITIVE-ROUNDTRIP` | positive control | 6/6 families: resolution `EXECUTABLE`, `bound_action` non-null, bound identifier == expected held-out identifier, `fixture_execute` status 200, `verify` true; `in_support_executable_rate == 1.0` and `held_out_binding_correct_rate == 1.0` |
| `AD-NEGATIVE-ROUNDTRIP` | negative control | 24/24 negatives refused: non-`EXECUTABLE`, `bound_action == null`, non-empty reason; per-category refusal rates (out-of-support, missing-parameter, wrong-intent) all `1.0` |
| `AD-TREATMENT-CONTRAST` | treatment vs comparator | real contrast_rate > 0.0 on ≥1 family, with treatment = the re-bound parameterized action and comparator = `B-RETRIEVAL-SHAPED` nearest-observation literal action |
| `NC-ZERO-CONTRAST-TREATMENT` | degenerate null | comparator-vs-itself contrast_rate == 0.0 and `degenerate_variant_detected == true` |
| `PC-ACCOUNTING-FIDELITY` | accounting | (a) seeded 5-step scripted trajectory max relative error ≤ 0.01 over all eight counters; (b) real inherited-path exercise increments `retrieval_calls == 3`, `verification_calls == 2`, `repair_attempts == 1`; injected `model_calls`/`model_tokens` event is labeled and made no model call |
| `B-LITERAL-KERNEL` | ablation / baseline | literal `distill()` (confidence 0.5 < `min_confidence` 0.8) yields `held_out_executable_count == 0` |
| `AD-IDENTITY-BINDING` | identity gate | installed kernel file sha256 == `718efa6a…` and git blob == `b15ed848…`; pre-install baseline blob `cfec9866…` recorded; pre/post differ |
| `PKG-TESTS` | regression gate | pre-existing `tests/test_kernel.py` passes, and the EXECUTE-added shipping-path unit tests pass, under the canonical `PYTHONPATH=<src> python -m unittest discover -s tests -v` |

## 6. Freeze artifacts and identities

All paths are repository-relative and must exist at freeze. The deterministic freezer hashes them into `freeze.json.artifact_hashes`; they are immutable for this transaction.

| # | path | sha256 (at DESIGN) | role / rationale |
|---|---|---|---|
| 1 | `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` | treatment source **and** required installed-kernel identity target |
| 2 | `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` | carrier import dependency (== shipped) |
| 3 | `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` | carrier import dependency (== shipped) |
| 4 | `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py` | `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf` | SYNTH-INDUCTION-BANK-v1 task-bank source |
| 5 | `src/spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` | shipped import dependency |
| 6 | `src/spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` | shipped import dependency |
| 7 | `src/spider/__init__.py` | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` | shipped public surface (frozen unchanged) |
| 8 | `tests/test_kernel.py` | `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6` | pre-existing regression suite (frozen so it cannot be weakened) |

`src/spider/kernel.py` is intentionally absent from this list because EXECUTE replaces its content; its required post-install identity is pinned by C1, and its pre-install baseline (`46929b3a…`/`cfec9866…`) is recorded in `spec.json.baselines.B-SHIPPED-PRE-INSTALL`. The certificate runner and raw evidence written by EXECUTE are derived artifacts, not interpretation dependencies.

## 7. Pre-freeze treatment-liveness probe (mandatory v2 gate)

Because this is a v2 **Product** experiment containing a **SPIDER treatment arm** targeting inheritance, treatment liveness must be demonstrated **before freeze**. DESIGN executed a cheap, non-outcome-bearing satisfiability probe:

**Construction.** A sandbox package was assembled at `/tmp/opencode/probe37999047472/src/spider/` consisting of the frozen carrier's `kernel.py`, `models.py`, `registry.py` plus a minimal `__init__.py` — i.e. the frozen carrier laid at the shipping kernel position. The probe driver is `/tmp/opencode/probe37999047472/probe.py` (`sha256 6ec80584880ead401cde900944844bf63713101aa4bc6d4ea560ff251a5316e2`); its recorded output is `/tmp/opencode/probe37999047472/probe_results.json` (`sha256 a1bf08f9e90d1595968feb25c51aebc03e0b5a6158bcb7766c582a9504c1c34a`); `overall = "PASS"`.

**Reproduction (durable method, independent of the /tmp file).**

```bash
# 1. assemble the sandbox shipping package from the frozen artifacts
mkdir -p /tmp/probe/src/spider
cp research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py  /tmp/probe/src/spider/kernel.py
cp research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py  /tmp/probe/src/spider/models.py
cp research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py /tmp/probe/src/spider/registry.py
printf 'from .kernel import SpiderKernel, TrajectoryCounters\nfrom .models import Mechanism, Observation, Resolution, ResolutionStatus\n' > /tmp/probe/src/spider/__init__.py
# 2. run the certificate logic (positive/negative/contrast/accounting/literal/identity)
#    using fixture.py from the frozen artifact with PYTHONPATH=/tmp/probe/src
# 3. run the canonical regression suite against the sandbox package
PYTHONPATH=/tmp/probe/src python -m unittest discover -s tests -v
```

**Observed (all PASS).**

| check | observed |
|---|---|
| `AD-POSITIVE-ROUNDTRIP` | PASS — `in_support_executable_rate = 1.0`, `held_out_binding_correct_rate = 1.0` (6/6) |
| `AD-NEGATIVE-ROUNDTRIP` | PASS — `refusal_rate = 1.0` (24/24 refused, null actions, reasons) |
| `AD-TREATMENT-CONTRAST` | PASS — real `contrast_rate = 1.0`; degenerate variant detected |
| `PC-ACCOUNTING-FIDELITY` | PASS — scripted `max_relative_error = 0.0`; increments `retrieval_calls = 3`, `verification_calls = 2`, `repair_attempts = 1` |
| `B-LITERAL-KERNEL` | PASS — `held_out_executable_count = 0` |
| `AD-IDENTITY-BINDING` | PASS — sandbox kernel sha256 == `718efa6a…`, blob == `b15ed848…` |
| `PKG-TESTS` | PASS — `tests/test_kernel.py` green under the canonical discovery invocation |

**Determinism disclosure.** Because the installed bytes are pinned to the frozen carrier, this certificate is deterministic; the probe's values are pre-computable and are **not** new causal evidence about web behavior. EXECUTE's confirmatory measurement is the same certificate run against the **actual installed `src/spider` package**. Any deviation between the probe expectation and the EXECUTE observation is a measurement-invalidity signal (or `BLOCKED` if install is impossible); it must never be silently accepted as a pass.

## 8. EXECUTE procedure (frozen)

1. Record the execution base (`scripts/record_execution_base.py` runs automatically before EXECUTE; `execution_checkpoint.json.pre_execute_sha` is required by the promotion workflow).
2. Copy the frozen carrier `kernel.py` byte-identically to `src/spider/kernel.py`. Do not touch any frozen artifact (section 6).
3. Add new unit tests (e.g. `tests/test_ship_kernel.py`) covering: positive parameterized round trip, known-negative refusals with reasons/null actions, and counter increments. Do **not** modify `tests/test_kernel.py`.
4. Write the certificate runner into the experiment directory (`harness/`) and reconstruct `SYNTH-INDUCTION-BANK-v1` into `raw_fixture/`; write the certificate and accounting trace into `raw_certificate/`, recording sha256 for every artifact. **Critical import rule:** the runner must resolve the `spider` package exclusively from `REPO_ROOT/src` — the *installed* shipping package — and must never add the frozen carrier's directory or any vendored copy to `sys.path`. Otherwise `AD-IDENTITY-BINDING` and every behavioral check would measure the vendored copy instead of the installed kernel, silently invalidating C1. The fixture import (`import fixture`) may come from the runner's own harness directory.
5. Run the certificate against the installed package and the canonical regression invocation.
6. Verify identity C1 and all of C1–C7; write `result.json`, `report.md`, `provenance.json` with the exact required shapes, preserving control ids and artifact hashes.
7. Record the promotion recommendation in `result.json` interpretation fields; the actual `promote_to_product` decision belongs to the DIRECTOR verdict.

Raw evidence, observations, derived measurements, and interpretation must remain separated. Measurement failure must be recorded as `status = MEASUREMENT_INVALID` or `BLOCKED`, never as a scientific negative.

## 9. Decision mapping (frozen)

| condition | branch |
|---|---|
| C1 identity binding | installed kernel == frozen carrier hash and all frozen artifacts unchanged |
| C2 positive roundtrip | 6/6 `AD-POSITIVE-ROUNDTRIP` |
| C3 negative roundtrip | 24/24 `AD-NEGATIVE-ROUNDTRIP`, null actions, reasons |
| C4 treatment contrast | real contrast > 0 and degenerate zero-contrast detected |
| C5 accounting fidelity | scripted max rel err ≤ 0.01 and increments {3, 2, 1} |
| C6 literal control | 0 EXECUTABLE |
| C7 promotability/tests | regression suite + added tests pass; `compileall` clean |

- **SUPPORTS** = C1–C7 all PASS → `status = COMPLETE`; capability installed and promotion-ready; recommend `promote_to_product = true`.
- **FALSIFIES** = C2 fails, or C7 fails after a C1-passing byte-exact install → the audited carrier is not promotable in its audited form.
- **MEASUREMENT_INVALID** = C1 fails (identity/artifact violation) or C3/C4/C5/C6 fails → instrumentation invalid; do not promote; repair and re-run under a new packet.
- **BLOCKED** = infrastructure/scope failure independent of the hypothesis; never recorded as FALSIFIES.

## 10. Validity threats and mitigations

- **Predetermined certificate.** Mitigated by disclosure (section 7) and by binding the measurement to the actual installed package, with the promotion checks (`compileall`, `validate_repo.py`, canonical tests) as genuine integration gates.
- **Unbound mutable code.** Mitigated by eight frozen artifacts plus the C1 identity pin on the one deliberately mutable module.
- **Weakened tests.** Mitigated by binding `tests/test_kernel.py` and adding new tests in a separate file.
- **Identity drift (reformatting/semantic edits).** Mitigated by byte-for-byte install and sha256/blob equality.
- **Promotion divergence.** `product-promote.yml` computes the delta from `pre_execute_sha` and `git apply --index --3way` onto current main; divergence in `src/spider` since the base can hard-stop promotion. This is an operational dependency, recorded under `unresolved`, not a scientific falsifier.
- **Residue on rejection.** Mitigated by `revert_product_reject.py` (reverts the code-root delta to `pre_execute_sha`), restoring `B-SHIPPED-PRE-INSTALL`.
- **Governance regression.** The v2 freezer (`scripts/freeze_experiment.py`) now requires the six `freeze_eligibility` checks and a PASS `design_review.json`; the prior v1 defect where a certificate gate was asserted but not enforced cannot recur in this packet.

## 11. Product consequences

- **Positive.** The audited carrier is installed byte-identically at the shipping position, the certificate plus unit tests pass on the shipped package, so the DIRECTOR may advance `C-PARAM-INHERIT` to `PRODUCT_CORE` with `promote_to_product = true` (Product lane + PASS audit required). `product-promote.yml` then lands only the audited `src/`+`tests/` delta in `main` after `compileall`/`validate_repo`/unit tests, closing readiness condition (1) for the four-arm `C-LLM-INHERIT` benchmark and for first-party `C-PRODUCT-ECON`.
- **Negative.** No promotion; revert to `B-SHIPPED-PRE-INSTALL`; `C-PARAM-INHERIT` retains EXPERIMENTAL. FALSIFIES → bounded integration-defect diagnosis before any re-port. MEASUREMENT_INVALID → repair the arm-differentiation instrumentation and re-run; the capability is not judged.

## 12. Cost and expected information gain

Deterministic, standard-library-only, credential-free; seconds of compute; no model/browser/network/GPU. Program-level information gain is high: this is the first packet designed to convert two audit-PASS `C-PARAM-INHERIT` packets into a durable, promoted, shipped state and to exercise the pinned Product promotion path end-to-end. Claim-level information gain is bounded and disclosed: because the installed bytes are pinned to the frozen audited carrier, the certificate is deterministic and was already demonstrated as the pre-freeze liveness probe; the residual uncertainty tested is integration/identity/regression/promotion, which is the actual repeated blocker.
