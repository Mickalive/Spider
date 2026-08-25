# PB-001 BENCHMARK PREREGISTRATION — v2 — FROZEN BEFORE ANY PHASE-B OUTCOME

Beta: **PB-001** · Prereg author: BETA ARCHITECT · Freeze date: **2026-08-25** (v2; v1 preserved at
`cycle/product/32799261473/architect`) · Legal basis: `state/product_beta_request.json` rev 4
(Director floor + `directed_pre_outcome_revision_v2`) + `SPIDER_MASTER_PROMPT.md` §19.

**Pre-outcome integrity statement**: no Phase-A/B evaluation outcome exists anywhere in the
repository or mounts as of this freeze (re-verified 2026-08-25); builder WP-0 vendoring has not
begun. This v2 preregistration is therefore constitutionally clean under §19 and charter §3
("pre-outcome architecture revisions are permitted only when no outcome exists anywhere, disclosed
as a delta section naming the sole semantic change").

This document is the binding benchmark contract. The Beta Builder implements it without inventing
essential rules; the Beta Tester/Auditor verifies execution against it clause by clause. **No
Phase-B (evaluation) outcome may exist before the F2 freeze commit (MANIFEST.json F2 section)
lands.** Any later change to panel, prompts, thresholds or baselines quarantines all results as
exploratory and requires a new preregistration version.

Freeze checkpoints (semantics unchanged from v1):
- **F0** = this document set (architect snapshot v2).
- **F1** = build manifest: environment record, backbone model id/version, dependency hashes,
  vendored-file hashes (Graph `d41fe9b` AND Intel `fca0acb` lineages), `panel.json` + paraphrase
  files + prompt templates + seeds — committed BEFORE producer Phase A.
- **F2** = KB dump sha256 + counts, B1 trajectory corpus sha256, route-absence records,
  B2 sanity results, analysis-code hash — committed BEFORE Phase B.

---

## 0. DELTA vs v1 — sole semantic change (disclosed per charter §3)

Directed by `state/product_beta_request.json.directed_pre_outcome_revision_v2`. ONE component of
the SPIDER arm changes; everything else is carried verbatim from v1:

**CHANGED — SPIDER-arm candidate scoring layer.** In the SPIDER arm's memory-led execution model,
the ranking of auto-described fragment candidates is replaced by the audited SGDR-style fused score:

```
score(f) = α·cos(E(goal_text), E(desc_f)) + (1−α)·cos(E(summary(state_t)), E(desc_f))
α = 0.4 · E = lexical-hash embedder (vendored sgdr_repro/embedder.py) ·
desc_f = mechanically derived description (vendored sgdr_repro/descriptions.py) ·
summary(state_t) = deterministic contract-faithful summarizer on the CURRENT observation at
retrieval time (vendored sgdr_repro/summarizer.py; harness-side; cost-counted into SPIDER
wall-clock; zero provider calls) · pool = gate-passing candidates capped top-M = max(3k,20) = 20
by fused score · greedy MMR λ=0.7 · tie-break to lower fragment id.
```

Operationalization frozen (architect decision, disclosed): the goalsig eligibility gates
(matched-pairs ≥ MIN_MATCH=2 ∧ coverage ≥ TAU=0.30, DF-pruning, COV_CAP=6) are RETAINED UNCHANGED
as the OK|UNKNOWN gate; the fused score+MMR replaces only RANKING among gate-passing candidates.
This is the only reading consistent with "degrade to primitives/explore on weak match per unchanged
UNKNOWN thresholds". V31 canonicalization is RETAINED as query preprocessing/equipment. Retrieval
call sites unchanged (one whole-goal retrieval event; no stepwise re-scoring added). NO neural
embedder and NO LLM summarizer may be introduced mid-beta. Clean-room lineage: vendor ONLY from
`intel/experiments/sgdr_repro/` @ lab/intel `fca0acb`; never copy CC BY-SA reference source.

**UNCHANGED (explicit list)**: panel tasks and their anchored predicates with equal disclosure to
all arms; arms B0/B1/B2 definitions and their prompts (Appendix P); budgets/timeouts/retry/
exclusion rules; metrics definitions; WIN rule (Director floor clauses 1–4 + architect tightenings
5–7, verbatim); LOSE clauses; comparator-selection mechanics; scope caps; compute caps; health
gates; write-suppression discipline; producer Phase A corpus; paraphrase authorship discipline;
F1/F2 checkpoint semantics; analysis plan; amendment protocol.

## 1. Hypotheses under test (from the beta request)

| ID | Assumption | Where measured |
|---|---|---|
| A1 | Inheritance benefit survives a real LLM consumer | SPIDER arm end-to-end vs accepted scripted-consumer history; internal contrast vs B0/B1 |
| A2 | Free-form NL goals served end-to-end by the audited fused scorer, without hand-authored goal signatures | R1/R2 raw goal texts → desc_only retrieval with V31 preprocessing and fused state-grounded ranking; keyword channel DISABLED |
| A3 | Packaged procedures beat edge iteration AND prompt-level trajectory memory | SPIDER vs B1 primary; edge-iteration diagnostic ablation slice (outside win rule) |
| A4 | Savings material in tokens/model-calls/wall-clock | per-row usage accounting + perf_counter stage timers (first cost measurement of stack) |
| A5 | Known failure modes contained in scope | R3 control rows, UNKNOWN/false-match ledger, descriptive category-prefix logging |

## 2. Environment — unchanged from v1

- Sites (frozen): `https://books.toscrape.com/`, `https://quotes.toscrape.com/`.
  v1 architect preflight probes 2026-08-25 (GET only): books root 200 / 51294 B; quotes root 200 /
  11064 B; books `/catalogue/page-5.html` 200 / 51829 B; quotes `/page/5/` 200 / 10012 B; quotes
  login form action=`/login` (on-domain). Builder MUST re-run preflight at WP-2 and record byte
  sizes in MANIFEST F1; drift beyond health floors triggers the reserve contingency below.
- Health gate every row entry and reset: HTTP probe floors plus DOM floors (`dom_bytes ≥ 2000`,
  `elements ≥ 5`). Trip ⇒ row INFRA_EXCLUDED symmetrically for all arms.
- Reserve-site contingency: saucedemo.com may be added ONLY if preflight proves the auth/form class
  uncoverable on the two frozen sites (§5.4); disclosed in an F2 amendment BEFORE outcomes.
- Interactions read-only EXCEPT the demo sites' own intended forms (quotes login form; books search
  box). No writes beyond intended form submission.

## 3. Arms (all frozen here; B0/B1/B2 BYTE-IDENTICAL to v1)

Common runtime: one reference ReAct browser agent (ARCHITECTURE.md §1) — identical observation
format, action schema, budgets, decoding (temperature=0, seed=20260825 where supported), and the
anchored acceptance predicate disclosed as part of the task definition to ALL arms. Backbone:
one model id/version pinned at F1, identical across arms. Memory-block budget ≤1800 tokens for
every memory-carrying arm.

### B0 — cold current agent (primary credible baseline)
Same runtime, no memory of any kind. System prompt P0 (Appendix). This is a same-backbone,
same-budget, no-memory ReAct browser agent — the "credible current agent" comparator.

### B1 — trajectory-prompt memory (mandatory stronger comparator)
B0 + top-k=3 prior successful producer trajectories retrieved by lexical overlap over goal text +
site match, rendered via template T-B1 (AWM-class procedural-memory augmentation). Corpus =
the SAME successful Phase-A trajectories that build SPIDER's KB (identical experience, different
packaging). Per constitution §13 this arm is mandatory; win-rule reductions compare against B1
whenever B1's success ≥ B0's (exact tie → B1).

### SPIDER — inherited operational memory (the treatment) — v2 scoring layer
Memory-led execution per ARCHITECTURE.md §5: blind whole-goal retrieval with V31 preprocessing,
frozen goalsig eligibility gate (UNKNOWN discipline unchanged), and the SINGLE CHANGED component —
SGDR-style fused task+current-state-summary ranking (α=0.4, lexical-hash embedder, deterministic
summarizer, pool top-M=max(3k,20), greedy MMR λ=0.7) over the same auto-derived descriptions;
then LLM plan step; procedure application with verification/reset caps (MAX_RESETS=2,
MAX_APPLICATIONS=6); explicit UNKNOWN discipline; residual exploration through the same loop.
All retrieval/planning/summarization overhead counted inside SPIDER totals (zero provider calls
added by the scorer).

### B2 — exact replay sanity (DIAGNOSTIC ONLY, excluded from win rule)
Replay stored procedures verbatim on 4 producer-origin routes (§5.3). Purpose: prove the frozen
KB is functional before outcomes. B2 failing any route ⇒ dependent-class rows MEASUREMENT_INVALID
until repaired; B2 never contributes to WIN/LOSE arithmetic.

## 4. Producer phase (Phase A) — unchanged from v1

Runs ONCE after F1, before any evaluation outcome. Producers = vendored scripted cold-exploration
policies (Graph agentG/agentB lineage, PRODUCER-ONLY code, disabled during evaluation) under the
same health gates. Training corpus (8 tasks):

| task_id | site | subgoals (sigs) |
|---|---|---|
| T_B_cat_fiction_p2 | books | cat.fiction → paginate page-2 |
| T_B_cat_travel_first | books | cat.travel → open first product |
| T_B_cat_mystery_first | books | cat.mystery → open first product |
| T_B_home_page2 | books | home → catalogue page-2 (pager from root entry) |
| T_Q_login | quotes | login form (creds spiderbot/notasecret; predicate Logout visible) |
| T_Q_tag_love | quotes | tag/love navigation |
| T_Q_page2 | quotes | listing page-2 |
| T_Q_page3 | quotes | listing page-3 (pager depth training) |

Fragments auto-described (target-sig slugs + action kinds + post-state URL/title tokens);
producer hints allowed producer-side ONLY. Acceptance: producers solve ≥6/8 tasks live; else
Phase A repeats once after infrastructure repair; second failure ⇒ BLOCKED.

Outputs frozen at F2: KB dump sha256 + table counts; **B1 corpus = the successful training
trajectories rendered** (sha256 recorded); route-absence records for every eval task (adjacent-pair
test generalized + depth-bound assertions: trained pager depths are {books: 2, quotes: 3}; eval
depths 7/5 exceed them).

## 5. Evaluation panel (Phase B) — 10 tasks × 3 arms × 2 passes = 60 rows — unchanged

Row unit = one task × one arm × one pass. Success = harness-judged anchored predicate true on
final state WITH nav-chain integrity (INTERFACES §8.1 registry holds exact anchors).

### 5.1 Panel tasks

| # | task_id | regime | site | start | goal class | anchored completion (summary) |
|---|---|---|---|---|---|---|
| 1 | E_R1_auth_quotes | R1 | quotes | root | login form (repeat) | host∈{quotes.toscrape.com} ∧ Logout visible |
| 2 | E_R1_pag_books_2 | R1 | books | root | pagination depth 2 (repeat) | url anchor `/catalogue/page-2` |
| 3 | E_R1_comp_login_qpage2 | R1 | quotes | root | composite: login → quotes page 2 | Logout visible ∧ `/page/2` anchor |
| 4 | E_R1_tag_love | R1 | quotes | root | tag listing (repeat) | url anchor `/tag/love` |
| 5 | E_R2_pag_books_7 | R2 | books | root | pagination DEPTH SHIFT → 7 | url anchor `/catalogue/page-7` |
| 6 | E_R2_pag_quotes_5 | R2 | quotes | root | pagination DEPTH SHIFT → 5 | url anchor `/page/5` |
| 7 | E_R2_auth_entry_shifted | R2 | quotes | `/tag/love` | ENTRY-STATE SHIFT → login | Logout visible ∧ host constraint |
| 8 | E_R2_comp_fiction_p3 | R2 | books | root | composite SHIFT: fiction cat → its page 3 | `/catalogue/category/books/fiction_10` ∧ `fiction_10/page-3` |
| 9 | E_R3_search_books | R3 | books | root | NOVEL class: site search for named title | product URL segment = title slug ∧ title text present |
| 10 | E_R3_top10_tags | R3 | quotes | root | NOVEL class: top-ten-tags info nav | url anchor `/top10` ∧ list content present |

Exact goal texts, full anchor specs, fills and reserve entries live in `harness/panel.json`
(F1 artifact; hash in MANIFEST). Category appears ONLY as a prefix subgoal inside trained
coverage (tasks 3/8); no category-type goal is a primary endpoint (out-of-scope rule honored);
task 8's category-prefix behavior is logged descriptively for A5.

### 5.2 Paraphrase & authorship discipline — unchanged
R1/R2/R3 goal texts authored by an isolated authoring pass (subagent without file/tool access, no
access to panel construction), committed at F1 BEFORE outcomes, unedited. Limitation disclosed:
same-lab model-family authorship (instructional isolation), matching G-H4 practice; true human
independence not feasible in this pipeline. Texts contain no store keywords/signatures.

### 5.3 Diagnostic rows (excluded from win-rule accounting, disclosed) — unchanged
- **B2 sanity**: replay on T_Q_login, T_B_home_page2, T_Q_page3, T_B_cat_fiction_p2 (4 rows).
- **Pilot smoke** (baseline validity gate): 3 disjoint tasks run by B0 only BEFORE Phase B; B0 must
  solve ≥2/3 else MEASUREMENT_INVALID (batch halted, no outcomes used).
- **Ablation slice**: `memory.mode=edge_iter` on 6 R1+R2 tasks × 1 pass (SPIDER-machinery only).
  Exploratory diagnostics for A3 attribution; NEVER quoted as confirmatory.

### 5.4 Preflight contingency (only pre-outcome) — unchanged
If preflight shows a panel task unstable (predicate unreachable, external hard redirect away from
allowlisted host, structural DOM change breaking anchors), swap that slot with the corresponding
frozen reserve (R1→R-res_tag_life, R2→R-res_books_nf_p2 or R-res_q_p8, R3→R-res_quotes_authors_nav;
auth-class total failure → saucedemo.com login+cart pair with disclosure). Swaps recorded in F2
amendment with reasons. NO swap after first outcome.

## 6. Metrics (exact definitions) — v2 adds descriptive retrieval-internals capture only

Primary (per row; aggregated per arm/regime):
1. `success` ∈ {0,1} — harness-judged predicate + nav-chain integrity. Fabricated success
   (arm-claimed or memory-event-claimed success without predicate truth, or final state not
   produced by recorded action chain) ⇒ row FAILED + violation event.
2. `browser_actions` — primitive executions incl. retries; split novel/reused by source tag
   (`exploration` vs `memory_procedure`/`memory_guided`; uniform across arms).
3. `llm_calls`, `tokens_prompt+completion` — from provider usage fields only.
4. `wall_ms_perf` — perf_counter around the row; stage timers retrieval/llm/browser (float ms;
   SPIDER's retrieval stage includes summarize+embed+MMR CPU time).
5. `reused_action_share` = reused / browser_actions.
Descriptive (no win-rule clause reads these): recovery events after entry-state mismatch (reset
attempts/outcomes); UNKNOWN-discipline events; false-match events (violations when misreported as
memory-solved); **v2**: per-retrieval-event `n_gate_pass`, selected candidates' fused scores,
`alpha_used=0.4`, `mmr_lambda_used=0.7`, `pool_size`, `summary_status ∈ {hit, miss, fallback}`,
accumulated `summary_stats{hits,misses,fallbacks}`.

Consolidation: task-level status = SUCCESS iff SUCCESS in BOTH passes (replication is part of the
claim); costs per task = mean across passes. Report per-pass values alongside.

## 7. Budgets, timeout, retry, exclusions — unchanged

- MAX_STEPS=30 browser actions; MAX_LLM_CALLS=60; MAX_ROW_TOKENS=200,000; WALL_S=600 s per row.
- Action-level retry: 1 on transient browser error. Provider call: 90 s timeout, 1 retry (billed
  both). Malformed output: 1 structured repair attempt (billed).
- Row-level INFRA rerun: ≤1 per cell, HEALTH_TRIP/provider-outage classes only; original preserved
  (`status=RERUN`, replacement carries `rerun_of`). >10% infra-rerun rate ⇒ batch
  MEASUREMENT_INVALID. Two consecutive invalid batches ⇒ kill condition.
- Exclusion ONLY for health-gate trips / infra reruns / provider outage, applied symmetrically;
  performance failures are NEVER excluded. Batch abort if projected compute exceeds caps
  (≤25M tokens, ≤4000 calls total incl. Phase A/diagnostics) — partial artifacts disclosed.

## 8. WIN RULE (binding freeze; Director floor met verbatim and tightened — UNCHANGED from v1)

Comparator selection (mechanical): `CMP` = B1 if median-or-mean success(B1) ≥ success(B0) over full
panel, else B0; exact tie → B1. All reductions are paired per-task relative reductions on R1+R2:
`median over tasks of (CMP_t − S_t)/CMP_t` with pass-averaged costs.

### WIN if ALL (floor clauses 1–4 verbatim from request + architect tightenings 5–7):
1. success_SPIDER ≥ success_CMP − 0.10 absolute on the FULL panel including R3 rows
   (row-level rates, n=30/arm; task-level reported alongside);
2. on R1+R2 rows: median browser-action reduction ≥ 50% AND median total-token reduction ≥ 40%
   AND median wall-clock reduction ≥ 30% versus CMP (paired medians — stricter than ratio-of-medians);
3. zero fabricated-success events in the SPIDER arm;
4. results replicate across two deterministic passes where the environment is static
   (operationalized: per-cell success equality across passes for ALL three arms; drift-caused
   mismatches excluded symmetrically via health records and disclosed);
5. *(tightening)* SPIDER R3 success ≥ B0 R3 success − 1 row out of 4 (graceful degradation explicit);
6. *(tightening)* reused-action share ≥ 50% of SPIDER's actions on R1+R2 rows it solves via memory;
7. *(tightening)* write-suppression assertion green for every reported row.

### LOSE if ANY (floor clauses verbatim, operationalized):
1. SPIDER fails > 25% of tasks solved by the best baseline (task-consolidated statuses; with n=10:
   ≥3 CMP-solved tasks unsolved by SPIDER);
2. median reductions < 20% on R1+R2 versus the same CMP (any of actions/tokens/wall-clock);
3. any memory-induced fabricated success.

Verdict mapping: all WIN clauses pass ⇒ BEATS_BASELINE; any LOSE clause fires ⇒ LOSES; otherwise
PARITY (clauses near-miss documented) or INCONCLUSIVE/MEASUREMENT_INVALID per audit. Reporting
duty: ALL regimes, ALL arms including losses; negative outcome is a valid product result feeding
the PH-1 disposition.

## 9. Analysis plan (frozen) — unchanged

`analysis/compute_verdict.py` (hash pinned at F2) computes aggregates, paired reductions, win-rule
clause booleans, verdict; deterministic; recomputable from raw_rows.jsonl + events. The
Tester/Auditor independently recomputes headline numbers from raw artifacts. Uncertainty: n is
small by design (scope cap); NO sampling-based significance is claimed; replication is the
flake-guard, stated honestly. Claim-strength ceiling for a WIN: ROBUST-RESULT candidate within the
preregistered scope only (two demo sites, one backbone family, internal harness) — never
generalization language. All Intel-gate wording constraints (OPTIMIZATION_RATIONALE §7 register)
bind every narrative built on these rows.

## 10. Discipline rules — unchanged

UNKNOWN stays UNKNOWN: retrieval returning no gate-passing candidate must log `unknown` and proceed
by exploration; filling gaps from ground truth forbidden. Zero fabricated successes tolerated in
any arm for reporting integrity; in SPIDER they additionally fire LOSE clause 3. Store hygiene: KB
byte-restored per row; evaluation writes nothing (asserted per row; distinct-before-hash check
across runs like G-H3/G-H4 discipline proofs).

## 11. Amendment protocol — unchanged

Pre-outcome amendments (measurement fixes only) allowed with an explicit disclosure section
appended here and committed BEFORE outcomes; no threshold/token/task/arm semantic changes.
Post-outcome: nothing in §§3–8 may change; new claims require new preregistration + untouched
evidence.

## Appendix P — frozen prompt templates (verbatim; hash recorded at F1) — UNCHANGED from v1

**P0 (B0 system prompt):**
```
You are a careful web automation agent. Each turn you receive the current page state:
URL, title, a numbered list of interactive elements, and a text excerpt. Your job: complete
the user's GOAL using the primitive actions. Respond ONLY with JSON:
{"thought": "<brief plan>", "action": "click|fill|select|press|goto|wait|done",
 "element": <index>, "value": "<text if needed>"}
Rules: prefer minimal actions; verify effects from the next observation; call "done" only
when the GOAL's stated completion condition visibly holds on the page. Never invent elements.
```
GOAL message = task.goal_text + start URL + credential lines when the task provides them + the
sentence: "Completion condition (machine-checked after your run): <predicate description in natural
language>." — IDENTICAL wording injected for every arm.

**P-B1 addition (trajectory memory block, ≤1800 tokens total):**
```
Relevant past successful runs on this site (may help; verify against the live page):
[Trajectory k] Goal: <training goal text> | Start: <url>
 Steps: 1. click <element descriptor> 2. fill <field> = <value> ... Outcome: reached <anchor>
```

**P-SPIDER additions:** memory block renders retrieved candidates as auto-derived descriptions
(vendored mechanical derivation text) + step sketches + provenance counters (never goal_sig IDs as
lookup keys); planner JSON schema: `{"plan": [{"use_candidate": <id|null>, "subgoal_text":
"<free text>", "mode": "procedure|explore"}], "rationale": "<brief>"}`; executor messages fixed;
UNKNOWN block text: "No stored procedure cleared the matching threshold for this part; explore it
yourself."

*(Full byte-exact templates ship as `runtime/prompts/*.txt` at F1; hashes in MANIFEST; the above
fixes their semantic content and length bounds.)*
