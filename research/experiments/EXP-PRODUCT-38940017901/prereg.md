# EXP-PRODUCT-38940017901 preregistration

**Lane:** product
**Claim:** `C-RESIDUAL-NOVELTY` (Codex effective status: EXPERIMENTAL via EXP-PRODUCT-37989728440; registry HYPOTHESIS is stale)
**Design contract:** v2
**Origin run:** 38940017901 · base_sha `677bd0d2d29128493c03c652bd08d0959a70bc72` · HEAD at DESIGN `81fd5ef5`
**Parent handoff:** `research/experiments/EXP-PRODUCT-38234098353/handoff.json` sha256 `afd535847e31c0939734c09e898bf2b0fff40a85910be3c930ab5bfeef9a3e40` (continuity evidence only; binding direction is this request's `director_mandate`, action CONTINUE, parent disposition SUPERSEDE)
**Predecessor pre-freeze:** `research/experiments/EXP-PRODUCT-38315290076/` (same strategic question, prior cycle 38314939812; DESIGN_FAILURE, fingerprint `f44d199ab3d7a1cc1ee6462e`; product state consecutive_failures=3)

## 0. STATUS: DESIGN NOT FROZEN — NON-IDENTIFIABLE / DESIGN FAILURE

This preregistration specifies the experiment the mandate requests, then records the
pre-freeze satisfiability attack required by the DESIGN rules and by
`research/EXPERIMENT_PACKET.md` §2. That attack — independently re-executed for THIS
request against frozen accepted evidence and the current shipped tree at HEAD
`81fd5ef5`, not copied from any prior design — finds the mandate **cannot be frozen
as written** on the named instrument, for the same structural reasons as the
predecessor, re-verified fresh:

1. **Treatment/comparator identity.** The mandated treatment `T-MULTIRES`
   (parameterized inheritance *with decomposable/multi-resolution structure*) and the
   mandated strongest baseline `B-PROCEDURAL` (*compiled procedural lookup*) are
   counter- and success-identical on `SBA-CREDENTIAL-FREE-V3` under the only reading
   that makes the baseline strong (frozen measured: success 1.0 both; per-instance
   totals F1 50, F2 62; see spec.json `derived_decision_table`).
2. **Arithmetically impossible prediction.** The mandate predicts the treatment's
   advantage *grows with controlled residual novelty rather than full task length*. On
   this bank the success margin is exactly `1/K` (a function of task length only),
   constant across the scored novelty ladder (`M-NOVELTY-GROWTH = 0.0` exactly), and the
   frozen cost margin **grows** with `K` (8 → 10, `M-LENGTH-GROWTH = +2`) — the opposite
   of the prediction in both dimensions.
3. **Degenerate monotonicity statistic.** Only `n = 2` scored novelty points (0.5, 0.75)
   carry signal with tied advantage values, so any rank-monotonicity test is degenerate
   (permutation `p = 1.0`); a `rho > 0.5, p < 0.05`-style growth bar is unreachable.
4. **Ceiling grid points.** At novelty 0.0 and 0.25 the mechanism is inactive and every
   arm scores 1.0, so half the residual-novelty grid has zero discriminating signal.
5. **Carrier incapability (two-horn liveness failure).** The named shipped carrier
   (`src/spider/kernel.py`, re-hashed 2026-10-16 at HEAD `81fd5ef5`: sha256
   `3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3`,
   working tree clean for `src/`) induces single-level string-template slots with regex
   supports and performs no arithmetic function learning, so it cannot solve the bank's
   `M(x) = (a*x+b) mod P` chain task on an unseen input; the abstract multi-resolution
   treatment has no distinct executable instantiation either (the bank exposes no
   decomposable structure, and representation-internal compute is uninstrumented).
6. **Duplicate contrast.** The only live contrast (mechanism-containing inheritance vs
   memorization) is already certified `ROBUST` with audit `PASS` by
   `EXP-RUNTIME-38194351940`, whose frozen `result.json` already contains the full
   success matrix, per-instance counters, counter-distinctness and the novelty grid.
   Re-running it would be a forbidden duplicate, not a derisk.

Per `research/EXPERIMENT_PACKET.md` §2, "A treatment structurally incapable of becoming
EXECUTABLE is a DESIGN failure, not a scientific result." No outcome-bearing run is
authorized. `freeze_eligibility` records `decision_rule_reachability = FAIL`,
`baseline_identifiability = FAIL`, `treatment_liveness = FAIL`,
`measurement_prerequisites = PASS`, `control_sensitivity = PASS` (bounded),
`freeze_artifacts_bound = NOT_APPLICABLE`; the design is not freeze-eligible. Advisory
minimal re-scopes (R1/R2/R3) are proposed in §7 for the Director; none is substituted
for the mandate here.

Relation to sibling DESIGN failures (`EXP-PRODUCT-38244439628`, `EXP-PRODUCT-38291106470`,
same strategic question, both `DESIGN_FAILURE_NON_IDENTIFIABLE_NOT_FROZEN`) and to the
direct predecessor `EXP-PRODUCT-38315290076` (same question, `DESIGN_FAILURE`
fingerprint `f44d199ab3d7a1cc1ee6462e`): this packet is NOT an identical repeat. It
re-executes every satisfiability probe at this request's base/HEAD (carrier re-hashed,
capability grep re-run, frozen runtime packet re-read, decision table recomputed,
targeted primary-source reads), re-binds the current shipped carrier identity, and
additionally tests the NEW comparative_reasoning assertion of cycle 38939560846 — that
"the shipped byte-identical parameterized carrier plus empty-registry ablation supply
the treatment/comparator distinction" — finding it does not survive contact with the
frozen instrument (§6, probes P1–P4). The degenerate structure is a Research-2.0
instrument property of V3, not a pre-2.0 inheritance; repeating the *finding* with fresh
verification is the fail-loud duty, while repeating the *EXECUTE* would be the forbidden
duplicate.

---

## 1. Binding mandate (verbatim question)

> Resume the pre-freeze experiment: on the certified non-ceiling credential-free bank
> (SBA-CREDENTIAL-FREE-V3) with the shipped byte-identical parameterized carrier, does the
> founding multi-scale representation/work-compression hypothesis hold — i.e. does
> parameterized inheritance with decomposable/multi-resolution structure achieve strictly
> lower counter-cost (http_requests + retrieval_calls + verification_calls +
> repair_attempts) per VERIFIED SAFE success than strong internal baselines (flat
> exact-state cache, nearest-neighbour/retrieval, compiled procedural lookup, and the
> empty-registry inheritance ablation), with the advantage scaling with residual novelty
> rather than full task length?

Binding constraints: `action=CONTINUE`, `claim_id=C-RESIDUAL-NOVELTY`,
`cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`, **no agent arm / no LLM**,
**frozen V3 bank only** (B2 discharged via C-MEAS-VALID ROBUST; B1/B3 still gate the
flagship), stop trigger (treatment/comparator distinction collapses → abort). The
inherited B11 `C-PARAM-INHERIT` next-question is SUPERSEDED in sequence (parked as
narrower guard work after, not instead of, this derisk — not rejected) and is *not* the
direction. This DESIGN refines nothing away: it specifies the mandate exactly, then proves
it unfreezable. No nearby objective is substituted.

## 2. Hypothesis and falsifier

**H1 (mandated):** parameterized inheritance with decomposable/multi-resolution
structure achieves strictly lower counter-only cost per VERIFIED SAFE success than all
four mandated baselines at matched correctness, with the advantage scaling with
controlled residual novelty rather than full task length — with no LLM agent required.

**Falsifier (frozen for any future freezable instance):** at some scored cell T is not
strictly lower than B-PROCEDURAL, OR `M-NOVELTY-GROWTH <= 0`, OR `M-LENGTH-GROWTH > 0`
(see spec.json `decision_rule`). On the current instrument all three clauses are
entailed a priori (spec.json `derived_decision_table`), so the falsifier cannot be
exercised by EXECUTE here.

## 3. Arms, metrics, controls

Arms: `T-MULTIRES` (treatment, not live as specified) vs `B-FLAT-CACHE`, `B-NN`,
`B-PROCEDURAL` (mandated strong baselines), `B-EMPTY` (mandated empty-registry ablation),
plus disclosed identity control `B-CROSS-SESSION-COMPILE` (frozen measured == T),
null `NC-MECHANISM-OFF`, oracle positive `PC-EXACT-REPLAY`. Full policies and frozen
expectations: spec.json `baselines`, `positive_control`, `null_control`.

Primary metric `M-COST-PER-VERIFIED-SAFE-SUCCESS` (counter-only total per VERIFIED SAFE
success; aliases `http_requests=http_calls`, `repair_attempts=repair_calls`);
secondaries success rate, cost margin, `M-NOVELTY-GROWTH`, `M-LENGTH-GROWTH`.
Validity gates V1–V8: spec.json `measurement_validity`. No LLM arm exists (B3
NOT_SATISFIED); model calls/tokens would be structural zeros recorded as blockers,
not results.

## 4. Parent handoff preservation (four-way state)

Parent `EXP-PRODUCT-38234098353/handoff.json` state is preserved verbatim in
spec.json `parent_handoff_received.state_preserved`; key lines: the bounded positive
(measured trust root + syntactic adequacy, FA=0 within-envelope, coverage 1.0, three
mechanisms separately necessary) is established for the synthetic eleven-family bank
only; the B11 trusted-origin budget-sparse boundary (FA=3) and scorer endogeneity are
open unknowns; C-PARAM-INHERIT stays EXPERIMENTAL in all branches; no promotion; no
carrier substitution; no self-dispatch. Per the mandate's SUPERSEDE disposition, the B11
next_question is sequenced after this derisk, not rejected — this DESIGN takes no
position on B11 beyond that preservation.

## 5. Legacy comparison (targeted, not wholesale)

Screened `codex/legacy_brief.json` and the cited artifact identities (no 22 MB ingest;
no `SPIDER_CODEX.md` wholesale read):

- **P2-REPLAY-COST** (pre2 artifact 4.114, sha `9687ff787f2d74460bb7006826008852f5b4416b`,
  HISTORICAL_AUDITED_BOUNDED): withdrawn 8.5x → 1.002x matched (2.822s vs 2.816s).
  Guard honored here: matched cells and fully-loaded counterfactual discipline are built
  into the metric (counter-only cost per VERIFIED SAFE success at matched correctness).
- **P2-BLIND-COMPOSITION** (artifact 4.697, sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`,
  HISTORICAL_BOUNDED_NEEDS_EXACT_PRIMARY_CHECK): 3/3 with weak baselines. Guard honored
  here: the strongest baseline is retained rather than straw-manned — which is exactly
  what makes SUPPORTS unreachable. A design that dropped B-PROCEDURAL to manufacture a
  win would violate this guard.
- **P2-MIND2WEB** (archived Codex §1): retrieval 26.7% vs strict causal chains 2.27% —
  motivates distinguishing retrieval from mechanism inheritance; the V3 instrument
  already does (compile-vs-retain over identical raw information).

**Classification: LEGACY: DISTINCT_EXTENSION** (concurring with the Director with
conditions). No pre-2.0 artefact ran the counter-only novelty-scaling falsifier on a
certified non-ceiling bank, so the question is not a pre-2.0 duplicate. But the
degenerate structure found here is a Research-2.0 instrument property, not a pre-2.0
inheritance. No pre-2.0 result is relitigated, promoted, or overturned.

## 6. Cheap pre-freeze satisfiability probes (DESIGN-stage, non-outcome-bearing)

No confirmatory/outcome-bearing measurement was run. Four read-only probes:

- **P1 — carrier identity + capability.** `sha256sum src/spider/kernel.py` at HEAD
  `81fd5ef5` → `3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3`
  (identical to the frozen value; `git status` clean for `src/`). `grep` for
  `mod|affine|regress|lstsq|numpy` in `kernel.py`: no hits; `distill_parameterized`
  (lines 280–360) induces single-level string-template slots with regex supports only.
  Conclusion: byte-identical ⇒ identically incapable of the affine chain task. The
  mandate's "byte-identical carrier supplies the distinction" leg fails: identity of
  bytes preserves incapability, it does not create executability.
- **P2 — frozen counter re-read.** `codex/experiments/EXP-RUNTIME-38194351940/result.json`
  (`status=COMPLETE`, `outcome=SUPPORTS`): success matrix confirms ceiling at novelty
  0.0/0.25 (all arms 1.0, both families) and the (K-1)/K split at 0.5/0.75; per-instance
  counters confirm T == B-CROSS-SESSION-COMPILE == PC-EXACT-REPLAY exactly (F1 total 50,
  F2 total 62) vs memorization arms (F1 53/58/61, F2 65/72/75). Conclusion: the
  empty-registry leg restates the already-ROBUST memorization contrast; the mandated
  T-vs-B-PROCEDURAL contrast remains identity under the generalizing reading.
- **P3 — novelty-grid degeneracy re-derivation.** From the frozen matrix: scored points
  n=2 with tied advantages ⇒ `M-NOVELTY-GROWTH = 0.0` exactly, permutation `p = 1.0`;
  margins 8→10 across K ⇒ `M-LENGTH-GROWTH = +2`. Conclusion: the "new falsifier" is the
  prior falsifier verbatim, and it is entailed a priori with the wrong sign in both
  dimensions.
- **P4 — product-scope workspace search.** `grep` for `SBA-CREDENTIAL-FREE-V3`under
  `src/ tests/ sdk/ research/harness/ research/product/`: no harness files (only
  request/spec/prereg references); `grep` for `multires|multi-resolution|multiscale` in
  product scope: no implementation. Conclusion: no new local artifact repairs the
  instrument since the predecessor; `freeze_artifacts=[]` with `freeze_artifacts_bound =
  NOT_APPLICABLE` is correct because there is nothing mutable to bind, not because
  dependencies were ignored.

## 7. Advisory minimal re-scopes (NOT substituted; for the Director only)

If the Director wishes a freezable follow-up, three minimal repairs — each requiring a
NEW mandate; none is adopted here:

- **R1 — Asymmetric-discovery bank.** Replace the symmetric mandatory-discovery V3 class
  (where every arm pays full discovery) with a credential-free substrate with
  ASYMMETRIC discovery (one-time session/resource/schema discovery amortized across
  tasks), tested against the same counter-only certificate. Restores a live cost channel
  without an LLM arm. (Cf. EXP-PRODUCT-37989728440 next_question fallback.)
- **R2 — Instrumented representation cost.** Extend the counter family with a justified,
  pre-registered representation channel (build/inference/reuse cost in commensurable
  counter units) so that two mechanism-containing representations CAN separate; the
  counter itself must first be justified against real per-operation costs (cf. the
  Runtime counter-justification repair thread). Without this, any multi-scale claim on a
  protocol-counter-only instrument is non-identifiable by construction.
- **R3 — Exogenous capability gate first.** Fund the Intel B3 programmatic endpoint (or
  Runtime B1 executable-carrier repair) before any further Product derisk on this bank
  class; the flagship four-arm benchmark remains the decision that matters, and derisks
  that cannot separate treatment from the strongest baseline consume cycles without
  moving it.

Stop/pivot trigger (unchanged): treatment/comparator distinction collapses → abort and
fail loud, as done here. A fourth re-run of the symmetric mandatory-discovery
deterministic certificate without one of R1/R2/R3 should be PARKed, not funded.

## 8. Self-attack (pre-finalization)

- **Empty/unreachable branches?** SUPPORTS is proven unreachable (identity +
  growth-sign lemmas); FALSIFIES is entailed a priori — that IS the finding, recorded
  in `identifiability_precedence`, not hidden. No branch promises an EXECUTE outcome.
- **Missing prerequisites?** `measurement_prerequisites=PASS` (V3 certified, B2
  discharged); the missing pieces (B1 executable carrier for affine tasks, B3 endpoint)
  are recorded as blockers, and their absence is why Horn 2 fails — correctly routed to
  `treatment_liveness=FAIL`, not to a fake negative.
- **Treatment/comparator identity?** Directly confronted as the central FAIL; both
  readings of B-PROCEDURAL are traced; the strawman-partial-generalizer temptation is
  explicitly barred by the strongest-fair-baseline rule.
- **Ceiling baselines?** The 0.0/0.25 ceiling grid is documented (V5), not exploited;
  no success-rate advantage is claimed where the mechanism is inactive.
- **Insensitive controls?** `control_sensitivity=PASS` is bounded to the live contrast
  only, with the boundary (no control separates two mechanism-containing
  representations) stated in the reason — sensitivity is not over-claimed to rescue
  reachability.
- **Unbound mutable artifacts?** P4 verifies emptiness by search; `freeze_artifacts=[]`
  + `NOT_APPLICABLE` with reason satisfies the v2 contract for a non-freezing design.
- **Outcome-bearing measurement in DESIGN?** None: every number derives from frozen
  accepted evidence or read-only probes; no bank was instantiated, no arm executed.

## 9. Consequences

- **If the Director accepts this DESIGN failure:** no EXECUTE, no freeze, no promotion
  (`promote_to_product=false` implied; no code written, carrier untouched). The flagship
  stays unfunded pending R1/R2/R3 or B1/B3 resolution. C-RESIDUAL-NOVELTY remains at its
  Codex effective status EXPERIMENTAL (this DESIGN stage moves no claim).
- **If a future repaired instrument falsifies validly:** retire the multi-scale
  representation claim on that bank class; redirect via R1/R2/R3 or orthogonal
  mechanisms. **If it supports validly:** license flagship planning only (B1/B3-gated),
  never direct promotion.
- **What this packet must not become:** a fourth outcome-bearing run of the symmetric
  V3 certificate; a T-vs-memorization-only re-run presented as the mandated four-baseline
  test; a strawman-baseline positive; or a silent drift back to the B11 guard question
  (SUPERSEDE preserves its sequence).

---

*DESIGN-stage provenance: probes run 2026-10-16 on base_sha `677bd0d2...` / HEAD
`81fd5ef5`; carrier re-hash `3a6caf97...`; frozen runtime evidence
`codex/experiments/EXP-RUNTIME-38194351940/result.json` (COMPLETE/SUPPORTS, audit PASS);
claim states `codex/claim_state.json` effective events (C-RESIDUAL-NOVELTY EXPERIMENTAL,
C-MEAS-VALID VALIDATED, C-PARAM-INHERIT EXPERIMENTAL); parent handoff sha
`afd53584...`; legacy brief + artifact SHAs as cited. No outcome data generated or
inspected.*
