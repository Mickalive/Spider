# SPIDER — RESEARCH 2.0 AGENT OPERATING STANDARD

This file is binding for OpenCode sessions in the active Research 2.0 factory.

## Precedence

1. `SPIDER_MASTER_PROMPT.md` — scientific constitution and frozen conceptual distinctions.
2. `SPIDER_ARCHITECTURE_RESEARCH2.md` — active post-pre2 organization/automation.
3. `research/portfolio/POLICY.md` — binding Global Research Director / Scout direction policy for NEW experiments.
4. `research/EXPERIMENT_PACKET.md` — binding inter-agent transmission contract and packet semantics.
5. exact immutable `request.json`, including `director_mandate` when present, then frozen `spec.json`, `prereg.md`, `freeze.json`.
6. lane charter in `research/lanes/registry.json`.
7. accepted Codex evidence.

Never silently rewrite constitutional files.

`SPIDER_CODEX.md` is accepted-evidence output owned by the canonical Codex synchronization step. Lane DESIGN, EXECUTE, AUDIT, lane DIRECTOR, Scout and Global Research Director agents may read it but must never edit, regenerate, append to, format, or otherwise mutate it directly.

## Objective

Optimize for verified inherited work, not activity, run count, pretty reports or route replay.

The final product must materially change how external agents explore the Web. Do not assume the current kernel is the final architecture. Research may replace internals when evidence supports it.

## Evidence

Keep these distinct:

- observation;
- proof of concept;
- replication;
- generalization;
- robust result;
- hypothesis;
- operational diagnostic.

Negative, falsified, blocked and measurement-invalid results are first-class.

## Inter-agent transmission discipline

Every agent must read `research/EXPERIMENT_PACKET.md` before producing a stage output.

The canonical experiment packet is the communication channel between fresh-context agents. Do not rely on prior model conversation, Actions-log prose or unstated assumptions to carry scientific state forward.

Preserve the chain:

`RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT -> INTERPRETATION -> AUDIT FINDING -> DECISION -> HANDOFF`.

Do not collapse these levels. In particular:

- never turn an interpretation into a raw observation;
- never turn missing data or infrastructure failure into a negative scientific result;
- never omit a mandatory packet field because no value is available — use `null`, `[]` or `{}` according to the packet contract and explain the absence;
- preserve stable experiment, claim, metric, control and artifact identities so downstream agents can refer to the exact same objects;
- downstream stages may challenge upstream conclusions but may not silently rewrite upstream evidence;
- material claims should reference exact packet fields or artifacts when possible;
- `handoff.json` must preserve what is established, rejected, unknown and specifically unsafe to assume.

For `verdict.json.claim_updates[*].status`, DIRECTOR must use one of the canonical registry statuses exactly: `HYPOTHESIS`, `EXPERIMENTAL`, `VALIDATED`, `PRODUCT_CORE`, `SHIPPED`, `REJECTED`, `BLOCKED`, `MEASUREMENT_INVALID`, `SUPERSEDED`. Descriptive words such as `SUPPORTED`, `SUPPORTED_BOUNDED`, `PARTIAL` or `OPEN` belong in the event `reason`, not in `status`.

When `request.json` contains a `parent_handoff` reference, read that exact handoff before DESIGN. Treat its `carry_forward` categories as inherited scientific state, not as an automatic research agenda. `handoff.next_question` is a local proposal only. When `request.json` also contains `director_mandate`, the Global Research Director's target claim and strategic question are the binding direction for that NEW experiment. New evidence may supersede inherited state, but the change must be explicit.

Cross-lane inheritance occurs through accepted Codex evidence or exact immutable packet/artifact references. Do not import another lane's unrecorded narrative.

## Global direction discipline

The six scientific lanes do not self-authorize new child experiments.

A permanent non-scientific Scout lane runs broad reconnaissance for the Global Research Director. Scout may use Codex evidence, shallow external landscape research and general agent knowledge, but must label these epistemic categories separately and never create scientific claims.

The Global Research Director chooses the most promising next objective for every scientific lane from the whole current program. It may CONTINUE, PIVOT, PARK, REOPEN or TERMINATE a bounded thread. It is responsible for reactivating stopped/idle lanes when useful work exists.

Already-frozen experiments are completed before strategic redirection. Pre-freeze work may be superseded by a new Director mandate.

Local lane Directors still adjudicate evidence and produce bounded handoffs, but they do not dispatch their own next experiment.

## Work discipline

- read the exact request and lane charter before acting;
- read relevant Codex evidence rather than reconstructing from old logs;
- preserve RAW OBSERVATION separately from DERIVED STATE;
- do not run outcome-bearing measurements during DESIGN;
- do not modify frozen files after `freeze.json` exists;
- use strong baselines and nulls appropriate to the claim;
- disclose representation loss and validity threats;
- prefer a discriminating test over another narrative;
- do not ask interactive questions during autonomous runs;
- never invent a result when infrastructure fails;
- leave a durable handoff;
- for DESIGN of a governed NEW experiment, follow the `director_mandate` instead of drifting back to the parent handoff.

## Branch/scope discipline

You may edit only the paths granted in the exact workflow prompt.

Never edit `.github/`, `.opencode/`, constitutional files, model routing, `SPIDER_CODEX.md`, another lane, or another experiment.

Do not use `git add -A`, reset shared branches, force-push or erase prior evidence.

## Product discipline

`UNKNOWN` is a valid product answer.

Do not promote an experimental mechanism into Product Core without a verdict authorizing it.

Measure end-to-end economics: correctness, model calls/tokens, browser/network work, retrieval, verification, repair, latency, false accepts, staleness and amortization.

## Physics discipline

Graph reuse is not Physics.

Physics claims require an operational mathematical object, observable, falsifier, strong nulls and identifiability argument. A failed bounded Physics program does not close the Physics domain.

## Frontier discipline

Frontier exists to search outside the current solution basin. It must not merely rename failed experiments. Orthogonal mechanisms and levels of description are encouraged when they can be tested.

## Failure discipline

If a required substrate, model, dataset or tool is unavailable, write the exact failure and the smallest next action that could unblock it. Do not weaken a preregistration after seeing outcomes.
