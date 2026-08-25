# SPIDER PRODUCT ARCHITECTURE HYPOTHESES

Conceptual combinations of AUDITED technical building blocks.

Statuses: WATCH / PROMISING / PRODUCT_CANDIDATE / REJECTED.
PRODUCT_CANDIDATE authorizes at most an internal benchmarkable beta; it
never authorizes public deployment or commercialization.

Last updated: 2026-08-25 (third session on mounted accepted snapshots:
evidence basis unchanged — Graph through Run 32783797303 audit PASS;
Physics through WP-005 audit PASS; Intel through cycle-1 integration —
SGDR state-grounded retrieval VALIDATED_USEFUL, PoC ceiling, audit run
32800296360; no beta outcomes exist anywhere).

---

## PH-1 — Inherited operational memory layer for repeat/near-repeat web tasks — **PRODUCT_CANDIDATE (Beta PB-001 re-authorized, request rev 3)**

- **User problem**: Browser agents re-pay full exploration cost (actions,
  model calls, tokens, latency, flaky retries) every run, even when the
  task is a repeat or near-repeat of something some agent already solved
  (same login flow, same pagination drill, same form path with shifted
  parameters or reworded goal).
- **Validated building blocks (source)**: cumulative store with
  provenance/confidence + exact replay + entry-state reset (G-H1);
  blind content-addressed fragment retrieval with expected-UNKNOWN
  discipline (G-H2); oracle-equalized iterative replay policy (G-H2/G-H3
  E2); multi-step login procedure packaging as first-class reusable unit
  (G-H3 E2, G-H4 R3); V31 closed-class descriptor/query equipment
  (G-H4) used AS EQUIPMENT ONLY; SGDR-style fused task+current-state-summary
  candidate scoring for free-form goals in the NL-consumer regime
  (Intel cycle-1 clean-room reproduction, PoC ceiling — lexical-hash
  embedder + deterministic summarizer configuration only; binding wording
  constraints from audit gate 32800296360 travel with every use).
- **Unvalidated assumptions**: inheritance survives a real LLM consumer
  (all accepted results are scripted deterministic consumers); fused
  addressing serves free-form natural-language goals END-TO-END in the
  product loop (audited only at PoC scale inside an isolated harness;
  embedder/summarizer/scale adaptations untested); savings are material
  in tokens/model-calls/wall-clock; known failure modes (category goals,
  deep >3-fragment chains, cross-site) stay contained inside the declared
  scope.
- **Expected operational benefit**: on repeat/near-repeat tasks, large
  reductions in browser actions, model calls/tokens and latency at
  non-inferior success; reused-action share dominating the action mix.
- **Nearest competitors**: plain current browser agents (no memory);
  trajectory/workflow-memory systems (AWM-class retrieval augmentation);
  selector caches (Stagehand-class); workflow RPA replay (Skyvern-class).
- **Differentiation (bounded hypothesis, not a novelty claim)**:
  subgoal-addressable EXECUTABLE fragments with empirical validation
  statistics, provenance and freshness metadata consumed by an external
  model-agnostic layer — the combination was not identified among the
  systems inspected in Run 1; the externally-sourced addressing layer is
  now independently validated rather than home-grown.
- **Conceptual architecture**: producer runs grow a validated store →
  fused task+state-summary candidate scoring over auto-derived
  descriptions (V31 canonicalization as preprocessing) selects fragments/
  procedures for subgoals of the free-form goal → consumer LLM executes
  memory-led with exploration fallback and explicit UNKNOWN reporting →
  anchored completion predicate equalized across arms → outcomes written
  back with provenance (calibration deferred).
- **Biggest uncertainty**: whether the scripted-setup advantage survives
  contact with an actual LLM in the loop without inflating errors
  (memory-induced wrong actions, stale-fragment traps).
- **Evidence needed**: Beta PB-001 outcome vs B0 cold-agent and B1
  trajectory-RAG baselines under preregistered win rule.
- **Status**: PRODUCT_CANDIDATE. Beta request rev 3:
  `state/product_beta_request.json` (PB-001, single authorized beta).
  Rev-3 note: provenance-only bump after a second uncommitted working-tree
  reset (request deleted, beta_launch flipped false) — zero substantive
  clause deltas vs rev 2, evidence basis independently re-verified against
  the mounted snapshots, no beta outcome exists anywhere. The v2 architect
  freeze obligation stands: BENCHMARK_PREREG v2 must swap SPIDER-arm
  candidate scoring to the audited fused mechanism (everything else frozen
  unchanged) BEFORE any outcome.

## PH-2 — Shared capability infrastructure line (Steam-like) — **WATCH**

- **User problem**: many agents/teams independently re-explore the same
  sites; a registry through which agents discover, inherit, verify,
  version and possibly share reusable Web capabilities could amortize
  exploration across teams/models.
- **Mechanisms to evaluate as product mechanisms (NOT assumptions)**:
  discovery, semantic addressing, provenance, trust, scoring,
  freshness/decay, versioning, incentives, cross-model compatibility,
  permissions/auth, route invalidation.
- **Why WATCH**: exactly ONE Intel mechanism is validated (addressing-layer,
  PoC tier) and it is already allocated to PH-1's front door. The
  execution-substrate and registry layer remains unvalidated: the closest
  precedent (Unbrowse browser→first-party-API route capture/replay + shared
  ladder/registry) carries vendor-run headline claims (OFFICIAL_CLAIM only)
  and is Intel cycle-2's selected reproduction mission — no independent
  verdict exists. Registry design constraints already evidenced but not
  productized: ecosystem versioning is weak (content-addressing would be
  load-bearing); contributed procedures must be treated as untrusted input
  by default (documented injection threat model). Internal
  confidence/staleness remain UNCALIBRATED (G8/G9 open); cross-model
  consumption untested (G10 open). Nothing here may enter PB-001.
- **Path to PROMISING**: Intel cycle-2 independent reproduction verdict on
  Unbrowse-style route capture/replay (either direction is informative);
  G8/G9 calibration evidence; any cross-model consumption result.
- **Status**: WATCH.

## PH-3 — Predictive Web-dynamics routing ("physics-powered" navigation) — **REJECTED**

- **Claim that would be needed**: transferable action-conditioned
  environment regularity usable to predict/route transformations across
  sites beyond memory and similarity.
- **Evidence against (audited)**: Physics WP-003B-R2 FALSIFIED (mean D
  −0.5016, 0/5 adequate folds, site holdout) and WP-005 FALSIFIED at fine
  granularity (T1 wins 1/9 p=0.898; T2 wins 4/9 p=0.270); apparent
  predictability = persistence + site-local NN retrieval + generic
  action-type semantics. WP-004 committor work BLOCKED pending
  identifiability.
- **Disposition**: no product work builds on predictive dynamics. A
  genuinely new instrument (deliberate restart/matched-state designs,
  Physics WP-006 direction) producing a positive would be required to
  reopen this narrowly.
- **Status**: REJECTED.

## PH-4 — Selector self-healing / staleness product — **WATCH**

- **User problem**: agents break when site structure drifts; selectors
  need repair/revalidation (Healenium-adjacent space).
- **SPIDER angle**: store-level failure events + provenance + freshness
  could drive revalidation and localized re-exploration instead of
  silent failure (entry-reset mechanism is adjacent, audited as recovery
  POC only).
- **Why WATCH**: staleness/confidence UNCALIBRATED; no audited experiment
  demonstrates repair value over retry/TTL heuristics; competitor space
  established (Healenium). Needs an audited staleness-calibration or
  recovery-value result before any candidate status.
- **Status**: WATCH.

---

## Combination rules observed

- Only audited blocks combine into candidates (currently: PH-1 only).
- Physics negatives forbid any PH-1 marketing/feature language implying
  prediction or cross-site generalization.
- Intel SGDR wording constraints bind all downstream use: PoC tier only;
  advantage exists exactly and only vs task-text-only retrieval in the
  natural-language-consumer regime; exact hand-authored signatures stay
  more action-efficient where they exist; no login/pager-improvement
  claims; no WebArena headline numbers anywhere (never reproduced).
  GENERALIZATION language is forbidden at this tier.
- Any quantitative addressing claim inside a product report requires a
  third independently authored instrument (G-H4 spent-instrument rule).
- Unbrowse-style route/API replay features are FORBIDDEN in any beta or
  product narrative until Intel cycle-2 produces an independent verdict;
  vendor-run speedup claims may never be cited as SPIDER evidence.
