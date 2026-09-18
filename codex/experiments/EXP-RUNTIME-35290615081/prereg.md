# EXP-RUNTIME-35290615081 — Preregistration

## Status

DESIGN ONLY. Not yet frozen.

## Parent

EXP-RUNTIME-35280364816 (handoff sha256: c499c6aa50143e5be429c187b3b78d3298a10b0ea5fc730693b887ae4ba80c7c)

## Question

Does iterative decompression restore decompressed body-only discrimination >= 0.3 and decompressed hash determinism (all_same=true) under triple-brotli encoding for the valid_token success body when triple-br is guaranteed to be observed via stratified scenario assignment?

## Background and Motivation

The parent experiment (EXP-RUNTIME-35280364816) validated iterative decompression (brotli→gzip→identity loop to max_depth=5) for multi-layer encoding. It established:

- Double-brotli for ALL 4 auth states: discrimination 0.5, determinism all_same=true ✓
- Triple-brotli for error states (no_auth/expired_token/invalid_token): 81 observations, 0 decompression errors ✓
- Single-layer scenarios (correct_br, missing_ce, incorrect_gzip, garbled_ce): no regression ✓
- Decompression latency: 0.012-0.27ms ✓

**The ONE gap**: valid_token × triple-br was NEVER observed (0/180 reps across all 9 conditions). The audit V1 (severity high) identified the root cause: `scenario_rng = random.Random(SEED + 7919)` at line 736 consumed one draw for the proxy connectivity test (lines 741-749), shifting the scenario distribution. valid_token received triple_br in 0/180 observed requests despite triple_br being 1/6 of the theoretical distribution.

This is a **measurement defect**, not a scientific negative. The iterative decompression mechanism is state-agnostic — it iterates brotli→gzip→identity regardless of body content. If it handles triple-br for error bodies (which it does, 81/81), there is no mechanistic reason it would fail for the success body. But this must be verified experimentally.

## Design

### Fix: Stratified Round-Robin Scenario Assignment

Replace the parent's `scenario_rng.choice(ENCODING_SCENARIOS)` with deterministic round-robin assignment:

```
For each condition (content_type × size):
  For each auth_state (4 states × 20 reps = 80 requests):
    scenario = ENCODING_SCENARIOS[request_index % 6]
```

This guarantees:
- Each scenario appears ⌊80/6⌋ = 13 or ⌈80/6⌉ = 14 times per condition
- **valid_token × triple_br appears at least 13 times per condition** (was 0 in parent)
- No RNG dependency between proxy test and measured requests

### Proxy Connectivity Test Fix

The proxy connectivity test (lines 741-749 in parent) must NOT consume from the measured-request scenario RNG. Options:
1. Use a separate `test_rng = random.Random(SEED + 9999)` for the proxy test
2. Skip the proxy test entirely (it's diagnostic, not measurement)
3. Pre-assign all scenarios before any requests, decoupling test from measurement

Option 1 is preferred: preserve the connectivity diagnostic without affecting measurement.

### What Does NOT Change

Everything else from the parent is frozen:
- Mock server: localhost, brotli quality 6, same 4 auth states, same 3 content types × 3 sizes
- CDN proxy: same 6 encoding scenarios, same transformation logic
- Iterative decompression: same `decompress_body()` loop with max_depth=5
- Request ordering: same `rng = random.Random(SEED)` shuffle of (state, rep) pairs
- N=20 reps per state per condition, seed=44
- Metrics: decompressed_body_only_discrimination, decompressed hash determinism

### Expected Outcome

If iterative decompression is truly state-agnostic:
- valid_token × triple_br decompressed hash = single-layer hash (determinism holds)
- Discrimination = 0.5 (identical to all other passing combinations)
- Claim ceiling advances to "triple-brotli for all auth states"

If triple-br fails for valid_token:
- Discrimination < 0.3 or hash mismatch
- Failure must be characterized: is it depth-related? body-size-related? content-related?
- Claim ceiling remains bounded to "triple-brotli for error states only"

## Hypothesis

H1: Iterative decompression produces decompressed hash for valid_token × triple-br that matches the single-layer hash (all_same=true across encoding scenarios for valid_token).

H0 (falsifier): The decompressed hash for valid_token × triple-br differs from the single-layer hash, OR discrimination < 0.3.

## Decision Rule

**SURVIVES_CURRENT_TEST** if ALL of:

1. **Stratified coverage**: valid_token × triple_br has ≥1 observation per condition
2. **Triple-br survival**: decompressed body-only discrimination >= 0.3 for valid_token × triple_br at all content types × sizes
3. **Determinism**: decompressed hash variation all_same=true for valid_token × triple_br
4. **Regression**: decompressed body-only discrimination >= 0.3 for ALL (state, scenario) combinations from parent
5. **Regression determinism**: all_same=true for all conditions
6. **Null control**: B-RANDOM = 0.0
7. **Encoding variation**: C_STRATIFIED_COVERAGE passes

**FALSIFIED-IN-SETTING** if:
- valid_token × triple-br discrimination < 0.3 at any condition
- valid_token × triple-br hash differs from single-layer hash
- Any previously-passing (state, scenario) regresses

**MEASUREMENT_INVALID** if:
- Stratified coverage fails (valid_token triple-br not observed)
- Infrastructure failure prevents valid measurements

## Baselines

| ID | Description | Expected |
|---|---|---|
| B-PARENT-DOUBLE-BR-ALL-STATES-0.5 | Parent double-br discrimination for all states | 0.5 |
| B-PARENT-TRIPLE-BR-ERROR-STATES-0.5 | Parent triple-br discrimination for error states | 0.5 |
| B-SINGLE-PASS-0.2911 | Grandparent single-pass discrimination | 0.2911 |
| B-RANDOM | Random fingerprint discrimination | ~0.0 |
| B-COMPRESSED-BYTE-ONLY | Compressed-bytes-only discrimination | < 0.5 |

## Controls

| ID | Type | Description |
|---|---|---|
| C_STRATIFIED_COVERAGE | Positive | Every (state, scenario) pair appears ≥1 per condition |
| C_NULL_CONTROL | Null | B-RANDOM ~ 0.0 |

## Measurement Validity Threats

1. **Round-robin periodicity**: If request ordering interacts with round-robin scenario assignment, some (state, scenario) pairs could be systematically correlated. Mitigation: the parent's `rng.shuffle(plan)` randomizes request order, so round-robin scenario assignment is applied to a shuffled sequence.

2. **Proxy test interference**: If the connectivity test is not fully decoupled from measurement RNG, the parent defect could recur. Mitigation: use a completely separate RNG instance for the test.

3. **Success body triple-br failure mechanism**: If triple-br actually fails for valid_token (not just unobserved), the stratified assignment will reveal this. This is the desired discriminating outcome.

4. **Localhost ceiling**: Results are bounded to localhost mock server with deterministic brotli quality 6. Real CDN infrastructure (Cloudflare/Fastly/Akamai) is not tested. This is an inherited limitation from the parent.

## Product Consequence

- **Positive**: Claim ceiling advances to "triple-brotli for all auth states including success body" on localhost. Unblocks full multi-layer encoding confidence for CDN deployment.
- **Negative**: Triple-br fails for success body. Product must restrict CDN to max 2 compression layers or add layer-count validation.

## Estimated Cost

< 5000 tokens, < 3 minutes. Same infrastructure as parent. Marginal cost is the scenario assignment fix only.

## Expected Information Gain

HIGH. This is the smallest possible experiment that resolves the ONE untested condition. Not a repetition of the parent — a minimal targeted fix for the specific measurement defect identified by audit V1.
