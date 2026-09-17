# EXP-PRODUCT-35209109455 preregistration

## Status

DESIGN ONLY — not yet frozen.

## Experiment Identity

- **experiment_id**: EXP-PRODUCT-35209109455
- **lane**: product
- **claim_ids**: C-PARAM-INHERIT, C-PRODUCT-ECON
- **parent**: EXP-PRODUCT-35185290656 (handoff sha256: 760f0152...)

## Question

Does parameterized mechanism representation reduce token cost compared to literal mechanism representation across multiple URL patterns with varying parameter counts (1-3 params), and does the resolve/bind pipeline correctly handle manually-registered parameterized mechanisms in the current kernel.py HEAD?

## Hypothesis

Parameterized mechanisms (with `${var}` template slots) use fewer tiktoken tokens than literal mechanisms encoding the same action information, and the savings increase with parameter count.

### Rationale

The parent experiment measured a single data point: 68 tokens (parameterized) vs 96 tokens (literal) for `comments?postId=${url}`, a 29.17% savings. This is a structural advantage (template slots replace concrete values), but:
- Single data point cannot establish generalizability
- Different URL patterns (path params, query params, mixed) may have different savings profiles
- Multi-parameter patterns (2-3 params) may have different savings than single-parameter
- Token cost is a prerequisite for C-PRODUCT-ECON end-to-end measurement

This experiment generalizes from 1 pattern to 5 patterns with 1-3 parameters, measuring the distribution of token savings.

## Falsifier

Parameterized mechanisms use more or equal tokens than literal mechanisms for the majority of test patterns, OR token savings do not increase monotonically with parameter count, OR resolve() fails to return EXECUTABLE with correct bound_action for manually-registered parameterized mechanisms.

## URL Pattern Corpus (5 patterns, 15 observations total)

### Pattern 1: Single path parameter (1 param)
```
Training observations:
  {"intent": "fetch_user", "action": {"method": "GET", "url": "https://api.example.com/users/1"}}
  {"intent": "fetch_user", "action": {"method": "GET", "url": "https://api.example.com/users/2"}}
  {"intent": "fetch_user", "action": {"method": "GET", "url": "https://api.example.com/users/3"}}

Expected parameterized template: {"method": "GET", "url": "https://api.example.com/users/${id}"}
Expected slots: ["id"]
Expected token savings: moderate (1 param replaces 1-3 char values)
```

### Pattern 2: Single query parameter (1 param)
```
Training observations:
  {"intent": "fetch_comments", "action": {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=1"}}
  {"intent": "fetch_comments", "action": {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=2"}}
  {"intent": "fetch_comments", "action": {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=3"}}

Expected parameterized template: {"method": "GET", "url": "https://jsonplaceholder.typicode.com/comments?postId=${id}"}
Expected slots: ["id"]
Expected token savings: moderate
```

### Pattern 3: Two query parameters (2 params)
```
Training observations:
  {"intent": "search_posts", "action": {"method": "GET", "url": "https://api.example.com/posts?userId=1&limit=10"}}
  {"intent": "search_posts", "action": {"method": "GET", "url": "https://api.example.com/posts?userId=2&limit=20"}}
  {"intent": "search_posts", "action": {"method": "GET", "url": "https://api.example.com/posts?userId=3&limit=30"}}

Expected parameterized template: {"method": "GET", "url": "https://api.example.com/posts?userId=${userId}&limit=${limit}"}
Expected slots: ["userId", "limit"]
Expected token savings: higher than 1-param (2 template slots)
```

### Pattern 4: Path + query parameter (2 params, mixed)
```
Training observations:
  {"intent": "fetch_user_posts", "action": {"method": "GET", "url": "https://api.example.com/users/1/posts?page=1"}}
  {"intent": "fetch_user_posts", "action": {"method": "GET", "url": "https://api.example.com/users/2/posts?page=2"}}
  {"intent": "fetch_user_posts", "action": {"method": "GET", "url": "https://api.example.com/users/3/posts?page=3"}}

Expected parameterized template: {"method": "GET", "url": "https://api.example.com/users/${userId}/posts?page=${page}"}
Expected slots: ["userId", "page"]
Expected token savings: higher than 1-param
```

### Pattern 5: Three query parameters (3 params)
```
Training observations:
  {"intent": "filter_products", "action": {"method": "GET", "url": "https://api.example.com/products?category=books&minPrice=10&maxPrice=50"}}
  {"intent": "filter_products", "action": {"method": "GET", "url": "https://api.example.com/products?category=electronics&minPrice=20&maxPrice=100"}}
  {"intent": "filter_products", "action": {"method": "GET", "url": "https://api.example.com/products?category=clothing&minPrice=5&maxPrice=30"}}

Expected parameterized template: {"method": "GET", "url": "https://api.example.com/products?category=${category}&minPrice=${minPrice}&maxPrice=${maxPrice}"}
Expected slots: ["category", "minPrice", "maxPrice"]
Expected token savings: highest (3 template slots)
```

## Controls

### Positive Control: P1_RESOLVE_PARAM_EXECUTABLE
- Register a parameterized mechanism with `parameter_slots=["id"]` and `action_template={"method": "GET", "url": "https://api.example.com/users/${id}"}`
- Call `resolve("fetch_user", {}, {"id": "42"})`
- Expected: `status=EXECUTABLE`, `bound_action={"method": "GET", "url": "https://api.example.com/users/42"}`
- Validates the resolve/bind pipeline works with parameter_slots

### Null Control: N1_RESOLVE_PARAM_UNKNOWN
- Register the same parameterized mechanism
- Call `resolve("fetch_user", {}, {})` (no parameters)
- Expected: `status=UNKNOWN` (required_slots not satisfied)
- Confirms parameter_slots guard is active

### Regression Baseline: B_LITERAL_TOKEN_COST
- For each of the 5 patterns, create a literal mechanism (full URL, no template slots)
- Measure token cost of literal action_template
- Compare against parameterized token cost

## Measurement Methodology

### Token Encoding
- Use `tiktoken` library with `cl100k_base` encoding (GPT-4/GPT-4o tokenizer)
- Encode the `action_template` JSON serialization: `json.dumps({"method": "GET", "url": "..."}, sort_keys=True)`
- Token count = `len(encoding.encode(json_str))`

### Mechanism Construction
- **Literal mechanisms**: Create directly from training observation (full URL in action_template)
- **Parameterized mechanisms**: Manually construct from training observations using `_find_common_prefix_suffix` logic to identify varying values, create `${var}` templates
- Both use `confidence=0.9` (above min_confidence 0.8)
- Both registered in same MechanismRegistry

### Token Savings Calculation
```
savings_pct = (literal_tokens - parameterized_tokens) / literal_tokens * 100
```

### Per-Pattern Test Parameters
- Pattern 1: `{"id": "42"}`
- Pattern 2: `{"id": "5"}`
- Pattern 3: `{"userId": "5", "limit": "25"}`
- Pattern 4: `{"userId": "5", "page": "3"}`
- Pattern 5: `{"category": "tools", "minPrice": "15", "maxPrice": "75"}`

## Decision Rule (ALL must pass)

| ID | Condition | Threshold |
|----|-----------|-----------|
| C1 | resolve() returns EXECUTABLE for all 5 parameterized mechanisms | 5/5 |
| C2 | resolve() returns UNKNOWN for all 5 when parameters missing | 5/5 |
| C3 | _bind() produces correct bound_action for all 5 | 5/5 |
| C4 | Parameterized uses fewer tokens than literal per pattern | >= 4/5 patterns |
| C5 | Mean token savings percentage across 5 patterns | >= 15% |
| C6 | 3-param savings > 1-param savings (monotonic increase) | True |
| C7 | Existing kernel tests pass (regression) | 3/3 |

**Verdict**: ALL C1-C7 pass → SURVIVES_CURRENT_TEST. Any failure → FALSIFIED-INSETTING.

## Scope Limitations

1. **tiktoken not LLM tokenizer**: Token cost measured via tiktoken cl100k_base, not actual LLM inference tokenizer. Savings may differ with different tokenizers.
2. **No LLM inference cost**: Only representation cost measured, not inference cost (prompt construction, attention, output generation).
3. **Manual mechanism construction**: distill_parameterized() not in current HEAD; mechanisms constructed manually. Does not test parameter induction algorithm.
4. **Deterministic synthetic observations**: All training data is hand-crafted, not from real browser sessions.
5. **No browser automation, no model calls**: Pure in-kernel measurement.
6. **GET only**: No PUT/POST/DELETE methods tested.
7. **No cross-site**: All patterns use api.example.com or jsonplaceholder.typicode.com.
8. **Single confidence level**: All mechanisms use confidence=0.9.

## Inherited State (from parent handoff)

### Established
- Fix3 redesign validated: _is_protocol_only_prefix correctly rejects bare authority, accepts query-parameterized
- Kernel regression tests pass 3/3 after Fix3 redesign
- HTTP binding accuracy 1.0 (3/3) on query-parameterized endpoint with unseen IDs
- distill_parameterized with Fix3 produces correct Mechanism for query-parameterized observations

### Rejected
- Fix3 independent necessity over Fix2 not demonstrated (mutually exclusive for all non-trivial prefixes)

### Unknown
- Token savings generalization beyond single pattern
- HTTP generalization beyond single endpoint
- PUT/POST method fidelity
- End-to-end amortized cost

### Do Not Assume
- C-PARAM-INHERIT is VALIDATED or PRODUCT_CORE (remains EXPERIMENTAL)
- Token cost savings of 29.17% reflect real economics
- HTTP binding generalizes to PUT/POST, multi-slot, cross-site
- n=3 establishes statistical significance
