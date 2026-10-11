# EXP-RUNTIME-38164599133 — Preregistration

Lane: `runtime`
Claim ids: `C-MEAS-VALID`
Design contract: v2
Director mandate cycle: `38163904838` (action `CONTINUE`, target claim `C-MEAS-VALID`, `cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`)
Parent handoff: `research/experiments/EXP-RUNTIME-37973247935/handoff.json` sha256 `984049809ebf393e805f59c9b8d083caf2ebfc387348079b06ccacbe41b8928e` (carried for continuity only; SUPERSEDED by the mandate).

This preregistration is frozen before any confirmatory bank execution. It fixes the construction,
the arms, the counters, the controls and their taxonomy, the validity gates, the primary metric,
the pre-freeze certificate and the decision rule. Nothing here is weakened after outcomes are
visible.

**Resume, not rewrite.** The immediately preceding same-mandate PREFREEZE experiment
`EXP-RUNTIME-38151074771` had a substantively complete design (all six `freeze_eligibility` checks
PASS, `freeze_artifacts_bound` NOT_APPLICABLE with reason) whose only failure was the shared
independent design-review model outage (`model_design_review`: `opencode/exo-free`, exit 1,
category substantive; state fingerprint `3b9ff5e4e9e73f23e368efb4`). The current Director mandate
records this and re-issues the work as RESUME-first. This DESIGN therefore replicates that frozen
construction **exactly** at the new experiment id and repairs its single material weakness: the
predecessor's eligibility certificates were backed only by ephemeral `/tmp` probe files (absent
here), so downstream agents had to ATTEST the checks rather than RUN them. This packet embeds the
complete probe source and its verified deterministic output inside the frozen `spec.json`, so every
check is reconstructible and runnable from the frozen packet alone. No construction literal is
changed, no control is removed, and the frozen decision rule is unchanged.

---

## 1. Question (from the binding mandate)

Can a credential-free task bank engineered for ASYMMETRIC discovery — multi-task sessions in which
one-time session / resource / schema discovery is amortized or cached across tasks, and therefore
materially different from the bounded-negative mandatory-discovery deterministic REST class —
receive a **pre-freeze, arithmetically checkable dynamic-range certificate**
(B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED `success_rate < 0.95` at `novelty >= 0.50` on at least one
family, `matched_correctness >= 0.80` for all arms, and a treatment/comparator distinction)
so that it can serve as the reusable substrate that unblocks the flagship inheritance benchmark
(B2), recording a bounded substrate-class negative and freezing nothing if the certificate is
unsatisfiable on every credential-free substrate tested?

This packet is a **measurement-substrate construction and certification**. It changes no claim
status, promotes nothing to Product, and makes no real-agent capability claim.

## 2. Scope and interpretation boundary (disclosed, not hidden)

- Claim scope: `C-MEAS-VALID` only, bounded to the constructed two-family credential-free stdlib
  substrate. `C-RESIDUAL-NOVELTY`, `C-PARAM-INHERIT`, `C-LLM-INHERIT`, `C-PRODUCT-ECON` are
  **not** touched.
- Not authorized by the mandate (and not run here): a fourth re-run of the mandatory-discovery
  deterministic REST certificate (`EXP-PRODUCT-37989728440` class); the superseded parent
  out-of-surface oracle question (`EXP-RUNTIME-37973247935`) and its three code repairs.
- **What the certificate certifies.** Dynamic range against the mandate-named *memoryless-per-task*
  comparators — exactly the B2 blocker (cold/retrieval at the 1.0 correctness ceiling on the tested
  class). It does **not** certify difficulty for a memory-enabled agent: a policy that carries
  in-session context reaches 1.0 (`T-AMORTIZED-DISCOVERY`, and `NC-RETAIN-RECEIPT` at carry
  distance 1). The one-time binding is a small learnable artefact; the certificate is a
  substrate-validity object for the B2 benchmark, whose LLM arms measure real difficulty on the
  delivered bank. This amortization boundary is measured and disclosed. A class-level `FALSIFIES`
  is correspondingly bounded to the memoryless convention.
- **Retrieval convention.** `B-RETRIEVAL-SHAPED` retrieves from a prior-session store by the
  mandate's memoryless convention (no in-session carry). A retrieval variant that indexes the
  current session's own observations is behaviorally `T-AMORTIZED-DISCOVERY` and scores 1.0; that
  is the boundary, not a hidden crippling of the comparator.

## 3. Substrate class (materially different from the excluded class)

Class: **SESSION-BINDING-AMORTIZED**.

- Transport: Python standard library only (`http.server`, `http.client`, `urllib.request`,
  `hashlib`, `json`, `hmac`). A single in-process server bound to `127.0.0.1`. No persistence beyond
  process memory, no external network, no credentials, no LLM calls, no browser.
- `EXECUTE MUST NOT` import `research/runtime/*.py` or any other repository module into the
  measurement path (stdlib-only, frozen).
- Families: `F1-RECORDS`, `F2-WIDGETS`.
- Session: `K = 8` tasks. `GET /api/v1/{family}/session` returns
  `{session_token, schema, epoch}`. `session_token` is opaque (`SHA-256(server_secret, family,
  novelty, session_index, "token")`) and is **not** the binding.
- One-time binding: the correct `resource_id` of the chain task is a 48-bit value
  `= SHA-256(server_secret, family, novelty, session_index, "binding")` truncated to 12 hex chars.
  It is revealed **exactly once** in the precursor task's commit receipt under field
  **`chain_resource_id`** (named for the chain task, not the immediately-next task: at novelty
  `0.75` the reveal is carried across an intermediate task), is absent from every idempotent
  channel, is consumed on first successful use at the chain task, and any stale/foreign/consumed
  value returns `400`. Re-commit of the precursor returns `409` and never re-reveals the binding.
- Determinism: `server_secret = SHA-256(run_seed, "server_secret")`; the `secrets` module is not
  used for it, so bindings and tokens are reproducible.
- Novelty ladder `[0.0, 0.25, 0.5, 0.75]`:
  - `0.00`: `schema_required=false`; `resource_id` explicit in the task spec; no chain task.
  - `0.25`: `schema_required=true` (wire schema discovered via `/session`); `resource_id` explicit;
    no chain task.
  - `0.50`: `schema_required=true` + exactly one chain task at index `chain(K,0.50)=K-3=5`; binding
    revealed in `precursor(K,0.50)=K-4=4` commit receipt (carry distance 1).
  - `0.75`: `schema_required=true` + exactly one chain task at index `chain(K,0.75)=K-1=7`; binding
    revealed in `precursor(K,0.75)=K-3=5` commit receipt (carry distance 2).
- Novelty fraction: fraction of commit parameters not determined by the task spec union the frozen
  grammar (`0.00 -> 0/4`, `0.25 -> 1/4`, `0.50 -> 2/4` on the chain task, `0.75 -> 3/4` on the
  chain task). The band label is fixed by construction; the certificate gates evaluate at
  `novelty >= 0.50`.

### Protocol surface

| Request | Semantics |
|---|---|
| `GET /api/v1/{family}/session` | create/look up the session -> `{session_token, schema, epoch}`; never contains the binding except in the NC-MECHANISM-OFF ablation |
| `GET /api/v1/{family}/task/{i}` | `{index, intent, resource_id, requires_schema, is_chain}`; chain task has `resource_id=null` |
| `POST /api/v1/{family}/commit` | `{session_token, task_index, resource_id, payload}` -> `200`+receipt; `400` invalid/missing/consumed/foreign; `409` already-committed (never re-reveals). The precursor's first `200` receipt carries the single `chain_resource_id` reveal |

Response invariant: the binding appears only in the precursor's first `200` receipt under
`chain_resource_id`; `/session`, `/task/{i}`, ordinary receipts, and all `400`/`409` bodies must
not contain it (NC-NO-LEAK scans every such body in the mechanism-intact run).

## 4. Arms (frozen policies; arms interact only through the HTTP surface)

| Arm id | Policy | Predicted success at novelty `>=0.50` | Per-session counters `(http, retrieval, verification, repair)` |
|---|---|---|---|
| `T-AMORTIZED-DISCOVERY` | treatment (benchmark inheritor stand-in): one `/session` per session; retain all in-session context including every commit receipt; capture `chain_resource_id`; commit each task once | `1.0` | `(17, 0, 8, 0)` |
| `B-COLD-RE-DERIVE` | mandated comparator: `GET /session` before **every** task and discard all prior task context (no receipt retention); binding not re-derivable; first chain commit `400`, one repair re-attempt `400` | `0.875` (`7/8`) | `(25, 0, 9, 1)` (at `0.00/0.25`: `(24, 0, 8, 0)`) |
| `B-RETRIEVAL-SHAPED` | mandated comparator in the frozen memoryless retrieval convention: cold request pattern (`/session` re-read per task, no carry) plus exactly one retrieval call per task over the frozen prior-session store; retrieves a binding from a **different** session, which the server rejects | `0.875` | `(25, 8, 9, 1)` (at `0.00/0.25`: `(24, 8, 8, 0)`) |
| `PC-EXACT-REPLAY` | positive control: golden-input executor given the exact binding and schema by construction; 1 session read, 8 task reads, 8 commits | `1.0` | `(17, 0, 8, 0)` |

Every arm operates under the same `128`-request/session ceiling; maximum predicted usage is `25`,
so the budget never binds and comparator failure is not budget-induced. `T` and `PC` are expected
to be counter-identical (`(17,0,8,0)`); this is intended — `PC` is a liveness anchor, not a
comparator, and the distinction gate applies only to `T` vs the two comparators.

## 5. Baselines, positive control, null control

- `CEILING-1.0`: the excluded REST class's 1.0 ceiling, cited from `EXP-PRODUCT-37989728440`
  (`design_certified=false`), **not re-run** (mandate).
- `FLOOR-0.0`: floor anchor via `NC-NO-DISCOVERY-DIRECT` (an actor that has a valid session but
  ignores the schema and receipts), isolating schema applicability from mere token presence.
- Positive control `PC-EXACT-REPLAY`: proves the substrate is completable and the scorer
  non-degenerate; also the treatment-liveness anchor (T must equal PC at `1.0`).
- Null/ablation control `NC-MECHANISM-OFF`: the one-time-ness is disabled (the binding is also
  exposed by `/session`) with the identical bank and arms. Expected: comparators `1.0` at
  `novelty >= 0.50` -> certificate **FALSE**; proves the certificate can fire negative and that
  the one-time mechanism produces the dynamic range. NC-NO-LEAK is **not** evaluated in this
  ablation (it intentionally exposes the binding).

## 6. Controls and their frozen taxonomy

**Validity gates** (folded into V1–V7; any failure -> MEASUREMENT_INVALID):
`NC-DOUBLE-RUN`, `NC-COUNTER-INTEGRITY`, `NC-ARM-BLIND-SCORING`, matched manifests, `NC-NO-SYNTHETIC`,
`NC-EQUAL-BUDGET`, `NC-BINDING-UNIQUENESS` (entropy part), `NC-NO-LEAK` (executed and recorded), and
the server-enforcement checks.

**Falsifier control:** `NC-NO-LEAK` — scanning every idempotent/error body for the binding (sole
permitted occurrence is the precursor receipt, once). Firing -> F-LEAK -> **MIXED** (a leaked
binding destroys the asymmetry).

**Liveness controls:** `PC-EXACT-REPLAY == 1.0` and `T >= 0.80` at every band are required for a
SUPPORTS or a FALSIFIES reading; a treatment/PC failure -> MIXED.

**Diagnostic controls** (read diagnostically; never required to equal a single pre-set value for a
FALSIFIES reading):

| Control id | Meaning | Non-degenerate prediction | Degenerate-reading expectation |
|---|---|---|---|
| `NC-EMPTIED-CONTEXT` | T minus context retention | `0.875` at `>=0.50`, `1.0` below | tracks the comparators |
| `NC-SHUFFLED-BINDING` | T given a well-formed binding from another session of the same family; server registry rejects | `0.875` at `>=0.50` | tracks |
| `NC-FAMILY-ISOLATION` | T given a well-formed binding from the other family; server rejects | `0.875` at `>=0.50` | tracks |
| `NC-NO-DISCOVERY-DIRECT` | valid session but spec-only (no schema, no receipts) | `1.0` at `0.00`, `0.0` at `>=0.25` | tracks |
| `NC-RETAIN-RECEIPT` | 1-step receipt retainer (diagnostic) | `1.0` at `0.50`, `0.875` at `0.75` | at/above ceiling |
| `NC-MECHANISM-OFF` | one-time mechanism ablated | comparators `1.0` -> certificate FALSE | comparators at ceiling |
| `NC-K-SWEEP` | construction at `K in {7,9,10}` with identical mechanism and index formula | comparators `6/7`, `8/9`, `9/10` in `[0.80,0.95)` | — |
| `NC-BINDING-UNIQUENESS` | all session bindings pairwise distinct | `80/80` distinct (48-bit) over the scored matrix | — |

## 7. Measurement, counters and unit of analysis

- Sampling: `N_SESSIONS = 20` per `(family x novelty x scored arm)` cell -> `160` tasks per cell;
  `2 x 4 x 4 = 640` scored sessions (`5120` scored tasks). Controls add the cells in §6; a full
  double-run of the scored matrix is required.
- Determinism: one `run_seed` recorded in `provenance.json`; `server_secret` and per-cell seeds
  derived deterministically; no process `hash()`; no wall-clock dependence in outcomes (latency
  recorded advisory only).
- Primary metric: per-cell arm `success_rate` (exact match of the final committed state against the
  deterministic ground-truth manifest); `matched_correctness` equals `success_rate` under
  exact-match scoring.
- Counters: `http_requests`, `retrieval_calls`, `verification_calls`, `repair_attempts`; frozen
  invariants `http_requests == session_gets + task_reads + commit_requests`,
  `verification_calls == commit_requests`, `repair_attempts <= verification_calls`,
  `retrieval_calls > 0` only for `B-RETRIEVAL-SHAPED`.
- Unit of analysis: the session; the cell aggregate is the mean over 20 sessions.
- Uncertainty: the construction is deterministic, so cell rates are exact rationals with
  denominator `20*K`; no stochastic interval is claimed, and the boundary note proves no rate can
  land on `0.95` or `0.80`.

## 8. Validity gates (V1–V7)

`V1` packet immutability (frozen request/spec/prereg/design_review untouched), stdlib-only
measurement path, and a code-fidelity manifest (EXECUTE-authored generator/server/executors/scorer
paths + SHA-256 recorded in `result.json.artifacts`); `V2` NC-DOUBLE-RUN byte-identical per-task
outcomes and counters; `V3` NC-COUNTER-INTEGRITY trace re-derivation matches reported counters;
`V4` NC-ARM-BLIND-SCORING interface contract honored; `V5` matched manifests across arms and no arm
protocol violation; `V6` binding entropy recomputed `>= 40` bits; `V7` NC-SHUFFLED-BINDING and
NC-FAMILY-ISOLATION confirm server-enforced session/family scope and binding consumption.

Validity gates and scientific rate measurements are deliberately separated: a measured rate that
differs from the pre-freeze prediction is evaluated by §9, never auto-classified as invalid unless
it co-occurs with a `V1–V7` failure. Diagnostic-control values are never equality-frozen for a
FALSIFIES reading.

## 9. Decision rule (frozen)

A family **certifies** iff, at `novelty >= 0.50`, `B-COLD-RE-DERIVE < 0.95` AND
`B-RETRIEVAL-SHAPED < 0.95`, AND every scored arm (`T, COLD, RETRIEVAL, PC`) has
`success_rate >= 0.80` AND `matched_correctness >= 0.80` at every band, AND behavioural distinction
holds (at least 2 of the 4 counter dimensions distinct between `T` and each comparator, AND
`T-COLD >= 1/8` AND `T-RETRIEVAL >= 1/8` at `novelty >= 0.5`).

- `SUPPORTS`: `>= 1` family certifies AND `V1–V7` pass AND `NC-NO-LEAK` clean AND liveness
  (`PC=1.0`, `T>=0.80`) AND the diagnostic controls are consistent with the **non-degenerate**
  reading (NC-EMPTIED-CONTEXT `~0.875`; NC-MECHANISM-OFF -> FALSE; NC-RETAIN-RECEIPT `>=0.80` at
  `0.50`; NC-NO-DISCOVERY-DIRECT `1.0` at `0.00` / `0.0` at `>=0.25`) -> deliver the certified bank
  as a reusable substrate for B2; `C-MEAS-VALID` substrate-validity evidence only, no claim status
  change, no promotion.
- `FALSIFIES`: zero families certify AND `V1–V7` pass AND `NC-NO-LEAK` clean AND liveness holds
  (`PC=1.0`, `T>=0.80`) AND the non-certification is comparator-attributable — in **both** families
  either a comparator `success_rate >= 0.95` at `novelty >= 0.5` (certificate unsatisfiable on the
  frozen class) or a comparator `success_rate < 0.80` at some band — AND the diagnostic controls
  are consistent with the **degenerate** reading (comparators, NC-EMPTIED-CONTEXT and
  NC-RETAIN-RECEIPT all at/above ceiling; this is expected and does **not** convert the outcome to
  MIXED) -> bounded substrate-class negative: the `SESSION-BINDING-AMORTIZED` class is closed for
  credential-free stdlib deterministic substrates; flag the Global Research Director that the
  flagship benchmark class requires credentialed substrates or a changed product thesis.
  Reachability: diagnostic controls are not equality-frozen for FALSIFIES; the pre-registered
  `NC-MECHANISM-OFF` configuration independently witnesses that the procedure returns FALSE, and
  the rule-level classifier probe synthesizes a degenerate world (comparators `1.0`, diagnostic
  controls tracking them) and returns FALSIFIES — not MIXED.
- `MIXED`: `V1–V7` pass and the classification is neither `SUPPORTS` nor `FALSIFIES` — `NC-NO-LEAK`
  fires (F-LEAK); OR exactly one family certifies; OR a treatment-side failure (`T < 0.80` or
  `PC < 1.0`); OR `NC-RETAIN-RECEIPT = 0.0` at `novelty 0.50` (substrate-solvability failure); OR
  a diagnostic control is inconsistent with **both** readings. Emit the exact repair list; the bank
  is not deliverable as certified.
- `MEASUREMENT_INVALID`: any `V1–V7` failure (infrastructure failure, double-run divergence,
  counter inconsistency, frozen-file modification, arm protocol violation, stdlib-only breach,
  missing code-fidelity manifest, matched-manifest mismatch, server-enforcement failure) -> no
  scientific reading; record the diagnosis and the smallest unblocking next action.
  Infrastructure/substrate failure is never encoded as scientific falsification.

## 10. Pre-freeze arithmetic certificate (executed at DESIGN time)

Closed form: at `novelty <= 0.25` no chain task exists and every `resource_id` is spec-explicit, so
all arms reach `1.0`. At `novelty >= 0.5` each session has exactly one chain task whose correct
`resource_id` is the one-time 48-bit binding; `T` and `PC` hold it (`8/8 = 1.0`), while `COLD` and
`RETRIEVAL` cannot recover it (~`2^47` guesses vs a 128-request budget; no idempotent channel
reveals it; prior-session values are never the current binding by `NC-BINDING-UNIQUENESS`), so
exactly the chain task fails and their session rate is `(K-1)/K = 7/8 = 0.875`; the per-cell rate is
`[20 x (7/8) x 8] / 160 = 140/160 = 0.875`.

Boundary disclosure: a memory-enabled policy that retains the precursor receipt recovers the
binding without extra requests and reaches `1.0` (`NC-RETAIN-RECEIPT`) — the certificate certifies
dynamic range against the memoryless-per-task convention, not difficulty for a memory-enabled agent.

Chain/precursor indexes: `K=8`: `0.50 -> chain 5 / precursor 4` (distance 1),
`0.75 -> chain 7 / precursor 5` (distance 2); formula `chain(K,0.50)=K-3, precursor(K,0.50)=K-4;
chain(K,0.75)=K-1, precursor(K,0.75)=K-3`.

Per-cell certificate: `F1-RECORDS` and `F2-WIDGETS` both certify — comparators `0.875 < 0.95` at
`0.50` and `0.75`, minimum arm correctness `0.875 >= 0.80`, `T/PC` anchor `1.0`, margins `0.075`
below the ceiling and `0.075` above the floor. `K`-sweep `{7:6/7, 8:7/8, 9:8/9, 10:9/10}` is in
`[0.80, 0.95)`; `(K-1)/K` never equals `0.95` or `0.80`, so threshold-boundary ambiguity is
impossible. `NC-MECHANISM-OFF` flips comparators to `1.0` -> certificate `FALSE`. `80/80` bindings
pairwise distinct over the scored matrix. The rule-level decision classifier over synthetic worlds
returns `SUPPORTS`, `FALSIFIES`, `MIXED` (one-family and leak) and `MEASUREMENT_INVALID` as intended
(`all_branches_inhabited=true`).

### DESIGN-time satisfiability probe (cheap, non-outcome-bearing; does not execute the scored bank)

The complete probe source is embedded in `spec.json` at
`pre_freeze_arithmetic_certificate.probe_source`, and its verified deterministic output at
`pre_freeze_arithmetic_certificate.probe_output`. Content hashes:

| Artifact | sha256 |
|---|---|
| probe source (`probe_certificate.py`, embedded in spec) | `c13904106d9c9740b70160cc91d771486d0b4fe2237ea25056a50f50dd05c190` |
| probe output (embedded in spec) | `3f557b649683f8d42da4fb3a5f074e7187de94513451f00c2fa67567c98254ca` |

Verified results (all reproduced this cycle on python `3.12.15`, stdlib only):

- **B1 environment** — all required stdlib modules import (`ok=true`).
- **B2 transport** — a real in-process `ThreadingHTTPServer` on `127.0.0.1` passes `20/20` frozen
  protocol invariants (`B2_transport_all_ok=true`): `session_200`, `session_has_token`,
  `session_has_schema`, `session_no_binding`, `chain_task_resource_null`, `missing_token_400`,
  `ordinary_commit_200`, `ordinary_receipt_no_binding`, `precursor_commit_200`,
  `precursor_reveals_chain_resource_id`, `precursor_field_name_chain_not_next`,
  `precursor_reveal_matches_chain_task_id`, `precursor_recommit_409`,
  `precursor_recommit_no_binding`, `wrong_binding_400`, `wrong_binding_error_no_binding`,
  `foreign_binding_400`, `correct_binding_200`, `chain_recommit_409`,
  `no_leak_idempotent_and_error_bodies`.
- **B2 arm liveness** — every arm-band vector matches the §4 prediction
  (`B2_arm_liveness_all_ok=true`): `T-AMORTIZED-DISCOVERY` and `PC-EXACT-REPLAY` `8/8` at
  `(17,0,8,0)`; `B-COLD-RE-DERIVE` `7/8` at `(25,0,9,1)`; `B-RETRIEVAL-SHAPED` `7/8` at
  `(25,8,9,1)` — at both `novelty 0.50` and `0.75`. `treatment_live=true`.
- **B3 certificate** — comparator cell rates `140/160 = 0.875` in `[0.80, 0.95)`;
  `K`-sweep all in band; `80/80` bindings distinct; no threshold collision (no rate equals `0.95`
  or `0.80`); all four decision branches inhabited (`B3_all_branches_inhabited=true`);
  `NC-MECHANISM-OFF` exposes the binding from `/session` and lets a comparator recover it to a
  `200` chain commit -> comparators flip to `1.0` -> certificate `FALSE`
  (`B3_mechanism_off_flips_comparators_to_1.0=true`).
- Top-level `certificate_satisfiable=true`.

Determinism: two consecutive probe runs produced byte-identical stdout (`cmp` clean).
Durability: the probe is embedded in the frozen `spec.json`, so the checks are runnable from the
frozen packet alone; there is no `/tmp` interpretation dependency. The deterministic freezer hashes
`request.json`, `spec.json`, `prereg.md` and `design_review.json`.

## 11. Freeze eligibility

| Check | Status | Basis |
|---|---|---|
| `decision_rule_reachability` | PASS | all four branches reachable; the embedded rule-level classifier returns SUPPORTS / FALSIFIES / MIXED / MEASUREMENT_INVALID as intended (`all_branches_inhabited=true`); FALSIFIES is not conflated with MIXED because diagnostic controls are not equality-frozen, and `NC-MECHANISM-OFF` independently flips the certificate to FALSE |
| `measurement_prerequisites` | PASS | python `3.12.15` + stdlib present; live loopback transport `20/20`; all arm-band liveness vectors match; deterministic `server_secret`; no credentials/browser/dataset/model access; nothing deferred to EXECUTE; evidence embedded in the frozen spec |
| `baseline_identifiability` | PASS | comparators `0.875` vs ceiling `0.95` (margin `0.075`) and floor `0.80` (margin `0.075`); distinct counter profiles (`retrieval_calls` 8 vs 0); floor anchored at `0.0` by a schema-ignoring but token-bearing actor |
| `control_sensitivity` | PASS | explicit validity/liveness/falsifier/diagnostic taxonomy; every control has a distinct failure mode; `NC-MECHANISM-OFF` flips the certificate |
| `treatment_liveness` | PASS | `T-AMORTIZED-DISCOVERY` was EXECUTED end-to-end over the live loopback transport at novelty `0.50` and `0.75` (`8/8` at `(17,0,8,0)`); `PC` anchors liveness |
| `freeze_artifacts_bound` | NOT_APPLICABLE | at freeze time no mutable local code/task-bank/dataset/fixture exists whose identity could change the interpretation: the DESIGN-time certificate is made durable by EMBEDDING the probe source + verified output in the frozen spec, and the EXECUTE-authored code is authored from frozen literals with `V1` requiring a code-fidelity manifest hashed into `result.json.artifacts` |

`freeze_artifacts`: `[]` (explicitly empty; see `freeze_artifacts_bound`).

## 12. Consequences

- Positive (`SUPPORTS`): B2 — currently gated on benchmark degeneracy — receives a certified
  non-degenerate substrate plus a mechanically verified contamination certificate; downstream lanes
  can preregister it for `C-FRESHNESS` / `C-DELTA-REPAIR` / `C-LLM-INHERIT` work. No product
  promotion and no claim status change.
- Negative (`FALSIFIES`): a bounded `SESSION-BINDING-AMORTIZED` substrate-class negative; the
  factory must seek credentialed substrates or change the product thesis. Nothing is promoted and
  no claim is advanced.
- Measurement-invalid: deliver the exact repair list; never a scientific reading.

## 13. Legacy and predecessor comparison

- `LEGACY: NO_MATCH`. A targeted primary-source scan of the frozen pre-2.0 archive
  (`.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md`, blob
  `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`) for `task bank`, `dynamic range`, `success ceiling`,
  `retrieval-shaped` and `cold re-deriv` returns **zero** matches (`non-degenerate` 1;
  `amortiz` 115, all browser-traversal cost uses). A selective `codex/legacy_artifact_index.json`
  screen for `task bank`/`endpoint` also returned nothing across the 1,401 artifacts. No pre-2.0
  artifact is a non-ceiling asymmetric-discovery task bank with amortized session-scoped discovery.
- Governing legacy guards: `P2-REPLAY-COST` (sha `9687ff787f2d74460bb7006826008852f5b4416b`;
  matched tasks, fully loaded costs, no scripted-replay-as-economics) — enforced here via honest
  per-condition counters and no real-agent capability claim; `P2-AUTOMATION` (archived section 2;
  immutable identity, explicit write sets, hash-pinned inheritance, workflow completion !=
  scientific validity) — enforced by the embedded certificate and the validity/rate separation.
- Nearest precedents cited, not run: Mind2Web V0.50 (retrieval beats exact-route imitation, which
  is why a retrieval-shaped comparator is required) and `P2-REPLAY-COST` (matched-task /
  fully-loaded cost; motivates the four honest counters over latency-only proxies).
- Research-2.0 off-class references: `EXP-PRODUCT-37989728440` and `EXP-PRODUCT-37973256064` (the
  excluded REST class at the `1.0` ceiling; cited, not re-run) and `EXP-PRODUCT-36272385776`
  (a cold-discovery substrate was constructible, but its treatment arm had a code defect).
- Same-mandate Runtime pre-freeze predecessors (`EXP-RUNTIME-38121196004`, `-38112381024`,
  `-38123988847`, `-38125434571`) and the immediately preceding `EXP-RUNTIME-38151074771` all died
  at the independent design-review stage on the shared control-plane/model-routing failure (state
  fingerprint `3b9ff5e4e9e73f23e368efb4`, reviewer model `opencode/exo-free`, exit 1, category
  substantive), not on a scientific defect; none ever froze or executed. This design rigorously
  replicates the `-38151074771` construction, fixes the falsifying-branch unreachability defect
  identified by adversarial review, repairs the ephemeral-probe durability weakness by embedding
  the probe and its verified output in the frozen packet, and re-derives every satisfiability claim
  with fresh byte-deterministic DESIGN-time probes and a re-verified closed-form certificate.
