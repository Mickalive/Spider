# Spider product pilot — runnable boundaries (11 October 2026)

**Status: engineering pilot, NOT validated comparative economics or production release.**

## What is implemented

- A real local HTTP portal with two independent families (`invoices`, `shipments`), several IDs and a click -> search -> open sequence.
- An optional Browser Use LLM agent runner that can navigate Chromium to solve the portal task. Requires an explicit user-provided model credential and opt-in to model charges. Nothing paid is invoked by CI, tests or defaults.
- A real deterministic Playwright Chromium workflow is the `CACHE` arm (a compiled selector cache / workflow baseline, **not** Stagehand itself).
- An opt-in Spider adapter that consumes **a manually seeded, fixture-known, read-only HTTP mechanism**. It does *not* discover or distill a parameterized mechanism by observing Browser Use. When no applicable mechanism exists, it uses the same Browser Use agent.
- An independent server-side truth oracle, temporary registry, read-only URL authorization, error accounting and raw trace output.
- A strict four-arm descriptive scorer, plus a fifth CACHE competitor from an actual compiled Playwright browser workflow. A Stagehand v4 server-cache comparison is **still required independently** before a claim of superiority over Stagehand.
- All raw pilot traces have `cost_accounting_complete=false` and `cost_usd=null`. They are rejected by the economic scorer until actual fully loaded costs (tokens, browser, retrieval, verification, writing, storage and amortization) are measured. Never replace null with zero.

## Local use

Python >=3.11. From repo root:

```bash
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests -v
python -m pip install browser-use playwright
uvx browser-use install
python -m playwright install chromium
```

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

The seeded Spider path intentionally bypasses LLM inference, but **the seed was hand-written from fixture implementation**. That is a technical integration test, not proof that a first independent browser agent could have learned it. Do not claim end-to-end inheritance economics from this seed.

## Genuine launch gates

1. Verify that the same real model can complete unseen, multi-step tasks unaided, with auditable terminal result and usage.
2. Implement and independently audit `distill_parameterized` from agent/network traces, including reusing a newly seen ID, refusal on out-of-support IDs, and scope/freshness guards. Promote through the preexisting research Product lane gate; do not hand-copy experimental code into main.
3. Build an independently scored task bank with non-ceiling cold/retrieval performance, two distinct families, page drift, and a blinded oracle.
4. Collect matched `COLD`, `INSTRUCTIONS`, `RETRIEVAL`, `SPIDER` and real `CACHE` runs (Stagehand v4 caching / comparably strong compiled workflow). Same model, tools, budgets and task distribution, randomized arm order.
5. Produce exact amortized total cost per verified *safe success*. The scorer refuses incomplete accounting and requires the fifth arm when `--require-cache` is set.

**Go/no-go proposal, not a current result:** at least 20% lower complete cost per verified safe success than the strongest comparator, with non-inferior safety/success and a reproduced second-family effect. If this is not achieved, narrow the product claim rather than build more architecture.

## Known scope limits

No paid provider keys are committed. No real LLM/browser run or Stagehand cached result has been certified in CI. The local task bank is a controlled **real HTTP** fixture, not an independent external site; its easy direct API makes it unsuitable for proving competitive cost superiority. The final experiment must include practical Web workloads where a flat cache or compiled flow is already a serious comparator.

## Research factory

Continue the one cumulative scientific Codex, not a new 3.0 epoch. Research asks decision-changing questions and can retain Graph, fractal/multiscale compression and bounded exploratory Physics. Product consumes only validated results and runs on a separate cadence. The shipped code remains behind the independent Product promotion gate.
