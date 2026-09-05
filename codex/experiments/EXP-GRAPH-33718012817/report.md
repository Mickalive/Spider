# EXP-GRAPH-33718012817 — Report

## Experiment Summary

**ID:** EXP-GRAPH-33718012817  
**Lane:** graph  
**Claim:** C-PARAM-INHERIT  
**Status:** COMPLETE  
**Outcome:** SUPPORTS (literal universal matching causes false accepts in shared registry)  
**Decision Rule Verdict:** COMPETITION-UNSAFE

## Scientific Question

When both literal (zero-parameter) and parameterized mechanisms coexist in a shared registry, does the literal mechanism's universal matching cause false accepts — intercepting resolutions that should go to the parameterized mechanism, producing incorrect bound_action URLs?

## Answer

**Yes.** In all 6 shared-equal conditions (id=2..6), the literal mechanism wins by insertion-order tie-break at equal confidence (0.95) and produces bound_action url=/posts/1 instead of /posts/{id}. The false accept rate at equal confidence is 100% (6/6).

For example: when a user requests fetch with params={id: 3}, the kernel returns EXECUTABLE with bound_action url=/posts/1 (the literal mechanism's fixed URL) instead of url=/posts/3 (the parameterized mechanism's templated URL). The user intended to fetch post 3 but will fetch post 1.

## Results by Condition

### Baseline Controls (all pass)

| Condition | Resolution | Winner | URL | Status |
|---|---|---|---|---|
| cold (no mechanisms) | UNKNOWN | — | — | PASS |
| literal-only-original (id=1) | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | PASS |
| literal-only-unseen (id=2) | EXECUTABLE | literal-fetch-posts-1 | /posts/1 | PASS |
| param-only-original (id=1) | EXECUTABLE | param-fetch-posts | /posts/1 | PASS |
| param-only-unseen (id=2) | EXECUTABLE | param-fetch-posts | /posts/2 | PASS |

### Competition Conditions (all show false accepts)

| Condition | Params | Winner | Bound URL | Expected URL | False Accept? |
|---|---|---|---|---|---|
| compete-equal-id1 | {id: 1} | literal-fetch-posts-1 | /posts/1 | /posts/1 | No (coincidental) |
| compete-equal-id2 | {id: 2} | literal-fetch-posts-1 | /posts/1 | /posts/2 | **YES** |
| compete-equal-id3 | {id: 3} | literal-fetch-posts-1 | /posts/1 | /posts/3 | **YES** |
| compete-equal-id4 | {id: 4} | literal-fetch-posts-1 | /posts/1 | /posts/4 | **YES** |
| compete-equal-id5 | {id: 5} | literal-fetch-posts-1 | /posts/1 | /posts/5 | **YES** |
| compete-equal-id6 | {id: 6} | literal-fetch-posts-1 | /posts/1 | /posts/6 | **YES** |

### Disambiguation Controls (pass — confidence sorting works)

| Condition | Confidence | Winner | URL | Status |
|---|---|---|---|---|
| compete-param-higher (param=0.98, lit=0.95) | Higher param wins | param-fetch-posts-higher | /posts/3 | PASS |
| compete-literal-higher (lit=0.98, param=0.95) | Higher literal wins | literal-fetch-posts-1-higher | /posts/1 | PASS |

## Mechanism

The false accept occurs because of three interacting kernel behaviors:

1. **Presence-based slot checking (kernel.py L104-106):** For a literal mechanism with `parameter_slots=[]` and no template slots in `action_template`, `required_slots = set()`. The check `any(slot not in params for slot in set())` is always False, so the literal mechanism always becomes a candidate regardless of params.

2. **Confidence-based sorting (kernel.py L112):** `candidates.sort(key=lambda m: m.confidence, reverse=True)`. With equal confidence (0.95), Python's stable sort preserves insertion order.

3. **Insertion order tie-break:** The registry returns mechanisms sorted by `mechanism_id`. Since `'literal-fetch-posts-1' < 'param-fetch-posts'` lexicographically, the literal mechanism appears first in the sorted candidates list and wins the tie.

## Product Consequence

**COMPETITION-UNSAFE** — literal universal matching is a genuine operational hazard. Any shared registry containing both literal and parameterized mechanisms at equal or near-equal confidence will produce incorrect resolutions for parameterized requests. A code fix is required before C-PARAM-INHERIT can advance.

### Recommended Code Fix Options

1. **Tie-break favoring parameterized mechanisms:** When confidence is equal, prefer mechanisms with non-empty `parameter_slots` over literal mechanisms. This is the smallest targeted fix.
2. **Value-based constraint for literal mechanisms:** Add a check that params don't conflict with the literal mechanism's fixed resource (e.g., if the literal URL is /posts/1, reject params={id: 2} as conflicting).
3. **Fixed_resource field:** Require literal mechanisms to carry a `fixed_resource` field that prevents matching when params suggest a different resource.

## Confidence-Based Safety Valve

The experiment confirms that confidence-based disambiguation works correctly. In practice, if a parameterized mechanism is registered with higher confidence than a literal mechanism, the parameterized mechanism wins. This provides a partial safety valve: agents can ensure parameterized mechanisms have higher confidence to avoid false accepts. However, relying on confidence ordering is fragile — equal confidence is a realistic and common scenario.

## What This Does Not Test

- HTTP execution correctness (validated in parent experiment)
- verify() postcondition checking (known to hardcode status=200)
- Preconditions matching (all mechanisms had empty preconditions)
- Real-web endpoints (jsonplaceholder is a substrate validation)
- LLM-driven mechanism discovery (no model calls)
