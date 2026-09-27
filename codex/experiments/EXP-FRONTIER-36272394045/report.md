# EXP-FRONTIER-36272394045 — EXECUTE report

**Lane:** frontier  **Status:** COMPLETE  **Outcome (primary cost basis):** INCONCLUSIVE

Question: does goal conditioning, without inherited parameterization, reach the ratchet's
served-span coverage and cost, and is the ratchet's residual irreducibly binding?

## 1. What was run

The frozen design was executed as written: 5 novelty rates x 50 episodes x 7 arms over the
parent's deterministic HTTP task substrate, 24 span occurrences per episode, 6000 classified
span occurrences on the main grid plus 1200 each for the positive and null controls.
35600 substrate requests, 22.9 s wall clock,
no model calls, no network.

The reference arm was reproduced **field for field** from the parent packet
(1200/1200 rows identical,
0 field mismatches), so every number below is measured on a substrate
that is provably the parent's. The class-(iii) capability plant is realized exactly:
120/1200 gated span occurrences
per rate, 60/200 planted work items, and the handle is
verified absent from both the observable state blob and the goal prefix on every one.

## 2. Primary measurements

Per novelty rate. sigma_2 is read under prereg.md 8 step 2 taken literally; see section 5.

| novelty | sigma_1 (novel) | sigma_2 (blocked) | sigma_3 (absent) | witnessed det. | gamma_det | gamma_all | ref cost | cond cost |
|---|---|---|---|---|---|---|---|---|
| 0.00 | 0.6233 | 0.2767 | 0.1000 | 0.9250 | 0.9189 | 0.8500 | 34.08 | 48.0 |
| 0.25 | 0.6483 | 0.2517 | 0.1000 | 0.7500 | 0.9222 | 0.8500 | 36.64 | 48.0 |
| 0.50 | 0.6783 | 0.2217 | 0.1000 | 0.5500 | 0.9242 | 0.8500 | 40.94 | 48.0 |
| 0.75 | 0.7017 | 0.1983 | 0.1000 | 0.3583 | 0.9767 | 0.8500 | 44.84 | 48.0 |
| 1.00 | 0.7342 | 0.1658 | 0.1000 | 0.1667 | 1.0000 | 0.8500 | 47.06 | 48.0 |

Pooled over 6000 occurrences: sigma_1 = 0.6772,
sigma_2 = 0.2228 (CI95 [0.212483, 0.233539]),
sigma_3 = 0.1000,
headroom sigma_2+sigma_3 = 0.3228.

Costs are the parent's abstract units per episode at novelty 0.50: ratchet (parent-identical,
no class-(iii) plant) 38.6; ratchet with the class-(iii) plant 40.94; goal-conditioned 48.0
(24.0 on the model-calls-only basis); cold 72.0. Paired bootstrap, 5000 resamples, episode as
unit: conditioned minus ratchet +7.06 units (CI95 [6.26, 7.70], p = 0.0); ratchet minus cold
-31.06 (CI95 [-31.70, -30.26], p = 0.0).

## 3. Decision

**Clause 1 not triggered.** It requires sigma_2's CI95 upper bound below 0.01 at *every* rate.
The upper bound is 0.1879 at best. The ratchet's residual is
large and is not explained away by novelty.

**Clause 2 not triggered on the primary cost basis.** Coverage clears both thresholds
comfortably — gamma_all = 0.8500 >= 0.40 and gamma_det = 0.9242 >= 0.6857 at novelty 0.50,
and the coverage thresholds are met at every rate — but the treatment costs 48.0 abstract
units per episode against the 38.6 threshold, so the clause fails on cost alone.

NEITHER_TRIGGERED maps to **INCONCLUSIVE** in `spec.json.decision_rule.outcome_mapping`.
That is the reported outcome.

**The clause-2 result is cost-basis dependent, and this is the single most consequential
thing in this run.** prereg.md 7.2's literal wording charges 1 unit per oracle call and 0 per
execution, which puts the treatment at 24.0 units/episode and makes clause 2 fire at every
novelty rate, i.e. **FALSIFIES_SPIDER_PREMISE**. The parent's own ledger charges execution too,
giving 48.0 and no trigger. Both are reported; neither is promoted. See UR-04.

## 4. Span-level correctness, and a defect the endpoint metric cannot see

| arm | span-level action correctness | incorrect spans | goal-state success |
|---|---|---|---|
| B-COLD-EXPLORATION | 1.0 | 0 | 1.0 |
| B-NO-MEMORY-CONDITIONED | 0.85 | 180 | 1.0 |
| B-NO-MEMORY-CONDITIONED-NARROW | 0.5666666666666667 | 520 | 1.0 |
| B-NO-MEMORY-DETERMINISTIC | 0.9833333333333333 | 20 | 1.0 |
| NC-UNIQUE-STATES | 1.0 | 0 | 1.0 |
| PC-PLANTED-DISAMBIGUATION | 1.0 | 0 | 1.0 |
| REPL-REFERENCE-PARENT-IDENTICAL | 1.0 | 0 | 1.0 |

Two results sit here.

**The ratchet silently serves wrong actions on class-(iii) spans.** Across the grid it
recorded `COMPILED_REPLAY` on 1868 span occurrences,
of which 80 replayed a cached action that is *not* the declared
action. Every single one is a class-(iii) span and every single one is the `list_resources`
role: the cache key is the observable state, which does not contain the handle, so a cached
ungated `/resources` is replayed where `/resources?view=<handle>` was required.

| novelty | compiled replays | false compiled replays | roles | all class (iii) |
|---|---|---|---|---|
| 0.00 | 714 | 30 | list_resources=30 | yes |
| 0.25 | 582 | 30 | list_resources=30 | yes |
| 0.50 | 362 | 20 | list_resources=20 | yes |
| 0.75 | 162 | 0 | — | yes |
| 1.00 | 48 | 0 | — | yes |

**No status-code or goal-state metric detects any of this.** Goal-state success is 1.000 for
all seven arms, including the narrow-prefix arm that is wrong on 43.3% of its spans, because
the ungated read and list of a gated resource still return 200 and the declared goal state
(empty store) never requires the handle. Any product decision reading only success rate, HTTP
status, or a goal-state predicate would have seen no difference between these arms at all.

## 5. Controls

| control | result | criterion |
|---|---|---|
| CTRL-FROZEN-INPUTS | PASS | recomputed sha256 of request.json / spec.json / prereg.md equal freeze.json |
| CTRL-REPL-PARENT-NUMBERS | PASS | prereg.md 10.3: per-span witnessed determinism ~0.5833, compilable-given-deterministic ~0. |
| CTRL-SUBSTRATE-IDEMPOTENCY | PASS | prereg.md 10.4: 8 request shapes x 100 repeats -> exactly 1 response hash and 1 status cod |
| CTRL-ARM-STATELESSNESS | PASS | prereg.md 13: conditioned arm is a pure function action = f(observable_state, goal) with n |
| CTRL-MATCHED-TASK-INSTANCES | PASS | prereg.md 12.1: all arms execute identical task instances |
| CTRL-CORRECTNESS-INVARIANCE | PASS | prereg.md 10.5: all arms must reach success_rate 1.0; any arm below -> MEASUREMENT_INVALID |
| PC-PLANTED-DISAMBIGUATION | UNRESOLVED_BY_PREREG_CONFLICT | prereg.md 10.1: sigma_1 ~ 1.0, sigma_2 ~ 0, sigma_3 ~ 0 for planted spans |
| NC-UNIQUE-STATES | UNRESOLVED_BY_PREREG_CONFLICT | prereg.md 10.2: sigma_2 == 0 exactly and sigma_3 == 0 exactly; failure meaning = classific |
| B-COLD-EXPLORATION | PASS | prereg.md 10.3 strong baseline: 72.0 abstract units per episode, 0 compiled replays |

Two controls are **UNRESOLVED_BY_PREREG_CONFLICT**, and in both cases the substantive question
the control was meant to answer is answered, while the literal preregistered number is not
attainable from the prereg's own text.

- **Positive control.** The substantive test passes decisively: the goal-conditioned arm closes
  200/200 planted spans and the reference ratchet compiles 0/200, so goal conditioning does
  disambiguate the parent's exact failure mode and prereg.md 10.1's stated failure meaning
  (implementation defect) is excluded. But prereg.md 8 step 2 read literally labels those spans
  class (ii), so the same document's requirement that sigma_2 ~ 0 for planted spans cannot
  hold. Under the goal-aware reading required by prereg.md 7.3, they are class (i) and the
  criterion holds. Both readings are reported.
- **Null control.** All 49 class-(ii) spans come from exactly one state key occurring 50 times
  with 50 distinct declared actions: the entry-point span, whose observable state is
  necessarily (empty store, no prior request) at the start of every episode. prereg.md 13's
  stated mitigation puts the uniqueness nonce in the *world store snapshot*, but the inherited
  mechanism puts it in the request *path*, which prereg.md 5 excludes from the observable
  state. Implementing prereg.md 13's mechanism as written gives sigma_2 == 0 exactly (1200/1200
  unique state keys, 0 conflicts). The prereg's stated failure meaning — a classifier false
  positive on unique states — is therefore *not* what occurred.

## 6. Interpretation

Goal conditioning without inherited parameterization reaches higher served-span coverage than
the ratchet does (0.85 vs 0.40 compiled share of all spans) and costs more (48.0 vs 38.6). The
two mechanisms do not dominate each other: the ratchet achieves 0.9833 span-level correctness
where the treatment achieves 0.8500. What the treatment cannot do is supply a binding key it
never received, so it fails on 180/1200 span occurrences, all of them class (iii) or
mint-create spans. The remaining 85% is exactly the part where the goal prefix was sufficient.

The ratchet's residual is real and large: sigma_2 ranges 0.1658-0.2767
and is *not* recoverable by goal conditioning under the literal reading — the treatment closes
those spans only because the goal prefix happens to name the distinguishing key, which is
precisely what the positive control plants and what the treatment then closes 200/200. So the
"blocked" class is only epistemically blocked with respect to the state channel, not with
respect to the goal channel. The prereg's own two readings of class (ii) disagree about
exactly this point, and the two readings give different answers to the experiment's central
question. That is why the outcome is INCONCLUSIVE rather than a directional answer.

Reducing the conditioning prefix to intent+step+work_item+key, with identical arm code, drops
coverage from 0.8500 to 0.5667, and none of the 400 differing actions was a case the wide prefix
had got right. Goal-prefix content, not model capability, is the operative variable here.

## 7. Observations

- **OBS-01** — The parent reference arm was reproduced field for field: 1200/1200 span rows identical to the parent packet's raw evidence on state_sig, signature, response_code, response_body_hash, decision_path, role and work_item, with 0 field mismatches.
  *(source: `artifacts/replication_parent_comparison.json`)*
- **OBS-02** — sigma_3 is exactly 0.10 at every novelty rate (600/6000 pooled). The capability handle is verified absent from the observable state blob and from the goal prefix on all 600 class-(iii) spans, and 50 distinct handles exist across 50 episodes.
  *(source: `artifacts/classification_B-NO-MEMORY-DETERMINISTIC.jsonl, artifacts/matched_task_instances_check.json`)*
- **OBS-03** — sigma_2 (observable state key recurred with a different declared correct action) ranges from 0.1658 to 0.2767 across the grid, and its CI95 upper bound is 0.1879 at best, never approaching the preregistered 0.01 threshold.
  *(source: `artifacts/summary_rates.json, artifacts/falsifier_clause_1.json`)*
- **OBS-04** — The goal-conditioned arm emitted the exact declared action on 0.8500 of all span occurrences (1020/1200) at every novelty rate, and on 0.9242 of witnessed-deterministic occurrences at novelty 0.50. Both clear the clause-2 thresholds of 0.40 and 0.6857.
  *(source: `artifacts/summary_rates.json`)*
- **OBS-05** — The goal-conditioned arm's amortized cost is 48.0 abstract units per episode on the primary parent-identical ledger, against the clause-2 threshold of 38.6. The paired bootstrap gives conditioned-minus-reference 7.06 units (CI95 [6.26, 7.7], p=0.0), so the treatment is more expensive than the ratchet at every novelty rate.
  *(source: `artifacts/costs_B-NO-MEMORY-CONDITIONED.jsonl, artifacts/summary_costs.json`)*
- **OBS-06** — The ratchet emitted a NON-declared action on 80 span occurrences across the grid, every one of them a class-(iii) span and every one of them the list_resources role. In all cases decision_path was recorded as COMPILED_REPLAY while the emitted action had dropped the handle. At novelty 0.50 this is 20/362 of its compiled replays.
  *(source: `artifacts/reference_false_compile.json`)*
- **OBS-07** — Goal-state success (every step returned its expected status code and the final store was empty) is 1.000 for all seven arms, including arms whose span-level action correctness is 0.5667. The ungated read and list of a class-(iii) span still return 200, and the handle is not needed to reach the declared goal state.
  *(source: `artifacts/correctness_invariance.json`)*
- **OBS-08** — Reducing the conditioning prefix to intent+step+work_item+key lowered the treatment's coverage from 0.8500 to 0.5667; the 400 differing narrow actions were never a case where the wide prefix was correct.
  *(source: `artifacts/summary_rates.json`)*
- **OBS-09** — The positive control's 200 planted spans are all closed by the goal-conditioned arm (200/200) and none is compiled by the reference ratchet (0/200), so goal conditioning does disambiguate the exact parent failure mode.
  *(source: `artifacts/pc_verification.json`)*
- **OBS-10** — In the null control, all 49 class-(ii) spans arise from exactly one state key occurring 50 times with 50 distinct declared actions (the entry-point span, whose observable state is necessarily (empty store, no prior request) at the start of every episode). Under prereg.md 13's stated mechanism, which puts the uniqueness nonce in the world store snapshot, sigma_2 is exactly 0.
  *(source: `artifacts/nc_verification.json`)*

## 8. Validity notes

- **VN-01 (declared instrument correction (measurement, not a preregistration change))** — The first execution scored span-level correctness with each arm's OWN emitted action, which made span_level_correct_action_fraction tautologically 1.0 for every arm, and made conditioned coverage vacuous when the shared ground truth was substituted in. The correct action is now the DECLARED PLAN action bound at the moment the arm requested that plan index, identical for all arms, and every arm's EMITTED action is compared against it. No preregistered threshold, control criterion, class-assignment rule or decision rule was changed, and the parent replication numbers (0.5833 / 0.6857 / 0.40 / 38.6) were recomputed after the correction and are unchanged. Full record in artifacts/manifest.json and the derived section declared_instrument_correction.
- **VN-02 (representation loss)** — The class-(iii) plant is a synthetic capability handle (an opaque token minted by the substrate and gated on a prior response), not a real-world authorization, session or CSRF mechanism. The claim it supports is about the STRUCTURE of a binding key absent from the agent's observation and goal channels, not about any particular real protocol. The handle is a deterministic function of a fixed salt and the substrate's episode counter; the experiment does not test handle unpredictability, expiry, replay windows or cross-episode leakage.
- **VN-03 (representation loss: the conditioned arm is a rule, not a language model)** — The treatment is a pure deterministic function of (observable state signature, goal prefix). It therefore measures the INFORMATION AVAILABLE to a goal-conditioned policy, not the ability of any particular model to exploit that information. Clause 2's sensitivity cost basis (model calls only, 24.0 units/episode) credits the treatment one model call per span; a real model would add token cost, tool calls and error modes that this ledger cannot express. A real model would in any case have to read the handle out of a prior response body, which this substrate never places in a body.
- **VN-04 (the endpoint metric is insensitive to the class-(iii) binding key)** — Because the ungated read and list of a gated resource return 200 and the goal state (empty store) does not require the handle, goal-state success is 1.0 for every arm including arms wrong on up to 43.3% of spans. Any product decision that reads only success rate, HTTP status or a goal-state predicate would have seen no difference between these arms at all.
- **VN-05 (prereg internal conflicts, reported not resolved)** — Three conflicts are inherited from the frozen text and are surfaced, not resolved: (a) prereg.md 8 step 2 (literal) versus the goal-aware reading used in prereg.md 7.3/10.1, which disagree about the positive control's class assignment; (b) prereg.md 5 (observable state = store + last request) versus prereg.md 13's stated mitigation (nonce in the world store snapshot), which makes the null control's sigma_2 == 0 criterion unattainable by the inherited path-nonce mechanism; (c) spec.json decision_rule.outcome_mapping labels clause-1 'FALSIFIES_INHERITANCE_NICHE' while prereg.md 3 prose for the same clause says the ratchet residual has 'a real economic niche'. None of the three is decision-triggering in this run because neither clause fires on the primary basis, but all three would matter for a future run.
- **VN-06 (infrastructure deviations, declared)** — Two substrate changes were required to complete the preregistered program and neither alters a parent response byte. (1) The stdlib HTTP handler was given disable_nagle_algorithm = True: the handler writes headers and body as two socket writes, so with Nagle enabled the body write waited on the peer's delayed ACK and pinned the substrate at about 24 requests/second, which is what caused the two prior stage failures recorded in failure.json (exit 66) and model_execute.json (exit 124). TCP_NODELAY changes no response byte. (2) do_PUT now treats a missing request body as an empty object, matching do_PATCH, instead of raising and dropping the keep-alive connection; the narrow-prefix arm cannot reconstruct a request body, and no request the parent task plan issues ever has a missing body. Verified: the create-PUT response body is byte-identical with and without ?mint=1.
- **VN-07 (hash transcription discrepancy in the frozen preregistration)** — prereg.md records research/frontier/common.py as sha256 d9ceeb6a6bfee1bac7fcd8b65f9407dd616c171c52cfccc654b20c9f75185af6, but the tracked unmodified file hashes to d9ceeb6a6bfee1bac7fcd8b65f9403dd616c171c52cfccc654b20c9f75185af6 (3d, not 7d, at that position). The file was not modified by this run; the discrepancy is a transcription error in the frozen preregistration and is recorded here rather than corrected, because the preregistration is frozen.
- **VN-08 (cost model)** — All costs are the parent's abstract units: 1 per model/oracle call, 1 per substrate execution, plus the parent's compile and machinery charges. They are not tokens, dollars, wall-clock or browser work. The comparison conditioned 48.0 vs ratchet 40.94 vs cold 72.0 at novelty 0.50 is only meaningful under the parent's own unit definition; a real conditioned policy would additionally pay for reading the prior response and for its own prompt tokens.
- **VN-09 (environment)** — Python 3.12.14 (main, Aug 13 2026, 02:47:42) [GCC 13.3.0], git HEAD a9a0ce105a7a5f07103d99eff51339636695100d, 35600 substrate requests, 22.9 s wall clock, single machine, no network access, deterministic substrate with no real concurrency, no real model calls, no browser.
- **VN-10 (declared control deviation)** — the class-(iii) plant is disabled in this control; otherwise a planted class-(iii) span would (correctly) be reported as class (iii) and the null's exactly-zero criterion would be unattainable by construction

## 9. Unresolved

- **UR-01** — *spec.json decision_rule.outcome_mapping assigns the label FALSIFIES_INHERITANCE_NICHE to CLAUSE_1_TRIGGERED_and_NOT_CLAUSE_2, while prereg.md 3 prose for that same clause states the opposite consequence ('the ratchet's residual is irreducibly binding and inherited parameterization has a real economic niche'). Which is authoritative?*
  - producer cannot settle because: the label and the prose assert opposite consequences for one frozen condition, and resolving it would require amending a frozen input or substituting producer judgement for the Global Research Director's.
  - impact on this run: none: clause 1 did not fire on any basis, so the ambiguity is not decision-triggering here.
- **UR-02** — *Is class (ii) the prereg.md 8 literal rule (a state key recurring with any different action) or the goal-aware rule (a state key recurring with a different action that goal conditioning cannot disambiguate)?*
  - producer cannot settle because: both readings are textually supported and they give different class assignments to the positive control and therefore different sigma_2 values. The literal reading is used as primary because it is what prereg.md 8 step 2 says; the goal-aware reading is reported alongside.
  - impact on this run: material to the positive control and to the absolute level of sigma_2; not decision-triggering, because sigma_2's CI95 upper bound is far above 0.01 under either reading.
- **UR-03** — *The ratchet falsely compiled class-(iii) list_resources spans in 80 span occurrences across the grid, dropping the handle from a replayed action. Is this a cache-key defect to be fixed in the product, or an accepted consequence of a cache keyed only on the observable state?*
  - producer cannot settle because: fixing it changes the mechanism under characterisation; this run only measures it. Whether the handle belongs in the cache key is a product decision, and the substrate deliberately never returns the handle in a response body, so no cache key derivable from a response can contain it.
  - impact on this run: does not affect either clause, but it means the reference arm's own span-level action correctness is 0.9833 rather than 1.0, and any economic comparison that credits the ratchet with serving those spans overstates it.
- **UR-04** — *Under the prereg's own model calls only cost basis the treatment costs 24.0 units per episode and clause 2 fires, falsifying the SPIDER premise. Under the parent-identical ledger it costs 48.0 and clause 2 does not fire. Which basis is the intended one?*
  - producer cannot settle because: prereg.md 7.2's literal wording ('1 unit per oracle call, 0 per execution') and the parent's ledger definition disagree, and the choice flips the headline outcome between INCONCLUSIVE and FALSIFIES_SPIDER_PREMISE.
  - impact on this run: decision-determining. Both are reported; outcome is set from the primary parent-identical basis and the sensitivity result is carried explicitly.
- **UR-05** — *Is goal-conditioned coverage of 0.85 of all spans at 48.0 units/episode, against a ratchet that achieves 0.40 compiled share at 38.6 on the same task, an economic win anywhere?*
  - producer cannot settle because: the treatment is closed to 0.85 coverage and the ratchet's coverage is 0.9833, so neither dominates; the crossover would need a cost model in which a conditioned policy does not pay 1 execution unit per span, which is exactly the unresolved UR-04 question.
  - impact on this run: no clause fires; this is the product-level question the DIRECTOR must price.
- **UR-06** — *Does a real model, given the same goal prefix, behave like this rule?*
  - producer cannot settle because: no model was called in this run; the substrate returns the handle only as a response header and a server-side observation, and the prereg forbids surfacing it to the agent.
  - impact on this run: gamma_det and gamma_all are upper bounds on what a goal-conditioned policy can serve from its declared channels, not predictions of model behaviour.

## 10. What this report does not claim

- The treatment is not a language model and no model was called; coverage is an information-availability bound.
- The substrate is a synthetic capability token, not a real authorization or session mechanism.
- Nothing here promotes the class-(i)/(ii)/(iii) taxonomy or the conditioned arm into Product Core.
- The prior stage failures (exit 66, exit 124) were infrastructure timeouts and are not scientific results.

## 11. Suggested order for the Director

1. UR-04 first: settle the C_cond basis, since it alone flips the outcome between INCONCLUSIVE and FALSIFIES_SPIDER_PREMISE.
2. UR-02 second: settle the class-(ii) rule, since it sets the absolute level of sigma_2 and the positive control's verdict.
3. UR-03 third: decide whether the capability handle belongs in the ratchet's cache key, given it produced 80 false compiles that no status-code metric can see.
4. A cost model in which a conditioned policy does not pay 1 execution unit per span is required before any economic crossover between the treatment and the ratchet can be computed.

## 12. Reproduction

```
cd /home/runner/work/Spider/Spider
python3 -m research.frontier.test_conditioned_no_memory_36272394045
python3 -m research.frontier.run_execute_36272394045
```

Raw evidence: `research/experiments/EXP-FRONTIER-36272394045/artifacts/`.
Derived layer: `research/frontier/_run_output_36272394045.json`.
Full provenance: `provenance.json`. Machine-readable outcome: `result.json`.
