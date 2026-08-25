# SPIDER — CAPABILITY CAPSULE CONTRACT

This directive operationalizes the product-facing knowledge object introduced by `SPIDER_ARCHITECTURE_V2.md`.

## Purpose

A Capability Capsule is the smallest SPIDER artifact intended to let a future external agent avoid redoing verified work.

Capsules are model-agnostic and mechanism-agnostic. They may wrap a browser procedure, API call, deterministic transformation, recovery, composite plan, selector strategy, prediction or another validated mechanism.

## Minimum schema

A candidate capsule SHOULD expose the following fields when applicable:

```json
{
  "capsule_id": "namespace/name@version",
  "status": "CANDIDATE|VALIDATED_POC|REPLICATED|GENERALIZED|ROBUST",
  "intent": {
    "description": "human/agent-addressable effect",
    "semantic_keys": []
  },
  "preconditions": [],
  "context_signature": {},
  "mechanism": {
    "kind": "API|PROCEDURE|ROUTE_FRAGMENT|TRANSFORMATION|RECOVERY|COMPOSITE|PREDICTOR|OTHER",
    "entrypoint": null
  },
  "expected_effects": [],
  "verifier": {
    "kind": null,
    "entrypoint": null,
    "cost_class": null
  },
  "fallbacks": [],
  "negative_knowledge": [],
  "freshness": {
    "last_verified_at": null,
    "invalidation_signals": [],
    "ttl_policy": null
  },
  "confidence": {
    "value": null,
    "basis": null
  },
  "cost_estimate": {
    "model_calls": null,
    "tokens": null,
    "browser_actions": null,
    "browser_launches": null,
    "network_calls": null,
    "latency_ms": null
  },
  "provenance": {
    "source_lane": null,
    "source_run_ids": [],
    "evidence_paths": [],
    "source_agent_or_model": null
  },
  "risk": {
    "class": null,
    "permissions_required": []
  },
  "composition": {
    "input_effects": [],
    "output_effects": [],
    "known_incompatibilities": []
  }
}
```

Null is preferable to invented information.

## Candidate versus trusted capsule

A capsule may be created from historical evidence as a `CANDIDATE`, but historical fields that were not measured must remain unknown.

A capsule is eligible for normal Runtime reuse only when:
- applicability can be checked sufficiently for the claimed scope;
- its effect can be verified or otherwise supported at the evidence tier claimed;
- provenance is complete enough to trace the claim;
- known failure/staleness boundaries are represented;
- execution does not silently exceed its risk/permission scope.

## Dominance and duplicates

When several capsules achieve the same effect, do not blindly retain all as equal.

Runtime/Product should estimate a Pareto relation over:
- verified success;
- marginal compute/actions;
- verification cost;
- freshness/staleness;
- risk;
- portability;
- recovery cost.

A dominated capsule may remain provenance but should not be the default choice.

## Delta-learning

When an existing capsule fails because the environment changed, first test whether a small scoped patch can restore its precondition/execution/effect relationship.

Do not relearn the full route if the changed portion can be localized and independently verified.

Store:
- the invalidating observation;
- the smallest changed segment;
- the repair;
- whether the old version remains valid under another context;
- the new version boundary.

## Negative knowledge

Known failures are reusable only when scoped.

Never store `action X fails` without context. Prefer:
- state/context predicate;
- attempted action/mechanism;
- failure witness;
- date/version;
- whether a later repair supersedes it.

## Verification budget

A capsule that saves 100 units of work but requires 120 units to verify is not useful inheritance.

Every serious Runtime/Product comparison must account for retrieval + applicability checking + verification + expected recovery overhead, not only execution cost.

## Compatibility

This directive does not require older Graph/Intel/Product artifacts to be rewritten. Derived capsules may reference them as provenance while explicitly marking missing fields.
