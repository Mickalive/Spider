# EXP-PRODUCT-38149501627 preregistration

Lane: `product`. Claim: `C-PARAM-INHERIT` (registry status `EXPERIMENTAL`). Design contract: v2.
Request: `research/experiments/EXP-PRODUCT-38149501627/request.json`, `base_sha 148ba10ccd0d86e95c256934392fc1c97816edb5`, `director_mandate.allocation = {action: CONTINUE, claim_id: C-PARAM-INHERIT, parent_handoff_disposition: SUPERSEDE}`.
Parent handoff: `research/experiments/EXP-PRODUCT-37989728440/handoff.json` (sha256 `911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9`).

This preregistration is frozen before any outcome measurement. It is written for a fresh-context EXECUTE agent and a fresh-context AUDIT agent who will not see this author's reasoning. All identifiers (`PC1..PC7`, `PROMOTION-CERTIFICATE-B1-v1`, `PC-EXACT-REPLAY`, `N-EMPTY-REGISTRY`, `N-LITERAL-PATH`, `B-PREINSTALL-KERNEL`) are stable and must be reused verbatim downstream.

## 1. Direction: why this experiment, and what it is not

The mandate asks whether the already-audited parameterized carrier can be installed **byte-identically** at the shipping path `src/spider/kernel.py` and demonstrated to work through the shipped `spider` package, so that promotion is enabled only after independent audit PASS, discharging blocker B1. This is readiness condition (1) of the flagship C-LLM-INHERIT / C-RESIDUAL-NOVELTY / C-PRODUCT-ECON benchmark; readiness conditions (2) (non-degenerate asymmetric-discovery task bank, Runtime) and (3) (capable same-model Web-agent endpoint, Intel) are out of this lane's scope.

This experiment is **not** a re-run of the excluded dynamic-range economics certificate (`EXP-PRODUCT-37973256064` / `37982016598` / `37989728440`), and it does **not** run the four-arm C-LLM-INHERIT benchmark (unauthorized this cycle because readiness conditions (2) and (3) do not hold). It measures **integration identity + unseen-identifier execution + known-negative refusal through the public package on the real substrate**. It is a capability/promotion certificate, not a cost-per-success result, not novelty monotonicity, and not a savings or speed claim (P2-REPLAY-COST guard: the original 8.5x headline was withdrawn; the mandate makes no cost claim here).

The mechanism itself was already measured; the only unproven link is whether the frozen bytes can be installed and consumed as a product capability. Inherited state is preserved with the parent's four-way distinction (section 8). Nothing in the parent's bounded negative is reopened, and nothing in this design contradicts the parent's `do_not_assume` items.

## 2. Frozen objects

| Object | Exact identity |
|---|---|
| Carrier source (treatment bytes) | `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`, sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`, git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` |
| Carrier models (unchanged) | `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py`, sha256 `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` |
| Carrier registry (unchanged) | `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py`, sha256 `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` |
| Substrate fixture | `research/experiments/EXP-PRODUCT-37989728440/harness/substrate.py`, sha256 `0f9f9182cb90ac9e379000e4420a93ba2d2e6a167906c59bd9eac8a8392395af`, SEED=42 |
| Reference parent harness (protocol pin) | `research/experiments/EXP-PRODUCT-37989728440/harness/run_experiment.py`, sha256 `4cb974e8ba7fd7dc15596be53b40256a658607a2a3a36ec735468fcb3132442b` |
| Install target | `src/spider/kernel.py` (EXECUTE output, not a freeze artifact) |
| Pre-install baseline | git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50`, sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`, at `request.base_sha 148ba10c` and HEAD (verified) |
| Unchanged shipped modules | `src/spider/models.py` = carrier `models.py` (sha256 `338aaf4d...`); `src/spider/registry.py` = carrier `registry.py` (sha256 `51fb440d...`); `src/spider/__init__.py` (sha256 `3d173722...`) |
| Regression test | `tests/test_kernel.py` (sha256 `ff9c1561...`) |

The installed carrier requires no edit to `models.py` or `registry.py`: the carrier's vendored copies are byte-identical to the shipped modules (empty diff, probed at DESIGN), and `src/spider/__init__.py` already imports `SpiderKernel` from `.kernel`.

## 3. EXECUTE procedure (frozen)

1. Record `pre_execute_sha` and the pre-install `git hash-object src/spider/kernel.py` (must equal `cfec9866...`). Write `execution_checkpoint.json`.
2. Byte-copy the frozen carrier file to `src/spider/kernel.py` (no textual edits).
3. Assert PC1 before measuring: sha256 == `718efa6a...` and `git hash-object src/spider/kernel.py` == `b15ed848...`.
4. Import `spider` from `<repo>/src`; assert `spider.kernel.__file__` is `src/spider/kernel.py`. Do **not** import the parent's `audited_spider`.
5. Start one `SubstrateServer` (one `base_url` shared by training and held-out tasks). Capture the training observations for all 20 training tasks via real HTTP (`GET /api/session`, `GET /api/resources`, `GET /api/schema/<type>`, `POST /api/<type>/<id>/update`) exactly as `run_experiment.py` did.
6. For each resource type, call `distill_parameterized` over the 5 successful `update_resource` observations; upsert into the registry.
7. Positive branch PC2: for each novelty-0.0 held-out test task (10 tasks: 5 F1 + 5 F2), discover the session token, resolve with the task's target property/value and the held-out identifier, execute the bound action over real HTTP, and call `verify`.
8. Negative branch PC3: out-of-support-identifier cases (e.g. `doc-999`, empty string, `doc-01`, `doc-0/1`, and the F2 analogue), missing-parameter cases (omit a required slot), and wrong-intent cases (`delete`).
9. Controls PC5/PC6/PC7: empty-registry resolve; literal `distill` path; the 20 in-sample training replays (`PC-EXACT-REPLAY`); and `python -m unittest` on `tests/test_kernel.py`.
10. Re-assert PC1 after measuring. Emit raw per-task evidence (one record per resolve/execute/verify with success, status, bound_action, reason, counters) and the derived certificate JSON. Record the certificate harness sha256 in `provenance.json`. Never edit frozen inputs.

The certificate harness is the only EXECUTE-authored code; it must implement only the frozen checks of section 4 and must emit enough raw evidence for AUDIT to recompute every check without reading the harness.

## 4. Frozen promotion certificate `PROMOTION-CERTIFICATE-B1-v1`

The certificate is the conjunction of seven checks. Each is PASS or FAIL; no thresholds are tuned after outcomes.

- **PC1-INSTALL-IDENTITY** — installed `src/spider/kernel.py` sha256 == `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` AND `git hash-object` == `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` AND equal to the frozen artifact hash; asserted before and after the run.
- **PC2-POSITIVE-UNSEEN** — for every novelty-0.0 held-out task: a mechanism was induced from >=3 observations; `resolve` is `EXECUTABLE`; `confidence == 0.9`; `bound_action` is non-null; the bound identifier equals the task target identifier (never a training identifier); the real POST returns HTTP status 200 and `success == true`; `verify` returns true. Pass rate must be 1.0 over the 10 held-out novelty-0.0 tasks.
- **PC3-NEGATIVE-TAXONOMY** — every out-of-support-identifier case and every missing-parameter case is non-`EXECUTABLE` with `bound_action == null` and the correct recorded reason (`... outside inferred support`, `missing required parameter ...`); every wrong-intent case is exactly `ResolutionStatus.UNKNOWN` with `bound_action == null`. Pass rate 1.0.
- **PC4-COUNTER-HONESTY** — per positive execution: `retrieval_calls == 1`, `verification_calls == 1`, `repair_attempts == 0`; aggregate `model_calls == 0`, `model_tokens == 0`; no injected events. `latency_ms/1000` is excluded from every criterion.
- **PC5-ABLATION-SENSITIVITY** — (i) `N-LITERAL-PATH`: a fresh registry populated only via the installed kernel's preserved literal `distill()` over the training observations yields no `EXECUTABLE` and no bound action on the held-out tasks (0/10; literal confidence 0.5 < min_confidence 0.8). (ii) `N-EMPTY-REGISTRY`: an empty-registry resolve is exactly `UNKNOWN` with a null bound action and zero POSTs. (iii) static pre-install identity: `git show <pre_execute_sha>:src/spider/kernel.py` contains zero occurrences of `distill_parameterized`. Empirical anchor: parent `B-LITERAL-KERNEL` 200/200 EXPLORE.
- **PC6-IN-SAMPLE-POSITIVE** — `PC-EXACT-REPLAY` success_rate == 1.0 on 20/20 training tasks.
- **PC7-UNIT-REGRESSION** — `tests/test_kernel.py` passes with the installed kernel.

Decision:
- `PROMOTION_READY` iff PC1..PC7 all PASS. `certificate_overall = PASS`.
- Otherwise `NOT_PROMOTION_READY`. `certificate_overall = FAIL`; record every failing check and its raw evidence.

Both branches are reachable (see `spec.json.freeze_eligibility.decision_rule_reachability`). A PC2/PC3 failure means the shipped package cannot consume the carrier; a PC5 failure means the positive is not sensitive to the parameterized path.

## 5. Controls (stable identifiers)

- `PC-EXACT-REPLAY` — positive control, in-sample, expected 1.0 (20/20).
- `N-EMPTY-REGISTRY` — null carrier, expected exactly `UNKNOWN`, zero POSTs.
- `N-LITERAL-PATH` — ablation of the parameterized path, expected no `EXECUTABLE`.
- `B-PREINSTALL-KERNEL` — baseline identity blob `cfec9866`, expected to lack `distill_parameterized` (0 occurrences).
- `B-SYNTHETIC-CERT` — external consistency context: `EXP-PRODUCT-37950607128` `ARM-DIFFERENTIATION-CERTIFICATE-v1` (audit PASS, synthetic fixture). Disagreement with the real-substrate certificate is a validity threat to be reported, not re-measured.

## 6. Validity threats and mitigations

- **Support-boundary over-generalization** (carried from the parent): the held-out payload values are drawn inside `^draft-[0-9]{1}$`, so this certificate is an integration/unseen-identifier result inside the induced support grammar, not a free-form support-generalization result. Disclosed, not hidden.
- **Capability gate, not economics**: there is no comparative cost metric; the parent's 1.0 correctness ceiling makes arm-vs-arm economics non-identifying here, which is exactly why this experiment does not use it. Latency is excluded because the parent showed `latency_ms/1000` made its C3 criterion non-discriminating.
- **Instrument noise**: only integer structural counters are used; `latency_ms/1000` is excluded from every certificate check.
- **Wrong-import risk**: the certificate asserts `spider.kernel.__file__` is the shipping path and never imports `audited_spider`; a mis-import would fail PC1/PC2 and is itself informative.
- **Deterministic subscription**: identifiers/tokens/revisions are pure functions of SEED=42; the certificate is reproducible.
- **No external substrate**: everything is credential-free localhost stdlib HTTP; if the process cannot bind localhost or the harness cannot run, the result is a measurement failure, not a scientific negative.
- **Instrument mutable at freeze**: the EXECUTE certificate harness cannot be listed in `freeze_artifacts` because it does not exist at freeze time and DESIGN may not author code. Mitigation: its logic is fully specified in sections 3-4, its sha256 is recorded in `provenance.json`, and AUDIT must recompute every check from the emitted raw evidence.

## 7. Consequences

- **Positive (`PROMOTION_READY` + audit PASS)**: the Director may set `promote_to_product=true` and move `C-PARAM-INHERIT` toward `PRODUCT_CORE`; the shipped package exposes the parameterized path; B1 is discharged; the C-LLM-INHERIT / residual-novelty economics thread becomes constructible on a promoted carrier. Claim ceiling stays bounded to the deterministic credential-free REST class with `model_calls=0` by construction.
- **Negative (`NOT_PROMOTION_READY` or audit not PASS)**: no promotion; `C-PARAM-INHERIT` stays `EXPERIMENTAL`; B1 remains; revert `src` to the pre-execute checkpoint (`scripts/revert_product_reject.py`); record the exact failing checks so the next mandate targets the integration defect. Criteria are not weakened.

## 8. Inherited state preserved from the parent handoff (four-way)

- **established**: frozen-input/carrier integrity; the deterministic run is measurement-valid; the parameterized path is causally necessary on this substrate (`B-LITERAL-KERNEL` 0.0 vs `PC-EXACT-REPLAY` 1.0); the bounded substrate-class economics negative; the governance fact that the old freeze script did not enforce a certificate field.
- **rejected** (bounded to that substrate class and arm design): a certified dynamic range on the mandatory-discovery deterministic REST class; a counter-only treatment advantage there; the latency-inclusive metric as a discriminating instrument; the asserted `dynamic_range_certified` enforcement.
- **unknown**: whether any credential-free deterministic substrate can show a dynamic range for that arm design; whether asymmetric/amortized discovery would let the treatment save work; endpoint availability for the external benchmark; whether the kernel's support predicate on free-form values is a defect.
- **do_not_assume**: cold/retrieval 1.0 is a ceiling, not evidence inheritance lacks value; the treatment's 40/40/C3/C4 is not work compression; the shipped kernel still lacks the parameterized path (blob `cfec9866`); the old certificate gate was enforced; do not re-run the excluded certificate; do not promote the parent packet's scaffolding; the substrate workaround is not a support-generalization result; `model_calls=0` is by construction, not a measured zero.

This design supersedes the parent's `next_question` (which routed to an endpoint-gated four-arm benchmark) only because the Global Research Director issued a binding NEW mandate (`CONTINUE`, `SUPERSEDE`) for the B1 promotion transaction. It does not reopen the parent's rejected hypotheses and does not resume the parked four-arm benchmark.

## 9. DESIGN-time satisfiability self-attack (completed before freeze)

- **Empty/unreachable branches**: none. PC1..PC7 are an unordered finite conjunction; both `PROMOTION_READY` and `NOT_PROMOTION_READY` are reachable (section 4). No early check short-circuits a later check.
- **Arithmetic impossibility**: none. Pass rates are 0/1 over finite task sets (10 held-out, 20 in-sample); counters are exact integers; confidence 0.9 >= min_confidence 0.8.
- **Ceiling/floor baselines**: disclosed and deliberately avoided as a comparator. `B-PREINSTALL-KERNEL` is a floor for the positive (0 parameterized occurrences, confidence 0.5 < 0.8); `PC-EXACT-REPLAY` is the in-sample ceiling. The held-out PC2 check sits strictly between and is sensitive (PC5 would fail if a null control passed it).
- **Treatment/comparator identity**: treatment (blob `b15ed848`) and baseline (blob `cfec9866`) differ by exact bytes and by binary capability; only `src/spider/kernel.py` changes.
- **Insensitive controls**: rejected. `N-LITERAL-PATH` and `N-EMPTY-REGISTRY` must be non-`EXECUTABLE`; `PC-EXACT-REPLAY` must be 1.0. Parent evidence shows these expected values are attainable, and a null that fired the positive would fail PC5.
- **Missing prerequisites**: none; all prerequisites exist and are hashed (section 2, `freeze_eligibility.measurement_prerequisites`).
- **Unbound mutable artifacts**: all pre-existing mutable dependencies are bound in `freeze_artifacts`; `src/spider/kernel.py` is the EXECUTE treatment output and is pinned by pre-install identity; the EXECUTE harness is governed by sections 3-4 and recomputed by AUDIT (section 6).

## 10. Freeze eligibility

All six v2 checks are PASS with reasons and evidence refs in `spec.json.freeze_eligibility`. `freeze_artifacts` binds the pre-existing mutable local dependencies (carrier source and its vendored models/registry, substrate, reference parent harness, unchanged shipped modules, package entrypoint, regression test); `src/spider/kernel.py` is intentionally excluded because EXECUTE overwrites it with the byte-identical carrier.

## 11. Freeze protocol

This preregistration and `spec.json` are frozen by `scripts/freeze_experiment.py` only after an independent `design_review.json` returns `status = PASS`. After freeze they are immutable; EXECUTE may not re-design after outcomes are visible. EXECUTE adds `result.json`, `report.md`, `provenance.json` and raw/derived artifacts; AUDIT adds `audit.json`; DIRECTOR adds `verdict.json` and `handoff.json`. The certificate criteria in section 4 may not be edited at any later stage.
