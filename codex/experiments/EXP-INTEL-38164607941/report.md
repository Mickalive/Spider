# EXP-INTEL-38164607941 — EXECUTE report

**Lane:** intel · **Claim:** C-LLM-INHERIT · **Status:** COMPLETE · **Outcome:** FALSIFIES

Frozen design: single-factor prompt ablation (only `prompts.system` varies) on the audited
parent harness `EXP-INTEL-37982024058`, executed by the unmodified frozen parent runner.

- Treatment `P-TREAT-GOAL-SCHEMA`: goal sentence + action-schema enumeration
  (`sha256 36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716`).
- Comparator `P-COMP-UNDERSPECIFIED`: byte-identical to the parent system prompt
  (`sha256 1294954da7b1d6b9570b07e1e39cb48515b925355d0f33d5fabf72c8e8ce3876`).
- Candidates: `M-7B-QWEN` (primary) and `M-3B-QWEN` (fallback), Qwen2.5-Instruct Q4_K_M, CPU-only,
  credential-free, llama.cpp GBNF constrained decoding.

This report interprets `result.json`; it does not exceed the frozen claim or the bounded-negative
ceiling in `spec.json`. All numbers match `metrics` there.

## 1. Question and decision rule

Does supplying the task goal and action schema in the system prompt convert M-7B-QWEN's or
M-3B-QWEN's step-0 reveal-click into a full click-then-answer completion, where the only varied
dimension between paired cells is `prompts.system`?

The frozen decision rule was applied unchanged:

1. Preflight (PC-ORACLE-EPISODE 5/5, null control 0.0/0.0, random baseline parseable 1.0 and
   success < 0.6, all freeze artifact hashes, stack imports, GGUF digests) → **PASS**.
2. For each candidate, run the treatment and comparator cells unconditionally as a contemporaneous
   pair; classify each cell COMPLETE / EXCLUDED / PARTIAL; classify comparator as
   VALID / CONFOUND / REPLICATION_ANCHOR_*.
3. If ≥1 COMPLETE treatment cell exists and none clears → **FALSIFIES**.
4. If no COMPLETE treatment cell exists → MEASUREMENT_INVALID.

Applied trace: `rule1_preflight_pass → rule2a_run_pair (both candidates) →
rule2e_comparator=REPLICATION_ANCHOR_EXACT (both) → rule2h_treatment_fails_bar (both) →
rule3_falsifies`.

## 2. Measurement validity / controls

Preflight passed every gate (`raw/preflight.json`, `raw/controls.json`):

| Control | Expected | Observed | Verdict |
|---|---|---|---|
| `PC-ORACLE-EPISODE` | 5/5 task_success through the real scorer | 5/5 (2 steps each; revealed TARGET-42; terminal answer TARGET-42) | PASS |
| `NC-NO-MODEL-ACTION` | parseable 0.0, success 0.0 | parseable 0.0 (0/5), success 0.0 (0/5) | PASS |
| `B-RANDOM-ACTION` | parseable 1.0, success < 0.6 (served page) | parseable 1.0 (5/5), success 0.2 (1/5, seed-42) | PASS |
| `PC-JSON-CONSTRAINED-DECODING` | 10/10 per cell | 10/10 in all four cells | PASS |

The positive controls prove the decode path and the click-then-answer scoring path are live; the
null proves non-JSON is rejected; the random baseline proves chance does not clear the bar. All four
model cells are COMPLETE (PC gate 10/10 + exactly 5 episodes), 0 EXCLUDED, 0 PARTIAL.

Comparator cells are COMPLETE-and-VALID and reproduce the frozen parent anchor exactly
(task_success_rate 0/5, parseable_action_rate_step1 1.0, zero answer actions) →
**REPLICATION_ANCHOR_EXACT**. Interpretation is therefore not attributable to run-level drift.

## 3. Results

Stable metric ids per cell:

| Cell | PC pass | parseable@step1 | answer_action_emission | task_success | mean latency | mean tokens |
|---|---|---|---|---|---|---|
| M-7B-QWEN · P-TREAT-GOAL-SCHEMA | 1.0 (10/10) | 1.0 (5/5) | 0.0 (0/5) | 0.0 (0/5) | 6.2247 s | 15.0 |
| M-7B-QWEN · P-COMP-UNDERSPECIFIED | 1.0 (10/10) | 1.0 (5/5) | 0.0 (0/5) | 0.0 (0/5) | 6.2394 s | 15.0 |
| M-3B-QWEN · P-TREAT-GOAL-SCHEMA | 1.0 (10/10) | 1.0 (5/5) | 0.0 (0/5) | 0.0 (0/5) | 2.7325 s | 12.1429 |
| M-3B-QWEN · P-COMP-UNDERSPECIFIED | 1.0 (10/10) | 1.0 (5/5) | 0.0 (0/5) | 0.0 (0/5) | 2.7389 s | 12.1429 |

Capability bar: task_success_rate ≥ 0.6 **and** parseable_action_rate_step1 ≥ 0.6. No treatment
cell cleared. All latencies/tokens are over 35 model calls per cell (10 PC probes + 25 episode steps)
and are descriptive CPU-only cost observables, not part of the decision.

### Observed failure mode (all four cells identical in structure)

Every one of the 20 evaluated episodes:

- step 0: `{"action":"click","selector":"#reveal-btn"}` — `click_ok=true`, reveal fires,
  `revealed_value=TARGET-42`;
- steps 1–4: the model re-emits the **same** click on the now-hidden button (`click_ok=false`);
- no terminal answer action is ever emitted; `step_count=5`; `task_success=false`.

The treatment prompt adds the two attributes audit VF-01 named (a goal sentence and an enumerated
action schema) and does **not** leak `#reveal-btn` or `TARGET-42`, yet the trace is indistinguishable
from the comparator. The failure is therefore a post-reveal control/planning behavior
(re-clicking a hidden control instead of answering), not a step-0 discovery failure and not an
answer-parse failure.

## 4. Interpretation (bounded)

**FALSIFIES = the Director's bounded negative at the goal/schema protocol ceiling.** At the frozen
protocol, in the tested credential-free CPU-quantized Qwen2.5 3B–8B Q4_K_M class, supplying a
properly specified goal + action schema does **not** convert the step-0 reveal-click into a full
click-then-answer completion. Audit VF-01's prompt-underspecification hypothesis is **not**
sufficient to explain the parent failure mode: the recurrence is not caused by missing instruction
context at this model class. H1 is not supported; H1b attribution is not exercised (no cell cleared,
so the comparators are descriptive anchor replications, not a positive-effect contrast).

This closes the credential-free local 3B–8B path as a capability result under this task/harness,
not a prompt artifact, and does not satisfy readiness condition (3) by this model class. Per the
frozen negative consequence, the four-arm benchmark's credential-free path remains
DESIGN_COMPROMISED and the recorded endpoint receipts / re-scope set are Director decision inputs.
This packet does **not** pre-decide any re-scope.

Scope limits (also in `validity_notes`): single minimal task; one model family/quant; 5 seeded
deterministic episodes per cell; bundled treatment (goal vs schema vs phrasing not decomposed);
simplified text-DOM representation; packaging deviation for the 7B split shards (same repo/model/
quant, digest-verified). Failing this gate does not close other model classes, larger models,
hosted endpoints, or other domains.

## 5. Cost

CPU-only, no external API spend. Provisioning: ~6.8 GB GGUFs re-downloaded and digest-verified
fail-closed; llama-cpp-python 0.2.90 built from sdist; Playwright 1.63.0 + Chrome 154.0.8037.97
headless. Inference wall-clock: 7B cells ≈ 7 min each (≈3.6 min of it model load), 3B cells ≈ 4.3 min each;
total run including provisioning and controls well within the frozen 45–150 min estimate.

## 6. Artifacts and provenance

All raw per-cell evidence (`cells/*/*/raw/model_receipts.json`, `harness_config.json`), control and
preflight records (`raw/preflight.json`, `raw/controls.json`, `raw/materialized_configs.json`),
the derived decision (`raw/decision.json`), authored EXECUTE code and their sha256 are listed in
`result.json#artifacts`; run/commit/environment/models/commands are in `provenance.json`. Frozen
inputs and all five `freeze.artifact_hashes` were re-verified to match after EXECUTE. The
outcome-determining model invocation/parsing/scoring ran through the unmodified frozen parent runner
(`sha256 2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`).

## 7. Unresolved

- The goal+schema prompt did not convert the loop; the mechanism is not decomposed (goal-only vs
  schema-only vs phrasing vs longer-prompt).
- Why the model re-clicks the hidden button across all remaining steps instead of answering, even
  with the goal and answer action enumerated, remains open (small-model planning/state-tracking
  deficit vs residual prompt/harness effect).
- Larger (14B+) or non-Qwen CPU-quantized GGUFs and hosted endpoints are outside the frozen scope
  and untested.
- H1b (PROMPT_ATTRIBUTED) remains unmeasured because no treatment cell cleared.
