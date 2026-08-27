# INDEPENDENT AUDIT — PHYSICS LANE, GitHub run 32866107906 (repair round 0)

Auditor: Independent Scientific Auditor (separate session, Physics lane).
Team snapshot audited: `cycle/physics/32866107906/team` @ `38e697b`
(worktree `/tmp/spider_physics_team`, clean tree, HEAD = team tip).
Accepted base at audit start: `lab/physics` = `d3afd9b`.
Audit method: adversarial recomputation from raw committed rows and git
objects with throwaway auditor code (`/tmp/opencode/audit_32866107906/`);
team scripts rerun in an isolated scratch copy; no team module imported by
auditor code.

---

## 0. What this cycle claims (one paragraph)

The run performs **zero environment interactions**. It (i) carries the
WP-006 evidence chain (H-ID identifiability-by-restart gate, verdict
**FALSIFIED**) bit-exact from the four-times-audited snapshots onto the
accepted lineage `d3afd9b`, which had received **no Director integration**
for two succession dispatches; (ii) re-verifies the chain in a fresh
environment; (iii) adds ONE new descriptive-only exhibit — tiered
shortfall bounds + instrument-seam signature checks; and (iv) packages the
pre-declared lane-termination decision input for the Lane Director. No new
confirmatory claim is made anywhere.

---

## 1. Claims checked, evidence, recomputation, status

### C1 — "26 WP-006 scientific files carried BIT-EXACT onto d3afd9b"

- EVIDENCE: commit `91eff06`; blobs compared across `HEAD`,
  `origin/cycle/physics/32860596387/team` (`76a1d72`), certified snapshot
  `45fa5db` (= `origin/cycle/physics/32799587656/team`).
- RECOMPUTATION: all 29 wp006-pathed files in HEAD are blob-identical to
  `76a1d72`; the 22 core files are additionally identical to `45fa5db`;
  the 4 stewardship-layer files unique to run 32860596387 are carried
  unchanged; 3 files are NEW this run (terminal-bound script + exhibit JSON
  + termination package). Ledger diff vs `d3afd9b`: **+156/−0, purely
  additive** (+112 carry, +44 ADDENDUM 2). Protected conceptual files
  (`SPIDER_MASTER_PROMPT.md`, `directives/PHYSICS.md`, `docs/NEXT_PHYSICS.md`,
  `state/*`, `.github/*`) unchanged vs `d3afd9b`. Control-plane sync commit
  `f64848b`: **all 67 paths verified byte-identical to main tip `92192ea`**,
  separated from scientific commits per standing advisory; lane-owned
  `directives/PHYSICS.md` correctly NOT overwritten by the stale main copy.
- STATUS: **VALIDATED_FOR_CURRENT_TEST**.
- MAXIMUM DEFENSIBLE WORDING: exact claim as stated.

### C2 — "Dataset integrity: sha256 manifest-matched, unchanged since result commit"

- RECOMPUTATION: `sha256(data/physics/wp006_trials.jsonl.gz)` =
  `fafd1cef46bb6b25…31149397` = manifest value = script constant; git blob
  `4480db2b…` identical at result commit `8d84196` and at HEAD. Row census:
  **1075 = 1 setup + 164 calibration + 910 trials; 704 valid / 206 invalid
  (action_failed 171, exception 22, state_match 13)** — reproduced
  independently. Freeze `aba6858` = 2026-08-24T21:30:49Z; minimum row
  timestamp 21:55:03.357Z ⇒ **0 rows predate the freeze** (recomputed).
  Original freeze/result commits reachable via historical refs
  `origin/cycle/physics/32776372437/{team,audit}`; disclosure `744cdd3`
  precedes freeze; both pre-outcome instrument repairs (`a5c5112`,
  `d8303d2`) precede first row with preserved pre-fix hashes.
- STATUS: **VALIDATED_FOR_CURRENT_TEST**.

### C3 — "Fresh-environment verification reproduces everything" (§3.3 of package)

- RECOMPUTATION (all rerun by the auditor in a scratch copy):
  1. `physics/team_recheck_wp006_run32860596387.py` → BOTH artifacts
     byte-identical to committed versions (diff empty ×2).
  2. Unmodified frozen `verify_wp006.py` with freeze timestamp argument →
     **PASS=true, own_verdict=FALSIFIED, verdict_agreement=true**;
     deep-diff vs stored v2 = exactly one key
     (`C3_rows_before_freeze_commit=0`, present because the freeze
     timestamp was passed as CLI arg — the disclosed advisory-A1/C10
     difference); deep-diff vs stored v3 = zero value differences, only
     the added `/provenance` block absent. Exactly as disclosed.
  3. New `terminal_bound_…py` → output **byte-identical** to the committed
     exhibit JSON; stdlib-only; grep confirms no `hash()` use and no
     random module import.
- STATUS: **VALIDATED_FOR_CURRENT_TEST**.

### C4 — Primary verdict inherited unchanged: "FALSIFIED at director floors"

- RECOMPUTATION FROM RAW ROWS with auditor's own from-prereg
  implementation (no team imports): verified BPs = books 12, quotes 12,
  saucedemo 7, parabank 5, internet 2 (**38**); producers {books, quotes}
  = **2**; F1 satisfied (8 sites attempted spanning static+stateful);
  F3 holds by construction (each verified BP has two cells ≥6 valid).
  Frozen mapping (prereg §2): hard gates pass, DATA_INSUFFICIENT triggers
  false, SURVIVES ⇔ F2∧F4 false ⇒ **FALSIFIED** — unique outcome.
  This matches team results, verifier, recheck, and all four prior gates.
- STATUS: **VALIDATED_FOR_CURRENT_TEST** (as an honestly-derived,
  quadruple-reproduced negative).

### C5 — DATA_INSUFFICIENT negation (exhibit §A)

- RECOMPUTATION: 8 sites have ≥1 calibration/trial row (first-row UTC
  timestamps in the exhibit spot-checked against raw rows, e.g. books
  21:55:03.357Z ✓); trial rows span classes {static, stateful} ✓;
  38 > 0 verified BPs ✓. All three frozen triggers false.
- Minor observation O1: field `spans_both_classes` is hardcoded `true`
  rather than computed; the adjacent computed `classes_attempted` field
  corroborates it. Non-blocking.

### C6 — Tiered shortfall bounds (exhibit §B): U_tot=50<60, U_prod=3<4

- RECOMPUTATION: tier0 38/2 ✓; tier1 = 38+12 = 50 total, producers
  {books,quotes,openlibrary} = 3 ✓; tier2 dead-arm-only 38+24 = 62 / 4 ✓;
  combined ceiling 38+24+12+(7−7)+(7−5)+(8−2)=82 / 5 ✓ (stateful headroom
  +8 recomputed). The openlibrary cap-truncation premise is real:
  `wp006_collection_status.json` records `HARD TIMEOUT after 2400s`.
- Observation O2 (wording, non-blocking): the tier-1 label
  "ADMISSIBLE-imputation bound" credits openlibrary up to its full planned
  +12 although openlibrary demonstrates **zero floor-meeting cells** (only
  4 valid trial rows; 3 BPs attempted before the hard timeout). Under a
  stricter admissibility rule the bound would be 38/2 — floors fail even
  harder. Because the credit direction is generous *toward survival* and
  still fails both floors, the conclusion "both floors fail in EVERY
  admissible world" is invariant under either reading and in fact holds
  a fortiori under the stricter one. No repair required.
- STATUS: **SURVIVES_AUDIT_WITH_LIMITS** (bounds correctly stamped as
  bounds; tier-2 correctly stamped INADMISSIBLE-COMPONENT-INCLUDED with no
  modal force).

### C7 — Instrument-seam signature checks (exhibit §C) — the strongest attack surface

This is where a dishonest team could have smuggled a rescue narrative or a
self-serving MEASUREMENT_INVALID upgrade. Audited hardest:

- C1 homogeneity: all **171** action_failed rows share ONE first-line
  exception class (`TimeoutError: Locator.click: Timeout 8000ms
  exceeded.`) ✓; distribution wikipedia|click_link#0 = 84,
  gutenberg|click_link#0 = 84, openlibrary|click_link#0 = 3 ✓. Stored
  error strings truncated at exactly 160 chars; the single distinct
  wikipedia string literally contains `locator resolved to <a href="#`
  (fragment-href skip-link anchor resolving, then timing out); the
  gutenberg/openlibrary strings cut before that line — exactly as the
  artifact states (truncation-limited inference honestly labeled).
- C2 zero-success: click_link#0 valid/attempts = books 84/84, quotes 84/84,
  internet 7/7, parabank 35/35, saucedemo 7/7 (**217 successes**),
  wikipedia 0/84, gutenberg 0/84, openlibrary 0/21 ✓.
- C3 sibling contrast: **24** dead-arm BPs; at ALL 24 the sibling
  click_button#0 cell holds exactly 7/7 valid while the dead arm is 0/7;
  state_match failures on wikipedia/gutenberg = **0** (all 13 corpus-wide
  state-match exclusions are openlibrary) ✓. Restart/state reproducibility
  was perfect on those strata; only the declared arm failed.
- Ordering probe: dead-arm failure uniform across replicate indices
  (12/site/rep, 168/168 failures) — no temporal/blocking transient ✓.
  Trial window 21:55:47Z–23:40:58Z matches ✓.
- Scope treatment: the seam finding is used to **bound** the claim
  (stratum-level scope collapse; wikipedia/gutenberg UNKNOWN, not refuted)
  — NOT to flip the verdict and NOT to relabel the measurement invalid.
  The frozen mapping gives no MEASUREMENT_INVALID route here: no hard gate
  G1–G10 covers declared-arm executability; V3 menu_ok passed honestly;
  failed clicks were recorded as honest invalid observations; >0 BPs were
  verified, so the DATA_INSUFFICIENT execution-failure trigger is false.
  Notably this is the anti-self-serving choice: declaring the seam a
  measurement defect would have been the escape hatch that keeps the lane
  alive; the team kept FALSIFIED ⇒ termination instead, and fenced the
  seam as descriptive with explicit wording limits (§6 MAY/MAY NOT).
- STATUS: **VALIDATED_FOR_CURRENT_TEST as descriptive signature analysis;
  scope-collapse wording is the maximum defensible wording.**

### C8 — Per-cell census (exhibit §D)

- RECOMPUTATION: 130 cells with trials; 100 ≥6 valid; 30 below =
  24 dead arms + 6 openlibrary cells (fantasy 0/7 & mathematics 1/7 &
  science 3/7 on click_button#0, plus three click_link#0 zeros) ✓;
  reading sentence accurate.
- STATUS: **VALIDATED_FOR_CURRENT_TEST** (verdict-inert integrity note).

### C9 — Audit-chain index and stop-condition provenance (package §5)

- RECOMPUTATION: all four referenced gate files exist on their audit
  branches: round 0 `REVISE` RF1–RF5 (`CYCLE_32776372437`), then
  `PASS, safe_to_integrate=true, required_fixes=[]` at rounds 1–3
  (`CYCLE_32793165981`, `CYCLE_32799587656`, `CYCLE_32860596387`) — read
  directly from the gate JSONs. The lane-termination condition is genuinely
  **pre-declared** in accepted base state, not manufactured post hoc:
  `directives/PHYSICS.md@ d3afd9b` ("PROGRAM STOP CONDITION
  (pre-declared): if H-ID fails … the Physics lane TERMINATES — no further
  program will be manufactured"), `docs/NEXT_PHYSICS.md` decision horizon,
  and `state/physics_loop.json.next_program.stop_condition` all agree.
  Prereg aba6858 itself freezes the falsification-closes-WP-004 consequence.
- STATUS: **VALIDATED_FOR_CURRENT_TEST**. The team explicitly claims no
  Director authority; integration, ledger adoption, `state/` rewrite and
  directive terminalization remain Director-owned proposals (§5.2), which
  is the correct authority boundary.

### C10 — Descriptive-only discipline / preregistration timing for the NEW exhibit

- The prereg's confirmatory extraction set {hard gates; three
  DATA_INSUFFICIENT triggers; SURVIVES ⇔ F2∧F4} is fully evaluated —
  exhaustion claim verified against prereg §2. D1–D5 were frozen
  descriptive and were extracted in prior audited cycles. The new
  terminal-bound/seam analysis is post hoc but is labeled DESCRIPTIVE ONLY
  everywhere it appears (script docstring, artifact
  `artifact_class`, ledger ADDENDUM 2, report §4), uses no inferential
  statistic, consumes no CI, and carries an explicit
  `downstream_use_forbidden` fence (no floor recalibration, no
  re-collection justification, no verdict alteration). Nothing fitted
  anywhere (G6 vacuous, confirmed). This complies with constitution §19
  (post-outcome analyses are exploratory and may not feed confirmatory
  claims) — they do not.
- Uncertainty level (directive item 6/18): primary inference remains exact
  counts vs frozen floors; no CI is consumed anywhere in this run; the
  small-cluster descriptive-only rule (P3) is respected by construction.
- Resampling-unit discipline (directive item 17): moot this run — no
  resampling performed; all quantities are exact row/BP counts.
- Verifier independence (item 16): respected and preserved — verifier,
  fn-control and recheck are stdlib-only with own reference paths; the new
  exhibit imports nothing from team analysis modules; the auditor's own
  code path reproduced all numbers.
- STATUS: **VALIDATED_FOR_CURRENT_TEST**.

### C11 — Representation integrity / raw-observation losses

- Carried riders honestly restate known representation boundaries:
  ephemeral raw DOM (/tmp policy), executor-relative atomicity (action row
  keys verified: error, ok, ordinal, primitive, primary, target,
  target_kind, value — no retry counter), client-fresh vs server-side
  session state, lost openlibrary BP manifest. Session/carryover coverage
  recomputed: assertions present on 196/196 stateful rows, 0 failed among
  valid; calibration precedes trials per BP with 0 violations.
- STATUS: **SURVIVES_AUDIT_WITH_LIMITS** (limits disclosed in-artifact).

## 2. Failure modes tested and NOT found

Target/post-state leakage into the new exhibit (none — exhibit computes
from validity flags, error strings, cell labels and timestamps only);
hidden site/task identity effects on any count (counts are per-site
explicit); denominator/matched-comparison errors (all six headline tables
recomputed exactly); degenerate frequency nulls presented as strength
(none presented — no nulls consumed at all this cycle); policy-vs-
environment confusion (moot — no dynamics claim made or inherited beyond
the scoped falsification); seed nondeterminism (no RNG anywhere in the
new code — byte-reproducible output verified twice); silent history edits
(none — additive diffs only; prior artifacts byte-preserved); floor
loosening (grep-level and semantic check: none; floors quoted verbatim);
post-hoc confirmatory laundering (fences verified in artifact, ledger and
report); self-serving verdict escape hatch (explicitly declined — see C7).

## 3. Corrected interpretation

None required. The snapshot's interpretation IS the corrected one: WP-006
H-ID is FALSIFIED at the director floors as preregistered; the miss
decomposes into 24 BPs blocked by a classifier×executor composability seam
on hidden-anchor slots (wikipedia/gutenberg restart reproducibility
UNKNOWN, not refuted), ≤12 openlibrary BPs lost to wall-clock truncation,
and stateful sites planned below the producer bar by design; even maximal
admissible recovery (U_tot=50<60, U_prod=3<4) leaves both floors failing.
The negative is real, quadruple-audited, and now correctly positioned on
the accepted lineage so the pre-declared termination decision can be taken
by the Lane Director.

## 4. Required fixes

None. No same-cycle repairable defect was found. Observations O1–O3
(hardcoded boolean corroborated by adjacent computed field; generous
tier-1 "admissible" label whose conclusion is invariant under the stricter
reading; evidence-chain commits reachable via historical refs rather than
ancestry of the carry lineage — content provenance established by blob
identity, consistent with the workflow's validated carryforward pattern)
are recorded as provenance notes and require no action.

## 5. Safety to integrate and gate

The Lane Director may safely consider this snapshot. Integrating it does
not create knowledge beyond what the four previous PASS gates plus this
audit certify: a bit-exact-carried, fresh-environment-reproduced,
honestly-bounded FALSIFIED verdict, plus one deterministic descriptive
exhibit whose every number the auditor reproduced independently.

**INTEGRATION GATE: PASS** (`safe_to_integrate=true`). A correctly
represented negative result passes. The termination decision itself belongs
to the PHYSICS LANE DIRECTOR alone; this audit expresses no view on whether
the lane should terminate, only that the decision input is now valid,
complete and uncorrupted.

— Independent Scientific Auditor, run 32866107906 audit, repair round 0.
