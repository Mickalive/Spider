# EXP-FRONTIER-36249071934 — producer report

Lane: `frontier`
Frozen claim: `C-RESIDUAL-NOVELTY`
Producer stage: EXECUTE
`status = COMPLETE`, `outcome = MIXED`
Frozen decision-rule classification: `DEOPT_DOMINATES`
Producer position on the frozen falsifier: **not triggered** (see §7 and `result.json.falsifier_note`)

This report is explanatory. The machine handoff is `result.json`. The bound on the claim belongs to
the independent AUDIT; the bounded decision belongs to the lane DIRECTOR. Nothing here promotes a
claim or modifies Product code.

---

## 1. What was frozen and what was run

The frozen design is in `spec.json` and `prereg.md`, sealed by `freeze.json`. All frozen inputs were
re-hashed before execution and matched:

| frozen input | sha256 |
|---|---|
| `request.json` | `a8e62c29148047fb86763ea45916abc33c87c01e2530eec24cd6b8979e16e1c7` |
| `spec.json` | `7db7ee2e783d77523912a75012640e5c5622572930cd7c2ccc4858c7d0a51dc1` |
| `prereg.md` | `96627a9de0993b0b31a8183e761d2ecafebe9f29006f222d4098e26d264999c0` |

The frozen question was: on a real, reachable, deterministic, browser-free, key-free local HTTP
substrate, what is the measured per-span witnessed-determinism fraction of a task execution, and does
a no-memory compiled executor with a selective deopt-to-agent ratchet achieve lower amortised
end-to-end cost than inherited-mechanism execution at matched correctness?

Executed, exactly as preregistered: 3 primary arms × 50 episodes × 24 spans = 3600 spans, plus
`PC-WITNESSED-DETERMINISM` (50 episodes), `NC-ZERO-DETERMINISM` (50), `PC-EXACT-REPLAY` (2) and
`NC-EMPTY-REGISTRY` (1). Final wall time 559.2 s. One non-decision-gating addition: a 5-point
novelty-rate sensitivity sweep, 5 points × 2 arms × 20 episodes × 24 spans = 4800 spans (§6, `DEV-1`).
Total 8442 model-oracle invocations, 0 real LLM calls, 0 browser sessions, 0 docker invocations,
10 848 real HTTP round trips against the substrate plus 800 for the idempotency check.

---

## 2. RAW EVIDENCE

Durable, hash-verified evidence. `artifacts/run_manifest.json` records the sha256 of all 16 of these;
every hash was re-read from disk and verified after the final run.

| path | content | role |
|---|---|---|
| `artifacts/spans_no-memory-deterministic.jsonl` | 1200 span records, Arm A | raw |
| `artifacts/spans_inherited-spider.jsonl` | 1200 span records, Arm B | raw |
| `artifacts/spans_cold-exploration.jsonl` | 1200 span records, Arm C | raw |
| `artifacts/episodes_*.jsonl` (3 files) | 50 episode ledgers per primary arm | raw |
| `artifacts/control_spans_pc_witnessed_determinism.jsonl` | 1200 control span records | raw |
| `artifacts/control_spans_nc_zero_determinism.jsonl` | 1200 null-control span records | raw |
| `artifacts/control_spans_pc_exact_replay.jsonl` | 48 replay-control span records | raw |
| `artifacts/kernel_probe.json` | direct probes of the shipped `SpiderKernel` | raw |
| `artifacts/substrate_determinism_check.json` | 8 request shapes × 100 identical repeats | raw |
| `artifacts/availability_probe.json` | substrate/credential availability | raw |
| `artifacts/matched_task_instances_check.json` | cross-arm span-identity check | derived |
| `artifacts/controls.json` | control verdicts | derived |
| `artifacts/sensitivity_novelty_sweep.json` | sweep points | derived |
| `artifacts/derived_metrics.json` | all preregistered metrics | derived |

Code under test: `research/frontier/{substrate_deterministic_http,taskplan,measure}.py` and
`research/frontier/arms/{common,deopt_ratchet,inherited_spider,cold_exploration}.py`, driven by
`research/frontier/run_experiment_EXP_FRONTIER_36249071934.py`. The incumbent arm imports
`src/spider/kernel.py`, `src/spider/models.py` and `src/spider/registry.py` **unmodified**; those
three files were not edited by this experiment and are hashed in `result.json.artifacts`.

---

## 3. OBSERVATIONS (what was directly seen, not interpreted)

1. A Python-stdlib `ThreadingHTTPServer` on `127.0.0.1` served real HTTP/1.1 keep-alive
   GET/PUT/PATCH/DELETE traffic. No Flask, FastAPI, BrowserGym, Playwright, Chromium or LLM
   credential was present. All 3600 primary-comparison spans executed over real sockets, plus 4800
   sweep spans.
2. Substrate idempotency held: 8 request shapes × 100 identical repeats = 800 round trips, every shape
   returning exactly one response-body hash and one status code, destructive verbs exercised on their
   success path.
3. All three arms observed the identical span population. For all 1200 shared `(episode, index)` keys
   the span signature, status code and response-body hash are equal across arms.
4. `SpiderKernel.distill()` returned mechanisms at confidence `0.5`; `SpiderKernel.__init__` sets
   `min_confidence = 0.8`. Over 1200 resolve calls on a 24-mechanism registry: 689 `EXPLORE`,
   511 `UNKNOWN`, **0 `EXECUTABLE`**, 0 mechanisms executed.
5. The only confidence literal in `src/spider/` is `0.5`; there is no `distill_parameterized`.
   `distill()` left `parameter_slots`, `freshness`, `applicability_guards`, `verification_rule`,
   `repair_scope` and `failure_boundary` empty on all 24 mechanisms.
6. Diagnostic probe (no arm used it): a resolve at `min_confidence = 0.5` returned `EXECUTABLE` on the
   exact intent and preconditions, and `verify()` returned `True`. A paraphrased intent
   (`create a new resource on the server`) resolved `UNKNOWN` against an exact `create_resource`
   mechanism.
7. Arm A compiled 10 of 511 observed state keys, completed compilation during episode 2, served 480
   span occurrences from compiled replay, and fell from 24 model calls/episode (episodes 1–2) to 14
   (episodes 3–50), stable thereafter.
8. `PC-WITNESSED-DETERMINISM` reached determinism 1.0, compiled 20 state keys, and settled at exactly
   4 model calls per episode.
9. The witness-count histogram is strictly bimodal: 500 occurrences witnessed in exactly one episode,
   700 in all 50. No intermediate counts.
10. The docker CLI is present in this environment but was recorded and not used.

Full list with identical wording in `result.json.observations`.

---

## 4. DERIVED MEASUREMENTS

### 4.1 Primary estimand — `per_span_witnessed_determinism_fraction`

| quantity | value |
|---|---|
| deterministic span occurrences | 700 / 1200 |
| **fraction** | **0.5833333333333334** |
| Wilson 95% CI | `[0.5552167229809802, 0.6109181102518974]` |
| unique span signatures | 511 |
| per-arm cross-check | 0.5833333333333334 in all three arms |
| prereg H1 (≥ 0.70) | **not met** |
| learning curve (ep 10/20/30/40/50) | 0.5238095238095238 at every checkpoint |

### 4.2 Amortised cost at matched correctness (abstract units/episode)

| arm | compile | machinery | model | execution | total | success |
|---|---|---|---|---|---|---|
| `B-NO-MEMORY-DETERMINISTIC` | 10 | 0 | 720 | 1200 | **38.6** | 1.0 |
| `B-INHERITED-SPIDER` | 0 | 1200 | 1200 | 1200 | **72.0** | 1.0 |
| `B-COLD-EXPLORATION` | 0 | 1200 | 1200 | 1200 | **72.0** | 1.0 |

Paired bootstrap, 10 000 resamples, seed 20260926: deopt − inherited = **−33.4**,
CI95 `[−34.0, −32.4]`, p = 0.0. deopt − cold is identical, for the reason in §5.2.

Frozen rule outcome: `DEOPT_DOMINATES` (38.6 < 72.0 and 38.6 < 72.0, both arms at success 1.0 ≥ 0.95).

### 4.3 Determinism versus compilability

| quantity | value |
|---|---|
| deterministic occurrences | 700 |
| served by compiled replay | 480 |
| deterministic but deopted | 220 |
| `compilable_given_deterministic` | 0.6857142857142857 |
| `compiled_share_of_all_spans` | 0.4 |

The 220-occurrence gap was re-derived independently from the raw span records and splits exactly:

| cause | occurrences | where |
|---|---|---|
| state key ambiguous (recurs, but maps to >1 correct action) | 100 | `create_resource` of the two episode-invariant work items |
| state key never recurs (embeds an episode-specific previous request) | 100 | `entry_point` following an episode-specific create |
| fewer than 2 witnesses (prereg 6.1 compilation rule) | 20 | first two occurrences of each remaining key |

In the main run only work items 2 and 3 use episode-invariant resource paths, so only their
`create_resource` spans are witnessed-deterministic; work items 0 and 1 get episode-specific paths
(`r-<episode>-<item>`), witness count exactly 1, and are not deterministic at all.

### 4.4 Residual-novelty cost by tier (Arm A)

| tier | spans | compiled replays | model calls |
|---|---|---|---|
| never_seen | 511 | 0 | 511 |
| seen_once | 14 | 0 | 14 |
| seen_multiple | 675 | 480 | 195 |

### 4.5 Controls

| control | expected | result |
|---|---|---|
| `PC-WITNESSED-DETERMINISM` | determinism ≥ 0.99 by ep 10 **and** zero model calls after ep 1 | **FAIL** — determinism 1.0 ✓; 4 model calls/episode from ep 3 → 216 calls over ep 2–50 (192 strictly after compile completion) |
| `NC-ZERO-DETERMINISM` | determinism 0.0, cost ≥ cold | **PASS** — determinism 0.0, 1200 unique signatures, 1200 model calls; cost ratio 1.0 on the literal prereg 7.2 formula, 0.6666666666666666 machinery-inclusive |
| `PC-EXACT-REPLAY` | measured, not decision-gating | **FAIL as an executability instrument** — 0/48 `EXECUTABLE`; 27 `EXPLORE` ("confidence below execution threshold"), 21 `UNKNOWN`; all 24 ep-2 spans novel |
| `NC-EMPTY-REGISTRY` | empty registry → all `UNKNOWN` | **PASS** — 24/24 `UNKNOWN` |

### 4.6 Kernel probe (diagnostic, no arm used it)

`distill` confidence 0.5; kernel `min_confidence` 0.8; exact intent+preconditions → `EXPLORE`;
paraphrase → `UNKNOWN`; resolve at 0.5 → `EXECUTABLE`; `verify()` → `True`; no
`distill_parameterized`; shipped confidence literals `[0.5]`.

---

## 5. INTERPRETATION (producer, bounded)

### 5.1 The headline fraction is a property of the task plan, not of agent work

`prereg.md 5.2` fixes the five intents, the signature and the episode structure, but never fixes the
task generator's residual-novelty rate — the dominant free parameter of the design. The value 0.5833
is a property of the pre-declared mixture at the neutral midpoint novelty rate 0.50. The sweep shows
the same experiment yields 1.0 down to 0.1667 across the grid. **The determinism fraction must not be
promoted to a claim-level number about real Web work.** What is informative is the *rung* — the arm
ordering at fixed novelty, and the monotone novelty→determinism relation.

### 5.2 The three-way comparison's inherited leg is not identified, and the frozen rule cannot detect it

This is the most important line in this report.

`prereg.md 6.2` mandates the shipped kernel with `distill()` at confidence 0.5 and `min_confidence`
0.8. Under exactly that configuration the incumbent executed **zero** mechanisms in 1200 spans, so
`C_i` measures *shipped kernel plus perfect-model deopt on every span*, not inherited-mechanism
execution. Because `C_i` came out exactly equal to the mandatory null `C_c` (72.0), the only
difference between the incumbent arm and inheritance ablation is a registry the incumbent can never
use.

Consequences:

- The `C_d < C_c` leg **is** a clean within-design comparison: same oracle, same substrate, same
  tasks, same success rate. A no-memory compiled executor with a deopt ratchet is genuinely cheaper
  than always deopting, on this plan family, at this cost model.
- The `C_d < C_i` leg is **not** identified. It cannot separate "inheritance is uneconomic" from "the
  shipped kernel cannot execute".

`DEOPT_DOMINATES` is therefore mechanically correct and scientifically narrow. `PC-EXACT-REPLAY` is
the pre-declared instrument check that makes this unambiguous, and it fails the same way.

This is the same identifiability defect the parent handoff recorded as audit findings B1/B2 for
`EXP-FRONTIER-36129180789`. `prereg.md 6.2` re-states `min_confidence 0.8` verbatim rather than
repairing it, so the defect propagated by construction.

### 5.3 On the frozen falsifier

`spec.json.falsifier` says `DEOPT_DOMINATES`/`DEOPT_TIES` → `FALSIFIED-IN-SETTING` for SPIDER's
central inheritance premise. The producer reports **not triggered**. The falsifier's discriminating
premise is an identified comparison against an *executable* inherited arm; this instrument has none.
Encoding the nominal trigger as fired would convert a missing measurement into a negative scientific
result, which the packet contract forbids. The auditor and Director own this decision.

### 5.4 What the `PC-WITNESSED-DETERMINISM` failure means

The determinism component of the control reached 1.0 by episode 10 as required. Only the "zero model
calls after episode 1" component failed. It failed because the four work items are *observationally
identical but goal-distinct*: all four present the state (empty store, last request `GET /`) and
require four different correct actions. A no-memory state→action table provably cannot disambiguate
them without parameter induction, and `prereg.md 6.1` forbids parameter induction in this arm. The
failure is a property of the preregistered architecture, not of the substrate or the instrumentation.

### 5.5 Representation loss

The substrate is a self-authored, single-machine, stateless-per-episode CRUD service: no DOM, no
accessibility tree, no cross-site state, no auth, no rate limiting, no partial failure, no
adversarial content. Success 1.0 in all three arms reflects a perfectly deterministic substrate, not
robust agent behaviour. Generalization to live heterogeneous Web work is `C-CROSSSITE` /
`C-WEB-DYNAMICS` and is explicitly not tested here. The cost model is a preregistered abstract unit,
not a measured economic quantity: no tokens, no latency, no dollars. `token_denominated_cost` and
`browser_or_dom_measurements` are `null` for that reason. The model oracle is a deterministic perfect
policy, so the deopt arm's advantage is an *idealised upper bound* relative to real model pricing and
real model reliability.

---

## 6. Frozen design deviations and reconciliation (full list in `result.json.frozen_design_deviations`)

- `DEV-1` **addition, not substitution** — 5-point novelty sweep (4800 spans) because the frozen design
  leaves the novelty rate unspecified and novelty determines the primary estimand. All 250
  decision-bearing episodes ran unchanged; the classification was computed only from them.
- `DEV-2` **implementation choice** — `prereg.md 6.1` does not say how a no-memory executor locates a
  compiled span without a model. Implemented as a (world state, own last request) key with a
  conservative refusal to compile any key that ever maps to two different correct actions. No plan,
  step index or goal is given to this arm, so the choice weakens the treatment arm. This is the
  opposite of parent defect B1.
- `DEV-3` **reconciliation** — `prereg.md 7.2` (three cost components) vs `prereg.md 6.2` (per-span
  inheritance machinery) resolved by a fourth ledger component `machinery`, 1 unit per span for any arm
  that performs a resolve. Setting it to 0 recovers the literal three-term formula. Machinery is
  charged to the mandatory null too, so the comparison is conservative against the treatment arm. It
  is the entire reason `NC-ZERO-DETERMINISM` has two cost ratios; both are reported and PASS uses the
  literal formula.
- `DEV-4` — `NC-ZERO-DETERMINISM` additionally forces a per-episode query nonce on every span, as
  `prereg.md 8.2` itself prescribes.
- `DEV-5` — `taskplan.py` and `build_result_*.py` were added inside the lane's allowed code root so
  the plan structure, the novelty constant and the nonce rule are inspectable in code, and so no
  reported figure is hand-transcribed into `result.json`.
- **Unresolvable-by-EXECUTE spec/prereg inconsistency** — `spec.json`'s positive control says "compile
  all spans on first episode" / "model_calls_after_compile=0" while `prereg.md 6.1` step 2 requires
  ≥2 witnesses and `prereg.md 8.1` reads "model_calls_after_episode_1 = 0". Under the prereg rule
  compilation completes during episode 2, so episode 2 still deopts. Both readings are reported (216
  literal, 192 post-compile); PASS/FAIL uses `prereg.md 8.1` under `prereg.md 6.1`. **The specification
  was not edited to remove the ambiguity.**

---

## 7. What this run did and did not settle

**Settled, within this setting and cost model:**

- A no-memory compiled executor with a selective deopt ratchet is cheaper than always-deopting at
  matched correctness (38.6 vs 72.0 units/episode, paired bootstrap CI `[−34.0, −32.4]`), and cheaper
  at every swept novelty rate.
- Compilation payoff is real but bounded: 0.4 of spans served from compiled entries, model calls
  falling 24 → 14 per episode and then flat. A witnessed-deterministic span is *not* automatically
  compilable (0.6857 given determinism), and the three measured obstacles are now separated.
- The shipped kernel, at the configuration `prereg.md 6.2` mandates, cannot execute anything it
  distils: confidence 0.5 distilled vs a 0.8 gate, no parameterised distillation, no freshness,
  applicability, verification, repair or failure fields populated, and exact-intent-only matching.

**Not settled:**

- Whether inherited-mechanism execution is economically superior, inferior or indistinguishable to a
  no-memory compiled executor. **The experiment contains no observation of working inheritance.**
- The per-span determinism fraction of real agent work. Measured only on an experimenter-authored plan.
- Whether `C-SEMANTIC-RESOLVE` is structurally unreachable (consistent with one paraphrase probe, not
  established).
- Whether the deopt advantage survives a non-ideal model; whether the incumbent would be
  cost-competitive once executable.
- Whether `DEOPT_TIES` / `DEOPT_LOSES` are reachable on this substrate at all — the incumbent's cost is
  pinned to the null's by total non-executability, which no novelty setting can change.

The external convergent-compilation figures in the director mandate were **not** imported and **not**
compared against anything here. They remain unverified agent priors; only an Intel artifact could
license that comparison.

No Product code was modified, no mechanism was promoted, no claim was self-promoted, no frozen input
was edited. This is a producer handoff.

---

## 8. Handoff pointers for AUDIT

Recompute or dispute using these exact identifiers:

- metric `primary_estimand` (value, Wilson CI, `per_arm_cross_check`), `determinism_witness_count_histogram`,
  `determinism_fraction_by_episode_checkpoints`, `compilability_boundary` incl.
  `deterministic_but_deopted_exact_split`, `amortized_cost_breakdown`, `success_rate`,
  `cost_difference_bootstrap`, `deopt_arm_operational`, `inherited_arm_operational`,
  `kernel_direct_probe`, `determinism_vs_target_novelty_rate_sweep`
- controls `PC-WITNESSED-DETERMINISM`, `NC-ZERO-DETERMINISM`, `PC-EXACT-REPLAY`, `NC-EMPTY-REGISTRY`
- validity attacks to prioritise: inherited-leg identifiability (§5.2), generator-relative estimand
  (§5.1), `PC-WITNESSED-DETERMINISM` verdict under the spec/prereg inconsistency (§6), Wilson CI
  clustering, `DEV-1..DEV-5`
- fields to dispute: `outcome=MIXED`, `falsifier_triggered=false`, `hypothesis_statuses`
