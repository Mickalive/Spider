# R1 CYCLE 1 — FROZEN PREREGISTRATION

Status: **FROZEN** — committed BEFORE any sweep outcome, any live launch,
any economics measurement result, or any negative-control outcome existed
(git-orderable freeze; closes the W4 discipline for this cycle).
Cycle: R1-1 (Program R1 "Compression Validation & Honest Economics").
GitHub run: 32916020607. Branch: `cycle/runtime/32916020607/team`.
Directive: `directives/RUNTIME.md` (R1 priorities 1–6). Refuse list obeyed.

---

## 0. Question and branch structure

Program R1 question (chartered): *Does any memory-free scripted policy —
goal tokens plus a frozen generic account-affordance/href vocabulary frozen
pre-outcome — reach the login anchor from both committed entry snapshots
within SPIDER's four-action budget; and if one exists and runs live, does
SPIDER inheritance still strictly win?*

Three outcome branches, decided MECHANICALLY by sections 2/3 below:

* **B-NO-SURVIVOR** — no variant passes the survival bar → live arm is
  REFUSED; the offline bound becomes durable negative knowledge.
* **B-KILLED** — survivor runs live and fails every margin gate → the
  near-repeat compression OBSERVATION does not survive its strongest
  preregistered comparator (observation-strength scoped negative).
* **B-SURVIVES** — survivor runs live and all margin gates hold → the
  compression OBSERVATION survives its strongest comparator (still
  OBSERVATION strength; multi-task replication owed to R1-2).

No other interpretation of outcomes is authorized. Post-hoc wording
beyond section 8 ceilings is prohibited.

## 0.1 Inputs (all pre-existing, hash-pinned)

* Committed T3 entry snapshots (AUDITED_DURABLE lineage, recorded live in
  R0-2): `results/runtime/probes/entry_snapshot_taglove.json` — file sha256
  `f5a306041c32509728ba90cd15bd2b93ccc1e791af4409bba46ae822f4621241`,
  inner page digest `b66af808aaaf6a60fa558b49ca03e7a2c8f5cfc3d7cde88218d9498c838f1f91`;
  `results/runtime/probes/entry_snapshot_page10.json` — file sha256
  `7abf039fbe942bdaa9036c978f6d1140bc79878b0b84a24ec087c6ef24e1b9b0`,
  inner page digest `96d2c4a5e545b5d91432db3298d8df393b0ce4ea1ec32c5ef6780f05719787cb`.
  Dual pins are checked at load; either mismatch aborts the sweep.
* Parent capsule registry + quarantined `-wb` registry (accepted R0-2).
* Accepted observation store (7 records) and accepted pilot2 stream
  (`results/runtime/pilot2/cost_events.jsonl`, 224 spider rows;
  `pilot_results.json`) — read-only inputs for the wb-v2 evidence join
  and for the W-C2-5 golden pin.

## 1. Priority 1 — OFFLINE POLICY-SWEEP GATE (zero browser launches)

### 1.1 Policy family (FROZEN)

Eight gated variants = features × root_bonus:
features ∈ {`goal_only`, `goal_lexicon`, `goal_href`,
`goal_lexicon_href`} × root_bonus ∈ {0, 2}.

Matching operator (FROZEN): **token-boundary equality only. Substring
containment is prohibited.** All strings NFKC-normalized, casefolded,
tokenized to `[a-z0-9]+` runs. Element surface = text ∪ aria tokens;
href path tokens included in keyword matching. Rationale: substring
semantics scores `auth` inside `/author/…` (~20 false affordances per
recorded snapshot) and produced the recorded `"site"~"opposite"` artifact
in `t3_offline_rank_probe.json`.

Weights (FROZEN pre-outcome): keyword hit +3 (legacy lineage);
account-affordance class hit +6; href-pattern hit +6; button tag +1;
root prior +root_bonus for href ∈ {"/", "#"} only. Tie-break: ascending
snapshot element index. The legacy baseline's brand-text home-link bonus
is deliberately NOT inherited (recorded as an inherited Graph-lineage
defect); root prior uses generic href ∈ {"/", "#"} signals only when the
variant carries root_bonus=2.

Account-affordance LEXICON (FROZEN, canonical-JSON sha256
`7c76bdb76634b87174ff8b841ed5ad2440573089cac798324202a8a338b3243d`),
five equivalence classes:

```
[auth, authenticate, authentication, log, log-in, login, sign, sign-in,
 signin, signon]
[account, acct, member, profile]
[join, register, registration, sign-up, signup]
[passphrase, passwd, password, pwd]
[email, login-name, loginname, user, username]
```

HREF PRIOR (FROZEN regex): `(?:^|/)(?:login|signin|sign-in|log-in|signon|
auth)(?:/|$)` over the href path.

"Retire-order" is NOT an independent axis: on an immutable single
snapshot, retire-and-repeat degenerates to walking one static ranking;
every retirement variant is a PREFIX of the same ordering. It is reported
as descriptive picks-to-reach only and never gates. The root-bonus axis is
kept as a gated axis because it can reorder candidates (it is a real score
term), while retirement cannot.

### 1.2 Attestation (lexicon authorship honesty)

The lexicon was authored by agents AWARE of audit warning W-C2-6 (the
synonym gap between the T3 goal text and the "Login" anchor). Genericity
is claimed from generic web UI vocabulary usage of each token, NOT from
designer ignorance; no target-site string ("toscrape", brand phrases,
demo credentials) appears in the lexicon BY CONSTRUCTION, verified by a
mechanical scan against the frozen blinding-token fixture
(`runtime/schemas/policy_blinding_tokens.json`, sha256
`94114009b32f48d486e372cb4df84dec4d611107019dd7b8576f2787538b49e7`).
The oracle (§1.3) is task ground truth, not a lexicon input; lexicon
authors saw the oracle definition. **The lexicon is single-shot**: no
token may be added, removed, or reweighted after any sweep or live output
this cycle; changes require a new preregistration.

### 1.3 Oracle and survival bar (FROZEN)

Oracle (task ground truth): an element whose normalized text == `login`
OR whose href path (trailing slash stripped, casefolded) == `/login`.
Normalization is required because snapshots record text `Login`; exact-
case clauses would be dead wiring (gate-repair precedent avoided here by
construction).

**SURVIVAL BAR (gates the live arm): a variant SURVIVES iff an oracle
element ranks STRICT FIRST under the variant's deterministic ordering on
BOTH committed entries AND that top-1 placement holds under K=100 seeded
permutations of equal-score tie groups (permutation seed 20260826 +
crc32(variant id); variants whose top-1 depends on element order are
TIE-LUCK-DEPENDENT and are ineligible to trigger the live arm).**

Why rank-based rather than "reachable within ≤4 simulated clicks":
SPIDER's pinned plan spends action 1 clicking the Login anchor; a policy
that first reaches the anchor at simulated pick k>1 needs ≥ k+3 live
actions, so under budget parity a weaker bar selects policies
arithmetically incapable of parity and makes the live arm confirmatory
rather than discriminating. Rank-1 is the only offline condition under
which the kill branch remains reachable. The offline sweep is therefore a
frozen NECESSARY-condition gate: no survivor ⇒ final negative knowledge
at ≤4 actions for this family; any survivor ⇒ exactly one live
confirmation, never an offline performance claim.

Descriptive statistics recorded per variant per entry (never gating):
full rank distribution head with scores, retire-and-repeat
picks-to-reach within 4, permutation top-1 fraction.

### 1.4 Decision rule (mechanical, no discretion)

Survivor set non-empty ⇒ live arm runs the UNIQUE winner by frozen
tie-break: fewest feature additions beyond goal_only (lexicon +1,
href +1), then lexicographic variant id. Empty ⇒ live arm REFUSED and the
offline bound is recorded as durable negative knowledge. **No variant may
be added, reweighted, or re-scored after sweep output has been viewed.**

### 1.5 Disclosed limitations (priority 1)

* Offline simulation performs zero navigation; survival is necessary-not-
  sufficient, and no offline number predicts live action counts.
* Survival is rank-based partly because click-sequence survival would
  select policies arithmetically incapable of success under budget parity.
* The lexicon was designed with knowledge of the target failure mode; its
  genericity rests on attestation, not blindness.
* Winner selection among tied survivors is arbitrary by frozen tie-break;
  claims are scoped to "a representative of the strongest frozen
  memory-free family", never "the strongest possible baseline".
* Both snapshots come from one site family on one date; drift is bounded
  by digest guards, not eliminated; DOM-order fragility is quantified by
  the permutation audit, not removed.
* One task family, two offset entries; pilot scale throughout.

## 2. Priority 2 — AT MOST ONE LIVE STRONGEST-BASELINE ARM

Runs ONLY under §1.4 survivor branch (refuse list: no live stronger-
baseline arm without an offline-surviving policy).

### 2.1 Cells and pairing (FROZEN)

Tasks RT2-T3-nearrepeat-taglove (/tag/love/) and RT2-T3-nearrepeat-page10
(/page/10/) — the SAME two entries as the audited T3 observation. Two
paired passes each. Counterbalanced arm order FROZEN NOW: pass 1 STRONG
first then SPIDER; pass 2 SPIDER first then STRONG (order-effect cancel).
Fresh browser session per row. Deterministic health trips allow max ONE
PAIRED retry (both arms or neither); originals preserved append-only.

### 2.2 Arms (FROZEN)

STRONG = `StrongExplorer(policy_id)` running the §1.4 winner via THE SAME
scoring module as the simulator (identity asserted by test — an offline
survivor must not be a simulator artifact). Standard budgets identical to
the audited zero-provider baseline: MAX_CLICKS=30 / MAX_LOADS=16 /
WALL_S=80 s advisory; health floor dom_bytes≥1200 ∧ elements≥5. **No cap
in the producer-favoring direction is imposed**; budget exhaustion is
recorded truthfully and licenses ONLY failure-avoidance wording (see
G-R1a censoring). Typed-fill logic consumes the SHARED task fills spec
(identical information both arms).

Blinding fixture (mechanical, pre-launch): policies module source and all
STRONG-side task inputs scanned against the forbidden-token fixture
(capsule ids, registry paths, site strings, credentials, witness refs).
The shared goal-text echo is exempt by design (identical information both
arms). Residual disclosed: authors know the oracle; the test is biased in
the BASELINE'S favor by construction (policy selected ON these snapshots)
— that direction is honest and deliberate.

SPIDER arm = the audited R0-2 repeat shape RE-RUN LIVE (numbers never
reused across sessions — drift stays inside the experiment). Behavior
identity: same resolve→execute→verify flow, same pinned 4-step plan, same
event grammar; wall-clock values necessarily differ and stay advisory.

Drift guard: both arms serialize their entry digest as event-stream rows;
within-pair digest equality required; live digests compared to the
committed snapshot page digests; after the one paired retry, remaining
mismatch rows are excluded as DIGEST_MISMATCH (recorded, disclosed).

Metric mapping freeze: primary unit = STREAM-COUNTED BROWSER ACTIONS
(cost-event `-actN` rows) for BOTH arms; loads counted separately;
wall-clock advisory only. MARGIN M=2 (inherited noise-surviving margin).

### 2.3 Gates (FROZEN; survivor-blind wiring; witness refs from registry)

Gate code (`runtime/gates_r1.py`) is parameterized by policy_id read from
the committed sweep artifact and by run-id maps; it MUST be committed
before any launch and MUST self-test on fabricated streams for BOTH
branches (strong-success / strong-exhaustion) proving outcome-blindness —
this prevents a second gate-repair addendum (W-C2-3 lesson).

* **G-R1a** per-pass success structure: BOTH arms harness-judged
  (predicate dialect, harness-only judge) on every pass. Any pass where
  STRONG fails/exhausts is CENSORED for compression wording (no inf, no
  capped-denominator margins); truthful recording required.
* **G-R1b** compression survival vs strongest baseline: per-pass margin
  (STRONG_actions − SPIDER_actions) ≥ M=2 on EVERY pass AND aggregate sum
  inequality ≥ M×passes AND zero censored passes AND no sign discordance
  between passes. **Split outcome** (some passes ≥M, others <M, both arms
  succeeding everywhere) ⇒ "does not survive cleanly", reported
  per-entry, never averaged.
* **G-R1c** mechanical trail: SPIDER trail predicates P1–P5 true per pass
  with reused == steps_len pinned by APPLICABILITY_PASS rows and zero
  novel actions; entry-digest pair equality; committed-digest drift
  recorded as disclosure; twin-identity errors zero.
* Witness refs are READ FROM REGISTRY CAPSULE ARTIFACTS
  (`expected_effects[0].witness_predicate.predicate_ref`); the accepted
  ref-set duality (harness task ref on STRONG verify rows vs capsule
  witness ref on SPIDER verify rows naming the same clause body) is
  handled by construction via the audited `_harness_verdict` machinery.

### 2.4 Disclosed limitations (priority 2)

* STRONG budget exhaustion licenses only failure-avoidance wording and
  censors compression denominators for that pass.
* In-family-optimal policy selection biases the test toward the baseline;
  claims remain scoped to "the strongest frozen scripted comparator".
* Two passes × two entries replicate the ORIGINAL observation's strength
  exactly; this cycle can kill or preserve an OBSERVATION, never upgrade
  it to REPLICATION.

## 3. Priority 3 — WRITE-BACK ECONOMICS (rescoped)

### 3.1 Overhead-side measurement (W-C2-1)

Decomposed operations, each timed natively (perf_counter), 30 reps, cold
rep 1 reported SEPARATELY (never averaged away): `build_record`
(validation+hash), `put_fresh`, `put_idempotent` (read+deep-compare
branch), `hygiene_filter` (strip_value_tokens), `derive_successors`
(full observation set incl. dominance scan), `registry_append`
(content-addressed append incl. O(N) index rewrite), `index_read_all`
(Registry.all_latest over parent+wb union), `resolve_e2e` (full offline
resolve() — the recurring consumer-side tax paid by EVERY resolution).

Rules: benchmark runs on a /tmp CLONE of accepted registries/observations;
accepted-path byte identity asserted after; telemetry rides NOTE
discriminators inside the frozen envelope (`phase="diag"`,
`stage="maintenance"`, `event_class="summary_event"`, note kind
`WB_MAINTENANCE_MEASURE` with min/median/max/cold) — NO new cost_event
fields; separate events file under `results/runtime/economics/`;
asymptotic order stated analytically per op; figures are point
measurements at the current population (7 observations, 3 capsules) with
NO linear extrapolation claimed. Excluded-from-accounting disclosure:
telemetry emission itself; fsync/durability window (os.replace without
fsync); repository growth/commit cost.

### 3.2 wb-v2 re-derivation (W-C2-2 semantics pin)

Construction RULE (not hardcoded answers): each verified-outcome
observation's `task_id` is joined to the ACCEPTED R0-2 verification
evidence (`pilot_results.json` rows where `arm=="spider"` ∧ `success` ∧
`cell_task==task_id` → host(`final_url`)). effect_witnessed_hosts := that
join (= {quotes.toscrape.com} expected); observed_entry_hosts := hosts of
the observations' own entry_urls (incl. books.toscrape.com, which hosted
a correct ABSTAIN) move into `context_signature.observed_entry_hosts`.
Preconditions additionally retain the EXECUTION-witnessed step-1
affordance (`elem_text_any=["login"]`) — a separately-named evidence
class required by mechanism execution. Both classes named distinctly in
`derived_from`. Artifact: `runtime/form-login-procedure-wb@v2`, appended
to the quarantined registry (append-only monotone versioning), provenance
pointing at v1's content sha256; **v1 file byte-untouched**;
`validate_capsule` smoke BEFORE freezing; status stays CANDIDATE;
`negative_knowledge` stays empty (frozen-v0 checker rejects populated
free-object arrays — known /v1 candidate). The fact that
spider.observation/v0 cannot express the EFFECT-witnessed host is logged
as the THIRD /v1 schema candidate in the derivation manifest and report.

Disclosed open failure mode: an already-authenticated caller finds no
login anchor → applicability fail → ABSTAIN instead of satisfied-goal
short-circuit (unresolved; scoped out this cycle).

### 3.3 Yield and break-even bookkeeping (FROZEN definitions)

**Branch chosen pre-outcome: reuse_yield is UNDEFINED — not pending, not
zero** (zero would require consuming tasks that gained nothing; none
exist; no wb capsule has ever been consumed by any cell). No consumer
cell runs this cycle (complexity-per-cycle constraint; quarantined tier).
To keep this non-evasive: (i) definitions below are frozen now; (ii) the
minimal R1-2 consumer cell is preregistered HERE — verbatim T1 goal
text, ONE paired cell resolved against wb-v2 vs parent-resolved, same
executor, stream-counted actions primary, paired health-retry only, both
outcome directions meaningful (fewer actions than parent arm ⇒ write-back
value > 0; equal/worse ⇒ write-back failed its reason to exist); (iii) no
reuse_yield quotation before such a cell executes.

Numerator (pre-defined): numerator_gross := verified baseline_work
avoided per consuming task (stream-counted caller actions), EXCLUDING
recovery; net saving := numerator_gross − (amortized maintenance +
recovery term); no quantity counted on both sides. Denominator recovery
term: repair_cost ≥ 1 caller action + 1 load — a LOWER bound anchored on
the single observed C2 datapoint (upper bound unmeasured); stale-rate
sensitivity {0.05, 0.2} are scenario parameters ONLY, never gate inputs;
a second stale datapoint supersedes them. Amortization basis: maintenance
recurs per COMMITTED CYCLE at the observed R0-2 rate (7 records / 6
executed tasks), claiming nothing beyond it. break_even outputs are
monotone TABLES over hypothetical avoided-work x ∈ {1..5} caller-action
units with all denominator components listed — never a headline number.

## 4. Priority 4 — PLAN.V0 MESSAGE-CODE CONFORMANCE FIXTURE

Deliverable: machine-readable fixture `runtime/schemas/
plan.v0.conformance.json` + pure-stdlib validator
`runtime.plan_conformance` implementing: decision/segment consistency;
gap-reason↔abstain-code mapping; known hint.message_codes with declared
params (expected_host is the ONLY actionable param); unknown codes =
conformance ERROR for producers and UNACTIONABLE for consumers; blinding
rule encoded; valid + invalid example plans. Cross-check test: every code
in the FROZEN doc `PLAN_V0_MESSAGE_CODES.md` appears in the fixture and
vice versa. Resolver emissions must conform (RESOLVED, ABSTAIN-failed,
ABSTAIN-no-capsule shapes tested). Wording ceiling: this ENABLES
alternate-caller conformance; it does NOT prove portability.

## 5. Priority 5 — binding constraints folded in

* **W-C2-2**: satisfied by §3.2 construction (rule-based join, two
  evidence classes named, context_signature relocation, append-only v2,
  v1 untouched).
* **W-C2-5**: analyze() regression pin shipped WITH this harness change —
  golden DEEP-equality test of analyze() output (gates + margins + counts
  + empty derivation_errors) against the ACCEPTED R0-2 stream under the
  labeled ADDENDUM wiring; the ORIGINAL live analysis (three FALSE
  booleans) preserved and asserted as a NEGATIVE fixture so history
  cannot be silently repaired; read-only byte-identity proof over
  accepted artifacts; spider-row-count truncation guard (224).
* **W-C2-4**: commits are path-scoped lane writes only; no edits to other
  lanes' files; `baseline.py`, `derive.py`, `gates.py`, `pilot2.py`
  remain byte-identical (additive modules only).

## 6. Priority 6 — RETRIEVAL NEGATIVE CONTROLS

Trigger met: ≥3 capsules exist across parent+wb registries. Sets FROZEN
here (module constants; authored pre-outcome):

MUST_ABSTAIN (7 goals; ANY retrieval at adopted tau=0.30/min_match=2 in
parent, wb, OR union registry is leakage feeding the invalid-hit-rate
dimension): "convert celsius to fahrenheit quickly"; "book a flight to
lisbon next spring"; "translate this document to german"; "fix the broken
bicycle chain"; "play jazz music in the evening"; "water the office
plants on monday"; "summarize this quarterly sales report".

NEAR_MISS (4 goals with declared must-not-match family `login`;
cross-matches are DISCLOSED false-positive risk of the vendored prefix
channels — they never silently pass and never retune constants alone):
book-search/shopping intents ("search for books about dragons on the
catalogue site"; "find cheap horror novels in the store"; "filter the
product list by price range"; "open the shopping basket checkout page").

Mechanics: REAL registry read path (Registry.all_latest + rank_capsules
at adopted constants) over parent, wb, and union registries. Outcomes
recorded AFTER this commit in `results/runtime/probes/
negative_controls_r11.json`.

## 7. Analysis plan / what would change our mind

Primary analysis = mechanical gate evaluation (§1.4, §2.3). Branch
outcomes feed R1 succession per directive: B-KILLED ⇒ honest scoped
negative with offline bound durable; B-SURVIVES ⇒ R1-2 multi-task
replication vs THIS comparator (≥3 tasks × ≥3 samples, frozen list);
B-NO-SURVIVOR ⇒ refusal branch records the full rank table as the bound.
Successor hypothesis (recorded, NOT acted on): if route-level inheritance
value collapses to the affordance/href synonym gap, effect-level
(witness-level) addressing becomes the materially-different successor
candidate.

## 8. Wording ceilings (bound on ALL reports of this cycle)

* B-KILLED: "On the strongest frozen scripted comparator, the near-repeat
  compression OBSERVATION does not survive: … , 2 paired passes, single
  task/site family — observation-strength scoped negative."
* B-SURVIVES: "OBSERVATION survives its strongest preregistered scripted
  comparator: … margin ≥ M=2 per pass, zero novel decisions; magnitude
  unquoted; ratios as numbers only; multi-task replication and
  ≥3-sample statistics owed." Never unscoped "inheritance beats
  exploration"; never "strictly wins".
* B-NO-SURVIVOR: "No memory-free policy in the frozen family places the
  login anchor within four ranked picks on both committed entry
  snapshots; this necessary-condition bound is the cycle's durable
  negative knowledge; live arm refused per prereg; no live-behavior
  claim made."
* All branches: no reuse_yield; wall-clock advisory; model independence
  UNFALSIFIABLE (single scripted caller, zero provider calls); economics
  worded as denominator measurement only.

## 9. Refusals honored this cycle

No second caller implementation (transfer trigger ungated); no MCP/SDK/
wire freeze; no Pareto engine; no TTL/confidence-decay machinery; no
delta-repair executor; no internal fallback agent; no new cost_event
fields or enum values; no live arm without an offline-surviving policy;
no reuse_yield quotation; no registry infrastructure beyond hashed
directories; no schema mutation (v0 frozen; /v1 candidates logged only);
no edits to audited lane artifacts (baseline/derive/gates/pilot2 byte-
identical); no merging of R1-2 into this cycle.
