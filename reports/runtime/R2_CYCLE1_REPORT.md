# R2 CYCLE 1 — REPORT (mechanism-floor null)

Cycle: R2-1, Program R2 "Inheritance Headroom & Mechanism Floor".
GitHub run: 32928419260. Branch: `cycle/runtime/32928419260/team`.
Prereg: `reports/runtime/R2_CYCLE1_PREREG.md` (FROZEN at `5dd51ab`, before
the first live request; disclosed pre-outcome correction `95aa45a` with
zero live requests existing). Harness frozen at `b4254a6`.

**Headline verdict (exact frozen-gate ceiling): `FLOOR_VOID` — the
mechanism-floor null is VOID on the quotes-login goal class because the
ENVIRONMENT accepts any credentials; no substrate inference is licensed in
either direction; repair-first.**

---

## 1. What ran

* Priority 1a (offline): URL-construction comparator arm
  `url_construct_account_route` recorded descriptively over both committed
  entry snapshots (`results/runtime/probes/url_arms_r21.json`). Gating:
  NONE. The accepted R1 sweep artifact and winner `goal_href|root0` are
  byte-untouched. Blinding scan clean against the frozen fixture.
* Priority 1b (live, zero browser launches): direct-HTTP measurement arm
  over the same login goal class — cells FLR-T3P1 (/tag/love/),
  FLR-T3P2 (/page/10/), FLR-CONFIRM-P2 (/tag/love/, second pass), plus
  wrong-password negative control FLR-NEGCTRL. Fresh cookie jar per cell;
  affordance-cascade discovery first; manual redirect walk; every wire
  transaction after the entry GET counted.
* Preflight (pre-POST): parser parity of the floor extractor vs committed
  browser snapshots PASSED on both entries (oracle anchors matched, 44/44
  and 57/57 element counts equal); blinding clean; shared fills identity
  asserted.

## 2. Observed facts (OBSERVATION tier — void-caveated)

| cell | steps | judge | guards | taxonomy |
|---|---|---|---|---|
| FLR-T3P1 | 3 | pass | all true | FLOOR_PASS |
| FLR-T3P2 | 3 | pass | all true | FLOOR_PASS |
| FLR-CONFIRM-P2 | 3 | pass | all true | FLOOR_PASS |
| FLR-NEGCTRL (wrongpass) | 3 | **pass** | all true | FLOOR_PASS |

Steps anatomy everywhere: affordance-probe GET /login (1) + credential
POST (2) + redirect-hop GET (3). Sensitivity at B ∈ {3,4,5,6}: all true,
DESCRIPTIVE ONLY. G-FLOOR0/P5' consistent; twin identity errors 0.

## 3. Why VOID (mechanism, not harness defect)

The negative control PASSED verification: posting a WRONG password also
produces an authenticated session on quotes.toscrape.com (302 → / with
Logout anchor). Out-of-harness verification recorded in the decision
record: anonymous home shows Login/no-Logout; wrong-pass POST yields
Logout. [wording correction, cycle-3 repair r1 (W-2, audit
CYCLE_32928419260): these facts are derivable solely from committed
stream rows — MUST_NOT_FIRE_OK rows FLR-T3P1-mnf / FLR-T3P2-mnf /
FLR-CONFIRM-P2-mnf prove no logout token pre-action on the entry pages,
and the FLR-NEGCTRL verify row proves the Logout anchor appears after the
wrongpass POST; no separate manual artifact exists. The decision-record
artifact substrate_decision_r21.json is left byte-untouched; its
phrasing is superseded by this tag and by the repair_round_1 block in
results/runtime/r2_cycle1_state.json.] So the goal class cannot
discriminate credential validity — the preregistered control assumption
is falsified BY THE ENVIRONMENT. Per frozen prereg §2.2 step 9 the
verdict is FLOOR_VOID and nothing flips.

The kill-discipline worked exactly as designed: the specialist-predicted
false-positive class was caught by the pre-frozen control, and the
seductive FLOOR_DOMINATES reading (3 steps ≤ 6, all success) was refused
by the frozen rule instead of being harvested post hoc.

## 4. Substrate decision

`NO_SUBSTRATE_DECISION_VOID` (`results/runtime/r2_floor/
substrate_decision_r21.json`). Per prereg §6: VOID ⇒ repair-first; NO
headroom claim in either direction; witnessed-effect addressing POC NOT
triggered (priority 2 requires surviving cells); stop-rule (b) NOT invoked
(the discriminator was voided — cell-class death did NOT occur).

Binding notes for R2-2 (recorded, not acted on):
1. The floor discriminator needs a goal class where wrong inputs
   verifiably FAIL. No such class is demonstrated within the current
   accepted substrate; relocation/repair requires Director ruling and,
   for expansion beyond lane self-authorization, Product/CTO demand input.
2. Any future strongest-comparator canon must include URL-construction /
   convention arms (artifact exists) or margins repeat the K3 lesson.
3. Retroactive scoping: ALL prior browser-side login-cell economics on
   this family measured FORM-COMPLETION, not credential-authenticated
   sessions (cells used the shared correct fills spec, so sessions were
   real — but the goal class is weaker than its wording assumed).

## 5. Priority 3 — WB-consumer cell decision

QUARANTINE (decided pre-outcome, prereg §3): write-back stays
NON-DEFAULT with NO consumer evidence owed; verbatim R1-1 §3.3 design
preserved by reference. Grounds: run environment lacks the browser stack
(OPERATIONAL_DIAGNOSTIC); under a dominating floor the §3.3 decisive
condition could not yield interpretable value. `reuse_yield` stays
UNDEFINED; no economics figure is quoted anywhere (W-R1-1, X31).

## 6. Refusals honored

No HTTP executor productized (measurement arm only); no substrate
expansion; no replication of killed observations; no new cost_event
fields/enums; schemas v0 untouched; audited modules byte-untouched; no
browser launches; no compression phrasing anywhere (X31 — killer (ii) not
discharged, it was VOIDED); wall-clock advisory; model independence
UNFALSIFIABLE.

## 7. Limitations / negative knowledge (scoped)

* One site family, one date, one scripted implementation; three passes.
* Static HTML parsing cannot reproduce computed-style visibility
  (mitigated by must-not-fire + negative-control + form-guard; residual
  open).
* Convention list contains the answer route for this family — bias
  direction AGAINST inheritance, disclosed; affordance-cascade fired
  first on every cell so no convention probe was ever spent.
* Negative knowledge: the accepted substrate's login goal class is
  credential-non-discriminating → unusable for mechanism-floor
  discrimination AND for any future claim of "authenticated" effect
  without a stronger witness.

## 8. Next high-information action

Director succession input per directive R2 stop rule: bottleneck
re-measured (substrate lacks any floor-decidable class) → choose between
(i) Product/CTO substrate-demand request naming JS-gated/non-affordance
goal classes with frozen task/site lists, or (ii) loop-only
productionization charter. Do NOT rerun the floor on this family without
a repaired discriminator.
