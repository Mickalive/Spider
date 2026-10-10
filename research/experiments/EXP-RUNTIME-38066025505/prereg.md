# EXP-RUNTIME-38066025505 preregistration (Runtime lane)

**Status:** DESIGN (pre-freeze, design-contract v2). This file plus `spec.json` is the
complete frozen interpretation surface for EXECUTE. No outcome-bearing measurement has been
run. DESIGN-phase probes (section 16) are cheap, non-outcome-bearing satisfiability checks.

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
> novelty, a real treatment/comparator behavioural distinction, honest per-condition
> counters, and a preregistered contamination/dynamic-range certificate -- and be delivered
> as a reusable substrate on the lane and/or shipped path that unblocks the flagship
> inheritance benchmark (blocker B2), rather than producing another mandatory-discovery
> deterministic REST certificate that ties cold at the ceiling?

The mandate explicitly **forbids** a further re-run of the deterministic mandatory-discovery
REST certificate (the construction already excluded after `EXP-PRODUCT-37989728440`).

## 2. Why this is a materially new construction (not a repeat)

- The excluded construction (`EXP-PRODUCT-37989728440`, FALSIFIES, bounded) had **symmetric
  mandatory discovery**: every arm had to issue the same `GET /api/session` /
  `GET /api/resources` / `GET /api/schema` calls before acting, so both comparators sat at
  the 1.0 correctness ceiling and no cost gap could exist.
- **ADB-v3 changes the discovery structure**: discovery is *asymmetric* — a session-scoped
  role-resolution layer whose per-role valid candidate must be discovered by experiment and
  can be **persisted across the multiple tasks of one session** only by a stateful mechanism.
  Stateless arms re-pay the bootstrap per task and re-try both candidates per role per task;
  a stateful arm pays the bootstrap once per session and reuses already-discovered roles.
- ADB-v3 is also materially different from the two earlier unfinished Runtime drafts under
  this mandate (`EXP-RUNTIME-38051419597` ADB-v1 and `EXP-RUNTIME-38054047834` ADB-v2): it
  replaces the ambiguous "schema revealed at the end of the boot chain" + "decoy slots"
  framing with an explicit `/try`-accept primitive and an explicit *nested-role, incremental
  within-session persistence* rule; it uses a 5-node boot chain (bootstrap 7, not 8), a
  retrieval baseline that amortises the root/hub prefix from its index but still pays all 3
  index probes, and a rebuilt budget set `{13,14,14,18}` whose success/failure margins are
  all >= 2 requests on every comparator failure cell. No identical invalid/degenerate design
  is repeated; both ADB-v1 and ADB-v2 attempted no freeze and produced no result.

## 3. Inherited state preserved (request `parent_handoff` = `EXP-RUNTIME-37973247935`, SUPERSEDED)

- **established (inherited, unchanged):** the parent `C-MEAS-VALID` ceiling is a bounded
  authorship-separated real-Chromium fixture; the composite oracle's discriminator was
  measurement-invalid on the parent (fingerprint component fired on 260/260 episodes
  including 120 matched nulls).
- **rejected (inherited, unchanged):** no claim change follows from the parent.
- **unknown (inherited):** whether the repaired composite oracle retains out-of-surface
  arm-constrained discrimination — **not tested here**; this experiment does not touch the
  fingerprint/`Connection`-header thread.
- **do_not_assume (inherited):** do not read an absent/failed measurement as a scientific
  negative; do not treat the parent's `MEASUREMENT_INVALID` as closing the transfer question.
- The mandate's `SUPERSEDE` is honoured: this design pivots away from the oracle micro-thread
  to the dynamic-range gate that blocks the flagship chain. Product's accepted bounded
  negative (`EXP-PRODUCT-37989728440`: certificate unsatisfiable on the mandatory-discovery
  deterministic credential-free REST class) is the need this experiment answers.

## 4. Substrate declaration ADB-v3

Credential-free, deterministic, locally-served multi-page REST bank. Python 3.12 stdlib only
(`http.server.ThreadingHTTPServer`, `urllib.request`, `html.parser`, `json`, `hashlib`,
`random`, `statistics`); no browser, no network egress, no credentials, no cookies, no model
calls. Transport is `http://127.0.0.1:<ephemeral>`; the port is **not** part of the frozen
identity (declared `ephemeral-not-frozen`).

Site topology (deterministic, seed `20261010`):

- `GET /` (1) — links to `/hub` and `/sitemap.xml`.
- `GET /sitemap.xml` — lists only `/`, `/hub`, `/about` (site-native enumeration channel; it
  MUST NOT list `/boot/*`, `/tasks`, `/slot/*`, `/try/*`, `/verify`, or any session id).
- `GET /hub` (1) — session classifier; links to `/boot/1`.
- `GET /boot/1 .. /boot/5` (5) — chain; `/boot/5` returns the session manifest: session id,
  canonical base, the ordered role registry `R1..R6`, and, per role, two candidate slot URLs
  `/slot/<role>/a` and `/slot/<role>/b`. For a single-task episode `/boot/5` also returns the
  task spec; for a multi-task session it links to `/tasks`.
- `GET /tasks` (1) — ordered task list (levels 0.0, 0.25, 0.5, 0.75) plus the first task spec.
- `GET /try/<role>/<candidate>` — the resolution primitive: fetches the candidate and commits
  it in one request; the server accepts iff the candidate is the session-valid one for the
  role. Exactly one of `/a`, `/b` is valid per role per session.
- `GET /verify` (1) — confirms the committed state of the current task.

**Role rule.** `h(n) = 8n` hidden roles; level `n` uses the first `h(n)` roles of the
registry: `h(0)=0, h(0.25)=2, h(0.5)=4, h(0.75)=6`. Roles are **nested** (level `n` extends
level `n'<n`), so a role's valid candidate learned at one level is reusable at later levels
of the same session.

**Bank.** `F = 2` families (`F1`,`F2`), `3` test sessions per family, `4` tasks per session
(one per level) = **24 test tasks per arm**; high-novelty (`n>=0.5`) = **12 per arm**;
low-novelty (`n<0.5`) = **12 per arm**. PC-FOREKNOWN-SCHEMA is the fourth matrix arm and runs on
**all 24 tasks** (so the full 4-arm x 4-level matrix is measured and P6 is evaluable). Plus: 6
replay sessions, 5 out-of-family null sessions, 6 budget-truncation episodes.

**Route-leak rule.** Every rendered spec/slot/hub/boot/task page MUST contain no absolute URL
and none of the literals `/s/`, `{sid}`, `/boot/`, `/hub`, `/tasks`, `/slot/`, `/try/`,
`/verify`, or the session id; only the arm's own navigational relative links are permitted.
Checked statically in DESIGN and re-checked at EXECUTE (gate I7).

## 5. Cost model and static traces

The exact per-task request ledger (all arms, identical budget `B(n)`):

| component | B-COLD-RE-DERIVE | B-RETRIEVAL-SHAPED | T-AMORT-REUSE (task k) | PC-FOREKNOWN-SCHEMA |
|---|---|---|---|---|
| bootstrap | 7 (root,hub,boot1..5; spec at boot5) | 5 (boot1..5; index supplies root,hub) | 1x per session (7) | 0 |
| `/tasks` + first spec | — | — | +2 on task 1 | 0 |
| per-task spec fetch | — | — | 1 on tasks 2..4 | 0 |
| role `/try` | `2h` (both candidates) | `2h` (both candidates) | `known*1 + new*2` = 0,4,6,8 | `h` (valid candidate known) |
| retrieval index | 0 | 3 | 0 | 0 |
| `/verify` | 1 | 1 | 1 | 1 |
| **cost** | `2h+8` | `2h+9` | `[10,6,8,10]` (session total 34) | `h+1` |

Costs by level `n` = 0 / 0.25 / 0.5 / 0.75:

- `B-COLD-RE-DERIVE` = 8, 12, 16, 20
- `B-RETRIEVAL-SHAPED` = 9, 13, 17, 21
- `T-AMORT-REUSE` = 10, 6, 8, 10 (discovery charged to task 1)
- `PC-FOREKNOWN-SCHEMA` = 1, 3, 5, 7
- budgets `B(n)` = **13, 14, 14, 18**

Success = every required `/try` accepted and `/verify` confirms, within `B(n)`. Predicted
success matrix: cold `T,T,F,F`; retrieval `T,T,F,F`; treatment `T,T,T,T`; PC `T,T,T,T`.
Comparator-minus-treatment per-task gaps: cold `-2,6,8,10`; retrieval `-1,7,9,11` (both
strictly increasing; Spearman rho = 1.0; minimum high-novelty gaps 8 and 9).

**Behavioural distinction (route traces).** Cold and retrieval walk the boot chain on every
task and issue `/try` both candidates per role; the treatment walks the boot chain once per
session, issues `/tasks` once per session, has `reused_role_tries > 0` from level 0.25, and
issues `/try` counts 0,4,6,8. The positive control skips the bootstrap. The null refuses at
`/hub` with no `/try` and no `/verify`. These signatures are disjoint by construction.

**Static non-degeneracy argument.** Budgets are non-decreasing and do not shrink with
novelty (they are lenient toward comparators). Cold fails at `n>=0.5` because its per-task
cost grows at `2h` while the budget grows slower; the treatment succeeds because it pays the
bootstrap once per session and reuses discovered roles. The failure is not a floor effect:
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
{"arms":["B-COLD-RE-DERIVE","B-RETRIEVAL-SHAPED","T-AMORT-REUSE","PC-FOREKNOWN-SCHEMA"],"budgets":{"0.0":13,"0.25":14,"0.5":14,"0.75":18},"families":["F1","F2"],"h":{"0.0":0,"0.25":2,"0.5":4,"0.75":6},"h_rule":"h(n)=8n","ledger":{"DISCOVERY_COLD":7,"DISCOVERY_RETRIEVAL":5,"DISCOVERY_TREATMENT_SESSION":9,"INDEX_PROBES":3,"TREATMENT_SPEC_FETCH":1,"TREATMENT_TRY_RULE":"known_roles*1 + new_roles*2","TRY_STATELESS_PER_ROLE":2,"VERIFY":1},"levels":[0.0,0.25,0.5,0.75],"name":"ADB-v3","seed":20261010,"sessions_per_family":3,"tasks_per_session":4,"version":3}
```

`D1 = c4a07c9003ed60b4ab007eccec9f72b8dff253a7cbdc3f536a80446bc1508810`

**Predicted-certificate digest D2.** The certificate object is:

```json
{"gaps_vs_treatment":{"B-COLD-RE-DERIVE":[-2,6,8,10],"B-RETRIEVAL-SHAPED":[-1,7,9,11]},"min_high_gap":{"B-COLD-RE-DERIVE":8,"B-RETRIEVAL-SHAPED":9},"n_high":12,"n_low":12,"predicted_costs":{"B-COLD-RE-DERIVE":[8,12,16,20],"B-RETRIEVAL-SHAPED":[9,13,17,21],"PC-FOREKNOWN-SCHEMA":[1,3,5,7],"T-AMORT-REUSE":[10,6,8,10]},"predicted_high_k":{"B-COLD-RE-DERIVE":0,"B-RETRIEVAL-SHAPED":0,"PC-FOREKNOWN-SCHEMA":12,"T-AMORT-REUSE":12},"predicted_success":{"B-COLD-RE-DERIVE":[true,true,false,false],"B-RETRIEVAL-SHAPED":[true,true,false,false],"PC-FOREKNOWN-SCHEMA":[true,true,true,true],"T-AMORT-REUSE":[true,true,true,true]},"wilson":{"k0_n12":{"hi":0.242494,"lo":0.0,"point":0.0},"k12_n12":{"hi":1.0,"lo":0.757506,"point":1.0}}}
```

`D2 = ffa312bb8d376bb0736400b4d83144cbdcad47e98a632951f40610af2a74b88c`

EXECUTE must reproduce `D1` and `D2` byte-for-byte (gate I6). A mismatch is a
MEASUREMENT_INVALID instrument failure, not a scientific negative.

## 7. Controls

- **PC-FOREKNOWN-SCHEMA** (positive; solvability ceiling): given the manifest and valid
  candidate per role out of band, cost `h+1`; must succeed 24/24 across all levels (the 12/12
  high-novelty stratum is the accept region; the 12 low cells are solvability sanity cells).
  Excluded from the gap computation.
- **NC-OOS-FAMILY** (null; out-of-support): 5 frozen out-of-family sessions; the treatment
  must refuse with reason `OUT_OF_SUPPORT` at `/hub` (<=2 requests), `false_accept = 0/5`.
- **NC-BUDGET-TRUNCATION** (negative): 6 episodes with the budget forced below the required
  cost; each must stop at the imposed budget with zero overrun and a recorded failure state.
- **PC-EXACT-SESSION-REPLAY** (independent replay): 6 treatment test sessions re-run; their
  per-route counter vectors must be identical.
- **M-COUNTER-RECONCILE** (honesty): every arm-reported counter must reconcile exactly to the
  site request log.

## 8. Decision rule

Frozen thresholds: ceiling point 0.95; ceiling Wilson lo 0.90; high-novelty threshold 0.5;
`n_high = n_low = 12`; minimum high-novelty gap 8 requests; counter mismatches 0; OOS false
accepts 0; budget overruns 0.

Integrity gates **I1..I9** (spec.json#decision_rule.integrity_gates) are evaluated first; any
failure → `MEASUREMENT_INVALID`. I9 is the low-novelty treatment liveness **abort gate** (the
treatment must resolve every `n<0.5` task within `B(n)`), so it is an instrument gate, not a
scientific proposition. Then:

- **P1** cold high-novelty point < 0.95 AND Wilson lo < 0.90 (predicted `k=0/12`).
- **P2** retrieval high-novelty point < 0.95 AND Wilson lo < 0.90 (predicted `k=0/12`).
- **P3** treatment succeeds 12/12 high AND 12/12 low, every per-task cost <= `B(n)`.
- **P4** per-task comparator-minus-treatment mean gap strictly increasing across levels for
  BOTH comparators (rho = 1.0) and all pooled adjacent increments > 0.
- **P5** minimum high-novelty per-task mean gap >= 8.
- **P6** observed 4x4 success matrix == predicted and observed ledger == predicted (D2).

Mapping: **SUPPORTS** iff I1..I9 and P1..P6; else **FALSIFIES** iff `NOT(P1 AND P2)`; else
**MIXED** = `P1 AND P2 AND NOT(P1 AND P2 AND P3 AND P4 AND P5 AND P6)`. `MEASUREMENT_INVALID`
for any I1..I9 failure. A treatment failure at low novelty (`n<0.5`) is gate I9 → instrument
failure; a treatment failure only at `n>=0.5` is a scientific P3 failure and maps to MIXED.
`INCONCLUSIVE` for bring-up / bind / transport failure. SUPPORTS, FALSIFIES and MIXED are
disjoint and cover every integrity-passing case: the partition is total.

**Reachability of the negative branches (pre-freeze, no outcomes).** *FALSIFIES* is reachable
under an integrity-passing render via any realisation that lets a comparator fit `B(n)` at high
novelty without tripping a gate: the retrieval index realising a larger saving than the
declared 2 requests, or a bootstrap cheaper than the declared `2h+8` (neither is
integrity-gated — a route-token leak is gate I7 and maps to `MEASUREMENT_INVALID`, not to
FALSIFIES). *MIXED* is reachable via a cost-model-only divergence that preserves P1/P2/P3 but
breaks P6/P4/P5. *MEASUREMENT_INVALID* is reachable via any I1..I9 failure. Under a
byte-faithful render SUPPORTS is expected by construction; that is the honest nature of a
certification experiment — the empirical content is the verification that the render matches
the declaration.

## 9. Metrics (stable identities for AUDIT)

`M-HIGH-POINT` (comparator high-novelty success proportion), `M-HIGH-WILSON-LO` (two-sided
95% lower bound, n=12), `M-GAP-PER-LEVEL` (comparator minus treatment per-task request cost,
per level), `M-MIN-HIGH-GAP`, `M-LEDGER` (per-route request counts), `M-RECONCILE-DELTA`
(arm counter minus site log). Decision inputs are deterministic HTTP-request counters only;
`latency_ms` and model calls/tokens are recorded but **prohibited** as decision inputs.

## 10. EXECUTE procedure and abort gates

1. Materialise the generator + site + harness from this frozen declaration; recompute D1/D2
   (gate I6) before any arm runs.
2. Run the **low-novelty block FIRST** as the post-freeze liveness abort gate **I9**: the
   treatment must succeed at `n=0` and `n=0.25` with its per-task cost within `B(n)`; failure
   aborts to MEASUREMENT_INVALID.
3. Run PC-FOREKNOWN-SCHEMA first among controls (I1) to prove solvability, then the full
   4-arm x 4-level matrix, then NC-OOS-FAMILY (I2), NC-BUDGET-TRUNCATION (I3),
   PC-EXACT-SESSION-REPLAY (I5), counter reconciliation (I4), route-leak scan (I7) and
   determinism re-run (I8).
4. Preserve raw evidence (`raw_evidence/` trajectories + server request logs) separately from
   derived measurements (`derived/`) and interpretation.

## 11. Validity threats (disclosed)

1. **Synthetic substrate.** The bank is authored, not sampled from the Web; it certifies the
   *instrument*, not transfer to the open Web or to a real LLM agent.
2. **Declared policies / memory asymmetry.** The declared asymmetry between the arms is a
   within-session *memory* asymmetry, stated openly: the protocol is
   `GET /try/<role>/<candidate>` (fetch-and-commit, returns accepted/rejected); a stateless
   episode treats each task independently and does not carry a resolution receipt across
   tasks, so the declared cold/retrieval policies try both candidates per role on every task
   (2h), while the treatment carries the receipt within the session and reuses it. The
   comparators are otherwise deliberately strong (shortest bootstrap, full site-native
   enumeration, a real 3-probe index that saves only the 2-request root/hub prefix). This
   experiment certifies the instrument under exactly these declared policies and explicitly
   does **not** claim the stateless policy is optimal; a stronger stateless policy that
   persists a receipt within a task, or a retrieval policy with a within-session mechanism
   store, is out of scope and is precisely what F1/F3 is designed to detect if it
   nevertheless reaches the ceiling.
3. **Within-session persistence is the treatment's claimed mechanism.** A retrieval policy
   that also persists within a session would blur into the treatment; it is out of scope by
   construction and is exactly the downstream four-arm question.
4. **Tautology risk.** Because the certificate is arithmetic, SUPPORTS is largely the
   declaration taking effect under a byte-faithful render; the genuinely falsifiable content
   is implementation divergence, index/bootstrap realisation larger or cheaper than declared,
   leakage, dishonesty and behavioural divergence (MIXED/FALSIFIES/MEASUREMENT_INVALID). This
   is disclosed openly; section 8 states the concrete reachable negative branches. The
   experiment must not be read as if SUPPORTS were an independent corroboration of the
   arithmetic.
5. **Harness-authored ground truth.** The site is the request-log authority; authorship
   separation (site never imports an arm) and explicit counter reconciliation reduce this risk.
6. **Comparator coincidence.** Because B-RETRIEVAL-SHAPED saves only the fixed 2-request
   root/hub prefix over cold, its stratum-level success profile coincides with cold
   (`T,T,F,F`); the two comparators bracket the ceiling jointly, not independently. Both are
   mandated by the Director, both remain strictly below the treatment, and their ledgers still
   differ (retrieval pays 3 index probes and 1 fewer bootstrap request), so this is disclosed
   rather than hidden; a genuinely stronger retrieval arm is a candidate follow-up.
7. **Controls are deterministic under a faithful render.** Every control passes by
   construction once the render matches the declaration; the controls' non-trivial content is
   detection of a deviating render, so a control failure diagnoses a broken instrument rather
   than a scientific effect.
8. **Session ordering is load-bearing for treatment liveness.** Liveness depends on the frozen
   per-session ordering (task1 at `n=0`, then 0.25/0.5/0.75): a session whose first task were
   `n=0.75` would cost `~9+12+1=22 > B=18` and fail. The ordering is seed-frozen, so the
   treatment is live; a reordered/resumed session is a render divergence caught by I9/I6.

## 12. Interpretation bounds (non-claims)

- This is an **operational diagnostic / instrument readiness certificate**, not a
  generalization or a product claim. It does not promote anything to product core.
- SUPPORTS removes readiness condition (2) for *this* instrument and widens `C-MEAS-VALID`
  only within its bounded measurement-substrate scope.
- No change is claimed for `C-RESIDUAL-NOVELTY`, `C-PARAM-INHERIT`, `C-LLM-INHERIT` or
  `C-PRODUCT-ECON`. A negative outcome is bounded to this construction and does not close the
  dynamic-range question generally.

## 13. Deliverables / artifacts

- Reusable substrate generator: `research/runtime/adb_bank.py` (Runtime lane authorized code
  root), produced by EXECUTE and sha256-recorded in `provenance.json`.
- Frozen bank manifest: `research/experiments/EXP-RUNTIME-38066025505/bank_manifest.json`.
- Harness + site + arm policies under the experiment directory; raw evidence under
  `raw_evidence/`; derived measurements under `derived/`.
- Producer outputs: `result.json`, `report.md`, `provenance.json`.

Freeze hashes `request.json`, `spec.json`, `prereg.md` (and, for v2, `design_review.json`).
`freeze_artifacts` is empty and `freeze_artifacts_bound` is `NOT_APPLICABLE` because no
pre-existing mutable repository dependency is consumed; the interpretation surface is pinned
by D1/D2 instead.

## 14. Reproducibility

All topology, ordering, role values and slot values are deterministic functions of the
declaration and seed `20261010`. The same episode run twice must produce byte-identical
counters (I8). No wall-clock-, network- or model-dependent quantity enters the decision.

## 15. Design-phase probes (non-outcome-bearing)

- **Probe 1 (prerequisites):** Python 3.12.15 confirmed; stdlib imports for `http.server`,
  `urllib.request`, `html.parser`, `json`, `hashlib`, `random`, `statistics`, `socket`,
  `threading` all succeed; a `ThreadingHTTPServer` canary bound `127.0.0.1:ephemeral` and
  returned HTTP 200. No arm was run; no success/cost outcome was observed.
- **Probe 2 (arithmetic certificate):** the cost model, success matrix, Wilson bounds, gaps
  and digests above were computed by pure arithmetic on the declaration (independent of any
  arm execution) and reproduced independently.
- **Probe 3 (static traces):** the arm procedures were expanded statically to confirm the
  route-trace signatures are disjoint and that each control can deviate from its expectation;
  no episode was executed.

No confirmatory/outcome-bearing measurement was taken in DESIGN.
