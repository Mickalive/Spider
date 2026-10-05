# Preregistration: EXP-INTEL-36314207239

## 1. Experiment Identity

- **experiment_id**: EXP-INTEL-36314207239
- **lane**: intel
- **claim_ids**: ["C-PRODUCT-ECON"]
- **director_mandate**: Global Research Director CONTINUE on C-PRODUCT-ECON with cognitive reset. Binding strategic question in request.json director_mandate.question.
- **parent_handoff**: EXP-INTEL-36306525220 (MEASUREMENT_INVALID — frozen corpus defect, wrong construct population, identity gate repaired)

## 2. Question

**Primary (Part A)**: Using the validated identity-before-scoring instrument (4-condition conjunction) from EXP-INTEL-36306525220: which PUBLISHED web-agent systems actually persist state across sessions or episodes, and does ANY report a cost quantity carrying a denominator, an accounting convention, a stated uncertainty, and specifically a MEASURED break-even reuse count f*?

**Secondary, bounded and separately scored (Part B)**: Does any published system report a MEASURED stationarity metric for the state it carries?

## 3. Hypothesis

- **H_A**: At least one published web-agent system that persists state across sessions/episodes reports a measured break-even reuse count f* with denominator, accounting convention, and stated uncertainty.
- **H_B**: At least one such system reports a measured stationarity metric for its persistent state.

## 4. Falsifier

- **F_A**: After exhaustive construction-seeded search (PC bibliography seeds + 3 external systems + 1 bounded 1-hop snowball via Semantic Scholar author-title-year), zero candidates satisfy the identity conjunction AND report a measured f* with denominator/convention/uncertainty.
- **F_B**: Zero candidates report a measured stationarity metric.

## 5. Construct Population — Built by Construction, Not Name Recall

The candidate set is **frozen at design time** and built exclusively from:

### 5.1 Seed Set (5 entries)

| # | Name | Authors | Year | Source |
|---|------|---------|------|--------|
| 1 | Agent workflow memory | Wang, Mao, Fried, Neubig | 2024 | PC bibliography (arXiv:2608.05784v1 references) |
| 2 | Position: Episodic memory is the missing piece for long-term LLM agents | Pink et al. | 2025 | PC bibliography (arXiv:2608.05784v1 references) |
| 3 | Agent Workflow Memory | Wang, Mao, Fried, Neubig | 2024 | External systems from last packet (result.json coverage_summary.systems_not_in_frozen_list) |
| 4 | WebCoach | — | — | External systems from last packet |
| 5 | ReasoningBank | — | — | External systems from last packet |

### 5.2 Snowball (exactly ONE bounded 1-hop)

- **Source**: References cited in PC-COST-ACCOUNTING (arXiv:2608.05784v1)
- **Resolution method**: Author-title-year against Semantic Scholar Graph API (`https://api.semanticscholar.org/graph/v1/paper/search`)
- **Parameters**: `fields=paperId,title,authors,year,venue,abstract,references,citations`, `limit=20`
- **Maximum candidates**: 20
- **Frozen at design**: The exact query parameters and max_candidates are frozen. No iterative or fuzzy expansion.

### 5.3 Explicitly Excluded (14 entries from EXP-INTEL-36306525220 frozen list)

The following are **benchmarks or environments**, not persistent-state agents. They are NOT carried forward:

- WebShop (2207.01206v4)
- Mind2Web (2306.06070v3)
- WebVoyager (2401.13919v4)
- WebArena (2307.13854v3)
- AgentBench (2308.03688v2)
- BrowserGym (2401.15378) — **wrong identifier** (resolves to Islamic QA system)
- MiniWoB++ (1802.08827) — **wrong identifier** (resolves to spin chains)
- SeeAct (2402.04566) — **wrong identifier** (resolves to radiotherapy dose prediction)
- Crux (2406.01234) — placeholder (resolves to average-reward MDPs)
- WebAgent (2403.01234) — placeholder (resolves to molecular functionalities)
- RULER (2405.01234) — placeholder (resolves to Hermite rings)
- WebCanvas (2407.01234) — placeholder (resolves to power-storage optimal control)
- BrowserBench (2408.01234) — placeholder (resolves to quantum entanglement routing)

**No post-hoc repair** of the 3 wrong identifiers. They remain excluded.

## 6. Identity-Before-Scoring Instrument (Validated)

The resolver from EXP-INTEL-36306525220 is reused **unchanged** except for the PC-COST-ACCOUNTING `expected_authors` correction (from `['TBD']` to `['Iyamu', 'Nossa']`).

### 6.1 Four-Condition Conjunction (ALL must pass)

| Condition | Specification | Pass Criterion |
|-----------|---------------|----------------|
| **C1** Exact base_id | Exact arXiv base ID match (e.g., `2608.05784`) | Exact string match |
| **C2** Title substring + coverage | Case-insensitive expected token coverage >= 0.85 (Director ruling: **substring + coverage**, NOT full-token-set Jaccard) | `coverage >= 0.85` |
| **C3** Author substring | At least one expected author surname substring match in returned author list | `any(expected in returned for expected in expected_authors)` |
| **C4** Domain keywords | At least 4 of 6 domain keywords present in title+abstract | `count >= 4` |

### 6.2 Identity Outcomes

- **All 4 pass** → `RESOLVED` (proceed to field extraction)
- **Any fail** → `AMBIGUOUS` → `UNMEASURED` (record reason: `C2_title_mismatch`, `C3_author_mismatch`, etc.)
- **Never** → `NOT_FOUND` (validated: 0/38 rows in parent)

### 6.3 Frozen Target List (Controls Only)

| Role | base_id | version | expected_title | expected_authors | expected_token_coverage | domain_keywords (6) |
|------|---------|---------|----------------|------------------|------------------------|---------------------|
| PC-COST-ACCOUNTING | 2608.05784 | v1 | Activity Frames: Deterministic Screen-Activity Compilation for Agent Memory and Replay | ["Iyamu", "Nossa"] | 1.0 | ["agent", "memory", "replay", "screen", "activity", "deterministic"] |
| NC-REAL-BUT-WRONG | 1802.05012 | v2 | Getting out of the closet: Scientific authorship of literary fiction and knowledge transfer | ["Azagra-Caro"] | 0.0 | ["agent", "memory", "web", "browser", "automation", "llm"] |

**Note**: The 5 seed candidates and up to 20 snowball candidates are resolved using the same conjunction but are **not frozen in spec.json** — they are discovered at execution time via the construction procedure. Only the two controls are frozen targets.

## 7. Controls

### 7.1 Positive Control: PC-COST-ACCOUNTING

- **Target**: arXiv:2608.05784v1 (Activity Frames)
- **Validates**: Field-extraction pipeline works when identity gate passes
- **Expected identity outcome**: `RESOLVED` (all 4 conditions pass)
- **Expected field determinations** (verbatim quotes required):
  - `break_even_reuse_count_fstar`: `NOT_REPORTED_AS_A_COMPUTED_QUANTITY` (0 pattern hits over 69,607 chars for: break-even, breakeven, break even reuse, reuse count, payback, amortization point, f*)
  - `real_cost_advantage_persistence`: `no_measured_real_cost_advantage` (paper states "modeled from measured artifacts and token counts, not billed"; "full live three-arm billing with real usage JSON remains reserved")
  - `staleness_forgetting_maintenance_cost`: `NOT_REPORTED_AS_A_QUANTIFIED_COST`
  - `modeled_vs_measured`: `modeled_explicitly_stated`

### 7.2 Null Control: NC-REAL-BUT-WRONG

- **Target**: arXiv:1802.05012v2 (literary fiction authorship, 2018)
- **Validates**: Specificity of 4-condition conjunction (C4 alone would pass due to 'agent' token)
- **Expected identity outcome**: `UNMEASURED` (fails C2 and/or C3)
- **Pass criterion**: Resolver records `pass=null` with reason containing `C2_title_mismatch` or `C3_author_mismatch`; `resolution_status=UNMEASURED`; **never** `NOT_FOUND`.

### 7.3 Baselines

- **B-PUBLISHED-NUMBERS-ONLY**: Read-only extraction from published artifacts (same as parent prereg §10). No reproduction, no SPIDER measurements.
- **B-NULL-FUZZY-RECALL**: Name-recall fuzzy queries (Google Scholar: "persistent state web agent", "cross-episode memory agent", "break-even reuse count agent") — expected to retrieve irrelevant/noisy results. Serves as negative control for construction-vs-recall comparison.

## 8. Field Extraction Schema (Per RESOLVED Candidate)

For each candidate that passes the identity conjunction, extract **verbatim quotes** for:

| Field | Type | Evidence Required | Inference Rule |
|-------|------|-------------------|----------------|
| `persists_state_across_sessions` | enum: yes/no/UNKNOWN | Verbatim quote | **Never from keywords alone** |
| `cost_quantity_denominator` | string | Verbatim quote | e.g., per_task, per_episode, per_token, per_dollar |
| `cost_quantity_accounting_convention` | string | Verbatim quote | e.g., modeled_from_measured_artifacts, billed_usage_json, wall_clock_seconds |
| `cost_quantity_stated_uncertainty` | string | Verbatim quote | e.g., CI_95%, IQR, std_dev, NOT_STATED |
| `break_even_reuse_count_fstar` | string | Verbatim quote OR full-text pattern sweep | Values: numeric_value, NOT_REPORTED_AS_A_COMPUTED_QUANTITY, SYMBOLIC_ONLY |
| `modeled_vs_measured` | enum: modeled/measured/unknown | Verbatim quote | Paper's own characterization |
| `stationarity_metric` | string | Verbatim quote | Values: numeric_with_denominator_convention_uncertainty, NOT_REPORTED, SYMBOLIC_ONLY |

**Absence determination ceiling**: "Absent from retrieved text" over named character count. PDF text-layer loss (ligatures, de-hyphenation, non-linearized tables) bounds every absence.

## 9. Coverage Reporting

Report **exactly** these counts (no proxy metrics):

- `n_candidates_searched` (seeds + snowball)
- `n_resolved` (identity conjunction passed)
- `n_persisting_state_yes`
- `n_persisting_state_no`
- `n_persisting_state_unknown`
- `n_reporting_fstar_measured` (with denominator + convention + uncertainty)
- `n_reporting_stationarity_measured` (with denominator + convention + uncertainty)
- Snowball coverage: `papers_examined`, `papers_resolved`
- Seed coverage: `seeds_examined`, `seeds_resolved`

**Never** report `identity_resolution_recall` as construct-population proxy (rejected in parent handoff).

## 10. Substrate

- **HTTP only**: Python stdlib (`urllib`) or `requests`. No browser, no Docker, no model credentials.
- **arXiv**: `https://arxiv.org/abs/<id>` (HTTP 200 verified; Atom API returned 406 on parent run)
- **Semantic Scholar Graph API**: `https://api.semanticscholar.org/graph/v1` (HTTP 200 verified on parent substrate probe)
- **PDF/text extraction**: `arxiv.org/pdf/<id>.pdf` or HTML from abs page

## 11. Decision Rules (Frozen)

### Part A (Primary)

| Outcome | Rule |
|---------|------|
| **SUPPORTS** | ≥1 RESOLVED candidate with `persists_state_across_sessions=yes` AND `break_even_reuse_count_fstar` = measured numeric value WITH explicit denominator, accounting convention, and stated uncertainty |
| **FALSIFIES** | 0 RESOLVED candidates with `persists_state_across_sessions=yes` AND measured f* with denominator/convention/uncertainty |
| **INCONCLUSIVE** | ≥1 RESOLVED candidate with `persists_state_across_sessions=yes` but f* = `NOT_REPORTED_AS_A_COMPUTED_QUANTITY` or `SYMBOLIC_ONLY` (or modeled only), AND no SUPPORTS |
| **MEASUREMENT_INVALID** | PC-COST-ACCOUNTING fails identity OR field extraction; OR NC-REAL-BUT-WRONG resolves to RESOLVED or emits NOT_FOUND; OR >50% substrate probes fail |

### Part B (Stationarity — Separately Scored)

| Outcome | Rule |
|---------|------|
| **SUPPORTS** | ≥1 RESOLVED candidate with `persists_state_across_sessions=yes` AND `stationarity_metric` = measured numeric with denominator/convention/uncertainty |
| **FALSIFIES** | 0 such candidates |
| **INCONCLUSIVE** | ≥1 RESOLVED with `persists_state_across_sessions=yes` but stationarity NOT_REPORTED or SYMBOLIC_ONLY |
| **MEASUREMENT_INVALID** | Same as Part A (shared identity gate and substrate) |

### Overall Experiment Status

- `MEASUREMENT_INVALID` if either part is MEASUREMENT_INVALID
- `COMPLETE` otherwise, with per-part outcomes recorded separately

## 12. Product Consequences

### Positive (SUPPORTS)

- **Part A**: External corroboration that SPIDER's cross-episode persistence premise has measured economic precedent. Product can anchor C-PRODUCT-ECON's next_gate (`end-to-end amortized economics on real agents`) to a published f* benchmark.
- **Part B**: External evidence that stationarity measurement is a reporting practice, informing Runtime's freshness guard design (C-FRESHNESS).

### Negative (FALSIFIES)

- **Part A**: The field has no measured break-even reuse count — SPIDER's premise is economically unprecedented. Product must generate its own f* internally via first-party measurement.
- **Part B**: Stationarity reporting absent; Runtime must invent freshness metrics without external anchor.

### Inconclusive

Question remains open. Next cycle may widen snowball (2-hop), change seeds, or pivot substrate — but **only with new Global Research Director mandate**.

## 13. Validity Threats (Pre-Declared)

| Threat | Mitigation |
|--------|------------|
| PDF text-layer loss (ligatures, tables, hyphenation) | Absence ceiling = "absent from retrieved text" over named char count; report char count per artifact |
| Semantic Scholar API rate limits / schema changes | Frozen query params; max 20 candidates; cache responses with sha256 |
| Seed candidates may not have arXiv IDs | Resolution by author-title-year via Semantic Scholar (same as snowball) |
| "Persists state" may be described implicitly | **Never infer from keywords**; require verbatim quote or explicit statement |
| Modeled vs measured ambiguity | Require paper's own characterization; if absent, code `unknown` |
| Snowball may retrieve non-agent papers | Identity conjunction filters; domain keywords require 4/6 match |
| Single snowball hop may miss key literature | Bounded by design; Director mandate specifies "exactly ONE bounded 1-hop" |

## 14. Scope Boundaries (From Parent Prereg §10, Retained)

- **Excluded**: Reproduction of published numbers; SPIDER's own measurements; WebArena/Docker; browser automation; compiler/regime extraction; C-CROSSSITE four-part transfer.
- **Included**: Read-only literature verification on the construction-seeded population only.

## 15. Artifact Commitment

All raw evidence preserved with sha256:
- `raw/identity_resolution.json` — per-candidate C1/C2/C3/C4 sub-checks
- `raw/field_determinations.json` — verbatim quotes for all 7 fields per RESOLVED candidate
- `raw/controls_result.json` — PC and NC outcomes with pass/fail/reason
- `raw/snowball_candidates.json` — Semantic Scholar API responses
- `results/table.json` — machine-checkable table with integrity self-checks
- `results/coverage.json` — coverage summary per §9
- `provenance.json` — commits, environment, artifact index with hashes

## 16. Binding Inheritance from Parent Handoff

The following are **frozen and non-negotiable** for this experiment:

1. **Identity instrument is validated** — do not modify the 4-condition conjunction.
2. **PC-COST-ACCOUNTING expected_authors corrected** to `["Iyamu", "Nossa"]` (was `['TBD']`).
3. **14 frozen benchmarks excluded** — they are environments, not persistent-state agents.
4. **3 wrong identifiers excluded** — no post-hoc repair (BrowserGym, MiniWoB++, SeeAct).
5. **No 'author list unavailable' branch** — any relaxation must be frozen BEFORE search (parent VN-2).
6. **Snowball executable via Semantic Scholar** — HTTP 200 verified on parent substrate probe.
7. **Director title-condition ruling** — substring + coverage >= 0.85, NOT full-token Jaccard.
8. **Standing output contract** — every cost quantity carries denominator, convention, uncertainty; modeled labeled modeled; absence reported as absence.

---

**Frozen at design. No outcome data inspected. This preregistration and spec.json are the immutable design for EXECUTE.**