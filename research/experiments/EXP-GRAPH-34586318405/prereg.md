# EXP-GRAPH-34586318405 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-GRAPH-34586318405
- **Lane**: Graph
- **Claims**: C-SEMANTIC-RESOLVE
- **Date**: 2026-09-11
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-GRAPH-34409639346 (C-SEMANTIC-RESOLVE falsified at current kernel level for simple path aliasing)

## 2. Scientific Question

Can the kernel handle query-parameter aliasing scenarios — where two mechanisms share the same intent but differ in URL template structure — and does HTTP execution success against real endpoints provide a grounding signal for template correctness that resolver selection alone cannot?

## 3. Motivation

The parent experiment (EXP-GRAPH-34409639346) established:
- Kernel uses exact intent matching (kernel.py L97: m.intent != intent)
- For equal-confidence candidates, selection determined by mechanism_id ordering via stable sort (L112)
- Aliased-first subset: 0/10 selects template-matching mechanism (binomial p=1.0)
- C-SEMANTIC-RESOLVE falsified at current kernel level for simple path aliasing

The parent's handoff identifies the next question: more complex aliasing scenarios (query parameters, path rewriting, server-side routing) and whether HTTP execution provides a grounding signal absent from resolver selection.

The parent experiment tested only simple path aliasing where both templates map to valid endpoints. It did not test:
1. Query-parameter aliasing (`/posts/{id}` vs `/posts?id={id}`)
2. Path rewriting (`/posts/${id}` where endpoint accepts both `/posts/1` and `/posts?id=1`)
3. Whether HTTP execution can distinguish correct from incorrect templates
4. Whether execution provides corrective signal when resolver selects incorrectly

This experiment addresses all four gaps using real HTTP endpoints.

## 4. Hypotheses

### H1: No Semantic Template Analysis
The kernel does not analyze URL template structure. In aliased-first conditions (where tie-breaking favors the aliased mechanism), the kernel selects the template-matching mechanism in 0% of cases (always follows tie-breaking).

### H2: HTTP Execution Provides Grounding Signal
HTTP execution against real endpoints identifies at least 1 case where the resolver-selected template fails HTTP execution (404/timeout) but an alternative registered template succeeds (HTTP 200). Grounding value > 0.

### H3: Baseline Integrity
All 6 baselines pass: B-EMPTY-REGISTRY (UNKNOWN), B-SINGLE-MECHANISM (EXECUTABLE), B-CONFIDENCE-HIGHER (higher confidence wins), B-CONFIDENCE-EQUAL-DIFFERENT-INTENT (exact match only), B-HTTP-POSITIVE (HTTP 200), B-HTTP-NEGATIVE (HTTP 404).

### H4: Execution-Resolver Divergence
There exist conditions where resolver selection and HTTP execution outcomes diverge: resolver picks template A but HTTP shows template B works and A does not. This divergence demonstrates that execution provides information absent from resolver selection.

## 5. Experimental Design

### 5.1 Kernel Resolution Layer

For each test condition:
1. Create fresh `MechanismRegistry` with controlled contents
2. Create `SpiderKernel` with `min_confidence=0.8`
3. Call `kernel.resolve(intent, context, params)` and record `Resolution` (status, mechanism_id, bound_action)
4. Do NOT execute HTTP in the kernel — HTTP execution is a separate measurement layer

### 5.2 HTTP Execution Layer

For each condition where the kernel returns EXECUTABLE with a bound_action:
1. Extract the URL from bound_action (template with parameters substituted)
2. Prepend base URL: `https://jsonplaceholder.typicode.com`
3. Execute HTTP GET with timeout=10s
4. Record: status_code, response_body_contains_expected_fields, latency_ms
5. HTTP success = status 200 AND body contains expected fields
6. HTTP failure = status != 200 OR timeout OR connection error

For aliased pairs, execute BOTH the resolver-selected template AND the alternative template.

### 5.3 Test Scenarios

#### Scenario A: Query-Parameter Aliasing (Both Templates Work)
Two mechanisms with same intent 'get-post-by-id', equal confidence 0.9:
- Mechanism a-alpha: template `/posts/${postId}` (path parameter)
- Mechanism z-alpha: template `/posts?id=${postId}` (query parameter)
- Both map to jsonplaceholder /posts/1 (known working)
- Aliased-first: z-alpha inserted first (larger ID), a-alpha second
- Expected resolver selection: a-alpha (smaller ID wins tie-break)
- Expected HTTP: both templates return 200 (both work)
- Grounding value: 0 (both work, no corrective signal)

#### Scenario B: Query-Parameter Aliasing (One Template Broken)
Two mechanisms with same intent 'get-post-comments', equal confidence 0.9:
- Mechanism a-beta: template `/posts/${postId}/comments` (correct nested path)
- Mechanism z-beta: template `/posts?id=${postId}/comments` (malformed query path)
- a-beta maps to jsonplaceholder /posts/1/comments (known working)
- z-beta maps to jsonplaceholder /posts?id=1/comments (404 — no such endpoint)
- Aliased-first: z-beta inserted first, a-beta second
- Expected resolver selection: a-beta (smaller ID wins tie-break)
- Expected HTTP: a-beta returns 200, z-beta returns 404
- Grounding value: depends on which template resolver selects

#### Scenario C: Path Rewriting (Same Resource, Different Patterns)
Two mechanisms with same intent 'list-user-posts', equal confidence 0.9:
- Mechanism a-gamma: template `/users/${userId}/posts` (nested path)
- Mechanism z-gamma: template `/users?userId=${userId}/posts` (query + path)
- a-gamma maps to jsonplaceholder /users/1/posts (known working)
- z-gamma maps to jsonplaceholder /users?userId=1/posts (404)
- Aliased-first: z-gamma inserted first, a-gamma second
- Expected resolver selection: a-gamma (smaller ID wins tie-break)
- Expected HTTP: a-gamma returns 200, z-gamma returns 404

#### Scenario D: Server-Side Routing (Multiple Valid Templates)
Two mechanisms with same intent 'get-album-photos', equal confidence 0.9:
- Mechanism a-delta: template `/albums/${albumId}/photos` (nested path)
- Mechanism z-delta: template `/photos?albumId=${albumId}` (query filter)
- Both map to jsonplaceholder endpoints that return photos
- a-delta: /albums/1/photos (200, returns photos)
- z-delta: /photos?albumId=1 (200, returns photos)
- Aliased-first: z-delta inserted first, a-delta second
- Expected resolver selection: a-delta (smaller ID wins tie-break)
- Expected HTTP: both return 200

### 5.4 Sample Size

- 4 aliased scenarios × 2 ID orderings = 8 aliased conditions
- Plus 2 additional scenarios (E, F) for broader coverage = 4 more conditions
- Total aliased conditions: 12 (6 scenarios × 2 orderings)
- Plus 6 baselines
- Total kernel calls: 18
- Total HTTP executions: up to 30 (18 resolver-bound + 12 alternative-template executions)

## 6. Controls

### 6.1 Positive Control (B-SINGLE-MECHANISM)
- One mechanism: intent='get-post-by-id', template='/posts/${postId}', preconditions={'method':'GET'}
- Kernel returns EXECUTABLE with bound_action={'url':'/posts/1','method':'GET'}
- HTTP GET https://jsonplaceholder.typicode.com/posts/1 returns 200 with userId field
- Verifies: resolution pipeline + HTTP execution pipeline both work

### 6.2 Null Control (B-EMPTY-REGISTRY)
- Empty registry returns UNKNOWN
- Verifies: kernel does not hallucinate candidates

### 6.3 HTTP Positive Control (B-HTTP-POSITIVE)
- Template '/posts/1' against jsonplaceholder -> HTTP 200
- Verifies: HTTP execution against real endpoint succeeds for known-good URL

### 6.4 HTTP Negative Control (B-HTTP-NEGATIVE)
- Template '/nonexistent-resource/999' against jsonplaceholder -> HTTP 404
- Verifies: HTTP execution correctly detects broken template

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

- **aliased_first_correct_selection_rate**: Fraction of aliased-first conditions where kernel selects the template-matching mechanism (H1)
- **http_grounding_value**: Number of conditions where resolver-selected template fails HTTP but alternative template succeeds (H2)
- **execution_resolver_divergence_count**: Number of conditions where resolver selection and HTTP execution outcomes diverge (H4)

### 7.2 Secondary Metrics

- **resolver_status_distribution**: Count of EXECUTABLE, UNKNOWN, EXPLORE across all conditions
- **http_success_rate_by_template_type**: HTTP success rate for path-parameter templates vs query-parameter templates
- **http_latency_ms**: HTTP execution latency (informational)
- **baseline_pass_rate**: Fraction of baselines that pass (H3)

### 7.3 Derived Metrics

- **grounding_value_ratio**: http_grounding_value / total_aliased_conditions (0 = execution provides no corrective signal; 1 = execution always corrects resolver)
- **resolver_execution_agreement**: Fraction of conditions where resolver selection and HTTP execution agree (both work or both fail)

## 8. Statistical Tests

### 8.1 Primary: Binomial Test (H1)
- H0: kernel selects template-matching mechanism in 50% of aliased-first conditions (chance)
- H1: kernel selects in 0% of conditions (always follows tie-breaking)
- Test: binomial test, n=6 (aliased-first conditions), k=0 (correct selections)
- One-sided, alpha=0.05
- Note: with n=6, 0/6 yields p=0.016 (significant); 1/6 yields p=0.109 (not significant)

### 8.2 Descriptive: Grounding Value (H2)
- http_grounding_value > 0 is sufficient for H2 support
- No formal hypothesis test — this is a count of corrective events
- Report exact count and which scenarios produced corrective signal

### 8.3 Baseline Verification (H3)
- All 6 baselines must pass (binary: pass/fail)
- No statistical test needed — deterministic pass/fail

## 9. Validity Threats

### 9.1 Network Reliability
HTTP execution against real endpoints may fail due to network issues. Mitigation: timeout=10s; retry once on timeout/connection error; record failures as measurement issues, not negative results. If >50% of HTTP executions fail, verdict = MEASUREMENT_INVALID.

### 9.2 Endpoint Stability
jsonplaceholder.typicode.com may change behavior. Mitigation: use well-known stable endpoints (/posts, /users, /albums, /comments, /photos). Verify B-HTTP-POSITIVE and B-HTTP-NEGATIVE before main conditions.

### 9.3 Small Sample Size
n=6 aliased-first conditions has limited power for binomial test. Mitigation: this is a proof-of-concept screen. 0/6 is significant (p=0.016); >=2/6 is not significant but would weaken the hypothesis. Report exact p-values and effect sizes.

### 9.4 Intent String Matching
All aliased mechanisms share the same intent string. The kernel's exact-match filter (L97) ensures both qualify as candidates. This is by design — we are testing tie-breaking behavior, not intent filtering.

### 9.5 Template Parameter Binding
All templates use `${param}` syntax. The kernel's `_bind()` function (L35-49) substitutes parameters. If a template has incorrect parameter names, binding may produce malformed URLs. Mitigation: all templates use parameter names that exist in the provided params dict.

### 9.6 HTTP Execution Scope
HTTP execution tests GET requests only. POST, PUT, DELETE, PATCH are out of scope. This bounds the claim to read-only template validation.

## 10. Decision Rules

### 10.1 SURVIVES_CURRENT_TEST
If ALL of:
1. All 6 baselines pass
2. No exceptions or crashes across all kernel calls
3. Aliased-first correct selection rate = 0% (0/6 aliased-first conditions select template-matching mechanism)
4. HTTP grounding value > 0 (at least 1 case where resolver-selected template fails HTTP but alternative succeeds)

### 10.2 FALSIFIED-IN-SETTING
If ANY of:
1. Aliased-first correct selection rate > 0% (kernel shows semantic template analysis)
2. HTTP grounding value = 0 across all scenarios (execution cannot correct resolver mispredictions)
3. Any baseline fails
4. >50% of HTTP executions fail due to infrastructure issues (then MEASUREMENT_INVALID instead)

### 10.3 MEASUREMENT_INVALID
If:
1. >50% of HTTP executions fail due to network/infrastructure issues
2. Kernel crashes or throws exceptions in >50% of conditions
3. jsonplaceholder.typicode.com is unreachable during execution window

## 11. Expected Outcomes

### 11.1 SURVIVES_CURRENT_TEST (Most Likely)
- Kernel follows tie-breaking exactly (0/6 aliased-first correct selections) — consistent with parent
- HTTP execution identifies at least 1 case where resolver-selected template fails but alternative succeeds
- Demonstrates: execution provides corrective signal absent from resolver selection
- Product consequence: 'resolve then validate' pattern is viable; include HTTP execution validation in resolution pipeline
- C-SEMANTIC-RESOLVE remains falsified at resolver level but gains practical mitigation

### 11.2 FALSIFIED (Grounding Value = 0)
- Kernel follows tie-breaking (0/6) but HTTP execution never corrects resolver
- This happens if: in all aliased-first conditions, the resolver-selected template happens to be the one that works (lucky tie-breaking)
- Or if: both templates always work or always fail (no discriminative signal)
- Product consequence: neither resolver selection nor execution can distinguish correct templates; must require exact intent matching
- Graph lane should pivot to other priority claims (C-FRESHNESS, C-DELTA-REPAIR)

### 11.3 FALSIFIED (Kernel Shows Semantic Analysis)
- Kernel selects template-matching mechanism in >0% of aliased-first conditions
- Would be surprising given code analysis and parent result
- Product consequence: kernel has unrecognized capability; re-evaluate C-SEMANTIC-RESOLVE
- Requires replication with larger sample

### 11.4 MEASUREMENT_INVALID
- Network/infrastructure failures prevent measurement
- Not scientific evidence; retry with network diagnostics

## 12. Analysis Plan

1. **Baseline Verification**: Execute all 6 baselines. If any fail, stop and report MEASUREMENT_INVALID.
2. **Aliased Conditions**: Execute 6 aliased scenarios × 2 ID orderings = 12 conditions.
3. **Resolver Recording**: For each condition, record kernel.resolve() output (status, mechanism_id, bound_action).
4. **HTTP Execution**: For each EXECUTABLE result, execute bound_action URL against jsonplaceholder. For aliased pairs, execute BOTH templates.
5. **Metric Computation**: Compute aliased_first_correct_selection_rate, http_grounding_value, execution_resolver_divergence_count.
6. **Statistical Tests**: Binomial test on aliased-first subset.
7. **Control Checks**: Verify all controls pass.
8. **Reporting**: Report all outcomes with equal prominence.

## 13. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 14. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
