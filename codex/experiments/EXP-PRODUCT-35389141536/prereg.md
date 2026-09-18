# Preregistration: EXP-PRODUCT-35389141536

## Experiment Identity

- **Experiment ID:** EXP-PRODUCT-35389141536
- **Lane:** product
- **Claim:** C-PRODUCT-ECON (SPIDER saves total cost per successful task after retrieval, verification and maintenance)
- **Parent:** EXP-PRODUCT-35375591046 (MEASUREMENT_INVALID, no LLM API keys, 0/32 tasks)
- **Grandparent:** EXP-PRODUCT-35353007958 (MEASUREMENT_INVALID, no LLM API keys, 0/32 tasks)
- **Most recent valid measurement:** EXP-PRODUCT-35330741529 (analytical 5.42% token savings, audit REVISE)

## Motivation

Two consecutive PRODUCT lane experiments were MEASUREMENT_INVALID due to identical infrastructure failure: no LLM API keys. Zero evidence was produced across two cycles. The frozen COLD baseline design requires real LLM API calls and cannot execute without API credentials.

The parent handoff offers three options:
- (A) Configure LLM API access and retry -- requires external provisioning unavailable here
- (B) Close token-based inheritance economics entirely -- premature without measuring browser/verification costs
- (C) Pivot to measuring browser/verification costs -- directly testable without LLM API

This experiment implements option (C). It is the smallest high-information experiment that can change a product decision because: (1) it does NOT require LLM API keys, (2) it directly answers whether browser/verification costs dominate the 5.42% token savings, and (3) either outcome changes the C-PRODUCT-ECON decision.

## Inherited State

### Established

- Analytical deduplication economics on synthetic 32-task corpus: parameterized 25 vs literal 32 mechanisms (21.9% reduction), selection savings 3168 tokens (16.09%), resolution overhead 2101 tokens (10.67%), net workflow savings 1067 tokens (5.42%) -- from EXP-PRODUCT-35330741529
- Positive control validated analytically: 5 blog-read-post tasks collapse to 1 parameterized pattern -- from EXP-PRODUCT-35330741529
- Null control passes analytically: unique-pattern overhead 1.85% (ratio 1.0185) -- from EXP-PRODUCT-35330741529
- COLD baseline at 77 tokens/task is 8x cheaper than either registry condition -- from EXP-PRODUCT-35330741529

### Rejected

- Token savings as general claim for short-value URL patterns: FALSIFIED (EXP-PRODUCT-35209109455)
- Token savings as general claim for long-value URL patterns: FALSIFIED (EXP-PRODUCT-35262262156)
- Producer SUPPORTS for EXP-PRODUCT-35330741529: NOT JUSTIFIED (C1 unmeasured, C2/C3 narrow under estimated completions)

### Unknown (resolved by this experiment)

- Whether browser/verification costs dominate the 5.42% token savings -- PRIMARY QUESTION
- Whether total workflow cost (token + browser + verification) for parameterized remains <= literal
- Whether COLD browser cost equals LITERAL/PARAMETERIZED (same HTTP requests, different URL source)

### Do Not Assume

- Do not assume 5.42% workflow savings generalizes to real SPIDER corpus
- Do not assume C1 100% success -- assumed analytically, not measured with real LLM
- Do not assume completion tokens are accurate -- hard-coded estimates
- Do not assume browser/verification costs are negligible -- that is what this experiment measures
- Do not assume C-PRODUCT-ECON is measured -- remains HYPOTHESIS
- Do not assume this MEASUREMENT_INVALID parent is a scientific negative

## Hypothesis

H1: Browser execution time is non-zero and measurable for the 32-task corpus via HTTP requests.

H2: Verification overhead (response parsing, status validation) adds non-trivial cost per task.

H3: LITERAL vs PARAMETERIZED browser cost difference is negligible (both execute identical HTTP actions; only URL source differs).

H4: Total workflow cost (token + browser + verification) for PARAMETERIZED remains <= LITERAL after adding measured browser/verification costs.

## Falsifier

F1 (INFRASTRUCTURE): Browser execution time is 0 or unmeasurable for all tasks -- triggers MEASUREMENT_INVALID.

F2 (ECONOMIC): Total browser+verification cost difference between LITERAL and PARAMETERIZED exceeds 10% of token savings (106.7 token-equivalent), OR total workflow cost PARAMETERIZED > LITERAL after adding browser/verification -- triggers FALSIFIED-IN-SETTING.

## Measurement Protocol

### Step 1: Task Corpus Remapping

The frozen 32-task corpus from EXP-PRODUCT-35330741529 references example.com and blog.example.com URLs. These are remapped to jsonplaceholder.typicode.com endpoints with equivalent structure:

- blog.example.com/posts/{id} -> jsonplaceholder.typicode.com/posts/{id}
- api.example.com/users/{id} -> jsonplaceholder.typicode.com/users/{id}
- api.example.com/posts -> jsonplaceholder.typicode.com/posts
- Remaining tasks mapped to equivalent jsonplaceholder endpoints or localhost mock

### Step 2: Browser Execution Cost Measurement

For each of the 32 tasks:
1. Record start time via time.perf_counter()
2. Execute HTTP request via Python requests library (GET/POST as per task specification)
3. Record end time after receiving full response
4. Compute browser_execution_time_ms = (end - start) * 1000
5. Repeat 3 times per task; report median

### Step 3: Verification Cost Measurement

For each task response:
1. Record verification start time
2. Parse response body (json.loads for JSON responses)
3. Validate HTTP status code (200 for success tasks, 403/404 for null control tasks)
4. Validate response content type
5. Record verification end time
6. Compute verification_time_ms = (end - start) * 1000

### Step 4: Cost Aggregation

- Per-task total browser cost = browser_execution_time_ms + verification_time_ms
- Per-condition total = sum across 32 tasks
- Token-equivalent conversion: 1ms ~ 1 token (rough approximation for cost comparison)
- Compare: PARAMETERIZED total workflow cost (18624 tokens + browser_ms) vs LITERAL (19691 tokens + browser_ms) vs COLD (2475 tokens + browser_ms)

### Step 5: Control Validation

- Positive control: 5 blog-read-post tasks must return HTTP 200 with valid JSON
- Null control: 3 admin/auth tasks must return error status (403/404/401)

## Decision Rule

SURVIVES_CURRENT_TEST requires ALL of:

- **C1:** Browser execution time measurable for >=25/32 tasks (at least 78% completion)
- **C2:** Median verification time >0 for >=20/32 tasks
- **C3:** LITERAL vs PARAMETERIZED browser cost difference <106.7 token-equivalent (10% of 1067 token savings)
- **C4:** Total workflow cost (token + browser + verification) for PARAMETERIZED <= LITERAL
- **C5:** Positive control 5/5 success

MEASUREMENT_INVALID if C1 fails (browser execution infrastructure unavailable).

FALSIFIED-IN-SETTING if C3 or C4 fails (browser costs offset or exceed token savings).

MIXED if C1-C3 pass but C4 fails (browser costs wipe out token savings in total workflow).

## Consequences

**Positive outcome (SURVIVES):** Browser/verification costs are small relative to token savings. The 5.42% analytical token savings is preserved in end-to-end workflow cost. Supports C-PRODUCT-ECON advancing. Validates token-based deduplication as economically viable.

**Negative outcome (FALSIFIED):** Browser/verification costs dominate token savings. The 5.42% token savings is illusory in practice. Falsifies token-based economics line. Redirects product lane to non-token mechanisms or closes C-PRODUCT-ECON.

**Infrastructure failure (MEASUREMENT_INVALID):** Cannot measure browser costs. Third consecutive MEASUREMENT_INVALID in product lane. Director decision required: provision infrastructure or close economics line.
