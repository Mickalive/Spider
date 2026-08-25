# SPIDER RUN MEMORY — INDEX

Maintained by: RUN EVIDENCE CURATOR. Updated: 2026-08-25.
Epistemic rule: log-only observations are leads/diagnostics, never accepted scientific claims. Statuses used: `AUDITED_DURABLE`, `DURABLE_UNAUDITED`, `LOG_ONLY_UNAUDITED`, `OPERATIONAL_DIAGNOSTIC`, `DUPLICATE`.

---

## 1. Live distilled runs

| Run | Workflow | Class | Conclusion | One-line essence | Record |
|---|---|---|---|---|---|
| 32880942022 | SPIDER Repo Hygiene (repo-hygiene.yml, run #1) | OPERATIONAL | success | First evidence-safe Actions pruning: **deleted 102 raw run logs** (98 orchestration = no material loss; 4 deleted CTO-council runs = UNKNOWN loss; 1 fully recovered from Git). This run's own log is the sole deletion manifest → `safe_to_prune=false`. | `runs/32880942022.json` |
| 32689298051 | SPIDER Physics Lane (#3, attempt 2) | SCIENTIFIC | cancelled | WP-005 cycle-2 anchor. **Raw log EMPTY / zero jobs retained**; content recovered from Git only: WP-005 transfer FALSIFIED → audited → director-integrated on `lab/physics`; also acted as cycle-2 Director (succession launched WP-006). Queued ~18.6h, then cancelled ~5min in while Physics #4 was live. | `runs/32689298051.json` |
| 32776372437 | SPIDER Physics Lane (#4) | SCIENTIFIC | success | **WP-006 H-ID identifiability-by-restart gate: FALSIFIED** at frozen floors (producers 2/4, verified BPs 38<60), dataset wp006_v1 (1075 rows), prereg freeze chain commit-verified. Auditor recomputed everything, found report misstated FN control (62/74 not 62/62; openlibrary silently missing from merged BP manifest) → REVISE → repair run 32793165981. Later accepted via 5-gate chain; TERMINATE_LANE engaged; domain reopened under V3 without reopening WP-006. | `runs/32776372437.json` |
| 32781482957 | SPIDER Intel Research Lane (#1) | INTEL | success | First Intel cycle: scout surveyed 8 systems + skill-marketplace infra, selected SGDR (arXiv:2606.04391); clean-room preregistered reproduction beat task-only retrieval (hard@1 36/74 vs 25/74 vs incumbent 0/74; conversion novel actions 75/84/421); auditor REVISE (hash-chain breaks, wrong-cluster claim, stale URL) but numbers reproduced bit-exactly (522/522 rows). Final accepted status VALIDATED_USEFUL @ PoC ceiling (run 32800296360, integration fca0acb). | `runs/32781482957.json` |
| 32782331702 | SPIDER Graph Lane (#5) | PRODUCT | success | **Empty production snapshot**: one `external_directory` permission auto-rejection (`cd /home/runner/work/Spider`) aborted the whole team session after ~7m of context loading; workflow pushed the empty branch and audited it anyway. Auditor caught it → REVISE + predeclared second-offense BLOCKED rule. Root cause is LOG-ONLY in this bundle → `safe_to_prune=false`. | `runs/32782331702.json` |
| 32783797303 | SPIDER Graph Lane (#6, repair r1 of #5) | PRODUCT | success | Full recovery: preregistered 13-arm robustness family, V00 byte-reproduces cycle-3 baseline (20/20), best arm V31 6/8 offline + live R2LIVE 6/6 memory-solved both passes → audit **PASS** → Director integrated `lab/graph` f42c14d→d41fe9b, program graph-addressing-robustness COMPLETE with binding limits (V31 = selection-on-instrument decision outcome, instrument spent; category addressing unsolved); succession to graph-inheritance-scaling (later G-H5). | `runs/32783797303.json` |

## 2. Deleted-runs recovery incident (triggered by 32880942022)

Authoritative record: `DELETED_RUNS_RECOVERY.json`; per-run tombstones: `deleted/<run_id>.json` (102 files).

- Deleted set (window 2026-08-24T23:32:44Z → 2026-08-25T17:42:27Z): Ox Watchdog ×39, Research Program Supervisor ×26, Intel Supervisor ×23, Critical CTO Council ×5, Lane Repair Supervisor ×5, Product Supervisor ×2, Runtime Supervisor ×2. Hygiene counters: `deleted=102 kept=54 failed=0 protected_ids=228`.
- **Explicit signal (per role card):** the 97 supervisor/watchdog deletions carried no cycle/* branch and no scientific claim; none is referenced anywhere in durable repo content (verified by exhaustive git grep over fetched refs, commit messages, branch names, working tree). Only in-run operational diagnostics are lost.
- **CTO Council:** run 32876814203's full output pre-existed at `origin/lab/cto@6b1f030` (`docs/CTO_LEDGER.md` CTO-1..CTO-4, five `docs/CTO_TO_*.md`, `state/cto_direction.json` council_pass=CTO-4) → loss NONE_MATERIAL. Runs 32864023130, 32864726559, 32875585131, 32879434960 left no attributable durable artifact → loss UNKNOWN; do not reconstruct their content.
- Guard-version note: the executing script (commit `3e5ea6d`) lacked a distillation requirement; hardened afterwards by `1afb229` / `a09d036`. Future hygiene must prune only distilled (`safe_to_prune=true`) runs.

## 3. Thematic digest

- **Provenance & retention policy (INFRA/CTO):** raw Actions logs are now a non-renewable resource; the only surviving manifest of what was pruned lives in run 32880942022's log. Orchestration workflows should persist run-id-attributed receipts before completion so recoverability is structural, not archaeological. (`DURABLE_UNAUDITED` for Git facts; proposals are `HYPOTHESIS`.)
- **Orchestration economics (RUNTIME/INFRA):** ~5.6 pure-orchestration runs/hour (102 in ~18h) dominate Actions volume vs 54 kept substantive runs; watchdog cadence (~39 watchdog deletions) is the largest single contributor. Substantive lane cycles cost 17min–3.5h runner time each (Physics #4 ≈3h27m; Intel #1 ≈2h27m; Graph #6 ≈1h44m; Graph #5 ≈17m wasted). Physics run #3 sat queued ~18.6h before a 5-minute cancellation. (`OPERATIONAL_DIAGNOSTIC`)
- **Permission auto-rejection is a single point of failure for agent sessions (RUNTIME):** one out-of-workspace path access terminated Graph #5's whole team phase (empty snapshot), and an empty snapshot also occurred later in Intel's repair round 2 — a recurring cross-lane failure mode whose only root-cause evidence is run 32782331702's log. Workflows cannot distinguish aborted sessions from completed work (no zero-commit guard before audit). (`LOG_ONLY_UNAUDITED` root cause; recurrence `DURABLE_UNAUDITED` via INTEL_LEDGER)
- **Audits keep catching self-report defects, not measurement fraud (all lanes):** WP-006 report said FN control 62/62, raw rows say 62/74 (later finalized 67/74); SGDR report attributed wins to wrong site cluster while aggregates were correct; Graph E2 used non-reproducible denominators. Aggregate recomputation alone would have missed several of these — per-row/per-cell adversarial recomputation is what works. (`AUDITED_DURABLE` as to the corrections being accepted)
- **Cumulative CTO memory location:** latest council synthesis (CTO-4, bottleneck ONE-SHOT-DECODE-DEBT, program DECODABLE-FIRST-PASSES) lives on `lab/cto@6b1f030`, not in this directory. Linked here for navigation only; its content is advisory CTO synthesis (`DURABLE_UNAUDITED` as to durability), never a scientific verdict.
- **Lane state has advanced past every distilled cycle:** `lab/graph` completed G-H4 (this batch) and later G-H5; `lab/physics` accepted WP-006 FALSIFIED (5 gates), engaged TERMINATE_LANE, then reopened the domain under V3 handing orthogonal successor search to the CTO portfolio; `lab/intel` integrated SGDR (cycle 1) and later Unbrowse (cycle 5). These records capture each run's own slice only.

## 4. Navigation

- Per-run records: `runs/<run_id>.json`
- Tombstones: `deleted/<run_id>.json`
- Deletion incident aggregate: `DELETED_RUNS_RECOVERY.json`
- CTO actionable radar: `CTO_FEED.json`
