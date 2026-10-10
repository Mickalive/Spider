# EXP-RUNTIME-38072217499 preregistration (Runtime lane)

**Status:** DESIGN (pre-freeze, design-contract v2). This file plus `spec.json` is the
complete frozen interpretation surface for EXECUTE. No outcome-bearing measurement has been
run. DESIGN-phase probes (section 15) are cheap, non-outcome-bearing satisfiability checks.

**Lane:** runtime. **Claim:** `C-MEAS-VALID` ("Measurement substrate is intervention-valid";
owner lanes runtime/physics; next gate "writable/auth/session/drift controls must produce
discriminating positive and null outcomes"). **Director mandate:** `request.json`
`director_mandate.allocation` action `CONTINUE`, claim `C-MEAS-VALID`, cognitive reset true,
`parent_handoff_disposition = SUPERSEDE`.

---

## 1. Director mandate (binding research direction)

The Global Research Director's question (verbatim intent) is:

> Can a non-degenerate asymmetric-discovery task bank be certified arithmetically BEFORE
> freeze -- cold and retrieval-shaped comparators demonstrably below ceiling at high residual
> novelty, a real treatment/comparator behavioural distinction, honest per-condition counters
> (`http_requests + retrieval_calls + verification_calls + repair_attempts`), and a
> preregistered contamination/dynamic-range certificate -- and be delivered as a reusable
> substrate on the lane and/or shipped path that unblocks the flagship inheritance benchmark
> (blocker B2)?

The mandate explicitly **forbids** a further re-run of the deterministic mandatory-discovery
REST certificate (the construction already excluded after `EXP-PRODUCT-37989728440`), and asks
this DESIGN either to **certify dynamic range or fail loudly**.

## 2. Why this is a materially new construction (not a repeat)

- The excluded construction (`EXP-PRODUCT-37989728440`, and the sibling
  `EXP-PRODUCT-37982016598`) had **symmetric mandatory discovery**: every arm had to issue the
  same `GET /api/session` / `GET /api/resources` / `GET /api/schema` calls before acting, so
  both comparators sat at the correctness ceiling and no cost gap could exist.
- **ADB-v4 changes the discovery structure**: discovery is *asymmetric* — a session-scoped,
  carry-chained role-resolution layer whose 3-step protocol cannot be shortened by any policy,
  and whose resolved role tokens can be persisted across the multiple tasks of one session
  only by a stateful mechanism.
- ADB-v4 is materially different from the rejected `EXP-RUNTIME-38066025505` (ADB-v3), which
  the design review returned `substantive` (openrouteservice/exo-free exit 1). ADB-v4 fixes the
  two disclosed ADB-v3 defects:
  1. **No strawman comparator.** ADB-v3 used a `GET /try/<candidate>` fetch-and-commit
     primitive and declared the stateless arms as "try both candidates per role (2h)". That is a
     policy artifact: a rational stateless arm could stop after the first acceptance. ADB-v4
     replaces it with a fixed 3-step carry chain (`/disc/<role>/1,2,3`) in which each step
     requires the previous step's value and the chain is role-specific, so the per-role cost is
     **strategy-invariant** (exactly 3 for every non-persisting arm) and the only way to pay
     less is the declared treatment capability (cross-task persistence).
  2. **No load-bearing session ordering.** ADB-v3's treatment liveness depended on a first task
     at `n=0` and would blow budget if reordered. ADB-v4 makes the ascending warm-up sequence a
     declared structural property of every session, has the treatment **validate and refuse**
     (never overspend) on any non-conforming session, and keeps per-task costs (`9,8,8,8`)
     within `B(n)` under the declared schema regardless of family/session instance.
- ADB-v4 also differs from the two earlier unfinished Runtime drafts under this mandate
  (`EXP-RUNTIME-38051419597` ADB-v1 and `EXP-RUNTIME-38054047834` ADB-v2), which used an
  ambiguous "schema revealed at the end of the boot chain" + "decoy slot" framing.
- No identical invalid/degenerate design is repeated; the excluded mandatory-discovery
  deterministic REST certificate is **not** re-run.

## 3. Inherited state preserved (request `parent_handoff` = `EXP-RUNTIME-37973247935`, SUPERSEDED)

- **established (inherited, unchanged):** the parent `C-MEAS-VALID` ceiling is a bounded
  authorship-separated real-Chromium fixture; the composite oracle's discriminator was
  measurement-invalid on the parent (fingerprint component fired on 260/260 episodes including
  120 matched nulls).
- **rejected (inherited, unchanged):** no claim change follows from the parent.
- **unknown (inherited):** whether the repaired composite oracle retains out-of-surface
  arm-constrained discrimination — **not tested here**; this experiment does not touch the
  fingerprint/`Connection`-header thread.
- **do_not_assume (inherited):** do not read an absent/failed measurement as a scientific
  negative; do not treat the parent's `MEASUREMENT_INVALID` as closing the transfer question.
- The mandate's `SUPERSEDE` is honoured: this design pivots away from the oracle micro-thread to
  the dynamic-range gate that blocks the flagship chain. Product's accepted bounded negative
  (`EXP-PRODUCT-37989728440`: certificate unsatisfiable on the mandatory-discovery
  deterministic credential-free REST class) is the need this experiment answers.

## 4. Substrate declaration ADB-v4

Credential-free, deterministic, locally-served multi-page REST bank. Python 3.12 stdlib only
(`http.server.ThreadingHTTPServer`, `urllib.request`, `html.parser`, `json`, `hashlib`,
`random`, `statistics`); no browser, no network egress, no credentials, no cookies, no model
calls. Transport is `http://127.0.0.1:<ephemeral>`; the port is **not** part of the frozen
identity (declared `ephemeral-not-frozen`).

Site topology (deterministic, seed `20261010`):

- `GET /` (1) — links to `/hub` and `/sitemap.xml`.
- `GET /sitemap.xml` — lists only `/`, `/hub`, `/about` (site-native enumeration channel; it
  MUST NOT list `/boot/*`, `/tasks`, `/disc/*`, `/verify`, or any session id).
- `GET /hub` (1) — session classifier; links to `/boot/1`.
- `GET /boot/1 .. /boot/5` (5) — **carry-chained**; each page requires the carry returned by
  its predecessor, and `/boot/5` returns the session manifest: session id, the ordered role
  registry `R1..R6`, the frozen ascending task sequence `['0.0','0.25','0.5','0.75']`, and
  (for a multi-task session) links to `/tasks`. Because the chain is carry-bound, the bootstrap
  cannot be shortened below 7 (root, hub, boot1..5).
- `GET /tasks` (1) — ordered task list (levels 0.0, 0.25, 0.5, 0.75) plus the first task spec.
- `GET /disc/<role>/1` — returns a per-role session nonce `N_r`.
- `GET /disc/<role>/2/<N_r>` — returns a partial token `P_r` iff `N_r` is the session-valid
  nonce.
- `GET /disc/<role>/3/<P_r>` — returns the resolved token `T_r` and commits role `r` for the
  session iff `P_r` is valid. The chain is role-specific (mixes the role id with the session
  secret) so it cannot be shared across roles within a task.
- `GET /verify` (1) — confirms the committed state of the current task.

**Role rule.** `h(n) = 8n` hidden roles; level `n` uses the first `h(n)` roles of the registry:
`h(0)=0, h(0.25)=2, h(0.5)=4, h(0.75)=6`. Roles are **nested** (level `n` extends level
`n'<n`), so a role token resolved at one level is reusable at later levels of the same session.

**Bank.** `F = 2` families (`F1`,`F2`), `3` test sessions per family, `4` tasks per session
(one per level, fixed ascending) = **24 test tasks per arm**; high-novelty (`n>=0.5`) =
**12 per arm**; low-novelty (`n<0.5`) = **12 per arm**. PC-FOREKNOWN-SCHEMA is the fourth
matrix arm and runs on **all 24 tasks** (so the full 4-arm x 4-level matrix is measured and P6
is evaluable). Plus: 6 replay sessions, 5 out-of-family null sessions, 6 budget-truncation
episodes, 6 transient-repair episodes.

**Route-leak rule.** Every rendered spec/disc/hub/boot/task page MUST contain no absolute URL
and none of the literals `/s/`, `{sid}`, `/boot/`, `/hub`, `/tasks`, `/disc/`, `/verify`, or
the session id; only the arm's own navigational relative links are permitted. Checked
statically in DESIGN and re-checked at EXECUTE (gate I7).

## 5. Cost model and static traces

The exact per-task request ledger (all arms, identical budget `B(n)`):

| component | B-COLD-RE-DERIVE | B-RETRIEVAL-SHAPED | T-AMORT-REUSE (task k) | PC-FOREKNOWN-SCHEMA |
|---|---|---|---|---|
| bootstrap | 7 (root,hub,boot1..5; manifest at boot5) | 5 (boot1..5; index supplies root,hub) | 1x per session (7) | 7 (root,hub,boot1..5) |
| `/tasks` + first spec | — | — | +2 on task 1 | — |
| per-task spec fetch | — | — | 1 on tasks 2..4 | — |
| role discovery (`/disc` 3 steps) | `3h` (full chain per role) | `3h` (full chain per role) | `new_roles*3` = 0,6,6,6 | `h` (one commit per role, tokens known) |
| retrieval index (local probes) | 0 | 3 | 0 | 0 |
| `/verify` | 1 | 1 | 1 | 1 |
| **server cost** | `3h+8` | `3h+6` | `[9,8,8,8]` (session total 33) | `h+8` |
| **total arm cost** (incl. local probes) | `3h+8` | `3h+9` | `[9,8,8,8]` | `h+8` |

Costs by level `n` = 0 / 0.25 / 0.5 / 0.75:

- `B-COLD-RE-DERIVE` = 8, 14, 20, 26
- `B-RETRIEVAL-SHAPED` server = 6, 12, 18, 24; total = 9, 15, 21, 27
- `T-AMORT-REUSE` = 9, 8, 8, 8 (bootstrap + session-open charged to warm-up task 1)
- `PC-FOREKNOWN-SCHEMA` = 8, 10, 12, 14
- budgets `B(n)` = **10, 15, 16, 18**

Success = every required role committed and `/verify` confirms, within `B(n)`. Predicted
success matrix: cold `T,T,F,F`; retrieval `T,T,F,F`; treatment `T,T,T,T`; PC `T,T,T,T`.
Comparator-minus-treatment per-task gaps: cold `-1,6,12,18`; retrieval `0,7,13,19` (both
non-decreasing across levels and strictly increasing across the high-novelty levels; minimum
high-novelty gaps 12 and 13).

**Behavioural distinction (route traces).** Cold and retrieval walk the carried boot chain on
every task and issue all 3 discovery steps per role; the treatment walks the boot chain once
per session, issues `/tasks` once per session, has `discovery_calls = 0,6,6,6` (zero on
already-resolved roles), and reuses role tokens. Retrieval alone issues 3 local index probes
per task. The positive control skips the discovery chain (tokens known) and the null refuses at
`/hub` with no commit and no `/verify`. These signatures are disjoint by construction apart from
the declared shared navigational routes (gate I10).

**Static non-degeneracy argument.** Budgets are non-decreasing and do not shrink with novelty
(they are lenient toward comparators). Cold fails at `n>=0.5` because its per-task cost grows at
`3h` while the budget grows slower; the treatment succeeds because it pays the bootstrap once
per session and pays discovery only for never-seen roles. The failure is not a floor effect:
both comparators succeed at `n<0.5`, so the instrument has genuine dynamic range.

## 6. Arithmetic certificate CERT-ADB-DYNAMIC-RANGE

Computed in DESIGN by pure arithmetic on the frozen declaration (probe 2 recomputed it
independently). No outcomes used.

**Declared prediction.** high-novelty (`n=12`) success counts: cold `k=0/12`, retrieval
`k=0/12`, treatment `k=12/12`, PC `k=12/12`. Wilson 95% two-sided (`z=1.959963984540054`):
`k=0` → point 0.0, lo 0.0, hi 0.242494; `k=12` → point 1.0, lo 0.757506, hi 1.0. The
comparator accept region (point < 0.95 AND Wilson lo < 0.90) is satisfied for `k<=11` and
violated only at `k=12`; it is non-empty.

**Canonicalization (frozen; repeated at EXECUTE for I6).** `canonical(obj) =
json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=True)`, encoded UTF-8;
digest = `sha256(canonical(obj)).hexdigest()`.

**Render-declaration digest D1.** The declaration object is:

```json
{"arms":["B-COLD-RE-DERIVE","B-RETRIEVAL-SHAPED","T-AMORT-REUSE","PC-FOREKNOWN-SCHEMA"],"budgets":{"0.0":10,"0.25":15,"0.5":16,"0.75":18},"discovery_chain_length":3,"families":["F1","F2"],"h":{"0.0":0,"0.25":2,"0.5":4,"0.75":6},"h_rule":"h(n)=8n","ledger":{"BOOT_CHAIN":5,"BOOTSTRAP_COLD":7,"BOOTSTRAP_RETRIEVAL":5,"DISCOVERY_PER_ROLE":3,"INDEX_PROBES":3,"SESSION_OPEN":1,"TREATMENT_DISCOVERY_RULE":"new_roles*3","TREATMENT_SPEC_FETCH":1,"VERIFY":1},"levels":[0.0,0.25,0.5,0.75],"name":"ADB-v4","seed":20261010,"session_task_order":["0.0","0.25","0.5","0.75"],"sessions_per_family":3,"tasks_per_session":4,"version":4}
```

`D1 = cc146763642147f391e410bd8c46806386c1333ff9c5fd1aaf9e6ce37696b028`

**Predicted-certificate digest D2.** The certificate object is:

```json
{"gaps_vs_treatment":{"B-COLD-RE-DERIVE":[-1,6,12,18],"B-RETRIEVAL-SHAPED":[0,7,13,19]},"min_high_gap":{"B-COLD-RE-DERIVE":12,"B-RETRIEVAL-SHAPED":13},"n_high":12,"n_low":12,"predicted_costs":{"B-COLD-RE-DERIVE":[8,14,20,26],"B-RETRIEVAL-SHAPED_http":[6,12,18,24],"B-RETRIEVAL-SHAPED_total":[9,15,21,27],"PC-FOREKNOWN-SCHEMA":[8,10,12,14],"T-AMORT-REUSE":[9,8,8,8]},"predicted_high_k":{"B-COLD-RE-DERIVE":0,"B-RETRIEVAL-SHAPED":0,"PC-FOREKNOWN-SCHEMA":12,"T-AMORT-REUSE":12},"predicted_success":{"B-COLD-RE-DERIVE":[true,true,false,false],"B-RETRIEVAL-SHAPED":[true,true,false,false],"PC-FOREKNOWN-SCHEMA":[true,true,true,true],"T-AMORT-REUSE":[true,true,true,true]},"wilson":{"k0_n12":{"hi":0.242494,"lo":0.0,"point":0.0},"k12_n12":{"hi":1.0,"lo":0.757506,"point":1.0}}}
```

`D2 = 5e4424a10dec21a585c169b2568348a2490c562007b7e512144310805b4f38a9`

EXECUTE must reproduce `D1` and `D2` byte-for-byte (gate I6). A mismatch is a
MEASUREMENT_INVALID instrument failure, not a scientific negative.

## 7. Controls

- **PC-FOREKNOWN-SCHEMA** (positive; solvability ceiling): given the manifest and resolved role
  tokens out of band, cost `h+8`; must succeed 24/24 across all levels (the 12/12 high-novelty
  stratum is the accept region; the 12 low cells are solvability sanity cells). Excluded from the
  gap computation.
- **NC-OOS-FAMILY** (null; out-of-support): 5 frozen out-of-family sessions; the treatment must
  refuse with reason `OUT_OF_SUPPORT` at `/hub` (<=2 requests), `false_accept = 0/5`.
- **NC-BUDGET-TRUNCATION** (negative): 6 episodes with the budget forced below the required
  cost; each must stop at the imposed budget with zero overrun and a recorded failure state.
- **NC-REPAIR-TRANSIENT** (repair-counter liveness): 6 episodes with one injected transient 503
  on a designated role's first discovery step; the arm must either repair (`repair_attempts=1`,
  charged to `http_requests`) and succeed, or honestly fail with `repair_attempts<=1` and no
  hidden retry. Makes the `repair_attempts` counter non-trivially observable.
- **PC-EXACT-SESSION-REPLAY** (independent replay): 6 treatment test sessions re-run; their
  per-route counter vectors must be identical.
- **M-COUNTER-RECONCILE** (honesty): every arm-reported counter must reconcile exactly to the
  site request log, with the declared subset relations (`bootstrap_requests + discovery_calls +
  verification_calls <= http_requests`).

## 8. Decision rule

Frozen thresholds: ceiling point 0.95; ceiling Wilson lo 0.90; high-novelty threshold 0.5;
`n_high = n_low = 12`; minimum high-novelty gap 8 requests; counter mismatches 0; OOS false
accepts 0; budget overruns 0; repair attempts <= 1 per task.

Integrity gates **I1..I10** (spec.json#decision_rule.integrity_gates) are evaluated first; any
failure → `MEASUREMENT_INVALID`. I9 is the treatment session-schema guard plus the low-novelty
liveness **abort gate** (the treatment must resolve every `n<0.5` task within `B(n)` and must
refuse rather than overspend on a non-conforming session), so it is an instrument gate, not a
scientific proposition. I10 is the contamination gate. Then:

- **P1** cold high-novelty point < 0.95 AND Wilson lo < 0.90 (predicted `k=0/12`).
- **P2** retrieval high-novelty point < 0.95 AND Wilson lo < 0.90 (predicted `k=0/12`).
- **P3** treatment succeeds 12/12 high AND 12/12 low, every per-task cost <= `B(n)`.
- **P4** per-task comparator-minus-treatment mean gap is non-decreasing across levels for BOTH
  comparators AND strictly increasing across the two high-novelty levels (0.5 < 0.75).
- **P5** minimum high-novelty per-task mean gap >= 8.
- **P6** observed 4x4 success matrix == predicted and observed ledger == predicted (D2).

Mapping: **SUPPORTS** iff I1..I10 and P1..P6; else **FALSIFIES** iff `NOT(P1 AND P2)`; else
**MIXED** = `P1 AND P2 AND NOT(P1 AND P2 AND P3 AND P4 AND P5 AND P6)`. `MEASUREMENT_INVALID`
for any I1..I10 failure. A treatment failure at low novelty (`n<0.5`) or a non-conforming
session is gate I9 → instrument failure; a treatment failure only at `n>=0.5` is a scientific
P3 failure and maps to MIXED. `INCONCLUSIVE` for bring-up / bind / transport failure.
SUPPORTS, FALSIFIES and MIXED are disjoint and cover every integrity-passing case: the
partition is total.

**Reachability of the negative branches (pre-freeze, no outcomes).** *FALSIFIES* is reachable
under an integrity-passing render via any realisation that lets a comparator fit `B(n)` at high
novelty without tripping a gate: the retrieval index realising a saving larger than the declared
2 bootstrap requests (its total is `3h+9`; if an un-gated realisation lets the constant fall to
`<=4`, then at `h=4` cost `16` fits `B(0.5)=16`), or a bootstrap cheaper than the declared
`3h+8` (a saving of `>=4` lets cold fit `B(0.5)=16`). Neither saving is integrity-gated — a
route-token leak is gate I7 and maps to `MEASUREMENT_INVALID`, not to FALSIFIES. *MIXED* is
reachable via a cost-model-only divergence that preserves P1/P2/P3 but breaks P6/P4/P5.
*MEASUREMENT_INVALID* is reachable via any I1..I10 failure. Under a byte-faithful render
SUPPORTS is expected by construction; that is the honest nature of a certification experiment —
the empirical content is the verification that the render matches the declaration.

## 9. Metrics (stable identities for AUDIT)

The four mandate counters, used verbatim as stable metric identities:

- `M-HTTP-REQUESTS` (counter `http_requests`): server-logged total HTTP requests.
- `M-RETRIEVAL-CALLS` (counter `retrieval_calls`): local index queries (0 cold/treatment; 3/task
  retrieval).
- `M-VERIFICATION-CALLS` (counter `verification_calls`): `/verify` calls (1/task).
- `M-REPAIR-ATTEMPTS` (counter `repair_attempts`): recovery actions (<=1/task).

Supporting measurements: `M-HIGH-POINT` (comparator high-novelty success proportion),
`M-HIGH-WILSON-LO` (two-sided 95% lower bound, n=12), `M-GAP-PER-LEVEL` (comparator minus
treatment per-task request cost, per level), `M-MIN-HIGH-GAP`, `M-LEDGER` (per-route request
counts), `M-RECONCILE-DELTA` (arm counter minus site log). Decision inputs are deterministic
HTTP-request counters (plus the local retrieval-call counter) only; `latency_ms` and model
calls/tokens are recorded but **prohibited** as decision inputs.

## 10. EXECUTE procedure and abort gates

1. Materialise the generator + site + harness from this frozen declaration; recompute D1/D2
   (gate I6) before any arm runs.
2. Run the **low-novelty block FIRST** as the post-freeze liveness abort gate **I9**: the
   treatment must succeed at `n=0` and `n=0.25` with its per-task cost within `B(n)`, and must
   refuse (not overspend) on any session whose declared sequence is not the frozen ascending
   warm-up; failure aborts to MEASUREMENT_INVALID.
3. Run PC-FOREKNOWN-SCHEMA first among controls (I1) to prove solvability, then the full
   4-arm x 4-level matrix, then NC-OOS-FAMILY (I2), NC-BUDGET-TRUNCATION (I3),
   NC-REPAIR-TRANSIENT, PC-EXACT-SESSION-REPLAY (I5), counter reconciliation (I4), route-leak
   scan (I7), contamination checks (I10) and determinism re-run (I8).
4. Preserve raw evidence (`raw_evidence/` trajectories + server request logs) separately from
   derived measurements (`derived/`) and interpretation.

## 11. Validity threats (disclosed)

1. **Synthetic substrate.** The bank is authored, not sampled from the Web; it certifies the
   *instrument*, not transfer to the open Web or to a real LLM agent.
2. **Declared policies / memory asymmetry.** The declared asymmetry between the arms is a
   within-session *memory* asymmetry, stated openly: the discovery protocol is a fixed 3-step
   carry chain whose steps each require the previous step's value, so the per-role cost is
   strategy-invariant (3) and the only way to pay less per task is to persist a role token
   across tasks — the declared treatment capability. The comparators are otherwise deliberately
   strong (shortest bootstrap, full site-native enumeration, a real 3-probe leave-instance-out
   index that saves only the 2-request root/hub prefix). This experiment certifies the
   instrument under exactly these declared policies and explicitly does **not** claim a
   memory-carrying LLM agent is bounded by them; that is readiness condition (3) and the
   downstream four-arm question.
3. **Within-session persistence is the treatment's claimed mechanism.** A retrieval policy that
   also persists within a session would blur into the treatment; it is out of scope by
   construction and is exactly the downstream four-arm question.
4. **Tautology risk.** Because the certificate is arithmetic, SUPPORTS is largely the
   declaration taking effect under a byte-faithful render; the genuinely falsifiable content is
   implementation divergence, index/bootstrap realisation larger or cheaper than declared,
   leakage, dishonesty, contamination and behavioural divergence (MIXED/FALSIFIES/
   MEASUREMENT_INVALID). This is disclosed openly; section 8 states the concrete reachable
   negative branches. The experiment must not be read as if SUPPORTS were an independent
   corroboration of the arithmetic.
5. **Harness-authored ground truth.** The site is the request-log authority; authorship
   separation (site never imports an arm) and explicit counter reconciliation reduce this risk.
6. **Comparator coincidence.** Because B-RETRIEVAL-SHAPED saves only the fixed 2-request
   root/hub prefix over cold, its stratum-level success profile coincides with cold (`T,T,F,F`);
   the two comparators bracket the ceiling jointly, not independently. Both are mandated by the
   Director, both remain strictly below the treatment, and their ledgers still differ (retrieval
   pays 3 index probes and 1 fewer bootstrap request), so this is disclosed rather than hidden; a
   genuinely stronger retrieval arm is a candidate follow-up.
7. **Controls are deterministic under a faithful render.** Every control passes by construction
   once the render matches the declaration; the controls' non-trivial content is detection of a
   deviating render, so a control failure diagnoses a broken instrument rather than a scientific
   effect.
8. **Session schema is load-bearing for treatment liveness, but failure is a refusal, not an
   overspend.** The treatment's per-task costs assume the declared ascending warm-up sequence.
   If a session's manifest declares any other sequence, the treatment validates and refuses
   (UNKNOWN, no commit, no verify) rather than overspending; any such refusal in the test matrix
   is gate I9 → MEASUREMENT_INVALID (render divergence), and the availability of `B(0.75)=18`
   for a declared single high-novelty task is not assumed.

## 12. Interpretation bounds (non-claims)

- This is an **operational diagnostic / instrument readiness certificate**, not a
  generalization or a product claim. It does not promote anything to product core.
- SUPPORTS removes readiness condition (2) for *this* instrument and widens `C-MEAS-VALID`
  only within its bounded measurement-substrate scope.
- No change is claimed for `C-RESIDUAL-NOVELTY`, `C-PARAM-INHERIT`, `C-LLM-INHERIT` or
  `C-PRODUCT-ECON`. A negative outcome is bounded to this construction and does not close the
  dynamic-range question generally.

## 13. Deliverables / substrate

- Reusable substrate generator: `research/runtime/adb_bank.py` (Runtime lane authorized code
  root), produced by EXECUTE and sha256-recorded in `provenance.json`.
- Frozen bank manifest: `research/experiments/EXP-RUNTIME-38072217499/bank_manifest.json`.

Freeze hashes `request.json`, `spec.json`, `prereg.md` (and, for v2, `design_review.json`).
`freeze_artifacts` is empty and `freeze_artifacts_bound` is `NOT_APPLICABLE` because no
pre-existing mutable repository dependency is consumed; the interpretation surface is pinned
by D1/D2 instead (section 14).

## 14. Artifacts

- Harness + site + arm policies under the experiment directory; raw evidence under
  `raw_evidence/` (per-episode trajectories + server request logs); derived measurements under
  `derived/` (`derived/A-DYNAMIC-RANGE-CERTIFICATE.json`, `derived/A-TASK-BANK-CERTIFICATE.json`,
  `derived/A-PER-TASK-COUNTERS.jsonl`, `derived/A-TREATMENT-LIVENESS.jsonl`).
- Producer outputs: `result.json`, `report.md`, `provenance.json`.
- Bank identity: `research/experiments/EXP-RUNTIME-38072217499/bank_manifest.json` plus the
  generator `research/runtime/adb_bank.py`, both sha256-recorded (delivered post-freeze).
- `freeze_artifacts` list (empty) is recorded in `spec.json`; `freeze_artifacts_bound` is
  `NOT_APPLICABLE` with the reason recorded there.

## 15. Design-phase probes (non-outcome-bearing)

- **Probe 1 (prerequisites):** Python 3.12.15 confirmed; stdlib imports for `http.server`,
  `urllib.request`, `html.parser`, `json`, `hashlib`, `random`, `statistics`, `socket`,
  `threading` all succeed; a `ThreadingHTTPServer` canary bound `127.0.0.1:ephemeral` and
  returned HTTP 200. No arm was run; no success/cost outcome was observed.
- **Probe 2 (arithmetic certificate):** the cost model, success matrix, Wilson bounds, gaps,
  budget separations and digests above were computed by pure arithmetic on the declaration
  (independent of any arm execution) and reproduced independently.
- **Probe 3 (static traces):** the arm procedures were expanded statically to confirm the
  route-trace signatures are disjoint on the declared shared navigational routes and that each
  control can deviate from its expectation (including the NC-REPAIR-TRANSIENT injection); no
  episode was executed.

No confirmatory/outcome-bearing measurement was taken in DESIGN.
