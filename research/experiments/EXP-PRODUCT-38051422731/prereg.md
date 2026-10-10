# EXP-PRODUCT-38051422731 preregistration

Lane: product. Design contract version: 2.
Claim under test: `C-PARAM-INHERIT`.
Binding mandate: Director allocation on cycle `38051032552`, `action=CONTINUE`, `parent_handoff_disposition=SUPERSEDE`, question as recorded in `request.json#director_mandate.allocation.question`.

## 1. Objective

Determine whether the already-audited parameterized-inheritance capability can be **landed as a durable, promotable mechanism on the SHIPPED kernel path** (`src/spider`), rather than remaining an experiment-local module, so that it is carried onto `main` by the pinned Product promotion path (`product-promote.yml`) and satisfies program readiness condition (1).

This is not a re-run of the bounded substrate-class negative (EXP-PRODUCT-37989728440) and not the forbidden four-arm C-LLM-INHERIT dynamic-range benchmark. It is the carrier-landing certification the Director ranked as the #1 blocker.

## 2. Treatment and comparator

- **Treatment (T):** `src/spider/kernel.py` is replaced byte-identically by the frozen audited carrier
  `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`
  (sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`, git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`).
  `src/spider/models.py`, `src/spider/registry.py` and `src/spider/__init__.py` stay at their frozen shipped bytes.
- **Comparator / pre-treatment baseline (B-SHIPPED-PRE-INSTALL):** the shipped kernel at `pre_execute_sha`
  (git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50`), which has no `distill_parameterized`, `TrajectoryCounters`, `_bind` or `_support_accepts`.
- **Floor ablation (B-LITERAL-KERNEL):** the post-install literal `distill()` path (confidence 0.5, below the 0.8 execution threshold) on the same frozen bank; must yield exactly 0 held-out executables.
- **Non-gating comparator (B-RETRIEVAL-SHAPED):** `fixture.retrieval_comparator_action` (nearest-observation literal retrieval, no model/network), used by the contrast check.

## 3. Instrument

The frozen instrument is `ARM-DIFFERENTIATION-CERTIFICATE-v1`.

- Runner: `research/experiments/EXP-PRODUCT-37950607128/harness/run_certificate.py`
  (sha256 `59895ddd9a85b6b3f75f9bfef6d39c423740679517df24505d26965918525970`).
- Fixture / task bank: `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py`
  (sha256 `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf`), reconstructing `SYNTH-INDUCTION-BANK-v1` (seed 37950607128).

EXECUTE byte-copies both files into `research/experiments/EXP-PRODUCT-38051422731/harness/`, replaces `src/spider/kernel.py` with the carrier, and runs the copied runner so that raw evidence lands in this experiment's `raw_fixture/` and `raw_certificate/` directories. The runner's embedded `experiment_id` field (`EXP-PRODUCT-37950607128`) is the instrument's origin and must not be rewritten; this packet's own `experiment_id` is authoritative and the origin is disclosed in `provenance.json`.

## 4. Fixture and controls (stable identifiers)

- Families (6): `F1-PATH-ID`, `F2-QUERY-ID`, `F3-BODY-FIELD`, `F4-HEADER-FIELD`, `F5-TWO-SLOT`, `F6-NOISE-STRESS`.
- Positive control: `AD-POSITIVE-ROUNDTRIP` (6/6 families: slot count, EXECUTABLE, non-null correctly bound action, fixture status 200, verify true).
- Negative control: `AD-NEGATIVE-ROUNDTRIP` (refusal_rate 1.0 over 24 cases: 2 `missing_param`, 16 `out_of_support`, 6 `wrong_intent`; refusal = non-EXECUTABLE AND null action AND non-empty reason).
- Null / degenerate control: `NC-ZERO-CONTRAST-TREATMENT` (reported inside `AD-TREATMENT-CONTRAST.degenerate_variant`): comparator actions substituted for treatment actions ⇒ degenerate `contrast_rate == 0.0` and `degenerate_variant_detected == true`.
- Contrast (non-gating comparator): `AD-TREATMENT-CONTRAST` real `contrast_rate == 1.0`.
- Accounting: `PC-ACCOUNTING-FIDELITY` (`counter_max_relative_error <= 0.01`; declared inherited-path increments `{retrieval_calls: 3, verification_calls: 2, repair_attempts: 1}`).
- Identity: `AD-IDENTITY-BINDING`.
- Floor: `B-LITERAL-KERNEL` (`held_out_executable_count == 0`).
- Regression: `PROMOTABILITY-REGRESSION` (`compileall src`, `unittest discover -s tests`, `scripts/validate_repo.py` all exit 0).

## 5. Decision rule

Checks `C1..C7` and the precedence/outcome mapping are defined verbatim in `spec.json#decision_rule`. Summary:

- `C1 AD-IDENTITY-BINDING` — MEASUREMENT_INVALID gate.
- `C2 AD-POSITIVE-ROUNDTRIP` — FALSIFIES gate.
- `C3 AD-NEGATIVE-ROUNDTRIP` — FALSIFIES gate.
- `C4 AD-TREATMENT-CONTRAST` — MEASUREMENT_INVALID gate.
- `C5 PC-ACCOUNTING-FIDELITY` — MEASUREMENT_INVALID gate.
- `C6 B-LITERAL-KERNEL` — MEASUREMENT_INVALID gate.
- `C7 PROMOTABILITY-REGRESSION` — FALSIFIES gate.

Precedence: C1 first; C1 fails ⇒ `MEASUREMENT_INVALID`; else any of C2/C3/C7 fails ⇒ `FALSIFIES`; else any of C4/C5/C6 fails ⇒ `MEASUREMENT_INVALID`; else `SUPPORTS`. Missing frozen prerequisite or out-of-scope installation ⇒ `BLOCKED`.

## 6. Design-time satisfiability probes (non-outcome-bearing)

These are cheap canaries that establish the frozen design is capable of answering its own question. They are **not** the frozen measurement; EXECUTE re-runs the full frozen certificate and writes its own raw evidence. All probes ran in `/tmp/opencode/probe` against copies of frozen artifacts and wrote nothing into the repository.

Probe P1 — carrier liveness at the shipping position. An isolated package copy was built by copying `src/spider` and overwriting only `kernel.py` with the frozen carrier, then adding the frozen `fixture.py`. Result (stdout excerpt):

```
F1-PATH-ID  slots=["item"]      EXECUTABLE bound_nonnull exec_status=200 verify=true
F2-QUERY-ID slots=["q"]         EXECUTABLE bound_nonnull exec_status=200 verify=true
F3-BODY-FIELD slots=["token"]   EXECUTABLE bound_nonnull exec_status=200 verify=true
F4-HEADER-FIELD slots=["resource"] EXECUTABLE bound_nonnull exec_status=200 verify=true
F5-TWO-SLOT slots=["item_id","tenant"] EXECUTABLE bound_nonnull exec_status=200 verify=true
F6-NOISE-STRESS slots=["node"]  EXECUTABLE bound_nonnull exec_status=200 verify=true
positive_all_pass=true slot_counts_match=true
```

Probe P2 — representative refusal. `resolve("fetch_item", ctx, {"item": ""})` returned `status=EXPLORE`, `bound_action=null`, `reason="parameter 'item' outside inferred support"`. A broader canary over the frozen `negative_cases()` observed refusal counts `out_of_support 16/16`, `missing_param 2/2`, `wrong_intent 6/6`.

Probe P3 — literal floor. The post-install literal `distill()` path produced `held_out_executable_count == 0`.

Probe P4 — pre-install unreachability. The shipped `src/spider/kernel.py` (blob `cfec9866...`) has no `distill_parameterized` (AST inspection) and a canary call raised `AttributeError: 'SpiderKernel' object has no attribute 'distill_parameterized'`.

Probe P5 — existing regression on the treatment. `tests/test_kernel.py` ran 3/3 OK both against the pre-install shipped package and against the isolated treatment package.

## 7. Consequences

- **Positive (`SUPPORTS`):** the frozen `src/tests` delta is exactly what `product-promote.yml` extracts (`git diff --binary --full-index pre_execute_sha..verdict_commit -- src tests`) and applies to `main`. The shipping package gains the audited parameterized distill → resolve → execute path with honest counters and unit-test coverage, satisfying readiness condition (1) and unblocking the deferred four-arm benchmark. Promotion remains gated by audit `PASS` and `verdict.promote_to_product`; DESIGN does not self-promote.
- **Negative (`FALSIFIES`):** the carrier does not survive installation/promotion at the shipping position; `C-PARAM-INHERIT` stays `HYPOTHESIS`/`EXPERIMENTAL`; the Product runner reverts the allowed code roots to `pre_execute_sha` (`scripts/revert_product_reject.py`). Next action: re-audit or re-derive the carrier at the shipping position.
- **Invalid (`MEASUREMENT_INVALID`):** no claim moves; repair the named gate and re-run.
- **Blocked:** restore the missing frozen artifact or grant the required scope.

## 8. Validity threats (disclosed)

- The fixture is synthetic and credential-free; a `SUPPORTS` result certifies **durability/promotability of the carrier on the shipping path**, not real-Web generalization. It does not advance `C-LLM-INHERIT` or `C-RESIDUAL-NOVELTY`.
- The audited carrier and the shipped `models.py`/`registry.py` are byte-identical to the audited harness copies; therefore the positive round trip is expected to pass. The discriminating value of this experiment is the identity/regression/contrast/accounting/floor gates (C1/C4/C5/C6/C7), which a drifted installation, a non-discriminating contrast, an accounting defect or a literal leak would still fail.
- `AD-IDENTITY-BINDING` inside the frozen runner only checks hash lengths; the full identity binding (exact carrier sha256/blob and `freeze.json.artifact_hashes` equality) is enforced by C1 in the decision rule and must be recorded by EXECUTE.
- The runner imports `spider.kernel` from `REPO_ROOT/src` first, so the measurement is genuinely taken at the shipping position; the experiment-local harness copies are pinned by content hash to the frozen sources.
- Reproducibility depends on `F6-NOISE-STRESS` noise fields (`trace_id`, `seq`, `ts`, `nonce`) never being promoted to parameter slots; the frozen fixture marks them explicitly and the audited carrier drops non-varying/state-only fields.

## 9. Freeze artifacts

`freeze_artifacts` (see `spec.json`) lists every mutable local interpretation dependency that exists at freeze:

```
research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py
research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py
research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py
research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py
research/experiments/EXP-PRODUCT-37950607128/harness/run_certificate.py
src/spider/__init__.py
src/spider/models.py
src/spider/registry.py
tests/test_kernel.py
```

`src/spider/kernel.py` is intentionally excluded: it is the treatment subject that EXECUTE replaces, and its identity is pinned indirectly by C1 to the frozen carrier artifact. The experiment-local harness copies do not exist at freeze and are instead bound by the required content-hash equality to the frozen fixture/runner sources.

## 10. Scope

EXECUTE may write only within the Product `allowed_code_roots` (`src`, `tests`, `sdk`, `pyproject.toml`) plus this experiment's directory. It must not modify any file listed in `freeze_artifacts` or `freeze.json.artifact_hashes`, and must not commit/push.
