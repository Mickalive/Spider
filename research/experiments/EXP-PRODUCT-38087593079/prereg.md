# EXP-PRODUCT-38087593079 — preregistration

- Lane: product. Claim: `C-PARAM-INHERIT`. design_contract_version: 2.
- Director mandate (from `request.json#director_mandate` and `research/portfolio/PROGRAM_AUDIT_2026-10-10.md`): readiness condition **B1** and readiness condition **(1)** — before any four-arm economics benchmark is funded, the Product lane must land the audited parameterized-inheritance carrier on the shipped path so that `src/spider/kernel.py` contains a concrete parameterized mechanism that an inherited procedure visibly instantiates and executes on a real task, plus a companion known-negative refusal certificate.
- Parent: `EXP-PRODUCT-37989728440` (disposition SUPERSEDE, action CONTINUE). Chain depth 0. `base_sha` = `6b4a1f7b18e84015e1765965081f2a8e97d3ba27`; `claim_registry_sha256` = `3511a7885c…` (request.json).
- This packet is DESIGN-stage output. It freezes the question, hypothesis, falsifier, baselines, controls, decision rule, consequences, cost, information gain, freeze eligibility and freeze artifacts. It does NOT execute measurements.

## 1. Precedent and inherited state (from the exact packets, not from memory)

1. **EXP-PRODUCT-37950607128 — AUDIT PASS.** The frozen synthetic arm-differentiation certificate (F1..F6) was established against the carrier under a *temporary install* of `src/spider/kernel.py`, then reverted to the literal kernel. Certificate semantics established: positive round trips **6/6** (held-out bound identifiers `itm-0009`, `epsilon`, `tok-99`, `res-z`, `t9+i9`, `n-09` per family F1-PATH-ID/F2-QUERY-ID/F3-BODY-FIELD/F4-HEADER-FIELD/F5-TWO-SLOT/F6-NOISE-STRESS; fixture-declared slot counts 1/1/1/1/2/1), declared negatives refused **24/24** (6 `wrong_intent`, 5 `out_of_support_empty`, 5 `out_of_support_space`, 5 `out_of_support_slash`, 2 `missing_param` — F5 tenant + item_id, 1 `out_of_support_pair`), treatment-vs-comparator contrast, scripted accounting fidelity, identity binding, literal floor 0 held-out EXECUTABLE at confidence 0.5. Follow-up constraint recorded: the landing was temporary, so promotion requires a durable byte-identical install plus a promotion delta pinned by `pre_execute_sha`.
2. **EXP-PRODUCT-37989728440 — FALSIFIES / BOUNDED_SUBSTRATE_CLASS_NEGATIVE.** The four-arm economics benchmark on the vENDORED (never-landed) carrier. Established: on this substrate the correctness ceiling is 1.0 at novelty ≥ 0.5, so the spec-construction comparator arm (`B-COLD-RE-DERIVE`) has zero dynamic range there and cannot identify a treatment effect; `T-SPIDER-PARAM` at novelty 0.0 achieved 10/10 success, mean_repair_attempts 0, retrieval 0.0 / verification 2.0 / model 0.0 (qualified). Raw evidence reused here as frozen input: `training_observations.jsonl` (80 observations), `induced_mechanisms.json` (4 mechanisms: `mech-8a45e6dd1d3e150d` F1 documents, `mech-650a9820f7c2ccf8` F1 records, `mech-1c2f86c4f26b0b1c` F2 gadgets, `mech-68b26e27622cd30c` F2 widgets; slots `[session_token, property, value, <id>]`; support grammars `^tok\-[a-z0-9]{16}$`, `^[a-z]+$`, `^draft\-[0-9]{1}$`, `^<type>\-0[0-9]{2}$`; confidence 0.9).
3. **EXP-PRODUCT-38085188374 — pre-freeze control-plane block (not scientific).** The identical mandate was blocked before freeze by the shared cross-lane model DESIGN REVIEW failure (fingerprint `3b9ff5e4e9e73f23e368efb4`); there was no scientific objection. This packet re-proposes the same design with design-time satisfiability probes (§11) now actually run, and with self-attack corrections applied (§3.3, §4.5, §8.1).

### carry_forward

- **established**: carrier is auditable (fixed bytes, blob `b15ed848…`, sha256 `718efa6a…`); synthetic certificate semantics and thresholds; real substrate behavior at fixed ids; four-arm economics non-identifying at novelty ≥ 0.5 on this substrate.
- **rejected**: running the four-arm economics benchmark at this stage; `B-COLD-RE-DERIVE` as a discriminating arm on the 1.0-ceiling substrate.
- **unknown**: whether the shipped path (currently literal-only) can instantiate the parameterized mechanism and pass the promotion suite — exactly what this certificate measures.
- **do_not_assume**: do not assume the frozen certificate is runnable pre-install (its imports resolve only against the carrier-mounted package); do not assume model calls are consumed by the real tier (0 by construction); do not assume the four-arm comparator stays non-identifying on other substrates; do not assume promotion without the pinned verdict pipeline (`product-promote.yml`).

## 2. Frozen artifact table (all content-hashed at DESIGN; re-verified byte-for-byte this run)

| Artifact | sha256 (this run, re-verified) | Role |
|---|---|---|
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` (git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`) | THE carrier: `distill_parameterized` + `_infer_support` + `_support_accepts` + `TrajectoryCounters` + literal `distill` — the exact object to install at `src/spider/kernel.py` |
| `research/experiments/EXP-PRODUCT-37989728440/harness/substrate.py` | `0f9f9182cb90ac9e379000e4420a93ba2d2e6a167906c59bd9eac8a8392395af` | Frozen real substrate (stdlib HTTPServer, 127.0.0.1, SEED 42): `build_train_tasks`/`build_test_tasks`/`build_scenario` |
| `research/experiments/EXP-PRODUCT-37989728440/harness/run_experiment.py` | `4cb974e8…` | Transcription source for the real tier's induction recipe and counter semantics |
| `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py` | `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf` | Frozen synthetic bank (F1..F6 families, grammars, degraded variants, `negative_cases()` = 24) |
| `research/experiments/EXP-PRODUCT-37950607128/harness/run_certificate.py` | `59895ddd9a85b6b3f75f9bfef6d39c423740679517df24505d26965918525970` | The AUDIT-PASSED frozen certificate runner (computes the six gated checks + `certificate_overall`) |
| `src/spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` | Shipped models — must stay unchanged (C0) |
| `src/spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` | Shipped registry — must stay unchanged (C0) |
| `src/spider/__init__.py` | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` | Shipped package init — must stay unchanged (C0) |
| `tests/test_kernel.py` | `ff9c1561…` | Existing regression test — must stay unchanged and keep passing (C5) |

Pre-install identity of `src/spider/kernel.py` (immutable): git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` at `base_sha` == same blob at DESIGN-time HEAD `74aac236` == working-tree file sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`. The DESIGN-time HEAD's allowed-root files were verified identical to `base_sha` (kernel `cfec9866…`, models `f08608c3…`, registry `986317f7…`, `__init__` `c8f3ab04…`, tests `05f4156f…`, pyproject `a01ce97d…`).

### Interpretation of frozen artifacts (mutable-dependency policy)

- EXECUTE never edits a frozen file; the five harness files are **byte-copied** into this experiment's `harness/` and hash-verified (C0). The shipped `models.py`/`registry.py`/`__init__.py`/`test_kernel.py` are read-only inputs, hash-verified at C0.
- The ONLY intentionally mutated file is `src/spider/kernel.py`, which is **excluded from `freeze_artifacts` by design** (EXECUTE replaces it with exact carrier bytes; its pre-install identity is pinned by immutable git object identity, its post-install identity by hash equality to the frozen carrier). Creation of `tests/test_ship_kernel.py` (required assertions enumerated verbatim in §8.1) and of this experiment's `harness/` copies are the only other writes inside the allowed code roots; everything else is written inside the experiment directory.
- Nothing is sampled from outside the frozen localhost substrate or the two frozen observation sets.

## 3. Real tier — substrate recipe (C1, C2, C8, C9)

### 3.1 Substrate
- `substrate.py` copied byte-identically; SEED 42; stdlib `http.server` bound to `127.0.0.1` only (no DNS, no external network, no browser, no model, no credentials). The server answers per-scenario, isolates scenarios, and includes noise fields that must never become parameter slots.
- `build_train_tasks()`: 5 training tasks per (family, resource_type), 10 per family, 20 total — ids `011, 022, 033, 044, 055` per resource type on `(j+1)*11` (`j` in 0..4); resources `documents`/`records` (F1) and `widgets`/`gadgets` (F2), sorted types per family (`types[0]`, `types[1]` per actual occurrence order); payload values `draft-0 … draft-4` (4 distinct), property names lowercase (`^[a-z]+$`), session token `tok-<16 hex>` (`^tok\-[a-z0-9]{16}$`).
- `build_test_tasks(novelty_fraction=0.0)`: the ONLY novelty level gated in this certificate; ids `013, 026, 039, 052, 065` on `(i+1)*13`, alternating resource types (F1: doc-013, rec-026, doc-039, rec-052, doc-065; F2: gad-013, wid-026, gad-039, wid-052, gad-065). All training ids are disjoint from all held-out ids (011/022/033/044/055 vs 013/026/039/052/065), verified at DESIGN §11.
- Server contract per task: `GET /session` returns `session_token = tok-<16 hex>`; `POST <resource>/<id>/update` with `{"property": <lowercase>, "value": <draft-\d>}` returns 200 `{"success": true, …}` only for a valid id and token; a control replay of a *training* id (e.g. doc-011) against a held-out scenario returns HTTP 404 (training identifiers are not bindable on held-out scenarios). At novelty 0.0 the session endpoint also serves a token-less driver convenience but the certificate always uses the real `tok-<16hex>` token so that the induced `^tok\-[a-z0-9]{16}$` grammar is exercised honestly.

### 3.2 Induction recipe (mechanism construction — transcription of frozen `run_experiment.py` T-SPIDER-PARAM)
1. For the 20 training tasks (10 per family, 5 per (family, resource_type)): `mechanism = kernel.capture(...)` collecting request/context; issue the update action; record observation `(scenario, request, response, outcome)`. Persist to `raw_evidence/training_observations.jsonl` (all 4 (family, rtype) pairs; ~80 observation records expected, mirroring the parent's frozen file).
2. Per (family, rtype): `kernel.distill_parameterized(observations)` → one `ParameterizedMechanism` (confidence 0.9; slots `[session_token, property, value, <id>]`; support grammars as in §1.2; id-slot support `^<type>\-0[0-9]{2}$`). Persist `raw_evidence/induced_mechanisms.json`.
3. Register the four mechanisms in `MechanismRegistry` of the INSTALLED kernel. The certificate's resolve path is the kernel's own (SpiderKernel with `counters=TrajectoryCounters()`; the harness NEVER hand-sets counters — C8).

### 3.3 Confirmatory task set (the exact 40 live cases; no subset selection)
- **C1 positives (10)**: held-out ids must resolve EXECUTABLE with non-null bound action whose URL contains the held-out identifier, execute over real HTTP (200, `success: true`), `verify(mechanism_id, response_body, params)` true, no cold fallback (`repair_attempts == 0`). Per task: `retrieval_calls == 1`, `verification_calls == 1`, `http_requests == 2`. Each held-out task carries its own in-grammar payload value `draft-{5+i}` (held-out, never a training value 0..4), which exercises value-slot binding through the induced `^draft\-[0-9]{1}$` support.
- **C2 negatives (30 = 3 × 10)**, same context/params as the matching positive except the single injected dimension; resolve must be non-EXECUTABLE with `bound_action == null` and the category-exact reason, and no HTTP execution attempt:
  - (a) out-of-support identifier `<type>-999` (e.g. `doc-999`, `gad-999`) → EXPLORE, reason category: `outside inferred support` (exact string verified at DESIGN: `parameter '<id-slot>' outside inferred support`);
  - (b) missing required parameter `property` → EXPLORE, reason category: `missing required parameter '<slot>'`;
  - (c) wrong intent `delete_resource` instead of `update_resource` → UNKNOWN, reason category: `no applicable validated mechanism`.
  - Expected refusal_rate = 1.0 (30/30).
- **C1/C2 controls**: PC-PARAM-BINDING, PC-NULL-REFUSAL, B-EMPTIED-REGISTRY (all fired in C0, §4.3, verified at DESIGN §11), and the replay-404 control (§3.1) inside C9.
- **C7 floor on the real batch**: a registry containing only literal mechanisms resolves every one of the 10 held-out inputs to EXPLORE with `bound_action null` (confidence 0.5 < 0.8); recorded, never a replacement of the carrier registry.

### 3.4 Raw evidence layout (real tier)
`raw_evidence/real_server.log` (per-request method/url/status), `raw_evidence/resolve_decisions.jsonl` (per case: input, family, resolve status, bound action or refusal reason, mechanism id), `raw_evidence/training_observations.jsonl`, `raw_evidence/induced_mechanisms.json`, `raw_evidence/counters.json` (per task kernel counters + `http_requests` recomputed from the server log). Every gated rate must be recomputable from these files by AUDIT.

## 4. Synthetic tier — frozen certificate (C4, C7, C8)

### 4.1 Invocation
- Byte-copy `fixture.py` and `run_certificate.py` into `harness/`; verify hashes (C0). Run **after the install (C0 passes)** and **before the EXECUTE install commit**, because the runner imports `from spider.kernel import SpiderKernel, TrajectoryCounters, _bind, _support_accepts`, which DESIGN-verified resolves ONLY against the carrier-mounted package (it raises ImportError against the shipped src). The runner's embedded `EXPERIMENT_ID = EXP-PRODUCT-37950607128` is the instrument's origin and is disclosed in `result.json`, never rewritten.
- The runner needs NO duplicate package trees: it creates fresh temp registries inside the INSTALLED package (`MechanismRegistry(tempfile.mkdtemp())`), exercises `distill_parameterized`/`distill`/`resolve`/`verify`/`rebind` of the installed kernel, and writes `raw_fixture/synth_induction_bank.json` + `raw_certificate/certificate.json` + `raw_certificate/accounting_fidelity_trace.json` into THIS experiment dir (REPO_ROOT resolves to this repo via `EXPERIMENT_DIR.parents[2]` after the byte-copy). B-LITERAL-KERNEL uses the installed package's own literal `distill()` into a fresh registry. The pre-install src bytes are used ONLY by the C3 and T5 checks (EXECUTE/AUDIT side), never by the runner. EXECUTE copies the runner's outputs verbatim and never mutates them.

### 4.2 Expected gating pass (C4)
`certificate_overall == "PASS"` AND all six `ad_positive_roundtrip_pass`, `ad_negative_roundtrip_pass`, `ad_treatment_contrast_pass`, `pc_accounting_fidelity_pass`, `ad_identity_binding_pass`, `b_literal_kernel_pass` are true. `ad_positive_roundtrip`: 6/6 (per family: resolved held-out bound identifier == fixture `bound_identifier(action)`, exactly `expected_slot_count` inferred slots: 1/1/1/1/2/1). `ad_negative_roundtrip`: 24/24 refused with the per-family refusal semantics. `b_literal_kernel`: 0 held-out EXECUTABLE under the literal-only registry (0.5 < 0.8).

### 4.3 Accounting semantics (C8, exact)
- Harness never sets kernel counters. `SpiderKernel(counters=TrajectoryCounters())`; only the installed kernel increments `retrieval_calls` (resolve) and `verification_calls` (verify); `repair_attempts` recorded by the harness only if a fallback were taken (none may occur: `repair_attempts == 0` required on the real tier).
- The frozen runner's `PC-ACCOUNTING-FIDELITY` asserts the scripted inherited-path increments `{retrieval_calls: 3, verification_calls: 2, repair_attempts: 1}` and the injected event `model_calls: 1, model_tokens: 128`; the injected event is **explicitly labelled an injected synthetic event, not observed model usage** and is never reported as observed model usage (observed model calls/tokens == 0 on the real tier; C10).

### 4.4 Non-vacuity recompute (EXECUTE + AUDIT, gating under C4)
From `raw_certificate/certificate.json` EXECUTE recomputes and AUDIT re-recomputes: (i) every AD-POSITIVE treatment case resolution_status == EXECUTABLE with non-null bound_action; (ii) every AD-TREATMENT-CONTRAST treatment action non-null; (iii) recomputed action-identity contrast == reported `contrast_rate` with every treatment action a fully bound template action (no `'${'` placeholders, equals the expected held-out binding); (iv) AD-POSITIVE inferred slot counts == fixture-declared (1/1/1/1/2/1); (v) the degenerate injection (treatment := comparator) collapses discriminators to 0.0 with `degenerate_variant_detected` true. Any failure of (i)-(v) fails C4 even if the runner's own booleans read true.

## 5. Pre-install discrimination and literal floor (C3, C7)

- **C3 structural**: against the immutable `base_sha` bytes (`git show 6b4a1f7b:src/spider/kernel.py` loaded in isolation, NOT from the post-install file): `hasattr(SpiderKernel, 'distill_parameterized')` is False; `from spider.kernel import _support_accepts, _infer_support, TrajectoryCounters` raises ImportError; calling `distill_parameterized` raises AttributeError; module-level `distill()` exists and returns literal 0.5 mechanisms. (All verified at DESIGN, §11.)
- **C3 behavioral**: the SAME induced mechanism (e.g. `mech-8a45e6dd1d3e150d`, F1 documents) serialized from the installed-carrier registry, upserted into a pre-install kernel → resolves the out-of-support `doc-999` AND the path-traversal value `../../etc` to EXECUTABLE with a non-null bound action URL, while the installed carrier resolves BOTH to EXPLORE (`outside inferred support`) with bound null on the IDENTICAL inputs, and both kernels resolve the in-support `doc-013` to EXECUTABLE. The pair {carrier refuses, pre-install accepts} must hold on `doc-999` (at least one family). Verified at DESIGN (§11, PROBE-D).
- **C7**: literal `distill()` confidence stays 0.5 < 0.8 and the literal path yields 0 held-out EXECUTABLE on the synthetic bank (runner's own check) and 0 on the 10 real held-out inputs (§3.3); the install does not silently alter literal behavior.

## 6. EXECUTE sequence (ordered; hides nothing)

1. **Execution-base**: confirm the EXECUTE-start HEAD; `record_execution_base.py` writes `execution_checkpoint.json` with `pre_execute_sha` = EXECUTE-start HEAD; verify all allowed-root files at that HEAD are byte-identical to `base_sha` (blob table §2) — mismatch ⇒ BLOCKED with the exact diff recorded.
2. **Pre-install identity**: `sha256sum src/spider/kernel.py` == `46929b3a…` and `git rev-parse HEAD:src/spider/kernel.py` == `cfec9866…`; else MEASUREMENT_INVALID (the baseline is wrong).
3. **Install**: byte-copy the carrier to `src/spider/kernel.py`; verify `sha256sum` == `718efa6a…` AND `git hash-object src/spider/kernel.py` == `b15ed848…` (working-tree object id; HEAD blob stays `cfec9866…` until the commit — this is what AD-IDENTITY-BINDING records). Write `tests/test_ship_kernel.py` (§8.1).
4. **C0**: hash-verify the five harness copies AND the four unchanged shipped files; fire PC-PARAM-BINDING (hand-authored parameterized mechanism in an emptied registry → EXECUTABLE, in-support identifier bound into the URL) and PC-NULL-REFUSAL (emptied registry on a positive-shaped task → non-EXECUTABLE, bound null). Controls not firing ⇒ MEASUREMENT_INVALID.
5. **Real tier** (§3): induction observations → `distill_parameterized` → registry; 10 positives + 30 negatives + C7 floor + replay-404 control; counters recorded. No cold fallback anywhere.
6. **Synthetic certificate** (§4): run the frozen runner pre-commit; copy `certificate.json` verbatim; recompute non-vacuity (§4.4).
7. **Suite (C5)**: `python -m compileall -q src` → 0; `PYTHONPATH=src python -m unittest discover -s tests -v` → 0 with tests/test_kernel.py (3) + tests/test_ship_kernel.py passing; `python scripts/validate_repo.py` → `SPIDER_R2_VALIDATE_OK` (no working-tree/HEAD check exists in `validate_repo.py`; the suite runs on the installed tree).
8. **Commit**: one commit containing EXACTLY `src/spider/kernel.py` (carrier bytes, `718efa6a…`) and `tests/test_ship_kernel.py`. Post-commit: `git diff --name-only <pre_execute_sha>..HEAD -- src tests sdk pyproject.toml` == exactly those two files (C6); installed kernel hash still `718efa6a…`.
9. **Packet outputs**: `result.json`, `report.md`, `provenance.json` per `research/EXPERIMENT_PACKET.md` (status/outcome/metrics/controls/artifacts/observations/validity_notes/unresolved), with the runner's embedded `EXPERIMENT_ID` disclosed; raw evidence per §3.4/§4.

### 6.1 Save / retry rules
- If a frozen artifact is missing or unreadable, or the install at `src/spider/kernel.py` is impossible in scope ⇒ **BLOCKED**: record the exact failure and the smallest next action; retry only by restoring the exact frozen bytes (carrier copies exist at two paths: `EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` and `EXP-PRODUCT-37989728440/kernel_treatment.py`; re-hash either copy before use; a hash mismatch after copy ⇒ BLOCKED, do not fall back to fishing the vendor repo).
- If C0 fails ⇒ **MEASUREMENT_INVALID**; record control outputs verbatim.
- No outcome-dependent redesign after seeing results: if a gated check fails, record the honest per-check state and map per `spec.json#decision_rule`; do not weaken or re-derive thresholds.

## 7. Required promotion regression test — `tests/test_ship_kernel.py` (T1–T4; created at EXECUTE, assertions enumerated here verbatim so EXECUTE does not improvise)

In-file assertions (exact-value assertions, no `assertTrue(True)` placeholders; must FAIL against the pre-install bytes with ImportError/AttributeError on the parameterized symbols):

- **T1 — identity and support machinery**: imports `from spider.kernel import SpiderKernel, TrajectoryCounters, _support_accepts, _infer_support` (module-level names; `distill_parameterized` exists only as a method — importing it as a module-level name is unsatisfiable, corrected from the prior draft); `hasattr(SpiderKernel, "distill_parameterized") is True`; `_support_accepts(r"^<type>\-0[0-9]{2}$", "doc-013") is True` and `_support_accepts(r"^<type>\-0[0-9]{2}$", "doc-999") is False`; `_infer_support` over slot values `["draft-1", "draft-3", "draft-7"]` yields a pattern matching `"draft-9"` and rejecting `"draft-10"`.
- **T2 — parameterized induction contract**: on 4+ stored training observations, `SpiderKernel().distill_parameterized(...)` returns a mechanism whose `confidence == 0.9` and whose `parameter_slots` equals the observed slot set (order-insensitive set equality).
- **T3 — binding hygiene**: a mechanism with `parameter_slots=["document"]`, `action_template` containing `"${document}"`, and support `^doc\-0[0-9]{2}$` produces, under `_bind`, a bound action whose URL contains `doc-013` and contains NO `"${"` placeholder; `_bind` with `doc-999` raises/returns refusal (status EXPLORE, `bound_action is None`), not an executable action.
- **T4 — literal floor preserved**: `SpiderKernel().distill(...)` (the shipped literal path) yields a mechanism with `confidence == 0.5`, and a registry containing only literal mechanisms resolves `doc-013` to EXPLORE (EXPLORE status literal, `bound_action is None`) — i.e., the literal floor is unchanged by the installation.
- **T5 — AUDIT-recomputed, NOT an in-file assertion**: AUDIT independently re-parses `tests/test_ship_kernel.py` to confirm the specific status/value literals (EXECUTABLE / 0.5 / None / EXPLORE / UNKNOWN) are asserted (no `assertTrue(True)`), and re-runs the module against the immutable pre-install kernel bytes in an isolated tree, confirming it fails with ImportError/AttributeError on `_support_accepts`/`_infer_support`/`TrajectoryCounters`/`distill_parameterized`.

## 8. Additional EXECUTE constraints

- Only paths granted by the workflow and `check_scope.py`: `src`, `tests`, `sdk`, `pyproject.toml`, and this experiment directory. Never edit `.github/`, `.opencode/`, constitutional files, `SPIDER_CODEX.md`, another lane/experiment. No `git add -A`, no force-push, no shared-branch resets.
- The certificate runs pre-commit so AD-IDENTITY-BINDING records `pre_blob=cfec9866…` (HEAD) vs working carrier `b15ed848…` with `pre_post_differ=true`; `pass` semantics = recorded.
- Promotion suite on `main` will re-run `compileall`/`validate_repo`/`unittest` with the delta applied; the delta extracted by `product-promote.yml` (`git diff --binary --full-index <pre_execute_sha> <verdict-creation commit> -- src tests sdk pyproject.toml`) must be exactly `{src/spider/kernel.py, tests/test_ship_kernel.py}` (C6). Promotion additionally requires the DIRECTOR verdict `promote_to_product=true` with lane/experiment matching and `state.json promotion_ready=true` — outside EXECUTE's remit.
- No four-arm benchmark arm, no `B-COLD-RE-DERIVE` success metrics, no pick-accuracy/no-budget semantics (C10); `model_calls == 0` and `model_tokens == 0` observed on the real tier.

### 8.1 Self-attack corrections applied versus the prior identical-mandate draft
1. T1 imports only module-level carrier symbols and asserts `hasattr(SpiderKernel, "distill_parameterized")` (the prior `from spider.kernel import distill_parameterized` was unsatisfiable — carrier defines it only as a method).
2. C8/C10 rephrased: observed model counters == 0 on the REAL tier; the synthetic runner's injected `model_calls=1/model_tokens=128` event is an explicitly-labeled injected (non-observed) event, so a literal "0 on both tiers" phrasing is not contradicted.
3. HEAD references: the prior draft pinned `d47e5208`; this draft requires the EXECUTE-start HEAD (recorded in `execution_checkpoint.json`) to have allowed-root files byte-identical to `base_sha`, with the DESIGN-time HEAD `74aac236` verified to satisfy that property (design commits touch only this experiment directory).
4. The full synthetic certificate is NOT run at DESIGN (outcome-bearing for C4); DESIGN touches were import-resolution, static arithmetic, fixture counts, expected-values contract checks, and non-live in-memory resolves on non-confirmatory values only.

## 9. Spoofing / identity guards

- Every package-level identity assertion (experiment_id/lane in `result.json`, `report.md`, `provenance.json`) must equal `EXP-PRODUCT-38087593079`/`product`. The runner's embedded `EXPERIMENT_ID EXP-PRODUCT-37950607128` is disclosed as the instrument origin.
- Genuine positive-arm evidence = `raw_evidence/training_observations.jsonl` + `induced_mechanisms.json` + per-task server log + resolve decisions; negative-arm evidence = refusal records with categories; accounting evidence = kernel counters (`TrajectoryCounters`, never hand-set) + per-task recompute; identity evidence = pre/post blobs with `pre_post_differ`; discrimination evidence = the C3 pair logs (identical mechanism+params on both kernels).
- AUDIT re-runs the frozen substrate + runner with the frozen hashes and must reproduce every gated rate; any drift → MEASUREMENT_INVALID with the diff.

## 10. Declared artifacts (EXECUTE)

- `execution_checkpoint.json` (pre_execute_sha; allowed-root blob table), `raw_evidence/*` (§3.4, §4), `derived/arm_metrics.json` (per-family/task success, refusal rates, counters), `result.json`, `report.md`, `provenance.json`, `harness/` (byte-copies of the five frozen files), `src/spider/kernel.py` (installed carrier), `tests/test_ship_kernel.py`.

## 11. Design-time satisfiability probes (non-outcome-bearing; run during DESIGN)

| Probe | What ran | Result |
|---|---|---|
| P-A liveness | Static replay of the frozen stored training observations (80 lines, parent's `raw_evidence/training_observations.jsonl`) through the carrier's `distill_parameterized` for all 4 (family, rtype) pairs | 4/4 mechanisms induced with mechanism_ids identical to the parent's frozen `induced_mechanisms.json` (`mech-8a45e6dd1d3e150d`, `mech-650a9820f7c2ccf8`, `mech-1c2f86c4f26b0b1c`, `mech-68b26e27622cd30c`), slots `[session_token, property, value, <id>]`, id-slot support `^<type>\-0[0-9]{2}$` (confidence 0.9), `_support_accepts` true for all five held-out ids 013/026/039/052/065 per type and false for `<type>-999` |
| P-C structural baseline | Pre-install bytes in isolation | No `distill_parameterized`/`_support_accepts`/`_infer_support`/`TrajectoryCounters` (hasattr False; ImportError; AttributeError on call); `distill()` exists, confidence 0.5 |
| P-D behavioral discrimination | Identical mechanism + params on (a) carrier, (b) pre-install bytes | Carrier: doc-013 → EXECUTABLE with URL containing doc-013; doc-999 and `../../etc` → EXPLORE `outside inferred support`; missing `property` → EXPLORE `missing required parameter 'property'`; wrong intent → UNKNOWN `no applicable validated mechanism`; empty registry → UNKNOWN. Pre-install: doc-013, doc-999 AND `../../etc` all EXECUTABLE (over-accepts). PC-PARAM-BINDING fires; PC-NULL-REFUSAL fires |
| P-E synthetic-instrument import + arithmetic | Imported the frozen runner's exact imports against the carrier-mounted package only; validated SCRIPTED_STEPS totals and fixture counts | Imports resolve ONLY against installed package (fail against shipped src); SCRIPTED_STEPS totals retrieval 2.0 / verification 2.0 / model_calls 1.0 / model_tokens 128.0 / http 1.0 / browser 1.0 / repair 1.0 / latency 12.5; declared 3/2/1 increments present; 6 families; `negative_cases()` == 24 (6 wrong_intent, 5 empty, 5 space, 5 slash, 2 missing_param, 1 out_of_support_pair) |
| P-E/baseline probes | `python -m compileall -q src`, existing tests, `python scripts/validate_repo.py` on the clean tree | compileall 0; unittest 3/3 green; `SPIDER_R2_VALIDATE_OK` |

Confirmatory/outcome-bearing measurements (live positive/negative round trips, the synthetic certificate's gated flags under the durable install, the promotion suite) are deliberately EXECUTE-only; the full frozen certificate was NOT executed at DESIGN.

## 12. Consequence binding (see also `spec.json#decision_rule`, `product_consequence_positive/negative`)

- SUPPORTS ⇒ readiness condition B1 cleared: shipped path carries the audited parameterized mechanism with known-positive real execution + known-negative refusal certificate (30/30 real across three classes; 24/24 synthetic), behavioral discrimination vs the pre-install bytes, identity/accounting fidelity, passing promotion suite, promotion delta exactly `{src/spider/kernel.py, tests/test_ship_kernel.py}`. Product lane may recommend promotion (DIRECTOR verdict) and may then fund the four-arm economics thread; `C-PARAM-INHERIT` stays EXPERIMENTAL until the DIRECTOR adjudicates.
- FALSIFIES ⇒ the failing check names the next bounded repair; no promotion; `C-PARAM-INHERIT` unchanged (EXPERIMENTAL).
- MEASUREMENT_INVALID ⇒ instrument fault (identity/literal-floor/accounting/promotion-delta/real-HTTP-validity/benchmark-scope), not science.
- BLOCKED ⇒ missing frozen artifact or impossible in-scope install; smallest unblocking action recorded.