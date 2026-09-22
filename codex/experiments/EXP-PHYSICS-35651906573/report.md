# EXP-PHYSICS-35651906573 — Bayesian Dirichlet-Multinomial (K=12) model comparison on real TodoMVC hash-SPA transitions

- Lane: `physics` | Claim: `C-WEB-DYNAMICS` (URL fragment-aware state dynamics of everywhere-apps)
- Status: **COMPLETE** | Outcome: **SUPPORTS** (frozen decision rule → `SURVIVES_CURRENT_TEST`)
- Frozen design: `request.json`, `spec.json`, `prereg.md`, `freeze.json` (hashes verified intact — see `provenance.json`)
- Raw results: `raw_results.json` (headline numbers), `raw_output.txt` (full console transcript)

---

## 1. What was frozen and what was executed

The frozen question (spec.json): does the Bayesian Dirichlet-Multinomial model comparison
(K=12 next-state categories, alpha ∈ {0.5, 1.0, 2.0}) pass **C1** (null median log BF < 0 nats)
and **C3** (within-session shuffled-action permutation p < 0.001) on at least 2/5 real TodoMVC
hash-SPA variants, using state-history K2 = (url_before, H_K2) memories, genuine browser
interactions and fragment-aware URL states?

M1: next-state ~ DM per (state-history z, action a); M0: next-state ~ DM per z.
log BF = log ML(M1) − log ML(M0), both exact Dirichlet-Multinomial marginals (K=12, parent-identical).

All 2,040 measurement units ran to completion in a single worker: synthetic positive control
(3 alphas × 1999 shuffles on N=5000) + 5 variants × 3 alphas × 1999 shuffles on ~80 records each,
plus three baselines per variant (wall ≈ 125 s). No measurement failure; the run is bit-reproducible
(seed=42 everywhere).

## 2. Positive control (C6) — replication-exact vs parent

Synthetic stochastic 12-state hash-routed SPA, N=5000, seed=42, parent-identical environment and
null framework (EXP-PHYSICS-35578258358):

| alpha | observed log BF | observed (parent) | null median | null median (parent) | null max | p |
|-------|-----------------|-------------------|-------------|----------------------|----------|---|
| 0.5 | 643.089 | 643 | −78.360 | −78 | −21.141 | 0.0005 |
| 1.0 | 338.671 | 338 | −130.908 | −131 | −92.941 | 0.0005 |
| 2.0 | 167.898 | 168 | −116.099 | −116 | −92.767 | 0.0005 |

All three alphas: observed > 0, null median < 0, p = 0.0005 → **C6 PASS**.
The estimator implementation is validated bit-identically against the parent; real-data readings
below cannot be dismissed as an implementation artifact.

## 3. Real variants — measurements

Per variant: 144 raw browser transitions (6 sessions × 24 interactions), 112 valid, 32 link-click
leakages filtered, **80 non-leakage (NL) transitions** (C5 5/5, threshold ≥50). NL actions:
form_submit=36, button_click=26, js_navigate=18; action_target=None on all 80 (link targets only
exist on the filtered leakage records).

| variant | URL (live) | states | K2 strata det. | alpha | observed log BF | null median | null max | p |
|---|---|---|---|---|---|---|---|---|
| vanillajs | javascript-es6/dist | 4 | 17/18 | 0.5 / 1.0 / 2.0 | −11.49 / −11.54 / −10.38 | −39.73 / −32.69 / −24.82 | −29.93 / −24.90 / −19.11 | 0.0005 ×3 |
| react | react/dist | 4 | 17/18 | 0.5 / 1.0 / 2.0 | identical to vanillajs | … | … | 0.0005 ×3 |
| vue | vue/dist | 3 | 11/13 | 0.5 / 1.0 / 2.0 | −13.75 / −15.51 / −15.57 | −38.90 / −34.52 / −28.69 | −28.87 / −26.93 / −22.69 | 0.0005 ×3 |
| angular | angular/dist/browser | 3 | 11/13 | 0.5 / 1.0 / 2.0 | identical to vue | … | … | 0.0005 ×3 |
| svelte | svelte/dist | 4 | 17/18 | 0.5 / 1.0 / 2.0 | identical to vanillajs | … | … | 0.0005 ×3 |

Frozen decision rule counts (strict all-3-alpha variant pass): **C1 = 5/5, C3 = 5/5, C5 = 5/5,
C6 = PASS** → **SURVIVES_CURRENT_TEST / SUPPORTS**, ceiling bounded to the passing variants at
URL-level fragment-aware state representation.

## 4. Baselines

- **B1** URL-only conditional MI I(url_after; action | url_before), plug-in, Laplace a=1.0:
  0.0581 bits (vanillajs/react/svelte), 0.0716 bits (vue/angular). Small but > 0: a weak action
  signal conditional on the current URL alone.
- **B2** action-history K=3 prediction accuracy: **1.0** on all 5 variants — replicates the
  deterministic-FSM finding of the parent chain (EXP-PHYSICS-35290611436/35209110569).
- **B3** state-history K2 MI I(url_after; (url_before, H_K2)): 0.7020–0.8269 bits — memory alone
  strongly predicts the next state; this is the baseline against which action-conditioning M1
  competes (and loses on the absolute scale, see §5).

## 5. Interpretation — what the numbers mean (and do not mean)

Two facts define the scientific content, and they are *both* real:

1. **Relative detection (frozen C3)**: in every (variant × alpha) cell the observed log BF exceeds
   **all 1999** within-session shuffled-action null samples (p = 0.0005, the resolution floor).
   The arrangement of actions across (state-history → next-state) cells is statistically unlike a
   random shuffle of the same actions.
2. **Absolute model preference**: the observed log BF is **negative** (−10.4 to −15.6 nats) on all
   5 variants. The Dirichlet-Multinomial comparison at K=12 favors the memory-only model M0 over
   the action-conditioned M1. Actions do not buy predictive evidence beyond (url_before, H_K2)
   once the K=12 Occam penalty is paid.

Per-stratum decomposition (vanillajs, alpha=1.0) explains the mechanism: two multi-record
deterministic strata drive the negative BF (`#/ → #/` −9.68 nats; `#/completed → #/completed`
−2.15 nats); the only stochastic strata contribute +0.30/+0.56 nats; all other strata 0.00 nats.
The environment is thus a near-deterministic 4-state FSM (85–94% deterministic K2 strata; B2=1.0),
where the frozen K=12 prior over a 3–4 state space is a strong penalty — and the shuffle null is
even more negative because reshuffled action labels mix outcomes inside deterministic cells.

Two validity implications follow, both recorded in `result.json`:
- The claimed detection is *relative-to-null*; it must not be read as absolute evidence for
  action-conditioned web dynamics on this data. The claim ceiling in `verdict.json`/`handoff.json`
  should keep the fragment-aware, near-deterministic, TodoMVC-scope wording.
- Effective independent replications are ≤ 5 and possibly as few as 2: vanillajs/react/svelte and
  vue/angular are bit-identical measurement classes (isomorphic deterministic FSMs run under
  identical action protocols — a deterministic cross-check, not a bug).

## 6. Measurement-validity resolutions (AUDIT-relevant)

- **URLs**: spec shorthand `todomvc.com/examples/{vanillajs,…}/` returns HTTP 404; live serving
  URLs are the `dist/` paths frozen by the infra parent EXP-PHYSICS-35209110569. Same five
  variants, same fragment routing.
- **Action variable**: prereg's "Action: URL of the action target" is stale carryover; verified
  that this encoding is a constant on NL data (all 80 records/variant have action_target=None)
  and produces log BF ≡ 0.000000 — a degenerate test. The model action is `action_primitive`,
  matching the parent whose baselines this spec cites (EXP-PHYSICS-35262258744). Frozen priors,
  K, shuffles and seeds untouched.
- **Null**: within-session shuffle with per-session permutation RNGs seeded from a master seed=42,
  identical to the parent; C6 validates it end-to-end.
- **p floor**: 0.0005 (N_SHUFFLE=1999); "p<0.001" is satisfied at the floor.

## 7. Direct observations (raw)

See `result.json → observations` (10 items). Key raw facts repeated here for the record:
720 raw transitions; 560 valid; 400 NL; 160 link-click leakages; NL primitives only
{form_submit, button_click, js_navigate}; fragment-aware states include `#/`, `#/active`,
`#/completed`, and Angular's `#/all`; all 15 observed-BF values exceed their null maxima;
positive control matches the parent to the third decimal.

## 8. Unresolved

1. Director adjudication of C3 semantics given observed BF < 0 (relative detection vs absolute
   M0-preference) — governs claim-ceiling wording.
2. Sensitivity to K (data-matched K ≈ 4 would change the BF scale) — unfrozen, untested.
3. B1 scope discrepancy vs parent-cited 0.188–0.209 bits — reconcile before any gating use.
4. p resolution floor (1999 shuffles).
5. Effective replication count (2 vs 5 given isomorphic pairs).
6. Generalization to non-deterministic / stateful web apps — untested.

## 9. Consequences (product/claim)

- Positive route (taken): the physics estimator survives the frozen test on real browser
  transitions; C-WEB-DYNAMICS remains a supported (bounded) claim for fragment-routed,
  near-deterministic SPAs. Any product use must treat observed-BF<0 as "memory-model preferred"
  on such environments and must not claim action-conditioned dynamics absolutely.
- Negative route (not taken): if C6 had failed the run would be MEASUREMENT_INVALID; if C1/C3 had
  failed on all 5, FALSIFIED-IN-SETTING for this setting/tooling. Neither occurred.