# Preregistration: EXP-INTEL-36306525220

## 1. Experiment Identification

- **Experiment ID**: EXP-INTEL-36306525220
- **Lane**: intel
- **Claim IDs**: C-PRODUCT-ECON
- **Director Mandate**: CONTINUE with cognitive_reset=true, SUPERSEDE parent handoff
- **Parent Handoff**: EXP-INTEL-36293264917 (MEASUREMENT_INVALID, identity-before-scoring failure)
- **Request Hash**: 6549f54917b70e15eaf014f5d55c25c26909559de88ffa8862f41f405d9f6110

## 2. Binding Research Question (from Director Mandate)

Under a hard identity-before-scoring contract in which every target must resolve to an artifact whose title and abstract demonstrably concern the named system under a matching rule frozen before the search, a positive control must pass before any target is scored, unresolvable targets are recorded UNMEASURED and never converted to NOT_FOUND, and absence of a reported quantity is reported as absence rather than as a negative:

**Part 1 (Cost Accounting)**: What do published web-agent systems that persist state across sessions or episodes actually report about cost — the exact cost accounting convention used (tokens, requests, latency, or a modeled ratio) with its denominator and stated uncertainty, any break-even reuse count or marginal cost of a cached versus re-derived observation, any reported staleness, forgetting or maintenance cost of retained state, and whether any published result shows persistent cross-episode state beating re-derivation on a real cost basis?

**Part 2 (Performance Envelope)**: What end-to-end success rates do the strongest published memory-augmented or workflow-inducing web agents report on the benchmarks SPIDER would actually use (Mind2Web, WebArena, WebVoyager and their online variants), reported as a published envelope with denominators and evaluation conventions rather than as a comparison SPIDER has run?

**Part 3 (Retrieval vs Write)**: Does published evidence show that retrieval quality rather than write sophistication, comparing raw chunked storage against summarization and extraction pipelines, is the dominant driver of downstream accuracy?

## 3. Hypothesis and Falsifier

### Hypothesis
Published web-agent systems with persistent state report cost quantities that are either (a) modeled upper bounds rather than measurements, (b) lack denominators/uncertainties, or (c) show break-even reuse counts that are not achieved in practice; published performance envelopes on Mind2Web/WebArena/WebVoyager exist but use heterogeneous evaluation conventions that prevent direct comparison; retrieval quality (coverage, precision of relevant context) is reported as a stronger driver of downstream accuracy than write-pipeline sophistication (summarization vs extraction vs raw storage).

### Falsifier
Any of:
1. A published system reports a **measured** (not modeled) break-even reuse count f* with denominator, accounting convention and uncertainty, and demonstrates persistent state beating re-derivation on real cost.
2. Published performance envelopes on Mind2Web/WebArena/WebVoyager use a **common evaluation convention** with stated denominators enabling direct comparison.
3. Published ablation evidence shows **write-pipeline sophistication** (summarization/extraction) explains more variance in downstream accuracy than **retrieval quality** (recall/precision of relevant context).

## 4. Identity Resolution Protocol (FROZEN BEFORE SEARCH)

### 4.1 Matching Rule
A target is **CORRECTLY_RESOLVED** iff ALL of the following hold:
1. The resolver retrieves an artifact by **exact arXiv ID** from the frozen target list (Section 4.3).
2. The artifact's **title** matches the expected title substring (case-insensitive, fuzzy threshold ≥ 0.85 Jaccard on token sets).
3. At least one **author name** matches the expected author list (substring match).
4. The artifact's **abstract** contains at least one keyword from the system's domain keyword list (web, agent, browser, automation, LLM, e-commerce, benchmark, environment, multimodal, replay, compilation, memory).

If ANY condition fails, the resolution is **AMBIGUOUS** (partial match) or **NOT_LOCATED** (no candidate found), and the target is recorded as **UNMEASURED** in the output table. **NEVER scored as NOT_FOUND.**

### 4.2 Resolution Procedure
1. Query arXiv API with exact arXiv ID from frozen target list.
2. Parse response: title, authors, abstract, categories.
3. Apply matching rule (4.1) deterministically.
4. Record resolution_status: CORRECTLY_RESOLVED | AMBIGUOUS | NOT_LOCATED.
5. If CORRECTLY_RESOLVED → proceed to field extraction (Section 5).
6. If AMBIGUOUS or NOT_LOCATED → emit UNMEASURED row with resolution_status and evidence_for_absence = "Identity resolution failed: [specific condition]".

### 4.3 Frozen Target List
| System | arXiv ID | Expected Title Substring | Expected Authors | Domain Keywords |
|--------|----------|--------------------------|------------------|-----------------|
| WebShop | 2207.01206v4 | WebShop | Yao, Chen, Yang, Narasimhan | web, shop, agent, e-commerce |
| Mind2Web | 2306.06070v3 | Mind2Web | Deng, Gu, Chen, Liu | web, agent, mind, automation |
| WebVoyager | 2401.13919v4 | WebVoyager | He, Zhang, Yao, Chen | web, voyager, agent, multimodal, browser |
| WebArena | 2307.13854v3 | WebArena | Zhou, Liu, Gu, Chen | web, arena, agent, benchmark, environment |
| AgentBench-web | 2308.03688v2 | AgentBench | Liu, Zhang, Yang, Chen | agent, bench, web, evaluation |
| BrowserGym | 2401.15378v2 | BrowserGym | Drouin, Gagnon, Lacoste | browser, gym, environment, agent |
| MiniWoB++ | 1802.08827v3 | MiniWoB | Liu, Shi, Zhou, Chen | miniwob, web, automation, benchmark |
| SeeAct | 2402.04566v2 | SeeAct | Zheng, Chen, Yang, Liu | seeact, agent, web, action |
| Crux | 2406.01234v1 | Crux | TBD | crux, agent, web |
| WebAgent | 2403.01234v1 | WebAgent | TBD | web, agent |
| RULER | 2405.01234v1 | RULER | TBD | ruler, agent, web, evaluation |
| WebCanvas | 2407.01234v1 | WebCanvas | TBD | webcanvas, agent, web |
| BrowserBench | 2408.01234v1 | BrowserBench | TBD | browserbench, agent, web |
| ActivityFrames | 2608.05784v1 | Activity Frames | TBD | activity, frames, agent, memory, replay, compilation |

**Note**: arXiv IDs for Crux, WebAgent, RULER, WebCanvas, BrowserBench are placeholders; if they do not resolve, those targets are NOT_LOCATED → UNMEASURED. This is correct behavior.

### 4.4 Snowball Sampling (Optional, Bounded)
- 1-hop citation snowball from correctly resolved targets.
- Maximum 50 additional papers.
- Each snowball target undergoes same identity resolution protocol with its own frozen arXiv ID.
- Reported separately as `snowball_coverage` in coverage summary.

## 5. Field Extraction Protocol

### 5.1 Part 1: Cost Accounting Fields
For each CORRECTLY_RESOLVED target, extract the following with **exact evidence quotes**:

| Field | Description | Required |
|-------|-------------|----------|
| `Routine_Overhead_Ratio_R` | Overhead ratio (e.g., 60-343x) or statement that none reported | Yes |
| `delegable_recurrence_h` | Delegable recurrence fraction (e.g., 9.0%) or statement that none reported | Yes |
| `break_even_reuse_count_fstar` | Break-even reuse count f* or statement that none reported | Yes |
| `marginal_cost_cached_vs_derived` | Marginal cost comparison or statement that none reported | Yes |
| `staleness_forgetting_maintenance_cost` | Any reported staleness/forgetting/maintenance cost or statement that none reported | Yes |
| `real_cost_advantage_persistence` | Whether persistence beats re-derivation on real cost basis (Y/N/partial/none) | Yes |
| `denominator` | Denominator for cost quantities (per task, per episode, per 1000 tokens, etc.) | Yes |
| `accounting_convention` | Convention: input+output tokens, wall-clock seconds, modeled upper bound, etc. | Yes |
| `stated_uncertainty` | CI, range, standard error, or "not reported" | Yes |
| `modeled_vs_measured` | "modeled", "measured", or "not_reported" | Yes |

### 5.2 Part 2: Performance Envelope Fields
For each CORRECTLY_RESOLVED target on Mind2Web/WebArena/WebVoyager benchmarks:

| Field | Description | Required |
|-------|-------------|----------|
| `success_rate` | Reported success rate (percentage or fraction) | Yes |
| `denominator` | Denominator: number of tasks, episodes, steps | Yes |
| `evaluation_convention` | Exact convention: success rate@k, task completion rate, step success rate, etc. | Yes |
| `benchmark_split` | Train/val/test split, number of tasks, sites | Yes |
| `modeled_vs_measured` | "modeled", "measured", or "not_reported" | Yes |

### 5.3 Part 3: Retrieval vs Write Fields
For each CORRECTLY_RESOLVED target that compares retrieval vs write:

| Field | Description | Required |
|-------|-------------|----------|
| `retrieval_quality_metric` | Recall/precision/F1 of relevant context retrieval | Yes |
| `write_pipeline_type` | Raw chunked / summarization / extraction / hybrid | Yes |
| `downstream_accuracy` | Accuracy on downstream task | Yes |
| `ablation_result` | Which factor explains more variance (retrieval/write/both/neither) | Yes |
| `evidence_quote` | Exact quote supporting the ablation conclusion | Yes |

### 5.4 Evidence Quote Requirement
**Every extracted field must carry its exact evidence quote** from the resolved artifact (title, abstract, or full text if accessible). If full text is not accessible without credentials, extract from abstract + title only and note "abstract_only" in evidence quote. Modeled quantities MUST have `modeled_vs_measured="modeled"` and `accounting_convention` must explicitly state the modeling assumption (e.g., "modeled upper bound assuming X").

## 6. Controls (FROZEN BEFORE SEARCH)

### 6.1 Positive Control: PC-COST-ACCOUNTING (Part 1 Gate)
- **Target**: arXiv:2608.05784v1 (Activity Frames)
- **Required Fields**: All 10 fields in Section 5.1
- **Pass Criterion**: All 10 fields extracted with evidence quotes from artifact that passes identity resolution (Section 4.1).
- **Failure Consequence**: **MEASUREMENT_INVALID for entire experiment** (Part 1, 2, 3).
- **Rationale**: This paper is the single external source the Scout brief and prior handoff identified as reporting cost accounting conventions. If the instrument cannot extract known quantities from a correctly resolved known paper, it has no power.

### 6.2 Positive Control: PC-PERFORMANCE-ENVELOPE (Part 2 Gate)
- **Target**: arXiv:2401.13919v4 (WebVoyager)
- **Required Fields**: success_rate, denominator, evaluation_convention, benchmark_split (Section 5.2)
- **Pass Criterion**: All 4 fields extracted with evidence quotes from correctly resolved artifact.
- **Failure Consequence**: **MEASUREMENT_INVALID for Part 2 only**.

### 6.3 Null Control: NC-REAL-BUT-WRONG (Program-Level Specificity Control)
- **Target**: Map system name **"WebArena"** to arXiv:1802.05012v2 ("Getting out of the closet: Scientific authorship of literary fiction and knowledge transfer", 2018, Azagra-Caro et al.) — a REAL paper that is demonstrably NOT about WebArena.
- **Pass Criterion**: Resolver flags identity mismatch (title/abstract/arXiv ID do not concern WebArena) and emits **UNMEASURED** for this target. Does NOT score NOT_FOUND.
- **Failure Consequence**: **MEASUREMENT_INVALID for entire experiment**.
- **Rationale**: This is the exact failure mode that occurred 5 times in EXP-INTEL-36293264917 (WebArena, WebGym, MiniWoB++, BrowserGym, AgentBench-web all resolved to wrong papers and scored NOT_FOUND). A null control with a REAL-but-WRONG identity has power against this failure; a fabricated ID (NC-FABRICATED-CLAIM) does not.

### 6.4 Null Control: NC-FABRICATED-CLAIM (Sanity Check Only)
- **Target**: arXiv:2609.99999 (non-existent arXiv ID)
- **Pass Criterion**: Resolver fails to locate artifact and emits NOT_LOCATED.
- **Failure Consequence**: Recorded but **does not trigger MEASUREMENT_INVALID** (no power against real-but-wrong failure).

## 7. Measurement Validity Gates (FROZEN)

The experiment is **MEASUREMENT_INVALID** if ANY of the following triggers:

1. **PC-COST-ACCOUNTING fails** → entire experiment INVALID.
2. **NC-REAL-BUT-WRONG fails to flag mismatch** (emits LOCATED/NOT_FOUND instead of UNMEASURED) → entire experiment INVALID.
3. **Any target scored NOT_FOUND** instead of UNMEASURED → entire experiment INVALID.
4. **PC-PERFORMANCE-ENVELOPE fails** → Part 2 INVALID (Parts 1, 3 may still be valid).
5. **Identity resolution recall < 0.6** (correctly_resolved / named_systems_searched) for a given part → that part INCONCLUSIVE.

**Note**: These gates are evaluated BEFORE any scientific outcome (SUPPORTS/FALSIFIES/MIXED) is assigned. A MEASUREMENT_INVALID outcome is a measurement-validity failure, NOT a scientific falsification.

## 8. Decision Rules (FROZEN)

### Part 1: Cost Accounting
| Outcome | Condition |
|---------|-----------|
| MEASUREMENT_INVALID | Gate 1, 2, or 3 triggered |
| SUPPORTS | ≥1 system reports **measured** break-even f* with denominator, convention, uncertainty, AND demonstrates real-cost advantage of persistence |
| FALSIFIES | **No** system reports any break-even reuse count or real-cost advantage; all cost quantities are modeled upper bounds or lack denominators/uncertainties |
| MIXED | Some systems report partial cost accounting (e.g., token counts without break-even), but no complete measured break-even with uncertainty |
| INCONCLUSIVE | Identity resolution recall < 0.6 |

### Part 2: Performance Envelope
| Outcome | Condition |
|---------|-----------|
| MEASUREMENT_INVALID | Gate 4 or 3 triggered |
| SUPPORTS | Published envelopes on Mind2Web/WebArena/WebVoyager use **common evaluation convention** with stated denominators enabling direct comparison |
| FALSIFIES | Published envelopes exist but use **heterogeneous conventions** preventing direct comparison; no common denominator |
| MIXED | Some benchmarks have comparable conventions, others do not |
| INCONCLUSIVE | Identity resolution recall < 0.6 |

### Part 3: Retrieval vs Write
| Outcome | Condition |
|---------|-----------|
| MEASUREMENT_INVALID | Gate 3 triggered |
| SUPPORTS | Published ablation shows **retrieval quality** explains significantly more variance than write-pipeline sophistication |
| FALSIFIES | Published ablation shows **write-pipeline sophistication** explains more variance than retrieval quality |
| MIXED | Both factors significant but neither clearly dominant; or evidence from single paper only |
| INCONCLUSIVE | No published ablation evidence comparing these factors; or identity resolution recall < 0.6 |

### Overall Experiment Outcome
| Outcome | Condition |
|---------|-----------|
| MEASUREMENT_INVALID | Any part is MEASUREMENT_INVALID |
| SUPPORTS | All three parts are SUPPORTS or MIXED with at least one SUPPORTS |
| FALSIFIES | All three parts are FALSIFIES |
| MIXED | Otherwise |

## 9. Output Contract (MACHINE-CHECKABLE)

### 9.1 Primary Output: JSON Table
File: `results/table.json` (or `result.json` metrics.artifact_table)

Schema per row:
```json
{
  "part": 1|2|3,
  "system": "string",
  "benchmark": "string|null",
  "metric": "string",
  "value": "number|null",
  "denominator": "string|null",
  "accounting_convention": "string|null",
  "stated_uncertainty": "string|null",
  "modeled_vs_measured": "modeled|measured|not_reported|null",
  "source_quote": "string|null",
  "source_arxiv_id": "string|null",
  "resolution_status": "CORRECTLY_RESOLVED|AMBIGUOUS|NOT_LOCATED|UNMEASURED",
  "evidence_for_absence": "string|null"
}
```

**Requirements**:
- Every row has `resolution_status`. UNMEASURED rows have `value=null` and `evidence_for_absence` populated if paper was resolved but lacked the quantity.
- **No row may have `resolution_status="NOT_FOUND"`**.
- Modeled quantities must have `modeled_vs_measured="modeled"` and `accounting_convention` explicitly stating the modeling assumption.
- Table accompanied by coverage summary:
  ```json
  {
    "identity_resolution_recall": 0.XX,
    "named_systems_searched": N,
    "correctly_resolved": M,
    "unsearched_systems": ["list"],
    "snowball_coverage": {"papers_examined": K, "papers_resolved": L}
  }
  ```

### 9.2 Result.json Metrics
The `result.json` metrics object must include:
- `part1_outcome`, `part2_outcome`, `part3_outcome`, `overall_outcome`
- `identity_resolution_recall_part1`, `part2`, `part3`
- `pc_cost_accounting_pass`, `pc_performance_envelope_pass`, `nc_real_but_wrong_pass`, `nc_fabricated_claim_pass`
- `coverage_summary` (as above)
- `artifact_table_path` (path to the JSON table)

### 9.3 Controls Object
The `result.json` controls object must include entries for each control ID with:
- `expected_behavior`, `observed_behavior`, `pass_fail`, `evidence_ref`

## 10. Scope Boundaries

- **IN SCOPE**: Published web-agent papers (arXiv, conference proceedings accessible via Semantic Scholar/Crossref) that report persistent state across sessions/episodes.
- **OUT OF SCOPE**: 
  - Papers without persistent state (single-episode only).
  - Non-web-agent domains (mobile, desktop, API-only).
  - Reproduction of experiments (reading published numbers only).
  - SPIDER's own measurements (this is INTEL lane, not Graph/Physics/Product).
  - Infrastructure deployment (WebGym, WebArena-Infinity, Docker, credentials).
  - Compiler addressing/regime extraction (explicitly prohibited by Director mandate).

## 11. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Identity resolution fails for valid papers (false negative) | Frozen matching rule with generous fuzzy threshold (0.85 Jaccar); manual verification of AMBIGUOUS cases logged but not scored |
| Full text not accessible (extraction from abstract only) | Record `evidence_quote` as "abstract_only: [quote]"; note limitation in validity_notes |
| arXiv IDs in target list incorrect (placeholder IDs) | Placeholders for Crux/WebAgent/RULER/WebCanvas/BrowserBench will resolve to NOT_LOCATED → UNMEASURED; this is correct behavior, not a failure |
| Heterogeneous evaluation conventions prevent comparison | This is the scientific question for Part 2; the output records each convention explicitly |
| Single paper (Activity Frames) dominates Part 1 evidence | Coverage summary reports unsearched systems; snowball sampling bounded to 50 papers to broaden |
| Modeled vs measured distinction ambiguous in source | `modeled_vs_measured` field forces explicit classification; "not_reported" for ambiguous cases |

## 12. Estimated Resources

- Wall-clock: ~300 seconds (credential-free HTTP over arXiv, Semantic Scholar, Crossref)
- Model calls: 0
- Browser interactions: 0
- Network requests: ~200
- Credentials required: None

## 13. Consequences

### If SUPPORTS (or MIXED with SUPPORTS):
- C-PRODUCT-ECON gains external justification → can advance toward EXPERIMENTAL.
- SPIDER has published benchmarks to beat (performance envelope with conventions).
- Architectural focus on retrieval quality over write sophistication is externally validated.

### If FALSIFIES:
- No external justification for persistence economics → SPIDER must produce its own honest ledger.
- Published performance envelopes are incomparable → SPIDER must define its own evaluation standard.
- Write-path investment may be warranted → architectural pivot possible.
- C-PRODUCT-ECON remains HYPOTHESIS with no external anchor (decision-grade absence).

### If MEASUREMENT_INVALID:
- Instrument defect not fixed → program-level repair required before any intel cycle on this question.
- No claim update; C-PRODUCT-ECON remains HYPOTHESIS.
- This would be the third consecutive MEASUREMENT_INVALID for this failure class.

## 14. Reproducibility

- All arXiv IDs, matching rules, extraction schemas frozen in this document.
- Deterministic resolver: same arXiv ID → same result (arXiv API is stable).
- No model calls, no random seeds, no browser state.
- Raw API responses logged to `raw/search_log.jsonl` with timestamps.
- Coverage summary enables exact replication of identity resolution recall.

---

**FROZEN**: This preregistration is immutable after `freeze.json` is created. No outcome-bearing measurements may be inspected during DESIGN. Any deviation from this protocol during EXECUTE must be recorded in `provenance.json` deviations_from_frozen_design and evaluated against the frozen decision rules.