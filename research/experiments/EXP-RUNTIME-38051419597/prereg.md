# EXP-RUNTIME-38051419597 preregistration

Lane: `runtime`. Claim: `C-MEAS-VALID` (owner_lanes runtime+physics). Design contract v2.
Director mandate: CONTINUE on `C-MEAS-VALID`, `parent_handoff_disposition=SUPERSEDE`.
This document is frozen by `freeze.json`. It is the complete scientific input for EXECUTE; no
interpretation-critical quantity is left to EXECUTE discretion.

## 1. Mandate and scope

The Global Research Director's binding question is: *can a non-degenerate asymmetric-discovery
task bank be certified arithmetically before freeze - cold/retrieval comparators demonstrably below
ceiling at high novelty, a real treatment/comparator distinction, and honest per-condition
counters - and be delivered as a reusable substrate that unblocks the flagship inheritance tests,
rather than another mandatory-discovery REST certificate that only re-validates the existing
measurement harness?* (request.json `director_mandate.allocation.question`).

This experiment answers exactly that question with the smallest instrument that can change the
decision:

- It builds and certifies the **instrument** (a task bank with certified dynamic range), not a
  transfer or product-economics result.
- It is **not** another run of the existing C-MEAS-VALID WAL / out-of-surface oracle harness
  (`EXP-RUNTIME-37973247935`) and **not** a re-run of the mandatory-discovery deterministic REST
  certificate (`EXP-PRODUCT-37989728440`). Those established the defect this experiment removes.
- It does **not** require the Product parameterized carrier (readiness condition 1) or a proven
  model driver (readiness condition 3); both are explicitly soft dependencies and are not invoked.

## 2. Inherited state this design must respect (parent_handoff EXP-RUNTIME-37973247935)

Per `request.json.parent_handoff_disposition = SUPERSEDE`, the parent's `next_question` (out-of-
surface oracle response-fingerprint repair) is **not** the objective of this experiment. Its
four-way distinction is preserved as inherited continuity state and is not re-litigated here:

- **established (inherited, do not re-derive):** the parent oracle packet is MEASUREMENT_INVALID;
  C-MEAS-VALID's effective epistemic status is the parent bounded VALIDATED ceiling of
  `EXP-RUNTIME-36293257855` (authorship-separated real-Chromium fixture). Frozen-input integrity,
  capability-ledger/readiness mechanics and the WAL byte vector stability held.
- **rejected (inherited, do not reintroduce):** reading the parent packet's per-arm rates as
  support/falsification; treating the detector compromise or the gate mis-specification as a
  scientific negative; treating instability as a WAL-substrate problem.
- **unknown (inherited):** whether the oracle detects committed out-of-surface transitions; whether
  a repaired re-run would separate arms. None is measured here.
- **do_not_assume (inherited):** do not cite the parent's rates; do not downgrade or advance
  C-MEAS-VALID on them; do not let a downstream lane preregister the parent substrate as
  measurement-valid for real drift.

Additional relevant accepted evidence driving this design:
- `EXP-PRODUCT-37973256064` (audit PASS, outcome FALSIFIES): the parameterized `distill ->
  resolve -> execute` path is live and causally attributable on a real credential-free localhost
  HTTP substrate, but cold (1.0) and retrieval (1.0) were at the success ceiling, so the frozen
  margin was arithmetically unreachable.
- `EXP-PRODUCT-37989728440` (audit REVISE, outcome FALSIFIES): on the mandatory-discovery
  deterministic credential-free REST class, cold and retrieval were both at 1.0 at novelty 0.5/0.75
  because discovery was mandatory and *symmetric for every arm*; the audit's required fix is "a
  substrate that allows asymmetric discovery (e.g., multi-task sessions where discovery can be
  amortized)". The `cost_per_success` metric was also contaminated by `latency_ms/1000` noise.

This experiment implements that audit fix directly: discovery is **asymmetric** (route discovery
cost exceeds the per-task budget for high-novelty tasks, and collapses to ~0 once a compiled route
schema is inherited), and the primary signal is **deterministic counters only** (latency is
prohibited as a decision input).

## 3. What this experiment deliberately is NOT

- Not a real-LLM-agent measurement (readiness condition 3 is unmet; this is a deterministic
  instrument certificate).
- Not a transfer/generalization claim (the bank is synthetic by construction; see section 11).
- Not a Product promotion and not a change to C-MEAS-VALID beyond a bounded instrument-readiness
  widening if SUPPORTS.

## 4. Substrate declaration: ADB-v1 (Asymmetric-Discovery Bank, v1)

ADB-v1 is a credential-free, locally served, deterministic multi-page link-and-value substrate.
Implementation is **Python 3.12 standard library only**: `http.server.ThreadingHTTPServer` (site),
`urllib.request` (arm transport), `html.parser` + `json` (parsing), `hashlib` (digests),
`random.Random(MASTER_SEED)` (seeded order). No third-party package, no browser, no external
network egress, no cookies, no credentials, no API keys.

Topology (fully declared, deterministic from a fixed seed):

- `/` : entry page linking to `F=3` family listing pages `/list/<family>/page-1.html`.
- `/list/<family>/page-{p}.html` : paginated listing pages (each links to item pages and to the
  next page). Listing order is frozen.
- `/item/<id>` : item page carrying the target value.
- **Hidden resolution layer:** each family has a frozen schema variant token and route template
  that lets an arm jump directly to the target item page (`/resolve/<family>/<token>/<id>`). The
  token is discoverable **only** by traversing the listing pages; it is never present in a task
  spec.

Route tokens are opaque fixed-length strings. The **route-leak rule** is: for every task, the token
set of its task spec intersected with the declared route-token set must be empty. The task spec
contains only `{task_id, family, target_label, required_value_kind}`.

Frozen per-task request budget: `B = 10` substrate requests; `max_repair_attempts = 3`.

Serving digest: EXECUTE records a `sha256` of the canonical serialization of the served topology
(entry + listing + item + resolve routes) in `provenance.json`; the digest is a raw artifact, not a
decision input.

### 4.1 Satisfiability probe performed in DESIGN (allowed, non-outcome-bearing)

A stdlib import probe (`importlib.import_module` for `http.server`, `urllib.request`, `html.parser`,
`json`, `hashlib`, `random`) confirmed every dependency is present in the environment. No
outcome-bearing measurement was run.

## 5. Task bank declaration and arithmetic certificate (computed in DESIGN)

18 frozen task instances across F1/F2/F3: **12 high-novelty (novelty_fraction >= 0.5)** and **6
low-novelty (novelty_fraction < 0.2)**. The interval `[0.2, 0.5)` is frozen empty.

`novelty_fraction(t) = 1 - (reused_edges / shortest_path_edges)`, where `reused_edges` are edges of
the declared shortest resolution path that also occur in at least one **other-family** training
trajectory (leave-one-family-out).

Declared shortest discovery path lengths `d(t)` (requests to resolve the route) and the resulting
budgeted cost `cost = d + 2` (one resolve, one extract):

| family | high-novelty `d(t)` | low-novelty `d(t)` |
|---|---|---|
| F1 | 7, 9, 12, 14 | 3, 5 |
| F2 | 8, 11, 13, 16 | 3, 4 |
| F3 | 9, 12, 15, 18 | 4, 5 |

The novelty stratum is **fully enumerated** so membership is arithmetic, not EXECUTE discretion.
`shortest_path_edges = d(t)`; `reused_edges` are path edges occurring in at least one other-family
training trajectory (leave-one-family-out); `novelty_fraction = 1 - reused/path` is computed:

| task | path_edges | reused_edges | novelty_fraction | stratum |
|---|---|---|---|---|
| F1-T1 | 7 | 3 | 0.571 | high |
| F1-T2 | 9 | 4 | 0.556 | high |
| F1-T3 | 12 | 5 | 0.583 | high |
| F1-T4 | 14 | 6 | 0.571 | high |
| F2-T1 | 8 | 4 | 0.500 | high |
| F2-T2 | 11 | 5 | 0.545 | high |
| F2-T3 | 13 | 6 | 0.538 | high |
| F2-T4 | 16 | 7 | 0.562 | high |
| F3-T1 | 9 | 4 | 0.556 | high |
| F3-T2 | 12 | 5 | 0.583 | high |
| F3-T3 | 15 | 7 | 0.533 | high |
| F3-T4 | 18 | 8 | 0.556 | high |
| F1-L1 | 3 | 3 | 0.000 | low |
| F1-L2 | 5 | 5 | 0.000 | low |
| F2-L1 | 3 | 3 | 0.000 | low |
| F2-L2 | 4 | 4 | 0.000 | low |
| F3-L1 | 4 | 4 | 0.000 | low |
| F3-L2 | 5 | 5 | 0.000 | low |

Declared per-arm budgeted success on the high-novelty stratum (`success iff cost <= B = 10`):

- `A-COLD-RE-DERIVE`: cost `d+2`; succeeds iff `d <= 8` -> F1-T1 (d=7), F2-T1 (d=8) -> **k=2/12**.
- `A-RETRIEVAL-SHAPED`: succeeds on the `d <= 8` tasks plus two tasks with an admissible
  leave-one-family-out fragment `{F1-T2 (d=9), F3-T1 (d=9)}` -> **k=4/12**.
- `A-TREAT-PARAM-MECH` (in-support): cost `3` (bind + resolve + extract) -> **k=12/12**.
- `PC-ORACLE-SCHEMA-COLD` (schema given): cost `2` -> **k=12/12**.
- Low-novelty (liveness): all three arms succeed within budget -> treatment liveness **6/6**.

### 5.1 Wilson reachability certificate (two-sided 95%, z = 1.959963984540054)

Accept region for a comparator at high novelty: `point < 0.95 AND Wilson_lo < 0.90`, at `n = 12`:

| k | point | Wilson_lo | accept |
|---|---|---|---|
| 0 | 0.0000 | 0.0000 | yes |
| 1 | 0.0833 | 0.0149 | yes |
| 2 | 0.1667 | 0.0470 | yes |
| 4 | 0.3333 | 0.1381 | yes |
| 8 | 0.6667 | 0.3906 | yes |
| 11 | 0.9167 | 0.6461 | yes |
| 12 | 1.0000 | 0.7575 | **no** |

The accept region `{0..11}` is non-empty and the declared predictions (cold k=2: point 0.1667,
Wilson_lo 0.0470; retrieval k=4: point 0.3333, Wilson_lo 0.1381) lie strictly inside it. The rule is
therefore reachable by a genuinely imperfect instrument and is not forced.

### 5.2 Constructibility falsifier (pre-freeze)

If the declared topology cannot place >= 12 tasks in the high-novelty stratum, or the accept region
is empty, or no arm distinction is arithmetically reachable, the experiment is a DESIGN failure and
must not freeze. It is not bootstrapped at EXECUTE.

## 6. Arms and identifiability

Frozen arm identifiers and procedures (identical per-task budget `B = 10` for all arms):

- **`A-COLD-RE-DERIVE`** - stateless per task; no index, no mechanism store, no oracle schema.
  `reset_state -> bfs_from_entry(seed=MASTER_SEED) -> resolve_route -> extract_value -> verify`.
  Counters: `retrieval_calls = 0`, `mechanism_lookup_calls = 0`, `route_discovery_requests > 0`.
- **`A-RETRIEVAL-SHAPED`** - `embed_task -> retrieve_top_k(leave_one_family_out) ->
  bind_parameters -> execute | fallback_bfs -> verify`. Counters: `retrieval_calls >= 1`,
  `mechanism_lookup_calls = 0`, `route_discovery_requests >= 0`.
- **`A-TREAT-PARAM-MECH`** - compiled route schema + parameter bind learned from same-family
  training tasks; refuses (UNKNOWN) when the target is out of support. Counters:
  `mechanism_lookup_calls >= 1` (in support), `retrieval_calls = 0`, `route_discovery_requests = 0`.

Identifiability: the three signatures are disjoint; the retrieval index is built **leave-one-
family-out** so no evaluated family is memorized; the treatment's route-discovery counter is 0 on
in-support tasks by construction, which is the asymmetric-discovery distinction itself.

## 7. Controls

- **`PC-ORACLE-SCHEMA-COLD`** (primary positive control): cold policy given the schema out of band on
  the same 12 high-novelty tasks; must reach point >= 0.95. Purpose: distinguish "bank solvable but
  discovery is the cost" from "bank unsolvable / budget too small". Failure maps to
  MEASUREMENT_INVALID (instrument), never to FALSIFIES. This is a **solvability ceiling**, **not a
  headroom comparator**: it is excluded from the treatment-minus-comparator margin, so both it and
  the treatment reaching 12/12 is expected and contributes no independent comparison.
- **`PC-EXACT-REPLAY`** (positive liveness control): replay a stored training trajectory on one
  training task per family (3 episodes); must be 1.0. Verifies the site subtopology, transport and
  counter instrumentation.
- **`NC-OOS-TYPE`** (null control): 5 out-of-support instances; treatment must refuse with reason
  `OUT_OF_SUPPORT`, `bound_value = null`; refusal rate must be 1.0 with zero false accepts.
- **`NC-BUDGET-HONESTY`** / `M-COUNTER-RECONCILE` (integrity control): every arm-reported counter
  reconciles exactly to the server request log; mismatch count must be 0.
- **`NC-ROUTE-LEAK`** (integrity control): task-spec token set intersected with route-token set must
  be empty for all 18 tasks.
- **`NC-STRATUM-NONDEGENERACY`** (arithmetic control): high stratum size 12 and accept region
  non-empty (section 5). A failure here is a DESIGN defect caught before freeze.

## 8. Treatment liveness and abort

Treatment liveness is structural (section 6): the compiled schema is built from same-family training
tasks and applies to the held-out in-support instances by construction. Because this is a Runtime
instrument certificate with a declared deterministic mechanism rather than a Product carrier, the
packet's pre-freeze Product-carrier liveness run does not apply; liveness is instead a
**post-freeze abort gate** exercised at the START of EXECUTE by the low-novelty liveness block
(expected 6/6). If it fails, EXECUTE aborts the primary decision and reports MEASUREMENT_INVALID with
the failing phase and the smallest unblocking action. `PC-EXACT-REPLAY` (expected 1.0) is a separate
substrate/transport control and is **not** cited as evidence of treatment liveness. A structurally
live treatment is a precondition, so a liveness failure is an instrument abort, not a scientific
negative.

## 9. Freeze artifacts

Bound by sha256 in `freeze.json.artifact_hashes`:

- `research/runtime/shared_config.py` - supplies `WILSON_Z` (governs every interval) and
  `MASTER_SEED` (governs the seeded arm/episode order). EXECUTE must import these and assert they
  equal the frozen values `1.959963984540054` and `36293257855`; a mismatch is MEASUREMENT_INVALID.

All other interpretation-critical input (topology, bank, strata, `novelty_fraction`, arm procedures,
counter definitions, thresholds, accept regions, decision rule) is declared inside the frozen
`spec.json`/`prereg.md` and is therefore bound by `freeze.json.hashes`. The EXECUTE implementation is
materialized once inside the frozen experiment directory; every implementation/raw artifact is
hashed in `result.json.artifacts` and independently recomputed by AUDIT. No external site, dataset
or fixture is read.

## 10. Measurement validity

- **Counters are deterministic and server-reconciled.** `latency_ms`, model calls and token counts
  are prohibited as decision inputs (a prior audit found `latency_ms/1000` is instrument noise).
  The frozen reconciliation predicate is: `arm_reported_http_requests == server_logged_requests`
  **and** `route_discovery_requests <= http_requests` (`route_discovery_requests` is a *subset* of
  `http_requests`, never summed with it); `retrieval_calls` and `mechanism_lookup_calls` are recorded
  independently. This avoids a double-count that would otherwise make reconciliation unsatisfiable
  once the cold arm mandates `route_discovery_requests > 0`.
- **No synthetic fallback.** Site bind, transport or digest failure is recorded with the exact error
  and mapped to MEASUREMENT_INVALID/BLOCKED.
- **Authorship separation.** The site (ground-truth provider) never imports an arm module; the
  retrieval-index builder cannot read the site source; the server request log is ground truth.
- **Seeded order.** Episode order is `random.Random(MASTER_SEED).shuffle` over the frozen episode
  list; the scoring is arm-blind (the scorer reads only counter records and success flags).

## 11. Statistics and decision rule

Frozen thresholds: `success_ceiling_point = 0.95`; `success_ceiling_wilson_lo = 0.90`;
`high_novelty_threshold = 0.5`; `n_high = 12`; `n_low = 6`; `treatment_margin_min = 0.25`;
`oracle_schema_control_min_point = 0.95`; `counter_mismatch_max = 0`; `refusal_rate_min = 1.0`.

Primary predicates (per-task `M-SUCCESS-IN-BUDGET` is binary):

- **P1** cold high-novelty `point < 0.95 AND Wilson_lo < 0.90`.
- **P2** retrieval high-novelty `point < 0.95 AND Wilson_lo < 0.90`.
- **P3** `PC-ORACLE-SCHEMA-COLD` high-novelty `point >= 0.95`.
- **P4** treatment low-novelty liveness `point = 1.0`.
- **P5** treatment-minus-`max(cold,retrieval)` high-novelty success margin `>= 0.25`.
- **P6** `M-COUNTER-RECONCILE` mismatch count `= 0`.
- **P7** route-leak check passed for all 18 tasks.
- **P8** `NC-OOS-TYPE` refusal rate `= 1.0`.

Decision mapping (total partition; **integrity set** = `{P3, P4, P6, P7, P8}`):

- If **any** integrity-set predicate fails -> **MEASUREMENT_INVALID** (instrument abort), never a
  scientific negative.
- Given the integrity set holds:
  - **SUPPORTS** iff `P1 AND P2 AND P5`.
  - **MIXED** iff exactly one of `{P1, P2}` fails, **or** (`P1 AND P2 AND NOT P5`) - headroom exists
    but the treatment-minus-comparator margin is `< 0.25`.
  - **FALSIFIES** iff `NOT P1 AND NOT P2` (both comparators at ceiling while the bank is solvable
    when the schema is known). Bounded negative about this declared bank class; `status=COMPLETE`.
- **INCONCLUSIVE** iff substrate bring-up/transport prevents completion; recorded per component.

These three cases exhaust the `P1/P2/P5` boolean space, so no outcome is unmapped. Note `P3`
requires `k = 12/12` at `n = 12` (`11/12 = 0.9167 < 0.95`), so the positive control must be clean
for the primary decision to run at all.

Secondary continuous metric: `M-REQUESTS-UNBUDGETED` (median requests-to-success with the budget
removed) must show cold > retrieval > treatment; it is reported but is not a primary predicate.

## 12. Validity threats and do-not-assume

- **Synthetic bank.** ADB-v1 is authored by the same lane that measures it, so it certifies the
  *instrument's* dynamic range under declared non-omniscient policies, **not** transfer to the open
  Web or to a real agent. Any downstream inheritance result must add a third-party / adversarial /
  holdout task population and a real-agent arm.
- **Policy-shaped comparators.** Cold and retrieval are deterministic policies. The
  `PC-ORACLE-SCHEMA-COLD` control and the counter-reconciled, route-leak-free design are the
  mitigations that prevent the below-ceiling result from being a pure budget artifact, but they do
  not prove that an unbounded agent could not solve the high-novelty tasks.
- **Budget sensitivity.** Dynamic range depends on `B = 10` and the declared `d(t)`. If `B` is
  varied the headroom changes; `B` is frozen and the unbudgeted counterfactual is reported so the
  dependence is visible.
- **Certificate is conditional on the declaration.** The arithmetic certificate guarantees dynamic
  range only if EXECUTE implements the declared topology exactly; once implemented, SUPPORTS is
  largely the declaration taking effect. The genuinely falsifiable pathways are implementation
  divergence, route/index leakage, counter dishonesty, oracle-control failure, and a cross-family
  retrieval fragment generalizing further than declared (which would push retrieval to ceiling and
  fire MIXED/FALSIFIES). This is disclosed rather than hidden.
- **Do not** read a SUPPORTS result as a transfer, generalization, or product-economics result.
- **Do not** re-run, repair or re-score the parent `EXP-RUNTIME-37973247935` packet.
- **Do not** treat the declared prediction as a measurement; only the EXECUTE matrix is measured.
- **Do not** use the parent's `THRESH_WILSON_LO = 0.80`; this experiment's binding thresholds are
  `0.90` (Wilson ceiling) and `0.95` (point ceiling). Only `WILSON_Z` and `MASTER_SEED` are consumed
  from the frozen `shared_config.py`.

## 13. Estimated cost

74 local stdlib HTTP episodes (36 high-novelty arm episodes, 18 low-novelty, 15 positive-control, 5
null). No network egress, browser, model calls or credentials. Estimated wall clock ~10 minutes;
the arithmetic certificate costs zero runtime.

## 14. Failure mapping

| condition | status | outcome |
|---|---|---|
| integrity set holds; P1,P2,P5 hold | COMPLETE | SUPPORTS |
| integrity set holds; exactly one of P1/P2 fails, or P5 fails | COMPLETE | MIXED |
| integrity set holds; P1 and P2 both fail | COMPLETE | FALSIFIES |
| any integrity-set predicate (P3,P4,P6,P7,P8) fails | MEASUREMENT_INVALID | INCONCLUSIVE |
| substrate bring-up/transport failure | BLOCKED / MEASUREMENT_INVALID | INCONCLUSIVE |
