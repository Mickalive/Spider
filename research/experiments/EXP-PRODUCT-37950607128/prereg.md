# EXP-PRODUCT-37950607128 preregistration

Experiment: `EXP-PRODUCT-37950607128`
Lane: `product`
Target claim: `C-LLM-INHERIT` (registry status unchanged at `HYPOTHESIS`)
Director mandate: cycle `37949204501`, action `PIVOT`, `claim_id` `C-LLM-INHERIT`, parent handoff disposition `USE`.

This document is a preregistration, not a result. It is frozen before any outcome
measurement. It must be read as a contract for EXECUTE and AUDIT and it may not be
edited after `freeze.json` exists.

---

## 0. Mandate reconciliation and the one DESIGN decision

The binding Director question asks whether the SHIPPED kernel executes an inherited
parameterized mechanism at a non-zero rate, demonstrated by a pre-execution
arm-differentiation certificate that is SHOWN TO FIRE on a synthetic fixture before any
expensive arm runs. It also warns that a sixth rerun of the old readiness gate is
forbidden, and that if the kernel path or model credential cannot be provisioned the
experiment must fail loudly rather than re-freeze the same gate.

The pre-DESIGN provisioning probe (Section 1) found the model credential definitively
absent and the kernel parameterized path definitively absent at HEAD. The single DESIGN
decision is therefore:

> This experiment is scoped to the credential-free half of the mandate: prove the shipped
> kernel can be made to execute an inherited parameterized mechanism with a demonstrated-
> firing arm-differentiation certificate, on a synthetic fixture, offline. It does NOT run
> the four LLM arms, so it does not need the model credential and the credential is not one
> of its gates.

Rationale, stated so an auditor can reject it if wrong: the mandated deliverable is a
certificate over kernel operations (distill -> resolve -> bind -> execute -> verify) plus
accounting counters, all of which are deterministic and none of which calls a model. The
model credential is a prerequisite only of the downstream four-arm benchmark that this
experiment exists to unblock. Reading the mandate's failure clause as "any named
prerequisite of the whole program is absent" would abort the one cheap repair the mandate
itself calls "cheaper than the credential" and would produce a sixth consecutive
information-free abort. Reading it as "a prerequisite of THIS certificate cannot be
provisioned" is the only reading under which the mandate's own deliverable is reachable.
The kernel path is provisionable inside Product's allowed code roots (`src`, `tests`,
`sdk`, `pyproject.toml`), so the certificate experiment proceeds. If EXECUTE finds that
any mandatory check actually needs a model credential it MUST emit BLOCKED with the exact
receipt rather than substitute a proxy.

This experiment is NOT the parent's identifier-level support-model question (assigned to
Graph) and NOT another isolation-level economics packet. It is the arm-differentiation
prerequisite named by the parent handoff and the audit.

---

## 1. Pre-DESIGN provisioning probe (exact receipt)

Run 2026-10-09 by DESIGN, read-only, no outcome measurement. These are artifact/environment
identity facts, not scientific data.

Environment probes (all recorded verbatim as observed):

- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_BASE_URL`, `ANTHROPIC_BASE_URL`,
  `OPENCODE_API_KEY`, `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `AZURE_OPENAI_API_KEY`,
  `HF_TOKEN`, `TOGETHER_API_KEY`, `GROQ_API_KEY`, `MISTRAL_API_KEY`, `OLLAMA_HOST`:
  all **UNSET**.
- `config/models.json`: roles contain only `opencode/*-free` and `opencode/big-pickle`
  routing identities. These confer no programmatic HTTP endpoint and no API key.
- Local model servers: none. `http://localhost:11434/api/tags` and
  `http://localhost:8000/v1/models` both unreachable.
- Python modules: `playwright`, `httpx`, `requests`, `openai`, `anthropic`, `litellm`,
  `numpy`, `sklearn`, `scipy` all raise `ModuleNotFoundError`.

Kernel-path probes at HEAD:

- `src/spider/kernel.py` is 132 lines and defines only `_matches`, `_template_slots`,
  `_bind`, `SpiderKernel.observe`, `.distill`, `.resolve`, `.verify`, `.invalidate`.
  There is **no** `distill_parameterized`.
- `distill()` returns `confidence=0.5` (line 90); `resolve()` defaults
  `min_confidence=0.8` (line 59) and returns `Resolution(EXPLORE, ..., bound_action=None)`
  whenever `best.confidence < min_confidence` (lines 114-115). Therefore no mechanism the
  shipped literal path produces can ever reach `EXECUTABLE`. `src/spider/models.py` already
  carries `Mechanism.parameter_slots`, `applicability_guards`, `verification_rule`,
  `failure_boundary` and `repair_scope` (currently unused by the engine).

Disposition: the model credential is a **downstream dependency**, recorded, not a gate
here. The kernel path is **provisionable in scope** and is this experiment's treatment.

---

## 2. Inherited state (four-way distinction preserved)

Inherited from `research/experiments/EXP-PRODUCT-37385633334/handoff.json`
(sha256 `91f7e00fa032ac22a1a7f9b4ee9fb3117a314ce6d3bd101687c3091cf98355fa`, pinned by
`request.json`). These categories are carried forward as inherited scientific state, not
as an automatic agenda, and none is silently upgraded or downgraded.

**Established (inherited, not re-tested here):** the readiness certificate is a working
reusable substrate artifact; all three old readiness failures are independently confirmed
environment facts; the hygiene revert at commit `39fcfd96` is discharged; zero arms ran so
every scientific metric is an explicit unknown; the transaction was neither an
infrastructure failure nor a scientific negative; freeze can bind only request/spec/prereg
and not code; and the bounded finding that the old gate can certify substrate PRESENCE but
can never certify that a treatment arm differs from its comparator.

**Rejected (inherited, still rejected):** reading `MEASUREMENT_INVALID` as a statement
about the product thesis; reading the gate failure as evidence about agent benefit; reading
the gate's internal pass as instrument validation; treating
`research/experiments/EXP-PRODUCT-35777355953/tasks.json` as a valid task bank; citing
`1.045`/`0.472` (they belong to `EXP-PRODUCT-35949571341`, not `EXP-PRODUCT-35797365772`);
and treating producer verification of the revert as sufficient.

**Unknown (inherited, still open):** whether any real external LLM agent benefits from
inherited mechanisms beyond a strong retrieval baseline; whether the kernel can execute an
inherited mechanism at all (this experiment attacks exactly this); whether the credential
is provisionable; whether playwright/httpx are provisionable; whether a >=30-task
credential-free real-Web mechanical-verifier bank can be built; honest cost per success;
retrieval comparator strength; and whether counter instrumentation passes once written.

**Do not assume (inherited, still binding):** C-LLM-INHERIT has not advanced, weakened or
been refuted by the parent; null metrics are explicit unknowns, never zero; the old
certificate did not validate the instrument; the SPIDER arm cannot execute on the current
product code *as shipped* (this experiment tests whether a bounded in-scope repair changes
that); the parent design must not be re-run as frozen; this handoff does not self-authorize
a child experiment; and repository/environment probes are artifact identity, not
measurements.

---

## 3. Scope and non-goals

In scope: a bounded code change in `src/spider/` (plus `tests/` and a deterministic harness
inside this experiment directory) that adds a parameterized induction/execution path and a
per-trajectory counter surface, and a synthetic credential-free certificate that is shown
to fire.

Explicit non-goals: no LLM arm runs, no browser, no network, no real-Web tasks, no
economics benchmark, no cross-site, no freshness/delta-repair, no promotion, and no claim
update to `C-LLM-INHERIT` beyond "the arm-differentiation prerequisite is or is not
established". The old three-check readiness gate is NOT re-run.

---

## 4. Required in-scope kernel contract (treatment to be implemented in EXECUTE)

EXECUTE implements exactly this contract. If the contract cannot be implemented, EXECUTE
emits BLOCKED with the diagnostic; it does not weaken the certificate.

1. `distill_parameterized(observations) -> Mechanism | None`. From at least two successful
   observations with the same intent, induce one mechanism. A field of the action template
   (or a postcondition field that co-varies with it) becomes a parameter slot only if it
   varies across the observations and is structurally aligned with the action; fields that
   merely vary in the surrounding observation (trace/sequence/timestamp noise) MUST NOT
   become slots. The mechanism records `parameter_slots` and per-slot support descriptors
   inferred from the induction values (the descriptor is EXECUTE's choice, e.g. a regex or
   a value-grammar predicate, but it must reject the declared out-of-support values in
   Section 5). Returns `None` if there are fewer than two observations or the structure is
   not stable.
2. Confidence policy. After induction, a mechanism whose applicability is demonstrated by
   successful re-verification on its own induction observations must reach the execution
   threshold, so `resolve` can return `EXECUTABLE`. The pre-repair asymmetry
   (`distill` 0.5 vs `resolve` 0.8) must be closed, the default reconciled, or the policy
   documented and reported. The policy may not make every mechanism EXECUTABLE; Section 5
   negatives enforce selectivity.
3. `resolve(intent, context, params)`. As today, plus: refuse a provided parameter whose
   value violates the inferred support, returning a non-executable status with a non-empty
   reason naming the offending slot; return `EXECUTABLE` only when all required slots are
   present and in support; keep `bound_action` null on every non-executable resolution.
4. `verify(mechanism_id, observed_state, params=None)`. When `params` is supplied, bind the
   postconditions and verification rule before matching, so a parameterized postcondition
   can be verified against a held-out identifier. Keep the literal signature working.
5. Counter surface. A per-trajectory counter object with the fixed field identities
   `model_calls`, `model_tokens`, `browser_actions`, `http_requests`, `retrieval_calls`,
   `verification_calls`, `repair_attempts`, `latency_ms`. `resolve` must count at least one
   `retrieval_calls` event for the inherited path; `verify` counts `verification_calls`;
   one re-bind after a support/verify rejection counts `repair_attempts`. The literal
   `distill()` path may remain but must not be the default for the parameterized certificate.
6. `B-LITERAL-KERNEL` mode. EXECUTE provides a documented mode reproducing pre-repair
   literal semantics (integer confidence 0.5, min_confidence 0.8) so the causal-attribution
   control in Section 6 can run. This is a control, not a shipping default.
7. Any code written for this experiment that is not accepted must be revertible; the tree
   must not retain experiment residue on a negative outcome.

---

## 5. Frozen synthetic fixture bank `SYNTH-INDUCTION-BANK-v1`

Credential-free, deterministic, Python standard library only. Seed constant
`SEED = 37950607128`. The bank is defined *in this frozen text*; EXECUTE reconstructs it
and records its sha256; AUDIT rebuilds it independently. This is the documented
preregistered substitute for a committed real task-bank hash.

Common shape. An induction observation is
`Observation(intent, state, action, next_state, success=True)`.
Each family declares: the action-template field that varies, the value grammar, the
induction values, one held-out unseen value, and the declared out-of-support values.

| Family | Intent | Action template (varying field in `**`) | Slot grammar | Induction values | Held-out |
|---|---|---|---|---|---|
| `F1-PATH-ID` | `fetch_item` | `{"method":"GET","url":"https://fixture.invalid/v1/items/**item_id**"}` | `^[a-z]+-[0-9]{4}$` | `itm-0001..itm-0004` | `itm-0009` |
| `F2-QUERY-ID` | `search` | `{"method":"GET","url":"https://fixture.invalid/v1/search","params":{"q":"**query**"}}` | `^[a-z]{4,8}$` | `alpha,beta,gamma,delta` | `epsilon` |
| `F3-BODY-FIELD` | `echo` | `{"method":"POST","url":"https://fixture.invalid/v1/echo","json":{"token":"**token**"}}` | `^tok-[0-9]{2}$` | `tok-11..tok-44` | `tok-99` |
| `F4-HEADER-FIELD` | `verify` | `{"method":"POST","url":"https://fixture.invalid/v1/verify","headers":{"X-Resource":"**resource**"}}` | `^res-[a-z]$` | `res-a..res-d` | `res-z` |
| `F5-TWO-SLOT` | `write` | `{"method":"POST","url":"https://fixture.invalid/v1/tenants/**tenant**/items","json":{"item_id":"**item_id**"}}` | tenant `^t[0-9]$`, item `^i[0-9]$` | `(t1,i1)..(t4,i3)` | `(t9,i9)` |
| `F6-NOISE-STRESS` | `ping` | `{"method":"GET","url":"https://fixture.invalid/v1/nodes/**node**"}` | `^n-[0-9]{2}$` | `n-01..n-04` | `n-09` |

Declared per-family expected action-template slot count: F1=1, F2=1, F3=1, F4=1, F5=2,
F6=1. Noise stress: every family's `state`/`next_state` carries additional fields that vary
across observations but are absent from the action template (`trace_id`, `seq`, `ts`).
These MUST NOT become slots. In `F6-NOISE-STRESS` all four noise fields vary and the
expected slot count stays 1; any inferred slot count greater than the declared value is a
certificate failure (over-parameterization).

Declared out-of-support and negative cases (must be refused): for F1-F4 and F6 the empty
string, a value containing a space, and a value containing `/`; for F5 a missing `tenant`,
a missing `item_id`, and an out-of-support pair; plus one wrong-intent resolution per
family (same context and params, different intent).

Deterministic fixture executor `fixture_execute(bound_action) -> observed_state`:
- If host is not `fixture.invalid`, or the method and path structure do not match the
  family schema, return `{"status":412,"error":"bad_request"}`.
- If the bound identifier fails the family grammar or is empty/contains whitespace or `/`,
  return `{"status":422,"error":"unsupported_identifier"}`.
- Otherwise return `{"status":200,"resource_echo": <bound identifier>}` (for F5 both
  `resource_echo` values). The mechanism's `postconditions` contain the same slot
  placeholders, e.g. `{"status":200,"resource_echo":"${item_id}"}`, so `verify` with the
  held-out params is a genuine, non-tautological check that the bound action addressed the
  requested held-out resource.

Case count: 6 families x (4 induction + 1 held-out) = 30 positive cases plus
>= 6 x 4 = 24 declared negative cases. The certificate reports per-case expected vs
observed.

---

## 6. Certificate checks, controls and stable metric identities

Stable control/baseline identities (EXECUTE and AUDIT must reuse these exact strings):
`AD-POSITIVE-ROUNDTRIP`, `AD-NEGATIVE-ROUNDTRIP`, `AD-TREATMENT-CONTRAST`,
`NC-ZERO-CONTRAST-TREATMENT`, `PC-ACCOUNTING-FIDELITY`, `AD-IDENTITY-BINDING`,
`B-LITERAL-KERNEL`, `B-RETRIEVAL-SHAPED`.

- `AD-POSITIVE-ROUNDTRIP` (positive control). For each held-out in-support case:
  `distill_parameterized(induction) -> M`; declared slot count matches; `resolve(intent,
  context, {slot: held_out})` returns `EXECUTABLE` with non-null `bound_action` containing
  the held-out value at the expected field; `fixture_execute(bound_action)` returns the
  expected 200 state; `verify(M.mechanism_id, state, {slot: held_out})` is `True`. PASS iff
  all cases succeed.
- `AD-NEGATIVE-ROUNDTRIP` (null control). For every declared negative case, `resolve`
  returns a non-executable status with `bound_action` null and a non-empty reason. PASS iff
  refusal rate is exactly 1.0.
- `AD-TREATMENT-CONTRAST` (discriminating control). treatment action = the bound action;
  comparator action = `B-RETRIEVAL-SHAPED` nearest-observation literal action (structural
  field-overlap K=5, no model, no network). Require at least one case with
  treatment != comparator. Then run the forced `NC-ZERO-CONTRAST-TREATMENT` variant in
  which treatment action := comparator action; the check must report contrast 0 and FAIL.
  PASS iff contrast fires on the real cases AND the degenerate variant is detected.
- `PC-ACCOUNTING-FIDELITY` (positive accounting control). On the seeded deterministic
  5-step scripted trajectory, all eight counter fields match ground truth within
  `max_relative_error <= 0.01`. On a mechanism execution, `retrieval_calls`,
  `verification_calls` and `repair_attempts` each increment by their declared non-zero
  expected amount. Model counters are shown to fire only on an injected synthetic event and
  are labelled injected. PASS iff all hold.
- `AD-IDENTITY-BINDING`. The reconstructed fixture sha256, the pre-repair kernel blob hash
  and the post-repair kernel blob hash (`git rev-parse HEAD:src/spider/kernel.py`) are
  recorded and internally consistent. PASS iff recorded and consistent.
- `B-LITERAL-KERNEL` (causal-attribution control). The pre-repair literal mode produces
  zero `EXECUTABLE` resolutions on the held-out in-support set. PASS iff zero. If it
  produces any `EXECUTABLE`, liveness attribution fails and the certificate FAILS.
- `B-RETRIEVAL-SHAPED` (comparator). Records the comparator action per case and the contrast.
  Non-gating.

Stable metric names (result.json): `certificate_overall` (PASS/FAIL),
`ad_positive_roundtrip_pass`, `ad_negative_roundtrip_pass`, `ad_treatment_contrast_pass`,
`pc_accounting_fidelity_pass`, `ad_identity_binding_pass`, `b_literal_kernel_pass`,
`in_support_executable_rate`, `held_out_binding_correct_rate`,
`out_of_support_refusal_rate`, `missing_param_refusal_rate`, `wrong_intent_refusal_rate`,
`treatment_contrast_rate`, `degenerate_variant_detected`,
`declared_vs_inferred_slot_count` (per family), `counter_max_relative_error`,
`inherited_path_counter_increments` (retrieval_calls, verification_calls, repair_attempts).

---

## 7. Decision rule

Outcome mapping (spec.json `decision_rule` is canonical):

- ALL checks PASS -> `SUPPORTS` / CERTIFICATE_ESTABLISHED.
- `AD-POSITIVE-ROUNDTRIP` FAIL with a conforming implementation -> `FALSIFIES` (kernel
  liveness not achievable on this architecture).
- Any of `AD-NEGATIVE-ROUNDTRIP`, `AD-TREATMENT-CONTRAST`, `PC-ACCOUNTING-FIDELITY`,
  `AD-IDENTITY-BINDING`, `B-LITERAL-KERNEL` FAIL -> `MEASUREMENT_INVALID`.
- Kernel path not implementable in scope, or genuine infrastructure error -> `BLOCKED` with
  the exact receipt.
- Otherwise -> `INCONCLUSIVE`.

`status` describes measurement validity and completion; a valid negative is `COMPLETE`.
An absent model credential is never encoded as a scientific negative of C-LLM-INHERIT.

---

## 8. Validity threats and mitigations

1. **Self-fulfilling certificate** (EXECUTE writes both kernel and test). Mitigated by the
   negative round trip, held-out identifiers, the degenerate-treatment detection, the
   pre-repair `B-LITERAL-KERNEL` control, declared slot counts, and an independent AUDIT
   rebuild. An always-EXECUTABLE kernel fails `AD-NEGATIVE-ROUNDTRIP`; a kernel that passes
   only because treatment == retrieval fails `AD-TREATMENT-CONTRAST`.
2. **Over-parameterization / noise slottage.** Declared per-family slot counts plus the
   `F6-NOISE-STRESS` family bound it.
3. **Synthetic-to-real gap.** The fixture is not the Web; the comparator is not a real LLM
   retrieval arm. Claim ceiling is instrument establishment only.
4. **Freeze cannot bind code.** Documented substitute in Section 4 / spec
   `measurement_validity`; the behavioural checks are behaviour-bound and AUDIT re-runs
   against the recorded kernel commit.
5. **Counter fiction.** Model counters cannot be exercised by a real model and are labelled
   injected; only inherited-path counters are required to fire on a real mechanism
   execution; unexercised counters are `null`/not-exercised, not measured zeros.
6. **Representation loss.** The parameterization contract is deliberately minimal
   (single-field and two-field templates); results do not generalize to arbitrary DOM/
   browser mechanisms. This loss is disclosed, not hidden.

---

## 9. Reproducibility, artifacts and compute

Expected EXECUTE artifacts (paths relative to
`research/experiments/EXP-PRODUCT-37950607128/`): `raw_fixture/synth_induction_bank.json`
(reconstructed bank, with sha256), `raw_certificate/arm_differentiation_certificate.json`
(per-case expected/observed, per-check PASS/FAIL), and
`raw_certificate/accounting_fidelity_trace.json`. Plus `result.json`, `report.md`,
`provenance.json`, and the in-scope code changes under `src/spider/` and `tests/`.
`provenance.json` must record: pre-execute commit/blob hash of `src/spider/kernel.py`,
post-repair blob hash, fixture sha256, Python version, and the exact certificate command.

Compute: stdlib only, deterministic, single process, sub-minute. No model, browser or
network calls. Estimated wall clock <= 1 hour including code authoring. `model_calls` and
`model_tokens` estimate 0.

---

## 10. Consequences

Positive (`SUPPORTS`): the arm-differentiation prerequisite is established; the first
admissible four-arm C-LLM-INHERIT benchmark becomes executable and non-degenerate. No
promotion; `C-LLM-INHERIT` stays `HYPOTHESIS`. Product action: queue the four-arm benchmark
as a NEW mandated experiment once a model credential is provisioned.

Negative (`FALSIFIES`): the current kernel architecture cannot execute an inherited
parameterized mechanism without admitting wrong bindings; further gate reruns stop and the
kernel-liveness thread is PARKed or the execution architecture is changed.

Invalid (`MEASUREMENT_INVALID`): the certificate cannot discriminate a live treatment from
a degenerate retrieval-shaped one and must be redesigned before any benchmark is frozen.

Blocked (`BLOCKED`): the in-scope kernel path cannot be installed; the exact receipt is
recorded and the arm-differentiation prerequisite remains open.

---

## 11. Explicitly not tested

No claim about real external LLM agents (C-LLM-INHERIT), parameterized inheritance to
unseen identifiers on real sites (C-PARAM-INHERIT), cross-site transfer (C-CROSSSITE),
freshness (C-FRESHNESS), delta repair (C-DELTA-REPAIR), residual novelty or economics
(C-RESIDUAL-NOVELTY, C-PRODUCT-ECON), semantic resolution (C-SEMANTIC-RESOLVE), or Web
dynamics (C-WEB-DYNAMICS). None of these claims is advanced, weakened or refuted by this
packet.
