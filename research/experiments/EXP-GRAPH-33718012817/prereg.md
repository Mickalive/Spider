# EXP-GRAPH-33718012817 — Preregistration

## Experiment Identity

- **ID:** EXP-GRAPH-33718012817
- **Lane:** graph
- **Claim:** C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers"
- **Status at design:** EXPERIMENTAL (parameterized pipeline validated on isolated registries; shared-registry competition untested)
- **Parent handoff:** EXP-GRAPH-33528827169 (sha256: ee1b24b92a766eed03606f1ac95623303234ab03baada15c351940e257c3460c)
- **Request hash:** 74f0cd9d82bf303b81e142802f71ec4b7a289d7ee9d78ad28310763a46ca7558

## Scientific Question

When literal and parameterized mechanisms coexist in the same registry with equal confidence, does the literal mechanism's universal matching create false accepts — selecting the literal mechanism and returning an incorrect bound_action URL for unseen resources?

## Background and Motivation

### What prior experiment established (EXP-GRAPH-33528827169)
- Parameterized mechanism pipeline works end-to-end on jsonplaceholder: 5 unseen integer IDs resolved EXECUTABLE with correct URLs, HTTP 200, verify()=True
- Literal mechanism (parameter_slots=[]) returns EXECUTABLE for ANY params due to presence-based slot checking (kernel.py L104-106)
- The literal-unseen failure was identified as a spec-kernel design mismatch: the kernel implements presence-based matching, the spec assumed value-based matching
- **Critical gap identified by auditor (V_ISOLATION_NO_COMPETITION):** Each condition used an isolated registry. No condition tested literal vs parameterized competition in a shared registry.

### What the parent handoff requires
The handoff explicitly recommends: "Add a mechanism-competition test: register both literal and parameterized mechanisms in the same registry, resolve with various params, verify that parameterized mechanisms are not shadowed by literal universal matches."

### Why this matters
In production, a SPIDER registry will contain multiple mechanism types. If a literal mechanism for "fetch post 1" incorrectly matches a query for "fetch post 2" (returning the wrong URL), this is a false accept that could cause incorrect agent behavior. The prior experiment's isolated-registry design missed this failure mode.

### Kernel code path under test

From `src/spider/kernel.py`, the `resolve()` method (lines 93-123):

1. Iterates `self.registry.all()` looking for mechanisms matching `intent`
2. Checks `m.preconditions` against `context` via `_matches()`
3. Checks `m.applicability_guards` against `context` via `_matches()`
4. Computes `required_slots = set(m.parameter_slots) | _template_slots(m.action_template)`
5. Skips mechanism if any `slot not in params`
6. Sorts candidates by confidence (descending)
7. Returns EXECUTABLE with `bound_action=_bind(best.action_template, params)`

**Critical observation:** Step 6 sorts by confidence ONLY. There is no secondary sort by specificity (parameter_slots count). When two mechanisms have equal confidence, the one encountered first in the candidate list wins. The candidate list preserves iteration order from `self.registry.all()`, which returns mechanisms sorted by mechanism_id (from `MechanismRegistry.replace()`). Since "literal-fetch-posts-1" < "param-fetch-posts" alphabetically, the literal mechanism is iterated first and appended to candidates first.

**Prediction:** In a shared registry with equal confidence, the literal mechanism will be selected for any params (since it has zero required_slots and matches vacuously), producing a bound_action URL pointing to the literal's fixed resource (/posts/1) instead of the requested resource.

## Hypothesis

In a shared registry containing both:
- A literal mechanism: `parameter_slots=[]`, `action_template={method: GET, url: .../posts/1}`, `confidence=0.95`
- A parameterized mechanism: `parameter_slots=["id"]`, `action_template={method: GET, url: .../posts/${id}}`, `confidence=0.95`

When `resolve("fetch", context, {"id": <unseen_id>})` is called:

1. Both mechanisms match (literal via vacuous slot check, parameterized via id-present check)
2. Both have equal confidence (0.95)
3. The kernel sorts by confidence descending (tie) and takes the first candidate
4. The literal mechanism is first in iteration order (alphabetical by mechanism_id)
5. **The literal mechanism is selected**, producing `bound_action={method: GET, url: .../posts/1}` — incorrect for the requested unseen resource

Additionally:
- When the parameterized mechanism has strictly higher confidence (0.99 vs 0.95), it will be selected correctly
- When the literal mechanism has strictly higher confidence (0.99 vs 0.95), it will be selected (confirming confidence-based sorting works)
- When only one mechanism type exists, behavior matches prior findings (literal matches any, parameterized matches correctly)

## Falsification Criteria

The hypothesis is **FALSIFIED** if ANY of:

1. In equal-confidence shared-registry conditions, the parameterized mechanism is selected (not the literal) for unseen resource IDs — the kernel has an unknown specificity tiebreaker or iteration order differs from predicted
2. The bound_action URL for equal-confidence conditions correctly targets the requested resource (e.g., /posts/2 for id=2) — the literal mechanism's bound_action is resource-aware despite having no parameter_slots
3. The kernel sorts by something other than confidence first (e.g., parameter_slots count, mechanism_id reverse order)
4. The literal mechanism does NOT match in the shared registry (e.g., some interaction prevents the vacuous slot check from passing)

Any of these would mean the false-accept scenario does not occur as predicted, and the shared registry is safe under the current kernel design.

## Experimental Design

### Test Endpoint
- **URL:** `https://jsonplaceholder.typicode.com`
- **Resources:** `/posts/1` through `/posts/4`
- **Rationale:** Same substrate as prior experiment. Stable, deterministic, no auth. This is a shared-registry competition test, not a new substrate validation.

### Mechanisms Registered

| Mechanism ID | Type | parameter_slots | action_template | confidence |
|---|---|---|---|---|
| `literal-fetch-posts-1` | Literal | [] | {method: GET, url: .../posts/1} | varies (0.95 or 0.99) |
| `param-fetch-posts` | Parameterized | ["id"] | {method: GET, url: .../posts/${id}} | varies (0.95 or 0.99) |

All mechanisms: intent="fetch", preconditions={}, applicability_guards={}, postconditions={status: 200, has_keys: [userId, id, title, body]}

### Conditions Matrix

| # | Condition | Registry | Literal Confidence | Param Confidence | Params | Expected Selected | Expected URL |
|---|---|---|---|---|---|---|---|
| 1 | shared-equal-confidence-id2 | Both | 0.95 | 0.95 | {id: 2} | param-fetch-posts | .../posts/2 |
| 2 | shared-equal-confidence-id3 | Both | 0.95 | 0.95 | {id: 3} | param-fetch-posts | .../posts/3 |
| 3 | shared-equal-confidence-id4 | Both | 0.95 | 0.95 | {id: 4} | param-fetch-posts | .../posts/4 |
| 4 | shared-param-higher-confidence | Both | 0.95 | 0.99 | {id: 2} | param-fetch-posts | .../posts/2 |
| 5 | shared-literal-higher-confidence | Both | 0.99 | 0.95 | {id: 2} | literal-fetch-posts-1 | .../posts/1 |
| 6 | literal-only-unseen | Literal only | 0.95 | — | {id: 4} | literal-fetch-posts-1 | .../posts/1 |
| 7 | param-only-unseen | Param only | — | 0.95 | {id: 3} | param-fetch-posts | .../posts/3 |
| 8 | cold | None | — | — | {id: 2} | none | — |

### Measurements (for each condition)

1. **Selected mechanism_id** — which mechanism did the kernel choose?
2. **Resolution status** — EXECUTABLE or UNKNOWN?
3. **bound_action URL** — does it match the expected URL?
4. **HTTP execution** — for conditions with expected correct URLs, execute HTTP GET and verify status 200 + JSON keys
5. **Resolution reason** — for debugging

### Execution Order

Conditions executed in order 1→8. Each condition uses a fresh kernel instance with a dedicated registry file containing exactly the specified mechanisms. Registry files are created by writing mechanism JSONL sorted by mechanism_id (deterministic iteration order).

## Decision Rule

**SHARED-REGISTRY-UNSAFE** if ANY of conditions 1-3 (equal-confidence shared-registry) has:
- The literal mechanism selected instead of the parameterized, OR
- The bound_action URL targeting the wrong resource (e.g., /posts/1 for id=2)

**SHARED-REGISTRY-SAFE** if ALL of conditions 1-3 select the parameterized mechanism with correct URLs.

**CONFIDENCE-DOMINATES** if condition 4 (param higher) selects parameterized AND condition 5 (literal higher) selects literal.

**BASELINE-CONSISTENT** if condition 6 (literal-only) → EXECUTABLE with /posts/1, condition 7 (param-only) → EXECUTABLE with correct URL, condition 8 (cold) → UNKNOWN.

The overall verdict combines these: the primary question is SHARED-REGISTRY-UNSAFE vs SHARED-REGISTRY-SAFE. CONFIDENCE-DOMINATES and BASELINE-CONSISTENT are supporting checks.

## Controls Summary

| Control | Condition # | Purpose | Type |
|---|---|---|---|
| Cold (no mechanism) | 8 | Kernel abstains when no knowledge exists | Null |
| Literal only (unseen) | 6 | Literal mechanism matches any params (baseline false accept) | Null |
| Param only (unseen) | 7 | Parameterized mechanism works correctly in isolation | Positive |
| Param higher confidence | 4 | Confidence-based sorting works when parameterized has higher confidence | Positive |
| Literal higher confidence | 5 | Confidence-based sorting works when literal has higher confidence | Null |

## Validity Threats

1. **Substrate simplicity:** JSONPlaceholder is deterministic. No drift, no auth, no DOM. **Mitigation:** Accepted for this gate. This tests kernel competition logic, not real-web complexity. The prior experiment's substrate validation is inherited.

2. **Registry ordering assumption:** The experiment assumes MechanismRegistry.replace() writes mechanisms sorted by mechanism_id, establishing iteration order. **Mitigation:** This is verified by reading registry.py lines 31-33: `items = {m.mechanism_id: m for m in self.all()}; self.replace(items[k] for k in sorted(items))`. The sorted() call uses alphabetical mechanism_id ordering.

3. **Confidence values are artificial:** The experiment uses 0.95 and 0.99 as confidence values. In production, confidence values may differ. **Mitigation:** The experiment tests the kernel's sorting logic, not the confidence assignment policy. The key question is whether equal confidence causes problems, not what confidence values are assigned.

4. **No HTTP execution for wrong-URL conditions:** Conditions where the literal mechanism is predicted to win (conditions 1-3, 5-6) will have incorrect URLs. HTTP execution of wrong URLs would succeed (posts/1 exists) but would not test the right resource. **Mitigation:** HTTP execution is performed only for conditions with correct predicted URLs (conditions 4, 7) to verify the bound_action is valid. For wrong-URL conditions, the bound_action URL string comparison is sufficient.

5. **Single literal mechanism:** The experiment tests one literal mechanism competing with one parameterized mechanism. Real registries may have multiple literals. **Mitigation:** Sufficient for the gate question. Multiple literals would only amplify the false-accept problem (more universal matches competing).

6. **Prior experiment's verify() issue (V_VERIFY_HARDCODED_STATUS):** The audit identified that verify_postconditions() hardcodes status=200. This does not affect this experiment because: (a) all HTTP requests to jsonplaceholder return 200; (b) the primary measurement is mechanism selection and URL correctness, not verify(). The verify() issue is inherited and documented.

## Consequences

### If SHARED-REGISTRY-UNSAFE
- The literal mechanism's universal matching creates false accepts in shared registries
- A kernel fix is required before C-PARAM-INHERIT can be declared validated for production
- Candidate fixes: (a) add specificity tiebreaker (sort by parameter_slots count when confidence tied); (b) add fixed_resource constraint to literal mechanisms; (c) exclude literal mechanisms from intent-matching when parameterized alternatives exist
- The fix must be implemented and re-tested as a regression
- C-PARAM-INHERIT remains EXPERIMENTAL until the shared-registry competition is resolved

### If SHARED-REGISTRY-SAFE
- The literal mechanism's universal matching does NOT create false accepts when parameterized mechanisms are present with equal confidence
- The current kernel behavior is safe for shared registries
- C-PARAM-INHERIT can advance: the "succeed on B" half is validated including shared-registry competition
- No kernel fix needed for this specific issue
- Next experiment: test parameterized mechanisms on real-web endpoints (pagination, search, form interaction)

### If CONFIDENCE-DOMINATES fails
- The kernel's confidence-based sorting is not working as predicted
- The sorting logic must be audited before any claim about mechanism selection

## Preregistration Timestamp

This design was created during the DESIGN phase of EXP-GRAPH-33718012817.
No outcome data has been inspected. All measurements are deferred to EXECUTE.
The design addresses the exact gap identified by the auditor (V_ISOLATION_NO_COMPETITION) and the parent handoff's recommended action.
