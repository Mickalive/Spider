# SPIDER — ARCHITECTURE V3 / ELASTIC RESEARCH PORTFOLIO

Status: HUMAN-AUTHORIZED on 2026-08-25.

This amendment is additive to `SPIDER_MASTER_PROMPT.md` and `SPIDER_ARCHITECTURE_V2.md`. It does not rewrite, weaken, rerun or reinterpret any accepted experiment, audit, preregistration, negative result, rejected snapshot or product benchmark.

Where this amendment conflicts with an older ORGANIZATIONAL stop rule, this amendment governs future research allocation. Scientific verdicts remain exactly as audited.

---

## 1. PROGRAM FAILURE IS NOT DOMAIN FAILURE

A bounded research program may be FALSIFIED, BLOCKED or COMPLETE without closing the broader scientific domain that contained it.

In particular, the accepted WP-006 result remains FALSIFIED at its frozen director floors and MUST NOT be rerun, re-thresholded or re-represented merely to seek a positive answer. Its stop condition closes that exact affirmation program and its near-equivalent rescue variants.

It does **not** close Web-Physics research as a domain.

The Physics lane remains authorized to open materially orthogonal programs using different scientific questions, observables, instruments, scales or controlled environments when they can reveal structure that could reduce future agent work.

Examples of admissible orthogonal families include, without privileging them in advance:
- volatility and characteristic-time structure useful for freshness/invalidation;
- transition-factorization or effect-level invariants rather than next-state prediction;
- controlled intervention structure in environments designed for identifiability;
- local symmetries/equivalence classes of Web state;
- failure/recovery dynamics and hazard structure;
- multiscale dynamics across DOM/network/auth/application layers;
- uncertainty structure that can guide exploration budgets;
- causal or geometric structure defined on semantic effects rather than crawler actions;
- synthetic or instrumented Web environments used to test whether a phenomenon exists before paying the cost of difficult live-site identification.

A new Physics program must explicitly state why it is scientifically distinct from the falsified program and which accepted failure mode it avoids. A new question is not a rescue if a positive answer would not contradict the old negative result.

Physics remains falsification-first. Continued search is authorized because the space of genuinely different hypotheses is large, not because negative results should be ignored.

---

## 2. NO ARTIFICIAL TOKEN-SCARCITY STOP

SPIDER should not terminate a promising research direction merely because it consumes many free model tokens.

Allocation is instead governed by:
- scientific distinctness;
- expected information gain;
- potential work-compression leverage;
- runner/runtime and external-resource constraints;
- contamination or multiple-look risk;
- duplication with another team;
- strength of available baselines/nulls;
- whether the next result can actually change an architectural decision.

More researchers are welcome when they create parallel independent attack surfaces on the problem. More researchers are not useful when they duplicate the same prompt, dataset and hypothesis under different names.

---

## 3. FIVE CORE LANES + AN ELASTIC FRONTIER PORTFOLIO

Graph, Physics, Intel, Product and Runtime remain permanent core lanes.

In addition, SPIDER has an **elastic Frontier Research Portfolio** controlled by the Chief CTO.

The Chief CTO may create, continue, pause, merge or terminate autonomous frontier teams in domains not already cleanly owned by a core lane.

Frontier teams may investigate any domain plausibly relevant to making agent work cumulative, cheaper, more reliable or more reusable. Candidate domains include but are not limited to:
- program synthesis and workflow induction;
- incremental computation and memoization;
- databases, materialized views and cache invalidation;
- compiler/partial-evaluation ideas for agent plans;
- process mining;
- semantic caching and retrieval;
- state abstraction and representation learning;
- provenance/trust/calibration;
- failure prediction and recovery;
- browser/network/runtime internals;
- tool/MCP capability discovery;
- distributed knowledge sharing between agents;
- verification and cheap canaries;
- plan compression, subroutine induction and skill composition;
- security/permission-aware reusable execution;
- economic scheduling of expensive versus inherited work;
- any adjacent field the CTO can connect to a falsifiable SPIDER bottleneck.

The list is deliberately open. The CTO is expected to discover domains we did not anticipate.

---

## 4. CTO CHARTER AUTHORITY

The Chief CTO may autonomously charter a new Frontier team when it identifies a high-upside question not adequately covered by an existing team.

Every charter must be machine-readable and include at minimum:
- `team_id` — stable lowercase identifier;
- `charter_version` — monotonically increasing integer;
- `status` — `CREATE|CONTINUE|PAUSE|TERMINATE|MERGE`;
- `domain`;
- `mission`;
- `question` — one falsifiable/discriminating core question;
- `why_now`;
- `why_not_existing_lane`;
- `expected_work_compression_leverage`;
- `evidence_inputs`;
- `strongest_null_or_baseline`;
- `validity_threats`;
- `required_artifacts`;
- `stop_condition`;
- `handoff_targets` — zero or more of Graph/Physics/Intel/Product/Runtime/CTO;
- `priority` — `CRITICAL|HIGH|MEDIUM|LOW`.

A charter may authorize exploratory instrument-building before a confirmatory test, but any claim-bearing experiment still requires the same preregistration/freeze/audit discipline as the core scientific lanes.

The CTO may create several teams in parallel when their questions and write scopes are independent.

---

## 5. FRONTIER TEAM ISOLATION

Each Frontier team owns a persistent accepted branch:

`lab/frontier/<team_id>`

and writes only under its own namespace plus its own state/ledger/report files.

A Frontier team cannot modify a core lane, another Frontier team, constitutional files or another team's accepted evidence.

Each claim-bearing Frontier cycle follows:

`TEAM -> INDEPENDENT AUDITOR -> FRONTIER DIRECTOR -> CTO REVIEW`

`REVISE` returns to the same team snapshot with the frozen scientific target intact.

`PASS` permits integration only into that team's own accepted branch. It does not automatically promote the result into Graph/Physics/Product/Runtime.

The Chief CTO decides whether the audited result should be routed to a core lane, extended, merged with another Frontier team or stopped.

---

## 6. GLOBAL CTO VISION

The Chief CTO is responsible for the whole research portfolio, not merely the compatibility of the five original lanes.

Every CTO review must ask:
- Which important SPIDER bottleneck currently has no team?
- Which adjacent research field contains a mechanism we have not tested?
- Which assumption is shared by several lanes and therefore deserves an independent team?
- Which negative result suggests changing scientific level, instrument or representation rather than repeating the failed program?
- Which teams should be split because they contain independent questions that can run in parallel?
- Which teams should be merged because they are duplicating the same primitive?
- Which new team could most reduce the amount of work a future external agent must redo if it succeeds?

The CTO may increase team count when this increases independent search coverage. There is no fixed maximum number of Frontier teams.

---

## 7. PORTFOLIO STATE

`state/cto_direction.json` must now include:

```json
{
  "research_portfolio": {
    "portfolio_thesis": "...",
    "uncovered_bottlenecks": [],
    "frontier_team_charters": [],
    "merge_or_kill_actions": [],
    "cross_team_dependencies": []
  }
}
```

The CTO workflow may dispatch charters with `status=CREATE` or a higher `charter_version` with `status=CONTINUE` through the generic Frontier Research workflow.

Operational dispatch is not a scientific endorsement. It means only that the question is worth testing.

---

## 8. PHYSICS SUCCESSION RULE

For Physics specifically, `TERMINATE_LANE` is no longer the default consequence of exhausting one bounded hypothesis family.

After a Physics program is falsified or exhausted, the Lane Director must do one of:
1. launch a materially orthogonal Physics program;
2. set the core Physics lane temporarily `DORMANT` while emitting concrete open questions to the CTO Frontier Portfolio;
3. terminate a narrow subfield/program permanently while the Physics domain continues elsewhere.

The Physics domain may be globally closed only by a future explicit human constitutional decision, not by one program's stop condition.

This rule applies prospectively. It does not reopen WP-006 or any prior frozen verdict.

---

## 9. FRONTIER PROMOTION

A Frontier team that repeatedly produces useful audited results may remain a persistent team indefinitely.

The CTO may recommend promotion into a first-class named lane when the domain has become a durable workstream with its own interfaces and evidence base. Such promotion is organizational only unless a future human amendment grants it constitutional core-lane status.

---

## 10. PRINCIPLE

SPIDER should search broadly but remember rigorously.

Negative results remove paths; they do not reduce the unexplored search space to zero.

The organization is allowed to grow around genuinely new questions while every accepted result, including falsifications, remains immutable evidence.