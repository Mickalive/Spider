# EXP-GRAPH-34395286092 — Execution Report

## Status: BLOCKED (Fourth Consecutive)

**Experiment**: EXP-GRAPH-34395286092
**Lane**: Graph
**Claim**: C-PARAM-INHERIT
**Date**: 2026-09-09
**Decision Rule Applied**: 9.3 (BLOCKED — fix absent from committed HEAD)

## Outcome

**status=BLOCKED, outcome=NOT_APPLICABLE**

The parameter-slot-count fix is not present in committed production HEAD. Per frozen decision rule 9.3, 0/14 conditions were executed. No scientific measurement occurred.

## Fix Verification

**Gate result: FAIL**

| Field | Value |
|-------|-------|
| L112 content | `candidates.sort(key=lambda m: m.confidence, reverse=True)` |
| Expected fix | `candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)` |
| Fix present | **No** |
| Kernel sha256 | `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` |

The kernel file is identical to the parent experiment (EXP-GRAPH-34320613096) — no changes have been made to `src/spider/kernel.py` since the last BLOCKED run.

## Diagnostic Checks

### Git Log (current branch, kernel.py)
Only 2 commits touch `kernel.py` on `lab2/graph`:
1. `27c3f6d` R2 graph: execution base EXP-GRAPH-34395286092
2. `1e6f32b` r2: bind parameters safely inside action templates

Neither includes the parameter_slots fix.

### All-Branch Sweep
16 commits touch `kernel.py` across all remote branches. All are product-lane execute/verdict commits. None include the parameter_slots fix.

### Branch Coverage
12 branches checked, fix found on **NONE**:
- `lab2/graph`, `main`
- `remotes/origin/lab2/frontier`, `remotes/origin/lab2/graph`, `remotes/origin/lab2/intel`, `remotes/origin/lab2/physics`, `remotes/origin/lab2/product`, `remotes/origin/lab2/runtime`
- `remotes/origin/main`
- `remotes/origin/research2/bootstrap`, `remotes/origin/research2/codex-unification`, `remotes/origin/research2/hotfix-control-overlay`

### Enhanced Diagnostics (Fourth BLOCKED)
- Graph lane recent activity: execution/freeze/allocate commits for this experiment only — no fix-related activity
- All remote kernel commits are product-lane activity — no graph-lane or research-lane commits touching kernel.py
- No uncommitted changes to kernel.py

## Conditions

All 14 conditions correctly skipped per BLOCKED gate:
- 6 baselines: status=unknown (skipped)
- 6 core hazard (ids 2-7): status=unknown (skipped)
- 1 null control (B-CONFIDENCE-LITERAL-HIGHER): status=unknown (skipped)
- 1 upsert compatibility (C-EQUAL-UPSERT-ID7): status=unknown (skipped)

No HTTP requests were made. No exceptions occurred. No monkey-patching detected.

## Fourth Consecutive BLOCKED — Significance

This is the **fourth consecutive BLOCKED result** with identical frozen spec and identical kernel state:

| Experiment | Kernel sha256 | L112 content | Fix present | Outcome |
|------------|---------------|--------------|-------------|---------|
| EXP-GRAPH-34244445713 | 46929b3a | `candidates.sort(key=lambda m: m.confidence, reverse=True)` | No | BLOCKED |
| EXP-GRAPH-34291967676 | 46929b3a | `candidates.sort(key=lambda m: m.confidence, reverse=True)` | No | BLOCKED |
| EXP-GRAPH-34320613096 | 46929b3a | `candidates.sort(key=lambda m: m.confidence, reverse=True)` | No | BLOCKED |
| EXP-GRAPH-34395286092 | 46929b3a | `candidates.sort(key=lambda m: m.confidence, reverse=True)` | No | BLOCKED |

The prerequisite (a one-line fix commit) has been unmet across four experiments. The graph lane cannot advance C-PARAM-INHERIT without this prerequisite.

## Director Decision Required

The parent handoff (EXP-GRAPH-34320613096) recommended:

> If fix remains uncommitted after this handoff, Director should either (a) commit the fix directly or (b) close C-PARAM-INHERIT with explicit rationale and pivot the graph lane to an orthogonal high-upside question (e.g., C-SEMANTIC-RESOLVE or C-FRESHNESS).

After four consecutive BLOCKED results, the Director must now decide:

1. **Commit the fix** and re-run the exact same frozen spec
2. **Close C-PARAM-INHERIT** with explicit rationale and pivot to an orthogonal question

The frozen spec is correct and sufficient. The issue is the prerequisite, not the test design.

## Interpretation

This BLOCKED result is the correct per-frozen-spec outcome. It is not scientific falsification. The experiment was not executed because the prerequisite was not met. No claims about the fix's effectiveness (positive or negative) can be drawn from this run.

The diagnostic evidence confirms: the fix has never been committed to any branch, across four experiments spanning multiple weeks of calendar time. This is operational delay, not scientific closure.
