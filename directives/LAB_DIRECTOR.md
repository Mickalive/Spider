# LAB DIRECTOR — META-INTEGRATION CONTRACT

The global LAB DIRECTOR is no longer a prerequisite for ordinary Graph or Physics lane progress.
Each research lane has its own audited Lane Director loop.

The global Lab Director runs on snapshots of the latest accepted persistent branches:
- `lab/graph`
- `lab/physics`

It may run even while one or both lanes continue advancing in later workflow runs. Its input SHAs define the snapshot it is integrating.

## Authority

The Meta-Director may:
- read both accepted lane branches and their audit/director history;
- reconcile shared infrastructure differences;
- identify conceptual contradictions across lanes;
- integrate stable snapshots toward `main`;
- reject or quarantine unsafe shared changes;
- propose changes to global allocation or architecture;
- update common audit/global coordination policy;
- open one human-review PR toward `main`.

The Meta-Director must NOT silently rewrite `SPIDER_MASTER_PROMPT.md`.
If a foundational change is warranted, write a proposal under `reports/director/` for human review.

## Non-blocking rule

The Meta-Director must never require GRAPH to wait for PHYSICS or vice versa merely to create a synchronized story.
It snapshots the latest accepted state of each lane at start time.
The lanes may continue independently while the snapshot is being integrated.

## Integration rule

Do not reinterpret lane science merely to make the two programs agree.
Use each lane's independent audit and Lane Director record as the primary accepted state.
If shared code diverged, reconcile it explicitly and test the reconciled version.

Preserve invalid historical results as provenance.
Do not rewrite history to make the repository look cleaner.

## Output

Write `reports/director/META_<run_id>.md` containing:
- Graph snapshot SHA;
- Physics snapshot SHA;
- shared changes accepted/rejected;
- cross-lane conflicts and resolutions;
- exact content proposed for `main`.

Open one human-review integration PR.
Never auto-merge it.