# R0 CYCLE 2 — NEAR-REPEAT KILL EXPERIMENT PREREGISTRATION
# (FROZEN BEFORE OUTCOMES)

Lane: RUNTIME. Cycle: R0-2 (GitHub run 32908002333). Date frozen:
2026-08-26. Status: FROZEN. Freeze ordering is GIT-AUDITABLE (audit W4):
this file and the probe evidence are committed to the cycle branch in a
commit that precedes any commit containing live outcome rows. The driver
records `prereg_sha256` in its results file at run start. Any analysis
change after seeing outcomes is exploratory and must be labeled as such.

## 1. Question

Does SPIDER inheritance compress work when ROUTE-FINDING dominates — i.e.,
when the goal text does NOT lexically reveal the route to the memory-free
greedy baseline — and is the structured handoff hint CAUSAL rather than
decorative? Either answer completes R0's missing measurement: a strict
margin win is the program's first demonstrated compression observation;
parity/non-causality completes R0 as an honest negative skeleton.

Not claimed this cycle: composition, cross-model inheritance (single caller
implementation; UNFALSIFIABLE), calibrated confidence, TTL/staleness
arithmetic, inter-capsule ranking (key sets remain byte-identical).

## 2. Fixed inputs

- Capsules: exactly the two accepted R0-1 CANDIDATE capsules derived from
  the Graph cycle-3 store dump (sha256
  `ec5af9e146ea629fac642ec4a7b14c49b685e5c193cff345a92191b7e05e7073`),
  reproduced byte-identically (golden test
  `tests/runtime/test_derive_golden.py`). Status stays CANDIDATE; unmeasured
  fields null.
- Retrieval: vendored goalsig desc_only scoring over
  `intent.semantic_keys` ONLY; inherited UNTUNED constants tau=0.30 /
  min_match=2 / topk=3 are RETAINED per the frozen probe decision rule
  (§8); retrieval_version pinned in every response.
- Sites: quotes.toscrape.com, books.toscrape.com (frozen sandbox sites).
  Single-site template coupling is a named threat (§11).
- derive.py is NOT modified this cycle (golden byte-regression guard);
  write-back lives in new `runtime/writeback.py`.

## 3. Tasks and the near-repeat construction rule

Shared success predicate `rt.tasks:quotes_login_success@v1`
(host_allowlist=[quotes.toscrape.com], elem_text_any=["logout"]); shared
capsule precondition `host_allowlist=[quotes.toscrape.com]` +
`elem_text_any=["login"]`.

Keyword derivation (PINNED pure function, both arms symmetric):
raw `[a-z0-9]+` tokens of goal_text, STOPWORDS removed, NO stemming,
first-occurrence order preserved (`runtime/pilot2.py::goal_keywords`).

Leakage fixture (machine-checked pre-batch; violation aborts): no keyword
may be a substring of any route-anchor surface (`login`, `/login`).

- T1 (exact-repeat, R0-1 continuity): goal_text "log in to quotes toscrape
  with the username spiderbot and password notasecret" (deliberately
  lexically transparent — disclosed); start https://quotes.toscrape.com/.
- T2 (stale/wrong-host): same goal/predicate; entry
  https://books.toscrape.com/. Capsule artifact NOT edited.
- T3 NEAR-REPEAT KILL CELL. Construction rule (disclosed): demand/effect
  vocabulary drawn from capsule-key families MINUS all route-anchor
  vocabulary; retrieval must clear thresholds WITHOUT naming the anchor.
  Frozen goal_text: "access your quotes toscrape account: use the public
  demo credentials to complete the site sign-in form".
  Retrieval arithmetic (pre-outcome): tokens {access,your,quot,toscrape,
  account,public,demo,credential,complete,site,sign,form}; matched pairs=3
  (quot, toscrape, form) >= 2; coverage 3/min(12,6)=0.50 >= 0.30 ->
  RESOLVED expected; one spare pair above MIN_MATCH guards tokenizer drift.
  Keywords=[access,your,quotes,toscrape,account,public,demo,credentials,
  complete,site,sign,form]; leakage fixture passes (verified).
  Entries: p1 = https://quotes.toscrape.com/tag/love/ ;
           p2 = https://quotes.toscrape.com/page/10/
  (two DIFFERENT offset entries: replication + offset-robustness in one;
  the capsule precondition persists via the global header anchor).
  Pre-outcome diagnostic: results/runtime/probes/t3_offline_rank_probe.json
  records the frozen offline rank simulation over captured snapshots —
  login_is_top=false on BOTH entries (top choice = brand link). The probe
  predicts intent, not the full live trajectory; gates decide outcomes.

## 4. Arms

- BASE ("b0"): vendored zero-memory scripted explorer (runtime/baseline.py,
  policy UNTOUCHED this cycle; additive telemetry only: entry_digest,
  predicate_evals_total, native final-verdict timing).
- SPIDER ("spider"): resolve -> applicability -> per-segment
  APPLICABILITY_PASS trail -> inherited replay OR clause-attributed ABSTAIN
  -> HANDOFF-TO-CALLER.
- A0 hint arm: the C2 caller repairs context using ONLY
  hint.params.expected_host from the materialized plan.
- A1 stripped-hint arm: pure transform `strip_hint()` removes ALL FIVE
  resolver-added target channels (hint.params.expected_host,
  hint.params.capsule_id, failed_clauses[*].detail,
  abstain_reason.clause_results[*].detail, segments[*].capsule_id +
  capsule_version_sha256); caller-supplied echoes (goal_text_echo,
  context.*) are not resolver leakage and stay. Mechanical blinding scan
  masks echo fields and asserts absence of {quotes.toscrape.com, books…
  toscrape, toscrape, login, /login, quot}; validate_plan must still pass.
  BLINDED CALLER (W2): there is NO default target anywhere; absent usable
  hint => outcome UNACTIONABLE, ZERO navigation/actions.

## 5. Cells, order, rerun policy

Cell C1 = T1 both arms, passes p1+p2. Cell C2/A0 = T2 both arms, p1+p2.
Cell T3 = both entries, p1+p2. ABL A1 = single pass (causal logic, not
magnitude). Order: C1, C2, T3, A1; BASE first then SPIDER per pass; fresh
browser session per row. Preflight (phase=smoke) MUST pass before the
batch: quotes-home login anchor; /login inputs; books-home healthy; BOTH
T3 entries healthy with EXACTLY ONE `a|||||login` signature and
applicability PASS (evaluate_applicability). Keyword leakage fixture must
pass. HEALTH_TRIP classes (unhealthy entry, wall deadline 80s advisory
BOTH arms, transport error) and EXPECTATION_TRIPs are RECORDED rows (W9),
never crashes; deterministic health classes get max ONE PAIRED retry
(both arms or neither; suffix r2; originals preserved append-only).
Within-pair entry_digest equality required for same-entry pairs (C1/C2)
(W8); mismatch => one paired retry, then DIGEST_MISMATCH failed row excluded
from claims. Loads are read from summary rows and cross-checked (P5);
gates depend only on stream-counted actions.

## 6. Metrics (frozen definitions; stage-semantics invariant)

latency_ms carries the natively-timed duration of exactly the operation
identified by (stage, event_class): browser/action -> act() ms;
retrieval/retrieval_event -> resolve()/applicability ms;
verify/health -> verifier compute ms ONLY (never wall); maintenance/
summary_event -> whole-arm wall_ms_perf (sole in-stream wall record);
plan/write_guard -> caller-repair ms. Violation => mechanical label gate
False. BASE discloses predicate_evals_total (~once/action asymmetry).
Actions/novel/reused counted from ACTOR-TAGGED event rows
(runtime_inherited | caller | baseline_explorer); counters ignored by gate
code. Integer action counts only; NO ms->action conversion anywhere.

## 7. Gates (frozen before outcomes; all computed BY CODE from
cost_events.jsonl filtered to schema spider.cost_event/v0 — runtime/gates.py)

Per-pass exact-repeat/stale gates (C1, C2):
- G-C1a: both arms succeed, harness_predicate-judged verify rows.
- G-C1b: spider_stream_actions <= base_stream_actions AND reused ==
  steps_len pinned from APPLICABILITY_PASS rows AND novel(stream)==0.
- G-C1c: ordered-stream predicates P1-P5 (every runtime_inherited action
  preceded STRICTLY by its own segment's APPLICABILITY_PASS; no action
  before first retrieval/handoff; summary-count consistency; verify-label
  invariant). Scope: applicability is established ONCE PER SEGMENT on the
  ENTRY snapshot; caller actions sit outside runtime applicability BY
  DESIGN.
- G-C2a: ret1 ABSTAIN with >=1 fail/unknown clause attributed, ZERO
  spider actions before handoff, attribution echoed through handoff note.
- G-C2b: handoff note plan_validated=true, validator_errors=[], plan
  schema spider.plan/v0; ret2 RESOLVED; verified success.
- G-C2c': BASE honesty = mutual consistency (harness judge; stream-counted
  actions == summary cost.actions; reported host-failure checks consistent
  with final landing host).

Near-repeat kill-cell gates (T3), M=2 FROZEN:
- G-T3a: both arms succeed on every pass.
- G-T3b (compression): EVERY pass satisfies spider_actions <=
  base_actions - 2, reused == expected, novel == 0; aggregate
  sum(spider) <= sum(base) - 2M; DISCORDANCE KILL-SWITCH: sign disagreement
  between passes => DISCORDANT, no compression wording; BASE_CAPPED: any
  base pass at >=60 actions without success censors the denominator =>
  ineligible regardless of ratio.
- G-T3c: P1-P5 + label invariant per pass.
- Off-host excursion of BASE => baseline-fragility artifact class; any
  compression wording additionally requires BASE on-host AND success.
- DIGEST_MISMATCH handling as §5.

Hint causality (FROZEN): hint causal iff A0 verified-success with
<=1 novel action AND (A1 records UNACTIONABLE-with-ZERO actions OR A1
novel >= A0 novel + 2). Disclosed ceiling: sufficiency-vs-necessity within
THIS caller implementation only.

Outcome rule, both directions: G-T3a AND G-T3b AND G-T3c true =>
preregistered COMPRESSION OBSERVATION at the wording ceiling below; else
the near-repeat thesis is KILLED at this scale and R0 completes as a valid
negative skeleton (with bottleneck measurement owed to docs/NEXT_RUNTIME).

## 8. Tau policy (W5) — frozen decision rule, applied pre-outcome

Offline probe suite (runtime/probes.py; committed BEFORE outcomes):
true-positive paraphrases / true negatives / token-sharing near-misses;
benchmark task texts excluded. Decision rule: keep inherited (0.30, 2)
unless TN leakage > 0 there (then smallest tau with zero TN leakage and
TP recall >= 0.75) or TP recall < 0.75 there (then largest qualifying
tau); otherwise keep and record. Near-miss hits NEVER retune alone.
Probe results are committed with this prereg (results/runtime/probes/
probe_suite.json). Derive-time duplicate-key degeneracy rule adopted in
writeback.duplicate_key_note.

## 9. Write-back scope (priority 3)

Verified outcomes/aborts/handoffs persist as content-hashed
spider.observation/v0 records (value=null pinned; ts copied from source
events; exclusion-hash ids; conflicting content rejected). Successor
CANDIDATE capsules derive via runtime/writeback.py (derive.py untouched):
semantic_keys from OBSERVED goal-text stems; mechanism copied VERBATIM
from parent via manifest join; freshness.last_verified_at + measured
action counts populated; disjoint `-wb@v{k}` slugs, append-only versions.
DISCLOSED: observations are derivation substrate ONLY; whether they can
serve as applicability-boundary evidence stays OPEN (Director/CTO
question). Because every execution this cycle traces to the parent
mechanism, the compounding claim may be NULL-BY-DESIGN; a duplicate-key
dominance outcome is reported as such, not spun as partial credit.
Write-back persistence cost is charged OUTSIDE pilot cells and disclosed
separately (maintenance accounting).

## 10. Claim-strength ceilings (maximum defensible wordings)

If G-T3* pass: "strictly fewer browser actions than the memory-free
baseline, replicated across both offset-entry passes of a single
near-repeat task, with zero novel decisions — a work-compression
OBSERVATION at pilot scale; magnitude not quoted pending >=3 samples and
multi-task replication." Never "speedup"; ratios reported as numbers only.
Registry-level resolution wording ONLY (tie-break picks among
byte-identical key sets; "ranked the right capsule" is unsupported).
Model independence remains UNFALSIFIABLE (one caller implementation).

## 11. Threats (named)

Single-site template coupling (all cells share one site's header-login
invariant); BASE competence partly a DOM-order artifact (expected
trajectory ~6 actions: logo wander, Login, form — declared, BASE not
retuned post-hoc); leak-free scoring relies on href being extracted
path-relative in the vendored observation layer (environment-coupled,
re-probed each cycle); signature sensitivity boundary: cls/text/tag/type/
role/name churn flips to safe UNRESOLVED_STEP, href/aria/position churn
tolerated (pinned by tests, not assumed); warm-process registry reads
inside timed retrieval region (conservative direction).

## 12. Determinism scope

Seed 20260825 governs policy/scoring ORDER only; live-server behavior is
probed, not controlled. Zero provider calls anywhere in either arm.

## 13. Post-outcome obligations

Results, mechanical gate outputs, twin identity errors, observation
records, successor manifest, and the cycle report are committed together
AFTER outcomes exist; state/runtime_loop.json updated to
CYCLE_COMPLETE_PENDING_INDEPENDENT_AUDIT with exact evidence paths.
