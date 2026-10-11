# Spider — second implementation audit (11 October 2026)

**Type:** engineering/strategy decision note, **not canonical scientific evidence**. One cumulative Codex remains on main; do not ingest this note as an independently audited scientific result.

## Verified GitHub state

- Main includes PR #40 (free-only model allowlist and a lane circuit breaker) and PR #41 (two separately steered loops; one Codex; attrition diagnostics). Main CI succeeded on both merges.
- PR #42 is draft and isolated from main scientific claims. The repository CI and real Playwright Chromium smoke have succeeded on the functional browser-trace learner; no paid LLM evaluation has run in CI.
- At last canonical snapshot, historical artifacts 1,401; Research 2.0 audited experiment packets 436. No new validated promotion is inferred from raw workflow execution status.

## What was wrong with the first product pilot

1. Each trial opened a fresh ephemeral Web port and a **temporary, discarded** Spider registry. That prevented genuine cross-task inherited-memory testing.
2. Its Spider "advantage" came only from **hand-entered knowledge of the fixture API**, while the cold agent used the UI — a fatal advantage confound if represented as discovery.
3. There was no train/evaluation split for the small four-task fixture.
4. Its usage output read `history.usage`, but Browser Use defaults to `calculate_cost=False`, so observed model-cost fields could remain unpopulated even when tokens were spent.
5. The descriptive economic scorer accepted unitemized totals and could be handed arbitrarily low numbers.
6. The competitive comparator was deterministic Playwright, **not** Stagehand's native cache. It remained misleading to infer a market-leading advantage.

## Corrections on the product PR

- Browser trace compiler `src/spider/pilot_learning.py`: two **independent recorded Chromium detail-route observations** with distinct record IDs, exact same local origin, constrained path/query, page answer and matching record reference. It refuses arbitrary cross-origin paths, malformed IDs, mismatched content and additional query fields.
- `scripts/train_pilot_memory.py`: two real Chromium explorations per family produce durable parameterized relative GET procedures. Record training cost in a manifest; never hide the onboarding work.
- `src/spider/pilot_portal.py` + `scripts/run_pilot_matrix.py`: disjoint train/eval identifiers and controlled reproducible paired five-arm plans. Held-out replay can run in a new server session/port.
- `run_real_agent_pilot.py`: opt-in persistent scoped registry and read-only exact-path authorization; independent page-reference + answer verification; explicit Browser Use token/cost instrumentation, model identities and no automatic provider charges.
- `scripts/smoke_compiled_browser.py` and Playwright workflow: actual Chromium learn/compile/persist/replay cycle over both families and never-observed IDs, no provider credentials.
- `score_product_benchmark.py`: componentized model, browser, retrieval, verification, memory, amortized training, repair and other; cost components must reconcile with total; manually preseeded Spider rows cannot establish economic value. The score is still labelled descriptive, not independently audited.

## Current achievements (exact bounded scope)

1. A **scripted browser** successfully completes two families of real HTTP/Chromium UI tasks.
2. Two previously observed details per family can be compiled into a scope-limited reusable relative URL procedure.
3. A later Spider run can perform a **single read-only HTTP GET** to extract the correct result for an ID not seen during training, even with a fresh local server port.
4. On a missing or non-executable mechanism, Browser Use remains an available but **not yet live-validated** fallback.
5. Repo CI and actual Chromium smoke verify the engineering path; they do not prove Spider beats a competent cached workflow.

## Still NOT demonstrated

- A real LLM browser agent completing the fixture or recording the exact training traces. The current source agent is the *scripted Playwright* baseline, not an autonomous navigator.
- General-purpose learning, safely compiled arbitrary HTTP actions, graph-fractal memory, incremental repair under actual drift, authenticated/session use, or across-site transfer.
- Measured total marginal cost per safe success, including tracing/onboarding/amortization, or Stagehand-native cache behavior.
- Commercial superiority: a simple deterministic Playwright script and a flat cache may already be comparably cheap on this particular toy substrate.
- Product scientific promotion. The prototype must stay out of main until the independent Product promotion gate is satisfied.

## Recommended resource allocation / next gates

**Gate A (highest value):** demonstrate one Browser Use agent *actually succeeding* on a held-out interactive task, produce instrumented navigation/network evidence from that exact agent, compile a reusable procedure from its successful trace, and prove a second agent can inherit it. Do not replace the model with a scripted fixture for the claim.

**Gate B:** benchmark 3 variants on the same task distribution — Browser Use cold, strongest deterministic/cache baseline (Playwright and Stagehand-native cache) and Browser Use+Spider; keep matched model/tool budgets, failure costs, confidence bounds, and training amortization. Add separate instructions/retrieval controls.

**Gate C:** Introduce controlled page changes and two genuinely distinct task families. Verify safety, abstention, repair costs and false-accept rates. Only then ablate the *graph/fractal* representation against simpler procedural caches.

**Stop/pivot:** if Spider cannot reduce the fully loaded cost per independently verified safe task by the preregistered threshold versus the strongest practical baseline, stop layering research-derived architecture into the product. Physics and Frontier remain independent falsification-focused research lanes with spending and repeated-failure limits.

The current gain is **engineering readiness and truthful test design**, not verified savings.
