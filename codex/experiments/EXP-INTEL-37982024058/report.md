# EXP-INTEL-37982024058 — EXECUTE Report

**Experiment**: EXP-INTEL-37982024058 · **Lane**: intel · **Claim**: C-LLM-INHERIT
**Status**: COMPLETE · **Outcome**: FALSIFIES (frozen prereg §7 decision rule)
**Frozen inputs**: `request.json` (6d0dfc15…), `spec.json` (86cf8894…), `prereg.md` (ea24f965…), `freeze.json` — not modified during EXECUTE.

---

## 1. What was measured (information-class chain)

### RAW EVIDENCE (paths in `raw/`)
- `raw/model_receipts.json` — per candidate: download URLs, bytes, sha256, load time/status, 10 positive-control probe outputs, 5 episodes × up-to-5 steps with **verbatim raw completions**, parsed actions, parse details, latencies, completion tokens, mechanical page-state verification (final `#target` visibility/text).
- `raw/task_episodes.json` — per-candidate aggregation mandated by prereg §10.
- `raw/control_episodes.json` — NC-NO-MODEL-ACTION and B-RANDOM-ACTION episodes.
- `raw/gguf_sha256.txt` — download-time sha256 receipts.
- `raw/provisioning_evidence.json` — frozen-URL 404 evidence + replacement shard artifacts.
- `raw/harness_config.json` — fixture (frozen prompts, GBNF grammar, seeds, thresholds), written before any outcome measurement.

### OBSERVATIONS (direct, unchanged)
1. Frozen primary URL `…/qwen2.5-7b-instruct-q4_k_m.gguf` → **HTTP 404**; Q4_K_M exists only as two split shards in the same repo.
2. 7B shards load under `llama-cpp-python 0.2.90` (`Llama(model_path=<shard1>)`; companion shard auto-located; `n_vocab=152064`); 3B single file loads identically.
3. **Positive control**: 10/10 valid schema-conforming JSON for **both** models (PC-JSON-CONSTRAINED-DECODING PASS).
4. **Task episodes (both models, all 5 episodes, all seeds 42–46)**:
   - step 0 → `{"action":"click","selector":"#reveal-btn"}` executes; `#target` becomes visible with `TARGET-42` (`revealed_value='TARGET-42'`, `final_target_visible=true`);
   - steps 1–4 → the **same click action re-emitted** on the now-hidden button (`click_ok=False`); ELEMENTS in the observation is empty and PAGE_TEXT contains `TARGET-42`;
   - **no `answer` action was ever emitted**;
   - step_count = 5 in all episodes; `task_success=false` in 0/5 for both models.
5. NC-NO-MODEL-ACTION: fixed non-JSON content rejected 5/5 (0% parseable, 0% success). *(Verification logic rejects non-JSON.)*
6. B-RANDOM-ACTION: 5/5 valid JSON by construction, 0/5 task success. *(Chance bound.)*

### DERIVED MEASUREMENTS (stable metric ids, prereg §6)
| Metric | M-7B-QWEN | M-3B-QWEN | NC | B-RANDOM |
|---|---|---|---|---|
| `positive_control_pass_rate` | 1.0 (10/10) | 1.0 (10/10) | — | — |
| `parseable_action_rate_step1` | 1.0 (5/5) | 1.0 (5/5) | 0.0 | 1.0 |
| `task_success_rate` | 0.0 (0/5) | 0.0 (0/5) | 0.0 | 0.0 |
| `mean_inference_latency_s` | 5.065 | 2.154 | — | — |
| `mean_completion_tokens` | 17.0 | 13.0 | — | — |

### INTERPRETATION (per frozen decision rule, prereg §7)
- Clearing condition is **task_success_rate ≥ 0.6 AND parseable_action_rate_step1 ≥ 0.6**. 0.0 < 0.6 for task success on both candidates → no candidate cleared → after exhausting the candidate list: **OUTCOME = FALSIFIES**.
- This is a **valid negative**: positive controls passed 10/10 for both models, so the failure is not constrained-decoding infrastructure. The models can emit schema-valid JSON on demand and can click the right button; the deficit is task-level — an underspecified instruction set (frozen system prompt contains no goal) under which both models saturate the reveal click and never transition to `answer`.

---

## 2. Decision-rule application

```
For each candidate M_i (order: M-7B-QWEN, M-3B-QWEN):
  1. positive_control_pass_rate(M_i) < 1.0?  NO (1.0) -> not excluded
  2. task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6?  NO (0.0)
  3. -> continue to next candidate
Candidates exhausted: no model cleared the bar
-> OUTCOME = FALSIFIES, STATUS = COMPLETE          (prereg §7)
```

Prereg §14 consequence: **FALSIFIES** → carry forward to the Global Research Director that the credential-free 3B–8B GGUF range is exhausted under factory constraints, Gate 2 remains FAIL, and the frozen four-arm C-LLM-INHERIT benchmark remains DESIGN_COMPROMISED; the explicit re-scope option (drop Gate 3's external same-model anchor; internally re-run comparators with their own quality on a task bank with dynamic range) is now licensed.

---

## 3. Controls / baselines

| Control id | Expected | Observed | Verdict | Evidence |
|---|---|---|---|---|
| PC-JSON-CONSTRAINED-DECODING | 10/10 valid JSON per model | 10/10 both models | **PASS** | `model_receipts.json` |
| NC-NO-MODEL-ACTION | 0% parseable, 0% success | 0.0 / 0.0 | **PASS** | `control_episodes.json` |
| B-RANDOM-ACTION | chance-level success | 0/5 (0.0) | **PASS** (chance-consistent) | `control_episodes.json` |
| B-0.5B-QWEN-LOCAL (carried, not re-run) | 0% / 0% | parent evidence (prose, no JSON) | UNKNOWN_NOT_RERUN | parent result.json |
| B-POLLINATIONS-PROXY (carried, not re-run) | 0% success | parent evidence (token cap, 402s) | UNKNOWN_NOT_RERUN | parent result.json |

---

## 4. Deviations and validity notes (summary; full list in `result.json`)

1. **Provisioning packaging deviation — not a model substitution.** The frozen single-file 7B URL 404s; same-model, same-quant Q4_K_M split shards were downloaded, sha256-recorded at download time, load-tested (load succeeded) before evaluation. This is the prereg §8-anticipated download-failure path, resolved in the intended direction.
2. **Prompt sensitivity (explicit prereg §8 threat) is the most plausible driver of the negative.** The frozen system prompt (prereg §4.1) states only "reply with a valid JSON action" — no action-schema enumeration, no goal ("click the button, then answer the revealed code"). The parent harness's SYS prompt contained goal + schema. Under the frozen protocol the outcome is FALSIFIES; the question whether the parent-style prompt converts the step-0 click into a completed task is deliberately left **unresolved** rather than answered by post-freeze prompt tuning (prohibited).
3. **Deterministic protocol**: temperature=0.0, seed=42+episode_idx → 5/5 uniform traces; no variance estimate; interpret as deterministic-protocol outcome, not independently sampled trials.
4. **Capability gate only**: one synthetic page, click/answer space, no economics, no generality; clearing is necessary-not-sufficient for the benchmark.
5. **Small n** (5 episodes/candidate) with the pre-declared 3/5 adequacy rule; no statistics beyond the decision rule (prereg §13.3).

---

## 5. Economics / cost to the factory

- Downloads: 6.79 GB total (7B shards 4.683 GB, 3B 2.105 GB) via the confirmed resolve-redirect route; sha256 computed locally.
- Compute: 35 model calls per candidate = 10 positive-control probes + 25 episode-step inference calls (5 episodes × 5 steps; every step is a real llama.cpp call). CPU-only. 7B ~5.1 s/call, 3B ~2.2 s/call.
- No credentials, no budgeted external API spend.

---

## 6. What this experiment does and does not say

**Does say**: With the frozen protocol (prompt, task, decoding, seeds), no accessible credential-free CPU-quantized GGUF in the 3B–8B Qwen class clears the minimal Web-agent bar; Gate 2 remains FAIL; the DESIGN_COMPROMISED boundary from the parent is stable against scaling the local model class.

**Does not say**: that these models cannot complete the task under any prompt; that a 14B+ or non-Qwen model fails; that constrained decoding or the HTTP provisioning route failed (both are verified working); anything about economics, generality, or other claims.

**Next-most-decision-changing measurement** (for the Global Research Director): the explicit-goal prompt probe — same frozen task and models, system prompt amended to parent-style goal + schema enumeration — which would separate "credential-free model cannot plan/act" from "credential-free model cannot act under this frozen prompt". This is a NEW experiment decision, not something EXECUTE may run post-freeze.