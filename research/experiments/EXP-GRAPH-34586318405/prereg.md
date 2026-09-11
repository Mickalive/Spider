# EXP-GRAPH-34586318405 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34586318405
- **Lane**: Graph
- **Claims**: C-SEMANTIC-RESOLVE
- **Date**: 2026-09-11
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-GRAPH-34409639346 (C-SEMANTIC-RESOLVE falsified at current kernel level for simple path aliasing, 0/10 aliased-first correct selections, binomial p=1.0)

## 2. Scientific Question

Can the kernel handle more complex aliasing scenarios — query parameters, path rewriting, or server-side routing — and does HTTP execution success against real endpoints provide a grounding signal for template correctness that resolver selection alone cannot?

## 3. Motivation

The parent experiment (EXP-GRAPH-34409639346) established:
- Kernel uses exact intent matching (kernel.py L97: `m.intent != intent`)
- Selection for equal-confidence candidates determined by confidence sort then mechanism_id tie-breaking (L112)
- Aliased-first subset: 0/10 selects template-matching mechanism (binomial p=1.0)
- C-SEMANTIC-RESOLVE falsified at current kernel level for **simple path aliasing** (distinct path patterns like `/users/{id}` vs `/accounts/{uid}`)

The parent's handoff identifies the next question:
- More complex aliasing scenarios: query parameters, path rewriting, server-side routing
- Whether HTTP execution provides a grounding signal absent from resolver selection

The parent experiment tested only simple path aliasing where both templates point to distinct (non-existent) paths. It did not test:
1. **Query-parameter aliasing**: `/posts/${id}` vs `/posts?id=${id}` (same resource, different URL structure)
2. **Path rewriting**: `/users/${id}/posts` vs `/users?userId=${id}/posts` (server maps both to same resource)
3. **Server-side routing**: `/albums/${id}/photos` vs `/photos?albumId=${id}` (multiple valid routes to same data)
4. Whether HTTP execution can distinguish correct from incorrect templates
5. Whether execution provides corrective signal when resolver selects incorrectly

This experiment addresses all five gaps using real HTTP endpoints (jsonplaceholder.typicode.com).

## 4. Hypotheses

### H1: No Semantic Template Analysis
The kernel does not analyze URL template structure. In aliased-first conditions (where tie-breaking favors the aliased mechanism), the kernel selects the template-matching mechanism in 0% of cases (always follows tie-breaking). This extends the parent's simple-path-aliasing finding to complex aliasing scenarios.

### H2: HTTP Execution Identifies Template Correctness
For scenarios where one template is correct (HTTP 200) and one is incorrect (HTTP 404/error), HTTP execution correctly identifies the valid template in 100% of cases. This measures whether HTTP success is a reliable grounding signal.

### H3: Baseline Integrity
All 6 baselines pass: B-EMPTY-REGISTRY (UNKNOWN), B-SINGLE-MECHANISM (EXECUTABLE + HTTP 200), B-CONFIDENCE-HIGHER (higher confidence wins), B-CONFIDENCE-EQUAL-DIFFERENT-INTENT (exact match only), B-HTTP-POSITIVE (HTTP 200), B-HTTP-NEGATIVE (HTTP 404/error).

### H4: Execution-Resolver Divergence Exists
There exist conditions where resolver selection and HTTP execution outcomes carry different information: the resolver picks a template deterministically (based on mechanism_id), but HTTP execution reveals that the alternative template is also valid (or the selected one is invalid). This divergence demonstrates that execution provides information absent from resolver selection.

## 5. Experimental Design

### 5.1 Two-Layer Architecture

The experiment has two independent measurement layers:

**Layer 1 — Kernel Resolution**: For each condition, create a fresh kernel+registry, call `kernel.resolve()`, record the Resolution (status, mechanism_id, bound_action). This layer tests whether the kernel performs semantic template analysis.

**Layer 2 — HTTP Execution**: For each condition where the kernel returns EXECUTABLE, execute HTTP requests against real endpoints. For aliased pairs, execute BOTH:
- The resolver-selected template (via kernel bound_action with base URL prepended)
- The alternative template (via direct HTTP call with same parameters)

This layer tests whether HTTP success provides grounding signal absent from resolver selection.

### 5.2 Test Scenarios

#### Scenario A: Query-Parameter Aliasing (Both Templates Work)
- Intent: `get-post-by-id`
- Template A (path param): `/posts/${postId}` → jsonplaceholder `/posts/1` → HTTP 200
- Template B (query param): `/posts?id=${postId}` → jsonplaceholder `/posts?id=1` → HTTP 200
- Both templates produce valid URLs for the same resource
- Expected resolver: selects based on mechanism_id tie-breaking (not template correctness)
- Expected HTTP: both return 200 (functional equivalence)
- Grounding value: 0 (both work, no corrective signal)
- Purpose: tests whether the kernel distinguishes URL structure when both are valid

#### Scenario B: Query-Parameter Aliasing (One Template Broken)
- Intent: `get-post-comments`
- Template A (correct): `/posts/${postId}/comments` → jsonplaceholder `/posts/1/comments` → HTTP 200
- Template B (malformed): `/posts?id=${postId}/comments` → jsonplaceholder `/posts?id=1/comments` → HTTP 404
- Template B produces a URL that no endpoint accepts
- Expected resolver: selects based on tie-breaking (not correctness)
- Expected HTTP: A=200, B=404
- Grounding value: >0 if resolver selects B (fails HTTP) while A works
- Purpose: tests whether HTTP execution catches incorrect templates

#### Scenario C: Path Rewriting (One Template Broken)
- Intent: `list-user-posts`
- Template A (correct): `/users/${userId}/posts` → jsonplaceholder `/users/1/posts` → HTTP 200
- Template B (malformed): `/users?userId=${userId}/posts` → jsonplaceholder `/users?userId=1/posts` → HTTP 404
- Template B mixes query and path syntax incorrectly
- Expected resolver: tie-breaking selects based on mechanism_id
- Expected HTTP: A=200, B=404
- Grounding value: >0 if resolver selects B while A works
- Purpose: tests path rewriting aliasing with incorrect alternative

#### Scenario D: Path Rewriting (Both Templates Work)
- Intent: `get-album-photos`
- Template A (nested): `/albums/${albumId}/photos` → jsonplaceholder `/albums/1/photos` → HTTP 200
- Template B (query filter): `/photos?albumId=${albumId}` → jsonplaceholder `/photos?albumId=1` → HTTP 200
- Both are valid routes to the same data (server-side routing)
- Expected resolver: tie-breaking selects based on mechanism_id
- Expected HTTP: both return 200
- Grounding value: 0 (both work)
- Purpose: tests whether server-side routing produces functional equivalence

#### Scenario E: Server-Side Routing (One Template Broken)
- Intent: `get-user-albums`
- Template A (correct): `/users/${userId}/albums` → jsonplaceholder `/users/1/albums` → HTTP 200
- Template B (incorrect): `/albums?userId=${userId}` → jsonplaceholder `/albums?userId=1` → HTTP 200 (returns all albums, not filtered)
- Note: B returns 200 but with DIFFERENT data (all albums vs user's albums). This is a semantic correctness issue, not HTTP status.
- Expected HTTP: both return 200, but response bodies differ
- Grounding value: measured by response body comparison, not just status code
- Purpose: tests whether HTTP status alone is sufficient grounding (it is not — body content matters)

#### Scenario F: URL Encoding Variant (Both Work)
- Intent: `search-posts`
- Template A (path): `/posts?q=${query}` → jsonplaceholder `/posts?q=test` → HTTP 200 (returns all posts, query ignored by API)
- Template B (path): `/posts?_q=${query}` → jsonplaceholder `/posts?_q=test` → HTTP 200 (returns all posts, unknown param ignored)
- Both return same data (jsonplaceholder ignores query params)
- Expected HTTP: both return 200 with identical bodies
- Grounding value: 0
- Purpose: tests whether URL encoding differences affect grounding

### 5.3 ID Ordering Control

For each scenario, two orderings:
- **Correct-first**: Template A (correct) has smaller mechanism_id (e.g., `a-01`), Template B (aliased) has larger ID (e.g., `z-01`). Tie-breaking selects A (correct). Grounding value = 0 (resolver already picks correct).
- **Aliased-first**: Template B (aliased) has smaller mechanism_id (`a-01`), Template A (correct) has larger ID (`z-01`). Tie-breaking selects B (potentially incorrect). Grounding value >0 if HTTP shows B fails and A works.

Only aliased-first conditions can produce grounding value. Correct-first conditions are consistency checks.

### 5.4 Sample Size

- 6 scenarios x 2 orderings = 12 aliased conditions
- Plus 6 baselines
- Total kernel calls: 18
- Total HTTP executions: up to 30 (18 resolver-bound + up to 12 alternative-template executions for aliased pairs)

## 6. Controls

### 6.1 Positive Control (B-SINGLE-MECHANISM)
- One mechanism: intent='get-post-by-id', template='/posts/${postId}', preconditions={'method':'GET'}
- Kernel returns EXECUTABLE with bound_action={'url':'/posts/1','method':'GET'}
- HTTP GET jsonplaceholder /posts/1 returns 200 with userId field
- Verifies: resolution pipeline + HTTP execution pipeline both work

### 6.2 Null Control (B-EMPTY-REGISTRY)
- Empty registry returns UNKNOWN
- Verifies: kernel does not hallucinate candidates

### 6.3 HTTP Positive Control (B-HTTP-POSITIVE)
- Template '/posts/1' against jsonplaceholder → HTTP 200
- Verifies: HTTP execution against known-good endpoint succeeds

### 6.4 HTTP Negative Control (B-HTTP-NEGATIVE)
- Template '/nonexistent-resource/999' against jsonplaceholder → HTTP 404 or error
- Verifies: HTTP execution correctly detects broken templates

### 6.5 Confidence Ordering Control (B-CONFIDENCE-HIGHER)
- Two mechanisms with different intents, confidences 0.95 vs 0.8
- Higher-confidence mechanism wins
- Verifies: confidence ordering works correctly

### 6.6 Intent Filtering Control (B-CONFIDENCE-EQUAL-DIFFERENT-INTENT)
- Two mechanisms with different intents, equal confidence
- Only exact intent match qualifies
- Verifies: intent filtering works correctly

## 7. Metrics

### 7.1 Primary Metrics

- **aliased_first_correct_selection_rate**: Fraction of aliased-first conditions (n=6) where kernel selects the template-matching mechanism. Expected: 0.0 (H1).
- **http_template_accuracy**: For asymmetric scenarios (B, C where one template works and one fails), fraction where HTTP execution correctly identifies the valid template. Expected: 1.0 (H2).
- **grounding_event_count**: Number of aliased-first conditions where resolver-selected template fails HTTP but alternative template succeeds. This is the corrective signal count.

### 7.2 Secondary Metrics

- **resolver_status_distribution**: Count of EXECUTABLE, UNKNOWN, EXPLORE across all 18 conditions
- **http_success_rate_by_template_type**: HTTP success rate for path-parameter vs query-parameter templates
- **http_latency_ms**: Per-request latency (informational)
- **response_body_agreement**: For scenarios where both templates return 200, whether response bodies are identical (JSON comparison)
- **baseline_pass_rate**: Fraction of 6 baselines that pass

### 7.3 Derived Metrics

- **grounding_value_ratio**: grounding_event_count / 6 (aliased-first conditions). 0 = execution provides no corrective signal; 1 = execution always corrects resolver misprediction.
- **resolver_execution_agreement**: Fraction of conditions where resolver selection and HTTP execution agree (both indicate correct template or both indicate incorrect).

## 8. Statistical Tests

### 8.1 Primary: Binomial Test (H1)
- H0: kernel selects template-matching mechanism in 50% of aliased-first conditions (chance)
- H1: kernel selects in 0% (always follows tie-breaking)
- Test: binomial test, n=6 (aliased-first conditions), k=0 (correct selections)
- One-sided, alpha=0.05
- Power: 0/6 yields p=0.016 (significant); 1/6 yields p=0.109 (not significant)

### 8.2 Descriptive: HTTP Accuracy (H2)
- http_template_accuracy = correct_identifications / asymmetric_conditions
- No formal hypothesis test — descriptive count
- Report exact counts per scenario

### 8.3 Baseline Verification (H3)
- All 6 baselines must pass (binary pass/fail)

## 9. Validity Threats

### 9.1 Network Reliability
HTTP execution against real endpoints may fail due to network issues.
Mitigation: timeout=10s; retry once on timeout/connection error; record failures as measurement issues. If >50% of HTTP executions fail, verdict = MEASUREMENT_INVALID.

### 9.2 Endpoint Stability
jsonplaceholder.typicode.com may change behavior or become unavailable.
Mitigation: use well-known stable endpoints (/posts, /users, /albums, /comments, /photos). Verify B-HTTP-POSITIVE and B-HTTP-NEGATIVE before main conditions. jsonplaceholder is a widely-used public test API with high availability.

### 9.3 Small Sample Size
n=6 aliased-first conditions has limited power for binomial test.
Mitigation: this is a proof-of-concept screen. 0/6 is significant (p=0.016); >=2/6 is not significant but weakens the hypothesis. Report exact p-values.

### 9.4 Query Parameter Ignorance
jsonplaceholder.typicode.com may ignore query parameters (returns same data regardless of query). This means templates A, D, E, F may return 200 with identical bodies even when query parameters are structurally different.
Mitigation: this is by design — it tests whether HTTP STATUS alone provides grounding (it does not when APIs ignore params). Response body comparison is a secondary metric. Scenarios B and C use paths that genuinely 404.

### 9.5 Template Parameter Binding
All templates use `${param}` syntax. The kernel's `_bind()` function substitutes parameters. If template has incorrect parameter names, binding may produce malformed URLs.
Mitigation: all templates use parameter names that exist in the provided params dict.

### 9.6 HTTP Execution Scope
HTTP execution tests GET requests only. POST, PUT, DELETE, PATCH are out of scope.
This bounds the claim to read-only template validation.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. All 6 baselines pass
2. No exceptions in kernel calls
3. Aliased-first correct selection rate = 0% (0/6 aliased-first conditions select template-matching mechanism)
4. For asymmetric scenarios (B, C), HTTP execution correctly identifies the valid template in 100% of cases

### 10.2 FALSIFIED-IN-SETTING
If ANY of:
1. Aliased-first correct selection rate > 0% (kernel shows semantic template analysis)
2. Any baseline fails
3. For asymmetric scenarios, HTTP execution fails to identify the valid template in >50% of cases

### 10.3 MEASUREMENT_INVALID
If:
1. >50% of HTTP executions fail due to network/infrastructure issues
2. Kernel crashes in >50% of conditions
3. jsonplaceholder.typicode.com is unreachable during execution window

## 11. Expected Outcomes

### 11.1 SURVIVES_CURRENT_TEST (Most Likely)
- Kernel follows tie-breaking exactly (0/6 aliased-first correct) — consistent with parent
- HTTP execution correctly identifies valid templates in asymmetric scenarios
- For scenarios where both templates work (A, D, F), execution confirms functional equivalence
- Product consequence: 'resolve then validate' pattern is viable; HTTP execution validation catches resolver mispredictions
- C-SEMANTIC-RESOLVE remains falsified at resolver level but gains practical mitigation

### 11.2 FALSIFIED (Kernel Shows Semantic Analysis)
- Kernel selects template-matching mechanism in >0% of aliased-first conditions
- Would be surprising given code analysis and parent result
- Product consequence: kernel has unrecognized capability; re-evaluate C-SEMANTIC-RESOLVE
- Requires replication with larger sample

### 11.3 FALSIFIED (HTTP Cannot Distinguish Templates)
- Kernel follows tie-breaking (0/6) but HTTP execution fails to identify correct templates in asymmetric scenarios
- This would mean HTTP status codes are not a reliable grounding signal
- Product consequence: must implement explicit template validation as separate feature, not rely on HTTP status
- Graph lane should pivot to other priority claims

### 11.4 MEASUREMENT_INVALID
- Network/infrastructure failures prevent measurement
- Not scientific evidence; retry with diagnostics

## 12. Analysis Plan

1. **Baseline Verification**: Execute all 6 baselines. If any fail, stop and report MEASUREMENT_INVALID.
2. **Aliased Conditions**: Execute 6 scenarios x 2 orderings = 12 conditions.
3. **Resolver Recording**: For each condition, record kernel.resolve() output.
4. **HTTP Execution**: For each EXECUTABLE result, execute resolver-selected URL. For aliased pairs, also execute alternative template URL.
5. **Response Comparison**: Compare HTTP status codes and response bodies between resolver-selected and alternative templates.
6. **Metric Computation**: Compute aliased_first_correct_selection_rate, http_template_accuracy, grounding_event_count.
7. **Statistical Tests**: Binomial test on aliased-first subset.
8. **Control Checks**: Verify all controls pass.
9. **Reporting**: Report all outcomes with equal prominence.

## 13. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 14. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
