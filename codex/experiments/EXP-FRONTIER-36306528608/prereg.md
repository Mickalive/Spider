# Preregistration: EXP-FRONTIER-36306528608

## 1. Experiment Identity

- **Experiment ID**: EXP-FRONTIER-36306528608
- **Lane**: frontier
- **Claim ID**: C-CROSSSITE (Reusable mechanisms transfer across website holdout)
- **Status**: NEW governed experiment with director_mandate
- **Parent Handoff**: EXP-FRONTIER-36293269574 (disposition: USE, but director_mandate is binding)
- **Director Mandate**: CONTINUE on C-CROSSSITE with cognitive_reset=true, measuring the re-derivable surface precondition

## 2. Scientific Question

**Primary Question**: On real, credential-free, publicly reachable websites selected by a preregistered screen that guarantees the substrate actually contains action-gating structure (at least N=3 objects per site whose correct action is not determined by a single unconditional GET from a root observation, with the screen itself calibrated on at least one site known to contain such structure), what fraction of real action-gating objects is reachable by one unconditional GET from a root observation and therefore free to re-derive at the measured observation cost, versus requiring a discovered multi-step path or a state-dependent or non-GET request and therefore costing cross-episode state to know?

**Strategic Context**: All 48 prior C-CROSSSITE events in the Codex measured whether a mechanism TRANSFERS to a held-out site; none measured whether there is anything to transfer. The previous packet (EXP-FRONTIER-36293269574) attempted this but failed on instrument validity: the selected TEST sites were read-only JSON APIs with 0.000 session-scoped identifiers, no write verbs, and an HTTP-200 primary endpoint that saturated at 1.0000 for all arms. This experiment changes the level of description: it measures the SURFACE OVER WHICH INHERITANCE COULD POSSIBLY AMORTIZE, not whether a particular cache transfers.

## 3. Hypothesis and Falsifier

### Hypothesis (H1)
On credential-free public websites that genuinely gate actions behind session state, CSRF tokens, or multi-step paths, the re-derivable fraction of action-gating objects is **below 0.3**. The majority of action-gating structure requires cross-episode knowledge to navigate correctly. This would make C-CROSSSITE transfer testable for the first time in this substrate class.

### Falsifier (F1)
If the measured re-derivable fraction of action-gating objects **exceeds 0.8** on the qualifying site set, then C-CROSSSITE inheritance is **falsified in the credential-free public HTTP substrate class** because almost all action-gating objects are free to re-derive at observation cost, leaving negligible surface for cross-episode inheritance to amortize. The program would then redirect toward self-hosted credentialed substrates where persistence value is not in question.

### Intermediate Zone
If 0.3 < rederivable_fraction < 0.8: INCONCLUSIVE — surface size ambiguous, requires larger sample or different substrate.

## 4. Site Selection Screen (Preregistered, Calibrated)

### 4.1 Calibration Site (Known Positive)
**Site**: `https://httpbin.org/forms/post`
**Rationale**: This endpoint returns an HTML form with a CSRF-like token (`<input name="csrf_token" ...>`), requires POST to submit, and the response depends on the submitted token. It demonstrably has:
- Action-gating structure: correct action (POST with valid token) not determined by single GET from root
- Session-scoped identifier: the csrf_token rotates or is session-bound
- Write verb: POST
- Multi-step: GET form → extract token → POST
- Reachable with stdlib HTTP, no auth, no JS rendering

**Calibration Procedure** (executed before TEST site selection):
1. Fetch root observation from calibration site
2. Apply screen criteria (Section 4.2) — must PASS all
3. Verify at least 3 action-gating objects detected
4. Record calibration result in provenance.json
5. Only if calibration PASSES, proceed to TEST site screening

### 4.2 Screen Criteria (Applied to Each Candidate Site)
A site QUALIFIES if ALL of the following are true:

| Criterion | Operational Test | Pass Condition |
|-----------|------------------|----------------|
| **C1: Root returns parseable HTML** | GET root URL, parse with regex for `<form>`, `<a>`, `<input>` | At least one form OR link with actionable href found |
| **C2: Action-gating objects >= 3** | Count objects where correct action requires: (a) non-GET verb with token/state, OR (b) >=2 hops from root, OR (c) state-dependent response | Count >= 3 |
| **C3: Non-GET verb with token/state** | Detect forms with method POST/PUT/PATCH/DELETE AND input with name matching csrf|token|nonce|_token | At least 1 such form |
| **C4: Multi-step path** | From root, shortest path to action-gating object >= 2 hops (link → form → submit) | At least 1 object with path_length >= 2 |
| **C5: State-dependent response** | Same URL returns different content/hash on repeated GETs (after interaction) | Content hash differs on repeat GET |
| **C6: Stdlib HTTP reachable** | GET root succeeds with urllib, no browser/JS required | HTTP 200, HTML content-type |
| **C7: No auth required** | No Authorization header, no cookie login, no OAuth flow needed | Publicly accessible |

### 4.3 Candidate Site Pool (Pre-registered)
The following sites will be screened in order. Additional sites may be added ONLY via preregistration amendment before freeze:

1. `https://httpbin.org` (forms, cookies, auth endpoints)
2. `https://httpbin.org/forms/post` (calibration site, also candidate)
3. `https://httpbin.org/cookies/set` (session cookies)
4. `https://httpbin.org/post` (POST echo)
5. `https://postman-echo.com` (POST/GET echo, headers)
6. `https://api.publicapis.org` (if reachable — previously DNS failed)
7. `https://reqres.in` (simulated auth, CRUD)
8. `https://jsonplaceholder.typicode.com` (read-only, likely fails C3/C4)
9. `https://developer.mozilla.org` (may have forms)
10. `https://docs.python.org` (search forms)
11. `https://en.wikipedia.org` (search, login forms)
12. `https://example.com` (minimal, likely fails)
13. `https://github.com` (public forms, may need auth for writes)
14. `https://gitlab.com` (public forms)
15. `https://bitbucket.org` (public forms)

### 4.4 Fallback If Insufficient Qualifying Sites
If fewer than 3 sites pass the screen after exhausting the candidate pool:
- **Outcome**: Record exact list of sites tested, which criteria each failed, and the specific missing ingredient (CSRF token, session cookie, write verb, multi-step path)
- **Interpretation**: Re-derivable surface = 1.0 (or unmeasurably high) in this substrate class because no action-gating structure exists to require cross-episode state
- **Consequence**: C-CROSSSITE falsified in credential-free public HTTP substrate; program redirects to self-hosted credentialed substrates
- **NO SUBSTITUTION**: Read-only JSON APIs (dog.ceo, catfact.ninja, etc.) will NOT be substituted. This is a hard constraint from the director mandate.

## 5. Arms (Fixed Identities for Downstream Transmission)

| Arm ID | Type | Description |
|--------|------|-------------|
| **RE_DERIVABLE** | Treatment | Discards all prior state each episode. Re-reads root observation, extracts action-gating object identifiers, executes correct action. Charged full 763-token structural observation cost (body-sensitive) per span. No cross-episode memory. |
| **CACHE_AND_REVALIDATE** | Treatment | Binds stable agent-visible identifier of gating object on first encounter. On replay: charges 1 verification_call + 1 re-fetch request to re-validate identifier before executing action. If re-validation fails, falls back to re-derivation (charged). |
| **NULL_COST** | Null Control | Mimics CACHE_AND_REVALIDATE structure but uses a randomized/invalid identifier, forcing re-derivation every time while charging identical verification + re-fetch costs. Must have cost >= COLD_REEXPLORATION. Discriminating on ANY substrate. |
| **COLD_REEXPLORATION** | Baseline | Fresh exploration each episode. No memory. Re-derives from root each span. Charged full observation cost. |
| **NO_MEMORY_DETERMINISTIC** | Baseline | Same as COLD but with deterministic policy (fixed tie-breaking). Controls for policy variance. |
| **WITHIN_EPISODE_SCRATCHPAD** | Reference | Within-episode propagation only. Zero cross-episode retention. Can reuse resource IDs discovered within same episode. |
| **ORACLE_PERFECT_TRANSFER** | Positive Control | Knows all stable identifiers from episode 1. Minimum possible cost after episode 1 (verification + re-fetch only). |

**Stable Arm Identities** (must be preserved in result.json, audit.json, verdict.json):
`RE_DERIVABLE`, `CACHE_AND_REVALIDATE`, `NULL_COST`, `COLD_REEXPLORATION`, `NO_MEMORY_DETERMINISTIC`, `WITHIN_EPISODE_SCRATCHPAD`, `ORACLE_PERFECT_TRANSFER`

## 6. Episode Structure

- **Episode**: One complete interaction sequence on a single site, covering all detected action-gating objects
- **Spans per Episode**: One span per action-gating object (detected during screen)
- **Sites**: 3–5 qualifying sites (from screen)
- **Episodes per Site**: 50 (25 for re-derivable fraction estimation, 25 for cost measurement)
- **Total Episodes**: 150–250
- **Arms per Episode**: All 7 arms run sequentially on same site/episode (independent state)

## 7. Action-Gating Object Detection (Per Site, Pre-Episode)

During site screening, each qualifying site yields a fixed list of **action-gating objects** with:
- `object_id`: stable label (e.g., "login_form", "search_submit", "create_post")
- `root_url`: entry point URL
- `required_action`: {method, url_template, required_fields[], state_dependencies[]}
- `gating_type`: "csrf_token" | "session_cookie" | "multi_step" | "state_dependent" | "rotating_handle"
- `ground_truth_verifier`: function(response) -> bool confirming correct execution

This list is frozen after screen and used identically for all arms.

## 8. Observation Representation (Body-Sensitive, 763-Token Target)

**MinimalObservation** includes:
- URL, method, status_code
- Link relations (rel, href)
- Form actions (action, method, inputs[])
- Input names (all)
- Semantic landmarks (main, nav, article, section, form, table, etc.)
- **Response headers** (Content-Type, ETag, Cache-Control, Set-Cookie, etc.)
- **Response body hash** (SHA256)
- **Key body content fields** (extracted JSON keys, form values, token values — truncated to 500 chars)
- **Tokens**: computed on FULL serializable structure above using `cl100k_base` tokenizer

**Explicit Declaration**: No token-to-latency or token-to-dollar mapping is defensible. Cost reported in tokens and request counts only. Product economics answer is UNKNOWN.

## 9. Cost Ledger (Per Episode, Per Arm)

| Cost Component | Unit | Charged When |
|----------------|------|--------------|
| `observation_tokens` | tokens | Every observation extraction (full body-sensitive representation) |
| `requests` | count | Every HTTP request (GET, POST, etc.) |
| `verification_calls` | count | CACHE_AND_REVALIDATE and NULL_COST: before each cached replay |
| `repair_events` | count | When fallback to re-derivation occurs after failed verification |

**Amortized Cost Per Episode** = (observation_tokens + requests + verification_calls + repair_events) / episodes

## 10. Primary Endpoint: action_gating_correctness

**Definition**: For each action-gating span, correctness = 1.0 if the arm's executed action matches the ground-truth required action for that object, verified against response content/structure.

**Ground Truth Verification** (per object, pre-registered):
- For POST with CSRF: response contains success indicator AND subsequent GET shows state change
- For multi-step: all required steps completed in order, final state verified
- For state-dependent: response hash matches expected post-action state
- **Never**: HTTP status code alone (200 ≠ correct action)

**Dynamic Range Verification (Pre-Freeze)**:
- Pilot on calibration site: COLD_REEXPLORATION correctness must be in (0.1, 0.9)
- ORACLE_PERFECT_TRANSFER correctness > COLD_REEXPLORATION + 0.1
- If not satisfied, site is DISQUALIFIED (cannot measure)

## 11. Prevalence Estimator: rederivable_fraction

**Definition**: 
- **Numerator**: Count of action-gating spans where the correct action is fully determined by a single unconditional GET from the root observation (no prior episode state needed, no multi-step discovery, no token/state from prior interaction)
- **Denominator**: Total count of action-gating spans across all episodes and sites
- **Unit**: Both are counts of spans → **same unit**

**Classification Protocol** (deterministic, pre-registered):
For each action-gating object detected during screen:
1. Fetch root observation (single GET)
2. Extract all links, forms, tokens, identifiers from root ONLY
3. Determine if `required_action` can be constructed solely from root observation data
4. If YES → re-derivable; if NO → requires cross-episode state
5. This classification is FIXED per object and used for all episodes

**Per-Site Stratification**: rederivable_fraction computed per site, then averaged (equal weight per site).

## 12. Null Control Design: NULL_COST

**Purpose**: The previous NULL_STATE_KEYED arm failed because it could not make a wrong action on read-only APIs (no session-scoped identifiers to omit). NULL_COST is designed to be discriminating on ANY substrate.

**Mechanism**:
- On first encounter: "learns" a fake identifier (random UUID) for the action-gating object
- On replay: charges 1 verification_call + 1 re-fetch request to "validate" the fake identifier
- Validation always fails (fake identifier not found) → falls back to re-derivation (charged)
- Total cost per replay = verification_call + re-fetch + re-derivation_observation + re-derivation_request
- **Expected**: NULL_COST cost >= COLD_REEXPLORATION cost (cache overhead + forced re-derivation)

**Discriminating Power**: If CACHE_AND_REVALIDATE beats NULL_COST, the benefit comes from VALID identifier binding, not cache structure alone. This null can fire even on read-only APIs.

## 13. Threshold Satisfiability (Pre-Freeze Audit)

Before freeze, the following MUST be demonstrated on pilot data from calibration site:

1. **Primary endpoint dynamic range**: COLD_REEXPLORATION action_gating_correctness ∈ (0.1, 0.9)
2. **Baseline max rule**: For any criterion `TREATMENT > BASELINE + delta`, must have `BASELINE <= 1 - delta` at freeze. Specifically:
   - If success requires `CACHE_AND_REVALIDATE_correctness > COLD_correctness + 0.05`, then `COLD_correctness <= 0.95`
3. **Re-derivable fraction range**: Pilot estimate must show the threshold 0.3 and 0.8 are within [min_possible, max_possible] given observed variance
4. **NULL_COST firing**: NULL_COST cost >= COLD_REEXPLORATION cost (proves null discriminating)
5. **Cost variance**: Token/request variance low enough to detect 10% cost difference at N=150 episodes

If ANY threshold fails satisfiability, the experiment is REDESIGNED before freeze (not run with unsatisfiable criteria).

## 14. Decision Rule (Frozen)

### Primary Decision (rederivable_fraction)
Let `rf` = rederivable_fraction (point estimate), `rf_ci_lower`, `rf_ci_upper` = 95% CI (bootstrap, site-clustered resampling).

| Condition | Outcome | Claim Update |
|-----------|---------|--------------|
| Screen yields < 3 qualifying sites | **FALSIFIES C-CROSSSITE in this substrate** | C-CROSSSITE: REJECTED (in credential-free HTTP); redirect to self-hosted |
| `rf_ci_upper < 0.5` AND `rf <= 0.3` | **SUPPORTS** C-CROSSSITE transfer testable | C-CROSSSITE: EXPERIMENTAL → VALIDATED (precondition met) |
| `rf_ci_lower > 0.6` AND `rf >= 0.8` | **FALSIFIES** C-CROSSSITE in this substrate | C-CROSSSITE: REJECTED (in credential-free HTTP); redirect to self-hosted |
| Otherwise | **INCONCLUSIVE** | C-CROSSSITE: HYPOTHESIS (unchanged); larger sample/different substrate needed |

### Secondary: Cost Economics (amortized_cost_per_episode)
- If `CACHE_AND_REVALIDATE` cost < `NULL_COST` cost (paired bootstrap, p < 0.05, site-clustered): valid identifier binding provides measurable benefit
- If not: cache structure alone insufficient; re-derivation cheaper than invalid cache maintenance

### Tertiary: Abstention Rate
- All arms report `abstention_rate` = spans with `decision_path == ABSTAIN` / total spans
- Arms that never abstain on ambiguous objects are flagged in validity_notes
- High abstention with maintained correctness = desirable (avoids false accepts)

## 15. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Site substitution post-freeze** | All TEST sites frozen in spec.json; no substitution allowed; any change requires new experiment |
| **HTTP-200 endpoint saturation** | Primary endpoint is action_gating_correctness (content-verified), NOT HTTP status; dynamic range verified pre-freeze |
| **Prevalence numerator/denominator mismatch** | Both are span counts; per-site stratification; explicit in spec |
| **NULL control vacuous** | NULL_COST designed to fire on ANY substrate; cost-based not wrongness-based |
| **INHERITED_PARAMETERIZED unavailable** | Not used as treatment; RE_DERIVABLE and CACHE_AND_REVALIDATE are self-contained |
| **Body-omitting observation** | MinimalObservation INCLUDES body hash and key content; tokens computed on full structure |
| **No durable evidence** | Per-span records, per-episode logs, identifier logs, response cache all persisted with non-self-referential hashes |
| **Token-to-dollar mapping** | Explicitly declared UNKNOWN; no economic claims beyond token/request counts |
| **Single-site generalization** | Minimum 3 qualifying sites required; per-site stratification; site-clustered bootstrap |

## 16. Dependencies (From Parent Handoff and Director Mandate)

1. **NO NEW INFRASTRUCTURE**: stdlib HTTP only, no browser, no docker, no model key, no network beyond selected sites
2. **HARD EXECUTION CONDITION**: Site screen must be satisfied before primary comparison; if no qualifying sites, record exact smallest next action (sites/credentials needed)
3. **NO POST-FREEZE SITE SUBSTITUTION**: Frozen site list in spec.json
4. **PRIMARY ENDPOINT INDEPENDENT OF HTTP STATUS**: action_gating_correctness verified against content
5. **BASELINE_MAX RULE**: Every `treatment > baseline + delta` clause has `baseline_max <= 1 - delta` at freeze
6. **SAME-UNIT PREVALENCE**: Numerator and denominator both span counts
7. **ONE COST BASIS**: Body-sensitive observation, explicit UNKNOWN for token-to-latency/dollar
8. **HARD DEPENDENCY (NOT FRONTIER'S TO FIX)**: Executable inherited mechanism in committed kernel required for any inheritance verdict — Product allocated this cycle; if not landed, record surface measurement only, issue NO transfer verdict
9. **C-RESIDUAL-NOVELTY TERMINATED**: Bounded negative must not be read as closing Frontier lane, C-CROSSSITE domain, or inheritance question

## 17. Analysis Plan (Frozen)

### 17.1 Primary Analysis
1. Compute `rederivable_fraction` per site (span counts)
2. Bootstrap 95% CI (10,000 resamples, clustered by site)
3. Apply decision rule (Section 14)

### 17.2 Secondary Analysis
1. Amortized cost per episode per arm
2. Paired comparison: CACHE_AND_REVALIDATE vs NULL_COST (site-clustered bootstrap)
3. Cost decomposition: observation_tokens, requests, verification_calls, repair_events

### 17.3 Validity Checks (Reported in validity_notes)
1. Primary endpoint dynamic range achieved?
2. NULL_COST cost >= COLD_REEXPLORATION cost?
3. Baseline_max rule satisfied for all thresholds?
4. Per-span records persisted with valid hashes?
5. Identifier classification log complete?
6. Calibration site screen PASS recorded?

## 18. Artifacts to Produce

- `result.json` (schema_version=1, all mandatory fields)
- `report.md` (interpretation bounded by measurements)
- `provenance.json` (GitHub run ID, commits, sites, code paths, environment)
- Raw evidence: `spans.jsonl`, `episodes.jsonl`, `identifiers.jsonl`, `responses_cache/` (SHA256-named)
- All with non-self-referential SHA256 hashes in artifacts list

## 19. Carry-Forward from Parent Handoff (Preserved Distinctions)

### Established (Carry Forward)
- Credential-free real-web substrate reachable with stdlib HTTP
- Committed kernel cannot execute inherited mechanism (src/spider/kernel.py defect)
- Previous TEST sites exposed 0.000 session-scoped identifiers (structurally expected for read-only APIs)
- NULL_STATE_KEYED null control had no wrong action available on read-only substrate
- Primary endpoint (HTTP-200) had zero dynamic range
- Frozen success rule was arithmetically unsatisfiable (>1.05 on [0,1] quantity)
- Observation cost 119 tokens (but body-omitting representation; NOT reconcilable with 763-token floor)

### Rejected (Do Not Carry Forward)
- 0.060 stable_identifier_prevalence (numerator/denominator mismatch)
- NULL_STATE_KEYED 0.000 false-replay rate as evidence about synthetic 80/600 finding
- F3/F4/F5 passing (treatment arm was stub)
- F2 transfer correctness (mechanism didn't exist)
- span_level_action_correctness=1.0000 as competence measure
- Any inference to real LLMs, agents, authorization, tokens-as-dollars, product economics

### Unknown (Remain Open)
- Size of re-derivable surface (THIS EXPERIMENT MEASURES IT)
- True stable-identifier prevalence on action-gating sites (per-span denominator)
- Whether sound cross-episode replay cache exists
- Whether state-keyed cache produces silent wrong actions on real credential-free substrate
- Whether executable inherited mechanism would transfer/amortize
- Whether credential-free site with real session/CSRF/write exists (SCREEN TESTS THIS)
- Correct token-to-latency/dollar mapping

### Do Not Assume (Explicitly Forbidden)
- Do NOT read 0.060 as real-Web prevalence
- Do NOT read NULL_STATE_KEYED 0.000 as refuting synthetic 80/600
- Do NOT treat five previous sites as real-Web sample
- Do NOT treat 119 tokens as reconcilable with 763 tokens
- Do NOT treat C-CROSSSITE next_gate as discharged
- Do NOT treat write leg as exercised
- Do NOT use self-referential artifacts
- Do NOT assume durable raw evidence exists from previous packet
- Do NOT update other lanes' claims from this packet
- Do NOT read this as closing Frontier/C-CROSSSITE/inheritance question

## 20. Expected Information Gain

This experiment measures the **upstream precondition** that 48 prior C-CROSSSITE events assumed but never tested. Both outcomes are decision-changing:
- **Small surface (≤0.3)**: Genuine negative for architecture in largest accessible domain → redirect program to self-hosted credentialed substrates
- **Large surface (≥0.8)**: Unblocks C-CROSSSITE for first time → tells Graph, Physics, Product, Intel what a holdout must contain
- Uses only substrate class where SPIDER has actually executed on real websites (stdlib HTTP, no browser, no docker, no model key)
- Terminates the bounded C-RESIDUAL-NOVELTY thread (12 of 15 frontier experiments) per Director portfolio decision

---

**End of Preregistration**

This preregistration is frozen upon `freeze.json` creation. No outcome data may be inspected before freeze. Any modification after seeing outcomes requires a new experiment.