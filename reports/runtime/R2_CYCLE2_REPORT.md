# R2 CYCLE 2 REPORT — Decidable In-Canon Pagination Mechanism-Floor Null

Cycle: R2-2 (Program R2 "Inheritance Headroom & Mechanism Floor").
GitHub run: 32940627441. Branch: `cycle/runtime/32940627441/team`.
Prereg: `reports/runtime/R2_CYCLE2_PREREG.md` @ `e0ae931` (sha256
`6958b7ef5cabde8db86e311385a087cc152b6919d8acf53eb7fbaeab46f02c9e`,
committed 07:55:51Z BEFORE any live request of this cycle; priority-1
demand spec filed earlier at `ce70080`). This report is written at the
frozen ceilings and nowhere higher. All timestamps mechanical.

---

## 1. Headline verdict (exact frozen-gate ceiling — do not strengthen)

**FLOOR_DOMINATES at the frozen gates (decidable discriminator).** The
prereg §0 binding wording applies verbatim:

> "on BOTH frozen targets derived from committed entries plus one
> confirmation pass, ONE site family, ONE date, bare HTTP reached verified
> success in <=B_PG wire transactions AND discriminated the out-of-range
> control." Never "the pagination goal class", never "all k", never
> cross-site.

Observed under that ceiling: budgeted cells PG-K3F (`/tag/love/` →
`/page/3/`), PG-K9B (`/page/10/` → `/page/9/`) and confirmation PG-KCONF
(= K3F) each reached harness-verified success in **1 wire transaction
after the entry GET** (loads=1 per cell; B_PG=6 anatomy-derived); the
out-of-range control PG-NEGCTL-OOR (`/tag/love/` → `/page/1000/`)
returned HTTP 200 with a 3051-byte render carrying **zero**
`class="quote"` markers → judged `fail` via pinned failure-witness
branch 1 (`failure_witness_branch_1`, matched branch recorded in the
verify row). The full-success void-detector was evaluated FIRST per the
frozen judge order and did NOT fire (a success requires ≥1 content
marker; zero markers observed) — so this is a FED control, not a second
void. Zero browser launches; zero provider calls (model independence
UNFALSIFIABLE, auditor-confirmable from the stream).

This is MEASURED BACKING for Director stop-rule branch (b), scoped to
this cell class only. Recording branch (b) is a DIRECTOR action and was
NOT recorded by the runner (`r2_cycle2_state.json.substrate_decision.
stop_rule_branch_b = NOT_RECORDED_BY_RUNNER`). Login-class coverage of
any branch-(b) wording stays VOID-CAVEATED (R2-1 FLOOR_VOID decides
nothing). Witnessed-effect addressing POC: NOT_TRIGGERED (gated on
FLOOR_FAILS cells, which did not occur).

## 2. Mechanical gate application and integrity evidence

* Gates computed BY CODE from the event stream by the pre-frozen
  `runtime/gates_r22.py` (module sha256 `8fd7e85a…e79348a1`; driver
  `a346b8f8…4343bdb`; arm `18e1c0e6…ae07e03` — all four prereg pins
  byte-match the committed files).
* G-PG0 (P5' consistency) TRUE on all four cells; G-PGa TRUE (all three
  budgeted cells JUDGE_SUCCESS); G-PGn TRUE (control fed, tri-value
  honored); G-PGb → FLOOR_DOMINATES with sensitivity at B∈{1..6}
  DESCRIPTIVE ONLY (max steps 1 ≤ every B; never verdict-flipping).
* Independent recomputation this session: fresh
  `gate_pagination_cycle()` over `cost_events.jsonl` reproduces the
  committed analysis block DEEP-EQUAL (0 key mismatches);
  `verify_twin_identity` clean (25 logical rows × dual-name twins + 1
  PREFLIGHT row); `self_test()` decides all 9 fabricated branches
  correctly (dominates / fails_wellformed / void_soft200_mirror /
  negctl_unknown / health_trip / invalid_target / malformed_fail /
  invalid_arm / mnf_violation).
* Freeze order git-orderable: `fcbeaa2` accepted tip → `ce70080`
  demand spec → `a2bbaaa` harness+tests → `e0ae931` FROZEN prereg
  → outcomes. Witness receipt
  (`pagination_witness_derivation_r22.json`, mtime 07:56:29.006Z)
  predates even the authorized parity fetches (PREFLIGHT row
  ts 07:56:29.741Z) — offline self-check preceded ALL network traffic,
  exactly prereg §6 step order.
* Stream hygiene: exactly 10 wire transactions total (2 authorized
  parity GETs + 4 entry loads + 4 scored steps); driver truncates any
  pre-existing stream before emission (single uninterrupted pass; no
  retries exist under the frozen no-retry rule); `cell_ids()`
  dash-prefix assertion guarantees `collect_run` key isolation.
* Lane tests at outcome time: 216/216 pass (`pytest tests/runtime`,
  Python 3.12.3; 182 accepted lineage + 34 new hermetic tests).
  Audited modules byte-untouched (delta vs `fcbeaa2` is additive only).

## 3. Scope, X31 bookkeeping, and prohibitions

* Killer status: mechanism-floor killer (ii) moves VOIDED →
  **DISCHARGED FOR THIS CELL CLASS ONLY** via the fed-control
  DOMINATES. Killer (i) stands UNDISCHARGED (R1 K1 margin 0 vs
  strongest comparator). **X31 therefore still binds everywhere else:
  no compression phrasing leaves observation tier until BOTH killers
  discharge.**
* No SPIDER arm and no comparator arm ran on these targets. No margin,
  M=2 vocabulary, compression, speedup, novelty or reuse_yield claim
  exists at any tier (`reuse_yield` stays UNDEFINED; economics figures
  banned per W-R1-1/prereg §9). Wall-clock advisory only.
* Route-tier HTTP executor: REFUSED, unchanged. CTO-6 §3 flip
  conditions (Intel round-4 primary USEFUL AND parameterization-to-
  new-ids on a writable substrate AND capture-value-over-declaration >
  0 on spec-less SPA hosts) are untouched by this result — none of the
  three was exercised or satisfied here. The floor null remains a
  measurement arm only.
* Substrate: NO expansion licensed or claimed. Ruling R2-2-A covered
  same-host task additions only; Class A/B/C candidates await the
  two-gate path (Director family-membership ruling + Product/CTO
  demand input) exactly as filed in `R2_SUBSTRATE_DEMAND_SPEC.md`.
* Demand-spec supersession tag (honesty): spec §1.4 asserted "The
  discriminator itself is unfedable in-canon". The pagination outcome
  falsifies that sentence FOR THIS CELL CLASS — an in-canon decidable
  cell exists and decided. Spec §3's gating statement anticipated
  exactly this ("its verdict enters the Director's branch-(b) record
  as MEASURED backing scoped to that cell class"); reference §3, not
  §1.4, when consuming the escalation package. §1.4 text stands
  unmodified as history (no-amend discipline).
* Never-generalize list: not "the pagination goal class", not "all k",
  not books.toscrape.com or any second site, not "static sites", not
  "agents", not "the Web".

## 4. Total-overhead accounting disclosures (C4/W3 lineage)

1. Step counts count wire transactions AFTER the entry GET; true wire
   traffic per cell is entry load + steps (loads=1 in every row). The
   qualifier rides every externally quoted figure.
2. CONSTRUCTION_DECISION rows carry `latency_ms: 0.0` placeholders;
   construction overhead is assertable only by anatomy
   (`probing: none_by_construction`), never by a quoted number.
3. Budgeted-cell verify rows carry native eval ms (~0.04–0.05 ms,
   descriptive); the NEGATIVE-CONTROL verify row carries 0.0.
   Verification compute remains UNMEASURED globally (accepted C4
   lineage): no verification-cost or absolute-latency claim permitted.
4. Free site-model endowment (disclosed bias, AGAINST inheritance):
   construction templates, canonical netlocs and byte-exact pager
   tokens were derived OFFLINE from prior cycles' committed snapshots
   at zero measured cost to the floor arm. Legitimate for a floor null
   (deliberately strengthens the comparator side), but "construction is
   trivially sufficient" must not be generalized off static-canon
   cells whose conventions the snapshots already encode.
5. Decidability itself is environment luck bounded to this sample: the
   soft-200-empty behavior at `/page/1000/` is what made the control
   decidable on this date; a content-mirroring route would have
   auto-VOIDed. Sampled-scope observation only (see state-file note).

Pre-empted defect flag (BY DESIGN, prereg §3): the negative control's
gate record shows `well_formedness_reason: "transcript_incomplete"`
with taxonomy `FLOOR_FAIL`. Expected — the control bypasses
positive-path health floors BY CONSTRUCTION, so no well-formedness
transcript exists for it; its tri-value comes from the pinned-witness
decision path. No repair is owed; do not "fix" this.

## 5. Handoff for Runtime Director + Independent Auditor

* Audit entry points: frozen prereg (sha above), stream
  `results/runtime/r2_pagination/cost_events.jsonl`, results
  `results/runtime/r2_pagination/r22_floor_results.json`, lane-state
  `results/runtime/r2_pagination/r2_cycle2_state.json` (contains
  disclosed_post_run_edits E1/E2 applied PRE-commit while untracked:
  sampled-scope rewording of the route-totality note + generator
  provenance; originals preserved verbatim in-file), witness receipt
  under `results/runtime/probes/`.
* Director decisions now unblocked (not made by runner):
  record stop-rule branch (b) measurement-backed scoped to this cell
  class; treat escalation per filed demand spec (expansion vs loop-only
  productionization charter — Product/CTO authority).
* Binding notes carried into the next cycle are enumerated in
  `r2_cycle2_state.json.binding_notes_for_next_cycle` (X31 unchanged;
  URL-construction arms mandatory in any future strongest-comparator
  canon; two-gate rule for JS variants/new sites; W-A2 owed at next
  pilot.py/economics.py touch — untouched this cycle; W-4 http_floor
  registration owed at next schema-touching change — none occurred).
* Next high-information action: Director audit of THIS run, then the
  Program R2 stop/succession decision per `directives/RUNTIME.md`.
