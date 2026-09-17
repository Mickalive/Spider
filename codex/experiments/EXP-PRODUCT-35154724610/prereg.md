# EXP-PRODUCT-35154724610 — Real HTTP Binding Correctness for Parameterized Mechanisms

## Status

DESIGN NOT YET FROZEN.

## Parent Experiment

- **Experiment**: EXP-PRODUCT-35132898840
- **Lane**: product
- **Key Finding**: Fix1+Fix2+Fix3 distill_parameterized() produces 3 parameterized mechanisms from 5 synthetic API endpoints with string-match binding_accuracy=1.0, mechanism reduction 40% (method-excluded), protocol-only prevalence 19.23% on curated 52-URL corpus
- **Critical Audit Gap**: V2_BINDING_NOT_HTTP (HIGH) — binding accuracy validated by exact URL string equality, NOT by real HTTP execution. All 5 decision conditions pass arithmetically but measurement validity is compromised.
- **Carry Forward**: Fix1+Fix2+Fix3 code committed to src/spider/kernel.py; C-PARAM-INHERIT remains EXPERIMENTAL; C-PRODUCT-ECON remains HYPOTHESIS; all conditions synthetic with zero model/network/browser calls

## 1. Question

Do parameterized mechanisms induced by `distill_parameterized()` execute correctly over real HTTP, producing expected response states for unseen resource IDs — and does parameterized resolution reduce token cost compared to literal mechanism replay?

## 2. Hypothesis

Parameterized mechanisms from Fix1+Fix2+Fix3 `distill_parameterized()` in `src/spider/kernel.py` bind correctly to real HTTP endpoints (`jsonplaceholder.typicode.com`) with `binding_accuracy >= 1.0` on 3 parameterized endpoints × 3 unseen IDs each, and parameterized resolution uses fewer tokens than literal mechanism replay.

## 3. Falsifier

Any of:
1. `binding_accuracy < 1.0` on real HTTP execution (unexpected status, wrong body, connection failure, query encoding error)
2. Parameterized token cost ≥ literal token cost
3. Any existing kernel regression test fails after HTTP execution path is exercised

## 4. Inherited State

### Established (from parent handoff)
- Fix1+Fix2+Fix3 code restored and importable from `src/spider/kernel.py`
- `distill_parameterized` induces 1 slot 'url' on 3 synthetic P1_API_ENDPOINTS with string-match binding_accuracy=1.0
- Method-excluded mechanism count reduction 40% (3 vs 5); method-aware 20% (5 vs 4)
- Fix3 structural '/' delimiter check rejects scheme+authority-only prefixes
- Fix3 protocol-only prevalence 19.23% on curated 52-URL corpus (NOT live traffic)
- Existing kernel tests pass after Fix1+Fix2+Fix3 restoration

### Rejected (from parent handoff)
- Protocol-only over-parameterization IS real: unfixed produces slot_count=1 for protocol-only URLs
- Cross-host parameterization IS rejected by Fix2
- Method-conflated counting valid only when method is metadata

### Unknown (from parent handoff)
- Real HTTP binding correctness: all validation was string-match only
- Live browser traffic prevalence of protocol-only patterns
- Token cost per resolution with documented pricing
- C-PRODUCT-ECON end-to-end amortized cost
- Fix2 limitation: path-embedded version parameters fail
- resolve() tie-break from EXP-GRAPH-33816735314 not present

### Do Not Assume (from parent handoff)
- Do not assume binding_accuracy=1.0 applies to real HTTP endpoints
- Do not assume 40% reduction applies to real task sets
- Do not assume token cost savings reflects real economics
- Do not assume n=3+3 establishes statistical significance

## 5. Baselines

### B_LITERAL_HTTP_EXECUTION
Literal mechanism (exact URL template) executed over real HTTP for same unseen IDs. Serves as upper-bound cost reference and confirms endpoint reachability. Expected: all 9 literal HTTP calls succeed with correct status/body; literal token cost ≥ parameterized token cost.

### B_UNFIXED_PROTOCOL_ONLY
Unfixed heuristic (pre-Fix3) on same training observations. Confirms Fix3 necessity by showing unfixed produces over-parameterized templates for protocol-only URLs. Expected: unfixed slot_count=1 for protocol-only URLs while fixed produces slot_count=0.

## 6. Controls

### P1_REAL_HTTP_BINDING (Positive Control)
3 parameterized endpoints (fetch_posts GET, fetch_users GET, fetch_comments GET) executed over real HTTP with 3 unseen IDs each (99, 100, 101). Each call must return status 200 and valid JSON matching expected resource type. Expected: binding_accuracy = 1.0 (9/9 correct), all status=200, all response bodies valid JSON.

### N1_NONEXISTENT_ENDPOINT (Null Control)
Parameterized mechanism resolved with non-existent resource ID (999999) on each endpoint. HTTP execution must return 404 or empty array, not crash or return unrelated data. Expected: all 3 calls return status 404 or empty array; no crashes.

## 7. Measurement Validity

1. Real HTTP GET requests executed against `jsonplaceholder.typicode.com` for binding accuracy validation
2. Response status code and body verified against expected resource type (post/user/comment JSON schema)
3. Token cost measured by actual tokenization of resolution input/output, not arbitrary arithmetic
4. Training observations use same P1_API_ENDPOINTS as parent (fetch_posts 5 obs GET+PUT, fetch_users 3, fetch_comments 3); unseen IDs 99, 100, 101
5. Existing kernel regression tests re-run after HTTP execution to confirm no side effects

## 8. Decision Rule

All of:
1. P1_REAL_HTTP_BINDING binding_accuracy ≥ 1.0 (9/9 correct HTTP executions)
2. N1_NONEXISTENT_ENDPOINT all 3 calls return 404/empty without crash
3. B_LITERAL_HTTP_EXECUTION all 9 literal calls succeed
4. B_UNFIXED_PROTOCOL_ONLY confirms Fix3 necessity (unfixed slot_count > fixed for protocol-only URLs)
5. existing_kernel_tests all pass
6. parameterized_token_cost < literal_token_cost (actual tokenization)

If ANY condition fails, the experiment FALSIFIES the claim at the tested scope.

## 9. Product Consequence

### Positive Outcome
C-PARAM-INHERIT advances from EXPERIMENTAL toward PRODUCT_CORE with real HTTP binding correctness established; C-PRODUCT-ECON gains first real cost measurement; product may include parameterized mechanisms in shipping kernel with HTTP execution validated.

### Negative Outcome
C-PARAM-INHERIT REJECTED at real HTTP scope; parameterized mechanisms cannot be trusted for real endpoint execution; product must fall back to literal mechanism replay; C-PRODUCT-ECON remains HYPOTHESIS with no cost data.

## 10. Scope Limitations

This experiment tests ONLY:
- Real HTTP binding correctness (closes V2_BINDING_NOT_HTTP)
- Basic token cost comparison (partial closure of V4_TOKEN_COST_ARBITRARY)
- GET-only endpoints (method conflation V3 not tested — GET-only design avoids the issue)

This experiment does NOT test:
- Live browser traffic prevalence (V1 remains open)
- End-to-end amortized cost per successful real-browser task (C-PRODUCT-ECON remains HYPOTHESIS beyond token cost)
- Multi-slot induction (G4 bound persists)
- resolve() tie-break (inherited unresolved)
- Fix2 path-embedded version parameters (inherited limitation)
- Real LLM distillation (no model calls)
- Browser automation (no browser calls)
- Cross-site transfer

## 11. Estimated Cost

Low: single Python script with urllib/requests, 12 HTTP calls to free API, no LLM calls, no browser automation, ~2 minutes execution time.

## 12. Expected Information Gain

High: closes V2_BINDING_NOT_HTTP (highest-severity audit gap from parent); either validates or falsifies real HTTP binding correctness for parameterized mechanisms; enables or blocks C-PRODUCT-ECON cost measurement.
