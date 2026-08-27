# TEAM PHYSICS — WP-006 CARRYFORWARD + FRESH-ENVIRONMENT REPRODUCTION

## Physics lane, GitHub run 32799587656 (cycle index 1 of this dispatch chain)

Author role: TEAM PHYSICS (physics_runner). Date: 2026-08-25.
Base checkout: accepted `lab/physics` at `d3afd9b` (post cycle-2 Director
integration). Human steering note: "AUTO PROGRAM SUCCESSION from Director run
32689298051" — subordinate to the constitution and to
`directives/PHYSICS.md`; it is not a demand for a positive result.

---

## 0. Why this cycle performs NO new confirmatory collection

The binding directive (`directives/PHYSICS.md`, cycle-3 mission) pre-declared:

> PROGRAM STOP CONDITION: if H-ID fails (FALSIFIED or DATA_INSUFFICIENT) ...
> the Physics lane TERMINATES - no further program will be manufactured.

The lane's factual state at team start:

1. **WP-006 H-ID was executed and returned FALSIFIED** (run 32776372437,
   result commit `8d84196`): producers **2/4** (books 12, quotes 12 verified
   branch points), total verified matched branch points **38/60**, floors
   never loosened, exclusions counted. Dataset `wp006_v1` (8 sites attempted,
   1075 rows), prereg frozen (`aba6858`, 2026-08-24T21:30:49Z) before any data.
2. The independent audit of that run returned REVISE with required fixes
   RF1-RF5 (`reports/audit/CYCLE_32776372437_PHYSICS.md`).
3. Repair round 1 (run 32793165981, commit `a00dc6a`) closed RF1-RF5
   additively; the independent audit of the repaired snapshot returned
   **PASS, `safe_to_integrate=true`, `required_fixes=[]`**
   (`reports/audit/CYCLE_32793165981_PHYSICS.md`,
   `results/audit/CYCLE_32793165981_PHYSICS_GATE.json`).
4. However, **no Lane Director integration followed**: `lab/physics` still
   sits at `d3afd9b` and contains none of the WP-006 evidence; there is no
   director report for runs 32776372437 / 32793165981.

Under the frozen verdict mapping the primary question ("can verified matched
branch points be produced at pre-declared floors?") is already answered
negatively and that answer survived adversarial audit twice. Launching any new
collection now would manufacture exactly the rescue program the stop rule
forbids; committor/barrier estimation stays blocked (H-ID did not survive);
reusing wp005/wp003b rows as confirmatory evidence stays forbidden.
The only legitimate team work remaining is: (a) place the audited-repair
WP-006 evidence into THIS run's team snapshot so the audit-to-Director chain
can finally integrate it, with byte-exact provenance; (b) reproduce it
independently in this fresh environment; (c) close the one open audit
advisory affecting artifacts (A1/C10); (d) hand the Director exact proposed
integration wording. This is honest negative-result stewardship, not busywork:
without it, an audited measurement-valid FALSIFIED verdict would silently fall
out of the accepted lane state.

## 1. What was carried forward, with exact provenance

All scientific WP-006 files were copied bit-exact from the audited repair
snapshot `origin/cycle/physics/32793165981/team` (= commit `07eac1d`;
scientific content = `a00dc6a`). For every file below, `git hash-object` of
the working-tree copy equals the blob on that branch (verified file-by-file;
19/19 OK):

| Area | Files |
|---|---|
| Prereg + reports | `reports/physics/wp006_preregistration.md`, `reports/physics/wp006_report.md` |
| Instrument | `physics/collector_wp006.py`, `physics/run_wp006.py`, `physics/run_wp006_collection.py`, `physics/smoke_wp006.py`, `physics/smoke_wp006b.py`, `physics/smoke_wp006c.py` |
| Verifier + FN tool | `physics/verify_wp006.py` (sha256 `adb0ad009dae81f2...cb8acb0`), `physics/fn_control_wp006_v2.py` |
| Data + manifests | `data/physics/wp006_trials.jsonl.gz` (sha256 `fafd1cef46bb6b25...31149397`, matches manifest), `data/physics/wp006_bp_manifest.json`, `data/physics/wp006_collection_status.json`, `data/manifests/wp006_dataset_manifest.json` |
| Results | `results/physics/wp006_results.json` (sha256 `4d34b1cb43bf5ce4...98b2dd`, byte-identical to audited original), `results/physics/wp006_results_v2_amended.json` (additive erratum copy), `results/physics/wp006_fn_control_corrected.json`, `results/physics/wp006_verification.json` (v1, preserved), `results/physics/wp006_verification_v2.json` |
| Ledger | `docs/PHYSICS_LEDGER.md`: WP-006 block incl. round-1 erratum carried verbatim |

New in THIS run (additive only):

- `physics/make_wp006_verification_v3.py` - regeneration driver closing audit
  advisory A1 (see section 3); sha256 `14b9575dc04fc2ee...e9fdc78ae`.
- `results/physics/wp006_verification_v3.json` - see section 3.
- This report.

Nothing carried was edited; no frozen rule, target, floor or tolerance was
touched; v1/v2 verification artifacts remain byte-identical to the audited
state (`4a7720e6dbc638de...3f1f1d` and `63d1c71bf35decde...fe8ad`).

## 2. Fresh-environment reproduction (this run)

Executed here on the committed dataset alone (no live re-collection - raw DOM
snapshots are ephemeral per prereg section 3 / constitution section 29, as
disclosed):

1. **Dataset integrity**: recomputed sha256 of
   `data/physics/wp006_trials.jsonl.gz` =
   `fafd1cef46bb6b2542a4ba5a91aca9ea61e94f3b70edd32986fbd53731149397` - equal
   to the committed manifest value and to the hash quoted by both prior audits.
2. **Frozen verifier rerun** (`python3 physics/verify_wp006.py <datadir>
   "2026-08-24T21:30:49Z"`): `PASS=true`, `own_verdict=FALSIFIED`,
   `verdict_agreement=true`. Key checks reproduced exactly:
   T1/T2 rederivation mismatches 0; C2 state-match recomputed on 888/910
   trial rows (868 manifest refs + 20 reconstructed from raw calibration
   rows), 0 mismatches, 22 rows without PRE snapshot counted explicitly as
   not-recomputable, 0 unreconstructable BPs; declared-slot redeclaration
   mismatches 0; calibration-before-trials violations 0; atomicity violations
   0 on all 704 valid rows; missing stateful session assertions 0; G5
   chosen-descriptor check 875 rows, 0 menu-count and 0 tag/kind violations
   (791 direct + 84 consistent-only-via-unrecorded-role=button, disclosed,
   never counted either way); FN double-reset control from raw calibration
   rows: corpus **67 pass / 74 evaluated** (FN rate 9.46%), openlibrary
   **5/12**, static core 48/48, saucedemo 7/7, parabank 5/5, internet 2/2.
3. **Determinism of regenerated artifacts**: invoking the FN-control tool in
   this environment rewrote its two output files byte-identically to the
   audited copies (sha256s unchanged: `f89a4aeb85db236e...`,
   `3171b39d63f566bf...`); the rerun verifier output equals the stored v2
   artifact except exactly the advisory-C10 key (section 3).
4. **Team-independent raw-row recomputation** (throwaway script written in
   /tmp for this run only; imports nothing from team modules): phase counts
   1 setup + 164 calibration + 910 trials = 1075 rows; valid 704 / invalid
   206 (171 action_failed timeouts, 22 exceptions, 13 state_match); verified
   BPs by site books 12, quotes 12, saucedemo 7, parabank 5, internet 2 ->
   total 38; producer sites {books, quotes} = 2; attempted 8 sites spanning
   static+stateful -> own verdict **FALSIFIED**, agreeing with team results
   and both verifier versions.

## 3. Advisory A1 closed (audit finding C10)

Finding C10 (round-1 audit): the regenerated `wp006_verification_v2.json`
omitted `C3_rows_before_freeze_commit` because the regeneration was invoked
without the freeze-timestamp argument. Advisory A1: bake the freeze timestamp
into the invocation or record it in the emitted artifact.

Implemented WITHOUT touching the frozen verifier:

- `physics/make_wp006_verification_v3.py` invokes the unmodified
  `verify_wp006.py` with `FREEZE_ISO=2026-08-24T21:30:49Z` baked in
  (freeze commit `aba6858`), captures its raw output via a temp file, and
  writes a NEW versioned artifact `results/physics/wp006_verification_v3.json`
  carrying (a) all v2 checks, (b) the restored
  `C3_rows_before_freeze_commit = 0` (matching v1's recorded value),
  (c) an explicit provenance block: freeze commit/time, exact generator
  invocation, dataset sha256 recomputed at generation time and compared to
  the manifest, relation to v1/v2, generating GitHub run id.
- Verified: v3 shares every v2 key/value with zero changed check values; the
  only additions are the C3 key and the provenance block. v1/v2 are preserved
  untouched.
- This run's v3 generation: `PASS=true`, `own_verdict=FALSIFIED`,
  `verdict_agreement=true`, `C3_rows_before_freeze_commit=0`,
  `dataset_hash_agreement=true`.

## 4. Verdict discipline

Exactly one constitutional verdict applies to H-ID and is unchanged:
**FALSIFIED** (floors under the frozen mapping: F1 satisfied - 8 >= 6 sites
attempted spanning static+stateful; F2 violated - 2 < 4 producer sites;
F3 satisfied wherever cells existed - >= 2 distinct executed actions x >= 6
valid replicate trials per cell; F4 violated - 38 < 60 total verified BPs;
no hard validity-gate failure => not MEASUREMENT_INVALID; verification nonzero
=> not DATA_INSUFFICIENT).

Bounded decomposition that survives (corrected figures per round-1 audit):
instrument-side executability dominated two static skins (frozen ordinal-0
anchor slots selected non-actionable accessibility skip links on
wikipedia/gutenberg); genuine within-site state instability at the frozen
tolerance dominated openlibrary (identical-reset control 5/12; corpus FN rate
9.46% - NOT "~0%"); stateful sites executed near-perfectly but were planned
below the producer bar (<= 8 BPs/site < 10). Descriptive-only (cannot rescue
the primary): wherever both arms executed from matched states, response was
near-deterministic at T2 DOM-diff granularity (101/102 cells).

Per the pre-declared stop condition, H-ID FALSIFIED engages **lane termination
at the next Director step**. That decision belongs to the Lane Director alone;
this team adds no program proposal.

## 5. Proposed ledger integration lines (Director's to apply)

The carried ledger entry still reads "TEAM RESULT, PENDING INDEPENDENT AUDIT"
- correct when written, stale now. Proposed additive addendum (erratum-style,
no history rewrite):

> - **AUDIT ADDENDUM (Lane Director integration)**: repair round 1 (run
>   32793165981, commit `a00dc6a`) closed RF1-RF5; independent audit
>   `reports/audit/CYCLE_32793165981_PHYSICS.md` /
>   `results/audit/CYCLE_32793165981_PHYSICS_GATE.json` = **PASS,
>   safe_to_integrate=true, required_fixes=[]**. Status upgraded from
>   "pending audit" to **FALSIFIED - INDEPENDENTLY AUDITED
>   (VALID_FOR_CURRENT_TEST)**. Carryforward reproduction in a fresh
>   environment (run 32799587656): verifier PASS/FALSIFIED reproduced,
>   corrected FN control 67/74 reproduced, dataset sha256 match;
>   advisory A1 closed via `results/physics/wp006_verification_v3.json` +
>   `physics/make_wp006_verification_v3.py`; v1/v2 artifacts preserved.

## 6. Limitations and non-goals (exact)

- No live websites were visited this run; no new rows exist. Everything above
  is recomputation of committed compact evidence. Live-state claims therefore
  remain bounded to the original collection window
  2026-08-24T21:52Z..2026-08-25T00:01Z and are not refreshed by this run.
- Raw full-DOM snapshots were ephemeral by design (prereg section 3,
  constitution section 29); all recomputation uses the committed compact rows.
  What cannot be recomputed later is unchanged from prior disclosures.
- This cycle makes NO new confirmatory claim and re-tests nothing: cross-site
  transfer stays falsified; committor/barrier estimation stays BLOCKED;
  no wp005/wp003b row was reused for any target family.
- Control-plane files staged by the environment (agent definitions,
  directives/AUDITOR.md, directives/LANE_DIRECTOR.md sync) are NOT part of the
  scientific carryforward; they are left to the workflow packaging commit so
  provenance stays separated where possible (round-1 audit advisory A2).
- Verifier independence note: `verify_wp006.py` and `fn_control_wp006_v2.py`
  import nothing from team analysis/collector modules (stdlib only); the new
  driver only wraps the verifier as a subprocess and adds provenance metadata;
  it computes no metric itself beyond file hashes.

