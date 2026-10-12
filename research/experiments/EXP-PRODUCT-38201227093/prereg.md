# Preregistration — EXP-PRODUCT-38201227093

- Lane: `product`
- Claim target (binding Director mandate): `C-PARAM-INHERIT`
- Dependency claims: `C-MEAS-VALID`, `C-SEMANTIC-RESOLVE`
- `design_contract_version`: 2
- Status: **FROZEN** (DESIGN). Outcome-bearing execution is EXECUTE's job; no confirmatory
  measurement was taken during DESIGN.
- Immutable request: `research/experiments/EXP-PRODUCT-38201227093/request.json`
  (base_sha `a39bdaab694fe400f275e3e8254fffebf6116186`, chain_depth `0`,
  `design_contract_version` 2).
- Spec: `research/experiments/EXP-PRODUCT-38201227093/spec.json`.

## 1. Scope, mandate, inherited state

The Global Research Director mandate **CONTINUE/REOPEN**s `C-PARAM-INHERIT`
(cycle `38200665974`, action CONTINUE, claim REOPEN, parent_handoff_disposition `USE`,
reason `global-director-CONTINUE`). The parent handoff (`EXP-PRODUCT-38197856050`) is
*continuity evidence only*. This experiment is the exact mandate licensed by
`request.json#director_mandate.allocation`: test whether a **SHIPPED-CANDIDATE,
NOT-purely-data-driven applicability guard** — an ingested declared grammar, or a pre-bind
verification/refusal step that detects an observationally-ambiguous pinned shared run and
refuses — can hold `M-FALSE-ACCEPT-COUNT==0` AND `M-HTTP-ON-OUT==0` AND
`M-REFUSAL-EXECUTED-COUNT==0` while raising SAFE coverage on the byte-identical shipped
carrier, on the four frozen families INCLUDING pinned-subrange FAM-D and on at least one
declared grammar whose shared run is NOT observably pinned, reporting safe+complete versus
safe+incomplete per family. Exclusions (binding): do NOT re-run the parent support-widening
certificate; do NOT re-run readiness `EXP-PRODUCT-38186502935`; do NOT substitute the carrier;
do NOT re-run the excluded mandatory-discovery deterministic REST certificate; do NOT fund the
four-arm `C-LLM-INHERIT` benchmark.

### 1.1 Inherited state (preserved verbatim in category, not re-litigated)

**Established (accepted):**
- The shipped carrier (git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256
  `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`, == `src/spider/kernel.py`)
  parameterizes a repeated item request into a support and re-binds it via
  `distill_parameterized` → `resolve`/`verify`; default `min_confidence` 0.8.
- `EXP-PRODUCT-38197856050` (accepted bounded negative, audit PASS): the frozen
  data-driven widening rule (`widen_support`) over-accepted FAM-D (`region-010..region-999`;
  `M-T-WIDENED-FALSE-ACCEPT-COUNT=9`, HTTP-on-OUT=9) and is **NOT unconditionally safe**;
  family disposition on the parent 4-family bank: FAM-A/B safe+complete, FAM-C safe+incomplete
  (width 2 vs declared 1..4), FAM-D safe+incomplete at shipped / unsafe widened; the
  declared-grammar comparator B-DECLARED-FULL achieved FA=0 AND coverage 1.0, proving a
  safe+complete support exists.
- `B-LITERAL-KERNEL` pre-promotion blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` (sha256
  `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`) lacks
  `distill_parameterized`.
- Claim status: `C-PARAM-INHERIT` EXPERIMENTAL, `C-SEMANTIC-RESOLVE` HYPOTHESIS. This packet
  changes neither in ANY branch.

**Rejected (do not re-run, do not assume true):**
- The four-arm `C-LLM-INHERIT` benchmark was NOT funded/run; no LLM-inheritance result exists.
- The parent's data-driven widening rule as a shipped mechanism was rejected
  (FALSIFIES/WIDENING_UNSAFE on FAM-D).

**Unknown (this experiment's question):**
- Whether a NOT-purely-data-driven applicability guard (ingested declared grammar, or purely
  observational pre-bind ambiguity refusal) holds ZERO false accepts and raises SAFE coverage
  toward 1.0 on the four frozen families INCLUDING FAM-D and on declared grammars whose shared
  run is NOT observably pinned.
- Whether the purely observational refusal generalizes to a non-saturating alpha shared run
  (`case-z[a-z]{2}`), i.e., whether FAM-D's failure was a one-class artifact or a general
  identifiability limit.

**do_not_assume (parent handoff + mandate):** (a) do not re-run the support-widening
certificate / readiness / excluded REST certificate; (b) do not substitute a different carrier;
(c) do not self-dispatch or fund the four-arm `C-LLM-INHERIT` benchmark (dependency-gated on
Runtime B2 and Intel B3); (d) do not treat the parent's FAM-D-only negative as proof that all
observational refusal is safe on non-digit shared runs — that is exactly what is probed here
via FAM-F/FAM-G.

### 1.2 Non-duplication

`codex/legacy_brief.json` (accepted evidence): `P2-REPLAY-COST` (sha
`9687ff787f2d74460bb7006826008852f5b4416b`) warns against pricing replay as real-agent
economics; `P2-BLIND-COMPOSITION` (sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`) warns that
blind-composition results are inflated by keyword/oracle dependence. Neither tests an
applicability/refusal guard under a zero-false-accept contract on the parameterized carrier,
and the immediately preceding R2 packet already bounded the pure data-driven widening rule, so
re-running that rule is excluded: this is a materially different mechanism (non-purely-data-driven
guard), not a duplicate. The declared-grammar arm is retained as the strong comparator
(mandate rationale: "The declared-full arm in the frozen design gives a non-trivial comparator
that proves safe+complete is achievable").

## 2. Question, hypotheses, falsifier

**Question.** On the byte-identical shipped carrier, can a SHIPPED-CANDIDATE, not-purely-data-driven
applicability guard — (A) an **ingested declared grammar** with a training-consistency gate and
shipped fallback (`T-DECLARED-GUARD`), or (B) a purely **observational pre-bind refusal** of an
observationally-ambiguous widened support (`T-AMBIGUITY-GUARD`) — hold ZERO false accepts, ZERO
out-of-grammar HTTP executions and ZERO refusal-semantics violations while raising SAFE coverage,
per family (a) on the four frozen families INCLUDING pinned-subrange FAM-D where the pure
data-driven rule over-accepted, and (b) on declared grammars whose shared run is NOT observably
pinned (FAM-F `case-z[a-z]{2}` non-saturating alpha shared run; FAM-G `token-ab[a-z]` saturating
alpha remainder)?

**H1 (primary, constructive).** `T-DECLARED-GUARD` (ingest declared grammar; adopt iff every
training value fullmatches it, else fall back to the shipped support) attains
`M-DECLARED-GUARD-FALSE-ACCEPT-COUNT == 0`, `M-DECLARED-GUARD-HTTP-ON-OUT == 0`,
`M-DECLARED-GUARD-REFUSAL-EXECUTED-COUNT == 0` and `M-DECLARED-GUARD-COVERAGE == 1.0` on the
extended bank (safe+complete per family, including FAM-D and the non-pinned FAM-F/FAM-G).

**H2 (secondary, discriminating).** `T-AMBIGUITY-GUARD` — the purely observational alternative
that refuses to widen only when the observed terminal remainder saturates its full character
class — also holds zero false accepts on the extended bank. This is the non-tautological,
decision-relevant claim: if H2 fails on FAM-F (non-saturating alpha remainder absorbed into the
widened prefix), the observational route is a general identifiability limit, not a FAM-D artifact,
and the declared-grammar route becomes mandatory.

**H0 (null).** No guard (declared or observational) can hold zero false accepts while raising
coverage on the extended bank; equivalently the shipped conservative supports are the ceiling.

**Falsifier (decisive, primary).** Any false accept, out-of-grammar HTTP or executed refusal
under `T-DECLARED-GUARD` → `FALSIFIES` (the constructive route fails). The FALSIFIES branch of
the decision function is concretely exercised by the boundary control `BP-DECL-OVERWIDE` (an
unsound over-wide declaration passes the training-consistency gate and yields false accepts;
DESIGN point-prediction FA=201), and the MIXED branch by `PC-DECL-UNDER` (a too-narrow
declaration is refused by the gate → shipped fallback → safe but incomplete; predicted FA=0,
coverage<1). **Secondary disposition (mandatory co-report):** `T-AMBIGUITY-GUARD` disposition
`UNSAFE` iff its false-accept/HTTP-on-OUT/refusal-execution counts are >0;
`SAFE_AND_COMPLETE` iff 0 and coverage==1.0; else `SAFE_INCOMPLETE`. Frozen DESIGN
point-prediction: declared guard SAFE_AND_COMPLETE; observational guard **UNSAFE** on FAM-F
(4 false accepts: `FF-OG-ALPHA-ALL`=`case-abc`, `FF-OG-WRONGRANGE00..02`=`case-aab/case-bcd/
case-xyz`), giving overall decision `DECLARED_GUARD_SAFE_AND_COMPLETE__OBSERVATIONAL_GUARD_UNSAFE`.

`MEASUREMENT_INVALID`/`BLOCKED` (NEVER falsifies): V8 freeze-binding mismatch; shipping kernel
sha != `718efa6a...` (substituted carrier); induced shipped support drift; M-REGRESSION<3/3;
PC-DETERMINISM-REPEAT mismatch; PC-EXACT-REPLAY <61/61; B-LITERAL-KERNEL unexpectedly exposing
`distill_parameterized`; B-SHIPPED FA>0 or B-DECLARED-FULL not safe+complete (bank/label-rule
inconsistency); a failing sensitivity/null gate (PC-UNSAFE-COARSE FA==0 OR PC-OVERWIDE-OPEN
FA==0 OR PC-DECL-UNDER adopted any OR NC-REJECT-ALL accept!=0/HTTP!=0); missing git objects or
oracle/fixture failure.

## 3. Frozen bank and label rule

The FROZEN RUNNER (Section 14) enumerates a single frozen bank of n=524 unique items in SEVEN
families. Families A-D are byte-identical reproductions of the parent bank families
(EXP-PRODUCT-38197856050); E/F/G are new declared families. Each family declares an inner
grammar; the declared inner pattern is the oracle's contract and the OUT label is assigned purely
by whether the concrete value fullmatches it.

| family | resource path | train values | declared inner pattern |
|---|---|---|---|
| `FAM-A` | `/api/items/item-<id>` | `item-001`..`item-005` | `^item\-[0-9]{3}$` |
| `FAM-B` | `/api/accounts/acct-<id>` | `acct-0001`..`acct-0005` | `^acct\-[0-9]{4}$` |
| `FAM-C` | `/api/docs/doc-<id>` | `doc-01`..`doc-05` | `^doc\-[0-9]{1,4}$` |
| `FAM-D` | `/api/regions/region-<id>` | `region-000`..`region-009` | `^region\-00[0-9]$` (pinned subrange) |
| `FAM-E` | `/api/invoices/invoice-<id>` | `invoice-0001`..`invoice-0005` | `^invoice\-[0-9]{4}$` |
| `FAM-F` | `/api/cases/case-<id>` | `case-zab`..`case-zij` | `^case\-z[a-z]{2}$` (non-digit shared run, NOT observably pinned) |
| `FAM-G` | `/api/tokens/token-<id>` | `token-aba`..`token-abz` (26) | `^token\-ab[a-z]$` (saturating alpha remainder) |

Expected bank composition (frozen by the runner, re-derived in DESIGN probes): n=524, IN=120,
OUT=404; per family A 16/56, B 18/55, C 19/53, D 10/65, E 16/55, F 12/61, G 29/59. Three
payload rows are legitimately IN because their mutated value still matches the declared grammar
(`FB-OG-LEN-TOO-LONG1`=`acct-0000`, `FC-OG-LEN-TOO-SHORT2`=`doc-00`,
`FC-OG-LEN-TOO-LONG1`=`doc-0000`, plus `FF-OG-PCT`=`case-zab`, `FG-OG-ALPHA-ALL`=`token-abc`,
`FG-OG-PCT`=`token-aba`), demonstrating the label rule is purely value-vs-declared-grammar.

Labelling is objective and outcome-independent: an item is IN iff its concrete id fullmatches the
family's declared inner pattern AND intent == family intent AND context ==
`{resource_type:<resource>, authenticated:true}` AND params == `{<resource>: value}`; else OUT.
HTTP-on-OUT is defined as the runner issuing a real HTTP request whose path the oracle did not
declare success for.

## 4. Arms and controls

**Treatments (SHIPPED-CANDIDATE guards, NOT shipped bytes; support descriptors are injected
in-run only).**
- `T-DECLARED-GUARD` (PRIMARY) — ingested declared grammar adopted iff every training value
  fullmatches it; else fall back to the shipped support (training-consistency gate, literally the
  `declared_guard_support` rule, Section 5). Non-purely-data-driven: the grammar is external
  knowledge, the gate is a verification step.
- `T-AMBIGUITY-GUARD` (SECONDARY, discriminating) — no external grammar; purely observational
  pre-bind refusal: widen only when the widening is NOT observationally ambiguous; refuse
  (keep shipped) when the absorbed run shares the remainder's class AND the terminal observed
  remainder saturates that full class.

**Baselines (strong).**
- `B-SHIPPED` — the shipped carrier's own induced supports, unchanged (over-conservative; safe).
- `B-DECLARED-FULL` — oracle-declared full grammar per family, injected raw WITHOUT the gate.
  Ceiling: must be safe+complete (`M-COVERAGE=1.0`, `M-FALSE-ACCEPT-COUNT=0`); any failure is a
  bank/label-rule inconsistency → MEASUREMENT_INVALID. The gate makes `T-DECLARED-GUARD`
  formally distinct; on the main bank the gate accepts all SOUND declarations so their supports
  coincide BY DESIGN (the target result), and the divergence is exercised by the gate controls.
- `B-DATA-WIDENED` — the frozen parent data-driven widening rule (`widen_support`, parent
  certificate) on the extended bank: predicted unsafe on FAM-D (9) + FAM-F (4) + FAM-G (5).
- `B-LITERAL-KERNEL` — literal pre-promotion kernel blob (hermetic temp package, same
  models/registry/init); must NOT expose `distill_parameterized`.

**Positive controls (must be *sensitive* / must fire).**
- `PC-UNSAFE-COARSE` (`__COARSE__`, the carrier's own fail-open sentinel) — must accept >=1 OUT
  (DESIGN point-prediction FA=271).
- `PC-OVERWIDE-OPEN` (`^<id_prefix>\-[0-9a-zA-Z]+$`) — must accept >=1 OUT (predicted 91).
- `PC-DECL-UNDER` — declared guard fed a too-narrow wrong declaration (literal exact-match of
  `train[0]`): the gate must REFUSE adoption (predicted all-false) and fall back to the shipped
  support (FA=0, coverage<1). Sensitivity control for the gate itself.
- `BP-DECL-OVERWIDE` — boundary probe: declared guard fed a too-wide wrong declaration
  (`^<id_prefix>.*$`): consistent with training, so the gate ADOPTS it (predicted all-true) and
  the arm inherits its own false accepts (predicted FA=201). Declares declaration soundness
  EXTERNAL to the gate.
- `PC-DETERMINISM-REPEAT` — full arm metrics re-run; must be byte-identical.

**Null control.** `NC-REJECT-ALL` — empty registry; must accept nothing and issue no HTTP.

**Validity anchor.** `PC-EXACT-REPLAY` — all 61 training ids re-resolve EXECUTABLE under the
induced mechanisms; must PASS before any outcome is interpreted.

## 5. Frozen guard rules

- `declared_guard_support(values, decl, shipped) -> (support, adopted)`: adopt `decl` iff
  `values` non-empty and every observed training value `re.fullmatch(decl, v)`; otherwise return
  `(shipped, False)`. This is the PRIMARY mechanism (ingest + consistency gate + shipped
  fallback).
- `ambiguity_guard_support(values, shipped, widened) -> (support, refused)`: compute the common
  prefix and the observed varying remainder's minimal character class; **refuse** (keep
  `shipped`) iff the trailing common-prefix run shares that class AND the terminal observed
  remainder position saturates the FULL class (`CLASS_FULL[klass]`); else adopt the widened
  support. Purely observational; never consults a declaration.
- `widen_support(values)`: the frozen parent data-driven widening rule (comparator only).
- `_shipped_infer(values)`: verbatim copy of the shipped `_infer_support` (baseline/liveness).
- V12-equivalence: `mechanism_id` is a hash of `{intent, template, slots}` and is
  support-independent, so overwriting `verification_rule["parameter_supports"]` in-run is
  equivalent to re-running `distill_parameterized` with `_infer_support` replaced by the guard
  rule, while leaving the shipped bytes untouched.

## 6. Oracle

The runner starts a stdlib `ThreadingHTTPServer` bound to `127.0.0.1:0` (ephemeral port) with a
request counter. For each family it declares `VALID_PATH_RES[fam]`
(`^/api/<resource>s/<declared inner>$`) mapping to HTTP 200 returning
`{"type":<resource>,"id":<id>,"data":"res:"+<id>}`; any other path is 404. Every HTTP value is a
real request; a non-success response for an OUT item counts as HTTP-on-OUT. No network egress
beyond loopback.

## 7. Metrics (stable ids)

Primary (T-DECLARED-GUARD):
- `M-DECLARED-GUARD-FALSE-ACCEPT-COUNT` (primary decision metric)
- `M-DECLARED-GUARD-HTTP-ON-OUT`, `M-DECLARED-GUARD-REFUSAL-EXECUTED-COUNT`
- `M-DECLARED-GUARD-FALSE-REJECT-COUNT`, `M-DECLARED-GUARD-COVERAGE` (+BY-FAMILY)
- `M-DECLARED-GUARD-SILENT-FALSE-ACCEPT-COUNT`, `M-DECLARED-GUARD-ADOPTED-BY-FAMILY`

Secondary / comparison:
- `M-OBSERVATIONAL-GUARD-FALSE-ACCEPT-COUNT` / `-HTTP-ON-OUT` / `-COVERAGE` /
  `-FALSE-REJECT-COUNT`, `M-OBSERVATIONAL-GUARD-REFUSED-FAMILIES`,
  `M-OBSERVATIONAL-GUARD-DISPOSITION` ∈ {SAFE_AND_COMPLETE, SAFE_INCOMPLETE, UNSAFE}
- `M-B-DATA-WIDENED-FALSE-ACCEPT-COUNT` (parent comparator), `M-B-SHIPPED-COVERAGE` (0.6750 on
  the extended bank), `M-COVERAGE-DELTA`
- `M-GUARD-SUPPORT-BY-FAMILY` (declared/ambiguity), `M-SHIPPED-SUPPORT-BY-FAMILY`,
  `M-B-DECLARED-FULL-FALSE-ACCEPT-COUNT` / `-COVERAGE`
- `M-CONTROL-PC-COARSE-*`, `M-CONTROL-PC-OVERWIDE-*`, `M-CONTROL-PC-DECL-UNDER-*`,
  `M-CONTROL-NC-REJECT-ALL-*`, `M-BOUNDARY-DECL-OVERWIDE-*`
- `M-REFUSAL-SEMANTICS-VIOLATIONS` (must be 0 structurally)

Identity/validity: `M-BANK` (n=524, IN=120, OUT=404, unique bids), `M-IDENTITY`,
`M-SUPPORT-IDENTITY` (induced shipped supports == 7 canonical shipped regexes; widened/ambiguity
supports == DESIGN constants), `M-REGRESSION` (tests/test_kernel.py 3/3 on the shipping path),
`PC-EXACT-REPLAY` (61/61), `M-DETERMINISM-REPEAT`, `B-LITERAL-KERNEL` ablation.

## 8. Decision rule

Precedence: `MEASUREMENT_INVALID` > `FALSIFIES` > (`SUPPORTS` | `MIXED`).

- **MEASUREMENT_INVALID** if any validity gate fails (V8, M-IDENTITY, M-SUPPORT-IDENTITY,
  M-REGRESSION, PC-DETERMINISM-REPEAT, PC-EXACT-REPLAY, B-LITERAL-KERNEL, B-SHIPPED,
  B-DECLARED-FULL) or any sensitivity gate fails (PC-UNSAFE-COARSE FA>=1, PC-OVERWIDE-OPEN
  FA>=1, PC-DECL-UNDER all-refused + FA==0, NC-REJECT-ALL accept==0/http==0), or the bank
  cannot be instantiated. (Validity/infrastructure failure ≠ scientific negative.)
- **FALSIFIES** (decision `DECLARED_GUARD_UNSAFE`) if `M-DECLARED-GUARD-FALSE-ACCEPT-COUNT>0`
  OR `-HTTP-ON-OUT>0` OR `-REFUSAL-EXECUTED-COUNT>0`. Unreachable with SOUND declarations on
  this bank; the decision function's FALSIFIES branch is exercised by BP-DECL-OVERWIDE
  (predicted FA=201 on the same function with an unsound declaration).
- **SUPPORTS** (decision `DECLARED_GUARD_SAFE_AND_COMPLETE__OBSERVATIONAL_GUARD_<DISP>`) if
  T-DECLARED-GUARD is safe AND `M-DECLARED-GUARD-COVERAGE==1.0`; `<DISP>` is the mandatory
  co-report of the secondary observational guard. **DESIGN prediction: SUPPORTS with
  `OBSERVATIONAL_GUARD_UNSAFE`** (FAM-F 4 false accepts).
- **MIXED** (decision `DECLARED_GUARD_SAFE_BUT_INCOMPLETE__OBSERVATIONAL_GUARD_<DISP>`) if safe
  but coverage < 1.0 (e.g. any family where the gate refuses an inconsistent declaration and
  falls back — the PC-DECL-UNDER branch).

**Claim-status semantics (no self-promotion):** `C-PARAM-INHERIT` stays `EXPERIMENTAL` and
`C-SEMANTIC-RESOLVE` stays `HYPOTHESIS` in ALL branches. This packet produces evidence only; it
does not advance, promote or ship any claim. Product impact is bounded to the choice of
applicability-guard mechanism.

## 9. Reachability and DESIGN probes (non-outcome only)

Performed during DESIGN; none outcome-bearing (no treatment `resolve()` over the frozen bank was
run in DESIGN; the real-carrier induction path was probed for liveness only):

- **D1 arithmetic/reachability:** bank constructible (n=524, 120 IN, 404 OUT, unique bids; per
  family A 16/56, B 18/55, C 19/53, D 10/65, E 16/55, F 12/61, G 29/59); each family has
  train>=5 and OUT items; value-level arm arithmetic (below) leaves no branch empty.
- **D2 support identity:** `_shipped_infer` on the frozen training reproduces the 7 expected
  shipped regexes; `widen_support` reproduces the 7 widened regexes; `ambiguity_guard_support`
  reproduces the 7 expected ambiguity regexes (refused: D, G; widened: A,B,C,E,F);
  `declared_guard_support` adopts all sound declarations.
- **D3 treatment liveness:** REAL-CARRIER induction probe (non-outcome prerequisite probe) for
  all 7 families: `distill_parameterized` yields a single parameter slot
  (`item/account/doc/region/invoice/case/token`), confidence 0.9 (>=0.8 gate), support ==
  expected shipped regex. All 61 training ids fullmatch shipped/widened/declared/ambiguity
  supports, so all arms are live on the training ids (PC-EXACT-REPLAY 61/61 expected).
- **D4 control sensitivity (value-level):** PC-UNSAFE-COARSE FA=271 (using the carrier's own
  `_support_accepts` semantics for `__COARSE__`: non-empty, no whitespace, no '/');
  PC-OVERWIDE-OPEN FA=91; PC-DECL-UNDER adopted=={all False}, FA=0 (shipped fallback);
  NC-REJECT-ALL accept==0/http==0; BP-DECL-OVERWIDE adopted=={all True}, FA=201.
- **D5 treatment/comparator identity:** the ONLY in-run mutation across arms is
  `verification_rule["parameter_supports"]` (V12: `mechanism_id` support-independent); the
  declared guard and the raw ceiling differ only in the consistency gate, and the gate's
  behavior is isolated by PC-DECL-UNDER / BP-DECL-OVERWIDE; T-AMBIGUITY-GUARD is a distinct
  rule (refuses D,G; widens A,B,C,E,F) differing from B-DATA-WIDENED on D/G and from B-SHIPPED
  on A/B/C/E.
- **D6 satisfiability:** the predicted SUPPORTS branch is concretely reachable; the secondary
  UNSAFE disposition is concretely reachable (FAM-F: `case-aab`,`case-bcd`,`case-xyz`,
  `case-abc` are OUT under `^case\-z[a-z]{2}$` but accepted by the widened `^case\-[a-z]{3}$`);
  the primary FALSIFIES branch is exercised by BP-DECL-OVERWIDE on the same decision function;
  MIXED by PC-DECL-UNDER. No arithmetic impossibility.

Frozen DESIGN value-level point-predictions (pure predicates, no carrier resolve() over the
bank): B-SHIPPED FA=0 cov=81/120=0.6750 (FR 39: A8 B10 C13 D0 E8 F0 G0);
T-DECLARED-GUARD FA=0 cov=1.0 adopted=all;
T-AMBIGUITY-GUARD FA=4 cov=110/120=0.9167 (FR 10: FAM-C) disposition=UNSAFE,
refused={D,G}; B-DATA-WIDENED FA=18 (D9+F4+G5) cov=0.9167;
B-DECLARED-FULL FA=0 cov=1.0; PC-UNSAFE-COARSE FA=271; PC-OVERWIDE-OPEN FA=91;
BP-DECL-OVERWIDE FA=201; NC-REJECT-ALL 0/0.

## 10. Freeze eligibility (v2, six checks)

| check | status | basis |
|---|---|---|
| `decision_rule_reachability` | PASS | D1/D6: SUPPORTS predicted and reachable; MIXED reachable via PC-DECL-UNDER branch of the same decision function; FALSIFIES branch exercised by BP-DECL-OVERWIDE; secondary UNSAFE disposition concretely reachable (FAM-F). No empty/degenerate branch. |
| `measurement_prerequisites` | PASS | python3.12.15 + stdlib; both git blobs present (b15ed848..., cfec9866...); shipping kernel sha256 == 718efa6a... == carrier; six freeze artifacts exist with recorded sha256; public API imports cleanly; default min_confidence 0.8; real-carrier induction probe succeeded for all 7 families (confidence 0.9, expected supports); runner py_compile OK; tests 3/3 with src on sys.path. |
| `baseline_identifiability` | PASS | All arms are the SAME seven induced mechanism objects with ONLY `parameter_supports` rewritten (V12); B-SHIPPED keeps induced supports; B-DECLARED-FULL injects raw declaration (no gate); T-DECLARED-GUARD = gate + shipped fallback (coinciding with the ceiling on SOUND declarations BY DESIGN, separated by the gate controls); T-AMBIGUITY-GUARD = observational refusal rule (distinct supports on D,G); B-DATA-WIDENED = parent widening; B-LITERAL-KERNEL = different frozen blob. Carrier pinned by sha256 + V8 artifact hashes. |
| `control_sensitivity` | PASS | D4: PC-UNSAFE-COARSE (FA>=1, predicted 271), PC-OVERWIDE-OPEN (91), PC-DECL-UNDER (gate refuses; FA=0), BP-DECL-OVERWIDE (gate cannot detect unsound declaration; FA=201), NC-REJECT-ALL (0/0), PC-EXACT-REPLAY (61/61), PC-DETERMINISM-REPEAT, M-REGRESSION (3/3). A detector that never fires yields no meaningful zero. |
| `treatment_liveness` | PASS | D3: real-carrier induction probe — 7/7 families induce a single-slot mechanism at confidence 0.9 >= 0.8; all 61 training ids fullmatch every arm's support (PC-EXACT-REPLAY 61/61 expected); guards are pure support-rewrites, so liveness is inherited from the shipped path (EXP-PRODUCT-38186502935 audit PASS). |
| `freeze_artifacts_bound` | PASS | six immutable files listed in spec.freeze_artifacts (all existing, hashes recorded); the bank, oracle, label rule and both guard rules are fully in-process inside the FROZEN RUNNER (bound via prereg.md hash); no unbound mutable local code/data/task-bank/fixture dependency remains. |

## 11. Binding model

- `EXPECTED_MIN_CONFIDENCE = 0.8` (kernel default; all 7 families induce 0.9).
- V8 freeze binding (checked by EXECUTE):
  1. `sha256(prereg.md) == freeze.json.hashes["prereg.md"]`;
  2. `norm(prereg.md source) == norm(FROZEN RUNNER block)` where
     `norm(s) = s.replace("\r\n", "\n").rstrip()`;
  3. `sha256(file) == freeze.json.artifact_hashes[file]` for every listed artifact.
- V12 equivalence (justifies read-only overlay): `mechanism_id` is support-independent, so
  overriding `verification_rule.parameter_supports` is equivalent to re-running
  `distill_parameterized` with `_infer_support` replaced by the guard rule.
- Probe mode: `EXP_PROBE_MODE=1` records `UNBOUND-RUN` when `freeze.json` is absent;
  `EXP_TARGET_ROOT` sets the repo root.
- EXECUTE materializes `harness/run_guard.py` from the FROZEN RUNNER block below (byte-for-byte
  after `norm`).

## 12. Canonical hashes

| artifact | sha256 |
|---|---|
| `pyproject.toml` | `5f03fb5914f388c19973831287cce6773c7364e1bea856a595cd7247d3115b83` |
| `src/spider/__init__.py` | `3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77` |
| `src/spider/models.py` | `338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78` |
| `src/spider/registry.py` | `51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c` |
| `src/spider/kernel.py` | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` |
| `tests/test_kernel.py` | `ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6` |

FROZEN RUNNER block (normalized) sha256:
`f7ebfe4c319c0a8d1d8153fb1408384968b9675bfae2f2da93b16cce032019ce` (un-normalized file sha256 `f46b97c99bae20178af06a99218f8a5a439c06ca2d16e0c5d4168e4cd99bf5db`). These are DESIGN
references; the binding hashes are established by `freeze.json` at freeze time.

## 13. Cost and scope limits

- Stdlib only; loopback HTTP; no LLM calls; no network egress. `model_calls==0`,
  `model_tokens==0` by construction.
- EXECUTE scope: prefix `research/experiments/EXP-PRODUCT-38201227093` plus lane
  `allowed_code_roots`. DESIGN writes only `spec.json` and `prereg.md`.
- Estimated cost: small (single deterministic pass; induction GETs 61 + arm GETs
  ~T-DECLARED-GUARD 120 + T-AMBIGUITY-GUARD 110 + B-DATA-WIDENED 110 + B-SHIPPED 81 +
  B-DECLARED-FULL 120 + PC-COARSE ~120 + PC-OVERWIDE ~120 + PC-DECL-UNDER 81 +
  BP-DECL-OVERWIDE ~120; run twice for determinism).

## 14. FROZEN RUNNER

Materialization source for `harness/run_guard.py`. The block below is verbatim; EXECUTE must
reproduce it exactly (V8 binding).
<!-- BEGIN FROZEN RUNNER -->
#!/usr/bin/env python3
"""FROZEN RUNNER for EXP-PRODUCT-38201227093 (embedded verbatim in prereg.md).

Read-only GUARD-AUGMENTED-WIDENING safety/coverage certificate for the
as-installed parameterized carrier (src/spider/kernel.py, git blob b15ed848... /
sha256 718efa6a...).  NEVER writes src/spider/ and never calls a model.

The experiment tests whether a NOT-PURELY-DATA-DRIVEN applicability guard can
admit widened parameter supports while holding zero false accepts / zero
out-of-grammar execution / zero refusal-semantics violations, on an EXTENDED
bank that reproduces the four frozen families of EXP-PRODUCT-38197856050 and adds
three new declared families.

Arms (stable ids):
  T-DECLARED-GUARD      PRIMARY treatment: ingested declared applicability
                        grammar adopted only after a training-consistency check;
                        fallback to the shipped support when the declaration is
                        inconsistent (non-purely-data-driven)
  T-AMBIGUITY-GUARD     SECONDARY treatment: purely observational pre-bind
                        refusal of an ambiguous (saturated-remainder) widening
  B-DATA-WIDENED        comparator: the frozen parent data-driven widening rule
  B-SHIPPED             the unmodified induced supports (shipped baseline)
  B-DECLARED-FULL       support replaced by the oracle declared grammar (ceiling)
  PC-UNSAFE-COARSE      support replaced by the carrier's own __COARSE__ sentinel
  PC-OVERWIDE-OPEN      support replaced by an open class pattern
  PC-DECL-UNDER         declared guard fed a too-narrow wrong declaration
  BP-DECL-OVERWIDE      declared guard fed a too-wide wrong declaration
  NC-REJECT-ALL         empty registry (null floor)
  B-LITERAL-KERNEL      pre-promotion literal kernel (lacks distill_parameterized)
  PC-EXACT-REPLAY       ALL training ids re-resolve EXECUTABLE
  ORACLE-SERVER         localhost oracle: 200 iff path matches declared grammar

Env overrides (hermetic dry-run only; never change certificate logic):
  EXP_TARGET_ROOT : repo root containing src/spider (default: auto-detected)
  EXP_PROBE_MODE  : "1" records UNBOUND-RUN for V8 when freeze.json is absent
"""
from __future__ import annotations

import copy
import hashlib
import http.server
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

# -- canonical identities (mirrors prereg CANONICAL-HASHES) --
CARRIER_BLOB = "b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796"
CARRIER_SHA256 = "718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72"
LITERAL_BLOB = "cfec98660b0277ccbf295e8a4119e8d81ddccf50"
LITERAL_SHA256 = "46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61"
EXPERIMENT_ID = "EXP-PRODUCT-38201227093"
EXP_DIR = "research/experiments/EXP-PRODUCT-38201227093"
EXPECTED_MIN_CONFIDENCE = 0.8
COARSE = "__COARSE__"

# Declared grammars + frozen training samples.  The four families A-D are
# byte-identical reproductions of EXP-PRODUCT-38197856050's bank families; E/F/G
# are new declared families.  `id_prefix` is the resource stem used by the frozen
# payload classes (as in the parent bank).
FAMILIES = [
    {"fam": "A", "intent": "read_item", "resource": "item", "id_prefix": "item",
     "declared": r"^item\-[0-9]{3}$",
     "train": ["item-001", "item-002", "item-003", "item-004", "item-005"],
     "in_extra": ["item-000", "item-006", "item-007", "item-010", "item-042",
                  "item-099", "item-100", "item-123", "item-256", "item-500", "item-999"],
     "out_wrong_subrange": []},
    {"fam": "B", "intent": "read_account", "resource": "account", "id_prefix": "acct",
     "declared": r"^acct\-[0-9]{4}$",
     "train": ["acct-0001", "acct-0002", "acct-0003", "acct-0004", "acct-0005"],
     "in_extra": ["acct-0006", "acct-0007", "acct-0010", "acct-0042", "acct-0099",
                  "acct-0100", "acct-0123", "acct-0256", "acct-0500", "acct-0999",
                  "acct-1000", "acct-9999"],
     "out_wrong_subrange": []},
    {"fam": "C", "intent": "read_doc", "resource": "doc", "id_prefix": "doc",
     "declared": r"^doc\-[0-9]{1,4}$",
     "train": ["doc-01", "doc-02", "doc-03", "doc-04", "doc-05"],
     "in_extra": ["doc-0", "doc-1", "doc-9", "doc-10", "doc-11", "doc-99",
                  "doc-100", "doc-123", "doc-999", "doc-1000", "doc-9999"],
     "out_wrong_subrange": []},
    {"fam": "D", "intent": "read_region", "resource": "region", "id_prefix": "region",
     "declared": r"^region\-00[0-9]$",
     "train": ["region-000", "region-001", "region-002", "region-003", "region-004",
               "region-005", "region-006", "region-007", "region-008", "region-009"],
     "in_extra": [],
     "out_wrong_subrange": ["region-010", "region-011", "region-042", "region-099",
                            "region-100", "region-123", "region-256", "region-500",
                            "region-999"]},
    {"fam": "E", "intent": "read_invoice", "resource": "invoice", "id_prefix": "invoice",
     "declared": r"^invoice\-[0-9]{4}$",
     "train": ["invoice-0001", "invoice-0002", "invoice-0003", "invoice-0004",
               "invoice-0005"],
     "in_extra": ["invoice-0000", "invoice-0006", "invoice-0042", "invoice-0099",
                  "invoice-0100", "invoice-0500", "invoice-0999", "invoice-1000",
                  "invoice-1234", "invoice-9999"],
     "out_wrong_subrange": []},
    {"fam": "F", "intent": "read_case", "resource": "case", "id_prefix": "case",
     "declared": r"^case\-z[a-z]{2}$",
     "train": ["case-zab", "case-zcd", "case-zef", "case-zgh", "case-zij"],
     "in_extra": ["case-zaa", "case-zmn", "case-zop", "case-zqr", "case-zzy",
                  "case-zzz"],
     "out_wrong_subrange": ["case-aab", "case-bcd", "case-xyz", "case-0ab",
                            "case-za", "case-zz11"]},
    {"fam": "G", "intent": "read_token", "resource": "token", "id_prefix": "token",
     "declared": r"^token\-ab[a-z]$",
     "train": ["token-aba", "token-abb", "token-abc", "token-abd", "token-abe",
               "token-abf", "token-abg", "token-abh", "token-abi", "token-abj",
               "token-abk", "token-abl", "token-abm", "token-abn", "token-abo",
               "token-abp", "token-abq", "token-abr", "token-abs", "token-abt",
               "token-abu", "token-abv", "token-abw", "token-abx", "token-aby",
               "token-abz"],
     "in_extra": ["token-abb"],
     "out_wrong_subrange": ["token-aaa", "token-aac", "token-bbb", "token-xyz",
                            "token-zzz"]},
]
FAM_BY_ID = {f["fam"]: f for f in FAMILIES}
FAM_ORDER = [f["fam"] for f in FAMILIES]

EXPECTED_SHIPPED = {
    "A": r"^item\-00[0-9]{1}$", "B": r"^acct\-000[0-9]{1}$",
    "C": r"^doc\-0[0-9]{1}$", "D": r"^region\-00[0-9]{1}$",
    "E": r"^invoice\-000[0-9]{1}$", "F": r"^case\-z[a-z]{2}$",
    "G": r"^token\-ab[a-z]{1}$",
}
EXPECTED_WIDENED = {
    "A": r"^item\-[0-9]{3}$", "B": r"^acct\-[0-9]{4}$",
    "C": r"^doc\-[0-9]{2}$", "D": r"^region\-[0-9]{3}$",
    "E": r"^invoice\-[0-9]{4}$", "F": r"^case\-[a-z]{3}$",
    "G": r"^token\-[a-z]{3}$",
}
EXPECTED_AMBIGUITY = {
    "A": r"^item\-[0-9]{3}$", "B": r"^acct\-[0-9]{4}$",
    "C": r"^doc\-[0-9]{2}$", "D": r"^region\-00[0-9]{1}$",
    "E": r"^invoice\-[0-9]{4}$", "F": r"^case\-[a-z]{3}$",
    "G": r"^token\-ab[a-z]{1}$",
}
# Main ingested applicability declarations == the family declared grammars.
DECLARED_GRAMMAR = {f["fam"]: f["declared"] for f in FAMILIES}
# Wrong declarations used by the declaration-consistency controls.
DECL_UNDER = {f["fam"]: "^" + re.escape(f["train"][0]) + "$" for f in FAMILIES}
DECL_OVERWIDE = {f["fam"]: "^" + re.escape(f["id_prefix"]) + ".*$" for f in FAMILIES}

CLASS_FULL = {
    "0-9": set("0123456789"),
    "a-z": set("abcdefghijklmnopqrstuvwxyz"),
    "A-Z": set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "a-zA-Z": set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "a-z0-9": set("abcdefghijklmnopqrstuvwxyz0123456789"),
    "a-zA-Z0-9": set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"),
}

PAYLOAD_CLASSES = [
    ("LEN-TOO-SHORT1", lambda p, v: p + "-0"),
    ("LEN-TOO-SHORT2", lambda p, v: p + "-00"),
    ("LEN-TOO-LONG1", lambda p, v: p + "-" + "0" * 4),
    ("LEN-TOO-LONG2", lambda p, v: p + "-" + "0" * 5),
    ("LEN-TOO-LONG3", lambda p, v: p + "-" + "0" * 6),
    ("ALPHA-TAIL", lambda p, v: p + "-00a"),
    ("ALPHA-ALL", lambda p, v: p + "-abc"),
    ("ALPHA-HEAD", lambda p, v: p + "-a00"),
    ("HEX", lambda p, v: p + "-0x1"),
    ("CASE-UP", lambda p, v: p.upper() + "-000"),
    ("CASE-TITLE", lambda p, v: p.capitalize() + "-000"),
    ("SEP-US", lambda p, v: p + "_000"),
    ("SEP-DOT", lambda p, v: p + ".000"),
    ("SEP-COLON", lambda p, v: p + ":000"),
    ("SEP-SLASH", lambda p, v: p + "/000"),
    ("WS-EMPTY", lambda p, v: ""),
    ("WS-SPACE", lambda p, v: " "),
    ("WS-TAB", lambda p, v: "\t"),
    ("WS-NL", lambda p, v: "\n"),
    ("WS-TRAIL", lambda p, v: v + " "),
    ("WS-LEAD", lambda p, v: " " + v),
    ("INJ-SEMI", lambda p, v: v + ";x"),
    ("INJ-SQ", lambda p, v: v + "'"),
    ("INJ-DQ", lambda p, v: v + '"'),
    ("INJ-NUL", lambda p, v: v + "\x00"),
    ("INJ-TRAV", lambda p, v: "../../etc/passwd"),
    ("INJ-ABS", lambda p, v: "/api/" + p + "s/" + v),
    ("INJ-URL", lambda p, v: "http://evil.example/" + v),
    ("INJ-DOTDOT", lambda p, v: v + "/../secret"),
    ("QRY", lambda p, v: v + "?x=1"),
    ("FRAG", lambda p, v: v + "#frag"),
    ("PCT", lambda p, v: v.replace("0", "%30", 1)),
    ("UNI-AR", lambda p, v: p + "-00\u0663"),
    ("UNI-FW", lambda p, v: p + "-00\uff10"),
    ("OTH-USER", lambda p, v: "user-000"),
    ("OTH-ORDER", lambda p, v: "order-000"),
    ("OTH-CAT", lambda p, v: p + "x000"),
    ("BIG-1000", lambda p, v: p + "-" + "0" * 1000),
    ("BIG-64", lambda p, v: p + "-" + "9" * 64),
]
TYPE_PAYLOADS = [None, 0, 0.0, True, False, [], ["X"], {}, {"id": "X"}, b"X"]


def detect_repo_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "pyproject.toml").exists() and (p / "src/spider").exists():
            return p
        p = p.parent
    raise RuntimeError("repo root not found upward from runner")


REPO_ROOT = Path(os.environ.get("EXP_TARGET_ROOT") or str(detect_repo_root()))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_source(spec: str) -> bytes:
    if spec.startswith("git:"):
        out = subprocess.run(["git", "-C", str(REPO_ROOT), "cat-file", "blob", spec[4:]],
                             capture_output=True)
        if out.returncode != 0:
            raise RuntimeError("git blob unavailable: " + out.stderr.decode()[:200])
        return out.stdout
    if spec.startswith("file:"):
        return Path(spec[5:]).read_bytes()
    raise RuntimeError("unknown source spec: " + spec)


# ----------------------------------------------------- frozen support inference
def _char_class(chars):
    digits = set("0123456789")
    lower = set("abcdefghijklmnopqrstuvwxyz")
    upper = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if chars and chars <= digits:
        return "0-9"
    if chars and chars <= lower:
        return "a-z"
    if chars and chars <= upper:
        return "A-Z"
    if chars and chars <= (lower | upper):
        return "a-zA-Z"
    if chars and chars <= (lower | digits):
        return "a-z0-9"
    if chars and chars <= (lower | upper | digits):
        return "a-zA-Z0-9"
    return None


def _common_prefix(values):
    if not values:
        return ""
    prefix = values[0]
    for value in values[1:]:
        limit = min(len(prefix), len(value))
        i = 0
        while i < limit and prefix[i] == value[i]:
            i += 1
        prefix = prefix[:i]
    return prefix


def _shipped_infer(values) -> str:
    """Verbatim copy of src/spider/kernel.py::_infer_support (frozen reference)."""
    values = [str(v) for v in values]
    if not values:
        return COARSE
    prefix = _common_prefix(values)
    remains = [v[len(prefix):] for v in values]
    klass = _char_class(set("".join(remains)))
    if klass is None:
        return COARSE
    lengths = {len(r) for r in remains}
    quantifier = "{%d}" % next(iter(lengths)) if len(lengths) == 1 else "+"
    return "^" + re.escape(prefix) + "[" + klass + "]" + quantifier + "$"


def widen_support(values) -> str:
    """Frozen parent data-driven widening rule (B-DATA-WIDENED comparator).

    Pure function of the observed values; it NEVER consults the declared grammar.
    """
    values = [str(v) for v in values]
    if not values:
        return COARSE
    prefix = _common_prefix(values)
    remains = [v[len(prefix):] for v in values]
    klass = _char_class(set("".join(remains)))
    if klass is None:
        return _shipped_infer(values)
    k = len(prefix)
    while k > 0 and _char_class({prefix[k - 1]}) == klass:
        k -= 1
    new_prefix = prefix[:k]
    new_remains = [v[len(new_prefix):] for v in values]
    new_klass = _char_class(set("".join(new_remains)))
    if new_klass is None:
        return _shipped_infer(values)
    lengths = {len(r) for r in new_remains}
    quant = "{%d}" % next(iter(lengths)) if len(lengths) == 1 else "+"
    return "^" + re.escape(new_prefix) + "[" + new_klass + "]" + quant + "$"


def declared_guard_support(values, decl: str, shipped: str) -> tuple[str, bool]:
    """PRIMARY candidate: ingested declared grammar with a training-consistency gate.

    Adopt the declaration iff every observed training value fullmatches it;
    otherwise refuse the declaration and fall back to the shipped support.  Returns
    (support, adopted).
    """
    vals = [str(v) for v in values]
    consistent = bool(vals) and all(re.fullmatch(decl, v) is not None for v in vals)
    return (decl, True) if consistent else (shipped, False)


def ambiguity_guard_support(values, shipped: str, widened: str) -> tuple[str, bool]:
    """SECONDARY candidate: purely observational pre-bind ambiguity refusal.

    Widen only when the widening is NOT observationally ambiguous.  The widening
    is ambiguous iff it absorbs at least one constant common-prefix character of
    the same character class as the varying remainder AND the terminal observed
    remainder position already saturates that full class.  Returns (support, refused).
    """
    vals = [str(v) for v in values]
    prefix = _common_prefix(vals)
    remains = [v[len(prefix):] for v in vals]
    klass = _char_class(set("".join(remains)))
    if klass is None:
        return widened, False
    absorbed = 0
    while absorbed < len(prefix) and _char_class({prefix[len(prefix) - 1 - absorbed]}) == klass:
        absorbed += 1
    if absorbed == 0:
        return widened, False
    last = {r[-1] for r in remains if r}
    saturated = last == CLASS_FULL[klass]
    if saturated:
        return shipped, True
    return widened, False


# ---------------------------------------------------------------- frozen bank
def build_bank():
    bank = []
    for f in FAMILIES:
        ctx = {"resource_type": f["resource"], "authenticated": True}
        slot = f["resource"]
        v0 = f["train"][0]

        def add(bid, value, intent=None, context=None, params=None, _f=f, _slot=slot):
            bank.append({"bid": bid, "fam": _f["fam"], "value": value,
                         "intent": _f["intent"] if intent is None else intent,
                         "context": dict(ctx) if context is None else context,
                         "params": dict(params) if params is not None else {_slot: value}})

        for i, v in enumerate(f["in_extra"]):
            add("F%s-IN-E%02d" % (f["fam"], i), v)
        for i, v in enumerate(f["train"]):
            add("F%s-IN-T%02d" % (f["fam"], i), v)
        for name, fn in PAYLOAD_CLASSES:
            val = fn(f["id_prefix"], v0)
            add("F%s-OG-%s" % (f["fam"], name), val)
        for i, wv in enumerate(f["out_wrong_subrange"]):
            add("F%s-OG-WRONGRANGE%02d" % (f["fam"], i), wv)
        for i, val in enumerate(TYPE_PAYLOADS):
            add("F%s-OG-TYPE%02d" % (f["fam"], i), val)
        vv = f["train"][1]
        add("F%s-OG-CTX-USERTYPE" % f["fam"], vv, context={"resource_type": "other",
                                                          "authenticated": True})
        add("F%s-OG-CTX-NOAUTH" % f["fam"], vv,
            context={"resource_type": f["resource"], "authenticated": False})
        add("F%s-OG-CTX-MISSING" % f["fam"], vv,
            context={"resource_type": f["resource"]})
        add("F%s-OG-CTX-EMPTY" % f["fam"], vv, context={})
        add("F%s-OG-CTX-INTENT" % f["fam"], vv, intent="delete_" + f["resource"])
        add("F%s-OG-CTX-WRONGKEY" % f["fam"], vv, params={"wrong_key": vv})
        add("F%s-OG-CTX-NOPARAM" % f["fam"], vv, params={})
    return bank


def label_of(item):
    f = FAM_BY_ID[item["fam"]]
    v = item["value"]
    if not isinstance(v, str):
        return "OUT"
    if re.fullmatch(f["declared"], v) is None:
        return "OUT"
    if item["intent"] != f["intent"]:
        return "OUT"
    if item["context"] != {"resource_type": f["resource"], "authenticated": True}:
        return "OUT"
    if item["params"] != {f["resource"]: v}:
        return "OUT"
    return "IN"


def value_repr(v) -> str:
    if isinstance(v, str):
        s = repr(v)
        return s if len(s) <= 140 else s[:140] + "...<%d chars>" % len(v)
    if isinstance(v, (int, float, bool)) or v is None:
        return repr(v)
    return type(v).__name__ + ":" + repr(v)[:80]


# --------------------------------------------------------------- oracle server
def _path_re(f):
    return re.compile("^/api/" + f["resource"] + "s/" + f["declared"][1:-1] + "$")


VALID_PATH_RES = {f["fam"]: _path_re(f) for f in FAMILIES}


class OracleHandler(http.server.BaseHTTPRequestHandler):
    count = 0

    def do_GET(self):
        type(self).count += 1
        path = self.path.split("?", 1)[0]
        matched = next((fam for fam, rx in VALID_PATH_RES.items()
                        if rx.fullmatch(path)), None)
        if matched is not None:
            ident = path.rsplit("/", 1)[-1]
            body = {"type": FAM_BY_ID[matched]["resource"], "id": ident,
                    "data": "res:" + ident}
            self.send_response(200)
        else:
            body = {"error": "not_found", "path": path}
            self.send_response(404)
        payload = json.dumps(body).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


def start_oracle():
    handler = type("Oracle", (OracleHandler,), {"count": 0})
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1], handler


def execute_action(bound):
    url = bound.get("url") if isinstance(bound, dict) else None
    if not isinstance(url, str):
        return None, {"exec_error": "no_url"}
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except Exception as exc:
        return None, {"exec_error": type(exc).__name__ + ": " + str(exc)[:160]}


def drop_modules():
    for m in ("spider", "spider.kernel", "spider.models", "spider.registry"):
        sys.modules.pop(m, None)


def make_arm_registry(mechs, support_by_fam, tmpdir, tag):
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
    reg = reg_cls(Path(tmpdir) / ("mechanisms_%s.jsonl" % tag))
    for fam in FAM_ORDER:
        m = copy.deepcopy(mechs[fam])
        if support_by_fam is not None:
            m.verification_rule = {"parameter_supports": {
                s: support_by_fam[fam] for s in m.parameter_slots}}
        reg.upsert(m)
    return reg


def evaluate(kernel, bank, handler):
    records = []
    for item in bank:
        http0 = handler.count
        rec = {"bid": item["bid"], "fam": item["fam"], "cls": item.get("cls", ""),
               "label": label_of(item), "value": value_repr(item["value"])}
        try:
            r = kernel.resolve(item["intent"], dict(item["context"]), dict(item["params"]))
            rec["status"] = r.status.value
            rec["reason"] = r.reason
            bound = r.bound_action
        except Exception as exc:
            rec["status"] = "RESOLVE_ERROR"
            rec["reason"] = type(exc).__name__ + ": " + str(exc)[:160]
            bound = None
        rec["bound"] = bound is not None
        ex_status, body, verify = None, None, None
        if bound is not None:
            ex_status, body = execute_action(bound)
            if ex_status == 200 and isinstance(body, dict):
                try:
                    verify = kernel.verify(item.get("_mech_id"), body, dict(item["params"]))
                except Exception:
                    verify = False
            elif ex_status is not None:
                verify = False
        rec["exec_status"] = ex_status
        rec["verify"] = verify
        rec["exec_error"] = body.get("exec_error") if isinstance(body, dict) else None
        rec["http_delta"] = handler.count - http0
        records.append(rec)
    return records


def _summarize(records):
    n_in = sum(1 for r in records if r["label"] == "IN")
    n_out = sum(1 for r in records if r["label"] == "OUT")
    accepts = [r for r in records if r["status"] == "EXECUTABLE"]
    fa = [r for r in records if r["label"] == "OUT" and r["status"] == "EXECUTABLE"]
    sfa = [r for r in fa if r["exec_status"] == 200 and r["verify"] is True]
    fr = [r for r in records if r["label"] == "IN" and r["status"] != "EXECUTABLE"]
    http_out = sum(r["http_delta"] for r in records if r["label"] == "OUT")
    http_total = sum(r["http_delta"] for r in records)
    refusal_exec = sum(1 for r in records
                       if r["label"] == "OUT" and r["status"] != "EXECUTABLE"
                       and r["http_delta"] > 0)
    cov = (n_in - len(fr)) / n_in if n_in else None
    return {
        "n_in": n_in, "n_out": n_out, "accept_count": len(accepts),
        "false_accept_count": len(fa), "silent_false_accept_count": len(sfa),
        "false_reject_count": len(fr), "coverage": cov,
        "http_on_out_label": http_out, "http_total": http_total,
        "refusal_executed_count": refusal_exec,
        "false_accept_bids": [r["bid"] for r in fa],
        "silent_false_accept_bids": [r["bid"] for r in sfa],
        "false_reject_bids": [r["bid"] for r in fr],
    }


def summarize(records):
    out = _summarize(records)
    out["per_family"] = {}
    for fam in FAM_ORDER:
        sub = [r for r in records if r["fam"] == fam]
        out["per_family"][fam] = _summarize(sub)
    return out


# --------------------------------------------------------------- V8 freeze bind
def _extract(text, name):
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END "
                  + re.escape(name) + r" -->", text, re.S)
    if not m:
        raise RuntimeError("block %s not found in prereg.md" % name)
    return m.group(1)


def v8_freeze_binding(result):
    probe = os.environ.get("EXP_PROBE_MODE") == "1"
    exp = REPO_ROOT / EXP_DIR
    freeze_path = exp / "freeze.json"
    if not freeze_path.exists():
        if probe:
            result["observations"].append({"type": "binding",
                                           "V8": "UNBOUND-RUN: no freeze.json (probe mode only)."})
            return True
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "freeze.json missing at %s (EXECUTE mode)" % freeze_path}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    try:
        freeze = json.loads(freeze_path.read_text())

        def norm(s):
            return s.replace("\r\n", "\n").rstrip()

        prereg_b = (exp / "prereg.md").read_bytes()
        block = _extract(prereg_b.decode("utf-8"), "FROZEN RUNNER")
        this_src = Path(__file__).resolve().read_text(encoding="utf-8")
        ok_a = hashlib.sha256(prereg_b).hexdigest() == freeze["hashes"]["prereg.md"]
        ok_b = norm(this_src) == norm(block)
        ok_c = all(hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest() == h
                   for rel, h in freeze.get("artifact_hashes", {}).items())
    except Exception as exc:
        result["certificate"]["V8_FREEZE_BINDING"] = {
            "status": "MEASUREMENT_INVALID", "reason": "freeze binding unreadable: " + str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    ok_all = ok_a and ok_b and ok_c
    result["certificate"]["V8_FREEZE_BINDING"] = {
        "status": "PASS" if ok_all else "FAIL", "prereg_sha_matches": ok_a,
        "runner_source_matches_frozen_block": ok_b, "artifact_hashes_match": ok_c,
        "reason": "hash-bound prereg; running source == FROZEN RUNNER block; freeze artifacts intact"}
    if not ok_all:
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return False
    return True


# -------------------------------------------------------------------- one run
def run_once(carrier_cls, counters_cls, reg_cls, obs_cls):
    server, port, handler = start_oracle()
    try:
        tmp = tempfile.mkdtemp(prefix="exp38201227093_")
        reg_cls(Path(tmp) / "base.jsonl")  # touch registry dir
        mechs = {}
        identity = {}
        for f in FAMILIES:
            obs = []
            for ident in f["train"]:
                url = "http://127.0.0.1:%d/api/%ss/%s" % (port, f["resource"], ident)
                st, body = execute_action({"url": url})
                if st != 200:
                    raise RuntimeError("induction GET %s -> %s" % (ident, st))
                obs.append(obs_cls(intent=f["intent"],
                                   state={"resource_type": f["resource"], "authenticated": True},
                                   action={"method": "GET", "url": url},
                                   next_state=body, success=True,
                                   provenance={"exp": EXPERIMENT_ID, "role": "induction"}))
            reg = reg_cls(Path(tmp) / ("base_%s.jsonl" % f["fam"]))
            kernel = carrier_cls(reg, counters=counters_cls())
            m = kernel.distill_parameterized(obs)
            if m is None:
                raise RuntimeError("distill_parameterized returned None for fam " + f["fam"])
            reg.upsert(m)
            mechs[f["fam"]] = m
            identity[f["fam"]] = {
                "slots": list(m.parameter_slots),
                "support": m.verification_rule["parameter_supports"],
                "confidence": m.confidence,
            }

        bank = build_bank()
        ids = [b["bid"] for b in bank]
        if len(ids) != len(set(ids)):
            raise RuntimeError("duplicate bank bids")

        shipped = {fam: mechs[fam].verification_rule["parameter_supports"][FAM_BY_ID[fam]["resource"]]
                   for fam in FAM_ORDER}
        for fam in FAM_ORDER:
            if shipped[fam] != EXPECTED_SHIPPED[fam]:
                raise RuntimeError("shipped support drift fam %s: %s" % (fam, shipped[fam]))

        widened = {fam: widen_support(FAM_BY_ID[fam]["train"]) for fam in FAM_ORDER}
        for fam in FAM_ORDER:
            if widened[fam] != EXPECTED_WIDENED[fam]:
                raise RuntimeError("widened support drift fam %s: %s" % (fam, widened[fam]))

        declared = {fam: DECLARED_GRAMMAR[fam] for fam in FAM_ORDER}

        decl_guard = {}
        decl_adopted = {}
        for fam in FAM_ORDER:
            s, adopted = declared_guard_support(FAM_BY_ID[fam]["train"], declared[fam], shipped[fam])
            decl_guard[fam] = s
            decl_adopted[fam] = adopted

        amb_guard = {}
        amb_refused = {}
        for fam in FAM_ORDER:
            s, refused = ambiguity_guard_support(FAM_BY_ID[fam]["train"], shipped[fam], widened[fam])
            amb_guard[fam] = s
            amb_refused[fam] = refused
        for fam in FAM_ORDER:
            if amb_guard[fam] != EXPECTED_AMBIGUITY[fam]:
                raise RuntimeError("ambiguity-guard support drift fam %s: %s"
                                   % (fam, amb_guard[fam]))

        decl_under = {}
        decl_under_adopted = {}
        for fam in FAM_ORDER:
            s, adopted = declared_guard_support(FAM_BY_ID[fam]["train"], DECL_UNDER[fam], shipped[fam])
            decl_under[fam] = s
            decl_under_adopted[fam] = adopted

        decl_overwide = {}
        decl_overwide_adopted = {}
        for fam in FAM_ORDER:
            s, adopted = declared_guard_support(FAM_BY_ID[fam]["train"], DECL_OVERWIDE[fam], shipped[fam])
            decl_overwide[fam] = s
            decl_overwide_adopted[fam] = adopted

        openwide = {fam: "^" + re.escape(FAM_BY_ID[fam]["id_prefix"]) + r"\-[0-9a-zA-Z]+$"
                    for fam in FAM_ORDER}
        coarse = {fam: COARSE for fam in FAM_ORDER}

        for fam in FAM_ORDER:
            for item in bank:
                if item["fam"] == fam:
                    item["_mech_id"] = mechs[fam].mechanism_id

        def arm(support_by_fam, tag):
            reg = make_arm_registry(mechs, support_by_fam, tmp, tag)
            k = carrier_cls(reg, counters=counters_cls())
            return evaluate(k, bank, handler)

        decl_recs = arm(decl_guard, "declared_guard")
        amb_recs = arm(amb_guard, "ambiguity_guard")
        data_recs = arm(widened, "data_widened")
        shipped_recs = arm(None, "shipped")
        declared_recs = arm(declared, "declared_full")
        coarse_recs = arm(coarse, "coarse")
        open_recs = arm(openwide, "open")
        under_recs = arm(decl_under, "decl_under")
        over_recs = arm(decl_overwide, "decl_overwide")
        empty_reg = reg_cls(Path(tmp) / "reg_empty.jsonl")
        empty_recs = evaluate(carrier_cls(empty_reg, counters=counters_cls()), bank, handler)

        replay = []
        for f in FAMILIES:
            for ident in f["train"]:
                r = carrier_cls(reg_cls(Path(tmp) / ("base_%s.jsonl" % f["fam"])),
                                counters=counters_cls()).resolve(
                    f["intent"], {"resource_type": f["resource"], "authenticated": True},
                    {f["resource"]: ident})
                replay.append({"fam": f["fam"], "id": ident, "status": r.status.value})

        return {
            "mechanism_identity": identity,
            "shipped_support": shipped,
            "widened_support": widened,
            "declared_guard_support": decl_guard,
            "declared_guard_adopted": decl_adopted,
            "ambiguity_guard_support": amb_guard,
            "ambiguity_guard_refused": amb_refused,
            "decl_under_adopted": decl_under_adopted,
            "decl_overwide_adopted": decl_overwide_adopted,
            "declared": summarize(decl_recs),
            "ambiguity": summarize(amb_recs),
            "data_widened": summarize(data_recs),
            "shipped": summarize(shipped_recs),
            "comparator_declared": summarize(declared_recs),
            "control_coarse": summarize(coarse_recs),
            "control_open": summarize(open_recs),
            "control_decl_under": summarize(under_recs),
            "boundary_decl_overwide": summarize(over_recs),
            "null_reject_all": summarize(empty_recs),
            "pc_exact_replay": {"status": "PASS" if all(x["status"] == "EXECUTABLE"
                                                        for x in replay) else "FAIL",
                                "replay": replay},
        }
    finally:
        server.shutdown()


def main():
    result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "lane": "product",
              "certificate": {}, "observations": [], "unresolved": []}
    if not v8_freeze_binding(result):
        return result

    kernel_path = REPO_ROOT / "src/spider/kernel.py"
    shipping_sha = sha256_bytes(kernel_path.read_bytes())
    result["identities"] = {"shipping_kernel_sha256": shipping_sha,
                            "carrier_expected_sha256": CARRIER_SHA256,
                            "carrier_git_blob": CARRIER_BLOB}
    if shipping_sha != CARRIER_SHA256:
        result["certificate"]["M-IDENTITY"] = {
            "status": "MEASUREMENT_INVALID",
            "reason": "shipping kernel sha %s != frozen carrier %s" % (shipping_sha, CARRIER_SHA256)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result
    result["certificate"]["M-IDENTITY"] = {
        "status": "PASS", "reason": "shipping kernel == frozen carrier " + CARRIER_BLOB}

    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        drop_modules()
        spider = __import__("spider")
        Carrier = spider.SpiderKernel
        obs_cls = spider.Observation
        counters_cls = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
        reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry
        min_conf = Carrier.__init__.__defaults__[0]
        if min_conf != EXPECTED_MIN_CONFIDENCE:
            raise RuntimeError("shipped min_confidence default %s != %s" % (min_conf, EXPECTED_MIN_CONFIDENCE))
    except Exception as exc:
        result["certificate"]["M-IDENTITY"] = {"status": "MEASUREMENT_INVALID",
                                              "reason": "import/threshold failure: " + str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result

    # B-LITERAL-KERNEL ablation
    try:
        lit = read_source("git:" + LITERAL_BLOB)
        if sha256_bytes(lit) != LITERAL_SHA256:
            raise RuntimeError("literal blob sha mismatch")
        with tempfile.TemporaryDirectory() as td:
            pkg = Path(td) / "spider"
            pkg.mkdir(parents=True)
            for name in ("models.py", "registry.py", "__init__.py"):
                (pkg / name).write_bytes((REPO_ROOT / "src/spider" / name).read_bytes())
            (pkg / "kernel.py").write_bytes(lit)
            sys.path.insert(0, td)
            drop_modules()
            litpkg = __import__("spider")
            has_param = hasattr(litpkg.SpiderKernel, "distill_parameterized")
            sys.path.remove(td)
            drop_modules()
        result["certificate"]["B-LITERAL-KERNEL"] = {
            "status": "PASS" if not has_param else "FAIL",
            "has_distill_parameterized": has_param,
            "reason": "literal pre-promotion kernel cannot construct the parameterized mechanism"}
    except Exception as exc:
        result["certificate"]["B-LITERAL-KERNEL"] = {"status": "MEASUREMENT_INVALID", "reason": str(exc)}
        result["status"], result["outcome"] = "BLOCKED", "NOT_APPLICABLE"
        return result

    drop_modules()
    spider = __import__("spider")
    Carrier = spider.SpiderKernel
    obs_cls = spider.Observation
    counters_cls = __import__("spider.kernel", fromlist=["TrajectoryCounters"]).TrajectoryCounters
    reg_cls = __import__("spider.registry", fromlist=["MechanismRegistry"]).MechanismRegistry

    run1 = run_once(Carrier, counters_cls, reg_cls, obs_cls)
    run2 = run_once(Carrier, counters_cls, reg_cls, obs_cls)
    det = (json.dumps(run1["declared"], sort_keys=True) == json.dumps(run2["declared"], sort_keys=True)
           and json.dumps(run1["ambiguity"], sort_keys=True) == json.dumps(run2["ambiguity"], sort_keys=True)
           and json.dumps(run1["data_widened"], sort_keys=True) == json.dumps(run2["data_widened"], sort_keys=True)
           and json.dumps(run1["shipped"], sort_keys=True) == json.dumps(run2["shipped"], sort_keys=True)
           and json.dumps(run1["comparator_declared"], sort_keys=True)
           == json.dumps(run2["comparator_declared"], sort_keys=True)
           and run1["mechanism_identity"] == run2["mechanism_identity"]
           and run1["declared_guard_support"] == run2["declared_guard_support"]
           and run1["ambiguity_guard_support"] == run2["ambiguity_guard_support"])
    result["certificate"]["PC-DETERMINISM-REPEAT"] = {
        "status": "PASS" if det else "FAIL",
        "reason": "two independent runs produce identical arm metrics and support identity"}

    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_*.py")
    tr = unittest.TextTestRunner(verbosity=0).run(suite)
    result["certificate"]["M-REGRESSION"] = {
        "status": "PASS" if (tr.wasSuccessful() and tr.testsRun >= 3) else "FAIL",
        "tests_run": tr.testsRun, "failures": len(tr.failures), "errors": len(tr.errors)}

    d = run1["declared"]
    a = run1["ambiguity"]
    w = run1["data_widened"]
    s = run1["shipped"]
    dd = run1["comparator_declared"]
    result["certificate"]["M-SUPPORT-IDENTITY"] = {
        "status": "PASS" if (run1["shipped_support"] == EXPECTED_SHIPPED
                             and run1["widened_support"] == EXPECTED_WIDENED
                             and run1["ambiguity_guard_support"] == EXPECTED_AMBIGUITY) else "FAIL",
        "shipped": run1["shipped_support"], "widened": run1["widened_support"],
        "ambiguity": run1["ambiguity_guard_support"],
        "reason": "induced shipped supports and frozen widened/ambiguity supports match DESIGN constants"}

    result["certificate"]["T-DECLARED-GUARD"] = {
        "status": "PASS",
        "false_accept_count": d["false_accept_count"],
        "silent_false_accept_count": d["silent_false_accept_count"],
        "false_reject_count": d["false_reject_count"],
        "coverage": d["coverage"],
        "http_on_out_label": d["http_on_out_label"],
        "refusal_executed_count": d["refusal_executed_count"],
        "false_accept_bids": d["false_accept_bids"],
        "false_reject_bids": d["false_reject_bids"],
        "adopted": run1["declared_guard_adopted"],
        "per_family": d["per_family"],
        "reason": "ingested declared grammar with training-consistency gate; safe iff "
                  "false_accept_count==0 and http_on_out_label==0; complete iff coverage==1.0"}
    result["certificate"]["T-AMBIGUITY-GUARD"] = {
        "status": "PASS",
        "false_accept_count": a["false_accept_count"],
        "silent_false_accept_count": a["silent_false_accept_count"],
        "false_reject_count": a["false_reject_count"],
        "coverage": a["coverage"],
        "http_on_out_label": a["http_on_out_label"],
        "refusal_executed_count": a["refusal_executed_count"],
        "false_accept_bids": a["false_accept_bids"],
        "false_reject_bids": a["false_reject_bids"],
        "refused_families": sorted(f for f in FAM_ORDER if run1["ambiguity_guard_refused"][f]),
        "per_family": a["per_family"],
        "reason": "purely observational ambiguity refusal; safe iff false_accept_count==0"}
    result["certificate"]["B-DATA-WIDENED"] = {
        "status": "PASS",
        "false_accept_count": w["false_accept_count"], "coverage": w["coverage"],
        "false_accept_bids": w["false_accept_bids"], "per_family": w["per_family"],
        "reason": "frozen parent data-driven widening comparator on the extended bank"}
    result["certificate"]["B-SHIPPED"] = {
        "status": "PASS" if s["false_accept_count"] == 0 else "FAIL",
        "false_accept_count": s["false_accept_count"], "false_reject_count": s["false_reject_count"],
        "coverage": s["coverage"], "http_on_out_label": s["http_on_out_label"],
        "false_reject_by_family": {f: s["per_family"][f]["false_reject_count"] for f in FAM_ORDER},
        "per_family": s["per_family"], "reason": "shipped single-observation-length supports"}
    result["certificate"]["B-DECLARED-FULL"] = {
        "status": "PASS" if (dd["false_accept_count"] == 0 and dd["coverage"] == 1.0) else "FAIL",
        "false_accept_count": dd["false_accept_count"], "coverage": dd["coverage"],
        "per_family": dd["per_family"],
        "reason": "strong comparator: declared-grammar supports are safe+complete on the bank"}
    result["certificate"]["PC-UNSAFE-COARSE"] = {
        "status": "PASS" if run1["control_coarse"]["false_accept_count"] >= 1 else "FAIL",
        "false_accept_count": run1["control_coarse"]["false_accept_count"],
        "reason": "positive control: the carrier's own __COARSE__ fallback must over-accept"}
    result["certificate"]["PC-OVERWIDE-OPEN"] = {
        "status": "PASS" if run1["control_open"]["false_accept_count"] >= 1 else "FAIL",
        "false_accept_count": run1["control_open"]["false_accept_count"],
        "reason": "positive control: an open-width class support must over-accept"}
    result["certificate"]["PC-DECL-UNDER"] = {
        "status": "PASS" if (not any(run1["decl_under_adopted"].values())
                             and run1["control_decl_under"]["false_accept_count"] == 0) else "FAIL",
        "adopted": run1["decl_under_adopted"],
        "false_accept_count": run1["control_decl_under"]["false_accept_count"],
        "reason": "treatment-sensitivity control: the consistency gate must refuse a too-narrow "
                  "declaration and fall back to the safe shipped support"}
    result["certificate"]["BP-DECL-OVERWIDE"] = {
        "status": "PASS",
        "adopted": run1["decl_overwide_adopted"],
        "false_accept_count": run1["boundary_decl_overwide"]["false_accept_count"],
        "reason": "boundary probe: an over-wide declaration passes the training-consistency gate "
                  "but inherits its own false accepts (declaration soundness is external)"}
    result["certificate"]["NC-REJECT-ALL"] = {
        "status": "PASS" if (run1["null_reject_all"]["accept_count"] == 0
                             and run1["null_reject_all"]["http_total"] == 0) else "FAIL",
        "accept_count": run1["null_reject_all"]["accept_count"],
        "http_total": run1["null_reject_all"]["http_total"],
        "reason": "null floor: empty registry accepts nothing and issues no HTTP"}
    result["certificate"]["PC-EXACT-REPLAY"] = run1["pc_exact_replay"]

    result["arms"] = {
        "T-DECLARED-GUARD": run1["declared"],
        "T-AMBIGUITY-GUARD": run1["ambiguity"],
        "B-DATA-WIDENED": run1["data_widened"],
        "B-SHIPPED": run1["shipped"],
        "B-DECLARED-FULL": run1["comparator_declared"],
        "PC-UNSAFE-COARSE": run1["control_coarse"],
        "PC-OVERWIDE-OPEN": run1["control_open"],
        "PC-DECL-UNDER": run1["control_decl_under"],
        "BP-DECL-OVERWIDE": run1["boundary_decl_overwide"],
        "NC-REJECT-ALL": run1["null_reject_all"],
    }
    result["mechanism_identity"] = run1["mechanism_identity"]
    result["bank"] = {
        "n_items": len(build_bank()), "n_in": d["n_in"], "n_out": d["n_out"],
        "per_family_n_in": {f: d["per_family"][f]["n_in"] for f in FAM_ORDER},
        "per_family_n_out": {f: d["per_family"][f]["n_out"] for f in FAM_ORDER},
    }

    validity_gates = ("V8_FREEZE_BINDING", "M-IDENTITY", "M-REGRESSION",
                      "PC-DETERMINISM-REPEAT", "PC-EXACT-REPLAY", "B-LITERAL-KERNEL",
                      "M-SUPPORT-IDENTITY", "B-SHIPPED", "B-DECLARED-FULL")
    validity = all(result["certificate"][k]["status"] == "PASS" for k in validity_gates)
    failed_validity = [k for k in validity_gates if result["certificate"][k]["status"] != "PASS"]
    sensitivity = (result["certificate"]["PC-UNSAFE-COARSE"]["status"] == "PASS"
                   and result["certificate"]["PC-OVERWIDE-OPEN"]["status"] == "PASS"
                   and result["certificate"]["PC-DECL-UNDER"]["status"] == "PASS"
                   and result["certificate"]["NC-REJECT-ALL"]["status"] == "PASS")
    if not validity:
        result["status"], result["outcome"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
        result["reason"] = "instrument/validity gates failed: " + ", ".join(failed_validity)
        return result
    if not sensitivity:
        result["status"], result["outcome"] = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
        result["reason"] = "guard/safety oracle failed its sensitivity/null controls; cannot certify"
        return result

    # ---- secondary disposition of the purely observational guard ----
    if a["false_accept_count"] > 0 or a["http_on_out_label"] > 0 or a["refusal_executed_count"] > 0:
        amb_disp = "UNSAFE"
    elif a["coverage"] == 1.0:
        amb_disp = "SAFE_AND_COMPLETE"
    else:
        amb_disp = "SAFE_INCOMPLETE"
    result["observational_guard_disposition"] = amb_disp

    # ---- primary decision on T-DECLARED-GUARD ----
    if d["false_accept_count"] > 0 or d["http_on_out_label"] > 0 or d["refusal_executed_count"] > 0:
        result["status"], result["outcome"] = "COMPLETE", "FALSIFIES"
        result["decision"] = "DECLARED_GUARD_UNSAFE__OBSERVATIONAL_GUARD_" + amb_disp
        result["reason"] = ("the ingested declared-grammar guard bound %d out-of-grammar payload(s) "
                            "and issued HTTP on out-of-grammar=%d" %
                            (d["false_accept_count"], d["http_on_out_label"]))
    elif d["coverage"] == 1.0:
        result["status"], result["outcome"] = "COMPLETE", "SUPPORTS"
        result["decision"] = "DECLARED_GUARD_SAFE_AND_COMPLETE__OBSERVATIONAL_GUARD_" + amb_disp
        result["reason"] = ("the ingested declared-grammar guard held zero false accepts and full "
                            "coverage on the extended bank; the purely observational ambiguity guard "
                            "disposition is %s" % amb_disp)
    else:
        result["status"], result["outcome"] = "COMPLETE", "MIXED"
        result["decision"] = "DECLARED_GUARD_SAFE_BUT_INCOMPLETE__OBSERVATIONAL_GUARD_" + amb_disp
        result["reason"] = ("the declared-grammar guard was safe but coverage %.4f < 1.0 "
                            "(false rejects %d); observational guard disposition %s" %
                            (d["coverage"], d["false_reject_count"], amb_disp))
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True, default=repr))

<!-- END FROZEN RUNNER -->
