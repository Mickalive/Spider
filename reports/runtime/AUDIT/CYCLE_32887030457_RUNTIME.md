# INDEPENDENT AUDIT — RUNTIME CYCLE 32887030457 (R0-1, repair round 3)

Auditor: runtime_auditor (independent session). Date: 2026-08-25.
Team snapshot audited: `/tmp/spider_runtime_team` (byte-identical to pushed
`origin/cycle/runtime/32887030457/team` == `.../team-attempt-2` ==
commit `f2178e45c68027310014d703b4bf84c13cf3b74f`, tree `824325ab11f8e8c7…`).
Accepted base: local checkout `runtime-audit-base` @ `7669dcd` (workflow YAML
only, zero Runtime artifacts — team's own pre-cycle description confirmed).
Sandbox copy used for all execution: `/tmp/opencode/rt_audit_r3/snap`
(mounted tree untouched).

Prior lineage: runs 32864270667 / 32875577618 / 32877702179 resubmitted the
byte-identical tree `44cda5fd` (commit `af164b9`) and were BLOCKED at repair
round 2 pending an external/orchestration decision. Run 32885208777 (never
audited) still carried the old architecture. Run 32887030457 attempt-1
(`c2f0ba8`, 20:22Z) was a derivative of that old line; attempt-2 = final
(`f2178e4`, 22:15Z) is a **restart**: a fresh minimal build with a new frozen
prereg (`R0_CYCLE1_PREREG.md`). The previously frozen six-W R0 instrument was
never executed and is abandoned without an explicit supersession record
(warning W7). No outcomes ever existed under the old prereg, so this is not
post-hoc benchmark movement.

## Provenance verification

| check | result |
|---|---|
| mounted tree vs pushed branch | identical (`git diff` empty for team and team-attempt-2) |
| `prereg_sha256` in pilot_results | `6b8b10ba…76bd6f` — recomputed, matches file bytes |
| input dump sha256 | `ec5af9e1…05e7073` — recomputed, matches pin and prior-cycle pin |
| capsule canonical sha ↔ index ↔ filenames | both capsules reproduce byte-identically via `derive.derive_capsules` + `canonical_sha256` (recomputed live) |
| freeze ordering | NOT git-auditable: prereg + code + outcomes in the single commit `f2178e4`; only the self-recorded run-start hash ties them (warning W4) |

## Claim-by-claim recomputation

### C1 — "Exact-repeat cell: action/load PARITY (4v4), novel decisions 0v4; compression withdrawn"

- EVIDENCE: `results/runtime/pilot/pilot_results.json` rows `RT0-C1-*`;
  event stream `cost_events.jsonl`.
- RECOMPUTATION: BASE 4 actions / 3 loads / success; SPIDER 4 actions
  (reused=4, novel=0) / 3 loads / success. `repeat_cost_ratio_actions=1.0`,
  `reuse_yield=0.0` degenerate-by-frozen-formula (disclosed naming pathology
  in POST_HOC_ADDENDUM). Wall 1607 vs 1611 ms.
- FAILURE MODES TESTED: double counting (loads/actions disjoint across
  prime/caller/plan; twins share row_id, filter-by-one-schema rule enforced);
  lexical transparency of the task for the greedy baseline (disclosed by the
  team itself as the reason parity, not compression); budget symmetry
  (BASE MAX_CLICKS×2=60 cap unused at 4 actions; SPIDER executor max_steps=64
  unused).
- STATUS: **SURVIVES_AUDIT**. Withdrawing the prereg §7 "work-compression"
  phrasing against producer interest is exactly the honesty the gate exists
  to protect.
- MAX WORDING: "action/load parity with zero inherited-arm novel decisions on
  a lexically transparent exact-repeat task; no compression demonstrated."

### C2 — "Stale/wrong-context: clause-attributed ABSTAIN before any browser action → valid plan/v0 handoff → caller repair → verified success vs budget-failed baseline"

- EVIDENCE: rows `RT0-C2-*`; raw file order in cost_events.jsonl:
  `ret1 → handoff(plan/write_guard) → caller(browser/action) → ret2 →
  act1..act4 → verify → rep`.
- RECOMPUTATION: first_decision=ABSTAIN with per-clause attribution
  (host_allowlist fail + elem_text_any fail on books home); zero
  CountingSession acts before handoff (assertion held; event order confirms);
  handoff plan validated at runtime (`validate_plan`); caller goto charged as
  1 novel action; second resolve RESOLVED; 4 reused actions; harness verdict
  pass. BASE truthfully recorded fail at its full 60-action / 51-load budget.
  Wall ratio ≈13.5× exists in raw data and was correctly refused as a quote.
- FAILURE MODES TESTED: hidden answer leakage — **found one**: the pilot's
  caller falls back to hardcoded `URL_Q_HOME` when the plan hint were absent
  (pilot.py:374–378), so hint *causality* for caller success is undemonstrated
  (sufficiency is demonstrated; the counterfactual no-hint arm does not
  exist). The report already forbids quoting magnitude and names the
  conflation, so no reported number depends on the leak; wording stays inside
  its ceiling (warning W2). Stale hits: freshness fields null, TTL machinery
  refused; staleness triggered deterministically by host mutation; preflight
  digests equal SPIDER entry digests (`395f96f5…`, `569f5535…`) bounding
  within-run DOM drift. Fallback correctness: executor refuses NOVELTY_GAP
  execution (test), UNRESOLVED_STEP/no-effect abort paths present.
- STATUS: **SURVIVES_AUDIT_WITH_LIMITS**.
- MAX WORDING: "observable clause-attributed abstain with zero prior browser
  actions, valid spider.plan/v0 handoff, and verified success after a
  single-novel-action context repair; a failure-avoidance illustration, never
  a speedup or hint-causality claim."

### C3 — Gate integrity

- G-C1a/b, G-C2a/b/c: independently recomputed TRUE from rows/events.
- **G-C1c is hardcoded `True`** in pilot.py:472 ("trail audited post-hoc").
  The durable trail supports it under the defensible reading (one
  applicability-pass retrieval event precedes all four actions; zero silent
  execution; refusal test green), but there are NO per-action applicability
  events, and the driver did not compute the frozen gate text mechanically.
  Same class: G-C2c operationalized as `isinstance(bool)` (trivially true).
- STATUS: **SURVIVES_WITH_WARNING** (W1): outcomes correct, computation
  method must become mechanical next cycle.

### C4 — Accounting honesty (retrieval/applicability/verification/recovery/maintenance overhead)

- Retrieval+applicability latency measured natively around `resolve()`
  (incl. registry reads): 0.54 ms C1, ~0.89 ms C2 total; warm-process
  exclusion disclosed. Recovery overhead charged where incurred (caller goto
  = 1 novel action + load inside SPIDER wall). llm/token fields null-not-zero;
  integer flooring absent (float latencies verified); 176/176 rows validate
  under `spider.cost_event/v0` incl. additive-default-null rule.
- Gaps found: verification COMPUTE unmeasured (count=1/row only, addendum-
  recomputed); verify-stage events mislabel `latency_ms` (SPIDER verify rows
  carry retrieval ms, BASE verify row carries whole-arm wall ms) — cosmetic
  but must be fixed before any verification-cost claim (W3). Maintenance =
  summary_event/report path exercised; registry index update trivial,
  unmeasured, immaterial at n=2.
- STATUS: **SURVIVES_WITH_LIMITS** — no quoted number rests on an unmeasured
  component.

### C5 — Internal-ID independence and leakage surface

- Consumer contract honored in the need-sense: caller acted on
  `hint.params.expected_host` alone; goal_sig values absent from plans/events
  (grep clean); credentials absent from the committed event stream (grep
  clean; public demo creds anyway); no kb:// or store-path tokens.
- Plans DO expose `capsule_id` + `capsule_version_sha256` (content-addressed
  provenance) and the handoff note exposes `capsule_id`. Keep "ID-free"
  phrasing scoped to *need-sense*, not absence (W6).
- Semantic keys nuance: `intent.semantic_keys` derive upstream from Graph
  fragment descriptions that encode mechanism-step vocabulary ('btn',
  'form-control', …). The R0 restriction (scoring consults semantic_keys
  ONLY, never steps/values) is real, tested (`test_goal_sig_and_steps_values_
  stripped_invariance`), and fill VALUES are absent from keys — but "route
  leakage structurally impossible" must be read query-time-only (W5). At n=2
  with byte-identical key sets and step sequences, ranking discrimination is
  untested (team disclosed).

### C6 — Evidence-tier discipline

- Both capsules status=CANDIDATE; validator enforces VALIDATED_POC
  production ceiling (negative fixture present); unmeasured fields null;
  derivation provenance complete; expected effects trace to Graph's own
  acceptance predicate. Model-independence declared UNFALSIFIABLE rather
  than claimed. No tier inflation found anywhere.
- STATUS: **VALIDATED_FOR_CURRENT_TEST**.

### C7 — Tests and hermeticity

- 23/23 pass in auditor sandbox (pytest 9.1.1, Python 3.12.3): schemas,
  tier ceiling, null-tolerance, dual-name identity, dialect semantics,
  UNKNOWN-not-forced-hit, wrong-host abstain, executor refusal, offline loop,
  foreign-executor materialization parity, tie-breaks, content addressing.
- Non-hermeticity of the old cycle is gone: test run mutates nothing committed
  (only `__pycache__`). Old defect patterns absent (no `ch["capsule"]`, no
  constant verify_ms, no host-absolute paths in committed artifacts).

### C8 — Attempt history / negative knowledge

- Attempt-1 preserved: BASE looped to 862 actions producing rcr=0.0046 /
  reuse_yield=858 — discarded AGAINST producer interest as a baseline-only
  defect (key-shape mismatch), matching the addendum account and now scoped
  negative knowledge. Attempt-2 preserved: valid outcomes, missing SPIDER
  wall_ms telemetry. Final = attempt-3. Post-hoc recomputations confined to
  labeled addendum. Ledger/handoff/status filled and consistent
  (`state/runtime_loop.json`: CYCLE_COMPLETE_PENDING_INDEPENDENT_AUDIT —
  accurate).

## Verdict

Every material headline number was independently recomputed from the raw
event stream and matches. All six frozen gates are true under auditor
recomputation (two of them verified manually because the driver asserts
rather than derives them). Wording ceilings were respected, including a
self-initiated withdrawal of the prereg's compression phrase. Residual
findings are measurement-mechanics and process items (warnings W1–W9) that
do not change any reported number or claim. Nothing blocks integration.

GATE: **PASS** — safe to integrate with the exact wording of
`reports/runtime/R0_CYCLE1_PILOT.md` + `docs/RUNTIME_LEDGER.md`.

Warnings W1–W9 are binding inputs to the next Runtime cycle design, not
optional commentary; W1/W2/W3 in particular define what cycle 2 must
mechanize before any strengthening of wording.
