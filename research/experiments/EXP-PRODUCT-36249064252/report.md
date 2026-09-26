# EXP-PRODUCT-36249064252 — Parameter inheritance across disjoint resources

- **Lane:** product
- **Claim under test:** `C-PARAM-INHERIT`
- **Status:** `COMPLETE` — the measurement transaction completed validly
- **Outcome:** `FALSIFIES` (by the frozen decision rule)
- **Frozen inputs:** unmodified; all three hashes in `freeze.json` re-verified at execute time

## 1. What was asked

Can the kernel inherit a *procedure* from one resource and re-apply it to a
resource whose identifiers were never observed, without guessing? And if it can,
does that capability pay for itself?

The frozen falsifier required **all seven** conditions to hold. Five passed and
two failed. Both failures are economic.

## 2. Result in one table

| ID | Condition | Threshold | Observed | Verdict |
|----|-----------|-----------|----------|---------|
| D1 | Success rate, all three families | ≥ 0.80 | 1.0 / 1.0 / 1.0 | **pass** |
| D2 | Abstention precision | ≥ 0.85 | 1.0 | **pass** |
| D3 | False-accept rate | ≤ 0.10 | 0.0 | **pass** |
| D4 | ECE | ≤ 0.15 | 0.0435 | **pass** |
| D5 | Amortized cost ratio vs best baseline | ≤ 0.85 | 1.02 – 1.67 | **fail** |
| D6 | Positive control (same resource) | success ≥ 0.95, binding ≥ 0.95, cost ≤ 0.50 | 1.0, 1.0, **2.0** | **fail** (cost half) |
| D7 | Null control (shuffled intents) | success ≤ 0.10, abstain ≥ 0.90, cost ≥ 1.0 | 0.0, 1.0, 1.0 | **pass** |

## 3. The capability works, and it works cleanly

From 100 successful observations on resource A (two collections, `items` and
`tags`, 20 identifiers each, five collection-neutral intents), `distill_parameterized`
produced exactly five durable mechanisms — one per intent — each with a
confidence of `0.956522` derived from its own evidence: a Beta(2,1) posterior
mean of `0.9565217` multiplied by a leave-one-out re-construction consistency of
`1.0`. That last term matters: the structure is not an artefact of any single
observation, because removing any one of the twenty and re-inducing still
reconstructs it.

The induced slots are the interesting part. `read`, `update` and `delete` expose
`collection` plus `id`; `create` adds the body's `id`; `list` exposes
`collection`, `q` and `limit`. The `collection` slot exists because the evidence
varied it, and the mechanism then bound `products` into it — a value it had never
seen — on all 150 transfer tasks.

On resource B, whose identifiers share no string with resource A:

- **150 / 150** tasks executed a bound mechanism. No `EXPLORE`, no `UNKNOWN`.
- Binding accuracy **1.0**: every bound action carried the correct resource-B
  identifier in the right position.
- **1.0 HTTP request per task**, in every family, with **0** cold fallbacks.
- All 60 negative probes (40 unlearned intents × 2 collections × 2 roles, plus 20
  prefix-collision intents) abstained. Zero false accepts.
- The null control, with intent labels permuted across all observations,
  transferred at **0.0** and abstained at **1.0** — so the transfer above is
  carried by genuine intent structure, not by a permissive matcher.

The committed incumbent, for contrast, has no `distill_parameterized` at all,
hardcodes `confidence=0.5` against `min_confidence=0.8`, resolves every
same-intent query to `EXPLORE`, and issues **0** HTTP requests on the resource-B
probe. This matches the prereg's expectation exactly.

## 4. Why it nevertheless fails the frozen rule

Both failures have the same cause, and it is not the mechanism.

**The cold baseline is already almost free on this substrate.** An agent that
knows nothing still solves a read or a query in **1.0** HTTP requests, because
the first candidate shape it tries is the right one. The treatment also costs
1.0. There is no per-task saving on those two families, so the 100-request
induction bill has nothing to amortize against:

| Family | Treatment amortized | B-COLD | Ratio | Break-even N |
|--------|--------------------|--------|-------|--------------|
| crud-read | 1.667 | 1.000 | 1.67 | never |
| query | 1.667 | 1.000 | 1.67 | never |
| crud-write | 1.667 | 1.640 | 1.02 | 254 tasks |

Writes are the only family with a real saving (cold must guess between three
endpoints), and even there the mechanism needs ~254 transfer tasks to clear the
0.85 bar.

**The same arithmetic sinks the positive control's cost half.** On the
same-resource control, B-COLD *also* costs 1.0 request per task, so a ratio of
≤ 0.50 is unreachable for any system on this substrate, including a perfect one.
The control's substantive halves — mechanism success 1.0, binding accuracy 1.0 —
pass cleanly. Its failure is a statement about the threshold's dynamic range on
this substrate, not about the pipeline.

So the frozen rule returns `FAIL (FALSIFIES)`, and that is reported as written.
The decomposition above is the honest reading of *which* part failed: the
transfer capability is established within this setting; the economic case is not.

## 5. Three product defects found and fixed during execution

These were real defects in `src/spider/kernel.py`, found by running the
experiment rather than by reading it, and each is covered by a unit test:

1. **String-only slot alignment.** A query parameter observed as an integer
   (`limit=2`) could not be aligned, because a slot only round-tripped strings.
   The leave-one-out check then failed on every fold of the `list` intent, the
   confidence collapsed to 0, and the kernel abstained permanently on the entire
   query family — a 0.0 success rate presented as a *scientific* result. Slots
   now carry the observed scalar's type.
2. **Credential leak on the constant path.** A field that happened to be constant
   across the evidence was copied verbatim, so an `Authorization` header — which
   is constant far more often than it is safe — was persisted into the durable
   template. The treatment now stores `${auth_token}`. The literal incumbent
   mechanisms still persist the token; that is recorded as an observation about
   the incumbent.
3. **Volatile context promoted to precondition.** A `session_id` present in
   training state became a hard precondition, so a mechanism could never be
   inherited across sessions. Session metadata is now filtered by the same
   denylist that already protected action fields.

Defect 1 is the cautionary one: without it the experiment would have reported
"parameter inheritance fails to transfer" and been wrong about the reason.

## 6. Validity limits a reader must carry

- **Substrate substitution.** prereg 8 names Flask; this environment has no
  Flask, so the substrate is stdlib `http.server` on an ephemeral loopback port.
  Its API surface, status codes, 401/403, session-scoped bodies, ETag/304 and
  CRUD behaviour were verified by a self-test before any arm ran.
- **Out-of-support generalization.** The collection slot was only ever observed
  holding `items` or `tags`. Binding it to `products` is an extrapolation to a
  third value, not an interpolation between known ones.
- **Low cost dynamic range.** Stated above; it is the reason D5 and D6 fail and
  it bounds how far the economic conclusion travels.
- **Single confidence value.** The treatment emits one confidence (`0.956522`)
  for all 150 executions, so its ECE is a single bin. The pooled all-arm ECE
  (`0.0198`, n=550) is the more informative calibration number.
- **Exact counts, degenerate CIs.** 50 tasks per family means the family-
  stratified bootstrap CI is `[1.0, 1.0]`. No claim is made beyond these task
  constructions.
- **Not an agent evaluation.** No model, browser or network egress was involved.
  This measures the inheritance path in a controlled harness.

## 7. What this does and does not license

**Established in this setting:** given successful evidence that varies the
target collection, the kernel induces a reusable, credential-safe, deterministic
procedure; binds it correctly to unseen identifiers; abstains on unlearned
intents and prefix collisions; and does so in one HTTP request per task.

**Not established:** that inheritance pays for itself. On a substrate where
cold exploration is already one request, it does not, and the frozen thresholds
say so. Also unestablished: inheritance beyond a single collection dimension,
correct abstention on out-of-support bindings in the failure direction,
staleness handling, and repair on binding failure (C-DELTA-REPAIR, out of scope).

**Not claimed:** that `C-PARAM-INHERIT` is globally false. The falsification is
bounded to this substrate's economics, and §4 names the measurement that would
separate an intrinsic economic failure from a substrate artefact.
