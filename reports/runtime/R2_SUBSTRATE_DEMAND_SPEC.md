# R2 SUBSTRATE DEMAND SPEC — Runtime lane → Product / CTO

Status: **FILED** by TEAM RUNTIME (Runtime Runner) at cycle R2-2
(GitHub run 32940627441). Filed FIRST, before any live request of this
cycle existed, per `directives/RUNTIME.md` Program R2 priority order item 1.
Written: 2026-08-26 07:35:38Z (mechanical).

**Scope of this document:** it packages ALREADY-ACCEPTED negative evidence
and states DEMANDS/DECISIONS that belong to Product/CTO portfolio authority.
It creates **NO new claims**, quotes **NO economics figures**
(X31 / W-R1-1 / E3 discipline), performs **no substrate expansion**, and
asserts **no server-behavior property** beyond what an audited cycle
already measured. Its content is measurement-invariant by design
(Director ruling R2-2-B): nothing pending in this lane can strengthen or
weaken it.

---

## 1. Measured impossibility record (accepted evidence only)

### 1.1 Canon affordance enumeration receipt

The committed canon of this lane is ONE site family measured on ONE date,
with two committed entry snapshots (dual-pinned, verified at load):

* `results/runtime/probes/entry_snapshot_taglove.json`
  (file sha256 `f5a30604…f4621241`, inner digest `b66af808…838f1f91`);
* `results/runtime/probes/entry_snapshot_page10.json`
  (file sha256 `7abf039f…e1b9b0`, inner digest `96d2c4a5…9787cb`).

Offline enumeration over both committed snapshots (reproducible by
`runtime/policy_sweep.load_snapshots()` + any auditor's own counter):

* entry `/tag/love/`: **57 interactive elements, all `<a>`; zero form-like
  elements** (`form/button/input/select/textarea` count = 0);
* entry `/page/10/`: **44 interactive elements, all `<a>`; zero form-like
  elements**.

The canon's ONLY POST-affording surface is the login route reached from
the persistent header anchor. Its behavior is not merely unmeasured — it
is **void-proven credential-non-discriminating**:

### 1.2 K1 comparator parity (R1-1, AUDITED_DURABLE)

The near-repeat work-compression observation does NOT survive its strongest
frozen scripted comparator (`goal_href|root0` + counterbalanced passes):
SPIDER 4 vs STRONG 4 stream-counted browser actions on all four paired
passes, margin 0 < M=2 (`docs/RUNTIME_LEDGER.md` §R1 CYCLE 1, result K1,
SURVIVES_AUDIT). The strongest comparator family was subsequently extended
with URL-construction arms recorded descriptively (R2-1 URLA) — margins
can only get worse for inheritance, never better, under the extended set.

### 1.3 Mechanism-floor void (R2-1 FLR, AUDITED_DURABLE)

The direct-HTTP mechanism floor executed live on the quotes-login goal
class (stdlib only, zero browser launches): every budgeted cell AND the
wrong-password negative control passed verification identically
(`FLOOR_VOID`) — the environment accepts ANY credentials there, so the
direct-HTTP surface cannot discriminate success from failure on that class
(`docs/RUNTIME_LEDGER.md` §R2 CYCLE 1; substrate decision
`NO_SUBSTRATE_DECISION_VOID`). Retroactive scoping also accepted there:
all prior browser-side login-cell economics measured FORM-COMPLETION, not
authenticated sessions.

### 1.4 Why this blocks honest mechanism work in-lane

Every candidate mechanism this lane could build next (witnessed-effect
addressing, cheap verifiers, fallback shaping) needs a substrate where a
WRONG input observably fails; otherwise verification cannot distinguish
inherited competence from environmental permissiveness (the R2-1 lesson:
a seductive FLOOR_DOMINATES reading was refused by the pre-frozen wrong-
input control). Within the current canon, the one POST affordance is
proven non-discriminating and the committed snapshots enumerate zero other
mutation affordances. **The discriminator itself is unfedable in-canon;
this is a measured property of the accepted substrate, not a hypothesis.**

---

## 2. Candidate classes where wrong inputs are EXPECTED to fail
(hypotheses for authorization — discriminability deliberately UNCLASSIFIED)

Per Director ruling R2-2-B, offline DISCRIMINABILITY classification from
committed snapshots is refused (server-behavior property, R2-1-proven).
The classes below are therefore named as **hypothesized-fail candidates**;
each would be decided live ONLY after authorization, using the same
hard-pinned expected-fail-control protocol that R2-1 froze (wrong-input
negative control MUST verifiably fail under pre-pinned status/body
witnesses before any positive claim is licensed).

For each class we provide the exact proposed site/task lists required for
an expansion authorization. Any authorization decision should freeze these
lists unchanged into a successor-cycle preregistration.

### Class A — JS-gated rendered flows (in-family; TWO gates required)

* Proposed sites/tasks (same registered host family as the canon):
  * `https://quotes.toscrape.com/js/` — task "reach page k of the
    JS-rendered quote list"; expected-fail probe: target beyond rendered
    range under raw-HTML parsing (content absent without JS execution);
  * `https://quotes.toscrape.com/scroll/` — task "retrieve quote block N
    under infinite scroll"; expected-fail probe: content absent from raw
    HTML at depth N.
* GATES REQUIRED BEFORE ANY USE (both, explicitly): (1) Director
  family-membership ruling — these variants were never snapshotted, so
  they may constitute a new DISTRIBUTION even on the canon host (R2-1
  prereg §6 rule); (2) Product/CTO demand input per the refuse list.
  This lane will NOT self-authorize either gate.

### Class B — Server-side-validated credential forms (NEW sites required)

* Proposed sites (public QA sandboxes, outside current canon — expansion):
  * `https://the-internet.herokuapp.com/login` — task "authenticate with
    the documented demo account"; hypothesized wrong-input failure:
    observable error state after invalid submission;
  * `https://www.saucedemo.com/` — task "authenticate as the standard
    user"; hypothesized wrong-input failures: error banner on bad
    credentials; locked-account message on the locked user.
* These names carry NO behavioral claim today. Their discriminating
  status would be established by the pinned-control protocol at execution
  time, exactly as R2-1 did for the canon login (and could still VOID).

### Class C — Non-GET-affordance mutations with observable rejection

* Proposed shape: forms whose server-side validation re-renders with
  field-level errors on invalid submissions (candidates exist inside the
  Class B sites' flows). Same protocol, same refusal to classify offline.

---

## 3. Stop-rule branch-(b) gating statement (explicit)

Stop-rule branch (b) wording ("no inheritance-positive cell class exists
within reachable substrate") remains **GATED** on this cycle's priority-2
in-canon pagination floor outcome (`reports/runtime/R2_CYCLE2_PREREG.md`,
frozen separately). A VOIDED discriminator decides nothing (accepted R2-1
rule): if the pagination cell voids, the escalation demanded here carries
BOTH voids and the branch-(b) question stays open pending authorized
substrate. If the pagination cell decides (either direction), its verdict
enters the Director's branch-(b) record as MEASURED backing scoped to that
cell class — never generalized beyond it.

## 4. Alternative demand — loop-only productionization charter

The audited agent-facing loop exists and is integration-proven end-to-end:
`resolve → execute-or-materialize → verify → report` over frozen
`capsule.v0`/`plan.v0`/`spider.cost_event.v0` schemas, plan.v0 ABSTAIN
handoff with clause-attributed fallback, total-overhead telemetry
(~ms-scale retrieval/applicability/write costs, denominator-only),
candidate-tier capsule registries derived byte-reproducibly from Graph
evidence. What does NOT exist: a second caller implementation (refuse-list
bar: transfer trigger unfired — zero tasks show margin ≥ M vs the
strongest baseline including URL-construction arms) and any demonstrated
compression-positive cell class (X31: killer (i) undischarged; killer (ii)
VOIDED, not discharged).

**Demand to CTO/portfolio (decision, not lane task):** either authorize
substrate expansion per §2 (which named classes/lists), or charter a
loop-only productionization track whose value proposition is the audited
fallback/verification/telemetry contract itself, decoupled from
work-compression claims until a surviving cell class exists. The second
option requires explicit portfolio sign-off of the second-caller bar; this
lane cannot grant it to itself.

---

## 5. Provenance

Accepted-evidence sources packaged above (no new claims):
`docs/RUNTIME_LEDGER.md` §§R0/R1/R2; audit records
`results/audit/CYCLE_32887030457_RUNTIME_GATE.json`,
`results/audit/CYCLE_32908002333_RUNTIME_GATE.json`,
`results/audit/CYCLE_32924286888_RUNTIME_GATE.json`,
`results/audit/CYCLE_32933579869_RUNTIME_GATE.json`; R2-1 frozen prereg
`reports/runtime/R2_CYCLE1_PREREG.md`; enumeration receipt reproducible
offline from the two dual-pinned committed snapshots listed in §1.1.

Filed by: TEAM RUNTIME (runtime_runner agent), cycle R2-2, run
32940627441. This document is a demand package; it authorizes nothing by
itself.
