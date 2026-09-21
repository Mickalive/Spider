# SPIDER Research 2.0 — Portfolio Governance Policy

Status: binding control-plane policy for allocation of NEW experiments.

## 1. Why this exists

Local scientific rationality is not global research rationality.

A lane handoff may identify an excellent next experiment inside its current thread while that thread is no longer the best use of SPIDER's finite research attention. Therefore `handoff.next_question` is a PROPOSAL, never an automatic command for the next experiment.

Every NEW experiment must be authorized by the global Portfolio Director. Frozen or partially completed experiments are resumed to completion under their original allocation; they are not retrospectively redesigned.

## 2. Objective

Allocate scarce research attention to maximize:

`important uncertainty reduced * claim centrality * product/scientific leverage / cost / measurement risk`

Do NOT reward PASS. A clean falsification, closure of an important dead end, discovery of a measurement invalidity, or a decision to park a branch can create more value than a positive result.

The Portfolio Director asks:

> If SPIDER were discovered today with all currently accepted evidence, what should receive the next unit of research attention?

This reset question is mandatory when a lane shows tunnel behavior.

## 3. Epistemic capital

Each portfolio cycle has 100 notional budget units.

Budget represents opportunity cost: model calls, runner time, browser/network work, researcher attention and — most importantly — research bandwidth displaced elsewhere.

Minimum active allocation cost is 5 units.

Repeated direct continuation of the same claim becomes progressively more expensive after the third consecutive same-claim experiment:

`min_continue_budget = min(35, 5 + 2 * max(0, claim_streak - 3))`

The depth premium is not a punishment. It encodes diminishing marginal value and forces a deep branch to justify why it still dominates untouched alternatives.

Total allocated budget may not exceed 100 units.

## 4. Allocation actions

For each lane, choose exactly one:

- `CONTINUE` — keep the current claim/thread because its marginal value still dominates alternatives.
- `PIVOT` — switch the lane to a different live claim or materially different problem family.
- `PARK` — preserve the thread and evidence, but allocate no new experiment now.
- `REOPEN` — return to a previously parked claim/thread because new evidence or dependencies make it high-value again.
- `TERMINATE` — close a bounded mechanism/thread that no longer merits further work. This never means a broader scientific domain is globally false unless evidence warrants that.

PARK and TERMINATE consume zero budget and dispatch no new experiment.

## 5. Anti-tunnel rules

A lane is in a tunnel when either:
- its same-claim streak is at least 5; or
- at least 8 of its last 10 canonical experiments target the same claim.

When a lane is in a tunnel:
- the Portfolio Director MUST perform a cognitive reset against the lane mission and whole claim portfolio;
- `CONTINUE` requires an explicit exceptional justification and must pay the depth premium;
- a local handoff cannot by itself justify continuation;
- the opportunity cost versus neglected claims must be stated.

At least one active allocation per cycle must target a starved claim when a starved eligible claim exists. A starved claim is one with no experiment in the recent global window and which is not globally closed.

Aim for portfolio diversity. Unless the active scientific state genuinely forbids it, active allocations should span at least 3 distinct claims.

## 6. Lane-specific discipline

### Graph
Graph owns cumulative inheritance. Freshness is one capability, not its identity. It must regularly return to parameter inheritance, delta repair, residual novelty, LLM inheritance and semantic resolution.

### Physics
Physics may pursue a technically deep estimator chain when it is unlocking a genuine measurement barrier, but after a validated measurement milestone it should move to real Web evidence or a materially orthogonal dynamics program rather than indefinitely tune the same estimator.

### Runtime
Runtime is a service substrate for high-value claims. It should prioritize concrete blockers from other lanes. It must not become a permanent specialist laboratory for a single protocol detail unless that detail is the current bottleneck for a central claim.

### Product
Product integrates audited capabilities and measures end-to-end external-agent economics. It should not duplicate Graph/Runtime fundamental work when another lane can own it. Its privileged questions concern successful-task cost, inheritance benefit, verification/repair burden and product behavior.

### Intel
Intel exists to find/reproduce/stress-test external datasets, competitor baselines and prior art that can change a live SPIDER decision. It must not become a self-contained measurement-research lane. An Intel allocation must name the strategic claim/product decision that the external evidence can alter.

### Frontier
Frontier exists to leave the current solution basin. Repeating variants of the same estimator/mechanism family is exceptional. After repeated negatives it should change level of description or mechanism family, not merely hyperparameters.

## 7. Cognitive reset

A cognitive reset means:
1. ignore the inherited `next_question` initially;
2. read the lane mission, all live claims, recent portfolio allocation and neglected claims;
3. propose what the lane would do if it were starting from accepted evidence today;
4. only then compare that proposal against the inherited handoff.

The handoff may win. It no longer wins by default.

## 8. Durable allocation contract

Every NEW experiment request stores the exact portfolio allocation that authorized it, including:
- portfolio cycle id;
- action;
- target claim;
- research question;
- mechanism family;
- budget units;
- decision impact;
- rationale;
- opportunity cost;
- parent-handoff disposition;
- cognitive-reset flag;
- exceptional-continuation justification when required.

DESIGN may narrow implementation details but MUST NOT silently switch the allocated claim, question or action. If the allocation is infeasible, fail loudly and return to portfolio allocation rather than inventing a nearby experiment.

## 9. Liveness and failure

The Portfolio Director is a global allocator, not a single point of scientific failure. If the model allocator is unavailable or emits an invalid allocation, a deterministic fallback allocator selects neglected eligible claims and parks expensive tunnel continuations.

Operational failure never becomes scientific evidence.

## 10. Success criterion

The factory is healthy when it can both:
- go deep enough to resolve hard uncertainties; and
- voluntarily stop going deeper when another question has higher expected value.

The ability to decide that a solvable question is not currently worth solving is a first-class capability.
