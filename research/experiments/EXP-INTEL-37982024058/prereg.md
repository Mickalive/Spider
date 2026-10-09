# EXP-INTEL-37982024058 Preregistration

**Experiment ID**: EXP-INTEL-37982024058
**Lane**: intel
**Target Claim**: C-LLM-INHERIT
**Director Mandate**: CONTINUE (global-director-CONTINUE, cycle_id=37980982065)
**Parent Handoff**: EXP-INTEL-37973264582 (sha256: 67e0316d0ecc74f714976ccf5e8b74e90cff1dc9174ad09b74742195bf8a9603)

---

## 1. Strategic Context

The Global Research Director has mandated a CONTINUE action on claim C-LLM-INHERIT with a cognitive reset. The parent experiment EXP-INTEL-37973264582 established (audit PASS, frozen label DESIGN_COMPROMISED):

- **Gate 0 PASS**: Two credential-free endpoints exist (E-LOCAL-LLAMA: Qwen2.5-0.5B-Instruct-Q4_K_M via llama.cpp; E-POLLINATIONS-OPENAI: gpt-oss-20b anonymous proxy).
- **Gate 1 PASS** (framework reading): Comparator packages obtainable; LangGraph runs under both endpoints.
- **Gate 2 FAIL**: Neither endpoint completes the minimal Web-agent task ("click #reveal-btn then answer TARGET-42"). Local 0.5B emits prose/no parseable JSON (150 tokens). Proxy returns empty/reasoning-only content, ~197-token cap, intermittent HTTP 402, no SLA/pinning.
- **Gate 3 FAIL_ZERO_PASS**: Zero external comparators publish same-model success/cost anchors for the attained models.

The frozen four-arm C-LLM-INHERIT benchmark (COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER, same model/tools/budget) is **not executable as specified** on current assets. The binding blocker is a **Web-agent-capable credential-free model**.

The Director's strategic question: **Can a larger CPU-quantized GGUF (3B-8B class via the confirmed huggingface.co resolve-redirect route) clear the minimal Web-agent capability bar?** Stopping rule: success unblocks the benchmark; exhaustion of the accessible range closes the credential-free path and licenses re-scope.

---

## 2. Hypothesis and Falsifier

**Hypothesis (H1)**: At least one accessible CPU-quantized GGUF model in the 3B-8B parameter range (primary: Qwen2.5-7B-Instruct-Q4_K_M; fallback: Qwen2.5-3B-Instruct-Q4_K_M) will emit a valid parseable JSON action and complete the minimal multi-step Web-agent task when served via llama.cpp with constrained JSON decoding, converting Gate-2 FAIL to PASS.

**Falsifier (H0)**: No accessible CPU-quantized GGUF model in the 3B-8B class (tested via the confirmed download route, served via llama.cpp with constrained JSON decoding) can emit a valid parseable JSON action and complete the task. Exhaustion of the accessible model size range under these constraints closes the credential-free external-agent path and licenses explicit re-scope of the frozen four-arm design.

**Both-directions outcome**: Either outcome is decision-changing. SUPPORTS unblocks the flagship benchmark. FALSIFIES confirms the DESIGN_COMPROMISED boundary is stable and forces an accountable re-scope.

---

## 3. Candidate Model Set (FROZEN — No Post-Freeze Additions)

| Candidate ID | Model | Quant | Est. Size | Download Route | Chat Format |
|--------------|-------|-------|-----------|----------------|-------------|
| **M-7B-QWEN** (primary) | Qwen2.5-7B-Instruct-Q4_K_M.gguf | Q4_K_M | ~4.1 GB | huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf | "qwen" |
| **M-3B-QWEN** (fallback) | Qwen2.5-3B-Instruct-Q4_K_M.gguf | Q4_K_M | ~1.9 GB | huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf | "qwen" |

**Constraints**:
- Download ONLY via `huggingface.co` resolve-redirect (confirmed working: redirects to `us.aws.cdn.hf.co`).
- `cdn-lfs.huggingface.co` and `api-inference.huggingface.co` do NOT resolve in this factory (parent evidence).
- No GPU available (CPU-only, nproc=4).
- `llama-cpp-python==0.2.90` (parent-verified version).
- Models tested in sequence: M-7B-QWEN first. If it clears the bar, stop (early success). If it fails positive control or task, test M-3B-QWEN.

---

## 4. Minimal Web-Agent Task (Identical to Parent Gate 2)

**Task Definition**: "Click the element with id `reveal-btn`, then answer the revealed target value `TARGET-42`."

**Environment**: Single synthetic HTML page served locally via Python HTTP server:
```html
<!DOCTYPE html>
<html>
<body>
  <button id="reveal-btn">Reveal</button>
  <div id="target" style="display:none">TARGET-42</div>
  <script>
    document.getElementById('reveal-btn').onclick = () => {
      document.getElementById('target').style.display = 'block';
      document.getElementById('reveal-btn').style.display = 'none';
    };
  </script>
</body>
</html>
```

**Action Schema** (enforced by GBNF constrained decoding):
```json
{
  "action": "click" | "answer",
  "selector": "string (required for click)",
  "text": "string (required for answer)"
}
```

**Episode Protocol**:
1. Model receives system prompt: "You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown."
2. Model receives user prompt with current page state (simplified text representation).
3. Model emits ONE action (constrained by GBNF).
4. Harness parses JSON, executes via Playwright, returns new page state.
5. Repeat until model emits `{"action":"answer","text":"TARGET-42"}` or max 5 steps reached.
6. Success = model emits valid click action on `#reveal-btn` THEN valid answer action with `text="TARGET-42"`.

**Parsing Rule**: Action must be valid JSON matching the schema exactly. Any parse error, schema violation, or missing required fields = parse failure.

---

## 5. Controls and Baselines

### Positive Control: PC-JSON-CONSTRAINED-DECODING
- **Purpose**: Verify constrained decoding infrastructure works for each candidate model before task evaluation.
- **Protocol**: 10 probes per model with prompt: `Emit exactly: {"action":"click","selector":"#test"}`
- **Success Criterion**: 10/10 syntactically valid JSON matching schema.
- **Failure Mode**: If positive control fails, the model is excluded from task evaluation (decoding infrastructure failure, not model capability). If BOTH candidates fail positive control -> OUTCOME=MEASUREMENT_INVALID.

### Null Control: NC-NO-MODEL-ACTION
- **Purpose**: Confirm task verification logic correctly rejects non-parseable actions.
- **Protocol**: Harness runs 5 episodes with a fixed script emitting invalid content (e.g., "I will click the button" — no JSON).
- **Success Criterion**: 0% task completion, 0% parseable JSON actions.

### Negative Baselines (from Parent, for Reference)
- **B-0.5B-QWEN-LOCAL**: Qwen2.5-0.5B-Instruct-Q4_K_M (parent E-LOCAL-LLAMA). Expected: 0% parseable actions, 0% task success.
- **B-POLLINATIONS-PROXY**: Pollinations gpt-oss-20b (parent E-POLLINATIONS-OPENAI). Expected: 0% task success (token cap, empty content, budget instability).

---

## 6. Measurement Protocol

### Per-Model Evaluation Sequence
1. **Download & Verify**: Download GGUF via huggingface.co resolve-redirect. Verify sha256 against known value (recorded at download time).
2. **Load Model**: `Llama(model_path=GGUF, n_ctx=2048, verbose=False, chat_format="qwen", seed=42)`. Record load time.
3. **Positive Control**: Run 10 constrained-decoding probes. Record pass rate. If < 10/10 -> model excluded, proceed to next candidate.
4. **Task Episodes**: Run 5 episodes of the minimal Web-agent task.
   - Temperature=0.0, max_tokens=512, seed=42+episode_idx.
   - Constrained decoding via GBNF grammar for action schema.
   - Record per-episode: raw completion, parsed action (or parse error), step count, task success (bool), token usage, latency.
5. **Aggregate Metrics**: Parseable action rate (step 1), task success rate (5 episodes), mean latency, mean tokens.

### Primary Metrics (Stable Identifiers for Downstream)
- `parseable_action_rate_step1`: Fraction of episodes where step 1 action is valid JSON matching schema.
- `task_success_rate`: Fraction of 5 episodes where model completes full task (click then answer TARGET-42).
- `mean_inference_latency_s`: Mean wall-time per model call.
- `mean_completion_tokens`: Mean tokens per completion.
- `positive_control_pass_rate`: Fraction of 10 probes with valid JSON.

### Success Threshold (Per Model)
**Model CLEARS capability bar** iff: `task_success_rate >= 0.6` (>= 3/5 episodes) AND `parseable_action_rate_step1 >= 0.6` (>= 3/5 episodes).

Rationale: 3/5 is the smallest majority above chance that survives binomial exact test (p=0.5, n=5, k>=3 -> p=0.5). This is a minimal but non-trivial threshold for a capability gate.

---

## 7. Decision Rule (Formal)

Let `M_i` be the i-th candidate model tested in order (M-7B-QWEN, then M-3B-QWEN).

For each `M_i`:
1. If `positive_control_pass_rate(M_i) < 1.0`: **EXCLUDE** `M_i`, continue to `M_{i+1}`. Log as `decoding_infrastructure_failure`.
2. Else evaluate task metrics.
3. If `task_success_rate(M_i) >= 0.6` AND `parseable_action_rate_step1(M_i) >= 0.6`: **OUTCOME = SUPPORTS**. Stop testing further models. **Status = COMPLETE**.
4. Else: Continue to `M_{i+1}`.

After all candidates exhausted:
- If no model cleared bar: **OUTCOME = FALSIFIES**. **Status = COMPLETE**.
- If all candidates excluded at positive control: **OUTCOME = MEASUREMENT_INVALID**. **Status = COMPLETE** (with validity_notes explaining decoding infrastructure failure).

---

## 8. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Constrained decoding masks model reasoning** | Positive control isolates decoding; task uses same GBNF. If positive control passes but task fails, failure is reasoning/planning, not formatting. |
| **Single synthetic task lacks generality** | This is a *capability gate*, not a generality claim. Parent used identical task. Clearing this bar is necessary (not sufficient) for benchmark execution. |
| **Qwen chat_format mismatch** | Parent verified `chat_format="qwen"` works for Qwen2.5-0.5B. Same format used for 3B/7B. |
| **CPU inference too slow for 7B** | 7B Q4_K_M on 4-core CPU: ~5-10s/step estimated. 5 episodes x 2 steps = 20 calls. ~2-3 min inference. Acceptable. Fallback to 3B if timeout. |
| **GGUF download fails / sha256 mismatch** | Record actual sha256 at download. If download fails for primary, proceed to fallback. If both fail -> MEASUREMENT_INVALID (provisioning failure). |
| **Prompt sensitivity** | Fixed system prompt (no tuning). Same as parent. If 7B fails, 3B tested with identical prompt. |
| **Playwright/Chrome flakiness** | Parent verified Chrome 154.0.8037.97 works. Same subprocess. Synthetic page has no network dependencies. |

---

## 9. Representation Loss Disclosure

- **State representation**: Simplified text representation of DOM (not full accessibility tree). Loss: visual layout, dynamic attributes, shadow DOM. Acceptable for this synthetic task.
- **Action space**: Only `click` and `answer` actions. Loss: type, select, hover, scroll, navigation. Acceptable for minimal task.
- **No session/auth/network variation**: Task is single-page, no auth, no network calls after load. Does not test freshness/staleness (C-FRESHNESS) or delta repair (C-DELTA-REPAIR).
- **Single model family (Qwen)**: Does not test architectural diversity (Llama, Gemma, Phi, etc.). Bounded to Qwen because: (a) parent used Qwen 0.5B; (b) Qwen 3B/7B GGUFs available via same resolve-redirect route; (c) `chat_format="qwen"` verified. Other families would be a separate probe.

---

## 10. Artifacts to Produce (Raw Evidence)

| Path | Role | Description |
|------|------|-------------|
| `raw/model_receipts.json` | raw | Per-model: download URL, sha256, bytes, load_time_s, positive_control results |
| `raw/task_episodes.json` | raw | Per-episode: raw completion, parsed action, parse_ok, step_count, task_success, tokens, latency_s |
| `raw/gguf_sha256.txt` | raw | Verified sha256 of each downloaded GGUF |
| `raw/harness_config.json` | fixture | Frozen harness configuration: prompts, GBNF schema, seeds, temperature, max_tokens |

---

## 11. Scope Boundaries (What This Experiment Does NOT Do)

- Does NOT run the four-arm C-LLM-INHERIT benchmark (COLD/INSTRUCTIONS/RETRIEVAL/SPIDER).
- Does NOT test cross-site transfer (C-CROSSSITE).
- Does NOT test parameterized inheritance (C-PARAM-INHERIT).
- Does NOT test freshness detection (C-FRESHNESS) or delta repair (C-DELTA-REPAIR).
- Does NOT test Web dynamics (C-WEB-DYNAMICS).
- Does NOT test semantic resolution (C-SEMANTIC-RESOLVE).
- Does NOT evaluate product economics (C-PRODUCT-ECON).
- Does NOT test any model requiring GPU, ollama, vLLM, TGI, or cloud credentials.
- Does NOT add candidate models post-freeze (audit-flagged deviation in parent explicitly prohibited).

---

## 12. Dependencies on Frozen Upstream Evidence

- **Parent Gate 2 task definition**: Identical minimal task ("click #reveal-btn then answer TARGET-42") for direct comparability.
- **Parent environment facts**: CPU-only, no GPU, huggingface.co resolve-redirect works, cdn-lfs/api-inference do not resolve, llama-cpp-python 0.2.90 verified, Chrome 154.0.8037.97 works.
- **Parent positive/negative baselines**: B-0.5B-QWEN-LOCAL and B-POLLINATIONS-PROXY carried forward as reference baselines (not re-run).
- **C-LLM-INHERIT claim registry**: Status HYPOTHESIS, next_gate "same model/tools/budget; cold vs instructions vs retrieval vs SPIDER".
- **Product committed kernel**: Blob b15ed848 (sha256 718efa6a...) as treatment carrier for any subsequent benchmark.

---

## 13. Pre-registered Analysis Plan (No Post-Hoc Changes)

1. **Primary analysis**: Apply decision rule in Section 7. Outcome = SUPPORTS / FALSIFIES / MEASUREMENT_INVALID.
2. **Secondary descriptive**: Report per-model metrics (parseable_action_rate_step1, task_success_rate, latency, tokens) with exact counts (k/n).
3. **No statistical testing beyond decision rule**: The 3/5 threshold is the pre-declared adequacy rule. No p-values, no confidence intervals, no model comparisons.
4. **Validity notes**: Record any deviations (download failures, timeouts, decoding errors) in `validity_notes` with explicit classification (infrastructure vs capability).
5. **Unresolved**: Record any questions EXECUTE cannot settle (e.g., "would prompt engineering change 7B outcome?", "would 14B model work if GPU available?").

---

## 14. Handoff Preparation

**If SUPPORTS**: Handoff to Global Research Director with `carry_forward.established` = ["credential-free 3B-8B GGUF clears minimal Web-agent capability bar", "Gate 2 converts to PASS", "C-LLM-INHERIT four-arm benchmark unblocked as specified"]. `next_question` = "Run the frozen four-arm benchmark on the verified credential-free model endpoint."

**If FALSIFIES**: Handoff with `carry_forward.established` = ["credential-free 3B-8B GGUF range exhausted under factory constraints", "Gate 2 remains FAIL", "four-arm benchmark DESIGN_COMPROMISED confirmed as stable boundary"]. `carry_forward.rejected` = ["credential-free path viable without model credential"]. `next_question` = "Global Research Director must explicitly re-scope: drop Gate 3 same-model external anchor; require internally re-run comparators with retrieval quality metrics on dynamic-range task bank."

**If MEASUREMENT_INVALID**: Handoff with `carry_forward.do_not_assume` = ["decoding infrastructure failure ≠ model capability failure"]. `next_question` = "Repair constrained decoding infrastructure and re-run; or test alternative decoding (outlines, instructor, manual parsing)."

---

## 15. Signatures

This preregistration is frozen before EXECUTE begins. The deterministic freezer will hash `request.json`, `spec.json`, and this `prereg.md` into `freeze.json`. No changes to hypothesis, candidate set, task, metrics, decision rule, or success thresholds after freeze.