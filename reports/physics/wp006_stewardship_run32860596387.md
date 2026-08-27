# TEAM PHYSICS — WP-006 TERMINAL STEWARDSHIP & INTEGRATION HANDOFF

## Physics lane, GitHub run 32860596387 (cycle index 1, program
## `within-site-dynamics-interventional`, succession/recovery dispatch)

Author role: TEAM PHYSICS (physics_runner). Date: 2026-08-25.
Base checkout: accepted `lab/physics` at `d3afd9b`
(`d3afd9b4d602d28b6914460c24c56ef2ce39fb61`, post cycle-2 Director
integration) — the authoritative accepted lane state. Human steering note:
"AUTO PROGRAM SUCCESSION/RECOVERY from Director run 32689298051 … A prior
successor may have failed operationally; accepted lane state remains
authoritative" — subordinate to the constitution and to
`directives/PHYSICS.md`; it is not a demand for a positive result.

---

## 0. Factual state at team start, and why this cycle performs NO new
##    confirmatory collection

The binding directive (`directives/PHYSICS.md`, WP-006 mission) pre-declared:

> PROGRAM STOP CONDITION (pre-declared): if H-ID fails (FALSIFIED or
> DATA_INSUFFICIENT) … the Physics lane TERMINATES — no further program will
> be manufactured.

The lane's factual state (all verifiable in git; exact provenance in §3):

1. **WP-006 H-ID was executed on live websites and returned FALSIFIED** by
   the frozen verdict mapping (run 32776372437, result commit `8d84196`):
   producer sites **2 of ≥4 required** (books 12, quotes 12 verified matched
   branch points), total verified matched branch points **38 of ≥60
   required**, floors never loosened, every exclusion counted.
2. The independent audit returned REVISE with RF1–RF5
   (`results/audit/CYCLE_32776372437_PHYSICS_GATE.json`, commit `eb90589`
   on `cycle/physics/32776372437/audit`).
3. Repair round 1 (run 32793165981, scientific content `a00dc6a`) closed
   RF1–RF5 additively; its independent audit returned **PASS,
   `safe_to_integrate=true`, `required_fixes=[]`**
   (`results/audit/CYCLE_32793165981_PHYSICS_GATE.json`).
4. Run 32799587656 carried that audited-repair snapshot forward bit-exact,
   reproduced it in a fresh environment, and closed advisory A1/C10
   additively (`wp006_verification_v3.json`); its independent audit again
   returned **PASS, `safe_to_integrate=true`, `required_fixes=[]`**
   (`reports/audit/CYCLE_32799587656_PHYSICS.md`,
   `results/audit/CYCLE_32799587656_PHYSICS_GATE.json`, snapshot `45fa5db`).
5. **No Lane Director integration followed any of this**: `lab/physics`
   still sits at `d3afd9b`; there is no Director report or accepted-state
   commit for runs 32776372437 / 32793165981 / 32799587656. This is the
   operational failure the human steering note anticipates.

Consequences for THIS team phase, applied strictly:

- The primary question of WP-006 ("can verified matched branch points be
  produced at pre-declared floors on live websites?") is already answered
  negatively by an executed experiment whose measurement was certified
  VALID_FOR_CURRENT_TEST by two consecutive independent audits with zero
  required fixes. Re-running collection would be a multiple-look attempt to
  flip a frozen-mapping negative at unchanged floors — precisely the rescue
  program the stop condition forbids ("no further program will be
  manufactured"). Prereg floors may be tightened, never loosened
  (`directives/PHYSICS.md`; prereg §1), so no honest re-run could even
  widen the gate. **No live collection occurred this run**; nothing in this
  snapshot touches `/tmp` browser state beyond read-only reruns of committed
  artifacts.
- Committor/barrier estimation stays BLOCKED (WP-004 gate unmet — H-ID did
  not survive). No learner-based claim is made anywhere this cycle;
  nothing is fitted.
- wp005/wp003b rows are not reused for any target family.

What remains legitimate and useful for TEAM PHYSICS is exactly three things:
(a) place the twice-audited WP-006 evidence into THIS run's team snapshot so
the audit→Director chain can finally integrate it (without it, an executed,
audited experiment silently falls out of the accepted lane state);
(b) add one genuinely new, descriptive-only layer: a fully independent
team-side recomputation plus a quantitative floor-failure post-mortem that
sharpens the terminal lesson recorded in the ledger; (c) hand the Director a
terminal-decision package. That is honest negative-result stewardship, not
program manufacture.

---

## 1. What was carried forward, with exact provenance

All 23 WP-006 scientific files were extracted bit-exact from the final
certified snapshot `origin/cycle/physics/32799587656/team` (= commit
`45fa5db415494dcc23f065f9fb4083e191668de1`). For every file,
`git show SRC:path > worktree` followed by `git hash-object` equality against
`git rev-parse SRC:path` passed: **23/23 OK, 0 failures**. The check itself
is re-derivable from git alone (no ephemeral tooling needed):
`git rev-parse origin/cycle/physics/32799587656/team:<file>` must equal
`git hash-object <file>` for each row of the table above; the carry commit
in this branch preserves the extracted blobs verbatim. Carried areas:

| Area | Files |
|---|---|
| Prereg + reports | `reports/physics/wp006_preregistration.md`, `wp006_report.md` (incl. §1b erratum), `wp006_carryforward_run32799587656.md` |
| Instrument | `physics/collector_wp006.py`, `run_wp006.py`, `run_wp006_collection.py`, `smoke_wp006{,b,c}.py` |
| Verifier + FN tool | `physics/verify_wp006.py` (sha256 `adb0ad009dae81f2…cb8acb0`), `physics/fn_control_wp006_v2.py`, `physics/make_wp006_verification_v3.py` (sha256 `14b9575dc04fc2ee…e9fdc78ae`) |
| Data + manifests | `data/physics/wp006_trials.jsonl.gz` (sha256 `fafd1cef46bb6b25…31149397`, = manifest value), `data/physics/wp006_bp_manifest.json`, `data/physics/wp006_collection_status.json`, `data/manifests/wp006_dataset_manifest.json` |
| Results | `results/physics/wp006_results.json` (`4d34b1cb43bf5ce4…98b2dd`), `wp006_results_v2_amended.json`, `wp006_fn_control_corrected.json`, `wp006_verification.json` (v1), `wp006_verification_v2.json`, `wp006_verification_v3.json` |
| Ledger | `docs/PHYSICS_LEDGER.md`: carried WP-006 block incl. round-1 erratum, verbatim |

Nothing carried was edited; no frozen rule, target, floor, tolerance or
verdict text was touched. The v1/v2/v3 verification artifacts remain
byte-identical to their audited states (sha256 prefixes `4a7720e6…`,
`63d1c71b…`; v3 = v2 checks + restored C3 key + provenance block).

Control-plane hygiene: the workspace index contained a pre-existing staged
role/directive sync (35 files). It was committed SEPARATELY as a control-plane
sync commit whose contents are byte-identical to `main` (`9fb2949`), before
any scientific commit — per audit advisory ("keep control-plane sync commits
separate from team-output commits").

---

## 2. New this run (additive only; descriptive-only science)

### 2.1 Independent team-side recheck — `physics/team_recheck_wp006_run32860596387.py`

Stdlib-only; imports NOTHING from any team module (no `spider_common`, no
verifier helpers — verifier-independence discipline, audit item 16/L1);
reimplements the frozen predicates from `wp006_preregistration.md` text.
Deterministic (bit-identical outputs across reruns; sha256-stable).
Output: `results/physics/wp006_team_recheck_run32860596387.json`.

Every headline number of the certified result reproduces exactly:

| Quantity | Certified | This recheck |
|---|---|---|
| Dataset sha256 | `fafd1cef…31149397` | match (manifest agree = true) |
| Rows | 1075 = 1 setup + 164 cal + 910 trial | identical |
| Valid / invalid trials | 704 / 206 | identical |
| Exclusions | action_failed 171, exception 22, state_match 13 | identical |
| Per-site valid rates | books 168/168, quotes 168/168, saucedemo 98/98, parabank 70/70, internet 28/28, wikipedia+gutenberg 84/168, openlibrary 4/42 | identical |
| Verified BPs by site | books 12, quotes 12, saucedemo 7, parabank 5, internet 2 = 38 | identical |
| Producers (≥10 BPs) | {books, quotes} = 2 <4 → F2 FAIL | identical |
| Total 38 <60 → F4 FAIL; F1 OK (8 sites, both classes) | FALSIFIED | applied verdict from own floor logic: **FALSIFIED** |
| FN double-reset control (raw rows) | 67 pass / 74 evaluated (FN 9.46%), openlibrary 5/12, 7× button_bucket Z-drift | identical (denominator convention documented; 8 menu-excluded BPs listed separately) |
| T1/T2 target re-derivation | 0 mismatches (v2 verifier: 888/910 coverage) | 0 mismatches on my 875 usable-row denominator; 35 rows counted explicitly not-recomputable (22 no-PRE exceptions + 13 PRE-without-usable-POST); denominators sum to 910 |
| T2 determinism spectrum (descriptive) | 101/102 cells all-identical; sole exception gutenberg-shelf4/click_button#0 | identical from stored labels AND from my own T2 rederivation |
| Atomicity primary==target | 0 violations claimed | 0 violations on 704 valid rows |
| Session assertions (stateful) | recorded on 100% of stateful trials | 196/196 present; 0 failed among valid |
| Prereg timing | freeze `aba68580…` 2026-08-24T21:30:49Z precedes all rows | min row ts 21:55:03Z; **0 rows before freeze** |

### 2.2 Fresh-environment rerun of the UNMODIFIED frozen verifier

`python3 physics/verify_wp006.py data/physics 2026-08-24T21:30:49Z` with
output redirected to scratch (`WP006_VERIFY_OUT=/tmp/...`; committed
artifacts untouched): **PASS=true, own_verdict=FALSIFIED,
verdict_agreement=true**, own FN control 67/74 (openlibrary 5/12). Key-level
diff vs stored committed `wp006_verification_v2.json`: exactly the
`C3_rows_before_freeze_commit` key (present=0 here because the freeze
timestamp was supplied; absent from stored v2 — the disclosed advisory
A1/C10 artifact-key omission, closed by the carried v3 artifact). No other
difference.

### 2.3 Floor-failure post-mortem (DESCRIPTIVE ONLY)

`results/physics/wp006_floor_postmortem_run32860596387.json`. Cannot rescue
or weaken the primary verdict; arithmetic on committed rows only. Findings:

1. **One-arm-zeroed branch points: 24** (wikipedia 12, gutenberg 12), dead
   arm always `click_link#0` (accessibility skip-link: menu-present/enabled
   but not actionable at click time → 171 action_failed exclusions), sibling
   arm ≥6 valid everywhere. This reproduces the report's "zeroing 24
   otherwise-perfectly-reproducible branch points" from raw rows.
2. **Counterfactual ARITHMETIC (not a claim, not a result)**: IF those dead
   arms had been executable and valid at sibling rate, the floor arithmetic
   would read F4 total 62 (≥60) and F2 producers 4 ({books, quotes,
   wikipedia, gutenberg}). This quantifies how much of the negative hinges
   on ONE declared slot-resolution rule — it is sensitivity analysis of the
   frozen floors, NOT evidence that H-ID survives, and NOT grounds for a
   re-run under the stop condition (any such attempt would need a NEW
   preregistration on fresh data, which the stop condition forecloses).
3. **Structural producer-bar fact**: planned BP counts from the BP manifest
   — books/quotes/wikipedia/gutenberg 12 each; saucedemo 7, parabank 7,
   internet 8 — i.e., every stateful site was planned BELOW the ≥10
   producer bar regardless of performance (saucedemo verified 7/7 plan;
   parabank 5/5 non-excluded; internet 2/2 non-excluded). openlibrary is
   absent from the manifest (known timeout defect) and established from raw
   rows only (12 calibrated BPs, 5/12 double-reset passes).
4. openlibrary invalid anatomy: 22 goto/reset TimeoutError exceptions +
   13 state_match (Z,n_elements drift) + 3 action_failed of 42 trials; site
   cap-truncated at 2400 s (driver status).

### 2.4 Files added this run

- `physics/team_recheck_wp006_run32860596387.py`
- `results/physics/wp006_team_recheck_run32860596387.json`
- `results/physics/wp006_floor_postmortem_run32860596387.json`
- `reports/physics/wp006_stewardship_run32860596387.md` (this file)
- `docs/PHYSICS_LEDGER.md`: ONE additive addendum block appended to the
  WP-006 entry (audit-chain certification + this run's recheck agreement),
  marked TEAM-PROPOSED PENDING INDEPENDENT AUDIT AND DIRECTOR INTEGRATION.
  Zero deletions elsewhere.

---

## 3. Complete provenance chain (git-verifiable)

| Step | Commit / artifact | Content |
|---|---|---|
| Pre-freeze disclosure | `744cdd3e46367d31563b5a4916360f1458eaa50e` | goto-only smokes + reset shakedown; no actions/outcomes |
| FREEZE | `aba68580a057861f348069cf06c45cf915fecd75` (2026-08-24T21:30:49Z) | prereg + collector v4 + driver + verifier (G1 files); 0 rows predate it |
| Instrument repair 1 (pre-outcome) | `a5c511282a98fb7951a77b6cda248fc9e17dedb9` | nested sync-playwright crash fix; pre-fix collector sha256 `49d2218b…` preserved; zero outcomes observed |
| Instrument repair 2 (pre-outcome) | `d8303d20aaa00f9fc091195f3c02db2d92a0162c` | trial-row persistence fix; partial rows discarded; zero outcomes observed |
| Result (run 32776372437) | `8d841967f8cd9402fe661f194241e7c46600c0c8` | wp006_v1 dataset + results + verifier PASS + report + ledger (pending-audit wording) |
| Audit round 0 | `eb90589…` on `cycle/physics/32776372437/audit` | REVISE, RF1–RF5 |
| Repair round 1 (run 32793165981) | scientific `a00dc6a71b8144ba6bdf47784c9a255c948b67a3` (packaging `07eac1dc…`) | RF1–RF5 closed additively |
| Audit round 1 | `results/audit/CYCLE_32793165981_PHYSICS_GATE.json` | **PASS, safe_to_integrate=true, required_fixes=[]** |
| Carryforward (run 32799587656) | `2f2b84e1a86650ff8f7f0dc5e63dc2dd693a07c6` (snapshot `45fa5db4…`) | bit-exact carry + fresh-env reproduction + A1 closure (v3) |
| Audit round 2 | `results/audit/CYCLE_32799587656_PHYSICS_GATE.json` | **PASS, safe_to_integrate=true, required_fixes=[]** |
| Accepted base (unchanged) | `lab/physics` = `d3afd9b4d602d28b6914460c24c56ef2ce39fb61` | none of the above integrated yet — the operational gap this run addresses |

Dataset blob identity across the whole chain: `data/physics/wp006_trials.jsonl.gz`
sha256 `fafd1cef46bb6b2542a4ba5a91aca9ea61e94f3b70edd32986fbd53731149397`,
unchanged since original result commit `8d84196` (verified by two prior
audits and by this run's manifest check).

---

## 4. Verdict status of this cycle

Exactly one primary status applies to the narrow hypothesis tested (H-ID at
director floors, via the frozen protocol):

**FALSIFIED** — inherited unchanged; this run performs no new measurement
and therefore cannot alter it. This cycle's new work (independent recheck +
post-mortem) is DESCRIPTIVE/stewardship and does not create a confirmatory
claim. Measurement validity of the inherited result: VALID_FOR_CURRENT_TEST
(two independent audits). No hard validity-gate failure exists anywhere in
this snapshot; had my recheck found one, the correct output would have been
MEASUREMENT_INVALID flagging, and it found none (all checks green, §2.1).

Per constitution §20 the verdict is never PROVEN and is bounded to these 8
attempted sites, this frozen reset/state-match tolerance, and this declared
slot-resolution scheme.

---

## 5. For the Lane Director — terminal decision package

The pre-declared stop condition (`directives/PHYSICS.md` "Lane rule and
program horizon") is engaged: **H-ID FALSIFIED ⇒ Physics lane TERMINATES at
this Director step; no further program will be manufactured.** Two
consecutive audits certified the input evidence (`safe_to_integrate=true`
twice) and explicitly left the termination decision to the Director. This
team snapshot makes that decision executable:

1. Integrate this snapshot's carried WP-006 evidence into `lab/physics`.
2. Adopt (or adapt) the additive ledger addendum appended to
   `docs/PHYSICS_LEDGER.md` §WP-006 — it upgrades only the STATUS line's
   certification context; the original "pending audit" wording remains on
   record above it as provenance, per audit advisory.
3. Record the termination in `state/physics_loop.json` (`continue=false`)
   and rewrite `directives/PHYSICS.md` / `docs/NEXT_PHYSICS.md` to reflect
   lane termination with this bounded closing knowledge:
   - Cross-site transferable dynamics: FALSIFIED at coarse and fine
     granularity (audited, cycles 1–2).
   - Within-site comparable-state identifiability at director floors via
     restart/matched-state intervention: FALSIFIED (audited, this program).
   - Descriptive residue (bounded, non-rescuing): wherever execution
     completed, matched-state response was near-deterministic at T2
     granularity (101/102 cells) and state-match reproducibility held
     except openlibrary (5/12 double-reset passes); the floor miss is
     localized in one declared-action resolution rule (skip-link arms on
     wikipedia/gutenberg), page-weight/timeouts (openlibrary), and
     planned-count structure (stateful sites ≤8 < 10). WP-004
     committor/barrier lineage closes BLOCKED-never-unlocked.
4. If, and only if, the Director rules within its constitutional rights to
   override the stop condition, the honest record shows what any successor
   preregistration would have to change (action-declaration rule; stateful
   planned counts; openlibrary tolerance handling) — and must do so as a NEW
   preregistration on fresh data, which the current directive forbids
   manufacturing.

The team claims no authority over that decision.

---

## 6. Limitations (exact)

- Raw full-DOM snapshots are ephemeral (/tmp policy, prereg §3, constitution
  §29); what cannot be recomputed later is raw page content. Every analyzed
  field is committed; T1/T2 labels re-derive from committed observables with
  0 mismatches on my independent path.
- My target-rederivation denominator (875 usable rows) differs from the v2
  verifier's C2 denominator (888) because I additionally require a usable
  POST snapshot for BOTH targets; both count their complements explicitly
  (22 no-PRE + 13 unusable-POST vs 22 no-PRE). Both report 0 mismatches on
  their own denominators; neither silently drops rows.
- The counterfactual in §2.3.2 assumes dead-arm validity at sibling rates;
  it is arithmetic sensitivity, not a measurement.
- openlibrary evidence is cap-truncated (2400 s) by construction; its BP
  manifest is missing (documented collection defect), so all openlibrary
  figures derive from raw rows.
- This run adds no new environment interaction; consequently it cannot
  speak to any question requiring new observations (there are none left
  inside the frozen mission).
