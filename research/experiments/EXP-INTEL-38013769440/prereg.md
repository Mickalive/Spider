# EXP-INTEL-38013769440 Preregistration

- Experiment: `EXP-INTEL-38013769440`
- Lane: `intel`
- Claim: `C-LLM-INHERIT` (status HYPOTHESIS; current effective event EXP-INTEL-37982024058 FALSIFIES)
- Design contract version: 2 (freeze_eligibility + freeze_artifacts in spec.json)
- Request: `research/experiments/EXP-INTEL-38013769440/request.json` (contains `director_mandate`, allocation action REOPEN, parent_handoff disposition USE)
- Parent packet: `research/experiments/EXP-INTEL-37982024058` (handoff sha256 `b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55`)

## 0. Status

`FROZEN` (DESIGN complete, satisfiability checks PASS, awaiting freezer).

---

## 1. Strategic Context

The mandate (Director, Global Research Director, cycle 38013054267) asks one decision-changing question (B3): under the same credential-free, CPU-quantized constraints, does supplying the task goal/schema in the system prompt — removing the underspecification the parent harness did not have — convert the step-0 reveal-click into a full multi-step click-then-answer completion for the largest obtainable credential-free models; if not, what is the demonstrable capability ceiling for the minimal Web-agent task across ALL credential-free endpoints and local models actually available to the factory; and return an explicit close/re-scope recommendation for readiness condition (3) of the four-arm C-LLM-INHERIT benchmark, including a bounded external check of the published capability envelope for comparably sized local models.

Parent handoff (EXP-INTEL-37982024058) carry-forward — preserved verbatim in intent:

**Established**
- M-7B-QWEN and M-3B-QWEN (Qwen2.5-7B/3B-Instruct Q4_K_M via llama.cpp 0.2.90 constrained decoding, CPU-only, nproc=4) both pass PC-JSON-CONSTRAINED-DECODING 10/10.
- Both fail the frozen minimal Web-agent task 0/5, 0/5 (task_success_rate 0.0) with parseable_action_rate_step1 1.0 — models emit schema-valid JSON actions every episode but never complete the task.
- Trace: step-0/hidden-button clicks occur; revealed value TARGET-42 is surfaced in PAGE_TEXT; models re-click hidden elements and never emit the answer action (reveal-click loop).
- Audit PASS with material finding VF-01: system-prompt underspecification bounds the parent negative to the frozen prompt ceiling; the falsifier's generality (any 3B-8B credential-free model) is NOT established by the parent.
- Null and random controls behave as designed (NC 0/0; B-RANDOM 5/5 valid JSON, 0/5 success).

**Rejected**
- No smaller credential-free model can do the task: M-0.5B-QWEN-LOCAL emits prose, 0% parseable (established earlier, EXP-INTEL-37973264582).
- gpt-oss-20b via Pollinations anonymous proxy can drive the task: empty/reasoning-only content, ~197-token cap, intermittent HTTP 402.

**Unknown**
- Whether 3B/7B failure is a model-capability ceiling or a prompt-underspecification artifact (VF-01).
- Whether larger obtainable local models (14B) fail or pass under identical constraints.
- The published capability envelope for comparably sized local models on multi-step browser/tool tasks (only pre-2.0 PAPER_EVIDENCE exists: e.g., WebArena avg success 37.5% GPT-4.1 / 24.3% Qwen3-4B, NOT reproduced by SPIDER).

**Do not assume**
- Do not assume the parent's 0/5 transfers to a different (specified) system prompt — that is exactly what this experiment measures.
- Do not assume the parent's 0/5 transfers to 14B — not tested.
- Do not assume non-Qwen open-weight models (e.g., Llama-3.2-3B, Gemma-2-9B) — they are not in the obtainable set via the confirmed route without new provisioning; out of scope.
- Do not assume Pollinations receipts are reproducible contracts (timestamp-bound, budget instability); do not promote them.
- Do not assume an answer-action emission is a completion: completion requires answer text exactly `TARGET-42`.
- Do not assume this experiment authorizes promotion of any endpoint into Product Core.

---

## 2. Hypothesis and Falsifier

**Hypothesis (H1).** Under the same credential-free, CPU-quantized constraints, the parent-era 0/5 negatives for M-7B-QWEN and M-3B-QWEN are caused at least partly by system-prompt underspecification (audit finding VF-01), not by an immutable model-capability ceiling. Under a parent-style system prompt that states the goal and enumerates the action schema (PR-SPECIFIED below), the models' step-0 reveal-click (observed 5/5 in the parent) converts into a full click-then-answer completion: at least one candidate in {M-7B-QWEN, M-3B-QWEN, M-14B-QWEN} clears the frozen capability bar (task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6 per 5-episode run; cleared iff >= 3/5 episodes with both), all other frozen constraints byte-identical to the parent.

**Falsifier (F1).** Under the same constraints and PR-SPECIFIED, no model in the obtainable set {M-7B-QWEN, M-3B-QWEN, M-14B-QWEN} clears the bar, while the within-experiment replication control CV-UNDERSPEC-REPLICATION confirms behavioral continuity with the parent (0/5 + reveal-click loop on both 7B and 3B). Exhaustion of the obtainable credential-free range plus carried negatives (M-0.5B-QWEN-LOCAL, B-POLLINATIONS-PROXY) closes the credential-free external-agent path: readiness condition (3) is NOT satisfied by any credential-free same-model driver, and the four-arm C-LLM-INHERIT benchmark must be explicitly re-scoped off the credential-free path.

---

## 3. Frozen Environment and Substrate (verified at DESIGN time)

Verified live by non-outcome-bearing probes (recorded in this prereg; all PASS):

- Python 3.12.15 (runner toolchain).
- `llama-cpp-python==0.2.90` primary: no cp312 binary wheel exists; sdist `llama_cpp_python-0.2.90.tar.gz` (63,762,953 bytes) downloads; source-build toolchain present (gcc 13.3.0, g++ , cmake 3.31.6, make). Fallback ONLY if sdist build fails: latest 0.3.x wheel; document flag; continuity gated by CV-UNDERSPEC-REPLICATION.
- `playwright==1.63.0` (wheel verified downloadable); system `google-chrome` present at `/usr/bin/google-chrome` (version 154.0.8037.97, identical to parent); `executable_path` used; no browser install step required.
- Network: huggingface.co `resolve-redirect` route verified live (HTTP 200) for all model URLs below; content-lengths match the parent's `gguf_sha256.txt` receipts byte-for-byte.
- Hardware: nproc=4, CPU-only; free RAM 14 GiB (>= 11 GiB precondition for 14B); free disk 86 GiB (>= 15 GiB precondition).

Candidates with pinned identities (URLs verified at DESIGN; shas from parent receipt or computed at download):

| candidate_id | model / quant | files | bytes | sha256 (source) | URL (resolve-redirect) |
|---|---|---|---|---|---|
| M-7B-QWEN | Qwen2.5-7B-Instruct Q4_K_M | 00001-of-00002, 00002-of-00002 | 3,993,201,344 / 689,872,288 | dfce12e3...580db, 539cf93f...3d72a (parent raw/gguf_sha256.txt) | https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf (+ -00002-of-00002.gguf) |
| M-3B-QWEN | Qwen2.5-3B-Instruct Q4_K_M | single | 2,104,932,768 | 626b4a66...615c62d (parent raw/gguf_sha256.txt) | https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf |
| M-14B-QWEN (conditional) | Qwen2.5-14B-Instruct Q4_K_M | 00001-of-00003, 00002-of-00003, 00003-of-00003 | 3,991,999,872 / 3,989,373,504 / 1,006,737,120 | computed at download, recorded in provenance | https://huggingface.co/Qwen/Qwen2.5-14B-Instruct-GGUF/resolve/main/qwen2.5-14b-instruct-q4_k_m-00001-of-00003.gguf (+ -00002-of-00003.gguf, -00003-of-00003.gguf) |

If a shard download hash mismatch occurs, the run is NOT_MEASURED with fingerprint `SHA-MISMATCH`, never substituted.

---

## 4. Frozen Task and Prompts (single-variable ablation)

Task: `MIN-WEBAGENT-CLICK-REVEAL-ANSWER` — synthetic page served via local python http.server on 127.0.0.1 random port. Page HTML byte-identical to the parent fixture (`harness_config.json.task.page_html`):

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

Max steps per episode: 5. Threshold: final answer text == `TARGET-42`.

Action schema (frozen, identical to parent): `click` requires `action` + `selector`; `answer` requires `action` + `text`. Any parse error, schema violation, or missing required field = parse failure.

GBNF grammar (byte-identical to parent fixture `harness_config.json.gbnf_grammar`):

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

**Comparator system prompt (PR-UNDERSPEC)** — byte-identical to the parent fixture:

```
You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.
```

**Treatment system prompt (PR-SPECIFIED, parent-style)** — the single-variable change; goal + schema enumeration in the style of the grand-parent harness (EXP-INTEL-37973264582 `min_webagent.py`) adapted to the frozen `selector`-based schema:

```
You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<css selector>"} or {"action":"answer","text":"<code>"}. Click the reveal button to reveal the code, then answer it.
```

Sampling (identical to parent): temperature=0.0, max_tokens=512, n_ctx=2048, chat_format=`qwen`, llama_seed=42, base_seed=42, episode seed = 42 + episode_idx, 5 episodes per arm per model. CPU threads: 4.

The EXECUTE harness must construct its fixture such that the PR-UNDERSPEC and PR-SPECIFIED strings above are reproduced byte-for-byte (AUDIT-verifiable), and all other fixture fields are byte-identical to the parent `harness_config.json`.

---

## 5. Controls and Baselines (stable identifiers)

- **PC-JSON-CONSTRAINED-DECODING** (positive control, per candidate): 10/10 probes `Emit exactly: {"action":"click","selector":"#test"}` through the identical LlamaGrammar path; success = 10/10 syntactically valid JSON matching the action schema. Requirements: pass before candidate's task episodes.
- **NC-NO-MODEL-ACTION** (null control, 5 episodes): fixed invalid content producer (`I will click the button`); success criterion = 0% parseable, 0% completion (reproduction of parent).
- **B-RANDOM-ACTION** (random-baseline null, 5 episodes): uniform random from frozen action space `[click #reveal-btn, answer TARGET-41, answer TARGET-42, answer TARGET-43, answer unknown]`; expectation = chance-level success (~0%: correct answer requires preceding correct click and exact text), valid-JSON rate ~1.0 (parent reproduced: 5/5 valid JSON, 0/5 success).
- **CV-UNDERSPEC-REPLICATION** (within-experiment replication control, PRIMARY continuity gate): M-7B-QWEN and M-3B-QWEN under PR-UNDERSPEC in THIS harness. PASS iff per model: task_success_rate = 0/5 AND >= 4/5 episodes with step-0/step-1 reveal click AND >= 1 episode with the reveal-click loop signature (post-reveal hidden-element click or answer-without-reveal, final answer != TARGET-42). Deviation on either model (e.g., a clear, or a wholly novel trace) ⇒ MEASUREMENT_INVALID (environment/harness not behaviorally continuous with parent; ablation unidentifiable).
- **B-0.5B-QWEN-LOCAL** (carried negative): Qwen2.5-0.5B-Instruct Q4_K_M, 0% parseable on the task (EXP-INTEL-37973264582; not re-measured).
- **B-POLLINATIONS-PROXY** (carried negative, timestamp-bound): gpt-oss-20b via Pollinations anonymous proxy, empty/reasoning-only content, ~197-token cap (EXP-INTEL-37973264582; receipts not reproducible contracts; not re-measured).
- **B-UNDERSPEC-CARRIED** (comparator baseline): the parent's published 0/5 + 1.0 parseable numbers; re-anchored in-experiment by CV-UNDERSPEC-REPLICATION.

---

## 6. Measurement Protocol

Per-model sequence (fixed order): (1) model load + receipt; (2) PC-JSON-CONSTRAINED-DECODING (10/10); (3) 5 episodes PR-UNDERSPEC (replication) for M-7B-QWEN and M-3B-QWEN only (M-14B-QWEN has no parent replication reference, so it runs only PC then PR-SPECIFIED); (4) 5 episodes PR-SPECIFIED (treatment) for every measured candidate. Candidate order: M-7B-QWEN -> M-3B-QWEN -> [conditional] M-14B-QWEN. Early stop on first clear under PR-SPECIFIED (remaining candidates recorded NOT_ATTEMPTED-EARLY-STOP; never negatives).

Per episode: render user prompt; produce one action (model / null-random producer); parse (JSON schema + regex fallback both recorded); execute click (Playwright `eval_on_selector_all`, record click_selector and whether target visible after) or answer (record answer_text); repeat up to 5 steps or completion; record final_answer, seed, inference latency (mean over steps), completion tokens (mean over steps). Raw evidence per episode preserved (all fields of parent's episodes schema), appended to per-experiment artifacts.

Metrics (stable identifiers, reused from parent + two task-conversion metrics):

- `parseable_action_rate_step1` — fraction of episodes whose step-1 action parsed to valid schema JSON (0..1; bar threshold 0.6)
- `task_success_rate` — fraction of episodes with final answer == `TARGET-42` (bar threshold 0.6)
- `positive_control_pass_rate` — PC 10/10 required pre-task per candidate
- `answer_action_emission_rate` — NEW: fraction of episodes emitting >= 1 parseable `answer` action (the step-0 → click-then-answer conversion metric named by the mandate)
- `step0_reveal_click_rate` — fraction of episodes with a `click` on `#reveal-btn` at step 1 (parent observed 5/5)
- `mean_inference_latency_s`, `mean_completion_tokens` — economics/cost records per candidate
- `candidate_cleared_bar` (derived bool), `census_completed` (derived bool)

Success threshold (per candidate): cleared bar iff >= 3/5 episodes with BOTH step1-parseable >= 3/5 AND task success >= 3/5.

---

## 7. Formal Decision Rule

Run arms in order; evaluate in the order below. Exactly one outcome is written to `result.json.outcome` ∈ {SUPPORTS, FALSIFIES, MIXED, MEASUREMENT_INVALID}; `status` ∈ {COMPLETE, BLOCKED, MEASUREMENT_INVALID}.

1. If nodecode infra fails PC on BOTH M-7B-QWEN and M-3B-QWEN → OUTCOME=MEASUREMENT_INVALID (decoding infrastructure failure, not model capability). Candidates with PC-fail are NOT_MEASURED-PC-FAIL.
2. Run CV-UNDERSPEC-REPLICATION (7B, 3B). If either model under PR-UNDERSPEC CLEARS the bar or the loop signature is absent in both models → OUTCOME=MEASUREMENT_INVALID (environment not continuous with parent; ablation unidentifiable). Raw observations still reported.
3. Run treatment. If any measured candidate clears the bar under PR-SPECIFIED → OUTCOME=SUPPORTS (early stop; role/bar/hashes recorded). Readiness condition (3) satisfied by proven same-model driver; benchmark executable as frozen.
4. If replication passed and every measured candidate failed:
   - a. If M-14B-QWEN was attained and measured and failed → OUTCOME=FALSIFIES. Demonstrable ceiling = {M-0.5B-QWEN (carried), M-3B-QWEN, M-7B-QWEN, M-14B-QWEN, B-POLLINATIONS-PROXY (carried)} = the full credential-free endpoint/model set actually available (E-LOCAL-LLAMA range + E-POLLINATIONS-OPENAI; models.github.ai is an interception, not an endpoint). Issue explicit close/re-scope recommendation (below).
   - b. If M-14B-QWEN was NOT attempted or failed attainment/measurement (NOT_ATTEMPTED-URL / NOT_ATTEMPTED-RAM / NOT_ATTEMPTED-DISK / NOT_MEASURED-RUN_ERROR / NOT_MEASURED-PC-FAIL) → OUTCOME=MIXED. Negative bounded strictly to measured set {0.5B carried, 3B, 7B} + carried proxy; 14B explicitly UNRESOLVED. Close/re-scope recommendation still issued with strength caveat.
5. Infrastructure failures (build failure without acceptable fallback, playwright/chrome failure, server failure) → OUTCOME=MEASUREMENT_INVALID with exact failure string; never a scientific negative. Status=BLOCKED only if failure precedes any measurement.

Close/re-scope recommendation (deliverable, written to report.md regardless of positive/negative direction): if SUPPORTS → benchmark executable as frozen with the proven driver; if FALSIFIES/MIXED → readiness condition (3) is NOT satisfiable on the credential-free path; re-scope the four-arm C-LLM-INHERIT benchmark off the credential-free path: drop Gate 3's same-model external published-baseline anchor; require internally re-run comparators (same harness, frozen seeds) on a task bank with demonstrable dynamic range (cold and retrieval arms must NOT saturate at 1.0 at high novelty, per EXP-PRODUCT-37973256064 / EXP-PRODUCT-37950607128).

---

## 8. Bounded External Published-Envelope Check (Q-EXT-1/2/3)

Purpose: contextualize the close/re-scope recommendation with the published capability envelope for comparably sized (<14B open-weight) models. This is NOT a SPIDER measurement and is NOT reproduced; it cannot alter the packet outcome. Three pre-registered queries, run once during EXECUTE with the available web search tool:

- Q-EXT-1: `open weights small model browser agent task success rate WebArena 3B 7B 8B 14B`
- Q-EXT-2: `Qwen2.5 7B 14B function calling tool use accuracy benchmark BFCL`
- Q-EXT-3: `small local LLM agent success rate Mind2Web WebVoyager 2025 2026 published results`

Source classification per hit: `PAPER_EVIDENCE` (peer-reviewed/arXiv with explicit SR and N), `REPO_EVIDENCE` (official model/benchmark leaderboards with methodology), `BLOG_EVIDENCE` (unstructured claim), `UNAVAILABLE` (search failed). Record the top 3 per query with numbers and denominators. Anchor starting reference from pre-2.0 Codex (PAPER_EVIDENCE, NOT reproduced by SPIDER): WebArena avg success 37.5% GPT-4.1 / 24.3% Qwen3-4B (AWM/ASI/CER-style scaffolding, arXiv:2606.04391). Results appear only in report.md under a labeled external section and `validity_notes`; no citation is transferred to any claim update without DIRECTOR adjudication.

---

## 9. Validity Threats and Mitigations

- **Version drift (llama.cpp/playwright/chrome)**: pinned versions identical to parent (0.2.90, 1.63.0, chrome 154.0.8037.97). Fallback (0.3.x wheel) only on sdist build failure, gated by CV-UNDERSPEC-REPLICATION. Any drift that changes the replication trace ⇒ MEASUREMENT_INVALID.
- **Prompt-identity confound**: the treatment prompt is a fixed static string frozen in this prereg; the harness constructs it with no discretion; AUDIT re-verifies byte equality. The ablation is single-variable by construction (all other fixture fields byte-identical to the bound parent fixture).
- **Determinism/randomness**: temp=0, fixed seeds (42-46); the parent showed 5/5 uniform traces under these settings; any non-determinism appears as mixed traces and is recorded as an observation, not used to rescue an outcome.
- **Census completeness**: NOT_ATTEMPTED/NOT_MEASURED are records with reasons, never negatives. 14B excluded by RAM/URL/disk gates ⇒ MIXED (not FALSIFIES) with explicit UNRESOLVED.
- **Chance-level success**: B-RANDOM-ACTION establishes chance floor; bar thresholds (0.6) are above any plausible chance rate for exact-text completion after click.
- **Verification tautology**: success requires `TARGET-42` extracted from the actual page after the reveal click; a model answering from prior knowledge without the click yields the wrong context (target hidden ⇒ not in PAGE_TEXT/ELEMENTS).
- **Carried evidence decay**: Pollinations receipts are timestamp-bound; this design does not rely on them beyond the negative baseline already established by the audit.
- **Measurement vs infrastructure failure**: all failure modes map to explicit categories (NOT_MEASURED-*, MEASUREMENT_INVALID) per the decision rule; infrastructure failure is never encoded as a scientific negative.

---

## 10. Representation Loss Disclosure

- The synthetic two-step page is an extreme minimal instance of the Web-agent task class; results do not generalize to arbitrary multi-step web tasks (no claim beyond the minimal task is intended).
- Only Qwen2.5 family and the gpt-oss-20b proxy are in the obtainable credential-free set; "all credential-free models" means all obtainable via the confirmed route, not all open-weight models ever published.
- Constrained decoding forces JSON structure; the measured ability is reasoning+task completion under grammar constraints, not free-form formatting.
- The 14B arm, if unattainable, bounds the census to ≤7B and is so labeled.
- External published-envelope numbers carry their own publication context and are labeled NOT reproduced.

---

## 11. Scope Boundaries (Explicitly NOT Done)

- No new endpoint provisioning, Docker/ollama routes, GPU, paid APIs, or human-issued credentials.
- No candidate/prompt/grammar/seed additions after freeze.
- No measurement of C-PRODUCT-ECON economics, kernel promotion, or four-arm benchmark execution (downstream, gated on this result).
- No re-litigation of the audited negative baselines (0.5B, Pollinations).
- No promotion of any endpoint into Product Core.

---

## 12. Dependencies on Frozen Upstream Evidence

- Parent packet `EXP-INTEL-37982024058` spec/prereg/result/audit/provenance/raw (fixture + receipts + hashes) — bound via freeze_artifacts.
- `research/intel/run_exp_37982024058.py` — audited ancestor harness; the EXECUTE harness for this experiment is a minimal parameterized fork constrained to: (a) same modes/parsing/verification/page-server logic, (b) parameterization of system prompt per arm and per-candidate URL shards, (c) outdir = this experiment's dir. All other logic byte-preserved unless removal is required for the parameterization and is documented in provenance.
- Pre-2.0 Codex PAPER_EVIDENCE (WebArena numbers) as external-check anchor only.
- `codex/claim_state.json.effective_event_by_claim` — C-LLM-INHERIT HYPOTHESIS (current effective event: EXP-INTEL-37982024058 FALSIFIES).

---

## 13. Pre-Registered Analysis Plan (No Post-Hoc Changes)

- All rates computed as simple fractions over the frozen 5-episode arm; no ad-hoc filtering of episodes.
- Bar clearing threshold fixed (>= 3/5 both metrics) before results are read.
- Outcome selected by the formal rule in section 7; no post-hoc branch invention, no weakening of the falsifier after seeing outcomes.
- report.md may interpret but must not silently contradict result.json or exceed the frozen claim.

---

## 14. Artifacts to Produce (Raw Evidence)

Under `research/experiments/EXP-INTEL-38013769440/`:

- `raw/harness_config.json` — this experiment's fixture (must equal the parent fixture byte-for-byte except `prompts.system` per arm, plus candidate URLs/shas for 14B; AUDIT-verifiable against this prereg).
- `raw/model_receipts.json` — per candidate: load time, gguf sha256 (all shards), positive_control result.
- `raw/task_episodes.json` — per candidate per arm per episode: full trace (prompt, raw completion, parsed action, regex action, clicked selector, visibility, token/latency stats, final answer, seed).
- `raw/control_episodes.json` — NC + B-RANDOM episodes.
- `raw/provisioning_evidence.json` — download attrs (URL, bytes, sha256) and attainment-gate records for 14B (reason codes NOT_ATTEMPTED-URL/RAM/DISK if any).
- `result.json` (packet schema v1), `report.md`, `provenance.json`.

---

## 15. Handoff Preparation

`handoff.json` will preserve: established (prompt ablation outcome per candidate; PC/NC/random/replication control results; census completeness; cost records), rejected (any re-scope assumptions invalidated), unknown (14B if unmeasured; external envelope classification), and do_not_assume (no cross-model generalization, no endpoint promotion, no benchmark execution authorization).

---

## 16. Signatures

- Design: big-pickle (opencode/big-pickle), DESIGN mode, lane intel.
- No outcome-bearing measurements were performed during DESIGN; all environment probes were non-outcome-bearing satisfiability checks recorded in sections 3 and 9.