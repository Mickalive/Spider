# SPIDER Research 2.0 — Program Audit — 2026-10-10

**Status: GOVERNANCE SYNTHESIS, NOT CANONICAL SCIENTIFIC EVIDENCE.**

This is a dated strategic reading of canonical Research 2.0 evidence. Exact scientific claims remain subordinate to `codex/experiments/<experiment_id>/`, `codex/index.json` and `codex/claim_state.json`.

Canonical corpus at audit: **431 experiments**. Coverage gaps: **0**. Quarantined packets: **2**.

## Executive conclusion

SPIDER still has **not** demonstrated a universal Web Physics and has **not** yet demonstrated the decisive product claim: that a real external LLM agent pays materially less end-to-end cost per successful partially novel Web task because SPIDER lets it inherit useful mechanisms instead of redoing the whole task.

The program has nevertheless converged on a much sharper architecture and a smaller set of real blockers.

The strongest synthesis is now:

> **Persist/reuse procedures and parameterized mechanisms; re-observe unstable values; only persist state when its re-acquisition cost is genuinely material.**

The strongest positive pillars are:
- bounded parameterized mechanism induction/binding/execution;
- a bounded intervention-valid measurement substrate;
- a bounded freshness/extraction substrate;
- evidence that ephemeral server-minted values are mostly observation-bound on the credential-free HTTP substrate tested.

The decisive missing proof remains integration into a shipped treatment plus a non-degenerate real-agent benchmark.

## Portfolio health

| Lane | Canonical | PASS | REVISE | MEASUREMENT_INVALID | FAIL | BLOCKED |
|---|---:|---:|---:|---:|---:|---:|
| Graph | 78 | 27 | 16 | 23 | 7 | 5 |
| Physics | 68 | 13 | 21 | 29 | 5 | 0 |
| Runtime | 68 | 30 | 21 | 16 | 1 | 0 |
| Product | 83 | 34 | 25 | 21 | 2 | 1 |
| Intel | 77 | 23 | 42 | 7 | 3 | 2 |
| Frontier | 57 | 20 | 17 | 17 | 3 | 0 |
| **Total** | **431** | **147** | **142** | **113** | **21** | **8** |

The dominant inefficiency is still not lack of activity. It is spending cycles on designs that later prove non-identifying, prerequisite-blocked, comparator-degenerate, or instrument-invalid. Design-contract v2 and independent DESIGN REVIEW materially reduce that risk for new transactions, but legacy/frozen transactions still expose older defects.

## Effective claim audit

### C-MEAS-VALID — VALIDATED, bounded

Strongest accepted packet: `EXP-RUNTIME-36293257855`.

Bounded result:
- authorship-separated intervention surface;
- real Chromium transport;
- frozen positive/null arms;
- point sensitivity/specificity 1.0 at the frozen fixture scope;
- lower Wilson bounds around 0.84;
- independent audit PASS.

This does **not** generalize automatically to arbitrary upstream state changes.

Newest scope-expansion packet: `EXP-RUNTIME-37973247935`, **MEASUREMENT_INVALID**. It does not downgrade the claim.

The new failure is informative about the instrument:
- response fingerprint fired on 260/260 episodes, including matched nulls;
- a volatile hop-by-hop `Connection` header leaked into the supposedly stable fingerprint;
- the capture-stability code checked vector AND fingerprint AND logical identity although the preregistered gate meant WAL-byte identity;
- only 19 stability pairs were generated instead of 20;
- the experiment stopped before arm-blind scoring/recomputation.

Consequence: repair the instrument or pivot Runtime to the more central substrate blocker; do not inherit this packet as evidence about arbitrary real drift.

### C-PARAM-INHERIT — EXPERIMENTAL

Strongest recent packet: `EXP-PRODUCT-37973256064` (audit PASS).

What is now demonstrated:
- a parameterized `distill_parameterized -> resolve -> execute` path can be live and causally attributable;
- it ran on a real credential-free localhost HTTP substrate outside the synthetic induction fixture;
- 12/15 held-out identifiers executed successfully;
- literal kernel baseline executed 0/15 because its confidence 0.5 is below the default 0.8 execution threshold;
- accounting counters were honest;
- known-negative bindings were refused.

What is **not** demonstrated:
- superiority over cold/retrieval;
- the frozen primary margin was arithmetically unreachable because cold and retrieval were both at success=1.0;
- the treatment itself was 0.80 due to a conservative support-rule generalization defect;
- no real LLM agent ran.

Critical product blocker: the richer audited parameterized carrier has not yet survived the audited promotion path into the shipped `src/spider/kernel.py`. Main still exposes literal `distill()` with confidence 0.5 and no shipped `distill_parameterized()`.

### C-FRESHNESS — EXPERIMENTAL

Strongest recent packet: `EXP-GRAPH-37978902447` (audit PASS).

Bounded result:
- four pinned credential-free, server-rendered, no-JavaScript GET-only anchors;
- two independent extraction paths agree 4/4;
- corrected session-isolation certificate passes;
- session/value extraction confirmed on 3/4 anchors;
- values rotate at per-request scale on 3/4 anchors;
- prior zero-distinct failures on these anchors were extraction/instrument defects rather than representation loss.

Still missing:
- a non-degenerate multi-anchor D1V population (value-only rotation with neither structural nor transport change);
- therefore no valid clustered false-accept estimate for the incumbent value-blind guard;
- no validated end-to-end freshness guard or economic policy.

### C-DELTA-REPAIR — EXPERIMENTAL

Strongest accepted bounded positive remains `EXP-GRAPH-36018188168`.

Later measurement-invalid distributed attempts do not scientifically downgrade the claim. The effective-state reduction machinery now preserves the accepted epistemic state instead of replacing it with a later packet's operational/measurement status.

Still missing: convincing local repair-cost and contamination results on a realistic distributed substrate.

### C-RESIDUAL-NOVELTY — EXPERIMENTAL

The claim has bounded accepted evidence that later-agent work can track controlled novelty under narrow task families.

Recent Product work exposed the main benchmark defect instead of advancing the claim:
- `EXP-PRODUCT-37989728440`: deterministic REST cold and retrieval comparators remain at success=1.0 at high novelty;
- the treatment is causally live but cannot demonstrate advantage when the comparator is at ceiling.

Frontier `EXP-FRONTIER-37950626378` is measurement-valid but does **not** measure residual novelty itself. It measured a hop-depth re-derivation ratio; its growing ratio is substantially forced by a BFS-prefix estimator and one deep host family. It correctly holds C-RESIDUAL-NOVELTY at EXPERIMENTAL.

### C-LLM-INHERIT — HYPOTHESIS

Still no valid:
`COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER`
comparison with the **same model/tools/budget** on a non-degenerate task bank.

Intel `EXP-INTEL-37973264582` established an important blocker:
- two credential-free model endpoints were available;
- the local Qwen2.5-0.5B model could not emit usable JSON actions on the minimal multi-step Web task;
- the anonymous proxy was unstable/capped and also failed;
- comparator packages are obtainable, but published same-model benchmark anchors are absent for the attained models.

Current Intel work is therefore correctly testing whether a larger credential-free 3B-8B local model or another stable anonymous endpoint can clear the minimal Web-agent capability bar.

### C-PRODUCT-ECON — HYPOTHESIS

Intel `EXP-INTEL-37950616801` is a valid bounded negative about one external artifact:
- its algebra can define a break-even reuse count;
- but a numeric `f*` cannot be derived from the artifact's own published values because a commensurable `Cwrite/Cmiss` denominator is missing.

This is **not** evidence against SPIDER economics.

The necessary quantities remain first-party:
- recurrence `h(N)`;
- `Cwrite`;
- `Cmiss`;
- explicit cold counterfactual;
- cost per successful task including retrieval, verification and repair.

### C-WEB-DYNAMICS — HYPOTHESIS

The broad universal hypothesis remains unproved.

A strong bounded negative is now canonical: `EXP-PHYSICS-37973239386` (audit PASS).

On the frozen credential-free HTTP action-gating substrate:
- 46 primary indicator fields;
- 27 sites;
- 2 predictable fields;
- predictable prevalence = 0.04348;
- site-clustered 95% upper bound = 0.116;
- frozen low/high thresholds = 0.10 / 0.25;
- all measurement-invalid gates false.

Interpretation: **value-level persistence/predictability is rare in this substrate/window**. Procedures/paths plus fresh observation look more plausible than learning a predictive law for ephemeral server-minted values.

This does not reject Web dynamics globally. Authenticated SPAs, DOM transitions, richer interventional regimes, barriers/timescales and other observables remain open.

### C-CROSSSITE — HYPOTHESIS

No true website-holdout SPIDER mechanism-inheritance result without site identity leakage exists.

### C-SEMANTIC-RESOLVE — HYPOTHESIS

Synthetic alias work produced bounded positives and negatives. No live end-to-end product path currently justifies reopening semantic resolution as an isolated micro-benchmark.

## Strongest program-level discoveries

### 1. Local continuation is an agent failure mode

SPIDER's own factory produced an empirical example of autonomous research path dependence: agents can make locally rational improvements while global research utility collapses. This motivated Scout -> Global Research Director -> specialist lanes.

### 2. Measurement design is itself a scientific object

Repeated packet failures revealed recurring classes:
- empty accept regions;
- impossible thresholds;
- controls that cannot fire;
- treatment/comparator identity;
- unavailable prerequisites;
- estimator-induced effects;
- mutable code/assets not bound at freeze.

Design-contract v2 now moves much of this cost before freeze through six explicit eligibility checks plus independent DESIGN REVIEW.

### 3. The useful inheritance unit is increasingly procedural

The evidence hierarchy now looks like:
- literal action cache for exact repetition;
- compiled workflow for same workflow/new values;
- semantic locator for layout variation;
- parameterized mechanism for homologous transformations;
- procedure/path persistence when handles rotate;
- fresh re-observation when values are unstable or cheap to reacquire.

### 4. Economics is work avoided, not representation length

Parameterization does not reliably save representation tokens. Plausible value lies in avoided exploration, browser traversal, inference, verification and repair.

### 5. Stable prediction of Web values is not the same thing as useful Web structure

Bounded non-random dynamics and bounded negatives coexist. The strongest current Physics result argues against broad value-level persistence on one real public-HTTP substrate while leaving procedural/dynamical structure elsewhere open.

### 6. Benchmark dynamic range is now a first-class prerequisite

A treatment cannot demonstrate value against a cold/retrieval comparator already at success=1.0. This is now a core readiness condition rather than something to discover after an expensive run.

## Current operational/scientific blockers

### B1 — Shipped treatment carrier

**State:** OPEN, highest leverage.

The main kernel still lacks the richer audited parameterized carrier.

**Required resolution:** Product must build the carrier on its lane, demonstrate known-positive EXECUTABLE and known-negative refusal, receive audit PASS, and promote through the pinned Product promotion path. Do not manually copy experiment code to main.

### B2 — Non-degenerate task bank

**State:** OPEN.

Current deterministic REST families give cold/retrieval ceiling performance.

**Required resolution:** Runtime/Product must certify before freeze that the selected task family has real comparator headroom and treatment/comparator behavioral distinction.

### B3 — Real-agent model capability

**State:** OPEN.

Credential-free endpoints exist, but the tested ones cannot reliably drive the minimal multi-step Web task.

**Required resolution:** Intel's bounded endpoint-provisioning experiment must either find a stable capable endpoint/local model or close the credential-free path and recommend an explicit benchmark re-scope.

### B4 — Out-of-surface measurement oracle

**State:** OPEN but no longer the unique critical path.

`EXP-RUNTIME-37973247935` failed because the response fingerprint was volatile and the stability gate implementation diverged from preregistration.

**Required resolution if this scope is pursued:** exclude hop-by-hop/volatile headers correctly, restore exactly 20 WAL-byte stability pairs, then rerun the frozen discrimination matrix.

### B5 — Freshness D1V multi-anchor population

**State:** OPEN.

Graph needs >=2 independent anchors where value rotation is not automatically accompanied by body-derived transport/structural change.

### B6 — Historical freezer/code-binding defects

**State:** FIXED FOR NEW V2 TRANSACTIONS.

Design-contract v2 now:
- binds mutable repository files through `freeze_artifacts` hashes;
- requires `freeze_artifacts_bound` eligibility;
- requires independent `design_review.json`;
- refuses freeze unless all six eligibility checks are PASS/justified NOT_APPLICABLE.

Historical packets remain bounded by the contracts they actually froze; do not retroactively upgrade them.

### B7 — Strategic-control provider reliability

**State:** FIXED/DEGRADED-SAFE.

Scout/Director use `big-pickle` first; Scout failure produces a deterministic degraded brief rather than blocking direction.

### B8 — Research-provider ordering

**State at audit: FIX APPLIED IN CONTROL BRANCH, pending merge.**

All six sampled recent successful EXECUTE stages completed on `opencode/big-pickle`, typically after four or five earlier provider attempts. Intel and Frontier then shared the same failed EXECUTE fingerprint after exhausting the fallback chain.

**Fix:** put `big-pickle` first for the Research role while retaining all other providers as fallbacks.

## Live portfolio at audit time — NOT evidence

These are execution states, not scientific results:

- Graph: active C-FRESHNESS D1V multi-anchor continuation.
- Physics: active C-WEB-DYNAMICS access-barrier onset/recovery experiment; previous DESIGN failure was retryable.
- Intel: active C-LLM-INHERIT credential-free model-capability experiment, currently resuming EXECUTE.
- Frontier: active C-RESIDUAL-NOVELTY site-native-discovery versus BFS experiment, currently resuming EXECUTE.
- Runtime: Director has selected a PIVOT toward certifying a discriminating substrate/task family rather than continuing the long oracle-extension tunnel.
- Product: Director has selected REOPEN on C-PARAM-INHERIT to produce a promotable shipped carrier before funding the real-agent benchmark.

## Priority order

1. **Product:** land the audited parameterized carrier in the shipped kernel through promotion.
2. **Runtime/Product:** establish a task bank with genuine dynamic range and honest counters.
3. **Intel:** settle the credential-free capable-model question or explicitly close/re-scope it.
4. Run the first real **C-LLM-INHERIT** four-arm benchmark.
5. Measure first-party **C-PRODUCT-ECON / C-RESIDUAL-NOVELTY** quantities, especially `h(N)`, `Cwrite`, `Cmiss`.
6. Graph: continue Freshness only if D1V becomes multi-anchor/non-degenerate.
7. Physics: pursue materially new observables (e.g. access barriers/timescales), not another value-persistence estimator.
8. Frontier: test whether site-native discovery collapses apparent depth cost before treating path persistence as a core optimization.

## What SPIDER must not claim

- universal Web Physics discovered;
- real-agent SPIDER superiority demonstrated;
- cross-site transfer demonstrated;
- freshness solved;
- product economics validated;
- a stable handle/value can generally be predicted;
- token savings are the central economic mechanism.

## Decisive missing proof

The program should stay organized around one causal chain:

> observe -> parameterized mechanism -> executable binding in the **shipped** treatment -> applicability/freshness decision -> real external-agent action -> lower end-to-end cost per successful partially novel task after retrieval/verification/repair/maintenance.

No canonical packet currently validates that chain end to end.
