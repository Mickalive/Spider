# INDEPENDENT AUDIT — RUNTIME CYCLE 32908002333 (R0-2, repair round 0)

Auditor: runtime_auditor (independent session). Date: 2026-08-26.
Team snapshot audited: `/tmp/spider_runtime_team` — verified byte-identical to
pushed `origin/cycle/runtime/32908002333/team` == `.../team-attempt-1` ==
commit `613fbd4b…` (full-tree diff empty).
Accepted base: local checkout `runtime-audit-base` @ `9dc50ba` (Director
integration of audited R0-1, run 32887030457), untouched during this audit.
Sandbox copy used for all execution: `/tmp/opencode/rt_audit_c2/snap`
(mounted tree left pristine; no file outside the mount and the two audit
deliverables was created or modified — a transient git worktree used for the
tree comparison was removed immediately after use).

Prior-cycle binding inputs: warnings W1–W9 of
`reports/runtime/AUDIT/CYCLE_32887030457_RUNTIME.md`, all dispositioned by
the team in `state/runtime_loop.json`; dispositions re-verified below.

## Provenance and freeze verification

| check | result |
|---|---|
| mounted tree vs pushed branch tip | identical (`diff -rq` empty) |
| freeze ordering (W4) | **git-auditable**: `8ed968d` harness code (23:44:04Z) → `42eb66d` FROZEN prereg + probe evidence (23:44:21Z) → `e172e16` outcomes (23:56:48Z) → `613fbd4b` disclosure. Prereg+probes content at `42eb66d` byte-matches the mounted files |
| `prereg_sha256` pin | `9d07d391…24e3e` recomputed from file bytes; matches `pilot_results.json` |
| input dump sha256 | `ec5af9e1…05e7073` recomputed; matches R0-1 pin |
| accepted parent registry untouched | byte-identical to base (`results/runtime/capsules/**` unchanged); derive.py untouched (absent from all diffs) |
| commit-scope disclosure | `8ed968d` flushed 18 environment-staged V3 control-plane documents into the lane branch; receipt `R0_CYCLE2_COMMIT_SCOPE_DISCLOSURE.md` matches git reality exactly (warning W-C2-4) |

The W4 defect of R0-1 is genuinely closed: the frozen instrument existed as
a pushed commit before any live outcome row existed.

## Claim-by-claim recomputation

### C1 — "Exact-repeat PARITY replicated ×2 (4v4 actions / 3v3 loads), reused 4, novel 0"

- EVIDENCE: rows `RT2-C1-*` in `results/runtime/pilot2/pilot_results.json`;
  raw stream `cost_events.jsonl`.
- RECOMPUTATION: independent recount from schema-filtered stream (twins
  deduped): BASE 4 actions/3 loads/success, SPIDER 4/3/success on both
  passes; SPIDER actions are 4 `runtime_inherited` steps of segment seg-0,
  novel 0; `steps_len=4` pinned from APPLICABILITY_PASS rows equals reused.
  Entry digests equal within passes (`395f96f5…`). P1–P5 trail predicates
  hold under my independent implementation.
- FAILURE MODES TESTED: double counting (actions/loads disjoint; twin
  rule enforced; summary↔stream cross-check mechanical), stale reuse
  (freshness null but staleness handled structurally via host mutation →
  ABSTAIN and signature-churn → UNRESOLVED_STEP paths pinned in tests),
  self-grading (both arms judged by the same vendored predicate dialect,
  harness-side).
- STATUS: **SURVIVES_AUDIT**.
- MAX WORDING: unchanged from R0-1 — parity on lexically transparent exact
  repeats; inheritance does not beat exploration there.

### C2 — "Stale wrong-host ×2: clause-attributed ABSTAIN → zero pre-handoff actions → valid plan/v0 handoff → 1-novel-action caller repair → RESOLVED → verified success vs truthfully-recorded BASE budget exhaustion"

- RECOMPUTATION: ret1 ABSTAIN with failed_clauses
  `[{host_allowlist,fail},{elem_text_any,fail}]`; handoff note echoes the
  identical attribution (`plan_validated=true`, `validator_errors=[]`,
  `spider.plan/v0`); zero spider action rows precede handoff; caller goto
  charged as 1 novel action; ret2 RESOLVED; 4 inherited + 1 caller;
  harness verdict passed. BASE: 60 actions/51 loads/fail on both passes,
  verify rows honestly `passed=false`, host-fail check present iff final
  host off-allowlist (G-C2c mutual consistency holds). Replicated p1+p2.
- FAILURE MODES TESTED: hidden answer leakage — the R0-1 leak (caller fell
  back to a hardcoded default target) is **gone**: the blinded-caller path
  has NO default target anywhere; absent usable hint ⇒ UNACTIONABLE with
  zero navigation (proven live by ABL A1, below). Internal-ID dependence:
  the caller consumed ONLY `hint.params.expected_host`; capsule_id/sha
  exposure remains legitimate content-addressed provenance (W6 scope).
- STATUS: **SURVIVES_AUDIT** (failure-avoidance illustration only; no
  speedup wording used anywhere).
- MAX WORDING: as reported — clause-attributed abstain, valid handoff,
  single-novel-action repair, replicated twice; never a speedup.

### T3 — NEAR-REPEAT KILL CELL: "work-compression OBSERVATION — 11 vs 4 actions on BOTH offset entries (/tag/love/, /page/10/), margins 7≥M=2 per pass, aggregate 8 ≤ 22−4, zero novel decisions"

- EVIDENCE: rows `RT2-T3-*`; stream trajectories; prereg §3/§7 frozen
  construction rule and gates; pre-outcome probe
  `results/runtime/probes/t3_offline_rank_probe.json`.
- RECOMPUTATION (fully independent recount):
  BASE p1/p2 = 11 actions/7 loads/success each; SPIDER p1/p2 = 4/3/success,
  reused 4 (= pinned steps_len), novel 0; per-pass margins 7 and 7 ≥ M=2;
  aggregate 8 ≤ 18; not discordant; not base-capped (max 11 < 60);
  compression_observation_eligible=True reproduced from raw stream.
  Trajectories match the report narrative: BASE wanders via brand/tag links
  (acts 1–7: quotes-to-scrape ×3, tag/be-yourself ×3, be-yourself) before
  reaching `a|||||login` at act 8, then form; SPIDER replays click-login →
  fill → fill → submit directly. Entry digests differ across the two
  entries (`b66af808…` vs `96d2c4a5…`) and match within every arm — offset
  robustness, not single-context luck.
- CONSTRUCTION INTEGRITY: goal text contains no anchor substring
  (machine-checked pre-batch; recomputed: keywords {access,your,quotes,
  toscrape,account,public,demo,credentials,complete,site,sign,form}, none a
  substring of "login"//"login"); retrieval resolves on demand/effect keys
  only ({quot,toscrape,form}=3 pairs, coverage 0.50 ≥ τ=0.30, pairs ≥
  mm=2 — arithmetic reproduced against `retrieval.tokenize/_eq`);
  information symmetry holds (both arms receive the same goal text; only
  the ROUTE is inherited, which is precisely the tested hypothesis).
  The offline rank probe predicted top-choice = brand link and
  login_is_top=false on both entries — consistent with the observed BASE
  wander — and is correctly tiered OPERATIONAL_DIAGNOSTIC ("predicts
  intent, not the full live trajectory").
- FAILURE MODES TESTED: baseline strength — BASE is the frozen Graph-lineage
  memory-free greedy explorer, policy untouched this cycle (diff verified:
  additive telemetry only), and its DOM-order luck is declared pre-outcome;
  lexical transparency is excluded by construction, so this cell isolates
  route-finding. Stale hits: capsule derived 2026-08-24, replay executed
  2026-08-25 against live snapshots bounded by preflight digests +
  applicability PASS on entry. Metric double counting: none found —
  reused ⊂ actions presented consistently, loads separate, gates consume
  stream counts only. Expensive verification: verifier compute max
  0.082 ms, resolve() max 0.565 ms, applicability max 0.063 ms — all
  natively timed in-stream; walls live only in maintenance rows.
- LIMITS (all disclosed, all respected in wording): single task, single
  site template family, two passes; magnitude unquoted; ratios (0.36)
  reported as numbers only; wall-clock advisory (≈5010 ms vs ≈1723 ms);
  multi-task replication and ≥3-sample statistics owed.
- STATUS: **SURVIVES_AUDIT** as an OBSERVATION-tier result at the exact
  prereg ceiling. This is the program's first gate-passing compression
  observation and it survives adversarial recomputation.
- MAX WORDING: exactly the headline of `R0_CYCLE2_PILOT.md` — nothing
  stronger ("strictly fewer browser actions than the memory-free baseline,
  replicated across both offset-entry passes … a work-compression
  OBSERVATION at pilot scale").

### ABL A1 — hint causality: "stripped five-channel hint ⇒ UNACTIONABLE with ZERO actions ⇒ hint CAUSAL within this caller implementation"

- RECOMPUTATION: `strip_hint()` removes expected_host, hint.params.
  capsule_id, both clause-detail channels, and segment id/sha channels;
  validate_plan green post-strip; blinding scan (echo fields masked)
  reports zero leaks of {quotes/books.toscrape.com, toscrape, login,
  /login, quot}; run recorded UNACTIONABLE with 0 action rows (loads=1 =
  entry prime only). Frozen gate: A0 success with 1 novel AND (A1
  UNACTIONABLE-zero OR A1_novel ≥ A0_novel+2) ⇒ causal=true. Reproduced.
- STATUS: **SURVIVES_AUDIT** with the disclosed sufficiency-vs-necessity
  ceiling inside THIS caller implementation. R0-1 warning W2 is closed.

### GATE INTEGRITY and the POST-HOC GATE-REPAIR ADDENDUM

- FACTS: the frozen instrument's driver printed G-C1a/G-C2b/G-T3a=false
  with six "predicate_ref mismatch" derivation errors at run time. The
  original analysis IS preserved verbatim in `pilot_results.json`
  (`analysis.gates` shows the three false gates; `derivation_errors` lists
  exactly six SPIDER-row ref mismatches). The outcomes commit then modified
  `runtime/gates.py::_harness_verdict` to accept an ACCEPTED REF SET
  {task id, witness ref} for the SPIDER row only, documented in
  `POST_HOC_GATE_REPAIR_ADDENDUM.json`.
- AUDITOR VERIFICATION OF LEGITIMACY:
  1. The two refs name BYTE-IDENTICAL clause bodies: task predicate
     `{host_allowlist:[quotes.toscrape.com], url_anchor:null,
     elem_text_any:["logout"], neg_url:null}` ==
     capsule `expected_effects[0].witness_predicate.predicate`. The
     witness ref `graph.tasks:T_Q_login.accept` predates this cycle
     (present in both accepted R0-1 capsule artifacts in the base).
  2. The judge is arm-independent (harness-side vendored dialect over the
     final snapshot + nav chain; verifier compute natively timed).
  3. I reproduced BOTH wirings from the same committed stream: repaired →
     all ten gates TRUE, zero derivation errors; original wiring → exactly
     the three false gates of the preserved live analysis.
  4. No outcome row, cell, threshold, benchmark or question changed; the
     defect direction was AGAINST producer interest (gates false), which
     is the strongest available honesty signal.
- CLASSIFICATION: labeled instrumentation repair under the V2 same-cycle
  repair rule (code stricter than the frozen text, loosened toward it),
  NOT post-hoc benchmark movement. It does however mean gate-code v2 never
  existed before outcomes (warning W-C2-3).
- STATUS: **SURVIVES_WITH_DISCLOSURE**.

### WRITE-BACK PRIMITIVE (priority 3) and maintenance overhead

- VERIFIED: 7 observation records (6 VERIFIED_OUTCOME + 1 HANDOFF) — every
  `record_id` reproduces under the pinned exclusion-hash convention;
  `validate_observation` green; step `value`s structurally null (schema
  pins const null + defense-in-depth check); ts_utc copied from source
  verify rows (spot-checked); HANDOFF carries neither verdict nor abort.
  Successor `runtime/form-login-procedure-wb@v1`: CANDIDATE-only, disjoint
  `-wb` registry, mechanism copied VERBATIM via manifest join, value-token
  hygiene holds (spiderbot/notasecret absent from semantic_keys),
  freshness.last_verified_at measured, cost fields measured-or-null,
  confidence.value=null with stated basis. Duplicate-key dominance rule
  implemented and correctly reported as NOT fired. Parent registry
  untouched.
- FINDINGS (warnings, not blockers):
  - **W-C2-1 (maintenance accounting gap)**: prereg §9 promised write-back
    persistence cost "disclosed separately (maintenance accounting)" but no
    number exists anywhere — `tools/writeback_run.py` has no timing
    instrumentation; manifest/report/state contain none. No claimed number
    rests on it (write-back is excluded from cells, so no double
    counting), but the V2 economics vector requires storage/update
    overhead measurement before write-back ever becomes default-path.
  - **W-C2-2 (wb precondition breadth + doc/code mismatch)**:
    `derive_successors` docstring says hosts come from "where verification
    PASSED", but the code takes ENTRY-url hosts; C2 records have books
    entry with the effect witnessed on quotes, so the successor precondition
    asserts `books.toscrape.com` though the effect was never witnessed
    there. Bounded today (CANDIDATE quarantine + conjunction with
    elem_text_any login + the explicitly OPEN Director/CTO question about
    observations as applicability-boundary evidence), latent
    stale/false-positive reuse risk if it ever becomes trusted.
- STATUS: **SURVIVES_WITH_LIMITS**.

### Retrieval policy (W5), tests, hermeticity

- Probe suite recomputed: TP recall 1.0, TN leakage 0, one disclosed
  near-miss (format~form+text) at inherited (τ=0.30, mm=2); frozen decision
  rule keeps inherited constants; committed at `42eb66d` BEFORE outcomes;
  benchmark texts excluded by construction.
- Tests: runtime suite **58/58 pass** in auditor sandbox (pytest,
  Python 3.12) — matches the claim exactly (golden derive regression,
  gates incl. ref-set semantics, probes, writeback, ablation/blinding,
  DOM-mutation/host-norm).
- Note: shared `tests/test_integrity.py` has one failing Physics-lane guard
  that fails IDENTICALLY on the untouched base checkout — pre-existing,
  outside Runtime scope, flagged here for the Physics lane owner only.
- Registry-level resolution honesty: scored diagnostics show both capsules
  at identical coverage in every retrieval; selection is lexical
  capsule_id tie-break among byte-twins; "ranked the right capsule"
  claimed nowhere. Model independence remains UNFALSIFIABLE (zero provider
  calls anywhere — confirmed).

## Verdict

Every material headline number was independently recomputed from the raw
event stream and matches. The freeze is git-orderable and the prereg hash
pins reproduce. The near-repeat kill cell survives adversarial
recomputation as an OBSERVATION-tier work-compression result obtained
exactly where R0-1 predicted it must be sought, with honest parity retained
on transparent repeats and truthful failure recording elsewhere. The one
post-outcome event — the gate-repair addendum — was verified legitimate,
interest-reversing, and fully disclosed, with the original analysis
preserved. Write-back discipline holds at CANDIDATE tier in a quarantined
registry; its maintenance cost is disclosed-but-unmeasured (W-C2-1) and its
derived precondition breadth is flagged (W-C2-2). No required fix blocks
integration at the stated ceilings.

GATE: **PASS** — safe to integrate with the exact wording of
`reports/runtime/R0_CYCLE2_PILOT.md` and
`state/runtime_loop.json::results_summary_at_prereg_ceilings`.

Warnings W-C2-1…W-C2-5 below are binding inputs to the next Runtime cycle
design (they gate any strengthening of wording or promotion of wb
artifacts); they do not alter this cycle's claims.
