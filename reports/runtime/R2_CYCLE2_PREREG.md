# R2 CYCLE 2 — FROZEN PREREGISTRATION

Written mechanically at: 2026-08-26 07:55:19Z.
Status: **FROZEN** — committed BEFORE the first live HTTP request of this
cycle existed (freeze-before-outcomes extended to network outcomes;
W-C2-3 discipline). No pagination-floor outcome, no negative-control
outcome, and no witness-receipt artifact output had been produced or
viewed at commit time. The priority-1 demand spec was already filed and
committed (`ce70080`) BEFORE any live request of this cycle, per directive
priority order.
Cycle: R2-2 (Program R2 "Inheritance Headroom & Mechanism Floor").
GitHub run: 32940627441. Branch: `cycle/runtime/32940627441/team`.
Directive: `directives/RUNTIME.md` (R2-2 priority order 1-5). Refuse list
obeyed item by item (§9). Harness modules frozen pre-outcome:
`runtime/floor_pagination.py` (18e1c0e6225f7dd4…),
`runtime/gates_r22.py` (8fd7e85a7fee9589…),
`runtime/r2_cycle2.py` (a346b8f85373de51…). Git-orderable chain:
`fcbeaa2` accepted lane tip → `ce70080` demand spec → `a2bbaaa` harness +
tests → THIS commit → outcomes.

---

## 0. Question and branch structure

Directive R2-2 priority 2 question: *can the mechanism-floor discriminator
be made DECIDABLE on an in-canon goal class — i.e. is there a "reach page
k" target family on the SAME committed canon site where wrong inputs
verifiably fail under hard-pinned witnesses — and if so, does bare HTTP
reach every enumerated valid target within the anatomy-derived budget
(FLOOR_DOMINATES => measured in-canon impossibility backing for stop-rule
branch (b)), or does it observably fail somewhere (FLOOR_FAILS =>
falsifies the "static canon has no headroom" narrative; priority-3
witnessed-effect POC unlocks IN-CANON)?*

Four terminal classes, decided MECHANICALLY by §5:

* **FLOOR_DOMINATES** — every budgeted cell JUDGE_SUCCESS within B_PG AND
  the out-of-range negative control judged FAIL under the pinned witness
  (decidable discriminator). Scoped ceiling (binding wording): "on BOTH
  frozen targets derived from committed entries plus one confirmation
  pass, ONE site family, ONE date, bare HTTP reached verified success in
  <=B_PG wire transactions AND discriminated the out-of-range control."
  Never "the pagination goal class", never "all k", never cross-site.
* **FLOOR_FAILS** — >=1 budgeted cell judged FAIL on a WELL-FORMED final
  page (transcript complete: status 200 AND raw bytes >= MIN_DOM_BYTES AND
  >=1 parsed element AND no transport error) with the negative control fed
  and zero inconclusive-bucket cells. ONLY this branch supports browser-
  inheritance-headroom wording, and it carries a MANDATORY defect-hunt:
  on this static canon URL construction is trivially near-optimal, so a
  floor failure is presumed a harness defect until reproduced and ruled
  out; the priority-3 unlock may not be exercised before that hunt.
* **FLOOR_VOID** — the out-of-range negative control PASSED full success
  verification (soft-200/success mirror): surface non-discriminating;
  all verdicts void; escalate immediately with both voids documented
  (login-class void R2-1 + pagination void here).
* **CYCLE_INCONCLUSIVE / INVALID_ARM** — measurement-failure classes
  (health trips, transport errors, invalid targets i.e. non-200 finals,
  MNF violations, malformed transcripts, missing evidence, budget breach);
  NEVER headroom evidence in either direction; repair-first.

## 0.1 Inputs (all pre-existing, hash-pinned)

* Committed T3 entry snapshots (AUDITED_DURABLE lineage): file shas
  `f5a30604…f4621241` (taglove), `7abf039f…e1b9b0` (page10); inner page
  digests `b66af808…838f1f91` / `96d2c4a5…9787cb`. Dual pins checked at
  load by `runtime/policy_sweep.load_snapshots`; mismatch aborts.
* Audited transport/extraction layer reused UNCHANGED from R2-1
  (`floor_null.fetch/extract_snapshot/canonical_url/MIN_DOM_BYTES/
  MAX_REDIRECT_HOPS/meta_refresh_present/new_opener`).
* Shared vendored predicate dialect consumed unchanged
  (`runtime/predicates.py`) — NO new clause types anywhere. Guards are
  harness rows (R2-1 precedent), never dialect extensions.
* Frozen blinding fixture `runtime/schemas/policy_blinding_tokens.json`.
* Parity preflight reuses the audited `r2_cycle1.parity_check()`
  verbatim (additive import; module untouched).

## 1. Director rulings disclosed (binding framing)

* **R2-2-A**: adding measurement TASKS on sites already inside the
  committed canon, with exact task/URL lists frozen pre-outcome and
  disclosed here, is NOT substrate expansion. The canon site is
  quotes.toscrape.com; the cells below add NO new site, NO new
  site-family, NO new distribution — targets are pure constructions on
  the SAME host whose two entries carry the committed snapshots.
* **R2-2-B**: offline affordance ENUMERATION admissible; offline
  DISCRIMINABILITY classification refused (server-behavior property,
  R2-1-proven). Accordingly §3 pins witnesses MECHANICALLY; nothing here
  claims to know server behavior before the live pass.

## 2. Cells (FROZEN enumeration; disjoint `PG-` namespace)

| run_id | entry | construction | mode |
|---|---|---|---|
| PG-K3F | https://quotes.toscrape.com/tag/love/ | `/page/3/` | budgeted_cell |
| PG-K9B | https://quotes.toscrape.com/page/10/ | `/page/9/` | budgeted_cell |
| PG-KCONF | https://quotes.toscrape.com/tag/love/ | `/page/3/` | budgeted_cell (confirmation pass, repeat of K3F) |
| PG-NEGCTL-OOR | https://quotes.toscrape.com/tag/love/ | `/page/1000/` | negative_control (excluded from budget quantifier) |

Construction rule (pure; zero probing): `scheme://netloc(canonical entry)
+ /page/{k}/`. NEGCTL k=1000 chosen far out-of-range for robustness to
dataset growth (an adjacent boundary value could drift into range).
Fresh cookie jar/opener PER CELL. NO retries this cycle (single-step
anatomy; a transport blip terminates honestly CYCLE_INCONCLUSIVE —
selective retry could bury a failing-to-fail control, which is refused).

## 3. Hard-pinned witnesses (frozen BEFORE any outcome)

**Success effect** per budgeted cell k — JUDGE_SUCCESS := dialect state
'pass' AND all structural guards true AND no trip, where:

* dialect pred `rt.tasks:pagination_reach@v0(k)` =
  `{host_allowlist:[quotes.toscrape.com], url_anchor:["/page/{k}/"],
  elem_text_any:["Next →","← Previous"]}`;
* guards: `http_status_200`, `path_is_constructed_target`
  (norm_path(final)==norm_path(constructed); both sides recorded),
  `no_transport_error`, `quotes_content_present` (raw body contains
  >=1 occurrence of marker `class="quote"`);
* positive-path health floors (entry AND final pages): status 200 AND raw
  bytes >= MIN_DOM_BYTES=1200 AND no meta-refresh (mirrors R2-1 success
  path). A guard contradiction over a dialect hit judges FAIL (the
  claimed effect observably did not occur), never PASS.

Pager tokens are BYTE-EXACT rendered strings DERIVED MECHANICALLY from
the committed snapshots by the adjacency rule (anchor href == immediate
N±1 sibling of the entry's own path; entry without page segment treated
as page 1 → `<dir>page/2/`), because the vendored dialect uses EXACT
membership on element text and hand-typed ASCII guesses provably miss the
glyphs. Derivation receipt written pre-outcome to
`results/runtime/probes/pagination_witness_derivation_r22.json`
(extracted set `['Next →','← Previous']` must equal the frozen set;
MNF entry-checks must be 'fail' on both entries for both k in {3,9};
anchor-must-match-target assertions true). Any mismatch aborts pre-run.

Anchor-semantics scope note (pinned): slash-bounded matching is substring
containment inside the normalized path (e.g. `/tag/love/page/2/` would
match anchor `/page/2/`). This is neutralized HERE by (i) the frozen
enumeration (entries never satisfy their own target anchors — verified
offline for every cell) and (ii) the `path_is_constructed_target`
equality guard. Recorded so a future reuser cannot treat the anchor alone
as root-anchored.

**Failure witness** for PG-NEGCTL-OOR — pinned disjunction (status-code +
body predicate, hard):

* branch 0: HTTP status == 404 AND case-insensitive body containment of
  `"not found"`; OR
* branch 1: HTTP status == 200 AND raw-body count of `class="quote"`
  occurrences == 0 (route-total EMPTY render — observably NOT the
  reached-page effect);

with the FULL success verification evaluated FIRST as the void-detector:
if the out-of-range response passes dialect+guards+content exactly like a
budgeted cell would, judge 'pass' => **FLOOR_VOID** (soft-200 mirror,
directive auto-VOID rule). Judge order FROZEN: transport-level error →
'unknown' (inconclusive; environment property, NOT discriminability);
void-detector 'pass' → 'pass'; pinned-witness match → 'fail'; otherwise
'unknown'. The negative control BYPASSES the MIN_DOM_BYTES/meta-refresh
positive-path floors BY CONSTRUCTION (a genuine small 404 must judge
FAIL, never trip). HTTP-status error responses (fetch records
`error="HTTP_<code>"` while capturing status+body) are CLEAN server
responses and reach the witness branches; only transport-level failures
are 'unknown'.

## 4. Procedure per cell (FROZEN)

1. Entry GET — the LOAD analogue, NOT a step (mirrors browser arms where
   goto increments loads). Health: status 200 AND raw bytes >=1200, else
   HEALTH_TRIP ENTRY_UNHEALTHY.
2. MUST-NOT-FIRE (REDUCED control — R2-2 design fix): applicability-mode
   evaluation of the url_anchor-ONLY pred `["/page/{k}/"]` on the ENTRY
   snapshot; semantics "the constructed target effect must not already
   hold at the current URL". state=='pass' ⇒ MUST_NOT_FIRE_VIOLATION
   (trip, cell invalid); state!='fail' (unknown) ⇒ indeterminate trip.
   Reason token kept verbatim for gate consumption. (The R2-1 token-
   absence transplant would trip on EVERY cell here: pager affordances
   exist on every family page including entries.)
3. CONSTRUCTION_DECISION retrieval row: entry_final_url, k, template,
   constructed_url, probing=none_by_construction (auditor-recomputable).
4. Constructed-target GET — 1 step. Manual redirect walk <=5 hops
   (MAX_REDIRECT_HOPS), each hop 1 observed step; nav_chain[0] is the
   TARGET GET's response URL (never empty — the shared dialect's
   nav-chain integrity fails on an empty chain), then each hop URL.
5. Judge per §3; tri-value judge state + guards + WELLFORMEDNESS
   TRANSCRIPT (final_status, final_raw_bytes, n_parsed_elements,
   content_marker_count, min_dom_bytes_floor, transport_error,
   nav_chain_paths) recorded IN the verify row; native eval ms measured
   (W3 lineage).
6. Summary row cost.actions==steps; twin-dual emission; notes emitted
   WHOLE with round-trip assertion; NOTE_SANITY_MAX loud-abort (RF-2).

## 4.1 Cost accounting (FROZEN)

Primary unit: wire transactions after the entry GET (constructed GET +
redirect hops; transport retries excluded — none exist under the
no-retry rule). Four-column reporting per cell: steps | loads(=1 entry)
| wall-clock (advisory only) | guards. NO network-efficiency or
bytes-on-wire claim in EITHER direction. Margin/M=2 vocabulary BANNED
(browser-unit comparator family only). Cross-media arithmetic, if
recorded at all, is DESCRIPTIVE-ONLY and banned from prose (W-1).

## 4.2 Budget (FROZEN derivation, not calibration)

`B_PG = 1 + MAX_REDIRECT_HOPS = 6`: expected anatomy path = ONE
constructed-target GET (1); slack = manual redirect walk (<=5 observed
hops); no discovery reserve exists because discovery is pure
construction. NOT derived from SPIDER's 4-action comparator; sensitivity
at B in {1..6} reported descriptively and NEVER verdict-flipping.

## 5. Gates and decision rule (FROZEN; self-tested outcome-blind)

All gates computed BY CODE from the event stream (`runtime/gates_r22.py`,
committed BEFORE any live request; `self_test()` proves the identical
code decides fabricated streams of ALL branches — dominates /
fails_wellformed / void_soft200_mirror / negctl_transport_unknown /
health_trip / invalid_target / malformed_transcript / invalid_arm /
mnf_violation):

* **G-PG0** per-cell stream consistency (P5'): exactly one verify row
  keyed by the cell id, exactly one summary row, summary actions ==
  actN count; twin-dedup counting via schema-filtered reads (W-R1-5).
* **G-PGa** success structure: JUDGE_SUCCESS on EVERY budgeted cell
  (tri-value roll-up; boolean flattening prohibited).
* **G-PGn** negative control tri-value: 'fail' ⇒ fed; 'pass' ⇒
  FLOOR_VOID; anything else ⇒ CYCLE_INCONCLUSIVE. VOID precedence FIRST
  (mirrors the audited gate ordering).
* **G-PGb** three-outcome rule per §0 (DOMINATES / FAILS-with-transcript
  / INCONCLUSIVE / INVALID_ARM), B_PG=6, sensitivity descriptive.
* Substrate decision wording (binding ceiling): §0 DOMINATES paragraph
  verbatim; branch-(b) recording remains DIRECTOR action, scoped to this
  cell class, with the login-class void carried void-caveated (a voided
  discriminator decides nothing — R2-1 rule; stop-rule branch (b) stays
  gated exactly as the filed demand spec states).

## 6. Preflight (pre-outcome infrastructure checks; authorized fetches)

Executed AFTER this commit and BEFORE any scored request; failures ABORT
the cycle with zero floor outcomes:

1. Offline witness self-check vs COMMITTED snapshots (zero requests):
   token derivation equality, MNF entry-checks 'fail', anchor/target
   matches; receipt persisted.
2. Blinding scan of BOTH new modules against the frozen fixture — clean
   required, NO exemption block exists this cycle (the modules carry no
   task-spec strings by construction; task constants live in the driver
   layer, same placement as audited pilot2 constants).
3. Live parser parity reusing audited `r2_cycle1.parity_check()`:
   both entries fetched, committed-snapshot oracle anchors matched under
   the shared extractor; n_oracle >=1 per entry. Residual disclosed:
   static HTML parsing cannot reproduce computed-style visibility
   (carried R2-1 limitation; mitigations here are the reduced-MNF row,
   the out-of-range control, the content-marker guard, and transcripts).

## 7. Pre-freeze advisory observations disclosure (NON-EVIDENCE)

Before freezing, a fresh-context critical-challenge subagent performed
SEVEN unscored reachability GETs (3 on quotes.toscrape.com incl.
`/page/1000/`, `/page/11/`, `/page/10/`; 4 on books.toscrape.com
catalogue paths) and REPORTED: quotes out-of-range renders soft-200 with
an EMPTY quote list; books catalogue exhibits hard-404 beyond its last
page. These are OPERATIONAL_DIAGNOSTIC-tier advisory observations from
outside this cycle's evidence channels: they are NOT accepted evidence,
they gate NOTHING, and the frozen witnesses above do not DEPEND on them
(both disjunct branches are pinned mechanically and the live pass
decides). They are disclosed verbatim to prevent any impression of hidden
pre-knowledge, and they DID inform one design choice, recorded openly:
the failure witness carries the empty-render branch so the cell remains
DECIDABLE even if the quotes route is total (soft-200-empty ⇒ branch 1
FAIL; soft-200-WITH-content ⇒ VOID-detector fires; hard-404 ⇒ branch 0).
Expectation recorded for honesty: under the advisory reading, DOMINATES
is the expected outcome. If reality differs, the gates decide as frozen.
No books.toscrape.com request occurs in this cycle (its gating-cell
proposal lives in the filed demand spec awaiting Product/CTO input).

## 8. Analysis plan / what would change our mind

Mechanical gate evaluation (§5) is the PRIMARY analysis. DOMINATES ⇒
report records the §0 scoped wording + measured backing note for the
Director's branch-(b) record + escalation formally standing per the
filed demand spec. FAILS ⇒ mandatory defect-hunt replication BEFORE any
priority-3 unlock exercise (hunt protocol: rerun failing cell read-only,
re-extract transcript, compare against committed snapshots; verdict
retraction if any transcript field flips). VOID or INCONCLUSIVE ⇒
escalation with void(s) documented; repair-first; no substrate inference.

## 9. Wording ceilings & refusals honored

* X31 holds: NO compression phrasing leaves observation tier until BOTH
  killers discharge. This cycle can discharge killer (ii) AT MOST (and
  only via DOMINATES-with-fed-control on THIS cell class).
* Floor verdicts scoped to: one site family, one date, one goal class,
  three live passes + one control, one scripted implementation. Never
  "the Web", never "agents".
* Wall-clock advisory; model independence UNFALSIFIABLE (zero provider
  calls); reuse_yield UNDEFINED; no economics quotation anywhere.
* Refuse list honored item-by-item: measurement arm only (NO product HTTP
  executor; CTO-6 §3 flip conditions unmet); no substrate expansion (canon
  site only; ruling R2-2-A disclosed; new sites await the demand-spec
  decision); no replication of killed observations; no second caller; no
  MCP/SDK/wire freeze; no Pareto engine; no TTL/confidence machinery; no
  delta-repair executor; no new cost_event fields or enum values; no
  schema mutation (W-4 http_floor registration stays deferred until the
  next schema-touching change — none occurs this cycle); audited lane
  artifacts byte-untouched (policies.py, baseline.py, derive.py, gates.py,
  pilot2.py, gates_r1/gates_r2/r1_strong/r2_cycle1/floor_null, registries,
  streams, preregs, reports); no census cycle; no offline discriminability
  classification claim; no hand-written timestamps in lane state files;
  W-A2 whole-note fix owed at next pilot.py/economics.py touch — neither
  module is touched this cycle (deferral counter unchanged, still once).

## 10. Disclosed limitations

* One site family/date; drift bounded by parity+guards+transcripts, not
  eliminated. Site behavior may differ from any advisory observation —
  the gates decide, not the expectations.
* Anchor substring semantics neutralized only within the frozen
  enumeration (§3 scope note).
* Static-parser visibility limit carried (§6.3 residual).
* Single scripted implementation; urllib default User-Agent; no cache
  handler (frozen invariant).
