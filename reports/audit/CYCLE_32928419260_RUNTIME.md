# RUNTIME INDEPENDENT AUDIT — CYCLE R2-1 (run 32928419260, repair round 0)

Auditor: runtime_auditor (ACTIVE_AUDITOR, lane RUNTIME) — separate session.
Audit base: `/home/runner/work/Spider/Spider` @ `917bbf8` (untouched accepted
Runtime base, branch `runtime-audit-base`). Team snapshot audited:
`/tmp/spider_runtime_team` @ `8e99234` (= base + exactly 5 commits,
`cycle/runtime/32928419260/team`). Delta is **insertion-only** (12 new files,
0 deletions, 0 modifications): verified via `git diff --stat 917bbf8..8e99234`.
Write scope honored: only `reports/audit/` and `results/audit/`.

Cycle executed: Program R2 priority 1 (mechanism-floor null + additive
URL-construction comparator record) and priority 3 (WB-consumer cell:
quarantine). Priority 2 correctly NOT triggered (requires surviving cells).

---

## 0. Verdict summary

**GATE: REVISE** (round 0). The headline scientific result — `FLOOR_VOID`
on the quotes-login goal class, no substrate inference in either direction,
repair-first — **survives full adversarial recomputation** and its wording
respects every frozen ceiling. Three concrete, mechanical defects exist in
the *harness/provenance layer* (not in any verdict), each repairable
same-cycle without touching the frozen question, benchmark, thresholds or
outcome artifacts:

- **RF-1** zero-affordance fallback dead path in the measurement arm
  (convention paths computed but never probed; telemetry claims probes that
  never happened);
- **RF-2** PREFLIGHT event note truncated mid-JSON at the 900-char cap
  (malformed durable evidence row; prereg sha cut at 42/64 chars);
- **RF-3** impossible `updated_utc` (05:20:00Z) in the state JSON committed
  at 05:00:07Z — fabricated-looking provenance metadata.

None of the three flips any R2-1 outcome; all matter because Director
integration makes this snapshot the accepted harness base for R2-2.

---

## 1. Claim-by-claim audit

### C1 — Headline: `FLOOR_VOID`; wrong-password control passed; nothing flips

* **Evidence files:** `results/runtime/r2_floor/r2_floor_results.json`,
  `.../cost_events.jsonl`, `.../substrate_decision_r21.json`,
  `reports/runtime/R2_CYCLE1_REPORT.md`.
* **Recomputation performed (independent):** loaded the committed stream with
  the frozen loader (`gates_r2.g0.load_spider_events`): 74 raw lines → 37
  deduped rows; `verify_twin_identity` errors = 0. Re-ran
  `gates_r2.gate_floor_cycle` on the frozen enumeration
  [FLR-T3P1, FLR-T3P2, FLR-CONFIRM-P2] + FLR-NEGCTRL: output **deep-equal**
  (`json.dumps` identity) to the committed `analysis` block. Outcome
  `FLOOR_VOID`, precedence VOID > DOMINATES correct per prereg §2.2 step 9 /
  §4. Ran `gates_r2.self_test()` live during audit: all six fabricated
  branches decided mechanically correctly (dominates/fails/
  inconclusive_health_trip/invalid_arm_budget_breach/void_surface/
  must_not_fire_violation).
* **Stream anatomy:** actN rows per cell = exactly
  [`affordance_probe GET /login`, `submit POST /login`,
  `redirect_hop_1 GET /`] = 3 wire transactions on all four cells including
  the negative control; one verify row + one summary row per cell;
  summary actions == actN count (P5'/G-FLOOR0 true).
* **Mechanism check:** SUCCESS_PRED = {host_allowlist quotes.toscrape.com,
  elem_text_any ["logout"]}; NEGCTRL posted username=`spiderbot` /
  password=`wrongpass` (only `is_secret` mutated — verified) and still
  judged pass with all guards true. The environment accepts any credentials;
  the preregistered control assumption is falsified by the environment. This
  matches the well-known behavior of the sandbox site and is internally
  derivable from committed rows (must-not-fire OK proves the entry page has
  no logout token; NEGCTRL final judged pass proves logout appears after any
  POST). VOID reasoning sound; refusal of the seductive FLOOR_DOMINATES
  reading (3 ≤ 6, all pass) is exactly what the frozen rule mandates.
* **Failure modes tested:** hidden answer leakage (see C5), stale reuse
  (C6), double counting (twin dedup + P5' above), verdict flipping (gate
  precedence + self-test), negative-control gaming (control excluded from
  budget quantifier, present as its own row — verified).
* **STATUS: CONFIRMED.**

### C2 — Freeze-before-outcomes discipline (git-orderable chain)

* **Forensics performed:** `git ls-tree 5dd51ab -- results/runtime` → no
  R2 outcome artifacts existed at the prereg commit. Post-freeze commit
  `95aa45a` touches ONLY `reports/runtime/R2_CYCLE1_PREREG.md` (+26 addendum
  lines, §10 disclosure) and `runtime/r2_cycle1.py` (+24/−4: blinding
  exemption + raw-scan serialization — diff inspected line-by-line, no other
  change smuggled). Harness modules (`floor_null.py`, `gates_r2.py`,
  `policies_r2.py`) and tests are **byte-identical from `b4254a6` through
  HEAD** (empty diffs). Prereg sha256 recomputed =
  `950a4ded…279a199` == pin in results JSON == pin claimed in state/report.
  Outcomes commit `c2f0a6d` adds results only; report commit adds report
  only.
* **Residual limit:** single-machine timing cannot be cryptographically
  proven, but the chain is git-orderable, the correction is the *least*
  convenient direction (it documents a failed first start), and the realized
  outcome (VOID) is the lowest-reward branch — strong internal consistency.
* **STATUS: CONFIRMED** (with the irreducible single-machine caveat noted).

### C3 — Gates are mechanical, outcome-blind, and consume the stream only

* **Recomputation:** see C1. Additionally inspected gate code for
  denominator traps: negative control excluded from the budget quantifier;
  sensitivity B∈{3..6} computed but never verdict-bearing;
  `INVALID_ARM` requires all-success AND budget breach; `FLOOR_FAILS` is the
  only headroom-supporting branch and requires judge fail without health
  trips. Tri-value judge states preserved (no boolean flattening).
* **STATUS: CONFIRMED.**

### C4 — Matched-task discipline

Same committed T3 entry URLs as the R1 browser arms (dual hash pins checked
at load by `policy_sweep.load_snapshots`), same shared fills spec asserted by
`fills_identity()`, same ONE vendored predicate dialect (`predicates.py`
imported unchanged; no new clauses — grep-verified). No cross-task-set ratio
is presented anywhere; no speedup/margin number is presented at all.
* **STATUS: CONFIRMED.**

### C5 — Hidden IDs / leakage / blinding

* Independent auditor re-scan of both new modules against the frozen fixture
  (`policy_blinding_tokens.json`): hard leaks (site strings, credentials,
  capsule ids, witness refs) = **NONE**; only hits are `rt.tasks`/`rt.capsules`
  predicate refs, covered by the disclosed §10 exemption (fixture's own
  design note scopes the fixture to capsule knowledge in memory-free
  policies; these tokens name the shared judge and appear in every audited
  harness module). Raw+filtered scans serialized in the PREFLIGHT row match
  my re-scan exactly.
* `/login` appears as CONSTRUCTED_PATH/convention vocabulary: sanctioned by
  the fixture design note ("'login' is deliberately absent … generic
  affordance vocabulary") and disclosed in prereg §9 as deliberate
  bias-AGAINST-inheritance. The answer route being inside the frozen
  convention list strengthens, not weakens, the comparator.
* No internal fragment ID is required of any external caller anywhere in
  this cycle (no resolve surface touched).
* **STATUS: CONFIRMED** (see W-2 for wording of the void-mechanism
  diagnosis).

### C6 — Stale reuse / accepted-state mutation

Diff base→team is insertion-only across exactly the 12 declared files.
`policies.py`, `baseline.py`, `derive.py`, `gates.py`, `pilot2.py`,
`gates_r1.py`, `r1_strong.py`, accepted registries/streams, and
`directives/RUNTIME.md`: byte-untouched. R1 winner `goal_href|root0` and the
frozen sweep artifact never re-ranked (URL-arm artifact declares
gating NONE; verified no survival semantics in `policies_r2.py`). Reused
inputs (HREF_RE, LEXICON, FILLS, predicates, snapshots) are all accepted,
hash-pinned lineage.
* **STATUS: CONFIRMED.**

### C7 — Overhead accounting / X31 ceilings

No compression phrasing at any tier (scan: only "margins repeat the K3
lesson" — a future-canon requirement, not a claim); no economics figure
anywhere; `reuse_yield` UNDEFINED recorded in prereg/report/state; wall-clock
advisory only; model independence explicitly UNFALSIFIABLE (zero provider
calls; `model_id="none:http-floor-v0"`); zero browser launches (stdlib-only
imports verified). Verification overhead honestly tiny and recorded
(native predicate eval ms in verify rows); retrieval overhead = parse-only
discovery (0 transactions). See W-1 for the one cross-unit arithmetic field.
* **STATUS: CONFIRMED.**

### C8 — Refuse-list compliance

Measurement-arm-only module (header + grep: never imported by
resolver/executor/registry/writeback — verified clean); no substrate
expansion; no replication of killed observations; no second caller; no
MCP/wire freeze; no Pareto/TTL/confidence machinery; no new cost_event
fields/enums (row keys ⊆ v0 schema properties; stages/classes/phases within
enum; `arm` is an open string — `http_floor` is a new value, see W-4);
schemas v0 untouched; priority-3 quarantine is a directive-sanctioned
alternative and its ground (playwright absent) verified true in this
environment.
* **STATUS: CONFIRMED.**

### C9 — Test suite

Runtime lane suite executed independently by the auditor (pytest installed
by auditor into `/tmp/opencode/pylibs`; no repo mutation):
**tests/runtime: 160 passed, 0 failed**. Repo-wide `tests/test_integrity.py`
has 1 failing test (`PhysicsLeakageGuardTests::test_true_previous_action_sequence_passes`)
— reproduced identically on the untouched audit base → pre-existing
Physics-lane/environmental, **not** a Runtime-cycle regression.
* **STATUS: CONFIRMED** (with W-5).

---

## 2. Required fixes (same-cycle repairable; none touch frozen outcomes)

### RF-1 — Zero-affordance fallback dead path in `FloorMeasurementArm.run`

`runtime/floor_null.py` (lines ≈504–536):

```python
probes = [(u, source) for u in cands] if cands else []
if source != "convention_fallback":
    probes += [(root + cp, ...) for cp in CONVENTION_PATHS]
```

When `discover_login_url` returns `(None, "convention_fallback", convs)`
(i.e., the entry page contains **no** login-affordance anchor), `cands == []`
so `probes == []`, the append branch is skipped precisely because
`source == "convention_fallback"`, and the probe loop executes zero times:
`form is None` → `trip("NO_FORM_MATCHED")` → `FLOOR_FAIL` **without a single
convention GET**, while `discovery_candidates`/`candidates_tried` telemetry
records the five untried convention URLs. This contradicts the arm's own
frozen procedure text (prereg §2.2 step 4: "ONLY IF none yields a form, the
alphabetical convention paths are probed") and burns a live cell into
CYCLE_INCONCLUSIVE (missing verify row + health trip) instead of a decidable
verdict.

*Blast radius (accurate):* **zero effect on R2-1 outcomes** — all four live
cells discovered via `affordance_href` (stream-verified). Downstream, the
gate's P5' check prevents a false FLOOR_FAILS cycle classification (missing
verify row forces CYCLE_INCONCLUSIVE), so there is **no false-headroom
leak**; the harm is procedure violation, lying telemetry, wasted live
budget, and a broken primitive being handed to R2-2. Unit test coverage
confirms the gap: `test_convention_fallback_when_no_affordance` tests only
the pure discovery function; `test_stale_affordance_falls_back_to_conventions`
covers the affordance-hit-but-dead case, never the zero-affordance case.

*Fix:* build the unified probe list as `affordance candidates +
(convention paths if no candidate yields a form)` for BOTH discovery
sources (i.e., drop the `source != "convention_fallback"` guard and seed
`probes` with `[(u, source) for u in cands]` unconditionally, appending
conventions whenever affordance probing exhausts); add a full-cell mock test
with a no-anchor entry page asserting the convention GETs occur.

### RF-2 — PREFLIGHT evidence row truncated mid-JSON

The driver caps notes at 900 chars (`json.dumps(...)[:900]`). The PREFLIGHT
note is exactly 900 chars and ends mid-hash:
`"prereg_sha256": "950a4ded2b1698ba2cabf1cf554cd3db1e1f45a414` (42/64 chars)
— a malformed JSON payload inside a durable evidence row. What matters most
survived intact (raw blinding scan, filtered scan, full parity block,
parity_ok), and the full sha pin lives in `r2_floor_results.json`; but the
committed stream row is corrupt-as-JSON and the addendum's "serialized into
the PREFLIGHT event row for auditor re-derivation" is only partially true
for the trailing pin. No gate consumes this row.

*Fix:* raise the cap for this row or split PREFLIGHT into compact rows;
regenerate the PREFLIGHT provenance via a disclosed correction artifact (do
NOT rewrite the outcomes commit); add a serialization round-trip assertion
(`json.loads(note)` must succeed) to the harness.

### RF-3 — Impossible timestamp in the durable state record

`results/runtime/r2_cycle1_state.json` records
`"updated_utc": "2026-08-26T05:20:00Z"` but was committed in `c2f0a6d` at
**2026-08-26T05:00:07Z** — a hand-written time ~20 minutes after its own
commit. Everything else in that file reconciles with the artifacts (cells,
gate_reason, freeze_chain, quarantine, statuses all verified). A durable
record must not carry projected clock values: it poisons provenance ordering
in exactly the lane that polices git-orderable freeze chains.

*Fix:* correction block recording actual assembly time and disclosing
hand-assembly of the state file (or generate timestamps mechanically at
write time going forward). Do not silently edit the committed file's
history.

---

## 3. Warnings (non-blocking)

* **W-1** `strictly_cheaper_than_4_descriptive_only=true` embeds cross-media
  arithmetic (3 wire transactions < 4 browser actions) that prereg §2.3/§7
  forbid elevating to any efficiency claim (browser loads hide sub-resource
  fanout; floor requests are naked). It was frozen pre-outcome at
  `b4254a6`, is non-gating, and is unquoted in prose — acceptable as
  comparator arithmetic, but it must NEVER migrate into wording; rename or
  annotate at next harness touch.
* **W-2** The void-mechanism diagnosis says "verified out-of-harness"
  (anonymous home Login/no-Logout; wrongpass POST → Logout) with no separate
  artifact. The facts ARE derivable from committed rows (must-not-fire OK +
  NEGCTRL verify pass); tighten wording to cite those rows rather than
  implying an unsaved manual experiment.
* **W-3** Parser-parity oracle is thin: n_oracle anchors = 1 per entry
  (mitigated by 44/44 and 57/57 whole-element count equality plus the
  must-not-fire/negative-control/form guards; residual static-parser
  visibility limit already disclosed).
* **W-4** `http_floor` is a new `arm` string value in cost events. The v0
  schema leaves `arm` open (no enum violation), but register it in the
  schema documentation at the next schema-touching change.
* **W-5** Audit-environment note (OPERATIONAL_DIAGNOSTIC): pytest/numpy were
  absent from the audit mount; the auditor installed them into
  `/tmp/opencode/pylibs` (outside both mounts' tracked scope) to execute the
  suites. Lane suite result is the auditor's own execution.

---

## 4. Maximum defensible wording (integration ceiling)

> On the quotes-login goal class (one site family, one date, three live
> passes + one wrong-password negative control, one scripted stdlib
> implementation, zero browser launches), the mechanism-floor null is
> **FLOOR_VOID**: the wrong-password control PASSED verification, therefore
> the direct-HTTP surface cannot discriminate credential validity on this
> goal class; per the frozen gate ALL floor verdicts are void and no
> browser-inheritance-headroom or floor-domination inference is licensed in
> either direction. Witnessed-effect addressing POC not triggered;
> `reuse_yield` UNDEFINED; no economics figure quoted; model independence
> untested and unfalsifiable in this cycle (zero provider calls);
> observation-tier facts (3 wire transactions/cell ≤ B_FLOOR=6, all guards
> true, G-FLOOR0/G-FLOORa true) stand void-caveated. Substrate decision:
> NO_SUBSTRATE_DECISION_VOID — repair-first; stop-rule (b) not invoked.

This equals the team's report ceiling; the team did not exceed it anywhere.

---

## 5. Provenance of this audit

* Base tip: `917bbf8`; team tip: `8e99234`; delta insertion-only (12 files).
* Recomputation commands executed read-only against the team mount; no team
  artifact modified; no live HTTP performed by the auditor; gate/self-test
  executions write tempfiles only under the OS temp dir.
* Gate JSON: `results/audit/CYCLE_32928419260_RUNTIME_GATE.json`.

— runtime_auditor, independent session, 2026-08-26.
