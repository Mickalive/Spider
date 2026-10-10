# Preregistration: EXP-RUNTIME-37999040476

## Lane: runtime
## Claim: C-MEAS-VALID (Measurement substrate is intervention-valid)
## Experiment ID: EXP-RUNTIME-37999040476
## Director mandate: action=PIVOT, claim=C-MEAS-VALID (request.json `director_mandate`)
## Parent handoff disposition: SUPERSEDE

---

## 0. Inheritance (from the exact parent handoff)

This section preserves the four-way distinction of `research/experiments/EXP-RUNTIME-37973247935/handoff.json` (sha256 `984049809ebf393e805f59c9b8d083caf2ebfc387348079b06ccacbe41b8928e`). It is inherited state, not an agenda. The binding direction is the Director mandate in `request.json`.

### established (do not re-measure; may be cited at exactly this ceiling)
- C-MEAS-VALID is VALIDATED at the parent audit claim_ceiling (EXP-RUNTIME-36293257855): the composite oracle (length-framed SHA-256 WAL-byte vector + SQL logical projection + stable-header response fingerprint) maintains arm-constrained discrimination across the author/measurer and transport boundaries simultaneously, but **only against interventions performed through the fixture's own controlled endpoint**.
- Authorship separation exists as durable separable components: `intervention_surface.py` (ground-truth provider) and `oracle_scorer.py` (detector), sharing only constants-only `shared_config.py`.
- Real-browser transport with writes is proven: 120/120 episodes via the public Playwright API, real `page.click` as the only write mechanism.
- The one-command fail-closed capability contract (`bringup.py` + per-experiment `bringup_contract.json`) executes and passes; readiness floors met.
- The out-of-surface transfer question (EXP-RUNTIME-37973247935) remains UNTESTED in either direction (MEASUREMENT_INVALID due to fingerprint volatility and capture-stability gate mis-specification).

### rejected (do not revive as explanations)
- "The oracle only discriminates because the same author wrote the surface and the detector" — separate modules, no cross-imports, scorer receives no arm label.
- "Browser writes cannot run here" — 120/120 episodes ran through the canonical Chromium.
- "The out-of-surface oracle repair is the critical path" — the Director audit classifies it as 'OPEN but no longer the unique critical path' and it does not gate the benchmark; the actually-blocking task-bank question is unasked.
- "A mandatory-discovery deterministic REST certificate suffices" — EXP-PRODUCT-37989728440 and EXP-PRODUCT-37982016598 recorded the bounded substrate-class negative: cold and retrieval both sit at 1.0 ceiling at novelty >= 0.5 on that class.

### unknown (carried explicitly into this design)
- Whether a credential-free **browser** substrate on live sites with asymmetric discovery can achieve a non-degenerate task bank (cold < 0.95, retrieval < 0.95 at high novelty).
- Whether the parameterized treatment carrier (Product lane) is structurally executable on this substrate.
- Whether honest per-task economic counters (http_requests, retrieval_calls, verification_calls, repair_attempts) can be collected for all three arms.
- Whether any downstream lane will preregister the four-arm benchmark once readiness condition (2) is certified.

### do_not_assume (dangerous non-conclusions preserved)
- Do not assume the deterministic REST class result (cold=1.0, retrieval=1.0) transfers to browser-based live sites.
- Do not assume the out-of-surface oracle repair is required before this substrate work; the Director explicitly PIVOTed away from it.
- Do not assume a non-degenerate task bank exists without arithmetic certification.
- Do not assume the treatment carrier will work without a structural liveness check before freeze.
- Do not treat latency_ms/1000 or model calls as Runtime substrate counters; those are Product-lane economics.
- Do not schedule a durability re-experiment for the oracle; the PIVOT makes this substrate the priority.

### Director mandate disposition
`parent_handoff_disposition = SUPERSEDE`. The mandate's strategic question is reproduced in Section 1 and converted into a falsifiable substrate certification experiment. The previous handoff's `next_question` (oracle fingerprint repair) is advisory continuity state only and does not authorize this experiment. Agent priors recorded in `request.json.director_mandate.agent_priors_used` are treated as priors, not SPIDER evidence.

---

## 1. Strategic Question (binding, from the Director mandate)

> Can Runtime build and measurement-validly certify a credential-free execution substrate whose task bank is NON-DEGENERATE — i.e. cold re-derivation and a retrieval-shaped comparator are demonstrably below the success ceiling (e.g. < 0.95) at high residual novelty, with a real treatment/comparator behavioural distinction and honest per-task counters (http_requests, retrieval_calls, verification_calls, repair_attempts, excluding latency_ms/1000) — certified ARITHMETICALLY BEFORE freeze, so that readiness condition (2) holds before any four-arm C-LLM-INHERIT / C-RESIDUAL-NOVELTY benchmark is funded?

> Not another mandatory-discovery deterministic REST certificate: a substrate engineered for **asymmetric discovery** where one-time session/resource/schema discovery is real work that a parameterized treatment can amortize.

This experiment certifies the **substrate readiness gate (condition 2)**. It does not run the four-arm benchmark; it proves the substrate *can* support one.

---

## 2. Hypothesis

A credential-free browser substrate operating on live sites with asymmetric discovery structure can be constructed such that:

- **H1 (dynamic range).** The task bank admits a novelty-stratified partition where at high residual novelty (novelty_fraction >= 0.5) both the cold re-derivation baseline (B-COLD-RE-DERIVE) and the retrieval-shaped baseline (B-RETRIEVAL-SHAPED) have arithmetic accept regions with success rate point < 0.95 AND two-sided 95% Wilson lower bound < 0.90 at the planned per-task n.
- **H2 (treatment liveness).** The parameterized mechanism carrier interface (provided by Product lane per readiness condition 1) is structurally executable on this substrate: a minimal treatment execution on a low-novelty task succeeds (5/5) with valid bound_action, verification_pass, and per-task counters.
- **H3 (counter fidelity).** The substrate produces honest per-task economic counters for all three arms (cold, retrieval, treatment) on at least one task: http_requests, retrieval_calls (0 for cold, >=1 for retrieval/treatment), verification_calls, repair_attempts.
- **H4 (task bank non-degeneracy).** The certified task bank contains >= 10 tasks in the high-novelty stratum (novelty_fraction >= 0.5) and >= 5 tasks in the low-novelty stratum (novelty_fraction < 0.2).

This is a **bounded substrate readiness certification**, not a product promotion. Runtime may not set PRODUCT_CORE/SHIPPED.

---

## 3. Falsifier

Any of the following is an explicit falsification of the substrate readiness hypothesis:

1. The arithmetic dynamic-range certification (computed in DESIGN, pure arithmetic with no outcome measurements) fails to show both B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED below the success ceiling at high novelty (point < 0.95 AND Wilson_lo < 0.90 at novelty_fraction >= 0.5).
2. The treatment interface cannot be shown executable (treatment liveness fails: < 5/5 on low-novelty tasks) before freeze.
3. The per-task counters cannot be produced for all three arms on at least one task.
4. The task bank novelty stratification is degenerate (high_novelty_tasks < 10 OR low_novelty_tasks < 5).
5. The substrate bring-up or capability ledger fails (required scopes: CAP-CHROMIUM-LAUNCH, CAP-LIVE-SITE-REACHABILITY, CAP-TASK-BANK-LOADER).

Infrastructure or substrate failure maps to `INCONCLUSIVE` or `MEASUREMENT_INVALID` per decision_rule, not a scientific negative. The arithmetic certification in DESIGN ensures the decision rule is reachable before any episode runs.

---

## 4. Baselines (frozen reference, not re-measured as scientific question)

### B-COLD-RE-DERIVE
**Cold re-derivation baseline:** For each task, a fresh browser context executes the task from scratch with no prior knowledge, no retrieved fragments, no parameterized mechanism. The agent must discover the site structure, locate the target resources, understand the interaction schema, and complete the task. Measured per-task success (binary) and economic counters (http_requests, verification_calls, repair_attempts; retrieval_calls = 0 by definition).

### B-RETRIEVAL-SHAPED
**Retrieval-shaped baseline:** For each task, a semantic retrieval system (embedding-based over prior successful trajectories in the same task family) returns the top-k trajectory fragments; the agent executes the retrieved fragments with parameter binding for the current task instance. This is the 'strong retrieval/RAG over prior trajectories' baseline required by Graph experiment requirements (SPIDER_MASTER_PROMPT.md section 13). Measured per-task success and economic counters (http_requests, retrieval_calls, verification_calls, repair_attempts). The retrieval index is built from trajectories on OTHER tasks in the same family (leave-one-task-out), so it tests genuine generalization, not memorization.

**Prior evidence on deterministic REST class:** EXP-PRODUCT-37989728440 and EXP-PRODUCT-37982016598 recorded cold=1.0 and retrieval=1.0 at novelty>=0.5. This experiment uses a live-site browser substrate where discovery is asymmetric work — the prior result is a substrate-class negative, not a general ceiling.

---

## 5. Task Bank Construction

### 5.1 Candidate Credential-Free Live Sites
Sites must be: (a) accessible without auth/API keys/cookies, (b) stable enough for repeat measurement, (c) have discoverable structure requiring navigation/search/pagination. Final list fixed in this prereg:

| Site | Base URL | Task Family Types Supported |
|------|----------|----------------------------|
| Public APIs Directory | https://api.publicapis.org | search_and_extract, filter_by_category |
| Books to Scrape | https://books.toscrape.com | paginate_and_collect, filter_by_rating |
| Quotes to Scrape | https://quotes.toscrape.com | search_and_extract, paginate_and_collect |
| HTTPBin (for schema discovery) | https://httpbin.org | schema_discovery_and_call |
| JSONPlaceholder | https://jsonplaceholder.typicode.com | filter_and_extract, paginate_and_collect |

**Reachability requirement:** >= 3 of 5 sites must respond 200 to a HEAD/GET probe at bring-up (CAP-LIVE-SITE-REACHABILITY). Unreachable sites are dropped from the task bank; the bank is re-certified arithmetically after site filtering.

### 5.2 Task Families and Novelty Stratification
Each family defines a **semantic transformation type**. Task instances within a family differ in **target resource identifiers** (search query, category, filter values, page ranges).

| Family | Transformation | Site | Parameter Space | High-Novelty Condition |
|--------|----------------|------|-----------------|------------------------|
| F1-search-api | Search API directory, extract first result matching category | api.publicapis.org | category ∈ {Development, Photography, Finance, ...} | New category not in retrieval index |
| F2-paginate-books | Paginate through all pages, collect titles matching rating | books.toscrape.com | rating ∈ {One, Two, Three, Four, Five} | New rating value not in retrieval index |
| F3-search-quotes | Search quotes by tag, extract author/text | quotes.toscrape.com | tag ∈ {love, life, humor, ...} | New tag not in retrieval index |
| F4-schema-httpbin | Discover HTTPBin endpoint schema, make valid call | httpbin.org | endpoint ∈ {/get, /post, /put, /delete, /uuid, ...} | New endpoint not in retrieval index |
| F5-filter-jsonplaceholder | Filter posts/comments by userId, extract fields | jsonplaceholder.typicode.com | userId ∈ {1..10}, resource ∈ {posts, comments} | New userId/resource combo not in retrieval index |

**Novelty_fraction definition:** For a task instance, `novelty_fraction = 1 - (reused_actions / total_actions)` where `reused_actions` are actions whose (selector, action_type, target_url_pattern) tuple matches a retrieved fragment or parameterized mechanism from the same family (leave-one-task-out). Computed from execution traces.

**High-novelty stratum:** novelty_fraction >= 0.5 (discovery-heavy: new category/rating/tag/endpoint requires fresh navigation/schema discovery).
**Low-novelty stratum:** novelty_fraction < 0.2 (near-replay: same category/rating/tag/endpoint as a retrieved trajectory).

### 5.3 Task Bank Size Certification (Arithmetic, DESIGN)
- Planned: 5 families × 5 instances = 25 tasks.
- Expected high-novelty: ~15 (3 per family, leave-one-out on 5 instances).
- Expected low-novelty: ~10 (2 per family).
- Certified arithmetically in `A-TASK-BANK-CERTIFICATE.json` before freeze: actual counts after site reachability filtering.

---

## 6. Treatment Interface Contract (Product Lane Dependency)

**Readiness condition 1 (Product lane):** The parameterized mechanism carrier must implement the following interface:

```python
# research/runtime/treatment_interface.py (defined by Product, imported by Runtime)
class TreatmentCarrier:
    def resolve(self, task_signature: TaskSignature) -> Optional[BoundMechanism]:
        """Resolve a parameterized mechanism for the task signature. Returns None if no mechanism applies."""
        ...

    def execute(self, bound_mechanism: BoundMechanism, context: BrowserContext) -> ExecutionResult:
        """Execute the bound mechanism in the given browser context."""
        ...

    def verify(self, execution_result: ExecutionResult, task_signature: TaskSignature) -> VerificationResult:
        """Verify the execution result against the task goal."""
        ...
```

**Structural liveness check (this experiment, PC-TREATMENT-LIVENESS):** Before freeze, Runtime imports the Product carrier and executes it on 5 low-novelty tasks (novelty_fraction < 0.2). All 5 must produce `bound_action_valid=true`, `verification_pass=true`, and per-task counters. This is a **structural executability test**, not a discrimination test.

**No treatment discrimination is measured in this experiment.** The four-arm benchmark (cold vs retrieval vs treatment vs instructions) is a Product-lane experiment that requires this substrate certification as a precondition.

---

## 7. Experimental Design

### 7.1 Arithmetic Dynamic-Range Certification (DESIGN, zero runtime cost)
Computed in DESIGN using the frozen Wilson formula (z=1.959963984540054) and planned per-task n.

| Stratum | Baseline | Planned n | Accept Region (k) | Point at Boundary | Wilson_lo at Boundary | Non-degenerate? |
|---------|----------|-----------|-------------------|-------------------|----------------------|-----------------|
| High novelty (>=0.5) | B-COLD-RE-DERIVE | 15 | k <= 14 | 0.933 | 0.702 | Yes |
| High novelty (>=0.5) | B-RETRIEVAL-SHAPED | 15 | k <= 14 | 0.933 | 0.702 | Yes |
| Low novelty (<0.2) | PC-TREATMENT-LIVENESS | 5 | k = 5 | 1.0 | 0.566 | Yes |

**Certificate:** `A-DYNAMIC-RANGE-CERTIFICATE.json` materializes the full k=0..n table for each baseline/stratum combination. The accept region is non-empty and non-trivial: a genuinely imperfect instrument (success rate ~0.93) passes. This is the pre-freeze attainability certificate demanded by the mandate.

### 7.2 Substrate Bring-Up and Capability Ledger
One-command fail-closed: `python -m research.runtime.bringup --contract research/runtime/bringup_contract.json`
Required scopes (fail-closed):
- CAP-CHROMIUM-LAUNCH: Chromium executable at canonical path, sha256 matches, Playwright 1.63.0 launches successfully.
- CAP-LIVE-SITE-REACHABILITY: >= 3 of 5 candidate sites respond 200 to HEAD/GET within 10s.
- CAP-TASK-BANK-LOADER: `task_bank.json` loads, validates against schema, produces >= 10 high-novelty and >= 5 low-novelty tasks.

Advisory UNAVAILABLE (NOT on critical path): BrowserGym, AgentLab, policy-model credentials, GHCR.

### 7.3 Execution Matrix (EXECUTE)
| Arm | Tasks | Procedure | Per-Task Counters |
|-----|-------|-----------|-------------------|
| B-COLD-RE-DERIVE | All high-novelty tasks (>=10) + 5 low-novelty | Fresh context -> navigate -> discover -> execute -> verify | http_requests, retrieval_calls=0, verification_calls, repair_attempts |
| B-RETRIEVAL-SHAPED | All high-novelty tasks (>=10) + 5 low-novelty | Embed task -> retrieve top-k -> bind -> execute -> verify | http_requests, retrieval_calls>=1, verification_calls, repair_attempts |
| TREATMENT (liveness only) | 5 low-novelty tasks | Resolve -> bind -> execute -> verify | http_requests, retrieval_calls>=1, verification_calls, repair_attempts |

**Total task executions:** ~35 (15 cold high + 15 retrieval high + 5 treatment low). No high-novelty treatment executions in this certification experiment.

### 7.4 Per-Task Counter Collection (Mandatory)
Collected for every task execution across all arms:

| Counter | Source | Notes |
|---------|--------|-------|
| http_requests | Browser network events (CDP `Network.requestWillBeSent`) | Count of HTTP requests issued during task execution |
| retrieval_calls | Retrieval module / treatment carrier | 0 for cold, >=1 for retrieval/treatment |
| verification_calls | Explicit verification steps after task completion | DOM assertions, schema validation, content checks |
| repair_attempts | Explicit recovery actions after verification failure | Max 3 per task; recorded as 0 if verification passes |

**Excluded from Runtime substrate:** latency_ms, token counts, model calls, LLM latency — these are Product-lane economics.

### 7.5 Retrieval Baseline Implementation
- Index: Embedding-based (sentence-transformers/all-MiniLM-L6-v2, local, no API calls) over task signatures + successful trajectories from OTHER tasks in the same family (leave-one-task-out).
- Top-k: k=3 fragments retrieved.
- Parameter binding: Slot-filling by semantic matching (task parameter values -> fragment parameter slots).
- Execution: Retrieved fragments executed in fresh browser context with bound parameters.
- This is a **strong retrieval baseline** per Graph requirements (SPIDER_MASTER_PROMPT.md section 13), not a weak strawman.

---

## 8. Components and Architecture

### 8.1 Credential-Free Substrate — `research/runtime/credential_free_substrate.py` (NEW)
- Browser automation: Playwright 1.63.0 public API, canonical Chromium, viewport 1280x720.
- Fresh context per task for cold baseline; shared context only within evaluation block for retrieval/treatment.
- Real network egress to live sites; no mocking, no synthetic responses.
- Navigation timeout: 30s. Action timeout: 10s. Max 3 repair attempts per task.
- Per-task counter collection integrated into execution loop.

### 8.2 Task Bank Loader — `research/runtime/task_bank_loader.py` (NEW)
- Loads `task_bank.json` (experiment-local, frozen at freeze.json).
- Validates against JSON schema (family, instances, novelty_stratification).
- Computes novelty_fraction for each instance given a retrieval index (leave-one-out).
- Produces stratified task lists for execution.

### 8.3 Per-Task Counters — `research/runtime/per_task_counters.py` (NEW)
- Defines counter schema, collection hooks, and serialization.
- Integrated into substrate execution loop.
- Outputs `artifacts/A-PER-TASK-COUNTERS.jsonl` (one record per task execution).

### 8.4 Retrieval Baseline — `research/experiments/EXP-RUNTIME-37999040476/retrieval_baseline.py` (NEW)
- Implements B-RETRIEVAL-SHAPED procedure.
- Local embedding model (sentence-transformers/all-MiniLM-L6-v2).
- Leave-one-task-out index construction per family.
- Top-k retrieval + parameter binding + execution.

### 8.5 Treatment Interface — `research/runtime/treatment_interface.py` (NEW, interface only)
- Abstract base class defining the Product carrier contract.
- Product lane provides concrete implementation at runtime (imported dynamically).
- This experiment only tests structural liveness (PC-TREATMENT-LIVENESS).

### 8.6 Shared Constants — `research/runtime/shared_config.py` (EXTENDED)
- Extended with new constants: `EXPERIMENT_ID`, `WILSON_Z`, `DYNAMIC_RANGE_THRESHOLDS`, `TASK_BANK_SCHEMA`.
- Does NOT mutate parent oracle constants (oracle_scorer.py, intervention_surface.py unchanged).

**Authorship separation:** Substrate, task bank, counters, retrieval baseline are Runtime-owned. Treatment carrier is Product-owned (imported via interface). No cross-imports of detection/scoring logic.

---

## 9. Artifacts to Produce

| Path | Role | Description |
|------|------|-------------|
| `artifacts/A-TASK-BANK-CERTIFICATE.json` | derived | Task bank stratification counts, site reachability, schema validation |
| `artifacts/A-DYNAMIC-RANGE-CERTIFICATE.json` | derived | Full k=0..n Wilson tables for each baseline/stratum; accept regions |
| `artifacts/A-PER-TASK-COUNTERS.jsonl` | raw | Per-task counters for every execution (arm, task_id, counters) |
| `artifacts/A-TREATMENT-LIVENESS.jsonl` | raw | 5 low-novelty treatment executions with bound_action, verification, counters |
| `artifacts/A-CAPABILITY-LEDGER.json` | derived | Fail-closed capability ledger with all required scopes PASS |
| `artifacts/A-BRINGUP-CONTRACT.json` | derived | Bring-up contract execution record |
| `artifacts/B-PLAYWRIGHT-CAPABILITY.json` | raw | Browser launch receipt (path, sha256, version, viewport) |
| `artifacts/C-SITE-REACHABILITY.json` | raw | HEAD/GET probe results for all 5 candidate sites |

`result.json`, `report.md`, `provenance.json` produced by EXECUTE with exact required top-level shapes.

---

## 10. Pre-freeze Attainability and Control-Liveness Certificate (mandatory)

### 10.1 Arithmetic Attainability (DESIGN, pure arithmetic)
Frozen z = 1.959963984540054; two-sided 95% Wilson score interval.

| Arm class | n | accept region | point at boundary | Wilson_lo at boundary | non-degenerate |
|-----------|---|---------------|-------------------|----------------------|----------------|
| High-novelty cold | 15 | k <= 14 | 0.933 | 0.702 | yes |
| High-novelty retrieval | 15 | k <= 14 | 0.933 | 0.702 | yes |
| Low-novelty treatment liveness | 5 | k = 5 | 1.0 | 0.566 | yes |

**Reference:** At n=15, the dual-threshold accept region (point < 0.95 AND Wilson_lo < 0.90) is k <= 14. k=14 gives point=0.933, Wilson_lo=0.702 — passes both thresholds. k=13 gives point=0.867, Wilson_lo=0.621 — comfortably passes. k=15 fails the point threshold (1.0 >= 0.95). The accept region is non-empty and non-trivial (a genuinely imperfect instrument at ~93% success passes). This certificate must be reproduced as `A-DYNAMIC-RANGE-CERTIFICATE.json` before freeze.

### 10.2 Structural Control-Liveness Checks (must all pass before freeze)
Run mechanically; **never** invoke outcome measurements:

| id | check |
|----|-------|
| `CL-SITE-REACHABILITY` | >= 3 of 5 candidate sites respond 200 to HEAD/GET |
| `CL-TASK-BANK-LOAD` | `task_bank.json` loads, validates, produces >= 10 high-novelty + >= 5 low-novelty tasks |
| `CL-CHROMIUM-LAUNCH` | Canonical Chromium launches, CDP accessible, version matches frozen sha256 |
| `CL-COUNTER-COLLECTION` | Per-task counter hooks fire and serialize for a dummy task execution |
| `CL-RETRIEVAL-INDEX` | Retrieval index builds for a family with leave-one-out, returns >=1 fragment |
| `CL-TREATMENT-IMPORT` | Product treatment carrier imports via interface, `resolve()` callable |

**Failure discipline:** A failed check blocks freeze and makes the experiment `MEASUREMENT_INVALID`, never a scientific negative.

---

## 11. Decision Rule (Frozen)

| Outcome | Condition |
|---------|-----------|
| **SUPPORTS** | Dynamic-range certificate: both cold and retrieval have point < 0.95 AND Wilson_lo < 0.90 at high novelty (n=15). Task bank certificate: high_novelty >= 10, low_novelty >= 5. Treatment liveness: 5/5 on low-novelty. Per-task counters produced for all 3 arms on >=1 task. Capability ledger all required scopes PASS. Pre-freeze preflights passed. |
| **MIXED** | Dynamic-range passes for exactly one of {cold, retrieval} at high novelty; OR task bank non-degenerate but treatment liveness partial; OR counters for only 2 of 3 arms. Interpretation localizes ceiling-bound component. |
| **FALSIFIES** | Dynamic-range fails for BOTH cold and retrieval at high novelty (point >= 0.95 OR Wilson_lo >= 0.90); OR task bank degenerate (high_novelty < 10); OR treatment liveness 0/5; OR counters missing for all arms. `status=COMPLETE`. |
| **INCONCLUSIVE** | Infrastructure/substrate failure (browser launch, site unreachable, task bank load failure, capability ledger required scope FAIL). Smallest unblocking action recorded. |
| **MEASUREMENT_INVALID** | Synthetic fallback used; capability ledger FAIL not recorded as INCONCLUSIVE; treatment liveness not tested before freeze; counters not implemented; dynamic-range certificate not computed in DESIGN (post-hoc arithmetic). |

---

## 12. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Live site instability (flaky responses, layout changes) | Site reachability verified at bring-up; task bank re-certified after filtering; per-task counters record http_requests/repair_attempts as evidence of instability |
| Site blocks automated access (403, CAPTCHA, rate limit) | Credential-free sites chosen for automation tolerance; CAP-LIVE-SITE-REACHABILITY requires 200; failures reduce bank size but trigger INCONCLUSIVE if < 3 sites |
| Retrieval baseline too weak/strong | Strong retrieval baseline per Graph requirements (embedding + leave-one-out + parameter binding); not a strawman. Novelty_fraction measured from execution traces, not assumed. |
| Treatment carrier not available at EXECUTE | Readiness condition 1 is a Director mandate dependency. If unavailable, experiment is INCONCLUSIVE with unblocking action "Product lane delivers treatment carrier". |
| Novelty_fraction measurement circular | Computed from execution traces (reused_actions = actions matching retrieved fragment/mechanism by selector+action_type+url_pattern), not from task definition. |
| Counter collection affects behavior | Counters are passive observers (CDP network events, explicit verification/repair calls); no additional network requests or delays injected. |
| Single-run certification not generalizable | This certifies *this substrate on this task bank* as a readiness gate. Generalization requires replication (Product benchmark). |
| Arithmetic certification ≠ empirical result | The dynamic-range certificate is a DESIGN-time reachability proof. EXECUTE measures empirical success rates. Both must align for SUPPORTS. |

---

## 13. Dependencies and Preconditions

1. The Director mandate in `request.json` (`action=PIVOT`, `claim_id=C-MEAS-VALID`) is the binding direction.
2. The frozen parent packet `research/experiments/EXP-RUNTIME-37973247935/` is immutable and cited, not re-measured.
3. Validated components at recorded hashes (unchanged): `oracle_scorer.py` `7a30ff63...`, `intervention_surface.py` `10be3dcb...`, `shared_config.py` `6840f540...`, `bringup.py` `d6cc744b...`.
4. Product lane delivers parameterized treatment carrier implementing `TreatmentCarrier` interface (readiness condition 1).
5. Canonical Chromium re-verified at run time: sha256 `8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e`, Playwright 1.63.0 public API only.
6. Runtime code roots: `research/harness`, `research/runtime`, `substrates`.
7. Physics owns statistical-contract certification; Runtime must not duplicate it.
8. Downstream consumer: Product lane four-arm C-LLM-INHERIT / C-RESIDUAL-NOVELTY benchmark (blocked until this certifies).

---

## 14. Non-Goals (Explicitly Out of Scope)

- Running the four-arm C-LLM-INHERIT / C-RESIDUAL-NOVELTY benchmark (Product lane, requires this certification).
- Production OAuth/OIDC, TLS, CDN, load balancer, HTTP/2, multi-host, authenticated sites.
- BrowserGym, AgentLab, policy-model integration, LLM inheritance, cross-site transfer.
- Oracle fingerprint repair (SUPERSEDED by Director PIVOT).
- Durability re-experiment for oracle components.
- Any product promotion or claim-registry edit by this packet; the DIRECTOR owns verdicts.
- Generalizing the substrate certification beyond the declared sites and task families.

---

## 15. Seed and Determinism

- Master seed derived from `experiment_id` 37999040476.
- Task execution order: `random.Random(master_seed).shuffle(...)`, archived before task 1.
- Per-task RNG: `random.Random(master_seed + task_index)`.
- Retrieval embedding model: deterministic (sentence-transformers, fixed seed).
- All seeds recorded in `artifacts/A-SEEDED-ORDER.json` and `provenance.json`.

---

## 16. Freeze Checklist (before `freeze.json`)

- [ ] `research/runtime/task_bank_loader.py` exists, loads/validates `task_bank.json` against schema.
- [ ] `research/runtime/credential_free_substrate.py` exists, implements browser automation + counter collection.
- [ ] `research/runtime/per_task_counters.py` exists, defines counter schema and serialization.
- [ ] `research/experiments/EXP-RUNTIME-37999040476/task_bank.json` exists, defines 5 families, 25 instances, novelty stratification.
- [ ] `research/experiments/EXP-RUNTIME-37999040476/retrieval_baseline.py` exists, implements B-RETRIEVAL-SHAPED.
- [ ] `research/runtime/treatment_interface.py` exists, defines abstract `TreatmentCarrier` interface.
- [ ] `research/runtime/bringup_contract.json` declares required scopes (CAP-CHROMIUM-LAUNCH, CAP-LIVE-SITE-REACHABILITY, CAP-TASK-BANK-LOADER) and frozen readiness floors.
- [ ] `A-DYNAMIC-RANGE-CERTIFICATE.json` reproduced (accept regions: high-novelty cold/retrieval k<=14/15; low-novelty treatment k=5/5).
- [ ] All `CL-*` control-liveness checks pass mechanically without outcome measurements.
- [ ] Chromium sha256 matches and Playwright pinned to 1.63.0.
- [ ] No synthetic fallback code paths in substrate or baselines.
- [ ] `spec.json` and this `prereg.md` hashed into `freeze.json` before any task runs.

---

## 17. Cheap Pre-freeze Satisfiability Probes (design_contract_version >= 2)

The following probes are run in DESIGN (this phase) to verify freeze_eligibility. They are **non-outcome-bearing** and use only arithmetic, static analysis, and structural checks:

1. **Dynamic-range arithmetic probe:** Compute Wilson accept regions for planned n=15 (high novelty) and n=5 (low novelty) using frozen z. Verify accept regions non-empty and non-trivial (k=14 passes both thresholds: point=0.933, Wilson_lo=0.702). → Confirms `decision_rule_reachability` and `control_sensitivity`.
2. **Task bank schema probe:** Load `task_bank.json`, validate against schema, compute novelty stratification counts. Verify high_novelty >= 10, low_novelty >= 5. → Confirms `measurement_prerequisites` and `baseline_identifiability` (novelty_fraction computable).
3. **Site reachability probe:** HEAD/GET probe to all 5 candidate sites (timeout 10s). Verify >= 3 respond 200. → Confirms `measurement_prerequisites` (CAP-LIVE-SITE-REACHABILITY).
4. **Chromium launch probe:** Launch canonical Chromium via Playwright 1.63.0, verify CDP accessible, sha256 matches. → Confirms `measurement_prerequisites` (CAP-CHROMIUM-LAUNCH).
5. **Treatment interface probe:** Import Product carrier (if available in DESIGN context) or verify interface definition exists and is importable. Verify `resolve()`, `execute()`, `verify()` methods present. → Confirms `treatment_liveness` (structural).
6. **Counter collection probe:** Run dummy task execution through substrate, verify all 4 counters (http_requests, retrieval_calls, verification_calls, repair_attempts) serialize correctly. → Confirms `measurement_prerequisites` and `freeze_artifacts_bound`.
7. **Mutable artifact hash probe:** Compute sha256 of all 6 files in `freeze_artifacts` list. Verify they exist and are stable. → Confirms `freeze_artifacts_bound`.

**All probes must PASS before freeze.json is created.** A failed probe is a DESIGN failure, not a scientific result.

---

## 18. End of Preregistration

This preregistration is frozen upon creation of `freeze.json`. No changes to hypothesis, task bank, baselines, treatment interface, thresholds, decision rule or validity criteria are permitted after freeze. Any post-freeze change requires a new experiment ID. Operational retries of a frozen experiment must resume from the last valid checkpoint and must not rewrite frozen scientific inputs.