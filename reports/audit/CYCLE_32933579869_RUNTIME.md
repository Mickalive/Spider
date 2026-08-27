# RUNTIME INDEPENDENT AUDIT — CYCLE R2-1 REPAIR ROUND 1 (run 32933579869)

Auditor: runtime_auditor (ACTIVE_AUDITOR, lane RUNTIME) — separate session.
Audit base: `/home/runner/work/Spider/Spider` @ `917bbf8` (untouched accepted
Runtime base, branch `runtime-audit-base`). Team snapshot audited:
`/tmp/spider_runtime_team` @ `89ffeba` (== `origin/cycle/runtime/32933579869/team`
== `.../team-attempt-1`; working tree clean). Lineage verified: both
`917bbf8` and the rejected round-0 snapshot `8e99234` are ancestors; the
repair is exactly two commits (`09536fd` code+tests, `89ffeba`
artifacts+report). Delta vs accepted base remains **insertion-only**
(18 files, +4436/−0; no accepted file modified).
Write scope honored: only `reports/audit/` and `results/audit/`.

Audited object: REVISE-repair round 1 for audit `CYCLE_32928419260_RUNTIME`
(gate REVISE round 0; required fixes RF-1/RF-2/RF-3 + warnings W-1..W-5).

---

## 0. Verdict summary

**GATE: PASS.** All three required fixes are resolved inside the audit's
own scope, without touching the frozen question, cell enumeration, budget,
success oracle, gate rule, or any outcome artifact. The FLOOR_VOID headline
and its wording ceilings stand exactly as frozen. One material correction
to the round-0 audit itself is established: **RF-1's alleged dead path did
not exist on this snapshot** — the team refuted it with evidence and my own
independent reproduction confirms the refutation. The team nonetheless
applied the requested hardening plus stronger regressions, which is the
correct non-destructive-continuity behavior.

No remaining `required_fixes`. Six auditor warnings below (none blocking).

---

## 1. Claim-by-claim audit

### C1 — Frozen outcomes byte-preserved; freeze discipline intact

* **Evidence:** git blob identity `8e99234:` vs `HEAD:` for prereg, events
  stream, floor results, substrate decision, URL-arms artifact — all
  UNCHANGED; sha256 of all five recomputed by the auditor and equal to the
  repair report §5 manifest (`ce719500…`, `debe7cef…`, `db094b05…`,
  `0df622fb…`, `950a4ded…`). Prereg digest == results field == state field.
* **STATUS: CONFIRMED.**

### C2 — Gate recomputation over the committed stream (work-compression claims recomputed)

* **Recomputation performed (independent):** loaded the committed stream
  with the frozen loader: 74 raw lines → 37 deduped rows;
  `verify_twin_identity` errors = 0. Re-ran `gates_r2.gate_floor_cycle`
  over the frozen enumeration [FLR-T3P1, FLR-T3P2, FLR-CONFIRM-P2] +
  FLR-NEGCTRL at B_FLOOR=6: output **deep-equal** (`json.dumps` identity)
  to the committed `analysis` block. Outcome **FLOOR_VOID** unchanged.
  `gates_r2.self_test()` executed live: all six fabricated branches decide
  mechanically correctly.
* **Stream anatomy re-verified:** 12 actN rows = 4 cells × exactly
  [`affordance_probe GET /login`, `submit POST /login`,
  `redirect_hop_1 GET /`] — including the negative control. No convention
  probe was ever spent on a live cell, confirming the report's §2/§7
  anatomy statements.
* **Compression/economics wording rescan** of every new or changed prose
  artifact (report, repair report, state): zero compression/speedup/yield/
  break-even figures anywhere; `reuse_yield` stays UNDEFINED; X31 honored;
  the only "yield" hits are innocuous English verbs. No metric is double
  counted because no metric beyond per-cell step counts exists in this
  cycle, and those were recomputed identical to the committed analysis.
* **STATUS: CONFIRMED.**

### C3 — RF-1 disposition: prior finding EMPIRICALLY REFUTED; hardening applied anyway

* **Auditor's independent refutation repro (hermetic mock transport, no
  network), run against BOTH the audited snapshot module (`floor_null.py`
  @ `8e99234`) and the hardened module @ `89ffeba`:**
  - Zero-affordance entry (no HREF_RE anchor anywhere), formless
    conventions: OLD code executes **all five convention GETs in frozen
    order** (`/auth, /log-in, /login, /signin, /sign-in`), ends
    NO_FORM_MATCHED with trip row honestly recording `probes: 5`,
    verdict FLOOR_FAIL at 5 steps. NEW code byte-identical in observable
    behavior.
  - Form-at-/login variant: OLD == NEW (identical verdict/steps/probe
    sequence; my simplified mock judge plumbing yields `judge=fail` where
    the real predicate wiring passes — irrelevant to old-vs-new identity,
    and the team's own full-cell tests pin the FLOOR_PASS path).
* **Static confirmation:** at `8e99234`, `discover_login_url` returns
  `(None, "convention_fallback", convs)` with `convs` = the five convention
  URLs, so `cands` was never empty and the round-0 premise "`cands == []`"
  was false. The alleged "lying telemetry" and "burned live cell" harms
  could not occur. Recorded here as a **false-positive round-0 finding**;
  the round-0 report remains immutable history and this section is its
  correction of record.
* **Hardening inspected line-by-line:** probe construction now source-
  unified (affordance candidates first; conventions appended only when not
  already the seed — note the round-0 *literal* fix text would have
  double-probed conventions on fallback, ~10 GETs; the implemented version
  avoids that while preserving audited-harness behavior); fallback-seed
  identity pinned by assertion; full-cell regressions
  `TestZeroAffordanceFallbackCell` (conventions probed + pass-through
  /login; exhausted sweep = FLOOR_FAIL at probes=5) plus a divergence-pin
  test (lying discovery ⇒ AssertionError). All executed as part of the
  182-test lane suite.
* **STATUS: CONFIRMED** (refutation correct; hardening sound; zero outcome
  effect, consistent with the round-0 blast-radius statement).

### C4 — RF-2 disposition: defective durable row preserved; deterministic provenance correction verified

* **Pre-state sanity (auditor-checked):** the committed PREFLIGHT note in
  the byte-preserved stream is still exactly 900 chars, still FAILS
  `json.loads`, sha256 `39ada544…` — the defect is preserved as evidence,
  not rewritten.
* **Correction artifact independently verified:** full rebuilt note =
  924 chars; **exact-prefix byte identity over all 900 visible chars**
  against the committed truncated note; round-trips through `json.loads`;
  carries the complete 64/64 prereg sha == recomputed file digest; parity
  payload deep-equal to the committed `r2_floor_results.json:
  parity_preflight`; blinding raw-scan fragment verbatim-present in the
  committed prefix.
* **Generator discipline:** `python3 -m runtime.repair_cycle3 --check`
  fixed point OK (executed by auditor); bare re-run refuses write-once
  (verified live). Stop rules are pre-committed in code (sha re-pins,
  defect-present sanity, exact-prefix transcription, round-trip, triple
  prereg agreement).
* **Harness fix forward-inspected:** `_note_json` / `FloorMeasurementArm
  ._row` now emit notes WHOLE with a mechanical round-trip assertion;
  NOTE_SANITY_MAX=8000 raises rather than truncates; v0 schema types
  `note` as unconstrained string (schema-legal). Regression pins
  (`TestNoteHygiene`) present and passing.
* **STATUS: CONFIRMED.**

### C5 — RF-3 disposition: surgical state transform, disclosed hand-assembly

* **Independent deep-diff** `8e99234:` vs HEAD for
  `results/runtime/r2_cycle1_state.json`: exactly three changes —
  (i) `priority_1_floor_null.void_mechanism` gains the W-2 row-citing tag
  as a pure suffix (original preserved **verbatim** in the
  `repair_round_1.original_void_mechanism_verbatim` field — string-equality
  checked); (ii) one added top-level key `repair_round_1`; (iii)
  `updated_utc` restamped mechanically (`2026-08-26T05:40:53Z`, ≤ commit
  time of `89ffeba` = 05:48:25Z — the projection-ahead defect class is
  gone). **Zero removed keys; every other field deep-identical.**
* Disclosure block records hand_assembled=true, original value, actual
  commit time (`05:00:07Z` in `c2f0a6d`), and the mechanical-timestamp rule
  going forward. Exactly what the round-0 audit prescribed.
* **STATUS: CONFIRMED.**

### C6 — Warnings W-1..W-5 disposition

* **W-1:** annotated at definition site (`runtime/gates_r2.py`, comment
  only — key name unchanged so gate regeneration stays deep-equal, which I
  re-verified in C2). Non-gating witness re-verified: the key occurs
  exactly once across `runtime/*.py` (its definition); no consumer.
* **W-2:** corrected by suffix tags in report §3 and lane state; original
  wording preserved verbatim in the repair block;
  `substrate_decision_r21.json` left byte-untouched with supersession
  recorded — proper immutable-history handling.
* **W-4:** registration deferred to next schema-touching change per the
  round-0 condition, recorded durably in the repair block so it cannot be
  lost. Accepted.
* **W-3/W-5:** residual disclosed / environmental; correctly no-op.
* **STATUS: CONFIRMED.**

### C7 — Stale reuse, context mismatch, hidden IDs, fallback, verification cost

* **Stale reuse:** diff base→team insertion-only; no accepted module,
  registry, stream, directive, or schema touched; R1 winner/sweep artifact
  never re-ranked (URL-arms artifact gating NONE; regeneration deep-equal
  re-verified). All reused inputs hash-pinned lineage.
* **Hidden IDs / internal-ID dependence:** no resolve surface touched this
  cycle (grep: none of the touched modules references resolver/resolve);
  nothing new requires an external agent to know internal fragment IDs.
  Predicate refs in harness notes name the shared judge (exempt class),
  consistent with round-0 C5.
* **Leakage rescan extended by auditor to ALL touched/new modules AND the
  new artifacts:** harness modules carry only exempt `rt.tasks`/`rt.capsules`
  tokens; test fixtures contain sandbox site/credential strings — same
  precedent as accepted-base modules (`pilot2.py`, `r1_strong.py`) which
  also carry them; memory-free policy modules scan clean. No new leak.
* **Fallback correctness:** the cycle's one fallback path is now pinned by
  assertion and regression-tested (C3). No missing-fallback surface
  remains in the measurement arm.
* **Verification/maintenance overhead honestly accounted:** verify rows
  record native predicate eval ms; the repair adds one dumps+loads per
  durable row (negligible) and a write-once provenance tool; residual
  maintenance exposure is disclosed (see W-A2/W-A6).
* **Evidence tiers:** corrections labeled DURABLE_UNAUDITED until this
  acceptance; no tier inflation anywhere; FLOOR_VOID ceiling not exceeded.
* **STATUS: CONFIRMED.**

### C8 — Test suite and integrity (independent execution)

* Lane suite on the repair tip: **182 passed, 0 failed**. Lineage verified
  end-to-end: 160 passed on a throwaway clone of rejected `8e99234` →
  182 at tip (+22 repair pins), matching the claimed 160→182.
* Repo-wide `tests/test_integrity.py`: single failure
  `PhysicsLeakageGuardTests::test_true_previous_action_sequence_passes`,
  reproduced identically on the untouched base `917bbf8` → pre-existing
  Physics-lane/environmental, not a Runtime regression (base lane suite:
  129 passed).
* No live HTTP performed by the repair (all reruns hermetic or
  committed-evidence recomputation) — consistent with commit contents.
* **STATUS: CONFIRMED.**

---

## 2. Required fixes

None. All round-0 required fixes are resolved within their scoped blast
radius; nothing further is repairable-or-needed, and nothing was moved
post-outcome.

## 3. Warnings (non-blocking)

* **W-A1 (audit-process lesson, observation tier):** Round-0 RF-1 was a
  false positive caused by reasoning about a dead path from code reading
  without executing it. Standing lesson for future Runtime audits: alleged
  dead paths must be reproduced before being alleged, and literal fix
  prescriptions can themselves be harmful (the round-0 fix text would have
  introduced double-probing of conventions on the fallback source).
* **W-A2 (maintenance overhead, disclosed):** the historical 900-char
  truncation pattern still exists in accepted prior-cycle modules
  (`pilot.py`, `economics.py` per repair report §2). Durable rows emitted
  by those modules remain truncatable until their next harness touch.
  Deferred-with-record is acceptable; it must not be deferred twice.
* **W-A3 (budget semantics):** NOTE_SANITY_MAX raises mid-run (loud abort)
  rather than emitting corrupt evidence. Correct trade-off for durability,
  but an oversized payload would burn a live cell without a taxonomy
  verdict; keep payloads small or split rows.
* **W-A4 (inherited caveat):** freeze-chain ordering remains provable only
  up to single-machine timing; unchanged from round 0.
* **W-A5 (OPERATIONAL_DIAGNOSTIC):** pytest/numpy absent from the audit
  mount; installed by the auditor into `/tmp/opencode/pylibs` (outside
  tracked scopes), same as round 0. Suite results are the auditor's own
  executions.
* **W-A6 (tool scoping):** `runtime/repair_cycle3.py` embeds absolute
  pre-repair sha pins; `--check` will fail BY DESIGN after any legitimate
  future mutation of the five pinned artifacts. Intended tamper-evidence;
  the tool is cycle-scoped provenance, not living infrastructure.

## 4. Maximum defensible wording (integration ceiling)

> Repair round 1 (run 32933579869) resolves audit CYCLE_32928419260's three
> required fixes with zero changes to frozen outcomes, question, task set,
> thresholds, oracle or win rule: RF-1 is recorded as a false-positive
> audit finding (empirically refuted by independent reproduction; the
> requested hardening applied anyway with behavior verified identical and
> correctness no longer dependent on a seed coincidence); RF-2 is repaired
> in-harness (whole-note emission with round-trip assertion) with a
> deterministic, exact-prefix-verified provenance correction artifact that
> preserves the defective row; RF-3 is repaired via a surgical disclosed
> transform with mechanical timestamps going forward. The scientific
> headline stands exactly at its frozen ceiling: on the quotes-login goal
> class (one site family, one date, three live passes + one wrong-password
> negative control, one scripted stdlib implementation, zero browser
> launches) the mechanism-floor null is **FLOOR_VOID** — the environment
> accepts any credentials, so the direct-HTTP surface cannot discriminate
> credential validity; no substrate inference is licensed in either
> direction; substrate decision NO_SUBSTRATE_DECISION_VOID (repair-first);
> witnessed-effect addressing POC not triggered; `reuse_yield` UNDEFINED;
> no economics figure quoted; model independence unfalsifiable in this
> cycle. With this PASS, the provenance-layer corrections become
> AUDITED_DURABLE as corrections only; no outcome-tier claim is upgraded.

This equals the team's stated ceiling; the team exceeded it nowhere.

## 5. Provenance of this audit

* Base tip `917bbf8`; rejected snapshot `8e99234`; audited repair tip
  `89ffeba` (two commits). Delta vs base insertion-only (18 files).
* Auditor recomputations executed read-only against the team mount; mocks
  and clones under `/tmp/opencode`; no team artifact modified; no live
  HTTP by the auditor; pytest/numpy installed to `/tmp/opencode/pylibs`.
* Key auditor-owned reproductions kept at `/tmp/opencode/rf1repro/`
  (independent RF-1 refutation harness, old-vs-new behavioral identity).
* Gate JSON: `results/audit/CYCLE_32933579869_RUNTIME_GATE.json`.

— runtime_auditor, independent session, 2026-08-26.
