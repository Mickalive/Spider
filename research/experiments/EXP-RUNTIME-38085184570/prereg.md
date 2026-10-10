# EXP-RUNTIME-38085184570 preregistration

Lane: runtime. Claim ids: `["C-MEAS-VALID"]`. Design contract version: 2.

This file is frozen by `scripts/freeze_experiment.py` before any outcome measurement. After
`freeze.json` exists, no byte of this file or `spec.json` may change. EXECUTE must run exactly
this design; AUDIT must recompute against it.

---

## 0. Status and scope

DESIGN stage, pre-freeze. This is an **instrument/certificate** experiment, not a Web-transfer
or LLM-agent result. It certifies that a declared synthetic Asymmetric-Discovery Bank (ADB-v5)
has a non-degenerate dynamic range for the declared stateless/retrieval/amortizing policies, and
delivers it as a reusable Runtime substrate (blocker B2) or returns a bounded negative about the
construction. No claim status is changed by the arithmetic certificate alone.

## 1. Director mandate and inherited state (parent SUPERSEDED)

`request.json.director_mandate.allocation`: action `CONTINUE`, target claim `C-MEAS-VALID`,
`parent_handoff_disposition` = `SUPERSEDE`, `cognitive_reset` = true, dependencies
`C-PARAM-INHERIT` (Product B1 carrier, unshipped) and `C-LLM-INHERIT` (Intel B3 endpoint) -
referenced as dependencies only, never tested or written in this lane.

The parent handoff (`EXP-RUNTIME-37973247935`, sha256
`984049809ebf393e805f59c9b8d083caf2ebfc387348079b06ccacbe41b8928e`) concerns a composite-oracle
response-fingerprint repair (the hop-by-hop `Connection` header) and a capture-stability gate
mis-specification. The Director **supersedes** that thread: the mandate explicitly declines to
re-promote the composite-oracle repair and points Runtime at the B2 task-bank certification.
Accordingly this experiment does **not** continue the fingerprint-repair agenda and does not
assert any part of the parent's `carry_forward` state as its own. From the parent handoff we
carry only the negative discipline it established: `MEASUREMENT_INVALID` is neither support nor
falsification, and an unaudited re-derivation is not evidence.

## 2. Claim and constructs under test

`C-MEAS-VALID` ("Measurement substrate is intervention-valid"; next gate: "writable/auth/session/
drift controls must produce discriminating positive and null outcomes"). The construct tested
here is the narrow one on the critical path: *a session-scoped asymmetric-discovery instrument
whose cold and retrieval-shaped performance is provably below ceiling on high-novelty tasks while
a session-amortizing mechanism is live.*

## 3. Pre-2.0 screening

Screened against `codex/legacy_brief.json` and `codex/legacy_artifact_index.json`. No pre-2.0
asymmetric-discovery / certified-dynamic-range task-bank precedent exists (`LEGACY: NO_MATCH` for
the bank construction; `LEGACY: DISTINCT_EXTENSION` overall, as recorded in
`spec.json#measurement_validity.pre2_discipline`). The nearest applicable legacy lesson is
`P2-REPLAY-COST` (source sha `9687ff787f2d74460bb7006826008852f5b4416b`): the withdrawn 8.5x
replay claim rested on matched tasks with fully loaded counterfactuals. Guard applied here: all
arms pay fully loaded costs (retrieval pays its 3 local index probes; repairs are charged), tasks
are matched across arms, and no scripted-replay economics is claimed. This experiment does not
repeat the degenerate mandatory-discovery deterministic REST banks already shown at ceiling
(`EXP-PRODUCT-37989728440`, `EXP-PRODUCT-37973256064`, cold/retrieval success 1.0 per
`research/portfolio/PROGRAM_AUDIT_GLOBAL_2026-10-10.md`).

## 4. Substrate declaration (ADB-v5)

Credential-free, locally-served, deterministic multi-page REST site. Python 3.12 standard library
only (`http.server.ThreadingHTTPServer`, `urllib.request`, `html.parser`, `json`, `hashlib`,
`random`, `statistics`, `socket`, `threading`). No browser, no network egress, no credentials, no
model calls. HTTP on `127.0.0.1` with an OS-chosen ephemeral port (the literal
`ephemeral-not-frozen` identifies the transport; the port is not part of the frozen identity).

- **Bootstrap (carry-chained):** `GET /`, `/hub`, `/boot/1`..`/boot/5` = 7 requests. `/boot/5`
  yields the session manifest: the ordered role registry `R1..R6` and the ascending task list
  `['0.0','0.25','0.5','0.75']`.
- **Role discovery (fixed carry chain):** per role, `GET /disc/<role>/1` returns a session nonce
  `N_r`; `GET /disc/<role>/2/<N_r>` returns partial token `P_r` iff `N_r` is the session-valid
  nonce; `GET /disc/<role>/3/<P_r>` returns resolved token `T_r` and commits role `r` iff `P_r`
  is valid. Each step requires the previous step's value; the chain mixes the role id with the
  session secret. No arm can resolve a role in fewer than 3 requests without persisting `T_r`
  across tasks.
- **Tasks:** task at level `n` requires the first `h(n)=8n` of `R1..R6` committed and a
  subsequent `GET /verify` confirming committed state within `B(n)` server requests. Per-task
  budget `B(n) = {0.0:11, 0.25:15, 0.5:16, 0.75:18}`. The task specification is handed to every
  arm as the task input and is never fetched over HTTP (uniform across arms), so no arm pays a
  spec-fetch request; T-AMORT-REUSE's per-task costs are `[9,7,7,7]` (session total 30), with the
  one shared `/tasks` request charged to its warm-up task.
- **Bank:** `F=2` families, 3 sessions per family, 4 tasks per session = 24 test tasks per arm.
  High novelty is `n>=0.5` = 12 tasks per arm; low novelty = 12.
- **Authorship separation:** the site (ground-truth and request-log authority) never imports an
  arm module; no arm reads the site source; the retrieval index module cannot read the site
  source or the evaluated session/family.
- **Determinism:** all topology, ordering, disc values and task banks are generated from the
  frozen declaration and seed `20261010`. A repeat episode must produce identical counters.

## 5. Canonical declaration object (frozen; gate I6 target)

EXECUTE must render the site so that its canonical topology object equals this object exactly,
serialized with `json.dumps(obj, sort_keys=True, separators=(",", ":"))`. The informational
DESIGN cross-check digest (non-binding; I6 is structural equality) is
`sha256(canonical(declaration)) = 8e8268a4a6f5183458caa7d91055968294bc9756571629cba25422d612048543`.

```json
{
  "bootstrap_steps": ["root", "hub", "boot/1", "boot/2", "boot/3", "boot/4", "boot/5"],
  "budgets": {"0.0": 11, "0.25": 15, "0.5": 16, "0.75": 18},
  "discovery_steps_per_role": 3,
  "families": 2,
  "hidden_roles": "h(n)=8n",
  "levels": [0.0, 0.25, 0.5, 0.75],
  "roles": 6,
  "schema": "ADB-v5-declaration-1",
  "seed": 20261010,
  "sessions_per_family": 3,
  "site_policy": "keep-alive-disabled"
}
```

## 6. Arithmetic certificate

Computed in DESIGN by a non-outcome-bearing stdlib probe (python 3.12.15, `/tmp` only): no arm
was run and no success was measured. Per-task request costs:

| level n | h(n) | B(n) | cold 3h+8 | retrieval server 3h+6 | retrieval total 3h+9 | treatment | PC h+8 |
|---|---|---|---|---|---|---|---|
| 0.0  | 0 | 11 | 8  | 6  | 9  | 9  | 8  |
| 0.25 | 2 | 15 | 14 | 12 | 15 | 7  | 10 |
| 0.5  | 4 | 16 | 20 | 18 | 21 | 7  | 12 |
| 0.75 | 6 | 18 | 26 | 24 | 27 | 7  | 14 |

- Success = committed + `/verify` within `B(n)` server requests. **Success matrix:**
  cold `{T,T,F,F}`, retrieval `{T,T,F,F}`, treatment `{T,T,T,T}`, PC `{T,T,T,T}`.
- **High-novelty stratum (12 tasks):** cold `k=0/12`, retrieval `k=0/12`, treatment `k=12/12`,
  PC `k=12/12`.
- **Wilson 95% (z=1.959963984540054, n=12):** comparator `k=0` -> point `0.0`, hi `0.242494`;
  treatment `k=12` -> point `1.0`, lo `0.757506`. Intervals are disjoint and non-degenerate.
  Boundary: comparator `k<=6` gives hi `0.7462 < 0.7575` (certified); `k>=7` gives hi `0.8067`
  (overlap -> FALSIFIES).
- **Total-cost gaps** (comparator total minus treatment total; retrieval total includes its 3
  local probes): cold `{-1, 7, 13, 19}`, retrieval `{0, 8, 14, 20}`; non-decreasing across
  levels, strictly increasing across high-novelty levels; minimum high-novelty gap `13 >= 8`.

Predicted certificate object (frozen; gate I6 target). Informational DESIGN cross-check digest
(non-binding): `sha256(canonical(certificate)) = 2e0145e62e5cdc56e67db2904776208f6f933bcaf87e15cd49b7730b776eaecc`.

```json
{
  "costs": {
    "cold": {"0.0": 8, "0.25": 14, "0.5": 20, "0.75": 26},
    "pc": {"0.0": 8, "0.25": 10, "0.5": 12, "0.75": 14},
    "retrieval_http": {"0.0": 6, "0.25": 12, "0.5": 18, "0.75": 24},
    "retrieval_total": {"0.0": 9, "0.25": 15, "0.5": 21, "0.75": 27},
    "treatment": {"0.0": 9, "0.25": 7, "0.5": 7, "0.75": 7}
  },
  "high_novelty_k": {"cold": 0, "pc": 12, "retrieval": 0, "treatment": 12},
  "success_matrix": {
    "cold": {"0.0": true, "0.25": true, "0.5": false, "0.75": false},
    "pc": {"0.0": true, "0.25": true, "0.5": true, "0.75": true},
    "retrieval": {"0.0": true, "0.25": true, "0.5": false, "0.75": false},
    "treatment": {"0.0": true, "0.25": true, "0.5": true, "0.75": true}
  }
}
```

## 7. Controls

- **PC-FOREKNOWN-SCHEMA** (positive/solvability ceiling): given manifest, registry and resolved
  tokens out of band, must succeed 24/24 (12/12 high). Failure -> MEASUREMENT_INVALID (bank
  unsolvable), not a scientific negative.
- **NC-OOS-SCHEMA** (null): 5 out-of-support sessions (non-ascending sequence, or a registry that
  is not the nested first-`h(n)` draw). Treatment must refuse (UNKNOWN, no commit, no verify):
  `refusal_rate=1.0`, `false_accepts=0/5`.
- **NC-BUDGET-TRUNCATION**: 6 under-funded episodes; zero overrun, recorded failure/partial.
- **M-COUNTER-RECONCILE**: arm counters equal the server request log; mismatches must be 0.
- **M-REPAIR-TRANSIENT**: one injected transient fault per episode; observed
  `repair_attempts` is 1 (charged to `http_requests`) or an honest failure, no hidden retry.
- **PC-EXACT-SESSION-REPLAY**: 6 replayed treatment sessions reproduce counters exactly.
- **NC / leakage checks**: route-token leak (I7), index leave-instance-out and route-signature
  disjointness (I10), determinism (I8).

## 8. Decision rule

Integrity gates first: any failure of I1..I10 (`spec.json#decision_rule.integrity_gates`) ->
`status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`. Then:

- **SUPPORTS** iff P1 AND P2 AND P3 AND P4 AND P5 AND P6.
- **FALSIFIES** iff NOT (P1 AND P2).
- **MIXED** iff P1 AND P2 AND NOT (P1 AND P2 AND P3 AND P4 AND P5 AND P6).
- **INCONCLUSIVE** on bind/transport failure before the matrix completes.

This is a total, disjoint partition of every integrity-passing case. P1/P2 = comparator
high-novelty point `<0.95` AND comparator Wilson hi `<` treatment Wilson lo. P3 = treatment
12/12 high (point 1.0, Wilson lo `0.757506 >= 0.75`) AND 12/12 low. P4 = per-task mean
comparator-minus-treatment total-request gap non-decreasing across levels and strictly increasing
across high-novelty levels for both comparators. P5 = minimum high-novelty gap `>= 8`. P6 = exact
certificate agreement (success matrix and per-condition ledger equal section 6).

`result.json` reports per-arm high-novelty success, Wilson intervals, the success matrix, the
ledger, and the gate outcomes. A valid negative is `status=COMPLETE` with `outcome` in
{FALSIFIES, MIXED}; infrastructure failure is never encoded as a scientific negative.

## 9. Counters and honesty predicates

Four mandate counters per episode: `http_requests` (server-logged ground truth),
`retrieval_calls`, `verification_calls`, `repair_attempts`. Subsets `bootstrap_requests` and
`discovery_calls` are never summed with `http_requests`. Frozen predicate:
`arm_reported_http_requests == server_logged_requests` AND `bootstrap_requests + discovery_calls
+ verification_calls <= http_requests` AND `retrieval_calls`/`repair_attempts` recorded
independently. `latency_ms` and model tokens are excluded as decision inputs.

## 10. EXECUTE procedure and abort gates

1. Materialize `research/runtime/adb_bank.py` (site, arms, oracle) and
   `research/runtime/adb_harness.py` from sections 4-5.
2. **I6** render-equality: canonical declaration == section 5; recomputed certificate ==
   section 6.
3. **I1** positive control 24/24; **I2** null refusals 5/5.
4. **I9** low-novelty treatment liveness first (abort gate): 12/12 with per-task cost `<= B(n)`.
5. Test matrix: 4 arms x 24 tasks = 96 episodes in seeded arm-blind order.
6. Controls: 6 truncation, 6 repair, 6 replay.
7. **I3/I4/I5/I7/I8/I10** reconcile counters, leakage, determinism, contamination.
8. Compute high-novelty k, Wilson intervals and gaps; apply section 8; emit `result.json`,
   `report.md`, `provenance.json`.
9. Any integrity failure aborts to MEASUREMENT_INVALID; bind/transport failure to INCONCLUSIVE.
   No synthetic fallback.

## 11. Contamination / leakage checks

Per-arm fresh server process and in-memory namespace; per-arm request logs; leave-instance-out
retrieval index; no route literal or absolute URL in any rendered page; arm route-trace
signatures disjoint except the declared shared navigational routes (root/hub/boot/verify). Any
violation -> MEASUREMENT_INVALID.

## 12. DESIGN-phase probes (non-outcome-bearing)

Run in `/tmp` only, no repo writes, no arm execution: (a) stdlib import probe - all required
modules present on python 3.12.15; (b) localhost `ThreadingHTTPServer` canary bound
`127.0.0.1:ephemeral` and returned HTTP 200; (c) pure-arithmetic certificate over the frozen
declaration confirming the cost table, success matrix, Wilson bounds, gap monotonicity and
threshold attainability. These probes measure nothing about the arms; they establish
prerequisites and arithmetic satisfiability only.

## 13. Deliverable and reuse

`research/runtime/adb_bank.py` (generator + arms + oracle) and `research/runtime/adb_harness.py`,
plus `research/experiments/EXP-RUNTIME-38085184570/bank_manifest.json`, with sha256 recorded in
`provenance.json`. Downstream Runtime work (and the Product four-arm benchmark) may bind this
bank as the B2 substrate under the declared policies. This does not certify open-Web or
real-agent transfer.

## 14. Artifacts

`result.json` records raw per-episode ledgers, the success matrix, Wilson intervals, gap series,
gate outcomes and the deliverable hashes. `provenance.json` records run id, commits, environment,
code paths and hashes. Frozen inputs (request/spec/prereg) are hashed by `freeze.json`.

## 15. Validity threats and limitations

- **Declaration-contingent result.** Under a byte-faithful render, SUPPORTS is largely the
  declaration taking effect; the genuinely falsifiable content is render divergence, leakage,
  counter dishonesty, truncation/repair behaviour, out-of-support false acceptance and
  contamination.
- **Declared strategy bounds, not optimal agents.** Cold and retrieval are declared as the
  strongest bounded policies consistent with no cross-task persistence. A real memory-carrying
  LLM agent (readiness condition 3) could erase the declared memory asymmetry; this is not
  measured here.
- **Comparator coincidence.** Retrieval saves only the fixed 2-request navigation prefix, so its
  stratum-level success profile coincides with cold; the two comparators jointly bracket the
  ceiling rather than testing independent mechanisms.
- **Synthetic substrate.** No third-party site exhibits this exact structure; the result is an
  instrument certificate, not a Web-transfer claim.
- **Power.** n=12 per arm is small; the decision rule relies on disjoint Wilson intervals
  (conservative), and the predicted separation (`k=0` vs `k=12`) is large.
- **Spec-fetch convention.** Task specifications are handed to every arm out of band (not an HTTP
  request), so no arm is charged for them; every comparator cost dimension that is charged is
  charged uniformly across arms. A future variant that delivers specs over HTTP would raise all
  arms roughly equally and would require recomputing the certificate (P6) before reuse.

## 16. Failure transmission semantics

Infrastructure/substrate failure is recorded in `failure.json` / `validity_notes` and mapped to
MEASUREMENT_INVALID or INCONCLUSIVE with the smallest unblocking action. It is never encoded as
scientific falsification. A frozen transaction is not repaired in place; a successor is a new
experiment with a new mandate.
