# Automation invariants — SPIDER Research 2.0

This is the failure-prevention contract for the GitHub factory.

It carries forward concrete lessons from the previous SPIDER factory and from the ChoreScore/Wix multi-agent automations.

## 1. No global synchronization barrier

Graph, Physics, Runtime, Product, Intel and Frontier are independent workflow executions. An auditor for one lane starts when that lane is ready, not when unrelated lanes finish.

## 2. No central matrix as the source of truth

`factory-pulse.yml` is a liveness pulse only. It does not own scientific state. If it dies, lane branches and experiment packets remain valid and the next pulse can resume.

## 3. Immutable work identity

Every cycle has GitHub `run_id`, deterministic `experiment_id`, immutable `request_id`, immutable `request_hash`, and exact starting commit.

A runner must never consume an old "latest work request". This prevents the stale-request failure seen in prior product automation.

## 4. Stage checkpoints, not all-or-nothing recovery

DESIGN, EXECUTE, AUDIT and VERDICT checkpoint separately.

A failed AUDIT does not require rerunning EXECUTE. A failed VERDICT does not erase the audit. A rerun of the same GitHub run resumes the same experiment.

This replaces recovery designs that restarted too much work and then made no product progress.

## 5. Explicit dispatch, plus scheduled liveness

Do not depend on ordinary `push` events created with `GITHUB_TOKEN` to wake the next workflow.

Continuation uses explicit `workflow_dispatch`. A periodic pulse repairs any sleeping transition. This directly avoids the dead transitions encountered in the Wix automation.

## 6. Bounded chaining, unbounded program lifetime

One run may self-dispatch only a small number of immediate successors. The scheduled pulse keeps the program alive afterward.

This prevents both infinite busywork and a machine that silently stops forever.

## 7. Model failure is not scientific failure

Network, 429/5xx, provider unavailability and model disappearance are retryable operational faults. The runner rotates independent model candidates.

A failing test, invalid experiment, falsified hypothesis or bad code is not retried as a network fault.

## 8. Durable failure receipts

Every stage failure writes `failure.json` or an equivalent lane-state receipt before the runner exits.

Actions logs are diagnostics, not scientific memory.

## 9. Narrow Git writes

Never `git add -A`.

Every commit explicitly stages the experiment directory, the current lane state and the small lane-specific code scope granted by policy.

This prevents accidental control-plane or peer-lane commits.

## 10. No concurrent writers to one branch

Each lane has a distinct concurrency group and persistent branch.

Codex and Product promotion share a separate `spider-main-writer` concurrency group. They may queue, but they never block lane research.

## 11. Do not cancel useful in-progress work

`cancel-in-progress: false` on scientific and canonicalization workflows.

New pulses detect queued/running work before dispatching another copy.

## 12. Research must move Product; Product must not freeze Research

Every experiment states the product consequence of both positive and negative outcomes.

Product implements validated capabilities continuously.

Physics and Frontier remain free to discover a better internal architecture; the present kernel is not treated as doctrine.

## 13. Failed product cycles cannot contaminate future product state

A rejected Product cycle must end with experimental code reverted from the persistent Product branch, while its evidence packet remains.

Only audited, promotion-authorized code may survive into the branch tree and then `main`.

## 14. Codex coverage is mechanically checked

A finalized experiment without the full canonical packet appears in `codex/coverage_gaps.json`. The compiler never silently pretends the result is archived.

## 15. Health before volume

The factory prefers six healthy independent lanes over dozens of duplicated agents.

Additional parallel work is justified by distinct hypotheses or independent attack surfaces, not by different names for the same prompt.

## 16. Bootstrap must prove itself before activation

A new or materially changed control plane is first installed on an isolated bootstrap branch and must pass repository validation, product-kernel tests and workflow syntax checks before `main` is advanced. The factory is never intentionally activated from a partially installed or unvalidated control plane.
