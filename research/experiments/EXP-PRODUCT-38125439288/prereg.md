# EXP-PRODUCT-38125439288 preregistration

Lane: `product`. Claim: `C-PARAM-INHERIT` (registry status `EXPERIMENTAL`). Design contract: v2.
Parent handoff: `research/experiments/EXP-PRODUCT-37989728440/handoff.json` (sha256 `911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9`), disposition `SUPERSEDE` under the binding Global Research Director mandate in `request.json` (`allocation.action = CONTINUE`, `claim_id = C-PARAM-INHERIT`, authorized).

This preregistration is frozen before any outcome measurement. It is written for a fresh-context EXECUTE agent and a fresh-context AUDIT agent who will not see the author's reasoning. All identifiers (`PC1..PC7`, `PROMOTION-CERTIFICATE-B1-v2`, `B-PREINSTALL-KERNEL`, `N-LITERAL-PATH`, `N-NO-APPLICABLE`, `N-PREINSTALL-IMPORT`, `ARM-DIFFERENTIATION-CERTIFICATE-v1`) are stable and must be reused verbatim downstream. Thresholds and expected values in this file and in `spec.json` may not be edited after outcomes are visible.

## 1. Direction: why this experiment, and what it is not

The mandate asks whether the already-audited parameterized carrier can be installed **byte-identically** at the shipping path `src/spider/kernel.py` and demonstrated, through the shipped `spider` package, to pass a bounded positive/negative promotion certificate, so that promotion is enabled only after independent audit PASS, discharging blocker B1.

This experiment is **not** a re-run of the excluded dynamic-range economics certificate (EXP-PRODUCT-37973256064 / 37982016598 / 37989728440), and it is **not** a four-arm benchmark. It measures integration identity, unseen in-support identifier binding, negative selectivity and counter honesty through the public package, with no model and no network. The mechanism itself was already measured and audited; the unproven link is whether the frozen bytes can be installed and consumed as a durable, identity-pinned product capability.

Relationship to EXP-PRODUCT-37950607128 (honest disclosure): that experiment already ran the identical frozen certificate `ARM-DIFFERENTIATION-CERTIFICATE-v1` against an in-place install of this exact carrier and received an independent audit PASS, but it was frozen under design-contract v1 with **no** `artifact_hashes` (its provenance notes the kernel identities were "the documented preregistered substitute for a direct code-hash freeze"), and it did not require the pre-install kernel to fail the same certificate. The carrier was subsequently reverted (current `src/spider/kernel.py` is blob `cfec9866`). This experiment is therefore the v2-hash-bound re-establishment: it binds the carrier, the reused certificate driver and the fixture by sha256 in `freeze.json`, asserts the install identity before and after measurement, and requires the pre-install bytes to fail the certificate. It does not re-measure the mechanism economics and does not reopen the parent's bounded negative.

## 2. Frozen objects

| Object | Exact identity |
|---|---|
| Carrier source (treatment bytes) | `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`, sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`, git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` |
| Reused certificate driver | `research/experiments/EXP-PRODUCT-37950607128/harness/run_certificate.py`, sha256 `59895ddd9a85b6b3f75f9bfef6d39c423740679517df24505d26965918525970` |
| Reused certificate fixture | `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py`, sha256 `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf` (SYNTH-INDUCTION-BANK-v1, SEED=37950607128, 6 families x 4 induction observations) |
| Install target | `src/spider/kernel.py` (EXECUTE output, not a freeze artifact) |
| Pre-install baseline | git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50`, sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` at base_sha `15c00119031eb27d658101de411e33413585b308` and HEAD |
| Unchanged modules | `src/spider/models.py` = carrier `models.py` (sha256 `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78`); `src/spider/registry.py` = carrier `registry.py` (sha256 `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c`); `src/spider/__init__.py` (sha256 `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77`) |
| Regression test | `tests/test_kernel.py`, sha256 `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6` |

The installed carrier requires no change to `models.py` or `registry.py`: the carrier's vendored copies are byte-identical to the shipped modules and `src/spider/__init__.py` already imports `SpiderKernel` from `.kernel`.

## 3. EXECUTE procedure (frozen)

1. **Checkpoint.** Write `execution_checkpoint.json`: `pre_execute_sha` = `git rev-parse HEAD`; `pre_kernel_blob` = `git hash-object src/spider/kernel.py` (MUST equal `cfec9866...`); `pre_kernel_sha256` = sha256 of the file (MUST equal `46929b3a...`); `head_kernel_blob` = `git rev-parse HEAD:src/spider/kernel.py` (MUST equal `cfec9866...`).
2. **Materialize the frozen certificate.** `mkdir -p research/experiments/EXP-PRODUCT-38125439288/harness research/experiments/EXP-PRODUCT-38125439288/raw_certificate research/experiments/EXP-PRODUCT-38125439288/raw_fixture` (the raw directories are created up front so the step-6 shell redirect cannot fail); byte-copy the two frozen certificate files (section 2) into `harness/`; assert `sha256(copy)` equals the frozen artifact hash (`59895ddd...`, `b0ffcbba...`) and equals the corresponding `freeze.json.artifact_hashes` entry. If any copy hash differs, stop as MEASUREMENT_INVALID. Do not edit the copies. (Copying is required so that running the certificate writes this experiment's `raw_fixture/` and `raw_certificate/` instead of overwriting EXP-PRODUCT-37950607128's evidence.)
3. **Pre-install negative/ablation.** Run `PYTHONPATH=src python3 research/experiments/EXP-PRODUCT-38125439288/harness/run_certificate.py`, capturing stdout/stderr and exit code. Expected: non-zero exit with `ImportError` (the pre-install kernel lacks `_support_accepts`/`TrajectoryCounters`/`distill_parameterized`). Record the exit code and stderr as `N-PREINSTALL-IMPORT`. Also record `git show <pre_execute_sha>:src/spider/kernel.py | grep -c distill_parameterized` (MUST be 0).
4. **Install.** Byte-copy the frozen carrier to `src/spider/kernel.py` (no textual edits, no reformatting, no newline normalization).
5. **Identity (PC1, pre-measurement).** Assert `sha256(src/spider/kernel.py)` == `718efa6a...`, `git hash-object src/spider/kernel.py` == `b15ed848...`, and equality with `freeze.json.artifact_hashes` for the carrier path.
6. **Certificate.** Run `PYTHONPATH=src python3 <harness>/run_certificate.py > <raw_certificate>/certificate_stdout.json`, capture exit code, and read `<raw_certificate>/arm_differentiation_certificate.json`. Do not modify its outputs.
7. **Evaluate PC2..PC6** from the certificate JSON exactly as defined in `spec.json.decision_rule` (and restated in section 4). No threshold may be changed.
8. **Regression (PC7).** Run `PYTHONPATH=src python3 -m unittest tests.test_kernel -v`; record exit code and output.
9. **Re-assert PC1 after measurement.** Recompute the installed sha256 and git blob and confirm they still equal the carrier identity; confirm no other file changed by recording `git status --porcelain`.
10. **Write outputs.** `result.json`, `report.md`, `provenance.json`, and raw/derived artifacts, keeping RAW EVIDENCE (file hashes, certificate JSON, stderr, test output), OBSERVATIONS (per-check PASS/FAIL), DERIVED MEASUREMENTS (`certificate_overall`, rates) and INTERPRETATION separate. On FAIL, revert `src/spider/kernel.py` to the recorded pre-install bytes; on PASS, leave the carrier installed (promotion remains conditioned on AUDIT PASS).

## 4. Frozen promotion certificate `PROMOTION-CERTIFICATE-B1-v2`

The certificate is the conjunction of seven checks, each PASS/FAIL, each evaluated independently (no short-circuit). All inputs are either bound files, shell/hash command outputs, the reused certificate's JSON, or the regression exit code. No post-freeze-authored code may alter any expected value.

- **PC1-INSTALL-IDENTITY** — pre-install blob `cfec9866` / sha256 `46929b3a...` recorded; installed `sha256 == 718efa6a...` AND `git hash-object == b15ed848...` AND `== freeze.json.artifact_hashes` entry; re-asserted after measurement.
- **PC2-FIXTURE-CERTIFICATE** — reused `ARM-DIFFERENTIATION-CERTIFICATE-v1` reports `certificate_overall == "PASS"` and each of `AD-POSITIVE-ROUNDTRIP`, `AD-NEGATIVE-ROUNDTRIP`, `AD-TREATMENT-CONTRAST`, `PC-ACCOUNTING-FIDELITY`, `AD-IDENTITY-BINDING`, `B-LITERAL-KERNEL` has `pass == true`.
- **PC3-UNSEEN-IDENTIFIER-BINDING** — `AD-POSITIVE-ROUNDTRIP.n_pass == n_cases == 6`; every case `resolution_status == "EXECUTABLE"`, `bound_action != null`, `binding_correct == true`, `execution_status_200 == true`, `verify_true == true`, `slot_count_match == true`, `inferred_slot_count >= 1`; `in_support_executable_rate == 1.0`; `held_out_binding_correct_rate == 1.0`. Confidence `0.9` is entailed: `resolve()` returns EXECUTABLE only at confidence `>= 0.8`, `distill_parameterized` assigns `0.9` (self-verified) or `0.5`, literal `distill` assigns `0.5`, and the recorded non-empty `inferred_slots` identify the parameterized mechanism; therefore any EXECUTABLE positive case has confidence exactly `0.9`.
- **PC4-NEGATIVE-TAXONOMY** — `AD-NEGATIVE-ROUNDTRIP.refusal_rate == 1.0` and each of `out_of_support_refusal_rate`, `missing_param_refusal_rate`, `wrong_intent_refusal_rate` `== 1.0`; every `out_of_support*` / `missing_param` case is non-`EXECUTABLE` with `bound_action == null` and a non-empty reason; every `wrong_intent` case is exactly `ResolutionStatus.UNKNOWN` with `bound_action == null` and a non-empty reason (this is the mandated no-applicable-mechanism case).
- **PC5-COUNTER-HONESTY** — `PC-ACCOUNTING-FIDELITY.pass == true`; `inherited_path_counter_increments.pass == true` with `observed == {"retrieval_calls": 3, "verification_calls": 2, "repair_attempts": 1}` over the frozen resolve/verify/refuse/rebind/verify/resolve exercise sequence; `model_counters.model_calls == 0` and `model_tokens == 0`. The certificate calls resolve exactly once and verify exactly once per positive case with no rebind/fallback, so the per-positive-execution inherited-path increments are `retrieval_calls=1, verification_calls=1, repair_attempts=0` (established from the PC1-bound driver semantics, since `run_positive_roundtrip` constructs its kernel with `counters=None`). The seeded scripted trajectory is labeled injected and is excluded from the honest-counter claim.
- **PC6-ABLATION-SENSITIVITY** — the byte-identical driver exits non-zero with `ImportError` against the recorded pre-install bytes (the first missing symbol is `TrajectoryCounters`, alongside `_support_accepts`); `git show <pre_execute_sha>:src/spider/kernel.py` contains `0` occurrences of `distill_parameterized`; `B-LITERAL-KERNEL.pass == true`; `AD-TREATMENT-CONTRAST.pass == true` (contrast_rate > 0 and the degenerate variant detected).
- **PC7-UNIT-REGRESSION** — `PYTHONPATH=src python3 -m unittest tests.test_kernel -v` exits `0`.

Decision: `PROMOTION_READY` iff PC1..PC7 all PASS, and then `certificate_overall = PASS`; otherwise `NOT_PROMOTION_READY` with `certificate_overall = FAIL` and every failing check plus raw evidence recorded. Promotion itself is not self-authorized: it is enabled only by an independent AUDIT PASS.

Both branches are reachable (see `spec.json.freeze_eligibility.decision_rule_reachability`). A PC3/PC4 failure means the shipped package cannot consume the carrier; a PC6 failure means the positive is not sensitive to the parameterized path.

## 5. Controls (stable identifiers)

- `PC-AD-POSITIVE-ROUNDTRIP` — positive control, in-certificate, expected 6/6 (inherited 1.0).
- `N-LITERAL-PATH` = in-certificate `B-LITERAL-KERNEL` — ablation, expected 0 EXECUTABLE on held-out cases.
- `N-NO-APPLICABLE` = in-certificate `wrong_intent` cases — expected exactly `UNKNOWN`, null bound action.
- `N-PREINSTALL-IMPORT` — driver run against pre-install blob `cfec9866`, expected non-zero exit with `ImportError`.
- `B-RETRIEVAL-SHAPED` = in-certificate `AD-TREATMENT-CONTRAST` comparator — expected treatment action != comparator.
- `B-PREINSTALL-KERNEL` — baseline identity blob `cfec9866`, expected to lack `distill_parameterized`/`_support_accepts`/`TrajectoryCounters`/`rebind`.
- `B-AUDITED-CERT-ANCHOR` — external consistency context: EXP-PRODUCT-37950607128 audit PASS on the identical carrier; disagreement is a validity threat to report, not re-measure.

## 6. Validity threats and mitigations

- **Instrument reuse / not a fresh measurement of the mechanism**: the certificate is reused from EXP-PRODUCT-37950607128. This is disclosed; the new object is the v2 hash binding, the install-identity assertion and the pre-install ablation. The certificate is not treated as new mechanism evidence.
- **Support-boundary over-generalization** (carried from the parent): held-out identifiers lie inside the support grammar induced from the induction values, so this is an unseen in-support binding result, not free-form support generalization. Disclosed, not hidden.
- **Ceiling baseline**: the positive control is expected at 1.0; its ceiling status is disclosed, and the nulls (literal 0.5, UNKNOWN, ImportError) provide the floor that keeps the held-out check discriminating.
- **Copy drift**: EXECUTE executes copies of the frozen certificate files; byte-identity is asserted against frozen hashes before execution, and any mismatch is MEASUREMENT_INVALID, not a negative.
- **Import provenance**: the driver imports `spider` from `<repo>/src` and never imports the parent's `audited_spider`; a mis-import would fail PC1/PC2 and is itself informative.
- **Confidence 0.9 is an entailment, not an emitted field**: the certificate JSON does not record confidence; PC3's `inferred_slot_count >= 1` identifies the parameterized mechanism and the PC1-bound carrier arithmetic forces confidence exactly 0.9 (EXECUTABLE requires `>= 0.8`; the parameterized path yields 0.9, the literal path 0.5). AUDIT must read the PC1-bound carrier bytes to re-derive this; the entailment is valid only while PC1 holds.
- **Determinism**: `fixture.SEED = 37950607128`, stdlib only, no wall-clock, no network, no credential; the certificate is reproducible. EXECUTE records the interpreter version, because support inference depends on recorded Python 3.12 `re.escape` semantics; a version change is a measurement-environment change and must be recorded, not silently accepted.
- **Governance residual**: the freeze script binds `freeze_artifacts` by sha256 but does not itself execute the certificate; binding is achieved by making the certificate the frozen decision rule plus the independent AUDIT requirement. This residual is disclosed in `report.md`, not claimed as automatic enforcement.

## 7. Consequences

- **Positive (`PROMOTION_READY` + audit PASS)**: the Director may set `promote_to_product=true` and advance `C-PARAM-INHERIT` (EXPERIMENTAL) toward `PRODUCT_CORE`; the shipped package exposes the parameterized path; `B1` is discharged; the C-LLM-INHERIT / residual-novelty economics thread becomes constructible. Claim ceiling stays bounded to unseen in-support identifier binding on the deterministic credential-free REST class with `model_calls=0` by construction.
- **Negative (`NOT_PROMOTION_READY` or audit not PASS)**: no promotion; `C-PARAM-INHERIT` stays `EXPERIMENTAL`; `B1` remains open; revert `src/spider/kernel.py` to the recorded pre-install bytes; record the exact failing checks so the next mandate targets the integration defect. Criteria are not weakened.

## 8. Inherited state preserved from the parent handoff (four-way)

- **established**: frozen-input/carrier integrity; the deterministic run is measurement-valid; the parameterized path is causally necessary on the deterministic substrate-class tasks (`B-LITERAL-KERNEL` 0.0 vs `PC-EXACT-REPLAY` 1.0); the bounded substrate-class economics negative; the governance fact that the v1 freeze script did not enforce a certificate gate.
- **rejected** (bounded to that substrate class and arm design): a certified dynamic range on the mandatory-discovery deterministic REST class; a counter-only treatment advantage there; the latency-inclusive metric as a discriminating instrument; the asserted `dynamic_range_certified` enforcement.
- **unknown**: whether any credential-free deterministic substrate can show a dynamic range for that arm design; whether asymmetric/amortized discovery would let the treatment save work; endpoint availability for the external benchmark; whether the kernel's support predicate on free-form values is a defect.
- **do_not_assume**: cold/retrieval 1.0 is a ceiling, not evidence inheritance lacks value; the treatment's 40/40/C3/C4 is not work compression; the shipped kernel still lacks the parameterized path (blob `cfec9866`); the old certificate gate was enforced; do not re-run the excluded economics certificate; do not promote the parent packet's scaffolding; the substrate workaround is not a support-generalization result; `model_calls=0` is by construction, not a measured zero.

This design supersedes the parent's `next_question` (an endpoint-gated four-arm benchmark) only because the Global Research Director issued a binding NEW mandate for the B1 promotion transaction. It does not reopen the parent's rejected hypotheses and does not resume the parked benchmark.

## 9. Freeze eligibility

All six v2 checks are PASS with reasons and evidence refs in `spec.json.freeze_eligibility`. `freeze_artifacts` binds the reused certificate driver and fixture, the carrier, the vendor-equal models/registry, the package entrypoint and the regression test. `src/spider/kernel.py` is intentionally excluded because EXECUTE overwrites it with the byte-identical carrier; its pre-install identity (`cfec9866` / `46929b3a...`) is pinned in the design and re-asserted at run time.

## 10. Freeze protocol

This preregistration and `spec.json` are frozen by `scripts/freeze_experiment.py` only after an independent `design_review.json` returns `status = PASS`. After freeze they are immutable; EXECUTE may not re-design after outcomes are visible. EXECUTE adds `result.json`, `report.md`, `provenance.json` and raw/derived artifacts; AUDIT adds `audit.json`; DIRECTOR adds `verdict.json` and `handoff.json`. The certificate criteria in section 4 may not be edited at any later stage.
