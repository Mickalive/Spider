# EXP-PRODUCT-36129169543 — Preregistration (Product PIVOT C-PRODUCT-ECON — Instrument + Break-Even)

**Lane:** product  
**Claims:** `C-PRODUCT-ECON` (primary, binding Director mandate PIVOT with `cognitive_reset=true`, `SUPERSEDE` disposition)  
**Director Mandate:** `research/experiments/EXP-PRODUCT-36129169543/request.json` → `director_mandate`  
**Parent Handoff:** `EXP-PRODUCT-36095578013` (sha `c598732958acd88943a0eb81baa6225e22545af924dd3b431aff04d0e37613c2`, disposition `SUPERSEDE` per `AGENTS.md` — continuity evidence preserved, mandate binding)  
**Registry:** `research/claims/registry.json` sha `3511a788` — `C-PRODUCT-ECON` `HYPOTHESIS` (next_gate: end-to-end amortized economics on real agents) owner `product,graph`

---

## 1. Director Mandate (Binding)

> **Action:** PIVOT | **Claim:** C-PRODUCT-ECON | **Cognitive Reset:** true | **Disposition:** SUPERSEDE
>
> **Strategic Question:** "What does SPIDER's honest end-to-end accounting need in order to become decidable, and what is the break-even reuse count on the work that can actually be measured today?"
>
> **Three-Part Deliverable:**
>
> **Part A:** Freeze and unit-test an end-to-end evaluation harness that, from a task manifest and a pluggable policy, executes the full arm set — namely SPIDER inheritance with freshness gating and localized repair, B-COLD, B-INSTRUCTIONS, B-RAG with k=5, and a deterministic compiled executor — under identical model, tools and budget, with per-trajectory hard-reset integer counters for resolution, binding, verification, freshness, repair, browser steps, requests and latency, family-stratified trajectory-grouped bootstrap and block-permutation confidence intervals, and a fail-closed arm gate that marks any arm UNKNOWN, never surrogate-filled and never default-filled, when its prerequisite capability is absent.
>
> **Part B:** Dry-run every arm and every counter path against a deterministic scripted policy on the certified real distributed service, proving that the comparison, the counter accounting, the null controls and the abstention calibration execute end to end, and reporting explicitly that such a dry run establishes instrument correctness and NOT a scientific or product result.
>
> **Part C:** Compute and report the break-even reuse count at which inherited execution's amortized build and verification cost is repaid, from measured build, verification and serving work, and identify which single measured quantity most changes that number, since this is the quantity the whole product thesis turns on. Token-denominated economics are declared NOT_APPLICABLE and UNKNOWN until a policy-model credential exists. The packet already in PREFREEZE is superseded rather than executed, and no further full C-PRODUCT-ECON Pareto packet is to be frozen until Runtime's capability ledger reports a usable policy model and a certified browser.

---

## 2. Portfolio Context (from Director Assessment)

- SPIDER has 384 canonical experiments, 10 claims, and **ZERO claims at VALIDATED or PRODUCT_CORE**.
- Only audited VALIDATED scope: `C-MEAS-VALID` on bounded plain-HTTP localhost substrate (EXP-RUNTIME-36094450333, EXP-RUNTIME-36100549580).
- Everything else: HYPOTHESIS, MEASUREMENT_INVALID, or bounded synthetic SURVIVES/FALSIFIED ceiling.
- **Dominant failure mode shifted from wrong answers to no answer.**
- Recurring causes (recorded in Codex):
  1. Unlaunchable browser/CDP path (Runtime's frozen gate required private helper `playwright._impl._path_utils.get_executable_path`, absent in installed 1.63.0)
  2. Substrates never started (C-DELTA-REPAIR: `substrate_started=false`, `health_gate_pass=false`, `n_non304=0`; C-PARAM-INHERIT: B run made zero HTTP requests)
  3. Non-durable implementation (kernel working-tree sha differs from HEAD with `commit_made=false` because workflow forbids commits)
  4. Absent credentials (OPENAI_API_KEY absent, HF_TOKEN absent, GHCR browsergym 403)
- **Program cannot distinguish 'no effect' from 'no measurement' on any central claim.**
- Product has **twelve recent experiments on C-PRODUCT-ECON with twelve MEASUREMENT_INVALID outcomes**, traced to credential/substrate absence.
- A thirteenth structurally identical packet is close to certain to be invalid.
- **The decisive product number (break-even reuse count f*) has never been computed** — it is computable today from non-token work.

---

## 3. Inherited State from Parent Handoff (EXP-PRODUCT-36095578013)

### Established (Preserved)
- Contamination-free holdout RETAINED at MV1-MV2: rebuilt `webarena_verified_v2_tasks_192_36_rebuilt.json` sha `101e481d` verified 0/36 pool-level and 0/36 usage-level `value_set_A intersect B` empty STRICTLY on all 36 families, cross-family bigram Jaccard max 0.0 on 630 pairs <0.30 via `qcr_bank_manifest` sha `8c69804b` TAU0.30
- Single-node HS256 sticky substrate health-gated PASS at `n_non304>=360` stratified: `/tmp/spider-runtime/shared.db` WAL journal_mode wal single gunicorn 23.0.0 single-worker HS256 PyJWT 2.14.0, nginx 1.24.0 `$request_uri` consistent-hash sticky, `n_non304` 400 stratified ep-a 200 ep-b 200 (>=360/180)
- Correlated TTL 60s max-age ETag W/body_sha conditional probe discriminates health-gated: `n0 hit_rate 1.0` (150/150 304) at `n==0`, `n0.25 accuracy 1.0` (75 fresh 75 stale) `false_accept 0.0`, token saving 0.40 (4500/7500) >=0.30 vs full-fetch, seeded-42 random contrast 0.5933 delta 0.4067 >0.10 vs 0.53 random required
- Kernel dot-regex functionally PASS 5/5 EXECUTABLE confidence>=0.80 wrong-family UNKNOWN (working-tree sha `d926279d`)
- PC3 MockEnv calibration non-vacuous PASS per MV10: AUROC true 0.8714 vs shuffled null 0.4681, precision 0.9491 >=0.80, forced wrong-accept 0.1607 in [0.10,0.60], confidence_std 0.4543 >0.05, UNKNOWN_precision 0.9837 >=0.85, ECE 0.10696 <=0.15
- Honest per-trajectory-reset economics ceiling on rebuilt holdout (diagnostic): SPIDER f10 1981.09 vs COLD 5992.71 saving 0.6694 CI[0.652,0.687] — but SPIDER/RAG ratio 1.5064 CI[1.48,1.53] >0.85 FAIL at f10
- QCR orthogonality and toolchain pins retained

### Rejected (Preserved)
- Canonical 192/36 fallback census sha `391e8f6c` REJECTED as contamination-free holdout (18/36 pool and usage overlap)
- `per_hit` metric-design REJECTED bounded to file-proxy only (does not supersede `M_total` Pareto)
- NC1 shuffled null as deterministic file-proxy honest sum counters REJECTED as valid claim-level null (deterministic coupling `reused=max(0,L-n_novel*2)`)
- No rejection of C-PRODUCT-ECON `M_total` f10 honest economics on health-gated single-node + BrowserGym substrate — MEASUREMENT_INVALID bounded to infrastructure, not scientific falsification

### Unknown (Preserved)
- Whether GHCR authorization for `ghcr.io/servicenow/browsergym:0.14.3` + playwright 1.63.0 + OPENAI_API_KEY can restore BrowserGym path
- Whether committing kernel dot-regex `d926279d` to HEAD durable can be achieved
- Whether breaking NC1 deterministic counter coupling on real BrowserGym trajectories can achieve validity gates
- Whether honest `M_total` f10 saving>=25% vs COLD and ratio<=0.85 vs RAG holds — ceiling diagnostic passes but ratio fails on synthetic counters
- Whether per_hit supersession formally retires falsified per_hit
- Whether ST-WebAgentBench CuP safety non-inferior holds on live BrowserGym
- Whether Hard258 heterogeneous census should be vendored
- Whether P-SPIDER success margin>=0.12 vs baselines holds on real gpt-4o-mini trajectories

### Do Not Assume (Preserved — Critical)
- **MEASUREMENT_INVALID is infrastructure/measurement-gate failure NOT scientific falsification** — do not treat diagnostic ceiling saving 0.669 vs COLD or ratio 1.506 vs RAG or probe saving 0.40 or MockEnv AUROC 0.871 as SUPPORTS/FALSIFIED for C-PRODUCT-ECON
- Do not assume single-node substrate half PASS + correlated probe PASS implies Pareto dominance — probe/substrate diagnostics are substrate-level only
- Do not assume working-tree kernel patch `d926279d` is durable — at execute HEAD `8af66ccf` vs working-tree `d926279d`, `commit_made=false`
- Do not assume cross-family Jaccard max 0.0 implies holdout disjointness — Jaccard over A-pool first-slot bigram values not value_set intersection
- Do not assume GHCR/Docker/OPENAI health from toolchain pins — env_audit proves docker pull manifest unknown even after login, OPENAI_API_KEY ABSENT
- Do not assume PC3 MockEnv calibration AUROC 0.8714 transfers to real gpt-4o-mini trajectories
- Do not assume NC1 rho_shuffled -0.1367 band PASS means null valid — block_permutation p 0.0724 FAIL, rho_length pooled -0.287 per-stratum -0.084 to -0.657 all FAIL |0.20|
- Do not assume Stagehand file-proxy equals Docker BrowserGym validation
- Do not assume honest counter ratio >0.85 vs RAG proves RAG dominates generally
- Do not assume per_hit normalized <0.85 proves supersession — per_hit units incommensurable with M_total
- **Do not promote C-PRODUCT-ECON HYPOTHESIS to EXPERIMENTAL/VALIDATED/PRODUCT_CORE or claim amortized Pareto economics without live task success/accuracy and Director promote_to_product=true and audit PASS**

---

## 4. Experimental Design (Frozen at FREEZE)

### 4.1 Arm Set (Five Arms, Identical Model/Tools/Budget)

| Arm ID | Description | Inheritance Mechanism |
|--------|-------------|----------------------|
| `P-SPIDER` | SPIDER inheritance: freshness-gated 0.95/0.85 Jaccard 0.85 + deterministic localized repair (single-field re-bind) + correct-family reconstruction via kernel dot-regex `r'\$\{[A-Za-z_][A-Za-z0-9_\.]*\}'` + TTL 60s ETag W/body_sha conditional probe (10tok+30ms) + verified_state MEA auditor (softmax temp0.15+jitter UNKNOWN<0.80 or freshness<0.25 or probe stale) | Full mechanism inheritance with freshness gating + repair + audit |
| `B-COLD` | Cold exploration: no inherited knowledge, no retrieval, no instructions | None |
| `B-INSTRUCTIONS` | Static natural-language task instructions only | Instructions (no mechanism reuse) |
| `B-RAG-EMBED` | Embedding retrieval: TF-IDF TAU=0.30, QCR k=5, 200 token retrieval + 150ms verify cost model | RAG retrieval |
| `B-DETERMINISTIC-EXECUTOR` | **No-memory deterministic compiled executor** (Frontier's null against SPIDER's premise) — zero inheritance overhead, exact replay only | Deterministic compilation (no memory) |

**All arms share:** Deterministic scripted policy (for this experiment), per-trajectory hard reset, identical counter paths.

### 4.2 Counter Paths (Eight Integer Sum Counters, Per Trajectory)

1. `resolve` — mechanism resolution / lookup calls
2. `bind` — parameter binding operations
3. `verify` — verification / auditor calls
4. `freshness` — freshness probe / conditional fetch calls
5. `repair` — localized repair / re-bind operations
6. `browser_steps` — browser automation steps (Playwright actions)
7. `requests` — HTTP requests issued
8. `latency_ms` — wall-clock latency (milliseconds)

**No jitter, no n*3200 bijective proxy, no f*6.0 scaling.** Counters are honest integer sums reset per trajectory.

### 4.3 Substrate (Certified Real Distributed Service)

- Single-node HS256 sticky substrate: `/tmp/spider-runtime/shared.db` WAL, single gunicorn 23.0.0 worker, nginx 1.24.0 `$request_uri` consistent-hash sticky, HS256 PyJWT 2.14.0
- Health-gated: `n_non304>=360` stratified (180/endpoint × 2 endpoints), TN>=0.85
- ETag W/body_sha conditional probe: TTL 60s max-age, If-None-Match
- **No BrowserGym, no OPENAI_API_KEY, no playwright** — these are ABSENT and arms requiring them are gated UNKNOWN

### 4.4 Holdout & Stratification

- Contamination-free rebuilt 192/36 holdout: `webarena_verified_v2_tasks_192_36_rebuilt.json` sha `101e481d`
- 36 orthogonal alias families, `value_set_A intersect B` empty on ALL 36 families
- Cross-family bigram Jaccard max 0.0 on 630 pairs <0.30
- Family-stratified: L=8-14 family-specific constant within family, orthogonal to n within strata
- QCR bank: `qcr_bank_manifest` sha `8c69804b` TAU0.30 (TRAIN-only)

### 4.5 Statistical Rigor

- **Bootstrap:** Family-stratified trajectory-grouped B=5000
- **Block Permutation:** Family-stratified trajectory-grouped B=5000
- **Per-Stratum Gates:** `|rho_shuffled|<0.20`, block_permutation p>=0.20, `|rho_length|<0.20`
- **Confidence Intervals:** Wilson 95% for rates, trajectory-grouped bootstrap for ratios/rho/ECE/AUROC
- **Fail-Closed Gate:** Any arm whose prerequisite capability is absent → marked UNKNOWN (never surrogate-filled, never default-filled)

---

## 5. Decision Rules (Frozen)

### Part A: Harness Build & Unit Test
**PASS** iff:
- All 5 arms implemented with identical counter interface
- All 8 counter paths increment per trajectory under deterministic scripted policy
- Fail-closed UNKNOWN gate implemented and tested (unit test verifies gate fires for missing BrowserGym/credentials)
- Unit tests cover each arm + each counter + each gate
- Zero surrogate fills, zero default fills in unit tests

### Part B: Dry-Run on Certified Substrate
**PASS** iff:
- Deterministic scripted policy executes on certified distributed substrate (single-node HS256 sticky, health-gated)
- All 5 arms complete execution end-to-end
- All 8 counters recorded per trajectory for all arms
- Family-stratified B=5000 bootstrap + B=5000 block-permutation CIs compute without error
- UNKNOWN gates fire correctly for BrowserGym/credentials (arms marked UNKNOWN, not surrogate-filled)
- Zero crashes, zero surrogate fills, zero default fills
- **Result.json explicitly states:** "instrument correctness ONLY — not a scientific or product result"

### Part C: Break-Even Reuse Count f*
**PASS** iff:
- f* computed from measured non-token work ONLY:
  - Build cost: mechanism distillation + registry construction (measured in dry-run)
  - Verification cost: auditor + freshness probe (measured in dry-run)
  - Serving cost: lookup + bind + conditional fetch (measured in dry-run)
- Formula: `f* = (build_cost + verification_cost) / (serving_cost_cold - serving_cost_inherited)`
- Single measured quantity most changing f* identified via sensitivity analysis (one-at-a-time ±10% on each input)
- Token economics explicitly declared NOT_APPLICABLE and UNKNOWN

### Overall Experiment Status
| Part A | Part B | Part C | Overall Status | Outcome |
|--------|--------|--------|----------------|---------|
| PASS | PASS | PASS | COMPLETE | SUPPORTS (instrument decidable, f* computable) |
| FAIL | — | — | COMPLETE | FALSIFIES (specific instrument gap) |
| — | FAIL | — | COMPLETE | FALSIFIES (substrate integration gap) |
| — | — | FAIL | COMPLETE | FALSIFIES (breakeven computation gap) |
| Infrastructure failure | — | — | MEASUREMENT_INVALID | NOT_APPLICABLE (not scientific falsification) |

---

## 6. Positive Consequence (All Parts PASS)

1. **Instrument Deliverable:** Product obtains a frozen, unit-tested, dry-run-verified end-to-end accounting instrument. The next unblocking event (credential/substrate) converts into a run, not an infrastructure cycle.
2. **Decisive Number:** Break-even reuse count f* and its sensitivity are known — the quantity the entire product thesis turns on.
3. **Claim Advancement:** C-PRODUCT-ECON advances from HYPOTHESIS toward EXPERIMENTAL **on instrument readiness** (not economics result).
4. **No PRODUCT_CORE Promotion:** This is an instrument deliverable, not an economics result. Promotion requires separate Director verdict with audit PASS on live economics.
5. **Supersession Maintained:** The full Pareto packet (EXP-PRODUCT-36095578013) remains superseded. No further full C-PRODUCT-ECON Pareto packet frozen until Runtime capability ledger reports usable policy model and certified browser.

---

## 7. Negative Consequence (Any Part FAILS Validly)

1. **Specific Failure Diagnosis:** Which arm, which counter, which gate, which substrate dependency failed.
2. **Minimal Fix Identified:** Smallest change to unblock that component.
3. **Claim State:** C-PRODUCT-ECON remains HYPOTHESIS with instrument gap documented.
4. **No Pareto Retry:** Product lane does NOT retry full Pareto — Director mandate explicitly supersedes it.
5. **Next Cycle:** Either retries the failed instrument component or PARKS product economics pending Runtime capability ledger.

---

## 8. Validity Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| Deterministic scripted policy ≠ real LLM policy | Explicitly declared: this is INSTRUMENT validation only. Real LLM economics require credential (declared NOT_APPLICABLE/UNKNOWN). |
| Counter costs on scripted policy ≠ real costs | Measured non-token work (build/verify/serve) is substrate-bound, not policy-bound. Sensitivity analysis identifies which measured quantity matters most. |
| f* sensitivity to unmeasured token costs | Token costs explicitly excluded. f* computed from measurable non-token work only. Token f*_token declared UNKNOWN. |
| Single-node substrate ≠ distributed | Director gates distributed n>=800 behind single-node PASS. This experiment validates single-node instrument. |
| Kernel patch `d926279d` not committed to HEAD | Unit tests run against working-tree kernel. Dry-run uses working-tree. Durability is separate Runtime deliverable. |

---

## 9. Dependencies (from Director Mandate)

1. **Runtime capability ledger** and one-command distributed-substrate bring-up contract (single-node HS256 sticky certified)
2. **Graph C-FRESHNESS false-accept gate** (validated in EXP-PRODUCT-36095578013: correlated probe saving>=30% accuracy>=0.90 delta>10% vs random)
3. **Policy-model credential** (currently absent, outside SPIDER's control — blocks token dimension only, declared NOT_APPLICABLE)

---

## 10. Expected Information Gain

**HIGH — Decisive and Gating.** This is the smallest high-information experiment that can change a product decision:
- Twelve consecutive MEASUREMENT_INVALID C-PRODUCT-ECON packets failed chasing Pareto on absent substrate.
- The break-even reuse count f* (amortization denominator) has **never been computed** — it is the number the entire product thesis turns on.
- This experiment computes f* from measurable non-token work **today**, without any unavailable credentials.
- A valid negative (instrument gap found) is still decisive — it tells exactly what must be fixed before any economics measurement can be valid.
- Token economics correctly declared NOT_APPLICABLE/UNKNOWN avoids the credential trap that wasted 12 cycles.

---

## 11. Explicit Non-Goals (Do Not Assumptions Enforced)

- ❌ No token-denominated economics (NOT_APPLICABLE/UNKNOWN until credential exists)
- ❌ No BrowserGym / gpt-4o-mini / playwright execution (arms gated UNKNOWN)
- ❌ No Pareto dominance claims (M_total_f10 vs RAG/Stagehand/DSM/SGDR)
- ❌ No success margin / accuracy / safety CuP claims (require live BrowserGym)
- ❌ No rho_proxy_real / rho_novelty / calibration claims on real LLM (require credentials)
- ❌ No PRODUCT_CORE promotion (requires separate Director verdict + audit on live economics)
- ❌ No distributed n>=800 authorization (gated behind single-node PASS per Director)
- ❌ No f=100 Pareto claims (gated behind f=10 on live substrate)

---

## 12. Artifact Specification

**Primary Outputs (DESIGN → FREEZE → EXECUTE):**
- `spec.json` (this frozen specification)
- `prereg.md` (this frozen preregistration)
- `freeze.json` (deterministic hash of request+spec+prereg)

**EXECUTE Outputs:**
- `result.json` — with `status` ∈ {COMPLETE, BLOCKED, MEASUREMENT_INVALID}, `outcome` ∈ {SUPPORTS, FALSIFIES, MIXED, INCONCLUSIVE}, `metrics` (counter values, f*, sensitivity), `controls` (PC-INSTRUMENT-CORRECTNESS, NC-SHUFFLED-FAMILY-STRATIFIED), `artifacts` (harness code, unit test results, dry-run logs, breakeven computation), `observations`, `validity_notes`, `unresolved`
- `report.md` — bounded interpretation of measurements
- `provenance.json` — commits, environment, substrate certification

---

**FROZEN AT FREEZE.** No modifications after `freeze.json` exists. EXECUTE executes exactly this design.