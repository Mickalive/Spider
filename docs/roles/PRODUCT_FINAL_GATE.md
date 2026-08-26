# SPIDER — FINAL PRODUCT GATE

## Purpose

SPIDER's autonomous system is **nonterminal by default**. Graph, Physics, Intel, Runtime, Product, CTO and normal CTO-chartered Frontier work must keep recovering, repairing, replanning or opening the next bounded program while the product is unfinished.

A local `PASS`, `BLOCKED`, falsification, exhausted hypothesis, `continue=false`, `WAIT_FOR_EVIDENCE`, build failure, audit failure, runner failure or Ox failure is **never a global stop condition**. Such outcomes remain preserved as evidence and may change the next program, but they do not terminate autonomous work.

The only machine-readable stop condition is an accepted Product file:

`state/product_final.json`

on branch `lab/product`.

## Mechanical terminal contract

Autonomous supervisors may stop relaunching work only when the file exists and satisfies all of the following:

```json
{
  "final_product": true,
  "status": "READY_FOR_HUMAN_HANDOFF",
  "independent_audit_pass": true,
  "baseline_win_audited": true,
  "evidence_refs": ["... at least one durable accepted/audited reference ..."]
}
```

Extra fields are encouraged, especially:

- `product_id` / `version`;
- exact executable surface (SDK/CLI/API/adapter/package);
- installation/run instructions;
- audited Product Beta or benchmark IDs;
- baseline, version/date and locally reproduced status;
- predeclared win rule and measured metrics;
- reliability/recovery test references;
- known limitations and claim ceiling;
- final accepted Product commit;
- generated timestamp.

## Meaning of READY_FOR_HUMAN_HANDOFF

This status means the autonomous build/research loop has produced a **real executable product candidate**, not a concept, report, wrapper or decorative demo. At minimum:

1. an agent-facing executable product surface exists;
2. ordinary use does not depend on undocumented manual intervention;
3. installation/integration and acceptance tests are executable and pass;
4. at least one useful target task class has a credible baseline reproduced or otherwise validly established;
5. a predeclared comparative Product Beta / benchmark has passed independent audit and demonstrated the required win after relevant retrieval, verification, recovery and maintenance overhead;
6. important failure/recovery behavior has executable coverage;
7. limitations and the claim ceiling are explicit;
8. the accepted Product branch contains the exact candidate corresponding to the audited evidence.

`baseline_win_audited=true` must never be inferred from a vendor claim, an unaudited branch, a scout result, a partial metric or a changed post-hoc win rule.

## Authority and safety

The Product Director may write/update `state/product_final.json` only from accepted and independently audited Product evidence. If any required condition is not met, the file must be absent or contain `final_product=false`.

This gate authorizes **stopping autonomous research/build relaunches only**. It does not authorize public deployment, commercialization, external account actions or other human-gated operations.

## Continuity invariant

Until the terminal contract above is mechanically true:

> **No autonomous lane is allowed to die silently.**

A lane may repair the same cycle, preserve a BLOCKED result and replan, move to an orthogonal hypothesis, request CTO reallocation, or open a fresh bounded engineering/research program. It may not treat a local terminal state as permission for global inactivity.
