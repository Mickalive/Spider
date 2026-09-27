# Preregistration for EXP-FRONTIER-36287182510

**Experiment ID:** EXP-FRONTIER-36287182510
**Lane:** frontier
**Claim:** C-RESIDUAL-NOVELTY
**Parent Experiment:** EXP-FRONTIER-36272394045 (handoff.json sha256: b4df3a0aba6d5d5488103973509a7a1b610136b2a88771350e0c599d1dc7d491)
**Director Mandate:** CONTINUE with cognitive_reset=true, target claim C-RESIDUAL-NOVELTY

---

## 1. Scientific Question

Holding the residual's three-class decomposition fixed (sigma_1 = merely-novel, sigma_2 = epistemically-blocked, sigma_3 = observation-absent) and the novelty grid fixed {0.00, 0.25, 0.50, 0.75, 1.00}, does an identified **WITHIN-EPISODE scratchpad arm** — propagating only values it read from its own earlier response bodies, inducing no parameters, compiling nothing across episodes, retaining nothing between episodes — close the observation-absent class (sigma_3), and does a **cross-episode compiled arm whose cache key includes the induced binding** close what remains, so that the **minimum persistent state required to close the residual is quantified rather than asserted**, with **span-level action correctness against the shared declared plan action** as the primary endpoint?

---

## 2. Hypothesis

The observation-absent class (sigma_3 = 0.1000 exactly, numerically identical to the generator's declared class_iii_fraction) is closed by within-episode value propagation alone — no cross-episode compilation needed. The epistemically-blocked class (sigma_2 = 0.2228 pooled, declining monotonically with novelty) requires cross-episode compilation whose cache key binds the propagated value.

The within-episode scratchpad arm will achieve span-level action correctness on class-(iii) spans that matches or approaches the ratchet's 0.9833 but at lower amortized cost (no compile/machinery units). The cross-episode compiled arm with binding-key in its cache key will close the residual at or below the parent's 38.6 threshold.

**Persistent cross-episode inheritance is therefore not necessary; a scoped within-episode scratchpad suffices for the observation-absent share, and the minimum persistent state is a cache keyed on (observable state + induced binding).**

---

## 3. Falsifier

**Primary falsifier (clause 2):** If the within-episode scratchpad arm reaches the ratchet's 0.9833 span-level action correctness **at or below its amortized cost** (on the parent's three-term ledger: 38.6 units/episode) on the declared novelty grid, then persistent cross-episode inherited parameterization is not necessary to close the residual.

**Secondary falsifier (clause 3):** If the cross-episode compiled arm with binding key in its cache key achieves span-level action correctness >= 0.9833 at or below 38.6 units/episode, then the minimum persistent state is (observable state + induced binding), not full persistent parameterization.

**Clause 1 (residual not zero):** If sigma_2 CI95 upper bound < 0.01 at all five novelty rates, the residual is statistically zero -> INCONCLUSIVE (RESIDUAL_NOT_ZERO). This clause did not fire in the parent (best upper bound 0.1879 vs 0.01 threshold) and is not expected to fire here.

**Outcome mapping:**
- SCRATCHPAD_SUFFICES: Within-episode propagation alone closes residual; persistent inheritance not necessary.
- SCRATCHPAD_CORRECT_BUT_COSTLY: Scratchpad achieves correctness but exceeds cost threshold.
- BINDING_KEY_COMPILATION_SUFFICES: Cross-episode compilation with binding key closes residual at threshold.
- BINDING_COMPILATION_CORRECT_BUT_COSTLY: Binding-key compilation achieves correctness but exceeds cost.
- NEITHER_TRIGGERED: INCONCLUSIVE — no falsifier fired, residual remains open.

---

## 4. Substrate (Measurement Validity)

**Substrate:** Python stdlib `ThreadingHTTPServer` on 127.0.0.1 with `disable_nagle_algorithm=True`. Same verified substrate as parent experiment:
- 35,600 real HTTP/1.1 requests in parent (22.9s wall clock)
- Determinism check: 8 request shapes × 100 repeats = 800 identical round trips, all deterministic
- No browser, no docker, no model API key, no network
- Two declared deviations from parent (both verified not to alter any response byte):
  1. `TCP_NODELAY` (disabled Nagle algorithm) — fixed throughput pinning at ~24 req/s
  2. `do_PUT` treating missing body as empty object — matches `do_PATCH` behavior

**Critical modification for this experiment:** The capability handle is returned in the **response BODY** (field `capability_handle`) in addition to the header, for class-(iii) spans. This makes the handle an **observable channel** — a value that can be read from a prior response body and propagated — rather than a server-side plant only visible in headers.

**Span signature (frozen 6-tuple, prereg.md section 12):**
```
(method, path, normalized_headers, normalized_body, response_code, response_body_hash)
```
Normalized headers exclude volatile transport headers: Date, Server, Host, Content-Length, Connection, User-Agent, Accept-Encoding. Body is canonical JSON (sorted keys, no whitespace).

---

## 5. Task Generator

**Base generator:** `research/frontier/taskplan.py` (unmodified, sha256: 8875a05b54761f96a92cea8d3ec43bd6886347b5e04ef81d594d65d53f910816)

**Episode structure (fixed):**
- 4 work items per episode
- 6 steps per work item: entry_point → create_resource → read_resource → update_resource → list_resources → delete_resource
- 24 spans per episode
- 50 episodes per novelty rate per arm
- 1,200 span occurrences per arm per novelty rate
- 6,000 span occurrences per arm across the full grid

**Novelty grid (frozen):** {0.00, 0.25, 0.50, 0.75, 1.00}
- Novelty rate `nu` = fraction of 4 work items that are NOVEL (resource identity scoped to episode)
- Structural work items use fixed identity `s-const-{w}`
- Entry point `GET /` is byte-identical in every work item regardless of `nu`

**Class-(iii) plant (frozen, declared 0.10 span fraction):**
- Schedule: `planted(w) <=> (3 * k) % 10 < 3` where `k = 4*(episode-1) + work_item`
- 60 of 200 work items planted (0.30 work item fraction)
- Each planted work item contributes 2 class-(iii) spans (read_resource, list_resources)
- Realized: 120 / 1200 = 0.1000 span fraction exactly

**Class-(iii) mechanism (MODIFIED from parent):**
1. Planted work item's `create_resource` issued as `PUT /resources/{rid}?mint=1`
2. Response **BODY** includes `{"capability_handle": "<handle>", ...}` (byte-identical to non-mint PUT body plus the handle field)
3. Handle also published as response header `X-Capability-Handle` and as raw server observation
4. Planted work item's `read_resource` becomes `GET /resources/{rid}?t=<handle>`
5. Planted work item's `list_resources` becomes `GET /resources?view=<handle>`
6. Handle definition: `<episode_counter:08x><sha256(MINT_SALT|counter)[:8]>` (16 hex chars)
7. Handle is a pure function of (MINT_SALT, episode_counter). NOT a function of store, path, resource identity, or plan.
8. **The only channel carrying the handle value is the mint response body (and header).**

**Goal/intent conditioning prefix (frozen):**
- **Wide (PRIMARY):** `spider-frontier-goal-v1 || intent={role} || step={i}/24 || work_item={w} || key={key} || body={body} || novel={novel} || token_required={tok}`
- **Narrow (sensitivity):** `spider-frontier-goal-v1 || intent={role} || key={key}`
- **Handle value NEVER included in either prefix.**

---

## 6. Arms (Treatments and Controls)

### 6.1 WITHIN_EPISODE_SCRATCHPAD (New Treatment Arm)

**Mechanism:**
- Propagates **only values read from its own earlier response bodies** within the current episode
- **Induces no parameters** — no parameter slots, no bind/verify/freshness
- **Compiles nothing across episodes** — no cross-episode cache
- **Retains nothing between episodes** — scratchpad cleared at episode boundary
- Decision is a pure function of: `(observable_state_sig, goal_prefix_wide, scratchpad_values)`
- When a response body contains `capability_handle`, it is stored in the scratchpad keyed by the resource identity
- On subsequent spans requiring a handle (token_required=1), the scratchpad is consulted first; if the handle for that resource is present, it is used; otherwise the ungated request is emitted (same as conditioned arm)

**Cost model (parent three-term ledger):**
- 1 model unit per span (oracle call for spans not resolved from scratchpad)
- 1 execution unit per span
- **0 compile units** (no compilation)
- **0 machinery units** (no cross-episode resolution)

**Statelessness guarantee:** The arm holds no state between episodes. The scratchpad is a local variable in `run_episode`, recreated fresh each episode. Unit-tested for statelessness (14 checks, 0 failures, plus GoalOnlyPlan AttributeError guard).

### 6.2 CROSS_EPISODE_COMPILED_BINDING (New Treatment Arm)

**Mechanism:**
- Cross-episode compiled replay cache whose **key is (observable_state_sig, induced_binding_key)**
- Compiles a span after **2 witnesses** with the same `(state_sig, binding_key)` → action mapping
- **Retains compiled spans across episodes**
- On cache hit, replays the bound action **including the binding key** (so class-(iii) spans replay correctly)
- The binding key is the capability handle value induced from a prior response in the same or earlier episode

**Cost model (parent three-term ledger + machinery):**
- 1 compile unit per unique `(state_sig, binding_key)` combination
- 1 machinery unit per span served from cache (resolve+bind+verify+freshness)
- 1 execution unit per span
- 0 model units for compiled spans (model only for deopt)

**Cache key structure:** `(world_store_snapshot, last_request_method, last_request_path, binding_key)` where `binding_key` is the capability handle value (or `None` for non-gated spans).

### 6.3 B-NO-MEMORY-DETERMINISTIC (Reference — Parent Arm, Unmodified)

- Deopt ratchet with witness threshold = 2
- Cache key: `(world_store_snapshot, last_request_method, last_request_path)` — **excludes capability handle**
- Compiles within episode only, no cross-episode retention
- Cost: 38.6 units/episode (parent three-term ledger)
- Span-level correctness: 0.9833 (80 false compiles on class-(iii) spans)

### 6.4 B-NO-MEMORY-CONDITIONED-WIDE (Reference — Parent Treatment, Unmodified)

- Pure function of `(observable_state_sig, goal_prefix_wide)`
- No scratchpad, no compilation, no cross-episode memory
- Cost: 48.0 units/episode (parent three-term ledger)
- Span-level correctness: 0.8500 all-occurrences

### 6.5 B-COLD-EXPLORATION (Null Anchor — Parent Arm, Unmodified)

- Model oracle every span
- Cost: 72.0 units/episode (constant across grid)
- Span-level correctness: 1.0 by construction (oracle is perfect)

### 6.6 B-NO-MEMORY-CONDITIONED-NARROW (Declared Sensitivity — Parent Arm, Unmodified)

- Pure function of `(observable_state_sig, goal_prefix_narrow)`
- Cost: ~48.0 units/episode
- Span-level correctness: 0.5667 (parent measured)

---

## 7. Positive Control: PC-PLANTED-DISAMBIGUATION

**Protocol (identical to parent prereg.md 7.3):**
- 200 planted spans where correct action is goal-distinct but observation-identical
- Create_resource spans: all issued from `(empty store, last_request=GET /)` with 4 different resource identities
- The within-episode scratchpad and cross-episode compiled arm **must close 200/200**
- The ratchet compiles **0/200** because the state key is identical
- This validates that the scratchpad's value propagation disambiguates the exact failure mode the parent PC measured

**Expected:** `scratchpad_closure = 200/200`, `compiled_closure = 200/200`, `ratchet_closure = 0/200`

---

## 8. Null Control: NC-UNIQUE-STATES

**Protocol (implements prereg.md 13's mechanism literally):**
- Every span carries a world-store uniqueness nonce (episode/step ID appended to **world store snapshot**, not request path)
- Under the **authoritative goal-aware class-(ii) rule** (state key + goal intent), sigma_2 must be 0
- The scratchpad and compiled arms must not introduce spurious class-(ii) labels on truly unique states

**Expected:** `sigma_2 == 0` under goal-aware rule; scratchpad and compiled arms produce no false class-(ii) on unique states

**Note on parent conflict:** The parent's literal step-2 rule gave sigma_2 = 49/1200 because every episode's first span shared one observable state key with 50 different declared actions. The parent's prereg.md 13 stated the mitigation as "nonce in the world store snapshot" but the inherited implementation put it in the request path. This experiment uses the **literal prereg.md 13 mechanism** (nonce in world store) and the **goal-aware rule** (same intent required for class-(ii)). The literal step-2 rule is rejected as authoritative.

---

## 9. Classification Protocol (Frozen, Prereg.md Section 8)

Applied span-by-span in trace order, mutually exclusive and exhaustive:

1. **Class (iii) — Observation-Absent:** The correct action depends on a binding key (capability handle) that is **absent from the current observable state AND from the goal/intent prefix**. Verified against both, not assumed. STOP.
2. **Class (ii) — Epistemically-Blocked:** The observable state key has been seen before in the reference trace with a **different correct action FOR THE SAME GOAL INTENT** (goal-aware rule). STOP.
3. **Class (i) — Merely-Novel:** Everything else: the state key is novel, or recurs with the same correct action for the same intent.

**Authoritative class-(ii) rule:** Goal-aware (state key + goal intent). The literal step-2 rule (any different action) is rejected — it conflates goal-distinct spans with true epistemic blocking.

---

## 10. Primary Metrics

All metrics computed on **shared declared plan action** ground truth (MaterializedPlan.materialized, bound at execution time, identical for all arms):

1. **span_level_action_correctness**: Fraction of span occurrences where the arm's emitted (method, path, body) exactly matches the declared plan action. **PRIMARY ENDPOINT.**
2. **class_iii_closure_rate**: Fraction of class-(iii) span occurrences closed correctly by each arm.
3. **amortized_cost_units_per_episode**: `(compile + machinery + model + execution) / episodes` on the parent's three-term ledger basis.
4. **headroom_closed**: `(sigma_2 + sigma_3) - residual_after_arm`, per novelty rate.
5. **conditioned_coverage** (for reference): Fraction of reference-trace span occurrences whose correct action the conditioned arm reproduces.
6. **closure_attribution**: Counts of spans closed by compilation only, scratchpad only, both, neither.

**Goal-state success is explicitly NOT a primary endpoint.** It was measured at 1.000 for all seven arms in the parent, including one wrong on 43.3% of spans and the ratchet with 80 silent false compiles. It is blind to the binding key.

---

## 11. Cost Basis (Declared Before Freeze)

**Single declared cost basis:** Parent's three-term compile + model + execution ledger.
- `compile` = 1 unit per unique span compiled (or per unique `(state_sig, binding_key)` for binding arm)
- `model` = 1 unit per oracle call
- `execution` = 1 unit per span executed
- `machinery` = 1 unit per span for arms that perform cross-episode resolution (compiled arm only). Scratchpad has machinery=0.

**This is the basis the 38.6 threshold was derived on.** The model-calls-only reading (1 unit per oracle call, 0 per execution) is reported as a declared sensitivity only — it does not gate any falsifier clause. The clause-2 threshold 38.6 was computed under this ledger (parent prereg.md 7.2, amortized_cost = (compile + model + execution) / num_episodes, execution 1 unit per span).

---

## 12. Corrected Clause-1 Outcome Label

**Parent conflict:** spec.json decision_rule labeled the clause-1 condition `FALSIFIES_INHERITANCE_NICHE` while prereg.md 3 prose said the same condition leaves inherited parameterization a real economic niche. Self-contradictory.

**This experiment's label:** `RESIDUAL_NOT_ZERO`. If sigma_2 CI95 upper < 0.01 at all five rates -> residual is statistically zero -> INCONCLUSIVE (RESIDUAL_NOT_ZERO). This label is neutral and does not presuppose an architectural conclusion.

---

## 13. Uniqueness Nonce (Prereg.md 13 Mechanism)

The NC-UNIQUE-STATES control implements prereg.md 13's mitigation **literally**: the uniqueness nonce is appended to the **world store snapshot** (part of the observable state per prereg.md 5), not the request path. This yields sigma_2 == 0 exactly under the goal-aware rule, as the parent's NC verification variant demonstrated.

---

## 14. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Goal-state success blindness | Primary endpoint is span-level action correctness against shared declared plan action |
| Cache key silently dropping binding key | Cross-episode compiled arm's key explicitly includes binding_key; false compile measurement tracks this |
| Scratchpad leaking across episodes | Scratchpad is local to `run_episode`; unit-tested for statelessness (14 checks + GoalOnlyPlan guard) |
| Cost basis ambiguity | Single declared basis (parent three-term ledger) in spec.json and prereg before freeze |
| Class-(ii) rule ambiguity | Authoritative rule = goal-aware (state + intent); literal step-2 rule rejected |
| Clause-1 label contradiction | Replaced with neutral `RESIDUAL_NOT_ZERO` |
| Substrate determinism | 800 identical round trips verified; TCP_NODELAY and do_PUT fix verified byte-identical |
| Handle only in header (not observable) | **Fixed:** handle now in response BODY (`capability_handle` field) |

---

## 15. Analysis Plan (Frozen Before Outcomes)

1. Run substrate determinism check (800 round trips).
2. Run CTRL-REPL-PARENT-NUMBERS: reference arm on parent-identical generator (class_iii=False) across grid; byte-level comparison to parent raw spans.
3. Run all arms across full novelty grid (5 rates × 50 episodes = 250 episodes per arm).
4. Run PC-PLANTED-DISAMBIGUATION and NC-UNIQUE-STATES at novelty 0.50.
5. Classify reference trace (B-NO-MEMORY-DETERMINISTIC) using frozen three-way protocol.
6. Compute per-arm span-level action correctness against shared declared plan action.
7. Compute per-arm amortized cost on declared three-term ledger.
8. Compute Wilson CI95 for sigma_2 at each novelty rate; test clause 1.
9. Test clause 2: scratchpad correctness >= 0.9833 AND cost <= 38.6.
10. Test clause 3: binding compilation correctness >= 0.9833 AND cost <= 38.6.
11. Paired bootstrap (episode as unit, n=50, 5000 resamples, seed=36287182510) for cost differences.
12. Report per-novelty-rate and pooled metrics with CI95.
13. Apply frozen outcome mapping.

---

## 16. Artifacts to Preserve (Raw Evidence)

- `artifacts/spans_<ARM>.jsonl` — raw span records for every arm
- `artifacts/classification_<REFERENCE>.jsonl` — per-span class labels
- `artifacts/reference_false_compile.json` — ratchet false compiles (cache key missing binding)
- `artifacts/scratchpad_closure.json` — scratchpad arm class-(iii) closure detail
- `artifacts/binding_compilation_closure.json` — binding compilation arm class-(iii) closure detail
- `artifacts/costs_<ARM>.jsonl` — per-episode ledgers
- `artifacts/pc_verification.json` — PC results
- `artifacts/nc_verification.json` — NC results (literal prereg.md 13 mechanism)
- `artifacts/conditioned_arm_statelessness_test.json` — scratchpad statelessness verification
- `artifacts/substrate_idempotency.json` — determinism check

---

## 17. No-Go Conditions (Measurement Invalid)

The experiment is **MEASUREMENT_INVALID** if any of the following hold:

1. Substrate determinism check fails (any probe non-deterministic).
2. CTRL-REPL-PARENT-NUMBERS fails field-for-field replication (n_field_mismatches > 0).
3. PC-PLANTED-DISAMBIGUATION: scratchpad or compiled arm closes < 200/200 planted spans.
4. NC-UNIQUE-STATES: sigma_2 > 0 under goal-aware rule with literal prereg.md 13 mechanism.
5. Scratchpad arm fails statelessness test (any of 14 checks fails or GoalOnlyPlan guard fails).
6. Capability handle not present in mint response body (instrument defect).

These are **measurement validity gates**, not scientific outcomes. A MEASUREMENT_INVALID verdict means the instrument cannot answer the question; it does not falsify the hypothesis.

---

## 18. Independence from Parent Conflicts

This experiment **does not inherit** the parent's three frozen conflicts:
1. **Class-(ii) rule:** Authoritative = goal-aware (declared here, not ambiguous).
2. **Cost basis:** Single declared basis = parent three-term ledger (declared here, not ambiguous).
3. **Clause-1 label:** `RESIDUAL_NOT_ZERO` (declared here, neutral).

All three are resolved **in this experiment's own spec.json and prereg.md before freeze**, as the Director mandated. The parent packet's frozen files are not amended.

---

## 19. Scope Cap (Director Mandate)

- The class-(iii) binding key **must be a named object with a defined identity** (the `capability_handle` in the response body), not a cache-key detail.
- The experiment **must state in advance which outcome would cause SPIDER to narrow or drop persistent cross-episode inheritance**: `SCRATCHPAD_SUFFICES` or `BINDING_KEY_COMPILATION_SUFFICES`.
- This cycle returns a **scope verdict** rather than an eleventh decomposition.

---

## 20. Reproducibility

- Seed for bootstrap: 36287182510 (experiment_id)
- Seed for task generator: fixed by episode counter and novelty rate
- MINT_SALT: `sha256(b"spider-mint-salt-EXP-FRONTIER-36272394045")[:16]` (same as parent)
- All code paths: `research/frontier/arms/common.py`, `conditioned_no_memory.py`, `deopt_ratchet.py`, `substrate_deterministic_http.py`, `taskplan.py`, `episodegen_36272394045.py` — plus new arms `scratchpad.py` and `compiled_binding.py` to be created in `research/frontier/arms/`
- Runner: new `run_execute_36287182510.py` in `research/frontier/`

---

**This preregistration is frozen before any outcome measurement. No analysis changes after seeing results. A changed analysis requires a new preregistration and untouched evidence.**