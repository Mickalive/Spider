# INDEPENDENT RUNTIME AUDIT — CYCLE R2-2 (run 32940627441, repair round 0)

Auditor: SPIDER Runtime Independent Auditor (separate session).
Audited snapshot: team branch tip `548709d` mounted at `/tmp/spider_runtime_team`
(clean checkout; `git status` clean, detached at tip).
Untouched accepted base: this checkout = `runtime-audit-base` ≡ `origin/lab/runtime`
at `fcbeaa2` (Director integration of audited R2-1 repair r1, PASS, run
32933579869). Delta audited: `fcbeaa2 → ce70080 → a2bbaaa → e0ae931 → 88c7418
→ 548709d`, linear single-parent chain verified.
Audit date: 2026-08-26. Audit method: code + raw artifacts + independent
recomputation + same-day live reproduction. No Runtime code was repaired or
modified; no lane state touched; only `reports/audit/` and `results/audit/`
written.

---

## 0. Verdict summary

**GATE: PASS.** The FLOOR_DOMINATES headline survives full adversarial
recomputation at the frozen ceilings. Every material claim was recomputed
from raw artifacts by independent code execution, and — beyond the team's own
reproducibility evidence — every scored response body in the event stream was
**byte-identically reproduced live from the audit sandbox on audit day**,
including the fed negative control. No required fixes. Six non-blocking
warnings (W-B1..W-B6) below; standing obligations W-A2/W-4 correctly carried,
not owed this cycle.

The result is a **negative-knowledge measurement result** (bare HTTP dominates
an in-canon pagination goal class AND the discriminator is decidable there),
correctly reported at observation tier with X31 compression phrasing still
banned everywhere else (killer (i) undischarged). Integration is safe because
the wording never exceeds its ceilings.

---

## 1. Claim-by-claim recomputation

### C1 — "FLOOR_DOMINATES at the frozen gates (decidable discriminator)"

* CLAIM: PG-K3F (`/tag/love/` → `/page/3/`), PG-K9B (`/page/10/` → `/page/9/`),
  confirmation PG-KCONF (= K3F) each judge_success in ≤ B_PG=6 wire
  transactions after the entry GET; out-of-range control `/page/1000/`
  verifiably FAILED via pinned witness branch 1; discriminator FED, not voided.
* EVIDENCE FILES: `results/runtime/r2_pagination/cost_events.jsonl`,
  `r22_floor_results.json`, `r2_cycle2_state.json`;
  `runtime/floor_pagination.py`, `gates_r22.py`, `r2_cycle2.py`;
  prereg `reports/runtime/R2_CYCLE2_PREREG.md`.
* RECOMPUTATION:
  * Fresh `gate_pagination_cycle()` over the committed stream reproduces the
    committed analysis block **DEEP-EQUAL (0 key mismatches)**;
    `verify_twin_identity` clean (25 logical rows × twins + PREFLIGHT);
    `self_test()` decides all 9 fabricated branches correctly.
  * Stream arithmetic re-derived independently: exactly 10 wire transactions
    = 2 authorized parity GETs (inside PREFLIGHT note payload) + 4 entry loads
    + 4 scored steps; 25 logical rows; no retries exist; per-cell steps=1,
    loads=1; budget quantifier correctly excludes the control.
  * Verify rows inspected field-by-field: tri-value states, guards
    (`http_status_200`, `path_is_constructed_target`, `no_transport_error`,
    content marker ≥1) all true on positives; control row carries
    `decision_path=failure_witness_branch_1`, observed_status 200,
    content_marker_count 0, matched branch recorded; void-detector-first order
    honored in code (`_negctl_judge`) — a soft-200 WITH content would auto-VOID
    (hermetically tested), so the fed verdict is not an artifact of judge
    ordering.
* FAILURE MODES TESTED: fabricated stream (refuted — see C6); stale hits
  (refuted — C6); judge-order gaming (refuted — void-detector precedes witness
  in code, and the flip guard turns dialect-pass-without-content into FAIL);
  substring-anchor shortcut (neutralized by `path_is_constructed_target`
  equality guard; slash-bounded containment semantics disclosed in prereg §3);
  MNF bypass (control evaluated fresh per cell on the live entry snapshot;
  receipt shows entry checks 'fail' for all cells; violation trips to
  CYCLE_INCONCLUSIVE, tested).
* STATUS: **VERIFIED (observation tier, frozen ceiling)**.
* MAXIMUM DEFENSIBLE WORDING: prereg §0 verbatim — "on BOTH frozen targets
  derived from committed entries plus one confirmation pass, ONE site family,
  ONE date, bare HTTP reached verified success in <=B_PG wire transactions AND
  discriminated the out-of-range control." Never "the pagination goal class",
  never "all k", never cross-site. Independently added by this audit: "and the
  measured bodies byte-reproduce on the audit date."

### C2 — Freeze-before-outcomes discipline

* CLAIM: prereg committed BEFORE any live request of this cycle; demand spec
  filed before that; harness frozen pre-outcome; module sha pins byte-match.
* RECOMPUTATION: git chain linear `fcbeaa2(06:59) → ce70080(07:35:52 spec) →
  a2bbaaa(07:51:56 harness+tests) → e0ae931(07:55:51 FROZEN prereg) →
  88c7418(08:47:30 outcomes) → 548709d(report)`; all four pins recomputed and
  match (prereg sha256 `6958b7ef…f02c9e` = committed file = pin inside
  results/state; arm `18e1c0e6…ae07e03`; gates `8fd7e85a…e79348a1`; driver
  `a346b8f8…4343bdb`). Witness receipt `written_utc 07:56:29Z` < PREFLIGHT row
  `ts_utc 2026-08-26T07:56:29.741372+00:00` (the parity fetches land between
  them, exactly prereg §6 step order). First scored act rows follow PREFLIGHT.
  Prereg file today hashes to the pinned pre-outcome value — never amended.
* FAILURE MODES TESTED: post-hoc prereg edit (sha pin refutes); outcome-aware
  harness edits (harness commit predates prereg commit; pins bind the exact
  bytes that ran); silent backdating (commit timestamps internally consistent
  with emitted-row timestamps).
* STATUS: **VERIFIED** (with W-B2 on the unverifiable advisory GETs).

### C3 — Additivity / no mutation of accepted state

* RECOMPUTATION: `diff -rq` base↔team lists ONLY new files;
  `git diff --stat fcbeaa2..548709d` = 12 files, 2865 insertions, 0 deletions.
  Audited modules (policies, baseline, derive, gates*, pilot2, r2_cycle1,
  floor_null, registries, streams, schemas dir, docs ledgers, NEXT_RUNTIME)
  byte-untouched. Outcomes commit contains exactly the four outcome artifacts;
  report commit exactly the report. Cost-event schema hygiene: zero new
  top-level fields, zero new (arm, phase, stage, event_class) tuples vs the
  audited R2-1 stream; model_ids ⊆ {none:http-floor-v0, none:r2-harness-v0} →
  "zero provider calls" is auditor-confirmable from the stream as claimed.
* STATUS: **VERIFIED**.

### C4 — Overhead honesty (verification/recovery/maintenance accounting)

* RECOMPUTATION: step counts exclude the entry GET — disclosed with the
  qualifier riding externally quoted figures (true marginal wire cost per cell
  is entry+target = 2 transactions); CONSTRUCTION_DECISION latency 0.0 and
  negctl verify latency 0.0 are placeholders, disclosed; positive-cell verify
  eval ~0.04–0.05 ms measured natively; verification compute globally
  UNMEASURED carried as accepted C4 lineage; NO economics figure, margin/M=2
  vocabulary, reuse_yield, or cross-media arithmetic appears anywhere in
  report/results (checked); wall-clock advisory only. Free site-model endowment
  (pager tokens/templates derived offline from prior committed snapshots at
  zero measured cost) disclosed as a bias AGAINST inheritance — legitimate for
  a floor null whose comparator side it strengthens.
* FAILURE MODES TESTED: hidden overhead (placeholders are loud, not silently
  summed); double counting (confirmation pass disclosed as repeat; negctl
  excluded from quantifier; twins deduped by schema-filtered reads — W-R1-5
  rule applied in gates, twin identity clean); metric collapse into one number
  (cost vector preserved: steps|loads|advisory-wall|guards).
* STATUS: **VERIFIED AT CEILINGS** (W-B5 wording caveat).

### C5 — Fallback correctness and failure semantics

* RECOMPUTATION: frozen judge order implemented exactly as preregistered —
  transport-level error → unknown (never headroom); success mirror → VOID
  first; pinned branches (404+not-found OR 200+zero-markers) → fail; else
  unknown. `fetch()` records HTTP≥400 as clean server responses
  (`error="HTTP_<code>"` with status+body captured), so a genuine small-body
  404 reaches the witness instead of tripping inconclusive — hermetic
  regression present and passing. Behaviors outside the witness map (e.g.
  redirect-to-valid-page) fall to unknown → CYCLE_INCONCLUSIVE, honestly
  refusing to manufacture either direction. INVALID_ARM separated from
  DOMINATES; FLOOR_FAILS gated on complete well-formedness transcript with
  mandatory defect-hunt presumption. The control's
  `well_formedness_reason="transcript_incomplete"` row is BY-DESIGN (floors
  bypassed) and pre-empted in the report — correct, do not "fix".
* STATUS: **VERIFIED**.

### C6 — Authenticity and staleness (strongest available attack)

* RECOMPUTATION: from the audit sandbox, mimicking the audited transport
  (stdlib urllib, same UA), same day: `/tag/love/`, `/page/10/` (entries),
  `/page/3/`, `/page/9/` (targets), `/page/1000/` (control) fetched fresh.
  All five returned bodies hash **byte-identical** to the stream's recorded
  `entry_digest` / `body_sha256` values (full 64-hex equality on all six
  comparisons incl. KCONF). Control behavior reproduces: soft-200, 3051 bytes,
  zero quote markers → still FED today. These 10 audit-side GETs are audit
  instrumentation, NOT lane evidence, and license nothing beyond same-day
  reproducibility of the observation.
* FAILURE MODES TESTED: fabricated/hard-coded outcomes (refuted — live bytes
  match recorded hashes including latencies-plausible variance and parity
  digest cross-tie: parity live digests == prime digests within the stream);
  stale-hit inheritance from prior cycles (refuted — entries re-fetched live
  per cell, digests recorded, parity ties extractor to committed snapshots via
  oracle anchors); site drift invalidating the discriminator (not present on
  audit date; bounded by transcripts/guards as designed).
* STATUS: **VERIFIED (same-day)**.

### C7 — Tests and self-tests

* RECOMPUTATION: `pytest tests/runtime` on the team snapshot = **216 passed**
  (base alone = 182 passed; 34 new hermetic tests, substantive: genuine-404-
  not-trip, soft-200-with-content-voids, empty-render-fail, transport-unknown,
  MNF short-circuit, note whole-emission hygiene, anchor exactness, id
  collision, blinding cleanliness, all gate branches incl. sensitivity
  descriptive-only). Matches the claimed 216/216 = 182+34.
* STATUS: **VERIFIED**.

### C8 — Governance/refuse-list conformance

* RECOMPUTATION: measurement arm only (no product HTTP executor; CTO-6 §3
  flip conditions untouched, none exercised); substrate unchanged (canon host
  only under disclosed ruling R2-2-A; two-gate rule restated for JS variants/
  new sites); witnessed-effect POC correctly NOT triggered; stop-rule branch
  (b) correctly left `NOT_RECORDED_BY_RUNNER` (Director action); no census
  cycle; offline discriminability classification refused in artifact text
  (marker presence validated live only); no schema mutation (W-4 deferral
  intact); W-A2 modules untouched (deferral counter legitimately unchanged);
  mechanical timestamps throughout; hand-assembly/post-run-edit disclosure E1
  (route-totality → sampled scope) improves honesty and preserves the original
  verbatim in-file; demand-spec §1.4 sentence falsified by the outcome is
  handled by report supersession tag without amending history.
* STATUS: **VERIFIED** (W-B3 consumption caution for Director).

---

## 2. Warnings (non-blocking)

* **W-B1 — site-flavored guard key in the "generic" arm.**
  `floor_pagination.py` hardcodes the guard name `quotes_content_present`
  while claiming "NO site strings by construction". The scanned property
  (blinding fixture) is unaffected and the scan is genuinely clean, but the
  generic module is lexically coupled to the quotes canon. Rename/parameterize
  at the next module touch; do not touch it solely for this.
* **W-B2 — advisory pre-freeze GETs are unverifiable.**
  The seven disclosed unscored reachability GETs (incl. `/page/1000/`) have no
  preserved receipts; their influence is openly recorded (they informed the
  existence of failure-witness branch 1). Risk is contained because the pinned
  witness is exhaustive over plausible server behaviors {hard-404,
  soft-200-empty, soft-200-with-content→VOID, transport→unknown} and the
  void-detector-first order preserved the R2-1 kill discipline; the live pass
  decided. Future cycles that let advisory probes inform design should persist
  probe receipts.
* **W-B3 — demand-spec consumption path.**
  Spec §1.4 ("the discriminator itself is unfedable in-canon") is falsified
  for this cell class. The supersession tag lives in the report and state
  file (history unmodified — correct). The Director must consume the
  escalation package via spec §3 gating, never quote §1.4 as current truth.
* **W-B4 — confirmation pass adds near-zero information.**
  PG-KCONF's bodies are byte-identical to PG-K3F's (deterministic static
  site). Fine as a transport-repeat check; must never be counted toward
  REPLICATION/GENERALIZATION tiers (wording already discloses "plus one
  confirmation pass" — hold that line).
* **W-B5 — "1 wire transaction" headline needs its qualifier forever.**
  Steps exclude the entry GET; true marginal wire cost per cell is 2
  transactions (+ amortized parity/preflight). The qualifier is disclosed and
  binding; any future external quotation must carry it (already report-bound).
  Construction latency remains a 0.0 placeholder assertable only by anatomy.
* **W-B6 — residual trust on "untracked when patched".**
  The state-file E1/E2 disclosure ("applied PRE-commit while untracked",
  generator provenance recorded) cannot be cryptographically proven post-hoc.
  Load-bearing outcome artifacts are untouched (hashes reproduce live) and the
  edit direction was honesty-improving; acceptable, but prefer committing the
  state file before such patches or emitting patch receipts next time.

Standing obligations confirmed carried, NOT owed this cycle: W-A2 (whole-note
emission due at next `pilot.py`/`economics.py` touch — neither touched),
W-4 (http_floor arm registration due at next schema-touching change — none
occurred).

## 3. What would change this verdict

Any of the following would force REVISE/BLOCKED: prereg sha divergence from
the pinned value; a gate recompute mismatch; a stream body failing live
reproduction while claimed same-day-decisive; a found non-additive change to
audited artifacts; wording above the §0 ceiling anywhere in lane artifacts;
compression phrasing before killer (i) discharges. None found.

## 4. Provenance

* Audit mount: `/tmp/spider_runtime_team` @ `548709d` (clean).
* Base: `/home/runner/work/Spider/Spider` @ `fcbeaa2` (`runtime-audit-base`
  ≡ `origin/lab/runtime`).
* Recomputation scripts run ephemeral in `/tmp/opencode/audit329` (nothing
  written into either repo except this report and its gate JSON).
* Prior gates consulted for continuity:
  `results/audit/CYCLE_32933579869_RUNTIME_GATE.json` lineage (PASS R2-1 r1),
  standing warnings W-A1..W-A6, directive `directives/RUNTIME.md` R2-2
  priority order, rulings R2-2-A/R2-2-B, refuse list item-by-item.
