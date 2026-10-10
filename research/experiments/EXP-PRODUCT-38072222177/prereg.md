# EXP-PRODUCT-38072222177 preregistration — Product lane

Experiment: `EXP-PRODUCT-38072222177`  Lane: `product`  Claim: `C-PARAM-INHERIT`
Design contract: v2. Frozen request: `request.json` (immutable). Base SHA: `edd1f3803bdd49f7434e10bfe7a52b775906361a`.

## 0. Mandate and scope

The Global Research Director's mandate (`request.json.director_mandate`) is binding: `action=CONTINUE`,
target claim `C-PARAM-INHERIT`. This experiment lands the already-audited parameterized-inheritance
carrier (`research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py`, git blob
`b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256
`718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`) byte-identically at the shipped
path `src/spider/kernel.py`, evidenced by a pre-freeze arm-differentiation certificate with:

(i) a known-positive inherited-parameter round trip on a **real task**;
(ii) a known-negative refusal case;
(iii) an explicit treatment-vs-`INSTRUCTIONS` contrast showing the shipped-kernel treatment differs;
(iv) shipped-kernel identity and promoted tests;
(v) promotion-pinned accounting.

Explicitly **NOT** run: the four-arm benchmark (T-SPIDER-PARAM / B-COLD-RE-DERIVE / B-RETRIEVAL-SHAPED /
B-LITERAL-KERNEL success-rate or budget semantics) or any real-LLM benchmark. This experiment does not
promote the claim; it produces a promotion-pinned certificate the AUDIT/DIRECTOR stages consume.

## 1. Carried evidence (not re-tested)

- `EXP-PRODUCT-37950607128` established the arm-differentiation certificate on synthetic
  `SYNTH-INDUCTION-BANK-v1` (audit PASS, `producer_claim_supported=true`), but `promote=False`, no claim
  advance — the carrier was never shipped.
- `EXP-PRODUCT-37973256064` audit PASS on 15 held-out identifiers (12 executed), documenting the
  support-generalization boundary.
- `EXP-PRODUCT-37989728440` (parent) built the real localhost HTTP substrate (`substrate.py`), showed the
  carrier 40/40 on the real task and 30/30 on its negatives, but its four-arm dynamic-range certificate
  failed (all arms at the 1.0 ceiling). This experiment reuses that substrate as a **frozen real task
  bank** and defines the contrast on success/abstention discriminability rather than on success rate.

## 2. Design (frozen inputs and the one new apparatus)

Frozen inputs are pinned by `freeze_artifacts` and re-hashed into `freeze.json.artifact_hashes`:

| artifact | role | sha256 |
|---|---|---|
| `EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` | treatment bytes (installed at `src/spider/kernel.py`) | `718efa6a…bfb72` (blob `b15ed848…ebf796`) |
| `EXP-PRODUCT-37989728440/harness/substrate.py` | real localhost HTTP task bank + environment | `0f9f9182…5af` |
| `EXP-PRODUCT-37950607128/harness/fixture.py` | frozen synthetic bank | `b0ffcbba…6cf` |
| `EXP-PRODUCT-37950607128/harness/run_certificate.py` | frozen synthetic scoring engine | `59895ddd…970` |
| `src/spider/models.py` | shipped support (unchanged) | `338aaf4d…978` |
| `src/spider/registry.py` | shipped support (unchanged) | `51fb440d…32c` |
| `src/spider/__init__.py` | shipped support (unchanged) | `3d173722…a77` |
| `tests/test_kernel.py` | existing regression suite | `ff9c1561…0b6` |

`src/spider/kernel.py` is deliberately **excluded** (it is the treatment subject EXECUTE replaces); C0
pins it to the carrier artifact above.

Tier 1 (synthetic, fully frozen): the frozen runner (grammatically: imports `spider.kernel` at the
shipped path, `fixture` from `harness/`) exercises positives F1–F6, 24 negatives, the action-identity
contrast and its degenerate-variant injection, accounting fidelity, identity binding and the literal
floor. EXECUTE byte-copies `fixture.py` and `run_certificate.py` into `harness/`; a copy whose sha256
does not equal the frozen hash invalidates the measurement.

Tier 2 (real, frozen substrate + one EXECUTE-authored deterministic driver): EXECUTE byte-copies
`substrate.py` into `harness/` and authors `harness/run_real_certificate.py`, a deterministic driver
with **no tunable parameters** that provides the mandate's real-task items (i) and (iii). It imports the
shipped `spider` package (to certify the shipped path, not the carrier copy) and the frozen substrate,
and its sha256 is recorded in `provenance.json`; every decision quantity is recomputed by AUDIT from the
raw request/response and resolve-decision logs. Because the driver does not exist at freeze it cannot be
listed in `freeze_artifacts`; the real task bank and environment it depends on (`substrate.py`) is bound,
and all thresholds are frozen in this prereg and `spec.json` (§5).

## 3. Pre-freeze arm-differentiation certificate (satisfiability, no outcome data)

- **Arms differ by construction, and the contrasts are sensitivity-bearing.**
  - Treatment `T-SPIDER-SHIPPED`: `distill_parameterized` over real training demonstrations induces a
    mechanism with slots; `resolve` rebinds them to a held-out identifier; the bound action contains the
    held-out id and executes live.
  - `B-INSTRUCTIONS`: literal demonstration replay (no slots, no guard) whose action contains the
    *training* id, so it cannot succeed on held-out ids and never abstains on out-of-support ids.
  - `B-LITERAL-KERNEL`: confidence `0.5 < 0.8` → `EXPLORE`, 0 held-out executables.
  - `B-SHIPPED-PRE-INSTALL`: parameterized symbols absent, positive arm unreachable.
- **Arithmetic bound.** Real success >= 5/5; a small fixed refusal battery; synthetic 6/6 and 24/24;
  real equivalence discriminators `== 1.0`; literal floor 0; exit code 0. No outcome depends on an
  unbounded/stochastic quantity.
- **Total precedence.** `spec.json#decision_rule.precedence` is ordered (BLOCKED → C0 →
  C1–C7 FALSIFIES → C8–C12 MEASUREMENT_INVALID → SUPPORTS); the region {a core fails and an integrity
  check fails} is assigned to FALSIFIES, so no evaluated state is undefined.
- **No ceiling/floor trap.** `B-COLD-RE-DERIVE` at novelty 0.0 can reach the correct action, so it is a
  reported cost reference and explicitly **non-gating**. The gated real contrast (C3) is an equivalence
  test between the treatment and `B-INSTRUCTIONS`: its discriminators are `== 1.0` only when the
  treatment binds (success `1.0`) and refuses (refusal `1.0`); a treatment that behaves like
  `B-INSTRUCTIONS` (failing to bind or over-accepting) drives them to 0, and the degenerate injection
  makes that collapse explicit. The synthetic contrast (C6) is credited only after EXECUTE/AUDIT verify
  from the raw certificate JSON that all treatment actions are non-null and `EXECUTABLE`, so it cannot be
  passed by a broken treatment via `None != action`.

## 4. Design-time satisfiability probes (NON-CONFIRMATORY)

Run in DESIGN against isolated `/tmp` copies; they consume no frozen confirmatory bank identifier and hit
no commit path.

**Probe 1 — treatment liveness canary.** Carrier copied to the shipping position with the shipped
`models.py`/`registry.py`/`__init__.py`; two toy `update` observations with varying URL identifier
segment. Observed:

```
mechanism: {'id': 'mech-9cbc18e671b64563', 'slots': ['value', 'doc'], 'confidence': 0.9}
resolve: EXECUTABLE {'json': {'value': 'v9'}, 'method': 'PUT',
         'url': 'http://127.0.0.1:9000/api/doc/doc-044/update'}
literal confidence: 0.5
literal resolve: EXPLORE
```

Interpretation: the carrier at the shipping position induces a parameterized mechanism
(`confidence 0.9 ≥ 0.8`), rebinds an unseen identifier (`doc-044`) into an `EXECUTABLE` bound action,
and the shipped literal floor is preserved (`0.5 → EXPLORE`).

**Probe 2 — baseline reachability.** The shipped kernel (`src/spider/kernel.py`, base SHA) lacks
`distill_parameterized`, `_infer_support`, `_support_accepts` and `TrajectoryCounters` (verified
absent); it does already define `_bind`. The parameterized positive arm is therefore unreachable
pre-install; C0 strengthens the frozen runner's weaker identity check (which only asserts a blob was
recorded) with a sha256/git-blob equality gate.

**Probe 3 — frozen-artifact hashes.** Recorded at DESIGN (table in §2); the freezer re-hashes them into
`freeze.json.artifact_hashes`.

No confirmatory bank identifier, real held-out identifier, or arm success metric is produced by these
probes.

## 5. Treatment, comparator, controls, and exact pass conditions

Controls (stable ids reused downstream): `T-SPIDER-SHIPPED` (treatment), `B-INSTRUCTIONS` (mandate
comparator, deterministic proxy), `B-LITERAL-KERNEL` (shipped floor), `B-SHIPPED-PRE-INSTALL` (identity
baseline), `B-RETRIEVAL-SHAPED` (frozen synthetic comparator, non-gating), `B-COLD-RE-DERIVE` (reported,
non-gating), `PC-PARAM-BINDING` (positive control), `PC-NULL-REFUSAL` (null control / emptied registry).

Pass conditions (full text in `spec.json#decision_rule.checks`):

- **C0 identity**: installed sha256 `== 718efa6a…` and blob `== b15ed848…`; siblings unchanged; all
  `freeze.artifact_hashes` match; harness copies match frozen hashes. (gate: MEASUREMENT_INVALID)
- **C1 real positive**: >= 5 disjoint held-out in-support ids, both families, novelty 0.0; resolve
  `EXECUTABLE`, bound action contains the held-out id, live HTTP 200 with `body.success true`,
  `verify()` true; success `== 1.0`. (FALSIFIES)
- **C2 real negative**: out-of-support / missing-param / wrong-intent → non-`EXECUTABLE`,
  `bound_action == null`, non-empty reason; refusal `== 1.0`, zero executions. (FALSIFIES)
- **C3 real INSTRUCTIONS contrast**: equivalence test over the frozen cases (`prereg.md#real-tier-cases`):
  treatment success `== 1.0` and INSTRUCTIONS success `== 0.0` (discriminator `== 1.0`); treatment refusal
  `== 1.0` and INSTRUCTIONS refusal `== 0.0`; treatment action non-null on all held-out cases; degenerate
  injection (treatment := INSTRUCTIONS) collapses both discriminators to `0.0` and is flagged.
  (FALSIFIES)
- **C4/C5/C6 synthetic**: frozen runner AD-POSITIVE `6/6`, AD-NEGATIVE `24/24`, AD-TREATMENT-CONTRAST
  real rate `== 1.0` and `degenerate_variant_detected == true`, with EXECUTE/AUDIT verifying from the raw
  certificate JSON that all treatment actions are non-null and `EXECUTABLE`. (FALSIFIES)
- **C7 promotion suite**: `compileall -q src` exit 0; `unittest discover -s tests` exit 0 (existing
  `tests/test_kernel.py` + new `tests/test_ship_kernel.py` whose required assertions T1–T5 are enumerated
  in `#required-promotion-regression-test` and verified non-vacuous by AUDIT); `validate_repo.py` exit 0.
  (FALSIFIES)
- **C8 literal floor**: literal confidence `< 0.8`; 0 held-out `EXECUTABLE` synthetic and real.
  (MEASUREMENT_INVALID)
- **C9 accounting**: the frozen `PC-ACCOUNTING-FIDELITY` check deliberately builds a seeded scripted
  trajectory with `scripted.add` (declared `retrieval_calls=3, verification_calls=2, repair_attempts=1`,
  plus an injected model event) to test counter arithmetic; on the actual execution path the harness must
  not hand-set counters (only the shipped kernel increments them), verified by recomputation from raw;
  observed `model_calls == 0`, `model_tokens == 0`, injected event labelled injected-not-observed.
  (MEASUREMENT_INVALID)
- **C10 pre-install unreachable**: probed from the immutable `base_sha` bytes
  (`git show <base_sha>:src/spider/kernel.py`, blob `cfec9866…`) loaded in isolation, not from the
  post-install `src/spider/kernel.py`; the positive arm raises `AttributeError`. (MEASUREMENT_INVALID)
- **C11 no benchmark**: no four-arm arm executed; observed `model_calls == 0`. (MEASUREMENT_INVALID)
- **C12 real-HTTP validity**: substrate live (`validity == true`), non-200 for malformed/literal cases,
  loopback only. (MEASUREMENT_INVALID)

Outcome precedence is total (BLOCKED → C0 → C1–C7 FALSIFIES → C8–C12 MEASUREMENT_INVALID → SUPPORTS).

### Real-tier cases (frozen construction; anchor `prereg.md#real-tier-cases`)

To leave the EXECUTE driver no selection or threshold freedom, the real tier's cases and predicates are
fixed here (hashed in `freeze.json.hashes`); the driver is a mechanical transcription of this section.

- **Task bank.** Training tasks = `substrate.build_train_tasks()`; held-out tasks = `substrate.build_test_tasks()`
  (frozen `substrate.py`). **Held-out positive set = all** of `build_test_tasks()` evaluated at novelty 0.0
  (>= 5 tasks spanning both families); no subset selection is permitted.
- **Demonstrations.** For each training task: `server.set_scenario(build_scenario(task))`, then
  `GET /api/session`, `GET /api/resources`, `GET /api/schema/{resource_type}`, then
  `POST /api/{resource_type}/{target_identifier}/update` with header `X-Session-Token` from
  `/api/session` and JSON `{property: target_property, value: target_value}`. Record one
  `update_resource` `Observation` per task with `state={family, resource_type, base_url}` and the exact
  action executed. Induce one mechanism per `(family, resource_type)` with `distill_parameterized`.
- **Positive execution.** For each held-out task: `set_scenario`; the `resolve` params are derived from
  the discovered slot names by a fixed mapping — an id-named slot (`id`/`doc`/identifier-named) or any
  otherwise-unmapped slot receives `target_identifier`, a property-named slot receives `target_property`,
  a value-named slot receives `target_value`, and a token-named slot receives the fresh session token;
  `resolve` must return `EXECUTABLE` with a non-null bound action whose URL contains the held-out
  identifier; execute that action; success predicate = `status == 200 AND body.success is True`;
  `verify()` must return true.
- **Negative cases (fixed composition).** For each held-out task, three cases: (a) out-of-support id =
  replace the held-out id with `doc-999` for type `doc` and the analogous out-of-prefix id for the other
  type; (b) missing-param = call `resolve` with the identifier-bearing slot omitted; (c) wrong-intent = call `resolve`
  with intent `"wrong_intent__" + intent`. Refusal predicate = `status != EXECUTABLE AND bound_action is
  None AND reason` is a non-empty string; no case may execute an HTTP action.
- **INSTRUCTIONS (`B-INSTRUCTIONS`).** For each held-out task, take the verbatim update action recorded
  for the first training task of the same `(family, resource_type)` (an action targeting a training
  identifier) and execute it unchanged with a fresh session token; success uses the same predicate.
  Refusal is defined as never abstaining (it always attempts the literal action), so its refusal rate is
  0.0 by construction; its success rate is `== 0.0` (required, not merely expected) because the training
  identifier is absent from
  the held-out scenario.
- **Degenerate injection.** Recompute C3 with the treatment results replaced by the `B-INSTRUCTIONS`
  results; both discriminators must become 0.0 and be flagged.
- **Accounting.** No `TrajectoryCounters` field is hand-set by the driver; the shipped kernel increments
  `retrieval_calls` on `resolve` and `verification_calls` on `verify`, and the driver only reads them.

### Required promotion regression test (`tests/test_ship_kernel.py`)

Because `tests/test_ship_kernel.py` is EXECUTE-authored and ships in the promotion diff, its required
assertions are frozen here (binding via `freeze.json.hashes["prereg.md"]`) so C7 cannot be satisfied by a
vacuous test. The test file MUST import the installed `spider` package (no network, no model calls) and
assert, with concrete expected values/statuses:

- `T1` parameterized round trip: `distill_parameterized` over >= 2 in-support observations returns a
  mechanism with >= 1 slot and `confidence >= 0.8`; `resolve` with a bound held-out identifier returns
  status `EXECUTABLE` with a non-null `bound_action` whose URL contains that identifier.
- `T2` literal floor: `distill()` on the same observations returns `confidence == 0.5` (`< 0.8`), and the
  resulting `resolve` returns a non-`EXECUTABLE` status (not `EXECUTABLE`).
- `T3` refusal: a wrong-intent and an out-of-support `resolve` each return a non-`EXECUTABLE` status with
  `bound_action is None` and a non-empty `reason`.
- `T4` counter ownership: after one `resolve` and one `verify`, `TrajectoryCounters.retrieval_calls == 1`
  and `verification_calls == 1`, incremented by the kernel (not set by the test).
- `T5` non-vacuity: the same test module, run against the pre-install kernel bytes (C10), fails with
  `AttributeError` on `distill_parameterized`; AUDIT verifies the file contains these exact
  status/value assertions (no `assertTrue(True)` placeholders).

AUDIT independently re-parses the test file and confirms each frozen assertion is present and specific
to the listed status/value; the raw result of `unittest discover` is recorded in `result.json`.


## 6. Procedure (EXECUTE, exactly as frozen)

1. Verify `freeze.json.artifact_hashes` against the working tree; abort to MEASUREMENT_INVALID on any
   mismatch, or BLOCKED if a prerequisite file is missing.
2. Byte-copy the carrier to `src/spider/kernel.py`; assert C0. Byte-copy `models.py`/`registry.py`/
   `__init__.py` unchanged; byte-copy `fixture.py`, `run_certificate.py`, `substrate.py` into `harness/`
   and re-hash.
3. Tier 1: run the copied `run_certificate.py` against the installed shipped kernel; preserve
   `raw_fixture/` and `raw_certificate/`. (Its embedded `EXPERIMENT_ID` is the instrument's origin
   `EXP-PRODUCT-37950607128`; this is disclosed and not rewritten.)
4. Tier 2: run `harness/run_real_certificate.py`: start the frozen `SubstrateServer` on 127.0.0.1;
   capture training demonstrations for both families (`GET /api/session`, `GET /api/resources`,
   `GET /api/schema/{type}`, then `POST /api/{type}/{id}/update` with the discovered session token and
   the task property/value); induce one mechanism per `(family, resource_type)` via
   `distill_parameterized`; resolve the held-out in-support batch (>= 5 ids, novelty 0.0), execute live
   and `verify()`; run the negative battery; run `B-INSTRUCTIONS` (literal training action replay) and
   the degenerate injection; persist every raw request/response, server log and resolve decision.
 5. Write `tests/test_ship_kernel.py` implementing the frozen assertions T1–T5
    (`#required-promotion-regression-test`) and run the promotion suite.
6. Compute metrics from raw; write `result.json` / `report.md` / `provenance.json` per
   `research/EXPERIMENT_PACKET.md`; record `execution_checkpoint.json.pre_execute_sha` for
   promotion-pinned accounting.

## 7. Validity threats and disclosures

- **`INSTRUCTIONS` proxy:** `B-INSTRUCTIONS` is a deterministic literal-replay stand-in for a real LLM
  `INSTRUCTIONS` arm; it establishes separability (action identity + success + abstention), **not**
  benchmark superiority over a real instruction-following LLM.
- **EXECUTE-authored real-tier driver:** the driver is a mechanical transcription of the frozen
  `#real-tier-cases` section with no selection or threshold freedom; the exact task bank
  (`substrate.py`) and the exact held-out set, negative composition, success/refusal predicates,
  INSTRUCTIONS action and degenerate injection are frozen in this prereg (hashed in `freeze.json.hashes`).
  Its sha256 is recorded in provenance, and AUDIT verifies the raw logged cases equal these rules and
  recomputes every metric. It cannot be freeze-listed because it does not exist at freeze and
  `freeze_artifacts` requires existing files.
- **Synthetic bank reuse:** `SYNTH-INDUCTION-BANK-v1` is small and author-designed; results are a
  certificate, not generalization evidence beyond it.
- **Hard-coded runner id:** the frozen runner embeds `EXP-PRODUCT-37950607128`; disclosed, not an
  identity claim for this experiment.
- **Weaker built-in identity check:** the frozen runner's `AD-IDENTITY-BINDING` only asserts a pre-blob
  was recorded; C0 is the authoritative identity gate.
- **Injected model counters:** the frozen `PC-ACCOUNTING-FIDELITY` check deliberately injects a synthetic
  `model_calls=1` / `model_tokens=128` event; it is labelled injected-not-observed and is not real model
  usage. Observed `model_calls`/`model_tokens` are `0`.
- **Loopback HTTP:** the "real task" is a localhost server, not the open Web; it is real
  request/response execution with server-side state verification, not Web-scale generalization.
- **Novelty 0.0 selection:** the real positive tier uses novelty 0.0 because the parent degeneracy lives
  there; this is the worst case for arm differentiation, which is why the gated contrast is an
  equivalence test against `B-INSTRUCTIONS` (success and abstention) rather than success rate alone.
- **No claim self-promotion:** only a certificate and a promotion recommendation are produced; claim
  adjudication is downstream.

## 8. Consequences

Positive (all C0–C12 pass): the audited parameterized-inheritance mechanism is established on the shipped
path on a real task with refusal, INSTRUCTIONS separation, identity and accounting; the product lane may
ship the installed bytes (via `product-promote.yml`'s `src tests` diff) and proceed to
integration/economics work, bounded to in-support held-out identifiers from an observed family.
Negative (`FALSIFIES`): do not promote; the failing check names the next bounded repair.
`MEASUREMENT_INVALID`: the instrument, not the mechanism, is the problem — repair the named gate and
re-run. `BLOCKED`: restore the missing prerequisite or grant scope.
