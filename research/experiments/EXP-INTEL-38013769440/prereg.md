# EXP-INTEL-38013769440 Preregistration

**Experiment ID**: EXP-INTEL-38013769440
**Lane**: intel
**Target Claim**: C-LLM-INHERIT
**Director Mandate**: REOPEN (global-director-REOPEN, cycle_id=38013054267)
**Parent Handoff**: EXP-INTEL-37982024058 (sha256: b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55)
**Design Contract Version**: 2

---

## 1. Strategic Context

The Global Research Director has mandated a REOPEN action on claim C-LLM-INHERIT. The parent experiment EXP-INTEL-37982024058 (audit PASS, outcome FALSIFIES) established under the frozen underspecified protocol:

- **Gate 0 PASS**: Credential-free endpoints exist (local GGUF via huggingface.co resolve-redirect).
- **Gate 1 PASS**: Constrained decoding infrastructure verified (PC-JSON-CONSTRAINED-DECODING 10/10 for both M-7B-QWEN and M-3B-QWEN).
- **Gate 2 FAIL**: Neither model cleared the minimal Web-agent capability bar (task_success_rate=0.0, 0/5 episodes each). Both models executed step-0 reveal-click successfully, then entered a re-click loop on the hidden button, never emitting an answer action.
- **Audit VF-01**: Identified prompt underspecification as the likely driver — the frozen system prompt enumerated neither the action schema nor the task goal ('click the button, then answer the revealed code'), unlike the parent harness EXP-INTEL-37973264582 SYS prompt which did.

The frozen four-arm C-LLM-INHERIT benchmark (COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER, same model/tools/budget) remains **not executable as specified**. The binding blocker is a **Web-agent-capable credential-free model**. The Director's strategic question:

> Under the same credential-free, CPU-quantized constraints, does supplying the task goal/schema in the system prompt (removing the underspecification the parent harness did not have) convert the step-0 reveal-click into a full multi-step click-then-answer completion for the largest obtainable credential-free models, and if not, what is the demonstrable capability ceiling for the minimal Web-agent task across ALL credential-free endpoints and local models actually available to the factory? Return an explicit close/re-scope recommendation so that readiness condition (3) is either satisfied by a proven same-model driver or the four-arm C-LLM-INHERIT benchmark is re-scoped off the credential-free path. Include a bounded external check of the published capability envelope for comparably sized local models.

This experiment is a **bounded prompt ablation** (treatment = goal/schema-enriched system prompt; comparator = frozen underspecified prompt) plus a **bounded external capability ceiling check**. Both directions are decision-changing.

---

## 2. Hypothesis and Falsifier

**Hypothesis (H1)**: At least one of M-7B-QWEN or M-3B-QWEN will clear the minimal Web-agent capability bar (task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6) when the system prompt enumerates the task goal and action schema, converting the parent's FALSIFIES outcome to SUPPORTS at the goal/schema prompt protocol and unblocking the frozen C-LLM-INHERIT four-arm benchmark.

**Falsifier (H0)**: Even with the goal/schema-enriched system prompt, neither M-7B-QWEN nor M-3B-QWEN clears the capability bar. The capability ceiling for credential-free CPU-quantized models under factory constraints is below the minimal Web-agent task threshold. A bounded external check of published benchmarks for Qwen2.5-3B/7B-Instruct and comparable local models on Web-agent/tool-use tasks confirms no accessible credential-free model clears this bar, licensing an explicit re-scope of the four-arm benchmark off the credential-free path.

**Both-directions outcome**: Either outcome is decision-changing. SUPPORTS unblocks the flagship benchmark. FALSIFIES + external ceiling confirmation closes the credential-free path and forces an accountable re-scope.

---

## 3. Candidate Model Set (FROZEN — No Post-Freeze Additions)

| Candidate ID | Model | Quant | Est. Size | Download Route | Chat Format |
|--------------|-------|-------|-----------|----------------|-------------|
| **M-7B-QWEN** (primary) | Qwen2.5-7B-Instruct-Q4_K_M.gguf | Q4_K_M | ~4.1 GB (split shards) | huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf + -00002-of-00002.gguf | "qwen" |
| **M-3B-QWEN** (fallback) | Qwen2.5-3B-Instruct-Q4_K_M.gguf | Q4_K_M | ~1.9 GB | huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf | "qwen" |

**Constraints**:
- Download ONLY via `huggingface.co` resolve-redirect (confirmed working: redirects to `us.aws.cdn.hf.co`).
- `cdn-lfs.huggingface.co` and `api-inference.huggingface.co` do NOT resolve in this factory (parent evidence).
- No GPU available (CPU-only, nproc=4).
- `llama-cpp-python==0.2.90` (parent-verified version).
- Models tested in sequence: M-7B-QWEN first. If it clears the bar under treatment, stop (early success). If it fails treatment, test M-3B-QWEN under treatment.
- **Each model tested under TWO prompt conditions**: (A) Treatment = goal/schema-enriched system prompt; (B) Comparator = frozen underspecified system prompt (re-run for direct within-experiment comparison).

---

## 4. System Prompts (FROZEN)

### 4.1 Treatment Prompt (Goal/Schema-Enriched)
```
You are a web agent. Your task is to click the button with id 'reveal-btn', then answer the revealed target value 'TARGET-42'.

Valid actions (JSON only):
- Click: {"action": "click", "selector": "#reveal-btn"}
- Answer: {"action": "answer", "text": "TARGET-42"}

Reply with ONLY a valid JSON action per the schema above. No prose, no reasoning, no markdown.
```

### 4.2 Comparator Prompt (Frozen Underspecified from Parent)
```
You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.
```

**Note**: The comparator prompt is identical to `harness_config.json` `"prompts": {"system": "..."}` from EXP-INTEL-37982024058. It is re-run in this experiment (5 episodes per model, seeds 42-46) for direct within-experiment comparison.

---

## 5. Minimal Web-Agent Task (Identical to Parent Gate 2)

**Task Definition**: "Click the element with id `reveal-btn`, then answer the revealed target value `TARGET-42`."

**Environment**: Single synthetic HTML page served locally via Python HTTP server (identical to parent `harness_config.json` `task.page_html`).

**Action Schema** (enforced by GBNF constrained decoding, identical to parent):
```json
{
  "action": "click" | "answer",
  "selector": "string (required for click)",
  "text": "string (required for answer)"
}
```

**Episode Protocol**:
1. Model receives system prompt (treatment OR comparator).
2. Model receives user prompt with current page state (simplified text representation, identical to parent `user_template`).
3. Model emits ONE action (constrained by GBNF).
4. Harness parses JSON, executes via Playwright, returns new page state.
5. Repeat until model emits `{"action":"answer","text":"TARGET-42"}` or max 5 steps reached.
6. Success = model emits valid click action on `#reveal-btn` THEN valid answer action with `text="TARGET-42"`.

**Parsing Rule**: Action must be valid JSON matching the schema exactly. Any parse error, schema violation, or missing required fields = parse failure.

---

## 6. Controls and Baselines

### Positive Control: PC-JSON-CONSTRAINED-DECODING
- **Purpose**: Verify constrained decoding infrastructure works for each candidate model under the TREATMENT prompt condition before task evaluation. (Comparator prompt PC is run for reference evidence but is not decision-critical.)
- **Protocol**: 10 probes per model under treatment system prompt with prompt: `Emit exactly: {"action":"click","selector":"#test"}`
- **Success Criterion**: 10/10 syntactically valid JSON matching schema.
- **Failure Mode**: If positive control fails for a model under the TREATMENT prompt condition, that model is excluded from treatment evaluation (decoding infrastructure failure, not model capability). If BOTH candidates fail positive control under treatment -> OUTCOME=MEASUREMENT_INVALID.

### Null Control: NC-NO-MODEL-ACTION
- **Purpose**: Confirm task verification logic correctly rejects non-parseable actions.
- **Protocol**: Harness runs 5 episodes with a fixed script emitting invalid content (`"I will click the button"` — no JSON).
- **Success Criterion**: 0% task completion, 0% parseable JSON actions.

### Negative Baseline: B-RANDOM-ACTION
- **Purpose**: Establish chance-level parseable action rate and task completion rate.
- **Protocol**: Uniform random action selection from valid action space (5 actions: click #reveal-btn, answer TARGET-41/42/43/unknown). 5 episodes.
- **Expected**: parseable_action_rate_step1=1.0 (valid JSON by construction), task_success_rate near zero.

### Carried Reference Baselines (Not Re-run)
- **B-0.5B-QWEN-LOCAL**: Qwen2.5-0.5B-Instruct-Q4_K_M (parent E-LOCAL-LLAMA). Expected: 0% parseable actions, 0% task success.
- **B-POLLINATIONS-PROXY**: Pollinations gpt-oss-20b (parent E-POLLINATIONS-OPENAI). Expected: 0% task success (token cap, empty content, budget instability).

### Protocol Comparators (Re-run from Parent)
- **B-UNDERSPECIFIED-PROMPT-7B**: M-7B-QWEN under frozen underspecified prompt. Parent result: task_success_rate=0.0, parseable_action_rate_step1=1.0, answer_action_emission_rate=0.0.
- **B-UNDERSPECIFIED-PROMPT-3B**: M-3B-QWEN under frozen underspecified prompt. Parent result: task_success_rate=0.0, parseable_action_rate_step1=1.0, answer_action_emission_rate=0.0.

---

## 7. Measurement Protocol

### Per-Model Per-Prompt Evaluation Sequence
1. **Download & Verify**: Download GGUF via huggingface.co resolve-redirect. Verify sha256 at download time.
2. **Load Model**: `Llama(model_path=GGUF, n_ctx=2048, verbose=False, chat_format="qwen", seed=42)`. Record load time.
3. **Positive Control (Treatment Prompt)**: Run 10 constrained-decoding probes with treatment system prompt. Record pass rate. If < 10/10 -> model excluded from treatment evaluation.
4. **Task Episodes (Treatment Prompt)**: Run 5 episodes of minimal Web-agent task with treatment system prompt.
   - Temperature=0.0, max_tokens=512, seed=42+episode_idx.
   - Constrained decoding via GBNF grammar for action schema.
   - Record per-episode: raw completion, parsed action (or parse error), step count, task success (bool), token usage, latency, **answer_action_emitted** (bool).
5. **If Treatment Fails** (model evaluated on task but did not clear bar): Run positive control + 5 task episodes under COMPARATOR prompt (seeds 42-46) for direct within-experiment comparison.
6. **Aggregate Metrics**: Parseable action rate (step 1), task success rate (5 episodes), answer_action_emission_rate, mean latency, mean tokens, positive_control_pass_rate (treatment).

### Primary Metrics (Stable Identifiers for Downstream)
- `parseable_action_rate_step1`: Fraction of episodes where step 1 action is valid JSON matching schema.
- `task_success_rate`: Fraction of 5 episodes where model completes full task (click then answer TARGET-42).
- `answer_action_emission_rate`: Fraction of episodes where model emits at least one `answer` action (diagnostic for VF-01 loop).
- `mean_inference_latency_s`: Mean wall-time per model call.
- `mean_completion_tokens`: Mean tokens per completion.
- `positive_control_pass_rate`: Fraction of 10 probes with valid JSON (per prompt condition).
- `external_capability_envelope`: Structured findings from bounded external check (see Section 8).

### Success Threshold (Per Model Under Treatment)
**Model CLEARS capability bar** iff: `task_success_rate >= 0.6` (>= 3/5 episodes) AND `parseable_action_rate_step1 >= 0.6` (>= 3/5 episodes).

Rationale: 3/5 is the smallest majority above chance that survives binomial exact test (p=0.5, n=5, k>=3 -> p=0.5). This is a minimal but non-trivial threshold for a capability gate.

---

## 8. Bounded External Capability Check

**Scope**: Systematic search of published benchmarks for Qwen2.5-3B/7B-Instruct and comparable local models (Llama-3.2-3B/8B, Gemma-2-2B/9B, Phi-3.5-mini) on multi-step Web-agent or tool-use tasks.

**Sources to Search** (bounded list, searched in order until ceiling established or time bound hit):
1. WebArena leaderboard / publications
2. Mind2Web leaderboard / publications
3. MiniWoB++ / MiniWoB results for small models
4. τ-bench (τ-agent) results
5. AgentBench (Web/Tool subsets)
6. BMTools / ToolBench / API-Bank small-model results
7. HuggingFace Open LLM Leaderboard (tool-use / function-calling subset)
8. GAIA benchmark small-model submissions
9. WebShop benchmark small-model results
10. Recent (2024-2026) arXiv/Conference papers on small-model Web agents

**Search Protocol**:
- Search each source for model names: "Qwen2.5-3B", "Qwen2.5-7B", "Llama-3.2-3B", "Llama-3.2-8B", "Gemma-2-2B", "Gemma-2-9B", "Phi-3.5-mini" + keywords "Web agent", "tool use", "function calling", "browser", "WebArena", "Mind2Web".
- Time bound: 30 minutes wall-clock maximum.
- Record: source URL, access date, benchmark name, model, task subset, metric (success rate, pass@k, etc.), numeric result, whether credential-free/local inference.
- **Ceiling criterion**: If ANY source reports a credential-free/local inference result for a 3B-8B class model clearing a multi-step Web-agent task with success rate >= 0.6 on a task of comparable or greater complexity than MIN-WEBAGENT-CLICK-REVEAL-ANSWER, record as `ceiling_above_bar = true` with evidence. If all searched sources report failure or no results for all models within time bound, record `ceiling_above_bar = false` with evidence summary and `search_exhaustive = false` if time bound hit before completing all sources.
- Output: structured JSON `external_capability_envelope` with fields: `search_timestamp`, `sources_searched`, `findings[]`, `ceiling_above_bar`, `search_exhaustive`, `ceiling_summary`.

---

## 9. Decision Rule (Formal)

Let `M_i` be the i-th candidate model tested in order (M-7B-QWEN, then M-3B-QWEN).
Let `P_treat` = treatment prompt (goal/schema-enriched), `P_comp` = comparator prompt (frozen underspecified).

For each `M_i`:
1. Run `PC-JSON-CONSTRAINED-DECODING` under `P_treat`. If `pass_rate < 1.0` (10/10): **EXCLUDE** `M_i` from treatment evaluation, continue to `M_{i+1}`. Log as `decoding_infrastructure_failure`.
2. Else evaluate 5 task episodes under `P_treat`.
3. If `task_success_rate(M_i, P_treat) >= 0.6` AND `parseable_action_rate_step1(M_i, P_treat) >= 0.6`: **OUTCOME = SUPPORTS**. Stop testing further models. **Status = COMPLETE**.
4. Else: Continue to `M_{i+1}`.

After all candidates exhausted under treatment:
5. If **ALL candidates were excluded at positive control** (zero models evaluated on task): **OUTCOME = MEASUREMENT_INVALID**. **Status = COMPLETE**. (validity_notes explaining decoding infrastructure failure).
6. Else (at least one model evaluated on task, none cleared bar):
   a. Run comparator prompt `P_comp` for all candidates (5 episodes each, seeds 42-46) for direct within-experiment comparison.
   b. Execute bounded external capability check (Section 8).
   c. If `external_capability_envelope.ceiling_above_bar == false`: **OUTCOME = FALSIFIES**. **Status = COMPLETE**.
   d. If `external_capability_envelope.ceiling_above_bar == true`: **OUTCOME = MIXED** (treatment fails for tested models but bounded external evidence suggests capability ceiling above bar for other accessible models). **Status = COMPLETE**. Handoff must recommend investigating the specific external model/benchmark.

---

## 10. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Constrained decoding masks model reasoning** | Positive control isolates decoding; task uses same GBNF. If positive control passes but task fails, failure is reasoning/planning, not formatting. |
| **Prompt ablation not the true cause** | Comparator prompt re-run in same experiment (same seeds, same infrastructure). Direct within-experiment comparison isolates prompt effect. |
| **Single synthetic task lacks generality** | This is a *capability gate*, not a generality claim. Parent used identical task. Clearing this bar is necessary (not sufficient) for benchmark execution. |
| **Qwen chat_format mismatch** | Parent verified `chat_format="qwen"` works for Qwen2.5-0.5B. Same format used for 3B/7B. |
| **CPU inference too slow for 7B** | 7B Q4_K_M on 4-core CPU: ~5-10s/step estimated. 5 episodes x 2 steps x 2 prompts = 20 calls. ~2-3 min inference. Acceptable. |
| **GGUF download fails / sha256 mismatch** | Record actual sha256 at download. If download fails for primary, proceed to fallback. If both fail -> MEASUREMENT_INVALID (provisioning failure). |
| **Playwright/Chrome flakiness** | Parent verified Chrome 154.0.8037.97 works. Same subprocess. Synthetic page has no network dependencies. |
| **External check incompleteness** | Bounded source list + time bound. "Ceiling not found in bounded search" != "ceiling does not exist". Reported as `ceiling_above_bar = false` with `search_exhaustive = false` if time bound hit. |
| **Determinism** | Temperature=0.0, fixed seeds (42-46). Traces are perfectly uniform; no variance estimate. Read as deterministic-protocol result. |

---

## 11. Representation Loss Disclosure

- **State representation**: Simplified text representation of DOM (not full accessibility tree). Loss: visual layout, dynamic attributes, shadow DOM. Acceptable for this synthetic task.
- **Action space**: Only `click` and `answer` actions. Loss: type, select, hover, scroll, navigation. Acceptable for minimal task.
- **No session/auth/network variation**: Task is single-page, no auth, no network calls after load. Does not test freshness/staleness (C-FRESHNESS) or delta repair (C-DELTA-REPAIR).
- **Single model family (Qwen)**: Does not test architectural diversity (Llama, Gemma, Phi, etc.). Bounded to Qwen because: (a) parent used Qwen 0.5B; (b) Qwen 3B/7B GGUFs available via same resolve-redirect route; (c) `chat_format="qwen"` verified. Other families would be a separate probe.
- **External check scope**: Bounded to 10 sources, 30 min. Does not cover all possible benchmarks or private evaluations.

---

## 12. Artifacts to Produce (Raw Evidence)

| Path | Role | Description |
|------|------|-------------|
| `raw/model_receipts.json` | raw | Per-model per-prompt: download URL, sha256, bytes, load_time_s, positive_control results, prompt_condition |
| `raw/task_episodes.json` | raw | Per-episode: raw completion, parsed action, parse_ok, step_count, task_success, answer_action_emitted, tokens, latency_s, prompt_condition |
| `raw/control_episodes.json` | raw | NC-NO-MODEL-ACTION and B-RANDOM-ACTION episodes |
| `raw/gguf_sha256.txt` | raw | Verified sha256 of each downloaded GGUF |
| `raw/harness_config.json` | fixture | Frozen harness configuration: prompts (both), GBNF schema, seeds, temperature, max_tokens, candidate models |
| `raw/external_capability_envelope.json` | raw | Structured findings from bounded external capability check |

---

## 13. Scope Boundaries (What This Experiment Does NOT Do)

- Does NOT run the four-arm C-LLM-INHERIT benchmark (COLD/INSTRUCTIONS/RETRIEVAL/SPIDER).
- Does NOT test cross-site transfer (C-CROSSSITE).
- Does NOT test parameterized inheritance (C-PARAM-INHERIT).
- Does NOT test freshness detection (C-FRESHNESS) or delta repair (C-DELTA-REPAIR).
- Does NOT test Web dynamics (C-WEB-DYNAMICS).
- Does NOT test semantic resolution (C-SEMANTIC-RESOLVE).
- Does NOT evaluate product economics (C-PRODUCT-ECON).
- Does NOT test any model requiring GPU, ollama, vLLM, TGI, or cloud credentials.
- Does NOT add candidate models post-freeze.
- Does NOT perform open-ended literature review; external check is bounded to 10 sources / 30 min.

---

## 14. Dependencies on Frozen Upstream Evidence

- **Parent Gate 2 task definition**: Identical minimal task for direct comparability.
- **Parent environment facts**: CPU-only, no GPU, huggingface.co resolve-redirect works, cdn-lfs/api-inference do not resolve, llama-cpp-python 0.2.90 verified, Chrome 154.0.8037.97 works.
- **Parent positive/negative baselines**: B-0.5B-QWEN-LOCAL and B-POLLINATIONS-PROXY carried forward as reference baselines (not re-run).
- **Parent protocol comparator results**: B-UNDERSPECIFIED-PROMPT-7B/3B (0/5 task success) carried as established evidence; re-run in this experiment for direct comparison.
- **C-LLM-INHERIT claim registry**: Status HYPOTHESIS, next_gate "same model/tools/budget; cold vs instructions vs retrieval vs SPIDER".
- **Product committed kernel**: Blob b15ed848 (sha256 718efa6a...) as treatment carrier for any subsequent benchmark.
- **Audit VF-01**: Prompt underspecification identified as likely driver of re-click loop.

---

## 15. Pre-registered Analysis Plan (No Post-Hoc Changes)

1. **Primary analysis**: Apply decision rule in Section 9. Outcome = SUPPORTS / FALSIFIES / MIXED / MEASUREMENT_INVALID.
2. **Secondary descriptive**: Report per-model per-prompt metrics (parseable_action_rate_step1, task_success_rate, answer_action_emission_rate, latency, tokens) with exact counts (k/n).
3. **Prompt effect**: Compare treatment vs comparator per model (task_success_rate delta, answer_action_emission_rate delta).
4. **External ceiling**: Report `external_capability_envelope` structured findings.
5. **No statistical testing beyond decision rule**: The 3/5 threshold is the pre-declared adequacy rule. No p-values, no confidence intervals, no model comparisons.
6. **Validity notes**: Record any deviations (download failures, timeouts, decoding errors) in `validity_notes` with explicit classification (infrastructure vs capability).
7. **Unresolved**: Record any questions EXECUTE cannot settle (e.g., "would 14B model work if GPU available?", "would different schema enumeration format help?").

---

## 16. Handoff Preparation

**If SUPPORTS**: Handoff to Global Research Director with `carry_forward.established` = ["credential-free 3B-8B GGUF clears minimal Web-agent capability bar with goal/schema prompt", "Gate 2 converts to PASS at goal/schema prompt protocol", "C-LLM-INHERIT four-arm benchmark unblocked as specified", "Prompt underspecification (VF-01) confirmed as primary failure mode"]. `next_question` = "Run the frozen four-arm benchmark on the verified credential-free model endpoint with goal/schema prompt."

**If FALSIFIES**: Handoff with `carry_forward.established` = ["credential-free 3B-8B GGUF range exhausted under factory constraints even with goal/schema prompt", "Gate 2 remains FAIL at protocol ceiling", "Bounded external check finds no evidence of capability ceiling above bar for accessible models", "Four-arm benchmark DESIGN_COMPROMISED confirmed as stable boundary"]. `carry_forward.rejected` = ["credential-free path viable without model credential"]. `next_question` = "Global Research Director must explicitly re-scope: drop Gate 3 same-model external anchor; require internally re-run comparators with retrieval quality metrics on dynamic-range task bank."

**If MIXED**: Handoff with `carry_forward.established` = ["goal/schema prompt insufficient for Qwen 3B/7B under factory constraints", "bounded external search finds evidence of capability ceiling above bar for other accessible models"]. `carry_forward.unknown` = ["which specific external model/benchmark clears the bar", "whether that model is provisionable under factory constraints"]. `next_question` = "Intel to verify the specific external model/benchmark from capability envelope; if confirmed provisionable, test that model under same protocol."

**If MEASUREMENT_INVALID**: Handoff with `carry_forward.do_not_assume` = ["decoding infrastructure failure ≠ model capability failure"]. `next_question` = "Repair constrained decoding infrastructure and re-run; or test alternative decoding (outlines, instructor, manual parsing)."

---

## 17. Freeze Eligibility Justifications (v2 Design Contract)

| Check | Verdict | Justification |
|-------|---------|---------------|
| **decision_rule_reachability** | PASS | Decision rule (Section 9) is a deterministic finite-state machine with no unreachable branches. Every path terminates in one of {SUPPORTS, FALSIFIES, MIXED, MEASUREMENT_INVALID} with explicit conditions. Early-stop on success, exhaustive on failure, external check only invoked when treatment fails. |
| **measurement_prerequisites** | PASS | Models downloadable via confirmed route (parent evidence). Infrastructure (llama.cpp 0.2.90, Playwright, Chrome) verified working in parent. GGUF sha256 recorded at download. No unavailable substrate. |
| **baseline_identifiability** | PASS | Comparator prompt is the exact frozen underspecified prompt from parent (harness_config.json). Re-run with same seeds (42-46) for direct within-experiment comparison. Carried baselines explicitly labeled as not re-run. |
| **control_sensitivity** | PASS | Positive control (PC-JSON-CONSTRAINED-DECODING) isolates decoding from reasoning — it MUST pass for treatment evaluation to proceed. Null control (NC-NO-MODEL-ACTION) verifies verification logic. Random baseline (B-RANDOM-ACTION) bounds chance. All three have pre-declared success criteria and PASS/FAIL verdicts independent of treatment outcome. |
| **treatment_liveness** | PASS | Treatment is a system prompt string variant — no infrastructure change, no new model, no new hardware. The harness code modification (dual-prompt evaluation) is a pure software change within Intel's granted scope. The treatment is structurally capable of becoming EXECUTABLE. |
| **freeze_artifacts_bound** | PASS | Mutable local dependencies explicitly listed in `spec.freeze_artifacts`: (1) `research/intel/run_exp_38013769440.py` — the experiment harness (to be created from parent harness with dual-prompt support), (2) `research/experiments/EXP-INTEL-38013769440/raw/harness_config.json` — the frozen fixture. Both are repository-relative paths. No other mutable local code/data/task-bank/fixture dependencies exist. |

---

## 18. Freeze Artifacts (Mutable Local Dependencies)

1. `research/intel/run_exp_38013769440.py` — Experiment harness (derived from `run_exp_37982024058.py` with dual-prompt evaluation loop, external capability check module, and structured raw evidence emission for both prompt conditions). This file will be created before freeze and hashed into `freeze.json.artifact_hashes`.
2. `research/experiments/EXP-INTEL-38013769440/raw/harness_config.json` — Frozen fixture containing both prompts, candidate models, task definition, GBNF grammar, sampling parameters, and clearing thresholds. Constructed before any outcome-bearing measurement.

---

## 19. Signatures

This preregistration is frozen before EXECUTE begins. The deterministic freezer will hash `request.json`, `spec.json`, and this `prereg.md` into `freeze.json`. No changes to hypothesis, candidate set, task, prompts, metrics, decision rule, success thresholds, or external check protocol after freeze.

---

## 20. Legacy Comparative Reasoning (per POLICY.md Section 48)

**LEGACY: DISTINCT_EXTENSION** — This experiment extends the parent EXP-INTEL-37982024058 by:
- Adding the goal/schema-enriched prompt as a treatment (direct test of audit VF-01)
- Re-running the comparator prompt within the same experiment for direct comparison
- Adding a bounded external capability ceiling check (new Intel activity)
- Formalizing the re-scope recommendation as a decision rule output

**Pre-2.0 Artifacts Checked**:
- `codex/legacy_brief.json` findings P2-REPLAY-COST, P2-BLIND-COMPOSITION, P2-MIND2WEB — all relate to Graph replay/composition, not Intel capability gating.
- `codex/legacy_artifact_index.json` — no Intel-lane credential-free model capability gate experiments in pre-2.0 corpus.
- No duplicate of this prompt ablation + external ceiling design exists in legacy or Research 2.0 history.

**Justification for Proceeding**: This is the minimal high-information experiment that can change the C-LLM-INHERIT claim decision. The Director mandate explicitly requires it. No identical invalid/degenerate design is being repeated.