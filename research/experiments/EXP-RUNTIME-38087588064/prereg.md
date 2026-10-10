# EXP-RUNTIME-38087588064 preregistration

Lane: `runtime` — Claim at stake: `C-MEAS-VALID` — Design contract: v2
Authoring stage: DESIGN (pre-freeze candidate; this file and `spec.json` are the only DESIGN outputs and are not yet frozen).

This preregistration is the binding scientific record for `EXP-RUNTIME-38087588064`. It is written BEFORE any outcome-bearing measurement. Only cheap, non-outcome-bearing satisfiability probes were run in DESIGN (section 12). Everything the decision depends on is declared verbatim here or in `spec.json`.

---

## 1. Mandate and objective

The Global Research Director mandate (`request.json.director_mandate`, action `CONTINUE`, target claim `C-MEAS-VALID`) binds this experiment to one strategic question:

> Can a non-degenerate asymmetric-discovery task bank be certified arithmetically BEFORE freeze — cold re-derivation and a retrieval-shaped comparator demonstrably below ceiling at high residual novelty, a real treatment/comparator behavioural distinction, honest per-condition counters (`http_requests + retrieval_calls + verification_calls + repair_attempts`), and a preregistered contamination/dynamic-range certificate — and be delivered as a reusable substrate on the lane and/or the shipped path that unblocks the flagship inheritance benchmark (blocker B2)? DESIGN must record a bounded substrate-class negative and NOT freeze if the certificate is unsatisfiable on every credential-free substrate tested.

Program blocker **B2** is the reason this exists: no credential-free task bank has yet been produced whose cold and retrieval-shaped comparators are genuinely below ceiling, so any treatment effect on the flagship four-arm inheritance benchmark is unidentifiable regardless of sample size. SPIDER has already instantiated this failure twice — `EXP-PRODUCT-37989728440` and `EXP-PRODUCT-37973256064` measured the deterministic mandatory-discovery REST class at cold/retrieval success **1.0 / 1.0** (floor/ceiling, no dynamic range).

This document designs **ADB-v6** (Asymmetric-Discovery Bank, version 6): a credential-free, locally-served, deterministic REST substrate whose session-scoped carry-chained discovery layer makes cold and retrieval-shaped comparators provably over budget at high novelty while a session-amortizing mechanism and a foreknown-schema positive control remain live. ADB-v6 adds, over the immediately preceding ADB-v5 design (`EXP-RUNTIME-38085184570`), a same-transport **known-degenerate calibration class `CC-DEGENERATE`** whose discovery is query-answerable; the frozen certificate predicate must return `TRUE` for ADB-v6 and `FALSE` for `CC-DEGENERATE`, so an uninformative constant-`TRUE` certificate is detectable rather than assumed. This is the material difference that makes the certificate's non-vacuity an observational prediction (proposition P7, gate I11), not a design assertion.

## 2. Parent handoff and Director disposition (four-way preservation)

`parent_handoff` = `research/experiments/EXP-RUNTIME-37973247935/handoff.json` (sha256 `984049809ebf393e805f59c9b8d083caf2ebfc387348079b06ccacbe41b8928e`). `director_mandate.allocation.parent_handoff_disposition = SUPERSEDE`. The parent handoff is treated strictly as continuity evidence and does **not** authorize the parent's `next_question`.

Preserved four-way distinction from the parent packet:

- **established** (carry as inherited state): `C-MEAS-VALID` remains `VALIDATED` only at the authorship-separated **real-Chromium fixture scope** (`EXP-RUNTIME-36293257855`); the composite-oracle/substrate work in the parent produced no valid out-of-surface transfer measurement in either direction.
- **rejected** (bounded): the parent's out-of-surface composite-oracle **measurement** is `MEASUREMENT_INVALID` and must not be cited as evidence about the underlying mechanism; specifically the parent's `fingerprint_changed=true` on 260/260 episodes was a detector compromise from the volatile hop-by-hop `Connection` header absent from the exclusion set, and its capture-stability gate was mis-specified against prereg §8.
- **unknown**: whether the parent's repaired out-of-surface composite oracle would retain arm-constrained discrimination (point sensitivity/specificity ≥ 0.90, Wilson lower bound ≥ 0.80) on its frozen transfer design — **untested in either direction**.
- **do_not_assume**: that the parent's out-of-surface transfer question is the lane's required next object. The Director explicitly supersedes it. `inherited_next_question` (repair the `Connection`-header exclusion; correct the stability gate to the WAL byte vector) is **not** this experiment's objective and must not be silently substituted for it.

## 3. Claim, scope and construct boundary

- Target claim: `C-MEAS-VALID` (runtime lane priority claim; effective status `EXPERIMENTAL`).
- This is an **instrument/certificate** experiment. It certifies the dynamic range and honesty of a synthetic task-bank instrument under declared, non-omniscient arm policies. It does **not** establish inheritance economics (that is the downstream four-arm benchmark referencing dependencies `C-PARAM-INHERIT`, `C-LLM-INHERIT`, `C-RESIDUAL-NOVELTY`) and does **not** claim transfer to the open Web or to a real memory-carrying LLM agent.
- It is explicitly **not** a re-run of the degenerate deterministic mandatory-discovery REST class (`EXP-PRODUCT-37989728440`, `EXP-PRODUCT-37973256064`).

## 4. Substrate declaration

Credential-free, deterministic, locally-served multi-page REST site; **Python 3.12 standard library only** (`http.server.ThreadingHTTPServer`, `urllib.request`, `html.parser`, `json`, `hashlib`, `random`, `statistics`, `socket`, `threading`). No browser, no network egress, no credentials, no cookies, no model calls, no third-party package. Transport is `http` on `127.0.0.1` with an ephemeral OS-chosen port; the port is not part of the frozen declaration identity (literal `ephemeral-not-frozen`).

### 4.1 Asymmetric class ADB-v6 (the object under certification)

Bootstrap: `GET /` → `hub` → `boot/1..5` (7 requests); `/boot/5` serves the session manifest (ordered role registry `R1..R6`, task list, and the frozen ascending warm-up sequence `["0.0","0.25","0.5","0.75"]`). Discovery is a fixed **3-step carry chain** per role:

1. `GET /disc/<role>/1` → per-role session nonce `N_r`;
2. `GET /disc/<role>/2/<N_r>` → partial token `P_r` iff `N_r` is session-valid;
3. `GET /disc/<role>/3/<P_r>` → resolved token `T_r` and commits the role for the session iff `P_r` is valid.

Each step requires the previous step's value and mixes role id with the session secret. Therefore **no policy can resolve a role in fewer than 3 requests per task without persisting `T_r` across tasks** — the exact capability under test. The task specification is handed to every arm as task input (uniformly, not an HTTP request).

### 4.2 Calibration class CC-DEGENERATE (certificate-sensitivity sibling)

Same transport and bootstrap, but discovery is **query-answerable**: a single `GET /answer/<role>` returns `T_r` directly (1 request per role, no carry chain), and the budget `B_deg(n)` is deliberately generous so that stateless comparators are forced to the ceiling. The frozen certificate predicate (section 6) must return `FALSE` for this class.

### 4.3 Task bank, strata and novelty

- `F=2` families (`F1`,`F2`), 3 test sessions per family × 4 tasks (one per level `n ∈ {0.0, 0.25, 0.5, 0.75}`) = **24 test tasks per arm** for ADB-v6.
- Each session's task list is fixed ascending `["0.0","0.25","0.5","0.75"]`; each task requires the first `h(n)=8n` roles of the ordered registry (`h={0,2,4,6}`).
- **High-novelty stratum** `n ≥ 0.5` = 12 tasks/arm; **low-novelty stratum** `n < 0.5` = 12 tasks/arm.
- `CC-DEGENERATE` calibration bank: one family × 4 high-novelty tasks, run by both comparators (8 episodes).
- Seed: `20261010`.
- Budgets `B(n)={11,15,16,18}`; `B_deg(n)={11,13,15,17}`.
- **Route-leak rule**: no rendered task spec, disc/answer page, hub, boot page or sitemap may contain an absolute URL, the session id, or any of the literals `/s/`, `{sid}`, `/boot/`, `/hub`, `/tasks`, `/disc/`, `/answer/`, `/verify`. The sitemap lists only `/`, `/hub`, `/about`.

## 5. Cost model and embedded declaration

The frozen canonical declaration object (EXECUTE must re-render it exactly; canonicalization = `json.dumps(obj, sort_keys=True, separators=(",",":"))`):

```json
{"bootstrap":["root","hub","boot/1","boot/2","boot/3","boot/4","boot/5"],"budgets":{"0.0":11,"0.25":15,"0.5":16,"0.75":18},"calibration":{"budgets":{"0.0":11,"0.25":13,"0.5":15,"0.75":17},"discovery_requests_per_role":1,"name":"CC-DEGENERATE"},"discovery_steps":3,"families":["F1","F2"],"h":{"0.0":0,"0.25":2,"0.5":4,"0.75":6},"levels":[0.0,0.25,0.5,0.75],"role_rule":"h(n)=8n","schema":"ADB-v6","seed":20261010,"sessions_per_family":3,"tasks_per_session":4,"warmup_sequence":["0.0","0.25","0.5","0.75"]}
```

Derived per-task HTTP cost model (server-logged `http_requests`; `retrieval_total` adds the 3 local index probes counted as `retrieval_calls`):

| arm | n=0.0 | n=0.25 | n=0.5 | n=0.75 | formula |
|---|---|---|---|---|---|
| `B-COLD-RE-DERIVE` | 8 | 14 | 20 | 26 | `3h+8` |
| `B-RETRIEVAL-SHAPED` (server) | 6 | 12 | 18 | 24 | `3h+6` |
| `B-RETRIEVAL-SHAPED` (total incl. probes) | 9 | 15 | 21 | 27 | `3h+9` |
| `T-AMORT-REUSE` | 9 | 7 | 7 | 7 | session bootstrap 8 + new-role discovery + 1 verify |
| `PC-FOREKNOWN-SCHEMA` | 8 | 10 | 12 | 14 | `h+8` |
| `B-COLD-RE-DERIVE` on `CC-DEGENERATE` | 8 | 10 | 12 | 14 | `h+8` |
| `B-RETRIEVAL-SHAPED` on `CC-DEGENERATE` (total) | 9 | 11 | 13 | 15 | `h+9` |

`T-AMORT-REUSE` pays the 8-request session bootstrap once (charged to the warm-up task), then 3 requests for each newly introduced role (roles are nested: 2 new roles per escalating level ⇒ 6 discovery requests) plus 1 verify = 7 thereafter; session total 30.

## 6. Arithmetic certificate (computed in DESIGN; non-outcome-bearing)

Computed by a DESIGN stdlib probe (`python 3.12.15`); no arm was run and no success was measured.

Predicted certificate object (canonical form, `json.dumps(sort_keys=True, separators=(",",":"))`):

```json
{"ADB-v6":{"certificate":true,"cold":{"0.0":8,"0.25":14,"0.5":20,"0.75":26},"gap_vs_treatment":{"cold":[-1,7,13,19],"retrieval":[0,8,14,20]},"pc":{"0.0":8,"0.25":10,"0.5":12,"0.75":14},"retrieval_http":{"0.0":6,"0.25":12,"0.5":18,"0.75":24},"retrieval_total":{"0.0":9,"0.25":15,"0.5":21,"0.75":27},"success":{"cold":[true,true,false,false],"pc":[true,true,true,true],"retrieval":[true,true,false,false],"treatment":[true,true,true,true]},"treatment":{"0.0":9,"0.25":7,"0.5":7,"0.75":7}},"CC-DEGENERATE":{"certificate":false,"cold":{"0.0":8,"0.25":10,"0.5":12,"0.75":14},"retrieval_http":{"0.0":6,"0.25":8,"0.5":10,"0.75":12},"retrieval_total":{"0.0":9,"0.25":11,"0.5":13,"0.75":15},"success":{"cold":[true,true,true,true],"retrieval":[true,true,true,true]}}}
```

**Certificate predicate** `CERT(cls)` = `TRUE` iff (a) every strong baseline's predicted **minimum total cost at high novelty** (`n ≥ 0.5`) strictly exceeds `B(n)`; (b) the treatment's predicted maximum per-task cost ≤ `B(n)` at every level; (c) the positive control's predicted per-task cost ≤ `B(n)` at every level.

- `CERT(ADB-v6) = TRUE`: cold 20>16, 26>18 and retrieval_total 21>16, 27>18; treatment 9,7,7,7 ≤ B; PC 8,10,12,14 ≤ B.
- `CERT(CC-DEGENERATE) = FALSE`: cold 12≤15, 14≤17 (comparators not below ceiling), retrieval_total 13≤15, 15≤17.

**Wilson 95% intervals (n=12, z=1.959963984540054):** k=0 → point 0.0, [0.0, 0.242494]; k=6 → 0.5, [0.253782, 0.746218]; k=7 → 0.583333, [0.319511, 0.806740]; k=12 → 1.0, [0.757506, 1.0]. Boundary: comparator k ≤ 6 gives interval disjoint below treatment k=12 (0.746218 < 0.757506); k ≥ 7 overlaps.

**Informational hypothesis digests (non-binding cross-check; gate I6 is structural equality, not digest equality):**

- D1 (declaration) = `81280bcc13b55a2fac30a36b9a0e9e16bbccb459661eddeece53a90b66d66fcb`
- D2 (predicted certificate) = `95b4e47e3764cc87fb6493cd7d8934c16b0bc2c42def5c1777c0877e5191a87f`

## 7. Controls

- **`PC-FOREKNOWN-SCHEMA`** (positive control, solvability ceiling): given manifest, role registry and resolved tokens out of band; walks bootstrap (7) + one commit per role (`h`) + `/verify` (1) = `h+8 = {8,10,12,14}` ≤ `B(n)`. Required 24/24 (12/12 high novelty). Excluded from the gap computation.
- **`NC-OOS-SCHEMA`** (known-negative refusal null): 5 frozen out-of-support sessions (non-ascending sequence or non-nested registry) must be refused `OUT_OF_SUPPORT` within ≤2 requests; false accepts 0/5.
- **`CC-DEGENERATE`** (certificate-sensitivity calibration): both comparators must reach the ceiling on the query-answerable sibling; this is the observational counterpart of `CERT(CC-DEGENERATE)=FALSE`.
- **`NC-BUDGET-TRUNCATION`**: 6 deliberately under-funded episodes must stop at the imposed budget with zero overrun.
- **`M-COUNTER-RECONCILE`**: per-episode arm counters == server request log; subset relations hold; 0 mismatches.
- **`M-REPAIR-TRANSIENT`**: one injected transient fault per episode ⇒ `repair_attempts = 1` (charged to `http_requests`) or an honest failure; no hidden retries.
- **`PC-EXACT-SESSION-REPLAY`**: 6 replayed treatment sessions reproduce per-route counter vectors exactly.

## 8. Decision rule

**Frozen thresholds:** success ceiling point 0.95; high-novelty threshold 0.5; n_high = n_low = 12; treatment high-novelty k required = 12 (Wilson lo 0.757506 ≥ 0.75); interval disjointness = comparator Wilson hi < treatment Wilson lo; minimum high-novelty mean gap ≥ 8 requests; CC-DEGENERATE comparator high-novelty point ≥ 0.95; counter mismatches = 0; OOS false accepts = 0; budget overruns = 0; repair attempts ≤ 1/task.

**Integrity gates I1–I11:**

- **I1** `PC-FOREKNOWN-SCHEMA` 24/24 overall, 12/12 high novelty.
- **I2** `NC-OOS-SCHEMA` false accepts 0/5, all refusals at manifest classification.
- **I3** `NC-BUDGET-TRUNCATION` 6/6 stop at budget, zero overrun.
- **I4** `M-COUNTER-RECONCILE` 0 mismatches (all four mandate counters reconcile; subset relations hold).
- **I5** `PC-EXACT-SESSION-REPLAY` exact per-route vectors on 6 replays.
- **I6** Render equality: rendered canonical declaration == section 5; recomputed certificate == section 6.
- **I7** Route-token leak absent on every rendered page; sitemap lists only `/`, `/hub`, `/about`.
- **I8** Determinism: repeated episode → byte-identical counters.
- **I9** Treatment session-schema & low-novelty liveness abort gate.
- **I10** Contamination gate: per-arm server isolation; retrieval index leave-instance-out; route-trace signatures overlap only on declared navigational routes.
- **I11** Certificate-sensitivity calibration: both `CC-DEGENERATE` comparators reach the ceiling (point ≥ 0.95).

**Propositions P1–P7:**

- **P1** cold high-novelty point < 0.95 and Wilson hi < treatment lo (predicted k=0/12, hi 0.242494).
- **P2** retrieval high-novelty point < 0.95 and Wilson hi < treatment lo (predicted k=0/12).
- **P3** treatment succeeds 12/12 high novelty (lo 0.757506 ≥ 0.75) and 12/12 low novelty.
- **P4** observed mean comparator-minus-treatment total gap is non-decreasing across n and strictly increasing across 0.5<0.75 for both comparators.
- **P5** minimum observed high-novelty mean gap ≥ 8 requests (predicted 13 cold / 14 retrieval).
- **P6** observed 4-arm × 4-level ADB-v6 success matrix and per-condition ledger equal the prediction.
- **P7** certificate discrimination: `CERT(ADB-v6)=TRUE`, `CERT(CC-DEGENERATE)=FALSE`, confirmed observationally by I11.

**Result mapping (ordered, total, disjoint partition):** (0) if bring-up/site-bind/transport/digest infrastructure fails so a gate cannot be evaluated ⇒ `INCONCLUSIVE` (never a gate `MEASUREMENT_INVALID`, never a scientific negative); (1) otherwise evaluate I1–I11 — any evaluable gate that FAILED ⇒ `status=MEASUREMENT_INVALID`; (2) with the integrity set holding, `SUPPORTS` iff P1..P7; else `FALSIFIES` iff `NOT(P1 AND P2)`; else `MIXED`. Failure of the certificate to discriminate (`NOT P7`) is `MIXED` (bounded negative about the certificate/cost model) unless I11 itself fails, which is `MEASUREMENT_INVALID`.

**Consequences of both outcomes:**

- `SUPPORTS` ⇒ a reusable, hash-recordable bank with certified comparator headroom under the declared policies and a demonstrated-discriminating certificate; blocker B2 partially retired (readiness condition 2), no product promotion, no Web-transfer claim.
- `FALSIFIES` ⇒ the session-amortized asymmetric construction does not create certified headroom on the credential-free localhost class; the program must not fund the four-arm benchmark on this bank class and should change the discovery asymmetry or wait for readiness condition 3 (real-agent-capable substrate).
- `MIXED` ⇒ headroom retained but cost model / gap trend / certificate calibration must be corrected before reuse.
- `MEASUREMENT_INVALID` ⇒ instrument repaired before any downstream spend; **never** reported as a scientific negative.
- If the certificate is unsatisfiable on every credential-free class tested, DESIGN records a bounded substrate-class negative and does **not** freeze.

## 9. Sampling, matching and counter honesty

Tasks are matched across arms (same 24 ADB-v6 tasks; same 4 CC-DEGENERATE tasks). No arm is charged a cost it does not pay: stateless arms pay per-task bootstrap and the full 3-step chain per role; retrieval additionally pays its 3 index probes (counted as `retrieval_calls`, not omitted and not summed into `http_requests`); the treatment pays its single session bootstrap and discovery only for roles it has never resolved. Per-episode frozen ledger predicate: `arm_reported_http_requests == server_logged_requests` AND `bootstrap_requests + discovery_calls + verification_calls ≤ http_requests` AND `retrieval_calls` and `repair_attempts` recorded independently of `http_requests`. `latency_ms` and model tokens are prohibited as decision inputs.

## 10. EXECUTE procedure and abort gates

1. **Bring-up**: site binds `127.0.0.1:ephemeral`; render the canonical declaration and certificate; run I6 (structural equality) and I7 (route-leak scan) before any arm.
2. **Prerequisite probe**: re-confirm stdlib imports and the localhost canary (same as DESIGN section 12).
3. **Low-novelty block first**: run treatment (and controls) at n<0.5 as the post-freeze liveness abort gate (I9). Failure ⇒ `MEASUREMENT_INVALID`.
4. **ADB-v6 matrix**: run all arms (cold, retrieval, treatment, PC) over the 24 tasks; compute per-arm per-level success and ledgers.
5. **CC-DEGENERATE calibration**: run both comparators on the 4-task sibling; check I11.
6. **Controls**: OOS refusals (I2), budget truncation (I3), counter reconcile (I4), session replay (I5), determinism (I8), contamination (I10), transient repair (M-REPAIR-TRANSIENT).
7. **Recompute**: recompute the certificate from the rendered declaration; evaluate P1–P7 and the result mapping; write `result.json`, `report.md`, `provenance.json` and the produced substrate files (`research/runtime/adb_v6_bank.py`, `research/runtime/adb_v6_harness.py`, `research/experiments/EXP-RUNTIME-38087588064/bank_manifest.json`) with sha256 in `provenance.json`/`result.json.artifacts`.
8. Any bring-up/transport/digest failure is recorded with the exact error and mapped to `MEASUREMENT_INVALID`/`INCONCLUSIVE`; never silently substituted, never encoded as a scientific negative.

## 11. Validity threats and scope bounds

1. **Memory-asymmetry caveat (readiness condition 3)**: the asymmetry is a within-session memory asymmetry under declared policies. A real memory-carrying LLM agent might persist resolved roles and erase it; this instrument does not certify against such an agent. Declared limitation, not hidden.
2. **Comparator coincidence**: retrieval saves only the fixed 2-request root/hub prefix over cold, so both comparators coincide at stratum-success level and jointly bracket the ceiling rather than testing independent mechanisms. Their ledgers differ (retrieval pays 3 index probes, 1 fewer server request).
3. **Synthetic substrate**: no third-party site exhibits exactly this structure; external validity is not claimed.
4. **Declaration-fidelity risk**: SUPPORTS is largely the declaration taking effect; the residual empirical content is implementation divergence, leakage, dishonesty, out-of-support false acceptance, contamination, and the certificate-sensitivity prediction (I11/P7). This is disclosed honestly.
5. **Certificate sensitivity is constructed, not naturalistic**: `CC-DEGENERATE` is deliberately query-answerable. Its role is to prove the certificate is non-vacuous, encoding the mandate's "unsatisfiable on every credential-free substrate tested" branch; it is not independent external evidence.
6. **Descriptive intervals, not sampling inference**: the 24-task bank is a deterministic finite population, not a random sample. The Wilson intervals are a frozen, pre-declared separation criterion over fixed matched tasks, not sampling-based confidence intervals; no population-level claim is made.
7. **Shared discovery templates are expected**: cold and retrieval necessarily share `/disc/<role>/1..3` route templates. The contamination gate I10 compares instance-scoped content (session ids, nonces, partial/resolved tokens, per-session payloads), not those shared templates. The rendered bank instance is additionally hash-recorded via `bank_manifest.json` so an altered bank cannot pass unnoticed.

## 12. DESIGN-phase probes (non-outcome-bearing)

- `python 3.12.15`; stdlib import probe: `http.server, urllib.request, html.parser, json, hashlib, random, statistics, socket, threading` — all import (9/9).
- localhost `ThreadingHTTPServer` canary on `127.0.0.1:ephemeral` returned HTTP 200 (`b"ok"`), confirming transport.
- The arithmetic certificate and its calibration were computed with `json`/`statistics` only; **no arm was run and no success/failure outcome was observed**.

## 13. Pre-2.0 comparison and material difference

Screened against `codex/legacy_brief.json`: no pre-2.0 asymmetric-discovery / certified-dynamic-range task-bank precedent exists (`LEGACY: NO_MATCH` for the bank construction). Nearest legacy lesson `P2-REPLAY-COST` (source sha `9687ff787f2d74460bb7006826008852f5b4416b`: the withdrawn 8.5× claim rested on matched tasks with fully loaded counterfactuals) is applied as a guard: tasks are matched across arms, every arm pays fully loaded costs including retrieval probes and repair charges, and no scripted-replay economics is claimed.

`LEGACY: DISTINCT_EXTENSION`. Material differences from prior work on the same mandate:

- vs **ADB-v5** (`EXP-RUNTIME-38085184570`): ADB-v6 adds the `CC-DEGENERATE` same-transport calibration class, the certificate-sensitivity proposition P7 and gate I11, so the certificate's non-vacuity is an observable prediction rather than a design assertion. The core asymmetric arithmetic is preserved because it was already consistent.
- vs **ADB-v1** (`EXP-RUNTIME-38051419597`): the strategy-dependent discovery policy ("try both candidates") is removed; the fixed carry chain makes per-role cost strategy-invariant.
- vs **the degenerate mandatory-discovery REST class** (`EXP-PRODUCT-37989728440`, `EXP-PRODUCT-37973256064`, measured 1.0/1.0): ADB-v6 is preserved as a **negative-control precedent** and instantiated in spirit as `CC-DEGENERATE`; ADB-v6 proper is designed to be non-degenerate.

## 14. Deliverable artifacts

- `research/experiments/EXP-RUNTIME-38087588064/{result.json,report.md,provenance.json}`
- reusable substrate: `research/runtime/adb_v6_bank.py`, `research/runtime/adb_v6_harness.py` (Runtime lane authorized code root) and `research/experiments/EXP-RUNTIME-38087588064/bank_manifest.json`, each hashed into `provenance.json`/`result.json.artifacts`. `bank_manifest.json` carries a canonical digest of the fully-rendered bank instance (ordered role registry, role→token mapping, task payloads, route strings), extending gate I6 beyond the topology object.

## 15. Freeze eligibility

All six v2 checks are `PASS` except `freeze_artifacts_bound`, which is justified `NOT_APPLICABLE` with an empty `freeze_artifacts` list (no pre-existing mutable local dependency is consumed; the substrate is a deterministic function of the declaration embedded in this prereg and in `spec.json`, materialized at EXECUTE inside the transaction and pinned by gate I6). See `spec.json#freeze_eligibility`. This prereg and `spec.json` are not frozen until the deterministic freezer writes `freeze.json` after an independent `design_review.json` `PASS`.
