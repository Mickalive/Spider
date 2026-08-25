# SPIDER — CANONICAL ACTIVE WORKFLOW MAP

Status: operational inventory after Architecture V3 cleanup, 2026-08-25.

This file is descriptive, not scientific evidence. A workflow that is no longer needed by this architecture should be removed rather than kept as historical clutter. Scientific/history provenance belongs in accepted branches, cycle branches, ledgers and Run Evidence Memory — not in obsolete workflow YAML.

## Agent control plane

Every OpenCode session receives root `AGENTS.md`. Every configured custom agent in `.opencode/agents/` must have exactly one operating card in `docs/agents/AGENT_CARDS.md` defining status, mission, inputs, outputs, boundaries and handoff/stop rules.

`run-opencode-with-retry.sh` overlays this current control plane onto persistent lab branches and refuses to launch when the custom-agent registry is incomplete, duplicated or when a requested agent is `LEGACY_DISABLED` without explicit reactivation. This applies even when a lab branch contains an older role definition.

## Core work lanes

| Workflow | Purpose | Persistent truth |
|---|---|---|
| `graph-loop.yml` | Graph / operational-memory experiments, audit, Director | `lab/graph` |
| `physics-loop.yml` | Core Physics experiments, audit, Director | `lab/physics` |
| `intel-loop.yml` | External-mechanism discovery/reproduction/audit | `lab/intel` |
| `product-loop.yml` | Product hypothesis → architecture → build → independent benchmark/review | `lab/product` |
| `product-beta-repair.yml` | Same-beta repair after Product audit `REVISE`; benchmark remains frozen | `lab/product` + `cycle/product-repair/*` |
| `runtime-loop.yml` | Agent-facing Capability Capsule/runtime implementation, benchmark, audit | `lab/runtime` |
| `frontier-research.yml` | Generic CTO-chartered autonomous research team | `lab/frontier/<team_id>` |

## Portfolio / research governance

| Workflow | Purpose |
|---|---|
| `cto-council.yml` | Global critical CTO review; reads accepted evidence + distilled run-memory radar; charters Frontier teams |
| `program-supervisor.yml` | Recover/launch Director-recommended Graph/Physics program succession without consuming failed successors |

## Continuity / recovery

| Workflow | Purpose |
|---|---|
| `intel-supervisor.yml` | Keep Intel moving across legitimate continuation and infrastructure interruption |
| `product-supervisor.yml` | Keep Product optimization moving without hiding real benchmark/build failures |
| `runtime-supervisor.yml` | Keep Runtime moving across legitimate continuation/infrastructure interruption |
| `lane-repair-supervisor.yml` | Recover persisted Graph/Physics `REVISE` gates when the originating workflow dies before its own router |
| `ox-watchdog.yml` | Re-run only defensible transient OpenCode/network/runner infrastructure failures |

## Knowledge retention / hygiene

| Workflow | Purpose |
|---|---|
| `evidence-curator.yml` | Distill useful Actions-log knowledge into durable Run Evidence Memory; never promotes unaudited logs to scientific truth |
| `repo-hygiene.yml` | Delete completed Actions runs only after Curator distillation + explicit `safe_to_prune=true`; `cycle/*` runs remain protected |

## Explicitly retired

- `main.yml` — obsolete two-lane Graph+Physics launcher; replaced by autonomous lane/supervisor architecture.
- `meta-sync.yml` — obsolete two-lane Lab Director/meta sync; replaced by persistent accepted lanes + global Chief CTO/Runtime/Product/Frontier architecture.

## Invariants

1. A scientific or product run is not disposable merely because it failed operationally.
2. Runs referenced by `cycle/*` branches are protected from automatic pruning.
3. Unarchived Actions runs are never pruned.
4. A log-only finding can orient research but cannot become accepted evidence without validation.
5. Deleted workflow YAML is not an archive mechanism; durable knowledge must live elsewhere.
6. New workflows should be created only when an existing generic lane/supervisor cannot express the function cleanly.
7. A custom agent without exactly one canonical operating card is a control-plane error, not an invitation to improvise.
8. `LEGACY_DISABLED` agents remain historical definitions only until explicit human/CTO reactivation under the current architecture.
