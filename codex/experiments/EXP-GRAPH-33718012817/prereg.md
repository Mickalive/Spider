# EXP-GRAPH-33718012817 — Preregistration

## Experiment Identity

- **ID:** EXP-GRAPH-33718012817
- **Lane:** graph
- **Claim:** C-PARAM-INHERIT — "Mechanisms parameterize to unseen identifiers"
- **Status at design:** EXPERIMENTAL (parent verdict: PARAM-INHERIT-SUBSTRATE-BROKEN)
- **Request hash:** 74f0cd9d82bf303b81e142802f71ec4b7a289d7ee9d78ad28310763a46ca7558
- **Parent experiment:** EXP-GRAPH-33528827169 (handoff sha256: ee1b24b92a766eed03606f1ac95623303234ab03baada15c351940e257c3460c)

## Scientific Question

When both literal (zero-parameter) and parameterized mechanisms coexist in a shared registry, does the literal mechanism's universal matching cause false accepts — intercepting resolutions that should go to the parameterized mechanism, producing incorrect bound_action URLs?

## Background and Motivation

### What the parent experiment established (from EXP-GRAPH-33528827169)

The parent experiment validated the parameterized mechanism pipeline end-to-end on jsonplaceholder:
- 5 unseen resource IDs (2-6) resolved EXECUTABLE with correct bound_action URLs
- HTTP 200, valid JSON, verify()=True for all parameterized resolutions
- `_bind()` correctly substituted `${id}` in action_template URLs
- Parameter completeness enforcement works (missing-params → UNKNOWN)
- Applicability guards work independently of parameter binding
- Cold registry correctly returns UNKNOWN

The one failure: the literal mechanism (parameter_slots=[], fixed URL /posts/1) returned EXECUTABLE for unseen resource ID 2. This occurred because the kernel's `resolve()` method (kernel.py L104-106) checks `required_slots = set(m.parameter_slots) | _template_slots(m.action_template)` — for a literal mechanism with no parameter_slots and no template slots, `required_slots` is empty, so `any(slot not in params for slot in set())` is always False regardless of params. The literal mechanism is therefore a universal match for its intent and preconditions.

### What remains unknown

The parent handoff identified three critical unknowns:
1. Whether literal universal matching is intended kernel behavior or a bug requiring code fix
2. Whether literal universal matching creates false accepts when literal and parameterized mechanisms coexist in the same registry
3. Whether verify() works correctly for non-200 HTTP responses

This experiment addresses unknown #2 directly. Unknown #1 is resolved by the outcome: if competition causes false accepts, a code fix is needed; if it doesn't, the spec can be amended. Unknown #3 is deferred.

### Why this matters

If literal mechanisms shadow parameterized mechanisms in a shared registry, the kernel cannot safely support mixed mechanism types. Any external agent registering both literal (site-specific) and parameterized (reusable) mechanisms would get incorrect resolutions. This blocks C-PARAM-INHERIT advancement and product registration of mixed mechanism types.

If literal mechanisms do NOT shadow parameterized mechanisms (e.g., due to confidence-based tie-breaking or some other mechanism), the literal universal matching is benign and the spec can be amended to accept it.

## Hypothesis

In a shared registry containing both:
- A literal mechanism: parameter_slots=[], action_template fixed to /posts/1, confidence=0.95
- A parameterized mechanism: parameter_slots=['id'], action_template with ${id} slot, confidence=0.95

the literal mechanism will resolve EXECUTABLE for all parameter values (id=1..6) because its required_slots set is empty. The parameterized mechanism will also resolve EXECUTABLE for all id values. Since both have equal confidence, registry insertion order determines the winner. The literal mechanism, registered first, will shadow the parameterized mechanism, producing bound_action with the literal URL (/posts/1) instead of the parameterized URL (/posts/{id}).

This creates false accepts: the kernel returns a valid-looking EXECUTABLE resolution with an incorrect bound_action that fetches the wrong resource.

## Kernel Code Path Under Test

From `src/spider/kernel.py`, the `resolve()` method:

```python
required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
if any(slot not in params for slot in required_slots):
    continue
candidates.append(m)
```

For the literal mechanism:
- `m.parameter_slots = []`
- `_template_slots(action_template) = set()` (no `${}` templates)
- `required_slots = set()`
- `any(slot not in params for slot in set())` → False (empty iteration)
- Literal mechanism always passes the slot check → always becomes a candidate

For the parameterized mechanism:
- `m.parameter_slots = ['id']`
- `_template_slots(action_template) = {'id'}`
- `required_slots = {'id'}`
- `any(slot not in params for slot in {'id'})` → False only if 'id' is in params
- Parameterized mechanism passes only when 'id' is provided

When both are candidates with equal confidence (0.95):
```python
candidates.sort(key=lambda m: m.confidence, reverse=True)
best = candidates[0]  # First in list wins tie
```

Since `self.registry.all()` returns mechanisms in insertion order and the literal mechanism is registered first, it wins the tie.

## Falsification Criteria

The hypothesis is **FALSIFIED** if ANY of:

1. In shared-equal conditions (id=2..6), the parameterized mechanism wins (resolves to EXECUTABLE with parameterized bound_action URL /posts/{id}) — indicates the kernel prefers parameterized over literal despite equal confidence
2. In shared-equal conditions, the literal mechanism does NOT resolve EXECUTABLE — indicates the presence-based universal matching is not actually universal in a shared registry
3. The literal mechanism's bound_action URL correctly reflects the parameter value (e.g., /posts/2 for id=2) — indicates the literal mechanism is somehow using params despite having no parameter_slots

## Experimental Design

### Test Endpoint
- **URL:** `https://jsonplaceholder.typicode.com`
- This endpoint is used ONLY for mechanism registration context (base_url in preconditions). No HTTP execution is performed in this experiment — only kernel resolution and bound_action correctness are measured.
- Substrate continuity with the parent experiment (EXP-GRAPH-33528827169).

### Mechanisms Registered

| Mechanism ID | Type | parameter_slots | action_template | confidence | Applicability Guards |
|---|---|---|---|---|---|
| `literal-fetch-posts-1` | Literal | [] | {method: GET, url: https://jsonplaceholder.typicode.com/posts/1} | 0.95 | {} |
| `param-fetch-posts` | Parameterized | ["id"] | {method: GET, url: https://jsonplaceholder.typicode.com/posts/${id}} | 0.95 | {} |
| `param-fetch-posts-higher` | Parameterized | ["id"] | {method: GET, url: https://jsonplaceholder.typicode.com/posts/${id}} | 0.98 | {} |
| `literal-fetch-posts-1-higher` | Literal | [] | {method: GET, url: https://jsonplaceholder.typicode.com/posts/1} | 0.98 | {} |

All mechanisms: intent="fetch", postconditions={status: 200, has_keys: [userId, id, title, body]}

### Registry Configurations

| Config ID | Mechanisms | Insertion Order | Purpose |
|---|---|---|---|
| `empty` | none | — | Cold baseline |
| `literal-only` | literal-fetch-posts-1 | [literal] | Literal standalone behavior |
| `param-only` | param-fetch-posts | [param] | Parameterized standalone behavior |
| `shared-equal` | literal-fetch-posts-1, param-fetch-posts | [literal, param] | Competition at equal confidence |
| `shared-param-higher` | literal-fetch-posts-1 (0.95), param-fetch-posts-higher (0.98) | [literal, param-higher] | Disambiguation: parameterized wins |
| `shared-literal-higher` | literal-fetch-posts-1-higher (0.98), param-fetch-posts (0.95) | [literal-higher, param] | Disambiguation: literal wins |

### Conditions Matrix

| # | Condition ID | Registry | Params | Expected Resolution | Expected Winner | Expected URL | Expected Bound Action |
|---|---|---|---|---|---|---|---|
| 1 | cold | empty | {id: 2} | UNKNOWN | — | — | null |
| 2 | literal-only-original | literal-only | {id: 1} | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | {method: GET, url: .../posts/1} |
| 3 | literal-only-unseen | literal-only | {id: 2} | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | {method: GET, url: .../posts/1} |
| 4 | param-only-original | param-only | {id: 1} | EXECUTABLE | param-fetch-posts | /posts/1 | {method: GET, url: .../posts/1} |
| 5 | param-only-unseen | param-only | {id: 2} | EXECUTABLE | param-fetch-posts | /posts/2 | {method: GET, url: .../posts/2} |
| 6 | compete-equal-id1 | shared-equal | {id: 1} | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | {method: GET, url: .../posts/1} |
| 7 | compete-equal-id2 | shared-equal | {id: 2} | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | {method: GET, url: .../posts/1} |
| 8 | compete-equal-id3 | shared-equal | {id: 3} | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | {method: GET, url: .../posts/1} |
| 9 | compete-equal-id4 | shared-equal | {id: 4} | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | {method: GET, url: .../posts/1} |
| 10 | compete-equal-id5 | shared-equal | {id: 5} | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | {method: GET, url: .../posts/1} |
| 11 | compete-equal-id6 | shared-equal | {id: 6} | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | {method: GET, url: .../posts/1} |
| 12 | compete-param-higher | shared-param-higher | {id: 3} | EXECUTABLE | param-fetch-posts-higher | /posts/3 | {method: GET, url: .../posts/3} |
| 13 | compete-literal-higher | shared-literal-higher | {id: 3} | EXECUTABLE | literal-fetch-posts-1-higher | /posts/1 | {method: GET, url: .../posts/1} |

### Measurements (for each condition)

1. **Resolution status** (EXECUTABLE or UNKNOWN)
2. **Winning mechanism ID** (which mechanism was selected)
3. **Resolution reason** (for debugging)
4. **bound_action correctness** (exact URL match against expected_url)
5. **bound_action structure** (full dict for verification)
6. **Confidence of winning mechanism**

### Execution Order

Conditions executed in order 1→13. Each condition is independent (fresh kernel instance with explicitly controlled registry state). No cross-condition contamination.

## Decision Rules

### COMPETITION-SAFE

If ALL of:
1. cold → UNKNOWN ✓
2. literal-only-original → EXECUTABLE url=/posts/1 ✓
3. literal-only-unseen → EXECUTABLE url=/posts/1 ✓
4. param-only-original → EXECUTABLE url=/posts/1 ✓
5. param-only-unseen → EXECUTABLE url=/posts/2 ✓
6. compete-param-higher → EXECUTABLE url=/posts/3 with param mechanism winning ✓
7. compete-literal-higher → EXECUTABLE url=/posts/1 with literal mechanism winning ✓
8. In shared-equal conditions (id=2..6): EITHER the parameterized mechanism wins (unexpected tie-break favoring parameterized) OR the literal mechanism does NOT win (presence-based universal matching breaks in shared registry)

### COMPETITION-UNSAFE

If ANY of:
1. In shared-equal conditions (id=2..6): the literal mechanism wins AND produces bound_action url=/posts/1 instead of /posts/{id} — literal universal matching causes false accepts in shared registry at equal confidence

This is the EXPECTED outcome based on kernel code analysis.

## Controls Summary

| Control | Condition # | Purpose | Type |
|---|---|---|---|
| Cold (no mechanism) | 1 | Kernel abstains when no knowledge exists | Null |
| Literal on original | 2 | Literal mechanism standalone works | Positive |
| Literal on unseen | 3 | Literal mechanism is universal (expected) | Baseline |
| Param on original | 4 | Parameterized mechanism standalone works | Positive |
| Param on unseen | 5 | Parameterized mechanism generalizes (established) | Positive |
| Competition equal (×6) | 6-11 | Literal vs parameterized at equal confidence | Experimental |
| Param higher confidence | 12 | Confidence-based disambiguation works | Positive |
| Literal higher confidence | 13 | Confidence-based disambiguation works (reverse) | Null |

## Validity Threats

1. **Registry insertion order dependency:** The hypothesis assumes literal is registered before parameterized in shared-equal conditions. If the kernel sorts by mechanism_id or some other criterion before confidence, the tie-break may differ. **Mitigation:** The code shows candidates are sorted by confidence only (kernel.py L112), and insertion order determines the tie. The experiment explicitly controls insertion order.

2. **Equal confidence is realistic:** Both mechanisms at 0.95 confidence mirrors the parent experiment's setup. Real-world confidence values may differ, creating natural disambiguation. **Mitigation:** The confidence-disambiguation conditions (12, 13) test whether different confidence levels provide a practical safety valve.

3. **No HTTP execution:** This experiment measures resolution correctness, not end-to-end HTTP behavior. A mechanism could resolve correctly but execute incorrectly. **Mitigation:** HTTP correctness was validated in the parent experiment (EXP-GRAPH-33528827169) for parameterized mechanisms. The literal mechanism's HTTP behavior is known (always fetches /posts/1).

4. **Single intent ("fetch"):** Competition is tested only for the "fetch" intent. Other intents may have different competition dynamics. **Mitigation:** The kernel's resolution logic is intent-agnostic (kernel.py L97). Competition behavior is determined by the slot-checking and confidence-sorting logic, which applies uniformly across intents.

5. **Literal mechanism has no preconditions:** The literal mechanism has empty preconditions ({}), meaning it matches any context. A literal mechanism with specific preconditions might not compete with a parameterized mechanism in all contexts. **Mitigation:** Empty preconditions represent the most aggressive literal mechanism — the worst case for competition. If this worst case doesn't cause false accepts, specific preconditions won't either.

## Consequences

### If COMPETITION-UNSAFE (expected)

- Literal universal matching is a genuine operational hazard
- Any shared registry with literal + parameterized mechanisms produces incorrect resolutions
- **Code fix options:**
  - Option A: Add a tie-break in `resolve()` preferring parameterized mechanisms over literal when confidence is equal (e.g., prefer mechanism with non-empty parameter_slots)
  - Option B: Add value-based constraints for literal mechanisms (e.g., check that params don't conflict with the mechanism's fixed resource)
  - Option C: Require literal mechanisms to carry a `fixed_resource` field that prevents matching when params suggest a different resource
- C-PARAM-INHERIT remains BLOCKED until the competition hazard is resolved
- Product cannot safely register mixed mechanism types

### If COMPETITION-SAFE (unexpected)

- Literal universal matching is benign in practice
- The kernel naturally prefers parameterized mechanisms or breaks ties differently than expected
- **Spec fix:** Amend the frozen decision rule from the parent experiment to exclude B_LITERAL_UNSEEN as a failure condition — literal universal matching is acceptable behavior
- C-PARAM-INHERIT advances: the parameterized pipeline is validated, and literal over-matching is harmless
- Product can register mixed mechanism types safely

## Preregistration Timestamp

This design was created during the DESIGN phase of EXP-GRAPH-33718012817.
No outcome data has been inspected. All measurements are deferred to EXECUTE.
