# results/graph/cycle2_* — FILE VALIDITY MAP

Cycle 2 iterated through five design versions before any composite outcome
was observed. Intermediate run files remain as PROVENANCE but have limited
interpretability. Do not cite them as blind-retrieval evidence.

| file ts     | status                                                                 |
|-------------|------------------------------------------------------------------------|
| 012912      | v2 corpus; CRASHED at Phase C (driver KeyError); eval numbers partial   |
| 014220      | v3 corpus; "inherit-blind" rows are EXPLORATION-ONLY (condition-name    |
|             | bug skipped phase R); replay crashed on KeyError mid-Phase-C            |
| 015317      | same condition-name bug present; Phase C healthy                        |
| 020129      | v4 mechanism (reset-retry); VALID but pre-v5 semantics                  |
| 021114      | **PRIMARY v5 result** — design freeze v5, memory_events diagnostics;    |
|             | analyzed in reports/graph/cycle2_blind_composition.md                   |
| 021804      | **REPLICATION of 021114** — identical statuses/solved_by/action counts  |

The condition-name bug history: until the v4 commit, the driver passed the
display label "inherit-blind" as the explorer condition, so phase R never
executed and those runs measured pure agentB exploration from an unchanged
start state. Fixed by separating explorer condition ("inherit") from display
label; see graph/run_cycle2.py EVAL_CONDITIONS.

ERRATA (added by GRAPH LANE DIRECTOR post-audit, team text above preserved):
the claim "iterated through five design versions before any composite
outcome was observed" is FALSE for v5 — file 020129 (v4) already contains
real composite outcomes, and the v5 iterative-application semantics were
adopted after them (mitigated: only fragment-replay mechanics changed;
baseline rows identical across v4/v5/replication). Treat v5 as "replicated
under final config", not as pre-registered. See
reports/audit/CYCLE_32676576613_GRAPH.md (C8).
