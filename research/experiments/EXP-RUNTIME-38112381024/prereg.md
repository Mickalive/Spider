# Preregistration: EXP-RUNTIME-38112381024 (Runtime)

**Experiment ID**: EXP-RUNTIME-38112381024
**Lane**: runtime
**Design contract version**: 2
**Mode**: DESIGN ONLY — no outcome-bearing measurement. The only DESIGN computation is a closed-form arithmetic/satisfiability dry-run over the frozen construction constants (no HTTP, no server, no arm execution).

---

## 1. Director mandate (binding)

- cycle_id `38111995317`, action **CONTINUE**, target claim **C-MEAS-VALID**, `cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`.
- Dependencies named in `director_mandate.allocation.dependencies` (`C-PARAM-INHERIT`, `C-LLM-INHERIT`) are owned by other lanes, are **not** in the runtime lane charter's `priority_claims`, and are therefore **not** claim ids here. The only claim id in this packet is `C-MEAS-VALID`.
- **Binding strategic question**: Can a non-degenerate *asymmetric-discovery* task bank be certified arithmetically BEFORE freeze — cold re-derivation and a retrieval-shaped comparator demonstrably below the success ceiling at high residual novelty (`B-COLD-RE-DERIVE` and `B-RETRIEVAL-SHAPED` `success_rate < 0.95` at `novelty >= 0.5` on at least one task family, matched correctness `>= 0.80` for all arms), a real treatment/comparator behavioural distinction, honest per-condition counters (`http_requests + retrieval_calls + verification_calls + repair_attempts`) and a preregistered contamination/dynamic-range certificate — delivered as a reusable substrate that unblocks the flagship inheritance benchmark (B2), recording a **bounded substrate-class negative (and freezing nothing)** if the certificate is unsatisfiable on every credential-free substrate tested, on a substrate *materially different* from the mandatory-discovery deterministic REST class?
- **Excluded by mandate**: a fourth re-run of the mandatory-discovery deterministic credential-free REST certificate (the construction `EXP-PRODUCT-37989728440` falsified at the 1.0 ceiling). This design is a materially different construction.
- **Parent handoff** `EXP-RUNTIME-37973247935` is **SUPERSEDED as authorization** and retained strictly as continuity evidence (its `next_question` is NOT executed here).

## 2. Question

Can a credential-free, deterministic, multi-task-**session** task bank be constructed in which one-time session/resource/schema discovery is amortized or cached across tasks, such that BEFORE freeze and **purely arithmetically** the baselines sit below the 0.95 ceiling at high novelty while every arm keeps matched correctness `>= 0.80`, with a real treatment/comparator distinction, honest counters and a contamination/dynamic-range certificate — and does the realized deterministic run reproduce that arithmetic without the baselines returning to the ceiling? If unsatisfiable on every credential-free family tested, record the bounded substrate-class negative and deliver no validated bank.

## 3. Hypothesis

- **H1 (pre-freeze arithmetic certificate, construction-level).** Per session of `K=8` tasks exactly `L=1` is a CHAIN task whose required session-scoped binding (a 128-bit secret `s`) is revealed ONLY in the first successful commit receipt of a designated earlier task and is NOT re-derivable from any idempotent endpoint. Any agent whose readable response set excludes `s` cannot emit the correct chain value except with probability `<= 2^-128`. Hence `B-COLD-RE-DERIVE` and `B-RETRIEVAL-SHAPED` (stale/rotated retrieved binding) solve exactly `K-L = 7` tasks: baseline high-novelty `success_rate = (K-L)/K = 7/8 = 0.875`. `T-AMORTIZED-DISCOVERY` solves `K/K = 1.000`. Window: `0.80 <= 0.875 < 0.95`, margin `1/K = 0.125`.
- **H2 (realized, deterministic).** The realized run reproduces H1 exactly on `>= 1` family (expected on both), and the control lattice confirms causality (see §7).
- **H3 (bounded negation).** If on every family the realized baseline high-novelty `success_rate >= 0.95`, or any arm falls below `0.80`, the certificate is unsatisfiable for this asymmetric-discovery class too and the **bounded substrate-class negative** is recorded with no bank delivered.

## 4. Falsifier (frozen labels)

- **F-CERT-ARITH**: pre-freeze arithmetic certificate false on every family → `FALSIFIES`, bounded class-negative.
- **F-CEILING**: realized baseline high-novelty `success_rate >= 0.95` on all families (asymmetry not enforced / binding leaked or re-derivable) → `FALSIFIES`, bounded class-negative (never a treatment effect).
- **F-FLOOR**: any arm `< 0.80` at any level on all families → `FALSIFIES`, floor violation.
- **F-LEAK**: `NC-NO-LEAK` finds the chain binding (or a re-derivable equivalent) in an idempotent response, or the one-time receipt is re-readable → `FALSIFIES`, bounded class-negative.
- **F-SUBSTRATE**: `PC-EXACT-REPLAY success_rate < 1.0`, or an unsolvable cell → `MEASUREMENT_INVALID`.
- **F-CONTROL**: any null-control numeric prediction violated → `MEASUREMENT_INVALID`.
- **F-RECOMPUTE**: independent recompute mismatch → `MEASUREMENT_INVALID`.
- **F-INFRA**: server start / arm execution failure → `BLOCKED`/`MEASUREMENT_INVALID`, never encoded as a scientific negative.

## 5. Construction

- **Substrate**: credential-free, deterministic Python stdlib `http.server` on `127.0.0.1`, `SEED=38112381024`. Real localhost HTTP; no browser, no model, no credentials, no external network. `model_calls=0`, `model_tokens=0`.
- **Material difference from the excluded class**: `EXP-PRODUCT-37989728440` used a *single-task* REST class where discovery was **mandatory and symmetric** (every arm could read the session token, resource id and schema per task); both baselines reached the 1.0 ceiling. This construction makes discovery **asymmetric across a multi-task session**: exactly one session-scoped 128-bit binding per session is revealed exactly once in a completion receipt and is not re-derivable from any idempotent endpoint. Not a re-run of the excluded certificate.
- **Families**: `F1 = CHAIN-BINDING-RECORDS` (documents), `F2 = CHAIN-BINDING-WIDGETS` (widgets); disjoint abstract vocabulary and wire names.
- **Session**: `K=8` tasks in fixed frozen order. Secret `s = random.Random(session_seed).getrandbits(128)`. Endpoints: `GET /s/{sid}/session` → schema/resource_base/epoch (idempotent); `GET /s/{sid}/task/{i}` (idempotent); `POST /s/{sid}/task/{i}/commit` → `{ok, receipt:{next_resource_id?}}` (stateful, idempotent-rejected after first success). The single CHAIN task omits `resource_id`; its correct value is `s`; `s` is revealed ONLY in the first successful commit receipt of a designated earlier task, and a later re-read returns `409`/redacted. `s` rotates per session.
- **Novelty ladder**: `0.00` no chain, action fully determined by spec; `0.25` schema required, all resource_id present, no chain; `0.50` chain at index 5, reveal in task 4's receipt (depth 1); `0.75` chain at index 7, reveal in task 5's receipt (depth 2; a one-step-only reader fails).
- **Arms**: `T-AMORTIZED-DISCOVERY` (fetch `/session` once, retain context, record & apply the binding); `B-COLD-RE-DERIVE` (context reset; re-fetch `/session` per task; no prior receipt); `B-RETRIEVAL-SHAPED` (cold + one cross-session stale retrieval, `retrieval_calls=1`/task); `B-EMPTIED-CONTEXT` (ablation; treatment with forced context clear).
- **Frozen retry policy**: one repair attempt after a failed commit (re-issue `GET /task/{i}`, re-POST). A re-deriving arm's repair also fails.
- **Honest counters** per trajectory per session: `http_requests, retrieval_calls, verification_calls, repair_attempts, model_calls(0), model_tokens(0), latency_ms(advisory only)`. Predicted at novelty `>= 0.5`: `B-COLD/B-EMPTIED/B-RETRIEVAL http=26` (8+8+1 repair GET+8+1 repair POST), `T=17` (1+8+8); `B-RETRIEVAL retrieval=8`; `T repair=0`. Counters are reported but are **NOT** a certificate condition (the certificate axis is `success_rate`/correctness).
- **Cells / seeds**: `{F1,F2} x {0.00,0.25,0.50,0.75} x 4 arms x N_SESSIONS=20`, plus control cells. Session seed `= SEED + stable integer hash(family, novelty, session_index)`; process-randomized `hash()` never used. Deterministic ⇒ each cell's fraction is an exact multiple of `1/K`.
- **Identifiability**: the certificate asserts a substrate property P (one task requires a one-time 128-bit secret absent from every idempotent response). Given P, ANY agent whose evidence set excludes `s` cannot emit the correct value except with probability `<= 2^-128`, so the baseline failure is forced by P, not by a script's memory policy. P is tested mechanically by `NC-NO-LEAK`. The arms are deterministic witnesses of P; the packet claims a substrate property, never a real-agent treatment effect.

## 6. Baselines and controls

**Baselines**
- `B-COLD-RE-DERIVE` — strongest legitimate from-scratch comparator; expected `1.000` at `0.00/0.25`, `0.875` at `0.50/0.75`. Constraint: `< 0.95` at `novelty >= 0.5` on `>= 1` family; `>= 0.80` matched.
- `B-RETRIEVAL-SHAPED` — cold + one stale cross-session retrieval; expected `0.875` at high novelty. Same constraint.
- `T-AMORTIZED-DISCOVERY` — treatment; expected `1.000` everywhere.
- `B-EMPTIED-CONTEXT` — ablation; expected `== B-COLD-RE-DERIVE`.

**Positive control**
- `PC-EXACT-REPLAY` — oracle given full discovery up front commits every task: `== 1.000` at every novelty/family (`M-PC-EXACT-REPLAY-PASS` true). Failure → `F-SUBSTRATE`.

**Null controls (stable ids)**
- `NC-SHUFFLED-BINDING` — permutation null; `== 0.875` at `novelty >= 0.5` (else `F-CONTROL`).
- `NC-EMPTIED-CONTEXT` — `== B-COLD-RE-DERIVE` at every level.
- `NC-NO-DISCOVERY-DIRECT` — `1.000` at `0.00`, `<= 0.875` at `>= 0.50`.
- `NC-SHALLOW-LAST-RESPONSE` — `1.000` at `0.50`, `0.875` at `0.75` (depth discriminator).
- `NC-NO-LEAK` — secret must NOT appear in any idempotent response consumed by a re-deriving arm; receipt returned exactly once (re-read `409`/redacted). Failure → `F-LEAK`.
- `NC-FAMILY-ISOLATION` — cross-family binding must fail.
- `NC-EQUAL-BUDGET`, `NC-NO-SYNTHETIC`, `NC-ARM-BLIND-SCORING`, `NC-COUNTER-INTEGRITY` — tooling/fairness/accounting guards.

## 7. Pre-freeze arithmetic certificate (BEFORE freeze)

Closed form from frozen constants only. Predicted `success_rate`:

| novelty | T | B-COLD | B-RETRIEVAL | B-EMPTIED |
|---|---|---|---|---|
| 0.00 | 1.000 | 1.000 | 1.000 | 1.000 |
| 0.25 | 1.000 | 1.000 | 1.000 | 1.000 |
| 0.50 | 1.000 | 0.875 | 0.875 | 0.875 |
| 0.75 | 1.000 | 0.875 | 0.875 | 0.875 |

- **CERT-A (dynamic range)**: at each of `0.50`, `0.75`, `0.875 < 0.95` → HOLDS.
- **CERT-B (floor)**: min arm `0.875 >= 0.80` → HOLDS.
- **CERT-C (distinction)**: `1.000 - 0.875 = 0.125 = 1/K >= 1/K` → HOLDS.
- **CERT-D (non-vacuity)**: too-few-chain (baseline `1.000 >= 0.95` → F-CEILING) and too-many-chain (baseline `< 0.80` → F-FLOOR) are reachable alternatives; `L=1, K=8` sits strictly inside `(0.80, 0.95)`.

**Certificate verdict**: SATISFIABLE on both F1 and F2 from arithmetic alone. Because the substrate is deterministic, EXECUTE must reproduce these exact fractions (`0` or `8` of 8 tasks per cell); a realized mismatch is itself the falsification (`F-CEILING`/`F-FLOOR`/`F-LEAK`), never silently accepted.

## 8. Satisfiability dry-run and self-attack (DESIGN)

A satisfiability/identifiability probe over the frozen constants (no HTTP/server/arm execution) proves every decision branch is reachable and non-vacuous, with a concrete realized trigger for `SUPPORTS`, `F-CEILING`, `F-FLOOR`, `F-LEAK`, `F-SUBSTRATE`, `F-CONTROL`, `F-RECOMPUTE`, `F-INFRA` and `MIXED`. Self-attack findings (`SA-01..SA-12`, full text in `spec.json#pre_freeze_satisfiability_dry_run`), with resolutions: circularity (grounded in property P + live leak scan + floor), floor violation (frozen `L=1`), symmetric-rediscovery relapse (only the chain secret is one-time), shallow-depth confound (depth-2 novelty + `NC-SHALLOW-LAST-RESPONSE`), cost-not-success confound (certificate is correctness, counters non-gating), chance success (`2^-128`), single-family artifact (F1/F2), latency smuggling (excluded), governance gap (certificate bound to realized branches; script not editable), budget asymmetry (`NC-EQUAL-BUDGET`), retrieval-comparator weakness (bounded to this bank), empty/unreachable branch risk (reachability matrix).

## 9. Measurement validity (V01–V13)

Blocking: `V01` pre-registration before any run; `V02` certificate is a prediction, not a run; `V03` determinism via frozen seeds; `V04` credential-free (`model_calls=0`); `V05` raw-evidence retention (re-analyzable); `V06` frozen-input re-verification; `V07` binding causality (`NC-SHUFFLED-BINDING`/`NC-EMPTIED-CONTEXT` each equal baseline); `V08` no-leak; `V09` equal budget/tooling; `V10` no synthetic fallback; `V11` latency excluded from gates; `V12` recompute. Non-blocking: `V13` records the program-level governance gap that the freezer does not compute/enforce the certificate (see §10).

## 10. Decision rule (fail-closed, ordered)

Controls and the substrate certificate are read FIRST; the certificate and success comparison are read only if substrate and controls are valid.

- **C1** pre-freeze arithmetic certificate holds for `>= 1` family (DESIGN asserts TRUE, 0.875).
- **C2** substrate validity: `PC-EXACT-REPLAY == 1.000` at every cell (else F-SUBSTRATE).
- **C3** controls: all null-control predictions hold (else F-CONTROL/F-LEAK).
- **C4** realized dynamic range: on `>= 1` family, `B-COLD` and `B-RETRIEVAL < 0.95` at each of `0.50/0.75` and every arm `>= 0.80` (else F-CEILING/F-FLOOR, bounded class-negative).
- **C5** realized certificate match: realized equals prediction exactly.
- **C6** treatment distinction: `T - B-COLD >= 0.125` and `T - B-RETRIEVAL >= 0.125`, causally confirmed.
- **C7** accounting honesty: `model_calls=0`, `model_tokens=0`; counters complete with predicted ordering (non-gating).
- **C8** recompute: zero mismatches.

`OVERALL_OUTCOME`: `SUPPORTS` (C1–C8 pass), `FALSIFIES` (bounded substrate-class negative via F-CEILING/F-FLOOR/F-LEAK), `MIXED` (window holds on `>= 1` family but a non-control C5–C8 item partially fails), `INCONCLUSIVE`, `MEASUREMENT_INVALID` (F-SUBSTRATE/F-CONTROL/F-RECOMPUTE/infra).

## 11. v2 freeze eligibility

- `decision_rule_reachability`: **PASS** (every branch reachable; bounded-negative exit bound to decisive realized check).
- `measurement_prerequisites`: **PASS** (stdlib-only; bank realized literally from frozen literals; deterministic certificate).
- `baseline_identifiability`: **PASS** (distinguishable deterministic signatures; asymmetry forces failure).
- `control_sensitivity`: **PASS** (every control has a pre-declared numeric outcome; `latency_ms` excluded).
- `treatment_liveness`: **PASS** (treatment executable with stdlib only, exercised in every session).
- `freeze_artifacts_bound`: **NOT_APPLICABLE** (all interpretation-determining constants embedded in `spec.json`/`prereg.md`, which the freezer hashes; no pre-existing mutable fixture/task-bank/code dependency; `freeze_artifacts=[]`).

## 12. Consequences

- **Positive**: B2 unblocked for this construction — a credential-free, deterministic, reusable multi-task-session bank with a pre-freeze arithmetic certificate: baselines `0.875` (non-ceiling, `>= 0.80`), treatment `1.000`, per-session counter separation (`http_requests 17` vs `26`; `retrieval_calls 0` vs `8`). The flagship inheritance benchmark gains genuine dynamic range. `C-MEAS-VALID` gains a recheckable substrate-construction fact at the packet's bounded scope; any status change is the DIRECTOR's, not this packet's. No Product Core promotion is implied or authorized.
- **Negative**: bounded substrate-class negative recorded — even the asymmetric-discovery multi-task-session construction cannot produce a pre-freeze-certifiable non-degenerate credential-free task bank. The decision is to stop constructing credential-free synthetic banks for this purpose and redirect to (a) an external-agent benchmark on a provisioned model endpoint, or (b) procedure caching. Do not promote, do not deliver a bank, and do not re-run the excluded mandatory-discovery deterministic REST certificate.

## 13. Historical precedents

- **P2-REPLAY-COST** (sha `9687ff787f2d74460bb7006826008852f5b4416b`): 8.5x replay headline withdrawn to 1.002x on matched tasks → this design uses matched task families and fully counted counters; it certifies a substrate property, not an economic ratio. `DISTINCT_EXTENSION`.
- **P2-BLIND-COMPOSITION** (sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`): weak baselines / oracle-guided stopping inflate results → strongest from-scratch comparator + permutation null + emptied-context ablation. `DISTINCT_EXTENSION`.
- **P2-MIND2WEB** (archived Codex section 1): route overlap ≠ causal composition → measures a concrete one-time information asymmetry with a mechanical no-leak scan. `DISTINCT_EXTENSION`.
- **P2-AUTOMATION** (archived Codex section 2): immutable request identity, hash-pinned inheritance, workflow/validity separation → preserved; records the `EXP-PRODUCT-37989728440` asserted-but-unenforced certificate gate and binds the certificate to realized branches. `DISTINCT_EXTENSION`.
- **P2-WP003 / P2-WP003B** (sha `292e3243d9bc7a3b88712788a7cb05709eb74eb9`; `f6cfdfc749cae9eb4d9fcc4b11b94b63a2bcfb6e`): Web-dynamics state-feature leakage — no possible duplicate. `NO_MATCH`.
- **Parent** `EXP-RUNTIME-37973247935`: `MEASUREMENT_INVALID`; its out-of-surface oracle repair is subordinate and NOT executed here.

*This preregistration is a self-contained binding mirror of `spec.json`; where the two differ, `spec.json` governs.*
