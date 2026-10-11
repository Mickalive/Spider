# Spider product pilot — runnable boundaries (11 October 2026)

**Status: engineering pilot, NOT validated comparative economics or production release.**

## What is implemented

- A real local HTTP portal with two independent families (`invoices`, `shipments`), several IDs and a click -> search -> open sequence.
- An optional Browser Use LLM agent runner that can navigate Chromium to solve the portal task. Requires an explicit user-provided model credential and opt-in to model charges. Nothing paid is invoked by CI, tests or defaults.
- A real deterministic Playwright Chromium workflow is the `CACHE` arm (a compiled selector cache / workflow baseline, **not** Stagehand itself).
- An opt-in Spider adapter that can consume **a persisted parameterized mechanism compiled from two observed Chromium browser trajectories**, only for this fixed local fixture schema. A separate manual-seed path is retained for negative controls. When no applicable mechanism exists, the same Browser Use agent is the fallback. This is **not** learning from an autonomous LLM browser agent or the production `distill_parameterized()`.
- An independent server-side truth oracle, optional **persistent** registry, read-only URL authorization, error accounting and raw trace output. Learning uses training identifiers disjoint from all evaluation identifiers.
- A strict four-arm descriptive scorer, plus a fifth CACHE competitor from an actual compiled Playwright browser workflow. A Stagehand v4 server-cache comparison is **still required independently** before a claim of superiority over Stagehand.
- All raw pilot traces have `cost_accounting_complete=false` and `cost_usd=null`. They are rejected by the economic scorer until fully loaded costs are priced **and** broken down into eight audited components (model, browser, retrieval, verification, memory read/write, amortized training, repair and other). Never replace null with zero.

## Local use

Python >=3.11. From repo root:

```bash
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests -v
python -m pip install browser-use playwright
uvx browser-use install
python -m playwright install chromium
```

First, exercise **real Chromium trace learning and held-out inheritance without using an LLM**:

```bash
PYTHONPATH=src python scripts/smoke_compiled_browser.py
PYTHONPATH=src python scripts/train_pilot_memory.py \
  --memory-path /tmp/spider-fixture-memory.jsonl \
  --manifest /tmp/spider-fixture-learning.json
PYTHONPATH=src python scripts/run_real_agent_pilot.py \
  --arm CACHE --family invoices --id A-303 \
  --output /tmp/spider-raw.jsonl
```

The CACHE baseline is a deterministic compiled Playwright workflow, not Stagehand's own cache. To replay an observed mechanism on a **previously unseen** identifier, run `run_real_agent_pilot.py --arm SPIDER --family invoices --id A-303 --memory-path /tmp/spider-fixture-memory.jsonl --allow-model-charges --output /tmp/spider-raw.jsonl`. The spending permission remains mandatory because a missing or invalidated mechanism may trigger the paid LLM fallback. A correctly trained fixture mechanism runs without invoking the model.

The manifest exposes the two browser discovery costs per family. It is **not** acceptable to divide a later task's near-zero model cost without including this discovery and validation expenditure. These traces and the scorer continue to reject a commercial win because provider token prices, full runtime costs, model reliability and Stagehand-native caching are not yet independently audited.

Generate a **matched, randomized five-arm plan without invoking any model or spending money**:

```bash
PYTHONPATH=src python scripts/run_pilot_matrix.py --output /tmp/spider-raw.jsonl
```

To actually execute its 20 task/arm combinations, add `--execute --allow-model-charges`, a provider key, and an explicit `--max-trials` cap. The generated `.plan.json` is retained. The optional `--seeded-fixture` arm is only a hand-built upper bound, not autonomous discovery. The resulting raw traces are intentionally rejected by the economic scorer until all cost components can be independently priced.

To use a real agent (not executed automatically by CI):

```bash
export GOOGLE_API_KEY="<your-user-provided-key>"
PYTHONPATH=src python scripts/run_real_agent_pilot.py --arm COLD --family invoices --id A-101 --provider google --allow-model-charges --output /tmp/spider-pilot.jsonl
PYTHONPATH=src python scripts/run_real_agent_pilot.py --arm SPIDER --family invoices --id A-202 --provider google --seeded-fixture --allow-model-charges --output /tmp/spider-pilot.jsonl
```

`--allow-model-charges` is mandatory even if a provider sometimes offers a free quota. The OpenCode research model fallback is a **different** mechanism and is constrained to documented-free candidates; this browser-agent example makes no free-model guarantee. Use account-level spending caps.

Manual seed remains only an explicit upper-bound control and is now rejected by the complete-cost scorer. The trace-compiled path genuinely extracts a parameterized **detail-page URL from two real deterministic Chromium runs**, persists it, and retrieves previously unseen IDs. It does **not** yet learn from an independent LLM navigator, nor show a cross-site transfer or a graph/fractal advantage. This separation is mandatory for honest benchmarking.

## Genuine launch gates

1. Verify the same real model on unseen, multi-step tasks unaided, using Browser Use `calculate_cost=True` and independent terminal correctness/safety. This model-capability test has not been run in CI.
2. Advance the fixture trace compiler to independent **LLM-agent-observed traces** and real-world guarded `distill_parameterized`; add URL/parameter scope, out-of-support refusal, drift and freshness. Promote through the preexisting research Product lane gate; do not hand-copy experimental code into main.
3. Build an independently scored task bank with non-ceiling cold/retrieval performance, two distinct families, page drift, and a blinded oracle.
4. Collect matched `COLD`, `INSTRUCTIONS`, `RETRIEVAL`, `SPIDER` and real `CACHE` runs (Stagehand v4 caching / comparably strong compiled workflow). Same model, tools, budgets and task distribution, randomized arm order.
5. Produce exact amortized total cost per verified *safe success*. The scorer refuses incomplete accounting and requires the fifth arm when `--require-cache` is set.

**Go/no-go proposal, not a current result:** at least 20% lower complete cost per verified safe success than the strongest comparator, with non-inferior safety/success and a reproduced second-family effect. If this is not achieved, narrow the product claim rather than build more architecture.

## Known scope limits

No paid provider keys are committed. No real LLM/browser run or Stagehand cached result has been certified in CI. The local task bank is a controlled **real HTTP** fixture, not an independent external site; its easy direct API makes it unsuitable for proving competitive cost superiority. The final experiment must include practical Web workloads where a flat cache or compiled flow is already a serious comparator.

## Research factory

Continue the one cumulative scientific Codex, not a new 3.0 epoch. Research asks decision-changing questions and can retain Graph, fractal/multiscale compression and bounded exploratory Physics. Product consumes only validated results and runs on a separate cadence. The shipped code remains behind the independent Product promotion gate.
