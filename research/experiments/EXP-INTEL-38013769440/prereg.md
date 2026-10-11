# EXP-INTEL-38013769440 preregistration (intel lane)

Experiment: EXP-INTEL-38013769440
Lane: intel
Target claim: C-LLM-INHERIT
Design contract: v2 (requires an independent PASS `design_review.json` before freeze)
Director mandate action: REOPEN (Global Research Director, cycle 38013054267)
Parent: EXP-INTEL-37982024058 (audit PASS; outcome FALSIFIES under the underspecified prompt)
Grandparent: EXP-INTEL-37973264582 (credential-free endpoints exist; Gate 2 failed at 0.5B/pollinations)

This preregistration is written BEFORE any outcome-bearing measurement of this experiment.
Only non-outcome-bearing satisfiability probes (static arithmetic, file/hash checks, a
no-model/no-browser simulation of the random baseline) were run at DESIGN time; they are
recorded verbatim in section 13. No candidate-model inference, episode, or success rate
for this experiment existed when this file was written.

--------------------------------------------------------------------------------
## 1. Purpose and decision

Resolve readiness condition (3) of the C-LLM-INHERIT program: whether at least one
credential-free, CPU-quantized local model can perform the minimal multi-step Web-agent
task (click a reveal button, then answer the revealed value) when the system prompt
enumerates the task goal and the action schema, or whether the credential-free path has a
capability ceiling below the bar.

Decision changed by this experiment:
- Positive (SUPPORTS): unblock the frozen four-arm C-LLM-INHERIT benchmark and hand off a
  verified credential-free endpoint (model + exact prompt + harness config). Readiness
  condition (3) satisfied by a proven same-model driver.
- Negative (FALSIFIES): close the credential-free same-model path and emit an explicit
  re-scope recommendation (drop the Gate 3 same-model external anchor). Readiness
  condition (3) resolved by re-scope.
- MEASUREMENT_INVALID: no capability verdict; the measurement transaction failed.

## 2. Inherited evidence (parent handoff, carry-forward; exact reference)

Source: `research/experiments/EXP-INTEL-37982024058/handoff.json`
(sha256 b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55).

ESTABLISHED (inherited, not re-litigated):
- Under the frozen underspecified prompt, constrained GBNF, temp=0, seeds 42-46, CPU-only
  llama.cpp 0.2.90, Qwen2.5 3B/7B Q4_K_M via huggingface.co resolve-redirect, no
  credential-free model cleared the bar; M-7B-QWEN 0/5, M-3B-QWEN 0/5 (audit PASS).
- Constrained decoding verified working: PC-JSON-CONSTRAINED-DECODING PASS 10/10 for both
  models; the task failure is planning under the frozen prompt, not formatting.
- Verification logic sound: NC-NO-MODEL-ACTION 0/5 parseable, 0/5 success.
- Prompt-sensitive failure mode: step-0 reveal-click succeeds (TARGET-42 enters PAGE_TEXT)
  and both models re-emit a click for the remaining steps; no answer action is emitted
  (audit VF-01).

REJECTED / BOUNDED (inherited): no general rejection of the credential-free path (a
prompt ablation was needed); the negative is bounded to the frozen 3B-8B Qwen class, the
frozen underspecified prompt, and the frozen minimal synthetic task.

UNKNOWN (this experiment addresses the first two): whether a goal/schema prompt converts
the step-0 click to a full click-then-answer (audit U-01); whether the failure is general
small-model multi-step planning or prompt-specific (U-02); whether 14B+/non-Qwen clear the
bar (U-03, out of scope); 7B split-shard provisioning stability across HF revisions (U-04).

DO-NOT-ASSUME (inherited): the FALSIFIES was at the frozen protocol ceiling only; the 7B
primary packaging deviated to same-quant split shards (VF-02); deterministic protocol gives
no variance estimate and the 3/5 rule is a pre-declared adequacy rule, not a significance
test (VF-03); the task text is present after reveal and representation loss does not explain
the loop (VF-04); C-LLM-INHERIT remains HYPOTHESIS and Gate 2 remains FAIL under the frozen
protocol.

## 3. Prerequisites

### 3.1 Models and GGUF artifacts (remote content, pinned by URL + sha256)

| candidate_id | model | quant | frozen artifact | sha256 (parent-pinned) |
|---|---|---|---|---|
| M-7B-QWEN | Qwen2.5-7B-Instruct | Q4_K_M | two same-repo split shards `qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf`, `-00002-of-00002.gguf` | `dfce12e3...` / `539cf93f...` (full digests in `research/experiments/EXP-INTEL-37982024058/raw/gguf_sha256.txt`) |
| M-3B-QWEN | Qwen2.5-3B-Instruct | Q4_K_M | `qwen2.5-3b-instruct-q4_k_m.gguf` (2,104,932,768 bytes) | `626b4a66...` (full digest in the same file) |

Route: `https://huggingface.co/<repo>/resolve/main/<file>` (confirmed 302 -> cdn). Only this
route is in scope; cdn-lfs/api-inference do not resolve in the factory.

PROVISIONING RULE: before a candidate is evaluated, locate matching-digest files (e.g. under
`/tmp/opencode/gguf/`) or download via the frozen URL, then sha256-verify against the
parent-pinned digest. A download failure or unresolved digest mismatch is a
`provisioning_failure` for that candidate: record the exact failure, continue with the
remaining candidate, and never substitute a different artifact. If BOTH candidates are
unprovisionable, OUTCOME=MEASUREMENT_INVALID.

### 3.2 Libraries, browser, hardware

- `llama-cpp-python==0.2.90` (pip install; parent-verified on the identical runner image).
- `playwright==1.63.0` + system Chrome at `/usr/bin/google-chrome` (headless, `--no-sandbox`;
  parent-verified, Chrome 154.0.8037.97).
- CPU-only, nproc=4, ~14 GB RAM, ~7 GB free disk for the two models. No GPU, no credential,
  no paid API.

Install/download/import failures are recorded as infrastructure failures and map to a frozen
MEASUREMENT_INVALID path, never to a capability verdict.

## 4. Treatments and comparator (the single varied dimension)

### 4.1 Treatment prompt P-TREAT-GOAL-SCHEMA (`prompts.system`)

Derived from the grandparent SYS constant in
`research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py` (bound in
freeze_artifacts) with the single field-name adaptation `ref` -> `selector` required by the
parent task schema. It adds exactly the two dimensions audit VF-01 says the parent prompt
lacked: (a) enumeration of the action schema and (b) the task goal sentence. It does NOT
leak `#reveal-btn` or `TARGET-42`.

Provenance caveat: the grandparent harness DEFINES this prompt shape, but its own Gate 2
FAILED (`comparator_web_agent_tasks_completed_under_identical_model: 0` in
`research/experiments/EXP-INTEL-37973264582/result.json`), so the grandparent is cited only
as the provenance of P_treat, NOT as evidence that this prompt converts the task. Whether it
does is the open question this experiment measures.

Verbatim string (this is the exact `prompts.system` value for the treatment config):

```
You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<id>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it.
```

### 4.2 Comparator prompt P-COMP-UNDERSPECIFIED (`prompts.system`)

Byte-identical to the frozen parent system prompt (the bound fixture
`research/experiments/EXP-INTEL-37982024058/raw/harness_config.json#prompts.system`):

```
You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.
```

### 4.3 Single-variable justification

Treatment and comparator differ in EXACTLY one field: `prompts.system`. Task page,
`prompts.user_template`, `prompts.positive_control_probe`, GBNF grammar, action schema,
sampling (temperature=0.0, max_tokens=512, n_ctx=2048, chat_format=qwen, llama_seed=42,
episode seeds 42-46), `max_steps_per_episode=5`, threshold `TARGET-42`, harness, and scoring
are byte-identical. The paired comparator is collected within THIS packet for every
evaluated candidate (section 9, Phase A step A3) so the prompt is identified as the driver
locally, without importing the parent's un-remeasured narrative.

## 5. Task, fixture and per-condition configs

Task (`FIX-CFG-EXP-INTEL-38013769440-*`): `MIN-WEBAGENT-CLICK-REVEAL-ANSWER`. The page is the
frozen synthetic page from the bound parent fixture: a visible `#reveal-btn` button, a hidden
`#target` div containing `TARGET-42`, and a click handler that reveals `#target` and hides
the button. Success is mechanical: `clicked_reveal AND revealed_value=="TARGET-42" AND
final_answer=="TARGET-42"`, with terminal page-state re-verification.

EXECUTE transcribes three configs from the bound fixture template (all fields byte-identical
to the template except the noted ones; the parent fixture is reused unmodified as the
template):

1. `raw_controls/raw/harness_config.json` — `fixture_id=FIX-CFG-EXP-INTEL-38013769440-CONTROLS`,
   `source` updated; `prompts.system` irrelevant (all control producers are scripted).
2. `raw_treatment/raw/harness_config.json` — `fixture_id=FIX-CFG-EXP-INTEL-38013769440-TREAT`,
   `source` updated, `prompts.system` := the verbatim string in 4.1.
3. `raw_comparator/raw/harness_config.json` — `fixture_id=FIX-CFG-EXP-INTEL-38013769440-COMP`,
   `source` updated (`prompts.system` already equals 4.2).

Each transcribed config is sha256-recorded in `result.json.artifacts` and `provenance.json`.

## 6. Controls and preflight (run BEFORE any candidate inference)

All controls run against the SAME served task page and through the SAME `run_episode` scorer
used by the candidate arms, via the frozen controls driver (Appendix A). This repairs the
parent control-sensitivity defect: the parent's `null-random` mode scored NC and B-RANDOM on
an un-navigated `about:blank` page because `run_episode` reloads `page.url` and that mode
never navigated to the served port; the repaired driver navigates to the served task page.

Control driver invocation (per condition):
`python3 research/intel/run_exp_38013769440_controls.py --outdir <EXP_DIR>/raw_controls --harness research/intel/run_exp_37982024058.py`

| control id | scripted producer | expected | role |
|---|---|---|---|
| PC-ORACLE-EPISODE | click `#reveal-btn` at step 0, answer `TARGET-42` thereafter | 5/5 `task_success`, 5/5 step-1 parseable | scorer-path canary; if < 5/5 the scoring pipeline is broken -> MEASUREMENT_INVALID |
| NC-NO-MODEL-ACTION | fixed non-JSON content `I will click the button` | 0.0 step-1 parseable, 0.0 success | verifies non-parseable actions are rejected and success cannot be awarded accidentally |
| B-RANDOM-ACTION | uniform choice over the frozen 5-action space, one `random.Random(42)` reused across the 5 episodes | 1.0 step-1 parseable, `task_success_rate < 0.6` | negative baseline; a chance policy must not clear the bar |

B-RANDOM chance arithmetic (design-time): per-episode success requires clicking `#reveal-btn`
at step 0 and then drawing `answer TARGET-42` before any other answer within 5 steps, giving
an i.i.d. per-episode probability p = 156/3125 = 0.04992. Hence
P(task_success_rate >= 3/5) ~= 1.15e-3. A static no-model/no-browser simulation of the
frozen seeded stream (section 13) yields exactly 1/5 = 0.2 for the realized run. The 3/5 bar
is unreachable by the frozen random baseline.

PC-JSON-CONSTRAINED-DECODING (gate, ID inherited from the parent) is run inside the parent
harness per candidate per prompt condition: 10 probes of
`Emit exactly: {"action":"click","selector":"#test"}` must all be schema-valid (10/10).

Preflight failure -> OUTCOME=MEASUREMENT_INVALID (never a capability verdict):
- PC-ORACLE-EPISODE < 5/5, or
- NC step-1 parseable != 0.0 or NC success != 0.0, or
- B-RANDOM success >= 0.6.

## 7. Measurement procedure (EXECUTE)

All model-backed measurement uses the UNMODIFIED parent harness
`research/intel/run_exp_37982024058.py` (sha256 bound in freeze_artifacts). Per candidate
`<ID>` and condition `<COND>` in {treatment, comparator}:

```
python3 research/intel/run_exp_37982024058.py --mode probe-candidate \
  --outdir research/experiments/EXP-INTEL-38013769440/raw_<COND> \
  --candidate <ID> --gguf <verified gguf path(s)> --chrome /usr/bin/google-chrome
```

The harness runs PC-JSON (10 probes) then, on PC pass, 5 episodes with seeds 42..46 and
writes `raw/model_receipts.json` (per-episode raw completions, parsed actions, `click_ok`,
reveal detection, `final_answer`, step counts, latency, completion tokens). No early stop
within a model: all 5 episodes are the frozen unit. Derive for each cell:
`task_success_rate` (k/5), `parseable_action_rate_step1`, `answer_action_emission_rate`
(fraction of episodes emitting at least one valid answer action), mean latency and mean
completion tokens.

Evaluation order per section 9 (M-7B-QWEN first; stop once a candidate clears under
treatment; the comparator cell of an evaluated candidate is always collected).

## 8. Bounded external capability check (informational, non-gating)

### 8.1 Scope and budget

Time-boxed to <= 30 minutes of design-type search (websearch + archived leaderboards / model
cards), performed AFTER the local outcome is fixed (Phase B). Purpose: bound the "ALL
credential-free endpoints actually available" ceiling statement and prevent an unbounded
model census. It must not alter OUTCOME or the frozen thresholds.

### 8.2 Structured output schema

Record `metrics.external_capability_envelope` as a list of
`{"model_family","size","source_url","task_class","evidence_type":"published_leaderboard|model_card|paper|forum","clears_equal_or_harder_web_agent_task":true|false|null,"local_credential_free":true|false|null,"notes"}`.
`null` is used when the source does not state the field; unknown entries are retained and
never silently dropped.

### 8.3 Mapping to the close/re-scope recommendation

- SUPPORTS (local positive): recommend unblocking the four-arm C-LLM-INHERIT benchmark with
  the verified endpoint; external check is context only.
- FALSIFIES and no envelope entry credibly clears an equal-or-harder multi-step Web-agent
  task: recommend re-scoping the four-arm benchmark off the credential-free path (drop the
  Gate 3 same-model external anchor; internally re-run comparators on a dynamic-range task
  bank where cold/retrieval arms are not at ceiling, per the B2 precedent).
- FALSIFIES but the envelope flags a specific credible credential-free model: recommend a
  bounded follow-up (provision + same frozen protocol) before closing, named explicitly in
  `unresolved`.

## 9. Decision rule and outcomes

OUTCOME in {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID}; separate secondary
`prompt_attribution` in {PROMPT_ATTRIBUTED, NOT_PROMPT_ATTRIBUTED, UNDETERMINED}.

Preflight (section 6) -> Provisioning (3.1) -> Phase A (order M-7B-QWEN, then M-3B-QWEN):
- A1: PC-JSON under P_treat; < 10/10 -> exclude candidate (decoding_infrastructure_failure),
  record, next candidate.
- A2: 5 task episodes under P_treat -> T(m)=task_success_rate, P1(m)=step-1 parseable rate,
  plus answer_action_emission_rate.
- A3: 5 task episodes under P_comp for the SAME candidate, ALWAYS and before A4 -> C(m).
- A4: if T(m) >= 0.6 AND P1(m) >= 0.6 -> capability CLEARED: OUTCOME=SUPPORTS,
  status=COMPLETE. If C(m) < 0.6 -> prompt_attribution=PROMPT_ATTRIBUTED; if C(m) >= 0.6 ->
  prompt_attribution=NOT_PROMPT_ATTRIBUTED with a mandatory validity note. STOP.
- A5: else record not-cleared, next candidate.
Phase B (both candidates exhausted/excluded, at least one evaluated on task, none cleared):
- B1 external check (section 8); B2 prompt_attribution=UNDETERMINED; B3 OUTCOME=FALSIFIES,
  status=COMPLETE.

MEASUREMENT_INVALID only if: every candidate excluded at PC; or a preflight control fails; or
both candidates unprovisionable. MEASUREMENT_INVALID is not a capability verdict. The
external envelope never changes OUTCOME. If PC excludes exactly one candidate and the other
is evaluated but does not clear, OUTCOME=FALSIFIES with a validity note naming the excluded
candidate (partial coverage, not MIXED).

Threshold note: 3/5 = 0.6 exactly; the bar is inherited from the parent
(`clearing_threshold.task_success_rate_min=0.6`, `episodes=5`) and is a pre-declared
operational adequacy rule, not a significance test (parent VF-03). It is neither at ceiling
(parent comparator 0/5) nor at floor (oracle canary 5/5).

## 10. Metrics and analysis

Stable metric ids: `parseable_action_rate_step1`, `task_success_rate`,
`answer_action_emission_rate`, `mean_inference_latency_s`, `mean_completion_tokens`,
`positive_control_pass_rate`.

| cell | P_treat | P_comp |
|---|---|---|
| M-7B-QWEN | T(7B), P1(7B), answer-rate, cost | C(7B), cost |
| M-3B-QWEN (only if 7B does not clear) | T(3B), P1(3B), answer-rate, cost | C(3B), cost |

Primary endpoint: `task_success_rate` under P_treat. Secondary: the paired comparator
`task_success_rate` (attribution) and `answer_action_emission_rate`. Cost is reported per arm
(calls, tokens, latency) with identical budgets across arms.

Claim update (advisory only; DIRECTOR adjudicates): SUPPORTS -> recommend
C-LLM-INHERIT event `EXPERIMENTAL` (readiness (3) cleared by a proven same-model driver,
bounded to credential-free Qwen 3B/7B Q4_K_M, goal/schema prompt, deterministic protocol);
FALSIFIES -> recommend keeping C-LLM-INHERIT `HYPOTHESIS` and record the credential-free
same-model path as closed at this ceiling with an explicit re-scope. Never `SUPPORTED`/
`PARTIAL` as a registry status.

## 11. Validity threats and mitigations

- **Deterministic protocol / no variance:** temp=0, fixed seeds -> 5/5 uniform traces likely;
  the 3/5 rule is an adequacy rule, not a significance test (VF-03). Mitigation: report each
  cell as k/5 and do not attach p-values.
- **Representation loss:** the observation string truncates page text to 300 chars; after
  reveal, PAGE_TEXT contains TARGET-42 (VF-04). It does not explain the re-click loop.
- **System-prompt attentiveness:** if the model ignores system content, the two prompt cells
  collapse; this is itself the measured question, and the comparator cell makes the collapse
  visible rather than assumed.
- **Provisioning drift:** shard set / HF revision drift (U-04). Mitigation: sha256
  verification before load; mismatch -> provisioning_failure.
- **Control-sensitivity defect repaired:** see section 6; the parent's structural 0/5 is not
  inherited as if it were a chance baseline.
- **Prompt leakage:** P_treat contains neither `#reveal-btn` nor `TARGET-42`.
- **External check is not local evidence:** labeled informational and non-gating.

## 12. Consequences

Positive: readiness condition (3) satisfied; four-arm C-LLM-INHERIT benchmark unblocked at
zero new infrastructure; audit VF-01 retired with evidence; C-RESIDUAL-NOVELTY and
C-PRODUCT-ECON regain an executable substrate.

Negative: credential-free 3B-8B GGUF path closed at this ceiling; U-01/U-02 closed; explicit
close/re-scope recommendation emitted; C-LLM-INHERIT stays HYPOTHESIS until a re-scoped
design is approved.

MEASUREMENT_INVALID: no capability statement; report the exact failed prerequisite and the
smallest unblocking action.

## 13. Design-time non-outcome-bearing satisfiability probes

1. Static B-RANDOM simulation (no model, no browser): replayed the frozen action space with a
   single `random.Random(42)` across 5 episodes, mirrored the `run_episode` success
   condition, and obtained `[True, False, False, False, False]` -> `task_success_rate=0.2`.
   Independent re-seeds 42..46 give `[True, True, False, False, False]`; neither equals the
   shared-stream realization. Exact i.i.d. p = 156/3125 = 0.04992; P(>=3/5) = 1.15e-3. The
   bar is unreachable by the frozen baseline.
2. Arithmetic: 3/5 = 0.6 exactly; the threshold is attainable, not at ceiling/floor.
3. File/hash checks: bound artifacts exist; `run_exp_37982024058.py` sha256
   `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`; parent fixture
   `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`;
   `min_webagent.py` sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`.
4. Prompt provenance: `min_webagent.py` SYS constant confirmed verbatim (line 16-18);
   P_treat differs only by `ref` -> `selector`.
5. Control-driver syntax parse: `ast.parse` succeeded; the driver imports only the bound
   harness. Its materialized sha256 must equal
   `3865258d43807ef7bf24fdc8666b251b1273badafbbdfd179979af1446b42d7b` (Appendix A).

No candidate-model inference or task outcome was observed in DESIGN.

## 14. Claim handling and non-promotion

This experiment is Intel provisioning/capability research. It may recommend a bounded claim
event but must not self-promote C-LLM-INHERIT or any other claim. Registry statuses remain
DIRECTOR-owned. `UNKNOWN`/`MEASUREMENT_INVALID`/`FALSIFIES` are valid and are not failures of
execution quality.

## 15. Reproduction and artifact binding

Bound by `freeze.json.artifact_hashes` (existing files):
- `research/intel/run_exp_37982024058.py` (harness, reused unmodified)
- `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (fixture template;
  supplies P-COMP)
- `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py` (P-TREAT derivation
  source)

EXECUTE-time materializations fully determined by this packet (sha256-recorded):
- `raw_controls/raw/harness_config.json`, `raw_treatment/raw/harness_config.json`,
  `raw_comparator/raw/harness_config.json` (section 5)
- `research/intel/run_exp_38013769440_controls.py` (Appendix A; expected sha256
  `3865258d43807ef7bf24fdc8666b251b1273badafbbdfd179979af1446b42d7b`; mismatch ->
  MEASUREMENT_INVALID)

--------------------------------------------------------------------------------
## Appendix A — frozen controls driver source (verbatim) and expected sha256

EXECUTE must materialize exactly the bytes below at
`research/intel/run_exp_38013769440_controls.py` (the content between the fences, including
the final newline). Expected sha256:
`3865258d43807ef7bf24fdc8666b251b1273badafbbdfd179979af1446b42d7b`.

```python
#!/usr/bin/env python3
"""Frozen preflight-controls driver for EXP-INTEL-38013769440 (intel lane).

Source is frozen verbatim in prereg.md Appendix A, which is hashed by freeze.json, and
its expected sha256 is frozen in prereg.md Appendix A and spec.json
freeze_eligibility.freeze_artifacts_bound. EXECUTE must materialize it byte-identically at
  research/intel/run_exp_38013769440_controls.py

It exercises PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION and B-RANDOM-ACTION through the
UNMODIFIED parent harness EXP-INTEL-37982024058 (navigated page path), so the three
controls are sensitive to the exact scorer that will grade the model arms. It performs
no scientific interpretation.
"""
import argparse
import importlib.util
import json
import os
import random
import sys


def load_harness(path):
    spec = importlib.util.spec_from_file_location("h37982024058", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--harness", required=True)
    ap.add_argument("--chrome", default="/usr/bin/google-chrome")
    args = ap.parse_args()

    h = load_harness(args.harness)
    cfg = h.load_config(args.outdir)
    rawdir = os.path.join(args.outdir, "raw")
    os.makedirs(rawdir, exist_ok=True)
    n = cfg["clearing_threshold"]["episodes"]
    threshold = cfg["task"]["threshold_target_text"]
    max_steps = cfg["task"]["max_steps_per_episode"]

    out = {}
    srv, port = h.start_page_server(cfg["task"]["page_html"])
    try:
        with h.sync_playwright() as p:
            b = p.chromium.launch(executable_path=args.chrome, headless=True, args=["--no-sandbox"])
            page = b.new_page()

            def oracle_prod(obs, step):
                if step == 0:
                    act = {"action": "click", "selector": "#reveal-btn"}
                else:
                    act = {"action": "answer", "text": threshold}
                return json.dumps(act), 0.0, 0, {"kind": "oracle"}

            oracle_eps = []
            for ep in range(n):
                r = h.run_episode(page, "", "", max_steps, oracle_prod, threshold=threshold)
                r["episode"] = ep
                oracle_eps.append(r)
            out["PC-ORACLE-EPISODE"] = {
                "control_id": "PC-ORACLE-EPISODE",
                "episodes": oracle_eps,
                "parseable_action_rate_step1": sum(1 for e in oracle_eps if e["step1_parse_ok"]) / len(oracle_eps),
                "task_success_rate": sum(1 for e in oracle_eps if e["task_success"]) / len(oracle_eps),
                "criterion": "5/5 success",
            }

            nc = cfg["null_control"]
            null_prod = h.make_null_producer(nc["fixed_invalid_content"])
            nc_eps = []
            for ep in range(nc["episodes"]):
                r = h.run_episode(page, "", "", max_steps, null_prod, threshold=threshold)
                r["episode"] = ep
                nc_eps.append(r)
            out["NC-NO-MODEL-ACTION"] = {
                "control_id": nc["id"],
                "episodes": nc_eps,
                "parseable_action_rate_step1": sum(1 for e in nc_eps if e["step1_parse_ok"]) / len(nc_eps),
                "task_success_rate": sum(1 for e in nc_eps if e["task_success"]) / len(nc_eps),
                "criterion": nc["success_criterion"],
            }

            rb = cfg["random_baseline"]
            rng = random.Random(cfg["sampling"]["base_seed"])
            rand_prod = h.make_random_producer(rb["action_space"], rng)
            rand_eps = []
            for ep in range(rb["episodes"]):
                r = h.run_episode(page, "", "", max_steps, rand_prod, threshold=threshold)
                r["episode"] = ep
                rand_eps.append(r)
            out["B-RANDOM-ACTION"] = {
                "baseline_id": rb["id"],
                "episodes": rand_eps,
                "parseable_action_rate_step1": sum(1 for e in rand_eps if e["step1_parse_ok"]) / len(rand_eps),
                "task_success_rate": sum(1 for e in rand_eps if e["task_success"]) / len(rand_eps),
            }
            b.close()
    finally:
        srv.shutdown()

    with open(os.path.join(rawdir, "control_episodes.json"), "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(json.dumps({
        "PC_oracle_success": out["PC-ORACLE-EPISODE"]["task_success_rate"],
        "NC_parseable_step1": out["NC-NO-MODEL-ACTION"]["parseable_action_rate_step1"],
        "NC_success": out["NC-NO-MODEL-ACTION"]["task_success_rate"],
        "RANDOM_parseable_step1": out["B-RANDOM-ACTION"]["parseable_action_rate_step1"],
        "RANDOM_success": out["B-RANDOM-ACTION"]["task_success_rate"],
    }))


if __name__ == "__main__":
    sys.exit(main())
```

## Appendix B — parent handoff carry-forward (verbatim reference)

See `research/experiments/EXP-INTEL-37982024058/handoff.json`
(sha256 b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55), categories
`carry_forward.established`, `carry_forward.rejected`, `carry_forward.unknown`,
`carry_forward.do_not_assume`, reproduced in section 2. `handoff.next_question` is treated as
continuity evidence only; the binding direction is the Director mandate (REOPEN,
C-LLM-INHERIT).
