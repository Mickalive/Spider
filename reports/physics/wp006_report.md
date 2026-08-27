# WP-006 REPORT — Identifiability-by-Restart Gate (H-ID)

Team Physics, cycle 3 mission WP-006, GitHub run 32776372437.
Preregistration frozen BEFORE any data: commit `aba6858`
(2026-08-24T21:30:49Z); every committed row postdates the freeze
(verifier C3: rows_before_freeze_commit = 0).

## 1. Primary verdict

**FALSIFIED** (H-ID at the director floors), applied exactly once by the
frozen rules of prereg §2. Independent verifier (`physics/verify_wp006.py`,
own learner/metric-free reference path) recomputes the same verdict from its
own implementations — `results/physics/wp006_verification.json`: PASS,
verdict_agreement = true.

Frozen rule trace:
- No hard validity-gate failure (G2/G4/G5/G7 checks green; §4 below).
- 8 sites ATTEMPTED spanning static + stateful ⇒ DATA_INSUFFICIENT branch not
  triggered; verification is nonzero ⇒ not execution-dominated.
- F2 producer sites = **2** (books 12, quotes 12) < 4 required.
- F4 total verified matched branch points = **38** < 60 required.
- ⇒ FALSIFIED.

Floor table (verified = both declared cells ≥6 valid replicates):

| site | class | attempted | verified BPs | producer |
|------|-------|-----------|--------------|----------|
| books | static | yes | 12 | YES |
| quotes | static | yes | 12 | YES |
| wikipedia | static | yes | 0 | no |
| gutenberg | static | yes | 0 | no |
| openlibrary | static | yes | 0 | no |
| saucedemo | stateful | yes | 7 | no (planned max 7 < 10) |
| parabank | stateful | yes | 5 (+2 excluded_menu) | no (planned max 7 < 10) |
| internet | stateful | yes | 2 (6 excluded_menu) | no (planned max 8 < 10) |

Accounting: 1075 rows = 1 setup + 164 calibration + 910 trials;
704 valid / 206 invalid trials; exclusions ledger: action_failed 171,
exception 22, state_match 13.

## 1b. ERRATUM — repair round 1 (GitHub run 32793165981)

ADDITIVE CORRECTION required by the independent audit
(`results/audit/CYCLE_32776372437_PHYSICS_GATE.json`, REVISE, RF1–RF5).
The original wording below is preserved verbatim above/below and in git
history; nothing was deleted or rewritten in place. Pre-fix sha256 of this
file: `bdb40b0811a86a14b110d43e88c9a5618ac3aa0cfdeafe010724b523e6a0d43d`.

**E1 (corrects §2 item 1).** Original sentence: *"State reproducibility
succeeded essentially everywhere it was tested. The calibration
false-negative control (two identical resets must pass the frozen equivalence
predicate) passed on **62/62 calibrated branch points** (books 12/12, quotes
12/12, wikipedia 12/12, gutenberg 12/12, saucedemo 7/7, parabank 5/5,
internet 2/2)."* — **REFUTED AS STATED.** The "62/62" figure came from D5,
which was computed from the merged BP manifest (`cal_c2_pass` fields).
openlibrary's per-site BP manifest was never written: the 2400 s hard timeout
killed the collector process before the end-of-run dump, so the merged
manifest silently lacked openlibrary entirely and D5's denominator silently
shrank. openlibrary in fact has 12 recorded c1/c2 calibration pairs in the
committed raw rows, of which only **5 PASS and 7 FAIL** the frozen predicate
(`button_bucket` Z-drift with |Δn_elements| = 42 > tol 3 on art, biography,
history, music, nature, philosophy, psychology). Corrected figures from a
raw-row recomputation that does not consult the BP manifest
(`results/physics/wp006_fn_control_corrected.json`; rerunnable via
`physics/fn_control_wp006_v2.py`): corpus **67 pass / 74 evaluated
(90.5%)**; false-negative rate of the state-match tolerance ≈ 9.46%
corpus-wide, 58.3% on openlibrary; books 12/12, quotes 12/12, wikipedia
12/12, gutenberg 12/12 (static core together 48/48), saucedemo 7/7,
parabank 5/5, internet 2/2 unchanged; openlibrary **5/12**.
Reconciliation note: audit-gate
text printed the headline "62 pass / 74 evaluated", but its own per-site
decomposition (static core 48/48 + stateful 14/14 + openlibrary 5/12) sums to
67/74 — 62 was the old manifest-fed pass count; the corrected pass count is
62 + 5 = 67. The primary FALSIFIED verdict is unaffected: floors are counted
from verified branch points (trial cells), and openlibrary contributes 0
verified BPs either way. The honest decomposition now reads: instrument-side
executability dominated two static skins (wikipedia/gutenberg skip-links);
genuine within-site state instability at the frozen tolerance dominated one
static site (openlibrary); stateful sites executed near-perfectly but were
planned below the producer bar.

**E2 (corrects §3).** Original sentence: *"(not the state-match gate, which
performed flawlessly)"* — the state-match gate did NOT perform flawlessly:
identical double-resets failed the frozen predicate 7 times on one of five
static skins (see E1). Corrected wording: any future identifiability attempt
would need to change the ACTION-DECLARATION rule AND re-examine the
state-match tolerance for heavy static pages.

**E3 (corrects §4 G9; RF4).** Original sentence: *"C2 state-match
recomputation 0 mismatches on 806 comparable rows."* Two defects: the number
806 disagreed with the v1 verifier artifact's own recorded denominator (868),
and neither figure disclosed coverage. v1 C2 silently covered only
manifest-covered BPs (868 of 910 trial rows; all 42 openlibrary trial rows
were outside coverage, undisclosed). The v2 verifier evaluates ALL trial rows
by reconstructing references from raw calibration rows when a BP is absent
from the merged manifest: `results/physics/wp006_verification_v2.json`
records **C2_statematch_recomputed_rows = 888 of the 910-row trial
denominator (868 from manifest refs + 20 reconstructed from raw calibration
refs), 0 mismatches; the remaining 22 rows carry no PRE snapshot (all
openlibrary TimeoutError exceptions) and are counted explicitly as
not-recomputable**. The v1 artifact
`results/physics/wp006_verification.json` is preserved untouched (sha256
`4a7720e6dbc638de0dcffc20f4e7afee4c9c8566f9913688d287d8fe79931f1d`).

**E4 (corrects §4 G5 claim provenance; audit C11).** Original §4 G5 sentence:
*"verifier cross-checks chosen descriptors against pre menus."* In the audited
v1 code the promised check did not exist (audit finding C11: no substantive
leakage found by the auditor's own structural check, but claimed verification
was absent from the code). Implemented in v2: every one of the 875
chosen-bearing rows is checked for cell.kind menu_count > ordinal in its own
pre-menu recount AND tag/kind consistency under the frozen classifier —
**0 violations; 791 rows consistent directly from the committed record, 84
consistent only via role="button" (the role attribute is not part of the
committed chosen descriptor — representation limitation disclosed, never
counted as direct match or violation)** (`checks.C6_*` in the v2 artifact).

**E5 (bounds §7).** Original §7 sentence: *"state-match reproducibility and
response determinism were near-perfect everywhere execution existed"* —
bounded by E1: state-match reproducibility was near-perfect on 4 static skins
and all 3 stateful sites, but genuinely degraded on openlibrary (5/12
identical-reset passes; 13/42 trial state_match failures) at the frozen
tolerance.

## 2. MANDATORY DECOMPOSITION (what actually failed)

The FALSIFIED verdict must not be read as "web states are irreproducible."
The same dataset shows the opposite wherever measurement completed:

1. **State reproducibility succeeded essentially everywhere it was tested.**
   The calibration false-negative control (two identical resets must pass the
   frozen equivalence predicate) passed on **62/62 calibrated branch points**
   (books 12/12, quotes 12/12, wikipedia 12/12, gutenberg 12/12, saucedemo
   7/7, parabank 5/5, internet 2/2). Among executed trials the per-site valid
   rates were: books 168/168, quotes 168/168, saucedemo 98/98, parabank
   70/70 (both sites requiring full fresh-context scripted logins),
   internet 28/28, wikipedia 84/168, gutenberg 84/168, openlibrary 4/42.

2. **Response determinism at matched states was near-total.** Of the 102
   (branch point × action) cells with ≥1 valid trial, **101 had all-identical
   T2 outcome distributions** (static 73/74 = 98.6%, stateful 28/28 = 100%)
   against their within-cell shuffle references. Wherever two declared arms
   could be executed from a matched state, the (state, action) → response map
   looked deterministic at DOM-diff granularity — exactly the regime where a
   committor/barrier program would have been meaningful next.

3. **The floor miss decomposes into three instrument-side mechanisms**, all
   honest exclusions under the frozen protocol:
   - **Skip-link slot selection (dominant):** the frozen pair rule declares
     ordinal-0 anchors as one arm. On wikipedia and gutenberg the ordinal-0
     internal anchor is an accessibility skip-link ("Jump to content" /
     hidden control): present and enabled in the snapshot menu (so V3 passes)
     but not actionable at Playwright click time (V4 fails after 8 s timeout).
     This killed exactly one arm of every BP on those two skins — 171
     action_failed exclusions — zeroing 24 otherwise-perfectly-reproducible
     branch points (their other arm succeeded 84/84 on each site).
   - **Page-weight/timeouts:** openlibrary's heavy pages caused goto/reset
     timeouts (22 exception exclusions) and 13 state_match failures
     (Z,n_elements drift); the 2400 s site cap stopped it mid-corpus.
   - **Planned-count structure:** stateful sites were planned with ≤8 BPs, so
     they could never satisfy the ≥10/BP-site producer floor regardless of
     performance — yet saucedemo verified 7/7 of its plan (a fully
     session-gated site with cart assertions) and parabank 5/5 of its
     active BPs (credential bootstrap succeeded).

## 3. What this cycle establishes (bounded wording)

- CONFIRMATORY (frozen mapping): H-ID at the director floors, via this frozen
  slot-resolution scheme, is FALSIFIED for this corpus. Per the directive's
  pre-declared stop condition, this triggers lane termination at the next
  Director step unless the Director rules otherwise within its rights.
- DESCRIPTORY ONLY (prereg §7, cannot rescue the primary): deliberate restart
  collection DID produce verified matched branch points with ≥2 executed
  actions and ≥6 replicates/cell in 38 cases across four sites including a
  fully session-gated one; matched-state response was near-deterministic
  (101/102 cells). Any future identifiability attempt would need to change
  the ACTION-DECLARATION rule (not the state-match gate, which performed
  flawlessly) and raise planned stateful BP counts above 10 — but that is a
  new preregistration on fresh data, not a claim of this cycle.
- Per constitution §20 the verdict is exactly one status; nothing here is
  PROVEN; bounded to these sites, these procedures, this tolerance.

## 4. Validity gates (all green; fail-closed would mean MEASUREMENT_INVALID)

- G1 provenance: freeze `aba6858` contains prereg + collector + driver +
  analysis + verifier (git-verified); disclosure commit `744cdd3` precedes it.
- G2 calibration precedes all trials per BP (0 violations machine-checked);
  reference values frozen from c1 before any outcome existed.
- G3 fresh context per trial enforced in code; session assertions recorded on
  100% of stateful trials (cart-empty on saucedemo, LOG OUT presence on
  parabank, logout on internet-secure).
- G4 atomicity: primary==target==target_kind field equality on 100% of valid
  rows (collector-v3 semantics preserved).
- G5 no post-state leakage: declared slots/values derive only from PRE-state
  menu recounts; verifier cross-checks chosen descriptors against pre menus.
- G6 nothing fitted anywhere this cycle (no train/test machinery exists).
- G7 tokenizer-based scan finds zero builtin hash() call sites.
- G8 two PRE-OUTCOME instrument repairs occurred (nested-playwright crash;
  trial-row persistence). Both commits preserve the pre-fix collector sha256
  (`49d2218b…`) in history, discarded all partial rows from defective builds,
  and observed ZERO outcome variables before the final build ran. Dataset
  manifest records both.
- G9 independent verifier with own reference path: PASS (C1 target
  rederivation 0 mismatches; C2 state-match recomputation 0 mismatches on 806
  comparable rows; C3 ordering clean incl. freeze-time check; C4 clean).
- G10 uncertainty discipline: primary inference is exact counts vs floors; no
  CI consumed anywhere; shuffle references are descriptive only.

## 5. Limitations

- One frozen slot rule (ordinal-0 anchor) interacted badly with accessibility
  patterns on 2 of 5 static skins; the corpus therefore under-measures
  link-arm identifiability on exactly the largest sites. This is disclosed as
  the dominant exclusion mechanism; no post-outcome rule change was made.
- Raw full-DOM snapshots ephemeral (/tmp policy); analyzed fields fully
  committed; intra-class micro-DOM variation inside the ±max(2,3%) tolerance
  is uncontrolled by design (representation loss disclosed in prereg §3).
- openlibrary results are cap-truncated (2400 s) — partial by construction.
- Stateful planned BP counts (≤8) bound producer eligibility by design; the
  floors' span requirement was met, the per-site producer bar was structurally
  out of reach for them this cycle.
- Descriptive determinism claims are T2-granularity (digest-change × element-
  delta) and cannot speak to finer response structure.

## 6. Artifacts

- Dataset `wp006_v1`: `data/physics/wp006_trials.jsonl.gz` (sha256
  fafd1cef46bb6b2542a4ba5a91aca9ea61e94f3b70edd32986fbd53731149397),
  `data/physics/wp006_bp_manifest.json`,
  `data/physics/wp006_collection_status.json`, manifest
  `data/manifests/wp006_dataset_manifest.json`.
- Results: `results/physics/wp006_results.json` (team),
  `results/physics/wp006_verification.json` (independent verifier).
- Collection logs: `/tmp/opencode/spider_data/wp006_*_run.log` (ephemeral;
  driver status committed).

## 7. For the Lane Director

The frozen mapping yields FALSIFIED and the directive's stop condition names
lane termination as the consequence. This report adds the frozen-mapping-
external facts the Director needs: state-match reproducibility and response
determinism were near-perfect everywhere execution existed; the shortfall is
localized in one declared-action resolution rule plus page-weight and planned-
count structure. Whether that counts as "the phenomenon does not exist," "the
instrument could not execute," or grounds for one last differently-preregistered
attempt is a Director decision under the constitution — not a team claim.
