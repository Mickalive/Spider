# EXP-PRODUCT-38085188374 — preregistration (unfrozen draft for freeze)

Lane: `product` · contract version 2 · claim: `C-PARAM-INHERIT`
Request: `research/experiments/EXP-PRODUCT-38085188374/request.json` (director_mandate action=CONTINUE, parent_handoff EXP-PRODUCT-37989728440 disposition=SUPERSEDE).
Frozen companion: `spec.json` in this directory. This prereg is the frozen recipe for EXECUTE; `spec.json` is the machine contract.

## 1. Precedent and distinct extension

- `EXP-PRODUCT-37950607128` (AUDIT PASS): established the frozen synthetic arm-differentiation certificate (`ARM-DIFFERENTIATION-CERTIFICATE-v1`) against a temporarily installed carrier on `src/spider/kernel.py`, but the verdict set `promote_to_product=false` and the lane's revert step restored the literal 0.5-confidence kernel (`src/spider/kernel.py` back to git blob `cfec9866…`). The certificate is established; the landing is NOT durable.
- `EXP-PRODUCT-37989728440` (FALSIFIES, BOUNDED_SUBSTRATE_CLASS_NEGATIVE): ran the four-arm economics benchmark with a VENDORED carrier (`kernel_treatment.py`, identical bytes) and proved the mandatory-discovery deterministic REST substrate class cannot discriminate (B-COLD-RE-DERIVE at the 1.0 correctness ceiling at novelty ≥ 0.5). It never landed the carrier at the shipped path.
- This experiment is a LEGACY DISTINCT_EXTENSION: it lands the audited carrier byte-identically at the shipped path and produces (i) a live known-positive executable round trip on a real task, (ii) a companion known-negative refusal certificate (30/30 real across three classes + 24/24 synthetic declared negatives), (iii) a behavioral treatment-vs-pre-install discrimination on identical mechanism+input, (iv) identity/delta binding for the sanctioned promotion path, and (v) the promotion validation suite — while explicitly NOT running any four-arm benchmark arm. It does not repeat the pre-2.0 P2-REPLAY-COST / P2-BLIND-COMPOSITION precedents (matched procedural-reuse economics) and does not spend a four-arm economics cycle.

## 2. Mandate, question, hypothesis

Director mandate question (verbatim from `request.json.director_mandate.allocation.question`): can the audited parameterized inherited carrier be landed into the shipped kernel through the sanctioned promotion path — i.e. after promotion the shipped execution path contains a concrete parameterized mechanism that an inherited procedure visibly instantiates and executes, together with a companion known-negative refusal certificate — such that B1 is satisfied and the pre-freeze executable mechanism required by readiness condition (1) exists, rather than once more running the four-arm economics benchmark on a kernel that still emits literals below the execution threshold?

Hypothesis (one sentence): installing the carrier bytes (blob `b15ed848…`, sha256 `718efa6a…`) at `src/spider/kernel.py` — preserving the literal path — makes the shipped package induce one parameterized mechanism per (family, resource_type) from repeated successful observations on the frozen real substrate, resolve every held-out novelty-0.0 in-support identifier to EXECUTABLE with a correctly bound action that executes (HTTP 200, success, verify true) with no fallback, refuse the three known-negative classes with bound_action null and category-correct reasons, differ behaviorally from the uninstalled baseline on identical mechanism+input, reproduce the audited synthetic certificate, and pass the promotion suite with an exact two-file promotion delta.

## 3. Frozen artifact table (all content-hashed at DESIGN against base 6b4a1f7b; re-verified this run)

| Path (repo-relative) | Role | sha256 (file) | git blob (where relevant) |
|---|---|---|---|
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` | CARRIER (treatment bytes) | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` | `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` |
| `research/experiments/EXP-PRODUCT-37989728440/harness/substrate.py` | real localhost HTTP substrate (SEED 42, stdlib) | `0f9f9182cb90ac9e379000e4420a93ba2d2e6a167906c59bd9eac8a8392395af` | — |
| `research/experiments/EXP-PRODUCT-37989728440/harness/run_experiment.py` | frozen transcription source for the real-tier driver (capture/induce/resolve recipe) | `4cb974e8ba7fd7dc15596be53b40256a658607a2a3a36ec735468fcb3132442b` | — |
| `research/experiments/EXP-PRODUCT-37950607128/harness/fixture.py` | SYNTH-INDUCTION-BANK-v1 (6 families, 24 declared negatives) | `b0ffcbba5041871f58408c4766268b31bb84cb81ccef965cd944c486fd4dd6cf` | — |
| `research/experiments/EXP-PRODUCT-37950607128/harness/run_certificate.py` | ARM-DIFFERENTIATION-CERTIFICATE-v1 runner (imports `from spider.kernel import SpiderKernel, TrajectoryCounters, _bind, _support_accepts`) | `59895ddd9a85b6b3f75f9bfef6d39c423740679517df24505d26965918525970` | — |
| `src/spider/models.py` | shipped support (byte-identical between harness and shipped; untouched) | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` | `f08608c3…` |
| `src/spider/registry.py` | shipped support (untouched) | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` | `986317f7…` |
| `src/spider/__init__.py` | shipped package export (untouched) | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` | `c8f3ab04…` |
| `tests/test_kernel.py` | existing regression suite (3 tests, must stay green) | `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6` | — |

Pre-install baseline bytes (NOT in `freeze_artifacts` by design): `src/spider/kernel.py` at base `6b4a1f7b` = git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` = HEAD `d47e5208` blob (verified) = freeze-time file sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`. Identity is pinned by immutable git object identity, not by the freeze file list, because EXECUTE replaces this one file (see §11).

## 4. Confirmatory task set

Source: frozen `substrate.py` (FAMILIES F1 documents/records `doc/rec`, F2 widgets/gadgets `wid/gad`; properties status/priority/owner and config/metadata/tags; `UPDATE_PATH = /api/{type}/{id}/update`).

- TRAINING (10 tasks/family, `build_train_tasks()`, novelty 0.0, ids `011/022/033/044/055` per resource type, property cycling status/priority/owner or config/metadata/tags, values `draft-0..draft-4`, endpoint provided): used ONLY for induction observations via `capture_training` semantics (GET `/api/session`, GET `/api/resources`, GET `/api/schema/<type>`, then the UPDATE POST per the task spec — see `run_experiment.py` `capture_training`).
- POSITIVE CONFIRMATORY (10 tasks, `build_test_tasks()` filtered to `novelty_fraction == 0.0`): 5 per family, ids per resource type `013/026/039/052/065` (in-support: all verified to match the induced grammar `^<type>\-0[0-9]{2}$` at DESIGN), property cycling, values `draft-5..draft-9`, endpoint and identifier provided, token NOT required (but session token still discovered per task, since `session_token` is a slot and its support `^tok\-[a-z0-9]{16}$` must be satisfied by the real discovered token).
- REFUSAL BATTERY (30 cases): every positive task × 3 constructions, all sharing the positive task's context and params EXCEPT one injected dimension:
  - R1 out-of-support identifier: `identifier := <type>-999` (e.g. `doc-999`; fails `^<type>\-0[0-9]{2}$`).
  - R2 missing required parameter: drop `property` from params.
  - R3 wrong intent: `resolve("delete_resource", ...)` with the positive params.
- DISJOINTNESS: training ids `{011,022,033,044,055}` vs positive ids `{013,026,039,052,065}` are disjoint; refusal values `-999` and `../../etc` appear only in refusal/pre-install cases; DESIGN probe ids (`doc-077`-style liveness and `doc-999`/`../../etc` discrimination checks) are documented in §9 and are never used as positive confirmatory ids. None of the confirmatory positives were LIVE-measured at DESIGN: probes ran on stored static observations (no server, no HTTP) — the live confirmatory transaction happens only during EXECUTE.

## 5. Real-tier recipe (EXECUTE executes this mechanically; no tunable parameters)

1. Copy `substrate.py` byte-identically into this experiment's `harness/` (verify sha256 `0f9f9182…`; C0).
2. Start `SubstrateServer` (127.0.0.1, random port; keep the instance alive for the whole tier so `base_url` in mechanism preconditions matches the held-out scenarios).
3. For each of the 10 training tasks (`build_train_tasks()`): `set_scenario(build_scenario(task))`, then capture observations exactly as `run_experiment.py#capture_training` does (the 4-observation sequence per task: session/resources/schema + update). Record RAW rows `{task_id, phase=training, family, resource_type, intent, state, action, next_state, success}` to `raw_evidence/training_observations.jsonl`.
4. Induce: for each (family, resource_type) in {F1×documents, F1×records, F2×widgets, F2×gadgets}, collect the `update_resource` observations, call `kernel.distill_parameterized(obs)` on a `SpiderKernel(MechanismRegistry(...), counters=TrajectoryCounters())` using the INSTALLED `src/spider` package, and `registry.upsert(mech)` (the carrier's `distill_parameterized` builds but does not register; the caller registers — mirror `run_experiment.py`). Record RAW `raw_evidence/induced_mechanisms.json` with mechanism_id, parameter_slots, parameter_supports, action_template, postconditions, confidence, evidence, per mechanism.
5. POSITIVE CERTIFICATE (C1): for each of the 10 confirmatory tasks: `set_scenario(build_scenario(task))`; discover the session token (GET `/api/session`); build params from the mechanism's slots (`session_token`=discovered token, `property`=spec.target_property, `value`=spec.target_value, id slot=spec.identifier); `resolve("update_resource", context, params)` with context `{"family", "resource_type", "base_url"}`; require EXECUTABLE and a non-null `bound_action` whose URL contains the held-out identifier (NO fallback is allowed: a non-EXECUTABLE resolve aborts C1 for that task and the task counts as failed); execute the bound action via `SubstrateClient.execute`; call `kernel.verify(mech.mechanism_id, resp["body"], params)`; require HTTP 200, body.success true, verify true. Record RAW per-task rows `{task_id, family, resource_type, identifier, mechanism_id, parameter_slots, supports, resolution_status, reason, bound_action, http_status, body_success, verify, repair_attempts, retrieval_calls, verification_calls, http_requests}`.
6. REFUSAL CERTIFICATE (C2): for each confirmatory task, with the same server+registry, resolve the three constructions R1-R3 (R1/R2 keep intent `update_resource`; R3 keeps positive params) and require: non-EXECUTABLE, `bound_action is None`, non-empty reason, and reason category matching §7. Record RAW `raw_evidence/known_negatives.jsonl` rows `{task_id, construction, status, reason, bound_action, expected_reason_category}`.
7. PRE-INSTALL BASELINE (C3): in a separate subprocess loading IMMUTABLE base bytes (a temp package dir containing `git show 6b4a1f7b:src/spider/kernel.py` as `spider/kernel.py` plus `src/spider/models.py`, `registry.py`, `__init__.py`): (a) assert `hasattr(SpiderKernel,'distill_parameterized') is False`, module lacks `_support_accepts`/`_infer_support`, and a `distill_parameterized` call on real training observations raises AttributeError; (b) upsert ONE mechanism serialized from the installed-carrier registry (write it to a temp jsonl via `MechanismRegistry`) into the pre-install kernel, and resolve the out-of-support id `doc-999` (and `../../etc`) with the same params → require EXECUTABLE with a non-null bound URL (over-acceptance); (c) report the pairwise contrast with the carrier's refusal on identical inputs. Record RAW `raw_evidence/preinstall_baseline.json` with all statuses/reasons/bound URLs.
8. NULL (PC-NULL-REFUSAL): fresh empty `MechanismRegistry`, installed kernel, resolve a positive-shaped task → require UNKNOWN, bound_action null. Record in `raw_evidence/null_control.json`.
9. Real-HTTP validity (C9): raw server log (method, url, status per request) plus the documented control: replay the first training update action verbatim (training id, e.g. `doc-011`) against a held-out scenario → require HTTP 404.
10. Tear down the server; write `raw_evidence/server_log.jsonl` and `derived/` aggregates (rates per check, per-category refusal rates, accounting sums).

## 6. Synthetic tier (C4)

1. Copy `fixture.py` and `run_certificate.py` byte-identically into this experiment's `harness/` (verify sha256 `b0ffcbba…` / `59895ddd…`; C0). Do NOT modify them; the embedded `EXPERIMENT_ID = "EXP-PRODUCT-37950607128"` is the instrument's origin and stays.
2. With the carrier installed at `src/spider/kernel.py` (working tree), run `python3 research/experiments/EXP-PRODUCT-38085188374/harness/run_certificate.py`. The runner reconstructs SYNTH-INDUCTION-BANK-v1, imports `spider` from `REPO_ROOT/src` (the installed package), executes AD-POSITIVE-ROUNDTRIP (6/6, slot counts 1/1/1/1/2/1), AD-NEGATIVE-ROUNDTRIP (24/24), AD-TREATMENT-CONTRAST, NC-ZERO-CONTRAST-TREATMENT, PC-ACCOUNTING-FIDELITY (declared 3/2/1 + injected labeled event), AD-IDENTITY-BINDING (requires a resolvable git HEAD blob for `src/spider/kernel.py` — i.e. a git working tree; records pre blob `cfec9866…` vs post carrier `b15ed848…` as `pre_post_differ=true`), B-LITERAL-KERNEL (0/6), and writes raw outputs into THIS experiment's `raw_fixture/` and `raw_certificate/`.
3. C4 pass requires `certificate_overall == "PASS"` and all six `checks_pass` fields true, plus the non-vacuity recomputation (i)-(v) from the raw certificate JSON (see spec.json C4): every positive treatment case EXECUTABLE with non-null action; every contrast treatment action non-null; recomputed action-identity contrast equals reported; slot counts match declared; degenerate injection collapse flagged (`degenerate_variant_detected == true`, discriminators 0.0).

## 7. Refusal semantics (frozen expected categories)

| Construction | Expected status | Expected reason substring | Expected bound_action |
|---|---|---|---|
| R1 out-of-support id | EXPLORE | `parameter '<id-slot>' outside inferred support` (e.g. `parameter 'document' outside inferred support`) | None |
| R2 missing required parameter | EXPLORE | `missing required parameter '<slot>'` (e.g. `missing required parameter 'property'`) | None |
| R3 wrong intent | UNKNOWN | `no applicable validated mechanism` | None |

These exact strings were observed at DESIGN (PROBE-D) and are produced by the carrier's `resolve` (deterministic: missing-slot check precedes support check; support check precedes candidate selection; wrong intent leaves no applicable candidate). The certificate asserts the category, i.e. the reason CONTAINS the expected substring; it does not depend on unrelated prose.

## 8. Promotion suite and required regression test (C5, C6)

Commands (must all exit 0):
- `python -m compileall -q src`
- `PYTHONPATH=src python -m unittest discover -s tests -v`
- `python scripts/validate_repo.py`

EXECUTE creates `tests/test_ship_kernel.py` (the second half of the promotion delta) with in-file assertions, at minimum:
- T1: `from spider.kernel import SpiderKernel, distill_parameterized, _support_accepts` succeeds; `hasattr(SpiderKernel, "distill_parameterized") is True`.
- T2: literal floor preserved: `spider.kernel`'s literal `distill()` on a successful `Observation` returns a Mechanism with `confidence == 0.5`.
- T3: two+ successful observations of one intent with a varying URL path segment distill to a parameterized mechanism (or, if hand-built instead of induced: a hand-built parameterized Mechanism with a support-guarded id slot resolves EXECUTABLE for an in-support id and EXPLORE `outside inferred support` for the out-of-support id), asserting `ResolutionStatus.EXECUTABLE` and the bound id/URL explicitly.
- T4: resolve with a missing required slot → EXPLORE with `missing required parameter`; resolve with a wrong intent → UNKNOWN with bound_action None.
No `assertTrue(True)` placeholders; every assertion must reference the frozen literals (`EXECUTABLE`, `0.5`, `None`, `EXPLORE`, `UNKNOWN`). AUDIT property T5 (not an in-file assertion): the same test module, run against the immutable pre-install bytes in an isolated tree, must fail with ImportError/AttributeError on the parameterized symbols, proving the new suite is sensitive to the installed carrier.

Promotion delta integrity (C6): `execution_checkpoint.json.pre_execute_sha` = EXECUTE-start HEAD (d47e5208; allowed-root files verified identical to base 6b4a1f7b). The diff `pre_execute_sha..HEAD -- src tests sdk pyproject.toml` must be exactly `{src/spider/kernel.py → carrier bytes, tests/test_ship_kernel.py → new file}`. `product-promote.yml` reads `state.json.promotion_ready` + `last_experiment_id`, pins `SOURCE_SHA` to the commit that CREATED `verdict.json`, requires `audit.json` PASS and `verdict.json.promote_to_product == true`, extracts exactly this two-file delta and applies it to `main`, then re-runs compileall/validate_repo/unittest on `main`.

## 9. Design-time satisfiability probes (evidence for freeze_eligibility; receipts)

Run during DESIGN against immutable materials; none is a live confirmatory measurement (no server, no HTTP; or non-confirmatory ids).

- PROBE-A (real-substrate replay, static stored data): re-enabled the carrier on the parent's frozen `raw_evidence/training_observations.jsonl`; `distill_parameterized` per (family, resource_type) → 4/4 mechanisms, slots `['session_token','property','value',<id>]`, supports `{'session_token': '^tok\\-[a-z0-9]{16}$', 'property': '^[a-z]+$', 'value': '^draft\\-[0-9]{1}$', <id>: '^<type>\\-0[0-9]{2}$'}`, confidence 0.9; `_support_accepts` true for all five held-out ids `013/026/039/052/065` per type and false for `<type>-999`. Corroborated by the parent's frozen raw `induced_mechanisms.json` (identical mechanism_ids, e.g. `mech-8a45e6dd1d3e150d`) and `arm_metrics.json` T-SPIDER-PARAM novelty=0.0: 10/10 success, `mean_repair_attempts == 0` (mechanism path, no fallback).
- PROBE-B (synthetic certificate vs carrier): carrier mounted as `pkg/spider` (kernel=models=registry) with the frozen runner in a scratch tree → `AD-POSITIVE-ROUNDTRIP`, `AD-NEGATIVE-ROUNDTRIP`, `AD-TREATMENT-CONTRAST`, `PC-ACCOUNTING-FIDELITY` (`counter_max_relative_error == 0.0`, observed 3/2/1 == declared 3/2/1), `B-LITERAL-KERNEL` all true; `AD-IDENTITY-BINDING` false ONLY because the scratch tree has no git repo (`pre_blob_sha1 == None`); structurally PASS in the real working tree (HEAD blob `cfec9866…` ≠ working carrier `b15ed848…`). `degenerate_variant_detected == true`.
- PROBE-C (pre-install structural): isolated import of `git show 6b4a1f7b:src/spider/kernel.py` in a temp package → `hasattr(SpiderKernel,'distill_parameterized') == False`; `hasattr(kernel,'_support_accepts') == False`; `import _support_accepts` → ImportError; `kernel.distill_parameterized(obs)` → AttributeError.
- PROBE-D (behavioral discrimination + refusal categories, carrier vs pre-install, identical mechanism `mech-8a45e6dd1d3e150d` + identical params): carrier `doc-013/026/039/052/065` → EXECUTABLE with bound URL `http://127.0.0.1:43839/api/documents/<id>/update`; carrier `doc-999` → EXPLORE `parameter 'document' outside inferred support` (bound None); carrier missing `property` → EXPLORE `missing required parameter 'property'`; carrier wrong intent → UNKNOWN `no applicable validated mechanism`; PRE-INSTALL `doc-013`, `doc-999` AND `../../etc` → all EXECUTABLE with bound URLs (over-acceptance). NOTE: the session token must be a real 16-char `tok-…` (support `^tok\\-[a-z0-9]{16}$`); an arbitrary short token is itself refused, which is why EXECUTE always discovers the real token.
- PROBE-E (shipped suite vs carrier): the existing 3 `tests/test_kernel.py` tests ran green against a carrier-mounted temp package (0 failures, 0 errors). `scripts/validate_repo.py` and `compileall` are run unchanged by the promotion path on main.

## 10. Accounting and raw evidence (C8)

- Kernel counters: `SpiderKernel(registry, counters=TrajectoryCounters())`; only `resolve` increments `retrieval_calls`, only `verify` increments `verification_calls` (kernel code). The harness READS `counters.as_dict()` per task and computes `http_requests`/`latency_ms` from its own network calls; it never writes kernel counters. Expected per positive task at novelty 0.0: retrieval_calls 1, verification_calls 1, repair_attempts 0, http_requests 2 (1 GET session + 1 POST update). `model_calls == 0`, `model_tokens == 0` everywhere; the frozen runner's injected `model_calls=1/model_tokens=128` event is labeled `injected synthetic event, not observed model usage` and must not be reported as observed.
- Raw evidence files (all under this experiment dir, JSON or JSONL, written by EXECUTE): `raw_evidence/training_observations.jsonl`, `raw_evidence/induced_mechanisms.json`, `raw_evidence/positive_trajectories.jsonl`, `raw_evidence/known_negatives.jsonl`, `raw_evidence/preinstall_baseline.json`, `raw_evidence/null_control.json`, `raw_evidence/server_log.jsonl`, `raw_certificate/*.json`, `raw_fixture/*.json`, plus `derived/aggregates.json`.
- `result.json.metrics` uses these stable names: `M-REAL-POSITIVE-RATE`, `M-REAL-REFUSAL-RATE`, `M-REFUSAL-BY-CATEGORY`, `M-PREINSTALL-OVERACCEPT`, `M-MECHANISMS-INDUCED`, `M-SYNTH`, `M-PROMOTION-SUITE`, `M-LITERAL-FLOOR`, `M-ACCOUNTING`, `M-DELTA`. `controls` uses `C0-INSTALL-IDENTITY … C10-NO-BENCHMARK`, `PC-PARAM-BINDING`, `PC-NULL-REFUSAL`, `B-SHIPPED-PRE-INSTALL`, `B-LITERAL-KERNEL`, `B-EMPTIED-REGISTRY`, `B-RETRIEVAL-SHAPED`, `B-COLD-RE-DERIVE` — same identifiers as spec.json.

## 11. Interpretation of frozen artifacts / why `src/spider/kernel.py` is not frozen

`freeze.json.artifact_hashes` freezes the nine files in §3 as immutable interpretation dependencies. `src/spider/kernel.py` is intentionally EXCLUDED because it is the experiment's own in-scope mutation (its pre-install identity is pinned by immutable git object identity: base blob `cfec9866…`; freeze-time sha256 `46929b3a…`; identical at HEAD). This avoids the known unsatisfiable freeze-time code-binding pattern (freezing a digest of code that cannot exist at freeze time): the CARRIER is an already-committed git blob plus an already-committed harness file whose identity IS frozen; the INSTALLED copy is verified by sha256 at EXECUTE in C0, not at freeze. Mutable EXECUTE-time artifacts whose identity changes interpretation (harness byte-copies, the real-tier driver, `tests/test_ship_kernel.py`) are specified EXACTLY by this prereg (bytes and recipes), their copy hashes are checked against the frozen originals in C0, and their own hashes are recorded in `provenance.json`.

## 12. Validity threats and mitigations

- Support inferred too narrow (held-out positives refused): ruled out at DESIGN by PROBE-A grammar check (all five confirmatory ids accepted); would surface as C1/C2 failure (gated).
- Refusal leakage (over-acceptance by carrier): gated by C2 with category assertions and zero-execution requirement; pre-install over-acceptance (PROBE-D) proves the support guard, not the input, is the discriminator.
- Session-token slot: token support `^tok\-[a-z0-9]{16}$`; arbitrary tokens are refused (observed), so EXECUTE always discovers the real token from the live server (frozen recipe) — an incidental demonstration that slot guards bind working values.
- Port dependence: `base_url` is bound at runtime from the same server instance serving held-out scenarios; the parent's identical-bytes run used the same pattern successfully.
- Determinism: substrate SEED=42; all ids/properties fixed; induction is deterministic given observations; no random sampling anywhere in the certificate.
- Duplication / hindsight: probes used static stored parent data or non-confirmatory ids; the live confirmatory transaction (fresh server, fresh scenarios, raw evidence, accounting) is measured only in EXECUTE. The synthetic tier is a replication of an already-audited certificate under the new durable-install condition (the audited run was reverted); its added value is the promotion/durability context, not re-establishment of the certificate itself.
- Ceiling artifacts: B-COLD-RE-DERIVE (1.0 ceiling on this substrate) is never gated; no cost-metric dimension is omitted from the only counters scored (kernel counters + live http_requests).
- Control-plane hazards: no freeze-time code hashing requirement (see §11); all six `freeze_eligibility` checks are PASS with evidence refs; every mutable local dependency is frozen.
- Disclosed ceiling: this certificate gates B1 and promotion, not C-PARAM-INHERIT generalization or economics; novelty levels 0.25/0.5/0.75 are reported-only (integration breadth) and never gated.

## 13. Consequences (mirrors spec.json)

- SUPPORTS → B1 cleared; promotion delta pinned; DIRECTOR may authorize promotion (promote_to_product=true after AUDIT PASS) and the serial chain B1→B2→B3 proceeds; C-PARAM-INHERIT stays EXPERIMENTAL pending DIRECTOR adjudication.
- FALSIFIES → no promotion; the failing check names the next bounded repair; C-PARAM-INHERIT stays EXPERIMENTAL.
- MEASUREMENT_INVALID → instrument/integrity fault; not scientific evidence.
- BLOCKED → restore the missing frozen artifact or grant scope.