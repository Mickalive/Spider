# EXP-PRODUCT-35651924708 Preregistration

## 1. Claims

- **Primary claim**: C-LLM-INHERIT — "A real LLM agent benefits from SPIDER beyond strong memory/instruction baselines"
- **Specific hypothesis**: Parameterized mechanism inheritance reduces total workflow cost (tokens + browser + verification) compared to cold exploration, literal replay, and retrieval baselines in the 25-75% novelty range

## 2. Background and Rationale

After 37+ experiments, no real LLM API calls have been made for C-LLM-INHERIT or C-PARAM-INHERIT. All mechanism claims are validated on synthetic or mock infrastructure. The product cannot be promoted without at least one end-to-end demonstration with real model calls.

The Global Research Director has identified this as the single largest strategic gap: "The absence of real LLM API calls for C-LLM-INHERIT and C-PARAM-INHERIT after 37+ experiments is the single largest strategic gap."

External competitors (TERX, WebCoach, HMT, AgentRR) demonstrate trajectory-level memory works. SPIDER's differentiation must be mechanism-level inheritance with formal guarantees. This experiment tests whether that differentiation translates to measurable cost reduction.

## 3. Task Corpus

### 3.1 Site Selection

JSONPlaceholder (https://jsonplaceholder.typicode.com) — a free fake REST API for testing.

**Rationale**: 
- Free, no authentication required, no rate limiting
- Predictable responses enable verification
- Multiple resource types (posts, comments, albums, photos, todos, users) enable novelty control
- Already used in prior C-PARAM-INHERIT experiments (EXP-GRAPH-33528827169, EXP-GRAPH-34170139507)
- Real HTTP endpoints (not mock servers)

### 3.2 Task Design

10 tasks designed to span the novelty spectrum:

| Task ID | Description | Novelty | Training Source |
|---------|-------------|---------|-----------------|
| T1 | Fetch post with ID=1 | 0% | Identical to training |
| T2 | Fetch post with ID=5 | 25% | Different ID, same endpoint |
| T3 | Fetch post with ID=15 | 25% | Different ID, same endpoint |
| T4 | Fetch comments for post ID=1 | 50% | Different endpoint, same resource type |
| T5 | Fetch comments for post ID=5 | 50% | Different endpoint, same resource type |
| T6 | Fetch albums for user ID=1 | 75% | Different resource type, same API |
| T7 | Fetch todos for user ID=1 | 75% | Different resource type, same API |
| T8 | Fetch users | 100% | Unseen endpoint structure |
| T9 | Create a new post | 100% | Unseen action type (POST) |
| T10 | Update post with ID=1 | 100% | Unseen action type (PUT) |

### 3.3 Training Set

Tasks T1-T3 are used for mechanism distillation (parameterized mechanism induction). Tasks T4-T10 are held out for testing.

## 4. Conditions

### 4.1 B-COLD (Cold Exploration)

LLM agent receives:
- System prompt: "You are a web agent. Complete the given task by navigating and interacting with the website."
- Task goal: "Fetch post with ID=1 from JSONPlaceholder API"
- No prior knowledge, no mechanisms, no trajectories

### 4.2 B-LITERAL (Literal Trajectory Replay)

LLM agent receives:
- System prompt: "You are a web agent. Complete the given task by following these exact steps."
- Task goal: "Fetch post with ID=1 from JSONPlaceholder API"
- Exact action sequence from training:
  1. Navigate to https://jsonplaceholder.typicode.com/posts/1
  2. Verify HTTP 200
  3. Extract response body

### 4.3 B-RETRIEVAL (Semantic Retrieval)

LLM agent receives:
- System prompt: "You are a web agent. Complete the given task using these prior examples as reference."
- Task goal: "Fetch post with ID=5 from JSONPlaceholder API"
- Top-3 semantically similar trajectories retrieved via cosine similarity over task descriptions
- Agent must adapt retrieved trajectories to current task parameters

### 4.4 B-SPIDER (SPIDER Parameterized Mechanism Inheritance)

LLM agent receives:
- System prompt: "You are a web agent. Complete the given task using this mechanism."
- Task goal: "Fetch post with ID=5 from JSONPlaceholder API"
- Parameterized mechanism:
  - Template: `GET https://jsonplaceholder.typicode.com/posts/${post_id}`
  - Parameters: `{post_id: 5}`
  - Preconditions: `endpoint exists, post_id is integer`
  - Postconditions: `HTTP 200, response contains userId, title, body fields`
  - Verification: `status == 200 && body contains required fields`

## 5. Metrics

### 5.1 Primary Metrics

| Metric ID | Name | Definition | Unit |
|-----------|------|------------|------|
| M-TOKENS | Total tokens | sum(usage.prompt_tokens + usage.completion_tokens) across all LLM calls | tokens |
| M-BROWSER | Browser interactions | count(clicks + navigations + form_fills) | count |
| M-VERIFY | Verification steps | count(assertion_checks) | count |
| M-TOTAL-COST | Total workflow cost | M-TOKENS + 10*M-BROWSER + 5*M-VERIFY (weighted composite) | normalized units |
| M-SUCCESS | Task success | 1 if correct HTTP request + response validated + content verified, else 0 | binary |

### 5.2 Secondary Metrics

| Metric ID | Name | Definition | Unit |
|-----------|------|------------|------|
| M-LATENCY | Wall-clock time | time(task_start -> verification_complete) | seconds |
| M-TOKEN-BREAKDOWN | Token breakdown | (prompt_tokens, completion_tokens) per condition | tokens |
| M-COST-PER-SUCCESS | Cost per successful task | M-TOTAL-COST / M-SUCCESS | normalized units |

## 6. Controls

### 6.1 Positive Control (PC-IDENTICAL)

Task T1 (0% novelty, identical to training). All conditions should succeed. Literal replay should have lowest cost. Validates measurement infrastructure.

**Pass criterion**: All 4 conditions succeed on T1.

### 6.2 Null Control (NC-NO-MECHANISM)

Task: "Fetch weather data from openweathermap.org" (unrelated to JSONPlaceholder). SPIDER registry has no applicable mechanisms.

**Pass criterion**: SPIDER condition reports "no applicable mechanism" or falls back to cold behavior. No hallucinated mechanisms.

## 7. Sampling and Randomization

- Each task x condition combination is executed 3 times with independent LLM context
- Total executions: 10 tasks x 4 conditions x 3 reps = 120
- Randomization: task order is randomized within each condition
- No cross-contamination: fresh LLM context for each execution

## 8. Analysis Plan

### 8.1 Primary Analysis

For tasks in the 25-75% novelty range (T2-T7, n=6 tasks x 3 reps = 18 observations per condition):

1. Compute mean total cost per condition
2. Paired bootstrap (5000 samples) comparing SPIDER vs min(cold, literal, retrieval)
3. Two-sided test at alpha=0.05
4. Report: point estimate, 95% CI, p-value, effect size (Cohen's d)

### 8.2 Secondary Analysis

1. Success rate comparison across conditions in 25-75% range
2. Cost breakdown analysis (tokens vs browser vs verification)
3. Novelty-scaling analysis: plot total cost vs novelty fraction per condition

### 8.3 Exploratory Analysis

1. Latency comparison
2. Token efficiency (cost per token)
3. Failure mode analysis (which tasks fail, why)

## 9. Decision Tree

```
IF primary_analysis p < 0.05 AND SPIDER_mean < min(baseline_means):
    CLAIM = SUPPORTS (C-LLM-INHERIT at synthetic-REST API ceiling)
    NEXT = Replicate on WebArena with LLM agent
ELIF primary_analysis p >= 0.05:
    CLAIM = DOES_NOT_SUPPORT (C-LLM-INHERIT remains HYPOTHESIS)
    NEXT = Investigate cost breakdown, consider alternative differentiation
ELIF primary_analysis p < 0.05 AND SPIDER_mean >= min(baseline_means):
    CLAIM = MIXED (SPIDER statistically different but not cheaper)
    NEXT = Analyze which cost components drive the difference
```

## 10. Validity Threats

### 10.1 Internal Validity

| Threat | Mitigation |
|--------|------------|
| LLM non-determinism | 3 reps per task x condition, bootstrap CI |
| Prompt sensitivity | Fixed prompt templates, no prompt engineering per condition |
| Task difficulty imbalance | Matched tasks across novelty levels, same API |
| Baseline strength | Cold baseline is genuinely zero-knowledge; retrieval uses same embedding model |

### 10.2 External Validity

| Threat | Mitigation |
|--------|------------|
| JSONPlaceholder simplicity | Acknowledged ceiling; real-Web validation requires WebArena |
| REST API only (no DOM) | Acknowledged; DOM interaction is separate claim (C-PARAM-INHERIT) |
| Single LLM model | gpt-4o-mini; cross-model validation is future work |
| Synthetic novelty control | Real-Web novelty is unstructured; controlled novelty is a design choice |

### 10.3 Construct Validity

| Threat | Mitigation |
|--------|------------|
| Total cost weighting | Sensitivity analysis on weights (10x browser, 5x verify) |
| Success definition | Binary success may miss partial progress; consider graded success |
| Token cost proxy | Real cost includes latency, API rate limits, error retries |

## 11. Sample Size Justification

- 10 tasks x 3 reps x 4 conditions = 120 total executions
- Primary analysis: 6 tasks x 3 reps = 18 observations per condition in 25-75% range
- Bootstrap CI width at n=18: approximately ±0.3 standard deviations (sufficient for medium effect sizes d>0.5)
- Cost: ~120K tokens at $0.01/1K = $1.20 total

## 12. Preregistration Notes

- This preregistration was written during DESIGN phase (no outcome data inspected)
- Analysis code will be frozen before execution
- Any deviation from this preregistration will be documented in result.json validity_notes
- Exploratory analyses are labeled as such and cannot support confirmatory claims

## 13. Parent Handoff Disposition

The parent handoff (EXP-PRODUCT-35611617123) concerns C-FRESHNESS orthogonality bounds. The Global Research Director has issued a PIVOT mandate to C-LLM-INHERIT. The parent's carry_forward categories are preserved as continuity evidence but DO NOT override the Director's PIVOT decision. The C-FRESHNESS thread is parked, not terminated — it may be reopened by a future Director mandate.

## 14. Dependencies

- Graph lane: C-PARAM-INHERIT mechanism induction must be functional on JSONPlaceholder (established in EXP-GRAPH-33528827169)
- Runtime lane: No runtime dependencies for this experiment (JSONPlaceholder is HTTP-only)
- Intel lane: No intel dependencies (using existing 2-site corpus)
- Infrastructure: OpenAI API key (or equivalent) for real LLM calls
