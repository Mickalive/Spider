# Preregistration: EXP-FRONTIER-36249071934

**Lane:** frontier  
**Experiment ID:** EXP-FRONTIER-36249071934  
**Target Claim:** C-RESIDUAL-NOVELTY  
**Director Mandate:** PIVOT (cognitive_reset=true)  
**Created:** 2026-09-26

---

## 1. Strategic Context

The Global Research Director has mandated a PIVOT from the C-RESIDUAL-NOVELTY thread, which has been:
- Validly falsified at the task-family correlation gate (rho_novelty=0.4837, CI [0.410, 0.552] < 0.60, ECE=0.216 > 0.15, RAG dominance=false) in EXP-FRONTIER-36042599040
- Blocked by 4 consecutive MEASUREMENT_INVALID packets on the WebChoreArena substrate (verified absent)
- Stalled at a 21/40 = 0.525 ceiling with 13/15 MEASUREMENT_INVALID and 2 FALSIFIED-IN-SETTING outcomes

The Director's cognitive-reset question: **what would this lane investigate meeting today's Codex cold?**

The answer is an orthogonal mechanism SPIDER has never tested: **a no-memory compiled executor with a selective deopt-to-agent ratchet**, measured at the **per-span level** on a **real, reachable, deterministic local substrate**.

This is not a rename of the failed correlation experiment. It changes:
- **Level of description**: from task-family correlation (rho) to per-span determinism fraction
- **Architecture under test**: from retrieval+compilation vs. inheritance to compile+deopt ratchet vs. inheritance vs. cold
- **Substrate**: from unavailable WebChoreArena to verified-available stdlib HTTP
- **Decision rule**: from continuous correlation threshold to three-way dominance verdict

---

## 2. Scientific Question

**Primary:** On a real, reachable, deterministic local substrate with no browser, no docker, and no LLM key, what is the measured per-span witnessed-determinism fraction of a task execution?

**Comparative:** Does a no-memory compiled executor with a selective deopt-to-agent ratchet (compile witnessed-deterministic spans, hand residual to model, recompile as residual shrinks) achieve lower amortized end-to-end cost than inherited-mechanism execution at matched correctness, with the inheritance-ablation arm (emptied registry) as the mandatory null and the incumbent shipped kernel as an additional arm?

---

## 3. Hypothesis

**H1 (Primary):** The per-span witnessed-determinism fraction on the local deterministic substrate is ≥ 0.70 (i.e., ≥ 70% of spans repeat identically across episodes).

**H2 (Comparative):** The deopt ratchet achieves lower amortized cost than both (a) SPIDER's inherited-mechanism execution and (b) cold exploration, at matched correctness (success rate ≥ 0.95).

**H3 (Falsifier):** If H2 holds (DEOPT_DOMINATES or DEOPT_TIES), then SPIDER's central premise — that cumulative inheritance infrastructure pays for itself — is **FALSIFIED-IN-SETTING**.

---

## 4. Falsification Criteria

The experiment is **FALSIFIED-IN-SETTING for SPIDER's central premise** if:
- The deopt ratchet arm achieves amortized cost ≤ inherited-mechanism arm cost at matched correctness (success ≥ 0.95), OR
- The deopt ratchet arm achieves amortized cost ≤ cold-exploration arm cost at matched correctness

In either case, a no-memory architecture matches or beats the inheritance architecture, invalidating the premise that accumulation is necessary.

The experiment **SUPPORTS the inheritance premise** (DEOPT_LOSES) only if:
- Inherited-mechanism cost < deopt ratchet cost AND inherited-mechanism cost < cold cost, both at matched correctness

---

## 5. Substrate Specification

### 5.1 Required Substrate
- **Real, deterministic local HTTP service** using Python stdlib only (`http.server`, `socketserver`)
- **No Flask, FastAPI, BrowserGym, Playwright, Chromium, Docker, or LLM API keys**
- Parent handoff A-PROBE demonstrated stdlib HTTP GET/POST round trips work in this environment

### 5.2 Task Definition
- **Task family**: Synthetic but structurally realistic HTTP interaction tasks
- **Span definition**: A span = contiguous sequence of HTTP requests with identical (method, path, headers, body) signature across episodes for the same intent
- **Episode structure**: 50 episodes per arm, each episode = 1 task instance with ~15-25 spans
- **Intent space**: 5 distinct intents (e.g., "create_resource", "read_resource", "update_resource", "delete_resource", "list_resources")
- **Determinism source**: Server is purely deterministic; identical requests → identical responses

### 5.3 Availability as Observation
If any substrate component is unavailable:
- Record exact failure in `observations`
- Provide explicit smallest-next-action in `validity_notes`
- Do NOT treat as blocking falsifier or MEASUREMENT_INVALID
- Continue with available components

---

## 6. Arms (Three-Way Comparison)

### 6.1 Arm A: B-NO-MEMORY-DETERMINISTIC (Deopt Ratchet) — PRIMARY TEST ARM
**Mechanism:**
1. **Episode 1 (cold)**: Execute all spans via model oracle. Record every (state, action, next_state) tuple.
2. **Compile**: After each episode, identify spans that have been witnessed ≥2 times with identical signatures. Compile these into a local "deterministic cache" (executable Python functions).
3. **Deopt**: For spans not yet compiled, invoke model oracle (cost = 1 unit per span).
4. **Ratchet**: On subsequent episodes, execute compiled spans directly (cost = 1 unit per span, no model call). Deopt only novel spans to model. Recompile newly-witnessed-deterministic spans.
5. **Amortization**: Compile cost = 1 unit per unique span compiled (one-time). Model call cost = 1 unit per deopt. Execution cost = 1 unit per span.

**No inheritance infrastructure**: No registry, no distillation, no resolution, no freshness guards, no parameter induction. Pure compile+deopt.

### 6.2 Arm B: B-INHERITED-SPIDER (Inherited Mechanism) — INCUMBENT
**Mechanism:** Current `src/spider/kernel.py` SpiderKernel with:
- MechanismRegistry populated by `distill()` from Episode 1 observations
- `resolve()` for mechanism lookup with confidence gating (min_confidence=0.8)
- `verify()` for postcondition checking
- No parameter induction (kernel.distill does not induce parameters)
- Cost accounting: 1 unit per resolve+bind+verify+freshness check per span, plus 1 unit per span execution

**Registry construction**: After Episode 1, distill all successful observations into registry. Registry is static thereafter (no online learning).

### 6.3 Arm C: B-COLD-EXPLORATION (Inheritance Ablation) — MANDATORY NULL CONTROL
**Mechanism:** Same substrate, same tasks, **empty registry**.
- Every span resolved as UNKNOWN → deopt to model oracle
- No compilation, no caching, no inheritance
- Cost = 1 unit per model call per span per episode
- This is the absolute floor: if inheritance or deopt ratchet cannot beat this, they are negative-value

---

## 7. Measurement Definitions

### 7.1 Per-Span Witnessed Determinism Fraction
```
deterministic_spans = spans with identical (method, path, headers, body, response) across ≥2 episodes
total_spans = all spans executed across all episodes
determinism_fraction = deterministic_spans / total_spans
```

**Per-episode learning curve:** `determinism_fraction(episode_i) = deterministic_spans_up_to_i / total_spans_up_to_i`

### 7.2 Amortized End-to-End Cost
```
amortized_cost = (compile_cost_total + model_call_cost_total + execution_cost_total) / num_episodes
```
Where:
- `compile_cost_total` = number of unique spans compiled (one-time cost per span)
- `model_call_cost_total` = number of deopt invocations across all episodes
- `execution_cost_total` = total spans executed across all episodes (1 unit per span)

### 7.3 Correctness (Task Success)
A task succeeds if the final state matches the expected goal state.
**Matched correctness threshold:** success_rate ≥ 0.95 for an arm to be eligible for cost comparison.

### 7.4 Residual Novelty Dependence
For each span, track:
- `novelty_tier`: "never_seen" (first episode), "seen_once" (second episode), "seen_multiple" (third+ episode)
- Cost contribution by tier
- Determinism acquisition by tier

---

## 8. Controls

### 8.1 Positive Control: PC-WITNESSED-DETERMINISM
- **Task**: Synthetic task where ALL spans are identical across all 50 episodes
- **Expected**: determinism_fraction = 1.0 by Episode 2; model_calls = 0 after Episode 1; amortized_cost → execution_cost only
- **Pass criterion**: determinism_fraction ≥ 0.99 by Episode 10, model_calls_after_episode_1 = 0

### 8.2 Null Control: NC-ZERO-DETERMINISM
- **Task**: Synthetic task where NO spans repeat (unique path/query/body per episode)
- **Expected**: determinism_fraction = 0.0; model_calls = all_spans every episode; amortized_cost = cold_cost + compile_overhead
- **Pass criterion**: determinism_fraction ≤ 0.01, cost_ratio_vs_cold ≥ 1.0

### 8.3 Additional Controls (measured but not decision-gating)
- **PC-EXACT-REPLAY**: Task where inherited kernel has exact mechanism match (should achieve EXECUTABLE with zero novel decisions)
- **NC-EMPTY-REGISTRY**: Same as Arm C but verified that inherited kernel returns UNKNOWN for all spans

---

## 9. Sample Size and Power

- **Episodes per arm**: 50 (fixed, not adaptive)
- **Spans per episode**: ~20 (determined by task structure)
- **Total spans per arm**: ~1,000
- **Arms**: 3 primary + 2 controls = 5 arms × 50 episodes = 250 episodes total
- **Determinism fraction CI**: Wilson score interval at 95%
- **Cost comparison**: Non-parametric bootstrap (10,000 resamples) for cost difference CI

**Justification**: 50 episodes provides sufficient span observations for stable determinism fraction estimation (expected ~1000 spans) and learning curve resolution. This is a measurement experiment, not a hypothesis test with pre-specified effect size.

---

## 10. Decision Rule (Formal)

Let:
- `C_d` = amortized cost of deopt ratchet (Arm A)
- `C_i` = amortized cost of inherited SPIDER (Arm B)
- `C_c` = amortized cost of cold exploration (Arm C)
- `S_d, S_i, S_c` = success rates (must all be ≥ 0.95 for comparison)

**Outcome classification:**

| Condition | Outcome | Claim Consequence |
|-----------|---------|-------------------|
| `S_d ≥ 0.95 ∧ S_i ≥ 0.95 ∧ S_c ≥ 0.95 ∧ C_d < C_i ∧ C_d < C_c` | **DEOPT_DOMINATES** | FALSIFIED-IN-SETTING |
| `S_d ≥ 0.95 ∧ S_i ≥ 0.95 ∧ S_c ≥ 0.95 ∧ \|C_d - C_i\| ≤ 0.05·max(C_d,C_i) ∧ C_d < C_c ∧ C_i < C_c` | **DEOPT_TIES** | FALSIFIED-IN-SETTING |
| `S_d ≥ 0.95 ∧ S_i ≥ 0.95 ∧ S_c ≥ 0.95 ∧ (C_d ≥ C_i ∨ C_c ≤ min(C_d,C_i))` | **DEOPT_LOSES** | Inheritance premise survives |
| Any `S < 0.95` | **MATCHED_CORRECTNESS_FAILED** | INCONCLUSIVE — report which arm(s) failed |

**Tie threshold**: 5% relative difference (standard in systems performance comparison).

---

## 11. Reporting Requirements (Mandatory in result.json)

### 11.1 Primary Metrics
- `determinism_fraction`: overall, per-episode (learning curve), per-novelty-tier
- `amortized_cost`: per arm, with breakdown (compile, model, execution)
- `success_rate`: per arm
- `outcome`: one of {DEOPT_DOMINATES, DEOPT_TIES, DEOPT_LOSES, MATCHED_CORRECTNESS_FAILED}

### 11.2 Secondary Metrics
- `determinism_histogram`: distribution of per-span witness counts
- `compile_curve`: unique spans compiled vs episode
- `model_call_curve`: model calls per episode
- `residual_novelty_cost`: cost by novelty tier
- `span_signature_diversity`: number of unique span signatures

### 11.3 Controls
- `PC-WITNESSED-DETERMINISM`: pass/fail with metrics
- `NC-ZERO-DETERMINISM`: pass/fail with metrics

### 11.4 Validity Notes
- Infrastructure availability observations
- Any deviations from protocol
- Smallest-next-action for any unavailable component

### 11.5 Unresolved
- Questions the producer cannot settle from this run

---

## 12. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Substrate not truly deterministic | Verify server idempotency: identical request → identical response (test 100x) |
| Span definition arbitrary | Pre-define span as (method, path, normalized_headers, normalized_body, response_code, response_body_hash) |
| Model oracle not representative | Model oracle = deterministic function returning correct action for given state (simulated perfect model). Cost = 1 unit per call regardless of "model quality". |
| Compile cost not realistic | Compile cost = 1 unit per unique span (conservative; real compilation is cheaper than model call) |
| Inherited kernel not representative | Use actual `src/spider/kernel.py` with registry built from Episode 1. This is the shipped kernel. |
| Cold exploration not a fair baseline | Cold arm uses same model oracle, same substrate, same tasks — only difference is empty registry |
| Task not representative of Web | Explicitly acknowledged: this is a local deterministic substrate test. Generalization to live Web is a separate claim (C-CROSSSITE). This experiment tests the *architecture's economic logic*, not Web representativeness. |

---

## 13. Dependencies (from Director Mandate)

| Dependency | Owner | Status |
|------------|-------|--------|
| Intel: verified external numbers + strong-baseline spec for no-memory deterministic executor | Intel lane | This cycle's Intel mandate |
| Product: durable parameter induction in src/ for inherited-mechanism arm | Product lane | Required for non-vacuous comparison |
| Runtime: availability-as-observation discipline | Runtime lane | Required so missing asset ≠ zero information |

**Explicitly NOT depended upon:** BrowserGym, WebChoreArena, WebArena-Verified, any LLM key, docker, Chromium — all verified absent.

---

## 14. Consequences

### If DEOPT_DOMINATES or DEOPT_TIES (FALSIFIED-IN-SETTING):
- SPIDER's central premise (cumulative inheritance pays for itself) is falsified in this setting
- Architecture must pivot to non-inheriting compiled execution with deopt ratchet
- C-RESIDUAL-NOVELTY → REJECTED or SUPERSEDED
- Product kernel replaced by compile+deopt runtime
- Frontier lane has achieved its charter: "search outside the current solution basin for high-upside falsifiable mechanisms that could radically reduce agent exploration or change SPIDER's architecture"

### If DEOPT_LOSES:
- Inherited-mechanism execution remains justified on this substrate
- C-RESIDUAL-NOVELTY remains HYPOTHESIS/EXPERIMENTAL
- Next experiment: test hybrid architecture (compile deterministic spans + inherit residual mechanisms)
- The deopt ratchet becomes a validated strong baseline for future inheritance experiments

### If MATCHED_CORRECTNESS_FAILED:
- INCONCLUSIVE — report which arm failed correctness
- Debug and re-run with corrected implementation
- Do not weaken decision rule

---

## 15. Code Locations (for EXECUTE)

- **Substrate**: `research/frontier/substrate_deterministic_http.py` (to be created)
- **Arms**: `research/frontier/arms/` directory (to be created)
  - `deopt_ratchet.py` — Arm A implementation
  - `inherited_spider.py` — Arm B wrapper around `src/spider/kernel.py`
  - `cold_exploration.py` — Arm C implementation
- **Measurement**: `research/frontier/measure.py` — determinism, cost, success tracking
- **Main experiment**: `research/frontier/run_experiment_EXP_FRONTIER_36249071934.py`

All code stdlib-only, no external dependencies.

---

## 16. Freeze Checklist (before EXECUTE)

- [ ] spec.json written and matches this prereg.md
- [ ] prereg.md frozen (this document)
- [ ] freeze.json created by deterministic freezer (hashes request.json, spec.json, prereg.md)
- [ ] No outcome data inspected
- [ ] All controls pre-declared
- [ ] Decision rule fully specified with no free parameters
- [ ] Substrate verified available (A-PROBE replicated)

---

**End of Preregistration**

This preregistration is frozen. EXECUTE must implement exactly this design. Any deviation requires a new experiment with a new Director mandate.