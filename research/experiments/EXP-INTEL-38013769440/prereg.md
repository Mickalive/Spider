# EXP-INTEL-38013769440 — Preregistration (lane intel)

Status: DESIGN FINAL (this file is byte-authority for the frozen prompts; `spec.json` is machine authority).

## 0. Identity and authority

- Experiment: `EXP-INTEL-38013769440`, lane `intel`, claim `C-LLM-INHERIT` (only claim addressed).
- Binding direction: `request.json` `director_mandate` (cycle `38013054267`, action `REOPEN`, target `C-LLM-INHERIT`, `parent_handoff_disposition=USE`, `cognitive_reset=false`). The mandate's strategic question is the authorization; the inherited `EXP-INTEL-37982024058` handoff (sha256 `b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55`) is continuity evidence only.
- This packet determines readiness condition (3) of the four-arm C-LLM-INHERIT benchmark. It does not promote the claim; any status change is the DIRECTOR's decision.

Binding question: Under the same credential-free, CPU-quantized constraints, does supplying the task goal/schema in the system prompt (removing the underspecification the parent harness did not have) convert the step-0 reveal-click into a full multi-step click-then-answer completion for the largest obtainable credential-free models, and if not, what is the demonstrable capability ceiling for the minimal Web-agent task across ALL credential-free endpoints and local models actually available to the factory? Return an explicit close/re-scope recommendation so that readiness condition (3) is either satisfied by a proven same-model driver or the four-arm benchmark is re-scoped off the credential-free path. Include a bounded external check of the published capability envelope for comparably sized local models.

## 1. Established / rejected / unknown / do_not_assume (from parent EXP-INTEL-37982024058)

- **Established.** Under the frozen underspecified-prompt protocol (no goal/schema; constrained GBNF; temp=0; seeds 42-46; CPU-only llama.cpp 0.2.90; Qwen2.5 3B/7B Q4_K_M): M-7B-QWEN 0/5 and M-3B-QWEN 0/5 task success, `parseable_action_rate_step1` 1.0, PC-JSON 10/10, audit PASS. Verification is mechanical (`clicked_reveal AND revealed_value==TARGET-42 AND final answer==TARGET-42`). NC 0/5; B-RANDOM 5/5 valid JSON, 0/5 success. Failure mode: step-0 reveal-click succeeds, then the models re-click the now-hidden `#reveal-btn` for all remaining steps and never answer.
- **Rejected.** Bounded to the frozen 3B-8B Qwen class under the underspecified prompt (not a general rejection of the credential-free path). The census unconstrained-decoding 0.5B prose result does NOT transfer to this GBNF protocol. The Pollinations proxy (gpt-oss-20b) is carried as a timestamp-bound endpoint-layer negative (empty/reasoning-only, ~197-token cap, intermittent 402), not re-measured.
- **Unknown.** Whether the goal/schema prompt converts the click into full completion; whether the failure is prompt-specific or a general small-model planning ceiling; whether 14B clears; whether 0.5B clears under GBNF.
- **do_not_assume.** Do not generalize the parent FALSIFIES to other prompts/architectures/models; the 7B single-file URL 404s (split shards are same model/quant, not a substitution); NOT_ATTEMPTED/NOT_MEASURED records are not negatives; carried negatives are not protocol-transferable; do not re-run the census.

## 2. Hypothesis (H1) and Falsifier (F1)

**H1.** The parent's 0/5 negatives are caused at least partly by system-prompt underspecification (audit VF-01), not by an immutable capability ceiling. Under PR-SPECIFIED (below), the step-0 reveal-click converts into a full click-then-answer: at least one candidate in {M-7B-QWEN, M-3B-QWEN, M-14B-QWEN} clears the bar (`task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6` over 5 episodes), all other constraints byte-identical to the parent. M-0.5B-QWEN is additionally measured as a census-completeness candidate; if it alone clears, the outcome is still SUPPORTS with it recorded as the driver.

**F1.** Under PR-SPECIFIED no obtainable candidate clears the bar, while CV-UNDERSPEC-REPLICATION reproduces the parent 0/5 + reveal-click loop and PC-SCRIPTED-ORACLE proves the task is passable (5/5). Exhaustion of the obtainable range plus the carried proxy negative closes the credential-free path: readiness condition (3) is NOT satisfied and the benchmark must be re-scoped off the credential-free path.

## 3. Candidates (frozen)

| id | model | packaging | bytes | sha256 / source | URL |
|---|---|---|---|---|---|
| M-0.5B-QWEN | Qwen2.5-0.5B-Instruct Q4_K_M | single | 491,400,032 | `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db` (census receipts; recomputed at download) | huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF resolve qwen2.5-0.5b-instruct-q4_k_m.gguf |
| M-3B-QWEN | Qwen2.5-3B-Instruct Q4_K_M | single | 2,104,932,768 | `626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d` (parent gguf_sha256.txt) | .../Qwen2.5-3B-Instruct-GGUF ... qwen2.5-3b-instruct-q4_k_m.gguf |
| M-7B-QWEN | Qwen2.5-7B-Instruct Q4_K_M | 2 shards | 3,993,201,344 + 689,872,288 | shard1 `dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db`, shard2 `539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a` (parent gguf_sha256.txt) | .../Qwen2.5-7B-Instruct-GGUF ...-00001-of-00002.gguf, -00002-of-00002.gguf |
| M-14B-QWEN (escalation, availability-gated) | Qwen2.5-14B-Instruct Q4_K_M | 3 shards | 3,991,999,872 + 3,989,373,504 + 1,006,737,120 | recomputed at download; sizes pinned at DESIGN | .../Qwen2.5-14B-Instruct-GGUF ...-000{1,2,3}-of-00003.gguf |

The 7B single-file URL `...q4_k_m.gguf` returns 404 (pre-probed) — EXECUTE must not use it. A shard hash mismatch => `NOT_MEASURED-SHA-MISMATCH`, never a silent substitution.

## 4. Frozen task and prompts (single-variable ablation)

Task `MIN-WEBAGENT-CLICK-REVEAL-ANSWER`: synthetic page served via local `http.server` on 127.0.0.1 random port. HTML byte-identical to the parent fixture `harness_config.json`:

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

Max 5 steps/episode. Success requires `clicked_reveal=True` AND `revealed_value==TARGET-42` AND final answer text == `TARGET-42`. Action schema: `click` requires `action`+`selector`; `answer` requires `action`+`text`; any parse error, schema violation or missing field is a parse failure (regex-parse recorded as raw evidence only).

GBNF grammar (byte-identical to parent fixture):

```
root ::= ws "{" ws "\"action\"" ws ":" ws action ws "," ws field ws "}" ws
ws ::= [ \t\n]*
action ::= "\"click\"" | "\"answer\""
field ::= "\"selector\"" ws ":" ws string | "\"text\"" ws ":" ws string
string ::= "\"" strchars "\""
strchars ::= strchar strchars | strchar
strchar ::= [^"\\] | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])
```

User template (byte-identical to parent):

```
PAGE_TEXT: {page_text}
ELEMENTS: {elements_json}
HISTORY: {history}
Next action (JSON only): 
```

**Comparator system prompt (PR-UNDERSPEC)** — byte-identical to the parent fixture `prompts.system`:

```
You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.
```

**Treatment system prompt (PR-SPECIFIED)** — the single-variable change; byte-frozen to the grand-parent census harness SYS literal (`EXP-INTEL-37973264582/raw/code/min_webagent.py`, sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`), with exactly two token-level adaptations in the click example — the schema key `ref`->`selector` (the frozen grammar accepts only keys `selector`/`text`) and its placeholder `<id>`->`<css selector>`. Every other word is VERBATIM, including the goal sentence:

```
You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<css selector>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it.
```

Leak guard (P2-BLIND-COMPOSITION): neither prompt contains the exact selector `#reveal-btn` nor the answer string `TARGET-42`.

Sampling (identical to parent): temperature=0.0, max_tokens=512, n_ctx=2048, chat_format=`qwen`, llama_seed=42, base_seed=42, episode seed = 42 + episode_idx, 5 episodes/arm/model, CPU threads=4. The EXECUTE harness must reconstruct PR-UNDERSPEC and PR-SPECIFIED byte-for-byte (AUDIT-verifiable against this section) and all other fixture fields byte-identical to the parent `harness_config.json`.

## 5. Procedure (frozen)

Candidate order: M-7B-QWEN -> M-3B-QWEN -> (conditional) M-14B-QWEN -> (census-completeness) M-0.5B-QWEN. Per candidate: (1) load + receipt (shard sha256); (2) PC-JSON-CONSTRAINED-DECODING (10/10); (3) 5 episodes under PR-UNDERSPEC (M-7B-QWEN and M-3B-QWEN only = CV-UNDERSPEC-REPLICATION); (4) 5 episodes under PR-SPECIFIED. M-14B-QWEN and M-0.5B-QWEN run PC then PR-SPECIFIED only. PC-SCRIPTED-ORACLE runs once before any model episode; NC-NO-MODEL-ACTION and B-RANDOM-ACTION run once. Early stop on the first clear under PR-SPECIFIED (remaining candidates `NOT_ATTEMPTED-EARLY-STOP`, never negatives).

Obtainable set (pre-declared, non-outcome-bearing): M-0.5B/3B/7B-QWEN are always in the obtainable set; M-14B-QWEN joins iff all 3 shards download with pinned content-lengths AND available memory >= 11 GiB at load time. Otherwise M-14B-QWEN is recorded `NOT_IN_OBTAINABLE_SET` (RAM or PROVISIONING) and excluded by the definition (bounded ceiling, not a scientific negative). "Largest obtainable" is defined by the runner's ~16 GiB RAM under CPU-only llama.cpp: 14B Q4_K_M (~8.37 GiB weights) fits; Qwen2.5-32B Q4_K_M is 19,851,336,384 B (~18.49 GiB) across 5 shards and 72B is larger still, so 32B/72B are `NOT_IN_OBTAINABLE_SET` by the same memory definition and the E-LOCAL-LLAMA Q4_K_M range ends at 14B.

## 6. Metrics

- `task_success_rate` — episodes with `clicked_reveal=True` AND `revealed_value==TARGET-42` AND final answer == `TARGET-42` (bar >= 0.6).
- `parseable_action_rate_step1` — step-1 action parsed to valid schema JSON (bar >= 0.6).
- `positive_control_pass_rate` — PC-JSON passes / 10 (requirement 10/10 pre-task).
- `scripted_oracle_task_success_rate` — PC-SCRIPTED-ORACLE successes / 5 (requirement 5/5).
- `answer_action_emission_rate` — episodes emitting >= 1 parseable `answer` action.
- `step0_reveal_click_rate` — episodes with a step-1 click on `#reveal-btn`.
- `loop_signature_rate` — episodes with >= 1 post-reveal click on the now-hidden `#reveal-btn`.
- `mean_inference_latency_s`, `mean_completion_tokens` — economics records.
- `candidate_cleared_bar` (derived) — `parseable_action_rate_step1 >= 0.6 AND task_success_rate >= 0.6`.
- `obtainable_set_complete` (derived) — every candidate in the pre-declared obtainable set measured under PR-SPECIFIED.

## 7. Controls

- **PC-SCRIPTED-ORACLE** (positive, NEW): deterministic non-model policy emits `{"action":"click","selector":"#reveal-btn"}` then `{"action":"answer","text":"TARGET-42"}` through the identical episode pipeline; 5 episodes. Requirement 5/5; < 5/5 => `MEASUREMENT_INVALID` (unpassable-task / broken-verifier artifact cannot masquerade as a negative).
- **PC-JSON-CONSTRAINED-DECODING** (positive): 10/10 schema-valid JSON per candidate through the identical grammar path. A failure is `NOT_MEASURED-PC-FAIL`; both 7B and 3B failing => `MEASUREMENT_INVALID`.
- **NC-NO-MODEL-ACTION** (null): fixed invalid producer ('I will click the button'), 5 episodes; expect 0 parseable / 0 success.
- **B-RANDOM-ACTION** (null-random): uniform random from `[click #reveal-btn; answer TARGET-41/42/43/unknown]`, 5 episodes; expect ~0 success, chance-consistent parseable rate.
- **CV-UNDERSPEC-REPLICATION** (continuity): M-7B-QWEN and M-3B-QWEN under PR-UNDERSPEC. PASS iff for EACH model: `task_success_rate == 0/5` AND `step0_reveal_click_rate >= 0.8` AND `loop_signature_rate >= 0.2` AND `parseable_action_rate_step1 >= 0.8`. All-or-nothing: ANY unmet condition on either model (including a clear under PR-UNDERSPEC) => `MEASUREMENT_INVALID` reason `REPLICATION-DEVIATION`.
- Carried context (not controls): B-0.5B-QWEN-LOCAL (different protocol), B-POLLINATIONS-PROXY (timestamp-bound).

## 8. Decision rule

Bar cleared iff `parseable_action_rate_step1 >= 0.6` AND `task_success_rate >= 0.6` (>= 3/5 both; success mechanically requires the reveal click).

1. `PC-SCRIPTED-ORACLE != 5/5` => `MEASUREMENT_INVALID`. `PC-JSON` fails on BOTH 7B and 3B => `MEASUREMENT_INVALID`.
2. CV-UNDERSPEC-REPLICATION not PASS => `MEASUREMENT_INVALID` (`REPLICATION-DEVIATION`). Raw observations still reported.
3. Any measured candidate clears under PR-SPECIFIED => `SUPPORTS` (early stop; first clearing candidate in frozen order + all clearing candidates recorded as drivers).
4. Replication PASS and no candidate clears:
   a. EVERY candidate in the obtainable set measured and failed => `FALSIFIES`. Ceiling = measured E-LOCAL-LLAMA range + carried proxy negative; issue close/re-scope.
   b. Any candidate IN the obtainable set unresolved for a non-capability reason => `MIXED`; negative bounded to the measured subset; unresolved arm explicitly UNRESOLVED.
5. Infra failure preventing measurement => `MEASUREMENT_INVALID` (never a scientific negative); `status=BLOCKED` only if it precedes any measurement. A valid scientific negative is `status=COMPLETE` with `outcome=FALSIFIES`.

Close/re-scope deliverable (report.md, regardless of direction): SUPPORTS -> benchmark executable as frozen with the proven driver (id + shard hashes); FALSIFIES/MIXED -> readiness condition (3) NOT satisfiable on the credential-free path; re-scope the four-arm benchmark off it (drop Gate 3's same-model external anchor; internally re-run comparators on a dynamic-range task bank per EXP-PRODUCT-37973256064/EXP-PRODUCT-37950607128).

## 9. Validity threats and representation loss

- **Constrained decoding** measures reasoning+completion under grammar, not free-form formatting; PC-JSON isolates decoding from reasoning.
- **Verification tautology** avoided: success requires `TARGET-42` extracted after the reveal click; answering from prior knowledge without the click yields wrong context (target hidden).
- **Version/representation loss**: GBNF, chrome 154.0.8037.97, playwright 1.63.0 and llama-cpp-python 0.2.90 are pinned; the only fallback (0.3.x wheel) is gated by CV-UNDERSPEC-REPLICATION so drift becomes `MEASUREMENT_INVALID`, not silent.
- **Determinism**: temp=0 + fixed seeds; the 3/5 rule is pre-declared, not statistical; 5/5-uniform traces should be read as a deterministic-protocol result, not a sampled rate with independent trials.
- **Scope**: bounds hold only for the frozen minimal two-step task, prompts, sampling and measured candidates; no generalization to arbitrary multi-step web tasks; no Product-Core promotion.
- **Prerequisite honesty**: the runner image ships the chrome binary but not the python `llama_cpp`/`playwright` packages; both pinned versions were verified to exist on public PyPI at DESIGN and the identical stack was already built and run in the parent EXECUTE.

## 10. Legacy / pre-2.0 comparison and bounded external envelope check

`codex/legacy_brief.json` records no prior SPIDER experiment on small-local-model agentic prompt ablation; the closest legacy findings are about compiled replay (P2-REPLAY-COST) and content-addressed reuse (P2-BLIND-COMPOSITION), neither of which is this measurement. This experiment is a distinct new measurement, not a repeat of a pre-2.0 design.

Bounded external check (mandate request; non-confirmatory; `EXTERNAL_PRIOR_ART` only) — completed at DESIGN and recorded in `spec.external_capability_envelope_check`:

- WebArena (arXiv:2307.13854, ICLR 2024): best GPT-4 agent 14.41% end-to-end success vs human 78.24%; GPT-3.5 8.75%.
- Public WebArena leaderboard metadata: zero-shot Qwen2.5-7B ~12.3%; DPO-tuned Qwen2.5-7B ~24-28%.
- Qwen2.5 official function-calling docs: tool use is prompt/template dependent; the model can "fall into a loop and require calling the same function again and again", and protocol conformance is not guaranteed; a fine-tuned Qwen2.5-3B is offered because base 3B is not reliable multi-step.

These anchors are consistent with the parent observation (step-1 action fine, multi-step completion fragile) but are NOT measurements of this task, these GGUF builds or this prompt, and cannot alter the primary outcome. EXECUTE records them as context only.

## 11. Environment / prerequisites (verified live at DESIGN, non-outcome-bearing)

python 3.12.15; nproc=4; disk 85 GiB free; RAM 15,989 MiB total / 14,473 MiB available; Google Chrome 154.0.8037.97 at `/usr/bin/google-chrome`; gcc 13.3.0 / cmake 3.31.6 / GNU Make 4.3; PyPI-verified pinned artifacts llama-cpp-python==0.2.90 sdist 63,762,953 B and playwright==1.63.0 manylinux wheel (the identical stack already built and ran in the parent EXECUTE). GGUF URLs HTTP-verified at pinned sizes (0.5B/3B/7B/14B); the 7B single-file URL 404 is recorded. No credential, paid endpoint, GPU or new substrate required.

## 12. Code / artifact binding (design_contract_version 2)

`freeze_artifacts` lists the pre-existing mutable local inputs whose identity can change the interpretation; `scripts/freeze_experiment.py` hashes them into `freeze.json.artifact_hashes` and they become immutable for this transaction:

- `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (`7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`) — task HTML, GBNF, `prompts.system`=PR-UNDERSPEC, user template, sampling, action schema.
- `research/intel/run_exp_37982024058.py` (`2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`) — fork source; success mechanics verified at DESIGN.
- `research/experiments/EXP-INTEL-37982024058/raw/gguf_sha256.txt` (`93836c2594b0c156c0fa913fb384e913586cb03adbd501773fdf6fd450176dbd`) — 3B/7B identities.
- `research/experiments/EXP-INTEL-37973264582/raw/endpoint_receipts.json` (`b7f5c850c4cee3dbac892e28188c1ef18b32c44dc926cf42de121e731db294e9`) — 0.5B pinning + proxy/interception receipts.
- `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py` (`4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`) — treatment-provenance SYS literal for PR-SPECIFIED.

`freeze_artifacts_bound = PASS`. The EXECUTE harness (`research/intel/run_exp_38013769440.py`) and its derived fixture do not exist at freeze time because DESIGN writes only `spec.json`/`prereg.md`; they are bound at EXECUTE by sha256 into `result.json.artifacts` (roles `code`/`fixture`) and `provenance.json`. AUDIT re-verifies the derived fixture and both prompt strings byte-for-byte against section 4. Remote GGUF responses are pinned by URL + sha256 (sampling protocol frozen), not by file hash.

## 13. Branch-reachability matrix

| branch | reachable when |
|---|---|
| SUPPORTS | any measured candidate clears under PR-SPECIFIED (early stop; driver recorded) |
| FALSIFIES | PC-SCRIPTED-ORACLE 5/5, replication PASS, and EVERY candidate in the obtainable set measured under PR-SPECIFIED and failing (14B either in the set and measured, or excluded by the pre-declared availability definition) |
| MIXED | replication PASS, measured candidates fail, but a candidate IN the obtainable set is unresolved for a non-capability reason |
| MEASUREMENT_INVALID | scripted-oracle < 5/5; PC-JSON fails on both 7B and 3B; replication not PASS; playwright/chrome/server/build failure |

## 14. Handoff preparation

`handoff.json` will preserve established (per-candidate ablation outcome; all control results; census completeness incl. 0.5B/14B; cost records), rejected (invalidated re-scope assumptions), unknown (14B/0.5B if unmeasured; external-envelope classification), do_not_assume (no cross-model generalization, no endpoint promotion, no four-arm benchmark execution authorization, carried negatives not protocol-transferable).

## 15. Signatures

- Design: `opencode/big-pickle`, DESIGN mode, lane intel.
- No outcome-bearing measurements were performed during DESIGN; all probes were non-outcome-bearing and recorded in `spec.pre_freeze_satisfiability_dry_run.environment_probes`.
- Fidelity: parent/census fixture hashes re-verified at DESIGN; PR-SPECIFIED byte-compared against `min_webagent.py` SYS literal — the only deviations are the two click-example tokens (`ref`->`selector`, `<id>`->`<css selector>`), with all other text verbatim.
