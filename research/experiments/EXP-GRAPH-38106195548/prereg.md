# EXP-GRAPH-38106195548 preregistration

Lane: graph. Claim: **C-FRESHNESS** (only). Director mandate cycle_id **38105755182**, action
`PIVOT`, target claim C-FRESHNESS, parent_handoff_disposition `SUPERSEDE`.
Parent: `EXP-GRAPH-37992949248` (handoff sha256
`4dd5f69fc4909b8531e1901a1dc0cef5ad3eb76f18d1c2581ba797124a51c780`).

This is **DESIGN ONLY** - no outcome-bearing measurements will be performed. This preregistration
is written before any confirmatory measurement in this transaction.

## 1. Research question and objective

The director mandate asks: can a value-only-rotation (D1V) population spanning >=2
credential-free, server-rendered, no-JavaScript GET-only anchors be constructed - either by
admitting a materially different anchor population whose transport validators (ETag,
Last-Modified, Cache-Control max-age, Vary, final_url) are provably independent of the
rotating value, or by an instrument redesign that decouples body-derived validators and
token-bearing final_urls from value rotation?

The objective is to resolve this blocking question that prevented non-degenerate Part II
read on the original 4 anchors. The parent established (and time-stability confirmed) that
only CAL-POS-2 yielded D1V under frozen transport signature; CAL-POS-1 has BODY_DERIVED_ETAG,
CAL-POS-3 has TOKEN_BEARING_FINAL_URL, CAL-POS-4 is NO_FIELD.

## 2. Hypotheses

- **H-CONSTRUCT**: Either (a) there exists a materially different anchor population (>=2
  anchors meeting all inclusion criteria: credential-free, server-rendered, no-JavaScript,
  GET-only) whose transport validators are provably independent of the rotating value,
  enabling M-N-D1V-ANCHORS >= 2; or (b) an instrument redesign (decoupling body-derived
  validators from value rotation or decoupling token-bearing final_urls from value rotation)
  yields M-N-D1V-ANCHORS >= 2 on a feasible population while preserving the frozen D1V
  definition and substrate constraints.
- **H-NOT-CONSTRUCT**: No such anchor population exists and no feasible instrument redesign
  satisfies all constraints, so M-N-D1V-ANCHORS >= 2 is not constructible.

## 3. Approach (feasibility assessment)

This is a design/feasibility experiment. Key activities:
1. Systematically identify candidate credential-free, server-rendered, no-JavaScript GET-only
   anchors that plausibly exhibit value rotation (forms with tokens, session-related fields)
   distinct from the original set.
2. For each candidate, assess transport validator independence: determine if ETag/LM/Cache-Control
   max-age/Vary/final_url vary as deterministic function of the rotating value. Document
   blockers (BODY_DERIVED_ETAG, TOKEN_BEARING_FINAL_URL, NO_FIELD, etc.)
3. Evaluate instrument redesign strategies: e.g. decoupling ETag from body-derived content for
   D1V detection (separating structural vs value effects), handling token-bearing final_urls,
   or alternative transport_change criteria that don't invalidate D1V when only value rotates.
   Any redesign must preserve credential-free GET-only substrate and frozen D1V semantics.
4. Test feasibility with small probes - apply same estimator controls (GATE F) from parent to
   any population with >=2 anchors.
5. Document all candidates, blockers, and rationale for constructability decision.

## 4. Decision rule

**DECISION-CONSTRUCTABLE** if we identify >=2 anchors forming a viable D1V population with
M-N-D1V-ANCHORS >= 2 and transport validators provably independent of value rotation,
satisfying all substrate constraints and passing estimator capability controls.

**DECISION-NOT-CONSTRUCTABLE** if systematic search over candidate populations and
documented instrument redesigns fails to produce >=2 anchors satisfying all criteria;
all candidates blocked by transport-value coupling or substrate constraints. In this case,
recommend PARKing the four-anchor Part II route and redirecting C-FRESHNESS to an
alternative objective (e.g. guard false-accept/calibration on broader population with
different instrumentation, or different freshness sub-mechanism).

## 5. Controls and validity

- **PC-ESTIMATOR-CAPABLE**: Apply anchor-clustered estimator positive controls (heterogeneous
  2-anchor fixture yielding LOW>0, UB97<1, LOW<UB97) to any candidate population with >=2 anchors.
- **NC-TRANSPORT-INDEPENDENCE**: For candidates in D1V population, demonstrate transport
  validators do not vary as deterministic function of rotating value.
- **Substrate constraints**: credential-free, server-rendered, no-JavaScript, GET-only
- **Preserve frozen definitions**: D1V definition, transport_signature fields, guard structure unchanged
- **No outcome-bearing guard measurements**: This is DESIGN ONLY per mandate.

## 6. Scope and claim ceiling

All findings are bounded to the feasibility question for C-FRESHNESS. No claim event for other
claims (C-MEAS-VALID, C-DELTA-REPAIR, C-SEMANTIC-RESOLVE, C-PARAM-INHERIT, C-LLM-INHERIT,
C-PRODUCT-ECON, C-CROSSSITE). The experiment will produce a decisive bounded reason either way.

## 7. Relationship to parent

Parent (EXP-GRAPH-37992949248) established degeneracy on original 4 anchors with time-stable
coupling. This experiment evaluates the remedies proposed in parent handoff: different anchor
population or instrument redesign. Per director mandate, parent handoff is continuity evidence
only (SUPERSEDE). The question is whether either remedy is constructible under stated constraints.
