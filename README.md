# SPIDER — Research 2.0 / Product Convergence

SPIDER is a model-agnostic external knowledge layer for Web agents:

> The first agent explores. The next ones inherit.

Research 2.0 deliberately keeps two goals alive at once:

1. build a usable execution-inheritance product core;
2. continue broad falsification-first research into mechanisms that could radically reduce how agents search, explore, verify and repair Web work.

The pre-2.0 scientific record is frozen at `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md`. It is never rewritten by Research 2.0.

Active architecture: `SPIDER_ARCHITECTURE_RESEARCH2.md`.

## Active lanes

Six independent lanes run without synchronizing on one another:

- `graph` — cumulative operational inheritance and mechanism reuse;
- `physics` — Web-dynamics hypotheses beyond memory/similarity;
- `runtime` — valid measurement, writable substrates, capture and execution;
- `product` — the shipping kernel, SDK surface and product economics;
- `intel` — datasets, baselines, reproductions and external evidence tied to live claims;
- `frontier` — high-upside orthogonal hypotheses and new research directions.

Each lane can advance while every other lane is slow, failed, auditing or idle.

## Product core

The first stable surface is:

`observe -> distill -> resolve -> execute -> verify -> repair/UNKNOWN`

The implementation under `src/spider/` is intentionally conservative. It is a substrate for validated capabilities, not a claim that the final SPIDER architecture is already known.

## Scientific memory

Every claim-bearing run uses one standard experiment packet:

`request.json + spec.json + prereg.md + freeze.json + result.json + report.md + provenance.json + audit.json + verdict.json + handoff.json`

The active Codex compiler ingests finalized packets from all lane branches into `SPIDER_CODEX.md`. Negative, blocked, invalid and falsified outcomes are first-class entries.

## Automation

- `.github/workflows/factory-pulse.yml` wakes independent lanes without creating a global barrier.
- `.github/workflows/spider-lane.yml` executes one idempotent, checkpointed lane cycle.
- `.github/workflows/codex-sync.yml` serializes only canonical-memory writes; it never blocks lane research.
- `.github/workflows/product-promote.yml` is the guarded path for accepted Product code into `main`.
- `.github/workflows/ci.yml` validates the control plane and product kernel.

Operational invariants and lessons carried forward from the pre-2.0 factory and the ChoreScore/Wix automations are in `docs/AUTOMATION_INVARIANTS.md`.
