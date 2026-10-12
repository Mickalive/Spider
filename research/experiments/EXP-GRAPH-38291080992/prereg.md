# EXP-GRAPH-38291080992 - Frozen Preregistration

- experiment_id: `EXP-GRAPH-38291080992`
- lane: `graph`
- claim: `C-SEMANTIC-RESOLVE`
- design_contract_version: `2`
- request: `research/experiments/EXP-GRAPH-38291080992/request.json` (base_sha `0c2f8f3bd69383aa51599ba9b085e7979eaf429e`, chain_depth 0)
- director mandate: cycle_id `38290683955`, action `PIVOT`, cognitive_reset `true`, parent_handoff_disposition `USE`, claim_id `C-SEMANTIC-RESOLVE`
- parent handoff (continuity, disposition USE): `research/experiments/EXP-GRAPH-38205284279/handoff.json` sha256 `eed76bd6c21f4efd57599fd60e98bc0a5868f9a5dd55fc1ffc2e48078c715a47`
- CANONICAL-RUNNER-SHA256: `11fa24673a0d7ceb4c06252a6495dc6a11fcc5e47350c6ccbff7ced24edc7508`
- environment: `Python 3.12.15`, **stdlib only** (no numpy / sklearn / sentence_transformers available).

This prereg freezes the smallest decisive experiment requested by the mandate: a
single-validity-repair re-run on the SAME independently authored held-out surface
(`AXIS-G3-NEW`, block bytes verified identical to the parent prereg) with the SAME
zero-tunable-parameter clause set (no third surface, no refitting), a retest of the
frozen HELDOUT surface (`AXIS-G2-RETEST`), regression retention on the two surfaces
where the treatment already met the gate (`AXIS-G1-PRIMARY`, `AXIS-G1-ALTLEX`), and
the now-measurable retrieval comparator (Arm B). The ONLY authorized change relative
to the parent transaction is the treatment-liveness predicate scope repair
(`audit.json#required_fixes` of the parent): the applicable-only predicate validated
on calibration but evaluated on test is replaced by a global non-degeneracy predicate
pre-declared on the exact split where it is evaluated.


## 1. Question, hypothesis, falsifier

**Question (mandate).** On a re-frozen run keeping the SAME G3-NEW surface (the
blind-authored public-transit fleet goal bank + synonym lexicon from the parent
transaction, reused byte-identically - §5) and the SAME zero-tunable-parameter
T-FRAME clause set (frozen B-LEX-STRONG selector plus structural frame-completeness
abstention C1-SUBOP / C3-NO-REFERENCE / C4-COMPLEMENT / C5-SET-QUANT / C6-SOURCE /
C7-CREATE-OBLIQUE, with no refitting and no third independently authored surface),
but repairing the liveness predicate so it is pre-declared on the exact split where
it is evaluated, does the treatment validly reach a frozen ship-scope branch - and
in particular, does T-FRAME+ hold `pooled_false_accept <= 0.10` AND `coverage >=
0.50` AND `unknown_precision >= 0.85` on the disjoint calibration/test splits, is
the AXIS-G2-RETEST `unknown_precision` shortfall (`0.8333 < 0.85` as
auditor-recomputed in the parent packet) intrinsic to the no-refit deterministic
clause set, and does the deterministic-vs-retrieval fork (parent: `BOTH_PASS_G3`
with selective_acc `1.0 vs 0.2727`; Arm B G2 collapse at false_accept `0.70`)
favour structure on this surface family - thereby deciding whether
C-SEMANTIC-RESOLVE can be re-asserted to EXPERIMENTAL through a valid packet or
stays bounded to PRIMARY+ALTLEX with Product keeping the conservative shipped
abstention boundary?

**Hypothesis (H1).** The SAME treatment (`T-FRAME+`, Arm A, byte-identical clauses)
holds `pooled_false_accept <= 0.10 AND coverage >= 0.50 AND unknown_precision >= 0.85` on the
disjoint test split of the SAME surface `AXIS-G3-NEW` **and** on the retested frozen
`AXIS-G2-RETEST` surface, while retaining `selective_acc >= 0.80` on all four axes.

**Hypothesis (H2, comparator).** The stdlib retrieval comparator `B-RETRIEVAL-TFIDF`
(calibration-fitted gate, fit on calibration rows only) is measurable and does not strictly
dominate T-FRAME+ on `AXIS-G3-NEW`.

**Falsifier.** H1 is falsified for `AXIS-G3-NEW` if on the frozen test split the Arm A metrics
`pooled_false_accept > 0.10` OR `coverage < 0.50` OR `unknown_precision < 0.85`; or if
`C7-CREATE-OBLIQUE` reduces test coverage below 0.50; or if the measurement is invalid
(repaired liveness fails on the G3 TEST split, or `unknown_precision` undefined on any axis).
H1 is bounded (not falsified) if the gate holds on `AXIS-G2-RETEST` but not on `AXIS-G3-NEW`.
H2 is falsified if Arm B is not live / not measurable, or if Arm B meets the gate on
`AXIS-G3-NEW` where T-FRAME+ does not (then retrieval dominates).

**Liveness repair (frozen, the single mandate-authorized change).** The parent's applicable-only predicate `0 < executed_app < n_applicable_test` (evaluated on the G3 TEST split, validated on calibration) is REPLACED by a non-degeneracy predicate pre-declared on the exact split where it is evaluated (`AXIS-G3-NEW` TEST): `LIVE = (0 < executed_total_test < n_total_test) AND (executed_app_test >= 1) AND (abstained_resolved_test >= 1)`, where `abstained_resolved_test` counts resolved (`mech != None`) rows the treatment abstains on. This is the audit's second offered fix ("adjust liveness predicate scope to calibration-delineated range") in global non-degeneracy form: it fires on execute-all, abstain-all, and selector-degenerate runs, but no longer flags a treatment whose abstention load concentrates on the OOS half. Same surface, same zero-parameter clause set, no refitting, no third surface.

A negative (bounded) result is a first-class outcome: it scopes the architecture to the
PRIMARY+ALTLEX fixture and keeps the conservative shipped abstention boundary.


## 2. Inherited state from the USE parent handoff (four-way distinction preserved)

The mandate sets `parent_handoff_disposition = USE`. The parent handoff (`research/experiments/EXP-GRAPH-38205284279/handoff.json`) is continuity evidence with a binding PIVOT mandate behind it; its four-way distinction is carried forward unchanged, and the Director's strategic question (request.json#director_mandate.allocation.question) is the binding research direction. The handoff `next_question` is advisory only.

**established** (packet-level facts of the parent transaction):
- The frozen deterministic transaction completed validly as an execution (parent runner sha256 `d9edd0dc9e6a243847758c062744f4db6ffc9a93c986dcbf863f6a31bb7ffd4c`, two byte-identical `--mechanics-only` canaries, scored run twice byte-identical `c80a8f42...`, exit 0 empty stderr) but emitted `status=MEASUREMENT_INVALID`, `decision=null` via its own frozen liveness rule on `AXIS-G3-NEW` test (`36/36` applicable executed).
- The invalidity is a pre-declared frozen-rule event: NOT infrastructure failure, NOT scientific falsification.
- The defect is scoped to the liveness predicate: validated on G3 calibration (`38/39` applicable executed, 1 abstention) but evaluated on the G3 TEST split where structural abstention fired on 0 applicable rows (`36/36` executed; all 7 resolved abstentions on OOS).
- Auditor-recomputed observations inside the invalid measurement: G3 test T-FRAME+ `pooled_false_accept=0.10 / coverage=1.0 / unknown_precision=1.0 / selective_acc=1.0`; C7 fires on 0 applicable rows on every axis and strictly reduces G3 test FA `0.20 -> 0.10` and G2 test FA `0.10 -> 0.00`.
- `AXIS-G2-RETEST` test gate NOT met solely on `unknown_precision=0.8333 < 0.85` (`pooled_false_accept=0.0`, `coverage=0.925`, `selective_acc=1.0`); G1-PRIMARY and G1-ALTLEX gates ARE met.
- Arm B (`B-RETRIEVAL-TFIDF`) is MEASURABLE: G3 gate-met (`FA=0.05`, `selective_acc=0.2727`, fitted `tau=0.4278, mu=0.0`) with fork `BOTH_PASS_G3`; G2 collapse (`FA=0.70`).
- All controls moved as pre-declared (`PC-AXIS-G1-ALTLEX` gate-met; `NC-EXEC-ALL` FA `0.2778-0.50` vs Arm A `0.0-0.10`; shuffled/random near chance; `CTRL-RANDOM-GATE` FA `0.70-0.9444`; `CTRL-INCUMBENT` FA `0.1667-0.20`).
- Derived branch re-evaluation: with `gate_met(AXIS-G2-RETEST)=false`, `DECIDE_SHIP_TFRAME_BROAD` and `DECIDE_SHIP_TFRAME_SCOPED` are unreachable and the remaining frozen branch is `DECIDE_REQUIRE_RETRIEVAL_B` (derived statement; the runner emitted `decision=null`).

**rejected** (bounded to the frozen surface set / predicate scope):
- The frozen test-split applicable-only liveness predicate `0 < executed_app < n_applicable_test` as a liveness instrument for surfaces whose abstention load concentrates on the OOS half (flags a globally discriminating treatment `FA 0.10 vs 0.45 execute-all` as degenerate).
- The ship branches `DECIDE_SHIP_TFRAME_BROAD / DECIDE_SHIP_TFRAME_SCOPED` as reachable on the observed gate vector (derived routing statement, not the emitted decision).
- NOT rejected: `C-SEMANTIC-RESOLVE` itself, the deterministic T-FRAME architecture, structural abstention, retrieval in general, or the `B-LEX-STRONG` selector; `BOTH_PASS_G3` rejects neither arm.

**unknown** (unchanged): whether the invalidity is genuine degeneracy or an over-strict trigger (treatment abstained on 18/20 OOS G3 test rows); whether the G2-RETEST UP shortfall is reducible under the no-refitting constraint; whether a third independently authored surface is justified (mandate stop rule binds; Director decides); whether a retrieval comparator with an ACTIVE margin gate would change the fork; whether `C-SEMANTIC-RESOLVE`'s prior EXPERIMENTAL elevation can be re-asserted by a VALID packet; Arm B's extreme G2 calibration/test transfer; the NOT_RUN `B-EMBED-COSINE` behaviour.

**do_not_assume** (unchanged): do not treat the parent `MEASUREMENT_INVALID` as falsification, infra failure, or downgrade; do not elevate on the parent packet (effective status stays `HYPOTHESIS`, itself a Product-lane coordination artifact per the mandate rationale); do not quote G3 `0.10/1.0/1.0/1.0` as a valid gate passage; do not treat derived `DECIDE_REQUIRE_RETRIEVAL_B` as the emitted decision; do not treat `BOTH_PASS_G3` as retrieval parity (selective_acc `0.2727 vs 1.0`, G2 collapse, shared-split coupling, inactive `mu=0.0` margin); do not author a third surface; do not promote to product; do not re-run the exact frozen design; do not treat `B-EMBED-COSINE` absence as a result; do not treat C7 observations as claim-level closure of the CREATE-with-S=0 gap.

**Effect of USE.** This experiment executes the Director's binding PIVOT repair: SAME G3-NEW surface, SAME zero-tunable-parameter clause set (no third surface, no refitting), with the single authorized change being the liveness-predicate scope repair pre-declared on the exact split where it is evaluated, per `audit.json#required_fixes`. Regime state (`codex/claim_state.json#effective_event_by_claim.C-SEMANTIC-RESOLVE = HYPOTHESIS`) may be re-asserted ONLY through this packet's own valid measurement - never by editing registry/state files.


## 3. Treatment: Arm A = `T-FRAME+` (deterministic resolver + structural abstention)

Selection is the FROZEN `B-LEX-STRONG` selector (`comp()`): tokenize to `[a-z]+`; longest
matched family-noun phrase (plural-tolerant) and longest matched op-synonym phrase over the
bank-specific lexicon; homograph guard suppresses a family-headword used as the CREATE object;
bidirectional agreement `r1 == r2` produces `mech_<family>_<op>`; otherwise `mech=None`. It has
**zero tunable parameters** (all thresholds are fixed constants frozen at request time).

Abstention = any frozen structural clause firing => `ABSTAIN` (`mech=None`):
- `C1-SUBOP`: a subordinator precedes the op span while the head token differs;
- `C3-NO-REFERENCE`: READ/UPDATE/DELETE with no reference cue (`id/number/named/...`);
- `C4-COMPLEMENT`: a non-preposition, non-reference, non-relative token directly follows the
  family span (attributive compound / complement);
- `C5-SET-QUANT`: a set/quantifier token is present (all/every/each/both/... );
- `C6-SOURCE`: a CREATE whose post-family span contains a source preposition (from/into/onto).

**Inherited clause `C7-CREATE-OBLIQUE` (parent's pre-declared clause, reused byte-identically here).** Zero tunable
parameters; declared from the frozen HELDOUT false-accept pattern before any parent outcome was
observed, and frozen unchanged for this repair run per the mandate's no-refitting constraint. It fires for a bound CREATE operation when EITHER:
- (a) a source/extraction preposition `{from, into, onto}` occurs anywhere in the instruction
  (the object is placed from/onto/into a host resource); OR
- (b) a placement preposition `{to,on,onto,into,in,at,from,by,upon,toward,towards,with}` occurs
  strictly between the end of the matched CREATE verb phrase and the start of the first
  bound-family noun phrase (the resource sits in an oblique argument, so the created entity is
  a non-resource object attached to it).

Rationale: the two named HELDOUT false accepts are exactly this pattern -
`oos_010` "Upload a new attachment onto a document." (source-prep `onto`, caught by (a)) and
`oos_014` "Add a tag to the issue about login failures." (non-resource object `tag` then
placement-prep `to` before family noun `issue`, caught by (b)). The clause is structural and
threshold-free; it is NOT fitted to any metric.

`T-FRAME+` (used in every decision) = `B-LEX-STRONG` + ALL clauses including C7.
`tframe_frozen` (diagnostic only, not a decision arm) = same clauses WITHOUT C7.
`incumbent` = B-LEX-STRONG + the pre-existing `S<=0` lexical gate (no structural clauses).
`gatefree` = execute all resolved (the execute-all ceiling baseline).


## 4. Comparator: Arm B = `B-RETRIEVAL-TFIDF` (retrieval/embedding fork, previously BLOCKED)

The previously BLOCKED Arm B (`B-EMBED-COSINE`) depended on `numpy`/`sklearn`/
`sentence_transformers`, which are absent (`EXP-GRAPH-38188798583` V5 prereq note). The mandate
requires the fork be decided, not re-BLOCKED. Arm B is therefore unblocked with a **pure
stdlib** comparator that requires no third-party module and no network:
- features = word unigrams + adjacent bigrams; IDF from the **calibration** fit rows only;
- per-class L2-normalised centroids over the fit rows;
- prediction = nearest centroid; confidence = top cosine; margin = top minus second;
- abstention gate = thresholds `(tau, mu)` chosen on **calibration rows only** by the frozen
  lexicographic rule: maximise feasibility (gate met on calibration) then coverage; then
  freeze and apply unchanged to the test split.

Arm B is a genuine, distinct comparator (instance/centroid retrieval vs deterministic lexical
structure) fit on calibration only; it is never used as the cost denominator of Arm A and its
gate is never tuned on test. This is the smallest change that unblocks the fork while keeping
the harness stdlib-only and hash-bindable at freeze.


## 5. Surface provenance (`AXIS-G3-NEW`, inherited byte-identically)

`LEXICON-G3`, `GOAL-BANK-G3` and `OOS-BANK-G3` were authored for the PARENT transaction by **fresh-context blind
subagents** that received no repository access, no view of `LEXICON-G1`, `LEXICON-G1-ALT`,
`LEXICON-G2-HELDOUT`, `GOAL-BANK-G1/G2`, `OOS-BANK-G1/G2`, and no description of the T-FRAME
clause set. They were told only: (i) invent a new operational Web-agent domain distinct from
task-management/service-desk domains; (ii) produce a synonym lexicon mapping family nouns and
CRUD verbs with explicit surface forms; (iii) produce an applicable goal bank of unambiguous
single-operation CRUD instructions covering every (family, op) cell; (iv) produce a 40-item
out-of-scope bank with 10 each of categories A (unsupported/invented operation), B (relational
/ sub-resource request), C (multi-step / conditional), D (other/nearby domain). The selected
domain is **public transit fleet management** (families: `routes`, `vehicles`, `drivers`,
`stops`, `fares`), clearly disjoint from the G1/G2 car-rental/helpdesk/animals surfaces and
from `goal_generator.py`'s token vocabulary. This satisfied the parent mandate's "independently
authored, no-reference" requirement. Bank statistics: 80 applicable rows = 16 (family, op)
cells x 4 surfaces; 40 OOS rows = 4 categories x 10.

**Reuse (this experiment, per the Director's stop rule).** No new surface was authored here:
the three G3 blocks embedded in §13.1-13.3 below were verified byte-identical to the
corresponding blocks of `research/experiments/EXP-GRAPH-38205284279/prereg.md` (block-text
comparison in DESIGN: `LEXICON-G3`, `GOAL-BANK-G3`, `OOS-BANK-G3` all identical, lengths
3834/6357/3672). Authoring a third independently authored surface would violate the mandate's
stop rule; this design complies by pure reuse.

**Contamination screen (frozen).** Any row whose token-set Jaccard `>= 0.60` OR char-trigram
Jaccard `>= 0.75` against the union of {`goal_generator.py` INTENTS/PARAPHRASES/
NO_APPLICABLE_TEMPLATES/OOD_PARAPHRASES, the grandparent PRIOR-PARENT-BANK-TEXTS, all
G1/G2 applicable and OOS texts} is **dropped from binding** (recorded, not counted). On the
frozen G3 bank this drops 5 applicable rows (`app_009`, `app_026`, `app_030`, `app_036`,
`app_076`) and 0 OOS rows -> G3 binding n = 115 (75 applicable, 40 OOS).


## 6. Axes, splitting, and exchangeability

Split rule (frozen, deterministic): row `i` is `test` iff `(i % splitmod) in (1,3,5)`, else
`cal`; `splitmod = 4` for the G3 and G2-HELDOUT surfaces, `splitmod = 6` for G1/ALT.
Calibration and test rows are disjoint and exchangeable by construction (same bank, fixed
modular interleave). No test row is ever read by Arm A, by any clause, by the contamination
screen, or by the Arm B gate fit; the Arm B gate is fit on calibration rows only.

| axis | surfaces | splitmod | decision role |
|---|---|---|---|
| `AXIS-G3-NEW` | `LEXICON-G3`, `GOAL-BANK-G3`, `OOS-BANK-G3` | 4 | **primary generalization** |
| `AXIS-G2-RETEST` | frozen G2 bank + `LEXICON-G2-HELDOUT` | 4 | retest of the C7 gap surface |
| `AXIS-G1-PRIMARY` | frozen G1 bank + `LEXICON-G1` | 6 | regression retention |
| `AXIS-G1-ALTLEX` | frozen G1 bank + `LEXICON-G1-ALT` | 6 | positive-control retention |

Counts: G3 bound = 115 (cal 39 app + 20 OOS; test 36 app + 20 OOS after the screen).
G2 bound = 120 (cal 40 app + 20 OOS; test ~40 app + 20 OOS). G1/ALT bound = 151 each.


## 7. Metrics, gates, and controls (stable identifiers reused by EXECUTE and AUDIT)

Gates (frozen constants): `FA_TARGET = 0.10`, `COV_TARGET = 0.50`, `PREC_TARGET = 0.85`,
`SEL_TARGET = 0.80`, `TOK_BAND = 0.60`, `TRI_BAND = 0.75`.

For each (axis, mode) the runner emits `coverage`, `pooled_false_accept`,
`unknown_precision`, `unknown_precision_inclusive`, `selective_acc`, `executed`,
`executed_oos`, `executed_app`, `abstained_resolved`, `unresolved_applicable`.
`unknown_precision` is defined over resolved-then-abstained rows only; it is `null` (an
invalid-measurement trigger) if there are none.

Gate met (an axis, for a mode) = `pooled_false_accept <= 0.10 AND coverage >= 0.50 AND
unknown_precision >= 0.85`. `selection_preserved` = `selective_acc >= 0.80` on all four axes.

Controls (stable ids):
- `PC-AXIS-G1-ALTLEX`: AXIS-G1-ALTLEX must remain gate-met (known-positive from
  `EXP-GRAPH-38188798583`); if it fails, the measurement is invalid, not a science negative.
- `NC-EXEC-ALL` (`gatefree`): execute-all pools the OOS false accepts; must show materially
  higher `pooled_false_accept` than Arm A (parent-published calibration: 0.30 on G3, 0.55 on G2,
  0.275 on G1, 0.275 on ALT).
- `NC-ABSTAIN-ALL`: all-abstain control, coverage 0, `unknown_precision` 1.0.
- `CTRL-SHUFFLED-SELECTION` and `CTRL-RANDOM-ROLE`: label-permutation selection near chance.
- `CTRL-RANDOM-GATE` (`matched_random_gate`): abstention volume matched by random rows.
- `CTRL-B-LEX-ONLY`: gatefree selective_acc (selection without abstention).
- `CTRL-INCUMBENT`: B-LEX-STRONG + lexical `S<=0` gate (the previously shipped logic).


## 8. Design satisfiability probes (synthetic + published-evidence only; no test outcome observed)

These probes are non-outcome-bearing. No test-split metric of THIS experiment was computed in DESIGN: the frozen runner was never executed on the real banks; real-bank numbers cited below are parent-published frozen evidence (`result.json`, `audit.json`), quoted for reachability arithmetic, not re-measured.

**8.1 Treatment liveness, repaired scope (PASS).** The frozen predicate is evaluated on the `AXIS-G3-NEW` TEST split only (the exact split named in the predicate - the parent scope defect is closed by construction). Pre-freeze probes, all non-outcome-bearing: (a) the extracted `FROZEN-RUNNER` module compiles and its frozen analysis path (`comp`/`frame`/`clause_c7`/`is_executed`/`metrics`) executes on synthetic rows with a toy lexicon, yielding a non-degenerate treatment (`executed=1`, `abstained_resolved=2` over 3 synthetic rows) for which the frozen liveness formula evaluates True; (b) predicate arithmetic on the parent-published G3-TEST counts (prior packet evidence, not a new measurement: `executed_total=38`, `n_total_test=56`, `executed_app=36`, `abstained_resolved=7`) evaluates the repaired `LIVE` to True, while the parent predicate `0 < 36 < 36` evaluates False - the repair flips exactly the defective trigger and nothing else; (c) degeneracy sensitivity: execute-all (`abstained_resolved=0`) and abstain-all (`executed_total=0`) analogues both evaluate `LIVE=False`, so the repaired predicate still rules out genuine degeneracy (a selector-degenerate run with all `mech=None` likewise yields `executed_total=0`); (d) calibration non-degeneracy is retained parent evidence (`T-FRAME+` executes 38/39 calibration applicable rows, coverage 0.9744, 1 abstention). No test-split metric of THIS experiment was computed in DESIGN.

**8.2 C7 non-vacuity and zero applicable cost (PASS, parent-published structural facts quoted, not re-measured).** Per the parent `result.json#metrics.c7_firing` and `audit.json#recomputed_metrics`, `C7-CREATE-OBLIQUE` fires on **0** applicable rows on every axis and on
2 G3 / 4 G2 / 2 G1 / 1 ALT OOS rows; on the frozen `AXIS-G2-RETEST` surface it fires on
exactly the named false accepts `oos_010` and `oos_014` (plus `oos_006`, `oos_023`). No
fitted parameter exists; C7 fires iff the structural triggers hold.

**8.3 Decision-rule reachability (PASS).** The exact frozen `if/elif/else` cascade (repaired-liveness invalid path with the new reason string and `decision=null`; `g3_gate & g2_gate & selection_preserved -> DECIDE_SHIP_TFRAME_BROAD`; `g2_gate & selection_preserved -> DECIDE_SHIP_TFRAME_SCOPED`; else `DECIDE_REQUIRE_RETRIEVAL_B`) was enumerated over synthetic inputs covering all four decision outcomes, and the retrieval-fork ordering was enumerated over all four gate combinations (`RETRIEVAL_DOMINATES_G3` / `TFRAME_DOMINATES_G3` / `BOTH_PASS_G3` / `NEITHER_PASSES_G3`); the repaired `LIVE` formula returned True on the synthetic non-degenerate rows (8.1a) and False on degenerate analogues. Branch map: `g3_gate & g2_gate &
selection_preserved -> DECIDE_SHIP_TFRAME_BROAD`; `g2_gate & selection_preserved ->
DECIDE_SHIP_TFRAME_SCOPED`; else `DECIDE_REQUIRE_RETRIEVAL_B`; any invalid reason ->
`MEASUREMENT_INVALID` with `decision = null`. Retrieval fork: `RETRIEVAL_DOMINATES_G3` /
`TFRAME_DOMINATES_G3` / `BOTH_PASS_G3` / `NEITHER_PASSES_G3`. All branches are reachable.

**8.4 Arithmetic attainability (PASS).** On the G3 test split the gate requires
`<= 2` false accepts among 20 OOS (`FA <= 0.10`), `>= 18/36` executed applicable
(`coverage >= 0.50`), and `unknown_precision >= 0.85`, all within the bounded (36,20) split;
the bars are attainable and not at a ceiling/floor.

**8.5 Baseline / comparator identity (PASS).** Arm A (deterministic structure) and Arm B
(calibration-fitted instance retrieval) are distinct implementations; the incumbent lexical
`S<=0` gate is a third, distinct arm. Arm B measurability is parent-published evidence (`result.json#metrics.arm_b`: fitted `tau = 0.4278`, `mu = 0.0`, `cal_fit_feasible = true`; test measurable with G3 gate-met), quoted not re-measured; the frozen gate procedure (lexicographic maximise-feasibility-then-coverage on calibration rows only) is unchanged, so re-applying it at EXECUTE is the frozen procedure, not a refit of the clause set (refitting the deterministic clauses is forbidden).
The `DECIDE_REQUIRE_RETRIEVAL_B` branch is therefore not an empty branch.

**8.6 Control sensitivity (PASS, parent-published values quoted).** On the parent test splits NC-EXEC-ALL pools 0.2778-0.50 false accepts
vs 0.0-0.10 for Arm A; the abstain-all control has coverage 0; shuffled/random controls are
near-chance; the C7 clause is the only clause whose removal changes the two named HELDOUT
rows. Controls can move.

**8.7 Measurement prerequisites (PASS).** Verified in DESIGN without outcome measurement: Python `3.12.15`; top-level runner imports are stdlib-only (`argparse`, `hashlib`, `json`, `math`, `os`, `re`, `random`, `sys`, `pathlib`, `__future__`) with the single declared repo-local `goal_generator` import inside `main()`; `numpy`/`sklearn`/`sentence_transformers` confirmed absent; `research/harness/goal_generator.py` imports cleanly (`INTENTS`/`PARAPHRASES` present); every block name the runner extracts (`GOAL-BANK-G1`, `OOS-BANK-G1`, `LEXICON-G1`, `LEXICON-G1-ALT`, `GOAL-BANK-G2`, `OOS-BANK-G2`, `LEXICON-G2-HELDOUT` in the parent prereg; `PRIOR-PARENT-BANK-TEXTS` in the grandparent prereg) verified present. No
network, model, credential, browser or third-party package is required.

**8.8 Freeze artifacts bounded (PASS).** The only external mutable files that can change the
interpretation (parent/grandparent preregs and the contamination-prior generator) are listed
in `spec.json#freeze_artifacts`; the treatment runner and all banks/lexicons are embedded in
this prereg and hashed.

**8.9 Self-attack (declared threats, not failures).**
- C7 trigger (a) uses `from/into/onto` anywhere; an unseen applicable that uses one as a
  benign idiom would over-abstain. Parent DESIGN verified 0 such rows in the frozen binding bank (clauses unchanged since); the
  threat is declared and would surface as reduced coverage, not a false accept.
- C7 trigger (b) could in principle fire on a differently-parsed applicable; parent DESIGN verified 0 on
  the frozen bank.
- The G3 applicable bank is structurally simple by construction; this makes the surface a
  fairness test of abstention and of the C7 clause, not of hard parsing. The OOS bank is the
  discriminating half and is non-trivial (NC-EXEC-ALL FA 0.30).
- The contamination screen drops 5 G3 applicable rows; it cannot inflate coverage
  unfavourably (dropping applicable rows can only lower the executed denominator).

## 8.10 Self-attack on the repaired design (empty-branch / identity / ceiling audit)

- Empty/unreachable branches: with the SAME frozen surface and clause set, the G2-RETEST test metrics will reproduce deterministically, so `gate_met(AXIS-G2-RETEST)=false` is EXPECTED and `DECIDE_SHIP_TFRAME_BROAD / DECIDE_SHIP_TFRAME_SCOPED` are expected-unreachable. This is NOT a satisfiability failure: all branches are arithmetically reachable and synthetically enumerated (8.3); the decision-changing fork is VALID-`DECIDE_REQUIRE_RETRIEVAL_B` (bounds the resolver to PRIMARY+ALTLEX with a valid fork observation) vs `MEASUREMENT_INVALID` (retires this surface family per the mandate rationale). A valid negative is the predicted informative outcome, and it changes the claim/product decision (retains HYPOTHESIS with a valid bound, keeps the conservative shipped abstention boundary).
- Treatment/comparator identity: Arm A (deterministic lexical structure + 6 frozen clauses) and Arm B (calibration-fitted TF-IDF centroid retrieval) are distinct implementations sharing no fitted state; the incumbent and gatefree arms are separately reported. Identity holds.
- Ceiling baselines: the G3 gate (`<= 2` OOS executes of 20; `>= 18/36` applicable executes; `UP >= 0.85`) is attainable and non-degenerate (8.4); `gatefree` FA `0.45` proves headroom.
- Insensitive controls: every control moved on the parent run (NC-EXEC-ALL gap `0.35` on G3; random-gate FA `0.70-0.9444`); the repaired liveness preserves sensitivity to execute-all and abstain-all degeneracy (8.1c). The positive control `PC-AXIS-G1-ALTLEX` remains an invalidity trigger, not a science claim.
- Missing prerequisites: none - stdlib-only, no network/model/browser/credential, all block dependencies probed present (8.7).
- Mutable dependencies: every file whose identity can change the interpretation is bound in `spec.json#freeze_artifacts` (12); the runner, banks and lexicons are embedded here.


## 9. Decision rule and product consequences

**Decision (frozen).**
- `MEASUREMENT_INVALID` (`decision = null`) if the repaired G3-TEST liveness fails
  (`NOT(0 < executed_total_test < n_total_test AND executed_app_test >= 1 AND
  abstained_resolved_test >= 1)` on `AXIS-G3-NEW` test), or `unknown_precision` is undefined
  on any axis, or `PC-AXIS-G1-ALTLEX` fails.
- `DECIDE_SHIP_TFRAME_BROAD` if `AXIS-G3-NEW` and `AXIS-G2-RETEST` both meet the gate and
  selection is preserved on all axes.
- `DECIDE_SHIP_TFRAME_SCOPED` if only `AXIS-G2-RETEST` meets the gate and selection is
  preserved (architecture bounded to PRIMARY+ALTLEX).
- `DECIDE_REQUIRE_RETRIEVAL_B` otherwise (deterministic architecture not licensed to ship).

**Retrieval fork (frozen, derived).** On `AXIS-G3-NEW`, compare Arm A gate vs Arm B gate:
`RETRIEVAL_DOMINATES_G3` / `TFRAME_DOMINATES_G3` / `BOTH_PASS_G3` / `NEITHER_PASSES_G3`.

**Positive consequence.** If BROAD: the deterministic resolver + abstention gate is licensed to
ship broadly; the audit's named product gap ("unseen-goal calibrated resolution with abstention
in the product path") is closed; `C-SEMANTIC-RESOLVE` evidence supports a scoped Product
promotion of the `resolve()` + abstention path. If SCOPED: Product keeps a bounded but audited
resolver on the shipped surfaces and a regression-free abstention boundary.

**Negative consequence.** If REQUIRE_RETRIEVAL_B: the deterministic T-FRAME architecture is NOT
shipped; Product must keep the conservative shipped abstention boundary, and the
deterministic-vs-retrieval fork is recorded as retrieval-favouring on this surface - a real
architecture decision. A measured Arm B that ties or loses still informs the fork.

This packet does not promote anything itself; promotion requires an audited verdict and a
separate Product-lane frozen experiment against the shipping tree.


## 10. Cost and expected information gain

**Estimated cost.** No model calls, no network, no browser, no third-party packages. One
deterministic in-process run over ~500 bound rows plus calibration fitting for Arm B; total
wall time seconds; the only substantive design cost was the blind authoring of the G3 surface
and the pre-declared clause. This is near-zero marginal cost for a decision-bearing result.

**Expected information gain.** High governance value from a single validity repair. This run does not discover new metric values (the deterministic re-run is predicted to reproduce the parent gate vector); its information lies in converting a `MEASUREMENT_INVALID` status-confusion packet into a VALID decision: predicted VALID `DECIDE_REQUIRE_RETRIEVAL_B` bounds the `C-SEMANTIC-RESOLVE` resolver to PRIMARY+ALTLEX through a valid packet (retaining HYPOTHESIS with a structural-favouring fork observation) and keeps Product's conservative shipped abstention boundary; VALID ship-scope branches would re-open the EXPERIMENTAL question for the Director; G3 gate failure falsifies H1 on this surface family; a second `MEASUREMENT_INVALID` retires the surface family per the mandate rationale. Every branch changes the claim or product state, and both valid-positive and valid-negative outcomes change a current product decision.


## 11. Environment and EXECUTE command

- Python `3.12.15`, stdlib only. `research/harness/goal_generator.py` is importable and is used
  only for the contamination priors.
- EXECUTE writes the following files into the experiment directory (raw evidence preserved):
  - `raw_evidence/runner_tframe_g3.py` - the runner extracted from the `FROZEN-RUNNER` block
    (block content restored with exactly one trailing newline; sha256 must equal
    `CANONICAL-RUNNER-SHA256 = 11fa24673a0d7ceb4c06252a6495dc6a11fcc5e47350c6ccbff7ced24edc7508`);
  - `raw_evidence/run_output.json` - verbatim stdout of the scored run;
  - `result.json`, `report.md`, `provenance.json`.
- Run (from the repository root):
  `python3 research/experiments/EXP-GRAPH-38291080992/raw_evidence/runner_tframe_g3.py > research/experiments/EXP-GRAPH-38291080992/raw_evidence/run_output.json`
- Determinism: fixed seed `SEED = 38291080992 % 2**32`; no wall-clock/RNG-dependent state.
  EXECUTE must confirm two `--mechanics-only` runs are byte-identical before the scored run
  (V2 canary).


## 12. Freeze artifacts (v2)

`spec.json#freeze_artifacts` lists the exact repository-relative mutable files whose identity
can change the interpretation. All other inputs (the runner, banks and lexicons) are embedded
in this prereg and hashed by the freezer; the runner additionally self-hashes
(`runner_self_sha`). Each listed path MUST be hashed into `freeze.json.artifact_hashes` and is
immutable for the EXECUTE transaction.


### 13.1 LEXICON-G3

<!-- BEGIN LEXICON-G3 -->
{"family_nouns":{"routes":["route","line","path","corridor","itinerary","circuit","loop","artery","passage","track","course","channel","way","trajectory","leg","alignment","thoroughfare","throughway","expressway","boulevard"],"vehicles":["bus","tram","coach","streetcar","trolley","van","minibus","shuttle","train","subway","metro","railcar","trolleybus","ferry","vehicle","cruiser","sedan","wagon","carriage"],"drivers":["driver","operator","chauffeur","motorist","conductor","pilot","captain","navigator","motorman","coachman","cabbie","helmsman","teamster","rider","marshal","attendant","wheelman","trucker","busman"],"stops":["stop","station","depot","terminal","halt","platform","wharf","pier","dock","berth","bay","shelter","stand","interchange","junction","node","landing","anchorage","stopover","waypoint"],"fares":["fare","price","tariff","toll","charge","fee","cost","rate","payment","levy","surcharge","expense","outlay","expenditure","remittance","dues","stipend","tollage","rent","hire"]},"op_synonyms":{"CREATE":["add","create","make","build","set up","register","generate","start","open","launch","introduce","bring","enter","draft","compose","initiate","establish","form","produce","construct","enroll","raise","schedule","book","devise","invent","originate","fabricate","assemble","craft","mint","forge","concoct","spawn","hatch","pioneer","found","institute","inaugurate","constitute","organize","arrange","plan","design","author","write","pen","coin","cast","model","fashion","manufacture","erect","convene","summon","mount","stage","propose","pitch","submit"],"READ":["get","fetch","show","list","find","view","retrieve","look up","display","read","inspect","search","query","check","print","pull","browse","review","examine","gather","access","obtain","download","locate","scan","skim","survey","peruse","study","audit","monitor","observe","spot","discover","uncover","expose","reveal","detect","identify","pinpoint","explore","probe","investigate","seek","hunt","screen","sift","filter","extract","collect","compile","enumerate","tabulate","glance","peek","glimpse","watch","count","tally","note","ascertain","determine","verify","confirm"],"UPDATE":["update","change","edit","modify","adjust","revise","amend","set","correct","rename","extend","move","assign","replace","tweak","patch","alter","fix","reschedule","reassign","switch","transfer","enable","disable","refresh","sync","apply","save","mark","merge","convert","transform","upgrade","downgrade","overhaul","revamp","refactor","rework","remodel","reshape","recast","reposition","relocate","realign","recalibrate","tune","polish","refine","enhance","augment","boost","expand","shrink","reduce","shorten","lengthen","renumber","relabel","rebrand","toggle","activate","suspend","resume","reorder","rotate","swap","substitute","exchange","redefine","reset","revert","rollback","commit","persist","store","flag","tag","annotate","label","classify","categorize","sort","tidy","streamline","optimize","normalize","standardize"],"DELETE":["remove","delete","erase","discard","cancel","drop","archive","withdraw","retire","scrap","clear","destroy","purge","revoke","deactivate","close","unlink","detach","void","wipe","terminate","dismiss","expunge","eliminate","abolish","annihilate","demolish","dismantle","disassemble","dispose","dump","trash","bin","jettison","evict","oust","eject","expel","banish","scrub","abort","kill","end","finish","conclude","retract","rescind","repeal","nullify","invalidate","suppress","strip","shed","unset","disconnect","sever","cut","trim","prune","cull","weed","sweep","flush","zap","obliterate","exterminate","unbind","unhook","unmount","reject","veto","block","ban","bar","forbid","shut","shut down","power down","switch off","turn off","take out","throw away","get rid of","do away with","phase out","write off","call off"]}}
<!-- END LEXICON-G3 -->

### 13.2 GOAL-BANK-G3

<!-- BEGIN GOAL-BANK-G3 -->
{"family": "routes", "op": "CREATE", "text": "Create a new route for the north zone."}
{"family": "routes", "op": "CREATE", "text": "Add a new route between two towns."}
{"family": "routes", "op": "CREATE", "text": "Establish a new route through the valley."}
{"family": "routes", "op": "CREATE", "text": "Introduce a new route for early mornings."}
{"family": "routes", "op": "READ", "text": "Show the route with id 12."}
{"family": "routes", "op": "READ", "text": "Find the route named Oak Street."}
{"family": "routes", "op": "READ", "text": "Fetch the route whose code is R5."}
{"family": "routes", "op": "READ", "text": "Display the route numbered 7."}
{"family": "routes", "op": "UPDATE", "text": "Update the route with id 12."}
{"family": "routes", "op": "UPDATE", "text": "Change the route numbered 7."}
{"family": "routes", "op": "UPDATE", "text": "Rename the route whose code is R5."}
{"family": "routes", "op": "UPDATE", "text": "Reschedule the route named Oak Street."}
{"family": "routes", "op": "DELETE", "text": "Delete the route with id 12."}
{"family": "routes", "op": "DELETE", "text": "Remove the route numbered 7."}
{"family": "routes", "op": "DELETE", "text": "Cancel the route whose code is R5."}
{"family": "routes", "op": "DELETE", "text": "Archive the route named Oak Street."}
{"family": "vehicles", "op": "CREATE", "text": "Add a new bus to the fleet."}
{"family": "vehicles", "op": "CREATE", "text": "Register a new vehicle with id 300."}
{"family": "vehicles", "op": "CREATE", "text": "Create a new tram for the city."}
{"family": "vehicles", "op": "CREATE", "text": "Introduce a new coach for long runs."}
{"family": "vehicles", "op": "READ", "text": "Show the bus numbered 202."}
{"family": "vehicles", "op": "READ", "text": "Find the vehicle with id 300."}
{"family": "vehicles", "op": "READ", "text": "Fetch the tram labelled T4."}
{"family": "vehicles", "op": "READ", "text": "Display the coach whose code is C9."}
{"family": "vehicles", "op": "UPDATE", "text": "Update the bus numbered 202."}
{"family": "vehicles", "op": "UPDATE", "text": "Modify the vehicle with id 300."}
{"family": "vehicles", "op": "UPDATE", "text": "Move the tram labelled T4 to bay 3."}
{"family": "vehicles", "op": "UPDATE", "text": "Replace the coach whose code is C9."}
{"family": "vehicles", "op": "DELETE", "text": "Delete the bus numbered 202."}
{"family": "vehicles", "op": "DELETE", "text": "Remove the vehicle with id 300."}
{"family": "vehicles", "op": "DELETE", "text": "Retire the tram labelled T4."}
{"family": "vehicles", "op": "DELETE", "text": "Scrap the coach whose code is C9."}
{"family": "drivers", "op": "CREATE", "text": "Register a new driver."}
{"family": "drivers", "op": "CREATE", "text": "Enroll a new driver with badge D-88."}
{"family": "drivers", "op": "CREATE", "text": "Add a driver named Alex."}
{"family": "drivers", "op": "CREATE", "text": "Introduce a new driver."}
{"family": "drivers", "op": "READ", "text": "Show the driver with badge D-88."}
{"family": "drivers", "op": "READ", "text": "Find the driver named Alex."}
{"family": "drivers", "op": "READ", "text": "Inspect the driver with id 42."}
{"family": "drivers", "op": "READ", "text": "Fetch the driver whose code is N42."}
{"family": "drivers", "op": "UPDATE", "text": "Update the driver with badge D-88."}
{"family": "drivers", "op": "UPDATE", "text": "Reassign the driver named Alex."}
{"family": "drivers", "op": "UPDATE", "text": "Modify the driver whose code is N42."}
{"family": "drivers", "op": "UPDATE", "text": "Transfer the driver with id 42."}
{"family": "drivers", "op": "DELETE", "text": "Delete the driver with badge D-88."}
{"family": "drivers", "op": "DELETE", "text": "Remove the driver named Alex."}
{"family": "drivers", "op": "DELETE", "text": "Terminate the driver whose code is N42."}
{"family": "drivers", "op": "DELETE", "text": "Dismiss the driver with id 42."}
{"family": "stops", "op": "CREATE", "text": "Create a new stop near the market."}
{"family": "stops", "op": "CREATE", "text": "Add a new stop with code S7."}
{"family": "stops", "op": "CREATE", "text": "Build a new stop on the hill."}
{"family": "stops", "op": "CREATE", "text": "Set up a new stop for the school."}
{"family": "stops", "op": "READ", "text": "Show the stop named Oak Street."}
{"family": "stops", "op": "READ", "text": "Locate the stop numbered 9."}
{"family": "stops", "op": "READ", "text": "Inspect the stop with code S7."}
{"family": "stops", "op": "READ", "text": "View the stop whose code is N42."}
{"family": "stops", "op": "UPDATE", "text": "Update the stop named Oak Street."}
{"family": "stops", "op": "UPDATE", "text": "Move the stop numbered 9."}
{"family": "stops", "op": "UPDATE", "text": "Rename the stop with code S7."}
{"family": "stops", "op": "UPDATE", "text": "Fix the stop whose code is N42."}
{"family": "stops", "op": "DELETE", "text": "Delete the stop named Oak Street."}
{"family": "stops", "op": "DELETE", "text": "Remove the stop numbered 9."}
{"family": "stops", "op": "DELETE", "text": "Close the stop with code S7."}
{"family": "stops", "op": "DELETE", "text": "Discard the stop whose code is N42."}
{"family": "fares", "op": "CREATE", "text": "Create a new fare for tourists."}
{"family": "fares", "op": "CREATE", "text": "Introduce a new fare for children."}
{"family": "fares", "op": "CREATE", "text": "Add a new fare for weekend travel."}
{"family": "fares", "op": "CREATE", "text": "Set up a new fare for seniors."}
{"family": "fares", "op": "READ", "text": "Show the fare with code F3."}
{"family": "fares", "op": "READ", "text": "Find the fare named Standard."}
{"family": "fares", "op": "READ", "text": "Fetch the fare numbered 2."}
{"family": "fares", "op": "READ", "text": "Review the fare with id 5."}
{"family": "fares", "op": "UPDATE", "text": "Update the fare with code F3."}
{"family": "fares", "op": "UPDATE", "text": "Change the fare named Standard."}
{"family": "fares", "op": "UPDATE", "text": "Amend the fare numbered 2."}
{"family": "fares", "op": "UPDATE", "text": "Adjust the fare with id 5."}
{"family": "fares", "op": "DELETE", "text": "Delete the fare with code F3."}
{"family": "fares", "op": "DELETE", "text": "Remove the fare named Standard."}
{"family": "fares", "op": "DELETE", "text": "Cancel the fare numbered 2."}
{"family": "fares", "op": "DELETE", "text": "Retire the fare with id 5."}
<!-- END GOAL-BANK-G3 -->

### 13.3 OOS-BANK-G3

<!-- BEGIN OOS-BANK-G3 -->
{"family": "routes", "category": "A", "text": "Optimize the midday routes for fuel savings."}
{"family": "vehicles", "category": "A", "text": "Compare the hybrid and electric vehicles."}
{"family": "drivers", "category": "A", "text": "Rank the drivers by on-time performance."}
{"family": "stops", "category": "A", "text": "Forecast foot traffic at busy stops."}
{"family": "fares", "category": "A", "text": "Simulate revenue under new fares."}
{"family": "routes", "category": "A", "text": "Merge the two redundant express routes."}
{"family": "vehicles", "category": "A", "text": "Evaluate the battery life of electric vehicles."}
{"family": "drivers", "category": "A", "text": "Analyze fatigue trends among night drivers."}
{"family": "stops", "category": "A", "text": "Sort stops by wheelchair accessibility levels."}
{"family": "fares", "category": "A", "text": "Export fare tables for the auditor."}
{"family": "routes", "category": "B", "text": "Add a note to the crosstown route."}
{"family": "vehicles", "category": "B", "text": "Attach a damage label onto the trolley."}
{"family": "drivers", "category": "B", "text": "Put a seniority tag on the driver."}
{"family": "stops", "category": "B", "text": "Create a landmark pin for the plaza stop."}
{"family": "fares", "category": "B", "text": "Set up a surcharge line on peak fares."}
{"family": "routes", "category": "B", "text": "Add a detour warning to the highway route."}
{"family": "vehicles", "category": "B", "text": "Stick a mileage sticker on the coach."}
{"family": "drivers", "category": "B", "text": "Generate a safety badge for the trainee driver."}
{"family": "stops", "category": "B", "text": "Attach a shelter code to the transfer stop."}
{"family": "fares", "category": "B", "text": "Build a discount clause into the student fare."}
{"family": "routes", "category": "C", "text": "Reroute the bus and then alert waiting passengers."}
{"family": "vehicles", "category": "C", "text": "Check tire pressure before sending the coach out."}
{"family": "drivers", "category": "C", "text": "Swap drivers if heavy fog rolls in tonight."}
{"family": "stops", "category": "C", "text": "If it rains, close the uncovered stops."}
{"family": "fares", "category": "C", "text": "Verify eligibility before applying the discount fare."}
{"family": "routes", "category": "C", "text": "Confirm capacity and then divert the rush route."}
{"family": "vehicles", "category": "C", "text": "Charge batteries fully before releasing the shuttle."}
{"family": "drivers", "category": "C", "text": "Check licenses and then assign the night driver."}
{"family": "stops", "category": "C", "text": "Clear snow first, then open the hillside stops."}
{"family": "fares", "category": "C", "text": "Count coins and then print the change receipt."}
{"family": null, "category": "D", "text": "Send a text message to my shift supervisor."}
{"family": null, "category": "D", "text": "Reserve a hotel near the downtown core."}
{"family": null, "category": "D", "text": "Order lunch for the entire maintenance crew."}
{"family": null, "category": "D", "text": "Pay the electric bill for the depot office."}
{"family": null, "category": "D", "text": "Schedule a haircut at the corner salon."}
{"family": null, "category": "D", "text": "Call a locksmith to open the front gate."}
{"family": null, "category": "D", "text": "Subscribe to the local newspaper for home delivery."}
{"family": null, "category": "D", "text": "Book a tennis court for Saturday afternoon."}
{"family": null, "category": "D", "text": "Donate blood at the mobile clinic today."}
{"family": null, "category": "D", "text": "Pick up dry cleaning after the morning shift."}
<!-- END OOS-BANK-G3 -->

### 13.4 FROZEN-RUNNER

<!-- BEGIN FROZEN-RUNNER -->
#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38291080992 (design_contract_version 2).
# Arm A = T-FRAME+ : shared deterministic lexical selection (B-LEX-STRONG, frozen)
#   + structural frame-completeness abstention clauses C1-SUBOP, C3-NO-REFERENCE,
#   C4-COMPLEMENT, C5-SET-QUANT, C6-SOURCE (frozen) + the NEW pre-declared,
#   zero-tunable-parameter clause C7-CREATE-OBLIQUE (this experiment).
# Arm B = B-RETRIEVAL-TFIDF : stdlib pure-Python TF-IDF nearest-class-centroid
#   retrieval resolver with a calibration-fitted abstention gate (comparator).
# Stdlib only (argparse, hashlib, json, math, re, random, sys, pathlib).
# Usage: python runner_tframe_g3.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, math, os, re, random, sys
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38291080992"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
PARENT = ROOT / "research/experiments" / "EXP-GRAPH-38180711589"
GRANDPARENT = ROOT / "research/experiments" / "EXP-GRAPH-38175554380"

SEED = 38291080992 % (2 ** 32)
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
SEL_TARGET = 0.80
TOK_BAND = 0.60
TRI_BAND = 0.75

DET = {"a", "an", "the", "this", "that", "these", "those", "one", "two", "my", "your", "his", "her",
       "its", "our", "their", "each", "every", "any", "some", "all", "no", "another", "other"}
REF = {"id", "identifier", "identified", "number", "numbered", "named", "called", "titled", "referred",
       "labelled", "labeled", "code", "badge"}
QUANT = {"all", "every", "each", "any", "some", "several", "many", "both", "whole", "entire",
         "multiple", "batch", "bulk"}
POLITE = {"please", "kindly", "can", "could", "would", "will", "i", "want", "need", "help", "lets", "let"}
SOURCE = {"from", "into", "onto"}
OBLIQUE = {"to", "on", "onto", "into", "in", "at", "from", "by", "upon", "toward", "towards", "with"}
REL = {"whose", "which", "who", "that", "where", "matching", "containing"}
SUBORD = {"to", "that", "which", "who", "so", "then"}
PREP = {"of", "with", "by", "using", "for", "about", "from", "in", "to", "on", "at", "into", "onto",
        "under", "over", "across", "via", "through", "as", "per", "within", "without", "against",
        "between", "among", "upon", "toward", "towards", "near", "around", "behind", "before",
        "after", "during", "inside", "outside"}


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def self_sha() -> str:
    try:
        return sha_file(Path(__file__))
    except Exception:
        return "UNKNOWN"


def extract_block(text: str, name: str) -> str:
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->", text, re.S)
    if not m:
        raise SystemExit(f"missing block {name}")
    return m.group(1)


def jlines(block: str):
    return [json.loads(l) for l in block.splitlines() if l.strip()]


def tokens(s: str):
    return re.findall(r"[a-z]+", s.lower())


def _spans(t, phrase, plural=False):
    pt = phrase.split(); L = len(pt); res = []
    for i in range(len(t) - L + 1):
        ok = True
        for k, p in enumerate(pt):
            x = t[i + k]
            if x == p:
                continue
            if plural and (x == p + "s" or x + "s" == p):
                continue
            ok = False; break
        if ok:
            res.append((i, i + L, L))
    return res


def jaccard(a, b):
    A, B = set(a), set(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0


def trigrams(s):
    x = " " + " ".join(tokens(s)) + " "
    return {x[i:i + 3] for i in range(len(x) - 2)}


def comp(text: str, lex: dict):
    """Shared deterministic selector (B-LEX-STRONG): longest key-set + homograph guard. FROZEN."""
    t = tokens(text)
    fam_first = {p.split()[0] for ph in lex["family_nouns"].values() for p in ph}
    fsp = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(t, p, plural=True)]
    osp = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(t, p)
           if not (t[s] in fam_first and s > 0 and t[s - 1] in DET)]
    fmax = max([L for _, _, _, L in fsp], default=0); omax = max([L for _, _, _, L in osp], default=0)
    fkm = {f for f, _, _, L in fsp if L == fmax}; okm = {o for o, _, _, L in osp if L == omax}
    fst = "NONE" if not fsp else ("UNIQUE" if len(fkm) == 1 else "TIE")
    ost = "NONE" if not osp else ("UNIQUE" if len(okm) == 1 else "TIE")
    fam = list(fkm)[0] if fst == "UNIQUE" else None
    op = list(okm)[0] if ost == "UNIQUE" else None
    r1 = None
    if fam:
        s0 = min(s for f, s, _, _ in fsp if f == fam); e0 = max(e for f, _, e, _ in fsp if f == fam)
        rem = t[:s0] + t[e0:]
        ors = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(rem, p)
               if not (rem[s] in fam_first and s > 0 and rem[s - 1] in DET)]
        om = max([L for _, _, _, L in ors], default=0); okm2 = {o for o, _, _, L in ors if L == om}
        if len(okm2) == 1:
            r1 = (fam, list(okm2)[0])
    r2 = None
    if op:
        s0 = min(s for o, s, _, _ in osp if o == op); e0 = max(e for o, _, e, _ in osp if o == op)
        rem = t[:s0] + t[e0:]
        frs = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(rem, p, plural=True)]
        fm = max([L for _, _, _, L in frs], default=0); fkm2 = {f for f, _, _, L in frs if L == fm}
        if len(fkm2) == 1:
            r2 = (list(fkm2)[0], op)
    res = (r1 if r1 == r2 else None) if (r1 and r2) else (r1 or r2)
    hasref = any(w in REF for w in t)
    return dict(t=t, fsp=fsp, osp=osp, hasref=hasref,
                mech=None if res is None else f"mech_{res[0]}_{res[1].lower()}",
                fam=None if res is None else res[0], op=None if res is None else res[1],
                famNONE=int(fst == "NONE"), famTIE=int(fst == "TIE"),
                opNONE=int(ost == "NONE"), opTIE=int(ost == "TIE"),
                noslot=1 if (res is not None and res[1] in ("READ", "UPDATE", "DELETE") and not hasref) else 0,
                quant=1 if any(w in QUANT for w in t) else 0)


def frame(r: dict):
    """Frozen structural frame-completeness clauses (FROZEN, fires => ABSTAIN)."""
    t = r["t"]; cl = {}
    h = 0
    while h < len(t) and t[h] in POLITE:
        h += 1
    head = t[h] if h < len(t) else None
    fire = False
    if r["op"]:
        spans = [(s, e) for o, s, e, L in r["osp"] if o == r["op"]]
        if spans:
            osx = min(s for s, _ in spans)
            if head is not None and head != t[osx] and any(i < osx and t[i] in SUBORD for i in range(len(t))):
                fire = True
    cl["C1-SUBOP"] = fire
    cl["C3-NO-REFERENCE"] = bool(r["op"] in ("READ", "UPDATE", "DELETE") and not r["hasref"])
    cl["C4-COMPLEMENT"] = False
    cl["C6-SOURCE"] = False
    if r["fam"]:
        spans = [(s, e) for f, s, e, L in r["fsp"] if f == r["fam"]]
        if spans:
            after = t[max(e for _, e in spans):]
            idx = 0
            while idx < len(after) and after[idx] in DET:
                idx += 1
            if idx < len(after) and after[idx] not in PREP and after[idx] not in REF and after[idx] not in REL:
                cl["C4-COMPLEMENT"] = True
            if r["op"] == "CREATE" and any(w in SOURCE for w in after):
                cl["C6-SOURCE"] = True
    cl["C5-SET-QUANT"] = any(w in QUANT for w in t)
    return cl


def clause_c7(r: dict) -> bool:
    """NEW pre-declared clause C7-CREATE-OBLIQUE. Zero tunable parameters.
    Fires for a bound CREATE operation when either:
      (a) a source/extraction preposition {from, into, onto} occurs anywhere in the instruction
          (the object being created/imported is placed from/onto/into a host resource); or
      (b) a placement preposition {to,on,onto,into,in,at,from,by,upon,toward,towards,with} occurs
          strictly between the end of the matched CREATE verb phrase and the start of the first
          bound-family noun phrase (the resource sits in an oblique argument, so the created
          entity is a non-resource object attached to it).
    Both triggers are structural and threshold-free."""
    if r["op"] != "CREATE":
        return False
    t = r["t"]
    if any(w in SOURCE for w in t):
        return True
    osp = [(s, e) for o, s, e, L in r["osp"] if o == "CREATE"]
    if not osp:
        return False
    osx = min(e for _, e in osp)
    fs = [s for f, s, e, L in r["fsp"] if f == r["fam"] and s >= osx] if r["fam"] else []
    if fs and any(t[i] in OBLIQUE for i in range(osx, min(fs))):
        return True
    return False


def analyze(text: str, lex: dict):
    r = comp(text, lex)
    cl = frame(r)
    cl["C7-CREATE-OBLIQUE"] = clause_c7(r)
    r["clauses"] = cl
    r["S"] = r["famNONE"] + r["opNONE"] + r["opTIE"] + r["noslot"] + r["quant"]
    return r


def is_executed(r: dict, mode: str) -> bool:
    if mode == "gatefree":
        return r["mech"] is not None
    if mode == "incumbent":
        return r["mech"] is not None and r["S"] <= 0
    if mode == "tframe_frozen":  # existing 5 clauses, WITHOUT C7 (diagnostic only)
        return r["mech"] is not None and not any(v for k, v in r["clauses"].items() if k != "C7-CREATE-OBLIQUE")
    return r["mech"] is not None and not any(r["clauses"].values())  # tframeplus (Arm A)


def target_of(goal):
    return f"mech_{goal['family']}_{goal['op'].lower()}"


def build_axis(app, oos, lex, splitmod, prior_texts):
    rows = []
    for i, g in enumerate(app):
        rows.append(dict(gid=f"app_{i+1:03d}", text=g["text"], app=1, target=target_of(g), split=(i % splitmod) in (1, 3, 5)))
    for i, g in enumerate(oos):
        rows.append(dict(gid=f"oos_{i+1:03d}", text=g["text"], app=0, target=None, split=(i % splitmod) in (1, 3, 5)))
    flagged = []
    for r in rows:
        r.update(analyze(r["text"], lex))
        if max(jaccard(tokens(r["text"]), tokens(p)) for p in prior_texts) >= TOK_BAND or \
           max(jaccard(trigrams(r["text"]), trigrams(p)) for p in prior_texts) >= TRI_BAND:
            flagged.append(r["gid"])
    bound = [r for r in rows if r["gid"] not in flagged]
    return bound, flagged


def metrics(rows, mode):
    ex = [r for r in rows if is_executed(r, mode)]
    exo = sum(1 for r in ex if not r["app"]); exa = sum(1 for r in ex if r["app"])
    co = sum(1 for r in rows if not r["app"]); ca = sum(1 for r in rows if r["app"])
    abR = [r for r in rows if r["mech"] is not None and not is_executed(r, mode)]
    abRo = sum(1 for r in abR if not r["app"])
    ab_all = [r for r in rows if not is_executed(r, mode)]
    sel = sum(1 for r in ex if r["app"] and r["mech"] == r["target"])
    return dict(coverage=exa / ca if ca else None, pooled_false_accept=exo / co if co else None,
                unknown_precision=abRo / len(abR) if abR else None,
                unknown_precision_inclusive=(sum(1 for r in ab_all if not r["app"]) / len(ab_all)) if ab_all else None,
                executed=len(ex), executed_oos=exo, executed_app=exa, abstained_resolved=len(abR),
                selective_acc=sel / exa if exa else None,
                unresolved_applicable=sum(1 for r in rows if r["app"] and r["mech"] is None))


def gate_met(m):
    return bool(m["pooled_false_accept"] is not None and m["pooled_false_accept"] <= FA_TARGET
                and m["coverage"] is not None and m["coverage"] >= COV_TARGET
                and m["unknown_precision"] is not None and m["unknown_precision"] >= PREC_TARGET)


# ---------------- Arm B : stdlib TF-IDF nearest-centroid retrieval ----------------
def _feats(text):
    t = tokens(text)
    bg = [t[i] + "_" + t[i + 1] for i in range(len(t) - 1)]
    return t + bg


def _vec(fs, idf):
    v = {}
    for f in fs:
        v[f] = v.get(f, 0.0) + 1.0
    for f in list(v):
        v[f] = (1.0 + math.log(v[f])) * idf.get(f, 0.0)
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {f: x / n for f, x in v.items()}


def _cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(f, 0.0) for f, x in a.items())


def arm_b(cal, test, seed):
    fit = [r for r in cal if r["app"]]
    N = len(fit)
    df = {}
    docs = []
    for r in fit:
        fs = _feats(r["text"])
        docs.append((r["target"], fs))
        for f in set(fs):
            df[f] = df.get(f, 0) + 1
    idf = {f: math.log((1 + N) / (1 + d)) + 1.0 for f, d in df.items()}
    cent = {}
    for cls, fs in docs:
        v = _vec(fs, idf)
        c = cent.setdefault(cls, {})
        for f, x in v.items():
            c[f] = c.get(f, 0.0) + x
    cent = {cls: _vec([], {}) if not v else {f: x / (math.sqrt(sum(y * y for y in v.values())) or 1.0) for f, x in v.items()} for cls, v in cent.items()}

    def score(rows):
        out = []
        for r in rows:
            v = _vec(_feats(r["text"]), idf)
            sims = sorted(((_cos(v, c), cls) for cls, c in cent.items()), reverse=True)
            top = sims[0][0] if sims else 0.0
            margin = (sims[0][0] - sims[1][0]) if len(sims) > 1 else 1.0
            out.append((r, sims[0][1] if sims else None, top, margin))
        return out

    def gate_metrics(scored, tau, mu):
        ex = [(r, cls) for r, cls, s, m in scored if s >= tau and m >= mu]
        ab = [(r, cls, s, m) for r, cls, s, m in scored if not (s >= tau and m >= mu)]
        exo = sum(1 for r, c in ex if not r["app"]); exa = sum(1 for r, c in ex if r["app"])
        co = sum(1 for r in scored if not r[0]["app"]); ca = sum(1 for r in scored if r[0]["app"])
        abRo = sum(1 for r, c, s, m in ab if not r["app"])
        sel = sum(1 for r, c in ex if r["app"] and c == r["target"])
        return dict(coverage=exa / ca if ca else 0.0, pooled_false_accept=exo / co if co else None,
                    unknown_precision=abRo / len(ab) if ab else None, selective_acc=sel / exa if exa else None,
                    executed=len(ex), executed_app=exa, executed_oos=exo, abstained=len(ab))

    cal_scored = score(cal)
    taus = sorted({round(s, 4) for _, _, s, _ in cal_scored})
    mus = sorted({round(m, 4) for _, _, _, m in cal_scored})
    best = None
    for tau in taus:
        for mu in mus:
            gm = gate_metrics(cal_scored, tau, mu)
            feasible = (gm["pooled_false_accept"] is not None and gm["pooled_false_accept"] <= FA_TARGET
                        and gm["coverage"] >= COV_TARGET
                        and gm["unknown_precision"] is not None and gm["unknown_precision"] >= PREC_TARGET)
            key = (1 if feasible else 0, gm["coverage"] if gm["coverage"] else 0.0)
            if best is None or key > best[0]:
                best = (key, (tau, mu), gm)
    if best is None:
        return dict(tau=None, mu=None, cal_gate=None, cal_fit_feasible=False,
                    test_gate=gate_metrics([], 1.0, 1.0), classes=sorted(cent.keys()), n_fit=len(fit))
    tau, mu = best[1]
    cal_gate = best[2]
    fit_feasible = bool(best[0][0])
    test_rows = test
    test_scored = score(test_rows)
    test_gate = gate_metrics(test_scored, tau, mu)
    return dict(tau=tau, mu=mu, cal_gate=cal_gate, cal_fit_feasible=fit_feasible, test_gate=test_gate,
                classes=sorted(cent.keys()), n_fit=len(fit))


def shuffled_selection(rows, mode, seed):
    rng = random.Random(seed)
    ex = [r for r in rows if is_executed(r, mode) and r["app"]]
    if not ex:
        return None
    targets = [r["target"] for r in ex]
    rng.shuffle(targets)
    return sum(1 for r, t in zip(ex, targets) if r["mech"] == t) / len(ex)


def random_role_selection(rows, mode, seed):
    rng = random.Random(seed)
    mechs = sorted({r["target"] for r in rows if r["app"]})
    ex = [r for r in rows if is_executed(r, mode) and r["app"]]
    if not ex or not mechs:
        return None
    return sum(1 for r in ex if r["mech"] == rng.choice(mechs)) / len(ex)


def matched_random_gate(rows, mode, seed):
    rng = random.Random(seed)
    ab_n = sum(1 for r in rows if not is_executed(r, mode))
    idx = list(range(len(rows))); rng.shuffle(idx)
    ab = set(idx[:ab_n])
    ex = [r for i, r in enumerate(rows) if i not in ab]
    co = [r for r in rows if not r["app"]]
    abr = [r for i, r in enumerate(rows) if i in ab]
    return dict(pooled_false_accept=(sum(1 for r in ex if not r["app"]) / len(co)) if co else None,
                unknown_precision=(sum(1 for r in abr if not r["app"]) / len(abr)) if abr else None,
                matched_abstention_count=ab_n)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    prereg_path = Path(os.environ.get("SPIDER_PREREG", str(EXP_DIR / "prereg.md")))
    self_text = prereg_path.read_text(encoding="utf-8")
    g3_app = jlines(extract_block(self_text, "GOAL-BANK-G3"))
    g3_oos = jlines(extract_block(self_text, "OOS-BANK-G3"))
    lex_g3 = json.loads(extract_block(self_text, "LEXICON-G3"))
    parent_text = (PARENT / "prereg.md").read_text(encoding="utf-8")
    g1_app = jlines(extract_block(parent_text, "GOAL-BANK-G1"))
    g1_oos = jlines(extract_block(parent_text, "OOS-BANK-G1"))
    lex_g1 = json.loads(extract_block(parent_text, "LEXICON-G1"))
    lex_alt = json.loads(extract_block(parent_text, "LEXICON-G1-ALT"))
    g2_app = jlines(extract_block(parent_text, "GOAL-BANK-G2"))
    g2_oos = jlines(extract_block(parent_text, "OOS-BANK-G2"))
    lex_ho = json.loads(extract_block(parent_text, "LEXICON-G2-HELDOUT"))
    grand = (GRANDPARENT / "prereg.md").read_text(encoding="utf-8")
    prior_parent = json.loads(extract_block(grand, "PRIOR-PARENT-BANK-TEXTS"))
    sys.path.insert(0, str(ROOT / "research/harness"))
    from goal_generator import INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES
    gg = list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs] + \
        list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES)
    prior_full = gg + list(prior_parent)
    priors_g3 = gg + list(prior_parent) + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos] + \
        [g["text"] for g in g2_app] + [g["text"] for g in g2_oos]

    axes = {}
    for nm, (app, oos, lex, sm, priors) in {
        "AXIS-G3-NEW": (g3_app, g3_oos, lex_g3, 4, priors_g3),
        "AXIS-G2-RETEST": (g2_app, g2_oos, lex_ho, 4, gg + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos]),
        "AXIS-G1-PRIMARY": (g1_app, g1_oos, lex_g1, 6, prior_full),
        "AXIS-G1-ALTLEX": (g1_app, g1_oos, lex_alt, 6, prior_full),
    }.items():
        bound, flagged = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        axes[nm] = dict(bound=bound, flagged=flagged, cal=cal, test=test,
                        cal_metrics={m: metrics(cal, m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")})
        if not args.mechanics_only:
            axes[nm]["test_metrics"] = {m: metrics(test, m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
            axes[nm]["arm_b"] = arm_b(cal, test, SEED)
            axes[nm]["shuffled_selection"] = shuffled_selection(test, "tframeplus", SEED)
            axes[nm]["random_role_selection"] = random_role_selection(test, "tframeplus", SEED)
            axes[nm]["ctrl_random_gate"] = matched_random_gate(test, "tframeplus", SEED)

    if args.mechanics_only:
        out = dict(status="DESIGN-MECHANICS-ONLY", experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
                   axes={k: dict(bound=len(v["bound"]), flagged=v["flagged"],
                                 cal_n=[sum(1 for r in v["cal"] if r["app"]), sum(1 for r in v["cal"] if not r["app"])],
                                 cal_metrics=v["cal_metrics"],
                                 cal_feasible_tframeplus=gate_met(v["cal_metrics"]["tframeplus"])) for k, v in axes.items()},
                   c7_firing={k: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                      oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                              for k, v in axes.items()},
                   liveness=dict(g3_cal_executed=axes["AXIS-G3-NEW"]["cal_metrics"]["tframeplus"]["executed"],
                                 g3_cal_unresolved=axes["AXIS-G3-NEW"]["cal_metrics"]["tframeplus"]["unresolved_applicable"]),
                   embedding_status="REPLACED-BY-B-RETRIEVAL-TFIDF-STDLIB")
        print(json.dumps(out, indent=2))
        return

    prim = axes["AXIS-G3-NEW"]["test_metrics"]["tframeplus"]
    gates = {a: gate_met(v["test_metrics"]["tframeplus"]) for a, v in axes.items()}
    sels = {a: v["test_metrics"]["tframeplus"]["selective_acc"] for a, v in axes.items()}
    selection_preserved = all(s is not None and s >= SEL_TARGET for s in sels.values())
    g3t = axes["AXIS-G3-NEW"]["test"]
    g3t_total = len(g3t)
    g3t_abstained_resolved = sum(1 for r in g3t if r["mech"] is not None and not is_executed(r, "tframeplus"))
    live = ((0 < prim["executed"] < g3t_total)
            and (prim["executed_app"] >= 1)
            and (g3t_abstained_resolved >= 1))
    invalid_reasons = []
    if not live:
        invalid_reasons.append("treatment-not-live: AXIS-G3-NEW test non-degenerate execution failed (need 0 < executed_total < n_total_test AND executed_app >= 1 AND abstained_resolved >= 1)")
    for a, v in axes.items():
        if v["test_metrics"]["tframeplus"]["unknown_precision"] is None:
            invalid_reasons.append(f"{a}: unknown_precision undefined (no resolved abstention on test)")
    g3_gate = gates.get("AXIS-G3-NEW"); g2_gate = gates.get("AXIS-G2-RETEST")
    armb_g3 = axes["AXIS-G3-NEW"]["arm_b"]
    armb_g2 = axes["AXIS-G2-RETEST"]["arm_b"]
    armb_g3_met = (armb_g3["test_gate"]["pooled_false_accept"] is not None
                   and armb_g3["test_gate"]["pooled_false_accept"] <= FA_TARGET
                   and armb_g3["test_gate"]["coverage"] >= COV_TARGET
                   and armb_g3["test_gate"]["unknown_precision"] is not None
                   and armb_g3["test_gate"]["unknown_precision"] >= PREC_TARGET)
    armb_g2_met = (armb_g2["test_gate"]["pooled_false_accept"] is not None
                   and armb_g2["test_gate"]["pooled_false_accept"] <= FA_TARGET
                   and armb_g2["test_gate"]["coverage"] >= COV_TARGET
                   and armb_g2["test_gate"]["unknown_precision"] is not None
                   and armb_g2["test_gate"]["unknown_precision"] >= PREC_TARGET)
    if armb_g3_met and not g3_gate:
        retrieval_fork = "RETRIEVAL_DOMINATES_G3"
    elif g3_gate and not armb_g3_met:
        retrieval_fork = "TFRAME_DOMINATES_G3"
    elif g3_gate and armb_g3_met:
        retrieval_fork = "BOTH_PASS_G3"
    else:
        retrieval_fork = "NEITHER_PASSES_G3"
    status = "MEASUREMENT_INVALID" if invalid_reasons else "COMPLETE"
    if invalid_reasons:
        decision = None
    elif g3_gate and g2_gate and selection_preserved:
        decision = "DECIDE_SHIP_TFRAME_BROAD"
    elif g2_gate and selection_preserved:
        decision = "DECIDE_SHIP_TFRAME_SCOPED"
    else:
        decision = "DECIDE_REQUIRE_RETRIEVAL_B"
    out = dict(status=status, experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
               invalid_reasons=invalid_reasons, decision=decision,
               gates=gates, selection={a: sels[a] for a in sels}, selection_preserved=selection_preserved,
               selection_rule="B-LEX-STRONG + C7-CREATE-OBLIQUE",
               retrieval_fork=retrieval_fork, arm_b_gate_met={"g3": armb_g3_met, "g2": armb_g2_met},
               arm_b={"g3": armb_g3["test_gate"], "g2": armb_g2["test_gate"],
                      "g3_tau": armb_g3["tau"], "g3_mu": armb_g3["mu"],
                      "g3_cal_fit_feasible": armb_g3["cal_fit_feasible"]},
               test_metrics={a: v["test_metrics"] for a, v in axes.items()},
               test_n={a: [sum(1 for r in v["test"] if r["app"]), sum(1 for r in v["test"] if not r["app"])] for a, v in axes.items()},
               cal_metrics={a: v["cal_metrics"] for a, v in axes.items()},
               c7_firing={a: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                  oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                          for a, v in axes.items()},
               execution_vectors={a: {r["gid"]: {"split": "test" if r["split"] else "cal",
                                                 "app": r["app"], "mech": r["mech"], "target": r["target"],
                                                 "text_sha256": hashlib.sha256(r["text"].encode()).hexdigest(),
                                                 "clauses": r["clauses"], "S": r["S"],
                                                 "executed": is_executed(r, "tframeplus")} for r in v["bound"]}
                                 for a, v in axes.items()},
               controls={a: dict(shuffled_selection=v["shuffled_selection"], random_role_selection=v["random_role_selection"],
                                 ctrl_random_gate=v["ctrl_random_gate"],
                                 b_lex_strong=v["test_metrics"]["tframeplus"]["selective_acc"],
                                 b_lex_only=v["test_metrics"]["gatefree"]["selective_acc"],
                                 b_incumbent_kernel=0.0,
                                 ctrl_exec_all_fa=v["test_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_abstain_all_cov=0.0, ctrl_abstain_all_up=1.0) for a, v in axes.items()},
               flagged={a: v["flagged"] for a, v in axes.items()})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
<!-- END FROZEN-RUNNER -->

## 14. Director-mandate conformance, pre-2.0 comparison, and stop-rule compliance

- Binding direction: `request.json#director_mandate` (cycle `38290683955`, Graph PIVOT, `C-SEMANTIC-RESOLVE`). This design converts its strategic question into the smallest rigorous repair experiment: SAME G3-NEW surface, SAME zero-tunable clause set, single liveness-scope fix. No third surface authored, no refitting, no drift to the parent handoff's local proposal.
- Pre-2.0 comparison (`codex/legacy_brief.json`, `codex/legacy_artifact_index.json`, targeted archive reads only): `LEGACY: DISTINCT_EXTENSION`. `P2-BLIND-COMPOSITION` (pre2 product summary artifact 4.697 sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`: 3/3 compositions with keyword/oracle caveats) and `P2-MIND2WEB` (archived Codex section 1: 176 routes, 3.41% exact matches) concern composition/retrieval breadth, not a deterministic resolver liveness-predicate scope defect on a fixed split. Corroborating grep over the mounted `.spider-runtime/pre2/SPIDER_CODEX_ULTIME.md` (566403 lines): zero hits for `T-FRAME`, and `liveness` hits concern only infrastructure aliveness, never a resolver liveness predicate - no pre-2.0 artefact tests, or could test, a liveness-predicate scope repair; nothing is repeated. The guard from both precedents (strong comparators, no oracle/keyword crutches) is honored via the measurable stdlib retrieval Arm B and the frozen enumerated fork.
- Stop-rule compliance: the mandate's "do not iterate surface thrice / any refit, third surface, or predicate evaluated off-split -> MEASUREMENT_INVALID, park thread" is frozen into the design - the G3 bank bytes are verbatim copies of the parent prereg blocks (sameness verifiable by block sha), the clause set is byte-identical including C7, and the predicate names its evaluated split explicitly.
- Product consequence restated: VALID-`DECIDE_REQUIRE_RETRIEVAL_B` (expected) bounds T-FRAME to PRIMARY+ALTLEX, retains `C-SEMANTIC-RESOLVE` at HYPOTHESIS with a valid fork observation favouring structure (`BOTH_PASS_G3` with selective_acc asymmetry + G2 collapse), and Product keeps the conservative shipped abstention boundary. VALID ship-scope branches would re-open the EXPERIMENTAL question for the Director; `MEASUREMENT_INVALID` again retires this surface family. This packet itself promotes nothing to product.

_End of frozen preregistration._
