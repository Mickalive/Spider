# Preregistration: EXP-FRONTIER-36272394045

**Lane:** frontier
**Claim:** C-RESIDUAL-NOVELTY
**Director Mandate:** CONTINUE with cognitive_reset=true
**Parent Experiment:** EXP-FRONTIER-36249071934 (handoff SHA256: 4f733eefc581a3cfa4f927ef0b3c2a0abd672e5f4ff5eea05f78592fbc1d6877)

---

## 1. Scientific Question

On a verified-reachable deterministic stdlib HTTP substrate (no browser, no docker, no model key), the previous packet (EXP-FRONTIER-36249071934) established that a no-memory deopt ratchet beats always-deopting cold exploration by 33.4 abstract units/episode (CI95 [-34.0, -32.4]) at matched correctness across all five swept novelty rates. However, the inherited-mechanism arm was **not identified**: 0 of 1200 resolve calls returned EXECUTABLE, 0 mechanisms executed, C_i == C_c exactly. The decisive comparison against inheritance could not be run.

The **compilability boundary** was quantified and independently recomputed by audit:
- 0.5833 of span occurrences (700/1200) are witnessed-deterministic
- Only 0.6857 of those (480) are served from compiled replay = 0.40 of all occurrences
- The 220-occurrence loss splits exactly into three causes:
  - 100 occurrences: observable state key recurred but mapped to >1 correct action (observationally identical, goal-distinct)
  - 100 occurrences: observable state key never recurred (embedded episode-specific prior request)
  - 20 occurrences: witness-buildup (first two witnesses under 2-witness rule)

This experiment **stops measuring how often work repeats** and instead **measures what is epistemically visible to an executor**. We define D(s) = the correct next action of a span as a function of the executor's own observable state, and decompose the deopt ratchet's residual into three mutually exclusive classes:

| Class | Description | Closable by Goal Conditioning? | Requires Parameter Induction / Cross-Episode Memory? |
|-------|-------------|-------------------------------|------------------------------------------------------|
| (i) Merely-novel | Span's observable state is novel, but correct action is determined by goal/intent prefix alone | **YES** | No |
| (ii) Epistemically blocked | Byte-identical observable state requires DIFFERENT correct actions depending on goal | No | **YES** (only parameter induction or persistent cross-episode memory can bind) |
| (iii) Observation-absent | Correct action depends on a binding key (e.g., resource ID from prior response) NOT present in current observable state NOR in goal/intent prefix | No | **YES** (requires cross-episode memory or parameter induction from prior observation) |

We report the three shares across the pre-declared novelty grid {0.00, 0.25, 0.50, 0.75, 1.00}, with a planted-disambiguation positive control and a matched unique-states null, using the accepted no-memory deterministic deopt ratchet as the reference arm.

---

## 2. Hypothesis

The deopt ratchet's residual (the 60% of span occurrences not served from compiled replay) decomposes into **non-zero shares of epistemically blocked (class ii) and observation-absent (class iii) spans**. Goal conditioning alone will **not** saturate the reference arm's compiled-replay coverage (0.6857 of deterministic occurrences, 0.40 of all occurrences) at equal or lower amortized cost. The sum of shares (ii) + (iii) quantifies the **maximum headroom** any inheriting architecture could recover on this plan family.

---

## 3. Falsifier (Pre-declared, Two Independent Clauses)

**Clause 1 (Inheritance Niche Confirmed):** If `share_class_ii_epistemically_blocked == 0.0` (within measurement precision: CI95 upper bound < 0.01) at **ALL** novelty rates in {0.00, 0.25, 0.50, 0.75, 1.00}, then the ratchet's residual is **irreducibly binding** — there are no epistemically blocked spans. Inherited parameterization has a **real economic niche** on this substrate because parameter induction is the ONLY mechanism that can close class (ii) spans.

**Clause 2 (SPIDER Premise Falsified):** If the goal-conditioned no-memory arm reaches or exceeds the reference arm's measured compiled-replay coverage:
- `conditioned_compiled_replay_coverage_deterministic >= 0.6857` AND
- `conditioned_compiled_replay_coverage_all >= 0.40` AND
- `conditioned_amortized_cost <= 38.6` (reference deopt cost)

then **goal conditioning substitutes for inherited parameterization** and SPIDER's mechanism-accumulation premise is **falsified in this setting on identified, executable arms**.

**Outcome Mapping:**
- Clause 1 only → `FALSIFIES_INHERITANCE_NICHE` (inheritance has niche)
- Clause 2 only → `FALSIFIES_SPIDER_PREMISE` (goal conditioning substitutes)
- Both → `CONTRADICTORY` (investigate)
- Neither → `INCONCLUSIVE` (headroom > 0, goal conditioning does not saturate)

---

## 4. Substrate & Environment

- **Server:** Python stdlib `ThreadingHTTPServer` bound to `127.0.0.1`, stateless CRUD service
- **No:** Browser, Docker, Playwright, Chromium, BrowserGym, Flask, FastAPI, LLM credentials
- **Verified Reachable:** EXP-FRONTIER-36249071934 served 8400 real HTTP/1.1 keep-alive requests
- **Idempotency:** 8 distinct request shapes × 100 identical repeats = 800 round trips, each returning exactly one response-body hash and status code (destructive verbs exercised on success path)
- **Determinism:** Substrate is deterministic by construction; no auth, no rate limiting, no partial failure, no non-determinism

---

## 5. Span Definition (Atomic Unit)

- **Observable State:** `(world_store_snapshot, last_request_method, last_request_path)`
  - `world_store_snapshot`: JSON-serialized state of the in-memory key-value store
  - `last_request_method`: HTTP method of the immediately preceding request
  - `last_request_path`: HTTP path of the immediately preceding request
- **Correct Action:** `(method, path, body_template)` tuple
- **Span:** A single `(observable_state, correct_action)` pair within a work item
- **Span Key:** Hash of observable_state (used for compilation/deopt decisions in reference arm)

---

## 6. Task Generator & Episode Structure

**Base Generator:** `research/frontier/taskplan.py` (identical to EXP-FRONTIER-36249071934)
- 5 preregistered intents (fixed before any arm runs)
- 4 work items per episode
- 24 spans per episode (6 spans per work item)
- 50 episodes per novelty rate per arm

**Novelty Grid:** `{0.00, 0.25, 0.50, 0.75, 1.00}` (target_novelty_rate parameter)

**Extensions for This Experiment:**

| Mode | Parameter | Description |
|------|-----------|-------------|
| Reference (B-NO-MEMORY-DETERMINISTIC) | `goal_conditioning_mode=false`, standard novelty sweep | Deopt ratchet: 2-witness compilation, selective deopt on ambiguous keys |
| Treatment (B-NO-MEMORY-CONDITIONED) | `goal_conditioning_mode=true`, standard novelty sweep | No compilation, no parameter induction, no cross-episode memory. Goal/intent prefix provided at each decision. |
| Positive Control (PC-PLANTED-DISAMBIGUATION) | `planted_disambiguation_mode=true`, `target_novelty_rate=0.50` | Goal-distinct work items with byte-identical observable states. Binding key carried in goal prefix. |
| Null Control (NC-UNIQUE-STATES) | `unique_states_mode=true`, `target_novelty_rate=0.50` | Each span occurrence gets a unique observable state key by construction. Shares (ii) and (iii) must be exactly 0. |
| Class III Fraction | `class_iii_fraction=0.10` (declared, non-zero) | Fraction of spans whose binding key comes from a prior response NOT in current observable state nor goal. Ensures class (iii) > 0 by construction. |

---

## 7. Arms (Experimental Conditions)

### 7.1 B-NO-MEMORY-DETERMINISTIC (Reference Arm)
- **Algorithm:** Deopt ratchet from EXP-FRONTIER-36249071934 (`research/frontier/arms/deopt_ratchet.py`)
- **Compilation:** After 2 witnesses of same span key → compile to replay table
- **Deopt:** On encountering a span key that maps to >1 correct action → deopt to oracle for that occurrence only
- **Cost Model:** 1 unit per compile, 1 per deopt, 1 per span executed, +1 per-span machinery bundle for arms that resolve mechanisms (not applicable here)
- **Episodes:** 50 per novelty rate × 5 rates = 250 episodes
- **No Goal Conditioning:** Oracle receives only `(world_store, last_request)`

### 7.2 B-NO-MEMORY-CONDITIONED (Treatment Arm)
- **Algorithm:** No-memory executor with goal/intent conditioning prefix
- **No Compilation:** No replay table, no witness counting, no deopt logic
- **No Parameter Induction:** No parameter slots, no binding, no cross-episode memory
- **Input to Oracle:** `(world_store, last_request, goal_intent_prefix)` — the goal/intent string is prepended as a conditioning context
- **Cost Model:** 1 unit per model call (oracle invocation). No compile/deopt/machinery costs.
- **Episodes:** 50 per novelty rate × 5 rates = 250 episodes
- **Correctness:** Must achieve success_rate = 1.0 (matched with reference)

### 7.3 PC-PLANTED-DISAMBIGUATION (Positive Control)
- **Design:** Work items where 4 distinct goals present byte-identical observable states (e.g., empty store, last request GET /) but require 4 different correct actions
- **Binding Key:** Carried explicitly in the goal/intent prefix (e.g., "CREATE resource:A", "CREATE resource:B", "READ resource:A", "READ resource:B")
- **Expected Classification:** All such spans → Class (i) merely-novel (close with goal conditioning)
- **Shares (ii) and (iii):** Must be 0 by construction
- **Episodes:** 50 at fixed novelty_rate=0.50

### 7.4 NC-UNIQUE-STATES (Null Control)
- **Design:** Each span occurrence gets a unique observable state key by construction (e.g., append episode_id + step_id to world_store_snapshot)
- **Expected Classification:** All spans → Class (i) merely-novel (modulo witness-buildup)
- **Shares (ii) and (iii):** Must be exactly 0 by construction
- **Episodes:** 50 at fixed novelty_rate=0.50

---

## 8. Classification Protocol (Per Span Occurrence)

For each span occurrence in the **reference arm's execution trace** (the ground truth trace):

1. **Extract:** `(observable_state_key, correct_action, goal_intent, prior_response_binding_keys)`

2. **Class (iii) Observation-Absent Check:**
   - Does `correct_action` depend on a binding key (e.g., resource_id from a prior POST response)?
   - Is that binding key **ABSENT** from both:
     - Current `observable_state` (world_store + last_request), AND
     - Current `goal_intent` prefix?
   - If YES → Class (iii). **Stop.**

3. **Class (ii) Epistemically Blocked Check:**
   - Has this `observable_state_key` been seen before in the reference trace?
   - Did it map to a **DIFFERENT** `correct_action` on a prior occurrence?
   - If YES → Class (ii). **Stop.**

4. **Class (i) Merely-Novel:**
   - All remaining spans: observable state is either novel or recurs with same correct action
   - These are the spans that close with goal conditioning alone (or were compilable in reference)

**Verification:** The three classes are mutually exclusive and exhaustive. Every span occurrence gets exactly one label.

---

## 9. Primary Metrics (Per Novelty Rate, Per Arm)

| Metric | Symbol | Description | Reference Value (from parent) |
|--------|--------|-------------|-------------------------------|
| Share Class (i) | `σ₁` | Fraction of spans merely-novel | — |
| Share Class (ii) | `σ₂` | Fraction of spans epistemically blocked | — |
| Share Class (iii) | `σ₃` | Fraction of spans observation-absent | — |
| Max Headroom | `σ₂ + σ₃` | Maximum recoverable by any inheritance | — |
| Conditioned Coverage (deterministic) | `γ_det` | Fraction of deterministic spans served by conditioned arm | 0.6857 (reference) |
| Conditioned Coverage (all) | `γ_all` | Fraction of all spans served by conditioned arm | 0.40 (reference) |
| Conditioned Amortized Cost | `C_cond` | Abstract units/episode for conditioned arm | 38.6 (reference deopt) |
| Saturation Share (i) | `σ₁_sat` | Share (i) at which γ reaches reference level | — |

**Measurement Precision:** Wilson score intervals (95%) for proportions; paired bootstrap (5000 resamples, episode as unit) for cost differences.

---

## 10. Controls & Validity Checks

### 10.1 Positive Control (PC-PLANTED-DISAMBIGUATION)
- **Pass Criterion:** `σ₁ ≈ 1.0` (within CI), `σ₂ ≈ 0`, `σ₃ ≈ 0` for planted spans
- **Failure Meaning:** Goal conditioning cannot disambiguate even when binding key is in goal → implementation defect

### 10.2 Null Control (NC-UNIQUE-STATES)
- **Pass Criterion:** `σ₂ == 0` exactly, `σ₃ == 0` exactly (by construction)
- **Failure Meaning:** Classification logic defect (false positive on unique states)

### 10.3 Reference Arm Replication
- **Pass Criterion:** Reproduce parent's key numbers within measurement error:
  - Per-span witnessed determinism ≈ 0.5833
  - Compilable-given-deterministic ≈ 0.6857
  - Compiled share of all spans ≈ 0.40
  - Deopt amortized cost ≈ 38.6 vs cold 72.0
  - Compilability gap split: ~100 ambiguous, ~100 never-recur, ~20 witness-buildup

### 10.4 Substrate Idempotency
- 8 request shapes × 100 repeats → exactly 1 response hash and 1 status code per shape
- Verified before any arm runs

### 10.5 Correctness Invariance
- All arms must achieve `success_rate = 1.0` on all episodes
- Any arm with success < 1.0 → MEASUREMENT_INVALID

---

## 11. Sample Size & Power

- **Episodes per arm per novelty rate:** 50 (same as parent)
- **Total episodes:** 250 (reference) + 250 (conditioned) + 50 (PC) + 50 (NC) = 600
- **Total span occurrences:** 600 × 24 = 14,400 (plus sweep arms)
- **Paired Design:** Reference and conditioned arms run on **identical task instances** (same seeds, same episode structure) for direct per-episode cost pairing
- **Bootstrap:** 5000 resamples, episode as sampling unit (50 episodes per novelty rate)

**Power Consideration:** The parent packet achieved CI95 [-34.0, -32.4] on cost difference with 50 paired episodes. For proportion estimates (σ₂, σ₃), with n=1200 span occurrences per novelty rate, the standard error for a proportion near 0.1 is ~0.0086, giving CI95 width ~0.034 — sufficient to distinguish 0 from >0.05.

---

## 12. Analysis Plan (Frozen Before Execution)

1. **Run all arms** on identical task instances (seeded deterministically)
2. **Generate reference trace** (B-NO-MEMORY-DETERMINISTIC) with full span logging
3. **Classify every span occurrence** in reference trace using Protocol (Section 8)
4. **Run conditioned arm** (B-NO-MEMORY-CONDITIONED) on same instances, record which spans it resolves correctly on first encounter
5. **Compute shares** σ₁, σ₂, σ₃ per novelty rate (from reference trace classification)
6. **Compute conditioned coverage** γ_det, γ_all per novelty rate (from conditioned arm results vs reference trace)
7. **Compute conditioned cost** C_cond per novelty rate
8. **Run PC and NC** at novelty_rate=0.50, verify pass criteria
9. **Evaluate falsifier clauses:**
   - Clause 1: Is σ₂ CI95 upper bound < 0.01 at ALL 5 novelty rates?
   - Clause 2: Is γ_det ≥ 0.6857 AND γ_all ≥ 0.40 AND C_cond ≤ 38.6 at ANY novelty rate?
10. **Map to outcome** per Section 3

**No post-hoc analysis changes.** Any exploratory analysis will be clearly labeled as such in `report.md` and will not affect `result.json.outcome`.

---

## 13. Validity Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| Classification logic error | PC and NC controls directly test classification boundaries; reference trace classification is deterministic and auditable |
| Goal conditioning implementation leak (accidental memory) | Conditioned arm is stateless function: `action = f(obs, goal)` with no closure over prior episodes; unit tested |
| Substrate non-determinism | Verified idempotency pre-run; all arms on identical seeds |
| Novelty rate confound | Novelty rate is a task-generator parameter; same episodes used for reference and conditioned arms |
| Cost model mismatch | Abstract units defined identically to parent: 1 per oracle call; reference includes compile/deopt per parent spec |
| Positive control too easy | PC uses the EXACT failure mode from parent (4 goals, identical obs, different actions) |
| Null control not unique enough | Unique state keys constructed by appending episode/step IDs to world store snapshot |
| Class (iii) fraction not achieved | `class_iii_fraction=0.10` enforced by task generator; verified post-hoc |

---

## 14. Product Consequences (Bounded to This Experiment)

**If Clause 1 triggers (σ₂ = 0):**
- The 60% compilation gap is purely novelty (σ₁) + observation-absence (σ₃)
- No epistemically blocked spans exist → parameter induction is not needed for disambiguation
- Inheritance's economic niche is **confirmed** (it solves the σ₃ class which conditioning cannot)
- Product should invest in durable parameterized mechanism accumulation

**If Clause 2 triggers (goal conditioning saturates):**
- SPIDER's central mechanism-accumulation premise is **falsified** on this plan family
- Goal/intent conditioning alone achieves equal/better coverage at equal/lower cost
- No compiled memory, no parameter induction needed
- Product should pivot to non-inheriting compiled execution with semantic conditioning

**If Neither triggers (Inconclusive):**
- Headroom (σ₂ + σ₃) > 0 but goal conditioning does not saturate reference coverage
- Inheritance has a **bounded economic niche** of size (σ₂ + σ₃)
- Parameter induction or cross-episode memory required for that headroom
- Product should continue building parameterized mechanisms with quantified ceiling
- The sum (σ₂ + σ₃) becomes the maximum possible ROI for inheritance work on this substrate

---

## 15. Artifacts to Preserve (For Audit & Reproduction)

- Raw span traces: `artifacts/spans_<arm>.jsonl` (one line per span occurrence)
- Classification labels: `artifacts/classification_<arm>.jsonl`
- Episode-level cost ledgers: `artifacts/costs_<arm>.jsonl`
- Control verification: `artifacts/pc_verification.json`, `artifacts/nc_verification.json`
- Substrate idempotency check: `artifacts/substrate_idempotency.json`
- Per-novelty-rate summaries: `artifacts/summary_<novelty_rate>.json`
- Task generator config: `artifacts/task_generator_config.json`
- Git commit, Python version, random seeds: `provenance.json`

---

## 16. Dependencies & Preconditions

- **research/frontier/taskplan.py** (SHA256: 8875a05b54761f96a92cea8d3ec43bd6886347b5e04ef81d594d65d53f910816) — must exist and be unmodified from parent
- **research/frontier/arms/deopt_ratchet.py** (SHA256: 0c09a680a0dbde2488fdb9cf94632a9d70af135ab6351a7912401840063f3aee) — reference arm implementation
- **research/frontier/arms/common.py** (SHA256: d9ceeb6a6bfee1bac7fcd8b65f9407dd616c171c52cfccc654b20c9f75185af6) — shared oracle, cost model
- **research/frontier/substrate_deterministic_http.py** (SHA256: e0e2e9b525bc9ad80628b30f2cf9d565ade8ce726134069e0497109208993790) — HTTP server
- Python 3.12+ stdlib only (no external deps)

---

## 17. No-Go Conditions (Result in MEASUREMENT_INVALID)

1. Substrate idempotency check fails
2. Any arm achieves success_rate < 1.0
3. PC-PLANTED-DISAMBIGUATION fails (σ₁ < 0.95 or σ₂ > 0.01 or σ₃ > 0.01)
4. NC-UNIQUE-STATES fails (σ₂ > 0 or σ₃ > 0)
5. Reference arm cannot replicate parent's key numbers within 2× parent's CI width
6. Infrastructure unavailable (server won't start, port conflict, etc.)

**Infrastructure failure ≠ scientific falsification.** If a no-go condition triggers, `result.json.status = MEASUREMENT_INVALID` with exact failure recorded.

---

## 18. Commitment

This preregistration is **frozen** before any outcome data is inspected. The `freeze.json` will hash this document, `spec.json`, and `request.json`. No changes to hypothesis, falsifier, metrics, controls, or decision rule after freeze.

**Date:** 2026-09-26
**Author:** Frontier DESIGN agent (fresh context)
**Binding Packet:** research/experiments/EXP-FRONTIER-36272394045/