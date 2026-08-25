# SPIDER RUN MEMORY — INDEX

Maintained by: RUN EVIDENCE CURATOR. Updated: 2026-08-25.
Epistemic rule: log-only observations are leads/diagnostics, never accepted scientific claims. Statuses used: `AUDITED_DURABLE`, `DURABLE_UNAUDITED`, `LOG_ONLY_UNAUDITED`, `OPERATIONAL_DIAGNOSTIC`, `DUPLICATE`.

---

## 1. Live distilled runs

| Run | Workflow | Class | Conclusion | One-line essence | Record |
|---|---|---|---|---|---|
| 32880942022 | SPIDER Repo Hygiene (repo-hygiene.yml, run #1) | OPERATIONAL | success | First evidence-safe Actions pruning: **deleted 102 raw run logs** (98 orchestration = no material loss; 4 deleted CTO-council runs = UNKNOWN loss; 1 fully recovered from Git). This run's own log is the sole deletion manifest → `safe_to_prune=false`. | `runs/32880942022.json` |

## 2. Deleted-runs recovery incident (triggered by 32880942022)

Authoritative record: `DELETED_RUNS_RECOVERY.json`; per-run tombstones: `deleted/<run_id>.json` (102 files).

- Deleted set (window 2026-08-24T23:32:44Z → 2026-08-25T17:42:27Z): Ox Watchdog ×39, Research Program Supervisor ×26, Intel Supervisor ×23, Critical CTO Council ×5, Lane Repair Supervisor ×5, Product Supervisor ×2, Runtime Supervisor ×2. Hygiene counters: `deleted=102 kept=54 failed=0 protected_ids=228`.
- **Explicit signal (per role card):** the 97 supervisor/watchdog deletions carried no cycle/* branch and no scientific claim; none is referenced anywhere in durable repo content (verified by exhaustive git grep over fetched refs, commit messages, branch names, working tree). Only in-run operational diagnostics are lost.
- **CTO Council:** run 32876814203's full output pre-existed at `origin/lab/cto@6b1f030` (`docs/CTO_LEDGER.md` CTO-1..CTO-4, five `docs/CTO_TO_*.md`, `state/cto_direction.json` council_pass=CTO-4) → loss NONE_MATERIAL. Runs 32864023130, 32864726559, 32875585131, 32879434960 left no attributable durable artifact → loss UNKNOWN; do not reconstruct their content.
- Guard-version note: the executing script (commit `3e5ea6d`) lacked a distillation requirement; hardened afterwards by `1afb229` / `a09d036`. Future hygiene must prune only distilled (`safe_to_prune=true`) runs.

## 3. Thematic digest

- **Provenance & retention policy (INFRA/CTO):** raw Actions logs are now a non-renewable resource; the only surviving manifest of what was pruned lives in run 32880942022's log. Orchestration workflows should persist run-id-attributed receipts before completion so recoverability is structural, not archaeological. (`DURABLE_UNAUDITED` for Git facts; proposals are `HYPOTHESIS`.)
- **Orchestration economics (RUNTIME/INFRA):** ~5.6 pure-orchestration runs/hour (102 in ~18h) dominate Actions volume vs 54 kept substantive runs; watchdog cadence (~39 watchdog deletions) is the largest single contributor. (`OPERATIONAL_DIAGNOSTIC`)
- **Cumulative CTO memory location:** latest council synthesis (CTO-4, bottleneck ONE-SHOT-DECODE-DEBT, program DECODABLE-FIRST-PASSES) lives on `lab/cto@6b1f030`, not in this directory. Linked here for navigation only; its content is advisory CTO synthesis (`DURABLE_UNAUDITED` as to durability), never a scientific verdict.

## 4. Navigation

- Per-run records: `runs/<run_id>.json`
- Tombstones: `deleted/<run_id>.json`
- Deletion incident aggregate: `DELETED_RUNS_RECOVERY.json`
- CTO actionable radar: `CTO_FEED.json`
