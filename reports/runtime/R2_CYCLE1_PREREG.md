# R2 CYCLE 1 — FROZEN PREREGISTRATION

Status: **FROZEN** — committed BEFORE the first live HTTP request of this
cycle existed (freeze-before-outcomes extended to network outcomes; W-C2-3
discipline). No floor outcome, no negative-control outcome, and no
URL-arm artifact output had been produced or viewed at commit time.
Cycle: R2-1 (Program R2 "Inheritance Headroom & Mechanism Floor").
GitHub run: 32928419260. Branch: `cycle/runtime/32928419260/team`.
Directive: `directives/RUNTIME.md` (R2 priority order 1–5). Refuse list
obeyed item by item (§9).
Harness frozen at commit `b4254a6` (this file pins its tree state; the
git-orderable chain is `917bbf8` → `b4254a6` harness → THIS commit →
outcomes).

---

## 0. Question and branch structure

Program R2 discriminating question (chartered): *does any goal class
reachable by this lane's substrate retain strictly positive verified-
inheritance value over BOTH (i) the strongest memory-free scripted
comparator family extended with URL-construction arms and (ii) a direct-
HTTP mechanism-floor null; and on any surviving class, does witnessed-
effect addressing capture that value within total measured overhead?*

This cycle executes priority 1 ONLY (the cheapest decisive discriminator)
plus the priority-3 decision. Three outcome branches, decided MECHANICALLY
by §4:

* **B-FLOOR-DOMINATES** — bare HTTP solves the login goal class within the
  anatomy-derived budget on every enumerated cell → this cell class has
  ZERO browser-inheritance headroom regardless of addressing scheme;
  substrate relocation becomes mandatory BEFORE any further mechanism
  work (directive branch); witnessed-effect POC is REFUSED here.
* **B-FLOOR-FAILS** — at least one cell produces a well-formed final page
  with judge state FAIL (and no inconclusive/health-tripped cells) →
  genuine headroom exists; priority 2 may proceed on floor-failure cells
  in a successor cycle chosen by floor failure, not convenience.
* **B-INCONCLUSIVE / B-INVALID-ARM / B-FLOOR-VOID** — measurement failure
  classes; NEVER headroom evidence in either direction.

Interpretation note (frozen): "the two committed entry snapshots" cannot
literally host an HTTP arm (snapshots are not servers). The two budgeted
cells are therefore LIVE runs anchored at the same entry URLs whose
browser snapshots are committed (`/tag/love/`, `/page/10/`); the committed
snapshots serve as pre-outcome parser-parity fixtures (§5) and their dual
pins are checked at load. This reading is disclosed, not silent.

## 0.1 Inputs (all pre-existing, hash-pinned)

* Committed T3 entry snapshots (AUDITED_DURABLE lineage): file shas
  `f5a30604…21241` (taglove), `7abf039f…e19b0` (page10); inner page
  digests `b66af808…838f1f91` / `96d2c4a5…9787cb`. Dual pins checked at
  load by `runtime/policy_sweep.load_snapshots`; mismatch aborts.
* Shared task fills spec (`pilot2.FILLS`: username spiderbot / password
  notasecret) — byte-identical information to every browser arm; asserted
  by `fills_identity()` preflight.
* Frozen blinding fixture `runtime/schemas/policy_blinding_tokens.json`
  (sha256 recorded into the URL-arm artifact).
* SUCCESS predicate `rt.tasks:quotes_login_success@v1` = {host_allowlist
  [quotes.toscrape.com], elem_text_any ["logout"]} and precondition
  `rt.capsules:quotes_login_precondition@v1` = {elem_text_any ["login"]},
  both consumed UNCHANGED through the ONE vendored dialect
  (`runtime/predicates.py`). No new clauses anywhere.

## 1. Priority 1a — OFFLINE URL-construction comparator-family record

Additive module `runtime/policies_r2.py`; the accepted R1 sweep artifact
`policy_sweep_r11.json`, its winner `goal_href|root0`, and
`runtime/policies.py` remain BYTE-UNTOUCHED (verified by test).

Arm `url_construct_account_route` (FROZEN):
* Construction rule: `<entry scheme>://<entry host>` + `/login`. Path
  segment from the SAME generic account-route token class as
  `policies.HREF_RE`/`policies.LEXICON`; single-shot deterministic; no
  probing, no page content consumed.
* Browser-sim anatomy (comparator arithmetic only — NO live browser run
  this cycle): goto(constructed)=LOAD + fill + fill + click-submit =
  **3 actions / 2 loads**.
* Floor anatomy: login GET + credential POST + redirect GET = **3 wire
  transactions**.
* GATING: NONE. Descriptive record per committed entry only
  (`results/runtime/probes/url_arms_r21.json`). No survival semantics,
  no re-ranking of the frozen R1 grid, K1/K2 untouched.
* Blinding attestation: module source mechanically scanned against the
  FROZEN fixture (site strings/credentials/capsule ids/witness refs must
  be absent BY CONSTRUCTION); "login" is generic affordance vocabulary
  per the fixture's own design note.

## 2. Priority 1b — DIRECT-HTTP MEASUREMENT ARM (mechanism-floor null)

Placement discipline: `runtime/floor_null.py` is headed MEASUREMENT ARM
ONLY — NOT A RUNTIME EXECUTOR (refuse-list grep surface); stdlib only
(urllib/cookiejar/html.parser); no browser launch anywhere in this cycle
(`browser_launches: 0` recorded).

### 2.1 Cells (FROZEN enumeration; disjoint `FLR-` namespace)

| run_id | entry | mode |
|---|---|---|
| FLR-T3P1 | https://quotes.toscrape.com/tag/love/ | budgeted_cell |
| FLR-T3P2 | https://quotes.toscrape.com/page/10/ | budgeted_cell |
| FLR-CONFIRM-P2 | https://quotes.toscrape.com/tag/love/ | budgeted_cell (confirmation pass) |
| FLR-NEGCTRL | …/tag/love/, WRONG password `wrongpass` | negative_control (excluded from the budget quantifier) |

Fresh cookie jar/opener PER CELL (no session bleed). One deterministic
health-trip retry permitted (both original rows preserved append-only);
retries excluded from step counts under the frozen exclusion-row rule.

### 2.2 Procedure per cell (FROZEN)

1. GET entry (the LOAD analogue — NOT a step; mirrors browser arms where
   goto increments loads, not actions). Health: status 200 AND raw body ≥
   MIN_DOM_BYTES=1200 (same numeric floor as browser arms; raw-response
   bytes ≠ serialized-DOM bytes — never compared across media).
2. MUST-NOT-FIRE control (pre-action): success tokens ("logout") must NOT
   match the entry snapshot via applicability-mode evaluation; violation ⇒
   cell invalid (trip row), never success.
3. Applicability row: LOGIN_PRECOND evaluated ON THE ENTRY SNAPSHOT via
   `evaluate_applicability` (entry-context affordance-witness semantics;
   W-C2-2 lineage). fail/unknown ⇒ trip row, no POST ever.
4. Discovery (zero transactions): affordance-cascade over parsed anchors
   using `policies.HREF_RE`; if candidates exist they are probed in order;
   ONLY IF none yields a form, the alphabetical convention paths
   `/auth, /log-in, /login, /signin, /sign-in` are probed. EVERY probe
   fetch counts one step (misses included).
5. Form identification: first fetched page containing BOTH a username-ish
   text input and a password input (`find_login_form`, structural rule,
   auditor-checkable from notes). None ⇒ FLOOR_FAIL (well-formed pages).
6. POST body (FROZEN echo policy): ALL hidden inputs copied VERBATIM
   (csrf_token safe — no site values hardcoded; policy not answers) +
   shared fills mapped to name-hinted fields; urlencoded; form method/
   action respected.
7. Submit (1 step) + MANUAL redirect walk ≤5 hops, each hop 1 observed
   step; nav_chain := observed hop URLs after the entry GET.
8. Judge: `evaluate_predicate(SUCCESS_PRED, final_snap, nav_chain)` on the
   html.parser-built snapshot; tri-value state recorded; native eval ms in
   verify row (W3 lineage). Guards recorded as rows: status==200,
   NO_LOGIN_FORM_ON_FINAL, set-cookie-seen, no-cache-handler.
   JUDGE_SUCCESS := state=='pass' ∧ all guards ∧ no trips.
9. Negative control: identical recipe, password `wrongpass`; expected
   judge FAIL. If it PASSES verification ⇒ surface non-discriminating ⇒
   FLOOR_VOID (all floor verdicts void, nothing flips).

### 2.3 Cost accounting (FROZEN)

Primary unit: **wire transactions after the entry GET** (probe misses,
POST, redirect hops included; transport retries excluded). Four-column
reporting contract per cell: steps | loads(=1 entry) | wall-clock
(advisory only) | guards. NO network-efficiency or bytes-on-wire claim may
be derived from this cycle in EITHER direction (browser loads hide
sub-resource fanout; floor requests are naked). Margin/M=2 vocabulary is
BANNED in all floor gates (browser-unit comparator family only).

### 2.4 Budget (FROZEN derivation, not calibration)

`B_FLOOR = 6`: expected anatomy path = login GET (1) + POST (2) +
redirect GET (3); slack +1 discovery miss (4); reserve (5–6). NOT derived
from SPIDER's 4 browser actions; sensitivity at B ∈ {3,4,5,6} reported
descriptively and NEVER verdict-flipping.

## 3. Priority 3 — WB-CONSUMER CELL DECISION: QUARANTINE

Decision made PRE-OUTCOME (recorded here so the report cannot strengthen
or weaken it post hoc):

**QUARANTINE — the write-back tier stays NON-DEFAULT with no consumer
evidence owed**, exactly per directive R2-1 priority 3 alternative. The
verbatim minimal consumer-cell design of the R1-1 prereg §3.3 (T1 goal
text; ONE paired cell resolved against wb-v2 vs parent-resolved; same
executor; stream-counted actions primary; paired health-retry only; both
outcome directions meaningful) remains preserved BY REFERENCE to that
frozen prereg for any future authorized execution; nothing is re-frozen
or mutated here.

Grounds recorded honestly: (i) this run environment lacks the browser
stack entirely (no playwright module; OPERATIONAL_DIAGNOSTIC fact, not a
scientific result), making live execution impossible without heavyweight
provisioning; (ii) under the expected floor-dominating outcome the parent
arm itself is dominated on this goal class, so §3.3's decisive condition
could not yield interpretable value this cycle. Consequences that BIND:
`reuse_yield` stays UNDEFINED (E3 lineage); NO economics figure is quoted
anywhere (W-R1-1 flow-weighting requirement stands; X31 wording ceiling
stands); the quarantined `-wb` registry and both capsules stay CANDIDATE.

## 4. Gates and decision rule (FROZEN; self-tested outcome-blind)

All gates computed BY CODE from the event stream (`runtime/gates_r2.py`,
committed at `b4254a6` before ANY live request; `self_test()` proves the
identical code decides fabricated streams of ALL branches):

* **G-FLOOR0** per-cell stream consistency (P5'): exactly one verify row,
  exactly one summary row, summary actions == actN count; twin-dedup
  counting via schema-filtered reads (W-R1-5).
* **G-FLOORa** success structure: JUDGE_SUCCESS on EVERY enumerated
  budgeted cell (tri-value roll-up — boolean flattening prohibited).
* **G-FLOORb** three-outcome rule:
  - `FLOOR_DOMINATES` ⟺ G-FLOORa ∧ max(steps) ≤ B_FLOOR=6;
  - `INVALID_ARM` ⟺ G-FLOORa ∧ max(steps) > B_FLOOR (measurement
    failure — never scored as floor-failure/headroom);
  - `CYCLE_INCONCLUSIVE` when any non-successing cell is INCONCLUSIVE /
    health-tripped (never headroom evidence);
  - `FLOOR_FAILS` otherwise (≥1 well-formed final page judged fail) —
    the ONLY branch supporting browser-inheritance-headroom wording.
* **G-FLOORn** negative control must judge FAIL else `FLOOR_VOID`.
* Substrate decision wording (binding ceiling): "on the quotes-login goal
  class (ONE site family, ONE date, three live passes), bare HTTP reaches
  verified success in ≤B steps ⇒ ZERO browser-inheritance headroom on
  THIS cell class; witnessed-effect addressing on this class REFUSED."
  Cell-class death is NOT program-R2 completion and NOT stop-rule (b);
  succession requires the Director-recorded bottleneck re-measurement and
  Product/CTO demand input for substrate expansion (outside lane
  self-authorisation).

## 5. Preflight (pre-outcome infrastructure checks; authorized fetches)

Executed AFTER this commit and BEFORE any credential POST; failures ABORT
the cycle with zero floor outcomes:

1. Parser parity: live-fetch both entries, parse with the floor extractor,
   require every committed-snapshot oracle anchor to appear with matching
   href-path OR normalized text; also require n_oracle ≥ 1 per entry.
   Residual disclosed: static HTML parsing cannot reproduce computed-style
   visibility; mitigations are the must-not-fire control, the wrong-
   password negative control, and the no-login-form-on-final guard.
2. Blinding scan of BOTH new modules against the frozen fixture.
3. Shared fills identity assertion.

## 6. Analysis plan / what would change our mind

Primary analysis = mechanical gate evaluation (§4). B-FLOOR-DOMINATES ⇒
SUBSTRATE_DECISION record written with the §4 scoped wording + two binding
notes for R2-2: (i) the convention-path prior must migrate into the
strongest-comparator canon (`goal_href|root0` + URL-construction arms +
convention arm) or the next margin repeats the K3 lesson; (ii) JS-gated /
non-GET-affordance goals are the candidate relocation substrate; any
in-family candidate requires Director family-membership ruling BEFORE use,
and any expansion requires frozen task/site lists pre-outcome.
B-FLOOR-FAILS ⇒ successor cycle selects cells by floor failure.
B-INCONCLUSIVE/-INVALID-ARM/-VOID ⇒ repair-first; no substrate inference.

## 7. Wording ceilings (bound on ALL reports of this cycle)

* X31 holds: NO compression phrasing leaves observation tier until BOTH
  killers discharge (strongest-comparator margin ≥ M AND mechanism-floor
  non-domination). This cycle can discharge killer (ii) at most.
* Floor verdicts are scoped to: one site family, one date, one goal
  class, three live passes, one scripted implementation. Never "the Web",
  never "agents", never cross-site generalization.
* Wall-clock advisory; model independence UNFALSIFIABLE (no provider
  calls); reuse_yield UNDEFINED; no economics quotation.
* Browser-sim action arithmetic (3 vs SPIDER's 4) is comparator
  ARITHMETIC recorded offline — never a live performance claim.

## 8. Refusals honored this cycle

No route-tier HTTP executor productized (measurement arm only; CTO-6 §3
flip conditions unmet); no substrate expansion (no new site/task lists);
no replication of killed observations; no second caller; no MCP/SDK/wire
freeze; no Pareto engine; no TTL/confidence machinery; no delta-repair
executor; no new cost_event fields or enum values (notes carry payloads);
no schema mutation (v0 frozen; logged /v1 candidates untouched); no edits
to audited lane artifacts (policies.py, baseline.py, derive.py, gates.py,
pilot2.py, gates_r1.py, r1_strong.py, accepted registries/streams all
byte-untouched); no registry infrastructure beyond hashed directories; no
reuse_yield quotation; no live browser launches; no compression phrasing
before both killers discharge.

## 9. Disclosed limitations (priority 1)

* One site family/date; drift bounded by parity+guards, not eliminated.
* Static parser visibility limit (§5 residual).
* The convention list contains the answer route for this family —
  mitigated by affordance-cascade-first ordering, alphabetical fallback,
  per-probe recording, and the budget cap; bias direction AGAINST
  inheritance is deliberate and disclosed.
* Single scripted implementation; model independence untested by design.
* urllib default User-Agent; no cache handler (frozen invariant, noted).

---

## 10. PRE-OUTCOME CORRECTION ADDENDUM (committed before ANY live request)

Disclosure: the first driver start ABORTED at blinding preflight with ZERO
live requests made and ZERO outcomes produced. Cause: §5.2 as written
scanned both new modules against the frozen fixture without noting that
the vendored predicate REF STRINGS (`rt.tasks:quotes_login_success@v1`,
`rt.capsules:quotes_login_precondition@v1`) are members of the fixture's
forbidden-token list (`rt.tasks`, `rt.capsules`). These tokens name the
SHARED task judge and appear verbatim in every audited harness module of
this lane (`pilot2.py`, `r1_strong.py`, `gates_r1.py`); the fixture's own
design note scopes it to CAPSULE KNOWLEDGE leakage into memory-free
POLICIES ("nor in its runtime inputs beyond the shared task-spec echo" —
R1-1 prereg §2.2 lineage).

Correction (mechanical, no scientific target/benchmark/outcome-rule
change): `blinding_preflight` now records the RAW scan alongside a
documented exemption for the two predicate-ref namespace prefixes; site
strings, credentials, capsule ids, witness refs remain forbidden and were
never present. Raw + filtered scans are serialized into the PREFLIGHT
event row for auditor re-derivation. This addendum is committed BEFORE
the first live request; the freeze chain remains git-orderable:
`917bbf8` → `b4254a6` harness → `5dd51ab` prereg → THIS correction →
outcomes.
