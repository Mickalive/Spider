# Preregistration: EXP-FRONTIER-36293269574

**Lane**: frontier
**Claim**: C-CROSSSITE (cross-site transfer)
**Director Mandate**: PIVOT from synthetic plan family to real credential-free public websites with true holdout
**Parent Experiment**: EXP-FRONTIER-36287182510 (audit PASS, outcome SCRATCHPAD_CORRECT_BUT_COSTLY)
**Parent Handoff Disposition**: SUPERSEDE — inherited next_question is advisory only, not binding

---

## 1. Scientific Question

On **real, credential-free, publicly reachable websites** with a **true holdout** (TRAIN sites for distillation, TEST sites never observed during distillation) and **no site-identity leakage** in any inherited mechanism:

1. **ARCHITECTURAL PRECONDITION**: What fraction of real action-gating objects expose a **STABLE, agent-visible, episode-invariant identifier** — readable in the HTTP response, equal across episodes, and sufficient together with observable state to determine the declared action? What is the matching fraction for **session-scoped identifiers** (CSRF-bound-to-session, rotating capability handles) that cannot support cross-episode replay?

2. **PARAMETERIZED TRANSFER EXECUTION**: Does inherited, parameterized transfer actually execute on held-out TEST sites — resolving to the correct action and verifying against response-derived postconditions — at what span-level action correctness rate, with what abstention rate, and with what honest cost in real tokens, requests, verification, and repair?

3. **AMORTIZATION**: Does the inherited arm cost less than **cold re-exploration** AND less than a **no-memory deterministic executor** that re-derives every episode, on this real substrate with real token/request mapping (not an abstract ledger)?

---

## 2. Hypothesis

**H1 (Identifier Prevalence)**: A non-trivial fraction (>10%) of real action-gating objects expose stable, episode-invariant, agent-visible identifiers sufficient for action determination.

**H2 (Transfer Execution)**: A parameterized mechanism distilled on TRAIN sites achieves span-level action correctness on TEST sites exceeding COLD_REEXPLORATION by >5 percentage points, with abstention rate <50%.

**H3 (Amortization vs Cold)**: The inherited arm's amortized cost per episode (tokens + requests + verification + repair) is strictly less than COLD_REEXPLORATION's.

**H4 (Amortization vs No-Memory)**: The inherited arm's amortized cost per episode is strictly less than NO_MEMORY_DETERMINISTIC's.

**H5 (Null Arm)**: A state-keyed cache that omits the gating object's identity (NULL_STATE_KEYED) produces silently wrong actions at a measurable rate (≥5% false replay rate on TEST sites), converting the synthetic 80/600 finding from EXP-FRONTIER-36287182510 into a real credential-free number.

---

## 3. Falsification Conditions (Any ONE triggers FALSIFIES)

| Condition | Threshold | Interpretation |
|-----------|-----------|----------------|
| **F1** Stable identifier prevalence | ≤ 0.10 | Architectural precondition absent; cross-episode replay fundamentally unsound on real Web |
| **F2** INHERITED_PARAMETERIZED correctness | ≤ COLD_REEXPLORATION + 0.05 | Parameterized transfer does not exceed cold exploration on holdout |
| **F3** INHERITED_PARAMETERIZED abstention | ≥ 0.50 | Mechanism abstains too often; not executable on holdout |
| **F4** INHERITED_PARAMETERIZED cost vs COLD | ≥ COLD_REEXPLORATION | No amortization over cold re-exploration |
| **F5** INHERITED_PARAMETERIZED cost vs NOMEM | ≥ NO_MEMORY_DETERMINISTIC | No amortization over no-memory re-derivation |
| **F6** NULL_STATE_KEYED false replay rate | < 0.05 | Synthetic false-replay finding was substrate-specific; null arm fails to replicate |
| **F7** Parameterized mechanism unavailable | N/A | MEASUREMENT_INCOMPLETE — record identifier prevalence and baselines only |

---

## 4. Site Selection (Frozen Before Execution)

### 4.1 TRAIN Sites (10 sites, distillation only)
Pre-registered list of 10 diverse credential-free public websites, distinct eTLD+1, no authentication, no cookies required, no JavaScript-rendered content:

1. `https://httpbin.org` — HTTP testing service (REST-like endpoints)
2. `https://jsonplaceholder.typicode.com` — Fake REST API
3. `https://api.github.com` — GitHub public API (no auth for public repos)
4. `https://developer.mozilla.org` — MDN Web Docs (static content + API)
5. `https://docs.python.org` — Python Documentation
6. `https://doc.rust-lang.org` — Rust Documentation
7. `https://go.dev` — Go Documentation
8. `https://en.wikipedia.org` — Wikipedia (REST API + HTML)
9. `https://example.com` — IANA reserved example domain
10. `https://postman-echo.com` — Postman echo service

**Holdout Rule**: TRAIN sites are NEVER used for execution evaluation. Distillation runs ONLY on TRAIN sites.

### 4.2 TEST Sites (5 sites, execution only)
Pre-registered list of 5 held-out credential-free public websites, distinct eTLD+1 from TRAIN and from each other:

1. `https://api.publicapis.org` — Public APIs directory
2. `https://dog.ceo` — Dog API (REST-like)
3. `https://catfact.ninja` — Cat Facts API
4. `https://api.chucknorris.io` — Chuck Norris Jokes API
5. `https://zenquotes.io` — Quotes API

**Holdout Rule**: TEST sites are NEVER observed during distillation. Execution runs ONLY on TEST sites.

### 4.3 Site Identity Leakage Prevention
- Mechanism distillation outputs must not contain hostname, domain, IP, or any site-specific fingerprint.
- Cache keys must be purely structural (resource type, action pattern, identifier schema).
- **Audit Check**: No TEST-site hostname appears in any TRAIN-distilled artifact.

---

## 5. Observation Representation (Fixed from EXP-INTEL-36287179392)

- **Representation**: Minimal HTTP+HTML structural extraction (status, headers, link relations, form actions, input names, semantic HTML landmarks).
- **Tokenizer**: `cl100k_base` (n_vocab 100277).
- **Cost**: 763 tokens/observation (baseline from EXP-INTEL-36287179392, n=155, 15 hosts).
- **No**: Full DOM, accessibility tree, JavaScript execution, browser.
- **Accounting**: Every observation incurs its token cost. Token counts summed per episode and amortized. No model API called; token cost is the measurement unit for observation economy.

---

## 6. Arms (Frozen Identities for Downstream Transmission)

### 6.1 INHERITED_PARAMETERIZED (Treatment)
- **Mechanism**: Parameterized mechanisms from C-PARAM-INHERIT product kernel (`src/spider/kernel.py` → `distill_parameterized` / `resolve` path).
- **Distillation**: Run on TRAIN sites only. Observe successful CRUD trajectories. Distill mechanisms with parameter slots for varying resource identifiers. Confidence must meet `min_confidence=0.8` for `EXECUTABLE` resolution.
- **Transfer**: On TEST sites, resolve mechanisms using only structural matching (intent, preconditions, applicability guards) — **no site identity**. Bind parameters using detected stable identifiers from TEST-site responses. Verify postconditions against response.
- **Re-validation**: Before replaying a compiled action, re-fetch the gating object's identifier from the response and verify it matches the bound value. If mismatch → abstain (EXPLORE/UNKNOWN).
- **Availability**: If parameterized mechanism is unavailable at experiment start, arm = UNAVAILABLE. Experiment proceeds with identifier prevalence + baselines + null arm.

### 6.2 NULL_STATE_KEYED (Mandatory Null Control)
- **Mechanism**: Replay/cache key = observable state signature only (world store snapshot + last request method/path). **Omits the gating object's identity**.
- **This is exactly the shape of SPIDER's incumbent state-keyed cache** that produced 80/600 silent false compiled replays in EXP-FRONTIER-36287182510.
- **Behavior**: When observable state is identical but gating-object identity differs across episodes, the cache replays the wrong bound action silently.
- **Measurement**: Per-span false replay rate on TEST sites (action executed ≠ declared correct action, but cache served it).

### 6.3 COLD_REEXPLORATION (Baseline)
- **Mechanism**: Fresh exploration each episode. No memory inheritance. Each episode independently discovers action-gating identifiers by probing the site (following links, submitting forms, reading responses) and executes the task.
- **Cost**: Real token/request cost measured per episode. Zero cross-episode amortization.

### 6.4 NO_MEMORY_DETERMINISTIC (Baseline)
- **Mechanism**: No persistent memory. Each episode re-derives the action sequence from observable state (HTTP responses, HTML structure) using the same minimal structural observation representation (763 tokens) as the treatment arm. No cross-episode cache.
- **Cost**: Lower per-episode cost than COLD_REEXPLORATION (no exploration search), but no cross-episode amortization.

### 6.5 WITHIN_EPISODE_SCRATCHPAD (Reference)
- **Mechanism**: Within-episode value propagation only (from EXP-FRONTIER-36287182510). Propagates identifiers read from response bodies within the current episode; **zero cross-episode retention**.
- **Purpose**: Establishes the correctness upper bound without amortization. Cost identical to NO_MEMORY_DETERMINISTIC per episode.

### 6.6 ORACLE_PERFECT_TRANSFER (Positive Control)
- **Mechanism**: Oracle that knows the correct stable identifier for every action-gating object on TEST sites and binds it perfectly.
- **Purpose**: Instrument calibration — measures theoretical maximum correctness and minimum cost with perfect identifier knowledge.
- **Expected**: Correctness = 1.0000, abstention = 0.0, minimal cost.

---

## 7. Episode Structure

- **Episodes per TEST site**: 10
- **Total episodes**: 50 (5 sites × 10 episodes)
- **Task Family**: Read-write resource CRUD on REST-like endpoints (create, read, update, delete, list) — same intent family as synthetic substrate, but on real sites with real identifier schemas.
- **Novelty**: All TEST sites are novel (never seen in distillation). Within a TEST site, episodes 1-5 may reuse resources; episodes 6-10 use fresh resources to measure cold-start vs amortized behavior.
- **Per-episode spans**: Variable per site (target ~20 spans/episode = ~1000 total spans).

---

## 8. Identifier Detection Protocol (Per Action-Gating Span)

For each span on TEST sites where an action requires a gating identifier (e.g., resource ID, CSRF token, capability handle):

1. **Extract candidates** from HTTP response (body JSON fields, headers, link relations, form inputs, meta tags).
2. **Classify** each candidate:
   - `STABLE`: Readable in response, equal across 5+ episodes for same logical resource, sufficient + observable state → correct action, episode-invariant.
   - `SESSION_SCOPED`: Meets above but varies across episodes (session-bound, CSRF, rotating handle, nonce).
   - `ABSENT`: No identifier readable in response sufficient for action determination.
3. **Record per span**: `identifier_type`, `identifier_value`, `episode_invariance` (boolean across 5 episodes), `action_determination_sufficiency` (boolean: binding yields correct action).
4. **Prevalence**: `stable_identifier_prevalence = count(STABLE) / count(action-gating spans)`.

---

## 9. Cost Ledger (Real Substrate, Real Units)

| Component | Unit | Description |
|-----------|------|-------------|
| `observation_tokens` | tokens | Minimal structural observation (763 tokens/observation baseline). Summed per episode. |
| `requests` | count | HTTP requests issued (exploration, execution, verification, repair). |
| `verification_calls` | count | Postcondition verification checks against response (1 per check). |
| `repair_events` | count | When verification fails: re-fetch, re-bind, re-execute → additional requests + verification. |
| `model_calls` | — | **NOT USED** — no model API. Replaces synthetic "model unit". |

**Amortized Cost per Episode** = `(sum of all components over all episodes) / episodes`.

Compared across arms: INHERITED_PARAMETERIZED vs COLD_REEXPLORATION vs NO_MEMORY_DETERMINISTIC.

---

## 10. Primary Endpoint & Decision Rule

### Primary Endpoint
`span_level_action_correctness` on TEST sites = fraction of spans where executed action matches declared correct action for that span.

### Secondary Endpoints (All Measured)
- `stable_identifier_prevalence`
- `session_scoped_identifier_prevalence`
- `abstention_rate` (UNKNOWN/EXPLORE resolutions)
- `amortized_cost_per_episode` (tokens + requests + verification + repair)
- `false_replay_rate` (NULL_STATE_KEYED only)

### Success Criteria (ALL Required for SUPPORTS)
1. `stable_identifier_prevalence > 0.10`
2. `INHERITED_PARAMETERIZED.span_level_action_correctness > COLD_REEXPLORATION.span_level_action_correctness + 0.05`
3. `INHERITED_PARAMETERIZED.abstention_rate < 0.50`
4. `INHERITED_PARAMETERIZED.amortized_cost_per_episode < COLD_REEXPLORATION.amortized_cost_per_episode`
5. `INHERITED_PARAMETERIZED.amortized_cost_per_episode < NO_MEMORY_DETERMINISTIC.amortized_cost_per_episode`
6. `NULL_STATE_KEYED.false_replay_rate >= 0.05`

### Outcome Mapping
| Outcome | Condition |
|---------|-----------|
| **SUPPORTS** | All 6 criteria met |
| **FALSIFIES_PRECONDITION** | F1 only |
| **FALSIFIES_TRANSFER_CORRECTNESS** | F2 only |
| **FALSIFIES_TRANSFER_ABSTENTION** | F3 only |
| **FALSIFIES_AMORTIZATION_COLD** | F4 only |
| **FALSIFIES_AMORTIZATION_NOMEM** | F5 only |
| **FALSIFIES_NULL_ARM** | F6 only |
| **MEASUREMENT_INCOMPLETE** | F7 (mechanism unavailable) |
| **MIXED** | Multiple criteria failed — report which passed/failed |

---

## 11. Validity Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| **Site identity leakage** | Audit: grep TRAIN artifacts for TEST hostnames. Cache keys structural only. |
| **Identifier detection bias** | Blind classification: classifier sees only response body/headers, not site identity. Inter-rater on 10% sample. |
| **Parameterized mechanism overfitting** | Distillation on TRAIN only; confidence threshold 0.8; applicability guards required. |
| **Cost ledger incompleteness** | All HTTP requests counted. Token cost from fixed tokenizer. No hidden model calls. |
| **Null arm not triggered** | TEST sites selected for known identifier variation (APIs with rotating tokens, session-bound forms). |
| **Substrate failure (blocked/rate-limited)** | Pre-flight check all 15 sites. Retry with backoff. Record NOT_MEASURED per site with exact error. |
| **Representation loss (763 tokens)** | Acknowledge: no JS-rendered content, no auth surfaces, single crawl depth. Scope bounded in handoff. |
| **Single tokenizer absolute counts** | Ratios tokenizer-robust; absolute counts not portable. Record tokenizer explicitly. |

---

## 12. Product Consequences

### Positive (SUPPORTS)
- C-CROSSSITE advances HYPOTHESIS → EXPERIMENTAL with measured real-Web identifier prevalence, transfer correctness, abstention, and amortization.
- Enables Product to build cross-site inheritance with verified economics.
- Null arm result validates that SPIDER's incumbent state-keyed cache is unsound on real Web (architectural liability).
- Product may implement stable-identifier binding + re-validation in kernel.

### Negative (Any FALSIFIES_*)
- **F1 (Precondition)**: Cross-episode replay architecture fundamentally unsound on real Web — no stable handle to bind. SPIDER must pivot to per-episode re-derivation or within-episode propagation only.
- **F2/F3 (Transfer)**: Parameterized mechanisms do not generalize across sites even when identifiers exist.
- **F4/F5 (Amortization)**: Inheritance costs more than re-derivation on real substrate.
- **F6 (Null)**: Synthetic 80/600 false-replay finding was substrate-specific; state-keyed cache may be sounder than thought.
- In all negative cases: C-CROSSSITE remains HYPOTHESIS or moves to REJECTED/BLOCKED with evidence.

---

## 13. Estimated Cost

- HTTP requests: ~2,500
- Observation tokens: ~380,000 (763 × ~500 observations)
- Wall-clock: ~30 minutes
- Compute: stdlib HTTP only, no browser, no model API, no docker

---

## 14. Expected Information Gain

**High**. This is the first SPIDER experiment to measure on the same credential-free HTTP substrate:
- (a) Real Web stable identifier prevalence
- (b) Cross-site parameterized transfer on true holdout
- (c) Honest amortization with real token/request costs
- (d) Null arm's silent error rate on real sites

A decisive result in either direction changes the C-CROSSSITE claim status and SPIDER's architectural commitment to cross-episode replay.

---

## 15. Frozen Artifacts & Identifiers (For Downstream Transmission)

All metric and control identifiers use stable names defined above:
- Metrics: `stable_identifier_prevalence`, `session_scoped_identifier_prevalence`, `span_level_action_correctness`, `abstention_rate`, `amortized_cost_per_episode`, `false_replay_rate`
- Arms: `INHERITED_PARAMETERIZED`, `NULL_STATE_KEYED`, `COLD_REEXPLORATION`, `NO_MEMORY_DETERMINISTIC`, `WITHIN_EPISODE_SCRATCHPAD`, `ORACLE_PERFECT_TRANSFER`
- Controls: `NULL_STATE_KEYED` (mandatory null), `ORACLE_PERFECT_TRANSFER` (positive control)
- Baselines: `COLD_REEXPLORATION`, `NO_MEMORY_DETERMINISTIC`, `WITHIN_EPISODE_SCRATCHPAD`

These exact identifiers must be used in `result.json`, `audit.json`, and `handoff.json`.