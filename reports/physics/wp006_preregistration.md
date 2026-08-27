# WP-006 PREREGISTRATION — Identifiability-by-Restart Gate (H-ID)

Frozen: 2026-08-24, SPIDER Team Physics, cycle 3 mission WP-006 (GitHub run
32776372437), BEFORE any WP-006 dataset existed and before any WP-006 outcome
was observed. Authority: `directives/PHYSICS.md` cycle-3 mission. This cycle
tests ONLY the H-ID identifiability gate with deliberate restart/matched-state
intervention. NO committor/barrier estimation is permitted this cycle
(WP-004 stays BLOCKED pending H-ID survival; the pilot would be next cycle's
preregistered business on untouched data). Cross-site transferability remains
FALSIFIED (WP-003B-R2, WP-005) and is NOT retested here.

## 1. Primary hypothesis H-ID (exact frozen form)

H-ID: Deliberate restart/matched-state collection produces, on live websites,
VERIFIED MATCHED BRANCH POINTS — repeated arrivals at nominally identical
states (§3 predicate) from which ≥2 distinct primitive actions are executed
with valid replicate trials (§5) — at or above these DIRECTOR FLOORS:

- F1: ≥ 6 sites attempted, spanning static-structured AND stateful/session
  sites;
- F2: ≥ 4 sites each contributing ≥ 10 verified matched branch points;
- F3: ≥ 2 distinct executed actions per branch point; ≥ 6 valid replicate
  trials per (state, action) cell;
- F4: total ≥ 60 verified matched branch points across the corpus.

Floors are quoted verbatim from `directives/PHYSICS.md`; this prereg tightens
operational definitions but never loosens a floor.

Expected direction (honest prior): deep-linkable static pages should satisfy
restart reproducibility under a moderate tolerance; the binding uncertainties
are (i) whether live-page micro-variation breaks even this tolerance anywhere,
and (ii) whether session sites sustain asserted matched states across full
context restarts. Prior on H-ID survival ≈ 0.55–0.70. A FALSIFIED outcome is a
real possibility and would close the WP-004 lineage per the program stop
condition.

## 2. Verdict application (frozen, applied exactly once, in this order)

Exactly one constitutional verdict:

- **MEASUREMENT_INVALID** if any hard validity gate (§8) fails. No
  interpretation follows.
- Else **DATA_INSUFFICIENT** if fewer than 6 sites are ATTEMPTED (definition
  §6) or the attempted set does not span both site classes (static-structured
  AND stateful/session), or zero branch points reached verification because of
  execution/infrastructure failure.
- Else **SURVIVES_CURRENT_TEST** (for H-ID) iff F2 ∧ F4 hold on verified
  branch points (each satisfying F3 by construction, §5) — F1 having been
  guaranteed by the DATA_INSUFFICIENT check above.
- Else **FALSIFIED**: collection executed adequately but matched branching
  below the director bar — live web states of the tested kinds are not
  reproducible enough for comparable-state dynamics at this tolerance. This is
  the directive's publishable negative closing the WP-004 lineage.

No other claim is confirmatory this cycle. §7 secondary items are DESCRIPTIVE
ONLY and cannot rescue or weaken the primary verdict. Scope bounding: any
SURVIVES_CURRENT_TEST wording must state the site classes actually represented
among producer sites; identifiability demonstrated only on static-structured
sites bounds any future committor pilot to those sites until stateful sites
replicate.

## 3. Operational definition of "nominally identical state" (FROZEN)

A branch point BP = (site, declared target URL, frozen reset procedure). For
every trial the agent performs the BP's reset procedure in a FRESH browser
context (cookies/storage empty at context creation; contexts are never reused
across trials — restart semantics uniform across all sites), waits the fixed
settle time (1000 ms) and captures a PRE-state snapshot S. The trial's
pre-state PASSES the state-match gate iff ALL of:

1. **URL exactness**: S.url == declared target URL (exact string equality
   after redirect settle; no prefix/fuzzy matching).
2. **Structural vector equality**: Z(S) equals the branch point reference
   Z_ref on ALL 13 mechanics-only dimensions (frozen feature builder,
   `physics/spider_common.py::features`; nothing fitted).
3. **Element-count tolerance**: |n_elements(S) − n_ref| ≤ tol_N with
   tol_N = max(2, floor(0.03 × n_ref)), n_ref from the reference snapshot.
4. **Title equality**: normalize_title(S.title) == normalize_title(ref),
   where normalize_title = lowercase, collapse all whitespace runs to single
   spaces, strip, truncate to 80 chars.
5. **Declared action menu present**: both declared action slots (§4) exist and
   are enabled in THIS trial's snapshot menu recount.
6. **Session/carryover assertions** (stateful sites only; evaluated and
   recorded on 100% of stateful trials):
   - saucedemo: cart badge absent or text ∈ {"", "0"} (empty-cart assertion);
   - parabank: an enabled anchor whose text uppercased contains "LOG OUT"
     (authenticated-session assertion);
   - internet: for the /secure branch point, an enabled element with text
     containing "log out" case-insensitive; all other internet BPs assert the
     authenticated reset succeeded (final URL == /secure immediately after
     login, recorded in reset info).

Reference values (Z_ref, n_ref, title_ref, menu_counts_ref) are frozen from
the FIRST calibration reset of each BP (§6 Phase A), BEFORE any trial outcome
exists. Representation loss is disclosed: bitwise DOM identity is NOT required
(live-site non-stationarity makes sha256-level equality unachievable in
general); intra-class micro-variation of raw HTML inside the tolerance is
therefore NOT controlled by the gate. Raw snapshots stay ephemeral under /tmp.

State-match FALSE-NEGATIVE control (director-mandated): two consecutive
identical resets of the same BP must PASS against each other — calibrated in
Phase A before any action/outcome exists; per-site pass rates reported.

## 4. Branch points and declared actions (frozen rules)

Site roster (ATTEMPT set; F1 requires ≥6 actually attempted):

- Static-structured (reset = fresh context + goto declared URL):
  books.toscrape.com, quotes.toscrape.com, en.wikipedia.org (/wiki/ article
  space), www.gutenberg.org, openlibrary.org — plan 12 BPs each.
- Stateful/session (reset = fresh context + credential/scripted login +
  navigate): saucedemo (plan 7), parabank (plan 7), the-internet.herokuapp.com
  (plan 8).

BP URL resolution (frozen deterministic rules, executed in Phase A):

- books: from homepage snapshot, anchors with href starting
  `/catalogue/category/books/`, dedup preserving DOM order → first 5 as
  category BPs; from the first such category page, anchors with href starting
  `/catalogue/` excluding `/catalogue/category/` → dedup, first 7 as book
  BPs. IDs books-cat{j}/books-item{j}.
- quotes: pagination BPs `https://quotes.toscrape.com/page/{2..7}/` (6);
  from homepage, anchors href starting `/tag/`, dedup → first 6 tag BPs.
- wikipedia: literal articles: Spider, Ant, Coffee, Mount_Everest,
  Mathematics, Physics, Chemistry, Biology, Astronomy, Geology, Computer,
  Ocean.
- gutenberg: `https://www.gutenberg.org/ebooks/bookshelf/{1..12}`.
- openlibrary: subjects science, history, fantasy, philosophy, music, art,
  mathematics, poetry, psychology, cooking, biography, nature.
- saucedemo: `inventory.html` plus `inventory-item.html?id={0..5}` (all
  reached after authenticated reset).
- parabank: overview.htm, transfer.htm, billpay.htm, loan.htm, findtrans.htm,
  opennewaccount.htm, updateprofile.htm (authenticated).
- internet: secure, status_codes, redirector, dynamic_loading/1,
  dynamic_loading/2, checkbox, dropdown, login (visited while
  authenticated). Dead/flaky URLs die in calibration and are counted — never
  silently replaced.

Menu classifier (frozen; candidates must be enabled, external links excluded;
the shared snapshot schema exposes tag/type/role but no onclick attribute, so
that clause is not operational here):
click_button = tag button ∨ role=button ∨ type=submit;
click_link = tag a (internal); fill_text = input type ∈ {"",text,email};
fill_password = input[type=password]; select_option = select;
check_box = input[type=checkbox]. Ordinal = position within a kind's candidate
list ordered by snapshot element index (DOM order).

Declared action pair (frozen selection from the REFERENCE calibration
snapshot's menu): kind priority ["click_button","click_link","fill_text",
"select_option","check_box","fill_password"]; if ≥2 kinds present → slots
(first-kind,0),(second-kind,0); elif some kind has ≥2 candidates → slots
(kind,0),(kind,1); else BP EXCLUDED at calibration (menu<2, counted).
Distinctness of the two executed actions = distinct (kind, ordinal) slots.
Canned values: fill_text → "spider walk" (type email →
"research@example.com"); fill_password → "notasecret-42"; select_option →
option index 0. Exactly ONE primitive action executes between pre and post
snapshots (collector-v3 atomicity semantics preserved).

## 5. Trials, validity, verification of a branch point (frozen)

Per BP, the trial schedule is the Cartesian product {slot A, slot B} ×
{replicate r=0..6} (7 planned replicates per cell — floor is ≥6 VALID),
ordered by a seeded Fisher-Yates shuffle (seed = int of first 8 bytes of
sha256("20260827|order|{site}|{bp_id}") — integer/sha256 seeds only, Python
hash() forbidden anywhere).

A TRIAL is VALID iff all hold (any failure ⇒ invalid row retained with
machine-readable reason; exclusions counted, never dropped):

- V1 reset_ok: fresh context created; reset procedure completed (including
  scripted login for stateful sites, with at most one immediate retry of a
  failed reset);
- V2 state_match PASS per §3 (at most ONE immediate full re-reset allowed on
  first-pass failure; the second evaluation is final; attempts counted);
- V3 menu_ok: both declared slots present+enabled in the trial snapshot;
- V4 atomicity: exactly one primitive action; last_action.ok == true;
  primary==target field equality;
- V5 session assertions hold (stateful sites, §3.6).

A (state, action) CELL meets the floor iff it accumulates ≥6 VALID replicate
trials. A BRANCH POINT IS VERIFIED iff both its declared cells meet the floor
(this implies F3's "≥2 distinct executed actions"). A site is a PRODUCER iff
it contributes ≥10 VERIFIED branch points. Corpus totals sum verified BPs.

## 6. Collection protocol (frozen phases; all AFTER the freeze commit)

- Phase 0 SETUP (stateful credentials only, no measurements): parabank
  one-time account bootstrap — attempt scripted registration with frozen
  credentials; if the username exists, proceed directly; site marked
  FAILED-CREDENTIALS if neither works (counted; roster has margin).
  saucedemo/internet use public demo credentials (standard_user/secret_sauce;
  tomsmith/SuperSecretPassword!).
- Phase A CALIBRATION per BP: TWO consecutive resets (fresh contexts), no
  action executed, NO post-state/outcome observable computed or recorded.
  Reference = reset c1; BP proceeds iff c2 passes §3 (items 1–4; menu check
  uses c1 for slot declaration) AND the pair-selection rule yields 2 slots.
  Otherwise BP EXCLUDED PRE-OUTCOME (counted with reason). Per-site
  calibration false-negative pass rates reported.
- Phase B TRIALS per §5. Inter-trial sleep U(0.15,0.45)s. Per-site wall-clock
  caps enforced by the driver (static 2400 s, stateful 3300 s); a capped site
  keeps its flushed rows and simply contributes what it contributed.

ATTEMPTED site (for F1/DATA_INSUFFICIENT): the site's collection process
started AND ≥1 calibration reset row was recorded for ≥1 BP.

Stateful reset hardening (frozen): after a scripted login click, the collector
polls up to 6 s for the declared authenticated landing state; on failure the
full scripted login is retried ONCE within the same fresh context (V1). A
still-failed login marks the trial reset_failed (invalid, counted).

## 7. Secondary DESCRIPTIVE items (frozen; cannot rescue primary)

- D1 Per-(BP, cell) outcome distributions over the ALREADY-COMMITTED
  observable classes T1 (URL-shape transition class) and T2 (DOM-diff
  signature) from `physics/spider_common.py` (formulas unchanged); modal
  share and Shannon entropy per cell.
- D2 Determinism/spread spectrum: fraction of cells with all-identical
  outcomes (deterministic limit), stratified by site class and action kind.
- D3 Within-cell label-shuffle reference distributions (500 shuffles, seeded)
  for modal share — DESCRIPTIVE calibration of spread, never inferential.
- D4 Static vs stateful comparison of D1–D3; action-kind stratification.
- D5 Exclusion ledger: every invalid/excluded unit with reason; calibration
  false-negative rates; reset-attempt counts.
NO learner-based confirmatory claim exists this cycle; consequently no
train/test machinery is used anywhere (nothing is fitted).

## 8. Hard validity gates (fail closed ⇒ MEASUREMENT_INVALID)

- G1 Prereg provenance truth: the freeze commit contains THIS file plus
  `physics/collector_wp006.py`, `physics/run_wp006_collection.py`,
  `physics/run_wp006.py`, `physics/verify_wp006.py` — audited against git;
  every provenance sentence here must match git reality.
- G2 State-match verification ran per trial with the frozen predicate;
  exclusions counted; reference values provably frozen in Phase A
  (calibration row timestamps precede ALL trial-row timestamps per BP —
  machine-checked).
- G3 Restart/carryover integrity: fresh context per trial enforced in code;
  session assertions evaluated and recorded on 100% of stateful trials;
  carryover probe = cart/logout/logout-link assertions reported per site.
- G4 Atomicity: exactly one primitive action between pre/post snapshots;
  primary==target equality on 100% of rows.
- G5 No post-state leakage: predictor-relevant declared inputs derive ONLY
  from PRE-state observables (structural by construction: the declared slot
  and value exist before execution); targets T1/T2 derive only from POST
  observables; verifier spot-checks chosen-element descriptors appear in the
  PRE snapshot records.
- G6 Train-only fitting: vacuously satisfied — nothing is fitted (stated for
  the record).
- G7 Determinism: integer/sha256 seeds only; Python hash() forbidden
  (grep-audited).
- G8 Pre-fix artifact preservation: any post-outcome defect fix must preserve
  pre-fix artifacts or their recomputed hashes alongside.
- G9 Independent verifier with OWN reference path: the verifier implements
  its OWN T1/T2 target derivations, OWN bucketization/state-match
  recomputation from committed ingredient counts, OWN floor counting and OWN
  verdict arithmetic; it imports NOTHING from the team analysis module.
- G10 Uncertainty discipline: primary inference = exact counts vs frozen
  floors (no CI consumed); shuffle references are descriptive-only (G10/P3
  standing rule).

## 9. Provenance commitments

Dataset: compact rows committed at `data/physics/wp006_trials.jsonl.gz` with
sha256 manifest `data/manifests/wp006_dataset_manifest.json`; resolved-BP
reference/calibration artifact at `data/physics/wp006_bp_manifest.json`;
collection logs at `data/physics/wp006_collection_status.json`. Raw full-DOM
snapshots remain ephemeral in /tmp (constitution §29): what cannot later be
recomputed is exactly the raw page content; every analyzed field is committed.
Results: `results/physics/wp006_results.json` (team) and
`results/physics/wp006_verification.json` (independent verifier). Historical
result files are never overwritten.

Pre-freeze disclosures (no outcome exposure): HTTP reachability checks
(curl HEAD/GET, 2026-08-24) and goto-only availability smoke tests
(`physics/smoke_wp006.py`, `physics/smoke_wp006b.py`) of candidate BP URLs;
plus `physics/smoke_wp006c.py` — a reset-procedure shakedown that exercised
the FRESH-CONTEXT scripted logins (saucedemo, internet) and one static reset,
capturing only pre-state menu counts; NO primitive action under test was
executed, NO transition recorded, NO T1/T2 or post-state variable computed or
examined. Parabank credential bootstrap was deliberately NOT touched before
the freeze. All smoke scripts are committed BEFORE the freeze commit. No
WP-006 dataset exists in /tmp or git at freeze time.
