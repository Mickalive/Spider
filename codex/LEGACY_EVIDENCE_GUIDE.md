# SPIDER — Pre-2.0 evidence bridge (read before allocating NEW research)

The full **frozen** pre-2.0 source is `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md`, Git blob `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3` (~22 MB, 566,404 lines). Research 2.0 packets are **separate**. Do not join their counts or treat a substring labelled PASS as a successful hypothesis.

## Available lightweight entry points

- `codex/legacy_brief.json` — source-pinned, bounded historical findings, automatically included as `legacy_history` in `scripts/build_portfolio_snapshot.py`. It is a first-pass *screen*, not evidence that no other relevant historical artifact exists.
- `codex/legacy_artifact_index.json` — 1,401 historic unique final-state scientific/data artifacts, with `sha`, original `paths`, `experiment_ids`, `lane`, `role`, and exact **source line interval** in the frozen document. Artifact counts are not experimental counts: there are 717 `result_measurement`, 250 `audit_gate`, 106 `report_verdict`, 153 `state_provenance`, 51 `prereg_protocol`, 107 `context_input`, 17 `charter_question` entries.
- Exact **archived original** is authoritative; an index's `verdict_tokens` are search aids only. A candidate repeated experiment requires reading original design/results/audit, not just the keyword inventory.

## Read one archived artifact; never load the 22 MB whole file into LLM context

On a checkout with Git installed:

```bash
git fetch -q origin 'refs/heads/archive/spider-codex-ultimate:refs/remotes/origin/archive/spider-codex-ultimate'
git show origin/archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md | sed -n '201815,201870p'
```

This is an example source excerpt for the corrected Graph speed claim, **not** a generic proof; use the exact `start_line/end_line` returned by the JSON index for your selected artifact. To find matching index entries:

```python
import json
entries=json.load(open("codex/legacy_artifact_index.json",encoding="utf-8"))["artifacts"]
for x in entries:
    if any("physics" in p.lower() and "report" in p.lower() for p in x["paths"]):
        print(x["sha"],x["paths"],x["start_line"],x["end_line"])
```

The underlying source is **read-only**. No scientific claim can be upgraded by indexing alone.

## Product-relevant historical counterexamples

| Prior | Status / precise scope | Consequence |
|---|---|---|
| Graph run-1 (artifact 4.114, `9687ff787f2d74460bb7006826008852f5b4416b`) | Withdrawn 8.5x speed headline; on 3 **matched** tasks wall time 2.822s cold vs 2.816s replay = **1.002x**. Eliminated novel decisions, not total real-agent latency. | Exact replay cannot be sold as an 8.5x result; compare identical tasks and full costs. |
| G-H2 blind composition (product summary 4.697, `017a80aeb9a6759c8f6913a37031ff1616ec1bda`) | Small 3/3 composition result against 0/3 limited baselines, with keyword and oracle dependence. | Evidence that composition can be made to work *in a controlled scope*, not general cross-site or strong-baseline advantage. |
| WP-002B (Codex section 1) | 901 real next-state transitions, 300 trajectories; rule dimensional accuracy 0.6238, NN 0.6295, shuffle 0.5706; only repeated trajectory holdouts. | Reject false superior-to-NN or website-holdout claims; replicate only on genuinely independent sites/protocols. |
| WP-003 (artifact 4.203, `292e3243d9bc7a3b88712788a7cb05709eb74eb9`) | **MEASUREMENT_INVALID** due to target leakage and invalid 'bootstrap'. | Do not treat an invalid experiment as falsification of Web physics; never repeat the flawed measurement design. |
| WP-003B follow-up (artifact 4.237, `f6cfdfc749cae9eb4d9fcc4b11b94b63a2bcfb6e`) | Controlled 875-row follow-up: action-only MSE 0.756 vs full 0.735; pre-state mechanics added <3% explained variance in that setting. | Further pre-state-only predictor tuning has limited upside; change representation/observable or park. |
| Mind2Web V0.50 (Codex section 1) | 6/176 exact human routes, 4/176 strict causal chains; action extraction 3843/6766. | Human-route replay and loosely defined composition are too weak as a general product thesis. |

## Mandatory anti-duplication review

When proposing NEW direction on Graph, Physics, Runtime, Product, Intel or Frontier:

1. Match historical **scientific question, substrate, controls, exact comparator, metric and failure mode**, not only the name of a claim.
2. Use the `legacy_history` snapshot and filter `codex/legacy_artifact_index.json`; inspect exact archived source if a match looks material.
3. Put one of `LEGACY: DUPLICATE / REPLICATION / DISTINCT_EXTENSION / NO_MATCH / UNCERTAIN` in the existing `comparative_reasoning`, alongside source SHA or an explicit limitation of the search.
4. Don't allocate expensive work to a duplicate unless it is a proper independently powered replication with a meaningful validity upgrade. A historical invalid is not proof of falsification, but it **is** a warning not to repeat the same flaw.
5. Keep the pre-2.0 archive immutable and separate from Research 2.0 canonical `claim_state.json`. Only experiments that pass Research 2.0's own gates may advance current claim statuses.

This makes the legacy archive usable for strategic choices without adding another autonomous lane, an oversized agent prompt or a new epistemic authority.
