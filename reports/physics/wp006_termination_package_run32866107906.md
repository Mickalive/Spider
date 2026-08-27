# WP-006 TERMINATION PACKAGE & TEAM REPORT — Physics lane, GitHub run 32866107906

Team Physics (physics_runner), program `within-site-dynamics-interventional`,
succession/recovery dispatch cycle index 1. Date: 2026-08-25.
Base checkout: accepted `lab/physics` at `d3afd9b` — the authoritative
accepted lane state. Human steering note handled strictly subordinate to
`SPIDER_MASTER_PROMPT.md` and `directives/PHYSICS.md`; it is not a demand for
a positive result.

---

## 0. One-line status

The WP-006 primary verdict is **inherited unchanged: FALSIFIED at the
declared director floors** (prereg `aba6858`, applied exactly once),
measurement validity **VALID_FOR_CURRENT_TEST** per a four-audit chain whose
final three gates returned `PASS, safe_to_integrate=true, required_fixes=[]`.
This run performs **zero environment interactions** and adds no confirmatory
claim; it completes transmission integrity so the audit→Director termination
chain can finally execute.

## 1. Factual state at team start (all git-verifiable)

1. WP-006 H-ID was executed on live websites (runs 32776372437 → 32793165981
   → 32799587656): dataset `wp006_v1`, 1075 rows, 8 sites attempted spanning
   static+stateful, 704 valid trials; verified matched branch points books 12,
   quotes 12, saucedemo 7, parabank 5, internet 2 = **38 (<60, F4 FAIL)**;
   producer sites {books, quotes} = **2 (<4, F2 FAIL)** ⇒ FALSIFIED by the
   frozen mapping.
2. Independent audits: round 0 REVISE (RF1–RF5, decomposition defects only,
   primary verdict unaffected) → repaired additively → **PASS**
   (`CYCLE_32793165981`) → carried bit-exact, reproduced fresh-env, advisory
   closed → **PASS** (`CYCLE_32799587656`, snapshot `45fa5db`) → stewardship
   snapshot of run 32860596387 → **PASS** (`CYCLE_32860596387`).
3. **No Lane Director integration followed any of this**: `lab/physics` still
   sat at `d3afd9b`. This is the operational failure anticipated by the
   steering note ("a prior successor may have failed operationally"); it has
   now repeated across two succession dispatches.

## 2. Why THIS run performs no live collection (scope ruling)

Endorsed by the Physics CTO and both challenge specialists
(identifiability/statistics; intervention red-team) before any execution:

- Re-running collection at unchanged floors is a **multiple-look retry** of a
  threshold-crossing statistic under genuine sampling noise (optional-
  stopping/forking-paths), against a verdict application the prereg freezes
  "exactly once". Floors may be tightened, never loosened, so an honest re-run
  could only re-fail or raise the bar.
- Re-running with a modified slot/action-declaration instrument would be a
  **new program wearing stewardship's clothes**: chosen post hoc from the
  failure anatomy of the falsified corpus, requiring a new preregistration on
  untouched evidence — which the pre-declared stop condition forecloses
  ("H-ID fails ⇒ the Physics lane TERMINATES — no further program will be
  manufactured").
- No measurement defect was found by four audits; a re-run would implicitly
  allege MEASUREMENT_INVALID with zero identified defects. Network
  reachability proves nothing new: feasibility was established by 704 valid
  trials in the original window.

**Confirmatory extraction set of prereg aba6858: EXHAUSTED.** The complete
inferential content is {hard-gate predicates; three DATA_INSUFFICIENT
triggers; SURVIVES ⇔ F2 ∧ F4}; every element is evaluated and quadruple-
audited. F3 holds by construction and carries no evidential weight; D1–D5
were frozen descriptive; nothing is fitted anywhere.

## 3. What this run did

1. **Control-plane sync separated** (commit `f64848b`): 67 staged paths,
   byte-identical to main tip `92192ea`, committed apart from scientific
   content per standing audit advisory.
2. **Bit-exact carry onto the accepted lineage** (commit `91eff06`): all 26
   WP-006 scientific files extracted from the audited snapshot
   `origin/cycle/physics/32860596387/team`; 22 core files verified
   blob-identical to certified snapshot `45fa5db`
   (= `origin/cycle/physics/32799587656/team`), 4 stewardship-layer files
   unique to run 32860596387/team (itself audited PASS). Ledger purely
   additive (+112/−0 vs `d3afd9b`). Dataset blob unchanged since result commit
   `8d84196`: sha256 `fafd1cef46bb6b25…31149397`, manifest-matched.
3. **Fresh-environment verification (this run, zero RNG):**
   - Committed deterministic recheck
     `physics/team_recheck_wp006_run32860596387.py` rerun in a scratch tree
     reproduces BOTH of its artifacts **byte-identical** to the committed
     versions (`wp006_team_recheck_run32860596387.json`,
     `wp006_floor_postmortem_run32860596387.json`). Certified headlines
     reconfirmed from raw rows: rows 1075 = 1+164+910; 704/206 valid/invalid;
     exclusions action_failed 171 / exception 22 / state_match 13; verified
     BPs books 12, quotes 12, saucedemo 7, parabank 5, internet 2 = 38;
     producers {books, quotes} = 2; applied verdict from own floor logic:
     **FALSIFIED**.
   - UNMODIFIED frozen verifier `verify_wp006.py` rerun (freeze timestamp
     supplied, output redirected to scratch):
     **PASS=true, own_verdict=FALSIFIED, verdict_agreement=true**. Key-level
     diff vs stored `wp006_verification_v2.json`: exactly the disclosed
     advisory-A1/C10 key (`C3_rows_before_freeze_commit`, present here because
     the freeze timestamp was passed as an argument); vs stored v3: exactly
     the added `/provenance` block. All checks identical otherwise.
4. **ONE new descriptive-only artifact** (pre-declared structure, fenced):
   `results/physics/wp006_terminal_bound_and_seam_run32866107906.json`
   generated by committed stdlib-only `physics/terminal_bound_wp006_run32866107906.py`
   (byte-identical across reruns; no random module imported). Summary in §4.

## 4. New descriptive exhibit (cannot rescue or weaken the primary verdict)

**A. DATA_INSUFFICIENT negation (row-cited).** All three frozen triggers
false: 8 ≥ 6 sites attempted (first-row timestamps recorded per site); both
classes present; 38 > 0 verified BPs. Cap-truncation biases downward and even
maximal admissible recovery cannot flip either floor (tier 1 below).

**B. Tiered attribution-of-shortfall bounds** (estimand = REALIZED verified
BPs; tiers are bounds, not estimates):

| tier | credit rule | total | producers | floors |
|---|---|---|---|---|
| 0 measured | none | **38** | **2** | F4 FAIL, F2 FAIL |
| 1 admissible-imputation bound | only components with ≥1 committed success (openlibrary full recovery ≤+12) | **≤50** | **≤3** | **both STILL FAIL** |
| 2 upper bounds (INADMISSIBLE component included — stamped) | + 24 dead-arm BPs at sibling rates (0-for-168 in own attempts); + stateful planned headroom (+8) | ≤62 / ≤82 | ≤4 / ≤5 | would pass |

Verdict robustness in one line: **U_prod = 3 < 4 and U_tot = 50 < 60 — both
floors fail in EVERY admissible world.** Tier-2 numbers are mutually
idealized, additively stacked, jointly unrealized; they carry no probability
or modal force and are never grounds for re-collection or floor recalibration.

**C. Instrument-seam signature checks (new finding, from raw rows).** The
floor miss on wikipedia/gutenberg is a **classifier×executor composability
seam**, not environment instability:

- **C1 homogeneity**: all 171 action_failed exclusions share ONE exception
  class (`Locator.click: Timeout 8000ms exceeded`); the only untruncated
  call-log evidence (84 wikipedia strings) shows the locator *resolving* to a
  fragment-href anchor (`<a href="#…`, i.e., an in-page skip link) and then
  timing out — deterministic element-class behavior consistent with the seam
  (168/171 rows on `click_link#0` at wikipedia/gutenberg; gutenberg/
  openlibrary strings are stored truncated before that line).
- **C2 zero-success test**: `click_link#0` succeeds 100% on
  books/quotes/internet/parabank/saucedemo (217 corpus successes) yet is
  0/84 wikipedia, 0/84 gutenberg, 0/21 openlibrary — a property of
  visually-hidden anchor elements on heavy static skins, not of the slot kind.
- **C3 sibling contrast**: at ALL 24 affected BPs, slot A executes 7/7 valid
  while slot B fails 0/7, with **0 state-match exclusions** on those BPs —
  restart/state reproducibility was PERFECT there; only the declared arm
  failed.
- Scope consequence: **no verdict flip** (failed clicks honestly observed;
  nothing measured is wrong); instead **stratum-level scope collapse** —
  wikipedia/gutenberg restart reproducibility is UNKNOWN (blocked by the
  instrument vocabulary), NOT refuted.

**D. Per-cell census (verdict-inert integrity note).** 130 cells with trials;
100 reach ≥6 valid replicates; all 30 sub-floor cells are exactly the 24 dead
arms plus cap-truncated openlibrary cells (e.g., fantasy 0/7, mathematics
1/7, science 3/7).

**E. Ordering/transient probe.** Dead-arm failure is uniform across replicate
positions (every dead-arm trial fails regardless of order/timestamp): no
block-position degradation; consistent with the deterministic seam.

## 5. Terminal decision package FOR THE LANE DIRECTOR

Pre-declared stop condition (`directives/PHYSICS.md`, "Lane rule and program
horizon") is engaged: **H-ID FALSIFIED ⇒ the Physics lane TERMINATES at this
Director step; no further program will be manufactured.** The stop condition
binds irrespective of dispatch count; this run performed zero environment
interactions and makes that decision executable:

### 5.1 Evidence-chain index

| step | artifact |
|---|---|
| Pre-freeze disclosure | commit `744cdd3` (goto-only smokes, reset shakedown; no actions/outcomes) |
| FREEZE | `aba6858` 2026-08-24T21:30:49Z (prereg + collector v4 + driver + verifier; G1 complete; 0 rows predate it) |
| Pre-outcome instrument repairs | `a5c5112`, `d8303d2` (pre-fix hashes preserved; zero outcomes observed) |
| Result | `8d84196` — wp006_v1 dataset + results + verifier PASS + report |
| Audit round 0 | REVISE RF1–RF5 (`CYCLE_32776372437_PHYSICS_GATE.json`, branch …/audit `eb90589`) |
| Repair round 1 | `a00dc6a` (RF1–RF5 closed additively) |
| Audit round 1 | **PASS safe_to_integrate=true** (`CYCLE_32793165981_PHYSICS_GATE.json`) |
| Carryforward + fresh-env repro | `45fa5db` (run 32799587656) |
| Audit round 2 | **PASS safe_to_integrate=true** (`CYCLE_32799587656_PHYSICS_GATE.json`) |
| Stewardship snapshot | run 32860596387 team tip `76a1d72` |
| Audit round 3 | **PASS safe_to_integrate=true** (`CYCLE_32860596387_PHYSICS_GATE.json`) |
| This run | team branch `cycle/physics/32866107906/team`: carry `91eff06` + verification/new-exhibit/report commits |

Canonical results artifact: `results/physics/wp006_results_v2_amended.json`
(original `wp006_results.json` preserved byte-exact; errata E1–E5 additive);
canonical verification: `results/physics/wp006_verification_v3.json` (v1/v2
preserved byte-exact).

### 5.2 Proposed Director actions (Director-owned; team claims no authority)

1. Integrate this snapshot's carried WP-006 evidence into `lab/physics`.
2. Adopt/adapt the additive ledger addendum in `docs/PHYSICS_LEDGER.md` §WP-006.
3. Record lane termination in `state/physics_loop.json` — PROPOSED content:
   `continue=false`, `next_program.launch=false`,
   `program_status="TERMINATE_LANE"`, reason "WP-006 H-ID FALSIFIED at
   director floors; stop condition engaged" — and rewrite
   `directives/PHYSICS.md` / `docs/NEXT_PHYSICS.md` to terminal status.
4. Bounded closing knowledge for the record (see §6 wording limits):
   cross-site transferable dynamics FALSIFIED coarse+fine (cycles 1–2);
   within-site comparable-state identifiability via restart/matched-state
   intervention at director floors FALSIFIED (this program); WP-004
   committor/barrier lineage closes BLOCKED-never-unlocked.

### 5.3 Riders required on the terminal lesson (red-team)

- **Program ≠ proposition**: FALSIFIED falsicates the PREREGISTERED
  AFFIRMATION PROGRAM (floors at this tolerance/vocabulary/budget); it is
  NOT proof that restart-idempotence fails at untested states/BPs.
- **Stratum scope collapse**: wikipedia/gutenberg UNKNOWN (instrument seam);
  openlibrary undemonstrated (cap-truncation + FN control 5/12, MNAR
  direction biases AGAINST floor attainment, capped decisively below flip
  thresholds); stateful producer performance UNTESTED BY DESIGN
  (planned capacities 7/7/8 < 10 producer bar) — not refuted.
- **Design brittleness note**: sites planned at ≥10 BPs numbered exactly 4 =
  F2 requirement → zero site-level tolerance; a single stratum-level
  instrument event dominated the corpus outcome. Any hypothetical successor
  planning rule should budget planned producers ≥ required + 1.
- **Measurand boundary**: client-fresh contexts guarantee cookie/storage
  emptiness only; server-side session/bucket/rate-limit state persists across
  "fresh" trials from one runner IP.
- **Atomicity scope**: V4 atomicity is executor-relative; no retry counter is
  committed, so wire-level single-attempt semantics are not re-verifiable
  from committed rows.
- **Descriptive residue, never product claims**: T2 near-determinism
  (101/102 cells) and perfect sibling-arm reproducibility are descriptive;
  they must not be promoted to compression/product primitives without their
  own preregistered identifiability gate — which the stop condition now
  forecloses inside this lane.

### 5.4 Designated opening experiment IF a human ever charters a successor

(ledger knowledge only; NOT a queued program; launching it would require a
human-authorized amendment given the engaged stop condition): a ~12-trial
calibration matrix — 2 BPs × {default locator click, JS dispatchEvent,
keyboard activation} × {hidden anchor, visible anchor} — converting the
62/4 repair bound into a measured quantity and yielding a permanent
instrument lint (*integration-test every classifier×executor pair before
freeze; never declare slots violating executor preconditions*).

## 6. Wording limits (binding)

MAY claim: deliberate restart/matched-state collection produced verified
matched branch points within single live sites (5/8 sites; two sites at the
≥10 producer bar); realized yield was dominated by declared-arm executability
and one wall-clock truncation, not by state matching outside openlibrary;
both floors fail in every admissible recovery world (U_prod=3<4, U_tot=
50<60). MAY NOT claim: matched-state verification impossible or unreliable in
general; "would have survived but-for X"; causal arm-level findings;
per-site production probabilities; anything fitted/predictive; any
committor/barrier/metastability conclusion (WP-004 stays BLOCKED).

## 7. Limitations (exact)

- Raw full-DOM snapshots are ephemeral (/tmp policy): what cannot be
  recomputed later is raw page content. Every analyzed field is committed;
  T1/T2 labels re-derive from committed observables with 0 mismatches on
  explicit denominators summing to 910 (22 no-PRE + 13 unusable-POST counted,
  never dropped).
- The tier-2 bounds assume sibling-rate transferability onto arms that are
  0-for-k in their own attempts: arithmetic sensitivity, not measurement.
- openlibrary evidence is cap-truncated by construction; its BP manifest was
  lost to the timeout; figures derive from raw rows only.
- This run adds no new observations; it cannot speak to questions requiring
  new data (there are none left inside the frozen mission).
- Team-side work does not constitute independent validation; the audit gate
  belongs to the separate Auditor session.
