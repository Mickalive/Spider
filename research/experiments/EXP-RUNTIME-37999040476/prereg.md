# EXP-RUNTIME-37999040476 preregistration

Lane: `runtime` · Claim: `C-MEAS-VALID` ("Measurement substrate is intervention-valid") · Design contract v2 · Director mandate PIVOT (cycle 37998281030) · This document and `spec.json` are the frozen design.

## s1 Question, hypothesis, falsifier

**Question.** Can Runtime build and measurement-validly certify a credential-free, deterministic localhost execution substrate (`ASYM-DISC-A`) whose task bank is NON-DEGENERATE — B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED below the 0.95 success ceiling at residual novelty ≥ 0.5 with matched correctness ≥ 0.80, and the parameterized treatment (frozen carrier git blob `b15ed848`, sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`) showing a real treatment/comparator behavioural distinction on honest per-task counters (http_requests, retrieval_calls, verification_calls, repair_attempts; `latency_ms` excluded from every decision metric) — certified ARITHMETICALLY BEFORE FREEZE, so that readiness condition (2) of the future four-arm C-LLM-INHERIT / C-RESIDUAL-NOVELTY benchmark holds?

This repairs the exact failure recorded in `EXP-PRODUCT-37982016598` and `EXP-PRODUCT-37989728440` (BOUNDED_SUBSTRATE_CLASS_NEGATIVE): on the old mandatory-discovery deterministic REST class, cold and retrieval both sat at success 1.0 at every novelty, so the C1 dynamic-range gate was arithmetically unsatisfiable. `ASYM-DISC-A` instead makes one-time session/resource/schema discovery real work (rate-limited session grants, session-scoped universe, session-locked schema revision) that retention + parameterization can amortize.

**Hypothesis (H1).** On `ASYM-DISC-A`, the frozen no-memory cold and retrieval-shaped comparators must re-derive session/universe/schema per task, so they (a) deterministically fail session establishment on non-granted task slots (F1 7/40, F2 6/40 at SEED=37999040476) and (b) pay a strictly larger per-task HTTP cost than T-SPIDER-PARAM, which retains one granted session per batch of K=4 and re-binds the retained session token / resource id through the frozen parameterized mechanism. Because the substrate is deterministic, measured success and counter costs reproduce the pre-freeze arithmetic certificate within tolerance 0.02. The advantage is causally attributable to the parameterized registry (vanishes under NC-EMPTY-REGISTRY and B-LITERAL-KERNEL) and is not a harness artifact (vanishes under NC-FULLY-SPECIFIED at K=1).

**Falsifier.** Falsified if, under the frozen contract at novelty ≥ 0.5 on ≥1 family: (F2a) measured cold or retrieval success ≥ 0.95 (ceiling; the bounded negative is reproduced); or (F2b) no behavioural distinction — measured mean treatment http_requests/task is NOT at least 1.0 below both comparators, or treatment counter-sum cost per success is NOT below both; or (F3) measured rates deviate from the certified values by > 0.02 or the DET-DETERMINISM two-run control disagrees, so the certificate is not faithful. Any of these blocks funding the four-arm benchmark and keeps C-MEAS-VALID's session/auth control gate unmet.

## s2 Prerequisites

Available now (verified in DESIGN):
- Python 3.12 stdlib only (`http.server`, `hashlib`, `json`, `urllib`) — no third-party packages.
- Localhost loopback; writable `/tmp`; single Linux runner; no GPU.

Explicitly NOT prerequisites (credential-free by construction): no external network, no browser, no credentials/API keys, no model endpoint. The blocked EXP-INTEL credential-free-model-endpoint question is OUT OF SCOPE for this packet; arms are deterministic scripted policies and `model_calls` must be 0. The later four-arm benchmark is what would add an LLM arm.

Required-and-available dependency — the treatment carrier package:
- Path: `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/{__init__.py,kernel.py,models.py,registry.py}` on `origin/lab2/product` commit `18d17211`.
- `kernel.py` = git blob `b15ed848`, sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`; `models.py` sha256 `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78`; `registry.py` sha256 `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c`.
- It is NOT on `main` or `lab2/runtime` (verified: no `distill_parameterized` there). EXECUTE obtains it read-only:
  `git fetch origin refs/heads/lab2/product:refs/remotes/origin/lab2/product` then `git cat-file blob b15ed848`, `git show 18d17211:.../models.py`, `git show 18d17211:.../registry.py`, and MUST verify all three sha256 before any arm runs.
- If the fetch or a hash check fails: EXECUTE reports `status=BLOCKED`, `outcome=INCONCLUSIVE` with the exact failing command; this is an infrastructure failure, never a scientific negative.

## s3 Substrate contract

`ASYM-DISC-A` is a credential-free, deterministic, single-threaded stdlib-HTTP substrate on `127.0.0.1`. A fresh server instance is started per arm run with `MASTER_SEED = 37999040476`; every response is a pure function of (route, family, task index, session token). No time-dependent content; `Date` is fixed. Raw request logs are written per arm.

**Identities and grammars (shared by training and test banks — frozen).**
- session token: `^sess-[a-z0-9]{16}$` (deterministic: `sess-` + sha256(`SEED:family:index:session`)[:16])
- record id: `^res-[a-z0-9]{8}$`
- auth nonce: `^nonce-[0-9]{10}$` (deterministic per (session, id, task index))
- update value: `^[a-z]+$` (e.g. `open`, `closed`, `held`); update-body key literal per revision (`field` for rev2, `property` for rev1)
- resource name (selection key, not a mechanism slot): `^[a-z0-9-]+$`

**Routes (frozen semantics).**
- `POST /api/session`, header `X-Task-Id: {family}-{novelty}-{index}`. On a GRANTED slot → `201 {"session_token": [...], "base":"/api/{type}"}`; on a DENIED slot → `429 {"error":"SESSION_RATE_LIMIT"}` and the denial is terminal for that task slot (retries at the same slot return `429`). The session is bound to (family, session-locked `schema_rev` ∈ {rev1, rev2}) and carries the task's batch.
- `GET /api/session/{token}/resources?page={n}` (header `X-Session-Token`) → the session's universe: 5 records (target + 4 distractors) at novelty < 0.5 (one page), 8 records (target + 7 distractors) in 2 pages of 5 at novelty ≥ 0.5; response `{"records":[{"id":[..],"name":[..]}...],"next":<bool>}`. The task's target is the record whose `name` matches the task spec (unique match by construction). **Target pinning (frozen):** at novelty ≥ 0.5 the target is deterministically placed on the LAST page (page 2, which holds 3 of the 8 records), so a correct discovery always fetches exactly 2 pages and the frozen request recipes in this section are exact rationals with zero per-task variance; at novelty < 0.5 the target is on the single page (exactly one fetch). This placement is identical for every arm.
- `GET /api/session/{token}/authorize?resource={id}` → `{"nonce":[...]}` — required per task for the update.
- `GET /api/schema/{type}` (header `X-Session-Token`) → `{"rev":"rev1"|"rev2","update_path":"/api/{type}/{id}/update","body_keys":["field","value"]}` (rev2) or `["property","value"]` (rev1). `rev` is session-locked and revealed by this response.
- `GET /api/{type}/{id}/detail` (header `X-Session-Token`) → `{"id":[...],"fields":[..]}` — used at novelty 0.75 to discover the per-record updateable field name.
- `POST /api/{type}/{id}/update`, headers `X-Session-Token`, `X-Auth-Nonce`, body per the session revision → `200 {"status_code":200,"updated":true,"rev":[...]}`; `401` on invalid/stale token; `403` on invalid nonce; `422` on wrong body key.

**Deterministic session-grant schedule (the environment dynamic; Director prior #6).** Session creation is rate-limited uniformly for all arms:
`deny(family, i) = False` if `i % K_BATCH == 0` (batch-start slots are always granted), else `True` iff `int(sha256("{SEED}:{family}:{i}").hexdigest(), 16) % 8 == 0`.
At `K_BATCH = 4`, `N_CELL = 40`: F1 denies indices `{1,17,19,21,25,29,39}` (7/40); F2 denies `{3,7,13,23,30,39}` (6/40). Batch starts `{0,4,8,...,36}` are never denied. Thus the treatment's single granted session per batch is always obtainable, while a per-task re-deriver is denied on exactly those slots and fails the task. This schedule is a pure function of the task index, so retries within a denied slot are also denied (a per-task cooldown), which is why the comparators cannot recover by retrying.

**Task-bank generator.** `TEST_SEED = 37999040476`, `TRAIN_SEED = 37999040477`; families `F1` (type `record`) and `F2` (type `catalog`); novelty ∈ {0.0, 0.25, 0.5, 0.75}; 40 tasks per (family, novelty); batches of `K_BATCH = 4` in bank order. The novelty ladder determines what the task spec omits (discovery required) and the frozen per-arm request recipes:
- novelty 0.0: spec gives `{id, field, value}` → cold `create+authorize+update = 3`; treatment per-task `authorize+update` plus amortized batch overhead 1/4.
- novelty 0.25: spec gives `{id, value}`; body key from schema → cold 4; batch overhead 2/4.
- novelty 0.5: spec gives `{target_name, value}`; id from universe (2 pages) + body key from schema → cold 6; batch overhead 4/4.
- novelty 0.75: spec gives `{target_name, value}`; id from universe + field from per-record detail + body key from schema → cold 7; per-task treatment `detail+authorize+update`, batch overhead 4/4.

Training bank: 4 sessions × 4 tasks per (family, schema_rev), disjoint from the test bank, all grants allowed (training is unscored). Training observations are recorded for the intents needed to induce mechanisms.

**Observation schema for induction (frozen).** `intent ∈ {open_session, list_resources, get_schema, get_detail, authorize, update_resource}`; `state = {"session_established": true, "schema_rev": "rev1"|"rev2", "family": "F1"|"F2"}` (stable within an induction group); `action = {"method","url","headers","body"}`; `next_state = {"status_code":200,...}` on success. Two carrier constraints discovered by the DESIGN liveness probe are frozen here: (1) URL-carrying action templates MUST use a fixed authority/static prefix with EXACTLY ONE varying final path segment (the record id), otherwise the carrier names the slot after the host/port and binds nothing; (2) `distill_parameterized` does NOT register a mechanism — the harness MUST call `registry.upsert(m)` before `resolve`. Induction groups are `(intent, family, schema_rev)` with ≥2 successful observations; `min_confidence = 0.8`.

## s4 Arms

Frozen arm policies (identical across the bank; only these memory policies differ):

- **T-SPIDER-PARAM (treatment).** Uses the vendored frozen carrier (`SpiderKernel` with `distill_parameterized` on the training bank, `registry.upsert`, `TrajectoryCounters`) plus per-batch retention. Per batch: (1) establish ONE granted session via the batch-start slot; (2) fetch/retain the universe pages and schema revision; (3) for each task: (novelty 0.75) fetch record detail, fetch authorize nonce, `resolve("update_resource", context=live state, params={retained session_token, retained record id, fetched nonce, spec value})`; execute the bound action; `verify` the postcondition; on non-`EXECUTABLE` refusal use `rebind` (one repair attempt) then the documented cold fallback. Retained token/id are re-bound per task through the parameterized mechanism (this re-binding is the causal capability vs retrieval). The frozen policy issues exactly the listed requests per task with NO cross-task instruction caching: at novelty 0.75 it fetches the per-record detail on every task and does not reuse a previously seen record's field across tasks (the updateable field name is per-record, derived from the record id), keeping the certified 4.0 average exact.
- **B-COLD-RE-DERIVE.** No cross-task memory. Per task: full re-derivation (create + optional list/schema/detail + authorize + update per the recipes above). A `429` session-grant denial is a task failure; the policy does not retry beyond the denial. Issues exactly the listed requests per task; no caching or short-circuiting is permitted.
- **B-RETRIEVAL-SHAPED.** Retrieves the top-1 training trajectory for the task's required-intent signature by a frozen deterministic key, then replays the stored update action with the spec value substituted; the stored session token is stale → `401` → repairs by full per-task discovery (as cold, +1 failed replay). Counts `retrieval_calls = 1` and `repair_attempts = 1` per task honestly.
- **B-LITERAL-KERNEL (carrier ablation).** Identical harness/retention, but the kernel uses the pre-repair literal `distill` path (confidence 0.5 < 0.8) so `resolve` returns `EXPLORE` and the harness falls back to per-task cold discovery — no amortization. Isolates the parameterized induction path as the causal carrier.
- **NC-EMPTY-REGISTRY (inheritance ablation/null).** Treatment harness with an empty registry → `resolve` returns `UNKNOWN` → cold fallback. Must not beat cold.

## s5 Controls

- **PC-SESSION-AMORTIZE (positive).** A fixed 8-task batch at **novelty 0.5** run with **K_BATCH=8** under the frozen schedule (batch-start slots 0 and 8 are always granted; other slots follow `deny()`). The treatment must reach success 1.0 with average http_requests/task ≤ 3.0 (per-task authorize+update = 2, plus amortized batch overhead create + 2-page-list + schema = 4/8 = 0.5) while cold on the same batch pays its full 0.5 recipe (6 requests/task) and/or a grant denial. Fires iff retention + parameterized re-binding is actually implemented. A null here is an implementation failure, not a scientific result.
- **NC-FULLY-SPECIFIED (null).** `K_BATCH = 1`: no cross-task amortization is possible, so every arm is forced onto the identical per-task recipe; all arms must agree on success and http/task within **0.01 relative difference**, and the certificate must NOT certify a margin at K=1. This is the strict null that proves the distinction is not a substrate artifact.
- **NC-EMPTY-REGISTRY (null/ablation).** As above: http margin vs cold < 1.0 and success within 0.02. Proves the parameterized registry is the causal carrier.
- **KNOWN-NEGATIVES (mechanical selectivity).** Out-of-support id (unexpected characters), missing `session_token` param, wrong intent, tampered postcondition. Refusal rate ≥ 0.95 and reason correctness 1.0; DESIGN liveness probe already showed `EXPLORE`/`UNKNOWN`/`verify=False` for these on the frozen carrier.
- **D-DIRECT-NO-DISCOVERY (diagnostic).** At novelty ≥ 0.5, construct the update from the spec alone (guess id) with no discovery → success must be 0.0, proving discovery is genuinely required by the bank (bank non-triviality).
- **DET-DETERMINISM.** Re-execute the entire F1 × novelty-0.5 cell (40 tasks) for every arm and require byte-identical request logs. Any mismatch is `MEASUREMENT_INVALID`.

## s6 Metrics

Stable metric identities for EXECUTE/AUDIT reuse:
- `m_success_rate` — fraction of tasks completed with a 200 update and verified postcondition, per (family, novelty, arm).
- `m_http_requests_per_task` — total cell `http_requests` / `n_tasks`, amortized batch overhead included; **primary** behavioural-distinction metric (symmetric across arms).
- `m_counter_sum_per_success` — `(http_requests + retrieval_calls + verification_calls + repair_attempts) / successes`; secondary distinction metric.
- `m_retrieval_calls`, `m_verification_calls`, `m_repair_attempts` — kernel events counted identically for every arm that performs them.
- `m_model_calls` — must be 0 for every arm.
- `m_latency_ms` — recorded but **EXCLUDED** from every decision metric and from the certificate (frozen; the product-lane C3-on-latency-noise failure mode cannot recur).

## s7 Arithmetic certificate

The certificate is computed from frozen parameters only, with NO arm executed and NO outcome inspected. It is the DESIGN satisfiability probe required by design contract v2.

Algorithm: for each (family, novelty):
- `cold_success = (N_CELL - denied(family)) / N_CELL`, `denied(family) = #{i ∈ [0,40) : deny(family,i)}`;
- `retrieval_success = cold_success` (same per-task session policy);
- `treatment_success = 1.0` (batch-start slots `{0,4,...,36}` are never denied);
- `cold_http`, `treat_http = base + overhead/K_BATCH`, `retr_http = cold_http + 1` from the frozen recipes;
- `*_cps = http / success`.

Gate: exists (family, novelty ≥ 0.5) with `cold_success < 0.95 ∧ retrieval_success < 0.95`; all main arms ≥ 0.80; `treatment_success − max(cold,retrieval) ≥ 0.05`; `treat margin vs both ≥ 1.0`.

**Pre-freeze result: PASS.** Exact values are stored in `spec.json#prefreeze_certificate.per_cell` (also summarized here):
- F1: cold/retrieval success `0.825`; treatment `1.0`; at novelty 0.5/0.75 the http margin vs cold is `3.0`, vs retrieval `4.0`; counter-sum cost/success treatment `3.0` vs cold `7.27` vs retrieval `8.48`.
- F2: cold/retrieval success `0.85`; treatment `1.0`; at novelty 0.5/0.75 the http margin vs cold is `3.0`, vs retrieval `4.0`; counter-sum cost/success treatment `3.0` vs cold `7.06` vs retrieval `8.24`.
- All arms ≥ 0.80 at every cell (0.825/0.85 comparators, 1.0 treatment), so there is no floor degeneracy; comparators strictly below 0.95, so there is no ceiling degeneracy.

EXECUTE transcribes `research/runtime/asym_disc/certificate.py` from this algorithm, re-runs it before reporting any arm outcome, and must reproduce every number exactly; any mismatch is `MEASUREMENT_INVALID`.

## s8 Measurement chain and determinism

`RAW EVIDENCE` = per-arm byte logs of HTTP request/response lines + kernel counter dicts, written under `research/experiments/EXP-RUNTIME-37999040476/artifacts/`. `OBSERVATION` = per-task success and counts. `DERIVED MEASUREMENT` = the metrics in s6. `INTERPRETATION` = the certificate comparison and the D0–D4 gates. These levels are kept separate in `result.json`. The substrate is single-threaded and seed-deterministic; DET-DETERMINISM is the formal determinism assertion.

## s9 Decision rule

Ordered gates; the FIRST failing gate decides:
- **D0 CERTIFICATE-PASS** (pre-freeze): already PASS as recorded in spec; EXECUTE only verifies reproducibility. A D0 regression is `MEASUREMENT_INVALID`.
- **D1 MEASURED-FAITHFUL**: `|measured_success − certified_success| ≤ 0.02` for every (family, novelty, arm); measured http_requests/task equals the frozen recipe value EXACTLY for every arm/level (frozen values are rational: integers for cold/retrieval, fractions with denominator 4 for the treatment e.g. 2.25/2.5/3.0/4.0; equality is checked as exact rational arithmetic); DET-DETERMINISM logs identical. Fail → `status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE`.
- **D2 COMPARATOR-BELOW-CEILING**: measured cold < 0.95 and retrieval < 0.95 at novelty ≥ 0.5 on ≥1 family. Fail → `status=COMPLETE, outcome=FALSIFIES`. GUARD NOTE: for a D1-faithful implementation this branch is entailed, not independently reachable (the 0.02 tolerance vs certified 0.825/0.85 makes measured comparator success ≥ 0.95 arithmetically impossible); it is kept as an explicit named predicate because the mandate names it. The genuinely reachable decision-changing branches are D1 (INCONCLUSIVE), D3 (FALSIFIES) and D4 (MIXED).
- **D3 BEHAVIOURAL-DISTINCTION**: at novelty ≥ 0.5 on ≥1 family, measured treatment http/task ≤ cold − 1.0 and ≤ retrieval − 1.0, and treatment counter-sum cost/success < both comparators. Fail → `status=COMPLETE, outcome=FALSIFIES`.
- **D4 CONTROLS**: PC fires; NC-FULLY-SPECIFIED and NC-EMPTY-REGISTRY remain null; KNOWN-NEGATIVES refusal ≥ 0.95. Fail with D1–D3 passed → `status=COMPLETE, outcome=MIXED` naming the failing control.
- D0∧D1∧D2∧D3∧D4 → `status=COMPLETE, outcome=SUPPORTS`.

## s10 Validity threats and preemptions

1. **Grant-schedule fairness (highest risk).** The rate limit is a uniform environment dynamic applied to every arm; the treatment succeeds because it makes 1/K session creations, not because it is exempt. Director prior #6 explicitly treats server-side access control as legitimate environment dynamics. The NCs prove the advantage additionally requires the parameterized registry: at K=1 or with an empty registry the treatment ties cold.
2. **Support-grammar brittleness.** Training and test banks share the frozen grammars in s3; the DESIGN liveness probe validated an unseen in-support token/id → `EXECUTABLE` and an out-of-support id → refusal. KNOWN-NEGATIVES re-checks at EXECUTE.
3. **Carrier URL-shape constraint.** Frozen (fixed authority, exactly one varying final path segment) and probe-validated; otherwise the id slot would be mis-derived.
4. **Comparator identity.** Cold and retrieval are distinct (retrieval adds a stale replay, `retrieval_calls`, `repair_attempts`), and both differ from treatment by frozen policies, not by post-hoc tuning.
5. **Ceiling/floor.** Frozen at comparators 0.825/0.85 and treatment 1.0; both inside the [0.80, 0.95] envelope that makes the bank non-degenerate but non-trivial.
6. **Cost-metric completeness.** The primary metric is symmetric (http/task); the secondary counts all four honest counters; `latency_ms` carries no weight.
7. **Attribution.** B-LITERAL-KERNEL and NC-EMPTY-REGISTRY remove the parameterized registry; NC-FULLY-SPECIFIED removes retention.
8. **Scope.** Novelty-monotonicity is C-RESIDUAL-NOVELTY's own later gate; this packet only certifies that the bank SUPPORTS the gradient and reports per-level values as an exploratory readout, not a decision.
9. **Model-free.** No LLM; `model_calls=0`; the later four-arm benchmark owns the model arm.

## s11 Consequences

**Positive.** C-MEAS-VALID advances from EXPERIMENTAL: runtime ships `ASYM-DISC-A` (server, deterministic task-bank generator, arithmetic certificate, run harness) as a certified measurement-valid credential-free substrate whose bank is arithmetically and measured non-degenerate with discriminating session/auth positive and null controls (next_gate satisfied for the session/auth family). Product may fund the four-arm C-LLM-INHERIT / C-RESIDUAL-NOVELTY benchmark on this bank (readiness condition 2). The handoff carries the frozen substrate contract, certified certificate and measured confirmation for reuse.

**Negative.** If D2 fails: the asymmetric-discovery thesis is bounded on this class a second time; the handoff records the exact structural reason and the smallest next design direction (stochastic dynamics, selection ambiguity with real verification cost, or a non-REST substrate) so the program stops re-testing the unsatisfiable class. If D3 fails: carrier/harness repair in the owning scope, not a benchmark. C-MEAS-VALID stays EXPERIMENTAL with the session/auth gate unmet; no four-arm benchmark is funded.

## s12 Freeze scope and audit conformance

`freeze_artifacts` is empty with `freeze_artifacts_bound = NOT_APPLICABLE` for the reason recorded in `spec.json`: no mutable local file exists at DESIGN time whose identity can change interpretation, and the DESIGN stage scope (`scripts/check_scope.py` stage=design admits only `spec.json`, `prereg.md`, `design_review.json`, `failure.json`, `model_design*.json`) forbids DESIGN from creating code files. Interpretation is bound by the packet's freeze-identifier-and-protocol rule: the full substrate contract, bank generator, arm policies, counters and decision rule are frozen verbatim in `spec.json`/`prereg.md` (hash-frozen by `freeze.json`); the treatment carrier is pinned by blob id `b15ed848` + sha256 `718efa6a...` (plus models/registry hashes) on `origin/lab2/product`; EXECUTE transcribes code into `research/runtime/asym_disc/` from the frozen contract, records every produced file's sha256 in `result.json.artifacts`, and reproduces the certificate exactly; AUDIT verifies byte-level conformance of the transcribed code to this contract and recomputes the certificate. Expected layout: `research/runtime/asym_disc/{server.py,task_bank.py,certificate.py,run_experiment.py,audited_spider/*}`; raw logs under `research/experiments/EXP-RUNTIME-37999040476/artifacts/`.

Note for AUDIT: the substrate deliberately makes discovery fail for per-task re-derivers via a uniform rate limit. If the measured success of cold/retrieval differs from 0.825/0.85, treat it first as a conformance question (did the implementation honor the grant schedule and arm recipes?), i.e. D1, before reading it as a scientific result.
