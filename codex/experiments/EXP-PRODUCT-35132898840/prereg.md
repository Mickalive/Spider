# EXP-PRODUCT-35132898840 preregistration

## Experiment Identity

- **experiment_id**: EXP-PRODUCT-35132898840
- **lane**: product
- **claim_ids**: C-PARAM-INHERIT, C-PRODUCT-ECON
- **parent_handoff**: EXP-PRODUCT-35130681515
- **created_at**: 2026-09-16T18:12:13.956002+00:00

## Question

Does the parameterized distillation kernel (Fix1+Fix2+Fix3) save total cost per successful real-browser task compared to literal mechanism replay, and what is the prevalence of protocol-only over-parameterization patterns in live browser traffic?

## Hypothesis

The parameterized kernel reduces the total cost per successful task by (a) requiring fewer distinct mechanisms to cover a realistic task set (mechanism count reduction), and (b) enabling correct binding to unseen parameter values without new mechanism creation. The cost savings from mechanism count reduction and reuse exceed the overhead of parameter resolution (model tokens for slot extraction + binding computation). Protocol-only patterns affect <10% of real API URL patterns in live browser traffic, bounded by Fix3.

## Falsifier

Any of:
1. The parameterized kernel requires >=80% as many mechanisms as the literal baseline (mechanism count reduction <20%)
2. Parameterized binding accuracy drops below 0.8 on real HTTP endpoints
3. Protocol-only patterns affect >30% of real API URL patterns, implying the parameterized kernel is fundamentally misdesigned for real traffic
4. The parameterized kernel produces incorrect bindings that cause task failure on any real endpoint

## Baselines

### B_LITERAL_MECHANISM_COUNT
Number of distinct literal mechanisms needed to cover all tasks (one mechanism per unique URL). Expected: N mechanisms for N unique URLs. Upper bound on parameterized kernel cost.

### B_LITERAL_TOKEN_COST
Estimated model token cost for literal mechanism resolution (selecting from N candidates). Expected: O(log N) tokens per resolution.

### B_UNFIXED_PROTOCOL_ONLY
Unfixed heuristic on live URL corpus. Expected: over-parameterized templates for protocol-only URLs, quantifying Fix3 necessity in real traffic.

## Positive Control

### P1_API_ENDPOINTS
5 real JSONPlaceholder API endpoints:
- GET /posts/{id}
- GET /users/{id}
- GET /comments?postId={id}
- POST /posts
- PUT /posts/{id}

Parameterized kernel induces 3 mechanisms (posts/{id} shared by GET/PUT, users/{id}, comments?postId={id}) vs 5 literal mechanisms. Binding accuracy=1.0 on unseen IDs.

## Null Control

### N1_PROTOCOL_ONLY_LIVE
Real-world protocol-only URLs sampled from live browser traffic (e.g., https://, http://, https://a.com). Fix3 should reject all: slot_count=0. Measures prevalence of false-positive parameterization in real traffic.

## Measurement Validity

1. Fix1+Fix2+Fix3 code must be restored to src/spider/kernel.py before execution (currently absent from HEAD, referenced at sha256=8aed6377 in parent verdict)
2. Real HTTP endpoints used (jsonplaceholder.typicode.com) for binding accuracy validation
3. Protocol-only prevalence measured on actual live URLs from browser traffic logs or URL corpora
4. Mechanism count comparison uses identical task sets for parameterized and literal baselines
5. Token cost estimation uses conservative bounds (model pricing documentation, not live LLM calls)

## Decision Rule

If ALL of:
1. Fix1+Fix2+Fix3 code restored and importable from src/spider/kernel.py
2. Parameterized kernel produces correct bindings (binding_accuracy >= 0.8) on all 5 P1_API_ENDPOINTS with unseen IDs
3. Mechanism count reduction >= 20% (parameterized mechanisms <= 80% of literal mechanisms)
4. Protocol-only prevalence in live URL corpus < 30%
5. No task failures caused by incorrect parameterized bindings

Verdict = SURVIVES_CURRENT_TEST

If any condition (2-4) fails: verdict = FALSIFIED-IN-SETTING

## Product Consequences

### Positive
C-PRODUCT-ECON advances from HYPOTHESIS to EXPERIMENTAL with measured mechanism count reduction and protocol-only prevalence. Product lane has quantitative evidence for cost savings claim. Path to real-browser agent testing with model/network/browser calls is validated.

### Negative
If mechanism count reduction is <20% or protocol-only prevalence >30%, C-PRODUCT-ECON remains HYPOTHESIS. Product lane cannot claim cost savings without stronger evidence. Alternative approaches (domain-aware validation, authority-boundary check) needed before re-evaluation.

## Estimated Cost

Low: real HTTP endpoints (jsonplaceholder.typicode.com, free), protocol-only URL sampling (web search or public URL corpus), mechanism count comparison (offline computation), token cost estimation (model pricing lookup). Zero LLM calls, zero browser automation. ~20 operations total.

## Expected Information Gain

High: directly measures the two unknowns from parent handoff (C-PRODUCT-ECON cost savings and protocol-only prevalence). Either validates the parameterized kernel's economic viability or identifies fundamental design issues. The mechanism count reduction is the core economic signal; protocol-only prevalence bounds the real-world significance of the Fix3 boundary condition.

## Inherited State (from parent handoff EXP-PRODUCT-35130681515)

### Established
- Fix3 (_is_protocol_only_prefix structural '/' check) closes Fix2 protocol-only gap
- All 5 parent established single-slot URL classes preserved with Fix1+Fix2+Fix3
- Nulls N1_ORIGINAL/N1_CORRECTED slot_count=0
- Fix1/Fix2/Fix3 necessity quantified
- B_LITERAL fail_rate=1.0 confirms parameterized induction necessary
- Template invariance preserved
- Committed-code synthetic single-slot with prefix metadata

### Rejected
- Protocol-only over-parameterization is NOT hidden
- Cross-host parameterization IS rejected by Fix2
- Realistic corpus prevalence measurement is illustrative only

### Unknown
- End-to-end product economics (C-PRODUCT-ECON): does parameterized kernel save total cost per successful real-browser task?
- Real-browser external validity: prevalence of protocol-only vs minimal-path URL patterns in live browser traffic
- Real-world URL pattern prevalence
- VALUE CONTRACT slot_prefixes consumption
- Fix2 limitation: path-embedded version parameters
- Multi-slot induction (G4 architectural bound)

### Do Not Assume
- C-PARAM-INHERIT is VALIDATED or SHIPPED (remains EXPERIMENTAL)
- promote_to_product=true
- Fix3 eliminates all protocol-only over-parameterization
- The frozen 12-char threshold was implemented (structural check, not length)
- slot_prefixes changes action_template or _bind
- overall_condition_pass_rate=0.778 represents decision-rule performance
- n=3+3 per condition establishes statistical significance
- Fix3 threshold is length-based
