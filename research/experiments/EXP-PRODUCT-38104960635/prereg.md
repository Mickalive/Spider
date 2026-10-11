# Preregistration: EXP-PRODUCT-38104960635

Lane: `product`  •  Claim: `C-PARAM-INHERIT`  •  base_sha: `d77b4f54e90ef4af8aff5b1cc991a00a0c73374f`  •  design_contract_version: 2

This experiment is the Product-lane implementation of the Global Research Director's binding mandate
(`request.json.director_mandate`, cycle `38104396391`, `action=CONTINUE` on `C-PARAM-INHERIT`,
`cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`). The director's question is reproduced
verbatim in `spec.json.question`. The parent's proposed four-arm `C-LLM-INHERIT` economics benchmark is
explicitly NOT this experiment's question and is NOT run here.

---

## 1. Binding strategic question (Director mandate)

> Can the audited parameterized inherited carrier be landed into the shipped kernel through the sanctioned
> promotion path so that after promotion the shipped execution path contains a concrete parameterized
> mechanism that an inherited procedure visibly instantiates and executes, together with a companion
> known-negative refusal certificate - satisfying blocker B1 and the pre-freeze executable-mechanism
> requirement of readiness condition (1) - rather than once more running the four-arm economics benchmark
> on a kernel that still emits literals below the execution threshold?

Mandate constraints that are binding on this design:

- `parent_handoff_disposition=SUPERSEDE`: this experiment must NOT drift back to the parent
  `next_question` (the four-arm benchmark or the asymmetric-discovery substrate fallback). Those are not
  measured here.
- The excluded fourth deterministic-REST certificate re-run remains excluded. This experiment does not
  compute, assert or re-run any dynamic-range certificate.
- The mandate names the audited promotion path `product-promote.yml` with explicit positive/negative
  tests, one known positive and one known negative, and a pinned shipped version, as the required output.
- This is a SHIPMENT / PREREQUISITE result. It is not an economics result and not a generalization result.

## 2. Inherited parent state that is explicitly preserved (EXP-PRODUCT-37989728440)

Read from `research/experiments/EXP-PRODUCT-37989728440/handoff.json` (sha256
`911f765d04a83974f20d113da206b4075337c3a9bed4c5a77a8f06ffb4773ed9`). These distinctions are inherited
scientific state and are not silently rewritten.

### 2.1 Established (carried forward, not re-measured here)
- Frozen-input and treatment-carrier integrity: the audited carrier is byte-identical to git blob
  `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` (sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`);
  shipped `src/spider/kernel.py` is unchanged git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50`.
- The parent's deterministic run was measurement-valid for its own arms (C2, C6-C11 PASS): all four arms
  reached success_rate 1.0; known negatives refused 30/30 with `bound_action=null`; `model_calls=0`,
  `model_tokens=0`; B-LITERAL-KERNEL 0.0 (200/200 EXPLORE) vs PC-EXACT-REPLAY 20/20 (C9 PASS). The
  kernel's parameterized path IS causally necessary on that substrate.
- Bounded substrate-class negative (certificate): the pre-freeze dynamic-range certificate is false at
  design and observed on the mandatory-discovery deterministic credential-free REST class (C1 FAIL).
- Bounded substrate-class negative (economics): on deterministic counters the treatment ties cold at
  novelty >= 0.25 and is worse at 0.0; vs retrieval it is a flat +2 `retrieval_calls`, rho=0.0, p=1.0; C5
  FAILS. C3's apparent pass is `latency_ms/1000` noise (C3_counter_only=false).
- Governance fact: the freeze step does not enforce the C1 certificate (`spec.json` has no
  `dynamic_range_certified` field; `scripts/freeze_experiment.py` has no such check).
- Director ruling: the frozen OVERALL row `FALSIFIES` governs the parent's scientific outcome; the
  pre-freeze MUST-NOT-FREEZE clause is preserved as a governance defect on C-MEAS-VALID.

### 2.2 Rejected (bounded to the parent substrate class / instrument)
- That a certified dynamic range can be produced on the mandatory-discovery deterministic credential-free
  REST substrate with this arm design.
- That T-SPIDER-PARAM saves `http_requests` vs cold or shows novelty-scaling counter-only advantage there.
- The latency-inclusive `cost_per_success` as a discriminating instrument on that substrate.
- That the freeze step enforces C1 by reading `spec.json.dynamic_range_certified`.

### 2.3 Unknown (not closed by the parent)
- Whether ANY credential-free deterministic substrate can exhibit a certified dynamic range for that arm
  design. Whether asymmetric/amortized discovery would let the treatment save work vs cold. Whether the
  external four-arm benchmark can run (blocked on Intel model-endpoint provisioning). Whether applying
  support predicates to free-form payload values is a kernel defect. When the freeze gate will be
  repaired. The registry-vs-Codex status discrepancy for C-RESIDUAL-NOVELTY / C-FRESHNESS.

### 2.4 Do not assume (unsafe assumptions this experiment respects)
- Do not read the parent packet as evidence for or against C-RESIDUAL-NOVELTY; C1 is false so the frozen
  economics test was non-discriminating by construction.
- Do not treat cold/retrieval success_rate 1.0 as evidence inheritance lacks value (deterministic ceiling
  with mandatory symmetric discovery).
- Do not treat the parent's 40/40 success or C3/C4 "PASS" as work compression.
- **Do not assume the shipped `src/spider/kernel.py` contains the parameterized path** - it does not. This
  experiment is precisely the mandated action that removes that unsafe assumption; it must not inherit the
  parent's promotion refusal (`promote_to_product=false`) as a permanent block, because the mandate
  supersedes the parent's agenda and authorizes exactly this landing.
- Do not assume the pre-freeze C1 certificate gate is enforced - it is not. This design therefore makes NO
  dynamic-range claim and touches no certificate.
- Do not re-run the mandatory-discovery deterministic REST certificate; do not generalize the parent's
  substrate workaround (target values kept inside the induced support grammar) into a free-form
  support-generalization result; do not read `model_calls=0` as a measured zero-cost claim.

### 2.5 What this experiment changes relative to the parent
The parent refused promotion because its own frozen gate failed (C1/C5) and its audit was REVISE. That
refusal is about the parent's economics claim, not about the carrier's landability. This experiment takes
the SAME audited carrier and measures a disjoint object: the shipped-path behavior and the promotion
landability of the carrier delta, with its own positive/negative certificates. It inherits the carrier's
integrity and the parent's causal-necessity finding, and it inherits none of the parent's economics claims.

## 3. Claim under test

`C-PARAM-INHERIT` - "Mechanisms parameterize to unseen identifiers" (registry status EXPERIMENTAL).
The claim's registered next gate ("learn on resource A, succeed on never-observed B against
cold/replay/retrieval baselines") is NOT satisfied by this experiment. This experiment only removes
blocker B1 / readiness condition (1) by landing the executable carrier and producing the positive and
known-negative refusal certificates. It must not advance the claim status; the deferred four-arm benchmark
remains the gate.

## 4. Arms and identities

All arms share: the same localhost stdlib HTTP server and the same fixed `base_url` (ephemeral port chosen
once per run); the same intent `update_resource`; the same context `{"authenticated": true, "role":
"owner"}`; the same `SpiderKernel(min_confidence=0.8)` default; and the same params shape.

| id | role | definition | expected |
|----|------|------------|----------|
| `T-LANDED-PARAM` | treatment | landed `src/spider/kernel.py` (must equal carrier sha256 `718efa6a...`) imported via `PYTHONPATH=src` as `spider.kernel`; mechanism induced by `distill_parameterized` | 2/2 unseen in-support -> EXECUTABLE + real HTTP execute + `verify()==True`; conf 0.9 |
| `B-LITERAL-ABLATION` | causal ablation | the same landed file's literal `distill()` (confidence 0.5, no slots) in a fresh registry, same inputs | 0/2 EXECUTABLE; EXPLORE, `bound_action=null` |
| `N-EMPTY-REGISTRY` | null control | fresh kernel over an empty registry, same inputs | 0/2 EXECUTABLE; UNKNOWN, `bound_action=null` |
| `PC-SUPPORT-BOUNDARY` | two-sided sensitivity control | accept unseen in-support (`doc-555`, `rec-999`) and refuse near-miss (`doc-55`, `rec-55`) | accept 2, refuse 2 with reason "outside inferred support" |
| `KN-OUT-OF-SUPPORT` | known negative | near-miss identifier | EXPLORE, `bound_action=null`, "outside inferred support" |
| `KN-MISSING-PARAM` | known negative | `resolve(intent, context, {})` | EXPLORE, `bound_action=null`, "missing required parameter" |
| `KN-WRONG-INTENT` | known negative | intent `delete` with the same context/params | UNKNOWN, `bound_action=null`, "no applicable validated mechanism" |
| `T-IDENTITY-CARRIER` | identity clause | sha256 and `git hash-object` of landed `src/spider/kernel.py` | == `718efa6a...` / `b15ed848...`; != `46929b3a...` |
| `N-ABSTENTION-NO-REQUEST` | null control | count server requests during all refused resolutions | 0 |
| `G-PROMOTION-LANDABILITY` | gate rehearsal | delta paths + the three `product-promote.yml` commands | delta ⊆ {src, tests}; compileall/validate_repo/unittest exit 0 |

Baseline identity is by CODE HASH, not by narrative: treatment == carrier hash; ablation == same file's
literal path; `B-PRE-LANDING-KERNEL` == sha256 `46929b3a...` / blob `cfec9866...` (identity only). The
treatment-vs-ablation contrast is a binary code-path difference on identical inputs, so no
ceiling/degeneracy assumption is needed for identifiability.

## 5. Fixtures and instrument

Substrate: `http.server.ThreadingHTTPServer` on `127.0.0.1:0` (ephemeral), stdlib only, no external
network, no model, no randomness. `POST /api/<type>/<id>` with JSON body `{"property": ..., "value":
...}` returns `200 {"ok": true, "document": <id>, "property": <property>, "value": <value>}`; all other
paths return 404. Server request count is recorded for `N-ABSTENTION-NO-REQUEST`.

| family | induction identifiers (A) | unseen in-support (B) | near-miss (C) | fixed token | values |
|--------|---------------------------|-----------------------|---------------|-------------|--------|
| docs | `doc-102`, `doc-247`, `doc-391` | `doc-555` | `doc-55` | `tok-a1b2c3d4e5f6a7b8` | `draft-1..draft-3` (test `draft-7`) |
| records | `rec-514`, `rec-628`, `rec-736` | `rec-999` | `rec-55` | `tok-9911aabbccddeeff` | `draft-1..draft-3` (test `draft-7`) |

Property is the constant `"title"`. Induction observations are `Observation("update_resource",
context, action, response_body, True)` where `action = {method:"POST", url:<base>/api/<type>/<id>,
headers:{Content-Type:"application/json", X-Session-Token:<token>}, json:{property:"title",
value:"draft-<i>"}}`. Each induction observation is captured from a REAL HTTP response. The induced
mechanism is upserted into a tempfile-backed `MechanismRegistry` (never the committed
`src/spider/mechanisms.jsonl`).

Instrument: one self-contained module `tests/test_product_param_promotion.py` that (a) exposes a scenario
runner returning a structured dict and (b) has unittest assertions for the durable certificate. It imports
`spider.kernel`, `spider.models`, `spider.registry` from `src/` via `PYTHONPATH=src`; it records
`spider.kernel.__file__` to prove shipped-path provenance. `python tests/test_product_param_promotion.py`
prints the raw JSON evidence block used as raw evidence.

DESIGN-time non-outcome-bearing satisfiability probes (run in `/tmp`, not part of the confirmatory
measurement, no experiment artifacts written) were used only to confirm that each fixture induces the
intended grammar and each branch is reachable; their results are recorded in section 12.

## 6. Decision rule (FROZEN before execution)

- **DR-1 treatment_identity (HARD):** sha256(`src/spider/kernel.py`) ==
  `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` AND `git hash-object` ==
  `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` AND != `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`.
- **DR-2 positive_roundtrip (HARD):** for BOTH families, unseen in-support resolves `EXECUTABLE` with
  non-null `bound_action` whose url targets the unseen identifier; that bound action executes over real
  HTTP; `verify(mechanism_id, response_body, params) == True`. `M-PC-ROUNDTRIP-EXECUTABLE-COUNT == 2`,
  `M-PC-ROUNDTRIP-VERIFY-COUNT == 2`.
- **DR-3 causal_ablation:** `B-LITERAL-ABLATION` returns `EXPLORE`, `bound_action=null`, both families;
  `M-ABLATION-LITERAL-EXECUTABLE-COUNT == 0`.
- **DR-4 known_negative_refusal (HARD):** all three KN categories refused, `bound_action=null`,
  non-empty typed reason; `M-KN-REFUSAL-RATE == 1.0`, `M-KN-REASON-CORRECT-COUNT == 3/3`. Reason predicate:
  out-of-support -> status in {EXPLORE,UNKNOWN} AND "support" in reason; missing -> "missing required
  parameter" in reason; wrong-intent -> status UNKNOWN AND "no applicable validated mechanism" in reason.
- **DR-5 null_control:** `N-EMPTY-REGISTRY` -> UNKNOWN, `bound_action=null`;
  `M-NULL-EMPTY-EXECUTABLE-COUNT == 0`.
- **DR-6 boundary_sensitivity:** `M-BOUNDARY-ACCEPT-COUNT == 2`, `M-BOUNDARY-REFUSE-COUNT == 2`.
- **DR-7 shipped_path_import:** resolved `spider.kernel.__file__` is under the repo `src/spider/`;
  `spider.kernel` exposes `distill_parameterized`, `resolve`, `verify`; no vendored copy used.
- **DR-8 promotion_landability:** experiment delta paths ⊆ {`src`, `tests`}, and specifically
  `src/spider/kernel.py` (carrier bytes) + `tests/test_product_param_promotion.py`; `python -m compileall -q
  src scripts` exit 0; `python scripts/validate_repo.py` exit 0; `PYTHONPATH=src python -m unittest discover
  -s tests -v` exit 0 (including the 3 pre-existing `tests/test_kernel.py` tests).
- **DR-9 freeze_integrity_and_accounting:** every `freeze_artifacts` sha256 unchanged from
  `freeze.json.artifact_hashes`; `M-MODEL-CALLS == 0`; `M-MODEL-TOKENS == 0`;
  `M-ABSTENTION-HTTP-REQUESTS == 0`.

Overall: `SUPPORTS` iff DR-1..DR-9 all PASS. `FALSIFIES` iff DR-1, DR-2 or DR-4 fails. `MIXED` iff
DR-1/DR-2/DR-4 pass but any of DR-3, DR-5, DR-6, DR-7, DR-8, DR-9 fails. `MEASUREMENT_INVALID` iff a
declared prerequisite is missing (carrier absent/hash mismatch; landed module cannot import; server cannot
bind; required python/git tooling unavailable). A missing prerequisite is never scored as a scientific
negative. `status=COMPLETE` with outcome `MIXED`/`FALSIFIES` is a valid scientific result, not an
infrastructure failure.

### 6.E The sanctioned promotion path: what is and is not measured here
`product-promote.yml` runs on `main` from a schedule/dispatch, requires a PASS `audit.json` and
`verdict.promote_to_product == true`, pins `SOURCE_SHA` to the commit that created `verdict.json`, takes
`BASE = execution_checkpoint.json.pre_execute_sha`, and applies only `git diff BASE SOURCE_SHA -- src tests
sdk pyproject.toml` after running the three commands in DR-8. EXECUTE cannot observe the main-branch
application: audit, verdict and the scheduled workflow are downstream of this transaction. Therefore this
experiment measures (i) the exact delta and its confinement to allowed roots, (ii) the exact validation
commands the workflow will run, and (iii) the pinned shipped identity. It does NOT claim that main was
merged; that is the DIRECTOR-authorized downstream step. This avoids the unreachable-branch defect of
`EXP-PRODUCT-38094123727`, which required an out-of-process merge and simultaneously froze the treatment
target.

## 7. Metrics (stable ids)

`M-SHIPPED-KERNEL-SHA256`, `M-CARRIER-KERNEL-SHA256`, `M-CARRIER-GIT-BLOB`, `M-PRE-LANDING-KERNEL-SHA256`,
`M-PC-ROUNDTRIP-EXECUTABLE-COUNT`, `M-PC-ROUNDTRIP-VERIFY-COUNT`, `M-BOUNDARY-ACCEPT-COUNT`,
`M-BOUNDARY-REFUSE-COUNT`, `M-KN-TOTAL`, `M-KN-REFUSAL-RATE`, `M-KN-REASON-CORRECT-COUNT`,
`M-ABLATION-LITERAL-EXECUTABLE-COUNT`, `M-NULL-EMPTY-EXECUTABLE-COUNT`, `M-ABSTENTION-HTTP-REQUESTS`,
`M-MODEL-CALLS`, `M-MODEL-TOKENS`, `M-EXISTING-TESTS-PASS`, `M-NEW-TESTS-PASS`, `M-VALIDATE-REPO-EXIT`,
`M-COMPILEALL-EXIT`, `M-DELTA-PATHS`, `M-DELTA-ALLOWED-VIOLATIONS`, `M-FROZEN-ARTIFACTS-UNCHANGED`.
All are deterministic integers/booleans/strings; no latency-derived or continuous metric is used as a
discriminator (the parent's C3 lesson).

## 8. Validity threats and mitigations

| Threat | Mitigation |
|--------|------------|
| Harness measured a vendored copy, not the shipped path | DR-7 records `spider.kernel.__file__` and requires it under `src/spider/`; MEASUREMENT_INVALID otherwise |
| Landing silently changes `models.py`/`registry.py`/`__init__.py` | those files are `freeze_artifacts`; DR-9 requires unchanged hashes |
| Reference solution mutates committed registry data | test uses a tempfile registry only |
| Support grammar too permissive/restrictive | two-sided boundary control plus digit-count near-misses |
| Positive result manufactured without a mechanism | empty-registry null + no-request abstention |
| Causality over-claimed | binary literal ablation at the 0.5 < 0.8 gate |
| Confirmatory measurement fabricated | raw HTTP response bodies preserved as raw evidence |
| Promotion "success" over-claimed | DR-8 measures local landability only; main merge is explicitly not claimed (6.E) |
| Localhost sockets unavailable on the runner | declared prerequisite; unbindable server -> MEASUREMENT_INVALID |
| Identity checks rely on git | sha256 is primary; `git hash-object` is corroborating; git absence is a prerequisite failure only for DR-8 |
| New test weakens the existing suite | `tests/test_kernel.py` is frozen; DR-8 requires all existing tests to still pass |

## 9. Consequences

Positive: B1 is closed at source and the pinned shipped version is available for the DIRECTOR to authorize
via `product-promote.yml`; readiness condition (1) is satisfied; B2/B3 and the deferred four-arm benchmark
are unblocked to be *scheduled*, not run here. Negative/MIXED: no promotion is authorized; the report
records the exact failing clause and the smallest repair. In both cases `C-PARAM-INHERIT` stays
`EXPERIMENTAL` - no self-promotion.

## 10. Comparative reasoning against pre-2.0 legacy

Per mandate `comparative_reasoning: LEGACY: NO_MATCH`. `codex/legacy_brief.json` was scanned for
parameter/instruct/replay: the closest precedents are `P2-REPLAY-COST` (sha
`9687ff787f2d74460bb7006826008852f5b4416b`, 1.002x cold-vs-replay, whose 8.5x claim was withdrawn) and the
bounded substrate-class negative EXP-PRODUCT-37989728440. Neither is a shipped-kernel promotion gate with
paired known-positive and known-negative certificates; this experiment makes no cost/economics claim and
does not replay either. No pre-2.0 artifact corresponds to what is measured here.

## 11. Artifacts to produce (EXECUTE)

- `tests/test_product_param_promotion.py` (promoted; durable positive/negative certificate)
- `src/spider/kernel.py` (landed; must equal carrier bytes)
- `harness/measure.py` (experiment-local; identity + scenario + validation-command runner; NOT promoted)
- `raw_evidence/server_log.jsonl`, `raw_evidence/scenario_outcomes.json`, `raw_evidence/unittest_output.txt`
- `derived/metrics.json`, `derived/decision_rule_eval.json`
- `result.json`, `report.md`, `provenance.json`

`freeze_artifacts` (bound, hashed): `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`,
`src/spider/models.py`, `src/spider/registry.py`, `src/spider/__init__.py`, `tests/test_kernel.py`.
`src/spider/kernel.py` is deliberately NOT frozen (EXECUTE must mutate it); its post-landing identity is the
HARD DR-1 clause instead.

## 12. Design self-attack (satisfiability probes, non-confirmatory)

Six mandatory v2 failure modes were attacked. All probes ran in `/tmp` against the carrier in a temp
package; no outcome-bearing experiment data was produced or inspected.

1. **Unreachable/empty decision branches.** None. Design probes on the exact fixtures produced: F1 induced
   slots `{value, doc}` with supports `{value: ^draft\-[0-9]{1}$, doc: ^doc\-[0-9]{3}$}` at confidence 0.9;
   unseen `doc-555` -> EXECUTABLE (`.../api/docs/doc-555`) and verify True; near-miss `doc-55` -> EXPLORE
   "parameter 'doc' outside inferred support"; missing -> EXPLORE "missing required parameter 'doc'";
   wrong intent -> UNKNOWN "no applicable validated mechanism". F2 symmetric (supports
   `^rec\-[0-9]{3}$`; `rec-999` EXECUTABLE+verify True; `rec-55` refused). `B-LITERAL-ABLATION` ->
   EXPLORE at confidence 0.5. `N-EMPTY-REGISTRY` -> UNKNOWN. So every DR clause can return either
   PASS or a distinguishable fail; no branch is empty or arithmetic-impossible.
2. **Missing prerequisites.** Carrier exists at the pinned blob/sha256; `models.py`/`registry.py` are
   byte-identical between carrier and shipped; shipped `__init__.py` already exports the imported names;
   the existing 3 `tests/test_kernel.py` tests PASS against the carrier in a temp package (`Ran 3 tests
   ... OK`). Missing prerequisites map to MEASUREMENT_INVALID.
3. **Ceiling/floor baselines.** The ablation is a floor at the hard 0.5<0.8 gate, not a correctness
   ceiling; the treatment is not assumed to succeed on any rate - success is checked per family on unseen
   identifiers, and the null/empty controls bound the false-positive floor. There is no comparator assumed
   to sit at a 1.0 correctness ceiling, so the parent's degeneracy trap cannot recur.
4. **Treatment/comparator identity.** Treatment and ablation are the SAME landed file; they differ only by
   code path (parameterized induction + support guards vs literal 0.5). Identity is enforced by sha256.
   The pre-landing kernel is pinned only for the before/after identity clause.
5. **Insensitive controls.** Ablation flips EXPLORE vs EXECUTABLE on a one-line code-path change; boundary
   control is two-sided (accept unseen, reject digit-count near-miss); three KN categories exercise three
   distinct guards with three distinct reasons; empty registry cannot execute; abstention asserts zero
   requests. If any control were insensitive the corresponding DR clause fails to `MIXED`, not to a false
   `SUPPORTS`.
6. **Unbound mutable artifacts.** Enumerated in `freeze_artifacts`; all exist and are hashed by the freezer.
   The treatment target is intentionally excluded and pinned by DR-1 instead. The prior attempt
   `EXP-PRODUCT-38094123727` failed precisely because it froze the treatment target AND required an
   unreachable out-of-process main merge; this design fixes both.

## 13. Freeze statement

Upon creation of `freeze.json` this spec and prereg are immutable. No outcome-bearing measurement may be
inspected before freeze. The decision rule in section 6 is binding. This experiment does not self-promote
`C-PARAM-INHERIT` and does not authorize product promotion by itself.
